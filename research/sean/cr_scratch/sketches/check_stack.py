"""Pose stack arithmetic for the sketches, from params.yaml and the overlay only.

Frames (FRAME RULING, gameplan Design Notes 17):
  z_A  datum A = base-plate underside = frame top plane. params stop.*, upper.park_z, stop.collar_top_z are z_A.
  z_R  receiver floor (ASSEMBLY.md "floor frame"): z_R = z_A - icd.floor_above_datum_a.
  z_S  shop floor, the frame the sketches plot in: z_S = z_A + jig.datum_a_above_floor.
Every spec z_rule is evaluated in z_A; to_shop_floor() is the one z_A -> z_S conversion.

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


FUNCS = {"min": min, "max": max, "abs": abs, "sind": sind, "cosd": cosd}


# ---------------------------------------------------------------- frames

def to_shop_floor(z_A, P):
    """z_A -> z_S. The only conversion into the plotting frame."""
    return z_A + P.get("jig.datum_a_above_floor")


def shop_floor_in_z_A(P):
    """The shop floor plane (z_S = 0) expressed in z_A; inverse of to_shop_floor at z_S = 0."""
    return -P.get("jig.datum_a_above_floor")


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
    """Collet core seat top. ASSUMED: collet foot on the receiver floor, seat at collet.core_seat_height above it."""
    return receiver_to_datum_a(P.get("collet.core_seat_height"), P)


def park_tip_z_A(P, q9_keys):
    """DRAFT re-derived park rule (S1-2, S1-3; 1.1 signs it): the cutter tip clears the highest start pose and the
    tallest supported core by upper.load_clearance."""
    tallest = core_stop_z_A(P) + max(P.get(k) for k in q9_keys)
    return max(max(P.get("stop.start_z")), tallest) + P.get("upper.load_clearance")


def global_vars(P, spec):
    g = P.get
    q9 = spec.get("q9_length_keys", DEFAULT_Q9)
    park = park_tip_z_A(P, q9)
    lowest = min(g("stop.height_z"), min(g("stop.height_range")))
    receiver_floor = receiver_to_datum_a(0, P)
    drop = g("holder.stroke_gap_R") - g("witness.zone_high")
    return {
        "shop_floor": shop_floor_in_z_A(P),
        "receiver_floor": receiver_floor,
        "collar_top": collar_top_z_A(P),
        "holder_bottom": receiver_floor + g("seat.holder_bottom_R") - drop,
        "core_stop": core_stop_z_A(P),
        "park_tip": park,
        "start_tip_max": max(g("stop.start_z")),
        "capture_end_tip": g("stop.height_z"),
        "lowest_tip": lowest,
        "lift_stroke": park - lowest,
        "ring_bottom_low": lowest + g("ring.position_above_tip"),
        "height_target_z_A": g("jig.height_target") - g("jig.datum_a_above_floor"),
    }


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
    return float(ev(tree))


# ---------------------------------------------------------------- spec evaluation

def applies(row, pose_id):
    return not row.get("poses") or pose_id in row["poses"]


def evaluate_spec(P, spec):
    """Per pose: tip, stack names (z_A), and per feature z_min/z_max in z_S and the depth band (view-direction mm)."""
    glob = global_vars(P, spec)
    out = {"frame": "z_S", "z_rule_frame": "z_A", "global_z_A": glob, "poses": {}}
    for pose in spec.get("poses", []):
        pid = pose["id"]
        tip = eval_expr(pose.get("tip_z", 0), P, glob)
        names = dict(glob)
        names.update(pose_vars(P, tip))
        feats = {}
        for row in spec.get("features", []):
            if not applies(row, pid):
                continue
            rec = {}
            zr = row.get("z_rule")
            if zr:
                rec["z_min"] = to_shop_floor(eval_expr(zr["z_min"], P, names), P)
                rec["z_max"] = to_shop_floor(eval_expr(zr["z_max"], P, names), P)
            if row.get("depth") is not None:
                rec["depth"] = sorted(eval_expr(d, P, names) for d in row["depth"])
            feats[row["id"]] = rec
        out["poses"][pid] = {"tip_z_A": tip, "tip_z_S": to_shop_floor(tip, P), "vars_z_A": names, "features": feats}
    return out


def reported(P, spec, stack):
    """Reported values (no threshold, gameplan l.116): highest point and margin to the soft target per pose, lift stroke."""
    rep = {"lift_stroke_mm": stack["global_z_A"]["lift_stroke"],
           "collar_top_recomputed_z_A": stack["global_z_A"]["collar_top"],
           "collar_top_params_z_A": P.get("stop.collar_top_z"), "poses": {}}
    for pid, pr in stack["poses"].items():
        ref =[r["id"] for r in spec.get("features", []) if r.get("reference")]
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
    spec = sketch_loader.load_yaml(a.spec)
    stack = evaluate_spec(P, spec)
    print(json.dumps({"stack": stack, "reported": reported(P, spec, stack)}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
