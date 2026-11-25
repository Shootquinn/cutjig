## Corrections to the brief

1. The S2-2 computed value 52.779 is the 128-gon value at theta 30 and 150 only. At theta 270 the same evaluation gives 52.800. `sketch_common._ngon` puts vertices at (i + 0.5) x 2.8125 deg, so at 270 deg both polygons present edges to each other (edge-to-edge distance 52.80). At 30 and 150 they are out of phase (52.7786). The polygon bounds are 52.7677 (vertex to vertex) and 52.8000 (edge to edge). 52.779 falls inside them and errs low. MEASURED.
2. The S1 K7 label moves in Engineer Correction 6 (G 16 to 0, F 266 to 282, and the rest) cannot be traced to pairs from the records. In `s1_checks_r4.json` and `wip/s1_checks_r5.json`, K7 `states` is a bare list of labels with no pair ids. The pair values in section 3 are hand values plus my own plan evaluation (check_stack and sketch_common footprints), made outside the record. NOTE 3.
3. The members' new seat is better supported than the shape text says. Member a or b over the end-member strip (x 202 to 262): 3256.89 of 3600 mm² at r 274, against 1951.89 at r 300 (r4). MEASURED, `overlap_area`.
4. Engineer section 1 says "No key, expression, class or row change" to s1_spec.yaml. The diff against the frozen r4 copy (`research/sean/cr_scratch/sketches/s1_spec.yaml`) confirms it for the r5 edits. Three other differences in the file are not from the Engineer at P2: the H5 park-rule text and the `symbols.c` block (P0), the collar gloss (P0, NOTE R2), and two header path strings. MEASURED (diff).

## 1 Hand values beside the Engineer's

All DERIVED by hand. Engineer values are from step1.2_engineer_spec.md sections 3 and 4.

| Quantity | Hand | Engineer | Agree |
|---|---|---|---|
| screw b, theta 30: (160 cos 30, 160 sin 30) | (138.564, 80.000) | (138.56, 80) | yes |
| screw a, theta 150 | (-138.564, 80.000) | (-138.56, 80) | yes |
| screw c, theta 270 | (0.000, -160.000) | (0, -160) | yes |
| spacing 150 - 30, 270 - 150, 390 - 270 | 120, 120, 120 | S2-1 within 0.000 | yes |
| pinion pitch points at r_heel 125 (pinion c 90, a 210, b 330) | (0, 125); (-108.253, -62.500); (108.253, -62.500) | n/a (S2-3 not drawn) | n/a |
| S2-3: r_heel minus gear pitch radius 250 / 2 | 125 - 125 = 0.00 | not drawn | identity |
| pinion r_in: 96.54 - (83.33 / 20) sin 18.435 | 96.54 - 1.318 = 95.22 | 95.22 | yes |
| S2-2: 160 - 21 - 86.2 | **52.80** | 52.779 (128-gon) / 52.80 drawn extents | yes (Correction 1) |
| screw rod to keep-out: 160 - 4 - 86.2 | 69.80 | 69.78 | yes (polygon) |
| member c outer face: 274 + 30 against the plate edge 304 | 0.00 | 0.00 | yes (identity) |
| member c in the notch: sides 35 - 30; inboard (304 - 65) to 244 | 5.00; 5.00 | 5.000 | yes |
| member c length: foot z_A 0 (rail top = datum A), top 1165 + 60 | 1225; members a, b 12 + 1213 = 1225 | 1225 | yes |
| members a, b, x extent: 244 cos 30 - 30 sin 30 to 304 cos 30 + 30 sin 30 | 196.31 to 278.27 | 196.31 to 278.27 | yes |
| members a, b, y band: 244 sin 30 - 30 cos 30 to 304 sin 30 + 30 cos 30 | 96.02 to 177.98 | 96.02 to 177.98 | yes |
| members a, b, x centre: 274 cos 30 | ±237.29 | ±237.29 | yes |
| arms: r 181 (160 + 21) to 244 (274 - 30) | 63 long, r_c 212.50 | r 181 to 244, 212.50 | yes |
| arm b centre (212.5 cos 30, 212.5 sin 30) | (184.03, 106.25) | (184.03, 106.25) | yes |
| arm b x: 181 cos 30 - 15 to 244 cos 30 + 15 | 141.75 to 226.31 | 141.75 to 226.31 | yes |
| arm b y: 181 sin 30 - 25.98 to 244 sin 30 + 25.98 | 64.52 to 147.98 | 64.52 to 147.98 | yes |
| pad and post at 150: r 200 to 215, half-width 30; y band | 74.02 to 133.48, on an arm r 181 to 244 | 74.02 to 133.48 | yes |
| ring rim to member face: 244 - 210 | 34.00 | 34.000 (c), 33.944 (a, b; 128-gon) | yes |
| ring rim to guide rod: 230 - 10 - 210 | 10.00 | 10.000 | yes (identity, G 10) |
| gear OD to guide block: 160 - 21 - 126.32 | 12.68 | 12.659 / 12.680 (polygon, MEASURED by me) | yes |
| nut housing to pad: 200 - (160 + 25) | 15.00 | 14.993 (MEASURED by me) | yes |

S2-5a sector boundary (apex at the axis, edges at 45 and 135 deg, r 400). The distance from a point at polar (rho, phi) to the edge at 135 deg is rho sin(phi - 135):

| Nearest part of each class (theta 150 side; theta 30 mirrors it) | Hand | Engineer |
|---|---|---|
| lift motor, circumscribing circle r 29.70: 160 sin 15 - 29.70 | 41.41 - 29.70 = **11.71** | 11.71 |
| screw rod, r 4: 41.41 - 4 | 37.41 | n/a |
| anchor or guide block, r 21: 41.41 - 21 | 20.41 | 20.41 |
| arm corner (u 181, v -30): rho 183.47, phi 140.59 | 17.87 | 17.87 |
| pad corner (u 200, v -30): rho 202.24, phi 141.47 | 22.79 | 22.79 |
| member corner (u 244, v -30): rho 245.84, phi 142.99 | 34.17 | n/a |
| NEMA 23 at 90 (motor23_c), and mount, pinion and shaft c | inside the sector by construction; S2-5b relief, bearing bottom 1076.84 against hand band 940: 136.84 | 136.84 |

## 2 Shared rows: ruling

The 43 shared rows have string-equal `place` and `z_rule` expressions, keepout aside. Both specs read one overlay and one params.yaml through one `check_stack.evaluate_spec`. **The S1/S2 footprint agreement is therefore an identity of the evaluation.** No numeric cross-sketch footprint comparison is needed. Each drawing is held to its own footprint by K8 projected_extent in its own sketch.

The identity rests on one premise: the expressions stay string-equal. Nothing checks that premise today. One revision that edits a `place` in one spec and not the other breaks the agreement silently, and both sketches still pass their own K8. The rule needs its premise check (detail 1 common (h); my 1.1 position that a relief is only as good as its premise check). Specification, for 1.2 (c):

- **X1 shared-row lint** (check_sketch.py, run on every sN run and on --stale): for every row id present in two or more specs under docs/sketches/, compare `place` (r_in, r_out, theta, half_width, footprint, rot) and `z_rule` (z_min, z_max) after whitespace normalisation. The lint fails on any difference. A row that has `place` in one spec and none in the other is skipped and listed (today: keepout). A declared `x1_exempt: {reason}` on the row also passes it.
- X1-Z: live s1_spec.yaml with s2_spec.yaml, which reads clean: 43 rows compared, 1 skipped (keepout).
- X1-B1: a fixture copy of s2_spec.yaml with frame_upper_b `r_in` changed to `frame_upper.radius - profile.width / 2 + 1`. It must fire, naming frame_upper_b and `place.r_in`.
- X1-B2: a fixture copy with nut_a `z_rule.z_max` changed. It must fire on `z_rule`.

Shape, kind and projection may differ between views and are left out of the lint.

## 3 S1 r5: rows, pairs, values, spec-edit ruling

Key changed: `frame_upper.radius` 300 to 274. S1 rows that read it: frame_upper_a, frame_upper_b, bracket_anchor_a, bracket_anchor_b, bracket_guide_a, bracket_guide_b. No other S1 row reads it (grep of s1_spec.yaml).

| Row | r4 | r5 (hand) |
|---|---|---|
| frame_upper_a, _b | r 270 to 330, x ±(218.83 to 300.79), y 109.02 to 190.98 | r 244 to 304, x ±(196.31 to 278.27), y 96.02 to 177.98 |
| bracket_anchor_x, bracket_guide_x | r 181 to 270 (89), x ±(141.75 to 248.83), y 64.52 to 160.98 | r 181 to 244 (63), x ±(141.75 to 226.31), y 64.52 to 147.98 |

K7 pairs that move (S1, r5 hand values; every one passes):

| Pair | Class | r4 | r5 | Basis |
|---|---|---|---|---|
| bracket_x / frame_upper_x | C plan-contact | faces at r 270 | faces at r 244, full 60 x 60 face, overlap 0 | identity: arm r_out = member r_in, equal half-widths, same theta |
| ring / frame_upper_a, _b (fixed_g10) | G 10 | XZ gap 8.83 (218.83 - 210) plus plan 60 | **XZ overlap 13.69** (196.31 < 210), depth bands overlap; passes plan-separated at 34.00 (33.94 polygon) | ring depth-band disk r 210 against the member true square |
| nut_housing_a, _b / frame_upper_a, _b | G 10 | 85.00 | 59.00 | 244 - 185 |
| nut_a, _b / frame_upper | F (undeclared) | 89.00 | 63.00 | 244 - 181 |
| descent_stop, post / frame_upper_a | F | 55.00 | 29.00 | 244 - 215, same azimuth |
| liftmotor_x / frame_upper_x | F | 80.30 | 54.30 | 244 - 189.70 |
| ring, bearing, pinions, motors / bracket_guide_x | G 10 | z 33.16 at park (1135 - 1101.84 z_A) | unchanged (r_in 181 and z unchanged) | z band |
| guide_member / frame_upper_b (rod at 0, member at 30) | F | > 100 | 86.09 (rod surface to member corner (226.31, 96.02)) | plan |

Depth bands that move: the members (13 toward the axis) and the arms (outer end 13 inward). S1 margins S1-1 to S1-7 do not read the key. The preview reads them unchanged (650.00, 125.00, 367.34 / 117.34, 0.84, 192.34, 142.00, 607.66), and I agree: no S1-x rule reads `frame_upper.radius`.

**Bracket-arm shape strings reading "r 244": they stand.** A shape string is the representative-shape note M1 reads against the drawing. The r5 drawing puts the member face at r 244 (274 - 30). A frozen "r 270" would describe a part the r5 PNG does not show, which is the class of mismatch that cost S1 r3. The edit changes no key, expression, class, neighbour or row, and both numbers (244, 63) check by hand. The edit is text that describes the drawn geometry, inside the r5 change. It needs no Sean decision. The Designer owns the wording at P3a. NOTE 1 covers the echo risk.

**Does S1 r5 need spec edits beyond comments? Yes (FIX 1).** The shape strings are not the reason. S2 adds parts that S1 r5 has no row or not_drawn entry for. S1 shares the guide-lug rows with S2 and disagrees with S2 about them:

- S2 draws `guide_bushing_a/_b`, LM20UU housings of d 40 that hang 30 below the ring underside (284.84 to 314.84 z_A at capture_end, x ±210 to 250, MEASURED stack). S2 also gives guide_lug_x a C neighbour on the housing. The S1 guide_lug_a/_b shape reads "with linear bushing ... ring thickness", and S1 draws no housing. In the S1 side view the housing is the lowest ring-mounted part at x ±210 to 250 at capture_end. The S1 r5 header comment is the only record of the omission. A comment is neither a row nor a not_drawn entry (detail 1 common (b)), and s1_spec.yaml has no not_drawn field.
- The same applies to `guide_tie_a/_b` (z 1212 to 1272, or wherever the Designer moves them at P3a), which show in the S1 side view at x 200 to 267.

If the housings become S1 rows, S1-5b's measured least moves. housing_b to collar: z gap 314.84 - 30 - 159.84 = 125.00; plan gap 230 - 20 - 76.20 = 133.80; certified max = 133.80. The wing-nut sweep r 115 gives a plan gap of 95.00 and a z gap of at least 125.00. The S1-5b least therefore falls from 142.00 to between 125.00 and 133.80 (DERIVED), still well over g_min 10. Against anchor arm b (z 265 to 295 z_A), the z bands overlap by 10.16 and the plan gap is 64.995 (MEASURED by me), so the pair passes plan-separated.

## 4 Footprints: containment and true sections

| Row(s) | Footprint | Contains the part | True section (plan-contact claimable) |
|---|---|---|---|
| frame_upper_a, _b, _c | radial square r R ∓ 30, half-width 30, rot 0 | yes | yes (60 x 60, one face toward the axis, ASSUMED) |
| bracket_anchor_x, bracket_guide_x | radial r 181 to 244, half-width 30 | yes | yes |
| anchor_x, guide_x, nut_x | round r 21 | yes | yes (128-gon) |
| nut_housing_x | round r 25 | yes | yes |
| screw_x | round r 4 | yes | yes |
| liftmotor_x | round r 29.70 about a 42 square | yes (circumscribing) | no; F and G relief only. No C is claimed on it in S2 (MEASURED: neighbours are G 10 and S2-a G 0) |
| descent_stop, post | radial r 200 to 215, half-width 30 | yes | yes |
| motor_mount_x, motor23_x, motor_shaft_x | radial, half-width 28.5 / 28.5 / 4 | yes | yes (square body, round shaft drawn as a rectangle in plan, which is the true plan of a radial cylinder) |
| pinion_x | radial r 95.22 to 140, half-width 45.62 about a trapezoid | yes | no (trapezoid inside a rectangle); F and G only |
| guide_lug_x | radial r 210 to 250, half-width 20 | yes | yes |
| guide_bushing_x, guide_member(_b) | round r 20 / r 10 at r 230 | yes | yes |
| ring, bearing, gear, gear_hub, drill_tube | depth-band disk r 210 / 100 / 126.32 / 90 / 76.20 | yes (containment bound) | no; Engineer open item 4d (annuli) |
| base_plate | five convex pieces, the 644 x 608 plate less two 70 x 65 notches | yes (holes are void rows) | yes |
| base_frame | six convex strips (rails, end members, supports) | yes | yes |
| guide_tie_x | strip of half-width 30 from rod centre to member centre | yes for the span; the ends overlap rod and member (Designer, P3a) | as a strip |

No footprint fails containment. The `plan_poly` and `sector` evaluators (`plan_poly_pieces`, `strip_corners`, `sector_record`) agree with hand values. The strip normal is (-dy, dx) / L x w. The sector extents are ±282.84 by 0 to 400, which includes the 90 deg vertex.

## 5 Swept K7 case in plan

For each `moves: true` row I took the outline at load (plan positions do not change with pose) against every fixed row whose z band intersects the sweep band, the min to max of z_S over the four poses, on spec z bands. MEASURED (check_stack + sketch_common footprints; script in the session temp dir, not of record).

- Every plan overlap with intersecting z is declared: N for screw/nut, screw/housing, screw/ring disk, rod/lug and rod/bushing; C for ring/descent_stop at capture_end only (558.27 mm²; hand ≈ 557.1 for the pad strip r 200 to 210 x 60 under the rim). No undeclared overlap.
- Least G distances: ring / guide rods **10.000** (identity, Engineer Correction 5), gear / guide blocks 12.659 (hand 12.68), nut_housing_a / pad 14.993 (hand 15.00), ring / members 33.944 to 34.000, gear / guide arms 54.646, nut housings / members 58.993, pinions / ties 64.531, bushings / anchor arms 64.995, NEMA 23 / ties 72.902.
- The plan C pairs that touch in z and overlap in plan (ring/pad, member feet on the plate and rail, mount/motor, lug/bushing) need the plan C rule that is LF-8's remainder (Engineer open item 4e). That is a 1.2 (c) rule, and it ships with its premise check under (h).

LF-8 status: the side-view box test is replaced, for the S2 rows, by true plan outlines on the spec z bands. It closes at (c) when the plan K7 C rule and the annulus form (4d) land.

## 6 NOTES

1. Shape text that quotes a value derived from a key is an echo site: "r 244" in four S1 arm strings and "r 250" in the S2 lug strings. Write the expression beside the number, for example "member face (frame_upper.radius - profile.width / 2, r 244)", so M1 can see the source. No change required at (b).
2. The member tops are two independent DERIVED leaves: `frame_upper.member_length` 1213 (from z_A 12) and `member_length_rail` 1225 (from z_A 0). Both are meant to end at `jackscrew.top_guide_z` + `profile.height` = 1225. A change to top_guide_z moves neither. Add a `stack_ties` entry (frame_upper_a z_max = frame_upper_c z_max = bracket_guide_a z_max + profile.height) at (c). The K6 tie lint already exists.
3. The K7 record keeps labels only. Write the pair ids beside each state in sN_checks_rk.json so that a revision diff names the pairs that moved (Correction 2). 1.2 (c) harness item, for the Software Engineer.
4. Tray relief (params `tray.relief` [72, 19], y 241 to 260, x ±36; tray width 520): member c's inner face at y -244 sits 3.00 outboard of the relief's inner edge (241), with 6.00 each side in x. DERIVED. S2 does not draw the tray. Member c stands at Quinn's -Y column site, which is what the notch and relief were cut for. For the Step 2 frame row, not S2.
5. Pre-existing at r4: the bracket arm rows are "30-6060 stub, 60 wide" and 30 tall (265 to 295, 1135 to 1165 z_A). A 30-6060 section is 60 x 60 (`profile.height` 60, VERIFIED). Either the arm is not a 30-6060 piece or it is 60 tall. This belongs with LF1.1-9 to -11 at Step 2 and S3 (blocks, mounts). r5 does not change it.
6. Side view r5: the member's projected x (196.31) now lies 13.69 inside the ring rim (210), against 8.83 outside at r4, and the arm reaches x 226.31. The drawing needs draw order and dashing so the member reads behind or in front of the ring. Flag for P6 and the r5 M1.
7. Guide tie z is left to the Designer (P3a). Section 5 shows tie/pinion 64.53 and tie/NEMA 23 72.90 on the current z band. A tie moved to 1165 to 1225 z_A (1225 to 1285 z_S) stays above every swept part: the motor top at park is 1242.34 z_S, so the band intersects and the plan gap governs (72.90 ≥ 10).

## Verdict

**FIX** (1 item). The S2 arithmetic and placement check by hand, and the shared-row identity holds (X1 lint to land at (c)). The S1 r5 bracket shape strings stand.

1. **S1 r5 spec, guide_lug_a/_b, guide_bushing_a/_b, guide_tie_a/_b.** S1 r5 needs a spec change beyond comments, which is Sean's decision mid-step (stop table, "P3b rules a spec change to S1 beyond comments"). Options:
   - **A (recommended for the housings):** add guide_bushing_a/_b to s1_spec.yaml as rows with the S2 `place` and `z_rule` expressions (the X1 lint then covers them), with neighbours `use: s1_5b_base` and `fixed_g10` and the lug C. Change the S1 guide_lug shape to name the housing row. S1-5b's least moves from 142.00 to between 125.00 and 133.80 (DERIVED). The gameplan S1-5b reference and N1 text move with it.
   - **B:** add a `not_drawn` field to s1_spec.yaml with entries for guide_bushing_a/_b and guide_tie_a/_b, reason "drawn in S2 (plan); S1 r5 side view omits", and drop "with linear bushing" from the S1 lug shape. S1-5b stays 142.00 and does not cover the lowest ring-mounted part.
   - Ties: B until the Designer fixes their z at P3a, then A or B by the same rule.

## Gameplan lines to change

**l.248** (detail 1.2 Spec line), fragment:

Old:
```
S1 ids kept for the 43 shared rows, same place expressions;
```
New:
```
S1 ids kept for the 43 shared rows, same place and z_rule expressions (footprint agreement is an identity of check_stack; its premise is held by the X1 shared-row lint, 1.2 (c), Loftsman 1.2 (b));
```

**K table** (after the K9 row, l.142 region): insert a row:
```
| X1 | Shared rows (1.2): for every row id in two or more specs, `place` and `z_rule` expressions equal after whitespace normalisation; a row placed in one spec only is skipped and listed; `x1_exempt: {reason}` passes a declared difference | Live s1 + s2 specs (43 compared, keepout skipped) | B1 s2 frame_upper_b r_in + 1; B2 s2 nut_a z_max changed |
```

**l.234** (S1-5b row) and **N1** (l.707): only if Sean adopts FIX 1 option A. Replace the S1-5b reference value 142.00 with the value the r5 run measures, expected between 125.00 and 133.80 (housing|collar or housing|wing-nut sweep). Exact text follows the r5 record.

**Echo Site Registry**, after the "Bracket arms r 181 to 244" row the Engineer proposed, insert:
```
| Member tops **1225 z_A** (members a, b: 12 + frame_upper.member_length 1213; member c: 0 + frame_upper.member_length_rail 1225) = jackscrew.top_guide_z 1165 + profile.height 60 | overlay frame_upper.member_length, frame_upper.member_length_rail, jackscrew.top_guide_z | DERIVED (stack tie at 1.2 (c), Loftsman 1.2 (b) NOTE 2) |
```
