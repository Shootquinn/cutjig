"""Pure-python glyph reading and frame member-name parsing (no FreeCAD import): used by probe_step6_marks.py and by the pytest controls.
Input: void sample points (x, y, z) of one recessed glyph on a nut wing face. Output: principal-axis span, tail-to-head direction,
sense seen from +Z (+1 counter-clockwise, -1 clockwise) and the point count. The head is the end of the principal axis with the larger
perpendicular spread (arrowhead wider than the shaft)."""
import math


def _axis(pts):
    n = len(pts)
    c = [sum(p[i] for p in pts) / n for i in range(3)]
    d = [[p[i] - c[i] for i in range(3)] for p in pts]
    cov = [[sum(q[i] * q[j] for q in d) / n for j in range(3)] for i in range(3)]
    v = [1.0, 0.3, 0.1]
    for _ in range(60):
        w = [sum(cov[i][j] * v[j] for j in range(3)) for i in range(3)]
        m = math.sqrt(sum(x * x for x in w)) or 1.0
        v = [x / m for x in w]
    return c, v, d


def analyze(pts):
    if len(pts) < 3:
        return {"count": len(pts), "span": 0.0, "direction_sign": 0}
    c, v, d = _axis(pts)
    t = [sum(q[i] * v[i] for i in range(3)) for q in d]
    perp = [math.sqrt(max(sum(q[i] ** 2 for i in range(3)) - ti * ti, 0.0)) for q, ti in zip(d, t)]
    lo, hi = min(t), max(t)
    third = (hi - lo) / 3.0
    tail = [p for p, ti in zip(perp, t) if ti <= lo + third]
    head = [p for p, ti in zip(perp, t) if ti >= hi - third]
    s = 1.0 if (sum(head) / max(len(head), 1)) >= (sum(tail) / max(len(tail), 1)) else -1.0
    dx, dy = s * v[0], s * v[1]
    z_cross = c[0] * dy - c[1] * dx            # z component of r x d about the Z axis, centroid r
    return {"count": len(pts), "span": hi - lo, "direction_sign": 1 if z_cross > 0 else -1 if z_cross < 0 else 0,
            "centroid": c, "direction": [s * x for x in v]}


def synthetic_arrow(x_tail, x_head, y_face, half_shaft=1.0, half_head=3.0, head_len=5.0, step=0.5):
    """Recess on a y-normal wing face: shaft plus wider head, points at (x, y_face, z). Control fixture."""
    pts, sgn = [], 1.0 if x_head > x_tail else -1.0
    n = int(abs(x_head - x_tail) / step)
    for i in range(n + 1):
        x = x_tail + sgn * i * step
        hw = half_head * (1 - (abs(x_head - x) / head_len)) if abs(x_head - x) <= head_len else half_shaft
        k = int(max(hw, half_shaft) / step)
        pts += [(x, y_face, j * step) for j in range(-k, k + 1)]
    return pts


def member_id(name):
    """Frame object name member_<id>_<n> -> <id>; ids may hold underscores (plate_support)."""
    return name[len("member_"):].rsplit("_", 1)[0]
