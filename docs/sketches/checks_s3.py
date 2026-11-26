"""S3 checks S3-1 to S3-3 (contributor gameplan (sean) detail 1.3 table; Design Notes 4 and 31).
Skeleton written at 1.3 (b) from the spec blocks s3_checks, load_cases and chains. The arithmetic (load cases, F_stall,
P_cr, critical speed, back-drive) is complete and feeds reported(ctx) for RPT; the checks read drawn patches located by
gid in the section Axes and fail closed (cause "absent") when a part they need is not drawn, so they are red on the
floor-only stub. The section-view readers (u = +Y, depth along X) and S3-3's cross-record reader land at 1.3 (c) (P4) with
the S3-x fixtures; until then S3-3 fails closed. Heights z_A from check_stack unless stated.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402

K_CHECKS = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9"]


class Absent(Exception):
    pass


class Content(Exception):
    pass


def _cfg(ctx, cid):
    c = (ctx.spec.get("s3_checks") or {}).get(cid)
    if not c:
        raise Content(f"spec s3_checks has no {cid} block")
    return c


def _fig_pose(ctx):
    pf = (ctx.spec.get("section_figure") or {}).get("pose", "capture_end")
    if not ctx.figs or pf not in ctx.figs:
        raise Absent(f"section figure (pose {pf}) not built")
    return pf


def _pieces(ctx, fid):
    pose = _fig_pose(ctx)
    p = sc.pieces(ctx.figs[pose].axes[0], fid)   # P4 (TP-7): the section Axes by declaration, not axes[0]
    if not p:
        raise Absent(f"{fid} not drawn")
    return p


def _run(cid, fn, ctx):
    try:
        return fn(ctx)
    except Absent as e:
        return sc.result(cid, False, f"measured: none; {e}", cause="absent")
    except Content as e:
        return sc.result(cid, False, str(e), cause="content")


# ---------------------------------------------------------------- arithmetic from the keys (no drawing)

def loads(P, spec):
    """Load cases, F_stall, eta and thread angles from the overlay (spec load_cases, s3_checks.S3-2). Forces in N."""
    lc = spec["load_cases"]
    g = float(lc["g"])
    W_kg = check_stack.eval_expr(lc["W_kg"], P, {})
    W = W_kg * g
    c2 = spec["s3_checks"]["S3-2"]
    st = c2["stall"]
    lead, starts = P.get(st["lead"]), P.get(st["starts"])
    d2 = P.get(st["mean_diameter"])
    lam = math.atan(lead / (math.pi * d2))
    half = math.radians(P.get(st["half_angle"]))
    T = P.get(st["torque"])
    mus = list(P.get(st["mu"]))
    thread = {}
    for mu in mus:
        phin = math.atan(mu / math.cos(half))
        eta = math.tan(lam) / math.tan(lam + phin)
        thread[mu] = {"phi_n_deg": math.degrees(phin), "eta": eta, "F_stall_per_screw": 2 * math.pi * T * eta / (lead / 1000.0),
                      "eta_back": math.tan(lam - phin) / math.tan(lam)}
    n = P.get("jackscrew.count")
    fst = max(v["F_stall_per_screw"] for v in thread.values())     # governing: low mu (largest stall thrust)
    core = P.get(c2["core_mass"]) * g    # liftload.core_mass_capture (P2f, Designer 1.3 (b) section 7 item 9)
    per = {"static": W / n, "capture_lift": (W + core) / n, "retract_bind": min((W + P.get("liftload.f_bind")) / n, fst),
           "cut": (P.get("loads.axial_design") - W) / n, "stall_up": fst}
    two = {k: v * n / 2 for k, v in per.items() if k != "stall_up"}
    return {"W_kg": W_kg, "W": W, "lambda_deg": math.degrees(lam), "thread": thread, "per_screw": per, "two_screw": two,
            "F_stall_max": fst, "lead": lead, "starts": starts, "T": T, "n": n}


def euler(P, spec, L, K):
    d = P.get(spec["s3_checks"]["S3-2"]["d_r"])
    E = P.get(spec["s3_checks"]["S3-2"]["E"])
    I = math.pi * d ** 4 / 64
    return math.pi ** 2 * E * I / (K * L) ** 2, I


def spans(P, spec, stack):
    """L_t from the spec expression and the rigid-nut segment at park (nut centre at park - anchor bearing line)."""
    c2 = spec["s3_checks"]["S3-2"]
    Lt = check_stack.eval_expr(c2["column"]["length"], P, {})
    nut_park = check_stack.from_shop_floor(stack["poses"]["park"]["features"]["nut_station_park"]["z_min"], P)
    seg = nut_park - P.get("jackscrew.anchor_bearing_z")
    return Lt, seg


def critical_speed(P, Lt):
    d = P.get("jackscrew.root_diameter")
    E = P.get("jackscrew.youngs_modulus") * 1e3          # N/mm2 -> kg/(mm s2)
    rho = P.get("jackscrew.density") * 1e-9              # kg/m3 -> kg/mm3
    I, A = math.pi * d ** 4 / 64, math.pi * d ** 2 / 4
    out = {}
    for name, beta in (("pinned-pinned", math.pi), ("fixed-pinned", 3.9266)):
        w = beta ** 2 / Lt ** 2 * math.sqrt(E * I / (rho * A))
        out[name] = w * 60 / (2 * math.pi)
    rpm = P.get("liftload.rapid_speed") / P.get("jackscrew.lead") * 60
    return out, rpm


# ---------------------------------------------------------------- checks

def s3_1(ctx):
    """Sign: the screw segment from the nut down to the anchor bearing line is in tension in the cut case at every nut
    position from the S1 poses: drawn bearing line below the nut bottom (check_stack nut_z per pose) and the drawn cut
    arrow pointing +Z. P4 (c) adds the section-view reader of the bearing line (anchor_bearing_c:line)."""
    c = _cfg(ctx, "S3-1")
    line = _pieces(ctx, c["anchor_line"])
    _pieces(ctx, c["load_arrow"])
    z_line = min(sc.extent_z(line))   # P4: the :line sub-artist's z, not the row extent
    issues, worst = [], None
    for pose in c["nut_positions"]:
        nz = check_stack.to_shop_floor(ctx.stack["poses"][pose]["vars_z_A"]["nut_z"] - ctx.P.get("jackscrew.nut_length") / 2, ctx.P)
        m = nz - z_line
        worst = m if worst is None else min(worst, m)
        if m <= 0:
            issues.append(f"{pose}: nut bottom {nz:.2f} not above the anchor line {z_line:.2f} z_S (compression)")
    return sc.result("S3-1", not issues, sc._summ(issues) if issues else f"tension segment least {worst:.2f} mm (nut bottom above the anchor line in every pose)",
                     measured=round(worst, 3), threshold=0, n_issues=len(issues))


def s3_2(ctx):
    """Buckling, floating nut: P_cr over the drawn anchor-to-guide bearing span, K jackscrew.end_factor_floating;
    P_cr / F >= jackscrew.buckling_sf in every case of s3_checks.S3-2 (Sean STOP S3-A, Design Notes 31). The drawn span
    must equal the spec expression within 0.05 (P4: bearing-line readers in the section Axes)."""
    c = _cfg(ctx, "S3-2")
    a = _pieces(ctx, c["column"]["from"])
    b = _pieces(ctx, c["column"]["to"])
    za, zb = sum(sc.extent_z(a)) / 2, sum(sc.extent_z(b)) / 2
    L_drawn = zb - za
    L_spec = check_stack.eval_expr(c["column"]["length"], ctx.P, {})
    issues = []
    if abs(L_drawn - L_spec) > sc.TOL_Z:
        issues.append(f"drawn span {L_drawn:.2f} against {L_spec:.2f} (spec)")
    ld = loads(ctx.P, ctx.spec)
    K = ctx.P.get(c["column"]["K"])
    Pcr, _ = euler(ctx.P, ctx.spec, L_spec, K)
    sf = ctx.P.get(c["sf"])
    margins = {k: Pcr / ld["per_screw"][k] for k in c["cases"]}
    for k, m in margins.items():
        if m < sf:
            issues.append(f"{k}: P_cr {Pcr:.1f} / {ld['per_screw'][k]:.2f} = {m:.2f} < SF {sf}")
    least = min(margins.values())
    return sc.result("S3-2", not issues, sc._summ(issues) if issues else
                     f"P_cr {Pcr:.1f} N (K {K}, L_t {L_spec:.2f}); least margin {least:.2f} ({min(margins, key=margins.get)}) against SF {sf}",
                     measured=round(least, 3), threshold=sf, n_issues=len(issues))


def s3_3(ctx):
    """Axial loop closed in the cut case (spec chains): every consecutive pair class C in a certifying record (latest
    accepted S1 and S2 records, --stale clean, and this run's K7). Cross-record reader: P4 (c). Fails closed until then."""
    _cfg(ctx, "S3-3")
    for f in ("anchor_c", "anchor_bearing_c", "screw_c", "nut_c", "nut_housing_c", "ring"):
        _pieces(ctx, f)
    raise Content("S3-3 cross-record reader not written (1.3 (c), P4); fail-closed skeleton")


# ---------------------------------------------------------------- reported (RPT items; no threshold, never asserted)

def reported(ctx):
    P, spec, stack = ctx.P, ctx.spec, ctx.stack
    ld = loads(P, spec)
    Lt, seg = spans(P, spec, stack)
    c2 = spec["s3_checks"]["S3-2"]
    Kf, Kr = P.get(c2["column"]["K"]), P.get(c2["alternative"]["K"])
    rows, items = [], {}
    rep = check_stack.reported(P, spec, stack)
    items["L_min"] = {"value": "; ".join(f"{k}: " + ", ".join(f"{lk} {check_stack.report_value(v):.2f}" if isinstance(check_stack.report_value(v), float) else f"{lk} {v}" for lk, v in o["L"].items())
                                         for k, o in rep["q9_options"].items()) + " (DN23 800 to 900)",
                      "basis": "check_stack.reported q9_options, spec screw_length (S1 expressions)", "tag": "DERIVED"}
    ncs, rpm = critical_speed(P, Lt)
    items["n_crit"] = {"value": ", ".join(f"{k} {v:.0f} rpm ({v / rpm:.2f} x)" for k, v in ncs.items()) + f" against {rpm:.0f} rpm at {P.get('liftload.rapid_speed'):g} mm/s",
                       "basis": f"L_t {Lt:.2f}, d_r {P.get('jackscrew.root_diameter')}, E, density; fixed-pinned is the drawn end condition (K 0.7)", "tag": "DERIVED"}
    out = []
    for lab, K, L in (("floating", Kf, Lt), ("floating K 1.0", 1.0, Lt), ("rigid", Kr, seg), ("rigid K 1.0", 1.0, seg)):
        Pcr, _ = euler(P, spec, L, K)
        per = ", ".join(f"{k} {Pcr / ld['per_screw'][k]:.2f}" for k in c2["cases"])
        two = ", ".join(f"{k} {Pcr / ld['two_screw'][k]:.2f}" for k in c2["cases"] if k in ld["two_screw"])
        out.append(f"{lab} (K {K}, L {L:.2f}, P_cr {Pcr:.1f} N): per screw {per}; two-screw {two}")
    items["pcr_margin"] = {"value": " | ".join(out), "basis": "Euler, I = pi d_r^4 / 64; per-screw forces from load_cases", "tag": "DERIVED"}
    th = ld["thread"]
    items["f_stall"] = {"value": "; ".join(f"mu {mu}: {v['F_stall_per_screw']:.2f} per screw, {ld['n'] * v['F_stall_per_screw']:.2f} total, both directions" for mu, v in th.items()),
                        "basis": "2 pi T eta / lead, eta over jackscrew.thread_mu", "tag": "DERIVED"}
    items["wob_max"] = {"value": "; ".join(f"mu {mu}: {ld['n'] * v['F_stall_per_screw'] + ld['W']:.2f} N" for mu, v in th.items()) + f" against {P.get('loads.axial_design'):g} N",
                        "basis": f"F_stall total + W ({ld['W_kg']:.2f} kg, {ld['W']:.2f} N)", "tag": "DERIVED"}
    lead = ld["lead"] / 1000.0
    items["lift_torque"] = {"value": "; ".join(f"mu {mu}: cut {ld['per_screw']['cut'] * lead / (2 * math.pi * v['eta']):.3f}, capture lift {ld['per_screw']['capture_lift'] * lead / (2 * math.pi * v['eta']):.3f} N m" for mu, v in th.items()) + f" against {ld['T']} N m",
                            "basis": "T = F lead / (2 pi eta), per screw", "tag": "DERIVED"}
    items["kept_axial"] = {"value": f"{P.get('loads.axial_design'):g} N at the cut; " + "; ".join(f"mu {mu}: {ld['n'] * v['F_stall_per_screw'] + ld['W']:.2f} N at F_stall + W" for mu, v in th.items()) + " (collet, holder, receiver, base plate, compression)",
                           "basis": "loads.axial_design; F_stall + W (N5)", "tag": "DERIVED"}
    items["backdrive"] = {"value": f"lambda {ld['lambda_deg']:.2f} deg; " + "; ".join(f"mu {mu}: phi_n {v['phi_n_deg']:.2f} deg, back-drive efficiency {v['eta_back']:.3f} (self-locking)" if v["eta_back"] < 0 else f"mu {mu}: phi_n {v['phi_n_deg']:.2f} deg, back-drive efficiency {v['eta_back']:.3f} (back-drives)" for mu, v in th.items()),
                          "basis": "lambda = atan(lead / (pi d2)), phi_n = atan(mu / cos 15)", "tag": "DERIVED"}
    items["screw_share"] = {"value": "; ".join(f"{k} {v:.2f}" + (f" / {ld['two_screw'][k]:.2f}" if k in ld["two_screw"] else "") for k, v in ld["per_screw"].items()),
                            "basis": "per screw (load / 3) / two-screw (load / 2), N", "tag": "DERIVED"}
    try:
        line = _pieces(ctx, "anchor_bearing_c")
        z_line = check_stack.from_shop_floor(sum(sc.extent_z(line)) / 2, P)
        items["tension_segment"] = {"value": "; ".join(f"{p} {stack['poses'][p]['vars_z_A']['nut_z'] - z_line:.2f}" for p in ("load", "start", "capture_end", "park")),
                                    "basis": "nut centre per pose (check_stack) - drawn anchor bearing line (P4: anchor_bearing_c:line)", "tag": "MEASURED"}
    except Absent:
        items["tension_segment"] = {"value": None, "basis": "anchor_bearing_c not drawn", "tag": None}
    for k, v in items.items():
        rows.append((k, v["value"], v["basis"]))
    return {"id": "reported", "result": "pass", "rows": rows, "items": items}


# Per-sketch tables (check_sketch.sketch_table). Every S3 check reads drawn patches and fails closed (absent) on the
# floor-only stub; the content evidence is the S3-x B fixtures in run 1 (1.3 (c)).
_ABS = ("absent", "red (absent, fail-closed; content evidence run 1, S3-x B fixtures 1.3 (c))")
_ABS_K = ("absent", "red (absent, fail-closed; content evidence run 1)")
STUB_EXPECT = {"guard": ["K1", "K2", "K3", "K5", "X1"],
               "red": ["K4", "K6", "K7", "K8", "K9", "S3-1", "S3-2", "S3-3", "RPT"]}
STUB_CAUSE = {"K6": _ABS_K, "K7": _ABS_K, "K8": _ABS_K, "RPT": _ABS_K,
              **{k: _ABS for k in ("S3-1", "S3-2", "S3-3")}}
SOURCES = {
    "S3-1": "[DN23]; gameplan detail 1.3 S3-1",
    "S3-2": "[DN23]; Design Notes 31 (SF 3 every case, K 0.7 on L_t, F_bind 300 N); E, d_r, mu, masses ASSUMED",
    "S3-3": "SE-2; gameplan detail 1.3 S3-3; 1.3 open O11 (cross-record); Designer 1.3 (a) section 11",
}

CHECKS = [("S3-1", s3_1), ("S3-2", s3_2), ("S3-3", s3_3)]


def run(ctx):
    return [_run(cid, fn, ctx) for cid, fn in CHECKS]
