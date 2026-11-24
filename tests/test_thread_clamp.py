"""Step 4 thread and clamp tests: T1a to T3, T4, T5, T7 to T9, F1, F4.
T1a to T3, T8, T9 read only the receiver, nut and holder shapes, through results/probes/{thread,thread_mesh,tilt}.json
(tests/probes/probe_thread.py, probe_thread_mesh.py, probe_tilt.py under freecadcmd). They exist at B4: invariants.
T4, T5 read pose artifacts (Step 7). F1 reads the collet probe (Step 5). T7 reads the prediction record in common.py (absent at B4: Step 8).
Number basis: radii are centre-line radii of the part, diameters are 2 x radius; clearances c_r radial per side, g_a the total axial gap at
the pitch line (nut groove width minus receiver tooth width, g_a / 2 per flank)."""
import math

import pytest

import cad_helpers as H
from build_parts import common

P = H.P
G = lambda k: common.get(P(), k)
FAM = H.family()
D_MIN, D_MAX = min(FAM), max(FAM)
THREAD_IN = H.part_inputs("receiver", "nut")


def _thread():
    return H.probe("thread", THREAD_IN)


# ---------------------------------------------------------------- T1a to T1c
@H.label("invariant", 4)
def test_T1a_chirality_on_receiver_boss_and_nut():
    d = _thread()
    pitch = G("thread.pitch")
    assert common.HAND == "right"
    assert d["receiver"]["self_check"] and d["nut"]["self_check"]  # p + eps n outside, p - eps n inside, before any sign is read
    assert H.check_chirality(d["receiver"]["dz0"], d["receiver"]["dz90"], pitch, common.HAND) == []
    assert H.check_chirality(d["nut"]["dz0"], d["nut"]["dz90"], pitch, common.HAND) == []
    m = d["nut_mirrored"]
    assert H.check_chirality(m["dz0"], m["dz90"], pitch, common.HAND) != []  # known-bad: the mirrored nut fires
    src = {n: (H.ROOT / "build_parts" / f"{n}.py").read_text(encoding="utf-8") for n in ("receiver", "nut")}
    assert all("thread_ridge_stud" in t and "hand_right=False" not in t and "reversed_=True" not in t for t in src.values())  # one helix function, one hand (stud-subtract, Step 4 fix pass)


@H.label("invariant", 4)
def test_T1a_control_synthetic_helices_and_mirror():
    pitch = 8.0
    right = H.helical_blade_mesh(pitch, "right")
    left = H.helical_blade_mesh(pitch, "left")
    z0, z90 = H.ridge_dz_blade(right, 73.0, pitch)
    assert H.check_chirality(z0, z90, pitch, "right") == []  # zero control
    z0, z90 = H.ridge_dz_blade(left, 73.0, pitch)
    assert H.check_chirality(z0, z90, pitch, "right") != []  # known-bad
    assert H.check_chirality(z0, z90, pitch, "left") == []


@H.label("invariant", 4)
def test_T1b_screw_motion_mesh_and_opposite_hand():
    d = H.probe("thread_mesh", THREAD_IN)
    assert d["baseline_common"] <= H.OVERLAP_TOL
    assert all(v <= H.OVERLAP_TOL for v in d["screw_common"].values()), d["screw_common"]
    assert sorted(d["screw_common"]) == ["15", "180", "360", "90"]
    assert d["opposite_hand_90"] > 100 * H.OVERLAP_TOL  # known-bad: opposite-hand motion at 90 degrees interferes
    assert d["pure_rotation_90"] > 100 * H.OVERLAP_TOL  # known-bad: pure rotation interferes


@H.label("invariant", 4)
def test_T1c_clockwise_turn_lowers_the_nut():
    d = _thread()
    assert d["receiver"]["rise_sign"] == 1 and d["nut"]["rise_sign"] == 1  # right hand: the ridge rises with +theta
    m = H.probe("thread_mesh", THREAD_IN)
    assert m["cw_down_dz"] < 0 and m["cw_down_common"] <= H.OVERLAP_TOL  # clockwise 90 degrees from K: dz < 0, no interference
    assert d["nut_mirrored"]["dz90"] != pytest.approx(d["nut"]["dz90"])  # known-bad: the mirrored nut turns the other way


# ---------------------------------------------------------------- T2, T3
@H.label("invariant", 4)
def test_T2_thread_dimensions_against_the_step3_chain():
    d = _thread()
    r, n = d["receiver"], d["nut"]
    chain = H.thread_major_chain()
    assert chain == pytest.approx(G("thread.major"), abs=0.005)  # params carries the chain output, not a constant
    assert 2 * r["crest_r"] == pytest.approx(chain, abs=0.05)
    assert 2 * r["root_r"] == pytest.approx(chain - 2 * G("chain.h"), abs=0.05)
    assert r["crest_r"] - r["root_r"] == pytest.approx(G("chain.h"), abs=0.05)  # tooth depth
    for part in (r, n):
        assert part["lead"] == pytest.approx(G("thread.pitch"), abs=0.05)  # pitch = lead
        assert part["starts"] == pytest.approx(G("thread.starts"), abs=0.01)
        assert part["down_flank_deg"] == pytest.approx(G("thread.flank_deg"), abs=0.5)
        assert part["up_flank_deg"] == pytest.approx(G("thread.flank_deg"), abs=0.5)
    assert r["tooth_w_crest"] == pytest.approx(G("thread.land_width"), abs=0.05)  # crest flat
    assert r["tooth_w_pitch"] == pytest.approx(G("thread.pitch") / 2.0, abs=0.05)


# SRC: Printer: not a design input | DECLARED | gameplan.md 411
@H.label("invariant", 4)
def test_T3_crest_clearance_and_flank_gap():
    c = _thread()["clearance"]
    for k in ("c_r_root_side", "c_r_crest_side"):
        assert c[k] == pytest.approx(G("fit.c_r"), abs=0.05), k
        assert c[k] > G("fit.c_r_min")
    assert c["g_a_total"] == pytest.approx(G("fit.g_a"), abs=0.05)  # total at the pitch line, g_a / 2 per flank
    assert c["g_a_total"] > G("fit.g_a_min")


@H.label("invariant", 4)
def test_T2_T3_control_thresholds_fire():
    d = _thread()
    assert abs(2 * d["receiver"]["crest_r"] - H.thread_major_chain()) <= 0.05  # zero control
    assert abs(165.0 - H.thread_major_chain()) > 0.05  # known-bad: the superseded 165 mm seed
    assert abs(d["clearance"]["c_r_root_side"] - G("fit.c_r")) <= 0.05
    assert abs((d["clearance"]["c_r_root_side"] + 0.2) - G("fit.c_r")) > 0.05  # known-bad: 0.2 mm off


# ---------------------------------------------------------------- T8
@H.label("invariant", 4)
def test_T8_no_down_facing_flank_below_45_degrees():
    d = _thread()
    floor = G("thread.flank_deg")  # 45 degrees from horizontal for a 45/45 form
    assert H.check_overhang(d["receiver"]["down_flank_deg"], floor) == []
    assert H.check_overhang(d["nut"]["down_flank_deg"], floor) == []


@H.label("invariant", 4)
def test_T8_control_tr15_profile_fires():
    assert H.check_overhang(45.0, 45.0) == []  # zero control
    assert H.check_overhang(15.0, 45.0) != []  # known-bad: Tr 15 degree flank


# ---------------------------------------------------------------- T9
# Loftsman ruling (cr_scratch/step4_loftsman_t9_ruling.md). Cross-threading is a half-pitch axial misregistration across the thread
# diameter at thread start: D tan(alpha) >= P / 2. alpha = measured register stop (holder in the bore at first thread contact,
# probe_tilt.py) + plate rock atan(p / arm). Pass line: margin 1.5 on P / 2, the same line as register.tilt_limit_deg = alpha_crit / 1.5.
# Margin 1.5: DECLARED design margin, cr_scratch/step2_loftsman_crossreview_reply.md section 3 (not a Register row).
T9_MARGIN = 1.5


def _tilt():
    return H.probe("tilt", H.part_inputs("receiver", "holder", "nut"))


def _t9_thread():
    r = _thread()["receiver"]
    return 2.0 * r["crest_r"], r["lead"]  # measured D (crest diameter, the widest contact span) and P


def _t9_rock_deg():
    arm = G("washer.id") / 2.0 + G("nut.plate_hole_dia") / 2.0  # washer lower contact to plate-hole upper contact, 136.44
    return math.degrees(math.atan(G("nut.lift_play") / arm))


def _t9_fails(alpha_deg, D, pitch):
    mis = D * math.tan(math.radians(alpha_deg))
    return [] if T9_MARGIN * mis <= pitch / 2.0 else [f"misregistration {mis:.3f} mm x {T9_MARGIN} > P/2 {pitch / 2.0:.3f} mm at {alpha_deg:.3f} deg"]


def _edge_stop_deg(insertion):
    """Analytic register stop: holder generator (diameter d) meets the bore edge (diameter Db) at L = insertion - chamfer above the
    bottom wall contact: d + L sin a = Db cos a."""
    d, Db = 2 * (G("receiver.register_bore_radius") - G("register.g_reg")), 2 * G("receiver.register_bore_radius")
    L, lo, hi = insertion - G("receiver.register_chamfer"), 0.0, 0.2
    for _ in range(60):
        m = 0.5 * (lo + hi)
        lo, hi = (m, hi) if d + L * math.sin(m) < Db * math.cos(m) else (lo, m)
    return math.degrees(lo)


@H.label("invariant", 4)
def test_T9_probe_is_self_consistent():
    d = _tilt()
    assert d["tilt_deg"] == pytest.approx(G("register.t9_tilt_deg"))
    assert all(s["valid"] for s in d["samples"]), [s for s in d["samples"] if not s["valid"]]  # V_common == V_receiver - V_cut
    for key in ("register", "short_register"):
        r = d[key]
        assert r["valid"] and r["stop_deg"] is not None, r
        assert r["common_at_zero_mm3"] <= H.OVERLAP_TOL  # zero control: the wall pose is clear at zero tilt
        a = _edge_stop_deg(r["insertion_mm"])
        assert a <= r["stop_deg"] <= a + 0.03, (key, r["stop_deg"], a)  # the instrument reads the cylinder-in-bore stop
    assert d["register"]["insertion_mm"] == pytest.approx(G("receiver.register_depth") + G("nut.lift_play"))
    assert d["flank_gap_zero_tilt_mm"] == pytest.approx(G("fit.g_a") / 2.0 * 0.70710678, abs=0.01)  # flank-normal gap at thread start
    lo, hi = (d["axial_drop"]["%.3f" % (G("fit.g_a") / 2.0 + s * d["drop_band_mm"])] for s in (-1, 1))
    assert lo["valid"] and hi["valid"]
    assert lo["common_mm3"] <= H.OVERLAP_TOL < hi["common_mm3"]  # the nut rests on the flank at g_a/2: clear below, interfering above


@H.label("invariant", 4)
def test_T9_control_short_register_and_double_critical_tilt_fire():
    d = _tilt()
    D, pitch = _t9_thread()
    a_crit = math.degrees(math.atan(pitch / (2.0 * D)))
    assert _t9_fails(0.0, D, pitch) == []  # zero control
    short = d["short_register"]["stop_deg"] + _t9_rock_deg()
    assert _t9_fails(short, D, pitch) != []  # known-bad: the superseded L_h 54 register, measured, can cross-thread
    assert _t9_fails(2 * a_crit, D, pitch) != []  # known-bad: 2 x alpha_crit is a full pitch across D
    assert d["register_common_at_2x_crit_mm3"] is not None and d["register_common_at_2x_crit_mm3"] > H.OVERLAP_TOL  # the register blocks it


@H.label("invariant", 4)
def test_T9_register_tilt_keeps_cross_thread_misregistration_under_half_pitch():
    d = _tilt()
    D, pitch = _t9_thread()
    total = d["register"]["stop_deg"] + _t9_rock_deg()
    assert _t9_fails(total, D, pitch) == []
    assert total <= G("register.tilt_limit_deg")
    assert total <= G("register.t9_tilt_deg") + 0.005  # params carries an upper bound on the measured tilt
    mis = D * math.tan(math.radians(total))
    print(f"T9: register {d['register']['stop_deg']:.4f} + rock {_t9_rock_deg():.4f} = {total:.4f} deg; "
          f"misregistration {mis:.3f} mm against P/2 {pitch / 2:.3f} (factor {pitch / 2 / mis:.3f})")


# ---------------------------------------------------------------- F4
# SRC: 106.369 mm | VERIFIED | double_dong_params.py 372-380
@H.label("invariant", 4)
def test_F4_exposed_core_arithmetic_and_assumed_standoff(params, mutated):
    g = lambda k, p=None: common.get(p or params, k)
    total = g("drill.kerf_standoff") + g("stop.g_stop") + g("stop.margin") + g("collar.top_above_plate")
    assert total == pytest.approx(143.119, abs=0.001)
    assert g("core.min_exposed") == pytest.approx(total, abs=0.01)
    assert common.leaf(params, "drill.kerf_standoff")["status"] == "ASSUMED"  # applicability to the 6 in drill
    assert "kerf SPHERE CENTRE" in common.leaf(params, "drill.kerf_standoff")["source"]
    low = mutated("stop.g_stop", 10)  # known-bad: the superseded g_stop gives 128.12
    assert abs(g("drill.kerf_standoff", low) + g("stop.g_stop", low) + g("stop.margin", low) + g("collar.top_above_plate", low)
               - g("core.min_exposed")) > 1.0
    print("recorded core lengths: install", g("core.length_install"), "optional", g("core.length_optional"))


# ---------------------------------------------------------------- T7
# SRC: Holding torque 10 N m (jig) | DECLARED | gameplan.md 401 | key=loads.torque_design
@H.label("discriminator", 8)
def test_T7_holding_torque_prediction_record_with_labelled_inputs(params):
    fn = getattr(common, "holding_torque", None)
    H.need(callable(fn), "common.holding_torque(params, d) prediction record (inputs with labels), T7")
    for d in (D_MIN, D_MAX):
        rec = fn(params, d)
        assert rec["value_nm"] > 0 and rec["inputs"], rec
        for key, lab in rec["inputs"].items():
            assert common.leaf(params, key)["status"] == lab, (key, lab)
        print(f"T7 d {d}: predicted {rec['value_nm']:.2f} N m, margin to loads.torque_design {rec['value_nm'] - common.get(params, 'loads.torque_design'):.2f}")


# ---------------------------------------------------------------- F1
@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=[H.tag(x) for x in FAM])
def test_F1_collet_seat_fit(d):
    c = H.probe(f"collet_{H.tag(d)}", H.collet_inputs(d))
    clr, tol = G("fit.seat_clearance"), 0.05
    s = c["seat"]
    H.need(s.get("R_gap_min") is not None, "collet cone inside holder cone, R pose")
    assert abs(s["R_gap_min"] - clr) <= tol and abs(s["R_gap_max"] - clr) <= tol, s
    for pose in ("Kd1", "Kmax"):
        H.need(pose in s, f"clamped collet solid, pose {pose} (generator output collet_{H.tag(d)}_clamped_{pose}.FCStd)")
        assert s[pose]["common_mm3"] < H.OVERLAP_TOL, s[pose]
        assert s[pose]["contact_mm2"] > G("seat.min_contact_area"), s[pose]


# ---------------------------------------------------------------- T4, T5
@H.label("discriminator", 7)
@pytest.mark.parametrize("pose,d", [(p, x) for p in H.POSES for x in (D_MIN, D_MAX)], ids=lambda v: str(v))
def test_T4_thread_engagement(pose, d):
    data = H.probe(f"pose_{pose}_{H.tag(d)}", H.pose_inputs(pose, d))
    assert H.measure(data, "engaged_mm") >= G("thread.min_engage_pitches") * G("thread.pitch")


@H.label("invariant", 4)
def test_T4_control_nut_at_the_top_reads_zero():
    nut_zone, rec_zone = (60.0, 108.0), (40.5, 88.5)
    assert H.interval_overlap(nut_zone, rec_zone) > 0  # zero control: overlapping zones read nonzero
    assert H.interval_overlap((90.0, 138.0), rec_zone) == 0  # nut at the top, no overlap, reads 0


# SRC: Core diameter tolerance | ASSUMED | gameplan.md 400 | key=core.tol
@H.label("discriminator", 7)
@pytest.mark.parametrize("pose", ["R", "Kmax"])
@pytest.mark.parametrize("d", [D_MIN, D_MAX], ids=lambda v: H.tag(v))
def test_T5_clamp_range_at_the_extremes(pose, d):
    c = H.probe(f"collet_{H.tag(d)}", H.collet_inputs(d))
    pd = H.probe(f"pose_{pose}_{H.tag(d)}", H.pose_inputs(pose, d))
    if pose == "R":
        assert sum(c["bore"]["dia"]) / len(c["bore"]["dia"]) >= common.bore_free(P(), d) - 0.02
        assert c["sweep"][str(d)]["interference_mm3"] <= H.OVERLAP_TOL  # a core of d + tau slides in
    else:
        assert H.measure(pd, "slit_width_clamped_min") > G("collet.min_slit_clamped")
        assert H.measure(pd, "nut_stop_travel_mm") >= G("thread.pitch")  # S12: physical stop (nut rim on plate underside) leaves one pitch of travel
        assert pd["feature_pairs"]["holder flange underside|receiver rim"]["gap"] > 0
    assert H.measure(pd, "engaged_mm") >= G("thread.min_engage_pitches") * G("thread.pitch")
