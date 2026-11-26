"""S1 side poses (contributor gameplan (sean) detail 1.1): side XZ of the whole jig at load, start, capture_end and park.

One figure per pose through sketch_common.setup_figure; every artist through sc.draw with gid = spec row id.
Every z comes from check_stack (z_S, shop floor); every x from check_stack `place` or from params named below.
Shapes follow each row's `shape` field (Designer 1.1 (a) section 2) as far as the K checks admit: an artist tagged
with a round-kind row must be its declared projection, so section detail is drawn as extra rectangles of that row.

  python s1_side_poses.py [--rev k]   writes s1_pose_<pose>_r<k>.png to wip/ (sketch_loader output rule; default rev 1)
"""
import argparse
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params, load_spec, output_path  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

GREY = "0.8"
DARK = "0.45"
BRASS = "goldenrod"
HATCH_GEAR, HATCH_PINION = "////", "\\\\\\\\"     # F1 (c): gear and pinions hatched in opposite directions


# ---------------------------------------------------------------- shape helpers (x from params, z from check_stack)

def _sides(ax, fid, r0, r1, z0, z1, **kw):
    """Annulus in section: one rectangle per side, mirrored about x = 0."""
    for s in (-1, 1):
        sc.draw_rect(ax, fid, s * r0, s * r1, z0, z1, **kw)


def _cone_sides(ax, fid, r_in, r_out, z0, z1, alpha_deg):
    """Collet cone in section: per side a four-vertex piece, bore edge vertical at r_in, outer face narrowing upward
    by (z1 - z0) tan(alpha) (TP-2: narrows up)."""
    t = (z1 - z0) * math.tan(math.radians(alpha_deg))
    for s in (-1, 1):
        pts = [(s * r_in, z0), (s * r_out, z0), (s * (r_out - t), z1), (s * r_in, z1)]
        sc.draw(fid, Polygon(pts, closed=True, fill=False), ax)


def _pinion(ax, fid, x0, x1, z0, z1, toe_over_heel, **kw):
    """Bevel pinion projected at its azimuth: full outer diameter at the outer (heel and hub) end, toe height scaled by
    r_toe / r_heel at the inner end (cone apex on the drill axis), centred on the pinion axis (TP-2: narrows inward)."""
    inner, outer = (x0, x1) if abs(x0) < abs(x1) else (x1, x0)
    zc, h = (z0 + z1) / 2, (z1 - z0) * toe_over_heel
    pts = [(inner, zc - h / 2), (outer, z0), (outer, z1), (inner, zc + h / 2)]
    sc.draw(fid, Polygon(pts, closed=True, fill=False, **kw), ax)


def _hidden_by_nearer(feats, fid):
    """True when a placed part wholly nearer the viewer (side view seen from -Y: depth band below this row's band)
    overlaps this row in z and covers at least half its projected x length. Designer M1 r2 F2: such an arm is drawn
    dashed (guide arm behind the NEMA 23 at load and park); a 20 mm guide rod in front of an arm leaves it solid."""
    me = feats[fid]
    mx0, mx1 = me["place"]["x"]
    for oid, o in feats.items():
        if oid == fid or "place" not in o or "z_min" not in o or "depth" not in o:
            continue
        x_ov = min(mx1, o["place"]["x"][1]) - max(mx0, o["place"]["x"][0])
        z_ov = min(me["z_max"], o["z_max"]) > max(me["z_min"], o["z_min"])
        if z_ov and x_ov >= (mx1 - mx0) * 0.5 and o["depth"][1] < me["depth"][0]:
            return True
    return False


# ---------------------------------------------------------------- one pose

def draw_pose(P, spec, stack, pose):
    pid = pose["id"]
    pr = stack["poses"][pid]
    feats = pr["features"]
    g = P.get
    title = f"S1 pose {pid}, tip {pr['tip_z_S']:.2f} z_S ({pose.get('purpose', '')})"
    fig, ax = sc.setup_figure(spec["view"], title=title)
    half_fp = g("icd.footprint_x") / 2
    rows = {r["id"]: r for r in spec["features"]}

    def z(fid):
        return feats[fid]["z_min"], feats[fid]["z_max"]

    def px(fid):
        return feats[fid]["place"]["x"]

    def on(fid):
        return fid in feats and "z_min" in feats[fid] and sc.applies(rows[fid], pid)

    # floor and soft target: lines across the footprint
    z0, _ = z("floor")
    sc.draw_hline(ax, "floor", -half_fp, half_fp, z0, linewidth=2)
    # margin notes, untagged Text (Designer M1 r2 F4: every label in the right margin, the drawing left clear)
    notes = [((half_fp, z0), f"shop floor z_S {z0:g}"),
             # TP1.1-7: parts at x = 0 behind or in front of the drill axis are not drawn in the side view
             (None, f"not drawn (project onto x = 0): third screw set, theta {g('jackscrew.angle')[-1]:g};\n"
                    f"third pinion and NEMA 23, theta {g('pinion.angle')[0]:g}; see S2 plan")]
    z0, _ = z("height_target")
    sc.draw_hline(ax, "height_target", -half_fp, half_fp, z0, linestyle="--", color=DARK)

    # base frame: side rail band over footprint_x, end members as profile sections at x = +/- frame.end_x
    z0, z1 = z("base_frame")
    sc.draw_rect(ax, "base_frame", -half_fp, half_fp, z0, z1)
    for s in (-1, 1):
        xc = s * g("frame.end_x")
        sc.draw_rect(ax, "base_frame", xc - g("profile.width") / 2, xc + g("profile.width") / 2, z0, z0 + g("profile.height"), hatch="xx")

    # base plate in section
    z0, z1 = z("base_plate")
    sc.draw_rect(ax, "base_plate", -half_fp, half_fp, z0, z1, hatch="//")

    # receiver cup in section: floor either side of the debris hole, walls from the register bore to the spigot OD
    z0, z1 = z("receiver")
    zf = stack["poses"][pid]["vars_z_A"]["receiver_floor"] + (pr["tip_z_S"] - pr["tip_z_A"])
    r_reg, r_out = g("receiver.register_bore_radius"), g("receiver.spigot_od") / 2
    _sides(ax, "receiver", g("receiver.floor_hole_dia") / 2, r_reg, z0, zf, hatch="//")
    _sides(ax, "receiver", r_reg, r_out, z0, z1, hatch="//")

    # collet cone (bore at the core OD) and the core-seat ledge inside its bore bottom
    z0, z1 = z("collet")
    r_bore = g("core.diameter_nominal") / 2
    _cone_sides(ax, "collet", r_bore, r_reg, z0, z1, g("cone.alpha"))
    z0, z1 = z("core_seat")
    _sides(ax, "core_seat", r_bore - g("collet.core_seat_width"), r_bore, z0, z1, fill=True, facecolor=DARK)

    # holder tube (wall to the register bore) with the flange on top of holder.length (LF1.1-1). Over the collet height
    # the bore follows the collet outer cone (spec bore_cone, TP1.1-3: contact on the cone face, class C); above the
    # collet top the bore is at the core OD.
    zc0, zc1 = z("collet")
    tan_a = math.tan(math.radians(g("cone.alpha")))
    z0, z1 = z("holder")
    zfl = z1 - g("holder.flange_thickness")
    zk = min(zc1, zfl)
    if z0 < zk:
        r_c0, r_c1 = r_reg - (z0 - zc0) * tan_a, r_reg - (zk - zc0) * tan_a
        for s in (-1, 1):
            pts = [(s * r_c0, z0), (s * r_reg, z0), (s * r_reg, zk), (s * r_c1, zk)]
            sc.draw("holder", Polygon(pts, closed=True, fill=False), ax)
    _sides(ax, "holder", r_bore, r_reg, max(z0, zk), zfl)
    _sides(ax, "holder", r_bore, g("holder.flange_od") / 2, zfl, z1)

    # wing nut: body, two wings at the bottom to the span, sweep radius as a dashed envelope
    z0, z1 = z("wingnut")
    sc.draw_rect(ax, "wingnut", -g("wingnut.body_od") / 2, g("wingnut.body_od") / 2, z0, z1)
    _sides(ax, "wingnut", g("wingnut.body_od") / 2, g("wingnut.span") / 2, z0, z0 + g("wingnut.wing_height"))
    r_sw = g("wingnut.sweep_clear_radius")
    sc.draw_rect(ax, "wingnut", -r_sw, r_sw, z0, z1, linestyle="--")

    # collar ring in section
    z0, z1 = z("collar")
    _sides(ax, "collar", g("collar.id") / 2, g("collar.od") / 2, z0, z1, hatch="//")

    # capture core: solid outline, absent at park
    if on("core_750"):
        z0, z1 = z("core_750")
        sc.draw_rect(ax, "core_750", -r_bore, r_bore, z0, z1, linewidth=2)

    # drill: head (cutter teeth strip, iris throat dashed), tube (bore dashed), top-end block (solid)
    z0, z1 = z("drill_head")
    x0, x1 = px("drill_head")
    sc.draw_rect(ax, "drill_head", x0, x1, z0, z1, linewidth=2)
    teeth = (g("drill.head_od") - g("drill.tube_od")) / 2
    sc.draw_rect(ax, "drill_head", x0, x1, z0, z0 + teeth, hatch="||")
    sc.draw_rect(ax, "drill_head", -g("drill.tube_id") / 2, g("drill.tube_id") / 2, z0, z1, linestyle="--")
    z0, z1 = z("drill_tube")
    x0, x1 = px("drill_tube")
    sc.draw_rect(ax, "drill_tube", x0, x1, z0, z1)
    sc.draw_rect(ax, "drill_tube", -g("drill.tube_id") / 2, g("drill.tube_id") / 2, z0, z1, linestyle="--")
    z0, z1 = z("drill_top_block")
    x0, x1 = px("drill_top_block")
    sc.draw_rect(ax, "drill_top_block", x0, x1, z0, z1, fill=True, facecolor=DARK)
    z0, _ = z("bore_ceiling")
    sc.draw_hline(ax, "bore_ceiling", -g("drill.tube_id") / 2, g("drill.tube_id") / 2, z0, linestyle="--", color=DARK)
    z0, z1 = z("keepout")
    for s in (-1, 1):
        sc.draw(ax=ax, feature_id="keepout", artist=sc.Line2D([s * g("icd.keepout_radius")] * 2, [z0, z1], linestyle="--", linewidth=0.5))

    # ring structure: plate in section either side of the clearance bore, bosses, lugs, standoffs, bearing
    z0, z1 = z("ring")
    _sides(ax, "ring", g("ring.clearance_bore") / 2, g("ring.od") / 2, z0, z1, hatch="//")
    # r5: LM20UU housings under the lugs (rows guide_bushing_a, _b; Loftsman 1.2 (b) FIX 1)
    for fid in ("nut_housing_a", "nut_housing_b", "guide_lug_a", "guide_lug_b", "guide_bushing_a", "guide_bushing_b",
                "motor_mount_a", "motor_mount_b"):
        z0, z1 = z(fid)
        x0, x1 = px(fid)
        sc.draw_rect(ax, fid, x0, x1, z0, z1)
    z0, z1 = z("bearing")
    rb_in, rb_out = g("bearing.bore") / 2, g("bearing.od") / 2
    rb_mid = (rb_in + rb_out) / 2
    _sides(ax, "bearing", rb_in, rb_mid, z0, z1)
    _sides(ax, "bearing", rb_mid, rb_out, z0, z1)

    # bevel ring gear (teeth down, TP-2) on its hub; pinions toe inward; NEMA 23 bodies outboard
    z0, z1 = z("gear")
    sc.draw_gear_section(ax, "gear", g("gear.bore") / 2, g("gear.od") / 2, z0, z1, hatch=HATCH_GEAR)
    z0, z1 = z("gear_hub")
    _sides(ax, "gear_hub", g("drill.tube_od") / 2, g("gear.bore") / 2, z0, z1)
    for fid in ("pinion_a", "pinion_b"):
        z0, z1 = z(fid)
        x0, x1 = px(fid)
        _pinion(ax, fid, x0, x1, z0, z1, g("pinion.r_toe") / g("pinion.r_heel"), hatch=HATCH_PINION)
    for fid in ("motor23_a", "motor23_b"):
        z0, z1 = z(fid)
        x0, x1 = px(fid)
        sc.draw_rect(ax, fid, x0, x1, z0, z1, fill=True, facecolor=GREY, edgecolor="k")
    # F1 (a): NEMA 23 output shaft, radial, from motor_r_in - shaft_length to the flange face, on the pinion axis
    for fid in ("motor_shaft_a", "motor_shaft_b"):
        z0, z1 = z(fid)
        x0, x1 = px(fid)
        sc.draw_rect(ax, fid, x0, x1, z0, z1, fill=True, facecolor=DARK, edgecolor="k")
    # F1 (b): pinion centreline, dash-dot, toe tip to the motor outer end
    for fid in ("pinion_axis_a", "pinion_axis_b"):
        z0, _ = z(fid)
        x0, x1 = px(fid)
        sc.draw(ax=ax, feature_id=fid, artist=sc.Line2D([x0, x1], [z0, z0], linestyle="-.", color="k"))

    # jack screws (lead hatch), nuts, anchors (thrust-bearing line), top guides, lift motors, guide rods, frame members
    for s in ("a", "b"):
        z0, z1 = z(f"screw_{s}")
        x0, x1 = px(f"screw_{s}")
        sc.draw_rect(ax, f"screw_{s}", x0, x1, z0, z1, hatch="--")
        z0, z1 = z(f"nut_{s}")
        x0, x1 = px(f"nut_{s}")
        sc.draw_rect(ax, f"nut_{s}", x0, x1, z0, z1, fill=True, facecolor=BRASS, edgecolor="k")
        z0, z1 = z(f"anchor_{s}")
        x0, x1 = px(f"anchor_{s}")
        sc.draw_rect(ax, f"anchor_{s}", x0, x1, z0, z1, hatch="xx")
        sc.draw_rect(ax, f"anchor_{s}", x0, x1, (z0 + z1) / 2, (z0 + z1) / 2, linewidth=2)
        z0, z1 = z(f"guide_{s}")
        x0, x1 = px(f"guide_{s}")
        sc.draw_rect(ax, f"guide_{s}", x0, x1, z0, z1, hatch="..")
        # F2: bracket arms, block face to the frame member face at the block height; dashed where a nearer part covers
        for arm in (f"bracket_anchor_{s}", f"bracket_guide_{s}"):
            z0, z1 = z(arm)
            x0, x1 = px(arm)
            sc.draw_rect(ax, arm, x0, x1, z0, z1, linestyle="--" if _hidden_by_nearer(feats, arm) else "-")
        z0, z1 = z(f"liftmotor_{s}")
        x0, x1 = px(f"liftmotor_{s}")
        sc.draw_rect(ax, f"liftmotor_{s}", x0, x1, z0, z1, fill=True, facecolor=GREY, edgecolor="k")
        z0, z1 = z(f"frame_upper_{s}")
        x0, x1 = px(f"frame_upper_{s}")
        sc.draw_rect(ax, f"frame_upper_{s}", x0, x1, z0, z1)
    for fid in ("guide_member", "guide_member_b"):
        z0, z1 = z(fid)
        x0, x1 = px(fid)
        sc.draw_rect(ax, fid, x0, x1, z0, z1)
    # r5: rod top ties on the top-guide arms (Designer 1.2 (b) FIX 1), x over the plan_poly extent, dashed (Step 2 stand-in)
    for fid in ("guide_tie_a", "guide_tie_b"):
        z0, z1 = z(fid)
        x0, x1 = feats[fid]["plan_x"]
        sc.draw_rect(ax, fid, x0, x1, z0, z1, linestyle="--")

    # descent stop pad (metal hatch)
    z0, z1 = z("descent_stop")
    x0, x1 = px("descent_stop")
    sc.draw_rect(ax, "descent_stop", x0, x1, z0, z1, hatch="////")
    # F3: post from the anchor arm top to the pad bottom
    z0, z1 = z("descent_stop_post")
    x0, x1 = px("descent_stop_post")
    sc.draw_rect(ax, "descent_stop_post", x0, x1, z0, z1, fill=True, facecolor=DARK)

    # V9 (F2, F5): the axial loop, named along the drawn members (margin note under the axes)
    notes.append((None, "axial loop: ring nut - T8 screw - anchor and guide blocks - bracket arms -\n"
                        "screw frame 30-6060 - base plate - base frame - floor"))
    # F4: on the park figure, the lift stroke and the park rule (spec park_rule.park)
    if pid == "park":
        glob = stack["global_z_A"]
        low_id = min(stack["poses"], key=lambda k: stack["poses"][k]["tip_z_S"])
        low = stack["poses"][low_id]["tip_z_S"]
        notes.append(((px("drill_head")[1], pr["tip_z_S"]),
                      f"lift stroke {glob['lift_stroke']:.0f} (park {pr['tip_z_S']:.2f} - {low_id} {low:.2f} z_S)"))
        notes.append((None, f"park rule (option R, Design Notes 22):\npark = {spec['park_rule']['park']}\n"
                            f"= {glob['park_tip']:.2f} z_A = {pr['tip_z_S']:.2f} z_S"))

    # Designer 1.2 (c) FIX R1: the spec figure note (not_drawn parts) on every pose figure, tagged for K4
    if spec.get("figure_note"):
        notes.append((None, spec["figure_note"], sc.NOTE_GID))

    sc.finish_axes(ax)
    sc.place_labels(ax, spec, P, pid, margin=True, stack_pose=feats, notes=notes)
    return fig


def build(P, spec, stack):
    """check_sketch.py entry point: {pose id: Figure}."""
    return {pose["id"]: draw_pose(P, spec, stack, pose) for pose in spec["poses"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="S1 side poses: write one PNG per pose")
    ap.add_argument("--rev", type=int, default=1)
    a = ap.parse_args(argv)
    P = Params()
    spec = load_spec(HERE / "s1_spec.yaml")
    stack = check_stack.evaluate_spec(P, spec)
    out = []
    for pid, fig in build(P, spec, stack).items():
        path = output_path(f"s1_pose_{pid}_r{a.rev}.png")   # wip/ (sketch_loader output rule)
        fig.savefig(path, bbox_inches="tight")   # every text inside the saved image (1.2 (h), Designer M1 S1 r5 F1; K3)
        out.append(path)
    for p in out:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
