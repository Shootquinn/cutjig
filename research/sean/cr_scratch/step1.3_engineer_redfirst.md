## Corrections to the brief

1. **S3-2-B1 cannot be red on the pre-change code.** S3-2's threshold logic was written at (b) (P2, `checks_s3.py`), and P4 changed only its Axes reader. On the save point 3 code the B fires with its planted reason and count (MEASURED). The red-first evidence for this B comes from branch deletion instead: with `if m < sf` disabled, S3-2-B1 reads clean, a mismatch (MEASURED).
2. **The signed spec has three defects that block a clean K5 or K8 on any faithful drawing.** No check is relaxed for them. They are listed as findings F2 and F3 for P6. The Z fixtures draw the signed spec with those three edits applied (`s3_fixtures.p4_spec_findings`). `s3_live` draws the signed spec unedited, and K3, K6 and K9 read clean on it.
   - `nut_c` and `guide_c` are drawn in the section only, but carry `projection: circle`. In the section their projection is a rectangle, so K5 reads 7 issues.
   - `motor_shaft_c` declares outboard with `frame: radial`. That is a plan form (TP1.2-1), and K8 rules it a spec error in the section.
3. **The S3-3 B "anchor frame member 1 mm clear of the base plate" needs a rule the brief does not state.** Every chain c link that S3 certifies also has an S1 or S2 certifier. A defect drawn only in the section therefore stays masked unless a failing S3 test vetoes the link. The rule written here: an S3 certifier that tests the pair and reads it open opens the link.
   - Under that rule the signed spec's own `S3 base_plate|receiver` certifier vetoes link receiver|base_plate. The section draws the receiver spigot 0.20 clear of the plate hole and no seat face (finding F1, MEASURED 0.200 mm).
   - The S3-3 fixtures drop that one certifier. The S1 record certifies the link.
4. **The SYM lint as worded ("equal in keys") is red on the live specs on key lists, apart from the anchor exemptions.**
   - S3 c rows carry section-detail keys that the inset a, b rows do not. `screw_c` has 8 keys `screw_a` lacks, `anchor_c` 5, `nut_housing_c` 8.
   - S1 `screw_a` lists `jackscrew.length` and `screw_b` does not.
   - The rule is implemented as worded. Clearing it at P6 is a spec edit of key lists (finding F4), or the raiser rules a subset.
5. **K5 mark admission in the section.** P0T M5 admits side views only and asks for a section form at (b)/(c). The form written here: M4 reads the convex hull of the parent's drawn pieces, and M5 needs each endpoint on a vertical edge of any parent piece.
   - For a one-piece parent (the S1 anchors) this is the signed M4 and M5.
   - `anchor_bearing_c` draws as four pieces, so the bearing line crosses the journal gap. The Topologist signs this form at P5T.

Tags: MEASURED (read from a run in this session), DERIVED (arithmetic on those), DECLARED (spec or ruling).

## 1 Rules

Every new B in the table was run on the save point 3 code first. That code is a copy of `docs/sketches/` taken before the first P4 edit, at `docs/sketches/wip/p4_prerun/` (git-ignored, kept for P5), with `fixtures/s3_fixtures.py` and a manifest of the 51 new controls added (`new_manifest.yaml`). Result: 36 of 37 B controls red (a mismatch), MEASURED.

- Section B controls and the S3-3 B controls fire on the old code for other reasons (fail-closed skeleton, other issues). That counts as red: reason substrings and counts mismatch.
- SYM controls error on the old code: there is no `sym_lint` there.
- S3-2-B1 is the one exception (Correction 1).

| Rule | Premise | Premise check | Z | B (red on pre-change code: observed there) |
|---|---|---|---|---|
| TP-7 per-Axes views: setup_figure gives every Axes `sketch_view` and `sketch_axes`; `add_inset` builds a declared inset with its view, title, labels, grids and extent. K3 to K9 run once per declared Axes (`per_axes`): the Axes' view, its rows (`sub_spec`: the row's `axes`, `projection_by_axes`, neighbours and predicates restricted to that Axes, label in the home Axes) and its stack. Results merge with an `[axes id]` prefix. S1 and S2 (one Axes, no insets) are evaluated as before | Every Axes of the figure is a declared Axes; every declared Axes is present; a predicate is evaluated in at least one Axes | `undeclared_axes_issues` (K3); declared-Axes-absent (K3, K9); `orphan_predicates` (K8, main Axes) | K3-Z4, K6-Z5, K9-Z4 (`s3_live`); K5-Z4, K8-Z14 (`s3_fixed`) | K8-B53 inset y inverted (clean on the inset Axes: 22 other issues, planted 2 absent); K5-B25 screw_a square in the inset (14 other issues); K9-B8 screw_a in the section Axes (19 other issues); K9-B9 inset Axes removed (20 other issues); K3-B10 undeclared third Axes (clean) |
| Section view `section_yz` (O4): plane x = 0 seen from +X, u = +Y. The section Axes is evaluated as the side view of the plan reflected across x = y (`reflect_stack`). x' = u = plan y gives the projected centre r_c sin theta; y' = plan x gives the depth bands. Reflected footprints (theta' = 90 - theta, rot' = -rot) give K7 plan relief. K5 judges a radial axis X at its placed theta against the normal X (`axis_parallel`). A section azimuth predicate reads the drawn u centre, r_c sin(azimuth) | u equals plan y with no sign change (spec handedness line) | K8 projected_x and section azimuth; K8 `side` on screw_c, frame_upper_c, motor23_c, pinion_c | K6-Z5, K8-Z14 | K8-B54 section mirrored: 129 issues (old code: 30 issues, reasons absent); K8-B55 screw_c at u = r cos theta = 0: 8 issues (old: 23, reasons absent) |
| section_u true pieces: a row with `section_u` is drawn as exactly those pieces. This replaces the TP-3 centre test for that row (the true section need not be centred on its footprint, e.g. `nut_screws_c` inboard screw at u -144); projected_extent stays | Drawn pieces = spec pieces, each within TOL_Z | `section_u_issues` (K8) | K8-Z14 | K8-B63 ring outboard piece 5 short: 2 issues (old: 22 other issues) |
| Renderer section convention (`render_section` draws; `section_convention_issues` checks, K8, section views) | — | (1) every cut row is hatched with its material pattern (HATCH by spec `hatch`), and the plane cuts it (depth band reaches x = 0); (2) an unsectioned row is unhatched, outline above the cut hatch (zorder); (3) a beyond row is unhatched: dashed when wholly behind drawn cut pieces, solid when visible, split when partly behind, depth within 0 >= x >= -profile.width; (4) no drawn row lies in front of the plane (x > 0) or past one profile width; such rows are omitted and named in the figure note; (5) every area row carries a section_class | K8-Z14 | K8-B56 ring unhatched; B57 brass nut hatched as steel; B58 screw hatched; B59 coupling under the hatch; B60 standoff behind the anchor block drawn solid; B61 visible standoff dashed; B62 screw b set (x +138.6) drawn: each 1 issue (old: 22 other issues each) |
| Arrows and plan marks (spec predicates `points`, `look_direction`, `axes_not_inverted`). `points`: FancyArrowPatch arrows along the stated direction (DIR_TOL 0.1), or `apart` (two arrows, heads farther apart than tails). `look_direction`: a cutting-plane line on x = 0 and every look arrow toward -X. `axes_not_inverted`: the Axes not inverted and the axis marks from the origin toward +X, +Y. K6 reads an arrow tail to head. Look arrows are left out of a line row's plan centre and plan extent (`geom_pieces`) | The arrow's direction is its posA to posB (`arrow_ends`) | K8 per predicate; S3-1 reads `points` on load_cut | K8-Z14, S3-1-Z | S3-1-B2 cut arrow pointing down: 1 issue (old: clean); K8-B53 carries the axes_not_inverted issue |
| K4 label value (spec `expr`, `value_from`, fmt `s`): the label prints the expression's value, the spec value at the path, or the key's string value; a list key or a block prints in the text | — | K4 | K4-Z5 span_lt prints 870 | K4-B20 span_lt prints 1150 (key) where expr is 870 (old: clean) |
| K5 mark admission `<row>:line` (Topologist P0T section 4, signed in advance), with the section form (Correction 5); K9 admits `:line` with its parent drawn | A mark is ink on its part | M1 declared; M2 parent an area drawn at the pose; M3 one two-vertex Line2D; M4 endpoints in the parent's hull (half-space on every edge); M5 horizontal, at mark.z, endpoints on vertical edges | K5-Z5, K9-Z5 (S1, both marks); K5-Z4 (S3 bearing line) | K5-B26 (B-m1), B27 (B-m2), B28 (B-m3a), B29 (B-m3b), B30 (B-m4, planted 2: M4 and M5), B31 (B-m5a), B32 (B-m5b, planted 2: direction and place): each clean on the old code (K5 skipped `:line`) |
| Declared sub-artists (spec `sub_artists`: balls, lever). K5 admits `<row>:balls` (Circles, every point inside a drawn piece of the row) and `<row>:lever` (one two-vertex Line2D whose ends equal `lever.from` and `lever.to`), only when declared and with the parent drawn; K9 admits the same | Ink on its part, fixed by the spec | K5 `sub_artist_issues` | K5-Z4 | K5-B33 balls on guide_c (undeclared); B34 ball 10 outboard; B35 lever end 5 low: each 1 issue (old: 14 other issues) |
| SYM screw-set symmetry (Loftsman (b) sign-off): in every spec, the anchor, anchor_locknut, screw, nut and nut_housing rows of a and b equal the c row (or each other where the spec has no c row) in z_rule, place and keys, with the angle index swapped. Each theta names its own index (a 1, b 0, c 2). No x1_exempt on those rows. Run with every run of a spec that has `chains`; S3-3 certifies a, b screw-set links only when SYM passes | Premise of the a, b links certified from c | `check_sketch.sym_lint` | SYM-Z (post-P6 specs: 18 pairs) | SYM-B1 exempt anchor_b; B2 screw_a at index 0; B3 nut_housing_b z_max + 1 (old: error, no lint) |
| x1_exempt narrowed to `place` (z_rule and plan_poly still compared on an exempt row); --accept refuses while any spec in docs/ carries x1_exempt | An exemption covers the 42-square place only, until P6 | X1; accept | X1-Z (existing) | X1-B3 exempt anchor_c z_max + 1 (old: clean); H1-B9 accept with the live s3_spec in docs/ (old: accepted) |
| S3-1 (sign): the drawn bearing line `anchor_bearing_c:line` lies below the nut bottom at every S1 pose, and the cut arrow points +Z | The bearing line is held to mark.z and the part by K5 M1 to M5 | K5 | S3-1-Z: least 25.84 mm (MEASURED) | S3-1-B1 line at guide_bearing_z: 4 issues (old: clean); S3-1-B2 |
| S3-2 (buckling, Design Notes 31 form): drawn bearing-row centres span L_t = expression within 0.05; P_cr / F >= SF 3 per case; reader moved to the section Axes | — | — | S3-2-Z: P_cr 1363.8 N, least 3.97 stall_up; S3-2-Z2: 100 mm, least 300.79 (MEASURED) | S3-2-B1 T8 root 6.2 on 850: retract 2.26, stall 1.18 (Correction 1: deletion test red) |
| S3-3 (cross-record loop). Each link passes on any certifier: S1 or S2 (latest accepted unsuperseded record, not stale, K7 entry of the pair at the figure pose in a C state); S3 (this run's section K7, C state, and the neighbour face z when named: both drawn pieces have a horizontal edge at that z overlapping in u); "declared" (listed). A failing S3 test vetoes the link. "none" a, b links pass by symmetry from c when SYM passes and every c link between the counterparts passes | A stale record certifies nothing; symmetry certifies only under SYM | stale_diffs inside S3-3; SYM | S3-3-Z: 51 links closed (MEASURED) | S3-3-B1 member c 1 mm clear of its foot: 1 issue; B2 receiver|holder absent from the S1 record: 3 (chains a, b, c); B3 S1 record stale (lead recorded 8): 14 (old: each the skeleton reason, mismatched) |

## 2 S3-x fixture table

Fixtures in `docs/sketches/fixtures/s3_fixtures.py`. `s3_ctx` draws every row of `s3_spec.yaml` from check_stack values:
- Section Axes: section_u pieces as drawn; axis-Z section rows mirrored about u = 0; other placed rows over their plan y extent; plan_poly rows over each piece's y extent.
- Bearing line by the mark rule; balls in each bearing piece; the lever.
- The plan inset drawn by the S2 fixture's plan drawer, plus look arrows on section_line.
- `render_section` on the section and `render_plan` on the inset.

`_s3_3_ctx` adds a temporary records directory holding the S1 r7 and S2 r5 records with `keys_read` refreshed to the live values. These stand for S1 r8 and S2 r9 with the same K7 entries. It also adds the three specs in the post-P6 symmetry state for SYM. All values in the table are MEASURED.

| Control | Fixture | Planted | Expected / observed |
|---|---|---|---|
| S3-1-Z | `s3_fixed` | — | clean; least tension segment 25.84 mm (nut bottom 365.84 at capture_end against the line 340.00 z_S) |
| S3-1-B1 | `s3_1_b1` | bearing line at guide_bearing_z (1210.00 z_S) | fires 4 (load, start, capture_end, park) |
| S3-1-B2 | `s3_1_b2` | cut arrow reversed | fires 1 |
| S3-2-Z | `s3_fixed` | — | clean; P_cr 1363.8 N, least margin 3.97 stall_up |
| S3-2-Z2 | `s3_2_z2` | guide bearing 100 above the anchor bearing | clean; P_cr 103223.7 N |
| S3-2-B1 | `s3_2_b1` | root 6.2, span 850 | fires 2: retract_bind 2.26, stall_up 1.18 against SF 3 (P_cr 404.4 N) |
| S3-3-Z | `s3_3_z` | — | clean: 51 links. Declared: drill_head\|core_750, bearing\|drill_tube (c only), drill_tube\|drill_head, per chain. By symmetry: anchor\|screw, screw\|nut, nut\|nut_housing, nut_housing\|ring for a and b |
| S3-3-B1 | `s3_3_b1` | frame_upper_c drawn 1 mm up | fires 1: base_frame\|frame_upper_c, S3 state F |
| S3-3-B2 | `s3_3_b2` | receiver\|holder entries deleted from the S1 record | fires 3 (chains c, a, b) |
| S3-3-B3 | `s3_3_b3` | S1 keys_read jackscrew.lead 8 | fires 14 (every link certified by S1 alone) |
| S3-FULL | `s3_full_draw` | — | runs: no check errors, none absent |

## 3 --controls counts and time

`check_sketch.py --controls` at the default jobs (12), run of record, MEASURED: **336/336 match**: Z clean 88/88, B fired 245/245, smoke 3/3, **148.4 s wall**. P0 target: 200 s. Before P4: 285/285 at 126 s. Results: `docs/sketches/wip/fixtures/controls_results.json`.

Added at P4: 51 controls (Z 13, B 37, smoke 1).
- K3: Z4, B10.
- K4: Z5, B20.
- K5: Z4, Z5, B25 to B35.
- K6: Z5.
- K8: Z14, B53 to B63.
- K9: Z4, Z5, B8, B9.
- S3-1: Z, B1, B2.
- S3-2: Z, Z2, B1.
- S3-3: Z, B1 to B3.
- SYM: Z, B1 to B3.
- X1: B3.
- H1: B9.
- S3-FULL.

Red-first record on the save point 3 code: `docs/sketches/wip/p4_prerun/controls_results_prechange.json` and `prechange_run.log`. Z 5/13 clean, B 1/37 fired (S3-2-B1, Correction 1), smoke 0/1. Every other B mismatches there. S3-2-B1 reads clean with its margin branch deleted.

Regression on the new library (MEASURED):
- `check_sketch.py s1 --rev 7`: 18/19. K5 red 8 issues: the TP1.1-9 zero-area anchor line, known since step 0 and resolved by S1 r8 at P6. The record is identical in result, reason and count to the run made before any P4 run.
- `check_sketch.py s2 --rev 8`: 18/18. It differs from the P1Rf2 record only in the K2 and X1 reason text, from the P2 overlay and the S3 spec.
- PNGs drawn by `s1_side_poses.py --rev 7` and `s2_plan.py --rev 8` with the new library are pixel-equal to the same scripts on the save point 3 code at the live overlay (4/4 S1, 1/1 S2). The wip/ r7 and r8 PNGs are restored to their pre-session pixels.
- `--stale`: 2 records, the same 5 differences. X1 pass, 70 rows; the exemptions are listed as `place`.

## 4 Stub run table against expectations

`check_sketch.py s3 --rev 0` on `stubs/s3_stub.py` (setup_figure with the declared inset; floor line only), `docs/sketches/wip/s3_checks_r0.json`. `--baseline s3`: run 2 matched **15/15**, written to `wip/baseline_red.json`. All values MEASURED.

| Check | Expected | Observed (cause, issues) | Match |
|---|---|---|---|
| K1 | green, guard | green | yes |
| K2 | green, guard | green (409 keys, 20 expr leaves agree) | yes |
| K3 | green, guard | green, both Axes | yes |
| K4 | red | red, content, 23 (no label annotations) | yes |
| K5 | green, guard | green, both Axes | yes |
| K6 | red, absent | red, absent, 69 | yes |
| K7 | red, absent | red, absent, 326 | yes |
| K8 | red, content (F3) | red, content, 112: 1 spec error (motor_shaft_c frame radial, finding F3), 111 untestable | yes (STUB_CAUSE entry written for F3) |
| K9 | red | red, content, 71 (rows without patches) | yes |
| S3-1 | red, absent | red, absent (load_cut not drawn) | yes |
| S3-2 | red, absent | red, absent (anchor_bearing_c not drawn) | yes |
| S3-3 | red, absent | red, absent (anchor_c not drawn) | yes |
| X1 | green, guard | green | yes |
| SYM | red, content | red, content, 10 (3 S3 anchor exemptions; 7 key-list differences, finding F4) | yes |
| RPT | red, absent | red, absent: tension_segment needs the drawn bearing line; the other 9 items carry values | yes |

No S3 check is green on the stub. Each S3 check's content evidence is its B fixture in run 1. On the live tree S3-3 is also red on content once drawn: S1 r7 and S2 r5 are stale (5 differences), and SYM fails. It certifies after S1 r8 and S2 r9 are accepted with the 42-square anchors.

## 5 Code changes

`docs/sketches/sketch_common.py`:
- Views:
  - `section_yz` added to SIDE_VIEWS, VIEW_NORMAL (X) and VIEW_LABELS; SECTION_VIEWS.
  - `setup_figure(view, title, insets=None)` tags each Axes (`sketch_view`, `sketch_axes`).
  - New: `main_axes_id`, `add_inset`, INSET_RECT.
- Per-Axes block:
  - `AxesFig`, `real_figure`, `declared_axes`, `row_axes`, `needs_split`, `axes_of_figure`.
  - `sub_spec` with `_pred_in_axes`, Z_PREDS, PLAN_PREDS; `orphan_predicates`.
  - `filter_stack`, `reflect_record`, `reflect_stack`, `axes_contexts`, `axes_context`, `undeclared_axes_issues`, `_merge`, `per_axes`.
  - CHECKS K3 to K9 wrapped; `.unsplit` keeps the single-Axes function.
- K3: an inset skips the figure size and dpi test; the text clip test runs once, on the real figure.
- K4: label values (`_spec_path`, `label_value`; `label_text(..., spec)` at both placer call sites).
- K5:
  - `axis_parallel`, `expected_projection_par` (section views).
  - Circle-in-side-view lint also for normal X.
  - Sub-artist branch: `sub_artist_issues`, `mark_issues` (M1 to M5) and helpers `_hull_contains`, `_on_vertical_edge`, `_z_S_expr`, `_in_any`.
- K6: arrows read tail to head; plan centres via `geom_pieces`.
- K8:
  - Orphan predicates.
  - `section_u_issues`, `section_u_pieces`; the TP-3 centre test is replaced for section_u rows.
  - Section azimuth.
  - `points_issues`, `look_direction_issues`, `axes_arrows_issues`; PRED_TARGET gains look_direction, axes_not_inverted, points.
  - `section_convention_issues`; plan_extent via `geom_pieces`.
- K9: admits `:line` and declared sub-artists with the parent drawn; a stray row names the Axes that declares it.
- `render_section`, HATCH, SECTION_CLASSES, `arrow_ends`, `geom_pieces`; `classify` reads a FancyArrowPatch as a line.

`docs/sketches/check_sketch.py`:
- `x1_lint`: the exemption covers `place` only (X1_EXEMPT_FIELD).
- New: `x1_exemptions`, `specs_in`.
- SYM: `sym_lint`, SYM_FAMILIES, SYM_INDEX, `_sym_norm`.
- `run_sketch`: sets `ctx.records_dir` and `ctx.wip_dir` from `--docs-dir` / `--wip-dir`; appends SYM for a spec with `chains`.
- K_SOURCES gains SYM.
- `accept`: refuses while any spec in docs/ carries x1_exempt.

`docs/sketches/checks_s3.py`:
- Readers in the section Axes (`_section`, `_ax`); `anchor_line_z` reads the mark.
- S3-1 adds the cut-arrow `points` test.
- S3-3 written: `_records`, `_k7_tests`, `_pair_ok`, `_face_of`, `_face_issue`, veto, declared, symmetry.
- STUB_EXPECT gains SYM; STUB_CAUSE K8 (F3) and SYM.

New files:
- `docs/sketches/stubs/s3_stub.py`.
- `docs/sketches/fixtures/s3_fixtures.py`: S3 faithful draw, 51 control builders, `p4_spec_findings`, a pre-P4 figure fallback for red-first runs.
- `docs/sketches/fixtures/manifest.yaml`: 51 entries.

`check_stack.py`, the specs and the overlay are unchanged. Run outputs:
- `wip/s3_checks_r0.json`, `wip/s3_summary_r0.md`, `wip/baseline_red.json`.
- `wip/s1_checks_r7.json`, `wip/s2_checks_r8.json`.
- `wip/fixtures/controls_results.json`.
- `wip/p4_prerun/` (pre-change copy with the red-first record).

## 6 Rules awaiting signature and by whom

| Rule | Signs |
|---|---|
| TP-7 per-Axes views (setup_figure / add_inset, per_axes, sub_spec, undeclared and absent Axes, orphan predicates) | The Topologist (P5T; verifies at (e)); The Software Engineer (P5) |
| Section view section_yz by reflection; K5 axis_parallel; section azimuth; section_u premise | The Topologist (P5T: handedness, half-space sense); The Loftsman (P5L: plane coordinates, depth bands) |
| Renderer section convention (items 1 to 5) | The Topologist and The Designer (renderer co-owners; Designer at (f) on pixels); The Loftsman (depth limits) |
| Arrow and plan-mark predicates (points, look_direction, axes_not_inverted), arrow K6 extent, geom_pieces | The Topologist (P5T) |
| K4 label value rule (expr, value_from, fmt s) | The Designer (label conventions co-owner); The Software Engineer (P5) |
| K5 mark admission section form (Correction 5); declared sub-artists balls, lever | The Topologist (P0T raiser; P5T) |
| SYM; x1_exempt narrowed; --accept refusal | The Loftsman (raiser; P5L) |
| S3-1, S3-2 readers; S3-3 cross-record reader, veto rule (Correction 3), symmetry certification | The Loftsman (P5L: S3-3, cross-record); The Topologist (P5T: S3-1 sign, chain order); The Software Engineer (P5: fixtures) |

Findings for P6 (signed-spec edits; none applied to `s3_spec.yaml` here):

| # | Finding | Basis (MEASURED) | Proposed disposition |
|---|---|---|---|
| F1 | receiver\|base_plate open in the section. The receiver spigot is drawn 0.20 clear of the plate hole (spigot_od 160 in spigot_hole_dia 160.4), with no seat face drawn on the plate top. The spec's own S3 certifier vetoes the link | K7 section 0.200 mm, state F | Draw the receiver seat on the plate top (a section piece bearing on z_A 12), or remove the S3 certifier from that link. Raiser: the Loftsman |
| F2 | nut_c and guide_c `projection: circle` on section-only rows | K5 7 issues on `s3_live` | projection rectangle (or projection_by_axes) |
| F3 | motor_shaft_c outboard `frame: radial` in a section | K8 spec error | Drop `frame` (the side form in the section frame holds: theta' 0) |
| F4 | SYM key lists: S3 c rows carry section keys the a, b rows lack; S1 screw_a lists jackscrew.length and screw_b does not | SYM 10 issues live (3 are the exemptions) | Copy the c key lists onto a, b in S3 and add the key to S1 screw_b at P6, or the Loftsman rules a subset |
| F5 | Inset K7: screw_c inside nut_housing_c and through anchor_c is declared F, but the plan outlines are full disks and squares, so they overlap (113.12 mm2) | 13 inset pair-pose tests on `s3_live` | Declare N in the inset, or give the housing and block a plan bore (`section` annulus) |

## 7 Gameplan lines to change

Old and new text are exact fragments of the named line, each unique in it.

1. l.137 (K3). Old: `K3-Z3 live S1 with the tight premise |` New: `K3-Z3 live S1 with the tight premise; K3-Z4 live S3 (section Axes and plan inset, each with its view; TP-7) |`
2. l.137 (K3). Old: `K3-B9 one savefig without bbox_inches="tight" |` New: `K3-B9 one savefig without bbox_inches="tight"; K3-B10 a third Axes with no declared id in the S3 figure (TP-7, 1.3 P4) |`
3. l.137 (K3). Old: `read from the script; 1.2 (h), Designer M1 S1 r5 F1) |` New: `read from the script; 1.2 (h), Designer M1 S1 r5 F1); 1.3 P4 (TP-7): every Axes carries its view and Axes id (setup_figure, add_inset); K3 to K9 run once per declared Axes (main Axes and spec insets) with that Axes' view, rows (row field axes; projection_by_axes; neighbours, predicates and the label restricted to the Axes) and stack, results prefixed by the Axes id; an undeclared Axes fails K3, a declared Axes absent from a figure fails K3 and K9, a predicate evaluated in no Axes is a K8 spec error; S1 and S2 (one Axes) unchanged; figure size and dpi judged with the main Axes |`
4. l.138 (K4). Old: `K4-Z4 live S1 drawn by s1_side_poses.py |` New: `K4-Z4 live S1 drawn by s1_side_poses.py; K4-Z5 S3 span_lt label prints its expr value 870 |`
5. l.138 (K4). Old: `K4-B7, B8, B10 to B12, B14 counts re-read at P1R to P1Rf2 |` New: `K4-B7, B8, B10 to B12, B14 counts re-read at P1R to P1Rf2; K4-B20 span_lt label prints its key value 1150 where the spec names expr (1.3 P4: a label prints label.expr, a label.value_from spec value, or for fmt s the key's string value) |`
6. l.139 (K5). Old: `K5-Z3 live S2 |` New: `K5-Z3 live S2; K5-Z4 S3 per Axes (section: radial axis X at its placed theta against the normal X; inset circles; bearing line, balls, lever admitted); K5-Z5 S1 with both anchor marks |`
7. l.139 (K5). Old: `(Topologist P0T re-check FIX 1r; Software Engineer P0S re-check FIX R1) |` New: `(Topologist P0T re-check FIX 1r; Software Engineer P0S re-check FIX R1); 1.3 P4: K5-B25 screw_a square in the S3 plan inset (TP-7); mark admission <row>:line (Topologist P0T section 4: M1 declared, M2 parent area drawn, M3 one two-vertex Line2D, M4 endpoints in the parent's hull, M5 horizontal at mark.z with endpoints on vertical edges; section form reads the hull of the parent's pieces): K5-B26 to B32 (B-m1, m2, m3a, m3b, m4, m5a, m5b); declared sub-artists (spec sub_artists: balls inside the row's drawn pieces, lever ends at lever.from and lever.to): K5-B33 undeclared balls, B34 ball outside, B35 lever end 5 low |`
8. l.140 (K6). Old: `Fixture drawn from the same params; K6-Z4 live S2 |` New: `Fixture drawn from the same params; K6-Z4 live S2; K6-Z5 live S3 (section frame: u = plan y, z extents, arrows tail to head; inset plan centres; 1.3 P4) |`
9. l.141 (K7). Old: `record lint k7_record_issues, K7-Z16, Z17, B32, signed at re-check r2) |` New: `record lint k7_record_issues, K7-Z16, Z17, B32, signed at re-check r2); 1.3 P4 section_yz: the section is judged as the side view of the plan reflected across x = y (depth bands along plan x, reflected footprints for plan relief); a per-Axes result carries tests_axes beside tests |`
10. l.142 (K8). Old: `K8-Z4, K8-Z5 live S1; K8-Z6 live S2 |` New: `K8-Z4, K8-Z5 live S1; K8-Z6 live S2; K8-Z14 S3 per Axes with the section convention |`
11. l.142 (K8). Old: `under the opaque-fill clause and cover (5); B22 re-rendered |` New: `under the opaque-fill clause and cover (5); B22 re-rendered; 1.3 P4: K8-B53 S3 inset y inverted (TP-7); B54 section mirrored; B55 screw_c at u = r cos theta; section_u premise (a section_u row is drawn as exactly its spec pieces; replaces the TP-3 centre test for that row) B63; renderer section convention (render_section; cut hatched by material, unsectioned unhatched above the hatch, beyond solid / dashed behind cut parts / split, no row in front of the plane or past one profile width, section_class on every area row) B56 to B62; section azimuth (u centre = r_c sin azimuth); predicates points, look_direction, axes_not_inverted |`
12. l.143 (K9). Old: `K9-Z3 live S2 (one plan figure; texts with gid note: are not rows) |` New: `K9-Z3 live S2 (one plan figure; texts with gid note: are not rows); K9-Z4 live S3 per Axes; K9-Z5 S1 with anchor marks |`
13. l.143 (K9). Old: `K9-B7 outline under a row the spec does not have |` New: `K9-B7 outline under a row the spec does not have; K9-B8 S3 inset row drawn in the section Axes; K9-B9 declared inset absent (TP-7); 1.3 P4: <row>:line and declared sub-artists admitted with the parent drawn |`
14. l.144 (X1). Old: `` `x1_exempt: {reason}` passes a declared difference `` New: `` `x1_exempt: {reason}` skips the place field only (1.3 P4, Loftsman (b) sign-off; --accept refuses while any spec carries x1_exempt, H1-B9) ``
15. l.144 (X1). Old: `B1 s2 frame_upper_b r_in + 1; B2 s2 nut_a z_max changed |` New: `B1 s2 frame_upper_b r_in + 1; B2 s2 nut_a z_max changed; B3 exempt s3 anchor_c z_max + 1 |`
16. Insertion after l.144 (the X1 row; new row): `| SYM | Screw-set symmetry (1.3 P4, Loftsman 1.3 (b) R1 and (b) sign-off; premise of S3-3's a, b links): in every spec the anchor, anchor_locknut, screw, nut and nut_housing rows of a and b equal the c row (or each other) in z_rule, place and keys with the angle index swapped, each theta names its own index (a 1, b 0, c 2), no x1_exempt on those rows; runs with every run of a spec that has chains | SYM-Z the three specs in the post-P6 state (18 pairs) | B1 x1_exempt on s3 anchor_b; B2 s2 screw_a at angle[0]; B3 s2 nut_housing_b z_max + 1 |`
17. l.146 (K table pointer). Old: `(285 controls: Z 75, B 208, smoke 2, all match; 121.9 s at --jobs 12).` New: `(285 controls: Z 75, B 208, smoke 2, all match; 121.9 s at --jobs 12). Step 1.3 (c) P4 (research/sean/cr_scratch/step1.3_engineer_redfirst.md) added K3-Z4, K3-B10, K4-Z5, K4-B20, K5-Z4, K5-Z5, K5-B25 to B35, K6-Z5, K8-Z14, K8-B53 to B63, K9-Z4, K9-Z5, K9-B8, K9-B9, S3-1-Z, S3-1-B1, S3-1-B2, S3-2-Z, S3-2-Z2, S3-2-B1, S3-3-Z, S3-3-B1 to B3, SYM-Z, SYM-B1 to B3, X1-B3, H1-B9 and the smoke control S3-FULL (fixtures/s3_fixtures.py; 336 controls: Z 88, B 245, smoke 3, all match; 148.4 s at --jobs 12).`
18. l.286 (S3-1). Old: `| Anchor moved to the top guide (screw hung from the top) | [DN23] |` New: `| Anchor moved to the top guide (screw hung from the top); cut arrow drawn -Z (1.3 P4: reads the drawn bearing line anchor_bearing_c:line, held by K5 M1 to M5, and the cut arrow by K8 points) | [DN23] |`
19. l.287 (S3-2). Old: `| 1000 N compression on an 850 mm T8, which [DN23] states would buckle |` New: `| 1000 N compression on an 850 mm T8, which [DN23] states would buckle (1.3 P4 form: T8 root 6.2 on an 850 span under the Design Notes 31 cases, retract 2.26 and stall 1.18 against SF 3) |`
20. l.288 (S3-3). Old: `| Anchor frame member drawn 1 mm clear of the base plate (loop open) |` New: `| Anchor frame member drawn 1 mm clear of the base plate (loop open; 1.3 P4: member c 1 mm clear of its rail foot, an S3 certifier that reads the pair open vetoes the link); a chain pair absent from every record; a stale record (1.3 P4: a link passes on any certifier: S1 or S2 latest accepted unsuperseded record, not stale, K7 entry in a C state; S3 section K7 in a C state with the named face; declared listed; a, b links by symmetry from c under SYM) |`
21. l.275 (detail 1.3 Script line). Old: `pose capture_end, 63 rows, load_cases, s3_checks, chains, reported_items (10).` New: `pose capture_end, 65 rows, load_cases, s3_checks, chains, reported_items (10). Stub: docs/sketches/stubs/s3_stub.py (1.3 (c) P4; s3 --rev 0 red by cause 15/15 in wip/baseline_red.json).`
22. l.295 (TP-7 carried). Old: `with a B control that plants an inverted or mis-projected inset; The Topologist verifies at (e).` New: `with a B control that plants an inverted or mis-projected inset; The Topologist verifies at (e). Done at 1.3 (c) P4 (step1.3_engineer_redfirst.md): view per Axes, per_axes wrapper, section view section_yz, renderer section convention, S3-1 to S3-3, SYM, x1_exempt narrowed; K3-B10, K5-B25, K8-B53, K9-B8, K9-B9; signatures at P5T (Topologist), P5L (Loftsman), P5 (Software Engineer).`
23. l.299 (Carried to S1 r8). Old: `If the rule fails its Z or B, option B (line deleted) applies.` New: `If the rule fails its Z or B, option B (line deleted) applies. Landed at P4 (c): K5 mark_issues M1 to M5 with K5-Z5, K9-Z5 (S1 fixture with both marks) and K5-B26 to B32, each clean on the pre-change code; section form (hull of the parent's pieces) for anchor_bearing_c:line in S3, for the Topologist at P5T.`
24. l.607 (Design Notes 20 TP-7 row). Old: `| TP-7 | K3 to K9 iterate over declared inset Axes, with a B control | 1.3 (S3), before the stub run | The Engineer; The Topologist verifies |` New: `| TP-7 | K3 to K9 iterate over declared inset Axes, with a B control | 1.3 (S3), before the stub run; landed at 1.3 (c) P4 (per_axes; K3-B10, K5-B25, K8-B53, K9-B8, K9-B9), Topologist signature at P5T pending | The Engineer; The Topologist verifies |`
