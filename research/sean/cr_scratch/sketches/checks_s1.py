"""S1 checks S1-1 to S1-6 (research/sean/gameplan.md detail 1.1, lines 223-231).

Each check measures drawn patch coordinates per pose, located by gid, and compares them with check_stack.py values.
A check that read params alone would be green on the floor-only stub (Manager open F3). Heights in z_S.
cause: "absent" when the check stopped on an undrawn part (fail-closed), "content" otherwise (SW-7, SW-11).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402

TOL = sc.TOL_Z


class Absent(Exception):
    pass


class Content(Exception):
    pass


def _pieces(ctx, pose, fid):
    if pose not in ctx.figs:
        raise Absent(f"pose {pose} has no figure")
    p = sc.pieces(ctx.figs[pose].axes[0], fid)
    if not p:
        raise Absent(f"{fid} not drawn in pose {pose}")
    return p


def _zmin(ctx, pose, fid):
    return sc.extent_z(_pieces(ctx, pose, fid))[0]


def _zmax(ctx, pose, fid):
    return sc.extent_z(_pieces(ctx, pose, fid))[1]


def _tip(ctx, pose):
    """Drawn tip = bottom of the drill head; must agree with check_stack tip_z_S."""
    drawn = _zmin(ctx, pose, "drill_head")
    want = ctx.stack["poses"][pose]["tip_z_S"]
    if abs(drawn - want) > TOL:
        raise Content(f"drawn tip {drawn:.2f} in {pose} differs from check_stack {want:.2f} z_S")
    return drawn


def _run(cid, fn, ctx):
    try:
        return fn(ctx)
    except Absent as e:
        return sc.result(cid, False, f"measured: none; {e}", cause="absent")
    except Content as e:
        return sc.result(cid, False, str(e), cause="content")


def s1_1(ctx):
    g = ctx.P.get
    reach = _tip(ctx, "start") - _tip(ctx, "capture_end")
    lo, hi = g("upper.drill_advance_500core"), g("upper.travel_max")
    ok = lo <= reach + TOL and reach <= hi + TOL
    return sc.result("S1-1", ok, f"drawn start tip minus end-of-capture tip {reach:.2f} mm against [{lo}, {hi}]",
                     measured=round(reach, 3), threshold=[lo, hi])


def s1_2(ctx):
    need = check_stack.to_shop_floor(max(ctx.P.get("stop.start_z")), ctx.P)
    issues, worst = [], None
    for pose in ("park", "load"):
        tip = _tip(ctx, pose)
        worst = tip - need if worst is None else min(worst, tip - need)
        if tip <= need:
            issues.append(f"{pose}: drawn tip {tip:.2f} not above max(stop.start_z) {need:.2f} z_S")
    return sc.result("S1-2", not issues, "; ".join(issues) or f"park tip above max(stop.start_z) by {worst:.2f} mm",
                     measured=round(worst, 3), threshold="> 0")


def s1_3(ctx):
    """Park clears each Q9 core standing on the load plane; the plane is the spec's load_plane (LF-6), the same
    field check_stack's park rule reads."""
    g = ctx.P.get
    lp = check_stack.load_plane(ctx.spec)
    tip = _tip(ctx, "park")
    ext = sc.extent_z(_pieces(ctx, "park", lp["feature"]))
    plane = (ext[1] if lp["edge"] == "z_max" else ext[0]) + check_stack.eval_expr(lp.get("offset", 0), ctx.P, {})
    issues, margins = [], {}
    for k in ctx.spec.get("q9_length_keys", check_stack.DEFAULT_Q9):
        m = tip - g("upper.load_clearance") - (plane + g(k))
        margins[k] = round(m, 3)
        if m < -TOL:
            issues.append(f"{k}: park tip - load_clearance - ({lp['term']} + length) = {m:.2f}")
    return sc.result("S1-3", not issues, "; ".join(issues) or f"margins over {lp['term']} {margins}", measured=margins, threshold=">= 0")


def s1_4(ctx):
    g = ctx.P.get
    half = g("jackscrew.nut_length") / 2
    issues, worst = [], None
    for pose in [p["id"] for p in ctx.spec["poses"]]:
        for s in ("a", "b"):
            anchor = _zmin(ctx, pose, f"anchor_{s}")
            guide = _zmax(ctx, pose, f"guide_{s}")
            nut = sc.centroid(_pieces(ctx, pose, f"nut_{s}"))[1]
            lo = anchor + g("jackscrew.anchor_allowance") + half
            hi = guide - g("jackscrew.guide_allowance") - half
            m = min(nut - lo, hi - nut)
            worst = m if worst is None else min(worst, m)
            if m < -TOL:
                issues.append(f"{pose}/screw {s}: nut z {nut:.1f} outside [{lo:.1f}, {hi:.1f}]")
    return sc.result("S1-4", not issues, sc._summ(issues) if issues else f"nut inside travel at every pose, least margin {worst:.2f} mm",
                     measured=round(worst, 3), threshold=">= 0")


def s1_5a(ctx):
    ceiling = _zmin(ctx, "capture_end", "bore_ceiling")
    top = _zmax(ctx, "capture_end", "core_500")
    gap = ceiling - top
    need = ctx.P.get("stop.g_stop")
    return sc.result("S1-5a", gap >= need - TOL, f"bore ceiling minus 0.5 m core top at end of capture {gap:.2f} mm, need {need}",
                     measured=round(gap, 3), threshold=need)


def s1_5b(ctx):
    """Pairs and g_min from the spec: neighbours with group S1-5b (gameplan l.148; SW-9). Same judgement as K7."""
    pose = "capture_end"
    pairs = [(row["id"], nb) for row in ctx.spec["features"] for nb in (row.get("neighbours") or []) if nb.get("group") == "S1-5b"]
    if not pairs:
        raise Content("spec carries no neighbour with group S1-5b")
    worst, issues, tested = None, [], 0
    for a, nb in pairs:
        PA, PB = _pieces(ctx, pose, a), _pieces(ctx, pose, nb["id"])
        gap = sc.band_gap(sc._depth(ctx, pose, a), sc._depth(ctx, pose, nb["id"]))
        ok, st, txt, lb = sc.assess_pair(nb["class"], nb.get("g_min"), PA, PB, gap, (a, nb["id"]))
        tested += 1
        if lb is not None:
            worst = lb if worst is None else min(worst, lb)
        if not ok:
            issues.append(f"{a}|{nb['id']}: {txt}")
    need = sorted({nb.get("g_min") for _, nb in pairs})
    return sc.result("S1-5b", not issues, sc._summ(issues) if issues else f"{tested} pairs, least certified clearance {worst:.2f} mm",
                     measured=None if worst is None else round(worst, 3), threshold=need[0] if len(need) == 1 else need,
                     n_issues=len(issues))


def s1_6(ctx):
    """Screw projection: drawn x centre = r cos(theta), depth centre = r sin(theta); r and theta from the spec place."""
    issues, n = [], 0
    for fid in ("screw_a", "screw_b"):
        for pose in [p["id"] for p in ctx.spec["poses"]]:
            f = ctx.stack["poses"][pose]["features"][fid]
            pl = f.get("place")
            if not pl:
                raise Content(f"{fid} has no place in the spec")
            r, th = pl["r_c"], pl["theta"]
            x = sc.centroid(_pieces(ctx, pose, fid))[0]
            dep = f["depth"]
            n += 1
            if abs(x - r * check_stack.cosd(th)) > TOL:
                issues.append(f"{pose}/{fid}: drawn x {x:.2f}, r cos(theta) {r * check_stack.cosd(th):.2f} (theta {th:g})")
            if abs((dep[0] + dep[1]) / 2 - r * check_stack.sind(th)) > TOL:
                issues.append(f"{pose}/{fid}: depth centre {(dep[0] + dep[1]) / 2:.2f}, r sin(theta) {r * check_stack.sind(th):.2f}")
    return sc.result("S1-6", not issues, sc._summ(issues) if issues else f"{n} screw projections at r cos(theta), depth r sin(theta)",
                     measured=len(issues), threshold=0, n_issues=len(issues))


CHECKS = [("S1-1", s1_1), ("S1-2", s1_2), ("S1-3", s1_3), ("S1-4", s1_4), ("S1-5a", s1_5a), ("S1-5b", s1_5b), ("S1-6", s1_6)]


def run(ctx):
    return [_run(cid, fn, ctx) for cid, fn in CHECKS]
