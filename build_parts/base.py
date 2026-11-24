"""Base plate (BS1 to BS4). Datum A frame: origin at the plate centre, x along the rails, plate underside at z = 0 (frame top plane).
Plate icd.footprint_x x icd.footprint_y x base.plate_thickness; spigot hole, drain hole, eight slots (asymmetric pattern, Rule P), three underside
pockets (two plate keys, one stop pin), two column notches at the long edges. One tool fuse, one cut."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("base")
    ov = g("collet.tool_overshoot")
    Lx, Ly, T = g("icd.footprint_x"), g("icd.footprint_y"), g("base.plate_thickness")
    plate = S.box(-Lx / 2, Lx / 2, -Ly / 2, Ly / 2, 0.0, T)
    # BS2 holes
    dx, dy = g("base.drain_xy")
    spigot = S.cyl_z(0.0, 0.0, g("base.spigot_hole_dia") / 2, -ov, T + ov)
    drain = S.cyl_z(dx, dy, g("base.drain_hole_dia") / 2, -ov, T + ov)
    # BS3 slots, long axis X, through
    sw, sl = g("base.slot_width"), g("base.slot_length")
    slots = [S.stadium(C.V(x, y, -ov), C.V(1, 0, 0), C.V(0, 0, 1), sl, sw, T + 2 * ov) for x, y in g("base.slot_centres")]
    # BS4 underside pockets and column notches
    kp, pd = g("base.key_pocket_size"), g("base.pocket_depth")
    kx, ky = g("base.key_pocket_xy")
    keys = [S.box(s * kx - kp / 2, s * kx + kp / 2, ky - kp / 2, ky + kp / 2, -ov, pd) for s in (-1, 1)]
    px, py = g("base.pin_pocket_xy")
    pw, pl = g("base.pin_pocket_size")
    pin = S.box(px - pw / 2, px + pw / 2, py - pl / 2, py + pl / 2, -ov, pd)
    nw, nd = g("base.column_notch")
    nx = g("base.column_notch_x")
    notches = [S.box(-nx, nx, y0, y1, -ov, T + ov) for (y0, y1) in ((Ly / 2 - nd, Ly / 2 + ov), (-Ly / 2 - ov, -Ly / 2 + nd))]
    tools = [spigot, drain] + slots + keys + [pin] + notches
    vol = {"BS2": S.removed(spigot, plate) + S.removed(drain, plate), "BS3": sum(S.removed(s, plate) for s in slots),
           "BS4": sum(S.removed(k, plate) for k in keys) + S.removed(pin, plate) + sum(S.removed(n, plate) for n in notches)}
    tool = rec.fuse("tools_fuse", tools)
    sh = S.solid_of(rec.cut("tools_cut", plate, tool))
    # ---- measurements on the final solid (Rule M)
    zmid = T / 2
    sp = C.radial_ivals(sh, 90.0, zmid, 0.0, 120.0)
    dr = C.line_ivals(sh, C.V(dx - 2 * g("base.drain_hole_dia"), dy, zmid), C.V(dx + 2 * g("base.drain_hole_dia"), dy, zmid))
    sl_len, sl_wid = [], []
    for x, y in g("base.slot_centres"):
        a = C.line_ivals(sh, C.V(x - sl, y, zmid), C.V(x + sl, y, zmid))
        b = C.line_ivals(sh, C.V(x, y - sw, zmid), C.V(x, y + sw, zmid))
        sl_len.append(a[1][0] - a[0][1] if len(a) == 2 else None)
        sl_wid.append(b[1][0] - b[0][1] if len(b) == 2 else None)
    slot_ok = all(v is not None for v in sl_len + sl_wid)
    n_empty = sum(1 for x, y in g("base.slot_centres") if not sh.isInside(C.V(x, y, zmid), 1e-6, True))
    asym = not all(any(abs(x - x2) < 1e-6 and abs(-y - y2) < 1e-6 for x2, y2 in g("base.slot_centres")) for x, y in g("base.slot_centres"))
    key_x = C.line_ivals(sh, C.V(kx - kp, ky, pd / 2), C.V(kx + kp, ky, pd / 2))
    key_d = C.line_ivals(sh, C.V(kx, ky, -ov), C.V(kx, ky, T + ov))
    pin_x = C.line_ivals(sh, C.V(px - pw, py, pd / 2), C.V(px + pw, py, pd / 2))
    pin_y = C.line_ivals(sh, C.V(px, py - pl, pd / 2), C.V(px, py + pl, pd / 2))
    pin_d = C.line_ivals(sh, C.V(px, py, -ov), C.V(px, py, T + ov))
    nt_y = C.line_ivals(sh, C.V(0.0, 0.0, zmid), C.V(0.0, Ly, zmid))
    nt_x = C.line_ivals(sh, C.V(-2 * nx, Ly / 2 - nd / 2, zmid), C.V(2 * nx, Ly / 2 - nd / 2, zmid))
    notch_w = nt_x[1][0] - nt_x[0][1] if len(nt_x) == 2 else None
    rows = [
        S.row("BS1", "plate length (A) = icd.footprint_x", plate.Volume, sh.BoundBox.XLength, Lx, S.TOL),
        S.row("BS1", "plate width (T) = icd.footprint_y", plate.Volume, sh.BoundBox.YLength, Ly, S.TOL),
        S.row("BS1", "plate thickness (Z) = base.plate_thickness", plate.Volume, sh.BoundBox.ZLength, T, S.TOL),
        S.row("BS2", "spigot hole diameter (D) = base.spigot_hole_dia", vol["BS2"], 2 * sp[0][0] if sp else None, g("base.spigot_hole_dia"), S.TOL),
        S.row("BS2", "drain hole diameter (D) = base.drain_hole_dia", vol["BS2"], dr[1][0] - dr[0][1] if len(dr) == 2 else None, g("base.drain_hole_dia"), S.TOL),
        S.row("BS3", "slot count (through, centre empty)", vol["BS3"], n_empty, len(g("base.slot_centres")), S.TOL),
        S.row("BS3", "slot length (A) = base.slot_length", vol["BS3"], sum(sl_len) / len(sl_len) if slot_ok else None, sl, 0.02),
        S.row("BS3", "slot width (T) = base.slot_width", vol["BS3"], sum(sl_wid) / len(sl_wid) if slot_ok else None, sw, 0.02),
        S.row("BS3", "slot pattern is not symmetric under a flip about X (Rule P)", vol["BS3"], asym, True, ok=asym),
        S.row("BS4", "plate key pocket width (T) = base.key_pocket_size", vol["BS4"], key_x[1][0] - key_x[0][1] if len(key_x) == 2 else None, kp, 0.02),
        S.row("BS4", "plate key pocket depth from the underside (Z) = base.pocket_depth", vol["BS4"], key_d[0][0] - ov if key_d else None, pd, 0.02),
        S.row("BS4", "stop pin pocket x (T)", vol["BS4"], pin_x[1][0] - pin_x[0][1] if len(pin_x) == 2 else None, pw, 0.02),
        S.row("BS4", "stop pin pocket y (T)", vol["BS4"], pin_y[1][0] - pin_y[0][1] if len(pin_y) == 2 else None, pl, 0.02),
        S.row("BS4", "stop pin pocket wall x (pin contact, declared)", vol["BS4"], pin_x[0][1] + px - pw if pin_x else None, px - pw / 2, 0.02),
        S.row("BS4", "stop pin pocket depth (Z)", vol["BS4"], pin_d[0][0] - ov if pin_d else None, pd, 0.02),
        S.row("BS4", "column notch depth from the long edge (L) = base.column_notch[1]", vol["BS4"], Ly / 2 - nt_y[0][1] if nt_y else None, nd, 0.02),
        S.row("BS4", "column notch width (T) = base.column_notch[0]", vol["BS4"], notch_w, nw, 0.02, note="notch spans x -base.column_notch_x to +base.column_notch_x about the column at x 0"),
    ]
    res = S.result("base", sh, rows, rec, extra={"mass_note": "plate volume only; printed mass in findings"})
    S.save_single("base", sh, res)
    return res


if __name__ in ("__main__", "base"):
    C.run_main("base", build)
