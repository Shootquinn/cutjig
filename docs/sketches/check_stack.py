"""Pose stack arithmetic for the sketches, from params.yaml and the overlay only.

Frames (FRAME RULING, gameplan Design Notes 17):
  z_A  datum A = base-plate underside = frame top plane. params stop.*, upper.park_z, stop.collar_top_z are z_A.
  z_R  receiver floor (ASSEMBLY.md "floor frame"): z_R = z_A - icd.floor_above_datum_a.
  z_S  shop floor, the frame the sketches plot in: z_S = z_A + jig.datum_a_above_floor.
Every spec z_rule is evaluated in z_A; to_shop_floor() is the one z_A -> z_S conversion, from_shop_floor() its inverse.
K6 anchors these signs against independent numbers (sketch_common.stack_anchor_issues).

Imports: stdlib and sketch_loader only (K6 B3 guard). Usage: check_stack.py [spec.yaml] [--params P] [--overlay O]
"""
import argparse
import ast
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import sketch_loader  # noqa: E402

DEFAULT_Q9 = ["core.length_capture", "core.length_install"]


def cosd(t):
    return math.cos(math.radians(t))


def sind(t):
    return math.sin(math.radians(t))


# ---------------------------------------------------------------- symbols (H5, Design Notes 23: clearance c)

INF = float("inf")
EPS = 1e-9


class PW:
    """Piecewise-linear function of one spec symbol s on its domain [lo, inf): segments (s_lo, s_hi, a, b), value a + b*s.
    Closed under +, -, scalar *, scalar /, unary -, min, max, abs. A spec symbol (spec `symbols`) has no value; an
    expression that reads it evaluates to a PW, check_stack reports it as an expression, and a drawn value is taken only
    where the PW is constant on its first segment (numeric()). Product or quotient of two non-constant PWs: ValueError."""

    def __init__(self, segs, name="c"):
        self.name = name
        out = []
        for s in segs:
            if out and abs(out[-1][2] - s[2]) < EPS and abs(out[-1][3] - s[3]) < EPS:
                out[-1] = (out[-1][0], s[1], out[-1][2], out[-1][3])
            else:
                out.append(tuple(s))
        self.segs = out

    @classmethod
    def sym(cls, name="c", lo=0.0):
        return cls([(lo, INF, 0.0, 1.0)], name)

    def _lift(self, o):
        return o if isinstance(o, PW) else PW([(self.segs[0][0], INF, float(o), 0.0)], self.name)

    def _merge(self, o, fn):
        o = self._lift(o)
        cuts = sorted({s[0] for s in self.segs + o.segs} | {s[1] for s in self.segs + o.segs})
        out = []
        for lo, hi in zip(cuts, cuts[1:]):
            out += fn(lo, hi, self._at(lo, hi), o._at(lo, hi))
        return PW(out, self.name)

    def _at(self, lo, hi):
        mid = lo + 1.0 if hi == INF else (lo + hi) / 2
        return next((a, b) for s0, s1, a, b in self.segs if s0 <= mid <= s1)

    def __add__(self, o):
        return self._merge(o, lambda lo, hi, p, q: [(lo, hi, p[0] + q[0], p[1] + q[1])])
    __radd__ = __add__

    def __sub__(self, o):
        return self._merge(o, lambda lo, hi, p, q: [(lo, hi, p[0] - q[0], p[1] - q[1])])

    def __rsub__(self, o):
        return self._lift(o) - self

    def __neg__(self):
        return PW([(lo, hi, -a, -b) for lo, hi, a, b in self.segs], self.name)

    def __pos__(self):
        return self

    def is_const(self):
        return all(abs(b) < EPS for *_, b in self.segs) and len({round(a, 9) for _, _, a, _ in self.segs}) == 1

    def _scale(self, k):
        return PW([(lo, hi, a * k, b * k) for lo, hi, a, b in self.segs], self.name)

    def __mul__(self, o):
        if isinstance(o, PW):
            if o.is_const():
                return self._scale(o.segs[0][2])
            if self.is_const():
                return o._scale(self.segs[0][2])
            raise ValueError(f"product of two expressions in symbol {self.name}")
        return self._scale(o)
    __rmul__ = __mul__

    def __truediv__(self, o):
        if isinstance(o, PW):
            if not o.is_const():
                raise ValueError(f"division by an expression in symbol {self.name}")
            o = o.segs[0][2]
        return self._scale(1.0 / o)

    def _pick(self, o, take_max):
        def fn(lo, hi, p, q):
            pts = [lo]
            if abs(p[1] - q[1]) > EPS:
                x = (q[0] - p[0]) / (p[1] - q[1])
                if lo + EPS < x < hi - EPS:
                    pts.append(x)
            pts.append(hi)
            seg = []
            for a, b in zip(pts, pts[1:]):
                m = a + 1.0 if b == INF else (a + b) / 2
                vp, vq = p[0] + p[1] * m, q[0] + q[1] * m
                use = p if (vp >= vq) == take_max else q
                seg.append((a, b, use[0], use[1]))
            return seg
        return self._merge(o, fn)

    def __abs__(self):
        return self._pick(-self, True)

    def at(self, s):
        return next(a + b * s for s0, s1, a, b in self.segs if s0 <= s <= s1)

    def describe(self, nd=2):
        def line(a, b):
            if abs(b) < EPS:
                return f"{a:.{nd}f}"
            t = self.name if abs(b - 1) < EPS else f"{b:g} {self.name}"
            return t if abs(a) < EPS else f"{a:.{nd}f} + {t}" if a > 0 else f"{t} - {-a:.{nd}f}"
        parts = []
        for lo, hi, a, b in self.segs:
            rng = f"{self.name} >= {lo:g}" if hi == INF else f"{lo:g} <= {self.name} <= {hi:.{nd}f}"
            parts.append(f"{line(a, b)} for {rng}")
        return "; ".join(parts)

    def first_const(self):
        """(value, s_hi) when the PW is constant on its first segment, else None."""
        lo, hi, a, b = self.segs[0]
        return (a, hi) if abs(b) < EPS else None

    def __repr__(self):
        return f"PW({self.describe()})"


def pmax(*xs):
    xs = list(xs[0]) if len(xs) == 1 and not isinstance(xs[0], (int, float, PW)) else list(xs)
    out = xs[0]
    for x in xs[1:]:
        if isinstance(out, PW) or isinstance(x, PW):
            out = (out if isinstance(out, PW) else x._lift(out))._pick(x, True)
        else:
            out = max(out, x)
    return out


def pmin(*xs):
    xs = list(xs[0]) if len(xs) == 1 and not isinstance(xs[0], (int, float, PW)) else list(xs)
    out = xs[0]
    for x in xs[1:]:
        if isinstance(out, PW) or isinstance(x, PW):
            out = (out if isinstance(out, PW) else x._lift(out))._pick(x, False)
        else:
            out = min(out, x)
    return out


def pabs(x):
    return abs(x)


def symbol_names(spec):
    """Spec `symbols`: {name: {domain: [lo, null], ...}}. Each becomes a PW identity on its domain."""
    out = {}
    for name, d in ((spec or {}).get("symbols") or {}).items():
        lo = ((d or {}).get("domain") or [0])[0]
        out[name] = PW.sym(name, float(lo))
    return out


def numeric(x, what="value", validity=None):
    """A drawn or checked number. A PW is accepted only when constant on its first segment (the domain lower bound up to
    the first breakpoint); the upper end of that segment goes into validity[what]. Else ValueError: the drawn value would
    depend on a symbol that has no value."""
    if not isinstance(x, PW):
        return x
    fc = x.first_const()
    if fc is None:
        raise ValueError(f"{what} depends on symbol {x.name} ({x.describe()}); a drawn value needs it constant")
    if validity is not None:
        validity[what] = min(validity.get(what, INF), fc[1])
    return fc[0]


def report_value(x):
    """Reported value: a number, or for a PW its value on the first segment when constant there (the range is listed with
    it under symbol_terms), else the expression string."""
    if isinstance(x, PW):
        fc = x.first_const()
        return fc[0] if fc is not None else x.describe()
    return x


FUNCS = {"min": pmin, "max": pmax, "abs": pabs, "sind": sind, "cosd": cosd, "sqrt": math.sqrt}


# ---------------------------------------------------------------- frames

def to_shop_floor(z_A, P):
    """z_A -> z_S. The only conversion into the plotting frame."""
    return z_A + P.get("jig.datum_a_above_floor")


def from_shop_floor(z_S, P):
    """z_S -> z_A. The only conversion out of the plotting frame (inverse of to_shop_floor; LF-12)."""
    return z_S - P.get("jig.datum_a_above_floor")


def receiver_to_datum_a(z_R, P):
    """z_R (ASSEMBLY.md floor frame, receiver floor) -> z_A."""
    return z_R + P.get("icd.floor_above_datum_a")


# ---------------------------------------------------------------- stack terms (z_A)

def collar_top_z_A(P):
    """test_P18_collar_top_recomputed_from_params (tests/test_params_bom.py 694-702), nut plate 8 written from params:
    nut.plate_thickness 7.5 + washer proud (washer.thickness 1.3 - nut.washer_pocket_depth 0.8) = 8."""
    g = P.get
    drop = g("holder.stroke_gap_R") - g("witness.zone_high")
    nut_plate = g("nut.plate_thickness") + g("washer.thickness") - g("nut.washer_pocket_depth")
    top_R = g("seat.holder_bottom_R") - drop + g("holder.length") + g("holder.flange_thickness") + nut_plate + g("collar.top_above_plate")
    return receiver_to_datum_a(top_R, P)


def core_stop_z_A(P):
    """Collet core stop: overlay leaf collet.core_stop_z (G4, ASSUMED). Without the leaf (older overlays), the receiver
    floor plus collet.core_seat_height. LF-16 lints it against the drawn core_seat edge."""
    if P.has("collet.core_stop_z"):
        return P.get("collet.core_stop_z")
    return receiver_to_datum_a(P.get("collet.core_seat_height"), P)


DEFAULT_LOAD_PLANE = {"term": "core_stop", "feature": "core_seat", "edge": "z_max", "offset": 0}
PLANE_FIELDS = ("load_plane", "entry_plane")


def load_plane(spec, field="load_plane"):
    """A named plane of the spec (LF-6). load_plane: the plane the core stands on, read by S1-3 (G1, core stop).
    entry_plane: the plane the core bottom passes over while it enters the holder, read by the park rule
    (gameplan Design Notes 22, collar top). Without entry_plane the park rule reads load_plane (1.0 behaviour)."""
    lp = dict(DEFAULT_LOAD_PLANE)
    src = spec.get(field) or (spec.get("load_plane") if field == "entry_plane" else None) or {}
    lp.update(src)
    return lp


def park_lengths(P, spec, q9_keys):
    """Core lengths the park must clear: the Q9 list plus spec always_loaded (G2: the 0.75 m install core is the
    capture core, so it is loaded under every Q9 option)."""
    keys = list(q9_keys) + [k for k in spec.get("always_loaded", []) if k not in q9_keys]
    return keys


def _class_names(spec, names, L):
    nm = dict(names or {})
    for k, v in symbol_names(spec).items():
        nm.setdefault(k, v)
    nm["L"] = L
    return nm


def class_starts_z_A(P, spec, q9_keys, names=None, symbolic=False, validity=None):
    """Start tip per supported core class. spec park_rule.stop_k and start_k are expressions in L (core length) and
    stop_k (option R, gameplan Design Notes 22); without park_rule, params stop.start_z (1.0 behaviour). A spec symbol
    (H5: the 1 m clearance c) makes a class value a PW; symbolic=False returns numeric() values (ValueError where a
    class depends on the symbol), symbolic=True the PW."""
    pr = spec.get("park_rule")
    if not pr:
        return {"params stop.start_z": max(P.get("stop.start_z"))}
    out = {}
    for k in park_lengths(P, spec, q9_keys):
        nm = _class_names(spec, names, P.get(k))
        nm["stop_k"] = eval_expr(pr["stop_k"], P, nm)
        v = eval_expr(pr["start_k"], P, nm)
        out[k] = v if symbolic else numeric(v, f"start {k}", validity)
    return out


def class_stops_z_A(P, spec, q9_keys, names=None, symbolic=False, validity=None):
    pr = spec.get("park_rule")
    if not pr:
        return {"params stop.height_range": max(P.get("stop.height_range"))}
    out = {}
    for k in park_lengths(P, spec, q9_keys):
        v = eval_expr(pr["stop_k"], P, _class_names(spec, names, P.get(k)))
        out[k] = v if symbolic else numeric(v, f"stop {k}", validity)
    return out


def park_tip_z_A(P, q9_keys, plane_z_A, spec=None, names=None, symbolic=False, validity=None):
    """Park rule (S1-2, S1-3): the cutter tip clears the highest start pose of the supported classes and the tallest
    loaded core standing on the plane by upper.load_clearance. spec None: 1.0 draft (max params stop.start_z)."""
    spec = spec or {}
    lengths = park_lengths(P, spec, q9_keys)
    tallest = plane_z_A + max(P.get(k) for k in lengths)
    start = pmax(class_starts_z_A(P, spec, q9_keys, names, symbolic=True).values())
    v = pmax(start, tallest) + P.get("upper.load_clearance")
    return v if symbolic else numeric(v, "park", validity)


def screw_block_g_min(spec, s):
    """K7 g_min of the nut housing against the anchor and the guide block of screw s (spec neighbours of row
    nut_housing_<s>, g_min seed l.148). Read by S1-4 and the screw_length expressions (FIX 2, Loftsman 1.1 (b)).
    Returns (anchor g_min, guide g_min); KeyError when the spec declares neither pair."""
    row = next((r for r in spec.get("features", []) if r.get("id") == f"nut_housing_{s}"), None)
    nbs = {nb.get("id"): nb for nb in ((row or {}).get("neighbours") or [])}
    try:
        return nbs[f"anchor_{s}"]["g_min"], nbs[f"guide_{s}"]["g_min"]
    except KeyError:
        raise KeyError(f"spec declares no nut_housing_{s}|anchor_{s} and |guide_{s} g_min")


def global_vars(P, spec):
    g = P.get
    q9 = spec.get("q9_length_keys", DEFAULT_Q9)
    lowest = min(g("stop.height_z"), min(g("stop.height_range")))
    validity = {}
    if spec.get("park_rule"):
        lowest = numeric(pmin(class_stops_z_A(P, spec, q9, {}, symbolic=True).values()), "lowest stop", validity)
    receiver_floor = receiver_to_datum_a(0, P)
    drop = g("holder.stroke_gap_R") - g("witness.zone_high")
    out = {
        "shop_floor": from_shop_floor(0, P),
        "receiver_floor": receiver_floor,
        "collar_top": collar_top_z_A(P),
        "holder_bottom": receiver_floor + g("seat.holder_bottom_R") - drop,
        "core_stop": core_stop_z_A(P),
        "capture_end_tip": g("stop.height_z"),
        "lowest_tip": lowest,
        "ring_bottom_low": lowest + g("ring.position_above_tip"),
        "height_target_z_A": from_shop_floor(g("jig.height_target"), P),
    }
    if P.has("jackscrew.top_guide_z"):   # 1.3 step 0 R2 (Loftsman 1.2 (b) NOTE 2): member-top stack_ties term, z_A
        out["top_guide"] = g("jackscrew.top_guide_z")
    out["load_plane"] = out[load_plane(spec)["term"]]
    out["entry_plane"] = out[load_plane(spec, "entry_plane")["term"]]
    out["park_tip"] = park_tip_z_A(P, q9, out["entry_plane"], spec, out, validity=validity)
    out["start_tip_max"] = numeric(pmax(class_starts_z_A(P, spec, q9, out, symbolic=True).values()), "start max", validity)
    out["lift_stroke"] = out["park_tip"] - lowest
    if validity:   # H5: drawn values constant in every spec symbol up to these bounds (reported, no threshold)
        out["_symbol_validity"] = validity
    return out


def pose_vars(P, tip):
    g = P.get
    ring_bottom = tip + g("ring.position_above_tip")
    ring_top = ring_bottom + g("ring.thickness")
    drill_top = tip + g("drill.length")
    return {
        "tip": tip,
        "head_top": tip + g("drill.head_length"),
        "drill_top": drill_top,
        "top_block_top": drill_top + g("drill.top_block_length"),
        "bore_ceiling": tip + g("drill.bore_ceiling_above_tip"),
        "ring_bottom": ring_bottom,
        "ring_top": ring_top,
        "nut_z": ring_bottom + g("ring.thickness") / 2,
        "gear_top": ring_top + g("gear.face_width"),
    }


# ---------------------------------------------------------------- expression evaluator

def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_dotted(node.value)}.{node.attr}"
    raise ValueError("bad key expression")


def eval_expr(expr, P, names):
    """Arithmetic over stack names, dotted params/overlay keys (k.sub[0]) and min/max/abs/sind/cosd."""
    if isinstance(expr, (int, float)):
        return float(expr)
    tree = ast.parse(str(expr), mode="eval")

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.Name):
            if n.id in names:
                return names[n.id]
            raise KeyError(f"unknown stack name {n.id!r} in {expr!r}")
        if isinstance(n, ast.Attribute):
            return P.get(_dotted(n))
        if isinstance(n, ast.Subscript):
            return ev(n.value)[int(ev(n.slice))]
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            ops = {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a * b, ast.Div: lambda: a / b}
            return ops[type(n.op)]()
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FUNCS:
            return FUNCS[n.func.id](*[ev(a) for a in n.args])
        raise ValueError(f"unsupported expression node {type(n).__name__} in {expr!r}")
    v = ev(tree)
    if isinstance(v, PW):
        return v.segs[0][2] if v.is_const() else v
    return float(v)


# ---------------------------------------------------------------- spec evaluation

def applies(row, pose_id):
    return not row.get("poses") or pose_id in row["poses"]


def radial_corners(r_in, r_out, theta, w, rot=0):
    """Plan corners (x, y) of a radial footprint: rectangle from r_in to r_out along the radial direction at theta,
    half-width w across it, turned by rot (deg, counter-clockwise) about its own centre (r4: rot 0 is one face toward
    the axis; the LF1.1-8 control turns the 30-6060 member square 45 deg)."""
    s, c = sind(theta), cosd(theta)
    uc = (r_in + r_out) / 2
    sr, cr = sind(rot), cosd(rot)
    out = []
    for u, v in ((r_in, -w), (r_out, -w), (r_out, w), (r_in, w)):
        du, dv = u - uc, v
        u2, v2 = uc + du * cr - dv * sr, du * sr + dv * cr
        out.append((u2 * c - v2 * s, u2 * s + v2 * c))
    return out


def place_extents(r_in, r_out, theta, w, footprint, rot=0):
    """Plan footprint of a placed part projected on X (side-view x extent) and Y (side-view depth band).
    round: circle of radius w at every radius from r_in to r_out (axis-Z parts).
    radial: rectangle along the radial direction from r_in to r_out, half-width w across it (radial-axis parts; LF-5, TP-4):
      y in [min(r_in s, r_out s) - w|c|, max(r_in s, r_out s) + w|c|], x in [min(r_in c, r_out c) - w|s|, max(...) + w|s|]."""
    s, c = sind(theta), cosd(theta)
    if footprint == "radial":
        pts = radial_corners(r_in, r_out, theta, w, rot)
        x = [min(p[0] for p in pts), max(p[0] for p in pts)]
        y = [min(p[1] for p in pts), max(p[1] for p in pts)]
    elif footprint == "round":
        x = [min(r_in * c, r_out * c) - w, max(r_in * c, r_out * c) + w]
        y = [min(r_in * s, r_out * s) - w, max(r_in * s, r_out * s) + w]
    else:
        raise ValueError(f"unknown footprint {footprint!r}")
    return x, y, (r_in + r_out) / 2


def strip_corners(a, b, w):
    """Plan corners of a strip of half-width w from point a to point b (S2 guide ties: rod top to frame member)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    if L < EPS:
        raise ValueError("plan strip of zero length")
    nx, ny = -dy / L * w, dx / L * w
    return [(a[0] - nx, a[1] - ny), (b[0] - nx, b[1] - ny), (b[0] + nx, b[1] + ny), (a[0] + nx, a[1] + ny)]


def plan_poly_pieces(row, P, names):
    """Spec field plan_poly (1.2 (b), plan rows with no radial or round footprint: base plate less the column notches,
    base frame members, plate holes, slot lines, guide ties). A list of convex pieces; each piece is a list of [x, y]
    expression pairs (two points: a segment) or {strip: {from: [x, y], to: [x, y], half_width: e}}. A strip may also
    carry `back: e` (start e behind `from` along the axis u = unit(to - from)) and `stop_at: [x, y]` (end at the station
    of that point on the axis, u . (point - from); `to` then sets the direction only). 1.2 (b) Designer FIX 1: the guide
    tie runs 30 past the rod centre and ends at the member's near corner. Returns the pieces as lists of (x, y) in plan,
    mm."""
    out = []
    for pc in row.get("plan_poly") or []:
        if isinstance(pc, dict) and "strip" in pc:
            st = pc["strip"]
            a = tuple(eval_expr(e, P, names) for e in st["from"])
            b = tuple(eval_expr(e, P, names) for e in st["to"])
            if "back" in st or "stop_at" in st:
                L = math.hypot(b[0] - a[0], b[1] - a[1])
                if L < EPS:
                    raise ValueError("plan strip direction of zero length")
                u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
                s0 = -eval_expr(st.get("back", 0), P, names)
                if "stop_at" in st:
                    k = tuple(eval_expr(e, P, names) for e in st["stop_at"])
                    s1 = u[0] * (k[0] - a[0]) + u[1] * (k[1] - a[1])
                else:
                    s1 = L
                a, b = (a[0] + s0 * u[0], a[1] + s0 * u[1]), (a[0] + s1 * u[0], a[1] + s1 * u[1])
            out.append(strip_corners(a, b, eval_expr(st["half_width"], P, names)))
        else:
            out.append([tuple(eval_expr(e, P, names) for e in pt) for pt in pc])
    return out


def sector_record(sec, P, names):
    """Spec field sector (S2 operator sector): apex on the axis, theta and half_angle in deg, radius r. Returns the
    values and the plan x, y extents of the wedge."""
    th, ha, r = (eval_expr(sec[k], P, names) for k in ("theta", "half_angle", "r"))
    angs = [th - ha, th + ha] + [a for a in range(-720, 721, 90) if th - ha < a < th + ha]
    pts = [(0.0, 0.0)] + [(r * cosd(a), r * sind(a)) for a in angs]
    return {"theta": th, "half_angle": ha, "r": r, "x": [min(p[0] for p in pts), max(p[0] for p in pts)],
            "y": [min(p[1] for p in pts), max(p[1] for p in pts)]}


def evaluate_spec(P, spec):
    """Per pose: tip, stack names (z_A), and per feature z_min/z_max in z_S, the placement and the depth band.
    depth: the spec band when given, hulled with the placed projection when the row also has `place`; else the placed
    projection. depth_spec and depth_true are kept for the K7 band lint."""
    glob = global_vars(P, spec)
    out = {"frame": "z_S", "z_rule_frame": "z_A", "global_z_A": glob, "poses": {}}
    for pose in spec.get("poses", []):
        pid = pose["id"]
        tip = eval_expr(pose.get("tip_z", 0), P, glob)
        names = dict(glob)
        names.update(pose_vars(P, tip))
        for k, v in (pose.get("vars") or {}).items():   # per-pose stack names (TP-9: core position per pose)
            names[k] = eval_expr(v, P, names)
        feats = {}
        for row in spec.get("features", []):
            if not applies(row, pid):
                continue
            rec = {}
            zr = row.get("z_rule")
            if zr:
                rec["z_min"] = to_shop_floor(eval_expr(zr["z_min"], P, names), P)
                rec["z_max"] = to_shop_floor(eval_expr(zr["z_max"], P, names), P)
            pl = row.get("place")
            if pl:
                r_in = eval_expr(pl["r_in"], P, names)
                r_out = eval_expr(pl.get("r_out", pl["r_in"]), P, names)
                th = eval_expr(pl["theta"], P, names)
                w = eval_expr(pl["half_width"], P, names)
                rot = eval_expr(pl.get("rot", 0), P, names)
                x, y, rc = place_extents(r_in, r_out, th, w, pl.get("footprint", "round"), rot)
                rec["place"] = {"r_c": rc, "theta": th, "x": x, "y": y, "r_in": r_in, "r_out": r_out, "half_width": w,
                                "footprint": pl.get("footprint", "round"), "rot": rot}
                rec["depth_true"] = y
            if row.get("plan_poly"):
                pcs = plan_poly_pieces(row, P, names)
                rec["plan_pieces"] = pcs
                rec["plan_x"] = [min(p[0] for pc in pcs for p in pc), max(p[0] for pc in pcs for p in pc)]
                rec["plan_y"] = [min(p[1] for pc in pcs for p in pc), max(p[1] for pc in pcs for p in pc)]
            if row.get("sector"):
                rec["sector"] = sector_record(row["sector"], P, names)
            if row.get("depth") is not None:
                rec["depth"] = sorted(eval_expr(d, P, names) for d in row["depth"])
                if pl:
                    rec["depth_spec"] = rec["depth"]
                    rec["depth"] = [min(rec["depth"][0], y[0]), max(rec["depth"][1], y[1])]
            elif pl:
                rec["depth"] = list(y)
            elif row.get("plan_poly"):   # 1.2 (b): side-view depth band of a plan_poly row (S1 r5 guide ties) = its plan y extent
                rec["depth"] = list(rec["plan_y"])
            feats[row["id"]] = rec
        out["poses"][pid] = {"tip_z_A": tip, "tip_z_S": to_shop_floor(tip, P), "vars_z_A": names, "features": feats}
    return out


def _try_block_g_min(spec, s):
    try:
        return list(screw_block_g_min(spec, s))
    except KeyError:
        return []


def reported(P, spec, stack):
    """Reported values (no threshold, gameplan l.116): highest point and margin to the soft target per pose, lift stroke."""
    glob = stack["global_z_A"]
    lp = load_plane(spec)
    rep = {"lift_stroke_mm": glob["lift_stroke"],
           "park_tip_z_A": glob["park_tip"], "start_tip_max_z_A": glob["start_tip_max"],
           "collar_top_recomputed_z_A": glob["collar_top"],
           "collar_top_params_z_A": P.get("stop.collar_top_z"),
           "load_plane": lp["term"], "entry_plane": load_plane(spec, "entry_plane")["term"], "poses": {}}
    # LF-6: park tip per plane and per core length (no threshold)
    lengths = [k for k in ("core.length_capture", "core.length_install", "core.length_optional") if P.has(k)]
    rep["park_tip_by_plane_z_A"] = {term: {k: report_value(park_tip_z_A(P, [k], glob[term], spec, glob, symbolic=True)) for k in lengths} for term in ("core_stop", "collar_top")}
    # Q9 options (gameplan detail 1.1 Reported): park, stroke and screw length per option; no threshold
    opts = {}
    for name, keys in (spec.get("q9_options") or {}).items():
        keys = [k for k in keys if P.has(k)]
        park = park_tip_z_A(P, keys, glob["entry_plane"], spec, glob, symbolic=True)
        low = pmin(class_stops_z_A(P, spec, keys, glob, symbolic=True).values()) if spec.get("park_rule") else glob["lowest_tip"]
        nm = dict(glob)
        nm.update({"park": park, "stroke": park - low})
        gm = [g for s in ("a", "b") for g in _try_block_g_min(spec, s)]
        if gm:
            nm["g_min_screw_block"] = max(gm)
        Ls = {lk: eval_expr(ex, P, nm) for lk, ex in (spec.get("screw_length") or {}).items()}
        starts = class_starts_z_A(P, spec, keys, glob, symbolic=True)
        stops = class_stops_z_A(P, spec, keys, glob, symbolic=True) if spec.get("park_rule") else {}
        # FIX 5 (Loftsman 1.1 (b)), reported only: start tip minus the top of that class's core on the core stop.
        # Negative = the cutter starts inside the uncut core. H5: with the start-above-core term it reads c (1 m class).
        over = {k: v - (glob["core_stop"] + P.get(k)) for k, v in starts.items() if P.has(k)}
        rv = report_value
        o = {"lengths": keys, "stops_z_A": {k: rv(v) for k, v in stops.items()}, "starts_z_A": {k: rv(v) for k, v in starts.items()},
             "park_tip_z_A": rv(park), "lowest_stop_z_A": rv(low), "lift_stroke": rv(park - low),
             "L": {k: rv(v) for k, v in Ls.items()}, "start_minus_core_top": {k: rv(v) for k, v in over.items()}}
        # H5: every value that reads a spec symbol is also listed as its full expression with the ranges it holds for.
        terms = [("park", park), ("lowest stop", low), ("lift stroke", park - low), *[(f"L {k}", v) for k, v in Ls.items()],
                 *[(f"stop {k}", v) for k, v in stops.items()], *[(f"start {k}", v) for k, v in starts.items()],
                 *[(f"start_minus_core_top {k}", v) for k, v in over.items()]]
        sym = {lab: v.describe() for lab, v in terms if isinstance(v, PW)}
        if sym:
            o["symbol_terms"] = sym
        opts[name] = o
    rep["q9_options"] = opts
    if glob.get("_symbol_validity"):
        rep["drawn_symbol_validity"] = {k: (v if v != INF else "every value") for k, v in glob["_symbol_validity"].items()}
    # LF-7 / G2: start pose against the capture core on the core stop (no threshold)
    ck = spec.get("capture_core_length", "core.length_capture")
    core_top = glob["core_stop"] + P.get(ck)
    rep["capture_core_length_key"] = ck
    # LF1.1-3 (r2): the capture class start from the park rule, not params stop.start_z (which Step 4 rewrites)
    start_ck = class_starts_z_A(P, spec, [ck], glob).get(ck, max(class_starts_z_A(P, spec, [ck], glob).values()))
    rep["start_tip_minus_core_top_mm"] = start_ck - core_top
    # LF1.1-2 (r2): the governing park term, reported with no threshold: park - load_clearance - (entry plane + max L)
    lengths_park = park_lengths(P, spec, spec.get("q9_length_keys", DEFAULT_Q9))
    rep["entry_plane_margin_mm"] = glob["park_tip"] - P.get("upper.load_clearance") - (glob["entry_plane"] + max(P.get(k) for k in lengths_park))
    rep["end_tip_plus_advance_z_A"] = glob["capture_end_tip"] + P.get("upper.drill_advance_500core")
    rep["core_top_on_core_stop_z_A"] = core_top
    ref = [r["id"] for r in spec.get("features", []) if r.get("reference")]
    for pid, pr in stack["poses"].items():
        tops = [pr["features"][k]["z_max"] for k in pr["features"] if k not in ref and "z_max" in pr["features"][k]]
        hi = max(tops) if tops else None
        rep["poses"][pid] = {"highest_z_S": hi, "margin_to_soft_target": (P.get("jig.height_target") - hi) if hi is not None else None}
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("spec", nargs="?", default=str(HERE / "s1_spec.yaml"))
    ap.add_argument("--params")
    ap.add_argument("--overlay")
    a = ap.parse_args(argv)
    P = sketch_loader.Params(a.params, a.overlay)
    spec = sketch_loader.load_spec(a.spec)
    stack = evaluate_spec(P, spec)
    print(json.dumps({"stack": stack, "reported": reported(P, spec, stack)}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
