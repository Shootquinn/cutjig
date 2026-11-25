# Step 1.2 (a) Designer params review, S2 plan XY

Sources (read 2026-11-25): gameplan l.118-206, 243-261, 493-505, 595-703; step1.2_manager_open.md sections 0, 1, 4 and P1; step1.1_manager_close.md sections 8, 9; my 1.1 files (params review, spec sign-off N1 to N6, `docs/sketches/s1_visual_gate_r3.md`); `docs/sketches/proposed_params.yaml`; `docs/sketches/s1_spec.yaml` placed rows; `docs/sketches/s1_checks_r4.json` keys_read; params.yaml `drill`, `icd`, `frame`, `profile`, `base`; ASSEMBLY.md Coordinate frame; llm_plm_cad.md 8.4 to 8.4.2; `docs/sketches/s1_pose_load_r4.png` (read as an image). Plan distances are DERIVED by convex-polygon distance on the spec footprints (radial strips as 4-gons, round parts as 128-gons; script in the session scratchpad, not a project file). Heights z_A unless marked z_S (z_S = z_A + 60).

## Corrections to the brief

1. **The theta 270 frame member cannot stand on the plate top at any radius from 250 to 300.** `base.column_notch` (70 x 65, x -35 to 35, y -304 to -239, one per long edge, params, Quinn's base) removes the plate there. At `frame_upper.radius` 300 the member spans y -330 to -270: 34 of its 60 depth sits over the notch void on the rail, 26 hangs in air. Design Notes 23 "frame members stand on the plate top" holds for the theta 30 and 150 members only. S1 never drew the theta 270 member, so S1 never saw it. DERIVED.
2. **Radius 274 seats that member on the rail.** At 274 the member spans y -304 to -244 and x -30 to 30, wholly inside the notch (5 clear each side, 5 inboard), centred on the rail centre line y -274 (rail y -304 to -244 = `icd.footprint_y` / 2 minus `profile.width`). The in-notch range is 269 <= R <= 274. DERIVED.
3. **Screw phase change does not fix S2-c at R 300.** Over every screw phase psi, the largest member radius that keeps all three members on the 644 x 608 plate is 292.0 (psi 0 or 60 mod 60); at the current psi 30 it is 274.0. DERIVED (0.5 mm search).
4. **My 1.1 NOTE N2 said 274 clears the guide lugs by about 117. The plan distance is 76.02** (member theta 30 to lug theta 0). Still above G 10. DERIVED.
5. **The S2-5 sector as written cannot be a free-space test.** A sector with its apex on the axis overlaps the drill, keep-out, bearing, gear and ring disc in every azimuth. It is a test against a named list. O1 confirmed: at the current phase the sector between screws 30 and 150 holds the NEMA 23 (r 142 to 218, half-width 28.5), its mount and the pinion (r 95.22 to 140, half-width 45.62) on the 90 deg bisector.
6. **One descent-stop pad.** S1 draws one pad at theta 150 (`descent_stop`, `jackscrew.angle[1]`). A metal stop rated 1000 N on one rim point at r 207.5 puts a 207 N m tipping moment on the ring. It is a limit, but not a stop. FAIL in section 1.
7. Lower bound 250 confirmed: ring rim to member inner face 250 - 30 - 210 = 10.00 (G 10 met with zero margin; plan polygon 10.03 at theta 30 and 150). The arms run r 181 to 220, which still carries the pad (r_out 215). DERIVED.

## 1. Functional completeness (8.4a), S2 parts

| # | Feature | Keys | Result | Missing leaf, proposed value |
|---|---|---|---|---|
| 1 | Base plate: 644 x 608 x 12, spigot hole 160.4, column notches, slotted holes, key and pin pockets, drain | `icd.footprint_*`, `base.*` (params) | PASS | none |
| 2 | Base frame: rails along X at y +-274, end members at x +-232, plate supports at x +-112 | `frame.end_x`, `frame.support_x`, `frame.members`, `profile.width` | PASS | rail centre y is DERIVED: `icd.footprint_y / 2 - profile.width / 2` = 274 (spec expression; no key) |
| 3 | Screw frame members a, b (theta 30, 150) | `frame_upper.radius`, `.member_profile`, `.member_length` | PASS | radius per section 3 |
| 4 | Screw frame member c (theta 270) | as 3 | **FAIL**: no seat (Correction 1) | `frame_upper.member_length_rail` 1225 mm DERIVED (= `jackscrew.top_guide_z` + `profile.height`; foot on the rail top z_A 0 in `base.column_notch`); `frame_upper.foot` "a, b on the plate top over the end members; c on the rail top through base.column_notch" ASSUMED |
| 5 | Member orientation | text only at l.140 | **FAIL**: no leaf | `frame_upper.orientation` "one 60 face toward the axis" ASSUMED (Designer M1 r2 F2) |
| 6 | T8 screws (three) | `jackscrew.*` | PASS | none |
| 7 | Nuts with flange | `jackscrew.nut_*` | PASS | none |
| 8 | Anchor and top-guide blocks | r 21 by declaration (LF1.1-9) from `jackscrew.nut_flange_od` | PASS (stand-in, T2-b, S3) | none |
| 9 | Bracket arms (anchor below, guide above; one plan footprint per screw) | `jackscrew.pitch_radius`, `.nut_flange_od`, `frame_upper.radius`, `profile.width` | PASS | none |
| 10 | Descent stop | `frame_upper.stop_pad_*`, `stop.pad_*` | **FAIL**: one pad (Correction 6) | `frame_upper.stop_pad_count` 3 ASSUMED, one pad on each anchor arm at `jackscrew.angle[k]`, r 200 to 215 |
| 11 | Ring plate, OD 420, bore 200 | `ring.od`, `.thickness`, `.clearance_bore`, `.material_form` | PASS | none |
| 12 | Nut housings (three) | `ring.nut_housing_*` | PASS | none |
| 13 | Motor mounts (three) | `ring.motor_mount_*` | PASS | none |
| 14 | Clearance bore over gear and keep-out | `ring.clearance_bore` 200 | PASS | none |
| 15 | Drill-to-ring bearing | `bearing.*` | PASS | none |
| 16 | Gear with hub | `gear.*` | PASS | none |
| 17 | Bevel pinions (three) | `pinion.*` | PASS | none |
| 18 | NEMA 23 with shaft (three) | `pinion.motor_*` | PASS | none |
| 19 | Guide rods (H4 position) | `guide.*` | PASS: 0 and 180 deg, r 230 confirmed (section 4) | none |
| 20 | Guide bushings (S2-d) | `ring.guide_interface` text only | **FAIL**: no bushing leaves | `guide.bushing_type` "LM20UU in a housing block under the lug" ASSUMED; `guide.bushing_od` 32 ASSUMED; `guide.bushing_length` 42 ASSUMED; `guide.bushing_housing_od` 40 DERIVED (= 2 x `ring.guide_lug_half_width`); `guide.bushing_drop` 30 DERIVED (= length - `ring.thickness`) |
| 21 | Guide rod top support | none | **FAIL**: a 20 mm rod 1200 tall is free at the top | `guide.top_support` "tie from each rod top (z_A 1212) to the nearest screw frame member: rod 0 to member theta 30, rod 180 to member theta 150; 30-6060 stand-in; Step 2 decides" ASSUMED |
| 22 | Lift motors (H4) | `liftmotor.*` | **FAIL**: plan orientation undeclared | `liftmotor.position` text "coaxial under the anchor block at (jackscrew.pitch_radius, jackscrew.angle[k]), coupling up to the screw bottom"; `liftmotor.plan_rot` 0 deg (faces radial and tangential about the screw azimuth) ASSUMED |
| 23 | Drill tube | `drill.tube_od`, `.tube_id` | PASS | none |
| 24 | Keep-out | `icd.keepout_radius` 86.2 | PASS (overhang reported, section 7) | none |
| 25 | Cutter | `drill.head_od` 177.8 ASSUMED (Q2) | PASS | none |
| 26 | Collet axis (datum B, origin) | `icd.datum_b` | PASS | none |
| 27 | Slot lines | `icd.datum_c`, `icd.mounting_pattern`, `profile.slot_pitch` | PASS | slot line y DERIVED: rail centre +- `profile.slot_pitch` / 2 = +-259, +-289; slot line C at y +259 (`base.key_pocket_xy`) |
| 28 | Operator sector and sightline | none | **FAIL**: no keys | `operator.*`, section 9 |

Count: 21 PASS, 7 FAIL. `ring.*` functional features (rows 11 to 15, 20): PASS apart from the bushing leaves, which sit under `guide.*`.

## 2. O1 / S2-e: motor in the operator sector

Fixed parts at each screw azimuth subtend +-10.69 deg (lift motor circumscribing r 29.70 at r 160; arms +-9.41, housing +-8.99, pad +-8.53, member +-7.0 at R 274). The free arc between screws 30 and 150 is 40.69 to 139.31 deg (98.6 deg). A NEMA 23 subtends +-11.35 deg, a pinion +-25.6 deg.

A motor coaxial with a screw is impossible: the screw (r 160) passes through the motor body (r 142 to 218).

| Option | Values | Keys moved (S1 r5?) | Sector achieved | Hazard left | Cost |
|---|---|---|---|---|---|
| **O1-A** phase change: pinion = screw + 30 | `pinion.angle` [60, 180, 300]; `guide.angle` [225, 345] (rods at 180 sit 2.00 from the theta 180 motor, under G 10) | `pinion.angle`, `guide.angle`: **yes, S1 r5** (pinion, motor, mount, shaft, axis rows; guide rods and lugs; S1 projections of all of them) | theta 105.3, half-angle 30 (60 deg), free of motors (least 9.98) and fixed parts (least 10.90, lift motor 150). The theta 60 pinion still enters it | none new | Least plan gaps at Delta 30: motor to guide arm 36.02, to block 30.61, pinion to screw 30.38, pinion to nut housing 9.38 (same body). Delta below 22 fails motor to guide arm G 10 (11.49 at 22, 5.21 at 20); below 28 the pinion overlaps the housing in plan, z overlap 2.62. Rods lose their diametral pair. The sector is 30 deg narrower than O1-B |
| **O1-B** keep phase 60; S2-5 split into S2-5a (fixed parts, all z, K7 F) and S2-5b (premise check: ring-mounted parts in the sector stay above the hand band at load) | `operator.*` (section 9) only | **none; S1 stays r4** | theta 90, half-angle 45 (90 deg), r 400, free of every fixed part (least 11.71, lift motors 30 and 150) | NEMA 23 at theta 90 overhead at load, z_S 1185.34 to 1242.34, r 142 to 218. The ring disc (r <= 210, z_S 1136.84 to 1161.84 with the bearing) overhangs every sector. The motor raises that overhead band by 80.5 over a +-11.35 deg arc and reaches 8 past the rim | Relaxed rule: ships with its premise check (section 5) under detail 1 common (h). The guard covers the motor strike (T2-d) together with the gear-in-sector guard already in the watch row |
| O1-C reworded S2-5 with z band only, no fixed/moving split | none | none | as O1-B | as O1-B | Rejected: a z band applied to fixed parts would pass a screw or member inside the sector, which spans every height |

**Recommendation: O1-B.** The ring rim at 1.14 to 1.16 m z_S is the overhead obstacle in every sector, with or without a motor. O1-A buys a motor-free sector by narrowing it to 60 deg, moving two S1 keys and breaking the diametral guide pair. The loading sector sits at theta 90, the only screw gap with no guide rod (+Y side, at the datum C rail).

## 3. S2-c: theta 270 member overhang

Hand values (DERIVED): plate edge `icd.footprint_y` / 2 = 304. A square member, one face toward the axis, has its outer face at R + `profile.width` / 2 = R + 30 on the theta 270 bisector, so R + 30 <= 304 gives R <= 274. The theta 30 and 150 members' x extent at R 274 is 196.31 to 278.27, inside 322. Lower bounds: ring rim 210 + G 10 + 30 gives R >= 250; the arm must carry the pad, R - 30 >= 215, so R >= 245; motors (corner radius 219.86) are 60 deg off every member, and the motor to member gap is 147.15 at R 250.

| Option | Values | S1 rows that move | Other consequences |
|---|---|---|---|
| **S2-c-1** radius 274 | `frame_upper.radius` 300 to 274; new `frame_upper.member_length_rail` 1225, `frame_upper.foot` | frame_upper_a/_b: x centre +-259.81 to +-237.29, plan footprint r 244 to 304, side-view depth band y 109.02..190.98 to 96.02..177.98; bracket_anchor_a/_b, bracket_guide_a/_b r_out 270 to 244 (89 to 63 long); shape strings naming "r 270" and the "r 300" label; every K7 pair with these rows; operator row "r >= 330". `frame_upper.member_length` 1213 unchanged. Pad and post unchanged (r 200 to 215 on a 244 arm) | **S1 r5.** Member c stands on the rail top in the column notch, the seat Quinn's column used. Members a, b stand on the plate over the end members (x 202 to 262). Gaps at 274: member to ring rim 34.00, to guide lug 76.02, to guide rod 86.09, to nearest motor 167.81 |
| S2-c-2 wider plate | new overlay key for the plate width (K2 refuses `icd.footprint_y` in the overlay); plate >= 660 or -Y side +26 | S1 base_plate depth band (reads `icd.footprint_y`) and its K7 pairs; S1 and S2 spec key lists | **S1 r5.** The plate overhangs the rails by 26 with no frame under it. The theta 270 member still lands over the notch void (y -304 to -270), so the plate change does not seat it without also changing `base.column_notch`. Both are Quinn's kept base parts (frame rails and end members 488, plate) |
| S2-c-3 screw phase change | `jackscrew.angle` psi + 120k; R_max 292 at psi 0 or 60 | every S1 projection: screws, nuts, housings, blocks, arms, members, pad, lift motors; pinions too if the 60 deg phase is kept | **S1 r5.** Does not reach R 300 (Correction 3). At psi 0 and R 292 the theta 0 member stands at x 262 to 322, outboard of the end member, on 60 of unsupported plate |

**Recommendation: S2-c-1, radius 274, member c on the rail top through the column notch.** It is the only option that gives all three members a seat on frame metal. It moves one S1 key.

## 4. Phase, guides, lift motor, bushing

- Screw-to-pinion phase: **60 deg** (pinion = screw + 60 mod 120; screws 30, 150, 270; pinions 90, 210, 330). `pinion.angle` source text becomes "phase 60 deg from the screws, Designer 1.2 (a), Sean STOP S2-A"; value unchanged. (O1-A gives 30 deg instead.)
- Guide members, option drawn (N2): **two round rods, r 230, at 0 and 180 deg** (sectors centred 330 and 210; loading sector 90 kept clear), with LM20UU bushings and top ties (rows 20, 21). The rods clear the plate features: the rod at 0 is 14 in x from the stop-pin pocket wall (x 244, underside); the rod at 180 is 35 from the drain hole edge. Alternative Sean may pick at M2: **profile rail on the inner face of each screw frame member** (r 244), with the carriage on a ring lug at the screw azimuth. The ring stays between the arms over the whole stroke: ring top at park 1101.84 against the guide-arm bottom 1135 (33.16), and ring bottom at capture_end 314.84 against the anchor-arm top 295 (19.84). It frees the 210 and 330 sectors and puts anti-rotation on the members that carry the axial loop (Design Notes 11). It moves `guide.angle` and `guide.radius` (S1 keys), so S1 would reopen. M2 pick.
- Lift motor plan position (H4): coaxial with each screw under the anchor block at (160, `jackscrew.angle[k]`), 42 square with faces radial and tangential (`liftmotor.plan_rot` 0). Its plan footprint lies inside the arm strip and block circle. S1 keeps the circumscribing r 29.70 footprint (admitted for F and G).
- Guide bushing (S2-d): LM20UU (OD 32, length 42) in a housing block OD 40 under the lug, hanging 30 below the ring underside (to 284.84 z_A at capture_end). In plan the housing coincides with the lug footprint (r 210 to 250, half-width 20). Rod in bushing: class N, declared. No S1 key moves; S1 r5 adds the housing as a row, or a `not_drawn` entry if r5 does not open.

## 5. S2-5 sector rule (O1-B)

| Field | Value |
|---|---|
| apex | on the axis (datum B) |
| azimuth | `operator.sector_theta` 90 deg (+Y side) |
| half-angle | `operator.sector_half_angle` 45 deg |
| radius | `operator.sector_radius` 400 |
| hand band | `operator.hand_band` [440, 940] z_A (0.5 to 1.0 m z_S, from the load row) |

- **S2-5a** (all z, K7 F on plan footprints, circumscribing footprints admitted): the sector is free of every fixed part: screws, blocks, bracket arms, lift motors, frame members, descent-stop pads and posts, guide rods and top ties. Z: the live layout, least 11.71 (lift motors 30 and 150), then housings 16.41, arms 17.87, pads 22.8. B1: sector widened to 130 deg (half 65), which fires on arms, blocks, lift motors, members and housings at 30 and 150 (gameplan B unchanged). At half-angle 49 the least gap is 0.84, so 45 holds 4.31 deg either side.
- **S2-5b** (premise of the relief that lets ring-mounted parts sit in the sector; detail 1 common (h); I raise and sign it): at load, every ring-mounted part whose plan footprint enters the sector (ring plate, bearing, gear, motor mount, pinion and NEMA 23 at theta 90) has its lowest z at least g 10 above the hand-band top. Value: bearing bottom 1076.84 z_A against 940, margin 136.84 (DERIVED). Z: the live layout. B2: NEMA 23 at theta 90 drawn at load with its bottom at 930 z_A, which fires. Reported, not asserted: the overhead strike list in the sector at load (bearing 1136.84, ring 1149.84 to 1161.84, pinion 1168.22 to 1259.46, motor 1185.34 to 1242.34, gear to 1275.84 z_S), and the drill tip 1019.84 z_S, 19.84 above the band top (the part the operator loads under).
- Under O1-A instead: one rule S2-5 with sector theta 105.3, half-angle 30, free of fixed parts and motors (least 9.98); B: widened to half-angle 33 (motor 2.40, lift motor 2.75; widen further to fire); no S2-5b.

## 6. S2-b sightline row (F6)

| Field | Value |
|---|---|
| id | `sightline_f6` |
| kind, projection | line, line |
| poses | [capture_end] |
| from | observer at r `operator.watch_r` 400, theta `operator.watch_theta` 60 (between screw 30 and motor 90, 30 deg from each), eye `operator.eye_height` 1540 z_A (1.6 m z_S, standing) |
| to | the cut at the axis, z_S 244.84 |
| draw | solid r 400 to 210, dashed r 210 to 0 ("hidden by the ring at capture_end") |
| label | "F6 sightline, eye 1.6 m at r 400: ring rim r 210 hides the cut at capture_end; eye limit 0.49 m (axis), 0.58 m (cutter rim r 88.9)" |
| keys | `operator.watch_r`, `operator.watch_theta`, `operator.eye_height`, `ring.od`, `ring.position_above_tip`, `drill.head_od` |
| neighbours | none (line) |

Hand values (DERIVED): ring underside at capture_end 374.84 z_S, cut at 244.84. Limit slope to the axis is 130 / 210 = 0.619, so the eye must be at or below 244.84 + 0.619 x 400 = 492.46 at r 400. To the cutter rim the slope is 130 / 121.1 = 1.0735, giving 578.80. A 1.6 m eye at r 400 crosses the ring-top plane at r 62.9, inside the clearance bore, where the bearing, gear and tube block it. A sight window in the ring plate on this azimuth would not open the view. T2-a (camera or stop indicator) stays the route.

## 7. S2-a keep-out pairs and cutter overhang

| Pair (plan) | Class | g_min | Clearance over 86.2 | Over cutter r 88.9 |
|---|---|---|---|---|
| lift motors (circumscribing r 29.70; z_A 192 to 240, inside the head's band at capture_end 184.84 to 291.21) | G | 0 | 44.10 | 41.40 |
| anchor and guide blocks (r 139) | G | 0 | 52.80 | 50.10 |
| screw rods (r 156) | G | 0 | 69.80 | 67.10 |
| descent-stop pads (r 200) | G | 0 | 113.80 | 111.10 |
| guide rods (r 220) | G | 0 | 133.80 | 131.10 |
| frame members (r 244 at R 274) | G | 0 | 157.80 | 155.10 |
| base parts below the lowest tip (collet, holder, collar r 76.2, wing-nut sweep r 115) | plan overlap admitted, z-separated | stop.g_stop 25 in z (S1 drill_head\|collar 25.000, S1-5b) | n/a | n/a |
| ring-mounted parts (gear bore r 90, ring bore r 100, pinion r_in 95.22, bearing) | move with the drill; no sweep relative to it | reported | 3.80, 13.80, 9.02 | n/a |

S2-2 check value: 160 - 21 - 86.2 = 52.80 >= 10.

Cutter overhang (reported, never asserted): `drill.head_od` / 2 - `icd.keepout_radius` = 88.90 - 86.20 = **2.70** (DERIVED; head OD ASSUMED, Q2). It feeds the Step 4 ICD row `icd.keepout_radius`: the row either becomes max(`drill.tube_od`, `drill.head_od`) / 2 + `drill.r_face_margin` (98.9 if Q2 confirms 177.8; S2-2 then reads 40.10, still >= 10), or keeps 86.2 for the tube and adds a head keep-out radius over the head z band.

## 8. Shape notes (8.4b), S2 plan

| Part id | shape |
|---|---|
| base_plate | "aluminium base plate 644 x 608 x 12 seen from above: rectangle with the receiver spigot hole 160.4 at the centre, a 70 x 65 column notch at x 0 on each long edge, slotted fastener holes along both long edges; underside key and pin pockets dashed" |
| base_frame | "30-6060 base frame under the plate, dashed: two rails along X at y +-274, end members at x +-232, plate supports at x +-112" |
| slot_line_c | "slot line C: chain line along +X at y +259 on the +Y rail, labelled +X; the other rail slot lines thin" |
| frame_upper_a, _b | "screw frame member, 30-6060 seen end-on: 60 x 60 square, one face toward the axis, at frame_upper.radius on the screw azimuth, on the plate top over the end member" |
| frame_upper_c | "screw frame member, 30-6060 end-on, 60 x 60 square on the rail top inside the column notch at theta 270; plate notch outline drawn around it" |
| screw_a, _b, _c | "T8 lead screw seen end-on: circle d 8 at the pitch radius, inside its nut flange circle d 42 and nut-housing boss d 50" |
| bracket_a, _b, _c | "anchor and top-guide bracket arms (same plan footprint): radial 60-wide strip from the block face r 181 to the member face, with the block circle r 21 at the screw" |
| descent_stop_a, _b, _c | "metal descent-stop pad, radial r 200 to 215 x 60 on each anchor arm, metal hatch, under the ring rim" |
| liftmotor_a, _b, _c | "NEMA 17 lift motor under the anchor block, 42 square, faces radial and tangential, centred on the screw; dashed (below the block)" |
| ring | "ring plate seen from above: disc OD 420 with the 200 clearance bore, carrying three nut-housing bosses, three NEMA 23 mounts and two guide lugs; reads as a structure, not a washer" |
| nut_housing_a, _b, _c | "nut-housing boss d 50 on the ring at each screw, concentric with the nut flange" |
| motor_mount_a, _b, _c | "NEMA 23 mount block on the ring top, 57 wide, r 142 to 210 on the pinion azimuth" |
| guide_lug_a, _b | "guide lug, ring rim to r 250, 40 wide, with the LM20UU housing d 40 below it (dashed) round the rod" |
| bearing | "drill-to-ring bearing, annulus r 76.2 to 100 in the clearance bore, dashed under the gear" |
| gear | "bevel ring gear seen from above: annulus r 90 to 126.32 with tooth ticks on the OD, clamp hub on the tube" |
| pinion_a, _b, _c | "bevel pinion on a radial shaft: toothed trapezoid r 95.2 to 125 narrowing toward the axis, hub to r 140, axis drawn as a radial chain line through the motor" |
| motor_a, _b, _c | "NEMA 23 seen from above: 57 x 76 body outboard of the pinion, r 142 to 218, shaft d 8 inboard to the pinion; motor outboard, pinion inboard" |
| guide_member_a, _b | "ring guide rod d 20 seen end-on at r 230, inside the lug bushing" |
| guide_tie_a, _b | "rod top tie, 30-6060 stand-in from the rod top to the nearest screw frame member, dashed, labelled Step 2" |
| drill_tube | "drill tube seen end-on: annulus OD 152.4 / ID 146.05" |
| keepout | "keep-out circle r 86.2, dashed, labelled keep-out" |
| drill_head | "cutter rim circle r 88.9 (ASSUMED, Q2), dotted, 2.70 outside the keep-out, labelled cutter OD ASSUMED" |
| collet_axis | "datum B: cross at the origin with +X and +Y arrows and the theta sense arrow counter-clockwise" |
| operator_sector | "operator loading sector: 90 deg wedge from the axis to r 400 centred on theta 90, light fill, labelled load and collet change" |
| sightline_f6 | "F6 sightline at theta 60 from the observer at r 400 to the axis, solid outside the ring rim, dashed inside" |

Part list for (b): every part these strings name has a row above, except the wing nut, collet and holder (below the drill path, drawn in S1; `not_drawn` in S2 with that reason) and the hold device (Step 2, `not_drawn`).

## 9. Overlay value table

| Key | Old | New | Unit | Source | Status | S1 key |
|---|---|---|---|---|---|---|
| `frame_upper.radius` | 300 | 274 (S2-c-1) | mm | Designer 1.2 (a): plate edge 304 - profile.width / 2; centred on the rail; Sean STOP S2-A | ASSUMED | **yes** |
| `frame_upper.member_length_rail` | none | 1225 | mm | jackscrew.top_guide_z 1165 + profile.height 60; member c foot on the rail top (z_A 0) in base.column_notch | DERIVED | no |
| `frame_upper.foot` | none | "a, b on the plate top over the end members; c on the rail top through base.column_notch" | | Designer 1.2 (a) | ASSUMED | no |
| `frame_upper.orientation` | none | "one 60 face toward the axis" | | Designer M1 r2 F2; gameplan l.140 | ASSUMED | no |
| `frame_upper.stop_pad_count` | none | 3 | | one pad on each anchor arm; Designer 1.2 (a) | ASSUMED | no (S1 r5 adds the pad at theta 30) |
| `pinion.angle` | [90, 210, 330] | unchanged (O1-B); [60, 180, 300] under O1-A | deg | source text: "phase 60 deg from the screws, Designer 1.2 (a), Sean STOP S2-A" | ASSUMED | yes (value moves only under O1-A) |
| `guide.angle` | [0, 180] | unchanged (O1-B); [225, 345] under O1-A | deg | source text: "S2 places them in the sectors centred 330 and 210; loading sector 90 clear" | ASSUMED | yes (value moves only under O1-A) |
| `guide.bushing_type` | none | "LM20UU in a housing block under the lug" | | catalogue class; Designer 1.2 (a) S2-d | ASSUMED | no |
| `guide.bushing_od` | none | 32 | mm | LM20UU class | ASSUMED | no |
| `guide.bushing_length` | none | 42 | mm | LM20UU class | ASSUMED | no |
| `guide.bushing_housing_od` | none | 40 | mm | 2 x ring.guide_lug_half_width | DERIVED | no |
| `guide.bushing_drop` | none | 30 | mm | guide.bushing_length - ring.thickness | DERIVED | no |
| `guide.top_support` | none | text, row 21 | | Designer 1.2 (a); Step 2 decides | ASSUMED | no |
| `liftmotor.position` | placeholder text | text, row 22 | | Designer 1.2 (a), H4 | ASSUMED | no (not in keys_read) |
| `liftmotor.plan_rot` | none | 0 | deg | faces radial and tangential about the screw azimuth; S3 confirms | ASSUMED | no |
| `operator.sector_theta` | none | 90 | deg | Designer 1.2 (a): screw gap with no guide rod | ASSUMED | no |
| `operator.sector_half_angle` | none | 45 | deg | Designer 1.2 (a); 4.31 deg each side to the screw-azimuth parts | ASSUMED | no |
| `operator.sector_radius` | none | 400 | mm | stance radius, load and watch rows | ASSUMED | no |
| `operator.hand_band` | none | [440, 940] | mm z_A | 0.5 to 1.0 m z_S, load row | ASSUMED | no |
| `operator.watch_r` | none | 400 | mm | watch row | ASSUMED | no |
| `operator.watch_theta` | none | 60 | deg | between screw 30 and motor 90 | ASSUMED | no |
| `operator.eye_height` | none | 1540 | mm z_A | 1.6 m z_S, standing adult | ASSUMED | no |

`operator` is not a params.yaml namespace (checked; `access` is, and is not used).

## 10. g_min for the K7 pairs S2 uses

| Pair (plan) | Class | g_min | Value at proposed values | Seed (l.147-152) |
|---|---|---|---|---|
| fixed parts vs keep-out 86.2 | G | 0 | least 44.10 (lift motor) | confirmed |
| moving ring parts vs fixed members, arms, lift motors, rods, ties (swept z) | G | 10 | ring rim to member 34.00; lug to member 76.02; motor to rod 76.50 | confirmed |
| ring rim vs descent-stop pads | C at capture_end | 0 | S1 value | unchanged |
| nut housing vs pad | G at capture_end | 10 | 15.00 | unchanged |
| guide rod vs guide-lug bushing | N | declared | rod in bushing | new for S2 |
| operator sector vs fixed parts (S2-5a) | F | 0.05 | 11.71 | changed: fixed parts at all z; motors moved to S2-5b |
| ring-mounted parts in sector vs hand band top (S2-5b) | G in z at load | 10 | 136.84 | new (premise) |
| screws vs keep-out (S2-2) | G | 10 | 52.80 | confirmed |
| member foot vs seat (plate outline less notches, or notch over the rail) | contained | 0 | members a, b on the plate; c in the notch, 5 clear | new, proposed S2-6 |

## 11. Operator-task rows (S2, on the proposed values; z_S)

| Task | Pose | Stance and reach in plan | Sector | Sightline | Hazard |
|---|---|---|---|---|---|
| Lift a 0.75 m core into the collet | load | Stand at the +Y plate edge (y 304) on theta 90, torso at r >= 304, arms through the sector to the axis, about 330 reach; hands 0.5 to 1.0 m | theta 90 +- 45, r 400; fixed parts >= 11.71 outside it; opening 256 between the sector edges at r 181 | down into the holder bore from theta 90 | 15.6 kg at about 330 out (Step 2 loading aid). Overhead in the sector: bearing 1136.84, ring 1149.84 to 1161.84, NEMA 23 at theta 90 1185.34 to 1242.34, r to 218: head strike when leaning in (Step 2 guard, T2-d) |
| Change a collet | load | Kneel at theta 90, hands at r <= 115, reach about 190 from r 304 | as above | wing nut from theta 90 at knee height | Either side, outside the sector edge: lift motors 252 to 300 (11.71), anchor arms 325 to 355 r 181 to 244 (17.87), pads at 30 and 150 362.84 to 374.84 (22.8). Drill tip overhead at 1019.84 |
| Stand and watch a cut | start to capture_end | Stand at r 400, theta 60, eye 1.6 m | outside the frame | at start the cutter is in view under the ring; at capture_end the cut is hidden (limit 0.49 m to the axis, 0.58 m to the cutter rim at r 400) | Gear and pinions turn at 60 rpm and the gear passes through the open sector (Step 2 guard or interlock); end of cut by camera or stop indicator (T2-a) |

## 12. Items for Sean

**At STOP S2-A (block (b)):**

1. **S2-c**, pick one:
   - **S2-c-1, recommended:** `frame_upper.radius` 300 to 274; member c on the rail top through `base.column_notch` (new `member_length_rail` 1225). S1 r5: frame_upper_a/_b move in x from +-259.81 to +-237.29; the four bracket arms shorten from 89 to 63 (r_out 270 to 244); shape text and the "r 300" label change; K7 pairs on these rows are re-run. Member length 1213 is unchanged.
   - **S2-c-2:** a wider plate behind a new overlay key. S1 r5 (base plate depth band, spec key lists). The plate overhangs the frame by 26, and member c still sits over the notch void, so Quinn's plate, notch and frame change too.
   - **S2-c-3:** a screw phase change. It cannot reach R 300 (max 292). S1 r5 moves every screw-side projection.
2. **O1 / S2-e**, pick one:
   - **O1-B, recommended:** keep the 60 deg phase; S2-5a plus the S2-5b premise check; sector theta 90 +- 45. No S1 key moves. The motor strike goes to the Step 2 guard.
   - **O1-A:** phase 30, with `pinion.angle` [60, 180, 300] and `guide.angle` [225, 345]. S1 r5 (pinion and guide rows). Sector 60 deg, motor-free.
3. **Descent stop: three pads, one per anchor arm** (`frame_upper.stop_pad_count` 3). No S1 key value moves, but S1 gains a pad row at theta 30. It rides S1 r5 if item 1 or 2 opens it; otherwise it waits for M2 with a `not_drawn` note in S1.
4. Other S1 keys: none. Under the recommended picks, `frame_upper.radius` is the only S1 key that moves. Sources change on `pinion.angle` and `guide.angle`; their values do not.

**Can wait for M2:** N2 guide option (rods drawn; rails on the members as the alternative, which would move `guide.angle` and `guide.radius`); guide bushing form and top tie; sightline azimuth (60); lift-motor plan orientation; the S2-6 seat check wording.

## 13. Echo sites S2 creates

| Value | Authority | Derived locations |
|---|---|---|
| Screw frame radius 274 (on pick) | overlay `frame_upper.radius` | S1 r5 member and arm rows and label; S2 member, arm, tie rows; K7 plan pairs (LF-8); load row "torso r >= 304" |
| Member c seat: rail top in the column notch, length 1225 | overlay `frame_upper.member_length_rail`, `frame_upper.foot`; params `base.column_notch` | S2 frame_upper_c row; S2-6; Step 2 frame row; Quinn (notch is his base feature) |
| Screw-to-pinion phase 60 deg | overlay `pinion.angle`, `jackscrew.angle` | S2-1; `ring.motor_mount_placement` text; S1 pinion rows |
| Operator sector theta 90 +- 45, r 400 | overlay `operator.sector_*` | S2-5a Z fixture; operator rows; V10; Step 2 guard row |
| Hand band 0.5 to 1.0 m z_S | overlay `operator.hand_band` | S2-5b; load row |
| Watch position r 400, theta 60, eye 1.6 m; eye limits 0.49 / 0.58 m | overlay `operator.watch_*`, `operator.eye_height` | sightline_f6 row and label; watch row; T2-a |
| Cutter overhang 2.70 | reported (`drill.head_od`, `icd.keepout_radius`) | S2 summary; Step 4 ICD row; S1 F7 |
| Descent-stop pads, 3 | overlay `frame_upper.stop_pad_count` | S1 r5 pad rows; S2 pad rows; collet-change row |
| Guide bushing LM20UU 32 x 42 in an OD 40 housing, 30 below the ring | overlay `guide.bushing_*`, `ring.guide_lug_half_width` | S2 lug rows; S1 r5 housing row or `not_drawn`; S6 |

## 14. Gameplan lines to change

1. l.152. Old: `- Operator loading sector against screws, motors and frame members (plan view): F.` New: `- Operator loading sector (S2-5a) against every fixed part at all z (screws, blocks, bracket arms, lift motors, frame members, descent-stop pads and posts, guide rods and top ties), plan view: F. Ring-mounted parts whose plan footprint enters the sector (S2-5b, premise of that relief): at load, lowest z at least 10 above the top of `operator.hand_band` (Designer 1.2 (a)).` (Under O1-A instead: `- Operator loading sector against screws, motors and frame members (plan view): F; sector theta 105.3, half-angle 30 (Designer 1.2 (a), O1-A).`)
2. l.256. Old: `| S2-5 | Operator sector (apex on the axis, half-angle and radius in the spec, set by The Designer) free of screws, motors and frame members (K7 F) | Fixture with a 90 deg sector between two screws | Sector widened to 130 deg, wider than the gap between two screws at 120 deg | sector ASSUMED |` New (O1-B): `| S2-5a | Operator sector (apex on the axis, theta 90, half-angle 45, r 400; overlay operator.*, The Designer) free in plan of every fixed part at all z (screws, blocks, arms, lift motors, frame members, pads and posts, guide rods and ties; K7 F) | Live layout: least 11.71 (lift motors 30 and 150) | Sector widened to 130 deg, wider than the gap between two screws at 120 deg | sector ASSUMED |` then the new line `| S2-5b | Premise of the S2-5a relief for ring-mounted parts: at load every ring-mounted part whose plan footprint enters the sector lies at least 10 above the top of operator.hand_band (940 z_A); least: bearing bottom 1076.84, margin 136.84 | Live layout | NEMA 23 at theta 90 drawn at load with its bottom at 930 z_A | hand band ASSUMED |` then the new line `| S2-6 | Member seats: frame members a, b lie inside the plate outline less base.column_notch; member c lies inside the notch over the rail (contained, 0.05) | Live layout at frame_upper.radius 274 | Member c at radius 300 (26 off the plate edge) | params base.*, overlay frame_upper.foot |`
3. l.245. Old: `ring guide members (N2: rails or rods, which may also be the anti-rotation member; option drawn, Sean picks at M2)` New: `ring guide members with bushings and top ties (N2: two rods at 0 and 180 deg drawn; alternative profile rails on the screw frame members; Sean picks at M2), three descent-stop pads, member seats (theta 270 member on the rail top in base.column_notch)`
4. l.180. Old: `Operator stands in the S2-5 sector between two screws, torso outside the frame members (r >= 330)` New: `Operator stands in the S2-5 sector (theta 90 +- 45, the screw gap with no guide rod), torso outside the frame members (r >= 304 at frame_upper.radius 274)`. Same line, old: `with the NEMA 23 in the sector at 1185.34 to 1242.34: chest and shoulder strike when leaning in` New: `with the NEMA 23 at theta 90 in the sector at 1185.34 to 1242.34 (r 142 to 218), above the ring rim that overhangs every sector at 1136.84 to 1161.84: head strike when leaning in (Step 2 guard; S2-5b keeps it above the hand band)`
5. l.181. Old: `anchor arms (325 to 355, r 160 to 270), descent-stop pad (363 to 375, theta 150, r 200 to 215)` New: `anchor arms (325 to 355, r 181 to 244), descent-stop pads (363 to 375, r 200 to 215, one per anchor arm)`
6. l.184. Old: `outside the frame (r >= 400), standing` New: `outside the frame at r 400, theta 60 (operator.watch_*), eye 1.6 m, standing`. Same line, old: `from any eye above about 0.49 m at r 400;` New: `from any eye above about 0.49 m at r 400 (0.58 m for the cutter rim r 88.9; S2 sightline_f6);`
7. Echo Site Registry, after l.664 insert: `| Screw frame radius **274 mm** (members a, b on the plate top; c on the rail top in the column notch, length 1225) | overlay frame_upper.radius, frame_upper.member_length_rail; params base.column_notch | ASSUMED (Designer 1.2 (a); Sean STOP S2-A) |` and `| Operator sector **theta 90 +- 45, r 400**; hand band 0.5 to 1.0 m z_S | overlay operator.* | ASSUMED (Designer 1.2 (a)) |` (both applied only after Sean's STOP S2-A picks; under S2-c-2 or -3 the first row carries the picked value).
