# Step 1.4 P2, The Engineer: S4 spec (1.4 (b)), overlay, checks_s4 skeleton, S1 r9 / S3 r8 spec edits

## Corrections to the brief

1. **The S1/S3 holder edits change shared X1 fields, so they cannot land in one spec ahead of the others.** S4-b moves the holder `z_rule.z_max` (145.09 to 153.84, the tube top) and the collar `z_rule.z_min` (153.09 to 153.84), and the S1 `stack_ties.holder_flange` offset follows (DERIVED). X1 compares `z_rule` on every shared row; `s4_spec.yaml` joins the X1 glob the moment it exists (check_sketch.x1_lint, `s*_spec.yaml`). A live edit to s1_spec.yaml or s3_spec.yaml before P6 also changes the spec SHA-256 in the deps of the accepted S1 r8 and S3 r7 records, so `--stale` reads red, and it feeds the live-spec controls (K4-Z4, K9-Z2, S1-FULL, S3-FULL draw them). The 1.3 precedent applied the shared anchor-place edits at P6. Disposition: the S4 shared rows carry today's S1/S3 X1 fields (X1 pass, MEASURED). The three X1-field edits are in `s4_spec.yaml` `x1_edits_at_p6`. The full S1 r9 and S3 r8 edit set (22 and 20 edits) is staged as complete spec copies in `research/sean/cr_scratch/step1.4_p6_staged/`, with X1 run on the staged set (section 6). P6 applies the set to the live specs in one save point. Requirement 5 is delivered as staged spec text, and no live S1/S3 spec file was edited.
2. **S4 draws no core_750.** The Designer draws only the Q10 100 mm core (1.4 (a) section 10), so core_750 is not an S4 row and not a shared row of S4. The 0.75 m core and its stub are a not_drawn entry (owner S1) and a reported item.
3. **The rule (l) label anchors (requirement 5, second half) were not written.** The orchestrator note at save point 1 carries them to P6: S1 height_target and S2 slot_line_c under the L3 relief; S2 base_plate label_theta 5; S2 screw_b and S3 inset screw_b label_theta 28; S1 drill_tube frac 0.45 and guide_b frac 0.75 with the side-placer change; S2 keepout label_theta 355; TP1.4-2 wingnut sweep to a reference row in S1 r9 and S3 r8.
4. **The `section` field already differs today on three shared rows outside the base stack.** These are drill_tube (s1, s2 against s3), ring (s3 has none, it uses section_u) and gear (s1, s3 against s2) (MEASURED, `x1dry.py`). An X1 that compares `section` as it stands fires on these three before any S4 row. The true section therefore goes in a new field, `section_true`, with named pieces, and the ruled X1 extension compares that field (section 6, open item O2).
5. **Washer pocket radius.** Designer row wingnut: "washer pocket r 68.40 to 71.90". build_parts/nut.py profile: the pocket runs from the plate hole r 68.04 (nut.plate_hole_dia / 2) to r 71.90 (nut.washer_pocket_od / 2), 0.80 deep (DERIVED). The spec follows nut.py. The washer itself is r 68.40 to 71.60 (washer.id, washer.od).
6. **Collet foot-ring top 41.995 z_A, not 42.00.** cadlib.footring_derived: ring_top = holder.bottom_above_floor_Kmax - fit.model_contact_gap = 1.995 z_R (DERIVED). The spec uses the build_parts value. The cone at that height is r 63.2909 (63.29 at 42.00).
7. **The collet chamfer expression holds outside the chamfer band only.** collet_family.dims: c = chamfer_band_lo when room lies in (2.5, 3.5), else min(room, chamfer_cap). The spec writes min(room, collet.chamfer_cap). Room is 6.30 at d 100 and 3.80 at d 105 (DERIVED), both outside the band. The spec carries this as `section_true_note`.
8. **Liner figure: the carrier bears on 0.50 mm of the d 105 ledge.** Ledge r 50.00 to 53.00; carrier r 50.50; liner r 50.50 to 53.00 (DERIVED). The carrier bottom bears on the annulus r 50.00 to 50.50, and the liner carries the rest. This is open item O5 for the Designer.
9. **The -X wing of the wing nut lies past the signed beyond band.** The wing spans x -83.14 to -115 (wingnut.body_od / 2 to wingnut.span / 2). The section convention signed at 1.3 admits beyond parts only within 0 > x >= -profile.width (60), and K8-B74 enforces it. The spec declares the wing as sub-artist `wingnut:wing` with its x band, and the convention text names the conflict (open item O3, Topologist at (c)).
10. **s4_spec.yaml enters every S3 run's deps.** S3 has chains, so sym_lint reads every `s*_spec.yaml`, and the deps rule records each one in `spec_read`. The first full controls run after the S4 spec read Z 107/108: DEPS-Z2 fired with "deps spec_read [s1, s2, s4] against [s1, s2]" (MEASURED). The fixture hard-coded the 1.4 step 0 spec set. `step14_fixtures.deps_run_s3` now expects the set the rule names, every `s*_spec.yaml` but s3, read from the tree. DEPS family after the change: Z 4/4, B 13/13 (MEASURED). The accepted s3 r7 record's exemption deps list s1 and s2 only, and `--stale` recomputes the recorded files only, so `--stale` stays at 0 differences. S3 r8 will record s4_spec.yaml in its spec_read.
11. **The collet slit phase has no params leaf.** collet_family.build_solid: phi0 = receiver.key_offset_deg + 15.0, a literal 15 (DERIVED). Slit k sits at phi0 + 30 k, even k open at the top. The two ticks are k 2 (theta 112, top-open) and k 7 (theta 262, bottom-open), both behind the plane (x < 0), and they match the Designer's 2a. The spec writes `receiver.key_offset_deg + 15 + k * 360 / collet.slit_count`.

## 1 Overlay changes and the --stale list

`docs/sketches/proposed_params.yaml`, new block at the end (pre-edit copy: `D:\Unleashed Robotics\_scratch\cutjig\open14\p2\proposed_params.pre_p2.yaml`). Old value: none for every key (new leaves). No leaf shadows params.yaml (`Params.shadowed` = [], MEASURED).

| Key | New | Source | Status |
|---|---|---|---|
| core.length_short | 100 mm | critical path 4 (100 x 100 core); Designer 1.4 (a) row core_100; Design Notes 34 | ASSUMED |
| carrier.length | 160 mm | Designer 1.4 (a) sections 2, 6, 9; Design Notes 34 "D with C drawn" | ASSUMED |
| carrier.diameter | 101 mm, expr `core.diameter_nominal + collet.grip_window_hi` | Designer row carrier (K d+1) | DERIVED |
| carrier.material | nylon (PA6) rod, square ends | Designer row carrier; Design Notes 34 | ASSUMED |
| carrier.bond | gypsum or hot-melt bed, bond line, no stack height | Designer row carrier | ASSUMED |
| liner.od_offset | 5 mm | Designer section 8 (b), D = d + 5; Design Notes 34 | ASSUMED |
| liner.wall | 2.0 mm, expr `(liner.od_offset - core.tol) / 2` | Designer section 8 (b) | DERIVED |
| liner.collet_d | 105 mm, expr `core.diameter_nominal + liner.od_offset` | Designer sections 8, 10 | DERIVED |
| liner.material | PETG or card sleeve, cast-on, cut with each slice | Designer section 8 (b); batch 3 B3-3 | ASSUMED |

Every DERIVED leaf carries expr (K2 agreement within 0.05: 101, 2.0, 105, MEASURED through the loader).

`--stale` after the edit (MEASURED): 3 records checked, 0 differences; deps 3 records, 3 exempt, 0 differences. **Adopted-key list: empty.** No accepted record (s1 r8, s2 r9, s3 r7) reads any of the nine keys, and no params or overlay value read by a record moved.

## 2 Spec summary (`docs/sketches/s4_spec.yaml`)

View section_yz, section B-B: plane x = 0, viewer at +X looking toward -X, u = +Y, z_S plotted, the S3 plane and convention. Crop u -130 to 130, z_A -60 to 330. Two poses, both with the tip at stop.height_z 184.84: `carrier` (figure 1, `s4_base_section_r<k>.png`) and `liner` (figure 2, `s4_liner_section_r<k>.png`). Closes R10, R11 (as relative advance), R12; Q4, Q5, Q6, Q10.

**Rows: 19.**
- **Shared rows: 8.** floor, base_plate, receiver, collet, core_seat, holder, collar, wingnut, drill_head are shared with S1 and/or S3 (9 ids, floor counted). place, z_rule and plan_poly are copied verbatim from s3_spec.yaml.
- **S4-only rows: 10.** receiver_spigot, collet_105, core_seat_105, washer, carrier, core_100, liner, line_stop, line_kerf, line_min_core.

| Row | z_A (MEASURED, check_stack) | Section / form |
|---|---|---|
| floor | -60.00 | reference line |
| base_plate | 0 to 12.00 | cut, section_u -130 to -80.20 and 80.20 to 130 (break at the crop), plan_poly as S3 |
| receiver_spigot | 0 to 12.00 | r 40.00 to 80.00 |
| receiver | 12.00 to 128.50 | floor r 40 to 80 (12 to 40); wall r 67.29 to 80 (40 to 76.50); land r 67.29 to 72.29 (76.50 to 80.50); thread r 67.29 to 74.79 (80.50 to 127.25); rim polygon (lead-in 1.25 to r 73.54, register chamfer 1.0); shoulder r 80 to 100 (12 to 20); root lines r 72.29 over 80.50 to 128.50 |
| collet (carrier) | 40.00 to 72.00 | foot r 50.50 to 66.99 (40 to 41.995); cone polygon r 63.2909 to 59.1111 over 41.995 to 65.70, bore r 50.50; top polygon to r 58.00 / 56.80 at 72.00 |
| core_seat (carrier) | 40.00 to 42.50 | r 47.50 to 50.50 |
| collet_105 (liner) | 40.00 to 72.00 | foot r 53.00 to 66.99; cone r 63.2909 to 58.6703 over 41.995 to 68.20; top to 58.00 / 56.80 |
| core_seat_105 (liner) | 40.00 to 42.50 | r 50.00 to 53.00 |
| holder | 49.09 to 145.09 (153.84 at P6) | cone polygon r 62.04 to 56.75 over 49.09 to 79.09, OD r 67.04; tube 79.09 to 137.09; flange r 72.04 to 145.09; neck r 56.75 to 67.04 to 153.84 |
| collar | 153.09 to 159.84 (153.84 at P6) | ring r 55.00 to 76.20, 153.84 to 159.84 |
| wingnut | 97.09 to 153.09 | body r 74.79 to 83.14 (97.09 to 145.59); pocket rim r 71.90 to 83.14 (to 146.39); plate r 68.04 to 83.14 (to 153.09); skirt r 83.14 to 95.14 (102.09 to 111.09); sub-artists wing (beyond), sweep r 115 |
| washer | 145.09 to 146.39 | r 68.40 to 71.60 |
| carrier | 42.50 to 202.50 | unsectioned d 101; bond mark at 202.50 |
| core_100 | 202.50 to 302.50 | unsectioned d 101; chamfer mark at 299.50 |
| liner (liner) | 42.50 to 302.50 | r 50.50 to 53.00 |
| drill_head | 184.84 to 291.21 | unsectioned, as S3 |
| line_stop / line_kerf / line_min_core | 184.84 / 291.21 / 296.21 | reference lines |

**Neighbours: 39 declarations (S4-c as ruled).**
- G pairs: receiver|holder G 0.25; receiver_spigot|base_plate G 0.10; wingnut|holder G 0.50; collar|wingnut G 0.75; core and carrier against holder, collar and wing nut G 1.0; liner|holder G 0.5; liner|collar G 1.0; drill_head|collar G 25.
- C pairs: wingnut|receiver C on the drawn major cylinder r 74.79; collet foot|receiver floor (face 40.00); receiver|base_plate (face 12.00); core_seat|receiver; collet|holder (cone); collet|carrier (grip); holder|washer (flange top); washer|wingnut (class P in the source text); core_100|carrier; carrier|core_seat; the liner pairs.
- one_body: collet|core_seat, collar|holder, receiver_spigot|receiver.
- N: carrier, core_100 and liner against drill_head, with reasons: the core top is inside the drill bore, and the carrier top is 17.66 above the tip at the stop (second cut into the carrier, R12).
- Hand distances (DERIVED): 0.25, 0.20, 0.50 axial / 1.00 radial / 2.75 flange to body, 0.75, 6.25, 4.50, 17.54, 3.75, 2.00.

**Sense predicates: 21.** Existing forms:
- collet and collet_105: taper narrows up (`piece: cone`);
- carrier rests_on core_seat (core_seat_105 in the liner figure);
- core_100 rests_on carrier, above carrier;
- liner rests_on core_seat_105;
- collar clears_above holder (`of_piece: flange`);
- wingnut below drill_head, clears_above holder (`piece: pocket_rim`, `of_piece: flange`, +0.50);
- receiver below collet / collet_105 (`piece: floor`);
- drill_head above collar.

New forms, Topologist at (c):
- collet: vertical_edge on the cone piece's inner edge (S4-d), below holder (`piece: foot`), rests_on receiver (`seat_piece: floor`);
- washer: between holder flange and wing-nut plate;
- holder: taper narrows up on the inner edge of its cone piece.

**not_drawn: 12.** Base-frame rails (outside the crop); shoulder bolts; key slot, holder key, collet foot key (theta 37); holder inserts; witness ruler and flange tick; tommy bosses; +X wing (cut away); other slits; washer notch, pads, tab, windows; 0.75 m core (owner S1); rejected advance options A, B, E (owner Step 2); taller collet (owner Step 2). The figure_note names the head of each.

**part_list: 17 entries; reported_items: 10.**
- q10_core_top (drawing)
- q10_exposed (drawing)
- q10_min_on_stop
- grip_length (drawing)
- advance (option D, slices per core)
- carrier_torque
- q5_delta (collet length options with the collar-top move)
- liner_wall
- cut_case_seat (drawing)
- kept_axial

This covers the DC13 list. Rubric additions: 6 (V3 x3, V7 ticks, V10, handedness).

Further spec blocks:
- `s4_checks` S4-1, S4-2 (ruled form, per pose, grip_band expressions, expected values and B forms), S4-3.
- `x1_edits_at_p6` (3 items).
- New fields declared in the header for P4: section_true, piece / of_piece, vertical_edge, between, seat_piece, section_figures.

## 3 checks_s4.py skeleton (`docs/sketches/checks_s4.py`)

- `s4_1`: check_stack.collar_top_z_A (the test_P18 formula) against stop.collar_top_z within 0.01; the spec formula string evaluates equal to it; the drawn collar z_max (z_S to z_A once) within 0.05 in each figure.
- `s4_2`: per pose, (a) core on the carrier and the carrier on its seat within 0.05, (b) drawn core top minus the drawn wing-nut top >= core.min_exposed, (c) the grip member's drawn z extent covers grip_band.
- `s4_3`: section-Axes K8 issues restricted to the listed rows; untestable predicates read absent.
- `reported(ctx)`: every reported_items id. Arithmetic items come from the keys (slice_numbers, Q5 table, liner, torque). Drawing items read the drawn core_100 and wingnut and read None on no drawing.
- STUB_EXPECT guard [K1, K2, K3, K5, X1]; red [K4, K6, K7, K8, K9, S4-1, S4-2, S4-3, RPT]. STUB_CAUSE absent for K6, K7, K8, RPT, S4-1 to S4-3. SOURCES per check.

Smoke run on an empty figure set (MEASURED):
- S4-1, S4-2, S4-3 fail, cause absent ("section figure (pose carrier) not built").
- reported: q10_min_on_stop 253.71 / 260.46; advance least slice 76.44 axis / 56.02 surface, 0.75 m sliceable 496.29, 6 slices, stub 17.27 / 37.69; carrier_torque 50.9 / 6.37 kPa; q5_delta 159.84 / 184.84 / 209.84 with min core 253.71 / 278.71 / 303.71; liner_wall D = d + 5, wall 2.00.

## 4 Stack table (check_stack on s4_spec.yaml, beside the hand values)

| Item | check_stack z_A (MEASURED) | Hand value (DERIVED) | Hand arithmetic |
|---|---|---|---|
| Collar top | 159.840 (S4-1 formula, collar_top_z_A, collar z_max) | 159.84 | 40 + 13.626 - (13.126 - 8.59) + 88 + 8 + 8 + 6.75 = 159.84 = stop.collar_top_z |
| Holder bottom | 49.090 | 49.09 | 40 + 13.626 - 4.536 |
| Holder flange | 137.090 to 145.090 | 137.09 to 145.09 | 49.09 + 88; + 8 |
| Nut-plate top (wingnut z_max) | 153.090 | 153.09 | 159.84 - 6.75; = 145.09 + 0.50 washer proud + 7.50 nut.plate_thickness |
| Holder tube top / collar underside (P6 z_rule) | 153.840 | 153.84 | 153.09 + 0.75 nut.lift_play = 159.84 - 6.0 collar.thickness |
| 100 mm core top | 302.500 (on the carrier) | 302.50; 142.50 on the stop | 42.50 + 160 + 100; 42.50 + 100 (17.34 below the collar top) |
| Receiver floor | 40.000 (receiver floor piece top, collet z_min) | 40.00 | icd.floor_above_datum_a |
| Core stop | 42.500 | 42.50 | 40 + 2.5 |
| Minimum core top | 296.210 (line_min_core) | 296.21 | 153.09 + 143.12 = 291.209 + 5 |
| Exposure on the carrier | 149.41 (302.50 - 153.09) | 149.41, margin 6.29 | on the stop -10.59 |

Every hand value equals the check_stack value to 0.01. Section piece coordinates match the Designer's shape notes to 0.01, except the foot-ring top (Correction 6) and the pocket inner radius (Correction 5). Evaluation dump: `D:\Unleashed Robotics\_scratch\cutjig\open14\p2\evals4.json`.

## 5 S1 r9 and S3 r8 spec edits (staged; applied at P6)

Staged copies: `research/sean/cr_scratch/step1.4_p6_staged/s1_spec.yaml`, `s3_spec.yaml`, `s4_spec.yaml` (s4 with `x1_edits_at_p6` applied), and the generator `stage.py`. Every edit asserts a unique Old match. The exact Old/New pairs are in `D:\Unleashed Robotics\_scratch\cutjig\open14\p2\stage_edits.json`. Summary:

| # | S1 r9 | S3 r8 | Edit |
|---|---|---|---|
| 1 | yes | yes | holder z_rule.z_max: `holder_bottom + holder.length + holder.flange_thickness` to `... + washer.thickness - nut.washer_pocket_depth + nut.plate_thickness + nut.lift_play` (145.09 to 153.84) |
| 2 | yes | yes | collar z_rule.z_min: `collar_top - collar.top_above_plate` to `collar_top - collar.thickness` (153.09 to 153.84) |
| 3 | yes | n/a | stack_ties.holder_flange offset to `collar.thickness` (staged tie: 153.840 + 6.0 = 159.840, diff 0.0000, MEASURED) |
| 4 | yes | yes | keys added on holder (receiver.register_bore_radius, register.g_reg, chain.t_h, chain.H, nut.lift_play), collar (collar.thickness), receiver, collet, core_seat, wingnut (S4 lists less the tick and wing keys) |
| 5 | yes | yes | section_true on receiver, collet, core_seat, holder, collar, wingnut, text equal to s4_spec.yaml |
| 6 | yes | yes | receiver\|holder C to G 0.25; receiver\|wingnut N to C; holder\|wingnut N to G 0.50; collar\|holder F to C one_body; collar\|wingnut N to G 0.75 |
| 7 | yes | n/a | S1 note "Holder section is a stand-in; S4 governs ..." retired (Design Notes 25 S4-b); the C-meaning note names the S4-c fits |
| 8 | n/a | yes | wingnut section_class unsectioned to cut, hatch brass |

The r8-era `section` and `bore_cone` fields stay in the staged copies. P4 rules whether `section_true` supersedes them for K5, K7 and X1. K5-Z2 (live bore_cone holder) and K5-B6, B12 read the live S1 holder `bore_cone`, and any retirement re-plants those controls on a fixture. S1 check values that move: none.
- S1-5b: the ring's lowest pose has its bottom at 314.84 against the holder top 153.84.
- S1-4: unchanged.
- drill_head|collar: 25.000 (DERIVED).

The rule (l) anchors are carried to P6 by the orchestrator note (Correction 3).

## 6 X1 result

| Set | X1 (place, z_rule, plan_poly) | section_true on shared rows | section (r8 field) on shared rows |
|---|---|---|---|
| Live (s1, s2, s3, s4 as written) | **pass**: 70 shared rows; skipped base_frame plan_poly (s2, s3), base_plate plan_poly (s2, s3, s4), keepout place (s2, s3) | differs on receiver, collet, core_seat, holder, wingnut, collar (S4 only carries it) | equal on receiver, collet, core_seat, holder, collar, bearing, gear_hub; differs on drill_tube, ring, gear (pre-existing) |
| Staged P6 set (s1 r9, s3 r8, s4 with x1 edits) | **pass**: 70 shared rows | **equal on all six** | as live |

Source: `--stale` run (MEASURED) and `x1dry.py` (`D:\Unleashed Robotics\_scratch\cutjig\open14\p2\x1dry.json`). S4 adds no new shared id: washer, carrier, core_100, liner, receiver_spigot and the lines are S4-only.

## 7 Open items for the sign-offs

- O1 (Designer, Loftsman). The S1/S3 edits are staged, not live (Correction 1). Sign the staged text; P6 applies it with S1 r9 and S3 r8 drawn the same session.
- O2 (P4, Software Engineer). X1 extension:
  - compare `section_true` on every shared row, not `section`, which already differs on drill_tube, ring and gear;
  - expected red on the live set until P6: six base rows where only S4 carries the field.
- O3 (Topologist, (c)). The -X wing at x -83.14 to -115 lies past the beyond band (0 to -60, K8-B74). Options: a spec `beyond_depth` for S4, or the wing as not_drawn with the sweep lines only.
- O4 (Designer). The wing nut true section is outside the ruled list (holder, collar, collet, receiver wall). It is drawn in S4 and staged for S1/S3 for the X1 class. The new classes against the holder and collar follow from it.
- O5 (Designer). In the liner figure the carrier bears on 0.50 mm of the d 105 ledge, and the liner carries the rest.
- O6 (Topologist, (c)): new predicate forms (piece / of_piece, vertical_edge, between, seat_piece) and two new sub-artists.
  - `collet:slits`: 2 lines plus 2 ticks.
  - `receiver:root`: the signed screw_c:root form.
  - `carrier:line` and `core_100:line` use the existing mark admission.
- O7 (P4). Harness items:
  - section_figures (two figures at one tip);
  - section_true rendering, with polygon pieces and the 5-vertex receiver rim on a cylinder row (K5 admission);
  - per-pose rows in the section Axes.
- O8 (Loftsman). Chamfer expression validity (Correction 7). Foot-ring top 41.995 (Correction 6).
- O9 (TASK 0, Software Engineer). K8-B95 landed. Controls are now 480, and the DR4-2 controls await the Software Engineer's re-sign (raisers recheck section 1).
- O10 (Software Engineer). The DEPS-Z2 expectation was re-scoped to the rule's spec set (Correction 10); review it at P5.

## TASK 0. K8-B95 (orchestrator ruling on Software Engineer FIX 8 (b), class repeat)

Fixture `step14_fixtures.py::term_angle_rad0` (span_lt terminator, connectionstyle `angle,angleA=90,angleB=0,rad=0`). The manifest row is K8-B95 after K8-B94; reason "connection style Angle rad 0 is not straight"; finding "P0r SWE FIX 8 (b) class repeat (orchestrator ruling, Step 1.4 P2 TASK 0)". Fixture-only change; no rule or code change.

| Tree | K8-B94 | K8-B95 (MEASURED, `p2/b95.py`, `b95.json`) |
|---|---|---|
| Live code (scratch copy of the live tree) | fires 1, match | **fires 1**, "[section] capture_end/span_lt terminator: connection style Angle rad 0 is not straight (Arc3 rad 0; DR4-2)", match |
| Arc3 class test deleted (`type(cs_).__name__ != "Arc3" or` removed) | fires 1, match | **clean** (0 issues), "reason lacks ...", mismatch |

The class test now has its own B.

## Runs

- `--stale` after the overlay and the S4 spec (MEASURED): 3 records, 0 differences; deps 3 exempt, 0 differences; X1 pass, 70 rows.
- `check_stack.py s4_spec.yaml`: exit 0; collar_top_recomputed 159.84 = params 159.84.
- `check_sketch.py --controls` (full set, 480 controls, after K8-B95, the overlay block, s4_spec.yaml and checks_s4.py): first run Z 107/108 (DEPS-Z2, Correction 10), B 369/369, smoke 3/3, 147.8 s. After the DEPS-Z2 fixture change: **480/480 match (Z 108, B 369, smoke 3), 145.6 s at 12 jobs** (MEASURED). `--stale` after that run: 0 differences; X1 pass.

## Gameplan lines to change

1. Detail 1.4, Params keys line (line 309).
Old:
```
Params keys: `collet.*`, `holder.*`, `receiver.*`, `nut.*`, `washer.*`, `seat.*`, `collar.*`, `witness.zone_high`, `core.diameters`, `core.length_*`, `icd.floor_above_datum_a`.
```
New:
```
Params keys: `collet.*`, `holder.*`, `receiver.*`, `nut.*`, `washer.*`, `seat.*`, `collar.*`, `witness.zone_high`, `core.diameters`, `core.length_*`, `icd.floor_above_datum_a`; overlay (1.4 (b), Design Notes 34, ASSUMED unless DERIVED): `core.length_short` 100, `carrier.length` 160, `carrier.diameter` 101 (DERIVED), `carrier.material`, `carrier.bond`, `liner.od_offset` 5, `liner.wall` 2.0 (DERIVED), `liner.collet_d` 105 (DERIVED), `liner.material`.
```
2. Detail 1.4, Script line (line 310).
Old:
```
Script: `docs/sketches/s4_base_section.py`. PNG: `s4_base_section_r1.png` (location per the Design Notes 25 output rule).
```
New:
```
Script: `docs/sketches/s4_base_section.py`. PNGs: `s4_base_section_r1.png` (pose carrier: d 100 collet, carrier 160, 100 mm core) and `s4_liner_section_r1.png` (pose liner: cast-on liner OD 106 in the d 105 collet) (location per the Design Notes 25 output rule). Spec `docs/sketches/s4_spec.yaml` (section B-B, section_yz, 19 rows, `section_true` true sections, `x1_edits_at_p6`); checks `docs/sketches/checks_s4.py`. The S1 r9 and S3 r8 base-stack edits are staged in `research/sean/cr_scratch/step1.4_p6_staged/` and applied at P6 (`research/sean/cr_scratch/step1.4_engineer_spec.md` section 5).
```
3. Detail 1.4, check table row S4-2 (line 315).
Old:
```
| S4-2 | Advance path against the receiver floor (K7 F): the core's upward path from the core stop does not pass through receiver solid | Fixture with a floor opening | The current receiver as built (floor present) | [CP §9, Q4] |
```
New:
```
| S4-2 | Short-core exposure and grip on the drawn configuration (Sean STOP S4-A, Design Notes 34: advance D, the lift lowers the drill one slice per cut, with the carrier C drawn): (a) core_100 rests on the carrier and the carrier on the core seat within 0.05; (b) drawn core top minus the drawn nut-plate (wing-nut) top >= `core.min_exposed` 143.12 (149.41 on the 160 carrier, margin 6.29); (c) the grip member's drawn extent covers the collet straight bore (42.50 to 65.70 at d 100; the liner 42.50 to 68.20 at d 105); both figures | Live spec (carrier and liner poses) | B1 carrier deleted (core on the seat, exposure -10.59); B2 carrier.length 150 (139.41); B3 carrier bottom drawn at 66.00 (no grip overlap) | [CP §9, Q4]; Design Notes 34 |
```
4. Detail 1.4, check table row S4-3 (line 316).
Old:
```
| S4-3 | Orientation of the kept parts (K8 predicates in the S4 spec): collet taper sense per `cone.alpha`, narrow end as in ASSEMBLY.md; wing nut above holder; washer between nut and holder; receiver floor at the bottom | Fixture in correct sense | Collet flipped end for end | ASSEMBLY.md; critical-path 7.1 (backcap failure) |
```
New:
```
| S4-3 | Orientation of the kept parts (K8 predicates in the S4 spec): collet taper sense per `cone.alpha` on the cone piece, foot ring on the receiver floor, narrow end up as in ASSEMBLY.md; holder cone narrowing up; collet bore vertical (S4-d, Design Notes 34); wing nut above the holder flange; washer between the flange and the nut plate; receiver floor at the bottom; core and carrier upright | Fixture in correct sense | Collet flipped end for end; washer above the nut plate; wing nut below the flange; collet bore drawn parallel to the cone (S4-d) | ASSEMBLY.md; critical-path 7.1 (backcap failure) |
```
5. Detail 1.4, Reported line (line 318).
Old:
```
Reported: exposed length of a 100 mm tall core against `core.min_exposed` 143.12 (Q10); collet length options (Q5); sacrificial collet or liner (Q6).
```
New:
```
Reported (spec reported_items, RPT): 100 mm core top against the collar top (142.50 on the stop, 17.34 below; 302.50 on the carrier) and its exposure against `core.min_exposed` 143.12 (-10.59 / 149.41); minimum core on the stop 253.71 (nut-plate datum; 260.46 collar-top datum); collet grip 23.20 (d 100); advance D: least slice 76.44 axis / 56.02 surface, 0.75 m core 496.29 sliceable, 6 slices, 100 mm core 1 slice; carrier-joint shear 50.9 kPa (liner 6.37); collet length options Delta 0 / 25 / 50 (Q5, kept 32 mm); liner D = d + 5, wall 2.0 (Q6); cut-case seat as drawn; kept-part axial forces (as S3 r7).
```
6. Echo Site Registry, insert after line 773.
Insert after:
```
| Section A-A: plane x = 0, viewer at +X, u = +Y, pose capture_end | `s3_spec.yaml` section block | DECLARED (Designer 1.3 (a), Design Notes 4); S3 figure title, inset cutting-plane line, K8 section handedness |
```
New:
```
| Section B-B (S4): plane x = 0, viewer at +X, u = +Y, poses carrier and liner at the stop (tip 184.84 z_A) | `s4_spec.yaml` section block | DECLARED (Designer 1.4 (a) section 1; Sean STOP S4-A, Design Notes 34) |
```
7. Echo Site Registry, insert after line 770.
Insert after:
```
| Core stop **42.5 mm** z_A | overlay `collet.core_stop_z`; 4a promotion list | ASSUMED (G4) |
```
New:
```
| Short core **100 mm** on the **160 mm** nylon carrier: core top 302.50 z_A, exposure **149.41** over the nut-plate top against `core.min_exposed` 143.12; minimum core on the stop **253.71**; collet grip **23.20** (d 100) | overlay `core.length_short`, `carrier.length`; params `core.min_exposed`, `collet_family` dims | ASSUMED (Designer 1.4 (a); Sean STOP S4-A, Design Notes 34); S4-2 asserts the drawn exposure and grip |
| Liner **D = d + 5**, wall 2.0 (d 100 core in a 105 liner, d 105 collet) | overlay `liner.od_offset`, `liner.wall`, `liner.collet_d` | ASSUMED / DERIVED (Designer 1.4 (a) section 8; Design Notes 34) |
| Holder true section: tube top **153.84** z_A (collar underside), collar ring 153.84 to 159.84; nut-plate top 153.09 | `build_parts/holder.py` dims; s4_spec.yaml `x1_edits_at_p6` (S1, S3, S4 at P6) | DERIVED (Designer 1.4 (a) Correction 4) |
```
8. Echo Site Registry, insert after line 800.
Insert after:
```
| Core holding torque **10 N m** | `loads.torque_design` | DECLARED |
```
New:
```
| Least slice under F4 **76.44** (axis) / **56.02** (core surface, d 100); kerf centre at the stop 291.21, dome pole 219.77 z_A | `drill.kerf_standoff`, `drill.dome_pole_offset`, `iris.face_radius_core`, `stop.margin` | DERIVED (Designer 1.4 (a) Correction 6); B3-4 to Quinn |
```
