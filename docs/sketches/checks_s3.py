"""S3 checks S3-1 to S3-3 (contributor gameplan (sean) detail 1.3 table; Design Notes 4 and 31).
Skeleton written at 1.3 (b) from the spec blocks s3_checks, load_cases and chains; drawn readers and S3-3's cross-record
reader landed at 1.3 (c) (P4). The arithmetic (load cases, F_stall, P_cr, critical speed, back-drive) feeds reported(ctx)
for RPT. The checks read drawn patches located by gid in the section Axes (sketch_common.axes_context, TP-7: the Axes
declared `section`, u = +Y, depth along X) and fail closed (cause "absent") when a part they need is not drawn, so they
are red on the floor-only stub. Heights z_A from check_stack unless stated.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import check_stack  # noqa: E402
import sketch_common as sc  # noqa: E402

K_CHECKS = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9"]
SECTION_AXES = "section"
C_STATES = ("C", "z-contact", "plan-contact")   # K7 pass states of a class C pair (side, plan)


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


def _section(ctx):
    """The section Axes sub-context (TP-7); its stack is in the reflected section frame (x' = u = plan y)."""
    c = sc.axes_context(ctx, SECTION_AXES)
    if c is None:
        raise Content(f"spec declares no Axes {SECTION_AXES}")
    return c


def _ax(ctx):
    pose = _fig_pose(ctx)
    c = _section(ctx)
    if pose not in c.figs:
        raise Absent(f"section Axes absent from figure {pose}")
    return c.figs[pose].axes[0], pose


def _pieces(ctx, fid):
    ax, _ = _ax(ctx)
    p = sc.pieces(ax, fid)
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


# ---------------------------------------------------------------- drawn readers

def anchor_line_z(ctx, fid):
    """z_S of the drawn bearing line <fid>:line (the mark sub-artist; K5 M1 to M5 hold it to mark.z and the part)."""
    ax, _ = _ax(ctx)
    arts = sc.tagged(ax).get(f"{fid}:{sc.MARK_SUB}", [])
    if not arts:
        raise Absent(f"{fid}:{sc.MARK_SUB} (bearing line) not drawn")
    pts = [p for a in arts for p in sc.artist_polys(a)[0]]
    return sum(z for _, z in pts) / len(pts)


# ---------------------------------------------------------------- checks

def s3_1(ctx):
    """Sign: the screw segment from the nut down to the anchor bearing line is in tension in the cut case at every nut
    position from the S1 poses: the drawn bearing line (anchor_bearing_c:line) below the nut bottom (check_stack nut_z per
    pose) and the drawn cut arrow pointing +Z (K8 points form)."""
    c = _cfg(ctx, "S3-1")
    ax, _ = _ax(ctx)
    _pieces(ctx, c["load_arrow"])
    z_line = anchor_line_z(ctx, c["anchor_line"])
    issues, worst = [], None
    for t in sc.points_issues(ax, c["load_arrow"], "+Z"):
        issues.append(f"cut arrow {c['load_arrow']}: {t}")
    for pose in c["nut_positions"]:
        nz = check_stack.to_shop_floor(ctx.stack["poses"][pose]["vars_z_A"]["nut_z"] - ctx.P.get("jackscrew.nut_length") / 2, ctx.P)
        m = nz - z_line
        worst = m if worst is None else min(worst, m)
        if m <= 0:
            issues.append(f"{pose}: nut bottom {nz:.2f} not above the anchor line {z_line:.2f} z_S (compression)")
    return sc.result("S3-1", not issues, sc._summ(issues) if issues else f"tension segment least {worst:.2f} mm (nut bottom above the anchor line in every pose; cut arrow +Z)",
                     measured=round(worst, 3), threshold=0, n_issues=len(issues))


def s3_2(ctx):
    """Buckling, floating nut: P_cr over the drawn anchor-to-guide bearing span, K jackscrew.end_factor_floating;
    P_cr / F >= jackscrew.buckling_sf in every case of s3_checks.S3-2 (Sean STOP S3-A, Design Notes 31). The drawn span
    (centres of the drawn bearing rows in the section Axes) must equal the spec expression within 0.05."""
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


def _records(ctx):
    """{sketch: (path, record, stale diffs)} for the latest accepted, unsuperseded record of each sketch in the records
    directory (check_sketch.stale_records; ctx.records_dir, default docs/sketches/). A record whose keys_read differ
    from the live params and overlay is stale and certifies nothing (premise of S3-3, checked here)."""
    import check_sketch as cs   # lazy: check_sketch loads this module by path
    docs = Path(getattr(ctx, "records_dir", None) or HERE)
    wip = Path(getattr(ctx, "wip_dir", None) or (docs / "wip"))
    out = {}
    for p, rec in cs.stale_records(docs, wip):
        out[rec.get("sketch", Path(p).name.split("_")[0]).upper()] = (Path(p), rec, cs.stale_diffs(ctx.P, [(p, rec)]))
    return out


def _k7_tests(rec):
    k7 = next((c for c in rec.get("checks", []) if c.get("id") == "K7"), None) or {}
    f = k7.get("test_fields") or sc.K7_TEST_FIELDS
    return [dict(zip(f, t)) for t in (k7.get("tests") or [])]


def _pair_ok(tests, x, y, pose):
    """(found, ok, states) for the pair x|y (either order) at pose in K7 test entries."""
    st = [t["state"] for t in tests if t.get("pose") == pose and t.get("pair") in (f"{x}|{y}", f"{y}|{x}")]
    return bool(st), bool(st) and all(s in C_STATES for s in st), st


def _face_issue(ctx, sec, ax, pose, x, y, face):
    """The named face of an S3 certifier (s3_spec chains field face, or the neighbour entry's face z): the drawn pieces of
    x and y each have a horizontal edge at the face z (z_A expression, or the expression in the text before ',') within
    TOL_Z, overlapping in u: the axial face that carries the cut-case load."""
    expr = face.get("z") if isinstance(face, dict) else None
    if expr is None:
        return None
    names = ctx.stack["poses"][pose]["vars_z_A"]
    z = check_stack.to_shop_floor(check_stack.eval_expr(expr, ctx.P, names), ctx.P)
    spans = []
    for fid in (x, y):
        ss = []
        for P in sc.pieces(ax, fid):
            for i in range(len(P)):
                a, b = P[i], P[(i + 1) % len(P)]
                if abs(a[1] - b[1]) <= sc.TOL_Z and abs(a[1] - z) <= sc.TOL_Z:
                    ss.append((min(a[0], b[0]), max(a[0], b[0])))
        spans.append(ss)
    if not spans[0] or not spans[1]:
        return f"no horizontal edge of {x if not spans[0] else y} at the face z {z:.2f} z_S ({expr})"
    if not any(min(a1, b1) - max(a0, b0) > -sc.TOL_Z for a0, a1 in spans[0] for b0, b1 in spans[1]):
        return f"faces of {x} and {y} at z {z:.2f} do not overlap in u"
    return None


def _face_of(ctx, link, x, y):
    """The face a link names: a neighbour entry's face {z} (row x or y), else none (the chain text is descriptive)."""
    rows = {r["id"]: r for r in ctx.spec.get("features", [])}
    for a, b in ((x, y), (y, x)):
        for nb in (rows.get(a, {}).get("neighbours") or []):
            if nb.get("id") == b and isinstance(nb.get("face"), dict):
                return nb["face"]
    if isinstance(link.get("face"), dict):
        return link["face"]
    return None


def s3_3(ctx):
    """Axial loop closed in the cut case (spec chains, 1.3 open O11): every consecutive pair of each screw chain is class
    C in at least one certifier named for it: a record certifier "S1 a|b" or "S2 a|b" reads the K7 entries (pose of the
    section figure) of the latest accepted record of that sketch, which must not be stale (a stale record certifies
    nothing); "S3 a|b" reads this run's K7 entries in the section Axes, and a link that names a face (neighbour face z)
    has the two drawn pieces meeting on a horizontal edge at that z; an S3 certifier whose test fails opens the link (the
    drawing contradicts the record); "declared ..." passes as declared and is listed; "none" certifies nothing, except a,
    b links certified by symmetry from the c chain under SYM (check_sketch.sym_lint) when every c link between the two
    rows' c counterparts passes."""
    c = _cfg(ctx, "S3-3")
    chains = ctx.spec.get("chains") or {}
    if not chains:
        raise Content("spec has no chains")
    ax, pose = _ax(ctx)
    for f in ("anchor_c", "anchor_bearing_c", "screw_c", "nut_c", "nut_housing_c", "ring"):
        _pieces(ctx, f)
    sec = _section(ctx)
    k7 = sc.k7(sec)
    s3_tests = [dict(zip(k7.get("test_fields") or sc.K7_TEST_FIELDS, t)) for t in (k7.get("tests") or [])]
    recs = _records(ctx)
    import check_sketch as cs
    sym = cs.sym_lint(getattr(ctx, "specs", None))
    issues, listed, n = [], [], 0
    passed = {}
    for ch in sorted(chains, key=lambda k: (k != "c", k)):
        for i, link in enumerate(chains[ch]):
            x, y = link["pair"]
            n += 1
            ok, why, veto, decl = False, [], None, False
            for cert in link.get("certifiers") or []:
                w = str(cert).split()
                head = w[0] if w else ""
                if head in ("S1", "S2"):
                    if head not in recs:
                        why.append(f"{head}: no accepted record")
                        continue
                    p, rec, diffs = recs[head]
                    if diffs:
                        why.append(f"{head} {p.name} stale ({len(diffs)} key(s), e.g. {diffs[0].split(': ', 1)[-1]})")
                        continue
                    found, good, st = _pair_ok(_k7_tests(rec), x, y, pose)
                    if not found:
                        why.append(f"{head} {p.name}: pair absent")
                    elif good:
                        ok = True
                    else:
                        why.append(f"{head} {p.name}: states {sorted(set(st))}")
                elif head == "S3":
                    found, good, st = _pair_ok(s3_tests, x, y, pose)
                    face = _face_of(ctx, link, x, y)
                    fi = _face_issue(ctx, sec, ax, pose, x, y, face) if face and found and good else None
                    if not found:
                        why.append("S3: pair not tested in the section")
                    elif not good:
                        veto = f"S3 section K7 states {sorted(set(st))}"
                    elif fi:
                        veto = f"S3 face: {fi}"
                    else:
                        ok = True
                elif head.startswith("declared"):
                    decl = True
                elif head == "none":
                    why.append("none")
            if not ok and decl:
                ok = True
                listed.append(f"{ch} {x}|{y} declared")
            if not ok and ch in ("a", "b") and [str(q).split()[0] for q in link.get("certifiers") or []] == ["none"]:
                xc, yc = (v[:-2] + "_c" if v.endswith(f"_{ch}") else v for v in (x, y))
                cids = [tuple(l["pair"]) for l in chains.get("c", [])]
                seq = [v for pr in cids for v in pr]
                if xc in seq and yc in seq and sym["result"] == "pass":
                    i0, i1 = sorted((seq.index(xc) // 2, (len(seq) - 1 - seq[::-1].index(yc)) // 2))
                    if all(passed.get(("c", j)) for j in range(i0, i1 + 1)):
                        ok = True
                        listed.append(f"{ch} {x}|{y} by symmetry from c")
                    else:
                        why.append("symmetry: a c link between the counterparts is open")
                elif sym["result"] != "pass":
                    why.append(f"symmetry premise (SYM) fails: {sym['n_issues']} issue(s)")
            if veto:
                ok = False
                why.append(veto)
            passed[(ch, i)] = ok
            if not ok:
                issues.append(f"chain {ch}: {x}|{y} not certified ({'; '.join(why) or 'no certifier'})")
    return sc.result("S3-3", not issues, sc._summ(issues) if issues else
                     f"{n} chain link(s) closed in the cut case; listed: {'; '.join(listed) or 'none'}",
                     measured=len(issues), threshold=0, n_issues=len(issues), listed=listed)


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
        z_line = check_stack.from_shop_floor(anchor_line_z(ctx, "anchor_bearing_c"), P)
        items["tension_segment"] = {"value": "; ".join(f"{p} {stack['poses'][p]['vars_z_A']['nut_z'] - z_line:.2f}" for p in ("load", "start", "capture_end", "park")),
                                    "basis": "nut centre per pose (check_stack) - drawn anchor bearing line anchor_bearing_c:line", "tag": "MEASURED"}
    except (Absent, Content):
        items["tension_segment"] = {"value": None, "basis": "anchor_bearing_c:line not drawn", "tag": None}
    for k, v in items.items():
        rows.append((k, v["value"], v["basis"]))
    return {"id": "reported", "result": "pass", "rows": rows, "items": items}


# Per-sketch tables (check_sketch.sketch_table). Every S3 check reads drawn patches and fails closed (absent) on the
# floor-only stub; the content evidence is the S3-x B fixtures in run 1 (1.3 (c)).
_ABS = ("absent", "red (absent, fail-closed; content evidence run 1, S3-x B fixtures 1.3 (c))")
_ABS_K = ("absent", "red (absent, fail-closed; content evidence run 1)")
STUB_EXPECT = {"guard": ["K1", "K2", "K3", "K5", "X1"],
               "red": ["K4", "K6", "K7", "K8", "K9", "S3-1", "S3-2", "S3-3", "RPT", "SYM"]}
STUB_CAUSE = {"K6": _ABS_K, "K7": _ABS_K, "RPT": _ABS_K,
              "K8": ("content", "red (content: spec error motor_shaft_c outboard frame radial in the section, P4 finding F3; every other K8 issue absent)"),
              **{k: _ABS for k in ("S3-1", "S3-2", "S3-3")},
              "SYM": ("content", "red (content: S3 anchor rows carry x1_exempt and the a/b key lists differ from c; clears at P6, S1 r8 / S2 r9)")}
SOURCES = {
    "S3-1": "[DN23]; gameplan detail 1.3 S3-1",
    "S3-2": "[DN23]; Design Notes 31 (SF 3 every case, K 0.7 on L_t, F_bind 300 N); E, d_r, mu, masses ASSUMED",
    "S3-3": "SE-2; gameplan detail 1.3 S3-3; 1.3 open O11 (cross-record); Designer 1.3 (a) section 11",
}

CHECKS = [("S3-1", s3_1), ("S3-2", s3_2), ("S3-3", s3_3)]


def run(ctx):
    return [_run(cid, fn, ctx) for cid, fn in CHECKS]
