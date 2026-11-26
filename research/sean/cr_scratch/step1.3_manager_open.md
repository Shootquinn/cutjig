# Step 1.3 Manager Open (sean): S3, jack-screw section and three-screw inset

Date: 2026-11-25. Step-open pull: commit afe5d27, tree clean. Sources: gameplan Steps rows 1, 1.0 to 1.3 (l.90-94), detail 1.0 (l.118-162), detail 1 common (l.164-176), operator-task table (l.178-186), rubric applicability and M1 (l.188-206), detail 1.3 (l.267-295), Context Recipes (l.440-464), Progress Log (l.468-505), Design Notes 4, 13, 20, 25 to 30, Echo Site Registry (l.685-721), Open Questions (l.725-758); `step1.2_manager_close.md` (all); `step0_manager_close.md` decision 2; `research/sean/accumulator.md`; `docs/sketches/check_sketch.py`, `sketch_common.py`, `check_stack.py`, `proposed_params.yaml`, `s1_spec.yaml`, `s2_spec.yaml`, `s1_checks_r7.json` and `s2_checks_r5.json` keys_read; `step1.2_loftsman_redfirst_signoff.md`, `step1.2_topologist_redfirst_signoff.md`; `step1_quinn_batch1.md`.

TDD precondition (A.4): S3 is a sketch. Its suite is the signed harness (K1 to K9, X1; 230 controls at the 1.2 close) plus S3-1 to S3-3; its outline is `s3_spec.yaml`, signed at (b); its red-first run is (c). Precondition met for opening step 0 and (a). LLM-PLM 8.4 governs (a), (b), (f).

Numbering: done criteria are KC1 to KC14 (K-series as asked; the C keeps them apart from harness checks K1 to K9). Sub-steps are P0 to P10 as at 1.2; file names carry `step1.3_`.

## 0. Findings at open

Numbers are tagged MEASURED (read from a file or a run at this open), DERIVED (arithmetic on those) or DECLARED. The S3-2 preview uses overlay values that are ASSUMED and one working value of mine (E 200 GPa, no overlay leaf).

| # | Finding | Basis | Disposition |
|---|---|---|---|
| O1 | Record defects at open. (a) Design Notes 4 is not unconfirmed: Sean accepted the S3 redefinition at the Step 0 gate on 2026-11-24 (decision 2, "S3 one-screw section plus three-screw inset"); the 1.2 close D4 premise ("still awaiting your confirmation") is wrong. Headers of Design Notes 4, 5, 6, 7, 9 and 16 still read "for Sean to confirm" although all six were accepted at that gate. (b) Steps row 1.0 still reads "Awaiting Sean" (approved, Design Notes 21). (c) Open Questions N2 says the guide pick "is not named in Design Notes 13"; it is now recorded in Design Notes 27 (D2). (d) The D1 ratification (S2 r5 accepted without a fresh M1 on the r4/r5 pixels) is in the Progress Log only, not in the Design Notes 13 S2-r5 row the close recommended | Progress Log row 3 of Step 0 (l.474); `step0_manager_close.md` l.66; gameplan l.91, l.519-529, l.566, l.748, l.546 | STOP S3-0 still runs (Sean asked for it at D4), narrowed to "confirm it stands, name the section screw"; header and record edits in section 5 |
| O2 | Loftsman NOTE 2 member-top tie does not exist, and the tie as written is not sufficient. `s1_spec.yaml` `stack_ties` holds only `holder_flange`; `s2_spec.yaml` has none. `stack_ties` needs a `term` from `check_stack.global_vars`, which has no top-guide term. The chain under the member tops is three DERIVED overlay leaves written as literals with no agreement check: `jackscrew.top_guide_z` 1165 ("anchor_z 265 + length 900"), `frame_upper.member_length` 1213 (top_guide_z + 60 - 12), `frame_upper.member_length_rail` 1225 (top_guide_z + 60). A change to `jackscrew.length` at S3 leaves `top_guide_z` at 1165 and the member tops at 1225 with every check green; NOTE 2's tie alone (member z_max = top_guide_z + profile.height) would also stay green. The overlay holds 19 DERIVED literal leaves, none checked | grep `stack_ties` (MEASURED); `check_stack.py` l.337-364; `proposed_params.yaml` l.110, l.134, l.135 and 16 more DERIVED leaves | Lands at **P0 (step 0)**, before (a) values can move the chain and before (b): a global top-guide term and `stack_ties` rows for members a, b (S1 and S2) and c (S2), plus a K2 agreement lint for DERIVED leaves that carry an `expr` (mandatory on the three chain leaves). Z and B each. Spec edits in accepted S1 r7 and S2 r5 with no drawn change; ORCH-A re-accepts the refreshed records. The Loftsman signs at P0L |
| O3 | S3-2 is red by construction on the current seeds, and detail 1.3 contradicts itself on what a red S3-2 does. Preview (nut centre at park 959.84 + 130 + 6 = 1095.84 z_A to the anchor block top 295: L 800.84; I = pi 6.2^4 / 64 = 72.53 mm^4; E 200 GPa working value): P_cr 223.2 N at K = 1, 55.8 N at K = 2. Moving mass W 20.15 kg (ring 6, drill 8 with top end, gear 3, three NEMA 23 at 1.0, nuts 0.15; bearing has no mass leaf). Per screw: static 65.9 N, capture lift (W + 10.4 kg core) 99.9 N, stall 212.1 N (F_stall 636.2 N = 3 x 2 pi 0.45 x 0.6 / 0.008). P_cr / F at K = 1: 3.39, 2.23, 1.05; at K = 2: 0.85, 0.56, 0.26; SF 3. Every compression case but static at K = 1 fails. Detail 1.3 says "A failure of S3-2 is a finding for the Step 2 screw-size row, not a redraw by itself"; detail 1 common (d) iterates to green and `--accept` refuses any check not pass | DERIVED from overlay `jackscrew.root_diameter`, `ring.*`, `drill.mass`, `gear` mass, `pinion.motor_mass`, `jackscrew.nut_mass`, `liftmotor.holding_torque`, `jackscrew.lead`, `jackscrew.efficiency`, `stop`/`ring` stack; gameplan l.285, l.289; `check_sketch.py accept()` | P1 re-derives with the Designer's inputs and states options; **STOP S3-A** item 2 (Sean rules before (b)); harness form at P4 per the ruling |
| O4 | No screw lies in the XZ plane (screws 30, 150, 270 deg), and the harness has no view for a section through one screw axis. `VIEW_NORMAL` knows `side_xz`, `section_xz` (normal Y) and `plan_xy`; K6, K7 and S1-6 project a placed part at x = r cos theta. A section through the drill axis and screw c (270) is the YZ plane; through a or b it is a radial plane at 150 or 30 deg. The plane, the look direction and the section convention (cut, beyond, removed) are unstated anywhere | `sketch_common.py` l.42-46; `setup_figure` l.87-101; gameplan l.130, l.270 | STOP S3-0 names the screw; P1 sets plane, look direction and convention; P2 declares them; P4 implements the view in K3 to K9 with Z and B before the stub; P5L and P5T sign |
| O5 | TP-7 and TP1.1-9 sequencing. `setup_figure` owns one Axes; `ctx.view` is one view per sketch; K5 to K9 read `axes[0]` (17 sites in `sketch_common.py`, 1 in `checks_s1.py`, 2 in `checks_s2.py`); a declared inset silences the K3 multi-Axes lint (l.1172). S3's inset is `plan_xy` inside a section figure, so TP-7 needs a view per Axes, a harness change larger than an iteration loop. TP1.1-9 (zero-area Rectangle passes K5) also bears on S1 and S2 | MEASURED grep counts; Design Notes 20 TP-7, 25 TP1.1-9 | TP1.1-9 lands at **P0** (it changes K5 on accepted S1 and S2; any zero-area patch there surfaces before S3 work). TP-7 lands at **P4 (c), before `s3 --rev 0`**, after (b) has fixed the inset declaration format; B controls plant an inverted inset, a mis-projected inset and an inset row drawn in the main Axes. Topologist signs at P5T, verifies at (e) |
| O6 | Block and motor-mount dimensions have no source and are coupled to both accepted sketches. Batch 1 has no row for them (its rows: Q2a to Q2e, Q9, DN23-a to -e, N5 to N10); N12 (NEMA 23 shaft rating) is a next-batch row and concerns S6. Overlay leaves `jackscrew.anchor_allowance` 30, `guide_allowance` 30, `liftmotor.body` 42, `length` 48, `coupling_length` 25, blocks round r 21 by declaration: all "no source". S1 r7 reads 122 keys and S2 r5 128, including `jackscrew.anchor_z`, `anchor_allowance`, `guide_allowance`, `length`, `lead`, `nominal`, `nut_length`, `top_guide_z` and `liftmotor.body`, `length`, `coupling_length` (S2 also `plan_rot`, `position`). S1-4's least margin 0.84 at the anchor is an identity (T2-e): an anchor block taller than 30.84 turns S1-4 red unless `anchor_z` or `length` moves, which moves `top_guide_z` and the member tops (O2). Not read by either: `root_diameter`, `efficiency`, `holding_torque` | MEASURED from `s1_checks_r7.json`, `s2_checks_r5.json` keys_read; `proposed_params.yaml`; `step1_quinn_batch1.md` | P1 proposes values with catalogue basis (ASSUMED) and lists the S1/S2 keys each moves; every such value goes to **STOP S3-A** and opens S1 r8 / S2 r(m+1) under (i). Rows with no source go into a batch 2 draft (P1 section 13); not blocking |
| O7 | A belt sync loop that encloses the drill axis crosses the operator sector. The strand between screws 30 and 150 runs at y = 160 sin 30 + rho = 80 + rho (rho: pulley pitch radius), inside the S2-5a sector (theta 90 +- 45, r 400), which must be free of fixed parts at all z; S2-5a goes red. The same strand sits 80 + rho from the axis, against the cutter r 88.90 sweeping to 184.84 z_A at capture_end, and near knee height where the collet-change row kneels with hands at r <= 115. A loop that does not enclose the axis (both strands through the 210 and 330 deg sides) avoids the sector; a single controller with home switches avoids all three | DERIVED from `jackscrew.pitch_radius` 160, `jackscrew.angle`, `operator.sector_*`, `drill.head_od`; gameplan S2-5a row l.258, operator rows l.182-183 | P1 states both sync options with this cost; if the drawn option is a belt, its routing goes to **STOP S3-A** (it touches accepted S2-5a), the pick of method stays at M2 |
| O8 | N2 hidden-line renderer and leader placer do not exist (D5: before the first S3 draw). Today K8 cover and the K4 leader rules police the figure after drawing; `place_labels` re-anchors only on the row's ink and falls back silently (the S2 r5 fall-back to the r4 anchor, Design Notes 30). Five of seven 1.2 revisions came from this class (close section 5). The renderer must also serve a section view, which does not exist until P4 | `sketch_common.py` l.218-345, l.2447-2590; close section 5 | Plan renderer, leader placer, TP1.2-13 and TP1.2-19 at **P1R**, after step 0 and in parallel with (a) and STOP S3-A; applied to `s2_plan.py` it changes S2 pixels (ring rim under the guide arms dashed; descent-stop leader), so S2 opens r6 under (i) and runs (e) changed rows, (f) fresh M1 with S3, (g) M2 with S3. Section-view convention added at P4. `s1_side_poses.py` stays off the renderer and must stay pixel-equal under the new library; otherwise S1 r8 |
| O9 | Controls runtime 794 s serial (MEASURED at the 1.2 close); `controls()` runs the 230-row manifest in one process; this machine has 16 logical CPUs (MEASURED, `nproc`). Every agent below runs controls at least once; at 794 s the step pays about 15 runs x 13 min | `check_sketch.py controls()` l.232-262 | **P0 task 1**: `--controls --jobs N` with per-control results equal to a serial run, and `--only` for (d) iterations (never a record). Target: full set at most 200 s wall at the default jobs (MEASURED by P0, reviewed by P0S). Runs of record (end of (c), each revision's final run, accept, close) use the full set |
| O10 | Summary does not carry the detail's Reported list (D3). `write_summary` prints S1-centric park-rule lines plus whatever the script hands in `reported_drawn`; nothing compares the summary with the spec. S2 r5's summary lacks three of the four J13 items | `check_sketch.py write_summary()` l.343-376; close J13 | **P0**: spec field `reported_items`; summary row per item; check RPT (absent value fails; cause absent on the stub); `--accept` refuses through RPT. From S3 on; S1 r7 and S2 r5 exempt by record (accepted before the rule) |
| O11 | S3-3 reads figures of other sketches, and its chain is wrong for one screw. No check reads another sketch's figure or record (X1 reads specs only). The detail 1.3 chain "base plate, anchor frame member" holds for members a, b (on the plate top); member c stands on the base-frame rail inside `base.column_notch` (Design Notes 27), so its chain is base plate, base frame, member c. Member c's foot is drawn only in the S2 plan; no side view draws screw c | gameplan l.286; Design Notes 27; `s1_spec.yaml` rows frame_upper_a/_b only | (b) spec carries the chain per screw and names the record certifying each pair; P4 writes S3-3 to read the K7 entries of the latest accepted S1 and S2 records (premise: `--stale` clean, enforced in the check) plus the S3 figure; S3-3 row edit at the (b) save point |
| O12 | The lead back-drives, and the hold-device option couples to accepted keys. T8 lead 8 (4-start, pitch 2, mean diameter about 7.0): lead angle 20.0 deg against a friction angle about 8.8 to 11.7 deg (mu 0.15 to 0.20, ASSUMED, 30 deg thread). A non-back-driving lead (e.g. lead 2) changes `jackscrew.lead`, read by S1 r7 (screw label), and raises F_stall about four-fold at equal efficiency, which deepens O3 | DERIVED; `s1_checks_r7.json` keys_read | P1 states the hold options with cost; a lead change goes to STOP S3-A; the pick is at M2 (detail 1.3) |
| O13 | Harness hard-codes S1 and S2 in places S3 will hit: `run_control` routes only `S1-` and `S2-` checks to `checks_sN.py` (l.187) | `check_sketch.py` l.187 | P0 R4: generalise to `S<n>-`; P0 lists any other hard-code |
| O14 | S3-2 and the load cases need inputs that have no overlay leaf: E, SF, K per mounting, F_bind, rapid traverse (critical speed), screw-nut friction (back-drive), bearing mass. `loads.axial_design` 1000 N (ASSUMED) and `loads.wob_max` (VERIFIED) exist in params | grep `proposed_params.yaml`, `params.yaml` loads | P1 proposes each (ASSUMED, source stated); Sean owns SF and F_bind (detail 1.3); STOP S3-A |

## 1. Scope, done criteria, sequence

### 1.1 Scope (gameplan detail 1.3)

Question S3 answers: how is each screw anchored, guided, driven and synced, does the 1000 N axial load put it in tension, what holds the ring with power off, and does the axial load loop close? One section figure through one jack screw, with a plan inset (end view) of all three screws and the sync loop. Shows: bottom anchor with thrust bearing, screw (8 mm, lead labelled), brass nut on the ring with its mounting (option drawn), top guide, NEMA 17 mount and coupling, power-off hold device (option drawn), load arrows per load case, frame member with anchor and guide and its connection to the base. Closes R14 (path and loop), Q7 detail, Q8 (powered feed), DN23 sync and anchoring items, the TR10/TR12 fallback check, the axial-loop half of SE-2. Checks K1 to K9, X1, S3-1 to S3-3, RPT (new, O10).

Carried in (detail 1.3 carried paragraphs; Design Notes 20 TP-7; Design Notes 25 TP1.1-9, TP1.2-13, TP1.2-18/19, T2-b, T2-c, LF1.1-9 to -11; Step 1.2 gate D3, D5): sequenced by this file as follows.

| Carried item | Lands at | Owner; signs |
|---|---|---|
| Member-top stack tie (Loftsman NOTE 2) plus DERIVED-leaf agreement lint (O2) | P0, before (b) | The Engineer; The Loftsman (P0L) |
| Fast controls set (D5, close item 5) | P0 task 1 | The Engineer; The Software Engineer (P0S) |
| Summary carries every Reported item (D3, close item 6) | P0 | The Engineer; The Software Engineer (P0S) |
| TP1.1-9 zero-area K5 lint | P0 | The Engineer; The Topologist (P0T) |
| TP1.2-18 `stand_in_owner` names a Step or sketch id | P0 | The Engineer; The Topologist (P0T) |
| Topologist 1.2 (c) NOTE 2, `sense_lint` checks the value of `frame` | P0 | The Engineer; The Topologist (P0T) |
| Loftsman 1.2 (c) NOTE 1, side swept reads the fixed row's neighbour list | P0 | The Engineer; The Loftsman (P0L) |
| N2 hidden-line renderer (plan), leader placer, TP1.2-13 over-cover, TP1.2-19 annulus sampling and `is_opaque` | P1R; S2 r6 under (i) | The Engineer; The Topologist and The Designer co-sign (P1Rt, P1Rd) |
| Block and motor-mount dimensions (T2-b, LF1.1-9 to -11) | P1 (a); STOP S3-A for any S1/S2 key | The Designer proposes; Sean picks; The Loftsman re-checks at (e) |
| Hold device option (T2-c) | P1 (a) option; drawn at (d); pick at M2 | The Designer; Sean |
| TP-7 per-Axes view and inset iteration | P4 (c), before the stub | The Engineer; The Topologist (P5T, and (e)) |
| Section view for the picked screw (O4); renderer section convention | P4 (c) | The Engineer; The Loftsman (P5L), The Topologist (P5T) |
| S3-3 cross-record read, per-screw chain (O11) | P2 chain; P4 check | The Engineer; The Loftsman |
| Topologist 1.2 (c) NOTE 1 (radial symmetry is no predicate; M1 reads it) | every M1 from S3 on | The Designer (M1) |

Rulings in force: Design Notes 21 to 30 and the Step 1.2 gate D1 to D5 (Progress Log l.505). Accepted state: S1 r7, S2 r5 (`docs/sketches/`, `--stale` 2 records, 0 differences).

### 1.2 S1 r8 and S2 r6 inside 1.3

S2 r6 opens at P1R (renderer and placer change S2 pixels; no key moves). Either sketch opens a further revision when Sean adopts at STOP S3-A (or M2) a value for any key in its accepted record's `keys_read` (O6: most S3 leaves are such keys).

| Stage | Who | Rule |
|---|---|---|
| Overlay edit | The Engineer at P2 | After the edit `--stale` reads red on s1 r7 / s2 r5 listing exactly the adopted keys; recorded, never suppressed |
| Redraw | The Engineer at P1R (S2 r6), P6 (any key-driven revision) | to `docs/sketches/wip/`; S1 18/18, S2 17/17 required; script edits only where an expression must change |
| Cross-review | The Loftsman and The Topologist | changed rows only, hand value beside JSON value (P1Rt for the renderer; P7a, P7b for key changes) |
| M1 | The same fresh Designer spawn as S3 (P8) | separate files `wip/s2_visual_gate_r<m>.md`, `wip/s1_visual_gate_r8.md`; S2 V2, V6 to V10; S1 V1 to V10 |
| M2 | Sean, same stop as S3 | old and new PNGs side by side with the moved values |
| Record | Orchestrator | `--accept` supersedes the earlier record |

### 1.3 Done criteria (Step 1.3 closes when all hold)

| # | Criterion | Evidence |
|---|---|---|
| KC1 | Member-top tie and DERIVED-leaf agreement lint, each with Z and B, red-first on pre-change code; S1 r7 18/18 and S2 r5 17/17 with record differences limited to the listed fields; PNGs pixel-equal; Loftsman PASS; re-accepted; `--stale` clean | P0, P0L; ORCH-A run log |
| KC2 | `--controls --jobs N` per-control equal to a serial run; full-set wall time MEASURED against 200 s; `--only` never read by `control_tally` or `--accept`; Software Engineer PASS | P0, P0S |
| KC3 | RPT and `reported_items`: Z and B; `--accept` refuses on a missing item; S1 r7, S2 r5 exempt by record | P0, P0S |
| KC4 | TP1.1-9, TP1.2-18, Topologist NOTE 2, Loftsman NOTE 1: each with Z and B, signed by its raiser; S1/S2 stay green or open a revision | P0, P0T, P0L |
| KC5 | Plan renderer and leader placer with Z and B (incl. TP1.2-13, TP1.2-19), signed by The Topologist and The Designer; S2 r6 drawn by them, 17/17; placer reports every UNPLACEABLE label (no silent fall-back); S1 r7 pixel-equal under the new library | P1R, P1Rt, P1Rd |
| KC6 | (a) params review of every S3 key; shape notes; section plane, look direction and convention; block and motor-mount values; options (nut mounting, sync, hold, anchoring) with cost; S3-2 and load inputs; operator rows; STOP S3-A rulings recorded as Design Notes 31 | P1; Design Notes 31 |
| KC7 | (b) `s3_spec.yaml` signed by The Designer (part list) and The Loftsman; load-case table; `reported_items`; S3-3 chain per screw with the certifying record per pair; shared rows equal (X1) | P2, P3a, P3b |
| KC8 | (c) TP-7 per-Axes view and inset iteration; section view; renderer section convention; S3-1 to S3-3 per the signed spec and Sean's S3-2 ruling; S3-x fixtures; `--controls` green; `s3 --rev 0` red by cause; `--baseline s3`; Software Engineer, Topologist and Loftsman PASS | P4, P5, P5T, P5L |
| KC9 | (d) `docs/sketches/s3_jackscrew_section.py`; K1 to K9, X1, RPT, S3-1 to S3-3 green on the accepted revision (S3-2 per ruling); inset shows all three screws and the sync method; drawn through the renderer and placer | `wip/s3_checks_r<k>.json`, then `docs/sketches/` |
| KC10 | (e) Loftsman and Topologist PASS with hand values (P_cr, F_stall, L_min, critical speed, back-drive, kept-part axial forces, anchor below nut below guide, chain order); LF1.1-9 to -11 re-checked | P7a, P7b |
| KC11 | (f) fresh image-capable M1 PASS on the exact pixels Sean accepts, for S3 and every S1/S2 revision accepted in 1.3 (or a pixel-equality statement to a revision with a PASS file); reviewer controls scored (1.2 close J10 gap) | `wip/s3_visual_gate_r<k>.md` and S1/S2 equivalents |
| KC12 | (g) "S3-r<k> accepted" (and S2/S1 rows) with date in Design Notes 13; picks recorded (nut mounting, sync method, hold device, anchoring); `--accept` with copy-up equality; `--stale` clean on every latest record | Design Notes 13; run log |
| KC13 | Reported (never asserted), each a row of `s3_summary_r<k>.md` through RPT: L_min per Q9 option; critical speed with end factor; P_cr margin per compression case and K; F_stall; axial force in each kept part (collet, holder, receiver, base plate) at 1000 N and at F_stall (for N5); back-drive; per-screw share and two-screw share | `s3_summary_r<k>.md` |
| KC14 | Gameplan lines applied at each save point; one Progress row per agent return; insertions name their anchor; Manager close audits and writes accumulator entries | P10 |

### 1.4 Sequence

STOP marks the orchestrator halting for Sean. Background: **required** for every Engineer spawn and any spawn that runs `--controls` (794 s until P0 lands; P0 reports the new time) or any process over 30 s; recommended elsewhere. One Engineer spawn at a time (shared tree).

| # | Sub-step | Who | Mode | Runs after | Background |
|---|---|---|---|---|---|
| **STOP S3-0** | Design Notes 4 confirm; section screw | Sean | human, blocking | open | — |
| P0 | Step 0 harness: parallel controls (first), member-top tie and DERIVED lint, RPT, sN generalisation, four lints; S1 r7, S2 r5 re-runs | The Engineer | agent, **parallel with P1** | S3-0 | **required** |
| P1 | (a) params review for S3 | The Designer | agent, **parallel with P0**, then with P0L/P0T/P0S/P1R | S3-0 | recommended |
| P0L, P0T, P0S | step 0 checks (tie, NOTE 1; TP lints; controls runner, RPT) | The Loftsman; The Topologist; The Software Engineer | agents, **all three parallel** | P0 | P0S **required** (re-runs controls); others recommended |
| P0f | fix pass if FIX; re-check by raisers only | The Engineer, raisers | agents | P0 reviews | **required** for P0f |
| ORCH-A | re-accept s1 r7 and s2 r5 (refreshed records); `--stale`; gameplan lines; save point 1 | orchestrator | run, edit, git | P0 reviews PASS | — |
| P1R | plan renderer, leader placer, TP1.2-13/19; S2 r6 | The Engineer | agent | ORCH-A | **required** |
| **STOP S3-A** | P1 values that move S1/S2 keys; S3-2 disposition; belt routing; lead change; inputs Sean owns | Sean | human, blocking for P2 | P1 and ORCH-A (may overlap P1R) | — |
| P1Rt, P1Rd | renderer and placer sign-offs; S2 r6 changed-row read | The Topologist; The Designer | agents, **parallel** | P1R | recommended |
| P1Rf | fix pass if FIX; re-check by raisers | The Engineer, raisers | agents | P1Rt, P1Rd | **required** for P1Rf |
| — | gameplan lines; Design Notes 31; save point 2 | orchestrator | edit, git | P1R signed and S3-A ruled | — |
| P2 | (b) overlay values, `s3_spec.yaml`, `checks_s3.py` skeleton, check_stack on S3 | The Engineer | agent | save point 2 | **required** |
| P3a, P3b | (b) spec sign-offs | The Designer; The Loftsman | agents, **parallel** | P2 | recommended |
| P2f | (b) fix pass if FIX; re-sign by raiser | The Engineer, raiser | agents | P3 | **required** for P2f |
| — | gameplan lines; save point 3 (spec signed) | orchestrator | edit, git | P3 SIGNED | — |
| P4 | (c) TP-7, section view, renderer section convention, S3-1 to S3-3, S3-x fixtures, stub, `s3 --rev 0`, `--baseline s3` | The Engineer | agent | save point 3 | **required** |
| P5, P5T, P5L | (c) checks | The Software Engineer; The Topologist; The Loftsman | agents, **all three parallel** | P4 | P5 **required**; others recommended |
| P5f | fix pass if FIX; re-check by raisers | The Engineer, raisers | agents | P5 reviews | **required** for P5f |
| — | gameplan lines; save point 4 | orchestrator | edit, git | P5 reviews PASS | — |
| P6 | (d) draw S3 r1 to wip/, iterate to green; S1/S2 key-driven revision if triggered | The Engineer | agent | save point 4 | **required** |
| **STOP-T5** (non-blocking) | first `wip/s3_*_r1.png`: V1, V5, inset handedness | Sean | human | PNG mtime | — |
| P7a, P7b, P8 | (e) cross-review and (f) fresh M1 on r1 (S3; S2 r<m>; S1 r8 if any), **all three parallel** | The Loftsman; The Topologist; The Designer (fresh, image-capable) | agents | P6 | recommended |
| — | orchestrator scores reviewer controls against `wip/fixtures/figs/key.json` | orchestrator | read | P8 | — |
| P9 | (h) one revision from (e), M1, T5 together; every value-setting FIX dry-run first (detail 1 common (h)) | The Engineer | agent | P7, P8, T5 | **required** |
| P7r, P8r | raiser re-checks; then fresh M1 on the new revision | raisers; The Designer (fresh) | agents | P9 | recommended |
| — | gameplan lines; save point 5 (pre-M2) | orchestrator | edit, git | M1 PASS on the exact pixels | — |
| **STOP M2** | correction pass and picks | Sean | human, blocking | save point 5 | — |
| ORCH-B | `--accept s3`, `--accept s2 --rev <m>`, `--accept s1 --rev 8` if any; `--stale`; save point 6 | orchestrator | run, git | acceptance | — |
| P10 | Manager close | The Manager | agent | ORCH-B | **required** |

Loop cap: one fix pass per review (P0f, P1Rf, P2f, P5f, P9 after P7/P8). A second round on the same finding class goes to the orchestrator for a ruling. A FIX that names a value, field setting or coordinate carries a harness dry-run; a FIX that fails its dry-run returns to the raiser and opens no revision (detail 1 common (h)).

T5 rule: the orchestrator polls `docs/sketches/wip/s3_*_r1.png` mtimes while P6 runs. Sean's words go to Design Notes 13 as `S3-r1` and into P9.

Reviewer independence: P8 and every P8r are fresh Designer spawns that produced no figure and did not sign the renderer (P1Rd). Nobody in the reviewer packet opens `key.json`. If ctrl_a passes V3, ctrl_b fails, ctrl_c fails handedness or ctrl_d passes it, the reviewer model is replaced and P8 re-runs before any sketch is gated.

## 2. Stops for Sean

| Stop | When | Sean sees | Sean answers | Orchestrator then |
|---|---|---|---|---|
| **STOP S3-0** (blocking) | At open, before any spawn | The question below | One option | Design Notes 4 header per section 5 item 4 with Sean's words and the screw; Progress row; pass the screw to P0 (none needed) and P1 |
| **STOP S3-A** (blocking for P2) | After P1 and ORCH-A | From P1 section 12: (1) every value that moves a key S1 r7 or S2 r5 reads, with the S1/S2 rows that move (opens S1 r8 / S2 r(m+1)); (2) S3-2 disposition with options; (3) sync: if the drawn option is a belt, its routing against S2-5a; (4) hold device: if the drawn option changes `jackscrew.lead`; (5) inputs Sean owns (SF, F_bind) and the other no-source inputs (accept ASSUMED or give a value); (6) batch 2 draft (send or hold) | Pick per item, or corrections; items he defers go to M2 with P1's recommendation drawn | Design Notes 31 "Step 1.3 STOP S3-A rulings" with Sean's words; Progress row; hand to P2 |
| **STOP-T5** (non-blocking) | First `wip/s3_*_r1.png` during P6 | S3 PNG; S2/S1 PNGs of any key-driven revision | V1 (floor at the bottom, motor and nut hang as stated), V5 (screw vertical, anchor at the bottom, guide at the top, nut on the ring), inset handedness (+X right along slot line C, theta counter-clockwise from +X seen from +Z, screws at 30, 150, 270) | Design Notes 13 `S3-r1`; into P9 |
| **STOP M2** (blocking) | After M1 PASS on the exact pixels and save point 5 | S3 PNG, `wip/s3_visual_gate_r<k>.md`, `wip/s3_summary_r<k>.md`; S2 r<m> (and S1 r8) beside the accepted revision with the changed items | V1, V5, V9 yes/no; free corrections; picks: nut mounting (rigid or floating, sets K), sync method, hold device, anchoring (thrust bearing type, top guide type); acceptance of S3 and of each S1/S2 revision | Design Notes 13 rows; picks also into Design Notes 31; ORCH-B on acceptance |
| Decision mid-step (only if raised) | P2 or P4 reports a check red by construction on the ruled values, or P3b rules an S1/S2 spec change beyond comments | the conflict and the raiser's options | pick | Design Notes 31 addendum |

**STOP S3-0 question (exact text to put to Sean):**

> Design Notes 4: S3 is a side section through one jack screw (bottom anchor with thrust bearing, screw and lead, nut and its mounting, top guide, NEMA 17 and coupling, power-off hold device, load arrows, axial loop) plus a plan inset of all three screws and the sync loop. You accepted this at the Step 0 gate (2026-11-24, decision 2); the 1.2 close listed it as unconfirmed. Does it stand, and which screw does the section cut?
> - **A. Stands; section through screw c (theta 270).** Member c is the odd one: it stands on the base-frame rail in Quinn's column notch (length 1225), no side view draws screw c, and the S3-3 chain for it runs base plate, base frame, member c. The section plane is the YZ plane through the drill axis.
> - **B. Stands; section through screw a or b (theta 150 or 30).** Member on the plate top, as S1 already draws it; member c's foot is certified only by the S2 plan record. Radial plane at 150 or 30 deg.
> - **C. Stands, with the three-screw plan as a second figure instead of an inset.** Removes the mixed-view figure; TP-7 (per-Axes checks) moves to S6, the next sketch with an inset.
> - **D. Redefine S3** (state what it shows).
>
> Recommendation: **A.** The Designer fixes the look direction and the section convention at (a).

## 3. Spawn prompts

Each prompt is complete except the persona block and the common context, which the orchestrator pastes verbatim from section 3.0 at the marked lines. Paths are relative to the project root. `<screw>` is Sean's STOP S3-0 answer; the orchestrator substitutes it.

### 3.0 Persona blocks and common context

**[BLOCK DES] The Designer**
```
SYSTEM: You are The Designer, design critic for physical products and technical documents.
Biographical anchors: Author of The Design of Everyday Things (1988), founding director of the Design Lab at UC San Diego, VP of Apple's Advanced Technology Group. He spent decades studying why well-intentioned designs fail and what makes the difference between a product people tolerate and one they love. His framework (affordances, signifiers, constraints, mappings, feedback, and conceptual models) applies to everything from door handles to technical documents to 3D-printed RC cars.
Your characteristic approach: For physical products, evaluate: Does the design communicate its intent? Would the user understand what to do without being told? Does the product look like something its creator is proud of? Are error-prone operations designed out or designed to be recoverable? In CAD/PLM work your review extends to the params level: a parameter set that describes a functional part as a dimensionally correct but geometrically non-representative placeholder is a design failure you catch before geometry exists. Your visual gates run only on an image-capable model.
Your role on this team: params review (LLM-PLM 8.4a), representative-shape notes (8.4b), spec sign-off with the shape-text part list, operator-task table, and the M1 visual gate (8.4c) on an image-capable model; co-owner, with The Topologist, of the hidden-line renderer and leader placer conventions. The Engineer draws; you did not produce the images you gate (gameplan Design Notes 3).

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0, Wave 2): Review found 0 BLOCKS, 10 FIX, 5 NOTE, with a 12-item Manager close checklist (all items met at close). All accepted and applied except the D3 sub-item (premise wrong). Notable accepted fixes: governing line over the superseded "Start here" lines (D1), drill drawn with distinct head and top-end block, cutter OD ASSUMED and 152.4 labelled as tube OD (D4), S1-5 split into core-to-bore-ceiling and ring-to-base checks (D5), pose table (D6), `ring.*` seeded with functional features (D7), power-off hold and hard-stop rows (D8), operator-task table and rubric V10, captured-core removal owned (D9), S4 orientation predicates for kept parts (D10), Echo Site Registry rows (D12). Correction received: D3 misread the INSITU2 range. Positions that remain relevant: Designer owns params review, representative-shape notes, spec sign-off and the M1 visual gate on an image-capable model at every sketch; a functional part seeded as an outline fails the params review.
- Cycle 1.1 (Step 1.1, S1): P1 params review set the G3 values (ring 130 above the tip, anchors 265, allowances 30/30/30, L 900 under option R), confirmed G4 (core stop 42.5), flipped both TP-2 taper senses, wrote the pose table, shape notes, S1-7 row, TP-9 wording and operator rows; Sean adopted option R and the values (Design Notes 22, 23). P3a sign-off: 6 FIX (standoff overhang, lug width, base-plate nests replaced by members on the plate top, pad radius 200, rod text, pinion support), all closed; SIGNED. NOTES N1 to N6 carried (keep-out pair, theta 270 member overhang 26, bushing length, Design Notes 1 against the bearing, tilt margin, NEMA 23 in every sector). M1 at r2 as a fresh image-capable reviewer: controls scored correctly (ctrl_a FAIL V3, ctrl_b PASS); S1 FAIL with F1 to F7; F1 to F5 fixed in r3; F6 (ring rim hides the end of the cut) assigned to Step 2 and S2 and accepted by Sean; r3 and r4 PASS except F6. Corrections received: his (a) review listed the 1 m start at 917.5, inside the uncut core (Loftsman FIX 5); r2 F1 (a) called the shaft-pinion N pair already declared (self-corrected at r3); his (b) sign-off passed shape text naming bracket arms, a pad support and shafts that had no rows, which his M1 then failed. Positions that remain relevant: (b) sign-off now carries a shape-text part list (detail 1 common (b)); projected_extent is containment only, so M1 checks parts drawn narrower than their footprints; bracket values are ASSUMED until Step 2.
- Cycle 1.2 (Step 1.2, S2): params review (21 PASS, 7 FAIL with leaves): radius 274 (option A), O1-B split of S2-5, operator sector theta 90 +- 45, guide tie, LM20UU housing; Sean accepted all but the three-pad proposal (one pad kept). Spec sign-off FIX 4 then SIGNED with a 41-row part list. Fresh M1 spawns: S2 r1 FAIL F1 to F5, S2 r2 FAIL F1 (leaders under the gear fill), S2 r3 PASS; S1 r5 FAIL F1 (note clipped), S1 r6 FAIL F1 (core-750 leader under hatch, present in accepted r4), S1 r7 PASS; reviewer controls scored correctly every time. Signed the r2 to r4 rules. Corrections received: tick toe 95.22 ruled against (Design Notes 29, pitch point 96.54); D4-1 premise wrong (anchor 3.1 mm outside tie b, proposed anchor inside the bracket outline, 150 leader fails the hatch rule; Design Notes 30). Positions that remain relevant: a FIX that sets a coordinate needs a harness dry-run before it is issued; the ring rim under unfilled guide arms goes to the S3 hidden-line renderer, co-owned with the Topologist.
```

**[BLOCK ENG] The Engineer**
```
SYSTEM: You are The Engineer, the team's jack-of-all-trades engineer with a bias toward action.
Biographical anchors: JPL Chief Engineer for the Curiosity and Perseverance Entry, Descent, and Landing systems. Author of The Right Kind of Crazy (2016). Led the team that invented the sky crane, the system that lowered a car-sized rover to the Martian surface on cables from a hovering rocket platform, a concept dismissed as insane until the team proved it worked. Twice. His career spans mechanical engineering, electrical engineering, systems integration, and project leadership. He does not specialize; he solves whatever the hardest problem is.
Your characteristic approach: "Test as you fly, fly as you test." Write the code, run it, verify the output, report results with evidence. Break impossible-seeming problems into testable pieces, test each piece, build confidence from evidence. Laconic; just the facts.
Your role on this team: you write all production code, run every check, and produce empirical evidence. On this sketch you write the harness changes, the renderer and leader placer, the spec, the fixtures and the sketch script and iterate to green. Design values go to Sean or The Designer; you never choose them in the harness.

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0): Drafted research/sean/gameplan.md from templates/gameplan.md (Objectives, Steps 1.0 to 7, step details, Context Recipes, Design Notes 1 to 13, Open Questions with N-rows). Accepted with modification: the Software Engineer rewrote Steps and details for TDD; Wave 2 raised 33 findings (SE 2 BLOCKS, 13 FIX, 3 NOTE; Designer 10 FIX, 5 NOTE). Revision applied all 33; rejected one sub-item (D3, sending an INSITU2 discrepancy to Quinn) with a correct reason. Ruled the seven Software Engineer vs Systems Engineer tensions (Design Notes 15, T1 to T7). Corrections received: drill drawn as a symmetric rectangle defeats orientation checks (D4); lift stroke conflated with travel (SE-3); drill-to-ring bearing and the axial loop through the kept base unowned (SE-1, SE-2); ring specified as an outline (D7). Positions that remain relevant: execution of shared-file changes waits for Quinn's review of the proposal (T4); one decision locus, sketch M2 decides and Step 2 consolidates (T3); Engineer draws sketches, Designer gates (DN3).
- Cycle 1.0 (Step 1.0): Wrote step3_check.py Q3-0 (red on empty, Z pass, B fire) and question batch 1 (17 rows incl. N10), approved by Sean as drafted and pushed. Wrote the sketch harness: sketch_loader.py split out so check_stack.py imports the loader only, sketch_common.py K1 to K9, check_stack.py (z_A evaluation, one conversion to z_S), check_sketch.py (--controls, --stale, --baseline), checks_s1.py, draft s1_spec.yaml, S1 stub, 41 controls. Wave 2 raised 3 BLOCK, 22 FIX, 21 NOTE; revision accepted all BLOCK and FIX, each with a new control (68 controls: Z 17, B 50, smoke 1); reproduced each defect against the Wave 1b code before claiming the fix. Corrections received: spec key `on:` parsed by YAML as True crashed K8 (SW-1); disjoint depth bands masked C and G failures (LF-1); artist transforms ignored, so a drawn part could sit anywhere (TP-1); B controls matched on exit code alone (SW-2). Edited gameplan l.140 outside his write scope (ratified at close). Positions that remain relevant: the draft overlay does not fit the lift (stroke 830.16 against travel 650; S1-4 red); the start pose is travel-defined in params, so "first contact" in the pose table contradicts `stop.start_z`; design values go to Sean or the Designer, never chosen in the harness.
- Cycle 1.1 (Step 1.1, S1): Wrote the S1 spec revision and overlay from the Designer's values (P2), the LF-16 lint, S1-7 and the R6 dispositions; fix pass on 11 sign-off FIXes (P2f: collar row, S1-4 band with g_min from the spec, pose-restricted K7 declarations, plan footprints containing their parts); 14 S1-x fixtures red-first (99 controls); `s1_side_poses.py` green on run 1 (r1); revisions r2 (cross-review), r3 (Designer M1 F1 to F5), r4 (re-checks); P10 move of 34 files to `docs/sketches/` with equal results. Ended at 117 controls (Z 35, B 81, smoke 1), S1 17/17, each new control run red against the pre-fix code first. Accepted by Sean as S1 r4. Corrections received: holder flange 8 mm low (LF1.1-1); gear taper predicate passed a falling face, "absent at park" unchecked, holder|collet interference hidden by class N (TP1.1-1 to -3); S1-4 band ignored g_min, so S1-4-B1 read clean on the pre-fix code (Loftsman FIX 2); shape-text parts undrawn and labels overlapping (Designer F1 to F5); plan-contact certified the spec and not the drawing, and the member footprint was the inscribed circle (TP1.1-11, -12, LF1.1-8); gear lower bound 15.43 was a projected separation, true 54.65 (Loftsman r3). At close: Sean's FIX 5 ruling (Design Notes 23, 1 m start-above-core term) is not in the accepted spec (Design Notes 25 H5). Positions that remain relevant: a relief rule needs its premise enforced by a check; `docs/sketches/` is the only working copy (H2); the accepted flag, `--baseline sN` and the output location are his 1.2 step 0 items (H1, H3, H4).
- Cycle 1.2 (Step 1.2, S2): step 0 harness (--accept, r0 record and --baseline sN, wip/ output rule, H5 park-rule text; found that Design Notes 23 holds exactly only for c <= 42.34, accepted by the Loftsman); S2 spec (70 rows, 47 shared with S1) and fix pass; plan-view harness rules and S2-x fixtures at (c) with every new B red-first on pre-change code; S2 r1 to r5 and S1 r5 to r7; controls 126 to 230. Every BLOCK and FIX closed; S1 r7 and S2 r5 accepted with no Sean corrections. Disproved the Designer's D4-1 fix by measurement (end-quarter hatch rule, anchor inside the bracket outline, 5 deg candidate scan), ruled closed with no geometry change (Design Notes 30). Corrections received: TP1.2-1 (radial outboard ran in side views), TP1.2-3 (S2-5b hand list), LF-c1 (pose-restricted pairs in the swept form), Software Engineer FIX 1 to 5. Positions that remain relevant: the hidden-line renderer for solid pieces under unfilled covers is the right fix and belongs at S3 (c); controls runtime needs a fast set before S3.
```

**[BLOCK LOF] The Loftsman**
```
SYSTEM: You are The Loftsman, geometric reasoning, analytical lofting and computational geometry.
Biographical anchors: Inspired by Roy A. Liming (d. ~1970s), North American Aviation, author of Practical Analytic Geometry with Applications to Aircraft (1944) and Mathematics for Computer Graphics (1992). Two books, two halves of one career. The 1944 book came out of the wartime work that produced the P-51 Mustang, the first aircraft whose surfaces were defined analytically instead of by physical templates. Lofting is a centuries-old discipline from the shipbuilding mould loft; Liming put that practice on a mathematical footing using conic sections, so any point follows to high precision from the pencil equation for its family of conics. The 1992 book is the same mind turned on the machine that has to draw the surface: how a surface is parameterised so a machine can walk it, and what survives the passage from a continuous definition to a sampled raster.
Your characteristic approach: second- and third-degree curves, conic sections solvable with pencil and paper. Define geometry via equations, laws and control curves. Verify by inspection and by hand arithmetic. Of any mapped quantity ask its domain, its period, and whether it closes.
Your role on this team: challenge every geometric claim against real mathematics; arithmetic, placement and transformation math for the sketch stack, projection and overlap; on S3 also the section-plane coordinates, the screw length, buckling and stall arithmetic. You sign sketch specs where cross-review applies and cross-review the drawn sketch.

SESSION HISTORY (your prior contributions):
- Cycle 1.0 (Step 1.0, Wave 2 geometry cross-review of K6, K7, S1-6, check_stack.py): 1 BLOCK, 6 FIX, 8 NOTE; hand values written beside code values (collar top 159.84 z_A / 219.84 z_S, pose tips, stroke 830.16, screw_a band, kernel cases). BLOCK LF-1: disjoint depth bands passed C and G pairs; rule now "bands settle F only; C fails when band gap > 0.05; G passes on max(band gap, XZ distance) >= g_min", in one `assess_pair` used by K7 static, swept and S1-5b, and in gameplan l.140. Accepted FIXes: frame sign anchors in K6 (LF-2), swept hull per convex piece (LF-3), convexity guard (LF-4), depth bands from placement (LF-5, with TP-4), one `load_plane` spec field (LF-6), one core-stop function (LF-7). LF-6 and LF-7 design values went to Sean's gate. Re-check PASS; new NOTEs LF-16 (`load_plane` names one plane twice with no agreement lint; to 1.1 (b)) and LF-17 (gameplan swept wording; fixed at close). Positions that remain relevant: the park rule's load plane (core_stop 42.5 or collar_top 159.84 z_A, 117.34 apart) is a design choice; side-view K7 is a box test until S2 supplies an XY footprint (LF-8).
- Cycle 1.1 (Step 1.1, S1): P3b spec sign-off NOT SIGNED with 5 FIX (collar row and S1-5b reference 142.00, S1-4 band and the screw-length ruling L_min = stroke + allowances + max(nut length, housing height) + 2 g_min, pose-restricted K7 declarations, footprint containment, 1 m start 125.00 inside the uncut core); all closed or sent to Sean (FIX 5, Design Notes 23); SIGNED. The L expression now governs detail 1.3 and S1-4. P7a cross-review PASS with FIX LF1.1-1 (holder flange 8 low; stack tie proposed and adopted) and NOTEs LF1.1-2 to -7; r2 closed LF1.1-1 to -3; r3 signed the plan-contact rule on its containment premise, raised FIX LF1.1-8 (30-6060 member drawn as an r 30 circle; true 60 square, 81.96 projected) and corrected the Engineer's gear lower bound to 54.65; r4 closed LF1.1-8 and amended the l.140 wording (circumscribing footprints admitted for F and G relief; plan-contact needs true sections; member orientation tagged ASSUMED), applied at close. Hand values matched JSON to 0.01 mm throughout. Corrections received: none. Positions that remain relevant: containment is the premise of every plan relief; zero margins (S1-4 0.84, drill_head|collar 25.000, entry plane 0.00) are design identities; LF1.1-9 to -11 go to Step 2 and S3 (blocks, motor mount).
- Cycle 1.2 (Step 1.2, S2): H5 park-rule expression PASS; spec NOT SIGNED with FIX 1 (S1 r5 lacked the S2 housings and ties; Sean chose option A, Design Notes 28), then SIGNED; withdrew his S1-5b expectation 125.00 to 133.80 (a component, not the XZ distance). (c): LF-8 plan K7 signed after FIX LF-c1 (pose-restricted pairs swept as F). (e) S2 r1 and S1 r5 PASS with FIX LF1.2-1 (K7 record pair ids and basis) and LF1.2-2 (pinion|gear_hub undeclared, toe gap 5.22). r2 FIX R2-1 tick toe at the pitch point 96.54, ruled for him (Design Notes 29). Open NOTEs carried to S3: member-top stack tie before S3 (b) (not implemented; S3 can move jackscrew.length); side sweep reads only the moving row's list. Positions that remain relevant: a reviewer expectation is a component until checked against the certified distance.
```

**[BLOCK TOP] The Topologist**
```
SYSTEM: You are The Topologist, B-rep topology and spatial relationship specification.
Biographical anchors: Helsinki University of Technology (now Aalto University), author of An Introduction to Solid Modeling (1988), the foundational text on boundary representation. His work formalized the mathematical framework that underpins every modern CAD kernel: oriented surfaces, half-space classification, Euler operators that maintain topological validity by construction. His framework addresses the class of bugs where geometry is plausible but topology is wrong: slots on the wrong side, segments in the wrong direction, normals pointing the wrong way.
Your characteristic approach: precise geometric specifications: oriented boundaries, half-spaces and topological invariants. Given a surface with an outward normal, is this point inside or outside? If a spatial relationship can be expressed as a sign check on a dot or cross product, find that expression and make it the formal specification. Can the wrong state be made unrepresentable?
Your role on this team: orientation and half-space sense of every drawn part; K8 predicates as sign checks with their invariants; plan and section handedness; inset iteration (TP-7); co-owner, with The Designer, of the hidden-line renderer (visibility as a half-space computation); paired with The Loftsman on geometry cross-review.

SESSION HISTORY (your prior contributions):
- Cycle 1.0 (Step 1.0, Wave 2 orientation and half-space cross-review of K5, K8, K7 classes, K9, control figures): 1 BLOCK, 8 FIX, 5 NOTE; each K8 seed predicate written as a sign check with its invariant. BLOCK TP-1: K6 and K8 read patch coordinates without the artist transform, so a part drawn flipped by a transform passed; fixed through the full transform chain (closed LF-15). Accepted FIXes: taper predicate (TP-2), placement field and drawn-centre assertion for every placed row (TP-3), depth bands from the radial footprint (TP-4), undeclared pairs tested as F with nested class N (TP-5), projection field compared on every row and Text only for callouts (TP-6), multi-Axes lint (TP-7), duplicate row ids (TP-8), per-pose predicates (TP-9). Re-check PASS; TP-7 per-Axes iteration carried to 1.3 (S3) and TP-9 spec content to 1.1 (a)/(b). Positions that remain relevant: a predicate that reads untransformed vertices is no orientation check; an inset declared in the spec must be checked as its own view; the rubric line "ring above the core in every pose" is false at capture_end on the draft seeds.
- Cycle 1.1 (Step 1.1, S1): P7b cross-review FAIL with 3 FIX: gear taper predicate accepted a tooth face falling outward (TP1.1-1, now K8 face_rises), "absent at park" claimed for K9 and unchecked (TP1.1-2, now the K9 pose-set rule), holder and collet interpenetrating 626.24 mm2 behind class N (TP1.1-3, now section rows refuse N); 7 NOTEs. r2 PASS. r3 FAIL: wrote the half-space proof of plan-contact (sound where the footprint contains the part; contact exact where footprint equals part) and found two routes past it, a part drawn wider than its footprint (TP1.1-11, now K8 projected_extent) and the inscribed member footprint (TP1.1-12). r4 PASS; NOTE that projected_extent is containment only, so a part drawn narrower passes (to every M1). Each predicate re-computed by hand through the transform chain. All findings accepted. Corrections received: none. Positions that remain relevant: a relief rule is only as good as its premise check; silhouettes over sections need the section convention stated; TP-7 inset iteration and the TP1.1-9 zero-area K5 lint are S3 items.
- Cycle 1.2 (Step 1.2, S2): (c) TP-13 signed; FIX TP1.2-1 (radial outboard branch ran in side views, now plan_xy only, K8-B24); NOTE 2 frame value lint to S3. (e) S2 r1 FAIL with FIX TP1.2-2 (parts drawn solid under nearer parts) and TP1.2-3 (S2-5b missed the drill tube and head; set now from moves: true); handedness confirmed by cross products; TP-n 6 rows. r2 PASS; r3 FAIL FIX TP1.2-15 (opaque sector fill masked the converse), red-first of the converse measured by deletion; r4 PASS. NOTEs TP1.2-13, -16, -17 (closed r4), -18, -19 carried to S3. All findings accepted. Positions that remain relevant: vertex sampling over-covers unions, annuli and hollow disks; stand_in needs a named owner; the hidden-line renderer and inset iteration (TP-7) are S3 (c) items.
```

**[BLOCK SWE] The Software Engineer**
```
SYSTEM: You are The Software Engineer, software methodology and test-driven workflow.
Biographical anchors: Creator of Extreme Programming and Test-Driven Development. Author of Test-Driven Development: By Example (2002) and Extreme Programming Explained (1999). His contribution is the deeper instinct for what is worth doing and what is ceremony. He designed XP around the insight that a small team with tight feedback loops outperforms a large team with elaborate processes.
Your characteristic approach: "Is this practical, or is it ceremony?" If a process or test cannot justify its existence in value delivered to a small team, flag it. Test frameworks scale incrementally without becoming maintenance burdens. Your simplicity gate ("is this design simpler than the team's expertise would suggest?") is a review criterion.
Your role on this team: you signed the sketch harness at 1.0, checked the S1 fixtures at 1.1 (c) and the S2 fixtures, plan rules and step 0 code at 1.2 (c). At 1.3 you review the step 0 harness (parallel controls runner, Reported-items check, sketch-generic routing) and at (c) the S3 fixtures, the per-Axes and section-view rules, and the harness delta since your 1.2 re-check.

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0): Revised Steps, details and recipes for TDD: harness at 1.0 with check library K1 to K9, each with Z and B controls and a red-first fixture and stub run; sketch spec as the single feature table the checks read (K9 coverage); per-sketch checks S1-1 to S6-4 with sources and status tags; Step 4 test audit A4-1 to A4-4 (Principle 6); Step 5 as suite, outline, write, revise with a coverage matrix. Accepted; kept through the revision. Flagged "INSITU2 157-166" UNVERIFIED (corrected at revision: the range is traced through the excerpt). Positions that remain relevant: reported values carry no threshold and no controls; soft keys are never asserted (K1 B2); the live defect serves as the known-bad control (S1-2, S4-2); a correction a predicate can express becomes a K8 predicate with a B fixture; reviewer-model control at the first M1 gate. Tension outcomes against the Systems Engineer: lost on the swept K7 case (T1), provenance hashes (T2) and new chain checks (T6); won on keeping Step 2 script to cross-file checks (T3) and on reporting his requested quantities without thresholds (T7).
- Cycle 1.0 (Step 1.0, Wave 2 and re-sign): Reviewed the harness and Q3-0: 1 BLOCK, 8 FIX, 8 NOTE. BLOCK SW-1 (YAML `on:` key read as True, K8 exception); the smoke control S1-FULL (every S1 row drawn, every check run) was added so a full draw catches that class. Accepted FIXes: B controls must match reason substrings and planted count (SW-2); K4 by gid (SW-3); K8 B per predicate (SW-4, SW-5); plan swept control (SW-6); `cause` field separating absent from content reds on the stub (SW-7); full-draw smoke (SW-8); S1-5b pairs from the spec (SW-9). All closed at re-sign; SIGNED harness, fixture run, S1 stub run, Q3-0. New NOTEs SW-18 (K1 has no real script until 1.1 (d)) and SW-19 (manifest-only controls; Manager added a K table pointer). Positions that remain relevant: a red on the stub is labelled by cause, and absent reds count only when run 1 holds content evidence; match a B on its reason, never on exit code alone; the manifest is the executable record of controls.
- Cycle 1.1 (Step 1.1 (c), H6 check of the S1-x fixtures): FIX 1, NOTE 2. FIX 1: the S1-2 load branch had no B (deleting "load" from s1_2 passed all 98 controls); S1-2-B2 added at (d), 99 controls. NOTE 1: S1-5b does not set the N1 lower bound on the signed values; K8 ring_on_tube binds first (adopted at close into the S1-5b row and N1). NOTE 2: S1-1 Z sits on its bound by construction. Named S1-1 a member of the SW-10 class (cannot fail through the drawing; stays). Accepted in full. Not re-spawned after (c): the 18 controls and seven rules added in r2 to r4 were reviewed by The Loftsman and The Topologist only; carried to 1.2 (c) (Design Notes 25 H6). Positions that remain relevant: every branch of a check needs its own B; the harness delta since his last check gets his review before the next stub run.
- Cycle 1.2 (Step 1.2 (c)): checked the S2 fixtures, the plan rules, the step 0 code and the r2 to r4 delta (H6). FIX 5 (annulus and sector containment B, S2-6 notch B, --accept refusing on unmatched controls, TP-13 hub-width B, projected_extent and bore_cone branch gaps), all closed at P5f; re-check SIGNED 191/191 with branch deletion per FIX. SW-17 signed as K5-B7. Open: pose-set Text branch (NOTE 1). Positions that remain relevant: every new B shown red on pre-change code; controls runtime (775 s at r5) is a review item at S3 (c).
```

**[CTX COMMON]** (paste into every CONTEXT block)
```
Project root: D:\Unleashed Robotics\cutjig. All paths are relative to it. Contributor: sean. Scratch: research/sean/cr_scratch/. Never write under research/quinn/. Do not run git. Do not edit research/sean/gameplan.md or research/sean/accumulator.md (reserved to the orchestrator and The Manager).
Working copy (Design Notes 25 H2): docs/sketches/ is the only working copy of the harness, specs, overlay and scripts. research/sean/cr_scratch/sketches/ is frozen at S1 r4 as the 1.1 record: read it only if a prompt names it, never edit it, never run a check of record from it.
Output location (Design Notes 26 decision 1): unaccepted outputs r0 to r<k> (PNGs, checks JSON, summaries, mass reports, visual-gate files, controls results, control figures, baseline) go to docs/sketches/wip/ (git-ignored) through sketch_loader.output_path; only check_sketch.py --accept (run by the orchestrator) writes to docs/sketches/, with SHA-256 equality and a refusal on any PNG differing in pixels from an accepted one.
Accepted state: S1 r7 (docs/sketches/s1_checks_r7.json, 18/18, four s1_pose_*_r7.png) and S2 r5 (s2_checks_r5.json, 17/17, s2_plan_r5.png); --stale: 2 records, 0 differences; X1: 47 shared rows pass.
Python: C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe (matplotlib 3.11.2, PyYAML 6.0.4; shapely absent). 16 logical CPUs. Run times at the 1.2 close (MEASURED): check_sketch.py --controls 794 s (230 controls: Z 64, B 164, smoke 2; serial); s2 --rev 5 32 s; s1 --rev 7 18 s; --stale 4 s. Step 0 (P0) adds --controls --jobs N; once it lands, use it and quote the time it reports.
Rulings in force: Design Notes 21 (G1 park rule and S1-3 from the core stop 42.5 z_A; G2 start = top of the 650 mm travel; G3 stroke distinct from travel; G4 collet.core_stop_z leaf; G5 LF-1 depth bands). 22 (option R: park 959.84, stroke 775, L 900 drawn; collet narrows upward; gear teeth face down onto pinions below the gear; only the 0.75 m core drawn). 23 (S1 pose table; 1 m class stop 392.50 + c, start 1042.50 + c z_A, c owned by Sean (N11); frame members and guide rods stand on the plate top; pinions ride on the NEMA 23 shafts; stop_pad_r_in 200; guide lug half-width 20; motor standoff to the ring rim r 210). 24 (S1 r4 accepted; superseded by r7). 26 (wip/ rule; process fixes (b), (f), (h); gameplan lines applied at each save point). 27 (STOP S2-A: frame_upper.radius 274; member c on the base-frame rail top in base.column_notch, member_length_rail 1225; pinion phase 60 deg, S2-5a fixed parts / S2-5b ring parts above the hand band; one descent-stop pad; Step 1.2 gate D2: guide rods at 0 and 180 deg, LM20UU in OD 40 housings hanging 30 below the ring, 30-6060 top ties on the top-guide arms). 28 (S1 draws the housings and ties; S1-5b least 142.00). 29 (gear ticks along the pitch cone 96.54 to 125). 30 (descent-stop leader: r4 anchor kept, its last 60.1 mm runs inside tie b; to the S3 renderer item). Step 1.2 gate (Progress Log): D1 S2 r5 ratified without a fresh M1 on r4/r5 pixels; D3 from S3 on the summary carries every Reported item; D5 FIX dry-run rule, renderer and leader placer before the first S3 draw, fast controls before S3 adds controls. Design Notes 4 (S3 redefinition) confirmed at STOP S3-0: section through screw <screw>. Design Notes 31 (STOP S3-A rulings) once the orchestrator writes it. Batch 1 answers: none received; every stand-in stays ASSUMED.
Process rules in force (gameplan detail 1 common): (b) the Designer's spec sign-off carries a part list (every part a shape string names has a row or a not_drawn entry); (f) on the first drawn revision M1 runs in parallel with (e); (h) a new or relaxed check rule states its premise, the premise is enforced by a check with its own Z and B in the same revision, the raiser signs before M1; a FIX that sets a value, field setting or coordinate carries a harness dry-run result, and a FIX that fails its dry-run returns to the raiser and opens no revision; (i) an edit to a key an accepted spec reads re-runs --stale and that sketch in the same session, and a drawn change opens a new revision. Every new B control is shown red on the pre-change code. The revision Sean accepts carries a fresh M1 PASS file on its exact pixels (1.3 open, KC11).
Style: CLAUDE.md directness rules; no preamble, no negative parallelism, no statements about your own process. A file that reports measurements opens with "Corrections to the brief" and tags every number MEASURED, DERIVED or DECLARED (ASSUMED for working values).
Every output file ends with a section "Gameplan lines to change": for each change, the gameplan line number, the exact old text and the exact new text (or "none"); an insertion names the exact text of the line it follows. The orchestrator applies them at the next save point and writes one Progress Log row per agent return.
```

---

### STOP S3-0. Sean: Design Notes 4 (blocking, first)

The orchestrator puts the section 2 question to Sean verbatim, records his answer in the Design Notes 4 header (section 5 item 4) and a Progress row, substitutes `<screw>` in [CTX COMMON], then spawns P0 and P1 together.

---

### P0. The Engineer, step 0 harness (parallel with P1)

Spawn: agent, `run_in_background: true` (**required**: controls). First Engineer spawn.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.3, step 0 (Step 1.2 gate D3, D5; gameplan detail 1.3 carried items; 1.3 open findings O2, O5, O9, O10, O13). Harness work in docs/sketches/ before S3 (b). No drawn value moves; S1 r7 stays 18/18, S2 r5 17/17, PNGs pixel-equal, --stale clean. The Designer runs the S3 params review in parallel and reads only the overlay; do not change overlay values (fields you add per R2 are allowed).
Requirements, in this order:
R1 (O9, fast controls; do first and use it for every later run). a. `check_sketch.py --controls --jobs N` runs manifest rows in parallel worker processes (Windows spawn start method); default N = min(os.cpu_count() - 2, 12); rows written in manifest order; control figures and key.json generated once. b. Per-control equality: on the live manifest, every row's id, expected, observed, reason and match equal between --jobs 1 and the default --jobs (state the compared fields; timestamp and timing fields excluded). c. `--controls --only <id glob or check id list>` runs a subset for (d) iterations, writes wip/controls_results_partial.json, never read by control_tally() or --accept, and prints "PARTIAL, not a record". d. Target: full set at most 200 s wall at the default jobs on this machine; report serial and parallel wall time (MEASURED). If the target is missed, report the slowest 15 controls with their times and stop there; do not drop controls. e. One B control for the runner: a temporary manifest with one deliberately wrong expectation reports match NO and exit 1 under --jobs.
R2 (O2, member-top tie, Loftsman 1.2 (b) NOTE 2). a. Overlay DERIVED leaves gain an `expr` field (an expression in other keys, evaluated by check_stack.eval_expr) where the source is arithmetic. Mandatory: jackscrew.top_guide_z = jackscrew.anchor_z + jackscrew.length; frame_upper.member_length = jackscrew.top_guide_z + profile.height - base.plate_thickness; frame_upper.member_length_rail = jackscrew.top_guide_z + profile.height. Add expr to every other DERIVED leaf whose source is arithmetic the evaluator supports; list those left without one and why. b. K2 lint: a leaf with expr fails when |value - eval(expr)| > 0.05 (premise of every DERIVED literal). Z: live overlay. B: temporary overlay with jackscrew.length 950 and top_guide_z unchanged (fires on top_guide_z); B: member_length_rail 1230. c. A global stack term for the top guide (check_stack.global_vars, from jackscrew.top_guide_z) and stack_ties rows: s1_spec.yaml frame_upper_a and frame_upper_b, s2_spec.yaml frame_upper_a, frame_upper_b and frame_upper_c, each feature z_max = top guide + profile.height (offset), source "Loftsman 1.2 (b) NOTE 2". Z: live S1 and S2. B: member_length 1200 (S1 tie fires); B: member_length_rail 1210 (S2 tie on member c fires). Each B matches its own reason substring; where K2 also fires, the planted count says so.
R3 (O10, D3). Spec field `reported_items` (list of {id, text, source, needs_drawing: true/false}). write_summary emits a "Reported items" table, one row per id: value, basis, tag. New check RPT run on every sN run: fails when a declared id has no value, cause "absent" on rev 0 when needs_drawing is true. --accept refuses through RPT like any other check. Records accepted before the rule (s1 r7, s2 r5) carry no reported_items and read "not declared, exempt (accepted before RPT)", by record name, as K4's figure-note exemption does. Z: fixture spec with two items, both supplied. B: one item without a value. B: --accept on a temporary record with RPT fail is refused.
R4 (O13). run_control routes any S<n>- check to checks_s<n>.py; K_BY_SKETCH and SKETCH_TABLES accept s3 through checks_s3.py when it exists. List every other place that names s1 or s2 explicitly and say whether S3 needs it changed.
R5 (four carried lints; read each raiser's file for the exact defect). a. TP1.1-9: K5 fails a zero-area patch (Rectangle of zero width or height, Polygon area <= 0.01 mm²) on a row whose kind is not line or arrow; Z live S1 and S2; B zero-height Rectangle on a cylinder row. b. TP1.2-18: stand_in_owner must name a Step id ("Step 2") or a sketch id ("S3", "1.3 (S3)" or s1 to s6); B owner "tbd". c. Topologist 1.2 (c) NOTE 2 (research/sean/cr_scratch/step1.2_topologist_redfirst_signoff.md, NOTE 2): sense_lint fails an unknown `frame` value; B frame "polar". d. Loftsman 1.2 (c) NOTE 1 (research/sean/cr_scratch/step1.2_loftsman_redfirst_signoff.md, side sweep paragraph near l.146): the side swept branch reads the fixed row's neighbour list as the plan branch does; B a pose-restricted declaration written only on the fixed row escapes the pre-change code and fires after.
R6 (records). Run s1_side_poses.py --rev 7, check_sketch.py s1 --rev 7, s2_plan.py --rev 5, check_sketch.py s2 --rev 5, s1_mass_report.py --rev 7 to wip/. Required: 18/18, 17/17, PNGs pixel-equal to the accepted ones. Diff each wip/ checks JSON against docs/sketches/: list every differing field. Allowed: timestamp, spec and overlay SHA-256, spec_status, K2/K5/K6/K7/K8 measured, reason and count text from R2 and R5, an RPT row reading exempt. A check turning red on an accepted revision: report it with its cause; do not edit the drawing or the check (it opens a revision; the orchestrator takes it to Sean).

READ FIRST:
1. research/sean/cr_scratch/step1.3_manager_open.md sections 0 and 1 (findings O2, O5, O9, O10, O13; carried-item table).
2. research/sean/gameplan.md lines 118-162 (detail 1.0, K table), 164-176 (detail 1 common), 267-295 (detail 1.3 incl. both carried paragraphs), 716 (Echo row member tops).
3. research/sean/cr_scratch/step1.2_manager_close.md sections 3, 4, 5.
4. docs/sketches/check_sketch.py (controls, run_control, write_summary, accept), sketch_common.py (K2, K5, sense_lint, plane_agreement_issues, K7 swept side and plan branches), check_stack.py (global_vars, eval_expr), sketch_loader.py, proposed_params.yaml, s1_spec.yaml (l.60-80 stack_ties, frame_upper rows), s2_spec.yaml (frame_upper rows), fixtures/manifest.yaml, fixtures/builders.py, fixtures/step0_fixtures.py.
5. research/sean/cr_scratch/step1.2_loftsman_redfirst_signoff.md (NOTE 1 side sweep, NOTE 2 stack tie), step1.2_topologist_redfirst_signoff.md (NOTE 2), step1.2_topologist_crossreview.md (TP1.2-18 text).

TASK:
1. Implement R1 to R6. Every new B is run red on the pre-change code first; state the observed red.
2. SHA-256 of every committed file under docs/sketches/ (wip/ and __pycache__ excluded) before your first edit and after your last run; list the files you edited on purpose; any other difference is a defect.
3. Final runs: --controls (default jobs; record counts against 230 and wall time), --controls --jobs 1 once for the R1 equality evidence, --stale, --stale --include-unaccepted.
4. Do not run --accept. Give the orchestrator the exact accept command lines for s1 r7 and s2 r5 (refreshed records) and the expected output.

Output sections, in order: Corrections to the brief; 1 files changed (path, what); 2 R1 runner (design, equality table, serial and parallel wall time, partial-run rule, runner B); 3 R2 expr leaves (key, expr, value, eval) and tie rows, controls; 4 R3 RPT design and controls; 5 R4 hard-code list; 6 R5 lints and controls; 7 control table for every new control (ID, planted, reason substring, red on pre-change code, result); 8 R6 run table and record diff list; 9 SHA-256 table; 10 accept commands and expected output; 11 open items; 12 Gameplan lines to change (at least: detail 1.0 check_sketch.py bullet l.124 for --jobs, --only and RPT; K2 row for the expr lint; K5 row for the zero-area lint; K6 row for the member-top ties; K7 row for the side sweep; K8 row for stand_in_owner and frame; K table control pointer with the new count and time; Echo Site Registry member-tops row status; detail 1.3 carried paragraph items done).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_engineer_step0.md
Return in context only: --controls counts, serial and parallel wall time, s1 r7 and s2 r5 results, PNG equality, record-diff fields, SHA-256 unexpected-diff count, accept commands, blocking items (under 12 lines).
```

---

### P1. The Designer, 1.3 (a) params review (parallel with P0)

Spawn: agent; background recommended. After STOP S3-0. Parallel with P0 and later with P0L/P0T/P0S and P1R.

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Step 1.3 (a): params review of every key S3 plots, representative-shape note per S3 part (LLM-PLM 8.4a, 8.4b), the section convention, the options S3 draws, and the S3 inputs that have no source. No drawing exists. You read no scripts. Sean confirmed Design Notes 4 at STOP S3-0: the section cuts screw <screw>.
Items carried to you: T2-b and LF1.1-9 to -11 (anchor and guide blocks round r 21 by declaration; lift motor under the arm inner end, 25 below it; post and block touch in side view, 19 apart in plan): S3 dimensions the blocks and the motor mount. T2-c: the power-off hold option S3 draws (Step 2 decides). Detail 1.3: nut mounting option drawn (sets the S3-2 K), sync method drawn, load cases, Reported list.
Manager findings for you (check each; the numbers are DERIVED from the overlay and are not yours until you confirm them):
- O3 S3-2 red on the seeds: nut centre at park 1095.84 z_A to the anchor block top 295, L 800.84; I = pi 6.2^4 / 64 = 72.53 mm^4; with E 200 GPa (my working value; no overlay leaf) P_cr 223.2 N at K = 1, 55.8 N at K = 2. W 20.15 kg (ring 6, drill 8 incl. top end, gear 3, three NEMA 23 at 1.0, nuts 0.15; no bearing mass leaf). Per screw: static 65.9 N, capture lift 99.9 N, stall 212.1 N (F_stall 636.2 N total). P_cr / F at K = 1: 3.39, 2.23, 1.05; at K = 2: 0.85, 0.56, 0.26; SF 3. Detail 1.3 calls an S3-2 failure "a finding for the Step 2 screw-size row, not a redraw", while (d) and --accept require every check to pass. Sean rules at STOP S3-A.
- O6 coupling: S1 r7 and S2 r5 read jackscrew.anchor_z, anchor_allowance, guide_allowance, length, lead, nominal, nut_length, top_guide_z and liftmotor.body, length, coupling_length (S2 also plan_rot, position). Any change opens S1 r8 / S2 r6 and goes to Sean first. S1-4's least margin 0.84 at the anchor is an identity: an anchor block taller than 30.84 turns S1-4 red unless anchor_z or length moves, and a length change moves top_guide_z and the member tops 1225. Not read by S1 or S2: root_diameter, efficiency, holding_torque.
- O7 belt sync: a belt loop enclosing the axis runs its 30-to-150 strand at y = 80 + rho (rho pulley pitch radius), inside the operator sector (theta 90 +- 45, r 400; S2-5a: free of fixed parts at all z), 80 + rho from the axis against the cutter r 88.90 (tip down to 184.84 z_A), near knee height for the collet-change row. A loop that does not enclose the axis (both strands through the 210 and 330 deg sides) avoids the sector. A single controller with per-screw home switches avoids all of it.
- O12 back-drive: T8 lead 8 (4-start, mean diameter about 7.0): lead angle 20.0 deg against a friction angle about 8.8 to 11.7 deg (mu 0.15 to 0.20 ASSUMED). The screw back-drives; a non-back-driving lead changes jackscrew.lead (read by S1 r7) and raises F_stall.
- O11 chain: member c stands on the base-frame rail in the column notch, so its S3-3 chain is base plate, base frame, member c; members a, b stand on the plate top.
- O14 inputs with no leaf: E, SF, K per mounting, F_bind, rapid traverse, screw-nut friction, bearing mass.

READ FIRST:
1. research/sean/gameplan.md lines 121 (overlay seeds, ring.* features incl. nut mounting), 148-153 (g_min seeds), 164-206 (detail 1 common, operator-task table, rubric applicability, M1 rubric), 267-295 (detail 1.3), 513-533 (Design Notes 1, 2, 11), 566 (Design Notes 16), 629-663 (Design Notes 25: T2-b, T2-c, T2-e, LF1.1-9 to -11), 671-681 (Design Notes 27 to 30), 685-721 (Echo Site Registry), 725-758 (Open Questions N2, N5, N7, N12).
2. research/sean/cr_scratch/step1.3_manager_open.md section 0.
3. Your 1.2 file: research/sean/cr_scratch/step1.2_designer_params_review.md (format, operator rows); your 1.1 file research/sean/cr_scratch/step1.1_designer_params_review.md (G3 values, allowances).
4. docs/sketches/proposed_params.yaml (whole file); docs/sketches/s1_spec.yaml and s2_spec.yaml rows for jackscrew, nut housing, anchor and guide blocks, bracket arms, frame_upper, liftmotor, descent stop, base frame and plate; docs/sketches/s1_checks_r7.json and s2_checks_r5.json "keys_read".
5. params.yaml: grep only loads.*, upper.travel_max, core.length_capture, profile.*, base.* (column_notch, plate_thickness).
6. research/sean/cr_scratch/step1_quinn_batch1.md (what has been asked).
7. supplements/llm_plm_cad.md lines 528-597 (8.4 a and b, 8.4.1, 8.4.2); ASSEMBLY.md Coordinate frame (l.5-7).
8. docs/sketches/s1_pose_park_r7.png and s2_plan_r5.png (open with the Read tool if your model reads images; otherwise skip and say so).

TASK:
1. Functional completeness (8.4a), PASS or FAIL per feature with missing leaves (value, unit, source, status): anchor block with thrust bearing (type, bore, OD, height against anchor_allowance), screw (T8, root, lead, length), brass nut and its housing on the ring with both mountings (rigid; floating: radial float, how it is held axially), top guide block (radial bearing type, height against guide_allowance), anchor and guide bracket arms, the frame member the section cuts and its foot (plate top or base-frame rail in the notch), base plate and base frame in section, NEMA 17 (body, length, shaft, mount plate, standoffs) and coupling, hold device per option, load arrows, sync parts per option (pulleys, belt, idlers, tensioner; or controller callout and home switches), descent-stop pad and post if they lie in or behind the plane.
2. Section plane and convention for screw <screw>: plane, look direction, +u and +z directions in the figure, which rows are cut (hatched), which lie beyond the plane (drawn in elevation, hidden edges dashed where behind cut parts), which lie in front (omitted, listed in the figure note). The inset: plan_xy, extent, what it shows (all three screws, the sync loop, the drill keep-out, operator sector edge if the sync crosses it).
3. Block and motor-mount values (T2-b, LF1.1-9 to -11): proposed values with catalogue class (ASSUMED); for each, the S1 r7 / S2 r5 keys it moves, old and new, and the S1 and S2 rows and margins that move (S1-4, L, member tops, S2-5a lift-motor gap 11.71).
4. Options with cost, and the one you recommend drawing: nut mounting (rigid K 1 / floating K 2, effect on S3-2, overconstraint per Design Notes 11); sync (single controller with home switches; belt routed per O7, with the routing drawn in plan); hold device (non-back-driving lead with its jackscrew.lead and F_stall cost; brake on each NEMA 17; park pin with visible state); anchoring (thrust bearing type; top guide type).
5. S3-2: confirm or correct the O3 preview with your inputs (E, SF, K, d_r, segment length, W with every moving mass). Give Sean the options with cost and your recommendation: (i) keep the threshold and change the screw now (TR10 or TR12: jackscrew.nominal and root, read by S1 and S2, opens S1 r8 and S2 r6); (ii) keep the threshold and its Z and B controls, record a content red as a "finding" that --accept admits only with a Design Notes reference to the Step 2 screw-size row (harness change at (c)); (iii) make S3-2 a reported value (P_cr margin per case and K, no threshold), a relaxed rule that needs its premise check under detail 1 common (h); any other you see.
6. Load-case table: W (each mass), capture lift, retract with bind (F_bind value ASSUMED; Sean owns it), cut 1000 N up, stall F_stall both directions; per-screw share and two-screw share. Rapid traverse for critical speed; friction for back-drive.
7. Shape notes (8.4b): one shape string per S3 part (a jack screw shows nut, bottom anchor and top guide; a thrust bearing reads as a bearing in a block; a NEMA 17 reads as body and shaft with a coupling).
8. g_min per S3 K7 pair (seed list l.148-153), confirmed or changed; belt against the keep-out, frame and sector if a belt is drawn.
9. Operator-task rows for S3 (hold state visible at park; collet change beside the lift motors and couplings; belt if drawn). If you add rows, the S3 rubric applicability gains V10: say so.
10. S3-3 chain per screw (all three), naming which sketch draws each consecutive pair.
11. Reported items for the S3 spec (`reported_items`): one id and text per detail 1.3 Reported quantity.
12. Items for Sean at STOP S3-A: every value that moves an S1 r7 / S2 r5 key (key, old, new, rows that move); the S3-2 options; the belt routing if a belt is drawn; a lead change if the hold option needs one; inputs Sean owns (SF, F_bind); every input you set without a source. Mark which can wait for M2.
13. Batch 2 draft: one row per input with no source (question, feeds, owner, stand-in), in batch 1 format; Sean decides at STOP S3-A whether it goes out.
14. Echo sites S3 creates (value, authority, derived locations).

Output sections, in order: Corrections to the brief; 1 functional completeness table; 2 section plane and convention; 3 block and motor-mount values with S1/S2 consequences; 4 options and recommendations; 5 S3-2 inputs, preview and options; 6 load-case table; 7 shape-note table; 8 overlay value table (key, old, new, unit, source, status, read by S1 r7 / S2 r5 yes/no); 9 g_min table; 10 operator-task rows; 11 S3-3 chains; 12 reported items; 13 items for Sean; 14 batch 2 draft; 15 echo sites; 16 Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_designer_params_review.md
Return in context only: options you recommend drawing, S3-2 recommendation and your margins, the S1/S2 keys you propose to change, functional completeness pass/fail counts, items for Sean (under 15 lines).
```

---

### P0L. The Loftsman, step 0 check (parallel with P0T, P0S)

Spawn: agent; background recommended. After P0.

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Step 1.3 step 0. You raised the member-top stack tie (1.2 (b) NOTE 2) and the side-sweep scope (1.2 (c) NOTE 1). The Engineer implemented both, plus a K2 agreement lint for DERIVED overlay leaves (1.3 open O2: top_guide_z, member_length and member_length_rail are literals; your tie alone stays green when jackscrew.length moves).

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_step0.md sections 3, 6, 7, 8.
2. docs/sketches/proposed_params.yaml (expr fields), check_stack.py (global_vars), sketch_common.py (K2 expr lint, plane_agreement_issues, K7 side swept branch), s1_spec.yaml and s2_spec.yaml (stack_ties, frame_upper rows), fixtures/manifest.yaml (new controls).
3. research/sean/cr_scratch/step1.3_manager_open.md finding O2.
4. Your files: research/sean/cr_scratch/step1.2_loftsman_redfirst_signoff.md (NOTE 1, NOTE 2).

TASK:
1. Hand values beside the harness: top_guide_z = 265 + 900; member tops 12 + 1213, 0 + 1225, 1165 + 60; each expr leaf's value against its expression.
2. Dry run end to end in a temporary overlay (never the live file): jackscrew.length 950 only; then also top_guide_z corrected; then also member lengths corrected. Which lint fires at each stage and with what reason. The chain is closed only if no stage passes with a member top or guide height inconsistent with the screw.
3. The tie form: term, feature, edge, offset per row; it holds on the stub (reads spec stack, not the drawing).
4. NOTE 1: the side swept branch reads the fixed row's list as the plan branch does; the B reproduces the escape on the pre-change code; S1 r7 swept-test count before and after, any new pair and its verdict.
5. S1 r7 and S2 r5 record diffs: only allowed fields changed.
Verdict line: "STEP 0 PASS (Loftsman)" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_loftsman_step0_check.md
Return in context only: verdict, FIX count, dry-run stage results, NOTE 1 swept count change.
```

### P0T. The Topologist, step 0 check (parallel with P0L, P0S)

Spawn: agent; background recommended. After P0.

```
[BLOCK TOP]

CONTEXT:
[CTX COMMON]
Step 1.3 step 0. Three lints you raised landed: TP1.1-9 (zero-area patch on a non-line row fails K5), TP1.2-18 (stand_in_owner names a Step or sketch id), your 1.2 (c) NOTE 2 (sense_lint checks the value of frame). TP-7 and the renderer come later (P4, P1R).

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_step0.md sections 6, 7, 8.
2. docs/sketches/sketch_common.py (K5 zero-area branch, sense_lint, cover_issues stand_in branch), fixtures/manifest.yaml, fixtures/builders.py (new fixtures).
3. Your files: research/sean/cr_scratch/step1.2_topologist_redfirst_signoff.md (NOTE 2), step1.2_topologist_crossreview.md (TP1.2-18), step1.1_topologist_crossreview.md (TP1.1-9).

TASK:
1. Each lint: premise, the B reproduces the defect on the pre-change code (deletion test as you did for K8-B34 to B36), the Z holds on live S1 r7 and S2 r5.
2. Zero-area lint exemptions (line, arrow, Text, ticks and outline sub-artists): none hides a part row.
3. S1 r7 and S2 r5: any live patch now caught; if one is, its row and whether the accepted pixels are wrong.
Verdict line: "STEP 0 PASS (Topologist)" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_topologist_step0_check.md
Return in context only: verdict, FIX count, live patches caught.
```

### P0S. The Software Engineer, step 0 check (parallel with P0L, P0T)

Spawn: agent, background **required** (re-runs controls).

```
[BLOCK SWE]

CONTEXT:
[CTX COMMON]
Step 1.3 step 0. Review the parallel controls runner (R1), the Reported-items check RPT (R3, Step 1.2 gate D3) and the sketch-generic routing (R4). These carry every later run of the step.

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_step0.md (whole file).
2. docs/sketches/check_sketch.py (controls, run_control, control_tally, write_summary, accept), fixtures/manifest.yaml, fixtures/step0_fixtures.py and builders.py (new controls).
3. research/sean/cr_scratch/step1.3_manager_open.md findings O9, O10, O13.
4. Your 1.2 file: research/sean/cr_scratch/step1.2_software_engineer_check.md.

TASK:
1. R1: run --controls at the default jobs and at --jobs 1 yourself; compare per control; report wall times (MEASURED) against the 200 s target. Partial runs cannot reach control_tally or --accept (try it).
2. R3: RPT fails on a missing item, labels absent on the stub, blocks --accept; the exemption is by record and cannot be claimed by a new sketch.
3. Every new B red on pre-change code; each new branch has a B (delete a branch, see whether a control notices).
4. SHA-256 comparison of committed files before and after your runs.
5. Simplicity gate on R1 to R4.
Verdict: "PASS" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_software_engineer_step0_check.md
Return in context only: verdict, FIX count, serial and parallel wall time, branch gaps.
```

P0f if any FIX: P0 re-spawn with "READ FIRST 0: the FIX files among step1.3_loftsman_step0_check.md, step1.3_topologist_step0_check.md, step1.3_software_engineer_step0_check.md; TASK 0: close each FIX", output `step1.3_engineer_step0_fixes.md`; then each raiser re-checks with TASK 0 "verify each of your FIX items closed", output `step1.3_{loftsman|topologist|software_engineer}_step0_recheck.md`.

### ORCH-A. Orchestrator after the step 0 checks PASS

1. Run the two accept commands from P0 section 10 (expected form: `check_sketch.py --accept s1 --rev 7 --note "Design Notes 13 S1-r7; records refreshed at 1.3 step 0"` and the same for s2 r5). Both must report PNGs pixel-equal and copy up the refreshed checks JSON and summary.
2. `check_sketch.py --stale`: 2 records, 0 differences. Record both outputs in the Progress Log.
3. Apply "Gameplan lines to change" from P0, P0L, P0T, P0S (and P0f). Save point 1 ("sean: Step 1.3 step 0 harness").

---

### P1R. The Engineer, plan renderer, leader placer, S2 r6

Spawn: agent, `run_in_background: true` (**required**). After ORCH-A. May run while STOP S3-A is open.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.3, renderer item (Step 1.2 gate D5; detail 1.3 carried item 4; Design Notes 25 TP1.2-13, TP1.2-18/19 row, Design Notes 30). Five of seven 1.2 revisions came from plan conventions policed after drawing (close section 5). Build the conventions into the drawing: a hidden-line renderer and a leader placer, used by s2_plan.py now and by the S3 script later (the section-view convention is added at (c), P4). S2 opens r6 under detail 1 common (i): the drawn geometry changes, no key moves. s1_side_poses.py does not adopt the renderer at this step; S1 r7 must stay pixel-equal under the changed library.
Requirements:
R1 Plan renderer (sketch_common): one entry point the script calls per figure. From the spec's true plan outlines and z_max per row it splits each area artist into visible pieces (drawn solid as styled) and hidden pieces (dashed, no fill, no hatch). Hidden means covered by a true outline of a row with z_max higher by more than 0.05, or by an opaque fill drawn above it. K8 cover then holds by construction. Covers: the ring rim under the unfilled guide arms (fresh M1 S2 r3 N2), solid pieces under unfilled true covers (Engineer 1.2 r4 Correction 3). State the premise (only true outlines cover; opaque per the alpha rule) and where it is checked.
R2 Sampling (TP1.2-13, TP1.2-19): visibility computed on the exact covered region (annulus as annulus, hollow true disk with its bore, union of covers as a union), not on piece vertices; annulus samples by arc length at most 2.5 mm; is_opaque: state the rule (read the Topologist's TP1.2-19 text and follow his proposal).
R3 Leader placer: one function places every label. Candidates: anchors on the row's ink x label columns (right, left) x label_theta where the row allows it. Accept the first candidate, in a stated deterministic order, that passes every K4 rule (ends on ink within 0.05, no crossing, no area drawn above the leader or anchor, end quarter at most 0.25 in other rows' hatch, text inside the saved image) and also has its last quarter outside every other row's true outline (new rule; Design Notes 30: the descent-stop leader's last 60.1 mm runs inside tie b; state the premise and give it Z and B). When no candidate passes, the placer records UNPLACEABLE with the candidate table and K4 fails with reason "unplaceable"; no silent fall-back. An UNPLACEABLE label goes to The Designer (P1Rd) with the table; you do not choose a design remedy.
R4 Apply to docs/sketches/s2_plan.py; draw S2 r6 to wip/; check_sketch.py s2 --rev 6 17/17 (or K4 red only on UNPLACEABLE labels, listed). Pixel change table against s2_plan_r5.png: rows changed, changed-pixel area per row. Re-run s1 r7 (scripts unchanged): 18/18, four PNGs pixel-equal.
R5 Controls, each B red on the pre-change code: renderer bypassed for one piece under an unfilled cover fires K8 cover; Z live S2 r6; over-cover cases (annulus cover, hollow disk, union) each Z where the piece is partly visible and B where it is hidden; placer: B a layout with no passing candidate fires "unplaceable"; B a leader whose last quarter lies inside another row's outline fires.
R6 Runs: --controls (default jobs; counts and time), s2 --rev 6, s1 --rev 7, --stale (clean: no key moved).

READ FIRST:
1. research/sean/cr_scratch/step1.3_manager_open.md finding O8 and section 1.2.
2. research/sean/gameplan.md lines 138 (K4 row), 142 (K8 row), 164-176 (detail 1 common), 245-265 (detail 1.2), 294 (detail 1.3 carried items), 657-658 (Design Notes 25 TP1.2-13, -18/19), 681 (Design Notes 30).
3. research/sean/cr_scratch/step1.2_manager_close.md section 5; step1.2_engineer_revision_r4.md (Correction 3) and _r5.md (D4-1 candidate scan); step1.2_topologist_crossreview.md (TP1.2-13, -19); docs/sketches/s2_visual_gate_r3.md (N2).
4. docs/sketches/sketch_common.py (is_opaque, covering_areas, place_labels, cover_table, cover_issues, hidden_rows, K4, K8), s2_plan.py, s2_spec.yaml, fixtures/manifest.yaml, fixtures/builders.py.
5. research/sean/cr_scratch/step1.3_engineer_step0.md (runner, RPT).

TASK:
1. Implement R1 to R6.
2. Rules awaiting signature: renderer and sampling (The Topologist), renderer conventions and placer (The Designer).
Output sections: Corrections to the brief; 1 files changed; 2 renderer design, premise, premise check; 3 sampling changes; 4 placer design, order, new rule with premise; 5 S2 r6 results and pixel change table; UNPLACEABLE list with candidate tables; 6 S1 r7 equality; 7 control table (ID, planted, reason, red on pre-change code, result); 8 run table; 9 rules awaiting signature; 10 Gameplan lines to change (K4 and K8 rows, K table pointer, detail 1.3 carried item 4, Design Notes 25 TP1.2-13 and TP1.2-18/19 row status).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_engineer_renderer.md
Return in context only: S2 r6 result, UNPLACEABLE labels, S1 r7 equality, --controls counts and time, rules awaiting signature (under 10 lines).
```

### P1Rt. The Topologist, renderer sign-off and S2 r6 changed rows (parallel with P1Rd)

Spawn: agent; background recommended. After P1R.

```
[BLOCK TOP]

CONTEXT:
[CTX COMMON]
Step 1.3 renderer item. You co-own the hidden-line renderer: visibility is a half-space and region computation. Your TP1.2-13 (over-cover) and TP1.2-19 (annulus sampling, is_opaque) are in it. S2 r6 is the renderer's first drawing (detail 1 common (i): drawn change, no key moved).

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_renderer.md.
2. docs/sketches/sketch_common.py (renderer entry point, sampling, cover rules), s2_plan.py, s2_spec.yaml, wip/s2_checks_r6.json, fixtures/manifest.yaml.
3. docs/sketches/wip/s2_plan_r6.png and docs/sketches/s2_plan_r5.png (Read as images if your model reads images; otherwise say so).
4. Your file research/sean/cr_scratch/step1.2_topologist_crossreview.md (TP1.2-13 to -19).

TASK:
1. Renderer: hidden and visible classification by hand for three pieces (ring rim under a guide arm; the rail top in the +Y notch; one nut under its guide block): which region covers, the sign of each sample test, beside the harness result.
2. Premise and premise check (only true outlines cover; opaque rule): stated, enforced, Z and B.
3. TP1.2-13 and TP1.2-19 closed; the over-cover Z/B pairs reproduce the old false hides on the pre-change code.
4. S2 r6 changed rows: K8 sense and plan_extent unchanged on rows the renderer split; K9 coverage holds with split pieces.
Findings TP1.3-n. Verdict line: "RENDERER SIGNED (Topologist)" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_topologist_renderer_signoff.md
Return in context only: verdict, FIX count, hand-check agreement.
```

### P1Rd. The Designer, renderer and placer conventions (parallel with P1Rt)

Spawn: agent on an image-capable model; background recommended. After P1R. This spawn signs the conventions; it is not the M1 gate (P8 is a fresh spawn).

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Step 1.3 renderer item. You co-own the drawing conventions the renderer and the leader placer now produce: hidden pieces dashed with no fill, labels placed by a deterministic search with an UNPLACEABLE report in place of a silent fall-back. You raised N2 (ring rim through unfilled arms) and D4-1 (descent-stop leader); Design Notes 30 ruled D4-1. A remedy you propose for an UNPLACEABLE label that sets a coordinate or field value must name the placer dry-run the Engineer runs before a revision opens (detail 1 common (h)); you read no scripts.

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_renderer.md (sections 2, 4, 5).
2. docs/sketches/wip/s2_plan_r6.png and docs/sketches/s2_plan_r5.png (Read each as an image; if a Read returns no image content, write "convention review NOT RUN" and stop).
3. research/sean/gameplan.md lines 138 (K4), 142 (K8), 190-204 (M1 rubric), 681 (Design Notes 30).
4. docs/sketches/s2_visual_gate_r3.md (your N2) and docs/sketches/s2_visual_gate_r1.md (Sign-off r4, D4-1).

TASK:
1. Hidden convention as drawn on S2 r6: dashed hidden edges read as hidden and nothing visible reads as hidden; N2 closed or not.
2. Placer order and the new last-quarter outline rule: sign or FIX.
3. Each UNPLACEABLE label: your remedy (for example a numbered callout keyed in the figure note, a label inside a clear region, accepting the leader inside a named outline) with the dry-run the Engineer must run; or "accept as reported" with reason.
4. Anything on S2 r6 that changed against r5 and reads worse.
Verdict line: "CONVENTIONS SIGNED (Designer)" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_designer_renderer_signoff.md
Return in context only: verdict, FIX count, UNPLACEABLE remedies.
```

P1Rf if FIX: P1R re-spawn with "READ FIRST 0: research/sean/cr_scratch/step1.3_topologist_renderer_signoff.md and step1.3_designer_renderer_signoff.md; TASK 0: close each FIX; dry-run every value-setting remedy before drawing; S2 becomes r7 only if pixels change again", output `step1.3_engineer_renderer_fixes.md`; then the raiser(s) re-check (TASK 0 "verify each FIX closed"), output `step1.3_{topologist|designer}_renderer_recheck.md`.

---

### STOP S3-A. Sean: rulings before (b)

Blocking for P2, after P1 and ORCH-A (may overlap P1R and its sign-offs). The orchestrator presents from P1 sections 3, 4, 5, 12, 13:
1. Every value that moves an S1 r7 or S2 r5 key, with the rows and margins that move (opens S1 r8 / S2 r(m+1), section 1.2).
2. S3-2: P1's margins, options (i) to (iii) and recommendation.
3. Sync: the option P1 recommends drawing; if it is a belt, its routing against S2-5a and the cutter sweep.
4. Hold device: the option P1 recommends drawing; if it needs a lead change, the S1 key and the F_stall consequence.
5. Inputs Sean owns (SF, F_bind) and every input P1 set without a source.
6. Batch 2 draft: send now or hold.
The orchestrator writes Design Notes 31 "Step 1.3 STOP S3-A rulings (Sean, <date>)" with Sean's words, adds a Progress row, applies gameplan lines from P1, P1R, P1Rt, P1Rd (and P1Rf), and makes save point 2. Items Sean defers go to M2; P2 draws P1's recommendation.

---

### P2. The Engineer, 1.3 (b) spec

Spawn: agent, `run_in_background: true` (**required**). After save point 2.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.3 (b): write docs/sketches/s3_spec.yaml from The Designer's params review and Sean's rulings (gameplan Design Notes 4 and 31), apply the overlay values, and bring the spec to "ready for signature". No drawing before the spec is signed. A value missing from both sources: stop and report it.
S1/S2 coupling: if Sean adopted a value for any key in docs/sketches/s1_checks_r7.json or s2_checks_r<m>.json keys_read, --stale reads red on that record after your overlay edit. Record the exact key list; it opens a revision you draw at (d). Do not suppress it. The DERIVED expr lint (step 0) will fire on any chain leaf you leave inconsistent: update top_guide_z, member_length and member_length_rail from their expr when their inputs move, and list the change.

READ FIRST:
1. research/sean/cr_scratch/step1.3_designer_params_review.md (whole file).
2. research/sean/gameplan.md Design Notes 4 and 31, lines 118-162 (detail 1.0, spec format, K table, g_min), 164-176 (detail 1 common), 267-295 (detail 1.3).
3. docs/sketches/s1_spec.yaml and s2_spec.yaml (format, shared rows, stack_ties, reported fields), proposed_params.yaml, sketch_loader.py, sketch_common.py, check_stack.py, check_sketch.py, checks_s2.py (pattern for checks_s3.py).
4. research/sean/cr_scratch/step1.3_engineer_step0.md (RPT, reported_items, --jobs) and step1.3_engineer_renderer.md (renderer entry point).
5. research/sean/cr_scratch/step1.3_manager_open.md findings O3, O4, O7, O11, O12.
6. params.yaml keys listed in detail 1.3 (grep); ASSEMBLY.md Coordinate frame (l.5-7).

TASK:
1. Overlay: apply the Designer's value table and Sean's rulings; each changed leaf with source "Designer 1.3 (a)" or "Sean STOP S3-A, Design Notes 31" plus basis and status; new leaves for E, SF, K, F_bind, rapid traverse, friction, bearing mass as ruled.
2. Spec docs/sketches/s3_spec.yaml: header (question from detail 1.3, R and Q rows, view per Design Notes 4/31 with plane, look direction and axis directions stated, `insets` with view plan_xy and the rows each inset draws, section convention (cut, beyond, removed), pose(s), load-case table, `reported_items` from the Designer's list, rubric additions, k7_tolerance statement, script s3_jackscrew_section.py); one row per part (id, name, shape, kind, axis, projection per view and inset, keys, place, z_rule, depth along the plane normal, section, label, neighbours with class and g_min and source, sense, notes, chain membership); the S3-3 chain per screw, each consecutive pair with the record that certifies it (S1 r7 K7 record pair id, S2 r<m> K7 record pair id, this figure, or declared for the S6 segment); list pairs no record certifies.
3. Part list (detail 1 common (b)): every part a shape string names has a row or a not_drawn entry with reason; figure_note.
4. checks_s3.py skeleton: S3-1, S3-2 (per Sean's ruling on its form), S3-3 (cross-record form per O11), STUB_EXPECT, STUB_CAUSE, SOURCES; implementations may fail closed until (c).
5. check_stack.py on the S3 spec: z per row per pose; hand and computed side by side: L_min per Q9 option, nut-to-anchor segment at park, P_cr per K, F_stall, per-screw forces per load case, back-drive angle, critical speed.
6. Rows shared with S1 or S2 use identical place, z_rule and plan_poly expressions (X1); list them.
7. Runs: --controls (default jobs), --stale and --stale --include-unaccepted; if an S1 or S2 key moved, preview check_sketch.py s1 --rev 8 / s2 --rev <m+1> with the unchanged scripts to wip/ (not of record) and list every value that moved.
8. Open items for signature.
Output sections: Corrections to the brief; 1 files changed; 2 part list; 3 row table (id, view or inset, extents, z band); 4 load cases and S3-2/S3-3 hand vs computed; 5 S3-3 chains with certifying records; 6 shared rows; 7 run results (with stale key lists), previews; 8 open items for signature; 9 Gameplan lines to change (at least: detail 1.3 Shows if wording changes, S3-2 row per the ruling, S3-3 row chain per screw, Echo Site Registry rows).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_engineer_spec.md
Return in context only: --controls counts and time, --stale result and key lists, previews, S3-2 margins, uncertified chain pairs, blocking items (under 12 lines).
```

### P3a. The Designer, 1.3 (b) spec sign-off (parallel with P3b)

Spawn: agent; background recommended. After P2.

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Step 1.3 (b) sign-off. You wrote the params review; The Engineer wrote the S3 spec and overlay from it and from Sean's rulings (Design Notes 4, 31). You sign or return FIX items; The Loftsman signs in parallel on arithmetic and placement. Your sign-off carries the shape-text part list.

READ FIRST:
1. research/sean/cr_scratch/step1.3_designer_params_review.md (your review).
2. research/sean/cr_scratch/step1.3_engineer_spec.md.
3. docs/sketches/s3_spec.yaml; docs/sketches/proposed_params.yaml.
4. research/sean/gameplan.md lines 148-153, 164-206, 267-295, Design Notes 4 and 31.

TASK:
1. Part list: every part any shape string names, with its row id or not_drawn reason. A named part with neither is a FIX.
2. Every row's shape matches your note; section convention (cut, beyond, removed) as you set it; inset content.
3. Options drawn as you recommended and as Sean ruled (nut mounting, sync, hold, anchoring); load-case table; reported_items complete against detail 1.3 Reported.
4. Neighbour classes and g_min per pair.
5. Operator-task rows consistent with the spec.
6. Rubric additions true on the spec values, each with a predicate or marked visual-only.
Verdict line: "SPEC SIGNED (Designer)" or "FIX" with numbered items, each naming row id and the required change.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_designer_spec_signoff.md
Return in context only: verdict, FIX count, part-list count (rows / not_drawn / missing).
```

### P3b. The Loftsman, 1.3 (b) spec sign-off (parallel with P3a)

Spawn: agent; background recommended (may run check_stack.py).

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Step 1.3 (b) sign-off on arithmetic and placement. S3 is the first sketch in a plane through a screw axis (1.3 open O4) and the first with a cross-sketch check (S3-3 reads accepted K7 records, O11). LF1.1-9 to -11 are yours to re-check on the S3 values.

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_spec.md.
2. docs/sketches/s3_spec.yaml, proposed_params.yaml, check_stack.py, checks_s3.py (skeleton).
3. docs/sketches/s1_spec.yaml and s2_spec.yaml shared rows; s1_checks_r7.json and s2_checks_r<m>.json (keys_read, K7 record entries for the chain pairs).
4. research/sean/cr_scratch/step1.3_designer_params_review.md sections 2 to 6, 11.
5. research/sean/gameplan.md lines 129-153, 267-295; ASSEMBLY.md Coordinate frame.

TASK:
1. Section-plane coordinates: the map from (x, y, z) to the figure's (u, z) for screw <screw> and the look direction; depth along the plane normal for every row; the inset map; hand values for the screw, nut, anchor, guide, member and lift motor positions beside check_stack.
2. Hand values: L_min per Q9 option (S1-4 and detail 1.3 expression), nut-to-anchor segment at park, P_cr per K, F_stall, per-screw forces per load case, back-drive angle, critical speed with its end factor.
3. S3-3 chain per screw: each consecutive pair, its certifying record, and whether that record's entry is class C and current (--stale); pairs no record certifies.
4. If an S1 or S2 key moved: every row, K7 pair and margin that moves (S1-4, L, member tops, S2-5a); whether the S1/S2 revision needs spec edits beyond comments.
5. Shared rows equal (X1); LF1.1-9 to -11 on the S3 values.
Verdict line: "SPEC SIGNED (Loftsman)" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_loftsman_spec_signoff.md
Return in context only: verdict, FIX count, uncertified chain pairs, S1/S2 spec-edit ruling.
```

### P2f. The Engineer, (b) fix pass (only if P3a or P3b returns FIX)

Spawn: background **required**. Then re-spawn only the raiser(s) with their prompt plus "READ FIRST 0: research/sean/cr_scratch/step1.3_engineer_spec_fixes.md; TASK 0: verify each of your FIX items closed", output `step1.3_{designer|loftsman}_spec_recheck.md`.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.3 (b) fix pass on the spec sign-off findings.

READ FIRST:
1. research/sean/cr_scratch/step1.3_designer_spec_signoff.md and research/sean/cr_scratch/step1.3_loftsman_spec_signoff.md.
2. research/sean/cr_scratch/step1.3_engineer_spec.md.
3. docs/sketches/s3_spec.yaml, proposed_params.yaml, check_stack.py, checks_s3.py, fixtures/manifest.yaml.

TASK:
Close every FIX item. A design value a reviewer asks for comes from that reviewer's file; if none is given, list it open. A value-setting FIX is dry-run through the predicate that will judge it before you apply it; one that fails returns to the raiser with the measurement (detail 1 common (h)). Re-run check_stack.py and check_sketch.py --controls; record results. Set the spec header `status: signed (Designer, Loftsman)` only after both re-checks return SIGNED; until then `status: fixes applied, awaiting re-check`.
Output: Corrections to the brief; one row per FIX item (ID, change, dry-run result, evidence); re-run results; Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_engineer_spec_fixes.md
Return in context only: items closed, items open, --controls counts.
```

Orchestrator after both SIGNED: apply gameplan lines from P2, P3a, P3b, P2f; save point 3 ("sean: Step 1.3 (b) S3 spec signed").

---

### P4. The Engineer, 1.3 (c) red-first

Spawn: background **required**. After save point 3.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.3 (c), red-first (detail 1 common (c)). The S3 spec is signed. Before the S3 stub run the harness gains: the per-Axes view and inset iteration (TP-7), the section view S3 declares (1.3 open O4), the renderer's section convention, the cross-record S3-3 (O11) and S3-2 in the form Sean ruled (Design Notes 31). Each new or relaxed rule states its premise and enforces it with its own Z and B; the raiser signs at P5T, P5L, P5 or at (e).

READ FIRST:
1. research/sean/gameplan.md lines 129-162 (spec format, K table, red-first baseline), 164-176 (detail 1 common), 267-295 (detail 1.3), 596 (Design Notes 20 TP-7), Design Notes 31.
2. docs/sketches/s3_spec.yaml (signed), checks_s3.py, check_sketch.py, sketch_common.py (setup_figure, VIEW_NORMAL, K3 to K9, renderer, placer), check_stack.py, fixtures/manifest.yaml, fixtures/builders.py, baseline_red.json, stubs/s2_stub.py (pattern).
3. research/sean/cr_scratch/step1.3_engineer_spec.md, step1.3_engineer_spec_fixes.md (if present), step1.3_loftsman_spec_signoff.md (plane coordinates, chain records).
4. research/sean/cr_scratch/step1.0_topologist_crossreview.md (TP-7), step1.3_engineer_renderer.md, step1.3_engineer_step0.md.
5. research/sean/cr_scratch/step1.3_manager_open.md findings O3, O4, O5, O11.

TASK:
1. TP-7: setup_figure (or a sibling it owns) creates each declared inset with its own view; every Axes carries its view; K3 to K9 iterate every declared Axes with that Axes' view and rows (the multi-Axes lint stays for undeclared Axes). Controls, each B red on the pre-change code: Z the signed spec's inset drawn correctly; B inset with y inverted (handedness); B screw drawn as a rectangle in the plan inset (projection); B an inset row drawn in the main Axes; B a declared inset absent.
2. Section view: the plane per the spec; labels, projection normal, K6 centre and stack in plane coordinates, K7 depth bands along the plane normal, K8 handedness of the section. Z live S3 spec fixture; B section drawn mirrored; B a part placed at x = r (side-view projection) instead of the plane coordinate.
3. Renderer section convention: cut rows hatched, rows beyond the plane in elevation with hidden edges dashed behind cut rows, rows in front omitted and named in the figure note; placer in the section and the inset. Z and B per convention item.
4. S3-1, S3-2 (per Design Notes 31), S3-3 (reads the K7 entries of the latest accepted S1 and S2 records for the pairs they certify, premise --stale clean enforced inside the check, plus the S3 figure; declared contacts for the S6 segment). S3-x fixtures from the signed spec: S3-1 B anchor at the top guide; S3-2 B 1000 N compression on an 850 mm T8 (or the ruling's equivalent); S3-3 B anchor member 1 mm clear of its foot; S3-3 B a chain pair absent from every record; S3-3 B a stale record. Each B with reason substring and planted count.
5. stubs/s3_stub.py; STUB_EXPECT, STUB_CAUSE, SOURCES in checks_s3.py; RPT on the stub labels drawn items absent.
6. Runs: --controls (default jobs; counts and time against the P0 target); check_sketch.py s3 --rev 0 to wip/ (every S3 check red for its own reason; K1, K2, K3, K5 green as labelled guards); --baseline s3; s1 --rev 7 (or 8) and s2 --rev <m> unchanged. A sketch check green on the stub is rewritten until it fails on content.
Output sections: Corrections to the brief; 1 rules (rule, premise, premise check, Z, B, red on pre-change code); 2 S3-x fixture table; 3 --controls counts and time; 4 stub run table against expectations; 5 code changes; 6 rules awaiting signature and by whom; 7 Gameplan lines to change (K3 to K9 rows for per-Axes and section rules, S3-1 to S3-3 rows, K table pointer, detail 1.3 carried items, Design Notes 20 TP-7 status).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_engineer_redfirst.md
Return in context only: --controls counts and time, stub red/green counts, rules added, any check rewritten.
```

### P5. The Software Engineer, 1.3 (c) check (parallel with P5T, P5L)

Spawn: background **required** (re-runs controls). After P4.

```
[BLOCK SWE]

CONTEXT:
[CTX COMMON]
Step 1.3 (c). Review before the S3 stub run is accepted as the red-first record: (1) P4 rules (per-Axes view, section view, renderer section convention, S3-3 cross-record read, S3-2 form), (2) the S3-x fixtures and stub, (3) the harness delta since your 1.3 step 0 check (P1R renderer and placer and their controls).

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_redfirst.md, step1.3_engineer_renderer.md (and _fixes if present), step1.3_engineer_step0.md.
2. docs/sketches/check_sketch.py, sketch_common.py, checks_s3.py, s3_spec.yaml, stubs/s3_stub.py, wip/s3_checks_r0.json, fixtures/manifest.yaml, fixtures/builders.py, baseline_red.json.
3. research/sean/gameplan.md lines 129-162, 164-176, 267-295, Design Notes 31.
4. Your files: research/sean/cr_scratch/step1.3_software_engineer_step0_check.md, step1.2_software_engineer_check.md.

TASK:
1. Each new rule's premise is enforced with its own Z and B; each branch has a B (delete a branch, see whether any control notices).
2. Each S3-x B fires on its reason with its planted count; S3 checks that cannot fail through the drawing (SW-10 class) named, stay or drop; S3-2's form matches Design Notes 31 and cannot pass silently.
3. Re-run --controls and s3 --rev 0; compare with the Engineer's counts and times.
4. Simplicity gate on the per-Axes design, the section view and the renderer.
Verdict: "PASS" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_software_engineer_check.md
Return in context only: verdict, FIX count, branch gaps, controls time.
```

### P5T. The Topologist, 1.3 (c) TP-7 and section sense (parallel with P5, P5L)

Spawn: agent; background recommended. After P4.

```
[BLOCK TOP]

CONTEXT:
[CTX COMMON]
Step 1.3 (c). TP-7 is yours: an inset declared in the spec must be checked as its own view. P4 wrote per-Axes views, the section view and the renderer's section convention. Sign each or FIX.

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_redfirst.md sections 1, 2, 6.
2. docs/sketches/sketch_common.py (setup_figure and inset creation, K3 to K9 per-Axes iteration, section-view K8, renderer section convention), s3_spec.yaml, checks_s3.py, fixtures/manifest.yaml.
3. Your file research/sean/cr_scratch/step1.0_topologist_crossreview.md (TP-7).

TASK:
1. Per-Axes iteration: every K-check reads each declared Axes with its own view; the inset B controls reproduce an inverted and a mis-projected inset on the pre-change code.
2. Section handedness: the sign check that fixes the look direction ((u axis x z axis) against the plane normal), hand value beside the harness.
3. Section convention: cut, beyond, removed as half-space classifications against the plane; the figure note names removed rows.
4. Radial symmetry (your 1.2 (c) NOTE 1) for any radial part in the inset: predicate or M1 item.
Verdict line: "TP-7 SIGNED; SECTION RULES SIGNED" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_topologist_redfirst_signoff.md
Return in context only: verdict, FIX count.
```

### P5L. The Loftsman, 1.3 (c) section coordinates and cross-record S3-3 (parallel with P5, P5T)

Spawn: agent; background recommended. After P4.

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Step 1.3 (c). P4 implemented the section-plane coordinates you specified at (b), K6 and K7 in that plane, S3-2 per Design Notes 31 and S3-3 reading accepted K7 records. Sign each or FIX.

READ FIRST:
1. research/sean/cr_scratch/step1.3_engineer_redfirst.md sections 1, 2, 4, 6.
2. docs/sketches/sketch_common.py (section view K6, K7 depth along the plane normal), checks_s3.py (S3-1 to S3-3), s3_spec.yaml, check_stack.py, fixtures/manifest.yaml.
3. Your file research/sean/cr_scratch/step1.3_loftsman_spec_signoff.md.

TASK:
1. K6 and K7 in the section plane: hand values for three placed rows (centre in u, z; depth band) beside the harness on the stub fixture or the Z fixture.
2. S3-2: the formula, inputs and per-case arithmetic as implemented; the ruled form cannot pass a red silently.
3. S3-3: each chain pair resolved from the right record; the stale premise enforced; the B controls reproduce a missing pair and a stale record.
Verdict line: "SECTION AND S3 CHECKS SIGNED (Loftsman)" or "FIX" with numbered items.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_loftsman_redfirst_signoff.md
Return in context only: verdict, FIX count.
```

P5f if any FIX: P4 re-spawn with "READ FIRST 0: the FIX files among step1.3_software_engineer_check.md, step1.3_topologist_redfirst_signoff.md, step1.3_loftsman_redfirst_signoff.md; TASK 0: close each FIX", output `step1.3_engineer_redfirst_fixes.md`; then each raiser re-checks (TASK 0 "verify each FIX closed"), output `step1.3_{software_engineer|topologist|loftsman}_redfirst_recheck.md`. Then apply gameplan lines; save point 4 ("sean: Step 1.3 (c) red-first, harness checked").

---

### P6. The Engineer, 1.3 (d) draw S3 r1 (and any key-driven S1/S2 revision)

Spawn: background **required**. After save point 4. The orchestrator polls `docs/sketches/wip/s3_*_r1.png` for STOP-T5.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.3 (d): write the S3 script and iterate until K1 to K9, X1, RPT and S3-1 to S3-3 are green (S3-2 per Design Notes 31). Draw through the renderer and the leader placer; an UNPLACEABLE label goes into the output for The Designer, never to a hand-placed fall-back. The first PNG goes to Sean for an orientation preview; write it before iterating. Fix the drawing, never the check or the spec; a spec defect goes in the output as an open item for The Designer.
S1/S2 revisions: [orchestrator states: "triggered: Sean adopted <keys> at STOP S3-A (Design Notes 31); draw S1 r8 / S2 r<m+1>" / "not triggered: S2 stays r<m>, S1 stays r7"]. If triggered: s1_side_poses.py, check_sketch.py s1, s1_mass_report.py and s2_plan.py, check_sketch.py s2 at the new revision to wip/ (18/18, 17/17 required), script edits only where an expression must change, spec edits only as The Loftsman ruled at (b).

READ FIRST:
1. research/sean/gameplan.md lines 164-206 (detail 1 common, operator-task table, rubric, applicability), 267-295 (detail 1.3), Design Notes 4 and 31.
2. docs/sketches/s3_spec.yaml (signed), proposed_params.yaml, sketch_common.py (setup_figure, inset, renderer, placer), sketch_loader.py, check_stack.py, check_sketch.py, checks_s3.py, s2_plan.py and s1_side_poses.py (patterns).
3. research/sean/cr_scratch/step1.3_designer_params_review.md (shape notes, convention, options, operator rows).
4. research/sean/cr_scratch/step1.3_engineer_redfirst.md, step1.3_software_engineer_check.md, step1.3_topologist_redfirst_signoff.md, step1.3_loftsman_redfirst_signoff.md (and fixes/rechecks if present).
5. research/sean/cr_scratch/step1.3_loftsman_spec_signoff.md section 4 if S1/S2 revisions are triggered.
6. supplements/llm_plm_cad.md lines 570-597 (8.4.1, 8.4.2); ASSEMBLY.md Coordinate frame.

TASK:
1. Write docs/sketches/s3_jackscrew_section.py: the section figure and its inset through setup_figure and the inset owner, draw(gid), the renderer and the placer; every value from the loader; shapes per the spec; output through sketch_loader.output_path.
2. Write wip/s3_jackscrew_section_r1.png first; note the write time.
3. check_sketch.py s3 --rev 1; iterate (use --controls --only for interim control runs) until every check is green.
4. K1 on the script: literals found, angle sources.
5. Reported items in wip/s3_summary_r1.md through RPT (every item of the spec's reported_items).
6. S1/S2 revisions if triggered: results; table quantity, old, new; PNG paths.
7. Final runs: --controls full (default jobs), --stale (red only on adopted keys, if triggered).
Output sections: Corrections to the brief; 1 files written; 2 iteration log (run, red checks, fix); 3 final check table S3 (and S1/S2); 4 reported items; 5 UNPLACEABLE labels; 6 S1/S2 comparison; 7 open items; 8 Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_engineer_draw_r1.md
Return in context only: final check counts (S3; S1/S2 if drawn), PNG paths, S3-2 margins, L_min, UNPLACEABLE labels.
```

### STOP-T5 (non-blocking). Sean: orientation preview

When `docs/sketches/wip/s3_jackscrew_section_r1.png` exists, the orchestrator shows Sean the PNG and asks V1 (floor at the bottom; motor and nut hang as the spec states), V5 (screw vertical, anchor at the bottom, guide at the top, nut on the ring) and the inset's handedness (+X right along slot line C, theta counter-clockwise from +X seen from +Z, screws at 30, 150, 270). Not acceptance. Corrections go to Design Notes 13 as `S3-r1` with Sean's words and into P9.

---

### P7a. The Loftsman, 1.3 (e) cross-review (parallel with P7b and P8)

Spawn: background recommended. After P6.

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Step 1.3 (e), geometry cross-review (A.4 step 2): lengths, buckling and stall arithmetic, section placement, chain. Re-compute at least one value per check by hand and write it beside the JSON value. M1 runs in parallel on the same revision.
S1/S2 revisions: [orchestrator states triggered with keys, or not triggered]. If triggered, cross-review the changed rows only.

READ FIRST:
1. docs/sketches/s3_jackscrew_section.py, s3_spec.yaml, wip/s3_checks_r1.json, wip/s3_summary_r1.md, proposed_params.yaml, check_stack.py, checks_s3.py, sketch_common.py (section K6, K7).
2. research/sean/cr_scratch/step1.3_engineer_draw_r1.md, step1.3_engineer_redfirst.md section 1.
3. ASSEMBLY.md Coordinate frame; research/sean/gameplan.md lines 129-153, 267-295.
4. Your files: research/sean/cr_scratch/step1.3_loftsman_spec_signoff.md, step1.3_loftsman_redfirst_signoff.md.
5. If S1/S2 revisions: the new wip/ checks JSON and the accepted records.

TASK:
1. Hand values beside JSON: L_min per Q9 option; segment at park; P_cr per K and every compression case; F_stall; critical speed with end factor; back-drive angle; axial force in each kept part at 1000 N and at F_stall; per-screw and two-screw shares; K6 centre of at least three rows in plane coordinates; K7 depth bands of the screw, nut and member.
2. S3-1 at every nut position from the S1 poses; S3-3 chain per screw with the certifying records.
3. LF1.1-9 to -11 on the drawn blocks and motor mount.
4. Reported items: arithmetic only, no thresholds.
5. S1/S2 changed rows if triggered.
Findings LF1.3-n as BLOCK, FIX or NOTE. Verdict line: "CROSS-REVIEW PASS" or "CROSS-REVIEW FAIL"; separate verdicts for S1/S2 revisions.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_loftsman_crossreview.md
Return in context only: verdict(s), counts.
```

### P7b. The Topologist, 1.3 (e) cross-review (parallel with P7a and P8)

Spawn: background recommended. After P6.

```
[BLOCK TOP]

CONTEXT:
[CTX COMMON]
Step 1.3 (e), cross-review: sense and half-space in the section and the inset, renderer output, K9 coverage. Re-compute at least one K8 predicate by hand through the artist transform chain and write it beside the JSON value. M1 runs in parallel on the same revision.
S1/S2 revisions: [orchestrator states triggered with keys, or not triggered]. If triggered, sense and projected_extent on changed rows.

READ FIRST:
1. docs/sketches/s3_jackscrew_section.py, s3_spec.yaml, wip/s3_checks_r1.json, sketch_common.py (per-Axes K5, K8, K9; renderer).
2. research/sean/cr_scratch/step1.3_engineer_draw_r1.md, step1.3_engineer_redfirst.md section 1.
3. research/sean/cr_scratch/step1.3_designer_params_review.md sections 2 and 4 (convention, options).
4. ASSEMBLY.md Coordinate frame; research/sean/gameplan.md lines 133-145 (K table), 188-206 (rubric), 267-295.
5. Your files: research/sean/cr_scratch/step1.3_topologist_redfirst_signoff.md, step1.3_topologist_renderer_signoff.md.

TASK:
1. Anchor below nut below guide on the drawn screw at every pose the spec draws; section handedness; inset handedness ((p1 x p2) . z > 0 for consecutive screws).
2. Section convention as drawn: cut, beyond, removed; hidden edges where the renderer says.
3. K9: every row drawn in its declared Axes; all three screws and the sync parts in the inset.
4. S3-3 chain order per screw.
5. TP-n: parts drawn narrower than their footprints.
Findings TP1.3-n. Verdict line: "CROSS-REVIEW PASS" or "CROSS-REVIEW FAIL"; separate verdicts for S1/S2 revisions.
Output ends with Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_topologist_crossreview.md
Return in context only: verdict(s), counts, TP-n list length.
```

### P8. The Designer, 1.3 (f) M1 visual gate (parallel with P7a and P7b on r1)

Spawn: **fresh** agent on an image-capable model (the orchestrator's default subagent model; no text-only override; not P1, P1Rd, P3a or any spawn that drew or signed the renderer). Background recommended. The packet excludes `key.json` in every location. On r1 this runs in parallel with P7a/P7b; on later revisions (P8r) after the re-checks, again fresh.

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Step 1.3 (f), M1 visual gate (gameplan l.188-206; A.3.1 Visual gates). You did not produce these images. You must see pixels: open each PNG with the Read tool. If a Read returns no image content, write your numeric results and the line "visual gate NOT RUN" and stop.
Reviewer-model controls: four extra figures. ctrl_a.png and ctrl_b.png are drill side views: judge each on V1 to V5. ctrl_c.png and ctrl_d.png are plan views: judge each on handedness (+X to the right along the slot line, +Y up, theta counter-clockwise from +X seen from +Z). You are not told which figure is which.
Also gated here: S2 r<m> (renderer revision, [orchestrator: "r6" or the latest]) and, if drawn, S1 r8, each in its own file.

READ FIRST:
1. Control figures (Read each as an image): docs/sketches/wip/fixtures/figs/ctrl_a.png, ctrl_b.png, ctrl_c.png, ctrl_d.png. Never open key.json.
2. docs/sketches/wip/s3_jackscrew_section_r<k>.png (Read as an image).
3. docs/sketches/s3_spec.yaml (question, rubric_additions, section convention, inset, options drawn).
4. research/sean/gameplan.md lines 178-206 (operator-task table, rubric applicability, M1 rubric V1 to V10), 537-547 (Design Notes 13).
5. docs/sketches/wip/s3_checks_r<k>.json and wip/s3_summary_r<k>.md.
6. docs/sketches/wip/s2_plan_r<m>.png and docs/sketches/s2_plan_r5.png (Read both), docs/sketches/s2_spec.yaml, wip/s2_checks_r<m>.json.
7. If S1 r8: docs/sketches/wip/s1_pose_{load,start,capture_end,park}_r8.png and docs/sketches/s1_pose_load_r7.png (Read each), s1_spec.yaml, wip/s1_checks_r8.json.

TASK:
1. Controls: one line per figure ctrl_a to ctrl_d, PASS or FAIL each, with what you see.
2. S3: one line per applicable rubric item (V1, V5, V6, V7, V8, V9; V10 if the spec carries S3 operator rows; others N/A), PASS or FAIL with what you see. V7: the jack screw reads with nut, bottom anchor and top guide; the thrust bearing as a bearing in a block; the NEMA 17 as body and shaft with a coupling; the hold device as the option it is; the inset shows three screws and the sync method.
3. One line per S3 rubric addition; the section convention reads (cut hatched, beyond in elevation, hidden dashed); radial symmetry of any radial part in the inset (Topologist 1.2 (c) NOTE 1).
4. V9: your one-sentence answer to the S3 question from the figure alone, then the spec question.
5. S2 r<m>: V2, V6 to V10 and the S2 rubric additions; what changed against r5 (hidden edges, leaders) and whether it reads correctly.
6. S1 r8 if drawn: V1 to V10, the S1 rubric additions, what changed against r7.
7. Overall PASS per sketch only if every applicable item passes. FAIL items as numbered findings with the feature id. A finding that sets a coordinate or field value states the dry-run the Engineer must run (detail 1 common (h)).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: docs/sketches/wip/s3_visual_gate_r<k>.md, docs/sketches/wip/s2_visual_gate_r<m>.md (and docs/sketches/wip/s1_visual_gate_r8.md if gated). Each file ends with a section "Gameplan lines to change".
Return in context only: control verdicts per figure, overall verdict and FAIL count per sketch.
```

Orchestrator scoring after P8: per `key.json`, ctrl_a must FAIL V3, ctrl_b PASS, ctrl_c PASS handedness, ctrl_d FAIL handedness. Any mismatch: replace the reviewer model and re-run P8 before gating. Record the result in each visual-gate file footer and the Progress Log.

---

### P9. The Engineer, (h) revision r<k+1>

Spawn: background **required**. On r1: after P7a, P7b, P8 (and T5) return; one revision for all findings.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Step 1.3 (h): revision r<k+1> of S3 [and S2 r<m+1> / S1 r<n+1> if a finding applies]. Sources: [orchestrator lists: step1.3_loftsman_crossreview.md, step1.3_topologist_crossreview.md, docs/sketches/wip/s3_visual_gate_r<k>.md, s2_visual_gate_r<m>.md, Sean T5 / M2 rows verbatim from Design Notes 13].
Rule (h): a correction a signed predicate can express becomes a K8 predicate with a B fixture that reproduces the error. A new or relaxed rule states its premise, enforces it with its own Z and B in this revision, and its raiser signs before M1. A FIX that sets a value, field setting or coordinate is dry-run through the predicate that will judge it before you apply it; one that fails returns to the raiser with the measurement and does not enter the revision.

READ FIRST:
1. research/sean/gameplan.md lines 164-176 (detail 1 common), 537-547 (Design Notes 13), Design Notes 31.
2. Every source file named above.
3. docs/sketches/s3_jackscrew_section.py, s3_spec.yaml, proposed_params.yaml, checks_s3.py, sketch_common.py, fixtures/manifest.yaml.
4. research/sean/cr_scratch/step1.3_engineer_draw_r<k>.md (or step1.3_engineer_revision_r<k>.md).

TASK:
1. Per finding: dry-run result where required, fix, K8 predicate ID and B fixture or "visual only". A finding that changes a design value or the spec goes to The Designer (list it; spec re-sign by The Designer and, for placement, The Loftsman). A value change to an S1 or S2 key goes to the orchestrator for Sean.
2. Redraw as r<k+1> to wip/; check_sketch.py s3 --rev <k+1> (and s1/s2 if affected); --controls full at the end; iterate to green.
3. Reported items in wip/s3_summary_r<k+1>.md through RPT.
4. List new rules and their raisers for signature.
Output: Corrections to the brief; table (finding ID, source, dry-run, fix, K8 predicate ID or "visual only", B fixture); check results; PNG paths; rules awaiting signature; Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_engineer_revision_r<k+1>.md
Return in context only: findings closed, findings returned on failed dry-run, predicates added, rules awaiting signature, check counts.
```

After P9: P7r re-check by each raiser (same prompt, TASK 0 "verify each of your findings closed against step1.3_engineer_revision_r<k+1>.md; sign any rule you raised", output `step1.3_{loftsman|topologist}_recheck_r<k+1>.md`); then P8r (fresh image-capable spawn on r<k+1>, controls included, output `docs/sketches/wip/s3_visual_gate_r<k+1>.md` and the S1/S2 equivalents for any sketch redrawn). The revision presented at M2 must carry a fresh M1 PASS file on its exact pixels, or a pixel-equality statement (SHA-256 or pixel compare) to a revision that has one (KC11). Apply gameplan lines; save point 5; STOP M2.

### STOP M2. Sean: correction pass

Present: `docs/sketches/wip/s3_jackscrew_section_r<k>.png`, `wip/s3_visual_gate_r<k>.md`, `wip/s3_summary_r<k>.md`; S2 r<m> beside `s2_plan_r5.png` with the changed items and `wip/s2_visual_gate_r<m>.md`; S1 r8 package if drawn. Sean answers V1, V5, V9 for S3 (V2 and V9 for S2; V1 to V5 and V9 for S1 r8), gives free corrections and picks: nut mounting (rigid or floating), sync method, hold device, anchoring (thrust bearing type, top guide type), and any STOP S3-A item he deferred. The orchestrator writes each correction into Design Notes 13 as `S3-r<k>` (or `S2-r<m>`, `S1-r8`) with Sean's words, each pick into Design Notes 13 and Design Notes 31. Corrections: P9, P7r, P8r, M2 again. Acceptance: "S3-r<k> accepted" (and S2, S1 rows) with date in Design Notes 13, then ORCH-B.

### ORCH-B. Orchestrator after acceptance

1. `check_sketch.py --accept s3 --rev <k> --note "Design Notes 13 S3-r<k>"`; copy-up from wip/ with equality (PNG, checks JSON, summary, visual gate). Copy `wip/s3_checks_r0.json` up as the S3 red-first record.
2. `check_sketch.py --accept s2 --rev <m> --note "Design Notes 13 S2-r<m>"` (r5 marked superseded); `--accept s1 --rev 8` if accepted.
3. `check_sketch.py --stale`: 0 differences on every latest accepted record (3 records).
4. Apply remaining gameplan lines; save point 6 ("sean: Step 1.3 S3 r<k> accepted").

---

### P10. The Manager, Step 1.3 close

Spawn: background **required** (re-runs `--controls`).

```
SYSTEM: You are The Manager (method/operational_guide.md A.12.1; read it, plus A.4 step 7, A.5.2, A.5.3, A.3.1 Visual gates).

CONTEXT:
[CTX COMMON] (The Manager may edit research/sean/gameplan.md and research/sean/accumulator.md.)

READ FIRST:
1. research/sean/cr_scratch/step1.3_manager_open.md (this file: findings O1 to O14, done criteria KC1 to KC14, section 1.2 S1/S2 revision rule, section 5 edits).
2. Every research/sean/cr_scratch/step1.3_*.md file; docs/sketches/s3_visual_gate_r<k>.md, s3_checks_r<k>.json, s3_summary_r<k>.md, s3_checks_r0.json (and S2/S1 equivalents accepted in 1.3).
3. research/sean/gameplan.md Steps rows 1 and 1.3, detail 1 common, detail 1.3, K table, Design Notes 4, 13, 20, 25, 31, Progress Log, Echo Site Registry, Open Questions N2, N5, N7, N12.
4. research/sean/accumulator.md (sections of the personas that ran).

TASK:
1. Verify KC1 to KC14 with evidence; re-run from docs/sketches/: check_sketch.py --controls (default jobs; time against 200 s), check_sketch.py s3 --rev <k>, s2 --rev <m>, s1 --rev <7 or 8>, --stale. Confirm the runs leave committed files unchanged (SHA-256 before and after).
2. Audit that each agent's "Gameplan lines to change" was applied at the save point after it, and that every agent return has its own Progress row; list misses.
3. Disposition of each finding O1 to O14 (closed with evidence, or carried with step and owner).
4. Sequencing check for 1.4 (S4): any check cited before the step that writes it (S4-a to S4-d, holder section from build_parts/holder.py, the S4 back-edge into S1 heights, section view reuse from S3).
5. Process: count revisions and their causes; system or one-off. Did the renderer, placer and FIX dry-run rule remove the 1.2 rendering-convention revisions? Controls time per run across the step.
6. Gameplan close edits: Steps row 1.3, Current step, Progress Log, Design Notes 20 (TP-7) and 25 rows closed, Echo Site Registry (screw length, member tops, anchor and guide heights, lift motor, sync, hold), Open Questions N2 (nut mounting), N7, Q8.
7. Accumulator entries for every persona that ran and for The Manager.
8. Decisions for Sean at the inter-step gate.
Verdict: READY FOR SEAN or NOT READY with items.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.3_manager_close.md
Return in context only: verdict, KC criteria met count, decisions for Sean (under 10 lines).
```

## 4. Blockers

| # | Blocker | Effect | Resolution |
|---|---|---|---|
| B1 | Design Notes 4 re-confirmation and section screw (O1, O4) | P1 cannot set the plane; P4 cannot build the view | STOP S3-0 |
| B2 | S3-2 red by construction on the seeds; detail 1.3 and (d)/--accept disagree on a red S3-2 (O3) | S3 cannot be accepted as the harness stands | P1 options; STOP S3-A item 2; P4 implements the ruled form |
| B3 | No section view for a plane through a screw axis (O4) | Stub and draw cannot run | P4 with Z and B; P5L, P5T sign |
| B4 | No per-Axes view; K5 to K9 read axes[0]; a declared inset silences K3 (O5) | S3 inset unchecked | P4 (TP-7) before the stub |
| B5 | Member-top tie absent and DERIVED chain leaves unchecked (O2) | An S3 length change passes silently into S1 and S2 | P0, before (b); Loftsman signs |
| B6 | Block and motor-mount values unsourced and read by S1 r7 / S2 r5; S1-4 identity 0.84 (O6) | Any change reopens S1 and S2 | P1 proposes; STOP S3-A; S1 r8 / S2 r(m+1) under (i) |
| B7 | Belt sync enclosing the axis turns S2-5a red (O7) | A belt option touches an accepted check | P1 routing; STOP S3-A |
| B8 | Controls 794 s serial (O9) | About 13 min per run, about 15 runs in the step | P0 task 1, target 200 s |
| B9 | No renderer or leader placer (O8); D5 orders them before the first S3 draw | S3 r1 would repeat the 1.2 revision pattern | P1R (plan) and P4 (section) before P6 |
| B10 | No input leaves for E, SF, K, F_bind, rapid traverse, friction, bearing mass (O14) | S3-2, critical speed and back-drive cannot be computed from the overlay | P1 proposes; Sean rules SF and F_bind at STOP S3-A |
| B11 | Batch 1 unanswered (Q2, Q9, N5, N7, N10) | W, L, heights and the N5 kept-part forces stay ASSUMED | None for 1.3; reported |

Not a blocker: S2 r6 (renderer) and any key-driven S1/S2 revision run inside 1.3 under detail 1 common (i); "the next sketch opens only after acceptance" governs S4, which opens after S3 and every S1/S2 revision opened in 1.3 are accepted.

## 5. Gameplan lines to change (orchestrator, at the open save point)

1. l.12, header Current step. Old: `**Current step:** 1.3 (S3) approved to open (Step 1.2 approved by Sean 2026-11-25; research/sean/cr_scratch/step1.2_manager_close.md)` New: `**Current step:** 1.3 (S3) in progress (opened 2026-11-25, research/sean/cr_scratch/step1.3_manager_open.md)`
2. l.91, Steps row 1.0, status cell end. Old: `Carried items in Design Notes 20. Awaiting Sean |` New: `Carried items in Design Notes 20. Approved by Sean 2026-11-25 (Design Notes 21) |`
3. l.93, Steps row 1.2, status cell end. Old: `Carried items in detail 1.3 and Design Notes 25. Awaiting Sean |` New: `Carried items in detail 1.3 and Design Notes 25. Approved by Sean 2026-11-25 (gate decisions D1 to D5, Progress Log) |`
4. l.94, Steps row 1.3, status cell. Old: `S3-1 to S3-3 | Not started |` New: `S3-1 to S3-3 | In progress (opened 2026-11-25, research/sean/cr_scratch/step1.3_manager_open.md): STOP S3-0, step 0 with (a), renderer and S2 r6, STOP S3-A, (b) to (h); S1 r8 / S2 revisions inside 1.3 if a key moves |`
5. l.519, Design Notes 4 header. Old: `**4. S3 redefinition (for Sean to confirm).**` New: `**4. S3 redefinition (accepted by Sean at the Step 0 gate 2026-11-24, decision 2; re-confirmed at the 1.3 open, STOP S3-0, <date>: "<Sean's words>"; section through screw <screw>).**` (filled at the stop)
6. l.521. Old: `**5. Sketch drawing order and decision locus (for Sean to confirm).**` New: `**5. Sketch drawing order and decision locus (accepted by Sean at the Step 0 gate 2026-11-24).**`
7. l.523. Old: `**6. Proposed-keys overlay (for Sean to confirm).**` New: `**6. Proposed-keys overlay (accepted by Sean at the Step 0 gate 2026-11-24).**`
8. l.525. Old: `**7. Shared location for accepted sketches (for Sean to confirm).**` New: `**7. Shared location for accepted sketches (accepted by Sean at the Step 0 gate 2026-11-24).**`
9. l.529. Old: `**9. Week-close record is prose (for Sean to confirm).**` New: `**9. Week-close record is prose (accepted by Sean at the Step 0 gate 2026-11-24).**`
10. l.566. Old: `**16. The kept base parts carry the cut reaction under the screw lift (for Sean to confirm; Quinn rules, N5).**` New: `**16. The kept base parts carry the cut reaction under the screw lift (accepted by Sean at the Step 0 gate 2026-11-24; Quinn rules, N5).**`
11. l.268, detail 1.3. Old: `Redefinition for Sean to confirm (Design Notes 4): a one-screw section` New: `Redefinition confirmed (Design Notes 4; section screw named at the 1.3 open): a one-screw section`
12. l.546, Design Notes 13 row S2-r5, correction cell. Old: `the descent-stop leader inside tie b goes to S3 with N2 (Design Notes 30). r1 to r5 came from the 1.2 reviews |` New: `the descent-stop leader inside tie b goes to S3 with N2 (Design Notes 30). r1 to r5 came from the 1.2 reviews. Step 1.2 gate D1 (2026-11-25): accepted without a fresh M1 on the r4/r5 pixels (last fresh M1 PASS r3; r4 signed by the Designer's delta read; D4-1 closed by Design Notes 30) |`
13. l.748, Open Questions N2, status cell. Old: `the S2 M2 pick of the guide option is not named in Design Notes 13 (1.2 close D2)` New: `guide option picked by Sean at the Step 1.2 gate (D2, Design Notes 27)`
14. Detail 1.3, insertion after the line beginning `Carried from Step 1.2 (Manager close, `research/sean/cr_scratch/step1.2_manager_close.md` section 4):` — new line: `Sequenced at the 1.3 open (`research/sean/cr_scratch/step1.3_manager_open.md` section 1.1): step 0 (P0) carries item (1) with a K2 agreement lint for DERIVED overlay leaves (top_guide_z, member_length, member_length_rail are literals), item (5) as `--controls --jobs N` (target 200 s) and `--only`, item (6) as check RPT on spec field `reported_items`, and from item (3) TP1.1-9, TP1.2-18, Topologist NOTE 2 and Loftsman NOTE 1; P1R carries item (4) in plan with TP1.2-13 and TP1.2-19 and opens S2 r6; (c) carries TP-7 as a view per Axes, the section view for the screw Sean names, the renderer's section convention and S3-3 reading the accepted K7 records. S3-2 is red on the seeds (P_cr / F 2.23 capture lift, 1.05 stall at K = 1, SF 3, DERIVED at the open); its form goes to Sean at STOP S3-A before (b).`
15. Design Notes, new entry after 30 (insertion after the line beginning `**30. Descent-stop leader, D4-1 closed with no geometry change`): `**31. Step 1.3 STOP S3-A rulings (Sean, <date>, on `research/sean/cr_scratch/step1.3_designer_params_review.md`).**` with Sean's words per item (filled at the stop).
16. Progress Log, insertion after the row beginning `| 1.2 | 2026-11-25 | Approved by Sean ("Approve all five"`: `| 1.3 | 2026-11-25 | Opened by Manager (research/sean/cr_scratch/step1.3_manager_open.md): done criteria KC1 to KC14, sequence STOP S3-0, P0 with P1, P0L/P0T/P0S, ORCH-A, P1R and S2 r6, STOP S3-A, P2 to P10; findings O1 to O14 (record defects incl. Design Notes 4 already accepted at the Step 0 gate; member-top tie absent and DERIVED chain literals unchecked; S3-2 red on the seeds; no section view or per-Axes view; belt sync against S2-5a; renderer and placer; controls 794 s). Next: STOP S3-0. |`
