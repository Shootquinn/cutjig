"""T-nut proxy (FR3): PZRT 3030 roll-in spring M6 has no CAD on disk. Envelope from profile.* and tnut.*; local frame, top flush at z = 0.
Instanced 8 per bracket by frame.py (ASSUMED)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402
import hardware_geom as HG  # noqa: E402


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("tnut")
    sh, parts = HG.tnut_shape(p, rec)
    bw, bl, bh = g("tnut.body")
    nw, nl, nh = g("tnut.neck")
    ch = g("tnut.chamfer")
    # measurements on the final solid
    n_y = C.line_ivals(sh, C.V(nl / 4, -bw, -nh / 2), C.V(nl / 4, bw, -nh / 2))
    eps = S.TOL
    b_y = C.line_ivals(sh, C.V(bl / 4, -bw, -nh - eps), C.V(bl / 4, bw, -nh - eps))
    bot_y = C.line_ivals(sh, C.V(bl / 4, -bw, parts["z_bot"] + eps), C.V(bl / 4, bw, parts["z_bot"] + eps))
    n_x = C.line_ivals(sh, C.V(-bl, nw / 4, -nh / 2), C.V(bl, nw / 4, -nh / 2))
    hole_x = C.line_ivals(sh, C.V(-bl, 0, -nh / 2), C.V(bl, 0, -nh / 2))
    zz = C.line_ivals(sh, C.V(bl / 4, nw / 4, 2.0), C.V(bl / 4, nw / 4, -3 * bh))
    w = lambda iv: iv[-1][1] - iv[0][0] if iv else None
    rows = [
        S.row("FR3", "T-nut proxy overall height (A) = neck + body", sh.Volume, w(zz), nh + bh, S.TOL),
        S.row("FR3", "T-nut proxy body width across the slot (T)", sh.Volume, w(b_y), bw, S.TOL),
        S.row("FR3", "T-nut proxy neck width, under the profile opening (T)", sh.Volume, w(n_y), nw, S.TOL),
        S.row("FR3", "T-nut proxy neck length along the slot (L)", sh.Volume, w(n_x), nl, S.TOL),
        S.row("FR3", "T-nut proxy bottom width after the 45 deg chamfers (T)", sh.Volume, w(bot_y), bw - 2 * ch + 2 * eps, 0.001),
        S.row("FR3", "T-nut proxy tapped-hole region diameter (D)", parts["hole"].common(parts["body"].fuse(parts["neck"])).Volume,
              (hole_x[1][0] - hole_x[0][1]) if len(hole_x) == 2 else None, g("tnut.hole"), S.TOL),
    ]
    res = S.result("tnut", sh, rows, rec, extra={"assumption": "PZRT 3030 has no CAD on disk; proxy envelope from profile.* (ASSUMED)",
                                                   "cavity_width": g("profile.slot_cavity_width"), "opening": g("profile.slot_opening")})
    S.save_single("tnut", sh, res)
    return res


if __name__ in ("__main__", "tnut"):
    C.run_main("tnut", build)
