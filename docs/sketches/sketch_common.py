"""Shared plot and check library for the Step 1 sketches (contributor gameplan (sean) detail 1.0).

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
from matplotlib.collections import Collection, LineCollection  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Annulus, Circle, Ellipse, Patch, Polygon, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
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


def label_text(row, P, rec=None):
    """Label text: text + key value [+ suffix]. Label field z_S: true (a z_A height key) writes
    '<text> z_S <key + jig.datum_a_above_floor> (<key> <value> z_A)'. Field z_edge: z_min | z_max appends the row's
    stack edge in z_S at this pose (rec = check_stack feature record), e.g. the cutter tip (r3, Designer M1 F4)."""
    lab = row["label"]
    if "label_text_override" in row:
        return row["label_text_override"]
    fmt = lab.get("fmt", ".1f")
    v = P.get(lab["key"])
    if lab.get("z_S"):
        txt = f"{lab['text']} z_S {format(v + P.get('jig.datum_a_above_floor'), fmt)} ({lab['key']} {format(v, fmt)} z_A)"
    else:
        txt = f"{lab['text']} {format(v, fmt)}"
    txt += f" {lab['suffix']}" if lab.get("suffix") else ""
    edge = lab.get("z_edge")
    if edge and rec and edge in rec:
        txt += f"; {lab.get('z_edge_text', edge)} z_S {rec[edge]:.2f}"
    return txt


LABEL_FONTSIZE = 7
LABEL_LINESPACING = 1.2
LABEL_GAP_LINES = 0.5      # free space between stacked label boxes, in text lines (Designer M1 r2 F4)
LEADER_ZORDER = 100        # r3 (Designer M1 S2 r2 F1, S1 r6 F1): labels and leaders above every drawn area
ANCHOR_SAMPLES = 24        # r3: points per ink segment searched for an anchor no other area covers


def ink_pieces(ax, gid):
    """Drawn pieces of a row as (points, closed): a Patch is a closed outline, a Line2D or a Collection path an open
    polyline (1.2 (h), Designer M1 r1 F4: a leader ends on ink)."""
    out = []
    for a in tagged(ax).get(gid, []):
        closed = isinstance(a, Patch)
        out += [(poly, closed) for poly in artist_polys(a)]
    return out


def ink_distance(p, ink):
    """Distance from p to the nearest ink of a row (0 inside a closed outline)."""
    best = None
    for poly, closed in ink:
        if closed and len(poly) >= 3 and _inside(p, poly):
            return 0.0
        segs = _edges(poly) if closed else ([(poly[i], poly[i + 1]) for i in range(len(poly) - 1)] or [(poly[0], poly[0])])
        d = min(_pt_seg(p, a, b) for a, b in segs)
        best = d if best is None else min(best, d)
    return float("inf") if best is None else best


def _ray_hit(ink, theta):
    """Farthest point of a row's ink on the ray from the drill axis at theta (deg); None when the ray misses."""
    c, s = math.cos(math.radians(theta)), math.sin(math.radians(theta))
    best = None
    for poly, closed in ink:
        segs = _edges(poly) if closed else [(poly[i], poly[i + 1]) for i in range(len(poly) - 1)]
        for a, b in segs:
            ex, ey = b[0] - a[0], b[1] - a[1]
            den = c * ey - s * ex
            if abs(den) < 1e-12:
                continue
            t = (a[0] * ey - a[1] * ex) / den        # distance along the ray
            u = (a[0] * s - a[1] * c) / den          # position along the edge
            if t >= 0 and -1e-9 <= u <= 1 + 1e-9 and (best is None or t > best):
                best = t
    return None if best is None else (best * c, best * s)


def _rank(ax):
    """Draw order of the axes' artists: (zorder, index among the children); greater draws later (on top)."""
    kids = ax.get_children()
    return {id(a): (a.get_zorder(), i) for i, a in enumerate(kids)}


PHANTOM = (0, (12, 3, 3, 3, 3, 3))   # 1.3 P1Rf (Designer FIX D3): phantom line (long dash, two short) for plan stand-ins
STAND_IN_COLOR = "#8c510a"           # 1.3 P1Rf (Designer FIX D3): dark brown, apart from hidden black and rim blue
OPAQUE_ALPHA = 0.75     # 1.3 P1R (TP1.2-19): a fill whose rendered alpha is at least this hides what is under it
TRANSLUCENT_MAX = 0.5   # 1.3 P1R premise of the alpha rule: a fill counted see-through renders at alpha at most this


def fill_alpha(a):
    """Rendered alpha of a Patch's fill (0 for no fill). matplotlib folds a set artist alpha into the face colour (and
    forces it on the fill at draw time), so the face colour's alpha is the rendered one."""
    if not isinstance(a, Patch) or not a.get_fill():
        return 0.0
    fc = a.get_facecolor()
    return 0.0 if fc is None else float(fc[3])


def is_opaque(a):
    """A Patch whose fill hides what is under it (1.3 P1R alpha rule, TP1.2-19): filled with a rendered alpha of at least
    OPAQUE_ALPHA (0.75: what lies under shows at a quarter of its contrast or less). Premise, K8 cover opacity lint: no
    plan fill renders at an alpha between TRANSLUCENT_MAX and OPAQUE_ALPHA, so every fill is either opaque or shows what
    is under it at half its contrast or more."""
    return fill_alpha(a) >= OPAQUE_ALPHA - 1e-9


def is_area(a):
    """A drawn area that hides what is under it: a Patch with a visible fill or a hatch."""
    if not isinstance(a, Patch):
        return False
    fc = a.get_facecolor()
    return (bool(a.get_fill()) and fc is not None and fc[3] > 0) or bool(a.get_hatch())


def in_rings(p, polys):
    """p inside a patch's closed rings by the even-odd rule (an Annulus's bore is outside; a one-ring patch as _inside)."""
    return sum(1 for q in polys if len(q) >= 3 and _inside(p, q)) % 2 == 1


def in_drawn(a, p, polys=None):
    """p inside the area artist a as drawn: inside its rings (even-odd) and inside its clip region (1.3 P1R renderer:
    a split piece draws only inside its clip path; an artist with no clip path of its own draws everywhere)."""
    polys = polys if polys is not None else artist_polys(a)
    if not in_rings(p, polys):
        return False
    reg = drawn_region(a)
    return reg is None or reg.contains(p)


def covering_areas(ax, fid, p, rank=None):
    """gids of area artists of other rows that contain p and draw above every artist of row fid that carries ink at p.
    1.3 P1R: containment as drawn (even-odd rings, clip region of a renderer piece)."""
    rank = rank or _rank(ax)
    mine = [a for a in tagged(ax).get(fid, []) if ink_distance(p, [(q, isinstance(a, Patch)) for q in artist_polys(a)]) <= TOL_Z]
    top = max((rank[id(a)] for a in mine), default=(-1e9, -1))
    out = []
    for a in artists(ax):
        g = a.get_gid()
        if not g or g == fid or g.startswith(fid + ":") or not is_area(a) or rank[id(a)] <= top:
            continue
        if in_drawn(a, p):
            out.append(g)
    return out


def hatch_areas(ax):
    """(gid, closed pieces, artist) of every hatched Patch with a gid: dense ink a thin leader disappears into (Designer
    M1 S1 r6 F1). The artist is kept so containment reads the piece as drawn (1.3 P1R clip regions)."""
    return [(a.get_gid(), [q for q in artist_polys(a) if len(q) >= 3], a) for a in artists(ax)
            if a.get_gid() and isinstance(a, Patch) and a.get_hatch()]


LEADER_END = 0.25        # r3: the end quarter of a leader, next to its anchor
LEADER_HATCH_MAX = 0.25  # r3: at most this share of the end samples may lie in other rows' hatch (a thread strip passes)


def leader_hatch(fid, p0, p1, hatches):
    """gids of other rows' hatched areas the end of a leader (text p0, anchor p1) runs in, when more than
    LEADER_HATCH_MAX of the samples over its last LEADER_END (next to the anchor) lie in such hatch (Designer M1 S1 r6
    F1: a leader whose end runs through hatch is lost); empty otherwise."""
    k0 = int(ANCHOR_SAMPLES * (1 - LEADER_END))
    ks = list(range(k0, ANCHOR_SAMPLES))
    hit, gids = 0, set()
    for k in ks:
        q = (p0[0] + (p1[0] - p0[0]) * k / ANCHOR_SAMPLES, p0[1] + (p1[1] - p0[1]) * k / ANCHOR_SAMPLES)
        inq = {h[0] for h in hatches if h[0] != fid and not h[0].startswith(fid + ":") and
               (in_drawn(h[2], q, h[1]) if len(h) > 2 else any(_inside(q, pp) for pp in h[1]))}
        if inq:
            hit += 1
            gids |= inq
    return gids if hit > LEADER_HATCH_MAX * len(ks) else set()


def _reanchor(ax, fid, anc, text_xy, hatches, rank, left=False):
    """r3: an anchor on the row's ink, nearest the first choice, whose leader from text_xy crosses no other row's hatch
    and that no other row's area covers; the first choice when none exists."""
    ink = ink_pieces(ax, fid)
    cands = []
    for poly, closed in ink:
        segs = _edges(poly) if closed else [(poly[i], poly[i + 1]) for i in range(len(poly) - 1)]
        for a, b in segs:
            cands += [(a[0] + (b[0] - a[0]) * k / ANCHOR_SAMPLES, a[1] + (b[1] - a[1]) * k / ANCHOR_SAMPLES) for k in range(ANCHOR_SAMPLES + 1)]
    if left:   # r4: a left-column label searches from the left edge of its ink
        x_min = min(q[0] for q in cands)
        cands.sort(key=lambda q: (q[0] > x_min + TOL_Z, math.hypot(q[0] - x_min, q[1] - anc[1])))
    else:
        cands.sort(key=lambda q: (q[0] < anc[0] - TOL_Z, math.hypot(q[0] - anc[0], q[1] - anc[1])))   # same edge first
    for c in cands:
        if not leader_hatch(fid, text_xy, c, hatches) and not covering_areas(ax, fid, c, rank):
            return c
    return anc


def label_anchor(ax, row):
    """Leader end of a row's label, on the row's ink (1.2 (h), Designer M1 r1 F4 and F5). A row with label_theta (deg,
    spec field; concentric circles) anchors where the ray from the drill axis at that azimuth leaves its ink. Otherwise
    (max x, mid y) of the drawn pieces when that point is on the ink (a rectangle's or circle's right edge), else the
    drawn vertex of greatest x (nearest mid y among equals): the observer end of a slanted line, the corner of a wedge."""
    ink = ink_pieces(ax, row["id"])
    if not ink:
        return None
    if row.get("label_theta") is not None:
        hit = _ray_hit(ink, float(row["label_theta"]))
        if hit is not None:
            return hit
    pts = [p for poly, _ in ink for p in poly]
    xm = max(p[0] for p in pts)
    ym = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
    if ink_distance((xm, ym), ink) <= TOL_Z:
        first = (xm, ym)
    else:
        cand = [p for p in pts if p[0] >= xm - TOL_Z]
        first = min(cand, key=lambda p: abs(p[1] - ym))
    rank = _rank(ax)
    if not covering_areas(ax, row["id"], first, rank):
        return first
    # r3 (Designer M1 S1 r6 F1): the anchor lies on ink no other row's area covers; search the ink edges, greatest x
    # first, then nearest the first choice
    cands = []
    for poly, closed in ink:
        segs = _edges(poly) if closed else [(poly[i], poly[i + 1]) for i in range(len(poly) - 1)]
        for a, b in segs:
            cands += [(a[0] + (b[0] - a[0]) * k / ANCHOR_SAMPLES, a[1] + (b[1] - a[1]) * k / ANCHOR_SAMPLES) for k in range(ANCHOR_SAMPLES + 1)]
    cands.sort(key=lambda p: (-round(p[0], 3), math.hypot(p[0] - first[0], p[1] - first[1])))
    for c in cands:
        if not covering_areas(ax, row["id"], c, rank):
            return c
    return first


def _stack_z(wants, hs, zlo, zhi, gap):
    """Text z for a column of labels in descending anchor z: each as near its anchor as the boxes above allow, lifted from
    the bottom if the stack runs below the axes (the right-column rule, place_labels)."""
    zs = []
    for i, (want, h) in enumerate(zip(wants, hs)):
        zs.append(min(want, zhi - h / 2) if i == 0 else min(want, zs[-1] - hs[i - 1] / 2 - gap - h / 2))
    for i in range(len(zs) - 1, -1, -1):
        floor_z = zlo + hs[i] / 2 if i == len(zs) - 1 else zs[i + 1] + hs[i + 1] / 2 + gap + hs[i] / 2
        zs[i] = max(zs[i], floor_z)
    return zs


def place_labels(ax, spec, P, pose=None, margin=False, stack_pose=None, notes=()):
    """One annotation per spec row with a label, gid label:<id>, anchored at the right edge of the row's drawn pieces.
    margin=True (S1 r3, Designer M1 r2 F4): every label and every note goes into one column right of the axes, each
    with a leader to its anchor, stacked in anchor-z order with LABEL_GAP_LINES of free space between text boxes.
    Call after finish_axes (the column reads the final limits). notes: (anchor (x, z) or None, text[, gid]) tuples;
    a note without a gid is untagged (the figure note carries gid note:figure_note, Designer 1.2 (c) FIX R1)."""
    items, left_ids = [], set()
    for row in spec.get("features", []):
        if not row.get("label") or (pose and row.get("poses") and pose not in row["poses"]):
            continue
        anc = label_anchor(ax, row)
        if anc is None:
            continue
        rec = (stack_pose or {}).get(row["id"])
        items.append((anc, label_text(row, P, rec), f"label:{row['id']}"))
        if row.get("label_side") == "left":
            left_ids.add(f"label:{row['id']}")
    if not margin:
        for (x, z), txt, gid in items:
            ann = ax.annotate(txt, xy=(x, z), xytext=(x + 60, z + 20), fontsize=LABEL_FONTSIZE,
                              arrowprops={"arrowstyle": "-", "linewidth": 0.5}, zorder=LEADER_ZORDER)
            ann.set_gid(gid)
        return
    items += [(n[0], n[1], n[2] if len(n) > 2 else None) for n in notes if n[0]]
    free = [(n[1], n[2] if len(n) > 2 else None) for n in notes if not n[0]]
    ax.apply_aspect()
    (_, y0), (_, y1) = ax.transData.transform([(0, 0), (0, 1)])
    line = LABEL_FONTSIZE * ax.figure.dpi / 72 * LABEL_LINESPACING / abs(y1 - y0)   # one text line in data z
    gap = line * LABEL_GAP_LINES
    zlo, zhi = ax.get_ylim()
    x_col = ax.get_xlim()[1] + line
    hatches, rank = hatch_areas(ax), _rank(ax)
    x_left = ax.get_xlim()[0] - line
    for i, (anc, txt, gid) in enumerate(items):   # r3 (Designer M1 S1 r6 F1): the end of a leader clear of other hatch
        fid = gid[len("label:"):] if gid and gid.startswith("label:") else None
        tx = x_left if gid in left_ids else x_col
        if anc and fid and leader_hatch(fid, (tx, anc[1]), anc, hatches):
            items[i] = (_reanchor(ax, fid, anc, (tx, anc[1]), hatches, rank, left=gid in left_ids), txt, gid)
    left = sorted([it for it in items if it[2] in left_ids], key=lambda it: -it[0][1])   # r4: label_side left
    items = [it for it in items if it[2] not in left_ids]
    for it, z in zip(left, _stack_z([it[0][1] for it in left], [line * (it[1].count("\n") + 1) for it in left], zlo, zhi, gap)):
        ann = ax.annotate(it[1], xy=it[0], xytext=(x_left, z), fontsize=LABEL_FONTSIZE, ha="right", va="center",
                          zorder=LEADER_ZORDER, annotation_clip=False, arrowprops={"arrowstyle": "-", "linewidth": 0.4, "color": "0.35"})
        ann.set_gid(it[2])
    order = sorted(items, key=lambda it: -it[0][1])
    hs = [line * (it[1].count("\n") + 1) for it in order]
    zs = []
    for i, (it, h) in enumerate(zip(order, hs)):
        want = it[0][1]
        z = min(want, zhi - h / 2) if i == 0 else min(want, zs[-1] - hs[i - 1] / 2 - gap - h / 2)
        zs.append(z)
    for i in range(len(zs) - 1, -1, -1):        # lift from the bottom if the stack runs below the axes
        floor_z = zlo + hs[i] / 2 if i == len(zs) - 1 else zs[i + 1] + hs[i + 1] / 2 + gap + hs[i] / 2
        zs[i] = max(zs[i], floor_z)
    # notes without an anchor: same column, below the axes bottom, so no leader crosses them
    z = zlo - gap
    for txt, gid in free:
        h = line * (txt.count("\n") + 1)
        order.append((None, txt, gid))
        zs.append(z - h / 2)
        z -= h + gap
    for (anc, txt, gid), z in zip(order, zs):
        if anc:
            ann = ax.annotate(txt, xy=anc, xytext=(x_col, z), fontsize=LABEL_FONTSIZE, ha="left", va="center", zorder=LEADER_ZORDER,
                              annotation_clip=False, arrowprops={"arrowstyle": "-", "linewidth": 0.4, "color": "0.35"})
        else:
            ann = ax.annotate(txt, xy=(x_col, z), fontsize=LABEL_FONTSIZE, ha="left", va="center", annotation_clip=False)
        if gid:
            ann.set_gid(gid)


# ------------------------------------------------------------------------ plan leader placer (1.3 P1R R3)
# One function, place_plan_labels, places every label of a plan figure. Each label's candidates, in this order: label
# column (the row's label_side first, right when unset, then the other column) x anchor (the ray hit at label_theta when
# the row sets it and the ray meets its ink; then the column's default anchor: (max x, mid y) of the ink for the right
# column, (min x, mid y) for the left, or the extreme vertex nearest mid y when that point is off the ink; then every
# ink sample, at most ANCHOR_STEP apart along each ink edge, the column edge first and then by distance from the
# default anchor).
# A candidate passes when its leader passes every K4 leader rule: ends on the row's ink within TOL_Z; the anchor under
# no area of another row drawn above the row's ink there; no area drawn above the leader; at most LEADER_HATCH_MAX of
# its end-quarter samples in other rows' hatch; its last quarter outside every other row's true plan outline that does
# not contain the anchor (leader_outline_issue, Design Notes 30); and no crossing with another leader. Text inside the
# saved image is K3's rule (a margin column is inside the tight bounding box the script saves; K3 reads the premise);
# a left-column text box must also not overlap a y tick label (placer rule, margin mode).
# Labels are taken in spec row order: each takes its first candidate that passes at its wanted text position (column
# x, anchor y); the columns are then stacked (_stack_z) and every leader is re-judged at its stacked position; a label
# that fails there takes, in candidate order, the first candidate whose stacked layout gives it no failure and adds no
# failure to another label (at most PLACER_PASSES rounds). A label with no passing candidate is UNPLACEABLE: drawn at
# its first candidate, recorded with its candidate table on the axes (ax._sc_placer), and K4 fails it with reason
# "unplaceable". No silent fall-back.

LEADER_OUTLINE_STEP = 0.5   # mm: sample step along a leader's last quarter for the outline rule
ANCHOR_STEP = 2.0           # mm: placer anchor candidates along each ink edge, at most this far apart (edge ends included)
PLACER_PASSES = 3


def leader_outlines(ctx, pose):
    """What the K4 outline rule reads at pose: cover_table's true outlines {id: (outline, box)} and z_max per row (every
    row with a stack record, labelled reference rows included)."""
    if ctx is None or ctx.stack is None or ctx.view != "plan_xy":
        return {}, {}
    outl = cover_table(ctx, pose)[2]
    zmax = {r["id"]: _feat(ctx, pose, r["id"]).get("z_max") for r in ctx.spec.get("features", [])}
    return outl, zmax


def leader_outline_issue(outl, fid, p0, p1, zmax=None):
    """1.3 P1R K4 rule (Design Notes 30): [(row id, mm)] of the true plan outlines of rows nearer the viewer than row fid
    that the last LEADER_END of its leader (text p0, anchor p1) runs inside, with the length inside (samples at most
    LEADER_OUTLINE_STEP apart, the anchor end excluded); empty when none. Premises: (1) the anchor lies on the row's ink
    (K4 (a)); (2) an outline counts when its row's z_max is higher than fid's z_max by more than TOL_Z (seen from +Z
    the end of the leader then runs over a nearer part, as the descent-stop leader runs over tie b; a lower part, the
    plate, the base frame, a ring under a gear, lies behind the labelled part and every leader crosses it); a row with
    no z_max (a zone) counts every outline; (3) 1.3 P1Rf (Designer FIX D1): an outline that encloses the anchor (outline_
    encloses: its outer boundary with holes filled contains the anchor within TOL_Z; containing implies enclosing) is
    exempt, since no straight leader from outside reaches that anchor without crossing it. A row with visible ink anchors
    on visible ink (rule (e1), anchor_visibility_issue), so for such a row a containing outline cannot occur at the anchor;
    a wholly hidden row (e2) ends inside its cover, and its label names the cover (clause (g), cover_name_issue).
    outl: cover_table's {id: (outline, box)}; zmax: {id: z_max} (None: every outline counts)."""
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    Lq = L * LEADER_END
    n = max(int(ANCHOR_SAMPLES * LEADER_END), int(math.ceil(Lq / LEADER_OUTLINE_STEP)))
    ts = [1 - LEADER_END + LEADER_END * k / n for k in range(n)]
    pts = [(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t) for t in ts]
    sx0, sx1 = min(p[0] for p in pts), max(p[0] for p in pts)
    sy0, sy1 = min(p[1] for p in pts), max(p[1] for p in pts)
    zf = (zmax or {}).get(fid)
    out = []
    for oid, (O, (x0, x1, y0, y1)) in sorted(outl.items()):
        if oid == fid or oid.startswith(fid + ":") or x0 > sx1 or x1 < sx0 or y0 > sy1 or y1 < sy0:
            continue
        zo = (zmax or {}).get(oid)
        if zf is not None and (zo is None or zo <= zf + TOL_Z):
            continue
        if outline_encloses(O, p1):
            continue
        if O[0] == "annulus":
            k = sum(1 for q in pts if outline_contains(O, q))
        else:
            rings = [ccw(q) for q in O[1] if len(q) >= 3]
            k = sum(1 for q in pts if any(_inside_c(q, C) for C in rings))
        if k:
            out.append((oid, Lq * k / n))
    return out


def outline_encloses(O, p):
    """1.3 P1Rf (Designer FIX D1): p lies inside the outer boundary of plan outline O with its holes filled, within TOL_Z.
    Annulus (a, b): r <= b (the bore is a hole, filled). Polys: p inside or within TOL_Z of a convex piece (a piece has
    no hole; premise: no counted row's pieces ring round a hole, true for every S2 row)."""
    if O[0] == "annulus":
        return math.hypot(*p) <= O[1][1] + TOL_Z
    return outline_outside(O, p) <= TOL_Z


def counted_outlines(outl, zmax, fid):
    """Rows whose true outlines rule (e) counts for row fid: z_max higher than fid's by more than TOL_Z (fid without
    z_max: every other row)."""
    zf = (zmax or {}).get(fid)
    out = {}
    for oid, v in outl.items():
        if oid == fid or oid.startswith(fid + ":"):
            continue
        zo = (zmax or {}).get(oid)
        if zf is None or (zo is not None and zo > zf + TOL_Z):
            out[oid] = v
    return out


def row_visibility(ctx, ax, pose):
    """{row id: (wholly hidden, [solid artists with their covers])} for every measurable row with an area artist, from the
    renderer split as K8 cover certifies it (plan_cover_states on drawn samples). A row is wholly hidden when every area
    artist of it reads 'hidden'. Rows absent from the map (lines, zones, reference rows) have visible ink. The ink of a
    plan_style stand_in row (drawn in its own convention line, out of the renderer) counts as visible ink."""
    cc = cover_context(ctx, ax, pose)
    states = plan_cover_states(ctx, ax, pose)
    stand_in = {r["id"] for r in ctx.spec.get("features", []) if r.get("plan_style") == "stand_in"}
    out = {}
    for a, (fid, st, by, op) in states.items():
        hid, sol = out.get(fid, (True, []))
        if st != "hidden":
            hid = False
        if is_solid(a) or fid in stand_in:   # a stand-in's convention line is its visible ink (K8 cover exempts it)
            sol = sol + [(a, [q for q in artist_polys(a) if len(q) >= 3], artist_covers(cc, a, fid))]
        out[fid] = (hid, sol)
    return out


def anchor_visibility_issue(vis, fid, p):
    """Rule (e1) (Designer FIX D1): a row with visible ink anchors on visible ink: p within TOL_Z of the ink of a solid
    artist of the row, inside its drawn region, under no cover of that artist. None when the rule holds or the row is
    wholly hidden or has no area artist."""
    if fid not in vis or vis[fid][0]:
        return None
    for a, polys, covers in vis[fid][1]:
        if ink_distance(p, [(q, True) for q in polys]) > TOL_Z:
            continue
        reg = drawn_region(a)
        if reg is not None and not reg.contains(p):
            continue
        if cover_hits([p], covers)[0][0] is None:
            return None
    return f"label anchor ({p[0]:.2f}, {p[1]:.2f}) on hidden ink of a row with visible ink (e1)"


def cover_name_issue(ctx, vis, outl, zmax, fid, p, text):
    """Clause (g) (Designer FIX D1): the drawn label of a wholly hidden row contains 'under ' followed by the spec name of
    a counted row whose true outline contains or encloses the anchor. None when it holds or the row is not wholly
    hidden."""
    if fid not in vis or not vis[fid][0]:
        return None
    names = {r["id"]: r.get("name", r["id"]) for r in ctx.spec.get("features", [])}
    cov = sorted(oid for oid, (O, box) in counted_outlines(outl, zmax, fid).items() if outline_encloses(O, p))
    if any(f"under {names[o]}" in text for o in cov):
        return None
    return (f"label of a wholly hidden row lacks 'under <cover>' (g); covers at the anchor: "
            f"{', '.join(names[o] for o in cov) or 'none'}")


def _inside_c(p, C):
    """_inside on a ring already in counter-clockwise order (ccw(P))."""
    n = len(C)
    return all((C[(i + 1) % n][0] - C[i][0]) * (p[1] - C[i][1]) - (C[(i + 1) % n][1] - C[i][1]) * (p[0] - C[i][0]) >= -1e-12
               for i in range(n))


class _AreaInfo:
    """An area artist with its rings in ccw order and bounding box, for fast as-drawn containment (in_drawn semantics)."""

    def __init__(self, a, polys):
        self.a, self.gid = a, a.get_gid()
        self.rings = [ccw(q) for q in polys if len(q) >= 3]
        self.box = bbox(self.rings) if self.rings else (1, 0, 1, 0)

    def contains(self, p):
        x0, x1, y0, y1 = self.box
        if not (x0 - 1e-9 <= p[0] <= x1 + 1e-9 and y0 - 1e-9 <= p[1] <= y1 + 1e-9):
            return False
        if sum(1 for C in self.rings if _inside_c(p, C)) % 2 != 1:
            return False
        reg = drawn_region(self.a)
        return reg is None or reg.contains(p)


class _LeaderCtx:
    """What the leader rules read from a figure, cached for the placer: draw order, area artists with their rings, hatch,
    ink per row, true outlines at the pose, and the draw rank a label annotation gets. Same rules as leader_issues."""

    def __init__(self, ax, outl, zmax=None, vis=None):
        self.ax, self.outl, self.zmax, self.vis = ax, outl, zmax, vis or {}
        self.rank = _rank(ax)
        self.polys = {id(a): [q for q in artist_polys(a)] for a in artists(ax)}
        self.areas = [_AreaInfo(a, self.polys[id(a)]) for a in artists(ax) if a.get_gid() and is_area(a)]
        self.hatch = [h for h in self.areas if h.a.get_hatch()]
        self.lz = (LEADER_ZORDER, len(ax.get_children()))
        self.by_gid = tagged(ax)

        self._segs = {}

    def ink(self, fid):
        return [(q, isinstance(a, Patch)) for a in self.by_gid.get(fid, []) for q in self.polys[id(a)]]

    def _art_dist(self, a, p):
        """ink_distance from p to one artist's ink (0 inside a closed piece), vectorised over its edges."""
        k = id(a)
        if k not in self._segs:
            closed = isinstance(a, Patch)
            segs, rings = [], []
            for q in self.polys[k]:
                if closed and len(q) >= 3:
                    rings.append(ccw(q))
                es = _edges(q) if closed else ([(q[i], q[i + 1]) for i in range(len(q) - 1)] or [(q[0], q[0])])
                segs += [(e0[0], e0[1], e1[0], e1[1]) for e0, e1 in es]
            self._segs[k] = (rings, np.asarray(segs, dtype=float).reshape(-1, 4))
        rings, S = self._segs[k]
        if any(_inside_c(p, C) for C in rings):
            return 0.0
        if not len(S):
            return float("inf")
        dx, dy = S[:, 2] - S[:, 0], S[:, 3] - S[:, 1]
        L2 = dx * dx + dy * dy
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(L2 > 1e-24, np.clip(((p[0] - S[:, 0]) * dx + (p[1] - S[:, 1]) * dy) / L2, 0, 1), 0.0)
        return float(np.min(np.hypot(p[0] - (S[:, 0] + t * dx), p[1] - (S[:, 1] + t * dy))))

    def ink_dist(self, fid, p):
        return min((self._art_dist(a, p) for a in self.by_gid.get(fid, [])), default=float("inf"))

    def covering(self, fid, p):
        """covering_areas on the cached rings."""
        mine = [a for a in self.by_gid.get(fid, []) if self._art_dist(a, p) <= TOL_Z]
        top = max((self.rank[id(a)] for a in mine), default=(-1e9, -1))
        return sorted({h.gid for h in self.areas if h.gid != fid and not h.gid.startswith(fid + ":")
                       and self.rank[id(h.a)] > top and h.contains(p)})

    def hatch_end(self, fid, p0, p1):
        """leader_hatch on the cached rings."""
        k0 = int(ANCHOR_SAMPLES * (1 - LEADER_END))
        ks = list(range(k0, ANCHOR_SAMPLES))
        hit, gids = 0, set()
        hs = [h for h in self.hatch if h.gid != fid and not h.gid.startswith(fid + ":")]
        for k in ks:
            q = (p0[0] + (p1[0] - p0[0]) * k / ANCHOR_SAMPLES, p0[1] + (p1[1] - p0[1]) * k / ANCHOR_SAMPLES)
            inq = {h.gid for h in hs if h.contains(q)}
            if inq:
                hit += 1
                gids |= inq
        return gids if hit > LEADER_HATCH_MAX * len(ks) else set()

    def fail(self, fid, txy, anc):
        """First failing single-leader rule as (rule, detail), or None."""
        d = self.ink_dist(fid, anc)
        if d > TOL_Z:
            return ("off ink", f"{d:.2f}")
        cov = self.covering(fid, anc)
        if cov:
            return ("anchor under area", ", ".join(cov))
        if anchor_visibility_issue(self.vis, fid, anc):
            return ("anchor on hidden ink (e1)", "row has visible ink")
        over = set()
        for h in self.areas:
            if self.rank[id(h.a)] <= self.lz:
                continue
            for k in range(1, ANCHOR_SAMPLES):
                q = (txy[0] + (anc[0] - txy[0]) * k / ANCHOR_SAMPLES, txy[1] + (anc[1] - txy[1]) * k / ANCHOR_SAMPLES)
                if h.contains(q):
                    over.add(h.gid)
                    break
        if over:
            return ("area above leader", ", ".join(sorted(over)))
        hx = self.hatch_end(fid, txy, anc)
        if hx:
            return ("end in hatch", ", ".join(sorted(hx)))
        lo = leader_outline_issue(self.outl, fid, txy, anc, self.zmax)
        if lo:
            return ("end inside outline", ", ".join(f"{o} {mm:.1f} mm" for o, mm in lo))
        return None


def _column_default(ink, column):
    pts = [p for poly, _ in ink for p in poly]
    xm = max(p[0] for p in pts) if column == "right" else min(p[0] for p in pts)
    ym = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
    if ink_distance((xm, ym), ink) <= TOL_Z:
        return (xm, ym)
    cand = [p for p in pts if abs(p[0] - xm) <= TOL_Z]
    return min(cand, key=lambda p: abs(p[1] - ym))


def anchor_candidates(lc, row, column):
    """[(source, anchor)] for one row in one column, in placer order (see the block comment)."""
    ink = lc.ink(row["id"])
    if not ink:
        return []
    out = []
    if row.get("label_theta") is not None:
        hit = _ray_hit(ink, float(row["label_theta"]))
        if hit is not None:
            out.append(("label_theta", hit))
    first = _column_default(ink, column)
    out.append(("default", first))
    samples = []
    for poly, closed in ink:
        segs = _edges(poly) if closed else [(poly[i], poly[i + 1]) for i in range(len(poly) - 1)]
        for a, b in segs:
            m = max(1, int(math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / ANCHOR_STEP)))
            samples += [(a[0] + (b[0] - a[0]) * k / m, a[1] + (b[1] - a[1]) * k / m) for k in range(m + 1)]
    if column == "right":
        samples.sort(key=lambda q: (q[0] < first[0] - TOL_Z, math.hypot(q[0] - first[0], q[1] - first[1])))
    else:
        x_min = min(q[0] for q in samples)
        samples.sort(key=lambda q: (q[0] > x_min + TOL_Z, math.hypot(q[0] - x_min, q[1] - first[1])))
    out += [("ink", q) for q in samples]
    seen, uniq = set(), []
    for src, q in out:
        k = (round(q[0], 6), round(q[1], 6))
        if k not in seen:
            seen.add(k)
            uniq.append((src, (float(q[0]), float(q[1]))))
    return uniq


def place_plan_labels(ax, ctx, pose, margin=True, stack_pose=None, notes=()):
    """The plan leader placer (1.3 P1R R3; rules in the block comment above). margin=True: labels in a right column
    (x = right axes limit + one text line, left-aligned) and a left column (left limit - one line, right-aligned),
    stacked in anchor-y order with LABEL_GAP_LINES between boxes, as place_labels(margin=True), no left-column text box
    over a y tick label; notes without an anchor
    go under the right column below the axes. margin=False (fixtures): text 60 right (left column: 60 left) and 20 above
    the anchor. Call after render_plan and finish_axes. Returns the placer record (also ax._sc_placer)."""
    spec, P = ctx.spec, ctx.P
    outl, zmx = leader_outlines(ctx, pose)
    vis = row_visibility(ctx, ax, pose) if ctx.view == "plan_xy" and ctx.stack is not None else {}
    lc = _LeaderCtx(ax, outl, zmx, vis)
    rows = [r for r in spec.get("features", []) if r.get("label") and applies(r, pose) and lc.ink(r["id"])]
    order = [r["id"] for r in rows]
    byid = {r["id"]: r for r in rows}
    texts = {r["id"]: label_text(r, P, (stack_pose or {}).get(r["id"])) for r in rows}
    cands = {}
    for r in rows:
        cols = ["left", "right"] if r.get("label_side") == "left" else ["right", "left"]
        cands[r["id"]] = [(col, src, anc) for col in cols for src, anc in anchor_candidates(lc, r, col)]
    ax.apply_aspect()
    (_, y0), (_, y1) = ax.transData.transform([(0, 0), (0, 1)])
    line = LABEL_FONTSIZE * ax.figure.dpi / 72 * LABEL_LINESPACING / abs(y1 - y0)
    gap = line * LABEL_GAP_LINES
    zlo, zhi = ax.get_ylim()
    x_col, x_left = ax.get_xlim()[1] + line, ax.get_xlim()[0] - line
    ticks = []   # y bands of the y tick labels: left-column text must not overlap one
    if margin:
        rnd = ax.figure.canvas.get_renderer()
        for tl in ax.get_yticklabels():
            if tl.get_visible() and tl.get_text():
                e = tl.get_window_extent(rnd)
                ya, yb = (float(v[1]) for v in ax.transData.inverted().transform([(e.x0, e.y0), (e.x1, e.y1)]))
                if zlo <= (ya + yb) / 2 <= zhi:
                    ticks.append((min(ya, yb), max(ya, yb)))
    hgt = {f: line * (texts[f].count("\n") + 1) for f in order}

    def wanted(f, c):
        col, _, anc = c
        if not margin:
            return (anc[0] + (60 if col == "right" else -60), anc[1] + 20)
        h = hgt[f]
        return (x_col if col == "right" else x_left, min(max(anc[1], zlo + h / 2), zhi - h / 2))

    def layout(choice):
        pos = {}
        if not margin:
            return {f: wanted(f, c) for f, c in choice.items() if c}
        for col, xx in (("right", x_col), ("left", x_left)):
            items = sorted([f for f in order if choice.get(f) and choice[f][0] == col], key=lambda f: -choice[f][2][1])
            zs = _stack_z([choice[f][2][1] for f in items], [hgt[f] for f in items], zlo, zhi, gap)
            pos.update({f: (xx, z) for f, z in zip(items, zs)})
        return pos

    memo = {}

    def fail1(f, txy, anc):
        k = (f, round(txy[0], 9), round(txy[1], 9), anc)
        if k not in memo:
            memo[k] = lc.fail(f, txy, anc)
        return memo[k]

    def tick_clash(f, col, txy):
        if col != "left" or not margin:
            return None
        h = hgt[f]
        hit = [f"{(a + b) / 2:.0f}" for a, b in ticks if a < txy[1] + h / 2 and b > txy[1] - h / 2]
        return ("text over y tick label", ", ".join(hit)) if hit else None

    def issues(choice, pos):
        out = {}
        legs = [(f, pos[f], choice[f][2]) for f in order if choice.get(f)]
        for f, t, anc in legs:
            r = fail1(f, t, anc) or tick_clash(f, choice[f][0], t)
            if r:
                out.setdefault(f, []).append(r)
        for i in range(len(legs)):
            for j in range(i + 1, len(legs)):
                (fa, a0, a1), (fb, b0, b1) = legs[i], legs[j]
                if _segs_cross(a0, a1, b0, b1):
                    out.setdefault(fa, []).append(("crosses leader", fb))
                    out.setdefault(fb, []).append(("crosses leader", fa))
        return out

    choice = {}
    for f in order:
        choice[f] = next((c for c in cands[f] if not fail1(f, wanted(f, c), c[2]) and not tick_clash(f, c[0], wanted(f, c))), None)
    for _ in range(PLACER_PASSES):
        pos = layout(choice)
        iss = issues(choice, pos)
        bad = [f for f in order if iss.get(f) or choice[f] is None]
        if not bad:
            break
        changed = False
        for f in bad:
            base = {g: set(v) for g, v in iss.items() if g != f}
            for c in cands[f]:
                if c == choice[f] or fail1(f, wanted(f, c), c[2]) or tick_clash(f, c[0], wanted(f, c)):
                    continue
                trial = dict(choice)
                trial[f] = c
                p2 = layout(trial)
                i2 = issues(trial, p2)
                if not i2.get(f) and all(set(v) <= base.get(g, set()) for g, v in i2.items() if g != f):
                    choice, iss, changed = trial, i2, True
                    break
        if not changed:
            break
    pos = layout(choice)
    iss = issues(choice, pos)
    record = {"pose": pose, "placed": {}, "unplaceable": {}}
    for f in order:
        if choice[f] is None or iss.get(f):
            table = [{"column": col, "source": src, "anchor": [round(anc[0], 2), round(anc[1], 2)],
                      "fails": " / ".join(fail1(f, wanted(f, (col, src, anc)), anc) or tick_clash(f, col, wanted(f, (col, src, anc)))
                                          or ("passes alone; fails in the stacked layout",))}
                     for col, src, anc in cands[f]]
            record["unplaceable"][f] = {"candidates": len(table), "table": table,
                                        "final": [" / ".join(map(str, x)) for x in iss.get(f, [])]}
            if choice[f] is None:
                choice[f] = cands[f][0]
    pos = layout(choice)
    for f in order:
        col, src, anc = choice[f]
        record["placed"][f] = {"column": col, "source": src, "anchor": [round(anc[0], 2), round(anc[1], 2)],
                               "text": [round(pos[f][0], 2), round(pos[f][1], 2)]}
        kw = {"ha": "left" if col == "right" else "right", "va": "center"} if margin else {}
        ann = ax.annotate(texts[f], xy=anc, xytext=pos[f], fontsize=LABEL_FONTSIZE, zorder=LEADER_ZORDER, annotation_clip=False,
                          arrowprops={"arrowstyle": "-", "linewidth": 0.4 if margin else 0.5, **({"color": "0.35"} if margin else {})}, **kw)
        ann.set_gid(f"label:{f}")
    if margin:
        z = zlo - gap
        for n_ in notes:
            if n_[0]:
                raise ValueError("place_plan_labels: notes carry no anchor (S2 notes are free text under the right column)")
            txt, gid = n_[1], (n_[2] if len(n_) > 2 else None)
            h = line * (txt.count("\n") + 1)
            ann = ax.annotate(txt, xy=(x_col, z - h / 2), fontsize=LABEL_FONTSIZE, ha="left", va="center", annotation_clip=False)
            if gid:
                ann.set_gid(gid)
            z -= h + gap
    ax._sc_placer = record
    return record


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


BEZIER_STEPS = 8   # samples per Bezier segment (1.2 (c)): curve points only, control points dropped


def _bezier(ctrl, t):
    pts = [np.asarray(p, dtype=float) for p in ctrl]
    while len(pts) > 1:
        pts = [(1 - t) * p + t * q for p, q in zip(pts[:-1], pts[1:])]
    return pts[0]


def flatten_path(path):
    """Polygons of a path in its own coordinates. Line segments keep their vertices; each Bezier segment is sampled at
    BEZIER_STEPS points on the curve (1.2 (c): a Circle path's control points lie up to 0.041 % outside the circle,
    which false-fires plan containment and contact tests; matplotlib's 8-segment circle is within 4e-6 r on the curve)."""
    polys, pts, cur, start = [], [], None, None
    for verts, code in path.iter_segments(curves=True, simplify=False):
        v = np.asarray(verts, dtype=float).reshape(-1, 2)
        if code == MPath.MOVETO:
            if len(pts) > 1:
                polys.append(pts)
            pts, cur, start = [(float(v[0][0]), float(v[0][1]))], v[0], v[0]
        elif code == MPath.LINETO:
            pts.append((float(v[0][0]), float(v[0][1])))
            cur = v[0]
        elif code in (MPath.CURVE3, MPath.CURVE4):
            ctrl = [cur] + list(v)
            for t in np.linspace(0, 1, BEZIER_STEPS + 1)[1:]:
                q = _bezier(ctrl, t)
                pts.append((float(q[0]), float(q[1])))
            cur = v[-1]
        elif code == MPath.CLOSEPOLY:
            if len(pts) > 1:
                polys.append(pts)
            pts, cur = [], start
    if len(pts) > 1:
        polys.append(pts)
    out = []
    for p in polys:
        if len(p) > 1 and abs(p[0][0] - p[-1][0]) < 1e-9 and abs(p[0][1] - p[-1][1]) < 1e-9:
            p = p[:-1]
        out.append(p)
    return out or [[(float(x), float(y)) for x, y in path.vertices]]


def artist_polys(a):
    """Polygons in rendered data coordinates (closing vertex dropped; curves sampled on the curve, 1.2 (c))."""
    T = _to_data(a)
    if isinstance(a, Line2D):
        return [_xy(T, list(zip(a.get_xdata(), a.get_ydata())))]
    if isinstance(a, Patch):
        path = a.get_path().transformed(T) if T is not None else a.get_path()
        return flatten_path(path)
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
    """Drawn polygons of a row, each part once: a renderer hidden copy (1.3 P1R; artist attribute _sc_hidden_copy, set by
    render_plan) repeats the geometry of the piece it is split from and is left out (areas, overlaps, extents)."""
    return [poly for a in tagged(ax).get(gid, []) if not getattr(a, "_sc_hidden_copy", False) for poly in artist_polys(a)]


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


def assess_pair(cls, g_min, PA, PB, gap, names=("a", "b"), plan_gap=None, plan_contact=None):
    """One judgement for K7 static, K7 swept and S1-5b (LF-1, LF-4, TP-11).
    gap: band gap along the view direction (side: depth bands; plan: z bands); disjoint bands settle F only.
    C: fails when the bands are more than TOL_C apart. G: the 3D distance is at least max(gap, projected distance),
    so it passes when that lower bound reaches g_min. N: nested, declared, not measured.
    plan_gap (side views; a number or a callable, evaluated only when the side-view test fails): distance between
    the two parts' plan footprints from the spec placement (LF-8 at 1.1 (b)). The plan view is a projection too, so
    the 3D distance is at least max(plan_gap, projected distance): an F pair passes when plan_gap > TOL_C, a G pair
    when that lower bound reaches g_min - TOL_C. State "plan-separated". C pairs are not relieved.
    plan_contact (side views, C pairs; callable -> (plan distance, plan overlap area) or None; r3, Designer M1 r2 F1/F2):
    a C pair whose side-view pieces overlap passes as "plan-contact" when both rows are placed prisms whose plan
    footprints touch (distance <= TOL_C) without overlap (area <= TOL_AREA). Vertical prisms with disjoint plan
    interiors cannot interpenetrate, and touching footprints with overlapping z extents (the side-view overlap
    proves it) are in contact on a vertical face. A side-view overlap at an oblique azimuth is then a projection
    artefact (bracket arm on its block and frame member at theta 150; motor shaft on its flange).
    Returns (ok, state, text, lower_bound)."""
    ok, st, txt, lb = _assess_pair(cls, g_min, PA, PB, gap, names)
    if not ok and cls == "C" and st == "overlap" and plan_contact is not None:
        pc = plan_contact() if callable(plan_contact) else plan_contact
        if pc is None:
            return ok, st, txt + "; no placed plan footprints for the plan-contact test", lb
        pd, pa = pc
        if pd <= TOL_C and pa <= TOL_AREA:
            return True, "plan-contact", f"plan footprints touch (distance {pd:.3f} mm, overlap {pa:.3f} mm2); side view: {txt}", 0.0
        return False, st, f"{txt}; plan footprints distance {pd:.3f} mm, overlap {pa:.3f} mm2 (plan-contact needs <= {TOL_C}, <= {TOL_AREA})", lb
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
            import check_stack as cs  # stdlib + sketch_loader only; no cycle
            return cs.radial_corners(r0, r1, pl["theta"], w, pl.get("rot", 0))
        pts = _ngon(r0 * c, r0 * s, w) + (_ngon(r1 * c, r1 * s, w) if abs(r1 - r0) > 1e-9 else [])
        return convex_hull(pts)
    pcs = (rec or {}).get("plan_pieces")
    if pcs:   # 1.2 (b): plan_poly row (guide tie strip); one piece is its true section, several give their hull
        return list(pcs[0]) if len(pcs) == 1 else convex_hull([p for pc in pcs for p in pc])
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


def plan_contact_fn(ctx, rows, pose, a, b):
    """Callable for assess_pair: (plan distance, plan overlap area) of rows a and b at pose from their `place`
    footprints, or None unless both rows are placed (a depth-band disk is a containment bound, no contact proof).
    1.2 (b): a plan_poly row of exactly one convex piece (guide tie strip) counts as placed; its containment premise is
    K8 projected_extent on plan_x (K8-B17)."""
    def placed(r):
        return bool(r.get("place")) or len(r.get("plan_pieces") or []) == 1

    def f():
        ra, rb = _feat(ctx, pose, a), _feat(ctx, pose, b)
        if not (placed(ra) and placed(rb)):
            return None
        fa, fb = plan_footprint(rows.get(a, {}), ra), plan_footprint(rows.get(b, {}), rb)
        return min_distance(fa, fb), overlap_area(fa, fb)
    return f


# ======================================================================== plan view (1.2 (c): SW-17, TP-13, LF-8, K6 plan)

def to_ut(pts, theta):
    """Radial frame at azimuth theta (deg): u along the radial direction, t across it (counter-clockwise positive)."""
    c, s = math.cos(math.radians(theta)), math.sin(math.radians(theta))
    return [(x * c + y * s, -x * s + y * c) for x, y in pts]


def bbox(polys):
    xs = [p[0] for poly in polys for p in poly]
    ys = [p[1] for poly in polys for p in poly]
    return (min(xs), max(xs), min(ys), max(ys)) if xs else None


def _eval_section(ctx, row, pose):
    """Plain section [r_in, r_out] (no z pieces) evaluated; None for a piecewise section or no section."""
    sec = row.get("section")
    if not sec or isinstance(sec[0], (list, tuple)):
        return None
    import check_stack as cs  # stdlib + sketch_loader only; no cycle
    names = (ctx.stack or {}).get("poses", {}).get(pose, {}).get("vars_z_A", {})
    a, b = (cs.eval_expr(e, ctx.P, names) for e in sec)
    return float(min(a, b)), float(max(a, b))


def plan_outline(ctx, row, pose):
    """Plan outline of a row from the spec, the K7 plan test geometry (1.2 (c), LF-8: true XY outlines). Returns
    (kind, data, true) or None. kind 'annulus': data (a, b), the radial interval about the drill axis (a section row:
    ring, bearing, gear, gear hub; a round place centred on the axis: drill tube, cutter rim, keep-out). kind 'polys':
    data a list of convex pieces (radial or round place footprint; plan_poly pieces, each its own piece). true: the
    outline is the part's true plan section, the premise of a plan C pass (radial footprint drawn as a rectangle,
    round footprint drawn as a circle, section annulus, plan_poly piece); a circumscribing footprint (lift motor 42
    square in a circle, pinion trapezoid in its rectangle, depth-band disk) is a containment bound for F and G only."""
    rec = _feat(ctx, pose, row["id"])
    proj = row.get("projection")
    sec = _eval_section(ctx, row, pose)
    if sec is not None and not rec.get("place"):
        return ("annulus", sec, True)
    pl = rec.get("place")
    if pl:
        centred = abs(pl["r_in"]) < 1e-9 and abs(pl["r_out"]) < 1e-9
        if pl["footprint"] == "round" and centred:
            return ("annulus", (0.0, float(pl["half_width"])), proj == "circle")
        true = (pl["footprint"] == "radial" and proj == "rectangle") or \
               (pl["footprint"] == "round" and proj == "circle" and abs(pl["r_in"] - pl["r_out"]) < 1e-9)
        return ("polys", [plan_footprint(row, rec)], bool(true))
    if rec.get("plan_pieces"):
        return ("polys", [list(p) for p in rec["plan_pieces"]], True)
    dep = rec.get("depth")
    if dep and row.get("kind") in ROUND_KINDS and row.get("axis") == "Z" and abs(dep[0] + dep[1]) < 1e-9:
        return ("annulus", (0.0, float(dep[1])), False)
    return None


def _radius_range(poly):
    """(least, greatest) distance from the drill axis (origin) to a convex piece (or segment, or point)."""
    rmax = max(math.hypot(x, y) for x, y in poly)
    if len(poly) >= 3 and _inside((0.0, 0.0), poly):
        return 0.0, rmax
    rmin = min(_pt_seg((0.0, 0.0), a, b) for a, b in _edges(poly))
    return rmin, rmax


def _annulus_vs_polys(ab, polys):
    a, b = ab
    dists, area = [], 0.0
    for poly in polys:
        rmin, rmax = _radius_range(poly)
        if rmax <= a:
            dists.append(a - rmax)
        elif rmin >= b:
            dists.append(rmin - b)
        else:
            dists.append(0.0)
            if len(poly) >= 3:
                area += overlap_area(poly, _ngon(0.0, 0.0, b)) - (overlap_area(poly, _ngon(0.0, 0.0, a)) if a > 1e-9 else 0.0)
    return min(dists), max(area, 0.0)


def _bbox_gap(A, B):
    ba, bb = bbox(A), bbox(B)
    return max(bb[0] - ba[1], ba[0] - bb[1], bb[2] - ba[3], ba[2] - bb[3], 0.0)


def outline_measure(OA, OB, need=TOL_C):
    """(distance, overlap area) between two plan outlines. Annulus pairs are exact (radial intervals about the axis);
    annulus against a piece uses the piece's radius range (exact distance; area by the circumscribing 128-gons).
    Pieces against pieces: when the bounding boxes are more than need + 1 apart the box gap is returned (a lower bound
    on the distance, overlap 0), else the exact convex measure."""
    ka, kb = OA[0], OB[0]
    if ka == "annulus" and kb == "annulus":
        (a1, b1), (a2, b2) = OA[1], OB[1]
        lo, hi = max(a1, a2), min(b1, b2)
        return max(a2 - b1, a1 - b2, 0.0), (math.pi * (hi * hi - lo * lo) if hi > lo else 0.0)
    if ka == "annulus":
        return _annulus_vs_polys(OA[1], OB[1])
    if kb == "annulus":
        return _annulus_vs_polys(OB[1], OA[1])
    g = _bbox_gap(OA[1], OB[1])
    if g > need + 1:
        return g, 0.0
    area = sum(overlap_area(p, q) for p in OA[1] for q in OB[1] if len(p) >= 3 and len(q) >= 3)
    return min(min_distance(p, q) for p in OA[1] for q in OB[1]), area


def outline_outside(O, p):
    """Distance by which point p lies outside outline O (0 inside or on it)."""
    if O[0] == "annulus":
        a, b = O[1]
        r = math.hypot(*p)
        return max(a - r, r - b, 0.0)
    best = None
    for poly in O[1]:
        d = 0.0 if (len(poly) >= 3 and _inside(p, poly)) else min(_pt_seg(p, q, r) for q, r in _edges(poly))
        best = d if best is None else min(best, d)
    return best


def sector_outside(sec, p):
    """Distance by which p lies outside the spec wedge (apex on the axis, theta +- half_angle, radius r), half-angle
    <= 90 (convex wedge)."""
    r = math.hypot(*p)
    if r < 1e-12:
        return 0.0
    phi = math.degrees(math.atan2(p[1], p[0]))
    d_ang = abs((phi - sec["theta"] + 180) % 360 - 180) - sec["half_angle"]
    d_edge = r * math.sin(math.radians(d_ang)) if 0 < d_ang < 90 else (r if d_ang >= 90 else 0.0)
    return max(r - sec["r"], d_edge, 0.0)


def sector_boundary(sec, step=1.0):
    th, ha, r = sec["theta"], sec["half_angle"], sec["r"]
    n = max(2, int(math.ceil(2 * ha / step)) + 1)
    arc = [(r * math.cos(math.radians(th - ha + 2 * ha * i / (n - 1))), r * math.sin(math.radians(th - ha + 2 * ha * i / (n - 1)))) for i in range(n)]
    edges = [(f * x, f * y) for x, y in (arc[0], arc[-1]) for f in (0.25, 0.5, 0.75)]
    return [(0.0, 0.0)] + arc + edges


def _plan_judge(cls, g_min, OA, OB, gap, measure=None):
    """One judgement for the K7 plan test (1.2 (c), LF-8 remainder). gap: z band gap (> TOL_C disjoint, |gap| <= TOL_C
    touching, < -TOL_C overlapping; None unknown, read as overlapping). Disjoint or touching bands settle F (no common
    volume, z-separated / z-touch); with overlapping bands F passes on plan overlap <= TOL_AREA; G on max(z gap, plan
    distance) >= g_min - TOL_C; a C pair with disjoint bands fails (z-separated). Plan C rule: bands touching and plan
    distance <= TOL_C (overlap allowed: one part stands on the other) is z-contact; bands overlapping, plan distance
    <= TOL_C and plan overlap <= TOL_AREA (side by side on a vertical face) is plan-contact; bands overlapping with plan
    overlap > TOL_AREA is interference. Premise of both C passes: both outlines are true plan sections (plan_outline
    true). Returns (ok, state, text, lower_bound)."""
    g = g_min or 0
    if cls == "N":
        return True, "N", "nested (declared)", None
    if cls not in ("C", "G", "F"):
        return False, "error", f"unknown class {cls}", None
    if cls == "F" and gap is not None and gap >= -TOL_C:
        # F forbids overlap only (gameplan K7 classes): z bands that touch leave no common volume whatever the plan
        # overlap (a drill tube standing on its head; the side-view analogue is touching pieces, state C)
        return True, ("z-separated" if gap > TOL_C else "z-touch"), f"z bands {gap:.3f} mm apart", max(gap, 0.0)
    if gap is not None and gap > TOL_C:
        if cls == "G" and gap >= g - TOL_C:
            return True, "z-separated", f"z bands {gap:.3f} mm apart, g_min {g}", gap
        if cls == "C":
            return False, "z-separated", f"C pair z-separated by {gap:.3f} mm (contact needs z bands within {TOL_C})", gap
    d, area = (measure or outline_measure)(OA, OB, g if cls == "G" else TOL_C)
    touch = gap is not None and gap >= -TOL_C
    if cls == "F":
        st = pair_state(d, area)
        return area <= TOL_AREA, st, f"plan distance {d:.3f} mm, overlap {area:.3f} mm2, z gap {_f3(gap)}, state {st}", d if area <= TOL_AREA else -area
    if cls == "G":
        zg = gap if (gap is not None and gap > 0) else 0.0
        lb = max(zg, d if area <= TOL_AREA else 0.0)
        ok = lb >= g - TOL_C
        return ok, ("G" if ok else "short"), (f"z gap {_f3(gap)}, plan distance {d:.3f} mm, overlap {area:.3f} mm2, lower bound {lb:.3f}, "
                                              f"g_min {g}, gap - g_min {lb - g:+.3f}"), lb
    true = OA[2] and OB[2]
    if touch:
        if d > TOL_C:
            return False, "open", f"z bands touch ({gap:.3f} mm), plan distance {d:.3f} mm (contact needs <= {TOL_C})", d
        if not true:
            return False, "z-contact", f"z-contact (plan overlap {area:.3f} mm2) needs true plan sections; a circumscribing outline certifies F and G only", 0.0
        return True, "z-contact", f"z bands touch ({gap:.3f} mm), plan distance {d:.3f} mm, plan overlap {area:.3f} mm2", 0.0
    if area > TOL_AREA:
        return False, "interference", f"z bands overlap {-gap if gap is not None else float('nan'):.3f} mm, plan overlap {area:.3f} mm2 (interference)", -area
    if d > TOL_C:
        return False, "open", f"z bands overlap, plan distance {d:.3f} mm (contact needs <= {TOL_C})", d
    if not true:
        return False, "plan-contact", "plan-contact needs true plan sections; a circumscribing outline certifies F and G only", 0.0
    return True, "plan-contact", f"z bands overlap, plan outlines touch (distance {d:.3f} mm, overlap {area:.3f} mm2)", 0.0


def _f3(v):
    return "none" if v is None else f"{v:.3f}"


def plan_fig(ctx, pose):
    """The figure that carries the plan drawing at pose: its own figure, else the one plan figure (spec plan_figure)."""
    if pose in ctx.figs:
        return ctx.figs[pose]
    pf = (ctx.spec.get("plan_figure") or {}).get("pose")
    if pf in ctx.figs:
        return ctx.figs[pf]
    return next(iter(ctx.figs.values())) if len(ctx.figs) == 1 else None


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
               "mirror_about_axis": "axis", "azimuth": "expr", "taper": "narrows", "face_rises": "toward",
               "ticks_radial": "count", "outline_matches": "pieces"}


FRAME_VALUES = ("radial",)   # sense `frame` values a predicate may carry (outboard radial form, plan_xy only: TP1.2-1)
STAND_IN_OWNER = re.compile(r"\bStep\s+\d+(?:\.\d+)?\b|\b[Ss][1-6]\b")   # TP1.2-18: a Step id or a sketch id


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
            elif "frame" in pr and pr["frame"] not in FRAME_VALUES:
                # Topologist 1.2 (c) NOTE 2 (1.3 step 0 R5 c): plan reads any frame value as radial; only a known value passes
                msg = f"{row['id']} {kind}: spec error, unknown frame {pr['frame']!r} (known: {', '.join(FRAME_VALUES)})"
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
    expr_issues, n_expr = expr_agreement_issues(P)
    issues += expr_issues
    n = len(P.overlay)
    return result("K2", not issues, _summ(issues) if issues else f"{len(spec_keys(ctx.spec))} spec keys resolve; {n} overlay leaves sourced, legal status, no shadow; "
                  f"{n_expr} expr leaves agree within {TOL_Z}",
                  measured=len(issues), threshold=0, n_issues=len(issues))


# The member-top chain (1.3 open O2): these overlay leaves, when present, must carry exactly this expr (whitespace-free
# comparison), so neither deleting nor rewriting the expr silences the agreement lint (Loftsman P0L FIX 1).
EXPR_REQUIRED = {
    "jackscrew.top_guide_z": "jackscrew.anchor_z + jackscrew.length",
    "frame_upper.member_length": "jackscrew.top_guide_z + profile.height - base.plate_thickness",
    "frame_upper.member_length_rail": "jackscrew.top_guide_z + profile.height",
}


def expr_agreement_issues(P):
    """1.3 step 0 R2 (O2): an overlay leaf with an `expr` field (arithmetic in other keys, check_stack.eval_expr) fails
    when |value - eval(expr)| > TOL_Z. Premise of every DERIVED literal that carries one (jackscrew.top_guide_z,
    frame_upper.member_length, frame_upper.member_length_rail mandatory). The evaluation does not add to P.accessed, so
    a record's keys_read is unchanged by the lint. Returns (issues, leaves with expr)."""
    import check_stack as cs  # stdlib + sketch_loader only; no cycle
    issues, n = [], 0
    norm = lambda e: "".join(str(e).split())  # noqa: E731
    for k, want in EXPR_REQUIRED.items():   # Loftsman P0L FIX 1: the chain premise is a check, not a convention
        leaf = P.overlay.get(k)
        if not isinstance(leaf, dict) or leaf.get("_malformed"):
            continue
        if "expr" not in leaf:
            issues.append(f"overlay {k}: expr required ({want}) (Loftsman P0L FIX 1)")
        elif norm(leaf["expr"]) != norm(want):
            issues.append(f"overlay {k}: expr altered, has {leaf['expr']!r}, required {want!r} (Loftsman P0L FIX 1)")
    acc = dict(P.accessed)
    try:
        for k, leaf in P.overlay.items():
            if not isinstance(leaf, dict) or "expr" not in leaf or leaf.get("_malformed"):
                continue
            n += 1
            try:
                v = cs.eval_expr(leaf["expr"], P, {})
            except Exception as e:  # noqa: BLE001
                issues.append(f"overlay {k}: expr {leaf['expr']!r} does not evaluate ({type(e).__name__}: {e})")
                continue
            val = P.get(k)
            if not isinstance(val, (int, float)) or isinstance(val, bool) or not isinstance(v, (int, float)):
                issues.append(f"overlay {k}: expr {leaf['expr']!r} on a non-numeric value {val!r}")
            elif abs(val - v) > TOL_Z:
                issues.append(f"overlay {k}: value {val:g} vs expr {leaf['expr']} = {v:.2f}, {abs(val - v):.2f} apart")
    finally:
        P.accessed.clear()
        P.accessed.update(acc)
    return issues, n


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
    issues += text_clip_issues(ctx)
    return result("K3", not issues, _summ(issues) if issues else f"{len(ctx.figs)} figure(s): one Axes, title, (mm) labels, equal aspect, grids, figsize, dpi {DPI}; every text inside the saved image",
                  measured=len(issues), threshold=0, n_issues=len(issues))


def saves_tight(paths):
    """True when every savefig call in the scripts passes bbox_inches="tight" (and there is at least one)."""
    calls = []
    for path in paths:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "savefig":
                calls.append(any(kw.arg == "bbox_inches" and isinstance(kw.value, ast.Constant) and kw.value.value == "tight"
                                 for kw in node.keywords))
    return bool(calls) and all(calls)


def text_clip_issues(ctx):
    """1.2 (h), Designer M1 S1 r5 F1: every Text of the figure (labels, notes, tags, title) lies inside the saved image.
    The saved image is the figure canvas, or the tight bounding box of every artist when every savefig call of the
    script passes bbox_inches="tight" (premise read from the script source; a fixture without a script is held to the
    canvas). Window extents in pixels, tolerance half a pixel."""
    out = []
    tight = saves_tight(ctx.script_paths) if ctx.script_paths else False
    for name, fig in ctx.figs.items():
        r = fig.canvas.get_renderer()
        box = fig.get_tightbbox(r).transformed(fig.dpi_scale_trans) if tight else fig.bbox
        texts = [t for ax in fig.axes for t in ax.texts] + list(fig.texts) + [ax.title for ax in fig.axes]
        for t in texts:
            if not t.get_visible() or not t.get_text():
                continue
            e = t.get_window_extent(r)
            over = max(box.x0 - e.x0, box.y0 - e.y0, e.x1 - box.x1, e.y1 - box.y1)
            if over > 0.5:
                first = t.get_text().splitlines()[-1][:60] if t.get_text().splitlines() else t.get_text()[:60]
                out.append(f"{name}: text {first!r} runs {over:.0f} px outside the saved image")
    return out


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
    issues += figure_note_issues(ctx)
    issues += leader_issues(ctx)
    extra = {}
    for pose, fig in ctx.figs.items():   # 1.3 P1R: the placer's UNPLACEABLE candidate tables go into the record
        for fid, u in ((getattr(fig.axes[0], "_sc_placer", None) or {}).get("unplaceable") or {}).items():
            extra.setdefault("unplaceable", {})[f"{pose}/{fid}"] = u
    return result("K4", not issues, _summ(issues) if issues else f"{n} label(s) carry their key value, each leader ends on its part, no two leaders cross; figure note names every not_drawn part",
                  measured=len(issues), threshold=0, n_issues=len(issues), **extra)


NOTE_GID = "note:figure_note"


def leader_issues(ctx):
    """1.2 (h), Designer M1 r1 F4 and F5. (a) Every label annotation (gid label:<id>) ends its leader (xy) on the ink of
    its row, within TOL_Z: on a closed outline or inside it, or on a drawn line. (b) No two label leaders cross: the
    leader is the segment from the text position (xytext; the label xy when the label has no separate text position)
    to xy, in data coordinates, and two leaders that properly intersect fail. r3 (Designer M1 S2 r2 F1, S1 r6 F1):
    (a') the anchor lies on ink no area of another row covers (an area artist, filled or hatched, drawn above the
    row's ink there); (c) no area artist is drawn above a leader where the leader runs (sampled along the segment), so
    the visible end of the leader is its anchor. 1.3 P1R, plan view: (e) the last quarter of a leader lies outside every
    other row's true plan outline that does not contain its anchor (leader_outline_issue; Design Notes 30); (f) a label
    the placer recorded UNPLACEABLE (ax._sc_placer) fails with reason "unplaceable" and is not judged again by (a) to (e).
    Containment of an area is as drawn (even-odd rings, clip region of a renderer piece)."""
    out = []
    plan = ctx.view == "plan_xy"
    for pose, fig in ctx.figs.items():
        ax = fig.axes[0]
        legs = []
        rank = _rank(ax)
        rec = getattr(ax, "_sc_placer", None) or {}
        unpl = rec.get("unplaceable", {})
        for fid in sorted(unpl):   # 1.3 P1R: the placer found no candidate passing every rule (no silent fall-back)
            out.append(f"{pose}/{fid}: label unplaceable ({unpl[fid]['candidates']} candidate(s), none passes every leader rule; "
                       f"table in the placer record)")
        outl, zmx = leader_outlines(ctx, pose)
        vis = row_visibility(ctx, ax, pose) if plan and ctx.stack is not None else {}
        areas = [(a, [q for q in artist_polys(a) if len(q) >= 3]) for a in artists(ax) if a.get_gid() and is_area(a)]
        hatches = hatch_areas(ax)
        for t in ax.texts:
            g = t.get_gid() or ""
            if not g.startswith("label:") or not hasattr(t, "xy"):
                continue
            fid = g[len("label:"):]
            ink = ink_pieces(ax, fid)
            xy = tuple(float(v) for v in t.xy)
            if not ink or fid in unpl:
                continue          # K9 reports an undrawn row; an unplaceable label is reported once, above
            d = ink_distance(xy, ink)
            if d > TOL_Z:
                out.append(f"{pose}/{fid}: label leader ends at ({xy[0]:.2f}, {xy[1]:.2f}), {d:.2f} off the drawn part")
            else:
                cov = covering_areas(ax, fid, xy, rank)
                if cov:
                    out.append(f"{pose}/{fid}: label anchor ({xy[0]:.2f}, {xy[1]:.2f}) under the area of {', '.join(sorted(set(cov)))}")
            xt = getattr(t, "xyann", None)
            if xt is not None and (abs(xt[0] - xy[0]) > 1e-9 or abs(xt[1] - xy[1]) > 1e-9):
                lz = (t.get_zorder(), max(i for i, k in enumerate(ax.get_children()) if k is t))
                over = set()
                for a, polys in areas:
                    if rank[id(a)] <= lz:
                        continue
                    for k in range(1, ANCHOR_SAMPLES):
                        q = (xt[0] + (xy[0] - xt[0]) * k / ANCHOR_SAMPLES, xt[1] + (xy[1] - xt[1]) * k / ANCHOR_SAMPLES)
                        if in_drawn(a, q, polys):
                            over.add(a.get_gid())
                            break
                if over:
                    out.append(f"{pose}/{fid}: label leader runs under the area of {', '.join(sorted(over))}")
                hx = leader_hatch(fid, (float(xt[0]), float(xt[1])), xy, hatches)
                if hx:
                    out.append(f"{pose}/{fid}: label leader ends across the hatch of {', '.join(sorted(hx))}")
                if plan:   # 1.3 P1Rf (Designer FIX D1): (e1) visible ink, (g) a wholly hidden row names its cover
                    for msg in (anchor_visibility_issue(vis, fid, xy), cover_name_issue(ctx, vis, outl, zmx, fid, xy, t.get_text())):
                        if msg:
                            out.append(f"{pose}/{fid}: {msg}")
                for oid, mm in leader_outline_issue(outl, fid, (float(xt[0]), float(xt[1])), xy, zmx):   # 1.3 P1R, Design Notes 30
                    out.append(f"{pose}/{fid}: label leader ends inside the outline of {oid} ({mm:.1f} mm of its last quarter)")
            if xt is not None and (abs(xt[0] - xy[0]) > 1e-9 or abs(xt[1] - xy[1]) > 1e-9):
                legs.append((fid, (float(xt[0]), float(xt[1])), xy))
        for i in range(len(legs)):
            for j in range(i + 1, len(legs)):
                (fa, a0, a1), (fb, b0, b1) = legs[i], legs[j]
                if _segs_cross(a0, a1, b0, b1):
                    out.append(f"{pose}: label leaders {fa} and {fb} cross")
    return out


def part_head(part):
    """Name head of a not_drawn part: the text before the first ' (' or ' at ' ('descent-stop pads at ...' -> 'descent-stop
    pads', 'LM20UU bushing (OD 32 x 42)' -> 'LM20UU bushing')."""
    return re.split(r" \(| at ", str(part), maxsplit=1)[0].strip()


def figure_note_issues(ctx):
    """Detail 1 common (b), from S2 on (1.2 (c), Designer 1.2 (b) FIX 3): the spec figure_note (plan_figure.figure_note
    or a top-level figure_note) names the head of every not_drawn part, and each figure carries a Text with gid
    note:figure_note whose text names every head. A spec with not_drawn and no figure_note fails, whatever its sketch id
    (Designer 1.2 (c) FIX R1). The only exempt record is one accepted before the rule with no not_drawn entry (S1 r4),
    which this branch passes because its not_drawn is empty; S1 r5 on carries a figure_note."""
    spec = ctx.spec or {}
    note = (spec.get("plan_figure") or {}).get("figure_note") or spec.get("figure_note")
    nd = spec.get("not_drawn") or []
    if note is None:
        return [f"spec error: not_drawn ({len(nd)}) without figure_note"] if nd else []
    norm = lambda s: " ".join(str(s).split())  # noqa: E731
    heads = [part_head(e.get("part") if isinstance(e, dict) else e) for e in nd]
    out = [f"spec figure_note lacks not_drawn part {h!r}" for h in heads if norm(h) not in norm(note)]
    for pose, fig in ctx.figs.items():
        texts = [t.get_text() for t in fig.axes[0].texts if t.get_gid() == NOTE_GID]
        if not texts:
            out.append(f"{pose}: no figure note ({NOTE_GID})")
            continue
        drawn = norm(" ".join(texts))
        out += [f"{pose}: drawn figure note lacks not_drawn part {h!r}" for h in heads if norm(h) not in drawn]
    return out


# ======================================================================== K5 projection

def _is_rect(pts, rel=1e-7):
    """Four vertices with four right angles (any orientation; TP-13 at 1.2 (c))."""
    for i in range(4):
        o, a, b = pts[i - 1], pts[i], pts[(i + 1) % 4]
        e1, e2 = (a[0] - o[0], a[1] - o[1]), (b[0] - a[0], b[1] - a[1])
        n1, n2 = math.hypot(*e1), math.hypot(*e2)
        if n1 < 1e-12 or n2 < 1e-12 or abs(e1[0] * e2[0] + e1[1] * e2[1]) > rel * n1 * n2:
            return False
    return True


def classify(a):
    """Projection class of an artist. 1.2 (c) TP-13: a four-vertex Polygon with four right angles is a rectangle at any
    orientation (a radial rectangle at an oblique azimuth read as trapezoid before); an Annulus is the circle
    projection of an axis-Z part with a bore."""
    if isinstance(a, (Circle, Ellipse, Annulus)):
        return "circle"
    if isinstance(a, Rectangle):
        return "rectangle"
    if isinstance(a, Line2D):
        return "line"
    if isinstance(a, Polygon):
        pts = artist_polys(a)[0]
        if len(pts) == 4:
            return "rectangle" if _is_rect(pts) else "trapezoid"
        return "polygon"
    return type(a).__name__


RADIAL_TOL_DEG = 0.1


def _tangential_edges(pts, theta):
    """Edges of a piece that run across the radial direction at theta (within RADIAL_TOL_DEG), with their mean u."""
    out = []
    for p, q in _edges(pts):
        (u0, t0), (u1, t1) = to_ut([p, q], theta)
        L = math.hypot(u1 - u0, t1 - t0)
        if L > 1e-9 and abs(u1 - u0) / L <= math.sin(math.radians(RADIAL_TOL_DEG)):
            out.append(((u0 + u1) / 2, (p, q)))
    return out


def heel_point(pts, theta):
    """Pitch point of a bevel pinion drawn in plan (S2-3, 1.2 (c)): midpoint of the outer of the toothed trapezoid's
    two tangential edges (the heel). None when the piece has no tangential edge pair."""
    te = _tangential_edges(pts, theta)
    if len(te) < 2:
        return None
    _, (p, q) = max(te, key=lambda e: e[0])
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


TICKS_SUFFIX = ":ticks"


def ticks_admission_issue(row, artist, plan, siblings):
    """1.2 (h), Designer M1 r1 F1 rule: K5 admits, under a gear row, one LineCollection sub-artist <row>:ticks (the
    dashed tooth ticks on the underside face) in plan_xy, only when the row carries the K8 ticks_radial predicate that
    enforces the premise (radial direction, ends between toe and heel, count). None when admitted, else the reason."""
    if row is None:
        return "sub-artist of no spec row"
    if row.get("kind") != "gear" or row.get("axis") != "Z" or not plan:
        return f"tick sub-artist admitted only for a gear row with axis Z in plan_xy ({row.get('kind')}, axis {row.get('axis')})"
    if not isinstance(artist, LineCollection):
        return f"tick sub-artist must be a LineCollection (drawn as {type(artist).__name__})"
    if len(siblings) != 1:
        return f"{len(siblings)} tick sub-artists, one admitted"
    if not any(pr.get("pred") == "ticks_radial" for pr in row.get("sense") or []):
        return "tick sub-artist without the K8 ticks_radial predicate on its row (premise unenforced)"
    return None


OUTLINE_SUFFIX = ":outline"
SUB_SUFFIXES = (TICKS_SUFFIX, OUTLINE_SUFFIX)


def outline_admission_issue(row, artist, plan, siblings):
    """r4 (Designer sign-off r3, M1 S2 r2 N2): K5 admits, under a plate row with plan_poly pieces, one unfilled closed
    Polygon <row>:outline in plan_xy, only when the row carries the K8 outline_matches predicate (its premise check).
    None when admitted, else the reason."""
    if row is None:
        return "sub-artist of no spec row"
    if row.get("kind") != "plate" or not row.get("plan_poly") or not plan:
        return f"outline sub-artist admitted only for a plate row with plan_poly in plan_xy ({row.get('kind')})"
    if not isinstance(artist, Polygon) or artist.get_fill():
        return f"outline sub-artist must be an unfilled Polygon (drawn as {type(artist).__name__}, fill {getattr(artist, 'get_fill', lambda: None)()})"
    if len(siblings) != 1:
        return f"{len(siblings)} outline sub-artists, one admitted"
    if not any(pr.get("pred") == "outline_matches" for pr in row.get("sense") or []):
        return "outline sub-artist without the K8 outline_matches predicate on its row (premise unenforced)"
    return None


def union_boundary(pieces, tol=1e-6):
    """Boundary ring of the union of convex pieces that meet along shared edges (plate pieces): every edge is cut at the
    vertices of the other pieces lying on it; sub-edges carried by two pieces are interior and dropped; the rest are
    chained into one ring and collinear vertices are merged. Counter-clockwise; None when the edges do not close
    into one ring."""
    verts = [tuple(v) for pc in pieces for v in pc]
    subs = {}
    for pc in pieces:
        pc = ccw([tuple(v) for v in pc])
        for a, b in _edges(pc):
            L2 = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
            ts = sorted({0.0, 1.0} | {((v[0] - a[0]) * (b[0] - a[0]) + (v[1] - a[1]) * (b[1] - a[1])) / L2
                                     for v in verts if _pt_seg(v, a, b) <= tol})
            for t0, t1 in zip(ts, ts[1:]):
                if t1 - t0 < 1e-12:
                    continue
                p0 = (round(a[0] + (b[0] - a[0]) * t0, 6), round(a[1] + (b[1] - a[1]) * t0, 6))
                p1 = (round(a[0] + (b[0] - a[0]) * t1, 6), round(a[1] + (b[1] - a[1]) * t1, 6))
                k = frozenset((p0, p1))
                subs.setdefault(k, []).append((p0, p1))
    edges = [v[0] for v in subs.values() if len(v) == 1]
    if not edges:
        return None
    nxt = {}
    for p0, p1 in edges:
        if p0 in nxt:
            return None
        nxt[p0] = p1
    start = edges[0][0]
    ring, cur = [start], nxt[start]
    while cur != start:
        if cur not in nxt or len(ring) > len(edges):
            return None
        ring.append(cur)
        cur = nxt[cur]
    if len(ring) != len(edges):
        return None
    out = []
    for i, q in enumerate(ring):
        a, b = ring[i - 1], ring[(i + 1) % len(ring)]
        if abs((q[0] - a[0]) * (b[1] - a[1]) - (q[1] - a[1]) * (b[0] - a[0])) > tol:
            out.append(q)
    return out


def outline_matches_issue(ax, ctx, pose, fid):
    """K8 outline_matches (r4, Designer sign-off r3): the <fid>:outline Polygon, through its artist transform, has the
    vertex ring of the boundary of the union of the row's plan_poly pieces: same vertex count, same orientation, every
    vertex within TOL_Z of its partner under one cyclic shift. Returns a list of issue texts."""
    arts = tagged(ax).get(fid + OUTLINE_SUFFIX, [])
    if not arts:
        return ["no outline sub-artist drawn"]
    pcs = _feat(ctx, pose, fid).get("plan_pieces") or []
    want = union_boundary(pcs)
    if want is None:
        return ["plan_poly pieces do not close into one boundary ring"]
    out = []
    for a in arts:
        got = artist_polys(a)[0]
        if len(got) != len(want):
            out.append(f"outline has {len(got)} vertices, the union boundary {len(want)}")
            continue
        if (poly_area(got) > 0) != (poly_area(want) > 0):
            out.append("outline runs clockwise, the union boundary counter-clockwise")
            continue
        best = min(max(math.hypot(got[(i + k) % len(got)][0] - want[i][0], got[(i + k) % len(got)][1] - want[i][1])
                       for i in range(len(want))) for k in range(len(got)))
        if best > TOL_Z:
            out.append(f"outline vertices off the union boundary by {best:.2f}")
    return out


def ticks_radial_issue(ax, fid, pr, P):
    """K8 ticks_radial (1.2 (h), Designer M1 r1 F1 premise): the row's <fid>:ticks LineCollection, through its artist
    transform, holds exactly `count` segments; each lies on a radius (the line through its ends passes within TOL_Z of
    the drill axis, and its ends lie on one side of it) with both ends between r_in - TOL_Z and r_out + TOL_Z.
    Returns a list of issue texts."""
    arts = tagged(ax).get(fid + TICKS_SUFFIX, [])
    if not arts:
        return ["no tick sub-artist drawn"]
    import check_stack as cs  # stdlib + sketch_loader only; no cycle
    r_in, r_out = cs.eval_expr(pr["r_in"], P, {}), cs.eval_expr(pr["r_out"], P, {})
    want = int(round(cs.eval_expr(pr["count"], P, {})))
    segs = [poly for a in arts for poly in artist_polys(a)]
    out = []
    if len(segs) != want:
        out.append(f"{len(segs)} ticks drawn, count {pr['count']} = {want}")
    for i, poly in enumerate(segs):
        if len(poly) != 2:
            out.append(f"tick {i} has {len(poly)} points, needs 2")
            continue
        (x0, y0), (x1, y1) = poly
        L = math.hypot(x1 - x0, y1 - y0)
        if L < 1e-9:
            out.append(f"tick {i} has zero length")
            continue
        off = abs(x0 * y1 - x1 * y0) / L
        same_side = (x0 * x1 + y0 * y1) > 0
        ra, rb = math.hypot(x0, y0), math.hypot(x1, y1)
        if off > TOL_Z or not same_side:
            out.append(f"tick {i} not radial: its line passes {off:.2f} from the drill axis")
        if min(ra, rb) < r_in - TOL_Z or max(ra, rb) > r_out + TOL_Z:
            out.append(f"tick {i} r [{min(ra, rb):.2f}, {max(ra, rb):.2f}] outside [{r_in:.2f}, {r_out:.2f}]")
    return out


def expected_projection(kind, axis, normal):
    if normal is None or axis is None:
        return None
    if kind in ("cylinder", "screw"):
        return "circle" if axis == normal else "rectangle"
    if kind in ("cone", "gear"):
        return "circle" if axis == normal else "trapezoid"
    return None


def zero_area_issue(row, a):
    """TP1.1-9 (1.3 step 0 R5 a; Topologist P0T FIX 1): on a row whose kind draws an area (not line, arrow or callout),
    (1) a non-Patch artist (Line2D, Collection) under the row's own id draws no area and fails; (2) a Patch whose least
    drawn thickness (least_thickness: least 2A/P over its pieces in data coordinates, transform chain applied; Annulus:
    radial width of the transformed rings) is <= TOL_Z (0.05 mm) is no projection of a solid part and fails."""
    kind = row.get("kind")
    if kind in NO_AREA_KINDS:
        return None
    if not isinstance(a, Patch):   # Topologist P0T FIX 1 (c): a line under a part row's own id draws no area
        return f"{type(a).__name__} on a {kind} row draws no area (TP1.1-9)"
    t = least_thickness(a)
    if t <= TOL_Z:
        return f"zero-area {type(a).__name__} (least thickness {t:.4f} mm <= {TOL_Z}) on a {kind} row (TP1.1-9)"
    return None


def _perimeter(P):
    return sum(math.hypot(P[(i + 1) % len(P)][0] - P[i][0], P[(i + 1) % len(P)][1] - P[i][1]) for i in range(len(P)))


def least_thickness(a):
    """Topologist P0T FIX 1 (a): least drawn thickness of a patch in data coordinates (transform chain applied). Annulus:
    radial width, from the transformed rings (outer minus inner mean radius about the ring centre). Any other patch: the
    least 2A/P over its pieces (a w x h rectangle gives wh / (w + h), the short side to first order); a piece with fewer
    than three distinct vertices, or no piece, is 0."""
    polys = [p for p in artist_polys(a) if len(p) >= 1]
    if isinstance(a, Annulus) and len(polys) >= 2:
        rings = sorted(polys, key=lambda p: -poly_area_abs(p) if len(p) >= 3 else 0)[:2]
        cx = sum(x for x, _ in rings[0]) / len(rings[0])
        cy = sum(y for _, y in rings[0]) / len(rings[0])
        r = [sum(math.hypot(x - cx, y - cy) for x, y in q) / len(q) for q in rings]
        return abs(r[0] - r[1])
    ts = []
    for p in polys:
        per = _perimeter(p) if len(p) >= 2 else 0.0
        ts.append(0.0 if len(p) < 3 or per <= 0 else 2 * poly_area_abs(p) / per)
    return min(ts) if ts else 0.0


def k5(ctx):
    """1.2 (c) plan rules (TP-13): in plan_xy a row with axis X or Y is a radial-axis part (the spec's X means radial,
    as in S1). Premise: its place footprint is radial (spec lint). Its four-vertex pieces have a tangential edge pair at
    the placed azimuth (radial axis, RADIAL_TOL_DEG). A gear row's rectangle piece is admitted as its hub when it starts
    on the heel edge of the row's trapezoid piece and is no wider than the heel."""
    issues, n = [], 0
    rows_list = ctx.spec.get("features", [])
    rows = {r["id"]: r for r in rows_list}
    plan = ctx.view == "plan_xy"
    for r in rows_list:
        if r.get("kind") in ROUND_KINDS and r.get("axis") not in ("X", "Y", "Z"):
            issues.append(f"{r['id']}: spec error, {r.get('kind')} row needs axis X, Y or Z (has {r.get('axis')!r})")
        if plan and r.get("kind") in ROUND_KINDS and r.get("axis") in ("X", "Y"):
            fp = (r.get("place") or {}).get("footprint")
            if fp != "radial":
                issues.append(f"{r['id']}: spec error, radial-axis {r.get('kind')} row in plan_xy needs a radial place footprint (TP-13; has {fp!r})")
    normal = VIEW_NORMAL.get(ctx.view)
    for pose, fig in ctx.figs.items():
        drawn = tagged(fig.axes[0])
        for a in artists(fig.axes[0]):
            gid = a.get_gid()
            if not gid:
                issues.append(f"{pose}: untagged {type(a).__name__}")
                continue
            row = rows.get(gid)
            if row is None:
                if gid.endswith(TICKS_SUFFIX):
                    n += 1
                    t = ticks_admission_issue(rows.get(gid[:-len(TICKS_SUFFIX)]), a, plan, drawn.get(gid, []))
                    if t:
                        issues.append(f"{pose}/{gid}: {t}")
                elif gid.endswith(OUTLINE_SUFFIX):
                    n += 1
                    t = outline_admission_issue(rows.get(gid[:-len(OUTLINE_SUFFIX)]), a, plan, drawn.get(gid, []))
                    if t:
                        issues.append(f"{pose}/{gid}: {t}")
                continue
            n += 1
            za = zero_area_issue(row, a)
            if za:
                issues.append(f"{pose}/{gid}: {za}")
                continue
            want = expected_projection(row.get("kind"), row.get("axis"), normal)
            got = classify(a)
            spec_proj = row.get("projection")
            pl = _feat(ctx, pose, gid).get("place") if plan else None
            radial = plan and row.get("axis") in ("X", "Y") and pl is not None and pl.get("footprint") == "radial"
            if radial and got in ("rectangle", "trapezoid"):
                pts = artist_polys(a)[0]
                if len(_tangential_edges(pts, pl["theta"])) < 2:
                    issues.append(f"{pose}/{gid}: {got} not radial: no edge pair across the radial direction at theta {pl['theta']:g} (TP-13)")
                    continue
            if radial and got == "rectangle" and want == "trapezoid":
                traps = [artist_polys(t)[0] for t in drawn.get(gid, []) if classify(t) == "trapezoid"]
                if traps:
                    th = pl["theta"]
                    ru, tu = zip(*to_ut(artist_polys(a)[0], th))
                    heel = max(max(u for u, _ in to_ut(tp, th)) for tp in traps)
                    heel_w = max(max(abs(t) for u, t in to_ut(tp, th) if abs(u - heel) <= TOL_Z) for tp in traps)
                    if abs(min(ru) - heel) <= TOL_Z and max(abs(t) for t in tu) <= heel_w + TOL_Z:
                        continue
                    issues.append(f"{pose}/{gid}: hub rectangle u [{min(ru):.2f}, {max(ru):.2f}], half-width {max(abs(t) for t in tu):.2f} "
                                  f"not on the heel of the toothed piece (u {heel:.2f}, half-width {heel_w:.2f})")
                    continue
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


def _plane_owner(field, lp, feat, sketch):
    """Name of another spec beside this file (s*_spec.yaml) that has row feat and carries field equal to lp after
    whitespace normalisation, else None."""
    norm = lambda d: {k: " ".join(str(v).split()) for k, v in (d or {}).items()}  # noqa: E731
    for p in sorted(HERE.glob("s*_spec.yaml")):
        name = p.stem.replace("_spec", "")
        if name == sketch:
            continue
        other = load_spec(p)
        if any(r["id"] == feat for r in other.get("features", [])) and norm(other.get(field)) == norm(lp):
            return name
    return None


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
    row_ids = {r["id"] for r in ctx.spec.get("features", [])}
    for field, lp in fields:
        if not lp:
            continue
        term, feat, edge = lp.get("term"), lp.get("feature"), lp.get("edge", "z_max")
        if term not in glob:
            issues.append(f"LF-16 {field}: term {term!r} is not a stack name")
            continue
        if feat not in row_ids and field in PLANE_FIELDS:
            # 1.2 (c): the field names a feature that is a row of another sketch (S2 carries the S1 park-rule planes for
            # check_stack; core_seat and collar are S1 rows). The agreement is linted where the row is drawn; premise:
            # a spec with that row carries the same field, equal after whitespace normalisation (K6-B9).
            owner = _plane_owner(field, lp, feat, ctx.spec.get("sketch"))
            if owner is None:
                issues.append(f"LF-16 {field}: feature {feat!r} is not a row of this spec and no other spec with that row carries an equal {field}")
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
    if ctx.view == "plan_xy":
        return _k6_plan(ctx, issues)
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


def plan_centre(ctx, row, pose):
    """K6 plan basis (1.2 (c)): ('ut', r_c, theta) for a placed row (centre compared in the radial frame: the drawn u
    mid-extent equals r_c and the t mid-extent is 0, which holds for rectangles, trapezoids symmetric about their axis,
    circles and footprints turned about their centre); ('xy', cx, cy) for a plan_poly row (mid-extent of its pieces), a
    sector (mid-extent of the wedge) or an axis-Z section or depth-band row (the drill axis); None (no plan basis)."""
    rec = _feat(ctx, pose, row["id"])
    pl = rec.get("place")
    if pl:
        return ("ut", pl["r_c"], pl["theta"])
    if rec.get("plan_pieces"):
        b = bbox(rec["plan_pieces"])
        return ("xy", (b[0] + b[1]) / 2, (b[2] + b[3]) / 2)
    if rec.get("sector"):
        s = rec["sector"]
        return ("xy", (s["x"][0] + s["x"][1]) / 2, (s["y"][0] + s["y"][1]) / 2)
    dep = rec.get("depth")
    if row.get("section") or (dep and row.get("kind") in ROUND_KINDS and row.get("axis") == "Z" and abs(dep[0] + dep[1]) < 1e-9):
        return ("xy", 0.0, 0.0)
    return None


def _k6_plan(ctx, issues):
    """K6 in plan_xy (1.2 (c)): z bands are not drawn in plan, so K6 asserts the z stack only through its spec lints
    (plane agreement, stack ties, check_stack anchors and import guard, above) and asserts placement in x and y: every
    row with a plan basis (plan_centre) is drawn with its centre on the spec centre within TOL_Z. Extent containment is
    K8 (plan outline containment)."""
    worst, n, absent = 0.0, 0, 0
    rows_list = ctx.spec.get("features", [])
    for pose, fig in ctx.figs.items():
        ax = fig.axes[0]
        for row in rows_list:
            if not applies(row, pose):
                continue
            basis = plan_centre(ctx, row, pose)
            if basis is None:
                continue
            n += 1
            me = pieces(ax, row["id"])
            if not me:
                issues.append(f"{pose}/{row['id']}: plan centre from the spec, nothing drawn")
                absent += 1
                continue
            if basis[0] == "ut":
                b = bbox([to_ut(p, basis[2]) for p in me])
                du, dt = (b[0] + b[1]) / 2 - basis[1], (b[2] + b[3]) / 2
                d = math.hypot(du, dt)
                txt = f"drawn centre u {(b[0] + b[1]) / 2:.2f}, t {dt:.2f} vs r_c {basis[1]:.2f}, t 0 at theta {basis[2]:g}"
            else:
                b = bbox(me)
                cx, cy = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2
                d = math.hypot(cx - basis[1], cy - basis[2])
                txt = f"drawn centre ({cx:.2f}, {cy:.2f}) vs spec ({basis[1]:.2f}, {basis[2]:.2f})"
            worst = max(worst, d)
            if d > TOL_Z:
                issues.append(f"{pose}/{row['id']}: {txt}, off {d:.2f}")
    return result("K6", not issues, _summ(issues) if issues else f"{n} plan centre(s) on the spec within {TOL_Z} mm (z not drawn in plan); check_stack imports and anchors clean",
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


K7_TEST_FIELDS = ["pose", "pair", "class", "state", "z_gap", "distance", "overlap", "basis"]


def _r3(v):
    return None if v is None else round(float(v), 3)


def _side_measure(st, lb, fp="plan footprint (spec placement, exact)"):
    """(distance, overlap, basis) of a side-view K7 judgement from its state and lower bound (assess_pair). r3 (Loftsman
    re-check r2 NOTE R2-2): a depth-separated entry carries no distance (null; the basis says depth band), and a plan
    footprint basis names a circumscribed 128-gon (fp from _fp_basis)."""
    if lb is None:
        return None, None, "declared N" if st == "N" else "none"
    d, a = (float(lb), 0.0) if lb >= 0 else (0.0, float(-lb))
    if st == "depth-separated":
        return None, None, "depth band"
    if st in ("plan-separated", "plan-contact"):
        return d, a, fp
    return d, a, "XZ projection (exact)"


def _fp_basis(ctx, pose, a, b):
    """Basis of a side-view plan-footprint distance: circumscribed 128-gon when either row's footprint is round or a
    depth-band disk (plan_footprint), else the exact spec placement (radial corners, one plan_poly piece)."""
    for fid in (a, b):
        rec = _feat(ctx, pose, fid)
        pl = rec.get("place")
        if (pl and pl.get("footprint") != "radial") or (not pl and not rec.get("plan_pieces")):
            return "plan footprint (circumscribed 128-gon)"
        if not pl and len(rec.get("plan_pieces") or []) > 1:
            return "plan footprint (hull of plan_poly pieces)"
    return "plan footprint (spec placement, exact)"


def _plan_basis(OA, OB, need, st):
    """Basis of a plan K7 distance (Loftsman 1.2 (e) LF1.2-1): z band, box bound, circumscribed outline, depth disk, exact."""
    if st in ("z-separated", "z-touch"):
        return "z band"
    kinds = []
    for O in (OA, OB):
        if O[0] == "annulus" and not O[2] and O[1][0] == 0.0:
            kinds.append("depth disk")
        elif not O[2]:
            kinds.append("circumscribed outline")
    if kinds:
        return " + ".join(sorted(set(kinds)))
    if OA[0] == "polys" and OB[0] == "polys" and _bbox_gap(OA[1], OB[1]) > need + 1:
        return "box bound"
    return "exact"


def k7_record_issues(res):
    """Record lint (Loftsman 1.2 (e) LF1.2-1): a K7 result carries `tests`, one entry per state, each a list in the order
    of `test_fields` with a pose, a pair "a|b", a class, a state equal to the state list entry, and a basis."""
    out = []
    tests, states = res.get("tests"), res.get("states") or []
    if res.get("test_fields") != K7_TEST_FIELDS:
        out.append(f"K7 record: test_fields {res.get('test_fields')!r}, want {K7_TEST_FIELDS}")
    if tests is None:
        return out + ["K7 record: no per-test entries (tests)"]
    if len(tests) != len(states):
        out.append(f"K7 record: {len(tests)} test entries for {len(states)} states")
    for i, t in enumerate(tests):
        if not isinstance(t, (list, tuple)) or len(t) != len(K7_TEST_FIELDS):
            out.append(f"K7 record: entry {i} is not a {len(K7_TEST_FIELDS)}-field list")
            continue
        e = dict(zip(K7_TEST_FIELDS, t))
        miss = [k for k in ("pose", "pair", "class", "state", "basis") if not e[k]]
        if miss or "|" not in str(e["pair"]):
            out.append(f"K7 record: entry {i} lacks {miss or ['pair a|b']}")
        elif i < len(states) and e["state"] != states[i]:
            out.append(f"K7 record: entry {i} state {e['state']!r} differs from states[{i}] {states[i]!r}")
    return out


def k7(ctx):
    rows_list = ctx.spec.get("features", [])
    rows = {r["id"]: r for r in rows_list}
    side = ctx.view in SIDE_VIEWS
    issues, states, tested, failing, absent = [], [], 0, 0, 0
    tests = []

    def log(pose, a, b, cls, st, gap, lb):
        d, ar, basis = _side_measure(st, lb, _fp_basis(ctx, pose, a, b))
        states.append(st)
        tests.append([pose, f"{a}|{b}", cls, st, _r3(gap), _r3(d), _r3(ar), basis])
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
    if ctx.view == "plan_xy":
        return _k7_plan(ctx, rows_list, rows, issues, failing)
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
                    log(pose, a, b, "N", "N", gap, None)
                    continue
                needs_draw = not (gap is not None and gap > 0 and nb["class"] in ("F", "G") and gap >= (nb.get("g_min") or 0) - TOL_C)
                if needs_draw and (not PA or not PB):
                    issues.append(f"{tag}: untestable, {'/'.join(x for x, p in ((a, PA), (b, PB)) if not p)} not drawn")
                    failing += 1
                    absent += 1
                    continue
                ok, st, txt, lb = assess_pair(nb["class"], nb.get("g_min"), PA, PB, gap, (a, b),
                                              plan_gap=plan_gap_fn(ctx, rows, pose, a, b) if side else None,
                                              plan_contact=plan_contact_fn(ctx, rows, pose, a, b) if side else None)
                tested += st not in ("depth-separated",)
                log(pose, a, b, nb["class"], st, gap, lb)
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
                    ok, st, txt, lb = assess_pair("F", 0, drawn[a], drawn[b], gap, (a, b),
                                                  plan_gap=plan_gap_fn(ctx, rows, pose, a, b) if side else None)
                    d, ar, basis = _side_measure(st, lb, _fp_basis(ctx, pose, a, b))
                    states.append(f"undeclared:{st}")
                    tests.append([pose, f"{a}|{b}", "F (undeclared)", f"undeclared:{st}", _r3(gap), _r3(d), _r3(ar), basis])
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
            # Loftsman 1.2 (c) NOTE 1 (1.3 step 0 R5 d): the moving row's neighbours, then every fixed row's entries that
            # name this row (read as the plan branch does), so a declaration written only on the fixed row is swept too;
            # the moving row's own entry comes first, and an N on either list excepts the pair
            nbs = list(row.get("neighbours") or [])
            for b, rb in rows.items():
                if b != a and not rb.get("moves"):
                    nbs += [dict(nb, id=b) for nb in rb.get("neighbours") or [] if nb.get("id") == a]
            unrestricted = {nb["id"] for nb in nbs if not nb.get("poses")}
            rel_n = {nb["id"] for nb in nbs if nb["class"] == "N"}
            seen_pr, seen_un = set(), set()
            for nb in nbs:
                b = nb["id"]
                if b not in rows or rows[b].get("moves") or b in rel_n:
                    continue
                if not nb.get("poses"):
                    if b in seen_un:   # the pair declared on both rows: the moving row's entry governs
                        continue
                    seen_un.add(b)
                if nb.get("poses"):
                    # LF-c1 (Loftsman 1.2 (c)): a pair declared at some poses only is undeclared at every swept
                    # position between them, so it is swept as F (g_min 0); a declaration of the pair without
                    # poses governs instead when there is one
                    if b in unrestricted or b in seen_pr:
                        continue
                    seen_pr.add(b)
                    nb = {"id": b, "class": "F", "g_min": 0}
                elif nb["class"] == "C":
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
                        tests.append([f"swept {lo}..{hi}", f"{a}|{b}", nb["class"], "swept:depth-separated", _r3(gap), None, None, "depth band"])
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
                ok, st, txt, lb = assess_pair(nb["class"], nb.get("g_min"), hulls, PB, gap, (f"{a} swept", b),
                                              plan_gap=plan_gap_fn(ctx, rows, lo, a, b) if side else None)
                tested += st not in ("depth-separated",)
                d, ar, basis = _side_measure(st, lb, _fp_basis(ctx, lo, a, b))
                states.append(f"swept:{st}")
                tests.append([f"swept {lo}..{hi}", f"{a}|{b}", nb["class"], f"swept:{st}", _r3(gap), _r3(d), _r3(ar), basis + " (swept hull)"])
                if not ok:
                    failing += 1
                    issues.append(f"{tag}: swept hull {txt}")
    return result("K7", not issues, _summ(issues) if issues else f"{tested} pair test(s) clean; states {sorted(set(states))}",
                  measured=failing, threshold=0, states=states, failing=failing, n_issues=len(issues), cause=_cause(absent, len(issues)),
                  test_fields=list(K7_TEST_FIELDS), tests=tests)


def _outline_diff(A, B):
    if A[0] != B[0]:
        return float("inf")
    if A[0] == "annulus":
        return max(abs(A[1][0] - B[1][0]), abs(A[1][1] - B[1][1]))
    if len(A[1]) != len(B[1]) or any(len(p) != len(q) for p, q in zip(A[1], B[1])):
        return float("inf")
    return max((math.hypot(p[0] - q[0], p[1] - q[1]) for P, Q in zip(A[1], B[1]) for p, q in zip(P, Q)), default=0.0)


def _k7_plan(ctx, rows_list, rows, issues, failing):
    """K7 in plan_xy (1.2 (c), LF-8). Geometry: each row's true XY outline from the spec (plan_outline; a row with no
    plan basis falls back to its drawn pieces). The drawing is held to the outline by K6 plan (centre) and K8 (every
    drawn point inside the outline), so the outline is a containment bound of the drawn part. Pairs are judged per
    stack pose with that pose's z bands (_plan_judge): disjoint z bands are listed z-separated (F; G when the z gap
    reaches g_min); C pairs pass as z-contact or plan-contact on true sections only. Presence: a pair not settled by its
    z bands is tested only when both rows are drawn (else untestable, absent). One plan figure (spec plan_figure): the
    figure serves every stack pose; premise: every row's plan outline is the same at every pose (lint below, 4f).
    Swept case: each moving row's outline against every fixed row (declared F or G without poses; undeclared, or
    declared with poses only, as F, LF-c1; N excepted)
    whose z band meets the sweep band (min to max of the moving row's z over the poses), Loftsman 1.2 (b) section 5."""
    states, tested, absent = [], 0, 0
    tests = []

    def log(pose, a, b, cls, st, gap, OA=None, OB=None, need=TOL_C):
        states.append(st)
        if OA is None or OB is None or st.split(":")[-1] in ("z-separated", "z-touch"):
            tests.append([pose, f"{a}|{b}", cls, st, _r3(gap), None, None,   # r3 NOTE R2-2: no distance on a z-band entry
                          "declared N" if st == "N" else "z band"])
            return
        d, ar = measure(OA, OB, need)
        tests.append([pose, f"{a}|{b}", cls, st, _r3(gap), _r3(d), _r3(ar), _plan_basis(OA, OB, need, st.split(":")[-1])])
    poses = list((ctx.stack or {}).get("poses", {})) or list(ctx.figs)
    one_fig = len(ctx.figs) < len(poses)
    out_cache, m_cache = {}, {}

    def zb(fid, pose):
        f = _feat(ctx, pose, fid)
        return [f["z_min"], f["z_max"]] if "z_min" in f else None

    def drawn(fid, pose):
        fig = plan_fig(ctx, pose)
        return fig is not None and bool(tagged(fig.axes[0]).get(fid))

    def outline(fid, pose):
        spec_o = plan_outline(ctx, rows[fid], pose) if ctx.stack else None
        key = (fid, None) if (spec_o is not None and one_fig) else (fid, pose)
        if key not in out_cache:
            if spec_o is None:
                fig = plan_fig(ctx, pose)
                pcs = pieces(fig.axes[0], fid) if fig is not None else []
                spec_o = ("polys", pcs, True) if pcs else None
            out_cache[key] = spec_o
        return out_cache[key]

    def measure(OA, OB, need):
        k = (id(OA), id(OB), need)
        if k not in m_cache:
            m_cache[k] = outline_measure(OA, OB, need)
        return m_cache[k]

    if one_fig and ctx.stack:   # 4f premise: one figure serves every pose only if plan outlines do not move
        for fid, row in rows.items():
            ref = None
            for pose in poses:
                if not applies(row, pose):
                    continue
                o = plan_outline(ctx, row, pose)
                if o is None:
                    break
                if ref is None:
                    ref = (pose, o)
                    continue
                d = _outline_diff(ref[1], o)
                if d > TOL_Z:
                    issues.append(f"{fid}: plan outline at {pose} differs from {ref[0]} by {d:.2f} mm; one plan figure needs pose-invariant plan positions")
                    failing += 1
                    break
    all_decl = set()   # pairs declared at every pose (LF-c1: a pose-restricted declaration leaves the pair undeclared in the sweep)
    for a, row in rows.items():
        for nb in row.get("neighbours") or []:
            if not nb.get("poses"):
                all_decl.add(frozenset((a, nb["id"])))
    for pose in poses:
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
                if nb["class"] == "N":
                    log(pose, a, b, "N", "N", band_gap(zb(a, pose), zb(b, pose)))
                    continue
                gap = band_gap(zb(a, pose), zb(b, pose))
                if gap is not None and gap > TOL_C and nb["class"] in ("F", "G") and gap >= (nb.get("g_min") or 0) - TOL_C:
                    log(pose, a, b, nb["class"], "z-separated", gap)
                    continue
                missing = [x for x in (a, b) if not drawn(x, pose)]
                if missing:
                    issues.append(f"{tag}: untestable, {'/'.join(missing)} not drawn")
                    failing += 1
                    absent += 1
                    continue
                OA, OB = outline(a, pose), outline(b, pose)
                if OA is None or OB is None:
                    issues.append(f"{tag}: no plan outline for {'/'.join(x for x, o in ((a, OA), (b, OB)) if o is None)}")
                    failing += 1
                    continue
                ok, st, txt, _ = _plan_judge(nb["class"], nb.get("g_min"), OA, OB, gap, measure)
                tested += st != "z-separated"
                log(pose, a, b, nb["class"], st, gap, OA, OB, (nb.get("g_min") or 0) if nb["class"] == "G" else TOL_C)
                if not ok:
                    failing += 1
                    issues.append(f"{tag}: {txt}")
        if ctx.spec.get("undeclared_pairs", "F") == "F":
            ids = [r["id"] for r in rows_list if _measurable(r) and applies(r, pose) and drawn(r["id"], pose)]
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    a, b = ids[i], ids[j]
                    if frozenset((a, b)) in declared:
                        continue
                    gap = band_gap(zb(a, pose), zb(b, pose))
                    if gap is not None and gap > TOL_C:
                        log(pose, a, b, "F (undeclared)", "undeclared:z-separated", gap)
                        continue
                    OA, OB = outline(a, pose), outline(b, pose)
                    ok, st, txt, _ = _plan_judge("F", 0, OA, OB, gap, measure)
                    log(pose, a, b, "F (undeclared)", f"undeclared:{st}", gap, OA, OB)
                    if not ok:
                        failing += 1
                        issues.append(f"{pose}/{a}|{b} undeclared (F): {txt}")
    if len(poses) > 1 and ctx.stack:
        order = sorted(poses, key=lambda p: ctx.stack["poses"][p]["tip_z_S"])
        lo, hi = order[0], order[-1]
        for a, row in rows.items():
            if not row.get("moves"):
                continue
            za = [zb(a, p) for p in poses if applies(row, p)]
            if not za or not all(za):
                continue
            sweep = [min(z[0] for z in za), max(z[1] for z in za)]
            rel, rel_n = {}, set()
            for nb in row.get("neighbours") or []:
                if nb["class"] == "N":
                    rel_n.add(nb["id"])
                if not nb.get("poses"):
                    rel.setdefault(nb["id"], nb)
            for b, rb in rows.items():
                if b == a or rb.get("moves"):
                    continue
                for nb in rb.get("neighbours") or []:
                    if nb["id"] == a:
                        if nb["class"] == "N":
                            rel_n.add(b)
                        if not nb.get("poses"):
                            rel.setdefault(b, nb)
                nb = rel.get(b)
                if nb is not None:
                    if nb["class"] in ("C", "N"):
                        continue
                    cls, g = nb["class"], nb.get("g_min") or 0
                else:
                    # undeclared, or declared with poses only (LF-c1): F; N excepted
                    if b in rel_n or frozenset((a, b)) in all_decl or not (_measurable(row) and _measurable(rb)):
                        continue
                    cls, g = "F", 0
                zbb = zb(b, lo)
                gap = band_gap(sweep, zbb)
                tag = f"swept {lo}..{hi}/{a}|{b} {cls}"
                if gap is not None and gap > TOL_C and (cls == "F" or gap >= g - TOL_C):
                    log(f"swept {lo}..{hi}", a, b, cls, "swept:z-separated", gap)
                    continue
                if not (drawn(a, lo) and drawn(a, hi) and drawn(b, lo)):
                    issues.append(f"{tag}: untestable, not drawn")
                    failing += 1
                    absent += 1
                    continue
                OA = outline(a, lo) if (ctx.stack and plan_outline(ctx, row, lo) is not None) else None
                if OA is None:
                    PL, PH = pieces(plan_fig(ctx, lo).axes[0], a), pieces(plan_fig(ctx, hi).axes[0], a)
                    if len(PL) != len(PH):
                        issues.append(f"{tag}: {len(PL)} pieces at {lo}, {len(PH)} at {hi}; swept hull needs matching pieces")
                        failing += 1
                        continue
                    OA = ("polys", [convex_hull(list(p) + list(q)) for p, q in zip(PL, PH)], True)
                OB = outline(b, lo)
                ok, st, txt, _ = _plan_judge(cls, g, OA, OB, gap, measure)
                tested += 1
                log(f"swept {lo}..{hi}", a, b, cls, f"swept:{st}", gap, OA, OB, g if cls == "G" else TOL_C)
                if not ok:
                    failing += 1
                    issues.append(f"{tag}: swept outline {txt}")
    return result("K7", not issues, _summ(issues) if issues else f"{tested} plan pair test(s) clean over {len(poses)} pose(s); states {sorted(set(states))}",
                  measured=failing, threshold=0, states=states, failing=failing, n_issues=len(issues), cause=_cause(absent, len(issues)),
                  test_fields=list(K7_TEST_FIELDS), tests=tests)


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


COVER_SHRINK = 0.98    # vertex samples pulled 2 % toward the piece centre (Topologist 1.2 (e) section 7)
COVER_GRID = 12        # r3 (TP1.2-13): interior grid samples per bbox side, so a partly visible piece is found
COVER_RINGS = (0.02, 0.25, 0.5, 0.75, 0.98)   # annulus samples across the width
SOLID_STYLES = ("-", "solid", None)


COVER_STEP_MAX = 2.5   # r4 (TP1.2-16): grid step at most 2.5 mm, so a 5 mm visible strip gets samples
COVER_SAMPLES_MAX = 20000


def _piece_samples(poly):
    """Points strictly inside one closed convex piece: its vertices pulled COVER_SHRINK toward the centroid, and a grid
    over its bounding box kept where inside (r3, TP1.2-13). r4 (TP1.2-16): the grid step is the short side over
    COVER_GRID, capped at COVER_STEP_MAX, so a long thin piece (a 644 x 60 rail) is sampled finely along its length."""
    if len(poly) < 3:
        return []
    cx, cy = centroid([poly])
    out = [(cx + COVER_SHRINK * (x - cx), cy + COVER_SHRINK * (y - cy)) for x, y in poly]
    x0, x1, y0, y1 = bbox([poly])
    w, h = x1 - x0, y1 - y0
    step = max(min(min(w, h) / COVER_GRID, COVER_STEP_MAX), 1e-6)
    nx, ny = max(1, int(math.ceil(w / step))), max(1, int(math.ceil(h / step)))
    while nx * ny > COVER_SAMPLES_MAX:
        nx, ny = max(1, nx // 2), max(1, ny // 2)
    I, J = np.meshgrid(np.arange(nx, dtype=float), np.arange(ny, dtype=float), indexing="ij")
    gx, gy = (x0 + w * (I.ravel() + 0.5) / nx), (y0 + h * (J.ravel() + 0.5) / ny)
    m = _inside_np(poly, gx, gy)   # 1.3 P1R: vectorised, same test and order as _inside over the i, j loop
    out += list(zip(gx[m].tolist(), gy[m].tolist()))
    return out


def _inside_np(P, xs, ys):
    """_inside for arrays of points: the same convex half-plane test on ccw(P), inclusive within 1e-12."""
    xs, ys = np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)
    if len(P) < 3:
        return np.zeros(xs.shape, dtype=bool)
    C = ccw(P)
    n = len(C)
    m = np.ones(xs.shape, dtype=bool)
    for i in range(n):
        (ax_, ay_), (bx_, by_) = C[i], C[(i + 1) % n]
        m &= (bx_ - ax_) * (ys - ay_) - (by_ - ay_) * (xs - ax_) >= -1e-12
    return m


ANNULUS_ARC_STEP = 2.5   # 1.3 P1R (TP1.2-19): annulus samples step by arc length at the outer radius, at most 2.5 mm


def _annulus_samples(cx, cy, ri, ro):
    """Samples of an annulus about (cx, cy): along directions spaced by at most ANNULUS_ARC_STEP of arc at the outer
    radius (1.3 P1R, TP1.2-19; the r4 form stepped by outer-ring vertex), and across the width on m fractions evenly
    spaced from 0.02 to 0.98, m = max(5, ceil(width / ANNULUS_ARC_STEP) + 1), so the radial step is at most 2.5 mm as
    well (1.3 P1Rf, Topologist TP1.3-1; P1R used the five COVER_RINGS fractions, 27.5 mm apart on the ring)."""
    n = max(8, int(math.ceil(2 * math.pi * ro / ANNULUS_ARC_STEP)))
    m = max(len(COVER_RINGS), int(math.ceil((ro - ri) / ANNULUS_ARC_STEP)) + 1)
    lo, hi = COVER_RINGS[0], COVER_RINGS[-1]
    fs = list(COVER_RINGS) if m == len(COVER_RINGS) else [lo + (hi - lo) * k / (m - 1) for k in range(m)]
    out = []
    for i in range(n):
        t = 2 * math.pi * (i + 0.5) / n
        ux, uy = math.cos(t), math.sin(t)
        out += [(cx + (ro - f * (ro - ri)) * ux, cy + (ro - f * (ro - ri)) * uy) for f in fs]
    return out


def _cover_samples(a):
    """Points strictly inside a drawn area artist's geometry (its clip region not applied), in rendered data
    coordinates. An Annulus (outer and inner rings from artist_polys) by _annulus_samples; any other closed piece by
    _piece_samples."""
    polys = [p for p in artist_polys(a) if len(p) >= 3]
    if isinstance(a, Annulus) and len(polys) == 2:
        outer, inner = sorted(polys, key=poly_area_abs, reverse=True)
        cx, cy = centroid([outer])
        ri = sum(math.hypot(x - cx, y - cy) for x, y in inner) / len(inner)
        ro = sum(math.hypot(x - cx, y - cy) for x, y in outer) / len(outer)
        return _annulus_samples(cx, cy, ri, ro)
    return [p for poly in polys for p in _piece_samples(poly)]


def poly_area_abs(P):
    return abs(poly_area(P))


def is_solid(a):
    """A drawn artist reads as visible: solid line style, or a fill, or a hatch."""
    ls = a.get_linestyle()
    fill = bool(a.get_fill()) if isinstance(a, Patch) else False
    hatch = a.get_hatch() if isinstance(a, Patch) else None
    return (ls in SOLID_STYLES) or fill or bool(hatch)


def outline_contains(O, p, eps=1e-9):
    """True when p lies inside or on plan outline O (the fast form of outline_outside(O, p) <= eps)."""
    if O[0] == "annulus":
        a, b = O[1]
        r = math.hypot(*p)
        return a - eps <= r <= b + eps
    return any(len(q) >= 3 and _inside(p, q) for q in O[1])


def _outline_box(O):
    if O[0] == "annulus":
        b = O[1][1]
        return (-b, b, -b, b)
    return bbox(O[1])


def cover_table(ctx, pose):
    """Per measurable row at pose: its z_max and its true plan outline with bounding box (the cover candidates)."""
    rows = [r for r in ctx.spec.get("features", []) if applies(r, pose) and _measurable(r)]
    zmax = {r["id"]: _feat(ctx, pose, r["id"]).get("z_max") for r in rows}
    outl = {}
    for r in rows:
        o = plan_outline(ctx, r, pose)
        if o is not None and o[2] and zmax[r["id"]] is not None:
            outl[r["id"]] = (o, _outline_box(o))
    return rows, zmax, outl


def _covers_of(fid, zmax, outl):
    z = zmax.get(fid)
    if z is None:
        return []
    return [(oid, o, box) for oid, (o, box) in outl.items() if oid != fid and zmax[oid] is not None and zmax[oid] > z + TOL_Z]


def _covered_by(p, covers):
    for oid, o, (x0, x1, y0, y1) in covers:
        if x0 - 1e-9 <= p[0] <= x1 + 1e-9 and y0 - 1e-9 <= p[1] <= y1 + 1e-9 and outline_contains(o, p):
            return oid
    return None


# ------------------------------------------------------------------------ plan renderer (1.3 P1R)
# One entry point, render_plan(ctx, ax, pose), called once per plan figure after every row is drawn and before the
# labels. Visibility rule (gameplan K8 row, 1.3 P1R R1): a point of a drawn area artist is hidden when it lies inside
# the true plan outline (plan_outline true) of a row whose z_max is higher by more than TOL_Z, or inside an opaque fill
# (is_opaque, the alpha rule) of another row drawn above the artist. Premise: only true outlines cover (a circumscribing
# outline is a bound for K7 F and G, never a cover: K8-Z7, K8-B33); opacity per the alpha rule (K8 cover opacity lint,
# K8-B45). The covered region is exact: a union of covers is a union (slab decomposition below), an annulus outline is
# an annulus (its bore open), a convex piece is itself; circles of annulus outlines are polygons with sagitta at most
# RENDER_SAGITTA, the outer one inscribed and the bore one circumscribed, so the hidden region lies inside the true
# covered region. A partly hidden artist keeps its style and draws only inside its visible region (clip path); a hidden
# copy (dashed, or its own non-solid line style; no fill, no hatch) draws only inside its hidden region, inserted in the
# draw order right after it. A wholly hidden artist is restyled in place. Rows with plan_style: stand_in (Step 2
# stand-ins drawn dashed by convention) are drawn as styled.

RENDER_SAGITTA = 0.01   # mm: chord error of the polygon standing for an annulus outline circle in the renderer
RENDER_MARGIN = 5.0     # mm: the region box extends this far past the artist (strokes at its edge stay inside)
REGION_BUCKETS = 512


def _circle_ring(r, circumscribe=False):
    n = 16 if r <= RENDER_SAGITTA else max(16, int(math.ceil(math.pi / math.acos(1 - RENDER_SAGITTA / r))))
    R = r / math.cos(math.pi / n) if circumscribe else r
    return [(R * math.cos(2 * math.pi * i / n), R * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _seg_cross_xs(A, B):
    """x of every proper intersection between the edges in A and in B (numpy arrays n x 4, m x 4: x0, y0, x1, y1)."""
    px, py = A[:, 0][:, None], A[:, 1][:, None]
    rx, ry = (A[:, 2] - A[:, 0])[:, None], (A[:, 3] - A[:, 1])[:, None]
    qx, qy = B[:, 0][None, :], B[:, 1][None, :]
    sx, sy = (B[:, 2] - B[:, 0])[None, :], (B[:, 3] - B[:, 1])[None, :]
    den = rx * sy - ry * sx
    with np.errstate(divide="ignore", invalid="ignore"):
        t = ((qx - px) * sy - (qy - py) * sx) / den
        u = ((qx - px) * ry - (qy - py) * rx) / den
    ok = (np.abs(den) > 1e-12) & (t >= 0) & (t <= 1) & (u >= 0) & (u <= 1)
    return (px + t * rx)[ok]


def region_split(shapes, box):
    """Exact split of a box by a union of shapes (1.3 P1R, TP1.2-13). shapes: list of shapes, each a list of closed rings
    (membership even-odd within a shape: an annulus is its outer ring and its bore ring); the union is over shapes.
    box: (x0, x1, y0, y1), every shape inside it in y. Vertical slab decomposition: slab edges at every vertex x and every
    x where edges of two shapes cross, so inside a slab every edge is one straight line and the order of the crossings
    is fixed; the union is merged per slab at the slab middle. Returns (hidden, visible): disjoint vertical-sided
    trapezoids [(xa, ya_lo), (xb, yb_lo), (xb, yb_hi), (xa, ya_hi)] (counter-clockwise), the union and its complement
    in the box, merged along x where the bounding edges continue."""
    bx0, bx1, by0, by1 = box
    E = []
    for si, rings in enumerate(shapes):
        for ring in rings:
            n = len(ring)
            for i in range(n):
                (xa, ya), (xb, yb) = ring[i], ring[(i + 1) % n]
                if abs(xb - xa) > 1e-12:
                    E.append((xa, ya, xb, yb, si))
    if not E:
        return [], [[(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)]]
    arr = np.asarray(E, dtype=float)
    X0, Y0, X1, Y1, S = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3], arr[:, 4].astype(int)
    xmin, xmax = np.minimum(X0, X1), np.maximum(X0, X1)
    slope = (Y1 - Y0) / (X1 - X0)
    ev = [np.array([bx0, bx1]), X0, X1]
    sb = []
    for si in range(len(shapes)):
        idx = np.nonzero(S == si)[0]
        sb.append(None if not len(idx) else (idx, xmin[idx].min(), xmax[idx].max(),
                                             min(Y0[idx].min(), Y1[idx].min()), max(Y0[idx].max(), Y1[idx].max())))
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            a, b = sb[i], sb[j]
            if a is None or b is None or a[1] > b[2] or b[1] > a[2] or a[3] > b[4] or b[3] > a[4]:
                continue
            ev.append(_seg_cross_xs(arr[a[0], :4], arr[b[0], :4]))
    xs = np.unique(np.concatenate(ev))
    xs = xs[(xs >= bx0) & (xs <= bx1)]
    keep = np.concatenate([[True], np.diff(xs) > 1e-9])
    xs = xs[keep]
    xa_s, xb_s = xs[:-1], xs[1:]
    xm = (xa_s + xb_s) / 2
    recs = []
    for si, b in enumerate(sb):
        if b is None:
            continue
        idx = b[0]
        j0, j1 = int(np.searchsorted(xm, b[1], "right")), int(np.searchsorted(xm, b[2], "left"))
        if j1 <= j0:
            continue
        xmm = xm[j0:j1][:, None]
        act = (xmin[idx][None, :] < xmm) & (xmax[idx][None, :] > xmm)
        Y = np.where(act, Y0[idx][None, :] + (xmm - X0[idx][None, :]) * slope[idx][None, :], np.inf)
        order = np.argsort(Y, axis=1, kind="stable")
        Ys = np.take_along_axis(Y, order, 1)
        cnt = act.sum(1)
        for j in range(0, int(cnt.max()) - 1, 2):
            rows = np.nonzero(cnt >= j + 2)[0]
            if len(rows):
                recs.append(np.column_stack([rows + j0, Ys[rows, j], Ys[rows, j + 1], idx[order[rows, j]], idx[order[rows, j + 1]]]))
    R = np.concatenate(recs) if recs else np.zeros((0, 5))
    R = R[np.lexsort((R[:, 1], R[:, 0]))]

    def yat(e, x):
        if e == -1:
            return by0
        if e == -2:
            return by1
        return float(Y0[e] + (x - X0[e]) * slope[e])

    hid, vis, open_h, open_v = [], [], {}, {}
    k, nrec = 0, len(R)
    for s in range(len(xm)):
        xa, xb = float(xa_s[s]), float(xb_s[s])
        merged = []
        while k < nrec and int(R[k, 0]) == s:
            _, ylo, yhi, elo, ehi = R[k]
            if merged and ylo <= merged[-1][1] + 1e-12:
                if yhi > merged[-1][1]:
                    merged[-1][1], merged[-1][3] = yhi, int(ehi)
            else:
                merged.append([ylo, yhi, int(elo), int(ehi)])
            k += 1
        hs = [(m[2], m[3]) for m in merged]
        bounds = [-1] + [e for m in merged for e in (m[2], m[3])] + [-2]
        vs = [(bounds[i], bounds[i + 1]) for i in range(0, len(bounds), 2)]
        for keys, opn, out in ((hs, open_h, hid), (vs, open_v, vis)):
            nxt = {}
            for key in keys:
                if key in opn:
                    out[opn[key]][3] = xb
                    nxt[key] = opn[key]
                else:
                    out.append([key[0], key[1], xa, xb])
                    nxt[key] = len(out) - 1
            opn.clear()
            opn.update(nxt)

    def traps(lst):
        return [[(xa, yat(lo, xa)), (xb, yat(lo, xb)), (xb, yat(hi, xb)), (xa, yat(hi, xa))] for lo, hi, xa, xb in lst]
    return traps(hid), traps(vis)


def region_path(traps):
    """Compound Path of disjoint closed pieces (all counter-clockwise; the non-zero fill is their union)."""
    if not traps:
        return MPath(np.zeros((0, 2)))
    verts, codes = [], []
    for t in traps:
        verts += list(t) + [t[0]]
        codes += [MPath.MOVETO] + [MPath.LINETO] * (len(t) - 1) + [MPath.CLOSEPOLY]
    return MPath(np.asarray(verts, dtype=float), codes)


class RegionIndex:
    """Point membership in a region given as closed pieces (from a clip path): vertical-sided trapezoids by x bucket and
    linear bounds, any other piece by bounding box and crossing number. Membership is inclusive within eps."""

    def __init__(self, polys, eps=1e-9):
        self.eps = eps
        self.traps, self.polys = [], []
        for q in polys:
            q = [tuple(map(float, v)) for v in q]
            if len(q) > 1 and abs(q[0][0] - q[-1][0]) < 1e-12 and abs(q[0][1] - q[-1][1]) < 1e-12:
                q = q[:-1]
            if len(q) == 4 and abs(q[0][0] - q[3][0]) < 1e-9 and abs(q[1][0] - q[2][0]) < 1e-9 and q[1][0] > q[0][0]:
                self.traps.append((q[0][0], q[1][0], q[0][1], q[1][1], q[3][1], q[2][1]))
            elif len(q) >= 3:
                self.polys.append((bbox([q]), q))
        xs = [t[0] for t in self.traps] + [t[1] for t in self.traps] + [b[0] for b, _ in self.polys] + [b[1] for b, _ in self.polys]
        self.x0, self.x1 = (min(xs), max(xs)) if xs else (0.0, 1.0)
        self.w = max((self.x1 - self.x0) / REGION_BUCKETS, 1e-9)
        self.buckets = {}
        for i, t in enumerate(self.traps):
            for b in range(self._b(t[0] - eps), self._b(t[1] + eps) + 1):
                self.buckets.setdefault(b, []).append(i)

    def _b(self, x):
        return int(math.floor((x - self.x0) / self.w))

    def contains(self, p):
        x, y = p
        e = self.eps
        for i in self.buckets.get(self._b(x), ()):
            xa, xb, ya0, yb0, ya1, yb1 = self.traps[i]
            if xa - e <= x <= xb + e:
                f = 0.0 if xb - xa < 1e-15 else min(1.0, max(0.0, (x - xa) / (xb - xa)))
                if ya0 + f * (yb0 - ya0) - e <= y <= ya1 + f * (yb1 - ya1) + e:
                    return True
        for (x0, x1, y0, y1), q in self.polys:
            if x0 - e <= x <= x1 + e and y0 - e <= y <= y1 + e and _pip(p, q):
                return True
        return False


def _pip(p, ring):
    """Crossing-number point-in-polygon (any simple ring)."""
    x, y = p
    c = False
    n = len(ring)
    for i in range(n):
        x0, y0 = ring[i]
        x1, y1 = ring[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c


def drawn_region(a):
    """RegionIndex of an artist's own clip path in data coordinates, or None when it has none (the axes box only): the
    region a renderer piece draws in (1.3 P1R). Read from the figure (Artist.get_clip_path), cached per clip path."""
    cp = a.get_clip_path()
    if cp is None or a.axes is None:
        return None
    path = cp._path if hasattr(cp, "_path") else cp.get_fully_transformed_path()
    cache = getattr(a, "_sc_region", None)
    if cache is not None and cache[0] is path:
        return cache[1]
    T = getattr(cp, "_transform", None)
    if T is a.axes.transData:
        data = path
    else:
        full = cp.get_fully_transformed_path()
        data = MPath(a.axes.transData.inverted().transform(full.vertices), full.codes)
    reg = RegionIndex(data.to_polygons(closed_only=False))
    a._sc_region = (path, reg)
    return reg


def cover_context(ctx, ax, pose):
    """What the visibility rule reads at pose: cover_table (true outlines, z_max), the draw order, the opaque fills."""
    rows, zmax, outl = cover_table(ctx, pose)
    rank = _rank(ax)
    opaque = [(a, [q for q in artist_polys(a) if len(q) >= 3]) for a in artists(ax) if a.get_gid() and is_opaque(a)]
    return {"rows": rows, "zmax": zmax, "outl": outl, "rank": rank, "drawn": tagged(ax),
            "opaque": [(a, polys, bbox(polys)) for a, polys in opaque if polys]}


def artist_covers(cc, a, fid):
    """Covers of one drawn area artist of row fid: ('ann', id, (r_in, r_out), box) for an annulus outline, ('poly', id,
    piece, box) per convex piece of a polys outline (true outlines of rows higher by more than TOL_Z), and ('patch', id,
    (artist, rings), box) per opaque fill of another row drawn above a (as drawn: even-odd rings, clip region)."""
    out = []
    for oid, o, box in _covers_of(fid, cc["zmax"], cc["outl"]):
        if o[0] == "annulus":
            out.append(("ann", oid, o[1], box))
        else:
            out += [("poly", oid, q, bbox([q])) for q in o[1] if len(q) >= 3]
    ra = cc["rank"].get(id(a), (-1e9, -1))
    for o_a, polys, box in cc["opaque"]:
        g = o_a.get_gid()
        if g == fid or g.startswith(fid + ":") or cc["rank"].get(id(o_a), (-1e9, -1)) <= ra:
            continue
        out.append(("patch", g, (o_a, polys), box))
    return out


def _edge_depth(p, polys):
    return min((_pt_seg(p, q[i], q[(i + 1) % len(q)]) for q in polys for i in range(len(q))), default=0.0)


def cover_hit(p, covers, deep=None):
    """(id of the first cover containing p or None, True when some cover contains p by more than deep). Containment is
    inclusive (a point on a cover's boundary is covered)."""
    hit, is_deep = None, False
    for kind, oid, data, (x0, x1, y0, y1) in covers:
        if not (x0 - 1e-9 <= p[0] <= x1 + 1e-9 and y0 - 1e-9 <= p[1] <= y1 + 1e-9):
            continue
        if kind == "ann":
            a, b = data
            r = math.hypot(*p)
            if not (a - 1e-9 <= r <= b + 1e-9):
                continue
            d = (b - r) if a <= 0 else min(r - a, b - r)
        elif kind == "poly":
            if not _inside(p, data):
                continue
            d = None
        else:
            if not in_drawn(data[0], p, data[1]):
                continue
            d = None
        hit = hit or oid
        if deep is None:
            return hit, False
        if d is None:
            d = _edge_depth(p, [data] if kind == "poly" else data[1])
        if d > deep:
            return hit, True
    return hit, is_deep


def _seg_dist_np(xs, ys, a, b):
    ax_, ay_ = a
    dx, dy = b[0] - ax_, b[1] - ay_
    L2 = dx * dx + dy * dy
    t = np.zeros_like(xs) if L2 < 1e-24 else np.clip(((xs - ax_) * dx + (ys - ay_) * dy) / L2, 0.0, 1.0)
    return np.hypot(xs - (ax_ + t * dx), ys - (ay_ + t * dy))


def in_drawn_np(a, polys, xs, ys):
    """in_drawn for arrays of points (even-odd over the closed rings, then the clip region)."""
    cnt = np.zeros(xs.shape, dtype=int)
    for q in polys:
        if len(q) >= 3:
            cnt += _inside_np(q, xs, ys)
    m = cnt % 2 == 1
    reg = drawn_region(a)
    if reg is not None and m.any():
        idx = np.nonzero(m)[0]
        m[idx] = [reg.contains((float(xs[i]), float(ys[i]))) for i in idx]
    return m


def cover_hits(pts, covers, deep=None):
    """cover_hit for a list of points, vectorised: (ids of the first cover containing each point or None, flags: some
    cover contains the point by more than deep)."""
    N = len(pts)
    if not N:
        return [], []
    X = np.fromiter((p[0] for p in pts), float, N)
    Y = np.fromiter((p[1] for p in pts), float, N)
    hit = np.full(N, -1)
    dp = np.zeros(N, dtype=bool)
    for ci, (kind, oid, data, (x0, x1, y0, y1)) in enumerate(covers):
        cand = (X >= x0 - 1e-9) & (X <= x1 + 1e-9) & (Y >= y0 - 1e-9) & (Y <= y1 + 1e-9)
        cand &= (hit < 0) if deep is None else ~dp
        if not cand.any():
            continue
        idx = np.nonzero(cand)[0]
        x, y = X[idx], Y[idx]
        d = None
        if kind == "ann":
            a, b = data
            r = np.hypot(x, y)
            m = (r >= a - 1e-9) & (r <= b + 1e-9)
            d = (b - r) if a <= 0 else np.minimum(r - a, b - r)
            rings = None
        elif kind == "poly":
            m = _inside_np(data, x, y)
            rings = [data]
        else:
            m = in_drawn_np(data[0], data[1], x, y)
            rings = data[1]
        sel = idx[m]
        if not len(sel):
            continue
        hit[sel[hit[sel] < 0]] = ci
        if deep is not None:
            if d is None:
                xs_, ys_ = X[sel], Y[sel]
                dd = np.full(len(sel), np.inf)
                for q in rings:
                    for i in range(len(q)):
                        dd = np.minimum(dd, _seg_dist_np(xs_, ys_, q[i], q[(i + 1) % len(q)]))
            else:
                dd = d[m]
            dp[sel[dd > deep]] = True
    return [covers[h][1] if h >= 0 else None for h in hit.tolist()], dp.tolist()


def _hidden_linestyle(a):
    ls = a.get_linestyle()
    return "--" if ls in SOLID_STYLES else ls


def _restyle_hidden(a):
    a.set_linestyle(_hidden_linestyle(a))
    if isinstance(a, Patch):
        a.set_fill(False)
        a.set_hatch(None)


def _patch_copy(a):
    """A new patch with a's geometry (same class where the class carries it: Polygon, Circle, Annulus, Rectangle)."""
    ax = a.axes
    plain = ax is not None and isinstance(a, (Circle, Annulus, Rectangle, Ellipse)) and \
        a.get_transform() == a.get_patch_transform() + ax.transData
    if isinstance(a, Polygon) and ax is not None and a.get_transform() == ax.transData:
        return Polygon(np.asarray(a.get_xy(), dtype=float), closed=a.get_closed())
    if plain and isinstance(a, Annulus):
        return Annulus(a.get_center(), a.get_radii(), a.get_width(), angle=a.get_angle())
    if plain and isinstance(a, Circle):
        return Circle(a.get_center(), a.get_radius())
    if plain and isinstance(a, Rectangle):
        return Rectangle(a.get_xy(), a.get_width(), a.get_height(), angle=a.get_angle())
    from matplotlib.patches import PathPatch
    return PathPatch(a.get_path().transformed(_to_data(a)))


def _cover_shapes(covers):
    """Renderer shapes (closed rings, even-odd per shape) of covers: an annulus outline by its polygons (outer
    inscribed, bore circumscribed), a convex piece as itself, an opaque fill by its rings, or, when the fill is a renderer
    piece with a clip region, by its rings intersected with each convex clip piece."""
    shapes = []
    for kind, oid, data, box in covers:
        if kind == "ann":
            a, b = data
            shapes.append([_circle_ring(b)] + ([_circle_ring(a, circumscribe=True)] if a > 0 else []))
        elif kind == "poly":
            shapes.append([data])
        else:
            o_a, polys = data
            reg = drawn_region(o_a)
            if reg is None:
                shapes.append(polys)
            else:
                outer = max(polys, key=poly_area_abs)
                for t in reg.traps:
                    q = [(t[0], t[2]), (t[1], t[3]), (t[1], t[5]), (t[0], t[4])]
                    c = clip(q, outer)
                    if len(c) >= 3:
                        shapes.append([c])
    return shapes


def _rendered_rows(ctx, pose):
    return [r for r in ctx.spec.get("features", []) if applies(r, pose) and _measurable(r) and r.get("plan_style") != "stand_in"]


def render_plan(ctx, ax, pose):
    """Plan hidden-line renderer (1.3 P1R R1, R2): the single entry point a plan script calls per figure, after every
    row is drawn and before the labels. Every area artist (Patch) of a measurable row that is not a stand-in is taken
    from the top of the draw order down (so the opaque fills above an artist are final when it is taken): no covered
    sample, unchanged; every sample covered, restyled in place (hidden line style, no fill, no hatch); otherwise split:
    the artist keeps its style and gets the visible region as its clip path, and a hidden copy (hidden line style, no
    fill, no hatch, same edge colour and width) gets the hidden region and is inserted in the draw order right after it.
    Samples as K8 cover (_cover_samples). Returns {artist: (row id, 'visible' | 'hidden' | 'split', cover ids)}."""
    cc = cover_context(ctx, ax, pose)
    rows = {r["id"] for r in _rendered_rows(ctx, pose)}
    todo = [a for g in rows for a in cc["drawn"].get(g, []) if isinstance(a, Patch) and a.get_clip_path() is None
            and not getattr(a, "_sc_hidden_copy", False)]   # a second call takes only pieces not yet split
    todo.sort(key=lambda a: cc["rank"][id(a)], reverse=True)
    out = {}
    for a in todo:
        fid = a.get_gid()
        covers = artist_covers(cc, a, fid)
        pts = _cover_samples(a)
        hits = cover_hits(pts, covers)[0]
        by = {h for h in hits if h}
        if not by:
            out[a] = (fid, "visible", by)
            continue
        if all(hits):
            _restyle_hidden(a)
            cc["opaque"] = [o for o in cc["opaque"] if o[0] is not a]   # no longer a fill over what lies under it
            out[a] = (fid, "hidden", by)
            continue
        polys = [q for q in artist_polys(a) if len(q) >= 3]
        x0, x1, y0, y1 = bbox(polys)
        box = (x0 - RENDER_MARGIN, x1 + RENDER_MARGIN, y0 - RENDER_MARGIN, y1 + RENDER_MARGIN)
        near = [c for c in covers if not (c[3][0] > box[1] or c[3][1] < box[0] or c[3][2] > box[3] or c[3][3] < box[2])]
        shapes = _cover_shapes(near)
        ys = [v[1] for s in shapes for ring in s for v in ring]
        box = (box[0], box[1], min([box[2]] + ys) - RENDER_MARGIN, max([box[3]] + ys) + RENDER_MARGIN)
        hid, vis = region_split(shapes, box)
        cp = _patch_copy(a)
        cp.set_edgecolor(a.get_edgecolor())
        cp.set_linewidth(a.get_linewidth())
        cp.set_linestyle(_hidden_linestyle(a))
        cp.set_fill(False)
        cp.set_hatch(None)
        cp.set_zorder(a.get_zorder())
        cp._sc_hidden_copy = True
        a.set_clip_path(region_path(vis), ax.transData)
        draw(fid, cp, ax)
        cp.set_clip_path(region_path(hid), ax.transData)
        kids = ax._children
        kids.remove(cp)
        kids.insert(kids.index(a) + 1, cp)
        out[a] = (fid, "split", by)
    return out


def plan_cover_states(ctx, ax, pose):
    """{artist: (row id, state, covering ids, uncovered sample points)} for every drawn area artist of a measurable row in
    plan (Line2D pieces and reference rows out), on the samples inside the artist's drawn region (its clip region):
    'hidden' when every such sample is covered, 'visible' when none is, else 'partial'."""
    cc = cover_context(ctx, ax, pose)
    out = {}
    for r in cc["rows"]:
        for a in cc["drawn"].get(r["id"], []):
            if isinstance(a, Line2D):
                continue
            covers = artist_covers(cc, a, r["id"])
            reg = drawn_region(a)
            pts = [p for p in _cover_samples(a) if reg is None or reg.contains(p)]
            hits = cover_hits(pts, covers)[0]
            by = {h for h in hits if h}
            open_pts = [p for p, h in zip(pts, hits) if h is None]
            st = "visible" if not pts or not by else ("hidden" if not open_pts else "partial")
            out[a] = (r["id"], st, by, open_pts)
    return out


def cover_issues(ctx, ax, pose, rows_list):
    """K8 cover (1.2 (h); Topologist TP1.2-2, TP1.2-9, TP1.2-13, TP1.2-15; Designer M1 r1 F2 rule; 1.3 P1R N2), plan
    view. Hidden: inside a true plan outline of a row with z_max higher by more than TOL_Z, or inside an opaque fill
    (alpha rule) of another row drawn above (1.3 P1R). Samples: interior grid plus pulled-in vertices of each piece,
    annulus rings by arc length (TP1.2-19); the drawn region of an artist is its geometry inside its clip region.
    (1) A solid artist (solid line, fill or hatch) whose every drawn sample is hidden fails. (2) 1.3 P1R (N2): a solid
    artist with a drawn sample hidden by more than TOL_Z (and some not hidden) fails: the covered part of a partly
    covered piece is drawn by the renderer as a hidden copy, not solid. (3) r3 converse: every uncovered sample of a
    non-solid artist's geometry lies in the drawn region of a solid artist of the same row under no opaque fill of
    another row drawn above that solid artist (TP1.2-15); rows with plan_style: stand_in and a stand_in_owner naming a
    Step or sketch id are out of (3). (4) 1.3 P1R premise of the alpha rule: no plan fill renders at an alpha between
    TRANSLUCENT_MAX and OPAQUE_ALPHA. Premise of the rule set: only true outlines (plan_outline true) cover (K8-Z7,
    K8-B33). (5) 1.3 P1Rf (TP1.3-2): an opaque fill of another row drawn above an artist and over one of its
    drawn samples belongs to a row with z_max at least the artist's z_max - TOL_Z (the draw order agrees with depth); a
    fill of a row without z_max hides nothing and fails here. Returns (artists tested, issues)."""
    rows = {r["id"]: r for r in rows_list}
    cc = cover_context(ctx, ax, pose)
    n, out = 0, []
    for a in artists(ax):
        g = a.get_gid()
        fa = fill_alpha(a)
        if g and TRANSLUCENT_MAX + 1e-9 < fa < OPAQUE_ALPHA - 1e-9:
            out.append(f"{pose}/{g} cover: fill alpha {fa:.2f} between {TRANSLUCENT_MAX:g} and {OPAQUE_ALPHA:g} (alpha rule "
                       f"premise: a fill is opaque or shows what is under it at half its contrast or more)")
    exempt = set()
    for fid, r in rows.items():
        if r.get("plan_style") == "stand_in":
            owner = str(r.get("stand_in_owner") or "").strip()
            if not owner:
                out.append(f"{pose}/{fid} cover: spec error, plan_style stand_in without stand_in_owner (TP1.2-17)")
            elif not STAND_IN_OWNER.search(owner):
                out.append(f"{pose}/{fid} cover: spec error, stand_in_owner {owner!r} names no Step id (Step 2) or sketch id (S3, s1 to s6) (TP1.2-18)")
            else:
                exempt.add(fid)
    solid_arts = {}
    for r in cc["rows"]:
        for a in cc["drawn"].get(r["id"], []):
            if not isinstance(a, Line2D) and is_solid(a):
                above = [c for c in artist_covers(cc, a, r["id"]) if c[0] == "patch"]
                solid_arts.setdefault(r["id"], []).append((a, [q for q in artist_polys(a) if len(q) >= 3], above))

    def shown(fid, pts):
        """Flags: each point lies in the drawn region of a solid artist of fid that no opaque fill of another row draws
        over (TP1.2-15)."""
        if not pts:
            return []
        X = np.fromiter((p[0] for p in pts), float, len(pts))
        Y = np.fromiter((p[1] for p in pts), float, len(pts))
        ok = np.zeros(len(pts), dtype=bool)
        for s_a, polys, above in solid_arts.get(fid, []):
            m = in_drawn_np(s_a, polys, X, Y) & ~ok
            if m.any():
                idx = np.nonzero(m)[0]
                h = cover_hits([pts[i] for i in idx], above)[0]
                ok[idx[[x is None for x in h]]] = True
        return ok.tolist()
    for r in cc["rows"]:
        fid = r["id"]
        for a in cc["drawn"].get(fid, []):
            if isinstance(a, Line2D):
                continue
            n += 1
            covers = artist_covers(cc, a, fid)
            reg = drawn_region(a)
            solid = is_solid(a)
            geo = _cover_samples(a)
            # (5) 1.3 P1Rf (Topologist TP1.3-2): an opaque fill hides only what lies behind it. An opaque fill of another
            # row drawn above the artist over a drawn sample belongs to a row whose z_max is not lower than the artist's
            # by more than TOL_Z; a fill of a row without z_max (a zone, a fixture row) hides nothing.
            zf = cc["zmax"].get(fid)
            inv = [c for c in covers if c[0] == "patch" and
                   (cc["zmax"].get(c[1]) is None or (zf is not None and cc["zmax"][c[1]] < zf - TOL_Z))]
            if inv:
                dpts = [p for p in geo if reg is None or reg.contains(p)]
                ih = cover_hits(dpts, inv)[0] if dpts else []
                bad = sorted({h for h in ih if h})
                if bad:
                    zs = ", ".join(f"{b} {cc['zmax'].get(b):.2f}" if cc["zmax"].get(b) is not None else f"{b} none" for b in bad)
                    out.append(f"{pose}/{fid} cover: opaque fill of {', '.join(bad)} drawn above it lies behind it or is no part "
                               f"(z_max {zs} against {fid} {'none' if zf is None else format(zf, '.2f')}); an opaque fill hides "
                               f"only what lies behind it (TP1.3-2)")
            if solid:
                pts = [p for p in geo if reg is None or reg.contains(p)]
                hits = list(zip(*cover_hits(pts, covers, deep=TOL_Z))) if pts else []
                by = {h for h, _ in hits if h}
                if pts and all(h for h, _ in hits):
                    out.append(f"{pose}/{fid} cover: {type(a).__name__} wholly under {', '.join(sorted(by))} drawn solid "
                               f"(linestyle {a.get_linestyle()!r}, fill {a.get_fill() if isinstance(a, Patch) else False}, "
                               f"hatch {a.get_hatch() if isinstance(a, Patch) else None!r}); a hidden part is dashed, no fill")
                elif any(d for _, d in hits):
                    deep = [p for p, (h, d) in zip(pts, hits) if d]
                    dby = {h for h, d in hits if d}
                    out.append(f"{pose}/{fid} cover: {type(a).__name__} partly covered drawn solid ({len(deep)} of {len(pts)} "
                               f"drawn samples under {', '.join(sorted(dby))} by more than {TOL_Z:g}, e.g. ({deep[0][0]:.2f}, "
                               f"{deep[0][1]:.2f})); the covered part is drawn hidden (dashed, no fill) by the renderer (N2)")
            elif fid not in exempt:
                open_pts = [p for p, h in zip(geo, cover_hits(geo, covers)[0]) if h is None]
                bare = [p for p, ok in zip(open_pts, shown(fid, open_pts)) if not ok]
                if bare:
                    out.append(f"{pose}/{fid} cover: {type(a).__name__} partly visible drawn dashed ({len(bare)} of "
                               f"{len(open_pts)} uncovered samples not shown by a solid piece of the row under no opaque fill, "
                               f"e.g. ({bare[0][0]:.2f}, {bare[0][1]:.2f})); its visible area is drawn solid")
    return n, out


def style_hidden(ctx, ax, pose):
    """r3 drawing helper, superseded at 1.3 P1R by render_plan (one renderer for scripts and fixtures). Returns
    plan_cover_states after rendering."""
    render_plan(ctx, ax, pose)
    return plan_cover_states(ctx, ax, pose)


def hidden_rows(ctx, pose):
    """Rows whose own plan outline lies wholly under true outlines of higher rows at pose (reports). 1.3 P1R (TP1.2-13):
    the outline is sampled as K8 cover samples a drawn piece (annulus by arc length, convex pieces by grid and pulled-in
    vertices) and each sample is tested against the exact covers (annulus as annulus, union as union)."""
    rows, zmax, outl = cover_table(ctx, pose)
    out = set()
    for r in rows:
        fid = r["id"]
        o = plan_outline(ctx, r, pose)
        covers = _covers_of(fid, zmax, outl)
        if o is None or not covers:
            continue
        if o[0] == "annulus":
            a, b = o[1]
            pts = _annulus_samples(0.0, 0.0, a, b)
        else:
            pts = [p for poly in o[1] for p in _piece_samples(poly)]
        if pts and all(_covered_by(p, covers) for p in pts):
            out.add(fid)
    return out


def k8(ctx):
    rows_list = ctx.spec.get("features", [])
    rows = {r["id"]: r for r in rows_list}
    lint, bad = sense_lint(rows_list)
    issues, n, absent = list(lint), 0, 0
    side, plan = ctx.view in SIDE_VIEWS, ctx.view == "plan_xy"
    # TP1.2-1: the radial outboard form reads the plan centroid (x, y) in the drill-axis frame; in a side view the
    # centroid is (x, z) and its hypot is no radius. frame: radial outside plan_xy is a spec error, reported once.
    if not plan:
        for fid, row in rows.items():
            for pr in row.get("sense") or []:
                if pr.get("pred") == "outboard" and pr.get("frame") == "radial" and id(pr) not in bad:
                    issues.append(f"{fid} outboard of {pr.get('of')}: spec error, frame radial needs plan_xy (view {ctx.view})")
                    bad.add(id(pr))
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
            # 1.2 (c) plan: every drawn point lies inside the row's plan outline (premise of the K7 plan test and of the
            # plan_poly and annulus outlines, 4g); the drawn centre is K6 plan. A sector is drawn equal to its wedge.
            if plan:
                po = plan_outline(ctx, row, pose) if ctx.stack else None
                sec = _feat(ctx, pose, fid).get("sector")
                if (po or sec) and not me:
                    issues.append(f"{pose}/{fid} plan_extent: untestable, {fid} not drawn")
                    absent += 1
                elif po:
                    n += 1
                    pts = [p for poly in me for p in poly]
                    d, p = max(((outline_outside(po, q), q) for q in pts), key=lambda e: e[0])
                    if d > TOL_Z:
                        issues.append(f"{pose}/{fid} plan_extent: drawn point ({p[0]:.2f}, {p[1]:.2f}) outside its plan outline (by {d:.2f})")
                elif sec:
                    n += 1
                    pts = [p for poly in me for p in poly]
                    d_out = max(sector_outside(sec, q) for q in pts)
                    d_in = max(min(min_distance([q], poly) if len(poly) >= 3 and not _inside(q, poly) else 0.0 for poly in me)
                               for q in sector_boundary(sec))
                    if d_out > TOL_Z or d_in > TOL_Z:
                        issues.append(f"{pose}/{fid} sector: drawn wedge differs from the spec wedge (theta {sec['theta']:g}, half-angle "
                                      f"{sec['half_angle']:g}, r {sec['r']:g}): {d_out:.2f} outside, spec boundary {d_in:.2f} outside the drawing")
            if pl and side:
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
                    # TP1.1-11 (r4): the whole drawn part lies inside its spec footprint's projection. K7 plan tests
                    # (plan-separated, plan-contact) read the spec footprint, so they hold only for a part it contains.
                    fx0, fx1 = pl["x"]
                    if ex[0] < fx0 - TOL_Z or ex[1] > fx1 + TOL_Z:
                        issues.append(f"{pose}/{fid} projected_extent: drawn x [{ex[0]:.2f}, {ex[1]:.2f}] outside the spec footprint x "
                                      f"[{fx0:.2f}, {fx1:.2f}] (by {max(fx0 - ex[0], ex[1] - fx1):.2f})")
                    if plan:
                        ey = extent_z(me)
                        wy = pl["r_c"] * math.sin(math.radians(pl["theta"]))
                        if abs((ey[0] + ey[1]) / 2 - wy) > TOL_Z:
                            issues.append(f"{pose}/{fid} projected_y: drawn y centre {(ey[0] + ey[1]) / 2:.2f} vs r_c sin(theta) {wy:.2f}")
                        fy0, fy1 = pl["y"]
                        if ey[0] < fy0 - TOL_Z or ey[1] > fy1 + TOL_Z:
                            issues.append(f"{pose}/{fid} projected_extent_y: drawn y [{ey[0]:.2f}, {ey[1]:.2f}] outside the spec footprint y [{fy0:.2f}, {fy1:.2f}]")
            # 1.2 (b): a plan_poly row with no place (guide tie) lies inside its plan pieces' extent: the premise of its
            # plan-separated and plan-contact relief in K7 (detail 1 common (h); K8-B17)
            pf = _feat(ctx, pose, fid)
            if not pl and pf.get("plan_x") and side and me:
                n += 1
                ex = extent_x(me)
                fx0, fx1 = pf["plan_x"]
                if ex[0] < fx0 - TOL_Z or ex[1] > fx1 + TOL_Z:
                    issues.append(f"{pose}/{fid} projected_extent: drawn x [{ex[0]:.2f}, {ex[1]:.2f}] outside the plan_poly x "
                                  f"[{fx0:.2f}, {fx1:.2f}] (by {max(fx0 - ex[0], ex[1] - fx1):.2f})")
                if plan:
                    ey = extent_z(me)
                    fy0, fy1 = pf["plan_y"]
                    if ey[0] < fy0 - TOL_Z or ey[1] > fy1 + TOL_Z:
                        issues.append(f"{pose}/{fid} projected_extent_y: drawn y [{ey[0]:.2f}, {ey[1]:.2f}] outside the plan_poly y [{fy0:.2f}, {fy1:.2f}]")
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
                elif kind == "outboard" and plan:
                    # 1.2 (c): radial form, the centroid farther from the drill axis than the other's (S2 rows carry
                    # frame: radial; at theta 90 the side form x cos(theta) reads 0)
                    ra, rb = math.hypot(*centroid(me)), math.hypot(*centroid(other))
                    if ra - rb <= 0:
                        issues.append(f"{pose}/{fid} outboard of {other_id} (radial): centroid radius {ra:.2f} vs {rb:.2f}, needs greater")
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
                elif kind == "taper" and plan and pl:
                    # 1.2 (c): plan form in the radial frame (u plays x, t plays z); the toothed trapezoid pieces only
                    # (a hub rectangle carries no taper)
                    tp = [to_ut(p, pl["theta"]) for p in me if len(p) == 4 and not _is_rect(p)]
                    t = taper_issue(tp, pr["narrows"]) if tp else "no four-vertex tapered piece drawn"
                    if t:
                        issues.append(f"{pose}/{fid} taper narrows {pr['narrows']} (radial frame): {t}")
                elif kind == "taper":
                    t = taper_issue(me, pr["narrows"])
                    if t:
                        issues.append(f"{pose}/{fid} taper narrows {pr['narrows']}: {t}")
                elif kind == "face_rises":
                    t = face_rises_issue(me, pr["toward"])
                    if t:
                        issues.append(f"{pose}/{fid} face_rises {pr['toward']}: {t}")
                elif kind == "ticks_radial":
                    for t in ticks_radial_issue(ax, fid, pr, ctx.P):
                        issues.append(f"{pose}/{fid} ticks_radial: {t}")
                elif kind == "outline_matches":
                    for t in outline_matches_issue(ax, ctx, pose, fid):
                        issues.append(f"{pose}/{fid} outline_matches: {t}")
        if plan and ctx.stack:
            nc, ci = cover_issues(ctx, ax, pose, rows_list)
            n += nc
            issues += ci
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
            if not g or g.startswith("label:") or g.startswith("note:"):
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
            if any(g.endswith(sfx) and g[:-len(sfx)] in ids for sfx in SUB_SUFFIXES) and g in gids:
                continue      # sub-artist of a row; K5 rules its admission (1.2 (h), Designer M1 r1 F1)
            issues.append(f"{pose}: tagged artist {g} has no spec row")
    return result("K9", not issues, _summ(issues) if issues else f"every spec row drawn, every tagged artist in the spec ({len(ids)} rows)",
                  measured=len(issues), threshold=0, n_issues=len(issues))


CHECKS = {"K1": k1, "K2": k2, "K3": k3, "K4": k4, "K5": k5, "K6": k6, "K7": k7, "K8": k8, "K9": k9}
