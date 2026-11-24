"""Drain plug (BS6): knob head with grip lug, flange, shank. Own part (Loftsman C5). World frame: shank bottom on the plate top z = base.plate_thickness,
axis at base.drain_xy. Fuse first: one multiFuse of three cylinders and the lug box (fix pass D6: box along X, plug.lug_length x plug.lug_width x
plug.lug_height above the head top, embedded plug.lug_embed in the head)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("plug")
    cx, cy = g("base.drain_xy")
    z0 = g("base.plate_thickness")
    z1 = z0 + g("plug.shank_h")
    z2 = z1 + g("plug.flange_t")
    z3 = z2 + g("plug.head_h")
    lug_l, lug_w, lug_h, lug_e = g("plug.lug_length"), g("plug.lug_width"), g("plug.lug_height"), g("plug.lug_embed")
    lug = S.box(cx - lug_l / 2, cx + lug_l / 2, cy - lug_w / 2, cy + lug_w / 2, z3 - lug_e, z3 + lug_h)
    parts = [S.cyl_z(cx, cy, g("plug.shank_dia") / 2, z0, z1), S.cyl_z(cx, cy, g("plug.flange_dia") / 2, z1, z2),
             S.cyl_z(cx, cy, g("plug.head_dia") / 2, z2, z3), lug]
    sh = S.solid_of(rec.fuse("plug_fuse", parts))
    rad = lambda z: C.radial_ivals(sh, 0.0, z, cx, cx + g("plug.head_dia"))[-1][1] - cx
    z_l = z3 + lug_h / 2
    lx = C.line_ivals(sh, C.V(cx - lug_l, cy, z_l), C.V(cx + lug_l, cy, z_l))
    ly = C.line_ivals(sh, C.V(cx, cy - lug_l, z_l), C.V(cx, cy + lug_l, z_l))
    lz = C.line_ivals(sh, C.V(cx + lug_l / 4, cy, z0 - 1.0), C.V(cx + lug_l / 4, cy, z3 + lug_h + 1.0))
    # shank-to-bore gap: minimum distance from the plug to a tube standing for the tray drain bore wall
    bore_r = g("tray.drain_dia") / 2
    tube = S.cyl_z(cx, cy, bore_r + g("plug.head_dia"), z0, z1).cut(S.cyl_z(cx, cy, bore_r, z0 - 1.0, z1 + 1.0))
    shank = sh.common(S.cyl_z(cx, cy, g("plug.head_dia"), z0 - 1.0, z1 - 0.5))     # the shank as built, below the flange
    gap = shank.distToShape(tube)[0]
    ins = lambda x, y, z: sh.isInside(C.V(x, y, z), 1e-6, True)
    corner_ok = ins(cx + lug_l / 2 - 0.01, cy + lug_w / 2 - 0.01, z3 + lug_h / 2) and ins(cx + lug_l / 2 - 0.01, cy + lug_w / 2 - 0.01, z3 - lug_e / 2)
    rows = [
        S.row("BS6", "plug head diameter (D)", parts[2].Volume, 2 * rad((z2 + z3) / 2), g("plug.head_dia")),
        S.row("BS6", "plug flange diameter (D)", parts[1].Volume, 2 * rad((z1 + z2) / 2), g("plug.flange_dia")),
        S.row("BS6", "plug shank diameter (D)", parts[0].Volume, 2 * rad((z0 + z1) / 2), g("plug.shank_dia")),
        S.row("BS6", "plug overall height (A) = shank + flange + head + lug", sh.Volume, sh.BoundBox.ZLength,
              g("plug.shank_h") + g("plug.flange_t") + g("plug.head_h") + lug_h),
        S.row("BS6", "plug grip lug length along X (L) = plug.lug_length", lug.Volume, (lx[0][1] - lx[0][0]) if lx else None, lug_l),
        S.row("BS6", "plug grip lug width along Y (T) = plug.lug_width", lug.Volume, (ly[0][1] - ly[0][0]) if ly else None, lug_w),
        S.row("BS6", "plug grip lug height above the head top (A) = plug.lug_height", lug.Volume, (lz[-1][1] - 1.0 - (z3 - z0)) if lz else None, lug_h),
        S.row("BS6", "plug grip lug corner stands on the head (corner point of the lug and the head under it are solid)", lug.Volume, int(corner_ok), 1, S.TOL,
              ok=corner_ok),
        S.row("BS6", "shank in the plain drain bore: radial gap R (minimum distance to the bore wall, bore thread named in the tray row)", shank.Volume, gap,
              (g("tray.drain_dia") - g("plug.shank_dia")) / 2, 1e-6),
    ]
    res = S.result("plug", sh, rows, rec)
    S.save_single("plug", sh, res)
    return res


if __name__ in ("__main__", "plug"):
    C.run_main("plug", build)
