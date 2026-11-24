"""Planted wrong states WS1 to WS11 and the zero control (G2, G3). For each parts_cache/assembly/ws<n>.FCStd the probe runs the same pose analysis as
probe_poses.py (analyse) and evaluates the six gates A1, A3, T1, T9, F1, F3 with gates.fired. Output results/probes/ws<n>.json:
  {pose, tag, fired: [gate...], reasons: {gate: [text...]}, expected: [gate...]}.
ws0.json is the zero control: the unplanted poses R, Kd1, Kmax at the nominal size, evaluated with strict=True (an absent pair fires A1):
  {fired: [], fired_by_pose: {R: [], Kd1: [], Kmax: []}}.

GATE DEFINITIONS (gates.fired; thresholds from params.yaml and ASSEMBLY.md through gates.thresholds)
 A1  any of the 45 part pairs or 6 feature pairs violates its class for the pose (check_class, check_feature_gap).
 A3  holder_bottom_above_floor off its pose value by more than 0.05; nut_skirt_bottom_above_floor < thread.pitch; engaged_mm below
     thread.min_engage_pitches x pitch; K poses: core_axis_offset > icd.core_axis_offset_max or clamped_tilt_deg > register.clamped_tilt_max_deg;
     receiver_underside_contact_mm2 > 0; frame footprint off icd.footprint_x / _y by more than 0.05.
 T1  base|nut common volume >= 0.01 mm3 (thread flanks interfere: opposite hand, nut inverted) or engaged_mm == 0.
 T9  nut_tilt_deg or holder_tilt_deg > register.tilt_limit_deg (cross-thread tilt).
 F1  K poses: holder|collet overlap >= 0.01 or contact area <= seat.min_contact_area; R: holder|collet min_dist off fit.seat_clearance by > 0.05.
 F3  collet|core overlap >= 0.01, or (K poses) collet|core contact area == 0 (core rejected or not gripped).
EXPECTED FIRING per planted state (gates.WS_EXPECT; the fired set must meet it and stay inside the six gates):
 WS1 collet upside down A1/F1; WS2 holder upside down A1/A3; WS3 nut upside down A1/T1; WS4 wrong-hand thread T1/A1; WS5 cross-threaded tilt T9/T1;
 WS6 wrong collet for core F3/A1; WS7 collet unseated A1/F1; WS8 holder bottomed A1/A3; WS9 nut bottomed on base A3/A1;
 WS10 base on frame upside down A1/A3; WS11 slit over key F1/A1.
Run: freecadcmd tests/probes/probe_ws.py   (env CJ_WS=2,3 limits the states; CJ_WS=none runs only ws0)
Run: freecadcmd tests/probes/probe_ws.py   (detach it). Smoke override: CJ_POSE_DIR, CJ_OUT, CJ_LEDGER as in probe_poses.py."""
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["CJ_PROBE_IMPORT"] = "1"   # importing probe_poses must not run its sweep (freecadcmd names a script run by its module name)
import probe_poses as PP  # noqa: E402
import probe_lib as L  # noqa: E402
import gates  # noqa: E402
C = L.C
DEFAULT_POSE = {8: "Kmax", 9: "Kmax"}


def shapes_of(doc):
    return {o.Label: C.final_shape(o) if o.TypeId == "PartDesign::Body" else o.Shape.copy() for o in doc.Objects
            if hasattr(o, "Shape") and o.Shape.Solids}


def main():
    import FreeCAD as App
    p = L.params()
    rels, feats = gates.parse_assembly()
    T = gates.thresholds(lambda k: L.G(p, k), rels, feats)
    pairs = [(r["a"], r["b"]) for r in rels]
    led = json.load(open(PP.LEDGER, encoding="utf-8")) if os.path.exists(PP.LEDGER) else {}
    nominal = L.G(p, "core.diameter_nominal")
    nom_tag = "%03dp%d" % (int(math.floor(nominal + 1e-9)), int(round((nominal - math.floor(nominal + 1e-9)) * 10)))
    for path in sorted(glob.glob(os.path.join(PP.POSE_DIR, "ws*.FCStd"))):
        m = re.match(r"ws(\d+)\.FCStd$", os.path.basename(path))
        if not m:
            continue
        n = int(m.group(1))
        if os.environ.get("CJ_WS") and str(n) not in os.environ["CJ_WS"].split(","):
            continue                                  # CJ_WS=2,3 runs only those states; CJ_WS=none runs only the zero control
        meta = led.get("ws", {}).get(str(n), {})
        pose = meta.get("pose", DEFAULT_POSE.get(n, "Kd1"))
        doc = App.openDocument(path)
        out = PP.analyse(shapes_of(doc), p, pairs)
        f = gates.fired(out, pose, T)
        L.finish("ws%d" % n, {"pose": pose, "tag": meta.get("tag", nom_tag), "fired": sorted(f), "reasons": f,
                              "expected": sorted(gates.WS_EXPECT[n]), "absent": out["absent"]}, [path])
        App.closeDocument(doc.Name)
    if os.environ.get("CJ_WS") and os.environ["CJ_WS"] != "none" and os.environ.get("CJ_WS0") != "1":
        return                                        # state subset: the zero control belongs to the run without CJ_WS (or with CJ_WS0=1)
    by_pose, Ts = {}, dict(T, strict=True)
    for pose in gates.POSE_IDX:
        path = os.path.join(PP.POSE_DIR, "pose_%s_%s.FCStd" % (pose, nom_tag))
        if os.path.exists(path):
            doc = App.openDocument(path)
            out = PP.analyse(shapes_of(doc), p, pairs)
            by_pose[pose] = gates.fired(out, pose, Ts)
            App.closeDocument(doc.Name)
    if by_pose:
        L.finish("ws0", {"fired": sorted({g for f in by_pose.values() for g in f}), "fired_by_pose": {k: sorted(v) for k, v in by_pose.items()},
                         "reasons": by_pose, "poses": sorted(by_pose)}, [])


if __name__ in ("__main__", "probe_ws"):
    L.guarded(main, "ws")
