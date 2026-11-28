"""Control fixtures for K1 to K9 (manifest.yaml). Each builder returns a sketch_common.Ctx or a list of them.

Figures are drawn from check_stack.py values (z_S, shop-floor frame) so a Z fixture is clean by construction;
each B builder plants exactly one defect on top of the matching Z drawing. K6-Z2 and K6-B4 anchor check_stack itself
to hand numbers written in manifest.yaml (LF-2). s1_full_draw draws every S1 spec row (SW-8 smoke control).
"""
import copy
import math
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import check_stack  # noqa: E402
import checks_s1  # noqa: E402
import checks_s2  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params, load_spec  # noqa: E402
from matplotlib.collections import LineCollection  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Annulus, Circle, Polygon, Rectangle  # noqa: E402
from matplotlib.transforms import Affine2D  # noqa: E402

CHECK_STACK_PATH = HERE.parent / "check_stack.py"


def _ctx(P, spec, figs, **kw):
    stack = check_stack.evaluate_spec(P, spec)
    kw.setdefault("check_stack_path", CHECK_STACK_PATH)
    return sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], **kw)


# ---------------------------------------------------------------- mini side spec (K4, K5, K6, K8, K9, ctrl figs)

def mini_side_spec(pose="capture_end", tip="stop.height_z"):
    zr = lambda a, b: {"z_min": a, "z_max": b}  # noqa: E731
    on_axis = lambda w: {"r_in": 0, "theta": 0, "half_width": w, "footprint": "round"}  # noqa: E731
    screw = lambda w: {"r_in": "jackscrew.pitch_radius", "theta": "jackscrew.angle[0]", "half_width": w, "footprint": "round"}  # noqa: E731
    return {
        "sketch": "mini", "view": "side_xz", "z_rule_frame": "z_A",
        "poses": [{"id": pose, "tip_z": tip}],
        "features": [
            {"id": "floor", "name": "shop floor", "kind": "line", "keys": ["jig.datum_a_above_floor", "icd.footprint_x"],
             "z_rule": zr("shop_floor", "shop_floor")},
            {"id": "core_seat", "name": "collet core seat", "kind": "prism", "projection": "rectangle",
             "keys": ["icd.floor_above_datum_a", "collet.core_seat_height", "core.diameter_nominal"],
             "z_rule": zr("receiver_floor", "core_stop")},
            {"id": "core_500", "name": "core", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["core.length_capture", "core.diameter_nominal"], "z_rule": zr("core_stop", "core_stop + core.length_capture"),
             "label": {"text": "core", "key": "core.length_capture", "fmt": ".0f"},
             "sense": [{"pred": "rests_on", "seat": "core_seat", "tol": 0.05}]},
            {"id": "drill_head", "name": "drill head", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["drill.head_od", "drill.head_length"], "z_rule": zr("tip", "head_top"), "place": on_axis("drill.head_od / 2"),
             "label": {"text": "cutter OD ASSUMED", "key": "drill.head_od", "fmt": ".1f"},
             "sense": [{"pred": "below", "of": "gear"}, {"pred": "below", "of": "drill_top_block"}]},
            {"id": "drill_tube", "name": "drill tube", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["drill.tube_od", "drill.length"], "z_rule": zr("head_top", "drill_top"), "place": on_axis("drill.tube_od / 2"),
             "label": {"text": "tube OD", "key": "drill.tube_od", "fmt": ".1f"}},
            {"id": "drill_top_block", "name": "top-end block", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["drill.top_block_od", "drill.top_block_length"], "z_rule": zr("drill_top", "top_block_top"),
             "place": on_axis("drill.top_block_od / 2")},
            {"id": "ring", "name": "ring", "kind": "plate", "projection": "rectangle",
             "keys": ["ring.od", "ring.thickness", "ring.position_above_tip"], "z_rule": zr("ring_bottom", "ring_top")},
            {"id": "gear", "name": "ring gear", "kind": "gear", "axis": "Z", "projection": "trapezoid",
             "keys": ["gear.pitch_diameter", "gear.bore", "gear.face_width"], "z_rule": zr("ring_top", "gear_top"),
             "sense": [{"pred": "mirror_about_axis", "axis": "drill_tube"}, {"pred": "taper", "narrows": "down"}]},
            {"id": "motor23_a", "name": "NEMA 23", "kind": "cylinder", "axis": "X", "projection": "rectangle",
             "keys": ["pinion.motor_body", "pinion.motor_length", "gear.pitch_diameter", "pinion.angle"],
             "z_rule": zr("ring_top", "ring_top + pinion.motor_body"),
             "place": {"r_in": "gear.pitch_diameter / 2", "r_out": "gear.pitch_diameter / 2 + pinion.motor_length",
                       "theta": "pinion.angle[1]", "half_width": "pinion.motor_body / 2", "footprint": "radial"},
             "sense": [{"pred": "above", "of": "ring"}, {"pred": "side", "of": "drill_tube", "sign": -1}]},
            {"id": "screw_a", "name": "jack screw", "kind": "screw", "axis": "Z", "projection": "rectangle",
             "keys": ["jackscrew.anchor_z", "jackscrew.top_guide_z", "jackscrew.nominal", "jackscrew.pitch_radius", "jackscrew.angle"],
             "z_rule": zr("jackscrew.anchor_z", "jackscrew.top_guide_z"), "place": screw("jackscrew.nominal / 2")},
            {"id": "anchor_a", "name": "anchor", "kind": "prism", "projection": "rectangle",
             "keys": ["jackscrew.anchor_z", "jackscrew.anchor_allowance"],
             "z_rule": zr("jackscrew.anchor_z", "jackscrew.anchor_z + jackscrew.anchor_allowance"),
             "place": screw("jackscrew.nut_flange_od / 2"), "sense": [{"pred": "below", "of": "nut_a"}]},
            {"id": "nut_a", "name": "nut", "kind": "prism", "projection": "rectangle",
             "keys": ["jackscrew.nut_length", "jackscrew.nut_flange_od"],
             "z_rule": zr("nut_z - jackscrew.nut_length / 2", "nut_z + jackscrew.nut_length / 2"),
             "place": screw("jackscrew.nut_flange_od / 2"), "sense": [{"pred": "below", "of": "guide_a"}]},
            {"id": "guide_a", "name": "top guide", "kind": "prism", "projection": "rectangle",
             "keys": ["jackscrew.top_guide_z", "jackscrew.guide_allowance"],
             "z_rule": zr("jackscrew.top_guide_z - jackscrew.guide_allowance", "jackscrew.top_guide_z"),
             "place": screw("jackscrew.nut_flange_od / 2")},
            {"id": "guide_member", "name": "anti-rotation member", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["guide.length", "guide.rod_od", "guide.radius", "guide.angle"], "z_rule": zr(0, "guide.length"),
             "place": {"r_in": "guide.radius", "theta": "guide.angle[0]", "half_width": "guide.rod_od / 2", "footprint": "round"}},
        ],
    }


def _x_extents(P, fid, feats):
    g = P.get
    if feats.get(fid, {}).get("place"):
        return tuple(feats[fid]["place"]["x"])
    table = {
        "floor": (-g("icd.footprint_x") / 2, g("icd.footprint_x") / 2),
        "core_seat": (-g("core.diameter_nominal") / 2, g("core.diameter_nominal") / 2),
        "core_500": (-g("core.diameter_nominal") / 2, g("core.diameter_nominal") / 2),
        "core_750": (-g("core.diameter_nominal") / 2, g("core.diameter_nominal") / 2),
        "ring": (-g("ring.od") / 2, g("ring.od") / 2),
    }
    return table[fid]


def draw_mini(P, spec, stack, mutate=None, title=None, labels=True, gear=None):
    """Draw the mini side spec at its single pose. mutate(fid, x0, x1, z0, z1) -> (x0, x1, z0, z1) or None to skip.
    gear(ax, fid, r_in, r_pitch, z0, z1) replaces draw_gear_section."""
    pose = spec["poses"][0]["id"]
    feats = stack["poses"][pose]["features"]
    fig, ax = sc.setup_figure(spec["view"], title=title or f"mini pose {pose}")
    for row in spec["features"]:
        fid = row["id"]
        z0, z1 = feats[fid]["z_min"], feats[fid]["z_max"]
        if row["kind"] == "gear":
            (gear or sc.draw_gear_section)(ax, fid, P.get("gear.bore") / 2, P.get("gear.pitch_diameter") / 2, z0, z1)
            continue
        x0, x1 = _x_extents(P, fid, feats)
        if mutate is not None:
            out = mutate(fid, x0, x1, z0, z1)
            if out is None:
                continue
            x0, x1, z0, z1 = out
        if row["kind"] == "line":
            sc.draw_hline(ax, fid, x0, x1, z0)
        else:
            sc.draw_rect(ax, fid, x0, x1, z0, z1)
    if labels:
        sc.place_labels(ax, spec, P)
    sc.finish_axes(ax)
    return {pose: fig}


def mini_ctx(mutate=None, label_override=None, extra=None, title=None, labels=True, gear=None, spec=None):
    P = Params()
    spec = spec or mini_side_spec()
    if label_override:
        for row in spec["features"]:
            if row["id"] in label_override:
                row["label_text_override"] = label_override[row["id"]]
    stack = check_stack.evaluate_spec(P, spec)
    figs = draw_mini(P, spec, stack, mutate=mutate, title=title, labels=labels, gear=gear)
    if extra:
        for fig in figs.values():
            extra(fig.axes[0])
    return _ctx(P, spec, figs)


# ---------------------------------------------------------------- K1

def k1_z():
    return sc.Ctx(script_paths=[HERE / "k1_z_clean.py"])


def k1_b1():
    return sc.Ctx(script_paths=[HERE / "k1_b1_literal.py"])


def k1_b2():
    return sc.Ctx(script_paths=[HERE / "k1_b2_softkey.py"])


# ---------------------------------------------------------------- K2

def _k2(overlay):
    P = Params(overlay_path=HERE / overlay)
    spec = sc.load_yaml(HERE / "k2_spec.yaml")
    return sc.Ctx(P=P, spec=spec, overlay_path=HERE / overlay)


def k2_z():
    return _k2("k2_z_overlay.yaml")


def k2_b1():
    return _k2("k2_b1_overlay.yaml")


def k2_b2():
    return _k2("k2_b2_overlay.yaml")


def k2_b3():
    return _k2("k2_b3_overlay.yaml")


# ---------------------------------------------------------------- K3

def _k3(mut=None):
    fig, ax = sc.setup_figure("side_xz", title="k3 fixture")
    sc.draw_rect(ax, "drill_tube", -1, 1, 0, 2)
    if mut:
        mut(fig, ax)
    return sc.Ctx(figs={"fixture": fig}, view="side_xz")


def k3_z():
    return _k3()


def k3_b1():
    return _k3(lambda f, a: a.set_title("k3 fixture pose start"))


def k3_b2():
    return _k3(lambda f, a: a.set_xlabel("x"))


def k3_b3():
    return _k3(lambda f, a: a.set_aspect("auto"))


def k3_b4():
    return _k3(lambda f, a: a.grid(False, which="minor"))


def k3_b5():
    return _k3(lambda f, a: f.set_size_inches(6.4, 4.8))


def k3_b6():
    return _k3(lambda f, a: f.set_dpi(100))


def k3_b7():
    """TP-7: an inset Axes the spec does not declare."""
    return _k3(lambda f, a: f.add_axes([0.6, 0.6, 0.25, 0.25]))


# ---------------------------------------------------------------- K4

def k4_z():
    return mini_ctx()


def k4_b1():
    return mini_ctx(label_override={"drill_tube": "tube OD"})


def k4_b2():
    return mini_ctx(label_override={"drill_tube": "tube OD 150"})


def k4_b3():
    """SW-3: two rows share label text 'core'; the two annotations are swapped onto the wrong parts."""
    P = Params()
    spec = mini_side_spec()
    rows = [r for r in spec["features"] if r["id"] in ("floor", "core_seat", "core_500")]
    rows.append({"id": "core_750", "name": "core", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
                 "keys": ["core.length_install", "core.diameter_nominal"],
                 "z_rule": {"z_min": "core_stop", "z_max": "core_stop + core.length_install"},
                 "label": {"text": "core", "key": "core.length_install", "fmt": ".0f"}})
    spec["features"] = rows
    stack = check_stack.evaluate_spec(P, spec)
    figs = draw_mini(P, spec, stack)
    ax = list(figs.values())[0].axes[0]
    anns = {t.get_gid(): t for t in ax.texts}
    a, b = anns["label:core_500"], anns["label:core_750"]
    ta, tb = a.get_text(), b.get_text()
    a.set_text(tb)
    b.set_text(ta)
    return _ctx(P, spec, figs)


# ---------------------------------------------------------------- K5

def _k5_side_spec():
    return {"sketch": "k5", "view": "side_xz", "poses": [{"id": "fixture", "tip_z": 0}],
            "features": [
                {"id": "drill_tube", "name": "drill tube", "kind": "cylinder", "axis": "Z", "projection": "rectangle", "keys": ["drill.tube_od"]},
                {"id": "pinion_a", "name": "bevel pinion", "kind": "gear", "axis": "X", "projection": "trapezoid", "keys": ["gear.face_width"]},
            ]}


def _k5_plan_spec():
    return {"sketch": "k5", "view": "plan_xy", "poses": [{"id": "fixture", "tip_z": 0}],
            "features": [{"id": "drill_tube", "name": "drill tube", "kind": "cylinder", "axis": "Z", "projection": "circle", "keys": ["drill.tube_od"]}]}


def _k5_side(tube="rect", pinion="trap", untagged=False, spec=None):
    P = Params()
    spec = spec or _k5_side_spec()
    fig, ax = sc.setup_figure("side_xz", title="k5 fixture")
    r = P.get("drill.tube_od") / 2
    if tube == "rect":
        sc.draw_rect(ax, "drill_tube", -r, r, 0, P.get("drill.length"))
    else:
        sc.draw(ax=ax, feature_id="drill_tube", artist=Circle((0, r), r))
    fw = P.get("gear.face_width")
    if pinion == "trap":
        sc.draw_trap(ax, "pinion_a", r + fw, r + fw + fw, fw, fw / 2, 0)
    else:
        sc.draw_rect(ax, "pinion_a", r + fw, r + 2 * fw, 0, fw)
    if untagged:
        ax.add_patch(Rectangle((-r, -fw), r, fw))
    sc.finish_axes(ax)
    return _ctx(P, spec, {"fixture": fig})


def _k5_plan():
    P = Params()
    spec = _k5_plan_spec()
    fig, ax = sc.setup_figure("plan_xy", title="k5 fixture")
    sc.draw(ax=ax, feature_id="drill_tube", artist=Circle((0, 0), P.get("drill.tube_od") / 2))
    sc.finish_axes(ax)
    return _ctx(P, spec, {"fixture": fig})


def k5_z():
    return [_k5_side(), _k5_plan(), mini_ctx()]


def k5_b1():
    return _k5_side(tube="circle")


def k5_b2():
    return _k5_side(pinion="rect")


def k5_b3():
    return _k5_side(untagged=True)


def k5_b4():
    """TP-6: nut_a (prism, projection rectangle) drawn as a 64-vertex circle polygon."""
    P = Params()

    def extra(ax):
        st = check_stack.evaluate_spec(P, mini_side_spec())["poses"]["capture_end"]["features"]["nut_a"]
        cx = st["place"]["r_c"] * check_stack.cosd(st["place"]["theta"])
        cz, rr = (st["z_min"] + st["z_max"]) / 2, (st["z_max"] - st["z_min"]) / 2
        n = 64
        pts = [(cx + rr * math.cos(2 * math.pi * i / n), cz + rr * math.sin(2 * math.pi * i / n)) for i in range(n)]
        sc.draw("nut_a", Polygon(pts, closed=True, fill=False), ax)
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: None if f == "nut_a" else (x0, x1, z0, z1), extra=extra)


def k5_b5():
    """TP-6: cylinder row with no axis (spec lint)."""
    spec = _k5_side_spec()
    spec["features"][0]["axis"] = None
    return _k5_side(spec=spec)


# ---------------------------------------------------------------- K6

DRILL = ("drill_head", "drill_tube", "drill_top_block")


def k6_z():
    return mini_ctx()


def k6_z2():
    """LF-2: live check_stack against the manifest hand numbers (run_control sets ctx.anchors)."""
    return mini_ctx()


def k6_b1():
    dz = Params().get("collar.top_above_plate")
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: (x0, x1, z0 + dz, z1 + dz) if f in DRILL else (x0, x1, z0, z1))


def k6_b2():
    dz = Params().get("jig.datum_a_above_floor")
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: (x0, x1, z0 - dz, z1 - dz) if f == "core_500" else (x0, x1, z0, z1))


def k6_b2b():
    P = Params()
    dz = P.get("jig.datum_a_above_floor") + P.get("icd.floor_above_datum_a")
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: (x0, x1, z0 - dz, z1 - dz) if f == "core_500" else (x0, x1, z0, z1))


def k6_b3():
    c = mini_ctx()
    c.check_stack_path = HERE / "k6_b3_check_stack.py"
    return c


def k6_b4():
    """LF-2: a scratch copy of check_stack with the sign of to_shop_floor flipped; the figures stay drawn from the live
    stack, so only the anchors can see it."""
    src = CHECK_STACK_PATH.read_text(encoding="utf-8")
    good = 'return z_A + P.get("jig.datum_a_above_floor")'
    if good not in src:
        raise RuntimeError("k6_b4: to_shop_floor body not found in check_stack.py")
    d = Path(tempfile.mkdtemp(prefix="k6_b4_"))
    p = d / "check_stack_signflip.py"
    p.write_text(src.replace(good, 'return z_A - P.get("jig.datum_a_above_floor")'), encoding="utf-8")
    c = mini_ctx()
    c.check_stack_path = p
    return c


def _lf16(load_plane=None, field="load_plane"):
    """LF-16: the live S1 spec and its stack, no figures (the lint reads spec rows' stack z, so it holds on the stub)."""
    P = Params()
    spec = load_spec(HERE.parent / "s1_spec.yaml")
    if load_plane is not None:
        spec[field] = load_plane
    stack = check_stack.evaluate_spec(P, spec)
    return sc.Ctx(P=P, spec=spec, figs={}, stack=stack, view=spec["view"], check_stack_path=CHECK_STACK_PATH)


def k6_z3():
    """LF-16 Z: live spec; load_plane (core stop) and entry_plane (collar top) each agree with their feature edge."""
    return _lf16()


def k6_b5():
    """LF-16 B: load_plane term core_stop (42.5 z_A) with feature wingnut, edge z_max, offset collar.top_above_plate,
    the collar-top plane (159.84 z_A), 117.34 apart."""
    return _lf16({"term": "core_stop", "feature": "wingnut", "edge": "z_max", "offset": "collar.top_above_plate"})


def k6_b6():
    """LF-16 B on the second field (Loftsman NOTE 1): entry_plane term collar_top (159.84 z_A) with feature core_seat,
    edge z_max, offset 0 (the core-stop plane, 42.50 z_A), 117.34 apart."""
    return _lf16({"term": "collar_top", "feature": "core_seat", "edge": "z_max", "offset": 0}, field="entry_plane")


# ---------------------------------------------------------------- K7

def _k7(rows, poses, draw_fn, view="side_xz", **spec_extra):
    P = Params()
    spec = {"sketch": "k7", "view": view, "poses": poses, "features": rows, **spec_extra}
    figs = {}
    for p in poses:
        fig, ax = sc.setup_figure(view, title=f"k7 fixture {p['id']}")
        draw_fn(ax, p["id"])
        sc.finish_axes(ax)
        figs[p["id"]] = fig
    return _ctx(P, spec, figs)


def _pair(cls, g_min=0, a="a", b="b", depth_a=(0, 10), depth_b=(0, 10)):
    return [{"id": a, "name": a, "kind": "prism", "projection": "rectangle", "depth": list(depth_a),
             "neighbours": [{"id": b, "class": cls, "g_min": g_min, "source": "fixture"}]},
            {"id": b, "name": b, "kind": "prism", "projection": "rectangle", "depth": list(depth_b)}]


ONE = [{"id": "fixture", "tip_z": 0}]
TWO = [{"id": "p1", "tip_z": 0}, {"id": "p2", "tip_z": 300}]
FOUR = [{"id": "p1", "tip_z": 0}, {"id": "p2", "tip_z": 150}, {"id": "p3", "tip_z": 450}, {"id": "p4", "tip_z": 500}]


def k7_z1():
    return _k7(_pair("F"), ONE, lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 200, 300, 0, 100)))


def k7_z2():
    return _k7(_pair("F", depth_a=(0, 10), depth_b=(20, 30)), ONE,
               lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 50, 150, 0, 100)))


def k7_z3():
    return _k7(_pair("C"), ONE, lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 100, 200, 0, 100)))


def _swept(member_z):
    rows = [{"id": "ring", "name": "ring", "kind": "plate", "projection": "rectangle", "moves": True, "depth": [-210, 210],
             "neighbours": [{"id": "member", "class": "G", "g_min": 10, "source": "fixture"}]},
            {"id": "member", "name": "fixed member", "kind": "prism", "projection": "rectangle", "depth": [-30, 30]}]
    tips = {p["id"]: p["tip_z"] for p in FOUR}

    def draw(ax, pid):
        z = tips[pid] + 100
        sc.draw_rect(ax, "ring", -210, 210, z, z + 20)
        sc.draw_rect(ax, "member", -100, 100, member_z, member_z + 10)
    return _k7(rows, FOUR, draw)


def k7_z4():
    return _swept(700)


def _plan_swept(member_z):
    """SW-6: plan view, ring outline moves with the tip (z band from the stack), fixed member inside the outline in XY."""
    rows = [{"id": "ring", "name": "ring", "kind": "plate", "projection": "rectangle", "moves": True,
             "z_rule": {"z_min": "tip + 100", "z_max": "tip + 120"},
             "neighbours": [{"id": "member", "class": "G", "g_min": 10, "source": "fixture"}]},
            {"id": "member", "name": "fixed member", "kind": "prism", "projection": "rectangle",
             "z_rule": {"z_min": member_z, "z_max": member_z + 10}}]

    def draw(ax, pid):
        sc.draw_rect(ax, "ring", -210, 210, -210, 210)
        sc.draw_rect(ax, "member", -100, 100, -5, 5)
    return _k7(rows, FOUR, draw, view="plan_xy")


def k7_z5():
    return _plan_swept(700)


def k7_z6():
    """LF-3: ring drawn as two halves either side of a fixed post through the bore; clearance 80 at every pose."""
    rows = [{"id": "ring", "name": "ring", "kind": "plate", "projection": "rectangle", "moves": True, "depth": [-210, 210],
             "neighbours": [{"id": "post", "class": "G", "g_min": 10, "source": "fixture"}]},
            {"id": "post", "name": "fixed post", "kind": "prism", "projection": "rectangle", "depth": [-20, 20]}]
    tips = {p["id"]: p["tip_z"] for p in FOUR}

    def draw(ax, pid):
        z = tips[pid] + 100
        sc.draw_rect(ax, "ring", -210, -100, z, z + 20)
        sc.draw_rect(ax, "ring", 100, 210, z, z + 20)
        sc.draw_rect(ax, "post", -20, 20, 0, 800)
    return _k7(rows, FOUR, draw)


def k7_z7():
    """TP-5: a declared nested pair (class N) overlaps; a third part clears both; undeclared pairs default to F."""
    rows = [{"id": "a", "name": "a", "kind": "prism", "projection": "rectangle", "depth": [0, 10],
             "neighbours": [{"id": "b", "class": "N", "source": "fixture: b sits inside a"}]},
            {"id": "b", "name": "b", "kind": "prism", "projection": "rectangle", "depth": [0, 10]},
            {"id": "c", "name": "c", "kind": "prism", "projection": "rectangle", "depth": [0, 10]}]
    return _k7(rows, ONE, lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 20, 80, 20, 80),
                                         sc.draw_rect(ax, "c", 200, 300, 0, 100)))


def k7_b1():
    rows = _pair("C", a="a", b="b") + _pair("G", 0, a="c", b="d") + _pair("F", a="e", b="f")

    def draw(ax, p):
        for i, (a, b) in enumerate((("a", "b"), ("c", "d"), ("e", "f"))):
            z = 200 * i
            sc.draw_rect(ax, a, 0, 100, z, z + 100)
            sc.draw_rect(ax, b, 99, 199, z, z + 100)
    return _k7(rows, ONE, draw)


def k7_b2():
    return _k7(_pair("C"), ONE, lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 101, 201, 0, 100)))


def k7_b3():
    return _k7(_pair("G", 10), ONE, lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 109, 209, 0, 100)))


def k7_b4():
    return _swept(400)


def k7_b31():
    """Loftsman 1.2 (c) FIX LF-c1, side branch: the K7-B4 member (mid-stroke, inside the ring outline, clear of all four
    poses) declared G 10 against the ring at p4 only; swept as undeclared F, it fires."""
    c = _swept(400)
    c.spec["features"][0]["neighbours"][0]["poses"] = ["p4"]
    return c


def k7_b5():
    """LF-1: a C pair touching in XZ with depth bands 490 mm apart."""
    return _k7(_pair("C", depth_a=(0, 10), depth_b=(500, 510)), ONE,
               lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 100, 200, 0, 100)))


def k7_b6():
    """LF-1: a G pair, g_min 10, depth bands 1 mm apart, overlapping in XZ."""
    return _k7(_pair("G", 10, depth_a=(0, 10), depth_b=(11, 21)), ONE,
               lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 50, 150, 0, 100)))


def k7_b7():
    """TP-4 / LF-5: motor at 210 deg with the Wave 1b point band (outer end +/- body / 2); a post depth-separated from
    that band and inside the true projection [-125.2, -37.8]."""
    rows = [{"id": "motor", "name": "motor", "kind": "cylinder", "axis": "X", "projection": "rectangle",
             "place": {"r_in": "gear.pitch_diameter / 2", "r_out": "gear.pitch_diameter / 2 + pinion.motor_length",
                       "theta": "pinion.angle[1]", "half_width": "pinion.motor_body / 2", "footprint": "radial"},
             "depth": ["(gear.pitch_diameter / 2 + pinion.motor_length) * sind(pinion.angle[1]) - pinion.motor_body / 2",
                       "(gear.pitch_diameter / 2 + pinion.motor_length) * sind(pinion.angle[1]) + pinion.motor_body / 2"],
             "neighbours": [{"id": "post", "class": "F", "source": "fixture"}]},
            {"id": "post", "name": "post", "kind": "prism", "projection": "rectangle", "depth": [-60, -45]}]

    def draw(ax, p):
        sc.draw_rect(ax, "motor", -190, -110, 0, 57)
        sc.draw_rect(ax, "post", -150, -140, -50, 200)
    return _k7(rows, ONE, draw)


def k7_b8():
    return _plan_swept(400)


def k7_b9():
    """LF-4: an L-shaped fixed member (non-convex) against a moving part, two poses: static twice, swept once."""
    rows = [{"id": "ring", "name": "ring", "kind": "plate", "projection": "rectangle", "moves": True, "depth": [-50, 50],
             "neighbours": [{"id": "lmember", "class": "G", "g_min": 10, "source": "fixture"}]},
            {"id": "lmember", "name": "L member", "kind": "prism", "projection": "polygon", "depth": [-50, 50]}]
    tips = {p["id"]: p["tip_z"] for p in TWO}

    def draw(ax, pid):
        z = tips[pid]
        sc.draw_rect(ax, "ring", -50, 50, z, z + 20)
        sc.draw("lmember", Polygon([(200, 0), (300, 0), (300, 10), (210, 10), (210, 100), (200, 100)], closed=True, fill=False), ax)
    return _k7(rows, TWO, draw)


def _plan_pair(cls, g_min, w_b):
    """LF-8 at 1.1 (b): a round part on the axis (radius 126.32, gear-like) and a round part at r 160, theta 150
    (radius w_b, guide-block-like). Both drawn as boxes from their placed x extents over one z band, so they overlap
    in XZ and their depth bands overlap; only the plan footprints separate them (plan gap 160 - 126.32 - w_b)."""
    rows = [{"id": "a", "name": "a", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "place": {"r_in": 0, "theta": 0, "half_width": 126.32, "footprint": "round"},
             "neighbours": [{"id": "b", "class": cls, "g_min": g_min, "source": "fixture"}] if cls else []},
            {"id": "b", "name": "b", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "place": {"r_in": 160, "theta": 150, "half_width": w_b, "footprint": "round"}}]
    P = Params()
    spec = {"sketch": "k7", "view": "side_xz", "poses": ONE, "features": rows}
    stack = check_stack.evaluate_spec(P, spec)
    f = stack["poses"]["fixture"]["features"]
    fig, ax = sc.setup_figure("side_xz", title="k7 fixture plan pair")
    for fid in ("a", "b"):
        x0, x1 = f[fid]["place"]["x"]
        sc.draw_rect(ax, fid, x0, x1, 0, 100)
    sc.finish_axes(ax)
    return _ctx(P, spec, {"fixture": fig})


def k7_z8():
    """Declared G 10 pair, plan footprints 11 mm apart, overlapping in XZ and in depth: plan-separated."""
    return _plan_pair("G", 10, 160 - 126.32 - 11)


def k7_z9():
    """Undeclared pair (F), plan footprints 11 mm apart, overlapping in XZ and in depth: plan-separated."""
    return _plan_pair(None, 0, 160 - 126.32 - 11)


def k7_b11():
    """Declared G 10 pair, plan footprints 9 mm apart (g_min - 1), overlapping in XZ and in depth."""
    return _plan_pair("G", 10, 160 - 126.32 - 9)


def k7_b10():
    """TP-5: two parts with no declared relation overlap."""
    rows = [{"id": "a", "name": "a", "kind": "prism", "projection": "rectangle", "depth": [0, 10]},
            {"id": "b", "name": "b", "kind": "prism", "projection": "rectangle", "depth": [0, 10]}]
    return _k7(rows, ONE, lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 50, 150, 0, 100)))


# ---------------------------------------------------------------- K8

def _flip_drill(P, stack, pose):
    f = stack["poses"][pose]["features"]
    lo, hi = f["drill_head"]["z_min"], f["drill_top_block"]["z_max"]

    def mut(fid, x0, x1, z0, z1):
        if fid in DRILL:
            return x0, x1, lo + hi - z1, lo + hi - z0
        return x0, x1, z0, z1
    return mut


def plan_spec():
    rows = [{"id": "drill_tube", "name": "drill tube", "kind": "cylinder", "axis": "Z", "projection": "circle", "keys": ["drill.tube_od"]}]
    for i, s in enumerate("abc"):
        rows.append({"id": f"screw_{s}", "name": "jack screw", "kind": "screw", "axis": "Z", "projection": "circle",
                     "keys": ["jackscrew.pitch_radius", "jackscrew.angle", "jackscrew.nominal"],
                     "sense": [{"pred": "azimuth", "expr": f"jackscrew.angle[{i}]", "tol_deg": 0.1}]})
    return {"sketch": "mini_plan", "view": "plan_xy", "poses": [{"id": "plan", "tip_z": 0}], "features": rows}


def plan_ctx(invert_y=False, angle_index=None):
    P = Params()
    spec = plan_spec()
    fig, ax = sc.setup_figure("plan_xy", title="mini plan")
    sc.draw(ax=ax, feature_id="drill_tube", artist=Circle((0, 0), P.get("drill.tube_od") / 2))
    r = P.get("jackscrew.pitch_radius")
    for i, s in enumerate("abc"):
        th = P.get("jackscrew.angle")[(angle_index or {}).get(s, i)]
        sc.draw(ax=ax, feature_id=f"screw_{s}",
                artist=Circle((r * check_stack.cosd(th), r * check_stack.sind(th)), P.get("jackscrew.nominal") / 2))
    sc.finish_axes(ax)
    if invert_y:
        ax.invert_yaxis()
    return _ctx(P, spec, {"plan": fig})


def _taper_spec():
    """TP-2 ruling (gameplan Design Notes 22): the collet outer cone narrows upward."""
    return {"sketch": "taper", "view": "side_xz", "poses": [{"id": "fixture", "tip_z": 0}],
            "features": [{"id": "collet", "name": "collet", "kind": "cone", "axis": "Z", "projection": "trapezoid",
                          "keys": ["cone.alpha"], "sense": [{"pred": "taper", "narrows": "up"}]}]}


def taper_ctx(invert=False):
    P = Params()
    fig, ax = sc.setup_figure("side_xz", title="taper fixture")
    R, h = P.get("receiver.register_bore_radius"), P.get("collet.slit_length")
    t = h * math.tan(math.radians(P.get("cone.alpha")))
    z_narrow, z_wide = (0, h) if invert else (h, 0)
    sc.draw("collet", Polygon([(-R + t, z_narrow), (R - t, z_narrow), (R, z_wide), (-R, z_wide)], closed=True, fill=False), ax)
    sc.finish_axes(ax)
    return _ctx(P, _taper_spec(), {"fixture": fig})


def k8_z():
    return [mini_ctx(), plan_ctx(), taper_ctx()]


def k8_b1():
    P = Params()
    spec = mini_side_spec()
    stack = check_stack.evaluate_spec(P, spec)
    return mini_ctx(mutate=_flip_drill(P, stack, spec["poses"][0]["id"]))


def k8_b2():
    P = Params()
    spec = mini_side_spec()
    stack = check_stack.evaluate_spec(P, spec)
    nut = stack["poses"][spec["poses"][0]["id"]]["features"]["nut_a"]
    lift = nut["z_max"] + P.get("jackscrew.nut_length")

    def mut(fid, x0, x1, z0, z1):
        if fid == "anchor_a":
            return x0, x1, lift, lift + (z1 - z0)
        return x0, x1, z0, z1
    return mini_ctx(mutate=mut)


def k8_b3():
    return plan_ctx(invert_y=True)


def k8_b4():
    """SW-4: core_500 lifted 1 mm off the core seat (rests_on)."""
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: (x0, x1, z0 + 1, z1 + 1) if f == "core_500" else (x0, x1, z0, z1))


def k8_z2():
    """TP-9: the K8-B4 defect (core 1 mm off its seat) under a rests_on predicate restricted to another pose reads clean."""
    spec = mini_side_spec()
    for r in spec["features"]:
        if r["id"] == "core_500":
            r["sense"] = [{"pred": "rests_on", "seat": "core_seat", "tol": 0.05, "poses": ["park"]}]
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: (x0, x1, z0 + 1, z1 + 1) if f == "core_500" else (x0, x1, z0, z1), spec=spec)


def k8_b5():
    """SW-4: one gear section piece shifted 1 mm in x (mirror_about_axis)."""
    def gear(ax, fid, r_in, r_pitch, z0, z1):
        right, left = sc.draw_gear_section(ax, fid, r_in, r_pitch, z0, z1)
        left.set_xy([(x + 1, z) for x, z in left.get_xy()])
    return mini_ctx(gear=gear)


def k8_b6():
    """SW-4: plan view, screw_b drawn at jackscrew.angle[2] (azimuth)."""
    return plan_ctx(angle_index={"b": 2})


def k8_b7():
    """SW-5 / TP-3: motor23_a mirrored to the far side of the drill axis (side, projected_x)."""
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: (-x1, -x0, z0, z1) if f == "motor23_a" else (x0, x1, z0, z1))


def k8_b8():
    """TP-1: drill rows at their stack coordinates, flipped tip-up by the artist transform only."""
    P = Params()
    spec = mini_side_spec()
    stack = check_stack.evaluate_spec(P, spec)
    f = stack["poses"]["capture_end"]["features"]
    lo, hi = f["drill_head"]["z_min"], f["drill_top_block"]["z_max"]

    def extra(ax):
        T = Affine2D().scale(1, -1).translate(0, lo + hi) + ax.transData
        for fid in DRILL:
            x0, x1 = f[fid]["place"]["x"]
            sc.draw(fid, Rectangle((x0, f[fid]["z_min"]), x1 - x0, f[fid]["z_max"] - f[fid]["z_min"], fill=False, transform=T), ax)
    return mini_ctx(mutate=lambda fid, x0, x1, z0, z1: None if fid in DRILL else (x0, x1, z0, z1), extra=extra)


def k8_b9():
    """SW-1: the mini spec written as YAML with `on: core_seat`; PyYAML reads the key as True."""
    text = yaml.safe_dump(mini_side_spec(), sort_keys=False).replace("seat: core_seat", "on: core_seat")
    spec = yaml.safe_load(text)
    return mini_ctx(spec=spec)


def k8_b10():
    """TP-2: gear section drawn teeth-up (the Step 1.0 draft sense): wide face at the bottom, narrowing upward."""
    def gear(ax, fid, r_in, r_pitch, z0, z1):
        h = z1 - z0
        right = [(r_in, z0), (r_pitch + h / 2, z0), (r_pitch, z1), (r_in, z1)]
        sc.draw(fid, Polygon(right, closed=True, fill=False), ax)
        sc.draw(fid, Polygon([(-x, z) for x, z in right], closed=True, fill=False), ax)
    return mini_ctx(gear=gear)


def k8_b11():
    """TP-2: collet cone inverted."""
    return taper_ctx(invert=True)


def _ring_on_tube(shift=None):
    """TP-9 ring_on_tube (Designer 1.1 (a) section 6): bearing clears_above drill_head, gear top_within drill_tube.
    shift: {fid: dz} moves one drawn row (the planted defect); the stack is unchanged."""
    P = Params()
    on_axis = lambda w: {"r_in": 0, "theta": 0, "half_width": w, "footprint": "round"}  # noqa: E731
    zr = lambda a, b: {"z_min": a, "z_max": b}  # noqa: E731
    rows = [
        {"id": "drill_head", "name": "drill head", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
         "keys": ["drill.head_od", "drill.head_length"], "z_rule": zr("tip", "head_top"), "place": on_axis("drill.head_od / 2")},
        {"id": "drill_tube", "name": "drill tube", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
         "keys": ["drill.tube_od"], "z_rule": zr("head_top", "drill_top"), "place": on_axis("drill.tube_od / 2")},
        {"id": "bearing", "name": "bearing", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
         "keys": ["bearing.height", "bearing.od"], "z_rule": zr("ring_top - bearing.height", "ring_top"),
         "sense": [{"pred": "clears_above", "of": "drill_head"}]},
        {"id": "gear", "name": "ring gear", "kind": "gear", "axis": "Z", "projection": "trapezoid",
         "keys": ["gear.bore", "gear.pitch_diameter"], "z_rule": zr("ring_top", "gear_top"),
         "sense": [{"pred": "top_within", "of": "drill_tube"}]},
    ]
    spec = {"sketch": "ring_on_tube", "view": "side_xz", "poses": [{"id": "capture_end", "tip_z": "stop.height_z"}], "features": rows}
    stack = check_stack.evaluate_spec(P, spec)
    f = stack["poses"]["capture_end"]["features"]
    fig, ax = sc.setup_figure("side_xz", title="ring on tube fixture")
    for row in rows:
        fid = row["id"]
        dz = (shift or {}).get(fid, 0)
        z0, z1 = f[fid]["z_min"] + dz, f[fid]["z_max"] + dz
        if fid == "gear":
            sc.draw_gear_section(ax, fid, P.get("gear.bore") / 2, P.get("gear.pitch_diameter") / 2, z0, z1)
        elif fid == "bearing":
            for s in (-1, 1):
                sc.draw_rect(ax, fid, s * P.get("bearing.bore") / 2, s * P.get("bearing.od") / 2, z0, z1)
        else:
            x0, x1 = f[fid]["place"]["x"]
            sc.draw_rect(ax, fid, x0, x1, z0, z1)
    sc.finish_axes(ax)
    return _ctx(P, spec, {"capture_end": fig})


def k8_z3():
    return _ring_on_tube()


def k8_b12():
    """Bearing (ring assembly) slid down onto the drill head: its bottom 5 mm below the head top."""
    P = Params()
    drop = P.get("ring.position_above_tip") - (P.get("bearing.height") - P.get("ring.thickness")) - P.get("drill.head_length") + 5
    return _ring_on_tube({"bearing": -drop})


def k8_b13():
    """Gear drawn 5 mm above the tube top (ring assembly off the drill end)."""
    P = Params()
    s = check_stack.evaluate_spec(P, {"poses": [{"id": "x", "tip_z": "stop.height_z"}], "features": [], "view": "side_xz"})
    v = s["poses"]["x"]["vars_z_A"]
    return _ring_on_tube({"gear": v["drill_top"] - v["gear_top"] + 5})


# ---------------------------------------------------------------- K9

def k9_z():
    return mini_ctx()


def k9_b1():
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: None if f == "guide_member" else (x0, x1, z0, z1))


def k9_b2():
    return mini_ctx(extra=lambda ax: sc.draw_rect(ax, "spare_bracket", 300, 340, 0, 40))


def k9_b3():
    """TP-6: guide_member replaced by a Text carrying its gid."""
    def extra(ax):
        t = ax.text(230, 600, "guide member")
        t.set_gid("guide_member")
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: None if f == "guide_member" else (x0, x1, z0, z1), extra=extra)


def k9_b4():
    """TP-8: a second anchor_a row with empty sense."""
    spec = mini_side_spec()
    dup = dict(next(r for r in spec["features"] if r["id"] == "anchor_a"))
    dup["sense"] = []
    spec["features"].append(dup)
    return mini_ctx(spec=spec)


# ---------------------------------------------------------------- SW-8 smoke: every S1 spec row drawn

def _section_pieces(P, stack, pid, row, z0, z1):
    """Spec field section (r2): [r_in, r_out] or a list of [r_in, r_out, z_lo, z_hi] (z_A stack names) -> z_S pieces."""
    sec = row["section"]
    pieces = sec if isinstance(sec[0], (list, tuple)) else [sec]
    pr = stack["poses"][pid]
    names, shift = pr["vars_z_A"], pr["tip_z_S"] - pr["tip_z_A"]
    out = []
    for p in pieces:
        r0, r1 = (check_stack.eval_expr(e, P, names) for e in p[:2])
        lo, hi = ((check_stack.eval_expr(e, P, names) + shift for e in p[2:4]) if len(p) > 2 else (z0, z1))
        out.append((r0, r1, lo, hi))
    return out


def _draw_section(ax, P, spec, stack, pid, row, z0, z1):
    """Section row, one piece per side. A cone row narrows by (z1 - z0) tan(cone.alpha) on its outer face per its taper
    sense. A bore_cone row follows the mate's outer cone over the mate's z extent (TP1.1-3)."""
    fid = row["id"]
    tan_a = math.tan(math.radians(P.get("cone.alpha")))
    rows = {r["id"]: r for r in spec["features"]}
    for r0, r1, lo, hi in _section_pieces(P, stack, pid, row, z0, z1):
        if row["kind"] == "cone":
            narrows = next((s["narrows"] for s in row.get("sense", []) if s.get("pred") == "taper"), "up")
            t = (hi - lo) * tan_a
            pts = [(r0, lo), (r1, lo), (r1 - t, hi), (r0, hi)] if narrows == "up" else [(r0, lo), (r1 - t, lo), (r1, hi), (r0, hi)]
            for s in (-1, 1):
                sc.draw(fid, Polygon([(s * x, z) for x, z in pts], closed=True, fill=False), ax)
            continue
        mate = row.get("bore_cone")
        if mate:
            mf = stack["poses"][pid]["features"][mate]
            mr0, mr1 = (check_stack.eval_expr(e, P, {}) for e in rows[mate]["section"])
            zk = min(mf["z_max"], hi)
            if lo < zk:
                rc = lambda z: mr1 - (z - mf["z_min"]) * tan_a  # noqa: E731
                for s in (-1, 1):
                    sc.draw(fid, Polygon([(s * rc(lo), lo), (s * r1, lo), (s * r1, zk), (s * rc(zk), zk)], closed=True, fill=False), ax)
                lo = zk
            if lo >= hi:
                continue
        for s in (-1, 1):
            sc.draw_rect(ax, fid, s * r0, s * r1, lo, hi)


def _s1_draw_pose(P, spec, stack, pid):
    fig, ax = sc.setup_figure(spec["view"], title=f"S1 full draw, pose {pid}")
    feats = stack["poses"][pid]["features"]
    half_fp = P.get("icd.footprint_x") / 2
    for row in spec["features"]:
        fid = row["id"]
        f = feats.get(fid)
        if f is None or "z_min" not in f:
            continue
        z0, z1 = f["z_min"], f["z_max"]
        if fid in ("keepout", "wingnut_sweep"):   # 1.4 P6: wingnut_sweep, the sweep envelope reference row (TP1.4-2)
            r = P.get("icd.keepout_radius") if fid == "keepout" else P.get("wingnut.sweep_clear_radius")
            for x in (-r, r):
                sc.draw(fid, Line2D([x, x], [z0, z1]), ax)
            continue
        if row.get("section_true") and row["kind"] != "line":   # 1.4 P6: the true section, as the S1 r9 script draws it
            pcs = sc.section_true_polys(P, stack["poses"][pid]["vars_z_A"], row)
            dz = z0 - min(v[1] for _, _, pts in pcs for v in pts)   # a _s1_ctx shift plant moves the drawn pieces
            for name, _side, pts in pcs:
                sc.draw_piece(ax, fid, name, [(x, z + dz) for x, z in pts])
            continue
        if row["kind"] == "line":
            # r3: a placed line (pinion centreline) runs over its projected x; else over its depth band or the footprint
            x0, x1 = f["place"]["x"] if f.get("place") else (f["depth"] if f.get("depth") else (-half_fp, half_fp))
            sc.draw_hline(ax, fid, x0, x1, z0)
            continue
        if row["kind"] == "gear" and row.get("axis") == "Z":
            r_out = P.get("gear.od") / 2 if P.has("gear.od") else P.get("gear.pitch_diameter") / 2
            sc.draw_gear_section(ax, fid, P.get("gear.bore") / 2, r_out, z0, z1)
            continue
        if row.get("section"):
            _draw_section(ax, P, spec, stack, pid, row, z0, z1)
            continue
        # 1.2 (b): a plan_poly row with no place (S1 r5 guide ties) spans its plan x extent
        x0, x1 = f["place"]["x"] if f.get("place") else (f["plan_x"] if f.get("plan_x") else f["depth"])
        if row["kind"] == "gear":
            inner, outer = (x0, x1) if abs(x0) < abs(x1) else (x1, x0)
            h = z1 - z0
            # bevel pinion: toe height at the inner end, full height at the outer end, centred on its axis
            sc.draw(fid, Polygon([(inner, z0 + h / 4), (outer, z0), (outer, z1), (inner, z1 - h / 4)], closed=True, fill=False), ax)
        elif row["kind"] == "cone":
            t = (z1 - z0) * math.tan(math.radians(P.get("cone.alpha")))
            narrows = next((s["narrows"] for s in row.get("sense", []) if s.get("pred") == "taper"), "up")
            if narrows == "up":
                pts = [(x0, z0), (x1, z0), (x1 - t, z1), (x0 + t, z1)]
            else:
                pts = [(x0 + t, z0), (x1 - t, z0), (x1, z1), (x0, z1)]
            sc.draw(fid, Polygon(pts, closed=True, fill=False), ax)
        else:
            sc.draw_rect(ax, fid, x0, x1, z0, z1)
    if hasattr(sc, "draw_cut_outlines"):   # 1.4 (h) r2 (M1 S4 F3): one outlined region per cut body, as the S1 r10 script
        sc.draw_cut_outlines(spec, ax)
    sc.place_labels(ax, spec, P, pid)
    if spec.get("figure_note"):   # Designer 1.2 (c) FIX R1: S1 r5 figure note, as s1_side_poses.py draws it
        ax.text(0, -0.06, spec["figure_note"], transform=ax.transAxes, fontsize=6).set_gid(sc.NOTE_GID)
    sc.finish_axes(ax)
    return fig


def _s1_ctx(shift=None, spec_mut=None, values=None, xshift=None):
    """Live S1 spec, every row drawn from check_stack values. shift {(pose or None, fid): (dz_min, dz_max)} moves the
    drawn z of one row (None: every pose) in the drawing only; the context keeps the true stack, so a B planted this
    way is a drawing that disagrees with the spec. xshift {(pose or None, fid): dx} moves the drawn x the same way.
    spec_mut(spec) edits the spec and values {key: value} replaces params/overlay values before check_stack runs, so a
    B planted that way is a spec or params decision drawn faithfully (SW-10: S1-2 and S1-3 can fail only that way)."""
    P = Params()
    for k, v in (values or {}).items():
        P.leaves[k] = dict(P.leaves[k], value=v)
    spec = load_spec(HERE.parent / "s1_spec.yaml")
    if spec_mut:
        spec_mut(spec)
    stack = check_stack.evaluate_spec(P, spec)
    drawn = copy.deepcopy(stack)
    for (pose, fid), (d0, d1) in (shift or {}).items():
        for pid, pr in drawn["poses"].items():
            if pose in (None, pid) and fid in pr["features"]:
                pr["features"][fid]["z_min"] += d0
                pr["features"][fid]["z_max"] += d1
    for (pose, fid), dx in (xshift or {}).items():
        for pid, pr in drawn["poses"].items():
            if pose in (None, pid) and fid in pr["features"]:
                pr["features"][fid]["place"]["x"] = [v + dx for v in pr["features"][fid]["place"]["x"]]
    figs = {p["id"]: _s1_draw_pose(P, spec, drawn, p["id"]) for p in spec["poses"]}
    return sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], script_paths=[], check_stack_path=CHECK_STACK_PATH)


def s1_full_ctx():
    return _s1_ctx()


def s1_live():
    """Z for S1-4, S1-5b and K7 on the live spec (1.1 (b) fix pass): the S1-FULL drawing."""
    return _s1_ctx()


def s1_4_b1():
    """FIX 2 (Loftsman): top guides drawn 20 low in every pose, i.e. L 880 against L_min 885. The 1.0 band
    (guide z_max - guide_allowance - nut_length / 2) passes it with 4.16 to spare; the K7-consistent band fires at
    load and park, both screws (high margin 14.16 - 20 = -5.84)."""
    return _s1_ctx({(None, "guide_a"): (-20, -20), (None, "guide_b"): (-20, -20)})


def s1_5b_b1():
    """FIX 1 (Loftsman): collar ring drawn 133 high at capture_end, bearing bottom 9 above the collar top (g_min 10)."""
    return _s1_ctx({("capture_end", "collar"): (133, 133)})


def k7_b12():
    """FIX 3 (Loftsman): capture core drawn 60 high at start, its top 17.66 into the drill head. core_750|drill_head is
    declared N at capture_end only; at start the pair is undeclared and must be tested as F."""
    return _s1_ctx({("start", "core_750"): (60, 60)})


def k7_b13():
    """F4 (Designer): screw frame member foot drawn 1 mm above the plate top at load (C pair open by 1)."""
    return _s1_ctx({("load", "frame_upper_a"): (1, 0)})


# ---------------------------------------------------------------- 1.1 (c) red-first: S1-x fixtures from the signed spec (H6)
# Z for every S1-x is s1_live (the signed spec drawn faithfully). Each B plants one defect named in the gameplan S1
# check table (l.226-234) or the SW-10 rule (Design Notes 20), as revised at 1.1 (b) (spec revision corrections 2, 3).

def _pose_tip(pid, expr):
    def mut(s):
        next(p for p in s["poses"] if p["id"] == pid)["tip_z"] = expr
    return mut


def s1_1_b1():
    """Gameplan l.228 B: upper.travel_max 500 (below drill_advance_500core 534.93); drawn reach 650.00 exceeds it.
    1.2 step 0 (H5): with travel 500 the start-above-core term governs the 0.75 m class (42.5 + 750 + c - 500), so the
    park-rule start would depend on c, which check_stack refuses. The fixture evaluates the term at c = 0 (a control
    input, not a design value); S1-1 reads the drawn tips only, so its reason is unchanged."""
    def c0(spec):
        spec["park_rule"]["stop_k"] = spec["park_rule"]["stop_k"].replace("L + c -", "L + 0 -")
        spec.pop("symbols", None)
    return _s1_ctx(values={"upper.travel_max": 500}, spec_mut=c0)


def s1_1_b2():
    """Low side: start tip set 1 below capture_end tip + drill_advance_500core (reach 533.93 < 534.93)."""
    return _s1_ctx(spec_mut=_pose_tip("start", "stop.height_z + upper.drill_advance_500core - 1"))


def s1_2_b1():
    """Design Notes 22 replacement for SW-10 (the 959.84 live-defect B is retired under option R): park tip_z set to
    start_tip_max, the top of the 650 mm travel (stroke conflated with travel, SE-3). Margin 0.00."""
    return _s1_ctx(spec_mut=_pose_tip("park", "start_tip_max"))


def s1_2_b2():
    """SW 1.1 (c) FIX 1: load branch of S1-2. Load tip_z set to start_tip_max (894.84 z_S), not above the highest
    class start. Margin 0.00."""
    return _s1_ctx(spec_mut=_pose_tip("load", "start_tip_max"))


def s1_3_b1():
    """SW-10 as revised at 1.1 (b) (correction 3): park tip_z = core_stop + core.length_install + upper.load_clearance
    - 1 (the SW-10 form park_tip - load_clearance - 1 leaves 66.34 under the collar-top park). Margin -1.00."""
    return _s1_ctx(spec_mut=_pose_tip("park", "core_stop + core.length_install + upper.load_clearance - 1"))


def s1_4_b2():
    """Gameplan l.231 B: ring nut drawn 100 above the top guide of screw a at park (nut and its housing moved)."""
    P = Params()
    spec = load_spec(HERE.parent / "s1_spec.yaml")
    f = check_stack.evaluate_spec(P, spec)["poses"]["park"]["features"]
    nut_c = (f["nut_a"]["z_min"] + f["nut_a"]["z_max"]) / 2
    dz = f["guide_a"]["z_max"] + 100 - nut_c
    return _s1_ctx({("park", "nut_a"): (dz, dz), ("park", "nut_housing_a"): (dz, dz)})


def s1_5a_b1():
    """Gameplan l.232 B: drill internal length (tip to bore ceiling) set 1 below drill_advance_500core (533.93)."""
    P = Params()
    return _s1_ctx(values={"drill.bore_ceiling_above_tip": P.get("upper.drill_advance_500core") - 1})


def s1_6_b1():
    """Gameplan l.234 B: screw b (theta jackscrew.angle[0] 30) drawn at x = r (160) in every pose, r cos(theta) 138.56."""
    P = Params()
    spec = load_spec(HERE.parent / "s1_spec.yaml")
    pl = check_stack.evaluate_spec(P, spec)["poses"]["load"]["features"]["screw_b"]["place"]
    dx = pl["r_c"] - pl["r_c"] * check_stack.cosd(pl["theta"])
    return _s1_ctx(xshift={(None, "screw_b"): dx})


def s1_7_b1():
    """Gameplan l.234 S1-7 B: the 0.5 m core as the capture core (core_750 row drawn core.length_capture long):
    542.50 - 184.84 = 357.66 against 534.93, short 177.27."""
    def mut(s):
        row = next(r for r in s["features"] if r["id"] == "core_750")
        row["z_rule"] = dict(row["z_rule"], z_max="capture_core_bottom + core.length_capture")
        s["capture_core_length"] = "core.length_capture"
    return _s1_ctx(spec_mut=mut)


# ---------------------------------------------------------------- r2: (e) cross-review findings (LF1.1-1, TP1.1-1 to -3)

def k6_b7():
    """LF1.1-1: holder z_max at the r1 rule (holder_bottom + holder.length, no flange). stack_tie holder_flange reads
    137.09 + 8.00 + 6.75 = 151.84 against collar_top 159.84 z_A, 8.00 apart."""
    def mut(s):
        row = next(r for r in s["features"] if r["id"] == "holder")
        row["z_rule"] = dict(row["z_rule"], z_max="holder_bottom + holder.length")
    P = Params()
    spec = load_spec(HERE.parent / "s1_spec.yaml")
    mut(spec)
    stack = check_stack.evaluate_spec(P, spec)
    return sc.Ctx(P=P, spec=spec, figs={}, stack=stack, view=spec["view"], check_stack_path=CHECK_STACK_PATH)


def _face_spec():
    spec = mini_side_spec()
    g = next(r for r in spec["features"] if r["id"] == "gear")
    g["sense"] = g["sense"] + [{"pred": "face_rises", "toward": "outward"}]
    return spec


def k8_z4():
    """TP1.1-1 Z: mini figure, gear drawn by draw_gear_section (tooth face rising outward)."""
    return mini_ctx(spec=_face_spec())


def k8_b14():
    """TP1.1-1 B (Topologist probe): gear pieces with the heel low and the face falling outward,
    (r_in, z0 + rise), (r_out, z0), (r_out, z1), (r_in, z1). The width taper (narrows down) passes it."""
    def gear(ax, fid, r_in, r_out, z0, z1):
        rise = (z1 - z0) / 2
        right = [(r_in, z0 + rise), (r_out, z0), (r_out, z1), (r_in, z1)]
        sc.draw(fid, Polygon(right, closed=True, fill=False), ax)
        sc.draw(fid, Polygon([(-x, z) for x, z in right], closed=True, fill=False), ax)
    return mini_ctx(spec=_face_spec(), gear=gear)


def k9_b5():
    """TP1.1-2: core_750 (poses load, start, capture_end) drawn seated at park, at its start-pose z."""
    c = _s1_ctx()
    f = c.stack["poses"]["start"]["features"]["core_750"]
    r = c.P.get("core.diameter_nominal") / 2
    sc.draw_rect(c.figs["park"].axes[0], "core_750", -r, r, f["z_min"], f["z_max"])
    return c


def k7_b14():
    """TP1.1-3 lint: collet|holder declared N again (the r1 declaration) between two section rows."""
    def mut(s):
        row = next(r for r in s["features"] if r["id"] == "collet")
        for nb in row["neighbours"]:
            if nb["id"] == "holder":
                nb["class"] = "N"
    return _s1_ctx(spec_mut=mut)


def k7_b15():
    """TP1.1-3 drawing: the r1 holder (bore at the core OD down to the holder bottom, no bore_cone) against the C
    declaration: 313.12 mm2 per side inside the collet cone, every pose."""
    # 1.4 P6: S1 r9 draws the holder as its true section, so the bore_cone field no longer shapes the drawing; the plant is
    # the class of the r1 drawing on the true section: the holder cone piece drawn 5 mm toward the axis on each side,
    # into the collet cone (collet|holder C, overlap), every pose.
    c = _s1_ctx()
    for fig in c.figs.values():
        for a in sc.tagged(fig.axes[0]).get("holder", []):
            if getattr(a, sc.PIECE_ATTR, None) == "cone":
                a.set_xy([(x - 5 * (1 if x > 0 else -1), z) for x, z in a.get_xy()])
    return c


def k5_b6():
    """TP1.1-3 K5 guard: a holder bore_cone trapezoid drawn above the collet top (outside the mate's z extent)."""
    c = _s1_ctx()
    ax = c.figs["capture_end"].axes[0]
    f = c.stack["poses"]["capture_end"]["features"]
    z0 = f["collet"]["z_max"]
    r = c.P.get("receiver.register_bore_radius")
    sc.draw("holder", Polygon([(r - 2, z0 + 5), (r, z0 + 5), (r, z0 + 10), (r - 3, z0 + 10)], closed=True, fill=False), ax)
    return c


# ---------------------------------------------------------------- r3: Designer M1 r2 (F1, F2): C pairs at an oblique azimuth

def _arm_block(r_in):
    """r3 plan-contact: a round block (r 160, half-width 21, theta 150: anchor-block-like) and a radial arm from r_in to
    270, half-width 30, same theta (bracket-arm-like), declared C, both drawn from their placed x extents over one z band.
    In the side view the boxes overlap at any r_in near 181; the plan footprints decide."""
    rows = [{"id": "arm", "name": "arm", "kind": "prism", "projection": "rectangle",
             "place": {"r_in": r_in, "r_out": 270, "theta": 150, "half_width": 30, "footprint": "radial"},
             "neighbours": [{"id": "block", "class": "C", "g_min": 0, "source": "fixture"}]},
            {"id": "block", "name": "block", "kind": "prism", "projection": "rectangle",
             "place": {"r_in": 160, "theta": 150, "half_width": 21, "footprint": "round"}}]
    P = Params()
    spec = {"sketch": "k7", "view": "side_xz", "poses": ONE, "features": rows, "undeclared_pairs": "F"}
    stack = check_stack.evaluate_spec(P, spec)
    f = stack["poses"]["fixture"]["features"]
    fig, ax = sc.setup_figure("side_xz", title="k7 fixture arm on block")
    for fid in ("arm", "block"):
        x0, x1 = f[fid]["place"]["x"]
        sc.draw_rect(ax, fid, x0, x1, 0, 30)
    sc.finish_axes(ax)
    return _ctx(P, spec, {"fixture": fig})


def k7_z11():
    """r3 Z: arm face at r 181 = block r 160 + 21, tangent in plan; side-view boxes overlap: plan-contact."""
    return _arm_block(181)


def k7_b16():
    """r3 B: arm face at r 182, 1 mm off the block in plan (the arm floats); side-view boxes still overlap."""
    return _arm_block(182)


def k7_b17():
    """r3 B: arm face at r 180, 1 mm into the block in plan (interference); side-view boxes overlap."""
    return _arm_block(180)


def _mut_row(fid, fn):
    def mut(s):
        fn(next(r for r in s["features"] if r["id"] == fid))
    return mut


def k7_b18():
    """r3 B on the live spec (Designer M1 r2 F3, pad floating): descent_stop_post ends 1 mm under the pad, drawn
    faithfully; descent_stop_post|descent_stop C opens by 1.000 in every pose."""
    return _s1_ctx(spec_mut=_mut_row("descent_stop_post", lambda r: r.__setitem__(
        "z_rule", dict(r["z_rule"], z_max="ring_bottom_low - stop.pad_thickness - 1"))))


def k7_b19():
    """r3 B on the live spec (Designer M1 r2 F2, block floating off its arm): bracket_anchor_a r_in 1 mm outboard of
    the anchor block face (pitch_radius + nut_flange_od / 2 + 1), drawn faithfully; plan footprints 0.994 apart."""
    return _s1_ctx(spec_mut=_mut_row("bracket_anchor_a", lambda r: r.__setitem__(
        "place", dict(r["place"], r_in="jackscrew.pitch_radius + jackscrew.nut_flange_od / 2 + 1"))))


# ---------------------------------------------------------------- r4: LF1.1-8 = TP1.1-12, TP1.1-11

def k7_b20():
    """r4 B (LF1.1-8): screw frame member a turned 45 deg in plan (place rot 45), drawn faithfully. The square's corner
    reaches r 300 - 42.43 = 257.57 toward the axis, 12.43 into each arm face at r 270: overlap 12.43^2 = 154.4 mm2."""
    return _s1_ctx(spec_mut=_mut_row("frame_upper_a", lambda r: r.__setitem__("place", dict(r["place"], rot=45))))


def _widen(fid, d):
    """Live S1 drawing with every artist of row fid drawn d wider at each end in x (centre unchanged)."""
    c = _s1_ctx()
    for fig in c.figs.values():
        for a in sc.tagged(fig.axes[0]).get(fid, []):
            a.set_x(a.get_x() - d)
            a.set_width(a.get_width() + 2 * d)
    return c


def k8_b15():
    """r4 B (TP1.1-11): bracket_anchor_a drawn 20 wider at each end; centre and spec footprint unchanged."""
    return _widen("bracket_anchor_a", 20)


def k8_b16():
    """r4 B (TP1.1-11): motor_shaft_a drawn 15 wider at each end; centre and spec footprint unchanged."""
    return _widen("motor_shaft_a", 15)


def k8_b28():
    """SW 1.2 (c) FIX 5 (r4 rule, low-x end of projected_extent): motor_shaft_a drawn 15 longer at its low-x end only;
    the high-x end and the spec footprint unchanged. Fires projected_x (centre 7.50 off) and projected_extent (by 15.00)
    at each of the four poses."""
    c = _s1_ctx()
    for fig in c.figs.values():
        for a in sc.tagged(fig.axes[0]).get("motor_shaft_a", []):
            a.set_x(a.get_x() - 15)
            a.set_width(a.get_width() + 15)
    return c


def k5_b12():
    """SW 1.2 (c) FIX 5 (r2 rule, bore_cone lower bound): a holder bore_cone trapezoid drawn 10 to 5 below the collet
    bottom at capture_end (outside the mate's z extent on the low side; K5-B6 is the high side)."""
    c = _s1_ctx()
    ax = c.figs["capture_end"].axes[0]
    z0 = c.stack["poses"]["capture_end"]["features"]["collet"]["z_min"]
    r = c.P.get("receiver.register_bore_radius")
    sc.draw("holder", Polygon([(r - 2, z0 - 10), (r, z0 - 10), (r, z0 - 5), (r - 3, z0 - 5)], closed=True, fill=False), ax)
    return c


def k8_b24():
    """Topologist 1.2 (c) FIX TP1.2-1: live S1 (side view) with frame: radial on motor23_a's outboard predicate. The radial
    form reads the plan centroid; in a side view it is a spec error, reported once."""
    def mut(s):
        row = next(r for r in s["features"] if r["id"] == "motor23_a")
        next(p for p in row["sense"] if p.get("pred") == "outboard")["frame"] = "radial"
    return _s1_ctx(spec_mut=mut)


def k4_b6():
    """Designer 1.2 (c) FIX R1: S1 r5 spec (not_drawn holds the LM20UU bushing) with its figure_note removed; the sketch-id
    exemption is gone, so K4 fires on the spec."""
    return _s1_ctx(spec_mut=lambda s: s.pop("figure_note", None))


def k8_b17():
    """1.2 (b) B (detail 1 common (h)): guide_tie_a (plan_poly row, no place) drawn 10 wider at each end in x; the
    plan_poly extent is unchanged. Premise check of the plan_poly footprint in K7 plan-contact and plan-separated."""
    return _widen("guide_tie_a", 10)


def k7_b21():
    """1.2 (b) B (Designer 1.2 (b) Correction 1): guide_tie_a strip run to the member centre (stop_at removed), drawn
    faithfully. The tie end lies inside the 60 x 60 member square, so tie|frame_upper_b C overlaps in plan at every pose."""
    def mut(r):
        st = dict(r["plan_poly"][0]["strip"])
        st.pop("stop_at")
        r["plan_poly"] = [{"strip": st}]
    return _s1_ctx(spec_mut=_mut_row("guide_tie_a", mut))


def s1_full_draw():
    """Returns (ctx, extra checks): K1 to K9 and S1-1 to S1-6 run on it."""
    return s1_full_ctx(), checks_s1.run


# ---------------------------------------------------------------- 1.2 (c): S2 plan drawing from the signed spec

S2_SPEC = HERE.parent / "s2_spec.yaml"


def _s2_pose(spec):
    return (spec.get("plan_figure") or {}).get("pose") or spec["poses"][0]["id"]


def _radial_poly(r0, r1, th, w0, w1=None):
    """Four-vertex piece along the radial direction at th: half-width w0 at r0, w1 at r1 (w1 = w0: rectangle)."""
    w1 = w0 if w1 is None else w1
    c, s = check_stack.cosd(th), check_stack.sind(th)
    return [(u * c - v * s, u * s + v * c) for u, v in ((r0, -w0), (r1, -w1), (r1, w1), (r0, w0))]


def _s2_draw_row(ax, P, spec, stack, pid, row):
    """One S2 row drawn faithfully from the check_stack record in plan (the drawing s2_plan.py makes at (d), as a
    fixture): sector as a wedge polygon; section rows as an Annulus; plan_poly pieces as polygons (two-point pieces as
    lines); placed radial rows as rectangles (bevel pinion: toothed trapezoid toe to pinion.r_heel, apex-consistent
    toe width, plus a hub rectangle to r_out); zero-width radial rows as lines (draw.solid / draw.dashed spans); placed
    round rows as circles (projection rectangle: the inscribed square, faces radial and tangential); collet_axis as the
    datum B cross with +X / +Y arrowheads and a counter-clockwise theta arc."""
    fid = row["id"]
    f = stack["poses"][pid]["features"].get(fid, {})
    names = stack["poses"][pid]["vars_z_A"]
    ev = lambda e: check_stack.eval_expr(e, P, names)  # noqa: E731
    if f.get("sector"):
        sc.draw(fid, Polygon(sc.sector_boundary(f["sector"])[:-6], closed=True, fill=False), ax)
        return
    if fid == "collet_axis":
        L = P.get("drill.tube_od") / 4
        hd = L / 6
        for xs, ys in (([-L, L], [0, 0]), ([0, 0], [-L, L]), ([L - hd, L, L - hd], [hd / 2, 0, -hd / 2]),
                       ([hd / 2, 0, -hd / 2], [L - hd, L, L - hd])):
            sc.draw(fid, Line2D(xs, ys), ax)
        arc = [(0.6 * L * check_stack.cosd(a), 0.6 * L * check_stack.sind(a)) for a in range(0, 61, 5)]
        sc.draw(fid, Line2D([p[0] for p in arc], [p[1] for p in arc]), ax)
        return
    if row.get("section") and not f.get("place"):
        a, b = sorted(ev(e) for e in row["section"])
        sc.draw(fid, Annulus((0, 0), b, b - a, fill=False) if a > 0 else Circle((0, 0), b, fill=False), ax)
        return
    if f.get("plan_pieces"):
        for pc in f["plan_pieces"]:
            if len(pc) == 2:
                sc.draw(fid, Line2D([pc[0][0], pc[1][0]], [pc[0][1], pc[1][1]]), ax)
            else:
                sc.draw(fid, Polygon(pc, closed=True, fill=False), ax)
        return
    pl = f.get("place")
    if not pl:
        return
    th, r0, r1, w = pl["theta"], pl["r_in"], pl["r_out"], pl["half_width"]
    c, s = check_stack.cosd(th), check_stack.sind(th)
    if pl["footprint"] == "radial":
        if w == 0:
            spans = [[ev(x) for x in row["draw"][k]] for k in ("solid", "dashed")] if row.get("draw") else [[r0, r1]]
            for u0, u1 in spans:
                sc.draw(fid, Line2D([u0 * c, u1 * c], [u0 * s, u1 * s]), ax)
        elif row["kind"] == "gear":
            heel = P.get("pinion.r_heel")
            w_toe = w * r0 / heel
            sc.draw(fid, Polygon(_radial_poly(r0, heel, th, w_toe, w), closed=True, fill=False), ax)
            sc.draw(fid, Polygon(_radial_poly(heel, r1, th, w / 2), closed=True, fill=False), ax)
        else:
            sc.draw(fid, Polygon(check_stack.radial_corners(r0, r1, th, w, pl.get("rot", 0)), closed=True, fill=False), ax)
        return
    cx, cy = pl["r_c"] * c, pl["r_c"] * s
    if row.get("projection") == "rectangle":
        h = w / math.sqrt(2)
        sq = [(cx + u * c - v * s, cy + u * s + v * c) for u, v in ((-h, -h), (h, -h), (h, h), (-h, h))]
        sc.draw(fid, Polygon(sq, closed=True, fill=False), ax)
    else:
        sc.draw(fid, Circle((cx, cy), w, fill=False), ax)


def _ticks(P, pr, n=None, r_in=None, r_out=None, turn=None, start=0.0):
    """LineCollection of radial ticks from the ticks_radial fields (count, r_in, r_out), evenly spaced from start (deg).
    turn = (index, deg): that tick turned about its midpoint (B1)."""
    r0 = check_stack.eval_expr(pr["r_in"], P, {}) if r_in is None else r_in
    r1 = check_stack.eval_expr(pr["r_out"], P, {}) if r_out is None else r_out
    n = int(round(check_stack.eval_expr(pr["count"], P, {}))) if n is None else n
    segs = []
    for i in range(n):
        a = math.radians(start + 360.0 * i / n)
        p0, p1 = (r0 * math.cos(a), r0 * math.sin(a)), (r1 * math.cos(a), r1 * math.sin(a))
        if turn and turn[0] == i:
            mx, my, t = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, math.radians(turn[1])
            rot = lambda q: (mx + (q[0] - mx) * math.cos(t) - (q[1] - my) * math.sin(t), my + (q[0] - mx) * math.sin(t) + (q[1] - my) * math.cos(t))  # noqa: E731
            p0, p1 = rot(p0), rot(p1)
        segs.append([p0, p1])
    return LineCollection(segs, linestyles="--")


def _notch_ring(pieces):
    """Fixture's own plate outline (independent of sketch_common.union_boundary): the bounding rectangle of the pieces with
    each notch cut in; a notch is a bbox edge interval no piece reaches, found from the piece x and y extents."""
    xs0, xs1 = min(p[0] for pc in pieces for p in pc), max(p[0] for pc in pieces for p in pc)
    ys0, ys1 = min(p[1] for pc in pieces for p in pc), max(p[1] for pc in pieces for p in pc)

    def gap(edge_y):
        on = sorted((min(p[0] for p in pc), max(p[0] for p in pc)) for pc in pieces if any(abs(p[1] - edge_y) < 1e-6 for p in pc))
        depth = min(abs(p[1] - edge_y) for pc in pieces for p in pc if abs(p[1] - edge_y) > 1e-6 and
                    any(abs(q[1] - edge_y) < 1e-6 for q in pc))
        return [(a[1], b[0]) for a, b in zip(on, on[1:]) if b[0] - a[1] > 1e-6], depth
    (bot, db), (top, dt) = gap(ys0), gap(ys1)
    ring = [(xs0, ys0)]
    for g0, g1 in bot:
        ring += [(g0, ys0), (g0, ys0 + db), (g1, ys0 + db), (g1, ys0)]
    ring += [(xs1, ys0), (xs1, ys1)]
    for g0, g1 in sorted(top, reverse=True):
        ring += [(g1, ys1), (g1, ys1 - dt), (g0, ys1 - dt), (g0, ys1)]
    ring += [(xs0, ys1)]
    return ring


def _s2_draw(P, spec, stack, skip=(), note=None):
    pid = _s2_pose(spec)
    fig, ax = sc.setup_figure(spec["view"], title=f"S2 plan fixture, pose {pid}")
    for row in spec["features"]:
        if row["id"] in skip or not sc.applies(row, pid):
            continue
        _s2_draw_row(ax, P, spec, stack, pid, row)
        tk = next((p for p in row.get("sense") or [] if p.get("pred") == "ticks_radial"), None)
        if tk:   # 1.2 (h): gear tooth ticks (Designer M1 r1 F1), from the predicate's own fields
            sc.draw(row["id"] + sc.TICKS_SUFFIX, _ticks(P, tk), ax)
    rctx = sc.Ctx(P=P, spec=spec, stack=stack, view=spec["view"])
    sc.render_plan(rctx, ax, pid)   # 1.3 P1R: the plan hidden-line renderer (r3 to r5: style_hidden)
    bp = next((r for r in spec["features"] if r["id"] == "base_plate"), None)
    if bp and any(p.get("pred") == "outline_matches" for p in bp.get("sense") or []) and "base_plate" not in skip:
        sc.draw("base_plate:outline", Polygon(_notch_ring(stack["poses"][pid]["features"]["base_plate"]["plan_pieces"]),
                                              closed=True, fill=False), ax)   # r4: plate outline (Designer sign-off r3)
    sc.finish_axes(ax)
    sc.place_plan_labels(ax, rctx, pid, margin=False)   # 1.3 P1R: the plan leader placer (text 60 right, 20 up)
    txt = (spec.get("plan_figure") or {}).get("figure_note") if note is None else note
    if txt:
        t = ax.text(0, -0.06, txt, transform=ax.transAxes, fontsize=6)
        t.set_gid(sc.NOTE_GID)
    return {pid: fig}


_S2_LIVE = {}


def _s2_ctx(spec_mut=None, values=None, skip=(), note=None, cache=False):
    """Live S2 spec drawn faithfully (one plan figure at plan_figure.pose). spec_mut and values as _s1_ctx (a B planted
    that way is a spec or params decision drawn faithfully). cache=True shares one read-only context among Z controls."""
    if cache and "ctx" in _S2_LIVE:
        return _S2_LIVE["ctx"]

    def make():
        P = Params()
        for k, v in (values or {}).items():
            P.leaves[k] = dict(P.leaves[k], value=v)
        spec = load_spec(S2_SPEC)
        if spec_mut:
            spec_mut(spec)
        stack = check_stack.evaluate_spec(P, spec)
        return P, spec, stack, _s2_draw(P, spec, stack, skip=skip, note=note)
    if spec_mut is None and not values and not skip and note is None:   # 1.4 step 0 R1 e
        P, spec, stack, figs = draw_cache("s2 fixture", [S2_SPEC], make)
    else:
        P, spec, stack, figs = make()
    ctx = sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], script_paths=[], check_stack_path=CHECK_STACK_PATH)
    if cache:
        _S2_LIVE["ctx"] = ctx
    return ctx


def s2_live():
    """Z for K4 to K9 in plan and S2-1 to S2-6: the signed S2 spec drawn faithfully."""
    return _s2_ctx(cache=True)


def _s2_ax(c):
    return next(iter(c.figs.values())).axes[0]


def _s2_replace(c, fid, artists_fn, render=False):
    """Remove every artist of row fid from the S2 plan figure and draw artists_fn(ctx) in its place (drawing-only B).
    render=True (1.3 P1R): the new artists go through the plan renderer as the drawing's own pieces did (a B whose
    planted defect is not the hidden-line drawing)."""
    ax = _s2_ax(c)
    for a in sc.tagged(ax).get(fid, []):
        a.remove()
    for a in artists_fn(c):
        sc.draw(fid, a, ax)
    if render:
        sc.render_plan(c, ax, _s2_pose(c.spec))
    return c


def _s2_place(c, fid):
    return c.stack["poses"][_s2_pose(c.spec)]["features"][fid]["place"]


def _shift(c, fid, dx, dy):
    T = Affine2D().translate(dx, dy)
    ax = _s2_ax(c)
    for a in sc.tagged(ax).get(fid, []):   # artist transform transData (patch transform, where any, applies first)
        a.set_transform(T + ax.transData)
    return c


# K4 (figure note, detail 1 common (b) second clause; Designer 1.2 (b) FIX 3)

def k4_b4():
    """Figure note drawn without the LM20UU bushing (the spec figure_note and not_drawn unchanged)."""
    note = load_spec(S2_SPEC)["plan_figure"]["figure_note"].replace("; LM20UU bushing (inside housing and lug)", "")
    return _s2_ctx(note=note)


def k4_b5():
    """Spec not_drawn gains a part the spec figure_note and the drawn note do not name (power-off brake)."""
    return _s2_ctx(spec_mut=lambda s: s["not_drawn"].append({"part": "power-off brake (Step 2)", "reason": "fixture"}))


# K5 plan (SW-17, TP-13)

def k5_b7():
    """SW-17: drill tube (cylinder, axis Z) drawn as a rectangle in plan."""
    def fn(c):
        r = c.P.get("drill.tube_od") / 2
        return [Rectangle((-r, -r), 2 * r, 2 * r, fill=False)]
    return _s2_replace(_s2_ctx(), "drill_tube", fn)


def k5_b8():
    """TP-13: radial-axis NEMA 23 (motor23_a, theta 210) drawn as a circle in plan."""
    def fn(c):
        pl = _s2_place(c, "motor23_a")
        return [Circle((pl["r_c"] * check_stack.cosd(pl["theta"]), pl["r_c"] * check_stack.sind(pl["theta"])), pl["half_width"], fill=False)]
    return _s2_replace(_s2_ctx(), "motor23_a", fn)


def k5_b9():
    """TP-13: motor23_a drawn as its rectangle turned 10 deg about its centre (axis off radial)."""
    def fn(c):
        pl = _s2_place(c, "motor23_a")
        return [Polygon(check_stack.radial_corners(pl["r_in"], pl["r_out"], pl["theta"], pl["half_width"], 10), closed=True, fill=False)]
    return _s2_replace(_s2_ctx(), "motor23_a", fn)


def k5_b10():
    """TP-13 premise: radial-axis motor23_a with a round place footprint (axis X needs a radial footprint)."""
    return _s2_ctx(spec_mut=_mut_row("motor23_a", lambda r: r.__setitem__("place", dict(r["place"], footprint="round"))))


def k5_b11():
    """Hub admission premise: pinion_a hub rectangle drawn 5 mm outboard of the heel (gap between teeth and hub)."""
    def fn(c):
        pl = _s2_place(c, "pinion_a")
        heel, w = c.P.get("pinion.r_heel"), pl["half_width"]
        return [Polygon(_radial_poly(pl["r_in"], heel, pl["theta"], w * pl["r_in"] / heel, w), closed=True, fill=False),
                Polygon(_radial_poly(heel + 5, pl["r_out"] + 5, pl["theta"], w / 2), closed=True, fill=False)]
    return _s2_replace(_s2_ctx(), "pinion_a", fn)


# K6 plan

def k6_b8():
    """K6 plan B: member c (frame_upper_c) drawn 6.75 off its spec centre in x (6.75 = collar.top_above_plate, the K6-B1
    offset)."""
    return _shift(_s2_ctx(), "frame_upper_c", Params().get("collar.top_above_plate"), 0)


def k6_b9():
    """K6 plan premise B (LF-16 owner rule, 1.2 (c)): S2 load_plane offset 1 (differs from S1's); core_seat is an S1 row
    only, so no spec with that row carries an equal load_plane. Stack lint only (no figure)."""
    P = Params()
    spec = load_spec(S2_SPEC)
    spec["load_plane"] = dict(spec["load_plane"], offset=1)
    return sc.Ctx(P=P, spec=spec, figs={}, stack=check_stack.evaluate_spec(P, spec), view=spec["view"], check_stack_path=CHECK_STACK_PATH)


# K7 plan (LF-8)

def _plan_rows(specs):
    """Plan fixture rows from (id, place, z band (z_A), neighbours [(id, class, g_min)], extra)."""
    rows = []
    for fid, place, z, nb, extra in specs:
        r = {"id": fid, "name": fid, "kind": extra.get("kind", "prism"), "axis": extra.get("axis", "Z"),
             "projection": extra.get("projection", "rectangle"), "z_rule": {"z_min": z[0], "z_max": z[1]}, "moves": extra.get("moves", False)}
        if place:
            r["place"] = place
        if extra.get("section"):
            r["section"] = extra["section"]
            r["depth"] = [-extra["section"][1], extra["section"][1]]
        r["neighbours"] = [{"id": b, "class": cls, "g_min": g, "source": "fixture"} for b, cls, g in (nb or [])]
        rows.append(r)
    return rows


def _k7_plan(specs, poses=None, plan_pose=None):
    """Plan K7 fixture: rows from _plan_rows, drawn faithfully by _s2_draw_row in one figure (one-figure mode: the
    figure serves every stack pose)."""
    P = Params()
    poses = poses or ONE
    spec = {"sketch": "k7plan", "view": "plan_xy", "poses": poses, "features": _plan_rows(specs),
            "plan_figure": {"pose": plan_pose or poses[0]["id"]}}
    stack = check_stack.evaluate_spec(P, spec)
    pid = spec["plan_figure"]["pose"]
    fig, ax = sc.setup_figure("plan_xy", title="k7 plan fixture")
    for row in spec["features"]:
        _s2_draw_row(ax, P, spec, stack, pid, row)
    sc.finish_axes(ax)
    return _ctx(P, spec, {pid: fig})


def _rad(r_in, r_out, th, w):
    return {"r_in": r_in, "r_out": r_out, "theta": th, "half_width": w, "footprint": "radial"}


def k7_z12():
    """Two 60 x 60 members at the same z, 100 apart in plan, declared F (states F)."""
    return _k7_plan([("a", _rad(200, 260, 0, 30), (0, 100), [("b", "F", 0)], {}),
                     ("b", _rad(360, 420, 0, 30), (0, 100), None, {})])


def k7_b22():
    """1 mm plan overlap on an F pair at the same z."""
    return _k7_plan([("a", _rad(200, 260, 0, 30), (0, 100), [("b", "F", 0)], {}),
                     ("b", _rad(259, 319, 0, 30), (0, 100), None, {})])


def k7_b23():
    """G pair (g_min 10) 9 apart in plan at the same z (g_min - 1)."""
    return _k7_plan([("a", _rad(200, 260, 0, 30), (0, 100), [("b", "G", 10)], {}),
                     ("b", _rad(269, 329, 0, 30), (0, 100), None, {})])


def k7_b24():
    """C pair touching in plan (faces at r 260) with z bands 100 apart (z-separated C)."""
    return _k7_plan([("a", _rad(200, 260, 0, 30), (0, 100), [("b", "C", 0)], {}),
                     ("b", _rad(260, 320, 0, 30), (200, 300), None, {})])


def k7_z13():
    """Plan C rule: a pad (r 200 to 215) standing on a post of the same footprint, z bands touching at 100, plan
    outlines overlapping in full: z-contact."""
    return _k7_plan([("pad", _rad(200, 215, 150, 30), (100, 110), [("post", "C", 0)], {}),
                     ("post", _rad(200, 215, 150, 30), (0, 100), None, {})])


def k7_b25():
    """Plan C rule B: the pad's z band reaches 1 mm into the post (z bands overlap 1, plan overlap): interference."""
    return _k7_plan([("pad", _rad(200, 215, 150, 30), (99, 110), [("post", "C", 0)], {}),
                     ("post", _rad(200, 215, 150, 30), (0, 100), None, {})])


def k7_b26():
    """Plan C premise B: a lift-motor-like part (round footprint r 29.70, drawn as its inscribed 42 square: a
    circumscribing outline) declared C on a plate below it, z touching, plan overlapping: z-contact refused."""
    return _k7_plan([("motor", {"r_in": 160, "theta": 30, "half_width": 29.6985, "footprint": "round"}, (100, 148), [("plate", "C", 0)], {}),
                     ("plate", _rad(120, 200, 30, 40), (88, 100), None, {})])


def k7_z14():
    """Plan annulus: ring annulus r 100 to 210 around a tube disk r 76.2 (undeclared F, z overlapping) with a bearing
    annulus r 76.2 to 100 in the bore (C to both): clean."""
    return _k7_plan([("ring", None, (0, 12), [("bearing", "C", 0)], {"kind": "plate", "projection": "circle", "section": [100, 210]}),
                     ("bearing", None, (-13, 12), [("tube", "C", 0)], {"kind": "cylinder", "projection": "circle", "section": [76.2, 100]}),
                     ("tube", {"r_in": 0, "theta": 0, "half_width": 76.2, "footprint": "round"}, (-200, 400), None,
                      {"kind": "cylinder", "projection": "circle"})])


def k7_b27():
    """Plan annulus B: bearing OD 1 mm into the ring bore (bearing r 76.2 to 101; C to the ring): interference."""
    return _k7_plan([("ring", None, (0, 12), [("bearing", "C", 0)], {"kind": "plate", "projection": "circle", "section": [100, 210]}),
                     ("bearing", None, (-13, 12), [("tube", "C", 0)], {"kind": "cylinder", "projection": "circle", "section": [76.2, 101]}),
                     ("tube", {"r_in": 0, "theta": 0, "half_width": 76.2, "footprint": "round"}, (-200, 400), None,
                      {"kind": "cylinder", "projection": "circle"})])


def k7_b28():
    """One-figure premise B (4f): a moving arm whose place r_in reads the pose (r_in = 200 + tip / 10), drawn in the one
    plan figure; its plan outline differs between the four poses."""
    rows = [("arm", {"r_in": "200 + tip / 10", "r_out": "260 + tip / 10", "theta": 0, "half_width": 30, "footprint": "radial"},
             ("tip", "tip + 20"), None, {"moves": True})]
    return _k7_plan(rows, poses=FOUR)


def k7_b29():
    """Swept case in one-figure mode: a fixed bar inside the ring annulus outline (r 150 to 170 at theta 0, z 300 to
    310) with its z band inside the ring's sweep (tip + 100 to tip + 120 over tips 0 to 500) and clear of every pose."""
    rows = [("ring", None, ("tip + 100", "tip + 120"), [("bar", "G", 10)],
             {"kind": "plate", "projection": "circle", "section": [100, 210], "moves": True}),
            ("bar", _rad(150, 170, 0, 10), (300, 310), None, {})]
    return _k7_plan(rows, poses=FOUR)


# K8 plan

def k8_b18():
    """K8-B3 on the S2 axes: the live S2 plan with the y axis inverted."""
    c = _s2_ctx()
    _s2_ax(c).invert_yaxis()
    return c


def k8_b19():
    """Plan handedness: the three screws drawn at -theta (azimuth order clockwise), everything else as the spec."""
    def mirror(fid):
        def fn(c):
            pl = _s2_place(c, fid)
            return [Circle((pl["r_c"] * check_stack.cosd(pl["theta"]), -pl["r_c"] * check_stack.sind(pl["theta"])), pl["half_width"], fill=False,
                           linestyle="--")]   # r2: dashed, so the mirrored screw under a pinion or motor is legal under K8 cover
        return fn
    c = _s2_ctx()
    for fid in ("screw_a", "screw_b", "screw_c"):
        _s2_replace(c, fid, mirror(fid))
    return c


def k8_b20():
    """Plan containment (premise of the K7 plan test): motor23_a drawn 10 wider each side across its axis."""
    def fn(c):
        pl = _s2_place(c, "motor23_a")
        return [Polygon(check_stack.radial_corners(pl["r_in"], pl["r_out"], pl["theta"], pl["half_width"] + 10), closed=True, fill=False)]
    return _s2_replace(_s2_ctx(), "motor23_a", fn)


def k8_b21():
    """Outboard (radial form): NEMA 23 c placed inboard of its pinion (motor23_c r 20 to 96, drawn faithfully)."""
    return _s2_ctx(spec_mut=_mut_row("motor23_c", lambda r: r.__setitem__(
        "place", dict(r["place"], r_in="pinion.motor_r_in - 122", r_out="pinion.motor_r_in - 122 + pinion.motor_length"))))


def k8_b22():
    """Taper (plan, radial frame): pinion_a toothed trapezoid drawn widening toward the axis (toe full width, heel
    narrow); hub as drawn."""
    def fn(c):
        pl = _s2_place(c, "pinion_a")
        heel, w = c.P.get("pinion.r_heel"), pl["half_width"]
        return [Polygon(_radial_poly(pl["r_in"], heel, pl["theta"], w, w * pl["r_in"] / heel), closed=True, fill=False),
                Polygon(_radial_poly(heel, pl["r_out"], pl["theta"], w * pl["r_in"] / heel / 2), closed=True, fill=False)]
    return _s2_replace(_s2_ctx(), "pinion_a", fn, render=True)   # 1.3 P1R: the taper alone is planted


def k8_b23():
    """Sector premise (S2-5a reads the drawn sector): operator sector drawn with half-angle 40, spec 45."""
    def fn(c):
        sec = dict(c.stack["poses"][_s2_pose(c.spec)]["features"]["operator_sector"]["sector"], half_angle=40)
        return [Polygon(sc.sector_boundary(sec)[:-6], closed=True, fill=False)]
    return _s2_replace(_s2_ctx(), "operator_sector", fn)


def _annulus_row(fid, d_in=0.0, d_out=0.0):
    """Drawing-only: row fid (a section annulus) drawn as an Annulus about the axis with its inner radius moved d_in and
    its outer radius moved d_out; the spec section unchanged."""
    def fn(c):
        names = c.stack["poses"][_s2_pose(c.spec)]["vars_z_A"]
        row = next(r for r in c.spec["features"] if r["id"] == fid)
        a, b = sorted(check_stack.eval_expr(e, c.P, names) for e in row["section"])
        a, b = a + d_in, b + d_out
        return [Annulus((0, 0), b, b - a, fill=False)]
    return _s2_replace(_s2_ctx(), fid, fn)


def k8_b25():
    """SW 1.2 (c) FIX 1 (4g annulus containment): gear drawn with outer radius OD / 2 + 5 (section r 90 to 126.32)."""
    return _annulus_row("gear", d_out=5)


def k8_b26():
    """SW 1.2 (c) FIX 1 (4g annulus containment): bearing drawn with its bore radius 5 under its section."""
    c = _annulus_row("bearing", d_in=-5)
    for a in sc.tagged(_s2_ax(c)).get("bearing", []):   # r2: the bearing is hidden under the gear and hub (K8 cover)
        a.set_linestyle("--")
    return c


def k8_b27():
    """SW 1.2 (c) FIX 2 (sector equality, wider direction): operator sector drawn at half-angle 50, spec 45; drawn
    points 400 sin 5 = 34.86 outside the wedge."""
    def fn(c):
        sec = dict(c.stack["poses"][_s2_pose(c.spec)]["features"]["operator_sector"]["sector"], half_angle=50)
        return [Polygon(sc.sector_boundary(sec)[:-6], closed=True, fill=False)]
    return _s2_replace(_s2_ctx(), "operator_sector", fn)


def k5_b13():
    """SW 1.2 (c) FIX 5 (TP-13 hub width): pinion_a hub drawn on the heel edge with half-width w + 5 (wider than the
    heel half-width w); teeth as the spec."""
    def fn(c):
        pl = _s2_place(c, "pinion_a")
        heel, w = c.P.get("pinion.r_heel"), pl["half_width"]
        return [Polygon(_radial_poly(pl["r_in"], heel, pl["theta"], w * pl["r_in"] / heel, w), closed=True, fill=False),
                Polygon(_radial_poly(heel, pl["r_out"], pl["theta"], w + 5), closed=True, fill=False)]
    return _s2_replace(_s2_ctx(), "pinion_a", fn)


def s2_6_b2():
    """SW 1.2 (c) FIX 3 (S2-6 notch clearance): member c drawn 2 toward the plate edge in the notch (3.00 against
    notch_clear 5); drawing only."""
    return _shift(_s2_ctx(), "frame_upper_c", 2, 0)


def k7_b30():
    """Loftsman 1.2 (c) FIX LF-c1: the K7-B29 bar (fixed, r 150 to 170 at theta 0, z 300 to 310, inside the ring annulus
    and inside its sweep, clear at all four poses) declared G 10 against the ring at capture_end (p4) only. The pair is
    undeclared at every swept position, so it is swept as F and fires."""
    rows = [("ring", None, ("tip + 100", "tip + 120"), [("bar", "G", 10)],
             {"kind": "plate", "projection": "circle", "section": [100, 210], "moves": True}),
            ("bar", _rad(150, 170, 0, 10), (300, 310), None, {})]
    c = _k7_plan(rows, poses=FOUR)
    c.spec["features"][0]["neighbours"][0]["poses"] = ["p4"]
    return c


# X1 shared-row lint (Loftsman 1.2 (b) section 2)

def _x1(mut=None):
    import check_sketch
    specs = {"s1": load_spec(HERE.parent / "s1_spec.yaml"), "s2": load_spec(S2_SPEC)}
    if mut:
        mut(specs["s2"])
    return check_sketch.x1_lint(specs)


def x1_z():
    return _x1()


def x1_b1():
    """s2 frame_upper_b place r_in + 1."""
    return _x1(_mut_row("frame_upper_b", lambda r: r.__setitem__("place", dict(r["place"], r_in="frame_upper.radius - profile.width / 2 + 1"))))


def x1_b2():
    """s2 nut_a z_rule z_max changed (nut length doubled upward)."""
    return _x1(_mut_row("nut_a", lambda r: r.__setitem__("z_rule", dict(r["z_rule"], z_max="nut_z + jackscrew.nut_length"))))


# S2-x fixtures from the signed spec (gameplan detail 1.2 table)

def s2_1_b1():
    """S2-1 B: screw_b (spec theta 30) drawn at 110 deg; nut, housing and blocks unchanged."""
    def fn(c):
        r, w = c.P.get("jackscrew.pitch_radius"), c.P.get("jackscrew.nominal") / 2
        return [Circle((r * check_stack.cosd(110), r * check_stack.sind(110)), w, fill=False)]
    return _s2_replace(_s2_ctx(), "screw_b", fn)


def s2_2_b1():
    """S2-2 B: screw pitch radius equal to the keep-out radius (jackscrew.pitch_radius = icd.keepout_radius), drawn
    faithfully."""
    return _s2_ctx(values={"jackscrew.pitch_radius": Params().get("icd.keepout_radius")})


def s2_3_b1():
    """S2-3 B: pinions placed on the gear OD (pinion.r_heel = gear.od / 2), drawn faithfully."""
    return _s2_ctx(values={"pinion.r_heel": Params().get("gear.od") / 2})


def s2_4_b1():
    """S2-4 B: collet axis (datum B cross) drawn 2 mm off in x."""
    return _shift(_s2_ctx(), "collet_axis", 2, 0)


def s2_5a_b1():
    """S2-5a B: sector widened to 130 deg (operator.sector_half_angle 65), wider than the 120 deg screw gap, drawn
    faithfully."""
    return _s2_ctx(values={"operator.sector_half_angle": 65})


def s2_5b_b1():
    """S2-5b B: NEMA 23 at theta 90 (motor23_c) with its bottom at 930 z_A at load (spec z_rule), 10 below the hand-band
    top 940."""
    return _s2_ctx(spec_mut=_mut_row("motor23_c", lambda r: r.__setitem__("z_rule", {"z_min": 930, "z_max": "930 + pinion.motor_body"})))


def s2_5b_b2():
    """S2-5b B2 (Topologist 1.2 (e) FIX TP1.2-3): drill_head with its tip at the hand-band top + 5 (945 z_A) at load
    (spec z_rule), drawn faithfully. drill_head moves and enters the sector; it is on no hand list."""
    return _s2_ctx(spec_mut=_mut_row("drill_head", lambda r: r.__setitem__("z_rule", {"z_min": 945, "z_max": "945 + drill.head_length"})))


def s2_6_b1():
    """S2-6 B: member c at radius 300 (26 off the plate edge), drawn faithfully."""
    return _s2_ctx(spec_mut=_mut_row("frame_upper_c", lambda r: r.__setitem__("place", dict(
        r["place"], r_in="300 - profile.width / 2", r_out="300 + profile.width / 2"))))


def s2_full_draw():
    """Smoke: every S2 spec row drawn from check_stack values; K1 to K9 and S2-1 to S2-6 run."""
    return _s2_ctx(), checks_s2.run


# ---------------------------------------------------------------- M1 reviewer control figures (gameplan detail 1, M1 controls)

def _plan_control(mirror=False, title="plan control figure"):
    """O5 plan control: the mini plan spec (drill tube, three screws at jackscrew.angle), screw labels with their spec
    azimuths, +X / +Y arrows and the theta arrow counter-clockwise. mirror: the same drawing reflected in y (screws at
    -theta, theta arrow clockwise, +Y arrow pointing down the page), same labels and title."""
    P = Params()
    fig, ax = sc.setup_figure("plan_xy", title=title)
    k = -1 if mirror else 1
    sc.draw("drill_tube", Circle((0, 0), P.get("drill.tube_od") / 2, fill=False), ax)
    r = P.get("jackscrew.pitch_radius")
    for i, s in enumerate("abc"):
        th = P.get("jackscrew.angle")[i]
        x, y = r * check_stack.cosd(th), k * r * check_stack.sind(th)
        sc.draw(f"screw_{s}", Circle((x, y), P.get("jackscrew.nut_flange_od") / 2, fill=False), ax)
        ax.annotate(f"screw {s}, theta {th:g} deg", xy=(x, y), xytext=(x * 1.25, y * 1.25), fontsize=8)
    L = r * 1.4
    ax.annotate("", xy=(L, 0), xytext=(0, 0), arrowprops={"arrowstyle": "->"})
    ax.annotate("+X", xy=(L, 0), fontsize=9)
    ax.annotate("", xy=(0, k * L), xytext=(0, 0), arrowprops={"arrowstyle": "->"})
    ax.annotate("+Y", xy=(0, k * L), fontsize=9)
    arc = [(0.5 * r * check_stack.cosd(a), k * 0.5 * r * check_stack.sind(a)) for a in range(0, 91, 5)]
    ax.add_line(Line2D([p[0] for p in arc], [p[1] for p in arc]))
    ax.annotate("", xy=arc[-1], xytext=arc[-2], arrowprops={"arrowstyle": "->"})
    ax.annotate("theta", xy=arc[9], fontsize=9)
    ax.set_xlim(-1.6 * r, 1.6 * r)
    ax.set_ylim(-1.6 * r, 1.6 * r)
    return fig


# M1 reviewer control figures by role (1.4 step 0 R3, Step 1.3 gate G2): {role: (figure, judging criterion, expected
# verdict)}. File names and tokens belong to check_sketch.py --m1-controls; this module names no file.
CONTROL_ROLES = {
    "side_drill_tip_up": ("rubric V3, kept-part and drill orientation (the K8-B1 figure: drill flipped tip-up)", "FAIL"),
    "side_correct": ("rubric V3, kept-part and drill orientation (the K8-Z figure: correct sense)", "PASS"),
    "plan_ccw": ("plan handedness (mini spec, screws counter-clockwise from +X at their jackscrew.angle azimuths)", "PASS"),
    "plan_mirrored": ("plan handedness (the same plan mirrored in y, azimuths clockwise)", "FAIL"),
}


def control_figures():
    """The four M1 reviewer control figures, {role: (figure, criterion, expected verdict)}: the mini side view drawn
    correctly and with the drill flipped tip-up (same title text), and the mini plan drawn correctly and mirrored in y
    (same title text) (1.2 (c), O5; 1.4 step 0 R3)."""
    P = Params()
    spec = mini_side_spec()
    stack = check_stack.evaluate_spec(P, spec)
    title = "control figure"
    z = draw_mini(P, spec, stack, title=title)
    b1 = draw_mini(P, spec, stack, mutate=_flip_drill(P, stack, spec["poses"][0]["id"]), title=title)
    figs = {"side_drill_tip_up": list(b1.values())[0], "side_correct": list(z.values())[0],
            "plan_ccw": _plan_control(), "plan_mirrored": _plan_control(mirror=True)}
    return {r: (figs[r], crit, verdict) for r, (crit, verdict) in CONTROL_ROLES.items()}


# ---------------------------------------------------------------- 1.2 (h) r2 (research/sean/cr_scratch/step1.2_engineer_revision_r2.md)
# Designer M1 r1 F1 (gear ticks: K5 admission, K8 ticks_radial), F2 (K8 cover, raised as TP1.2-9), F4 (leader on ink),
# F5 (leaders do not cross); S1 r5 F1 (K3 text inside the saved image); Loftsman LF1.2-1 (K7 record), LF1.2-2
# (pinion|gear_hub G 3); Topologist TP1.2-3 (S2-5b over every moving row).

S1_SPEC = HERE.parent / "s1_spec.yaml"


_DRAW_CACHE = {}   # 1.4 step 0 R1 e: unmutated live drawings per worker process, pickled; every call gets a fresh copy


def _fingerprint(mod):
    """Identity of every callable a module holds: a fixture that patches one (k8_b51 patches s2_plan._style_visible)
    changes the fingerprint, so draw_cache neither serves it a drawing made without the patch nor keeps its drawing for
    others."""
    d = mod if isinstance(mod, dict) else vars(mod)
    return tuple(sorted((k, id(v)) for k, v in d.items() if callable(v)))


def draw_cache(name, files, make, mods=()):
    """(P, spec, stack, figs) from make(), cached per process under name, the SHA-256 of files (params.yaml, the overlay,
    the spec, the drawing script) and the fingerprints of sketch_common, check_stack, this module and mods (the drawing
    modules); each call returns an independent copy (pickle round trip, an Agg canvas re-attached to every figure), so a
    control that mutates its copy never reaches another control's. Used only for drawings made with no spec_mut, values
    or skip; a mutate step runs on the copy after it is returned. Controls rows are equal to the uncached run (1.4 step 0
    R1 e)."""
    import hashlib
    import pickle
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from sketch_loader import default_overlay_path, default_params_path
    key = (name,) + tuple(hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in
                          [default_params_path(), default_overlay_path()] + [Path(f) for f in files])
    key += tuple(_fingerprint(m) for m in (sc, check_stack, globals()) + tuple(mods))
    blob = _DRAW_CACHE.get(key)
    if blob is None:
        blob = pickle.dumps(make(), protocol=pickle.HIGHEST_PROTOCOL)
        _DRAW_CACHE[key] = blob
    P, spec, stack, figs = pickle.loads(blob)
    for f in figs.values():
        FigureCanvasAgg(sc.real_figure(f))
    return P, spec, stack, figs


def _script_ctx(s, spec_mut=None, script_paths=None):
    """Live sketch drawn by its own script (s1_side_poses.py or s2_plan.py build), the drawing of record. With no
    spec_mut the drawing comes from draw_cache (one build per worker, a fresh copy per call)."""
    import importlib
    name = {"s1": "s1_side_poses", "s2": "s2_plan", "s3": "s3_jackscrew_section", "s4": "s4_base_section"}[s]
    mod = importlib.import_module(name)

    def make():
        P = Params()
        spec = load_spec(HERE.parent / f"{s}_spec.yaml")
        if spec_mut:
            spec_mut(spec)
        stack = check_stack.evaluate_spec(P, spec)
        return P, spec, stack, mod.build(P, spec, stack)
    if spec_mut is None:
        P, spec, stack, figs = draw_cache(f"script {s}", [HERE.parent / f"{s}_spec.yaml", HERE.parent / f"{name}.py"], make, mods=(mod,))
    else:
        P, spec, stack, figs = make()
    paths = [HERE.parent / f"{name}.py"] if script_paths is None else script_paths
    return sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], script_paths=paths, check_stack_path=CHECK_STACK_PATH)


# K3 text inside the saved image (Designer M1 S1 r5 F1)

def k3_z2():
    """Live S1 load as drawn by s1_side_poses.py, held to the canvas (no script, so no tight premise): every text inside."""
    c = _script_ctx("s1", script_paths=[])
    c.figs = {"load": c.figs["load"]}
    return c


def k3_b8():
    """Live S1 park as drawn at r5, held to the canvas (r5 saved the canvas): the figure-note line under the park-rule
    note runs below the image (Designer M1 S1 r5 F1)."""
    c = _script_ctx("s1", script_paths=[])
    c.figs = {"park": c.figs["park"]}
    return c


def k3_z3():
    """Premise Z: live S1, all four poses, with s1_side_poses.py (every savefig passes bbox_inches="tight"): clean."""
    return _script_ctx("s1")


def k3_b9():
    """Premise B: live S1 park with the script list holding one savefig without bbox_inches="tight" (a temporary copy of
    the r5 save line beside the r6 script): the canvas governs and the park note runs out."""
    tmp = Path(tempfile.mkdtemp()) / "s1_r5_save.py"
    tmp.write_text("def save(fig, path):\n    fig.savefig(path)\n", encoding="utf-8")
    c = _script_ctx("s1", script_paths=[HERE.parent / "s1_side_poses.py", tmp])
    c.figs = {"park": c.figs["park"]}
    return c


# K4 leaders (Designer M1 r1 F4, F5)

def k4_z3():
    """Live S2 as drawn by s2_plan.py: every leader ends on its part, no two cross."""
    return _script_ctx("s2")


def k4_b7():
    """F4 B: live S2, the sightline label anchored where r1 put it, (max x, mid y) = (200.00, 173.21), off the line."""
    c = _script_ctx("s2")
    ax = _s2_ax(c)
    t = next(t for t in ax.texts if t.get_gid() == "label:sightline_f6")
    pts = [p for poly in sc.pieces(ax, "sightline_f6") for p in poly]
    t.xy = (max(p[0] for p in pts), (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2)
    return c


def k4_b8():
    """F5 B: live S2 with two concentric labels at the r1 anchors (r, 0) on y = 0 (drill_tube 76.2, keepout 86.2) and
    their texts in reverse radial order below the anchors (inner label 10 above the outer): the leaders cross. 1.3 P1R
    re-plant (label_theta removal no longer crosses under the placer); P1Rf: text heights planted, not exchanged, so the
    crossing does not depend on where the placer puts the two texts."""
    c = _script_ctx("s2")
    ax = _s2_ax(c)
    t = {g: next(x for x in ax.texts if x.get_gid() == f"label:{g}") for g in ("drill_tube", "keepout")}
    for g in t:
        t[g].xy = (max(q[0] for poly in sc.pieces(ax, g) for q in poly), 0.0)
    xc = t["drill_tube"].xyann[0]
    yo = min(t[g].xyann[1] for g in t) - 20
    t["keepout"].xyann = (xc, yo)
    t["drill_tube"].xyann = (xc, yo + 10)
    return c


# K5 tick admission and K9 sub-gid (Designer M1 r1 F1)

def _gear_ticks_pr(c):
    return next(p for p in next(r for r in c.spec["features"] if r["id"] == "gear")["sense"] if p["pred"] == "ticks_radial")


def _replace_ticks(c, artists):
    ax = _s2_ax(c)
    for a in sc.tagged(ax).get("gear" + sc.TICKS_SUFFIX, []):
        a.remove()
    for a in artists:
        sc.draw("gear" + sc.TICKS_SUFFIX, a, ax)
    return c


def k5_b14():
    """Gear ticks drawn as one Line2D under gid gear:ticks (not a LineCollection)."""
    c = _s2_ctx()
    segs = _ticks(c.P, _gear_ticks_pr(c)).get_segments()
    xs, ys = [], []
    for (p, q) in segs:
        xs += [p[0], q[0]]
        ys += [p[1], q[1]]
    return _replace_ticks(c, [Line2D(xs, ys, linestyle="--")])


def k5_b15():
    """Gear ticks drawn while the gear row carries no ticks_radial predicate (premise unenforced)."""
    pr = {}

    def mut(spec):
        row = next(r for r in spec["features"] if r["id"] == "gear")
        pr.update(next(p for p in row["sense"] if p["pred"] == "ticks_radial"))
        row["sense"] = []
    c = _s2_ctx(spec_mut=mut)
    sc.draw("gear" + sc.TICKS_SUFFIX, _ticks(c.P, pr), _s2_ax(c))
    return c


def k5_b16():
    """Two tick LineCollections under gear:ticks (the set drawn twice)."""
    c = _s2_ctx()
    sc.draw("gear" + sc.TICKS_SUFFIX, _ticks(c.P, _gear_ticks_pr(c)), _s2_ax(c))
    return c


def k9_b6():
    """A tick sub-artist under gid gear2:ticks, a row the spec does not have."""
    c = _s2_ctx()
    sc.draw("gear2" + sc.TICKS_SUFFIX, _ticks(c.P, _gear_ticks_pr(c)), _s2_ax(c))
    return c


# K8 ticks_radial (premise of the tick admission)

def k8_b29():
    """Tick 0 turned 90 deg about its midpoint (tangential)."""
    c = _s2_ctx()
    return _replace_ticks(c, [_ticks(c.P, _gear_ticks_pr(c), turn=(0, 90))])


def k8_b30():
    """Tick 0 runs 5 past the heel (r_out gear.pitch_diameter / 2 + 5); the other ticks as drawn."""
    c = _s2_ctx()
    pr = _gear_ticks_pr(c)
    segs = [list(s) for s in _ticks(c.P, pr).get_segments()]
    r1 = check_stack.eval_expr(pr["r_out"], c.P, {}) + 5
    segs[0] = [tuple(segs[0][0]), (r1, 0.0)]
    return _replace_ticks(c, [LineCollection(segs, linestyles="--")])


def k8_b31():
    """gear.tooth_count - 1 ticks drawn."""
    c = _s2_ctx()
    pr = _gear_ticks_pr(c)
    n = int(round(check_stack.eval_expr(pr["count"], c.P, {}))) - 1
    return _replace_ticks(c, [_ticks(c.P, pr, n=n)])


# K8 cover (Designer M1 r1 F2 rule; Topologist TP1.2-2, TP1.2-9)

def k8_b32():
    """nut_a drawn solid (brass fill, solid edge) under guide_a, as at r1."""
    def fn(c):
        pl = _s2_place(c, "nut_a")
        th = pl["theta"]
        return [Circle((pl["r_c"] * check_stack.cosd(th), pl["r_c"] * check_stack.sind(th)), pl["half_width"], fill=True)]
    return _s2_replace(_s2_ctx(), "nut_a", fn)


def _cover_premise(motor_projection):
    """A pad (r 182 to 186 at theta 30, half-width 3, z 0 to 50) drawn solid inside the circumscribing circle (r 29.70)
    of a higher motor (z 100 to 148, round footprint r_c 160) and outside its inscribed 42 square."""
    return _k7_plan([("motor", {"r_in": 160, "theta": 30, "half_width": 29.6985, "footprint": "round"}, (100, 148), [("pad", "F", 0)],
                      {"kind": "prism", "projection": motor_projection}),
                     ("pad", _rad(182, 186, 30, 3), (0, 50), None, {})])


def k8_z7():
    """Cover premise Z: the circumscribing circle of a motor drawn as its 42 square is no cover: the solid pad stays legal."""
    return _cover_premise("rectangle")


def k8_b33():
    """Cover premise contrast B: the same motor drawn as its circle (a true outline) covers the solid pad."""
    return _cover_premise("circle")


# K7 record (Loftsman LF1.2-1) and pinion|gear_hub G 3 (LF1.2-2)

def _k7_lint(c, mutate=None):
    r = sc.k7(c)
    if mutate:
        mutate(r)
    lint = sc.k7_record_issues(r)
    return {"id": "K7", "result": "fail" if lint else "pass", "reason": sc._summ(lint) if lint else
            f"{len(r['tests'])} test entries with pose, pair, class, state, z gap, distance, overlap, basis",
            "n_issues": len(lint), "measured": len(lint), "threshold": 0}


def k7_z16():
    """Record lint Z: live S2 K7 record, one entry per state with ids."""
    return _k7_lint(_s2_ctx(cache=True))


def k7_z17():
    """Record lint Z: live S1 K7 record."""
    return _k7_lint(_s1_ctx())


def k7_b32():
    """Record lint B: live S2 K7 record with the pair id dropped from entry 0."""
    def mut(r):
        r["tests"][0][1] = None
    return _k7_lint(_s2_ctx(cache=True), mut)


def k7_b33():
    """pinion_a/_b/_c|gear_hub declared G g_min 6 (toe gap 5.22): short at every pose."""
    def mut(spec):
        row = next(r for r in spec["features"] if r["id"] == "gear_hub")
        for nb in row["neighbours"]:
            if nb["id"].startswith("pinion_"):
                nb["g_min"] = 6
    return _s2_ctx(spec_mut=mut)


# S2-5b premise set (TP1.2-3); s2_5b_b2 above

def s2_5b_b3():
    """S2-5b spec with the r1 hand list (ring_parts) in place of parts: moves."""
    def mut(spec):
        spec["s2_checks"]["S2-5b"].pop("parts", None)
        spec["s2_checks"]["S2-5b"]["ring_parts"] = ["ring", "bearing", "gear"]
    return _s2_ctx(spec_mut=mut)


# ---------------------------------------------------------------- 1.2 (h) r3 (research/sean/cr_scratch/step1.2_engineer_revision_r3.md)
# Topologist TP1.2-13 (cover over-cover; converse: partly visible drawn dashed), Designer M1 S2 r2 F1 and S1 r6 F1
# (anchor under another row's area; leader under an area).

def k8_z8():
    """Live S2 drawn by s2_plan.py: hidden pieces dashed, partly visible dashed pieces split (solid copy under the fills)."""
    return _script_ctx("s2")


def k8_b34():
    """Partly visible part drawn dashed: live S2 script drawing with the base-frame solid copy removed (the +Y rail top in
    the column notch, 70 x 60, visible from +Z, drawn dashed only, as at r2)."""
    c = _script_ctx("s2")
    for a in sc.tagged(_s2_ax(c)).get("base_frame", []):
        if sc.is_solid(a) and sc.bbox(sc.artist_polys(a))[2] > 0:   # r4: the +Y rail copy only (the -Y copy is K8-B40)
            a.remove()
    return c


def k8_b35():
    """Stand-in premise: the ties without plan_style: stand_in are partly visible (topmost) and drawn dashed: fires."""
    def mut(spec):
        for r in spec["features"]:
            r.pop("plan_style", None)
    return _script_ctx("s2", spec_mut=mut)


def k8_b36():
    """TP1.2-13 probe p4: bar c (r 100 to 200, z 0 to 10) whose ends lie under a (r 95 to 120) and b (r 180 to 205), both
    z 0 to 100, middle 60 open, drawn dashed. On r2 (vertex samples) it read hidden; the interior grid finds the gap."""
    c = _k7_plan([("c", _rad(100, 200, 0, 5), (0, 10), [("a", "F", 0), ("b", "F", 0)], {}),
                  ("a", _rad(95, 120, 0, 10), (0, 100), None, {}),
                  ("b", _rad(180, 205, 0, 10), (0, 100), None, {})])
    for a in sc.tagged(next(iter(c.figs.values())).axes[0]).get("c", []):
        a.set_linestyle("--")
    return c


def k4_z4():
    """Live S1 drawn by s1_side_poses.py: every anchor on ink no other area covers, no leader under an area."""
    return _script_ctx("s1")


def k4_b9():
    """S1 r6 F1: the core 750 label at capture_end anchored where r6 put it, (max x, mid z) of the core: the end of its
    leader runs through the pinion and gear hatch."""
    c = _script_ctx("s1")
    ax = c.figs["capture_end"].axes[0]
    t = next(t for t in ax.texts if t.get_gid() == "label:core_750")
    pts = [p for poly in sc.pieces(ax, "core_750") for p in poly]
    t.xy = (max(p[0] for p in pts), (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2)
    c.figs = {"capture_end": c.figs["capture_end"]}
    return c


def k4_b11():
    """Anchor premise: a filled area of another row (gid ring, 4 x 4, z order between the tube and the leaders) drawn
    over the tube OD label anchor."""
    c = _script_ctx("s2")
    ax = _s2_ax(c)
    t = next(t for t in ax.texts if t.get_gid() == "label:drill_tube")
    x, y = t.xy
    sc.draw("ring", Rectangle((x - 2, y - 2), 4, 4, fill=True, facecolor="white", zorder=sc.LEADER_ZORDER / 2), ax)
    return c


def k4_b10():
    """S2 r2 F1: a filled area (gid ring, 10 x 10) drawn above the leaders at the midpoint of the tube OD leader."""
    c = _script_ctx("s2")
    ax = _s2_ax(c)
    t = next(t for t in ax.texts if t.get_gid() == "label:drill_tube")
    mx, my = (t.xy[0] + t.xyann[0]) / 2, (t.xy[1] + t.xyann[1]) / 2
    sc.draw("ring", Rectangle((mx - 5, my - 5), 10, 10, fill=True, facecolor="white", zorder=sc.LEADER_ZORDER * 2), ax)
    return c


# ---------------------------------------------------------------- 1.2 (h) r4 (research/sean/cr_scratch/step1.2_engineer_revision_r4.md)
# Designer sign-off r3 (plate outline: K5 admission, K8 outline_matches, K9 sub-gid); Topologist TP1.2-15 (no opaque fill
# over a solid copy), TP1.2-16 (grid step from the short side), TP1.2-17 (stand_in needs an owner).

def _replace_outline(c, ring, n=1, fill=False):
    ax = _s2_ax(c)
    for a in sc.tagged(ax).get("base_plate:outline", []):
        a.remove()
    for _ in range(n):
        sc.draw("base_plate:outline", Polygon(ring, closed=True, fill=fill), ax)
    return c


def _plate_ring(c):
    return _notch_ring(c.stack["poses"][_s2_pose(c.spec)]["features"]["base_plate"]["plan_pieces"])


def k8_b37():
    """outline_matches B1: the outline drawn as the plain 644 x 608 rectangle (notches missing)."""
    c = _s2_ctx()
    r = _plate_ring(c)
    x0, x1, y0, y1 = sc.bbox([r])
    return _replace_outline(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def k8_b38():
    """outline_matches B2: the -Y notch of the outline 5 deeper (notch floor y -239 drawn at -234)."""
    c = _s2_ctx()
    r = _plate_ring(c)
    y_floor = min(p[1] for p in r if p[1] > sc.bbox([r])[2] + 1e-6)
    return _replace_outline(c, [(x, y + 5 if abs(y - y_floor) < 1e-6 else y) for x, y in r])


def k5_b17():
    """Outline admission B3: two outline Polygons."""
    c = _s2_ctx()
    return _replace_outline(c, _plate_ring(c), n=2)


def k5_b18():
    """Outline admission B4: outline drawn while base_plate carries no outline_matches predicate."""
    c = _s2_ctx(spec_mut=_mut_row("base_plate", lambda r: r.__setitem__("sense", [])))
    return _replace_outline(c, _plate_ring(c))


def k9_b7():
    """An outline sub-artist under gid base_plate2:outline, a row the spec does not have."""
    c = _s2_ctx()
    sc.draw("base_plate2:outline", Polygon(_plate_ring(c), closed=True, fill=False), _s2_ax(c))
    return c


def k8_b39():
    """TP1.2-15: live S2 drawing with the operator sector fill opaque (alpha 1, as at r3): the rail-top solid copy in the
    +Y notch is drawn under it."""
    c = _script_ctx("s2")
    for a in sc.tagged(_s2_ax(c)).get("operator_sector", []):
        a.set_alpha(1.0)
    return c


def k8_b40():
    """TP1.2-16: live S2 drawing with the base-frame -Y rail solid copy removed: the two 5 x 60 rail strips beside member
    c in the -Y notch are visible and drawn dashed only (on r3 the 12 x 12 grid missed them and read the rail hidden)."""
    c = _script_ctx("s2")
    for a in sc.tagged(_s2_ax(c)).get("base_frame", []):
        if sc.is_solid(a) and sc.bbox(sc.artist_polys(a))[3] < 0:
            a.remove()
    return c


def k8_b41():
    """TP1.2-17: guide_tie_a keeps plan_style: stand_in without stand_in_owner: lint fires and the exemption is void."""
    return _script_ctx("s2", spec_mut=_mut_row("guide_tie_a", lambda r: r.pop("stand_in_owner", None)))


# ---------------------------------------------------------------- 1.3 step 0 (research/sean/cr_scratch/step1.3_engineer_step0.md)
# R2 (O2, Loftsman 1.2 (b) NOTE 2): K2 expr agreement lint and the member-top stack_ties; R5 (carried lints): TP1.1-9
# zero-area K5, TP1.2-18 stand_in_owner, Topologist 1.2 (c) NOTE 2 frame value, Loftsman 1.2 (c) NOTE 1 side sweep.

def _k2_overlay(values=None):
    """K2 on the live S1 spec and a temporary copy of the live overlay with values {key: value} replaced (leaf value
    only; expr and every other field kept). The copy is read once by Params and deleted."""
    src = sc.load_yaml(HERE.parent / "proposed_params.yaml")
    for k, v in (values or {}).items():
        node = src
        for part in k.split(".")[:-1]:
            node = node[part]
        node[k.split(".")[-1]]["value"] = v
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "proposed_params.yaml"
        p.write_text(yaml.safe_dump(src, sort_keys=False, allow_unicode=True), encoding="utf-8")
        P = Params(overlay_path=p)
    spec = load_spec(HERE.parent / "s1_spec.yaml")
    return sc.Ctx(P=P, spec=spec, overlay_path=p)


def k2_z2():
    """R2 Z: live overlay (expr on the DERIVED leaves) and live S1 spec: every expr leaf agrees within 0.05."""
    return _k2_overlay()


def k2_b4():
    """R2 B: jackscrew.length 950 with jackscrew.top_guide_z left at 1165: top_guide_z disagrees with its expr by 50.
    member_length and member_length_rail read top_guide_z (1165) and stay consistent: planted 1."""
    return _k2_overlay({"jackscrew.length": 950})


def k2_b5():
    """R2 B: frame_upper.member_length_rail 1230 against top_guide_z 1165 + profile.height 60 = 1225: planted 1."""
    return _k2_overlay({"frame_upper.member_length_rail": 1230})


def _tie_ctx(s, values):
    """K6 stack_ties on the live spec of sketch s with values {key: value} replaced before check_stack runs; no figures
    (the lint reads the spec rows' stack z, as K6-B7)."""
    P = Params()
    for k, v in values.items():
        P.leaves[k] = dict(P.leaves[k], value=v)
    spec = load_spec(HERE.parent / f"{s}_spec.yaml")
    stack = check_stack.evaluate_spec(P, spec)
    return sc.Ctx(P=P, spec=spec, figs={}, stack=stack, view=spec["view"], check_stack_path=CHECK_STACK_PATH)


def k6_b10():
    """R2 B: S1 with frame_upper.member_length 1200: members a and b top at 12 + 1200 = 1212 z_A against top_guide 1165 +
    profile.height 60 = 1225, 13.00 apart on each tie (planted 2). K2 fires on the same values too (member_length expr,
    a separate check, not counted here)."""
    return _tie_ctx("s1", {"frame_upper.member_length": 1200})


def k6_b11():
    """R2 B: S2 with frame_upper.member_length_rail 1210: member c top 1210 z_A against 1225, 15.00 apart (planted 1;
    K2 also fires on the rail expr, a separate check)."""
    return _tie_ctx("s2", {"frame_upper.member_length_rail": 1210})


def k5_b19():
    """TP1.1-9 B: live S1 with one zero-height Rectangle tagged drill_tube (cylinder row) at load."""
    c = _s1_ctx()
    ax = c.figs["load"].axes[0]
    z = c.stack["poses"]["load"]["features"]["drill_tube"]["z_min"]
    sc.draw_rect(ax, "drill_tube", -10, 10, z, z)
    return c


def k8_b42():
    """TP1.2-18 B: guide_tie_a stand_in_owner "tbd" (names no Step or sketch id): the lint fires and the exemption is
    void, so the tie's dashed piece also fires the cover converse (planted 2, as K8-B41)."""
    return _script_ctx("s2", spec_mut=_mut_row("guide_tie_a", lambda r: r.__setitem__("stand_in_owner", "tbd")))


def k8_b43():
    """Topologist 1.2 (c) NOTE 2 B: live S2 with frame "polar" on motor23_a's outboard predicate (plan reads any value as
    radial today): sense_lint reports the unknown value."""
    def fn(r):
        next(p for p in r["sense"] if p.get("pred") == "outboard")["frame"] = "polar"
    return _s2_ctx(spec_mut=_mut_row("motor23_a", fn))


def k7_b34():
    """Loftsman 1.2 (c) NOTE 1 B: the K7-B31 member (mid-stroke, inside the ring outline, clear of all four poses) with
    the pose-restricted declaration (G 10 at p4) written only on the fixed row; the ring lists no neighbour. The 1.2 side
    sweep read only the moving row's list and passed it; read from the fixed row, it is swept as F and fires."""
    c = _swept(400)
    ring, member = c.spec["features"]
    ring["neighbours"] = []
    member["neighbours"] = [{"id": "ring", "class": "G", "g_min": 10, "poses": ["p4"], "source": "fixture"}]
    return c



# ---------------------------------------------------------------- 1.3 P0f (research/sean/cr_scratch/step1.3_engineer_step0_fixes.md)
# Loftsman P0L FIX 1 (mandatory chain exprs); Topologist P0T FIX 1 (K5 thickness form, line under a part row) merged with
# Software Engineer P0S FIX 4 (zero-area Polygon): K5-B20 to B23.

def _k2_expr(key, expr, values):
    """K2 on a temporary overlay: the live overlay with key's expr replaced (None: removed) and values replaced."""
    src = sc.load_yaml(HERE.parent / "proposed_params.yaml")
    for k, v in values.items():
        node = src
        for part in k.split(".")[:-1]:
            node = node[part]
        node[k.split(".")[-1]]["value"] = v
    node = src
    for part in key.split(".")[:-1]:
        node = node[part]
    leaf = node[key.split(".")[-1]]
    if expr is None:
        leaf.pop("expr", None)
    else:
        leaf["expr"] = expr
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "proposed_params.yaml"
        p.write_text(yaml.safe_dump(src, sort_keys=False, allow_unicode=True), encoding="utf-8")
        P = Params(overlay_path=p)
    return sc.Ctx(P=P, spec=load_spec(HERE.parent / "s1_spec.yaml"), overlay_path=p)


def k2_b6():
    """Loftsman P0L FIX 1 B: top_guide_z without expr, jackscrew.length 950: the agreement lint has nothing to compare
    (0 issues on the P0 code, K6 ties green); the mandatory-expr rule fires once."""
    return _k2_expr("jackscrew.top_guide_z", None, {"jackscrew.length": 950})


def k2_b7():
    """Loftsman P0L FIX 1 B: top_guide_z expr rewritten to "jackscrew.anchor_z + 900" (1165, agrees with the stale
    value), jackscrew.length 950: the agreement lint reads 0 apart; the altered-expr rule fires once."""
    return _k2_expr("jackscrew.top_guide_z", "jackscrew.anchor_z + 900", {"jackscrew.length": 950})


def k5_b20():
    """Topologist P0T FIX 1 B (sliver): the live S1 script drawing with each anchor bearing line drawn as a rectangle of
    its own row 0.001 high (the r7 form raised from height 0; area over 40 x 0.001 mm2, above the P0 absolute 0.01
    threshold): the thickness test fires at 2 anchors x 4 poses. Re-planted at 1.3 P6: S1 r8 draws the line as the mark
    sub-artist anchor_<s>:line, so the sliver is added on that line."""
    c = _script_ctx("s1")
    for fig in c.figs.values():
        ax = fig.axes[0]
        for gid in ("anchor_a", "anchor_b"):
            for a in sc.tagged(ax).get(f"{gid}:line", []):
                (x0, z), (x1, _) = sc.artist_polys(a)[0][:2]
                sc.draw_rect(ax, gid, x0, x1, z, z + 0.001)
    return c


def k5_b21():
    """Topologist P0T FIX 1 B (round patch): live S2 fixture drawing with screw_a's Circle at radius 0."""
    c = _s2_ctx()
    for a in sc.tagged(_s2_ax(c)).get("screw_a", []):
        if isinstance(a, Circle):
            a.set_radius(0)
    return c


def k5_b22():
    """Topologist P0T FIX 1 (c) B: fixture S1 with nut_a's projection field deleted and a Line2D drawn under nut_a at
    load; the P0 projection compare has no expectation for a prism without projection and passes it."""
    c = _s1_ctx(spec_mut=_mut_row("nut_a", lambda r: r.pop("projection", None)))
    ax = c.figs["load"].axes[0]
    z = c.stack["poses"]["load"]["features"]["nut_a"]["z_min"]
    sc.draw("nut_a", Line2D([-10, 10], [z, z]), ax)
    return c


def k5_b23():
    """Software Engineer P0S FIX 4 B: a degenerate Polygon (three collinear vertices) tagged drill_tube (cylinder row) at
    load, fixture S1."""
    c = _s1_ctx()
    ax = c.figs["load"].axes[0]
    z = c.stack["poses"]["load"]["features"]["drill_tube"]["z_min"]
    sc.draw("drill_tube", Polygon([(-10, z), (0, z), (10, z)], closed=True, fill=False), ax)
    return c


# 1.3 P0f addendum (orchestrator ruling after the P0T / P0S re-checks): the Annulus branch of least_thickness.

def k5_b24():
    """Topologist P0T re-check FIX 1r (= Software Engineer P0S re-check FIX R1): the S2 script drawing with the
    drill_tube Annulus wall set to 0.001 at load (outer radius kept). 2A/P per ring would read about 38 mm; the radial
    width reads 0.001."""
    c = _script_ctx("s2")
    for a in sc.tagged(_s2_ax(c)).get("drill_tube", []):
        if isinstance(a, Annulus):
            a.set_width(0.001)
    return c


# ---------------------------------------------------------------- 1.3 P1R (research/sean/cr_scratch/step1.3_engineer_renderer.md)
# Plan hidden-line renderer (sc.render_plan) and leader placer (sc.place_plan_labels): K8 cover (2) partly covered drawn
# solid (N2), exact covered region (annulus, hollow disk, union; TP1.2-13), annulus samples by arc length and the alpha
# rule (TP1.2-19); K4 leader last quarter outside other true outlines (Design Notes 30) and UNPLACEABLE.

def _rplan(specs, render=True):
    """Synthetic plan (_k7_plan rows, unfilled solid outlines) with the renderer applied (render=False: the drawing as
    before 1.3 P1R, each piece solid and unsplit)."""
    c = _k7_plan(specs)
    if render:
        pid = next(iter(c.figs))
        sc.render_plan(c, c.figs[pid].axes[0], pid)
    return c


def _sec(a, b):
    return {"section": [a, b], "kind": "cylinder", "projection": "circle"}


_R_ANN = [("c", _rad(80, 160, 0, 5), (0, 10), None, {}), ("u", None, (0, 100), None, _sec(100, 130))]
_R_HOLLOW = [("c", _rad(10, 50, 30, 5), (0, 10), None, {}), ("t", None, (0, 100), None, _sec(40, 60))]
_R_UNION = [("c", _rad(100, 220, 0, 5), (0, 10), None, {}), ("a", _rad(95, 130, 0, 10), (0, 100), None, {}),
            ("b", _rad(120, 205, 0, 10), (0, 100), None, {})]
# TP1.2-19: ring r 100 to 110 under two half-plane covers (u >= 1.5 along 94.225 deg, u <= -1.5 along 274.225 deg):
# visible only in a 3 mm strip through the axis at 4.225 and 184.225 deg (1.56 to 1.72 deg of arc across the ring),
# between the outer-vertex sample directions of the r4 annulus sampling (every 2.8125 deg: 2.81, 5.63, 182.81, 185.63)
# and wider than the 1.30 deg step of the P1R arc-length sampling (2.5 mm at r 110)
_R_GAP = [("ring", None, (0, 10), None, _sec(100, 110)), ("p", _rad(1.5, 300, 94.225, 300), (0, 100), None, {}),
          ("q", _rad(1.5, 300, 274.225, 300), (0, 100), None, {})]


def k8_z9():
    """Annulus cover: bar r 80 to 160 crossing an annulus r 100 to 130 above it, rendered (split: visible 80 to 100 and
    130 to 160 solid, hidden 100 to 130 dashed)."""
    return _rplan(_R_ANN)


def k8_b44():
    """Annulus cover B: the same bar drawn solid and unsplit (as before the renderer)."""
    return _rplan(_R_ANN, render=False)


def k8_z10():
    """Hollow disk with its bore: bar r 10 to 50 at 30 deg under a hollow disk r 40 to 60 (section annulus), rendered:
    the part in the bore (10 to 40) visible solid, 40 to 50 hidden dashed."""
    return _rplan(_R_HOLLOW)


def k8_b45():
    """Hollow disk B: the same bar drawn solid and unsplit."""
    return _rplan(_R_HOLLOW, render=False)


def k8_z11():
    """Union of covers: bar r 100 to 220 under a (95 to 130) and b (120 to 205), which overlap, rendered: hidden 100 to 205
    as one union, visible 205 to 220."""
    return _rplan(_R_UNION)


def k8_b46():
    """Union B: the same bar drawn solid and unsplit."""
    return _rplan(_R_UNION, render=False)


def k8_z12():
    """TP1.2-19: ring visible only in two 3 mm strips, rendered (split)."""
    return _rplan(_R_GAP)


def k8_b47():
    """TP1.2-19 B: the ring drawn wholly dashed (the r4 annulus sampling read it hidden): its visible strips are shown by
    no solid piece."""
    c = _rplan(_R_GAP, render=False)
    for a in sc.tagged(next(iter(c.figs.values())).axes[0]).get("ring", []):
        a.set_linestyle("--")
    return c


def k8_b48():
    """N2 B: live S2 drawn by s2_plan.py with the renderer bypassed for the ring: its clip path removed and its hidden
    copy deleted, so the rim under the unfilled guide arms is drawn solid."""
    c = _script_ctx("s2")
    for a in sc.tagged(_s2_ax(c)).get("ring", []):
        if sc.is_solid(a):
            a.set_clip_path(None)
        else:
            a.remove()
    return c


def k8_b49():
    """TP1.2-19 alpha rule B: live S2 with the operator sector fill at alpha 0.95 (counts opaque): the plate it draws over
    is partly covered and drawn solid."""
    c = _script_ctx("s2")
    for a in sc.tagged(_s2_ax(c)).get("operator_sector", []):
        a.set_alpha(0.95)
    return c


def k8_b50():
    """Alpha rule premise B: live S2 with the operator sector fill at alpha 0.6 (neither opaque nor see-through)."""
    c = _script_ctx("s2")
    for a in sc.tagged(_s2_ax(c)).get("operator_sector", []):
        a.set_alpha(0.6)
    return c


def k4_b12():
    """Design Notes 30 B: live S2 r6 drawing with the descent-stop label put back on the r4/r5 leader: anchor at the pad
    outer corner t +30 (-201.20, 81.52), text in the left column at the anchor height (the r5 layout); the last 60.1 mm
    of the leader runs inside guide_tie_b."""
    c = _script_ctx("s2")
    ax = _s2_ax(c)
    pl = _s2_place(c, "descent_stop")
    corners = check_stack.radial_corners(pl["r_in"], pl["r_out"], pl["theta"], pl["half_width"], pl.get("rot", 0))
    anc = min(corners, key=lambda p: (p[0], p[1]))   # outer corner t +30: least x
    t = next(t for t in ax.texts if t.get_gid() == "label:descent_stop")
    ax.apply_aspect()
    (_, y0), (_, y1) = ax.transData.transform([(0, 0), (0, 1)])
    line = sc.LABEL_FONTSIZE * ax.figure.dpi / 72 * sc.LABEL_LINESPACING / abs(y1 - y0)
    t.xy = anc
    t.xyann = (ax.get_xlim()[0] - line, anc[1])
    t.set_ha("right")
    return c


def k4_b13():
    """UNPLACEABLE B: a pad (r 150 to 170 at 0 deg, z 0 to 10, labelled) wholly under a lid (r 140 to 180, half-width 20,
    z 0 to 100) drawn with an opaque fill above it: every anchor on the pad's ink lies under the lid's area, so no
    candidate passes and the placer records the label UNPLACEABLE."""
    c = _k7_plan([("pad", _rad(150, 170, 0, 5), (0, 10), None, {}), ("lid", _rad(140, 180, 0, 20), (0, 100), None, {})])
    next(r for r in c.spec["features"] if r["id"] == "pad")["label"] = {"text": "pad", "key": "drill.tube_od", "fmt": ".1f"}
    pid = next(iter(c.figs))
    ax = c.figs[pid].axes[0]
    for a in sc.tagged(ax).get("lid", []):
        a.set_fill(True)
        a.set_facecolor("white")
    sc.render_plan(c, ax, pid)
    sc.place_plan_labels(ax, c, pid, margin=False)
    return c


# ---------------------------------------------------------------- 1.3 P1Rf (research/sean/cr_scratch/step1.3_engineer_renderer_fixes.md)
# Topologist TP1.3-1 (annulus samples across the width), TP1.3-2 (K8 cover (5): an opaque fill hides only what lies behind
# it); Designer FIX D1 (rule (e1) visible ink, enclosure exemption, clause (g)) and D2 (label suffixes naming the cover).

_R_RADIAL = [("ring", None, (0, 10), None, _sec(100, 210)), ("d", _rad(135, 145, 0, 5), (0, 100), None, {})]


def _filled_ring(c):
    for a in sc.tagged(next(iter(c.figs.values())).axes[0]).get("ring", []):
        a.set_fill(True)
        a.set_facecolor("#c9dcef")
    return c


def k8_z13():
    """TP1.3-1 Z: filled ring r 100 to 210 under a higher 10 x 10 cover centred at r 140 (between the P1R sample radii
    127.5 and 155), rendered: split, the cover's square dashed."""
    c = _filled_ring(_k7_plan(_R_RADIAL))
    pid = next(iter(c.figs))
    sc.render_plan(c, c.figs[pid].axes[0], pid)
    return c


def k8_b52():
    """TP1.3-1 B: the same filled ring drawn solid and unsplit (the P1R renderer left it so: no sample under the cover)."""
    return _filled_ring(_k7_plan(_R_RADIAL))


def k8_b51():
    """TP1.3-2 B: live S2 with the operator sector fill at alpha 0.95 set in the style before the renderer: the sector (a
    zone, no z_max) is taken as an opaque cover and the plate pieces under it are dashed."""
    import importlib
    mod = importlib.import_module("s2_plan")
    orig = mod._style_visible

    def style(row):
        kw = orig(row)
        if row["id"] == "operator_sector":
            kw = dict(kw, alpha=0.95)
        return kw
    mod._style_visible = style
    try:
        return _script_ctx("s2")
    finally:
        mod._style_visible = orig


def k4_b14():
    """D1 (e1) B: live S2 with the ring label anchored at the P1R r6 point (209.75, -10.33), on the rim's hidden stretch
    inside guide_tie_a (the ring has visible ink)."""
    c = _script_ctx("s2")
    ax = _s2_ax(c)
    th = math.atan2(-10.325733190674836, 209.7459794887204)
    r = c.P.get("ring.od") / 2
    t = next(t for t in ax.texts if t.get_gid() == "label:ring")
    t.xy = (r * math.cos(th), r * math.sin(th))
    return c


def k4_b15():
    """D1 (g) B: live S2 with the drill_head label suffix removed (the label does not name its cover)."""
    return _script_ctx("s2", spec_mut=_mut_row("drill_head", lambda r: r["label"].pop("suffix", None)))


def k4_b16():
    """D1 (e2) B: live S2 r7 drawing judged with the gear outline planted as an open C (annulus 90 to 126.32 from -170 to
    170 deg in convex pieces): the C neither contains nor encloses the cutter-rim anchor at theta 0, and the drill_head
    leader's last quarter runs inside it."""
    c = _script_ctx("s2")
    row = next(r for r in c.spec["features"] if r["id"] == "gear")
    row.pop("section", None)
    a, b = 90.0, 126.32
    angs = [-170 + 10 * k for k in range(35)]
    pieces = []
    for t0, t1 in zip(angs[:-1], angs[1:]):
        c0, s0, c1, s1 = (math.cos(math.radians(t0)), math.sin(math.radians(t0)), math.cos(math.radians(t1)), math.sin(math.radians(t1)))
        pieces.append([(a * c0, a * s0), (b * c0, b * s0), (b * c1, b * s1), (a * c1, a * s1)])
    for pr in c.stack["poses"].values():
        if "gear" in pr["features"]:
            pr["features"]["gear"]["plan_pieces"] = pieces
    return c


# ---------------------------------------------------------------- 1.3 P1Rf2 (step1.3_engineer_renderer_fixes.md, section P1Rf2)
# Topologist TP1.3-8 (strict enclosure exemption), Designer FIX D5 (stand-in visible ink only where no cover contains
# it) and FIX D4 (K4 (h), leaders at least 4.0 mm apart).

def _set_label(ax, fid, xy, xytext=None):
    t = next(t for t in ax.texts if t.get_gid() == f"label:{fid}")
    t.xy = xy
    if xytext is not None:
        t.xyann = xytext
    return t


def k4_b17():
    """TP1.3-8 B: live S2 with the ring label anchored on visible rim at (201.76, 34.40), 0.028 mm outside guide_tie_a
    (inside the old +0.05 enclosure band), text at (366.84, 34.40): the last quarter runs 41.3 mm inside tie a."""
    c = _script_ctx("s2")
    _set_label(_s2_ax(c), "ring", (201.76, 34.40), (366.84, 34.40))
    return c


def _lid_row(c0):
    """Spec row 'lid': a disk r 8 above every part (z 1300 to 1310 z_S) centred on the midpoint of guide_tie_a's edge
    of greatest x mid-way in y (a nearer true outline over that stretch of the tie's phantom line)."""
    def mut(spec):
        spec["features"].append({"id": "lid", "name": "planted lid", "kind": "cylinder", "axis": "Z", "projection": "circle",
                                 "z_rule": {"z_min": 1300, "z_max": 1310}, "place": dict(c0, half_width=8, footprint="round"),
                                 "neighbours": [], "sense": [], "moves": False})
    return mut


def k4_b18():
    """D5 B: guide_tie_a's label anchored on its phantom line where a planted nearer outline (row lid, disk r 8, z 1300
    to 1310) covers it: (e1) fires. Red-first by deleting the cover term for stand-in artists in row_visibility."""
    c = _script_ctx("s2")
    ax = _s2_ax(c)
    pts = [p for poly in sc.pieces(ax, "guide_tie_a") for p in poly]
    xm = max(p[0] for p in pts)
    edge = sorted([p for p in pts if abs(p[0] - xm) < 10], key=lambda p: p[1])
    mid = ((edge[0][0] + edge[-1][0]) / 2, (edge[0][1] + edge[-1][1]) / 2)
    r, th = math.hypot(*mid), math.degrees(math.atan2(mid[1], mid[0]))
    c = _script_ctx("s2", spec_mut=_lid_row({"r_in": r, "r_out": r, "theta": th}))
    ax = _s2_ax(c)
    t = next(t for t in ax.texts if t.get_gid() == "label:guide_tie_a")
    ink = [(q, True) for q in sc.pieces(ax, "guide_tie_a")]
    best = min(((a[0] + (b[0] - a[0]) * k / 40, a[1] + (b[1] - a[1]) * k / 40) for poly, _ in ink for a, b in sc._edges(poly)
                for k in range(41)), key=lambda q: math.hypot(q[0] - mid[0], q[1] - mid[1]))
    t.xy = best
    return c


_R7 = {"drill_tube": ((76.1539, 1.8734), (366.8424, 1.8734)), "base_plate": ((322.0, 0.0), (366.8424, -17.0903)),
       "drill_head": ((88.9, 0.0), (366.8424, -36.0539))}   # S2 r7 placer record (anchor, text), MEASURED


def k4_b19():
    """D4 B: live S2 with drill_tube, base_plate and drill_head put back on their S2 r7 leaders: the tube OD leader runs
    1.87 mm above the cutter anchor and about 2.2 mm from the base plate leader start (h)."""
    c = _script_ctx("s2")
    ax = _s2_ax(c)
    for f, (xy, xt) in _R7.items():
        _set_label(ax, f, xy, xt)
    return c
