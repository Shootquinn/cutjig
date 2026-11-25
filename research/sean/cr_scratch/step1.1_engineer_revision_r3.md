# Step 1.1 (h) Engineer revision, S1 r3 (from the Designer's M1 visual gate on r2)

Source: sketches/s1_visual_gate_r2.md, findings F1 to F5 marked "fix in r3" (orchestrator ruling: fix before Sean's M2 pass). Every new dimension is the Designer's ASSUMED value. Drawn and check values are MEASURED (run 2026-11-25). Hand values are DERIVED.

## Corrections to the brief

1. **"C with the block and with frame_upper" cannot pass the r2 K7 rule in a side view.**
   - The arms sit at theta 150 / 30. In projection, the radial footprint adds w |sin theta| = 15 to each end. The arm box (x -248.83 to -141.75, hand: 181 cos 150 = -156.75, 270 cos 150 = -233.83, plus or minus 15) overlaps the anchor block box (-159.56 to -117.56) and the member box (-289.81 to -229.81).
   - Under the r2 rule, live S1 read 40 C failures: 4 poses x (4 arms x 2 contacts + 2 shafts). Arm|block overlap is 534.40 mm2 and arm|member is 570.58 mm2 (MEASURED).
   - New K7 behaviour, **plan-contact**: a C pair whose side-view pieces overlap passes when both rows are placed and their plan footprints touch (distance <= 0.05) without overlap (area <= 0.01). Vertical prisms with disjoint plan interiors cannot interpenetrate. Touching footprints with overlapping z extents are in contact on a vertical face.
   - Live values: arm|block distance 0.000 with plan overlap 0.001 mm2, and arm|member 0.000 with 0.003 mm2. Both overlaps are circumscribed 128-gon artefacts.
   - Controls K7-Z11, K7-B16 and K7-B17. The rule needs Loftsman and Topologist sign-off.
2. **Shaft "C with the motor" hits the same projection artefact.** The side-view overlap is 130.00 mm2, and it passes as plan-contact with distance 0.000 and plan overlap 0.000. The Designer wrote "N with the pinion hub (already declared)", but only pinion|motor23 was declared. The shaft is a new row, so pinion_a|motor_shaft_a and pinion_b|motor_shaft_b are added as N.
3. **Label wording.** The Designer asked for "anchor z_S 325 (jackscrew.anchor_z)". K4 requires the key value (265) in the label. The labels read "anchor z_S 325 (jackscrew.anchor_z 265 z_A)" and "top guide z_S 1225 (jackscrew.top_guide_z 1165 z_A)", through a new label field `z_S: true`.
4. **The dashed-arm rule, read literally, dashes both anchor arms in every pose.** The guide rods at theta 0 and 180 (y 0) are in front of the arms (y 64.52 to 160.98) and cover 20 of the arms' 107.08 projected length.
   - Drawn rule: an arm is dashed when a wholly nearer part overlaps it in z and covers at least half its projected x length.
   - Result: the guide arms are dashed at load and park (motor23 covers 61.3 of 107.1) and solid at start and capture_end. The anchor arms are solid in every pose. **Designer to confirm.**
5. **Notes without a leader go under the axes.** These are the axial loop, the "not drawn" third set and, on the park figure, the park rule. In the label column they were crossed by the shop-floor and soft-target leaders.
6. **Mass report omits the new rows.** s1_mass_report.py omits the bracket arms and the post, as it already omits the anchor and guide blocks. The mass table is unchanged from r2.

## Correction table

| ID | Finding (Designer's words) | Fix | Predicate / rule | B fixture |
|---|---|---|---|---|
| F1 (a) | "no motor or pinion shaft" | Rows motor_shaft_a/_b:<br>- cylinder, axis X, radial r 121 to 142 (pinion.motor_r_in - motor_shaft_length to motor_r_in), half-width motor_shaft_od / 2.<br>- z = pinion axis +/- 4. Drawn filled.<br>- C with motor23, N with the pinion, fixed_g10.<br>- Sense: side of drill_tube, outboard of the pinion. | K7 plan-contact, K8 projected_x / side / outboard, K9 | K7-B19 covers the plan-contact failure. A missing shaft is caught by K9 (K9-B1 behaviour). |
| F1 (b) | "pinion axis cannot be read" | Rows pinion_axis_a/_b:<br>- line, dash-dot, r 95.22 to 218 at theta 210 / 330, horizontal at the pinion-axis z.<br>- Drawn x -188.79 to -82.47 (_a). | K6 (z), K8 projected_x and side, K9 | visual only beyond K9 |
| F1 (c) | "pinion outline indistinct from the gear" | Gear hatched "////", pinions hatched "\\\\" | visual only | none |
| F2 | "anchor blocks, top-guide blocks ... float" | Rows bracket_anchor_a/_b and bracket_guide_a/_b:<br>- prism, radial r 181 to 270, half-width 30, block z (265 to 295 / 1135 to 1165 z_A).<br>- C with the block and the member (plan-contact).<br>- Added to fixed_g10.<br>- Sense: below / above nut, outboard of the block. | K7 C plan-contact, K7 G (fixed_g10), K8, K9 | K7-B19 (live): anchor arm r_in + 1, "bracket_anchor_a\|anchor_a C ... plan footprints distance 0.994", 4 poses. K7-B16 / B17 (mini): 1 mm off, 1 mm into. |
| F3 | "Pad drawn floating" | Row descent_stop_post:<br>- r 200 to 215, half-width 30, z_rule anchor_z + anchor_allowance to ring_bottom_low - stop.pad_thickness (295.00 to 302.84 z_A, 7.84).<br>- C with bracket_anchor_a and descent_stop. Added to fixed_g10. | K7 C, K8 below, K9 | K7-B18 (live): post 1 mm short, "descent_stop_post\|descent_stop C, distance 1.000", 4 poses |
| F4 | label overlaps; name-only labels | `place_labels(margin=True)`: one column right of the axes, leaders, stacked in anchor-z order with 0.5 line free between boxes.<br>Labels on rows:<br>- anchor_b, guide_b (z_S plus key).<br>- frame_upper_b "screw frame 30-6060 r 300".<br>- drill_head "HEAD (cutter, tip); cutter OD ASSUMED 177.8; tip z_S <tip>" (label field z_edge).<br>- drill_top_block "TOP-END BLOCK (tail) 150".<br>Park figure: "lift stroke 775 (park 1019.84 - capture_end 244.84 z_S)" and the spec park_rule.park line with 959.84 z_A / 1019.84 z_S. | K4 (55 labels carry their key value) | K4 controls unchanged. Label overlap is visual only. |
| F5 / V9 | "Axial loop not readable" | Arms drawn (F2). The members are labelled. Margin note: "axial loop: ring nut - T8 screw - anchor and guide blocks - bracket arms - screw frame 30-6060 - base plate - base frame - floor". Park rule and stroke on the park figure. | visual only | none |
| Header | holder stand-in; C meaning | Spec field `notes`: (1) the holder section is a stand-in and S4 governs (build_parts/holder.py); (2) C means "located on that face", and fit values belong to S4 and Step 4 | none | none |

Spec status: unchanged, with an r3 edit comment under it. **Re-sign is due:** the Designer for the new rows, the dash rule and the label text; the Loftsman for placement and the plan-contact rule; the Topologist for the plan-contact half-space argument.

## Check values (MEASURED, hand DERIVED)

| Pair / value | Pose | Measured | Hand |
|---|---|---|---|
| nut_housing_a \| bracket_anchor_a (G 10) | capture_end | 10.840 | 305.84 - 295 = 10.84 |
| ring \| bracket_anchor_a (G 10) | capture_end | 19.840 | 314.84 - 295 = 19.84 |
| ring \| descent_stop_post (G 10) | capture_end | 12.000 | 314.84 - 302.84 = 12.00 |
| nut_housing_a \| descent_stop_post (G 10) | capture_end | side view 3.000; plan 14.993 (plan-separated) | 200 - 185 = 15.00 (128-gon lower bound) |
| nut_housing_a \| bracket_guide_a (G 10) | park | 24.160 | 1135 - 1110.84 = 24.16 |
| ring \| bracket_guide_a (G 10) | park | 33.160 | 1135 - 1101.84 = 33.16 |
| gear \| bracket_guide_a (G 10) | park | 37.295 | x gap 141.75 - 126.32 = 15.43 (lower bound; drawn gear face sets 37.30) |
| motor23_a \| bracket_guide_a (G 10) | park | depth bands 110.838 apart | 64.52 + 46.32 = 110.84 |
| bracket_anchor_a drawn x | all | -248.83 to -141.75 | above |
| descent_stop_post z_S | all | 355.00 to 362.84 | 295 + 60, 302.84 + 60 |
| motor_shaft_a z_S, load | load | 1209.84 to 1217.84 | ring top 1161.84 + 52 +/- 4 |

## Check results

`check_sketch.py s1 --rev 3`: 17/17 pass on run 1 of the drawing.

| Check | Result | Reason |
|---|---|---|
| K1 | pass | 0 literals. Two style literals (linewidth 1.2 and 0.8) were caught on the first draw and removed. |
| K2 | pass | 284 spec keys resolve (r2: 219) |
| K3 | pass | 4 figures |
| K4 | pass | 55 labels carry their key value |
| K5 | pass | 327 tagged artists (r2: 291) |
| K6 | pass | 215 z_rules within 0.05 (r2: 179) |
| K7 | pass | 457 pair tests clean (r2: 309). New state: plan-contact |
| K8 | pass | 330 predicates (r2: 234) |
| K9 | pass | 54 rows (r2: 45) |
| S1-1 to S1-7 | pass | unchanged: 650.00, 125.00, 367.34 / 117.34, 0.84, 192.34, 142.00, 8 projections, 607.66 (spare 72.73) |

- **Controls:** `--controls` returns 113: Z 34/34 clean, B 78/78 fired, smoke 1/1, exit 0. The r3 additions are K7-Z11, K7-B16, K7-B17, K7-B18 and K7-B19.
- **Red first:**
  - Under the r2 rule (plan_contact disabled), K7-Z11 fires: "arm|block C ... overlap 534.404".
  - Live S1 fires 40 C failures under the same rule.
  - K7-B16 to B19 fire with the planted reason and count.
- **Stale:** `--stale` reports 0 records and 0 differences.
- **Baseline:** `--baseline` was re-run because run 1 grew. Run 1 is 34/34, 78/78 and 1/1. Run 2 (stub) matches 17/17.
- **Stub on the r3 spec:** checked in-process with no file written, the red set is unchanged. K1, K2, K3 and K5 are green. K4 and K9 are red on content. K6 to K8 and S1-1 to S1-7 are red as absent.
- **Reported:** unchanged from r2 (s1_summary_r3.md with the s1_mass_report section).

## PNGs

- research/sean/cr_scratch/s1_pose_load_r3.png
- research/sean/cr_scratch/s1_pose_start_r3.png
- research/sean/cr_scratch/s1_pose_capture_end_r3.png
- research/sean/cr_scratch/s1_pose_park_r3.png

Also written: sketches/s1_checks_r3.json, sketches/s1_summary_r3.md, fixtures/controls_results.json and baseline_red.json (prior record kept).

Visual residue for M1:
- Two leader crossings remain. On the park figure, the keep-out and lift-stroke leaders cross near the head. At capture_end, the core leader passes over the gear.
- No label text overlaps another label or the drawing.

## Files changed

- sketches/s1_spec.yaml: 9 rows, 5 labels, fixed_g10 +5, notes, pinion N pairs, descent-stop shape text.
- sketches/s1_side_poses.py
- sketches/sketch_common.py:
  - label_text (z_S, z_edge), place_labels margin mode
  - K7 plan_contact_fn and the assess_pair plan-contact branch
- sketches/fixtures/builders.py: placed line in the smoke drawer; k7_z11, k7_b16 to b19.
- sketches/fixtures/manifest.yaml

## Items assigned elsewhere by the Designer (not implemented; Design Notes 20 style rows for the gameplan)

| Item | Owner | Carried text |
|---|---|---|
| Base plate spigot-hole break, 80.2 hole on the 80 spigot | S4 | Draw at detail scale; reclassify receiver\|base_plate as G 0.10 |
| Holder part section (build_parts/holder.py) | S4 | Adopt OD 67.04, cone 62.04 to 56.75 over chain.H 30, bore 56.75, tube through the nut plate to the collar. receiver\|holder becomes G 0.25 and collar\|holder becomes C. Retire the S1 spec note when S4 is accepted. |
| C contacts as idealised fits (Loftsman R2-1) | S4, Step 4 tolerancing | Fit values per C pair. S1 spec note in force. |
| F6: ring rim hides the end of the cut at capture_end (V10) | Step 2 (with the gear guard and interlock row), S2 plan sightline | Sight window between the screw and pinion azimuths, a camera, or end-of-cut by the descent stop with a stop indicator. **Sean accepts the assignment at M2.** |
| F7: cutter r 88.90 outside keep-out r 86.2 (LF1.1-5) | S2 plan clearance, Step 4 ICD icd.keepout_radius | No S1 action |
| Tooth-level read of the gear and pinions (module 4.17, under 3 px at S1) | S6 | S6 fixes the gear and pinion geometry |
| Bracket arm and post design (all ASSUMED) | Step 2 | Step 2 rules the bracket design |
| Ring and NEMA 23 at chest-to-shoulder height at load (strike hazard) | Step 2 operator-task table row | From the V10 load row |
| Dashed-arm half-coverage rule, label text, new rows | Designer re-sign (M1 on r3) | See Corrections 3 and 4 |
| K7 plan-contact rule | Loftsman, Topologist sign-off | See Correction 1 |

## Gameplan lines that need a change (gameplan not edited)

- **l.140 (K7 classes):** add "a C pair whose side-view pieces overlap passes as plan-contact when both rows are placed and their plan footprints touch without overlap (distance <= 0.05, area <= 0.01)", with controls K7-Z11, K7-B16 and K7-B17. Add the live controls K7-B18 (F3) and K7-B19 (F2).
- **l.144 (control count):** append "1.1 (h) r3 added K7-Z11, K7-B16, K7-B17, K7-B18, K7-B19 (113 controls: Z 34, B 78, smoke 1)".
- **Design Notes 20:** add the rows in the table above.
- **Carried and still pending if not applied:** the r2 list (l.138, 139, 141, 142, 237) and the r1 items (l.144 S1-2-B2, l.229).
