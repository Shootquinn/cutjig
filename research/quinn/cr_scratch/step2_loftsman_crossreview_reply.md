## 1. Dispositions on D-1 to D-9 (the Topologist's Section 6)

All numbers below were run in `python -I` (script `cr.py` in the scratchpad), not by hand. alpha = 10 degrees, tan = 0.176327.

| ID | Verdict | Deciding quantity and the number that settles it |
|---|---|---|
| D-1 | ACCEPT. The chain follows the axial stack. New D_T = 149.58 mm. | Holder bottom in pose R = 2 + z0 + s_z = 13.626 (z0 1.7014, s_z 9.9247; sum 11.626). Collet cone radius there 61.74. Under my old chain the holder inner radius at that bottom was 64.09, so the radial gap was 2.350, not 0.30. The holder inner radius at its bottom is the clamped collet cone radius at K-max: D_S/2 + H tan(alpha) - Delta/2 = 58.5 + 5.290 - 1.75 = 62.040. Holder OD = 2(62.040 + 5) = 134.08. D_T = 134.08 + 0.50 + 10.0 + 5.0 = 149.58. Closed form: D_T = B_f + 2 t_c + 2 H tan(alpha) - Delta + 2 (t_h + g_reg + t_b + h) = 149.580. My old chain was dead on its own stack: first touch at holder bottom z = 0.299, full closure at z = -9.626, the holder meets the 63.79 foot ring at z = -7.92. It could not be built. |
| D-2 | ACCEPT. Contact height at K-max is 30.0, not 18.37. My L-4 is withdrawn. | Interval overlap [max(2, holder bottom), 32]. Holder bottom 2.000 at K-max, 9.089 at core d + 1.0, 11.926 at first touch (R0). Heights 30.0 / 22.91 / 20.08. L-4 assumed the holder cone started at the cone base in pose R; the stack puts it at 13.626. Gross cone area at K-max 11,368 mm2 against `seat.min_contact_area` 200. |
| D-3 | ACCEPT the finding. REFINE the cure: L_h = 88.0, p = 0.75, not 80.0. | The register is measured at first thread contact, not at pose R. Insertion there = L_h - (L_n - t_f) + p (hanging) = L_h - 40 + 0.75 (hanging) or L_h - 40 (seated). With L_h = 54 it is 14.0 / 15.5. Details in section 3. |
| D-4 | ACCEPT the rule. Flange OD = 144.08 (the Topologist's 148.18 belonged to the old minor). | Offset stack 0.30 (thread lateral) + 0.25 (register) = 0.55. Nut crest diameter = minor + 2 c_r = 144.58 + 0.70 = 145.28. Flange OD = 145.28 - 2(0.55 + 0.05) = 144.08. Old numbers: 0.35 clearance - 0.55 offset = -0.20, contact. |
| D-5 | ACCEPT. The flange jacking holes are deleted. No replacement is needed. | Required radial width 5.0 + 2 x 1.2 = 7.4. Available in the flange annulus 72.04 - 67.04 = 5.00 (it was 5.25). Also the holes lie under the nut plate and cannot be reached. Back-off authority: axial lift at 12 N m back-off F_up = 12 / k_up = 12 / 0.04263 = 281.5 N against the wedge-release need 46 / 88 / 128 N at mu_k 0.25 / 0.35 / 0.50. Minimum ratio 2.20. The collar carries the release. |
| D-6 | ACCEPT. The washer is a separate part and is always fitted. | With no washer the old pocket left a ring 74.34 - 74.30 wide: area 18.7 mm2 against the 1,924 mm2 annulus assumed. New washer annulus r 68.4 to 71.6: area 1,407 mm2; pressure at F = 267 N is 0.19 MPa. Mean bearing radius by the uniform-pressure formula 70.01 mm (old 71.7 stated, 72.24 by the formula on the old annulus). Plain case = printed ring, PTFE case = PTFE ring, same geometry. |
| D-7 | ACCEPT. S15 reads L_n - t_f >= min_engage + z0 + s_z,max + m. | 8 + 24 + 1.701 + 9.925 + 1.5 = 45.126, so L_n >= 45.13 and 48 stands (S = 40 >= 37.13). My earlier form gave 9.925 + 24 + 8 = 41.92, short by 3.2. |
| D-8 | REFINE. The wing is moved off the holder, not trimmed. | Wing ellipse: rho_0 = 96.0, a = 19.0, b = 18.0 (inner extreme rho 77.0, tip 115.0). Nut thread root radius 75.14, nut body radius 83.14, so the inner extreme is 1.86 outside the thread root and 6.14 inside the body for fusion. Clearance to the holder (r 67.04) and to the plate hole (r 68.04) is 9.0 mm or more: common(wing, holder) = 0 by 9.0 mm. Visible wing 83.14 to 115 = 31.9 mm. Root section at the body: height 26.5, thickness 12, bending at a 150 N tip load, lever 31.9 mm: 7.5 MPa against 45 MPa, factor 6.0. |
| D-9 | ACCEPT. K rim gap at core d + 1.0 is 8.59. | 13.126 - 1.701 - 2.836 = 8.589. My 10.3 dropped z0. |

Section 6 is closed. Nothing in it is carried forward.

## 2. Other findings, point by point

| Topologist finding | Verdict | Number |
|---|---|---|
| Thread H1 to H7 | ACCEPT | Receiver run is an integer number of turns: 48 mm (6 turns) from the rim, plus 4.0 land. E_K + P = 38.5 + 8 = 46.5, rounded up to 48. |
| Tessellation | ACCEPT 0.020 mm | At r = 74.79 the sagitta bound needs n >= 135.8 per turn. Export at 140. |
| alpha_crit | ACCEPT, new value | P / (2 D_T) = 8 / (2 x 149.58) = 1.532 degrees. True cross-thread onset (half-pitch offset at the edge) P / D_T = 3.064 degrees; this is the T9 known-bad tilt. |
| Cone sense C1 to C9 | ACCEPT, with the C9 value 11.626 | One variable `cone.alpha` drives both cones. |
| Nesting order, radial | ACCEPT, values revised | core 53.0 < bore 53.5/46.0 < collet cone < holder cone < holder OD 67.04 < receiver bore 67.29 < minor 72.29 < nut crest 72.64 < major 74.79 < nut root 75.14 < nut OD 83.14. Holder wall 5.0 at its bottom, 10.29 above the cone zone. |
| Tube envelope note | REFINE | With D_T = 149.58 the receiver major radius 74.79 is inside the cutting annulus edge 76.20 by 1.41 (was outside by 0.64). Not a defect: the cutter stop is held 10 mm above the collar top (124.38), and the rim is at 88.5, so the cutter lowest point is at least 45.9 above the thread. A2 takes the maximum over poses, as he said. |
| Nesting order, axial | ACCEPT, restated | Table in section 4. Holder bottom and K/R gaps do not depend on L_h. |
| Holder floor pair, S6 | ACCEPT | Holder bottom above floor 2.00 at K-max, 0.50 after the 1.5 stroke margin. Class G. Added. |
| Key slot radial gap | ACCEPT 0.55 | Slot floor radius 67.29 + 3.3 = 70.59 against key tip 67.04 + 3.0 = 70.04 = 0.550. Wall under the slot to thread root 1.70. |
| Collar ID unspecified | SUPPLIED | Holder bore above the cone zone 113.50 (equals the clamped collet top radius 56.75 x 2). Collar ID 114.0, radial clearance to the largest core (53.0) 4.0. Four M6 on r = 62.0. |
| Clamped-state solid, delta 0.005 | ACCEPT | I withdraw my 1e-3. Holder cone from the same `alpha` variable. A 0.02 degree mismatch would be 30 tan(0.02 deg) = 0.0105 mm, above the 0.01 contact band. |
| Alternating slits: 1 shell, genus 1, chi 0, keyhole relief | ACCEPT | Clamped slit 1.5 - pi x 3.5 / 12 = 0.584. Tests C9a (nominal >= 0.5) and C9b (worst >= 0.1) kept separate. |
| WS1 | Now unrepresentable | Holder inner radius at its bottom 62.04 against the collet wide end 63.79: blocked by 1.75. |
| WS3 | ACCEPT the fix | Collar OD 152.4 against nut crest bore 145.28: it cannot enter a flipped skirt by 7.12. Collar radius 76.2 stays under the wing inner extreme 77.0. |
| WS5 | Reachable band closed by section 3 | |
| WS6 (F3 sweep 7x7), WS7 (pocket-slot lead-in chamfer) | ACCEPT | |
| T9 inputs | ACCEPT | Pass lines in section 3. |
| Contact class table | ACCEPT with revised values | Co-Cr 4.0, H flange to nut crest 0.55 offset margin 0.05, plate top to collar underside p = 0.75 (K), washer pair added: flange top to washer to plate underside. |

## 3. Register (D-3), closed by calculation

Skirt below the flange underside S = L_n - t_f = 40.0. Plate hole radius 68.04, washer inner radius 68.4. The plate tilts between the washer (lower contact) and the collar underside (upper contact on the far side): shortest arm 68.4 + 68.04 = 136.44 mm. (The Topologist used 144.44; the shorter arm is the worst case.)

Pass lines, stated once. Total tilt at first thread contact (register plus plate rock) <= alpha_crit / 1.5 = 1.021 degrees, which is 3.0 on the true onset 3.064. Register alone, seated <= alpha_crit / 2 = 0.766 degrees.

| L_h | p | g_reg | seated register | hanging register | plate rock | hanging total | vs 1.021 |
|---|---|---|---|---|---|---|---|
| 54 | 1.5 | 0.25 | 2.045 | 1.848 | 0.630 | 2.477 | fails |
| 80 | 0.75 | 0.25 | 0.716 | 0.703 | 0.315 | 1.018 | passes by 0.003 |
| 84 | 0.75 | 0.25 | 0.651 | 0.640 | 0.315 | 0.955 | passes |
| 88 | 0.75 | 0.25 | 0.597 | 0.588 | 0.315 | 0.903 | passes, factor 1.70 on alpha_crit |
| 88 | 0.75 | 0.30 | 0.716 | 0.705 | 0.315 | 1.020 | passes by 0.001 |
| 80 | 0.75 | 0.30 | 0.859 | 0.844 | 0.315 | 1.159 | fails |

Maximum g_reg that still passes the 1.021 line: L_h = 80 gives 0.2513, L_h = 84 gives 0.2759, L_h = 88 gives 0.3006. Minimum L_h for g_reg 0.25 is 79.80; for 0.30 it is 87.91.

Decision: L_h = 88.0. The Topologist's 80 passes only if the register fit is held at 0.2513 or tighter, a headroom of 0.001 mm on a printed fit. Every other seed fit in `params.yaml` is 0.30 or 0.35. L_h = 88 is sized to g_reg = 0.30 and passes at the seed 0.25 with factor 1.70. Receiver rim above floor = 2 + 88 - 1.5 = 88.5. The p = 0.75 figure is accepted: lost motion p / P = 0.094 turn. If the Step 8 coupon returns g_reg above 0.30, L_h follows from L_h = S - p + 2 g_reg / tan(1.021 - atan(p / 136.44) in degrees); that is the only edit.

Key length 40.0 stays; the key is in its slot at first contact (insertion 48.0 or more).

## 4. Revised numbers table (every changed value)

| Quantity | Old | New | Status | Test |
|---|---|---|---|---|
| Holder bottom in R | 13.63 (unsupported by my chain) | 13.626 | DERIVED | F1, F6 |
| Holder inner radius at its bottom | 64.09 | 62.040 | DERIVED | F1, WS1 |
| Holder OD | 138.18 | 134.08 | DERIVED | T9, A1 |
| Receiver bore | 138.68 | 134.58 | DERIVED | T9 |
| Thread minor / major `thread.major` | 148.68 / 153.68 (earlier seed 165) | 144.58 / 149.58 | DERIVED | T2, P1 |
| Nut crest / root / OD `wingnut.body_od` | 149.38 / 154.38 / 170.4 | 145.28 / 150.28 / 166.28 | DERIVED | A1, A2 |
| Releasing cone fallback, reference only | D_T 164.94 | D_T 160.84, nut OD 177.54 (+11.26 over primary) | DERIVED | A3 |
| Pitch diameter / lead angle | 151.18 / 0.965 | 147.08 / 0.992 degrees | DERIVED | T7 |
| alpha_crit / onset tilt | 1.49 / 2.98 | 1.532 / 3.064 degrees | DERIVED | T9 |
| Contact height K-max / core d + 1.0 / first touch | 18.37 | 30.0 / 22.91 / 20.08 | DERIVED | F1 |
| Holder body length L_h | 54.0 | 88.0 | DERIVED | A3, T9 |
| Receiver rim above floor `receiver.rim_above_floor` | 54.5 | 88.5 | DERIVED | F6, S6 |
| Lift play `nut.lift_play` | 1.5 | 0.75 | ASSUMED | A3, T9 |
| Collar top above plate top | 7.5 | 6.75 | DERIVED | F4, A2 |
| `core.min_exposed` | 128.9 | 128.12 (121.369 + 6.75) | DERIVED | F4 |
| Flange OD (and flange top annulus) | 148.68 (5.25) | 144.08 (5.00, r 67.04 to 72.04) | DERIVED | A1, WS2 |
| Collar OD / ID | 148.68 / unspecified | 152.4 / 114.0 | ASSUMED | WS3, A1 |
| Holder bore above the cone zone | not stated | 113.50 | DERIVED | A3 |
| Plate hole ID | 140.2 | 136.08 (holder OD + 2.0) | DERIVED | A1 |
| Washer (new part) | none | ID 136.8, OD 143.2, thickness 1.3 | ASSUMED | A1, T7 |
| Washer pocket in plate underside | r 70.1 to 74.3, depth 1.0 | r 68.3 to 71.7, depth 1.0 | ASSUMED | A1 |
| Jacking holes `holder.jack_hole_*` | 2 x M6 at r 71.84 | deleted | DERIVED | A3, H5 |
| Wing ellipse | rho_0 70, a 45, b 18 | rho_0 96, a 19, b 18 | ASSUMED | F5, A1 |
| Stack (R / K-max / K d + 1.0), flange underside | 67.63 / 56.00 / 63.09 | 101.63 / 90.00 / 97.09 | DERIVED | A2 |
| Plate top | 83.63 / 72.00 / 79.09 | 117.63 / 106.00 / 113.09 | DERIVED | F4 |
| Collar top | 91.13 / 79.50 / 86.59 | 124.38 / 112.75 / 119.84 | DERIVED | F4, A2 |
| Skirt bottom | 27.63 / 16.00 / 23.09 | 61.63 / 50.00 / 57.09 | DERIVED | A4 |
| Engaged length | 26.87 / 38.50 / 31.41 | 26.87 / 38.50 / 31.41 (unchanged) | DERIVED | T4, S13 |
| Flange minus rim | 13.13 / 1.50 / 8.59 | 13.13 / 1.50 / 8.59 (unchanged) | DERIVED | F6 |
| Clamped core tilt, 0.30 / contact height | 0.93 degrees, 8.2 / 12.2 mm | 0.57 degrees (5.0 / 7.5 mm at 0.5 / 0.75 m) at 30.0; 0.75 degrees (6.5 / 9.8 mm) at 22.91 | ASSUMED | H3 |
| Register tilt | 0.716 | 0.597 seated, 0.588 hanging | DERIVED | T9 |

Withdrawn: L-3 (c_s in the radial chain). c_s cancels in D_T; it sets only the travel z0. L-4 (contact height 18.37). The `chain.c_s` key stays for z0.

Unchanged and re-confirmed: z0 1.701, s_z,max 9.925, s_z at d + 1.0 2.836, g_stop 13.126, stroke margin 1.5, throat slack 1.29, collet law, slit count 12 and width 1.5, coverage table of seven windows.

## 5. Holding estimate, rerun on D_T = 149.58 with the washer geometry

k = r_p (tan(lambda) + mu') / (1 - mu' tan(lambda)) + mu_b r_bm, r_p = 73.54 mm, r_bm = 70.01 mm, mu' = 0.3536. Seeds as before, T_nut = 12 N m.

| | k (m/N) | F | T_hold d = 105 | T_hold d = 90 | Nut torque for 10 N m (105 / 90) |
|---|---|---|---|---|---|
| Plain printed washer | 0.04494 | 267.0 N | 10.65 N m | 9.13 N m | 11.26 / 13.14 N m |
| PTFE washer | 0.03094 | 387.8 N | 15.47 N m | 13.26 N m | 7.76 / 9.05 N m |

At 10 N m of nut torque: plain 8.88 / 7.61, PTFE 12.89 / 11.05 (d = 105 / 90). Spread from the unmeasured coefficients at d = 90: plain 3.8 to 23.1 N m, PTFE 5.8 to 31.0 N m.

Releasing cone (reference, alpha = 20): plain 7.52 / 6.45 N m, PTFE 10.72 / 9.19. Nut torque for 10 N m at d = 90: 18.6 plain, 13.1 PTFE. The ruling stands: that branch cannot reach 10 N m at d = 90 within a 12 N m hand limit even with the washer, and it costs +11.26 mm of thread major.

Plain printed washer, d = 90: 9.13 against 10, short by 8.7 percent. I say this plainly: the plain case does not meet the design torque at the smallest core. The PTFE washer does, by 33 percent (d = 90), and it is the recommended default. DERIVED from ASSUMED inputs. This is a prediction; H1 settles the sign.

## 6. Status per item

| Item | Status | Basis |
|---|---|---|
| Thread (hand, pitch 8, 45/45, single start, D_T 149.58, nut 48 mm, run 48 + 4 land) | AGREED | Both personas carry D_T = 149.58 (derived by the closed form in D-1) and L_n = 48 under the corrected S15. |
| Taper (alpha 10, self-lock 0.176 < 0.25, z0 1.701, s_z 9.925, g_stop 13.126, release by captured collar) | AGREED | |
| Seat (holder bottom 13.626 in R, 2.00 at K-max, contact 30.0 / 22.91 / 20.08, delta 0.005 coincident-face strategy, foot pocket 128.18) | AGREED | |
| Register | DISPUTED between L_h = 80 (Topologist) and 88 (here). CLOSED here at 88.0. | Deciding measurement: hanging total tilt against the 1.021 degree line with the 136.44 mm plate arm. L_h = 80 passes by 0.003 degrees and tolerates g_reg only to 0.2513; L_h = 88 tolerates 0.3006. p = 0.75, rim 88.5. |
| Collet family (7 windows, closure 3.5, N = 12, w_s 1.5, strain 0.954 of the allowable) | AGREED | |
| Holding estimate | AGREED on the model and the revised numbers: 10.65 / 9.13 N m plain, 15.47 / 13.26 N m PTFE (d = 105 / 90) | Washer always fitted (D-6). Plain washer misses 10 N m at d = 90 by 8.7 percent; H1 decides. |
