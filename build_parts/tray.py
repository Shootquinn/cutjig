"""Debris tray (BS5, BS6). World frame (datum A): tray bottom on the plate top z = base.plate_thickness, centred on the origin. Outer tray.length x
tray.width x tray.depth, wall tray.wall, floor top above the plate top = max(f, h) with f = tray.floor_min + |x - drain x| tan(tray.floor_slope_deg) and
h = tray.floor_min + |y - drain y| tan(tray.cross_fall_deg): the floor falls to the drain everywhere (fix pass D5). Cavity = xz prism common yz prism
over tray.fall_x; spot face tray.drain_spot_r flat at tray.floor_min under the plug flange; column reliefs tray.relief at each long edge (open to the edge);
spigot hole tray.hole_r; plain drain bore tray.drain_dia at base.drain_xy (Pass 1 form: the bore carries the thread name in its feature row).
The cavity common is a recorded boolean on tool primitives; one tool fuse, one cut on the outer block."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def fall_height(g, x, y):
    """Floor top above the plate top at (x, y): max of the x fall and the y fall, both measured from the drain centre."""
    dx, dy = g("base.drain_xy")
    f = g("tray.floor_min") + abs(x - dx) * math.tan(math.radians(g("tray.floor_slope_deg")))
    h = g("tray.floor_min") + abs(y - dy) * math.tan(math.radians(g("tray.cross_fall_deg")))
    return max(f, h)


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("tray")
    ov = g("collet.tool_overshoot")
    zb = g("base.plate_thickness")
    Lx, Wy, D, wall = g("tray.length"), g("tray.width"), g("tray.depth"), g("tray.wall")
    fx0, fx1 = g("tray.fall_x")
    ztop = zb + D
    fmin = g("tray.floor_min")
    dx, dy = g("base.drain_xy")
    yi = Wy / 2 - wall
    outer = S.box(-Lx / 2, Lx / 2, -Wy / 2, Wy / 2, zb, ztop)
    zf = lambda x, y: zb + fall_height(g, x, y)
    cav_xz = S.extrude_poly([(fx0, zf(fx0, dy)), (dx, zb + fmin), (fx1, zf(fx1, dy)), (fx1, ztop + ov), (fx0, ztop + ov)], "xz", -yi, yi)
    cav_yz = S.extrude_poly([(-yi, zf(dx, -yi)), (dy, zb + fmin), (yi, zf(dx, yi)), (yi, ztop + ov), (-yi, ztop + ov)], "yz", fx0, fx1)
    cavity = rec.common("cavity_xz_common_yz", cav_xz, cav_yz)
    spot = S.cyl_z(dx, dy, g("tray.drain_spot_r"), zb + fmin, ztop + ov)
    rw, rd = g("tray.relief")
    reliefs = [S.box(-rw / 2, rw / 2, Wy / 2 - rd, Wy / 2 + ov, zb - ov, ztop + ov), S.box(-rw / 2, rw / 2, -Wy / 2 - ov, -Wy / 2 + rd, zb - ov, ztop + ov)]
    hole = S.cyl_z(0.0, 0.0, g("tray.hole_r"), zb - ov, ztop + ov)
    bore = S.cyl_z(dx, dy, g("tray.drain_dia") / 2, zb - ov, ztop + ov)
    vols = {"cavity": S.removed(cavity, outer), "spot": S.removed(spot, outer), "reliefs": sum(S.removed(r, outer) for r in reliefs),
            "hole": S.removed(hole, outer), "bore": S.removed(bore, outer)}
    tool = rec.fuse("tools_fuse", [cavity, spot] + reliefs + [hole, bore])
    sh = S.solid_of(rec.cut("tools_cut", outer, tool))
    # ---- measurements on the final solid
    xs = C.line_ivals(sh, C.V(-Lx, Wy / 4.0, ztop - 1.0), C.V(Lx, Wy / 4.0, ztop - 1.0))
    ys = C.line_ivals(sh, C.V(-Lx / 5.0, -Wy, ztop - 1.0), C.V(-Lx / 5.0, Wy, ztop - 1.0))

    def z_at(x, y):
        iv = C.line_ivals(sh, C.V(x, y, zb - 1.0), C.V(x, y, ztop + 1.0))
        return (iv[0][1] - 1.0) if iv else None                      # floor top above the plate top

    tn = lambda deg: math.tan(math.radians(deg))
    sx, sc = g("tray.floor_slope_deg"), g("tray.cross_fall_deg")
    r_spot = g("tray.drain_spot_r")
    x_a, x_b = dx + r_spot + S.SCAN, fx1 - S.SCAN                    # east run, clear of the spot face and the end wall
    x_w0, x_w1 = fx0 + S.SCAN, dx - r_spot - S.SCAN                  # west shelf run
    y_a, y_b = r_spot + S.SCAN, yi - S.SCAN                          # cross-fall run along x = drain x
    slope_e = math.degrees(math.atan((z_at(x_b, dy) - z_at(x_a, dy)) / (x_b - x_a)))
    slope_w = math.degrees(math.atan((z_at(x_w0, dy) - z_at(x_w1, dy)) / (x_w1 - x_w0)))
    cross = math.degrees(math.atan((z_at(dx, dy + y_b) - z_at(dx, dy + y_a)) / (y_b - y_a)))
    x_mix, y_mix = (fx0 + dx) / 2.0, yi - 1.0                               # the y fall dominates here, clear of the column relief
    hr = C.radial_ivals(sh, 90.0, zb + 1.0, 0.0, 120.0)
    rel = [not sh.isInside(C.V(0.0, s * (Wy / 2 - rd / 2), zb + D / 2), 1e-6, True) and sh.isInside(C.V(rw, s * (Wy / 2 - wall / 2), zb + D / 2), 1e-6, True)
           for s in (-1, 1)]
    relx = C.line_ivals(sh, C.V(-rw, Wy / 2 - wall / 2, zb + D / 2), C.V(rw, Wy / 2 - wall / 2, zb + D / 2))
    bor = C.line_ivals(sh, C.V(dx, -2 * g("tray.drain_dia"), zb + 1.0), C.V(dx, 2 * g("tray.drain_dia"), zb + 1.0))
    x_sp = dx + (g("tray.drain_dia") / 2 + r_spot) / 2               # on the spot face, outside the bore
    wall_x_hi = z_at(fx1 - 0.01, dy)
    z_west = z_at(fx0 + 0.01, dy)
    z_north = z_at(dx, yi - 0.01)
    rows = [
        S.row("BS5", "tray length (A) = tray.length", outer.Volume, sh.BoundBox.XLength, Lx, S.TOL),
        S.row("BS5", "tray width (T) = tray.width", outer.Volume, sh.BoundBox.YLength, Wy, S.TOL),
        S.row("BS5", "tray depth (Z) = tray.depth", outer.Volume, sh.BoundBox.ZLength, D, S.TOL),
        S.row("BS5", "tray end wall (T) = tray.wall", vols["cavity"], xs[0][1] - xs[0][0] if xs else None, wall, 0.02),
        S.row("BS5", "tray side wall (T) = tray.wall", vols["cavity"], ys[0][1] - ys[0][0] if ys else None, wall, 0.02),
        S.row("BS5", "tray.fall_x +X end = inner face of the +X end wall (x)", vols["cavity"], (xs[1][0] - Lx) if len(xs) == 2 else None, fx1, 0.02),
        S.row("BS5", "tray floor thickness on the drain spot face (Z) = tray.floor_min", vols["spot"], z_at(x_sp, dy), fmin, 0.02),
        S.row("BS5", "spot face edge: floor top 0.5 outside tray.drain_spot_r (Z) = floor_min + (spot_r + 0.5) tan(slope)", vols["spot"],
              z_at(dx + r_spot + 0.5, dy), fmin + (r_spot + 0.5) * tn(sx), 0.02),
        S.row("BS5", "east floor slope (deg) between drain spot + SCAN and wall - SCAN = tray.floor_slope_deg", vols["cavity"], slope_e, sx, 0.05),
        S.row("BS5", "floor top at the +X wall (Z) = floor_min + (fall_x[1] - drain x) tan(slope)", vols["cavity"], wall_x_hi,
              fmin + (fx1 - dx - 0.01) * tn(sx), 0.02),
        S.row("BS5", "tray cavity depth at the +X wall (Z) = tray.depth - floor top", vols["cavity"], D - wall_x_hi if wall_x_hi is not None else None,
              D - fmin - (fx1 - dx - 0.01) * tn(sx), 0.02, ok=wall_x_hi is not None and D - wall_x_hi > 0),
        S.row("BS5", "west shelf slope (deg) rising away from the drain = tray.floor_slope_deg", vols["cavity"], slope_w, sx, 0.05),
        S.row("BS5", "floor top at the -X wall (Z) = floor_min + (drain x - fall_x[0]) tan(slope)", vols["cavity"], z_west,
              fmin + (dx - fx0 - 0.01) * tn(sx), 0.02),
        S.row("BS5", "cross fall (deg) along y at the drain x = tray.cross_fall_deg", vols["cavity"], cross, sc, 0.05),
        S.row("BS5", "floor top at the +Y wall, x = drain x (Z) = floor_min + (inner y) tan(cross fall)", vols["cavity"], z_north,
              fmin + (yi - 0.01 - dy) * tn(sc), 0.02),
        S.row("BS5", "floor top where the y fall dominates (Z) = max(f, h) at x = (fall_x[0] + drain x)/2, y = inner wall - 1", vols["cavity"], z_at(x_mix, y_mix),
              fall_height(g, x_mix, y_mix), 0.02),
        S.row("BS5", "column relief width (T) = tray.relief[0]", vols["reliefs"], (relx[1][0] - relx[0][1]) if len(relx) == 2 else None, rw, 0.02),
        S.row("BS5", "column reliefs open at both long edges", vols["reliefs"], int(all(rel)), 1, S.TOL, ok=all(rel)),
        S.row("BS5", "spigot hole radius (R) = tray.hole_r", vols["hole"], hr[0][0] if hr else None, g("tray.hole_r"), 0.02),
        S.row("BS6", "tray drain bore diameter (D) = tray.drain_dia, plain bore; thread named in this row: drain plug thread ASSUMED, modelled at Step 8",
              vols["bore"], bor[1][0] - bor[0][1] if len(bor) == 2 else None, g("tray.drain_dia"), 0.02),
    ]
    res = S.result("tray", sh, rows, rec, extra={"drain_thread": "plain bore dia %.1f; plug thread ASSUMED (tray.drain_plug), stud-subtract if modelled" % g("tray.drain_dia"),
                                                  "floor_top_at_drain_z": zb + fmin, "floor_top_east_wall_z": zb + wall_x_hi,
                                                  "floor_top_corners_z": {"west_wall": zb + z_west, "drain_x_plus_y_wall": zb + z_north}})
    S.save_single("tray", sh, res)
    return res


if __name__ in ("__main__", "tray"):
    C.run_main("tray", build)
