B = "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/build_parts/"


def rd(f):
    return open(B + f, encoding="utf-8").read()


def wr(f, s):
    open(B + f, "w", encoding="utf-8").write(s)


s = rd("receiver.py")
s = s.replace("    az, d_fl, zz0, nn = rd[\"az\"], rd[\"d_fl\"], rd[\"z0\"], rd[\"n\"]\n",
              "    az, d_fl, zz0, nn = rd[\"az\"], rd[\"d_fl\"], rd[\"z0\"], rd[\"n\"]\n    tspan = g(\"witness.channel_width\") / 2 + 2 * g(\"collet.tool_overshoot\")      # tangent measurement line half-length: past the channel edge, inside the root cylinder\n", 1)
for a in ("-8.0", "8.0"):
    pass
s = s.replace("d_fl + 0.02, -8.0, mid), S.point_at(az, d_fl + 0.02, 8.0, mid)", "d_fl + 0.02, -tspan, mid), S.point_at(az, d_fl + 0.02, tspan, mid)")
s = s.replace("d_fl - 0.25, -8.0, zmaj), S.point_at(az, d_fl - 0.25, 8.0, zmaj)", "d_fl - 0.25, -tspan, zmaj), S.point_at(az, d_fl - 0.25, tspan, zmaj)")
s = s.replace("d_fl - 0.25, -8.0, zmin_), S.point_at(az, d_fl - 0.25, 8.0, zmin_)", "d_fl - 0.25, -tspan, zmin_), S.point_at(az, d_fl - 0.25, tspan, zmin_)")
s = s.replace("len0 = 2.0 * (8.0 - k0[0][1])", "len0 = 2.0 * (tspan - k0[0][1])")
s = s.replace(", 0.01),\n        (\"RC6", ", S.TOL),\n        (\"RC6")
s = s.replace('d_fl, 0.01),', 'd_fl, S.TOL),')
s = s.replace('g("witness.line_height"), 0.02)', 'g("witness.line_height"), 0.02)')
s = s.replace("pitch_w, 0.01),", "pitch_w, S.TOL),")
s = s.replace("nn, 0.01),", "nn, S.TOL),")
s = s.replace("n_dig, 0.01),", "n_dig, S.TOL),")
wr("receiver.py", s)

s = rd("holder.py")
s = s.replace('az_w + 120.0, q["L"] + 1.0), 1e-6, True)) els', 'az_w + 120.0, q["L"] + ov), 1e-6, True)) els')
s = s.replace('C.polar(q["r_fl"] - g("witness.tick_depth") / 2, az_w, q["L"] + 1.0)', 'C.polar(q["r_fl"] - g("witness.tick_depth") / 2, az_w, q["L"] + ov)')
s = s.replace('az_w, 0.01),\n    ]', 'az_w, S.TOL),\n    ]')
wr("holder.py", s)

s = rd("nut.py")
s = s.replace("def measure_glyph(piece, p, q, face, x0, x1, step=0.5, y_half=7.5):", "def measure_glyph(piece, p, q, face, x0, x1, step=0.5):")
s = s.replace("    depth = g(\"nut.arrow_depth\")\n    r_in = g(\"wingnut.body_od\") / 2 + 3\n    root = g(\"wingnut.wing_root_width\")\n    sign",
              "    depth = g(\"nut.arrow_depth\")\n    r_in = g(\"wingnut.body_od\") / 2 + 3\n    y_half = g(\"wingnut.wing_thickness\") / 2 + step          # one sample beyond each wing face\n    sign")
s = s.replace('-1, 0.01),', '-1, S.TOL),').replace('+1, 0.01),', '+1, S.TOL),')
s = s.replace("slope_deg, slope_exp, 0.3)", "slope_deg, slope_exp, 20 * S.TOL)")
wr("nut.py", s)
print("ok")
