"""Shared plot and check library for the Step 1 sketches (research/sean/gameplan.md detail 1.0).

- Loader: re-exported from sketch_loader (params.yaml, then the overlay, leaf merge; load_spec rejects non-string keys).
- setup_figure(view): the only place figure size, dpi, aspect and grid are set.
- draw(feature_id, artist, ax): tags the artist with gid = feature_id and adds it.
- K1 to K9: each takes a Ctx and returns a result dict {id, result: pass|fail, reason, measured, threshold, n_issues, cause}.
  cause: "absent" when every issue is an undrawn part (fail-closed), else "content" (SW-7).
Geometry (K7) in plain Python: Sutherland-Hodgman convex clipping, convex polygon minimum distance, convex hull.
All measurements are in rendered data coordinates: each artist's own transform is applied (TP-1).
"""
import ast
import importlib.util
import math
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_agg import FigureCanvasAgg  # noqa: E402
from matplotlib.collections import Collection  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle, Ellipse, Patch, Polygon, Rectangle  # noqa: E402
from matplotlib.text import Text  # noqa: E402,F401

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from sketch_loader import LEGAL_STATUS, LEAF_FIELDS, Params, load_yaml, load_spec, find_root  # noqa: E402,F401

TOL_Z = 0.05          # K6, K8 rests_on, K8 placement: mm in data coordinates
TOL_C = 0.05          # K7 contact distance, mm
TOL_AREA = 0.01       # K7 overlap area, mm^2
TOL_ANCHOR = 0.01     # K6 stack anchors (test_P18 tolerance)
K1_ALLOWED = {0, 1, -1, 2, 0.5}
SOFT_KEYS = ("jig.height_target", "jig.height_is_soft", "core.length_install", "core.length_optional")
SIDE_VIEWS = ("side_xz", "section_xz")
VIEW_NORMAL = {"side_xz": "Y", "section_xz": "Y", "plan_xy": "Z"}
VIEW_LABELS = {"side_xz": ("x (mm)", "z (mm)"), "section_xz": ("x (mm)", "z (mm)"),
               "plan_xy": ("x (mm)", "y (mm)"), "stock": ("length (mm)", "bar (mm)")}
FIGSIZE = {"plan_xy": (10, 10)}
FIGSIZE_DEFAULT = (14, 10)
DPI = 150
CITATION = re.compile(r"\[CP §\s*\d+(\.\d+)*,\s*\d{1,2}:\d{2}\]|\[DN23\]")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
ROUND_KINDS = ("cylinder", "screw", "cone", "gear")
NO_AREA_KINDS = ("line", "arrow", "callout")


class Ctx:
    """What a check sees: params, spec (the feature table), figures per pose, check_stack values, file paths."""

    def __init__(self, P=None, spec=None, figs=None, stack=None, view=None, script_paths=None,
                 overlay_path=None, check_stack_path=None, anchors=None):
        self.P, self.spec, self.figs, self.stack = P, spec or {}, figs or {}, stack
        self.view = view or (spec or {}).get("view")
        self.script_paths = [Path(p) for p in (script_paths or [])]
        self.overlay_path = overlay_path
        self.check_stack_path = check_stack_path
        self.anchors = anchors


def result(cid, ok, reason, measured=None, threshold=None, n_issues=None, cause=None, **extra):
    out = {"id": cid, "result": "pass" if ok else "fail", "reason": reason, "measured": measured, "threshold": threshold,
           "n_issues": n_issues if n_issues is not None else (0 if ok else 1),
           "cause": None if ok else (cause or "content")}
    out.update(extra)
    return out


def _summ(issues, n=6):
    s = "; ".join(issues[:n])
    return s + (f"; ... {len(issues) - n} more" if len(issues) > n else "")


def _cause(n_absent, n_total):
    return "absent" if n_total and n_absent == n_total else "content"


# ======================================================================== figure and drawing helpers

def setup_figure(view, title=""):
    """Sole owner of figsize, dpi, aspect and grid (K3). Side views are seen from -Y looking along +Y (+X right, +Z up)."""
    fig = Figure(figsize=FIGSIZE.get(view, FIGSIZE_DEFAULT), dpi=DPI)
    FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    ax.set_title(f"{view}: {title}" if title else view)
    xl, yl = VIEW_LABELS.get(view, ("x (mm)", "y (mm)"))
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.set_aspect("equal")
    ax.minorticks_on()
    ax.grid(True, which="major", linewidth=0.6)
    ax.grid(True, which="minor", linewidth=0.3, alpha=0.5)
    fig.sketch_view = view
    return fig, ax


def draw(feature_id, artist, ax=None):
    ax = ax if ax is not None else plt.gca()
    artist.set_gid(feature_id)
    if isinstance(artist, Patch):
        ax.add_patch(artist)
    elif isinstance(artist, Line2D):
        ax.add_line(artist)
    elif isinstance(artist, Collection):
        ax.add_collection(artist)
    else:
        ax.add_artist(artist)
    return artist


def draw_rect(ax, fid, x0, x1, z0, z1, **kw):
    kw.setdefault("fill", False)
    return draw(fid, Rectangle((min(x0, x1), min(z0, z1)), abs(x1 - x0), abs(z1 - z0), **kw), ax)


def draw_trap(ax, fid, x0, x1, h0, h1, z0, **kw):
    """Four-vertex trapezoid: height h0 at x0, h1 at x1, base at z0."""
    kw.setdefault("fill", False)
    return draw(fid, Polygon([(x0, z0), (x1, z0), (x1, z0 + h1), (x0, z0 + h0)], closed=True, **kw), ax)


def draw_gear_section(ax, fid, r_in, r_out, z0, z1, rise=None, **kw):
    """Bevel ring gear in side section, teeth facing down onto pinions below (TP-2 ruling, gameplan Design Notes 22):
    two four-vertex pieces mirrored about x = 0; flat back face on top (z1) from r_in to r_out; bore edge vertical;
    tooth face underneath rising outward from (r_in, z0) to (r_out, z0 + rise). Each piece narrows downward."""
    kw.setdefault("fill", False)
    h = z1 - z0
    rise = h / 2 if rise is None else rise
    right = [(r_in, z0), (r_out, z0 + rise), (r_out, z1), (r_in, z1)]
    left = [(-x, z) for x, z in right]
    return [draw(fid, Polygon(right, closed=True, **kw), ax), draw(fid, Polygon(left, closed=True, **kw), ax)]


def draw_hline(ax, fid, x0, x1, z, **kw):
    return draw(fid, Line2D([x0, x1], [z, z], **kw), ax)


def label_text(row, P):
    lab = row["label"]
    if "label_text_override" in row:
        return row["label_text_override"]
    txt = f"{lab['text']} {format(P.get(lab['key']), lab.get('fmt', '.1f'))}"
    return txt + (f" {lab['suffix']}" if lab.get("suffix") else "")


def place_labels(ax, spec, P, pose=None):
    """One annotation per spec row with a label, gid label:<id>, anchored at the right edge of the row's drawn pieces."""
    for row in spec.get("features", []):
        if not row.get("label") or (pose and row.get("poses") and pose not in row["poses"]):
            continue
        pts = [p for poly in pieces(ax, row["id"]) for p in poly]
        if not pts:
            continue
        x = max(p[0] for p in pts)
        z = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
        ann = ax.annotate(label_text(row, P), xy=(x, z), xytext=(x + 60, z + 20), fontsize=7,
                          arrowprops={"arrowstyle": "-", "linewidth": 0.5})
        ann.set_gid(f"label:{row['id']}")


def finish_axes(ax):
    ax.relim()
    ax.autoscale_view()


# ======================================================================== artist access

def artists(ax):
    return list(ax.patches) + list(ax.lines) + list(ax.collections)


def tagged(ax):
    out = {}
    for a in artists(ax):
        if a.get_gid():
            out.setdefault(a.get_gid(), []).append(a)
    return out


def _to_data(a):
    """Transform from the artist's own coordinates to rendered data coordinates (TP-1). Uses the artist's full transform:
    T - transData when the chain ends in transData, else T followed by the inverse of transData (axes or figure
    coordinates mapped to where they render at the current limits)."""
    ax = a.axes
    T = a.get_transform()
    if ax is None:
        return a.get_patch_transform() if isinstance(a, Patch) else None
    if T.contains_branch(ax.transData):
        return T - ax.transData
    return T + ax.transData.inverted()


def _xy(T, pts):
    arr = np.asarray(pts, dtype=float).reshape(-1, 2)
    if T is not None:
        arr = T.transform(arr)
    return [(float(x), float(y)) for x, y in arr]


def artist_polys(a):
    """Polygons in rendered data coordinates (closing vertex dropped)."""
    T = _to_data(a)
    if isinstance(a, Line2D):
        return [_xy(T, list(zip(a.get_xdata(), a.get_ydata())))]
    if isinstance(a, Patch):
        path = a.get_path().transformed(T) if T is not None else a.get_path()
        polys = path.to_polygons(closed_only=False) or [path.vertices]
        out = []
        for poly in polys:
            pts = [(float(x), float(y)) for x, y in poly]
            if len(pts) > 1 and abs(pts[0][0] - pts[-1][0]) < 1e-12 and abs(pts[0][1] - pts[-1][1]) < 1e-12:
                pts = pts[:-1]
            out.append(pts)
        return out
    if isinstance(a, Collection):
        offs = np.asarray(a.get_offsets(), dtype=float).reshape(-1, 2)
        offT = a.get_offset_transform()
        if a.axes is not None and offT is not None:
            offT = offT - a.axes.transData if offT.contains_branch(a.axes.transData) else offT + a.axes.transData.inverted()
        out = []
        for i, p in enumerate(a.get_paths()):
            pts = _xy(T, p.vertices)
            if len(offs) and np.any(offs):
                ox, oy = offT.transform(offs[i % len(offs)]) if offT is not None else offs[i % len(offs)]
                pts = [(x + ox, y + oy) for x, y in pts]
            out.append(pts)
        return out
    return []


def pieces(ax, gid):
    return [poly for a in tagged(ax).get(gid, []) for poly in artist_polys(a)]


def extent_z(polys):
    zs = [p[1] for poly in polys for p in poly]
    return (min(zs), max(zs)) if zs else None


def extent_x(polys):
    xs = [p[0] for poly in polys for p in poly]
    return (min(xs), max(xs)) if xs else None


def centroid(polys):
    ax_, ay_, aw = 0.0, 0.0, 0.0
    for poly in polys:
        a = poly_area(poly)
        if abs(a) > 1e-9:
            cx = cy = 0.0
            n = len(poly)
            for i in range(n):
                x0, y0 = poly[i]
                x1, y1 = poly[(i + 1) % n]
                cr = x0 * y1 - x1 * y0
                cx += (x0 + x1) * cr
                cy += (y0 + y1) * cr
            cx /= 6 * a
            cy /= 6 * a
            w = abs(a)
        else:
            cx = sum(p[0] for p in poly) / len(poly)
            cy = sum(p[1] for p in poly) / len(poly)
            w = 1e-6
        ax_ += cx * w
        ay_ += cy * w
        aw += w
    return (ax_ / aw, ay_ / aw) if aw else None


# ======================================================================== geometry (K7)

def poly_area(P):
    n = len(P)
    return 0.5 * sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n)) if n >= 3 else 0.0


def ccw(P):
    return list(P) if poly_area(P) >= 0 else list(reversed(P))


def is_convex(P, eps=1e-9):
    n = len(P)
    if n < 4:
        return True
    sign = 0
    for i in range(n):
        o, a, b = P[i], P[(i + 1) % n], P[(i + 2) % n]
        cr = (a[0] - o[0]) * (b[1] - a[1]) - (a[1] - o[1]) * (b[0] - a[0])
        if abs(cr) > eps:
            s = 1 if cr > 0 else -1
            if sign and s != sign:
                return False
            sign = s
    return True


def clip(subject, clipper):
    """Sutherland-Hodgman: subject clipped by convex clipper. Either winding accepted (both normalised CCW)."""
    out = ccw(subject)
    C = ccw(clipper)
    if len(C) < 3:
        return []
    n = len(C)
    for i in range(n):
        a, b = C[i], C[(i + 1) % n]
        inside = lambda p: (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= -1e-12  # noqa: E731

        def cross(p, q):
            dx1, dy1 = q[0] - p[0], q[1] - p[1]
            dx2, dy2 = b[0] - a[0], b[1] - a[1]
            den = dx1 * dy2 - dy1 * dx2
            if abs(den) < 1e-15:
                return q
            t = ((a[0] - p[0]) * dy2 - (a[1] - p[1]) * dx2) / den
            return (p[0] + t * dx1, p[1] + t * dy1)
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(cross(s, e))
                out.append(e)
            elif inside(s):
                out.append(cross(s, e))
            s = e
    return out


def overlap_area(A, B):
    if len(A) < 3 or len(B) < 3:
        return 0.0
    return abs(poly_area(clip(A, B)))


def _pt_seg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _segs_cross(a, b, c, d):
    def orient(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return 0 if abs(v) < 1e-12 else (1 if v > 0 else -1)
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    return o1 * o2 < 0 and o3 * o4 < 0


def _inside(p, P):
    if len(P) < 3:
        return False
    C = ccw(P)
    n = len(C)
    return all((C[(i + 1) % n][0] - C[i][0]) * (p[1] - C[i][1]) - (C[(i + 1) % n][1] - C[i][1]) * (p[0] - C[i][0]) >= -1e-12
               for i in range(n))


def _edges(P):
    if len(P) == 1:
        return [(P[0], P[0])]
    if len(P) == 2:
        return [(P[0], P[1])]
    return [(P[i], P[(i + 1) % len(P)]) for i in range(len(P))]


def min_distance(A, B):
    """Minimum distance between two convex polygons (or segments). 0 when they touch or overlap."""
    if any(_inside(p, B) for p in A) or any(_inside(p, A) for p in B):
        return 0.0
    EA, EB = _edges(A), _edges(B)
    if any(_segs_cross(a, b, c, d) for a, b in EA for c, d in EB):
        return 0.0
    d = min(_pt_seg(p, c, e) for p in A for c, e in EB)
    return min(d, min(_pt_seg(p, a, b) for p in B for a, b in EA))


def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def pair_measure(PA, PB):
    area = sum(overlap_area(a, b) for a in PA for b in PB)
    dist = min(min_distance(a, b) for a in PA for b in PB)
    return dist, area


def pair_state(dist, area):
    if area > TOL_AREA:
        return "overlap"
    return "C" if dist <= TOL_C else "F"


def judge(cls, g_min, dist, area):
    if cls == "C":
        return dist <= TOL_C and area <= TOL_AREA
    if cls == "G":
        return area <= TOL_AREA and dist >= (g_min or 0) - TOL_C
    if cls == "F":
        return area <= TOL_AREA
    raise ValueError(f"unknown class {cls}")


def band_gap(da, db):
    """Gap between two bands along the view direction: > 0 disjoint, <= 0 overlapping, None when either is unknown."""
    if da is None or db is None:
        return None
    return max(db[0] - da[1], da[0] - db[1])


def assess_pair(cls, g_min, PA, PB, gap, names=("a", "b"), plan_gap=None):
    """One judgement for K7 static, K7 swept and S1-5b (LF-1, LF-4, TP-11).
    gap: band gap along the view direction (side: depth bands; plan: z bands); disjoint bands settle F only.
    C: fails when the bands are more than TOL_C apart. G: the 3D distance is at least max(gap, projected distance),
    so it passes when that lower bound reaches g_min. N: nested, declared, not measured.
    plan_gap (side views; a number or a callable, evaluated only when the side-view test fails): distance between
    the two parts' plan footprints from the spec placement (LF-8 at 1.1 (b)). The plan view is a projection too, so
    the 3D distance is at least max(plan_gap, projected distance): an F pair passes when plan_gap > TOL_C, a G pair
    when that lower bound reaches g_min - TOL_C. State "plan-separated". C pairs are not relieved.
    Returns (ok, state, text, lower_bound)."""
    ok, st, txt, lb = _assess_pair(cls, g_min, PA, PB, gap, names)
    if ok or plan_gap is None or cls not in ("F", "G") or st in ("non-convex", "error"):
        return ok, st, txt, lb
    pg = plan_gap() if callable(plan_gap) else plan_gap
    if pg is None:
        return ok, st, txt, lb
    g = g_min or 0
    proj = lb if (lb is not None and lb > 0) else 0.0
    lb2 = max(pg, proj)
    if (cls == "F" and pg > TOL_C) or (cls == "G" and lb2 >= g - TOL_C):
        return True, "plan-separated", f"plan footprints {pg:.3f} mm apart (side view: {txt}); lower bound {lb2:.3f}", lb2
    return False, st, f"{txt}; plan footprints {pg:.3f} mm apart, lower bound {lb2:.3f}" + (f", gap - g_min {lb2 - g:+.3f}" if cls == "G" else ""), lb


PLAN_NGON = 128


def _ngon(cx, cy, r, n=PLAN_NGON):
    """Regular n-gon circumscribing the circle (cx, cy, r): contains the circle, so distances are lower bounds."""
    R = r / math.cos(math.pi / n)
    return [(cx + R * math.cos(2 * math.pi * (i + 0.5) / n), cy + R * math.sin(2 * math.pi * (i + 0.5) / n)) for i in range(n)]


def plan_footprint(row, rec):
    """Convex plan polygon containing the part, from check_stack's placement record or, for an axis-Z round part or
    a section row without placement, the disk of its depth half-band. None when the spec gives no plan basis."""
    pl = (rec or {}).get("place")
    if pl and "r_in" in pl:
        t = math.radians(pl["theta"])
        c, s = math.cos(t), math.sin(t)
        r0, r1, w = pl["r_in"], pl["r_out"], pl["half_width"]
        if pl.get("footprint") == "radial":
            return [(r0 * c + w * s, r0 * s - w * c), (r1 * c + w * s, r1 * s - w * c),
                    (r1 * c - w * s, r1 * s + w * c), (r0 * c - w * s, r0 * s + w * c)]
        pts = _ngon(r0 * c, r0 * s, w) + (_ngon(r1 * c, r1 * s, w) if abs(r1 - r0) > 1e-9 else [])
        return convex_hull(pts)
    dep = (rec or {}).get("depth")
    round_z = row.get("kind") in ROUND_KINDS and row.get("axis") == "Z"
    if dep and (round_z or row.get("section")) and abs(dep[0] + dep[1]) < 1e-9:
        return _ngon(0.0, 0.0, dep[1])
    return None


def plan_gap_fn(ctx, rows, pose, a, b):
    """Callable for assess_pair: plan distance between rows a and b at pose, or None."""
    def f():
        fa = plan_footprint(rows.get(a, {}), _feat(ctx, pose, a))
        fb = plan_footprint(rows.get(b, {}), _feat(ctx, pose, b))
        if fa is None or fb is None:
            return None
        return min_distance(fa, fb)
    return f


def _assess_pair(cls, g_min, PA, PB, gap, names=("a", "b")):
    g = g_min or 0
    if cls == "N":
        return True, "N", "nested (declared)", None
    if cls not in ("C", "G", "F"):
        return False, "error", f"unknown class {cls}", None
    if gap is not None and gap > 0:
        if cls == "F":
            return True, "depth-separated", f"bands {gap:.3f} mm apart", gap
        if cls == "G" and gap >= g - TOL_C:
            return True, "depth-separated", f"bands {gap:.3f} mm apart, g_min {g}", gap
        if cls == "C" and gap > TOL_C:
            return False, "depth-separated", f"C pair depth-separated by {gap:.3f} mm (contact needs bands within {TOL_C})", gap
    nonconv = [n for n, PP in zip(names, (PA, PB)) if any(not is_convex(p) for p in PP)]
    if nonconv:
        return False, "non-convex", f"non-convex piece in {nonconv}; split it in the spec", None
    dist, area = pair_measure(PA, PB)
    if gap is not None and gap > 0:
        if cls == "G":
            lb = max(gap, dist)
            ok = lb >= g - TOL_C
            return ok, ("G" if ok else "short"), (f"band gap {gap:.3f} mm, projected distance {dist:.3f} mm, lower bound {lb:.3f}, "
                                                  f"g_min {g}, gap - g_min {lb - g:+.3f}"), lb
        ok = dist <= TOL_C
        return ok, ("C" if ok else "open"), f"bands touch ({gap:.3f} mm), projected distance {dist:.3f} mm", dist
    st = pair_state(dist, area)
    ok = judge(cls, g, dist, area)
    txt = f"distance {dist:.3f} mm, overlap {area:.3f} mm2, state {st}"
    if cls == "G":
        txt += f", g_min {g}, gap - g_min {dist - g:+.3f}"
    return ok, st, txt, (dist if area <= TOL_AREA else -area)


# ======================================================================== spec lint (SW-1, TP-6, TP-8)

PRED_TARGET = {"below": "of", "above": "of", "clears_above": "of", "top_within": "of", "side": "of", "outboard": "of", "rests_on": "seat",
               "mirror_about_axis": "axis", "azimuth": "expr", "taper": "narrows", "face_rises": "toward"}


def sense_lint(rows):
    """Spec errors in sense rows, one per bad predicate, never an exception. Returns (issues, ids of bad predicates)."""
    issues, bad = [], set()
    for row in rows:
        for pr in row.get("sense") or []:
            nonstr = [k for k in pr if not isinstance(k, str)]
            kind = pr.get("pred")
            need = PRED_TARGET.get(kind)
            msg = None
            if nonstr:
                msg = (f"{row['id']} {kind}: spec error, non-string key {nonstr[0]!r} (YAML 1.1 reads on/off/yes/no as booleans)"
                       + (f"; missing key '{need}'" if need and need not in pr else ""))
            elif need is None:
                msg = f"{row['id']}: spec error, unknown predicate {kind!r}"
            elif need not in pr:
                msg = f"{row['id']} {kind}: spec error, missing key '{need}'"
            if msg:
                issues.append(msg)
                bad.add(id(pr))
    return issues, bad


def duplicate_ids(rows):
    seen, dup = set(), []
    for r in rows:
        if r["id"] in seen and r["id"] not in dup:
            dup.append(r["id"])
        seen.add(r["id"])
    return dup


# ======================================================================== K1 literals, soft keys, figure settings

FIG_CALLS = {"figure", "subplots", "set_aspect", "grid", "set_size_inches", "set_dpi", "set_figwidth",
             "set_figheight", "minorticks_on", "minorticks_off", "Figure"}
FIG_KWARGS = {"figsize", "dpi"}


def k1(ctx):
    issues = []
    for path in ctx.script_paths:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"), filename=str(path))
        name = Path(path).name
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                if node.value not in K1_ALLOWED:
                    issues.append(f"{name}:{node.lineno} literal {node.value!r}")
            elif isinstance(node, ast.Compare):
                soft = [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and n.value in SOFT_KEYS]
                if soft:
                    issues.append(f"{name}:{node.lineno} comparison with soft key {soft[0]}")
            elif isinstance(node, ast.Call):
                fn = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
                if fn in FIG_CALLS:
                    issues.append(f"{name}:{node.lineno} figure setting {fn}() outside setup_figure")
                for kw in node.keywords:
                    if kw.arg in FIG_KWARGS:
                        issues.append(f"{name}:{node.lineno} figure keyword {kw.arg}= outside setup_figure")
    files = ", ".join(Path(p).name for p in ctx.script_paths) or "no script"
    return result("K1", not issues, _summ(issues) if issues else f"no literal outside {sorted(K1_ALLOWED)}, no soft-key comparison, no figure setting ({files})",
                  measured=len(issues), threshold=0, n_issues=len(issues))


# ======================================================================== K2 provenance

def spec_keys(spec):
    keys = []
    for row in spec.get("features", []):
        keys += list(row.get("keys") or [])
        if row.get("label"):
            keys.append(row["label"]["key"])
    return keys


def k2(ctx):
    P, issues = ctx.P, []
    for k in spec_keys(ctx.spec):
        if not P.has(k):
            issues.append(f"spec key {k} resolves in neither params.yaml nor the overlay")
    for k in P.shadowed:
        issues.append(f"overlay key {k} shadows params.yaml")
    for k, leaf in P.overlay.items():
        if leaf.get("_malformed"):
            issues.append(f"overlay {k}: {leaf['_malformed']}")
            continue
        miss = [f for f in LEAF_FIELDS if f not in leaf]
        if miss:
            issues.append(f"overlay {k}: missing {miss}")
        if not str(leaf.get("source") or "").strip():
            issues.append(f"overlay {k}: empty source")
        if leaf.get("status") not in LEGAL_STATUS:
            issues.append(f"overlay {k}: status {leaf.get('status')!r} not in {LEGAL_STATUS}")
        if leaf.get("status") == "DECLARED" and not CITATION.search(str(leaf.get("source") or "")):
            issues.append(f"overlay {k}: DECLARED without [CP §n, mm:ss] or [DN23]")
    n = len(P.overlay)
    return result("K2", not issues, _summ(issues) if issues else f"{len(spec_keys(ctx.spec))} spec keys resolve; {n} overlay leaves sourced, legal status, no shadow",
                  measured=len(issues), threshold=0, n_issues=len(issues))


# ======================================================================== K3 plot conventions

def _grid_on(axis, which):
    ticks = axis.get_major_ticks() if which == "major" else axis.get_minor_ticks()
    return bool(ticks) and any(t.gridline.get_visible() for t in ticks)


def k3(ctx):
    issues = []
    for name, fig in ctx.figs.items():
        ax = fig.axes[0]
        view = ctx.view
        if len(fig.axes) > 1 and not (ctx.spec or {}).get("insets"):
            issues.append(f"{name}: {len(fig.axes)} Axes in the figure, spec declares no inset (checks read the first Axes only)")
        if view not in ax.get_title():
            issues.append(f"{name}: title {ax.get_title()!r} lacks view {view}")
        for lab, txt in (("x", ax.get_xlabel()), ("y", ax.get_ylabel())):
            if not txt.strip().endswith("(mm)"):
                issues.append(f"{name}: {lab} label {txt!r} lacks (mm)")
        if ax.get_aspect() not in ("equal", 1.0):
            issues.append(f"{name}: aspect {ax.get_aspect()!r}")
        for which in ("major", "minor"):
            if not (_grid_on(ax.xaxis, which) and _grid_on(ax.yaxis, which)):
                issues.append(f"{name}: {which} grid off")
        need = FIGSIZE.get(view, FIGSIZE_DEFAULT)
        w, h = fig.get_size_inches()
        if w < need[0] - 1e-9 or h < need[1] - 1e-9:
            issues.append(f"{name}: figsize ({w:.1f}, {h:.1f}) below {need}")
        if abs(fig.dpi - DPI) > 1e-9:
            issues.append(f"{name}: dpi {fig.dpi:g} not {DPI}")
    return result("K3", not issues, _summ(issues) if issues else f"{len(ctx.figs)} figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi {DPI}",
                  measured=len(issues), threshold=0, n_issues=len(issues))


# ======================================================================== K4 labels carry their dimension

def applies(row, pose):
    return not row.get("poses") or pose in row["poses"]


def k4(ctx):
    """Each labelled row's annotation is located by gid label:<id> (SW-3) and must carry the row's text and key value."""
    issues, n = [], 0
    for pose, fig in ctx.figs.items():
        anns = {t.get_gid(): t.get_text() for t in fig.axes[0].texts if t.get_gid()}
        for row in ctx.spec.get("features", []):
            if not row.get("label") or not applies(row, pose):
                continue
            n += 1
            lab = row["label"]
            want = format(ctx.P.get(lab["key"]), lab.get("fmt", ".1f"))
            txt = anns.get(f"label:{row['id']}")
            if txt is None:
                issues.append(f"{pose}/{row['id']}: no annotation label:{row['id']}")
                continue
            if lab["text"] not in txt:
                issues.append(f"{pose}/{row['id']}: label {txt!r} lacks text {lab['text']!r}")
                continue
            nums = NUMBER.findall(txt.replace(lab["text"], " "))
            if not nums:
                issues.append(f"{pose}/{row['id']}: label {txt!r} carries no number (want {want} from {lab['key']})")
            elif not any(abs(float(m) - float(want)) < 1e-9 for m in nums):
                issues.append(f"{pose}/{row['id']}: label {txt!r} number differs from {lab['key']} = {want}")
    return result("K4", not issues, _summ(issues) if issues else f"{n} label(s) carry their key value", measured=len(issues), threshold=0,
                  n_issues=len(issues))


# ======================================================================== K5 projection

def classify(a):
    if isinstance(a, (Circle, Ellipse)):
        return "circle"
    if isinstance(a, Rectangle):
        return "rectangle"
    if isinstance(a, Line2D):
        return "line"
    if isinstance(a, Polygon):
        pts = artist_polys(a)[0]
        if len(pts) == 4:
            axis_aligned = all(abs(pts[i][0] - pts[(i + 1) % 4][0]) < 1e-9 or abs(pts[i][1] - pts[(i + 1) % 4][1]) < 1e-9 for i in range(4))
            return "rectangle" if axis_aligned else "trapezoid"
        return "polygon"
    return type(a).__name__


def expected_projection(kind, axis, normal):
    if normal is None or axis is None:
        return None
    if kind in ("cylinder", "screw"):
        return "circle" if axis == normal else "rectangle"
    if kind in ("cone", "gear"):
        return "circle" if axis == normal else "trapezoid"
    return None


def k5(ctx):
    issues, n = [], 0
    rows_list = ctx.spec.get("features", [])
    rows = {r["id"]: r for r in rows_list}
    for r in rows_list:
        if r.get("kind") in ROUND_KINDS and r.get("axis") not in ("X", "Y", "Z"):
            issues.append(f"{r['id']}: spec error, {r.get('kind')} row needs axis X, Y or Z (has {r.get('axis')!r})")
    normal = VIEW_NORMAL.get(ctx.view)
    for pose, fig in ctx.figs.items():
        for a in artists(fig.axes[0]):
            gid = a.get_gid()
            if not gid:
                issues.append(f"{pose}: untagged {type(a).__name__}")
                continue
            row = rows.get(gid)
            if row is None:
                continue
            n += 1
            want = expected_projection(row.get("kind"), row.get("axis"), normal)
            got = classify(a)
            spec_proj = row.get("projection")
            mate = row.get("bore_cone")
            if mate and got == "trapezoid" and want == "rectangle":
                # TP1.1-3: a section row whose bore follows a mating cone (holder over the collet) draws that zone as a
                # four-vertex piece; it is admitted only inside the mate's drawn z extent
                ez, mz = extent_z(artist_polys(a)), extent_z(pieces(fig.axes[0], mate))
                if mz is None or ez[0] < mz[0] - TOL_Z or ez[1] > mz[1] + TOL_Z:
                    issues.append(f"{pose}/{gid}: bore_cone trapezoid z [{ez[0]:.2f}, {ez[1]:.2f}] outside mate {mate} z "
                                  + (f"[{mz[0]:.2f}, {mz[1]:.2f}]" if mz else "(not drawn)"))
                continue
            if want:
                if got != want:
                    issues.append(f"{pose}/{gid}: {row.get('kind')} axis {row.get('axis')} in {ctx.view} drawn as {got}, needs {want}")
                if spec_proj and spec_proj != want:
                    issues.append(f"{pose}/{gid}: spec projection {spec_proj} disagrees with {want}")
            elif spec_proj:
                if got != spec_proj:
                    issues.append(f"{pose}/{gid}: {row.get('kind')} drawn as {got}, spec projection {spec_proj}")
            elif got == "circle" and normal == "Y" and row.get("kind") not in ("sphere",):
                issues.append(f"{pose}/{gid}: circle in side view for kind {row.get('kind')}")
    return result("K5", not issues, _summ(issues) if issues else f"{n} tagged artist(s) projected per kind, axis and spec projection (view normal {normal})",
                  measured=len(issues), threshold=0, n_issues=len(issues))


# ======================================================================== K6 stack

def import_violations(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    bad = []
    std = set(sys.stdlib_module_names)
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = ["." * node.level + (node.module or "")]
        for nm in names:
            top = nm.split(".")[0]
            if nm.startswith(".") or (top not in std and top != "sketch_loader"):
                bad.append(f"{Path(path).name}:{node.lineno} imports {nm}")
    return bad


_STACK_MODS = {}


def load_stack_module(path):
    path = Path(path).resolve()
    key = (str(path), path.stat().st_mtime_ns)
    if key not in _STACK_MODS:
        spec = importlib.util.spec_from_file_location(f"_check_stack_{len(_STACK_MODS)}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _STACK_MODS[key] = mod
    return _STACK_MODS[key]


def stack_anchor_issues(mod, P, hand=None):
    """LF-2: frame signs and the collar stack against independent numbers. Sign anchors: datum A sits
    jig.datum_a_above_floor above the shop floor; the receiver floor sits icd.floor_above_datum_a above datum A.
    Collar top from the test_P18 formula equals params stop.collar_top_z within 0.01. hand: manifest numbers in z_S."""
    bad = []
    a, r = P.get("jig.datum_a_above_floor"), P.get("icd.floor_above_datum_a")
    v = mod.to_shop_floor(0, P)
    if abs(v - a) > 1e-9:
        bad.append(f"to_shop_floor(0) = {v:.2f}, want +{a}")
    v = mod.from_shop_floor(0, P)
    if abs(v + a) > 1e-9:
        bad.append(f"from_shop_floor(0) = {v:.2f}, want -{a}")
    v = mod.receiver_to_datum_a(0, P)
    if abs(v - r) > 1e-9:
        bad.append(f"receiver_to_datum_a(0) = {v:.2f}, want +{r}")
    ct, want = mod.collar_top_z_A(P), P.get("stop.collar_top_z")
    if abs(ct - want) > TOL_ANCHOR:
        bad.append(f"collar_top_z_A {ct:.3f} vs params stop.collar_top_z {want}")
    if hand:
        got = {"floor_z_S": mod.to_shop_floor(mod.from_shop_floor(0, P), P),
               "datum_a_z_S": mod.to_shop_floor(0, P),
               "receiver_floor_z_S": mod.to_shop_floor(mod.receiver_to_datum_a(0, P), P),
               "collar_top_z_S": mod.to_shop_floor(mod.collar_top_z_A(P), P)}
        for k, w in hand.items():
            if abs(got[k] - w) > TOL_ANCHOR:
                bad.append(f"{k} {got[k]:.2f}, hand {w}")
    return bad


PLANE_FIELDS = ("load_plane", "entry_plane")


def plane_agreement_issues(ctx):
    """LF-16: a spec plane field names one plane twice, as a stack term (read by the park rule) and as a feature edge
    plus offset (read by S1-3). Both must resolve to the same z_A within TOL_Z. Reads the spec rows' stack z, not the
    drawing, so it holds on the stub. Only fields the spec states are linted."""
    issues = []
    if not ctx.stack or not ctx.spec:
        return issues
    import check_stack as cs  # stdlib + sketch_loader only; no cycle
    glob = ctx.stack.get("global_z_A", {})
    # LF1.1-1: stack_ties are the same agreement for a feature edge that the params stack reaches by a chain of terms
    # (holder z_max + nut plate + collar.top_above_plate = collar_top, test_P18). Each entry: {id, term, feature, edge, offset}.
    fields = [(f, ctx.spec.get(f)) for f in PLANE_FIELDS]
    fields += [(f"stack_tie {t.get('id', i)}", t) for i, t in enumerate(ctx.spec.get("stack_ties") or [])]
    for field, lp in fields:
        if not lp:
            continue
        term, feat, edge = lp.get("term"), lp.get("feature"), lp.get("edge", "z_max")
        if term not in glob:
            issues.append(f"LF-16 {field}: term {term!r} is not a stack name")
            continue
        rec = next(((p, pr["features"][feat]) for p, pr in ctx.stack["poses"].items()
                    if feat in pr["features"] and "z_min" in pr["features"][feat]), None)
        if rec is None:
            issues.append(f"LF-16 {field}: feature {feat!r} has no z_rule in any pose")
            continue
        pose, f = rec
        shift = ctx.stack["poses"][pose]["tip_z_S"] - ctx.stack["poses"][pose]["tip_z_A"]
        fz = (f["z_max"] if edge == "z_max" else f["z_min"]) - shift + cs.eval_expr(lp.get("offset", 0), ctx.P, {})
        d = abs(glob[term] - fz)
        if d > TOL_Z:
            issues.append(f"LF-16 {field}: term {term} {glob[term]:.2f} z_A vs {feat}.{edge} + offset {fz:.2f} z_A, {d:.2f} apart")
    return issues


def k6(ctx):
    issues, worst, n, absent = [], 0.0, 0, 0
    issues += plane_agreement_issues(ctx)
    if ctx.check_stack_path:
        imp = [f"import guard: {b}" for b in import_violations(ctx.check_stack_path)]
        issues += imp
        if not imp and ctx.P is not None:
            bad = stack_anchor_issues(load_stack_module(ctx.check_stack_path), ctx.P, ctx.anchors)
            if bad:
                issues.append("stack anchors: " + "; ".join(bad))
    for pose, fig in ctx.figs.items():
        feats = ctx.stack["poses"][pose]["features"]
        drawn = tagged(fig.axes[0])
        for fid, rec in feats.items():
            if "z_min" not in rec:
                continue
            n += 1
            if fid not in drawn:
                issues.append(f"{pose}/{fid}: z_rule [{rec['z_min']:.2f}, {rec['z_max']:.2f}] z_S, nothing drawn")
                absent += 1
                continue
            ez = extent_z([p for a in drawn[fid] for p in artist_polys(a)])
            d = max(abs(ez[0] - rec["z_min"]), abs(ez[1] - rec["z_max"]))
            worst = max(worst, d)
            if d > TOL_Z:
                issues.append(f"{pose}/{fid}: drawn z [{ez[0]:.2f}, {ez[1]:.2f}] vs stack [{rec['z_min']:.2f}, {rec['z_max']:.2f}] z_S, off {d:.2f}")
    return result("K6", not issues, _summ(issues) if issues else f"{n} z_rule(s) match drawn extents within {TOL_Z} mm; check_stack imports and anchors clean",
                  measured=round(worst, 4), threshold=TOL_Z, n_issues=len(issues), cause=_cause(absent, len(issues)))


# ======================================================================== K7 overlap between neighbours

def _feat(ctx, pose, fid):
    return ((ctx.stack or {}).get("poses", {}).get(pose, {}).get("features", {}).get(fid, {}) or {})


def _depth(ctx, pose, fid):
    return _feat(ctx, pose, fid).get("depth")


def _sep_band(ctx, pose, fid):
    """Band along the view direction: depth in side views, z band in plan (z_S; a relative gap is frame-free)."""
    f = _feat(ctx, pose, fid)
    if ctx.view in SIDE_VIEWS:
        return f.get("depth")
    if ctx.view == "plan_xy" and "z_min" in f:
        return [f["z_min"], f["z_max"]]
    return None


def _depth_separated(da, db):
    g = band_gap(da, db)
    return g is not None and g > 0


def _measurable(row):
    return not row.get("reference") and row.get("kind") not in NO_AREA_KINDS


def k7(ctx):
    rows_list = ctx.spec.get("features", [])
    rows = {r["id"]: r for r in rows_list}
    side = ctx.view in SIDE_VIEWS
    issues, states, tested, failing, absent = [], [], 0, 0, 0
    # TP-4 / LF-5: an explicit depth band must contain the placed part's true projection
    linted = set()
    for pose in ctx.figs:
        for fid, rec in ((ctx.stack or {}).get("poses", {}).get(pose, {}).get("features", {}) or {}).items():
            if fid in linted or "depth_spec" not in rec or "depth_true" not in rec:
                continue
            linted.add(fid)
            (lo, hi), (tlo, thi) = rec["depth_spec"], rec["depth_true"]
            if lo > tlo + TOL_C or hi < thi - TOL_C:
                issues.append(f"{fid}: spec depth band [{lo:.2f}, {hi:.2f}] does not contain the placed projection [{tlo:.2f}, {thi:.2f}]")
                failing += 1
    # TP1.1-3: two coaxial rows drawn in true section intersect in 3D exactly when their half-sections overlap, so a
    # nest between them is no nest; class N is refused between two `section` rows (declare C, G or F)
    for a, row in rows.items():
        for nb in row.get("neighbours") or []:
            b = nb["id"]
            if nb["class"] == "N" and row.get("section") and rows.get(b, {}).get("section"):
                issues.append(f"spec error: {a}|{b} class N between two section rows (declare C, G or F)")
                failing += 1
    for pose, fig in ctx.figs.items():
        ax = fig.axes[0]
        # FIX 3 (Loftsman 1.1 (b)): a neighbour with `poses` declares the pair at those poses only; at every other
        # pose the pair falls to the undeclared-F test below.
        declared = set()
        for a, row in rows.items():
            for nb in row.get("neighbours") or []:
                b = nb["id"]
                if nb.get("poses") and pose not in nb["poses"]:
                    continue
                declared.add(frozenset((a, b)))
                if not applies(row, pose) or b not in rows or not applies(rows[b], pose):
                    continue
                tag = f"{pose}/{a}|{b} {nb['class']}"
                PA, PB = pieces(ax, a), pieces(ax, b)
                gap = band_gap(_sep_band(ctx, pose, a), _sep_band(ctx, pose, b))
                if nb["class"] == "N":
                    states.append("N")
                    continue
                needs_draw = not (gap is not None and gap > 0 and nb["class"] in ("F", "G") and gap >= (nb.get("g_min") or 0) - TOL_C)
                if needs_draw and (not PA or not PB):
                    issues.append(f"{tag}: untestable, {'/'.join(x for x, p in ((a, PA), (b, PB)) if not p)} not drawn")
                    failing += 1
                    absent += 1
                    continue
                ok, st, txt, _ = assess_pair(nb["class"], nb.get("g_min"), PA, PB, gap, (a, b),
                                             plan_gap=plan_gap_fn(ctx, rows, pose, a, b) if side else None)
                tested += st not in ("depth-separated",)
                states.append(st)
                if not ok:
                    failing += 1
                    issues.append(f"{tag}: {txt}")
        # TP-5: every undeclared pair of drawn parts defaults to F
        if ctx.spec.get("undeclared_pairs", "F") == "F":
            ids = [r["id"] for r in rows_list if _measurable(r) and applies(r, pose)]
            drawn = {i: pieces(ax, i) for i in ids}
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    a, b = ids[i], ids[j]
                    if frozenset((a, b)) in declared or a == b or not drawn[a] or not drawn[b]:
                        continue
                    gap = band_gap(_sep_band(ctx, pose, a), _sep_band(ctx, pose, b))
                    ok, st, txt, _ = assess_pair("F", 0, drawn[a], drawn[b], gap, (a, b),
                                                 plan_gap=plan_gap_fn(ctx, rows, pose, a, b) if side else None)
                    states.append(f"undeclared:{st}")
                    if not ok:
                        failing += 1
                        issues.append(f"{pose}/{a}|{b} undeclared (F): {txt}")
    # swept case: per piece, hull of the piece at the lowest and the highest pose (LF-3)
    poses = list(ctx.figs)
    if len(poses) > 1 and ctx.stack:
        order = sorted(poses, key=lambda p: ctx.stack["poses"][p]["tip_z_S"])
        lo, hi = order[0], order[-1]
        for a, row in rows.items():
            if not row.get("moves"):
                continue
            for nb in row.get("neighbours") or []:
                b = nb["id"]
                if b not in rows or rows[b].get("moves") or nb["class"] in ("C", "N") or nb.get("poses"):
                    continue
                tag = f"swept {lo}..{hi}/{a}|{b} {nb['class']}"
                PL, PH = pieces(ctx.figs[lo].axes[0], a), pieces(ctx.figs[hi].axes[0], a)
                PB = pieces(ctx.figs[lo].axes[0], b)
                if side:
                    gap = band_gap(_depth(ctx, lo, a), _depth(ctx, lo, b))
                else:
                    za = [_sep_band(ctx, p, a) for p in poses]
                    zb = _sep_band(ctx, lo, b)
                    gap = band_gap([min(z[0] for z in za), max(z[1] for z in za)], zb) if all(za) and zb else None
                if not PL or not PH or not PB:
                    if gap is not None and gap > 0 and gap >= (nb.get("g_min") or 0) - TOL_C:
                        states.append("swept:depth-separated")
                        continue
                    issues.append(f"{tag}: untestable, not drawn")
                    failing += 1
                    absent += 1
                    continue
                if len(PL) != len(PH):
                    issues.append(f"{tag}: {len(PL)} pieces at {lo}, {len(PH)} at {hi}; swept hull needs matching pieces")
                    failing += 1
                    continue
                hulls = [convex_hull(list(p) + list(q)) for p, q in zip(PL, PH)]
                ok, st, txt, _ = assess_pair(nb["class"], nb.get("g_min"), hulls, PB, gap, (f"{a} swept", b),
                                             plan_gap=plan_gap_fn(ctx, rows, lo, a, b) if side else None)
                tested += st not in ("depth-separated",)
                states.append(f"swept:{st}")
                if not ok:
                    failing += 1
                    issues.append(f"{tag}: swept hull {txt}")
    return result("K7", not issues, _summ(issues) if issues else f"{tested} pair test(s) clean; states {sorted(set(states))}",
                  measured=failing, threshold=0, states=states, failing=failing, n_issues=len(issues), cause=_cause(absent, len(issues)))


# ======================================================================== K8 sense and orientation

def _key_index(P, expr):
    m = re.fullmatch(r"([\w.]+)(?:\[(\d+)\])?", str(expr).strip())
    v = P.get(m.group(1))
    return float(v[int(m.group(2))] if m.group(2) is not None else v)


def _width_at(poly, axis, level, tol=1e-6):
    """Extent along the other axis of the vertices lying at coordinate `level` on `axis` (0 = x, 1 = z)."""
    other = 1 - axis
    vals = [p[other] for p in poly if abs(p[axis] - level) <= tol]
    return (max(vals) - min(vals)) if vals else 0.0


def taper_issue(polys, narrows):
    """TP-2: per piece, narrows up/down compares the width at z_hi with the width at z_lo; inward/outward compares the
    height at the outer x end (farther from x = 0) with the inner end."""
    for k, poly in enumerate(polys):
        if narrows in ("up", "down"):
            zs = [p[1] for p in poly]
            w_lo, w_hi = _width_at(poly, 1, min(zs)), _width_at(poly, 1, max(zs))
            ok = w_hi < w_lo - TOL_Z if narrows == "up" else w_lo < w_hi - TOL_Z
            if not ok:
                return f"piece {k}: width at bottom {w_lo:.2f}, at top {w_hi:.2f}"
        elif narrows in ("inward", "outward"):
            xs = [p[0] for p in poly]
            x_out, x_in = (max(xs), min(xs)) if abs(max(xs)) >= abs(min(xs)) else (min(xs), max(xs))
            h_out, h_in = _width_at(poly, 0, x_out), _width_at(poly, 0, x_in)
            ok = h_in < h_out - TOL_Z if narrows == "inward" else h_out < h_in - TOL_Z
            if not ok:
                return f"piece {k}: height at inner end {h_in:.2f}, at outer end {h_out:.2f}"
        else:
            return f"unknown taper {narrows!r}"
    return None


def face_rises_issue(polys, toward):
    """TP1.1-1 (Designer TP-2 sign check (b)): per piece, the face edge leaves the lowest vertex a along the adjacent
    edge with the larger radial change, to b; outward requires (z_b - z_a)(|x_b| - |x_a|) > 0 (the tooth face rises
    with r, cone apex below), inward requires < 0."""
    for k, poly in enumerate(polys):
        n = len(poly)
        i = min(range(n), key=lambda j: (poly[j][1], -abs(poly[j][0])))
        a = poly[i]
        b = max((poly[(i - 1) % n], poly[(i + 1) % n]), key=lambda q: abs(abs(q[0]) - abs(a[0])))
        s = (b[1] - a[1]) * (abs(b[0]) - abs(a[0]))
        ok = s > 0 if toward == "outward" else s < 0 if toward == "inward" else None
        if ok is None:
            return f"unknown face_rises {toward!r}"
        if not ok:
            return (f"piece {k}: face from ({a[0]:.2f}, {a[1]:.2f}) to ({b[0]:.2f}, {b[1]:.2f}), "
                    f"dz {b[1] - a[1]:+.2f} over d|x| {abs(b[0]) - abs(a[0]):+.2f}")
    return None


def k8(ctx):
    rows_list = ctx.spec.get("features", [])
    rows = {r["id"]: r for r in rows_list}
    lint, bad = sense_lint(rows_list)
    issues, n, absent = list(lint), 0, 0
    side, plan = ctx.view in SIDE_VIEWS, ctx.view == "plan_xy"
    for pose, fig in ctx.figs.items():
        ax = fig.axes[0]
        n += 1
        if ax.xaxis_inverted() or ax.yaxis_inverted():
            issues.append(f"{pose}: axis inverted (x {ax.xaxis_inverted()}, y {ax.yaxis_inverted()})")
        for fid, row in rows.items():
            if not applies(row, pose):
                continue
            me = pieces(ax, fid)
            # TP-3: every placed row sits at its projected position (x = r_c cos theta in side views; x and y in plan)
            pl = _feat(ctx, pose, fid).get("place")
            if pl and (side or plan):
                if not me:
                    issues.append(f"{pose}/{fid} projected_x: untestable, {fid} not drawn")
                    absent += 1
                else:
                    n += 1
                    ex = extent_x(me)
                    cx = (ex[0] + ex[1]) / 2
                    want = pl["r_c"] * math.cos(math.radians(pl["theta"]))
                    if abs(cx - want) > TOL_Z:
                        issues.append(f"{pose}/{fid} projected_x: drawn x centre {cx:.2f} vs r_c cos(theta) {want:.2f} (r_c {pl['r_c']:.2f}, theta {pl['theta']:g})")
                    if plan:
                        ey = extent_z(me)
                        wy = pl["r_c"] * math.sin(math.radians(pl["theta"]))
                        if abs((ey[0] + ey[1]) / 2 - wy) > TOL_Z:
                            issues.append(f"{pose}/{fid} projected_y: drawn y centre {(ey[0] + ey[1]) / 2:.2f} vs r_c sin(theta) {wy:.2f}")
            for pr in row.get("sense") or []:
                if id(pr) in bad or (pr.get("poses") and pose not in pr["poses"]):
                    continue
                kind = pr["pred"]
                other_id = pr.get("of") or pr.get("seat") or pr.get("axis")
                other = pieces(ax, other_id) if other_id else None
                if not me or (other_id and not other):
                    issues.append(f"{pose}/{fid} {kind} {other_id or ''}: untestable, {fid if not me else other_id} not drawn")
                    absent += 1
                    continue
                n += 1
                if kind in ("below", "above"):
                    za, zb = centroid(me)[1], centroid(other)[1]
                    ok = za < zb if kind == "below" else za > zb
                    if not ok:
                        issues.append(f"{pose}/{fid} {kind} {other_id}: centroid z {za:.1f} vs {zb:.1f}")
                elif kind == "clears_above":
                    # TP-9 ring_on_tube (a): z_min(me) - z_max(of) > 0, me wholly above of
                    d = extent_z(me)[0] - extent_z(other)[1]
                    if d <= 0:
                        issues.append(f"{pose}/{fid} clears_above {other_id}: z_min minus {other_id} z_max {d:.2f}, needs > 0")
                elif kind == "top_within":
                    # TP-9 ring_on_tube (b), motor below the gear back face: z_max(of) - z_max(me) > 0
                    d = extent_z(other)[1] - extent_z(me)[1]
                    if d <= 0:
                        issues.append(f"{pose}/{fid} top_within {other_id}: {other_id} z_max minus z_max {d:.2f}, needs > 0")
                elif kind == "rests_on":
                    d = extent_z(me)[0] - extent_z(other)[1]
                    if abs(d) > pr.get("tol", TOL_Z):
                        issues.append(f"{pose}/{fid} rests_on {other_id}: bottom minus seat top {d:.3f} mm")
                elif kind == "mirror_about_axis":
                    x0 = centroid(other)[0]
                    pts = [p for poly in me for p in poly]
                    unmatched = [p for p in pts if not any(abs(2 * x0 - p[0] - q[0]) <= TOL_Z and abs(p[1] - q[1]) <= TOL_Z for q in pts)]
                    if unmatched or len(me) < 2:
                        issues.append(f"{pose}/{fid} not mirrored about x = {x0:.2f} ({len(unmatched)} unmatched vertices, {len(me)} pieces)")
                elif kind == "side":
                    d = centroid(me)[0] - centroid(other)[0]
                    if d * pr["sign"] <= 0:
                        issues.append(f"{pose}/{fid} side of {other_id}: centroid x minus {other_id} x {d:.2f}, spec sign {pr['sign']:+d}")
                elif kind == "outboard":
                    th = (pl or {}).get("theta")
                    if th is None or (side and abs(math.cos(math.radians(th))) < 1e-6):
                        issues.append(f"{pose}/{fid} outboard of {other_id}: spec error, no placed theta that shows in {ctx.view}")
                    else:
                        d = (centroid(me)[0] - centroid(other)[0]) * math.cos(math.radians(th))
                        if d <= 0:
                            issues.append(f"{pose}/{fid} outboard of {other_id}: (x - x_{other_id}) cos(theta) {d:.2f}, needs > 0")
                elif kind == "azimuth":
                    cx, cy = centroid(me)
                    got = math.degrees(math.atan2(cy, cx)) % 360
                    want = _key_index(ctx.P, pr["expr"]) % 360
                    d = abs((got - want + 180) % 360 - 180)
                    if d > pr.get("tol_deg", 0.1):
                        issues.append(f"{pose}/{fid} azimuth {got:.2f} deg vs {pr['expr']} = {want:.2f}")
                elif kind == "taper":
                    t = taper_issue(me, pr["narrows"])
                    if t:
                        issues.append(f"{pose}/{fid} taper narrows {pr['narrows']}: {t}")
                elif kind == "face_rises":
                    t = face_rises_issue(me, pr["toward"])
                    if t:
                        issues.append(f"{pose}/{fid} face_rises {pr['toward']}: {t}")
    return result("K8", not issues, _summ(issues) if issues else f"{n} predicate(s) hold, axes not inverted", measured=len(issues), threshold=0,
                  n_issues=len(issues), cause=_cause(absent, len(issues)))


# ======================================================================== K9 coverage

def k9(ctx):
    rows = ctx.spec.get("features", [])
    ids = {r["id"] for r in rows}
    kinds = {r["id"]: r.get("kind") for r in rows}
    issues = [f"spec error: id {d} appears on more than one row" for d in duplicate_ids(rows)]
    for pose, fig in ctx.figs.items():
        ax = fig.axes[0]
        gids = set(tagged(ax))
        text_gids = set()
        for t in ax.texts:
            g = t.get_gid()
            if not g or g.startswith("label:"):
                continue
            if kinds.get(g) == "callout":
                gids.add(g)
            else:
                text_gids.add(g)
        for r in rows:
            if applies(r, pose) and r["id"] not in gids:
                issues.append(f"{pose}: spec row {r['id']} has no patch" + (" (a Text carries its gid)" if r["id"] in text_gids else ""))
            # TP1.1-2: the half-space of the pose set; a row with `poses` has no artist at a pose outside it
            if not applies(r, pose) and (r["id"] in gids or r["id"] in text_gids):
                issues.append(f"{pose}: {r['id']} drawn at a pose outside its poses {r.get('poses')}")
        for g in sorted((gids | text_gids) - ids):
            issues.append(f"{pose}: tagged artist {g} has no spec row")
    return result("K9", not issues, _summ(issues) if issues else f"every spec row drawn, every tagged artist in the spec ({len(ids)} rows)",
                  measured=len(issues), threshold=0, n_issues=len(issues))


CHECKS = {"K1": k1, "K2": k2, "K3": k3, "K4": k4, "K5": k5, "K6": k6, "K7": k7, "K8": k8, "K9": k9}
