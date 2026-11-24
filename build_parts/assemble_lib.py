"""Step 7 assembly library (no main, no save on import): pose numbers, placements, shape loading, document writing, placement audit.
Used by assemble.py (poses, ledger, nominal output) and assemble_ws.py (planted states).

Frame: datum A (frame top plane, base plate underside) at z = 0, z up, origin on the datum B axis. Floor-frame heights (holder bottom above the
receiver floor, nut z0, core bottom) add icd.floor_above_datum_a.
One base pose per size: R. Kd1 and Kmax come from R by the screw motion S(phi) = Rz(phi) T(0, 0, L phi / 2 pi), L = thread.pitch (single start):
nut(P) = S(phi) nut(R), washer(P) = S(phi) washer(R). The holder moves by T(0, 0, dz) only; base, frame, bracket, tnut and cutter do not move.
phi = 360 dz / L, dz = nut z0(P) - nut z0(R), both from params (pose.*, seat.*, holder.*, witness.*). Placements are explicit and non-baked: every
object is a Part::Feature carrying the part shape in its own frame plus a Placement; the audit compares Placement.Matrix to the ledger.
"""
import importlib.util
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import cadlib as C  # noqa: E402
import common  # noqa: E402

ROOT = common.ROOT
CACHE = common.PARTS_CACHE
ASM = CACHE / "assembly"
OUT = ROOT / "output"
RESULTS = ROOT / "results"
LEDGER = RESULTS / "assembly_poses.json"
POSES = ("R", "Kd1", "Kmax")
PARTS = ("base", "holder", "collet", "nut", "washer", "core", "frame", "bracket", "tnut", "cutter")
FIXED = ("base", "frame", "bracket", "tnut", "cutter")
# L4 (DECLARED context placement): accessories stand beside the frame on the floor line, this far off the frame envelope.
CONTEXT_OFFSET = 100.0


def G(p, k):
    return common.get(p, k)


def tag(d):
    """Collet file tag (collet.file_name_pattern collet_{int}p{frac}), three-digit integer part."""
    whole = int(math.floor(d + 1e-9))
    return "%03dp%d" % (whole, int(round((d - whole) * 10)))


def lead(p):
    return G(p, "thread.pitch") * G(p, "thread.starts") if _has(p, "thread.starts") else G(p, "thread.pitch")


def _has(p, k):
    try:
        G(p, k)
        return True
    except KeyError:
        return False


# ----------------------------------------------------------------------------- numbers
def pose_numbers(p, d, pose):
    """All pose numbers for size d and pose P, no geometry. nut_z, washer_z, holder_z, core_z are datum A heights (z of the part origin)."""
    zf = G(p, "icd.floor_above_datum_a")
    hb = {"R": G(p, "seat.holder_bottom_R"),
          "Kd1": G(p, "seat.holder_bottom_R") - (G(p, "holder.stroke_gap_R") - G(p, "witness.zone_high")),
          "Kmax": G(p, "holder.bottom_above_floor_Kmax")}
    over = {"R": G(p, "pose.nut_over_holder_R"), "Kd1": G(p, "pose.nut_over_holder_K"), "Kmax": G(p, "pose.nut_over_holder_K")}
    nut_z = {k: zf + hb[k] + over[k] for k in POSES}
    L = lead(p)
    dz = nut_z[pose] - nut_z["R"]
    phi = 360.0 * dz / L
    core_d = d + {"R": 0.0, "Kd1": G(p, "collet.grip_window_hi"), "Kmax": G(p, "collet.grip_window_lo")}[pose]
    ledge = G(p, "collet.core_seat_height")
    core_z = zf + ledge + (G(p, "pose.core_lift_R") if pose == "R" else G(p, "fit.model_contact_gap"))
    return {"d": d, "tag": tag(d), "pose": pose, "zf": zf, "holder_z": zf + hb[pose], "nut_z_R": nut_z["R"], "nut_z": nut_z[pose],
            "washer_z_R": nut_z["R"] + G(p, "pose.washer_z_in_nut"), "dz": dz, "phi_deg": phi, "core_d": core_d, "core_z": core_z,
            "phi_R_deg": G(p, "pose.nut_phi_R_deg"), "frame_dz": G(p, "pose.frame_dz"), "lead": L}


def placements(p, d, pose):
    """{part: App.Placement} for the ten parts."""
    import FreeCAD as App
    n = pose_numbers(p, d, pose)
    V, Z = App.Vector, App.Vector(0, 0, 1)
    s = App.Placement(V(0, 0, n["dz"]), App.Rotation(Z, n["phi_deg"]))       # S(phi) = Rz(phi) T(0, 0, dz); the two commute (shared axis)
    nut_r = App.Placement(V(0, 0, n["nut_z_R"]), App.Rotation(Z, n["phi_R_deg"]))
    washer_r = App.Placement(V(0, 0, n["washer_z_R"]), App.Rotation(Z, n["phi_R_deg"]))
    fr = App.Placement(V(0, 0, n["frame_dz"]), App.Rotation())
    return {"base": App.Placement(), "holder": App.Placement(V(0, 0, n["holder_z"]), App.Rotation()),
            "collet": App.Placement(V(0, 0, n["zf"]), App.Rotation()), "nut": s.multiply(nut_r), "washer": s.multiply(washer_r),
            "core": App.Placement(V(0, 0, n["core_z"]), App.Rotation()), "frame": fr, "bracket": App.Placement(fr), "tnut": App.Placement(fr),
            "cutter": App.Placement()}


def matrix_rows(pl):
    a = pl.Matrix.A
    return [[a[4 * i + j] for j in range(4)] for i in range(4)]


# ----------------------------------------------------------------------------- shapes
_CACHE = {}


def _open(name):
    import FreeCAD as App
    return App.openDocument(str(CACHE / (name + ".FCStd")))


def part_shape(name):
    """Final shape of parts_cache/<name>.FCStd (Body: final solid, otherwise the first Part::Feature named Body). Local frame, read only."""
    if name in _CACHE:
        return _CACHE[name].copy()
    import FreeCAD as App
    doc = _open(name)
    o = doc.getObject("Body")
    sh = C.final_shape(o) if o.TypeId == "PartDesign::Body" else o.Shape.copy()
    sh.Placement = App.Placement()
    App.closeDocument(doc.Name)
    _CACHE[name] = sh
    return sh.copy()


def frame_shapes():
    """(member, bracket, tnut) compounds and their instance names in solid order, from parts_cache/frame.FCStd (global coordinates, unshifted)."""
    import Part
    import FreeCAD as App
    if "frame.FCStd" in _CACHE:
        return tuple(_CACHE["frame.FCStd"])
    doc = _open("frame")
    kinds = {"member": [], "bracket": [], "tnut": []}
    for o in doc.Objects:
        for k in kinds:
            if o.Name.startswith(k + "_") and hasattr(o, "Shape") and o.Shape.Solids:
                kinds[k].append((o.Name, o.Shape.copy()))
    App.closeDocument(doc.Name)
    comps = {k: Part.makeCompound([s for _, s in v]) for k, v in kinds.items()}
    names = {k: [n for n, _ in v] for k, v in kinds.items()}
    _CACHE["frame.FCStd"] = (comps["member"], comps["bracket"], comps["tnut"], names)
    return comps["member"], comps["bracket"], comps["tnut"], names


def load_core_lib():
    """core.py loaded under another module name: its guard runs build() (and saves core.FCStd) when imported as `core`."""
    spec = importlib.util.spec_from_file_location("core_lib", os.path.join(HERE, "core.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def collet_name(d, pose):
    return "collet_%s" % tag(d) if pose == "R" else "collet_%s_clamped_%s" % (tag(d), pose)


def base_shape(p):
    """Compound(receiver T(0,0,floor offset), plate identity): receiver and plate stay two solids (0.2 radial gap, A3b spigot fit)."""
    import Part
    import FreeCAD as App
    rec = part_shape("receiver")
    rec.translate(App.Vector(0, 0, G(p, "icd.floor_above_datum_a")))
    return Part.makeCompound([rec, part_shape("base")])


def local_shapes(p, d, pose, core_lib=None):
    """{part: shape in the part's own frame} for the ten parts; the frame group is the unshifted global compound."""
    members, brackets, tnuts, _ = frame_shapes()
    core_lib = core_lib or load_core_lib()
    n = pose_numbers(p, d, pose)
    return {"base": base_shape(p), "holder": part_shape("holder"), "collet": part_shape(collet_name(d, pose)), "nut": part_shape("nut"),
            "washer": part_shape("washer"), "core": core_lib.make_core(n["core_d"], G(p, "core.length_capture"), p),
            "frame": members.copy(), "bracket": brackets.copy(), "tnut": tnuts.copy(), "cutter": part_shape("cutter")}


# ----------------------------------------------------------------------------- documents
def new_pose_doc(name, shapes, pls, extra=None):
    """Document with one Part::Feature per name (Name = Label), Shape in the part frame, Placement explicit."""
    import FreeCAD as App
    doc = App.newDocument(name)
    order = list(PARTS) + [k for k in (extra or {}) if k not in PARTS]
    for nm in order:
        o = doc.addObject("Part::Feature", nm)
        o.Label = nm
        o.Shape = shapes[nm]
        o.Placement = pls[nm]
        o.Visibility = True
    doc.recompute()
    return doc


def save_doc(doc, path):
    """saveAs without a .FCBak: an existing target is removed first."""
    path = str(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        os.remove(path)
    doc.saveAs(path)


def audit(doc, pls, tol=1e-9):
    """Placement audit (llm_plm_cad 7.5, Topologist E2): every object's Placement.Matrix against the expected matrix; non-identity placements listed."""
    import FreeCAD as App
    ident = App.Placement().Matrix.A
    rows, worst = [], 0.0
    for o in doc.Objects:
        if not hasattr(o, "Shape"):
            continue
        want = pls.get(o.Name)
        got = o.Placement.Matrix.A
        diff = max(abs(a - b) for a, b in zip(got, want.Matrix.A)) if want is not None else None
        is_id = max(abs(a - b) for a, b in zip(got, ident)) <= tol
        phi = math.degrees(math.atan2(got[4], got[0]))
        rows.append({"name": o.Name, "matches_ledger": diff is not None and diff <= tol, "diff": diff, "identity": is_id, "phi_mod360_deg": phi,
                     "z": got[11], "volume": o.Shape.Volume, "faces": len(o.Shape.Faces), "solids": len(o.Shape.Solids),
                     "bbox_plain_z": [o.Shape.BoundBox.ZMin, o.Shape.BoundBox.ZMax], "bbox_optimal_z": _opt_z(o.Shape)})
        if diff is not None:
            worst = max(worst, diff)
    return {"objects": rows, "max_diff": worst, "all_match": all(r["matches_ledger"] for r in rows), "non_identity": [r["name"] for r in rows if not r["identity"]]}


def _opt_z(sh):
    bb = C.bbox(sh)
    return [bb.ZMin, bb.ZMax]


def ledger_entry(p, d, pose):
    n = pose_numbers(p, d, pose)
    pls = placements(p, d, pose)
    return {"phi_deg": n["phi_deg"], "dz_mm": n["dz"], "nut_azimuth_deg": n["phi_R_deg"] + n["phi_deg"], "nut_z0_floor_frame": n["nut_z"] - n["zf"],
            "holder_bottom_floor_frame": n["holder_z"] - n["zf"], "core_d": n["core_d"], "placements": {k: matrix_rows(v) for k, v in pls.items()}}


def write_ledger(p):
    """results/assembly_poses.json: lead, base pose (nominal R), per-size per-pose phi, dz and 4x4 matrices, instance names, ws metadata kept if present."""
    sizes = list(G(p, "core.diameters"))
    nominal = G(p, "core.diameter_nominal")
    members, brackets, tnuts, names = frame_shapes()
    led = {"sentinel": "LEDGER_OK", "generated_by": "build_parts/assemble.py (ledger mode)", "lead_mm": lead(p),
           "basis": "nut(P) = S(phi) nut(R), S(phi) = Rz(phi) T(0,0,L phi / 2 pi); phi, dz negative for a clockwise turn from R; unwrapped phi",
           "base_pose": {k: matrix_rows(v) for k, v in placements(p, nominal, "R").items()},
           "sizes": {tag(d): {pose: ledger_entry(p, d, pose) for pose in POSES} for d in sizes},
           "instances": {"member": names["member"], "bracket": names["bracket"], "tnut": names["tnut"]}, "ws": {}}
    if LEDGER.exists():
        try:
            led["ws"] = json.loads(LEDGER.read_text(encoding="utf-8")).get("ws", {})
        except Exception:
            pass
    os.makedirs(RESULTS, exist_ok=True)
    LEDGER.write_text(json.dumps(led, indent=1), encoding="utf-8")
    return led


def log(msg):
    print(msg, flush=True)
