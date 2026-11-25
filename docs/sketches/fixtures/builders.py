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
        if fid == "keepout":
            r = P.get("icd.keepout_radius")
            for x in (-r, r):
                sc.draw(fid, Line2D([x, x], [z0, z1]), ax)
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
    sc.place_labels(ax, spec, P, pid)
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
    return _s1_ctx(spec_mut=lambda s: next(r for r in s["features"] if r["id"] == "holder").pop("bore_cone"))


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


def _s2_draw(P, spec, stack, skip=(), note=None):
    pid = _s2_pose(spec)
    fig, ax = sc.setup_figure(spec["view"], title=f"S2 plan fixture, pose {pid}")
    for row in spec["features"]:
        if row["id"] in skip or not sc.applies(row, pid):
            continue
        _s2_draw_row(ax, P, spec, stack, pid, row)
    sc.finish_axes(ax)
    sc.place_labels(ax, spec, P, pid)
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
    P = Params()
    for k, v in (values or {}).items():
        P.leaves[k] = dict(P.leaves[k], value=v)
    spec = load_spec(S2_SPEC)
    if spec_mut:
        spec_mut(spec)
    stack = check_stack.evaluate_spec(P, spec)
    figs = _s2_draw(P, spec, stack, skip=skip, note=note)
    ctx = sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], script_paths=[], check_stack_path=CHECK_STACK_PATH)
    if cache:
        _S2_LIVE["ctx"] = ctx
    return ctx


def s2_live():
    """Z for K4 to K9 in plan and S2-1 to S2-6: the signed S2 spec drawn faithfully."""
    return _s2_ctx(cache=True)


def _s2_ax(c):
    return next(iter(c.figs.values())).axes[0]


def _s2_replace(c, fid, artists_fn):
    """Remove every artist of row fid from the S2 plan figure and draw artists_fn(ctx) in its place (drawing-only B)."""
    ax = _s2_ax(c)
    for a in sc.tagged(ax).get(fid, []):
        a.remove()
    for a in artists_fn(c):
        sc.draw(fid, a, ax)
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
            return [Circle((pl["r_c"] * check_stack.cosd(pl["theta"]), -pl["r_c"] * check_stack.sind(pl["theta"])), pl["half_width"], fill=False)]
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
    return _s2_replace(_s2_ctx(), "pinion_a", fn)


def k8_b23():
    """Sector premise (S2-5a reads the drawn sector): operator sector drawn with half-angle 40, spec 45."""
    def fn(c):
        sec = dict(c.stack["poses"][_s2_pose(c.spec)]["features"]["operator_sector"]["sector"], half_angle=40)
        return [Polygon(sc.sector_boundary(sec)[:-6], closed=True, fill=False)]
    return _s2_replace(_s2_ctx(), "operator_sector", fn)


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


def control_figures(out_dir):
    """K8 Z figure and K8 B1 (drill tip-up) figure, same title text; plan controls ctrl_c (correct handedness) and ctrl_d
    (mirrored), same title text (1.2 (c), O5). Returns the mapping written to key.json."""
    P = Params()
    spec = mini_side_spec()
    stack = check_stack.evaluate_spec(P, spec)
    title = "control figure"
    z = draw_mini(P, spec, stack, title=title)
    b1 = draw_mini(P, spec, stack, mutate=_flip_drill(P, stack, spec["poses"][0]["id"]), title=title)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    mapping = {"ctrl_a.png": "K8-B1 (drill flipped tip-up; must FAIL V3)", "ctrl_b.png": "K8-Z (correct sense; must PASS)",
               "ctrl_c.png": "plan of the mini spec, screws counter-clockwise from +X at 30, 150, 270 (must PASS handedness)",
               "ctrl_d.png": "the same plan mirrored in y, azimuths clockwise (must FAIL handedness)"}
    list(b1.values())[0].savefig(out_dir / "ctrl_a.png")
    list(z.values())[0].savefig(out_dir / "ctrl_b.png")
    _plan_control().savefig(out_dir / "ctrl_c.png")
    _plan_control(mirror=True).savefig(out_dir / "ctrl_d.png")
    return mapping
