"""Cross-part measurements on the built Step 3 shapes (Rule M): register fit, stacked register pair, nut stack, washer
pads, thread mesh. Reads parts_cache/*.FCStd, writes parts_cache/step3_cross_checks.json. Run with freecadcmd."""
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadlib as C  # noqa: E402


def load(name):
    import FreeCAD as App
    d = App.openDocument(str(C.CACHE / (name + ".FCStd")))
    return C.final_shape(d.getObject("Body"))


def moved(sh, x=0.0, y=0.0, z=0.0):
    s = sh.copy()
    s.translate(C.V(x, y, z))
    return s


def dist(a, b):
    return a.distToShape(b)[0]


def main():
    t0 = time.time()
    p = C.params()
    g = lambda k: C.G(p, k)
    th = g("receiver.key_offset_deg")
    clr = th + 180.0
    rec, hol, nut, wsh, ring = (load(n) for n in ("receiver", "holder", "nut", "washer", "footring"))
    out = []

    def add(name, built, expected, tol=0.05, note=""):
        out.append(C.chk(name, built, expected, tol, note))
        print(out[-1], flush=True)

    # ---- register fit g_reg and ring clearance, measured on the shapes, at an azimuth clear of keys
    r_bore = C.radial_ivals(rec, clr, 20.0, 0, 100)[0][0]
    r_hold = C.radial_ivals(hol, clr, 20.0, 0, 100)[0][1]
    r_ring = C.radial_ivals(ring, clr, 0.5, 0, 100)[0][1]
    add("register fit g_reg: receiver bore r - holder OD r (R)", r_bore - r_hold, g("register.g_reg"), 0.005)
    add("ring seat clearance: receiver bore r - ring OD r (R)", r_bore - r_ring, g("fit.seat_clearance"), 0.005)
    # ---- stacked register pair, pose K-max: ring on the floor (z 0), holder bottom at holder.bottom_above_floor_Kmax
    z_h = g("holder.bottom_above_floor_Kmax")
    hol_k = moved(hol, z=z_h)
    ring_top = C.axial_ivals(ring, clr, (r_ring + 50.0) / 2, -1, 10)[0][1]
    add("stacked pair: holder bottom - ring top (A) = fit.model_contact_gap", z_h - ring_top, g("fit.model_contact_gap"), 0.0005)
    hold_bot = C.axial_ivals(hol_k, clr, (r_hold + 60.0) / 2, -1, 200)[0][0]
    add("holder bottom above receiver floor, K-max (A)", hold_bot - 0.0, g("holder.bottom_above_floor_Kmax"), 0.001)
    fl_u = C.axial_ivals(hol_k, clr, (r_hold + g("holder.flange_od") / 2) / 2, -1, 300)[0][0]
    rim = C.bbox(rec).ZMax
    add("holder flange underside - receiver rim, K-max (A) = holder.stroke_gap_min_K", fl_u - rim, g("holder.stroke_gap_min_K"), 0.001)
    # clearances radial: both parts sit in the same bore, ring below holder
    add("holder OD r and ring OD r differ by (R): ring is the smaller", r_hold - r_ring, g("fit.seat_clearance") - g("register.g_reg"), 0.005)
    ov_rh = rec.common(hol_k).Volume
    ov_rr = rec.common(ring).Volume
    ov_hr = hol_k.common(ring).Volume
    add("overlap volumes receiver/holder, receiver/ring, holder/ring (mm3, sum) at K-max", ov_rh + ov_rr + ov_hr, 0.0, 0.01)
    add("min distance holder to receiver at K-max (mm)", dist(rec, hol_k), 0.5 * (g("receiver.key_slot_width") - g("holder.key_width")), 0.005,
        "governed by key tangential clearance (0.125 per side), not by the register")
    add("ring bottom on receiver floor: distance ring to receiver (mm), class C", dist(rec, ring), 0.0, 0.001, "ring z 0 bears on the floor; 0.30 radial is the seat clearance measured above")
    # key tips against slot floor
    r_slot = C.radial_ivals(rec, th, 20.0, 0, 100)[0][0]
    r_key = C.radial_ivals(hol, th, 20.0, 0, 100)[-1][1]
    r_fkey = C.radial_ivals(ring, th, 0.5, 0, 100)[-1][1]
    add("holder key tip to slot floor (R)", r_slot - r_key, g("receiver.key_slot_depth") + g("register.g_reg") - g("holder.key_height"), 0.005)
    add("foot key tip to slot floor (R)", r_slot - r_fkey, r_slot - r_key, 0.005)
    # ---- T9: cylinder tilt at the insertion depth with the built diameters
    L = g("receiver.register_depth") + g("nut.lift_play") - g("receiver.register_chamfer")      # 48.0 + 0.75 hanging - 1.0 chamfer = 47.75
    Dh, B = 2 * r_hold, 2 * r_bore
    t = 0.0
    lo, hi = 0.0, 0.2
    for _ in range(80):
        t = (lo + hi) / 2
        if L * math.sin(t) + Dh * math.cos(t) > B:
            hi = t
        else:
            lo = t
    rock = math.degrees(math.atan(g("nut.lift_play") / g("nut.plate_hole_dia")))
    add("T9 tilt (deg): cylinder tilt from built diameters at 47.75 + plate rock atan(lift_play / plate hole dia)", math.degrees(t) + rock,
        g("register.t9_tilt_deg"), 0.005, "cylinder part %.4f, rock %.4f; params rock uses 136.44 as the lever" % (math.degrees(t), rock))
    # ---- nut stack (nut frame: skirt bottom z = 0)
    h_off = g("nut.skirt_below_flange") - g("holder.length")             # holder bottom in nut frame
    hol_n = moved(hol, z=h_off)
    wsh_n = moved(wsh, z=g("nut.length"))                                 # washer on the flange top plane
    r_c = min(C.radial_ivals(nut, 15.0 * k, 10.0, 0, 120)[0][0] for k in range(24))      # crest radius: tooth azimuth
    r_ph = C.radial_ivals(nut, 30.0, 52.0, 0, 120)[0][0]
    r_fl = C.radial_ivals(hol_n, 30.0, g("nut.skirt_below_flange") + 4.0, 0, 120)[-1][1]
    add("nut crest bore r - holder flange r (R)", r_c - r_fl, 0.60, 0.005, "Loftsman 0.60")
    add("nut plate hole r - holder OD r (R)", r_ph - r_hold, 1.0, 0.005)
    plate_top = C.bbox(nut).ZMax
    fl_under = C.axial_ivals(hol_n, 30.0, 70.0, -1, 300)[0][0]
    add("plate top - flange underside (A)", plate_top - fl_under, 16.0, 0.001, "Loftsman: 16 = flange 8 + plate 8")
    add("holder top (collar underside) - nut plate top (A) = nut.lift_play", C.bbox(hol_n).ZMax - plate_top, g("nut.lift_play"), 0.001)
    add("overlap nut/holder (mm3)", nut.common(hol_n).Volume, 0.0, 0.01)
    # ---- washer: pads (class P interference) and gaps
    add("washer/nut common volume = press pads (mm3)", nut.common(wsh_n).Volume, 2.402, 0.05, "class P, Loftsman 2.402")
    w_top = C.bbox(wsh_n).ZMax
    pk_floor = C.axial_ivals(nut, 30.0, 70.0, -1, 100)[0][0]
    add("washer top - nut pocket floor (A)", pk_floor - w_top, 0.0, 0.001)
    w_bot = C.bbox(wsh_n).ZMin
    fl_top = C.axial_ivals(hol_n, 30.0, 70.0, -1, 300)[0][1]
    add("flange top - washer bottom (A)", w_bot - fl_top, 0.0, 0.001)
    # tab in notch: gaps
    z_mid = g("nut.length") + g("washer.thickness") - g("nut.washer_pocket_depth") + g("nut.washer_pocket_depth") / 2 - 0.5 + 0.5
    wn = C.tangential_ivals(wsh_n, th, g("washer.od") / 2 - g("washer.notch_depth") / 2, z_mid, 20.0)
    nt = [iv for iv in C.tangential_ivals(nut, th, g("nut.tab_inner_radius") + 0.4, z_mid, 20.0) if iv[0] < 0 < iv[1]]
    if len(wn) == 2 and nt:
        add("tab tangential gap per side (T)", ((wn[1][0] - wn[0][1]) - (nt[0][1] - nt[0][0])) / 2, 0.5, 0.01)
    r_nf = C.radial_ivals(wsh_n, th, z_mid, 0, 120)[-1][1]
    r_tab = C.radial_ivals(nut, th, z_mid, 0, 120)[0][0]
    add("tab radial gap to notch floor (R)", r_tab - r_nf, 1.0, 0.01)
    # ---- thread mesh: nut over receiver, rotated by the helix rule, no interference expected
    P = g("thread.pitch")
    z_run = g("receiver.rim_above_floor") - g("thread.run_turns") * P
    z0 = z_run + P / 2.0 + 2 * P                                         # nut groove centres on receiver tooth centres
    nut_m = moved(nut, z=z0)
    add("thread mesh: overlap volume nut/receiver (mm3)", nut_m.common(rec).Volume, 0.0, 0.05)
    d_mesh = dist(nut_m, rec)
    add("thread mesh: minimum nut-receiver distance (mm) = axial flank gap g_a/2 x sin(flank)", d_mesh,
        g("fit.g_a") / 2.0 * math.sin(math.radians(g("thread.flank_deg"))), 0.01)
    json.dump(out, open(C.CACHE / "step3_cross_checks.json", "w"), indent=1)
    print("VERIFY_DONE %d checks, %d fail, %.1fs" % (len(out), sum(1 for o in out if not o["pass"]), time.time() - t0), flush=True)


if __name__ in ("__main__", "verify_step3"):
    try:
        main()
    except BaseException:
        import traceback
        traceback.print_exc()
        print("VERIFY_FAILED", flush=True)
