"""Steady rest (AC3) in the closed pose, built as a free part. Local frame: z = 0 is the roller plane (rest.height_positions[0] above the seat),
axis of the core on Z, column face (interface plane, normal -y) at y = column.spacing / 2 - profile.width / 2. Block on the column face, hinge boss at
y = rest.arm_length, arm to a C-ring (mouth rest.mouth_deg centred on -X), three linked rollers on pins that bridge the gap to the ring, close handle,
hold-open detent notch in the boss, release tower (top at height_positions[1] - height_positions[0]). One fuse, one cut.
Fix pass (D2): roller centre radius follows the core, r_c(d) = d / 2 + rest.roller_dia / 2 + fit.model_contact_gap (rest.roller_r_range over rest.core_d_range);
the ring carries a radial slot per roller pin (rest.slot_depth up from the ring bottom, rest.slot_clear per side) spanning the full travel, so the adjustment is a modelled feature.
shape_at(p, core_d) builds the rest with the rollers at the radius for that core; build() uses rest.pose_core_d and records every size in rest.core_d_range."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def roller_radius(g, core_d):
    return core_d / 2.0 + g("rest.roller_dia") / 2.0 + g("fit.model_contact_gap")


def _rot(sh, deg):
    sh = sh.copy()
    sh.rotate(C.V(0, 0, 0), C.V(0, 0, 1), deg)
    return sh


def shape_at(p, core_d, rec=None):
    """Rest solid with the rollers at the contact radius for a core of diameter core_d."""
    return _core(p, core_d, rec or S.Rec("rest"), False)


def _core(p, core_d, rec, measure):
    g = lambda k: C.G(p, k)
    ov = g("collet.tool_overshoot")
    y_col = g("column.spacing") / 2 - g("profile.width") / 2
    bx, by, bz = g("rest.block")
    boss_r = g("rest.hinge_boss_dia") / 2
    y_boss = g("rest.arm_length")
    r_in, r_out, r_t = g("rest.ring")
    z_lo = g("rest.ring_z_lo")
    z_hi = z_lo + r_t
    aw, ah = g("rest.arm")
    n_r = g("rest.roller_count")
    rr, rh = g("rest.roller_dia") / 2, g("rest.roller_height")
    pin_r = g("rest.pin") / 2
    tw, td = g("rest.tower")
    z_tower = g("rest.height_positions")[1] - g("rest.height_positions")[0]
    z_mid = (z_lo + z_hi) / 2
    block = S.box(-bx / 2, bx / 2, y_col - by, y_col, -bz / 2, bz / 2)
    boss = S.cyl_z(0.0, y_boss, boss_r, -bz / 2, bz / 2)
    arm = S.box(-aw / 2, aw / 2, (r_in + r_out) / 2, y_boss, z_mid - ah / 2, z_mid + ah / 2)
    ring_plain = C.sector_solid(r_in, r_out, z_lo, z_hi, 0.0, 360.0 - g("rest.mouth_deg"))
    r_c = roller_radius(g, core_d)
    r_lo, r_hi = g("rest.roller_r_range")
    az_r = [360.0 / n_r * k for k in range(n_r)]
    gap = g("fit.model_contact_gap")
    z_slot = z_lo + g("rest.slot_depth")
    slots = [S.box(r_lo - pin_r - gap, r_hi + pin_r + gap, -pin_r - g("rest.slot_clear"), pin_r + g("rest.slot_clear"), z_lo - ov, z_slot) for _ in az_r]
    slots = [_rot(sl, a) for sl, a in zip(slots, az_r)]
    ring = rec.cut("ring_pin_slots_cut", ring_plain, C.fuse_all(slots))              # slotted ring primitive, before the one assembly fuse
    parts = [block, boss, arm, ring]
    for a in az_r:
        c = C.polar(r_c, a)
        parts.append(S.cyl_z(c.x, c.y, rr, -rh / 2, rh / 2))
        parts.append(S.cyl_z(c.x, c.y, pin_r, -rh / 2 - ov, z_slot + ov))
    hl = g("rest.close_handle_length")
    y_h = (r_out + y_boss) / 2
    parts.append(S.cyl_dir(C.V(aw / 2 - ov, y_h, z_mid), C.V(1, 0, 0), g("rest.handle_dia") / 2, hl + ov))
    parts.append(S.box(-tw / 2, tw / 2, g("rest.tower_inboard_r"), g("rest.tower_inboard_r") + td, z_mid, z_tower))
    fused = rec.fuse("rest_fuse", parts)
    dd, dw = g("rest.detent_depth"), g("rest.detent_width")
    notch = S.box(boss_r - dd, boss_r + ov, y_boss - dw / 2, y_boss + dw / 2, -bz / 2 - ov, bz / 2 + ov)
    notch_mm3 = S.removed(notch, fused)
    sh = S.solid_of(rec.cut("detent_cut", fused, notch))
    if not measure:
        return sh
    r_pose = r_c
    # ---- measurements on the final solid
    ins = lambda x, y, z: sh.isInside(C.V(x, y, z), 1e-6, True)
    x_b = (bx / 2 + boss_r) / 2                                   # beside the boss
    blk_y = C.line_ivals(sh, C.V(x_b, y_col + ov, 0.0), C.V(x_b, y_col - 2 * by, 0.0))
    blk_x = C.line_ivals(sh, C.V(-bx, y_col - by / 2, 0.0), C.V(bx, y_col - by / 2, 0.0))
    blk_z = C.line_ivals(sh, C.V(0.0, y_col - by / 2, -bz), C.V(0.0, y_col - by / 2, bz))
    boss_x = C.line_ivals(sh, C.V(-2 * boss_r, y_boss - boss_r / 2, bz / 4), C.V(2 * boss_r, y_boss - boss_r / 2, bz / 4))
    ring_r = C.radial_ivals(sh, 180.0 / n_r, z_mid, 0.0, r_out + g("collet.tool_overshoot"))
    ring_z = C.axial_ivals(sh, 180.0 / n_r, (r_in + r_out) / 2, -bz, bz)
    r_mid = (r_in + r_out) / 2
    step_deg = 360.0 / 3600
    mouth = sum(1 for a10 in range(int(round(360.0 / step_deg))) if not ins(r_mid * math.cos(math.radians(a10 * step_deg)), r_mid * math.sin(math.radians(a10 * step_deg)), z_mid))
    rollers = sum(1 for a in az_r if ins(r_pose * math.cos(math.radians(a)), r_pose * math.sin(math.radians(a)), 0.0))
    roll_d = C.line_ivals(sh, C.V(r_pose - 2 * rr, rr / 2, 0.0), C.V(r_pose + 2 * rr, rr / 2, 0.0))
    gap_z = C.axial_ivals(sh, 0.0, r_pose + rr * 0.7, -rh, z_hi + 2)
    pin_bridge = ins(r_pose, 0.0, rh / 2 + g("rest.roller_pin_gap") / 2)
    gap_open = not ins(r_pose + 2 * pin_r, 0.0, rh / 2 + g("rest.roller_pin_gap") / 2)
    handle = C.line_ivals(sh, C.V(0.0, y_h, z_mid), C.V(aw / 2 + hl + 10, y_h, z_mid))
    notch_r = C.line_ivals(sh, C.V(boss_r + ov, y_boss, 0.0), C.V(0.0, y_boss, 0.0))
    tower_r = C.radial_ivals(sh, 90.0, z_tower / 2, 0.0, r_out + 10)
    tower_x = C.line_ivals(sh, C.V(-tw, g("rest.tower_inboard_r") + td / 2, z_tower / 2), C.V(tw, g("rest.tower_inboard_r") + td / 2, z_tower / 2))
    # slot rows at az 0 (pin at the pose radius): inner and outer slot walls bound the travel; slot width across the slot at a radius off the pin
    slot_vol = S.removed(slots[0], ring_plain)
    z_s = z_lo + g("rest.slot_depth") / 2
    sl_r = C.radial_ivals(sh, 0.0, z_s, 0.0, r_out + ov)
    sl_w = C.tangential_ivals(sh, 0.0, r_lo - pin_r + 1.0, z_s, 20.0)
    slot_inner = sl_r[0][1] if sl_r else None
    slot_outer = sl_r[-1][0] if sl_r else None
    travel = r_hi - r_lo
    rows = [
        S.row("AC3", "interface plane y = column face (block back face)", block.Volume, sh.BoundBox.YMax, y_col, S.TOL),
        S.row("AC3", "block width x (T)", block.Volume, blk_x[0][1] - blk_x[0][0] if blk_x else None, bx, S.TOL),
        S.row("AC3", "block thickness y (L)", block.Volume, blk_y[0][1] - blk_y[0][0] if blk_y else None, by, S.TOL),
        S.row("AC3", "block height z (Z)", block.Volume, blk_z[0][1] - blk_z[0][0] if blk_z else None, bz, S.TOL),
        S.row("AC3", "hinge boss diameter (D) at y = rest.arm_length", boss.Volume, (boss_x[0][1] - boss_x[0][0]) if len(boss_x) == 1 else None,
              2 * math.sqrt(boss_r ** 2 - (boss_r / 2) ** 2), 0.02, note="chord at y = boss centre - boss_r / 2 on the boss"),
        S.row("AC3", "C-ring outer radius (R)", ring.Volume, ring_r[-1][1] if ring_r else None, r_out, 0.02),
        S.row("AC3", "C-ring inner radius (R)", ring.Volume, ring_r[0][0] if ring_r else None, r_in, 0.02),
        S.row("AC3", "C-ring thickness (Z)", ring.Volume, ring_z[0][1] - ring_z[0][0] if ring_z else None, r_t, 0.02),
        S.row("AC3", "C-ring mouth arc (deg) = rest.mouth_deg", ring.Volume, mouth * step_deg, g("rest.mouth_deg"), 3 * step_deg),
        S.row("AC3", "roller count at azimuth 360/n x k", rr * rr * math.pi * rh, rollers, n_r, S.TOL),
        S.row("AC3", "roller diameter (D) = rest.roller_dia", rr * rr * math.pi * rh, (roll_d[0][1] - roll_d[0][0]) if roll_d else None,
              2 * math.sqrt(rr ** 2 - (rr / 2) ** 2), 0.02, note="chord at y = roller_dia / 4"),
        S.row("AC3", "roller pin bridges the roller to ring gap (rest.roller_pin_gap) and the gap stays open beside the pin",
              math.pi * pin_r ** 2 * (rh + z_hi), int(pin_bridge and gap_open), 1, S.TOL, ok=(pin_bridge and gap_open)),
        S.row("AC3", "close handle length (L) = rest.close_handle_length", math.pi * (g("rest.handle_dia") / 2) ** 2 * hl,
              handle[-1][1] - (aw / 2) if handle else None, hl, 0.05),
        S.row("AC3", "hold-open detent notch depth (R) = rest.detent_depth", notch_mm3, (notch_r[0][0] - ov) if notch_r else None, dd, 0.05),
        S.row("AC3", "release tower inboard face radius (R)", tw * td * z_tower, tower_r[0][0] if tower_r else None, g("rest.tower_inboard_r"), 0.02),
        S.row("AC3", "release tower tangential width (T)", tw * td * z_tower, tower_x[0][1] - tower_x[0][0] if tower_x else None, tw, 0.02),
        S.row("AC3", "roller centre radius at rest.pose_core_d (R) = d/2 + roller_dia/2 + fit.model_contact_gap = rest.roller_r", math.pi * rr ** 2 * rh,
              r_pose, g("rest.roller_r"), 1e-6),
        S.row("AC3", "roller travel rest.roller_r_range spans core_d_range (R)", math.pi * rr ** 2 * rh, r_hi - r_lo,
              roller_radius(g, g("rest.core_d_range")[1]) - roller_radius(g, g("rest.core_d_range")[0]), 1e-6),
        S.row("AC3", "pin slot radial length (R) = travel + pin dia + 2 x fit.model_contact_gap", slot_vol, (slot_outer - slot_inner) if sl_r else None,
              travel + 2 * pin_r + 2 * gap, 0.02, note="slot bounded by ring walls; pin occupies the middle of the span at the pose"),
        S.row("AC3", "pin slot width (T) = rest.pin + 2 x rest.slot_clear", slot_vol, (sl_w[1][0] - sl_w[0][1]) if len(sl_w) == 2 else None,
              2 * pin_r + 2 * g("rest.slot_clear"), 0.02),
        S.row("AC3", "pin slot inner wall left in the ring (R) > 0", slot_vol, slot_inner - r_in if sl_r else None, r_lo - pin_r - gap - r_in, 0.02),
        S.row("AC3", "release tower top z = height_positions[1] - [0] (A)", tw * td * z_tower, sh.BoundBox.ZMax, z_tower, 0.02),
    ]
    sizes = size_sweep(p, rec, sh)
    res = S.result("rest", sh, rows, rec, extra={"pose": "closed", "pose_core_d": core_d, "sizes": sizes, "roller_plane_above_seat": g("rest.height_positions")[0],
                                                  "interface": {"plane": "y = %.1f" % y_col, "normal": "-y", "owner": "upper assembly column"}})
    return sh, res


def size_sweep(p, rec, pose_shape):
    """Zero-common-volume check per core size: rollers at that size's radius against a cylinder of the core diameter (all z), plus validity, gap,
    interface plane and bbox for the whole rest. Sizes: core_d_range ends and core.diameters."""
    import Part
    g = lambda k: C.G(p, k)
    lo, hi = g("rest.core_d_range")
    out = []
    for d in [lo] + list(g("core.diameters")) + [hi]:
        sh = shape_at(p, d, S.Rec("rest_%s" % d))
        core = S.cyl_z(0.0, 0.0, d / 2.0, sh.BoundBox.ZMin - 5.0, sh.BoundBox.ZMax + 5.0)
        # the three roller solids alone: smallest distance to the core cylinder
        n_r = g("rest.roller_count")
        rr, rh = g("rest.roller_dia") / 2, g("rest.roller_height")
        rollers = [S.cyl_z(*tuple(C.polar(roller_radius(g, d), 360.0 / n_r * k))[:2], rr, -rh / 2, rh / 2) for k in range(n_r)]
        gaps = [core.distToShape(r)[0] for r in rollers]
        aw, ah = g("rest.arm")
        z_mid = g("rest.ring_z_lo") + g("rest.ring")[2] / 2
        arm = S.box(-aw / 2, aw / 2, (g("rest.ring")[0] + g("rest.ring")[1]) / 2, g("rest.arm_length"), z_mid - ah / 2, z_mid + ah / 2)
        arm_d = min(r.distToShape(arm)[0] for r in rollers)
        out.append({"core_d": d, "roller_r": round(roller_radius(g, d), 4), "solids": len(sh.Solids), "isValid": bool(sh.isValid()),
                    "common_with_core_mm3": round(sh.common(core).Volume, 6), "roller_to_core_gap": round(min(gaps), 6),
                    "roller_to_arm": round(arm_d, 3), "interface_plane_ymax": round(sh.BoundBox.YMax, 6),
                    "bbox_plain_equals_optimal": all(abs(a - b) < 1e-6 for a, b in zip(S._bb(sh.BoundBox).values(), S._bb(C.bbox(sh)).values())),
                    "faces": len(sh.Faces), "euler_VEF": S.euler(sh), "volume_mm3": round(sh.Volume, 3)})
    return out


def build():
    p = C.params()
    rec = S.Rec("rest")
    sh, res = _core(p, C.G(p, "rest.pose_core_d"), rec, True)
    S.save_single("rest", sh, res)
    return res


if __name__ in ("__main__", "rest"):
    C.run_main("rest", build)
