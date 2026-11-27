# Step 1.4 P5L, The Loftsman: 1.4 (c) coordinates, S4-1 / S4-2 fixtures, X1 section_true

Verdict: **Item 1 PASS, item 2 PASS, item 3 PASS. FIX 0.** SIGNED:
- X1 `section_true` compare, form (i).
- S4-2 changes for N3 and N4: a carrier that is not drawn is an (a) issue, and the (b) datum is the wingnut `plate` piece.

The fixture state is confirmed: the P6 staged edits close the 8.75 holder and 0.75 collar K6 offsets (section 4).

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\open14\p5l\`. The scripts are `p5l_check.py` and `p5l_b.py`; the results are in `p5l_out.json`. The scripts import the live harness and fixtures and write nothing under docs/.

## Corrections to the brief

1. **The staged P6 X1 set compares 71 shared rows, not 70.** The staged s1 and s3 add a `washer` row, so `section_true` is compared on 7 rows: the six base rows and the washer. The set passes (MEASURED). My P3b Correction 4 count of 70 predates the washer row.
2. **The staged `step1.4_p6_staged/s4_spec.yaml` is stale against the live s4.** It lacks every P4 spec edit (MEASURED):
   - `exposure.datum_piece` is absent (0 occurrences in the staged file, 1 in the live file);
   - the marks `sub: line` and the P4 not_drawn omit forms are absent (0 occurrences against 8);
   - the base-row `collet.slits` differs (form (a)).

   On the six base rows, the staged s4 equals the live s4 after `p6_state` in every field except `collet.slits`. Its X1 fields and its `section_true` are equal. At P6, the s4 side of the save point must apply `x1_edits_at_p6` to the live s4. Copying the staged s4 over it would revert P4. The staged s1 and s3 copies are the ones to land.

## 1 S4-1 B and S4-2 B per branch: planted value against the hand value

Hand values are from my P3b sections 1a and 3 (DERIVED). Code values are from `checks_s4` run on the fixture builders (MEASURED).

| Control | Planted | Hand | Code reason / measured | Verdict |
|---|---|---|---|---|
| S4-1-Z | live (P6 state) | 159.84 | "collar top 159.84 z_A = stop.collar_top_z 159.84; drawn top equal in every figure" | PASS |
| S4-1-B1 | holder.flange_thickness 0 | 159.84 - 8.00 = 151.84 | "collar top by the test_P18 formula 151.840 vs stop.collar_top_z 159.840", measured 151.84, cause content | PASS |
| S4-2-Z | live, both figures | exposure 302.50 - 153.09 = 149.41, margin 6.29 | "least exposure margin 6.29" | PASS |
| S4-2-B1 | carrier row deleted; core on the seat, 42.50 to 142.50 | (a) carrier absent, core bottom minus seat top 0.00; (b) 142.50 - 153.09 = -10.59; both figures | 4 issues: "carrier not drawn ... 0.000" and "exposure -10.59 (core top 142.50 - nut-plate top 153.09)" in carrier and liner; cause content; measured -153.71 = -10.59 - 143.12 | PASS |
| S4-2-B2 | carrier.length 150 | 42.50 + 150 + 100 = 292.50; 292.50 - 153.09 = 139.41 < 143.12 | "exposure 139.41 (core top 292.50 ...)" x 2; measured -3.71 | PASS |
| S4-2-B3 | carrier bottom at 66.00 z_A, figure 1 | (a) 66.00 - 42.50 = 23.50; (c) 66.00 > 65.70 + 0.05 | "carrier bottom minus core_seat top 23.500"; "carrier drawn z [66.00, 202.50] does not cover the grip band [42.50, 65.70]" | PASS |

Notes on the table:
- On S4-1-B1, S4-2 reads margin 14.29 = 6.29 + 8.00. This is consistent: the nut plate drops with the flange.
- N3 is closed. B1 now returns cause content and matches on reason (`checks_s4.s4_2` l.165-166). The missing carrier is reported once, under (a); the (c) skip at l.184 covers it.
- N4 is closed. The datum reads `named_pieces(ax, "wingnut", "plate")` (spec `exposure.datum_piece: plate`). The drawn plate top is 153.09 z_A (213.09 z_S), and the sweep lines no longer enter the read.
- The ruled form matches my P3b section 3 premises (K d+1 is the highest plate; S4-1 and K6 enforce it).

## 2 Section coordinate map (u, z) on section_yz, by hand against the drawn fixture

Plane x = 0, viewer at +X, u = +Y. Since Y x Z = X toward the viewer, the frame is right-handed. Conversion: z_S = z_A + 60.00 (collar top 159.84 z_A to 219.84 z_S; MEASURED `to_shop_floor(0)` 60.00). Each `section_true` piece is drawn at +u, and its mirror at -u with the vertex order reversed, so both sides stay counter-clockwise. The read is the figure 1 (carrier) drawn polygons (MEASURED).

**Holder flange** (r 56.7502 to 72.04, z_A 137.09 to 145.09):
- Hand, +u: (56.75, 197.09), (72.04, 197.09), (72.04, 205.09), (56.75, 205.09) z_S.
- Hand, -u: (-56.75, 205.09), (-72.04, 205.09), (-72.04, 197.09), (-56.75, 197.09).
- Drawn: equal to 0.0001 on both sides.

**Receiver shoulder** (r 80 to 100, z_A 12 to 20):
- Hand, +u: (80, 72), (100, 72), (100, 80), (80, 80) z_S.
- Hand, -u: mirrored and reversed.
- Drawn: equal.

Also read, all equal to my P3b section 1 values:
- the holder cone (62.04 / 67.04 at 49.09; 56.7502 at 79.09);
- the collet cone (63.2909 at 41.995; 59.1111 at 65.6998);
- the receiver rim polygon (5 vertices);
- the wingnut plate (68.04 to 83.14, 146.39 to 153.09).

**Plane cut.** The wingnut `pocket_rim` is drawn at -u only, with centroid u -77.52 (MEASURED). This is the theta 90 washer window on +u (my P3b FIX 2; `plane_cuts`). Handedness holds: theta 90 maps to u = r sin 90 > 0.

K6 on the live fixture (P6 state): 33 z_rules match within 0.05 (MEASURED).

## 3 X1 section_true comparison (form (i))

**What it compares.** `check_sketch.x1_lint` l.313-326 runs on every row id present in two or more specs. For each such row that carries `section_true` in two or more specs, the `section_true` dicts are compared for equality after whitespace normalisation (`_x1_norm`, then sorted JSON). The issue names the differing piece keys. `section` is no longer compared: it is a view-specific renderer input. The fields X1_FIELDS (place, z_rule, plan_poly) are unchanged.

**Tolerance.** Zero: the compare is between expressions, as for z_rule. Equal values written as different expressions read as a difference. That is the intended strictness, since one expression gives one evaluation in every sketch. The fixture form is shown by X1-B4: r_out + 1 on the s3 holder flange fires "holder section_true.flange: s1 and s3 differ".

**Results (MEASURED):**

| Set | Result | Rows | section_true compared |
|---|---|---|---|
| live s1, s2, s3, s4 | pass | 70 | 0 (six base rows in s4 only, listed) |
| staged s1, s3 + live s2 + live s4 after p6_state | pass | 71 | 7 |
| staged s1, s3 + live s2 + live s4 as it stands | **fail**: holder z_rule.z_max, collar z_rule.z_min | 71 | 7 |
| live s1, s3 + live s2 + s4 after p6_state | **fail**: same two fields | 70 | 0 |

**Expected red on the holder until S1 r9.**
- Form (i) gives no red on the live set: the holder carries `section_true` in s4 only.
- The holder red the brief anticipates appears in three places:
  1. X1 z_rule (rows 3 and 4 of the table) whenever the edits land in one spec without the others;
  2. K6 8.75 on any figure that draws the true holder against the live z_rule (section 4);
  3. the presence rule O2 (ii) once it lands.
- All three clear together only when S1 r9 and S3 r8 land with the s4 edits in one save point. The Engineer's carry of O2 (ii) to P6 is correct.

## 4 Fixture P6 state and the K6 offsets

The Engineer's claim, measured with `p6_state` replaced by the identity (the fixture drawn to the live z_rule):
- "carrier/holder: drawn z [109.09, 213.84] vs stack [109.09, 205.09] z_S, off 8.75"
- "carrier/collar: drawn z [213.84, 219.84] vs stack [213.09, 219.84] z_S, off 0.75"
- the same two lines in the liner figure.

Hand (DERIVED):
- 153.84 - 145.09 = 8.75: washer proud 0.50 + nut plate 7.50 + lift_play 0.75.
- 153.84 - 153.09 = 0.75: nut.lift_play.

The P6 staged edits close it:

| Item | New expression | Hand value | Target |
|---|---|---|---|
| 1, holder z_max | 49.09 + 88 + 8 + 1.30 - 0.80 + 7.50 + 0.75 | 153.84 | tube top |
| 2, collar z_min | 159.84 - 6.00 | 153.84 | ring underside |
| 3, tie | 153.84 + collar.thickness 6.00 | 159.84 | collar top |

- With the edits applied (the fixture as committed), K6 passes on all 33 z_rules, and S4-1, S4-2 and S4-3 pass (MEASURED).
- The staged s1 and s3 carry the identical three expressions: holder z_max, collar z_min and the s1 tie offset `collar.thickness` (MEASURED). They also carry the FIX 3 relief and FIX 4 skirt in `wingnut.section_true`, equal to the live s4.
- X1 then passes on 71 rows with `section_true` equal on 7.
- The condition is Correction 2: P6 applies `x1_edits_at_p6` to the live s4, together with the staged s1 and s3. P6 does not copy the staged s4.

## 5 NOTES (no revision)

- N7. At P6, delete `x1_edits_at_p6` and the `p6_state` call in `s4_fixtures.s4_ctx` once the edits are in the live s4. `p6_state` asserts each Old text, so it raises on the edited spec. That raise is a guard and also a certain red on every S4 fixture after P6.
- N8. The tie `source` text differs between the staged s1 and s4 after p6_state. Ties are not X1-compared, so this has no effect.

## Gameplan lines to change

none
