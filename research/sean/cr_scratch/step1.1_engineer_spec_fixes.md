# Step 1.1 (b) Engineer fix pass, S1 spec sign-off findings

## Corrections to the brief

1. **Loftsman FIX 5 is a decision for Sean, not a fix (orchestrator ruling).** The option R stop rule puts the cutter 125.00 inside a 1 m core at start. The geometry is reported. The stop rule is unchanged. The spec carries an OPEN comment at `park_rule`.
2. **Spec status is not set to "signed pending Sean pose confirmation".** FIX 5 stays open by ruling, and both reviewers still have to re-check. Header now reads: `fix pass 1.1 (b) applied (step1.1_engineer_spec_fixes.md); awaiting Designer and Loftsman re-check, then signed pending Sean pose confirmation`.
3. **Loftsman FIX 4a states two different expressions.**
   - Section 6 gives addendum x sin(pitch_angle) = 4.1667 x 0.31623 = 1.32, so r 95.22.
   - The FIX 4a text gives (OD - PD) / 2 x sin(pitch_angle) = 3.955 x 0.31623 = 1.25, so r 95.29.
   - The spec uses m sin(pitch_angle), with m = pinion.pitch_diameter / pinion.tooth_count = 4.1665, which gives 95.222. That is the section 6 value and the smaller radius, so the footprint is larger.
4. **Designer section 6 operator-task rows are gameplan content (l.179-183).** No spec row or field holds them. They go to the orchestrator at G-edit, listed in section 4.
5. **Controls can now target S1 checks.** Before this pass, `check_sketch.run_control` dispatched only K1 to K9. It now also runs `checks_s1.CHECKS` entries by id, judged the same way. S1-4 gained `n_issues` so its B can be matched on count.

Tags: check_stack values are DERIVED. Smoke drawing and control results are MEASURED (run 2026-11-25). Overlay values are ASSUMED as marked.

## 1. Disposition per finding

Files are under research/sean/cr_scratch/sketches/ unless stated.

### 1.1 Designer findings

| ID | Change | Evidence | State |
|---|---|---|---|
| F1 | `ring.pinion_support` takes the E3 text verbatim, with source "Designer 1.1 (b): pinion on the NEMA 23 shaft; 2 mm between pinion back r 140 and flange r 142" (ASSUMED). Ring shape: "pinion-shaft bushing blocks;" deleted. | K9 45 rows, K2 clean (MEASURED, S1-FULL) | closed |
| F2 | motor_mount_a/_b place `r_out: "ring.od / 2"` (210). `ring.od` added to keys. Shape per F2 text. | place r 142 to 210, half-width 28.5. motor_mount\|motor23 C at 0.000. motor_mount\|pinion plan gap 2.000 (MEASURED) | closed |
| F3 | New leaf `ring.guide_lug_half_width` {20, mm, "Designer 1.1 (b): LM20UU OD 32 + 2 x 4 wall; no source", ASSUMED}. guide_lug_a/_b `half_width: ring.guide_lug_half_width`; key added. | guide_lug_a place r 210 to 250, half-width 20.0. guide_lug\|ring C 0.000 (MEASURED) | closed |
| F4 | Four N entries removed from base_plate. frame_upper_a/b: z_rule 12 to 12 + member_length, neighbour base_plate C (source per F4). guide_member/_b: z_rule 12 to 1212, neighbour base_plate C. `frame_upper.member_length` 1213 DERIVED. | frame_upper_a\|base_plate C 0.000 and guide_member\|base_plate C 0.000 at load and capture_end. frame_upper_a\|base_frame undeclared F, 12.000. Frame top 1285.00 z_S, unchanged. Rod top 1272.00 z_S (MEASURED) | closed; control K7-B13 |
| F5 | `frame_upper.stop_pad_r_in` 200 ASSUMED. descent_stop shape "r 200 to 215". nut_housing_a\|descent_stop source "plan gap 15.0". ring\|descent_stop source "contact strip r 200 to 210 x 60". | nut_housing_a\|descent_stop plan-separated, 14.993 (128-gon reads 0.007 low; true 15.00). ring\|descent_stop C 0.000 (MEASURED) | closed |
| F6 | guide_member/_b shape per F6 text. | text | closed |
| Section 6 operator rows | No spec change. Rows go to gameplan l.179-183 (section 4). | n/a | to orchestrator |

### 1.2 Loftsman findings

| ID | Change | Evidence | State |
|---|---|---|---|
| FIX 1 | New row `collar`: cylinder, axis Z, rectangle, keys [collar.od, collar.top_above_plate, stop.collar_top_z]. z_rule collar_top - 6.75 to collar_top (153.09 to 159.84 z_A). Depth +/- 76.2. N with holder, wingnut and core_750. collar added to group s1_5b_base (G 10, capture_end). drill_head\|collar G 25 at capture_end. entry_plane = {collar_top, collar, z_max, 0}. | S1-5b 77 pairs, least 142.00 (was 66 pairs, 148.75). drill_head\|collar 25.000, gap - g_min +0.000 (g_stop by definition). K6-Z3 clean on the new entry_plane. collar\|holder 16.00, collar\|receiver 24.59 (MEASURED) | closed; controls S1-5b-Z, S1-5b-B1 |
| FIX 2 | **checks_s1.s1_4:** low = anchor z_max + g_min + max(nut_length, nut_housing_height) / 2; high = guide z_min - g_min - max(...) / 2. g_min comes from the spec through the new `check_stack.screw_block_g_min(spec, s)` (nut_housing_s\|anchor_s and \|guide_s neighbours). A missing pair reads "content" red. The issue text carries both margins.<br>**Spec `screw_length`:** one governing expression, `L_min = stroke + a + g + max(nut_length, nut_housing_height) + 2 * g_min_screw_block`, plus the reported `at anchor_z`. The other two expressions are removed and the comment names them superseded, with the reason. `g_min_screw_block` is a stack name set in `reported()` from the same spec neighbours, so it is not a literal (NOTE 6). | S1-4 least 0.84 (capture_end, low), was 10.84. L_min 885.00 / 885.00 / 1135.00. At anchor_z 885.84 / 885.84 / 1135.84. Buy 900 / 900 / 1140 (DERIVED) | closed; controls S1-4-Z, S1-4-B1 |
| FIX 3 | sketch_common.k7: the declared set is built per pose. A neighbour with `poses` enters it only at those poses, and elsewhere the pair takes the undeclared-F test. | core_750\|drill_head at start: F, 42.340. At load: F, 108.670. core_750\|drill_tube at start: 148.709 (MEASURED). K7 on S1-FULL: 285 pair tests clean (was 265) | closed; controls K7-Z10, K7-B12 |
| FIX 4a | pinion_a/_b place `r_in: "pinion.r_toe - pinion.pitch_diameter / pinion.tooth_count * sind(pinion.pitch_angle)"` (correction 3). Shape notes name the toe tip r 95.22. | place r_in 95.222. drill_tube\|pinion_a 19.002, gear_hub\|pinion_a 5.198 (Loftsman 19.02 / 5.22 HAND; the 128-gon reads up to 0.02 low). States unchanged (MEASURED) | closed |
| FIX 4b | liftmotor_a/_b `half_width: "liftmotor.body / 2 * sqrt(2)"`, the round footprint round the 42 square. `sqrt` added to check_stack FUNCS. The orientation of the square is S3's, so the orientation-free circle is used. The side drawing now shows the lift motor 59.4 wide, the diagonal. | half_width 29.698. K7 clean; no lift-motor pair is relieved (MEASURED) | closed |
| FIX 4c | Spec `k7_tolerance` and its header comment carry the plan-separated clause and the FIX 3 rule. | text | closed; gameplan l.140 in section 4 |
| FIX 5 | No rule change (correction 1).<br>**Reported:** check_stack `reported().q9_options[*].start_minus_core_top` = start_k - (core_stop + L): 0.5 m +292.34, 0.75 m +42.34, 1 m -125.00 (start 917.50 against core top 1042.50).<br>**Spec:** OPEN comment at `park_rule`. | DERIVED, check_stack run | open, Sean (section 3) |
| NOTE 1 | K6-B6: entry_plane term collar_top with feature core_seat. | fires: "LF-16 entry_plane: term collar_top 159.84 z_A vs core_seat.z_max + offset 42.50 z_A, 117.34 apart" (MEASURED) | closed |
| NOTE 6 | Covered by FIX 2: no literal 10 in `screw_length`. | | closed |
| NOTES 2 to 5 | No action at (b). NOTE 4: the pad margin is now 5 over G 10 (F5). | | n/a |

## 2. Controls and runs

New controls, each B first run against the pre-fix code (scratch, MEASURED):

| Control | Fixture | Pre-fix code | Post-fix code |
|---|---|---|---|
| S1-4-Z | live S1 drawing | clean, 10.84 | clean, 0.84 |
| S1-4-B1 | top guides drawn 20 low (L 880 < L_min 885) | **clean, 4.16 (missed)** | fires 4: load and park, screws a and b, "high margin -5.84" |
| S1-5b-Z | live S1 drawing | clean, 148.75 | clean, 142.00 |
| S1-5b-B1 | collar drawn 133 high at capture_end (bearing 9 above it) | **clean, 148.75 (no collar row)** | fires 1: "bearing\|collar ... gap - g_min -1.000" |
| K7-Z10 | live S1 drawing | clean | clean |
| K7-B12 | capture core drawn 60 high at start, into the drill head | **clean (pair skipped at start)** | fires 1: "start/core_750\|drill_head undeclared (F): ... overlap 1766.000" |
| K7-B13 | frame member foot 1 mm above the plate at load | fires on frame_upper_a\|base_frame (old declaration) | fires 1: "load/frame_upper_a\|base_plate C: distance 1.000" |
| K6-B6 | entry_plane named on core_seat | fires | fires 1, reason above |

Runs:

| Command | Result |
|---|---|
| `check_stack.py` | exit 0. Park 959.84, stroke 775.00, highest 1969.84 / 1844.84 / 1285.00 / 1969.84 z_S (load, start, capture_end, park), all unchanged |
| `check_sketch.py --controls` | 84 controls: Z clean 24/24, B fired 59/59 (each on its reason substrings and planted count), smoke 1/1. Run time 68.5 s (was 51.4 s at 76 controls). exit 0 |
| `check_sketch.py --stale` | 0 records, 0 differences |

S1-FULL smoke drawing (MEASURED), every check pass:

| Check | Result |
|---|---|
| K1 to K9 | K2 210 keys, 103 overlay leaves; K6 179 z_rules; K7 285 pair tests clean; K8 230 predicates; K9 45 rows |
| S1-1 | 650.00 |
| S1-2 | +125.00 |
| S1-3 | 367.34 / 117.34 |
| S1-4 | 0.84 |
| S1-5a | 192.34 |
| S1-5b | 77 pairs, least 142.00 |
| S1-6 | 8 projections, 0 issues |
| S1-7 | 607.66, spare 72.73 |

Files changed:
- s1_spec.yaml
- proposed_params.yaml (pinion_support; new guide_lug_half_width; member_length 1213; stop_pad_r_in 200)
- check_stack.py (sqrt; `screw_block_g_min`; `g_min_screw_block` stack name in `reported()`; `start_minus_core_top`)
- checks_s1.py (S1-4)
- sketch_common.py (k7 per-pose declarations)
- check_sketch.py (S1 controls)
- fixtures/builders.py (`_s1_ctx` drawing-shift helper, `s1_live`, `s1_4_b1`, `s1_5b_b1`, `k7_b12`, `k7_b13`, `k6_b6`)
- fixtures/manifest.yaml

Pre-pass copies of the spec and overlay are in the session scratchpad and are not durable.

## 3. For Sean at STOP S-1

1. **FIX 5, 1 m core class.**
   - The option R stop rule gives stop 267.50 and start 917.50 for the 1 m class.
   - The 1 m core top on the core stop is 1042.50 z_A, so the cutter starts 125.00 inside the uncut core.
   - The rule has no start-above-core term. The Loftsman's candidate term (collet.core_stop_z + L + c - upper.travel_max, with c a cutter clearance) is recorded here but not applied.
   - The 1 m core is the third Q9 option and is not drawn in S1.
   - Decide whether the 1 m class stays a supported option and, if it does, the start rule and c. Park (1209.84), stroke (1025.00) and L (1135.00, buy 1140) are unchanged at c = 0 by the Loftsman's arithmetic.
2. **Base-frame interface (Designer F4).**
   - Screw frame members and guide rods stand on the 12 mm plate top: member_length 1213, rod 12 to 1212 z_A.
   - The alternative needs a cross member under each foot: members through a plate notch onto base-frame cross members, an S2 footprint choice.
3. **No separate pinion bushing (F1).** The pinions ride on the NEMA 23 shafts and bearings. No shaft rating is on file. Mesh load is 26.7 N per pinion (Designer, DERIVED).
4. **New ASSUMED values:**
   - frame_upper.stop_pad_r_in 200 (was 195)
   - ring.guide_lug_half_width 20
   - motor standoff to the ring rim at r 210, with the motor overhanging 8
5. **L_min 885.00 against the drawn L 900, 15.00 spare.** The spare splits 0.84 at the anchor and 14.16 at the guide, so S1-4's least margin is 0.84 at capture_end. The anchor has 0.84 of upward slack.
6. **Zero-margin pairs held by definition:**
   - drill_head|collar = stop.g_stop 25.000 at capture_end, from params stop.height_z.
   - ring|descent_stop C.

## 4. Gameplan lines to change (orchestrator)

| Line | Change |
|---|---|
| l.121 ring.* seed | "pinion support: the NEMA 23 shaft and motor mount (no separate bushing at S1)" (Designer section 7) |
| l.130 spec format | Add `screw_length` stack name `g_min_screw_block` (from the nut_housing\|anchor and \|guide neighbours). Add `sqrt` to the expression functions. |
| l.140 K7 | Plan-separated clause (FIX 4c text). Pose-restricted declarations (FIX 3). Controls K7-Z8, K7-Z9, K7-B11, K7-Z10, K7-B12, K7-B13. |
| l.144 control pointer | Add K6-B6, K7-Z10, K7-B12, K7-B13, S1-4-Z, S1-4-B1, S1-5b-Z, S1-5b-B1. |
| l.150 g_min seed | Base parts include the holder collar ring (collar top 159.84 z_A). drill_head\|collar G stop.g_stop at capture_end. |
| l.179-183 operator-task table | S1 rows from step1.1_designer_spec_signoff.md section 6. |
| l.231 S1-4 | "nut z +/- max(nut length, nut-housing height)/2 at least g_min (K7) clear of the anchor top and guide bottom". Z 0.84. B: top guides 20 low. |
| l.233 S1-5b | Z value 142.00 (bearing to collar top). B: collar 133 high. |
| l.284 detail 1.3 | L = lift stroke + anchor allowance + guide allowance + max(nut length, ring nut-housing height) + 2 g_min. 885.00 / 885.00 / 1135.00, buy 900 / 900 / 1140. |
| Design Notes 1 | "(1.1 (b): the ring carries the motors; the pinions ride on the motor shafts; the drill axial load goes through the drill-to-ring bearing)" |
| Design Notes 22 | "L_min 885.84" is the as-anchored value; the expression value is 885.00. The 1 m start-inside-core result (FIX 5) is open to Sean. |
