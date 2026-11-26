"""S3 section A-A through jack screw c (contributor gameplan (sean) detail 1.3; Design Notes 4: screw c, theta 270, YZ
plane): section_yz (plane x = 0 seen from +X, u = +Y right, z up, z_S plotted) at the spec section_figure pose
(capture_end, cut case), with the plan inset of all three screws (inset_plan, seen from +Z).

One figure through sketch_common.setup_figure (the spec view and its insets); every artist through sc.draw with gid =
spec row id (sub-artists <row>:line, <row>:balls, <row>:lever as the spec declares them). Every z comes from check_stack
(z_S) or from the spec's z_A expressions shifted by the pose's z_A to z_S offset; every u from check_stack `place` (plan
y), plan_poly pieces, the spec section_u pieces (true cut) or the spec section radii (axis-Z annulus mirrored about
u = 0). The renderer section convention (sketch_common.render_section) sets cut hatching by material, unsectioned
outlines above the hatch and beyond edges dashed behind cut parts; the inset goes through the plan renderer
(render_plan). Labels go through the leader placer (sketch_common.place_plan_labels) in both Axes; an UNPLACEABLE label
is recorded by the placer (K4 record), never hand-placed.

  python s3_jackscrew_section.py [--rev k]   writes s3_jackscrew_section_r<k>.png to wip/ (sketch_loader output rule)
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
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Polygon  # noqa: E402

MAIN = "section"
INSET = "inset_plan"
CHAIN = "-."
HIDDEN = "--"
DOTTED = ":"
DARK = "0.3"
GREY = "0.6"
BRASS = "goldenrod"
RING_EDGE = "#1f4e79"
LOAD = "#b2182b"
CALLOUT = "0.35"


# ---------------------------------------------------------------- helpers

class Pose:
    """Values of one pose: features (z_S), z_A names, z_A to z_S shift, spec expression evaluation."""

    def __init__(self, P, stack, pid):
        self.P, self.pid = P, pid
        pr = stack["poses"][pid]
        self.feats, self.names = pr["features"], pr["vars_z_A"]
        self.shift = pr["tip_z_S"] - pr["tip_z_A"]

    def ev(self, e):
        return check_stack.eval_expr(e, self.P, self.names)

    def zs(self, e):
        """z_A expression to z_S."""
        return self.ev(e) + self.shift

    def z(self, fid):
        f = self.feats[fid]
        return f["z_min"], f["z_max"]

    def u(self, fid):
        """Section u extent of a placed row: the plan y extent of its place."""
        return tuple(self.feats[fid]["place"]["y"])


def _arrow(ax, fid, tail, head, **kw):
    kw.setdefault("color", LOAD)
    return sc.draw(fid, FancyArrowPatch(tail, head, arrowstyle="-|>", mutation_scale=sc.LABEL_FONTSIZE * 2, shrinkA=0, shrinkB=0,
                                        linewidth=2, **kw), ax)


def _mirror(ax, fid, r0, r1, lo, hi, **kw):
    for s in (-1, 1):
        sc.draw_rect(ax, fid, s * r0, s * r1, lo, hi, **kw)


def _section_pieces(pz, row, z0, z1):
    """Spec section entries [r_in, r_out(, z_lo, z_hi)] as (r0, r1, lo, hi), z in z_S (omitted z: the row's extent)."""
    sec = row["section"]
    ents = sec if isinstance(sec[0], list) else [sec]
    out = []
    for e in ents:
        r0, r1 = sorted((pz.ev(e[0]), pz.ev(e[1])))
        lo, hi = (pz.zs(e[-2]), pz.zs(e[-1])) if len(e) > 2 else (z0, z1)
        out.append((r0, r1, lo, hi))
    return out


# ---------------------------------------------------------------- section Axes

def draw_section_row(ax, pz, spec, row):
    P, g = pz.P, pz.P.get
    fid, kind = row["id"], row.get("kind")
    rows = {r["id"]: r for r in spec["features"]}
    f = pz.feats.get(fid)
    if f is None:
        return
    z0, z1 = f.get("z_min"), f.get("z_max")
    us = g("jackscrew.pitch_radius") * check_stack.sind(g("jackscrew.angle")[2])   # screw c in the plane, u = r sin 270

    if fid == "keepout":
        r = g("icd.keepout_radius")
        for s in (-1, 1):
            sc.draw(fid, Line2D([s * r, s * r], [z0, z1], color="red", linestyle=HIDDEN, linewidth=1), ax)
        return
    if fid == "floor":
        u0, u1 = f["depth"]
        sc.draw_hline(ax, fid, u0, u1, z0, color="k", linewidth=2)
        return
    if kind == "line":
        if abs(z1 - z0) <= sc.TOL_Z:                       # nut station ticks across the screw
            u0, u1 = pz.u(fid)
            sc.draw_hline(ax, fid, u0, u1, z0, color="k", linestyle=CHAIN, linewidth=1)
        else:                                            # span L_t, on the screw axis between the bearing lines
            uc = sum(pz.u(fid)) / 2
            sc.draw(fid, Line2D([uc, uc], [z0, z1], color=LOAD, linewidth=1, marker="_", markersize=sc.LABEL_FONTSIZE * 2), ax)
        return
    if kind == "arrow":
        d = next((p["dir"] for p in row.get("sense") or [] if p.get("pred") == "points"), "+Z")
        if fid == "load_cut":
            _arrow(ax, fid, (0, z0), (0, z1))
        elif d == "apart":                               # tension in the segment: heads apart, on the screw axis
            zm = (z0 + z1) / 2
            _arrow(ax, fid, (us, zm), (us, z0))
            _arrow(ax, fid, (us, zm), (us, z1))
        else:                                            # compression cases: down onto the housing top, outer edge
            uh = us - g("ring.nut_housing_od") / 2
            _arrow(ax, fid, (uh, z1), (uh, z0))
        return
    if kind == "callout":                                # leader from the screw outline, label by the placer
        zc = pz.zs("(jackscrew.thread_start_z + jackscrew.thread_end_z) / 2")
        u0 = us - g("jackscrew.nominal") / 2
        sc.draw(fid, Line2D([u0, u0 - g("profile.width") / 2], [zc, zc], color=CALLOUT, linewidth=1), ax)
        return
    if z0 is None:
        return
    if row.get("section_u"):
        kw = {}
        if fid == "nut_c":
            kw = {"fill": True, "facecolor": BRASS}
        for ua, ub, za, zb in row["section_u"]:
            sc.draw_rect(ax, fid, pz.ev(ua), pz.ev(ub), pz.zs(za), pz.zs(zb), **kw)
        return
    if row.get("section"):
        if kind == "cone":
            narrows = next((s["narrows"] for s in row.get("sense", []) if s.get("pred") == "taper"), "up")
            tan_a = math.tan(math.radians(g("cone.alpha")))
            for r0, r1, lo, hi in _section_pieces(pz, row, z0, z1):
                t = (hi - lo) * tan_a
                pts = [(r0, lo), (r1, lo), (r1 - t, hi), (r0, hi)] if narrows == "up" else [(r0, lo), (r1 - t, lo), (r1, hi), (r0, hi)]
                for s in (-1, 1):
                    sc.draw(fid, Polygon([(s * x, zz) for x, zz in pts], closed=True, fill=False), ax)
            return
        mate = row.get("bore_cone")
        for r0, r1, lo, hi in _section_pieces(pz, row, z0, z1):
            if mate:                                     # holder bore follows the collet cone over the collet height
                tan_a = math.tan(math.radians(g("cone.alpha")))
                mz0, mz1 = pz.z(mate)
                mr1 = pz.ev(rows[mate]["section"][1])
                zk = min(mz1, hi)
                if lo < zk:
                    rc = lambda zz: mr1 - (zz - mz0) * tan_a  # noqa: E731
                    for s in (-1, 1):
                        sc.draw(fid, Polygon([(s * rc(lo), lo), (s * r1, lo), (s * r1, zk), (s * rc(zk), zk)], closed=True, fill=False), ax)
                    lo = zk
                if lo >= hi:
                    continue
            if fid == "bearing":                         # inner and outer race per side
                rm = (r0 + r1) / 2
                _mirror(ax, fid, r0, rm, lo, hi)
                _mirror(ax, fid, rm, r1, lo, hi)
            else:
                _mirror(ax, fid, r0, r1, lo, hi)
        return
    if fid == "gear":
        sc.draw_gear_section(ax, fid, g("gear.bore") / 2, g("gear.od") / 2, z0, z1)
        return
    if fid == "wingnut":                                 # body, two wings to the span, sweep radius dashed
        sc.draw_rect(ax, fid, -g("wingnut.body_od") / 2, g("wingnut.body_od") / 2, z0, z1)
        _mirror(ax, fid, g("wingnut.body_od") / 2, g("wingnut.span") / 2, z0, z0 + g("wingnut.wing_height"))
        r_sw = g("wingnut.sweep_clear_radius")
        sc.draw_rect(ax, fid, -r_sw, r_sw, z0, z1, linestyle=HIDDEN)
        return
    if fid == "core_750":
        u0, u1 = f["depth"]
        sc.draw_rect(ax, fid, u0, u1, z0, z1, linewidth=2)
        return
    if fid == "drill_head":                              # head outline and the cutter-teeth strip at the bottom
        u0, u1 = pz.u(fid)
        sc.draw_rect(ax, fid, u0, u1, z0, z1, linewidth=2)
        teeth = (g("drill.head_od") - g("drill.tube_od")) / 2
        sc.draw_rect(ax, fid, u0, u1, z0, z0 + teeth)
        return
    if fid == "pinion_c":                                # bevel pinion, toe toward the drill axis (TP-2 narrows inward)
        u0, u1 = pz.u(fid)
        inner, outer = (u0, u1) if abs(u0) < abs(u1) else (u1, u0)
        zc, h = (z0 + z1) / 2, (z1 - z0) * g("pinion.r_toe") / g("pinion.r_heel")
        sc.draw(fid, Polygon([(inner, zc - h / 2), (outer, z0), (outer, z1), (inner, zc + h / 2)], closed=True, fill=False), ax)
        return
    if fid in ("liftmotor_c", "liftmotor_pilot_c", "liftmotor_shaft_c", "coupling_c", "screw_end_c"):
        half = {"liftmotor_c": g("liftmotor.body") / 2, "liftmotor_pilot_c": g("liftmotor.pilot")[0] / 2,
                "liftmotor_shaft_c": g("liftmotor.shaft_od") / 2, "coupling_c": g("liftmotor.coupling_od") / 2,
                "screw_end_c": g("liftmotor.screw_end_d") / 2}[fid]
        kw = {"fill": True, "facecolor": GREY} if fid == "liftmotor_c" else {}
        sc.draw_rect(ax, fid, us - half, us + half, z0, z1, **kw)
        return
    if f.get("plan_pieces"):                             # standoffs: one elevation per plan piece (u = plan y)
        for pc in f["plan_pieces"]:
            ys = [p[1] for p in pc]
            sc.draw_rect(ax, fid, min(ys), max(ys), z0, z1)
        return
    if f.get("place"):
        u0, u1 = pz.u(fid)
        kw = {"fill": True, "facecolor": GREY} if fid == "motor23_c" else {}
        if fid == "motor_shaft_c":
            kw = {"fill": True, "facecolor": DARK}
        sc.draw_rect(ax, fid, u0, u1, z0, z1, **kw)
        return
    u0, u1 = f["depth"]
    sc.draw_rect(ax, fid, u0, u1, z0, z1)


def draw_subs(ax, pz, spec):
    """Declared sub-artists: the bearing line (mark, <row>:line at mark.z across the row's drawn width), ball circles in
    each drawn bearing piece (<row>:balls) and the switch lever (<row>:lever from lever.from to lever.to)."""
    for row in spec["features"]:
        if MAIN not in (row.get("axes") or [MAIN]):
            continue
        fid = row["id"]
        m = row.get("mark")
        if m and m.get("sub") == sc.MARK_SUB:
            u0, u1 = pz.u(fid)
            z = pz.zs(m["z"])
            sc.draw(f"{fid}:{sc.MARK_SUB}", Line2D([u0, u1], [z, z], color="k", linewidth=2, solid_capstyle="butt"), ax)
        if "balls" in (row.get("sub_artists") or []):
            for a in list(sc.tagged(ax).get(fid, [])):
                for poly in sc.artist_polys(a):
                    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
                    w, h = max(xs) - min(xs), max(ys) - min(ys)
                    sc.draw(f"{fid}:balls", Circle(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2), min(w, h) / 2 * 0.5,
                                                   fill=False, edgecolor="k", linewidth=1, zorder=2 * 2), ax)
        lv = row.get("lever")
        if lv and "lever" in (row.get("sub_artists") or []):
            pts = [(pz.ev(e[0]), pz.zs(e[1])) for e in (lv["from"], lv["to"])]
            sc.draw(f"{fid}:lever", Line2D([p[0] for p in pts], [p[1] for p in pts], color="k", linewidth=1), ax)


# ---------------------------------------------------------------- plan inset

def _inset_style(fid):
    pre = fid.rsplit("_", 1)[0] if fid[-2:] in ("_a", "_b", "_c") else fid
    if pre == "screw":
        return {"fill": True, "facecolor": "k", "edgecolor": "k", "zorder": sc.LABEL_FONTSIZE}
    if pre == "nut_housing":
        return {"edgecolor": RING_EDGE, "linewidth": 1, "zorder": sc.LABEL_FONTSIZE - 1}
    if pre == "frame_upper":
        return {"fill": True, "facecolor": "0.85", "edgecolor": "k", "hatch": "xx", "linewidth": 1, "zorder": 2}
    if pre in ("anchor", "liftmotor", "home_switch"):
        return {"edgecolor": DARK, "linewidth": 1, "zorder": 2 + 1}
    if fid == "keepout":
        return {"edgecolor": "red", "linestyle": HIDDEN, "linewidth": 1, "zorder": 2 * 2}
    if fid == "ring_ref":
        return {"edgecolor": RING_EDGE, "linestyle": HIDDEN, "linewidth": 1, "zorder": 2 * 2}
    return {"edgecolor": "k", "linewidth": 1, "zorder": sc.LABEL_FONTSIZE + 1}


def _line_kw(kw):
    out = {k: v for k, v in kw.items() if k in ("linestyle", "linewidth", "zorder")}
    out["color"] = kw.get("edgecolor", "k")
    return out


def draw_inset_row(ax, pz, row):
    P, g = pz.P, pz.P.get
    fid = row["id"]
    f = pz.feats.get(fid, {})
    kw = _inset_style(fid)
    kw.setdefault("fill", False)
    if row.get("kind") == "callout":                     # sync: leaders from the controller mark to the three lift motors
        hub = (-g("icd.footprint_x") / 2, g("icd.footprint_y") / 2)
        for m in row.get("leaders_to") or []:
            pl = pz.feats[m]["place"]
            c = (pl["r_c"] * check_stack.cosd(pl["theta"]), pl["r_c"] * check_stack.sind(pl["theta"]))
            sc.draw(fid, Line2D([hub[0], c[0]], [hub[1], c[1]], color=CALLOUT, linestyle=DOTTED, linewidth=1), ax)
        return
    if fid == "section_line":                            # cutting plane A-A on x = 0, look arrows toward -X, letters
        (x0, y0), (x1, y1) = f["plan_pieces"][0]
        sc.draw(fid, Line2D([x0, x1], [y0, y1], color="k", linestyle=CHAIN, linewidth=2), ax)
        L = g("profile.width")
        for y in (y0, y1):
            _arrow(ax, fid, (x0, y), (x0 - L, y), color="k")
            ax.text(x0 - L, y, "A", fontsize="small", ha="right", va="center", fontweight="bold")
        return
    if fid == "plan_axes":                               # +X, +Y marks (the theta arc lies outside the row's plan_poly: open item)
        for pc in f["plan_pieces"]:
            sc.draw(fid, Line2D([p[0] for p in pc], [p[1] for p in pc], color="k", linewidth=1), ax)
        L = g("profile.width")
        ax.text(L, 0, "+X", fontsize="x-small", ha="left", va="center")
        ax.text(0, L, "+Y", fontsize="x-small", ha="center", va="bottom")
        ax.text(L / 2, L / 2, "theta ccw from +X", fontsize="x-small", ha="left", va="bottom")
        return
    pl = f.get("place")
    if not pl:
        return
    th, r0, r1, w = pl["theta"], pl["r_in"], pl["r_out"], pl["half_width"]
    c, s = check_stack.cosd(th), check_stack.sind(th)
    if pl["footprint"] == "radial":
        sc.draw(fid, Polygon(check_stack.radial_corners(r0, r1, th, w, pl.get("rot", 0)), closed=True, **kw), ax)
        return
    cx, cy = pl["r_c"] * c, pl["r_c"] * s
    if row.get("projection") == "rectangle":             # NEMA 17 square inside its circumscribing footprint
        h = w / math.sqrt(2)
        sq = [(cx + a * c - b * s, cy + a * s + b * c) for a, b in ((-h, -h), (h, -h), (h, h), (-h, h))]
        sc.draw(fid, Polygon(sq, closed=True, **kw), ax)
    else:
        sc.draw(fid, Circle((cx, cy), w, **kw), ax)


# ---------------------------------------------------------------- figure

def _inset_right_of_labels(fig, ax, axi):
    """The inset keeps its declared size and height and moves right of the main Axes' label column (texts of the main
    Axes above the inset bottom), one label line clear, so no main label runs under the inset."""
    r = fig.canvas.get_renderer()
    p = axi.get_position()
    inv = fig.transFigure.inverted()
    right = p.x0
    for t in ax.texts:
        e = inv.transform(t.get_window_extent(r))
        if e[1][1] >= p.y0:
            right = max(right, e[1][0])
    gap = sc.LABEL_FONTSIZE / fig.dpi * sc.DPI / fig.get_figwidth() / sc.DPI
    axi.set_position([right + gap, p.y0, p.width, p.height])


def build(P, spec, stack):
    """check_sketch.py entry point: {pose id: Figure} (one figure at section_figure.pose)."""
    sf = spec.get("section_figure") or {}
    pid = sf.get("pose", "capture_end")
    pz = Pose(P, stack, pid)
    title = f"section A-A through screw c (x = 0, seen from +X; u = +Y), pose {pid}: cut case, tip {stack['poses'][pid]['tip_z_S']:.2f} z_S"
    fig, ax = sc.setup_figure(spec["view"], title=title, insets=spec.get("insets"))
    axi = next(a for a in fig.axes if getattr(a, "sketch_axes", None) == INSET)
    main_rows = [r for r in spec["features"] if MAIN in (r.get("axes") or [MAIN])]
    inset_rows = [r for r in spec["features"] if INSET in (r.get("axes") or [])]
    for row in main_rows:
        draw_section_row(ax, pz, spec, row)
    draw_subs(ax, pz, spec)
    for row in inset_rows:
        r2 = dict(row)
        r2["projection"] = (row.get("projection_by_axes") or {}).get(INSET, row.get("projection"))
        draw_inset_row(axi, pz, r2)
    ctx = sc.Ctx(P=P, spec=spec, figs={pid: fig}, stack=stack, view=spec["view"])
    sc.render_section(ctx, ax, pid)
    ictx = sc.axes_context(ctx, INSET)
    sctx = sc.axes_context(ctx, MAIN)
    sc.render_plan(ictx, axi, pid)
    sc.finish_axes(ax)
    ax.set_anchor("W")                                   # main Axes left; the inset holds the upper right
    g = P.get
    notes = [
        (None, f"section A-A: plane x = 0 through the drill axis and screw c at theta {g('jackscrew.angle')[2]:g} (u = r sin theta = "
               f"{g('jackscrew.pitch_radius') * check_stack.sind(g('jackscrew.angle')[2]):g}); viewer at +X, u = +Y right, z up (z_S plotted)"),
        (None, "hatch by material: aluminium //, extrusion xx, steel \\\\, brass .. ; unsectioned (screw, shafts, coupling, core, head):\n"
               "outline over the hatch; beyond the plane within one profile width (rear standoffs): solid, dashed behind cut parts;\n"
               "chain: nut stations at start and park; red: loads and the S3-2 span"),
        (None, spec["figure_note"].replace("; ", ";\n"), sc.NOTE_GID),
    ]
    sc.place_plan_labels(ax, sctx, pid, margin=True, stack_pose=pz.feats, notes=notes)
    _inset_right_of_labels(fig, ax, axi)
    sc.place_plan_labels(axi, ictx, pid, margin=True, stack_pose=pz.feats)
    return {pid: fig}


def main(argv=None):
    ap = argparse.ArgumentParser(description="S3 section A-A through screw c with the plan inset: write the PNG")
    ap.add_argument("--rev", type=int, default=1)
    a = ap.parse_args(argv)
    P = Params()
    spec = load_spec(HERE / "s3_spec.yaml")
    stack = check_stack.evaluate_spec(P, spec)
    name = (spec.get("section_figure") or {}).get("name", "s3_jackscrew_section")
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
