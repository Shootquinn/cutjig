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
from matplotlib.patches import Annulus, Circle, Ellipse, FancyArrowPatch, Patch, Polygon, Rectangle  # noqa: E402
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
SIDE_VIEWS = ("side_xz", "section_xz", "section_yz")
# 1.3 P4 (O4): section_yz, plane x = 0 seen from +X, u = +Y right, z up, depth along X (Design Notes 4, s3_spec section).
# Checks evaluate it as the side view of the plan reflected across x = y (reflect_stack): u = plan y, depth = plan x.
SECTION_VIEWS = ("section_yz",)
VIEW_NORMAL = {"side_xz": "Y", "section_xz": "Y", "plan_xy": "Z", "section_yz": "X"}
VIEW_LABELS = {"side_xz": ("x (mm)", "z (mm)"), "section_xz": ("x (mm)", "z (mm)"), "section_yz": ("y (mm)", "z (mm)"),
               "plan_xy": ("x (mm)", "y (mm)"), "stock": ("length (mm)", "bar (mm)")}
FIGSIZE = {"plan_xy": (10, 10), "section_yz": (20, 30)}   # 1.3 (h) r3: section_yz per Designer r2 pick 1 (M1 S3 r1 F1, option A, about 2.45 px/mm)
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

def setup_figure(view, title="", insets=None):
    """Sole owner of figsize, dpi, aspect and grid (K3). Side views are seen from -Y looking along +Y (+X right, +Z up);
    section_yz from +X looking along -X (+Y right, +Z up). 1.3 P4 (TP-7): every Axes carries its view and its Axes id
    (sketch_view, sketch_axes); insets (the spec's insets list) are added by add_inset with their own view."""
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
    ax.sketch_view, ax.sketch_axes = view, main_axes_id(view)
    for d in insets or []:
        add_inset(fig, d)
    return fig, ax


INSET_RECT = (0.60, 0.50, 0.36, 0.42)   # figure fraction (left, bottom, width, height): upper right, height >= 0.3 (s3_spec)


def main_axes_id(view):
    """Axes id of a figure's main Axes: rows name it in their `axes` field (s3_spec: section); a row without `axes` is drawn
    in the main Axes only."""
    return "section" if str(view).startswith("section") else "main"


def add_inset(fig, decl, rect=INSET_RECT):
    """1.3 P4 (TP-7): an inset Axes with its own view (title "<view>: <title>", (mm) labels, equal aspect, both grids, the
    declared extent). Returns the Axes; sketch_view and sketch_axes name its view and Axes id for K3 to K9."""
    view = decl["view"]
    ax = fig.add_axes(list(rect))
    ax.set_title(f"{view}: {decl.get('title', decl['id'])}", fontsize=8)
    xl, yl = VIEW_LABELS.get(view, ("x (mm)", "y (mm)"))
    ax.set_xlabel(xl, fontsize=7)
    ax.set_ylabel(yl, fontsize=7)
    ax.tick_params(labelsize=6)
    ax.set_aspect("equal")
    ax.minorticks_on()
    ax.grid(True, which="major", linewidth=0.6)
    ax.grid(True, which="minor", linewidth=0.3, alpha=0.5)
    ext = decl.get("extent") or {}
    if ext.get("x"):
        ax.set_xlim(*ext["x"])
    if ext.get("y"):
        ax.set_ylim(*ext["y"])
    ax.sketch_view, ax.sketch_axes = view, decl["id"]
    return ax


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


def _spec_path(spec, path):
    """1.3 P4 (label value_from): a dotted path into the spec; a list segment selects the entry whose id equals the
    segment; a missing first segment is skipped (s3_checks.load_cases reads spec load_cases), a dict with `cases` is
    entered. Returns the value or None."""
    def walk(node, segs):
        for sg in segs:
            if isinstance(node, dict) and sg in node:
                node = node[sg]
            elif isinstance(node, dict) and isinstance(node.get("cases"), list):
                node = next((c for c in node["cases"] if isinstance(c, dict) and c.get("id") == sg), None)
            elif isinstance(node, list):
                node = next((c for c in node if isinstance(c, dict) and c.get("id") == sg), None)
            else:
                return None
            if node is None:
                return None
        return node
    segs = str(path).split(".")
    v = walk(spec or {}, segs)
    return v if v is not None or len(segs) < 2 else walk(spec or {}, segs[1:])


LOAD_TOL = 0.005   # N: a load_cases per_screw literal agrees with checks_s3.loads() within this (1.3 (h) r6)
LOAD_PATH = "load_cases"


def computed_per_screw(spec, P):
    """1.3 (h) r6 (M1 S3 r5 Rule 1 fix): {case id: N per screw} computed by checks_s3.loads from the keys (stall_up and
    stall_down: F_stall at the governing mu), or None when the spec has no load_cases / s3_checks. Labels print these;
    the spec per_screw literals are held to them (load_literal_issues)."""
    if not (spec or {}).get("load_cases") or not (spec or {}).get("s3_checks"):
        return None
    import importlib
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    ld = importlib.import_module("checks_s3").loads(P, spec)
    out = dict(ld["per_screw"])
    out["stall_down"] = ld["F_stall_max"]
    return out


def _load_case_of(path):
    """Case id of a value_from path '<...>.load_cases.<case>.per_screw', else None."""
    segs = str(path).split(".")
    if LOAD_PATH in segs and segs[-1] == "per_screw" and len(segs) >= segs.index(LOAD_PATH) + 3:
        return segs[segs.index(LOAD_PATH) + 1]
    return None


def load_literal_issues(spec, P):
    """1.3 (h) r6: premise of the load labels. Every load_cases case's per_screw literal (its first number when text)
    agrees with checks_s3.loads() within LOAD_TOL, so a change of W or of any load key fails here unless the spec follows."""
    comp = computed_per_screw(spec, P)
    if comp is None:
        return []
    out = []
    for c in (spec.get("load_cases") or {}).get("cases") or []:
        v = _first_number(c.get("per_screw"))
        if v is None or c.get("id") not in comp:
            continue
        if abs(v - comp[c["id"]]) > LOAD_TOL:
            out.append(f"load_cases {c['id']} per_screw literal {v:g} against loads() {comp[c['id']]:.4f} N (W or a load key changed)")
        out += stall_literal_issues(c, spec, P)
    return out


_MU_LIST = re.compile(r"^(?P<vals>[^(]*)\(\s*mu\s+(?P<mus>[^)]*)\)")


def stall_literal_issues(c, spec, P):
    """1.4 step 0 R5 d (r6 reviewer NOTE on rule (j)): every number of a text per_screw literal of the form
    '<v1> / <v2> ... (mu <m1> / <m2> ...)' is held, not only the first. Each mu is one of the thread_mu values loads()
    uses, values and mus pair in order, and each value after the first (the first is held above against the governing
    case) agrees with F_stall per screw at its mu within LOAD_TOL. Designer P0D FIX J1: a text literal with two or more
    numbers and no mu list fails (all but its first number would be unheld)."""
    txt = c.get("per_screw")
    if not isinstance(txt, str):
        return []
    if "mu" not in txt:
        n_ = len(NUMBER.findall(txt))
        return [f"load_cases {c['id']} per_screw literal {txt!r}: {n_} numbers with no '(mu ...)' list (rule (j))"] if n_ > 1 else []
    m = _MU_LIST.match(txt.strip())
    if not m:
        return [f"load_cases {c['id']} per_screw literal {txt!r}: numbers with no '(mu ...)' list (rule (j))"]
    vals = [float(x) for x in NUMBER.findall(m.group("vals"))]
    mus = [float(x) for x in NUMBER.findall(m.group("mus"))]
    if len(vals) != len(mus):
        return [f"load_cases {c['id']} per_screw literal {txt!r}: {len(vals)} value(s) against {len(mus)} mu (rule (j))"]
    import importlib
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    th = importlib.import_module("checks_s3").loads(P, spec)["thread"]
    out = []
    for i, (v, mu) in enumerate(zip(vals, mus)):
        k = next((x for x in th if abs(float(x) - mu) < 1e-9), None)
        if k is None:
            out.append(f"load_cases {c['id']} per_screw literal mu {mu:g} is not a thread_mu value {sorted(th)} (rule (j))")
            continue
        f = th[k]["F_stall_per_screw"]
        if i and abs(v - f) > LOAD_TOL:
            out.append(f"load_cases {c['id']} per_screw literal {v:g} at mu {mu:g} against loads() F_stall {f:.4f} N (rule (j), every number)")
    return out


def label_value(lab, P, spec=None):
    """1.3 P4: the value a label must print, as a string, or None when the label carries no single value (its text
    carries it). expr: the expression's value in fmt; value_from: the spec value at that path (a number, str());
    fmt "s": the key's value when it is a string or number; else the key's value in fmt."""
    fmt = lab.get("fmt", ".1f")
    if lab.get("expr_ref"):   # 1.3 (h) r5 (M1 S3 r4 N5): the expression is a spec value read by the label and by RPT
        import check_stack as _cs
        return format(_cs.eval_expr(_spec_path(spec, lab["expr_ref"]), P, {}), fmt if fmt != "s" else ".2f")
    if lab.get("expr"):
        import check_stack as _cs
        return format(_cs.eval_expr(lab["expr"], P, {}), fmt if fmt != "s" else ".2f")
    if lab.get("value_from") and _load_case_of(lab["value_from"]):   # 1.3 (h) r6: a computed load, not the literal
        comp = computed_per_screw(spec, P)
        cid = _load_case_of(lab["value_from"])
        if comp is not None and cid in comp:
            return format(comp[cid], ".2f").rstrip("0").rstrip(".")
    if lab.get("value_from"):
        v = _spec_path(spec, lab["value_from"])
        return (format(v, ".2f").rstrip("0").rstrip(".") if isinstance(v, float) else str(v)) if isinstance(v, (int, float, str)) else None
    v = P.get(lab["key"])
    if fmt == "s":
        return str(v) if isinstance(v, (str, int, float)) else None
    return format(v, fmt)


def _first_number(v):
    if isinstance(v, (int, float)):
        return float(v)
    m = NUMBER.search(str(v))
    return float(m.group(0)) if m else None


def label_cases(lab, P, spec):
    """1.3 (h) r5 (M1 S3 r4 F1): [(case id, printed name, printed value)] of a cases label. label.value_from names the
    load_cases block; label.cases lists [case id, name] pairs (a name may carry {dotted.key}, formatted from P); the value
    is the case's per_screw (its first number when the entry is text, the governing mu) in label.fmt."""
    fmt = lab.get("fmt", ".0f")
    comp = computed_per_screw(spec, P)   # 1.3 (h) r6: values from checks_s3.loads, not the spec literals
    out = []
    for cid, name in lab["cases"]:
        nm = re.sub(r"\{([\w.\[\]]+)\}", lambda m: format(P.get(m.group(1)), "g"), str(name))
        v = comp.get(cid) if comp is not None else _first_number(_spec_path(spec, f"{lab['value_from']}.{cid}.per_screw"))
        out.append((cid, nm, None if v is None else format(v, fmt)))
    return out


def label_text(row, P, rec=None, spec=None):
    """Label text: text + key value [+ suffix]. Label field z_S: true (a z_A height key) writes
    '<text> z_S <key + jig.datum_a_above_floor> (<key> <value> z_A)'. Field z_edge: z_min | z_max appends the row's
    stack edge in z_S at this pose (rec = check_stack feature record), e.g. the cutter tip (r3, Designer M1 F4)."""
    lab = row["label"]
    if "label_text_override" in row:
        return row["label_text_override"]
    if lab.get("template"):   # 1.4 P6 (Designer P3a FIX 1): a sub-artist label printed from its keys
        return label_template_text(lab, P)
    fmt = lab.get("fmt", ".1f")
    v = P.get(lab["key"])
    if lab.get("z_S") and isinstance(v, (int, float)) and fmt != "s":
        txt = f"{lab['text']} z_S {format(v + P.get('jig.datum_a_above_floor'), fmt)} ({lab['key']} {format(v, fmt)} z_A)"
    elif lab.get("stack_z") and rec and lab["stack_z"] in rec:   # 1.3 (h) r6 (M1 S3 r5 F2): the row's stack height, z_S
        txt = f"{lab['text']} z_S {rec[lab['stack_z']]:.2f}"
    elif lab.get("cases"):   # 1.3 (h) r5 (M1 S3 r4 F1): one value per load case, read from load_cases at run time
        txt = f"{lab['text']} " + ", ".join(f"{name} {v}" for _, name, v in label_cases(lab, P, spec))
    else:
        lv = label_value(lab, P, spec)
        txt = f"{lab['text']}" + (f" {lv}" if lv is not None else "")
    txt += f" {lab['suffix']}" if lab.get("suffix") else ""
    edge = lab.get("z_edge")
    if edge and rec and edge in rec:
        txt += f"; {lab.get('z_edge_text', edge)} z_S {rec[edge]:.2f}"
    return txt


_TEMPLATE_FIELD = re.compile(r"\{([A-Za-z_][\w.\[\]]*)(?::([^}]*))?\}")


def label_template_text(lab, P):
    """1.4 P6 (Designer P3a FIX 1): the text of a label {template, keys, map}: every {dotted.key[:fmt]} field of the
    template is the key's value from P in fmt (str when no fmt); a key named in map prints map[key][value] (thread.hand
    right -> RH). The printed value is read from params, never a spec literal (1.3 position)."""
    mp = lab.get("map") or {}

    def field(m):
        k, fmt = m.group(1), m.group(2)
        v = P.get(k)
        if k in mp:
            return str(mp[k].get(v, v))
        return format(v, fmt) if fmt else str(v)
    return _TEMPLATE_FIELD.sub(field, str(lab["template"]))


def sub_label_rows(spec):
    """1.4 P6 (Designer P3a FIX 1): label rows of declared sub-artists, one per sub-artist whose spec block carries a
    label (collet:slits, collet_105:slits through same_as, receiver:root, wingnut:wing): {id: <row>:<sub>, label, poses,
    sub_of, on}. on (+u or -u) names the side of the sub-artist the leader ends on."""
    rows = {r["id"]: r for r in (spec or {}).get("features", [])}
    out = []
    for r in (spec or {}).get("features", []):
        for sub in r.get("sub_artists") or []:
            blk = slit_spec(rows, r) if sub == "slits" else r.get(sub)
            lab = blk.get("label") if isinstance(blk, dict) else None
            if lab:
                out.append({"id": f"{r['id']}:{sub}", "label": lab, "poses": r.get("poses"), "sub_of": r["id"], "on": lab.get("on"),
                            "kind": "sub"})
    return out


def sub_label_issues(ctx, ax, sr, ann):
    """1.4 P6 (Designer P3a FIX 1), the K4 reader of a sub-artist label (sr from sub_label_rows; ann the Text gid
    label:<row>:<sub> or None): (s1) the annotation exists; (s2) a template label prints label_template_text exactly and
    every template field is listed in label.keys; a text/key label carries its text and the key value; (s3) a label with
    on: +u / -u ends its leader on that side (sign of the anchor u). The leader rules (ink, cover, hatch, crossing,
    collinearity) read it as any label (leader_issues, collinear_issues)."""
    lab = sr["label"]
    if ann is None:
        return [f"no annotation label:{sr['id']} (sub-artist label, Designer P3a FIX 1)"]
    txt = ann.get_text()
    out = []
    if lab.get("template"):
        miss = [m.group(1) for m in _TEMPLATE_FIELD.finditer(str(lab["template"])) if m.group(1) not in (lab.get("keys") or [])]
        if miss:
            out.append(f"spec error: template field(s) {', '.join(miss)} not in label.keys")
        want = label_template_text(lab, ctx.P)
        if txt != want:
            out.append(f"label {txt!r} differs from its template printed from the keys {want!r}")
    else:
        want = label_value(lab, ctx.P, ctx.spec)
        if lab.get("text") not in txt:
            out.append(f"label {txt!r} lacks text {lab.get('text')!r}")
        elif want is not None and not any(abs(float(m) - float(want)) < 1e-9 for m in NUMBER.findall(txt.replace(lab["text"], " "))):
            out.append(f"label {txt!r} number differs from {lab.get('key')} = {want}")
    on = sr.get("on")
    if on in ("+u", "-u") and hasattr(ann, "xy"):
        u = float(ann.xy[0])
        if (u > TOL_Z) != (on == "+u") or abs(u) <= TOL_Z:
            out.append(f"label leader ends at u {u:.2f}, not on the {on} side named by label.on")
    elif on is not None and on not in ("+u", "-u"):
        out.append(f"spec error: label.on {on!r} (known: +u, -u)")
    return out


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
    """A drawn area that hides what is under it: a Patch with a visible fill or a hatch. A FancyArrowPatch (load and look
    arrows, line kinds) is no area (P5f: its filled head is a mark)."""
    if not isinstance(a, Patch) or isinstance(a, FancyArrowPatch):
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


def _own_gid(g, fid):
    """g is ink of the labelled row fid: the row itself or one of its sub-artists (a sub-artist label's parent row is not
    its own ink; no relief for it, 1.4 P6)."""
    return g == fid or g.startswith(fid + ":")


def covering_areas(ax, fid, p, rank=None):
    """gids of area artists of other rows that contain p and draw above every artist of row fid that carries ink at p.
    1.3 P1R: containment as drawn (even-odd rings, clip region of a renderer piece)."""
    rank = rank or _rank(ax)
    mine = [a for a in tagged(ax).get(fid, []) if ink_distance(p, [(q, isinstance(a, Patch)) for q in artist_polys(a)]) <= TOL_Z]
    top = max((rank[id(a)] for a in mine), default=(-1e9, -1))
    out = []
    for a in artists(ax):
        g = a.get_gid()
        if not g or _own_gid(g, fid) or not is_area(a) or rank[id(a)] <= top:
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
        inq = {h[0] for h in hatches if not _own_gid(h[0], fid) and
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


def label_anchor(ax, row, zr=None):
    """Leader end of a row's label, on the row's ink (1.2 (h), Designer M1 r1 F4 and F5). A row with label_theta (deg,
    spec field; concentric circles) anchors where the ray from the drill axis at that azimuth leaves its ink. Otherwise
    (max x, mid y) of the drawn pieces when that point is on the ink (a rectangle's or circle's right edge), else the
    drawn vertex of greatest x (nearest mid y among equals): the observer end of a slanted line, the corner of a wedge.
    1.4 P6 (Designer P0D section 4, side placer change): a row with label_anchor_frac anchors at frac_anchor on its
    column-side face (zr: the row's stack z range, as the plan placer and the K4 anchor record read it)."""
    return label_anchor_src(ax, row, zr)[0]


def label_anchor_src(ax, row, zr=None):
    """(anchor, source) of label_anchor; source label_theta, label_anchor_frac, default or ink (the uncovered-ink search)."""
    ink = ink_pieces(ax, row["id"])
    if not ink:
        return None, None
    if row.get("label_theta") is not None:
        hit = _ray_hit(ink, float(row["label_theta"]))
        if hit is not None:
            return hit, "label_theta"
    if row.get("label_anchor_frac") is not None:
        q = frac_anchor(ink, row["label_anchor_frac"], "left" if row.get("label_side") == "left" else "right", zr)
        if q is not None:
            return q, "label_anchor_frac"
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
        return first, "default"
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
            return c, "ink"
    return first, "default"


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


def place_labels(ax, spec, P, pose=None, margin=False, stack_pose=None, notes=(), collinear=False):
    """One annotation per spec row with a label, gid label:<id>, anchored at the right edge of the row's drawn pieces.
    margin=True (S1 r3, Designer M1 r2 F4): every label and every note goes into one column right of the axes, each
    with a leader to its anchor, stacked in anchor-z order with LABEL_GAP_LINES of free space between text boxes.
    Call after finish_axes (the column reads the final limits). notes: (anchor (x, z) or None, text[, gid]) tuples;
    a note without a gid is untagged (the figure note carries gid note:figure_note, Designer 1.2 (c) FIX R1)."""
    items, left_ids = [], set()
    record = {"pose": pose, "placed": {}, "unplaceable": {}}   # 1.4 P6 (Designer P0D section 4): the K4 anchor record (k) on S1
    for row in spec.get("features", []):
        if not row.get("label") or (pose and row.get("poses") and pose not in row["poses"]):
            continue
        rec = (stack_pose or {}).get(row["id"])
        zr_ = (rec["z_min"], rec["z_max"]) if rec and rec.get("z_min") is not None and rec.get("z_max") is not None and rec["z_max"] > rec["z_min"] else None
        anc, src = label_anchor_src(ax, row, zr_)
        if anc is None:
            continue
        items.append((anc, label_text(row, P, rec, spec), f"label:{row['id']}"))
        record["placed"][row["id"]] = {"column": "left" if row.get("label_side") == "left" else "right", "source": src,
                                       "anchor": [round(anc[0], 2), round(anc[1], 2)]}
        if row.get("label_side") == "left":
            left_ids.add(f"label:{row['id']}")
    ax._sc_placer = record
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
            if fid in record["placed"] and tuple(items[i][0]) != tuple(anc):
                record["placed"][fid].update(source="reanchor", anchor=[round(items[i][0][0], 2), round(items[i][0][1], 2)])
    left = sorted([it for it in items if it[2] in left_ids], key=lambda it: -it[0][1])   # r4: label_side left
    items = [it for it in items if it[2] not in left_ids]
    left_z = _stack_z([it[0][1] for it in left], [line * (it[1].count("\n") + 1) for it in left], zlo, zhi, gap)
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
    if collinear:   # 1.4 (h) r2 (Design Notes 35 R1): rule (l) at the 12 px clearance, angled leaders where needed
        left, left_z, order, zs = _side_collinear(ax, spec, left, order, x_left, x_col, zlo, zhi, gap, line, record)
    for it, z in zip(left, left_z):
        ann = ax.annotate(it[1], xy=it[0], xytext=(x_left, z), fontsize=LABEL_FONTSIZE, ha="right", va="center",
                          zorder=LEADER_ZORDER, annotation_clip=False, arrowprops={"arrowstyle": "-", "linewidth": 0.4, "color": "0.35"})
        ann.set_gid(it[2])
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


SIDE_EXTRA_ANGLES = (35.0, -35.0)   # deg: 1.4 (h) r2, side placer only (a long S1 leader between stacked labels)
SIDE_ANCHOR_ALTS = 8   # 1.4 (h) r2: other anchors on the row's ink (at least D apart) the side placer tries for a failing leader


def _side_collinear(ax, spec, left, order, x_left, x_col, zlo, zhi, gap, line, record):
    """1.4 (h) r2 (Design Notes 35 R1) side placer, option collinear (S1): every label leader is judged by rule (l) at the
    Axes clearance (collinear_scale: D = max(D_spec, COLLINEAR_PX_MIN px)) against the families of collinear_lines and
    the other label leaders; a failing label takes the text offset that gives its leader one of LEADER_ANGLES (text z =
    anchor z + tan(angle) |x_text - x_anchor|), the column is re-stacked (_stack_z), and the offset is kept only when
    the count of failing leaders and leader crossings falls (at most PLACER_PASSES rounds per label). Anchors are not
    moved (label_anchor_frac, label_theta and the default anchor stay; K4 anchor record). The angle taken is recorded in
    the placer record (leader_angle). Placer rule only: the check judges every leader (collinear_issues)."""
    import types
    D, R, prem = collinear_scale(ax)
    if prem:
        return left, _stack_z([it[0][1] for it in left], [line * (it[1].count("\n") + 1) for it in left], zlo, zhi, gap), order, None
    cx = types.SimpleNamespace(spec=spec, view=getattr(ax, "sketch_view", None) or "side_xz")
    every = collinear_lines(cx, ax, None)
    (x0, x1), (y0, y1) = sorted(ax.get_xlim()), sorted(ax.get_ylim())
    cols = [("left", left, x_left), ("right", order, x_col)]
    ang = {(c, i): 0.0 for c, its, _ in cols for i in range(len(its))}
    memo = {}

    def layout():
        out = {}
        for c, its, xx in cols:
            wants = [it[0][1] + math.tan(math.radians(ang[(c, i)])) * abs(xx - it[0][0]) if it[0] else it[0] for i, it in enumerate(its)]
            idx = sorted(range(len(its)), key=lambda i: -wants[i])
            zs_ = _stack_z([wants[i] for i in idx], [line * (its[i][1].count("\n") + 1) for i in idx], zlo, zhi, gap)
            for i, z in zip(idx, zs_):
                out[(c, i)] = z
        return out

    def legs(pos):
        out = []
        for c, its, xx in cols:
            for i, it in enumerate(its):
                if it[0] is None:
                    continue
                seg = _clip_box((xx, pos[(c, i)]), (float(it[0][0]), float(it[0][1])), x0, x1, y0, y1)
                out.append(((c, i), it[2], seg, ((xx, pos[(c, i)]), tuple(it[0]))))
        return out

    def leg_fail(fid, seg):
        k = (fid, None if seg is None else (round(seg[0][0], 6), round(seg[0][1], 6), round(seg[1][0], 6), round(seg[1][1], 6)))
        if k not in memo:
            bad = False
            if seg is not None and math.hypot(seg[1][0] - seg[0][0], seg[1][1] - seg[0][1]) > R:
                p0, p1 = seg
                for fam, nm, (a_, b_), reg in collinear_lines(cx, ax, fid, every=every):
                    if _angle_off(p0, p1, a_, b_) > COLLINEAR_DEG or seg_distance(p0, p1, a_, b_) > D:
                        continue
                    if _run_near_vis(p0, p1, a_, b_, reg, mm=D) > R:
                        bad = True
                        break
            memo[k] = bad
        return memo[k]

    hatches = hatch_areas(ax)
    hmemo = {}

    def hatch_fail(fid, t, a_):
        k = (fid, round(t[1], 6), round(a_[0], 6), round(a_[1], 6))
        if k not in hmemo:
            hmemo[k] = bool(leader_hatch(fid, t, a_, hatches))
        return hmemo[k]

    def failing(pos):
        L = legs(pos)
        bad = set()
        for key, gid, seg, full in L:
            if gid and gid.startswith("label:") and (leg_fail(gid[len("label:"):], seg)
                                                      or hatch_fail(gid[len("label:"):], full[0], full[1])):
                bad.add(key)
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                (ka, ga, sa, fa), (kb, gb, sb, fb) = L[i], L[j]
                if _segs_cross(fa[0], fa[1], fb[0], fb[1]):
                    bad |= {ka, kb}
                elif sa is not None and sb is not None and (ga or "").startswith("label:") and (gb or "").startswith("label:")                         and _angle_off(sa[0], sa[1], sb[0], sb[1]) <= COLLINEAR_DEG and seg_distance(sa[0], sa[1], sb[0], sb[1]) <= D                         and _run_near(sa[0], sa[1], sb[0], ((sb[1][0] - sb[0][0]) / (math.hypot(sb[1][0] - sb[0][0], sb[1][1] - sb[0][1]) or 1),
                                                           (sb[1][1] - sb[0][1]) / (math.hypot(sb[1][0] - sb[0][0], sb[1][1] - sb[0][1]) or 1)),
                                      seg=sb, mm=D) > R:
                    bad |= {ka, kb}
        return bad

    pos = layout()
    bad = failing(pos)
    tried = {}
    its_of = {c: its for c, its, _ in cols}
    moved = {}

    def alt_anchors(key):
        """The label's own anchor, then (default / ink / reanchor sources only) ink samples away from it, nearest first."""
        c, i = key
        it = its_of[c][i]
        fid = (it[2] or "")[len("label:"):]
        a0 = tuple(it[0])
        src = (record["placed"].get(fid) or {}).get("source")
        out = [a0]
        if src in ("label_anchor_frac", "label_theta") or not fid:
            return out
        rank = _rank(ax)
        smp = []
        for poly, closed in ink_pieces(ax, fid):
            segs = _edges(poly) if closed else [(poly[k], poly[k + 1]) for k in range(len(poly) - 1)]
            for a_, b_ in segs:
                smp += [(a_[0] + (b_[0] - a_[0]) * k / ANCHOR_SAMPLES, a_[1] + (b_[1] - a_[1]) * k / ANCHOR_SAMPLES) for k in range(ANCHOR_SAMPLES + 1)]
        smp = sorted({(round(q[0], 6), round(q[1], 6)) for q in smp if math.hypot(q[0] - a0[0], q[1] - a0[1]) > D},
                     key=lambda q: math.hypot(q[0] - a0[0], q[1] - a0[1]))
        for q in smp:
            if len(out) > SIDE_ANCHOR_ALTS:
                break
            if all(math.hypot(q[0] - o[0], q[1] - o[1]) > D for o in out) and not covering_areas(ax, fid, q, rank):
                out.append(q)
        return out

    for _ in range(PLACER_PASSES * max(1, len(ang))):
        if not bad:
            break
        changed = False
        for key in sorted(bad):
            if tried.get(key, 0) >= 2 * PLACER_PASSES:
                continue
            tried[key] = tried.get(key, 0) + 1
            c, i = key
            it0 = its_of[c][i]
            best = (len(bad) + 1, ang[key], it0[0])
            for anc in alt_anchors(key):
                for g in (0.0,) + LEADER_ANGLES + SIDE_EXTRA_ANGLES:
                    if g == ang[key] and tuple(anc) == tuple(it0[0]):
                        continue
                    old = ang[key]
                    ang[key] = g
                    its_of[c][i] = (anc, it0[1], it0[2])
                    b2 = failing(layout())
                    if key not in b2 and len(b2) < best[0]:
                        best = (len(b2), g, anc)
                    ang[key] = old
                    its_of[c][i] = it0
                if best[0] <= len(bad):
                    break   # the nearest anchor that clears the label
            if best[1] != ang[key] or tuple(best[2]) != tuple(it0[0]):
                ang[key] = best[1]
                if tuple(best[2]) != tuple(it0[0]):
                    its_of[c][i] = (best[2], it0[1], it0[2])
                    moved[key] = True
                changed = True
                pos = layout()
                bad = failing(pos)
                break
        if not changed:
            break
    for c, its, xx in cols:
        for i, it in enumerate(its):
            fid = (it[2] or "")[len("label:"):] if (it[2] or "").startswith("label:") else None
            if fid and fid in record["placed"]:
                if ang[(c, i)]:
                    record["placed"][fid]["leader_angle"] = ang[(c, i)]
                if moved.get((c, i)):
                    record["placed"][fid].update(source="ink", anchor=[round(it[0][0], 2), round(it[0][1], 2)])
    return left, [pos[("left", i)] for i in range(len(left))], order, [pos[("right", i)] for i in range(len(order))]


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


LEADER_SEP_MIN = 4.0   # mm, DECLARED (Designer P1Rf re-check FIX D4): least distance between two plan leaders, anchor ends included


def seg_distance(a0, a1, b0, b1):
    """Least distance between segments a0-a1 and b0-b1 (0 when they cross)."""
    if _segs_cross(a0, a1, b0, b1):
        return 0.0
    return min(_pt_seg(a0, b0, b1), _pt_seg(a1, b0, b1), _pt_seg(b0, a0, a1), _pt_seg(b1, a0, a1))


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
    exempt, since no straight leader from outside reaches that anchor without crossing it. 1.3 P1Rf2 (TP1.3-8): the
    exemption is strict (outline_encloses_deep: the anchor and every point within TOL_Z of it inside). A row with visible ink anchors
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
        if outline_encloses_deep(O, p1):
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


ENCLOSE_RING = 16   # points on the TOL_Z circle about an anchor tested by outline_encloses_deep


def outline_encloses_deep(O, p):
    """1.3 P1Rf2 (Topologist TP1.3-8, orchestrator ruling): the rule (e) exemption. The anchor and every point within
    TOL_Z of it lie inside the outer boundary of O with holes filled: annulus (a, b) r <= b - TOL_Z; polys: the anchor
    and ENCLOSE_RING points on the circle of radius TOL_Z about it each inside a convex piece. outline_encloses (+TOL_Z,
    inclusive) stays the test for naming the cover (clause (g))."""
    if O[0] == "annulus":
        return math.hypot(*p) <= O[1][1] - TOL_Z
    ring = [(p[0] + TOL_Z * math.cos(2 * math.pi * k / ENCLOSE_RING), p[1] + TOL_Z * math.sin(2 * math.pi * k / ENCLOSE_RING))
            for k in range(ENCLOSE_RING)]
    return all(any(len(q) >= 3 and _inside(x, q) for q in O[1]) for x in [p] + ring)


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
        return sorted({h.gid for h in self.areas if not _own_gid(h.gid, fid)
                       and self.rank[id(h.a)] > top and h.contains(p)})

    def hatch_end(self, fid, p0, p1):
        """leader_hatch on the cached rings."""
        k0 = int(ANCHOR_SAMPLES * (1 - LEADER_END))
        ks = list(range(k0, ANCHOR_SAMPLES))
        hit, gids = 0, set()
        hs = [h for h in self.hatch if not _own_gid(h.gid, fid)]
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


def frac_anchor(ink, frac, column, zr=None):
    """1.3 (h) r5, r6: the point of a row's ink at height y0 + frac (y1 - y0) farthest toward the label column (the
    column-side crossing of the ink at that height: a block face, an arrow shaft), or None."""
    pts = [p for poly, _ in ink for p in poly]
    y0, y1 = zr if zr else (min(p[1] for p in pts), max(p[1] for p in pts))   # r6: the row's stack z range when given
    y = y0 + float(frac) * (y1 - y0)
    xs = []
    for poly, closed in ink:
        segs = _edges(poly) if closed else [(poly[i], poly[i + 1]) for i in range(len(poly) - 1)]
        for a, b in segs:
            if min(a[1], b[1]) - 1e-9 <= y <= max(a[1], b[1]) + 1e-9:
                if abs(b[1] - a[1]) < 1e-12:
                    xs += [a[0], b[0]]
                else:
                    xs.append(a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]))
    if not xs:
        return None
    q = (max(xs) if column == "right" else min(xs), y)
    return q if ink_distance(q, ink) <= TOL_Z else None


def anchor_candidates(lc, row, column, zr=None):
    """[(source, anchor)] for one row in one column, in placer order (see the block comment)."""
    ink = lc.ink(row["id"])
    if not ink:
        return []
    out = []
    if row.get("label_theta") is not None:
        hit = _ray_hit(ink, float(row["label_theta"]))
        if hit is not None:
            out.append(("label_theta", hit))
    if row.get("label_anchor_frac") is not None:   # 1.3 (h) r5 (Designer DR4-1): on the column-side face at a height fraction
        q = frac_anchor(ink, row["label_anchor_frac"], column, zr)
        if q is not None:
            out.append(("label_anchor_frac", q))
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


LEADER_ANGLES = (8.0, -8.0, 15.0, -15.0, 25.0, -25.0)   # deg: 1.4 (h) r2 (Design Notes 35 R1) angled leader candidates


def cand_angle(src):
    """Leader angle (deg, text above the anchor positive) of a placer candidate source 'src@deg'; 0 when horizontal."""
    return float(str(src).split("@", 1)[1]) if src and "@" in str(src) else 0.0


def cand_source(src):
    """The anchor source of a placer candidate without its angle suffix (the K4 anchor record reads it)."""
    return str(src).split("@", 1)[0] if src else src


def angled_candidates(ink, cands, D):
    """1.4 (h) r2 (Design Notes 35 R1, placer rule; the check judges every leader by rule (l)): the candidate list with
    angled variants. Every candidate keeps its horizontal form first; then each anchor is offered with the text moved so
    the leader runs at each of LEADER_ANGLES (src suffixed '@deg'). An anchor of a default or ink source on a vertical
    face (within COLLINEAR_DEG) shorter than 2 D (a part thinner than twice the clearance) is moved to that face's
    mid-height and offered angled only (Design Notes 35: 'the leader lands angled at the part mid-height'). Anchors from
    label_anchor_frac and label_theta are kept where the spec puts them (K4 anchor record)."""
    edges = []
    for poly, closed in ink:
        segs = _edges(poly) if closed else [(poly[i], poly[i + 1]) for i in range(len(poly) - 1)]
        edges += [(a, b) for a, b in segs if math.hypot(b[0] - a[0], b[1] - a[1]) > 1e-9]
    base, angled, seen = [], [], set()
    for col, src, anc in cands:
        mid = None
        if src not in ("label_anchor_frac", "label_theta"):
            thin = [(math.hypot(b[0] - a[0], b[1] - a[1]), a, b) for a, b in edges
                    if _pt_seg(anc, a, b) <= 1e-6 and abs(b[0] - a[0]) <= math.tan(math.radians(COLLINEAR_DEG)) * abs(b[1] - a[1])
                    and math.hypot(b[0] - a[0], b[1] - a[1]) < 2 * D]
            if thin:
                _, a, b = min(thin)
                mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if mid is not None:
            key = (col, round(mid[0], 6), round(mid[1], 6))
            if key not in seen:
                seen.add(key)
                angled += [(col, f"{src}@{g:g}", mid) for g in LEADER_ANGLES]
            continue
        base.append((col, src, anc))
        if src in ("label_anchor_frac", "label_theta"):   # the spec's anchor: its angled forms before any other anchor
            base += [(col, f"{src}@{g:g}", anc) for g in LEADER_ANGLES]
        else:
            angled += [(col, f"{src}@{g:g}", anc) for g in LEADER_ANGLES]
    return base + angled


def place_plan_labels(ax, ctx, pose, margin=True, stack_pose=None, notes=(), edge_leaders=False, collinear=False):
    """The plan leader placer (1.3 P1R R3; rules in the block comment above). margin=True: labels in a right column
    (x = right axes limit + one text line, left-aligned) and a left column (left limit - one line, right-aligned),
    stacked in anchor-y order with LABEL_GAP_LINES between boxes, as place_labels(margin=True), no left-column text box
    over a y tick label; notes without an anchor
    go under the right column below the axes. margin=False (fixtures): text 60 right (left column: 60 left) and 20 above
    the anchor. Call after render_plan and finish_axes. Returns the placer record (also ax._sc_placer).
    edge_leaders (1.3 (h) r2, Designer M1 S3 r1 F2): the drawn leader leaves the text at the middle of its edge facing the
    anchor column (relpos (0, 0.5) right column, (1, 0.5) left column), so the drawn leader is the placer's leg from the
    text position to the anchor; without it matplotlib starts the leader at the text centre and a long label's leader
    leaves through its bottom edge into the label below (S3 r1 hold_callout through span_lt). S2 r9 keeps the default
    (K4 (i) passes on its pixels)."""
    spec, P = ctx.spec, ctx.P
    outl, zmx = leader_outlines(ctx, pose)
    vis = row_visibility(ctx, ax, pose) if ctx.view == "plan_xy" and ctx.stack is not None else {}
    lc = _LeaderCtx(ax, outl, zmx, vis)
    rows = [r for r in spec.get("features", []) if r.get("label") and applies(r, pose) and lc.ink(r["id"])]
    rows += [r for r in sub_label_rows(spec) if applies(r, pose) and lc.ink(r["id"])]   # 1.4 P6 (Designer P3a FIX 1)
    order = [r["id"] for r in rows]
    byid = {r["id"]: r for r in rows}
    texts = {r["id"]: label_text(r, P, (stack_pose or {}).get(r["id"]), ctx.spec) for r in rows}
    cands = {}
    for r in rows:
        cols = ["left", "right"] if r.get("label_side") == "left" else ["right", "left"]
        f_ = (stack_pose or {}).get(r["id"]) or {}
        zr_ = (f_["z_min"], f_["z_max"]) if f_.get("z_min") is not None and f_.get("z_max") is not None and f_["z_max"] > f_["z_min"] else None
        cands[r["id"]] = [(col, src, anc) for col in cols for src, anc in anchor_candidates(lc, r, col, zr_)]
        if r.get("on") in ("+u", "-u"):   # 1.4 P6: a sub-artist label ends on the side its label.on names
            sg = 1 if r["on"] == "+u" else -1
            cands[r["id"]] = [c for c in cands[r["id"]] if c[2][0] * sg > TOL_Z]
    ax.apply_aspect()
    if collinear:   # 1.4 (h) r2 (Design Notes 35 R1): angled leaders and the thin-face mid-height landing
        D_ = collinear_scale(ax)[0]
        if D_ is not None:
            for r in rows:
                cands[r["id"]] = angled_candidates(ink_pieces(ax, r["id"]), cands[r["id"]], D_)
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
        col, src, anc = c
        if not margin:
            return (anc[0] + (60 if col == "right" else -60), anc[1] + 20)
        h = hgt[f]
        xx = x_col if col == "right" else x_left
        z = anc[1] + math.tan(math.radians(cand_angle(src))) * abs(xx - anc[0])   # 1.4 (h) r2: angled candidate
        return (xx, min(max(z, zlo + h / 2), zhi - h / 2))

    def layout(choice):
        pos = {}
        if not margin:
            return {f: wanted(f, c) for f, c in choice.items() if c}
        for col, xx in (("right", x_col), ("left", x_left)):
            items = sorted([f for f in order if choice.get(f) and choice[f][0] == col], key=lambda f: -wanted(f, choice[f])[1])
            zs = _stack_z([wanted(f, choice[f])[1] for f in items], [hgt[f] for f in items], zlo, zhi, gap)
            pos.update({f: (xx, z) for f, z in zip(items, zs)})
        return pos

    memo = {}
    # 1.4 P6 (S4 r1), option collinear: a candidate also passes K4 rule (l) against the figure's reference lines,
    # gridlines, part edges and drawn lines (collinear_lines; D and R from collinear_scale; the leader family is judged by
    # the check), so the placer takes the first anchor whose leader does not merge with a line. Off by default: S2 and S3
    # place as accepted, their rule (l) firings held by spec anchors (Designer P0D section 4).
    col_every = collinear_lines(ctx, ax, None) if collinear else None
    col_D, col_R, _prem = collinear_scale(ax) if collinear else (None, None, None)

    def col_fail(f, txy, anc):
        """K4 rule (l) on one leader at this text position (the test of collinear_issues, without the leader family)."""
        (x0_, x1_), (y0_, y1_) = sorted(ax.get_xlim()), sorted(ax.get_ylim())
        seg = _clip_box((float(txy[0]), float(txy[1])), (float(anc[0]), float(anc[1])), x0_, x1_, y0_, y1_)
        if seg is None or math.hypot(seg[1][0] - seg[0][0], seg[1][1] - seg[0][1]) <= col_R:
            return None
        p0, p1 = seg
        for fam, nm, (a_, b_), reg in collinear_lines(ctx, ax, f, every=col_every):
            if _angle_off(p0, p1, a_, b_) > COLLINEAR_DEG or seg_distance(p0, p1, a_, b_) > col_D:
                continue
            if _run_near_vis(p0, p1, a_, b_, reg, mm=col_D) > col_R:
                return ("rule (l)", f"{fam} {nm}")
        return None

    def fail1(f, txy, anc):
        k = (f, round(txy[0], 9), round(txy[1], 9), anc)
        if k not in memo:
            memo[k] = lc.fail(f, txy, anc) or (col_fail(f, txy, anc) if collinear and not _prem else None)
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
                elif margin and seg_distance(a0, a1, b0, b1) < LEADER_SEP_MIN:   # (h), 1.3 P1Rf2 (Designer FIX D4)
                    out.setdefault(fa, []).append(("leader within 4.0 mm of", fb))
                    out.setdefault(fb, []).append(("leader within 4.0 mm of", fa))
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
        record["placed"][f] = {"column": col, "source": cand_source(src), "anchor": [round(anc[0], 2), round(anc[1], 2)],
                               "text": [round(pos[f][0], 2), round(pos[f][1], 2)]}
        if cand_angle(src):   # 1.4 (h) r2: the angled candidate taken (Design Notes 35 R1)
            record["placed"][f]["leader_angle"] = cand_angle(src)
        kw = {"ha": "left" if col == "right" else "right", "va": "center"} if margin else {}
        ann = ax.annotate(texts[f], xy=anc, xytext=pos[f], fontsize=LABEL_FONTSIZE, zorder=LEADER_ZORDER, annotation_clip=False,
                          arrowprops={"arrowstyle": "-", "linewidth": 0.4 if margin else 0.5, **({"color": "0.35"} if margin else {}),
                                      **({"relpos": (0.0, 0.5) if col == "right" else (1.0, 0.5)} if edge_leaders and margin else {})}, **kw)
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


def arrow_ends(a):
    """1.3 P4: (tail, head) of an arrow artist in data coordinates: a FancyArrowPatch's posA and posB through its own
    transform (transData by default), or the first and last vertex of a Line2D drawn tail to head; None otherwise."""
    if isinstance(a, FancyArrowPatch) and getattr(a, "_posA_posB", None) is not None and a.axes is not None:
        T = a.get_transform()
        pts = T.transform(np.asarray(a._posA_posB, dtype=float))
        (x0, y0), (x1, y1) = a.axes.transData.inverted().transform(pts)
        return (float(x0), float(y0)), (float(x1), float(y1))
    if isinstance(a, Line2D):
        p = artist_polys(a)[0]
        return (p[0], p[-1]) if len(p) >= 2 else None
    return None


def terminator_issues(ax, fid, pose, script=False):
    """1.3 (h) r4 (Designer NOTE D-r3-1): premise of reading a reference line row's extent without its arrows. Every
    FancyArrowPatch of the row has its tail and head on the row's Line2D ink within TOL_Z (a terminator lies on the
    dimension line it ends), so an arrow cannot stand away from the line it marks."""
    arts = tagged(ax).get(fid, [])
    ink = [q for a in arts if isinstance(a, Line2D) for q in artist_polys(a)]
    out = []
    for a in arts:
        if not isinstance(a, FancyArrowPatch):
            continue
        ends = arrow_ends(a)
        if not ends:
            continue
        for nm, p in zip(("tail", "head"), ends):
            d = min((_pt_seg(p, q[i], q[i + 1]) for q in ink for i in range(len(q) - 1)), default=float("inf"))
            if d > TOL_Z:
                out.append(f"{pose}/{fid} terminator: arrow {nm} ({p[0]:.2f}, {p[1]:.2f}) {d:.2f} off the line (D-r3-1)")
        out += terminator_shape_issues(a, ends, fid, pose, script)
    return out


TERM_STYLE = ("CurveFilledB", 0.4, 0.2)   # 1.4 step 0 R5 c: the signed r4 terminator, arrowstyle '-|>' (head_length, head_width)
TERM_MUTATION_SCALE = LABEL_FONTSIZE * 2   # points, as s3_jackscrew_section.py draws it (Designer r4 delta read: arrowheads PASS)


def terminator_shape_issues(a, ends, fid, pose, script=False):
    """1.4 step 0 R5 c (Designer NOTE DR4-2): the relief premise bounds the arrow's form and size, not only where it
    sits. (1) The connection is straight: connection style Arc3 with rad 0 (a curved connection bulges off the line it
    marks). (2) On a script-drawn figure the head is the signed r4 terminator: arrowstyle TERM_STYLE (class, head_length,
    head_width) at mutation_scale TERM_MUTATION_SCALE, so its rendered half-width is fixed (head_width x mutation_scale
    points at the figure dpi; 2.38 mm on S3 r7, DERIVED). A numeric bound in mm is The Designer's value (P0D)."""
    out = []
    cs_ = a.get_connectionstyle() if hasattr(a, "get_connectionstyle") else None
    rad = getattr(cs_, "rad", None)
    if cs_ is not None and (type(cs_).__name__ != "Arc3" or rad is None or abs(float(rad)) > 1e-12):
        out.append(f"{pose}/{fid} terminator: connection style {type(cs_).__name__}"
                   f"{'' if rad is None else f' rad {float(rad):g}'} is not straight (Arc3 rad 0; DR4-2)")
    if script:
        st = a.get_arrowstyle()
        got = (type(st).__name__, getattr(st, "head_length", None), getattr(st, "head_width", None))
        ms = float(a.get_mutation_scale())
        if got != TERM_STYLE or abs(ms - TERM_MUTATION_SCALE) > 1e-9:
            out.append(f"{pose}/{fid} terminator: arrowstyle {got[0]} (head_length {got[1]}, head_width {got[2]}) at mutation_scale "
                       f"{ms:g}, not the signed terminator {TERM_STYLE[0]} ({TERM_STYLE[1]}, {TERM_STYLE[2]}) at {TERM_MUTATION_SCALE:g} (DR4-2)")
    return out


def terminator_half_width_mm(a):
    """Rendered head half-width of an arrow in data mm at its figure's dpi: head_width x mutation_scale points (reported)."""
    st, ax = a.get_arrowstyle(), a.axes
    hw = getattr(st, "head_width", None)
    if hw is None or ax is None:
        return None
    px = hw * float(a.get_mutation_scale()) * ax.figure.dpi / 72.0
    (x0, y0), (x1, y1) = ax.transData.transform([(0, 0), (1, 0)])
    return px / math.hypot(x1 - x0, y1 - y0)


def geom_pieces(ax, row):
    """1.3 P4: the drawn geometry of a row for centre and extent tests: its pieces, without look arrows (FancyArrowPatch)
    on a line row (an arrowhead marks the direction of a cutting-plane line; it is not the line's extent)."""
    if row.get("kind") == "line":
        return [poly for a in tagged(ax).get(row["id"], []) if not isinstance(a, FancyArrowPatch)
                and not getattr(a, "_sc_hidden_copy", False) for poly in artist_polys(a)]
    return pieces(ax, row["id"])


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
               "ticks_radial": "count", "outline_matches": "pieces",
               "look_direction": "toward", "axes_not_inverted": "pred", "points": "dir",   # 1.3 P4 (s3_spec)
               "mirror_about_radial": "pred",   # P5f (Topologist FIX 6)
               "between": "below", "vertical_edge": "piece"}   # 1.4 P4 (O6): washer between; S4-d bore vertical


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
        if getattr(ctx, "axes_role", "main") == "inset":
            continue   # 1.3 P4 (TP-7): figure size and dpi belong to the figure, judged with the main Axes
        need = FIGSIZE.get(view, FIGSIZE_DEFAULT)
        w, h = fig.get_size_inches()
        if w < need[0] - 1e-9 or h < need[1] - 1e-9:
            issues.append(f"{name}: figsize ({w:.1f}, {h:.1f}) below {need}")
        if abs(fig.dpi - DPI) > 1e-9:
            issues.append(f"{name}: dpi {fig.dpi:g} not {DPI}")
    if getattr(ctx, "axes_role", "main") == "main":
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
        fig = real_figure(fig)   # 1.3 P4: every Axes of the figure, the inset included
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
            if row.get("label_home") and f"label:{row['id']}" in anns:   # P5f (SW FIX 5)
                issues.append(f"{pose}/{row['id']}: label drawn outside its home Axes {row['label_home']}")
            if not row.get("label") or not applies(row, pose):
                continue
            n += 1
            lab = row["label"]
            want = label_value(lab, ctx.P, ctx.spec)   # 1.3 P4: expr, value_from and fmt "s" labels
            txt = anns.get(f"label:{row['id']}")
            if txt is None:
                issues.append(f"{pose}/{row['id']}: no annotation label:{row['id']}")
                continue
            if lab["text"] not in txt:
                issues.append(f"{pose}/{row['id']}: label {txt!r} lacks text {lab['text']!r}")
                continue
            if lab.get("stack_z"):   # 1.3 (h) r6 (M1 S3 r5 F2): the printed z_S against check_stack nut_z at the named pose
                pz_ = lab.get("pose_of")
                st_ = (ctx.parent.stack if getattr(ctx, "parent", None) is not None else ctx.stack) or {}
                vz = ((st_.get("poses") or {}).get(pz_) or {}).get("vars_z_A", {}).get(lab.get("stack_name", "nut_z"))
                import check_stack as _cs
                m_ = re.search(r"z_S (-?\d+(?:\.\d+)?)", txt)
                if vz is None or m_ is None:
                    issues.append(f"{pose}/{row['id']}: label {txt!r} stack_z without a z_S value or pose_of {pz_!r}")
                elif abs(float(m_.group(1)) - _cs.to_shop_floor(vz, ctx.P)) > TOL_Z:
                    issues.append(f"{pose}/{row['id']}: label {txt!r} z_S {m_.group(1)} against check_stack {lab.get('stack_name', 'nut_z')} "
                                  f"at {pz_} {_cs.to_shop_floor(vz, ctx.P):.2f} (K4 stack_z)")
                continue
            if lab.get("cases"):   # 1.3 (h) r5 (M1 S3 r4 F1): every case value as load_cases per_screw prints it
                for cid, nm, v in label_cases(lab, ctx.P, ctx.spec):
                    if v is None or f"{nm} {v}" not in txt:
                        issues.append(f"{pose}/{row['id']}: label {txt!r} lacks case {cid} {nm!r} {v} (load_cases per_screw; K4 cases)")
                continue
            if want is None:
                continue   # 1.3 P4: no single value (a list key or a spec block); the text carries it
            if lab.get("fmt") == "s" and not lab.get("expr"):
                if want not in txt.replace(lab["text"], " "):
                    issues.append(f"{pose}/{row['id']}: label {txt!r} lacks the value {want!r} ({lab.get('value_from') or lab['key']})")
                continue
            nums = NUMBER.findall(txt.replace(lab["text"], " "))
            if not nums:
                issues.append(f"{pose}/{row['id']}: label {txt!r} carries no number (want {want} from {lab['key']})")
            elif not any(abs(float(m) - float(want)) < 1e-9 for m in nums):
                issues.append(f"{pose}/{row['id']}: label {txt!r} number differs from {('expr ' + lab['expr']) if lab.get('expr') else lab['key']} = {want}")
    for pose, fig in ctx.figs.items():   # 1.4 P6 (Designer P3a FIX 1): sub-artist labels, read where the sub-artist is drawn
        ax_ = fig.axes[0]
        drawn_ = tagged(ax_)
        anns_ = {t.get_gid(): t for t in ax_.texts if t.get_gid()}
        for sr in sub_label_rows(ctx.spec):
            if not applies(sr, pose) or not drawn_.get(sr["id"]):
                continue
            n += 1
            issues += [f"{pose}/{sr['id']}: {m}" for m in sub_label_issues(ctx, ax_, sr, anns_.get(f"label:{sr['id']}"))]
    issues += figure_note_issues(ctx)
    issues += leader_issues(ctx)
    issues += text_overlap_issues(ctx)   # 1.3 (h) r2: K4 (i), Designer M1 S3 r1 F2, F3
    if getattr(ctx, "axes_role", "main") == "main":   # 1.3 (h) r6: load literals, anchor record, frac lint, collinearity
        issues += load_literal_issues(ctx.spec, ctx.P)
    issues += anchor_record_issues(ctx)
    issues += collinear_issues(ctx)
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
    1.3 P1Rf2: (h) in plan, two leaders that do not cross keep at least LEADER_SEP_MIN (4.0 mm) apart, anchor ends
    included (segment distance; Designer FIX D4).
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
                elif plan:   # (h) 1.3 P1Rf2 (Designer FIX D4): leaders, anchor ends included, at least LEADER_SEP_MIN apart
                    d = seg_distance(a0, a1, b0, b1)
                    if d < LEADER_SEP_MIN:
                        out.append(f"{pose}: label leaders {fa} and {fb} {d:.2f} mm apart (h, least {LEADER_SEP_MIN:g})")
    return out




def anchor_record_issues(ctx):
    """1.3 (h) r6 (M1 S3 r5 Rule 2 fix (a), (c)): a row declaring label_anchor_frac has frac in [0, 1] (lint) and its
    placed leader ends at that anchor (placer record source label_anchor_frac, anchor within TOL_Z of frac_anchor on the
    row's ink); a fallback to another candidate is an issue, so the premise of the frac input is checked."""
    out = []
    for pose, fig in (ctx.figs or {}).items():
        ax = fig.axes[0]
        rec = (getattr(ax, "_sc_placer", None) or {}).get("placed") or {}
        for row in ctx.spec.get("features", []):
            fr = row.get("label_anchor_frac")
            if fr is None or not row.get("label"):
                continue
            if not isinstance(fr, (int, float)) or not 0 <= float(fr) <= 1:
                out.append(f"{row['id']}: spec error, label_anchor_frac {fr!r} outside [0, 1]")
                continue
            got = rec.get(row["id"])
            if got is None:
                continue
            f_ = ((ctx.stack or {}).get("poses", {}).get(pose, {}) or {}).get("features", {}).get(row["id"]) or {}
            zr_ = (f_["z_min"], f_["z_max"]) if f_.get("z_min") is not None and f_.get("z_max") is not None and f_["z_max"] > f_["z_min"] else None
            q = frac_anchor(ink_pieces(ax, row["id"]), fr, got["column"], zr_) if ink_pieces(ax, row["id"]) else None
            if got.get("source") != "label_anchor_frac" or q is None or math.hypot(got["anchor"][0] - q[0], got["anchor"][1] - q[1]) > TOL_Z + 0.01:
                out.append(f"{pose}/{row['id']}: label leader ends at {got['anchor']} ({got.get('source')}), not at its label_anchor_frac {fr:g} anchor "
                           f"{None if q is None else [round(q[0], 2), round(q[1], 2)]} (K4 anchor record)")
    return out


# P0D FIX L1: thresholds in mm on paper at the figure dpi, converted per Axes to data mm. Premise of the FIX (Designer P0D
# 1.2): equal to the signed 1.3 r6 S3 section values, 1.0 and 5.0 data mm at 2.45136 px per data mm and 150 dpi (0.41510,
# 2.07549 paper mm, DERIVED), rounded up at the fourth decimal so the section reads D 1.00025, R 5.00027 data mm. The
# sign-off's rounded 0.4 / 2.0 read D 0.9636 on the section and drop the K4-B28, K4-B29 r95 firing at 1.00 data mm
# (P0f file, FIX L1 dry run); the constant goes back to The Designer for signature.
COLLINEAR_PAPER_MM = 0.4152
COLLINEAR_PAPER_RUN_MM = 2.0756
COLLINEAR_DEG = 2.0            # 1.3 (h) r6: within this angle of a line a leader runs along it (M1 S3 r5 F1, Rule 2 fix (b))
COLLINEAR_ASPECT_TOL = 1e-6    # premise of the paper conversion: px per data mm equal in x and y (relative)
COLLINEAR_PX_MIN = 12.0        # 1.4 (h) r2 (Design Notes 35 R1, M1 S4 r1 F2): least clearance in px at the saved scale


def collinear_scale(ax):
    """Rule (l) thresholds of one Axes in data mm (P0D FIX L1): (D, R, premise issue or None). D = max(COLLINEAR_PAPER_MM,
    COLLINEAR_PX_MIN px) and R = COLLINEAR_PAPER_RUN_MM, converted at the Axes' px per data mm (transData at the figure
    dpi). 1.4 (h) r2 (Design Notes 35 R1): the clearance is judged in pixels of the saved image at 100 percent, at least
    COLLINEAR_PX_MIN px; premise of reading it from the figure dpi: every script saves at the figure dpi (savefig without
    a dpi argument, rcParams savefig.dpi 'figure'; K3 dpi and the save lint). Premise: equal aspect (px per data mm equal
    in x and y within COLLINEAR_ASPECT_TOL); an Axes that breaks it is reported and not judged."""
    (a, b, c) = ax.transData.transform([(0, 0), (1, 0), (0, 1)])
    kx, ky = math.hypot(b[0] - a[0], b[1] - a[1]), math.hypot(c[0] - a[0], c[1] - a[1])
    if kx <= 0 or ky <= 0 or abs(kx - ky) > COLLINEAR_ASPECT_TOL * max(kx, ky):
        return None, None, (f"rule (l) premise: px per data mm {kx:.4f} in x against {ky:.4f} in y; the paper-mm conversion needs "
                            f"equal aspect (K4 collinear)")
    f = ax.figure.dpi / 25.4 / kx
    return max(COLLINEAR_PAPER_MM * f, COLLINEAR_PX_MIN / kx), COLLINEAR_PAPER_RUN_MM * f, None


def _run_near(p0, p1, line_pt, line_dir, seg=None, step=0.25, mm=1.0):
    """Longest run (mm) of segment p0-p1 within mm of a line (point, unit direction; seg = (a, b) bounds it)."""
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    if L < 1e-9:
        return 0.0
    n = max(2, int(L / step) + 1)
    best = run = 0.0
    for k in range(n):
        t = k / (n - 1)
        q = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
        d = _pt_seg(q, seg[0], seg[1]) if seg else abs((q[0] - line_pt[0]) * line_dir[1] - (q[1] - line_pt[1]) * line_dir[0])
        run = run + L / (n - 1) if d <= mm and k else (0.0 if d > mm else run)
        best = max(best, run)
    return best


def _clip_box(p0, p1, x0, x1, y0, y1):
    """Segment p0-p1 clipped to the box [x0, x1] x [y0, y1] (Liang-Barsky); None when it misses the box."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, p0[0] - x0), (dx, x1 - p0[0]), (-dy, p0[1] - y0), (dy, y1 - p0[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return (p0[0] + t0 * dx, p0[1] + t0 * dy), (p0[0] + t1 * dx, p0[1] + t1 * dy)


# 1.4 step 0 R4 (Step 1.3 gate G2, G3; C1.3-a); P0f: drawn line (Designer P0D FIX L2, Topologist P0T TP1.4-1 "part line")
# and leader (Designer P0D FIX L4).
COLLINEAR_FAMILIES = ("reference line", "gridline", "part edge", "drawn line", "leader")
VIEW_AXES = {"side_xz": ("x", "z"), "plan_xy": ("x", "y"), "section_yz": ("u", "z"), "section_xz": ("u", "z")}
OWN_ROW_FAMILIES = ("part edge", "drawn line")   # the labelled row's own edges and lines are outside the rule (N-l3)


def strokes_boundary(a):
    """Topologist P0T TP1.4-1: a visible Patch whose boundary is drawn: a filled face or a hatch (is_area), or a stroked
    edge (linewidth > 0, edge alpha > 0, line style not none): every renderer solid or dashed piece, stand-in outline and
    unfilled part outline. A FancyArrowPatch is a mark, never a part boundary."""
    if not isinstance(a, Patch) or isinstance(a, FancyArrowPatch) or not a.get_visible():
        return False
    if is_area(a):
        return True
    ec = a.get_edgecolor()
    ls = a.get_linestyle()
    return (float(a.get_linewidth() or 0) > 0 and ec is not None and ec[3] > 0
            and not (isinstance(ls, str) and ls.strip().lower() in ("", "none")))


def collinear_lines(ctx, ax, fid, every=None):
    """The lines rule (l) holds a leader of row fid against, in the Axes ax: [(family, line id, (a, b), visible)] where
    visible is None or a RegionIndex (the clip region the artist draws in; a sample counts only where the line is drawn).
    Families: reference line (every Line2D segment of a reference line row, its :sub-artists and the labelled row's own
    included); gridline (major and minor, both axes, inside the limits); part edge (every edge of every ring of every
    visible Patch of another row whose boundary is drawn: strokes_boundary, renderer solid and dashed pieces and stand-in
    outlines included, counted inside their clip region; TP1.4-1); drawn line (every segment of every visible Line2D or
    Collection of another row that is not a reference line row, counted inside its clip region; P0D FIX L2, TP1.4-1).
    Hatch strokes, FancyArrowPatch marks and text are in no family. The leader family is added by collinear_issues.
    every: the result of collinear_lines(ctx, ax, None) for the same Axes state, filtered here by row (one geometry pass
    per Axes)."""
    if every is not None:
        return [ln for ln in every if not (ln[0] in OWN_ROW_FAMILIES and ln[1].split(":")[0] == fid)]
    (x0, x1), (y0, y1) = sorted(ax.get_xlim()), sorted(ax.get_ylim())
    refs = {r["id"] for r in ctx.spec.get("features", []) if r.get("reference") and r.get("kind") == "line"}
    hn, vn = VIEW_AXES.get(ctx.view, ("x", "z"))
    out = []
    for g, arts in tagged(ax).items():
        row = g.split(":")[0]
        for a in arts:
            if row in refs and isinstance(a, Line2D):
                q = artist_polys(a)[0]
                out += [("reference line", g, (q[i], q[i + 1]), None) for i in range(len(q) - 1)]
            elif row == fid:
                continue
            elif getattr(a, "_sc_outlined", False):   # 1.4 (h) r2 (M1 S4 F3): the body's edge is its :outline drawn line
                continue
            elif strokes_boundary(a):
                reg = drawn_region(a)
                for q in artist_polys(a):
                    if len(q) < 2:
                        continue
                    ring = list(q) + [q[0]] if len(q) >= 3 else list(q)
                    out += [("part edge", g, (ring[i], ring[i + 1]), reg) for i in range(len(ring) - 1)
                            if math.hypot(ring[i + 1][0] - ring[i][0], ring[i + 1][1] - ring[i][1]) > 1e-9]
            elif row not in refs and isinstance(a, (Line2D, Collection)) and a.get_visible():
                reg = drawn_region(a)
                for q in artist_polys(a):
                    out += [("drawn line", g, (q[i], q[i + 1]), reg) for i in range(len(q) - 1)
                            if math.hypot(q[i + 1][0] - q[i][0], q[i + 1][1] - q[i][1]) > 1e-9]
    out += [("gridline", f"gridline {vn} %g" % v, ((x0, v), (x1, v)), None)
            for v in sorted(set(ax.yaxis.get_majorticklocs()) | set(ax.yaxis.get_minorticklocs())) if y0 < v < y1]
    out += [("gridline", f"gridline {hn} %g" % v, ((v, y0), (v, y1)), None)
            for v in sorted(set(ax.xaxis.get_majorticklocs()) | set(ax.xaxis.get_minorticklocs())) if x0 < v < x1]
    return out


def _run_near_vis(p0, p1, a, b, reg, step=0.25, mm=1.0):
    """Longest run (mm) of segment p0-p1 within mm of segment a-b, counting a sample only where the nearest point of a-b
    is drawn (reg None, or reg contains it or a point within 0.05 across the line)."""
    if reg is None:
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        return _run_near(p0, p1, a, ((b[0] - a[0]) / L, (b[1] - a[1]) / L), seg=(a, b), step=step, mm=mm)
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    if L < 1e-9:
        return 0.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    ln = math.sqrt(L2) or 1.0
    nx, ny = -dy / ln, dx / ln
    n = max(2, int(L / step) + 1)
    best = run = 0.0
    for k in range(n):
        t = k / (n - 1)
        q = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
        s = 0.0 if L2 == 0 else max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / L2))
        c = (a[0] + s * dx, a[1] + s * dy)
        near = math.hypot(q[0] - c[0], q[1] - c[1]) <= mm and any(
            reg.contains((c[0] + e * nx, c[1] + e * ny)) for e in (0.0, 0.05, -0.05))
        run = run + L / (n - 1) if near and k else (0.0 if not near else run)
        best = max(best, run)
    return best


def _angle_off(p0, p1, a, b):
    """Angle (deg, 0 to 90) between the directions p0-p1 and a-b."""
    la = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    lb = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return abs((la - lb + 90) % 180 - 90)


def own_continuation(ax, row, t):
    """Designer P0D FIX L3, terms (1) to (3): [(e, o)] segments of the labelled row's own open ink when the row is a line row
    (kind line), the segment has an end e within TOL_Z of the leader's anchor, and the leader leaves e away from the ink
    ((o - e) . (text - e) < 0). Term (4) (the segment runs along the line judged) is tested in collinear_issues."""
    if row.get("kind") != "line":
        return []
    anc = (float(t.xy[0]), float(t.xy[1]))
    tx = (float(t.xyann[0]), float(t.xyann[1]))
    out = []
    for poly, closed in ink_pieces(ax, row["id"]):
        if closed:
            continue
        for i in range(len(poly) - 1):
            for e, o in ((poly[i], poly[i + 1]), (poly[i + 1], poly[i])):
                if (math.hypot(e[0] - anc[0], e[1] - anc[1]) <= TOL_Z
                        and (o[0] - e[0]) * (tx[0] - e[0]) + (o[1] - e[1]) * (tx[1] - e[1]) < 0):
                    out.append((e, o))
    return out


def collinear_issues(ctx):
    """K4 rule (l), leader collinearity. 1.3 (h) r6 (M1 S3 r5 F1 and Rule 2 fix (b)); 1.4 step 0 R4 (Step 1.3 gate G2 rule
    scope, G3; C1.3-a; r6 reviewer N1); P0f (Designer P0D FIX L1 to L4, Topologist P0T TP1.4-1). Premise: a leader is
    followed by eye only where it does not merge with another line. On a script-drawn figure (the context's script, or
    its parent's for an inset Axes), in every view and every declared Axes, no label leader (text position to anchor,
    data coordinates, clipped to the Axes box) runs within COLLINEAR_DEG of, and within D of, a line of the families in
    COLLINEAR_FAMILIES (collinear_lines, plus every other label leader of the Axes, clipped the same way) over more than
    R; D and R are COLLINEAR_PAPER_MM and COLLINEAR_PAPER_RUN_MM on paper, converted per Axes (collinear_scale; an Axes
    without equal aspect is reported, premise). Relief (FIX L3): a line row's leader that leaves an end of its own open
    ink away from the ink (own_continuation) is exempt against a line that ink segment itself runs along under the same
    test (premise: the line marks the row's own position). One issue per leader and reference-line segment or gridline,
    per leader and tagged artist id for part edges and drawn lines, per pair of leaders for the leader family."""
    sp = getattr(ctx, "script_paths", None) or getattr(getattr(ctx, "parent", None), "script_paths", None)
    if not sp:
        return []
    rows_ = {r["id"]: r for r in ctx.spec.get("features", [])}
    out = []
    for pose, fig in (ctx.figs or {}).items():
        ax = fig.axes[0]
        D, R, prem = collinear_scale(ax)
        if prem:
            out.append(f"{pose}: {prem}")
            continue
        (x0, x1), (y0, y1) = sorted(ax.get_xlim()), sorted(ax.get_ylim())
        legs = []
        for t in ax.texts:
            g = t.get_gid() or ""
            xt = getattr(t, "xyann", None)
            if not g.startswith("label:") or xt is None:
                continue
            seg = _clip_box((float(xt[0]), float(xt[1])), (float(t.xy[0]), float(t.xy[1])), x0, x1, y0, y1)
            if seg is None or math.hypot(seg[1][0] - seg[0][0], seg[1][1] - seg[0][1]) <= R:
                continue
            legs.append((g[len("label:"):], seg[0], seg[1], t))
        if not legs:
            continue
        every = collinear_lines(ctx, ax, None)
        pairs = set()
        for i, (fid, p0, p1, t) in enumerate(legs):
            lines = collinear_lines(ctx, ax, fid, every=every) + [
                ("leader", (j, ofid), (q0, q1), None) for j, (ofid, q0, q1, _) in enumerate(legs) if j != i]
            own = own_continuation(ax, rows_.get(fid) or {}, t)
            seen = set()
            for fam, nm, (a, b), reg in lines:
                if _angle_off(p0, p1, a, b) > COLLINEAR_DEG or seg_distance(p0, p1, a, b) > D:
                    continue
                if fam in OWN_ROW_FAMILIES and nm in seen:
                    continue
                if fam == "leader" and frozenset((i, nm[0])) in pairs:
                    continue
                if own and any(_angle_off(oa, ob, a, b) <= COLLINEAR_DEG and _run_near_vis(oa, ob, a, b, None, mm=D) > R
                               for oa, ob in own):
                    continue
                run = _run_near_vis(p0, p1, a, b, reg, mm=D)
                if run <= R:
                    continue
                if fam in OWN_ROW_FAMILIES:   # one issue per leader and tagged artist id (its edges and hidden copy)
                    seen.add(nm)
                if fam == "leader":
                    pairs.add(frozenset((i, nm[0])))
                lab = {"part edge": f"part edge of {nm}", "drawn line": f"drawn line of {nm}",
                       "leader": f"leader of {nm[1] if fam == 'leader' else ''}"}.get(fam, nm)
                out.append(f"{pose}/{fid}: label leader runs {run:.1f} mm along {lab} within {D:.2f} mm (K4 collinear)")
    return out


TEXT_TOL_PX = 1.0   # 1.3 (h) r2 (Designer M1 S3 r1 F2, F3): text boxes shrunk by 1 px before a crossing or overlap counts


def _fig_texts(fig, r):
    """[(text artist, window extent)] of every visible, non-empty Text of the figure: Axes texts and annotations, titles,
    axis labels, tick labels, figure texts (display pixels)."""
    out = []
    seen = set()
    cands = list(fig.texts)
    for ax in fig.axes:
        cands += list(ax.texts) + [ax.title, ax._left_title, ax._right_title, ax.xaxis.label, ax.yaxis.label]
        for axis in (ax.xaxis, ax.yaxis):   # tick labels as drawn: ticks inside the view interval only
            cands += [lb for tk in axis._update_ticks() for lb in (tk.label1, tk.label2) if lb.get_visible()]
    for t in cands:
        if id(t) in seen or not t.get_visible() or not t.get_text().strip():
            continue
        seen.add(id(t))
        e = Text.get_window_extent(t, r)   # the letters only (an Annotation's own extent includes its arrow)
        if e.width <= 0 or e.height <= 0:
            continue
        if not (fig.bbox.x0 - 1e4 < e.x0 < fig.bbox.x1 + 1e4):
            continue
        out.append((t, e))
    return out


def _seg_box(a, b, box):
    """True when segment a-b (display) meets the open box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    if x1 <= x0 or y1 <= y0:
        return False
    inside = lambda p: x0 < p[0] < x1 and y0 < p[1] < y1  # noqa: E731
    if inside(a) or inside(b):
        return True
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return any(_segs_cross(a, b, corners[i], corners[(i + 1) % 4]) for i in range(4))


def text_overlap_issues(ctx):
    """1.3 (h) r2, K4 (i) (Designer M1 S3 r1 F2, F3). Premise of every leader and label rule: a label is read only when
    no other ink runs through its letters. (i1) The drawn leader of a label annotation (its arrow path as rendered, in
    display pixels) meets no text box of the figure: no other label, note, tick label, axis label or title, and not its
    own text (the leader leaves its own box on the side facing its anchor). (i2) No two text boxes of the figure overlap
    (labels, notes, tick labels of every Axes, titles). Boxes shrunk by TEXT_TOL_PX (1 px). Run once per figure (main
    Axes context), on a drawing of record: a figure built by a sketch script (ctx.script_paths set); a fixture figure
    without a script is a plant for another rule, not a layout."""
    if getattr(ctx, "axes_role", "main") != "main" or not getattr(ctx, "script_paths", None):
        return []
    out = []
    for name, fig in (ctx.figs or {}).items():
        fig = real_figure(fig)
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        tx = _fig_texts(fig, r)
        boxes = [(t, (e.x0 + TEXT_TOL_PX, e.y0 + TEXT_TOL_PX, e.x1 - TEXT_TOL_PX, e.y1 - TEXT_TOL_PX)) for t, e in tx]
        tname = lambda t: (t.get_gid() or repr(t.get_text().splitlines()[0][:40]))  # noqa: E731
        for t, _ in tx:
            g = t.get_gid() or ""
            ap = getattr(t, "arrow_patch", None)
            if not g.startswith("label:") or ap is None or not ap.get_visible():
                continue
            path = ap.get_path()
            vs = ap.get_transform().transform(path.vertices)
            segs = [(tuple(vs[i]), tuple(vs[i + 1])) for i in range(len(vs) - 1)]
            for t2, b2 in boxes:
                if any(_seg_box(a, b, b2) for a, b in segs):
                    who = "its own text" if t2 is t else f"the text of {tname(t2)}"
                    out.append(f"{name}/{g[len('label:'):]}: label leader runs through {who} (i1)")
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                (ta, a), (tb, b) = boxes[i], boxes[j]
                if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                    out.append(f"{name}: text {tname(ta)} overlaps text {tname(tb)} (i2)")
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
    if isinstance(a, FancyArrowPatch):   # 1.3 P4: load and look arrows draw no area (line, arrow kinds)
        return "line"
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
    if not plan and row.get("section_true"):   # 1.4 (h) r2 (M1 S4 F3): the cut-body outline, judged by K8 cut_outline_issues
        if not isinstance(artist, Line2D):
            return f"section outline sub-artist must be a Line2D (drawn as {type(artist).__name__})"
        return None
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


def expected_projection_par(kind, axis, parallel):
    """expected_projection with the axis-normal relation given (1.3 P4: section views)."""
    if axis is None or parallel is None:
        return None
    if kind in ("cylinder", "screw"):
        return "circle" if parallel else "rectangle"
    if kind in ("cone", "gear"):
        return "circle" if parallel else "trapezoid"
    return None


def axis_parallel(row, rec, view, normal):
    """1.3 P4 (O4): is the row's axis along the view normal? In a section view (reflected frame, normal along y') a row
    with axis X or Y and a place is radial (X) or tangential (Y) at its placed theta (S1, S2 meaning of X); without a
    place X and Y are literal. Axis Z lies in every vertical section plane."""
    axis = row.get("axis")
    if axis is None:
        return None
    if view in SECTION_VIEWS:
        if axis == "Z":
            return False
        pl = (rec or {}).get("place")
        if pl:
            t = math.radians(pl["theta"]) + (math.pi / 2 if axis == "Y" else 0.0)
            return abs(math.sin(t)) > abs(math.cos(t))
        return axis == normal
    return axis == normal


MARK_SUB = "line"


def _hull_contains(hull, v, tol=TOL_Z):
    """Half-space test of point v against every edge (p, q) of the CCW convex hull: cross(q - p, v - p) >= -tol |q - p|."""
    for i in range(len(hull)):
        p, q = hull[i], hull[(i + 1) % len(hull)]
        ex, ey = q[0] - p[0], q[1] - p[1]
        if ex * (v[1] - p[1]) - ey * (v[0] - p[0]) < -tol * math.hypot(ex, ey):
            return False
    return True


def _on_vertical_edge(v, polys, tol=TOL_Z):
    for P in polys:
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            if abs(a[0] - b[0]) <= tol and abs(v[0] - a[0]) <= tol and min(a[1], b[1]) - tol <= v[1] <= max(a[1], b[1]) + tol:
                return True
    return False


def _z_S_expr(ctx, pose, expr):
    import check_stack as _cs   # lazy: check_stack imports no sketch module (K6 import guard)
    names = ((ctx.stack or {}).get("poses", {}).get(pose, {}) or {}).get("vars_z_A", {})
    return _cs.to_shop_floor(_cs.eval_expr(expr, ctx.P, names), ctx.P)


def mark_issues(ctx, ax, pose, prow, arts):
    """Topologist P0T section 4 (signed in advance; landed 1.3 P4): K5 admits one Line2D <row>:line per row per pose as
    ink on its parent when M1 to M5 hold. Section form (1.3 P4, s3_spec anchor_bearing_c): M4 reads the convex hull of
    the parent's drawn pieces and M5 an endpoint on a vertical edge of any parent piece, which for a one-piece parent
    (S1 anchors) is the signed form."""
    fid = prow["id"] if prow else None
    m = (prow or {}).get("mark")
    if not m or m.get("sub") != MARK_SUB:   # M1
        return ["mark sub-artist without a mark declaration on its row (premise unenforced) (M1)"]
    if prow.get("kind") in NO_AREA_KINDS:   # M2
        return [f"mark on a {prow.get('kind')} row: the parent draws no area (M2)"]
    own = [x for x in tagged(ax).get(fid, []) if isinstance(x, Patch) and not getattr(x, "_sc_hidden_copy", False) and least_thickness(x) > TOL_Z]
    if not own:
        return [f"mark on {fid}: parent {fid} not drawn as an area at this pose (M2)"]
    if len(arts) != 1:   # M3 count
        return [f"{len(arts)} mark artists on {fid} (one per row per pose) (M3)"]
    a = arts[0]
    if not isinstance(a, Line2D):   # M3 type
        return [f"mark drawn as a {type(a).__name__}, not a Line2D (M3)"]
    pts = artist_polys(a)[0]
    if len(pts) != 2:
        return [f"mark with {len(pts)} vertices, needs 2 (M3)"]
    if ctx.view not in SIDE_VIEWS:
        return [f"mark not admitted in {ctx.view} (side and section views only) (M5)"]
    polys = [p for x in own for p in artist_polys(x)]
    hull = convex_hull([q for P in polys for q in P])
    out = []
    for v in pts:   # M4
        if not _hull_contains(hull, v):
            out.append(f"mark endpoint ({v[0]:.2f}, {v[1]:.2f}) outside the drawn {fid} (M4)")
    (x0, z0), (x1, z1) = pts
    if abs(z1 - z0) > TOL_Z:   # M5 direction
        out.append(f"mark not normal to the axis: dz {z1 - z0:.2f} (M5)")
    zw = _z_S_expr(ctx, pose, m["z"])
    if abs((z0 + z1) / 2 - zw) > TOL_Z:   # M5 place
        out.append(f"mark at z {(z0 + z1) / 2:.2f} against mark.z {zw:.2f} z_S ({m['z']}) (M5)")
    for v in pts:
        if not _on_vertical_edge(v, polys):
            out.append(f"mark endpoint ({v[0]:.2f}, {v[1]:.2f}) not on a vertical edge of {fid} (M5)")
    return out


def _in_any(v, polys, tol=TOL_Z):
    return any(len(P) >= 3 and (_inside(v, P) or min_distance([v], P) <= tol) for P in polys)


def sub_artist_issues(ctx, ax, pose, rows, gid, arts):
    """1.3 P4: admission of a <row>:<sub> artist. :line is a mark (mark_issues). Any other sub must be declared in the
    row's sub_artists; balls: Circle patches, every drawn point inside a drawn piece of the row (ink on the part);
    lever: one two-vertex Line2D whose ends equal the row's lever.from and lever.to (section frame u, z_A) within TOL_Z."""
    fid, sub = gid.rsplit(":", 1)
    prow = rows.get(fid)
    if prow is None:
        return [f"sub-artist of no spec row {fid}"]
    arts = [a for a in arts if not getattr(a, "_sc_hidden_copy", False)]   # 1.4 (h) r2 (TP1.4-5): a renderer hidden copy repeats the stroke; clause (6) judges it
    if sub == MARK_SUB:
        return mark_issues(ctx, ax, pose, prow, arts)
    if sub not in (prow.get("sub_artists") or []):
        return [f"sub-artist {sub} not declared in {fid} sub_artists"]
    if sub == "arc":   # 1.3 (h) r2 (Topologist TP1.3-13): the plan theta arc, no parent area needed
        return arc_issues(ctx, ax, pose, prow, arts)
    if sub == "ext":   # 1.3 (h) r3 (Designer r2 item 3): dimension extension lines, the parent is a line row
        return ext_issues(ctx, ax, pose, prow, arts)
    own = [x for x in tagged(ax).get(fid, []) if isinstance(x, Patch) and not getattr(x, "_sc_hidden_copy", False)]
    if not own:
        return [f"{sub} on {fid}: parent {fid} not drawn at this pose"]
    if sub == "root":   # 1.3 (h) r2 (Topologist TP1.3-15): the simplified thread, two dashed root lines
        return root_issues(ctx, ax, pose, prow, arts, own)
    if sub == "slits":   # 1.4 P4: section-view tick class (Topologist P2r 3.1, form (a))
        return slit_issues(ctx, ax, pose, prow, arts, own, rows)
    if sub == "wing":   # 1.4 P4: beyond part by declared x_band (Designer P3a O3)
        return wing_issues(ctx, ax, pose, prow, arts, own)
    if sub == "sweep":   # 1.4 P4: S3 sweep form as a sub-artist
        return sweep_issues(ctx, ax, pose, prow, arts, own)
    if sub == "balls":
        polys = [p for x in own for p in artist_polys(x)]
        out = []
        for a in arts:
            if not isinstance(a, Circle):
                out.append(f"balls drawn as a {type(a).__name__}, not a Circle")
                continue
            bad = [v for P in artist_polys(a) for v in P if not _in_any(v, polys)]
            if bad:
                out.append(f"ball at ({a.center[0]:.2f}, {a.center[1]:.2f}) outside the drawn {fid} ({len(bad)} points)")
        return out
    if sub == "lever":
        lv = prow.get("lever") or {}
        if not lv.get("from") or not lv.get("to"):
            return [f"lever on {fid} without lever.from / lever.to in the spec"]
        if len(arts) != 1 or not isinstance(arts[0], Line2D) or len(artist_polys(arts[0])[0]) != 2:
            return [f"lever on {fid}: needs one two-vertex Line2D ({len(arts)} artists)"]
        import check_stack as _cs
        names = ((ctx.stack or {}).get("poses", {}).get(pose, {}) or {}).get("vars_z_A", {})
        want = [(_cs.eval_expr(e[0], ctx.P, names), _cs.to_shop_floor(_cs.eval_expr(e[1], ctx.P, names), ctx.P)) for e in (lv["from"], lv["to"])]
        got = artist_polys(arts[0])[0]
        out = []
        for w, g, nm in zip(want, got, ("from", "to")):
            if math.hypot(w[0] - g[0], w[1] - g[1]) > TOL_Z:
                out.append(f"lever {nm} drawn ({g[0]:.2f}, {g[1]:.2f}) vs spec ({w[0]:.2f}, {w[1]:.2f})")
        return out
    return [f"sub-artist {sub} has no admission rule"]


ARC_DEG_TOL = 0.1   # deg: the arc ends at theta0 and theta1 within this


def arc_issues(ctx, ax, pose, prow, arts):
    """1.3 (h) r2 (Topologist TP1.3-13). Admission of <row>:arc, the theta-sense arc of a plan axes mark. Premise: the arc
    is the one artist that states the theta sense, counter-clockwise from +X seen from +Z (ASSEMBLY.md Coordinate frame),
    so its sense is a sign check. Spec: row field arc {r, theta0, theta1} (r an expression). (a1) plan_xy only. (a2) one
    Line2D; every point on the circle about the origin at r within TOL_Z. (a3) consecutive points turn counter-clockwise:
    cross(p_i, p_i+1) > 0. (a4) first point at theta0, last at theta1 within ARC_DEG_TOL, theta1 > theta0. (a5) an optional
    FancyArrowPatch head: both ends on the circle within TOL_Z, the head end at theta1 within 5 deg, and (head - tail) .
    (-sin theta1, cos theta1) > 0. K8 plan_extent reads the parent row only (the gid <row>:arc is not the row)."""
    import check_stack as _cs
    if ctx.view != "plan_xy":
        return [f"arc on {prow['id']} admitted in plan_xy only (view {ctx.view})"]
    spec_arc = prow.get("arc") or {}
    if not all(k in spec_arc for k in ("r", "theta0", "theta1")):
        return [f"arc on {prow['id']} without arc.r / theta0 / theta1 in the spec"]
    r = float(_cs.eval_expr(str(spec_arc["r"]), ctx.P, {}))
    t0, t1 = float(spec_arc["theta0"]), float(spec_arc["theta1"])
    out = []
    if not t1 > t0:
        out.append(f"arc theta1 {t1:g} not above theta0 {t0:g}")
    lines = [a for a in arts if isinstance(a, Line2D)]
    heads = [a for a in arts if isinstance(a, FancyArrowPatch)]
    if len(lines) != 1 or len(lines) + len(heads) != len(arts) or len(heads) > 1:
        return out + [f"arc on {prow['id']}: needs one Line2D and at most one FancyArrowPatch head ({len(arts)} artists)"]
    pts = artist_polys(lines[0])[0]
    for x, y in pts:
        d = abs(math.hypot(x, y) - r)
        if d > TOL_Z:
            out.append(f"arc point ({x:.2f}, {y:.2f}) {d:.2f} off the circle r {r:g}")
            break
    for i in range(len(pts) - 1):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        if xa * yb - ya * xb <= 0:
            out.append(f"arc turns clockwise at point {i} (cross {xa * yb - ya * xb:.3f}); theta runs counter-clockwise from +X")
            break
    ang = lambda q: math.degrees(math.atan2(q[1], q[0]))  # noqa: E731
    for nm, q, want in (("start", pts[0], t0), ("end", pts[-1], t1)):
        dd = (ang(q) - want + 180) % 360 - 180
        if abs(dd) > ARC_DEG_TOL:
            out.append(f"arc {nm} at {ang(q):.2f} deg against {want:g}")
    for h in heads:
        tail, head = arrow_ends(h)
        if any(abs(math.hypot(*q) - r) > TOL_Z for q in (tail, head)):
            out.append("arc head ends off the circle")
        tx, ty = -math.sin(math.radians(t1)), math.cos(math.radians(t1))
        if (head[0] - tail[0]) * tx + (head[1] - tail[1]) * ty <= 0:
            out.append("arc head points against theta (clockwise)")
        if abs((ang(head) - t1 + 180) % 360 - 180) > 5:
            out.append(f"arc head at {ang(head):.2f} deg, not at theta1 {t1:g}")
    return out


EXT_OVERSHOOT_MAX = 3.0   # mm: an extension line ends past its dimension line by 0 to this (Designer 1.3 (h) r2 e3)


def ext_issues(ctx, ax, pose, prow, arts):
    """1.3 (h) r3 (Designer r2 item 3, raised by The Designer). Admission of <row>:ext, the extension lines of a dimension
    row. Premise: an extension line carries the measured feature out to the dimension line and states no part, so it is
    admitted only where (e4) its parent is a reference row of kind line (spec ext {screw: row}); (e1) it is a horizontal
    two-vertex solid Line2D at the z of one end of the parent's z_rule (TOL_Z), one line per end; (e2) it starts on the
    measured feature, the screw edge facing the dimension line, u_c -+ place half_width (TOL_Z); (e3) it ends past the
    dimension line (the parent's drawn vertical line) by 0 to EXT_OVERSHOOT_MAX and no further. The admitted artist has
    no area; the parent's projected_x and projected_extent read the dimension line alone (gid <row>:ext is not the row)."""
    fid = prow["id"]
    if not prow.get("reference") or prow.get("kind") != "line":
        return [f"ext on {fid}: parent is not a reference line row (e4)"]
    spec_ext = prow.get("ext") or {}
    scr = spec_ext.get("screw")
    f, fs = _feat(ctx, pose, fid), _feat(ctx, pose, scr) if scr else {}
    pl = (fs or {}).get("place")
    if not scr or not pl or f.get("z_min") is None:
        return [f"ext on {fid}: spec ext.screw names no placed row, or the parent has no z_rule"]
    uc, half = sum(pl["x"]) / 2, pl["half_width"]
    dim = [q for a in tagged(ax).get(fid, []) if isinstance(a, Line2D) for q in artist_polys(a)]
    xs = [v[0] for q in dim for v in q]
    if not xs:
        return [f"ext on {fid}: dimension line {fid} not drawn"]
    ud = sum(xs) / len(xs)
    side = 1.0 if ud > uc else -1.0
    u0 = uc + side * half
    out, ends = [], []
    for a in arts:
        if not isinstance(a, Line2D) or len(artist_polys(a)[0]) != 2:
            out.append(f"ext on {fid}: {type(a).__name__} is not a two-vertex Line2D")
            continue
        if a.get_linestyle() not in SOLID_STYLES:
            out.append(f"ext on {fid}: drawn {a.get_linestyle()!r}, extension lines are solid")
        (xa, za), (xb, zb) = artist_polys(a)[0]
        if abs(za - zb) > TOL_Z:
            out.append(f"ext on {fid}: not horizontal (dz {zb - za:.2f}) (e1)")
            continue
        z = (za + zb) / 2
        near = min((f["z_min"], f["z_max"]), key=lambda e: abs(e - z))
        if abs(near - z) > TOL_Z:
            out.append(f"ext on {fid}: at z {z:.2f}, not at a z_rule end ({f['z_min']:.2f} or {f['z_max']:.2f}) (e1)")
            continue
        ends.append(near)
        p_in, p_out = sorted(((xa, za), (xb, zb)), key=lambda q: abs(q[0] - uc))
        if abs(p_in[0] - u0) > TOL_Z:
            out.append(f"ext on {fid}: starts at u {p_in[0]:.2f}, not on the screw edge {u0:.2f} (e2)")
        over = (p_out[0] - ud) * side
        if over < -TOL_Z or over > EXT_OVERSHOOT_MAX + TOL_Z:
            out.append(f"ext on {fid}: ends {over:.2f} past the dimension line u {ud:.2f} (0 to {EXT_OVERSHOOT_MAX:g}) (e3)")
    if not out and sorted(ends) != sorted((f["z_min"], f["z_max"])):
        out.append(f"ext on {fid}: one line per z_rule end needed, drawn at {sorted(round(e, 2) for e in ends)} (e1)")
    return out


def root_issues(ctx, ax, pose, prow, arts, own):
    """1.3 (h) r2 (Topologist TP1.3-15). Admission of <row>:root, the simplified thread of a screw drawn in a side or
    section view: two dashed root lines. Spec: row field root {from, to, d} (z_A expressions; d the root diameter).
    Premise: the lead is in the label; the lines state where the thread runs and its root, nothing else. (r1) side or
    section view. (r2) exactly two Line2D, each two vertices, vertical (|dx| <= TOL_Z), dashed. (r3) the two lines at
    u_c - d / 2 and u_c + d / 2 within TOL_Z, u_c the centre of the parent's drawn pieces over the thread span. (r4) each
    runs from `from` to `to` (z_S) within TOL_Z. (r5) every vertex inside the drawn parent pieces."""
    import check_stack as _cs
    if ctx.view not in SIDE_VIEWS:
        return [f"root on {prow['id']} admitted in a side or section view only (view {ctx.view})"]
    rt = prow.get("root") or {}
    if not all(k in rt for k in ("from", "to")) or not ("d" in rt or "r" in rt):
        return [f"root on {prow['id']} without root.from / to / d (or r) in the spec"]
    names = ((ctx.stack or {}).get("poses", {}).get(pose, {}) or {}).get("vars_z_A", {})
    z0 = _cs.to_shop_floor(_cs.eval_expr(str(rt["from"]), ctx.P, names), ctx.P)
    z1 = _cs.to_shop_floor(_cs.eval_expr(str(rt["to"]), ctx.P, names), ctx.P)
    d = float(_cs.eval_expr(str(rt["d"]), ctx.P, names)) if "d" in rt else 2 * float(_cs.eval_expr(str(rt["r"]), ctx.P, names))
    polys = [q for x in own for q in artist_polys(x) if len(q) >= 3]
    if prow.get("section_true"):   # 1.4 P4: a true section mirrored about u = 0 (section_true_issues): u_c is the axis
        uc = 0.0
    else:
        span = [q for q in polys if min(v[1] for v in q) <= z0 + TOL_Z and max(v[1] for v in q) >= z1 - TOL_Z]
        if not span:
            return [f"root on {prow['id']}: no drawn piece of {prow['id']} spans z {z0:.2f} to {z1:.2f}"]
        xs = [v[0] for v in span[0]]
        uc = (min(xs) + max(xs)) / 2
    out = []
    if len(arts) != 2 or not all(isinstance(a, Line2D) and len(artist_polys(a)[0]) == 2 for a in arts):
        return [f"root on {prow['id']}: needs two two-vertex Line2D ({len(arts)} artists)"]
    got = []
    for a in arts:
        (xa, ya), (xb, yb) = artist_polys(a)[0]
        if abs(xa - xb) > TOL_Z:
            out.append(f"root line not vertical (dx {xb - xa:.2f})")
        if a.get_linestyle() in SOLID_STYLES:
            out.append("root line drawn solid (dashed: hidden thread root)")
        lo, hi = sorted((ya, yb))
        if abs(lo - z0) > TOL_Z or abs(hi - z1) > TOL_Z:
            out.append(f"root line z {lo:.2f} to {hi:.2f} against {z0:.2f} to {z1:.2f}")
        if not all(_in_any(v, polys) for v in ((xa, ya), (xb, yb))):
            out.append(f"root line at u {xa:.2f} leaves the drawn {prow['id']}")
        got.append((xa + xb) / 2)
    want = sorted((uc - d / 2, uc + d / 2))
    for w, g in zip(want, sorted(got)):
        if abs(w - g) > TOL_Z:
            out.append(f"root line at u {g:.2f} against {w:.2f} (u_c {uc:.2f} -+ d_r {d:g} / 2)")
    return out


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
    sub_seen = {}
    for pose, fig in ctx.figs.items():
        drawn = tagged(fig.axes[0])
        for a in artists(fig.axes[0]):
            gid = a.get_gid()
            if not gid:
                issues.append(f"{pose}: untagged {type(a).__name__}")
                continue
            row = rows.get(gid)
            if row is None and ":" in gid and not gid.endswith(SUB_SUFFIXES):
                # 1.3 P4: mark admission <row>:line (Topologist P0T section 4, M1 to M5) and declared sub-artists
                # (<row>:balls, <row>:lever; spec field sub_artists)
                n += 1
                if gid in sub_seen.setdefault(pose, set()):
                    continue
                sub_seen[pose].add(gid)
                for t in sub_artist_issues(ctx, fig.axes[0], pose, rows, gid, drawn.get(gid, [])):
                    issues.append(f"{pose}/{gid}: {t}")
                continue
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
            if ctx.view in SIDE_VIEWS and st_admitted(ctx, pose, row, a):   # 1.4 P4 (O7): true-section piece
                continue
            if ctx.view in SECTION_VIEWS:   # 1.3 P4 (O4): a radial axis X at its placed theta, against the section normal
                want = expected_projection_par(row.get("kind"), row.get("axis"), axis_parallel(row, _feat(ctx, pose, gid), ctx.view, normal))
            else:
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
            elif got == "circle" and normal in ("Y", "X") and row.get("kind") not in ("sphere",):
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
            if any(isinstance(a, FancyArrowPatch) for a in drawn[fid]):   # 1.3 P4: an arrow spans tail to head
                ez = extent_z([list(e) for e in (arrow_ends(a) for a in drawn[fid]) if e])
            else:
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
            me = geom_pieces(ax, row)
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
    if getattr(ctx, "axes_role", None) == "main" and getattr(ctx, "parent", None) is not None:
        issues += class_by_axes_issues(ctx.parent.spec)   # P5f (Topologist FIX 7)

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
    # 1.4 (h) r2 (Topologist FIX TP1.4-3, TP1.1-11 class): the TP-4 lint on every row with section_true in a side or
    # section view. Premise: a revolved row's band along the view normal equals its radial extent, so the depth band holds
    # [-r_max, r_max], r_max the largest |r| over the row's section_true pieces with plane_cuts ignored (the revolve).
    if side:
        st_linted = set()
        for pose in ctx.figs:
            pr_ = (ctx.stack or {}).get("poses", {}).get(pose, {}) or {}
            for row in rows_list:
                fid = row["id"]
                if fid in st_linted or not row.get("section_true") or not applies(row, pose):
                    continue
                rec = (pr_.get("features") or {}).get(fid) or {}
                dep = rec.get("depth_spec") or rec.get("depth")
                if not dep:
                    continue
                st_linted.add(fid)
                prof = {k: v for k, v in row.items() if k != "plane_cuts"}
                rmax = max(abs(p[0]) for _, _, pts in section_true_polys(ctx.P, pr_.get("vars_z_A", {}), prof, z_S=False) for p in pts)
                lo, hi = sorted(dep)
                if lo > -rmax + TOL_C or hi < rmax - TOL_C:
                    issues.append(f"{fid}: spec depth band [{lo:.2f}, {hi:.2f}] does not contain the true section radius "
                                  f"[{-rmax:.2f}, {rmax:.2f}] (section_true, TP1.4-3)")
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
    if getattr(ctx, "axes_role", None) == "main" and getattr(ctx, "parent", None) is not None:
        issues += orphan_predicates(ctx.parent.spec)   # 1.3 P4 (TP-7)
        if ctx.view in SECTION_VIEWS:
            issues += section_look_issues(ctx.parent.spec, ctx.view)   # P5f (Topologist FIX 2)
            if ctx.parent.stack:
                issues += omitted_row_issues(ctx, ctx.parent)   # P5f (Topologist FIX 3 b)
                issues += not_drawn_band_issues(ctx, ctx.parent)   # 1.3 (h) r2 (Topologist TP1.3-12)
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
            if row.get("kind") == "line" and row.get("reference") and side:
                # 1.3 (h) r4 (Designer D-r3-1): a dimension's arrowhead terminators are marks on its line, not its extent
                # (the geom_pieces premise, P4); premise check: both ends of every arrow of the row lie on the row's line ink
                me = geom_pieces(ax, row)
                issues += terminator_issues(ax, fid, pose, script=bool(getattr(ctx, "script_paths", None)))
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
                    pts = [p for poly in geom_pieces(ax, row) for p in poly]
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
            if side and row.get("section_true") and row.get("kind") not in NO_AREA_KINDS:   # 1.4 P4 (O7) premise
                if me:
                    n += 1
                    issues += [f"{pose}/{fid} section_true: {t}" for t in section_true_issues(ctx, ax, pose, row)]
                else:
                    issues.append(f"{pose}/{fid} section_true: untestable, {fid} not drawn")
                    absent += 1
            if ctx.view in SECTION_VIEWS and row.get("section_u"):
                if me:
                    n += 1
                    issues += [f"{pose}/{fid} section_u: {t}" for t in section_u_issues(ctx, pose, row, me)]
                elif not pl:
                    issues.append(f"{pose}/{fid} section_u: untestable, {fid} not drawn")
                    absent += 1
            if pl and side:
                if not me:
                    issues.append(f"{pose}/{fid} projected_x: untestable, {fid} not drawn")
                    absent += 1
                else:
                    n += 1
                    ex = extent_x(me)
                    cx = (ex[0] + ex[1]) / 2
                    want = pl["r_c"] * math.cos(math.radians(pl["theta"]))
                    if ctx.view in SECTION_VIEWS and row.get("section_u"):
                        want = cx   # 1.3 P4: the true section need not be centred on the footprint; section_u_issues rules it
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
            me_all = me
            for pr in row.get("sense") or []:
                if id(pr) in bad or (pr.get("poses") and pose not in pr["poses"]):
                    continue
                kind = pr["pred"]
                other_id = None if kind == "between" else (pr.get("of") or pr.get("seat") or pr.get("axis"))
                other = pieces(ax, other_id) if other_id else None
                # 1.4 P4 (O6): piece / of_piece / seat_piece read the named section_true pieces only (PIECE_ATTR)
                me = named_pieces(ax, fid, pr["piece"]) if pr.get("piece") else me_all
                op = pr.get("of_piece") or pr.get("seat_piece")
                if op and other:
                    other = named_pieces(ax, other_id, op)
                if not me or (other_id and not other):
                    nd = (f"{fid}" + (f" piece {pr['piece']}" if pr.get("piece") and me_all else "")) if not me else (f"{other_id}" + (f" piece {op}" if op else ""))
                    issues.append(f"{pose}/{fid} {kind} {other_id or ''}: untestable, {nd} not drawn")
                    absent += 1
                    continue
                n += 1
                if kind == "between":   # 1.4 P4 (O6, Designer 1.4 (a) section 12); P5f: min(z_mid - z_max(below), z_min(above) - z_mid) > 0
                    lo_id, hi_id = pr.get("below"), pr.get("above")
                    lo_p = named_pieces(ax, lo_id, pr["below_piece"]) if pr.get("below_piece") else pieces(ax, lo_id or "")
                    hi_p = named_pieces(ax, hi_id, pr["above_piece"]) if pr.get("above_piece") else pieces(ax, hi_id or "")
                    if not lo_id or not hi_id:
                        issues.append(f"{pose}/{fid} between: spec error, needs below and above")
                    elif not lo_p or not hi_p:
                        issues.append(f"{pose}/{fid} between {lo_id} and {hi_id}: untestable, {lo_id if not lo_p else hi_id} not drawn")
                        absent += 1
                    else:
                        ez_ = extent_z(me)
                        zm = (ez_[0] + ez_[1]) / 2
                        a_, b_ = zm - extent_z(lo_p)[1], extent_z(hi_p)[0] - zm
                        if min(a_, b_) <= 0:   # P5f (Topologist F4): the order, both factors > 0 (the product passed two negatives)
                            issues.append(f"{pose}/{fid} between {lo_id} and {hi_id}: (z_mid - {lo_id} z_max) {a_:.2f}, ({hi_id} z_min - z_mid) {b_:.2f}, needs both > 0")
                    continue
                if kind == "vertical_edge":   # 1.4 P4: S4-d (Sean STOP S4-A), the bore edge of the piece vertical
                    t = vertical_edge_issue(me, float(pr.get("tol", TOL_Z)))
                    if t:
                        issues.append(f"{pose}/{fid} vertical_edge {pr.get('piece')}: {t}")
                    continue
                if kind == "taper" and pr.get("edge") == "inner":   # 1.4 P4: holder bore cone narrows on its inner edge
                    t = inner_taper_issue(me, pr["narrows"])
                    if t:
                        issues.append(f"{pose}/{fid} taper narrows {pr['narrows']} (inner edge): {t}")
                    continue
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
                    if pr.get("min_bearing") is not None:   # 1.4 P2f (Designer P3a FIX 3): radial bearing, not z only
                        w, per = bearing_width(me, other)
                        if w < float(pr["min_bearing"]) - 1e-9:
                            issues.append(f"{pose}/{fid} rests_on {other_id}: bearing width {w:.3f} mm on the seat top face "
                                          f"(per side {', '.join(f'{v:.3f}' for v in per) or 'none'}), needs >= {float(pr['min_bearing']):g} (min_bearing)")
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
                elif kind == "azimuth" and ctx.view in SECTION_VIEWS:
                    # 1.3 P4 (O4): a section shows the azimuth as the drawn u centre, u = r_c sin(azimuth) (reflected
                    # frame: x' centre = r_c cos(90 - azimuth)); a row with no place has no section azimuth (spec error)
                    if not pl:
                        issues.append(f"{pose}/{fid} azimuth: spec error, no place to project in {ctx.view}")
                    else:
                        want = _key_index(ctx.P, pr["expr"])
                        ex = extent_x(me)
                        wu = pl["r_c"] * math.sin(math.radians(want))
                        if abs((ex[0] + ex[1]) / 2 - wu) > TOL_Z:
                            issues.append(f"{pose}/{fid} azimuth (section): drawn u centre {(ex[0] + ex[1]) / 2:.2f} vs r_c sin({pr['expr']} = {want:g}) {wu:.2f}")
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
                elif kind == "points":
                    for t in points_issues(ax, fid, pr["dir"]):
                        issues.append(f"{pose}/{fid} points {pr['dir']}: {t}")
                elif kind == "look_direction":
                    for t in look_direction_issues(ax, fid, pr["toward"]):
                        issues.append(f"{pose}/{fid} look_direction {pr['toward']}: {t}")
                elif kind == "axes_not_inverted":
                    for t in axes_arrows_issues(ax, fid):
                        issues.append(f"{pose}/{fid} axes_not_inverted: {t}")
                elif kind == "mirror_about_radial":
                    t = mirror_radial_issue(me, pl, plan)
                    if t:
                        issues.append(f"{pose}/{fid} mirror_about_radial: {t}")
        if plan and ctx.stack:
            nc, ci = cover_issues(ctx, ax, pose, rows_list)
            n += nc
            issues += ci
        if ctx.view in SECTION_VIEWS and ctx.stack:   # 1.3 P4: renderer section convention
            nc, ci = section_convention_issues(ctx, ax, pose)
            n += nc
            issues += ci
        elif ctx.view in SIDE_VIEWS and ((ctx.spec or {}).get("section") or {}).get("hatch_adjacency_gap") is not None:
            n += 1   # 1.4 P6 (Designer P2r 1.4 item 5): the adjacency lint on every Axes of a spec that declares the gap (S1 r9)
            issues += hatch_adjacency_issues(ctx, ax, pose)
        if ctx.view in SIDE_VIEWS and one_body_groups(ctx.spec):   # 1.4 (h) r2 (M1 S4 F3): one outlined region per cut body
            n += 1
            issues += cut_outline_issues(ctx, ax, pose)
    return result("K8", not issues, _summ(issues) if issues else f"{n} predicate(s) hold, axes not inverted", measured=len(issues), threshold=0,
                  n_issues=len(issues), cause=_cause(absent, len(issues)), issues=list(issues), absent=absent)


# ======================================================================== 1.3 P4: arrows and the section convention

DIRS = {"+Z": (0.0, 1.0), "-Z": (0.0, -1.0), "+X": (1.0, 0.0), "-X": (-1.0, 0.0), "+Y": (0.0, 1.0), "-Y": (0.0, -1.0),
        "+U": (1.0, 0.0), "-U": (-1.0, 0.0)}
DIR_TOL = 0.1   # |cross| / |d|: an arrow within about 5.7 deg of its stated direction


def _arrows(ax, fid):
    return [e for e in (arrow_ends(a) for a in tagged(ax).get(fid, []) if isinstance(a, FancyArrowPatch)) if e]


def points_issues(ax, fid, d):
    """1.3 P4 (s3_spec load arrows): the row's FancyArrowPatch arrows point along d (+Z, -Z: head minus tail along the
    direction, |cross| <= DIR_TOL |d|), or, for d = apart, two arrows on one line with the heads farther apart than the
    tails (tension in the member between them)."""
    arr = _arrows(ax, fid)
    if not arr:
        return ["no arrow (FancyArrowPatch) drawn"]
    if d == "apart":
        if len(arr) != 2:
            return [f"{len(arr)} arrows, needs 2"]
        (t0, h0), (t1, h1) = arr
        d0, d1 = (h0[0] - t0[0], h0[1] - t0[1]), (h1[0] - t1[0], h1[1] - t1[1])
        n0, n1 = math.hypot(*d0), math.hypot(*d1)
        out = []
        if d0[0] * d1[0] + d0[1] * d1[1] >= 0 or abs(d0[0] * d1[1] - d0[1] * d1[0]) > DIR_TOL * n0 * n1:
            out.append("arrows not of opposite senses on one line (P5f, Topologist FIX 4)")
        if math.dist(h0, h1) <= math.dist(t0, t1):
            out.append(f"heads {math.dist(h0, h1):.2f} apart against tails {math.dist(t0, t1):.2f} (arrows point together: compression)")
        return out
    if d not in DIRS:
        return [f"spec error, unknown direction {d!r}"]
    ux, uy = DIRS[d]
    out = []
    for t, h in arr:
        dx, dy = h[0] - t[0], h[1] - t[1]
        L = math.hypot(dx, dy)
        if L <= TOL_Z or dx * ux + dy * uy <= 0 or abs(dx * uy - dy * ux) > DIR_TOL * L:
            out.append(f"arrow ({t[0]:.1f}, {t[1]:.1f}) -> ({h[0]:.1f}, {h[1]:.1f}) does not point {d}")
    return out


def look_direction_issues(ax, fid, toward):
    """1.3 P4 (s3_spec section_line): a cutting-plane line in plan on x = 0 (a two-vertex Line2D, both ends |x| <= TOL_Z)
    and at least one look arrow (FancyArrowPatch) under the row, every arrow pointing `toward` (the viewer looks that
    way; A-A from +X looks toward -X)."""
    lines = [artist_polys(a)[0] for a in tagged(ax).get(fid, []) if isinstance(a, Line2D)]
    out = []
    if not any(len(p) >= 2 and all(abs(x) <= TOL_Z for x, _ in p) for p in lines):
        out.append("no cutting-plane line on x = 0")
    out += points_issues(ax, fid, toward)
    return out


def axes_arrows_issues(ax, fid):
    """1.3 P4 (s3_spec plan_axes): the Axes is not inverted and the row's drawn axis marks run from the origin toward +X
    and +Y (drawn points with x >= -TOL_Z and y >= -TOL_Z, reaching x > TOL_Z and y > TOL_Z)."""
    out = []
    if ax.xaxis_inverted() or ax.yaxis_inverted():
        out.append(f"Axes inverted (x {ax.xaxis_inverted()}, y {ax.yaxis_inverted()})")
    pts = [q for P in pieces(ax, fid) for q in P]
    if not pts:
        return out + ["axis marks not drawn"]
    if min(x for x, _ in pts) < -TOL_Z or min(y for _, y in pts) < -TOL_Z or max(x for x, _ in pts) <= TOL_Z or max(y for _, y in pts) <= TOL_Z:
        out.append("axis marks do not run from the origin toward +X and +Y")
    return out


HATCH = {"aluminium": "//", "extrusion": "xx", "steel": "\\\\", "brass": "..", "plastic": "oo"}
SECTION_CLASSES = ("cut", "unsectioned", "beyond", "reference")


def _area_artists(ax, fid):
    return [a for a in tagged(ax).get(fid, []) if isinstance(a, Patch) and not isinstance(a, FancyArrowPatch)]


def _cut_polys(ctx, ax):
    rows = ctx.spec.get("features", [])
    return [P for r in rows if r.get("section_class") == "cut" for a in _area_artists(ax, r["id"]) for P in artist_polys(a) if len(P) >= 3]


def _behind(a, cut):
    """(inside, outside) sample counts of artist a against the drawn cut pieces (strict inside)."""
    smp = _cover_samples(a)
    ins = sum(1 for p in smp if any(_inside(p, P) for P in cut))
    return ins, len(smp) - ins


def render_section(ctx, ax, pose):
    """1.3 P4 renderer section convention (s3_spec section.convention): cut rows hatched with their material pattern
    (HATCH[row.hatch]); unsectioned rows unhatched, outline drawn above the cut rows (zorder 3); beyond rows unhatched,
    solid where visible and dashed where every sample lies inside a drawn cut piece; reference rows untouched. Rows in
    front of the plane or past one profile width are not drawn by the script (figure note); the check reports any."""
    sctx = axes_context(ctx, main_axes_id(ctx.spec.get("view"))) if needs_split(ctx) else ctx
    rows = sctx.spec.get("features", [])
    for r in rows:
        if r.get("section_class") == "cut":
            for a in _area_artists(ax, r["id"]):
                a.set_hatch(cut_hatch(sctx, pose, r, a))
                a.set_zorder(1)
    for r in rows:
        if r.get("section_class") == "unsectioned":
            for a in _area_artists(ax, r["id"]):
                a.set_hatch(None)
                a.set_zorder(3)
    cut = _cut_polys(sctx, ax)
    for r in rows:
        if r.get("section_class") == "beyond":
            for a in _area_artists(ax, r["id"]):
                a.set_hatch(None)
                ins, outs = _behind(a, cut)
                a.set_linestyle("--" if ins and not outs else "-")
    draw_cut_outlines(sctx.spec, ax)   # 1.4 (h) r2 (M1 S4 F3): one outlined region per cut body, before the occlusion split
    render_occlusion(sctx, ax)


# ---------------------------------------------------------------- 1.4 (h) r2: one outlined region per cut body
# M1 S4 r1 F3, S3 r8 F1, S1 r9 (carried); Topologist P7b section 2 predicate. A cut body (a section_true row and its
# one_body partners) is drawn as its pieces, filled and hatched with no stroked edge, plus one outline: the boundary of
# the union of the drawn pieces (sub-artist <first row>:outline, solid Line2D polylines). The pieces stay in the spec and
# in the figure for K5 to K8 (they read the piece patches, never the outline).
OUTLINE_EPS = 0.02   # mm: side-test offset of an outline segment (Topologist P7b section 2)
OUTLINE_STEP = 0.5   # mm: sample step along outline and boundary segments (K8 cut_outline_issues)


def one_body_groups(spec):
    """[[row ids]]: the section_true rows of the spec grouped by one_body neighbour declarations (neighbour kind
    one_body, either direction), spec order; the first id of a group names its :outline sub-artist."""
    rows = [r for r in (spec or {}).get("features", []) if r.get("section_true")]
    ids = [r["id"] for r in rows]
    par = {i: i for i in ids}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for r in rows:
        for nb in r.get("neighbours") or []:
            if nb.get("kind") == "one_body" and nb.get("id") in par:
                a, b = find(r["id"]), find(nb["id"])
                if a != b:
                    par[max(a, b, key=ids.index)] = min(a, b, key=ids.index)
    out = {}
    for i in ids:
        out.setdefault(find(i), []).append(i)
    return [out[k] for k in ids if k in out]


def _seg_x(a, b, c, d):
    """Parameter t on a-b of a proper crossing with c-d, else None."""
    r = (b[0] - a[0], b[1] - a[1])
    q = (d[0] - c[0], d[1] - c[1])
    den = r[0] * q[1] - r[1] * q[0]
    if abs(den) < 1e-12:
        return None
    t = ((c[0] - a[0]) * q[1] - (c[1] - a[1]) * q[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    return t if 1e-9 < t < 1 - 1e-9 and -1e-9 <= u <= 1 + 1e-9 else None


def _in_material(p, polys):
    """p in the closed union of convex polygons (a point on a seam between two pieces is in material)."""
    return any(_inside(p, q) for q in polys if len(q) >= 3)


def body_boundary(polys, eps=OUTLINE_EPS):
    """Segments [(a, b)] of the boundary of the union of convex polygons: every edge is cut at the vertices of the other
    polygons lying on it and at proper crossings with their edges; a sub-segment is kept when exactly one side of its
    midpoint (offset eps along the edge normal) lies in material; coincident sub-segments are kept once."""
    polys = [[tuple(map(float, v)) for v in q] for q in polys if len(q) >= 3]
    out, seen = [], set()
    for P in polys:
        for a, b in _edges(P):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < 1e-9:
                continue
            ts = {0.0, 1.0}
            for Q in polys:
                for v in Q:
                    if _pt_seg(v, a, b) <= 1e-6:
                        ts.add(max(0.0, min(1.0, ((v[0] - a[0]) * (b[0] - a[0]) + (v[1] - a[1]) * (b[1] - a[1])) / (L * L))))
                for c, d in _edges(Q):
                    t = _seg_x(a, b, c, d)
                    if t is not None:
                        ts.add(t)
            ts = sorted(ts)
            nx, ny = (b[1] - a[1]) / L, -(b[0] - a[0]) / L
            for t0, t1 in zip(ts, ts[1:]):
                if (t1 - t0) * L < 1e-6:
                    continue
                p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
                p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
                m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
                s1 = _in_material((m[0] + eps * nx, m[1] + eps * ny), polys)
                s2 = _in_material((m[0] - eps * nx, m[1] - eps * ny), polys)
                if s1 == s2:
                    continue
                k = frozenset(((round(p0[0], 5), round(p0[1], 5)), (round(p1[0], 5), round(p1[1], 5))))
                if k in seen:
                    continue
                seen.add(k)
                out.append((p0, p1))
    return out


def chain_segments(segs, tol=1e-5):
    """Polylines joining segments end to end (rounded end points), collinear inner vertices merged."""
    key = lambda p: (round(p[0] / tol), round(p[1] / tol))  # noqa: E731
    left = list(segs)
    lines = []
    while left:
        a, b = left.pop(0)
        pl = [a, b]
        grown = True
        while grown:
            grown = False
            for i, (c, d) in enumerate(left):
                if key(c) == key(pl[-1]):
                    pl.append(d)
                elif key(d) == key(pl[-1]):
                    pl.append(c)
                elif key(d) == key(pl[0]):
                    pl.insert(0, c)
                elif key(c) == key(pl[0]):
                    pl.insert(0, d)
                else:
                    continue
                left.pop(i)
                grown = True
                break
        out = [pl[0]]
        for q in pl[1:]:
            if len(out) >= 2:
                o, p = out[-2], out[-1]
                if abs((p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])) < 1e-9 and \
                        (p[0] - o[0]) * (q[0] - p[0]) + (p[1] - o[1]) * (q[1] - p[1]) > 0:
                    out[-1] = q
                    continue
            out.append(q)
        lines.append(out)
    return lines


def _body_pieces(ax, ids):
    """(piece patches, polys) of the rows ids drawn in ax: area patches carrying a piece name, hidden copies excluded."""
    arts = [a for g in ids for a in tagged(ax).get(g, []) if isinstance(a, Patch) and not isinstance(a, FancyArrowPatch)
            and getattr(a, PIECE_ATTR, None) is not None and not getattr(a, "_sc_hidden_copy", False)]
    return arts, [q for a in arts for q in artist_polys(a) if len(q) >= 3]


def draw_cut_outlines(spec, ax):
    """1.4 (h) r2 (M1 S4 F3): for every one_body group of section_true rows drawn in ax, the piece patches lose their
    stroked edge (linewidth 0; fill and hatch unchanged, flag _sc_outlined) and the union boundary of the drawn pieces is
    drawn as solid Line2D polylines tagged <first row>:outline at the pieces' edge colour and width. Idempotent."""
    out = {}
    for ids in one_body_groups(spec):
        arts, polys = _body_pieces(ax, ids)
        if not arts or tagged(ax).get(ids[0] + OUTLINE_SUFFIX):
            continue
        lw = max(float(a.get_linewidth() or 0) for a in arts) or 1.0
        ec = arts[0].get_edgecolor()
        for a in arts:
            a.set_linewidth(0)
            a._sc_outlined = True
        n = 0
        for pl in chain_segments(body_boundary(polys)):
            draw(ids[0] + OUTLINE_SUFFIX, Line2D([p[0] for p in pl], [p[1] for p in pl], color=ec, linewidth=lw,
                                                 solid_capstyle="butt", zorder=2), ax)
            n += 1
        out[ids[0]] = n
    return out


def cut_outline_issues(ctx, ax, pose):
    """K8, 1.4 (h) r2 (M1 S4 F3; Topologist P7b section 2 predicate): for every one_body group of section_true rows drawn
    in a side or section Axes: (o1) no piece patch strokes its edge (a stroked piece edge draws a face inside the body);
    (o2) an outline <first row>:outline is drawn; (o3) every drawn outline sample (OUTLINE_STEP along each segment) has
    material of the body on exactly one side (offset OUTLINE_EPS along the segment normal): no seam, nothing off the
    body; (o4) every sample of the union boundary of the drawn pieces (body_boundary) lies within TOL_Z of the drawn
    outline. Premise: the drawn pieces are the spec pieces (section_true_issues, K8), so the outline is the spec body."""
    out = []
    for ids in one_body_groups(ctx.spec):
        arts, polys = _body_pieces(ax, ids)
        if not arts:
            continue
        g = ids[0] + OUTLINE_SUFFIX
        stroked = sorted({a.get_gid() for a in arts if float(a.get_linewidth() or 0) > 0 and a.get_edgecolor() is not None
                          and a.get_edgecolor()[3] > 0
                          and not (isinstance(a.get_linestyle(), str) and a.get_linestyle().strip().lower() in ("", "none"))})
        if stroked:
            out.append(f"{pose}/{'+'.join(ids)}: piece edges stroked on {', '.join(stroked)} (a line across the cut body; one outlined region per cut body, o1)")
        lines = [artist_polys(a)[0] for a in tagged(ax).get(g, []) if isinstance(a, Line2D) and not getattr(a, "_sc_hidden_copy", False)]
        if not lines:
            out.append(f"{pose}/{'+'.join(ids)}: no outline {g} (o2)")
            continue
        segs = [(pl[i], pl[i + 1]) for pl in lines for i in range(len(pl) - 1)]
        bad = 0
        for a, b in segs:
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < 1e-9:
                continue
            nx, ny = (b[1] - a[1]) / L, -(b[0] - a[0]) / L
            k = max(2, int(L / OUTLINE_STEP))
            for j in range(k):
                t = (j + 0.5) / k
                m = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                if _in_material((m[0] + OUTLINE_EPS * nx, m[1] + OUTLINE_EPS * ny), polys) == \
                        _in_material((m[0] - OUTLINE_EPS * nx, m[1] - OUTLINE_EPS * ny), polys):
                    bad += 1
        if bad:
            out.append(f"{pose}/{'+'.join(ids)}: {bad} outline sample(s) with body material on both sides or neither (a seam or a line off the body, o3)")
        miss = 0
        for a, b in body_boundary(polys):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            k = max(2, int(L / OUTLINE_STEP))
            for j in range(k):
                t = (j + 0.5) / k
                m = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                if min(_pt_seg(m, c, d) for c, d in segs) > TOL_Z:
                    miss += 1
        if miss:
            out.append(f"{pose}/{'+'.join(ids)}: {miss} sample(s) of the body boundary not drawn by the outline (o4)")
    return out


def _solid(a):
    return a.get_linestyle() in SOLID_STYLES


def unsectioned_occluders(ctx, ax):
    """[(row id, artist, ring)] of the solid unsectioned area artists of a section Axes (convention clause 2: a solid of
    revolution with its axis in the plane, drawn whole; its front half lies at x > 0 and hides every area of the section
    inside its outline). Hidden copies and dashed pieces (sweep envelopes) are no occluders."""
    out = []
    for r in ctx.spec.get("features", []):
        if r.get("section_class") != "unsectioned":
            continue
        for a in _area_artists(ax, r["id"]):
            if getattr(a, "_sc_hidden_copy", False) or not _solid(a):
                continue
            for q in artist_polys(a):
                if len(q) >= 3:
                    out.append((r["id"], a, q))
    return out


def _front_x(c, R, u):
    return math.sqrt(max(R * R - (u - c) ** 2, 0.0))


FRONT_SAMPLES = 40   # u samples over the overlap of two unsectioned bodies (TP1.4-4 front test)


def _cr(polys):
    """(centre, half width) along u of a drawn outline (the solid of revolution it stands for, axis in the plane)."""
    xs = [v[0] for P in polys for v in P]
    return (min(xs) + max(xs)) / 2, (max(xs) - min(xs)) / 2


def _in_front(q, polys, n=FRONT_SAMPLES):
    """1.4 (h) r2 (Topologist FIX TP1.4-4, renderer clause (2)): occluder ring q, a whole unsectioned body with its axis in
    the plane, is in front of the unsectioned target polys over their u overlap: x_front(O, u) - x_front(T, u) > TOL_Z at
    every sample, x_front(B, u) = sqrt(R_B^2 - (u - c_B)^2) from the drawn outline centre c_B and half width R_B. Premise:
    every unsectioned row is a solid of revolution with its axis in the plane, drawn whole (K8-B73 straddle, K5
    rectangle projection)."""
    co, Ro = _cr([q])
    ct, Rt = _cr(polys)
    lo, hi = max(co - Ro, ct - Rt), min(co + Ro, ct + Rt)
    if hi <= lo:
        return False
    us = [lo + (hi - lo) * (k + 0.5) / n for k in range(n)]
    return all(_front_x(co, Ro, u) - _front_x(ct, Rt, u) > TOL_Z for u in us)


def _parent_unsectioned(ctx, fid):
    """The drawn outline polys of row fid when it is an unsectioned row (TP1.4-4 front test target), else None."""
    r = next((x for x in ctx.spec.get("features", []) if x["id"] == fid), None)
    return r is not None and r.get("section_class") == "unsectioned"


def _occluded_by(fid, a, occ, ctx=None, ax=None):
    """Occluder rings of other rows whose overlap with artist a exceeds TOL_AREA. 1.4 (h) r2 (TP1.4-4): when the target row
    is itself unsectioned, only an occluder whose front surface is nearer over the overlap (_in_front) hides it."""
    polys = [q for q in artist_polys(a) if len(q) >= 3]
    tgt = None
    if any(g == fid for g, _, _ in occ) or (ctx is not None and _parent_unsectioned(ctx, fid)):
        tgt = [q for q in (pieces(ax, fid) if ax is not None else []) if len(q) >= 3] or polys
    return [(g, q) for g, oa, q in occ if g != fid and oa is not a and any(overlap_area(p, q) > TOL_AREA for p in polys)
            and (tgt is None or _in_front(q, tgt))]


STROKE_STEP = 0.5   # mm: sample step along a Line2D stroke (TP1.4-5, clause (6) line family)


def _stroke_samples(a, step=STROKE_STEP):
    out = []
    for pts in artist_polys(a):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            k = max(1, int(L / step))
            out += [(x0 + (x1 - x0) * i / k, y0 + (y1 - y0) * i / k) for i in range(k + 1)]
    return out


def _stroke_rows(ctx, ax):
    """[(gid, Line2D)] of solid, visible, tagged strokes of part rows (rows, sub-artists and :outline lines; reference
    rows and line, arrow and callout rows with their sub-artists are annotation, as the P7b dry run reads them), hidden
    copies excluded: the line family clause (6) reads (TP1.4-5)."""
    rows = {r["id"]: r for r in ctx.spec.get("features", [])}
    out = []
    for g, arts in tagged(ax).items():
        r = rows.get(g.split(":")[0])
        if r is None or r.get("reference") or r.get("kind") in NO_AREA_KINDS:
            continue
        for a in arts:
            if isinstance(a, Line2D) and a.get_visible() and not getattr(a, "_sc_hidden_copy", False) and _solid(a):
                out.append((g, a))
    return out


def _hidden_stroke(ctx, ax, g, a, occ):
    """(occluder ids, hidden samples, all samples) of stroke a (gid g): samples strictly inside (edge depth > TOL_Z) an
    occluder ring of another row; for an unsectioned parent only at u where that occluder is in front (TP1.4-4 sign)."""
    parent = g.split(":")[0]
    tgt = [q for q in pieces(ax, parent) if len(q) >= 3] if _parent_unsectioned(ctx, parent) else None
    smp = _stroke_samples(a)
    hid, names = [], set()
    rings = [(og, q) for og, oa, q in occ if og != parent]
    if tgt:
        ct, Rt = _cr(tgt)
    for p in smp:
        for og, q in rings:
            if not (_inside(p, q) and _edge_depth(p, [q]) > TOL_Z):
                continue
            if tgt:
                co, Ro = _cr([q])
                if _front_x(co, Ro, p[0]) - _front_x(ct, Rt, p[0]) <= TOL_Z:
                    continue
            hid.append(p)
            names.add(og)
            break
    return sorted(names), hid, smp


def render_occlusion(ctx, ax):
    """1.3 (h) r2 (Topologist TP1.3-11): section convention clause (2) occlusion. Every solid area artist of another row
    that overlaps a solid unsectioned piece by more than TOL_AREA is split as the plan renderer splits (render_plan): the
    artist keeps its style with the region outside the unsectioned pieces as its clip path, and a hidden copy (dashed, no
    fill, no hatch) gets the region inside them, inserted in the draw order right after it. Occluders are taken before any
    split (an unsectioned piece inside another, e.g. a shaft end inside the coupling, is split and still occludes).
    1.4 (h) r2: (TP1.4-4) an unsectioned target is hidden only by an occluder in front of it (_in_front); (TP1.4-5) every
    solid tagged Line2D stroke of a non-reference row (marks, ticks, root lines, :outline lines) with a sample hidden by
    an occluder (_hidden_stroke) is split the same way: the stroke keeps the visible region, a dashed copy the hidden one."""
    occ = unsectioned_occluders(ctx, ax)
    if not occ:
        return {}
    out = {}
    strokes = _stroke_rows(ctx, ax)
    for r in ctx.spec.get("features", []):
        if r.get("kind") in NO_AREA_KINDS or r.get("reference"):
            continue
        fid = r["id"]
        for a in list(_area_artists(ax, fid)):
            if getattr(a, "_sc_hidden_copy", False) or a.get_clip_path() is not None or not _solid(a):
                continue
            hits = _occluded_by(fid, a, occ, ctx, ax)
            if not hits:
                continue
            polys = [q for q in artist_polys(a) if len(q) >= 3]
            x0, x1, y0, y1 = bbox(polys)
            shapes = [[q] for _, q in hits]
            xs = [v[0] for sh in shapes for ring in sh for v in ring] + [x0, x1]
            ys = [v[1] for sh in shapes for ring in sh for v in ring] + [y0, y1]
            box = (min(xs) - RENDER_MARGIN, max(xs) + RENDER_MARGIN, min(ys) - RENDER_MARGIN, max(ys) + RENDER_MARGIN)
            hid, vis = region_split(shapes, box)
            cp = _patch_copy(a)
            cp.set_edgecolor(a.get_edgecolor())
            cp.set_linewidth(a.get_linewidth())
            cp.set_linestyle("--")
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
            out[a] = (fid, sorted({g for g, _ in hits}))
    for g, a in strokes:   # 1.4 (h) r2 (TP1.4-5): the line family
        if a.get_clip_path() is not None:
            continue
        names, hidp, smp = _hidden_stroke(ctx, ax, g, a, occ)
        if not hidp:
            continue
        rings = [q for og, oa, q in occ if og in names]
        tgt = [q for q in pieces(ax, g.split(":")[0]) if len(q) >= 3] if _parent_unsectioned(ctx, g.split(":")[0]) else None
        if tgt:   # the hidden region of an unsectioned parent's stroke: the occluder rings over the u where they are in front
            ct, Rt = _cr(tgt)
            clipped = []
            for q in rings:
                co, Ro = _cr([q])
                us = [v[0] for v in q]
                ua, ub = min(us), max(us)
                lo, hi = None, None
                for k in range(FRONT_SAMPLES * 4 + 1):
                    u = ua + (ub - ua) * k / (FRONT_SAMPLES * 4)
                    if _front_x(co, Ro, u) - _front_x(ct, Rt, u) > TOL_Z:
                        lo = u if lo is None else lo
                        hi = u
                if lo is not None:
                    zs = [v[1] for v in q]
                    clipped.append([(lo, min(zs)), (hi, min(zs)), (hi, max(zs)), (lo, max(zs))])
            rings = clipped
        if not rings:
            continue
        xs = [p[0] for p in smp] + [v[0] for q in rings for v in q]
        ys = [p[1] for p in smp] + [v[1] for q in rings for v in q]
        box = (min(xs) - RENDER_MARGIN, max(xs) + RENDER_MARGIN, min(ys) - RENDER_MARGIN, max(ys) + RENDER_MARGIN)
        hid, vis = region_split([[q] for q in rings], box)
        cp = Line2D(list(a.get_xdata()), list(a.get_ydata()), color=a.get_color(), linewidth=a.get_linewidth(), linestyle="--",
                    zorder=a.get_zorder())
        cp._sc_hidden_copy = True
        a.set_clip_path(region_path(vis), ax.transData)
        draw(g, cp, ax)
        cp.set_clip_path(region_path(hid), ax.transData)
        kids = ax._children
        kids.remove(cp)
        kids.insert(kids.index(a) + 1, cp)
        out[a] = (g, names)
    return out


def occlusion_issues(ctx, ax, pose):
    """1.3 (h) r2, section convention clause (6) (Topologist TP1.3-11). Premise of clause (2): an unsectioned row has its
    axis in the plane and is drawn whole, so its front surface over u lies at x = +sqrt(R^2 - (u - u_c)^2) > 0 and any area
    of the section at x <= 0 inside its outline lies behind it. (6a) No interior sample of a solid area artist of another
    row, inside that artist's drawn region (its clip region, if any), lies inside a solid unsectioned piece deeper than
    TOL_Z. (6b) An artist whose samples lie there has a dashed hidden copy (same row, no hatch, no fill) whose drawn region
    holds them: its hidden edges are drawn. 1.4 (h) r2: (TP1.4-4) an unsectioned target is behind an occluder only where
    the occluder's front surface is nearer (_in_front, x_front(O, u) - x_front(T, u) > TOL_Z); (6c) converse: no hidden
    copy of an unsectioned row holds an interior sample where no occluder is in front of it. (TP1.4-5) (6a) and (6b) read
    every solid tagged Line2D stroke of a non-reference row too (_stroke_rows; samples every STROKE_STEP mm, strictly
    inside by TOL_Z): the visible part of a stroke stays solid, the hidden part has a dashed copy of the same gid."""
    occ = unsectioned_occluders(ctx, ax)
    out = []
    for r in ctx.spec.get("features", []):
        if r.get("kind") in NO_AREA_KINDS or r.get("reference"):
            continue
        fid = r["id"]
        arts = _area_artists(ax, fid)
        copies = [c for c in arts if getattr(c, "_sc_hidden_copy", False) and not _solid(c) and not c.get_hatch()]
        for a in arts:
            if getattr(a, "_sc_hidden_copy", False) or not _solid(a):
                continue
            hits = _occluded_by(fid, a, occ, ctx, ax)
            if not hits:
                continue
            reg = drawn_region(a)
            ins = [p for p in _cover_samples(a) if any(_inside(p, q) and _edge_depth(p, [q]) > TOL_Z for _, q in hits)]
            vis_in = [p for p in ins if reg is None or reg.contains(p)]
            names = ", ".join(sorted({g for g, _ in hits}))
            if vis_in:
                out.append(f"{pose}/{fid}: drawn solid inside the unsectioned outline of {names} ({len(vis_in)} of {len(ins)} "
                           f"samples; section convention 6a, occlusion)")
                continue
            held = lambda c: all((drawn_region(c) is None or drawn_region(c).contains(p)) for p in ins)  # noqa: E731
            if ins and not any(held(c) for c in copies):
                out.append(f"{pose}/{fid}: hidden inside the unsectioned outline of {names} with no dashed hidden copy "
                           f"(section convention 6b)")
        if r.get("section_class") == "unsectioned":   # (6c) converse (TP1.4-4)
            for c in copies:
                reg = drawn_region(c)
                if reg is None:
                    continue
                inner = [p for p in _cover_samples(c) if reg.contains(p) and _edge_depth(p, [q for q in artist_polys(c) if len(q) >= 3]) > TOL_Z]
                front = _occluded_by(fid, c, [(g, oa, q) for g, oa, q in occ], ctx, ax)
                wrong = [p for p in inner if not any(_inside(p, q) for _, q in front)]
                if wrong:
                    out.append(f"{pose}/{fid}: hidden copy drawn dashed where no occluder is in front of it ({len(wrong)} of "
                               f"{len(inner)} samples; section convention 6c, TP1.4-4)")
    for g, a in _stroke_rows(ctx, ax):   # (TP1.4-5) the line family
        names, hidp, smp = _hidden_stroke(ctx, ax, g, a, occ)
        if not hidp:
            continue
        reg = drawn_region(a)
        vis_in = [p for p in hidp if reg is None or reg.contains(p)]
        if vis_in:
            out.append(f"{pose}/{g}: stroke drawn solid inside the unsectioned outline of {', '.join(names)} ({len(vis_in)} of "
                       f"{len(smp)} samples; section convention 6a, line family, TP1.4-5)")
            continue
        cps = [c for c in tagged(ax).get(g, []) if isinstance(c, Line2D) and getattr(c, "_sc_hidden_copy", False) and not _solid(c)]
        if not any(all(drawn_region(c) is None or drawn_region(c).contains(p) for p in hidp) for c in cps):
            out.append(f"{pose}/{g}: stroke hidden inside the unsectioned outline of {', '.join(names)} with no dashed hidden copy "
                       f"(section convention 6b, line family, TP1.4-5)")
    return out


def face_spans(polys, z, tol=TOL_Z):
    """Merged x intervals of the horizontal polygon edges lying at height z (within tol)."""
    sp = []
    for q in polys:
        n = len(q)
        for i in range(n):
            a, b = q[i], q[(i + 1) % n]
            if abs(a[1] - z) <= tol and abs(b[1] - z) <= tol and abs(a[0] - b[0]) > 1e-9:
                sp.append([min(a[0], b[0]), max(a[0], b[0])])
    sp.sort()
    out = []
    for s in sp:
        if out and s[0] <= out[-1][1] + 1e-9:
            out[-1][1] = max(out[-1][1], s[1])
        else:
            out.append(s)
    return out


def bearing_width(me, seat):
    """1.4 P2f (Designer P3a FIX 3): radial bearing of a member on its seat as drawn. The member's bottom-face spans
    (horizontal edges at its z_min) overlapped with the seat's top-face spans (at its z_max), per side of the member's
    centroid x (a round row drawn mirrored about its axis). Returns (least side width, [width per side with a member
    face]); 0 when a side has a member face and no seat face under it."""
    zb, zt = extent_z(me)[0], extent_z(seat)[1]
    mb, st = face_spans(me, zb), face_spans(seat, zt)
    x0 = centroid(me)[0]
    per = []
    for lo, hi in ((-math.inf, x0), (x0, math.inf)):
        ms = [(max(a, lo), min(b, hi)) for a, b in mb if min(b, hi) - max(a, lo) > 1e-9]
        if not ms:
            continue
        per.append(sum(max(0.0, min(b1, b2) - max(a1, a2)) for a1, b1 in ms for a2, b2 in st))
    return (min(per) if per else 0.0), per


def hatch_adjacency_issues(ctx, ax, pose):
    """1.4 P2f (Designer P3a FIX 2, rule (h) premise lint): two cut rows that are separate bodies (no one_body declaration
    either way) drawn with hatch patterns of one line family (hatch_family; 1.4 P4, orchestrator ruling on Designer P2r
    R2, the 1.3 R2-4 rule: density does not separate two parts) within section.hatch_adjacency_gap mm of each other read as one solid.
    Runs on a section Axes whose spec declares section.hatch_adjacency_gap (S4 from 1.4 (b); S3 r8 at P6, carried by
    name). Returns issues."""
    gap = ((ctx.spec or {}).get("section") or {}).get("hatch_adjacency_gap")
    if gap is None:
        return []
    feats = ctx.spec.get("features", [])
    out = []
    # 1.4 P6 (Designer P2r 1.4 item 1, material truth first): in a spec that declares the gap, every cut row names its
    # material; the default steel of cut_hatch is refused there (premise: a pattern the drawing carries is a material
    # the spec states, so two parts read alike only when the spec says they are one material).
    out += [f"{pose}: {r['id']}: cut row with no hatch in a spec that declares section.hatch_adjacency_gap" for r in feats
            if r.get("section_class") == "cut" and not r.get("hatch")]
    # 1.4 P6 (Designer P2r 1.4 item 5): a spec whose rows carry no section_class (S1 side views) takes every row drawn
    # with a hatched area; the drawn hatch is read from the artist and family-compared (no material convention assumed).
    has_cls = any(r.get("section_class") for r in feats)
    rows = [r for r in feats if r.get("section_class") == "cut"] if has_cls else [r for r in feats if r.get("kind") not in NO_AREA_KINDS]
    ob = {frozenset((r["id"], n["id"])) for r in feats for n in (r.get("neighbours") or []) if n.get("kind") == "one_body"}
    drawn = {}
    for r in rows:
        arts = [a for a in _area_artists(ax, r["id"]) if not getattr(a, "_sc_hidden_copy", False) and a.get_hatch()]
        if arts:
            drawn[r["id"]] = [(a.get_hatch(), P) for a in arts for P in artist_polys(a) if len(P) >= 3]
    ids = list(drawn)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if frozenset((a, b)) in ob:
                continue
            best = None
            for ha, pa in drawn[a]:
                for hb, pb in drawn[b]:
                    if hatch_family(ha) == hatch_family(hb):   # 1.4 P4 (orchestrator ruling on Designer P2r R2): line family
                        d = min_distance(pa, pb)
                        if best is None or d < best[0]:
                            best = (d, ha, hb)
            if best is not None and best[0] <= float(gap) + 1e-9:
                fam = "" if best[1] == best[2] else f" (line family of {best[2]!r})"
                out.append(f"{pose}: {a}|{b}: separate cut bodies with the same hatch {best[1]!r}{fam} {best[0]:.2f} mm apart "
                           f"(<= section.hatch_adjacency_gap {float(gap):g}); set hatch_variant on one (Designer P3a FIX 2)")
    return out


def hatch_alt_table(spec):
    """section.hatch_alt {material: pattern} (1.3 (h) r2, Topologist TP1.3-14): the alternate pattern a hatch_split row
    carries on its pieces above the split. Values are The Designer's."""
    return dict(((spec or {}).get("section") or {}).get("hatch_alt") or {})


def hatch_split_z(ctx, pose, row):
    """z_S of a row's hatch_split.at, or None."""
    hs = row.get("hatch_split") or {}
    if not hs.get("at"):
        return None
    import check_stack as _cs
    names = ((ctx.stack or {}).get("poses", {}).get(pose, {}) or {}).get("vars_z_A", {})
    return _cs.to_shop_floor(_cs.eval_expr(str(hs["at"]), ctx.P, names), ctx.P)


def cut_hatch(ctx, pose, row, a):
    """Hatch a cut artist carries: HATCH[material]; on a hatch_split row, a piece wholly above the split carries
    section.hatch_alt[material] (when declared)."""
    mat = row.get("hatch") or "steel"
    alt = hatch_alt_table(ctx.spec).get(mat)
    if row.get("hatch_variant") == "alt" and alt:   # 1.4 P2f (Designer P3a FIX 2): the whole row carries the alternate
        return alt
    zs = hatch_split_z(ctx, pose, row)
    if zs is not None and alt:
        polys = [q for q in artist_polys(a) if len(q) >= 3]
        if polys and min(v[1] for q in polys for v in q) >= zs - TOL_Z:
            return alt
    return HATCH.get(mat)


def hatch_family(h):
    """1.3 (h) r3 (Topologist R2-4): the line family of a hatch pattern, the set of its stroke characters, with '+' read
    as '|' and '-' and 'x' / 'X' as '/' and '\'. A repeated character changes the density only, not the family."""
    out = set()
    for ch in str(h or ""):
        out |= {"+": {"|", "-"}, "x": {"/", "\\"}, "X": {"/", "\\"}}.get(ch, {ch})
    return frozenset(out)


def hatch_alt_issues(spec):
    """Lint (TP1.3-14; 1.3 (h) r3 Topologist R2-4): every section.hatch_alt value differs in line family (hatch_family)
    from every HATCH value and from every other alternate, so the cover reads as a separate piece and not as another
    material; a row with hatch_split names a material that has an alternate."""
    alt = hatch_alt_table(spec)
    fams = {k: hatch_family(v) for k, v in HATCH.items()}
    out = []
    for m, v in alt.items():
        hit = sorted(k for k, f in fams.items() if f == hatch_family(v))
        if hit:
            out.append(f"spec error: section.hatch_alt {m} {v!r} in the line family of material pattern(s) {', '.join(hit)} (HATCH)")
        if [hatch_family(w) for w in alt.values()].count(hatch_family(v)) > 1:
            out.append(f"spec error: section.hatch_alt {m} {v!r} in the line family of another alternate")
    for r in (spec or {}).get("features", []):
        if r.get("hatch_split") and r.get("section_class") == "cut" and not alt.get(r.get("hatch") or "steel"):
            out.append(f"{r['id']}: hatch_split declared with no section.hatch_alt for {r.get('hatch') or 'steel'} (The Designer, TP1.3-14)")
        hv = r.get("hatch_variant")   # 1.4 P2f (Designer P3a FIX 2)
        if hv is not None and hv != "alt":
            out.append(f"spec error: {r['id']}: hatch_variant {hv!r} (known: alt)")
        elif hv and r.get("section_class") == "cut" and not alt.get(r.get("hatch") or "steel"):
            out.append(f"{r['id']}: hatch_variant declared with no section.hatch_alt for {r.get('hatch') or 'steel'} (The Designer, P3a FIX 2)")
    return out


SECTION_LOOK = {"section_yz": ("-X", (0.0, 1.0, 0.0))}   # P5f (TP FIX 2): u_view = +Y; u x z = +X; look = -(u x z)


def section_look_issues(spec, view):
    """P5f (Topologist FIX 2): the cutting-plane look direction is not free. For a section view the viewer sits on
    u_view x z, so (u_view x z) . toward = -1: section_yz (u = +Y) looks toward -X. A look_direction predicate naming
    another direction is a spec error in the main Axes, once per predicate."""
    want = SECTION_LOOK.get(view, (None,))[0]
    out = []
    for r in spec.get("features", []):
        for pr in r.get("sense") or []:
            if pr.get("pred") == "look_direction" and want and pr.get("toward") != want:
                out.append(f"{r['id']} look_direction: spec error, toward {pr.get('toward')} against the {view} viewer (u x z . toward = -1 needs {want})")
    return out


def omitted_row_issues(ctx, parent):
    """P5f (Topologist FIX 3 b): converse of the section convention. Every area row of the spec (not reference, not line,
    arrow or callout) that is not declared in the section Axes is omitted for a reason: its plan x band (place or
    plan_poly) lies wholly in front (x0 > 0.05) or wholly past one profile width (x1 < -profile.width - 0.05). A row in the
    section band that is not drawn in the section is an issue."""
    main_id = main_axes_id(parent.spec.get("view"))
    pw = ctx.P.get("profile.width") if ctx.P is not None and ctx.P.has("profile.width") else 60.0
    out = []
    for pose in ctx.figs:
        feats = parent.stack["poses"][pose]["features"]
        for r in parent.spec.get("features", []):
            if main_id in row_axes(r, main_id) or r.get("reference") or r.get("kind") in NO_AREA_KINDS:
                continue
            f = feats.get(r["id"]) or {}
            xb = (f.get("place") or {}).get("x") or f.get("plan_x")
            if not xb:
                continue
            if not (xb[0] > TOL_Z or xb[1] < -pw - TOL_Z):
                out.append(f"{pose}/{r['id']}: plan x [{xb[0]:.2f}, {xb[1]:.2f}] lies in the section band and is not drawn in the section (section convention 4, converse)")
    return out


ND_OMIT = ("off_plane", "deferred", "hidden")
_OTHER_STACKS = {}
ND_SAMPLE = 2.5   # omit: hidden sample step along r and z (mm), ends included


def _nd_steps(lo, hi, h=ND_SAMPLE):
    n = max(1, math.ceil((hi - lo) / h - 1e-9))
    return [lo + (hi - lo) * i / n for i in range(n + 1)]


def hidden_occluders(ctx, parent, pose, ax):
    """omit: hidden (h3) occluders at a pose, read from the rows drawn in the figure: [("cut", row, piece, (r, z_A) poly)]
    the section_true revolve half-profile pieces of each drawn row (plane_cuts ignored: the occluder is the profile;
    premise the K8 plane_cuts lint and section_true premise, drawn = spec), and [("whole", row, half-width, (z0, z1)
    z_A)] each drawn unsectioned row, drawn whole over its depth band. Feature voids in an occluder are neglected (the
    drafting convention, section.convention.omitted)."""
    import check_stack as _cs
    st = parent.stack["poses"][pose]
    names = st["vars_z_A"]
    drawn = tagged(ax)
    out = []
    for r in parent.spec.get("features", []):
        if not applies(r, pose) or r["id"] not in drawn or r.get("kind") in NO_AREA_KINDS or r.get("reference"):
            continue
        if r.get("section_true"):
            prof = {k: v for k, v in r.items() if k != "plane_cuts"}
            for nm, side, sp in section_true_polys(ctx.P, names, prof, z_S=False):
                if side > 0:
                    out.append(("cut", r["id"], nm, sp))
        elif r.get("section_class") == "unsectioned":
            f = st["features"].get(r["id"]) or {}
            band = (f.get("place") or {}).get("y") or f.get("depth")
            if f.get("z_min") is None or not band:
                continue
            z0, z1 = sorted((_cs.from_shop_floor(f["z_min"], ctx.P), _cs.from_shop_floor(f["z_max"], ctx.P)))
            out.append(("whole", r["id"], max(abs(v) for v in band), (z0, z1)))
    return out


def hidden_entry_issues(ctx, parent, e, head):
    """P5f (Topologist F5; Designer section 3: one hidden-detail convention): not_drawn omit: hidden. Premise of omitting a
    feature of a drawn row: it lies behind the plane and is occluded along its sight line (ASME Y14.3 omits hidden lines
    in a section; declared sub-artists are the stated exceptions). Entry {rows (parent row ids), theta [deg expressions],
    r [lo, hi], z [lo, hi] (z_A expressions over keys, R2-6), t (tangential half-width), source}. Samples: r and z at <=
    ND_SAMPLE with both ends, t at -t, 0, +t (theta shifted by atan(t / r), r_f = hypot(r, t)), at every figure pose
    where a listed row is drawn; x = r_f cos theta, u = r_f sin theta. (h1) |x| <= TOL_Z: the plane cuts the feature (draw
    it, or list it as a plane_cuts entry). (h2) x > TOL_Z: cut away with the front half, only when every listed row
    drawn at the pose is section_class cut (an unsectioned parent is drawn whole). (h3) x < -TOL_Z: an occluder drawn at
    the pose covers the sample: a section_true revolve piece whose chord [a, b] at z has a < r_f - TOL_Z and b > |u| +
    TOL_Z, or an unsectioned row drawn whole whose half-width exceeds |u| + TOL_Z over z (hidden_occluders)."""
    import check_stack as _cs
    out = []
    rows = {r["id"]: r for r in parent.spec.get("features", [])}
    need = ("rows", "theta", "r", "z")
    if any(not e.get(k) for k in need) or "t" not in e:
        return [f"spec error: not_drawn {head!r} hidden without {', '.join(k for k in need + ('t',) if k not in e or (k != 't' and not e.get(k)))}"]
    unknown = [i for i in e["rows"] if i not in rows]
    if unknown:
        return [f"spec error: not_drawn {head!r} hidden names unknown row(s) {', '.join(unknown)}"]
    for k in ("r", "z"):   # R2-6: bounds read keys or stack names (a stack name is evaluated from keys)
        lit = [v for v in e[k] if not ND_KEY_REF.search(str(v)) and not re.search(r"[A-Za-z_]", str(v))]
        if lit:
            out.append(f"spec error: not_drawn {head!r} {k} bound {lit[0]!r} reads no key: write it as an expression over keys (R2-6)")
    if out:
        return out
    for pose, fig in ctx.figs.items():
        if pose not in parent.stack["poses"]:
            continue
        ax = fig.axes[0]
        drawn = tagged(ax)
        par = [rows[i] for i in e["rows"] if applies(rows[i], pose) and i in drawn]
        if not par:
            continue
        names = parent.stack["poses"][pose]["vars_z_A"]
        ev = lambda x: float(_cs.eval_expr(str(x), ctx.P, names))  # noqa: E731
        r0, r1 = sorted(ev(v) for v in e["r"])
        z0, z1 = sorted(ev(v) for v in e["z"])
        t = abs(ev(e["t"]))
        occ = hidden_occluders(ctx, parent, pose, ax)
        all_cut = all(p.get("section_class") == "cut" for p in par)
        n = inpl = front = bad = 0
        ex = None
        for th0 in (ev(v) for v in e["theta"]):
            for rr in _nd_steps(r0, r1):
                for tt in sorted({-t, 0.0, t}):
                    th = th0 + math.degrees(math.atan2(tt, rr))
                    rf = math.hypot(rr, tt)
                    x, u = rf * math.cos(math.radians(th)), rf * math.sin(math.radians(th))
                    for zz in _nd_steps(z0, z1):
                        n += 1
                        if abs(x) <= TOL_Z:
                            inpl += 1
                        elif x > TOL_Z:
                            front += 0 if all_cut else 1
                        else:
                            hit = False
                            for kind, rid, nm, g in occ:
                                if kind == "whole":
                                    hit = g[0] - TOL_Z <= zz <= g[1] + TOL_Z and nm > abs(u) + TOL_Z
                                else:
                                    c = poly_chord(g, zz)
                                    hit = c is not None and c[0] < rf - TOL_Z and c[1] > abs(u) + TOL_Z
                                if hit:
                                    break
                            if not hit:
                                bad += 1
                                ex = ex or (th, rf, zz)
        if inpl:
            out.append(f"{pose}: not_drawn {head!r} hidden: {inpl} of {n} samples in the plane (|x| <= {TOL_Z:g}): draw it or list it as a plane_cuts entry (h1)")
        if front:
            out.append(f"{pose}: not_drawn {head!r} hidden: {front} of {n} samples in front of the plane on an unsectioned parent "
                       f"({', '.join(p['id'] for p in par if p.get('section_class') != 'cut')}), drawn whole: draw it (h2)")
        if bad:
            out.append(f"{pose}: not_drawn {head!r} hidden: {bad} of {n} samples behind the plane not occluded by a drawn row, e.g. theta "
                       f"{ex[0]:.1f}, r {ex[1]:.2f}, z_A {ex[2]:.2f}: draw it as hidden or state its convention (h3)")
    return out


def _other_sketch_bands(P, sketch, ids, pose):
    """{row id: (x0, x1)} plan x extent of rows of another sketch's spec at pose (its true plan outline: plan_outline)."""
    import check_stack as _cs
    from sketch_loader import load_spec as _ls
    key = (id(P), sketch)
    if key not in _OTHER_STACKS:
        sp = _ls(HERE / f"{sketch}_spec.yaml")
        _OTHER_STACKS[key] = (sp, _cs.evaluate_spec(P, sp))
    sp, st = _OTHER_STACKS[key]
    rows = {r["id"]: r for r in sp.get("features", [])}
    c = Ctx(P=P, spec=sp, figs={}, stack=st, view=sp.get("view"))
    out = {}
    pz = pose if pose in st["poses"] else next(iter(st["poses"]))
    for i in ids:
        if i not in rows:
            out[i] = None
            continue
        po = plan_outline(c, rows[i], pz)
        if po is None:
            f = st["poses"][pz]["features"].get(i) or {}
            xb = (f.get("place") or {}).get("x") or f.get("plan_x")
            out[i] = tuple(xb) if xb else None
        elif po[0] == "annulus":
            out[i] = (-po[1][1], po[1][1])
        else:
            xs = [v[0] for q in po[1] for v in q]
            out[i] = (min(xs), max(xs))
    return out


ND_KEY_REF = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_]")   # a dotted params or overlay key inside an expression


def not_drawn_band_issues(ctx, parent):
    """1.3 (h) r2 (Topologist TP1.3-12): the not_drawn converse of the section convention. Premise of omitting a part
    from a section: it lies wholly in front of the plane or wholly past one profile width behind it (clause 4), or its
    omission is deferred to a named owner. Every not_drawn entry carries omit: off_plane (with rows: S3 row ids,
    rows_s2: S2 row ids read on their true plan outline, or x: plan x bands [lo, hi], expressions allowed) or omit:
    deferred (with owner). An off_plane band that meets the section band (x0 <= 0.05 and x1 >= -profile.width - 0.05)
    is an issue: draw the part (beyond row) or state its convention. Deferred entries are listed, not judged. P5f
    (Topologist F5): omit: hidden, a hidden feature of a drawn row, judged at every figure pose (hidden_entry_issues)."""
    import check_stack as _cs
    spec = parent.spec or {}
    pw = ctx.P.get("profile.width") if ctx.P is not None and ctx.P.has("profile.width") else 60.0
    out = []
    pose = next(iter(ctx.figs), None) or (spec.get("section_figure") or {}).get("pose", "capture_end")
    feats = parent.stack["poses"][pose]["features"] if parent.stack and pose in parent.stack["poses"] else {}
    for e in spec.get("not_drawn") or []:
        e = e if isinstance(e, dict) else {"part": e}
        head = part_head(e.get("part"))
        om = e.get("omit")
        if om not in ND_OMIT:
            out.append(f"spec error: not_drawn {head!r} without omit (one of {', '.join(ND_OMIT)})")
            continue
        if om == "deferred":
            if not e.get("owner"):
                out.append(f"spec error: not_drawn {head!r} deferred with no owner")
            continue
        if om == "hidden":   # P5f (Topologist F5, Designer section 3)
            out += hidden_entry_issues(ctx, parent, e, head)
            continue
        bands = []
        for i in e.get("rows") or []:
            f = feats.get(i) or {}
            xb = (f.get("place") or {}).get("x") or f.get("plan_x")
            if not xb:
                out.append(f"spec error: not_drawn {head!r} names S3 row {i} with no plan x band")
                continue
            bands.append((i, tuple(xb)))
        if e.get("rows_s2"):
            for i, xb in _other_sketch_bands(ctx.P, "s2", e["rows_s2"], pose).items():
                if xb is None:
                    out.append(f"spec error: not_drawn {head!r} names S2 row {i} with no plan outline")
                else:
                    bands.append((f"s2 {i}", xb))
        for k, b in enumerate(e.get("x") or []):
            lit = [v for v in b if not ND_KEY_REF.search(str(v))]   # 1.4 step 0 R5 a (Topologist NOTE R2-6)
            if lit:
                out.append(f"spec error: not_drawn {head!r} x band {k + 1} bound {lit[0]!r} reads no key: write it as an expression "
                           f"over keys (a key edit reaches it through keys_read and --stale; R2-6)")
            lo, hi = sorted(float(_cs.eval_expr(str(v), ctx.P, {})) for v in b)
            bands.append((f"x band {k + 1}", (lo, hi)))
        if not bands:
            out.append(f"spec error: not_drawn {head!r} off_plane with no rows, rows_s2 or x band")
            continue
        for nm, (lo, hi) in bands:
            if not (lo > TOL_Z or hi < -pw - TOL_Z):
                out.append(f"{pose}: not_drawn {head!r} ({nm}) plan x [{lo:.2f}, {hi:.2f}] lies in the section band "
                           f"(0 to -{pw:g}): draw it as a beyond row or state its convention (TP1.3-12)")
    return out


def mirror_radial_issue(me, pl, plan):
    """P5f (Topologist FIX 6): plan only. In the radial frame at the placed theta (to_ut), every vertex (u, t) of every
    drawn piece has a partner (u, -t) in the same piece within TOL_Z: the part is symmetric about its own radial line."""
    if not plan or not pl:
        return "needs plan_xy and a place"
    for P in me:
        ut = to_ut(P, pl["theta"])
        for u, t in ut:
            if not any(abs(u - u2) <= TOL_Z and abs(t + t2) <= TOL_Z for u2, t2 in ut):
                return f"vertex (u {u:.2f}, t {t:.2f}) has no mirror (u, -t) about the radial at theta {pl['theta']:g}"
    return None


def section_u_pieces(ctx, pose, row):
    """Spec section_u pieces of a row at a pose as (u0, u1, z0, z1), u along +Y, z in z_S."""
    import check_stack as _cs
    names = ctx.stack["poses"][pose]["vars_z_A"]
    out = []
    for pc in row.get("section_u") or []:
        u0, u1 = sorted((_cs.eval_expr(pc[0], ctx.P, names), _cs.eval_expr(pc[1], ctx.P, names)))
        z0, z1 = sorted((_cs.to_shop_floor(_cs.eval_expr(pc[2], ctx.P, names), ctx.P), _cs.to_shop_floor(_cs.eval_expr(pc[3], ctx.P, names), ctx.P)))
        out.append((u0, u1, z0, z1))
    return out


def section_u_issues(ctx, pose, row, me):
    """1.3 P4 (s3_spec section_u): premise of reading a section row's drawn pieces as its true section: each spec piece
    [u0, u1, z0, z1] is drawn (a drawn piece with that bounding box within TOL_Z) and every drawn piece is a spec piece."""
    spec_p = section_u_pieces(ctx, pose, row)
    drawn = [bbox([P]) for P in me if len(P) >= 3]
    near = lambda a, b: all(abs(x - y) <= TOL_Z for x, y in zip(a, b))  # noqa: E731
    out = []
    for sp in spec_p:
        if not any(near(sp, d) for d in drawn):
            out.append(f"spec piece u [{sp[0]:.2f}, {sp[1]:.2f}] z [{sp[2]:.2f}, {sp[3]:.2f}] not drawn")
    for d in drawn:
        if not any(near(sp, d) for sp in spec_p):
            out.append(f"drawn piece u [{d[0]:.2f}, {d[1]:.2f}] z [{d[2]:.2f}, {d[3]:.2f}] is no spec piece")
    return out


def section_convention_issues(ctx, ax, pose):
    """1.3 P4: the renderer section convention as a check, per section Axes and pose.
    (1) cut: every area artist hatched with its material pattern; the plane cuts the row (depth band reaches x = 0).
    (2) unsectioned: no hatch; drawn above every cut artist (zorder).
    (3) beyond: no hatch; wholly behind drawn cut pieces -> dashed, wholly visible -> solid, partly -> split required;
        depth band within 0 >= x >= -profile.width.
    (4) omitted: no drawn row lies in front of the plane (depth band x > 0) or wholly past one profile width (x <
        -profile.width): such rows are not drawn and are named in the figure note.
    (5) every area row of the section Axes carries a section_class (spec error otherwise).
    Depth is the reflected stack depth (plan x band). Returns (tests, issues)."""
    rows = ctx.spec.get("features", [])
    pw = ctx.P.get("profile.width") if ctx.P is not None and ctx.P.has("profile.width") else 60.0
    cut = _cut_polys(ctx, ax)
    cut_z = max([a.get_zorder() for r in rows if r.get("section_class") == "cut" for a in _area_artists(ax, r["id"])] or [0])
    n, out = 0, []
    for r in rows:
        fid, cls = r["id"], r.get("section_class")
        arts = _area_artists(ax, fid)
        drawn = bool(tagged(ax).get(fid))
        if r.get("kind") in NO_AREA_KINDS or r.get("reference"):
            continue
        if cls not in SECTION_CLASSES:
            out.append(f"{pose}/{fid}: spec error, section_class {cls!r} (known: {', '.join(SECTION_CLASSES)})")
            continue
        dep = _feat(ctx, pose, fid).get("depth")
        if drawn and dep:
            n += 1
            if dep[0] > TOL_Z:
                out.append(f"{pose}/{fid}: drawn in front of the plane (depth x [{dep[0]:.2f}, {dep[1]:.2f}]); omit it and name it in the figure note (section convention 4)")
                continue
            if dep[1] < -pw - TOL_Z:
                out.append(f"{pose}/{fid}: drawn past one profile width behind the plane (depth x [{dep[0]:.2f}, {dep[1]:.2f}], limit -{pw:g}); omit it (section convention 4)")
                continue
        for a in arts:
            if getattr(a, "_sc_hidden_copy", False):   # 1.3 (h) r2: judged by clause (6b)
                continue
            n += 1
            h = a.get_hatch()
            if cls == "cut":
                want = cut_hatch(ctx, pose, r, a)   # 1.3 (h) r2: hatch_split pieces above the split carry the alternate
                if not h:
                    out.append(f"{pose}/{fid}: cut row drawn without hatch (section convention 1)")
                elif h != want:
                    out.append(f"{pose}/{fid}: hatch {h!r} against material {r.get('hatch')} {want!r} (section convention 1)")
            elif cls == "unsectioned":
                if h:
                    out.append(f"{pose}/{fid}: unsectioned row hatched {h!r} (section convention 2: outline over the hatch)")
                elif a.get_zorder() <= cut_z:
                    out.append(f"{pose}/{fid}: unsectioned outline at zorder {a.get_zorder():g}, not above the cut hatch ({cut_z:g}) (section convention 2)")
            elif cls == "beyond":
                if h:
                    out.append(f"{pose}/{fid}: beyond row hatched {h!r} (section convention 3)")
                ins, outs = _behind(a, cut)
                dashed = a.get_linestyle() not in SOLID_STYLES
                if ins and outs:
                    out.append(f"{pose}/{fid}: beyond piece partly behind a cut part ({ins} of {ins + outs} samples): draw visible and hidden parts as separate pieces (section convention 3)")
                elif ins and not dashed:
                    out.append(f"{pose}/{fid}: beyond piece behind a cut part drawn solid; edges behind a cut part are dashed (section convention 3)")
                elif outs and dashed:
                    out.append(f"{pose}/{fid}: visible beyond piece drawn dashed (section convention 3)")
        if cls == "beyond" and dep and drawn and (dep[1] > TOL_Z):
            out.append(f"{pose}/{fid}: beyond row reaches in front of the plane (depth x up to {dep[1]:.2f}) (section convention 3)")
        if cls == "unsectioned" and dep and drawn and not (dep[0] <= TOL_Z and dep[1] >= -TOL_Z):   # P5f (TP FIX 3 a)
            out.append(f"{pose}/{fid}: unsectioned row whose axis is not in the plane (depth x [{dep[0]:.2f}, {dep[1]:.2f}]) (section convention 2)")
        if cls == "cut" and dep and drawn and not (dep[0] <= TOL_Z and dep[1] >= -TOL_Z):
            out.append(f"{pose}/{fid}: cut row the plane x = 0 does not cut (depth x [{dep[0]:.2f}, {dep[1]:.2f}]) (section convention 1)")
    out += occlusion_issues(ctx, ax, pose)   # 1.3 (h) r2: clause (6), Topologist TP1.3-11
    out += [f"{pose}: {m}" for m in hatch_alt_issues(ctx.spec)]   # 1.3 (h) r2: TP1.3-14
    adj = hatch_adjacency_issues(ctx, ax, pose)   # 1.4 P2f: Designer P3a FIX 2 premise lint
    n += 1 if ((ctx.spec or {}).get("section") or {}).get("hatch_adjacency_gap") is not None else 0
    out += adj
    return n, out


# ======================================================================== 1.4 P4: section_true (true sections), S4 sub-artists

PIECE_ATTR = "_sc_piece"   # artist attribute: the section_true piece name a drawn area stands for (draw_piece)


def _dedup(poly, tol=1e-9):
    out = []
    for v in poly:
        if not out or math.hypot(v[0] - out[-1][0], v[1] - out[-1][1]) > tol:
            out.append((float(v[0]), float(v[1])))
    if len(out) > 1 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) <= tol:
        out.pop()
    return out


def poly_match(a, b, tol=TOL_Z):
    """Two drawn polygons are the same piece: equal vertex count (consecutive and closing duplicates dropped) and every
    vertex of each within tol of a vertex of the other."""
    a, b = _dedup(a), _dedup(b)
    if len(a) != len(b):
        return False
    near = lambda p, Q: any(math.hypot(p[0] - q[0], p[1] - q[1]) <= tol for q in Q)  # noqa: E731
    return all(near(p, b) for p in a) and all(near(q, a) for q in b)


def section_true_polys(P, names, row, z_S=True):
    """1.4 P4 (s4_spec section_true): [(piece name, side, polygon)] of a row's true section in the view plane, mirrored
    about u = 0 (side +1 at u > 0, -1 at u < 0), z in z_S (z_A when z_S is False). A rectangle piece is [r_in, r_out,
    z_lo, z_hi]; {poly: [[r, z], ...]} is a convex polygon. plane_cuts [{piece, side}] leave that piece out on that side
    (outside X1, Loftsman P3b O2 (iii)). Mirroring is keyed on the field, never on `axis` (Loftsman P3b O2)."""
    import check_stack as _cs
    ev = lambda e: float(_cs.eval_expr(str(e), P, names))  # noqa: E731
    zc = (lambda z: _cs.to_shop_floor(z, P)) if z_S else (lambda z: z)
    cuts = {(c.get("piece"), c.get("side")) for c in row.get("plane_cuts") or []}
    out = []
    for name, spec in (row.get("section_true") or {}).items():
        if isinstance(spec, dict):
            rz = [(ev(r), zc(ev(z))) for r, z in spec["poly"]]
        else:
            r0, r1, z0, z1 = (ev(v) for v in spec)
            rz = [(r0, zc(z0)), (r1, zc(z0)), (r1, zc(z1)), (r0, zc(z1))]
        for side, tag in ((1, "+u"), (-1, "-u")):
            if (name, tag) in cuts:
                continue
            pts = [(side * r, z) for r, z in rz]
            out.append((name, side, pts if side > 0 else pts[::-1]))
    return out


def st_polys(ctx, pose, row):
    names = ((ctx.stack or {}).get("poses", {}).get(pose, {}) or {}).get("vars_z_A", {})
    return section_true_polys(ctx.P, names, row)


def draw_piece(ax, fid, name, pts, **kw):
    """Draw one section_true piece as a closed unfilled Polygon tagged gid = fid and PIECE_ATTR = name."""
    kw.setdefault("fill", False)
    a = draw(fid, Polygon(pts, closed=True, **kw), ax)
    setattr(a, PIECE_ATTR, name)
    return a


def _piece_artists(ax, fid):
    return [a for a in tagged(ax).get(fid, []) if isinstance(a, Patch) and not getattr(a, "_sc_hidden_copy", False)
            and not isinstance(a, FancyArrowPatch)]


def named_pieces(ax, fid, names):
    """Drawn polygons of row fid whose artists carry a piece name in names (str or list)."""
    names = [names] if isinstance(names, str) else list(names)
    return [P for a in _piece_artists(ax, fid) if getattr(a, PIECE_ATTR, None) in names for P in artist_polys(a) if len(P) >= 3]


def section_true_issues(ctx, ax, pose, row):
    """1.4 P4 (O7), premise of reading a row's drawn pieces as its true section (K5 admission, K8 piece / of_piece,
    K7): every spec piece (name, side; plane_cuts applied) is drawn as an artist carrying that piece name whose polygon
    equals the spec polygon within TOL_Z (poly_match), and every drawn area artist of the row carries a piece name and
    equals that spec piece on one side. Scope: every row with section_true in a side or section view.
    P5f (Topologist F2 c): every plane_cuts entry carries theta, and the cut lies on its side of the plane: theta 90 for
    side +u, 270 for side -u (mod 360, within 1e-6; sign(sin theta) = side), the premise of reading the revolve profile
    with plane_cuts ignored (wing (iii), not_drawn omit: hidden (h3))."""
    spec = st_polys(ctx, pose, row)
    arts = _piece_artists(ax, row["id"])
    out = []
    for c in row.get("plane_cuts") or []:
        if c.get("theta") is None:
            out.append(f"plane_cuts {c.get('piece')} {c.get('side')}: spec error, no theta (the azimuth of the cut on the plane)")
            continue
        th = _ev(ctx, pose, c["theta"]) % 360.0
        want = {"+u": 90.0, "-u": 270.0}.get(c.get("side"))
        if want is None or abs(th - want) > 1e-6:
            out.append(f"plane_cuts {c.get('piece')} {c.get('side')}: theta {th:g} does not lie on side {c.get('side')} of the plane "
                       f"(90 for +u, 270 for -u)")
    for name, side, sp in spec:
        if not any(getattr(a, PIECE_ATTR, None) == name and any(poly_match(P, sp) for P in artist_polys(a)) for a in arts):
            out.append(f"piece {name} ({'+u' if side > 0 else '-u'}) not drawn as specified")
    for a in arts:
        nm = getattr(a, PIECE_ATTR, None)
        if nm is None:
            out.append(f"drawn {type(a).__name__} carries no section_true piece name")
            continue
        cand = [sp for n_, _, sp in spec if n_ == nm]
        if not cand:
            out.append(f"drawn piece {nm} is no section_true piece (or cut by plane_cuts)")
        elif not all(any(poly_match(P, sp) for sp in cand) for P in artist_polys(a) if len(P) >= 3):
            out.append(f"drawn piece {nm} differs from its spec polygon")
    return out


def st_admitted(ctx, pose, row, a):
    """K5 admission (1.4 P4, O7): an area artist of a section_true row that carries a piece name and equals that spec
    piece (poly_match) is the true section, admitted at any vertex count (receiver rim 5, collet cone 4 on a cone or
    cylinder row); the premise is section_true_issues (K8)."""
    nm = getattr(a, PIECE_ATTR, None)
    if nm is None or not row.get("section_true"):
        return False
    cand = [sp for n_, _, sp in st_polys(ctx, pose, row) if n_ == nm]
    polys = [P for P in artist_polys(a) if len(P) >= 3]
    return bool(polys) and bool(cand) and all(any(poly_match(P, sp) for sp in cand) for P in polys)


def inner_edge(poly, tol=TOL_Z):
    """The non-horizontal edge of a piece nearest the axis (least mean |u|): ((u0, z0), (u1, z1)) ordered by z."""
    n = len(poly)
    eds = [(poly[i], poly[(i + 1) % n]) for i in range(n) if abs(poly[i][1] - poly[(i + 1) % n][1]) > tol]
    if not eds:
        return None
    a, b = min(eds, key=lambda e: (abs(e[0][0]) + abs(e[1][0])) / 2)
    return (a, b) if a[1] <= b[1] else (b, a)


def vertical_edge_issue(polys, tol=TOL_Z):
    """S4-d (Sean STOP S4-A; TP1.1-4): the inner (bore) edge of every selected piece keeps u constant within tol."""
    if not polys:
        return "no piece drawn"
    for k, P in enumerate(polys):
        e = inner_edge(P, tol)
        if e is None:
            return f"piece {k}: no non-horizontal edge"
        if abs(e[1][0] - e[0][0]) > tol:
            return f"piece {k}: inner edge u {e[0][0]:.2f} at z {e[0][1]:.2f} to u {e[1][0]:.2f} at z {e[1][1]:.2f} (du {abs(e[1][0] - e[0][0]):.2f} > {tol:g})"
    return None


def inner_taper_issue(polys, narrows, tol=TOL_Z):
    """Taper on the inner (bore) edge (holder cone: the bore narrows upward while the material widens): narrows up needs
    |u| at the edge top < |u| at its bottom - tol; down the converse."""
    for k, P in enumerate(polys):
        e = inner_edge(P, tol)
        if e is None:
            return f"piece {k}: no inner edge"
        lo, hi = abs(e[0][0]), abs(e[1][0])
        ok = hi < lo - tol if narrows == "up" else lo < hi - tol if narrows == "down" else None
        if ok is None:
            return f"unknown taper {narrows!r} on the inner edge"
        if not ok:
            return f"piece {k}: inner edge |u| {lo:.2f} at the bottom, {hi:.2f} at the top"
    return None


def _ev_S(ctx, pose, e):
    return _z_S_expr(ctx, pose, str(e))


def _ev(ctx, pose, e):
    import check_stack as _cs
    names = ((ctx.stack or {}).get("poses", {}).get(pose, {}) or {}).get("vars_z_A", {})
    return float(_cs.eval_expr(str(e), ctx.P, names))


def _side_polys(own, sign):
    polys = [P for a in own for P in artist_polys(a) if len(P) >= 3]
    return [P for P in polys if (centroid([P])[0] > 0) == (sign > 0)]


def slit_spec(rows, prow):
    sl = prow.get("slits") or {}
    if sl.get("same_as"):
        sl = (rows.get(sl["same_as"]) or {}).get("slits") or {}
    return sl


def poly_chord(poly, z, tol=1e-9):
    """(lo, hi) x interval of a convex drawn polygon at height z, or None (P5f, Topologist F1, F2, F5)."""
    xs, n = [], len(poly)
    for i in range(n):
        (x0, z0), (x1, z1) = poly[i], poly[(i + 1) % n]
        if abs(z1 - z0) <= 1e-12:
            if abs(z - z0) <= tol:
                xs += [x0, x1]
            continue
        if min(z0, z1) - tol <= z <= max(z0, z1) + tol:
            xs.append(x0 + (x1 - x0) * (z - z0) / (z1 - z0))
    return (min(xs), max(xs)) if xs else None


def union_chords(polys, z, tol=TOL_Z):
    """Merged x intervals of the pieces at height z (pieces meeting within tol are one interval)."""
    iv = sorted(c for c in (poly_chord(P, z) for P in polys) if c)
    out = []
    for a, b in iv:
        if out and a <= out[-1][1] + tol:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def slit_issues(ctx, ax, pose, prow, arts, own, rows):
    """1.4 P4 tick admission for the section-view tick class (collet:slits; Topologist P2r 3.1, Designer/Topologist form
    (a)). Premise: a slit behind the plane is shown by one dashed line per declared slit, from its open face to its closed
    end, with a dashed horizontal tick across the wall at the closed end, and the line states nothing else. Spec slits
    {count_drawn, lines [{side, theta, open, from, to}], tick: wall} (same_as: another row's slits). (i0) spec lint: every
    line's slit lies behind the plane, cos(theta) < 0 (the premise of (iv); P5f, Topologist F1 c). (n) count: count_drawn
    vertical lines and as many ticks, one per spec line, every artist a two-vertex Line2D; each drawn line is read as the
    spec line of nearest z mid. (i) sign: sin(theta) x u_drawn > 0 (the line sits on the side the slit lies). (ii)
    containment: every point of the line, sampled at <= 0.5 with both ends, inside the union of the row's drawn pieces on
    the line's side within TOL_Z (P5f, Topologist F1 b: the convex hull admitted the foot-step triangle). (iii) open face:
    the open end (top or bottom) at the side pieces' z extreme and on a horizontal face edge there (face_spans). (iv)
    dashed (hidden: the slit lies behind the plane). (t) the closed end at the spec closed z and one horizontal tick
    there on the line's side, spanning the wall: its ends equal the ends of the union chord of the side pieces that holds
    the line at the closed z within TOL_Z, so the tick lies inside the part (P5f, Topologist F1 a), and dashed (F1 d).
    Scope: every row with sub_artists slits in a side or section view."""
    fid = prow["id"]
    if ctx.view not in SIDE_VIEWS:
        return [f"slits on {fid} admitted in a side or section view only (view {ctx.view})"]
    sl = slit_spec(rows, prow)
    lines = sl.get("lines") or []
    if not lines or "count_drawn" not in sl:
        return [f"slits on {fid} without slits.lines / count_drawn in the spec"]
    if sl.get("tick") != "wall":
        return [f"slits on {fid}: spec error, slits.tick {sl.get('tick')!r} (the tick spans the wall: tick: wall; P5f, Topologist F1 a)"]
    behind = []
    for ln in lines:   # (i0)
        th = _ev(ctx, pose, ln["theta"])
        if math.cos(math.radians(th)) >= 0:
            behind.append(f"slits on {fid}: spec line theta {th:.0f} has cos(theta) {math.cos(math.radians(th)):+.4f} >= 0, "
                          f"not behind the plane (a slit in front is cut away; one in the plane is drawn) (i0)")
    if behind:
        return behind
    out, verts, ticks = [], [], []
    for a in arts:
        if not isinstance(a, Line2D) or len(artist_polys(a)[0]) != 2:
            out.append(f"slits on {fid}: {type(a).__name__} is not a two-vertex Line2D (n)")
            continue
        (xa, za), (xb, zb) = artist_polys(a)[0]
        if abs(za - zb) <= TOL_Z:
            ticks.append(a)
        elif abs(xa - xb) <= TOL_Z:
            verts.append(a)
        else:
            out.append(f"slits on {fid}: line neither vertical nor horizontal (n)")
    want_n = int(sl["count_drawn"])
    if len(verts) != want_n or len(lines) != want_n or len(ticks) != want_n:
        out.append(f"slits on {fid}: {len(verts)} slit line(s) and {len(ticks)} tick(s) drawn, count_drawn {want_n}, spec lines {len(lines)} (n)")
    if out:
        return out
    spec_l = []
    for ln in lines:
        z0, z1 = sorted((_ev_S(ctx, pose, ln["from"]), _ev_S(ctx, pose, ln["to"])))
        spec_l.append((ln, z0, z1, math.sin(math.radians(_ev(ctx, pose, ln["theta"])))))
    used = set()
    for a in verts:
        (xa, za), (xb, zb) = artist_polys(a)[0]
        u, lo, hi = (xa + xb) / 2, min(za, zb), max(za, zb)
        k = min((i for i in range(len(spec_l)) if i not in used), key=lambda i: abs((spec_l[i][1] + spec_l[i][2]) / 2 - (lo + hi) / 2))
        used.add(k)
        ln, s0, s1, sn = spec_l[k]
        tag = f"slits on {fid}, theta {_ev(ctx, pose, ln['theta']):.0f} line at u {u:.2f}"
        if sn * u <= 0:   # (i)
            out.append(f"{tag}: sin(theta) {sn:+.4f} x u {u:+.2f} <= 0, drawn on the far side (i)")
        side = _side_polys(own, 1 if u > 0 else -1)
        if not side:
            out.append(f"{tag}: no drawn piece of {fid} on that side (ii)")
            continue
        ns = max(1, math.ceil((hi - lo) / 0.5))
        miss = [z for z in (lo + (hi - lo) * i / ns for i in range(ns + 1))
                if not any(a - TOL_Z <= u <= b + TOL_Z for a, b in union_chords(side, z))]
        if miss:   # (ii)
            out.append(f"{tag}: leaves the drawn {fid} (z {lo:.2f} to {hi:.2f}; {len(miss)} of {ns + 1} samples outside the union of its pieces "
                       f"on that side, e.g. z {miss[0]:.2f}) (ii)")
        top = ln.get("open") == "top"
        zf = extent_z(side)[1] if top else extent_z(side)[0]
        ze = hi if top else lo
        spans = face_spans(side, zf)
        if abs(ze - zf) > TOL_Z or not any(s0_ - TOL_Z <= u <= s1_ + TOL_Z for s0_, s1_ in spans):   # (iii)
            out.append(f"{tag}: open {ln.get('open')} end at z {ze:.2f} does not meet the {ln.get('open')} face (z {zf:.2f}, "
                       f"spans {', '.join(f'{x0:.2f} to {x1:.2f}' for x0, x1 in spans) or 'none'}) (iii)")
        if a.get_linestyle() in SOLID_STYLES:   # (iv)
            out.append(f"{tag}: drawn solid (hidden: the slit lies behind the plane) (iv)")
        zc = lo if top else hi
        zc_spec = s0 if top else s1
        tk = [t for t in ticks if (sum(v[0] for v in artist_polys(t)[0]) > 0) == (u > 0)
              and abs(artist_polys(t)[0][0][1] - zc) <= TOL_Z]
        wall = next(((a, b) for a, b in union_chords(side, zc) if a - TOL_Z <= u <= b + TOL_Z), None)
        if abs(zc - zc_spec) > TOL_Z or len(tk) != 1 or wall is None:   # (t)
            out.append(f"{tag}: closed end at z {zc:.2f} (spec {zc_spec:.2f}) needs one horizontal tick across the wall ({len(tk)} found"
                       f"{'' if wall else ', no wall chord holds the line'}) (t)")
        else:
            t0, t1 = sorted(v[0] for v in artist_polys(tk[0])[0])
            if abs(t0 - wall[0]) > TOL_Z or abs(t1 - wall[1]) > TOL_Z:
                out.append(f"{tag}: tick u [{t0:.2f}, {t1:.2f}] at z {zc:.2f} against the wall {wall[0]:.2f} to {wall[1]:.2f} "
                           f"(tick: wall; a tick past the wall leaves the part) (t)")
            if tk[0].get_linestyle() in SOLID_STYLES:
                out.append(f"{tag}: tick drawn solid (hidden: the closed end lies behind the plane) (iv)")
    return out


def wing_issues(ctx, ax, pose, prow, arts, own):
    """1.4 P4 beyond sub-artist admission by declared x_band (Designer P3a O3; Topologist signs at (c)): a part of a row
    lying past the beyond band (0 > x >= -profile.width, section convention 3) is admitted only as a hidden outline
    occluded by its own row. Spec wing {u, z, x_band}. (w0) x_band declared (else the part is refused, as K8-B74 refuses a
    beyond row past the band). (i) every artist dashed, unfilled and unhatched (a hatch reads as cut material; P5f,
    Designer N1). (ii) drawn u and z extents equal wing.u and wing.z (z_S) within TOL_Z. (iii) P5f (Topologist F2,
    Designer D-c1): every drawn edge is covered over its whole z interval, exactly (gaps > TOL_Z fail), by the union of
    the z bands of the occluders: the row's section_true revolve half-profile pieces (plane_cuts ignored: the occluder is
    the revolve profile, plane_cuts describe the plane only) with r_out > max |u| of the edge and r_out <= -x_band[1] (the
    revolved material at r <= r_out lies between the viewer and the part at |x| >= -x_band[1]: a sufficient half-space
    condition). Premise of ignoring plane_cuts, asserted in (iii): every occluder read has its in-front material within
    asin(max |u| / r_in) < 45 deg of theta 180 (the plane cuts lie at theta 90 or 270, K8 plane_cuts lint)."""
    fid = prow["id"]
    w = prow.get("wing") or {}
    if w.get("in_plane"):
        return wing_in_plane_issues(ctx, ax, pose, prow, arts)
    if not w.get("x_band"):
        return [f"wing on {fid} without wing.x_band: a part past the beyond band is not drawn (w0)"]
    if not all(k in w for k in ("u", "z")):
        return [f"wing on {fid} without wing.u / wing.z in the spec"]
    out = []
    for a in arts:
        if not isinstance(a, Patch) or a.get_linestyle() in SOLID_STYLES or a.get_fill() or a.get_hatch():
            how = ("filled" if a.get_fill() else "hatched " + repr(a.get_hatch()) if a.get_hatch() else "solid") if isinstance(a, Patch) else "solid"
            out.append(f"wing on {fid}: {type(a).__name__} drawn {how} (dashed, unfilled, unhatched outline) (i)")
    pts = [v for a in arts for P in artist_polys(a) for v in P]
    if not pts:
        return out + [f"wing on {fid}: nothing drawn"]
    u0, u1 = sorted(_ev(ctx, pose, e) for e in w["u"])
    z0, z1 = sorted(_ev_S(ctx, pose, e) for e in w["z"])
    du = (min(v[0] for v in pts), max(v[0] for v in pts))
    dz = (min(v[1] for v in pts), max(v[1] for v in pts))
    if max(abs(du[0] - u0), abs(du[1] - u1), abs(dz[0] - z0), abs(dz[1] - z1)) > TOL_Z:   # (ii)
        out.append(f"wing on {fid}: drawn u [{du[0]:.2f}, {du[1]:.2f}] z [{dz[0]:.2f}, {dz[1]:.2f}] against spec u [{u0:.2f}, {u1:.2f}] z [{z0:.2f}, {z1:.2f}] (ii)")
    xb = sorted(_ev(ctx, pose, e) for e in w["x_band"])
    r_lim = -xb[1]
    names = ((ctx.stack or {}).get("poses", {}).get(pose, {}) or {}).get("vars_z_A", {})
    prof = {k: v for k, v in prow.items() if k != "plane_cuts"}   # the revolve half-profile
    occ = []
    for name, side, sp in section_true_polys(ctx.P, names, prof):
        if side < 0:
            continue
        rs = [v[0] for v in sp]
        occ.append((name, min(v[1] for v in sp), max(v[1] for v in sp), min(rs), max(rs)))
    gaps, wide, read = [], set(), set()
    for a in arts:
        for P in artist_polys(a):
            n = len(P)
            for i in range(n if n > 2 else n - 1):
                (ua, za), (ub, zb) = P[i], P[(i + 1) % n]
                um = max(abs(ua), abs(ub))
                lo, hi = min(za, zb), max(za, zb)
                iv = sorted((zl, zh) for nm, zl, zh, ri, ro in occ if ro > um and ro <= r_lim + TOL_Z)
                for nm, zl, zh, ri, ro in occ:
                    if ro > um and ro <= r_lim + TOL_Z:
                        read.add(nm)
                        if um >= ri * math.sin(math.radians(45)):
                            wide.add(nm)
                cur, started = lo, False
                for zl, zh in iv:
                    if zl > cur + TOL_Z:
                        break
                    if zh >= cur - TOL_Z:
                        cur, started = max(cur, zh), True
                        if cur >= hi - TOL_Z:
                            break
                if not (started and cur >= hi - TOL_Z):
                    gaps.append((cur if started else lo, hi))
    if gaps:   # (iii)
        g0 = min(g[0] for g in gaps)
        out.append(f"wing on {fid}: {len(gaps)} drawn edge(s) not occluded by a section_true piece of {fid} (r_out <= {r_lim:.2f}, r_out > |u|) "
                   f"over their whole z extent, first gap from z_S {g0:.2f} (iii)")
    if wide:   # (iii) premise of reading the revolve profile with plane_cuts ignored
        out.append(f"wing on {fid}: occluder(s) {', '.join(sorted(wide))} read with in-front material 45 deg or more off theta 180 "
                   f"(asin(max |u| / r_in) >= 45): a plane cut at theta 90 or 270 may lie in the sight band (iii p)")
    return out


def draw_in_plane_wings(ax, P, names, row):
    """1.4 (h) r2 (Design Notes 35 R2): the in-plane wing form, sub-artist <row>:wing: one solid unfilled Rectangle per
    wing at u = [r_in, r_out] cos theta_k, theta_k = k 360 / count, over the wing z band (z_S); wing_in_plane_issues
    judges it."""
    import check_stack as _cs
    wg = row["wing"]
    ev = lambda e: float(_cs.eval_expr(str(e), P, names))  # noqa: E731
    r_in, r_out = sorted(ev(e) for e in wg["u"])
    z0, z1 = sorted(_cs.to_shop_floor(ev(e), P) for e in wg["z"])
    n = int(round(ev(wg["count"])))
    for k in range(n):
        c = math.cos(math.radians(k * 360.0 / n))
        u0, u1 = sorted((r_in * c, r_out * c))
        draw(f"{row['id']}:wing", Rectangle((u0, z0), u1 - u0, z1 - z0, fill=False, edgecolor="k", linewidth=1), ax)


WING_VIEW_PLANE = {"side_xz": lambda th: math.sin(math.radians(th))}   # the view plane holds azimuth th where this is 0


def wing_in_plane_issues(ctx, ax, pose, prow, arts):
    """1.4 (h) r2 (Design Notes 35 R2, M1 S1 r9 F1): the in-plane wing form of a side view. Spec wing {in_plane: true, u:
    [r_in, r_out], z: [lo, hi], count}. (p0) premise: every wing azimuth k 360 / count (k = 0 .. count - 1) lies in the
    view plane (side_xz: sin theta = 0 within 1e-9), so each wing is seen in its true outline at u = r cos theta; a view
    without the in-plane rule is refused. (i) every artist an unfilled, unhatched, solid Patch outline (a visible edge in
    elevation). (ii) one outline per wing: the drawn rings, sorted by u, equal [r_in, r_out] x [lo, hi] (z_S) at u = r cos
    theta for each azimuth, within TOL_Z."""
    fid = prow["id"]
    w = prow.get("wing") or {}
    if not all(k in w for k in ("u", "z", "count")):
        return [f"wing on {fid} in_plane without wing.u / wing.z / wing.count in the spec"]
    rule = WING_VIEW_PLANE.get(ctx.view)
    if rule is None:
        return [f"wing on {fid} in_plane in view {ctx.view}: no in-plane rule for this view (p0)"]
    n = int(round(_ev(ctx, pose, w["count"])))
    ths = [k * 360.0 / n for k in range(n)] if n > 0 else []
    off = [th for th in ths if abs(rule(th)) > 1e-9]
    out = []
    if not ths or off:
        out.append(f"wing on {fid}: wing azimuth(s) {', '.join(f'{t:g}' for t in off) or 'none'} outside the {ctx.view} plane (p0)")
    for a in arts:
        if not isinstance(a, Patch) or a.get_fill() or a.get_hatch() or a.get_linestyle() not in SOLID_STYLES:
            out.append(f"wing on {fid}: {type(a).__name__} not an unfilled, unhatched, solid outline (i)")
    r0, r1 = sorted(_ev(ctx, pose, e) for e in w["u"])
    z0, z1 = sorted(_ev_S(ctx, pose, e) for e in w["z"])
    want = sorted(tuple(sorted((r0 * math.cos(math.radians(t)), r1 * math.cos(math.radians(t))))) for t in ths)
    got = sorted(((min(v[0] for v in P), max(v[0] for v in P)), (min(v[1] for v in P), max(v[1] for v in P)))
                 for a in arts for P in artist_polys(a) if len(P) >= 3)
    if len(got) != len(want):
        return out + [f"wing on {fid}: {len(got)} outline(s) drawn against {len(want)} wings (ii)"]
    for (ua, ub), ((ga, gb), (za, zb)) in zip(want, got):
        if max(abs(ga - ua), abs(gb - ub), abs(za - z0), abs(zb - z1)) > TOL_Z:
            out.append(f"wing on {fid}: drawn u [{ga:.2f}, {gb:.2f}] z [{za:.2f}, {zb:.2f}] against u [{ua:.2f}, {ub:.2f}] z [{z0:.2f}, {z1:.2f}] (ii)")
    return out


def sweep_issues(ctx, ax, pose, prow, arts, own):
    """1.4 P4 (S3 sweep form as a sub-artist): the wing sweep is two dashed vertical two-vertex Line2D at u = -+ sweep.r
    within TOL_Z over the row's drawn z extent. (s1) type and count; (s2) dashed; (s3) position and extent."""
    fid = prow["id"]
    sw = prow.get("sweep") or {}
    if "r" not in sw:
        return [f"sweep on {fid} without sweep.r in the spec"]
    if len(arts) != 2 or not all(isinstance(a, Line2D) and len(artist_polys(a)[0]) == 2 for a in arts):
        return [f"sweep on {fid}: needs two two-vertex Line2D ({len(arts)} artists) (s1)"]
    r = _ev(ctx, pose, sw["r"])
    ez = extent_z([P for a in own for P in artist_polys(a)])
    out = []
    got = []
    for a in arts:
        (xa, za), (xb, zb) = artist_polys(a)[0]
        if a.get_linestyle() in SOLID_STYLES:
            out.append(f"sweep on {fid} drawn solid (dashed extent line) (s2)")
        got.append((xa + xb) / 2)
        if abs(xa - xb) > TOL_Z or abs(min(za, zb) - ez[0]) > TOL_Z or abs(max(za, zb) - ez[1]) > TOL_Z:
            out.append(f"sweep on {fid}: line u {xa:.2f} z {min(za, zb):.2f} to {max(za, zb):.2f} against vertical over {ez[0]:.2f} to {ez[1]:.2f} (s3)")
    for w_, g in zip((-r, r), sorted(got)):
        if abs(w_ - g) > TOL_Z:
            out.append(f"sweep on {fid}: line at u {g:.2f} against {w_:.2f} (sweep.r) (s3)")
    return out


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
        rows_by = {r["id"]: r for r in rows}
        for g in sorted((gids | text_gids) - ids):
            if any(g.endswith(sfx) and g[:-len(sfx)] in ids for sfx in SUB_SUFFIXES) and g in gids:
                continue      # sub-artist of a row; K5 rules its admission (1.2 (h), Designer M1 r1 F1)
            if ":" in g and g in gids:
                par, sub = g.rsplit(":", 1)
                pr = rows_by.get(par)
                if pr is not None and par in gids and (sub == MARK_SUB or sub in (pr.get("sub_artists") or [])):
                    continue  # 1.3 P4: mark (P0T section 4) or declared sub-artist with its parent drawn; K5 rules admission
            other = (getattr(ctx, "other_axes", None) or {}).get(g)
            issues.append(f"{pose}: tagged artist {g} has no spec row" + (f" in this Axes (declared in {', '.join(other)})" if other else ""))
    return result("K9", not issues, _summ(issues) if issues else f"every spec row drawn, every tagged artist in the spec ({len(ids)} rows)",
                  measured=len(issues), threshold=0, n_issues=len(issues))


# ======================================================================== 1.3 P4 (c): per-Axes views (TP-7), section view

class AxesFig:
    """One Axes of a figure presented as a one-Axes figure (TP-7): a check written for fig.axes[0] reads this Axes. Every
    other attribute (size, dpi, canvas, texts) is the real figure's; `fig` is the real figure."""

    def __init__(self, fig, ax):
        self.fig, self._ax = fig, ax

    @property
    def axes(self):
        return [self._ax]

    def __getattr__(self, name):
        return getattr(self.fig, name)


def real_figure(fig):
    return fig.fig if isinstance(fig, AxesFig) else fig


def declared_axes(spec):
    """The Axes a spec declares: the main Axes (spec view, id main_axes_id) and each entry of `insets` (id, view)."""
    view = (spec or {}).get("view")
    out = [{"id": main_axes_id(view), "view": view, "main": True}]
    for d in (spec or {}).get("insets") or []:
        out.append({"id": d["id"], "view": d["view"], "main": False, "decl": d})
    return out


def row_axes(row, main_id):
    return list(row.get("axes") or [main_id])


def needs_split(ctx):
    """Per-Axes evaluation applies when the spec declares insets or the view is a section view (TP-7, O4). S1 and S2 (one
    Axes, side_xz or plan_xy) are evaluated as before."""
    return bool((ctx.spec or {}).get("insets")) or ctx.view in SECTION_VIEWS


def axes_of_figure(fig, main_id):
    """({Axes id: Axes}, [Axes without a usable id]) of a figure; an Axes without sketch_axes counts as the main Axes when
    it is the first Axes."""
    out, extra = {}, []
    for i, ax in enumerate(real_figure(fig).axes):
        aid = getattr(ax, "sketch_axes", None)
        if aid is None and i == 0:
            aid = main_id
        if aid is None or aid in out:
            extra.append(ax)
        else:
            out[aid] = ax
    return out, extra


def sub_spec(spec, decl):
    """The spec as one Axes sees it: rows whose `axes` names this Axes; projection_by_axes[id] replaces projection;
    neighbours restricted to rows of this Axes; sense predicates with an `axes` field kept only in that Axes; the label
    only in the row's home Axes (the first entry of `axes`). The figure-level fields (figure note, not_drawn, planes,
    stack ties) stay with the main Axes."""
    main_id = main_axes_id(spec.get("view"))
    aid = decl["id"]
    rows_in = [r for r in spec.get("features", []) if aid in row_axes(r, main_id)]
    ids = {r["id"] for r in rows_in}
    rows = []
    for r in rows_in:
        r2 = dict(r)
        pba = r.get("projection_by_axes") or {}
        if aid in pba:
            r2["projection"] = pba[aid]
        r2["neighbours"] = [dict(nb, **{"class": nb["class_by_axes"][aid]}) if aid in (nb.get("class_by_axes") or {}) else nb
                            for nb in (r.get("neighbours") or []) if nb.get("id") in ids]   # P5f (TP FIX 7): class per Axes
        r2["sense"] = [pr for pr in (r.get("sense") or []) if _pred_in_axes(pr, aid, decl["view"], ids)]
        if row_axes(r, main_id)[0] != aid:
            if r.get("label"):
                r2["label_home"] = row_axes(r, main_id)[0]   # P5f (SW FIX 5): a label drawn here is refused by K4
            r2["label"] = None
        rows.append(r2)
    out = dict(spec)
    out["features"] = rows
    out["view"] = decl["view"]
    if not decl["main"]:
        for k in ("figure_note", "not_drawn", "part_list", "load_plane", "entry_plane", "stack_ties", "insets"):
            out.pop(k, None)
    return out


Z_PREDS = ("below", "above", "clears_above", "top_within", "rests_on", "mirror_about_axis", "face_rises")   # z-sense
PLAN_PREDS = ("ticks_radial", "outline_matches", "mirror_about_radial")


def _pred_in_axes(pr, aid, view, ids):
    """A sense predicate is evaluated in an Axes when its `axes` field is absent or names it, its target row is drawn
    there, and its kind reads that view: z predicates not in plan, plan-only predicates not in a side or section view."""
    if pr.get("axes") not in (None, aid):
        return False
    t = _pred_target(pr)
    if t is not None and t not in ids:
        return False
    if view == "plan_xy" and pr.get("pred") in Z_PREDS:
        return False
    if view in SIDE_VIEWS and pr.get("pred") in PLAN_PREDS:
        return False
    return True


def _pred_target(pr):
    return pr.get("of") or pr.get("seat") or (pr.get("axis") if pr.get("pred") == "mirror_about_axis" else None)


def orphan_predicates(spec):
    """1.3 P4 (TP-7): a sense predicate kept in no declared Axes (its `axes` names none, or its target shares no Axes with
    its row) is never evaluated: spec error, reported by K8 in the main Axes."""
    main_id = main_axes_id(spec.get("view"))
    decl = [d["id"] for d in declared_axes(spec)]
    rows = {r["id"]: r for r in spec.get("features", [])}
    out = []
    if not rows:
        return out
    for r in spec.get("features", []):
        ra = row_axes(r, main_id)
        for pr in r.get("sense") or []:
            views = {d["id"]: d["view"] for d in declared_axes(spec)}
            homes = [a for a in ra if a in decl and _pred_in_axes(pr, a, views[a], {k for k, rr in rows.items() if a in row_axes(rr, main_id)})]
            if not homes:
                out.append(f"{r['id']} {pr.get('pred')} {_pred_target(pr) or ''}: spec error, predicate evaluated in no declared Axes")
    return out


def class_by_axes_issues(spec):
    """P5f (Topologist FIX 7, F5): premise of a per-Axes neighbour class. A class_by_axes override to N in Axes A is
    admitted only when both rows are declared in another Axes of the figure where the pair keeps its base class C, F or
    G (so the true pieces are still tested); otherwise a K7 spec error, reported in the main Axes."""
    main_id = main_axes_id(spec.get("view"))
    decl = [d["id"] for d in declared_axes(spec)]
    rows = {r["id"]: r for r in spec.get("features", [])}
    out = []
    for r in spec.get("features", []):
        for nb in r.get("neighbours") or []:
            cba = nb.get("class_by_axes") or {}
            for aid, cls in cba.items():
                if aid not in decl:
                    out.append(f"{r['id']}|{nb.get('id')}: spec error, class_by_axes names undeclared Axes {aid}")
                    continue
                if cls != "N":
                    continue
                other = nb.get("id")
                kept = [a for a in decl if a != aid and a not in cba and a in row_axes(r, main_id)
                        and other in rows and a in row_axes(rows[other], main_id) and nb.get("class") in ("C", "F", "G")]
                if not kept:
                    out.append(f"{r['id']}|{other}: spec error, class_by_axes N in {aid} with the pair tested in no other Axes at its base class {nb.get('class')}")
    return out


def filter_stack(stack, ids):
    if not stack:
        return stack
    out = dict(stack)
    out["poses"] = {pid: dict(pr, features={k: v for k, v in pr["features"].items() if k in ids})
                    for pid, pr in stack["poses"].items()}
    return out


def _refl(pc):
    return [(y, x) for x, y in reversed(pc)]   # reflection across x = y; reversed keeps the ring orientation


def reflect_record(rec, row):
    """A check_stack feature record in the section frame (O4): reflection across x = y, so x' = plan y = section u and
    y' = plan x = depth along the section normal. A placed row's theta becomes 90 - theta and rot becomes -rot (the
    reflected footprint); the depth band is the spec depth (an x band in a section spec) hulled with the place x extent,
    or the place x extent, or the plan_poly x extent, as evaluate_spec builds it from y in a side view."""
    r = dict(rec)
    pl = rec.get("place")
    if pl:
        p = dict(pl)
        p["theta"], p["rot"] = 90.0 - pl["theta"], -pl.get("rot", 0)
        p["x"], p["y"] = list(pl["y"]), list(pl["x"])
        r["place"] = p
        r["depth_true"] = list(pl["x"])
    if rec.get("plan_pieces"):
        r["plan_pieces"] = [_refl(pc) for pc in rec["plan_pieces"]]
        r["plan_x"], r["plan_y"] = list(rec["plan_y"]), list(rec["plan_x"])
    if rec.get("sector"):
        sec = dict(rec["sector"])
        sec["theta"], sec["x"], sec["y"] = 90.0 - sec["theta"], list(rec["sector"]["y"]), list(rec["sector"]["x"])
        r["sector"] = sec
    if row.get("depth") is not None:
        if pl:
            d = rec.get("depth_spec") or rec.get("depth")
            r["depth_spec"] = list(d)
            r["depth"] = [min(d[0], pl["x"][0]), max(d[1], pl["x"][1])]
    elif pl:
        r["depth"] = list(pl["x"])
    elif rec.get("plan_pieces"):
        r["depth"] = list(rec["plan_x"])
    return r


def reflect_stack(stack, rows):
    """check_stack record in the section frame (reflect_record per feature); z values and stack names unchanged."""
    out = dict(stack)
    out["frame_view"] = "section_yz (reflected: x' = y, y' = x)"
    out["poses"] = {pid: dict(pr, features={k: reflect_record(v, rows.get(k, {})) for k, v in pr["features"].items()})
                    for pid, pr in stack["poses"].items()}
    return out


def axes_contexts(ctx):
    """[(decl, sub-context)] for a split context (needs_split): one sub-context per declared Axes with its view, its rows
    (sub_spec), its figures (AxesFig per pose; poses where the Axes is absent listed in missing_poses) and its stack
    (filtered to its rows; reflected for a section view). Cached on the context."""
    cache = getattr(ctx, "_axes_ctxs", None)
    if cache is not None:
        return cache
    spec = ctx.spec or {}
    main_id = main_axes_id(spec.get("view"))
    rows = {r["id"]: r for r in spec.get("features", [])}
    out = []
    for d in declared_axes(spec):
        ss = sub_spec(spec, d)
        ids = {r["id"] for r in ss["features"]}
        st = filter_stack(ctx.stack, ids)
        if st and d["view"] in SECTION_VIEWS:
            st = reflect_stack(st, rows)
        figs, missing = {}, []
        for pose, fig in (ctx.figs or {}).items():
            ax = axes_of_figure(fig, main_id)[0].get(d["id"])
            if ax is None:
                missing.append(pose)
            else:
                figs[pose] = AxesFig(real_figure(fig), ax)
        c = Ctx(P=ctx.P, spec=ss, figs=figs, stack=st, view=d["view"], script_paths=ctx.script_paths if d["main"] else [],
                overlay_path=ctx.overlay_path, check_stack_path=ctx.check_stack_path if d["main"] else None, anchors=ctx.anchors)
        c.axes_id, c.axes_role, c.parent, c.missing_poses = d["id"], "main" if d["main"] else "inset", ctx, missing
        c.other_axes = {r["id"]: row_axes(r, main_id) for r in rows.values() if d["id"] not in row_axes(r, main_id)}
        out.append((d, c))
    ctx._axes_ctxs = out
    return out


def axes_context(ctx, aid):
    """The sub-context of Axes aid (the context itself when it is not split; None when the spec does not declare aid)."""
    if not needs_split(ctx):
        return ctx
    return next((c for d, c in axes_contexts(ctx) if d["id"] == aid), None)


def undeclared_axes_issues(ctx):
    """TP-7 lint (replaces the 1.0 multi-Axes lint for split contexts): every Axes of every figure is a declared Axes."""
    out = []
    main_id = main_axes_id((ctx.spec or {}).get("view"))
    known = {d["id"] for d in declared_axes(ctx.spec)}
    for pose, fig in (ctx.figs or {}).items():
        found, extra = axes_of_figure(fig, main_id)
        for aid in sorted(set(found) - known):
            out.append(f"{pose}: Axes {aid} is not declared in the spec (insets)")
        if extra:
            out.append(f"{pose}: {len(extra)} Axes without a declared id (checks read declared Axes only)")
    return out


def _merge(cid, parts, extra):
    issues_n = sum((r.get("n_issues") or 0) for _, r in parts) + len(extra)
    ok = not extra and all(r["result"] == "pass" for _, r in parts)
    reasons = list(extra) + [f"[{d['id']}] {r['reason']}" for d, r in parts]
    failing = [r for _, r in parts if r["result"] != "pass"]
    cause = None if ok else ("absent" if not extra and failing and all(r.get("cause") == "absent" for r in failing) else "content")
    ms = [r.get("measured") for _, r in parts]
    num = all(isinstance(m, (int, float)) or m is None for m in ms)
    out = {"id": cid, "result": "pass" if ok else "fail", "reason": " | ".join(reasons), "n_issues": issues_n, "cause": cause,
           "measured": (max(m for m in ms if m is not None) if cid in ("K6",) else sum(m for m in ms if m is not None)) if num and any(m is not None for m in ms) else (None if num else ms),
           "threshold": parts[0][1].get("threshold") if parts else 0,
           "by_axes": {d["id"]: {"result": r["result"], "n_issues": r.get("n_issues"), "cause": r.get("cause")} for d, r in parts}}
    if any("states" in r for _, r in parts):
        out["states"] = [s for _, r in parts for s in r.get("states", [])]
        out["tests"] = [t for _, r in parts for t in r.get("tests", [])]
        out["test_fields"] = next((r["test_fields"] for _, r in parts if "test_fields" in r), K7_TEST_FIELDS)
        out["failing"] = sum(r.get("failing", 0) for _, r in parts)
        out["tests_axes"] = [d["id"] for d, r in parts for _ in r.get("tests", [])]
    return out


def per_axes(fn, cid):
    """TP-7: run check fn once per declared Axes with that Axes' view, rows and stack, and merge (reason prefixed by the
    Axes id). A declared Axes absent from a figure fails K3 and K9; an undeclared Axes fails K3."""
    def run(ctx):
        if not needs_split(ctx):
            return fn(ctx)
        parts, extra = [], []
        for d, c in axes_contexts(ctx):
            if c.missing_poses and cid in ("K3", "K9"):
                extra.append(f"[{d['id']}] declared Axes {d['id']} ({d['view']}) absent from figure(s) {', '.join(c.missing_poses)}")
            if not c.figs and not d["main"]:
                continue
            parts.append((d, fn(c)))
        if cid == "K3":
            extra += undeclared_axes_issues(ctx)
        return _merge(cid, parts, extra)
    run.__name__ = getattr(fn, "__name__", cid)
    run.unsplit = fn
    return run


CHECKS = {"K1": k1, "K2": k2, **{k: per_axes(f, k) for k, f in (("K3", k3), ("K4", k4), ("K5", k5), ("K6", k6), ("K7", k7), ("K8", k8), ("K9", k9))}}

