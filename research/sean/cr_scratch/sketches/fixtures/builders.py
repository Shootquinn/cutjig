"""Control fixtures for K1 to K9 (manifest.yaml). Each builder returns a sketch_common.Ctx or a list of them.

Figures are drawn from check_stack.py values (z_S, shop-floor frame) so a Z fixture is clean by construction;
each B builder plants exactly one defect on top of the matching Z drawing.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

CHECK_STACK_PATH = HERE.parent / "check_stack.py"


def _ctx(P, spec, figs, **kw):
    stack = check_stack.evaluate_spec(P, spec)
    kw.setdefault("check_stack_path", CHECK_STACK_PATH)
    return sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], **kw)


# ---------------------------------------------------------------- mini side spec (K4, K6, K8, K9, ctrl figs)

def mini_side_spec(pose="capture_end", tip="stop.height_z"):
    zr = lambda a, b: {"z_min": a, "z_max": b}  # noqa: E731
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
             "sense": [{"pred": "rests_on", "on": "core_seat", "tol": 0.05}]},
            {"id": "drill_head", "name": "drill head", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["drill.head_od", "drill.head_length"], "z_rule": zr("tip", "head_top"),
             "label": {"text": "cutter OD ASSUMED", "key": "drill.head_od", "fmt": ".1f"},
             "sense": [{"pred": "below", "of": "gear"}, {"pred": "below", "of": "drill_top_block"}]},
            {"id": "drill_tube", "name": "drill tube", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["drill.tube_od", "drill.length"], "z_rule": zr("head_top", "drill_top"),
             "label": {"text": "tube OD", "key": "drill.tube_od", "fmt": ".1f"}},
            {"id": "drill_top_block", "name": "top-end block", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["drill.top_block_od", "drill.top_block_length"], "z_rule": zr("drill_top", "top_block_top")},
            {"id": "ring", "name": "ring", "kind": "plate", "projection": "rectangle",
             "keys": ["ring.od", "ring.thickness", "ring.position_above_tip"], "z_rule": zr("ring_bottom", "ring_top")},
            {"id": "gear", "name": "ring gear", "kind": "gear", "axis": "Z", "projection": "trapezoid",
             "keys": ["gear.pitch_diameter", "gear.bore", "gear.face_width"], "z_rule": zr("ring_top", "gear_top"),
             "sense": [{"pred": "mirror_about_axis", "axis": "drill_tube"}]},
            {"id": "motor23_a", "name": "NEMA 23", "kind": "cylinder", "axis": "X", "projection": "rectangle",
             "keys": ["pinion.motor_body", "pinion.motor_length", "gear.pitch_diameter"],
             "z_rule": zr("ring_top", "ring_top + pinion.motor_body"), "sense": [{"pred": "above", "of": "ring"}]},
            {"id": "screw_a", "name": "jack screw", "kind": "screw", "axis": "Z", "projection": "rectangle",
             "keys": ["jackscrew.anchor_z", "jackscrew.top_guide_z", "jackscrew.nominal", "jackscrew.pitch_radius", "jackscrew.angle"],
             "z_rule": zr("jackscrew.anchor_z", "jackscrew.top_guide_z")},
            {"id": "anchor_a", "name": "anchor", "kind": "prism", "projection": "rectangle",
             "keys": ["jackscrew.anchor_z", "jackscrew.anchor_allowance"],
             "z_rule": zr("jackscrew.anchor_z", "jackscrew.anchor_z + jackscrew.anchor_allowance"),
             "sense": [{"pred": "below", "of": "nut_a"}]},
            {"id": "nut_a", "name": "nut", "kind": "prism", "projection": "rectangle",
             "keys": ["jackscrew.nut_length", "jackscrew.nut_flange_od"],
             "z_rule": zr("nut_z - jackscrew.nut_length / 2", "nut_z + jackscrew.nut_length / 2"),
             "sense": [{"pred": "below", "of": "guide_a"}]},
            {"id": "guide_a", "name": "top guide", "kind": "prism", "projection": "rectangle",
             "keys": ["jackscrew.top_guide_z", "jackscrew.guide_allowance"],
             "z_rule": zr("jackscrew.top_guide_z - jackscrew.guide_allowance", "jackscrew.top_guide_z")},
            {"id": "guide_member", "name": "anti-rotation member", "kind": "cylinder", "axis": "Z", "projection": "rectangle",
             "keys": ["guide.length", "guide.rod_od", "guide.radius", "guide.angle"], "z_rule": zr(0, "guide.length")},
        ],
    }


def _x_extents(P, fid):
    g = P.get
    r_s = g("jackscrew.pitch_radius") * check_stack.cosd(g("jackscrew.angle")[0])
    pd2 = g("gear.pitch_diameter") / 2
    gap = g("ring.thickness")
    table = {
        "floor": (-g("icd.footprint_x") / 2, g("icd.footprint_x") / 2),
        "core_seat": (-g("core.diameter_nominal") / 2, g("core.diameter_nominal") / 2),
        "core_500": (-g("core.diameter_nominal") / 2, g("core.diameter_nominal") / 2),
        "drill_head": (-g("drill.head_od") / 2, g("drill.head_od") / 2),
        "drill_tube": (-g("drill.tube_od") / 2, g("drill.tube_od") / 2),
        "drill_top_block": (-g("drill.top_block_od") / 2, g("drill.top_block_od") / 2),
        "ring": (-g("ring.od") / 2, g("ring.od") / 2),
        "motor23_a": (-(pd2 + gap + g("pinion.motor_length")), -(pd2 + gap)),
        "screw_a": (r_s - g("jackscrew.nominal") / 2, r_s + g("jackscrew.nominal") / 2),
        "anchor_a": (r_s - g("jackscrew.nut_flange_od") / 2, r_s + g("jackscrew.nut_flange_od") / 2),
        "nut_a": (r_s - g("jackscrew.nut_flange_od") / 2, r_s + g("jackscrew.nut_flange_od") / 2),
        "guide_a": (r_s - g("jackscrew.nut_flange_od") / 2, r_s + g("jackscrew.nut_flange_od") / 2),
        "guide_member": (g("guide.radius") - g("guide.rod_od") / 2, g("guide.radius") + g("guide.rod_od") / 2),
    }
    return table[fid]


def draw_mini(P, spec, stack, mutate=None, title=None, labels=True):
    """Draw the mini side spec at its single pose. mutate(fid, x0, x1, z0, z1) -> (x0, x1, z0, z1) or None to skip."""
    pose = spec["poses"][0]["id"]
    feats = stack["poses"][pose]["features"]
    fig, ax = sc.setup_figure(spec["view"], title=title or f"mini pose {pose}")
    for row in spec["features"]:
        fid = row["id"]
        z0, z1 = feats[fid]["z_min"], feats[fid]["z_max"]
        if fid == "gear":
            bore2, pd2 = P.get("gear.bore") / 2, P.get("gear.pitch_diameter") / 2
            sc.draw_gear_section(ax, fid, bore2, pd2, z0, z1)
            continue
        x0, x1 = _x_extents(P, fid)
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


def mini_ctx(mutate=None, label_override=None, extra=None, title=None, labels=True):
    P = Params()
    spec = mini_side_spec()
    if label_override:
        for row in spec["features"]:
            if row["id"] in label_override:
                row["label_text_override"] = label_override[row["id"]]
    stack = check_stack.evaluate_spec(P, spec)
    figs = draw_mini(P, spec, stack, mutate=mutate, title=title, labels=labels)
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


# ---------------------------------------------------------------- K4

def k4_z():
    return mini_ctx()


def k4_b1():
    return mini_ctx(label_override={"drill_tube": "tube OD"})


def k4_b2():
    return mini_ctx(label_override={"drill_tube": "tube OD 150"})


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


def _k5_side(tube="rect", pinion="trap", untagged=False):
    P = Params()
    spec = _k5_side_spec()
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
    return [_k5_side(), _k5_plan()]


def k5_b1():
    return _k5_side(tube="circle")


def k5_b2():
    return _k5_side(pinion="rect")


def k5_b3():
    return _k5_side(untagged=True)


# ---------------------------------------------------------------- K6

DRILL = ("drill_head", "drill_tube", "drill_top_block")


def k6_z():
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


# ---------------------------------------------------------------- K7

def _k7(rows, poses, draw_fn, view="side_xz"):
    P = Params()
    spec = {"sketch": "k7", "view": view, "poses": poses, "features": rows}
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


def k7_z1():
    return _k7(_pair("F"), ONE, lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 200, 300, 0, 100)))


def k7_z2():
    return _k7(_pair("F", depth_a=(0, 10), depth_b=(20, 30)), ONE,
               lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 50, 150, 0, 100)))


def k7_z3():
    return _k7(_pair("C"), ONE, lambda ax, p: (sc.draw_rect(ax, "a", 0, 100, 0, 100), sc.draw_rect(ax, "b", 100, 200, 0, 100)))


FOUR = [{"id": "p1", "tip_z": 0}, {"id": "p2", "tip_z": 150}, {"id": "p3", "tip_z": 450}, {"id": "p4", "tip_z": 500}]


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


def plan_ctx(invert_y=False):
    P = Params()
    spec = plan_spec()
    fig, ax = sc.setup_figure("plan_xy", title="mini plan")
    sc.draw(ax=ax, feature_id="drill_tube", artist=Circle((0, 0), P.get("drill.tube_od") / 2))
    r = P.get("jackscrew.pitch_radius")
    for i, s in enumerate("abc"):
        th = P.get("jackscrew.angle")[i]
        sc.draw(ax=ax, feature_id=f"screw_{s}",
                artist=Circle((r * check_stack.cosd(th), r * check_stack.sind(th)), P.get("jackscrew.nominal") / 2))
    sc.finish_axes(ax)
    if invert_y:
        ax.invert_yaxis()
    return _ctx(P, spec, {"plan": fig})


def k8_z():
    return [mini_ctx(), plan_ctx()]


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


# ---------------------------------------------------------------- K9

def k9_z():
    return mini_ctx()


def k9_b1():
    return mini_ctx(mutate=lambda f, x0, x1, z0, z1: None if f == "guide_member" else (x0, x1, z0, z1))


def k9_b2():
    return mini_ctx(extra=lambda ax: sc.draw_rect(ax, "spare_bracket", 300, 340, 0, 40))


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
