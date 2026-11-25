"""S2 checks S2-1 to S2-6 (contributor gameplan (sean) detail 1.2 table, lines 250-258; Design Notes 27).
Skeleton written at 1.2 (b) from the spec block s2_checks; fixtures (S2-x Z and B), STUB_EXPECT, STUB_CAUSE and SOURCES
come at 1.2 (c). Each check reads drawn patches located by gid in the plan figure and fails closed (cause "absent")
when a part it needs is not drawn, so it is red on the floor-only stub. Plan coordinates in mm; heights from check_stack
in z_A (S2-5b is a z premise and has no drawn z in plan).
S2-3 (1.2 (c)): the drawn pitch point is the midpoint of the heel edge of each pinion's toothed trapezoid (the outer of its
two edges across the radial direction; sketch_common.heel_point); the pinion is drawn as that trapezoid (toe to
pinion.r_heel, narrowing inward) plus its hub rectangle to the place r_out (K5 hub admission).
1.2 (c) tables: STUB_EXPECT, STUB_CAUSE and SOURCES for check_sketch.py (run_sketch, --baseline s2).
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
    """Pinion mesh: each drawn pinion pitch point (heel-edge midpoint of its toothed trapezoid, at the placed azimuth) lies
    at the gear pitch radius (spec expression pitch_r) within tol; the gear must be drawn."""
    c = _cfg(ctx, "S2-3")
    _pieces(ctx, c["gear"])
    pose = _fig_pose(ctx)
    want = check_stack.eval_expr(c["pitch_r"], ctx.P, {})
    issues, worst, got = [], 0.0, {}
    for p in c["pinions"]:
        polys = _pieces(ctx, p)
        pl = ctx.stack["poses"][pose]["features"][p].get("place")
        if not pl:
            raise Content(f"S2-3: {p} has no place (no azimuth for the radial frame)")
        traps = [q for q in polys if len(q) == 4 and not sc._is_rect(q)]
        if not traps:
            issues.append(f"{p}: no toothed trapezoid drawn (no heel edge)")
            continue
        hp = sc.heel_point(traps[0], pl["theta"])
        if hp is None:
            issues.append(f"{p}: trapezoid has no edge pair across the radial direction (no heel edge)")
            continue
        r = math.hypot(*hp)
        got[p] = round(r, 3)
        worst = max(worst, abs(r - want))
        if abs(r - want) > c["tol"]:
            issues.append(f"{p}: pitch point r {r:.2f} vs gear pitch radius {want:.2f} (off {r - want:+.2f})")
    return sc.result("S2-3", not issues, sc._summ(issues) if issues else f"pitch points {got} at the gear pitch radius {want:.2f} within {worst:.3f}",
                     measured=round(worst, 4), threshold=c["tol"], n_issues=len(issues))


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


def _outline(ctx, fid):
    """Plan outline of a drawn row (sketch_common.plan_outline: the spec footprint that contains the drawn part, K8);
    the drawn pieces when the row has no plan basis. Absent when the row is not drawn."""
    P = _pieces(ctx, fid)
    o = sc.plan_outline(ctx, {r["id"]: r for r in ctx.spec["features"]}[fid], _fig_pose(ctx))
    return o or ("polys", P, True)


def s2_5a(ctx):
    """Operator sector free in plan of every fixed part at all z (K7 F: overlap <= 0.01 mm2 and distance > 0.05).
    1.2 (c): the drawn sector (K8 holds it equal to the spec wedge) against each fixed part's plan outline (the spec
    footprint containing the drawn part, K8 plan_extent), so a part drawn narrower than its footprint cannot pass."""
    c = _cfg(ctx, "S2-5a")
    S = ("polys", _pieces(ctx, c["sector"]), True)
    issues, worst = [], None
    for f in c["fixed"]:
        d, a = sc.outline_measure(S, _outline(ctx, f), sc.TOL_C)
        worst = d if worst is None else min(worst, d)
        if a > sc.TOL_AREA or d <= sc.TOL_C:
            issues.append(f"{c['sector']}|{f}: distance {d:.3f}, overlap {a:.3f} mm2")
    return sc.result("S2-5a", not issues, sc._summ(issues) if issues else f"{len(c['fixed'])} fixed parts clear of the sector, least {worst:.2f} mm",
                     measured=None if worst is None else round(worst, 3), threshold="F", n_issues=len(issues))


def s2_5b(ctx):
    """Premise of the S2-5a relief: at the load pose every ring-mounted part whose plan outline enters the drawn
    sector has its lowest z (check_stack, z_A) at least g_min above the top of operator.hand_band."""
    c = _cfg(ctx, "S2-5b")
    S = ("polys", _pieces(ctx, c["sector"]), True)
    top = ctx.P.get(c["band"])[1]
    feats = ctx.stack["poses"][c["pose"]]["features"]
    issues, worst, n = [], None, 0
    for f in c["ring_parts"]:
        if sc.outline_measure(S, _outline(ctx, f), sc.TOL_C)[1] <= sc.TOL_AREA:
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


# Per-sketch tables (1.2 (c); check_sketch.sketch_table reads them). Every S2 check reads drawn patches and fails closed
# (absent) on the floor-only stub; the content evidence is the S2-x B fixtures in run 1 (fixtures/manifest.yaml).
_ABS = ("absent", "red (absent, fail-closed; content evidence run 1, S2-x B fixtures 1.2 (c))")
_ABS_K = ("absent", "red (absent, fail-closed; content evidence run 1)")
STUB_EXPECT = {"guard": ["K1", "K2", "K3", "K5", "X1"],
               "red": ["K4", "K6", "K7", "K8", "K9", "S2-1", "S2-2", "S2-3", "S2-4", "S2-5a", "S2-5b", "S2-6"]}
STUB_CAUSE = {"K6": _ABS_K, "K7": _ABS_K, "K8": _ABS_K,
              **{k: _ABS for k in ("S2-1", "S2-2", "S2-3", "S2-4", "S2-5a", "S2-5b", "S2-6")}}
SOURCES = {
    "S2-1": "[DN23], [CP §15]; phase 60 Designer 1.2 (a) section 4, Design Notes 27 (O1-B) ASSUMED",
    "S2-2": "keep-out DERIVED; 10 mm ASSUMED",
    "S2-3": "overlay gear.*, pinion.r_heel ASSUMED/DERIVED; drawn pitch point = heel-edge midpoint (1.2 (c))",
    "S2-4": "R13 ASSUMED [CP §14]; nominal only",
    "S2-5a": "sector ASSUMED (operator.*, Designer 1.2 (a) section 5; Design Notes 27 O1-B)",
    "S2-5b": "hand band ASSUMED (operator.hand_band); premise of S2-5a (detail 1 common (h))",
    "S2-6": "params base.*, overlay frame_upper.foot, frame_upper.radius 274 (Design Notes 27)",
}


CHECKS = [("S2-1", s2_1), ("S2-2", s2_2), ("S2-3", s2_3), ("S2-4", s2_4), ("S2-5a", s2_5a), ("S2-5b", s2_5b), ("S2-6", s2_6)]


def run(ctx):
    return [_run(cid, fn, ctx) for cid, fn in CHECKS]
