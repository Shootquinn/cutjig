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


FUNCS = {"min": min, "max": max, "abs": abs, "sind": sind, "cosd": cosd, "sqrt": math.sqrt}


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


def class_starts_z_A(P, spec, q9_keys, names=None):
    """Start tip per supported core class. spec park_rule.stop_k and start_k are expressions in L (core length) and
    stop_k (option R, gameplan Design Notes 22); without park_rule, params stop.start_z (1.0 behaviour)."""
    pr = spec.get("park_rule")
    if not pr:
        return {"params stop.start_z": max(P.get("stop.start_z"))}
    out = {}
    for k in park_lengths(P, spec, q9_keys):
        nm = dict(names or {})
        nm["L"] = P.get(k)
        nm["stop_k"] = eval_expr(pr["stop_k"], P, nm)
        out[k] = eval_expr(pr["start_k"], P, nm)
    return out


def class_stops_z_A(P, spec, q9_keys, names=None):
    pr = spec.get("park_rule")
    if not pr:
        return {"params stop.height_range": max(P.get("stop.height_range"))}
    out = {}
    for k in park_lengths(P, spec, q9_keys):
        nm = dict(names or {})
        nm["L"] = P.get(k)
        out[k] = eval_expr(pr["stop_k"], P, nm)
    return out


def park_tip_z_A(P, q9_keys, plane_z_A, spec=None, names=None):
    """Park rule (S1-2, S1-3): the cutter tip clears the highest start pose of the supported classes and the tallest
    loaded core standing on the plane by upper.load_clearance. spec None: 1.0 draft (max params stop.start_z)."""
    spec = spec or {}
    lengths = park_lengths(P, spec, q9_keys)
    tallest = plane_z_A + max(P.get(k) for k in lengths)
    start = max(class_starts_z_A(P, spec, q9_keys, names).values())
    return max(start, tallest) + P.get("upper.load_clearance")


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
    if spec.get("park_rule"):
        lowest = min(class_stops_z_A(P, spec, q9, {}).values())
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
    out["load_plane"] = out[load_plane(spec)["term"]]
    out["entry_plane"] = out[load_plane(spec, "entry_plane")["term"]]
    out["park_tip"] = park_tip_z_A(P, q9, out["entry_plane"], spec, out)
    out["start_tip_max"] = max(class_starts_z_A(P, spec, q9, out).values())
    out["lift_stroke"] = out["park_tip"] - lowest
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
    return float(ev(tree))


# ---------------------------------------------------------------- spec evaluation

def applies(row, pose_id):
    return not row.get("poses") or pose_id in row["poses"]


def place_extents(r_in, r_out, theta, w, footprint):
    """Plan footprint of a placed part projected on X (side-view x extent) and Y (side-view depth band).
    round: circle of radius w at every radius from r_in to r_out (axis-Z parts).
    radial: rectangle along the radial direction from r_in to r_out, half-width w across it (radial-axis parts; LF-5, TP-4):
      y in [min(r_in s, r_out s) - w|c|, max(r_in s, r_out s) + w|c|], x in [min(r_in c, r_out c) - w|s|, max(...) + w|s|]."""
    s, c = sind(theta), cosd(theta)
    if footprint == "radial":
        x = [min(r_in * c, r_out * c) - w * abs(s), max(r_in * c, r_out * c) + w * abs(s)]
        y = [min(r_in * s, r_out * s) - w * abs(c), max(r_in * s, r_out * s) + w * abs(c)]
    elif footprint == "round":
        x = [min(r_in * c, r_out * c) - w, max(r_in * c, r_out * c) + w]
        y = [min(r_in * s, r_out * s) - w, max(r_in * s, r_out * s) + w]
    else:
        raise ValueError(f"unknown footprint {footprint!r}")
    return x, y, (r_in + r_out) / 2


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
                x, y, rc = place_extents(r_in, r_out, th, w, pl.get("footprint", "round"))
                rec["place"] = {"r_c": rc, "theta": th, "x": x, "y": y, "r_in": r_in, "r_out": r_out, "half_width": w,
                                "footprint": pl.get("footprint", "round")}
                rec["depth_true"] = y
            if row.get("depth") is not None:
                rec["depth"] = sorted(eval_expr(d, P, names) for d in row["depth"])
                if pl:
                    rec["depth_spec"] = rec["depth"]
                    rec["depth"] = [min(rec["depth"][0], y[0]), max(rec["depth"][1], y[1])]
            elif pl:
                rec["depth"] = list(y)
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
    rep["park_tip_by_plane_z_A"] = {term: {k: park_tip_z_A(P, [k], glob[term], spec, glob) for k in lengths} for term in ("core_stop", "collar_top")}
    # Q9 options (gameplan detail 1.1 Reported): park, stroke and screw length per option; no threshold
    opts = {}
    for name, keys in (spec.get("q9_options") or {}).items():
        keys = [k for k in keys if P.has(k)]
        park = park_tip_z_A(P, keys, glob["entry_plane"], spec, glob)
        low = min(class_stops_z_A(P, spec, keys, glob).values()) if spec.get("park_rule") else glob["lowest_tip"]
        nm = dict(glob)
        nm.update({"park": park, "stroke": park - low})
        gm = [g for s in ("a", "b") for g in _try_block_g_min(spec, s)]
        if gm:
            nm["g_min_screw_block"] = max(gm)
        Ls = {lk: eval_expr(ex, P, nm) for lk, ex in (spec.get("screw_length") or {}).items()}
        starts = class_starts_z_A(P, spec, keys, glob)
        # FIX 5 (Loftsman 1.1 (b)), reported only: start tip minus the top of that class's core on the core stop.
        # Negative = the cutter starts inside the uncut core.
        over = {k: v - (glob["core_stop"] + P.get(k)) for k, v in starts.items() if P.has(k)}
        opts[name] = {"lengths": keys, "starts_z_A": starts, "park_tip_z_A": park,
                      "lowest_stop_z_A": low, "lift_stroke": park - low, "L": Ls, "start_minus_core_top": over}
    rep["q9_options"] = opts
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
