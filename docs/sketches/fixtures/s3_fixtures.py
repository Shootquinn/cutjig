"""Controls for 1.3 (c) (P4): TP-7 per-Axes views, the section view (section_yz), the renderer section convention, the
S3-x fixtures from the signed spec (S3-1 to S3-3), the K5 mark admission (Topologist P0T section 4) and declared
sub-artists, SYM (screw-set symmetry lint), the narrowed x1_exempt and the --accept refusal on a remaining exemption.

The S3 fixture draws every row of the signed s3_spec.yaml faithfully from check_stack values: the section Axes in the
section frame (u = plan y, the place / plan_poly y extent; section_u pieces as drawn; axis-Z section rows mirrored about
u = 0), the plan inset with the S2 fixture's plan drawer, the bearing line (mark), the balls and the switch lever, and the
renderer section convention (sketch_common.render_section) and plan renderer (render_plan) applied. Each B plants one
defect on top of that drawing, or edits the spec / params and draws faithfully (a spec or params decision drawn).
1.3 P6: the P4/P5f scaffolding is gone (p4_spec_findings, _receiver_cert, _plate_g, _post_p6_specs, the pre-P4 figure
fallback): the live specs carry F2, F3, the mirror_about_radial declaration, the receiver shoulder (Design Notes 32) and
the 42-square anchors in all three specs, so every fixture draws the live specs.
"""
import copy
import json
import math
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SK = HERE.parent
for p in (str(SK), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params, load_spec  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle  # noqa: E402

S3_SPEC = SK / "s3_spec.yaml"
CHECK_STACK_PATH = SK / "check_stack.py"
INSET = "inset_plan"
MAIN = "section"
VIEW_LABELS_FALLBACK = ("x (mm)", "y (mm)")


def _builders():
    import builders   # the K-control fixtures (S2 plan drawer, S1 fixture); loaded as a plain module here
    return builders


# ---------------------------------------------------------------- figure (with a pre-P4 fallback for red-first runs)

def _figure(spec, title):
    return sc.setup_figure(spec["view"], title=title, insets=spec.get("insets"))


def _axes(fig, aid):
    return next((a for a in fig.axes if getattr(a, "sketch_axes", None) == aid), fig.axes[0] if aid == MAIN else None)


def _rows_of(spec, aid):
    return [r for r in spec["features"] if aid in (r.get("axes") or [MAIN])]


def _reflect(rec):
    """Section frame of a stack record (as sketch_common.reflect_record; local so the fixture runs on pre-P4 code)."""
    r = dict(rec)
    if rec.get("place"):
        r["u"] = list(rec["place"]["y"])
    if rec.get("plan_pieces"):
        r["u_pieces"] = [(min(p[1] for p in pc), max(p[1] for p in pc)) for pc in rec["plan_pieces"]]
    return r


def _arrow(ax, fid, tail, head):
    return sc.draw(fid, FancyArrowPatch(tail, head, arrowstyle="-|>", mutation_scale=8, shrinkA=0, shrinkB=0, lw=1.2), ax)


def _draw_section_row(ax, P, spec, stack, pid, row):
    b = _builders()
    fid = row["id"]
    f = stack["poses"][pid]["features"].get(fid)
    if f is None:
        return
    pr = stack["poses"][pid]
    names, shift = pr["vars_z_A"], pr["tip_z_S"] - pr["tip_z_A"]
    ev = lambda e: check_stack.eval_expr(e, P, names)  # noqa: E731
    fr = _reflect(f)
    kind = row.get("kind")
    z0, z1 = f.get("z_min"), f.get("z_max")
    if fid == "keepout":
        r = P.get("icd.keepout_radius")
        for u in (-r, r):
            sc.draw(fid, Line2D([u, u], [z0, z1], linestyle="--"), ax)
        return
    if kind == "line":
        if z0 is None:
            return
        if abs(z1 - z0) <= 1e-9:
            u0, u1 = fr.get("u") or f.get("depth") or (-100.0, 100.0)
            sc.draw_hline(ax, fid, u0, u1, z0)
        else:
            uc = sum(fr["u"]) / 2 if fr.get("u") else 0.0
            sc.draw(fid, Line2D([uc, uc], [z0, z1]), ax)
        return
    if kind == "arrow":
        us = P.get("jackscrew.pitch_radius") * check_stack.sind(P.get("jackscrew.angle")[2])
        d = next((p["dir"] for p in row.get("sense") or [] if p.get("pred") == "points"), "+Z")
        if fid == "load_cut":
            _arrow(ax, fid, (0.0, z0), (0.0, z1))
        elif d == "apart":
            zm = (z0 + z1) / 2
            _arrow(ax, fid, (us - 20, zm), (us - 20, z0))
            _arrow(ax, fid, (us - 20, zm), (us - 20, z1))
        elif d == "-Z":
            _arrow(ax, fid, (us - 20, z1), (us - 20, z0))
        else:
            _arrow(ax, fid, (us - 20, z0), (us - 20, z1))
        return
    if kind == "callout":
        t = ax.text(-300, 900, row.get("name", fid), fontsize=6)
        t.set_gid(fid)
        return
    if z0 is None:
        return
    if row.get("section_u"):
        for pc in row["section_u"]:
            u0, u1 = ev(pc[0]), ev(pc[1])
            lo, hi = ev(pc[2]) + shift, ev(pc[3]) + shift
            sc.draw_rect(ax, fid, u0, u1, lo, hi)
        return
    if row.get("section"):
        b._draw_section(ax, P, spec, stack, pid, row, z0, z1)
        return
    if kind == "gear" and row.get("axis") == "Z":
        r_out = P.get("gear.od") / 2 if P.has("gear.od") else P.get("gear.pitch_diameter") / 2
        sc.draw_gear_section(ax, fid, P.get("gear.bore") / 2, r_out, z0, z1)
        return
    if fr.get("u"):
        u0, u1 = fr["u"]
        if kind == "gear":
            inner, outer = (u0, u1) if abs(u0) < abs(u1) else (u1, u0)
            h = z1 - z0
            sc.draw(fid, Polygon([(inner, z0 + h / 4), (outer, z0), (outer, z1), (inner, z1 - h / 4)], closed=True, fill=False), ax)
        else:
            sc.draw_rect(ax, fid, u0, u1, z0, z1)
        return
    if fr.get("u_pieces"):
        for u0, u1 in fr["u_pieces"]:
            sc.draw_rect(ax, fid, u0, u1, z0, z1)
        return
    u0, u1 = f["depth"]
    sc.draw_rect(ax, fid, u0, u1, z0, z1)


def _draw_subs(ax, P, spec, stack, pid):
    """Bearing line (mark, anchor_bearing_c:line, at mark.z across the bearing OD), balls (one Circle centred in each drawn
    bearing piece, radius 0.3 of its short side) and the switch lever (lever.from to lever.to)."""
    pr = stack["poses"][pid]
    names, shift = pr["vars_z_A"], pr["tip_z_S"] - pr["tip_z_A"]
    rows = {r["id"]: r for r in spec["features"]}
    for fid, row in rows.items():
        if MAIN not in (row.get("axes") or [MAIN]):
            continue
        m = row.get("mark")
        if m and m.get("sub") == "line":
            u0, u1 = _reflect(pr["features"][fid])["u"]
            z = check_stack.eval_expr(m["z"], P, names) + shift
            sc.draw(f"{fid}:line", Line2D([u0, u1], [z, z], color="k", lw=1.5), ax)
        if "balls" in (row.get("sub_artists") or []):
            for a in sc.tagged(ax).get(fid, []):
                for poly in sc.artist_polys(a):
                    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
                    w, h = max(xs) - min(xs), max(ys) - min(ys)
                    sc.draw(f"{fid}:balls", Circle(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2), 0.3 * min(w, h), fill=False), ax)
        lv = row.get("lever")
        if lv and "lever" in (row.get("sub_artists") or []):
            pts = [(check_stack.eval_expr(e[0], P, names), check_stack.eval_expr(e[1], P, names) + shift) for e in (lv["from"], lv["to"])]
            sc.draw(f"{fid}:lever", Line2D([p[0] for p in pts], [p[1] for p in pts]), ax)
        ex = row.get("ext")
        if ex and "ext" in (row.get("sub_artists") or []):   # 1.3 (h) r3 (Designer r2 item 3): screw edge to the line + 2
            sp = _reflect(pr["features"][ex["screw"]])
            uc, half = sum(sp["u"]) / 2, pr["features"][ex["screw"]]["place"]["half_width"]
            ud = sum(_reflect(pr["features"][fid])["u"]) / 2
            side = 1 if ud > uc else -1
            for zz in (pr["features"][fid]["z_min"], pr["features"][fid]["z_max"]):
                sc.draw(f"{fid}:ext", Line2D([uc + side * half, ud + side * 2], [zz, zz]), ax)
        rt = row.get("root")
        if rt and "root" in (row.get("sub_artists") or []):   # 1.3 (h) r2 (TP1.3-15)
            uc = sum(_reflect(pr["features"][fid])["u"]) / 2
            d = check_stack.eval_expr(rt["d"], P, names)
            z0, z1 = (check_stack.eval_expr(rt[k], P, names) + shift for k in ("from", "to"))
            for s_ in (-1, 1):
                sc.draw(f"{fid}:root", Line2D([uc + s_ * d / 2] * 2, [z0, z1], linestyle="--"), ax)


def _draw_inset(ax, P, spec, stack, pid, inset_rows):
    b = _builders()
    for row in inset_rows:
        fid = row["id"]
        if row.get("kind") == "callout":
            t = ax.text(-320, 300, row.get("name", fid), fontsize=5)
            t.set_gid(fid)
            continue
        r2 = dict(row)
        pba = row.get("projection_by_axes") or {}
        if INSET in pba:
            r2["projection"] = pba[INSET]
        b._s2_draw_row(ax, P, spec, stack, pid, r2)
        arc = row.get("arc")
        if arc and "arc" in (row.get("sub_artists") or []):   # 1.3 (h) r2 (TP1.3-13)
            _draw_arc(ax, P, row)
        if fid == "section_line":
            L = P.get("icd.footprint_y") / 2
            for y in (-L, L):
                _arrow(ax, fid, (0.0, y), (-40.0, y))


def _draw_arc(ax, P, row, reverse=False, dr=0.0, gid=None, head_from=None):
    """The arc line and, as the live script draws it (Topologist R2-3), a head arrow from head_from (default theta1 - 10)
    to theta1 on the circle."""
    arc = row["arc"]
    r = check_stack.eval_expr(str(arc["r"]), P, {}) + dr
    t0, t1 = float(arc["theta0"]), float(arc["theta1"])
    ts = [t0 + (t1 - t0) * k / 90 for k in range(91)]
    if reverse:
        ts = ts[::-1]
    g = gid or f"{row['id']}:arc"
    a = sc.draw(g, Line2D([r * math.cos(math.radians(t)) for t in ts], [r * math.sin(math.radians(t)) for t in ts]), ax)
    tb = t1 - 10 if head_from is None else head_from
    pt = lambda t: (r * math.cos(math.radians(t)), r * math.sin(math.radians(t)))  # noqa: E731
    sc.draw(g, FancyArrowPatch(pt(tb), pt(t1), arrowstyle="-|>", mutation_scale=8, shrinkA=0, shrinkB=0), ax)
    return a


FIXTURE_ALT = "--"   # the live section.hatch_alt aluminium (Designer r2 pick 4, orchestrator ruling 1.3 (h) r3), for plants


def _ctx_of(P, spec, stack, figs):
    return sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], script_paths=[], check_stack_path=CHECK_STACK_PATH)


def s3_draw(P, spec, stack, mutate=None, render=True, subs=True, skip=()):
    pid = (spec.get("section_figure") or {}).get("pose", "capture_end")
    fig, ax = _figure(spec, f"S3 fixture, section A-A at pose {pid}")
    axi = _axes(fig, INSET)
    for row in _rows_of(spec, MAIN):
        if row["id"] not in skip:
            _draw_section_row(ax, P, spec, stack, pid, row)
    if subs:
        _draw_subs(ax, P, spec, stack, pid)
    if axi is not None:
        _draw_inset(axi, P, spec, stack, pid, [r for r in _rows_of(spec, INSET) if r["id"] not in skip])
    figs = {pid: fig}
    if render and hasattr(sc, "render_section"):
        rc = _ctx_of(P, spec, stack, figs)
        sc.render_section(rc, ax, pid)
        ic = sc.axes_context(rc, INSET)
        if ic is not None and axi is not None:
            sc.render_plan(ic, axi, pid)
    if spec.get("figure_note"):
        # 1.3 P6: one note line per not_drawn part, inside the Axes (the fixture is held to the canvas; the P6 note is longer)
        ax.text(0, 0, spec["figure_note"].replace("; ", ";\n"), transform=ax.transAxes, fontsize=5, va="bottom").set_gid(sc.NOTE_GID)
    sc.finish_axes(ax)
    if mutate:
        mutate(fig, ax, axi, P, spec, stack, pid)
    return figs


def s3_ctx(spec_mut=None, values=None, mutate=None, render=True, subs=True, skip=(), records=None, specs=None, spec=None):
    """Live S3 spec drawn faithfully (one figure at section_figure.pose). spec_mut(spec), values {key: value} as the S1/S2
    fixtures (a spec or params decision drawn faithfully); mutate(fig, ax, axi, P, spec, stack, pid) plants a drawing
    defect after the faithful draw. records: directory S3-3 reads; specs: the {name: spec} SYM reads."""
    P = Params()
    for k, v in (values or {}).items():
        P.leaves[k] = dict(P.leaves[k], value=v)
    spec = copy.deepcopy(spec) if spec is not None else load_spec(S3_SPEC)
    if spec_mut:
        spec_mut(spec)
    stack = check_stack.evaluate_spec(P, spec)
    figs = s3_draw(P, spec, stack, mutate=mutate, render=render, subs=subs, skip=skip)
    c = _ctx_of(P, spec, stack, figs)
    if records is not None:
        c.records_dir, c.wip_dir = records, records
    if specs is not None:
        c.specs = specs
    return c


def s3_fixed():
    """Z for K5, K8, S3-1, S3-2 per Axes: the live spec drawn faithfully (1.3 P6: the P4 findings F2, F3 are in the spec,
    so this is the s3_live drawing)."""
    return s3_live()


_LIVE = {}


def s3_live():
    """Z: the signed S3 spec drawn faithfully (section Axes, inset, renderer section convention)."""
    if "c" not in _LIVE:
        _LIVE["c"] = s3_ctx()
    return _LIVE["c"]


# ---------------------------------------------------------------- TP-7 (per-Axes views)

def _first(ax, fid):
    return sc.tagged(ax)[fid][0]


def tp7_inset_y_inverted():
    """B (TP-7, handedness): the inset drawn correctly, then its y axis inverted."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: axi.invert_yaxis())


def tp7_screw_rect_in_inset():
    """B (TP-7, projection): screw_a drawn as a rectangle (its inscribed square) in the plan inset, where its projection
    is a circle."""
    def m(fig, ax, axi, P, spec, stack, pid):
        a = _first(axi, "screw_a")
        cx, cy = a.center
        r = a.radius / math.sqrt(2)
        a.remove()
        sc.draw("screw_a", Rectangle((cx - r, cy - r), 2 * r, 2 * r, fill=False), axi)
    return s3_ctx(mutate=m)


def tp7_inset_row_in_main():
    """B (TP-7): screw_a (an inset-only row) drawn in the main (section) Axes as well as in the inset."""
    def m(fig, ax, axi, P, spec, stack, pid):
        sc.draw_rect(ax, "screw_a", 74, 86, 325, 1225)
    return s3_ctx(mutate=m)


def tp7_inset_absent():
    """B (TP-7): the declared inset Axes removed from the figure (its rows drawn nowhere)."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: fig.delaxes(axi))


def tp7_undeclared_axes():
    """B (TP-7): a third Axes with no declared id added to the S3 figure."""
    def m(fig, ax, axi, *a):
        fig.add_axes([0.05, 0.05, 0.1, 0.1])
    return s3_ctx(mutate=m)


# ---------------------------------------------------------------- section view

def _mirror_main(fig, ax, axi, *a):
    for art in sc.artists(ax):
        if isinstance(art, Line2D):
            art.set_xdata([-x for x in art.get_xdata()])
        elif isinstance(art, Rectangle):
            x, w = art.get_x(), art.get_width()
            art.set_x(-(x + w))
        elif isinstance(art, Polygon):
            art.set_xy([(-x, y) for x, y in art.get_xy()])
        elif isinstance(art, FancyArrowPatch):
            (x0, y0), (x1, y1) = art._posA_posB
            art.set_positions((-x0, y0), (-x1, y1))
        elif isinstance(art, Circle):
            art.center = (-art.center[0], art.center[1])


def section_mirrored():
    """B (O4): the section drawn mirrored (u -> -u: viewed from -X); every placed off-axis row lands on the wrong side."""
    return s3_ctx(mutate=_mirror_main)


def section_side_projection():
    """B (O4): screw_c placed at x = r cos(theta) = 0 (the side-view projection) instead of its plane coordinate
    u = r sin(theta) = -160: every screw_c piece shifted +160 in u."""
    def m(fig, ax, axi, *a):
        for art in sc.tagged(ax).get("screw_c", []):
            art.set_x(art.get_x() + 160.0)
    return s3_ctx(mutate=m)


# ---------------------------------------------------------------- renderer section convention

def conv_cut_unhatched():
    """B (convention 1): the ring (cut, aluminium) drawn without its hatch."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: [x.set_hatch(None) for x in sc.tagged(ax)["ring"][:1]])


def conv_cut_wrong_hatch():
    """B (convention 1): the nut (brass) hatched with the steel pattern."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: [x.set_hatch(sc.HATCH["steel"] if hasattr(sc, "HATCH") else "\\\\") for x in sc.tagged(ax)["nut_c"][:1]])


def conv_unsectioned_hatched():
    """B (convention 2): screw_c (unsectioned, axis in the plane) drawn hatched."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: sc.tagged(ax)["screw_c"][0].set_hatch("//"))


def conv_unsectioned_under():
    """B (convention 2): the coupling (unsectioned) drawn at zorder 0.5, under the cut hatch."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: sc.tagged(ax)["coupling_c"][0].set_zorder(0.5))


def conv_beyond_hidden_solid():
    """B (convention 3): one standoff (beyond) drawn wholly behind the anchor block (cut), solid."""
    def m(fig, ax, axi, *a):
        art = sc.tagged(ax)["standoffs_c"][0]
        art.set_y(330.0)
        art.set_height(20.0)
        art.set_linestyle("-")
    return s3_ctx(mutate=m)


def conv_beyond_visible_dashed():
    """B (convention 3, converse): a visible standoff drawn dashed."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: sc.tagged(ax)["standoffs_c"][0].set_linestyle("--"))


def conv_front_drawn():
    """B (convention 4): a row in front of the plane drawn in the section (screw b set, theta 30, x +138.6: spec row
    screw_b_front, a copy of screw_b declared in the section Axes, drawn faithfully)."""
    def sm(spec):
        rb = copy.deepcopy(next(r for r in spec["features"] if r["id"] == "screw_b"))
        rb.update(id="screw_b_front", axes=[MAIN], section_class="unsectioned", projection="rectangle", projection_by_axes=None, sense=[], label=None)
        spec["features"].append(rb)
    return s3_ctx(spec_mut=sm)


# ---------------------------------------------------------------- sub-artists (balls, lever) in the section

def sub_balls_undeclared():
    """B: balls drawn on guide_c, whose row declares no sub_artists."""
    def m(fig, ax, axi, *a):
        p = sc.artist_polys(sc.tagged(ax)["guide_c"][0])[0]
        xs, ys = [q[0] for q in p], [q[1] for q in p]
        sc.draw("guide_c:balls", Circle(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2), 1.0, fill=False), ax)
    return s3_ctx(mutate=m)


def sub_ball_outside():
    """B: one anchor bearing ball moved 10 mm outboard, outside the drawn bearing pieces."""
    def m(fig, ax, axi, *a):
        b = sc.tagged(ax)["anchor_bearing_c:balls"][0]
        b.center = (b.center[0] - 10.0, b.center[1])
    return s3_ctx(mutate=m)


def sub_lever_off():
    """B: the home-switch lever drawn with its upper end 5 mm low against lever.to."""
    def m(fig, ax, axi, *a):
        ln = sc.tagged(ax)["home_switch_c:lever"][0]
        ys = list(ln.get_ydata())
        ln.set_ydata([ys[0], ys[1] - 5.0])
    return s3_ctx(mutate=m)


# ---------------------------------------------------------------- S3-x fixtures

def s3_1_b1():
    """S3-1 B: anchor moved to the top guide (screw hung from the top): the bearing line drawn at the guide bearing line
    jackscrew.guide_bearing_z, above the nut at every S1 pose."""
    def m(fig, ax, axi, P, spec, stack, pid):
        ln = sc.tagged(ax)["anchor_bearing_c:line"][0]
        z = P.get("jackscrew.guide_bearing_z") + P.get("jig.datum_a_above_floor")
        ln.set_ydata([z, z])
    return s3_ctx(mutate=m)


def s3_1_b2():
    """S3-1 B: the cut arrow drawn pointing down (-Z): the cut-case sign of the load reversed."""
    def m(fig, ax, axi, *a):
        art = sc.tagged(ax)["load_cut"][0]
        (x0, y0), (x1, y1) = art._posA_posB
        art.set_positions((x1, y1), (x0, y0))
    return s3_ctx(mutate=m)


def s3_2_z2():
    """S3-2 Z: a 100 mm column under W (guide bearing line 100 above the anchor bearing line), drawn faithfully."""
    P = Params()
    return s3_ctx(values={"jackscrew.guide_bearing_z": P.get("jackscrew.anchor_bearing_z") + 100})


def s3_2_b1():
    """S3-2 B (the ruling's equivalent of [DN23] "1000 N compression on an 850 mm T8 buckles"): T8 root diameter 6.2 on an
    850 mm anchor-to-guide span, the Design Notes 31 cases at K 0.7, SF 3, drawn faithfully."""
    P = Params()
    return s3_ctx(values={"jackscrew.root_diameter": 6.2, "jackscrew.guide_bearing_z": P.get("jackscrew.anchor_bearing_z") + 850})


# ---- S3-3: records and the live specs (1.3 P6: the 42-square anchors in all three specs, no x1_exempt)

def _live_specs():
    """The three live specs (the state SYM certifies from 1.3 P6), fresh copies a fixture may edit."""
    return {n: load_spec(SK / f"{n}_spec.yaml") for n in ("s1", "s2", "s3")}


def check_sketch_mod():
    import check_sketch
    return check_sketch


def _records_dir(t, s1_mut=None, s2_mut=None):
    """Temporary docs directory with the accepted S1 r7 and S2 r5 records, keys_read refreshed to the live params and
    overlay (standing for S1 r8 / S2 r9 with the same K7 entries), each optionally mutated."""
    P = Params()
    for name, mut in (("s1_checks_r7.json", s1_mut), ("s2_checks_r5.json", s2_mut)):
        rec = json.loads((SK / name).read_text(encoding="utf-8"))
        rec.pop("superseded_by", None)
        rec["accepted"] = True
        for k, v in rec["keys_read"].items():
            if P.has(k):
                v["value"] = P.get(k)
        if mut:
            mut(rec)
        (Path(t) / name).write_text(json.dumps(rec), encoding="utf-8")
    return Path(t)


_TMP = []


def _new_tmp():
    """A fresh records directory; the previous fixture's directory (its control already judged) is removed first."""
    _cleanup_tmp()
    del _TMP[:]
    t = tempfile.mkdtemp(prefix="s3_3_")
    _TMP.append(t)
    return t


def _cleanup_tmp():
    """P5f: the S3-3 fixtures' temporary record directories are removed at interpreter exit (they leaked at P4)."""
    import shutil
    for t in _TMP:
        shutil.rmtree(t, ignore_errors=True)


import atexit  # noqa: E402
atexit.register(_cleanup_tmp)


def _s3_3_ctx(s1_mut=None, s2_mut=None, mutate=None):
    t = _new_tmp()
    sp = _live_specs()
    return s3_ctx(spec=sp["s3"], mutate=mutate, records=_records_dir(t, s1_mut, s2_mut), specs=sp)


def s3_3_z():
    """S3-3 Z: the signed spec (post-P6 symmetry state) drawn faithfully, records fresh: every link of chains c, a, b
    closed (S1/S2 K7, this section's K7 with the nut face, declared links listed, a/b screw-set links by symmetry)."""
    return _s3_3_ctx()


def s3_3_b1():
    """S3-3 B: member c drawn 1 mm clear of its foot on the -Y rail (loop open in the section)."""
    def m(fig, ax, axi, *a):
        for art in sc.tagged(ax)["frame_upper_c"]:
            art.set_y(art.get_y() + 1.0)
    return _s3_3_ctx(mutate=m)


def _drop_pair(pairs):
    def m(rec):
        k7 = next(c for c in rec["checks"] if c["id"] == "K7")
        keep = [i for i, t in enumerate(k7["tests"]) if t[1] not in pairs]
        k7["tests"] = [k7["tests"][i] for i in keep]
        k7["states"] = [k7["states"][i] for i in keep]
    return m


BP_BF = ("base_frame|base_plate", "base_plate|base_frame")


def s3_3_b2():
    """S3-3 B: a chain pair absent from every record. 1.3 (h) r2 re-plant (the base route no longer runs through the
    holder, TP1.3-10): the S1 and S2 records without base_plate|base_frame (chain c link 7, face_record, no other
    certifier)."""
    return _s3_3_ctx(s1_mut=_drop_pair(BP_BF), s2_mut=_drop_pair(BP_BF))


def s3_3_b3():
    """S3-3 B: stale records: the S1 record with jackscrew.lead recorded 8 (the T8x8 value) against the live 3. 1.3 (h) r2
    re-plant: the S2 record stale too (jackscrew.nominal recorded 8), since every record-certified link of the rerouted
    chains names both records."""
    def m(rec):
        rec["keys_read"]["jackscrew.lead"]["value"] = 8
    def m2(rec):
        rec["keys_read"]["jackscrew.nominal"]["value"] = 8
    return _s3_3_ctx(s1_mut=m, s2_mut=m2)


# ---------------------------------------------------------------- SYM

def sym_z():
    """SYM Z: the three specs in the post-P6 state (no exemption, anchor place and key lists equal across a, b, c)."""
    return check_sketch_mod().sym_lint(_live_specs())


def sym_b1():
    """SYM B: x1_exempt on S3 anchor_b."""
    sp = _live_specs()
    next(r for r in sp["s3"]["features"] if r["id"] == "anchor_b")["x1_exempt"] = {"reason": "planted"}
    return check_sketch_mod().sym_lint(sp)


def sym_b2():
    """SYM B: S2 screw_a placed at jackscrew.angle[0] (the b index)."""
    sp = _live_specs()
    next(r for r in sp["s2"]["features"] if r["id"] == "screw_a")["place"]["theta"] = "jackscrew.angle[0]"
    return check_sketch_mod().sym_lint(sp)


def sym_b3():
    """SYM B: S2 nut_housing_b z_max 1 higher than nut_housing_c."""
    sp = _live_specs()
    r = next(r for r in sp["s2"]["features"] if r["id"] == "nut_housing_b")
    r["z_rule"]["z_max"] = r["z_rule"]["z_max"] + " + 1"
    return check_sketch_mod().sym_lint(sp)


def sym_live():
    """SYM on the live specs (expected red until P6: S3 anchor exemptions, S1 screw key lists)."""
    return check_sketch_mod().sym_lint()


# ---------------------------------------------------------------- x1_exempt narrowed; --accept refusal

def x1_b3():
    """X1 B: S3 anchor_c (x1_exempt) with z_max 1 higher than S2 anchor_c: the exemption covers place only."""
    cs = check_sketch_mod()
    sp = cs.specs_in(SK) if hasattr(cs, "specs_in") else {p.stem.replace("_spec", ""): load_spec(p) for p in sorted(SK.glob("s*_spec.yaml"))}
    r = next(r for r in sp["s3"]["features"] if r["id"] == "anchor_c")
    r["z_rule"]["z_max"] = r["z_rule"]["z_max"] + " + 1"
    return cs.x1_lint(sp)


def h1_b_exempt():
    """H1 B: --accept with a spec in docs/ carrying x1_exempt (the live s3_spec.yaml copied with x1_exempt planted on
    anchor_a, anchor_b, anchor_c; re-planted at 1.3 P6, the live spec has none): refused, nothing written."""
    import step0_fixtures as s0
    cs = check_sketch_mod()
    rec = s0._template()
    with tempfile.TemporaryDirectory() as t:
        docs, wip = s0._dirs(t)
        txt = S3_SPEC.read_text(encoding="utf-8")
        for fid in ("anchor_a", "anchor_b", "anchor_c"):   # 1.3 P6: the exemption planted (the live spec has none)
            i = txt.index(f"\n- id: {fid}\n")
            j = txt.index("\n  kind:", i)
            txt = txt[:j] + "\n  x1_exempt: {reason: planted}" + txt[j:]
        (Path(docs) / "s3_spec.yaml").write_text(txt, encoding="utf-8")
        s0._write(wip, rec)
        rc, msgs = cs.accept("s1", 4, s0.NOTE, docs, wip, out=s0._quiet)
        flagged = json.loads((Path(wip) / "s1_checks_r4.json").read_text(encoding="utf-8")).get("accepted")
        written = sorted(p.name for p in Path(docs).iterdir() if p.name != "s3_spec.yaml")
        fired = rc != 0 and not flagged and not written
        return s0._res("H1", fired, " / ".join(msgs) + (f"; flagged {flagged}, docs/ {written}" if not fired else ""), 1 if fired else 0)


# ---------------------------------------------------------------- K5 mark admission on S1 (Topologist P0T section 4)

def _s1_marks(spec_mut=None, mark_fn=None, mutate=None):
    """S1 fixture (builders._s1_ctx) with the bearing line of each anchor row that declares `mark` drawn by rule: a
    two-vertex Line2D <row>:line at mark.z across the drawn block (its x extent), per pose. mark_fn(pose, fid, ax, x0, x1,
    z) replaces the rule drawing for one mark; mutate(ctx) edits the figures after."""
    b = _builders()
    base = load_spec(SK / "s1_spec.yaml")
    marks = {r["id"]: r["mark"] for r in base["features"] if r.get("mark")}
    c = b._s1_ctx(spec_mut=spec_mut)
    for pid, fig in c.figs.items():
        ax = fig.axes[0]
        names = c.stack["poses"][pid]["vars_z_A"]
        for fid, m in marks.items():
            arts = sc.tagged(ax).get(fid)
            if not arts:
                continue
            x0, x1 = sc.extent_x([p for a in arts for p in sc.artist_polys(a)])
            z = check_stack.to_shop_floor(check_stack.eval_expr(m["z"], c.P, names), c.P)
            if mark_fn and mark_fn(pid, fid, ax, x0, x1, z):
                continue
            sc.draw(f"{fid}:line", Line2D([x0, x1], [z, z], color="k", lw=2, solid_capstyle="butt"), ax)
    if mutate:
        mutate(c)
    return c


def mark_z():
    """K5 Z (P0T fixture Z): S1 with both anchor marks drawn by rule."""
    return _s1_marks()


def mark_b1():
    """B-m1 (M1): anchor_a:line drawn, mark deleted from the anchor_a row."""
    def sm(spec):
        next(r for r in spec["features"] if r["id"] == "anchor_a").pop("mark", None)
    return _only_load(_s1_marks(spec_mut=sm))


def _only_load(c):
    """Keep the load pose figure only (one planted issue per control)."""
    c.figs = {"load": c.figs["load"]}
    return c


def mark_b2():
    """B-m2 (M2): anchor_a:line drawn, the anchor_a block artist removed at load."""
    def mu(c):
        ax = c.figs["load"].axes[0]
        for a in list(sc.tagged(ax)["anchor_a"]):
            a.remove()
    return _only_load(_s1_marks(mutate=mu))


def mark_b3a():
    """B-m3a (M3 type): the anchor_a mark drawn as a zero-height Rectangle under anchor_a:line."""
    def mf(pid, fid, ax, x0, x1, z):
        if fid != "anchor_a":
            return False
        sc.draw(f"{fid}:line", Rectangle((x0, z), x1 - x0, 0.0, fill=False), ax)
        return True
    return _only_load(_s1_marks(mark_fn=mf))


def mark_b3b():
    """B-m3b (M3 count): two :line artists on anchor_a."""
    def mf(pid, fid, ax, x0, x1, z):
        if fid != "anchor_a":
            return False
        for _ in range(2):
            sc.draw(f"{fid}:line", Line2D([x0, x1], [z, z]), ax)
        return True
    return _only_load(_s1_marks(mark_fn=mf))


def mark_b4():
    """B-m4 (M4): anchor_a mark right endpoint 5 mm outside the block (x1 + 5)."""
    def mf(pid, fid, ax, x0, x1, z):
        if fid != "anchor_a":
            return False
        sc.draw(f"{fid}:line", Line2D([x0, x1 + 5.0], [z, z]), ax)
        return True
    return _only_load(_s1_marks(mark_fn=mf))


def mark_b5a():
    """B-m5a (M5 place): anchor_a mark at z + 2 (282 against mark.z 280 z_A)."""
    def mf(pid, fid, ax, x0, x1, z):
        if fid != "anchor_a":
            return False
        sc.draw(f"{fid}:line", Line2D([x0, x1], [z + 2.0, z + 2.0]), ax)
        return True
    return _only_load(_s1_marks(mark_fn=mf))


def mark_b5b():
    """B-m5b (M5 direction): anchor_a mark tilted, z1 = z0 + 2."""
    def mf(pid, fid, ax, x0, x1, z):
        if fid != "anchor_a":
            return False
        sc.draw(f"{fid}:line", Line2D([x0, x1], [z, z + 2.0]), ax)
        return True
    return _only_load(_s1_marks(mark_fn=mf))


# ---------------------------------------------------------------- section_u premise, K4 expr label, smoke

def section_u_short():
    """B (section_u premise): the ring's outboard -Y piece drawn 5 mm short of its spec piece (u -205 for -210)."""
    def m(fig, ax, axi, *a):
        art = min(sc.tagged(ax)["ring"], key=lambda r: r.get_x())
        art.set_x(art.get_x() + 5.0)
        art.set_width(art.get_width() - 5.0)
    return s3_ctx(mutate=m)


def _k4_expr(number):
    """S3 fixture with one label (span_lt, label.expr guide_bearing_z - anchor_bearing_z): the annotation drawn with
    the given number, leader to the span line's midpoint; every other row's label removed from the spec."""
    def sm(spec):
        for r in spec["features"]:
            if r["id"] != "span_lt":
                r["label"] = None

    def m(fig, ax, axi, P, spec, stack, pid):
        ln = sc.tagged(ax)["span_lt"][0]
        x, z = ln.get_xdata()[0], sum(ln.get_ydata()) / 2
        txt = f"{spec_row(spec, 'span_lt')['label']['text']} {number}"
        ann = ax.annotate(txt, xy=(x, z), xytext=(x - 120, z + 40), fontsize=6, zorder=sc.LEADER_ZORDER,
                          arrowprops={"arrowstyle": "-", "lw": 0.5})
        ann.set_gid("label:span_lt")
        ax.texts[-1].set_gid("label:span_lt") if ax.texts and ax.texts[-1] is not ann else None
    return s3_ctx(spec_mut=sm, mutate=m)


def spec_row(spec, fid):
    return next(r for r in spec["features"] if r["id"] == fid)


def k4_expr_z():
    """K4 Z (1.3 P4 label value rule): the span_lt label prints its expr value, 870."""
    P = Params()
    return _k4_expr(format(P.get("jackscrew.guide_bearing_z") - P.get("jackscrew.anchor_bearing_z"), ".0f"))


def k4_expr_b():
    """K4 B: the span_lt label prints its key value (guide_bearing_z 1150) where the spec names expr (L_t 870)."""
    P = Params()
    return _k4_expr(format(P.get("jackscrew.guide_bearing_z"), ".0f"))


def s3_full_draw():
    """Smoke (SW-8 for S3): every S3 row of the live spec drawn faithfully; K1 to K9 and S3-1 to S3-3 run;
    none errors, none fails closed on an absent part."""
    import checks_s3
    return s3_fixed(), checks_s3.run


# ======================================================================== 1.3 P5f (c) fix pass
# research/sean/cr_scratch/step1.3_engineer_redfirst_fixes.md: Software Engineer FIX 1 to 5, Loftsman FIX 1 to 6,
# Topologist FIX 1 to 7. Each B run on the P4 code (docs/sketches/wip/p5f_pre/) first, or shown red by deleting its branch.

def _row(spec, fid):
    return next(r for r in spec["features"] if r["id"] == fid)


def orphan_b():
    """K8 B (SW FIX 1 = TP FIX 1): screw_a (inset only) carries {pred: below, of: anchor_a}, a z predicate no plan Axes
    evaluates: orphan, reported once."""
    return s3_ctx(spec_mut=lambda sp: _row(sp, "screw_a").setdefault("sense", []).append({"pred": "below", "of": "anchor_a"}))


def _reverse_look(fig, ax, axi, *a):
    for art in sc.tagged(axi)["section_line"]:
        if isinstance(art, FancyArrowPatch):
            (x0, y0), (x1, y1) = art._posA_posB
            art.set_positions((x0, y0), (2 * x0 - x1, y1))


def look_reversed():
    """K8 B (SW FIX 5 part = TP look sign): the look arrows drawn toward +X with the spec toward -X."""
    return s3_ctx(mutate=_reverse_look)


def look_spec_wrong():
    """K8 B (TP FIX 2): spec look_direction toward +X with the arrows drawn toward +X: drawing and spec agree, the
    section viewer (u = +Y, so the viewer at +X looking -X) does not."""
    def sm(sp):
        for pr in _row(sp, "section_line")["sense"]:
            if pr["pred"] == "look_direction":
                pr["toward"] = "+X"
    return s3_ctx(spec_mut=sm, mutate=_reverse_look)


def axes_undeclared_id():
    """K3 B (SW FIX 5, M14): a third Axes carrying the id inset_x, which the spec does not declare."""
    def m(fig, ax, axi, *a):
        ex = fig.add_axes([0.05, 0.05, 0.1, 0.1])
        ex.sketch_axes, ex.sketch_view = "inset_x", "plan_xy"
    return s3_ctx(mutate=m)


def _k4_one(fid, text_fn, axes=MAIN):
    """S3 fixture with one label drawn (row fid), every other row's label removed; text_fn(spec, P) gives the text; the
    leader runs to the first vertex of the row's first artist in the named Axes."""
    def sm(spec):
        for r in spec["features"]:
            if r["id"] != fid:
                r["label"] = None

    def m(fig, ax, axi, P, spec, stack, pid):
        tgt = ax if axes == MAIN else axi
        art = sc.tagged(tgt)[fid][0]
        x, z = sc.arrow_ends(art)[0] if isinstance(art, FancyArrowPatch) else sc.artist_polys(art)[0][0]
        ann = tgt.annotate(text_fn(spec, P), xy=(x, z), xytext=(x - 120, z + 40), fontsize=6, zorder=sc.LEADER_ZORDER,
                           arrowprops={"arrowstyle": "-", "lw": 0.5})
        ann.set_gid(f"label:{fid}")
    return s3_ctx(spec_mut=sm, mutate=m)


def k4_value_from_z():
    """K4 Z (SW FIX 5, M17): load_tension_c prints its value_from value (load_cases cut per_screw 247.5 at W 26.25 kg, 1.3 (h) r3)."""
    return _k4_one("load_tension_c", lambda sp, P: f"{_row(sp, 'load_tension_c')['label']['text']} 247.5")


def k4_value_from_b():
    """K4 B (SW FIX 5, M17): load_tension_c prints 300 against its value_from value 247.5."""
    return _k4_one("load_tension_c", lambda sp, P: f"{_row(sp, 'load_tension_c')['label']['text']} 300")


def k4_label_off_home():
    """K4 B (SW FIX 5, M16): the keepout label (home Axes section) drawn in the inset as well as the section."""
    def m(fig, ax, axi, P, spec, stack, pid):
        txt = sc.label_text(_row(spec, "keepout"), P, spec=spec)
        for tgt in (ax, axi):
            art = sc.tagged(tgt)["keepout"][0]
            x, y = sc.artist_polys(art)[0][0]
            tgt.annotate(txt, xy=(x, y), xytext=(x - 60, y + 30), fontsize=6, zorder=sc.LEADER_ZORDER,
                         arrowprops={"arrowstyle": "-", "lw": 0.5}).set_gid("label:keepout")

    def sm(spec):
        for r in spec["features"]:
            if r["id"] != "keepout":
                r["label"] = None
    return s3_ctx(spec_mut=sm, mutate=m)


def mark_gap_end():
    """K5 B (TP FIX 5): anchor_bearing_c:line from u -173 to -160, one end in the journal gap (inside the hull of the
    bearing pieces, on no vertical edge)."""
    def m(fig, ax, axi, *a):
        ln = sc.tagged(ax)["anchor_bearing_c:line"][0]
        xs = list(ln.get_xdata())
        ln.set_xdata([xs[0], -160.0])
    return s3_ctx(mutate=m)


# ---- section convention clauses (SW FIX 4; TP FIX 3)

def conv_class_missing():
    """K8 B (convention 5, M08): ring without section_class."""
    return s3_ctx(spec_mut=lambda sp: _row(sp, "ring").pop("section_class", None))


def _section_copy(fid, new_id, cls):
    def sm(sp):
        r = copy.deepcopy(_row(sp, fid))
        r.update(id=new_id, axes=[MAIN], section_class=cls, projection="rectangle", projection_by_axes=None, sense=[], label=None, neighbours=[])
        sp["features"].append(r)
    return sm


def conv_past_width():
    """K8 B (convention 4, M09): the screw a set (theta 150, x -138.6) drawn in the section (row screw_a_past)."""
    return s3_ctx(spec_mut=_section_copy("screw_a", "screw_a_past", "unsectioned"))


def conv_beyond_partly():
    """K8 B (convention 3, M10): one standoff moved to straddle the anchor block underside (z_S 315 to 335), solid."""
    def m(fig, ax, axi, *a):
        art = sc.tagged(ax)["standoffs_c"][0]
        art.set_y(315.0)
        art.set_height(20.0)
        art.set_linestyle("-")
    return s3_ctx(mutate=m)


def conv_beyond_hatched():
    """K8 B (convention 3, M11): a standoff hatched."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: sc.tagged(ax)["standoffs_c"][0].set_hatch("//"))


def conv_beyond_front():
    """K8 B (convention 3, M12): standoffs_c plan_poly x band moved to straddle x = 0 (-2.75 to 2.75)."""
    def sm(sp):
        r = _row(sp, "standoffs_c")
        for pc in r["plan_poly"]:
            for pt in pc:
                pt[0] = str(pt[0]).replace("-liftmotor.bolt_pattern / 2 - liftmotor.standoff_af / 2", "-liftmotor.standoff_af / 2").replace(
                    "-liftmotor.bolt_pattern / 2 + liftmotor.standoff_af / 2", "liftmotor.standoff_af / 2")
    return s3_ctx(spec_mut=sm)


def conv_cut_missed():
    """K8 B (convention 1, M13): ring depth set to x -50 to -40, a cut row the plane x = 0 does not cut."""
    return s3_ctx(spec_mut=lambda sp: _row(sp, "ring").__setitem__("depth", [-50, -40]))


def conv_unsectioned_off_plane():
    """K8 B (TP FIX 3 a): standoffs_c (depth x -18.25 to -12.75) re-classed unsectioned."""
    return s3_ctx(spec_mut=lambda sp: _row(sp, "standoffs_c").__setitem__("section_class", "unsectioned"))


def conv_omitted_in_band():
    """K8 B (TP FIX 3 b): coupling_c (plan x -9.5 to 9.5) declared in the inset only: in the section band, not drawn."""
    def sm(sp):
        r = _row(sp, "coupling_c")
        r["axes"] = [INSET]
        r["projection_by_axes"] = {INSET: "circle"}
    return s3_ctx(spec_mut=sm)


def points_same_sense():
    """K8 B (TP FIX 4): load_tension_c drawn as two arrows from one tail, both pointing up, heads 3 either side."""
    def m(fig, ax, axi, *a):
        arts = [x for x in sc.tagged(ax)["load_tension_c"] if isinstance(x, FancyArrowPatch)]
        (x0, y0), _ = arts[0]._posA_posB
        _, (x1, y1) = arts[1]._posA_posB
        arts[0].set_positions((x0, y0), (x0 - 3, y1))
        arts[1].set_positions((x0, y0), (x0 + 3, y1))
    return s3_ctx(mutate=m)


# ---- mirror_about_radial (TP FIX 6)

MIRROR_ROWS = ("anchor_a", "anchor_b", "anchor_c", "liftmotor_a", "liftmotor_b", "liftmotor_c", "frame_upper_a", "frame_upper_b",
               "frame_upper_c", "home_switch_a", "home_switch_b", "home_switch_c")


def mirror_z():
    """K8 Z (TP FIX 6): mirror_about_radial declared on the twelve radial inset rows (in the live spec from 1.3 P6),
    drawn faithfully."""
    return s3_ctx()


def mirror_b():
    """K8 B (TP FIX 6): frame_upper_b drawn rotated 15 deg and scaled 0.75 about its centre in the inset."""
    def m(fig, ax, axi, *a):
        art = sc.tagged(axi)["frame_upper_b"][0]
        P = sc.artist_polys(art)[0]
        cx, cy = sum(x for x, _ in P) / len(P), sum(y for _, y in P) / len(P)
        c, s_ = math.cos(math.radians(15)), math.sin(math.radians(15))
        art.set_xy([(cx + 0.75 * ((x - cx) * c - (y - cy) * s_), cy + 0.75 * ((x - cx) * s_ + (y - cy) * c)) for x, y in P])
    return s3_ctx(mutate=m)


# ---- class_by_axes (TP FIX 7, F5)

def cba_z():
    """K7 Z (TP FIX 7): the spec's class_by_axes N on screw_c|nut_housing_c and screw_c|anchor_c in the inset (F kept in
    the section): inset K7 clear of the 13 F overlaps; section K7 clean (1.3 P6: the receiver shoulder seats on the plate
    top, Design Notes 32)."""
    return s3_ctx()


def cba_b():
    """K7 B (TP FIX 7): screw_a|nut_housing_a with class_by_axes N in the inset, a pair no other Axes draws."""
    def sm(sp):
        _row(sp, "screw_a").setdefault("neighbours", []).append({"id": "nut_housing_a", "class": "F", "class_by_axes": {INSET: "N"}})
    return s3_ctx(spec_mut=sm)


# ---- S3-2 drawn span (SW FIX 2 = LF FIX 4)

def s3_2_b2():
    """S3-2 B: guide_bearing_c drawn 10 above its row, keys unchanged."""
    def m(fig, ax, axi, *a):
        for art in sc.tagged(ax)["guide_bearing_c"]:
            art.set_y(art.get_y() + 10.0)
    return s3_ctx(mutate=m)


# ---- S3-3 branches (SW FIX 3 = LF FIX 5; LF FIX 1 to 3; SW NOTE 7)

def s3_3_face_off():
    """S3-3 B (SW FIX 3 a, M02): the nut face named 1 above the counterbore shoulder (spec neighbour face z + 1)."""
    t = _new_tmp()
    sp = _live_specs()
    for nb in _row(sp["s3"], "nut_housing_c")["neighbours"]:
        if nb.get("id") == "nut_c" and isinstance(nb.get("face"), dict):
            nb["face"]["z"] = nb["face"]["z"] + " + 1"
    return s3_ctx(spec=sp["s3"], records=_records_dir(t), specs=sp)


def s3_3_sym_fail():
    """S3-3 B (SW FIX 3 b, M03): x1_exempt left on S3 anchor_b: SYM fails, no a, b link certifies by symmetry."""
    t = _new_tmp()
    sp = _live_specs()
    _row(sp["s3"], "anchor_b")["x1_exempt"] = {"reason": "planted"}
    return s3_ctx(spec=sp["s3"], records=_records_dir(t), specs=sp)


def s3_3_c_open():
    """S3-3 B (SW FIX 3 c, M04): nut_housing_c drawn 1 down: c link nut_c|nut_housing_c open; the a, b nut links whose
    counterpart range holds it open by symmetry."""
    def m(fig, ax, axi, *a):
        for art in sc.tagged(ax)["nut_housing_c"]:
            art.set_y(art.get_y() - 1.0)
    return _s3_3_ctx(mutate=m)


def _set_state(pair, pose, state, only_pose=None):
    def mut(rec):
        k7 = next(c for c in rec["checks"] if c["id"] == "K7")
        keep = []
        for i, t in enumerate(k7["tests"]):
            if t[1] in pair:
                if only_pose and t[0] != only_pose:
                    continue
                if pose and t[0] == pose:
                    t[3] = state
                    k7["states"][i] = state
            keep.append(i)
        k7["tests"] = [k7["tests"][i] for i in keep]
        k7["states"] = [k7["states"][i] for i in keep]
    return mut


def s3_3_record_not_c():
    """S3-3 B (SW FIX 3 d, M05): the S1 record with collet|holder at capture_end in state F."""
    return _s3_3_ctx(s1_mut=_set_state(BP_BF, "capture_end", "F"), s2_mut=_set_state(BP_BF, "capture_end", "F"))   # 1.3 (h) r2 re-plant


def s3_3_pose_only():
    """S3-3 B (SW NOTE 7, M07): the S1 record carrying collet|holder at pose load only (absent at the figure pose)."""
    return _s3_3_ctx(s1_mut=_set_state(BP_BF, None, None, only_pose="load"), s2_mut=_set_state(BP_BF, None, None, only_pose="load"))   # 1.3 (h) r2 re-plant


def s3_3_veto_pair():
    """S3-3 B (LF FIX 1; redefined at 1.3 P6 for Design Notes 32, Designer receiver shoulder section 2): the shoulder seat
    face 1 above the plate top (receiver.shoulder_z 13) with chains a and b certified by "S1 base_plate|receiver C" only,
    fresh records: the section reads receiver|base_plate open (F), so the pair is open in chains c, a and b."""
    t = _new_tmp()
    sp = _live_specs()
    for ch in ("a", "b"):
        for link in sp["s3"]["chains"][ch]:
            if link["pair"] == ["receiver", "base_plate"]:
                link["certifiers"] = ["S1 base_plate|receiver C"]
                link["kind"] = "face_record"   # 1.3 (h) r2: a record-only face (the kind lint holds a face link to S3)
    return s3_ctx(spec=sp["s3"], values={"receiver.shoulder_z": 13}, records=_records_dir(t), specs=sp)


def s3_3_true_cut():
    """S3-3 B (LF FIX 3): bracket_anchor_c, a row of an S3-certified pair, placed at jackscrew.angle[1] (150): off the
    plane, not its true cut (drawn faithfully)."""
    t = _new_tmp()
    sp = _live_specs()
    _row(sp["s3"], "bracket_anchor_c")["place"]["theta"] = "jackscrew.angle[1]"
    return s3_ctx(spec=sp["s3"], records=_records_dir(t), specs=sp)


def s3_3_face_corner():
    """S3-3 B (LF FIX 2): the anchor cover pieces (bottom at 348 z_S) drawn with the bore widened to the bearing OD, so
    the cover meets the bearing top at u -173 and -147 only."""
    def m(fig, ax, axi, *a):
        for art in sc.tagged(ax)["anchor_c"]:
            if abs(art.get_y() - 348.0) <= 1e-6:
                x0, x1 = art.get_x(), art.get_x() + art.get_width()
                if x1 <= -160:
                    art.set_width(-173.0 - x0)
                else:
                    art.set_x(-147.0)
                    art.set_width(x1 + 147.0)
    return _s3_3_ctx(mutate=m)


# ---- SYM-P (LF FIX 6)

def _keys_read(n, drop_accessed=False, drop_key=None):
    P = Params()
    spec = load_spec(SK / f"{n}_spec.yaml")
    if drop_key:
        for r in spec["features"]:
            if drop_key in (r.get("keys") or []):
                r["keys"] = [k for k in r["keys"] if k != drop_key]
    check_stack.evaluate_spec(P, spec)
    keys = set(sc.spec_keys(spec)) | (set() if drop_accessed else set(P.accessed))
    return spec, keys


def sym_p_z():
    """SYM-P Z: on S1, S2 and S3, keys_read (spec_keys plus every key check_stack read) covers every key the SYM rows'
    place and z_rule read."""
    cs = check_sketch_mod()
    rs = [cs.sym_keys_premise(*_keys_read(n)) for n in ("s1", "s2", "s3")]
    bad = [r for r in rs if r["result"] != "pass"]
    return {"id": "SYM-P", "result": "fail" if bad else "pass", "reason": " || ".join(r["reason"] for r in rs), "n_issues": sum(r["n_issues"] for r in rs)}


def sym_p_b():
    """SYM-P B: S3 keys_read built from spec_keys alone (P.accessed dropped) with jackscrew.top_guide_z removed from
    every row's keys list."""
    cs = check_sketch_mod()
    r = cs.sym_keys_premise(*_keys_read("s3", drop_accessed=True, drop_key="jackscrew.top_guide_z"))
    return r


# ======================================================================== 1.3 (h) r2 (P9, step1.3_engineer_revision_r2.md)
# Each B was run on the pre-change harness (D:\Unleashed Robotics\_scratch\cutjig\p9r2\pre) first and read clean there.

def k4_through_text():
    """K4 (i1) B (Designer M1 S3 r1 F2): live S2, a text planted centred three quarters along the drill_tube leader (the r1
    hold_callout leader through the span_lt text)."""
    b = _builders()
    c = b._script_ctx("s2")
    ax = b._s2_ax(c)
    t = next(x for x in ax.texts if x.get_gid() == "label:drill_tube")
    (x0, y0), (x1, y1) = t.xyann, t.xy
    ax.text(x0 + (x1 - x0) * 0.75, y0 + (y1 - y0) * 0.75, "PLANTED THROUGH", fontsize=sc.LABEL_FONTSIZE, ha="center", va="center")
    return c


def k4_text_overlap():
    """K4 (i2) B (Designer M1 S3 r1 F3): live S2, a figure-level text placed on the base_plate label text."""
    b = _builders()
    c = b._script_ctx("s2")
    ax = b._s2_ax(c)
    t = next(x for x in ax.texts if x.get_gid() == "label:base_plate")
    x, y = t.xyann
    ax.annotate("PLANTED OVERLAP", xy=(x, y), xytext=(x, y), fontsize=sc.LABEL_FONTSIZE, ha="left", va="center", annotation_clip=False)
    return c


def occl_undone():
    """K8 clause (6) B (Topologist TP1.3-11): the r1 renderer state, every split undone (clip paths removed, hidden copies
    deleted): the 8 occluded rows drawn solid inside the unsectioned outlines."""
    def m(fig, ax, axi, *a):
        for art in list(ax.get_children()):
            if getattr(art, "_sc_hidden_copy", False):
                art.remove()
            elif art.get_gid() and art.get_clip_path() is not None and hasattr(art, "get_hatch"):
                art.set_clip_path(ax.patch)
                art._clippath = None
    return s3_ctx(mutate=m)


def occl_no_copy():
    """K8 clause (6b) B: the hidden copies deleted, the splits kept: occluded areas with no dashed hidden edges."""
    def m(fig, ax, axi, *a):
        for art in list(ax.get_children()):
            if getattr(art, "_sc_hidden_copy", False):
                art.remove()
    return s3_ctx(mutate=m)


def root_z():
    """K5 Z (TP1.3-15): screw_c:root drawn as declared (fixture drawer)."""
    return s3_ctx()


def _root_mut(fn):
    def m(fig, ax, axi, *a):
        arts = sc.tagged(ax)["screw_c:root"]
        fn(sorted(arts, key=lambda x: x.get_xdata()[0]))
    return s3_ctx(mutate=m)


def root_at_nominal():
    """K5 B1 (TP1.3-15): the inboard root line at the nominal d / 2 (u -154) instead of d_r / 2."""
    def f(arts):
        x = arts[1].get_xdata()
        arts[1].set_xdata([x[0] + 1.75, x[1] + 1.75])
    return _root_mut(f)


def root_past_end():
    """K5 B2 (TP1.3-15): the outboard root line runs 5 past thread_end_z."""
    def f(arts):
        y = list(arts[0].get_ydata())
        arts[0].set_ydata([y[0], max(y) + 5] if y[1] > y[0] else [max(y) + 5, y[1]])
    return _root_mut(f)


def root_solid():
    """K5 B3 (TP1.3-15): both root lines drawn solid."""
    return _root_mut(lambda arts: [a.set_linestyle("-") for a in arts])


def _arc_mut(**kw):
    def m(fig, ax, axi, P, spec, *a):
        for art in list(sc.tagged(axi).get("plan_axes:arc", [])):
            art.remove()
        _draw_arc(axi, P, _row(spec, "plan_axes"), **kw)
    return s3_ctx(mutate=m)


def arc_z():
    """K5 Z (TP1.3-13): plan_axes:arc 0 to 90 deg at r profile.width * 2 / 3 (40), counter-clockwise."""
    return s3_ctx()


def arc_reversed():
    """K5 B1 (TP1.3-13): the arc points reversed (clockwise from 90 to 0)."""
    return _arc_mut(reverse=True)


def arc_radius():
    """K5 B2 (TP1.3-13): the arc at radius + 5."""
    return _arc_mut(dr=5.0)


def arc_in_section():
    """K5 B3 (TP1.3-13): the arc drawn in the section Axes."""
    def m(fig, ax, axi, P, spec, *a):
        _draw_arc(ax, P, _row(spec, "plan_axes"))
    return s3_ctx(mutate=m)


def hatch_alt_z():
    """K8 Z (TP1.3-14): anchor_c with the fixture alternate on the cover pieces (above 288 z_A), the material hatch on the
    block pieces."""
    return s3_ctx()


def _anchor_pieces(ax, above):
    out = []
    for art in sc.tagged(ax)["anchor_c"]:
        if getattr(art, "_sc_hidden_copy", False):
            continue
        y0 = min(v[1] for v in sc.artist_polys(art)[0])
        if (y0 >= 348.0 - 1e-6) == above:
            out.append(art)
    return out


def hatch_cover_plain():
    """K8 B1 (TP1.3-14): one cover piece with the plain aluminium hatch."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: _anchor_pieces(ax, True)[0].set_hatch(sc.HATCH["aluminium"]))


def hatch_block_alt():
    """K8 B2 (TP1.3-14): one block piece with the alternate."""
    return s3_ctx(mutate=lambda fig, ax, axi, *a: _anchor_pieces(ax, False)[0].set_hatch(FIXTURE_ALT))


def hatch_alt_equal():
    """K8 B3 (TP1.3-14 lint): section.hatch_alt aluminium equal to the steel pattern."""
    def sm(sp):
        sp["section"]["hatch_alt"] = {"aluminium": sc.HATCH["steel"]}
    return s3_ctx(spec_mut=sm)


def hatch_alt_missing():
    """K8 B4 (TP1.3-14 lint): hatch_split with no alternate (the r2 live state)."""
    def sm(sp):
        sp["section"]["hatch_alt"] = {}
    return s3_ctx(spec_mut=sm)


def nd_band_live():
    """K8 B (TP1.3-12): 1.3 (h) r3 re-plant: the rear nut shoulder screw entry made off_plane with its band (x -18.86 to
    -8.86), the r2 live state: it lies in the section band."""
    def sm(sp):
        for e in sp["not_drawn"]:
            if e.get("part") == "rear nut shoulder screw":
                e["omit"] = "off_plane"
                e.pop("owner", None)
                e["x"] = [["-ring.nut_screw_pcd / 2 * sind(60) - ring.nut_screw_head_d / 2", "-ring.nut_screw_pcd / 2 * sind(60) + ring.nut_screw_head_d / 2"]]
    return s3_ctx(spec_mut=sm)


def nd_no_omit():
    """K8 B (TP1.3-12 lint): a not_drawn entry without omit."""
    def sm(sp):
        sp["not_drawn"][0].pop("omit", None)
    return s3_ctx(spec_mut=sm)


def nd_pinion_footprint():
    """K8 B (TP1.3-12, NOTE case): pinions a and b read on their footprint (x1 -59.66) instead of the true trapezoid:
    enters the band by 0.34."""
    def sm(sp):
        for e in sp["not_drawn"]:
            if e.get("part") == "pinions a and b":
                e.pop("x", None)
                e["rows_s2"] = ["pinion_a", "pinion_b"]
    return s3_ctx(spec_mut=sm)


def _s33_spec_mut(fn):
    t = _new_tmp()
    sp = _live_specs()
    fn(sp["s3"])
    return s3_ctx(spec=sp["s3"], records=_records_dir(t), specs=sp)


def s3_3_face_sense_z():
    """S3-3 Z (TP1.3-10): the live chains with kinds, fresh records: 48 links closed, face links with their sense."""
    return _s3_3_ctx()


def s3_3_face_below():
    """S3-3 B12 (TP1.3-10): anchor_c|anchor_bearing_c face named at the block shoulder 272 z_A (332.00 z_S), where the
    cover's block piece lies below the face: the contact test passes it, the sense opens it."""
    def fn(s3):
        for nb in _row(s3, "anchor_c")["neighbours"]:
            if nb.get("id") == "anchor_bearing_c":
                nb["face"]["z"] = "jackscrew.anchor_bearing_z - jackscrew.anchor_bearing_width"
    return _s33_spec_mut(fn)


def s3_3_member_face():
    """S3-3 B13 (TP1.3-10): base_frame|frame_upper_c as a face link at the rail top (x below: the member foot face opens
    under the cut-case loop force)."""
    def fn(s3):
        for link in s3["chains"]["c"]:
            if link["pair"] == ["base_frame", "frame_upper_c"]:
                link["kind"], link["face"] = "face", {"z": "0", "side": "planted"}
    return _s33_spec_mut(fn)


def s3_3_side_face():
    """S3-3 B14 (TP1.3-10): frame_upper_c|bracket_anchor_c as a face link (a vertical side face: no horizontal edge)."""
    def fn(s3):
        for link in s3["chains"]["c"]:
            if link["pair"] == ["frame_upper_c", "bracket_anchor_c"]:
                link["kind"], link["face"] = "face", {"z": "jackscrew.anchor_z", "side": "planted"}
    return _s33_spec_mut(fn)


def s3_3_no_kind():
    """S3-3 B15 (TP1.3-10 lint): chain c link nut_housing_c|ring without a kind."""
    def fn(s3):
        for link in s3["chains"]["c"]:
            if link["pair"] == ["nut_housing_c", "ring"]:
                link.pop("kind")
    return _s33_spec_mut(fn)


# ======================================================================== 1.3 (h) r3 (P9 r3, step1.3_engineer_revision_r3.md)
# Designer r2 item 3 (span_lt:ext, e1 to e4), Topologist R2-1 to R2-4. Each B run on the r2 code (p9r3\pre) first.

def arc_head_cw():
    """K5 B43 (Topologist R2-3): the head drawn from 100 to 90 deg on the ccw line (clockwise head)."""
    return _arc_mut(head_from=100.0)


def _ext_mut(fn):
    def m(fig, ax, axi, *a):
        arts = sorted(sc.tagged(ax)["span_lt:ext"], key=lambda x: x.get_ydata()[0])
        fn(arts)
    return s3_ctx(mutate=m)


def ext_off_end():
    """K5 B44 (Designer e1): the lower extension line 5 above the z_rule end."""
    return _ext_mut(lambda arts: arts[0].set_ydata([y + 5 for y in arts[0].get_ydata()]))


def ext_off_edge():
    """K5 B45 (Designer e2): the upper extension line starting 5 inboard of the screw edge."""
    def f(arts):
        x = list(arts[1].get_xdata())
        x[0] = x[0] + 5
        arts[1].set_xdata(x)
    return _ext_mut(f)


def ext_run_on():
    """K5 B46 (Designer e3): the lower extension line run on 10 past the dimension line."""
    def f(arts):
        x = list(arts[0].get_xdata())
        x[1] = x[1] + 8
        arts[0].set_xdata(x)
    return _ext_mut(f)


def ext_non_reference():
    """K5 B47 (Designer e4): screw_c declares ext and draws two extension lines (screw_c is no reference line row)."""
    def sm(sp):
        r = _row(sp, "screw_c")
        r["sub_artists"] = list(r.get("sub_artists") or []) + ["ext"]
        r["ext"] = {"screw": "screw_c"}
    def m(fig, ax, axi, *a):
        sc.draw("screw_c:ext", Line2D([-154.0, -150.0], [400.0, 400.0]), ax)
    return s3_ctx(spec_mut=sm, mutate=m)


def s3_3_face_no_z():
    """S3-3 B16 (Topologist R2-1): frame_upper_c|bracket_anchor_c as kind face with no face z."""
    def fn(s3):
        for link in s3["chains"]["c"]:
            if link["pair"] == ["frame_upper_c", "bracket_anchor_c"]:
                link["kind"] = "face"
                link.pop("face", None)
    return _s33_spec_mut(fn)


def s3_3_face_no_s3():
    """S3-3 B17 (Topologist R2-1): base_plate|base_frame as kind face with record certifiers only."""
    def fn(s3):
        for link in s3["chains"]["c"]:
            if link["pair"] == ["base_plate", "base_frame"]:
                link["kind"] = "face"
    return _s33_spec_mut(fn)


def nd_no_owner():
    """K8 B86 (Topologist R2-2): the rear nut shoulder screw entry deferred with its owner removed."""
    def sm(sp):
        for e in sp["not_drawn"]:
            if e.get("part") == "rear nut shoulder screw":
                e.pop("owner", None)
    return s3_ctx(spec_mut=sm)


def hatch_alt_family():
    """K8 B87 (Topologist R2-4): section.hatch_alt aluminium '////', the aluminium line family at double density."""
    def sm(sp):
        sp["section"]["hatch_alt"] = {"aluminium": "////"}
    return s3_ctx(spec_mut=sm)
