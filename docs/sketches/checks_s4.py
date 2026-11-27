"""S4 checks S4-1 to S4-3 (contributor gameplan (sean) detail 1.4 table as ruled at STOP S4-A, Design Notes 34).
Skeleton written at 1.4 (b) from the spec block s4_checks; the drawn readers land at 1.4 (c) (P4) with the S4-x fixtures.
S4-1 reads the keys through check_stack.collar_top_z_A (the test_P18 formula) and the drawn collar top. S4-2 is the ruled
short-core exposure and grip on the drawn configuration (advance D with the carrier C drawn). S4-3 evaluates the K8 sense
predicates of the kept parts in the section Axes. Every drawn read fails closed (cause "absent") when a part it needs is
not drawn, so the checks are red on the floor-only stub; the content evidence is the S4-x B fixtures in run 1 (1.4 (c)).
Heights z_A unless stated; the figure plots z_S.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402

SECTION_AXES = "section"


class Absent(Exception):
    pass


class Content(Exception):
    pass


def _cfg(ctx, cid):
    c = (ctx.spec.get("s4_checks") or {}).get(cid)
    if not c:
        raise Content(f"spec s4_checks has no {cid} block")
    return c


def _poses(ctx):
    """Figure poses (spec section_figures; P4 generalises the single section_figure reader)."""
    figs = ctx.spec.get("section_figures") or [ctx.spec.get("section_figure") or {}]
    return [f.get("pose") for f in figs if f.get("pose")]


def _section(ctx):
    c = sc.axes_context(ctx, SECTION_AXES)
    if c is None:
        raise Content(f"spec declares no Axes {SECTION_AXES}")
    return c


def _ax(ctx, pose):
    c = _section(ctx)
    if not c.figs or pose not in c.figs:
        raise Absent(f"section figure (pose {pose}) not built")
    return c.figs[pose].axes[0]


def _pieces(ctx, pose, fid):
    p = sc.pieces(_ax(ctx, pose), fid)
    if not p:
        raise Absent(f"{pose}/{fid} not drawn")
    return p


def _z_A(ctx, z_S):
    return check_stack.from_shop_floor(z_S, ctx.P)


def _run(cid, fn, ctx):
    try:
        return fn(ctx)
    except Absent as e:
        return sc.result(cid, False, f"measured: none; {e}", cause="absent")
    except Content as e:
        return sc.result(cid, False, str(e), cause="content")


# ---------------------------------------------------------------- arithmetic from the keys (no drawing)

def collar_top_formula(P):
    """test_P18_collar_top_recomputed_from_params (tests/test_params_bom.py l.694-702), the one function check_stack
    uses for the stack term collar_top (nut plate 8 written from params there)."""
    return check_stack.collar_top_z_A(P)


def slice_numbers(P):
    """Q10 and advance arithmetic (Designer 1.4 (a) sections 6, 9): least slice under F4, sliceable length of the 0.75 m
    core, minimum core on the stop, stubs. All DERIVED from the keys; reported, never asserted."""
    g = P.get
    tip = g("stop.height_z")
    kc = tip + g("drill.kerf_standoff")
    pole = tip + g("drill.dome_pole_offset")
    r_core = g("core.diameter_nominal") / 2
    r_s = g("iris.face_radius_core")
    surf = kc - math.sqrt(r_s ** 2 - r_core ** 2)
    plate_top = check_stack.collar_top_z_A(P) - g("collar.top_above_plate")
    min_top = plate_top + g("core.min_exposed")
    cs_ = check_stack.core_stop_z_A(P)
    sl_axis, sl_surf = min_top - pole, min_top - surf
    sliceable = cs_ + g("core.length_install") - min_top
    car_top = cs_ + g("carrier.length")
    return {"kerf_centre": kc, "dome_pole": pole, "sphere_at_core_surface": surf, "plate_top": plate_top, "min_core_top": min_top,
            "slice_min_axis": sl_axis, "slice_min_surface": sl_surf, "min_on_stop": min_top - cs_,
            "min_on_stop_collar_datum": check_stack.collar_top_z_A(P) + g("core.min_exposed") - cs_,
            "sliceable_075": sliceable, "slices_075": math.floor(sliceable / sl_axis + 1e-9),
            "core_top_on_stop": cs_ + g("core.length_short"), "core_top_on_carrier": car_top + g("core.length_short"),
            "stub_axis": pole - car_top, "stub_surface": surf - car_top}


# ---------------------------------------------------------------- checks

def s4_1(ctx):
    """Collar top by the test_P18 formula against stop.collar_top_z within 0.01; the drawn collar top equals it within
    0.05 (z_S converted once to z_A). B (1.4 (c)): holder.flange_thickness dropped from the stack, 151.84."""
    c = _cfg(ctx, "S4-1")
    want = ctx.P.get(c["against"])
    got = collar_top_formula(ctx.P)
    f_form = check_stack.eval_expr(c["formula"], ctx.P, {})
    issues = []
    if abs(got - want) > float(c["tol"]):
        issues.append(f"collar top by the test_P18 formula {got:.3f} vs {c['against']} {want:.3f} (tol {c['tol']})")
    if abs(f_form - got) > 1e-9:
        issues.append(f"spec formula {f_form:.3f} differs from check_stack.collar_top_z_A {got:.3f}")
    dr = c["drawn"]
    for pose in _poses(ctx):
        zd = _z_A(ctx, sc.extent_z(_pieces(ctx, pose, dr["row"]))[1])
        if abs(zd - got) > float(dr["tol"]):
            issues.append(f"{pose}: drawn {dr['row']} top {zd:.3f} z_A vs formula {got:.3f}")
    return sc.result("S4-1", not issues, sc._summ(issues) if issues else f"collar top {got:.2f} z_A = {c['against']} {want:.2f}; drawn top equal in every figure",
                     measured=round(got, 3), threshold=c["tol"], n_issues=len(issues))


def s4_2(ctx):
    """Short-core exposure and grip on the drawn configuration (Sean STOP S4-A): (a) core rests on the carrier and the
    carrier on its core seat within 0.05; (b) drawn core top minus the drawn nut-plate top >= core.min_exposed; (c) the
    grip member's drawn z extent covers the collet straight-bore band."""
    c = _cfg(ctx, "S4-2")
    names = lambda pose: ctx.stack["poses"][pose]["vars_z_A"]  # noqa: E731
    mn = ctx.P.get(c["exposure"]["min"])
    issues, worst = [], None
    for pose, pc in c["poses"].items():
        ez = lambda fid: [_z_A(ctx, z) for z in sc.extent_z(_pieces(ctx, pose, fid))]  # noqa: E731
        core, car, seat = ez(pc["core"]), ez(pc["carrier"]), ez(pc["seat"])
        for a, b, za, zb in ((pc["core"], pc["carrier"], core[0], car[1]), (pc["carrier"], pc["seat"], car[0], seat[1])):
            if abs(za - zb) > 0.05:
                issues.append(f"{pose} (a): {a} bottom minus {b} top {za - zb:.3f}")
        plate = ez(c["exposure"]["datum_row"])[1]
        exp = core[1] - plate
        m = exp - mn
        worst = m if worst is None else min(worst, m)
        if m < 0:
            issues.append(f"{pose} (b): exposure {exp:.2f} (core top {core[1]:.2f} - nut-plate top {plate:.2f}) < core.min_exposed {mn:.2f}")
        lo, hi = (check_stack.eval_expr(e, ctx.P, names(pose)) for e in pc["grip_band"])
        g_ = ez(pc["grip_member"])
        if g_[0] > lo + 0.05 or g_[1] < hi - 0.05:
            issues.append(f"{pose} (c): {pc['grip_member']} drawn z [{g_[0]:.2f}, {g_[1]:.2f}] does not cover the grip band [{lo:.2f}, {hi:.2f}]")
    return sc.result("S4-2", not issues, sc._summ(issues) if issues else f"least exposure margin {worst:.2f} mm over core.min_exposed {mn:.2f}; rests_on and grip hold in every figure",
                     measured=None if worst is None else round(worst, 3), threshold=0, n_issues=len(issues))


def s4_3(ctx):
    """K8 sense predicates of the kept parts (spec s4_checks.S4-3.rows) in the section Axes: any issue fails. Reads the
    section Axes K8 result restricted to the listed rows (P4 wires the per-row filter; piece / of_piece, vertical_edge,
    between and seat_piece are new predicate forms signed by the Topologist at (c))."""
    c = _cfg(ctx, "S4-3")
    sec = _section(ctx)
    for pose in _poses(ctx):
        _ax(ctx, pose)
    rows = set(c["rows"])
    k8 = sc.k8(sec)
    mine = [t for t in (k8.get("issues") or []) if any(f"/{r} " in t for r in rows)]
    if k8.get("absent"):
        raise Absent(f"{k8.get('absent')} predicate(s) untestable (part not drawn)")
    return sc.result("S4-3", not mine, sc._summ(mine) if mine else f"kept-part sense predicates hold ({', '.join(sorted(rows))})", n_issues=len(mine))


def reported(ctx):
    """RPT items (spec reported_items). Arithmetic from the keys; needs_drawing items read the drawn rows and read
    'not drawn' on the stub."""
    P = ctx.P
    n = slice_numbers(P)
    items = {}
    items["q10_min_on_stop"] = {"value": f"{n['min_on_stop']:.2f} (nut-plate datum); {n['min_on_stop_collar_datum']:.2f} (collar-top datum)", "basis": "nut-plate top + core.min_exposed - core stop", "tag": "DERIVED"}
    items["advance"] = {"value": (f"option D: the lift lowers the drill one slice per cut; least slice {n['slice_min_axis']:.2f} (axis), {n['slice_min_surface']:.2f} (r {P.get('core.diameter_nominal') / 2:g}); "
                                  f"0.75 m core sliceable {n['sliceable_075']:.2f}, {n['slices_075']} slices; 100 mm core on the carrier: 1 slice, stub {n['stub_axis']:.2f} (axis) to {n['stub_surface']:.2f} (surface)"),
                        "basis": "F4: core top >= kerf centre + stop.margin at the stop", "tag": "DERIVED"}
    T = P.get("loads.torque_design") * 1000.0
    r = P.get("core.diameter_nominal") / 2
    items["carrier_torque"] = {"value": f"bottom face {2 * T / (math.pi * r ** 3) * 1000:.1f} kPa; liner side {T / (2 * math.pi * r ** 2 * P.get('core.length_short')) * 1000:.2f} kPa",
                               "basis": "2T / (pi r^3); T / (2 pi r^2 L)", "tag": "DERIVED"}
    ct = collar_top_formula(P)
    items["q5_delta"] = {"value": "; ".join(f"Delta {d}: collar top {ct + d:.2f}, stop {ct + d + P.get('stop.g_stop'):.2f}, min core on the stop {n['min_on_stop'] + d:.2f}" for d in (0, 25, 50)) + "; kept 32 mm (Design Notes 34)",
                         "basis": "Designer 1.4 (a) section 7", "tag": "DERIVED"}
    items["liner_wall"] = {"value": f"D = d + {P.get('liner.od_offset'):g}, free wall {P.get('liner.wall'):.2f}; d 105 core: no liner ({105 + P.get('liner.od_offset'):g} > collets.envelope_max {P.get('collets.envelope_max'):g})",
                           "basis": "liner.od_offset, liner.wall", "tag": "DERIVED"}
    items["kept_axial"] = {"value": "as S3 r7 kept_axial (1000 N at the cut; F_stall + W 1287.05 / 1104.16 N)", "basis": "checks_s3.loads (P4 reads it from the S3 spec)", "tag": "DERIVED"}
    for k, txt in (("q10_core_top", None), ("q10_exposed", None), ("grip_length", None), ("cut_case_seat", None)):
        items[k] = {"value": None, "basis": "needs the drawing (1.4 (d))", "tag": None}
    try:
        pose = _poses(ctx)[0]
        ez = lambda fid: [_z_A(ctx, z) for z in sc.extent_z(_pieces(ctx, pose, fid))]  # noqa: E731
        core, plate = ez("core_100"), ez("wingnut")[1]
        items["q10_core_top"] = {"value": f"on the carrier {core[1]:.2f} (collar top {ct:.2f}); on the stop {n['core_top_on_stop']:.2f} ({ct - n['core_top_on_stop']:.2f} below the collar top)", "basis": "drawn core_100 (MEASURED); core on the stop DERIVED", "tag": "MEASURED"}
        items["q10_exposed"] = {"value": f"{core[1] - plate:.2f} on the carrier against {P.get('core.min_exposed'):.2f}; on the stop {n['core_top_on_stop'] - n['plate_top']:.2f}", "basis": "drawn core_100 and wingnut tops", "tag": "MEASURED"}
    except (Absent, Content):
        pass
    rows = [(k, v["value"], v["basis"]) for k, v in items.items()]
    return {"id": "reported", "result": "pass", "rows": rows, "items": items}


_ABS = ("absent", "red (absent, fail-closed; content evidence run 1, S4-x B fixtures 1.4 (c))")
_ABS_K = ("absent", "red (absent, fail-closed; content evidence run 1)")
STUB_EXPECT = {"guard": ["K1", "K2", "K3", "K5", "X1"],
               "red": ["K4", "K6", "K7", "K8", "K9", "S4-1", "S4-2", "S4-3", "RPT"]}
STUB_CAUSE = {"K6": _ABS_K, "K7": _ABS_K, "K8": _ABS_K, "RPT": _ABS_K,
              **{k: _ABS for k in ("S4-1", "S4-2", "S4-3")}}
SOURCES = {
    "S4-1": "stop.collar_top_z DERIVED; tests/test_params_bom.py l.694-702 (test_P18); gameplan detail 1.4 S4-1",
    "S4-2": "[CP §9, Q4]; Sean STOP S4-A, Design Notes 34 (short-core exposure and grip, advance D with carrier C); Designer 1.4 (a) section 6",
    "S4-3": "ASSEMBLY.md; critical-path 7.1 (backcap failure); Designer 1.4 (a) section 12; S4-d (Design Notes 34)",
}

CHECKS = [("S4-1", s4_1), ("S4-2", s4_2), ("S4-3", s4_3)]


def run(ctx):
    return [_run(cid, fn, ctx) for cid, fn in CHECKS]
