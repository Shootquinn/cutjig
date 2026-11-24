import re
B = "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/build_parts/"


def rd(f):
    return open(B + f, encoding="utf-8").read()


def wr(f, s):
    open(B + f, "w", encoding="utf-8").write(s)


s = rd("step6lib.py")
s = s.replace("CACHE = C.CACHE\nV = C.V\n", "CACHE = C.CACHE\nV = C.V\nTOL = 0.015     # default feature-row tolerance, mm (not a part dimension)\nSCAN = 17.0     # measurement-line margin beyond a feature, mm (not a part dimension)\nND = 5          # digits kept in recorded positions\n", 1)
s = s.replace('round(shape.Volume / before["before_volume"], 6)', 'round(shape.Volume / before["before_volume"], ND)')
wr("step6lib.py", s)

for f in ("base.py", "tray.py", "foot.py", "tnut.py", "bracket.py", "frame.py", "caddy.py", "gauge.py", "rest.py", "stop.py"):
    s = rd(f)
    s = re.sub(r"(?<![\d.])0\.01(?![\d])", "S.TOL", s)
    wr(f, s)

s = rd("tray.py")
s = s.replace("C.V(-Lx, 100.0, ztop - 1.0), C.V(Lx, 100.0, ztop - 1.0)", "C.V(-Lx, Wy / 4.0, ztop - 1.0), C.V(Lx, Wy / 4.0, ztop - 1.0)")
s = s.replace("C.V(-100.0, -Wy, ztop - 1.0), C.V(-100.0, Wy, ztop - 1.0)", "C.V(-Lx / 5.0, -Wy, ztop - 1.0), C.V(-Lx / 5.0, Wy, ztop - 1.0)")
s = s.replace("C.V(x, 100.0, zb - 1.0), C.V(x, 100.0, ztop + 1.0)", "C.V(x, Wy / 4.0, zb - 1.0), C.V(x, Wy / 4.0, ztop + 1.0)")
s = s.replace("fl_x(x0 - 20.0), fl_x(x1 + 20.0)", "fl_x(x0 - S.SCAN), fl_x(x1 + S.SCAN)")
s = s.replace("z_at(x1 - 10.0) - z_at(x0 + 10.0)) / (x1 - x0 - 20.0)", "z_at(x1 - S.SCAN) - z_at(x0 + S.SCAN)) / (x1 - x0 - 2 * S.SCAN)")
s = s.replace("z_at(x1 + 20.0)", "z_at(x1 + S.SCAN)")
s = s.replace("C.V(dx, -40.0, zb + 1.0), C.V(dx, 40.0, zb + 1.0)", "C.V(dx, -2 * g(\"tray.drain_dia\"), zb + 1.0), C.V(dx, 2 * g(\"tray.drain_dia\"), zb + 1.0)")
wr("tray.py", s)

s = rd("base.py")
s = s.replace("C.V(dx - 40, dy, zmid), C.V(dx + 40, dy, zmid)", "C.V(dx - 2 * g(\"base.drain_hole_dia\"), dy, zmid), C.V(dx + 2 * g(\"base.drain_hole_dia\"), dy, zmid)")
wr("base.py", s)

s = rd("gauge.py")
s = s.replace("C.tangential_ivals(sh, th, r_p + kh / 2, kl / 2, 20.0)", "C.tangential_ivals(sh, th, r_p + kh / 2, kl / 2, S.SCAN)")
wr("gauge.py", s)

s = rd("caddy.py")
s = s.replace("* pitch, 6)", "* pitch, S.ND)")
wr("caddy.py", s)

s = rd("stop.py")
s = s.replace('round(nv, 6)', 'round(nv, S.ND)')
wr("stop.py", s)

s = rd("rest.py")
s = s.replace("C.radial_ivals(sh, 90.0 + 30.0, z_mid, 0.0, r_out + 10)", "C.radial_ivals(sh, 180.0 / n_r, z_mid, 0.0, r_out + g(\"collet.tool_overshoot\"))")
s = s.replace("C.axial_ivals(sh, 60.0, (r_in + r_out) / 2, -bz, bz)", "C.axial_ivals(sh, 180.0 / n_r, (r_in + r_out) / 2, -bz, bz)")
s = s.replace("mouth = sum(1 for a10 in range(3600) if", "step_deg = 0.1\n    mouth = sum(1 for a10 in range(int(round(360.0 / step_deg))) if")
s = s.replace("math.radians(a10 / 10.0)", "math.radians(a10 * step_deg)")
s = s.replace("mouth / 10.0, g(\"rest.mouth_deg\"), 0.3)", "mouth * step_deg, g(\"rest.mouth_deg\"), 3 * step_deg)")
wr("rest.py", s)
print("ok")
