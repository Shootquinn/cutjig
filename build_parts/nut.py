"""Wing nut: internal 45/45 right-hand thread, washer pocket with press pads and anti-rotation tab, three windows,
two wings, four tommy bosses, release arrow. Local frame: skirt bottom at z = 0.
Step 6 rebuild (NT4, NT5, NT7): tighten glyph on the top face and loosen glyph on the underside of wing 0 (they replace the old +y radial mark,
and carry Rule P), dust skirt below the wings. NT9: no nut window (Loftsman C1, C2).
Step 7 rebuild (Loftsman Revision 1, V3): thread relief, a plain bore r nut.relief_r from nut.relief_z to the plate underside, in the final cut. The nut groove runs out
helically, so no full turn exists above nut z 42.5; the relief lets the plate underside meet the receiver rim at z0 40.0 and restores nut travel left at Kmax to 10.01."""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadlib as C  # noqa: E402
import step6lib as S  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "probes"))
import glyph_math  # noqa: E402  (pure python: principal-axis span and sense of a sampled recess)


def dims(p):
    g = lambda k: C.G(p, k)
    P = g("thread.pitch")
    h_wp = g("washer.thickness") - g("nut.washer_pocket_depth")
    q = {
        "P": P, "tanf": math.tan(math.radians(g("thread.flank_deg"))),
        "r_c": g("thread.minor") / 2 + g("fit.c_r"), "r_root": g("thread.major") / 2 + g("fit.c_r"),
        "r_pitch": (g("thread.major") - g("chain.h")) / 2, "r_body": g("wingnut.body_od") / 2,
        "H": g("nut.overall_height"), "z_pu": g("nut.length") + h_wp, "pd": g("nut.washer_pocket_depth"),
        "r_pk": g("nut.washer_pocket_od") / 2, "r_hole": g("nut.plate_hole_dia") / 2, "lead": g("thread.nut_lead_in_length"),
        "h_wp": h_wp,
    }
    tooth_pl = P / 2.0 - g("fit.g_a")                                    # nut tooth at the pitch line
    q["crest_flat"] = tooth_pl - 2.0 * (q["r_pitch"] - q["r_c"]) * q["tanf"]
    return q


def groove_hw(q, r):
    """Half-width of the nut groove at radius r (widest at the crest radius, narrowing outward)."""
    return (q["P"] - q["crest_flat"] - 2.0 * (r - q["r_c"]) * q["tanf"]) / 2.0


def wing_poly(g, q):
    root, tip = g("wingnut.wing_root_width"), g("wingnut.wing_tip_width")
    r_tip = g("wingnut.span") / 2
    x0 = q["r_body"] - 3.0
    H = q["H"]
    return [(x0, H), (q["r_body"], H), (r_tip, H - (root - tip) / 2.0), (r_tip, H - (root - tip) / 2.0 - tip),
            (q["r_body"], H - root), (x0, H - root)], r_tip


def glyph_xc(g, q):
    """Radial centre of the glyph: middle of the free wing band, from the dust skirt outer radius + 0.5 to the start of the tip fillet."""
    r_tip = g("wingnut.span") / 2
    return (g("nut.skirt_r_out") + 0.5 + r_tip - g("wingnut.edge_radius")) / 2.0


def glyph_tool(p, q, kind):
    """Recessed arrow on wing 0, normal to the wing face (Loftsman section 2). kind 'tighten' = top face (+z, sloped), 'loosen' = underside (-z).
    Local frame: x along the face slope, z along the outward normal, origin on the face at the radial centre. Tail at local a = +length/2.
    Top: local y is world +y, so tail y +3 to tip y -3 (clockwise from +Z at +X). Underside: local y is world -y, so tail y -3 to tip y +3 (counter-clockwise)."""
    import Part
    g = lambda k: C.G(p, k)
    gl, sw, hw, hl = g("nut.glyph_length"), g("nut.shaft_width"), g("nut.head_width"), g("nut.head_length")
    ov, ad = g("collet.tool_overshoot"), g("nut.arrow_depth")
    root, tip = g("wingnut.wing_root_width"), g("wingnut.wing_tip_width")
    r_tip = g("wingnut.span") / 2
    tanphi = ((root - tip) / 2.0) / (r_tip - q["r_body"])
    phi = math.atan(tanphi)
    xc = glyph_xc(g, q)
    a_sh = gl / 2 - (gl - hl)
    pts = [(-sw / 2, gl / 2), (sw / 2, gl / 2), (sw / 2, a_sh), (hw / 2, a_sh), (0.0, -gl / 2), (-hw / 2, a_sh), (-sw / 2, a_sh)]
    face = Part.Face(Part.makePolygon([C.V(c, a, 0.0) for c, a in pts] + [C.V(pts[0][0], pts[0][1], 0.0)]))
    sol = face.extrude(C.V(0, 0, -(ov + ad)))
    if kind == "tighten":
        zf = q["H"] - (xc - q["r_body"]) * tanphi
        u, n = C.V(math.cos(phi), 0, -math.sin(phi)), C.V(math.sin(phi), 0, math.cos(phi))
    else:
        zf = q["H"] - root + (xc - q["r_body"]) * tanphi
        u, n = C.V(math.cos(phi), 0, math.sin(phi)), C.V(math.sin(phi), 0, -math.cos(phi))
    origin = C.V(xc + n.x * ov, 0.0, zf + n.z * ov)
    return S.placed(sol, origin, u, n), {"xc": xc, "zf": zf, "n": n, "phi_deg": math.degrees(phi)}


def skirt_solid(p, q):
    """NT7 dust skirt: revolved (r, z) polygon from nut.skirt_*; embeds nut.skirt_embed into the body so the fuse shares volume."""
    g = lambda k: C.G(p, k)
    r_in, r_out = q["r_body"] - g("nut.skirt_embed"), g("nut.skirt_r_out")
    z_lo, z_hi, rim = g("nut.skirt_z_lo"), g("nut.skirt_z_hi"), g("nut.skirt_rim")
    return C.revolve_solid([(r_in, z_lo), (r_out, z_lo), (r_out, z_lo + rim), (q["r_body"], z_hi), (r_in, z_hi)])


def measure_glyph(piece, p, q, face, x0, x1, step=0.5):
    """Same sampling as tests/probes/probe_step6_marks.glyphs on the wing-0 face (+z or -z): x columns on the probe grid, y samples across the wing,
    a void is a surface at least nut.arrow_depth/2 below the unrecessed face level (column extreme). Returns glyph_math.analyze of the void points."""
    g = lambda k: C.G(p, k)
    depth = g("nut.arrow_depth")
    r_in = g("wingnut.body_od") / 2 + 3
    y_half = g("wingnut.wing_thickness") / 2 + step          # one sample beyond each wing face
    sign = 1.0 if face == "+z" else -1.0
    void = []
    i = 0
    while True:
        x = r_in + i * step
        i += 1
        if x < x0:
            continue
        if x > x1:
            break
        col = []
        for j in range(int(2 * y_half / step) + 1):
            y = -y_half + j * step
            iv = C.line_ivals(piece, C.V(x, y, -10.0), C.V(x, y, 90.0))
            if iv:
                col.append((y, -10.0 + (iv[-1][1] if sign > 0 else iv[0][0])))
        if not col:
            continue
        vals = sorted(v for _, v in col)
        med = vals[-1] if sign > 0 else vals[0]                 # unrecessed wing-face level of the column: the glyph covers more than half of the wing thickness, so the median would sit on the glyph floor
        for y, v in col:
            if sign * (med - v) >= depth / 2.0:
                void.append((x, y, v))
    return glyph_math.analyze(void) if len(void) >= 4 else {"count": len(void), "span": 0.0, "direction_sign": 0}


def build():
    t0 = time.time()
    import Part
    before = S.before_state("nut", S.BEFORE_DIR_7)
    p = C.params()
    g = lambda k: C.G(p, k)
    q = dims(p)
    th = g("receiver.key_offset_deg")
    P, H, z_pu, pd = q["P"], q["H"], q["z_pu"], q["pd"]
    # ---- base revolve
    pts = [(q["r_pitch"], 0), (q["r_body"], 0), (q["r_body"], H), (q["r_hole"], H), (q["r_hole"], z_pu + pd),
           (q["r_pk"], z_pu + pd), (q["r_pk"], z_pu), (q["r_c"], z_pu), (q["r_c"], q["lead"])]
    doc, body = C.new_body("nut")
    C.body_revolve(doc, body, pts, "Body")
    # ---- additive features (one combined fuse): pads, tab, wings, bosses
    fuse = []
    n_pad = g("nut.pad_count")
    pad_arc_deg = math.degrees(g("nut.pad_arc") / (g("nut.pad_id") / 2))
    for k in range(n_pad):
        fuse.append(C.sector_solid(g("nut.pad_id") / 2, q["r_pk"] + 0.3, z_pu, z_pu + pd, 360.0 / n_pad * k, pad_arc_deg))
    fuse.append(C.box_at(th, g("nut.tab_inner_radius"), q["r_pk"] + 0.3, g("nut.tab_width") / 2, z_pu, z_pu + pd))
    poly, r_tip = wing_poly(g, q)
    thick = g("wingnut.wing_thickness")
    for k in range(g("wingnut.wing_count")):
        w = Part.makePolygon([C.V(x, -thick / 2, z) for x, z in poly] + [C.V(poly[0][0], -thick / 2, poly[0][1])])
        sol = Part.Face(w).extrude(C.V(0, thick, 0))
        tip_edges = [e for e in sol.Edges if all(abs(v.Point.x - r_tip) < 1e-6 for v in e.Vertexes) and abs(e.Vertexes[0].Point.y - e.Vertexes[-1].Point.y) > 1.0]
        sol = sol.makeFillet(g("wingnut.edge_radius"), tip_edges)
        sol.rotate(C.V(0, 0, 0), C.V(0, 0, 1), 360.0 / g("wingnut.wing_count") * k)
        fuse.append(sol)
    n_t = g("nut.tommy_hole_count")
    z_ax = H - g("nut.tommy_hole_depth")
    r_end = g("nut.tommy_hole_bottom_r") + g("nut.tommy_hole_depth")
    t_deg = [360.0 / n_t * (k + 0.5) for k in range(n_t)]
    for a in t_deg:
        c = Part.makeCylinder(g("nut.tommy_boss_od") / 2, r_end - (q["r_body"] - 2.0), C.V(q["r_body"] - 2.0, 0, z_ax), C.V(1, 0, 0))
        c.rotate(C.V(0, 0, 0), C.V(0, 0, 1), a)
        fuse.append(c)
    skirt = skirt_solid(p, q)
    fuse.append(skirt)
    pre_base = C.final_shape(body)
    skirt_mm3 = skirt.cut(pre_base).Volume
    fuse_tool = C.fuse_all(fuse)
    C.body_boolean(doc, body, fuse_tool, "Fuse", "PadsTabWingsBossesSkirt")
    after_fuse = C.final_shape(body)
    bools = [{"name": "PadsTabWingsBossesSkirt", "kind": "fuse", "faces_before": len(pre_base.Faces), "faces_after": len(after_fuse.Faces),
              "tool_faces": len(fuse_tool.Faces)}]
    # ---- internal thread: stud-subtract (Orchestrator ruling, Step 4 fix pass). A male thread solid at the nut's fit dimensions
    # (45/45 helical ridge from r_in, inside the bore, out to r_root, right hand, pitch thread.pitch; the bore cylinder r_c is already in the body revolve) is cut from the body as a Part solid.
    # The native helical-groove feature it replaces produced helicoid faces whose booleans failed above 1.06 deg tilt (T9).
    # The ridge is quarter-turn segments, each four helices joined by ruled surfaces, fused (cadlib.thread_ridge_stud); no scaling is applied, so the pitch is exactly thread.pitch.
    hw_cap = g("thread.tool_groove_fraction") * P / 2.0
    ov = (hw_cap - groove_hw(q, q["r_c"])) / q["tanf"]
    r_in = q["r_c"] - ov                                               # inward overshoot keeps the ridge root below tool_groove_fraction x pitch
    hw_root = groove_hw(q, q["r_root"])
    z_start = -P                                                       # starts below the skirt: open end
    z_end = z_pu - groove_hw(q, q["r_c"])                              # groove top at the plate underside; thread ends here
    stud = C.thread_ridge_stud([(r_in, -hw_cap), (q["r_root"], -hw_root), (q["r_root"], hw_root), (r_in, hw_cap)], P, z_start, z_end)
    print("stud valid=%s volume=%.1f solids=%d" % (stud.isValid(), stud.Volume, len(stud.Solids)), flush=True)
    C.body_boolean(doc, body, stud, "Cut", "ThreadStud")
    after_stud = C.final_shape(body)
    bools.append({"name": "ThreadStud", "kind": "cut", "faces_before": len(after_fuse.Faces), "faces_after": len(after_stud.Faces)})
    # ---- subtractive features (one combined tool): windows, tommy holes, release arrow, wing mark
    cut = []
    relief = S.cyl_z(0.0, 0.0, g("nut.relief_r"), g("nut.relief_z"), z_pu)
    cut.append(relief)
    n_w = g("nut.washer_window_count")
    w_deg = [180.0 / g("wingnut.wing_count") + 360.0 / n_w * k for k in range(n_w)]      # first window midway between the wings
    for a in w_deg:
        cut.append(C.box_at(a, q["r_pk"] - 1.0, q["r_body"] + 1.0, g("nut.washer_window_width") / 2, z_pu, z_pu + pd))
    for a in t_deg:
        c = Part.makeCylinder(g("nut.tommy_hole_dia") / 2, g("nut.tommy_hole_depth") + 1.0,
                              C.V(g("nut.tommy_hole_bottom_r"), 0, z_ax), C.V(1, 0, 0))
        c.rotate(C.V(0, 0, 0), C.V(0, 0, 1), a)
        cut.append(c)
    ad = g("nut.arrow_depth")
    r_m = (q["r_hole"] + q["r_body"]) / 2
    rsw, rhw, rhl = g("nut.release_shaft_width"), g("nut.release_head_width"), g("nut.release_head_length")
    head_deg = math.degrees(rhl / r_m)
    shaft_deg = g("nut.release_dead_turn_deg") - head_deg
    arrow_shaft = C.sector_solid(r_m - rsw / 2, r_m + rsw / 2, H - ad, H + 1.0, th + shaft_deg / 2, shaft_deg)     # arrow shaft from key azimuth
    cut.append(arrow_shaft)
    a_e = th + shaft_deg
    E = C.polar(r_m, a_e)
    u = C.polar(1.0, a_e)
    tv = C.V(-math.sin(math.radians(a_e)), math.cos(math.radians(a_e)), 0)
    tri = [C.V(E.x + u.x * rhw / 2, E.y + u.y * rhw / 2, H - ad), C.V(E.x - u.x * rhw / 2, E.y - u.y * rhw / 2, H - ad),
           C.V(E.x + tv.x * rhl, E.y + tv.y * rhl, H - ad)]
    arrow_head = Part.Face(Part.makePolygon(tri + [tri[0]])).extrude(C.V(0, 0, ad + 1.0))
    cut.append(arrow_head)
    cut.append(C.box_at(th, q["r_hole"], q["r_body"], ad / 2, H - ad, H + 1.0))                                  # mark line at key azimuth
    # NT4 tighten (top face) and NT5 loosen (underside) glyphs on wing 0; the old +y radial mark is gone
    zc_w = H - g("wingnut.wing_root_width") / 2
    gt, gt_info = glyph_tool(p, q, "tighten")
    gl_, gl_info = glyph_tool(p, q, "loosen")
    cut += [gt, gl_]
    cut_tool = C.fuse_all(cut)
    tighten_mm3, loosen_mm3 = S.removed(gt, after_stud), S.removed(gl_, after_stud)
    relief_mm3 = S.removed(relief, after_stud)
    release_mm3 = S.removed(arrow_shaft, after_stud) + S.removed(arrow_head, after_stud)
    C.body_boolean(doc, body, cut_tool, "Cut", "WindowsHolesGlyphs", refine=False)     # refine off: the face-merge pass corrupts the helicoid faces cut by the relief (BOP errors)
    sh = C.final_shape(body)
    bools.append({"name": "WindowsHolesGlyphs", "kind": "cut", "faces_before": len(after_stud.Faces), "faces_after": len(sh.Faces), "tool_faces": len(cut_tool.Faces)})
    C.CACHE.mkdir(exist_ok=True)
    doc.saveAs(str(C.CACHE / "nut.FCStd"))
    print("nut shape done %.1fs volume=%.1f valid=%s" % (time.time() - t0, sh.Volume, sh.isValid()), flush=True)

    inside = lambda pt: sh.isInside(pt, 1e-6, True)
    # ---- thread (theta 0 / 90 at the pitch line)
    keep = lambda iv: [i for i in iv if i[0] > 2.0 and i[1] < z_pu - 2.0]
    f0 = keep(C.axial_ivals(sh, 0.0, q["r_pitch"], -1.0, z_pu + 1.0))
    f90 = keep(C.axial_ivals(sh, 90.0, q["r_pitch"], -1.0, z_pu + 1.0))
    tooth_w = f0[1][1] - f0[1][0]
    period = f0[2][0] - f0[1][0]
    shift = (f90[1][0] - f0[1][0]) % P
    zc_tooth = (f0[1][0] + f0[1][1]) / 2
    zc_groove = (f0[1][1] + f0[2][0]) / 2
    r_crest = C.radial_ivals(sh, 0.0, zc_tooth, q["r_c"] - 1.0, q["r_root"] + 2.0)[0][0]
    r_rt = C.radial_ivals(sh, 0.0, zc_groove, q["r_c"] - 1.0, q["r_root"] + 2.0)[0][0]
    wcrest = [i for i in C.axial_ivals(sh, 0.0, q["r_c"] + 0.005, zc_tooth - 3.5, zc_tooth + 3.5) if i[0] < zc_tooth < i[1]][0]
    first = [min([i for i in C.radial_ivals(sh, 5.0 * k, 0.001, q["r_c"] - 1.0, q["r_root"] + 2.0)], default=(None,))[0] for k in range(72)]
    first = [x for x in first if x is not None]
    # groove presence below / above the plate underside at r between crest and root
    r_probe = (q["r_c"] + q["r_root"]) / 2
    grooves_below = sum(1 for k in range(72) if not inside(C.polar(r_probe, 5.0 * k, z_pu - 4.0)))
    voids_above = sum(1 for k in range(72) if (5.0 * k) % 360 not in [w for w in w_deg] and not inside(C.polar(r_probe, 5.0 * k, z_pu + pd / 2)) and
                      min(abs(5.0 * k - w) for w in w_deg) > 6.0)
    top_z = max(i[1] for k in range(72) for i in C.axial_ivals(sh, 5.0 * k, q["r_c"] + 0.05, z_pu - 8.0, z_pu + 0.001)) if False else None
    # ---- bodies of the plate
    ps = C.axial_ivals(sh, 30.0, 72.2, -1.0, H + 1)
    pk = C.axial_ivals(sh, 30.0, 70.0, -1.0, H + 1)
    od = C.radial_ivals(sh, 30.0, g("nut.skirt_z_hi") + g("nut.skirt_embed"), 0, 120)      # above the skirt, below the wing underside
    ph = C.radial_ivals(sh, 30.0, 52.0, 0, 120)
    pkw = C.radial_ivals(sh, 30.0, z_pu + pd / 2, 0, 120)
    # pads: ID, count, arc
    pad_id_r = C.radial_ivals(sh, 0.0, z_pu + pd / 2, 0, 120)[0][0]
    pads_present = sum(1 for k in range(n_pad) if inside(C.polar(g("nut.pad_id") / 2 + 0.1, 360.0 / n_pad * k, z_pu + pd / 2)))
    r_arc = g("nut.pad_id") / 2 + 0.01
    pad_deg = [a / 20.0 for a in range(-200, 201) if inside(C.polar(r_arc, a / 20.0, z_pu + pd / 2))]
    pad_arc_meas = math.radians(max(pad_deg) - min(pad_deg)) * g("nut.pad_id") / 2 if pad_deg else None
    pad_bot = C.axial_ivals(sh, 0.0, g("nut.pad_id") / 2 + 0.1, -1, H + 1)[0][0]
    # tab
    tab_r = C.radial_ivals(sh, th, z_pu + pd / 2, 0, 120)[0][0]
    tab_w = C.tangential_ivals(sh, th, g("nut.tab_inner_radius") + 0.4, z_pu + pd / 2, 20.0)
    # windows
    wins = sum(1 for a in w_deg if not C.radial_ivals(sh, a, z_pu + pd / 2, q["r_pk"] + 0.5, 120))
    win_w = C.tangential_ivals(sh, w_deg[0], q["r_body"] - 2.0, z_pu + pd / 2, 20.0)
    # wings
    w_at = lambda r: (lambda iv: iv[0][1] - iv[0][0])(C.axial_ivals(sh, 0.0, r, -1, H + 1))
    ra = g("nut.skirt_r_out") + 0.5 + 0.06                  # between the dust skirt and the glyph left edge
    rb = ra + 1.5
    w1, w2 = w_at(ra), w_at(rb)
    slope_w = (w1 - w2) / (rb - ra)
    w_root_x = w1 + slope_w * (ra - q["r_body"])
    w_tip_x = w2 - slope_w * (r_tip - rb)
    taper = math.degrees(math.atan(slope_w / 2.0))
    taper_exp = math.degrees(math.atan((g("wingnut.wing_root_width") - g("wingnut.wing_tip_width")) / 2.0 / (r_tip - q["r_body"])))
    wt = C.tangential_ivals(sh, 0.0, 100.0, H - 6.0, 20.0)
    tipz_hi = H - (g("wingnut.wing_root_width") - g("wingnut.wing_tip_width")) / 2.0
    fillet_ok = (not inside(C.V(r_tip - 0.5, 0, tipz_hi - 0.3))) and inside(C.V(r_tip - 0.5, 0, tipz_hi - g("wingnut.edge_radius") - 1.0))
    gp = lambda info, sgn: C.V(sgn * (info["xc"] - info["n"].x * ad / 2), 0.0, info["zf"] - info["n"].z * ad / 2)
    rule_p = (not inside(gp(gt_info, 1.0))) and (not inside(gp(gl_info, 1.0))) and inside(C.V(-gt_info["xc"] + gt_info["n"].x * ad / 2, 0.0, gt_info["zf"] - gt_info["n"].z * ad / 2)) \
        and inside(C.V(-gl_info["xc"] + gl_info["n"].x * ad / 2, 0.0, gl_info["zf"] - gl_info["n"].z * ad / 2))
    piece_box = S.box(q["r_body"] + 3.0, r_tip - 3.0, -(thick / 2 + 0.5), thick / 2 + 0.5, 0.0, H)
    piece = sh.common(piece_box)
    x0g = gt_info["xc"] - g("nut.head_width") / 2.0 - 1.0      # one column margin each side of the glyph; the glyph lies beyond the dust skirt (r > skirt_r_out)
    x1g = gt_info["xc"] + g("nut.head_width") / 2.0 + 1.0
    m_tight = measure_glyph(piece, p, q, "+z", x0g, x1g)
    m_loose = measure_glyph(piece, p, q, "-z", x0g, x1g)
    glyph_rec = {
        "tighten": {"wing": 0, "face": "+z", "direction_sign": m_tight["direction_sign"], "radial_span": round(m_tight["span"], 3), "sense": "clockwise from +Z",
                    "tail_to_tip_y": [g("nut.glyph_length") / 2, -g("nut.glyph_length") / 2], "centre_x": gt_info["xc"], "depth": ad,
                    "band": [q["r_body"] + 5.0, g("wingnut.span") / 2 - 5.0]},
        "loosen": {"wing": 0, "face": "-z", "direction_sign": m_loose["direction_sign"], "radial_span": round(m_loose["span"], 3), "sense": "counter-clockwise from +Z",
                   "tail_to_tip_y": [-g("nut.glyph_length") / 2, g("nut.glyph_length") / 2], "centre_x": gl_info["xc"], "depth": ad,
                   "band": [q["r_body"] + 5.0, g("wingnut.span") / 2 - 5.0]},
        "band_length_mm": g("nut.arrow_length"), "face_slope_deg": gt_info["phi_deg"],
    }
    # bosses
    t0_ = t_deg[0]
    off = g("nut.tommy_hole_dia") / 2 + (g("nut.tommy_boss_od") / 2 - g("nut.tommy_hole_dia") / 2) / 2
    cth, sth = math.cos(math.radians(t0_)), math.sin(math.radians(t0_))
    pl = lambda r, y, z: C.V(r * cth - y * sth, r * sth + y * cth, z)
    tb = C.tangential_ivals(sh, t0_, 90.0, z_ax, 20.0)
    bz = [iv for iv in C.line_ivals(sh, pl(90.0, off, 0.0), pl(90.0, off, H + 5.0)) if iv[0] <= z_ax <= iv[1]][0]      # boss interval, not the skirt below
    be = C.line_ivals(sh, pl(80.0, off, z_ax), pl(120.0, off, z_ax))
    hb = C.radial_ivals(sh, t0_, z_ax, 0.0, 120.0)
    bosses = sum(1 for a in t_deg if inside(C.V(90.0 * math.cos(math.radians(a)) - off * math.sin(math.radians(a)), 90.0 * math.sin(math.radians(a)) + off * math.cos(math.radians(a)), z_ax)))
    # release arrow
    arc_samples = [a / 20.0 for a in range(int((th - 5) * 20), int((th + 45) * 20)) if not inside(C.polar(r_m, a / 20.0, H - ad / 2))]
    arrow_span = max(arc_samples) - min(arc_samples) if arc_samples else None
    arrow_depth_m = H - C.axial_ivals(sh, th + shaft_deg / 2, r_m, 0, H + 1)[0][1]
    ang_bbox = C.bbox(sh)
    feats = [
        C.chk("thread crest (nut) D = minor + 2 `fit.c_r`", 2 * r_crest, 2 * q["r_c"]),
        C.chk("thread root (nut) D = major + 2 `fit.c_r`", 2 * r_rt, 2 * q["r_root"]),
        C.chk("`thread.pitch` tooth period (A)", period, P),
        C.chk("nut tooth at pitch line = pitch/2 - `fit.g_a` (A)", tooth_w, P / 2.0 - g("fit.g_a")),
        C.chk("nut crest flat (A)", wcrest[1] - wcrest[0], q["crest_flat"]),
        C.chk("hand: tooth shift per +90 deg = pitch/4 means right", shift, P / 4.0, 0.1),
        C.chk("`thread.starts` (period / pitch)", period / P, g("thread.starts"), 0.01),
        C.chk("`thread.nut_lead_in_length` bottom chamfer (R to pitch line)", min(first) - q["r_c"], q["lead"], 0.05),
        C.flag("one-ended thread start: groove present below plate underside", grooves_below > 0, "azimuths with groove at r mid: %d of 72" % grooves_below),
        C.flag("one-ended thread start: no groove at or above plate underside (outside windows)", voids_above == 0, "voids: %d" % voids_above),
        C.chk("`nut.length` + washer proud = plate underside z (A)", ps[0][0], z_pu),
        C.chk("`nut.plate_thickness` (A)", ps[0][1] - ps[0][0], g("nut.plate_thickness")),
        C.chk("`nut.overall_height` (A)", C.bbox(sh).ZMax, H),
        C.chk("`wingnut.body_od` (D)", 2 * od[-1][1], g("wingnut.body_od")),
        C.chk("`nut.plate_hole_dia` (D)", 2 * ph[0][0], g("nut.plate_hole_dia")),
        C.chk("`nut.washer_pocket_od` (D)", 2 * pkw[0][0], g("nut.washer_pocket_od")),
        C.chk("`nut.washer_pocket_depth` (A)", pk[0][0] - z_pu, pd),
        C.chk("`nut.pad_count`", pads_present, n_pad, 0.01),
        C.chk("`nut.pad_id` (D)", 2 * pad_id_r, g("nut.pad_id")),
        C.chk("`nut.pad_arc` (T, sampled at 0.05 deg)", pad_arc_meas, g("nut.pad_arc"), 0.15),
        C.chk("`nut.pad_height` (A): pad bottom at plate underside, top at pocket floor", (pk[0][0] - pad_bot), g("nut.pad_height")),
        C.chk("`nut.tab_inner_radius` (R)", tab_r, g("nut.tab_inner_radius")),
        C.chk("`nut.tab_width` (T)", [b - a for a, b in tab_w if a < 0 < b][0], g("nut.tab_width")),
        C.chk("`nut.washer_window_count`", wins, n_w, 0.01),
        C.chk("`nut.washer_window_width` (T)", win_w[1][0] - win_w[0][1] if len(win_w) == 2 else None, g("nut.washer_window_width")),
        C.chk("`wingnut.span` (D)", 2 * C.bbox(sh).XMax, g("wingnut.span")),
        C.chk("`wingnut.wing_root_width` (A, extrapolated to body)", w_root_x, g("wingnut.wing_root_width"), 0.1),
        C.chk("`wingnut.wing_tip_width` (A, extrapolated to tip)", w_tip_x, g("wingnut.wing_tip_width"), 0.1),
        C.chk("wing taper per edge (deg)", taper, taper_exp, 0.05),
        C.chk("`wingnut.wing_thickness` (T)", wt[0][1] - wt[0][0], thick),
        C.flag("`wingnut.edge_radius` tip corners rounded (corner out, 6+1 below inside)", fillet_ok),
        C.flag("Rule P marked wing: glyph pair recessed on wing 0, absent on wing 1", rule_p),
        C.chk("`nut.tommy_boss_od` (D)", tb[-1][1] - tb[0][0] if tb else None, g("nut.tommy_boss_od")),
        C.chk("`nut.tommy_hole_dia` (D)", tb[1][0] - tb[0][1] if len(tb) == 2 else None, g("nut.tommy_hole_dia")),
        C.chk("`nut.tommy_hole_depth` (R): boss end r - hole bottom r", be[-1][1] + 80.0 - hb[0][1] if be and hb else None, g("nut.tommy_hole_depth")),
        C.chk("tommy hole bottom r (`nut.tommy_hole_bottom_r`)", hb[0][1] if hb else None, g("nut.tommy_hole_bottom_r")),
        C.chk("tommy axis z = overall height - hole depth", (bz[0] + bz[1]) / 2 if bz else None, z_ax, 0.1),
        C.chk("`nut.tommy_hole_count` bosses", bosses, n_t, 0.01),
        C.chk("`nut.release_dead_turn_deg` arrow span (deg, incl. head and mark line)", arrow_span, g("nut.release_dead_turn_deg"), 1.0),
        C.chk("`nut.arrow_depth` (A)", arrow_depth_m, ad),
        C.flag("Rule P nut tab azimuth off-axis", (th % 90.0) > 1.0),
    ]
    skirt_r = C.radial_ivals(sh, 30.0, g("nut.skirt_z_lo") + g("nut.skirt_rim") / 2, 0, 120)
    skirt_bot = C.axial_ivals(sh, 30.0, (q["r_body"] + g("nut.skirt_r_out")) / 2, -1, H + 1)
    r_a, r_b = q["r_body"] + 5.0, q["r_body"] + 9.0
    z_a = C.axial_ivals(sh, 30.0, r_a, -1, H + 1)[0][1]
    z_b = C.axial_ivals(sh, 30.0, r_b, -1, H + 1)[0][1]
    slope_deg = math.degrees(math.atan((z_a - z_b) / (r_b - r_a)))
    slope_exp = math.degrees(math.atan((g("nut.skirt_z_hi") - g("nut.skirt_z_lo") - g("nut.skirt_rim")) / (g("nut.skirt_r_out") - q["r_body"])))
    try:
        sh.check(True)
        bop_clean = True
    except Exception as exc:
        bop_clean = False
        print("BOP_CHECK_FAIL", str(exc).replace(chr(10), " | ")[:400], flush=True)
    rel_r = C.radial_ivals(sh, 30.0, (g("nut.relief_z") + z_pu) / 2.0, 0, 120)
    rel_ax = C.axial_ivals(sh, 30.0, g("nut.relief_r") - 0.05, -1.0, H + 1.0)
    new_rows = [
        ("V3", "relief bore radius `nut.relief_r` (R, plain bore at mid relief)", relief_mm3, rel_r[0][0] if rel_r else None, g("nut.relief_r"), 0.02),
        ("V3", "relief floor z `nut.relief_z` (A)", relief_mm3, rel_ax[0][1] if rel_ax else None, g("nut.relief_z"), 0.02),
        ("V3", "relief top = plate underside z (A)", relief_mm3, rel_ax[1][0] if len(rel_ax) > 1 else None, z_pu, 0.02),
        ("V3", "BOP check clean (shape.check(True) raises on SelfIntersect or InvalidCurveOnSurface)", relief_mm3, int(bop_clean), 1, S.TOL),
        ("V3", "relief leaves one solid, one shell", relief_mm3, len(sh.Solids) + len(sh.Shells), 2, S.TOL),
        ("NT4", "NT4 tighten glyph sense (-1 clockwise from +Z)", tighten_mm3, m_tight["direction_sign"], -1, S.TOL),
        ("NT4", "NT4 tighten glyph principal span, inside nut.arrow_length (mm)", tighten_mm3, m_tight["span"], g("nut.glyph_length"), 1.5),
        ("NT5", "NT5 loosen glyph sense (+1 counter-clockwise from +Z)", loosen_mm3, m_loose["direction_sign"], +1, S.TOL),
        ("NT5", "NT5 loosen glyph principal span, inside nut.arrow_length (mm)", loosen_mm3, m_loose["span"], g("nut.glyph_length"), 1.5),
        ("NT8", "NT8 release arrow recess area (mm2) equals NT4 tighten recess area within 10 percent", release_mm3, release_mm3 / ad, tighten_mm3 / ad, 0.1 * tighten_mm3 / ad),
        ("NT7", "NT7 dust skirt outer radius (R)", skirt_mm3, skirt_r[-1][1] if skirt_r else None, g("nut.skirt_r_out"), 0.02),
        ("NT7", "NT7 dust skirt bottom z (A)", skirt_mm3, skirt_bot[0][0] if skirt_bot else None, g("nut.skirt_z_lo"), 0.02),
        ("NT7", "NT7 dust skirt cone slope (deg)", skirt_mm3, slope_deg, slope_exp, 20 * S.TOL),
    ]
    for fid, name, vol, built, exp, tol in new_rows:
        r = C.chk(name, built, exp, tol)
        r.update({"id": fid, "volume_mm3": round(vol, 3)})
        feats.append(r)
    res = C.base_result("nut", sh, feats, t0=t0, extra={"derived": {k: round(v, 4) for k, v in q.items()}, "glyphs": glyph_rec,
                        "booleans": bools, "boolean_count": len(bools), "bbox_plain": S._bb(sh.BoundBox), "bbox_optimal": S._bb(C.bbox(sh)),
                        "run_seconds": round(time.time() - t0, 1), "rebuild": S.rebuild_record(before, sh, ("NT4", "NT5", "NT7", "relief"), bools),
                        "relief": {"r": g("nut.relief_r"), "z_lo": g("nut.relief_z"), "z_hi": z_pu, "removed_mm3": round(relief_mm3, 3)},
                        "nt9": "no nut window: the reading plane is the skirt bottom face (Loftsman C1, C2)"},
                        notes=["thread helix ends where the groove top meets the plate underside (z_end = z_pu - groove half-width at the crest radius)",
                               "wing mark length: arm length minus two tab widths (40 mm `nut.arrow_length` exceeds the 31.86 mm arm)",
                               "tommy axis z = overall height - `nut.tommy_hole_depth` (Loftsman: axis 20 below plate top)"])
    C.save("nut", doc, body, res)
    return res


if __name__ in ("__main__", "nut"):
    C.run_main("nut", build)
