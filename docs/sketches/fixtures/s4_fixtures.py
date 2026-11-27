"""Controls for 1.4 (c) (P4): the S4-x fixtures from the signed s4_spec.yaml (S4-1 to S4-3), the section_true premise
and K5 admission (O7), the new K8 predicate forms (piece / of_piece, between, seat_piece, vertical_edge, inner-edge
taper; O6), the section-view tick admission (collet:slits, Topologist P2r form (a)), the beyond wing admission by
declared x_band (Designer P3a O3), the sweep sub-artist, min_bearing on the drawn S4 figure (Designer P3a FIX 3), the
hatch-adjacency lint through the K8 call site (Designer P2r R1) and by line family (R2, orchestrator ruling), and X1 on
section_true (Loftsman P3b O2 (i)).

The S4 fixture draws every row of the signed spec faithfully from check_stack values in both section figures (pose
carrier: figure 1; pose liner: figure 2; spec section_figures), with the shared-row X1 edits of `x1_edits_at_p6`
applied in memory (the P6 state S4 r1 is drawn in: holder z_max at the tube top 153.84, collar z_min 153.84, the S1
stack tie offset collar.thickness), each edit asserting its Old text. Rows with section_true are drawn piece by piece
(sketch_common.draw_piece, mirrored about u = 0, plane_cuts applied); base_plate from section_u; carrier, core_100 and
drill_head as unsectioned outlines over their depth bands; marks (<row>:line) at mark.z across the drawn width; the
sub-artists collet:slits (form (a)), receiver:root, wingnut:wing and wingnut:sweep; the renderer section convention
(sketch_common.render_section) applied. Each B plants one defect on that drawing, or edits the spec / params and draws
faithfully.
"""
import copy
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
for p in (str(SK), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402
from sketch_loader import Params, load_spec  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

S4_SPEC = SK / "s4_spec.yaml"
CHECK_STACK_PATH = SK / "check_stack.py"
MAIN = "section"
HIDDEN = "--"


def _builders():
    import builders
    return builders


# ---------------------------------------------------------------- local forms (the fixture draws on the pre-P4 code too)

PIECE_ATTR = getattr(sc, "PIECE_ATTR", "_sc_piece")


def _st_polys(P, names, row, z_S=True):
    """As sketch_common.section_true_polys (local, so the red-first run on the pre-change code draws the same figure)."""
    if hasattr(sc, "section_true_polys"):
        return sc.section_true_polys(P, names, row, z_S)
    ev = lambda e: float(check_stack.eval_expr(str(e), P, names))  # noqa: E731
    zc = (lambda z: check_stack.to_shop_floor(z, P)) if z_S else (lambda z: z)
    cuts = {(c.get("piece"), c.get("side")) for c in row.get("plane_cuts") or []}
    out = []
    for name, spec in (row.get("section_true") or {}).items():
        if isinstance(spec, dict):
            rz = [(ev(r), zc(ev(z))) for r, z in spec["poly"]]
        else:
            r0, r1, z0, z1 = (ev(v) for v in spec)
            rz = [(r0, zc(z0)), (r1, zc(z0)), (r1, zc(z1)), (r0, zc(z1))]
        for side, tag in ((1, "+u"), (-1, "-u")):
            if (name, tag) not in cuts:
                pts = [(side * r, z) for r, z in rz]
                out.append((name, side, pts if side > 0 else pts[::-1]))
    return out


def _draw_piece(ax, fid, name, pts):
    a = sc.draw(fid, Polygon(pts, closed=True, fill=False), ax)
    setattr(a, PIECE_ATTR, name)
    return a


def _slit_spec(rows, row):
    sl = row.get("slits") or {}
    return (rows.get(sl["same_as"]) or {}).get("slits") or {} if sl.get("same_as") else sl


# ---------------------------------------------------------------- the P6 spec state (x1_edits_at_p6 in memory)

def _get(d, path):
    for k in path[:-1]:
        d = d[k]
    return d, path[-1]


def p6_state(spec):
    """Apply x1_edits_at_p6 to the s4 spec in memory (items naming s4), each asserting its Old value."""
    rows = {r["id"]: r for r in spec["features"]}
    for e in spec.get("x1_edits_at_p6") or []:
        if "s4" not in e.get("specs", []):
            continue
        f = e["field"]
        if f.startswith("stack_ties."):
            _, tid, fld = f.split(".")
            t = next(t for t in spec["stack_ties"] if t["id"] == tid)
            assert " ".join(str(t[fld]).split()) == " ".join(e["old"].split()), (f, t[fld])
            t[fld] = e["new"]
        else:
            d, k = _get(rows[e["row"]], f.split("."))
            assert " ".join(str(d[k]).split()) == " ".join(e["old"].split()), (e["row"], f, d[k])
            d[k] = e["new"]
    return spec


# ---------------------------------------------------------------- drawing

def figure_poses(spec):
    return [f["pose"] for f in (spec.get("section_figures") or [spec.get("section_figure")])]


def _names(stack, pid):
    return stack["poses"][pid]["vars_z_A"]


def _zs(P, stack, pid, e):
    return check_stack.to_shop_floor(check_stack.eval_expr(str(e), P, _names(stack, pid)), P)


def _ev(P, stack, pid, e):
    return float(check_stack.eval_expr(str(e), P, _names(stack, pid)))


def _draw_row(ax, P, spec, stack, pid, row):
    fid = row["id"]
    f = stack["poses"][pid]["features"].get(fid)
    if f is None:
        return
    z0, z1 = f.get("z_min"), f.get("z_max")
    if row.get("kind") == "line":
        u0, u1 = f.get("depth") or (-130.0, 130.0)
        sc.draw_hline(ax, fid, u0, u1, z0, linestyle="-." if row.get("reference") else "-")
        return
    if row.get("section_true"):
        for name, side, pts in _st_polys(P, _names(stack, pid), row):
            _draw_piece(ax, fid, name, pts)
        return
    if row.get("section_u"):
        for pc in row["section_u"]:
            u0, u1 = sorted((_ev(P, stack, pid, pc[0]), _ev(P, stack, pid, pc[1])))
            sc.draw_rect(ax, fid, u0, u1, _zs(P, stack, pid, pc[2]), _zs(P, stack, pid, pc[3]))
        return
    if row.get("place"):
        u0, u1 = sorted(f["place"]["y"])
    else:
        u0, u1 = f["depth"]
    sc.draw_rect(ax, fid, u0, u1, z0, z1, linewidth=2 if row.get("section_class") == "unsectioned" else 1)


def _slit_u(P, stack, pid, row, ln, rows):
    """Form (a) (Designer/Topologist P2r): +u at the top-face mid-radius of the top piece; -u at r_mid sin(theta), r_mid
    the wall mid-radius at the line's mid-height (foot or cone piece inner and outer radius there)."""
    pcs = _st_polys(P, _names(stack, pid), row, z_S=False)
    top = [pts for nm, s, pts in pcs if nm == "top" and s > 0][0]
    if ln["side"] == "+u":
        zt = max(v[1] for v in top)
        rs = [v[0] for v in top if abs(v[1] - zt) <= 1e-9]
        return (min(rs) + max(rs)) / 2
    z0, z1 = sorted((_ev(P, stack, pid, ln["from"]), _ev(P, stack, pid, ln["to"])))
    zm = (z0 + z1) / 2
    cone = [pts for nm, s, pts in pcs if nm == "cone" and s > 0][0]
    r_in = min(v[0] for v in cone)
    # outer cone radius at zm: the edge between the two outer vertices
    outer = sorted([v for v in cone if v[0] > r_in + 1e-9], key=lambda v: v[1])
    (ra, za), (rb, zb) = outer[0], outer[-1]
    r_out = ra + (rb - ra) * (zm - za) / (zb - za)
    th = math.radians(_ev(P, stack, pid, ln["theta"]))
    return (r_in + r_out) / 2 * math.sin(th)


def _chord(poly, z):
    xs, n = [], len(poly)
    for i in range(n):
        (x0, z0), (x1, z1) = poly[i], poly[(i + 1) % n]
        if abs(z1 - z0) <= 1e-12:
            if abs(z - z0) <= 1e-9:
                xs += [x0, x1]
        elif min(z0, z1) - 1e-9 <= z <= max(z0, z1) + 1e-9:
            xs.append(x0 + (x1 - x0) * (z - z0) / (z1 - z0))
    return (min(xs), max(xs)) if xs else None


def _wall(P, stack, pid, row, z, u):
    """The merged chord of the row's section_true pieces on the side of u at height z (z_S) that holds u."""
    iv = sorted(c for c in (_chord(pts, z) for nm, s, pts in _st_polys(P, _names(stack, pid), row) if (s > 0) == (u > 0)) if c)
    out = []
    for a, b in iv:
        if out and a <= out[-1][1] + 0.05:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return next((a, b) for a, b in out if a - 0.05 <= u <= b + 0.05)


def _draw_subs(ax, P, spec, stack, pid, rows_here):
    rows = {r["id"]: r for r in spec["features"]}
    for row in rows_here:
        fid = row["id"]
        subs = row.get("sub_artists") or []
        m = row.get("mark")
        if m and "line" in subs:
            ps = sc.pieces(ax, fid)
            xs = [v[0] for P_ in ps for v in P_]
            z = _zs(P, stack, pid, m["z"])
            sc.draw(f"{fid}:line", Line2D([min(xs), max(xs)], [z, z], color="k", lw=1.0), ax)
        if "slits" in subs:
            sl = _slit_spec(rows, row)
            for ln in sl["lines"]:
                u = _slit_u(P, stack, pid, row, ln, rows)
                za, zb = _zs(P, stack, pid, ln["from"]), _zs(P, stack, pid, ln["to"])
                lo, hi = sorted((za, zb))
                sc.draw(f"{fid}:slits", Line2D([u, u], [lo, hi], linestyle=HIDDEN, lw=0.8), ax)
                zc = lo if ln["open"] == "top" else hi
                if sl.get("tick") == "wall":   # P5f (Topologist F1 a, d): dashed tick across the wall at the closed end
                    t0, t1 = _wall(P, stack, pid, row, zc, u)
                else:   # the P4 form (tick_length centred on the line), kept for the pre-change spec
                    tl = _ev(P, stack, pid, sl["tick_length"])
                    t0, t1 = u - tl / 2, u + tl / 2
                sc.draw(f"{fid}:slits", Line2D([t0, t1], [zc, zc], linestyle=HIDDEN if sl.get("tick") == "wall" else "-", lw=0.8), ax)
        if "root" in subs:
            rt = row["root"]
            r = _ev(P, stack, pid, rt["r"]) if "r" in rt else _ev(P, stack, pid, rt["d"]) / 2
            lo, hi = _zs(P, stack, pid, rt["from"]), _zs(P, stack, pid, rt["to"])
            for s in (-1, 1):
                sc.draw(f"{fid}:root", Line2D([s * r, s * r], [lo, hi], linestyle=HIDDEN, lw=0.8), ax)
        if "wing" in subs:
            w = row["wing"]
            u0, u1 = sorted(_ev(P, stack, pid, e) for e in w["u"])
            z0, z1 = sorted(_zs(P, stack, pid, e) for e in w["z"])
            sc.draw(f"{fid}:wing", Rectangle((u0, z0), u1 - u0, z1 - z0, fill=False, linestyle=HIDDEN), ax)
        if "sweep" in subs:
            r = _ev(P, stack, pid, row["sweep"]["r"])
            ez = sc.extent_z(sc.pieces(ax, fid))
            for s in (-1, 1):
                sc.draw(f"{fid}:sweep", Line2D([s * r, s * r], list(ez), linestyle=HIDDEN, lw=0.8), ax)


def _ctx_of(P, spec, stack, figs):
    return sc.Ctx(P=P, spec=spec, figs=figs, stack=stack, view=spec["view"], script_paths=[], check_stack_path=CHECK_STACK_PATH)


def _axes(fig):
    return next(a for a in sc.real_figure(fig).axes if getattr(a, "sketch_axes", None) == MAIN)


def s4_draw(P, spec, stack, render=True, skip=()):
    figs = {}
    for pid in figure_poses(spec):
        fig, ax = sc.setup_figure(spec["view"], title=f"S4 fixture, section B-B at pose {pid}")
        here = [r for r in spec["features"] if sc.applies(r, pid) and MAIN in (r.get("axes") or [MAIN]) and r["id"] not in skip]
        for row in here:
            _draw_row(ax, P, spec, stack, pid, row)
        _draw_subs(ax, P, spec, stack, pid, here)
        if spec.get("figure_note"):
            ax.text(0, 0, spec["figure_note"].replace("; ", ";\n"), transform=ax.transAxes, fontsize=4, va="bottom").set_gid(sc.NOTE_GID)
        sc.finish_axes(ax)
        figs[pid] = fig
    if render:
        rc = _ctx_of(P, spec, stack, figs)
        for pid, fig in figs.items():
            sc.render_section(rc, _axes(fig), pid)
    return figs


def s4_ctx(spec_mut=None, values=None, mutate=None, render=True, skip=()):
    """Signed S4 spec in its P6 state drawn faithfully (both figures). spec_mut(spec) and values {key: value}: a spec or
    params decision drawn faithfully; mutate(figs, P, spec, stack) plants a drawing defect after the faithful draw."""
    plain = spec_mut is None and not values and render and not skip

    def make():
        P = Params()
        for k, v in (values or {}).items():
            P.leaves[k] = dict(P.leaves[k], value=v)
        sp = p6_state(load_spec(S4_SPEC))
        if spec_mut:
            spec_mut(sp)
        stack = check_stack.evaluate_spec(P, sp)
        return P, sp, stack, s4_draw(P, sp, stack, render=render, skip=skip)
    if plain:
        P, spec, stack, figs = _builders().draw_cache("s4 fixture", [S4_SPEC], make, mods=(globals(),))
    else:
        P, spec, stack, figs = make()
    if mutate:
        mutate(figs, P, spec, stack)
    return _ctx_of(P, spec, stack, figs)


def s4_live():
    """Z: the signed S4 spec (P6 state) drawn faithfully in both figures, renderer section convention applied."""
    return s4_ctx()


# ---------------------------------------------------------------- plant helpers

def _arts(figs, pid, gid):
    return list(sc.tagged(_axes(figs[pid])).get(gid, []))


def _xform(a, fn):
    """Apply fn((u, z)) -> (u, z) to a Polygon, Rectangle or Line2D in place."""
    if isinstance(a, Line2D):
        pts = [fn(p) for p in zip(a.get_xdata(), a.get_ydata())]
        a.set_data([p[0] for p in pts], [p[1] for p in pts])
    elif isinstance(a, Rectangle):
        x, y, w, h = a.get_x(), a.get_y(), a.get_width(), a.get_height()
        (x0, y0), (x1, y1) = fn((x, y)), fn((x + w, y + h))
        a.set_xy((min(x0, x1), min(y0, y1)))
        a.set_width(abs(x1 - x0))
        a.set_height(abs(y1 - y0))
    else:
        a.set_xy([fn(tuple(p)) for p in a.get_xy()[:-1]] if len(a.get_xy()) > 1 and tuple(a.get_xy()[0]) == tuple(a.get_xy()[-1]) else [fn(tuple(p)) for p in a.get_xy()])


def _row_area(figs, pid, fid):
    return [a for a in _arts(figs, pid, fid) if not getattr(a, "_sc_hidden_copy", False) and not isinstance(a, Line2D)]


def _flip_z(figs, pid, fid):
    arts = _row_area(figs, pid, fid)
    z0, z1 = sc.extent_z([P for a in arts for P in sc.artist_polys(a)])
    for a in arts:
        _xform(a, lambda p: (p[0], z0 + z1 - p[1]))


def _shift(figs, pid, fid, dz, du=0.0):
    for a in _row_area(figs, pid, fid):
        _xform(a, lambda p: (p[0] + du, p[1] + dz))


def _zS(P, z_A):
    return check_stack.to_shop_floor(z_A, P)


def _piece_arts(figs, pid, fid, name, side=None):
    return [a for a in _row_area(figs, pid, fid) if getattr(a, PIECE_ATTR, None) == name
            and (side is None or (sc.centroid(sc.artist_polys(a))[0] > 0) == (side > 0))]


# ---------------------------------------------------------------- S4-1

def s4_1_b1():
    """S4-1 B: holder.flange_thickness dropped from the stack (0): collar top by the test_P18 formula 151.84 against
    stop.collar_top_z 159.84 (the drawn collar follows the stack)."""
    return s4_ctx(values={"holder.flange_thickness": 0})


# ---------------------------------------------------------------- S4-2

def _drop_carrier(sp):
    sp["features"] = [r for r in sp["features"] if r["id"] != "carrier"]
    core = next(r for r in sp["features"] if r["id"] == "core_100")
    core["z_rule"] = {"z_min": "core_stop", "z_max": "core_stop + core.length_short"}
    core["mark"] = dict(core["mark"], z="core_stop + core.length_short - core.top_chamfer")
    for r in sp["features"]:
        r["neighbours"] = [n for n in (r.get("neighbours") or []) if n.get("id") != "carrier"]
        r["sense"] = [s for s in (r.get("sense") or []) if s.get("seat") != "carrier" and s.get("of") != "carrier"]


def s4_2_b1():
    """S4-2 B1 (spec B form): carrier deleted, the core on the core seat (42.50 to 142.50): (a) carrier not drawn and (b)
    exposure -10.59 in both figures."""
    return s4_ctx(spec_mut=_drop_carrier)


def s4_2_b2():
    """S4-2 B2: carrier.length 150 drawn faithfully: exposure 139.41 < 143.12 in both figures."""
    return s4_ctx(values={"carrier.length": 150})


def s4_2_b3():
    """S4-2 B3: carrier bottom drawn at 66.00 z_A in figure 1 (top kept): (a) carrier off its seat and (c) no grip
    overlap."""
    def mut(figs, P, spec, stack):
        z_top = _zS(P, 202.5)
        for a in _row_area(figs, "carrier", "carrier"):
            _xform(a, lambda p: (p[0], p[1] if p[1] >= z_top - 1e-6 else _zS(P, 66.0)))
    return s4_ctx(mutate=mut)


# ---------------------------------------------------------------- S4-3 (kept-part sense)

def s4_3_b1():
    """S4-3 B: collet flipped end for end in figure 1 (foot ring at the top, cone widening upward)."""
    return s4_ctx(mutate=lambda figs, *a: _flip_z(figs, "carrier", "collet"))


def s4_3_b2():
    """S4-3 B: washer drawn above the nut plate (moved up 8.30, bottom 153.39 over the plate top 153.09), figure 1."""
    return s4_ctx(mutate=lambda figs, *a: _shift(figs, "carrier", "washer", 8.30))


def s4_3_b3():
    """S4-3 B: wing nut drawn 10 low in figure 1 (pocket rim 135.59, below the flange top 145.09): clears_above fires and
    the washer reads outside nut and holder."""
    def mut(figs, *a):
        _shift(figs, "carrier", "wingnut", -10.0)
    return s4_ctx(mutate=mut)


def s4_3_b4():
    """S4-3 B: receiver flipped end for end in figure 1 (floor piece at the top)."""
    return s4_ctx(mutate=lambda figs, *a: _flip_z(figs, "carrier", "receiver"))


def s4_3_b5():
    """S4-3 B: core and carrier stack inverted in figure 1 (core 42.50 to 142.50 on the seat, carrier 142.50 to 302.50
    above it)."""
    def mut(figs, P, spec, stack):
        _shift(figs, "carrier", "core_100", -160.0)
        _shift(figs, "carrier", "carrier", 100.0)
    return s4_ctx(mutate=mut)


def s4_3_b6():
    """S4-3 B (S4-d): collet bore drawn parallel to the outer cone in figure 1 (the cone piece inner edge given the cone
    slope: inner top vertex at r 50.50 - 23.705 tan 10 = 46.32)."""
    def mut(figs, P, spec, stack):
        t = math.tan(math.radians(P.get("cone.alpha")))
        for a in _piece_arts(figs, "carrier", "collet", "cone"):
            xy = [tuple(p) for p in a.get_xy()]
            xy = xy[:-1] if xy[0] == xy[-1] else xy
            zlo = min(p[1] for p in xy)
            rin = min(abs(p[0]) for p in xy)
            a.set_xy([(math.copysign(abs(x) - (z - zlo) * t, x), z) if abs(abs(x) - rin) < 1e-6 else (x, z) for x, z in xy])
    return s4_ctx(mutate=mut)


def s4_3_b7():
    """S4-3 B (holder inner-edge taper): holder cone piece drawn with its bore widening upward in figure 1 (inner
    vertices r 56.75 at the bottom and 62.04 at the top, swapped)."""
    def mut(figs, P, spec, stack):
        for a in _piece_arts(figs, "carrier", "holder", "cone"):
            xy = [tuple(p) for p in a.get_xy()]
            xy = xy[:-1] if xy[0] == xy[-1] else xy
            zs = sorted({round(p[1], 6) for p in xy})
            inner = sorted([p for p in xy if abs(p[0]) < max(abs(q[0]) for q in xy) - 1e-6], key=lambda p: p[1])
            rb, rt = abs(inner[0][0]), abs(inner[-1][0])
            sw = {inner[0]: (math.copysign(rt, inner[0][0]), inner[0][1]), inner[-1]: (math.copysign(rb, inner[-1][0]), inner[-1][1])}
            a.set_xy([sw.get(p, p) for p in xy])
    return s4_ctx(mutate=mut)


# ---------------------------------------------------------------- K8: min_bearing on the drawn S4 figure 2

def bearing_b():
    """K8 B (Designer P3a FIX 3, the S4 drawn B): carrier drawn at r 49.90 in figure 2 (inside the d 105 ledge r 50.00 to
    53.00): bearing width 0."""
    def mut(figs, P, spec, stack):
        for a in _row_area(figs, "liner", "carrier"):
            _xform(a, lambda p: (math.copysign(49.90, p[0]), p[1]))
    return s4_ctx(mutate=mut)


# ---------------------------------------------------------------- K8: section_true premise (O7)

def st_piece_missing():
    """K8 B (section_true premise): the holder flange piece at +u not drawn in figure 1."""
    def mut(figs, *a):
        for x in _piece_arts(figs, "carrier", "holder", "flange", side=1):
            x.remove()
    return s4_ctx(mutate=mut)


def st_piece_moved():
    """K8 B (section_true premise): the receiver shoulder at +u drawn 1.00 high in figure 1."""
    def mut(figs, *a):
        for x in _piece_arts(figs, "carrier", "receiver", "shoulder", side=1):
            _xform(x, lambda p: (p[0], p[1] + 1.0))
    return s4_ctx(mutate=mut)


def st_piece_untagged():
    """K8 B (section_true premise): the holder tube at -u drawn without its piece name in figure 1."""
    def mut(figs, *a):
        for x in _piece_arts(figs, "carrier", "holder", "tube", side=-1):
            delattr(x, PIECE_ATTR)
    return s4_ctx(mutate=mut)


def st_k5_untagged():
    """K5 B (section_true admission): the receiver rim (5 vertices) at +u drawn without its piece name in figure 1, so
    the cylinder row reads a polygon."""
    def mut(figs, *a):
        for x in _piece_arts(figs, "carrier", "receiver", "rim", side=1):
            delattr(x, PIECE_ATTR)
    return s4_ctx(mutate=mut)


def st_k5_moved():
    """K5 B (section_true admission, poly_match premise): the receiver rim at +u keeps its piece name and is drawn 1.00
    high in figure 1, so it equals no spec piece and the cylinder row reads a polygon."""
    def mut(figs, *a):
        for x in _piece_arts(figs, "carrier", "receiver", "rim", side=1):
            _xform(x, lambda p: (p[0], p[1] + 1.0))
    return s4_ctx(mutate=mut)


# ---------------------------------------------------------------- K5: slit ticks (Topologist P2r 3.1, form (a))

def _slit_lines(figs, pid="carrier", fid="collet"):
    arts = _arts(figs, pid, f"{fid}:slits")
    verts = [a for a in arts if abs(a.get_xdata()[0] - a.get_xdata()[1]) < 1e-9]
    ticks = [a for a in arts if a not in verts]
    pos = next(a for a in verts if a.get_xdata()[0] > 0)
    neg = next(a for a in verts if a.get_xdata()[0] < 0)
    # P5f: the tick of a line is the horizontal tick on its side (tick: wall; the P4 form centred it on the line)
    tick = lambda v: next(t for t in ticks if (sum(t.get_xdata()) > 0) == (v.get_xdata()[0] > 0))  # noqa: E731
    return pos, neg, tick(pos), tick(neg)


def slits_undeclared():
    """K5 B (undeclared ticks): collet sub_artists without slits; the ticks drawn (figure 1)."""
    def mut(figs, P, spec, stack):
        next(r for r in spec["features"] if r["id"] == "collet")["sub_artists"] = []
    return s4_ctx(mutate=mut)


def slits_count():
    """K5 B (n): the tick of the -u slit line deleted (figure 1)."""
    def mut(figs, *a):
        _slit_lines(figs)[3].remove()
    return s4_ctx(mutate=mut)


def slits_sign():
    """K5 B (i): the +u line (theta 112) moved to u -57.40 and its tick mirrored to the -u wall (figure 1; P5f re-plant:
    the tick spans the wall, so the mirrored tick passes (t) and only (i) fires)."""
    def mut(figs, *a):
        pos, _, tp, _ = _slit_lines(figs)
        u0 = pos.get_xdata()[0]
        pos.set_data([-u0, -u0], pos.get_ydata())
        tp.set_data([-x for x in tp.get_xdata()], tp.get_ydata())
    return s4_ctx(mutate=mut)


def _move_pos(figs, u=None, z_hi=None, solid=False, tick=False):
    """Plant on the +u slit line (figure 1). P5f: the tick spans the wall, so it moves with the line only when tick."""
    pos, _, tp, _ = _slit_lines(figs)
    u0 = pos.get_xdata()[0]
    lo, hi = sorted(pos.get_ydata())
    if u is not None:
        pos.set_data([u, u], [lo, hi])
        if tick:
            tx = tp.get_xdata()
            tp.set_data([x - u0 + u for x in tx], tp.get_ydata())
    if z_hi is not None:
        uu = pos.get_xdata()[0]
        pos.set_data([uu, uu], [lo, z_hi])
    if solid:
        pos.set_linestyle("-")


def slits_contain():
    """K5 B (ii): the +u line at the as-spec projection u +51.32, 47.00 to 72.00 (5.48 above the drawn hull; its top end
    also misses the top face, (iii))."""
    def mut(figs, P, spec, stack):
        _move_pos(figs, u=51.322)
    return s4_ctx(mutate=mut)


def slits_open_face():
    """K5 B (iii): the +u line at u +51.32 ended on the chamfer edge at 66.52 z_A (form (b)): inside the hull, off the top
    face."""
    def mut(figs, P, spec, stack):
        _move_pos(figs, u=51.322, z_hi=_zS(P, 66.522))
    return s4_ctx(mutate=mut)


def slits_solid():
    """K5 B (iv): the +u line drawn solid (figure 1)."""
    return s4_ctx(mutate=lambda figs, *a: _move_pos(figs, solid=True))


def slits_tick():
    """K5 B (t): the -u line's tick moved from its closed end (65.00) to its open end (40.00), figure 1."""
    def mut(figs, P, spec, stack):
        _, neg, _, tn = _slit_lines(figs)
        lo = min(neg.get_ydata())
        tn.set_data(tn.get_xdata(), [lo, lo])
    return s4_ctx(mutate=mut)


# ---------------------------------------------------------------- K5: wing (Designer P3a O3) and sweep

def _wing(figs, pid="carrier"):
    return _arts(figs, pid, "wingnut:wing")[0]


def wing_solid():
    """K5 B (wing (i)): the -X wing outline drawn solid (figure 1)."""
    return s4_ctx(mutate=lambda figs, *a: _wing(figs).set_linestyle("-"))


def wing_u9():
    """K5 B (wing (ii)): the wing drawn at u 5.50 to 12.50 (centre 9) in figure 1."""
    def mut(figs, *a):
        w = _wing(figs)
        w.set_x(5.5)
    return s4_ctx(mutate=mut)


def wing_no_band():
    """K5 B (wing (w0)): wing.x_band deleted from the spec; the wing drawn."""
    def sm(sp):
        r = next(r for r in sp["features"] if r["id"] == "wingnut")
        r["wing"] = {k: v for k, v in r["wing"].items() if k != "x_band"}
    return s4_ctx(spec_mut=sm)


def wing_unoccluded():
    """K5 B (wing (iii)): the wingnut body and plate pieces deleted from section_true (drawn faithfully): the wing ends at
    113.09 and 153.09 have no occluding piece."""
    def sm(sp):
        r = next(r for r in sp["features"] if r["id"] == "wingnut")
        r["section_true"] = {k: v for k, v in r["section_true"].items() if k not in ("body", "plate")}
    return s4_ctx(spec_mut=sm)


def sweep_solid():
    """K5 B (sweep (s2)): the +u sweep line drawn solid (figure 1)."""
    def mut(figs, *a):
        next(a for a in _arts(figs, "carrier", "wingnut:sweep") if a.get_xdata()[0] > 0).set_linestyle("-")
    return s4_ctx(mutate=mut)


def sweep_radius():
    """K5 B (sweep (s3)): both sweep lines at r 110 (sweep.r 115), figure 1."""
    def mut(figs, *a):
        for x in _arts(figs, "carrier", "wingnut:sweep"):
            s = 1 if x.get_xdata()[0] > 0 else -1
            x.set_data([s * 110.0] * 2, x.get_ydata())
    return s4_ctx(mutate=mut)


# ---------------------------------------------------------------- K8: hatch adjacency (Designer P2r R1, R2)

def hadj_s4_callsite():
    """K8 B (Designer P2r R1): the lint reached through k8 / section_convention_issues on the S4 figures with the
    receiver hatch_variant removed (drawn faithfully): receiver // beside holder // (0.25) and base plate // (0.00)."""
    def sm(sp):
        next(r for r in sp["features"] if r["id"] == "receiver").pop("hatch_variant")
    return s4_ctx(spec_mut=sm)


# ---------------------------------------------------------------- X1 on section_true (Loftsman P3b O2 (i))

ST_ROWS = ("receiver", "collet", "core_seat", "holder", "collar", "wingnut")


def _x1_specs(change=None):
    import check_sketch
    specs = check_sketch.specs_in(SK)
    s4 = {r["id"]: r for r in specs["s4"]["features"]}
    for nm in ("s1", "s3"):
        for r in specs[nm]["features"]:
            if r["id"] in ST_ROWS:
                r["section_true"] = copy.deepcopy(s4[r["id"]]["section_true"])
    if change:
        change(specs)
    return check_sketch.x1_lint(specs)


def x1_st_z():
    """X1 Z (section_true): live specs with the S4 section_true copied onto the six base rows of s1 and s3 (the staged P6
    form): equal on every row that carries it."""
    return _x1_specs()


def x1_st_b():
    """X1 B (section_true): as Z with the s3 holder flange outer radius written holder.flange_od / 2 + 1."""
    def ch(specs):
        h = next(r for r in specs["s3"]["features"] if r["id"] == "holder")
        h["section_true"]["flange"][1] = "holder.flange_od / 2 + 1"
    return _x1_specs(ch)


# ---------------------------------------------------------------- P5f (1.4 (c) fix pass): Software Engineer FIX 1 to 4

def s4_1_b2():
    """S4-1 B2 (SW FIX 1, E3): the collar drawn 1.00 high in figure 1: drawn collar top 160.84 against the formula."""
    return s4_ctx(mutate=lambda figs, *a: _shift(figs, "carrier", "collar", 1.0))


def s4_1_b3():
    """S4-1 B3 (SW FIX 1, E4): spec s4_checks.S4-1.formula without ' + holder.flange_thickness' (151.84)."""
    def sm(sp):
        f = sp["s4_checks"]["S4-1"]["formula"]
        assert " + holder.flange_thickness" in f
        sp["s4_checks"]["S4-1"]["formula"] = f.replace(" + holder.flange_thickness", "", 1)
    return s4_ctx(spec_mut=sm)


def s4_2_b4():
    """S4-2 B4 (SW FIX 4, E12): core_100 drawn 2.00 high in figure 1: (a) core bottom minus carrier top 2.000."""
    return s4_ctx(mutate=lambda figs, *a: _shift(figs, "carrier", "core_100", 2.0))


def s4_2_b5():
    """S4-2 B5 (SW FIX 2, E5): the liner's area artists removed in figure 2: (c) grip member liner not drawn."""
    def mut(figs, *a):
        for x in _row_area(figs, "liner", "liner"):
            x.remove()
    return s4_ctx(mutate=mut)


def sweep_count():
    """K5 B (sweep (s1); SW FIX 3, Topologist F3): the +u sweep line removed in figure 1."""
    def mut(figs, *a):
        next(a for a in _arts(figs, "carrier", "wingnut:sweep") if a.get_xdata()[0] > 0).remove()
    return s4_ctx(mutate=mut)


# ---------------------------------------------------------------- P5f: Topologist F1 (slit ticks)

def slits_tick_past():
    """K5 B (F1 a, (t)): the -u tick in figure 2 drawn 1.00 past the outer cone edge (-60.23 against the wall -59.23)."""
    def mut(figs, *a):
        _, neg, _, tn = _slit_lines(figs, "liner", "collet_105")
        x0, x1 = sorted(tn.get_xdata())
        tn.set_data([x0 - 1.0, x1], tn.get_ydata())
    return s4_ctx(mutate=mut)


def slits_union():
    """K5 B (F1 b, (ii)): the -u line moved to u -59.80 in figure 1 (inside the convex hull of the side pieces, outside
    their union above z_A 64.0); the tick stays across the wall."""
    def mut(figs, *a):
        _, neg, _, _ = _slit_lines(figs)
        neg.set_data([-59.80, -59.80], neg.get_ydata())
    return s4_ctx(mutate=mut)


def slits_front():
    """K5 B (F1 c, (i0)): the +u spec line at slit k 1 (theta 82: in front of the plane, sin > 0), drawn faithfully."""
    def sm(sp):
        ln = next(r for r in sp["features"] if r["id"] == "collet")["slits"]["lines"][0]
        assert "2 * 360" in ln["theta"]
        ln["theta"] = ln["theta"].replace("2 * 360", "1 * 360")
    return s4_ctx(spec_mut=sm)


def slits_tick_solid():
    """K5 B (F1 d): the +u tick drawn solid (figure 1)."""
    return s4_ctx(mutate=lambda figs, *a: _slit_lines(figs)[2].set_linestyle("-"))


# ---------------------------------------------------------------- P5f: Topologist F2, Designer D-c1 and N1 (wing)

def _wing_spec(fn):
    def sm(sp):
        fn(next(r for r in sp["features"] if r["id"] == "wingnut"))
    return sm


def wing_relief_gone():
    """K5 B (F2 a, (iii) edges): the relief piece deleted from wingnut section_true (drawn faithfully): the wing edges
    cross 139.09 to 145.59 z_A with no occluder (the four corners stay occluded)."""
    return s4_ctx(spec_mut=_wing_spec(lambda r: r["section_true"].pop("relief")))


def wing_wide():
    """K5 B (Designer D-c1, term r_out > |u|): spec wing.u -90 to 90, drawn so: no piece with r_out <= 83.14 is wider."""
    return s4_ctx(spec_mut=_wing_spec(lambda r: r["wing"].__setitem__("u", ["-90", "90"])))


def wing_band_inside():
    """K5 B (Designer D-c1, term r_out <= -x_band[1]): spec wing.x_band near end -70 (inside the body r 83.14)."""
    return s4_ctx(spec_mut=_wing_spec(lambda r: r["wing"].__setitem__("x_band", ["-wingnut.span / 2", "-70"])))


def wing_sight_wide():
    """K5 B ((iii) premise, F2 c): spec wing.u -60 to 60, drawn so: the edges are covered, but every occluder read has
    asin(60 / r_in) >= 45 deg (in-front material reaches toward the plane cuts at theta 90 / 270)."""
    return s4_ctx(spec_mut=_wing_spec(lambda r: r["wing"].__setitem__("u", ["-60", "60"])))


def wing_hatched():
    """K5 B (Designer N1, (i)): the -X wing drawn dashed and unfilled with hatch '//' (figure 1)."""
    return s4_ctx(mutate=lambda figs, *a: _wing(figs).set_hatch("//"))


def plane_cut_side():
    """K8 B (F2 c, plane_cuts lint): the wingnut pocket_rim plane cut on side +u given theta 270."""
    def sm(sp):
        c = next(r for r in sp["features"] if r["id"] == "wingnut")["plane_cuts"][0]
        c["theta"] = "270"
    return s4_ctx(spec_mut=sm)


# ---------------------------------------------------------------- P5f: Topologist F4 (between order)

def s4_3_b8():
    """S4-3 B (F4): washer 1.5 low and wing nut 2.5 low in figure 1: (z_mid - flange top) -0.85 and (plate bottom -
    z_mid) -0.35, product +0.30 (the product form passed); wingnut clears_above fires as well."""
    def mut(figs, *a):
        _shift(figs, "carrier", "washer", -1.5)
        _shift(figs, "carrier", "wingnut", -2.5)
    return s4_ctx(mutate=mut)


# ---------------------------------------------------------------- P5f: Topologist F5 (not_drawn omit: hidden)

def _nd_plant(entry):
    def sm(sp):
        sp["not_drawn"] = list(sp.get("not_drawn") or []) + [entry]
    return s4_ctx(spec_mut=sm)


def hidden_in_plane():
    """K8 B (F5 (h1)): a hidden holder insert at theta 90 (in the plane)."""
    return _nd_plant({"part": "plant insert at theta 90", "omit": "hidden", "rows": ["holder"], "theta": [90],
                      "r": ["holder.insert_circle_radius - holder.insert_dia / 2", "holder.insert_circle_radius + holder.insert_dia / 2"],
                      "z": ["collar_top - collar.thickness - holder.insert_depth", "collar_top - collar.thickness"], "t": 0})


def hidden_front_uncut():
    """K8 B (F5 (h2)): a hidden feature at theta 0 (in front) on the unsectioned carrier, r 49.50 to 50.50, z_A 100 to 110."""
    return _nd_plant({"part": "plant carrier feature at theta 0", "omit": "hidden", "rows": ["carrier"], "theta": [0],
                      "r": ["carrier.diameter / 2 - 1", "carrier.diameter / 2"], "z": ["core_stop + 57.5", "core_stop + 67.5"], "t": 0})


def hidden_unoccluded():
    """K8 B (F5 (h3)): a hidden insert on the holder bore at theta 110, r 56.75 to 57.75, z_A 130 to 136 (in the gap
    between carrier and holder bore: nothing drawn in front of part of it)."""
    return _nd_plant({"part": "plant insert at theta 110", "omit": "hidden", "rows": ["holder"], "theta": [110],
                      "r": ["holder.insert_circle_radius - 5.25", "holder.insert_circle_radius - 4.25"],
                      "z": ["holder_bottom + 80.91", "holder_bottom + 86.91"], "t": 0})


# ---------------------------------------------------------------- P5f: Software Engineer FIX 5 (RPT from checks_s3.loads)

def deps_run_s4():
    """DEPS Z (SW FIX 5): a live s4 run (stub, rev 0; record to a temporary wip/) lists s3_spec.yaml in deps.spec_read
    with its SHA-256 (the RPT kept_axial and seat_bearing values read checks_s3.loads on it), and nothing else there."""
    import json
    import check_sketch as cs
    import step14_fixtures as s14
    t = s14._tmp()
    cs.main(["s4", "--rev", "0", "--wip-dir", str(t)])   # the stub record's checks are not judged here
    rec = json.loads((t / "s4_checks_r0.json").read_text(encoding="utf-8"))
    sr = {(x.get("path"), x.get("sha256")) for x in (rec.get("deps") or {}).get("spec_read") or []}
    want = {("s3_spec.yaml", cs._sha(SK / "s3_spec.yaml"))}
    iss = [] if sr == want else [f"deps spec_read {sorted(sr)} against {sorted(want)}"]
    kept = ((rec.get("reported_drawn") or {}).get("items") or {}).get("kept_axial") or {}
    if "checks_s3.loads" not in str(kept.get("basis")):
        iss.append(f"kept_axial basis {kept.get('basis')!r}")
    return s14._res("DEPS", bool(iss), sc._summ(iss) if iss else "s4 run records deps.spec_read s3_spec.yaml (RPT kept_axial from checks_s3.loads)", len(iss))


def full_draw():
    """Smoke (S4-FULL): every S4 row drawn in both figures (fixture), every check run: none errors, none fails closed on an
    absent part."""
    import importlib
    cs4 = importlib.import_module("checks_s4")
    return s4_live(), (lambda ctx: cs4.run(ctx))


def hadj_family():
    """K8 B (orchestrator ruling on Designer P2r R2, the 1.3 R2-4 rule): the synthetic S4 stack (step14_fixtures._hadj)
    with the receiver variant removed and the receiver drawn '////' beside the holder '//' (0.25): one line family, so
    the adjacency lint fires; section convention 1 also reads '////' against the material '//'."""
    import step14_fixtures
    return step14_fixtures._hadj(variant=None, drawn="////")
