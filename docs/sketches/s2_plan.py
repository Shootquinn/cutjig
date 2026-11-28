"""S2 plan XY (contributor gameplan (sean) detail 1.2): the whole jig seen from +Z at the spec plan_figure pose (load).

One figure through sketch_common.setup_figure("plan_xy"); every artist through sc.draw with gid = spec row id.
Every plan position comes from check_stack (place, plan_pieces, sector) or from the params named below. Shapes follow
each row's `shape` field as far as the K checks admit: a round row is a circle or annulus, a radial row a rectangle
or a toothed trapezoid along its azimuth, a plan_poly row its convex pieces. Each row is drawn as seen; hidden parts
are drawn by the plan renderer (1.3 P1R, sketch_common.render_plan): a piece wholly under nearer parts (true plan
outline of a row higher by more than 0.05, or an opaque fill drawn above) is dashed, no fill; a partly covered piece
keeps its style inside its visible region and gets a dashed, unfilled copy inside its hidden region (the ring rim under
the guide arms, the base-frame rails in the notches, the pinion teeth and motor shafts under the gear). Labels are
placed by the leader placer (sketch_common.place_plan_labels). The gear teeth face down: dashed radial ticks on the
underside face (sub-artist gear:ticks, Designer M1 r1 F1). The geometry rules are those of the S2 fixture drawing (fixtures/builders.py
_s2_draw_row); this script adds line styles, fills, the datum B signifiers inside the tube bore, part tags and the
margin labels.

  python s2_plan.py [--rev k]   writes s2_plan_r<k>.png to wip/ (sketch_loader output rule; default rev 1)
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
from matplotlib.collections import LineCollection  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Annulus, Circle, Polygon  # noqa: E402

# colours and line styles (strings; K1 admits no numeric literal outside 0, 1, -1, 2, 0.5)
PLATE = "#dde4ec"
SECTOR = "#fbe3c0"
RING = "#c9dcef"
RING_EDGE = "#1f4e79"
BRASS = "goldenrod"
GREY = "0.6"
DARK = "0.3"
HIDDEN = "--"
DOTTED = ":"
CHAIN = "-."
HATCH_PAD = "////"
GEAR_FILL = "#eeeeee"

# z order bands: plate, sector, base detail, fixed parts, ring, ring-mounted parts, drive, drill, signifiers
Z_PLATE, Z_SECTOR, Z_BASE, Z_FIXED, Z_RING, Z_ON_RING, Z_DRIVE, Z_DRILL, Z_SIGN = (
    i + 1 for i, _ in enumerate(("plate", "sector", "base", "fixed", "ring", "on_ring", "drive", "drill", "sign")))

RING_MOUNTED = ("nut_housing", "motor_mount", "guide_lug", "guide_bushing")


def _style(row):
    """Draw keywords per row as seen (shape field); hidden parts and pieces are drawn by sketch_common.render_plan."""
    return _style_visible(row)


def _style_visible(row):
    fid = row["id"]
    pre = fid.rsplit("_", 1)[0] if fid[-2:] in ("_a", "_b", "_c") else fid
    if fid == "base_plate":
        return {"fill": True, "facecolor": PLATE, "edgecolor": PLATE, "zorder": Z_PLATE}
    if fid == "operator_sector":
        # r4 (TP1.2-15): translucent, so the rail-top solid copy in the +Y notch shows through (no opaque fill over it)
        return {"fill": True, "facecolor": SECTOR, "edgecolor": "darkorange", "linewidth": 1, "alpha": 0.5, "zorder": Z_SECTOR}
    if fid == "base_frame":
        return {"edgecolor": GREY, "linewidth": 0.5, "zorder": Z_BASE}
    if fid in ("base_key_pockets", "base_pin_pocket"):
        return {"edgecolor": DARK, "linestyle": HIDDEN, "linewidth": 0.5, "zorder": Z_BASE}
    if fid in ("base_spigot_hole", "base_slots"):
        return {"edgecolor": DARK, "linewidth": 0.5, "zorder": Z_BASE}
    if fid == "slot_line_c":
        return {"color": "k", "linestyle": CHAIN, "linewidth": 1, "zorder": Z_BASE}
    if fid == "slot_lines":
        return {"color": GREY, "linestyle": CHAIN, "linewidth": 0.5, "zorder": Z_BASE}
    if pre == "frame_upper":
        return {"fill": True, "facecolor": "0.85", "edgecolor": "k", "hatch": "xx", "linewidth": 1, "zorder": Z_FIXED}
    if pre == "liftmotor":   # Designer M1 r1 N1: line weight of the bracket outlines
        return {"edgecolor": DARK, "linewidth": 1, "zorder": Z_FIXED}
    if pre in ("bracket_anchor", "anchor"):
        return {"edgecolor": DARK, "linewidth": 0.5, "zorder": Z_FIXED}
    if pre in ("bracket_guide", "guide"):
        return {"edgecolor": "k", "linewidth": 1, "zorder": Z_FIXED + Z_RING}
    if fid == "descent_stop":
        return {"edgecolor": "k", "hatch": HATCH_PAD, "linewidth": 1, "zorder": Z_FIXED}
    if fid == "descent_stop_post":
        return {"edgecolor": DARK, "linestyle": DOTTED, "linewidth": 1, "zorder": Z_FIXED}
    if pre == "screw":
        return {"fill": True, "facecolor": "k", "edgecolor": "k", "zorder": Z_FIXED + Z_RING + 1}
    if pre == "nut":
        return {"fill": True, "facecolor": BRASS, "edgecolor": "k", "linewidth": 0.5, "zorder": Z_ON_RING}
    if fid in ("guide_member", "guide_member_b"):
        return {"fill": True, "facecolor": DARK, "edgecolor": "k", "zorder": Z_FIXED + Z_RING + 1}
    if fid in ("guide_tie_a", "guide_tie_b"):   # Step 2 stand-in: phantom line, brown (1.3 P1Rf, Designer FIX D3)
        return {"edgecolor": sc.STAND_IN_COLOR, "linestyle": sc.PHANTOM, "linewidth": 1, "zorder": Z_FIXED + Z_RING + 1}
    if fid == "ring":
        return {"fill": True, "facecolor": RING, "edgecolor": RING_EDGE, "linewidth": 2, "alpha": 0.5, "zorder": Z_RING}
    if pre == "guide_bushing":
        return {"edgecolor": RING_EDGE, "linewidth": 0.5, "zorder": Z_ON_RING}
    if pre in RING_MOUNTED:
        return {"edgecolor": RING_EDGE, "linewidth": 1, "zorder": Z_ON_RING}
    if fid == "bearing":
        return {"edgecolor": DARK, "linewidth": 0.5, "zorder": Z_ON_RING}
    if fid == "gear":   # light plain fill so the dashed tooth ticks read (Designer M1 r1 F1)
        return {"fill": True, "facecolor": GEAR_FILL, "edgecolor": "k", "linewidth": 1, "zorder": Z_DRIVE}
    if fid == "gear_hub":
        return {"edgecolor": "k", "linewidth": 1, "zorder": Z_DRIVE}
    if pre == "pinion":   # hub and toothed piece as styled; the renderer draws the part under the gear hidden
        return {"edgecolor": "k", "linewidth": 1, "zorder": Z_DRIVE + 1}
    if pre == "motor23":
        return {"fill": True, "facecolor": GREY, "edgecolor": "k", "alpha": 0.5, "linewidth": 1, "zorder": Z_DRIVE}
    if pre == "motor_shaft":
        return {"fill": True, "facecolor": DARK, "edgecolor": "k", "zorder": Z_DRIVE}
    if pre == "pinion_axis":
        return {"color": "k", "linestyle": CHAIN, "linewidth": 0.5, "zorder": Z_DRIVE + 1}
    if fid == "drill_tube":
        return {"fill": True, "facecolor": DARK, "edgecolor": "k", "zorder": Z_DRILL}
    if fid == "keepout":
        return {"edgecolor": "red", "linestyle": HIDDEN, "linewidth": 1, "zorder": Z_DRILL}
    if fid == "drill_head":
        return {"edgecolor": "k", "linestyle": DOTTED, "linewidth": 1, "zorder": Z_DRILL}
    return {"edgecolor": "k", "linewidth": 1, "zorder": Z_SIGN}


def _line_kw(kw):
    """Patch keywords to Line2D keywords."""
    out = {k: v for k, v in kw.items() if k in ("linestyle", "linewidth", "zorder", "color")}
    out.setdefault("color", kw.get("edgecolor", "k"))
    return out


def _radial_poly(r0, r1, th, w0, w1=None):
    """Four-vertex piece along the radial direction at th: half-width w0 at r0, w1 at r1 (w1 = w0: rectangle)."""
    w1 = w0 if w1 is None else w1
    c, s = check_stack.cosd(th), check_stack.sind(th)
    return [(u * c - v * s, u * s + v * c) for u, v in ((r0, -w0), (r1, -w1), (r1, w1), (r0, w0))]


def _datum_b(ax, P, kw):
    """Datum B inside the tube bore: cross to the bore radius, +X and +Y arrowheads, theta arc counter-clockwise from
    +X to +Y at half the bore radius with its arrowhead at +Y (all one row, collet_axis)."""
    fid = "collet_axis"
    L = P.get("drill.tube_id") / 2
    hd = L / 2 / 2 / 2
    lk = {"color": "k", "linewidth": 1, "zorder": Z_SIGN}
    for xs, ys in (([-L, L], [0, 0]), ([0, 0], [-L, L]),
                   ([L - hd, L, L - hd], [hd / 2, 0, -hd / 2]), ([hd / 2, 0, -hd / 2], [L - hd, L, L - hd])):
        sc.draw(fid, Line2D(xs, ys, **lk), ax)
    ra, n = L / 2, sc.PLAN_NGON
    arc = [(ra * math.cos(math.pi / 2 * i / n), ra * math.sin(math.pi / 2 * i / n)) for i in range(n + 1)]
    sc.draw(fid, Line2D([p[0] for p in arc], [p[1] for p in arc], **lk), ax)
    sc.draw(fid, Line2D([hd / 2, 0, hd / 2], [ra + hd / 2, ra, ra - hd / 2], **lk), ax)
    t = {"fontsize": "x-small", "zorder": Z_SIGN}
    ax.text(L, -hd, "+X", ha="right", va="top", **t)
    ax.text(hd / 2, L, "+Y", ha="left", va="top", **t)
    ax.text(ra * math.cos(math.pi / 2 / 2), ra * math.sin(math.pi / 2 / 2), "theta", ha="left", va="bottom", **t)


def _gear_ticks(ax, P, row, kw):
    """Dashed radial tooth ticks on the gear's underside face (Designer M1 r1 F1): one per tooth, from the toe to the
    heel radius of the row's ticks_radial predicate, evenly spaced from +X; LineCollection gid <row>:ticks."""
    pr = next(p for p in row["sense"] if p["pred"] == "ticks_radial")
    r0, r1 = (check_stack.eval_expr(pr[k], P, {}) for k in ("r_in", "r_out"))
    n = int(round(check_stack.eval_expr(pr["count"], P, {})))
    segs = []
    for i in range(n):
        a = 2 * math.pi * i / n
        segs.append([(r0 * math.cos(a), r0 * math.sin(a)), (r1 * math.cos(a), r1 * math.sin(a))])
    lc = LineCollection(segs, colors="k", linestyles=HIDDEN, linewidths=0.5, zorder=kw.get("zorder", Z_DRIVE) + 1)
    sc.draw(row["id"] + sc.TICKS_SUFFIX, lc, ax)


def draw_row(ax, P, stack, pid, row):
    fid = row["id"]
    f = stack["poses"][pid]["features"].get(fid, {})
    names = stack["poses"][pid]["vars_z_A"]
    ev = lambda e: check_stack.eval_expr(e, P, names)  # noqa: E731
    kw = _style(row)
    if f.get("sector"):
        sec = f["sector"]   # wedge: apex and arc of the spec boundary (its edge sample points dropped)
        wedge = [p for p in sc.sector_boundary(sec) if math.hypot(*p) <= sc.TOL_Z or abs(math.hypot(*p) - sec["r"]) <= sc.TOL_Z]
        sc.draw(fid, Polygon(wedge, closed=True, **kw), ax)
        return
    if fid == "collet_axis":
        _datum_b(ax, P, kw)
        return
    kw.setdefault("fill", False)
    if row.get("section") and not f.get("place"):
        a, b = sorted(ev(e) for e in row["section"])
        sc.draw(fid, Annulus((0, 0), b, b - a, **kw) if a > 0 else Circle((0, 0), b, **kw), ax)
        if row["kind"] == "gear" and any(p.get("pred") == "ticks_radial" for p in row.get("sense") or []):
            _gear_ticks(ax, P, row, kw)
        return
    if f.get("plan_pieces"):
        for pc in f["plan_pieces"]:
            if len(pc) == 2:
                sc.draw(fid, Line2D([pc[0][0], pc[1][0]], [pc[0][1], pc[1][1]], **_line_kw(kw)), ax)
            else:
                sc.draw(fid, Polygon(pc, closed=True, **kw), ax)
        return
    pl = f.get("place")
    if not pl:
        return
    th, r0, r1, w = pl["theta"], pl["r_in"], pl["r_out"], pl["half_width"]
    c, s = check_stack.cosd(th), check_stack.sind(th)
    if pl["footprint"] == "radial":
        if w == 0:
            lk = _line_kw(kw)
            if row.get("draw"):
                (u0, u1), (d0, d1) = ([ev(x) for x in row["draw"][k]] for k in ("solid", "dashed"))
                sc.draw(fid, Line2D([u0 * c, u1 * c], [u0 * s, u1 * s], marker="o", markevery=[1], **lk), ax)
                sc.draw(fid, Line2D([d0 * c, d1 * c], [d0 * s, d1 * s], **dict(lk, linestyle=HIDDEN)), ax)
            else:
                sc.draw(fid, Line2D([r0 * c, r1 * c], [r0 * s, r1 * s], **lk), ax)
        elif row["kind"] == "gear":
            heel = P.get("pinion.r_heel")   # toothed piece; its part under the gear annulus drawn hidden by the renderer
            sc.draw(fid, Polygon(_radial_poly(r0, heel, th, w * r0 / heel, w), closed=True, **kw), ax)
            sc.draw(fid, Polygon(_radial_poly(heel, r1, th, w / 2), closed=True, **kw), ax)
        else:
            sc.draw(fid, Polygon(check_stack.radial_corners(r0, r1, th, w, pl.get("rot", 0)), closed=True, **kw), ax)
        return
    cx, cy = pl["r_c"] * c, pl["r_c"] * s
    if row.get("projection") == "rectangle":
        h = w / math.sqrt(2)
        sq = [(cx + u * c - v * s, cy + u * s + v * c) for u, v in ((-h, -h), (h, -h), (h, h), (-h, h))]
        sc.draw(fid, Polygon(sq, closed=True, **kw), ax)
    elif fid == "drill_tube":
        sc.draw(fid, Annulus((cx, cy), w, w - P.get("drill.tube_id") / 2, **kw), ax)
    else:
        sc.draw(fid, Circle((cx, cy), w, **kw), ax)


def _plate_outline(ax, feats, spec):
    """Plate outline with both column notches (Designer sign-off r3, M1 S2 r2 N2): one unfilled Polygon, gid
    base_plate:outline, the boundary of the union of the base_plate plan_poly pieces, at bracket line weight above the
    plate tint; drawn only when the row carries outline_matches (K5 admission premise)."""
    row = next(r for r in spec["features"] if r["id"] == "base_plate")
    if not any(p.get("pred") == "outline_matches" for p in row.get("sense") or []):
        return
    ring = sc.union_boundary(feats["base_plate"]["plan_pieces"])
    sc.draw("base_plate" + sc.OUTLINE_SUFFIX, Polygon(ring, closed=True, fill=False, edgecolor=DARK, linewidth=1, zorder=Z_BASE), ax)


def _tags(ax, P, feats):
    """Untagged part tags: screw set letter and azimuth outboard of each frame member; pinion letter and azimuth beside
    each NEMA 23, on the side farther from the guide rods and the F6 sightline (Designer M1 S2 r2 N1: off slot line C;
    letter map in the spec header)."""
    t = {"fontsize": "x-small", "ha": "center", "va": "center", "zorder": Z_SIGN,
         "bbox": {"boxstyle": "round", "facecolor": "white", "edgecolor": "none", "alpha": 0.5}}
    off = P.get("profile.width")
    avoid = [p for g in ("guide_member", "guide_member_b", "sightline_f6") for p in sc.pieces(ax, g)]
    for s in ("a", "b", "c"):
        pl = feats[f"frame_upper_{s}"]["place"]
        r = pl["r_out"] + off / 2
        ax.text(r * check_stack.cosd(pl["theta"]), r * check_stack.sind(pl["theta"]), f"screw {s}\n{pl['theta']:g} deg", **t)
        pl = feats[f"motor23_{s}"]["place"]
        c, sn = check_stack.cosd(pl["theta"]), check_stack.sind(pl["theta"])
        u = (pl["r_in"] + pl["r_out"]) / 2
        sides = [(u * c - v * sn, u * sn + v * c) for v in (pl["half_width"] + off, -(pl["half_width"] + off))]
        x, y = max(sides, key=lambda q: min(sc.min_distance([q], a) for a in avoid))
        ax.text(x, y, f"pinion {s}\n{pl['theta']:g} deg", **t)


def build(P, spec, stack):
    """check_sketch.py entry point: {pose id: Figure} (one plan figure at plan_figure.pose)."""
    pf = spec.get("plan_figure") or {}
    pid = pf.get("pose") or spec["poses"][0]["id"]
    pr = stack["poses"][pid]
    feats = pr["features"]
    title = f"S2 plan seen from +Z, pose {pid} (ring at {feats['ring']['z_min']:.2f} to {feats['ring']['z_max']:.2f} z_S)"
    fig, ax = sc.setup_figure(spec["view"], title=title)
    for row in spec["features"]:
        if sc.applies(row, pid):
            draw_row(ax, P, stack, pid, row)
    ctx = sc.Ctx(P=P, spec=spec, stack=stack, view=spec["view"])
    sc.render_plan(ctx, ax, pid)   # 1.3 P1R hidden-line renderer
    _plate_outline(ax, feats, spec)
    _tags(ax, P, feats)
    s21 = spec["s2_checks"]["S2-1"]
    ang = lambda k, ids: ", ".join(f"{i[-1]} {feats[i]['place']['theta']:g}" for i in ids)  # noqa: E731
    yc = feats["slot_line_c"]["plan_pieces"][0][0][1]
    notes = [
        (None, f"handedness: +X along slot line C (y {yc:+g}, +Y rail); theta counter-clockwise from +X seen from +Z\n"
               f"(datum B cross, +X / +Y arrows and theta arc inside the drill tube bore)"),
        (None, f"screws {ang('s', s21['screws'])}; pinions {ang('p', s21['pinions'])} deg;\n"
               f"pinion phase {s21['phase_deg']:g} deg from the screws (Design Notes 27, O1-B)"),
        (None, "dashed, no fill: the part of a piece under a nearer part (base frame, pockets, lift motors, anchor arms and blocks, nut flanges, descent-stop\n"
               "pad, motor mounts, guide lugs and rods, bushings, bearing, pinion teeth and motor shafts under the gear, ring rim under the guide arms);\n"
               "dotted: cutter rim, descent-stop post\n"
               "phantom, brown: Step 2 stand-in (rod top ties)\n"
               "dashed radial ticks: gear teeth on the underside face (teeth face down); chain: slot lines, pinion axes"),
        (None, f"plan at pose {pid}; plan positions do not change with pose (z bands per pose in the checks)"),
    ]
    if pf.get("figure_note"):
        notes.append((None, pf["figure_note"].replace("; ", ";\n"), sc.NOTE_GID))
    sc.finish_axes(ax)
    y0, y1 = ax.get_ylim()   # room for the screw c tag outboard of member c (below the plate edge)
    ax.set_ylim(y0 - P.get("profile.width"), y1)
    sc.place_plan_labels(ax, ctx, pid, margin=True, stack_pose=feats, notes=notes, collinear=True)   # 1.3 P1R leader placer; 1.4 (h) r2 rule (l) at 12 px (Design Notes 35 R1)
    return {pid: fig}


def main(argv=None):
    ap = argparse.ArgumentParser(description="S2 plan: write the plan PNG")
    ap.add_argument("--rev", type=int, default=1)
    a = ap.parse_args(argv)
    P = Params()
    spec = load_spec(HERE / "s2_spec.yaml")
    stack = check_stack.evaluate_spec(P, spec)
    name = (spec.get("plan_figure") or {}).get("name", "s2_plan")
    out = []
    for pid, fig in build(P, spec, stack).items():
        path = output_path(f"{name}_r{a.rev}.png")   # wip/ (sketch_loader output rule)
        fig.savefig(path, bbox_inches="tight")
        out.append(path)
    for p in out:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
