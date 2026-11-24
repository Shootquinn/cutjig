"""T1a, T1c, T2, T3, T8 measurements on receiver and nut (and a mirrored copy of the nut for the T1a known-bad control).
Sampling only (line intersections); runs in seconds. Output results/probes/thread.json.
Run: freecadcmd tests/probes/probe_thread.py"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
C = L.C


def centres(iv):
    return [(a + b) / 2.0 for a, b in iv]


def unwrap_rise(zs, pitch):
    tot = 0.0
    for a, b in zip(zs, zs[1:]):
        d = (b - a) % pitch
        tot += d - pitch if d > pitch / 2 else d
    return tot


def ridge_z(sh, theta, r, zlo, zhi, zref):
    """Centre of the solid interval at (theta, r) nearest zref."""
    iv = C.axial_ivals(sh, theta, r, zlo, zhi)
    cs = centres(iv)
    return min(cs, key=lambda c: abs(c - zref)) if cs else None


def profile(sh, kind, p, zlo, zhi, zref, full=True):
    """kind 'ext' (receiver) or 'int' (nut). Radii, pitch, lead, tooth widths and flank slope from sections."""
    P = L.G(p, "thread.pitch")
    r_p = (L.G(p, "thread.major") - L.G(p, "chain.h")) / 2.0
    zmid = (zlo + zhi) / 2.0
    azs = [30.0 * k for k in range(12)]  # 30 degree steps: a 0.67 mm axial shift per step, the 1.5 mm crest flat is always sampled
    if kind == "ext":
        outs = [C.radial_ivals(sh, a, zmid, 60.0, 90.0)[-1][1] for a in azs]
        crest, root = max(outs), min(outs)
    else:
        ins = [C.radial_ivals(sh, a, zmid, 60.0, 90.0)[0][0] for a in azs]
        crest, root = min(ins), max(ins)
    # lead: unwrap the ridge centre over one revolution at the pitch radius
    zs = [ridge_z(sh, a, r_p, zlo, zhi, zref) for a in azs + [360.0]]
    rise = unwrap_rise(zs, P)
    # tooth flank from interval ends at two radii (down-facing flank = low end of the tooth interval)
    d = (crest - root) if kind == "ext" else (root - crest)
    r_a = (root if kind == "ext" else crest) + 0.25 * d
    r_b = (root if kind == "ext" else crest) + 0.75 * d
    zc = zs[0]

    def tooth(r):
        iv = C.axial_ivals(sh, 0.0, r, zlo, zhi)
        return min(iv, key=lambda ab: abs((ab[0] + ab[1]) / 2 - zc))

    ta, tb = tooth(r_a), tooth(r_b)
    dr = abs(r_b - r_a)
    lo_slope = math.degrees(math.atan2(abs(tb[0] - ta[0]), dr))
    hi_slope = math.degrees(math.atan2(abs(tb[1] - ta[1]), dr))
    off = 0.02
    tc = tooth(crest - off if kind == "ext" else crest + off)
    tp = tooth(r_p)
    crest_flat = (tc[1] - tc[0]) - (2 * off * math.tan(math.radians(lo_slope)) if kind == "ext" else -2 * off * math.tan(math.radians(lo_slope)))
    # Rule M sign self-check: the ridge centre is inside the solid, a point one half-width plus 0.05 above it is outside
    zc_p = (tp[0] + tp[1]) / 2.0
    pt_in = C.V(r_p, 0.0, zc_p)
    pt_out = C.V(r_p, 0.0, tp[1] + 0.05)
    self_check = bool(sh.isInside(pt_in, 1e-6, True)) and not bool(sh.isInside(pt_out, 1e-6, True))
    return {"crest_r": crest, "root_r": root, "lead": abs(rise), "rise_sign": 1 if rise > 0 else -1,
            "starts": abs(rise) / P, "tooth_w_pitch": tp[1] - tp[0], "tooth_w_crest": crest_flat, "self_check": self_check,
            "down_flank_deg": lo_slope, "up_flank_deg": hi_slope,
            "dz0": zs[0] % P, "dz90": zs[3] % P, "ridge_z_theta0": zs[0], "r_pitch": r_p}


def main():
    p = L.params()
    P = L.G(p, "thread.pitch")
    z_top = L.G(p, "receiver.rim_above_floor")
    z_run = z_top - L.G(p, "thread.run_turns") * P
    rec = L.part("receiver")
    nut = L.part("nut")
    mir = nut.mirror(C.V(0, 0, 0), C.V(0, 1, 0))
    r = profile(rec, "ext", p, z_run + P, z_top - P, z_run + 3.5 * P)
    n = profile(nut, "int", p, P, L.G(p, "nut.length") - 2 * P, 2.5 * P)
    zm = [ridge_z(mir, a, n["r_pitch"], P, L.G(p, "nut.length") - 2 * P, 2.5 * P) for a in (0.0, 90.0)]
    m = {"dz0": zm[0] % P, "dz90": zm[1] % P}
    clearance = {"c_r_root_side": n["crest_r"] - r["root_r"], "c_r_crest_side": n["root_r"] - r["crest_r"],
                 "g_a_total": (P - n["tooth_w_pitch"]) - r["tooth_w_pitch"], "pitch": P}
    L.finish("thread", {"receiver": r, "nut": n, "nut_mirrored": m, "clearance": clearance},
             [os.path.join(L.CACHE, "receiver.FCStd"), os.path.join(L.CACHE, "nut.FCStd")])


if __name__ in ("__main__", "probe_thread"):
    L.guarded(main, "thread")
