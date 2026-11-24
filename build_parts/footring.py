"""Collet foot ring (generator feature) for core family index 0: ring, lip, core seat ledge, foot key.
Slits and relief holes belong to the collet generator, not this part (a slit-cut ring is six solids)."""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadlib as C  # noqa: E402


def derived(p, d):
    return C.footring_derived(p, d)


def build(d=None):
    t0 = time.time()
    p = C.params()
    g = lambda k: C.G(p, k)
    d = d if d is not None else g("core.diameters")[0]
    q = derived(p, d)
    th = g("receiver.key_offset_deg")
    seat_h, seat_w = g("collet.core_seat_height"), g("collet.core_seat_width")
    r_in = q["r_bore"] - seat_w
    doc, body = C.new_body("footring")
    C.body_revolve(doc, body, [(r_in, 0), (q["r_fo"], 0), (q["r_fo"], q["ring_top"]), (q["r_bore"], q["ring_top"]),
                               (q["r_bore"], seat_h), (r_in, seat_h)], "Ring")
    key = C.box_at(th, q["r_fo"] - 1.0, q["r_key_tip"], g("holder.key_width") / 2, 0.0, q["ring_top"])
    C.body_boolean(doc, body, key, "Fuse", "FootKey")
    sh = C.final_shape(body)
    clear = th + 180.0
    rz = C.radial_ivals(sh, clear, q["ring_top"] / 2, 0, q["r_fo"] + 10)
    rl = C.radial_ivals(sh, clear, seat_h - 0.1, 0, q["r_fo"] + 10)          # ledge level
    rk = C.radial_ivals(sh, th, q["ring_top"] / 2, 0, q["r_key_tip"] + 10)
    ax_ring = C.axial_ivals(sh, clear, (q["r_bore"] + q["r_fo"]) / 2, -1, 10)
    ax_ledge = C.axial_ivals(sh, clear, (r_in + q["r_bore"]) / 2, -1, 10)
    ax_key = C.axial_ivals(sh, th, (q["r_fo"] + q["r_key_tip"]) / 2 + 1.0, -1, 10)
    tk = C.tangential_ivals(sh, th, (q["r_fo"] + q["r_key_tip"]) / 2 + 1.0, q["ring_top"] / 2, 20.0)
    feats = [
        C.chk("ring height `holder.bottom_above_floor_Kmax` (top z = 2.0 - fit.model_contact_gap)", ax_ring[0][1], q["ring_top"], 0.001),
        C.chk("ring OD radius (register bore - seat_clearance)", rz[0][1], q["r_fo"]),
        C.chk("`collet.foot_ring_width` lip beyond cone base (R)", rz[0][1] - q["r_cone_base"], g("collet.foot_ring_width")),
        C.chk("`collet.core_seat_height` (A)", ax_ledge[0][1], seat_h),
        C.chk("`collet.core_seat_width` (R)", rl[0][1] - rl[0][0] if len(rl) == 1 else None, seat_w + 0.0, 0.05,
              "interval at ledge level spans ledge only plus ring wall; see ledge ID"),
        C.chk("ledge ID = B_f - 2 x seat width (D)", 2 * rl[0][0], (d + g("core.tol") + g("collet.c_i")) - 2 * seat_w),
        C.chk("foot key radial tip", rk[-1][1], q["r_key_tip"]),
        C.chk("foot key width `holder.key_width` (T)", tk[0][1] - tk[0][0] if len(tk) == 1 else None, g("holder.key_width")),
        C.chk("foot key top = ring top (same plane)", ax_key[0][1], q["ring_top"], 0.001),
        C.flag("Rule P foot key off-axis (key azimuth not 0/90/180/270)", (th % 90.0) > 1.0),
    ]
    # ledge level interval spans ledge+ring wall (ledge top 2.5 > ring top 1.995, so only the ledge is solid at z = seat_h - 0.1)
    res = C.base_result("footring", sh, feats, extra={"d_core": d, "derived": {k: round(v, 4) for k, v in q.items()}}, t0=t0,
                        notes=["slits and relief holes not in this part: slit-cut ring is six solids; they belong to the collet generator"])
    C.save("footring", doc, body, res)
    return res


if __name__ == "__main__" or __name__ == "footring":
    C.run_main("footring", build)
