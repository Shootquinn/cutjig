"""S2 checks S2-1 to S2-6 (contributor gameplan (sean) detail 1.2 table, lines 250-258; Design Notes 27).
Skeleton written at 1.2 (b) from the spec block s2_checks; fixtures (S2-x Z and B), STUB_EXPECT, STUB_CAUSE and SOURCES
come at 1.2 (c). Each check reads drawn patches located by gid in the plan figure and fails closed (cause "absent")
when a part it needs is not drawn, so it is red on the floor-only stub. Plan coordinates in mm; heights from check_stack
in z_A (S2-5b is a z premise and has no drawn z in plan).
S2-3 has no drawn quantity yet: the pitch point is not a drawn feature until (c) defines one; it fails closed (content).
"""
import math
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


def _fig_pose(ctx):
    pf = (ctx.spec.get("plan_figure") or {}).get("pose", "load")
    if pf not in ctx.figs:
        raise Absent(f"plan figure (pose {pf}) not built")
    return pf


def _pieces(ctx, fid):
    pose = _fig_pose(ctx)
    p = sc.pieces(ctx.figs[pose].axes[0], fid)
    if not p:
        raise Absent(f"{fid} not drawn")
    return p


def _centre(ctx, fid):
    return sc.centroid(_pieces(ctx, fid))


def _az(xy):
    return math.degrees(math.atan2(xy[1], xy[0])) % 360


def _cfg(ctx, cid):
    c = (ctx.spec.get("s2_checks") or {}).get(cid)
    if not c:
        raise Content(f"spec s2_checks has no {cid} block")
    return c


def _run(cid, fn, ctx):
    try:
        return fn(ctx)
    except Absent as e:
        return sc.result(cid, False, f"measured: none; {e}", cause="absent")
    except Content as e:
        return sc.result(cid, False, str(e), cause="content")


def _spacing_issues(name, azs, spacing, tol):
    out = []
    s = sorted(azs)
    for i in range(len(s)):
        d = (s[(i + 1) % len(s)] - s[i]) % 360
        if abs(d - spacing) > tol:
            out.append(f"{name} spacing {d:.2f} deg, want {spacing} +- {tol}")
    return out


def s2_1(ctx):
    """Azimuths from drawn centres: screws and pinions 120 deg apart, pinion = screw + phase (mod spacing)."""
    c = _cfg(ctx, "S2-1")
    sp, ph, tol = c["spacing_deg"], c["phase_deg"], c["tol_deg"]
    sa = {f: _az(_centre(ctx, f)) for f in c["screws"]}
    pa = {f: _az(_centre(ctx, f)) for f in c["pinions"]}
    issues = _spacing_issues("screw", list(sa.values()), sp, tol) + _spacing_issues("pinion", list(pa.values()), sp, tol)
    worst = 0.0
    for p, a in pa.items():
        for s, b in sa.items():
            d = ((a - b) % sp) - ph
            worst = max(worst, abs(d))
            if abs(d) > tol:
                issues.append(f"{p} - {s} = {(a - b) % 360:.2f} deg, phase mod {sp} off {ph} by {d:+.2f}")
    return sc.result("S2-1", not issues, sc._summ(issues) if issues else
                     f"screws {sorted(round(v, 2) for v in sa.values())}, pinions {sorted(round(v, 2) for v in pa.values())}, phase {ph} within {worst:.3f}",
                     measured=round(worst, 4), threshold=tol, n_issues=len(issues))


def _radius_of(polys):
    ex, ey = sc.extent_x(polys), sc.extent_z(polys)
    return max(ex[1] - ex[0], ey[1] - ey[0]) / 2


def s2_2(ctx):
    """Screws clear the keep-out: drawn screw centre radius - drawn nut flange radius - drawn keep-out radius >= g_min."""
    c = _cfg(ctx, "S2-2")
    ko = _radius_of(_pieces(ctx, "keepout"))
    issues, worst = [], None
    for s in c["screws"]:
        r = math.hypot(*_centre(ctx, s))
        nut = _radius_of(_pieces(ctx, s.replace("screw_", "nut_")))
        m = r - nut - ko
        worst = m if worst is None else min(worst, m)
        if m < c["g_min"] - sc.TOL_C:
            issues.append(f"{s}: {r:.2f} - {nut:.2f} - {ko:.2f} = {m:.2f} < {c['g_min']}")
    return sc.result("S2-2", not issues, sc._summ(issues) if issues else f"least margin {worst:.2f} mm over g_min {c['g_min']}",
                     measured=round(worst, 3), threshold=c["g_min"], n_issues=len(issues))


def s2_3(ctx):
    """Pinion pitch point at the gear pitch radius (0.05). The pitch point is not a drawn feature at (b)."""
    c = _cfg(ctx, "S2-3")
    for p in c["pinions"] + [c["gear"]]:
        _pieces(ctx, p)
    raise Content("S2-3: no drawn pitch point to measure; (c) defines the drawn quantity (pitch-point marker or heel edge) and its Z and B")


def s2_4(ctx):
    """Nominal coaxiality: drawn centres of drill tube, datum B mark, ring and gear coincide within tol."""
    c = _cfg(ctx, "S2-4")
    cen = {}
    for f in c["rows"]:
        P = _pieces(ctx, f)
        ex, ey = sc.extent_x(P), sc.extent_z(P)
        cen[f] = ((ex[0] + ex[1]) / 2, (ey[0] + ey[1]) / 2)
    ref = cen[c["rows"][0]]
    issues, worst = [], 0.0
    for f, xy in cen.items():
        d = math.hypot(xy[0] - ref[0], xy[1] - ref[1])
        worst = max(worst, d)
        if d > c["tol"]:
            issues.append(f"{f} centre ({xy[0]:.2f}, {xy[1]:.2f}) is {d:.2f} from {c['rows'][0]}")
    return sc.result("S2-4", not issues, sc._summ(issues) if issues else f"{len(cen)} centres within {worst:.3f} mm",
                     measured=round(worst, 4), threshold=c["tol"], n_issues=len(issues))


def s2_5a(ctx):
    """Operator sector free in plan of every fixed part at all z (K7 F: overlap <= 0.01 mm2 and distance > 0.05)."""
    c = _cfg(ctx, "S2-5a")
    S = _pieces(ctx, c["sector"])
    issues, worst = [], None
    for f in c["fixed"]:
        P = _pieces(ctx, f)
        d, a = sc.pair_measure(S, P)
        worst = d if worst is None else min(worst, d)
        if a > sc.TOL_AREA or d <= sc.TOL_C:
            issues.append(f"{c['sector']}|{f}: distance {d:.3f}, overlap {a:.3f} mm2")
    return sc.result("S2-5a", not issues, sc._summ(issues) if issues else f"{len(c['fixed'])} fixed parts clear of the sector, least {worst:.2f} mm",
                     measured=None if worst is None else round(worst, 3), threshold="F", n_issues=len(issues))


def s2_5b(ctx):
    """Premise of the S2-5a relief: at the load pose every ring-mounted part whose drawn plan outline enters the drawn
    sector has its lowest z (check_stack, z_A) at least g_min above the top of operator.hand_band."""
    c = _cfg(ctx, "S2-5b")
    S = _pieces(ctx, c["sector"])
    top = ctx.P.get(c["band"])[1]
    feats = ctx.stack["poses"][c["pose"]]["features"]
    issues, worst, n = [], None, 0
    for f in c["ring_parts"]:
        P = _pieces(ctx, f)
        if sc.pair_measure(S, P)[1] <= sc.TOL_AREA:
            continue
        n += 1
        z = check_stack.from_shop_floor(feats[f]["z_min"], ctx.P)
        m = z - top
        worst = m if worst is None else min(worst, m)
        if m < c["g_min"] - sc.TOL_C:
            issues.append(f"{f}: lowest z {z:.2f} z_A, {m:.2f} above the hand band top {top}, need {c['g_min']}")
    if n == 0:
        raise Content("S2-5b: no ring-mounted part enters the drawn sector (premise untested)")
    return sc.result("S2-5b", not issues, sc._summ(issues) if issues else f"{n} ring parts in the sector, least {worst:.2f} mm above the hand band",
                     measured=round(worst, 3), threshold=c["g_min"], n_issues=len(issues))


def s2_6(ctx):
    """Member seats: each member's drawn outline lies inside its seat's drawn pieces (contained within tol; plate pieces
    exclude the column notches); a member seated on the frame also clears the plate by notch_clear."""
    c = _cfg(ctx, "S2-6")
    issues = []
    for m, seat in c["seats"].items():
        M, S = _pieces(ctx, m), _pieces(ctx, seat)
        area = sum(sc.poly_area(p) for p in M)
        on = sum(sc.overlap_area(p, q) for p in M for q in S if len(q) >= 3)
        if area - on > sc.TOL_AREA + c["tol"] * 1e-3 * area:
            issues.append(f"{m}: {area - on:.2f} mm2 of {area:.2f} outside {seat}")
        if seat != "base_plate":
            plate = _pieces(ctx, "base_plate")
            d = min(sc.min_distance(p, q) for p in M for q in plate if len(q) >= 3)
            if d < c["notch_clear"] - c["tol"]:
                issues.append(f"{m}: {d:.2f} from the plate edge in the notch, want {c['notch_clear']}")
    return sc.result("S2-6", not issues, sc._summ(issues) if issues else f"{len(c['seats'])} members seated",
                     measured=len(issues), threshold=0, n_issues=len(issues))


CHECKS = [("S2-1", s2_1), ("S2-2", s2_2), ("S2-3", s2_3), ("S2-4", s2_4), ("S2-5a", s2_5a), ("S2-5b", s2_5b), ("S2-6", s2_6)]


def run(ctx):
    return [_run(cid, fn, ctx) for cid, fn in CHECKS]
