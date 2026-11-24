# 1. Thread

Frame: z = 0 at receiver floor top (datum A at z = -40). All arithmetic `python -I` (scratchpad `s3.py`). Status: D derived, A assumed, C corrected (params value replaced), K closed at Step 2. Radial = per side; diametral stated as D.

| Symbol (key) | Basis | Formula | Value | Status |
|---|---|---|---|---|
| D_T `thread.major` | D | closed form, D-1 | 149.58 | K |
| D_1 `thread.minor` | D | D_T - 2h, h = `chain.h` 2.5 | 144.58 | K |
| D_2 pitch | D | D_T - h | 147.08 | D |
| lambda lead | deg | atan(P / (pi D_2)) | 0.992 | D |
| crest flat = `thread.land_width` | axial | P/2 - h tan 45 | 1.50 (was 1.0; 1.0 breaks P/2 tooth at pitch line) | C |
| nut crest / root | D | D_1 + 2c_r / D_T + 2c_r | 145.28 / 150.28 | K |
| c_r `fit.c_r` | radial | seed | 0.35 | A |
| g_a `fit.g_a` | axial, total | seed | 0.30 (nut tooth 3.70, receiver tooth 4.00 at pitch line) | A |
| e_t thread lateral float | radial | (g_a/2) / tan 45 | 0.15 (Step 2 stack used 0.30: conservative, flange OD 144.08 kept, margin 0.20) | D |
| `thread.lead_in_length` | axial | 45 deg chamfer crest to pitch line: receiver rim r 74.79 to 73.54; nut skirt bottom r 72.64 to 73.54 | receiver 1.25, nut 0.90 (was 8: one pitch at each end drops R full-form engagement to 10.87, below 24) | C |
| runout land | axial | below receiver run, r = 72.29 | 4.0 (z 40.5 to 36.5) | K |
| receiver run | axial | 6 turns from rim 88.5 | 48.0 (z 88.5 to 40.5) | K |
| helix tool overshoot max | radial | (0.9P - groove)/2; groove 6.5 receiver, 6.10 nut | receiver 0.35, nut 0.55 (FreeCAD groove < 0.9P rule) | D |

Engagement (overlap of thread zones; full-form = overlap - 1.25 - 0.90):

| Pose | Flange underside z | Skirt bottom z | Engaged | Full-form | Pitches (full-form) |
|---|---|---|---|---|---|
| K-max (core d-1.5) | 90.000 | 50.000 | 38.50 | 36.35 | 4.54 |
| K (core d+1.0) | 97.089 | 57.089 | 31.41 | 29.26 | 3.66 |
| R | 101.626 | 61.626 | 26.87 | 24.72 | 3.09 |

`thread.min_engage_pitches` 3 (24.0) holds in every pose; R margin 0.72.

Tilt budget at first thread contact (T9): alpha_crit = P/(2 D_T) = 1.532 deg; line 1.021 deg (1.5 factor). Register seated atan(2 g_reg / 48.0) = 0.597; hanging atan(0.5 / 48.75) = 0.588; plate rock atan(0.75 / 136.44) = 0.315. **T9 value: 0.903 deg against 1.021.** D.

# 2. Cone and seat

| Symbol (key) | Basis | Formula | Value | Status |
|---|---|---|---|---|
| alpha `cone.alpha` | deg | | 10 | K |
| H `chain.H` cone height | axial | z 2.00 to 32.00 on the collet | 30.0 | A |
| collet cone r top / base, free | radial | 58.5; 58.5 + H tan alpha | 58.500 / 63.790 | D |
| collet height | axial | ring 2.0 + H | 32.0 | D |
| holder cone r bottom / top | radial | 63.79 - 1.75; - 5.29 | 62.040 / 56.750 | K |
| holder cone thickness t_h | radial | 67.04 - 62.04 at bottom; 67.04 - 56.75 at top | 5.00 / 10.29 | D |
| z0 | axial | c_s / tan alpha, c_s 0.30 | 1.701 | K |
| s_z,max | axial | 1.75 / tan alpha | 9.925 | K |
| foot ring height `holder.bottom_above_floor_Kmax` | axial | | 2.00 (ring top z 2.00) | K |
| foot ring outer radius r_fo | radial | register r 67.29 - `fit.seat_clearance` 0.30 | 66.99 | D |
| foot ring lip `collet.foot_ring_width` | radial | r_fo - 63.79 | 3.20 (was 10: puts r_fo at 73.79, 6.5 outside the register bore) | C |
| seat diameter (new `seat.diameter`) | D | = register bore | 134.58: flat floor, no pocket. Step 2 foot pocket 128.18 withdrawn (it would not take the 3.20 lip) | C |
| seat depth (new `seat.depth`) | axial | ring stands on z 0 | 0 | D |
| floor ledge hole (new `receiver.floor_hole_dia`) | D | below smallest core ledge ID 83.30 (87.3 custom) | 80.0 debris path | A |
| core seat `collet.core_seat_height` / `_width` | axial / radial | inward ledge at bore bottom, z 0 to 4 | 4 / 3; ledge ID = B_f - 6 | A |
| ring top contact area K-max | mm2 | pi(65.24^2 - 62.04^2) | 1279.6 | D |
| cone contact area K-max | mm2 | | 11,368 against 200 | K |

Contact classes (G gap, C contact; values mm):

| Pair | R | K d+1 | K-max |
|---|---|---|---|
| holder cone / collet cone | G 0.30 radial | C | C |
| holder bottom / ring top | G 11.626 | G 7.089 | C |
| holder bottom / floor | G 13.626 | G 9.089 | G 2.000 |
| flange underside / rim | G 13.126 | G 8.589 | G 1.500 |
| holder OD / register bore | G 0.25 | G 0.25 | G 0.25 |
| ring OD / register bore | G 0.30 | G 0.30 + 1.75 | G 2.05 |
| collet bore / core | G 0.5 to 1.75 | C | C |
| core bottom / core seat; ring / floor | C | C | C |
| plate underside / washer / flange top | G 0.75 | C | C |
| plate top / collar underside | C | G 0.75 | G 0.75 |
| nut crest / flange OD | G 0.60 | G 0.60 | G 0.60 |

# 3. Slits, wall, bore

Slit count rule: N = 2 ceil(pi Delta_max / (2 (w_s - w_min))), Delta_max = 3.5 D (window d-1.5 to bore d+2), w_s 1.5, w_min 0.5: pi x 3.5 / 1.0 = 11.0, so N = 12. Delta_max does not depend on d, so N = 12 for every d in 85.0 to 106.585, including 87.3. D.

| Symbol | Basis | Value | Status |
|---|---|---|---|
| w_s `collet.slit_width_seed` | tangential | 1.5 | A |
| clamped slit, K-max | tangential | 1.5 - pi 3.5/12 = 0.584 | K |
| pattern | | 6 open at top, 6 open at bottom, alternating | K |
| ligament b (new `collet.slit_ligament`) | axial, hole edge to end face | 4.0 | A |
| relief hole `collet.relief_hole_dia` | D | 3.0, centre 5.5 from far face | A |
| slit length (new `collet.slit_length`) | axial, open face to hole centre | 32 - 5.5 = 26.5 | D |
| overlap, both sets cut | axial | z 5.5 to 26.5 = 21.0 | D |
| web strain | | 0.954 of allowable: carried from Step 2, NOT re-derived here | carried |

Bottom-open slits cut the foot ring and core ledge; top-open slits stop above them.

bore_free(d) = d + `core.tol` 1.0 + `collet.c_i` 1.0. Walls radial.

| d | B_f | wall top (58.5 - B_f/2) | wall base | chamfer (wall top - 1.2) | ledge ID |
|---|---|---|---|---|---|
| 87.3 | 89.30 | 13.85 | 19.14 | 12.65 | 83.30 |
| 90.0 | 92.00 | 12.50 | 17.79 | 11.30 | 86.00 |
| 92.5 | 94.50 | 11.25 | 16.54 | 10.05 | 88.50 |
| 95.0 | 97.00 | 10.00 | 15.29 | 8.80 | 91.00 |
| 97.5 | 99.50 | 8.75 | 14.04 | 7.55 | 93.50 |
| 100.0 | 102.00 | 7.50 | 12.79 | 6.30 | 96.00 |
| 102.5 | 104.50 | 6.25 | 11.54 | 5.05 | 98.50 |
| 105.0 | 107.00 | 5.00 | 10.29 | 3.80 | 101.00 |

# 4. Register

| Symbol (key) | Basis | Formula | Value | Status |
|---|---|---|---|---|
| `holder.flange_od` | D | 145.28 - 2(0.55 + 0.05) | 144.08 | D |
| `holder.flange_thickness` t_f | axial | | 8.0 | A |
| holder OD | D | | 134.08 | K |
| `receiver.register_bore_radius` | radial | | 67.29 | K |
| `register.g_reg` | radial | | 0.25 | K |
| `holder.length` L_h | axial, bottom to flange underside | | 88.0 | K |
| `receiver.register_depth` | axial, pilot insertion at first thread contact | L_h - S | 48.0 (was 24: the bore runs rim to floor; 24 is not a measured quantity) | C |
| bearing recess | nut plate underside | see section 6 | | |
| `receiver.key_slot_width` | tangential | | 12.00 | A |
| `holder.key_width` | tangential | 12 - 0.25 across | 11.75 (was 11.4 = 0.60 across) | C |
| `receiver.key_slot_depth` | radial | slot floor r 70.59, wall to thread root 1.70 | 3.30 (was 6: floor r 73.29 cuts 1.0 through the thread root r 72.29) | C |
| `holder.key_height` | radial | key tip r 70.04, gap 0.55 | 3.00 (was 5) | C |
| holder key length (new `holder.key_length`) | axial, from holder bottom | | 40.0 | K |
| `receiver.key_offset_deg` | deg | | 37 | A |
| slot extent | axial | rim z 88.5 to floor z 0 (collet foot key shares it) | 88.5 | D |
| key rotation play | deg | 0.25 / 68.5 rad | 0.209 | D |
| holder key bearing at 10 N m | MPa | 146 N on 2.75 x 40 | 1.33 | D |

"60 degree sector": no file derives it (only `access.key_sector_deg`, a hex-key swing). Withdrawn.

Collet foot key indexes only: at d = 105 cone friction capacity mu_k r_m = 20.79 against core mu_c cos(alpha) d/2 = 20.68 per unit N (ASSUMED mu), so torque goes cone, holder, holder key.

# 5. Clamped-state solid

Same generator call, five parameters: (1) bore = d_core; (2) Delta = B_f - d_core (D); (3) slit = w_s - pi Delta / 12; (4) cone radii reduced by Delta/2 + delta_r; (5) holder bottom z = 2 + s_z,max - s_z, s_z = (Delta/2) / tan alpha. Ring stays on z 0.

Offsets depend on core position in the window only; identical for all seven d and 87.3:

| Core | Delta D | s_z | holder bottom z | slit |
|---|---|---|---|---|
| d - 1.5 (K-max) | 3.50 | 9.925 | 2.000 | 0.584 |
| d (nominal) | 2.00 | 5.671 | 6.254 | 0.976 |
| d + 1.0 | 1.00 | 2.836 | 9.089 | 1.238 |

Coincidence offset: delta_n = 0.005 normal (under the 0.01 band) = delta_r 0.00508 radial, applied to the collet cone. Lifting the holder instead needs delta_z = delta_n / sin alpha = 0.0288, which opens the K-max ring pair past 0.01. At K-max drop the clamped ring top to z 1.995. Both pairs read 0.005; common volume 0.

# 6. Nut

| Symbol (key) | Basis | Formula | Value | Status |
|---|---|---|---|---|
| `nut.length` L_n | axial, skirt bottom to flange top plane | S + t_f | 48.0 | K |
| `nut.skirt_below_flange` S | axial | | 40.0 | K |
| washer proud h_wp | axial | `washer.thickness` 1.3 - `nut.washer_pocket_depth` 0.8 | 0.50 | D |
| nut plate t_p (new `nut.plate_thickness`) | axial | 16 - t_f - h_wp | 7.50 (keeps plate top = flange underside + 16, so every Step 2 z holds) | D |
| nut overall (new `nut.overall_height`) | axial | 40 + 8 + 0.5 + 7.5 | 56.0 | D |
| nut internal thread length | axial | skirt bottom to plate underside | 48.5 | D |
| `wingnut.body_od` | D | | 166.28 | K |
| plate hole | D | holder OD + 2.0 | 136.08 | K |
| dust skirt gap to receiver shoulder z 36.5 | axial | skirt bottom - 36.5 | 13.50 K-max, 20.59 K, 25.13 R (A3h at least 8) | D |

Wings: 2 vertical fins at 0 and 180 deg; side profile 40 at root (`wing_root_width` = `wing_height`), 28 at tip (`wing_tip_width`), taper 10.67 deg per edge; `wing_thickness` 14 tangential; `edge_radius` 6. Arm L_a = 115 - 83.14 = 31.86; top flush with plate top. Push centroid r_g = 83.14 + L_a (40 + 2 x 28)/(3 x 68) = 98.13.

Span: 10 N m hold at d = 90 needs T_nut 9.05 (PTFE, ASSUMED mu): 46.1 N per hand; 12 N m needs 61.1 N. At an ASSUMED 50 N per hand the minimum span is 197.6; `wingnut.span` 230 and `sweep_clear_radius` 115 confirmed. Root bending, Z = 1306.7 mm3: 1.75 MPa at 15 N m on one wing, 3.11 MPa at 25 N m, against 45.

Knuckle: wing bottom z 66.0 (K-max), 73.09 (K), 77.63 (R); clear to base plate top z -28 is 94.0 against 50, if nothing of the receiver lies outside r 80 above z 16.0.

Tommy bar: a 20 deep radial hole in the 8.0 skirt wall breaks the thread. Four bosses at 45/135/225/315 deg, axis 20 below plate top, OD 23, hole 13 (`nut.tommy_hole_dia`) x 20, bottom r 78.14 (3.0 over root), end r 98.14. Single-ended bar (the bore blocks a through bar): grip centroid r 150 gives 15 N m at 100 N; end r 200; `nut.tommy_bar_length` 122 (was 300) C. Boss root 6.2 MPa at 15 N m, 13.6 MPa at 25 N m. Axial at 25 N m: 808 N.

Release marker: arrow on plate top spanning `nut.release_dead_turn_deg` 33.75, mark line at the key azimuth.

Bearing face: pocket floor r 68.04 to 71.90, depth 0.8, normal -Z; washer bears on flange top r 67.04 to 72.04.

Captive washer: any lip holding a flat washer 0.5 proud overlaps it when seated. Retention C: three press pads, ID 143.0 on OD 143.2 (0.10 radial), a declared interference pair exempt from the overlap test. Tab notch 6.0 wide x 2.0 deep (1.2 ring left); tab 5.0 wide, inner r 70.6: gaps 0.5 tangential per side and 1.0 radial, Engineer seeds confirmed. Windows 3 x 10 wide to r 71.9.

# 7. Stop height

Collar top = z_hb + L_h + t_f + h_wp + t_p + p + t_col, with t_col (collar thickness) = 6.75 - 0.75 = 6.00.

z_hb is highest among clamped poses at core d + 1.0: 2 + 9.925 - 2.836 = 9.0891. It is the same for all seven d (collet outer is d-independent).

Collar top = 9.0891 + 88 + 8 + 0.5 + 7.5 + 0.75 + 6.0 = **119.839** (floor). + `icd.floor_above_datum_a` 40 = **159.84** `stop.collar_top_z` CONFIRMED. + `stop.g_stop` 25 = **184.84** `stop.height_z` CONFIRMED.

Conditions: t_p 7.5 (t_p 8 gives 160.34 / 185.34); wing top 113.09 below; collar screws flush, 4 x M6 ISO 10642 countersunk (head 12.0 x 3.3) on r 62.0, so `collar.id` C 114 to 110 (head edge r 56; core clearance 2.0). Socket heads would add 6.0.

`stop.collar_top_z_min` 152.75 confirmed (112.75 + 40).

# 8. Holding (T7). PREDICTION FROM ASSUMED COEFFICIENTS.

T_hold = mu_c F d / (2 (tan alpha + mu_k)). F = T_nut / k. k = r_p (tan lambda + mu') / (1 - mu' tan lambda) + mu_b r_bm. r_p 73.54, lambda 0.992 deg, mu' = 0.25 / cos 45 = 0.3536, r_bm 70.01 (washer r 68.4 to 71.6, uniform pressure). mu_c 0.40, mu_k 0.35, mu_b 0.25 plain / 0.05 PTFE. All mu ASSUMED. T_nut 12 N m.

| Washer | k (m) | F (N) | d 90 | d 97.5 | d 105 | T_nut for 10 N m (90 / 97.5 / 105) |
|---|---|---|---|---|---|---|
| PTFE (fitted) | 0.03094 | 387.8 | 13.26 | 14.37 | 15.47 | 9.05 / 8.35 / 7.76 |
| plain (reference) | 0.04494 | 267.0 | 9.13 | 9.89 | 10.65 | 13.14 / 12.13 / 11.26 |

Inputs unchanged from Step 2, so values unchanged. Not modelled: collet stiffness; ring path at K-max (upper bound there).

# 9. Parts for build (Rule P features; mm; keys or new keys)

| Part | Signed features and dimensions |
|---|---|
| Receiver | Register bore r 67.29, z 0 to 88.5; rim chamfer 1.0 x 45 (new `receiver.register_chamfer`, A). Thread per section 1, z 40.5 to 88.5, rim chamfer 1.25. Land r 72.29, z 36.5 to 40.5; shoulder to r 80.0 at z 36.5. Key slot 12.00 x 3.30, z 0 to 88.5, at 37 deg. Floor z 0, hole 80.0. |
| Holder | OD 134.08; bottom annulus r 62.04 to 67.04; cone r 62.04 to 56.75 over 30.0; bore 113.50. Flange underside +88.0, OD 144.08 x 8.0. Top +104.75. Key 11.75 x 3.00 x 40.0 at 37 deg. 4 x M6 inserts, r 62.0. |
| Nut | Thread per section 1, length 48.5, chamfer 0.90. OD 166.28, overall 56.0, plate 7.5, hole 136.08. Pocket 143.8 x 0.8, pads ID 143.0, tab 5.0 to r 70.6, 3 windows. Wings 40/28/14 R6 to r 115. 4 bosses OD 23, hole 13 x 20. Arrow 33.75 deg, 40 long, 0.8 deep. |
| Washer | 136.8 / 143.2 / 1.3 PTFE stock; notch 6.0 x 2.0. |
| Collet foot ring (generator feature) | z 0 to 2.00, bore to r 66.99; ledge z 0 to 4, inward 3; foot key 11.75, r 66.99 to 70.04, z 0 to 2.00. |
| Collar | OD 152.4, ID 110.0, 6.00 thick. |

# Numbers I expect the Topologist to challenge

1. Washer press pads, 0.10 interference, exempt from the overlap test.
2. delta_r 0.00508 on the collet; ring top 1.995.
3. Foot ring lip 3.20; 128.18 pocket withdrawn.
4. Key slot depth 3.30 (not 6); wall 1.70.
5. Lead-in 1.25 / 0.90 (not 8); R full-form margin 0.72.
6. Lateral float 0.15 against 0.30 used.
7. Nut plate 7.5 holding 159.84 / 184.84.
8. Collar ID 110, countersunk screws.
9. Web strain 0.954 carried, not re-derived.
10. Tommy bar 122, single-ended.

Withdrawn: "60 degree sector" key; any hand force beyond the ASSUMED 50 N.
