## Corrections to the brief

1. **S3 cannot be all green at r1 as briefed. Two reds stay, and neither is a drawing defect.**
   - **S3-3 (18 issues): records.** It resolves certifiers to the latest accepted S1 and S2 records in `docs/sketches/`. Those are S1 r7 and S2 r5, and both are stale on `jackscrew.lead`, `jackscrew.nominal` and `liftmotor.coupling_length`. S3-3 turns green once the orchestrator accepts S1 r8 and S2 r9. Dry run with `wip/s1_checks_r8.json` and `wip/s2_checks_r9.json` flagged accepted in a scratch records directory (`--docs-dir`, `--wip-dir` under `D:\Unleashed Robotics\_scratch\cutjig\p6\dry_records`): **S3-3 pass, 51 links closed** (MEASURED).
   - **K4 (1 issue): spec defect D1, sync_callout label.** The label `text` is "one controller, three drivers, home switch per screw". The key `liftsync.method` has the value "one controller, three drivers, home switch per screw at park; no belt". K4 removes every occurrence of the label text before it looks for the value. The value starts with the label text, so no drawing can pass. Open item for The Designer.
2. **Thread ticks on screw c, the reversed cover hatch and the anchor joint line (spec `ticks`, `hatch_split`) cannot be drawn under the harness as it stands.**
   - K5 admits tick sub-artists only on a gear row in plan.
   - `render_section` gives every cut row its material hatch, and convention clause (1) fails any other hatch.
   - Not drawn. The cover-to-block joint at 288 shows as the shared edge of the separate pieces. Open items D2 and D3.
3. **The inset theta arc (spec `plan_axes` shape) is not drawn.** K8 plan_extent holds the row to its plan_poly, which is two straight marks. A text "theta ccw from +X" stands in. Open item D4.
4. **The moving mass in S1 r8 is W 24.25 kg (the W_kg items) plus the top-end block 2 kg.** `s3_spec.yaml load_cases.W_kg` leaves out `drill.top_block_mass`. The mass report lists the block apart from W. Open item D5.
5. **Bolt leaf (exception f).** `receiver.shoulder_bolts` states "4 x M5 into the plate". PCD and azimuths are left to The Designer and are not set here. The bolts are `not_drawn` in S1, S2 and S3.

Tags: MEASURED (read from a run in this session), DERIVED (hand arithmetic), DECLARED (spec, params or ruling).

## 1 Files written

| File | Change |
|---|---|
| `docs/sketches/s3_jackscrew_section.py` | New. Section A-A plus plan inset via `setup_figure`; `render_section` and `render_plan`; `place_plan_labels` in both Axes; inset moved right of the main label column (`_inset_right_of_labels`, same size and height) |
| `docs/sketches/s3_spec.yaml` | (a) x1_exempt removed (3 rows); (e) F2 nut_c, guide_c projection rectangle; F3 motor_shaft_c outboard without `frame`; `mirror_about_radial` (axes inset_plan) on anchor, liftmotor, frame_upper, home_switch a/b/c; (f) receiver shape, keys, shoulder section piece, depth ±shoulder_od/2; base_plate\|receiver C with `face: receiver.shoulder_z`; chains a, b, c receiver link certified by "S3 base_plate\|receiver" alone (S1 C struck); not_drawn shoulder bolts and spigot; figure note |
| `docs/sketches/s1_spec.yaml` | anchor_a/_b to the S3 42-square radial place (keys + anchor_block_width, pitch_radius, angle); screw names, shapes and label to Tr12x3; receiver shoulder piece, keys, depth; base_plate\|receiver source (slab, struck from S3 chains); reported_items (8 ids, Designer sign-off section 8); not_drawn and figure note (bolts) |
| `docs/sketches/s2_spec.yaml` | anchor_a/_b/_c: kind prism, projection rectangle, 42-square radial place; screw names and shapes Tr12x3 d 12; bracket shape text; new row receiver_shoulder (cylinder, round r 100, z 12 to 20, C on base_plate); part_list, not_drawn, figure note |
| `docs/sketches/proposed_params.yaml` | Group `receiver`: shoulder_od 200, shoulder_thickness 8 (ASSUMED), shoulder_z 12 (expr base.plate_thickness, DERIVED), shoulder_bolts (ASSUMED) |
| `docs/sketches/s1_side_poses.py` | Bearing line drawn as `anchor_<s>:line` at the spec mark z (replaces the zero-area rectangle); shoulder pieces; loop note "Tr12x3" |
| `docs/sketches/s1_mass_report.py` | W items (bearing, pinions, hub, bushings added); Tr12x3 screws; NEMA 17 from `liftmotor.mass`; `pose_data` shared with checks_s1; W column |
| `docs/sketches/checks_s1.py` | `reported(ctx)` with the 8 RPT items |
| `docs/sketches/checks_s3.py` | STUB_EXPECT: SYM moves to guard. STUB_CAUSE: the K8 F3 entry and the SYM entry removed; K8 now reads absent |
| `docs/sketches/fixtures/s3_fixtures.py` | (g) `p4_spec_findings`, `_receiver_cert`, `_plate_g`, `_post_p6_specs` (now `_live_specs`) and the pre-P4 figure fallback removed; `s3_fixed` = `s3_live`; mirror fixtures use the live declaration; S3-3-B9 redefined; H1-B9 plants x1_exempt on a copy; fixture figure note inside the Axes |
| `docs/sketches/fixtures/builders.py` | K5-B20 re-planted on the `anchor_<s>:line` mark |
| `docs/sketches/fixtures/manifest.yaml` | S3-3-B3 planted 14 to 11; S3-3-B9 description; reasons for K7-B19 (1.000), K4-B6 (not_drawn (2)), K3-B8 (new note text) |
| `docs/sketches/wip/` | `s3_jackscrew_section_r1.png`, `s3_checks_r1.json`, `s3_summary_r1.md`, `s3_checks_r0.json`, `baseline_red.json`; `s1_pose_{load,start,capture_end,park}_r8.png`, `s1_checks_r8.json`, `s1_summary_r8.md`, `s1_mass_report_r8.json`; `s2_plan_r9.png`, `s2_checks_r9.json`, `s2_summary_r9.md`; `fixtures/controls_results.json` |

First S3 PNG: `docs/sketches/wip/s3_jackscrew_section_r1.png` first written **2026-11-26 11:59:12**. It was rewritten at 12:00:35 after iteration 1 (inset placement, inset axis marks); the 12:00:35 file is the r1 of record. Scratch, probes and logs: `D:\Unleashed Robotics\_scratch\cutjig\p6\` (pre-P6 copy of the harness in `pre\`). Nothing was written to C:.

## 2 Iteration log

| Run | Red | Fix |
|---|---|---|
| 1 (11:59, PNG first) | K1 2 (index literal 3 in `pc[3]`, `e[3]`); K4 1 (sync_callout, D1); K8 1 (inset plan_axes arc 21.21 outside its plan_poly outline); S3-3 18 (stale records) | Unpacked the section_u entries; arc removed (D4); inset moved right of the label column (the hold label ran under the inset) |
| 2 (12:00) | K4 1 (D1); S3-3 18 (records) | none in the drawing. S3-3 dry run with r8/r9 records: pass, 51 links |
| final (12:15) | the same two | — |

Controls, in sequence (all MEASURED):

| Run | Result |
|---|---|
| Run 1, spec edits only | 89/92 Z, 253/273 B. Mismatches: scaffolding (S3-3 Z and B with `_receiver_cert`; K7-Z18/B35 with `_plate_g` G 0.10; K8-B76 with a duplicated mirror declaration; H1-B9 with no exemption left). Re-plants also due: K7-B19 (footprint distance 0.994 to 1.000), K4-B6 (not_drawn count), K3-B8 (note text), K5-B20 (the zero-area line no longer drawn). The fixture figure note ran off the canvas (K3-Z4, B10, B11). |
| Run 2 | Every S3 fixture in error: a newline was written into a string literal by the edit script. Fixed. |
| Run 3 | 91/92, 271/273. The remaining fixture note clip (K3-Z4, B10, B11) was fixed by putting the note inside the Axes. |
| Final | Run of record (table below). |

## 3 Final check tables

**S3 r1** (`wip/s3_checks_r1.json`, MEASURED): 14 of 16 pass.

| Check | Result | Value |
|---|---|---|
| K1 | pass | no literal; angles from `jackscrew.angle[2]` (screw set c, u = r sin theta), `pinion.angle[0]` (check_stack place), inset theta from each row's place |
| K2 | pass | 412 keys; 190 overlay leaves; 21 expr leaves agree |
| K3 | pass | both Axes |
| K4 | **fail 1** | sync_callout label (D1); section: 19 labels pass, no UNPLACEABLE |
| K5 | pass | section 111 artists, inset 34 |
| K6 | pass | 48 z_rules within 0.05; 22 inset plan centres |
| K7 | pass | section 269 tests; inset clean |
| K8 | pass | section 218, inset 75 predicates |
| K9 | pass | 49 and 23 rows |
| S3-1 | pass | tension segment least 25.84 mm (nut bottom 365.84 against the bearing line 340.00 z_S at capture_end); cut arrow +Z |
| S3-2 | pass | P_cr 1363.8 N (K 0.7, L_t 870.00 drawn = expression), least 3.97 stall_up |
| S3-3 | **fail 18** | live: S1 r7 and S2 r5 stale; dry run with S1 r8 / S2 r9 as accepted: pass, 51 links; receiver\|base_plate on the shoulder face at 12 z_A |
| X1 | pass | 70 rows, no exemption |
| SYM | pass | 18 pairs |
| RPT | pass | 10 items |
| SYM-P | pass | |

**S1 r8** (`wip/s1_checks_r8.json`): **19/19 pass** (18 checks plus RPT). **S2 r9** (`wip/s2_checks_r9.json`): **18/18 pass**.

**Stub** `s3 --rev 0`: green guards K1, K2, K3, K5, X1, SYM, SYM-P. Red: K4 content, K6/K7/K8 absent, K9 content, S3-1/S3-2/S3-3 absent, RPT absent. `--baseline s3`: run 2 matched **16/16**.

**`--controls`** (default 12 jobs): **368/368 match** (Z 92/92, B 273/273, smoke 3/3), **160.9 s** wall.

**`--stale`**: 2 records, 5 differences, all on the adopted keys:
- S1 r7: jackscrew.lead 8 to 3, jackscrew.nominal 8 to 12, liftmotor.coupling_length 25 to 36.
- S2 r5: jackscrew.nominal 8 to 12, liftmotor.coupling_length 25 to 36.

X1 pass, 70 rows, no exemption.

**Re-planted fixtures** (exception (a): the 17 from the (b) dry run, each fires or reads clean as declared in the final run, MEASURED):
- Z clean: K5-Z3, K7-Z15.
- Fire 1/1: K5-B7 to B11, B13, B14, B15, B18, B21, B24.
- Fire 2/2: K5-B16, B17.
- Fire 12/12: K7-B33.
- Fire 4/4: K7-B19.

**Other re-plants:**
- Fire 8/8: K5-B20.
- Fire 1/1: K4-B6, K3-B8, H1-B9.
- S3-3-B3 fires 11/11.
- S3-3-B9 (redefined) fires 3/3. With the plant withdrawn (seat at 12, a/b S1-only) it passes, 51 links (`probe_b9.py`).
- K8-B76 fires 1/1.
- K7-Z18 clean, K7-B35 fires 1/1.

## 4 Reported items (`wip/s3_checks_r1.json` reported_drawn; DERIVED unless tagged)

| Item | Value |
|---|---|
| L_min | 0.5 m only and 0.5 + 0.75 m: L_min 885.00, at anchor 885.84; plus 1 m: 1135.00, 1135.84 (DN23 800 to 900). Drawn bar (screw-end bottom 254 to guide-block top 1165): 911.00 |
| n_crit | pinned-pinned 1336 rpm (2.67 x), fixed-pinned 2086 rpm (4.17 x), against 500 rpm at 25 mm/s |
| pcr_margin | floating K 0.7, L 870, P_cr 1363.8 N: static 17.20, capture 12.04, retract 7.61, stall up 3.97 (two-screw 11.47, 8.02, 5.07). K 1.0: P_cr 668.2, stall up 1.95. Rigid K 0.5, L 815.84: P_cr 3039.7, stall up 8.86 |
| f_stall | mu 0.15: 343.18 per screw, 1029.54 total; mu 0.20: 282.21, 846.64 |
| wob_max | 1267.43 N (mu 0.15), 1084.54 N (mu 0.20), against 1000 N |
| lift_torque | cut 0.333 / 0.405 N m, capture lift 0.149 / 0.181 N m, against 0.45 |
| kept_axial | 1000 N at the cut; 1267.43 / 1084.54 N at F_stall + W |
| backdrive | lambda 5.20 deg; phi_n 8.83 / 11.70 deg; back-drive efficiency -0.698 / -1.253 (self-locking) |
| screw_share | static 79.30 / 118.95; capture 113.31 / 169.96; retract 179.30 / 268.95; cut 254.04 / 381.05; stall up 343.18 N |
| tension_segment (MEASURED) | nut centre above the drawn bearing line: load 815.84, start 690.84, capture_end 40.84, park 815.84 |

## 5 UNPLACEABLE labels

None. The placer recorded no UNPLACEABLE label in either Axes (K4 record has no `unplaceable` field). The only K4 issue is D1.

## 6 S1/S2 comparison

S1 r8 was triggered by Design Notes 31 (Tr12x3), Design Notes 32 (shoulder) and the K5 mark. S2 r9 was triggered by the same rulings.

| Quantity | Old | New |
|---|---|---|
| Every S1 check value (S1-1 650.00, S1-2 125.00, S1-3 367.34 / 117.34, S1-4 0.84, S1-5a 192.34, S1-5b 142.00, S1-6 0, S1-7 607.66) | r7 | equal (MEASURED) |
| S1 K7 nut_housing_a\|anchor_a projected distance, capture_end | -46.00 | -53.69 (square at theta 150 projects wider), state F, plan relief unchanged |
| S1 K5 | 8 zero-area issues on the live r7 script (P4 record) | pass; bearing line is `anchor_<s>:line` |
| S1 RPT | exempt (r7) | pass, 8 items |
| S1 mass per pose (load / park) | 76.07 / 60.47 kg | 81.50 / 65.90 kg. W 24.25 kg; Tr12x3 screws 2.40 kg against 1.07 |
| S1 CoM z_S (load / capture_end) | 664.8 / 427.1 | 692.9 / 432.0 |
| S1 tip force at CoM / frame top, load | 341 / 177 N | 351 / 189 N |
| Every S2 check value (S2-2 52.80, S2-5a 11.71, S2-5b 19.84, others 0) | r5 | equal (MEASURED). K7 1292 to 1296 tests: receiver_shoulder\|base_plate z-contact |

PNGs:
- S1 r8: `docs/sketches/wip/s1_pose_load_r8.png`, `s1_pose_start_r8.png`, `s1_pose_capture_end_r8.png`, `s1_pose_park_r8.png`.
- S2 r9: `docs/sketches/wip/s2_plan_r9.png`.
- S3 r1: `docs/sketches/wip/s3_jackscrew_section_r1.png`.

## 7 Open items

| # | Item | Owner |
|---|---|---|
| D1 | sync_callout label text is a prefix of `liftsync.method`, so K4 cannot pass for any drawing. Remedy: a label text that is not a substring of the value (e.g. "sync"), or no label on a callout row | The Designer |
| D2 | screw_c `ticks` (lead 3 over 300 to 1120) has no K5 admission in a section; unsectioned rows take no hatch | The Designer / The Topologist |
| D3 | anchor_c `hatch_split` (reversed cover hatch, joint line) conflicts with convention clause (1) | The Designer / The Topologist |
| D4 | plan_axes theta arc lies outside the row's plan_poly (K8 plan_extent) | The Designer |
| D5 | `load_cases.W_kg` leaves out `drill.top_block_mass` (2 kg moving): W 24.25 against 26.25 with it | The Designer |
| D6 | Detail scale: the anchor, nut and coupling stack (42 mm block) draws at about 0.86 px per mm in the full section. A detail inset in the spec would serve V7/V8 | The Designer (M1) |
| D7 | Shoulder bolt PCD and azimuths open (`receiver.shoulder_bolts`); `tray.hole_r` 81.2 to 101 and the ASSEMBLY.md load-path line go to Quinn (B2-10) | The Designer; Quinn |
| D8 | bracket_anchor r_in stays `pitch_radius + nut_flange_od / 2` (181) in all three specs. The Loftsman's text form `anchor_block_width / 2` is a shared-row edit outside the named exceptions; same value | The Loftsman |
| D9 | `checks_s2.py` l.314 reads `s1_mass_report_r7.json` (tip-force item); it should read the accepted S1 report once S1 r8 is accepted | The Engineer at acceptance |
| D10 | S3-3 live green needs S1 r8 and S2 r9 accepted (`--accept s1`, `--accept s2`), then `s3 --rev 1` re-run | Orchestrator |

## 8 Gameplan lines to change

1. l.147 (K table pointer). Old: `S3-3-B4 to B11, SYM-P-Z, SYM-P-B1 (368 controls: Z 92, B 273, smoke 3, all match; 157.6 s at --jobs 12).` New: `S3-3-B4 to B11, SYM-P-Z, SYM-P-B1 (368 controls: Z 92, B 273, smoke 3, all match; 157.6 s at --jobs 12). Step 1.3 P6 (research/sean/cr_scratch/step1.3_engineer_draw_r1.md) removed the S3 fixture scaffolding (p4_spec_findings, _receiver_cert, _plate_g, _post_p6_specs, pre-P4 fallback), redefined S3-3-B9 (shoulder seat 1 up), re-planted K5-B20 (mark line), H1-B9, S3-3-B3 (11), K7-B19, K4-B6, K3-B8 and showed the 17 (b) dry-run controls at their declared results (368 controls, all match; 160.9 s at --jobs 12).`
2. l.276 (detail 1.3 Script line). Old: `s3 --rev 0 red by cause 16/16 in wip/baseline_red.json; SYM-P a green guard, 1.3 P5f).` New: `s3 --rev 0 red by cause 16/16 in wip/baseline_red.json; SYM-P a green guard, 1.3 P5f; 1.3 P6: SYM a guard and K8 absent after F3, 16/16). S3 r1 (1.3 P6, step1.3_engineer_draw_r1.md): 14/16, K4 red on the sync_callout label (spec), S3-3 red until S1 r8 / S2 r9 are accepted (dry run 51 links closed).`
3. l.243 (detail 1.1 Reported). Old: `the mass report carries W 24.25 kg (s3_spec load_cases.W_kg) and Tr12x3 screws.` New: `the mass report carries W 24.25 kg (s3_spec load_cases.W_kg) and Tr12x3 screws (S1 r8, 1.3 P6: mass 81.50 kg at load, top-end block 2 kg moving outside W_kg).`
4. l.300 (Carried to S1 r8). Old: `section form (hull of the parent's pieces) for anchor_bearing_c:line in S3, for the Topologist at P5T.` New: `section form (hull of the parent's pieces) for anchor_bearing_c:line in S3, for the Topologist at P5T. Drawn at 1.3 P6: S1 r8 anchor_a/_b:line at the mark z, K5 pass (19/19); S3 r1 anchor_bearing_c:line.`
5. l.674 (TP1.1-9 row). Old: `is redrawn in S1 r8 as anchor_<s>:line under the K5 mark admission rule |` New: `is redrawn in S1 r8 as anchor_<s>:line under the K5 mark admission rule (done at 1.3 P6, wip/s1_checks_r8.json K5 pass) |`
6. Insertion after the Progress Log row starting `| 1.3 | 2026-11-26 | Receiver shoulder (` (l.519): `| 1.3 | 2026-11-26 | (d) P6 (step1.3_engineer_draw_r1.md): s3_jackscrew_section.py; wip/s3_jackscrew_section_r1.png first written 11:59:12; S3 r1 14/16 (K4 sync_callout label spec defect D1; S3-3 stale records, dry run with S1 r8 / S2 r9 accepted 51 links); S3-2 least 3.97 stall up; L_min 885.00; no UNPLACEABLE; S1 r8 19/19, S2 r9 18/18; exceptions (a) to (g) applied (42-square anchors in all specs, x1_exempt removed, Tr12x3 names, shoulder OD 200, S1 reported_items, F2, F3, mirror_about_radial, scaffolding removed); controls 368/368 in 160.9 s; --stale 5 differences on the adopted keys |`
