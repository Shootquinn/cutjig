"""Shared foundation: paths, YAML loader, params validation, 30-6060 profile builder.

Pure-python functions (no FreeCAD import) are usable from pytest. Functions that need
FreeCAD import it inside the function body.
Success of any FreeCAD run is a sentinel line plus a fresh artifact, never the exit code (A.15).
"""
import math
import os
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARAMS_PATH = ROOT / "params.yaml"
RESULTS_DIR = ROOT / "results"
PARTS_CACHE = ROOT / "parts_cache"
REFERENCE_DIR = ROOT / "reference"

_FC_CANDIDATES = [
    r"C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe",  # gameplan path (absent on this machine)
    os.path.expandvars(r"%LOCALAPPDATA%/Programs/FreeCAD 1.1/bin/freecadcmd.exe"),
]


def freecadcmd_path():
    for c in _FC_CANDIDATES:
        if os.path.exists(c):
            return c
    return None


STATUSES = ("DECLARED", "ASSUMED", "VERIFIED", "DERIVED")
HAND = "right"  # thread hand is a constant, not a params field (T1a)
_PRINTER_KEY = re.compile(r"^(printer|bed|nozzle|material|filament|bed_size)$", re.I)


# ---------------------------------------------------------------- params access
def load_params(path=None):
    with open(path or PARAMS_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def is_leaf(node):
    return isinstance(node, dict) and "value" in node


def iter_leaves(params, prefix=""):
    for k, v in params.items():
        key = f"{prefix}{k}"
        if is_leaf(v):
            yield key, v
        elif isinstance(v, dict):
            yield from iter_leaves(v, key + ".")


def leaf(params, key):
    node = params
    for part in key.split("."):
        if not isinstance(node, dict) or part not in node:
            raise KeyError(key)
        node = node[part]
    if not is_leaf(node):
        raise KeyError(f"{key} is not a leaf")
    return node


def get(params, key):
    return leaf(params, key)["value"]


def set_value(params, key, value):
    leaf(params, key)["value"] = value


def status_counts(params):
    c = {s: 0 for s in STATUSES}
    n = 0
    for _, lf in iter_leaves(params):
        n += 1
        if lf.get("status") in c:
            c[lf["status"]] += 1
    c["total"] = n
    return c


# ---------------------------------------------------------------- rules
REQUIRED_KEYS = [
    "iris.throat_open_diameter", "iris.throat_open_radius", "core.diameter_nominal", "core.diameters", "core.tol",
    "core.length_capture", "core.length_install", "core.length_optional",
    "upper.travel_max", "jig.height_target", "loads.torque_design", "loads.axial_design",
    "drill.tube_od", "drill.tube_id", "drill.r_face", "drill.kerf_standoff", "collets.count", "collets.spacing",
    "collets.envelope_min", "collets.envelope_max", "collets.min_throat_slack", "collet.c_i", "collet.min_wall", "thread.major", "thread.pitch",
    "chain.t_c", "chain.t_h", "chain.t_b", "fit.c_r", "fit.g_a", "fit.seat_clearance",
    "stop.collar_top_z", "stop.height_z", "stop.g_stop", "profile.width", "profile.height", "stock.on_hand", "frame.members",
]
CLEARANCE_KEYS = ["fit.c_r", "fit.g_a", "fit.seat_clearance", "collet.c_i"]
ICD_FIELDS = [
    "icd.datum_a", "icd.datum_b", "icd.datum_c", "icd.mounting_pattern", "icd.coaxiality_budget",
    "icd.keepout_radius", "icd.stop_height", "icd.stop_rating", "icd.footprint_x",
    "icd.footprint_y", "icd.tipover_statement", "icd.cable_exit",
    "icd.floor_above_datum_a", "icd.coaxiality_chain", "icd.core_lead_in_capture", "icd.core_lead_in_centring",
    "icd.core_lead_in_bore", "icd.column_foot_moment", "icd.torque_reaction", "icd.mass_target",
    "stop.collar_top_z", "stop.height_range", "stop.start_z", "upper.park_z", "upper.park_lock",
    "upper.manual_raise", "upper.raise_fuse", "upper.metal_stop", "hoist.anchor_member", "strap.rating",
    "strap.handle_radial", "column.spacing", "rest.height_positions", "rest.roller_count",
    "rest.centre_repeatability", "rest.release_tower", "rest.cam_lug_radius", "core.min_exposed",
]


def throat_diameter(params):
    """Open throat diameter, always 2 x the DECLARED radius (the diameter leaf is derived)."""
    return 2.0 * get(params, "iris.throat_open_radius")


def bore_free(params, d):
    """bore_free(d) = d + tau + c_i (tau = core tolerance)."""
    return d + get(params, "core.tol") + get(params, "collet.c_i")


def _find_printer_keys(node, path=""):
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            if _PRINTER_KEY.match(str(k)):
                out.append(f"printer key {path}{k}")
            out += _find_printer_keys(v, f"{path}{k}.")
    return out


def validate_params(params):
    """Return a list of error strings; empty list means accepted."""
    errs = []
    for k in REQUIRED_KEYS:
        try:
            leaf(params, k)
        except KeyError:
            errs.append(f"missing key {k}")
    if errs:
        return errs
    errs += _find_printer_keys(params)
    for k in CLEARANCE_KEYS:
        if get(params, k) < 0:
            errs.append(f"negative clearance {k} = {get(params, k)}")
    fam = get(params, "core.diameters")  # single source for the collet family
    if abs(get(params, "iris.throat_open_diameter") - throat_diameter(params)) > 1e-6:
        errs.append("iris.throat_open_diameter is not 2 x iris.throat_open_radius")
    if len(fam) != get(params, "collets.count"):
        errs.append("collets.count does not match len(core.diameters)")
    if any(abs((b - a) - get(params, "collets.spacing")) > 1e-9 for a, b in zip(fam, fam[1:])):
        errs.append("core.diameters not at collets.spacing")
    cap = throat_diameter(params) - get(params, "core.tol") - get(params, "collets.min_throat_slack")
    if get(params, "collets.envelope_max") > cap + 1e-9:
        errs.append(f"generator envelope_max {get(params, 'collets.envelope_max')} exceeds throat cap {cap:.3f}")
    lo, hi = get(params, "collets.envelope_min"), get(params, "collets.envelope_max")
    for d in fam:
        if not lo <= d <= hi:
            errs.append(f"family diameter {d} outside generator envelope [{lo}, {hi}]")
    if fam:
        need = bore_free(params, max(fam)) + 2 * (get(params, "chain.t_c") + get(params, "chain.t_h") + get(params, "chain.t_b"))
        if get(params, "thread.major") < need:
            errs.append(f"thread major {get(params, 'thread.major')} < largest collet bore plus walls {need:.3f}")
    if not (get(params, "core.length_capture") <= get(params, "core.length_install") <= get(params, "core.length_optional")):
        errs.append("core lengths not ordered capture <= install <= optional")
    if get(params, "upper.travel_max") <= 0:
        errs.append("upper.travel_max must be positive")
    for key, lf in iter_leaves(params):
        if lf.get("status") not in STATUSES:
            errs.append(f"{key}: bad status {lf.get('status')!r}")
    return errs


def check_throat_rule(params):
    """P8: core diameter + tolerance < open throat, for every family diameter."""
    throat = throat_diameter(params)
    tol = get(params, "core.tol")
    errs = []
    diameters = list(get(params, "core.diameters"))
    for d in sorted(set(diameters)):
        if d + tol >= throat:
            errs.append(f"d {d} + tol {tol} >= throat {throat}")
    return errs


def throat_slack_per_side(params, d):
    """Iris slack per side for a core of diameter d plus tolerance: (throat - d - tol) / 2."""
    return (throat_diameter(params) - d - get(params, "core.tol")) / 2.0


def check_envelope_request(params, d):
    """Collet generator refuses a diameter above throat - tol - slack (decision 7)."""
    cap = throat_diameter(params) - get(params, "core.tol") - get(params, "collets.min_throat_slack")
    if d > cap + 1e-9:
        return [f"requested {d} exceeds envelope cap {cap:.3f}: change `iris.throat_open_radius`"]
    return []


def check_icd(params):
    """P6: every ICD field present and non-empty."""
    errs = []
    try:
        if get(params, "icd.keepout_radius") < get(params, "drill.r_face") - 1e-9:
            errs.append("icd.keepout_radius below drill.r_face")
    except KeyError:
        pass
    for k in ICD_FIELDS:
        try:
            v = get(params, k)
        except KeyError:
            errs.append(f"missing {k}")
            continue
        if v is None or (isinstance(v, str) and not v.strip()) or v == []:
            errs.append(f"empty {k}")
    return errs


# ---------------------------------------------------------------- 30-6060 profile
# Measured section (8020-30-6060 X 1540.step): a hollow 2 x 2 module of 30 mm cells.
#   material = outer - T-slot cavities - void - cell bores - corner holes
#   void     = inner square (outer wall thickness) - (slot bodies U cell tubes)
# slot body = the slot cavity plus its lining (side lining, 45 degree web); cell tube = square block around each bore.
# All primitives are convex polygons or circles, so the area is an exact scanline integral (pure python)
# and the same primitives build the FreeCAD faces.
_ARC_SEGS = 16


def _rot(pts, deg, cx, cy):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def _rounded_square(half, r, n=_ARC_SEGS):
    pts = []
    for (sx, sy), start in (((1, 1), 0), ((-1, 1), 90), ((-1, -1), 180), ((1, -1), 270)):
        cx, cy = sx * (half - r), sy * (half - r)
        for i in range(n + 1):
            a = math.radians(start + 90.0 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _tube(cx, cy, th, kx, ky, r, n=_ARC_SEGS):
    """Square block of half-size th about (cx, cy); the corner toward (kx, ky) is rounded with radius r."""
    pts = []
    for (sx, sy), start in (((1, 1), 0), ((-1, 1), 90), ((-1, -1), 180), ((1, -1), 270)):
        if (sx, sy) == (kx, ky):
            ax, ay = cx + sx * (th - r), cy + sy * (th - r)
            pts += [(ax + r * math.cos(math.radians(start + 90.0 * i / n)),
                     ay + r * math.sin(math.radians(start + 90.0 * i / n))) for i in range(n + 1)]
        else:
            pts.append((cx + sx * th, cy + sy * th))
    return pts


def profile_primitives(params):
    """Return dict of 2D primitives, section in the XY plane centred on the origin."""
    g = lambda k: get(params, "profile." + k)
    w, h = g("width"), g("height")
    assert abs(w - h) < 1e-9, "profile builder assumes a square 2 x 2 module"
    half_cell = g("slot_pitch") / 2.0
    off = g("slot_offset")
    so = g("slot_opening") / 2.0
    nd, cd = g("slot_neck_depth"), g("slot_cavity_depth")
    cw = g("slot_cavity_width") / 2.0
    vd = g("slot_cavity_vertical_depth")
    ang = math.radians(g("slot_flank_angle"))
    lining, web = g("slot_lining"), g("web_thickness")
    wall = g("wall_thickness")
    yf = half_cell                      # face, local frame: v outward from the cell centre
    v_neck = yf - nd
    v_flank0 = v_neck - vd              # flank starts at the cavity half-width
    v_floor = yf - nd - cd              # slot floor = top of the cell tube
    th = v_floor                        # tube half-size equals floor depth (measured 5.835)
    fh = cw - (v_flank0 - v_floor) / math.tan(ang)   # floor half-width
    dx, dv = math.cos(ang), math.sin(ang)            # flank runs (-dx, -dv) from (cw, v_flank0)
    nx, nv = dv, -dx                                 # outward normal of the flank (+u, down)
    p0u, p0v = cw + web * nx, v_flank0 + web * nv

    def v_at(u):                                      # offset flank line, v at u
        return p0v + (u - p0u) * (dv / dx)

    B = cw + lining
    cav_neck = [(-so, yf + 1.0), (so, yf + 1.0), (so, v_neck), (-so, v_neck)]
    cav_main = [(-cw, v_neck), (cw, v_neck), (cw, v_flank0), (fh, v_floor), (-fh, v_floor), (-cw, v_flank0)]
    body = [(-B, yf), (B, yf), (B, v_at(B)), (th, v_at(th)), (-th, v_at(th)), (-B, v_at(B))]
    prim = {"outer": _rounded_square(w / 2.0, g("outer_corner_radius")),
            "inner": [(-(w / 2 - wall), -(h / 2 - wall)), (w / 2 - wall, -(h / 2 - wall)),
                      (w / 2 - wall, h / 2 - wall), (-(w / 2 - wall), h / 2 - wall)],
            "cavities": [], "bodies": [], "tubes": [], "bores": [], "bore_lobes": [],
            "bore_channels": [], "corner_holes": [], "notches": []}
    tr, nw, nd_ = g("tube_corner_radius"), g("notch_half_width"), g("notch_depth")
    rb = g("centre_bore") / 2.0
    lr, ld, lw = g("bore_lobe_radius"), g("bore_lobe_centre_radius"), g("bore_lobe_channel_width")
    chs = g("corner_hole_size") / 2.0
    chi = g("corner_hole_inset")
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * off, sy * off
            prim["tubes"].append(_tube(cx, cy, th, -sx, -sy, tr))
            for deg in (0, 90, 180, 270):   # V-notch in each of the four tube faces
                prim["notches"].append(_rot([(-nw, th), (nw, th), (0.0, th - nd_)], deg, cx, cy))
            prim["bores"].append((cx, cy, rb))
            for k in range(4):
                a = math.radians(45 + 90 * k)
                prim["bore_lobes"].append((cx + ld * math.cos(a), cy + ld * math.sin(a), lr))
                seg = [(rb * 0.5, -lw / 2), (ld, -lw / 2), (ld, lw / 2), (rb * 0.5, lw / 2)]
                prim["bore_channels"].append(_rot(seg, 45 + 90 * k, cx, cy))
            cc = w / 2 - chi - chs
            hx, hy = sx * cc, sy * cc
            prim["corner_holes"].append([(hx - chs, hy - chs), (hx + chs, hy - chs), (hx + chs, hy + chs), (hx - chs, hy + chs)])
            # the two module-boundary faces of this cell (local +v rotated to the outward direction)
            for deg in ((0 if sy > 0 else 180), (90 if sx < 0 else 270)):
                prim["cavities"].append(_rot(cav_neck, deg, cx, cy))
                prim["cavities"].append(_rot(cav_main, deg, cx, cy))
                prim["bodies"].append(_rot(body, deg, cx, cy))
    return prim


def profile_polygons(params):
    """Back-compatible view: (outer, cavities, bore_radius). Cavities are the 16 polygons of the 8 T-slots."""
    prim = profile_primitives(params)
    return prim["outer"], prim["cavities"], get(params, "profile.centre_bore") / 2.0


def polygon_area(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
                   for i in range(len(pts)))) / 2.0


def _poly_interval(pts, y):
    """x-interval of a convex polygon on the line Y = y, or None."""
    xs = []
    n = len(pts)
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        if (y0 <= y < y1) or (y1 <= y < y0):
            xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
    return (min(xs), max(xs)) if len(xs) >= 2 else None


def _circle_interval(c, y):
    cx, cy, r = c
    d = r * r - (y - cy) ** 2
    if d <= 0:
        return None
    s = math.sqrt(d)
    return (cx - s, cx + s)


def _union(iv):
    iv = sorted(tuple(i) for i in iv if i)
    out = []
    for a, b in iv:
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def _subtract(base, cut):
    res = []
    for a, b in base:
        cur = a
        for c, d in cut:
            if d <= cur or c >= b:
                continue
            if c > cur:
                res.append([cur, c])
            cur = max(cur, d)
        if cur < b:
            res.append([cur, b])
    return res


def profile_area_model(params, lines=3000):
    """Section area (mm2) by scanline integration of the primitives (no FreeCAD needed)."""
    P = profile_primitives(params)
    w = get(params, "profile.width")
    total = 0.0
    for i in range(lines):
        y = -w / 2 + w * (i + 0.5) / lines
        outer = _union([_poly_interval(P["outer"], y)])
        inner = _union([_poly_interval(P["inner"], y)])
        solid_in_inner = _union([_poly_interval(q, y) for q in P["bodies"] + P["tubes"]])
        void = _subtract(inner, solid_in_inner)
        holes = _union([_poly_interval(q, y) for q in P["cavities"] + P["corner_holes"] + P["bore_channels"] + P["notches"]]
                       + [_circle_interval(c, y) for c in P["bores"] + P["bore_lobes"]] + void)
        total += sum(b - a for a, b in _subtract(outer, holes))
    return total * (w / lines)


def build_profile(length, params=None):
    """Parametric extrusion of the measured 30-6060 section along +Z. Requires FreeCAD (call inside freecadcmd)."""
    import FreeCAD as App
    import Part

    params = params or load_params()
    P = profile_primitives(params)

    def face(pts):
        v = [App.Vector(x, y, 0) for x, y in pts]
        return Part.Face(Part.makePolygon(v + [v[0]]))

    def disc(c):
        return Part.Face(Part.Wire(Part.makeCircle(c[2], App.Vector(c[0], c[1], 0))))

    def fuse(faces):
        acc = faces[0]
        for f in faces[1:]:
            acc = acc.fuse(f)
        return acc.removeSplitter()

    void = face(P["inner"]).cut(fuse([face(q) for q in P["bodies"] + P["tubes"]]))
    cutters = [face(q) for q in P["cavities"] + P["corner_holes"] + P["bore_channels"] + P["notches"]] + \
              [disc(c) for c in P["bores"] + P["bore_lobes"]]
    f = face(P["outer"]).cut(void).cut(fuse(cutters)).removeSplitter()
    return f.extrude(App.Vector(0, 0, length))
