p = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts\nut.py"
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)


rep('import cadlib as C  # noqa: E402\n', '''import cadlib as C  # noqa: E402
import step6lib as S  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "probes"))
import glyph_math  # noqa: E402  (pure python: principal-axis span and sense of a sampled recess)
''')
rep('two wings (one marked, Rule P), four tommy bosses, release arrow. Local frame: skirt bottom at z = 0."""',
    '''two wings, four tommy bosses, release arrow. Local frame: skirt bottom at z = 0.
Step 6 rebuild (NT4, NT5, NT7): tighten glyph on the top face and loosen glyph on the underside of wing 0 (they replace the old +y radial mark,
and carry Rule P), dust skirt below the wings. NT9: no nut window (Loftsman C1, C2)."""''')

# helper functions inserted before build()
rep('''def build():
    t0 = time.time()
    import Part
    p = C.params()''', '''def glyph_tool(p, q, kind):
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
    xc = (q["r_body"] + r_tip) / 2.0
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


def measure_glyph(piece, p, q, face, x0, x1, step=0.5, y_half=7.5):
    """Same sampling as tests/probes/probe_step6_marks.glyphs on the wing-0 face (+z or -z): x columns on the probe grid, y samples across the wing,
    a void is a surface at least nut.arrow_depth/2 below the column median. Returns glyph_math.analyze of the void points."""
    g = lambda k: C.G(p, k)
    depth = g("nut.arrow_depth")
    r_in = g("wingnut.body_od") / 2 + 3
    root = g("wingnut.wing_root_width")
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
        med = vals[len(vals) // 2]
        for y, v in col:
            if sign * (med - v) >= depth / 2.0:
                void.append((x, y, v))
    return glyph_math.analyze(void) if len(void) >= 4 else {"count": len(void), "span": 0.0, "direction_sign": 0}


def build():
    t0 = time.time()
    import Part
    before = S.before_state("nut")
    p = C.params()''')

# skirt into the additive fuse; record booleans
rep('''    C.body_boolean(doc, body, C.fuse_all(fuse), "Fuse", "PadsTabWingsBosses")''', '''    skirt = skirt_solid(p, q)
    fuse.append(skirt)
    pre_base = C.final_shape(body)
    skirt_mm3 = skirt.cut(pre_base).Volume
    fuse_tool = C.fuse_all(fuse)
    C.body_boolean(doc, body, fuse_tool, "Fuse", "PadsTabWingsBossesSkirt")
    after_fuse = C.final_shape(body)
    bools = [{"name": "PadsTabWingsBossesSkirt", "kind": "fuse", "faces_before": len(pre_base.Faces), "faces_after": len(after_fuse.Faces),
              "tool_faces": len(fuse_tool.Faces)}]''')
rep('''    C.body_boolean(doc, body, stud, "Cut", "ThreadStud")''', '''    C.body_boolean(doc, body, stud, "Cut", "ThreadStud")
    after_stud = C.final_shape(body)
    bools.append({"name": "ThreadStud", "kind": "cut", "faces_before": len(after_fuse.Faces), "faces_after": len(after_stud.Faces)})''')

# glyphs replace the old +y wing mark
i0 = s.index("    # Rule P marked wing: shallow arrow relief on the +y face of wing 0")
i1 = s.index('    C.body_boolean(doc, body, C.fuse_all(cut), "Cut", "WindowsHolesMarks")')
j1 = s.index("    sh = C.final_shape(body)", i1)
s = s[:i0] + '''    # NT4 tighten (top face) and NT5 loosen (underside) glyphs on wing 0; the old +y radial mark is gone
    zc_w = H - g("wingnut.wing_root_width") / 2
    gt, gt_info = glyph_tool(p, q, "tighten")
    gl_, gl_info = glyph_tool(p, q, "loosen")
    cut += [gt, gl_]
    cut_tool = C.fuse_all(cut)
    tighten_mm3, loosen_mm3 = S.removed(gt, after_stud), S.removed(gl_, after_stud)
    C.body_boolean(doc, body, cut_tool, "Cut", "WindowsHolesGlyphs")
''' + s[j1:]
rep('''    sh = C.final_shape(body)
    C.CACHE.mkdir(exist_ok=True)''', '''    sh = C.final_shape(body)
    bools.append({"name": "WindowsHolesGlyphs", "kind": "cut", "faces_before": len(after_stud.Faces), "faces_after": len(sh.Faces), "tool_faces": len(cut_tool.Faces)})
    C.CACHE.mkdir(exist_ok=True)''')

rep('''    bz = (lambda lines: lines[0])(C.line_ivals(sh, pl(90.0, off, 0.0), pl(90.0, off, H + 5.0)))''', '''    bz = [iv for iv in C.line_ivals(sh, pl(90.0, off, 0.0), pl(90.0, off, H + 5.0)) if iv[0] <= z_ax <= iv[1]][0]      # boss interval, not the skirt below''')

# measurement probe radii: skirt occupies z 5..14 below r 95.14
rep('''    od = C.radial_ivals(sh, 30.0, 10.0, 0, 120)''', '''    od = C.radial_ivals(sh, 30.0, g("nut.skirt_z_hi") + g("nut.skirt_embed"), 0, 120)      # above the skirt, below the wing underside''')
rep('''    w1, w2 = w_at(100.0), w_at(105.0)
    slope_w = (w1 - w2) / 5.0
    w_root_x = w1 + slope_w * (100.0 - q["r_body"])
    w_tip_x = w2 - slope_w * (r_tip - 105.0)''', '''    ra = gt_info["xc"] + g("nut.head_width") / 2.0 + g("nut.tab_width") / 2.0      # beyond the glyph right edge, before the tip fillet
    rb = ra + g("nut.tab_width") - g("collet.tool_overshoot")
    w1, w2 = w_at(ra), w_at(rb)
    slope_w = (w1 - w2) / (rb - ra)
    w_root_x = w1 + slope_w * (ra - q["r_body"])
    w_tip_x = w2 - slope_w * (r_tip - rb)''')

# replace the old marked-wing flag block
a0 = s.index("    mark_y = thick / 2 - ad / 2")
a1 = s.index("    # bosses")
s = s[:a0] + '''    gp = lambda info, sgn: C.V(sgn * (info["xc"] - info["n"].x * ad / 2), 0.0, info["zf"] - info["n"].z * ad / 2)
    rule_p = (not inside(gp(gt_info, 1.0))) and (not inside(gp(gl_info, 1.0))) and inside(C.V(-gt_info["xc"] + gt_info["n"].x * ad / 2, 0.0, gt_info["zf"] - gt_info["n"].z * ad / 2)) \\
        and inside(C.V(-gl_info["xc"] + gl_info["n"].x * ad / 2, 0.0, gl_info["zf"] - gl_info["n"].z * ad / 2))
    piece_box = S.box(q["r_body"] + 3.0, r_tip - 3.0, -(thick / 2 + 0.5), thick / 2 + 0.5, 0.0, H)
    piece = sh.common(piece_box)
    x0g, x1g = gt_info["xc"] - g("nut.head_width"), gt_info["xc"] + g("nut.head_width")
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
''' + s[a1:]

rep('''        C.flag("Rule P marked wing: arrow relief on wing 0 +y face, absent on wing 180 and wing 0 -y face", marked0 and clear180 and clear0_other_side),
''', '''        C.flag("Rule P marked wing: glyph pair recessed on wing 0, absent on wing 1", rule_p),
''')

# new rows and result extras
rep('''    res = C.base_result("nut", sh, feats, t0=t0, extra={"derived": {k: round(v, 4) for k, v in q.items()}},''', '''    skirt_r = C.radial_ivals(sh, 30.0, g("nut.skirt_z_lo") + g("nut.skirt_rim") / 2, 0, 120)
    skirt_bot = C.axial_ivals(sh, 30.0, (q["r_body"] + g("nut.skirt_r_out")) / 2, -1, H + 1)
    r_a, r_b = q["r_body"] + 5.0, q["r_body"] + 9.0
    z_a = C.axial_ivals(sh, 30.0, r_a, -1, H + 1)[0][1]
    z_b = C.axial_ivals(sh, 30.0, r_b, -1, H + 1)[0][1]
    slope_deg = math.degrees(math.atan((z_a - z_b) / (r_b - r_a)))
    slope_exp = math.degrees(math.atan((g("nut.skirt_z_hi") - g("nut.skirt_z_lo") - g("nut.skirt_rim")) / (g("nut.skirt_r_out") - q["r_body"])))
    new_rows = [
        ("NT4", "NT4 tighten glyph sense (-1 clockwise from +Z)", tighten_mm3, m_tight["direction_sign"], -1, 0.01),
        ("NT4", "NT4 tighten glyph principal span, inside nut.arrow_length (mm)", tighten_mm3, m_tight["span"], g("nut.glyph_length"), 1.0),
        ("NT5", "NT5 loosen glyph sense (+1 counter-clockwise from +Z)", loosen_mm3, m_loose["direction_sign"], +1, 0.01),
        ("NT5", "NT5 loosen glyph principal span, inside nut.arrow_length (mm)", loosen_mm3, m_loose["span"], g("nut.glyph_length"), 1.0),
        ("NT7", "NT7 dust skirt outer radius (R)", skirt_mm3, skirt_r[-1][1] if skirt_r else None, g("nut.skirt_r_out"), 0.02),
        ("NT7", "NT7 dust skirt bottom z (A)", skirt_mm3, skirt_bot[0][0] if skirt_bot else None, g("nut.skirt_z_lo"), 0.02),
        ("NT7", "NT7 dust skirt cone slope (deg)", skirt_mm3, slope_deg, slope_exp, 0.3),
    ]
    for fid, name, vol, built, exp, tol in new_rows:
        r = C.chk(name, built, exp, tol)
        r.update({"id": fid, "volume_mm3": round(vol, 3)})
        feats.append(r)
    res = C.base_result("nut", sh, feats, t0=t0, extra={"derived": {k: round(v, 4) for k, v in q.items()}, "glyphs": glyph_rec,
                        "booleans": bools, "boolean_count": len(bools), "bbox_plain": S._bb(sh.BoundBox), "bbox_optimal": S._bb(C.bbox(sh)),
                        "run_seconds": round(time.time() - t0, 1), "rebuild": S.rebuild_record(before, sh, ("NT4", "NT5", "NT7"), bools),
                        "nt9": "no nut window: the reading plane is the skirt bottom face (Loftsman C1, C2)"},''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
