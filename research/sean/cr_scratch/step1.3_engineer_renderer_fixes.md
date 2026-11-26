## Corrections to the brief

1. **Stand-in ink counts as visible ink under (e1).** In DR-1, the first run of D1 made guide_tie_a UNPLACEABLE: 374 candidates, every one "anchor on hidden ink". The renderer leaves the ties out (plan_style stand_in), so they have no solid artist, and (e1) found no visible ink. Fix: `row_visibility` counts the convention line of a stand_in row as its visible ink. K8 cover already exempts that line. This is a premise of D1 that the Designer did not state; it awaits the Designer's re-check. With it, DR-1 passes.
2. **K4-B16 cannot be red-first on the plant's own reason alone.** The P1R code has no enclosure exemption, so it reports "drill_head leader ends inside the outline of gear" on the planted figure, for its own reason. K4-B16 is red on the P1R code only through the missing (g) line. On the r7 drawing, the open-C gear no longer encloses the anchor, so the "under ring gear" suffix names no cover and (g) also fires (planted 2). The Designer forecast "unplaceable" on the P1R code; the measured P1R result is the gear line (section 3).
3. **K4-B8 was re-planted again.** The P1R plant exchanged the placed texts of drill_tube and keepout. In r7 the drill_tube text sits above the keepout text, so the exchange no longer crosses (MEASURED: clean). The P1Rf plant sets both texts below the anchors in reverse radial order. The two leaders cross, and the lowered keepout text also crosses the ring leader (planted 2).
4. **K4-B11 now fires (e1) as well.** Its planted white fill over the drill_tube anchor hides that anchor's ink, so (e1) fires beside "under the area of ring". The planted count stays 2: the drill_head UNPLACEABLE line has gone, and (e1) takes its place.
5. **Topologist dry-run counts reproduced.** Cover (5) is reported once per artist. K8-B6, B32, B39 and B49 read 3, 5, 7 and 7, as in the Topologist's `sk2` dry-run.
6. **For narrow annuli, TP1.3-1 keeps the r6 sample set.** When the width needs no more than five fractions (width ≤ 10 mm), the five COVER_RINGS fractions are kept exactly, so r6 samples are unchanged there. Wider annuli step at ≤ 2.5 mm across the width: the ring has 45 fractions × 528 directions = 23,760 samples.
7. **S2 r7 is wider than r6.** The image is 2634 px wide, against 2332 at r6: the left column grows leftward with the longer descent-stop text. K3 passes on it.

Tags: runs MEASURED 2026-11-26, Python 3.12, matplotlib 3.11.2. Dry-runs ran in a scratchpad copy of `docs/sketches/` with a copy of `params.yaml` above it (`scratchpad/p1rf/sketches`). Red-first used the P1R `sketch_common.py` (`scratchpad/p1rf/pre_p1rf`, copied before any P1Rf edit). Values from the overlay are DECLARED or ASSUMED as tagged there.

## 1 Dry-run table

| Dry-run | FIX | Expectation | Result (MEASURED, copy) | Outcome |
|---|---|---|---|---|
| DR-1 | D1, D2 | K3 passes with both longer texts inside the image | K3 pass | PASS |
| | | K4 with no UNPLACEABLE | K4 pass, 14 labels, `unplaceable` empty (after Correction 1) | PASS |
| | | drill_head in the right column at (88.90, 0.00) | right, label_theta, (88.90, 0.00); wholly hidden. Last quarter enters ring 59.1 mm (encloses), gear 36.3 mm (encloses), bearing 10.9 mm (contains), gear_hub 1.0 mm (contains) | PASS |
| | | descent_stop inside bracket_guide_a and ring only, no tie b | left, ink, (-166.21, 112.12); wholly hidden. Enters bracket_guide_a 50.2 mm (contains) and ring 10.9 mm (contains); no tie b | PASS |
| | | ring on visible rim outside tie a and guide_member | right, ink, (205.96, -40.97), visible ink; no counted outline entered | PASS |
| | | K4-Z3 clean | clean | PASS |
| | | K4-B7, B8, B10, B11, B12 planted counts each down by one | B7 3→2, B10 2→1, B12 2→1. B11 stays 2 ((e1) replaces the drill_head line; Correction 4). B8 re-planted (Correction 3) | PASS with stated changes |
| | | K4-B12 still fires on tie b | "descent_stop: label leader ends inside the outline of guide_tie_b (38.4 mm)" | PASS |
| | | B14 to B16 fire and match | match after counts B14 3, B15 1, B16 2 (section 3) | PASS |
| DR-2 | D3 | K5 admits the stand_in rows with the new dash | K5 pass, 121 artists | PASS |
| | | K8: stand_in rows stay out of the renderer; cover clause 3 does not apply to the phantom style | K8 pass, 206 predicates. The phantom tuple linestyle is non-solid (`is_solid` false) and exempt under stand_in, as the r6 dashes were | PASS |
| | | K8-B42 and every stand_in control pass | K8-B35, B41, B42 match | PASS |
| | | K4 figure note and the legend | K4 pass. Legend line "phantom, brown: Step 2 stand-in (rod top ties)" | PASS |
| | | S1 r7 pixel equality | four PNGs pixel-equal | PASS |
| DR-3 | reported_items | RPT green | "12 reported item(s) declared, every one has a value" | PASS |
| | | values equal the Designer's r6 column | all 12 equal (table below) | PASS |
| | | `--stale` clean | 2 records, 0 differences | PASS |
| | | RPT controls unchanged | RPT-Z, Z2, Z3 and B1 to B6 match | PASS |
| TP1.3-1 | annulus radial step | live render states and PNG unchanged; K8-B52 fires; Z clean | K8-B52 fires "Annulus partly covered drawn solid (24 of 23760 drawn samples under d by more than 0.05)"; K8-Z13 clean; S2 K8 pass with 206 predicates | PASS |
| TP1.3-2 | cover (5) | K8-B51 fires 3; B6, B32, B39, B49 read 3, 5, 7, 7; Z clean | as expected; live S2 K8 clean | PASS |

**DR-3 values** (r7 against the Designer's r6 column):

| id | r7 value | Designer r6 |
|---|---|---|
| outline_extents_all | x -322.00 to 322.00, y -304.00 to 304.00 | same |
| outline_extents_above_plate | x -278.27 to 278.27, y -304.00 to 218.00 | same |
| members_to_plate_edge | a, b 43.73 inside the x edge 322; c 0.00 to the plate y edge -304 | same |
| tip_force_footprint | 341 / 368 / 531 / 258 N over lever 304 | same |
| cutter_overhang | 2.70 | 2.70 |
| f6_eye_limits | 0.49 m (axis), 0.58 m (cutter rim) z_S (DERIVED 0.492, 0.579) | same |
| s2_5b_strike_list | drill_head 1019.84 to 1126.21 (19.84) least, then 9 more rows | drill_head 19.84 least |
| tight_rim_to_rod | 10.00 | 10.00 |
| tight_rim_to_member | 34.00 | 34.00 |
| tight_liftmotor_sector | 11.71 (bound) / 15.69 (drawn square) | same |
| tight_pinion_toe_hub | 5.22 | 5.22 |
| highest_point_parts | load 1819.84, start 1694.84, capture_end 1285.00, park 1819.84 z_S | same |

**f6_eye_limits basis (DERIVED).** The line runs from the cut at capture_end (drill_head z_min 244.84 z_S, at r 0 or r 88.9) through the ring rim (r 210, ring z_min 374.84) to r 400. The ring top (386.84) would give 0.52 m and 0.61 m. The ring bottom reproduces the Designer's values.

No FIX failed its dry-run. Every FIX landed.

## 2 Fix table with controls

| FIX | Change (files) | Controls |
|---|---|---|
| D1 (rule (e), clause (g)) | sketch_common.py: `outline_encloses`, `counted_outlines`, `row_visibility`, `anchor_visibility_issue` (e1), `cover_name_issue` (g). The rule (e) exemption is now enclosure (outer boundary with holes filled; containing implies enclosing). The placer rejects a hidden-ink anchor for a row with visible ink. K4 reports (e1) and (g) on plan leaders. Premise: stand-in ink counts as visible ink (Correction 1) | K4-Z3 clean; K4-B14, B15, B16 |
| D2 (label suffixes) | s2_spec.yaml: drill_head `suffix: "(dotted, under ring gear)"`; descent_stop `suffix: "(dashed, under top-guide bracket arm)"`; status line | K4-B15 (suffix removed) |
| D3 (stand-in line) | sketch_common.py: `PHANTOM = (0, (12, 3, 3, 3, 3, 3))`, `STAND_IN_COLOR = "#8c510a"` (shared constants; K1 reads the script only). s2_plan.py: ties drawn with them; legend line. s1_side_poses.py unchanged (S1 at r8) | K5, K8-B35, B41, B42 (existing) |
| Designer section 5 (RPT) | s2_spec.yaml: `reported_items`, 12 entries. checks_s2.py: `reported()` returns `items` through `_reported_items` | RPT on S2 r7; RPT controls unchanged |
| TP1.3-1 | sketch_common.py `_annulus_samples`: m = max(5, ceil(width / 2.5) + 1) fractions from 0.02 to 0.98 (COVER_RINGS when m = 5) | K8-Z13, K8-B52 |
| TP1.3-2 | sketch_common.py `cover_issues` clause (5) | K8-B51; K8-B6, B32, B39, B49 counts |
| TP1.3-6 (NOTE) | none. Since P1R, a label that ends the rounds with any issue is recorded as UNPLACEABLE with its final issues, so an unresolved layout cannot pass unrecorded | none |

**Changes to existing controls:**
- K8-B6: 2 → 3; K8-B32: 3 → 5; K8-B39: 3 → 7; K8-B49: 3 → 7. Each adds the cover (5) line to its reasons.
- K4-B7: 3 → 2; K4-B10: 2 → 1; K4-B12: 2 → 1. The drill_head unplaceable reason is removed.
- K4-B8: re-planted, 2.
- K4-B11: 2 (adds the (e1) reason).

## 3 Red-first (new B on the P1R check)

Each planted figure was built with the P1Rf code and judged by the P1R `sketch_common` K check (MEASURED, `scratchpad/p1rf/redfirst2.py`).

| ID | Planted | Reason substrings | P1R check | P1Rf result |
|---|---|---|---|---|
| K8-B51 | live S2, sector alpha 0.95 set in the style before `render_plan` | "cover: opaque fill of operator_sector drawn above it lies behind it or is no part" (planted 3) | pass, 208 predicates (the zone erases the plate, unreported) | fires 3, match |
| K8-B52 | filled ring r 100 to 210 under a 10 x 10 cover at r 140, unsplit | "fixture/ring cover: Annulus partly covered drawn solid", "under d by more than 0.05" | pass, 5 predicates | fires 1, match |
| K8-Z13 | same, rendered | (Z) | pass | clean |
| K4-B14 | ring label at the P1R r6 anchor (209.75, -10.33) | "(e1)" line, "ring and keepout cross", "ring and drill_head cross" (planted 3) | fails 4: two drill_head outline lines and the two crossings; no (e1) | fires 3, match |
| K4-B15 | drill_head suffix removed | "label of a wholly hidden row lacks 'under <cover>' (g)" | fails 2: drill_head gear and ring outline lines; no (g) | fires 1, match |
| K4-B16 | gear outline as an open C (-170 to 170 deg, 34 convex pieces) | "drill_head: label leader ends inside the outline of gear", "(g)" (planted 2) | fails 2: gear and ring outline lines; no (g) (Correction 2) | fires 2, match |

## 4 Check results

| Run | Result | Wall (MEASURED) |
|---|---|---|
| s2_plan.py --rev 7 | wip/s2_plan_r7.png | 12 s |
| check_sketch.py s2 --rev 7 | **19/19 pass**: K1 to K9, S2-1 to S2-6, X1, RPT (12 items); K4 14 labels, K5 121 artists, K8 206 predicates | 28 s |
| s1_side_poses.py --rev 7 | four PNGs pixel-equal to the accepted r7 | n/a |
| check_sketch.py s1 --rev 7 | 18/19: K5 red (pre-existing zero-area lint, until S1 r8); all others pass, RPT exempt | 18 s |
| check_sketch.py --controls (12 jobs) | **282 controls (Z 75, B 205, smoke 2): Z 75/75, B 205/205, smoke 2/2, all match** | 113.5 s |
| --stale | 2 records, 0 differences; X1 pass | n/a |
| --stale --include-unaccepted | 12 records, 0 differences | n/a |

**PNG.** `docs/sketches/wip/s2_plan_r7.png`: 1505 x 2634 px, SHA-256 710f124f35eb3fc28904460ad0b862ec4546601bf999340fcf8236396f04edd9. It is pixel-equal to the DR-1 copy's r7.

**Changes against r6:**
- The ties are drawn as brown phantom lines.
- The labels "cutter OD ASSUMED 177.8 (dotted, under ring gear)" and "descent stop (one pad) r 200 (dashed, under top-guide bracket arm)" are longer.
- The ring leader moves to visible rim at (205.96, -40.97).
- The drill_tube leader moves to an ink anchor at (76.15, 1.87).
- The right column is restacked.

**SHA-256 of committed files** under docs/sketches/ (wip/ and __pycache__ excluded), before landing and after the last run. Six files differ, all edited on purpose:

| File | Before | After |
|---|---|---|
| sketch_common.py | 4685bce046a8… | 0f54ead9b409… |
| s2_plan.py | afda3bfc5dde… | 8336c95e8d40… |
| checks_s2.py | e18708622e1f… | c0c8bd2f7711… |
| s2_spec.yaml | 7b3ab8e1f934… | eb1bdf1805da… |
| fixtures/builders.py | 0759d0025834… | 64e6b11e316b… |
| fixtures/manifest.yaml | 6b56920764bc… | 4563df4b75d8… |

**Accept state.** Every check on S2 r7 passes. The accept still needs the Designer and Topologist re-checks and the fresh M1 on the r7 pixels (P8, KC11).

## 5 Rules awaiting signature

**The Designer** (re-check, `step1.3_designer_renderer_recheck.md`):
1. D1 as implemented: enclosure exemption, (e1) with the stand-in premise (Correction 1), and (g) on the spec `name`.
2. D2 texts as drawn.
3. D3 phantom line and legend.
4. The reported_items values (DR-3).

**The Topologist** (re-check, `step1.3_topologist_renderer_recheck.md`):
1. TP1.3-1 radial step: COVER_RINGS kept when m = 5.
2. TP1.3-2 cover (5): one line per artist; a fill of a row without z_max fails.
3. D1 against the ring and tie a case: the ring now anchors on visible rim at (205.96, -40.97), and no counted outline is entered (DR-1 table). K4-B14 plants the r6 anchor and fires (e1).

## 6 Gameplan lines to change

**l.138 (K4 row), rule cell.** Supersedes the P1R and P1Rd new text for the same cell.

Old:
```
a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1) |
```
New:
```
a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking); (e) only true outlines of rows higher than the labelled row by more than 0.05 (zones: every outline) count; (e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor (outer boundary, holes filled); (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that neither contains nor encloses the anchor (Design Notes 30; Designer P1Rd FIX D1); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back; (g) the drawn label of a wholly hidden row contains "under " and the name of a counted row whose outline contains or encloses the anchor (1.3 P1Rf) |
```

**l.138 (K4 row), B cell.** Supersedes the P1R new text for the same cell.

Old:
```
K4-B11 an area of another row over an anchor |
```
New:
```
K4-B11 an area of another row over an anchor (with (e1) on the hidden ink); K4-B12 the descent-stop leader at the r4/r5 anchor (inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B14 ring label at the r6 anchor on hidden rim inside tie a (e1); K4-B15 drill_head label without its "under ring gear" suffix (g); K4-B16 gear outline planted as an open C, not enclosing the cutter anchor (e2, g); K4-B8 re-planted at 1.3 P1Rf (texts below the anchors in reverse radial order) |
```

**l.142 (K8 row), rule cell.** Apply after the P1R change. Old is the P1R new text ending:
```
alpha-rule premise: no plan fill alpha in (0.5, 0.75) |
```
New:
```
alpha-rule premise: no plan fill alpha in (0.5, 0.75); 1.3 P1Rf: annulus samples also step at most 2.5 mm across the width (Topologist TP1.3-1); cover (5) an opaque fill of another row drawn above an artist over a drawn sample belongs to a row whose z_max is not lower than the artist's by more than 0.05, and a fill of a row without z_max hides nothing (TP1.3-2); render state per piece decided on samples at most 2.5 mm apart, the declared cover resolution (TP1.3-4); plan stand-ins drawn as a brown phantom line (Designer P1Rd FIX D3) |
```

**l.142 (K8 row), B cell.** Apply after the P1R change. Old is the P1R new text ending:
```
B22 re-rendered |
```
New:
```
B22 re-rendered; K8-B51 operator sector at alpha 0.95 set before the renderer (cover (5), TP1.3-2); K8-Z13 and K8-B52 filled annulus under a 10 x 10 cover between the r6 sample radii, rendered and unsplit (TP1.3-1); K8-B6, B32, B39, B49 planted counts 3, 5, 7, 7 under cover (5) |
```

**l.146 (K table pointer).** Apply after the P1R change. Old is the P1R new sentence:
```
Step 1.3 P1R (`research/sean/cr_scratch/step1.3_engineer_renderer.md`) added K8-Z9 to Z12, K8-B44 to B50, K4-B12, K4-B13 and re-planted K4-B8 (276 controls: Z 74, B 200, smoke 2; 107.3 s at --jobs 12; K4-Z3 red on the drill_head UNPLACEABLE until the Designer's remedy).
```
New:
```
Step 1.3 P1R (`research/sean/cr_scratch/step1.3_engineer_renderer.md`) added K8-Z9 to Z12, K8-B44 to B50, K4-B12, K4-B13 and re-planted K4-B8; P1Rf (`research/sean/cr_scratch/step1.3_engineer_renderer_fixes.md`) added K8-Z13, K8-B51, K8-B52, K4-B14 to B16, re-planted K4-B8 and re-counted K8-B6, B32, B39, B49, K4-B7, B10, B11, B12 (282 controls: Z 75, B 205, smoke 2, all match; 113.5 s at --jobs 12).
```

**l.264 (detail 1.2, Reported).** As the Designer wrote it (P1Rd).

Old:
```
highest point over parts only (reference lines excluded, LF1.2-5).
```
New:
```
highest point over parts only (reference lines excluded, LF1.2-5). From S2 r7 (1.3 P1Rf) these are the spec field reported_items in s2_spec.yaml (12 ids, with members to plate edge, tip force, cutter overhang and F6 eye limits; Designer P1Rd section 5), read by RPT from checks_s2.reported items.
```

**l.296 (detail 1.3 carried item 4).** Apply after the P1R change. Old is the P1R new text ending:
```
signatures P1Rt, P1Rd; section-view convention at P4;
```
New:
```
signatures P1Rt, P1Rd; P1Rf (`research/sean/cr_scratch/step1.3_engineer_renderer_fixes.md`): Designer FIX D1 to D3 and Topologist FIX TP1.3-1, TP1.3-2 closed after dry-runs DR-1 to DR-3, reported_items added; S2 r7 19/19 (K4 with no UNPLACEABLE, RPT 12 items), S1 r7 PNGs pixel-equal; re-checks by the Designer and the Topologist, then the fresh M1 (P8); section-view convention at P4;
```

**l.666 (Design Notes 25, TP1.2-13 row).** As the Topologist wrote it (P1Rt); no further change from P1Rf.

**l.667 (Design Notes 25, TP1.2-18/19 and N2 renderer row).** Apply after the P1R change. Old is the P1R new text ending:
```
awaiting P1Rt and P1Rd signatures | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer co-owns the renderer |
```
New:
```
P1Rt: arc step and alpha rule signed; P1Rd: N2 closed on S2 r6, hidden convention and hidden-copy draw order signed; P1Rf: radial step (TP1.3-1), opaque-fill depth premise cover (5) (TP1.3-2), rule (e) by visible ink and enclosure with clause (g) (D1, closes TP1.3-3 by orchestrator ruling), label suffixes naming the cover (D2), stand-ins as a brown phantom line (D3) landed in S2 r7; awaiting the P1Rf re-checks | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer co-owns the renderer |
```

**Design Notes 25, new row.** As the Topologist wrote it (P1Rt, TP1.3-4 to TP1.3-7). Add to its text: "TP1.3-6: an unresolved layout is recorded as UNPLACEABLE with its final issues (P1R code; no change at P1Rf)".

**l.690 (Design Notes 30), end of entry.**

Old:
```
The 60.1 mm of leader inside tie b goes to Sean at M2 as a visual item and to the S3 hidden-line renderer item (N2).
```
New:
```
The 60.1 mm of leader inside tie b goes to Sean at M2 as a visual item and to the S3 hidden-line renderer item (N2). 1.3 P1R: placer rule (e) keeps the leader out of tie b (K4-B12); P1Rf (Designer FIX D1 and D2): the pad is wholly hidden, so its leader ends inside the containing top-guide bracket arm and its label says so ("under top-guide bracket arm"), S2 r7.
```
