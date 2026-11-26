# Step 1.2 (h) Engineer: S2 r5, D4-1 (S1 stays r7)

## Corrections to the brief

1. **D4-1 does not hold under K4 (d) at theta 150.** `label_theta: 150` gives the anchor (-186.20, 107.50) (MEASURED, `label_anchor`; equals the Designer's DERIVED point). The end-quarter hatch rule then rejects that leader. The r3 re-anchor in `place_labels` moves the anchor back to the r4 point (-201.20, 81.52). The r5 drawing is pixel-equal to r4 (MEASURED, numpy array equality).
2. **Member a's hatch on y 107.5 sits 8.4 mm further outboard than the Designer's figure.** MEASURED: x -246.17 to -219.71 (from `hatch_areas`, 4000 samples). Designer, DERIVED: -254.6 to -228.0. The width matches (26.5 against 26.6). The offset does not.
3. **The left-column leader is 180.6 long (MEASURED). The Designer's figure was about 170.** The label column sits at x -366.84, so the end quarter starts at x -231.68 (DERIVED, -186.20 - 180.65 / 4).
4. **K4 (d) fires on the theta-150 leader.** The hatch covers x -231.68 to -219.71 of the end quarter: 12.0 of 45.2 mm, 26.5 percent (DERIVED). On the rule's own samples, 2 of 6 end samples (k 18, 19 at x -231.36 and -223.83) lie in `frame_upper_a` hatch, 33 percent, over LEADER_HATCH_MAX 0.25 (DECLARED, r3) (MEASURED). The K4 check calls the same `leader_hatch` (`sketch_common.py` l.1312). If the theta-150 anchor were forced past the re-anchor, K4 would go red.
5. **No visual-gate stub.** The pipeline writes none for r5, as at r4.

Tags: run results MEASURED 2026-11-25 on `docs/sketches/`, Python 3.12, matplotlib 3.11.2. Hand values DERIVED. Design values DECLARED.

## 1 Fix table

| Finding | Fix | Check |
|---|---|---|
| D4-1 descent-stop leader ends inside the tie b outline | `label_theta: 150` added to `descent_stop` in `s2_spec.yaml`. Applied, but it has no effect: the anchor stays at (-201.20, 81.52) because of Correction 4. **Open: the Designer chooses the next value.** | K4 (d) (`leader_hatch`, end quarter; existing rule). No new predicate |

What the theta-150 leader would cross, (-366.84, 107.50) to (-186.20, 107.50), as MEASURED segment intersections with tagged ink (t from the text end):

| Row | x | t |
|---|---|---|
| base_plate, base_plate:outline | -322.00 | 0.248 |
| base_frame (dashed) | -262.00 | 0.580 |
| frame_upper_a (hatched member a), entry | -246.20 | 0.668 |
| frame_upper_a exit; bracket_anchor_a, bracket_guide_a edge | -219.68 | 0.815 |
| base_frame (dashed) | -202.00 | 0.913 |

The theta-150 leader clears tie b (top y 97.15, MEASURED). The r4/r5 leader at y 81.52 enters the tie b outline at x -264.38 (t 0.619) and leaves it at -204.30 (t 0.981). Its last 60.1 mm before the exit lie inside the tie. The anchor sits 3.1 mm outside the tie's right edge, measured along the leader (MEASURED; tie b corners (-198.45, -28.36), (-205.13, 97.15), (-265.04, 93.96), (-258.36, -31.55)).

Other changes: `s2_spec.yaml` status text (r4 edits marked signed, Designer sign-off r4; r5 edit named). Line endings CRLF as before.

## 2 Check results

**S2 r5** (`check_sketch.py s2 --rev 5`, 32 s): **17/17 pass**. K4 14 labels, K5 105 artists, K7 1292 plan tests, K8 190 predicates, S2-5a least 11.71, S2-5b least 19.84 (drill_head).

**Controls** (`check_sketch.py --controls`): exit 0, **230/230 matched** (Z 64/64, B 164/164, smoke 2/2), 775 s wall (MEASURED; 734 s at r4).

**r4 to r5 checks JSON diff** (recursive key-by-key comparison): `rev` 4 to 5, `spec_status` (r5 clause), `timestamp`. No other value differs. The record does not store label geometry, and the label geometry did not change (Correction 1).

PNG: `docs/sketches/wip/s2_plan_r5.png` (pixel-equal to `wip/s2_plan_r4.png`). Records: `wip/s2_checks_r5.json`, `wip/s2_summary_r5.md`.

S1 r7 is unaffected: no shared code changed.

## 3 Open item for the Designer

D4-1 needs a new value. These are the measured constraints at the left column x -366.84:
- A horizontal leader at the pad needs its end quarter to stay out of member a's hatch for more than 75 percent of its samples. The rule allows at most 1 of 6 samples in hatch.
- It must also stay out of the tie b outline (x -265.04 to -198.45, y -31.55 to 97.15, MEASURED).

The choice of angle or field is a design value and stays with the Designer.

## D4-1 candidate scan

The scan used the r5 code and spec unchanged and built each figure in memory. No PNG was written and no controls were run (MEASURED, 647 s for 74 builds; script `d41_scan.py` in the session scratchpad).

The fields that `place_labels` / `label_anchor` read for this label are `label_theta` and `label_side` (left, or absent for the right column). There is no anchor override field. The scan covers `label_theta` 90 to 270 in steps of 5, each in both columns.

How the inputs behave:
- **Ray hit.** The ray from the drill axis hits the pad only for theta 141.47 to 158.53 (DERIVED: pad r 200 to 215 x 60 at 150, atan(30 / 200) = 8.53 deg). The hit is always the descent-stop pad's own ink, on its outer edge (r 215).
- **Ray miss.** When the ray misses, `label_anchor` uses its default anchor, the pad corner (-165.24, 130.04): side edge t -30, r 208.1.
- **Hatch fraction.** This is the share of the 6 end-quarter samples that lie in another row's hatch. The limit is 0.25 (DECLARED, r3).
- **End inside an outline.** This is the point-in-polygon test on every other tagged closed outline, with the distance from the end point to that outline's boundary. base_plate contains every candidate end, because the plate lies under every part, so the CLEAN test leaves it out.
- **K4.** Every candidate keeps K4 green: `leader_issues` gives 0 issues in all 74 builds.

| Column | Theta | Ray hit (pad edge) | First anchor | place_labels | Final anchor | Hatch, first / final | End inside another outline | Leader crosses (text end to anchor) | K4 | CLEAN |
|---|---|---|---|---|---|---|---|---|---|---|
| left | 90 to 140, 160 to 270 | miss | (-165.24, 130.04), side edge t -30 | falls back (hatch 2/6, frame_upper_a) | (-201.20, 81.52), pad outer corner t +30 | 0.33 / 0.00 | none (tie b right edge 3.1 to the left of the end, along the leader) | base_plate and its outline, base_frame x2, guide_tie_b x2 (last 60.1 mm inside the tie) | green | no (fallback) |
| left | 145 | (-176.79, 123.79), outer edge t -18.8 | same | falls back (hatch 2/6, frame_upper_a) | (-201.20, 81.52) | 0.33 / 0.00 | none (as above) | as above | green | no (fallback) |
| left | 150 | (-186.20, 107.50), outer edge t 0 | same | falls back (hatch 2/6, frame_upper_a) | (-201.20, 81.52) | 0.33 / 0.00 | none (as above) | as above | green | no (fallback) |
| left | 155 | (-195.60, 91.21), outer edge t +18.8 | same | kept | (-195.60, 91.21) | 0.00 / 0.00 | bracket_anchor_a and bracket_guide_a, 11.19 inside | base_plate and its outline, base_frame x2, guide_tie_b x2 (enters at t 0.595, leaves at t 0.946), bracket_anchor_a and bracket_guide_a edge (t 0.869); length 171.2 | green | no (inside the brackets) |
| right | 90 to 140, 160 to 270 | miss | (-165.24, 130.04), side edge t -30 | kept | (-165.24, 130.04) | 0.00 / 0.00 | none; on the bracket_anchor_a and bracket_guide_a edge (0.00) | base_plate and its outline, base_frame x6, frame_upper_b, bracket_anchor_b and bracket_guide_b, ring x2, operator_sector x2, sightline_f6, pinion_c x2, motor_shaft_c, pinion_axis_c; length 532.1 | green | **yes** |
| right | 145 | (-176.79, 123.79), outer edge t -18.8 | same | kept | (-176.79, 123.79) | 0.00 / 0.00 | bracket_anchor_a and bracket_guide_a, 11.19 inside | as the row above plus gear x2, gear:ticks x6, the pad's post; length 543.9 | green | no (inside the brackets) |
| right | 150 | (-186.20, 107.50), outer edge t 0 | same | kept | (-186.20, 107.50) | 0.00 / 0.00 | bracket_anchor_a and bracket_guide_a, 29.00 inside | base_plate, base_frame x6, frame_upper_b, bracket_anchor_b and bracket_guide_b, ring x2, liftmotor_b, operator_sector, gear x2, gear:ticks x11, sightline_f6, pinion_c, pinion_axis_c, liftmotor_a, the pad's post; length 553.0 | green | no (inside the brackets) |
| right | 155 | (-195.60, 91.21), outer edge t +18.8 | same | kept | (-195.60, 91.21) | 0.00 / 0.00 | bracket_anchor_a and bracket_guide_a, 11.19 inside | 30 rows, including guide_tie_a, screw set b, bearing, gear_hub, drill_head, keepout, screw set a; length 562.7 | green | no (inside the brackets) |

Notes (MEASURED):
- The pad lies on the anchor arm of screw a. Every point on the pad's outer edge is inside the bracket_anchor_a and bracket_guide_a outlines, which coincide. Only the two outer corners (t +30, t -30) are clear of them: one is outside, the other on their edge.
- The one CLEAN candidate, right column with no ray hit, is the same anchor and leader as r3. That about-520 leader is the subject of the Designer's M1 S2 r3 N1. There, `label_theta` has no effect because the ray misses the pad.
- No left-column candidate is CLEAN. The left column keeps an anchor only at theta 155, and that end lies 11.19 inside the brackets.

## Gameplan lines to change

none
