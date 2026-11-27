"""S4 section B-B through the base on the drill axis (contributor gameplan (sean) detail 1.4; Sean STOP S4-A, Design
Notes 34): section_yz (plane x = 0 seen from +X, u = +Y right, z up, z_S plotted), the S3 plane and machinery. One figure
per spec section_figures pose: carrier (figure 1: d 100 collet, 160 carrier, 100 mm core) and liner (figure 2: cast-on
liner in the d 105 collet).

Every artist through sc.draw with gid = spec row id (sub-artists <row>:<sub> as the spec declares them). Rows with
section_true are drawn piece by piece as their true section (sketch_common.section_true_polys, mirrored about u = 0,
plane_cuts applied, each piece named; sketch_common.draw_piece); base_plate from section_u; carrier, core_100 and
drill_head as unsectioned outlines over their depth bands; marks <row>:line at mark.z across the drawn width;
sub-artists collet:slits (form (a), wall tick), receiver:root, wingnut:wing (hidden, by x_band) and wingnut:sweep. Every
z comes from check_stack (z_S) or from the spec's z_A expressions converted once. The renderer section convention
(sketch_common.render_section) sets cut hatching by material, unsectioned outlines above the hatch and the occlusion
split. Labels go through the leader placer (sketch_common.place_plan_labels; sub-artist labels printed from their keys,
Designer P3a FIX 1); an UNPLACEABLE label is recorded by the placer (K4 record), never hand-placed.

  python s4_base_section.py [--rev k]   writes s4_base_section_r<k>.png and s4_liner_section_r<k>.png to wip/
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
from matplotlib.patches import Rectangle  # noqa: E402

MAIN = "section"
CHAIN = "-."
HIDDEN = "--"


class Pose:
    """Values of one pose: features (z_S), z_A names, spec expression evaluation (z_A) and conversion to z_S."""

    def __init__(self, P, stack, pid):
        self.P, self.pid = P, pid
        pr = stack["poses"][pid]
        self.feats, self.names = pr["features"], pr["vars_z_A"]

    def ev(self, e):
        return float(check_stack.eval_expr(str(e), self.P, self.names))

    def zs(self, e):
        return check_stack.to_shop_floor(self.ev(e), self.P)


def _slit_spec(rows, row):
    return sc.slit_spec(rows, row)


def draw_row(ax, pz, row):
    fid = row["id"]
    f = pz.feats.get(fid)
    if f is None:
        return
    z0, z1 = f.get("z_min"), f.get("z_max")
    if row.get("kind") == "line":
        u0, u1 = f.get("depth")
        if fid == "floor":
            sc.draw_hline(ax, fid, u0, u1, z0, color="k", linewidth=2)
        else:
            style = HIDDEN if fid == "line_min_core" else CHAIN   # shape: stop and kerf dash-dot, minimum core top dashed
            sc.draw_hline(ax, fid, u0, u1, z0, color="k", linestyle=style, linewidth=1)
        return
    if row.get("section_true"):
        for name, side, pts in sc.section_true_polys(pz.P, pz.names, row):
            sc.draw_piece(ax, fid, name, pts)
        return
    if row.get("section_u"):
        for ua, ub, za, zb in row["section_u"]:
            u0, u1 = sorted((pz.ev(ua), pz.ev(ub)))
            sc.draw_rect(ax, fid, u0, u1, pz.zs(za), pz.zs(zb))
        return
    if fid == "drill_head":   # head outline and the cutter-teeth strip at the bottom (as S3)
        u0, u1 = sorted(f["place"]["y"])
        sc.draw_rect(ax, fid, u0, u1, z0, z1, linewidth=2)
        teeth = (pz.P.get("drill.head_od") - pz.P.get("drill.tube_od")) / 2
        sc.draw_rect(ax, fid, u0, u1, z0, z0 + teeth)
        return
    u0, u1 = f["depth"]
    sc.draw_rect(ax, fid, u0, u1, z0, z1, linewidth=2 if row.get("section_class") == "unsectioned" else 1)


def _slit_u(pz, row, ln):
    """Form (a) (Designer/Topologist P2r): +u at the top-face mid-radius of the top piece; -u at r_mid sin(theta), r_mid
    the wall mid-radius at the line's mid-height (the cone piece's inner radius and its outer edge there)."""
    pcs = sc.section_true_polys(pz.P, pz.names, row, z_S=False)
    top = [pts for nm, s, pts in pcs if nm == "top" and s > 0][0]
    if ln["side"] == "+u":
        zt = max(v[1] for v in top)
        rs = [v[0] for v in top if abs(v[1] - zt) <= sc.TOL_Z]
        return (min(rs) + max(rs)) / 2
    za, zb = sorted((pz.ev(ln["from"]), pz.ev(ln["to"])))
    zm = (za + zb) / 2
    cone = [pts for nm, s, pts in pcs if nm == "cone" and s > 0][0]
    r_in = min(v[0] for v in cone)
    outer = sorted([v for v in cone if v[0] > r_in + sc.TOL_Z], key=lambda v: v[1])
    (ra, zra), (rb, zrb) = outer[0], outer[-1]
    r_out = ra + (rb - ra) * (zm - zra) / (zrb - zra)
    return (r_in + r_out) / 2 * math.sin(math.radians(pz.ev(ln["theta"])))


def _wall(pz, row, z, u):
    """The merged chord of the row's section_true pieces on the side of u at height z (z_S) that holds u (tick: wall)."""
    polys = [pts for nm, s, pts in sc.section_true_polys(pz.P, pz.names, row) if (s > 0) == (u > 0)]
    iv = sorted(c for c in (sc.poly_chord(p, z) for p in polys) if c)
    out = []
    for a, b in iv:
        if out and a <= out[-1][1] + sc.TOL_Z:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return next((a, b) for a, b in out if a - sc.TOL_Z <= u <= b + sc.TOL_Z)


def draw_subs(ax, pz, spec, rows_here):
    rows = {r["id"]: r for r in spec["features"]}
    for row in rows_here:
        fid = row["id"]
        subs = row.get("sub_artists") or []
        m = row.get("mark")
        if m and m.get("sub") == sc.MARK_SUB and sc.MARK_SUB in subs:
            xs = [v[0] for p in sc.pieces(ax, fid) for v in p]
            z = pz.zs(m["z"])
            sc.draw(f"{fid}:{sc.MARK_SUB}", Line2D([min(xs), max(xs)], [z, z], color="k", linewidth=1), ax)
        if "slits" in subs:
            sl = _slit_spec(rows, row)
            for ln in sl["lines"]:
                u = _slit_u(pz, row, ln)
                lo, hi = sorted((pz.zs(ln["from"]), pz.zs(ln["to"])))
                sc.draw(f"{fid}:slits", Line2D([u, u], [lo, hi], color="k", linestyle=HIDDEN, linewidth=1), ax)
                zc = lo if ln["open"] == "top" else hi
                t0, t1 = _wall(pz, row, zc, u)
                sc.draw(f"{fid}:slits", Line2D([t0, t1], [zc, zc], color="k", linestyle=HIDDEN, linewidth=1), ax)
        if "root" in subs:
            rt = row["root"]
            r = pz.ev(rt["r"])
            lo, hi = pz.zs(rt["from"]), pz.zs(rt["to"])
            for s in (-1, 1):
                sc.draw(f"{fid}:root", Line2D([s * r, s * r], [lo, hi], color="k", linestyle=HIDDEN, linewidth=1), ax)
        if "wing" in subs:
            w = row["wing"]
            u0, u1 = sorted(pz.ev(e) for e in w["u"])
            z0, z1 = sorted(pz.zs(e) for e in w["z"])
            sc.draw(f"{fid}:wing", Rectangle((u0, z0), u1 - u0, z1 - z0, fill=False, edgecolor="k", linestyle=HIDDEN, linewidth=1), ax)
        if "sweep" in subs:
            r = pz.ev(row["sweep"]["r"])
            ez = sc.extent_z(sc.pieces(ax, fid))
            for s in (-1, 1):
                sc.draw(f"{fid}:sweep", Line2D([s * r, s * r], list(ez), color="k", linestyle=HIDDEN, linewidth=1), ax)


def build(P, spec, stack):
    """check_sketch.py entry point: {pose id: Figure}, one figure per spec section_figures entry."""
    figs, pzs = {}, {}
    for fd in spec.get("section_figures") or [spec["section_figure"]]:
        pid = fd["pose"]
        pz = Pose(P, stack, pid)
        tip = stack["poses"][pid]["tip_z_S"]
        title = f"section B-B through the base (x = 0, seen from +X; u = +Y), pose {pid}: drill at the stop, tip {tip:.2f} z_S"
        fig, ax = sc.setup_figure(spec["view"], title=title, insets=spec.get("insets"))
        here = [r for r in spec["features"] if sc.applies(r, pid) and MAIN in (r.get("axes") or [MAIN])]
        for row in here:
            draw_row(ax, pz, row)
        draw_subs(ax, pz, spec, here)
        figs[pid], pzs[pid] = fig, pz
    ctx = sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"])
    sctx = sc.axes_context(ctx, MAIN)
    for fd in spec.get("section_figures") or [spec["section_figure"]]:
        pid = fd["pose"]
        fig = figs[pid]
        ax = next(a for a in fig.axes if getattr(a, "sketch_axes", None) == MAIN)
        sc.render_section(ctx, ax, pid)
        sc.finish_axes(ax)
        notes = [
            (None, f"section B-B: plane x = 0 through the drill axis (the S3 plane); viewer at +X, u = +Y right, z up (z_S plotted); "
                   f"{fd.get('note') or spec['section_figure'].get('note', '')}"),
            (None, "cut: hatched by material (legend in the note below); unsectioned (carrier, core, drill head): outline over the hatch;\n"
                   "dashed: slit ticks behind the plane, receiver thread root lines, the -X wing of the wing nut (behind its own body),\n"
                   "sweep r lines, edges behind an unsectioned outline; dash-dot: cutter stop and kerf-centre lines"),
            (None, spec["figure_note"].replace("; ", ";\n"), sc.NOTE_GID),
        ]
        sc.place_plan_labels(ax, sctx, pid, margin=True, stack_pose=pzs[pid].feats, notes=notes, edge_leaders=True, collinear=True)
    return figs


def main(argv=None):
    ap = argparse.ArgumentParser(description="S4 section B-B through the base: write one PNG per section figure")
    ap.add_argument("--rev", type=int, default=1)
    a = ap.parse_args(argv)
    P = Params()
    spec = load_spec(HERE / "s4_spec.yaml")
    stack = check_stack.evaluate_spec(P, spec)
    names = {fd["pose"]: fd["name"] for fd in spec.get("section_figures") or [spec["section_figure"]]}
    out = []
    for pid, fig in build(P, spec, stack).items():
        path = output_path(f"{names[pid]}_r{a.rev}.png")   # wip/ (sketch_loader output rule)
        fig.savefig(path, bbox_inches="tight")
        out.append(path)
    for p in out:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
