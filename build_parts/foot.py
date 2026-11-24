"""Bolt-down foot (BS7): plate foot.size, two M6 clearance holes on the rail slot pitch, one M8 floor-fastener hole. Local frame: x 0 to 100
(rail covers x 0 to 60), y centred, z 0 to 8."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("foot")
    L, W, T = g("foot.size")
    mx, my = g("foot.m6_xy")
    ov = g("collet.tool_overshoot")
    plate = S.box(0.0, L, -W / 2, W / 2, 0.0, T)
    m6 = [S.cyl_z(mx, s * my, g("foot.m6_hole") / 2, -ov, T + ov) for s in (-1, 1)]
    m8 = S.cyl_z(g("foot.m8_x"), 0.0, g("foot.m8_hole") / 2, -ov, T + ov)
    tool = rec.fuse("holes_tool_fuse", m6 + [m8])
    sh = S.solid_of(rec.cut("holes_cut", plate, tool))
    vol = lambda t: S.removed(t, plate)
    gap = lambda x: (lambda iv: iv[1][0] - iv[0][1])(C.line_ivals(sh, C.V(x, -W, T / 2), C.V(x, W, T / 2)))
    m8x = C.line_ivals(sh, C.V(0.0, 0.0, T / 2), C.V(L, 0.0, T / 2))
    m6y = C.line_ivals(sh, C.V(mx, -W, T / 2), C.V(mx, W, T / 2))
    m6_c = [(m6y[0][1] + m6y[1][0]) / 2 - W, (m6y[1][1] + m6y[2][0]) / 2 - W]
    rows = [
        S.row("BS7", "foot plate length (A)", plate.Volume, sh.BoundBox.XLength, L, S.TOL),
        S.row("BS7", "foot plate width (T)", plate.Volume, sh.BoundBox.YLength, W, S.TOL),
        S.row("BS7", "foot plate thickness (Z)", plate.Volume, sh.BoundBox.ZLength, T, S.TOL),
        S.row("BS7", "M6 hole diameter (D)", vol(m6[0]) + vol(m6[1]), m6y[1][0] - m6y[0][1], g("foot.m6_hole"), S.TOL),
        S.row("BS7", "M6 hole pitch across the rail slot lines (T)", vol(m6[0]) + vol(m6[1]), m6_c[1] - m6_c[0], 2 * my, S.TOL),
        S.row("BS7", "M8 hole diameter (D)", vol(m8), gap(g("foot.m8_x")), g("foot.m8_hole"), S.TOL),
        S.row("BS7", "M8 hole distance from the rail end, rail covers x 0 to profile.width (A)", vol(m8), (m8x[0][1] + m8x[1][0]) / 2 - g("profile.width"),
              g("foot.m8_x") - g("profile.width"), S.TOL, note="%g from the rail end" % (g("foot.m8_x") - g("profile.width"))),
    ]
    res = S.result("foot", sh, rows, rec)
    S.save_single("foot", sh, res)
    return res


if __name__ in ("__main__", "foot"):
    C.run_main("foot", build)
