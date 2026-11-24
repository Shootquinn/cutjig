## TOPOLOGIST SIGNATURE

Script `sig.py`, `python -I`. Line numbers refer to `cr_scratch/step3_geometry_crossreview.md`.

Confirmed:
- W-2: line 60, seat 2.5.
- W-3: line 40, T9 0.924; lines 28, 36, 39 read 48.0, 88.0, 0.25.
- W-4: lines 10 and 69, key and ring top 1.995, gap 0.005.
- W-5: lines 48 and 11, pads 3 / 10.0 / 0.8 / 143.0, 2.402 mm3, class P.
- Lines 29, 30, 38, 57: 12 / 3.3, 37 deg, 11.75 / 3.0 / 40.0, 6.0 / 2.0.
- Lines 62 to 68: 12 slits, ligament 3.0, hole 8.0, centres 7.0 and 25.0, phase theta_key + 15 + 30k.

W-1 coefficient: h_w is `collet.web_height`, the ligament. Step 2 had L_c = h_w + h_s = 4 + 32, with h_s measured to the hole's far edge (centre 29, diameter 6). The check 4 x 0.9163 / (2 x 32 x 6) = 0.954 reproduces. Final geometry: h_w 3.0, h_s 29.0, l_h 8.0, strain **0.592**. The Loftsman's 0.916 used h_w 4 and h_s to the hole centre. My 0.881 also measured to the centre; read consistently, the 6.0 hole gives 0.790. Both readings pass with the 8.0 hole; the geometry stands.

Tangency, 8.0 hole:
- Top hole z 3.0 to 11.0: 0.5 over the 2.5 ledge, 1.0 over the ring top. Clear.
- Bottom hole z 21.0 to 29.0, ligament 3.0.
- Slit ends cross the hole circle 3.93 from its centre (1.5 against 8.0): transverse, clear.
- New: the bore chamfer edge sits at z = 32 - c, c = wall - 1.2. It meets the hole bottom (21.0) at d 90.6 and sits 0.0075 below the hole top (29.0) at d 106.585.

WITHHELD.

- Line 67: 0.916 -> 0.592.
- Line 65: chamfer edge meets hole bottom 21.0 at d 90.6 and is 0.0075 from hole top 29.0 at d 106.585 -> c = min(wall - 1.2, 10.5), and 2.5 where wall - 1.2 lies in (2.5, 3.5); the edge then clears both by at least 0.5 for d 85 to 106.585.
