"""Step 7 wave-0 additions (Software Engineer): G1 measure controls, G2 planted-state gate table, G3 zero control, G4 per-instance pair overlaps,
G5 pose ledger, G6 interference-report parse, G7 clamped-solid and parametrization checks. Artifact tests are discriminators green_at_7 and fail
as MISSING: / ABSENT FEATURE: until the Step 7 assembler and probes run. Controls on synthetic data are invariants (label() allows an invariant at 4 only).
Readers never compute a placement from params (Rule M): every number comes from results/probes/*.json, results/assembly_poses.json or the report."""
import json

import pytest

import cad_helpers as H
import test_assembly as TA
from build_parts import common

gates = H.gates
G = lambda k: common.get(H.P(), k)
FAM = H.family()
IDS = [H.tag(d) for d in FAM]
NOMINAL = G("core.diameter_nominal")
T = H.gate_thresholds()
LEAD = G("thread.pitch")


def _pd(pose, d=NOMINAL):
    return H.probe(f"pose_{pose}_{H.tag(d)}", H.pose_inputs(pose, d))


def synth_pose(pose, T=T):
    """A probe dict a correct assembly would produce: every pair at its class, feature gaps at the table values, measures at their targets."""
    pairs = {}
    for r in T["rels"]:
        cls = r["r"] if pose == "R" else r["k"]
        floor = gates.pair_floor(r, T)
        pad = T.get("pad") or (2.0, 2.45)
        pairs[f"{r['a']}|{r['b']}"] = ({"min_dist": 0.0, "overlap_mm3": (pad[0] + pad[1]) / 2.0, "contact_area_mm2": floor + 1.0} if cls == "P" else
                                       {"min_dist": 0.0, "overlap_mm3": 0.0, "contact_area_mm2": floor + 1.0} if cls == "C" else
                                       {"min_dist": r["g_min"] + 1.0, "overlap_mm3": 0.0, "contact_area_mm2": 0.0} if cls == "G" else
                                       {"min_dist": 50.0, "overlap_mm3": 0.0, "contact_area_mm2": 0.0})
    if pose == "R":
        pairs["holder|collet"]["min_dist"] = T["seat_clearance"] + max(0.0, 0.3 - T["seat_clearance"]) + 0.0
    idx = gates.POSE_IDX[pose]
    fps = {}
    for f in T["feats"]:
        kind, vals = gates.parse_gap_text(f["gaps"])
        fps[f"{f['fa']}|{f['fb']}"] = {"gap": vals if kind == "min" else vals[idx]}
        if kind == "min":
            fps[f"{f['fa']}|{f['fb']}"]["gap"] = gates.min_for_pose(vals, idx) + 1.0
    ms = {"holder_bottom_above_floor": T["holder_bottom"][pose], "nut_skirt_bottom_above_floor": T["pitch"] + 5.0, "engaged_mm": T["min_engage_mm"] + 5.0,
          "core_axis_offset": 0.1, "clamped_tilt_deg": 0.1, "receiver_underside_contact_mm2": 0.0, "frame_footprint_x": T["footprint_x"],
          "frame_footprint_y": T["footprint_y"], "nut_tilt_deg": 0.0, "holder_tilt_deg": 0.0}
    return {"pairs": pairs, "feature_pairs": fps, "measures": ms}


# ---------------------------------------------------------------- G1: measure controls
# (key, pose, op, threshold getter). The probe stores controls[key] = {good, bad}; the threshold passes good and fires on bad.
MEAS = [("core_axis_offset", "Kd1", "le", lambda: H.need_key("icd.core_axis_offset_max")),
        ("clamped_tilt_deg", "Kmax", "le", lambda: H.need_key("register.clamped_tilt_max_deg")),
        ("lead_in_clearance", "R", "ge", lambda: H.need_key("icd.core_lead_in_clearance_min")),
        ("funnel_capture_radius", "R", "ge", lambda: H.need_key("icd.core_lead_in_capture_min")),
        ("receiver_underside_contact_mm2", "Kmax", "zero", lambda: 0.0),
        ("frame_footprint_y", "R", "eq", lambda: G("icd.footprint_y")),
        ("slit_width_clamped_min", "Kmax", "ge", lambda: G("collet.min_slit_clamped") + 1e-6),
        ("nut_stop_travel_mm", "Kmax", "ge", lambda: G("thread.pitch")),  # bad control (nut without relief) reads about 4.0 and fails
        ("nut_tilt_deg", "Kd1", "le", lambda: G("register.tilt_limit_deg")),
        ("holder_tilt_deg", "Kd1", "le", lambda: G("register.tilt_limit_deg"))]


@H.label("discriminator", 7)
@pytest.mark.parametrize("key,pose,op,thr", MEAS, ids=[m[0] for m in MEAS])
def test_G1_measure_passes_its_good_value_and_fires_on_its_known_bad_control(key, pose, op, thr):
    pd = _pd(pose)
    H.measure(pd, key)
    ctl = pd.get("controls", {}).get(key)
    H.need(ctl is not None, f"probe control for {key}")
    tol = 0.05 if op == "eq" else 0.0
    assert H.check_measure(ctl["good"], op, thr(), tol) == [], (key, ctl)
    assert H.check_measure(ctl["bad"], op, thr(), tol) != [], (key, ctl)


@H.label("discriminator", 7)
def test_G1_nut_stop_travel_with_relief_is_10_01_and_without_relief_about_4():
    """Loftsman Revision 1 V3: the relief bore moves the stop from nut z0 46.0 to 40.0 (travel 10.01 at Kmax); the unrelieved nut reads about 4.0."""
    pd = _pd("Kmax")
    good = H.measure(pd, "nut_stop_travel_mm")
    bad = pd["controls"]["nut_stop_travel_mm"]["bad"]
    assert good == pytest.approx(10.01, abs=0.05), good
    assert bad == pytest.approx(4.0, abs=0.5) and bad < G("thread.pitch"), bad


@H.label("discriminator", 7)
def test_G1_lead_in_bore_is_the_working_bore_not_the_cutting_face():
    """A3d reads a bore radius; a cutter without the lead-in would read the face annulus (71.4375) and pass vacuously."""
    assert H.measure(_pd("R"), "lead_in_bore_radius") == pytest.approx(G("icd.core_lead_in_bore"), abs=0.01)


# ---------------------------------------------------------------- G2, G3: planted states and the zero control
@H.label("invariant", 4)
def test_G2_gate_predicates_fire_on_known_bad_variants_and_not_on_the_correct_pose():
    for pose in H.POSES:
        assert gates.fired(synth_pose(pose), pose, dict(T, strict=True)) == {}, pose  # zero control
    base = synth_pose("Kd1")
    bad = {"A1": lambda d: d["pairs"]["base|holder"].update(min_dist=0.0, contact_area_mm2=100.0),
           "A3": lambda d: d["measures"].update(holder_bottom_above_floor=T["holder_bottom"]["Kd1"] + 1.0),
           "T1": lambda d: d["pairs"]["base|nut"].update(overlap_mm3=500.0),
           "T9": lambda d: d["measures"].update(nut_tilt_deg=T["tilt_limit"] + 1.0),
           "F1": lambda d: d["pairs"]["holder|collet"].update(contact_area_mm2=0.0),
           "F3": lambda d: d["pairs"]["collet|core"].update(overlap_mm3=100.0)}
    assert sorted(bad) == sorted(gates.GATES)
    for gate, mutate in bad.items():
        d = json.loads(json.dumps(base))
        mutate(d)
        assert gate in gates.fired(d, "Kd1", T), gate


@H.label("invariant", 4)
def test_G2_ws_table_names_eleven_states_each_with_two_expected_gates():
    assert sorted(gates.WS_EXPECT) == list(range(1, 12)) and sorted(gates.WS_NAMES) == list(range(1, 12))
    assert all(v and v <= set(gates.GATES) for v in gates.WS_EXPECT.values())
    assert {n: gates.WS_NAMES[n] for n in TA.WS} == TA.WS  # the A6 test table and the probe table agree


@H.label("discriminator", 7)
@pytest.mark.parametrize("n", range(1, 12), ids=[f"WS{n}" for n in range(1, 12)])
def test_G2_planted_state_fires_its_expected_gate_and_only_the_six(n):
    d = H.probe(f"ws{n}", [H.CACHE / "assembly" / f"ws{n}.FCStd"])
    fired = set(d["fired"])
    assert fired <= set(gates.GATES) and fired & gates.WS_EXPECT[n], (n, gates.WS_NAMES[n], sorted(fired), sorted(gates.WS_EXPECT[n]))
    assert set(d["expected"]) == gates.WS_EXPECT[n]


@H.label("discriminator", 7)
def test_G3_unplanted_poses_fire_none_of_the_six_gates():
    d = H.probe("ws0", [H.CACHE / "assembly" / f"pose_{p}_{H.nominal_tag()}.FCStd" for p in H.POSES])
    assert d["poses"] == sorted(H.POSES) and d["fired"] == [] and all(v == [] for v in d["fired_by_pose"].values()), d.get("reasons")


# ---------------------------------------------------------------- G4: per-instance pair overlaps
INSTANCE_KINDS = ["bracket|bracket", "tnut|tnut", "bracket|member", "member|tnut", "bracket|tnut", "member|member"]


def _counts():
    """C6 option (a): 8 purchased (2 per outer-corner joint) + 4 printed (1 per support-end joint) = 12 brackets, 96 T-nuts."""
    nb = G("hardware.purchased_bracket_joints") * G("hardware.brackets_per_joint") + G("hardware.printed_bracket_joints") * H.need_key("hardware.printed_brackets_per_joint")
    return nb, nb * G("hardware.tnuts_per_bracket")


def _inst():
    N_BRACKETS, N_TNUTS = _counts()
    d = H.probe("frame_instances", [H.CACHE / "assembly" / f"pose_R_{H.nominal_tag()}.FCStd", H.LEDGER])
    H.need(d["counts"] == {"member": 6, "bracket": N_BRACKETS, "tnut": N_TNUTS}, f"instance counts 6 / 12 / 96, got {d['counts']}")
    return d


@H.label("discriminator", 7)
@pytest.mark.parametrize("kind", INSTANCE_KINDS)
def test_G4_instance_pairs_of_each_kind_have_no_common_volume(kind):
    d = _inst()
    pairs = {k: v for k, v in d["pairs"].items() if gates.pair_kind(*k.split("|")) == kind}
    assert gates.instance_errors(pairs, ruled=H.ruled_instance_pairs()) == [], kind


@H.label("discriminator", 7)
def test_G4_every_bracket_touches_its_eight_tnuts():
    N_BRACKETS, N_TNUTS = _counts()
    d = _inst()
    per = d["per_bracket_tnuts"]
    assert len(per) == N_BRACKETS == 12 and all(len(set(v)) == G("hardware.tnuts_per_bracket") for v in per.values()), {k: len(v) for k, v in per.items()}
    assert len({t for v in per.values() for t in v}) == N_TNUTS == 96  # each T-nut serves one bracket


@H.label("invariant", 4)
def test_G4_control_a_planted_overlapping_bracket_pair_fires():
    ok = {"bracket_purchased_1|bracket_printed_1": {"overlap_mm3": 0.0, "min_dist": 0.0}, "tnut_1|tnut_2": {"overlap_mm3": 0.004, "min_dist": 0.0}}
    assert gates.instance_errors(ok) == []  # zero control
    bad = dict(ok, **{"bracket_purchased_1|bracket_printed_2": {"overlap_mm3": 18248.6, "min_dist": 0.0}})
    assert len(gates.instance_errors(bad)) == 1
    assert gates.instance_errors(bad, ruled={"bracket|bracket": 20000.0}) == []  # a ruled row covers it only up to its stated volume
    assert gates.instance_errors(bad, ruled={"bracket|bracket": 100.0}) != []
    assert gates.pair_kind("member_end_1", "bracket_printed_3") == "bracket|member" and gates.pair_kind("tnut_5", "tnut_6") == "tnut|tnut"


# ---------------------------------------------------------------- G5: pose ledger
def _ledger():
    return json.loads(H.require(H.LEDGER).read_text(encoding="utf-8"))


@H.label("discriminator", 7)
def test_G5_poses_come_from_one_base_pose_by_the_screw_motion():
    led = _ledger()
    H.need(led.get("lead_mm") is not None and "sizes" in led and "base_pose" in led, "assembly_poses.json keys lead_mm, base_pose, sizes")
    assert led["lead_mm"] == pytest.approx(G("thread.pitch"), abs=1e-9)
    assert sorted(led["sizes"]) == sorted(IDS), sorted(led["sizes"])
    assert gates.ledger_errors(led, led["lead_mm"]) == []
    for tag, poses in led["sizes"].items():  # R is the base pose for every size: the fixed parts agree across sizes
        for part in gates.FIXED:
            assert gates.mat_diff(poses["R"]["placements"][part], led["base_pose"][part]) <= 1e-9, (tag, part)


@H.label("invariant", 4)
def test_G5_control_pure_z_nut_and_displaced_fixed_part_fire():
    assert gates.ledger_errors(gates.synth_ledger(LEAD), LEAD) == []  # zero control
    assert any("nut(P)" in e for e in gates.ledger_errors(gates.synth_ledger(LEAD, pure_z=True), LEAD))
    assert any("frame moved" in e for e in gates.ledger_errors(gates.synth_ledger(LEAD, move_part="frame"), LEAD))
    assert any("clockwise" in e for e in gates.ledger_errors(gates.synth_ledger(LEAD, dz_kd1=4.0, dz_kmax=9.0), LEAD))  # raising the nut is the wrong sign


# ---------------------------------------------------------------- G6: interference report
@H.label("discriminator", 7)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_G6_report_is_tool_generated_and_its_cells_equal_the_probe_json(d):
    text = H.require(H.REPORT).read_text(encoding="utf-8")
    assert "assemble_report.py" in "\n".join(text.splitlines()[:8]), "report header must name assemble_report.py"
    rows = gates.report_rows(text).get(H.tag(d))
    H.need(rows, f"report section '## Size {H.tag(d)}'")
    probes = {p: _pd(p, d) for p in H.POSES}
    assert len(rows) == 3 * (len(T["rels"]) + len(T["feats"])), len(rows)
    assert gates.report_errors(rows, probes, T) == []


@H.label("invariant", 4)
def test_G6_control_an_edited_cell_and_a_dropped_row_fire():
    probes = {p: synth_pose(p) for p in H.POSES}
    lines = []
    for pose, pd in probes.items():
        for key, errs in gates.pair_violations(pd, pose, T):
            a_b = key.replace("|", " / ")
            if key in pd["pairs"]:
                m3, dist = f"{pd['pairs'][key]['overlap_mm3']:.3f}", f"{pd['pairs'][key]['min_dist']:.3f}"
            else:
                m3, dist = "-", f"{pd['feature_pairs'][key]['gap']:.3f}"
            lines.append(f"| {a_b} | {pose} | {m3} | {dist} | {gates.pair_class_letter(key, pose, T)} | {'pass' if not errs else 'FAIL'} |")
    text = "## Size 100p0\n\n| Pair | Pose | mm3 | dist_mm | class | result |\n|---|---|---|---|---|---|\n" + "\n".join(lines) + "\n"
    rows = gates.report_rows(text)["100p0"]
    assert gates.report_errors(rows, probes, T) == []  # zero control
    edited = text.replace(lines[0], lines[0].replace(" 0.000 ", " 0.250 ", 1))
    assert edited != text and gates.report_errors(gates.report_rows(edited)["100p0"], probes, T) != []
    assert gates.report_errors(gates.report_rows("## Size 100p0\n" + "\n".join(lines[1:]))["100p0"], probes, T) != []  # a dropped row
    flipped = text.replace(lines[1], lines[1].replace(" pass |", " FAIL |"))
    assert gates.report_errors(gates.report_rows(flipped)["100p0"], probes, T) != []  # a verdict edited


# ---------------------------------------------------------------- G7: clamped solids and size coverage
@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", H.POSES)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_G7_pose_collet_is_the_generator_solid_for_that_pose(pose, d):
    rj = H.result_json(f"collet_{H.tag(d)}")
    want = rj["volume_mm3"] if pose == "R" else rj["clamped"][pose]["volume_mm3"]  # T4 and T5 read poses built from these solids
    H.require(H.CACHE / f"collet_{H.tag(d)}.FCStd" if pose == "R" else H.CACHE / f"collet_{H.tag(d)}_clamped_{pose}.FCStd")
    got = H.measure(_pd(pose, d), "collet_volume_mm3")
    assert got == pytest.approx(want, rel=5e-3), (got, want)
    if pose != "R":
        assert H.measure(_pd(pose, d), "slit_width_clamped_min") == pytest.approx(rj["clamped"][pose]["slit_width"], abs=0.05)


@H.label("invariant", 4)
def test_G7_family_parametrization_matches_across_A1a_A3d_A3e_A3h_A3i_T4_T5():
    import test_thread_clamp as TT

    def sizes(fn):
        vals = []
        for m in getattr(fn, "pytestmark", []):
            if m.name == "parametrize" and "d" in str(m.args[0]).replace(" ", "").split(","):
                names = str(m.args[0]).replace(" ", "").split(",")
                vals.append([v if not isinstance(v, tuple) else v[names.index("d")] for v in m.args[1]])
        return vals[0] if vals else None
    for fn in (TA.test_A1a_pair_matrix_by_pose_and_size, TA.test_A3d_lead_in_clearance_over_core_radius, TA.test_A3e_holder_bottom_above_the_receiver_floor,
               TA.test_A3h_nut_skirt_at_least_one_pitch_above_the_floor, TA.test_A3i_engaged_thread_length_in_every_pose):
        assert sizes(fn) == FAM, fn.__name__
    assert sorted({p[1] for m in TT.test_T4_thread_engagement.pytestmark if m.name == "parametrize" for p in m.args[1]}) == sorted([min(FAM), max(FAM)])
    assert sorted({p[0] for m in TT.test_T4_thread_engagement.pytestmark if m.name == "parametrize" for p in m.args[1]}) == sorted(H.POSES)
    assert len(FAM) == G("collets.count")
