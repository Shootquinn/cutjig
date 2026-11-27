# Step 1.4 step 0 (P0), The Engineer: harness work before S4 (b)

## Corrections to the brief

1. R1 a: every controls result row already carried `seconds` (1.3 step 0, `check_sketch.control_row`; excluded from `CONTROL_EQ_FIELDS`). No change; the profile reads it.
2. R6: the `s3_spec.yaml` W comment already reads 26.25 (l.115, set at 1.3 r7 under M1 S3 r6 N4); no "24.25" remains in `s3_spec.yaml` (MEASURED by search). R6 edits the status text and `ring.nut_mounting` only.
3. R4 c and R7: rule (l) at class scope fires on S2 r9 (3 plan gridline firings) and on the S3 r7 inset plan (1 gridline firing), as well as on S1 r8 (MEASURED, section 5). S3 r7 is clean in its section Axes for every family and clean for part edges and reference lines in both Axes, so the R4 a Z controls are written on those scopes (K4-Z9, K4-Z10). The refreshed S3 r7 record fails K4, so "s3 r7 re-acceptable with deps" does not hold (section 9).
4. R5 c: the Designer's DR4-2 reading of the live head half-width, 1.14 mm, is the arrow path taken at a dpi correction of 1 (figure not drawn at its dpi). Drawn at the figure dpi 150 the half-width is 2.38 mm (DERIVED: head_width 0.2 x mutation_scale 14 pt x 150/72 px per pt over 2.45 px per mm; the same value from the drawn path, MEASURED). The example bound 2.0 mm would fail S3 r7. No numeric bound is set here (section 6, item c).
5. Facts at the open: `--controls` wrote ctrl_a to ctrl_d PNGs to `wip/fixtures/figs/` and no key.json there (MEASURED); key.json and the four PNGs with the old mapping sit in the committed `docs/sketches/fixtures/figs/` (copied up by `--accept` at 1.3). The committed copies are not edited (outside R3 b); open item 4.
6. Pre-change full set at the open: 413 controls, 225.7 s wall at 12 jobs, 2504.3 control-seconds (MEASURED here; the 1.3 close quotes 229.0 s).

## 1 Files changed

| Path (docs/sketches/) | What |
|---|---|
| check_sketch.py | R1: `prior_seconds`, `submit_order` (pool tasks longest first; rows still in manifest order); `--fast`, `fast_ids`, `select_fast`, `controls_dst(man, only, fast)`. R2: `record_deps`, `deps` written by every sN run, `DEPS_EXEMPT`, `stale_deps`, the deps branch in `stale()`. R3: `--m1-controls --out --key`, `m1_controls`; control figures and key.json removed from `--controls`; `harness_outputs` copies no figure; `CONTROL_FIGS` removed. Docstring. |
| sketch_loader.py | R1 e: `load_yaml` parse cached per process under the file bytes' SHA-256, fresh deep copy per call. |
| sketch_common.py | R4: `collinear_lines`, `_clip_box`, `_run_near_vis`, `collinear_issues` rewritten (families, views, Axes), `COLLINEAR_FAMILIES`, `VIEW_AXES`. R5 a: `ND_KEY_REF` literal-band lint in `not_drawn_band_issues`. R5 c: `terminator_shape_issues`, `TERM_STYLE`, `TERM_MUTATION_SCALE`, `terminator_half_width_mm`, `terminator_issues(..., script)`. R5 d: `stall_literal_issues`, called from `load_literal_issues`. |
| checks_s3.py | R2: S3-3 records each certifier record it resolves on `ctx.certifiers`. |
| fixtures/builders.py | R3: `control_figures()` returns {role: (figure, criterion, expected)}, `CONTROL_ROLES`; no file name, no letter. R1 e: `draw_cache` (keyed on file SHA-256 and module fingerprints), used by `_script_ctx` and `_s2_ctx` for unmutated drawings. |
| fixtures/s3_fixtures.py | R1 e: `s3_ctx` takes the faithful drawing from `draw_cache` when it has no spec_mut, values, spec or skip; the plant runs on the copy. |
| fixtures/step14_fixtures.py | New: the 31 new controls (FAST, RUN-Z3, DEPS, M1C, K4 rule (l), R5 items). |
| fixtures/fast.yaml | New: the fast tier (314 ids). |
| fixtures/manifest.yaml | 31 controls added; K4-Z3, Z4, Z8 re-scoped Z to B; 20 K4 B re-counted (section 8). |
| s3_spec.yaml | R6 status text; R5 a pinion and base-frame not_drawn x bands as key expressions. |
| s2_spec.yaml | R5 e: l.94 reported_items source `s1_mass_report_r7.json` to `s1_mass_report_r8.json`. |
| proposed_params.yaml | R6: `ring.nut_mounting` value text. |
| wip/fixtures/figs/ctrl_a.png to ctrl_d.png | Deleted (generated outputs; no key.json was there). |

## 2 R1 profile, fast tier, pruning candidates, wall times

Pre-change full set (413 controls, 12 jobs, MEASURED): wall 225.7 s, 2504.3 control-seconds.

30 slowest controls (pre-change seconds in the worker; planted item from the manifest desc):

| ID | s | Family | Fixture | Planted |
|---|---|---|---|---|
| K4-B18 | 28.32 | K4 | builders.py::k4_b18 | tie a label on its phantom line under a planted nearer disk |
| S2-FULL | 27.89 | smoke | builders.py::s2_full_draw | every S2 row drawn, K1 to K9 and S2-1 to S2-6 |
| K4-B28 | 20.99 | K4 | s3_fixtures.py::k4_frac_range | guide_c frac 1.5 |
| K4-B27 | 20.98 | K4 | s3_fixtures.py::k4_frac_088 | anchor_c frac 0.88 |
| K4-B26 | 20.88 | K4 | s3_fixtures.py::k4_ring_mass | ring.mass + 4 kg, literals unchanged |
| S3-FULL | 20.85 | smoke | s3_fixtures.py::s3_full_draw | every S3 row drawn, K1 to K9 and S3-1 to S3-3 |
| K4-Z8 | 20.58 | K4 | s3_fixtures.py::k4_live_s3 | live S3 |
| K4-B29 | 19.38 | K4 | s3_fixtures.py::k4_frac_removed | frac removed (r95 layout) |
| K4-B30 | 18.77 | K4 | s3_fixtures.py::k4_leader_on_grid | load_comp_c leader on z 400 |
| K4-B31 | 18.52 | K4 | s3_fixtures.py::k4_start_label_wrong | start label 1020.84 |
| K4-B16 | 18.02 | K4 | builders.py::k4_b16 | gear outline as an open C |
| K4-B17 | 17.76 | K4 | builders.py::k4_b17 | ring label 0.028 outside tie a |
| K4-B12 | 17.73 | K4 | builders.py::k4_b12 | descent-stop label on the r4/r5 leader |
| K4-B11 | 17.66 | K4 | builders.py::k4_b11 | area over the tube OD anchor |
| K4-B15 | 17.25 | K4 | builders.py::k4_b15 | drill_head label without its suffix |
| K4-B23 | 17.22 | K4 | s3_fixtures.py::k4_through_text | text on the drill_tube leader |
| K4-B19 | 17.13 | K4 | builders.py::k4_b19 | S2 r7 leaders 1.87 apart |
| K4-B24 | 17.11 | K4 | s3_fixtures.py::k4_text_overlap | text on the base_plate label |
| K4-B10 | 17.09 | K4 | builders.py::k4_b10 | area above the tube OD leader |
| K4-B14 | 17.04 | K4 | builders.py::k4_b14 | ring label at the P1R r6 anchor |
| K4-B8 | 16.78 | K4 | builders.py::k4_b8 | r1 anchors on y = 0 |
| K4-B7 | 16.70 | K4 | builders.py::k4_b7 | sightline label at the r1 point |
| K4-Z3 | 16.55 | K4 | builders.py::k4_z3 | live S2 by s2_plan.py |
| S1-FULL | 16.48 | smoke | builders.py::s1_full_draw | every S1 row drawn |
| K8-B51 | 16.48 | K8 | builders.py::k8_b51 | sector alpha 0.95 before the renderer |
| K8-B35 | 16.23 | K8 | builders.py::k8_b35 | ties without plan_style stand_in |
| K8-B34 | 16.00 | K8 | builders.py::k8_b34 | rail top in the +Y notch dashed |
| K8-B42 | 15.91 | K8 | builders.py::k8_b42 | stand_in_owner tbd |
| K8-B40 | 15.85 | K8 | builders.py::k8_b40 | -Y rail solid copy removed |
| K8-B41 | 15.75 | K8 | builders.py::k8_b41 | tie a stand_in without owner |

Share of control-seconds (pre-change, MEASURED): K8 106 controls, 833.5 s, 33.3 %; K4 39, 484.7 s, 19.4 %; K5 54, 277.0 s, 11.1 %; K7 53, 220.0 s, 8.8 %; S3-3 18, 194.7 s, 7.8 %; smoke 3, 65.2 s, 2.6 %; K9 2.1 %; K6 2.0 %; K3 1.4 %; S2-5b 1.4 %; every other family under 1 % (RUN 0.9, S2-5a 0.9, S3-2 0.8, H1 0.8, S2-2 0.7, S2-6 0.7, S3-1 0.6, K2 0.5, SYM 0.4, S1-4 0.4, S2-3 0.4, S2-4 0.3, S2-1 0.3, S1-2 0.3, S1-1 0.3, SYM-P 0.3, X1 0.3, S1-6 0.3, S1-5a 0.2, S1-5b 0.2, S1-3 0.2, S1-7 0.2, H5 0.1, RPT 0.1, K1 0.0). 159 controls over 8 s hold 1926 of the 2504 control-seconds: every one rebuilds a live S2 or S3 drawing (s2_plan renderer and placer about 4 s, S3 script about 5 s, the YAML parse of params, overlay and spec about 1 s per build; solo, MEASURED).

Speedups (R1 e), rows compared with the pre-change run on id, expected, observed, reason, match (MEASURED, 413 controls, snapshot trees in the scratch folder):

| Change | Wall (12 jobs) | Control-seconds | Rows equal |
|---|---|---|---|
| none (pre-change) | 225.7 s | 2504.3 | reference |
| YAML parse cache + longest-first submission | 162.2 s | 1865.4 | 412/413; H1-B5 differs only in the temporary directory path inside its reason (excluded, 1.3 P0S) |
| + per-worker cache of unmutated live drawings (pickle copy, Agg canvas re-attached) | 128.4 s | 1497.2 | 412/413, the same H1-B5 path difference |

A later full run with the drawing cache keyed only on file hashes read K8-B51 clean: the fixture patches `s2_plan._style_visible` and received an unpatched cached drawing. The cache key now carries the identity of every callable in sketch_common, check_stack, the fixture module and the script module, so a patched build neither reads nor leaves an entry for others; K8-B51 and K4-Z3 matched in both orders in one process (MEASURED). The final run is the evidence of record.

Final runs of record (live tree, MEASURED): `--controls` 444 controls (Z 104, B 337, smoke 3; 413 at the open), all match, wall 128.5 s at 12 jobs, 1485.0 control-seconds; the 390 controls unchanged from the open read rows equal to the pre-change run (H1-B5 temp path only); the 23 re-scoped or re-counted K4 controls differ as section 8 lists. `--controls --fast` 314 controls (Z 37, B 277), all match, wall 103.3 s, PARTIAL, not a record.

Fast tier (`fixtures/fast.yaml`, `--controls --fast`). Rule: every check family's least-time Z and, per B branch, its least-time B; a branch is the manifest `finding` that added the B, or the B itself when it names none. 314 of 444 controls. Measured 103.3 s wall (Z 37, B 277, all match). The 60 s target is missed: most B controls are the only member of their branch, so one B per branch keeps 71 % of the set. What would close it: (i) a coarser branch definition ruled by The Software Engineer (by check rule letter or predicate kind instead of by finding); (ii) one build of each live drawing per run instead of one per worker (today each of 12 workers builds each live drawing once, about 11 x 20 = 220 control-seconds, about 18 s wall, DERIVED); (iii) K4 on live S3 costs about 4 s solo, now including rule (l) over every part edge.

Pruning candidates (R1 d): B pairs of one check with the same planted count, each pair's reason substrings found in the other's observed reason (MEASURED on the 413-control run). None deleted; The Software Engineer rules at P0S.

| Pair | Planted items | Reason substrings | Branch | Seconds saved (pre-change) |
|---|---|---|---|---|
| K7-B31 / K7-B34 | G 10 at p4 declared on the pair / written only on the fixed member | swept p1..p4/ring\|member F, swept hull, overlap 2000.000 | same (pose-restricted declaration in the swept form) | 1.0 |
| RPT-B1 / RPT-B5 | declared item absent / value None | reported item F_stall, no value | same (the value-None test) | 0.0 |
| S3-3-B2 / S3-3-B8 | S1 record without receiver\|holder / pair at load only | chain c: base_plate\|base_frame not certified (... pair absent) | same (`_pair_ok` not found) | 11.1 |
| K7-B4 / K7-B8 | side / plan swept member | swept, ring\|member | different (side and plan swept forms) | 1.0 |
| K8-B1 / K8-B8 | drill flipped in coordinates / by the artist transform | drill_head below gear, drill_head below drill_top_block | different (TP-1 transform chain) | 1.9 |
| K3-B8 / K3-B9 | text below the canvas / savefig without tight | ... outside the saved image | different (premise branch) | 4.1 |
| K8-B39 / K8-B49 | sector alpha 1 / 0.95 | base_plate cover, opaque fill of operator_sector | different (alpha rule band) | 15.5 |

Pruning the three same-branch candidates saves 12.1 control-seconds, about 1 s wall (DERIVED). Full-set target (G4, at most 200 s): met, 128.5 s for 444 controls (MEASURED); pruning is not needed for it.

## 3 R2 deps, --stale branch, controls

- Record: every sN run writes `deps = {spec: {path, sha256}, script: {path, sha256}, certifiers: [{sketch, path, rev, sha256}]}`; paths relative to docs/sketches/; the certifiers are the records S3-3 resolved through `_records` (`ctx.certifiers`, filled where a record certifier is consulted). `--accept` rewrites the record with its flags and carries `deps` unchanged.
- `--stale`: after the key branch, `stale_deps(docs, wip)` over the latest accepted, unsuperseded records: no deps fails unless the record name is in `DEPS_EXEMPT` (s1_checks_r8.json, s2_checks_r9.json, printed "deps not recorded, exempt (accepted before deps)"); spec and script SHA-256 recomputed under docs/; each certifier must be the latest accepted, unsuperseded record of its sketch at the recorded file name and SHA-256. Each difference prints `STALE deps ...`; exit 1.
- Live `--stale` now: section 9.
- Controls (temporary trees under TMP, removed after each control): DEPS-Z clean; DEPS-Z2 (a live s3 run to a temporary wip/ writes spec, script and certifiers s1 r8, s2 r9 with their SHA-256) clean; DEPS-B1 to B6 fire 1 each (section 8). On the pre-change code each B reads clean (the fixture falls back to the keys-only `--stale`, which reads 0 differences on every planted tree) and DEPS-Z2 fires (no deps field) (MEASURED).

## 4 R3 blinded control command and controls

- `check_sketch.py --m1-controls --out <dir> --key <path>`: `builders.control_figures()` draws the four figures by role; each is saved as `m1c_<token>.png` with a fresh `secrets.token_hex(3)` (redrawn on a collision within the round); the key (token, role, criterion, expected verdict) is written as JSON sorted by token to <path>. Refused with nothing written when <dir> exists and is not empty, when <path> lies inside the project root (the directory holding params.yaml), or when <path> lies inside <dir>.
- `--controls` draws no figure and writes no key.json; `harness_outputs` copies no figure; `wip/fixtures/figs/ctrl_a.png` to `ctrl_d.png` deleted. `builders.control_figures` holds no file name and no letter mapping in code or docstring (MEASURED by search).
- Controls: M1C-Z (4 PNGs, no other file, 4 distinct tokens, 4 key entries, the four roles) clean; M1C-Z2 (two runs: token sets 4 and 4, 0 shared) clean; M1C-B1 (key inside the project root) fires 1; M1C-B2 (out folder not empty) fires 1; M1C-B3 (key inside the out folder) fires 1; M1C-B4 (token source pinned, a stand-in for a non-random generator) fires 1 (4 shared). Pre-change: no command; the Z fire and the B read clean.
- This file prints no token-to-role mapping and no expected verdict.

## 5 R4 rule (l) class, controls, dry-run firing table

Rule (l) (`collinear_issues`, K4): on a script-drawn figure (the context's script, or its parent's for an inset Axes), in every view and every declared Axes, a label leader (text position to anchor, clipped to the Axes box) fails when it runs within 2 deg and 1.0 mm of a line over more than 5 mm (thresholds as signed). Line families (`collinear_lines`): reference line (every Line2D segment of a reference line row and its sub-artists); gridline (major and minor, both axes, inside the limits; named `gridline <axis> <value>`, axis names by view: side x/z, plan x/y, section u/z); part edge (every ring edge of every tagged area artist of another row, renderer hidden copies included; a renderer piece counts only where it is drawn, inside its clip path). One issue per leader and reference segment or gridline (as at r6), one per leader and tagged artist id for part edges. Reason text as at r6, "label leader runs X mm along <line> within 1 mm (K4 collinear)", part edges named "part edge of <gid>".

Scope reached: side_xz (S1), plan_xy (S2, S3 inset), section_yz (S3). section_xz: no view drawn yet; `VIEW_AXES` names its axes, nothing else in the rule is view-specific. Curved outlines are tested edge by edge (a leader tangent to a sampled circle is no run along one line); carried as a NOTE.

Controls: K4-Z9 (live S1 r8, S2 r9, S3 r7: 0 part-edge and 0 reference-line firings in every Axes), K4-Z10 (live S3 section Axes: 0 firings in every family), K4-Z11 (premise of the clip relief: a planted part edge clipped off along the leader reads 0 firings; red by deleting the clip term: fires "frame_upper_c ... part edge of motor23_c", MEASURED). B per family and view, each clean on the pre-change code (MEASURED):

| Family | Side (S1) | Plan (S2; S3 inset) | Section (S3) |
|---|---|---|---|
| gridline | K4-Z4 re-scoped to B (live height_target on z 2000, 4 poses) | K4-Z3 re-scoped to B (live S2, 3); K4-Z8 re-scoped to B (live S3 inset, 1) | K4-B30 (existing) |
| reference line | K4-B32 | K4-B34 | K4-B29 (existing) |
| part edge | K4-B33 | K4-B35 | K4-B36 |

Dry run on the drawings of record (live specs drawn by their scripts; MEASURED):

| Sketch | Axes (view) | Pose | Labelled row | Family | Line | Angle (deg) | Distance (mm) | Overlap (mm) |
|---|---|---|---|---|---|---|---|---|
| S1 r8 | main (side_xz) | load | height_target | gridline | gridline z 2000 | 0.00 | 0.00 | 32.2 |
| S1 r8 | main (side_xz) | start | height_target | gridline | gridline z 2000 | 0.00 | 0.00 | 32.2 |
| S1 r8 | main (side_xz) | capture_end | height_target | gridline | gridline z 2000 | 0.00 | 0.00 | 32.2 |
| S1 r8 | main (side_xz) | park | height_target | gridline | gridline z 2000 | 0.00 | 0.00 | 32.2 |
| S2 r9 | main (plan_xy) | load | base_plate | gridline | gridline y 0 | 0.00 | 0.00 | 32.2 |
| S2 r9 | main (plan_xy) | load | slot_line_c | gridline | gridline y 260 | 0.00 | 1.00 | 32.2 |
| S2 r9 | main (plan_xy) | load | screw_b | gridline | gridline y 80 | 1.29 | 0.00 | 44.5 |
| S3 r7 | inset_plan (plan_xy) | capture_end | screw_b | gridline | gridline y 80 | 0.00 | 0.00 | 195.4 |

Firings: S1 4, S2 3, S3 1; part edges 0 and reference lines 0 in every sketch. No label moved. All go to the P6 revision batch: S1 r9, S2 r10, S3 r8. S2 slot_line_c sits at 1.00 mm, on the threshold (within, inclusive). K4 now fails on all three drawings of record.

Consequence for existing controls: every K4 control drawn on a live script drawing carries the live firings. K4-Z3, K4-Z4, K4-Z8 (live S2, S1, S3 "clean") are re-scoped Z to B with the firings as their reasons; 20 K4 B are re-counted (section 8). They return to Z and to their 1.3 counts when P6 lands the layouts.

## 6 R5 item table

| Item | Disposition | Z | B (red on pre-change code) |
|---|---|---|---|
| a R2-6 not_drawn literal x bands | Implemented. Pinion bands: toe corner r_in cos theta - hw_in sin theta, r_in = r_toe - pitch_diameter / tooth_count sin(pitch_angle), hw_in = outer_diameter / 2 x r_in / r_heel; outer corner (r_heel + hub_length) cos theta + outer_diameter / 2 sin theta; theta = pinion.angle[1], [2]: -144.0536 to -65.0889 and 65.0889 to 144.0536 (DERIVED; literals were 144.05, 65.09). Base-frame bands: frame.end_x and frame.support_x +- profile.width / 2: -262, -202, -142, -82, 82, 142, 202, 262 (equal to the literals). Lint: a band bound naming no dotted key fails "reads no key". The keys enter keys_read through eval_expr, so --stale reaches them. Margins 5.09 and 22.00 unchanged. | live S3 K8 Z set clean | K8-B90: literal pinion bands re-planted, 2 issues; clean on pre-change |
| b R2-7 arc a1 branch | B added. | K5-Z7 | K5-B48: screw_c declares arc and draws screw_c:arc in the section, fires 1. It fires on the pre-change code too (the branch existed without a B); red by deleting the a1 lines: clean, mismatch (MEASURED) |
| c DR4-2 terminator form | Implemented: (1) every terminator's connection style is Arc3 rad 0; (2) on a script-drawn figure the arrowstyle is the signed r4 one, CurveFilledB (head_length 0.4, head_width 0.2) at mutation_scale LABEL_FONTSIZE x 2 = 14 pt, which fixes the head size. A numeric half-width bound in mm is The Designer's value: the drawn half-width is 2.38 mm on S3 r7 (Correction 4), so the 2.0 example would fail the live drawing. | live S3 K8 clean | K8-B91 mutation_scale 30, fires 1; K8-B92 arc3 rad 0.2, fires 1; both clean on pre-change |
| d rule (j) NOTE, every number of a stall literal | Implemented: `stall_literal_issues`: a text literal '<v1> / <v2> (mu <m1> / <m2>)' pairs values and mus in order; each mu must be a thread_mu value; each value after the first agrees with F_stall per screw at its mu within 0.005 N (the first stays held by the existing rule). Live: 282.21 against 282.2146 N in stall_up and stall_down, clean. | K4-Z10 scope (live S3 section) | K4-B37: 282.21 written 283.21 in stall_up, fires 1 (plus the live inset firing, planted 2); clean on pre-change |
| e LF1.3-11 | `s2_spec.yaml` l.94 source text `s1_mass_report_r7.json` to `s1_mass_report_r8.json` (text; S2 re-run under (i), section 9). | none | none (text) |
| f TP1.3-4 | Stays NOTE: declared 2.5 mm cover resolution; no live part or gap narrower. Carried to S4 (c) (holder section rows). | | |
| f TP1.3-5 | Stays NOTE (The Designer): stacked translucent fills; no live case. Carried to S4 (c). | | |
| f TP1.3-6 | Closed in the P1R code: after PLACER_PASSES rounds a label still failing is recorded UNPLACEABLE with its final issues (`place_plan_labels`). The rounds-exhausted path has no B of its own (K4-B13 covers the no-candidate path); the B is carried to S4 (c) with the K4 delta. | | |
| f TP1.3-7 | Stays NOTE: `drawn_region` reads the clip path's `_path` and `_transform`; matplotlib 3.11.2; re-check on upgrade. K4-Z11 now exercises it too. | | |
| f TP1.3-9 | Stays NOTE: annulus edge band above width 125 mm; no live case. Carried to S4 (c). | | |
| f TP1.3-16 | Stays NOTE: a K8 per-predicate test list (pose, row, predicate, measured, sign) changes every K8 record and result; carried to S4 (c) inside the K8 delta The Software Engineer reviews. | | |
| f TP1.3-17 | An accepted S1 spec edit (anchor mark.z to the key `jackscrew.anchor_bearing_z`) under (i): to the P6 S1 r9 batch. | | |
| f TP1.3-18 | Designer M1 NOTE (liftmotor_a/_b drawn at the circumscribing width): to the S1 r9 M1. | | |
| f TP1.3-20 | A drawn change (wingnut sweep envelope from the part gid to a reference row): to the P6 S1 r9 batch. | | |
| g LF1.3-12 | Step 2 bearing row; no action. | | |

## 7 R6

- `s3_spec.yaml` status: "draft for signature (Designer part list, Loftsman); ..." to "accepted at S3 r7 (Sean M2 2026-11-26, 'Apply fixes as r7, accept'; Design Notes 13; --accept s3 --rev 7 at 1.3 ORCH-B); signed by The Designer (part list) and The Loftsman at 1.3 (b) P2f2. History: ..." (edit history kept).
- `proposed_params.yaml` `ring.nut_mounting` value: "floating brass flange nut held by three shoulder screws: 0.5 radial float, 0.05 axial play, the shoulder screws also stop rotation (S3-2: K 0.7 over the anchor-to-guide span L_t)" (Design Notes 31 M2 pick). Source and status unchanged.
- W comment: already 26.25 (Correction 2).
- `ring.nut_mounting` in keys_read: 0 occurrences in s1_checks_r8.json, s2_checks_r9.json, s3_checks_r7.json, and read by no script or spec (MEASURED by search).
- Both edits precede every R2 hash; the R7 runs are the first records with deps.

## 8 Control table

New controls (31). Pre-change result: the entry run on the pre-change tree (`--manifest` of the new entries, step14_fixtures.py copied in), MEASURED.

| ID | Planted | Reason substring | Pre-change result | Result (final run) |
|---|---|---|---|---|
| RUN-Z3 | controls_dst(live manifest, --fast) is the partial destination, never the record | - | fires (red) | clean, match yes |
| FAST-Z | fixtures/fast.yaml keeps every check family's Z and one B per branch (finding, or the control itself) | - | error (red) | clean, match yes |
| FAST-B1 | fast list with every K4 Z removed | K4 has no Z in the fast tier | error (red) | fires (1 issue(s), planted 1), match yes |
| FAST-B2 | fast list without the K8 terminator branch | K8 branch 'Designer NOTE D-r3-1' has no B in the fast tier | error (red) | fires (1 issue(s), planted 1), match yes |
| DEPS-Z | temp tree: refreshed S3 record with deps; S1 r8, S2 r9 exempt by name | - | clean (matches) | clean, match yes |
| DEPS-Z2 | a live s3 run (record to a temp wip/) writes deps: spec, script, certifiers s1 r8 and s2 r9 with SHA-256 | - | fires (red) | clean, match yes |
| DEPS-B1 | temp S1 r9 accepted over r8: S3 certifier superseded | deps certifier s1 recorded s1_checks_r8.json; certifier superseded | clean (0 issue(s), planted 1); reason lacks ['deps certifier (red) | fires (1 issue(s), planted 1), match yes |
| DEPS-B2 | certifier record edited | deps certifier s1_checks_r8.json sha256 recorded | clean (0 issue(s), planted 1); reason lacks ['deps certifier (red) | fires (1 issue(s), planted 1), match yes |
| DEPS-B3 | one neighbour class edited in the temp spec | deps spec s3_spec.yaml sha256 recorded | clean (0 issue(s), planted 1); reason lacks ['deps spec s3_s (red) | fires (1 issue(s), planted 1), match yes |
| DEPS-B4 | one comment byte changed in the temp script | deps script s3_jackscrew_section.py sha256 recorded | clean (0 issue(s), planted 1); reason lacks ['deps script s3 (red) | fires (1 issue(s), planted 1), match yes |
| DEPS-B5 | a non-exempt accepted record without deps | s3_checks_r7.json: deps not recorded | clean (0 issue(s), planted 1); reason lacks ['s3_checks_r7.j (red) | fires (1 issue(s), planted 1), match yes |
| DEPS-B6 | the exemption does not cover S1 r9 (no deps) | s1_checks_r9.json: deps not recorded | clean (0 issue(s), planted 1); reason lacks ['s1_checks_r9.j (red) | fires (1 issue(s), planted 1), match yes |
| M1C-Z | --m1-controls into an empty folder, key outside: four m1c_<token>.png, no other file, four tokens, four key entries | - | fires (red) | clean, match yes |
| M1C-Z2 | two runs, disjoint token sets (counts only) | - | fires (red) | clean, match yes |
| M1C-B1 | key path inside the project root | refused: key path; inside the project root | clean (0 issue(s), planted 1); reason lacks ['refused: key p (red) | fires (1 issue(s), planted 1), match yes |
| M1C-B2 | out folder not empty | refused: out folder; is not empty | clean (0 issue(s), planted 1); reason lacks ['refused: out f (red) | fires (1 issue(s), planted 1), match yes |
| M1C-B3 | key path inside the out folder | refused: key path; inside the out folder | clean (0 issue(s), planted 1); reason lacks ['refused: key p (red) | fires (1 issue(s), planted 1), match yes |
| M1C-B4 | token source pinned: two runs share tokens | token sets overlap: 4 shared | clean (0 issue(s), planted 1); reason lacks ['token sets ove (red) | fires (1 issue(s), planted 1), match yes |
| K4-Z9 | live S1 r8, S2 r9, S3 r7: 0 part-edge and 0 reference-line firings in every Axes | - | clean (matches) | clean, match yes |
| K4-Z10 | live S3 r7 section Axes: 0 firings in every family | - | clean (matches) | clean, match yes |
| K4-Z11 | planted quad clipped so its edge along the leader is not drawn: 0 firings | - | clean (matches); red by deleting the clip term: fires | clean, match yes |
| K4-B32 | side view, reference line: height_target line beside the screw_a leader (S1 load; the live gridline firing reads too) | load/screw_a: label leader runs 294.0 mm along height_target within 1 mm; load/height_target: label leader runs 32.2 mm along gridline z 2000 | clean (0 issue(s), planted 2); reason lacks ['load/screw_a:  (red) | fires (2 issue(s), planted 2), match yes |
| K4-B33 | side view, part edge: base_plate quad edge beside the screw_a leader (S1 load) | load/screw_a: label leader runs 294.0 mm along part edge of base_plate; along gridline z 2000 | clean (0 issue(s), planted 2); reason lacks ['load/screw_a:  (red) | fires (2 issue(s), planted 2), match yes |
| K4-B34 | plan view, reference line: sightline_f6 line beside the frame_upper_c leader (S2; three live gridline firings read too) | load/frame_upper_c: label leader runs 196.4 mm along sightline_f6 within 1 mm; gridline y 0; gridline y 260; gridline y 80 | clean (0 issue(s), planted 4); reason lacks ['load/frame_upp (red) | fires (4 issue(s), planted 4), match yes |
| K4-B35 | plan view, part edge: ring quad edge beside the frame_upper_c leader (S2) | load/frame_upper_c: label leader runs 196.4 mm along part edge of ring; gridline y 0; gridline y 260; gridline y 80 | clean (0 issue(s), planted 4); reason lacks ['load/frame_upp (red) | fires (4 issue(s), planted 4), match yes |
| K4-B36 | section view, part edge: motor23_c quad edge beside the frame_upper_c leader (S3; the live inset gridline firing reads too) | capture_end/frame_upper_c: label leader runs 360.9 mm along part edge of motor23_c; capture_end/screw_b: label leader runs 195.4 mm along gridline y 80 | clean (0 issue(s), planted 2); reason lacks ['capture_end/fr (red) | fires (2 issue(s), planted 2), match yes |
| K4-B37 | stall_up literal second number 282.21 written 283.21 (live S3; inset gridline firing reads too) | load_cases stall_up per_screw literal 283.21 at mu 0.2; along gridline y 80 | clean (0 issue(s), planted 2); reason lacks ['load_cases sta (red) | fires (2 issue(s), planted 2), match yes |
| K8-B90 | pinions not_drawn entry with its literal x bands re-planted | x band 1 bound -144.05 reads no key; x band 2 bound 65.09 reads no key | clean (0 issue(s), planted 2); reason lacks ['x band 1 bound (red) | fires (2 issue(s), planted 2), match yes |
| K8-B91 | span_lt terminator at mutation_scale 30 (live S3) | at mutation_scale 30, not the signed terminator | clean (0 issue(s), planted 1); reason lacks ['at mutation_sc (red) | fires (1 issue(s), planted 1), match yes |
| K8-B92 | span_lt terminator with arc3 rad 0.2 (live S3) | connection style Arc3 rad 0.2 is not straight | clean (0 issue(s), planted 1); reason lacks ['connection sty (red) | fires (1 issue(s), planted 1), match yes |
| K5-B48 | screw_c declares sub_artists arc and draws screw_c:arc in the section | arc on screw_c admitted in plan_xy only (view section_yz) | fires (1 issue(s), planted 1) (matches); red by deleting the a1 branch: clean | fires (1 issue(s), planted 1), match yes |

Re-scoped and re-counted (23), each drawn on a live script drawing; the added issues are the live rule (l) firings of section 5. Pre-change result from the 413-control run.

| ID | Change | Pre-change | Final |
|---|---|---|---|
| K4-Z3 | Z to B, planted 3 | clean | fires (3 issue(s), planted 3), match yes |
| K4-Z4 | Z to B, planted 4 | clean | fires (4 issue(s), planted 4), match yes |
| K4-Z8 | Z to B, planted 1 | clean | fires (1 issue(s), planted 1), match yes |
| K4-B7 | planted 4 to 7 | fires (4 issue(s), planted 4) | fires (7 issue(s), planted 7), match yes |
| K4-B8 | planted 7 to 10 | fires (7 issue(s), planted 7) | fires (10 issue(s), planted 10), match yes |
| K4-B9 | planted 1 to 2 | fires (1 issue(s), planted 1) | fires (2 issue(s), planted 2), match yes |
| K4-B10 | planted 1 to 4 | fires (1 issue(s), planted 1) | fires (4 issue(s), planted 4), match yes |
| K4-B11 | planted 2 to 5 | fires (2 issue(s), planted 2) | fires (5 issue(s), planted 5), match yes |
| K4-B12 | planted 1 to 4 | fires (1 issue(s), planted 1) | fires (4 issue(s), planted 4), match yes |
| K4-B14 | planted 4 to 7 | fires (4 issue(s), planted 4) | fires (7 issue(s), planted 7), match yes |
| K4-B15 | planted 1 to 4 | fires (1 issue(s), planted 1) | fires (4 issue(s), planted 4), match yes |
| K4-B16 | planted 2 to 5 | fires (2 issue(s), planted 2) | fires (5 issue(s), planted 5), match yes |
| K4-B17 | planted 1 to 4 | fires (1 issue(s), planted 1) | fires (4 issue(s), planted 4), match yes |
| K4-B18 | planted 3 to 6 | fires (3 issue(s), planted 3) | fires (6 issue(s), planted 6), match yes |
| K4-B19 | planted 2 to 4 | fires (2 issue(s), planted 2) | fires (4 issue(s), planted 4), match yes |
| K4-B23 | planted 2 to 5 | fires (2 issue(s), planted 2) | fires (5 issue(s), planted 5), match yes |
| K4-B24 | planted 1 to 4 | fires (1 issue(s), planted 1) | fires (4 issue(s), planted 4), match yes |
| K4-B26 | planted 4 to 5 | fires (4 issue(s), planted 4) | fires (5 issue(s), planted 5), match yes |
| K4-B27 | planted 1 to 2 | fires (1 issue(s), planted 1) | fires (2 issue(s), planted 2), match yes |
| K4-B28 | planted 3 to 4 | fires (3 issue(s), planted 3) | fires (4 issue(s), planted 4), match yes |
| K4-B29 | planted 2 to 4 (+ reason: load_tension_c along part edge of bearing in the r95 layout) | fires (2 issue(s), planted 2) | fires (4 issue(s), planted 4), match yes |
| K4-B30 | planted 1 to 2 | fires (1 issue(s), planted 1) | fires (2 issue(s), planted 2), match yes |
| K4-B31 | planted 1 to 2 | fires (1 issue(s), planted 1) | fires (2 issue(s), planted 2), match yes |

## 9 R7 run table and record diffs

Order: final `--controls` (444) first, so each record's Z and B tallies read the final run; then the runs below to wip/ (MEASURED).

| Run | Exit | Checks | PNG against docs/sketches/ | Re-acceptable |
|---|---|---|---|---|
| s1_side_poses.py --rev 8; check_sketch.py s1 --rev 8 | 0; 1 | 18/19 pass; K4 fail (height_target on gridline z 2000, 4 poses) | 4 PNGs byte-equal | no (K4) |
| s1_mass_report.py --rev 8 | 0 | n/a | n/a | mass report JSON equal to the accepted one (0 field differences) |
| s2_plan.py --rev 9; check_sketch.py s2 --rev 9 | 0; 1 | 17/18 pass; K4 fail (3 plan gridline firings) | s2_plan_r9.png byte-equal | no (K4) |
| s3_jackscrew_section.py --rev 7; check_sketch.py s3 --rev 7 | 0; 1 | 15/16 pass; K4 fail (inset screw_b on gridline y 80) | s3_jackscrew_section_r7.png byte-equal | no (K4) |

Fields that differ, wip/ record against docs/sketches/ (MEASURED, `_json_field_diffs`):

- All three: `accepted` (false in wip/), `accepted_at` and `accepted_note` (absent in wip/), `timestamp`, `deps` (added), `files_sha256.proposed_params.yaml` (R6 overlay text), K4 result, reason, measured, n_issues, cause (checks.3), K4, K5 and K8 `b_result` tallies (new B counts). `keys_read` equal in all three (the R5 a band keys were already read by S3).
- S2 only: `reported_items.3.source` (R5 e text).
- S3 only: `spec_status` (R6), K4 `by_axes.inset_plan` (result, n_issues, cause).

`--stale` at the end (MEASURED): key branch 3 records, 0 differences; deps branch 2 exempt (s1 r8, s2 r9), 1 difference "s3_checks_r7.json: deps not recorded"; X1 pass; exit 1. It stays red until an S3 record with deps is accepted (open item 1).

## 10 SHA-256 table

Committed files under docs/sketches/ (wip/ and __pycache__ excluded): 83 before the first edit, 85 after the last run (MEASURED; full lists `sha_before.txt`, `sha_after.txt` in the scratch folder).

| File | Before (first 16) | After (first 16) | On purpose |
|---|---|---|---|
| check_sketch.py | ffd7aee24aec8fb3 | 9a0e2a4d7212aad7 | yes (R1, R2, R3) |
| checks_s3.py | ef512d265a78919f | 08eef561b7ad3853 | yes (R2) |
| sketch_common.py | e9404c73e468539b | 6861ba2466231cba | yes (R4, R5) |
| sketch_loader.py | a6fec2eb3f191513 | 5118e8f9c736076b | yes (R1 e) |
| fixtures/builders.py | 097a5ec0ffeb0324 | 54602a6bd9c996d0 | yes (R1 e, R3) |
| fixtures/s3_fixtures.py | 2917ab936ed60750 | 32bfed796a33c09d | yes (R1 e) |
| fixtures/manifest.yaml | 34df7f276fdfb2e9 | f0f928e8e1b3629e | yes |
| fixtures/fast.yaml | absent | 5169811e118d10e9 | yes (new) |
| fixtures/step14_fixtures.py | absent | fd4d47dbd4add483 | yes (new) |
| proposed_params.yaml | d1413c0e6e82fc9a | 68a2b0627faa53ad | yes (R6) |
| s2_spec.yaml | b7e8bf09fa4b70e5 | ef3993811224e9cb | yes (R5 e) |
| s3_spec.yaml | ed16fda6b9d7cfcb | 015aa79edc255a44 | yes (R6, R5 a) |

Every other committed file is byte-equal (73). Unexpected differences: 0. In wip/ (not committed): `fixtures/figs/ctrl_a.png` to `ctrl_d.png` deleted on purpose.

## 11 Accept commands and expected output

No refreshed record is re-acceptable: S1 r8, S2 r9 and S3 r7 all fail K4 under rule (l) at class scope, with pixels equal. The S3 command R7 anticipated would be refused:

```
check_sketch.py --accept s3 --rev 7 --note "1.4 step 0 deps re-record (ORCH-A)"
refused: s3_checks_r7.json has checks not pass: K4 fail
```

After the P6 layouts land (S1 r9, S2 r10, S3 r8, each drawn, checked and M1-gated), the records are accepted as new revisions in the usual order, S1 first so S3-3 resolves the new certifier:

```
check_sketch.py --accept s1 --rev 9 --note "<Design Notes ref>"
check_sketch.py --accept s2 --rev 10 --note "<Design Notes ref>"
check_sketch.py s3 --rev 8          # re-run after s1 r9 is accepted, so deps name s1_checks_r9.json
check_sketch.py --accept s3 --rev 8 --note "<Design Notes ref>"
check_sketch.py --stale              # expected: key branch 0 differences; deps: s1 r9, s2 r10, s3 r8 with deps, 0 exempt in use, 0 differences
```

Expected `--accept` output (each): "copied ... SHA-256 equal" per output, "<sN>_checks_r<old>.json: superseded_by <k> (flag kept)", "accepted <sN> r<k>: note ...". Accepting S1 r9 before S3 r8 is re-run makes `--stale` read "s3_checks_r7.json: deps not recorded" (or, once S3 carries deps, "certifier superseded"); that is the DEPS-B1 behaviour.

## 12 Open items

1. Blocking for ORCH-A as written: the S3 r7 re-record cannot be accepted (K4 fail from the inset gridline firing), so `--stale` stays red on "s3_checks_r7.json: deps not recorded" until S3 r8. Orchestrator ruling needed: (a) add s3_checks_r7.json to `DEPS_EXEMPT` until S3 r8 (one-line edit, with a Design Notes entry), (b) carry `--stale` red to P6, or (c) The Designer narrows rule (l) (for example gridlines in plan views excluded) at P0D, which would leave only S1 r8 firing and S3 r7 re-acceptable.
2. The Designer signs at P0D: rule (l) class scope and the 8 firings (S1 4, S2 3, S3 1, all gridlines); the DR4-2 form rule and any numeric head half-width bound (drawn 2.38 mm, not 1.14); the S2 slot_line_c leader at exactly 1.00 mm.
3. P6 batch: S1 r9 (height_target leader; TP1.3-17 mark.z key; TP1.3-20 wingnut sweep row; S4-b holder section), S2 r10 (base_plate, slot_line_c, screw_b leaders), S3 r8 (inset screw_b leader). The same revision restores K4-Z3, Z4, Z8 to Z and the 20 re-counted K4 B to their 1.3 counts.
4. Committed `docs/sketches/fixtures/figs/ctrl_a.png` to `ctrl_d.png` and `key.json` still print the old letter mapping; nothing writes or copies them any more. Delete at ORCH-A or the Manager close (outside R3 b).
5. The Software Engineer at P0S: fast tier 103.3 s against 60 s (branch definition or worker-shared drawings, section 2); the 3 same-branch pruning candidates; the drawing cache (`draw_cache`, keyed on file SHA-256 and module fingerprints) as an R1 e speedup.
6. deps hash the spec and the script only, as R2 a states; checks_sN.py, sketch_common.py and check_stack.py are not in deps, so a harness edit does not stale a record. NOTE for P0S.
7. Rule (l) tests curved outlines edge by edge; section_xz names only its axes until S4 draws it.
8. Carried to S4 (c): TP1.3-4, -5, -9, -16, the TP1.3-6 rounds-exhausted B.

## 13 Gameplan lines to change

1. detail 1.0, `check_sketch.py` bullet (l.124)

Old:

```
- `docs/sketches/check_sketch.py sN [--rev k]`: runs K1 to K9 and the sketch's own checks, writes `docs/sketches/wip/sN_checks_r<k>.json` (per check: ID, result, measured value, threshold, Z result, B result, source tags; per file: SHA-256 of params.yaml and of the overlay, and the list of keys the spec reads with their values) and `wip/sN_summary_r<k>.md` (one screen: pass and fail per check, reported values, open items; the M2 summary Sean reads). Output rule (Design Notes 26 decision 1, `sketch_loader.output_path`): every unaccepted and verification output (sN runs, sketch PNGs, mass report, visual-gate file, `--controls` results and control figures, `--baseline`) goes to `docs/sketches/wip/` (git-ignored); only `--accept` writes to `docs/sketches/`. `check_sketch.py --accept sN --rev k --note "<Design Notes ref>"` sets accepted, accepted_note, accepted_at, copies the revision's wip/ outputs (and the wip/ controls results, control figures and baseline record when every control matched) up with SHA-256 equality, refuses on an absent record, a check not pass, an empty note, a PNG differing in pixels from an accepted one or a wip/ controls results file with any control not matched (1.2 (c) SW FIX 4, H1-Z3, H1-B6), and marks earlier accepted records of the sketch superseded_by k. `check_sketch.py --stale` compares the latest accepted, unsuperseded record per sketch with the live params and overlay and fails on any difference (`--include-unaccepted` adds the wip/ records). `check_sketch.py --baseline sN` assembles run 2 for sN (Z and B controls: H1-Z1 to H1-Z3, H1-B1 to H1-B8). `check_sketch.py --controls --jobs N` runs the manifest in N spawn worker processes (default min(cpu_count - 2, 12)), rows in manifest order, per-control id, expected, observed, reason and match equal to `--jobs 1` (1.3 step 0, RUN-Z, RUN-B; 246 controls 113 s at 12 jobs against 775 s serial on 230); `--only <id globs or check ids>` writes `wip/fixtures/controls_results_partial.json`, "PARTIAL, not a record", never read by control_tally or `--accept` (destination from the pure function `controls_dst`, RUN-Z2, RUN-B2; its call site in `controls()`, RUN-B4); an `--only` that selects nothing exits 1 (RUN-B3); runs of record use the full set; per-control equality between job counts excludes the temporary-directory path in the H1-B5 reason (Software Engineer P0S). Every sN run ends with check RPT: each id in the spec's `reported_items` ({id, text, source, needs_drawing}) has a value from `checks_sN.py reported(ctx)["items"]`, cause absent on rev 0 for needs_drawing items; the summary carries a Reported items table; s1 r7 and s2 r5 read "not declared, exempt (accepted before RPT)" by record name; `--accept` refuses through RPT and refuses any record without an RPT row; the RPT reason states its cause (RPT-Z, RPT-Z2, RPT-Z3, RPT-B1 to RPT-B6, H1-B7, H1-B8; 1.3 open O10; Software Engineer P0S FIX 2, FIX 3). `run_control` routes any `S<n>-` check to `checks_s<n>.py`; `checks_sN.py K_CHECKS` overrides the K list (1.3 open O13).
```

New:

```
- `docs/sketches/check_sketch.py sN [--rev k]`: runs K1 to K9 and the sketch's own checks, writes `docs/sketches/wip/sN_checks_r<k>.json` (per check: ID, result, measured value, threshold, Z result, B result, source tags; per file: SHA-256 of params.yaml and of the overlay, and the list of keys the spec reads with their values) and `wip/sN_summary_r<k>.md` (one screen: pass and fail per check, reported values, open items; the M2 summary Sean reads). Output rule (Design Notes 26 decision 1, `sketch_loader.output_path`): every unaccepted and verification output (sN runs, sketch PNGs, mass report, visual-gate file, `--controls` results and control figures, `--baseline`) goes to `docs/sketches/wip/` (git-ignored); only `--accept` writes to `docs/sketches/`. `check_sketch.py --accept sN --rev k --note "<Design Notes ref>"` sets accepted, accepted_note, accepted_at, copies the revision's wip/ outputs (and the wip/ controls results, control figures and baseline record when every control matched) up with SHA-256 equality, refuses on an absent record, a check not pass, an empty note, a PNG differing in pixels from an accepted one or a wip/ controls results file with any control not matched (1.2 (c) SW FIX 4, H1-Z3, H1-B6), and marks earlier accepted records of the sketch superseded_by k. `check_sketch.py --stale` compares the latest accepted, unsuperseded record per sketch with the live params and overlay and fails on any difference (`--include-unaccepted` adds the wip/ records). `check_sketch.py --baseline sN` assembles run 2 for sN (Z and B controls: H1-Z1 to H1-Z3, H1-B1 to H1-B8). `check_sketch.py --controls --jobs N` runs the manifest in N spawn worker processes (default min(cpu_count - 2, 12)), rows in manifest order, per-control id, expected, observed, reason and match equal to `--jobs 1` (1.3 step 0, RUN-Z, RUN-B; 246 controls 113 s at 12 jobs against 775 s serial on 230); `--only <id globs or check ids>` writes `wip/fixtures/controls_results_partial.json`, "PARTIAL, not a record", never read by control_tally or `--accept` (destination from the pure function `controls_dst`, RUN-Z2, RUN-B2; its call site in `controls()`, RUN-B4); an `--only` that selects nothing exits 1 (RUN-B3); runs of record use the full set; per-control equality between job counts excludes the temporary-directory path in the H1-B5 reason (Software Engineer P0S). Every sN run ends with check RPT: each id in the spec's `reported_items` ({id, text, source, needs_drawing}) has a value from `checks_sN.py reported(ctx)["items"]`, cause absent on rev 0 for needs_drawing items; the summary carries a Reported items table; s1 r7 and s2 r5 read "not declared, exempt (accepted before RPT)" by record name; `--accept` refuses through RPT and refuses any record without an RPT row; the RPT reason states its cause (RPT-Z, RPT-Z2, RPT-Z3, RPT-B1 to RPT-B6, H1-B7, H1-B8; 1.3 open O10; Software Engineer P0S FIX 2, FIX 3). `run_control` routes any `S<n>-` check to `checks_s<n>.py`; `checks_sN.py K_CHECKS` overrides the K list (1.3 open O13). 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md`): `--controls` submits tasks longest first by the last run's seconds, and the YAML parse (`sketch_loader.load_yaml`) and the unmutated live drawings (`fixtures/builders.draw_cache`) are cached per worker, a fresh copy per call (rows equal to the uncached run on id, expected, observed, reason and match; 413 controls 225.7 s to 128.4 s at 12 jobs); `--controls --fast` runs the fast tier `fixtures/fast.yaml` (every check family's least-time Z and one B per branch, a branch being the manifest finding that added the B) to the partial destination, PARTIAL, not a record (FAST-Z, FAST-B1, FAST-B2, RUN-Z3); every sN run writes `deps` (spec and script {path, sha256}; certifiers {sketch, path, rev, sha256} for every accepted record a check resolved at run time, S3-3 today), `--accept` copies it unchanged, and `--stale` gains a deps branch: spec and script SHA-256 recomputed, each certifier the latest accepted, unsuperseded record at the recorded name and SHA-256, and a record without deps fails unless named in `DEPS_EXEMPT` (s1_checks_r8.json, s2_checks_r9.json) (DEPS-Z, DEPS-Z2, DEPS-B1 to B6); `check_sketch.py --m1-controls --out <dir> --key <path>` draws the four reviewer control figures as `m1c_<token>.png` with fresh `secrets.token_hex(3)` tokens and writes the key (token, role, criterion, expected verdict) to <path>, refusing a non-empty <dir>, a <path> inside the project root and a <path> inside <dir>; `--controls` and `--accept` write and copy no control figure (M1C-Z, M1C-Z2, M1C-B1 to B4).
```

2. detail 1.0, K table, K4 row (l.138)

Old:

```
| K4 | Labels carry their dimension (8.4.2): each spec row with `label` has one annotation containing its name and the number formatted from its key; a label number that differs from the key value fails; from S2 and S1 r5 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part; only a revision accepted before the rule with no not_drawn entry is exempt (1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1); every label leader ends on its row's ink within 0.05 and no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5); labels draw above every area (z order 100); no area artist (filled or hatched) of another row is drawn above a leader where it runs or above the row's ink at the anchor; at most a quarter of the samples in the last quarter of a leader lie in other rows' hatch, and place_labels re-anchors on the row's ink until it holds (1.2 (h) r3, Designer M1 S2 r2 F1, S1 r6 F1); red-first for K4-B9 to B11 MEASURED by branch deletion (Designer sign-off r3); a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking; left-column text clear of the y tick labels); (e) only true outlines of rows higher than the labelled row by more than 0.05 (zones: every outline) count; (e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink where no cover contains it) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor; (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that does not enclose the anchor (Design Notes 30; Designer P1Rd FIX D1); an outline encloses for (e1) and (e2) only when the anchor and every point within 0.05 of it lie inside its outer boundary with holes filled (Topologist TP1.3-8); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back; (g) the drawn label of a wholly hidden row contains "under " and the name of a counted row whose outline contains or encloses the anchor; (h) any two plan leaders that do not cross, anchor ends included, keep at least 4.0 mm apart (DECLARED, Designer P1Rf re-check FIX D4), judged and placed as a crossing is | Fixture with all labels from keys; K4-Z2 live S2; K4-Z3 live S2 drawn by s2_plan.py; K4-Z4 live S1 drawn by s1_side_poses.py; K4-Z5 S3 span_lt label prints its expr value 870 | B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note; K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1); K4-B7 sightline leader at the r1 anchor, off the line; K4-B8 r1 concentric anchors, three crossings; K4-B9 S1 core 750 at the r6 anchor (end in hatch); K4-B10 an area drawn over a leader; K4-B11 an area of another row over an anchor (with (e1) on the hidden ink); K4-B12 the descent-stop leader at the r4/r5 anchor (inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B14 ring label at the r6 anchor on hidden rim inside tie a (e1); K4-B15 drill_head label without its "under ring gear" suffix (g); K4-B16 gear outline planted as an open C, not enclosing the cutter anchor (e2, g); K4-B17 ring label anchored 0.028 mm outside tie a, last quarter 41.3 mm inside it (TP1.3-8); K4-B18 tie a label anchored on its phantom line under a planted nearer disk (e1, Designer FIX D5); K4-B19 the S2 r7 tube OD, base plate and cutter leaders, 1.87 mm apart (h, Designer FIX D4); K4-B8 re-planted at 1.3 P1R and P1Rf; K4-B7, B8, B10 to B12, B14 counts re-read at P1R to P1Rf2; K4-B20 span_lt label prints its key value 1150 where the spec names expr (1.3 P4: a label prints label.expr, a label.value_from spec value, or for fmt s the key's string value); K4-Z6 and K4-B21 load_tension_c value_from 254.04 against a printed 300; K4-B22 a label drawn outside its home Axes, refused (1.3 P5f); (i) on a script-drawn figure no drawn leader crosses a text box and no two text boxes overlap (labels, notes, tick labels, titles; boxes shrunk 1 px): K4-B23 text planted on two leaders, K4-B24 text planted on a label (1.3 (h) r2, Designer M1 S3 r1 F2, F3); K4-B7, B8, B18 re-counted 4, 7, 3; (j) a label printing a load reads checks_s3.loads() from the keys (load_comp_c cases, load_tension_c), and every load_cases per_screw literal agrees with loads() within 0.005 N (K4-Z7, Z8, B25 static 79, B26 ring.mass + 4 kg); (k) a row declaring label_anchor_frac ends its leader at that anchor, frac in [0, 1] (K4-B27, B28); (l) section views: no leader runs within 2 deg and 1.0 mm of a reference line or gridline over more than 5 mm (K4-B29, B30); (m) a stack_z label prints check_stack nut_z at its pose within 0.05 (K4-B31) (M1 S3 r4 F1, r5 Rule 1, Rule 2, F1, F2; 1.3 (h) r5, r6; rules (j) to (m) signed by the r6 fresh M1 reviewer, s3_visual_gate_r6.md; (l) covers reference lines and gridlines only, part edges and the S1/S2 views carried, Manager 1.3 close) |
```

New:

```
| K4 | Labels carry their dimension (8.4.2): each spec row with `label` has one annotation containing its name and the number formatted from its key; a label number that differs from the key value fails; from S2 and S1 r5 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part; only a revision accepted before the rule with no not_drawn entry is exempt (1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1); every label leader ends on its row's ink within 0.05 and no two leaders cross; a concentric row may set label_theta, the leader azimuth (1.2 (h), Designer M1 r1 F4, F5); labels draw above every area (z order 100); no area artist (filled or hatched) of another row is drawn above a leader where it runs or above the row's ink at the anchor; at most a quarter of the samples in the last quarter of a leader lie in other rows' hatch, and place_labels re-anchors on the row's ink until it holds (1.2 (h) r3, Designer M1 S2 r2 F1, S1 r6 F1); red-first for K4-B9 to B11 MEASURED by branch deletion (Designer sign-off r3); a row may set label_side: left, a left label column under the same rules (1.2 (h) r4, Designer M1 S2 r3 N1); 1.3 P1R: plan labels are placed by one placer (sketch_common.place_plan_labels; candidates in order: label_side column then the other, label_theta ray hit, column default anchor, ink samples at most 2 mm apart; first candidate passing every leader rule, re-judged after column stacking; left-column text clear of the y tick labels); (e) only true outlines of rows higher than the labelled row by more than 0.05 (zones: every outline) count; (e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink where no cover contains it) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor; (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that does not enclose the anchor (Design Notes 30; Designer P1Rd FIX D1); an outline encloses for (e1) and (e2) only when the anchor and every point within 0.05 of it lie inside its outer boundary with holes filled (Topologist TP1.3-8); (f) a label with no passing candidate is recorded UNPLACEABLE with its candidate table in the K4 record and fails with reason "unplaceable", no silent fall-back; (g) the drawn label of a wholly hidden row contains "under " and the name of a counted row whose outline contains or encloses the anchor; (h) any two plan leaders that do not cross, anchor ends included, keep at least 4.0 mm apart (DECLARED, Designer P1Rf re-check FIX D4), judged and placed as a crossing is | Fixture with all labels from keys; K4-Z2 live S2; K4-Z3 live S2 drawn by s2_plan.py; K4-Z4 live S1 drawn by s1_side_poses.py; K4-Z5 S3 span_lt label prints its expr value 870 | B1 label without a number; B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note; K4-B6 S1 r5 spec with not_drawn and no figure_note (FIX R1); K4-B7 sightline leader at the r1 anchor, off the line; K4-B8 r1 concentric anchors, three crossings; K4-B9 S1 core 750 at the r6 anchor (end in hatch); K4-B10 an area drawn over a leader; K4-B11 an area of another row over an anchor (with (e1) on the hidden ink); K4-B12 the descent-stop leader at the r4/r5 anchor (inside tie b); K4-B13 a pad under an opaque lid (unplaceable); K4-B14 ring label at the r6 anchor on hidden rim inside tie a (e1); K4-B15 drill_head label without its "under ring gear" suffix (g); K4-B16 gear outline planted as an open C, not enclosing the cutter anchor (e2, g); K4-B17 ring label anchored 0.028 mm outside tie a, last quarter 41.3 mm inside it (TP1.3-8); K4-B18 tie a label anchored on its phantom line under a planted nearer disk (e1, Designer FIX D5); K4-B19 the S2 r7 tube OD, base plate and cutter leaders, 1.87 mm apart (h, Designer FIX D4); K4-B8 re-planted at 1.3 P1R and P1Rf; K4-B7, B8, B10 to B12, B14 counts re-read at P1R to P1Rf2; K4-B20 span_lt label prints its key value 1150 where the spec names expr (1.3 P4: a label prints label.expr, a label.value_from spec value, or for fmt s the key's string value); K4-Z6 and K4-B21 load_tension_c value_from 254.04 against a printed 300; K4-B22 a label drawn outside its home Axes, refused (1.3 P5f); (i) on a script-drawn figure no drawn leader crosses a text box and no two text boxes overlap (labels, notes, tick labels, titles; boxes shrunk 1 px): K4-B23 text planted on two leaders, K4-B24 text planted on a label (1.3 (h) r2, Designer M1 S3 r1 F2, F3); K4-B7, B8, B18 re-counted 4, 7, 3; (j) a label printing a load reads checks_s3.loads() from the keys (load_comp_c cases, load_tension_c), and every load_cases per_screw literal agrees with loads() within 0.005 N, every number of a stall literal '<v1> / <v2> (mu <m1> / <m2>)' held to F_stall at its mu (K4-Z7, Z8, B25 static 79, B26 ring.mass + 4 kg; 1.4 step 0 K4-B37); (k) a row declaring label_anchor_frac ends its leader at that anchor, frac in [0, 1] (K4-B27, B28); (l) in every view (side, plan, section) and every declared Axes of a script-drawn figure, no leader (clipped to the Axes box) runs within 2 deg and 1.0 mm of a line of the families reference line, gridline (major and minor) or part edge (every edge of every tagged area artist of another row, counted only where drawn: a renderer piece inside its clip path) over more than 5 mm (K4-B29, B30; 1.4 step 0, C1.3-a: K4-Z9 to Z11, K4-B32 to B36; K4-Z3, Z4, Z8 re-scoped to B as the live red of S2 r9, S1 r8, S3 r7); (m) a stack_z label prints check_stack nut_z at its pose within 0.05 (K4-B31) (M1 S3 r4 F1, r5 Rule 1, Rule 2, F1, F2; 1.3 (h) r5, r6; rules (j) to (m) signed by the r6 fresh M1 reviewer, s3_visual_gate_r6.md; (l) at class scope from 1.4 step 0, The Designer signs at P0D) |
```

3. detail 1.0, K table control pointer paragraph (l.147)

Old:

```
The K table lists the controls the gameplan requires. The Step 1.0 revision added K3-B7, K4-B3, K5-B4, K5-B5, K6-Z2, K6-B4, K7-Z5 to Z7, K7-B7 to B10, K8-Z2, K8-B4 to B11, K9-B3, K9-B4 and the smoke control S1-FULL. Step 1.1 (b) added K6-Z3, K6-B5, K6-B6 (LF-16), K7-Z8, K7-Z9, K7-Z10, K7-B11, K7-B12, K7-B13, K8-Z3, K8-B12, K8-B13, S1-4-Z, S1-4-B1, S1-5b-Z and S1-5b-B1. Step 1.1 (c) added the S1-x fixtures from the signed spec (H6): S1-1-Z, S1-1-B1, S1-1-B2, S1-2-Z, S1-2-B1, S1-2-B2, S1-3-Z, S1-3-B1, S1-4-B2, S1-5a-Z, S1-5a-B1, S1-6-Z, S1-6-B1, S1-7-Z and S1-7-B1 (99 controls: Z 30, B 68, smoke 1). Step 1.1 (h) r2 added K5-Z2, K5-B6, K6-B7, K7-B14, K7-B15, K8-Z4, K8-B14, K9-Z2, K9-B5 (108); r3 added K7-Z11, K7-B16 to K7-B19 (113); r4 added K8-Z5, K7-B20, K8-B15, K8-B16 and re-scoped K8-B7 to planted 3 (117 controls: Z 35, B 81, smoke 1; Manager re-run from `docs/sketches/` at the 1.1 close: 117/117 matched). Step 1.2 step 0 added H1-Z1, H1-Z2, H1-B1 to H1-B5 (`--accept`, `--stale` supersession) and H5-Z, H5-B (park-rule symbol c) (126 controls: Z 38, B 87, smoke 1). Step 1.2 (b) fix pass added K8-B17, K7-B21 (128). Step 1.2 (c) added K4-Z2, K4-B4, K4-B5, K5-Z3, K5-B7 to B11, K6-Z4, K6-B8, K6-B9, K7-Z12 to Z15, K7-B22 to B29, K8-Z6, K8-B18 to B23, K9-Z3, X1-Z, X1-B1, X1-B2, S2-1-Z to S2-6-B1 (14) and the smoke control S2-FULL (178 controls: Z 55, B 121, smoke 2; 264 s). Step 1.2 (c) fix pass P5f (Designer FIX R1, Loftsman LF-c1, Topologist TP1.2-1, Software Engineer FIX 1 to 5; `research/sean/cr_scratch/step1.2_engineer_redfirst_fixes.md`) added K4-B6, K5-B12, K5-B13, K7-B30, K7-B31, K8-B24 to B28, S2-6-B2, H1-Z3 and H1-B6 (191 controls: Z 56, B 133, smoke 2; 295 s). Step 1.2 (h) r2 (`research/sean/cr_scratch/step1.2_engineer_revision_r2.md`) added K3-Z2, K3-Z3, K3-B8, K3-B9, K4-Z3, K4-B7, K4-B8, K5-B14 to B16, K9-B6, K8-Z7, K8-B29 to B33, K7-Z16, K7-Z17, K7-B32, K7-B33, S2-5b-B2, S2-5b-B3 (214 controls: Z 62, B 150, smoke 2; 1640 s). Step 1.2 (h) r3 (`research/sean/cr_scratch/step1.2_engineer_revision_r3.md`) added K8-Z8, K8-B34 to B36, K4-Z4, K4-B9 to B11 (222 controls: Z 64, B 156, smoke 2; 446 s). Step 1.2 (h) r4 (`research/sean/cr_scratch/step1.2_engineer_revision_r4.md`) added K8-B37 to B41, K5-B17, K5-B18, K9-B7 (230 controls: Z 64, B 164, smoke 2; 734 s). Step 1.3 step 0 (`research/sean/cr_scratch/step1.3_engineer_step0.md`) added RUN-Z, RUN-B, K2-Z2, K2-B4, K2-B5, K6-B10, K6-B11, RPT-Z, RPT-B1, RPT-B2, H1-B7, H1-B8, K5-B19, K8-B42, K8-B43, K7-B34 (246 controls: Z 67, B 177, smoke 2; 113 s at --jobs 12, 804.3 s at --jobs 1). Step 1.3 P0f (`research/sean/cr_scratch/step1.3_engineer_step0_fixes.md`) and its addendum added K2-B6, K2-B7, K5-B20 to B24, RUN-Z2, RUN-B2, RUN-B3, RUN-B4, RPT-Z2, RPT-Z3, RPT-B3 to B6 and re-planted H1-B8 (263 controls: Z 70, B 191, smoke 2; 111 s at --jobs 12). Step 1.3 P1R, P1Rf and P1Rf2 (`research/sean/cr_scratch/step1.3_engineer_renderer.md`, `step1.3_engineer_renderer_fixes.md`) added K8-Z9 to Z13, K8-B44 to B52, K4-B12 to B19, re-planted K4-B8 and re-counted K8-B6, B32, B39, B49, K4-B7, B10, B11, B12, B14 (285 controls: Z 75, B 208, smoke 2, all match; 121.9 s at --jobs 12). Step 1.3 (c) P4 (research/sean/cr_scratch/step1.3_engineer_redfirst.md) added K3-Z4, K3-B10, K4-Z5, K4-B20, K5-Z4, K5-Z5, K5-B25 to B35, K6-Z5, K8-Z14, K8-B53 to B63, K9-Z4, K9-Z5, K9-B8, K9-B9, S3-1-Z, S3-1-B1, S3-1-B2, S3-2-Z, S3-2-Z2, S3-2-B1, S3-3-Z, S3-3-B1 to B3, SYM-Z, SYM-B1 to B3, X1-B3, H1-B9 and the smoke control S3-FULL (fixtures/s3_fixtures.py; 336 controls: Z 88, B 245, smoke 3, all match; 148.4 s at --jobs 12). Step 1.3 P5f (research/sean/cr_scratch/step1.3_engineer_redfirst_fixes.md; Software Engineer FIX 1 to 5, Loftsman FIX 1 to 6, Topologist FIX 1 to 7) added K3-B11, K4-Z6, K4-B21, K4-B22, K5-B36, K7-Z18, K7-B35, K8-Z15, K8-B64 to B76, S3-2-B2, S3-3-B4 to B11, SYM-P-Z, SYM-P-B1 (368 controls: Z 92, B 273, smoke 3, all match; 157.6 s at --jobs 12). Step 1.3 (h) r2 (research/sean/cr_scratch/step1.3_engineer_revision_r2.md) added K4-B23, B24, K5-Z6, Z7, B37 to B42, K8-Z16, B77 to B85, S3-3-B12 to B15, re-planted K4-B7, B8, B18, K8-B54, B55, S3-3-B2 to B4, B7 to B9, and the fixture stand-ins for the two Designer-pending items (392 controls: Z 95, B 294, smoke 3, all match; 187.7 s at --jobs 12). Step 1.3 (h) r3 (research/sean/cr_scratch/step1.3_engineer_revision_r3.md) added K5-B43 to B47, K8-B86, B87, S3-3-B16, B17, removed the fixture stand-ins, re-planted K4-Z6 and B21 at 247.5 (W 26.25 kg) and K8-B83 on the rear nut shoulder screw entry, re-read K5-B41 (2) and K8-B81 (line family) (401 controls: Z 95, B 303, smoke 3, all match; 191.8 s at --jobs 12). Step 1.3 (h) r4 added K8-Z17, B88, B89 and re-worded K4-B20, K8-B79, B80 (404 controls: Z 96, B 305, smoke 3, all match; 196.5 s at --jobs 12). Step 1.3 (h) r5 added K4-Z7, B25 (406 controls: Z 97, B 306, smoke 3, all match; 197.1 s at --jobs 12). Step 1.3 (h) r6 added K4-Z8, B26 to B31 (413 controls: Z 98, B 312, smoke 3, all match; 211.1 s at --jobs 12); r7 added none (413/413, 225.7 s). Step 1.3 P6 (research/sean/cr_scratch/step1.3_engineer_draw_r1.md) removed the S3 fixture scaffolding (p4_spec_findings, _receiver_cert, _plate_g, _post_p6_specs, pre-P4 fallback), redefined S3-3-B9 (shoulder seat 1 up), re-planted K5-B20 (mark line), H1-B9, S3-3-B3 (11), K7-B19, K4-B6, K3-B8 and showed the 17 (b) dry-run controls at their declared results (368 controls, all match; 160.9 s at --jobs 12). `docs/sketches/fixtures/manifest.yaml` is the executable record of every control, with reason substrings and planted issue counts.
```

New:

```
The K table lists the controls the gameplan requires. The Step 1.0 revision added K3-B7, K4-B3, K5-B4, K5-B5, K6-Z2, K6-B4, K7-Z5 to Z7, K7-B7 to B10, K8-Z2, K8-B4 to B11, K9-B3, K9-B4 and the smoke control S1-FULL. Step 1.1 (b) added K6-Z3, K6-B5, K6-B6 (LF-16), K7-Z8, K7-Z9, K7-Z10, K7-B11, K7-B12, K7-B13, K8-Z3, K8-B12, K8-B13, S1-4-Z, S1-4-B1, S1-5b-Z and S1-5b-B1. Step 1.1 (c) added the S1-x fixtures from the signed spec (H6): S1-1-Z, S1-1-B1, S1-1-B2, S1-2-Z, S1-2-B1, S1-2-B2, S1-3-Z, S1-3-B1, S1-4-B2, S1-5a-Z, S1-5a-B1, S1-6-Z, S1-6-B1, S1-7-Z and S1-7-B1 (99 controls: Z 30, B 68, smoke 1). Step 1.1 (h) r2 added K5-Z2, K5-B6, K6-B7, K7-B14, K7-B15, K8-Z4, K8-B14, K9-Z2, K9-B5 (108); r3 added K7-Z11, K7-B16 to K7-B19 (113); r4 added K8-Z5, K7-B20, K8-B15, K8-B16 and re-scoped K8-B7 to planted 3 (117 controls: Z 35, B 81, smoke 1; Manager re-run from `docs/sketches/` at the 1.1 close: 117/117 matched). Step 1.2 step 0 added H1-Z1, H1-Z2, H1-B1 to H1-B5 (`--accept`, `--stale` supersession) and H5-Z, H5-B (park-rule symbol c) (126 controls: Z 38, B 87, smoke 1). Step 1.2 (b) fix pass added K8-B17, K7-B21 (128). Step 1.2 (c) added K4-Z2, K4-B4, K4-B5, K5-Z3, K5-B7 to B11, K6-Z4, K6-B8, K6-B9, K7-Z12 to Z15, K7-B22 to B29, K8-Z6, K8-B18 to B23, K9-Z3, X1-Z, X1-B1, X1-B2, S2-1-Z to S2-6-B1 (14) and the smoke control S2-FULL (178 controls: Z 55, B 121, smoke 2; 264 s). Step 1.2 (c) fix pass P5f (Designer FIX R1, Loftsman LF-c1, Topologist TP1.2-1, Software Engineer FIX 1 to 5; `research/sean/cr_scratch/step1.2_engineer_redfirst_fixes.md`) added K4-B6, K5-B12, K5-B13, K7-B30, K7-B31, K8-B24 to B28, S2-6-B2, H1-Z3 and H1-B6 (191 controls: Z 56, B 133, smoke 2; 295 s). Step 1.2 (h) r2 (`research/sean/cr_scratch/step1.2_engineer_revision_r2.md`) added K3-Z2, K3-Z3, K3-B8, K3-B9, K4-Z3, K4-B7, K4-B8, K5-B14 to B16, K9-B6, K8-Z7, K8-B29 to B33, K7-Z16, K7-Z17, K7-B32, K7-B33, S2-5b-B2, S2-5b-B3 (214 controls: Z 62, B 150, smoke 2; 1640 s). Step 1.2 (h) r3 (`research/sean/cr_scratch/step1.2_engineer_revision_r3.md`) added K8-Z8, K8-B34 to B36, K4-Z4, K4-B9 to B11 (222 controls: Z 64, B 156, smoke 2; 446 s). Step 1.2 (h) r4 (`research/sean/cr_scratch/step1.2_engineer_revision_r4.md`) added K8-B37 to B41, K5-B17, K5-B18, K9-B7 (230 controls: Z 64, B 164, smoke 2; 734 s). Step 1.3 step 0 (`research/sean/cr_scratch/step1.3_engineer_step0.md`) added RUN-Z, RUN-B, K2-Z2, K2-B4, K2-B5, K6-B10, K6-B11, RPT-Z, RPT-B1, RPT-B2, H1-B7, H1-B8, K5-B19, K8-B42, K8-B43, K7-B34 (246 controls: Z 67, B 177, smoke 2; 113 s at --jobs 12, 804.3 s at --jobs 1). Step 1.3 P0f (`research/sean/cr_scratch/step1.3_engineer_step0_fixes.md`) and its addendum added K2-B6, K2-B7, K5-B20 to B24, RUN-Z2, RUN-B2, RUN-B3, RUN-B4, RPT-Z2, RPT-Z3, RPT-B3 to B6 and re-planted H1-B8 (263 controls: Z 70, B 191, smoke 2; 111 s at --jobs 12). Step 1.3 P1R, P1Rf and P1Rf2 (`research/sean/cr_scratch/step1.3_engineer_renderer.md`, `step1.3_engineer_renderer_fixes.md`) added K8-Z9 to Z13, K8-B44 to B52, K4-B12 to B19, re-planted K4-B8 and re-counted K8-B6, B32, B39, B49, K4-B7, B10, B11, B12, B14 (285 controls: Z 75, B 208, smoke 2, all match; 121.9 s at --jobs 12). Step 1.3 (c) P4 (research/sean/cr_scratch/step1.3_engineer_redfirst.md) added K3-Z4, K3-B10, K4-Z5, K4-B20, K5-Z4, K5-Z5, K5-B25 to B35, K6-Z5, K8-Z14, K8-B53 to B63, K9-Z4, K9-Z5, K9-B8, K9-B9, S3-1-Z, S3-1-B1, S3-1-B2, S3-2-Z, S3-2-Z2, S3-2-B1, S3-3-Z, S3-3-B1 to B3, SYM-Z, SYM-B1 to B3, X1-B3, H1-B9 and the smoke control S3-FULL (fixtures/s3_fixtures.py; 336 controls: Z 88, B 245, smoke 3, all match; 148.4 s at --jobs 12). Step 1.3 P5f (research/sean/cr_scratch/step1.3_engineer_redfirst_fixes.md; Software Engineer FIX 1 to 5, Loftsman FIX 1 to 6, Topologist FIX 1 to 7) added K3-B11, K4-Z6, K4-B21, K4-B22, K5-B36, K7-Z18, K7-B35, K8-Z15, K8-B64 to B76, S3-2-B2, S3-3-B4 to B11, SYM-P-Z, SYM-P-B1 (368 controls: Z 92, B 273, smoke 3, all match; 157.6 s at --jobs 12). Step 1.3 (h) r2 (research/sean/cr_scratch/step1.3_engineer_revision_r2.md) added K4-B23, B24, K5-Z6, Z7, B37 to B42, K8-Z16, B77 to B85, S3-3-B12 to B15, re-planted K4-B7, B8, B18, K8-B54, B55, S3-3-B2 to B4, B7 to B9, and the fixture stand-ins for the two Designer-pending items (392 controls: Z 95, B 294, smoke 3, all match; 187.7 s at --jobs 12). Step 1.3 (h) r3 (research/sean/cr_scratch/step1.3_engineer_revision_r3.md) added K5-B43 to B47, K8-B86, B87, S3-3-B16, B17, removed the fixture stand-ins, re-planted K4-Z6 and B21 at 247.5 (W 26.25 kg) and K8-B83 on the rear nut shoulder screw entry, re-read K5-B41 (2) and K8-B81 (line family) (401 controls: Z 95, B 303, smoke 3, all match; 191.8 s at --jobs 12). Step 1.3 (h) r4 added K8-Z17, B88, B89 and re-worded K4-B20, K8-B79, B80 (404 controls: Z 96, B 305, smoke 3, all match; 196.5 s at --jobs 12). Step 1.3 (h) r5 added K4-Z7, B25 (406 controls: Z 97, B 306, smoke 3, all match; 197.1 s at --jobs 12). Step 1.3 (h) r6 added K4-Z8, B26 to B31 (413 controls: Z 98, B 312, smoke 3, all match; 211.1 s at --jobs 12); r7 added none (413/413, 225.7 s). Step 1.3 P6 (research/sean/cr_scratch/step1.3_engineer_draw_r1.md) removed the S3 fixture scaffolding (p4_spec_findings, _receiver_cert, _plate_g, _post_p6_specs, pre-P4 fallback), redefined S3-3-B9 (shoulder seat 1 up), re-planted K5-B20 (mark line), H1-B9, S3-3-B3 (11), K7-B19, K4-B6, K3-B8 and showed the 17 (b) dry-run controls at their declared results (368 controls, all match; 160.9 s at --jobs 12). `docs/sketches/fixtures/manifest.yaml` is the executable record of every control, with reason substrings and planted issue counts. Step 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md`) added RUN-Z3, FAST-Z, FAST-B1, FAST-B2, DEPS-Z, DEPS-Z2, DEPS-B1 to B6, M1C-Z, M1C-Z2, M1C-B1 to B4, K4-Z9 to Z11, K4-B32 to B37, K8-B90 to B92 and K5-B48, re-scoped K4-Z3, Z4, Z8 from Z to B (the live S2 r9, S1 r8 and S3 r7 red under rule (l) at class scope; back to Z at P6), re-counted K4-B7 to B12, B14 to B19, B23, B24 and B26 to B31 for the live rule (l) firings and removed the control figures from `--controls` (444 controls: Z 104, B 337, smoke 3, all match; 128.5 s at --jobs 12; fast tier `fixtures/fast.yaml` 314 controls, 103.3 s, PARTIAL, not a record).
```

4. Design Notes 25, row C1.3-a (l.705)

Old:

```
| C1.3-a (carried at the 1.3 close) | K4 rule (l) leader collinearity: (1) global scope, S1 and S2 side and plan views (dry-run fires on S1 r8 height_target leader along the z 2000 gridline; landing it opens S1 r9); (2) part-edge extension in section views (s3_visual_gate_r6.md N1: add every tagged artist edge except the label's own row; live r6 fires 2, r7 clean, MEASURED by the reviewer) | 1.4 (S4) step 0, before the S4 draw; S1 r9 only if Sean takes (1) | The Engineer; The Designer signs; Sean on (1) |
```

New:

```
| C1.3-a (carried at the 1.3 close) | K4 rule (l) leader collinearity: (1) global scope, S1 and S2 side and plan views (dry-run fires on S1 r8 height_target leader along the z 2000 gridline; landing it opens S1 r9); (2) part-edge extension in section views (s3_visual_gate_r6.md N1: add every tagged artist edge except the label's own row; live r6 fires 2, r7 clean, MEASURED by the reviewer) ; 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md`): implemented at class scope (reference lines, gridlines, part edges; side, plan, section; every declared Axes; K4-Z9 to Z11, K4-B32 to B36); dry run on the drawings of record fires S1 r8 4 (height_target on the z 2000 gridline, each pose), S2 r9 3 (plan gridlines y 0, y 260, y 80), S3 r7 1 (inset gridline y 80), part edges and reference lines 0; firings go to the P6 batch (S1 r9, S2 r10, S3 r8) | 1.4 (S4) step 0, before the S4 draw; S1 r9, S2 r10, S3 r8 at P6 | The Engineer; The Designer signs (P0D); Sean on (1) |
```

5. Design Notes 25, row C1.3-b (l.706)

Old:

```
| C1.3-b | Loftsman NOTE LF1.3-11 (S2 spec source text still names r7) and LF1.3-12 (anchor faces measured against a bearing drawn solid); Topologist NOTE R2-6 (not_drawn literal x bands for pinions and base frame, margins 5.09 and 22.00, out of --stale reach) and R2-7 (arc a1 plan-only branch reachable only by a spec plant, no B); Designer DR4-2 (terminator relief bounds arrow position, not head width or connection style); r6 reviewer NOTE on rule (j) (only the first figure of a stall literal is held; 282.21 unheld); N2 ticks named in five S3 shape strings and not drawn; N4 stale W comment | 1.4 (S4) step 0 (harness items); S6 (ticks); Step 2 (LF1.3-12 bearing row) | The Engineer; raisers re-check |
```

New:

```
| C1.3-b | Loftsman NOTE LF1.3-11 (S2 spec source text still names r7) and LF1.3-12 (anchor faces measured against a bearing drawn solid); Topologist NOTE R2-6 (not_drawn literal x bands for pinions and base frame, margins 5.09 and 22.00, out of --stale reach) and R2-7 (arc a1 plan-only branch reachable only by a spec plant, no B); Designer DR4-2 (terminator relief bounds arrow position, not head width or connection style); r6 reviewer NOTE on rule (j) (only the first figure of a stall literal is held; 282.21 unheld); N2 ticks named in five S3 shape strings and not drawn; N4 stale W comment ; 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md` section 6): R2-6 bands as key expressions with a literal lint (K8-B90), R2-7 B (K5-B48), DR4-2 straight connection and the signed terminator style (K8-B91, B92; numeric half-width bound to The Designer, live 2.38 mm), rule (j) every number of a stall literal (K4-B37), LF1.3-11 text corrected, N4 already corrected at 1.3 r7; LF1.3-12 to Step 2; N2 ticks to S6 | 1.4 (S4) step 0 (harness items); S6 (ticks); Step 2 (LF1.3-12 bearing row) | The Engineer; raisers re-check |
```

6. detail 1 common, Control blinding paragraph (l.196)

Old:

```
Control blinding (Manager, 1.3 close; for Sean at the 1.3 gate): the expected control outcomes live only in `key.json` and in an orchestrator-only section of the open file that no reviewer prompt points to; the M1 spawn receives the prompt text itself, never a line range of the open file. The 1.1 to 1.3 open files print the mapping (ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS, ctrl_d FAIL), so S4 step 0 re-letters the control figures under a new `key.json` (orchestrator only) before the first S4 M1; until then a control result read with the key in view earns no model credit (Step 1.3: control credit void, sketch verdicts stand).
```

New:

```
Control blinding (Manager, 1.3 close; for Sean at the 1.3 gate): the expected control outcomes live only in `key.json` and in an orchestrator-only section of the open file that no reviewer prompt points to; the M1 spawn receives the prompt text itself, never a line range of the open file. The 1.1 to 1.3 open files print the mapping (ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS, ctrl_d FAIL), so S4 step 0 re-letters the control figures under a new `key.json` (orchestrator only) before the first S4 M1; until then a control result read with the key in view earns no model credit (Step 1.3: control credit void, sketch verdicts stand). 1.4 step 0: the re-lettering is replaced by `check_sketch.py --m1-controls` (fresh random tokens per round, key written outside the project root; `builders.control_figures` returns figures by role and names no file); `--controls` writes no control figure.
```
