## Corrections to the brief

1. The inset B controls K8-B53 and K5-B25 "fire" on the pre-change code in the P4 record (22 and 14 issues, reasons mismatched). Read alone, that is no proof the old code was blind to the inset. Probe p1 compares each B with the Z on the save point 3 copy (`docs/sketches/wip/p4_prerun/`, copied to scratchpad). The issue lists are identical: K8 22 = 22, K5 14 = 14, same reason text (MEASURED). The old code does not see an inverted or mis-projected inset. On the P4 code each B adds exactly its planted issues over a clean Z: K8 0 -> 2, K5 0 -> 1 (MEASURED).
2. `orphan_predicates` (the K8 premise check of TP-7, "a predicate is evaluated in at least one Axes") raises NameError on its first hit. Line 4642 formats `t`, which is never assigned. No control plants an orphan, so no run has reached that line. With one orphan (screw_a `below anchor_a`, probe p2), K8 returns `error: NameError` and loses every other K8 issue (MEASURED). See FIX 1.
3. F5's proposed disposition "a plan bore (`section` annulus)" has no effect. `plan_outline` ignores `section` on a placed row. With `section: [nut_body_od / 2 + nut_float, nut_housing_od / 2]` added to nut_housing_c, the inset outline stays `polys`, flagged true, and K7 stays at 14 issues, overlap 113.120 mm2 (probe p7, MEASURED). In S3, `section` also means an axis-Z annulus about the drill axis (spec header l.25), which is the wrong centre for a row at r 160. See F5 below.

Tags: MEASURED (probe run in this session on a scratchpad copy of `docs/sketches/`), DERIVED (hand arithmetic), DECLARED (spec or ruling). Probes: `C:\Users\UR\AppData\Local\Temp\claude\eba575d6463ef2d6\6efaddfb-5e83-4849-8803-49d5d7303110\scratchpad\probes\p1_prechange_inset.py` to `p10_apart.py`. The copies are `scratchpad\live` (P4 code), `scratchpad\livefix` (P4 code with line 4642 given `t = _pred_target(pr)`, used only to see past FIX 1) and `scratchpad\pre` (save point 3). Nothing under `docs/sketches/` was edited.

**Verdict: FIX (7 items).** TP-7 per-Axes iteration is sound and its inset B controls are red-first. FIX 1 is the one TP-7 defect. FIX 2 to 7 are section-rule items.

## 1 Per-Axes iteration (TP-7)

| Item | Finding | Basis |
|---|---|---|
| Every Axes carries its view and id | `setup_figure` tags the main Axes (`sketch_view`, `sketch_axes`). `add_inset` builds the declared inset with its view title, (mm) labels, equal aspect, both grids and the declared extent | code l.90 to 141 |
| K3 to K9 per declared Axes | `per_axes` wraps K3 to K9. Each sub-context gets the declared view, `sub_spec` rows (row `axes`, `projection_by_axes`, neighbours, predicates and label restricted to that Axes), and the stack filtered to its rows (reflected for a section view) | code l.4700 to 4796 |
| Undeclared / absent Axes | K3-B10 (an undeclared third Axes) and K9-B9 (the inset deleted) each fire on their own reason | P4 record |
| Inverted inset (handedness) | Pre-change: B = Z (K8 22 = 22). P4 code: 0 -> 2 (`[inset_plan] axis inverted (x False, y True)` and the `plan_axes axes_not_inverted` issue) | p1, MEASURED |
| Mis-projected inset | Pre-change: B = Z (K5 14 = 14). P4 code: 0 -> 1 (`screw_a: screw axis Z in plan_xy drawn as rectangle, needs circle`) | p1, MEASURED |
| Inset row in the main Axes | Pre-change: K9 20 -> 19. The old code counts screw_a drawn in the wrong Axes as coverage and drops one "no patch" issue. P4 code: 0 -> 1 (`has no spec row in this Axes (declared in inset_plan)`) | p1, MEASURED |
| Inset handedness hand values | Inset centroids: screw_a (-138.56, 80.00), azimuth 150.00; screw_b (138.56, 80.00), 30.00; screw_c (0.00, -160.00), 270.00, counter-clockwise from +X seen from +Z. These match 160 (cos, sin) of 150, 30, 270 (DERIVED) | p3, MEASURED |
| Orphan predicate | Premise check present, crashes, no B | FIX 1 |

TP-7 SIGNED on the iteration, with FIX 1 to close.

## 2 Section handedness

Harness form: `reflect_record` maps a plan record to the section frame by reflection across x = y, so x' = plan y = u and y' = plan x = depth. `axis_parallel` and section azimuth read the reflected theta' = 90 - theta. The side-view machinery behind the reflection uses depth unsigned (K7 band gap, `_depth_separated`). The section convention reads the signed plan x band directly, with front = x > 0. The reflection has determinant -1, so its implied side-view viewer sits at -X. That is harmless because no check reads that viewer side: every signed depth test uses plan x.

Sign check, hand value beside the harness:

| Quantity | Hand (DERIVED) | Harness (MEASURED, p3) |
|---|---|---|
| u x z | (0, 1, 0) x (0, 0, 1) = (1, 0, 0) = +X, toward the viewer (DECLARED section.axes) | display sign of (u right) x (z up) on the section Axes: +1 (Axes not inverted; K8 inversion test per Axes) |
| (u x z) . look | look = -X: (1, 0, 0) . (-1, 0, 0) = -1 | plan look arrows (0, -304) -> (-40, -304) and (0, 304) -> (-40, 304): direction -X |
| screw c | u = 160 sin 270 = -160; depth x = 160 cos 270 = 0, band [-6, 6] | drawn u centroid -160.00, extent [-166.00, -154.00]; depth [-6.00, 6.00] |
| pinion c, NEMA 23 c | u = r sin 90 > 0 | pinion u 120.10, extent [95.22, 140.00]; motor u 180.00, extent [142.00, 218.00] |
| member c | u = 274 sin 270 = -274 | -274.00, extent [-304.00, -244.00] |
| radial axis X at theta 90 in the section | theta' = 0: \|sin 0\| > \|cos 0\| false, so the axis lies in the plane and projects as a trapezoid or rectangle | `axis_parallel` False for pinion_c, motor23_c, motor_shaft_c |

The data frame is right. The gap is between the section and the inset. The harness fixes u = +Y for `section_yz`, so the viewer is at +X. The look direction it compares the cutting-plane arrows against is a free spec value (`look_direction toward`). Probe p3 sets `toward: +X` and draws the arrows toward +X. K3, K5, K6, K8 and K9 stay clean, and K7 is unchanged at its existing 14 (MEASURED). A plan arrow that contradicts the section's own viewer passes. FIX 2.

## 3 Section convention as half-space classes

Implemented (`section_convention_issues`). The depth band is plan x [x0, x1] and pw is profile.width, 60 (DECLARED):

| Class | Rule as coded | Half-space form | Status |
|---|---|---|---|
| omitted, front | drawn row with x0 > 0.05 fails | wholly in x > 0 | sound |
| omitted, past | drawn row with x1 < -pw - 0.05 fails | wholly in x < -pw | sound |
| cut | x0 <= 0.05 and x1 >= -0.05; hatched with its material; unsectioned outlines above its zorder | band straddles x = 0 | sound |
| beyond | x1 <= 0.05; unhatched; dashed exactly when every sample lies inside a drawn cut piece | band in x <= 0, not wholly past -pw. A cut piece at x = 0 lies between the viewer at +X and any x < 0 point, so 2D containment in a cut piece is occlusion | sound |
| unsectioned | no depth test | band must straddle x = 0 (axis in the plane) | **gap**: standoffs_c (band [-18.25, -12.75]) re-classed unsectioned changes no check (p4 (b), MEASURED) |
| rows absent from the section Axes | not classified | a spec area row outside the section Axes must be omitted (front or past) | **gap**: coupling_c moved to `axes: [inset_plan]` changes no K-check through the section and no S3 check (p5, MEASURED; the only K5 change is a fixture artifact in the inset). screw_c moved out of the section is caught only through its section-only predicate, and that path crashes today (p4 (a), Correction 2) |
| figure note names removed parts | not_drawn heads against the spec and drawn note (`figure_note_issues`) | — | sound for named parts |

FIX 3 closes both gaps. The converse is green on the live spec. Every inset-only area row classifies as omitted: screw_a, nut_housing_a, anchor_a, liftmotor_a, frame_upper_a and home_switch_a are past (x1 from -132.56 to -196.31), and the b set is front (x0 from 108.87 to 196.31) (p5, MEASURED).

Unsectioned rows occluding beyond rows are outside the stated convention ("edges behind a cut part dashed"). At capture_end no beyond piece overlaps an unsectioned piece (p4 (c), MEASURED: none). NOTE 6.

## 4 New K8 predicates (points, look_direction, axes_not_inverted)

- `points` +Z / -Z: head minus tail along the direction (dot > 0) and \|cross\| <= 0.1 L. A sign check, sound. S3-1-B2 fires on it.
- `points apart`: two arrows with the heads farther apart than the tails. Two arrows from one tail that both point up, heads 3 mm either side, pass (p10: K8 clean, MEASURED). Tension needs opposite senses on one line. FIX 4.
- `look_direction`: a two-vertex line on x = 0 and every arrow pointing `toward`. Sound as a drawing test. Its `toward` is unanchored to the section view (FIX 2).
- `axes_not_inverted`: the Axes inversion part repeats K8's per-Axes inversion test (both fire in K8-B53). The mark part passes a single diagonal from the origin. NOTE 5.

## 5 K5 mark admission, section form; declared sub-artists

Section form (Correction 5 of P4): M4 reads the convex hull of the parent's pieces, and M5 needs each endpoint on a vertical edge of a parent piece. M5 puts each endpoint on the part boundary, and a point on a piece's edge lies in that piece and so in the hull. M4 is therefore implied by M5 in this form, and the hull's over-admission of the journal gap admits nothing M5 has not already placed on the part. The form is sound. For a one-piece parent it reduces to the signed M4 and M5.

| Mark drawn (anchor_bearing_c:line, z 340.00 z_S) | K5 (p6, MEASURED) |
|---|---|
| fixture: u -173.00 to -147.00 (bearing OD) | clean |
| u -173 to -160 (end in the journal gap, inside the hull) | fires 1, M5 "not on a vertical edge" |
| u -180 to -147 (past the OD) | fires 2, M4 and M5 |
| u -181 to -147 (block outer face) | fires 2, M4 and M5 |
| u -165 to -155 (bore faces only, across the journal) | clean (NOTE 4) |

The parent pieces are u [-173, -165] and [-155, -147], z [332, 340] and [340, 348] (MEASURED); mark.z = anchor_bearing_z 280 z_A + 60 = 340 z_S (DERIVED). The form signs. The case the relaxation opens, an endpoint inside the hull but off every edge, has no B in S3: K5-B26 to B32 all run on the one-piece S1 anchors. On the save point 3 code that planted gap endpoint gives B = Z (K5 14 = 14, MEASURED p8), so it is red-first. FIX 5.

Declared sub-artists: balls (Circle points inside a drawn piece of the row) and lever (one two-vertex Line2D with its ends at lever.from and lever.to) are admitted only when declared and with the parent drawn. Both sign. Lever hand values: from u = -160 - (190 - 160) = -190 = 190 sin 270, and to u = -182 = 182 sin 270 (DERIVED). These hold only because sin 270 = -1 (NOTE 3).

## 6 Radial symmetry in the inset (my 1.2 (c) NOTE 1)

Radial-footprint rows in the inset: anchor_a/_b/_c (42 square, "faces radial and tangential", Design Notes 31), liftmotor_a/_b/_c, frame_upper_a/_b/_c and home_switch_a/_b/_c. TP-13's tangential-edge test applies only to round kinds with axis X or Y. These rows are prisms, held by containment (plan_extent) and centre (K6 plan) only. Probe p9 draws frame_upper_b rotated 15 deg and scaled 0.75 about its centre. K5 to K9 do not change (MEASURED). Ruling: predicate, not an M1 item. FIX 6.

## 7 Findings F2, F3, F5 (spec edits for P6)

| # | Ruling | Basis |
|---|---|---|
| F2 | Confirmed. nut_c and guide_c are section-only cylinders with axis Z. In section_yz their projection is a rectangle. Set `projection: rectangle` (projection is not an X1 field) | s3_live K5 7 issues, "spec projection circle disagrees with rectangle"; s3_fixed (edit applied) K5 clean (MEASURED) |
| F3 | Confirmed. Drop `frame: radial` from motor_shaft_c `outboard of pinion_c`. In the section frame the side form reads (u_shaft - u_pinion) cos theta', with cos theta' = cos(90 - theta) = sin theta = r-hat . u. That is the radial outboard sense wherever the radial direction lies in the plane (theta 90, 270) | hand: (131.50 - 120.10) x cos 0 = +11.40 > 0 (centroids MEASURED, product DERIVED); s3_live K8 1 spec error (MEASURED) |
| F5 | Defect confirmed; disposition corrected (Correction 3). The inset is a plan projection. A screw inside a bored housing nests in projection, and the disk drawn for nut_housing_c is circumscribing: it is flagged true only because a round footprint drawn as a circle is presumed solid. The a and b pairs already carry N "(plan)" in the inset. Ruling: class per Axes, `class_by_axes: {inset_plan: N}` on screw_c\|nut_housing_c and screw_c\|anchor_c (both directions), with F kept on the true section pieces. Premise: the same pair carries C, F or G and is tested in another declared Axes of the figure. This is harness work, so it lands at P5f (FIX 7), and P6 then edits only the spec. Declaring N for the pair in every Axes is refused: it would lift the section F test on true pieces | K7 inset 13 pair-pose fails at 113.120 mm2 on s3_fixed; `section` annulus probe K7 unchanged at 14 (MEASURED) |

## FIX items (P5f, each B shown red on the code before the fix)

1. **orphan_predicates.** Assign `t = _pred_target(pr)` before the append (l.4642). Add K8-B: screw_a carries `{pred: below, of: anchor_a}` (a z predicate on an inset-only row), planted 1, reason "evaluated in no declared Axes". On the P4 code it errors (NameError, MEASURED p2). With the line fixed it fires 1 (p4 (a) on `livefix`: screw_c side predicate, MEASURED).
2. **Section look sign.** For a section view: (u_view x z) . toward = -1, with u_view = +Y for section_yz (VIEW frame) and toward the `look_direction` value of the section line, so toward must be -X. A spec with any other toward is a K8 spec error in the main Axes, reported once. Z: s3_fixed. B: toward +X with the arrows drawn +X, planted 1. That B is clean on the P4 code (p3, MEASURED).
3. **Convention completeness.** (a) An unsectioned row's depth band straddles x = 0 (x0 <= 0.05, x1 >= -0.05). B: standoffs_c classed unsectioned, planted 1; clean on the P4 code (p4 (b), MEASURED). (b) Every spec area row (not reference, not line, arrow or callout) whose `axes` omits the section Axes classifies as omitted against the parent stack's plan x band: front x0 > 0.05 or past x1 < -pw - 0.05. Otherwise it is an issue: "lies in the section band and is not drawn in the section". Z: s3_fixed (12 inset-only rows, all omitted, p5 MEASURED). B: coupling_c with `axes: [inset_plan]` and `projection_by_axes: {inset_plan: circle}`, planted 1; clean on the P4 code through the section Axes (p5, MEASURED).
4. **points apart.** Require opposite senses, d0 . d1 < 0, on one line, \|cross(d0, d1)\| <= DIR_TOL \|d0\| \|d1\|, with the heads farther apart than the tails. Fixture hand value: d0 = (0, -12.92), d1 = (0, +12.92), d0 . d1 = -166.9 < 0, cross 0 (DERIVED from the p10 arrow ends). B: both arrows from a common tail pointing up, heads 3 mm either side of the line, planted 1; clean on the P4 code (p10, MEASURED).
5. **Mark section form B.** Add K5-B (S3): anchor_bearing_c:line drawn u -173 to -160 (one end in the journal gap, inside the hull of the pieces), planted 1, reason "not on a vertical edge of anchor_bearing_c (M5)". It fires 1 on the P4 code and B = Z on the save point 3 code (p6, p8, MEASURED). This is the B that rule (h) requires for the relaxed M4.
6. **Radial symmetry in plan.** Add the K8 predicate `mirror_about_radial` (plan_xy only). In the radial frame at the placed theta (`to_ut`), every vertex (u, t) of each drawn piece has a partner (u, -t) within TOL_Z. Declare it at P6 on the S3 inset rows anchor_a/_b/_c, liftmotor_a/_b/_c, frame_upper_a/_b/_c and home_switch_a/_b/_c. Z: s3_fixed inset (radial_corners footprints, symmetric by construction, DERIVED). B: frame_upper_b rotated 15 deg and scaled 0.75 about its centre, planted 1; clean on the P4 code (p9, MEASURED). The aligned narrower square stays a containment-only case for M1 (my 1.1 NOTE).
7. **Per-Axes neighbour class (F5).** `sub_spec` reads a neighbour's `class_by_axes[aid]` in place of `class`. Premise lint: an override to N is admitted only when the pair, both rows drawn, is tested with its base class C, F or G in another declared Axes of the same figure. Otherwise it is a K7 spec error. Z: s3_fixed with the overrides on screw_c\|nut_housing_c and screw_c\|anchor_c (inset K7: the 13 pair-pose fails cleared). B: an override to N on a pair the section Axes does not draw, planted 1.

## NOTES (to (e) or M1, no revision)

1. Section azimuth fixes theta only up to theta <-> 180 - theta, because u = r sin theta. Rows in the plane (90, 270) are unique. For an off-plane row the sign of the depth band settles it, through the convention test (FIX 3).
2. `axis_parallel` picks the dominant component. An oblique radial axis in a section would be judged as in-plane or normal. Today every axis X row in the section sits at theta 90 (theta' 0, MEASURED p4 (e)). A one-line spec lint (theta in {90, 270} or {0, 180} for an axis X or Y row in a section) would make the oblique case unrepresentable.
3. The lever u expressions encode u = -r, which holds at theta 270 only (`pitch_radius * sind(angle[2]) - (r - pitch_radius)`). `r * sind(jackscrew.angle[2])` gives the same -190.00 and -182.00 (DERIVED) and holds for any theta. The lever's from-end could also be held on a drawn piece of the switch (`_in_any`), as M4 holds a mark.
4. The section form admits a bearing line across the bore faces only (u -165 to -155, p6). The conventional line spans the OD. Tightening: endpoints at the least and greatest u of the parent pieces whose z range contains mark.z. M1 item otherwise.
5. `axes_not_inverted` repeats K8's per-Axes inversion test, and its mark branch passes one diagonal from the origin. K3 checks the inset labels for "(mm)" and not for the view's axis letters.
6. Unsectioned rows (screw, coupling, shafts) drawn whole would occlude beyond rows behind them. The convention dashes only behind cut parts. No overlap exists at capture_end (p4 (c), MEASURED). If S3 r1 adds one, the beyond rule needs an unsectioned occluder.
7. In the section, N is held between two cut rows: gear\|pinion_c (mesh, S1 basis) and pinion_c\|motor23_c. The latter pair is drawn 2.00 apart (pinion hub end u 140.00, motor face 142.00, MEASURED p3), so N relieves nothing there. Declaring C or G removes a blanket pass. TP1.1-3 refuses N only between two `section` rows. Extending it to two cut rows in a section view is for (e).

S3-1 sign (section 6 of P4, my row) signs. Bearing line 340.00 z_S below the nut bottom 365.84 at capture_end, tension segment 25.84 (MEASURED by P4, DERIVED 365.84 - 340.00). The cut arrow points +Z. The cut-case faces run one way along the chain: nut flange down on the housing shoulder, locknut up under the lower inner race at 272, upper outer race up against the cover at 288 (DECLARED neighbour faces).

## Gameplan lines to change

Apply after P4's items 22 and 24 (`step1.3_engineer_redfirst.md` section 7).

1. l.295 (TP-7 carried). Old: `signatures at P5T (Topologist), P5L (Loftsman), P5 (Software Engineer).` New: `signatures at P5T (Topologist), P5L (Loftsman), P5 (Software Engineer). P5T (step1.3_topologist_redfirst_signoff.md): per-Axes iteration signed (K8-B53, K5-B25 blind on the pre-P4 code, B = Z MEASURED); FIX 1 to 7 (orphan_predicates B, section look sign, unsectioned straddle and omitted-row converse, points apart senses, mark section-form B, mirror_about_radial in plan, neighbour class_by_axes) to P5f.`
2. l.607 (Design Notes 20 TP-7 row). Old: `Topologist signature at P5T pending` New: `Topologist P5T: iteration signed, section rules FIX 1 to 7 to P5f (step1.3_topologist_redfirst_signoff.md)`
