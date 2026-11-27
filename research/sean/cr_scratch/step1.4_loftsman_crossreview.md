# Step 1.4 P7a, The Loftsman: (e) geometry cross-review of S4 r1 and the S1 r9 changed rows

Verdict: **FIX 1** (a control, no geometry). Every hand value below matches the JSON or the summary to 0.01 mm. S3-3 dry run on the final S1 r9 record: 48 links, unchanged. X1 O2 (ii) is signed once FIX 1 is in.

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\open14\p7a\`. Leaf dump `leaves.py`. Tree copy `ws\` (params.yaml and docs/sketches). Accept and S3 logs `acc.txt` and `s3dry.txt`. FIX 1 dry run `x1_s1dry.txt`.

## Corrections to the brief

none

## 1 Leaves read (params.yaml, overlay; DECLARED)

seat.holder_bottom_R 13.626; holder.stroke_gap_R 13.126; witness.zone_high 8.59; holder.length 88.0; holder.flange_thickness 8; holder.flange_od 144.08; nut.plate_thickness 7.5; washer.thickness 1.3; nut.washer_pocket_depth 0.8; collar.top_above_plate 6.75; collar.thickness 6.0; collar.id 110.0; collar.od 152.4; nut.lift_play 0.75; icd.floor_above_datum_a 40; jig.datum_a_above_floor 60 (overlay); receiver.register_bore_radius 67.29; register.g_reg 0.25; chain.t_h 5; chain.H 30; cone.alpha 10; receiver.spigot_od 160; base.spigot_hole_dia 160.4; base.plate_thickness 12; receiver.shoulder_z 12 (overlay); thread.major 149.58; receiver.rim_above_floor 88.5; collet.core_stop_z 42.5 (overlay, ASSUMED); core.length_short 100 (overlay, ASSUMED); carrier.length 160 (overlay); core.min_exposed 143.12; stop.height_z 184.84; drill.kerf_standoff 106.369; drill.dome_pole_offset 34.9315; iris.face_radius_core 71.4375; stop.margin 5; core.length_install 750; nut.overall_height 56.0; nut.length 48; nut.plate_hole_dia 136.08; wingnut.body_od 166.28.

## 2 S4 r1 hand values against the code (z_A unless marked)

| Quantity | Hand (DERIVED) | Code / JSON (MEASURED) | Agree |
|---|---|---|---|
| holder drop | 13.126 - 8.59 = 4.536 | | |
| holder bottom | 40 + 13.626 - 4.536 = 49.09 | K7 and K6 pass on 49.09 (spec shape) | yes |
| nut plate (test_P18) | 7.5 + 1.3 - 0.8 = 8.00 | check_stack.collar_top_z_A | yes |
| collar top | 49.09 + 88 + 8 + 8 + 6.75 = 159.84; z_S 219.84 | S4-1 159.84 = stop.collar_top_z 159.84; drawn top equal in both figures; PNG title tip 244.84 z_S | yes |
| collar top by holder.py | 49.09 + z_top (88 + 8 + 0.5 + 7.5 + 0.75 = 104.75) + t_col 6 = 159.84 | | yes; the two formulas agree because 6.75 = 6.00 + 0.75 (NOTE 2) |
| spigot radial gap | 160.4 / 2 - 160 / 2 = 80.20 - 80.00 = 0.20 | K7 base_plate\|receiver_spigot 0.2; RPT cut_case_seat 0.20 | yes |
| shoulder seat | shoulder underside 12.00 on plate top 12.00 | K7 base_plate\|receiver C 0.0; RPT gap 0.00 | yes |
| collet foot seat | foot 40.00 on floor top 40 + 0 = 40.00 | RPT gap 0.00; K7 receiver\|collet C 0.0 | yes |
| holder cone piece | r 67.04 out (67.29 - 0.25); r 62.04 in at 49.09 to r 62.04 - 30 tan 10 = 62.04 - 5.290 = 56.75 at 79.09 | holder.py dims r_od, r_cone_bot, r_cone_top, H; spec shape | yes |
| holder tube | r 56.75 to 67.04, 79.09 to 137.09 | spec shape | yes |
| holder flange | r 56.75 to 72.04, 137.09 to 145.09 | spec shape; label 144.08 | yes |
| holder neck | r 56.75 to 67.04, 145.09 to 145.09 + 0.5 + 7.5 + 0.75 = 153.84 | stack tie offset collar.thickness: 159.84 - 6.00 = 153.84; K6 pass | yes |
| collar ring | r 55.00 to 76.20, 153.84 to 159.84 | spec shape | yes |
| collet cone on holder cone | collet outer at 49.09: 63.791 - 0.5 - (49.09 - 41.995) tan 10 = 62.040; holder inner 62.04; both slope tan 10 | K7 collet\|holder C 0.0 | yes, line contact 49.09 to 72.00 (22.91) |
| grip d 100 | room 63.79 - 30 tan 10 - 51 - 1.2 = 6.30; chamfer start 72 - 6.30 = 65.70; grip 65.70 - 42.50 = 23.20 | RPT grip 23.20 (42.50 to 65.70) | yes |
| grip d 105 | room 63.79 - 5.29 - 53.5 - 1.2 = 3.80 (outside the 2.5 to 3.5 band); start 68.20; grip 25.70 | RPT 25.70 | yes |
| wing nut | bottom 153.09 - 56 = 97.09; pocket floor 97.09 + 48 + 0.5 = 145.59; plate underside 146.39; plate top 153.09 | spec shape; K7 pairs below | yes |
| washer | 145.09 to 146.39, r 68.40 to 71.60 in the pocket r 68.04 to 71.90 | K7 holder\|washer C 0.0, wingnut\|washer C 0.0 | yes |
| nut-plate top | 159.84 - 6.75 = 153.09 | S4-2 exposure datum | yes |
| 100 mm core top on the stop | 42.50 + 100 = 142.50; offset to the collar top 159.84 - 142.50 = 17.34 below | RPT q10_core_top 142.50, 17.34 | yes |
| 100 mm core top on the carrier | 42.50 + 160 + 100 = 302.50; z_S 362.50 | RPT 302.50 (drawn); PNG top at z_S 362.5 | yes |
| exposure on the carrier | 302.50 - 153.09 = 149.41; margin 149.41 - 143.12 = 6.29 | S4-2 6.29; RPT 149.41 | yes |
| exposure on the stop | 142.50 - 153.09 = -10.59 | RPT -10.59 | yes (DERIVED value in a row tagged MEASURED, NOTE 3) |
| min core top | 153.09 + 143.12 = 296.21; check 184.84 + 106.369 + 5 = 296.209 | line_min_core 296.21; line_kerf 291.21 | yes |
| min core on the stop | 296.21 - 42.50 = 253.71; collar datum 159.84 + 143.12 - 42.50 = 260.46 | RPT q10_min_on_stop 253.71, 260.46 | yes |
| min core on the carrier | 296.21 - 202.50 = 93.71 | RPT 93.71 | yes |
| seat bearing | carrier r 50.50 on ledge r 47.50 to 50.50: 3.00; d 105 ledge r 50.00 to 53.00: carrier 0.50, liner 2.50; 1287.05 / (pi (50.5^2 - 50^2) = 157.86) = 8.15 MPa | RPT 3.00, 0.50, 2.50, 8.15 | yes |

### Advance path, drawn option D (the lift lowers the drill; the core stays put)

| Quantity | Hand (DERIVED) | RPT | Agree |
|---|---|---|---|
| kerf centre at the stop | 184.84 + 106.369 = 291.209 | 291.21 | yes |
| dome pole | 184.84 + 34.9315 = 219.772 | | |
| sphere at r 50 | 291.209 - sqrt(71.4375^2 - 50^2) = 291.209 - 51.023 = 240.186 | | |
| least slice | axis 296.209 - 219.772 = 76.44; r 50: 296.209 - 240.186 = 56.02 | 76.44, 56.02 | yes |
| 0.75 m core | tip span 42.50 + 750 - 296.209 = 496.29; first tip 792.50 - 111.369 = 681.13; cuts floor(496.29 / 76.44) + 1 = 6 + 1 = 7; removed 792.50 - 219.772 = 572.73 | 496.29, 681.13, 7, 572.73 | yes |
| stub on the stop | 219.772 - 42.50 = 177.27 axis; 240.186 - 42.50 = 197.69 surface | 177.27, 197.69 | yes |
| stub moved onto the carrier | top 202.50 + 177.27 = 379.77; exposure 379.77 - 153.09 = 226.68; cuts floor(83.56 / 76.44) + 1 = 2; removed 379.77 - 219.77 = 160.00 | 379.77, 226.68, 2, 160.00 | yes |
| 100 mm core on the carrier | 302.50 >= 296.21: 1 cut; stub 219.77 - 202.50 = 17.27 axis, 240.19 - 202.50 = 37.69 surface | 17.27, 37.69 | yes |
| clearance at the end of the path | drill tip 184.84 - collar top 159.84 = 25.00 (stop.g_stop; zero margin at g_min 25, a design identity) | K7 drill_head\|collar 25.0 in both figures and swept carrier..liner 25.0 | yes |
| other kept parts under the head | holder top 184.84 - 153.84 = 31.00; nut plate 184.84 - 153.09 = 31.75; washer 184.84 - 146.39 = 38.45 | K7 undeclared F 31.0, 31.75, 38.45 | yes |
| core passage radial | holder bore 56.75 - 50.50 = 6.25; collar ID 55.00 - 50.50 = 4.50; plate hole 68.04 - 50.50 = 17.54 | K7 6.25, 4.5, 17.54 | yes |

### One K7 pair per class (S4, pose carrier)

| Class | Pair | Hand | JSON |
|---|---|---|---|
| C | base_plate\|receiver | shoulder underside 12.00 on plate top 12.00, annulus r 80.20 to 100.00 | C, distance 0.0, overlap 0.0 |
| C one_body | holder\|collar | neck top 153.84 = ring underside 153.84; faces overlap r 56.75 to 67.04 | C, 0.0, 0.0 |
| G | holder\|wingnut | flange top 145.09 to pocket floor 145.59 = 0.50; radial neck to plate hole 1.00; flange to body 74.79 - 72.04 = 2.75; least 0.50 = g_min (zero margin) | 0.5 |
| G | collar\|wingnut | ring underside 153.84 - plate top 153.09 = 0.75 = nut.lift_play = g_min (zero margin) | 0.75 |
| G | collar\|core_100 | corner (50.50, 202.50) to (55.00, 159.84): sqrt(4.50^2 + 42.66^2) = 42.897 | 42.897 |
| N | carrier\|drill_head | declared (the second cut runs into the carrier) | N, declared |
| undeclared F | receiver\|carrier | carrier bottom 42.50 - floor top 40.00 = 2.50 | 2.5 |
| swept F | drill_head\|collar | 25.00 at both figures, tip fixed at the stop | 25.0 |
| G (liner) | holder\|liner | 56.75 - 53.00 = 3.75 | 3.75 |

## 3 S1 r9 changed rows

| Item | Hand (DERIVED) | s1_checks_r9.json (MEASURED) | Agree |
|---|---|---|---|
| holder placement | z_S 49.09 + 60 = 109.09 to 153.84 + 60 = 213.84; pieces as section 2 (X1 equal to s4) | K6 239 z_rules within 0.05; X1 section_true equal on 7 rows | yes |
| holder z_max edit | old 145.09 (flange top) to new 153.84 (tube top): +8.75 = 0.5 + 7.5 + 0.75 | stack tie collar_top - collar.thickness = 153.84 | yes |
| collar z_min edit | old 159.84 - 6.75 = 153.09 to new 159.84 - 6.00 = 153.84 | K6 pass | yes |
| receiver\|holder G 0.25 | holder OD r 67.04 in register bore r 67.29: 0.25; flange underside 137.09 over the rim 128.50: 8.59 | G, 0.25 at load, start, capture_end, park | yes; zero margin at g_min 0.25 (register.g_reg, design identity) |
| collar\|holder C one_body | 153.84 against 153.84, faces r 56.75 to 67.04 | C, 0.0, overlap 0.0 in every pose | yes |
| receiver\|wingnut C | receiver thread piece r_out 149.58 / 2 = 74.79 = nut body r_in 74.79, z 97.09 to 127.25 | C, 0.0 | yes |
| holder\|wingnut G 0.50 | 0.50 as section 2 | 0.5 | yes |
| collar\|wingnut G 0.75 | 0.75 as section 2 | 0.75 | yes |
| S1-3 margins | load plane core_stop 42.50 and the pose rows are unchanged from r8 | 367.34, 117.34 | equal to r8 |
| S1-5b | rows above the base stack unchanged | 91 pairs, least 142.00 | unchanged |

## 4 S3-3 dry run on the final S1 r9

Run on the tree copy `ws\` after the last S1 edit (closes the Engineer's Correction 10 order).
- `check_sketch.py --accept s1 --rev 9` in the copy: exit 0; s1_checks_r8.json superseded_by 9.
- `check_sketch.py s3 --rev 8` in the copy: exit 0; **S3-3 pass, 48 links closed in the cut case** (MEASURED). The deps record names s1_checks_r9.json (rev 9, sha256 6bcea3ffee54) and s2_checks_r9.json as certifiers.
- Link list against the accepted s3_checks_r7.json: the reason splits into 31 items in each, and the sets are equal. The `listed` field and every other S3-3 field are equal (MEASURED). **Links unchanged.**
- Live wip/s3_checks_r8.json not touched (timestamp 18:31:05, before this run).

## 5 X1 O2 (ii) (Engineer section 9)

- Rule as written in check_sketch.py X1: a row with section_true in one spec, absent in a spec whose view is in SIDE_VIEWS and whose main Axes holds the row, is an issue. This is O2 (ii) as ruled at P3b.
- Premise: the drawn section equals section_true. K8 section_true_issues holds it on every side and section view (drawn piece named and equal to the spec piece), so a spec that carries section_true cannot draw the row from `section`. Plan views and the S3 plan inset are out of scope by the rule's own words.
- Red-first: X1-B5 is clean on the pre-change code (pre_run.txt l.15) and red by deletion `presence` (deltest.txt l.10).
- **FIX 1.** The one B control (X1-B5) plants the defect in s3 (section_yz, rows with `axes: [section]`, main Axes id "section"). The side_xz branch, rows without `axes` and main Axes id "main", which is the S1 form, has no control. Rule scope by class and view requires one.
  - Add X1-B6, fixture "s1 holder section_true removed", expected fires, reason "holder section_true: in s3, s4, absent in s1, which draws the row in side_xz (presence rule O2 (ii))", planted 1, gameplan_line 144.
  - Dry run (`x1_s1dry.txt`): s1_spec.yaml holder section_true deleted in the ws copy, then `check_sketch.py s4 --rev 1`. X1 fails with exactly that text (MEASURED). The copy was restored after the run.
  - Pre-change: the pre-change X1 has no presence branch, so X1-B6 is clean there (the X1-B5 evidence, same branch).
  - Signature: O2 (ii) is signed when X1-B6 is in the manifest and matches. No drawing change, and no revision opens.

## 6 NOTEs

1. carrier_torque uses r = core.diameter_nominal / 2 = 50 (50.9 kPa). The drawn carrier is r 50.50 (K d+1), which gives 2T / (pi 50.5^3) = 49.4 kPa (DERIVED). The reported value is the higher of the two, and both are far below any plastic shear limit. No change.
2. The holder.py tube top plus collar (z_top + t_col) and the test_P18 collar top agree only while collar.top_above_plate = collar.thickness + nut.lift_play (6.75 = 6.00 + 0.75, DECLARED leaves). The stack tie holder_flange (offset collar.thickness) lints the identity in s1, s3 and s4, and K6-B7 is re-planted red at 16.75. This is held, recorded for the Step 2 params owner.
3. RPT q10_exposed is tagged MEASURED. Its "on the stop -10.59" part is DERIVED, because no figure draws the core on the stop. q10_core_top states the split in its basis. q10_exposed does not.
4. Zero margins in S4 r1, all design identities: drill_head|collar 25.00, holder|wingnut 0.50, collar|wingnut 0.75, receiver|holder 0.25, collet foot and shoulder seats 0.00.

## Gameplan lines to change

1. detail 1.0, K table, row X1 (line 144). Apply after the Engineer's step1.4_engineer_draw_r1.md item 3 if it is still pending; the two edits are: Rule cell, append the signature after the P6 presence clause; B cell, X1-B5 view named and X1-B6 added (FIX 1).
Old:
```
| X1 | Shared rows (1.2): for every row id in two or more specs, `place`, `z_rule` and `plan_poly` expressions equal after whitespace normalisation; a row placed in one spec only is skipped and listed; `x1_exempt: {reason}` skips the place field only (1.3 P4, Loftsman (b) sign-off; --accept refuses while any spec carries x1_exempt, H1-B9); 1.4 P4: `section_true` equal on every shared row that carries it in two or more specs (Loftsman P3b O2 (i); `section` not compared); the presence rule O2 (ii) lands at P6; 1.4 P6: the presence rule O2 (ii): a shared row carrying section_true in one spec carries it in every spec that draws the row in a side or section view | Live s1 + s2 specs (47 compared; keepout place, base_plate and base_frame plan_poly skipped); runs with every sN run and --stale (1.2 (c)); X1-Z2 S4 section_true on the six base rows of s1 and s3 (staged form) | B1 s2 frame_upper_b r_in + 1; B2 s2 nut_a z_max changed; B3 exempt s3 anchor_c z_max + 1; X1-B4 s3 holder flange r_out + 1; X1-B5 s3 holder section_true removed (presence) |
```
New:
```
| X1 | Shared rows (1.2): for every row id in two or more specs, `place`, `z_rule` and `plan_poly` expressions equal after whitespace normalisation; a row placed in one spec only is skipped and listed; `x1_exempt: {reason}` skips the place field only (1.3 P4, Loftsman (b) sign-off; --accept refuses while any spec carries x1_exempt, H1-B9); 1.4 P4: `section_true` equal on every shared row that carries it in two or more specs (Loftsman P3b O2 (i); `section` not compared); the presence rule O2 (ii) lands at P6; 1.4 P6: the presence rule O2 (ii): a shared row carrying section_true in one spec carries it in every spec that draws the row in a side or section view (signed Loftsman P7a; premise drawn = spec held by K8 section_true_issues) | Live s1 + s2 specs (47 compared; keepout place, base_plate and base_frame plan_poly skipped); runs with every sN run and --stale (1.2 (c)); X1-Z2 S4 section_true on the six base rows of s1 and s3 (staged form) | B1 s2 frame_upper_b r_in + 1; B2 s2 nut_a z_max changed; B3 exempt s3 anchor_c z_max + 1; X1-B4 s3 holder flange r_out + 1; X1-B5 s3 holder section_true removed (presence, section_yz); X1-B6 s1 holder section_true removed (presence, side_xz; Loftsman P7a FIX 1) |
```
