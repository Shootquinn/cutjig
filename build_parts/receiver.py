"""Receiver: externally threaded cup. Floor frame: floor top z = 0, bottom at datum A (z = -icd.floor_above_datum_a).
Spigot (r = receiver.spigot_od / 2) below the shoulder; 6-turn right-hand 45/45 thread above; register bore; key slot; floor hole.
Step 6 rebuild (RC6, AC4): witness ruler on the thread at witness.azimuth_deg, cut with the key slot in one boolean."""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadlib as C  # noqa: E402
import step6lib as S  # noqa: E402


def dims(p):
    g = lambda k: C.G(p, k)
    P = g("thread.pitch")
    z_top = g("receiver.rim_above_floor")
    z_run = z_top - g("thread.run_turns") * P
    return {
        "P": P, "tanf": math.tan(math.radians(g("thread.flank_deg"))),
        "r_maj": g("thread.major") / 2, "r_min": g("thread.minor") / 2, "r_pitch": (g("thread.major") - g("chain.h")) / 2,
        "z_top": z_top, "z_run": z_run, "z_sh": z_run - g("thread.runout_land"), "z_bot": -g("icd.floor_above_datum_a"),
        "r_sp": g("receiver.spigot_od") / 2, "r_reg": g("receiver.register_bore_radius"),
        "r_hole": g("receiver.floor_hole_dia") / 2, "land": g("thread.land_width"),
    }


def groove_halfwidth(q, r):
    return (q["land"] + 2.0 * (r - q["r_min"]) * q["tanf"]) / 2.0


def width_at(sh, theta, r, zc, span=4.0):
    iv = C.axial_ivals(sh, theta, r, zc - span, zc + span)
    for a, b in iv:
        if a < zc < b:
            return b - a
    return None


def ruler_tool(p, q):
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
    p = C.params()
    g = lambda k: C.G(p, k)
    q = dims(p)
    th = g("receiver.key_offset_deg")
    P = q["P"]
    cham, lead = g("receiver.register_chamfer"), g("thread.lead_in_length")
    pts = [(q["r_hole"], q["z_bot"]), (q["r_sp"], q["z_bot"]), (q["r_sp"], q["z_sh"]), (q["r_min"], q["z_sh"]),
           (q["r_min"], q["z_run"]), (q["r_maj"], q["z_run"]), (q["r_maj"], q["z_top"] - lead), (q["r_pitch"], q["z_top"]),
           (q["r_reg"] + cham, q["z_top"]), (q["r_reg"], q["z_top"] - cham), (q["r_reg"], 0.0), (q["r_hole"], 0.0)]
    doc, body = C.new_body("receiver")
    C.body_revolve(doc, body, pts, "Cup")
    # helical groove: profile stays below tool_groove_fraction x pitch, so it overshoots outward past the crest
    hw_cap = g("thread.tool_groove_fraction") * P / 2.0
    ov = (hw_cap - groove_halfwidth(q, q["r_maj"])) / q["tanf"]
    r_out = q["r_maj"] + ov
    hw_root = groove_halfwidth(q, q["r_min"])
    zc = q["z_run"]
    # stud-subtract (Orchestrator ruling, Step 4 fix pass): the groove is a solid built from quarter-turn ruled-helicoid segments
    # (cadlib.thread_ridge_stud) and cut as a Part solid; the native SubtractiveHelix left GeomAbs_C0 edges and faces (BOP check) and
    # the tilted nut/receiver booleans failed above 1.06 deg. Same pitch, same profile, no scaling.
    groove = C.thread_ridge_stud([(q["r_min"], -hw_root), (r_out, -hw_cap), (r_out, hw_cap), (q["r_min"], hw_root)],
                                 P, zc, zc + q["z_top"] - q["z_run"] + P)
    # Order: key slot and witness ruler on the unthreaded cup (analytic faces only), then the thread stud. The ruler cut after the stud made an
    # Unorientable shape (helicoid faces cut by the ruler planes); the final solid is the same material removal either way.
    pre_cup = C.final_shape(body)
    slot = C.box_at(th, q["r_reg"] - 1.0, q["r_reg"] + g("receiver.key_slot_depth"), g("receiver.key_slot_width") / 2, 0.0, q["z_top"] + 1.0)
    ruler_parts, rd = ruler_tool(p, q)
    rrec = S.Rec("receiver")
    ruler = rrec.fuse("ruler_tool_fuse", ruler_parts)
    ruler.rotate(C.V(0, 0, 0), C.V(0, 0, 1), rd["az"])
    ruler_mm3 = S.removed(ruler, pre_cup)
    tool = C.fuse_all([slot, ruler])
    bools = list(rrec.booleans)
    C.body_boolean(doc, body, tool, "Cut", "KeySlotAndRuler")
    pre = C.final_shape(body)
    bools.append({"name": "KeySlotAndRuler", "kind": "cut", "faces_before": len(pre_cup.Faces), "faces_after": len(pre.Faces), "tool_faces": len(tool.Faces)})
    C.body_boolean(doc, body, groove, "Cut", "ThreadStud")
    sh = C.final_shape(body)
    bools.append({"name": "ThreadStud", "kind": "cut", "faces_before": len(pre.Faces), "faces_after": len(sh.Faces)})
    print("cut done %.1fs volume=%.1f" % (time.time() - t0, sh.Volume), flush=True)
    C.CACHE.mkdir(exist_ok=True)
    doc.saveAs(str(C.CACHE / "receiver.FCStd"))

    clr = th + 180.0
    # thread, theta 0 and 90 (hand), tooth width at the pitch line
    ax0 = C.axial_ivals(sh, 0.0, q["r_pitch"], q["z_run"] - 2.0, q["z_top"] + 1.0)
    ax90 = C.axial_ivals(sh, 90.0, q["r_pitch"], q["z_run"] - 2.0, q["z_top"] + 1.0)
    keep = lambda ivs: [iv for iv in ivs if iv[0] > q["z_run"] + 0.01 and iv[1] < q["z_top"] - lead - 0.01]
    f0, f90 = keep(ax0), keep(ax90)
    tooth_w = f0[1][1] - f0[1][0]
    period = f0[2][0] - f0[1][0]
    shift = (f90[1][0] - f0[1][0]) % P
    zc_tooth = (f0[1][0] + f0[1][1]) / 2
    zc_groove = (f0[1][1] + f0[2][0]) / 2
    r_crest = C.radial_ivals(sh, 0.0, zc_tooth, q["r_min"] - 1.0, q["r_maj"] + 2.0)[-1][1]
    r_root = C.radial_ivals(sh, 0.0, zc_groove, q["r_min"] - 1.0, q["r_maj"] + 2.0)[-1][1]
    w_crest = width_at(sh, 0.0, q["r_maj"] - 0.005, zc_tooth)
    r_lo, r_hi = q["r_min"] + 0.5, q["r_maj"] - 0.5
    flank = math.degrees(math.atan((width_at(sh, 0.0, r_lo, zc_tooth) - width_at(sh, 0.0, r_hi, zc_tooth)) / 2.0 / (r_hi - r_lo)))
    starts, outer_top = [], []
    for k in range(72):
        a = 5.0 * k
        ivs = C.axial_ivals(sh, a, q["r_maj"] - 0.2, q["z_run"] - 3.0, q["z_top"] + 1.0)
        if ivs:
            starts.append(ivs[0][0])
        ro = C.radial_ivals(sh, a, q["z_top"] - 0.001, q["r_reg"] + 3.0, q["r_maj"] + 1.0)
        if ro:
            outer_top.append(ro[-1][1])
    land = C.axial_ivals(sh, clr, q["r_min"] + 0.01, q["z_bot"] - 1.0, q["z_run"] + 0.5)
    sp = C.radial_ivals(sh, clr, q["z_sh"] - 1.0, 0, 90)
    sf = C.axial_ivals(sh, clr, q["r_sp"] - 3.0, q["z_bot"] - 1.0, q["z_top"] + 1.0)
    reg = C.radial_ivals(sh, clr, 20.0, 0, 90)
    reg_top = C.radial_ivals(sh, clr, q["z_top"] - 0.001, 0, 90)
    flr = C.radial_ivals(sh, clr, -10.0, 0, 90)
    fl_top = C.axial_ivals(sh, clr, (q["r_hole"] + q["r_reg"]) / 2, q["z_bot"] - 1.0, 5.0)
    sl_r = C.radial_ivals(sh, th, 20.0, 0, 90)
    sl_w = C.tangential_ivals(sh, th, q["r_reg"] + g("receiver.key_slot_depth") / 2, 20.0, 20.0)
    absent = [a / 4.0 for a in range(0, 360 * 4) if not sh.isInside(C.polar(q["r_reg"] + 1.0, a / 4.0, 20.0), 1e-6, True)]
    slot_az = (min(absent) + max(absent)) / 2.0 if absent and (max(absent) - min(absent)) < 30.0 else None
    open_ends = (not sh.isInside(C.polar(q["r_reg"] + 1.0, th, 0.05), 1e-6, True)) and \
                (not sh.isInside(C.polar(q["r_reg"] + 1.0, th, q["z_top"] - 0.05), 1e-6, True))
    az, d_fl, zz0, nn = rd["az"], rd["d_fl"], rd["z0"], rd["n"]
    tspan = g("witness.channel_width") / 2 + 2 * g("collet.tool_overshoot")      # tangent measurement line half-length: past the channel edge, inside the root cylinder
    pitch_w = g("witness.scale_pitch")
    mid = zz0 + pitch_w / 2
    fl_iv = C.radial_ivals(sh, az, mid, 60.0, q["r_maj"] + 3.0)
    chan_t = C.line_ivals(sh, S.point_at(az, d_fl + 0.02, -tspan, mid), S.point_at(az, d_fl + 0.02, tspan, mid))
    chan_w = (chan_t[1][0] - chan_t[0][1]) if len(chan_t) >= 2 else None
    zlo, zhi = zz0 - 3.0, zz0 + nn * pitch_w + 2.0
    ax = C.axial_ivals(sh, az, d_fl - g("witness.line_depth") / 2, zlo, zhi)
    gaps = [(a[1], b[0]) for a, b in zip(ax, ax[1:])]
    marks = [(a + b) / 2 for a, b in gaps]
    line_h = gaps[0][1] - gaps[0][0] if gaps else None
    zmaj = zz0 + g("witness.major_every") * pitch_w
    k0 = C.line_ivals(sh, S.point_at(az, d_fl - 0.25, -tspan, zmaj), S.point_at(az, d_fl - 0.25, tspan, zmaj))
    zmin_ = zz0 + 2 * pitch_w                                          # a minor line clear of the band strips and digit pockets
    k1 = C.line_ivals(sh, S.point_at(az, d_fl - 0.25, -tspan, zmin_), S.point_at(az, d_fl - 0.25, tspan, zmin_))
    len0 = 2.0 * (tspan - k0[0][1]) if k0 else None          # major line merges with its digit pocket on the + side: read the - side edge, twice
    len1 = k1[1][0] - k1[0][1] if len(k1) >= 2 else None
    line_dep = C.radial_ivals(sh, az, marks[1], 60.0, q["r_maj"] + 3.0)[0][1] if len(marks) > 1 else None
    tb = g("witness.band_t")
    bz = lambda t, d: C.line_ivals(sh, S.point_at(az, d, t, zlo), S.point_at(az, d, t, zhi))
    band_iv = bz((tb[0] + tb[1]) / 2, d_fl - g("witness.band_depth") / 2)
    band_gaps = [(zlo + a[1], zlo + b[0]) for a, b in zip(band_iv, band_iv[1:])]
    b_lo, b_hi = g("witness.wrong_collet_band_low"), g("witness.wrong_collet_band_high")
    dig_t = g("witness.digit_t")
    dig_iv = bz((dig_t[0] + dig_t[1]) / 2, d_fl - g("witness.line_depth") / 2)
    dig_gaps = [(zlo + a[1], zlo + b[0]) for a, b in zip(dig_iv, dig_iv[1:])]
    n_dig = len(range(0, nn, g("witness.major_every")))
    witness_rec = {"azimuth_deg": az, "zone": [g("holder.stroke_gap_min_K"), g("witness.zone_high")], "band_low": b_lo,
                   "band_high": b_hi, "z0": zz0, "marks_z": [round(m, 3) for m in marks],
                   "digits": [{"k": k, "text": str(k), "z": round(zz0 + k * pitch_w, 3)} for k in range(0, nn, g("witness.major_every"))],
                   "channel_floor_d": d_fl, "reading_plane": "nut skirt bottom face (flange underside - nut.skirt_below_flange)"}
    feats = [
        C.chk("`thread.major` (D) from crest radius", 2 * r_crest, g("thread.major")),
        C.chk("`thread.minor` (D) from root radius", 2 * r_root, g("thread.minor")),
        C.chk("`thread.pitch` (A) tooth period", period, P),
        C.chk("tooth width at pitch line = pitch / 2 (A)", tooth_w, P / 2.0),
        C.chk("`thread.land_width` crest flat (A)", w_crest, g("thread.land_width")),
        C.chk("hand: tooth shift per +90 deg = pitch/4 means right", shift, P / 4.0, 0.1, "left hand would read 3 x pitch/4"),
        C.chk("`thread.starts` (period / pitch)", period / P, g("thread.starts"), 0.01),
        C.chk("`thread.flank_deg` from tooth widths (deg)", flank, g("thread.flank_deg"), 0.5),
        C.chk("thread run start z (lowest tooth start)", min(starts), q["z_run"], 0.05),
        C.chk("`thread.lead_in_length` rim chamfer (R, to pitch line)", q["r_maj"] - max(outer_top), lead),
        C.chk("`thread.runout_land` length (A)", min(starts) - land[0][1], g("thread.runout_land")),
        C.chk("shoulder z (A)", sf[0][1], q["z_sh"]),
        C.chk("`receiver.spigot_od` (D)", 2 * sp[-1][1], g("receiver.spigot_od")),
        C.chk("`receiver.register_bore_radius` (R)", reg[0][0], q["r_reg"], 0.01),
        C.chk("`receiver.register_chamfer` (A)", reg_top[0][0] - q["r_reg"], cham),
        C.chk("`receiver.rim_above_floor` (A)", C.bbox(sh).ZMax, q["z_top"]),
        C.chk("`receiver.key_slot_depth` (R)", sl_r[0][0] - q["r_reg"], g("receiver.key_slot_depth")),
        C.chk("`receiver.key_slot_width` (T)", sl_w[1][0] - sl_w[0][1] if len(sl_w) == 2 else None, g("receiver.key_slot_width")),
        C.chk("`receiver.key_offset_deg` slot azimuth (deg)", slot_az, th, 0.3),
        C.flag("slot runs from floor to rim (open at both ends)", open_ends),
        C.chk("`receiver.floor_hole_dia` (D)", 2 * flr[0][0], g("receiver.floor_hole_dia")),
        C.chk("floor top z = 0 (floor frame)", fl_top[0][1], 0.0, 0.01),
        C.chk("receiver bottom z = -icd.floor_above_datum_a", C.bbox(sh).ZMin, q["z_bot"], 0.01),
        C.chk("`receiver.register_depth` = holder.length - nut.skirt_below_flange (param identity, not built)",
              g("holder.length") - g("nut.skirt_below_flange"), g("receiver.register_depth"), 0.001),
        C.flag("Rule P key slot off-axis (azimuth not 0/90/180/270)", (th % 90.0) > 1.0),
    ]
    rc6 = [
        ("RC6 ruler channel floor distance from the axis (R)", fl_iv[0][1] if fl_iv else None, d_fl, S.TOL),
        ("RC6 ruler channel width (T)", chan_w, g("witness.channel_width"), 0.05),
        ("RC6 graduation count", len(marks), nn, S.TOL),
        ("RC6 graduation 0 z (A): skirt bottom face at gap 0", marks[0] if marks else None, zz0, 0.05),
        ("RC6 graduation pitch (A)", (marks[-1] - marks[0]) / (len(marks) - 1) if len(marks) > 1 else None, pitch_w, S.TOL),
        ("RC6 graduation height (A)", line_h, g("witness.line_height"), 0.02),
        ("RC6 graduation depth below the channel floor (R)", d_fl - line_dep if line_dep else None, g("witness.line_depth"), 0.02),
        ("RC6 graduation length (T)", len1, g("witness.line_length"), 0.05),
        ("RC6 major graduation length (T)", len0, g("witness.line_length_major"), 0.05),
        ("RC6 wrong-collet band low: z extent (A)", band_gaps[0][1] - band_gaps[0][0] if len(band_gaps) >= 1 else None, b_lo[1] - b_lo[0], 0.05),
        ("RC6 wrong-collet band high: z extent (A)", band_gaps[1][1] - band_gaps[1][0] if len(band_gaps) >= 2 else None, b_hi[1] - b_hi[0], 0.05),
        ("RC6 wrong-collet band high: top z (A)", band_gaps[1][1] if len(band_gaps) >= 2 else None, zz0 + b_hi[1], 0.05),
        ("RC6 digit pocket count (0, 5, 10)", len(dig_gaps), n_dig, S.TOL),
    ]
    for name, built, exp, tol in rc6:
        r = C.chk(name, built, exp, tol)
        r.update({"id": "RC6", "volume_mm3": round(ruler_mm3, 3)})
        feats.append(r)
    res = C.base_result("receiver", sh, feats, extra={"derived": {k: round(v, 4) for k, v in q.items()}, "witness": witness_rec,
                        "booleans": bools, "boolean_count": len(bools), "bbox_plain": S._bb(sh.BoundBox), "bbox_optimal": S._bb(C.bbox(sh)),
                        "run_seconds": round(time.time() - t0, 1), "rebuild": S.rebuild_record(before, sh, ("RC6", "AC4"), bools)}, t0=t0,
                        notes=["solid spigot tube below z = 0 to datum A: assumption", "thread phase arbitrary: helix starts at theta 0, z_run - pitch"])
    C.save("receiver", doc, body, res)
    return res


if __name__ in ("__main__", "receiver"):
    C.run_main("receiver", build)
