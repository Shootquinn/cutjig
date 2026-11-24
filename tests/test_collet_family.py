"""Step 4 collet family tests: C1 to C10, F2, F3, F5 (collet row).
Discriminators read the collet probe (results/probes/collet_<tag>.json, tests/probes/probe_collet.py) and the generator result JSON
(parts_cache/collet_<tag>_result.json); neither exists at B4, so each fails with MISSING:. Invariants are params arithmetic and
checker controls and pass at B4. Predicates live in cad_helpers so each control calls the same function the real test calls.
Number basis: diameters are diametral, wall is radial (outer minus bore at a slit-free azimuth), slit width is tangential at mid-wall
radius, closure per slit is pi x Delta / N with Delta = s + c_i (collet_delta in cad_helpers)."""
import math

import pytest

import cad_helpers as H
from build_parts import common

P = H.P
G = lambda k: common.get(P(), k)
FAM = H.family()
EXTRA = (97.0, 93.7)  # C10b: off-grid sizes, between the 95 and 97.5 nominals and below the 95 nominal
IDS = [H.tag(d) for d in FAM]


def _c(d):
    return H.probe(f"collet_{H.tag(d)}", H.collet_inputs(d))


def _rj(d):
    return H.result_json(f"collet_{H.tag(d)}")


def _volume_errors(c, d):
    """C2 reference term: H.collet_expected_volume (profile with ledge, chamfer and cone; key; minus slits, relief holes, notches, label, lip),
    computed from params and the Loftsman definition. The +-5 percent band is unchanged."""
    return H.check_volume_band(c["volume_mm3"], H.collet_expected_volume(d)["total"])


def _bore_errors(c, d):
    n = int(G("collet.slit_count"))
    phi0 = G("receiver.key_offset_deg") + 15.0
    want = [(phi0 + 180.0 / n + 120.0 * k) % 360.0 for k in range(3)]
    e = [] if all(abs(((a - b + 180) % 360) - 180) < 1e-6 for a, b in zip(c["bore"]["az"], want)) else ["probe azimuths are not phi_0 + 180/N + 120k"]
    return e + H.check_bore(c["bore"], common.bore_free(P(), d))


def _all(c, rj, d):
    """C1 to C7 and C9b predicates for one collet; used by the family tests and by C10b."""
    n = int(G("collet.slit_count"))
    e = H.check_collet_valid(c) + _volume_errors(c, d) + _bore_errors(c, d)
    e += H.check_slits(c["slits"], n, G("collet.slit_width_seed")) + H.check_wall(c["wall_min_cone_top"], G("collet.min_wall"))
    e += H.check_topology(c) + H.check_cuts(rj.get("cuts", []))
    return e


# ---------------------------------------------------------------- C1 to C7 (per d)
@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C1_validity(d):
    assert H.check_collet_valid(_c(d)) == []


@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C2_volume_whole_part_and_per_cut(d):
    c, rj = _c(d), _rj(d)
    assert _volume_errors(c, d) == []
    names = " ".join(x["name"].lower() for x in rj.get("cuts", []))
    H.need("slit" in names and "relief" in names, "per-cut records for slits and relief holes in the generator result JSON")
    assert H.check_cuts(rj["cuts"]) == []
    ref = H.collet_expected_volume(d)  # the generator's own expected_mm3 must also match the independent integral of local wall thickness
    n = int(G("collet.slit_count"))
    want = {"slit": n // 2 * (ref["slit_cut"]["top"] + ref["slit_cut"]["bottom"]), "relief": ref["holes"]}
    for x in rj["cuts"]:
        for k, v in want.items():
            if k in x["name"].lower():
                assert abs(x["expected_mm3"] - v) <= 0.05 * v, (x["name"], x["expected_mm3"], v)


# SRC: Core diameter tolerance | ASSUMED | research/quinn/gameplan.md 400 | key=core.tol
@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C3_bore_diameter(d):
    assert _bore_errors(_c(d), d) == []


@H.label("discriminator", 5)
def test_C4_family_invariants():
    fam = H.probe("collet_family", [H.CACHE / f"collet_{H.tag(d)}.FCStd" for d in FAM])
    H.need(all(H.tag(d) in fam["tags"] for d in FAM), "all seven collets in collet_family.json")
    tags = [H.tag(d) for d in FAM]
    for key, common_v in fam["x_common"].items():
        a, b = key.split("|")
        if a in tags and b in tags:
            assert abs(common_v - fam["x_volume"][a]) <= H.OVERLAP_TOL and abs(common_v - fam["x_volume"][b]) <= H.OVERLAP_TOL, key
            # symmetric difference in the Loftsman region only (r >= r_out(z) - 1.2, z 0 to 32, minus notch and label boxes)
            H.need("symdiff_region_mm3" in fam, "region symmetric difference in collet_family.json (probe_collet.py, region_mask)")
            assert fam["symdiff_region_mm3"][key] <= H.OVERLAP_TOL, key
    H.need("symdiff_known_bad_mm3" in fam, "known-bad control in collet_family.json (slit widened by 0.5 mm)")
    assert fam["symdiff_zero_control_mm3"] <= H.OVERLAP_TOL, fam["symdiff_zero_control_mm3"]  # a size against itself
    assert fam["symdiff_known_bad_mm3"] > 1.0, fam["symdiff_known_bad_mm3"]  # the region sees a slit-width change
    probes = [_c(d) for d in FAM]
    for k in ("half_angle_deg", "large_od", "small_od", "seat_height"):
        vals = [p["outer"][k] for p in probes]
        assert max(vals) - min(vals) <= 0.02, (k, vals)


@H.label("invariant", 4)
def test_C4_control_region_excludes_per_size_features_and_keeps_a_slit_width_change():
    D = H.collet_dims(90.0)
    ro = D["outer"]
    az_plain, az_slit, az_notch, az_label = 67.0, 52.0 + 0.9 / 61.0 * 180.0 / math.pi, 97.0, 7.0
    assert H.collet_c4_region(ro(12.0) - 0.5, 12.0, az_plain)                      # zero control: outer skin at a probe azimuth is compared
    assert H.collet_c4_region(ro(12.0) - 0.5, 12.0, az_slit)                       # known-bad: a slit-width change lands in the region
    assert not H.collet_c4_region(D["r_b"] + 1.0, 10.0, az_plain)                  # bore difference between sizes is excluded
    assert not H.collet_c4_region(ro(30.0) - 3.0, 30.0, az_plain)                  # chamfer and lip are inside r_out - 1.2
    assert not H.collet_c4_region(ro(30.5) - 0.5, 30.5, az_notch)                  # a rim notch (size marker) is excluded
    assert H.collet_c4_region(ro(30.5) - 0.5, 30.5, az_plain)                      # the same height off a notch is compared
    assert not H.collet_c4_region(ro(16.0) - 0.5, 16.0, az_label)                  # the label window is excluded
    assert H.collet_c4_region(ro(16.0) - 0.5, 16.0, az_plain)


@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C5_slits(d):
    c = _c(d)
    n = int(G("collet.slit_count"))
    assert H.check_slits(c["slits"], n, G("collet.slit_width_seed")) == []
    assert c["relief_holes"] == n
    law = math.pi * H.collet_delta() / n + G("collet.min_slit_clamped")  # w_s >= pi x Delta / N + w_min
    assert all(w >= law - 0.05 for w in c["slits"]["width"]), (c["slits"]["width"], law)
    assert G("collet.slit_width_seed") >= law  # C5 conflict 3: the law is a lower bound (1.416); params 1.5 governs the built width and clears it by 0.084


# SRC: Printer: not a design input | DECLARED | research/quinn/gameplan.md 411
@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C6_minimum_wall_at_the_cone_top(d):
    assert H.check_wall(_c(d)["wall_min_cone_top"], G("collet.min_wall")) == []


@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C7_topology(d):
    c = _c(d)
    assert H.check_collet_valid(c) == [] and H.check_topology(c) == []
    ref = _c(FAM[0])["euler_VEF"]
    assert c["euler_VEF"] == ref  # same alternating-slit topology for every size
    print(f"C7 d {d}: euler_VEF {c['euler_VEF']} min face area {c['min_face_area']:.4f} min edge {c['min_edge_len']:.4f}")


# ---------------------------------------------------------------- C8 coverage (invariant: params arithmetic)
# SRC: Core diameter tolerance | ASSUMED | research/quinn/gameplan.md 400 | key=core.tol
# SRC: Core range 90 to 105 mm | CONTRACT | workorder.md
# SRC: Core nominal 100 mm | VERIFIED | INSITU2_text.md phrase "pre-cast to 100 mm" (conflict: "is above 100 mm")
def _uncovered(fam, params=None):
    p = params or P()
    tol = common.get(p, "core.tol")
    lo_all, hi_all = min(H.family(p)), max(H.family(p))  # the core range comes from the declared family, not from the collets under test
    rng = [H.accept_range(d, p) for d in fam]
    miss = []
    x = int(lo_all)
    while x <= hi_all + 1e-9:  # every core diameter 90 to 105 in 1 mm steps, widened by core.tol on both sides
        for pt in (x - tol, x + tol):
            if not any(lo - 1e-9 <= pt <= hi + 1e-9 for lo, hi in rng):
                miss.append(pt)
        x += 1
    return miss


@H.label("invariant", 4)
def test_C8_family_coverage():
    fam = H.family()
    assert _uncovered(fam) == []
    for d in fam:  # the accept range follows Delta = s + c_i and bore_free, it is not asserted
        lo, hi = H.accept_range(d)
        assert hi == pytest.approx(d + G("core.tol"))
        assert hi - lo == pytest.approx(G("collet.grip_window_hi") - G("collet.grip_window_lo"))


@H.label("invariant", 4)
def test_C8_control_removing_a_mid_collet_fires():
    fam = H.family()
    assert _uncovered(fam) == []  # zero control
    cut = [d for d in fam if d != 97.5]
    assert _uncovered(cut) != []  # known-bad
    assert _uncovered([d for d in fam if d != 90.0]) != []


# ---------------------------------------------------------------- C9a closure arithmetic (invariant) and C9b measured
# SRC: Friction mu_k about 0.35 | ASSUMED | research/quinn/gameplan.md 412 | key=collet.web_strain_allow
@H.label("invariant", 4)
def test_C9a_closure_arithmetic_and_web_strain():
    n, delta = int(G("collet.slit_count")), H.collet_delta()
    closure = math.pi * delta / n
    assert G("collet.delta") == pytest.approx(delta)  # params key agrees with the grip-window derivation
    assert closure < G("collet.slit_width_seed") - G("collet.min_slit_clamped")
    assert G("collet.clamped_slit") == pytest.approx(G("collet.slit_width_seed") - closure, abs=0.001)
    strain = H.web_strain(delta, n, G("collet.slit_length"), G("collet.relief_hole_dia"))
    assert strain <= G("collet.web_strain_allow")
    print(f"C9a closure {closure:.4f} mm, web strain {strain:.5f} against allowable {G('collet.web_strain_allow')}")


@H.label("invariant", 4)
def test_C9a_control_too_few_slits_or_a_small_hole_fires():
    delta = H.collet_delta()
    ok = math.pi * delta / 12 < G("collet.slit_width_seed") - G("collet.min_slit_clamped")
    assert ok  # zero control
    assert not (math.pi * delta / 8 < G("collet.slit_width_seed") - G("collet.min_slit_clamped"))  # known-bad: N = 8
    assert H.web_strain(delta, 12, G("collet.slit_length"), 4.0) > G("collet.web_strain_allow")  # known-bad: 4 mm relief hole


@H.label("discriminator", 5)
def test_C9b_measured_slit_width_wall_and_stiffness_ratio():
    n = int(G("collet.slit_count"))
    lo, hi = _c(min(FAM)), _c(max(FAM))
    floor = math.pi * H.collet_delta() / n + G("collet.min_slit_clamped") - 0.05
    for c in (lo, hi):
        assert min(c["slits"]["width"]) >= floor
    w_lo, w_hi = lo["wall_min_cone_top"], hi["wall_min_cone_top"]
    ratio = (w_hi / w_lo) ** 3  # screening: stiffness of a wall strip scales with thickness cubed (ASSUMED model, recorded)
    assert w_lo > 0 and w_hi > 0 and math.isfinite(ratio)
    print(f"C9b wall d {min(FAM)}: {w_lo:.3f} mm, d {max(FAM)}: {w_hi:.3f} mm, stiffness ratio {ratio:.3f}")


# ---------------------------------------------------------------- C3 control (invariant)
@H.label("invariant", 4)
def test_C3_control_probes_at_0_120_240_hit_the_slits_of_a_12_slit_stand_in():
    n = 12
    half_deg = 1.5 / 2 / 50.0 * 180 / math.pi  # 1.5 mm slit at r 50, half width in degrees
    assert all(H.slit_hit(a, 0.0, n, half_deg) for a in (0.0, 120.0, 240.0))  # known-bad stand-in: slits at 0 + 30k, probes at 0, 120, 240
    phi0 = G("receiver.key_offset_deg") + 15.0
    assert not any(H.slit_hit(phi0 + 180.0 / n + 120.0 * k, phi0, n, half_deg) for k in range(3))  # zero control: the real probe azimuths
    bore = {"slit_hits": [False] * 3, "dia": [99.0, 99.0, 99.0]}
    assert H.check_bore(bore, 99.0) == []
    assert H.check_bore(dict(bore, slit_hits=[True, False, False]), 99.0) != []
    assert H.check_bore(dict(bore, dia=[99.5] * 3), 99.0) != []


@H.label("invariant", 4)
def test_C_predicate_controls_zero_and_known_bad():
    good_c = {"solids": 1, "valid": True, "closed": True, "bad_edges": 0, "slit_plane_faces": 0}
    assert H.check_collet_valid(good_c) == [] and H.check_topology(good_c) == []
    assert H.check_collet_valid(dict(good_c, solids=2)) != [] and H.check_collet_valid(dict(good_c, closed=False)) != []
    assert H.check_topology(dict(good_c, bad_edges=3)) != [] and H.check_topology(dict(good_c, slit_plane_faces=1)) != []
    assert H.check_volume_band(100.0, 100.0) == [] and H.check_volume_band(80.0, 100.0) != []
    cuts = [{"name": "slits", "before_mm3": 1000.0, "after_mm3": 950.0, "tool_mm3": 60.0, "expected_mm3": 50.0}]
    assert H.check_cuts(cuts) == []
    assert H.check_cuts([dict(cuts[0], after_mm3=900.0)]) != []  # removed 100 > tool 60
    assert H.check_cuts([dict(cuts[0], expected_mm3=40.0)]) != []  # 25 percent off the analytic expectation
    assert H.check_cuts([dict(cuts[0], after_mm3=1000.0)]) != []  # a cut that removed nothing
    n, seed = 12, G("collet.slit_width_seed")
    s = {"count": 12, "plane_offset": [0.0] * 12, "width": [seed] * 12, "void_depth": [20.0] * 12, "solid_below": [True] * 12}
    assert H.check_slits(s, n, seed) == []
    assert H.check_slits(dict(s, count=11), n, seed) != [] and H.check_slits(dict(s, width=[seed + 0.2] * 12), n, seed) != []
    assert H.check_slits(dict(s, plane_offset=[0.05] * 12), n, seed) != [] and H.check_slits(dict(s, solid_below=[False] * 12), n, seed) != []
    assert H.check_wall(1.3, 1.2) == [] and H.check_wall(1.0, 1.2) != []
    assert H.check_flip(0.2, H.FLIP_FLOOR) == [] and H.check_flip(0.0, H.FLIP_FLOOR) != []  # a plain disc flips onto itself


# ---------------------------------------------------------------- C10
# SRC: Iris throat opening | DECLARED | research/quinn/gameplan.md 394 | key=iris.throat_open_radius
@H.label("invariant", 4)
def test_C10a_request_above_the_envelope_is_refused_with_a_reason(params):
    cap = common.get(params, "collets.envelope_max")
    assert common.check_envelope_request(params, cap) == []  # zero control
    for d in EXTRA:
        assert common.check_envelope_request(params, d) == []
    errs = common.check_envelope_request(params, cap + 0.5)
    assert errs and "exceeds envelope cap" in errs[0] and "iris.throat_open_radius" in errs[0]
    assert common.check_envelope_request(params, 130.0) != []


@H.label("discriminator", 5)
@pytest.mark.parametrize("d", EXTRA, ids=[H.tag(x) for x in EXTRA])
def test_C10b_generate_off_grid_collet_from_the_usage_doc(d):
    doc = H.require(H.ROOT / "docs" / "collet_generator_usage.md")  # the doc is the only instruction
    assert H.check_usage_doc(doc) == []
    c, rj = _c(d), _rj(d)
    assert d not in FAM
    assert _all(c, rj, d) == []
    assert rj.get("run_seconds") is not None
    fam = H.probe("collet_family", H.collet_inputs(d))
    assert any(H.tag(d) in k for k in fam["x_common"])  # C4 holds against the seven: the off-grid size is in the pair data
    print(f"C10b d {d}: generated in {rj['run_seconds']} s")


@H.label("invariant", 4)
def test_C10b_control_missing_usage_doc_fires(tmp_path):
    good = tmp_path / "usage.md"
    good.write_text("Run freecadcmd with the generator script and one diameter argument. " * 8, encoding="utf-8")
    assert H.check_usage_doc(good) == []  # zero control
    assert H.check_usage_doc(tmp_path / "absent.md") != []  # known-bad: doc missing
    empty = tmp_path / "empty.md"
    empty.write_text("TODO", encoding="utf-8")
    assert H.check_usage_doc(empty) != []


# ---------------------------------------------------------------- F2, F3, F5
@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_F2_core_in_collet(d):
    cb = _c(d)["core_in_bore"]
    assert cb["interference_mm3"] < H.OVERLAP_TOL
    assert H.check_base_gap(cb["base_gap"]) == []  # base_gap = ledge top z - collet.core_seat_height (probe), not the 1.0 mm radial clearance
    assert cb["ledge_top"] == pytest.approx(G("collet.core_seat_height"), abs=0.05)


@H.label("invariant", 4)
def test_F2_control_base_gap_is_ledge_height_not_radial_clearance():
    seat = G("collet.core_seat_height")
    assert H.check_base_gap(H.base_gap(seat, seat)) == []                  # zero control: ledge top at 2.5
    assert H.check_base_gap(H.base_gap(seat + 0.5, seat)) != []            # known-bad: ledge 0.5 high
    assert H.check_base_gap(H.base_gap(seat, seat) - 4.0) != []            # the old distToShape - 5.0 reading (-4.0) fails


@H.label("invariant", 4)
def test_C2_control_reference_term_includes_chamfer_ledge_key_notches():
    ref = H.collet_expected_volume(90.0)
    assert H.check_volume_band(ref["total"], ref["total"]) == []                                    # zero control
    assert ref["chamfer"] > 10000 and ref["key"] > 50 and ref["notches"] > 0 and ref["label"] > 100  # the terms the old reference omitted
    assert H.check_volume_band(ref["total"] - ref["chamfer"], ref["total"]) != []                    # known-bad: build without the chamfer fires
    assert H.check_volume_band(ref["total"] * 0.9, ref["total"]) != []                              # the +-5 percent band is not widened


@H.label("discriminator", 5)
def test_F3_collet_and_core_sweep():
    delta = H.collet_delta()
    for d in FAM:
        sweep = _c(d)["sweep"]
        for dc in FAM:
            cell = sweep[str(dc)]
            fits = cell["interference_mm3"] <= H.OVERLAP_TOL           # core diameter plus tolerance enters the free bore
            clamps = cell["bore_minus_core"] <= delta + 0.02            # the slit closure can reach the core
            lo, hi = H.accept_range(d)
            predicted = lo - 1e-9 <= dc <= hi + 1e-9
            assert (fits and clamps) == predicted, (d, dc, cell, (lo, hi))
        assert (sweep[str(d)]["interference_mm3"] <= H.OVERLAP_TOL)    # the diagonal passes


CHECKLIST = ("slit", "relief hole", "foot key", "foot ring", "core seat", "rim notch", "label", "chamfer", "bore lip")


@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_F5_collet_row_feature_checklist_and_flipped_copy(d):
    rj, c = _rj(d), _c(d)
    names = {x["feature"].lower(): x for x in rj.get("features", [])}
    for want in CHECKLIST:
        hit = [v for k, v in names.items() if want in k]
        H.need(bool(hit), f"collet feature '{want}' in the generator result JSON")
        assert hit[0].get("volume_mm3", 0) > 0, want
    assert c["solids"] == 1 and H.check_flip(c["flip_mismatch_fraction"], H.FLIP_FLOOR) == []


# ---------------------------------------------------------------- Step 5 additions: markers, chamfer rule, clamped slit, caddy, refusal
def _feat(rj, word):
    hit = [x for x in rj.get("features", []) if word in x["feature"].lower()]
    H.need(bool(hit), f"collet feature '{word}' in the generator result JSON")
    return hit[0]


@H.label("invariant", 4)
def test_C_rule_arithmetic_chamfer_notch_colour_label_clamped_width_caddy():
    table = {85.0: (10.5, 1), 90.0: (10.5, 1), 92.5: (10.05, 2), 93.7: (9.45, 2), 95.0: (8.8, 3), 97.0: (7.8, 4), 100.0: (6.3, 5),
             105.0: (3.8, 7), 106.585: (2.5, 7)}  # Loftsman table: c and family index (notch count, colour index)
    for d, (c, idx) in table.items():
        assert H.collet_chamfer_c(d) == pytest.approx(c, abs=0.005), d
        assert H.collet_family_index(d) == idx, d
    assert H.collet_label_text(92.5) == "92.5 | 91.0-93.5"
    assert H.collet_clamped_slit_width(G("collet.grip_window_hi")) == pytest.approx(1.238, abs=0.001)
    assert H.collet_clamped_slit_width(G("collet.grip_window_lo")) == pytest.approx(0.584, abs=0.001)
    assert H.collet_clamped_slit_width(G("collet.grip_window_lo")) == pytest.approx(G("collet.clamped_slit"), abs=0.001)
    assert 2 * H.collet_dims(90.0)["r_fo"] + 2 * G("caddy.socket_clear") == pytest.approx(139.98, abs=0.005)
    old = lambda d: round((d - FAM[0]) / G("collets.spacing")) + 1                # known-bad: the unclamped params formula
    assert old(85.0) == -1 and old(106.585) == 8                                   # leaves the 1 to 7 range
    assert min(H.collet_dims(106.585)["r0"] - 30.0 * H.collet_dims(106.585)["tan"] - H.collet_dims(106.585)["r_b"] - G("collet.min_wall"), 10.5) > 2.5  # without the 2.5 branch c would be 3.0


@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C11_chamfer_and_bore_lip_follow_the_rule(d):
    rj = _rj(d)
    ch, lip = _feat(rj, "chamfer"), _feat(rj, "bore lip")
    c = H.collet_chamfer_c(d)
    assert ch["c_mm"] == pytest.approx(c, abs=0.01) and ch["edge_z"] == pytest.approx(H.collet_dims(d)["edge_z"], abs=0.01)
    assert ch["c_mm"] >= G("collet.chamfer_floor")
    assert lip["radius"] == pytest.approx(G("collet.bore_lip_radius"), abs=1e-6)


@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C12_size_markers_notch_count_colour_and_label_text(d):
    rj = _rj(d)
    idx = H.collet_family_index(d)
    H.need("notch_count" in rj and "colour" in rj and "label_text" in rj, "notch_count, colour, label_text in the generator result JSON")
    assert rj["notch_count"] == idx == FAM.index(d) + 1
    assert rj["colour"] == G("collet.colour")[idx - 1]
    assert rj["label_text"] == H.collet_label_text(d)


@H.label("discriminator", 5)
def test_C13_caddy_socket_clearance_record():
    for d in FAM:
        rec = _rj(d).get("caddy")
        H.need(rec is not None, "caddy fit record in the generator result JSON")
        assert rec["socket_d"] == pytest.approx(2 * H.collet_dims(d)["r_fo"] + 2 * G("caddy.socket_clear"), abs=0.01), d
        assert rec["socket_depth"] == G("caddy.socket_depth") and rec["margin"] == pytest.approx(rec["socket_depth"] - rec["height"], abs=0.01)
        assert rec["height"] == pytest.approx(H.collet_dims(d)["height"], abs=0.01) and rec["margin"] > 0


@H.label("discriminator", 5)
@pytest.mark.parametrize("d", FAM, ids=IDS)
def test_C14_clamped_slit_width_at_kd1_and_kmax(d):
    cl = _rj(d).get("clamped")
    H.need(cl is not None and "Kd1" in cl and "Kmax" in cl, "clamped slit widths for Kd1 and Kmax in the generator result JSON")
    for pose, off in (("Kd1", G("collet.grip_window_hi")), ("Kmax", G("collet.grip_window_lo"))):
        assert cl[pose]["slit_width"] == pytest.approx(H.collet_clamped_slit_width(off), abs=0.01), (pose, cl[pose])
        assert cl[pose]["slit_width"] >= G("collet.min_slit_clamped")


@H.label("discriminator", 5)
def test_C15_generator_refuses_a_request_above_the_envelope_before_building():
    H.require(H.ROOT / "build_parts" / "collet_family.py")
    from build_parts import collet_family
    cap = G("collets.envelope_max")
    assert common.check_envelope_request(P(), cap) == []  # zero control: the cap itself is accepted by the predicate
    for d in (cap + 0.5, 130.0):
        with pytest.raises(Exception) as e:
            collet_family.build_collet(d)
        assert "exceeds envelope cap" in str(e.value) and "iris.throat_open_radius" in str(e.value), str(e.value)
        assert not (H.CACHE / f"collet_{H.tag(d)}.FCStd").exists()  # known-bad: a refused request writes no file
