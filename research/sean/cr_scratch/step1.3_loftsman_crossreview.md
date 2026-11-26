# Step 1.3 (e) geometry cross-review (P7a), The Loftsman

Date 2026-11-26. Revision under review: S3 r1 (`docs/sketches/wip/s3_checks_r1.json`, `s3_jackscrew_section_r1.png`, `s3_summary_r1.md`); S1 r8 and S2 r9 changed rows (key-driven revisions: Design Notes 31 Tr12x3, Design Notes 32 receiver shoulder OD 200 with 4 x M5). Section screw: c (theta 270, YZ plane).

Read: `research/sean/cr_scratch/step1.3_engineer_draw_r1.md`, `step1.3_engineer_redfirst.md` section 1; `docs/sketches/s3_jackscrew_section.py`, `s3_spec.yaml`, `checks_s3.py`, `check_stack.py`, `sketch_common.py` (K4, K6, K7, reflect_record, axes_contexts), `proposed_params.yaml`, `s1_spec.yaml` and `s2_spec.yaml` changed rows, `checks_s2.py` l.300-320; ASSEMBLY.md Coordinate frame; gameplan l.129-153, 267-300, Design Notes 31, 32; my files `step1.3_loftsman_spec_signoff.md` and `step1.3_loftsman_redfirst_signoff.md`.

Every run was on a copy of `docs/sketches/` at `D:\Unleashed Robotics\_scratch\cutjig\p7a\sk\` (dry runs on `sk2\`), with TMP and TEMP at `D:\Unleashed Robotics\_scratch\cutjig\tmp`. Scripts: `p7a\hand.py` (stand-alone, no harness import, run with `-I`), `p7a\probe.py` (section pieces, reflected depth bands, nut z per pose, S3-3 per link, named faces, inset centres), `p7a\probe2.py` (S1 r8 and S2 r9 changed rows). Records directory for S3-3: `p7a\records\` (S1 r7, S2 r5, and `wip/s1_checks_r8.json`, `wip/s2_checks_r9.json` copied with `accepted: true`, nothing else changed). Nothing under `docs/sketches/` was edited.

Tags: MEASURED (read from a run here), DERIVED (hand arithmetic), DECLARED (spec, overlay or ruling).

## Corrections to the brief

1. **The accepted-state line in the context is out of date.** It reads "--stale: 2 records, 0 differences". `--stale` on the live records today reports 2 records and 5 differences (MEASURED):
   - S1 r7: jackscrew.lead 8 to 3, jackscrew.nominal 8 to 12, liftmotor.coupling_length 25 to 36.
   - S2 r5: jackscrew.nominal 8 to 12, liftmotor.coupling_length 25 to 36.
2. **The S3-3 claim holds.** With S1 r8 and S2 r9 marked accepted in `p7a\records\`, `--stale --docs-dir records` reports 2 records and 0 differences, and `s3 --rev 1 --docs-dir records` gives S3-3 pass, 51 links closed, 14 listed (6 declared, 8 by symmetry from c) (MEASURED). The live run on the copy reproduces 14/16 with S3-3 red, 18 issues, all of them "stale" (MEASURED).
3. **The copy's PNG is pixel-equal to the r1 of record.** The scratch run rewrote `sk\wip\s3_jackscrew_section_r1.png`. Its array equals `docs/sketches/wip/s3_jackscrew_section_r1.png` (1559 x 4234 x 4, `numpy.array_equal` True, MEASURED).

## 1 Hand values beside the JSON

Inputs as read from the overlay (DECLARED/ASSUMED): Tr12x3 single start, d 12, lead 3, d_r 8.5, d2 = d - P/2 = 10.5, half angle 15, mu 0.15 / 0.20, T_hold 0.45 N m, E 200 GPa, density 7850, anchor_z 265, L 900, anchor and guide allowance 30. W_kg = 6 + 8 + 3 + 3 x 1.0 + 3 x 0.05 + 1.5 + 3 x 0.5 + 0.7 + 2 x 0.2 = 24.25 kg, W = 237.89 N (DERIVED).

| Quantity | Hand (DERIVED, `hand.py`) | JSON / harness (MEASURED) |
|---|---|---|
| L_min, 0.5 m only | 775 + 30 + 30 + max(30, 30) + 2 x 10 = 885.00; at anchor 959.84 + 130 + 6 + 15 + 30 + 10 - 265 = 885.84 | 885.00 / 885.84 |
| L_min, 0.5 and 0.75 m | 885.00 / 885.84 | 885.00 / 885.84 |
| L_min, plus 1 m | 1025 + 110 = 1135.00; 1209.84 + 191 - 265 = 1135.84 | 1135.00 / 1135.84 |
| Drawn bar (screw-end bottom to guide-block top) | motor face 265 - 36 = 229; shaft tip 229 + 24 = 253; screw end 253 + 1 = 254; 1165 - 254 = 911.00 | drawn screw_end_c 314.00 z_S, guide_c top 1225.00 z_S: 911.00 |
| Segment at park (nut centre - anchor bearing line) | 1095.84 - 280 = 815.84 | 815.84 |
| L_t | 1150 - 280 = 870.00 | 870.00; drawn bearing centres 340.00 and 1210.00 z_S, span 870.00 |
| I, A | pi 8.5^4 / 64 = 256.24 mm^4; 56.745 mm^2 | 256.24 |
| P_cr floating K 0.7 / K 1.0 (L 870) | 9.8696 x 200000 x 256.24 / 609^2 = 1363.8; / 870^2 = 668.2 N | 1363.8 / 668.2 |
| P_cr rigid K 0.5 / K 1.0 (L 815.84) | 3039.7 / 759.9 N | 3039.7 / 759.9 |
| lambda; phi_n | atan(3 / (pi 10.5)) = 5.197 deg; atan(mu / cos 15) = 8.827 / 11.698 deg | 5.20; 8.83 / 11.70 |
| eta | tan 5.197 / tan(5.197 + phi_n) = 0.3641 / 0.2994 | (used in F_stall) |
| F_stall per screw / total | 2 pi 0.45 eta / 0.003 = 343.18 / 1029.54 (mu 0.15); 282.21 / 846.64 (mu 0.20) | same |
| Back-drive efficiency | tan(lambda - phi_n) / tan lambda = -0.698 / -1.253 (self-locking) | same |
| Critical speed over L_t | sqrt(EI / rho A) = 1.073 x 10^7 mm^2/s; pinned-pinned pi^2 / 870^2: 1335.6 rpm (2.67 x); fixed-pinned 3.9266^2: 2086.4 rpm (4.17 x); rapid 25 / 3 x 60 = 500 rpm | 1336 / 2086 rpm, 500 |
| WOB max (3 F_stall + W) | 1267.43 / 1084.54 N | same |
| Lift torque per screw, cut / capture | 254.04 x 0.003 / (2 pi 0.3641) = 0.333, 0.149; mu 0.20: 0.405, 0.181 N m | same |
| Cut tension stress per screw | 254.04 / 56.745 = 4.48 MPa; stall down 343.18 / 56.745 = 6.05 MPa | 4.48 (spec) |

**Per-screw (load / 3) and two-screw (load / 2) shares, N (DERIVED; JSON equal):**

| Case | Per screw | Two-screw | P_cr / F, K 0.7 | K 1.0 | Rigid K 0.5 | Rigid K 1.0 |
|---|---|---|---|---|---|---|
| static (W) | 79.30 | 118.95 | 17.20 (two 11.47) | 8.43 | 38.33 | 9.58 |
| capture lift (W + 10.4 x 9.81) | 113.31 | 169.96 | 12.04 (8.02) | 5.90 | 26.83 | 6.71 |
| retract bind, min((W + 300) / 3, F_stall) | 179.30 | 268.95 | 7.61 (5.07) | 3.73 | 16.95 | 4.24 |
| cut ((1000 - W) / 3, tension) | 254.04 | 381.05 | - | - | - | - |
| stall up (F_stall, mu 0.15) | 343.18 | - | **3.97** | 1.95 | 8.86 | 2.21 |

**Axial force in each kept part (collet, holder, receiver, base plate), DERIVED:** 1000 N compression in the cut case. At F_stall alone 1029.54 / 846.64 N; at F_stall + W (stall down into a jam) 1267.43 / 1084.54 N. The base plate is a junction, not a column: in the cut case it takes 1000 down at the shoulder face, 2 x 254.04 = 508.07 up at members a, b, and member c's 254.04 plus W 237.89 = 491.93 goes through the base frame (spec load_cases cut note). Sum 1000.00.

## 2 Section-plane coordinates (K6 centres, K7 depth bands)

Map (DECLARED, signed at (b) and (c)): u = plan y, z_S = z_A + 60, depth = plan x, viewer at +X. A row at (r, theta) has u = r sin theta, depth centre r cos theta.

**K6 centres in plane coordinates, capture_end (hand DERIVED; drawn pieces MEASURED, `probe.py`):**

| Row | Hand u centre | Drawn u | Hand z_S | Drawn z_S |
|---|---|---|---|---|
| screw_c (r 160, theta 270) | 160 sin 270 = -160.00 | -166.00 to -154.00, centre -160.00 | 265 + 60 to 1165 + 60 = 325.00 to 1225.00, centre 775.00 | 325.00 to 1225.00, centre 775.00 |
| nut_c | -160.00 | -181.00 to -139.00, centre -160.00 | nut_z 320.84 + 60 = 380.84 ± 15: 365.84 to 395.84 | 365.84 to 395.84, centre 380.84 |
| frame_upper_c (r 274, radial 244 to 304) | -274.00 (-304.00 to -244.00) | -304.00 to -244.00, centre -274.00 | 0 + 60 to 1225 + 60 = 60.00 to 1285.00 | 60.00 to 1285.00 |
| anchor_c (42 square) | -160.00 (-181 to -139) | -181.00 to -139.00 | 325.00 to 355.00 | 325.00 to 355.00 |
| receiver (round, shoulder r 100) | 0.00 (-100 to 100) | -100.00 to 100.00 | 12 + 60 = 72.00 to 188.50 | 72.00 to 188.50 |

Inset (plan, MEASURED against DERIVED): screw_a centre (-138.564, 80.000) = 160 (cos 150, sin 150); anchor_a extent ±28.687 = 21 (cos 30 + sin 30); frame_upper_a x -278.272 to -196.310 = -237.291 ± 40.981; home_switch_b centre (173.205, 100.000) = 200 (cos 30, sin 30). All equal.

**K7 depth bands (x, along the plane normal), reflected stack MEASURED against place DERIVED:**

| Row | Hand | Harness |
|---|---|---|
| screw_c | 160 cos 270 ± 6 = ±6.00 | -6.00, 6.00 |
| nut_c (flange OD 42) | ±21.00 | -21.00, 21.00 |
| nut_housing_c (OD 50) | ±25.00 | -25.00, 25.00 |
| frame_upper_c (hw 30) | ±30.00 | -30.00, 30.00 |
| liftmotor_c | ±21 true square; ±29.70 circumscribed footprint | -29.70, 29.70 (footprint, as LF1.1-10) |

Every pair below was judged on in-plane distance with overlapping x bands; none rests on band separation. Sample K7 entries at capture_end (MEASURED) with hand values: nut_housing_c|anchor_c G 10.84 (305.84 - 295); screw_c|anchor_c F 2.00 (cover bore r 8 - r 6); screw_c|guide_c F 7.00 (r 13 - r 6); ring|frame_upper_c G 34.00; nut_c|nut_screws_c F 0.05 (axial play); base_plate|frame_upper_c undeclared F 5.00 (plate stops at u -239, member at -244).

## 3 S3-1 and S3-3

**S3-1, every nut position from the S1 poses (anchor bearing line drawn at 340.00 z_S = 280 z_A, MEASURED; cut arrow +Z):**

| Pose | nut_z (check_stack, MEASURED) | Nut bottom - line (DERIVED) | Nut centre - line | Thread margin (300 to 1120) |
|---|---|---|---|---|
| load | 1095.84 | 800.84 | 815.84 | top 1120 - 1110.84 = 9.16 |
| start | 970.84 | 675.84 | 690.84 | - |
| capture_end | 320.84 | **25.84** | 40.84 | bottom 305.84 - 300 = 5.84 |
| park | 1095.84 | 800.84 | 815.84 | top 9.16 |

All positive: tension in every pose. JSON least 25.84, tension_segment 815.84 / 690.84 / 40.84 / 815.84: equal.

**S3-3 per screw, with the certifying records (MEASURED, records S1 r8 and S2 r9, both 0 stale differences):**

Chain c (19 links):
- drill_head|core_750 and drill_tube|drill_head: declared.
- core_750|core_seat, anchor_c|anchor_bearing_c, anchor_bearing_c|anchor_locknut_c, anchor_locknut_c|screw_c, screw_c|nut_c, nut_c|nut_housing_c, nut_housing_c|ring: S3 section, C.
- receiver|base_plate: S3 section, C, named face receiver.shoulder_z.
- core_seat|collet, collet|holder, holder|receiver: S1 r8, C.
- base_plate|base_frame: S1 r8 C and S2 r9 z-contact.
- base_frame|frame_upper_c: S2 r9 z-contact and S3 C.
- frame_upper_c|bracket_anchor_c and bracket_anchor_c|anchor_c: S2 r9 plan-contact and S3 C.
- ring|bearing: S1 r8 C, S2 r9 plan-contact, S3 C.
- bearing|drill_tube: S1 r8 C, S2 r9 plan-contact, declared.

Chains a and b (16 links each):
- receiver|base_plate: S3 alone, the S1 slab certifier struck (Design Notes 32).
- base_plate|frame_upper_k: S1 r8 C and S2 r9 z-contact.
- frame_upper_k|bracket_anchor_k and bracket_anchor_k|anchor_k: S1 r8 and S2 r9 plan-contact.
- anchor_k|screw_k, screw_k|nut_k, nut_k|nut_housing_k, nut_housing_k|ring: by symmetry from c. SYM passes on 18 pairs.
- ring|bearing and bearing|drill_tube: S1 r8 C.

**Named faces at capture_end (horizontal edges at the face z, MEASURED; overlap in u DERIVED from the spans):**

| Face | z_A / z_S | Upper piece spans | Lower piece spans | Overlap per side |
|---|---|---|---|---|
| receiver shoulder on plate top | 12 / 72.00 | receiver -100.00 to -80.00 | plate -239.00 to -80.20 | 19.80 |
| cover underside on upper outer race | 288 / 348.00 | anchor_c -181.00 to -168.00 | bearing -173.00 to -165.00 | 5.00 |
| locknut top under lower inner race | 272 / 332.00 | bearing -173.00 to -165.00 | locknut -169.00 to -165.00 | 4.00 |
| counterbore shoulder under nut flange | 327.84 / 387.84 | nut flange -181.00 to -166.00 | housing -185.00 to -171.50 | 9.50 |

The receiver shoulder is 100 - 80.2 = 19.80 wide per side and lies 244 - 100 = 144.00 from member c (Design Notes 32, MEASURED 144.00). The cut-case path through the anchor is: locknut, lower inner race, the races clamped in the block, cover at 288. The screw shoulder at 288 unloads in the cut case. In the lifting cases the screw shoulder at 288 loads the inner races down onto the block shoulder at 272, overlap 3.00 (-181.00 to -170.00 against -173.00 to -165.00, MEASURED).

## 4 LF1.1-9 to -11 on the drawn blocks and motor mount

- **LF1.1-9, anchor block on the arm end: closed in S1, S2 and S3.**
  - S3: the anchor_c|bracket_anchor_c contact is C, distance 0.00, on u = -181.00 over z_S 325 to 355 (MEASURED).
  - S1 r8: bracket_anchor_a|anchor_a is plan-contact, "spec placement, exact" (r7: "circumscribed 128-gon").
  - S2 r9: plan-contact, exact, for anchor_a and anchor_c.
  - The 42-square outer face lies in the arm-end plane r 181 over its full 42 width (DERIVED: r_c 160 + 21).
  - The guide block stays round. See NOTE LF1.3-7.
- **LF1.1-10, motor square under the block: closed.**
  - The true square spans u -181 to -139 under the block (S3, MEASURED).
  - The motor top is at 229 z_A and the arm bottom at 265, a z gap of 36.00. This holds in S1 r8, S2 r9 and S3 (MEASURED; 25.00 in S1 r7 and S2 r5).
  - Only the circumscribed footprint (±29.70) reaches under the arm.
- **LF1.1-11, descent-stop post against block a: unchanged.**
  - The plan gap is 200 - 181 = 19.00. The block corners at r sqrt(181² + 21²) = 182.21 lie on the same r 181 face plane, so the gap does not shrink (DERIVED).
  - The post top is level with the block bottom: S2 r9 z-touch with z gap 0.00, and S1 r8 side projection undeclared:C at distance 0.00, the same as S1 r7 (MEASURED).
  - The pair is undeclared F and passes.

## 5 Reported items: arithmetic

Every RPT value in `wip/s3_checks_r1.json` equals the hand value in section 1 to the printed precision: L_min, n_crit, pcr_margin, f_stall, wob_max, lift_torque, kept_axial, backdrive, screw_share, tension_segment. Two items are short of what detail 1.3 asks: LF1.3-1 (bar length and head value missing from L_min) and LF1.3-2 (W leaves out moving mass).

## 6 S1 r8 and S2 r9 changed rows

Changed rows checked by hand against the drawn pieces (`probe2.py`, MEASURED) and the record values (r7/r5 to r8/r9, MEASURED):
- S1 anchor_a/_b, 42 square at theta 150 / 30 in side projection: x -138.564 ± 28.687 = -167.251 to -109.878, depth 80 ± 28.687. Drawn equal, and the mark line `anchor_a:line` at 340.00 z_S spans the block. Mirror for b.
- S1 screw_a/_b, Tr12x3: x -138.564 ± 6 = -144.564 to -132.564. Drawn equal.
- S1 receiver shoulder: ±100 at z_S 72 to 80. Drawn receiver extent ±100.00 from 72.00.
- S1 bracket_anchor_a: r 181 to 244, hw 30 at 150. Centre x -184.030 ± (31.5 x 0.866 + 30 x 0.5 = 42.280) gives -226.310 to -141.751. Drawn equal.
- S2 anchor_c, square: x ±21, y -181 to -139. S2 screw_c, d 12: x ±6, y -166 to -154. S2 receiver_shoulder: circle r 100. All drawn equal.
- Every S1 check value is equal r7 to r8: S1-1 650.00, S1-2 125.00, S1-3 367.34 / 117.34, S1-4 0.84, S1-5a 192.34, S1-5b 142.00, S1-6 0, S1-7 607.66. Every S2 check value is equal r5 to r9: S2-2 52.80, S2-5a 11.713, S2-5b 19.84, others 0.
- S1 K7 nut_housing_a|anchor_a, x overlap 25 + 28.687 = 53.69 (DERIVED). This matches the Engineer's -53.69: state F, z gap 10.84, plan relief.
- S2 r9 tip_force_footprint reads `s1_mass_report_r7.json`: 341 / 368 / 531 / 258 N, against S1 r8 351 / 379 / 563 / 269 N (MEASURED). See LF1.3-3.

## 7 Findings

**FIX LF1.3-1 (RPT L_min short of detail 1.3 l.293).**
- Gameplan l.293 requires the drawn bar length beside L_min, plus the value with the shoulder-screw head (my (b) NOTE 3; Designer re-sign note 1). The record's L_min item prints neither. The 911.00 appears only in the Engineer's report text.
- Remedy: `checks_s3.reported` appends both, read from the drawn pieces.
  - Bar: guide_c top - screw_end_c bottom = 911.00.
  - Head: nut_screws_c top - nut_housing_c top = 400.39 - 395.84 = 4.55, giving L_min 889.55 / 890.39 / 1139.55 / 1140.39.
- Dry run (`sk2`, MEASURED): RPT pass, 10 items. The value ends "drawn bar 911.00 ...; with the shoulder-screw head 4.55 above the housing top: L_min 889.55, at anchor_z 890.39, ..., L_min 1139.55, at anchor_z 1140.39". The run's other checks are unchanged.
- The edit changes no pixel.

**FIX LF1.3-2 (W leaves out the drill top-end block; Engineer D5).**
- `load_cases.W_kg` omits `drill.top_block_mass` 2 kg. The block is moving: the S1 r8 mass report lists it as "moving, not in W_kg", and it rides on the drill. `drill.mass` 8 is the drill from cutter tip to top end (overlay source), so the block is not inside it. The Designer confirms that last point.
- With the block, W = 26.25 kg, 257.51 N (DERIVED). Per screw:
  - static 85.84 (P_cr / F 15.89);
  - capture lift 119.85 (11.38);
  - retract bind 185.84 (7.34);
  - cut 247.50;
  - stall up unchanged at 343.18, so the least margin stays **3.97**.
- WOB max and kept axial at F_stall + W become 1287.05 / 1104.16 N, against the 1267.43 sent to Quinn as N5 (B2-7).
- Lift torque, cut / capture: 0.325 / 0.157 N m (mu 0.15).
- Dry run (`sk2`, W_kg plus `drill.top_block_mass`, MEASURED): S3-2 pass, least 3.97. pcr_margin, wob_max, kept_axial, screw_share and lift_torque read the values above.
- The spec literals in load_cases (per_screw, two_screw, kept_parts) and in S3-2 `expected` carry the 24.25 kg values and change with it.
- No pixel changes. The B2-7 figure to Quinn changes from 1267 to 1287 N.

**FIX LF1.3-3 (S2 r9 reported tip force from S1 r7; Engineer D9).**
- `checks_s2.py` l.314 reads `s1_mass_report_r7.json`, and the S2 r9 record carries 341 / 368 / 531 / 258 N.
- Remedy: read the latest accepted S1 mass report (r8 after `--accept s1`), with basis text to match. Re-run `s2 --rev 9` after S1 r8 is accepted and before `--accept s2`.
- Dry run (`sk2`, path to the r8 report, MEASURED): 18/18 pass, tip_force_footprint 351 / 379 / 563 / 269 N. The basis text still names r7 and must change with the path.
- No pixel changes.

**NOTE LF1.3-4 (K4 D1 confirmed in code).**
- `sketch_common.k4` (l.1942) tests `want not in txt.replace(lab["text"], " ")`, which removes every occurrence of the label text. The value "one controller, three drivers, home switch per screw at park; no belt" begins with the label text "one controller, three drivers, home switch per screw", so the value is cut out of every possible drawing.
- hold_callout passes because its text is not a substring of `hold.device`.
- Spec remedy (Designer): label text that is not a substring of the value. It needs no harness change. A harness change (replace once) needs its own Z and B under rule (h).
- The label is drawn text, so the fix opens S3 r2. Not a geometry item.

**NOTE LF1.3-5 (D8 and open item 7: arm end and guide block read nut_flange_od / 2).**
- bracket_anchor_a/_b/_c r_in = pitch_radius + nut_flange_od / 2.
- guide_c place and section_u read nut_flange_od / 2.
- The values equal anchor_block_width / 2 and guide_block_od / 2 (21). The S3 guide_c note promised the rename at P6; it did not land.
- A change to the nut flange alone moves the arm end off the block face. K7 C then fails closed in all three specs, so no wrong drawing can pass.
- Ruling on D8: no edit at r8/r9. The rename to anchor_block_width / 2 and guide_block_od / 2 lands in all three specs together (X1 keeps them equal) at the next revision that touches those rows, Step 2 at the latest.

**NOTE LF1.3-6 (receiver uplift arithmetic).**
- Design Notes 32 sizes the 4 x M5 against "up to 1029.5 N" (3 F_stall, gross).
- The receiver takes uplift only through a gripped core: the bind. The motors lift W first, so the stall-limited bind is 3 F_stall - W = 791.65 N (mu 0.15) or 608.75 N (mu 0.20), and 772.03 N with LF1.3-2 (DERIVED).
- Stall up with no core gripped closes through member, screw, ring and stop, and loads no kept part.
- 1029.5 is a safe upper bound. The value is reported for the bolt sizing.

**NOTE LF1.3-7 (guide block round on a flat arm end).**
- guide_c is a D42 round. In plan it meets the arm end r 181 at a tangent point.
- In S3 the cut at x = 0 runs through the tangent line, so the section shows a 30-tall contact. The 3D contact is a line, not a face.
- The guide is radial support only and is not in the axial loop. To Step 2 with Design Notes 25 T2-b (block form).

**NOTE LF1.3-8 (nut mass, carried from (b) NOTE 4).**
- nut_mass 0.05 is a T8 figure. At 0.14 per Tr12 nut, together with LF1.3-2: W 26.52 kg; static margin 15.73, retract 7.30, WOB 1289.70 N (DERIVED).
- The least margin is unchanged at 3.97.

**NOTE LF1.3-9 (thread travel margins).**
- The nut stays on the Tr12x3 thread (300 to 1120) in every pose: 5.84 at capture_end (bottom) and 9.16 at load and park (top) (DERIVED from check_stack nut_z).
- No check holds these margins.
- They are reported here for the Step 2 screw row: thread_start_z and thread_end_z are ASSUMED literals, not expressions in the pose stack.

Counts: BLOCK 0, FIX 3 (LF1.3-1, -2, -3), NOTE 6 (LF1.3-4 to -9).

**CROSS-REVIEW PASS (S3 r1, geometry).**
- Every hand value in sections 1 to 4 equals the JSON or drawn value to 0.01 mm, or to the printed precision.
- S3-1 tension holds in every pose. S3-2 holds at 3.97. S3-3 closes 51 links with S1 r8 and S2 r9 accepted.
- LF1.3-1 and LF1.3-2 change reported values only, and close with a re-run.
- K4 (LF1.3-4) is outside geometry and opens r2.

**CROSS-REVIEW PASS (S1 r8, changed rows).**

**CROSS-REVIEW PASS (S2 r9, changed rows), with FIX LF1.3-3 before `--accept s2`.**

## Gameplan lines to change

1. l.279 (load case Static). Applies when LF1.3-2 closes.
   - Old: `two guide bushings with housings (overlay masses, ASSUMED until Q2, DN23-d and batch 2 B2-6 are answered; 24.25 kg at the 1.3 (a) values, Designer 1.3 (a) Correction 1).`
   - New: `two guide bushings with housings + the drill top-end block (drill.top_block_mass, moving; Loftsman 1.3 (e) LF1.3-2) (overlay masses, ASSUMED until Q2, DN23-d and batch 2 B2-6 are answered; 24.25 kg at the 1.3 (a) values, Designer 1.3 (a) Correction 1; 26.25 kg with the block: WOB max 1287.05 N, S3-2 least margin 3.97 unchanged).`
2. l.293 (Reported).
   - Old: `and the value with the nut shoulder-screw head above the housing top (889.55 / 890.39 at 1.3 (b) P2f2; Designer re-sign note 1)`
   - New: `and the value with the nut shoulder-screw head above the housing top (889.55 / 890.39 at 1.3 (b) P2f2; Designer re-sign note 1; both printed in the RPT L_min item from the drawn pieces, Loftsman 1.3 (e) LF1.3-1)`
3. l.705 (Design Notes 32).
   - Old: `for uplift in retract-with-bind and stall up (up to 1029.5 N)`
   - New: `for uplift in retract-with-bind and stall up (up to 1029.5 N gross; the receiver takes uplift only through a gripped core, stall-limited 3 F_stall - W = 791.65 N at mu 0.15, DERIVED, Loftsman 1.3 (e) LF1.3-6)`
