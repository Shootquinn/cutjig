"""Shared plot and check library for the Step 1 sketches (research/sean/gameplan.md detail 1.0).

- Loader: re-exported from sketch_loader (params.yaml, then the overlay, leaf merge).
- setup_figure(view): the only place figure size, dpi, aspect and grid are set.
- draw(feature_id, artist, ax): tags the artist with gid = feature_id and adds it.
- K1 to K9: each takes a Ctx and returns a result dict {id, result: pass|fail, reason, measured, threshold, ...}.
Geometry (K7) in plain Python: Sutherland-Hodgman convex clipping, convex polygon minimum distance, convex hull.
"""
import ast
import math
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_agg import FigureCanvasAgg  # noqa: E402
from matplotlib.collections import Collection  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle, Ellipse, Patch, Polygon, Rectangle  # noqa: E402
from matplotlib.text import Text  # noqa: E402

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from sketch_loader import LEGAL_STATUS, LEAF_FIELDS, Params, load_yaml, find_root  # noqa: E402,F401

TOL_Z = 0.05          # K6, K8 rests_on: mm in data coordinates
TOL_C = 0.05          # K7 contact distance, mm
TOL_AREA = 0.01       # K7 overlap area, mm^2
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


class Ctx:
    """What a check sees: params, spec (the feature table), figures per pose, check_stack values, file paths."""

    def __init__(self, P=None, spec=None, figs=None, stack=None, view=None, script_paths=None,
                 overlay_path=None, check_stack_path=None):
        self.P, self.spec, self.figs, self.stack = P, spec or {}, figs or {}, stack
        self.view = view or (spec or {}).get("view")
        self.script_paths = [Path(p) for p in (script_paths or [])]
        self.overlay_path = overlay_path
        self.check_stack_path = check_stack_path


def result(cid, ok, reason, measured=None, threshold=None, **extra):
    out = {"id": cid, "result": "pass" if ok else "fail", "reason": reason, "measured": measured, "threshold": threshold}
    out.update(extra)
    return out


def _summ(issues, n=6):
    s = "; ".join(issues[:n])
    return s + (f"; ... {len(issues) - n} more" if len(issues) > n else "")


# ======================================================================== figure and drawing helpers

def setup_figure(view, title=""):
    """Sole owner of figsize, dpi, aspect and grid (K3)."""
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


def draw_gear_section(ax, fid, r_in, r_pitch, z0, z1, **kw):
    """Bevel ring gear in side section: two trapezoids mirrored about x = 0, bore edge vertical, outer edge slanted."""
    kw.setdefault("fill", False)
    h = z1 - z0
    right = [(r_in, z0), (r_pitch + h / 2, z0), (r_pitch, z1), (r_in, z1)]
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
    """One annotation per spec row with a label, anchored at the right edge of the row's drawn pieces."""
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


def artist_polys(a):
    """Polygons in data coordinates (closing vertex dropped)."""
    if isinstance(a, Line2D):
        return [[(float(x), float(y)) for x, y in zip(a.get_xdata(), a.get_ydata())]]
    if isinstance(a, Patch):
        path = a.get_path().transformed(a.get_patch_transform())
        polys = path.to_polygons(closed_only=False) or [path.vertices]
        out = []
        for poly in polys:
            pts = [(float(x), float(y)) for x, y in poly]
            if len(pts) > 1 and abs(pts[0][0] - pts[-1][0]) < 1e-12 and abs(pts[0][1] - pts[-1][1]) < 1e-12:
                pts = pts[:-1]
            out.append(pts)
        return out
    if isinstance(a, Collection):
        return [[(float(x), float(y)) for x, y in p.vertices] for p in a.get_paths()]
    return []


def pieces(ax, gid):
    return [poly for a in tagged(ax).get(gid, []) for poly in artist_polys(a)]


def extent_z(polys):
    zs = [p[1] for poly in polys for p in poly]
    return (min(zs), max(zs)) if zs else None


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
    files = ", ".join(Path(p).name for p in ctx.script_paths)
    return result("K1", not issues, _summ(issues) if issues else f"no literal outside {sorted(K1_ALLOWED)}, no soft-key comparison, no figure setting ({files})",
                  measured=len(issues), threshold=0)


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
                  measured=len(issues), threshold=0)


# ======================================================================== K3 plot conventions

def _grid_on(axis, which):
    ticks = axis.get_major_ticks() if which == "major" else axis.get_minor_ticks()
    return bool(ticks) and any(t.gridline.get_visible() for t in ticks)


def k3(ctx):
    issues = []
    for name, fig in ctx.figs.items():
        ax = fig.axes[0]
        view = ctx.view
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
    return result("K3", not issues, _summ(issues) if issues else f"{len(ctx.figs)} figure(s): title, (mm) labels, equal aspect, grids, figsize, dpi {DPI}",
                  measured=len(issues), threshold=0)


# ======================================================================== K4 labels carry their dimension

def applies(row, pose):
    return not row.get("poses") or pose in row["poses"]


def k4(ctx):
    issues, n = [], 0
    for pose, fig in ctx.figs.items():
        texts = [t.get_text() for t in fig.axes[0].texts]
        for row in ctx.spec.get("features", []):
            if not row.get("label") or not applies(row, pose):
                continue
            n += 1
            lab = row["label"]
            want = format(ctx.P.get(lab["key"]), lab.get("fmt", ".1f"))
            cands = [t for t in texts if lab["text"] in t]
            if not cands:
                issues.append(f"{pose}/{row['id']}: no annotation containing {lab['text']!r}")
                continue
            nums = [m for t in cands for m in NUMBER.findall(t.replace(lab["text"], " "))]
            if not nums:
                issues.append(f"{pose}/{row['id']}: label {cands[0]!r} carries no number (want {want} from {lab['key']})")
            elif not any(abs(float(m) - float(want)) < 1e-9 for m in nums):
                issues.append(f"{pose}/{row['id']}: label {cands[0]!r} number differs from {lab['key']} = {want}")
    return result("K4", not issues, _summ(issues) if issues else f"{n} label(s) carry their key value", measured=len(issues), threshold=0)


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
    rows = {r["id"]: r for r in ctx.spec.get("features", [])}
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
            if want and got != want:
                issues.append(f"{pose}/{gid}: {row.get('kind')} axis {row.get('axis')} in {ctx.view} drawn as {got}, needs {want}")
            elif want is None and got == "circle" and normal == "Y" and row.get("kind") not in ("sphere",):
                issues.append(f"{pose}/{gid}: circle in side view for kind {row.get('kind')}")
            if want and row.get("projection") and row["projection"] != want:
                issues.append(f"{pose}/{gid}: spec projection {row['projection']} disagrees with {want}")
    return result("K5", not issues, _summ(issues) if issues else f"{n} tagged artist(s) projected per kind and axis (view normal {normal})",
                  measured=len(issues), threshold=0)


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


def k6(ctx):
    issues, worst, n = [], 0.0, 0
    if ctx.check_stack_path:
        issues += [f"import guard: {b}" for b in import_violations(ctx.check_stack_path)]
    for pose, fig in ctx.figs.items():
        feats = ctx.stack["poses"][pose]["features"]
        drawn = tagged(fig.axes[0])
        for fid, rec in feats.items():
            if "z_min" not in rec:
                continue
            n += 1
            if fid not in drawn:
                issues.append(f"{pose}/{fid}: z_rule [{rec['z_min']:.2f}, {rec['z_max']:.2f}] z_S, nothing drawn")
                continue
            ez = extent_z([p for a in drawn[fid] for p in artist_polys(a)])
            d = max(abs(ez[0] - rec["z_min"]), abs(ez[1] - rec["z_max"]))
            worst = max(worst, d)
            if d > TOL_Z:
                issues.append(f"{pose}/{fid}: drawn z [{ez[0]:.2f}, {ez[1]:.2f}] vs stack [{rec['z_min']:.2f}, {rec['z_max']:.2f}] z_S, off {d:.2f}")
    return result("K6", not issues, _summ(issues) if issues else f"{n} z_rule(s) match drawn extents within {TOL_Z} mm; check_stack imports clean",
                  measured=round(worst, 4), threshold=TOL_Z)


# ======================================================================== K7 overlap between neighbours

def _depth(ctx, pose, fid):
    return ((ctx.stack or {}).get("poses", {}).get(pose, {}).get("features", {}).get(fid, {}) or {}).get("depth")


def _depth_separated(da, db):
    return da is not None and db is not None and (da[1] < db[0] or db[1] < da[0])


def k7(ctx):
    rows = {r["id"]: r for r in ctx.spec.get("features", [])}
    side = ctx.view in SIDE_VIEWS
    issues, states, tested, failing = [], [], 0, 0
    for pose, fig in ctx.figs.items():
        ax = fig.axes[0]
        for a, row in rows.items():
            for nb in row.get("neighbours") or []:
                b = nb["id"]
                if nb.get("poses") and pose not in nb["poses"]:
                    continue
                if not applies(row, pose) or b not in rows or not applies(rows[b], pose):
                    continue
                tag = f"{pose}/{a}|{b} {nb['class']}"
                if side and _depth_separated(_depth(ctx, pose, a), _depth(ctx, pose, b)):
                    states.append("depth-separated")
                    continue
                PA, PB = pieces(ax, a), pieces(ax, b)
                if not PA or not PB:
                    issues.append(f"{tag}: untestable, {'/'.join(x for x, p in ((a, PA), (b, PB)) if not p)} not drawn")
                    failing += 1
                    continue
                nonconv = [x for x, PP in ((a, PA), (b, PB)) if any(not is_convex(p) for p in PP)]
                if nonconv:
                    issues.append(f"{tag}: non-convex piece in {nonconv}; split it in the spec")
                    failing += 1
                    continue
                dist, area = pair_measure(PA, PB)
                tested += 1
                st = pair_state(dist, area)
                states.append(st)
                if not judge(nb["class"], nb.get("g_min"), dist, area):
                    failing += 1
                    issues.append(f"{tag}: distance {dist:.3f} mm, overlap {area:.3f} mm2, state {st}, g_min {nb.get('g_min')}")
    # swept case
    poses = list(ctx.figs)
    if len(poses) > 1 and ctx.stack:
        order = sorted(poses, key=lambda p: ctx.stack["poses"][p]["tip_z_S"])
        lo, hi = order[0], order[-1]
        for a, row in rows.items():
            if not row.get("moves"):
                continue
            for nb in row.get("neighbours") or []:
                b = nb["id"]
                if b not in rows or rows[b].get("moves") or nb["class"] == "C" or nb.get("poses"):
                    continue
                tag = f"swept {lo}..{hi}/{a}|{b} {nb['class']}"
                if side and _depth_separated(_depth(ctx, lo, a), _depth(ctx, lo, b)):
                    states.append("depth-separated")
                    continue
                pts = [p for P_ in (pieces(ctx.figs[lo].axes[0], a), pieces(ctx.figs[hi].axes[0], a)) for poly in P_ for p in poly]
                PB = pieces(ctx.figs[lo].axes[0], b)
                if not pts or not PB:
                    issues.append(f"{tag}: untestable, not drawn")
                    failing += 1
                    continue
                if not side:
                    za = [ctx.stack["poses"][p]["features"].get(a, {}) for p in poses]
                    zb = ctx.stack["poses"][lo]["features"].get(b, {})
                    if za and zb and "z_min" in zb and all("z_min" in z for z in za):
                        if max(z["z_max"] for z in za) < zb["z_min"] or min(z["z_min"] for z in za) > zb["z_max"]:
                            continue
                hull = convex_hull(pts)
                dist, area = pair_measure([hull], PB)
                tested += 1
                st = pair_state(dist, area)
                states.append(f"swept:{st}")
                if not judge(nb["class"], nb.get("g_min"), dist, area):
                    failing += 1
                    issues.append(f"{tag}: swept hull distance {dist:.3f} mm, overlap {area:.3f} mm2, state {st}")
    return result("K7", not issues, _summ(issues) if issues else f"{tested} pair test(s) clean; states {sorted(set(states))}",
                  measured=failing, threshold=0, states=states, failing=failing)


# ======================================================================== K8 sense and orientation

def _key_index(P, expr):
    m = re.fullmatch(r"([\w.]+)(?:\[(\d+)\])?", str(expr).strip())
    v = P.get(m.group(1))
    return float(v[int(m.group(2))] if m.group(2) is not None else v)


def k8(ctx):
    rows = {r["id"]: r for r in ctx.spec.get("features", [])}
    issues, n = [], 0
    for pose, fig in ctx.figs.items():
        ax = fig.axes[0]
        n += 1
        if ax.xaxis_inverted() or ax.yaxis_inverted():
            issues.append(f"{pose}: axis inverted (x {ax.xaxis_inverted()}, y {ax.yaxis_inverted()})")
        for fid, row in rows.items():
            if not applies(row, pose):
                continue
            for pr in row.get("sense") or []:
                kind = pr["pred"]
                me = pieces(ax, fid)
                other_id = pr.get("of") or pr.get("on") or pr.get("axis")
                other = pieces(ax, other_id) if other_id else None
                if not me or (other_id and not other):
                    issues.append(f"{pose}/{fid} {kind} {other_id or ''}: untestable, {fid if not me else other_id} not drawn")
                    continue
                n += 1
                if kind in ("below", "above"):
                    za, zb = centroid(me)[1], centroid(other)[1]
                    ok = za < zb if kind == "below" else za > zb
                    if not ok:
                        issues.append(f"{pose}/{fid} {kind} {other_id}: centroid z {za:.1f} vs {zb:.1f}")
                elif kind == "rests_on":
                    d = extent_z(me)[0] - extent_z(other)[1]
                    if abs(d) > pr.get("tol", TOL_Z):
                        issues.append(f"{pose}/{fid} rests_on {other_id}: bottom minus seat top {d:.3f} mm")
                elif kind == "mirror_about_axis":
                    x0 = centroid(other)[0]
                    pts = [p for poly in me for p in poly]
                    bad = [p for p in pts if not any(abs(2 * x0 - p[0] - q[0]) <= TOL_Z and abs(p[1] - q[1]) <= TOL_Z for q in pts)]
                    if bad or len(me) < 2:
                        issues.append(f"{pose}/{fid} not mirrored about x = {x0:.2f} ({len(bad)} unmatched vertices, {len(me)} pieces)")
                elif kind == "azimuth":
                    cx, cy = centroid(me)
                    got = math.degrees(math.atan2(cy, cx)) % 360
                    want = _key_index(ctx.P, pr["expr"]) % 360
                    d = abs((got - want + 180) % 360 - 180)
                    if d > pr.get("tol_deg", 0.1):
                        issues.append(f"{pose}/{fid} azimuth {got:.2f} deg vs {pr['expr']} = {want:.2f}")
                else:
                    issues.append(f"{pose}/{fid}: unknown predicate {kind}")
    return result("K8", not issues, _summ(issues) if issues else f"{n} predicate(s) hold, axes not inverted", measured=len(issues), threshold=0)


# ======================================================================== K9 coverage

def k9(ctx):
    rows = ctx.spec.get("features", [])
    ids = {r["id"] for r in rows}
    issues = []
    for pose, fig in ctx.figs.items():
        ax = fig.axes[0]
        gids = set(tagged(ax))
        gids |= {t.get_gid() for t in ax.texts if t.get_gid() and not t.get_gid().startswith("label:")}
        for r in rows:
            if applies(r, pose) and r["id"] not in gids:
                issues.append(f"{pose}: spec row {r['id']} has no patch")
        for g in sorted(gids - ids):
            issues.append(f"{pose}: tagged artist {g} has no spec row")
    return result("K9", not issues, _summ(issues) if issues else f"every spec row drawn, every tagged artist in the spec ({len(ids)} rows)",
                  measured=len(issues), threshold=0)


CHECKS = {"K1": k1, "K2": k2, "K3": k3, "K4": k4, "K5": k5, "K6": k6, "K7": k7, "K8": k8, "K9": k9}
