"""Step 7 fix pass: good/bad controls for fit_spigot_hole, fit_plate_key_stop_pin, frame_footprint_x, and the WS4 mirror guard (Topologist D1).
Readers use probe JSON and results/assembly_ws4_guard.json only (Rule M)."""
import json

import pytest

import cad_helpers as H
from build_parts import common

G = lambda k: common.get(H.P(), k)
NOM = H.nominal_tag()


def _pd(pose="R"):
    return H.probe(f"pose_{pose}_{NOM}", [H.CACHE / "assembly" / f"pose_{pose}_{NOM}.FCStd"])


@H.label("discriminator", 7)
@pytest.mark.parametrize("key,idx", [("fit_spigot_hole", 1), ("fit_plate_key_stop_pin", 0)])
def test_A3b_fit_measure_passes_its_good_value_and_fires_on_its_bad_control(key, idx):
    ctl = _pd().get("controls", {}).get(key)
    H.need(ctl is not None, f"probe control for {key}")
    chain = G("icd.coaxiality_chain")[idx]
    assert ctl["good"] <= chain + 0.02 and ctl["bad"] > chain + 0.02, (key, ctl, chain)


@H.label("discriminator", 7)
def test_P6b_frame_footprint_x_passes_good_and_fires_on_bad_control():
    ctl = _pd().get("controls", {}).get("frame_footprint_x")
    H.need(ctl is not None, "probe control for frame_footprint_x")
    assert abs(ctl["good"] - G("icd.footprint_x")) <= 0.05 and abs(ctl["bad"] - G("icd.footprint_x")) > 0.05, ctl


@H.label("discriminator", 7)
def test_G2_ws4_mirror_keeps_the_pose_centre_of_mass_and_the_displaced_mirror_does_not():
    g = json.loads(H.require(H.ROOT / "results" / "assembly_ws4_guard.json").read_text(encoding="utf-8"))
    assert g["good_mm"] <= g["tol_mm"] < g["bad_mm"], g
    assert abs(g["com_mirrored"][2] - g["com_pose"][2]) <= g["tol_mm"] and abs(g["com_mirrored"][1] + g["com_pose"][1]) <= g["tol_mm"]


@H.label("discriminator", 7)
def test_G2_ws4_fires_on_handedness_not_on_a_displaced_nut():
    d = H.probe("ws4", [H.CACHE / "assembly" / "ws4.FCStd"])
    assert "T1" in d["fired"], d["fired"]
    assert not any("nut skirt" in r for rs in d["reasons"].values() for r in rs), d["reasons"]


# ---------------------------------------------------------------- common-volume guard (Topologist addendum)
@H.label("discriminator", 7)
def test_common_guard_shifted_partner_reads_its_known_overlap_and_an_invalid_result_raises():
    d = H.probe("common_guard", [H.ROOT / "tests" / "probes" / "probe_common_guard.py"])
    for k in ("boxes", "tubes"):
        assert d[k]["measured"] == pytest.approx(d[k]["expected"], rel=1e-6), (k, d[k])
    assert d["invalid_raises"] is True


@H.label("invariant", 4)
def test_checked_common_raises_on_an_invalid_result_and_passes_a_valid_one():
    import os
    import subprocess
    import sys
    code = ("import os,sys; os.environ['CJ_PROBE_IMPORT']='1'; sys.path.insert(0, r'%s'); sys.path.insert(0, r'%s'); import probe_poses as P\n"
            "class V:\n isValid=lambda s: True\n common=lambda s,o: s\n"
            "class B:\n isValid=lambda s: False\n common=lambda s,o: s\n"
            "P.checked_common(V(), V())\n"
            "try:\n P.checked_common(B(), B()); print('NO_RAISE')\n"
            "except P.InvalidCommon: print('RAISED')\n" % (H.ROOT / "tests" / "probes", H.ROOT))
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=str(H.ROOT))
    assert "RAISED" in r.stdout and "NO_RAISE" not in r.stdout, r.stdout + r.stderr
