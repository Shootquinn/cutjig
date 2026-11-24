"""Receiver: externally threaded cup. Floor frame: floor top z = 0, bottom at datum A (z = -icd.floor_above_datum_a).
Spigot (r = receiver.spigot_od / 2) below the shoulder; 6-turn right-hand 45/45 thread above; register bore; key slot; floor hole."""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadlib as C  # noqa: E402


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


def build():
    t0 = time.time()
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
    C.body_helix_cut(doc, body, [(q["r_min"], zc - hw_root), (r_out, zc - hw_cap), (r_out, zc + hw_cap), (q["r_min"], zc + hw_root)],
                     P, q["z_top"] - q["z_run"] + P, "Thread")
    slot = C.box_at(th, q["r_reg"] - 1.0, q["r_reg"] + g("receiver.key_slot_depth"), g("receiver.key_slot_width") / 2, 0.0, q["z_top"] + 1.0)
    C.body_boolean(doc, body, slot, "Cut", "KeySlot")
    sh = C.final_shape(body)
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
    res = C.base_result("receiver", sh, feats, extra={"derived": {k: round(v, 4) for k, v in q.items()}}, t0=t0,
                        notes=["solid spigot tube below z = 0 to datum A: assumption", "thread phase arbitrary: helix starts at theta 0, z_run - pitch"])
    C.save("receiver", doc, body, res)
    return res


if __name__ in ("__main__", "receiver"):
    C.run_main("receiver", build)
