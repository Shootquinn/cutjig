"""Control fixtures for K1 to K9 (manifest.yaml). Each builder returns a sketch_common.Ctx or a list of them.

Figures are drawn from check_stack.py values (z_S, shop-floor frame) so a Z fixture is clean by construction;
each B builder plants exactly one defect on top of the matching Z drawing. K6-Z2 and K6-B4 anchor check_stack itself
to hand numbers written in manifest.yaml (LF-2). s1_full_draw draws every S1 spec row (SW-8 smoke control).
"""
import math
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import check_stack  # noqa: E402
import checks_s1  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params, load_spec  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402
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
             "sense": [{"pred": "mirror_about_axis", "axis": "drill_tube"}, {"pred": "taper", "narrows": "up"}]},
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
    return {"sketch": "taper", "view": "side_xz", "poses": [{"id": "fixture", "tip_z": 0}],
            "features": [{"id": "collet", "name": "collet", "kind": "cone", "axis": "Z", "projection": "trapezoid",
                          "keys": ["cone.alpha"], "sense": [{"pred": "taper", "narrows": "down"}]}]}


def taper_ctx(invert=False):
    P = Params()
    fig, ax = sc.setup_figure("side_xz", title="taper fixture")
    R, h = P.get("receiver.register_bore_radius"), P.get("collet.slit_length")
    t = h * math.tan(math.radians(P.get("cone.alpha")))
    z_narrow, z_wide = (h, 0) if invert else (0, h)
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
    """TP-2: gear section flipped, wide face at the top."""
    def gear(ax, fid, r_in, r_pitch, z0, z1):
        h = z1 - z0
        right = [(r_in, z0), (r_pitch, z0), (r_pitch + h / 2, z1), (r_in, z1)]
        sc.draw(fid, Polygon(right, closed=True, fill=False), ax)
        sc.draw(fid, Polygon([(-x, z) for x, z in right], closed=True, fill=False), ax)
    return mini_ctx(gear=gear)


def k8_b11():
    """TP-2: collet cone inverted."""
    return taper_ctx(invert=True)


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
        if fid == "keepout":
            r = P.get("icd.keepout_radius")
            for x in (-r, r):
                sc.draw(fid, Line2D([x, x], [z0, z1]), ax)
            continue
        if row["kind"] == "line":
            x0, x1 = f["depth"] if f.get("depth") else (-half_fp, half_fp)
            sc.draw_hline(ax, fid, x0, x1, z0)
            continue
        if row["kind"] == "gear" and row.get("axis") == "Z":
            sc.draw_gear_section(ax, fid, P.get("gear.bore") / 2, P.get("gear.pitch_diameter") / 2, z0, z1)
            continue
        x0, x1 = f["place"]["x"] if f.get("place") else f["depth"]
        if row["kind"] == "gear":
            inner, outer = (x0, x1) if abs(x0) < abs(x1) else (x1, x0)
            sc.draw_trap(ax, fid, inner, outer, (z1 - z0) / 2, z1 - z0, z0)
        elif row["kind"] == "cone":
            t = (z1 - z0) * math.tan(math.radians(P.get("cone.alpha")))
            sc.draw(fid, Polygon([(x0 + t, z0), (x1 - t, z0), (x1, z1), (x0, z1)], closed=True, fill=False), ax)
        else:
            sc.draw_rect(ax, fid, x0, x1, z0, z1)
    sc.place_labels(ax, spec, P, pid)
    sc.finish_axes(ax)
    return fig


def s1_full_ctx():
    P = Params()
    spec = load_spec(HERE.parent / "s1_spec.yaml")
    stack = check_stack.evaluate_spec(P, spec)
    figs = {p["id"]: _s1_draw_pose(P, spec, stack, p["id"]) for p in spec["poses"]}
    return sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], script_paths=[], check_stack_path=CHECK_STACK_PATH)


def s1_full_draw():
    """Returns (ctx, extra checks): K1 to K9 and S1-1 to S1-6 run on it."""
    return s1_full_ctx(), checks_s1.run


# ---------------------------------------------------------------- M1 reviewer control figures (gameplan detail 1, M1 controls)

def control_figures(out_dir):
    """K8 Z figure and K8 B1 (drill tip-up) figure, same title text. Returns the mapping written to key.json."""
    P = Params()
    spec = mini_side_spec()
    stack = check_stack.evaluate_spec(P, spec)
    title = "control figure"
    z = draw_mini(P, spec, stack, title=title)
    b1 = draw_mini(P, spec, stack, mutate=_flip_drill(P, stack, spec["poses"][0]["id"]), title=title)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    mapping = {"ctrl_a.png": "K8-B1 (drill flipped tip-up; must FAIL V3)", "ctrl_b.png": "K8-Z (correct sense; must PASS)"}
    list(b1.values())[0].savefig(out_dir / "ctrl_a.png")
    list(z.values())[0].savefig(out_dir / "ctrl_b.png")
    return mapping
