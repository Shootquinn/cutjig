# Step 1.1 (e) Topologist cross-review, S1 r1

## Corrections to the brief

1. `s1_checks_r1.json` and `s1_summary_r1.md` sit in `research/sean/cr_scratch/sketches/`, not `cr_scratch/`.
2. The JSON carries K8 as one aggregate ("230 predicate(s) hold", measured 0). It holds no per-predicate value. The code values below are computed with `sc.pieces`, which runs through `_to_data` (the full artist transform chain) as K8 does. They are MEASURED in-process on the r1 figures from `s1_side_poses.build` on 2026-11-25. No harness file was written. The probes are in the scratchpad (`tp11_probe.py`, `tp11_probe2.py`, `tp11_probe3.py`).
3. Designer 1.1 (a) section 6 quotes the gear "drawn chord 0.26". The r1 gear chord is 16.885 / 36.32 = 0.465 (MEASURED). See TP1.1-6.

Tags: hand values DERIVED from params and overlay (values as read in `keys_read`); code values MEASURED. z in z_S = z_A + 60.

## 1. Transform chain, one predicate by hand

`drill_head` outline at capture_end is a Rectangle. Its patch transform minus transData (MEASURED) is

```
[[177.8   0     -88.9 ]
 [  0   106.369 244.84]]
```

It maps the unit square to (-88.9, 244.84), (88.9, 244.84), (88.9, 351.209), (-88.9, 351.209). Hand: x = +/- drill.head_od / 2 = +/- 88.9. z0 = tip_S = stop.height_z 184.84 + 60 = 244.84. z1 = z0 + drill.head_length 106.369 = 351.209. The Polygons (collet, gear, pinions) and Line2D artists carry an identity transform relative to transData. No artist in r1 uses `transform=`.

`drill_head below drill_top_block`, centroid z through the chain, at load (tip_S 1019.84):
- The head row has three pieces: outline 177.8 x 106.369 (centroid tip + 53.1845), teeth strip 177.8 x 12.7 (tip + 6.35) and throat 146.05 x 106.369 (tip + 53.1845).
- Area-weighted: (18912.4 x 53.1845 + 2258.06 x 6.35 + 15535.2 x 53.1845) / 36705.7 = 50.303. c_z = 1070.143 (hand), 1070.143 (code).
- Top block: 1819.84 + 150 / 2 = 1894.84 (hand), 1894.840 (code).
- Sign: 1070.143 - 1894.84 = -824.70 < 0. Holds.

## 2. K8 predicates as sign checks, hand beside code

The JSON value for every row below is "pass" inside the K8 aggregate.

| Predicate (row) | Sign form and invariant | Pose | Hand | Code |
|---|---|---|---|---|
| Tip below top (drill_head below drill_top_block; gameplan l.141 seed "tip z below top z") | c_z(head) - c_z(top_block) < 0. Interval form: z_lo(head) - z_hi(top_block) < 0 | load, park | 1070.143 vs 1894.84; tip 1019.84 vs top 1019.84 + 800 + 150 = 1969.84 | 1070.143 vs 1894.840; 1019.84 vs 1969.84 |
| | | start | 945.143 vs 1769.84; 894.84 vs 1844.84 | 945.143 vs 1769.840 |
| | | capture_end | 295.143 vs 1119.84; 244.84 vs 1194.84 | 295.143 vs 1119.840 |
| Head below gear | c_z(head) - c_z(gear) < 0 | load | gear trapezoid: rectangle 36.32 x 16.885 at 1267.398 plus triangle 306.63 at 1253.327, giving 1262.707; head 1070.143 | 1262.707; 1070.143 |
| Anchor < nut < guide, screw a and b (anchor below nut, nut below guide, nut_housing below guide) | c_z(anchor) < c_z(nut) < c_z(guide). Interval invariant z_hi(anchor) < z_lo(nut), z_hi(nut) < z_lo(guide) | load, park | anchor 265 + 60 + 15 = 340; nut = tip + ring.position_above_tip + ring.thickness / 2 = 1019.84 + 136 = 1155.84; guide 1165 + 60 - 15 = 1210. Interval: nut top 1170.84 to guide bottom 1195 = 24.16 | 340.000 < 1155.840 < 1210.000 (a and b) |
| | | start | 340 < 894.84 + 136 = 1030.84 < 1210 | 340.000 < 1030.840 < 1210.000 |
| | | capture_end | 340 < 244.84 + 136 = 380.84 < 1210. Interval: anchor top 355 to nut bottom 365.84 = 10.84 | 340.000 < 380.840 < 1210.000 |
| Lift motor below anchor | c_z(liftmotor) - c_z(anchor) < 0 | all | 265 - coupling - 48 / 2 + 60 = 276 vs 340 | 276.000 vs 340.000 |
| Core bottom on collet.core_stop_z (core_750 rests_on core_seat, poses start and capture_end) | abs(z_lo(core) - z_hi(seat)) <= 0.05; seat top = receiver_floor + core_seat_height = 40 + 2.5 = 42.5 z_A = collet.core_stop_z (LF-16 lint) | start, capture_end | 42.5 + 60 = 102.5 vs 102.5: 0.000 | 102.5 vs 102.5: 0.0000 |
| | (not asserted at load) | load | 42.5 + 0.5 (159.84 - 42.5) = 101.17 z_A, 161.17 z_S | 161.17 (K6) |
| Collet taper narrows up | per piece: w(z_hi) < w(z_lo) - 0.05 | all | w_lo = 67.29 - 50 = 17.29; w_hi = 17.29 - 32 tan 10 = 17.29 - 5.6425 = 11.6475 | 17.290, 11.648 |
| Gear taper narrows down | per piece: w(z_lo) < w(z_hi) - 0.05 | load | z_lo vertex (90, 1242.07) alone: w 0; w_hi = 126.32 - 90 = 36.32 | 0, 36.32 |
| Pinion taper narrows inward | per piece: h(inner x) < h(outer x) - 0.05 | all | h_out = pinion.outer_diameter 91.24; h_in = 91.24 x 96.54 / 125 = 70.466 | 91.24, 70.466 |
| Gear mirror about the drill axis, tied to x = 0 | for every gear vertex p, a vertex q with abs(2 x0 - p_x - q_x) <= 0.05 at equal z; x0 = c_x(drill_tube). x0 is tied to x = 0 by TP-3 on drill_tube (place r 0: drawn x centre - 0 <= 0.05) | all | right piece (90, z0), (126.32, z0 + 16.885), (126.32, z1), (90, z1), left piece x negated; x0 = 0; 2 x 0 - 90 - (-90) = 0 | x0 0.000000; 0 unmatched of 8; tube x centre 0.000 |
| Motor side (motor23_a sign -1, motor23_b sign +1) | (c_x(motor) - c_x(tube)) x sign > 0 | all | r_c = (142 + 218) / 2 = 180; 180 cos 210 = -155.885; product +155.885 | -155.885, +155.885 |
| Motor outboard of pinion | (c_x(motor) - c_x(pinion)) cos theta > 0 | all | pinion trapezoid, parallel sides at x -59.655 (h 70.466) and -144.054 (h 91.24): centroid -59.655 - 84.399 (70.466 + 182.48) / (3 x 161.706) = -103.661; (-155.885 + 103.661)(-0.8660) = 45.227 | -103.661; 45.227 |
| Motor below the gear back face (top_within gear) | z_hi(gear) - z_hi(motor) > 0 | all | (axis + 62) - (axis + 28.5) = 33.5 | 1275.84 - 1242.34 = 33.50 (load) |
| ring_on_tube (a): bearing clears_above drill_head | z_lo(bearing) - z_hi(head) > 0 | every pose | 130 + 12 - 25 - 106.369 = 10.631 | 10.631 in all four |
| ring_on_tube (b): gear top_within drill_tube | z_hi(tube) - z_hi(gear) > 0 | every pose | 800 - (142 + 52 + 62) = 544.00 | 544.000 in all four |
| Wing nut below drill head | c_z(wingnut) - c_z(head) < 0 | capture_end (closest) | 184.27 vs 295.14 | 184.266 vs 295.143 |

Every predicate holds in every pose with the drawn sense. Hand equals code at three decimals throughout.

## 3. TP-9, the reworded rubric line

"The ring assembly is on the drill tube between the head and the top-end block in every pose" is true in all four poses: 10.631 above the head and 544.00 below the tube top (hand and code). The bearing is the lowest ring-assembly element (tip + 117 against nut housing tip + 121, ring tip + 130, pinion tip + 148.38). The gear back face is the highest (tip + 256 against pinion tip + 239.62, motor tip + 222.5). The two edges therefore bound the whole assembly. It is a K8 predicate pair (`clears_above`, `top_within`). The x half of "on the tube" has no K8 predicate. It is carried by the K7 C pairs drill_tube|bearing, drill_tube|gear_hub and ring|bearing and by the gear mirror. Probe: ring, bearing, hub and gear shifted +30 in x fires K7 (overlap 1190.0 mm2 on drill_tube|bearing) and K8 (gear 8 unmatched vertices). The ring plate alone shifted +30 fires K7 ring|bearing. TP-9 is closed.

## 4. Rubric additions

| Addition | Encoded | Evidence |
|---|---|---|
| Ring assembly on the tube between head and top block | K8 `clears_above` and `top_within` | Section 3 |
| Motors on the same side of the gear, outboard of the pinions, below the back face | K8 `side`, `outboard`, `top_within gear` (`above ring` is vacuous, TP1.1-5) | Section 2 |
| 0.75 m core solid at load, start and capture_end, absent at park, no 0.5 m core | Spec says "K9 by row poses"; K9 does not enforce absence | TP1.1-2 |
| Head at the bottom, top block at the top | K8 `below` ×2 | Section 2 |

## 5. K5 and K9

- K5: 71 + 71 + 71 + 70 = 283 artists, all tagged, 0 untagged (MEASURED), one Axes per figure. Classification per row: the Rectangle pieces classify rectangle (cylinder axis Z or X, normal Y → rectangle; prism, plate and screw rows match `projection: rectangle`). The collet, gear and pinion Polygons are four-vertex and not axis-aligned, so they classify trapezoid, matching cone and gear → trapezoid. Floor, height_target, bore_ceiling and keepout are Line2D, matching `projection: line`. 17 or 18 untagged Text notes per figure, which K5 does not read (correct).
- K9: 45 gids at load, start and capture_end, and 44 at park, where core_750 is absent. Every applicable row is drawn and no gid lacks a row. K9 does not test the converse, a row drawn at a pose it does not apply to (TP1.1-2).

## 6. Findings

**TP1.1-1 FIX. The gear taper predicate accepts a tooth face falling outward, so the cone apex can sit above the gear.**
- Where: `taper_issue` (sketch_common.py 1046-1065) measures width at the lowest and highest vertex levels. Each gear piece has one vertex at z_lo, so w(z_lo) = 0 whichever end is low.
- Probe: gear pieces redrawn as (90, z0 + 16.885), (126.32, z0), (126.32, z1), (90, z1). The heel is low and the face falls outward. K5 to K9 and S1-1 to S1-7 all pass.
- The Designer's TP-2 ruling (1.1 (a) section 6) names sign check (b), "the tooth-face edge rises with r (dz/dr > 0)". No predicate encodes it.
- Fix: a predicate `face_rises: outward` (or `apex: below`) on the gear. Per piece, take the lower edge, from the z_lo vertex to the other vertex below the back face, and require (z_b - z_a)(|x_b| - |x_a|) > 0. Add a K8 B fixture with the falling face.
- The r1 drawing is correct: +16.885 over +36.32 per side.

**TP1.1-2 FIX. "Absent at park" is claimed for K9 and is not checked.**
- Where: s1_spec.yaml l.103 reads "(K9 by row poses ...)". K9 (1166-1189) fails a row missing at a pose where it applies and a gid with no row. It never fails a row's artist at a pose outside `row.poses`.
- Probes: core_750 drawn seated (102.5 to 852.5) at park, and a 500 mm core tagged core_750 at park. Both pass K5 to K9 and S1-1 to S1-7.
- The r1 park figure is correct: 44 gids, no core_750.
- Fix: K9 adds the half-space of the pose set. For every row with `poses` and every pose not in it, the count of artists with that gid is 0. Add a K9 B fixture with the core at park. Alternatively, mark the line visual-only in the spec and at gameplan l.237.

**TP1.1-3 FIX. Holder and collet interpenetrate, and class N hides it.**
- Holder pieces run r 50 to 67.29 from 109.09 to 189.09 z_S. Collet pieces run r 50 to the cone face (67.29 at 100, 61.6475 at 132).
- Overlap per side: 22.91 x 17.29 - tan 10 x (32² - 9.09²) / 2 = 396.11 - 82.99 = 313.12 mm2 (hand), 313.12 (code). The total is 626.24 in every pose (MEASURED).
- Both parts are coaxial solids of revolution drawn in half-section. Two such solids intersect in 3D exactly when their half-sections overlap. This overlap is therefore a solid interference, not a nest.
- The spec declares collet|holder N, "holder clamps the collet cone". A clamp is contact on the cone face, which is class C. Class N passes unconditionally (sketch_common.py 501).
- Of the N pairs between section-drawn coaxial rows (receiver, collet, core_seat, holder, collar), only collet|holder overlaps. The others read 0.00 (MEASURED).
- Fix, drawing: over the collet length the holder's lower bore follows the collet outer cone, r = 67.29 - (z - z_floor) tan 10, in convex pieces. The Designer confirms the holder's internal cone and its height. The Engineer's open item 1 (flange 0.59 above the rim against stroke gap 13.126) is the same holder z stack and goes with it.
- Fix, spec: collet|holder becomes C. Add `section` to the receiver, collet, holder, collar and core_seat rows, and lint refuses class N between two `section` rows.
- Silhouette-drawn rows (drill tube, drill head, wing nut, core) keep N where they nest, because their outlines are not sections.

**TP1.1-4 NOTE.** `taper` reads widths only, not which face tapers. Probe: the collet redrawn with the bore tapered and the outer face vertical passes everything. A collet bore that narrows upward would not pass the core. If the Designer wants it encoded, require the bore-side edge to be vertical: x(z_lo) = x(z_hi) on the inner edge within 0.05. The r1 collet is correct, with a vertical bore at r 50.

**TP1.1-5 NOTE.** Carried from TP-10.
- `below` and `above` order centroids. The interval invariants hold with margin: anchor top to nut bottom 10.84 at capture_end, and nut top to guide bottom 24.16 at load and park. S1-4 asserts the interval band (least margin 0.84 over g_min 10).
- `ring above core_seat` (1155.84 vs 101.25) and `motor23 above ring` hold by construction from the z_rules. They are harmless but test nothing that K6 does not.

**TP1.1-6 NOTE, to the Designer at M1.**
- The gear tooth-face chord rises 16.885 over 36.32, a slope of 0.465 (MEASURED). The pitch cone is 1 in 3: tan(90 - 71.565) = 0.333.
- The rise comes from the `draw_gear_section` default (z1 - z0) / 2. That is a literal in sketch_common, outside the K1 scan of the script.
- The sense is correct; the magnitude is drafting. The Designer's quoted 0.26 does not describe r1.

**TP1.1-7 NOTE.**
- Parts at jackscrew.angle[2] 270 project to x = 0: the third screw, nut, anchor, guide, lift motor and frame member. They lie on the viewer side, since side_xz is seen from -Y.
- Parts at pinion.angle[0] 90 also project to x = 0: the third pinion, NEMA 23 and mount, behind the drill.
- None is drawn. Gameplan l.211 states "two of the three jack screws". No figure says so, and the motors are counted three in the mass report.
- Suggest one untagged note per figure: "third screw set at 270 and third motor at 90 project onto x = 0, not drawn". An M1 reader then does not read a two-screw, two-motor jig.

**TP1.1-8 NOTE.**
- Each figure mixes half-sections (receiver, collet, holder, collar, core seat, bearing, ring, gear, hub) with silhouettes (drill tube, head, top block, wing nut, core, screws, motors).
- The N pairs receiver|wingnut 1596.88, holder|wingnut 2918.40, wingnut|core_750 10384 to 11200, and core_750|drill_tube 100258 mm2 exist only because silhouettes are drawn over sections (MEASURED).
- The convention is legitimate. Stating it in the spec header would let the TP1.1-3 lint apply to section rows only.

**TP1.1-9 NOTE.**
- The anchor thrust-bearing line is a zero-height Rectangle tagged to the anchor row. It is a degenerate 2-cell that passes K5 as "rectangle" and adds 0 area.
- Here it is inside the row's extent and harmless. The same device can carry any line past K5's projection rule.
- If the device is to be closed: K5 could fail a Rectangle or Polygon of zero area on a row whose projection is not `line`.

**TP1.1-10 NOTE.**
- The pinion trapezoid spans the plan-footprint envelope in x: r_in cos theta + w |sin theta| = -82.46 + 22.81 = -59.655, to -144.054. The toe end is drawn at the heel half-width.
- The true toe silhouette edge is about -82.46 + 35.23 x 0.5 = -64.85, toe radius 45.62 x 96.54 / 125 = 35.23 (DERIVED).
- The drawn toe height ratio 70.466 / 91.24 = 0.7723 = r_toe / r_heel is correct. The envelope is K7-conservative.

## 7. Gameplan lines that need a change (for the orchestrator)

- l.141 (K8 seed set): add "gear tooth face rises outward (cone apex below the gear)" with the B fixture from TP1.1-1.
- l.142 (K9): add "no artist of a row at a pose outside its `poses`" with the B fixture from TP1.1-2.
- l.237 (rubric additions): after TP1.1-2, name the K9 rule for "absent at park", or mark it visual-only.
- l.140 (K7 classes): N is refused between two rows drawn in true section (TP1.1-3).

## Verdict

CROSS-REVIEW FAIL (TP1.1-1, TP1.1-2, TP1.1-3 FIX; 0 BLOCK; 7 NOTE). Every K8 predicate holds in every pose with hand values equal to code values, and TP-9 is closed. The holder|collet interference (TP1.1-3) is a drawing defect in r1. TP1.1-1 and TP1.1-2 are checks that pass a reversed or extra part.

## Re-check r2

Inputs: `step1.1_engineer_revision_r2.md`; `sketch_common.py` k5 (bore_cone admission), k7 (section-N lint), `face_rises_issue`, k8, k9 (pose-set rule); `s1_spec.yaml` r2; the r2 figures from `s1_side_poses.build`. All values MEASURED 2026-11-25, in-process. No harness file was written: `controls_results.json` was not rewritten. Probe: scratchpad `tp11_r2_probe.py`, which runs the r1 probes against r2.

**Controls (manifest, in-process, matched on reason and planted count):** K5 Z 2/2, B 6/6; K7 Z 10/10, B 15/15; K8 Z 4/4, B 14/14; K9 Z 2/2, B 5/5. The new controls carry their reasons:
- K8-B14: "dz +15.00 over d|x| -35.00".
- K9-B5: "park: core_750 drawn at a pose outside its poses".
- K7-B14: "collet|holder class N between two section rows".
- K7-B15: "overlap 626.239 mm2" x 4 poses, against r1 hand 626.24.
- K5-B6: "bore_cone trapezoid z [137.00, 142.00] outside mate collet z [100.00, 132.00]".

**Probes on r2.** Each r1 probe re-run against r2 gives:

| Probe | r1 | r2 |
|---|---|---|
| Gear tooth face falling outward | all pass | K8 fires: face_rises, dz +16.88 over d|x| -36.32, all poses |
| core_750 seated at park | all pass | K9 fires: drawn outside its poses |
| 500 mm core tagged core_750 at park | all pass | K9 fires |
| Collet bore tapered, outer face vertical | all pass | K7 fires: collet|holder C overlap 165.989 mm2 (the holder cone piece guards the outer face) |
| Ring and assembly shifted +30, pinions toe outward | K7 / K8 fire | unchanged |
| Live r2 | n/a | K5 to K9 and S1-1 to S1-7 all pass |

**face_rises sign check by hand, live gear (load):** the lowest vertex is a = (90, 1242.07). Its adjacent vertex with the larger radial change is b = (126.32, 1258.955). (16.885)(36.32) = +613.3 > 0, so it holds (code: no issue, all four poses).

**Holder cone piece, by hand:** r = 67.29 - (z - 100) tan 10.
- At 109.09: 67.29 - 1.6028 = 65.687 (code 65.687).
- At 132.00: 61.648 (code 61.648).

collet|holder is class C, at distance 0.000 and overlap 0.000 in every pose. The holder has 6 pieces: the cone zone, the tube from 132.00 to 197.09, and the flange from 197.09 to 205.09. K9 counts 45 gids at load, start and capture_end and 44 at park.

**TP1.1-7:** every figure carries an untagged note: "not drawn (project onto x = 0): third screw set, theta 270; third pinion and NEMA 23, theta 90; see S2 plan".

| ID | Status | Evidence |
|---|---|---|
| TP1.1-1 | CLOSED | K8 `face_rises: outward` on the gear. K8-Z4 clean, K8-B14 fires; the r1 probe fires in all poses. The sign form (z_b - z_a)(|x_b| - |x_a|) > 0 matches the Designer's TP-2 check (b). |
| TP1.1-2 | CLOSED | K9 pose-set half-space: no artist or Text of a row at a pose outside `poses`. K9-Z2 clean, K9-B5 fires; both r1 park probes fire. |
| TP1.1-3 | CLOSED | Drawing: holder bore on the collet cone, overlap 0.000 and distance 0.000 in four poses. Spec: class C, `section` on receiver, collet, core_seat, holder and collar, and N refused between section rows (K7-B14). The r1 drawing fires at 626.239 (K7-B15). The bore_cone piece is admitted only inside the collet z extent (K5-Z2, K5-B6). The holder's true section (build_parts/holder.py OD 67.04, cone 62.04 to 56.75) is the Designer's at M1, as the revision lists. |
| TP1.1-7 | CLOSED | Note on all four figures. |
| TP1.1-4 | NOTE, now covered | A tapered collet bore with a vertical outer face fires K7 collet|holder (165.989 mm2). A bore that tapers while the outer cone stays is still unencoded; it stays optional for the Designer. |
| TP1.1-5, -6, -8, -9, -10 | NOTE, carried | -6, -9 and -10 are on the Designer's M1 list in the revision. -8 is stated in the spec header. |

No new finding.

CROSS-REVIEW PASS (TP1.1-1, TP1.1-2, TP1.1-3 closed; TP1.1-7 closed; NOTEs carried to M1)

## Re-check r3

Inputs: `step1.1_engineer_revision_r3.md`; `sketch_common.py` `assess_pair` plan-contact branch, `plan_contact_fn`, `plan_footprint`, `_ngon`; `s1_spec.yaml` r3 rows bracket_anchor_a/_b, bracket_guide_a/_b, descent_stop_post, motor_shaft_a/_b, pinion_axis_a/_b; the r3 figures from `s1_side_poses.build`. All values MEASURED 2026-11-25, in-process. No harness file was written. Probe: scratchpad `tp11_r3_probe.py`.

**Controls (manifest, in-process, matched on reason and planted count):** K5 Z 2/2, B 6/6; K7 Z 11/11, B 19/19; K8 Z 4/4, B 14/14; K9 Z 2/2, B 5/5. The new controls:
- K7-Z11: clean, state plan-contact.
- K7-B16: plan distance 0.994.
- K7-B17: plan overlap 8.607.
- K7-B18: post|pad distance 1.000 x 4.
- K7-B19: arm|block plan distance 0.994 x 4.

The live r3 figures pass K5 to K9 and S1-1 to S1-7.

### 1. Plan-contact from the half-space view

**Statement.** Let part A lie inside the prism P_A x [z_A0, z_A1], with P_A its plan footprint, and B likewise.
- The interiors of A and B can meet only if int P_A ∩ int P_B ≠ ∅ and (z_A0, z_A1) ∩ (z_B0, z_B1) ≠ ∅.
- With plan overlap ≤ 0.01 mm2, the first condition is false, so A and B cannot interpenetrate.
- A side-view overlap of area > 0.01 implies the open z intervals meet. With plan distance ≤ 0.05, the closures meet on a vertical face of positive height. That is contact.

**Two premises.**
1. Interference exclusion needs footprint ⊇ part, the LF-8 containment premise.
2. The contact claim is exact only when the footprint equals the part on the touching face.

When premise 1 holds and premise 2 fails, the rule can label a small gap as C. That is the safe direction. When premise 1 fails, an interference passes. The rule is sound exactly where the premises hold, and it is not tied to "prisms". The code accepts any placed row (shafts and motors are horizontal cylinders), which is correct because each such part lies inside footprint x [z_min, z_max]. The docstring should state the premise in that form.

**Hand values, live (capture_end):**

| Pair | Plan distance | Plan overlap (mm2) | Side view | Reading |
|---|---|---|---|---|
| arm\|block | 0.0000 | 0.0014 | | 128-gon artefact; face r 181 on the circumscribed block disk, centre r 160 + 21 |
| arm\|member | 0.0000 | 0.0030 | | r 270 = 300 - 30 |
| shaft\|motor23 | 0.0000 | 0.0000 | | radial rectangles meeting at r 142 |
| post\|arm | | 900 (post inside arm) | z abutting at 355.00 | ordinary C, not plan-contact; correct |

**Can a real interference pass? Yes, by two routes.**
- **TP1.1-11 FIX. Plan-contact certifies the spec footprints, not the drawing.**
  - For a C pair that passes as plan-contact, the drawn side-view overlap is waived whatever its size. Only the x centre of a placed row is tied to the spec (TP-3).
  - Probe: bracket_anchor_a drawn 20 wider at each end, centre kept. The drawing then runs 20 into the block and the member. Result: all of K5 to K9 and S1-x pass.
  - Same probe on motor_shaft_a, 15 wider each end, 15 into the motor: all pass.
  - Before r3, a drawn overlap on any C pair fired K7.
  - Fix: K8 projected_x goes from centre to extent. For every placed row, the drawn x extent equals the projected footprint [min(r_in c, r_out c) - w|s|, max(r_in c, r_out c) + w|s|] (radial) or r_c c ± w (round), within 0.05. Add a B fixture with the widened arm.
  - Hand against drawn:

    | Row | Hand | Drawn |
    |---|---|---|
    | Arm | 181 cos 150 = -156.751, 270 cos 150 = -233.827, ± 30 x 0.5 gives [-248.827, -141.751] | [-248.827, -141.751] |
    | Anchor block | 160 cos 150 ± 21 = [-159.564, -117.564] | equal |
    | Shaft | 121 cos 210, 142 cos 210 ± 4 x 0.5 = [-124.976, -102.789] | equal |
    | Post | 200 cos 150, 215 cos 150 ± 15 = [-201.195, -158.205] | equal |

    The live drawing satisfies the rule today.
- **TP1.1-12 FIX. The frame_upper footprint does not contain the member.**
  - The shape is "vertical 30-6060, 60 wide", but `place` gives a round footprint of radius profile.width / 2 = 30. That is the inscribed circle of the 60 x 60 section, whose circumradius is 42.43.
  - The member's orientation is not declared. With the member turned 45 deg, its corner sits at r 300 - 42.43 = 257.57, which is 12.43 inside the arm end at r 270.
  - Plan overlap with the arm footprint is 154.415 mm2 (MEASURED). The spec footprints still read distance 0.000 and overlap 0.003, so plan-contact passes a real interference.
  - With one face normal radial (rot 0), the face contact at r 270 is exact: overlap 0.000.
  - Fix: a `square` footprint for frame_upper_a/_b with that orientation stated, the face normal radial. Alternatively, the circumscribed r 42.43 (the liftmotor FIX 4b precedent), but then the arm r_out becomes 257.57 and the contact is a corner.
  - No other frame_upper pair changes state at r 42.43. The least G margin is ring|frame_upper, 59.96 → 47.53 against g_min 10 (MEASURED).

### 2. New rows: orientation and mating faces (capture_end; hand = code)

| Row | Drawn x, z_S | Sense and mating face |
|---|---|---|
| bracket_anchor_a | x [-248.827, -141.751], z 325 to 355 | Outboard of anchor_a: (-195.289 + 138.564)(cos 150) = +49.125. Below nut_a: 340 < 380.84. Inner end on the block at r 181, outer end on the member face at r 270. Top flush with the block top 355 |
| bracket_guide_a | z 1195 to 1225 | Above nut_a: 1210 > 1155.84 at load and park. Outboard of guide_a, +49.125 |
| descent_stop_post | x [-201.195, -158.205], z 355.00 to 362.84 | Foot on the arm top (355.00 = arm z_max). Top under the pad (362.84 = pad z_min). Pad top 374.84 = ring bottom at capture_end. Below descent_stop: 358.92 < 368.84 |
| motor_shaft_a | x [-124.976, -102.789], z 434.84 to 442.84 | On the pinion axis 386.84 + 52 = 438.84 ± 4. Outer end on the motor flange r 142. Inner r 121 to 140 nested in the pinion hub (N). Side -1: -113.882. Outboard of pinion_a: (-113.882 + 103.661)(-0.866) = +8.851 |
| pinion_axis_a | x [-188.794, -82.465] at z 438.84 | Line, half-width 0. 95.22 cos 210 to 218 cos 210. Side -1 |

Every new row is on the correct side of its mating face. The arm has no `inboard of the member` predicate. TP-3 and the C pair carry it, and TP1.1-11 makes that binding on the drawing.

### 3. K5, K8 and K9 coverage of the new rows

- K5: 82 + 82 + 82 + 81 = 327 artists, 0 untagged, one Axes per figure. Arms, post and shafts are Rectangles on prism or cylinder-axis-X rows, so they classify rectangle. The pinion axes are Line2D on `projection: line`.
- K8: projected_x on all nine placed rows, plus the sense rows above.
- K9: 54 rows. There are 54 gids at load, start and capture_end, and 53 at park (core_750 absent).

| ID | Status |
|---|---|
| TP1.1-11 | FIX, open |
| TP1.1-12 | FIX, open |
| NOTE (new) | `assess_pair` docstring: state the premise as "part inside footprint x [z_min, z_max]; contact exact where footprint = part". The anchor and guide block footprints are round r 21, borrowed from nut_flange_od, and the block's plan shape is undeclared. Same premise; Step 2 / S3 rule the block. |
| TP1.1-1, -2, -3, -7 | remain closed (controls re-run above) |

CROSS-REVIEW FAIL (TP1.1-11, TP1.1-12 FIX; 0 BLOCK). The plan-contact rule is sound under its premises. As implemented, it passes an interference drawn wider than the spec footprint, and an interference hidden by the inscribed frame_upper footprint.

## Re-check r4

Inputs: `step1.1_engineer_revision_r4.md`; `sketch_common.py` k8 projected_extent (1226-1239) and plan_footprint; `check_stack.radial_corners` and place_extents with `rot`; `s1_spec.yaml` frame_upper_a/_b `place`; the r4 figures from `s1_side_poses.build`. All values MEASURED 2026-11-25, in-process. No harness file was written. Probe: scratchpad `tp11_r4_probe.py`.

**Controls (manifest, in-process, matched on reason and planted count):** K5 Z 2/2, B 6/6; K7 Z 11/11, B 20/20; K8 Z 5/5, B 16/16; K9 Z 2/2, B 5/5.
- K8-Z5 is clean: 330 predicates.
- K8-B15 fires 4x: "(by 20.00)".
- K8-B16 fires 4x: "(by 15.00)".
- K7-B20 fires 8x: "overlap 154.416 mm2".
- K7-Z10 is clean, with states including plan-contact and plan-separated.

**K8-B7, third issue.** The mini fixture mirrors motor23_a to +x. Its footprint is r 125 to 201 at theta 210, half-width 28.5:
- Projected x [201 cos 210 - 28.5 x 0.5, 125 cos 210 + 14.25] = [-188.32, -94.00].
- Drawn x [94.00, 188.32].
- Excess: ex_hi - fx_hi = 188.32 + 94.00 = 282.32 (hand = code).

The mirrored part lies wholly outside its footprint. projected_extent is an independent half-space test (drawn interval ⊆ footprint interval), so a third detection of the one planted defect is legitimate. Planted 3 is correct.

**TP1.1-11 probes on r4:**
- Arm +20 at each end: K8 fires 4x, by 20.00.
- Shaft +15 at each end: K8 fires 4x, by 15.00.
- Arm 10 short at the member end: K8 projected_x fires (-190.29 vs -195.29).

Across all four poses, 148 placed-row instances were checked. Max excess is 0.00 and none is drawn narrower than its footprint (MEASURED). The invariant is now complete: the drawn extent is contained in the spec footprint projection, and K7 plan tests run on that footprint. A drawn interference therefore cannot hide behind plan-contact.

**TP1.1-12 hand values, frame_upper_a (theta 150).** The footprint is radial, r 270 to 330, half-width 30, one face toward the axis.

| Quantity | Hand | Code |
|---|---|---|
| Corner radii | sqrt(270² + 30²) = 271.66; sqrt(330² + 30²) = 331.36 | 271.66, 331.36 |
| Drawn x | 330 cos 150 - 15 = -300.79; 270 cos 150 + 15 = -218.83 | [-300.788, -218.827] = place x |
| Depth band | 150 ± 25.98 = [109.02, 190.98] | [109.02, 190.98] |
| Arm\|member plan | | distance 0.0000, overlap 0.0000 |

The arm end at r 270 lies on the member inner face, so the face contact is exact; the r3 128-gon artefact is gone. With `place.rot 45` set on the live spec, K7 fires 8x at 154.416 mm2. Hand: (270 - 257.57)² = 12.43² = 154.5; the corner is 300 - 30 sqrt 2 = 257.57. `radial_corners` rotates in the (radial, tangential) frame about the footprint centre and then maps by theta. It is correct.

| ID | Status |
|---|---|
| TP1.1-11 | CLOSED. K8 projected_extent; K8-Z5, B15, B16; r3 probes fire. |
| TP1.1-12 | CLOSED. Square member footprint, face toward the axis; `place.rot`; K7-B20; r3 corner probe fires as a spec mutation. |
| NOTE (new) | projected_extent is containment, not equality. A part drawn narrower than its footprint passes; probe: member drawn 60 wide as in r3, all pass. That error is in the safe direction for interference, so only the M1 read sees it. The live r4 drawing is exact on every placed row. |
| NOTE (r4 correction 3) | ring\|frame_upper passes on the plan gap 59.94 (hand 270 - 210 = 60). The side view reads 8.83 against g_min 10, because the oblique member's projection is wider than its plan distance. Correct under containment. |
| TP1.1-1, -2, -3, -7 | remain closed |

CROSS-REVIEW PASS (TP1.1-11, TP1.1-12 closed; plan-contact rule signed by the Topologist on its containment premise, now enforced by K8 projected_extent and the true member section)
