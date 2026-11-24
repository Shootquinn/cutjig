"""Evidence for HD5 and HD6: the test predicates fail on probe-window choices, not on holder geometry. Re-reads the built holder with the
annulus bounds and the flange-interval radius changed (no test file edited)."""
import math
import sys
sys.path.insert(0, "C:/Users/Quinn Morley/OneDrive/PROJECTS/CC/CuttingJig/tests/probes")
import probe_lib as L
C = L.C
p = L.params()
G = lambda k: L.G(p, k)
sh = L.part("holder")
r_od = G("receiver.register_bore_radius") - G("register.g_reg")
r_fl = G("holder.flange_od") / 2
z0, z1 = sh.BoundBox.ZMin - 1, sh.BoundBox.ZMax + 1
key_az = G("receiver.key_offset_deg")
# the probe window as written
r0 = G("holder.insert_circle_radius") + G("holder.insert_dia") / 2 + 0.5
r1 = r_fl - G("holder.index_notch_depth") - 0.5
print("EVID window written r0 %.2f r1 %.2f holder OD r %.2f key tip r %.2f" % (r0, r1, r_od, r_od + G("holder.key_height")), flush=True)
bad_written = []
for k in range(3):
    r = r0 + (r1 - r0) * k / 2.0
    for az in range(0, 360, 3):
        n = len(C.axial_ivals(sh, float(az), r, z0, z1))
        if n != 1:
            bad_written.append((round(r, 2), az, n))
print("EVID as written: azimuths with !=1 interval", bad_written, flush=True)
half = math.degrees(math.asin(G("holder.key_width") / 2 / r1)) + 3.0
bad_fixed = [b for b in bad_written if abs(((b[1] - key_az + 180) % 360) - 180) > half]
print("EVID excluding the key sector (+-%.1f deg about %.0f): remaining" % (half, key_az), bad_fixed, flush=True)
# HD6
ref = (key_az + 180.0) % 360.0
iv_written = C.axial_ivals(sh, ref, (r0 + r1) / 2, z0, z1)
r_mid = (r_od + r_fl) / 2
iv_fixed = C.axial_ivals(sh, ref, r_mid, z0, z1)
down = sorted(set(round(f.CenterOfMass.z, 3) for f in sh.Faces if f.Surface.__class__.__name__ == "Plane" and f.Area > 50 and f.normalAt(0, 0).z < -0.99))
print("EVID HD6 interval at r %.2f (written, inside the tube wall): %s" % ((r0 + r1) / 2, [(round(a, 3), round(b, 3)) for a, b in iv_written]), flush=True)
print("EVID HD6 interval at r %.2f (flange annulus): %s" % (r_mid, [(round(a, 3), round(b, 3)) for a, b in iv_fixed]), flush=True)
print("EVID HD6 downward planar faces z:", down, "allowed [bottom %.3f, flange underside %.3f]" % (sh.BoundBox.ZMin, iv_fixed[-1][0]), flush=True)
print("EVID_DONE", flush=True)
