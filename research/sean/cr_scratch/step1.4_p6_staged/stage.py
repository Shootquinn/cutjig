"""Stage the S1 r9 / S3 r8 spec edits (S4-b scope (i), x1_edits_at_p6) on scratch copies; record each edit as Old/New.
P2 edits (step1.4_engineer_spec.md section 5) re-run from the live s1/s3 with the s4 rows given, plus the P2f follow-ons:
Designer P3a FIX 5 (wing-nut note, S3 wing-nut shape and wing sub-artist, washer row in S1 and S3), Loftsman P3b FIX 2
(theta 90 window, S3 only: same plane), FIX 3 and 4 (relief, skirt: carried by the section_true copy from s4).
Usage: stage2.py <dir holding s4_spec.yaml> <out dir>. Live s1/s2/s3 are read from docs/sketches; s2 is copied unchanged."""
import json
import sys
from pathlib import Path
import yaml
D = Path(r"D:/Unleashed Robotics/cutjig/docs/sketches")
SRC4, S = Path(sys.argv[1]), Path(sys.argv[2])
S.mkdir(parents=True, exist_ok=True)
s4 = yaml.safe_load((SRC4 / "s4_spec.yaml").read_text(encoding="utf-8"))
rows4 = {r["id"]: r for r in s4["features"]}
WING_KEYS = ("wingnut.wing_height", "wingnut.wing_thickness")
WINDOW_KEYS = ("nut.washer_window_width", "nut.washer_window_count", "wingnut.wing_count")


def flow(v):
    s = yaml.safe_dump(v, default_flow_style=True, width=100000, sort_keys=False).strip()
    return s[:-3].strip() if s.endswith("\n...") else s


def st_block(rid, ind):
    lines = [f"{ind}section_true:"]
    for nm, pc in rows4[rid]["section_true"].items():
        lines.append(f"{ind}  {nm}: {flow(pc)}")
    return "\n".join(lines)


edits = {"s1": [], "s3": []}


def rep(name, t, old, new, why):
    assert t.count(old) == 1, (name, old[:90], t.count(old))
    edits[name].append({"why": why, "old": old, "new": new})
    return t.replace(old, new)


def row_span(t, rid, head):
    """(start, end) of the row text: from its '- id: rid' line to the next row head."""
    i = t.index(f"{head}- id: {rid}\n")
    j = t.index(f"{head}- id: ", i + 1)
    return i, j


def ins_in_row(name, t, rid, head, anchor, new, why):
    """Insert new after the first line starting with anchor inside row rid."""
    i, j = row_span(t, rid, head)
    k = t.index(anchor, i)
    assert k < j, (name, rid, anchor)
    e = t.index("\n", k) + 1
    edits[name].append({"why": why, "old": t[k:e].rstrip("\n") + f"  (row {rid})", "new": t[k:e] + new.rstrip("\n")})
    return t[:e] + new + t[e:]


Q = {"s1": '"', "s3": ""}
for name, ind in (("s1", "    "), ("s3", "  ")):
    q = Q[name]
    head = "  " if name == "s1" else ""
    t = (D / f"{name}_spec.yaml").read_text(encoding="utf-8")
    t = rep(name, t, f"z_rule: {{z_min: holder_bottom, z_max: {q}holder_bottom + holder.length + holder.flange_thickness{q}}}",
            f"z_rule: {{z_min: holder_bottom, z_max: {q}holder_bottom + holder.length + holder.flange_thickness + washer.thickness - nut.washer_pocket_depth + nut.plate_thickness + nut.lift_play{q}}}",
            "x1_edits_at_p6 item 1 (holder z_max to the tube top 153.84)")
    t = rep(name, t, f"z_rule: {{z_min: {q}collar_top - collar.top_above_plate{q}, z_max: collar_top}}",
            f"z_rule: {{z_min: {q}collar_top - collar.thickness{q}, z_max: collar_top}}", "x1_edits_at_p6 item 2 (collar z_min to the ring underside 153.84)")
    if name == "s1":
        t = rep(name, t, 'feature: holder, edge: z_max, offset: "nut.plate_thickness + washer.thickness - nut.washer_pocket_depth + collar.top_above_plate", source: "Loftsman 1.1 (e) LF1.1-1; check_stack.collar_top_z_A (test_P18)"}',
                'feature: holder, edge: z_max, offset: "collar.thickness", source: "Loftsman 1.1 (e) LF1.1-1; check_stack.collar_top_z_A (test_P18); 1.4 S4-b (s4_spec x1_edits_at_p6 item 3): the holder z_max is the tube top, collar.thickness below the collar top"}',
                "x1_edits_at_p6 item 3 (tie offset)")
    hk = "keys: [seat.holder_bottom_R, holder.stroke_gap_R, witness.zone_high, holder.length, holder.flange_od, holder.flange_thickness, cone.alpha, nut.plate_thickness, washer.thickness, nut.washer_pocket_depth, collar.top_above_plate]"
    t = rep(name, t, hk, hk[:-1] + ", receiver.register_bore_radius, register.g_reg, chain.t_h, chain.H, nut.lift_play]", "holder keys read by section_true")
    ck = "keys: [collar.od, collar.id, collar.top_above_plate, stop.collar_top_z]"
    t = rep(name, t, ck, ck[:-1] + ", collar.thickness]", "collar keys")
    rk = "keys: [base.plate_thickness, icd.floor_above_datum_a, receiver.rim_above_floor, receiver.spigot_od, receiver.floor_hole_dia, receiver.register_bore_radius, receiver.shoulder_od, receiver.shoulder_thickness, receiver.shoulder_z]"
    t = rep(name, t, rk, "keys: " + flow([k for k in rows4["receiver"]["keys"] if k != "thread.hand"]), "receiver keys (S4 list less the root-label key)")
    clk = "keys: [icd.floor_above_datum_a, collet.slit_length, collet.slit_ligament, collet.relief_hole_dia, receiver.register_bore_radius, cone.alpha]"
    t = rep(name, t, clk, "keys: " + flow([k for k in rows4["collet"]["keys"] if k not in ("collet.slit_count", "receiver.key_offset_deg")]), "collet keys (S4 list less the slit tick keys)")
    csk = "keys: [icd.floor_above_datum_a, collet.core_seat_height, collet.core_seat_width, core.diameter_nominal, collet.core_stop_z]"
    t = rep(name, t, csk, csk[:-1] + ", collet.grip_window_hi]", "core_seat keys")
    wk = "keys: [stop.collar_top_z, collar.top_above_plate, nut.overall_height, wingnut.sweep_clear_radius, wingnut.span]"
    drop = WING_KEYS + WINDOW_KEYS if name == "s1" else ()
    t = rep(name, t, wk, "keys: " + flow([k for k in rows4["wingnut"]["keys"] if k not in drop]),
            "wingnut keys (S4 list" + (" less the wing and window keys)" if name == "s1" else "; S3 r8 draws the -X wing and the theta 90 window, P2f)"))
    deps = {"receiver": ("-receiver.shoulder_od / 2", "receiver.shoulder_od / 2"), "collet": ("-receiver.register_bore_radius", "receiver.register_bore_radius"),
            "core_seat": ("-core.diameter_nominal / 2", "core.diameter_nominal / 2"), "holder": ("-holder.flange_od / 2", "holder.flange_od / 2"),
            "collar": ("-collar.od / 2", "collar.od / 2"), "wingnut": ("-wingnut.sweep_clear_radius", "wingnut.sweep_clear_radius")}
    for rid, (a, b) in deps.items():
        dep = f'depth: ["{a}", "{b}"]' if name == "s1" else f"depth: [{a}, {b}]"
        old = f"{ind}{dep}\n"
        i = t.index(f"id: {rid}\n")
        j = t.index(old, i)
        new = old + st_block(rid, ind) + "\n"
        if rid == "wingnut":   # Designer P3a FIX 5 (a)
            new += f"{ind}section_true_note: {flow(rows4['wingnut']['section_true_note'])}\n"
        edits[name].append({"why": f"{rid} section_true (as s4_spec.yaml; Sean STOP S4-A scope (i))" + ("; section_true_note (Designer P3a FIX 5 a)" if rid == "wingnut" else ""),
                            "old": old.rstrip("\n"), "new": new.rstrip("\n")})
        t = t[:j] + new + t[j + len(old):]
    if name == "s1":
        sq = lambda s: '"' + s + '"'  # noqa: E731
        o = lambda body: "- {" + body + "}"  # noqa: E731
        t = rep(name, t, o('id: holder, class: C, g_min: 0, source: "R6: holder tube in the register bore (S1 draws holder OD = register bore; build_parts/holder.py has g_reg 0.25), flange above the rim (TP1.1-3)"'),
                o('id: holder, class: G, g_min: 0.25, source: "S4-b, S4-c (Sean STOP S4-A, Design Notes 34): holder OD r 67.04 in the register bore r 67.29, register.g_reg 0.25; flange 8.59 above the rim"'), "receiver|holder C -> G 0.25")
        t = rep(name, t, o('id: wingnut, class: N, source: "R6: wing nut threaded on the receiver"'),
                o('id: wingnut, class: C, source: "S4-c (Design Notes 34): thread flank contact drawn on the receiver major cylinder r 74.79; fit.c_r 0.35 and fit.g_a 0.30 not drawn"'), "receiver|wingnut N -> C (wing nut in true section)")
        t = rep(name, t, o('id: wingnut, class: N, source: "R6: wing nut over the holder flange"'),
                o('id: wingnut, class: G, g_min: 0.50, source: "S4-c (Design Notes 34): pocket floor 0.50 above the flange top, radial 1.00 at the plate hole"'), "holder|wingnut N -> G 0.50")
        t = rep(name, t, o('id: holder, class: F, source: "TP1.1-3: section rows, N refused. S1 draws the holder to its flange top (145.09 z_A) and the collar from the plate top (153.09): the nut plate lies between, 8.00. build_parts/holder.py runs the tube up to the collar underside; the Designer rules the tube above the flange at M1"'),
                o('id: holder, class: C, kind: one_body, source: "S4-b (Design Notes 34): collar ring fused on the holder tube top 153.84 (build_parts/holder.py)"'), "collar|holder F -> C one_body")
        t = rep(name, t, o('id: wingnut, class: N, source: "wing nut under the collar ring, over the holder flange"'),
                o('id: wingnut, class: G, g_min: 0.75, source: "S4-c (Design Notes 34): nut.lift_play 0.75, nut-plate top to the collar underside"'), "collar|wingnut N -> G 0.75")
        t = rep(name, t, '  - "Holder section is a stand-in; S4 governs (build_parts/holder.py: OD 67.04, inner cone 62.04 to 56.75 over chain.H 30, bore 56.75, tube through the nut plate to the collar). Designer M1 r2 section 7; no S1 check value moves."',
                '  - "Holder, collar, collet, core seat, receiver and wing nut carry their true sections (section_true, as s4_spec.yaml; S4-b, Sean STOP S4-A, Design Notes 34); the r8 stand-in note is retired at S1 r9. No S1 check value moves (S1-4, S1-5b, drill_head|collar 25.000 unchanged)."',
                "holder stand-in note retired (Design Notes 25 S4-b)")
        old_c = "  - \"Class C means 'located on that face'. Fit values (holder g_reg 0.25, spigot hole 0.10 per side, collar lift play) belong to S4 (base stack) and Step 4 tolerancing; no C pair states a clearance. Designer M1 r2 section 7 (Loftsman R2-1).\""
        new_c = "  - \"Class C means 'located on that face'. Base-stack fits are set in s4_spec.yaml (S4-c, Design Notes 34: receiver|holder G 0.25, receiver_spigot|base_plate G 0.10, wingnut|holder G 0.50, collar|wingnut G 0.75); other fits belong to Step 4 tolerancing. Designer M1 r2 section 7 (Loftsman R2-1).\""
        t = rep(name, t, old_c, new_c, "C-meaning note (S4-c landed)")
    else:
        o = lambda body: "- {" + body + "}"  # noqa: E731
        t = rep(name, t, o("id: holder, class: C, g_min: 0, source: 'R6: holder tube in the register bore (S1 draws holder OD = register bore; build_parts/holder.py has g_reg 0.25), flange above the rim (TP1.1-3)'"),
                o("id: holder, class: G, g_min: 0.25, source: 'S4-b, S4-c (Sean STOP S4-A, Design Notes 34): holder OD r 67.04 in the register bore r 67.29, register.g_reg 0.25; flange 8.59 above the rim'"), "receiver|holder C -> G 0.25")
        t = rep(name, t, o("id: wingnut, class: N, source: 'R6: wing nut threaded on the receiver'"),
                o("id: wingnut, class: C, source: 'S4-c (Design Notes 34): thread flank contact drawn on the receiver major cylinder r 74.79; fit.c_r 0.35 and fit.g_a 0.30 not drawn'"), "receiver|wingnut N -> C")
        t = rep(name, t, o("id: wingnut, class: N, source: 'R6: wing nut over the holder flange'"),
                o("id: wingnut, class: G, g_min: 0.50, source: 'S4-c (Design Notes 34): pocket floor 0.50 above the flange top, radial 1.00 at the plate hole'"), "holder|wingnut N -> G 0.50")
        t = rep(name, t, o("id: holder, class: F, source: 'TP1.1-3: section rows, N refused. S1 draws the holder to its flange top (145.09 z_A) and the collar from the plate top (153.09): the nut plate lies between, 8.00. build_parts/holder.py runs the tube up to the collar underside; the Designer rules the tube above the flange at M1'"),
                o("id: holder, class: C, kind: one_body, source: 'S4-b (Design Notes 34): collar ring fused on the holder tube top 153.84 (build_parts/holder.py)'"), "collar|holder F -> C one_body")
        t = rep(name, t, o("id: wingnut, class: N, source: 'wing nut under the collar ring, over the holder flange'"),
                o("id: wingnut, class: G, g_min: 0.75, source: 'S4-c (Design Notes 34): nut.lift_play 0.75, nut-plate top to the collar underside'"), "collar|wingnut N -> G 0.75")
        i = t.index("- id: wingnut\n")
        j = t.index("  section_class: unsectioned\n", i)
        t = t[:j] + "  section_class: cut\n  hatch: brass\n" + t[j + len("  section_class: unsectioned\n"):]
        edits[name].append({"why": "wingnut section_class unsectioned -> cut, hatch brass (true section)", "old": "  section_class: unsectioned  (row wingnut)", "new": "  section_class: cut\n  hatch: brass"})

    # ------------------------------------------------------------ P2f follow-ons
    w4 = rows4["wingnut"]
    if name == "s3":
        # Designer P3a FIX 5 (b): S3 wing-nut shape string to the drawn pieces; -X wing hidden (FIX 4); sweep; +X wing not_drawn
        t = rep(name, t, "  shape: 'wing nut: body wingnut.body_od x nut.overall_height, two wings to span 230, sweep radius 115 as dashed extent lines'\n",
                "  shape: 'wing nut in true section, cut, brass (as s4_spec.yaml; build_parts/nut.py): thread body drawn at the receiver major r 74.79 to r 83.14 from 97.09; relief bore r 75.34 over 139.09 to 145.59; pocket rim r 71.90 to 83.14 over 145.59 to 146.39 on the -u side only (theta 90 washer window at +u, plane_cuts); nut plate r 68.04 to 83.14 over 146.39 to 153.09; dust skirt rim 2.0 then a slope; PTFE washer in the pocket (row washer); -X wing hidden over its whole extent, dashed, labelled (sub-artist wing); sweep r 115 as dashed extent lines (sub-artist sweep); +X wing in front of the plane (not_drawn) (Designer P3a FIX 5 b)'\n",
                "wingnut shape string to the drawn pieces (Designer P3a FIX 5 b)")
        blk = (f"  plane_cuts: {flow(w4['plane_cuts'])}\n  sub_artists: [wing, sweep]\n  wing: {flow(w4['wing'])}\n  sweep: {flow(w4['sweep'])}\n")
        t = ins_in_row(name, t, "wingnut", head, "  section_true_note:", blk,
                       "wingnut plane_cuts (Loftsman P3b FIX 2, same plane as S4), sub-artists wing and sweep (Designer P3a FIX 4, 5 b)")
        nd_old = '  - {part: "receiver spigot below the plate top", omit: deferred, owner: "S4-a",'
        i = t.index(nd_old)
        e = t.index("\n", i) + 1
        nd_new = '  - {part: "+X wing of the wing nut", omit: off_plane, reason: "in front of the plane (x > 0), cut away; the -X wing is drawn beyond, hidden (Designer P3a O3, FIX 5 b; as s4_spec.yaml)"}\n'
        edits[name].append({"why": "+X wing not_drawn (Designer P3a FIX 5 b)", "old": t[i:e].rstrip("\n")[:120] + " ...", "new": t[i:e].rstrip("\n")[:120] + " ...\n" + nd_new.rstrip("\n")})
        t = t[:e] + nd_new + t[e:]
        t = rep(name, t, "receiver spigot below the plate top (S4-a). Hatch:", "receiver spigot below the plate top (S4-a); +X wing of the wing nut (cut away). Hatch:",
                "figure_note names the +X wing (Designer P3a FIX 5 b)")
        t = rep(name, t, '  - {part: "receiver, collet, core seat, holder, wing nut, collar, capture core", row: "receiver, collet, core_seat, holder, wingnut, collar, core_750"}',
                '  - {part: "receiver, collet, core seat, holder, wing nut (-X wing hidden, sweep lines), PTFE washer, collar, capture core", row: "receiver, collet, core_seat, holder, wingnut (sub-artists wing, sweep), washer, collar, core_750"}',
                "part list names the washer and the wing-nut sub-artists (Designer P3a FIX 5 b, c)")
    # Designer P3a FIX 5 (c): washer row (shared, equal to S4 for X1) and its declarations on holder and wingnut
    hold_n = '{id: washer, class: C, source: "S4-c: flange top bears on the PTFE washer at pose K (as s4_spec.yaml)", face: {z: "holder_bottom + holder.length + holder.flange_thickness", side: washer on the flange top}}'
    wn_n = '{id: washer, class: C, source: "S4-c: washer in the pocket, three press pads (contact class P, ASSEMBLY.md; as s4_spec.yaml)"}'
    li = "      " if name == "s1" else "  "
    t = ins_in_row(name, t, "holder", head, f"{ind}neighbours:", f"{li}- {hold_n}\n", "holder|washer C (Designer P3a FIX 5 c)")
    if name == "s3":
        t = rep(name, t, "  label: {text: wing nut sweep r, key: wingnut.sweep_clear_radius, fmt: .0f}\n  neighbours: []\n",
                f"  label: {{text: wing nut sweep r, key: wingnut.sweep_clear_radius, fmt: .0f}}\n  neighbours:\n  - {wn_n}\n", "wingnut|washer C (Designer P3a FIX 5 c)")
    else:
        t = ins_in_row(name, t, "wingnut", head, f"{ind}neighbours:", f"{li}- {wn_n}\n", "wingnut|washer C (Designer P3a FIX 5 c)")
    wr = rows4["washer"]
    flds = ["name", "shape", "kind", "axis", "projection", "keys", "z_rule", "section_true", "depth", "label", "neighbours", "sense", "chain", "moves"]
    if name == "s3":
        flds += ["axes", "section_class", "hatch"]
    lines = [f"{head}- id: washer"] + [f"{ind}{k}: {flow(wr[k])}" for k in flds]
    if name == "s1":
        lines.append(f"{ind}notes: [\"shared with s3 and s4 (X1); S1 draws the wing nut in true section from r9, so the washer it stands on is drawn (Designer P3a FIX 5 c)\"]")
    blk = "\n".join(lines) + "\n" + ("\n" if name == "s1" else "")
    i, j = row_span(t, "wingnut", head)
    edits[name].append({"why": "washer row added after wingnut (Designer P3a FIX 5 c)", "old": f"{head}- id: collar  (row after wingnut)", "new": blk.rstrip("\n") + f"\n{head}- id: collar"})
    t = t[:j] + blk + t[j:]
    (S / f"{name}_spec.yaml").write_text(t, encoding="utf-8", newline="")
t4 = (SRC4 / "s4_spec.yaml").read_text(encoding="utf-8")
for a, b in (("z_rule: {z_min: holder_bottom, z_max: holder_bottom + holder.length + holder.flange_thickness}",
              "z_rule: {z_min: holder_bottom, z_max: holder_bottom + holder.length + holder.flange_thickness + washer.thickness - nut.washer_pocket_depth + nut.plate_thickness + nut.lift_play}"),
             ("z_rule: {z_min: collar_top - collar.top_above_plate, z_max: collar_top}", "z_rule: {z_min: collar_top - collar.thickness, z_max: collar_top}"),
             ('feature: holder, edge: z_max, offset: "nut.plate_thickness + washer.thickness - nut.washer_pocket_depth + collar.top_above_plate"', 'feature: holder, edge: z_max, offset: "collar.thickness"')):
    assert t4.count(a) == 1, a
    t4 = t4.replace(a, b)
(S / "s4_spec.yaml").write_text(t4, encoding="utf-8", newline="")
(S / "s2_spec.yaml").write_text((D / "s2_spec.yaml").read_text(encoding="utf-8"), encoding="utf-8", newline="")
json.dump(edits, open(S / "stage_edits.json", "w"), indent=1)
print({k: len(v) for k, v in edits.items()})
