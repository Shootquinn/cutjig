# Step 1.2 (d) Engineer: S2 r1 drawn, S1 r5 run

## Corrections to the brief

1. **S1 r5 check count.** The brief asks for 17/17. The S1 run carries 18 checks since 1.2 (c): K1 to K9, S1-1 to S1-7 (S1-5 split a/b) and X1. Result 18/18 (MEASURED).
2. **S1 r5 outputs existed before this run.** The P5f fix pass wrote an S1 r5 preview to `wip/` at 17:41 to 17:51. This pass re-ran all three S1 r5 commands at 17:58 and overwrote them; the record is the 17:58 set.
3. **S2 check count.** S2 carries 17 checks: K1 to K9, S2-1 to S2-6 (S2-5 split a/b), X1.
4. **Gear tooth ticks cannot be drawn under the signed rules.** The gear shape text asks for tooth ticks on the OD. K5 requires every artist tagged `gear` (kind gear, axis Z, plan) to be a circle; an untagged artist fails K5 and an artist under any other gid fails K9. The gear is drawn as the hatched annulus r 90 to 126.32 with the pitch circle r 125 chain-dashed (drafting convention). Open item 1.
5. **Mass report r5 equals r4.** `s1_mass_report_r5.json` is value-equal to r4 (MEASURED, diff empty): frame_upper.radius moves no mass term in the model (members keep their length; arm mass is not modelled).

Tags: run results MEASURED 2026-11-25 on `docs/sketches/` (Python 3.12, matplotlib 3.11.2). Hand values DERIVED. Design values DECLARED or ASSUMED as in the overlay.

## 1 Files written

| File | Written (MEASURED) | Content |
|---|---|---|
| `docs/sketches/s2_plan.py` | before 17:57:05 (last edit before 17:57:54) | S2 plan script, `build(P, spec, stack)` entry and `--rev` CLI |
| `docs/sketches/wip/s2_plan_r1.png` | first write **17:57:05**; final 17:57:54 | plan XY at pose load |
| `docs/sketches/wip/s2_checks_r1.json`, `wip/s2_summary_r1.md` | 17:58:08 | S2 r1 record; summary with an appended reported-values section |
| `docs/sketches/wip/s1_pose_load_r5.png`, `_start_r5`, `_capture_end_r5`, `_park_r5` | 17:58:21 to 17:58:24 | S1 r5 four poses |
| `docs/sketches/wip/s1_checks_r5.json`, `wip/s1_summary_r5.md` | 17:58:39 | S1 r5 record |
| `docs/sketches/wip/s1_mass_report_r5.json` (and its section in `s1_summary_r5.md`) | 17:58:45 | S1 r5 mass and tip force |

Not changed: every spec, the overlay, the harness, checks_s1.py, checks_s2.py, fixtures, the S1 script.

## 2 Iteration log

| Run | Red checks | Fix |
|---|---|---|
| 1 (`s2_plan.py` before first execution, K1 by inspection) | K1 would read `range(1, 10)` (z order bands) and `[:-6]` (sector edge samples) | z order from `enumerate` over band names; sector wedge kept as the apex and arc points of `sector_boundary` (radius 0 or r within TOL_Z) |
| 2 (`check_sketch.py s2 --rev 1`, 14 s) | none: 17/17 | none |
| 3 (visual, the PNG) | screw c tag (r 334 at theta 270) on the x tick labels | y limit lowered by profile.width after `finish_axes`; 17/17 re-run |

The drawing follows the fixture geometry of `fixtures/builders.py::_s2_draw_row` (the signed S2 drawing that K4-Z2, K5-Z3, K6-Z4, K7-Z15, K8-Z6, K9-Z3 and S2-x Z run on) and adds styles, fills, the gear pitch circle, the datum B signifiers, part tags and margin labels.

## 3 Final check tables

**S2 r1** (`wip/s2_checks_r1.json`, 17:58:08): **17/17 pass**.

| Check | Result | Measured |
|---|---|---|
| K1 | pass | 0 literals outside {-1, 0, 0.5, 1, 2}; no figure setting |
| K2 | pass | 420 spec keys; 121 overlay leaves |
| K3 | pass | 1 figure |
| K4 | pass | 14 labels carry their key value; figure note names every not_drawn part |
| K5 | pass | 99 tagged artists |
| K6 | pass | 69 plan centres within 0.05 |
| K7 | pass | 1280 plan pair tests over 4 poses |
| K8 | pass | 114 predicates; axes not inverted |
| K9 | pass | 70 rows drawn, no stray gid |
| S2-1 | pass | screws 30, 150, 270; pinions 90, 210, 330; phase 60 within 0.000 |
| S2-2 | pass | least 52.80 over g_min 10 |
| S2-3 | pass | heel pitch points r 125.000 (gear pitch radius 125.00) |
| S2-4 | pass | 4 centres within 0.000 |
| S2-5a | pass | 27 fixed parts clear, least 11.71 (lift motors a, b) |
| S2-5b | pass | 8 ring parts in the sector, least 136.84 above the hand band (bearing) |
| S2-6 | pass | 3 members seated |
| X1 | pass | 47 shared rows equal |

**S1 r5** (`wip/s1_checks_r5.json`, 17:58:39): **18/18 pass**. K1, K2 (322 keys), K3 (4 figures), K4 (55 labels; figure note), K5 (343 artists), K6 (231 z_rules), K7 (609 tests), K8 (346 predicates), K9 (58 rows), S1-1 650.00 in [534.93, 650], S1-2 125.00, S1-3 367.34 / 117.34, S1-4 0.84, S1-5a 192.34, S1-5b 142.00 over 91 pairs, S1-6 8 projections, S1-7 spare 72.73, X1.

**K1 on `s2_plan.py`.** Numeric literals: 0, 1, 2, 0.5 only (MEASURED, K1 pass). Angle sources: every azimuth is check_stack `place.theta` or `sector.theta`, from `jackscrew.angle`, `pinion.angle`, `guide.angle`, `operator.sector_theta`, `operator.watch_theta`; the tie pieces from their plan_poly expressions. The one angle in the script is the theta arc of datum B, `math.pi / 2` (+X to +Y quarter turn), a frame signifier with no design value. Offsets from params: `profile.width` (tag offset, y margin), `drill.tube_id` (datum B size and the tube annulus bore), `gear.pitch_diameter`, `pinion.r_heel`.

**Controls** (`check_sketch.py --controls`, end of pass): exit 0, **191/191 matched** (Z 56/56, B 133/133, smoke 2/2), 284 s; no regression. `wip/fixtures/controls_results.json`.

**Stale** (`check_sketch.py --stale`): exit 1, one difference, `sketches/s1_checks_r4.json: frame_upper.radius recorded 300, live 274` (the adopted key only). With `--include-unaccepted`: 4 records checked (s1 r4, s1 r5, s2 r0, s2 r1), the same single difference.

## 4 Reported values (S2 r1; also appended to `wip/s2_summary_r1.md`)

| Quantity | Value | Tag |
|---|---|---|
| Outline extents, every drawn part | x -322.00 to 322.00, y -304.00 to 304.00, equal to 644 x 608 (plate and frame) | MEASURED |
| Outline extents, parts above the plate | x -278.27 to 278.27, y -304.00 to 218.00 | MEASURED |
| Operator sector | y to 400, 96 past the +Y plate edge | MEASURED |
| Members a, b to the plate edge x 322 | **43.73** (x extent 196.31 to 278.27) | MEASURED |
| Members a, b to the plate edge y 304 | 126.02 | MEASURED |
| Member c outer face to the rail outer edge y -304 | **0.00** (274 + 30 = 304, on the rail top in the notch; 5 clear of the plate, S2-6) | MEASURED, DERIVED |
| Cutter overhang of the keep-out (S2-a) | **2.70** = 88.90 - 86.20 | DERIVED (drill.head_od ASSUMED, Q2) |
| Footprint against the S1 unbolted tip force | lever 304; tip force at COM load 341 N, start 368 N, capture_end 531 N, park 258 N; at frame top 177 N (park 140 N) | MEASURED (S1 r5 = r4) |
| F6 eye limits at r 400 | 492.46 z_S (axis), 578.80 z_S (cutter rim) | DERIVED: 244.84 + 130.00 x 400 / 210; 244.84 + 130.00 x 311.10 / 121.10 |
| S2-5b strike list at load (z_S, margin over 940 z_A) | bearing 1136.84 (136.84), ring 1149.84 (149.84), motor_mount_c 1161.84 (161.84), pinion_c 1168.22 (168.22), motor23_c 1185.34 (185.34), motor_shaft_c 1209.84 (209.84), gear and hub 1242.07 (242.07) | MEASURED |
| Drill tip above the hand band at load | 19.84 (959.84 z_A) | MEASURED |
| Tight spots | ring rim to rod 10.00; ring rim to member face 34.00; lift motors to sector 11.71 | DERIVED, DERIVED, MEASURED |

**Orientation preview (STOP-T5) for Sean, plan `wip/s2_plan_r1.png`:**
- V2: drill tube annulus, keep-out, cutter rim, bearing, gear, gear hub and ring are concentric circles on the origin (S2-4 0.000). Pinion trapezoids, shafts, NEMA 23 bodies and their chain-line axes run radially at 90, 210, 330, narrowing toward the axis, motors outboard.
- Handedness: +X right, +Y up, seen from +Z. Slot line C is the heavy chain line at y +259 on the +Y rail, labelled "+X". Datum B cross in the tube bore carries +X and +Y arrowheads and a theta arc counter-clockwise from +X. Screws a 150 (upper left), b 30 (upper right), c 270 (bottom, member c in the -Y notch); pinions c 90 (top, in the sector), a 210 (lower left), b 330 (lower right); guide rods at 0 and 180; descent-stop pad at 150. Every screw and pinion carries a tag with its letter and azimuth.
- Operator sector: orange wedge theta 90 +- 45 to r 400 toward +Y (slot line C side); F6 sightline at theta 60 with the observer dot at r 400.

S1 r5 poses for V1 to V5: `wip/s1_pose_load_r5.png`, `wip/s1_pose_start_r5.png`, `wip/s1_pose_capture_end_r5.png`, `wip/s1_pose_park_r5.png`.

## 5 S1 r4 / r5 comparison

Values that moved (MEASURED; load pose x in the side view, z unchanged at every pose):

| Quantity | r4 | r5 |
|---|---|---|
| frame_upper.radius | 300 | 274 (Design Notes 27) |
| frame_upper_a drawn x (side view, 60 square at theta 150) | -300.79 to -218.83 | -278.27 to -196.31 |
| frame_upper_b drawn x | 218.83 to 300.79 | 196.31 to 278.27 |
| bracket_anchor_a, bracket_guide_a x | -248.83 to -141.75 | -226.31 to -141.75 |
| bracket_anchor_b, bracket_guide_b x | 141.75 to 248.83 | 141.75 to 226.31 |
| Rows (K9) | 54 | 58 (guide_bushing_a, _b, guide_tie_a, _b; Design Notes 28) |
| guide_tie_a / _b plan x | not drawn | 198.45 to 265.04 / -265.04 to -198.45, z_S 1225 to 1285 |
| Keys read new in r5 | none | guide.bushing_drop 30, bushing_housing_od 40, bushing_length 42, bushing_od 32, bushing_type, top_support |
| figure_note | none | "Not drawn: LM20UU bushing (inside the housing and lug)" on all four poses |
| K2 keys / overlay leaves | 284 / 103 | 322 / 121 |
| K5 artists | 327 | 343 |
| K6 z_rules | 215 | 231 |
| K7 tests | 477 | 609 (LF-c1 swept F +94; G 16 to 0 by the pose-restricted rule) |
| K8 predicates | 330 | 346 |
| S1-5b pairs | 77 | 91 (least 142.00 unchanged) |
| X1 | not run | pass, 47 shared rows |

Unchanged (MEASURED): S1-1 650.00, S1-2 125.00, S1-3 367.34 / 117.34, S1-4 0.84, S1-5a 192.34, S1-5b 142.00, S1-6, S1-7 spare 72.73; park 959.84 z_A, stroke 775.00; mass and tip force (section Corrections 5).

## 6 Open items

1. **Gear tooth ticks (Designer).** Spec shape for `gear` names "tooth ticks on the OD"; K5 and K9 admit no tick artist (section Corrections 4). Drawn: hatched annulus plus chain-dashed pitch circle. Designer to amend the shape text, or raise a rule that admits a tick artist (with its premise check, detail 1 common (h)).
2. **F6 label reads "eye z_S z_S 1600" (Designer, spec defect).** `sightline_f6.label.text` ends in "eye z_S" and `z_S: true` appends " z_S <value>". K4 passes; V8 will read the doubled "z_S". Fix in the spec label text (drop the trailing "z_S"); not changed here.
3. **Highest-point report counts the sightline (Loftsman, Designer).** `wip/s2_summary_r1.md` reports capture_end highest point 1600.00 z_S: the eye end of `sightline_f6` (z_rule to operator.eye_height). The row is a reference line, not a part. Mark it `reference: true` in the spec or exclude kind line from the highest-point report.
4. **Spec status string (orchestrator).** `s2_spec.yaml` status still reads "gear section field added ... (awaiting the Loftsman and Designer at (c)/(e))"; (c) closed with all raisers signed. The status text is a spec edit; not changed here.
5. **Label leaders (M1, V8).** Margin labels sit in one column right of the plan, as in S1; leaders to parts at theta 150 (descent-stop pad) and the six concentric circles cross the drawing. M1 to judge.
6. **Plate drawn as tinted pieces without edges.** K5 requires each base_plate artist to be a rectangle, so the plate outline with its notches shows as the boundary of the tint (pieces drawn edge colour = fill), with the dashed base frame over it. M1 to judge legibility.

## 7 Gameplan lines to change

**l.490** (Progress Log, add a row after it).

Old:
```
| 1.2 | 2026-11-25 | (c) re-signs after P5f: Software Engineer SIGNED (191/191; branch deletion on every FIX), Designer SIGNED (all 5 rules), Loftsman SIGNED (LF-c1; S1 swept 515 to 609 confirmed), Topologist SIGNED (all 4 rules). (c) closed. Next: P6 Engineer draws S2 r1 and S1 r5. |
```
New:
```
| 1.2 | 2026-11-25 | (c) re-signs after P5f: Software Engineer SIGNED (191/191; branch deletion on every FIX), Designer SIGNED (all 5 rules), Loftsman SIGNED (LF-c1; S1 swept 515 to 609 confirmed), Topologist SIGNED (all 4 rules). (c) closed. Next: P6 Engineer draws S2 r1 and S1 r5. |
| 1.2 | 2026-11-25 | (d) P6 (`step1.2_engineer_draw_r1.md`): `s2_plan.py` written; `wip/s2_plan_r1.png` first written 17:57:05; S2 r1 17/17 on run 1; S1 r5 18/18 (four poses, mass report equal to r4); members a, b 43.73 from the plate x edge, member c on the rail edge 0.00; cutter overhang 2.70; controls 191/191 (284 s); --stale red on s1 r4 frame_upper.radius only. Open: gear ticks, F6 label "z_S z_S", sightline in the highest-point report, s2 status text. Next: STOP-T5, (e) and M1 in parallel. |
```
