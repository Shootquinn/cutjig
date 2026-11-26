## Corrections to the brief

1. **The over-cover Z controls do not reproduce a false hide on the pre-change code, except K8-Z12.** On the save-point-1 `sketch_common.py` (`scratchpad/p1r/pre`), with the Z9, Z10 and Z11 geometries left unrendered, the old `plan_cover_states` reads the bar `partial`, the old `hidden_rows` reads nothing hidden, and the old K8 passes (MEASURED). The r4 grid already caught these three cases. Only the Z12 geometry (ring visible in two 3 mm strips) reproduces the old false hide: old state `hidden`, old `hidden_rows` {ring}, old K8 "Annulus wholly under p, q drawn solid" (MEASURED). B44 to B46 are valid red-first controls for cover clause (2), the N2 class: the old K8 passes each one clean. They are not over-cover controls.
2. **The rule (e) anchor exemption passes a Design Notes 30 leader on live S2 r6.** The ring label anchor (209.75, -10.33) lies inside the outline of guide_tie_a (z_max 1285, above the ring at 1161.84). The last quarter of the leader runs 39.9 mm inside tie a (MEASURED, exemption switched off). The exemption lets it pass. The ring has visible ink elsewhere. Section 6.
3. **The opaque-fill clause can hide a nearer part, and an existing control already shows it.** The re-planted K8-B32 reason added at P1R tells the author that screw_a and guide_a (z_max 1225) lie "wholly under nut_a" (z_max 1170.84). The nut is lower. Its fill is drawn above them in the fixture only. Section 3, FIX TP1.3-2.
4. **The annulus sampler steps only by arc.** Across the width it still uses the five COVER_RINGS fractions: 27.5 mm apart on the ring (width 110). A filled ring under a 10 x 10 cover that lies between two sample radii is left solid by the renderer, and K8 passes (MEASURED). FIX TP1.3-1.

Tags: runs MEASURED 2026-11-26 on `docs/sketches/` (read only) and on scratchpad copies `scratchpad/p1rt/sk0_base`, `sk1`, `sk2`, with Python 3.12 and matplotlib 3.11.2. Hand values DERIVED. Thresholds DECLARED where proposed here. Images: `wip/s2_plan_r6.png` and `s2_plan_r5.png` were read as images.

## 1 Hand classification of three pieces

Rule under test: a point p of row L's drawn area is hidden when p lies in the true outline of a row X with z_max(X) - z_max(L) > 0.05, or in an opaque fill of another row drawn above. Signed tests are my own: annulus r - a and b - r; a radial rectangle in its (u, v) frame (u along theta, v tangential) as u - r_in, r_out - u, w - |v|; a disk as R - |p - c|; a convex polygon as the least signed edge distance on its counter-clockwise ring. p is inside when every term is ≥ 0. Harness: `cover_hits` on the artist's covers, then the drawn region (clip path) of the solid original and of the hidden copy.

### 1a Ring rim under guide arm a (bracket_guide_a: theta 150, r 181 to 244, w 30, z_max 1225; ring (100, 210), z_max 1161.84)

| Point | Own test | Covering test | dz | Hand | Harness |
|---|---|---|---|---|---|
| P1 r 195, theta 150 (-168.875, 97.500) | r - a +95.00, b - r +15.00 | arm: u 195.00, v 0.00: u - 181 +14.00, 244 - u +49.00, 30 - abs(v) +30.00. guide_a -14.00, nut_housing_a -10.00, frame_upper_a -49.00 (outside) | +63.16 | hidden (arm) | bracket_guide_a, deep; original clip excludes P1, copy clip contains P1 |
| P2 r 200, theta 160.08 (-188.032, 68.146) | +100.00, +10.00 | arm: v +35.00, so 30 - abs(v) = -5.00 (outside); guide_a -29.87, nut_housing_a -25.87, frame_upper_a -47.09 | n/a | visible | no hit; original clip contains P2, copy clip excludes it |
| P2' r 200, theta 139.92 (-153.032, 128.768) | +100.00, +10.00 | arm: v -35.00, 30 - abs(v) = -5.00 (outside); same misses | n/a | visible | no hit; original clip contains P2' |

The rim's covered arc under the arm is drawn dashed by the hidden copy, and the rim on each side 5 mm past the arm edge stays solid. In the r6 image the rim is dashed where it crosses both arms and solid between them. This closes N2 (M1 S2 r3).

### 1b Rail top in the +Y notch (base_frame piece (-322, 244) to (322, 304), z_max 60; base_plate pieces z_max 72; notch x in (-35, 35), y in (239, 304))

| Point | Plate pieces (signed, least term) | Other higher outlines | dz plate | Hand | Harness |
|---|---|---|---|---|---|
| P3 (0, 274) | centre piece 239 - y = -35.00; left notch piece -35 - x = -35.00; right notch piece x - 35 = -35.00 | frame_upper_a -207.29; arms, guides far | +12.00 | visible | no hit; rail original clip contains P3 |
| P3' (30, 250) | centre -11.00; right piece x - 35 = -5.00 | far | +12.00 | visible | no hit; original clip contains P3' |
| P4 (100, 274) | right piece: x - 35 +65.00, 322 - x +222.00, y - 239 +35.00, 304 - y +30.00 | far | +12.00 | hidden (plate) | base_plate, deep; copy clip contains P4, original excludes it |

The operator sector (alpha 0.5, no z_max) is not a cover. The rail top in the notch, the TP1.2-13 live case, is drawn solid through the translucent sector, and the rest of the rail is dashed.

### 1c Nut a under its guide block (nut_a and guide_a both disks r 21 centred (-138.564, 80.000), r_c 160 theta 150; nut z_max 1170.84, guide z_max 1225; nut_housing_a r 25, z_max 1170.84; screw_a r 4, z_max 1225)

| Point | guide_a (R - d) | screw_a | nut_housing_a | dz | Hand | Harness |
|---|---|---|---|---|---|---|
| P5 r 170, theta 150 (-147.224, 85.000) | 21 - 10 = +11.00 (128-gon inradius 20.994: +10.99) | -6.00 | dz 0.00: not higher, no cover | +54.16 | hidden | guide_a, deep |
| P6 centre | +21.00 | +4.00 | dz 0.00 | +54.16 | hidden | screw_a (first cover listed), deep |

The nut outline equals the guide block outline, the guide block is 54.16 higher, and so the whole nut is covered. The harness restyles the nut in place: Circle, "--", no fill, no clip, state hidden by guide_a and screw_a. Its brass fill was opaque and is no longer a cover (`cc["opaque"]` drops it).

**Agreement: 8 of 8 points.** The harness classification matches the hand sign tests on every point. `probe7.py` in the scratchpad.

## 2 Renderer premise and premise checks

| Premise | Enforced by | Z / B | Verdict |
|---|---|---|---|
| Only true outlines cover. Circumscribing footprints (lift motor square in its circle, pinion trapezoid in its rectangle, depth-band disk) never cover. | `cover_table` takes `plan_outline(...)[2]` true only | K8-Z7, K8-B33 (existing) | SIGNED |
| Opaque per the alpha rule: opaque at rendered alpha ≥ 0.75, see-through at ≤ 0.5, the band refused | cover clause (4) lint | Z live (alphas 1 and 0.5), B49 (0.95), B50 (0.6) | SIGNED. The face colour alpha is the rendered alpha, since matplotlib replaces the face alpha with the artist alpha when one is set. NOTE TP1.3-5 on stacked fills. |
| An opaque fill drawn above an artist lies at or above it in z (the draw order agrees with depth) | **not checked** | none | **FIX TP1.3-2** |
| Drawn region = geometry inside the artist's own clip path | `drawn_region` | B48, Z8 | SIGNED. `drawn_region` reads private attributes (`_path`, `_transform`), so re-check it on a matplotlib upgrade. |
| Covered region exact | `region_split` | Z9 to Z11, B44 to B46, random test (below) | SIGNED |
| Render state per piece decided on samples | `_cover_samples` | none | FIX TP1.3-1 (annulus radial); NOTE TP1.3-4 (2.5 mm residue) |

**Why the opaque clause needs a depth premise.** The renderer takes artists from the top of the draw order down. A lower opaque part L is processed before a higher part H drawn under it. If H's outline is true and covers L, L is split first, and its opaque region loses H's outline. The inversion then cannot hide H, and on live S2 r6 that is the case: the shaft fills over the gear are corrected this way (MEASURED: the gear reads visible). The inversion goes through in three cases:
- H's outline is not true: lift motors, pinions;
- the covering fill belongs to a row with no z_max (a zone);
- K8 is judging a planted fill.

In each case H is drawn dashed under a lower fill, and K8 passes, because K8 uses the same rule. Measured:
- **Sector at alpha 0.95 set before `render_plan`** (live S2 otherwise): the three plate pieces under the sector are split and dashed, and K8 passes with 208 predicates. A reference zone silently erases the plate. Compare K8-B49, which sets the alpha after rendering and so fires on solid pieces.
- **K8-B32 at P1R:** the filled nut_a drawn above screw_a and guide_a. K8 reports the two higher parts as "wholly under nut_a drawn solid", which is an instruction to dash nearer parts.
- **Live S2 r6:** the only drawn-hidden samples under an opaque fill alone are guide_a/b/c under screw_a/b/c. The z_max values are equal (1225 = 1225), so the tie is broken by draw order. This is legitimate.

**FIX TP1.3-2 (Engineer implements; Topologist signs).** Add K8 cover clause (5). An opaque fill of another row, drawn above an artist and containing one of its drawn samples, must belong to a row with a z_max at least z_max(artist) - 0.05. Otherwise fail with "opaque fill of X drawn above it lies behind it or is no part (z_max ..); an opaque fill hides only what lies behind it".
- Z: live S2 r6 clean.
- B (new, K8-B51): sector alpha 0.95 set in the style before `render_plan`. It fires 3, one per plate piece. The current code passes it (red-first shown).
- Existing B counts under (5) (MEASURED in the `sk2` copy):

| Control | Count change | Lines added by (5) |
|---|---|---|
| K8-B6 | 2 to 3 | screw_b under screw_c (fixture rows without z_max) |
| K8-B32 | 3 to 5 | screw_a and guide_a under nut_a |
| K8-B39 | 3 to 7 | plate under the sector |
| K8-B49 | 3 to 7 | plate under the sector |

  Under (5), B32's two "wholly under nut_a" lines become correct defect reports, because the inverted fill is named.
- Dry-run (copy `sk2`, scratchpad): 276 controls. Z 73/74 (K4-Z3 red as before: drill_head). B 196/200: the four count changes above, every one of them a (5) line. Smoke 2/2.

## 3 Sampling and region split (TP1.2-13, TP1.2-19)

**Exact region split, signed.**
- `region_split` was tested against direct membership. The test used 60 random unions of 1 to 5 shapes (annuli with open bores, and convex 3- to 9-gons), with points farther than 0.02 mm from every ring edge: 89,952 points, 0 disagreements. Hidden pieces hold exactly the points in the union, and visible pieces the rest (MEASURED, `split_test.py`).
- The slab argument holds:
  - slab edges lie at every vertex x and at every crossing between edges of two shapes;
  - edges within one shape do not cross (convex pieces; annulus rings are concentric; opaque rings are clipped per convex clip piece);
  - so inside a slab the order is fixed, and a union merged at the slab middle holds over the whole slab.
- The outer circle is inscribed and the bore circumscribed, so the hidden region lies inside the true covered region. The visible clip keeps slivers of at most 0.01 mm inside a cover's circular edge. Clause (2) needs a depth greater than 0.05, so the two agree.

**Arc-length annulus samples, signed.** These are 528 directions on the ring. K8-Z12/B47 is a valid red-first pair (Correction 1).

**FIX TP1.3-1 (Engineer).** Annulus samples step at most 2.5 mm across the width as well as along the arc: `m = max(5, ceil((ro - ri) / 2.5) + 1)` fractions evenly spaced from 0.02 to 0.98. Today the radial step is (ro - ri)/4: 27.5 mm on the ring, 9.1 mm on the gear. Measured on the current code: a filled annulus (100, 210) under a higher 10 x 10 cover centred at r 140 or 165, both between sample radii 127.5, 155 and 182.5, is left `visible` (solid, filled) by the renderer, and K8 passes. That is the N2 defect: the fill shows under a nearer unfilled part.
- B (new, K8-B52): that fixture with the ring filled, drawn by the current renderer. The current K8 passes it. The fixed K8 fires "Annulus partly covered drawn solid (24 of 23760 drawn samples under d by more than 0.05)" (MEASURED). After the fix the renderer splits the ring, and K8 is clean on the re-render (Z).
- Dry-run (copy `sk1`):
  - live S2 r6 render states equal, PNG bytes equal, K8 pass with 206 predicates;
  - build plus K8 14.5 s against 14.1 s;
  - 276 controls: Z 73/74 (K4-Z3, unchanged), B 200/200, smoke 2/2, every row equal to the unpatched copy.
- The radial cap applies to `hidden_rows`, which calls the same sampler, as well.

**NOTE TP1.3-4 (sampled render state).**
- The split geometry is exact, but the render state (visible, hidden or split) is decided on samples at most 2.5 mm apart. A visible strip narrower than the step can be restyled wholly dashed, and a cover narrower than the step can leave a piece solid. K8 samples the same points, so it agrees with the error.
- Measured: a bar 120 x 40 with a 1.0 mm visible gap between two higher covers is drawn wholly dashed in 2 of 4 gap phases (gap at 150.0 and 151.9), and K8 passes. The visible ink is two 1 mm edge segments.
- No live case. Declare 2.5 mm as the K8 cover resolution in the K8 row. At S3, if a drawn part or gap narrower than 2.5 mm appears, decide the state from `region_split` (area of the artist inside the hidden and visible pieces) and drop the sampling.

**TP1.2-13: CLOSED.** The live case (rail top in the +Y notch) is drawn solid, hand check 1b. Union, annulus and hollow-disk covers are exact in the split (Z9 to Z11). The residue is TP1.3-4.

**TP1.2-19: CLOSED** for the arc step and the alpha rule. The radial step remains open as FIX TP1.3-1.

**TP1.2-7 left with solid disks: SIGNED as left open.**
- The cutter is drawn as its rim only (dotted, unfilled). The rim at r 88.9 lies under gear_hub (76.2 to 90) and the bearing, not in the tube bore, so the solid-disk outline of drill_tube (0, 76.2) misjudges no drawn ink.
- The plate tint removed inside the tube bore is correct as seen: the cutter head (z above the plate) fills that view, and it is drawn unfilled.
- A filled or hatched part inside a hollow true disk's bore would be falsely hidden. This stays with S3/S6 under TP1.2-7.

## 4 S2 r6 changed rows: K8 sense, plan_extent, K9

- **Piece geometry per row, r5 against r6.** The r5 script and library ran from the save-point-1 copy; r6 is live. `sc.pieces` was read on every one of the 72 rows. The set of piece polygons is equal on every row (MEASURED, `dump.py`). Only the counts differ:

  | Row | r5 pieces | r6 pieces |
  |---|---|---|
  | base_frame | 8 | 6 |
  | pinion_a, pinion_b, pinion_c | 3 each | 2 each |

  The extra r5 pieces were duplicate solid copies drawn by hand. `pieces()` leaves out renderer copies, so K8 sense, plan_extent, K6 centres and the K7 plan pairs read the same geometry as at r5.
- **K8 record.** r5 has 190 predicates, r6 has 206. The 16 added are cover tests on the 16 hidden copies (K5 105 to 121 artists). No sense or plan_extent predicate changed result.
- **K6:** 69 centres, equal. **K7:** 1292 plan pair tests, equal states.
- **K9:** 70 rows, pass. Every hidden copy carries its row's gid, and no orphan gid exists.

**K8 sense and plan_extent unchanged on split rows: CONFIRMED. K9 coverage with split pieces: CONFIRMED.**

## 5 Images

- r6 against r5: the ring rim is dashed under both guide arms and arm c, and solid between them (N2 closed).
- The plate tint is removed inside every nearer part's outline, so unfilled nearer parts read white. This convention is the Designer's (P1Rd item 1).
- The ring fill is removed under the arms, ties, housings and mounts. The gear-zone pinion teeth and shaft ends are dashed.
- No solid edge appears inside a cover that the hand rule calls hidden at the three hand-checked pieces.

## 6 K4 rule (e): half-space view (premise is the Designer's to sign)

**The z premise is sound.** It is the K8 cover predicate: q in outline(X) and z_max(X) - z_max(L) > 0.05. With it, rule (e) reads: the leader's last quarter lies in the region where L is not covered by a true outline. Seen from +Z, a point of that region shows L or something behind it, never a nearer part. A leader end over a lower part (plate, base frame, ring under the gear) still ends on L's ink and is not read as pointing elsewhere. Rows with no z_max count every outline, which is strict but safe.

Two gaps follow.

**FIX TP1.3-3 (to the Designer for the premise; the Engineer implements). The anchor exemption is broader than its stated reason.**
- The stated reason is "a hidden part under its cover: no leader can end on that ink without entering it". That is true only for a row with no visible ink.
- As written, the exemption applies whenever the anchor lies in X, and the placer accepts an anchor on hidden ink (dashed copy) when an unfilled cover makes rule (a') blind.
- Live S2 r6, measured with the exemption switched off:

  | Label | Anchor | Last quarter inside | Row wholly hidden? |
  |---|---|---|---|
  | ring | (209.75, -10.33) | guide_tie_a 39.9 mm | no |
  | descent_stop | (-166.21, 112.12) | bracket_guide_a 50.2 mm, ring 10.9 mm | yes |
  | operator_sector | (282.84, 282.84) | base_plate 21.0 mm, base_frame 21.0 mm | zone |

  The ring case is the Design Notes 30 defect (a leader end running inside a tie), passed by the exemption.
- Proposed premise (3'): an outline containing the anchor is exempt only when the labelled row has no z_max or is wholly hidden (`hidden_rows`). Otherwise the anchor lies outside every higher true outline.
- B: K4-B14, the r6 ring leader at its live anchor. The current code passes it; under (3') it fires "ends inside the outline of guide_tie_a (39.9 mm)". Z: live S2 after the placer re-runs.
- **Dry-run (monkeypatched, live S2):**
  - the ring re-anchors at (207.43, -32.52), clear of tie a;
  - the stacked layout then leaves a ring/drill_tube leader crossing, and K4 reads 2 issues (drill_head unplaceable, ring and drill_tube cross) (MEASURED, `probe10.py`);
  - **the dry-run does not converge on the current placer.** Under detail 1 common (h) this returns to me as raiser and opens no revision until the Designer chooses the premise and the placer resolves the crossing.

**drill_head UNPLACEABLE is geometric, not a search miss (DERIVED).**
- The anchor on the cutter rim (r 88.9) lies inside two exempt outlines: gear_hub (76.2, 90) and the bearing. drill_tube (0, 76.2) and the gear (90, 126.32) are higher and do not contain it.
- The longest straight run from a rim point that stays in r ∈ [76.2, 90] is the chord tangent to the tube circle: sqrt(88.9² - 76.2²) + sqrt(90² - 76.2²) = 45.8 + 47.9 = 93.7 mm.
- A leader to the margin column (text end x ±366.8, MEASURED from the placer record) along that chord has length ≥ 366.8 + 45.8 = 412.6 mm, so a last quarter of 103.2 mm, longer than 93.7. For |y0| = 80 the free run is 80.0 against a quarter of 101.4.
- So no straight margin leader passes (e) from that rim. The remedy is the Designer's. Options:
  - cap the end length (min(L/4, a declared length)), which makes (e) a local test at the anchor;
  - an in-figure label;
  - a figure-note entry.

**NOTE TP1.3-6 (Engineer). The placer exits a failing layout without recording it.** In the (3') dry-run, the 3 rounds ended with a crossing and no UNPLACEABLE entry. K4 still fails (crossing), so the failure is not silent, but the placer record should name the label as "layout unresolved".

## 7 Findings

| ID | Kind | Owner | Item |
|---|---|---|---|
| TP1.3-1 | FIX | Engineer | Annulus samples step ≤ 2.5 mm across the width. B K8-B52 (filled ring under a 10 x 10 cover at r 140). Dry-run: live unchanged and PNG equal; controls unchanged. |
| TP1.3-2 | FIX | Engineer; Topologist signs | K8 cover clause (5): an opaque fill hides only a row at or below its z_max + 0.05, and a fill of a row without z_max hides nothing. B K8-B51 (sector 0.95 before the renderer). B6, B32, B39, B49 counts become 3, 5, 7, 7. Dry-run: Z clean. |
| TP1.3-3 | FIX | Designer (premise), Engineer | Rule (e) anchor exemption only for wholly hidden rows or rows without z_max. Live ring leader 39.9 mm in tie a. Dry-run does not converge (ring/drill_tube crossing): returns to raiser pending the Designer. |
| TP1.3-4 | NOTE | Engineer, S3 | Render state sampled at 2.5 mm. Declare it as the K8 cover resolution; at S3 decide state from `region_split` if needed. |
| TP1.3-5 | NOTE | Designer | Translucent fills compound: two 0.5 fills render 0.75 over what lies under both. No live case (sector and ring overlap only over the plate, which the ring's outline already hides). Lint per fill only. |
| TP1.3-6 | NOTE | Engineer | Placer: an unresolved layout after 3 rounds is recorded. |
| TP1.3-7 | NOTE | Engineer | `drawn_region` reads private matplotlib attributes; re-check on upgrade. |

Rows signed now, from Engineer section 9:
- 1 (true-outline clause);
- 2;
- 3;
- 4;
- 5 (clause (2));
- 6;
- 7 (arc step);
- 8;
- 9 (TP1.2-7 left open).

Signed after the FIXes land: the opaque-fill clause of rule 1 (TP1.3-2) and the radial half of rule 7 (TP1.3-1).

**Verdict: FIX** (TP1.3-1, TP1.3-2 on the renderer; TP1.3-3 on rule (e), to the Designer). Hand-check agreement 8/8.

## Gameplan lines to change

**l.142 (K8 row), rule cell.** Apply after the P1R change. Old is the P1R New text ending:
```
alpha-rule premise: no plan fill alpha in (0.5, 0.75) |
```
New:
```
alpha-rule premise: no plan fill alpha in (0.5, 0.75); P1Rt (step1.3_topologist_renderer_signoff.md): annulus samples also step at most 2.5 mm across the width (TP1.3-1); cover (5) an opaque fill drawn above an artist hides it only when the fill's row has a z_max not lower than the artist's by more than 0.05, a fill of a row without z_max hides nothing (TP1.3-2); render state per piece decided on samples at most 2.5 mm apart, the declared cover resolution (TP1.3-4) |
```

**l.142 (K8 row), B cell.** Apply after the P1R change. Old is the P1R New text ending:
```
B22 re-rendered |
```
New:
```
B22 re-rendered; K8-B51 operator sector at alpha 0.95 set before the renderer (cover (5), TP1.3-2); K8-B52 filled annulus under a 10 x 10 cover between the r4 sample radii (TP1.3-1); K8-B6, B32, B39, B49 planted counts 3, 5, 7, 7 under cover (5) |
```

**l.296 (detail 1.3 carried item 4).** Apply after the P1R change. Old is the P1R New text ending:
```
signatures P1Rt, P1Rd; section-view convention at P4;
```
New:
```
signatures P1Rt, P1Rd; P1Rt (`research/sean/cr_scratch/step1.3_topologist_renderer_signoff.md`): hand classification 8/8, renderer FIX TP1.3-1 (annulus radial step) and TP1.3-2 (opaque fill depth premise, cover (5)), rule (e) anchor exemption FIX TP1.3-3 to the Designer (ring leader 39.9 mm inside tie a; dry-run not converged), drill_head UNPLACEABLE geometric (free run 93.7 mm against a last quarter of at least 101 mm); section-view convention at P4;
```

**l.666 (Design Notes 25, TP1.2-13 row).** Apply after the P1R change. Old is the P1R New text ending:
```
awaiting P1Rt signature | 1.3 (S3) | The Topologist proposes; The Engineer |
```
New:
```
CLOSED at P1Rt: live notch case drawn solid (hand check), union, annulus and hollow disk exact in the split; Z9 to Z11 are not over-cover red-first (the r4 grid caught them), Z12/B47 is; residue NOTE TP1.3-4 (render state sampled at 2.5 mm) | 1.3 (S3) | The Topologist proposes; The Engineer |
```

**l.667 (Design Notes 25, TP1.2-18/19 and N2 renderer row).** Apply after the P1R change. Old is the P1R New text ending:
```
awaiting P1Rt and P1Rd signatures | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer co-owns the renderer |
```
New:
```
P1Rt: arc step and alpha rule SIGNED; radial step open (FIX TP1.3-1); opaque fill depth premise open (FIX TP1.3-2); rule (e) anchor exemption to the Designer (FIX TP1.3-3); awaiting P1Rd signature | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer co-owns the renderer |
```

**Design Notes 25, new row.** Insert after the TP1.2-18/19 row (l.667):
```
| TP1.3-4 to TP1.3-7 (renderer notes) | render state sampled at 2.5 mm (declared resolution; region_split decides at S3 if a part or gap narrower appears); stacked translucent fills compound (two 0.5 fills render 0.75); placer records an unresolved layout after its rounds; drawn_region reads private matplotlib attributes | 1.3 (S3) | The Topologist proposes; The Engineer; The Designer (TP1.3-5) |
```
