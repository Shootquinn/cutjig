# Step 1.3 (b) spec sign-off (P3b), The Loftsman

Date 2026-11-26. Read: `step1.3_engineer_spec.md`; `docs/sketches/s3_spec.yaml` (whole), `proposed_params.yaml` (jackscrew, liftmotor, frame_upper), `check_stack.py`, `checks_s3.py`; `s1_spec.yaml` and `s2_spec.yaml` screw-set rows; K7 records of `s1_checks_r7.json` and `s2_checks_r5.json`; Designer params review sections 1 to 11; gameplan l.129-153, 267-295, Design Notes 31. Section screw: c (theta 270, YZ plane). Scripts, all in the scratchpad (`C:\Users\UR\AppData\Local\Temp\claude\eba575d6463ef2d6\6efaddfb-5e83-4849-8803-49d5d7303110\scratchpad\p3b\`): `hand.py` (stand-alone, no harness import), `comp.py` and `comp2.py` (check_stack and checks_s3 on the live spec), `dry.py` (section pieces through `sketch_common.overlap_area` and `min_distance`), `k7b.py` (K7 record entries). Nothing under `docs/sketches/` was edited. `check_sketch.py --stale` was run once (read only).

## Corrections to the brief

1. **My P0L NOTE 1 was conditional, and Tr12x3 triggered none of it.** The note reads "any change to anchor_z, length or block height must carry top_guide_z and both member leaves". The overlay as read: anchor_z 265, length 900, anchor_allowance 30, top_guide_z 1165 (expr agrees), member_length 1213, member_length_rail 1225 (MEASURED). The Engineer's Correction 1 is right. The note binds only a coupling remedy that moves anchor_z (Ruling R3).
2. **The spec carries no coupling remedy yet.** In s3_spec.yaml the coupling_c and screw_end_c z_rules use the centred-gap convention, and liftmotor_shaft_c|screw_end_c is declared F with the note "open item 5" (MEASURED). Section 5 checks the remedy space as inequalities, so the result holds for whichever remedy the Designer sets.
3. **S1 r7 and S2 r5 are stale, so under S3-3's own premise they certify nothing today.** `--stale` reports 2 records with 3 differences: jackscrew.lead and jackscrew.nominal on S1 r7, jackscrew.nominal on S2 r5 (MEASURED). The `chains` certifiers name those files (FIX 6).
4. **Housing to home switch at park is 12.23, not 11.16.** 11.16 is the vertical component. The in-plane distance is sqrt(5.00² + 11.16²) = 12.23 (DERIVED). The pair still passes G 10.

## 1 Section-plane coordinates

**Map (DECLARED in the spec, checked by hand).** For a point (x, y, z_A): u = y, plotted height z_S = z_A + 60, depth = x along the plane normal, positive toward the viewer. The viewer stands at +X and looks toward -X. The viewer's right is (-X) x (+Z) = +Y, so +u = +Y to the right, which agrees with the spec (DERIVED). For a row placed at (r_c, theta):
- Radial footprint, half-length a = (r_out - r_in) / 2 and half-width w: x = r_c cos theta ± (a |cos theta| + w |sin theta|); u = r_c sin theta ± (a |sin theta| + w |cos theta|).
- Round footprint: ± w on both.

At theta 270 this gives x = ± w and u = -r_c ± a. At theta 90 it gives x = ± w and u = +r_c ± a. Screw c is at (0, -160), so u = -160. Pinion c and NEMA 23 c are at theta 90 (`pinion.angle[0]` = 90), so u > 0.

**Inset map.** (x, y) → (x, y), +X right, +Y up, theta counter-clockwise seen from +Z. Screws at 30 (b, `angle[0]`), 150 (a, `angle[1]`) and 270 (c, `angle[2]`). A-A lies on x = 0 with its arrows toward -X.

**Depth along the plane normal (x band, DERIVED from place, section or plan_poly).**

| Row | x band | Row | x band |
|---|---|---|---|
| base_frame, base_plate | ±322 (plan_poly) | screw_c | ±6 |
| axis rows (receiver, collet, holder, collar, core, drill) | ± own outer radius (drill head ±88.90, tube ±76.20) | screw_end_c | ±4 |
| ring | ±210 | anchor_c | ±21 (square, tangential = X) |
| nut_housing_c | ±25 | anchor_bearing_c, guide_bearing_c | ±13 |
| nut_c | ±21 (flange) | guide_c | ±21 |
| bearing | ±100 | bracket_anchor_c, bracket_guide_c | ±30 |
| pinion_c | ±45.62 | frame_upper_c | ±30 |
| motor23_c | ±28.50 | liftmotor_c | ±21 true, ±29.70 footprint |
| motor_shaft_c | ±4 | liftmotor_pilot_c | ±11 |
| home_switch_c | ±3 | liftmotor_shaft_c | ±2.50 |
| standoffs_c | -18.25 to -12.75 (beyond) | coupling_c | ±9.50 |

**check_stack depth in section_yz is the wrong axis (MEASURED).** `evaluate_spec` returns `depth` = place y extent. Examples: screw_c gives [-166, -154] and standoffs_c gives [-178.25, -141.75]. Both are the in-plane u, not x. The LF-1 band rule needs x. This is the Engineer's open item 7, and it must land at P4 before any K7 of record on S3. It changes no verdict below: every pair here was judged on in-plane distance with the x bands overlapping, or on bands disjoint along x.

**Positions at capture_end, hand beside check_stack (z_S).** Hand values are from `hand.py`; computed values are from `comp2.py`.

| Row | u hand | z_S hand | check_stack (u = place y; z) |
|---|---|---|---|
| screw_c | -166 to -154 | 325.00-1225.00 | -166 to -154; 325.00-1225.00 |
| nut_c / nut_housing_c | -181 to -139 / -185 to -135 | 365.84-395.84 | same |
| anchor_c | -181 to -139 | 325.00-355.00 | same (radial r 139-181, hw 21) |
| anchor_bearing_c, line | -173 to -147 | 332.00-348.00, line 340.00 | same |
| guide_c / guide_bearing_c | -181 to -139 / -173 to -147 | 1195.00-1225.00 / 1206.00-1214.00 | same |
| frame_upper_c | -304 to -244 | 60.00-1285.00 | same |
| bracket arms c | -244 to -181 | 325.00-355.00, 1195.00-1225.00 | same |
| liftmotor_c | -181 to -139 (true), -189.70 to -130.30 (footprint) | 252.00-300.00 | footprint; 252.00-300.00 |
| pilot / shaft / coupling / screw end | ±11 / ±2.5 / ±9.5 / ±4 about -160 | 300-302 / 300-324 / 303.5-323.5 / 313.5-325 | same |
| home_switch_c | -210 to -190 | 1182.00-1195.00 | same |
| nut station park | - | 1155.84 | 1155.84 |

Inset (DERIVED; all equal to the Engineer's row table): screw_a x -144.56 to -132.56, y 74 to 86. anchor_a x -167.25 to -109.88, y 51.31 to 108.69 (half-extent 21 (cos 30 + sin 30) = 28.69). frame_upper_a x -278.27 to -196.31. home_switch_a x -183.37 to -163.04.

## 2 Hand values (DERIVED, `hand.py`) against computed (MEASURED, `comp.py`)

| Quantity | Hand | Computed |
|---|---|---|
| I, A (d_r 8.5) | 256.24 mm⁴, 56.75 mm² | same |
| L_min per Q9 option (0.5; 0.5 and 0.75; plus 1 m) | 885.00 / 885.00 / 1135.00; at anchor_z 885.84 / 885.84 / 1135.84 | 885.00, 885.84 (q9_options) |
| L_t = guide_bearing_z - anchor_bearing_z | 1150 - 280 = 870.00 (= L - 30, independent of anchor_z) | 870.00 |
| Nut-to-anchor segment at park | 1095.84 - 280 = 815.84 | 815.84 |
| P_cr floating K 0.7 / K 1.0, L_t | 1363.8 / 668.2 N | same |
| P_cr rigid K 0.5 / K 1.0, 815.84 | 3039.7 / 759.9 N | same |
| lambda; phi_n (mu 0.15 / 0.20) | 5.197 deg; 8.827 / 11.698 deg | same |
| eta; back-drive efficiency | 0.3641 / 0.2994; -0.698 / -1.253 (self-locking) | same |
| F_stall per screw / total | 343.18 / 1029.54; 282.21 / 846.64 N | 343.18 (governing) |
| WOB max = 3 F_stall + W | 1267.43 / 1084.54 N | - |
| Per screw: static, capture, retract, cut | 79.30, 113.31, 179.30, 254.04 N (W 24.25 kg, 237.89 N) | same |
| S3-2 margins, K 0.7 | 17.20, 12.04, 7.61, **3.97** at stall up (two-screw 11.47, 8.02, 5.07) | same |
| S3-2 margins, K 1.0 | 8.43, 5.90, 3.73, 1.95 | - |
| Cut tension stress per screw | 254.04 / 56.75 = 4.48 MPa | - |
| Lift torque cut / capture (mu 0.15; 0.20) | 0.333 / 0.149; 0.405 / 0.181 N m against 0.45 | - |
| Critical speed over L_t, d_r, E 200 GPa, 7850 | 1335.6 rpm pinned-pinned (2.67 x), 2086.4 rpm fixed-pinned (4.17 x) against 500 rpm (25 / 3 x 60) | 1335.59 / 2086.44; 500.00 |
| S3-1, nut bottom - anchor line per pose | load 800.84, start 675.84, capture_end 25.84, park 800.84 (all > 0: tension) | needs drawing |
| Tension segment, nut centre - 280 | 815.84 / 690.84 / 40.84 / 815.84 | needs drawing |

The end factor for critical speed: the drawn mounting is fixed anchor plus radial guide, so fixed-pinned (beta 3.9266) applies. Pinned-pinned is the conservative bound. Both pass at 2.67 or better.

What the hand values depend on:
- S3-1, S3-2, L_t, critical speed, F_stall and the torques read only jackscrew.length, anchor_allowance, guide_allowance, root_diameter, lead and mean_diameter, the thread mu and angle, the masses, and the pose tips.
- None of those depends on the coupling remedy or on the missing nut dimensions, unless the remedy moves anchor_z (R3).
- nut_mass 0.05 is a T8 figure (NOTE 4). At an estimated 0.14 per Tr12 nut, W rises 2.6 N and every margin falls by less than 1 percent.

## 3 S3-3 chains, certifying records, currency

K7 entries are MEASURED with `k7b.py`, all four poses. Every certifier the Engineer lists agrees with the records:
- S1 r7, class C, state C: collet|core_seat, collet|holder, receiver|holder, base_plate|receiver, base_frame|base_plate, ring|bearing, drill_tube|bearing, frame_upper_a|base_plate and frame_upper_b|base_plate.
- S1 r7, plan-contact: bracket_anchor_a/b|frame_upper_a/b and bracket_anchor_a/b|anchor_a/b.
- S2 r5: frame_upper_c|base_frame and base_plate|base_frame as z-contact; bracket_anchor_c|frame_upper_c and bracket_anchor_c|anchor_c as plan-contact.
- S1 r7: core_seat|core_750 is undeclared F, state undeclared:C at capture_end. drill_head|drill_tube is undeclared F with state undeclared:C. core_750|drill_head is N at capture_end.
- S2 r5: drill_tube|drill_head is undeclared F with state z-touch.

Currency: neither record is current (Correction 3). The stale keys (jackscrew.nominal, jackscrew.lead) touch no chain pair in either record: the screw-set pairs are N there, and the screw width enters no certified pair. So the r8/r9 entries should reproduce the r7/r5 classes. The record that certifies is still r8/r9 (FIX 6). The S2 r5 certifier for bracket_anchor_c|anchor_c is a round r 21 block: a tangent point at r 181. The 42 square keeps the contact plane at r 181, so the contact survives in value. S2 r9 re-certifies it as face contact, and S3 certifies it in section at u -181.

Pairs no record certifies today:
1. drill_head|core_750, on all three chains. This is the load-application pair (FIX 6 sets its certifier).
2. anchor_k|screw_k, screw_k|nut_k, nut_k|nut_housing_k and nut_housing_k|ring for k = a, b: 8 pairs (Ruling R1).
3. bearing|drill_tube and drill_tube|drill_head are declared only, as detail 1.3 states (S6-5).
4. With FIX 1 to 3 open, the S3-certified c pairs anchor_bearing_c|screw_c and nut_c|nut_housing_c read interference on the spec as written. anchor_c|anchor_bearing_c reads C on a radial face with no axial seat (section 4).

## 4 Section pieces, dry run (MEASURED, `dry.py`, `sketch_common.overlap_area` / `min_distance`, capture_end, z_A)

| Pair | Declared | Overlap mm² | Distance |
|---|---|---|---|
| screw_c\|anchor_bearing_c (screw drawn 12 wide, bore journal_d 10) | C | **32.00** | 0 |
| screw_c\|guide_bearing_c | C | **16.00** | 0 |
| anchor_c\|anchor_bearing_c | C | 0.00 | 0 (vertical face r 13 only) |
| nut_c\|nut_housing_c, placeholders body 22 / flange 8 | C | **152.00** | 0 |
| same, placeholders body 25 / flange 10 | C | **160.00** | 0 |
| same with a counterbore r flange_od / 2 + float in the flange band | C | 0.00 | 0 (shoulder face) |
| liftmotor_shaft_c\|screw_end_c | F | **52.50** | 0 |
| base_plate\|base_frame (in the plane x = 0) | C | 0.00 | **5.00** |
| base_frame\|frame_upper_c | C | 0.00 | 0.00 |
| screw_c\|anchor_c, screw_c\|nut_housing_c (body 22) | F | 0.00 | 7.00, 5.50 |

The nut placeholders (22/8 and 25/10) are dry-run values only. The interference holds for any nut_body_od < 41: area per side = (21 - body/2 - 0.5) x flange thickness.

## 5 Coupling stack (Engineer blocker 2)

Symbols: F = anchor_z - CL (motor face), CL = `liftmotor.coupling_length`, S = shaft length, H = coupling height, pilot height 2, clearances c_t (coupling top to block underside) and c_b (pilot top to coupling bottom), e_s = screw-end engagement, g = end gap between shaft tip and screw end. Values in z_A.

As written (CL 25, S 24, H 20, c_t = c_b = 1.5, e_s 10):
- Motor face 240, pilot top 242, coupling 243.5 to 263.5.
- Shaft tip 264.00 lies 0.50 above the coupling top.
- Screw end runs 253.5 to 265. Shaft and screw end overlap 10.50, 52.50 mm² (DERIVED and MEASURED).

Closure conditions (DERIVED):
- (a) CL >= H + c_t + c_b + 2 = 25.00: the coupling fits between pilot and block. This holds with equality today.
- (b) F + S + g <= anchor_z - c_t - e_s, that is CL >= S + e_s + g + c_t.
- (c) The shaft engages the coupling: e_m = F + S - (anchor_z - c_t - H) > 0, and H >= e_m + g + e_s.

With S 24, e_s 10, g 1, c_t 1.5, condition (b) needs CL >= 36.50. With CL 25 it needs S <= 12.50.

| Remedy | Values | Stack (z_A) | Keys S1/S2 read | Dry run shaft\|end |
|---|---|---|---|---|
| A: short shaft | S 12.5 (cut or short-shaft variant), CL 25 | face 240, shaft to 252.5, coupling 243.5-263.5, end 253.5-265; e_m 9, g 1, e_s 10 | none (`liftmotor.shaft_length` is S3-only) | G 1: 0.00 overlap, 1.00 |
| B: longer standoffs | CL 36.5, S 24 | face 228.5, motor 180.5-228.5, shaft to 252.5, coupling 243.5-263.5 (top-anchored), end 253.5-265 | `liftmotor.coupling_length` (S1 liftmotor_a/_b, S2 liftmotor_a/_b/_c): --stale adds it to both records; motors drop 11.50; no margin moves (motor\|arm z gap 25 to 36.5, LF1.1-10; motor bottom 180.5 is clear of the wing-nut band, top 153.09) | G 1: 0.00 overlap, 1.00 |
| C: longer coupling, CL 25, S 24 | none | (b) fails for every H: the shaft already reaches 264 of the 263.5 available | - | - |
| D: move anchor_z | window -2.50 <= delta <= +0.84 | +0.84 is the housing\|block g_min 10 at capture_end (10.84). -2.50 is the housing\|switch in-plane G 10 at park (sqrt(5² + (11.16 - delta)²) >= 10). -14.16 is the guide-block bound | anchor_z, top_guide_z, both member leaves, S1-4 | cannot reach 11.50 |

Under remedy B the spec's centred-gap z_rules (coupling at anchor_z - (CL - 2)/2 ± H/2, screw end from anchor_z - (CL - 2)/2) put the coupling at 237.75 to 257.75 and the screw end from 247.75. The shaft (to 252.5) and the end would overlap 4.75 again (DERIVED). The z_rules must be top-anchored (FIX 4).

Hand values that depend on the remedy: motor, pilot, shaft, standoff and coupling z bands; the screw-end bottom; and the drawn bar length = top_guide_z - screw-end bottom = 1165 - 253.5 = 911.50 under A or B (NOTE 3). No S3-1, S3-2, L_min, L_t or critical-speed value depends on it under A or B.

## 6 Rulings requested by the orchestrator

**R1. Symmetry premise for the a, b screw-set pairs: adopted, with a stated lint.**
- The S3 section is a true slice, so a C contact drawn there on screw c is a 3D contact. The a and b sets are the same parts rotated by 120 deg. Composing c's two anchor pairs (anchor_c|anchor_bearing_c and anchor_bearing_c|screw_c) certifies anchor_k|screw_k, and no anchor_bearing_a/_b rows are needed.
- Premise, as a check with Z and B (detail 1 common (h)): in every spec that carries them, the rows anchor, screw, nut and nut_housing for k = a, b have z_rule, place and keys equal to the c row after substituting `jackscrew.angle[2]` → `jackscrew.angle[k]`. Geometry fields only: S1/S2 declare these pairs N, which is the side-view nesting convention and does not contradict C. No row of the set may carry x1_exempt. The ring needs no rotation lint: it has no theta-dependent field except its S3 section_u, which is the cut through c.
- Consequences: until P6 removes x1_exempt from anchor_a/_b/_c, the S1/S2 anchor rows (round r 21) differ from S3's square, so the premise fails for anchor_k|screw_k. screw|nut, nut|housing and housing|ring can pass as soon as the lint lands.
- Z: live S1, S2 and S3 specs after P6. B: nut_housing_a z_rule offset 1; anchor_a place round while anchor_c is square; screw_b theta substituted wrongly (`angle[1]`).
- Until then the 8 pairs stay uncertified and S3-3 fails closed. That blocks S3 acceptance, not this signature.

**R2. x1_exempt on the S3 anchor rows until P6: accepted, with two conditions (NOTE 1).**
- The Engineer's dry run (17 live controls red) justifies keeping S1/S2 unchanged until their redraw.
- `x1_lint` exempts the whole row (check_sketch.py l.180-183, MEASURED), so the z_rule of anchor_a/_b/_c goes uncompared. By text it is equal today: "jackscrew.anchor_z" / "jackscrew.anchor_z + jackscrew.anchor_allowance" in all three specs.
- Condition 1: the exemption is scoped to the field (`fields: [place]`), so z_rule and plan_poly stay compared.
- Condition 2: S3's `--accept` is refused while any x1_exempt remains. P6 draws S1 r8 and S2 r9 before S3 is accepted, so this costs nothing and stops the exemption from outliving its reason. Harness items at P4, each with Z and B.

**R3. P0L NOTE 1: verified, and nothing moved.** The overlay values are in Correction 1. K2 expr agreement passes on the live overlay (Engineer, MEASURED). Section 5 bounds anchor_z to [-2.50, +0.84] at L 900, so no coupling remedy can use it. The five-key edit is triggered only if the Designer chooses D, and D cannot close the stack.

**R4. Coupling remedy.** A and B both close the stack (section 5). A moves no key that S1 or S2 reads. B moves `liftmotor.coupling_length` in both records with no margin change. Either way FIX 4 applies to the z_rules and the shaft|end declaration.

## 7 S1/S2 keys moved: rows, pairs, margins, spec edits

- **Keys moved by Tr12x3:** jackscrew.nominal (S1, S2) and jackscrew.lead (S1). Rows that move: S1 screw_a/_b widen from 8 to 12 (x band ±4 to ±6), the S1 lead ticks go to 3, the S2 screw circles go from d 8 to d 12. No K7 pair involving the screw is anything but N. The Engineer's previews (S1 r8, S2 r9, MEASURED) give every check value equal.
- **Margins, by hand:** S1-4 0.84 (housing to block 10.84 - 10); L 900 against 885.84; member tops 1225; S2-5a least 11.71. Screw b to the 45 deg sector edge: 160 sin 15 - 6 = 35.41. Block square to the 135 edge: 41.41 - 21 (cos 15 + sin 15) = 15.69. Neither is the least.
- **Ruling: S1 r8 and S2 r9 need spec edits beyond comments.**
  - S1 r8: anchor_a/_b place to the 42-square radial form. bracket_anchor_a/_b r_in to `jackscrew.pitch_radius + jackscrew.anchor_block_width / 2` (value 181 unchanged). screw_a/_b name, shape and label text from "T8" to "Tr12x3". reported_items (RPT). The mark line (already in the spec).
  - S2 r9: anchor_a/_b/_c place to the square, kind and projection from cylinder/circle to prism/rectangle; bracket r_in; the screw_c shape text "d 8" to "d 12".
  - Both: remove x1_exempt. Re-plant the fixtures the P2 dry run turned red (K5-Z3, K7-Z15, K5-B7 to B11, B13 to B18, B21, B24, K7-B33, K7-B19), each B re-shown red.
  - Remedy B adds only the value of `liftmotor.coupling_length`; the z_rule reads the key.
- **LF1.1-9 to -11 on the S3 values (DERIVED):**
  - **LF1.1-9 closed in S3:** the block's outer face lies in the arm end plane r 181, so the contact is 42 long, a face instead of a tangent point. The NEMA 17 31 pattern corner sits at r 21.92 from the axis and the standoff outer edge at 18.25 < 21, both inside the square. The S1/S2 rows close at P6.
  - **LF1.1-10 closed:** the true motor square is r 139 to 181 under the block, and its outer face lies in the arm end plane. Only the circumscribing footprint (to 189.70) still reaches under the arm, separated by 25 in z (36.5 under remedy B).
  - **LF1.1-11 unchanged:** the post and the block a square face each other in parallel at theta 150. The plan gap is 200 - 181 = 19.00. The block corners at r 182.21 do not reduce it.

## 8 Shared rows (X1)

`--stale` run: X1 pass, 70 shared rows compared, 3 skipped (base_frame and base_plate plan_poly; keepout place), 3 exempt (anchor_a, anchor_b, anchor_c) (MEASURED). The screw-set rows screw_c, nut_c, nut_housing_c, guide_c, bracket_anchor_c, bracket_guide_c, frame_upper_c and liftmotor_c match S2 in place and z_rule. S3 adds section_u, which X1 does not compare. FIX 1 and 3 can therefore be met in section_u without breaking X1.

## 9 Findings

**FIX 1 (screw_c, journal through the bearings).** screw_c is drawn as one rectangle 12 wide from 265 to 1165. The bearing bores are journal_d 10, so the declared C pairs read interference: 32.00 mm² at the anchor pair and 16.00 mm² at the guide (MEASURED, section 4).

Required: screw_c carries in-plane pieces (section_u, admitted for an unsectioned row) that step to journal_d over each bearing band:
- 272 to 288 at the anchor and 1146 to 1154 at the guide;
- a shoulder of d 12 under the lower anchor inner race at 272, which is the axial face the cut-case tension (S3-1) bears on;
- place half_width 6 unchanged, so it still contains every piece.

Dry run: with journal pieces of r 5 the pair is in contact at r 5 with 0.00 overlap, by the same arithmetic as anchor_c|anchor_bearing_c in section 4. The values (shoulder length, thread end) are the Designer's.

**FIX 2 (anchor_c, axial seats).** The block bore is a plain r 13 from 265 to 295, so anchor_c|anchor_bearing_c touches only on the vertical face. Nothing drawn carries axial load from the bearing pair into the block, so S3-3 would certify a radial touch as the axial loop.

Required:
- A block face above the upper outer race. In the cut case the screw is pulled up, and that face is the seat.
- A face or cover below the lower outer race, for the lifting cases (S3-2) in which the screw is pushed down.
- Example: bore r 13 over 272 to 288, and r 11 over 265 to 272 and 288 to 295. The upper lip clears the M10x1 locknut (about r 9), and the lower lip clears the d 12 shoulder (r 6).
- The locknut above the upper inner race stays not_drawn with its reason.

The values are the Designer's; the property (a face normal to Z in each load direction) is what this item requires.

**FIX 3 (nut_c and nut_housing_c, flange seat).** The housing pieces run the full 30 from body_od / 2 + float to 25. The flange (to r 21) is in the top t_f of the same band, so the pair interferes for any nut_body_od < 41: 152.00 mm² at placeholders 22 / 8 (MEASURED).

Required:
- (a) A housing counterbore of radius nut_flange_od / 2 + ring.nut_float = 21.5 in the flange band (wall 3.5 to the OD 50). Its shoulder face at nut_z + nut_length / 2 - t_f is the cut-case seat (the nut pushes the ring down) and the drawn S3-3 contact. Dry run: 0.00 overlap, contact on the shoulder.
- (b) A seat for the lifting cases, in which the nut pushes the housing up, above the flange. With the flange top flush with the housing top (both nut_z + 15, X1-shared z_rules) there is no housing material above it.
- The Designer's "retaining ring under the flange" would make a not-drawn ring the cut-case seat and leave no upward seat.
- The Designer states the upward seat (cap, bolts with float clearance, or a ring over a recessed flange) together with nut_body_od and nut_flange_thickness (Engineer blocker 1).

The condition body_od / 2 + 0.5 > nominal / 2 holds for any body_od > 11 (screw_c|nut_housing_c F).

**FIX 4 (coupling stack, whatever remedy).**
- (a) coupling_c and screw_end_c z_rules top-anchored from leaves: coupling z_max = `jackscrew.anchor_z - <coupling top clearance>`, z_min = z_max - `liftmotor.coupling_height`; screw end z_min = coupling z_max - `<screw-end engagement>`. The two new leaves are ASSUMED (1.5, 10). Under remedy B the centred-gap form re-creates a 4.75 overlap (section 5).
- (b) liftmotor_shaft_c|screw_end_c declared G, g_min 1 (shaft-tip to screw-end gap, ASSUMED). K7 in the section then enforces closure condition (b) on every future value.
- (c) The remedy is A (`liftmotor.shaft_length` <= 12.5) or B (`liftmotor.coupling_length` >= 36.5). D cannot close the stack (window [-2.50, +0.84]).

Dry run for A and B: 0.00 overlap, distance 1.00 (MEASURED).

**FIX 5 (base_plate|base_frame in the section).** Both rows declare the pair C. In the plane x = 0 the plate stops at |u| 239 and the rails start at 244, so the drawn pieces are 5.00 apart (MEASURED). K7 C fails at a distance above 0.05 when the x bands overlap (both ±322).

Required: declare the pair in S3 as F, with source "contact off the plane (rails beyond the notch, supports); certified by S1/S2, Designer 1.3 (a) Correction 8". The chain certifiers already exclude S3 for this pair, so no chain change is needed. Dry run: F, 0.00 overlap.

**FIX 6 (`chains` certifiers).**
- (a) The certifiers name `s1_checks_r7.json` and `s2_checks_r5.json`. Both are stale, and the S3-3 rule (spec s3_checks.S3-3.records) gives a stale record no certifying power. Certifiers name the sketch and the pair id ("S1 collet|core_seat C"). S3-3 resolves them to the latest accepted, unsuperseded record (S1 r8, S2 r9) at run time. S3's acceptance follows theirs; P6 draws all three.
- (b) drill_head|core_750 on chains a, b and c: certifier "declared (load application: the cut force acts between cutter and core; row load_cut, S3-1 reads it +Z)". No row draws the kerf face, and K7 holds the head and core as N by design, so no record can ever certify it C. As "none", S3-3 fails permanently.

**NOTE 1 (x1_exempt scope and expiry).** Ruling R2: field-scoped exemption and an `--accept` refusal on any remaining exemption, P4 harness items with Z and B.

**NOTE 2 (home switch lever against the housing, G 10).** The housing|switch pair passes at 12.23 in the plane at park. The lever sub-artist, drawn "down to the nut-housing top at park", touches the housing at park (distance 0) and enters the swept hull. Under the same row, G 10 then fails. The lever is excluded from the body pair and declared on its own (C at park, F elsewhere), or drawn as a phantom (Engineer open item 11). The Designer decides at P3a, and the declaration lands at P4.

**NOTE 3 (bar length).** screw_c (265 to 1165) plus screw_end_c (253.5 to 265) is a 911.50 bar under A or B (DERIVED). L_min (885.00 / 885.84) runs from the block underside to the guide top and omits the coupling end. The figure labels L 900, correct for the screw_c row, against DN23's 800 to 900. Reported item L_min should print the bar length beside it, and detail 1.3 sends values outside the range to Sean with the sketch.

**NOTE 4 (nut leaves).** `jackscrew.nut_mass` 0.05 and the `nut_length` source text ("brass T8 flange nut") are T8 figures. A brass Tr12 flange nut is about 0.14 kg (DERIVED at body 22, flange 42 x 8, density 8.5; ASSUMED). W rises 2.6 N and the margins fall less than 1 percent. The Designer sets these with blocker 1.

**NOTE 5 (check_stack depth in section_yz).** It reads place y (MEASURED, section 1). The x band must land at P4 (Engineer open item 7, O4) before any K7 of record on S3.

**NOTE 6 (carried, Loftsman 1.2 (b) item 5).** The bracket arms are "30-6060 stub" drawn 30 tall. A 30-6060 is 60 x 60. Unchanged at S3.

**Verdict: FIX (6 items: FIX 1 to 6).** Hand and computed values agree everywhere in section 2. FIX 1 to 3 and FIX 5 are section-piece and declaration edits in s3_spec.yaml. FIX 4 waits on the Designer's remedy (A or B). FIX 3 waits on the two nut leaves. I re-check on the edited spec with `dry.py`, and sign without re-reviewing the other sections.

## Gameplan lines to change

1. l.288, the S3-3 row. This supersedes the Engineer P2 item 7 if applied together. Old: "every consecutive pair class C in the drawn figures (S1 for core, base and frame members; S3 for anchor, screw, nut, ring; S6 for bearing and tube), K7 C |" New: "every consecutive pair class C, as an axial face contact in the section, in the K7 entries of a certifier named per pair in the spec `chains` by sketch and pair id and resolved at run time to the latest accepted S1 and S2 records (a stale record certifies nothing; S3 is accepted after S1 r8 and S2 r9), this figure, or declared (cutter\\|core as the load-application pair, row load_cut; bearing and tube for S6-5). Chain per screw: screw c runs base plate, base frame, member c (Design Notes 27); screws a, b run base plate, member a or b; the a, b screw-set pairs are certified from screw c under the symmetry premise lint (anchor, screw, nut, nut-housing rows equal in z_rule, place and keys after angle[c] to angle[k] in every spec, no x1_exempt) (Loftsman 1.3 (b) R1), K7 C |"
2. l.292, within the line. Old: "+ max(nut length, ring nut-housing height) + 2 g_min (Loftsman ruling, 1.1 (b);" New: "+ max(nut length, ring nut-housing height) + 2 g_min, with the drawn bar length beside it (screw-end bottom to guide-block top: L plus the coupling end, 911.50 at 1.3 (b), Loftsman 1.3 (b) NOTE 3) (Loftsman ruling, 1.1 (b);"
3. Insert after the line inserted by the Engineer P2 item 10 (text begins "| Section A-A: plane x = 0"). If that line is absent, insert after l.718 (text begins "| Ring **130 mm** above the tip"): "| Lift coupling stack: NEMA 17 shaft tip + 1 <= screw-end bottom; coupling 1.5 clear of the pilot top and the anchor-block underside; `liftmotor.coupling_length` >= shaft length + engagement + gap + clearance (36.5 at shaft 24) or shaft <= 12.5 at 25 | overlay `liftmotor.*`, s3_spec.yaml coupling_c, screw_end_c, liftmotor_shaft_c (G 1) | ASSUMED (Loftsman 1.3 (b) FIX 4); S1, S2 liftmotor rows read coupling_length |"
