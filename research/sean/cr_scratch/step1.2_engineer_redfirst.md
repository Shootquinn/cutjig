## Corrections to the brief

1. **The signed S2 spec failed K6 on its own stack fields.** `load_plane` and `entry_plane` name `core_seat` and `collar`, which are S1 rows. The 1.1 LF-16 lint reports "feature has no z_rule in any pose" twice on any S2 run (MEASURED, pre-change K6 on the live S2 drawing). The lint is relaxed by an owner rule: a plane whose feature is not a row of this spec is linted where the row is drawn. Its premise is that a spec with that row carries the same field, equal after whitespace normalisation. Z is K6-Z4 and B is K6-B9 (rule 1f). The spec is unchanged.
2. **One spec edit at (c): the S2 `gear` row gains `section: ["gear.bore / 2", "gear.od / 2"]`.** Without it the gear's plan outline is the depth-band disk r 126.32 (DERIVED). That disk is a containment bound, so gear|gear_hub C cannot pass as a contact on true sections, and gear|drill_tube F overlaps the tube disk. No key, class or row changes. `section` is outside the X1 field list (S1 has no gear section). The spec `status` line now reads "signed ...; 1.2 (c) gear section field added". The edit is awaiting the Loftsman and the Designer (section 7).
3. **S2-5a least clearance: 11.71 on the plan outline, 15.69 on the drawn part.** The lift motor drawn as its 42 square, faces radial and tangential, sits 160 sin 15 - 21 (cos 15 + sin 15) = 41.41 - 25.72 = **15.69** from the sector edge (DERIVED; pre-change S2-5a MEASURED 15.69). The gameplan Z value 11.71 is the circumscribing circle, 41.41 - 29.70 (DERIVED). S2-5a and S2-5b now measure each part's plan outline, the spec footprint that K8 holds around the drawn part, against the drawn sector. They read 11.71 (MEASURED). A part drawn narrower than its footprint therefore cannot pass S2-5a. The drawn sector is held equal to the spec wedge by K8 (K8-B23).
4. **`artist_polys` read Bezier control points as vertices.** A Circle path's polygon reached 100.041 for r 100 and 210.086 for r 210 (MEASURED). That broke plan containment at TOL_Z 0.05 and gave tangent contacts a false lens overlap. Curves are now sampled on the curve (`flatten_path`, 8 points per segment; matplotlib's 8-segment circle is within 4e-6 r). All 128 prior controls still match (section 4).
5. **The (b) skeleton S2 checks were correct except S2-3.** On the pre-change code, S2-1, S2-2, S2-4, S2-5a, S2-5b and S2-6 each read clean on Z and fired on B with the planted count (MEASURED, section 1 table B). Only S2-3 was red on Z: no drawn pitch point.
6. **Pre-change K9 fires on a figure-note Text.** A Text with a gid that is not a row reads as "tagged artist ... has no spec row" (pre-change K9-Z3). Texts with gid `note:` are now skipped, as `label:` texts already were.
7. **K7-Z12 and K7-B22 match on the pre-change code.** The 1.0 plan path already reads F distance and overlap on drawn pieces. They are kept as the brief's required Z and B. Every other K7 plan control is a mismatch on the pre-change code (section 1).
8. The stub's K7 red carries 1278 issues, every one "untestable, not drawn" (cause absent, MEASURED). They are declared pairs at four stack poses plus the swept tests.

## 1 Plan rules

Pre-change runs used a copy of `docs/sketches/` with the pre-change `sketch_common.py`, `check_sketch.py` and `checks_s2.py`. The copy also had the new spec, fixtures and manifest, and two drawing helpers (`sector_boundary`, `NOTE_GID`) appended so the fixtures could build. "mismatch" means the control did not give its expected result. Results are MEASURED. The copy was deleted after the run.

### 1a K5 plan (SW-17, TP-13)

| Rule | Premise | Premise check | Z | B | Pre-change |
|---|---|---|---|---|---|
| SW-17: an axis-Z cylinder in plan must be drawn as a circle (existing comparison; B added) | none | n/a | K5-Z3 live S2 | K5-B7 drill tube as a rectangle | Z: fires (23 trapezoid issues, TP-13). K5-B7 fires with 24 issues: count mismatch, reason present |
| TP-13 classify: a four-vertex Polygon with four right angles is a rectangle at any orientation; an Annulus is a circle | n/a | n/a | K5-Z3 | K5-B8 NEMA 23 as a circle | Z fires: every radial rectangle at 30, 150, 210 or 330 read as a trapezoid (23 issues) |
| TP-13 radial axis: in plan_xy a cylinder, screw, cone or gear row with axis X or Y is radial; each four-vertex piece has an edge pair across the radial direction at the placed theta (0.1 deg) | the row has a radial place footprint | spec lint "radial-axis ... needs a radial place footprint" | K5-Z3 | K5-B9 rectangle turned 10 deg; K5-B10 (premise) round footprint | B9 and B10 mismatch (reason absent) |
| Hub admission: a gear row's rectangle piece is admitted as its hub | it starts on the heel edge of the row's trapezoid (TOL_Z) and is no wider than the heel | the same test; otherwise "hub rectangle ... not on the heel" | K5-Z3 (pinion trapezoid r 95.22 to 125 plus hub to 140) | K5-B11 hub 5 outboard of the heel | mismatch |

### 1b K6 in plan_xy

What K6 asserts in plan: z bands are not drawn, so K6 asserts z only through its spec lints (LF-16 planes, stack ties, check_stack anchors and import guard). It asserts placement in x and y. Every row with a plan basis has its drawn centre on the spec centre within 0.05:
- A placed row is checked in the radial frame at theta: the drawn u mid-extent equals r_c and the t mid-extent is 0. This holds for rectangles, trapezoids symmetric about their axis, circles, and squares turned about their centre.
- A plan_poly row is checked by the mid-extent of its pieces, a sector by the mid-extent of its wedge, and an axis-Z section or depth row by the drill axis.

Extent is K8's (1d).

| Rule | Premise | Premise check | Z | B | Pre-change |
|---|---|---|---|---|---|
| K6 plan centre | n/a | n/a | K6-Z4 live S2 (69 centres, worst 0.0000) | K6-B8 member c 6.75 off in x: "off 6.75" | Z fires 70 issues (drawn y compared with z bands, plus the LF-16 pair). B8 mismatch |
| LF-16 owner rule (relaxed: a plane whose feature is not a row of this spec) | a spec with that row carries an equal field | `_plane_owner` over `s*_spec.yaml` | K6-Z4 (s1 owns both planes) | K6-B9 S2 load_plane offset 1 | B9: 2 issues with the wrong reason, mismatch |

### 1c K7 in plan_xy (LF-8)

Geometry: each row's true XY outline from the spec (`plan_outline`). The outline types are:
- **Annulus about the axis:** a plain `section` row (ring, bearing, gear, gear hub), or a round place centred on the axis (drill tube, cutter rim, keep-out).
- **Footprint polygon:** a radial or round place.
- **Plan_poly pieces:** each piece separately (plate pieces, frame strips, tie strip).
- **Depth-band disk:** an axis-Z round row with no section.
- **Drawn pieces:** fallback for a row with no plan basis.

Rules:
- **Presence:** a pair is measured only when both rows are drawn.
- **Poses:** pairs are judged at every stack pose with that pose's z bands.
- **F:** z bands disjoint or touching (gap >= -0.05) pass as "z-separated" or "z-touch" (no common volume). Overlapping bands pass on plan overlap <= 0.01 mm².
- **G:** passes on max(z gap, plan distance) >= g_min - 0.05.
- **C:** fails on z bands more than 0.05 apart ("z-separated"). The plan C rule:
  - "z-contact": bands touch and plan distance <= 0.05, overlap allowed.
  - "plan-contact": bands overlap, plan distance <= 0.05 and plan overlap <= 0.01 mm².
  - "interference": bands overlap with plan overlap > 0.01.
- **Swept:** each moving row's outline is tested against every fixed row, declared F or G without poses or undeclared as F. A pair is tested when the fixed row's z band meets the sweep band (min to max over the poses).

| Rule | Premise | Premise check | Z | B | Pre-change |
|---|---|---|---|---|---|
| Plan F, G, C on z bands | outlines contain the drawn parts | K8 plan_extent (1d); K6 plan centre | K7-Z12 two members 100 apart, state F | K7-B22 1 mm overlap on F; K7-B23 G at g_min - 1 (9.000); K7-B24 C with z bands 100 apart | Z12, B22 match. B23 mismatch ("plan distance" absent). B24 mismatch ("depth-separated", not "z-separated") |
| Plan C rule (z-contact, plan-contact, interference; Engineer 1.2 (b) item 4e) | both outlines are true plan sections: radial footprint drawn as a rectangle, round footprint as a circle, a section annulus, a plan_poly piece. A circumscribing outline certifies F and G only | `plan_outline` true flag in `_plan_judge` | K7-Z13 pad on post, state z-contact | K7-B25 pad 1 mm into the post (interference); K7-B26 (premise) circumscribed round footprint C on a plate | Z13 fires (C overlap 900.000); B25, B26 mismatch |
| Annulus form (item 4d) | section is the true radial interval | containment of the drawn annulus in [a, b] (K8 plan_extent) | K7-Z14 ring round tube (F), bearing in the bore (C) | K7-B27 bearing OD 1 into the ring bore: overlap 631.460 = pi (101² - 100²) (DERIVED) | Z14 fires (outer and inner disks read as solid) |
| One plan figure (item 4f): one figure serves every stack pose | every row's plan outline is the same at every pose (0.05) | lint in `_k7_plan` | K7-Z15 live S2 | K7-B28 an arm whose r_in reads the pose | mismatch (clean) |
| Swept plan form (Loftsman 1.2 (b) section 5) | as the plan F/G rows | as above | K7-Z15 live S2 | K7-B29 fixed bar inside the ring annulus, z inside the sweep, clear of every pose | mismatch (one figure: the 1.0 swept loop never runs) |

Live S2 K7 (MEASURED): 1278 tests clean over 4 poses. Labels: undeclared:z-separated 2154, undeclared:F 1826, z-separated 1319, G 706, swept:z-separated 425, swept:G 243, N 172, undeclared:z-touch 158, swept:F 154, plan-contact 92, z-contact 81, swept:z-touch 2. K7 run time 3.3 s.

### 1d K8 plan

| Rule | Premise | Premise check | Z | B | Pre-change |
|---|---|---|---|---|---|
| Plan handedness: K8-B3 on the S2 axes; screws at -theta | n/a | azimuth predicates, axes not inverted | K8-Z6 live S2 (114 predicates) | K8-B18 y inverted; K8-B19 screws at -theta (3 azimuth + 3 plan_extent) | Z6 fires (pinion projected_x/y from the extent midpoint, item 4c; outboard at theta 90 reads 0). B18 9 issues (count mismatch). B19 17 issues, "screw_c azimuth 90.00" absent |
| plan_extent (items 4c, 4g): every drawn point inside the row's plan outline (0.05). Replaces projected_x/y/extent in plan; side views unchanged | outline from the spec | it is the premise check for K7 plan, plan_poly and annulus outlines | K8-Z6 | K8-B20 NEMA 23 a 10 wider | mismatch |
| Outboard, radial form (item 4b): centroid radius greater than the other's (`frame: radial` or plan) | n/a | n/a | K8-Z6 | K8-B21 NEMA 23 c placed inboard of its pinion | mismatch |
| Taper in plan (item 4b): radial frame (u for x, t for z), trapezoid pieces only (the hub carries no taper) | n/a | n/a | K8-Z6 | K8-B22 pinion teeth widening inward | mismatch |
| Sector equal to its wedge (S2-5a reads the drawn sector) | n/a | drawn points inside the wedge; spec boundary (apex, arc at 1 deg, edges) within 0.05 of the drawing | K8-Z6 | K8-B23 sector drawn at half-angle 40 (spec boundary 34.86 outside) | mismatch |

### 1e Figure note (Designer 1.2 (b) FIX 3), in K4

| Rule | Z | B | Pre-change |
|---|---|---|---|
| The spec `plan_figure.figure_note` and the drawn Text gid `note:figure_note` name the head of every `not_drawn` part. The head is the text before " (" or " at ": wing nut, collet, holder, power-off hold device, descent-stop pads, LM20UU bushing. A spec with `not_drawn` and no figure_note fails, S1 excepted (accepted before the rule) | K4-Z2 live S2 | K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note (planted 2) | Z2 matches. B4, B5 mismatch (clean) |

### 1f X1 shared rows (Loftsman 1.2 (b) section 2 and re-check ruling 5)

`check_sketch.x1_lint` runs with every `sN` run (result id X1) and with every `--stale` run. It covers `place`, `z_rule` and `plan_poly`, whitespace-normalised. A field present in only one spec is skipped and listed. `x1_exempt: {reason}` passes a row.

| Z | B | Pre-change |
|---|---|---|
| X1-Z: 47 compared; skipped base_frame plan_poly, base_plate plan_poly, keepout place (MEASURED) | X1-B1 frame_upper_b `place.r_in`; X1-B2 nut_a `z_rule.z_max` | error (no `x1_lint`) |

## 2 S2-x fixtures from the signed spec

Z for every check is `s2_live`, the signed S2 spec drawn faithfully in one plan figure at pose load.

| ID | Z (MEASURED) | B | Reason substring | Planted | Result | Pre-change |
|---|---|---|---|---|---|---|
| S2-1 | screws 30/150/270, pinions 90/210/330, phase 60 within 0.000 | screw b drawn at 110 deg | "screw spacing 40.00", "screw spacing 200.00", "pinion_a - screw_b" | 5 | fires 5 | matched |
| S2-2 | 52.80 over g_min 10 (160 - 21 - 86.2, DERIVED) | pitch radius = keep-out radius, drawn faithfully | "screw_a: 86.20 - 21.00 - 86.20 = -21.00" | 3 | fires 3 | matched |
| S2-3 | heel pitch points r 125.00 = 250 / 2, within 0.000 | pinion.r_heel = gear.od / 2 (126.32) | "pitch point r 126.32 vs gear pitch radius 125.00" | 3 | fires 3 | Z red (no drawn quantity), B mismatch |
| S2-4 | 4 centres within 0.000 | datum B cross 2 off in x | "collet_axis centre (2.00, 0.00) is 2.00 from drill_tube" | 1 | fires 1 | matched |
| S2-5a | 27 fixed parts clear, least 11.71 (outline) | half-angle 65 (130 deg), drawn faithfully | "operator_sector\|liftmotor_a", "\|liftmotor_b", "\|frame_upper_a" | 18 | fires 18 | matched (Z read 15.69 on drawn parts, Correction 3) |
| S2-5b | 8 ring parts in the sector, least 136.84 (bearing 1076.84 - 940) | motor23_c bottom 930 z_A at load | "motor23_c: lowest z 930.00 z_A, -10.00 above the hand band top 940" | 1 | fires 1 | matched |
| S2-6 | 3 members seated | member c at radius 300 | "frame_upper_c: 1560.00 mm2 of 3600.00 outside base_frame" | 1 | fires 1 | matched |
| S2-FULL (smoke) | every S2 row drawn; K1 to K9 and S2-1 to S2-6 run, none error or absent | | | | runs | runs (K5 to K9 fail on content) |

S2-3 drawn quantity (item 4h): the pinion is drawn as a toothed trapezoid from the toe r 95.22 to pinion.r_heel 125, narrowing inward, plus a hub rectangle to r 140. The pitch point is the midpoint of the trapezoid's outer tangential edge (`heel_point`). S2-5a and S2-5b read plan outlines (Correction 3).

## 3 Control figures (O5)

Written by `--controls` to `docs/sketches/wip/fixtures/figs/` (P0 output rule), with `key.json`:
- `ctrl_c.png`: "plan of the mini spec, screws counter-clockwise from +X at 30, 150, 270 (must PASS handedness)".
- `ctrl_d.png`: "the same plan mirrored in y, azimuths clockwise (must FAIL handedness)".

Both carry the title "plan_xy: plan control figure", the screw labels "screw a, theta 30 deg" etc., +X and +Y arrows and the theta arc. In ctrl_d the +Y arrow points down the page against the y tick labels, and the labelled 30 deg screw sits at -30. ctrl_a and ctrl_b are unchanged.

## 4 --controls

| Run | Result | Time |
|---|---|---|
| `check_sketch.py --controls` (new code) | **Z 55/55, B 121/121, smoke 2/2 (178/178)**, exit 0, to `wip/fixtures/` | 264 s (MEASURED; was 189 s at 128) |
| Pre-change copy, the 50 new entries | 15 matched, 35 mismatched (section 1 and 2 tables) | 74 s |

New: 50 (Z 17, B 32, smoke 1). Per-check tallies: K4 Z 2/B 5; K5 Z 3/B 11; K6 Z 4/B 10; K7 Z 15/B 29; K8 Z 6/B 23; K9 Z 3/B 5; X1 Z 1/B 2; S2-1 to S2-6 Z 1/B 1 each. The 128 earlier controls match under the flattened curves, the right-angle classify and the plan branches.

## 5 Stub run

`check_sketch.py s2 --rev 0` uses `stubs/s2_stub.py`: one plan figure at pose load, base_plate pieces only. It wrote `wip/s2_checks_r0.json` in 5.6 s. `check_sketch.py --baseline s2` gave run 2 **17/17**, with run 1 from `wip/fixtures/controls_results.json` (178/178). It wrote `wip/baseline_red.json`; `run2_by_sketch` is s1 17/17, s2 17/17; 2.3 s.

| Check | Expected (STUB_EXPECT / STUB_CAUSE) | Observed | Match |
|---|---|---|---|
| K1, K2, K3, K5, X1 | green (guard) | pass | yes |
| K4 | red (content) | fail content, 15 issues (labels and figure note absent) | yes |
| K6 | red (absent) | fail absent, 68 | yes |
| K7 | red (absent) | fail absent, 1278 | yes |
| K8 | red (absent) | fail absent, 112 | yes |
| K9 | red (content) | fail content, 69 | yes |
| S2-1 to S2-6 (7 checks) | red (absent), content evidence from the S2-x B fixtures in run 1 | fail absent, 1 each ("measured: none; ... not drawn") | yes |

No sketch check is green on the stub, so none was rewritten. The tables live in `checks_s2.py`. SOURCES S2-1 to S2-6 are written. `check_sketch.SKETCH_TABLES` lists X1 as an S1 guard; s1_checks_r0.json predates X1, so S1 run 2 is unchanged.

Side effects (MEASURED):
- `check_sketch.py s1 --rev 5` (preview, wip/): 18/18; X1 is added, and S1-1 to S1-7 and K values are unchanged (S1-5b 142.00).
- `--stale`: unchanged red on `frame_upper.radius` 300 to 274; X1 pass.

## 6 Code changes

All under `docs/sketches/`. CRLF is kept where the file had it.

| File | Change |
|---|---|
| `sketch_common.py` | `flatten_path` (curves sampled on the curve) in `artist_polys`. `_is_rect`; `classify` (rectangle at any orientation, Annulus as circle). `to_ut`, `bbox`, `plan_outline` (annulus, polys, true flag), `outline_measure` (exact annulus pairs; annulus against pieces by radius range; box-gap fast path), `outline_outside`, `sector_outside`, `sector_boundary`, `_plan_judge` (plan F, G, C rules), `plan_fig`, `_tangential_edges`, `heel_point`. K4 `figure_note_issues`, `part_head`, `NOTE_GID`. K5 radial-axis lint, radial-orientation test and hub admission. K6 `plan_centre`, `_k6_plan`, `_plane_owner` (LF-16 owner rule). K7 `_k7_plan` (static per stack pose, undeclared F, swept, one-figure lint, measure cache). K8 plan_extent and sector equality in plan; projected_x/y/extent and the plan_poly x branch now side views only; outboard radial form; taper in the radial frame. K9 skips `note:` texts |
| `check_sketch.py` | `x1_lint` (X1) appended to every sN run and run in `--stale`; `run_control` dispatches S2-x to `checks_s2.py`; K_SOURCES X1; S1 guard list + X1 |
| `checks_s2.py` | S2-3 heel pitch point; S2-5a and S2-5b on plan outlines (`_outline`); STUB_EXPECT, STUB_CAUSE, SOURCES |
| `stubs/s2_stub.py` | new: plan_xy figure at the plan_figure pose, base_plate pieces only |
| `s2_spec.yaml` | gear `section` (Correction 2); status line |
| `fixtures/builders.py` | `_s2_draw_row`, `_s2_draw`, `_s2_ctx`, `s2_live` (cached), `_s2_replace`, `_shift`; plan K7 fixture builder `_k7_plan`; the 50 new fixtures; `_plan_control`; `control_figures` writes ctrl_c, ctrl_d |
| `fixtures/manifest.yaml` | 50 entries (section 4) |

Not changed: `check_stack.py`, `sketch_loader.py`, `s1_spec.yaml`, `s1_side_poses.py`, `proposed_params.yaml`, params.yaml.

## 7 Rules awaiting their raiser's signature

| Rule | Raiser signs | Controls |
|---|---|---|
| SW-17 K5 plan B | Software Engineer | K5-B7 |
| TP-13: right-angle classify, radial-axis orientation, radial-footprint premise, hub admission; K8 taper in the radial frame, outboard radial, plan handedness B | Topologist | K5-Z3, K5-B8 to B11; K8-Z6, B18, B19, B21, B22 |
| LF-8 plan K7: outlines, z-band rules incl. F z-touch, plan C rule and its true-section premise, annulus form, swept plan form | Loftsman | K7-Z12 to Z15, K7-B22 to B27, B29 |
| K6 plan centre; LF-16 owner rule (relaxed) | Loftsman | K6-Z4, B8, B9 |
| X1 | Loftsman | X1-Z, B1, B2 |
| One-figure premise (4f), plan_extent premise (4g), curve flattening | Engineer raised; Loftsman and Topologist sign at (e); Software Engineer reviews the code at P5 | K7-B28, K8-B20 |
| Figure note check; sector equality premise; S2-5a/5b on outlines; S2-3 drawn pitch point (heel) | Designer | K4-Z2, B4, B5; K8-B23; S2-3, S2-5a, S2-5b rows |
| Gear `section` spec edit | Loftsman and Designer | K7-Z15 (live) |

Open, carried: Loftsman sign-off NOTE 2 (member-top stack tie, a spec edit) and NOTE 3 (K7 pair ids in the record) are not done here. The narrower-than-footprint read stays with M1 for parts drawn inside their footprints, except under S2-5a, which now reads outlines.

## 8 Gameplan lines to change

**l.131** (spec format, 1.2 (b) fields sentence), end fragment.

Old:
```
check_stack evaluates `plan_poly` and `sector`; their containment premise gets its check at 1.2 (c).
```
New:
```
check_stack evaluates `plan_poly` and `sector`; their containment premise is K8 plan_extent (every drawn point inside the row's plan outline; a sector drawn equal to its wedge; 1.2 (c), K8-B20, K8-B23). A plain `section` [r_in, r_out] on a row without `place` is its plan annulus (K7 plan; S2 gear row given one at 1.2 (c)). The plan figure note is a Text with gid `note:figure_note` (K4).
```

**l.138** (K4 row): three fragments.

Old:
```
a label number that differs from the key value fails |
```
New:
```
a label number that differs from the key value fails; from S2 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part (1.2 (c), Designer 1.2 (b) FIX 3) |
```
Old:
```
| Fixture with all labels from keys |
```
New:
```
| Fixture with all labels from keys; K4-Z2 live S2 |
```
Old:
```
B2 label "tube OD 150" against `drill.tube_od` 152.4 |
```
New:
```
B2 label "tube OD 150" against `drill.tube_od` 152.4; K4-B4 drawn note without the LM20UU bushing; K4-B5 a not_drawn part in neither note |
```

**l.139** (K5 row): three fragments.

Old:
```
a `bore_cone` row's four-vertex piece is admitted only inside its mate's z extent (1.1 r2) |
```
New:
```
a `bore_cone` row's four-vertex piece is admitted only inside its mate's z extent (1.1 r2); 1.2 (c): a four-vertex piece with four right angles is a rectangle at any orientation and an Annulus is a circle; in plan a row with axis X or Y is radial: premise a radial place footprint (spec lint), each four-vertex piece has an edge pair across the radial direction at its theta (0.1 deg), and a gear row's rectangle is admitted as its hub only on the heel edge of its trapezoid and no wider (TP-13) |
```
Old:
```
K5-Z2 live bore_cone holder |
```
New:
```
K5-Z2 live bore_cone holder; K5-Z3 live S2 |
```
Old:
```
K5-B6 bore_cone piece above the collet top |
```
New:
```
K5-B6 bore_cone piece above the collet top; K5-B7 drill tube as a rectangle in plan (SW-17); K5-B8 NEMA 23 as a circle in plan; K5-B9 NEMA 23 rectangle 10 deg off radial; K5-B10 radial-axis row with a round footprint; K5-B11 pinion hub 5 off the heel |
```

**l.140** (K6 row): three fragments.

Old:
```
must name the same z within 0.05 mm |
```
New:
```
must name the same z within 0.05 mm; a plane whose feature is not a row of this spec is linted in the spec that has the row, premise: that spec carries an equal field (1.2 (c), K6-B9). In plan_xy z is not drawn: K6 keeps its stack lints and asserts each row's drawn centre on its spec centre within 0.05 (placed rows in the radial frame: u mid-extent r_c, t mid-extent 0; plan_poly and sector by mid-extent; axis-Z section rows on the axis) |
```
Old:
```
| Fixture drawn from the same params |
```
New:
```
| Fixture drawn from the same params; K6-Z4 live S2 |
```
Old:
```
K6-B7 the holder flange tie at the r1 rule (8.00 apart) |
```
New:
```
K6-B7 the holder flange tie at the r1 rule (8.00 apart); K6-B8 member c drawn 6.75 off its plan centre; K6-B9 S2 load_plane unequal to the S1 field that owns core_seat |
```

**l.141** (K7 row): three fragments.

Old:
```
in plan the outline against every fixed member whose z band intersects the sweep |
```
New:
```
in plan the outline against every fixed member whose z band intersects the sweep. Plan view (1.2 (c), LF-8): true XY outlines from the spec (section annulus, place footprint, plan_poly pieces; drawn pieces where a row has none), held round the drawing by K6 and K8; every stack pose judged with its z bands in one plan figure (premise: plan outlines pose-invariant, lint); F passes on z bands disjoint or touching, else on plan overlap <= 0.01; G on max(z gap, plan distance) >= g_min - 0.05; C fails z-separated, passes as z-contact (bands touch, plan distance <= 0.05) or plan-contact (bands overlap, plan outlines touch without overlap), fails as interference; C passes need both outlines true plan sections; swept: each moving outline against every fixed row (declared F or G without poses, undeclared F) whose z band meets the sweep band |
```
Old:
```
Z8 to Z11 live S1 (plan-separated, pose-restricted, plan-contact) |
```
New:
```
Z8 to Z11 live S1 (plan-separated, pose-restricted, plan-contact); Z12 plan members 100 apart F; Z13 plan z-contact (pad on post); Z14 plan annuli (ring, bearing, tube); Z15 live S2 |
```
Old:
```
B21 live S1 tie a strip to the member centre (plan_poly plan-contact) |
```
New:
```
B21 live S1 tie a strip to the member centre (plan_poly plan-contact); B22 plan 1 mm overlap on F; B23 plan G at g_min - 1; B24 plan C z-separated by 100; B25 pad 1 mm into its post (interference); B26 z-contact on a circumscribing footprint; B27 bearing OD 1 into the ring bore; B28 plan outline moving with the pose in one figure; B29 swept plan: fixed bar inside the ring annulus within the sweep |
```

**l.142** (K8 row): three fragments.

Old:
```
containment only, a part drawn narrower than its footprint passes and is left to M1) |
```
New:
```
containment only, a part drawn narrower than its footprint passes and is left to M1). Plan view (1.2 (c)): every drawn point inside the row's plan outline (plan_extent, replacing projected_x/y in plan), the sector drawn equal to its wedge, outboard in radial form (centroid radius), taper in the radial frame on the toothed trapezoid |
```
Old:
```
K8-Z4, K8-Z5 live S1 |
```
New:
```
K8-Z4, K8-Z5 live S1; K8-Z6 live S2 |
```
Old:
```
B17 live S1 tie a drawn 10 wider than its plan_poly extent |
```
New:
```
B17 live S1 tie a drawn 10 wider than its plan_poly extent; B18 live S2 y inverted; B19 screws at -theta (azimuth clockwise); B20 NEMA 23 a 10 wider; B21 NEMA 23 c inboard of its pinion; B22 pinion teeth widening inward; B23 sector drawn at half-angle 40 |
```

**l.143** (K9 row), Z cell.

Old:
```
K9-Z2 live S1 |
```
New:
```
K9-Z2 live S1; K9-Z3 live S2 (one plan figure; texts with gid note: are not rows) |
```

**l.144** (X1 row), Z cell.

Old:
```
| Live s1 + s2 specs (47 compared; keepout place, base_plate and base_frame plan_poly skipped) |
```
New:
```
| Live s1 + s2 specs (47 compared; keepout place, base_plate and base_frame plan_poly skipped); runs with every sN run and --stale (1.2 (c)) |
```

**l.146** (K table control pointer), end fragment.

Old:
```
(126 controls: Z 38, B 87, smoke 1).
```
New:
```
(126 controls: Z 38, B 87, smoke 1). Step 1.2 (b) fix pass added K8-B17, K7-B21 (128). Step 1.2 (c) added K4-Z2, K4-B4, K4-B5, K5-Z3, K5-B7 to B11, K6-Z4, K6-B8, K6-B9, K7-Z12 to Z15, K7-B22 to B29, K8-Z6, K8-B18 to B23, K9-Z3, X1-Z, X1-B1, X1-B2, S2-1-Z to S2-6-B1 (14) and the smoke control S2-FULL (178 controls: Z 55, B 121, smoke 2; 264 s).
```

**l.255** (S2-3 row), check cell.

Old:
```
| S2-3 | Pinion mesh: each pinion pitch point at the gear pitch radius within 0.05 mm |
```
New:
```
| S2-3 | Pinion mesh: each pinion pitch point at the gear pitch radius within 0.05 mm (drawn pitch point: midpoint of the heel edge of the pinion's toothed trapezoid, drawn toe to pinion.r_heel with its hub outboard; 1.2 (c)) |
```

**l.257** (S2-5a row), fragment.

Old:
```
guide rods and ties; K7 F) |
```
New:
```
guide rods and ties; K7 F; measured on each fixed part's plan outline against the drawn sector, which K8 holds equal to the spec wedge, 1.2 (c); the drawn 42 square lift motor reads 15.69) |
```

**l.263** (detail 1.2 carried line), fragment.

Old:
```
XY footprint test replacing the side-view box approximation for frame members (LF-8, `frame_upper.radius` 300);
```
New:
```
XY footprint test replacing the side-view box approximation for frame members (LF-8, `frame_upper.radius` 300) (written at 1.2 (c): K5 plan rules with K5-B7 to B11, K6 plan centre, K7 plan form with K7-Z12 to Z15 and B22 to B29, K8 plan with B18 to B23, X1, figure note; raisers sign at (c) or (e), step1.2_engineer_redfirst.md section 7);
```

**Progress Log, row 1.2** (append): `P4 red-first: plan rules (SW-17, TP-13, K6 plan, LF-8 plan K7 with the plan C rule, annuli, one-figure premise, swept form; K8 plan containment, radial outboard and taper, sector premise; figure note; X1; LF-16 owner rule) and S2-x fixtures; controls 178/178 (Z 55, B 121, smoke 2), 264 s; s2 r0 stub 17/17 against STUB_EXPECT, --baseline s2 run 2 17/17; s2_spec gear section added (awaiting Loftsman, Designer); S2-5a least 11.71 on outlines.`
