"""T9 register and tilt (Loftsman ruling, cr_scratch/step4_loftsman_t9_ruling.md). Receiver frame (floor z 0, rim z = receiver.rim_above_floor).

Measured: the register stop angle of the holder in the receiver bore. The holder hangs at first thread contact (insertion
receiver.register_depth + nut.lift_play below the rim), is shifted -register.g_reg onto the -X wall and tilted about Y through that
bottom wall point (top moves +X). The holder is cut to the slab |y| <= SLAB (the two register contact lines lie at y = 0; the slab
leaves out the anti-rotation key, which can only lower the stop, so the slab stop is the upper bound; the receiver itself cannot be
sliced: receiver-box common returns 0 under OCC 1.1). The stop is the first angle with holder-slab/receiver common > TOL. Bisection to
BISECT_TOL deg; every boolean is cross-checked by V_common = V_receiver - V_cut.
Known-bad pose: the same measurement at the superseded short register (holder length SHORT_LH, insertion SHORT_LH - nut skirt + p).
Register at 2 x alpha_crit: holder-slab/receiver common at that tilt (must be > tolerance: the register blocks the cross-thread onset).

Instrument control on the thread-start pose (nut seated a meshed half-turn on the receiver start, skirt bottom at the rim): flank
distance at zero tilt, and nut/receiver common after an axial drop of fit.g_a/2 -/+ DROP_BAND (clear below, interfering above).
The rigid-tilt nut sweep of the fix pass is withdrawn: it forced the nut through the flank it rests on (see the ruling).

Outputs results/probes/tilt.json. Heavy: launch detached."""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib as L  # noqa: E402
import Part  # noqa: E402
C = L.C

SLAB = 20.0          # mm half-width in y of the register measurement slab
BISECT_TOL = 0.001   # deg
HI_DEG = 5.0         # bisection upper bracket (holder booleans valid to 5 deg, step4 fix pass)
TOL = 0.01           # mm3, overlap tolerance (tdd_method, llm_plm_cad 7.4)
SHORT_LH = 54.0      # mm, superseded holder length (step2_loftsman_crossreview_reply.md section 3 table, fails at 2.477 deg)
DROP_BAND = 0.05     # mm
AGREE_ABS, AGREE_REL = 0.05, 0.02


def clean(sh):
    s = Part.Shape()
    s.importBrepFromString(sh.exportBrepToString())
    return s


def main():
    p = L.params()
    P = L.G(p, "thread.pitch")
    rim = L.G(p, "receiver.rim_above_floor")
    R = L.G(p, "receiver.register_bore_radius")
    g_reg = L.G(p, "register.g_reg")
    lift = L.G(p, "nut.lift_play")
    depth = L.G(p, "receiver.register_depth")
    skirt = L.G(p, "nut.skirt_below_flange")
    rec = clean(L.part("receiver"))
    hol = clean(L.part("holder"))
    bb = hol.BoundBox
    hol = clean(hol.common(Part.makeBox(bb.XLength + 2, 2 * SLAB, bb.ZLength + 2, C.V(bb.XMin - 1, -SLAB, bb.ZMin - 1))))
    assert hol.Volume > 0 and len(hol.Solids) >= 1, "holder slab boolean failed"
    vs = rec.Volume
    log = []

    def hit(sh, a, z_hb):
        s = sh.copy()
        s.rotate(C.V(-R, 0.0, z_hb), C.V(0, 1, 0), a)
        s = clean(s)
        vc = rec.common(s).Volume
        vk = vs - rec.cut(s).Volume
        ok = vk > -1.0 and abs(vc - vk) <= AGREE_ABS + AGREE_REL * max(vc, vk)
        log.append({"deg": a, "z_hb": z_hb, "common": vc, "via_cut": vk, "valid": bool(ok)})
        print("REG z_hb %.2f a %.4f common %.4f viaCut %.4f %s" % (z_hb, a, vc, vk, "ok" if ok else "INVALID"), flush=True)
        return vc, ok

    def stop(insertion):
        z_hb = rim - insertion
        sh = clean(L.moved(hol, x=-g_reg, z=z_hb))
        v0, ok0 = hit(sh, 0.0, z_hb)
        vh, okh = hit(sh, HI_DEG, z_hb)
        lo, hi, valid = 0.0, HI_DEG, ok0 and okh and v0 <= TOL and vh > TOL
        while valid and hi - lo > BISECT_TOL:
            m = 0.5 * (lo + hi)
            v, ok = hit(sh, m, z_hb)
            valid = valid and ok
            lo, hi = (lo, m) if v > TOL else (m, hi)
        return {"insertion_mm": insertion, "z_hb": z_hb, "stop_deg": hi if valid else None, "clear_deg": lo,
                "common_at_zero_mm3": v0, "valid": bool(valid)}, sh

    t0 = time.time()
    reg, hol_hang = stop(depth + lift)
    short = stop(SHORT_LH - skirt + lift)[0]
    D = L.G(p, "thread.major")
    a_crit = math.degrees(math.atan(P / (2.0 * D)))
    v2, ok2 = hit(hol_hang, 2 * a_crit, reg["z_hb"])

    # thread-start instrument control
    nut = clean(L.part("nut"))
    z_run = rim - L.G(p, "thread.run_turns") * P
    z0 = z_run + P / 2.0 + 2 * P
    nut_p = nut.copy()
    nut_p.rotate(C.V(0, 0, 0), C.V(0, 0, 1), 180.0)
    nut_p.translate(C.V(0, 0, z0 + 3.5 * P))                       # screw motion: 180 deg plus 3.5 pitches puts the skirt bottom at the rim
    nut_p = clean(nut_p)
    gap0 = rec.distToShape(nut_p)[0]
    ga2 = L.G(p, "fit.g_a") / 2.0
    drop = {}
    for dz in (ga2 - DROP_BAND, ga2 + DROP_BAND):
        s = clean(L.moved(nut_p, z=-dz))
        vc, vk = rec.common(s).Volume, rec.Volume - rec.cut(s).Volume
        drop["%.3f" % dz] = {"common_mm3": vc, "valid": bool(abs(vc - vk) <= AGREE_ABS + AGREE_REL * max(vc, vk))}
        print("DROP %.3f common %.4f viaCut %.4f" % (dz, vc, vk), flush=True)

    out = {"tilt_deg": L.G(p, "register.t9_tilt_deg"), "register": reg, "short_register": short, "short_lh_mm": SHORT_LH,
           "alpha_crit_deg_from_params": a_crit, "register_common_at_2x_crit_mm3": v2 if ok2 else None,
           "slab_half_width_mm": SLAB, "bisect_tol_deg": BISECT_TOL, "samples": log, "g_reg": g_reg, "register_bore_radius": R,
           "holder_radius": R - g_reg, "register_chamfer": L.G(p, "receiver.register_chamfer"),
           "flank_gap_zero_tilt_mm": gap0, "fit_g_a": 2 * ga2, "axial_drop": drop, "drop_band_mm": DROP_BAND,
           "register_seconds": round(time.time() - t0, 1)}
    L.finish("tilt", out, [os.path.join(L.CACHE, n + ".FCStd") for n in ("receiver", "holder", "nut")])


if __name__ in ("__main__", "probe_tilt"):
    L.guarded(main, "tilt")
