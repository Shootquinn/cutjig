"""Alignment gauge (AC2): register plug gauge.register_plug_dia x gauge.length with the holder key at receiver.key_offset_deg, cavity from below
(gauge.cavity), handle bar on top (gauge.handle). Local frame: plug bottom at z = 0, axis Z. One revolve (cavity in the profile), one fuse."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("gauge")
    th = g("receiver.key_offset_deg")
    r_p, Lg = g("gauge.register_plug_dia") / 2, g("gauge.length")
    cav_d, cav_h = g("gauge.cavity")
    hb_l, hb_w, hb_h = g("gauge.handle")
    ov = g("collet.tool_overshoot")
    kh, kw, kl = g("holder.key_height"), g("holder.key_width"), g("holder.key_length")
    body = C.revolve_solid([(cav_d / 2, 0.0), (r_p, 0.0), (r_p, Lg), (0.0, Lg), (0.0, cav_h), (cav_d / 2, cav_h)])
    key = C.box_at(th, r_p - ov, r_p + kh, kw / 2, 0.0, kl)
    bar = S.box(-hb_l / 2, hb_l / 2, -hb_w / 2, hb_w / 2, Lg - ov, Lg + hb_h)
    sh = S.solid_of(rec.fuse("plug_key_bar_fuse", [body, key, bar]))
    clr = th + 180.0
    rad = C.radial_ivals(sh, clr, Lg / 2, 0, r_p + 10)
    ax = C.axial_ivals(sh, clr, (cav_d / 2 + r_p) / 2, -1, Lg + hb_h + 1)
    cav_ax = C.axial_ivals(sh, clr, cav_d / 4, -1, Lg + hb_h + 1)
    ktan = C.tangential_ivals(sh, th, r_p + kh / 2, kl / 2, S.SCAN)
    krad = C.radial_ivals(sh, th, kl / 2, 0, r_p + 10)
    kax = C.axial_ivals(sh, th, r_p + kh / 2, -1, Lg + hb_h + 1)
    bar_x = C.line_ivals(sh, C.V(-hb_l, 0, Lg + hb_h / 2), C.V(hb_l, 0, Lg + hb_h / 2))
    bar_y = C.line_ivals(sh, C.V(0, -hb_l, Lg + hb_h / 2), C.V(0, hb_l, Lg + hb_h / 2))
    vol_key = key.cut(body).Volume
    rows = [
        S.row("AC2", "gauge plug diameter (D)", body.Volume, 2 * rad[-1][1], g("gauge.register_plug_dia"), S.TOL),
        S.row("AC2", "gauge plug length (A)", body.Volume, ax[0][1] - ax[0][0], Lg, S.TOL),
        S.row("AC2", "gauge cavity diameter (D)", body.Volume, 2 * rad[0][0], cav_d, S.TOL),
        S.row("AC2", "gauge cavity depth from below (A)", body.Volume, cav_ax[0][0] if cav_ax else None, cav_h, S.TOL),
        S.row("AC2", "gauge key width (T)", vol_key, ktan[-1][1] - ktan[0][0] if len(ktan) == 1 else None, kw, S.TOL),
        S.row("AC2", "gauge key height (R)", vol_key, krad[-1][1] - r_p, kh, S.TOL),
        S.row("AC2", "gauge key length (A)", vol_key, kax[0][1] - kax[0][0], kl, S.TOL),
        S.row("AC2", "gauge key azimuth = receiver.key_offset_deg (deg): key present, absent opposite",
              vol_key, th if (krad[-1][1] > r_p + 1 and rad[-1][1] < r_p + S.TOL) else None, th, S.TOL),
        S.row("AC2", "gauge handle bar length (L)", hb_l * hb_w * hb_h, bar_x[-1][1] - bar_x[0][0], hb_l, S.TOL),
        S.row("AC2", "gauge handle bar width (T)", hb_l * hb_w * hb_h, bar_y[-1][1] - bar_y[0][0], hb_w, S.TOL),
        S.row("AC2", "gauge overall height (A)", sh.Volume, sh.BoundBox.ZMax, Lg + hb_h, S.TOL),
    ]
    res = S.result("gauge", sh, rows, rec)
    S.save_single("gauge", sh, res)
    return res


if __name__ in ("__main__", "gauge"):
    C.run_main("gauge", build)
