"""Step 4 assembly tests: A1, A1a to A1e, A2a to A2h, A3a to A3i, A4, A6, A6a to A6c, F5 (five existing parts), F6, P6b.
Relations are data: A1a iterates the Relations table (45 rows) and the Feature pairs table (6 rows) of ASSEMBLY.md for poses R, Kd1, Kmax
and every size in core.diameters. Pose-dependent predicates read results/probes/pose_<P>_<tag>.json written by tests/probes/probe_poses.py
from the Step 7 assembler output parts_cache/assembly/pose_<P>_<tag>.FCStd; the test never computes a placement from params (Rule M).
Measures the pose probe does not yet produce (frame, rest, cutter, upper assembly) fail as ABSENT FEATURE naming the key; MEASURES lists them.
The 0.5 m core is the asserted case; 0.75 m and 1 m appear as recorded values only."""
import re

import pytest

import cad_helpers as H
from build_parts import common

P = H.P
G = lambda k: common.get(P(), k)
FAM = H.family()
NOMINAL = G("core.diameter_nominal")
IDS = [H.tag(d) for d in FAM]
RELS, FEATS = H.parse_assembly()
PARTS = H.parts_of(RELS)
ASM_TEXT = (H.ROOT / "ASSEMBLY.md").read_text(encoding="utf-8")

# Measure keys the Step 7 and Step 12 versions of probe_poses.py must write under "measures" (one row per test ID).
MEASURES = {
    "A1b": ["head_clear_radius_min", "key_sector_deg_min", "key_arm_reach_mm"],
    "A1c": ["column_foot_path_printed_overlap_mm3"], "A1d": ["column_baseplate_contact_area_mm2", "column_baseplate_overlap_mm3"],
    "A1e": ["strap_handle_parked_overlap_mm3"], "A2a": ["keepout_radius_used", "keepout_common_mm3"],
    "A2b": ["cutter_gap_to_collar_top"], "A2c": ["stop_path_forbidden_members"], "A2d": ["core_cutter_contact_area_mm2"],
    "A2e": ["rest_arm_min_radius"], "A2f": ["cam_lug_minus_cutter_lowest_z", "cam_lug_swept_printed_overlap_mm3"],
    "A2g": ["rest_arm_swept_overlap_mm3"], "A2h": ["manual_raise_printed_members"],
    "A3b": ["fit_plate_key_stop_pin", "fit_spigot_hole", "fit_column_foot", "fit_carriage_guide"],
    "A3c": ["core_axis_offset"], "A3d": ["lead_in_clearance"], "A3e": ["holder_bottom_above_floor"], "A3f": ["clamped_tilt_deg"],
    "A3g": ["funnel_capture_radius"], "A3h": ["nut_skirt_bottom_above_floor"], "A3i": ["engaged_mm"],
    "A6a": ["receiver_underside_contact_mm2"], "P6b": ["frame_footprint_x", "frame_footprint_y"],
}


T7 = H.gate_thresholds()


def _row(a, b):
    return [r for r in RELS if (r["a"], r["b"]) == (a, b)][0]


@H.label("discriminator", 7)
def test_A1_contract_rows_revision_1():
    """Row 3 holder|nut K g_min = washer.thickness - nut.washer_pocket_depth; row 4 nut|washer class P; row 5 per-pose minima 0 / 25 / 25."""
    H.need(abs(_row("holder", "nut")["g_min"] - (G("washer.thickness") - G("nut.washer_pocket_depth"))) <= 0.011, "ASSEMBLY.md holder|nut g_min = washer.thickness - nut.washer_pocket_depth")
    H.need((_row("nut", "washer")["r"], _row("nut", "washer")["k"]) == ("P", "P"), "ASSEMBLY.md nut|washer class P")
    f = [x for x in FEATS if x["fa"] == "nut collar top"][0]
    kind, vals = H.parse_gap_text(f["gaps"])
    H.need(kind == "min" and vals == [0.0, G("stop.g_stop"), G("stop.g_stop")], f"ASSEMBLY.md per-pose minima 0 / 25 / 25 in the nut collar top row, got {f['gaps']}")
    assert (f["r"], f["kd1"], f["kmax"]) == ("G", "G", "G")


@H.label("invariant", 4)
def test_A1_control_class_P_and_per_pose_minima_predicates():
    ok = {"min_dist": 0.0, "overlap_mm3": 2.2, "contact_area_mm2": 100.0}
    assert H.check_class("P", ok, 0.0, 0.0, pad=(2.0, 2.45)) == []  # zero control
    assert H.check_class("P", dict(ok, overlap_mm3=2.6), 0.0, 0.0, pad=(2.0, 2.45)) != []
    assert H.check_class("P", dict(ok, overlap_mm3=1.5), 0.0, 0.0, pad=(2.0, 2.45)) != []
    assert H.check_class("P", dict(ok, min_dist=0.5), 0.0, 0.0, pad=(2.0, 2.45)) != []
    assert H.check_class("P", ok, 0.0, 0.0, pad=(None, None))[0].startswith("MISSING:")
    assert H.parse_gap_text("at least 0 / 25 / 25") == ("min", [0.0, 25.0, 25.0]) and H.parse_gap_text("at least 25 at the stop") == ("min", 25.0)
    assert H.gates.min_for_pose([0.0, 25.0, 25.0], 0) == 0.0 and H.gates.min_for_pose([0.0, 25.0, 25.0], 2) == 25.0
    assert H.check_feature_gap("G", 20.464, H.gates.min_for_pose([0.0, 25.0, 25.0], 1), "min") != []  # R value 20.464 fails the Kd1 minimum
    assert H.check_feature_gap("G", 20.464, H.gates.min_for_pose([0.0, 25.0, 25.0], 0), "min") == []


def _pd(pose, d):
    return H.probe(f"pose_{pose}_{H.tag(d)}", H.pose_inputs(pose, d))


def _run(rows, pd):
    """rows: (measure key, op, threshold, tol). Returns violations."""
    e = []
    for key, op, thr, tol in rows:
        v = H.measure(pd, key)
        if isinstance(v, list):
            if op == "empty" and v:
                e.append(f"{key}: {v}")
            continue
        e += [f"{key}: {m}" for m in H.check_measure(v, op, thr, tol)]
    return e


# ---------------------------------------------------------------- A1 parser (invariant) and controls
@H.label("invariant", 4)
def test_A1_parser_reads_45_pairs_and_the_class_counts():
    assert len(PARTS) == 10 and len(RELS) == 45 and len(FEATS) == 6
    assert H.pair_table_errors(RELS) == []
    cc = H.class_counts(RELS)
    assert cc["r"] == {"C": 7, "G": 12, "F": 25, "P": 1} and cc["k"] == {"C": 9, "G": 10, "F": 25, "P": 1}   # Step 7 Revision 1: nut|washer C -> P (press pads)
    assert H.pair_class(RELS, "nut", "cutter", "Kd1") == ("G", G("stop.g_stop"))  # g_min = stop.g_stop
    with pytest.raises(AssertionError):
        H.pair_class(RELS, "nut", "ghost", "R")  # every unlisted pair fails


@H.label("invariant", 4)
def test_A1_parser_control_a_deleted_row_fires():
    assert H.pair_table_errors(RELS) == []  # zero control
    for i in (0, 20, 44):
        cut = RELS[:i] + RELS[i + 1:]
        errs = H.pair_table_errors(cut)
        assert any("unlisted pair" in x for x in errs), i
    assert any("duplicate" in x for x in H.pair_table_errors(RELS + [RELS[0]]))
    assert any("illegal class" in x for x in H.pair_table_errors([dict(RELS[0], r="X")] + RELS[1:]))
    dropped = "\n".join(ln for ln in ASM_TEXT.splitlines() if not ln.startswith("| base | holder |"))
    assert len(H.parse_assembly(dropped)[0]) == 44 and H.pair_table_errors(H.parse_assembly(dropped)[0]) != []


@H.label("invariant", 4)
def test_A1a_predicate_controls_every_class():
    C_ok = {"min_dist": 0.005, "overlap_mm3": 0.0, "contact_area_mm2": 50.0}
    G_ok = {"min_dist": 2.0, "overlap_mm3": 0.0, "contact_area_mm2": 0.0}
    F_ok = {"min_dist": 40.0, "overlap_mm3": 0.0, "contact_area_mm2": 0.0}
    assert H.check_class("C", C_ok, 0.0) == [] and H.check_class("G", G_ok, 1.5) == [] and H.check_class("F", F_ok, 0.0) == []  # zero controls
    # nut resting on the collet top: overlap 0, distance 0, contact: G (g_min 1.0) fires
    assert H.check_class("G", {"min_dist": 0.0, "overlap_mm3": 0.0, "contact_area_mm2": 80.0}, 1.0) != []
    # holder resting on the receiver top: G (g_min 1.5) fires
    assert H.check_class("G", {"min_dist": 0.0, "overlap_mm3": 0.0, "contact_area_mm2": 400.0}, 1.5) != []
    # two parts 100 mm apart read F; the same pair fails class C
    far = {"min_dist": 100.0, "overlap_mm3": 0.0, "contact_area_mm2": 0.0}
    assert H.check_class("F", far, 0.0) == [] and H.check_class("C", far, 0.0) != []
    # a 1 mm overlap fires every class
    over = {"min_dist": -1.0, "overlap_mm3": 500.0, "contact_area_mm2": 100.0}
    assert all(H.check_class(c, over, 1.0) for c in ("C", "G", "F"))
    # feature gaps: exact and minimum
    assert H.check_feature_gap("G", 13.126, 13.126, "exact") == [] and H.check_feature_gap("G", 12.0, 13.126, "exact") != []
    assert H.check_feature_gap("G", 30.0, 25.0, "min") == [] and H.check_feature_gap("G", 20.0, 25.0, "min") != []
    assert H.parse_gap_text("11.626 / 7.089 / 0.00") == ("exact", [11.626, 7.089, 0.0])
    assert H.parse_gap_text("at least 1 pitch (8)") == ("min", 8.0) and H.parse_gap_text("at least 25 at the stop") == ("min", 25.0)


@H.label("invariant", 4)
def test_A2_control_a_ring_in_the_face_annulus_path_fires():
    face = (G("iris.face_radius_core"), G("drill.r_face"))  # cutting-face annulus: core kerf radius to R_face
    tube = (G("drill.tube_id") / 2.0, G("drill.tube_od") / 2.0)
    assert H.interval_overlap((G("icd.keepout_radius"), 120.0), face) == 0  # zero control: a ring outside the keep-out radius
    assert H.interval_overlap((80.0, 90.0), face) > 0  # known-bad: a ring placed in the face annulus path
    assert H.interval_overlap((74.0, 75.0), tube) > 0
    assert H.interval_overlap((100.0, 110.0), face) == 0 and H.interval_overlap((100.0, 110.0), tube) == 0


# ---------------------------------------------------------------- A1 contact area is the common-face intersection (Revision 1)
def collar_plate_area_max():
    """Geometric maximum of the collar underside on the nut plate top: annulus from the plate hole radius to the collar outer radius (3,694 mm2)."""
    import math
    return math.pi * ((G("collar.od") / 2.0) ** 2 - (G("nut.plate_hole_dia") / 2.0) ** 2)


@H.label("invariant", 4)
def test_A1_control_collar_contact_bound_is_3694_and_the_old_9978_read_fires():
    import math
    assert math.pi * (76.2 ** 2 - 68.04 ** 2) == pytest.approx(3694, abs=5)  # zero control: the Topologist figure (3,694 quoted; 3,697.6 computed)
    assert 9978.0 > math.pi * (76.2 ** 2 - 68.04 ** 2) + 0.5  # known-bad: the sum-of-smaller-face reading exceeds the bound


@H.label("discriminator", 7)
def test_A1_holder_nut_contact_area_at_R_is_within_the_geometric_maximum():
    m = _pd("R", NOMINAL)["pairs"].get("holder|nut")
    H.need(m is not None, "pair holder|nut in the pose probe")
    assert 0.0 < m["contact_area_mm2"] <= collar_plate_area_max() + 1.0, (m["contact_area_mm2"], collar_plate_area_max())


# ---------------------------------------------------------------- A1a matrix (discriminator, step 7)
@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", H.POSES)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_A1a_pair_matrix_by_pose_and_size(pose, d):
    pd = _pd(pose, d)
    errs = []
    for r in RELS:
        m = pd["pairs"].get(f"{r['a']}|{r['b']}")
        H.need(m is not None, f"pair {r['a']}|{r['b']} in the pose probe")
        cls, gmin = H.pair_class(RELS, r["a"], r["b"], pose)
        floor = G("seat.min_contact_area") if {r["a"], r["b"]} == {"holder", "collet"} else G("fit.min_contact_patch")
        errs += [f"{r['a']}|{r['b']} {x}" for x in H.check_class(cls, m, gmin, floor, pad=T7["pad"])]
    idx = {"R": 2, "Kd1": 3, "Kmax": 4}[pose]
    for f in FEATS:
        key = f"{f['fa']}|{f['fb']}"
        fp = pd["feature_pairs"].get(key)
        H.need(fp is not None and fp.get("gap") is not None, f"feature pair {key} in the pose probe")
        kind, vals = H.parse_gap_text(f["gaps"])
        cls = (f["r"], f["kd1"], f["kmax"])[idx - 2]
        want = H.gates.min_for_pose(vals, idx - 2) if kind == "min" else vals[idx - 2]
        errs += [f"{key} {x}" for x in H.check_feature_gap(cls, fp["gap"], want, kind)]
    assert errs == [], errs


# ---------------------------------------------------------------- A1b to A1e, A2a to A2h (discriminator, step 12)
@H.label("discriminator", 12)
def test_A1b_fastener_head_clear_radius_and_key_sector():  # tool access: 25 mm clear radius, 60 degree sector, 150 mm key
    pd = _pd("R", NOMINAL)
    assert _run([("head_clear_radius_min", "ge", G("access.head_clear_radius"), 0.0), ("key_sector_deg_min", "ge", G("access.key_sector_deg"), 0.0),
                 ("key_arm_reach_mm", "ge", G("access.key_arm_length"), 0.0)], pd) == []


@H.label("discriminator", 12)
def test_A1c_no_printed_solid_in_the_column_foot_path():
    assert _run([("column_foot_path_printed_overlap_mm3", "zero", 0, H.OVERLAP_TOL)], _pd("R", NOMINAL)) == []


@H.label("discriminator", 12)
def test_A1d_column_to_base_plate_is_class_G_or_F():
    assert _run([("column_baseplate_contact_area_mm2", "zero", 0, 0.0), ("column_baseplate_overlap_mm3", "zero", 0, H.OVERLAP_TOL)], _pd("R", NOMINAL)) == []


@H.label("discriminator", 12)
def test_A1e_strap_handle_clears_the_parked_upper_assembly():
    assert _run([("strap_handle_parked_overlap_mm3", "zero", 0, H.OVERLAP_TOL)], _pd("R", NOMINAL)) == []


@H.label("discriminator", 12)
def test_A2a_frame_rest_and_cable_solids_clear_the_keepout_cylinder():
    assert _run([("keepout_radius_used", "eq", G("icd.keepout_radius"), 1e-6), ("keepout_common_mm3", "zero", 0, H.OVERLAP_TOL)], _pd("R", NOMINAL)) == []


# SRC: 152.4 mm as the cutter OD | ASSUMED | gameplan.md 390 | key=drill.tube_od
@H.label("discriminator", 12)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_A2b_stop_gap_above_the_collar_top(d):  # g_stop is a mechanical clearance: cutter lowest point at the stop to the collar top, wings included
    assert _run([("cutter_gap_to_collar_top", "ge", G("stop.g_stop"), 0.01)], _pd("Kd1", d)) == []


@H.label("discriminator", 12)
def test_A2c_stop_and_torque_path_holds_no_printed_member():
    assert H.measure(_pd("R", NOMINAL), "stop_path_forbidden_members") == []  # no nut, holder, collet, receiver or base-plate member


@H.label("discriminator", 12)
def test_A2d_no_cutter_or_lead_in_face_bears_on_the_core_at_the_stop():
    assert _run([("core_cutter_contact_area_mm2", "zero", 0, 0.0)], _pd("Kd1", NOMINAL)) == []


@H.label("discriminator", 12)
def test_A2e_released_rest_arm_stays_outside_the_swing_radius():
    assert _run([("rest_arm_min_radius", "ge", G("rest.swing_clear_radius"), 0.0)], _pd("R", NOMINAL)) == []


@H.label("discriminator", 12)
def test_A2f_cam_lug_not_below_the_cutter_and_swept_volume_clear():
    assert _run([("cam_lug_minus_cutter_lowest_z", "ge", 0.0, 0.0), ("cam_lug_swept_printed_overlap_mm3", "zero", 0, H.OVERLAP_TOL)], _pd("R", NOMINAL)) == []


@H.label("discriminator", 12)
def test_A2g_released_arm_clear_of_the_cutter_and_lug_swept_volume():
    assert _run([("rest_arm_swept_overlap_mm3", "zero", 0, H.OVERLAP_TOL)], _pd("R", NOMINAL)) == []


@H.label("discriminator", 12)
def test_A2h_manual_raise_path_holds_no_printed_member():
    assert H.measure(_pd("R", NOMINAL), "manual_raise_printed_members") == []


# ---------------------------------------------------------------- A3a to A3i
# SRC: Friction mu_k about 0.35 | ASSUMED | gameplan.md 412 | key=friction.mu_k
@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_A3a_cone_half_angle_against_atan_mu_max_or_the_capture_pair_exists(d):
    import math
    c = H.probe(f"collet_{H.tag(d)}", H.collet_inputs(d))
    alpha = G("cone.alpha")
    assert abs(c["cone_half_angle_deg"] - alpha) <= 0.02  # collet cone against the holder cone (holder_result.json reads 10.0)
    hol = [f for f in H.result_json("holder")["features"] if "cone.alpha" in f["feature"]][0]
    assert abs(hol["built"] - c["cone_half_angle_deg"]) <= 0.02
    mu_max = max(G(k) for k in ("friction.mu_k", "friction.mu_c", "friction.mu_t", "friction.bearing"))
    captured = any({r["a"], r["b"]} == {"holder", "nut"} and r["r"] == "C" for r in RELS)
    assert alpha > math.degrees(math.atan(mu_max)) or captured, (alpha, mu_max)


# Orchestrator ruling 1 (Step 7): key/pin (chain[0] 0.32, built 0.250) and spigot (chain[1] 0.20, built 0.200; two coaxial cylinder faces in base) are
# measured at 7; column foot and carriage guide (chain[2:]) belong to the Step 12 assembly and carry green_at_12.
A3B_AT_7 = ["fit_plate_key_stop_pin", "fit_spigot_hole"]


@H.label("discriminator", 7)
def test_A3b_built_fits_within_the_coaxiality_chain_key_pin_and_spigot():
    pd = _pd("R", NOMINAL)
    chain = G("icd.coaxiality_chain")
    got = [H.measure(pd, k) for k in A3B_AT_7]
    assert all(g <= c + 0.02 for g, c in zip(got, chain)), (got, chain)
    assert sum(got) <= G("icd.coaxiality_budget")


@H.label("discriminator", 12)
def test_A3b_built_fits_within_the_coaxiality_chain_column_foot_and_carriage_guide():
    pd = _pd("R", NOMINAL)
    chain = G("icd.coaxiality_chain")
    got = [H.measure(pd, k) for k in MEASURES["A3b"][2:]]
    assert all(g <= c + 0.02 for g, c in zip(got, chain[2:])), (got, chain)
    assert sum(got) <= G("icd.coaxiality_budget")


@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", ["Kd1", "Kmax"])
def test_A3c_core_axis_offset_at_the_collet(pose):
    pd = _pd(pose, NOMINAL)
    assert H.measure(pd, "core_axis_offset") <= H.need_key("icd.core_axis_offset_max")


@H.label("discriminator", 7)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_A3d_lead_in_clearance_over_core_radius(d):
    assert H.measure(_pd("R", d), "lead_in_clearance") >= H.need_key("icd.core_lead_in_clearance_min")


@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", H.POSES)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_A3e_holder_bottom_above_the_receiver_floor(pose, d):
    want = {"R": G("seat.holder_bottom_R"), "Kd1": G("seat.holder_bottom_R") - (G("holder.stroke_gap_R") - G("witness.zone_high")),
            "Kmax": G("holder.bottom_above_floor_Kmax")}[pose]
    v = H.measure(_pd(pose, d), "holder_bottom_above_floor")
    assert v > 0 and abs(v - want) <= 0.05, (v, want)


@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", ["Kd1", "Kmax"])
def test_A3f_clamped_tilt(pose):
    assert H.measure(_pd(pose, NOMINAL), "clamped_tilt_deg") <= H.need_key("register.clamped_tilt_max_deg")


@H.label("discriminator", 7)
def test_A3g_funnel_capture_radius():
    assert H.measure(_pd("R", NOMINAL), "funnel_capture_radius") >= H.need_key("icd.core_lead_in_capture_min")


@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", H.POSES)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_A3h_nut_skirt_at_least_one_pitch_above_the_floor(pose, d):
    assert H.measure(_pd(pose, d), "nut_skirt_bottom_above_floor") >= G("thread.pitch")


@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", H.POSES)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_A3i_engaged_thread_length_in_every_pose(pose, d):
    assert H.measure(_pd(pose, d), "engaged_mm") >= G("thread.min_engage_pitches") * G("thread.pitch")


# ---------------------------------------------------------------- A4 product tree
@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", H.POSES)
def test_A4_product_tree(pose):
    pd = _pd(pose, NOMINAL)
    assert sorted(pd["tree"]) == sorted(PARTS)
    assert pd["visible_count"] == len(PARTS)  # expected count computed from the part list, not read from the saved file


# ---------------------------------------------------------------- A6 planted states
WS = {1: "collet upside down", 2: "holder upside down", 3: "nut upside down", 4: "wrong-hand thread", 5: "cross-threaded tilt",
      6: "wrong collet for core", 7: "collet unseated", 10: "base on frame upside down", 11: "slit over key"}
FIRES = {"A1", "A3", "T1", "T9", "F1", "F3"}


def _ws(n):
    d = H.probe(f"ws{n}", [H.CACHE / "assembly" / f"ws{n}.FCStd"])
    return set(d["fired"])


@H.label("discriminator", 7)
@pytest.mark.parametrize("n", sorted(WS), ids=[f"WS{n}" for n in sorted(WS)])
def test_A6_planted_wrong_state_fires_a_gate(n):
    fired = _ws(n)
    assert fired and fired <= FIRES, (n, WS[n], fired)


@H.label("discriminator", 7)
def test_A6a_receiver_underside_carries_no_force_on_the_base_plate():
    assert _run([("receiver_underside_contact_mm2", "zero", 0, 0.0)], _pd("Kmax", NOMINAL)) == []


@H.label("discriminator", 7)
def test_A6b_holder_bottomed_state_ws8_fires():
    assert _ws(8) and _ws(8) <= FIRES


@H.label("discriminator", 7)
def test_A6c_nut_bottomed_on_base_state_ws9_fires():
    assert _ws(9) and _ws(9) <= FIRES


# ---------------------------------------------------------------- F6, P6b
@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", H.POSES)
def test_F6_holder_stroke_gap_and_ring_top_gap(pose):
    pd = _pd(pose, NOMINAL)
    flange = {"R": G("holder.stroke_gap_R"), "Kd1": G("witness.zone_high"), "Kmax": G("holder.stroke_gap_min_K")}[pose]
    hb = {"R": G("seat.holder_bottom_R"), "Kd1": G("seat.holder_bottom_R") - (G("holder.stroke_gap_R") - G("witness.zone_high")),
          "Kmax": G("holder.bottom_above_floor_Kmax")}[pose]
    ring = hb - G("holder.bottom_above_floor_Kmax")  # 11.626 / 7.09 / 0 (the built ring top sits fit.model_contact_gap below)
    fp = pd["feature_pairs"]
    H.need("holder flange underside|receiver rim" in fp and "holder bottom|collet foot ring top" in fp, "holder stroke gap features in the pose probe")
    assert abs(fp["holder flange underside|receiver rim"]["gap"] - flange) <= 0.05
    # F6 conflict 4: the spec ring gap 0.00 at K-max is the class C contact; the built solid carries the OCC contact offset
    # fit.model_contact_gap (0.005) on every class C pair, so the expected gap is ring + that key and the tolerance is 0.001 there
    mcg = G("fit.model_contact_gap")
    assert abs(fp["holder bottom|collet foot ring top"]["gap"] - (ring + mcg)) <= (0.001 if pose == "Kmax" else 0.05)
    assert pd["pairs"]["base|holder"]["contact_area_mm2"] == 0  # the stroke gap is never loaded (S6)


# SRC: 30-6060: 60 x 60 mm | DECLARED | gameplan.md 409
@H.label("discriminator", 7)
def test_P6b_frame_solids_644_by_608():
    pd = _pd("R", NOMINAL)
    assert abs(H.measure(pd, "frame_footprint_x") - G("icd.footprint_x")) <= 0.05
    assert abs(H.measure(pd, "frame_footprint_y") - G("icd.footprint_y")) <= 0.05


# ---------------------------------------------------------------- F5 for the five existing parts (invariant)
def _step3():
    return H.probe("step3_parts", H.part_inputs(*H.FIVE_PARTS))


@H.label("invariant", 4)
@pytest.mark.parametrize("part", H.FIVE_PARTS)
def test_F5_five_parts_shell_features_and_flipped_copy(part):
    pr, rj = _step3()[part], H.result_json(part)
    assert pr["valid"] and pr["closed"] and pr["solids"] == 1 and pr["shells"] == 1
    assert pr["euler_VEF"] == rj["euler_VEF"] and abs(pr["volume"] - rj["volume_mm3"]) <= 0.01 * rj["volume_mm3"]
    # genus: cell count over the built B-rep (probe_step3_parts.cell_genus) equals the declared through-hole count (F5 conflict 1; the
    # result JSONs record genus null because cadlib cannot count it, so the probe computes it from the solid)
    assert pr["cell_genus"] == H.declared_genus(part), (pr["cell_genus"], H.declared_genus(part))
    assert rj["features"] and all(f["pass"] for f in rj["features"]) and rj["all_features_pass"]
    assert H.check_flip(pr["flip_mismatch_fraction"], H.FLIP_FLOOR) == []  # Rule P: the flipped copy differs


@H.label("invariant", 4)
def test_F5_control_flipped_copy_checker():
    assert H.check_flip(0.0085, H.FLIP_FLOOR) == []  # zero control: the washer, the thinnest signed part, reads 0.0085
    assert H.check_flip(0.0, H.FLIP_FLOOR) != []  # known-bad: a plain disc flips onto itself
    assert H.check_flip(H.FLIP_FLOOR, H.FLIP_FLOOR) != []


@H.label("invariant", 4)
def test_F5_control_genus_counter_distinguishes_one_hole_from_two():
    assert H.declared_genus("nut") == 1 + G("nut.washer_window_count") and H.declared_genus("washer") == 1
    assert H.declared_genus("nut") != H.declared_genus("holder")  # known-bad: a nut read as a plain ring would miss the window tunnels
