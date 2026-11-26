## Corrections to the brief

1. **The new K4 rule, as literally worded, makes five S2 labels unplaceable.** "Last quarter outside every other row's true outline" counts outlines that lie under or around the labelled part. Measured on the r6 drawing in a single-leader pass at each label's wanted text position, with the plate exempt because it contains every anchor, five labels have no passing candidate in either column (MEASURED):
   - frame_upper_c: every leader crosses base_plate, because the member sits in the notch.
   - screw_b: leaders cross the anchor brackets on the right and the gear and bearing on the left.
   - descent_stop: leaders cross base_frame and guide_tie_b.
   - keepout and drill_head: leaders cross the gear and ring annuli around them.

   The rule as implemented states a z premise: an outline counts only when its row's z_max is higher than the labelled row's z_max by more than 0.05. Seen from +Z, the leader's end then runs over a nearer part, which is the Design Notes 30 case (tie b z_max 1285 over the pad at 374.84). A row with no z_max counts every outline. An outline that contains the anchor is exempt. Under this premise one label is UNPLACEABLE: drill_head (section 5). Choosing the premise is a rule decision that awaits signature (section 9). I did not choose a design remedy.
2. **The rendered alpha is the face colour's alpha.** The r5 `is_opaque` multiplied the face alpha by the artist alpha. matplotlib already folds a set artist alpha into the face colour, so the operator sector read 0.25 where it renders at 0.5. This did not change any r5 result, because only alpha 1 counted as opaque.
3. **The opaque-fill clause makes three existing B controls fire extra issues.** The brief's hidden rule includes "an opaque fill drawn above". In K8-B6, K8-B32 and K8-B39 the planted figure places an opaque fill over another row, so the clause adds 1, 2 and 2 issues to them (MEASURED). Their planted counts and reasons are updated (section 7). K8-B39's r3 defect, a solid copy under the opaque sector, no longer exists in the renderer drawing. Its plant now hides three plate pieces that stay solid.
4. **One live red stays on every live-S2 K4 control.** The drill_head UNPLACEABLE adds one issue to every K4 control built on the live S2 r6 script. K4-Z3 reads red. K4-B7, B8, B10, B11 and B12 count it in their planted totals. These counts drop by one when the Designer's remedy lands.
5. **S2 r6 also reads RPT red.** RPT (step 0) fails any new record whose spec declares no `reported_items`. s2_spec.yaml declares none, and r6 is a new record, so it is not covered by the exemption for records accepted before RPT. This is not a renderer item. It needs either the S2 Reported list added to the spec (a spec edit for signature) or an orchestrator ruling. It is left open as item R in section 8.
6. **S1 r7 reads 17/18 on both the old and the new library.** K5 is red on the anchor-line zero-area rectangles (the TP1.1-9 lint, the P0T ruling, pending S1 r8). The K3, K4, K5, K7, K8 and K9 results are field-equal between the pre-P1R and post-P1R libraries on the same S1 drawing (MEASURED). P1R adds no S1 red.
7. **The hollow true disks keep their solid outlines (TP1.2-7).** The renderer computes an annulus outline exactly, bore open. drill_tube and drill_head, however, are round centred places whose outlines are solid disks (0, b), and their spec rows give no bore. Opening the tube bore alone would make the dotted cutter rim read as partly visible through the bore, and the cutter has no bore key. Control K8-Z10/B45 exercises the exact hollow-disk case on a section row. TP1.2-7 stays with S3/S6.
8. **Hidden copies stay at their own draw order.** A piece under an opaque fill drawn above it gets its dashed copy beneath that fill, so it remains unseen, as at r5: bearing under the gear fill, guide-block edges under the screw disks. Lifting those copies above opaque fills would show dashed edges over the screws. The Designer decides this convention (section 9).

Tags: run results MEASURED 2026-11-26 on `docs/sketches/`, Python 3.12, matplotlib 3.11.2, 16 logical CPUs. Hand values DERIVED. Thresholds DECLARED (this file) or as in the gameplan.

## 1 Files changed

| Path | What |
|---|---|
| docs/sketches/sketch_common.py | Plan renderer `render_plan`. Exact region split `region_split` (slab decomposition), plus `region_path`, `RegionIndex` and `drawn_region` (an artist's clip region read from the figure). Cover context, `artist_covers`, and `cover_hit`/`cover_hits` (numpy). The alpha rule (`fill_alpha`, `is_opaque` at 0.75, `TRANSLUCENT_MAX` 0.5). `in_rings`/`in_drawn`, which give as-drawn containment in `covering_areas`, `leader_hatch` and the K4 area clause. K8 `cover_issues` clause (2) and the opacity lint. Annulus samples by arc length. Vectorised `_piece_samples` (same samples, same order). `pieces()` skips renderer copies. `style_hidden` now calls `render_plan`. `hidden_rows` uses the exact covers. The leader placer `place_plan_labels`, with `anchor_candidates`, `_LeaderCtx`, `leader_outlines` and `leader_outline_issue`. K4: the outline rule (e), the UNPLACEABLE rule (f), and the UNPLACEABLE tables in the K4 record. |
| docs/sketches/s2_plan.py | Rows drawn as seen: base frame, lift motors, anchor arms and blocks, bushings and bearing lose their pre-set dashes, and the pinion toothed piece is solid. `sc.render_plan` replaces `_hidden_lines`, and `_hidden`/`_hidden_lines` are removed. `sc.place_plan_labels` replaces `place_labels`. Legend line and docstring updated. |
| docs/sketches/fixtures/builders.py | `_s2_draw` uses `render_plan` and `place_plan_labels(margin=False)`. `_s2_replace(render=)` and K8-B22 re-rendered. K4-B8 re-planted. New builders k8_z9 to z12, k8_b44 to b50, k4_b12 and k4_b13. |
| docs/sketches/fixtures/manifest.yaml | 13 new rows. K8-B6, K8-B32, K8-B39, K8-B49, K4-B7, K4-B8, K4-B10, K4-B11 and K4-B12 counts and reasons as in section 7. |

s1_side_poses.py, checks_s1.py, checks_s2.py, check_sketch.py, check_stack.py, sketch_loader.py and both specs are unchanged (SHA-256 section 8). No overlay key moved.

## 2 Renderer design, premise, premise check

**Entry point.** `sketch_common.render_plan(ctx, ax, pose)` is called once per plan figure, after every row is drawn and before the plate outline, tags and labels. It is used by s2_plan.py and by the S2 fixture drawing, and the S3 script calls it the same way.

**Visibility rule.** A point of a drawn area artist is hidden when either of these holds:
- it lies inside the true plan outline (`plan_outline` true) of a row whose z_max is higher by more than 0.05;
- it lies inside an opaque fill of another row drawn above the artist, where opaque means rendered fill alpha ≥ 0.75.

**Procedure.**
- **Which artists.** Every Patch of a measurable row that is not plan_style stand_in.
- **Order.** Artists are taken from the top of the draw order down, so the opaque fills above an artist are final when it is taken.
- **Samples.** The K8 cover samples (section 3), tested against the covers.
  - No sample covered: the artist is unchanged.
  - All samples covered: the artist is restyled in place. It gets "--" (or keeps its own non-solid style, such as the dotted cutter rim and post), no fill, no hatch.
  - Otherwise the artist is split. It keeps its style and gets the visible region as its clip path. A hidden copy gets the hidden region as its clip path. The copy is the same class (Polygon, Circle or Annulus), same edge colour and width, hidden line style, no fill, no hatch, and is inserted in the draw order right after the original.
- **Regions.** `region_split` computes the exact union of the covers and its complement in a box. The box is the artist's bounding box plus 5 mm, with y extended past every cover. The result is two sets of disjoint vertical-sided trapezoids (section 3).
- **Second calls.** A second call takes only unsplit pieces: an artist with a clip path, or a renderer copy, is skipped.

**K8 cover holds by construction.** K8 cover now judges each artist on its drawn region (geometry inside its clip region) and has four clauses:
1. A solid artist whose every drawn sample is hidden fails (r3 rule).
2. A solid artist with a drawn sample hidden by more than 0.05 fails (new, N2).
3. Every uncovered sample of a non-solid artist's geometry lies in the drawn region of a solid artist of the row, under no opaque fill drawn above it (r3/r4 converse).
4. Opacity lint: no plan fill has a rendered alpha in (0.5, 0.75).

The renderer output meets clauses 1 to 3 by the way it is made: the visible clip excludes every covered point (to 0.01 mm at annulus circles), and the hidden copy covers exactly the covered part. Live S2 r6: K8 pass, 206 predicates; K5 121 tagged artists, against 105 at r5 (16 hidden copies, each admitted by its class) (MEASURED).

**Covers on S2 r6.** All MEASURED.
- **Split (clip plus copy), 23 pieces:**
  - base_plate (1 piece) and base_frame (2 rails, notches);
  - guide_a, guide_b, guide_c under the screw disks;
  - bracket_guide_a and bracket_guide_b under the ties;
  - ring, under the guide arms, ties, nut housings, motor mounts, gear, shafts and nuts;
  - nut_housing_a, nut_housing_b, nut_housing_c;
  - pinion_a, pinion_b, pinion_c (toothed piece and hub);
  - motor_shaft_a, motor_shaft_b, motor_shaft_c.
- **Wholly hidden (restyled in place):** nuts, anchors, bracket_anchor_a/b/c, lift motors, descent_stop and its post, motor mounts, guide lugs, bushings, bearing, guide_member and guide_member_b, drill_head.

**Premises and where they are checked.**

| Premise | Statement | Check, Z and B |
|---|---|---|
| Only true outlines cover | A circumscribing footprint (lift motor 42 square in its circle, pinion trapezoid in its rectangle, depth-band disk) is a containment bound for K7 F/G, never a cover. `cover_table` takes `plan_outline(...)[2]` true only. | K8-Z7 (circle drawn as a square: no cover) and K8-B33 (the same motor drawn as its circle covers the pad), both existing and both passing |
| Opaque per the alpha rule | A fill is opaque at rendered alpha ≥ 0.75 (DECLARED): what lies under shows at a quarter of its contrast or less. A fill counted see-through renders at ≤ 0.5, so what lies under shows at half its contrast or more. The band (0.5, 0.75) is refused. | K8 cover clause (4). Z: live S2 r6 (alphas 1 and 0.5), K8-Z8. B: K8-B50, sector 0.6. Threshold B: K8-B49, sector 0.95, opaque, hides the plate it draws over. |
| Drawn region read from the figure | A piece's drawn region is its geometry inside its own clip path (`Artist.get_clip_path`, converted to data). An artist with no clip path of its own draws everywhere. | K8-B48 (clip removed: fires), K8-Z8 |
| Piece rings convex | `_inside` is a convex test (as in K7). The renderer's slab split uses crossing parity and takes any ring. | K7 convexity guard (existing) |

## 3 Sampling changes (TP1.2-13, TP1.2-19)

- **Exact covered region.** The renderer computes the union of covers as a union, not from vertex samples. Each cover becomes a shape:
  - an annulus outline (a, b): outer ring an inscribed polygon with sagitta ≤ 0.01 mm, bore ring circumscribed, so the bore is open and the hidden region lies inside the true annulus;
  - a convex piece: itself;
  - an opaque fill: its rings, intersected with its clip trapezoids when it is itself a split piece.

  `region_split` places vertical slab edges at every vertex x and at every x where edges of two shapes cross (vectorised segment intersection). Within a slab every edge is one line and the crossing order is fixed, so the union is merged per slab at mid-x. The result is trapezoids merged along x while their bounding edges continue.
- **Check side.** The tests are exact per sample. An annulus is tested as r in [a, b], a convex piece by half-planes, an opaque fill by even-odd rings plus its clip region, and a union as "any cover". `hidden_rows` now samples outlines the same way.
- **Annulus samples step by arc length.** Directions are spaced at most 2.5 mm of arc at the outer radius, on the same five rings across the width. On the ring (r 210) that is 528 directions and 2640 samples, against 128 directions (about 10.3 mm of arc) at r5 (DERIVED). The arc length depends on the radius; the brief's 20.6 mm figure is for the outline sampling.
- **Clause (2) tolerance.** A drawn sample counts as covered only when it is more than 0.05 inside a cover. A point on a shared boundary, or inside a 0.01 mm sagitta sliver, does not fire.
- **Speed.** Grid samples and cover tests are vectorised in numpy. The `_piece_samples` grid gives the same points in the same order as the loop (r6 pixels identical before and after vectorising, MEASURED). The live S2 K8 cover test takes 1.3 s.

## 4 Placer design, order, new rule with premise

**One function, `sketch_common.place_plan_labels(ax, ctx, pose, margin, stack_pose, notes)`, places every plan label.**

**Candidates per label, in this deterministic order:**
1. Column: the row's `label_side` first (right when unset), then the other column.
2. Within a column, anchors in this order:
   1. the ray hit at `label_theta`, when the row sets it and the ray meets its ink;
   2. the column default: (max x, mid y) of the ink for the right column, (min x, mid y) for the left, or the extreme vertex nearest mid y when that point is off the ink;
   3. every ink sample, at most 2 mm apart along each ink edge (`ANCHOR_STEP`, DECLARED), the column edge first and then by distance from the default anchor, with duplicates dropped.

**A candidate passes when its leader passes every K4 leader rule:**
- (a) it ends on the row's ink within 0.05;
- (a') the anchor is under no area of another row drawn above the row's ink;
- (c) no area is drawn above the leader;
- (d) at most 0.25 of the end-quarter samples lie in other rows' hatch;
- (e) the new outline rule (below);
- (b) it does not cross another leader;
- in margin mode, a left-column text box does not overlap a y tick label. This is a placer rule; without it the descent-stop text sat on the "100" tick.

Text inside the saved image is K3's rule: a margin column lies inside the tight bounding box the script saves, and K3 reads that premise.

**Layout steps:**
1. Labels are taken in spec row order. Each takes the first candidate that passes at its wanted text position (column x, anchor y).
2. Both columns are stacked (`_stack_z`, gap 0.5 line), and every leader is re-judged at its stacked position, crossings included.
3. A label that fails there takes, in candidate order, the first candidate whose stacked layout gives it no failure and adds none to another label. At most 3 rounds.
4. A label with no passing candidate is **UNPLACEABLE**. It is drawn at its first candidate and recorded with its candidate table (column, source, anchor, first failing rule and detail) in `ax._sc_placer`. The table is copied into the K4 record (`unplaceable`), and K4 fails it with reason "label unplaceable" without judging it again under (a) to (e). There is no silent fall-back.

**New rule (e), `leader_outline_issue`.** The last quarter of a plan leader, sampled at most 0.5 mm apart with the anchor end excluded, lies outside every true plan outline of a row that meets both conditions:
- its z_max is higher than the labelled row's z_max by more than 0.05;
- its outline does not contain the anchor (within 0.05).

Premises:
1. The anchor is on the row's ink (K4 (a)).
2. Only nearer parts count. Seen from +Z, a leader end over a higher part reads as pointing at it, which is the Design Notes 30 case (tie b). Lower parts lie behind the labelled part and every leader crosses them: the plate, the base frame, the ring under the gear. A row with no z_max (a zone) counts every outline.
3. An outline that contains the anchor is exempt. That covers a part seated on or in another, and a hidden part under its cover: no leader can end on that ink without entering it.

Z: K4-Z3, live S2 r6. It is red only through the drill_head UNPLACEABLE; every other leader passes rule (e). B: K4-B12, the Design Notes 30 leader. The literal-rule measurement is in Correction 1.

## 5 S2 r6 results and pixel change table; UNPLACEABLE list

**check_sketch.py s2 --rev 6:** 17 of 19 rows pass (MEASURED).
- K1 to K3 and K5 to K9 pass: K5 121 artists, K7 1292 plan pair tests, K8 206 predicates.
- S2-1 to S2-6 pass. S2-6 reads 3 members seated; S2-5a has a least margin of 11.71 mm and S2-5b of 19.84 mm, both unchanged from r5.
- X1 passes.
- **K4 fails**, on one label only: load/drill_head, label unplaceable.
- **RPT fails**: spec declares no reported_items (Correction 5).
- `--stale` finds no key moved. Files: `docs/sketches/wip/s2_plan_r6.png` (1505 x 2332 px, SHA-256 916a4f84…5d79), `wip/s2_checks_r6.json`, `wip/s2_summary_r6.md`.

**Placed labels** (MEASURED, placer record). Leaders that moved against r5:

| Label | Column | Source | Anchor | Note |
|---|---|---|---|---|
| ring | right | ink | (209.75, -10.33) | r5 anchor (210, 0) ends 19.9 mm inside guide_member (z 1272 over the ring at 1161.84) |
| descent_stop | left | ink | (-166.21, 112.12), pad side edge | r5 anchor ends 36.5 mm inside guide_tie_b (DN30); the label_theta 150 hit fails hatch (frame_upper_a); the first ink candidates put the text over the y = 100 tick label |
| drill_head | right | label_theta (first candidate) | (88.9, 0) | UNPLACEABLE, drawn at the first candidate |

The other 11 labels take their first candidate, default or label_theta. Their text heights move with the stack.

**UNPLACEABLE: drill_head ("cutter OD ASSUMED 177.8").**
- **Candidates:** 640, 320 per column, all failing (e).
- **Outlines entered by the last quarter** (count of candidates): gear 446, ring 418, drill_tube 210, motor23_a/b and motor_mount_a/b 32 each, nut_housing_a/b 28 each, guide_a/b and nut_a/b 22 each, motor_shaft_a/b 15 each.
- **Geometry (DERIVED).** The cutter rim at r 88.9 lies inside the gear annulus (90 to 126.32, z_max 1275.84, above the head at 1126.21). Only gear_hub (76.2 to 90) contains the anchor, so only the hub is exempt. Every column leader's last quarter is at least about 70 mm long and crosses the 36.3 mm gear wall.
- **First rows of the table** (`wip/s2_checks_r6.json`, K4 `unplaceable["load/drill_head"]`):

| Column | Source | Anchor | Fails |
|---|---|---|---|
| right | label_theta | (88.90, 0.00) | end inside outline / gear 36.0 mm, ring 58.5 mm |
| right | ink | (88.81, -1.76) | end inside outline / gear 36.2 mm, ring 58.6 mm |
| right | ink | (88.81, 1.76) | end inside outline / gear 36.2 mm, ring 58.6 mm |
| right | ink | (88.73, -3.51) | end inside outline / gear 36.3 mm, ring 58.6 mm |
| left | (320 rows) | rim samples | end inside outline / gear, ring or drill_tube |

This goes to the Designer (P1Rd). I chose no remedy.

**Pixel change table.**
- **Basis.** s2_plan_r6.png against docs/sketches/s2_plan_r5.png. r5 is 1487 x 2362 px and r6 is 1505 x 2332 px: the legend gains a line and the longest legend line is shorter. The comparison runs on the common top-left window (the title and left label column fix the left and top edges); in-memory rebuild = wip r6 (MEASURED).
- **Total.** 414,569 changed pixels of 3,467,684.
- **Attribution.** Changed pixels inside each row's footprint mask: r6 geometry, fill on, line width 3, clip ignored. Overlapping rows count a pixel once per row.

| Row | Changed px | Cause |
|---|---|---|
| base_plate | 308,601 | plate tint removed under every nearer part's true outline (unfilled parts now read white) |
| ring | 177,845 | rim dashed and fill removed under arms, ties, housings, mounts, shafts, nuts, gear |
| base_frame | 134,342 | rails: visible notch parts by clip (r5 used solid copies), rest dashed |
| operator_sector | 78,868 | plate tint under the sector removed where parts sit |
| drill_head | 46,705 | inside the plate change (cutter disk area) |
| keepout | 44,580 | inside the plate change |
| base_spigot_hole | 38,713 | inside the plate change |
| bearing | 17,142 | plate/ring fill change around it |
| gear_hub | 15,211 | same |
| guide_tie_a / _b | 15,075 / 15,065 | arm parts under the ties dashed; plate tint removed |
| motor23_a / _c | 9,259 / 8,981 | ring and plate tint removed under the motors |
| motor_mount_a / _b / _c | 8,468 / 8,471 / 8,098 | same |
| bracket_guide_a / _b / _c | 7,855 / 7,891 / 6,770 | parts under ties dashed; tint removed |
| bracket_anchor_a / _b / _c | 7,818 / 7,850 / 6,770 | tint removed (inside the arm outlines) |
| drill_tube | 5,482 | tint removed in the bore (under the drill_head solid disk, TP1.2-7) |
| nut_housing_a / _b / _c | 4,137 / 4,107 / 4,041 | parts under the guide blocks and screws dashed |
| liftmotor_a / _b / _c | 3,803 / 3,789 / 3,653 | tint removed |
| guide_lug_a / _b, guide_bushing_a / _b | 3,553 / 3,484, 2,849 / 2,830 | tint removed |
| pinion_a / _b / _c | 3,283 / 3,409 / 2,796 | the part under the gear is now a clipped hidden copy (r5: dashed piece plus a solid copy under the gear fill) |
| guide_a, _b, _c; nut_*, anchor_* | about 3,000 each | tint removed |
| descent_stop, descent_stop_post | 2,339 each | tint removed; old leader end gone |
| label:sightline_f6, descent_stop, guide_tie_a, drill_head, frame_upper_c, drill_tube, operator_sector, frame_upper_b, base_plate, keepout, slot_line_c, screw_b, ring, gear | 1,463 to 225 | leaders and texts moved (descent_stop and ring anchors; restacked column) |
| frame_upper_a/b/c, motor_shaft_a/b/c, screws, pinion axes, slot_line_c, collet_axis, pockets | 39 to 1,269 | edge antialiasing at changed neighbours; shaft inner ends dashed under the gear |

Row with no changed pixel in its footprint: slot_lines. Every other row's footprint holds some changed pixels, mostly from the plate tint and ring fill removed around it. The full per-row list is in the session scratchpad `pixdiff.log` (86 lines). Sub-artists are counted with their row: gear:ticks with gear, base_plate:outline with base_plate.

## 6 S1 r7 equality

- **Scripts.** s1_side_poses.py is unchanged and does not call the renderer or the placer. It keeps `place_labels`.
- **Pixels.** `s1_side_poses.py --rev 7` gives all four PNGs pixel-equal to docs/sketches/s1_pose_{load, start, capture_end, park}_r7.png (numpy array equality, MEASURED).
- **Checks.** `check_sketch.py s1 --rev 7` reads 17/18: every check passes except K5, which is red on the anchor-line zero-area rectangles (P0T ruling, pending S1 r8). X1 and RPT pass, RPT exempt.
- **Library equality.** K3, K4, K5, K7, K8 and K9 on the same S1 drawing give equal result, reason, n_issues and measured under the save-point-1 library and the P1R library (MEASURED). The shared changes that reach S1 are as-drawn containment, even-odd for multi-ring patches and clip regions; S1 has no Annulus artists and no clip regions.
- **Record.** wip/s1_checks_r7.json differs from the accepted record in these fields:
  - K2, K7 and RPT reason text (step 0);
  - K5 result, from the step 0 lint;
  - b_result/z_result tallies, timestamp, files_sha256, accepted fields.

  None of these is from P1R.

## 7 Control table

Each new B was run first on its planted figure with the K check of the save-point-1 `sketch_common.py` (copy taken before the first P1R edit). In every case the pre-P1R check did not report the planted defect: it read clean, or fired other issues without the planted reason (MEASURED, `redfirst.py` in the session scratchpad).

| ID | Planted | Reason substring | Pre-P1R check on the plant | P1R result |
|---|---|---|---|---|
| K8-Z9 | bar r 80 to 160 crossing an annulus cover r 100 to 130, rendered | (Z) | n/a | clean |
| K8-B44 | same bar solid, unsplit | "fixture/c cover: Polygon partly covered drawn solid", "under u by more than 0.05" | pass, clean | fires 1, match |
| K8-Z10 | bar r 10 to 50 from the bore into a hollow disk r 40 to 60, rendered | (Z) | n/a | clean |
| K8-B45 | same bar solid, unsplit | "…partly covered drawn solid", "under t by more than 0.05" | pass, clean | fires 1, match |
| K8-Z11 | bar under two overlapping covers a, b, rendered | (Z) | n/a | clean |
| K8-B46 | same bar solid, unsplit | "…partly covered drawn solid", "under a, b by more than 0.05" | pass, clean | fires 1, match |
| K8-Z12 | ring r 100 to 110 visible only in two 3 mm strips at 4.225 and 184.225 deg, rendered | (Z) | pre-P1R K8 fails: "ring wholly under p, q drawn solid" (the r4 false hide) | clean |
| K8-B47 | same ring wholly dashed | "fixture/ring cover: Annulus partly visible drawn dashed" | pass, clean (r4 directions every 2.8125 deg miss the strips) | fires 1, match |
| K8-B48 | live S2 r6, ring clip removed, hidden copy deleted | "load/ring cover: Annulus partly covered drawn solid", "bracket_guide_a" | fires 3 on guide_a/b/c (old checks ignore clip regions), no ring issue: planted defect not reported | fires 1, match |
| K8-B49 | live S2 r6, sector alpha 0.95 | "load/base_plate cover: Polygon partly covered drawn solid", "operator_sector" (planted 3, one per plate piece under the sector) | fires 3 (guide_a/b/c), no sector or plate issue | fires 3, match |
| K8-B50 | live S2 r6, sector alpha 0.6 | "load/operator_sector cover: fill alpha 0.60 between 0.5 and 0.75" | fires 3 (guide_a/b/c), no alpha issue | fires 1, match |
| K4-B12 | live S2 r6, descent-stop label on the r4/r5 leader (anchor (-201.20, 81.52), text in the left column at the anchor height) | "load/descent_stop: label leader ends inside the outline of guide_tie_b", "load/drill_head: label unplaceable" (planted 2) | pass, clean | fires 2 (tie b 38.4 mm of the last quarter), match |
| K4-B13 | pad wholly under an opaque lid drawn above it, placer run | "fixture/pad: label unplaceable" | fails "label anchor (170.00, 0.00) under the area of lid" (silent fall-back, no unplaceable) | fires 1 (62 candidates), match |

**Existing controls changed by P1R** (no new red-first; the cause is stated):

| ID | Change | Cause |
|---|---|---|
| K8-B6 | planted 1 to 2, reason adds "plan/screw_b cover: Circle wholly under screw_c drawn solid" | screw_b planted onto screw_c; screw_c's opaque fill drawn above hides it (alpha rule) |
| K8-B22 | fixture re-renders the replaced pinion pieces (`_s2_replace(render=True)`) | the planted defect is the taper; unsplit pieces would add two N2 issues |
| K8-B32 | planted 1 to 3, reasons add screw_a and guide_a "wholly under nut_a" | the planted filled nut is an opaque fill drawn above both |
| K8-B39 | reason to "load/base_plate cover: Polygon partly covered drawn solid", "under operator_sector by more than 0.05"; planted 3 | r6 has no solid copy under the sector; the opaque sector now hides three plate pieces that stay solid |
| K4-B7 | crossing reason now "operator_sector and sightline_f6 cross"; adds unplaceable; planted 3 | placer draws labels in spec order; live drill_head red |
| K4-B8 | re-planted: drill_tube and keepout at their r1 anchors (r, 0) with their placed texts exchanged, one crossing; planted 2 | with label_theta removed the placer finds non-crossing anchors, so the r1 plant no longer crosses |
| K4-B10, K4-B11 | planted 1 to 2 | live drill_head UNPLACEABLE |
| K4-Z3 | unchanged; reads red | live drill_head UNPLACEABLE (Correction 4) |
| K8-Z8, K4-Z3 desc | now the renderer and placer drawing | |

**Controls:** 276 (Z 74, B 200, smoke 2), up from 263. Z 73/74 clean (K4-Z3 red as stated), B 200/200 fired and matched, smoke 2/2. Wall time 107.3 s at the default 12 jobs (MEASURED).

## 8 Run table

| Run | Result | Wall (MEASURED) |
|---|---|---|
| check_sketch.py --controls (default, 12 jobs) | 276 controls: Z 73/74, B 200/200, smoke 2/2; one mismatch, K4-Z3 (drill_head UNPLACEABLE) | 107.3 s |
| s2_plan.py --rev 6 | wip/s2_plan_r6.png | 14 s |
| check_sketch.py s2 --rev 6 | 17/19: K4 fail (drill_head unplaceable), RPT fail (no reported_items) | 29 s |
| s1_side_poses.py --rev 7 | four PNGs pixel-equal to the accepted r7 | n/a |
| check_sketch.py s1 --rev 7 | 17/18 (K5 red, pre-existing; P1R-neutral, section 6) | 18 s |
| check_sketch.py --stale | 2 records, 0 differences; X1 pass | 4 s |
| check_sketch.py --stale --include-unaccepted | 11 records, 0 differences | 4 s |

**SHA-256** of committed files under docs/sketches/ (wip/ and __pycache__ excluded; 57 files), before the first edit and after the last run. Four files differ, all edited on purpose; no other difference.

| File | Before | After |
|---|---|---|
| sketch_common.py | 2e47d361…21118 | 4685bce0…9b6f |
| s2_plan.py | b37e498d…9b5e | afda3bfc…8f60 |
| fixtures/builders.py | 3f15ad86…b56b8 | 0759d002…ecd5a |
| fixtures/manifest.yaml | ec8f6d28…b2e | 6b569207…010f |

**Open run items:** (R) RPT on S2 r6 (Correction 5); (U) drill_head UNPLACEABLE to the Designer. Until both close, S2 r6 cannot be accepted (`--accept` refuses a record with any check not pass).

## 9 Rules awaiting signature

**The Topologist (renderer and sampling):**
1. Visibility rule: true outline higher by more than 0.05, or opaque fill drawn above.
2. Premise "only true outlines cover" (K8-Z7/B33).
3. Alpha rule: opaque at rendered alpha ≥ 0.75, see-through at ≤ 0.5, band (0.5, 0.75) refused by lint (K8-B49, K8-B50). The rendered alpha is the face colour alpha (Correction 2).
4. Exact region split: slab decomposition; annulus polygons inscribed outside and circumscribed at the bore, sagitta 0.01; covered region a union.
5. K8 cover clause (2): a solid artist with a drawn sample covered by more than 0.05 fails (K8-B44 to B46, B48).
6. Drawn region = geometry inside the artist's own clip path, read from the figure.
7. Annulus samples by arc length ≤ 2.5 mm (K8-Z12/B47).
8. `pieces()` leaves out renderer copies.
9. TP1.2-7 left with solid disks (Correction 7).

**The Designer (conventions and placer):**
1. Hidden pieces drawn dashed (or keeping their own dotted style), no fill, no hatch, clipped to the hidden region; visible part as styled. The plate tint and ring fill are removed under nearer parts' outlines (section 5 table).
2. Hidden copies stay at their own draw order (Correction 8).
3. Placer candidate order and layout steps (section 4); left-column text clear of the y tick labels.
4. Rule (e) with its z premise and anchor exemption (Correction 1).
5. The UNPLACEABLE record and K4 reason.
6. Remedy for drill_head (section 5 table).
7. N2 reading on S2 r6: ring rim dashed under the guide arms.

## 10 Gameplan lines to change

**l.138 (K4 row), rule cell.**

Old:
```
a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1) |
```
New:
```
a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking; left-column text clear of the y tick labels); (e) the last quarter of a plan leader lies outside every true plan outline of a row higher than the labelled row by more than 0.05 that does not contain its anchor (Design Notes 30; premises: anchor on ink, nearer parts only, anchor-containing outlines exempt); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back |
```

**l.138 (K4 row), B cell.**

Old:
```
K4-B11 an area of another row over an anchor |
```
New:
```
K4-B11 an area of another row over an anchor; K4-B12 the descent-stop leader at the r4/r5 anchor (38.4 mm of its last quarter inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B8 re-planted at 1.3 P1R (r1 anchors with exchanged texts); K4-Z3, B7, B8, B10 to B12 carry the live drill_head UNPLACEABLE until the Designer's remedy |
```

**l.142 (K8 row), rule cell.**

Old:
```
within 0.05 (Designer sign-off r3) |
```
New:
```
within 0.05 (Designer sign-off r3); 1.3 P1R plan renderer (sketch_common.render_plan, one entry point per plan figure): hidden = inside the true outline of a row higher by more than 0.05 or inside an opaque fill (rendered alpha >= 0.75) of another row drawn above; covered region exact (annulus as annulus with its bore, union as union; slab decomposition, circle sagitta 0.01); a partly covered piece keeps its style inside its visible clip region and a dashed unfilled copy draws its hidden region; cover samples are judged inside each artist's clip region; cover (2): a solid artist with a drawn sample covered by more than 0.05 fails (N2); annulus samples by arc length at most 2.5 mm (TP1.2-19); alpha-rule premise: no plan fill alpha in (0.5, 0.75) |
```

**l.142 (K8 row), B cell.**

Old:
```
B43 frame "polar" |
```
New:
```
B43 frame "polar"; K8-Z9 to Z12 and B44 to B47 (annulus cover, hollow disk with its bore, union of covers, annulus arc sampling: rendered Z, unsplit or wholly dashed B); B48 renderer bypassed for the ring (rim solid under the guide arms, N2); B49 sector alpha 0.95; B50 sector alpha 0.6; at 1.3 P1R K8-B6, B32, B39 counts and the B39 reason re-read under the opaque-fill clause, B22 re-rendered |
```

**l.146 (K table pointer).**

Old:
```
RPT-B3 to B6 and re-planted H1-B8 (263 controls: Z 70, B 191, smoke 2; 111 s at --jobs 12).
```
New:
```
RPT-B3 to B6 and re-planted H1-B8 (263 controls: Z 70, B 191, smoke 2; 111 s at --jobs 12). Step 1.3 P1R (`research/sean/cr_scratch/step1.3_engineer_renderer.md`) added K8-Z9 to Z12, K8-B44 to B50, K4-B12, K4-B13 and re-planted K4-B8 (276 controls: Z 74, B 200, smoke 2; 107.3 s at --jobs 12; K4-Z3 red on the drill_head UNPLACEABLE until the Designer's remedy).
```

**l.296 (detail 1.3 carried items), item (4).**

Old:
```
(4) (c) rule with Z and B, then (d): N2 hidden-line renderer, solid pieces under unfilled covers drawn dashed (ring rim under the guide arms, fresh M1 S2 r3 N2), including the descent-stop leader whose last 60.1 mm runs inside tie b (Design Notes 30); S2 re-runs under (i); The Engineer, with The Designer and The Topologist;
```
New:
```
(4) (c) rule with Z and B, then (d): N2 hidden-line renderer, solid pieces under unfilled covers drawn dashed (ring rim under the guide arms, fresh M1 S2 r3 N2), including the descent-stop leader whose last 60.1 mm runs inside tie b (Design Notes 30); S2 re-runs under (i); The Engineer, with The Designer and The Topologist; plan renderer and leader placer done at P1R (`research/sean/cr_scratch/step1.3_engineer_renderer.md`): S2 r6 drawn (ring rim dashed under the arms; descent-stop leader re-anchored on the pad side edge, clear of tie b), K4 red on the drill_head UNPLACEABLE (to the Designer, P1Rd) and RPT red (S2 spec has no reported_items); signatures P1Rt, P1Rd; section-view convention at P4;
```

**l.666 (Design Notes 25, TP1.2-13 row).**

Old:
```
| TP1.2-13 (cover over-cover) | K8 cover and hidden_rows sample piece vertices: a union of covers, an annulus cover or a hollow true disk (TP1.2-7) can mark a partly visible piece hidden; never passes a solid hidden part; live: base_frame rail top in the +Y notch (70 x 60) drawn dashed while visible; visible-drawn-dashed is unchecked | 1.3 (S3) | The Topologist proposes; The Engineer |
```
New:
```
| TP1.2-13 (cover over-cover) | K8 cover and hidden_rows sample piece vertices: a union of covers, an annulus cover or a hollow true disk (TP1.2-7) can mark a partly visible piece hidden; never passes a solid hidden part; live: base_frame rail top in the +Y notch (70 x 60) drawn dashed while visible; visible-drawn-dashed is unchecked. 1.3 P1R: covered region exact (annulus with its bore, union as union) in the renderer and per sample in K8; K8-Z9 to Z11, B44 to B46; drill_tube and drill_head outlines stay solid disks (TP1.2-7, no bore key for the cutter); awaiting P1Rt signature | 1.3 (S3) | The Topologist proposes; The Engineer |
```

**l.667 (Design Notes 25, TP1.2-18/19 and N2 renderer row).**

Old:
```
| TP1.2-18, TP1.2-19 (cover limits), N2 renderer | stand_in_owner must name a Step or sketch id (1.3 step 0, K8-B42, signed P0T; overlay-key form deferred to S3 stand-ins); annulus cover samples step by angle (about 20.6 mm at r 210), not the 2.5 mm cap; is_opaque needs alpha 1; solid pieces under unfilled true covers (ring rim under the guide arms) draw no dashed hidden arc (Engineer r4 Correction 3); the descent-stop leader runs 60.1 mm inside tie b (Design Notes 30) | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer co-owns the renderer |
```
New:
```
| TP1.2-18, TP1.2-19 (cover limits), N2 renderer | stand_in_owner must name a Step or sketch id (1.3 step 0, K8-B42, signed P0T; overlay-key form deferred to S3 stand-ins); annulus cover samples step by angle (about 20.6 mm at r 210), not the 2.5 mm cap; is_opaque needs alpha 1; solid pieces under unfilled true covers (ring rim under the guide arms) draw no dashed hidden arc (Engineer r4 Correction 3); the descent-stop leader runs 60.1 mm inside tie b (Design Notes 30). 1.3 P1R: annulus samples by arc length at most 2.5 mm (K8-Z12, B47); alpha rule opaque at rendered alpha >= 0.75, band (0.5, 0.75) refused (K8-B49, B50); renderer splits partly covered pieces (K8-B48); descent-stop leader placed clear of tie b (K4-B12); drill_head label UNPLACEABLE under the new leader rule; awaiting P1Rt and P1Rd signatures | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer co-owns the renderer |
```
