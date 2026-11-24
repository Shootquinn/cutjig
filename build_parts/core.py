"""Core stand-in (Detail 7, L2): plain cylinder of diameter d and length L about the Z axis, bottom end square at z = 0, top end chamfered core.top_chamfer x 45 deg
(Rule P: the chamfer on the top end only). make_core(d, length) is imported by the pose assembler; build() writes parts_cache/core.FCStd for d = core.diameter_nominal
and length = core.length_capture. One revolve, no boolean."""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def make_core(d, length, p=None):
    """Core solid, local frame: axis Z through the origin, bottom face z = 0, top end z = length."""
    p = p or C.params()
    ch = C.G(p, "core.top_chamfer")
    r = d / 2.0
    import Part
    w = Part.makePolygon([C.V(0, 0, 0), C.V(r, 0, 0), C.V(r, 0, length - ch), C.V(r - ch, 0, length), C.V(0, 0, length), C.V(0, 0, 0)])
    return Part.Face(w).revolve(C.V(0, 0, 0), C.V(0, 0, 1), 360)


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("core")
    d, L, ch = g("core.diameter_nominal"), g("core.length_capture"), g("core.top_chamfer")
    sh = make_core(d, L, p)
    r = d / 2.0
    inside = lambda pt: sh.isInside(pt, 1e-6, True)
    # radius at z mid, at the bottom face and just under the top face, read from the built shape
    r_mid = C.radial_ivals(sh, 20.0, L / 2.0, 0.0, r + 5.0)
    r_bot = C.radial_ivals(sh, 20.0, 0.001, 0.0, r + 5.0)
    r_top = C.radial_ivals(sh, 20.0, L - 0.001, 0.0, r + 5.0)
    ax = C.axial_ivals(sh, 20.0, r - 0.5 * ch, -1.0, L + 1.0)
    bb = sh.BoundBox
    rows = [
        S.row("L2", "core diameter = core.diameter_nominal (D)", sh.Volume, 2 * r_mid[-1][1] if r_mid else None, d, S.TOL),
        S.row("L2", "core length = core.length_capture (A)", sh.Volume, bb.ZLength, L, S.TOL),
        S.row("L2", "bottom end square: radius at z 0.001 equals the full radius (R)", sh.Volume, r_bot[-1][1] if r_bot else None, r, 0.01),
        S.row("L2", "top end chamfered: radius at z top - 0.001 equals r - core.top_chamfer (R)", sh.Volume, r_top[-1][1] if r_top else None, r - ch, 0.01),
        S.row("L2", "chamfer height core.top_chamfer (A): side wall ends at top - chamfer", sh.Volume, (L - ax[0][1] + ch / 2.0) if ax else None, ch, 0.01),
        S.row("L2", "Rule P single-end chamfer: bottom corner solid, top corner removed", sh.Volume,
              int(inside(C.polar(r - 0.05, 20.0, 0.1)) and not inside(C.polar(r - 0.05, 20.0, L - 0.05)) and inside(C.polar(r - ch - 0.05, 20.0, L - 0.05))), 1, S.TOL),
        S.row("L2", "axis x = y = 0 (bbox centre offset)", sh.Volume, math.hypot((bb.XMin + bb.XMax) / 2, (bb.YMin + bb.YMax) / 2), 0.0, S.TOL),
    ]
    res = S.result("core", sh, rows, rec, extra={"diameter": d, "length": L, "top_chamfer": ch, "recorded_lengths": [g("core.length_capture"), g("core.length_install"), g("core.length_optional")]})
    S.save_single("core", sh, res)
    return res


if __name__ in ("__main__", "core"):
    C.run_main("core", build)
