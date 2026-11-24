"""Frame (FR1 to FR4). Datum A frame: origin at the plate centre, X along the rails, frame top plane z = 0, members z -profile.width to 0.
Six members from stock (whole pieces: rail 644 x2, end 488 x2, plate_support 468 x2), 12 brackets (8 purchased 14089 class, 4 printed 68 mm class),
96 T-nut proxies (8 per bracket, ASSUMED), datum C slot-line notch on rail_1 (Rule P). Document objects: member_<id>_<n>, bracket_<kind>_<n>, tnut_<n>.
Step 7 C6 option (a) (Loftsman L5): the four printed brackets on the support-member outer faces (x 142 to 210) are not built; the rail inner face has
room for the 57 mm purchased bracket only (need 740 mm against 644 mm). One printed bracket per plate-support-end joint, inboard."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402
import common  # noqa: E402
import hardware_geom as HG  # noqa: E402


def sgn(v):
    return 1.0 if v > 0 else -1.0


def place_member(shape_z, length, axis, cx, cy, half_w):
    """Profile extrusion (along +Z from 0) laid along X (axis 'x') or Y (axis 'y'), centred on (cx, cy), z from -2 half_w to 0."""
    s = shape_z.copy()
    if axis == "x":
        s.rotate(C.V(0, 0, 0), C.V(0, 1, 0), 90.0)
        s.translate(C.V(cx - length / 2.0, cy, -half_w))
    else:
        s.rotate(C.V(0, 0, 0), C.V(1, 0, 0), -90.0)
        s.translate(C.V(cx, cy - length / 2.0, -half_w))
    return s


def build():
    import FreeCAD as App
    import Part
    t0 = time.time()
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("frame")
    ov = g("collet.tool_overshoot")
    half_w = g("profile.width") / 2.0
    zc = -half_w
    rail_y = g("column.spacing") / 2.0
    members = g("frame.members")
    end_x, sup_x = g("frame.end_x"), g("frame.support_x")
    doc = App.newDocument("frame")
    mem_objs, br_objs, tn_objs = [], [], []
    # ---- FR1 members
    cent = {"rail": [(0.0, rail_y), (0.0, -rail_y)], "end": [(end_x, 0.0), (-end_x, 0.0)], "plate_support": [(sup_x, 0.0), (-sup_x, 0.0)]}
    axis = {"rail": "x", "end": "y", "plate_support": "y"}
    prof_t = {}
    for m in members:
        L = m["cut_mm"]
        t1 = time.time()
        base = common.build_profile(L, p)
        prof_t[m["id"]] = round(time.time() - t1, 1)
        for i in range(m["qty"]):
            cx, cy = cent[m["id"]][i]
            sh = place_member(base, L, axis[m["id"]], cx, cy, half_w)
            mem_objs.append({"name": f"member_{m['id']}_{i + 1}", "id": m["id"], "n": i + 1, "shape": sh, "L": L, "cx": cx, "cy": cy})
        print("member profile %s %.1fs" % (m["id"], time.time() - t1), flush=True)
    # ---- FR4 datum C slot-line notch on rail_1 (Rule P)
    nw, nl, nd = g("frame.notch")
    rail1 = [o for o in mem_objs if o["name"] == "member_rail_1"][0]
    L_r = rail1["L"]
    y_slot = rail1["cy"] - g("profile.slot_offset")
    notch = S.box(-L_r / 2 - ov, -L_r / 2 + nl, y_slot - nw / 2, y_slot + nw / 2, -nd, ov)
    v_before = rail1["shape"].Volume
    rail1["shape"] = S.solid_of(rec.cut("rail_1_notch", rail1["shape"], notch))
    notch_mm3 = v_before - rail1["shape"].Volume
    notch_exp = (nw - g("profile.slot_opening")) * nl * nd
    pk_lo = rail1["cy"] - half_w + g("profile.corner_hole_inset")                                   # profile corner pocket, y range
    notch_note = ("removed volume is %.2f mm2 x along short of the nominal: the notch edge at y %.0f breaks %.1f mm into the profile corner pocket "
                  "(y %.1f to %.1f, z -%.1f to -%.1f)" % ((notch_exp - notch_mm3) / nl, y_slot - nw / 2, y_slot - nw / 2 - pk_lo, pk_lo, pk_lo + g("profile.corner_hole_size"),
                                                          g("profile.corner_hole_inset"), g("profile.corner_hole_inset") + g("profile.corner_hole_size")))
    # ---- FR2 brackets, FR3 T-nuts
    tn_shape, _ = HG.tnut_shape(p, S.Rec("tnut_inst"))
    acr = g("bracket.across")
    pur_pos, prn_pos = g("bracket.holes_purchased"), g("bracket.slots_printed")
    y_c = g("icd.footprint_y") / 2.0 - g("profile.width")
    pw = g("profile.width") / 2.0
    spec = []
    for sx_ in (1, -1):
        for sy_ in (1, -1):
            cyp = sy_ * y_c
            spec.append(("purchased", sx_ * (end_x - pw), cyp, -sx_, -sy_))        # inboard: away from the end member, toward the plate
    for sx_ in (1, -1):
        for sy_ in (1, -1):
            spec.append(("purchased", sx_ * (end_x + pw), sy_ * y_c, sx_, -sy_))   # outboard
    for sx_ in (1, -1):
        for sy_ in (1, -1):
            spec.append(("printed", sx_ * (sup_x - pw), sy_ * y_c, -sx_, -sy_))    # support inner face
    counts = {"purchased": 0, "printed": 0}
    n_tn = 0
    for kind, cx, cy, sx, sy in spec:
        counts[kind] += 1
        sh, info = HG.bracket_shape(p, kind, cx, cy, float(sx), float(sy), zc, rec)
        br_objs.append({"name": f"bracket_{kind}_{counts[kind]}", "kind": kind, "shape": sh, "cx": cx, "cy": cy, "sx": sx, "sy": sy})
        pos = pur_pos if kind == "purchased" else prn_pos
        for a in pos:
            for dz in (-acr, acr):
                n_tn += 1
                tn_objs.append({"name": f"tnut_{n_tn}", "bracket": f"bracket_{kind}_{counts[kind]}", "leg": "rail",
                                "shape": S.placed(tn_shape, C.V(cx + sx * a, cy, zc + dz), C.V(1, 0, 0), C.V(0, sy, 0))})
                n_tn += 1
                tn_objs.append({"name": f"tnut_{n_tn}", "bracket": f"bracket_{kind}_{counts[kind]}", "leg": "cross",
                                "shape": S.placed(tn_shape, C.V(cx, cy + sy * a, zc + dz), C.V(0, 1, 0), C.V(sx, 0, 0))})
    # ---- document objects
    for o in mem_objs + br_objs + tn_objs:
        ob = doc.addObject("Part::Feature", o["name"])
        ob.Shape = o["shape"]
    doc.recompute()
    CACHE = C.CACHE
    CACHE.mkdir(exist_ok=True)
    doc.saveAs(str(CACHE / "frame.FCStd"))
    print("frame saved %.1fs" % (time.time() - t0), flush=True)

    # ---- checks and Pass 1 data
    allm = [o["shape"] for o in mem_objs]
    bbs = [s.BoundBox for s in allm]
    foot_x = max(b.XMax for b in bbs) - min(b.XMin for b in bbs)
    foot_y = max(b.YMax for b in bbs) - min(b.YMin for b in bbs)
    z_lo, z_hi = min(b.ZMin for b in bbs), max(b.ZMax for b in bbs)
    comp = Part.makeCompound(allm)
    stock = {s["length"]: s["qty"] for s in g("stock.on_hand")}
    alloc = [{"id": m["id"], "qty": m["qty"], "cut_mm": m["cut_mm"], "stock_piece_mm": m["source_mm"], "role": m["role"]} for m in members]
    used = {}
    for a in alloc:
        used[a["stock_piece_mm"]] = used.get(a["stock_piece_mm"], 0) + a["qty"]
    consumption = [{"stock_mm": L_, "on_hand": stock.get(L_, 0), "used": used.get(L_, 0), "left": stock.get(L_, 0) - used.get(L_, 0)} for L_ in sorted(stock, reverse=True)]
    mass_kg = sum(o["L"] for o in mem_objs) / 1000.0 * g("profile.mass_per_m_catalog")
    valid_all = all(o["shape"].isValid() and o["shape"].isClosed() and len(o["shape"].Solids) == 1 for o in mem_objs + br_objs + tn_objs)
    # overlaps (C6 and Step 7 inputs): bracket-bracket, bracket-member, T-nut pairs at bracket-bracket sites
    ovl = []
    def bb_hit(a, b):
        A, B = a.BoundBox, b.BoundBox
        return not (A.XMax <= B.XMin or B.XMax <= A.XMin or A.YMax <= B.YMin or B.YMax <= A.YMin or A.ZMax <= B.ZMin or B.ZMax <= A.ZMin)
    for i, a in enumerate(br_objs):
        for b in br_objs[i + 1:]:
            if bb_hit(a["shape"], b["shape"]):
                v = a["shape"].common(b["shape"]).Volume
                if v > S.TOL:
                    ovl.append({"a": a["name"], "b": b["name"], "volume_mm3": round(v, 1)})
        for m in mem_objs:
            if bb_hit(a["shape"], m["shape"]):
                v = a["shape"].common(m["shape"]).Volume
                if v > S.TOL:
                    ovl.append({"a": a["name"], "b": m["name"], "volume_mm3": round(v, 1)})
    tn_pairs = []
    for i, a in enumerate(tn_objs):
        for b in tn_objs[i + 1:]:
            if bb_hit(a["shape"], b["shape"]):
                v = a["shape"].common(b["shape"]).Volume
                if v > S.TOL:
                    tn_pairs.append({"a": a["name"], "b": b["name"], "volume_mm3": round(v, 1)})
    sample = {}
    n_corner = len({(b["sx"], b["sy"]) for b in br_objs})
    per_b = g("hardware.tnuts_per_bracket")
    names = ["tnut_%d" % (per_b * bi + k + 1) for bi in range(0, len(br_objs), len(br_objs) // n_corner) for k in range(2)]       # first two T-nuts of one bracket per frame corner
    for nm in names:
        t = [o for o in tn_objs if o["name"] == nm][0]
        host = [m for m in mem_objs if bb_hit(t["shape"], m["shape"])]
        sample[nm] = [{"member": m["name"], "overlap_mm3": round(t["shape"].common(m["shape"]).Volume, 2)} for m in host]
    br_vs = {"purchased_inboard_vs_printed_outer": [o for o in ovl if o["a"].startswith("bracket_purchased") and o["b"].startswith("bracket_printed")],
             "printed_vs_end_member": [o for o in ovl if o["a"].startswith("bracket_printed") and o["b"].startswith("member_end")]}
    kinds = [b["kind"] for b in br_objs]
    mem_rows = []
    for m in members:
        got = [o for o in mem_objs if o["id"] == m["id"]]
        okL = all(abs(max(o["shape"].BoundBox.XLength, o["shape"].BoundBox.YLength) - m["cut_mm"]) <= 0.05 for o in got)
        mem_rows.append((m["id"], len(got), m["qty"], okL))
    vol_members = sum(o["shape"].Volume for o in mem_objs)
    rows = [
        S.row("FR1", "member count = sum frame.members qty", vol_members, len(mem_objs), sum(m["qty"] for m in members), S.TOL),
        S.row("FR1", "member lengths = frame.members cut_mm (all ids)", vol_members, int(all(r[3] for r in mem_rows)), 1, S.TOL, ok=all(r[3] for r in mem_rows)),
        S.row("FR1", "footprint x = icd.footprint_x", vol_members, foot_x, g("icd.footprint_x"), 0.05),
        S.row("FR1", "footprint y = icd.footprint_y", vol_members, foot_y, g("icd.footprint_y"), 0.05),
        S.row("FR1", "member z range: top at datum A (0), height profile.width", vol_members, z_hi - z_lo, g("profile.width"), S.TOL, ok=abs(z_hi) < S.TOL and abs((z_hi - z_lo) - g("profile.width")) < S.TOL),
        S.row("FR1", "stock allocation: whole pieces, none above quantity on hand", vol_members, int(all(c["left"] >= 0 for c in consumption)), 1, S.TOL,
              ok=all(c["left"] >= 0 for c in consumption) and all(a["stock_piece_mm"] == a["cut_mm"] for a in alloc)),
        S.row("FR2", "bracket count = purchased joints x brackets_per_joint + printed joints x printed_brackets_per_joint", sum(b["shape"].Volume for b in br_objs), len(br_objs),
              g("hardware.purchased_bracket_joints") * g("hardware.brackets_per_joint") + g("hardware.printed_bracket_joints") * g("hardware.printed_brackets_per_joint"), S.TOL),
        S.row("FR2", "purchased bracket count", sum(b["shape"].Volume for b in br_objs if b["kind"] == "purchased"), kinds.count("purchased"),
              g("hardware.purchased_bracket_joints") * g("hardware.brackets_per_joint"), S.TOL),
        S.row("FR2", "printed bracket count", sum(b["shape"].Volume for b in br_objs if b["kind"] == "printed"), kinds.count("printed"),
              g("hardware.printed_bracket_joints") * g("hardware.printed_brackets_per_joint"), S.TOL),
        S.row("FR3", "T-nut instances = hardware.tnuts_per_bracket x bracket count", sum(t["shape"].Volume for t in tn_objs), len(tn_objs),
              g("hardware.tnuts_per_bracket") * len(br_objs), S.TOL),
        S.row("FR4", "datum C notch volume removed from rail_1 = (notch across - slot opening) x along x depth", notch_mm3, notch_mm3, notch_exp, 0.02 * notch_exp,
              note=notch_note),
    ]
    res = S.result("frame", comp, rows, rec, extra={
        "solid_count_objects": len(mem_objs) + len(br_objs) + len(tn_objs), "all_objects_valid_closed_one_solid": valid_all,
        "allocation": alloc, "stock_consumption": consumption, "bracket_count": len(br_objs), "tnut_instances": len(tn_objs),
        "members": [{"name": o["name"], "volume_mm3": round(o["shape"].Volume, 1), "bbox": [round(v, 3) for v in (o["shape"].BoundBox.XMin, o["shape"].BoundBox.XMax,
                     o["shape"].BoundBox.YMin, o["shape"].BoundBox.YMax, o["shape"].BoundBox.ZMin, o["shape"].BoundBox.ZMax)]} for o in mem_objs],
        "mass_kg_stock": round(mass_kg, 3), "profile_seconds": prof_t, "datum_c_notch": {"member": "member_rail_1", "x": [-L_r / 2, -L_r / 2 + nl],
                     "y": [y_slot - nw / 2, y_slot + nw / 2], "z": [-nd, 0.0], "removed_mm3": round(notch_mm3, 1), "expected_mm3": notch_exp},
        "overlaps": ovl, "overlap_summary": {k: {"sites": len(v), "mm3_each_max": max([o["volume_mm3"] for o in v], default=0.0),
                                                  "mm3_total": round(sum(o["volume_mm3"] for o in v), 1)} for k, v in br_vs.items()},
        "tnut_pair_overlaps": {"pairs": len(tn_pairs), "mm3_total": round(sum(o["volume_mm3"] for o in tn_pairs), 1)}, "tnut_host_overlap_sample": sample,
        "bracket_positions": [{"name": b["name"], "corner": [b["cx"], b["cy"]], "sx": b["sx"], "sy": b["sy"]} for b in br_objs]})
    with open(CACHE / "frame_result.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    return res


if __name__ in ("__main__", "frame"):
    C.run_main("frame", build)
