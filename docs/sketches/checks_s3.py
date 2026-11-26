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


LINK_KINDS = ("face", "face_record", "thread", "one_body", "fastened", "declared")   # 1.3 (h) r2 (Topologist TP1.3-10)


def _face_issue(ctx, sec, ax, pose, x, y, face, sense=False):
    """The named face of an S3 certifier (s3_spec chains field face, or the neighbour entry's face z): the drawn pieces of
    x and y each have a horizontal edge at the face z (z_A expression, or the expression in the text before ',') within
    TOL_Z, overlapping in u: the axial face that carries the cut-case load. sense (1.3 (h) r2, Topologist TP1.3-10, a
    link of kind face written x -> y in chain order): the edge of x is a bottom edge of a drawn piece of x (the piece
    lies above the face) and the edge of y a top edge of a piece of y (below it), so x holds y down under the cut-case
    loop force (-Z of x on y); a face with x below it is loaded in tension and opens."""
    expr = face.get("z") if isinstance(face, dict) else None
    if expr is None:
        return None
    names = ctx.stack["poses"][pose]["vars_z_A"]
    z = check_stack.to_shop_floor(check_stack.eval_expr(expr, ctx.P, names), ctx.P)
    spans = []
    for k, fid in enumerate((x, y)):
        ss = []
        for P in sc.pieces(ax, fid):
            zmid = sum(sc.extent_z([P])) / 2
            for i in range(len(P)):
                a, b = P[i], P[(i + 1) % len(P)]
                if abs(a[1] - b[1]) <= sc.TOL_Z and abs(a[1] - z) <= sc.TOL_Z:
                    if sense and ((k == 0 and zmid < z) or (k == 1 and zmid > z)):
                        continue   # x's piece must lie above the face, y's below it
                    ss.append((min(a[0], b[0]), max(a[0], b[0])))
        spans.append(ss)
    if not spans[0] or not spans[1]:
        what = "bottom " if sense and not spans[0] else ("top " if sense else "")
        return (f"no {what}horizontal edge of {x if not spans[0] else y} at the face z {z:.2f} z_S ({expr})"
                + (f"; {x} must lie above the face and {y} below it (cut-case sense)" if sense else ""))
    if not any(min(a1, b1) - max(a0, b0) > sc.TOL_Z for a0, a1 in spans[0] for b0, b1 in spans[1]):   # P5f (LF FIX 2)
        return f"faces of {x} and {y} at z {z:.2f} overlap by no more than {sc.TOL_Z} in u (a corner is no axial seat)"
    return None


def link_kind_issues(chains):
    """1.3 (h) r2 (Topologist TP1.3-10): spec lint. Every chain link has a kind in LINK_KINDS; a face link names a face
    {z} on the link (or on the neighbour entry, read by _face_of) and has an S3 certifier, except an a / b link certified
    by symmetry from c (certifiers ["none"]), whose c counterparts carry the faces."""
    out = []
    for ch, lst in (chains or {}).items():
        for link in lst:
            k = link.get("kind")
            x, y = link["pair"]
            heads = [str(q).split()[0] for q in link.get("certifiers") or [] if str(q).split()]
            if k not in LINK_KINDS:
                out.append(f"chain {ch}: {x}|{y} spec error, link kind {k!r} (one of {', '.join(LINK_KINDS)})")
            elif k == "face" and "S3" not in heads and not (ch in ("a", "b") and heads == ["none"]):
                out.append(f"chain {ch}: {x}|{y} spec error, face link with no S3 certifier (the sense is read in the section only)")
    return out


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


def true_cut_issues(ctx):
    """P5f (Loftsman FIX 3): premise of the veto. Every row of a pair an S3 certifier names is drawn as its true cut
    through x = 0: it carries section_u or section, or is an axis-Z round row whose depth band is symmetric about x = 0,
    or has a place footprint centred on x = 0 (|r_c cos theta| <= TOL_Z) and symmetric about it (round, or radial at
    theta 90 or 270 with rot 0). Otherwise a spec error."""
    rows = {r["id"]: r for r in ctx.spec.get("features", [])}
    pose = (ctx.spec.get("section_figure") or {}).get("pose", "capture_end")
    feats = ctx.stack["poses"][pose]["features"]
    named = set()
    for lst in (ctx.spec.get("chains") or {}).values():
        for link in lst:
            if any(str(q).split()[:1] == ["S3"] for q in link.get("certifiers") or []):
                named.update(link["pair"])
    out = []
    for fid in sorted(named):
        r, f = rows.get(fid, {}), feats.get(fid, {})
        if r.get("section_u") or r.get("section"):
            continue
        dep = f.get("depth")
        if r.get("kind") in sc.ROUND_KINDS and r.get("axis") == "Z" and not r.get("place") and dep and abs(dep[0] + dep[1]) <= sc.TOL_Z:
            continue
        pl = f.get("place")
        if pl:
            th = pl["theta"] % 360
            centred = abs(pl["r_c"] * math.cos(math.radians(pl["theta"]))) <= sc.TOL_Z
            sym = pl["footprint"] == "round" or (pl["footprint"] == "radial" and min(abs(th - 90), abs(th - 270)) <= 1e-6 and abs(pl.get("rot", 0)) <= 1e-9)
            if centred and sym:
                continue
        out.append(f"{fid}: spec error, row of an S3-certified pair not drawn as its true cut through x = 0 (veto premise)")
    return out


def _c_range(chains, xc, yc):
    """P5f (Loftsman NOTE 1): the c links between the c counterparts of a link's rows, p(x_c) to p(y_c) - 1 along the
    rows of chain c."""
    rows = [l["pair"][0] for l in chains["c"]] + [chains["c"][-1]["pair"][1]]
    if xc not in rows or yc not in rows:
        return None
    i, j = sorted((rows.index(xc), rows.index(yc)))
    return list(range(i, j))


def s3_3(ctx):
    """Axial loop closed in the cut case (spec chains, 1.3 open O11): every consecutive pair of each screw chain is class
    C in at least one certifier named for it: a record certifier "S1 a|b" or "S2 a|b" reads the K7 entries (pose of the
    section figure) of the latest accepted record of that sketch, which must not be stale (a stale record certifies
    nothing); "S3 a|b" reads this run's K7 entries in the section Axes, and a link that names a face (neighbour face z)
    has the two drawn pieces meeting on a horizontal edge at that z; an S3 certifier whose test fails opens the link (the
    drawing contradicts the record); "declared ..." passes as declared and is listed; "none" certifies nothing, except a,
    b links certified by symmetry from the c chain under SYM (check_sketch.sym_lint) when every c link between the two
    rows' c counterparts passes. P5f: the S3 verdict is per pair (a failing section test opens the pair in every chain),
    a named face needs an overlap in u above TOL_Z, the veto premise is linted (true_cut_issues), the symmetry range is
    p(x_c) to p(y_c) - 1 along chain c. 1.3 (h) r2 (Topologist TP1.3-10): every link has a kind (link_kind_issues); an S3
    certifier of a face link reads the face with its sense (x above the face, y below: compression under the cut-case
    loop force); fastened, face_record and declared links are listed."""
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
    issues, listed, n = list(true_cut_issues(ctx)) + link_kind_issues(chains), [], 0
    passed = {}
    # P5f (Loftsman FIX 1): the S3 verdict is per pair. A pair any link certifies with "S3 x|y" is judged once by the
    # section (K7 state, named face); a failing verdict opens that pair in every chain where it occurs.
    s3v = {}
    for lst in chains.values():
        for link in lst:
            if not any(str(q).split()[:1] == ["S3"] for q in link.get("certifiers") or []):
                continue
            x, y = link["pair"]
            key = frozenset((x, y))
            found, good, st = _pair_ok(s3_tests, x, y, pose)
            face = _face_of(ctx, link, x, y)
            kface = link.get("kind") == "face"
            if kface and not face:
                s3v[frozenset((x, y))] = ("fail", f"S3 face link names no face z ({x} -> {y})")
                continue
            fi = _face_issue(ctx, sec, ax, pose, x, y, face, sense=kface) if face and found and good else None
            v = ("absent", "S3: pair not tested in the section") if not found else (
                ("fail", f"S3 section K7 states {sorted(set(st))}") if not good else (("fail", f"S3 face: {fi}") if fi else ("pass", None)))
            if key not in s3v or v[0] == "fail":
                s3v[key] = v
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
                    v = s3v.get(frozenset((x, y)))
                    if v and v[0] == "pass":
                        ok = True
                    elif v and v[0] == "absent":
                        why.append(v[1])
                elif head.startswith("declared"):
                    decl = True
                elif head == "none":
                    why.append("none")
            v = s3v.get(frozenset((x, y)))
            if v and v[0] == "fail":   # P5f (LF FIX 1): veto per pair, in every chain
                veto = v[1]
            kind = link.get("kind")
            if kind == "declared":   # 1.3 (h) r2 (TP1.3-10): load application, radial fits with S6-5 seats
                decl = True
            if not ok and decl:
                ok = True
                listed.append(f"{ch} {x}|{y} declared")
            elif ok and kind in ("fastened", "face_record", "declared"):
                listed.append(f"{ch} {x}|{y} {kind}")
            if not ok and ch in ("a", "b") and [str(q).split()[0] for q in link.get("certifiers") or []] == ["none"]:
                xc, yc = (v[:-2] + "_c" if v.endswith(f"_{ch}") else v for v in (x, y))
                rng = _c_range(chains, xc, yc) if "c" in chains else None
                if rng is not None and sym["result"] == "pass":
                    if all(passed.get(("c", j)) for j in rng):
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
    try:   # 1.3 (h) r2 (Loftsman LF1.3-1, gameplan detail 1.3 Reported): drawn bar and the shoulder-screw head, from the drawing
        zb = lambda fid: sc.extent_z(_pieces(ctx, fid))  # noqa: E731
        bar = zb("guide_c")[1] - zb("screw_end_c")[0]
        head = zb("nut_screws_c")[1] - zb("nut_housing_c")[1]
        with_head = "; ".join(f"{k}: " + ", ".join(f"{lk} {check_stack.report_value(v) + head:.2f}" for lk, v in o["L"].items()
                                                  if isinstance(check_stack.report_value(v), float))
                              for k, o in rep["q9_options"].items())
        items["L_min"]["value"] += (f"; drawn bar {bar:.2f} (screw_end_c bottom to guide_c top); with the shoulder-screw head "
                                    f"{head:.2f} above the housing top: {with_head}")
        items["L_min"]["basis"] += "; drawn pieces screw_end_c, guide_c, nut_screws_c, nut_housing_c (section Axes, MEASURED)"
    except (Absent, Content):
        items["L_min"]["value"] += "; drawn bar: not drawn"
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
# 1.3 P6: F3 landed (motor_shaft_c outboard in the side form), so the stub K8 reads absent; the S3 anchor exemptions are
# gone, so SYM (a spec lint, no drawing) is a guard on the stub.
STUB_EXPECT = {"guard": ["K1", "K2", "K3", "K5", "X1", "SYM-P", "SYM"],
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
