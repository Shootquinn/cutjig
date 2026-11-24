"""Step 6 per-part measurements: validity, solid count, Euler record, volume, flipped-copy mismatch (Rule P), bbox.
Writes results/probes/step6_parts.json {part: {...}} (plug is its own part). Extra keys by part:
  holder   flange_scan{r: {az: interval_count}}, flange_interval, down_planar_z[] (z of downward-facing planar faces, area > 50 mm2)
  frame    members[{name, id, valid, closed, solids, volume, length, flip_mismatch_fraction}], brackets[{name, kind, valid, closed, solids}],
           tnut_instances, bbox [xmin, xmax, ymin, ymax]
  stop     pad_faces[{z, dx, dy}] (planar +/-Z faces, area > 100 mm2), common_with_nut_mm3
Frame FCStd contract: one solid object per member named member_<id>_<n>, per bracket bracket_<purchased|printed>_<n>, per T-nut tnut_<n>.
Run: freecadcmd tests/probes/probe_step6_parts.py"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
import glyph_math  # noqa: E402
C = L.C
PARTS = ("base", "tray", "plug", "foot", "tnut", "bracket_purchased", "bracket_printed", "caddy", "gauge", "rest", "stop", "receiver", "holder", "nut")


def flip_mismatch(sh, own_centre=False):
    """180 degree turn about a world-X parallel line. Parts on the Z axis turn about (0, 0, zmid); frame members turn about their own centre line."""
    bb = sh.BoundBox
    f = sh.copy()
    cy = (bb.YMin + bb.YMax) / 2.0 if own_centre else 0.0
    f.rotate(C.V(0, cy, (bb.ZMin + bb.ZMax) / 2.0), C.V(1, 0, 0), 180.0)
    return 1.0 - sh.common(f).Volume / sh.Volume


def basics(sh):
    bb = sh.BoundBox
    return {"valid": bool(sh.isValid()), "closed": bool(sh.isClosed()), "solids": len(sh.Solids), "shells": len(sh.Shells), "volume": sh.Volume,
            "euler_VEF": len(sh.Vertexes) - len(sh.Edges) + len(sh.Faces), "bbox": [bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax]}


def holder_extra(sh, p):
    G = lambda k: L.G(p, k)
    r0 = G("holder.insert_circle_radius") + G("holder.insert_dia") / 2 + 0.5
    r1 = G("holder.flange_od") / 2 - G("holder.index_notch_depth") - 0.5
    ref_az = (G("receiver.key_offset_deg") + 180.0) % 360.0
    z0, z1 = sh.BoundBox.ZMin - 1, sh.BoundBox.ZMax + 1
    # HD5 scan window starts above the key top (holder bottom + holder.key_length): the key (az key_offset, r to 70.04) lies below it,
    # so the flange annulus is scanned at every azimuth and the key is never in the window.
    zs = sh.BoundBox.ZMin + G("holder.key_length") + 1.0
    # HD6 flange interval read inside the flange annulus (r1 + 1 = 69.54), outside the tube wall (holder OD r 67.04).
    # Step 7: the collar ring (holder.FCStd, r 55.0 to 76.2 above the tube top) lies above the flange; both windows end at the flange top + 1.
    z_fl = G("holder.length") + G("holder.flange_thickness") + 1.0
    iv = C.axial_ivals(sh, ref_az, r1 + 1.0, z0, z_fl)
    scan = {}
    for k in range(3):
        r = r0 + (r1 - r0) * k / 2.0
        scan["%.2f" % r] = {str(az): len(C.axial_ivals(sh, float(az), r, zs, z_fl)) for az in range(0, 360, 3)}
    down = []
    for f in sh.Faces:
        if f.Surface.__class__.__name__ == "Plane" and f.Area > 50 and f.normalAt(0, 0).z < -0.99:
            down.append(round(f.CenterOfMass.z, 3))
    above = [z for z in down if z > z_fl]          # Step 7: the collar underside (nut plate catch face), the only downward face above the flange
    return {"flange_scan": scan, "flange_interval": iv[-1] if iv else None, "down_planar_z": sorted(set(down)), "collar_underside_z": min(above) if above else None}


def holder_controls(sh, p):
    """Known-bad holders run through the same measurement: a jacking hole through the flange annulus (HD5) and a hard-stop shoulder (HD6)."""
    G = lambda k: L.G(p, k)
    bb = sh.BoundBox
    r_mid = (G("holder.insert_circle_radius") + G("holder.insert_dia") / 2 + 0.5 + G("holder.flange_od") / 2 - G("holder.index_notch_depth") - 0.5) / 2
    import math
    import Part
    ang = math.radians(100.0)
    hole = Part.makeCylinder(2.0, bb.ZLength + 2, C.V(r_mid * math.cos(ang), r_mid * math.sin(ang), bb.ZMin - 1), C.V(0, 0, 1))
    shoulder = Part.makeCylinder(G("holder.flange_od") / 2 + 5, 3.0, C.V(0, 0, bb.ZMin + 30.0), C.V(0, 0, 1))
    return {"hole": holder_extra(sh.cut(hole), p), "shoulder": holder_extra(sh.fuse(shoulder), p)}


def rest_extra(sh, p):
    """D2: rest rebuilt at each core size (rest.shape_at); roller solids must not touch the core cylinder, and the pin slot must be cut in the ring."""
    import Part
    import importlib.util
    # rest.py runs and saves its build when imported under the name "rest" (its __main__ guard accepts that name); load it under another
    # name so the probe measures and never rewrites parts_cache/rest.FCStd.
    spec = importlib.util.spec_from_file_location("rest_readonly", os.path.join(L.ROOT, "build_parts", "rest.py"))
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    import step6lib as S6
    G = lambda k: L.G(p, k)
    lo, hi = G("rest.core_d_range")
    sizes = [lo] + [90.0 + 2.5 * k for k in range(7)] + [hi]
    r_lo, r_hi = G("rest.roller_r_range")
    z_lo, r_t = G("rest.ring_z_lo"), G("rest.ring")[2]
    z_slot = z_lo + G("rest.slot_depth")
    out = []
    for d in sizes:
        shp = R.shape_at(p, d, S6.Rec("rest"))
        core = Part.makeCylinder(d / 2.0, 400.0, C.V(0, 0, -200.0), C.V(0, 0, 1))
        r_c = R.roller_radius(G, d)
        y_s = G("rest.pin") / 2.0 + G("rest.slot_clear") / 2.0         # beside the pin, inside the slot's side clearance
        iv = [i for i in C.axial_ivals(shp, math.degrees(math.atan2(y_s, r_c)), math.hypot(r_c, y_s), z_lo - 1.0, z_lo + r_t + 1.0) if i[1] > z_lo + r_t - 0.1]
        out.append({"core_d": d, "valid": bool(shp.isValid()), "solids": len(shp.Solids), "common_with_core_mm3": shp.common(core).Volume,
                    "faces": len(shp.Faces), "ring_bottom_z_at_slot": iv[0][0] if iv else None, "slot_z_expected": z_slot, "ring_z_lo": z_lo})
    return {"sizes": out}


def stop_extra(sh, p):
    faces = []
    for f in sh.Faces:
        if f.Surface.__class__.__name__ == "Plane" and f.Area > 100 and abs(f.normalAt(0, 0).z) > 0.99:
            bb = f.BoundBox
            faces.append({"z": f.CenterOfMass.z, "dx": bb.XLength, "dy": bb.YLength})
    nut = L.part("nut")
    return {"pad_faces": faces, "common_with_nut_mm3": sh.common(nut).Volume}


def frame_probe(p):
    import FreeCAD as App
    doc = App.openDocument(os.path.join(L.CACHE, "frame.FCStd"))
    out = {"members": [], "brackets": [], "tnut_instances": 0}
    xs, ys = [], []
    for o in doc.Objects:
        if not hasattr(o, "Shape") or not o.Shape.Solids or not o.Name.startswith(("member_", "bracket_", "tnut_")):
            continue
        sh = o.Shape
        if o.Name.startswith("member_"):
            bb = sh.BoundBox
            xs += [bb.XMin, bb.XMax]
            ys += [bb.YMin, bb.YMax]
            out["members"].append({"name": o.Name, "id": glyph_math.member_id(o.Name), "valid": bool(sh.isValid()), "closed": bool(sh.isClosed()),
                                   "solids": len(sh.Solids), "volume": sh.Volume, "length": max(bb.XLength, bb.YLength, bb.ZLength),
                                   "flip_mismatch_fraction": flip_mismatch(sh, own_centre=True)})
        elif o.Name.startswith("bracket_"):
            out["brackets"].append({"name": o.Name, "kind": o.Name.split("_")[1], "valid": bool(sh.isValid()), "closed": bool(sh.isClosed()),
                                    "solids": len(sh.Solids)})
        else:
            out["tnut_instances"] += 1
    out["bbox"] = [min(xs), max(xs), min(ys), max(ys)] if xs else None
    return out


def main():
    p, out, inputs = L.params(), {}, []
    for name in PARTS:
        path = os.path.join(L.CACHE, name + ".FCStd")
        if not os.path.exists(path):
            continue
        t = time.time()
        sh, doc = L.open_shape(path)
        d = basics(sh)
        d["flip_mismatch_fraction"] = flip_mismatch(sh)
        if name == "holder":
            d.update(holder_extra(sh, p))
            d["controls"] = holder_controls(sh, p)
        if name == "rest":
            d.update(rest_extra(sh, p))
        if name == "stop":
            d.update(stop_extra(sh, p))
        out[name] = d
        inputs.append(path)
        print("PART %s %.1fs" % (name, time.time() - t), flush=True)
    fp = os.path.join(L.CACHE, "frame.FCStd")
    if os.path.exists(fp):
        out["frame"] = frame_probe(p)
        inputs.append(fp)
    L.finish("step6_parts", out, inputs)


if __name__ in ("__main__", "probe_step6_parts"):
    L.guarded(main, "step6_parts")
