# Step 1.4 (e) P7b, The Topologist: orientation and half-space cross-review of S4 r1 and S1 r9

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\open14\p7b\`.
- `ws\` is a copy of docs/sketches and params.yaml. The live tree was not edited.
- `bin\tp_s4.py` recomputes the predicates through the artist transform chain: path, then `get_transform()` to display, then `transData` inverted. It does not use `sc._to_data`.
- Outputs: `tp_s4.json`, `tp_s1.json`, `tp_s3.json`.
- Dry runs:
  - `bin\depth_lint.py`: `depth_lint_pre.txt`, `depth_lint_post.txt`.
  - `bin\occl.py`: `occl.txt`, `occl_post.txt`.
  - `bin\lines_hidden.py`: `lines_hidden.txt`.
  - `bin\seams.py`: `seams.txt`.
  - Harness runs: `run_s1.txt`, `run_s3.txt`, `run_s4.txt`, `run2_s3.txt`, `run2_s4.txt`.
  - Controls: `controls_dry.txt`, `controls_fix1only.txt`, `controls_fix12_k7.txt`.
  - Comparisons: `png_sha.txt`, `k7_diff.txt`, `s1_k7_state_moves.txt`.
  - Sweep plants: `plant_A.txt`, `plant_B.txt`.
  - Head crops: `crop_r1.png` (live), `crop_r2.png` (TP1.4-4 prototype).

## Corrections to the brief

1. **"Core upright on the stop."** S4 does not draw this state. The 100 mm core stands on the carrier, and the carrier stands on the core seat (Design Notes 34; S4-3 rows core_100 rests_on carrier and carrier rests_on core_seat / core_seat_105). Section 1 recomputes that chain.
2. **"Wing nut above the holder."** In S4 this predicate is `clears_above holder`, which reads piece pocket_rim against of_piece flange.
   - pocket_rim is drawn on the -u side only, because plane_cuts at theta 90 removes it on +u (MEASURED).
   - So the predicate reads the -u piece. The nut plate is also checked against the flange below.
3. **Rows drawn wider than their depth band.** One row is drawn wider than its depth band in all three specs: core_seat (FIX TP1.4-3). That is the TP1.1-11 class, not TP-n.

## 1 S4-3 predicates through the transform chain (task 1)

Frame: u right, z up. The display cross product (u image) x (z image) is +66.09 px² per data mm² in both S4 figures and +0.276 in every S1 pose (MEASURED). Neither axis is inverted. Values below are in z_A (MEASURED from the drawn patches unless tagged).

| Predicate (sign form) | Carrier figure | Liner figure | S1 r9 (four poses) | Invariant |
|---|---|---|---|---|
| Collet taper, cone piece: d\|u_out\|/dz < 0 on the outer edge | -0.17633 both sides; tan(cone.alpha) 0.17633 (DERIVED) | -0.17633 both sides | -0.17633 | The width test (taper_issue) and vertical_edge together imply d\|u_out\|/dz < 0, because \|u_in\| is constant |
| Collet bore vertical (S4-d): \|u_in(top)\| - \|u_in(bot)\| | 0.000 over 41.995 to 65.70 | 0.000 over 41.995 to 68.20 | 0.000 | |
| Narrow end up | top piece \|u\| max 59.11 at 65.70, foot 66.99 at 40.00 to 41.995 | 58.67, 66.99 | 59.11, 66.99 | Foot z_max - cone z_min = 0.000 (pieces stacked in order) |
| Collet foot below holder (centroid z difference < 0) | -65.23 | -65.23 | -65.23 | |
| Collet rests on the receiver floor: z_min(collet) - z_max(floor) | 0.000; bearing 16.49 per side | 0.000; 13.99 | 0.000 | min_bearing 0.25 (DECLARED) |
| Holder cone (inner edge) narrows up: \|u\| bottom, top | 62.04, 56.75 at 49.09, 79.09; OD edge du 0.000 | same | same | Holder inner line equals the collet outer line at 49.09 (62.04 vs 62.04, DERIVED): mating sense, contact |
| Wing nut clears the holder flange: z_min(pocket_rim) - z_max(flange) > 0 | +0.50 (-u) | +0.50 | +0.50 (both sides; xz plane, no window) | Nut plate z_min - flange z_max +1.30 |
| Washer between flange and plate: min(z_mid - z_max(flange), z_min(plate) - z_mid) > 0 | 0.65, 0.65 | 0.65, 0.65 | 0.65, 0.65 | P5f min form (TP F4). Order comes from the factors themselves |
| Washer bears on the flange: z_min(washer) - z_max(flange) | 0.000; washer r 68.40 to 71.60 inside flange r 56.75 to 72.04 | same | same | |
| Wing nut below the drill head (centroid) | -108.47 | -108.47 | -885.42 to -110.42 | |
| Receiver floor at the bottom: floor z_min - least receiver piece z_min | 0.000 (floor 12.00 to 40.00, cup 12.00 to 128.50) | same | same | The spigot row 0 to 12 is one body below it |
| Floor below collet: centroid difference; z_max(floor) - z_min(collet) | -27.28; 0.000 | -27.23; 0.000 | -27.28; 0.000 | |
| Core on carrier: z_min(core) - z_max(carrier) | 0.000 (core 202.50 to 302.50, u +-50.50, edges vertical) | 0.000 | n/a | Upright: the core rectangle has vertical sides at u +-50.50 |
| Carrier on core seat: z_min(carrier) - z_max(seat) | 0.000; bearing 3.00 (DERIVED from 47.50 to 50.50) | 0.000; 0.50 | n/a | |

The cone pieces are counter-clockwise on both sides: signed area +253.665 (d 100) and +209.129 (d 105), MEASURED. The -u mirror reverses the vertex order and keeps the orientation.

Every S4-3 predicate holds, with signs as the spec states. **PASS.**

## 2 Section convention on the S4 plane (task 2)

**Look sign.**
- u = +Y and z = +Z, so u x z = +X, which points toward the viewer.
- The look direction is -X, so (u x z) . look = -1 (K8-B66 form).
- The title reads "seen from +X; u = +Y" in both figures.
- Slit azimuths: theta 112 gives sin > 0 and cos < 0, so the slit is at u > 0 and behind the plane. Theta 262 gives sin < 0 and cos < 0, so it is at u < 0 and behind the plane.
- The theta 90 plane cut lies at +u. The -X wing (theta 180) lies behind the plane. The +X wing and the theta 37 key band lie in front (x > 0) and are omitted.

**Cut, hatched by material** (MEASURED, both figures):

| Material | Pattern | Rows |
|---|---|---|
| Aluminium | `//` | base_plate, holder, collar |
| Aluminium, alt | `\|\|` | receiver, receiver_spigot |
| Brass | `..` | wingnut |
| Plastic | `oo` | collet, core_seat, washer, collet_105, core_seat_105 |
| Plastic, alt | `--` | liner |

The legend in the figure note matches. Equal hatch meets only across one_body pairs (collet|core_seat, holder|collar).

**Unsectioned.**
- carrier, core_100 and drill_head are drawn unhatched at zorder 3.
- The renderer splits carrier and core_100 under drill_head. The sense is right: x_front(head) - x_front(T) is +38.40 to +73.16 over the overlap. The same holds for the liner cut wall in figure 2.
- It also splits drill_head under carrier and core_100. That sense is wrong: x_front(head) - x_front(T) is -73.16 to -38.40, so the head's teeth line (z_S 257.54) and bottom edge (z_S 244.84) are drawn dashed across |u| < 50.50. See **FIX TP1.4-4**.

**Hidden.**
- Correct: the wing (dashed, unfilled), the slit ticks and the root lines are dashed.
- Wrong: carrier:line is a bond-line mark at z_S 262.50, wholly inside the drill-head outline and behind its front wall (203 of 203 samples), yet it is drawn solid. See **FIX TP1.4-5**.

**Beyond.** The wing is the only beyond artist. NOTE TP1.4-6 lists the visible far-side edges of the revolved bores, which are neither drawn nor named.

**Interior seams (concurrence with M1 D-F3).** A drawn edge with material of the same body on both sides asserts a face that does not exist. Interior seam length per side (MEASURED, carrier figure; spec pieces, one_body partners grouped):

| Body | Seam length per side | Edges |
|---|---|---|
| receiver + spigot | 77.98 | 12 |
| holder + collar | 41.41 | 8 |
| collet + core_seat | 23.95 | 7 |
| wingnut (+u) | 16.72 | 4 |
| washer | 0 | 0 |

The predicate for D-F3: the drawn outline of each cut body equals the boundary of the union of its pieces and its one_body partners. Every outline segment needs material on exactly one side (test offset 0.02). The scope is every section and side Axes that draws section_true (S1, S3, S4). The finding is the Designer's (F3); this cross-review adds no FIX of its own.

## 3 Ticks and sub-artists admitted as declared (task 3)

All values MEASURED, both figures; d 105 values follow the slash.

| Sub-artist | Drawn | Admission |
|---|---|---|
| collet:slits, +u (theta 112, top-open) | line u 57.40 from 47.00 to 72.00 | Top-face mid-radius (56.80 + 58.00) / 2. sin(theta) u > 0, cos < 0. Open end on the top face 72.00. Tick at the closed end 47.00, spanning the wall chord 50.50 to 62.408 / 53.00 to 62.408 |
| collet:slits, -u (theta 262, bottom-open) | line u -55.425 / -56.662 from 40.00 to 65.00 | Mid-radius 55.97 x sin 262 = -55.42 (DERIVED). Open end on the foot face 40.00. Tick at 65.00 spanning -59.234 to -50.50 / -53.00; the cone outer at 65.00 is 59.235 (DERIVED) |
| receiver:root | dashed at u +-72.29, 80.50 to 128.50 | Inside the thread piece (67.29 to 74.79) and the rim. External thread: minor inside the major, with the wing-nut bore on the major at 74.79 |
| wingnut:wing | dashed, unfilled box u +-7.00, 113.09 to 153.09 | Occluded over its whole z extent by the row's own body, relief, pocket rim and plate, with r_out 83.14 > 7.00. asin(7 / r_in) is 5.37 to 5.90 deg, under 45 deg. The theta 210 window lies 30 deg off the sight line |
| wingnut:sweep | dashed at u +-115.00, 97.09 to 153.09 | Sweep form (s1) to (s3) |
| carrier:line | solid at 202.50 | Mark position and span pass (M1 to M5). Drawn solid while hidden behind the head front wall: FIX TP1.4-5 |
| core_100:line | solid at 299.50 | Visible, above the head top 291.21 |

Admitted as declared, except carrier:line visibility (FIX TP1.4-5).

## 4 TP-n rows: parts drawn narrower than their footprint (task 4)

Drawn u extent against the footprint band, per side (MEASURED; every pose and figure equal):

| Sketch | Row | Footprint | Drawn | Narrower | Reason (true part) |
|---|---|---|---|---|---|
| S4 r1 | wingnut | +-115.00 (sweep) | +-95.14 (skirt) | 19.86 | Wings off the plane; the -X wing is drawn as the hidden sub-artist |
| S4 r1 | collet, collet_105 | +-67.29 (register bore) | +-66.99 (foot) | 0.30 | fit.seat_clearance |
| S4 r1 | base_plate | +-304.00 | +-130.00 | 174.00 | Crop, with break lines declared |
| S1 r9 | wingnut | +-115.00 | +-95.14 | 19.86 | Wings not drawn (Correction 2 of P6; M1 S1 F1) |
| S1 r9 | collet | +-67.29 | +-66.99 | 0.30 | as S4 |

The other S1 r9 changed rows (holder, collar, receiver, washer, core_seat) are not narrower. core_seat is wider (FIX TP1.4-3).

## 5 Findings

**FIX TP1.4-3 (TP1.1-11 class: a part drawn wider than its depth band).**

*Defect.* core_seat carries `depth: [-core.diameter_nominal / 2, core.diameter_nominal / 2]`, i.e. +-50.00. Its section_true ledge is drawn to r 50.50, the clamped bore (MEASURED, s1 l.324, s3 l.509, s4 l.358).

*Why it matters.* The depth band is the premise of the K7 depth-band relief and of plan_footprint. On the understated band, live S1 r9 relieves core_seat|liftmotor_a and core_seat|liftmotor_b as undeclared:depth-separated: band gap 0.302 in four poses, 8 pair-poses. Under the true band they overlap by 0.198 and are judged by XZ projection: F, 150.296 apart (MEASURED). The result is unchanged; the relief basis was false.

*Rule scope gap.* The TP-4 / LF-5 lint ("an explicit depth band must contain the placed part's true projection") reads placed rows only.

*Fix.*
- (a) In s1, s3 and s4, set core_seat `depth: ["-(core.diameter_nominal + collet.grip_window_hi) / 2", "(core.diameter_nominal + collet.grip_window_hi) / 2"]`. This is the core_seat_105 form. `collet.grip_window_hi` is already in core_seat keys in all three specs.
- (b) K7 extends the TP-4 lint to every row with section_true in a side or section view. The rule: depth contains [-r_max, r_max], where r_max is the largest |r| over the row's section_true pieces with plane_cuts ignored. Premise: a revolved row's X band equals its radial extent.
  - Z: live S1, S3, S4 after (a).
  - B: core_seat at +-50.00 in each spec, red on the pre-change specs (`depth_lint_pre.txt`: fires core_seat in s1, s3 and s4; 28, 28 and 17 row-poses read).
  - Scope: every side and section Axes. Plan views read plan_outline (NOTE TP1.4-8).

*Dry run* (scratch `ws\`, (a) applied):
- Lint: `depth_lint_post.txt` reads no firings.
- Check runs: S4 r1 14/14, S1 r9 19/19, S3 r8 16/16 (`run_s4.txt`, `run_s1.txt`, `run_s3.txt`).
- Pixels: all seven PNGs are SHA-256 equal to live wip (`png_sha.txt`), so no drawn change and no new revision.
- K7 state counts:
  - S4 and S3: equal to live; only core_seat distances move by 0.50.
  - S1: the 8 pair-poses above move from undeclared:depth-separated to undeclared:F.
- Controls K7-* plus K8-B54, B55, B77, B78: Z 19/19, B 39/39 match (`controls_fix1only.txt`).
- Process rule (i): the s1 and s3 spec edits re-run --stale at the fix pass.

**FIX TP1.4-4 (renderer clause (2) / (6): occlusion between two unsectioned bodies needs the depth sign).**

*Premise as written.* Clause (2) (TP1.3-11, mine) says an unsectioned body's front half "hides every area of the section inside its outline". That holds for cut and beyond areas, which lie at x <= 0. It does not hold for another whole unsectioned body.

*Rule.* O hides a point (u, z) of unsectioned T only where x_front(O, u) - x_front(T, u) > TOL_Z. Here x_front(B, u) = sqrt(R_B² - (u - c_B)²), with c_B and R_B taken from B's drawn outline (centre, half width).
- Premise: every unsectioned row is a solid of revolution with its axis in the plane, drawn whole. This is held by K8-B73 (straddle) and the K5 rectangle projection.
- Cut and beyond targets are unchanged.

*Live wrong splits* (`occl.txt`, MEASURED):
- S4 r1, both figures: drill_head (u +-88.90) split dashed under carrier and core_100 (u +-50.50), margin -73.16 to -38.40. Three splits on the two head artists.
- S3 r8: drill_head under core_750 (two artists), and coupling_c under screw_end_c and liftmotor_shaft_c, margins -8.62 to -5.50 and -9.17 to -7.00.
- The same renderer drew the accepted S3 r7. The fix lands with the next drawn S3 and S4 revisions.

*Controls.*
- (6c) converse: no hidden copy holds a sample where its row's front surface is nearer than every occluder.
- Z: live S3, S4 after the fix.
- B: the pre-change renderer on live S4 r1 (drill_head) and S3 (coupling_c).

*Scope.* Section Axes (render_section). S1 side views and S2 plan have no unsectioned-body renderer clause; the plan cover rule orders by z_max. Both are carried by name.

*Dry run* (prototype `_in_front` in `ws\sketch_common.py`, applied in `_occluded_by`; `sketch_common.fix2.py`):
- `occl_post.txt`: only right-sense splits remain (carrier, core_100, core_750 under drill_head; liftmotor_shaft_c and screw_end_c under coupling_c).
- S4 14/14 (`run2_s4.txt`) and S3 16/16 (`run2_s3.txt`).
- Controls K8-*, S4-*, K5-*: Z 33/33, B 200/204 (`controls_dry.txt`). The four mismatches still fire, at lower counts, so they are re-counts:

| Control | Was | Now |
|---|---|---|
| K8-B54 | 136 | 135 |
| K8-B55 | 12 | 10 |
| K8-B77 | 7 | 5 |
| K8-B78 | 7 | 5 |

  With TP1.4-3 alone these four match at the old counts.
- K7-* with both fixes: 19/19, 35/35.
- Pixels: `crop_r2.png` shows the head teeth line and bottom edge solid across the core; `crop_r1.png` (live) shows them dashed.
- This is a drawn change: S4 and S3 open new revisions.

**FIX TP1.4-5 (clause (6) line-family scope).**

*Defect.* render_occlusion and occlusion_issues read area artists only. A solid Line2D stroke behind a whole unsectioned body passes. Live firing set (`lines_hidden.txt`; 20 strokes read on S4, 5 on S3):
- S4 r1 carrier:line, both figures, 203 of 203 samples behind drill_head.
- S3 r8 anchor_bearing_c:line, 19 of 53 samples behind screw_c.

*Rule.* Every tagged Line2D stroke of a non-reference row, sub-artists included (marks, slit ticks, root lines, sweep), is split visible solid / hidden dashed by the occluders in front. That means the cut/beyond rule, plus the TP1.4-4 sign for unsectioned parents.
- (6a) and (6b) read the strokes, sampled at 0.5 mm, strictly inside by TOL_Z.
- Z: live after the fix.
- B: live S4 r1 carrier:line and S3 r8 anchor_bearing_c:line, red now.

*Scope.* Section Axes. S1 side views are carried by name; their side renderer has no occlusion clause.

*No value set.* The firing set above is the dry run of the predicate.

**NOTEs.**

- **TP1.4-6.** The section convention draws "beyond" in elevation. The visible far-side edges of revolved bores are neither drawn nor named, so the section-convention text and the figure note are silent on them. Examples (DERIVED):
  - Debris-hole edges at z_A 0 and 40 across |u| < 40.
  - The core-seat ledge inner edge at 40.
  - Collet chamfer and holder-bore transitions in the gap |u| 50.50 to 56.75 at 72.00, 79.09, 153.84 and 159.84.
  - The class covers S3 r7 / r8 and S4.
  - The Designer at M1 rules: draw them (a revolve-edge renderer clause) or name them in the convention text and figure note.
- **TP1.4-7.** The placer `on` filter has an empty-side path. A label.on naming a side with no ink leaves `cands[f]` empty, and `cands[f][0]` then raises IndexError: a run error, never a pass. The guard should record UNPLACEABLE.
- **TP1.4-8.** The r8-era `section` fields are still read in two places:
  - `plan_outline` reads them as the true plan annulus, e.g. core_seat [47.00, 50.00] against the drawn 47.50 to 50.50.
  - `plan_footprint` uses `section` to choose the depth disk.
  - Plan views draw neither row today (S2). Fix the field or exclude section_true rows when a plan view first draws them.
- **Carried unchanged.** N1 to N7 (P5T); TP-n at every M1.

## 6 Rulings on the P6 open items (orchestrator note)

1. **S4 `wingnut:sweep` against the TP1.4-2 reference row: S4 keeps the signed sub-artist. K5-B61, B62 and B64 stand.**
   - *Class.* TP1.3-20 / TP1.4-2 was "envelope ink under the part gid", read by K5, K6 and K7 as part geometry.
   - *S4 sits outside it.* Its sweep is gid `wingnut:sweep`, which `pieces(ax, "wingnut")` excludes. The drawn wingnut extent is +-95.14 (MEASURED).
   - *The class cannot be represented in any of the three specs.* Wingnut carries section_true in S1, S3 and S4 (X1 O2 (ii) presence). In S4 both forms of the defect fire:
     - Plant A, the sweep as Line2D under gid wingnut: K5 "Line2D on a prism row draws no area (TP1.1-9)".
     - Plant B, the TP1.3-20 dashed Rectangle under gid wingnut: K8 section_true "drawn Rectangle carries no section_true piece name", K7 receiver|wingnut overlap, K4 unplaceable.
     - Evidence: `plant_A.txt`, `plant_B.txt` (MEASURED).
   - *Two drawn forms remain* (reference row in S1/S3, sub-artist in S4). X1 compares neither, and both close the class.
   - *Label.* The S4 label "wing nut sweep r 115" anchored on the skirt is M1 S4 F1 (the Designer's).
2. **Placer `on` filter: accepted with no B of its own.**
   - It is placer code that only narrows the candidate list. It cannot admit a drawing that the check refuses.
   - The guard is K4 (s3), the anchor side, with B58 red by deletion.
   - Process rule (h) binds check rules and reliefs. That is why the Correction 8 relief had to go, and it does not apply here.
   - Empty-side path: NOTE TP1.4-7.
3. **Placer option `collinear`: SIGNED.**
   - `col_fail` is the per-leader test of `collinear_issues` minus two parts: the leader family and the own_continuation relief (FIX L3). So the placer is at least as strict as the check on every family it reads. The check still judges the leader family.
   - When the equal-aspect premise fails, the placer drops the filter and `collinear_issues` reports the premise: a fail.
   - Therefore the option can produce UNPLACEABLE, never a pass the check would refuse.
   - Deletion turns K4-Z14 and B57 to B59 red (P6 `deltest`).
   - The signature covers the option, not the threshold. At dpi 150, D 0.4152 paper mm is 2.45 px (DERIVED). M1 S4 F2 (leaders 3 to 8 px from edges) is the A.4 threshold question.

## Verdict

**FIX 3: TP1.4-3, TP1.4-4, TP1.4-5.**
- S4-3, the section look sign, the hatch-by-material table and the declared ticks PASS.
- TP1.4-3 carries its dry run (no pixel change).
- TP1.4-4 and TP1.4-5 change pixels of S4 and S3: S4 r2 and the next S3 revision. S1 r9 pixels are unaffected by all three.
- Concurrence with M1 D-F3, with its predicate (section 2).
- NOTEs TP1.4-6 to -8.
- Rulings: 1 keep the sweep sub-artist; 2 `on` filter accepted; 3 collinear signed.

## Gameplan lines to change

1. Design Notes open-items table, row TP-n (line 710).
Old:
```
| TP-n (narrower than footprint) | K8 projected_extent is containment only: a part drawn narrower than its footprint passes (probe: member drawn 60 wide as in r3). Safe for interference; only the M1 read sees it. S2 r1 (Topologist 1.2 (e)): 6 rows, liftmotor_a, _b, _c (42 square in its r 29.70 circle, 8.70) and pinion_a, _b, _c (trapezoid and hub in the radial rectangle, 15.00); drill_tube and drill_head outlines are solid disks flagged true over hollow parts (TP1.2-7, S3/S6); S3 r1 (Topologist 1.3 (e)): 5 rows, liftmotor_c in the section and the inset (42 square in r 29.70, 8.70), liftmotor_a, _b in the inset (1.01), nut_screws_c in the section (inside the nut-flange footprint, 32.00), each the true part | every M1 from 1.2 on | The Designer (M1); The Topologist at each (e) |
```
New:
```
| TP-n (narrower than footprint) | K8 projected_extent is containment only: a part drawn narrower than its footprint passes (probe: member drawn 60 wide as in r3). Safe for interference; only the M1 read sees it. S2 r1 (Topologist 1.2 (e)): 6 rows, liftmotor_a, _b, _c (42 square in its r 29.70 circle, 8.70) and pinion_a, _b, _c (trapezoid and hub in the radial rectangle, 15.00); drill_tube and drill_head outlines are solid disks flagged true over hollow parts (TP1.2-7, S3/S6); S3 r1 (Topologist 1.3 (e)): 5 rows, liftmotor_c in the section and the inset (42 square in r 29.70, 8.70), liftmotor_a, _b in the inset (1.01), nut_screws_c in the section (inside the nut-flange footprint, 32.00), each the true part; S4 r1 and S1 r9 (Topologist 1.4 (e), step1.4_topologist_crossreview.md): S4 wingnut (skirt r 95.14 in the sweep band r 115, 19.86; wings off the plane), collet and collet_105 (foot r 66.99 in the register band r 67.29, 0.30), base_plate (crop u +-130 in +-304, 174.00); S1 r9 wingnut (19.86, wings not drawn) and collet (0.30), each the true part | every M1 from 1.2 on | The Designer (M1); The Topologist at each (e) |
```

2. Design Notes open-items table, new row after row C1.3-b (line 716).
Insert after:
```
| C1.3-b | Loftsman NOTE LF1.3-11 (S2 spec source text still names r7) and LF1.3-12 (anchor faces measured against a bearing drawn solid); Topologist NOTE R2-6 (not_drawn literal x bands for pinions and base frame, margins 5.09 and 22.00, out of --stale reach) and R2-7 (arc a1 plan-only branch reachable only by a spec plant, no B); Designer DR4-2 (terminator relief bounds arrow position, not head width or connection style); r6 reviewer NOTE on rule (j) (only the first figure of a stall literal is held; 282.21 unheld); N2 ticks named in five S3 shape strings and not drawn; N4 stale W comment ; 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md` section 6): R2-6 bands as key expressions with a literal lint (K8-B90), R2-7 B (K5-B48), DR4-2 straight connection and the signed terminator style (K8-B91, B92; numeric half-width bound to The Designer, live 2.38 mm), rule (j) every number of a stall literal (K4-B37), LF1.3-11 text corrected, N4 already corrected at 1.3 r7; LF1.3-12 to Step 2; N2 ticks to S6 | 1.4 (S4) step 0 (harness items); S6 (ticks); Step 2 (LF1.3-12 bearing row) | The Engineer; raisers re-check |
```
New:
```
| TP1.4-3 to TP1.4-8 (S4 r1 / S1 r9 cross-review, step1.4_topologist_crossreview.md) | FIX TP1.4-3: core_seat depth +-50.00 under its drawn ledge r 50.50 in s1, s3, s4 (live S1 r9 relieves core_seat\|liftmotor_a, _b as depth-separated on it, 8 pair-poses); depth to (core.diameter_nominal + collet.grip_window_hi) / 2 and the TP-4 lint extended to every section_true row (depth contains the largest section_true radius); dry run: no pixel change, S4 14/14, S1 19/19, S3 16/16. FIX TP1.4-4: section occlusion between two unsectioned bodies by the front-surface sign x_front(O, u) - x_front(T, u) > 0 (drill_head drawn dashed under carrier, core_100, core_750; coupling_c under screw_end_c, liftmotor_shaft_c), converse clause (6c); K8-B54, B55, B77, B78 re-count 135, 10, 5, 5. FIX TP1.4-5: clause (6) over every tagged Line2D stroke (S4 carrier:line, S3 anchor_bearing_c:line drawn solid behind an unsectioned body). NOTEs: TP1.4-6 visible far-side bore edges neither drawn nor named (S3, S4; Designer at M1), TP1.4-7 placer on-filter empty side raises IndexError, TP1.4-8 r8-era section fields read by plan_outline as the true annulus. Rulings: S4 keeps wingnut:sweep (K5-B61, B62, B64 stand); placer on filter accepted, no B; placer collinear signed. Scope not reached: S1 side views (no occlusion clause), carried | 1.4 (d) fix pass; TP1.4-4, -5 open S4 r2 and the next S3 revision | The Engineer; The Topologist re-checks |
```
