# Step 1.1 (b) Loftsman spec sign-off, S1 (arithmetic and placement)

## Corrections to the brief

1. The P3b brief asks for the park tip "G1, core_stop". Under Design Notes 22 (option R) the park reads `entry_plane`, the collar top 159.84 z_A. The core-stop park is now a reported value only: 884.84 z_A. G1 governs S1-3 alone.
2. The brief's lift-fit figures (stroke 830.16, L 920.16 / 950.16) are from the 1.0 draft. Option R replaces them: stroke 775.00, and L by the expressions in section 2.
3. S1-5b is not a ring-to-wing-nut question. The highest fixed base part under the ring is the holder collar ring at 159.84 z_A. The spec has no row for it (section 3).

Tags: HAND = my pencil arithmetic. DERIVED = check_stack.py output (run 2026-11-25, exit 0). MEASURED = control or fixture runs I made in scratch. Overlay design values are ASSUMED as the overlay marks them.

## 1. Hand values beside the Engineer's values

### 1.1 Park, stop, stroke (option R)

Option R stop rule: stop_k = max(stop.height_z 184.84, core_stop 42.5 + L + g_stop 25 - bore_ceiling_above_tip 800).

| Quantity | Hand | check_stack (DERIVED) | Engineer | Agree |
|---|---|---|---|---|
| stop_k, 0.5 m | max(184.84, -232.50) = 184.84 | 184.84 | 184.84 | yes |
| stop_k, 0.75 m | max(184.84, 17.50) = 184.84 | 184.84 | 184.84 | yes |
| stop_k, 1 m | max(184.84, 267.50) = 267.50 | 267.5 | 267.5 | yes (but see FIX 5) |
| start_k, 0.5 and 0.75 m | 184.84 + 650 = 834.84 | 834.84 | 834.84 | yes |
| Park tip, entry plane (collar top) | max(834.84, 159.84 + 750 = 909.84) + 50 = 959.84 | 959.84 | 959.84 | yes; equals params upper.park_z |
| Park tip, core-stop plane (reported) | max(834.84, 42.5 + 750 = 792.50) + 50 = 884.84 | 884.84 | 884.84 | yes |
| Park tip with 1 m, collar top | max(917.50, 1159.84) + 50 = 1209.84 | 1209.84 | 1209.84 | yes |
| Lowest stop tip | 184.84 | 184.84 | 184.84 | yes |
| Lift stroke, stand-in | 959.84 - 184.84 = 775.00 | 775.0 | 775.00 | yes |
| Lift stroke, plus 1 m | 1209.84 - 184.84 = 1025.00 | 1025.0 | 1025.00 | yes |
| Highest point, load and park | tip 959.84 + 800 + 150 = 1909.84 z_A = 1969.84 z_S; margin +30.16 | 1969.84 / 30.16 | same | yes |
| Highest point, start | 834.84 + 950 + 60 = 1844.84 z_S; +155.16 | same | same | yes |
| Highest point, capture_end | frame member 1225 + 60 = 1285.00 z_S; +715.00 (drill top block 1194.84 z_S lies below it) | same | same | yes |
| S1-2 | 959.84 - 834.84 = 125.00 | n/a | +125.00 MEASURED | yes |
| S1-3, 0.5 / 0.75 m | 959.84 - 50 - 542.50 = 367.34; 959.84 - 50 - 792.50 = 117.34 | n/a | 367.34 / 117.34 | yes |

### 1.2 S1-4 band per pose (as coded)

Stack, relative to the tip: ring underside +130, ring top +142, nut_z +136, nut and housing +121 to +151.
- Anchor block: 265 to 295. Guide block: 1135 to 1165.
- Band as coded: low = 265 + 30 + 15 = 310; high = 1165 - 30 - 15 = 1120 z_A.

| Pose | Tip z_A | Nut z_A (HAND) | Low margin HAND / Engineer | High margin HAND / Engineer |
|---|---|---|---|---|
| load | 959.84 | 1095.84 | 785.84 / 785.84 | 24.16 / 24.16 |
| start | 834.84 | 970.84 | 660.84 / 660.84 | 149.16 / 149.16 |
| capture_end | 184.84 | 320.84 | 10.84 / 10.84 | 799.16 / 799.16 |
| park | 959.84 | 1095.84 | 785.84 / 785.84 | 24.16 / 24.16 |

All eight values agree. Each pose's low and high margins sum to 810.00 = L 900 - 30 - 30 - 30, so the band closes.

K7 G gaps from the nut housing (HAND):
- To the anchor top at capture_end: 305.84 - 295 = 10.84.
- To the guide bottom at park: 1135 - 1110.84 = 24.16.

Both agree with the Engineer. S1-4 with FIX 2 applied: low = 295 + 10 + 15 = 320, high = 1135 - 10 - 15 = 1110.

| Pose | Low (HAND) | High (HAND) |
|---|---|---|
| load / park | 775.84 | 14.16 |
| start | 650.84 | 139.16 |
| capture_end | 0.84 | 789.16 |

### 1.3 Capture reach, bore ceiling, ring to base

| Check | Hand | Engineer | Agree |
|---|---|---|---|
| S1-7 Z | core top 42.5 + 750 = 792.50; 792.50 - 184.84 = 607.66 against 534.93, spare 72.73 | 607.66 / 534.93 / 72.73 | yes |
| S1-7 planned B | 42.5 + 500 = 542.50; 542.50 - 184.84 = 357.66; short 534.93 - 357.66 = 177.27 | 357.66 / 177.27 | yes |
| S1-5a with the capture core | bore ceiling 184.84 + 800 = 984.84; 984.84 - 792.50 = 192.34 >= 25 | 192.34 | yes |
| S1-5b, drawn rows | bearing bottom 184.84 + 117 = 301.84; wing-nut top 159.84 - 6.75 = 153.09; 148.75 | 148.75 | arithmetic yes; reference wrong (section 3) |
| S1-5b, physical | 301.84 - collar top 159.84 = 142.00 | Designer 142.00 | Designer correct |
| ring_on_tube (a) | bearing bottom +117 - head top +106.369 = 10.63 | Designer 10.63 | yes |
| ring_on_tube (b) | drill top +800 - gear top +256 = 544.00 | Designer 544.00 | yes |

Ring assembly at capture_end, z_A (HAND):

| Part | Rule | z_A |
|---|---|---|
| bearing | +117 to +142 | 301.84 to 326.84 |
| housing | +121 to +151 | 305.84 to 335.84 |
| pinion | pinion axis +194 +/- 45.62 | 333.22 to 424.46 |
| NEMA 23 | +194 +/- 28.5 | 350.34 to 407.34 |
| gear | +194 + 28.23 to +194 + 62 | 407.07 to 440.84 |
| descent pad | (184.84 + 130) - 12 to 314.84 | 302.84 to 314.84 |
| lift motor | 265 - 25 - 48 to 265 - 25 | 192 to 240 |

All of these agree with the Engineer's table.

### 1.4 TP-9 core_750 load z_rule (task 6)

- Core bottom: 42.5 + 0.5 x (159.84 - 42.5) = 42.5 + 58.67 = 101.17 z_A. Core top: 851.17 (HAND; check_stack 161.17 / 911.17 z_S = 101.17 / 851.17 z_A, DERIVED).
- This is the midpoint of the insertion stroke from the entry plane (collar top) to the load plane (core stop), as stated.
- Tip at load: 959.84. Core top to tip: 108.67.
- Entry instant (bottom on the collar top): core top 909.84, 50.00 under the tip = upper.load_clearance. The park rule closes on this case by construction.

## 2. Screw length (B3, Engineer open item 2)

### 2.1 Derivation

Moving body around the nut: nut and housing coaxial, both centred on nut_z.
- Axial half-extent: e = max(nut_length, ring.nut_housing_height) / 2 = 15.
- Fixed blocks: anchor block anchor_z to anchor_z + a (a = anchor_allowance 30); guide block anchor_z + L - g to anchor_z + L (g = guide_allowance 30).
- K7 clearance g_min = 10 (fixed_g10, g_min seed l.148), housing to each block.

| End | Pose | Inequality |
|---|---|---|
| Bottom | lowest stop | (z_low + p + t/2) - e - (anchor_z + a) >= g_min |
| Top | park | (anchor_z + L - g) - (z_park + p + t/2) - e >= g_min |

Adding the two eliminates anchor_z, p and t:

**L_min = lift stroke + anchor_allowance + guide_allowance + max(nut_length, ring.nut_housing_height) + 2 g_min**

### 2.2 The four candidates

| Candidate | Stand-in (HAND) | Ruling |
|---|---|---|
| S1-4 band as coded: stroke + a + g + nut_length | 775 + 90 = 865.00 | Short by 2 g_min. It lets the nut face touch the blocks, which K7 forbids. |
| detail 1.3: stroke + nut_length + a + g + nut_housing_height | 895.00 | Counts the coaxial 30 mm twice (nut inside the housing, same centre, same height) and omits g_min; 10.00 over the requirement at these values, with no basis. |
| Designer: stroke + a + g + max(n, h) + 2 x 10 | 885.00 | **Taken.** Equals section 2.1. |
| Designer at anchor_z | 885.84 | The same constraint with the anchor fixed at the drawn 265. The anchor may rise to 184.84 + 136 - 15 - 30 - 10 = 265.84, so the drawn anchor carries 0.84 of slack at the bottom. Reported, not the expression. |

Per Q9 option (HAND = check_stack DERIVED):

| Q9 option | L_min | L at the drawn anchor 265 | L to buy |
|---|---|---|---|
| 0.5 m only | 885.00 | 885.84 | 900 |
| 0.5 and 0.75 m | 885.00 | 885.84 | 900 |
| plus 1 m | 1135.00 | 1135.84 | 1140 |

The drawn 900 leaves 15.00 of spare: 0.84 at the anchor and 14.16 at the guide (the guide-end K7 gap 24.16 less g_min 10).

### 2.3 Corrections that follow

- Gameplan l.284 detail 1.3: replace with the expression in section 2.1, in words: "lift stroke + anchor allowance + guide allowance + max(nut length, ring nut-housing height) + 2 g_min (nut housing to anchor and to guide block)".
- S1-4 (checks_s1.py and gameplan l.231): FIX 2. With the correction, S1-4 is the exact feasibility test for L. As coded it checks a band 20 mm wider than the one K7 enforces.

## 3. S1-5b reference (Engineer open item 8)

The Designer's 142.00 is correct. The Engineer's 148.75 is the right arithmetic against an incomplete drawing.

Collar stack (params, z_A):

| Part | z_A |
|---|---|
| holder bottom | 49.09 |
| holder tube top (holder.length 88) | 137.09 |
| flange (8) | to 145.09 |
| nut plate (8) | to 153.09, which is the wing-nut row z_max |
| collar ring (collar.top_above_plate 6.75, collar.od 152.4) | to stop.collar_top_z 159.84 |

The holder row stops at holder_bottom + holder.length = 137.09. The holder's shape note draws a "collar ring on top", but no row's z_rule reaches 159.84. The part params name as the highest clamped base feature (test_P18, the g_stop reference "collar top (wings included)") is therefore absent from K7, K9 and S1-5b.

In plan, the bearing bore r 76.2 sits over the collar OD r 76.2, so the vertical gap governs: 301.84 - 159.84 = 142.00.

The drill head at capture_end sits 184.84 - 159.84 = 25.00 above the collar top. That is stop.g_stop by definition (params stop.height_z). Today the pair is tested only as undeclared F against the wing nut, at 31.75.

## 4. LF-16 (task 3)

- **Lint**, `sketch_common.plane_agreement_issues`: for each of load_plane and entry_plane, the stack term against the feature edge + offset, |d| <= TOL_Z 0.05.
  - Reads spec stack z, so it holds on the stub.
  - core_seat z_max = receiver_floor 40 + collet.core_seat_height 2.5 = 42.50 against the leaf collet.core_stop_z 42.5. The lint compares a geometric expression with the leaf, so it is not a tautology.
- **K6-Z3** (MEASURED, direct call): [] (clean).
- **K6-B5** (MEASURED): "LF-16 load_plane: term core_stop 42.50 z_A vs wingnut.z_max + offset 159.84 z_A, 117.34 apart". Fires on its reason; matches the manifest substrings.
- **entry_plane mutation** (MEASURED, scratch, not in the manifest): term collar_top with feature core_seat gives "LF-16 entry_plane: term collar_top 159.84 z_A vs core_seat.z_max + offset 42.50 z_A, 117.34 apart". The lint covers the second field; no control does (NOTE 1).

## 5. LF-9 (task 4)

The header `k7_tolerance` and comment match `judge` and `_assess_pair`:
- G: area <= 0.01 and distance >= g_min - 0.05.
- C: distance <= 0.05 and area <= 0.01.
- F: area <= 0.01.
- Depth-separated G: band gap >= g_min - 0.05.

The header does not yet state the plan-separated clause of `assess_pair`:
- F passes when the plan gap > 0.05. This is stricter than the XZ F rule.
- G passes when max(plan gap, projected distance) >= g_min - 0.05.

That clause goes in with the K7 ruling (FIX 4c).

## 6. K7 plan-footprint lower bound (Engineer open item 1): KEEP

**Basis.** Orthogonal projection onto XY is 1-Lipschitz, so the 3D distance between two parts is at least the distance between their plan projections. That is at least the distance between any two plan polygons containing those projections. This is the same argument LF-1 used for the depth bands, one axis over. The rule is sound exactly when every footprint contains its part's plan projection over the row's full z extent. C pairs are not relieved (`assess_pair` returns before the plan test for C); correct.

**Controls (MEASURED, direct calls on the builders):**

| Control | Result |
|---|---|
| K7-Z8 | plan-separated, 0 issues |
| K7-Z9 | undeclared: plan-separated, 0 issues |
| K7-B11 | 1 issue |

**Footprint containment, checked row by row (HAND):**

| Row | Footprint | Contains the part |
|---|---|---|
| drill_tube, drill_head, gear, gear_hub, bearing, ring | circumscribed 128-gon on the depth or place radius | yes (reads at most 0.01 low, conservative) |
| nut_housing, nut, screw | 128-gon r 25 / 21 / 4 | yes |
| descent_stop, motor23, motor_mount, guide_lug | radial rectangle | yes, except the NEMA 23 shaft (NOTE 3) |
| pinion_a, _b | radial rectangle r_in = pinion.r_toe 96.54 | **no**: r_toe is the toe pitch point. The toe tooth tip lies inboard along the back cone by addendum x sin(pinion.pitch_angle) = 4.1667 x 0.31623 = 1.32, at r 95.22 |
| liftmotor_a, _b | 128-gon r = liftmotor.body / 2 = 21 | **no**: the NEMA 17 body is a 42 square, circumradius 21 sqrt 2 = 29.70; corners outside by 8.70 |
| anchor, guide blocks | 128-gon r = jackscrew.nut_flange_od / 2 = 21 | by declaration only: the block has no plan dimension of its own (NOTE 5) |

**Effect on the nine relieved pairs (HAND):**

| Pair | Engineer plan gap | True plan gap | State |
|---|---|---|---|
| drill_tube\|pinion | 20.32 | 95.22 - 76.2 = 19.02 | F, unchanged |
| gear_hub\|pinion | 6.52 | 95.22 - 90 = 5.22 | F, unchanged |
| motor_mount\|pinion | 2.00 | 142 - 140 = 2.00 | F, unchanged |
| nut\|descent_stop | 13.99 | 195 - 181 = 14.00 | F, unchanged |
| nut_housing\|descent_stop | 9.99 | 195 - 185 = 10.00 | G 10, passes on the 0.05 tolerance (NOTE 4) |
| gear swept\|guide | about 12.68 | 139 - 126.32 = 12.68 | G 10, unchanged |

None of the nine pairs changes state. No relieved pair involves the lift motor. The containment defects still go in before (d), because a later pair would be relieved on an undersized footprint (FIX 4).

## 7. Placement of new and changed rows (task 5)

check_stack x and y extents against HAND, all within 0.01:

| Row | theta, r, half-width | x (HAND) | y (HAND) |
|---|---|---|---|
| pinion_a | 210, r 96.54 to 140, w 45.62 | r cos: -83.60 to -121.24, +/- 22.81 = [-144.05, -60.80] | -48.27 to -70.00, +/- 39.51 = [-109.51, -8.76] |
| motor23_a | 210, r 142 to 218, w 28.5 | [-203.04, -108.73] | [-133.68, -46.32] |
| descent_stop | 150, r 195 to 215, w 30 | -168.87 to -186.19, +/- 15 = [-201.20, -153.87] | 97.5 to 107.5, +/- 25.98 = [71.52, 133.48] |
| nut_housing_a | 150, r 160, w 25 | -138.56 +/- 25 | 80 +/- 25 |
| anchor_a, guide_a, nut_a, liftmotor_a | 150, r 160, w 21 | -138.56 +/- 21 | 80 +/- 21 |

S1-6 projection fields:
- screw_a (theta 150): x = 160 cos 150 = -138.56; depth centre 160 sin 150 = 80.00.
- screw_b (theta 30): x = +138.56; depth 80.00.
- The third screw (270) projects to x 0, depth -160 and is not drawn. The spec states two.

Side signs: motor23_a cos 210 < 0 (sign -1) and motor23_b cos 330 > 0 (sign +1) agree with the place theta.

Clearances checked by hand, all clear:

| Pair | Plan gap |
|---|---|
| ring \| guide rods | 220 - 210 = 10 |
| motor23_a \| guide rod at 180 | 230 sin 30 - 28.5 - 10 = 76.5 |
| pinion_a \| guide block at 150 | 73.4 |
| gear \| screws | 160 - 4 - 126.32 = 29.68 |

**Pose-restricted N declarations (Engineer open item 7).** The cause is `sketch_common.k7` l.944. A declaration enters `declared` for every pose, so the undeclared-F pass (l.975) skips the pair at poses outside its `poses` list. core_750|drill_head and core_750|drill_tube are declared N at capture_end only, and go untested at:

| Pose | Gap (HAND) |
|---|---|
| start | tip 834.84 - core top 792.50 = 42.34 |
| load | tip 959.84 - core top 851.17 = 108.67 |

The start gap is the cutter-to-core clearance at the top of travel. Nothing else in K7 or S1-x measures it. A two-line change closes it: key `declared` by pose, honouring `nb["poses"]` (FIX 3).

## 8. Findings

### FIX

1. **S1-5b reference / missing collar row.**
   - Add row `collar`: kind cylinder, axis Z, projection rectangle, keys [collar.od, collar.top_above_plate, stop.collar_top_z]; z_rule {z_min: "collar_top - collar.top_above_plate", z_max: collar_top}; depth +/- collar.od / 2; moves false.
   - Add `{id: collar, class: G, g_min: 10, poses: [capture_end], group: S1-5b}` to neighbour group s1_5b_base.
   - Declare N with holder, wingnut and core_750.
   - Declare drill_head|collar G stop.g_stop 25 at capture_end (params stop.height_z definition; HAND 25.00).
   - Set entry_plane to {term: collar_top, feature: collar, edge: z_max, offset: 0}.
   - Expected S1-5b least: 142.00 (bearing|collar).
   - Gameplan l.150: collar named in the base-part list.
2. **S1-4 band and screw length.**
   - checks_s1.s1_4: low = anchor z_max + g_min + max(nut_length, ring.nut_housing_height) / 2; high = guide z_min - g_min - max(...) / 2. Read g_min from the spec's nut_housing|anchor and nut_housing|guide neighbour (fixed_g10), not a literal.
   - Expected least margin: 0.84 (capture_end, low); park high 14.16.
   - Spec `screw_length`: one governing expression, "stroke + jackscrew.anchor_allowance + jackscrew.guide_allowance + max(jackscrew.nut_length, ring.nut_housing_height) + 2 * g_min" (885.00 / 885.00 / 1135.00). Keep "at anchor_z" as a reported line (885.84 / 885.84 / 1135.84). Drop the other two or mark them superseded with the reason in section 2.2.
   - Gameplan l.231 and l.284 per section 2.3.
   - The S1-4 B fixture at (c) is written against the corrected band.
3. **K7 pose-restricted declarations.**
   - `sketch_common.k7`: a neighbour with `poses` counts as declared only at those poses. Elsewhere the pair falls to the undeclared-F test.
   - Add a B control: capture core drawn into the drill head at start, which must fire "start/core_750|drill_head undeclared (F)".
   - Expected on the spec: start 42.34 and load 108.67 clear.
4. **Plan-footprint containment (condition of the KEEP ruling).**
   - (a) pinion_a/_b place r_in from the toe tooth tip, r_toe - (pinion.outer_diameter - pinion.pitch_diameter) / 2 x sin(pinion.pitch_angle) = 95.22. Use a new DERIVED overlay leaf or the expression in place.
   - (b) liftmotor_a/_b footprint containing the 42 square: half_width liftmotor.body / 2 x sqrt 2 (29.70) round, or a radial footprint with half_width body / 2 and r_in/r_out = pitch_radius -/+ body / 2.
   - (c) spec header `k7_tolerance` and gameplan l.140 add: "side views: an F pair passes when its plan footprints are > 0.05 apart; a G pair when max(plan gap, projected distance) >= g_min - 0.05 (plan-separated); footprints contain the part; C pairs are not relieved".
5. **Option R stop rule for the 1 m class puts the cutter inside the core at start.**
   - stop_1000 = 267.50 gives start 917.50 against a 1 m core top at 42.5 + 1000 = 1042.50: 125.00 inside the uncut core.
   - The stop rule needs the start-above-core term: stop_k = max(stop.height_z, collet.core_stop_z + L + stop.g_stop - drill.bore_ceiling_above_tip, collet.core_stop_z + L + c - upper.travel_max). Here c is the cutter clearance over the core top at the top of travel. Its value goes to the Designer or Sean; c = 0 is the geometric floor.
   - At c = 0: stop_1000 = 392.50, start 1042.50, capture advance 650 >= 534.93. Park (1209.84; the entry-plane term governs), stroke (1025.00) and L (1135.00 / 1140) are unchanged.
   - At 0.5 and 0.75 m the new term is -107.5 and 142.5 (c = 0), so stop stays 184.84, and the 0.75 m start keeps 42.34 over its core.
   - Edit the spec comment block, `park_rule.stop_k`, `park_rule.for_step4`, the Engineer section 4 note, and Designer section 4's "start = 917.5" before S-1 shows it to Sean.

### NOTE

1. K6-B5 plants only load_plane. Add K6-B6 for entry_plane. The scratch mutation above fires: "LF-16 entry_plane ... 117.34 apart".
2. LF-16 docstring: "term (read by the park rule) ... feature (read by S1-3)" is true of the pair of fields, not of each field. Each field's term and feature serve its own reader.
3. motor23 footprint (r 142 to 218) excludes the 8 x 21 shaft (r 121 to 142). The shaft lies inside the pinion footprint except r 140 to 142, and motor23|pinion is N. No pair is affected.
4. nut_housing|descent_stop: true plan gap 10.00 against g_min 10. The pass rests on the 0.05 tolerance and the 128-gon reads 9.99. Designer open item 6 (stop_pad_r_in 196) gives 1.00 of margin. Design value, his call.
5. Anchor and guide blocks take their plan footprint from jackscrew.nut_flange_od. The gear swept|guide relief (12.68) depends on that borrowed size, and the bracket arms (r 181 to 270) are not rows. S3 dimensions the blocks; the relief is re-checked there.
6. The spec `screw_length` uses a literal 10 for g_min. FIX 2 replaces it with the spec neighbour's g_min.

## 9. Gameplan lines (for the orchestrator)

| Line | Change |
|---|---|
| l.140 K7 | FIX 4c text; controls K7-Z8, K7-Z9, K7-B11 and the FIX 3 control |
| l.150 g_min seed | base parts include the holder collar ring (collar top 159.84 z_A) |
| l.231 S1-4 | "nut z +/- max(nut length, nut-housing height)/2 at least g_min (K7) clear of the anchor top and guide bottom" |
| l.233 S1-5b | Z value 142.00 (bearing to collar top) |
| l.284 detail 1.3 | L = lift stroke + anchor allowance + guide allowance + max(nut length, ring nut-housing height) + 2 g_min; 885.00 / 885.00 / 1135.00, buy 900 / 900 / 1140 |
| Design Notes 22 | "L_min 885.84" is the as-anchored value; the expression value is 885.00; option R stop_k gains the start-above-core term (FIX 5) |

## Verdict

NOT SIGNED. FIX 1 to 5 open. Re-check on `step1.1_engineer_spec_fixes.md`: hand values S1-5b 142.00, S1-4 least 0.84, 1 m start 1042.50 (c = 0), and the FIX 3 control firing.

Screw-length ruling: **L_min = lift stroke + anchor_allowance + guide_allowance + max(nut_length, ring.nut_housing_height) + 2 g_min** = 885.00 (stand-in), 1135.00 (plus 1 m); 885.84 / 1135.84 at the drawn anchor 265; buy 900 / 900 / 1140.

The Loftsman, 2026-11-25.

## Re-check after fix pass

Read: research/sean/cr_scratch/step1.1_engineer_spec_fixes.md and the revised s1_spec.yaml, proposed_params.yaml, check_stack.py, checks_s1.py, sketch_common.py (k7), fixtures/builders.py and manifest.yaml.

Runs (MEASURED, scratch, 2026-11-25):
- check_stack.py exit 0, with park 959.84 and stroke 775.00.
- New controls called directly on the builders.
- Pair distances read off the S1-FULL live drawing (`builders.s1_live`).

### Per finding

| ID | Hand | Measured | State |
|---|---|---|---|
| FIX 1 collar row | collar 159.84 - 6.75 = 153.09 to 159.84 z_A (213.09 to 219.84 z_S). S1-5b: 301.84 - 159.84 = 142.00. drill_head\|collar 184.84 - 159.84 = 25.00 = g_stop | collar z_S 213.09 to 219.84. S1-5b Z: "77 pairs, least certified clearance 142.00". S1-5b-B1 fires "bearing\|collar ... gap - g_min -1.000". head\|collar 25.000. entry_plane {collar_top, collar, z_max, 0}; K6-Z3 clean | **closed** |
| FIX 2 S1-4 and L | Band: 295 + 10 + 15 = 320 to 1135 - 10 - 15 = 1110. Margins: capture_end low 0.84, load and park high 14.16. L_min 775 + 30 + 30 + 30 + 20 = 885.00; 1 m 1135.00; at anchor 885.84 / 1135.84 | S1-4-Z "least margin 0.84". S1-4-B1 (guides 20 low: high 1115 - 10 - 15 = 1090; 1090 - 1095.84 = -5.84) fires 4, "high margin -5.84". check_stack L_min 885.0 / 885.0 / 1135.0, at anchor_z 885.84 / 885.84 / 1135.84. g_min read from spec neighbours (`screw_block_g_min`) | **closed** |
| FIX 3 pose-restricted N | core_750\|drill_head: start 834.84 - 792.50 = 42.34; load 959.84 - 851.17 = 108.67 | k7 builds `declared` per pose (l.940-948). Live pair_measure: start 42.340 (area 0); load 108.670 (area 0); core\|drill_tube at start 148.709. K7 live 0 issues. K7-B12 fires "start/core_750\|drill_head undeclared (F) ... overlap 1766.000" | **closed** |
| FIX 4a pinion footprint | see ruling below: 96.54 - 4.1665 x 0.31623 = 95.222 | place r_in 95.2224 | **closed** |
| FIX 4b lift motor | 21 sqrt 2 = 29.698 | half_width 29.6985 | **closed** |
| FIX 4c header | | `k7_tolerance` carries the plan-separated clause and the pose rule | **closed** (gameplan l.140 to the orchestrator) |
| NOTE 1 | | K6-B6 fires "LF-16 entry_plane: term collar_top 159.84 z_A vs core_seat.z_max + offset 42.50 z_A, 117.34 apart" | **closed** |
| NOTE 6 | | `screw_length` reads `g_min_screw_block`; no literal 10 | **closed** |
| FIX 5 1 m start | 917.50 - 1042.50 = -125.00 | check_stack `start_minus_core_top` 1 m -125.00 (0.5 m +292.34, 0.75 m +42.34) | **open, Sean at STOP S-1** (orchestrator ruling) |

### Pinion toe-tip ruling (95.22 against 95.29)

95.22 is right. The FIX 4a text formula in section 8 was wrong.
- The tooth tip sits one addendum m = 4.1667 from the toe pitch point, along the back cone.
- The back cone is perpendicular to the pitch-cone element, which is inclined at delta = 18.435 deg to the pinion axis.
- The tip's radial (drill-axis) displacement is therefore m sin delta = 1.318.
- (OD - PD) / 2 = m cos delta = 3.953 is the addendum's projection perpendicular to the pinion axis. Multiplying that by sin delta gives m cos delta sin delta = 1.250, which has no geometric meaning here.
- The spec expression `pinion.r_toe - pinion.pitch_diameter / pinion.tooth_count * sind(pinion.pitch_angle)` is m sin delta with m = 4.1665: 95.222.

### Consequences of the Designer fixes, checked

- **Descent pad** (stop_pad_r_in 200): nut_housing\|descent_stop 200 - 185 = 15.00 (MEASURED 14.993, 128-gon). NOTE 4 is closed by his value.
- **Frame members on the plate top:**
  - z_A 12 to 12 + 1213 = 1225, top 1285.00 z_S, unchanged.
  - Rods 12 to 1212 against guide.length 1200.
  - frame_upper\|base_frame is now undeclared F at 12.00.
  - New NOTE R1: gameplan l.280 S3-3 lists the chain "... base plate, base frame, anchor frame member ...", which needs base_frame\|frame_upper C. The axial loop now runs frame member to plate (C) and plate to frame (C). The l.280 chain order goes to the orchestrator as "... receiver, base plate, anchor frame member ...", with the base frame as the plate's support. That is the Designer's F4 call. S3-3 does not run before 1.3.
- **Pose-restricted declarations elsewhere:** the s1_5b_base G pairs, ring\|descent_stop C and drill_head\|collar G now take the undeclared-F test outside capture_end. K7 live is clean at 0 issues (MEASURED).

### FIX 5 options for Sean (geometry only)

- (a) Raise the 1 m stop to put the start at the core top: stop_1000 = core_stop + L + c - travel = 392.50 + c, start 1042.50 + c. Capture advance becomes 650 - c (>= 534.93 for c <= 115.07). Park 1209.84, stroke 1025.00 and L 1135.00 do not change.
- (b) Keep stop 267.50 and lengthen travel for the 1 m class to 775.00 + c (beyond the DN23 650). Or (c) drop the 1 m class from the supported Q9 options, which leaves park, stroke and L at the stand-in values.

### Verdict

SPEC SIGNED (Loftsman), pending Sean at STOP S-1 on FIX 5. FIX 1 to 4, NOTE 1 and NOTE 6 are closed. NOTE R1 (gameplan l.280 chain) goes to the orchestrator.

The Loftsman, 2026-11-25.
