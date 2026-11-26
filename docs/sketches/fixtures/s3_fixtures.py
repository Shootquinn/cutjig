"""Controls for 1.3 (c) (P4): TP-7 per-Axes views, the section view (section_yz), the renderer section convention, the
S3-x fixtures from the signed spec (S3-1 to S3-3), the K5 mark admission (Topologist P0T section 4) and declared
sub-artists, SYM (screw-set symmetry lint), the narrowed x1_exempt and the --accept refusal on a remaining exemption.

The S3 fixture draws every row of the signed s3_spec.yaml faithfully from check_stack values: the section Axes in the
section frame (u = plan y, the place / plan_poly y extent; section_u pieces as drawn; axis-Z section rows mirrored about
u = 0), the plan inset with the S2 fixture's plan drawer, the bearing line (mark), the balls and the switch lever, and the
renderer section convention (sketch_common.render_section) and plan renderer (render_plan) applied. Each B plants one
defect on top of that drawing, or edits the spec / params and draws faithfully (a spec or params decision drawn).
Figures are built with the pre-P4 API where the new one is missing (inset fallback below), so the B controls can be run
on the pre-change code for the red-first evidence.
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
    try:
        return sc.setup_figure(spec["view"], title=title, insets=spec.get("insets"))
    except TypeError:   # pre-P4 code: one Axes from setup_figure; the inset is added here as P4's add_inset does
        fig, ax = sc.setup_figure(spec["view"], title=title)
        ax.sketch_axes = MAIN
        for d in spec.get("insets") or []:
            ai = fig.add_axes([0.60, 0.50, 0.36, 0.42])
            ai.set_title(f"{d['view']}: {d.get('title', d['id'])}", fontsize=8)
            ai.set_xlabel("x (mm)", fontsize=7)
            ai.set_ylabel("y (mm)", fontsize=7)
            ai.set_aspect("equal")
            ai.minorticks_on()
            ai.grid(True, which="major", linewidth=0.6)
            ai.grid(True, which="minor", linewidth=0.3, alpha=0.5)
            ai.set_xlim(*d["extent"]["x"])
            ai.set_ylim(*d["extent"]["y"])
            ai.sketch_view, ai.sketch_axes = d["view"], d["id"]
        return fig, ax


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
        if fid == "section_line":
            L = P.get("icd.footprint_y") / 2
            for y in (-L, L):
                _arrow(ax, fid, (0.0, y), (-40.0, y))


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
        ax.text(0, -0.06, spec["figure_note"], transform=ax.transAxes, fontsize=5).set_gid(sc.NOTE_GID)
    sc.finish_axes(ax)
    if mutate:
        mutate(fig, ax, axi, P, spec, stack, pid)
    return figs


def s3_ctx(spec_mut=None, values=None, mutate=None, render=True, subs=True, skip=(), records=None, specs=None, spec=None, findings=True):
    """Live S3 spec drawn faithfully (one figure at section_figure.pose). spec_mut(spec), values {key: value} as the S1/S2
    fixtures (a spec or params decision drawn faithfully); mutate(fig, ax, axi, P, spec, stack, pid) plants a drawing
    defect after the faithful draw. records: directory S3-3 reads; specs: the {name: spec} SYM reads."""
    P = Params()
    for k, v in (values or {}).items():
        P.leaves[k] = dict(P.leaves[k], value=v)
    spec = copy.deepcopy(spec) if spec is not None else load_spec(S3_SPEC)
    if findings:   # every fixture but s3_live draws the signed spec with the P4 spec findings applied (p4_spec_findings)
        p4_spec_findings(spec)
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


def p4_spec_findings(spec):
    """The three signed-spec findings of P4 applied (step1.3_engineer_redfirst.md section 1, findings F2, F3; for P6):
    nut_c and guide_c are drawn in the section only, where their projection is a rectangle (the spec says circle);
    motor_shaft_c outboard of pinion_c in the side form (frame radial is a plan form, TP1.2-1)."""
    rows = {r["id"]: r for r in spec["features"]}
    for fid in ("nut_c", "guide_c"):
        rows[fid]["projection"] = "rectangle"
    for pr in rows["motor_shaft_c"].get("sense") or []:
        if pr.get("pred") == "outboard":
            pr.pop("frame", None)


def s3_fixed():
    """Z for K5 and K8 per Axes: the signed spec with the P4 spec findings applied, drawn faithfully."""
    if "f" not in _LIVE:
        _LIVE["f"] = s3_ctx()
    return _LIVE["f"]


_LIVE = {}


def s3_live():
    """Z: the signed S3 spec drawn faithfully (section Axes, inset, renderer section convention)."""
    if "c" not in _LIVE:
        _LIVE["c"] = s3_ctx(findings=False)
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


# ---- S3-3: records and specs as they stand after P6 (S1 r8, S2 r9 accepted with the 42-square anchors)

def _post_p6_specs():
    """The three specs with the S3 anchor place on S1/S2 anchor rows, x1_exempt removed and the a, b key lists equal to
    the c rows' (S1: a, b equal each other): the state SYM certifies after P6."""
    sp = {n: load_spec(SK / f"{n}_spec.yaml") for n in ("s1", "s2", "s3")}
    s3rows = {r["id"]: r for r in sp["s3"]["features"]}
    for n, spec in sp.items():
        rows = {r["id"]: r for r in spec["features"]}
        for fam in ("anchor", "anchor_locknut", "screw", "nut", "nut_housing"):   # check_sketch.SYM_FAMILIES
            have = {l: rows[f"{fam}_{l}"] for l in "abc" if f"{fam}_{l}" in rows}
            for l, r in have.items():
                r.pop("x1_exempt", None)
                if fam == "anchor" and f"anchor_{l}" in s3rows:
                    r["place"] = copy.deepcopy(s3rows[f"anchor_{l}"]["place"])
            if have:
                ref = have.get("c") or have[sorted(have)[0]]
                keys = sorted(set(k for r in have.values() for k in r.get("keys") or []))
                for r in have.values():
                    r["keys"] = list(keys)
                del ref
    return sp


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


def _receiver_cert(spec):
    """Finding F1 (P4): the signed section draws the receiver spigot 0.2 clear of the plate hole (spigot_od 160 in
    spigot_hole_dia 160.4) and no seat face, so the S3 certifier of receiver|base_plate reads F and vetoes the link; the
    S3-3 fixtures drop that certifier (S1 base_plate|receiver C certifies the link), pending the P6 spec decision."""
    for link in spec["chains"]["c"]:
        if link["pair"] == ["receiver", "base_plate"]:
            link["certifiers"] = [c for c in link["certifiers"] if not str(c).startswith("S3 ")]


def _s3_3_ctx(s1_mut=None, s2_mut=None, mutate=None):
    t = tempfile.mkdtemp(prefix="s3_3_")
    _TMP.append(t)
    sp = _post_p6_specs()
    _receiver_cert(sp["s3"])
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


def s3_3_b2():
    """S3-3 B: a chain pair absent from every record: the S1 record without its receiver|holder entries (the link
    holder|receiver in chains c, a, b has no other certifier)."""
    def m(rec):
        k7 = next(c for c in rec["checks"] if c["id"] == "K7")
        keep = [i for i, t in enumerate(k7["tests"]) if t[1] not in ("receiver|holder", "holder|receiver")]
        k7["tests"] = [k7["tests"][i] for i in keep]
        k7["states"] = [k7["states"][i] for i in keep]
    return _s3_3_ctx(s1_mut=m)


def s3_3_b3():
    """S3-3 B: a stale record: the S1 record with jackscrew.lead recorded 8 (the T8x8 value) against the live 3."""
    def m(rec):
        rec["keys_read"]["jackscrew.lead"]["value"] = 8
    return _s3_3_ctx(s1_mut=m)


# ---------------------------------------------------------------- SYM

def sym_z():
    """SYM Z: the three specs in the post-P6 state (no exemption, anchor place and key lists equal across a, b, c)."""
    return check_sketch_mod().sym_lint(_post_p6_specs())


def sym_b1():
    """SYM B: x1_exempt on S3 anchor_b."""
    sp = _post_p6_specs()
    next(r for r in sp["s3"]["features"] if r["id"] == "anchor_b")["x1_exempt"] = {"reason": "planted"}
    return check_sketch_mod().sym_lint(sp)


def sym_b2():
    """SYM B: S2 screw_a placed at jackscrew.angle[0] (the b index)."""
    sp = _post_p6_specs()
    next(r for r in sp["s2"]["features"] if r["id"] == "screw_a")["place"]["theta"] = "jackscrew.angle[0]"
    return check_sketch_mod().sym_lint(sp)


def sym_b3():
    """SYM B: S2 nut_housing_b z_max 1 higher than nut_housing_c."""
    sp = _post_p6_specs()
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
    """H1 B: --accept with a spec in docs/ carrying x1_exempt (the live s3_spec.yaml copied): refused, nothing written."""
    import step0_fixtures as s0
    cs = check_sketch_mod()
    rec = s0._template()
    with tempfile.TemporaryDirectory() as t:
        docs, wip = s0._dirs(t)
        (Path(docs) / "s3_spec.yaml").write_text(S3_SPEC.read_text(encoding="utf-8"), encoding="utf-8")
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
    """Smoke (SW-8 for S3): every S3 row drawn faithfully (P4 spec findings applied); K1 to K9 and S3-1 to S3-3 run;
    none errors, none fails closed on an absent part."""
    import checks_s3
    return s3_fixed(), checks_s3.run
