"""Collet caddy (AC1): seven sockets (collets.count) in staggered rows (caddy.rows), socket diameter = holder key-tip OD + 2 caddy.socket_clear
(Loftsman C8), depth caddy.socket_depth, size label recess at each socket front 1.0 off the socket wall (Topologist). Local frame: centred on
the origin in x and y, z 0 to floor + socket depth."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step6lib as S  # noqa: E402
import cadlib as C  # noqa: E402


def build():
    p = C.params()
    g = lambda k: C.G(p, k)
    rec = S.Rec("caddy")
    ov = g("collet.tool_overshoot")
    r_tip = g("receiver.register_bore_radius") - g("register.g_reg") + g("holder.key_height")
    d_sock = 2 * r_tip + 2 * g("caddy.socket_clear")
    r_s = d_sock / 2
    web, border, floor, depth = g("caddy.web"), g("caddy.border"), g("caddy.floor"), g("caddy.socket_depth")
    pitch = d_sock + web
    rows_n = g("caddy.rows")
    assert sum(rows_n) == g("collets.count")
    n_max = max(rows_n)
    Lx = (n_max - 1) * pitch + d_sock + 2 * border
    Ly = g("caddy.row_spacing") + d_sock + 2 * border
    H = floor + depth
    fam = g("core.diameters")
    lo, hi = g("collet.grip_window_lo"), g("collet.grip_window_hi")
    box = S.box(-Lx / 2, Lx / 2, -Ly / 2, Ly / 2, 0.0, H)
    centres, k = [], 0
    ys = [-g("caddy.row_spacing") / 2, g("caddy.row_spacing") / 2]
    for ri, n in enumerate(rows_n):
        for i in range(n):
            centres.append((round((i - (n - 1) / 2.0) * pitch, S.ND), ys[ri], fam[k]))
            k += 1
    sockets = [S.cyl_z(x, y, r_s, floor, H + ov) for x, y, _ in centres]
    lw, lh, ld = g("caddy.label_width"), g("collet.label_height"), g("collet.label_depth")
    labels = []
    for x, y, d in centres:
        yb = y - r_s - g("caddy.label_gap")
        labels.append(S.box(x - lw / 2, x + lw / 2, yb - lh, yb, H - ld, H + ov))
    ov_label_socket = sum(l.common(s).Volume for l in labels for s in sockets)
    tool = rec.fuse("sockets_labels_tool_fuse", sockets + labels)
    sh = S.solid_of(rec.cut("sockets_labels_cut", box, tool))
    vs = sum(S.removed(s, box) for s in sockets)
    vl = sum(S.removed(l, box) for l in labels)
    x0, y0, _ = centres[0]
    xr = C.line_ivals(sh, C.V(x0 - r_s - 10, y0, floor + 1.0), C.V(x0 + r_s + 10, y0, floor + 1.0))
    ax0 = C.line_ivals(sh, C.V(x0, y0, -1.0), C.V(x0, y0, H + 1.0))
    empty = sum(1 for x, y, _ in centres if not sh.isInside(C.V(x, y, floor + 1.0), 1e-6, True))
    web_min = min(((xa - xb) ** 2 + (ya - yb_) ** 2) ** 0.5 for i, (xa, ya, _) in enumerate(centres) for (xb, yb_, _) in centres[i + 1:]) - d_sock
    lab_ok = sum(1 for x, y, _ in centres if not sh.isInside(C.V(x, y - r_s - g("caddy.label_gap") - lh / 2, H - ld / 2), 1e-6, True)
                 and sh.isInside(C.V(x, y - r_s - g("caddy.label_gap") - lh / 2, H - 2 * ld), 1e-6, True))
    rows = [
        S.row("AC1", "caddy length (L) = (n-1) pitch + socket + 2 border", box.Volume, sh.BoundBox.XLength, Lx, S.TOL),
        S.row("AC1", "caddy width (W) = row spacing + socket + 2 border", box.Volume, sh.BoundBox.YLength, Ly, S.TOL),
        S.row("AC1", "caddy height (A) = floor + caddy.socket_depth", box.Volume, sh.BoundBox.ZLength, H, S.TOL),
        S.row("AC1", "socket count = collets.count", vs, empty, g("collets.count"), S.TOL),
        S.row("AC1", "socket diameter (D) = key tip OD + 2 caddy.socket_clear", vs, xr[1][0] - xr[0][1] if len(xr) == 2 else None, d_sock, S.TOL),
        S.row("AC1", "socket floor thickness (A)", vs, ax0[0][1] - ax0[0][0] if ax0 else None, floor, S.TOL),
        S.row("AC1", "web between nearest sockets (L) = caddy.web", vs, web_min, web, 0.05),
        S.row("AC1", "size label recesses, one per socket", vl, lab_ok, g("collets.count"), S.TOL,
              note="recess edge caddy.label_gap off the socket wall; label-socket overlap %.4f mm3" % ov_label_socket),
    ]
    caddy_labels = [{"socket": i + 1, "x": round(x, 3), "y": round(y, 3), "collet_d": d, "text": f"{d:.1f} | {d + lo:.1f}-{d + hi:.1f}"}
                    for i, (x, y, d) in enumerate(centres)]
    res = S.result("caddy", sh, rows, rec, extra={"labels": caddy_labels, "socket_dia": d_sock, "pitch": pitch,
                                                   "label_socket_overlap_mm3": ov_label_socket})
    S.save_single("caddy", sh, res)
    return res


if __name__ in ("__main__", "caddy"):
    C.run_main("caddy", build)
