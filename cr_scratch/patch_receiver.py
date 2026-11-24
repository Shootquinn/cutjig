p = r"C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\CuttingJig\build_parts\receiver.py"
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new, 1)


rep('import cadlib as C  # noqa: E402\n', 'import cadlib as C  # noqa: E402\nimport step6lib as S  # noqa: E402\n')
rep('register bore; key slot; floor hole."""',
    'register bore; key slot; floor hole.\nStep 6 rebuild (RC6, AC4): witness ruler on the thread at witness.azimuth_deg, cut with the key slot in one boolean."""')

rep('''def build():
    t0 = time.time()
    p = C.params()''', '''def ruler_tool(p, q):
    """Witness ruler as one fused tool (Loftsman section 1). Built at azimuth 0 (x radial, y = t tangential counter-clockwise, z axial), then turned
    to witness.azimuth_deg. Floor plane at distance d_fl from the axis; lines, wrong-collet bands and digit pockets cut below the floor."""
    g = lambda k: C.G(p, k)
    ov = g("collet.tool_overshoot")
    d_fl = q["r_min"] - g("witness.channel_floor_depth")
    cz0, cz1 = g("witness.channel_z")
    z0 = q["z_top"] - g("nut.skirt_below_flange")
    x_hi = q["r_maj"] + ov
    cw = g("witness.channel_width")
    n = int(math.floor(g("holder.stroke_gap_R") / g("witness.scale_pitch") + 1e-9)) + 1
    lh, ld = g("witness.line_height"), g("witness.line_depth")
    parts = [S.box(d_fl, x_hi, -cw / 2, cw / 2, cz0, cz1)]
    for k in range(n):
        zk = z0 + k * g("witness.scale_pitch")
        half = (g("witness.line_length_major") if k % g("witness.major_every") == 0 else g("witness.line_length")) / 2
        parts.append(S.box(d_fl - ld, d_fl + ov, -half, half, zk - lh / 2, zk + lh / 2))
    bd = g("witness.band_depth")
    t0_, t1_ = g("witness.band_t")
    for b in (g("witness.wrong_collet_band_low"), g("witness.wrong_collet_band_high")):
        parts.append(S.box(d_fl - bd, d_fl + ov, t0_, t1_, z0 + b[0], z0 + b[1]))
    dt0, dt1 = g("witness.digit_t")
    dz, dh = g("witness.digit_z_shift"), g("witness.digit_height")
    for k in range(0, n, g("witness.major_every")):
        zc = z0 + k * g("witness.scale_pitch") + dz
        parts.append(S.box(d_fl - ld, d_fl + ov, dt0, dt1, zc - dh / 2, zc + dh / 2))
    return parts, {"d_fl": d_fl, "z0": z0, "n": n, "az": g("witness.azimuth_deg")}


def build():
    t0 = time.time()
    before = S.before_state("receiver")
    p = C.params()''')

rep('''    C.body_boolean(doc, body, groove, "Cut", "ThreadStud")
    slot = C.box_at(th, q["r_reg"] - 1.0, q["r_reg"] + g("receiver.key_slot_depth"), g("receiver.key_slot_width") / 2, 0.0, q["z_top"] + 1.0)
    C.body_boolean(doc, body, slot, "Cut", "KeySlot")
    sh = C.final_shape(body)''', '''    f0 = len(C.final_shape(body).Faces)
    C.body_boolean(doc, body, groove, "Cut", "ThreadStud")
    pre = C.final_shape(body)
    bools = [{"name": "ThreadStud", "kind": "cut", "faces_before": f0, "faces_after": len(pre.Faces)}]
    slot = C.box_at(th, q["r_reg"] - 1.0, q["r_reg"] + g("receiver.key_slot_depth"), g("receiver.key_slot_width") / 2, 0.0, q["z_top"] + 1.0)
    ruler_parts, rd = ruler_tool(p, q)
    rrec = S.Rec("receiver")
    ruler = rrec.fuse("ruler_tool_fuse", ruler_parts)
    ruler.rotate(C.V(0, 0, 0), C.V(0, 0, 1), rd["az"])
    ruler_mm3 = S.removed(ruler, pre)
    tool = C.fuse_all([slot, ruler])
    bools += rrec.booleans
    C.body_boolean(doc, body, tool, "Cut", "KeySlotAndRuler")
    sh = C.final_shape(body)
    bools.append({"name": "KeySlotAndRuler", "kind": "cut", "faces_before": len(pre.Faces), "faces_after": len(sh.Faces), "tool_faces": len(tool.Faces)})''')

rep('''    feats = [
        C.chk("`thread.major` (D) from crest radius"''', '''    az, d_fl, zz0, nn = rd["az"], rd["d_fl"], rd["z0"], rd["n"]
    pitch_w = g("witness.scale_pitch")
    mid = zz0 + pitch_w / 2
    fl_iv = C.radial_ivals(sh, az, mid, 60.0, q["r_maj"] + 3.0)
    chan_t = C.line_ivals(sh, S.point_at(az, d_fl + 0.02, -8.0, mid), S.point_at(az, d_fl + 0.02, 8.0, mid))
    chan_w = (chan_t[1][0] - chan_t[0][1]) if len(chan_t) >= 2 else None
    zlo, zhi = zz0 - 3.0, zz0 + nn * pitch_w + 2.0
    ax = C.axial_ivals(sh, az, d_fl - g("witness.line_depth") / 2, zlo, zhi)
    gaps = [(a[1], b[0]) for a, b in zip(ax, ax[1:])]
    marks = [(a + b) / 2 for a, b in gaps]
    line_h = gaps[0][1] - gaps[0][0] if gaps else None
    zmaj = zz0 + g("witness.major_every") * pitch_w
    k0 = C.line_ivals(sh, S.point_at(az, d_fl - 0.25, -8.0, zmaj), S.point_at(az, d_fl - 0.25, 8.0, zmaj))
    k1 = C.line_ivals(sh, S.point_at(az, d_fl - 0.25, -8.0, zz0 + pitch_w), S.point_at(az, d_fl - 0.25, 8.0, zz0 + pitch_w))
    len0 = 2.0 * (8.0 - k0[0][1]) if k0 else None          # major line merges with its digit pocket on the + side: read the - side edge, twice
    len1 = k1[1][0] - k1[0][1] if len(k1) >= 2 else None
    line_dep = C.radial_ivals(sh, az, marks[1], 60.0, q["r_maj"] + 3.0)[0][1] if len(marks) > 1 else None
    tb = g("witness.band_t")
    bz = lambda t, d: C.line_ivals(sh, S.point_at(az, d, t, zlo), S.point_at(az, d, t, zhi))
    band_iv = bz((tb[0] + tb[1]) / 2, d_fl - g("witness.band_depth") / 2)
    band_gaps = [(a[1], b[0]) for a, b in zip(band_iv, band_iv[1:])]
    b_lo, b_hi = g("witness.wrong_collet_band_low"), g("witness.wrong_collet_band_high")
    dig_t = g("witness.digit_t")
    dig_iv = bz((dig_t[0] + dig_t[1]) / 2, d_fl - g("witness.line_depth") / 2)
    dig_gaps = [(a[1], b[0]) for a, b in zip(dig_iv, dig_iv[1:])]
    n_dig = len(range(0, nn, g("witness.major_every")))
    witness_rec = {"azimuth_deg": az, "zone": [g("holder.stroke_gap_min_K"), g("witness.zone_high")], "band_low": b_lo,
                   "band_high": b_hi, "z0": zz0, "marks_z": [round(m, 3) for m in marks],
                   "digits": [{"k": k, "text": str(k), "z": round(zz0 + k * pitch_w, 3)} for k in range(0, nn, g("witness.major_every"))],
                   "channel_floor_d": d_fl, "reading_plane": "nut skirt bottom face (flange underside - nut.skirt_below_flange)"}
    feats = [
        C.chk("`thread.major` (D) from crest radius"''')

rep('''        C.flag("Rule P key slot off-axis (azimuth not 0/90/180/270)", (th % 90.0) > 1.0),
    ]
    res = C.base_result("receiver", sh, feats, extra={"derived": {k: round(v, 4) for k, v in q.items()}}, t0=t0,''', '''        C.flag("Rule P key slot off-axis (azimuth not 0/90/180/270)", (th % 90.0) > 1.0),
    ]
    rc6 = [
        ("RC6 ruler channel floor distance from the axis (R)", fl_iv[0][1] if fl_iv else None, d_fl, 0.01),
        ("RC6 ruler channel width (T)", chan_w, g("witness.channel_width"), 0.05),
        ("RC6 graduation count", len(marks), nn, 0.01),
        ("RC6 graduation 0 z (A): skirt bottom face at gap 0", marks[0] if marks else None, zz0, 0.05),
        ("RC6 graduation pitch (A)", (marks[-1] - marks[0]) / (len(marks) - 1) if len(marks) > 1 else None, pitch_w, 0.01),
        ("RC6 graduation height (A)", line_h, g("witness.line_height"), 0.02),
        ("RC6 graduation depth below the channel floor (R)", d_fl - line_dep if line_dep else None, g("witness.line_depth"), 0.02),
        ("RC6 graduation length (T)", len1, g("witness.line_length"), 0.05),
        ("RC6 major graduation length (T)", len0, g("witness.line_length_major"), 0.05),
        ("RC6 wrong-collet band low: z extent (A)", band_gaps[0][1] - band_gaps[0][0] if len(band_gaps) >= 1 else None, b_lo[1] - b_lo[0], 0.05),
        ("RC6 wrong-collet band high: z extent (A)", band_gaps[1][1] - band_gaps[1][0] if len(band_gaps) >= 2 else None, b_hi[1] - b_hi[0], 0.05),
        ("RC6 wrong-collet band high: top z (A)", band_gaps[1][1] if len(band_gaps) >= 2 else None, zz0 + b_hi[1], 0.05),
        ("RC6 digit pocket count (0, 5, 10)", len(dig_gaps), n_dig, 0.01),
    ]
    for name, built, exp, tol in rc6:
        r = C.chk(name, built, exp, tol)
        r.update({"id": "RC6", "volume_mm3": round(ruler_mm3, 3)})
        feats.append(r)
    res = C.base_result("receiver", sh, feats, extra={"derived": {k: round(v, 4) for k, v in q.items()}, "witness": witness_rec,
                        "booleans": bools, "boolean_count": len(bools), "bbox_plain": S._bb(sh.BoundBox), "bbox_optimal": S._bb(C.bbox(sh)),
                        "run_seconds": round(time.time() - t0, 1), "rebuild": S.rebuild_record(before, sh, ("RC6", "AC4"), bools)}, t0=t0,''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
