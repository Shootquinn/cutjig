"""Holder: tube with 10 deg inner cone, flange, key, index notch (Rule P), four M6 insert bores. Local frame: bottom at z = 0.
Step 6 rebuild (HD7, AC5): witness tick groove on the flange rim at witness.azimuth_deg, in the same cut as the notch and inserts.
Step 7 rebuild (collar, Loftsman Revision 1, Topologist E1): collar ring r collar.id/2 to collar.od/2, z_top to z_top + collar.thickness, fused with the key
in the one Fuse boolean; each insert tool gains a collar.hole_dia cylinder through the ring so the ring leaves no void shell over the insert bores."""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadlib as C  # noqa: E402
import step6lib as S  # noqa: E402


def dims(p):
    g = lambda k: C.G(p, k)
    tan_a = math.tan(math.radians(g("cone.alpha")))
    r_od = g("receiver.register_bore_radius") - g("register.g_reg")
    r_cone_bot = r_od - g("chain.t_h")
    H = g("chain.H")
    h_wp = g("washer.thickness") - g("nut.washer_pocket_depth")
    return {
        "tan_a": tan_a, "r_od": r_od, "r_cone_bot": r_cone_bot, "H": H, "r_cone_top": r_cone_bot - H * tan_a,
        "L": g("holder.length"), "t_f": g("holder.flange_thickness"), "r_fl": g("holder.flange_od") / 2,
        "z_top": g("holder.length") + g("holder.flange_thickness") + h_wp + g("nut.plate_thickness") + g("nut.lift_play"),
        "r_col_in": g("collar.id") / 2, "r_col_out": g("collar.od") / 2, "t_col": g("collar.thickness"),
    }


def build():
    t0 = time.time()
    before = S.before_state("holder", S.BEFORE_DIR_7)
    p = C.params()
    g = lambda k: C.G(p, k)
    q = dims(p)
    th = g("receiver.key_offset_deg")
    doc, body = C.new_body("holder")
    pts = [(q["r_cone_bot"], 0), (q["r_od"], 0), (q["r_od"], q["L"]), (q["r_fl"], q["L"]), (q["r_fl"], q["L"] + q["t_f"]),
           (q["r_od"], q["L"] + q["t_f"]), (q["r_od"], q["z_top"]), (q["r_cone_top"], q["z_top"]),
           (q["r_cone_top"], q["H"])]
    C.body_revolve(doc, body, pts, "Tube")
    key = C.box_at(th, q["r_od"] - 1.0, q["r_od"] + g("holder.key_height"), g("holder.key_width") / 2, 0.0, g("holder.key_length"))
    ring = C.revolve_solid([(q["r_col_in"], q["z_top"]), (q["r_col_out"], q["z_top"]), (q["r_col_out"], q["z_top"] + q["t_col"]), (q["r_col_in"], q["z_top"] + q["t_col"])])
    key_collar = C.fuse_all([key, ring])
    f_tube = len(C.final_shape(body).Faces)
    C.body_boolean(doc, body, key_collar, "Fuse", "KeyCollar")
    pre_key = C.final_shape(body)
    bools = [{"name": "KeyCollar", "kind": "fuse", "faces_before": f_tube, "faces_after": len(pre_key.Faces), "tool_faces": len(key_collar.Faces)}]
    notch_deg = -th
    n_ins = g("holder.insert_count")
    tools = [C.box_at(notch_deg, q["r_fl"] - g("holder.index_notch_depth"), q["r_fl"] + 1.0, g("holder.index_notch_width") / 2,
                      q["L"] - 1.0, q["L"] + q["t_f"] + 1.0)]
    import Part
    ins_deg = [360.0 / n_ins * (k + 0.5) for k in range(n_ins)]
    for a in ins_deg:
        c = Part.makeCylinder(g("holder.insert_dia") / 2, g("holder.insert_depth") + 1.0,
                              C.polar(g("holder.insert_circle_radius"), a, q["z_top"] - g("holder.insert_depth")), C.V(0, 0, 1))
        tools.append(c)
        tools.append(Part.makeCylinder(g("collar.hole_dia") / 2, q["t_col"] + g("collet.tool_overshoot"), C.polar(g("holder.insert_circle_radius"), a, q["z_top"]), C.V(0, 0, 1)))
    ov = g("collet.tool_overshoot")
    az_w = g("witness.azimuth_deg")
    tick = C.box_at(az_w, q["r_fl"] - g("witness.tick_depth"), q["r_fl"] + ov, g("witness.tick_width") / 2, q["L"] - ov, q["L"] + g("witness.tick_height"))
    tick_mm3 = S.removed(tick, pre_key)
    tools.append(tick)
    tool = C.fuse_all(tools)
    C.body_boolean(doc, body, tool, "Cut", "NotchInsertsTick")
    sh = C.final_shape(body)
    bools.append({"name": "NotchInsertsTick", "kind": "cut", "faces_before": len(pre_key.Faces), "faces_after": len(sh.Faces), "tool_faces": len(tool.Faces)})

    clr = th + 180.0
    R = lambda z, th_=clr, r1=90: C.radial_ivals(sh, th_, z, 0, r1)
    r_in = lambda z: R(z)[0][0]
    slope = (r_in(5.0) - r_in(10.0)) / 5.0
    r_top = r_in(q["H"] + 5.0)
    h_meas = 10.0 + (r_in(10.0) - r_top) / slope
    fl = C.axial_ivals(sh, clr, (q["r_od"] + q["r_fl"]) / 2, -1, q["z_top"] + 1)
    tk = C.tangential_ivals(sh, th, q["r_od"] + g("holder.key_height") / 2, 20.0, 20.0)
    kr = C.radial_ivals(sh, th, 20.0, 0, 90)
    kz = C.axial_ivals(sh, th, q["r_od"] + g("holder.key_height") / 2, -1, 80)
    nt = C.tangential_ivals(sh, notch_deg, q["r_fl"] - 0.5, q["L"] + q["t_f"] / 2, 20.0)
    nr = C.radial_ivals(sh, notch_deg, q["L"] + q["t_f"] / 2, 0, 90)
    ia = C.axial_ivals(sh, ins_deg[0], g("holder.insert_circle_radius"), 0, q["z_top"] + 1)
    it = C.tangential_ivals(sh, ins_deg[0], g("holder.insert_circle_radius"), q["z_top"] - 1.0, 10.0)
    tk_w = C.tangential_ivals(sh, az_w, q["r_fl"] - g("witness.tick_depth") / 2, q["L"] + g("witness.tick_height") / 2, 5.0)
    tk_r = C.radial_ivals(sh, az_w, q["L"] + g("witness.tick_height") / 2, 0, 90)
    tk_a = C.axial_ivals(sh, az_w, q["r_fl"] - g("witness.tick_depth") / 2, -1, q["z_top"] + 1)
    under_other = C.axial_ivals(sh, az_w + 120.0, q["r_fl"] - g("witness.tick_depth") / 2, -1, q["z_top"] + 1)
    col_iv = C.axial_ivals(sh, clr, (q["r_col_in"] + q["r_cone_top"]) / 2.0, -1, q["z_top"] + q["t_col"] + 1)          # inside the tube bore radius: the ring overhang only
    col_r = C.radial_ivals(sh, clr, q["z_top"] + q["t_col"] / 2.0, 0, 90)
    ch_t = C.tangential_ivals(sh, ins_deg[0], g("holder.insert_circle_radius"), q["z_top"] + q["t_col"] / 2.0, 10.0)
    collar_holes = sum(1 for a in ins_deg if not sh.isInside(C.polar(g("holder.insert_circle_radius"), a, q["z_top"] + q["t_col"] / 2.0), 1e-6, True))
    feats = [
        C.chk("holder outer diameter (D) = 2 (register r - g_reg)", 2 * R(20.0)[0][1], 2 * q["r_od"]),
        C.chk("inner cone radius at bottom (R)", r_in(0.001), q["r_cone_bot"], 0.01),
        C.chk("`cone.alpha` measured from r(z) slope (deg)", math.degrees(math.atan(slope)), g("cone.alpha"), 0.05),
        C.chk("cone height `chain.H` (A)", h_meas, q["H"]),
        C.chk("inner cone radius at top (R)", r_top, q["r_cone_top"], 0.01),
        C.chk("bore above the cone (D)", 2 * r_top, 2 * q["r_cone_top"]),
        C.chk("`holder.length` bottom to flange underside (A)", fl[0][0], g("holder.length")),
        C.chk("`holder.flange_thickness` (A)", fl[0][1] - fl[0][0], g("holder.flange_thickness")),
        C.chk("`holder.flange_od` (D)", 2 * R(q["L"] + q["t_f"] / 2)[0][1], g("holder.flange_od")),
        C.chk("holder tube top height (A) = length + flange + washer proud + plate + lift play = collar underside", col_iv[0][0] if col_iv else None, q["z_top"]),
        C.chk("`collar.thickness` ring height (A)", col_iv[0][1] - col_iv[0][0] if col_iv else None, q["t_col"]),
        C.chk("holder top = collar top = tube top + `collar.thickness` (A)", C.bbox(sh).ZMax, q["z_top"] + q["t_col"]),
        C.chk("`collar.id` / 2 ring inner radius (R)", col_r[0][0] if col_r else None, q["r_col_in"]),
        C.chk("`collar.od` / 2 ring outer radius (R)", col_r[-1][1] if col_r else None, q["r_col_out"]),
        C.chk("`collar.hole_dia` hole through the ring over the insert bore (D)", ch_t[1][0] - ch_t[0][1] if len(ch_t) == 2 else None, g("collar.hole_dia")),
        C.chk("collar holes open (insert bore reaches the ring top), count", collar_holes, n_ins, 0.01),
        C.chk("shell count (no void shell under the ring)", len(sh.Shells), 1, 0.01),
        C.chk("`holder.key_width` (T)", tk[0][1] - tk[0][0] if len(tk) == 1 else None, g("holder.key_width")),
        C.chk("`holder.key_height` (R)", kr[-1][1] - q["r_od"], g("holder.key_height")),
        C.chk("`holder.key_length` (A)", kz[0][1] - kz[0][0], g("holder.key_length")),
        C.chk("key azimuth = `receiver.key_offset_deg` (key present at azimuth, absent opposite)",
              th if (kr[-1][1] > q["r_od"] + 1 and R(20.0)[0][1] < q["r_od"] + 0.01) else None, th, 0.01),
        C.chk("Rule P index notch width (T)", nt[1][0] - nt[0][1] if len(nt) == 2 else None, g("holder.index_notch_width")),
        C.chk("Rule P index notch depth (R)", q["r_fl"] - nr[0][1] if nr else None, g("holder.index_notch_depth")),
        C.flag("Rule P index notch off-axis (azimuth not 0/90/180/270)", (notch_deg % 90.0) > 1.0),
        C.chk("insert bore depth (A)", q["z_top"] - ia[0][1] if ia else None, g("holder.insert_depth")),
        C.chk("insert bore diameter (D)", it[1][0] - it[0][1] if len(it) == 2 else None, g("holder.insert_dia")),
        C.chk("insert circle radius", (lambda iv: (iv[0][1] + iv[1][0]) / 2 if len(iv) >= 2 else None)(C.radial_ivals(sh, ins_deg[0], q["z_top"] - 1.0, 0, 90)), g("holder.insert_circle_radius")),
    ]
    inserts_present = 0
    for a in ins_deg:
        pt = C.polar(g("holder.insert_circle_radius"), a, q["z_top"] - 1.0)
        inserts_present += 0 if sh.isInside(pt, 1e-6, True) else 1
    feats.append(C.chk("insert bore count (`holder.insert_count`)", inserts_present, n_ins, 0.01))
    hd7 = [
        ("HD7 tick groove width (T)", tk_w[1][0] - tk_w[0][1] if len(tk_w) == 2 else None, g("witness.tick_width"), 0.02),
        ("HD7 tick groove depth from the flange OD (R)", q["r_fl"] - tk_r[-1][1] if tk_r else None, g("witness.tick_depth"), 0.02),
        ("HD7 tick groove height above the flange underside (A)", tk_a[0][0] - q["L"] if tk_a else None, g("witness.tick_height"), 0.02),
        ("HD7 tick lower edge = flange underside (A)", under_other[0][0] if under_other else None, g("holder.length"), 0.02),
        ("HD7 tick azimuth = witness.azimuth_deg (deg), groove empty at the azimuth, flange solid at +-120",
         az_w if (not sh.isInside(C.polar(q["r_fl"] - g("witness.tick_depth") / 2, az_w, q["L"] + ov), 1e-6, True)
                  and sh.isInside(C.polar(q["r_fl"] - g("witness.tick_depth") / 2, az_w + 120.0, q["L"] + ov), 1e-6, True)) else None, az_w, S.TOL),
    ]
    for name, built, exp, tol in hd7:
        r = C.chk(name, built, exp, tol)
        r.update({"id": "HD7", "volume_mm3": round(tick_mm3, 3)})
        feats.append(r)
    res = C.base_result("holder", sh, feats, extra={"derived": {k: round(v, 4) for k, v in q.items()}, "booleans": bools, "boolean_count": len(bools),
                        "bbox_plain": S._bb(sh.BoundBox), "bbox_optimal": S._bb(C.bbox(sh)), "run_seconds": round(time.time() - t0, 1),
                        "collar": {"r_in": q["r_col_in"], "r_out": q["r_col_out"], "z_lo": q["z_top"], "z_hi": q["z_top"] + q["t_col"], "hole_dia": g("collar.hole_dia"), "hole_count": collar_holes},
                        "witness": {"azimuth_deg": az_w, "tick_lowest_z": q["L"], "tick_height": g("witness.tick_height")},
                        "rebuild": S.rebuild_record(before, sh, ("HD7", "AC5", "collar", "E1"), bools)}, t0=t0)
    C.save("holder", doc, body, res)
    return res


if __name__ == "__main__" or __name__ == "holder":
    C.run_main("holder", build)
