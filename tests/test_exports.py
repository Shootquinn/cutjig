"""Step 4 export and independent re-measure tests: E1, E2, E3, T1d, B1, X1.
STL checks are pure Python (cad_helpers.read_stl, stl_metrics). STEP re-import needs FreeCAD, so E1 and the STEP half of T1d read
results/probes/exports.json (tests/probes/probe_exports.py). X1 is independent/x1_remeasure.py, written at Step 10, sharing no code
with build_parts or tests; its output is results/x1_remeasure.json.
Files: output/step/<name>.step, output/stl/<name>.stl, results/rebuild_record.json {run_started_epoch, first{name: volume}, second{name: volume}},
parts_cache/<name>_result.json carrying tessellation{linear_deflection, angular_deflection_deg}.
Names: the five Step 3 parts, collet_<tag> for each core.diameters entry, and "assembly" (STEP only)."""
import json

import pytest

import cad_helpers as H
from build_parts import common

P = H.P
G = lambda k: common.get(P(), k)
FAM = H.family()
COLLETS = [f"collet_{H.tag(d)}" for d in FAM]
PRINTABLE = list(H.FIVE_PARTS) + COLLETS
STEP_NAMES = PRINTABLE + ["assembly"]
OUT = H.ROOT / "output"
PITCH_WINDOW = {"nut": (8.0, 32.0), "receiver": (48.5, 80.5)}  # thread zones used for the ridge phase (z, part frame)


def _record():
    return json.loads(H.require(H.ROOT / "results" / "rebuild_record.json").read_text(encoding="utf-8"))


def _exports(names):
    return H.probe("exports", [OUT / "step" / f"{n}.step" for n in names])


# ---------------------------------------------------------------- E1 STEP
@H.label("discriminator", 10)
@pytest.mark.parametrize("name", STEP_NAMES)
def test_E1_step_export(name):
    f = H.require(OUT / "step" / f"{name}.step")
    assert f.stat().st_mtime >= _record()["run_started_epoch"]  # written by this run, not left over
    rec = _exports([name])[name]
    expect = len(H.parts_of(H.parse_assembly()[0])) if name == "assembly" else 1
    assert H.check_step_record(rec, expect, at_least=(name == "assembly")) == []
    if name == "assembly":
        assert set(H.parts_of(H.parse_assembly()[0])) <= set(rec["tree_names"])
    else:
        assert rec["tree_names"] == [name] or name in rec["tree_names"]


@H.label("invariant", 4)
def test_E1_checker_controls():
    good = {"step_solids": 1, "step_volume": 1000.0, "fcstd_volume": 1000.4, "unit": "mm", "tree_names": ["x"]}
    assert H.check_step_record(good, 1) == []  # zero control
    assert H.check_step_record(dict(good, step_solids=2), 1) != []  # known-bad: wrong solid count
    assert H.check_step_record(dict(good, step_volume=1010.0), 1) != []  # 1 percent off
    assert H.check_step_record(dict(good, unit="unverified"), 1) != []
    assert H.check_step_record(dict(good, fcstd_volume=None), 1) != []


# ---------------------------------------------------------------- E2 STL
def _stl(name):
    return H.read_stl(H.require(OUT / "stl" / f"{name}.stl"))


# SRC: Printer: not a design input | DECLARED | gameplan.md 411
@H.label("discriminator", 10)
@pytest.mark.parametrize("name", PRINTABLE)
def test_E2_stl_export(name):
    tris = _stl(name)
    m = H.stl_metrics(tris)
    rj = H.result_json(name)
    assert m["watertight"], m
    assert m["degenerate"] == 0, m
    assert m["signed_volume"] > 0 and H.rel_diff(m["signed_volume"], rj["volume_mm3"]) <= 0.01, (m["signed_volume"], rj["volume_mm3"])
    bb = rj["bbox"]
    want = (bb["xmax"] - bb["xmin"], bb["ymax"] - bb["ymin"], bb["zmax"] - bb["zmin"])  # units mm: the STL extent equals the FCStd extent
    assert all(abs(a - b) <= 0.01 * max(b, 1.0) for a, b in zip(H.stl_bbox_size(tris), want)), (H.stl_bbox_size(tris), want)
    assert H.check_tessellation(rj.get("tessellation"), G("fit.c_r")) == []


@H.label("invariant", 4)
def test_E2_checker_controls_unit_cube_and_removed_triangle():
    cube = H.unit_cube_tris()
    m = H.stl_metrics(cube)
    assert m["watertight"] and m["degenerate"] == 0 and m["signed_volume"] == pytest.approx(1.0)  # zero control
    assert not H.stl_metrics(cube[1:])["watertight"]  # known-bad: one triangle removed
    bad = cube + [((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), (2.0, 2.0, 2.0))]
    assert H.stl_metrics(bad)["degenerate"] == 1
    flipped = [(a, c, b) for a, b, c in cube]
    assert H.stl_metrics(flipped)["signed_volume"] < 0
    c_r = G("fit.c_r")
    ok = {"linear_deflection": c_r / 10.0, "angular_deflection_deg": 2.0}
    assert H.check_tessellation(ok, c_r) == []
    assert H.check_tessellation(dict(ok, linear_deflection=c_r), c_r) != [] and H.check_tessellation(dict(ok, angular_deflection_deg=5.0), c_r) != []
    assert H.check_tessellation(None, c_r) != []


# ---------------------------------------------------------------- T1d export chirality
@H.label("discriminator", 10)
@pytest.mark.parametrize("name", ["nut", "receiver"])
def test_T1d_export_chirality_stl_and_step(name):
    pitch, rho = G("thread.pitch"), (G("thread.major") - G("chain.h")) / 2.0
    tris = _stl(name)
    zmid = sum(PITCH_WINDOW[name]) / 2.0
    z0, z90 = (H.ridge_phase(tris, rho, th, pitch, zmid) for th in (0.0, 90.0))
    H.need(z0 is not None and z90 is not None, f"ridge pierce points in the {name} STL")
    assert H.check_chirality(z0, z90, pitch, common.HAND) == []
    s0, s90 = _exports([name])[name]["ridge_theta0_90"]
    assert H.check_chirality(s0, s90, pitch, common.HAND) == []


@H.label("invariant", 4)
def test_T1d_control_mirrored_stl_checker_fires():
    pitch, rho = 8.0, 73.0
    for hand, fires in (("right", False), ("left", True)):
        tris = H.helical_ridge_mesh(pitch, hand, rho_a=70.0, rho_b=76.0)
        z0, z90 = (H.ridge_phase(tris, rho, th, pitch, 16.0) for th in (0.0, 90.0))
        assert (H.check_chirality(z0, z90, pitch, common.HAND) != []) == fires, hand


# ---------------------------------------------------------------- B1 rebuild
@H.label("discriminator", 10)
def test_B1_rebuild_twice_gives_equal_volumes():
    rec = _record()
    assert set(H.FIVE_PARTS) <= set(rec["first"]) and set(COLLETS) <= set(rec["first"])
    for n, v in rec["first"].items():
        assert H.rel_diff(v, rec["second"][n]) <= 1e-6, (n, v, rec["second"][n])


@H.label("invariant", 4)
def test_B1_control_relative_difference():
    assert H.rel_diff(1.0e5, 1.0e5) <= 1e-6  # zero control
    assert H.rel_diff(1.0e5, 1.0e5 * (1 + 1e-5)) > 1e-6  # known-bad: 1e-5 drift fires
    assert H.rel_diff(0.0, 0.0) <= 1e-6


# ---------------------------------------------------------------- X1
X1 = H.ROOT / "independent" / "x1_remeasure.py"


def _x1():
    H.require(X1)
    return json.loads(H.require(H.ROOT / "results" / "x1_remeasure.json").read_text(encoding="utf-8"))


@H.label("discriminator", 10)
def test_X1_independent_remeasure_agrees_with_the_build_side():
    src = H.require(X1).read_text(encoding="utf-8")
    assert not any(w in src for w in ("build_parts", "cad_helpers", "from tests", "import tests", "common.load_params")), "X1 shares code with build or tests"
    x = _x1()
    for n in PRINTABLE:
        assert H.rel_diff(x["volumes"][n], H.result_json(n)["volume_mm3"]) <= 0.005, n  # E1 tolerance
    pitch = G("thread.pitch")
    for k in ("nut_stl", "boss_stl", "nut_step"):
        assert H.check_chirality(x["chirality"][k][0], x["chirality"][k][1], pitch, common.HAND) == [], k
    for key, v in x["interference"].items():  # A1 tolerance: overlap below 0.01 mm3 on every class G and F pair, per the build-side poses
        a, b = key.split("|")
        cls = H.pair_class(H.parse_assembly()[0], a, b, "R")[0]
        assert cls == "C" or v <= H.OVERLAP_TOL, key


@H.label("discriminator", 10)
def test_X1_negative_controls_fire():
    c = _x1()["controls"]
    assert c["away_hits"] is True  # probes away from the feature still hit
    assert c["wrong_expected_fires"] is True  # a deliberately wrong expected value fires
    assert c["mirrored_nut_fires"] is True  # a mirrored nut export fires


# ---------------------------------------------------------------- E3 FCStd opens
@H.label("invariant", 4)
@pytest.mark.parametrize("part", H.FIVE_PARTS)
def test_E3_five_parts_reopen_with_one_named_deliverable(part):
    pr = H.probe("step3_parts", H.part_inputs(*H.FIVE_PARTS))[part]
    rj = H.result_json(part)
    assert len(pr["bodies"]) == 1  # visible deliverable count computed from the document's Body objects
    assert rj["part"] == part and pr["object_count"] > 0


@H.label("discriminator", 10)
@pytest.mark.parametrize("name", COLLETS + ["assembly"])
def test_E3_collets_and_assembly_reopen_with_every_deliverable_named(name):
    if name == "assembly":
        pd = H.probe(f"pose_R_{H.tag(max(FAM))}", H.pose_inputs("R", max(FAM)))
        assert sorted(pd["tree"]) == sorted(H.parts_of(H.parse_assembly()[0])) and pd["visible_count"] == len(pd["tree"])
    else:
        H.require(H.CACHE / f"{name}.FCStd")
        rj = H.result_json(name)
        assert rj["part"] == name and rj["solid_count"] == 1
