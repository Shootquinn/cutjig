# Step 1.1 (d) Engineer draw, S1 r1

## Corrections to the brief

1. **No iteration was needed.** Run 1 of `check_sketch.py s1 --rev 1` is green on all 18 checks (K1 to K9, S1-1 to S1-7). There are no fixes to log.
2. **`s1_summary_r1.md` is rewritten on every `check_sketch.py s1` run.** The reported values that check_stack does not produce (drawn highest point, ring and anchor heights, COM, tip force) are appended by the new `sketches/s1_mass_report.py`. Re-run it after each check run.
3. **check_stack.reported labels its highest points "spec values, not drawn".** The drawn highest points (MEASURED from the figures) are identical in every pose.
4. **The unbolted tip force at the frame top does not depend on pose for a fixed mass.** With the COM on the drill axis, F = W g a / h_top, so the COM height does not enter it. It changes only with the core (load, start and capture_end against park). The COM height does change the force at the COM, which is the form used by the old icd.tipover_statement.
5. **The Software Engineer's FIX 1 (S1-2-B2) is applied with this pass,** as the brief states.

Tags: check, control and drawn values are MEASURED (run 2026-11-25). Stack values are DERIVED. Masses are ASSUMED (overlay) or DERIVED (geometry, ASSUMED densities). The NEMA 17 mass is ASSUMED as a working value.

## Files written

| File | What |
|---|---|
| `research/sean/cr_scratch/sketches/s1_side_poses.py` | S1 script: `build(P, spec, stack)` gives one figure per pose. Run directly with `--rev k`, it writes the PNGs. |
| `research/sean/cr_scratch/s1_pose_load_r1.png` | Written 2026-11-25 12:07:59 |
| `research/sean/cr_scratch/s1_pose_start_r1.png` | Written 12:08:00 |
| `research/sean/cr_scratch/s1_pose_capture_end_r1.png` | Written 12:08:00 |
| `research/sean/cr_scratch/s1_pose_park_r1.png` | Written 12:08:01 (before the first check run) |
| `research/sean/cr_scratch/sketches/s1_checks_r1.json`, `s1_summary_r1.md` | `check_sketch.py s1 --rev 1` |
| `research/sean/cr_scratch/sketches/s1_mass_report.py`, `s1_mass_report_r1.json` | Drawn reported values; appends to `s1_summary_r1.md` |
| `sketches/fixtures/builders.py` | Adds `s1_2_b2()` = `_s1_ctx(spec_mut=_pose_tip("load", "start_tip_max"))` (SW FIX 1) |
| `sketches/fixtures/manifest.yaml` | Adds S1-2-B2: reason "load: drawn tip 894.84 not above the highest class start 894.84", planted 1, gameplan_line 229 |
| `sketches/fixtures/controls_results.json`, `sketches/baseline_red.json` | `--controls` and `--baseline` re-run. The prior baseline is kept under `prior` |

No change was made to the checks, the spec, the overlay or check_stack.

## Shapes drawn (spec `shape` field) and what the checks exclude

The checks constrain decoration in two ways. K5 requires every patch, line and collection to be tagged and drawn as its row's declared projection, so a Line2D tagged to a rectangle row fails. K8 reads the x extent of all of a placed row's pieces for the TP-3 centre check, and it applies the taper and mirror predicates to every piece. Section detail is therefore drawn as extra rectangles of the same row, inside its extents, and orientation notes are untagged Text.

| Row | Drawn |
|---|---|
| base_frame | Rail band over footprint_x, with end-member 60 x 60 sections at x = +/- frame.end_x (hatched) |
| base_plate | Section, hatched. The spigot-hole break is not drawn: the hole radius (80.2) leaves the receiver (r 80) 0.20 from the plate, and the C pair would fail |
| receiver | Cup section: floor either side of the debris hole (r 40) up to receiver_floor, walls from r 67.29 to 80 up to the rim |
| collet | Two four-vertex cone sides, bore at the core OD, narrowing up by 32 tan 10 = 5.64 |
| core_seat | Ledge per side, 3 wide, inside the bore at r 47 to 50 |
| holder | Wall per side (r 50 to 67.29) with the flange (holder.flange_od, holder.flange_thickness) on top |
| wingnut | Body, wings per side to span / 2 (wing_height, at the bottom), sweep r 115 as a dashed envelope |
| collar | Section per side, r 55 to 76.2 |
| core_750 | Heavy solid outline. Absent at park |
| drill_head | Heavy outline. Teeth strip (hatched, height (head_od - tube_od) / 2 = 12.7, drafting choice) at the tip. Iris throat dashed at tube ID. Note "HEAD (cutter, tip)" |
| drill_tube | Outline, bore dashed at tube ID |
| drill_top_block | Solid filled. Note "TOP-END BLOCK (tail)" |
| ring, bearing, gear_hub | Sections per side. The bearing is split into inner and outer races at the mid radius |
| gear | `sc.draw_gear_section` (back face up, teeth down) |
| pinions | Trapezoid. Heel at the full OD, toe height scaled by r_toe / r_heel, narrowing inward |
| screws | Lead hatch |
| anchors | Hatched block with the thrust-bearing line (zero-height rectangle) |
| guides | Dotted hatch. Notes "anchor" and "top guide" |
| nuts | Filled brass |
| motors | Filled |
| descent_stop | Metal hatch |
| keepout, bore_ceiling, height_target | Dashed lines |

Not drawn, because each would add a line, or a piece outside the row's place extent, and fail K5 or K8: the screw-frame bracket arms, the NEMA 23 shaft, the pinion shaft line, the core chamfer mark, the cable-exit mark, the collet slit ticks and the gear and pinion tooth ticks.

## SW-18: K1 on the real script

K1 scans `s1_side_poses.py`: 0 literals outside [-1, 0, 0.5, 1, 2], no soft-key comparison and no figure setting (MEASURED). The literals in use are 1 and -1 (side signs, default rev) and 2 (halving, line width). Angle sources:
- The collet taper reads `cone.alpha` (P.get) in `_cone_sides`.
- Every azimuth (jackscrew.angle, pinion.angle, guide.angle) enters through check_stack `place.x`, which is r_c cos(theta).
- The pinion toe ratio reads `pinion.r_toe / pinion.r_heel`.
- The gear rise is the `draw_gear_section` default, (z1 - z0) / 2, in sketch_common.

## Iteration log

| Run | Command | Red | Fix |
|---|---|---|---|
| 1 | `check_sketch.py s1 --rev 1` | none | none |

## Final check table (r1, MEASURED)

| Check | Result | Reason |
|---|---|---|
| K1 | pass | 0 literals, no soft key, no figure setting (s1_side_poses.py) |
| K2 | pass | 210 spec keys resolve, 103 overlay leaves sourced |
| K3 | pass | 4 figures conform |
| K4 | pass | 43 labels carry their key value |
| K5 | pass | 283 tagged artists projected per kind |
| K6 | pass | 179 z_rules match drawn extents within 0.05, anchors clean |
| K7 | pass | 285 pair tests clean |
| K8 | pass | 230 predicates hold, axes not inverted |
| K9 | pass | every spec row drawn, every tagged artist in the spec (45 rows) |
| S1-1 | pass | reach 650.00 in [534.93, 650] (margin 0.00 on the upper bound, by construction) |
| S1-2 | pass | park above the highest class start by 125.00 |
| S1-3 | pass | over core_stop: 367.34 (0.5 m), 117.34 (0.75 m) |
| S1-4 | pass | least margin 0.84 |
| S1-5a | pass | 192.34, need 25 |
| S1-5b | pass | 77 pairs, least clearance 142.00 |
| S1-6 | pass | 8 screw projections |
| S1-7 | pass | 607.66, need 534.93 (spare 72.73) |

**Controls, end of pass:** `--controls` gives 99 controls. Z clean 30/30, B fired 68/68, smoke 1/1, exit 0. S1-2-B2 fires 1/1 on "load: drawn tip 894.84 not above the highest class start 894.84 z_S".

**Stale check:** `--stale` gives 0 records and 0 differences (no record accepted yet).

**Baseline:** `--baseline` gives run 1 at 30/30, 68/68, 1/1, and run 2 at 17/17.

## Reported values (no threshold, never asserted)

| Pose | Highest drawn point z_S (part) | Margin to 2000 | Ring z_S | Mass kg | COM z_S | Tip force at COM N | Tip force at frame top (1285 z_S) N |
|---|---|---|---|---|---|---|---|
| load | 1969.84 (top-end block) | 30.16 | 1149.84 to 1161.84 | 76.07 | 664.8 | 341 | 177 |
| start | 1844.84 (top-end block) | 155.16 | 1024.84 to 1036.84 | 76.07 | 616.4 | 368 | 177 |
| capture_end | 1285.00 (screw frame member) | 715.00 | 374.84 to 386.84 | 76.07 | 427.1 | 531 | 177 |
| park | 1969.84 (top-end block) | 30.16 | 1149.84 to 1161.84 | 60.47 | 698.0 | 258 | 140 |

Notes on the table:
- Tip force uses a 304 mm lever (min footprint / 2), with the COM on the axis by three-fold symmetry.
- The masses are the overlay masses (drill 8, top block 2, ring 6, gear 3, 3 x NEMA 23 at 1.0, 3 nuts at 0.05) plus the 0.75 m core 15.6 kg at load, start and capture_end. The core is counted at load, where it is held mid-insertion. The structure is DERIVED: base frame 8.23 from frame.members and the catalog kg/m, plate 12.69 with aluminium ASSUMED, 3 screw frame members 9.36, 2 guide rods 5.92 with steel ASSUMED, 3 screws 1.07, and 3 NEMA 17 at 0.35 WORKING ASSUMED. The receiver, collet, holder, wing nut and blocks are omitted.
- The old reference (icd.tipover_statement) is 158 N at the COM (0.69 m) and 68 N at the column top.

Other reported values:
- **Ring (N1):** ring.position_above_tip 130 (ring plate bottom above the tip), thickness 12.
- **Anchors:** jackscrew.anchor_z 265 z_A (325 to 355 z_S drawn).
- **Top guides:** jackscrew.top_guide_z 1165 z_A (1195 to 1225 z_S drawn).
- **Screw:** jackscrew.length 900.
- **Park rule for Step 4:** `upper.park_z = max(max_k (max(stop.height_z, collet.core_stop_z + L_k + stop.g_stop - drill.bore_ceiling_above_tip) + upper.travel_max), stop.collar_top_z + max_k L_k) + upper.load_clearance`. It gives 959.84 z_A.

| Q9 option | Park z_A | Lift stroke | L_min | L at anchor_z |
|---|---|---|---|---|
| 0.5 m only | 959.84 | 775.00 | 885.00 | 885.84 |
| 0.5 and 0.75 m | 959.84 | 775.00 | 885.00 | 885.84 |
| plus 1 m | 1209.84 | 1025.00 | 1135.00 | 1135.84 |

The 900 mm screw covers the first two options and is 235 short for the 1 m option. The 1 m start is 125.00 inside the uncut core (OPEN, Loftsman FIX 5).

## Open items

1. **Designer: holder flange against the receiver rim.** With the flange drawn on the holder top (the shape field says "flange ... on top"), the flange bottom is 189.09 z_S and the rim is 188.50, a gap of 0.59. The shape field says the gap is the stroke gap, holder.stroke_gap_R 13.126. Either the flange is not at the holder top or the holder z_rule is short. This is a spec or params question, and nothing in the drawing was changed for it.
2. **Designer: screw-frame bracket arms, the descent-stop pad support, and the motor and pinion shafts are not drawn.** The K5 and K8 rules exclude them, as tabulated above. The pad reads as floating at r 200 to 215. Options: new spec rows (bracket_a/_b, kind prism, place radial from frame_upper.radius to the screw), or accept them as absent at S1.
3. **Base plate spigot-hole break.** It is not drawn, because the hole radius 80.2 against the spigot r 80 would open the receiver|base_plate C pair by 0.20. The spec C pair assumes the receiver bears on the plate top. This is consistent, and no action is needed unless the Designer wants the break shown.
4. **Gameplan l.144 (orchestrator).** Insert S1-2-B2 after S1-2-B1. The count becomes "(99 controls: Z 30, B 68, smoke 1)".
5. **Gameplan l.229 (orchestrator).** Append "; the load pose at the top of travel (S1-2-B2)".

## For Sean's orientation preview (V1 to V5)

- **V1 to V5 read correctly in all four PNGs:**
  - The floor is at z_S 0 at the bottom, with the base frame and plate on it.
  - The drill axis is vertical at x = 0.
  - The hatched cutter head is at the bottom and the solid top-end block at the top, each with a note.
  - The core stands upright on the seat at start and capture_end, is mid-insertion at load and is absent at park.
  - The screws are vertical, with the hatched anchors (lift motor below) at the bottom and the top guides at the top.
- **The side projection overlaps parts that sit at different azimuths.** At load and park the NEMA 23 bodies and the gear overlap the top-guide blocks: motors 1185.34 to 1242.34 z_S against guides 1195 to 1225. The motors are at azimuths 210 and 330 and the screws at 150 and 30, so the parts are plan-separated and K7 is clean. The guide rods (theta 0 and 180) are drawn over the screw frame members (theta 30 and 150).
- **The lift motor draws 59.4 wide,** the diagonal envelope of the 42 mm square (Designer re-check), which is not a defect.
