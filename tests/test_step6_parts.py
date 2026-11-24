"""Step 6 tests (exploratory build of every part and accessory). Red-first: every discriminator fails with MISSING: or ABSENT FEATURE:
at baseline B6. Reads results/probes/step6_parts.json (probe_step6_parts.py), results/probes/step6_marks.json (probe_step6_marks.py) and
parts_cache/<part>_result.json. Numbers come from params keys named at the assertion; Rule M readings come from probes, not params.
Checklist IDs: see research/quinn/cr_scratch/step6_manager_open.md section 3. Controls (invariant, green_at_4) call the same predicates as the real tests."""
import math
import pathlib
import sys

import pytest

import cad_helpers as H
from build_parts import common

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "probes"))
import glyph_math  # noqa: E402

CACHE = H.CACHE
NEW_IDS = {"base": ("BS1", "BS2", "BS3", "BS4"), "tray": ("BS5", "BS6"), "plug": ("BS6",), "foot": ("BS7",), "tnut": ("FR3",),
           "bracket_purchased": ("FR2",), "bracket_printed": ("FR2",), "frame": ("FR1", "FR4"), "caddy": ("AC1",),
           "gauge": ("AC2",), "rest": ("AC3",), "stop": ("ST1",)}
FLIP_PARTS = ("base",)                      # frame flips per rail member (FR4), see test_frame_members
BOOL_KEYS = ("faces_before", "faces_after")


def K(key):
    try:
        return common.get(H.P(), key)
    except KeyError:
        raise AssertionError(f"MISSING: params key {key}")


def probe6(name, *inputs):
    return H.probe(name, [CACHE / f"{i}.FCStd" for i in inputs])


# ------------------------------------------------------------------ predicates (shared with controls)
def row_errors(rj, ids):
    e = []
    rows = rj.get("features", []) if isinstance(rj, dict) else []
    for i in ids:
        hit = [f for f in rows if f.get("id") == i]
        if not hit:
            e.append(f"ABSENT FEATURE: {i} row in features")
        elif not (hit[0].get("volume_mm3") or 0) > 0:
            e.append(f"{i} volume_mm3 is zero")
        elif not hit[0].get("pass"):
            e.append(f"{i} pass is false")
    return e


def data71_errors(rj, expect_solids=True):
    """Fuse first, boolean once: per-boolean face counts, plain versus optimal bbox, boolean count (llm_plm_cad 7.1)."""
    e = []
    for k in ("booleans", "boolean_count", "bbox_plain", "bbox_optimal", "run_seconds", "euler_VEF"):
        if rj.get(k) is None:
            e.append(f"ABSENT FEATURE: {k} in result JSON")
    if e:
        return e
    if rj["boolean_count"] != len(rj["booleans"]) or not rj["booleans"]:
        e.append("boolean_count differs from the booleans list")
    for b in rj["booleans"]:
        if any(not isinstance(b.get(k), int) for k in BOOL_KEYS):
            e.append(f"ABSENT FEATURE: faces_before/faces_after on boolean {b.get('name')}")
    return e


def fail_first(errs):
    assert not errs, errs[0]


def glyph_errors(g, senses, span_max, tol=0.05):
    """g: probe glyph list. senses: {'tighten': -1, 'loosen': +1}. Each sense present once; spans inside span_max; opposite faces, same wing."""
    e, pick = [], {}
    for name, s in senses.items():
        hit = [x for x in g if x["direction_sign"] == s]
        if len(hit) != 1:
            e.append(f"ABSENT FEATURE: {name} glyph (sense {s:+d}) count {len(hit)}")
        else:
            pick[name] = hit[0]
            if hit[0]["span"] > span_max + tol:
                e.append(f"{name} span {hit[0]['span']:.2f} > {span_max}")
    if len(pick) == 2:
        a, b = pick["tighten"], pick["loosen"]
        if not (a["wing"] == b["wing"] and a["face"][1:] == b["face"][1:] and a["face"][0] != b["face"][0]):
            e.append(f"glyphs not on opposite faces of one wing: {a['wing']}{a['face']} {b['wing']}{b['face']}")
    return e


def witness_reading(tick_low_local_z, under_local_z, skirt_bottom_z, zero_mark_z, gap):
    """Loftsman C1: the reading plane is the nut skirt bottom face (flange underside - nut.skirt_below_flange). Place the holder so its flange
    underside sits `gap` above the rim top; the tick's lowest edge, measured from the underside, lands on skirt_bottom_z + gap; read it against
    the zero graduation (skirt_bottom_z = rim top - nut.skirt_below_flange)."""
    placed_tick = tick_low_local_z - under_local_z + skirt_bottom_z + gap
    return placed_tick - zero_mark_z


def scale_errors(marks, n, pitch, first, tol=0.05):
    """RC6: n graduations at `pitch`, graduation 0 at `first` (rim top - nut.skirt_below_flange, the skirt bottom face at gap 0)."""
    if len(marks) != n:
        return [f"graduation count {len(marks)} vs {n}"]
    e = [f"pitch {b - a:.3f} vs {pitch}" for a, b in zip(marks, marks[1:]) if abs((b - a) - pitch) > tol]
    return e + ([f"graduation 0 at {marks[0]:.3f}, want {first:.3f}"] if abs(marks[0] - first) > tol else [])


def one_rail_notched(fracs, floor):
    """FR4 (Rule P): exactly one rail differs from its flipped copy by more than `floor`."""
    hot = sum(1 for f in fracs if f > floor)
    return [] if hot == 1 and len(fracs) == 2 else [f"{hot} of {len(fracs)} rails carry the slot-line notch (want 1 of 2)"]


LOFTSMAN_KEYS = {"witness": ("index_face_nut_z", "azimuth_deg", "channel_width", "channel_floor_depth", "line_height", "line_depth", "band_depth",
                             "tick_width", "tick_depth", "tick_height"),
                 "nut": ("glyph_length", "shaft_width", "head_width", "head_length", "skirt_r_out", "skirt_z_lo", "skirt_z_hi", "skirt_rim",
                         "skirt_embed", "release_shaft_width", "release_head_width", "release_head_length"),
                 "base": ("slot_centres", "key_pocket_xy", "pin_pocket_xy", "drain_xy", "column_notch", "key_pocket_size", "pocket_depth",
                          "pin_pocket_size", "drain_hole_dia"),
                 "tray": ("wall", "floor_min", "fall_x", "cross_fall_deg", "drain_spot_r", "hole_r", "relief"),
                 "plug": ("head_dia", "head_h", "flange_dia", "flange_t", "shank_dia", "lug_length", "lug_width", "lug_height", "lug_embed"),
                 "foot": ("size", "m6_xy", "m6_hole", "m8_x", "m8_hole"),
                 "tnut": ("body", "neck", "hole"), "frame": ("end_x", "support_x", "notch"),
                 "bracket": ("holes_purchased", "slots_printed"), "caddy": ("web", "border", "floor"), "gauge": ("cavity",),
                 "rest": ("ring", "roller_r", "pin", "mouth_deg", "pose_core_d", "roller_r_range", "core_d_range", "slot_clear", "slot_depth"), "stop": ("pad_thickness", "pad_xy")}


def stock_errors(members, on_hand):
    e, used = [], {}
    stock = {s["length"]: s["qty"] for s in on_hand}
    for m in members:
        if m["cut_mm"] not in stock:
            e.append(f"{m['id']} cut {m['cut_mm']} is not a whole stock piece")
        used[m["cut_mm"]] = used.get(m["cut_mm"], 0) + m["qty"]
    for L_, n in used.items():
        if L_ in stock and n > stock[L_]:
            e.append(f"cut {L_} consumes {n} > on hand {stock[L_]}")
    return e


def count_errors(n_brackets, n_tnuts, n_expect_brackets, per_bracket):
    e = []
    if n_brackets != n_expect_brackets:
        e.append(f"brackets {n_brackets} vs {n_expect_brackets}")
    if n_tnuts != n_brackets * per_bracket:
        e.append(f"T-nuts {n_tnuts} vs {n_brackets * per_bracket}")
    return e


def flange_errors(scan):
    """HD5: every vertical line through the flange top annulus (outside the insert circle) meets one solid interval; a hole shows two or none."""
    bad = [(r, az, n) for r, d in scan.items() for az, n in d.items() if n != 1]
    return [f"hole on flange annulus at r {bad[0][0]} az {bad[0][1]} ({bad[0][2]} intervals)"] if bad else []


def hd6_allowed(h):
    """Allowed downward faces: holder bottom, flange underside, and (Step 7, collar in holder.FCStd) the collar underside at holder top - collar.thickness."""
    out = [h["bbox"][4], h["flange_interval"][0]]
    cu = h.get("collar_underside_z")
    if cu is not None and abs(cu - (h["bbox"][5] - K("collar.thickness"))) <= 0.05:
        out.append(cu)
    return out


def stop_face_errors(down_z, allowed):
    """HD6: downward-facing planar faces of the holder sit only at allowed z (flange underside, holder bottom)."""
    extra = [z for z in down_z if all(abs(z - a) > 0.05 for a in allowed)]
    return [f"extra downward face at z {extra[0]} (hard-stop face)"] if extra else []


# ------------------------------------------------------------------ F5-style per new part
@H.label("discriminator", 6)
@pytest.mark.parametrize("part", [p for p in NEW_IDS if p != "frame"])
def test_F5_new_part_shell_rows_and_71_data(part):
    H.require(CACHE / f"{part}.FCStd")
    rj = H.result_json(part)
    pr = probe6("step6_parts", part)[part]
    assert pr["valid"] and pr["closed"] and pr["solids"] == 1 and pr["shells"] == 1
    assert rj["isValid"] and rj["isClosed"] and rj["solid_count"] == 1
    assert pr["euler_VEF"] == rj["euler_VEF"] and abs(pr["volume"] - rj["volume_mm3"]) <= 0.01 * rj["volume_mm3"]   # key: none (probe vs JSON)
    fail_first(row_errors(rj, NEW_IDS[part]))
    fail_first(data71_errors(rj))
    if part in FLIP_PARTS:
        assert H.check_flip(pr["flip_mismatch_fraction"], H.FLIP_FLOOR) == []   # Rule P: BS3 slot pattern is asymmetric


@H.label("discriminator", 6)
def test_F5_frame_one_solid_per_member_and_bracket_and_flip_of_the_notched_rail():
    H.require(CACHE / "frame.FCStd")
    rj = H.result_json("frame")
    fr = probe6("step6_parts", "frame")["frame"]
    members = K("frame.members")
    assert len(fr["members"]) == sum(m["qty"] for m in members)                       # frame.members qty
    assert all(m["valid"] and m["closed"] and m["solids"] == 1 for m in fr["members"] + fr["brackets"])
    fail_first(row_errors(rj, NEW_IDS["frame"]))
    fail_first(data71_errors(rj))
    rails = [m for m in fr["members"] if m["id"] == "rail"]
    fail_first(one_rail_notched([m["flip_mismatch_fraction"] for m in rails], H.FLIP_FLOOR))   # FR4 datum C notch on one rail only (Rule P)


@H.label("discriminator", 6)
def test_FR1_member_lengths_counts_and_footprint():
    H.require(CACHE / "frame.FCStd")
    fr = probe6("step6_parts", "frame")["frame"]
    for m in K("frame.members"):                                                       # frame.members id, cut_mm, qty
        got = [x for x in fr["members"] if x["id"] == m["id"]]
        assert len(got) == m["qty"], m["id"]
        assert all(abs(x["length"] - m["cut_mm"]) <= 0.05 for x in got), m["id"]
    xmin, xmax, ymin, ymax = fr["bbox"]
    assert abs((xmax - xmin) - K("icd.footprint_x")) <= 0.05 and abs((ymax - ymin) - K("icd.footprint_y")) <= 0.05


@H.label("discriminator", 6)
def test_FR1_stock_allocation_whole_pieces_not_above_quantity_on_hand():
    H.require(CACHE / "frame.FCStd")
    rj = H.result_json("frame")
    H.need("allocation" in rj, "allocation [{id, qty, cut_mm, stock_piece_mm}] in frame result JSON")
    members = K("frame.members")                                                       # frame.members, stock.on_hand
    assert [(a["id"], a["qty"], a["cut_mm"]) for a in rj["allocation"]] == [(m["id"], m["qty"], m["cut_mm"]) for m in members]
    fail_first(stock_errors(rj["allocation"], K("stock.on_hand")))
    assert all(a["stock_piece_mm"] == a["cut_mm"] for a in rj["allocation"])           # whole piece, no remainder


@H.label("discriminator", 6)
def test_FR2_FR3_bracket_and_tnut_counts():
    H.require(CACHE / "frame.FCStd")
    rj = H.result_json("frame")
    fr = probe6("step6_parts", "frame")["frame"]
    # Step 7 C6 option (a): two purchased brackets per outer-corner joint, one printed bracket per support-end joint (12 brackets, 96 T-nuts)
    per_joint = K("hardware.brackets_per_joint")
    n_pur, n_prn = K("hardware.purchased_bracket_joints") * per_joint, K("hardware.printed_bracket_joints") * K("hardware.printed_brackets_per_joint")
    assert [b["kind"] for b in fr["brackets"]].count("purchased") == n_pur == 8
    assert [b["kind"] for b in fr["brackets"]].count("printed") == n_prn == 4
    fail_first(count_errors(len(fr["brackets"]), fr["tnut_instances"], n_pur + n_prn, K("hardware.tnuts_per_bracket")))
    assert K("hardware.purchased_bracket_joints") + K("hardware.printed_bracket_joints") == K("frame.joints")
    assert n_pur + n_prn == 12 and fr["tnut_instances"] == 96
    for k, v in (("bracket_count", n_pur + n_prn), ("tnut_instances", fr["tnut_instances"])):
        H.need(rj.get(k) == v, f"frame result JSON {k} equals the probe count")


# ------------------------------------------------------------------ rebuilt parts
REBUILT_ROWS = (("receiver", "RC6"), ("holder", "HD7"), ("nut", "NT4"), ("nut", "NT5"), ("nut", "NT7"))


@H.label("discriminator", 6)
@pytest.mark.parametrize("part,rid", REBUILT_ROWS, ids=[f"{p}-{i}" for p, i in REBUILT_ROWS])
def test_rebuilt_part_row_present(part, rid):
    fail_first(row_errors(H.result_json(part), (rid,)))


@H.label("discriminator", 6)
@pytest.mark.parametrize("part", ("receiver", "holder", "nut"))
def test_rebuilt_part_f5_stays_green(part):
    pr = probe6("step6_parts", part)[part]
    rj = H.result_json(part)
    assert pr["valid"] and pr["closed"] and pr["solids"] == 1
    assert rj["all_features_pass"] and H.check_flip(pr["flip_mismatch_fraction"], H.FLIP_FLOOR) == []
    assert rj.get("rebuild", {}).get("reason_ids"), "ABSENT FEATURE: rebuild record {before_volume, after_volume, reason_ids} in result JSON"


@H.label("discriminator", 6)
def test_HD5_no_jacking_holes_on_the_flange_annulus():
    fail_first(flange_errors(probe6("step6_parts", "holder")["holder"]["flange_scan"]))   # annulus bounds: holder.insert_circle_radius, insert_dia, flange_od, index_notch_depth


@H.label("discriminator", 6)
def test_HD6_no_hard_stop_face_on_the_holder():
    h = probe6("step6_parts", "holder")["holder"]
    iv = h["flange_interval"]
    allowed = hd6_allowed(h)                                                           # holder bottom, flange underside, collar underside
    fail_first(stop_face_errors(h["down_planar_z"], allowed))


# ------------------------------------------------------------------ nut glyphs
@H.label("discriminator", 6)
def test_NT4_NT5_glyph_sense_span_and_faces():
    g = probe6("step6_marks", "nut")["glyphs"]
    fail_first(glyph_errors(g, {"tighten": -1, "loosen": +1}, K("nut.arrow_length")))     # clockwise tighten, counter-clockwise loosen, <= 21.86


@H.label("discriminator", 6)
def test_NT4_NT5_result_json_glyph_record_matches_probe():
    rj, g = H.result_json("nut"), probe6("step6_marks", "nut")["glyphs"]
    rec = rj.get("glyphs")
    H.need(rec is not None and {"tighten", "loosen"} <= set(rec), "glyphs {tighten, loosen} in nut result JSON")
    for name, s in (("tighten", -1), ("loosen", +1)):
        r = rec[name]
        assert r["direction_sign"] == s and r["radial_span"] <= K("nut.arrow_length") + 0.05
        assert abs(r["radial_span"] - K("nut.glyph_length")) <= 1.5                   # principal span 10.0 modelled; 9.04 measured against the unrecessed face level
        hit = [x for x in g if x["direction_sign"] == s]
        assert hit and f"{hit[0]['wing']}{hit[0]['face']}" == f"{r['wing']}{r['face']}" and abs(hit[0]["span"] - r["radial_span"]) <= 0.5


# ------------------------------------------------------------------ witness
@H.label("discriminator", 6)
def test_RC6_scale_graduation_count_and_pitch():
    assert K("witness.azimuth_deg") == (K("receiver.key_offset_deg") + 90) % 360        # reader faces the ruler 90 deg from the key slot
    w = probe6("step6_marks", "receiver", "holder")["witness"]
    H.need("marks_z" in w, "witness marks in the marks probe " + str(w.get("error", "")))
    n = int(math.floor(K("holder.stroke_gap_R") / K("witness.scale_pitch") + 1e-9)) + 1    # 0 to stroke_gap_R at scale_pitch
    first = w["rim_top_z"] - K("nut.skirt_below_flange")                                # graduation 0 at the skirt bottom face (Loftsman C1)
    fail_first(scale_errors(sorted(w["marks_z"]), n, K("witness.scale_pitch"), first))


@H.label("discriminator", 6)
def test_RC6_zone_and_band_edges_equal_witness_params():
    rec = H.result_json("receiver").get("witness")
    H.need(rec is not None, "witness record {zone, band_low, band_high} in receiver result JSON")
    assert rec["zone"] == [K("holder.stroke_gap_min_K"), K("witness.zone_high")]
    assert rec["band_low"] == K("witness.wrong_collet_band_low") and rec["band_high"] == K("witness.wrong_collet_band_high")


@H.label("discriminator", 6)
@pytest.mark.parametrize("name,gap_key", (("K-max", "holder.stroke_gap_min_K"), ("K d+1", "witness.zone_high")))
def test_HD7_tick_reads_the_zone_edge_at_the_built_pose(name, gap_key):
    w = probe6("step6_marks", "receiver", "holder")["witness"]
    H.need(w.get("tick_local_z") is not None and w.get("marks_z"), "tick and scale marks in the marks probe")
    gap = K(gap_key)                                                                   # 1.5 at K-max, 8.59 at K d+1
    assert w["tick_count"] == 1, w["tick_count"]
    skirt_bottom = w["rim_top_z"] - K("nut.skirt_below_flange")
    got = witness_reading(w["tick_local_z"], w["holder_under_local_z"], skirt_bottom, min(w["marks_z"]), gap)   # tick_local_z = lowest z of the mark
    assert abs(got - gap) <= 0.05, (name, got)


@H.label("discriminator", 6)
def test_loftsman_params_keys_present_before_the_builds():
    absent = [f"{g}.{k}" for g, ks in LOFTSMAN_KEYS.items() for k in ks if not H.has_key(f"{g}.{k}")]
    if absent:
        K(absent[0])                                                                      # raises MISSING: params key <first absent>
    assert not absent


# ------------------------------------------------------------------ stop interface
@H.label("discriminator", 6)
def test_ST1_stop_pad_face_height_owner_and_no_nut_volume():
    H.require(CACHE / "stop.FCStd")
    rj, st = H.result_json("stop"), probe6("step6_parts", "stop", "nut")["stop"]
    assert rj.get("owner") == K("stop.owner") == "upper assembly"
    w, ln = K("stop.pad_width"), K("stop.pad_length")
    hit = [f for f in st["pad_faces"] if abs(f["z"] - K("stop.height_z")) <= 0.05 and sorted((round(f["dx"], 2), round(f["dy"], 2))) == sorted((w, ln))]
    H.need(len(hit) >= 1, "stop pad face at stop.height_z of stop.pad_width x stop.pad_length")
    under = [f for f in st["pad_faces"] if abs(f["z"] - (K("stop.height_z") - K("stop.pad_thickness"))) <= 0.05]
    H.need(len(under) >= 1, "stop pad underside at stop.height_z - stop.pad_thickness")
    assert st["common_with_nut_mm3"] <= H.OVERLAP_TOL
    assert not any(f["feature"].lower().startswith("nut") for f in rj["features"])


# ------------------------------------------------------------------ controls (invariant, green_at_4): each family has a known-bad fixture that fires
def _good_json():
    return {"features": [{"id": i, "feature": i, "volume_mm3": 10.0, "pass": True} for i in ("BS1", "BS2")]}


@H.label("invariant", 4)
def test_control_deleted_feature_row_fires_and_empty_result_fires():
    assert row_errors(_good_json(), ("BS1", "BS2")) == []
    bad = _good_json()
    del bad["features"][1]
    assert row_errors(bad, ("BS1", "BS2"))[0].startswith("ABSENT FEATURE")
    assert row_errors({}, ("BS1",))[0].startswith("ABSENT FEATURE")                    # absent-feature detector on an empty result
    zero = _good_json()
    zero["features"][0]["volume_mm3"] = 0.0
    assert row_errors(zero, ("BS1",))
    assert data71_errors({})[0].startswith("ABSENT FEATURE")


@H.label("invariant", 4)
def test_control_flip_checker_fires_on_a_plain_disc():
    assert H.check_flip(0.0, H.FLIP_FLOOR) != [] and H.check_flip(0.0085, H.FLIP_FLOOR) == []


@H.label("invariant", 4)
def test_control_glyph_wrong_sense_fires_and_right_sense_passes():
    cw = glyph_math.analyze(glyph_math_arrow(+1.0))       # +x wing, +y face, head toward +x: clockwise from +Z
    ccw = glyph_math.analyze(glyph_math_arrow(-1.0))
    assert cw["direction_sign"] == -1 and ccw["direction_sign"] == +1
    pair = lambda t, l: [{"wing": 0, "face": "+y", "span": t["span"], "direction_sign": t["direction_sign"]},
                         {"wing": 0, "face": "-y", "span": l["span"], "direction_sign": l["direction_sign"]}]
    assert glyph_errors(pair(cw, ccw), {"tighten": -1, "loosen": +1}, 21.86) == []
    assert glyph_errors(pair(ccw, ccw), {"tighten": -1, "loosen": +1}, 21.86)           # wrong sense: no clockwise glyph
    assert glyph_errors(pair(cw, ccw), {"tighten": -1, "loosen": +1}, cw["span"] - 1.0)  # span over the limit
    same = [{"wing": 0, "face": "+y", "span": 10.0, "direction_sign": -1}, {"wing": 0, "face": "+y", "span": 10.0, "direction_sign": 1}]
    assert glyph_errors(same, {"tighten": -1, "loosen": +1}, 21.86)                     # same face


def glyph_math_arrow(direction):
    return glyph_math.synthetic_arrow(90.0, 106.0, 20.0) if direction > 0 else glyph_math.synthetic_arrow(106.0, 90.0, 20.0)


@H.label("invariant", 4)
def test_control_tick_off_by_one_mm_fires():
    assert abs(witness_reading(5.0, 4.0, 88.5, 88.5, 1.5) - 2.5) <= 0.05                # tick 1 mm above the underside reads gap + 1
    good = witness_reading(4.0, 4.0, 88.5, 88.5, 8.59)
    assert abs(good - 8.59) <= 0.05
    assert abs(witness_reading(4.0 + 1.0, 4.0, 88.5, 88.5, 8.59) - 8.59) > 0.05          # 1 mm off fails the 0.05 band


@H.label("invariant", 4)
def test_control_scale_reference_and_tick_edge_fire():
    good = [48.5 + k for k in range(14)]
    assert scale_errors(good, 14, 1.0, 48.5) == []
    assert scale_errors([m + 40.0 for m in good], 14, 1.0, 48.5)                          # old rim-top reference fires
    assert scale_errors(good[:-1], 14, 1.0, 48.5) and scale_errors([48.5 + 1.1 * k for k in range(14)], 14, 1.0, 48.5)
    zero = witness_reading(88.0, 88.0, 48.5, 48.5, 1.5)                                   # tick lowest z = underside reads the gap
    assert abs(zero - 1.5) <= 0.05
    assert abs(witness_reading(89.5, 88.0, 48.5, 48.5, 1.5) - 1.5) > 0.05                  # mark-centre reading (3 mm tick) is 1.5 off


@H.label("invariant", 4)
def test_control_member_id_and_rail_flip_detectors_fire():
    assert [glyph_math.member_id(n) for n in ("member_plate_support_1", "member_rail_2", "member_end_1")] == ["plate_support", "rail", "end"]
    assert "member_plate_support_1".split("_")[1] != "plate_support"                       # the old split read "plate"
    assert one_rail_notched([0.0024, 0.0], H.FLIP_FLOOR) == []
    assert one_rail_notched([0.0024, 0.0024], H.FLIP_FLOOR) and one_rail_notched([0.0, 0.0], H.FLIP_FLOOR)


@H.label("invariant", 4)
def test_control_stock_and_count_checks_fire():
    on_hand = [{"length": 644, "qty": 2}, {"length": 488, "qty": 2}]
    assert stock_errors([{"id": "rail", "cut_mm": 644, "qty": 2}], on_hand) == []
    assert stock_errors([{"id": "rail", "cut_mm": 650, "qty": 2}], on_hand)             # not a whole stock piece
    assert stock_errors([{"id": "rail", "cut_mm": 644, "qty": 3}], on_hand)             # above quantity on hand
    assert count_errors(16, 128, 16, 8) == [] and count_errors(16, 127, 16, 8) and count_errors(15, 120, 16, 8)


@H.label("invariant", 4)
def test_control_hd5_hd6_detectors_fire():
    assert flange_errors({"66.00": {"0": 1, "3": 1}}) == [] and flange_errors({"66.00": {"0": 1, "3": 2}})
    assert stop_face_errors([2.0, 10.0], [2.0, 10.0]) == [] and stop_face_errors([2.0, 10.0, 40.0], [2.0, 10.0])


@H.label("invariant", 4)
def test_control_missing_params_key_reports_missing():
    absent = "_".join(("no", "such", "key"))
    with pytest.raises(AssertionError, match="MISSING: params key " + absent):
        K(absent)


# ------------------------------------------------------------------ known-bad controls through the real measurement (probe-built defects)
@H.label("discriminator", 6)
def test_control_hd5_hd6_fire_on_a_holder_with_a_jacking_hole_and_a_hard_stop_shoulder():
    h = probe6("step6_parts", "holder")["holder"]
    c = h.get("controls")
    H.need(c is not None, "holder controls (jacking-hole and shoulder variants) in the parts probe")
    assert flange_errors(h["flange_scan"]) == []                                              # the built holder reads clean through the same window
    assert flange_errors(c["hole"]["flange_scan"])                                            # jacking hole through the annulus fires HD5
    allowed = hd6_allowed(h)
    assert stop_face_errors(h["down_planar_z"], allowed) == []
    assert stop_face_errors(c["shoulder"]["down_planar_z"], allowed)                          # shoulder at holder bottom + 30 fires HD6


@H.label("discriminator", 6)
def test_control_nt4_nt5_fire_on_a_nut_with_the_glyph_window_filled():
    m = probe6("step6_marks", "nut")
    H.need("glyphs_control_filled" in m, "filled-window nut control in the marks probe")
    sense = {"tighten": -1, "loosen": +1}
    assert glyph_errors(m["glyphs"], sense, K("nut.arrow_length")) == []
    assert glyph_errors(m["glyphs_control_filled"], sense, K("nut.arrow_length"))              # no glyph: both senses missing


# ------------------------------------------------------------------ NT8 recess area, witness ray-cast, rest D2
@H.label("discriminator", 6)
def test_NT8_release_arrow_recess_area_equals_NT4_within_10_percent():
    nt8 = [f for f in H.result_json("nut")["features"] if f.get("id") == "NT8" and "recess area" in f["feature"]]
    H.need(nt8, "NT8 recess area row in nut result JSON")
    row = nt8[0]
    assert row["pass"] and row["volume_mm3"] > 0
    assert abs(row["built"] - row["params"]) <= 0.1 * row["params"], (row["built"], row["params"])      # built = NT8 area, params = NT4 area (mm2)


@H.label("invariant", 4)
def test_control_NT8_area_check_fires_on_a_double_width_arrow():
    area_nt4 = 35.41
    assert abs(34.37 - area_nt4) <= 0.1 * area_nt4 and not abs(2 * 34.37 - area_nt4) <= 0.1 * area_nt4


def sight_errors(rec, line_count, edge_tol=0.1):
    e = []
    if rec["edge"] is None or abs(rec["edge"] - rec["expected_edge"]) > edge_tol:
        e.append(f"reading edge {rec['edge']} vs nut z 0 face at {rec['expected_edge']:.3f}")
    if rec["lines_visible"] != line_count:
        e.append(f"{rec['lines_visible']} graduation lines visible, want {line_count}")
    return e


@H.label("discriminator", 6)
@pytest.mark.parametrize("name,count", (("K-max", 2), ("K d+1", 9)))
def test_witness_ray_cast_edge_and_visible_line_count(name, count):
    w = H.probe("witness_sight", [CACHE / "receiver.FCStd", CACHE / "nut.FCStd"])
    assert abs(w["edge_zero"] - (w["rim_top_z"] - K("nut.skirt_below_flange"))) <= 0.05 and K("witness.index_face_nut_z") == 0.0
    fail_first(sight_errors(w["poses"][name], count))


@H.label("discriminator", 6)
def test_control_witness_nut_five_mm_low_fails_the_ray_cast():
    w = H.probe("witness_sight", [CACHE / "receiver.FCStd", CACHE / "nut.FCStd"])
    assert sight_errors(w["poses"]["K-max"], 2) == []
    assert sight_errors(w["control"], 2)                                                  # nut at edge - 5 reads the wrong edge
    assert sight_errors({"edge": 50.0, "expected_edge": 50.0, "lines_visible": 1}, 2)    # wrong line count fires


@H.label("discriminator", 6)
def test_rest_D2_rollers_clear_the_core_at_every_size_and_pin_slots_are_cut():
    rs = probe6("step6_parts", "rest")["rest"]["sizes"]
    lo, hi = K("rest.core_d_range")
    assert [s["core_d"] for s in rs][0] == lo and rs[-1]["core_d"] == hi and len(rs) == 9
    for s in rs:
        assert s["valid"] and s["solids"] == 1, s["core_d"]
        assert s["common_with_core_mm3"] <= H.OVERLAP_TOL, (s["core_d"], s["common_with_core_mm3"])
        assert s["ring_bottom_z_at_slot"] is not None and abs(s["ring_bottom_z_at_slot"] - s["slot_z_expected"]) <= 0.05, s["core_d"]   # pin slot cut: ring material starts slot_depth above the ring bottom


@H.label("discriminator", 6)
def test_control_rest_slot_and_overlap_detectors_fire():
    ok = {"core_d": 100.0, "common_with_core_mm3": 0.0, "ring_bottom_z_at_slot": 18.5, "slot_z_expected": 18.5}
    bad_overlap = dict(ok, common_with_core_mm3=895.0)
    no_slot = dict(ok, ring_bottom_z_at_slot=15.5)                                         # plain ring: bottom at ring_z_lo
    pred = lambda s: s["common_with_core_mm3"] <= H.OVERLAP_TOL and abs(s["ring_bottom_z_at_slot"] - s["slot_z_expected"]) <= 0.05
    assert pred(ok) and not pred(bad_overlap) and not pred(no_slot)
