# Step 1.0 Wave 2: Topologist cross-review of K5, K8, K7 classes, K9

Verdict: CROSS-REVIEW FAIL (TP-1 BLOCK; TP-2 to TP-9 FIX). One BLOCK, eight FIX, five NOTE.

All controls for K5, K7, K8, K9 re-run in-process from `fixtures/builders.py` (no harness file written): 19 of 19 behave as the manifest states, each B on its planted reason (MEASURED). Probe script: `C:\Users\UR\AppData\Local\Temp\claude\1df41a1c7c14cc45\6efaddfb-5e83-4849-8803-49d5d7303110\scratchpad\topo_probe.py`; probe results below are MEASURED from it. Paths are under `research/sean/cr_scratch/sketches/`.

## 1. K5, projection classification

Rule in code (sketch_common.py 520-551): kind cylinder or screw, axis equal to the view normal: circle, otherwise rectangle; kind cone or gear: circle, otherwise trapezoid; any other kind, or no axis: no expectation, except that a Circle or Ellipse in a side view fails. `classify` (504-517): Circle/Ellipse = circle; Rectangle = rectangle (rotation ignored); 4-vertex Polygon with axis-aligned edges = rectangle, any other quad = trapezoid; otherwise the type name.

Paths by which a wrong projection passes:

| Path | Result | Probe |
|---|---|---|
| Circle approximated by a Polygon (64 vertices) on a prism, plate or line row in a side view | K5, K6, K9 pass | G (nut_a) |
| Cylinder row with `axis` missing: rectangle in plan passes; only a true Circle in side view is caught | no expectation | code 521-522 |
| Text artist carrying the row's gid | K9 counts it (746), K5 never sees it | D (guide_member) |
| Artist on a second Axes (inset) | every check reads `fig.axes[0]` only | H |
| Patch drawn with a non-identity artist transform | measured coordinates differ from rendered ones | A, C2 (TP-1) |
| Rotated Rectangle (tilted cylinder) | classified rectangle; K6 fires on the changed z extent | code 507 |

A Circle in a side view on a cylinder, screw, cone or gear row with an axis fires (K5-B1). A cylinder with axis Z drawn as a Rectangle in plan fires (want circle). Those two paths are closed. The open ones are TP-1, TP-6, TP-7.

## 2. K8, seed predicates as sign checks

Notation: c_z(F) is the area-weighted centroid z of the drawn pieces of F; z_lo, z_hi drawn extents; all from `artist_polys`, which is drawn data coordinates except under TP-1.

| Seed | Invariant (sign form) | In s1_spec | From drawn coordinates | Gap |
|---|---|---|---|---|
| Head below gear and top block | c_z(head) − c_z(gear) < 0; c_z(head) − c_z(top_block) < 0 | drill_head sense (204) | yes (711-714) | none in data; TP-1 in rendering |
| Tip below top | z_lo(head) − z_hi(top_block) < 0 | implied by the row above | yes | none |
| Core bottom on the core stop | abs(z_lo(core) − z_hi(core_seat)) ≤ 0.05 | core_500, core_750 rests_on (172, 188) | yes (715-718) | core_750 at load contradicts the pose table (TP-9) |
| Anchor below nut below guide, per screw per pose | c_z(anchor) < c_z(nut) < c_z(guide) | anchor_a/b, nut_a/b (428, 443, 458, 473) | yes | centroid order, not half-space separation (TP-10) |
| Gear section mirrored about the drill axis at equal z | for every vertex p of gear, a vertex q with abs(2·x0 − p_x − q_x) ≤ 0.05 and abs(p_z − q_z) ≤ 0.05, x0 = centroid x of drill_tube; at least two pieces | gear (317) | yes (719-724) | a z-flipped bevel section is also mirror-symmetric: probe K passes (TP-2); x0 is never tied to x = 0 (TP-3) |
| Motors on the stated side of the gear | sign((x_motor − x_pinion)·cos θ) > 0 (radially outboard), and same z side of the gear plane in every pose | motor23_a/b `above ring` (364, 380) | yes, but the predicate is vacuous: motor z_rule starts at ring_top | probe J: motor mirrored to +x passes K5, K6, K8 (TP-3) |
| Plan axes not inverted | `xaxis_inverted()` false and `yaxis_inverted()` false | n/a (S1 is side only) | yes, axes[0] only (696) | inset axes unchecked (TP-7) |
| Azimuth counter-clockwise from +X seen from +Z | abs(wrap(atan2(c_y, c_x) − θ_key)) ≤ 0.1 deg | plan fixture only; S1 screws via S1-6 | yes (725-731) | screws only in side view (TP-3) |

K8-B3 detection: `ax.yaxis_inverted()` after `invert_yaxis()` (builders.py 439-440). Further cases:
- x-axis inversion fires, same expression: "plan: axis inverted (x True, y False)" (probe B).
- Mirrored data (y drawn as −r sin θ, axes normal) fires only through the azimuth predicates: 330 against 30, 210 against 150, 90 against 270 (probe C). In a side view no azimuth predicate exists; S1-6 catches a mirrored x for the screws only.
- Mirrored artist transform (`Affine2D().scale(1, -1) + ax.transData`) does not fire (probe C2). See TP-1.

Hand value, K8-B1: flipped head spans [hi − head_length, hi], hi = tip_S + drill.length + top_block_length = 244.84 + 800 + 150 = 1194.84, head [1088.47, 1194.84], centroid 1141.66 (DERIVED); code 1141.7 (MEASURED). Gear right piece is a trapezoid with bottom width 50 and top width 35 over height 30 from ring_top 456.84: centroid 456.84 + 30·(50 + 2·35)/(3·85) = 470.96 (DERIVED); code 471.0 (MEASURED). K8-Z plan screw_a at (160 cos 30, 160 sin 30) = (138.56, 80.00): atan2 = 30.00 deg (DERIVED); code clean at 0.1 deg (MEASURED).

## 3. K7 classes as half-space statements

- C (judge 365-366): distance ≤ 0.05 and overlap area ≤ 0.01 mm². Closures meet, interiors do not overlap beyond tolerance: contact with no penetration. Correct.
- G (367-368): overlap area ≤ 0.01 and distance ≥ g_min − 0.05. Interiors disjoint and separated by g_min. Distance is unsigned; penetration appears as area only. `pair_state` (358-361) labels a 9 mm G pair "F" (K7-B3 reason "state F") and never reports a signed gap (TP-11).
- F (369-370): overlap area ≤ 0.01. Interiors disjoint; touching passes, so F contains C. Matches gameplan l.140 "F free (overlap 0)".
- Depth separation (604-605, 622): pair skipped when the spec depth bands are disjoint (strict inequality; touching bands are tested). If each band contains the true Y extent of its part, disjoint bands imply disjoint solids, so separation is sound. It masks a real overlap when a band is narrower than the part. The draft spec writes radial parts at oblique azimuth as a point plus or minus a half-width (TP-4). A missing band (`depth: null`) never separates: fail-safe.
- Plan: no depth separation for static pairs (overlap in plan of parts at different heights fires: conservative). The swept plan case skips pairs with disjoint z bands (665-669): sound for vertical motion.
- Coverage: only declared neighbour pairs are tested (614-616). An overlap between two undeclared parts is invisible (TP-5).

## 4. K9, gid uniqueness and wrong-kind coverage

- Several artists sharing a gid is by design (gear: two mirrored pieces). It needs no uniqueness rule.
- Duplicate spec row ids are not detected: K5, K7, K8 build `{r["id"]: r}` (532, 609, 691), the later row wins; K9 uses a set (741). Probe E: a second anchor_a row with empty sense hides the K8-B2 defect from K8 and K9 (TP-8).
- A spec row is satisfied by any artist with its gid: a Text (probe D) or a shape of the wrong kind on a row K5 has no expectation for (probe G) (TP-6).

## 5. Control figures

Read as images. ctrl_a (K8-B1) and ctrl_b (K8-Z) differ only in the drill_head, drill_tube and drill_top_block artists and their two labels; floor, core, core seat, ring, gear, motor, screw, anchor, nut, guide and guide member are identical. Titles are both "side_xz: control figure". PNG text chunks hold only "Software: Matplotlib version3.11.2" (MEASURED). No text names the good or bad figure. key.json sits beside the PNGs in `fixtures/figs/`: the reviewer gets the two PNGs alone. Observations in TP-12.

## 6. Findings

**TP-1 BLOCK. Checks measure pre-transform coordinates; a part rendered upside down passes K5, K6, K7, K8 and S1-x.** sketch_common.py 169-185: `artist_polys` maps a Patch path through `get_patch_transform()` only and reads `Line2D.get_xdata()` raw; the artist's own transform is ignored. Probe A: drill_head, drill_tube and drill_top_block given `Affine2D().scale(1, -1).translate(0, lo + hi) + ax.transData`. Rendered head z [1088.47, 1194.84]; measured head z [244.84, 351.21]. K6 pass, K8 pass. Probe C2: plan screws mirrored by transform, K8 pass. This is the known failure the harness exists for, and K1 does not forbid `transform=`; a sketch that rotates pinions or motors with `Affine2D().rotate_deg_around` uses this path. Fix: compute pieces in rendered data coordinates, `(a.get_transform() - ax.transData).transform(path.vertices)` for patches and lines (Collections through their offsets and transforms), or fail any tagged artist whose data transform is not `ax.transData`. Add a K8 B fixture: drill flipped by transform only.

**TP-2 FIX. No sense predicate for taper; an inverted cone or bevel gear passes.** sketch_common.py 520-527 (K5 accepts any non-axis-aligned quad as trapezoid), 690-734 (no taper predicate). Probe F: a collet trapezoid narrow-up and narrow-down both pass K5 and K8. Probe K: gear section flipped (wide face at top) passes K5, K6, K8. s1_spec: collet (102, "narrow end per cone.alpha"), gear (308, "teeth facing the pinions"), pinion_a/b carry the sense in prose only. Fix: predicate `taper: {narrows: up | down | outward | inward}`, computed per piece as sign(width at z_hi − width at z_lo) for axis-Z rows and sign(height at outer x − height at inner x) for radial rows; add it to collet, gear, pinion_a/b; B fixtures: collet inverted, gear section flipped.

**TP-3 FIX. Horizontal placement is checked for the screws only; "motor side" is vacuous.** checks_s1.py 147 loops `screw_a`, `screw_b`. Rows with an azimuth (pinion_a/b, motor23_a/b) are not checked; rows that place by angle in `depth` (nut_a/b, anchor_a/b, guide_a/b, liftmotor_a/b, frame_upper_a/b, guide_member, descent_stop) carry no `azimuth` field. s1_spec 364, 380: motor `above ring` holds by construction (motor z_rule starts at ring_top). Probe J: motor23_a mirrored to +x passes K5, K6, K8. The drill axis is never tied to x = 0; the gear mirror predicate uses the drill_tube centroid, wherever drawn. Fix: one K8 predicate `projected_x: {r: expr, theta: expr}` asserting drawn centroid x = r cos θ in side views, applied to every placed row; motor side as sign((x_motor − x_pinion)·cos θ) > 0; drill rows centroid x = 0 within 0.05. B fixture: motor mirrored to the far side.

**TP-4 FIX. Depth bands of radial parts are narrower than the parts; depth separation can mask an overlap.** s1_spec 329, 345 (pinions: pitch point ± face_width / 2), 361, 377 (motors: outer end ± body / 2), 314 (gear: ± pitch_diameter / 2). motor23_a at θ 210, radial span 125 to 201, body 57: true Y band [201·(−0.5) − 28.5·0.866, 125·(−0.5) + 28.5·0.866] = [−125.2, −37.8] (DERIVED); spec band [−129.0, −72.0] (MEASURED, check_stack). The inboard 34.2 mm are missing. Gear outer edge is at pitch radius + face_width / 2 = 140 in `draw_gear_section` (sketch_common.py 118); band ±125 omits 15 mm each side. Fix: check_stack derives the band of a radial part from (r_in, r_out, θ, half-width) as [min(r_in s, r_out s) − w|c|, max(r_in s, r_out s) + w|c|], s = sin θ, c = cos θ, or a lint fails any band that does not contain that projection. K7 B fixture: a pair depth-separated by point bands and overlapping by true projections.

**TP-5 FIX. K7 tests declared pairs only.** sketch_common.py 614-616. s1_spec declares neighbours on 6 of 35 rows (base_frame, base_plate, core_500, ring, frame_upper_a/b). Gear, pinions, motors, bearing, nuts, lift motors and drill rows declare none; the l.146 seed (moving parts against frame members and lift motors, G 10) appears for the ring alone. An overlap between two undeclared parts reads clean. Fix: every pair whose depth bands (side) or z bands (plan) intersect defaults to F; legitimate containment (screw in nut, nut in ring housing, core in drill bore, drill in bearing bore) is declared with a new class N (nested, one outline inside the other); the spec lint requires the l.144-149 seed pairs. B fixture: undeclared overlapping pair.

**TP-6 FIX. A spec row is satisfied by an artist of the wrong kind.** K5 (544-551) compares drawn class with the spec only for cylinder, screw, cone and gear rows with an axis; 18 of 35 s1_spec rows (12 prism, 2 plate, 4 line) get no comparison beyond "no Circle in side view". Probe G: nut_a drawn as a 64-gon circle passes K5, K6, K9. K9 (746) counts Text gids: probe D, guide_member replaced by a text passes K9 and K5 (K6 fires only because that row has a z_rule). Fix: K5 compares `classify(a)` with the row's `projection` for every row that has one (every s1_spec row does); K9 accepts a Text only for kind callout; spec lint requires `axis` in {X, Y, Z} for cylinder, screw, cone and gear rows.

**TP-7 FIX. Only the first Axes of a figure is checked.** sketch_common.py 452, 483, 535, 581, 613, 694, 744; checks_s1.py 25. Probe H: an inset Axes with a Circle tagged drill_tube, an untagged Rectangle and an inverted y axis passes K5 and K8. Detail 1.3 (S3) l.258 puts a plan inset in a sketch. Fix: K3 or K9 fails on a figure with more than one Axes until the spec declares each inset with its own view; then K3 to K9 iterate over the declared Axes.

**TP-8 FIX. Duplicate spec row ids pass silently.** sketch_common.py 532, 609, 691, 741. Probe E: a duplicated anchor_a row with empty sense hides the planted K8-B2 defect (K8 pass, K9 pass). Live s1_spec has no duplicate (MEASURED). Fix: K9 (or the spec loader) fails on a repeated id; B fixture with one duplicate.

**TP-9 FIX (draft spec; may be carried to 1.1 (b)). Sense rows disagree with the pose table and rubric.** (a) s1_spec 188: core_750 `rests_on core_seat` in load and park; gameplan l.213 draws the 0.75 m core "mid-insertion" at load. Drawn per the pose table, K6 and K8 fire; drawn seated, the operator task is not shown. (b) s1_spec 26, rubric "the ring is on the drill above the core in every pose"; the predicate is `ring above core_seat` (287). On the draft seeds at capture_end the ring bottom is 184.84 + 200 = 384.84 z_A and the 0.5 m core top 42.5 + 500 = 542.5 z_A (DERIVED): the rubric line as worded is false at capture_end and no predicate encodes it. The Designer rewords the rubric line or names the predicate at 1.1 (a).

**TP-10 NOTE.** `below` and `above` (711-714) order centroids. The half-space form z_hi(me) ≤ z_lo(other) also rejects overlapping parts. K6 already pins vertical extents and S1-4 checks nut travel with allowances, so the centroid form is adequate for S1.

**TP-11 NOTE.** `pair_state` (358-361) reports C, F or overlap, never G and never a signed gap. K7-B3 reads "state F" on a G pair at 9 mm. Report distance minus g_min, negative on violation, for the M1 reader.

**TP-12 NOTE.** Control figures: `drill.top_block_od` 152.4 equals `drill.tube_od` 152.4 (ASSUMED), so the top-end block reads as a tube segment divided by one line; the V3 cue is the 12.7 mm radial step of the head and the label "cutter OD ASSUMED 177.8". A reviewer can fail B1 from the label alone without reading geometry. `draw_mini(labels=False)` exists (builders.py 103); an unlabelled pair would test geometry reading. Keep key.json out of what the reviewer receives.

**TP-13 NOTE.** The spec `axis` field takes X, Y or Z. Pinions and motors at 210 and 330 deg have radial axes; in a plan view a rotated Polygon for such a part classifies as trapezoid and fires K5, while a rotated Rectangle passes. S2 needs an `axis_theta` or radial axis value.

**TP-14 NOTE.** The side_xz viewing direction is not stated. With +X right and +Z up, the right-handed reading looks along +Y, and the spec depth sign (`sind(θ)`, +Y far) agrees. State it in `setup_figure` or the spec header so near and far, and hidden lines, are read one way.

CROSS-REVIEW FAIL (TP-1; TP-2, TP-3, TP-4, TP-5, TP-6, TP-7, TP-8, TP-9)

## Re-check after revision

Inputs: step1.0_engineer_revision_notes.md; sketch_common.py (`_to_data` 184-194, `artist_polys` 204-232, k3 588, k5 671-703, k7 826-923, `taper_issue` 945-964, k8 967-1050, k9 1055-1078); check_stack.py `place_extents` 180; s1_spec.yaml `place` and `sense` rows. All results MEASURED 2026-11-24, in-process; no harness file written. Probes: scratchpad `topo_probe.py` (Wave 2 probes against revised code) and `topo_probe2.py` (G, H, J, K re-run on the new builders, plus a 180 deg rotation).

Controls K5, K7, K8, K9 from manifest.yaml: 41/41 as expected, each B carrying its manifest reason substrings (K5 Z, B1-B5; K7 Z1-Z7, B1-B10; K8 Z, Z2, B1-B11; K9 Z, B1-B4).

Tip-up probes:
- Reflection `Affine2D().scale(1, -1).translate(0, lo + hi)` on the three drill rows: measured head z [1088.47, 1194.84], equal to the rendered extent (hand value lo + hi - z: [1088.47, 1194.84]). K6 fails, off 843.63; K8 fails, head centroid 1141.7 against gear 471.0 and top block 319.8.
- Rotation `rotate_deg_around(0, mid, 180)`: K6 and K8 fail on the same values.
- Plan y-mirror by transform (C2): K8 fails, azimuths 330, 210, 90 against 30, 150, 270.

| ID | Status | Evidence |
|---|---|---|
| TP-1 | CLOSED | Pieces are now measured through the artist's full transform, `T - transData` (184-194). Tip-up probes above; K8-B8 fires. |
| TP-2 | CLOSED | Predicate `taper` (945-964) is on collet (down), gear (up), pinion_a/b (inward). K8-B10 and K8-B11 fire. Probe K (gear flipped by transform): K8 fails, width at bottom 35.00, at top 50.00. K6 stays clean, so K8 alone carries taper. The collet direction is ASSUMED and goes to the Designer at 1.1 (a). |
| TP-3 | CLOSED | `place` sits on every placed row: drill rows at r 0, pinions, motors, screws, nuts, anchors, guides, lift motors, guide member, frame members, descent stop. K8 asserts x centre = r_c cos θ (989-999). Motor side is now `side` sign and `outboard` (1026-1037). Probe J (motor23_a mirrored by transform): projected_x fails, 141.16 against -141.16, and `side` fails. K8-B7 fires. |
| TP-4 | CLOSED | check_stack `place_extents` derives the band from (r_in, r_out, θ, w); an explicit band is linted against it (k7 831-841). motor23_a band [-125.18, -37.82] against hand [-125.2, -37.8]. Gear ±140 against hand 140. K7-B7 fires on the Wave 2 spec band [-129, -72]. |
| TP-5 | CLOSED | Undeclared drawn pairs default to F (871-885); class N declares nesting; s1_spec `undeclared_pairs: F`. K7-Z7 is clean and K7-B10 fires. On the draft, S1-FULL shows 58 undeclared pairs, mostly nests; declaring them N is 1.1 (b) spec content. |
| TP-6 | CLOSED | k5 compares the drawn class with `projection` on every row (697-699) and requires an axis on round kinds (675-677). k9 accepts a Text only for kind callout (1068). Probe G (nut as 64-gon): K5 fails. Probe D: K9 fails "(a Text carries its gid)". K5-B4, K5-B5 and K9-B3 fire. |
| TP-7 | CLOSED for 1.0 | K3 fails a figure with more than one Axes unless the spec declares `insets` (588). Probe H: K3 fails. Residual: a spec that declares insets suppresses the lint, and K5 to K9 still read `axes[0]` only. Per-Axes iteration is needed when S3 declares its plan inset (detail 1.3 l.258). Carried to S3. |
| TP-8 | CLOSED | `duplicate_ids` in K9 (1059). Probe E: K9 fails "id anchor_a appears on more than one row". K8 alone still passes that probe; K9 is the guard. K9-B4 fires. |
| TP-9 | CLOSED for 1.0 | Predicates accept `poses` (1001), and K8-Z2 is clean. The core_750 load z_rule and the rubric line "ring above the core" are Designer content at 1.1 (a)/(b), with a comment at s1_spec 198. My finding allowed carrying them to 1.1 (b). |
| TP-11 | CLOSED | G failures print "gap - g_min" signed (K7-B3: -1.000). |
| TP-14 | CLOSED | The `setup_figure` docstring states side views are seen from -Y. |
| TP-10, TP-12, TP-13 | NOTE, carried | No change needed at 1.0 (TP-12 to the 1.1 M1 gate, TP-13 to S2). |

New observations (NOTE, no finding raised):
- K6 does not see taper; K8 carries it alone. This is adequate because the taper predicate is in the spec.
- In the draft spec, the motor radial span (125 to 201) overlaps the pinion span (110 to 140). The Engineer already lists this for the Designer (revision notes section 6 item 5).

CROSS-REVIEW PASS (TP-1 to TP-9 closed for Step 1.0; TP-7 inset iteration carried to S3, TP-9 spec content carried to 1.1 (b))
