"""PTFE washer: ring 136.8 / 143.2 / 1.3 with one off-axis radial tab notch (Rule P). All values from params.yaml."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadlib as C  # noqa: E402
import math  # noqa: E402


def build():
    t0 = time.time()
    p = C.params()
    g = lambda k: C.G(p, k)
    r_i, r_o, t = g("washer.id") / 2, g("washer.od") / 2, g("washer.thickness")
    nw, nd = g("washer.notch_width"), g("washer.notch_depth")
    th = g("receiver.key_offset_deg")      # notch indexed to the key azimuth (assumption)
    doc, body = C.new_body("washer")
    C.body_revolve(doc, body, [(r_i, 0), (r_o, 0), (r_o, t), (r_i, t)], "Ring")
    cut = C.box_at(th, r_o - nd, r_o + 1.0, nw / 2, -1.0, t + 1.0)
    C.body_boolean(doc, body, cut, "Cut", "TabNotch")
    sh = C.final_shape(body)
    # Rule M predicates, all from sh
    ri = C.radial_ivals(sh, th + 180.0, t / 2, 0, r_o + 5)           # clear azimuth
    rn = C.radial_ivals(sh, th, t / 2, 0, r_o + 5)                   # through the notch
    tn = C.tangential_ivals(sh, th, r_o - nd / 2, t / 2, 20.0)       # notch width at mid depth
    ax = C.axial_ivals(sh, th + 180.0, (r_i + r_o) / 2, -2, t + 2)
    feats = [
        C.chk("washer.id (D)", 2 * ri[0][0], g("washer.id")),
        C.chk("washer.od (D)", 2 * ri[0][1], g("washer.od")),
        C.chk("washer.thickness", ax[0][1] - ax[0][0], t),
        C.chk("washer.notch_depth (R)", ri[0][1] - rn[0][1], nd),
        C.chk("notch floor radius", rn[0][1], r_o - nd),
        C.chk("washer.notch_width (T)", tn[1][0] - tn[0][1], nw),
        C.flag("Rule P notch off-axis (azimuth not 0/90/180/270)", (th % 90.0) > 1.0),
    ]
    res = C.base_result("washer", sh, feats, t0=t0)
    C.save("washer", doc, body, res)
    return res


if __name__ == "__main__" or __name__ == "washer":
    C.run_main("washer", build)
