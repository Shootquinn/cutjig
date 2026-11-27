# Step 1.4 Manager Open (sean): S4, side section through the base

Date: 2026-11-27. Step-open pull: commit 5c52522, tree clean (DECLARED, orchestrator). Sources: gameplan header, Steps rows 1, 1.3, 1.4, detail 1.0 (K table), detail 1 common (incl. record keeping, rule scope, control blinding), operator-task table, rubric applicability, M1 rubric, detail 1.4, Context Recipes, Design Notes 8, 13, 16, 20, 24, 25 (S4-a to S4-d, C1.3-a, C1.3-b), 26 to 32, Echo Site Registry, Open Questions, Repository Sync item 6; `step1.3_manager_close.md` (all sections); `step1.3_manager_open.md` (format, section 3.0 blocks); `research/sean/accumulator.md`; `docs/sketches/check_sketch.py` (controls, stale), `sketch_common.py` l.45, `fixtures/builders.py` l.1961-1979, `s1_checks_r8.json`, `s2_checks_r9.json`, `s3_checks_r7.json`, `s1_spec.yaml`, `s3_spec.yaml` (row ids), `params.yaml` (core, collet, stop, holder, receiver), `proposed_params.yaml` (collet.core_stop_z); ASSEMBLY.md (receiver floor, clamp loop); critical path Q4, Q5, Q6, Q10, R10 to R12; `method/operational_guide.md` A.3.1 to A.3.5, A.4, A.5.4, A.9, A.10, A.12.

Runs at this open (MEASURED): `check_sketch.py --stale` 3 records checked (s1 r8, s2 r9, s3 r7), 0 differences; X1 pass, 70 shared rows, 3 skipped. C: free 6.22 GB (6.51 GB at the 1.3 close). A read-only `git log -1` (5c52522) was run against the open's "no git" rule; nothing else touched git.

TDD precondition (A.4): S4 is a sketch. Its suite is the signed harness (K1 to K9, X1, SYM, RPT; 413 controls at the 1.3 close) plus S4-1 to S4-3. Its outline is `s4_spec.yaml`, signed at (b), and its red-first run is (c). The precondition is met for opening step 0 and (a). LLM-PLM 8.4 governs (a), (b) and (f).

Numbering: findings are F4-1 to F4-16 and done criteria DC1 to DC15. Sub-steps are P0 to P10 as at 1.3. Stops are STOP S4-0, STOP S4-A, STOP-T5 and STOP M2. File names carry `step1.4_`.

## 0. Findings at open

Numbers are tagged MEASURED (read from a file or a run at this open), DERIVED (arithmetic on those) or DECLARED.

| # | Finding | Basis | Disposition |
|---|---|---|---|
| F4-1 | **Control key: four leak routes. A plain re-letter rebuilds the defect.** (a) The 1.1 to 1.3 open files print the mapping (close 3.1). (b) Gameplan l.195 tells the reviewer the expected outcomes ("Z must pass; B1 must fail V3"), and l.196 prints the old mapping in full. DN24 l.668 prints the scores. Before 1.3 the M1 prompt pointed at "gameplan lines 178-206", which take in l.195. (c) A route the close did not name: the [BLOCK DES] SESSION HISTORY pasted into every 1.3 M1 spawn carries the old control scores, letter by letter, in its Cycle 1.1 entry (1.3 open l.166; accumulator l.30). (d) `builders.control_figures` hard-codes the letter-to-figure mapping as a literal (l.1972), and `--controls` writes `key.json` into `wip/fixtures/figs/`, beside the PNGs the reviewer opens (check_sketch.py l.495-500). If S4 re-letters with a new fixed literal, the next open or the source file prints the key again | MEASURED (files and lines named) | **P0 R3**: a new `--m1-controls` command gives each M1 round fresh random tokens. It writes only the four PNGs to the reviewer folder and puts the key outside the project tree. `--controls` stops generating reviewer figures. The M1 persona block [BLOCK DES-M1] carries no control text. The M1 prompt pastes the rubric itself and never points at the gameplan or this file. Gameplan l.195-196 is rewritten (section 6 item 5). This file states no mapping or expected verdict for any 1.4 round. The old fixed-letter mapping appears here only as quoted old text ([BLOCK DES] history, copied verbatim from the accumulator; the section 6 Old blocks), and per-round random tokens void it. Scoring is in section 5, against the out-of-tree key |
| F4-2 | **G5's gap is a class, not one case.** A record stores `files_sha256` for params.yaml and the overlay only. It names the spec and script without hashing them. `--stale` compares `keys_read` alone (check_sketch.py l.689-696). Three record inputs are invisible to it: certifier records (G5, S4-Q3), spec edits that move no key (neighbour classes, `section` pieces, not_drawn bands; R2-6 is one member of this class), and script edits. Under the G2 rule-scope ruling the branch covers all three | MEASURED (s3_checks_r7.json fields: sketch, rev, timestamp, spec, spec_status, script, accepted, frame, files_sha256, keys_read, ...) | **P0 R2**: record `deps` (spec SHA, script SHA, each certifier record resolved by S3-3 with path and SHA) plus a `--stale` branch with a B per dependency kind. S1 r8 and S2 r9 are exempt by record name, the RPT pattern. S3 r7 is not exempt: it is re-recorded at ORCH-A, since it is the case G5 exists for. P0L checks the premise against S3-3's certifier semantics |
| F4-3 | **The C1.3-a dry run covered two cases.** The 1.3 close measured rule (l) firing on the S1 r8 height_target leader (gridline, side view) and the part-edge form on S3 r6/r7 (fires on r6, clean on r7, measured by the reviewer). Nobody has run part edges in side and plan views (S1, S2), or the global form on S2 r9. G2 sets the class: reference lines, gridlines and part edges in side, plan and section views. Any accepted sketch that fires opens a revision | 1.3 close C1.3-a (1), (2); Design Notes 25 C1.3-a | **P0 R4** lands rule (l) for the whole class, with a Z and a B per line family and view, and dry-runs S1 r8, S2 r9 and S3 r7. Every firing goes into the P6 revision batch with S1 r9 (G3: one revision per sketch). A sketch other than S1 that fires is reported at STOP S4-A |
| F4-4 | **The S4-b holder section reaches S3 as well as S1, and X1 cannot see the difference.** The `holder` row is in `s1_spec.yaml` and `s3_spec.yaml` (MEASURED), both drawn as the stand-in section. X1 compares only `place`, `z_rule` and `plan_poly` (MEASURED, --stale output). A true holder section in S4 and a stand-in in S1 and S3 would pass X1 under the same row id. G3 approved one S1 r9. Under G2 the holder section is one class, every view that draws it | MEASURED; Design Notes 25 S4-b; s1_spec.yaml l.37 stand-in note | **STOP S4-A item 5**: (A) S1 r9 and S3 r8 both draw the holder from `build_parts/holder.py`, and X1 gains the `section` field (plus `depth` and `bore_cone`) with a Z and a B; (B) S1 r9 only, with S3 keeping the stand-in and a named note. Recommendation A |
| F4-5 | **S4-a meets X1.** The spigot below the plate top (z_A 0 to 12) cannot join the shared `receiver` row: z_rule z_min = plate top is shared with S1 and S3 (Designer receiver-shoulder file l.193). `base_plate` is shared by S1, S2 and S3 and is drawn without its hole | `step1.3_designer_receiver_shoulder.md` l.20, l.193; X1 output | P1 (a) proposes the row split: a new S4-only row `receiver_spigot`, plus the hole break as an S4-only row or field so the shared `base_plate` stays equal. P2 (b) writes it, P3b signs |
| F4-6 | **Q10: a 100 mm core on the core stop cannot be cut.** Core stop 42.50 z_A (overlay `collet.core_stop_z`), so the core top sits at 142.50, which is 17.34 below the collar top 159.84 (`stop.collar_top_z`). `core.min_exposed` 143.12 includes `collar.top_above_plate` 6.75, so its datum reads as the nut-plate top, 153.09 z_A. Exposure then needs core top >= 296.21, or at least 253.71 of core on the stop (260.46 if the datum is the collar top). The 100 mm core is short by at least 153.71. No kept collet length on its own changes this (a taller collet raises the collar top with it) | DERIVED from params `core.min_exposed`, `stop.collar_top_z`, `collar.top_above_plate`, overlay `collet.core_stop_z` | P1 (a) fixes the min_exposed datum and states which advance option exposes a 100 mm core. Reported through RPT (core top against collar top, minimum core length on the stop). The answer goes to Q10 at M2 |
| F4-7 | **S4-2 is red by construction, and detail 1.4 assumes a push from below.** The kept receiver has a floor (S4-2 B is "the receiver as built"). That floor is the collet foot seat for core weight (ASSEMBLY.md l.41, l.110), part of the clamp loop (l.103), and a link in the accepted S3-3 cut-case chain (core, collet core stop, collet, receiver). A floor opening changes a kept part (Start here: receiver kept; Quinn's design), reroutes S3-3 and touches N5 and B2-10. Advance options that leave the floor alone (spacer pucks under the core in the collet bore; lift-out and re-seat on a spacer stack) change what S4-2 tests | MEASURED (gameplan S4-2 row; ASSEMBLY.md; S3-3 chain in s3_checks_r7) | P1 (a) states the options with cost: kept-part change, S3-3 effect, operator steps per slice. **STOP S4-A item 2** rules the drawn option and the S4-2 form. P4 implements the ruled form, and a floor change goes to Quinn in a batch 3 row |
| F4-8 | **Q5 back-edge.** A taller collet moves `stop.collar_top_z`, and with it `stop.height_z`, all four S1 poses, the S3 capture_end pose and the S2 hand-band heights. It also moves the zero-margin identities (S1-4 0.84, drill_head\|collar 25.000; T2-e). Adopting a collet length reopens S1, S2 and S3 | 1.3 close S4-Q4; Design Notes 25 T2-e | **STOP S4-A item 3**: draw the taller collet as an alternate outline with the keys unchanged (recommended), or adopt a value and open the three revisions. Q5 is owned by Quinn and Sean, so it goes in a batch 3 row |
| F4-9 | **Section plane.** `SECTION_VIEWS = ("section_yz",)` (sketch_common.py l.45). The section convention, look sign, `section_u` K7, hatch_split and rule (l) run only there. The kept parts are round except for the wing-nut wings (span 230), the holder key (3.0 high, 40 long), the 12 collet slits and the receiver-shoulder bolts at 30, 150, 210 and 330 deg (DN32). In the x = 0 plane those bolts sit at x +-77.94, off the band, as in S3 | MEASURED | P1 (a) sets the plane and look direction. Recommendation: section_yz (x = 0, viewed from +X, u = +Y), which reuses the signed S3 machinery. If section_xz is chosen, P4 generalises SECTION_VIEWS with a Z and a B per rule, signed at P5T and P5L (1.3 close S4-Q1). **STOP S4-A item 1** |
| F4-10 | **Roster: detail 1.4 and Design Notes 8 are out of date.** Detail 1.4 says "Cross-review: none required (no new placement computed)". Design Notes 8 says "S4 and S5 compute no new placement". S4 now computes section placement (holder section from holder.py, a 0.20 radial spigot gap, the plate-hole break, the advance-path sweep, possibly a new plane). It changes K7 classes in S1 (receiver\|holder G 0.25, collar\|holder C), and the 1.3 close sends S1 r9's changed rows to (e). A.4 step 2's geometry cross-review rule applies | gameplan l.320, l.557; close S4-Q2 | **STOP S4-0** (asked at open; blocking only for P3b onward): add The Loftsman and The Topologist at (b), (c) and (e), and The Software Engineer at step 0 and (c). Precedent: Design Notes 18 |
| F4-11 | **Controls runtime (G4).** 229.0 s at 413 controls, about 0.55 s per control at 12 jobs plus about 15 s spread. S4 at about 60 more controls projects to about 260 s. The results record no per-control time, so a pruning case has nothing to stand on | MEASURED (close 1.1, 4.2); DERIVED projection | **P0 R1**: a per-control time field, a slowest-30 profile, a fast tier for (d) iterations, and pruning candidates with evidence (no deletion before P0S rules). Full-set target 200 s restated |
| F4-12 | **C1.3-c correction: `ring.nut_mounting` is in no record's `keys_read`.** S1 r8 reads 126 keys, S2 r9 132, S3 r7 232; none is `ring.nut_mounting` (MEASURED). The close's line "S3 reads the key, so the fix runs under (i)" does not hold. The text fix leaves `--stale` clean and needs no refreshed record for that reason. The s3_spec `status` text and W comment are spec edits, which the F4-2 spec SHA will see | MEASURED | P0 R6 makes all three text fixes before R2 records spec hashes, so the S3 r7 refresh at ORCH-A carries them |
| F4-13 | **C1.3-b mixes harness items and notes.** R2-6 (not_drawn literal x bands, out of `--stale` reach) is a member of the F4-2 class. R2-7 (arc a1 branch with no B) and DR4-2 (terminator relief covers position, not head width or connection style) are branches with no B. Rule (j) holds only the first number of a stall literal (282.21 unheld). LF1.3-11 is spec source text. TP1.3-4 to -7, -9, -16 to -18 and -20 are notes. LF1.3-12 goes to Step 2 | Design Notes 25 C1.3-b, TP1.3 rows | P0 R5: each item implemented with a Z and a B, or given a stated disposition. Raisers re-check at P0T, P0D and P0L |
| F4-14 | **Ticks carried to S4 (Sean, "Carry all"): collet slit and receiver thread.** The harness admits `<row>:ticks` only on gear rows in plan (K5 1.2 (h)) and screw root lines in section (TP1.3-15). Collet slits and a receiver thread in a section view have no admission rule | Design Notes 13 S3-r7; K5 row | P1 (a) shape notes name them. P4 (c) adds a general section-view tick admission rule scoped to its class (any row with a declared tick form), with a Z and a B per branch, signed at P5T |
| F4-15 | **The S1 r9 batch must cover every revision trigger at once.** Triggers: C1.3-a (1) firing on height_target; S4-b holder rows and the retired stand-in note; X1 `section` if ruled; any further rule (l) firing in S1 from F4-3. S1 r9 opens once, at P6, after (c). A second S1 revision inside 1.4 counts as a process defect | 1.3 close S4-Q2, G3 | P6 draws S1 r9 with every trigger. P7a and P7b review S1 r9's changed rows. The P8 fresh M1 gates S1 r9 with S4 |
| F4-16 | **Superseding S1 r8 makes S3 r7 stale under the new branch.** That is the B condition of F4-2 happening for real. After `--accept s1 --rev 9`, S3 r7 must re-run (S3-3 on the S1 r9 K7 entries) and be re-recorded, or open S3 r8 if its pixels change. The holder sits outside the S3-3 cut-case route (TP1.3-10 (a)), so no link should move. P6 dry-runs this in a scratch copy | close S4-Q3, G5 | P6 runs the scratch-copy dry run. ORCH-B order: accept S4 and S1 r9, then `--stale` (S3 red, the expected branch), then the s3 re-run and refreshed accept, then `--stale` clean |

## 1. Scope, done criteria, sequence

### 1.1 Scope (gameplan detail 1.4)

Question S4 answers: how does the core move up through the collet (push-pop), and does the kept collet family cover a 100 mm tall core? The figure is one section through the base: collet, holder, wing nut, receiver (with the DN32 shoulder and the S4-a spigot), PTFE washer, core stop, the advance path, the taller-collet option, the sacrificial collet or liner option, and a 100 x 100 mm core. It closes R10, R11, R12 and Q4, Q5, Q6, Q10. Checks: K1 to K9, X1, RPT, S4-1 to S4-3 (S4-2 in the form STOP S4-A rules).

Carried in (G2 to G5 land at step 0; Design Notes 25 S4-a to S4-d, C1.3-a, C1.3-b, C1.3-c; Sean "Carry all" ticks):

| Carried item | Lands at | Owner; signs |
|---|---|---|
| G4 controls profile, fast tier, pruning (F4-11) | P0 R1 | The Engineer; The Software Engineer rules pruning (P0S) |
| G5 record dependencies: certifier records, spec, script; `--stale` branch (F4-2) | P0 R2; S3 r7 re-recorded at ORCH-A | The Engineer; The Loftsman (P0L), The Software Engineer (P0S) |
| G2 control blinding, re-lettered per round, key out of tree (F4-1) | P0 R3; used at every P8 | The Engineer; The Software Engineer (P0S); the orchestrator holds the key |
| G2 rule scope by class; G3 rule (l) global scope and part-edge extension (C1.3-a, F4-3) | P0 R4; firings to P6 | The Engineer; The Designer signs (P0D) |
| C1.3-b harness items and notes (F4-13) | P0 R5 | The Engineer; raisers re-check (P0T, P0D, P0L) |
| C1.3-c text defects (F4-12) | P0 R6 | The Engineer |
| S4-a spigot and plate-hole break (F4-5) | P1 (a); P2 (b) | The Designer proposes; The Engineer; The Loftsman signs |
| S4-b holder section from holder.py; S1 r9 (and S3 r8 if ruled) (F4-4, F4-15) | P1 (a) values; STOP S4-A; P2 (b) spec edits; P6 draw | The Designer; The Engineer; The Loftsman and The Topologist at (e) |
| S4-c fit values per C pair (base stack) | P1 (a) | The Designer |
| S4-d optional predicate, collet bore edge vertical | P1 decides; P4 if adopted | The Designer; The Engineer; The Topologist (P5T) |
| Ticks: collet slit, receiver thread (F4-14) | P1 shape notes; P4 admission rule | The Designer; The Engineer; The Topologist (P5T) |
| Section plane (F4-9) | P1; STOP S4-A; P4 if section_xz | The Designer; The Engineer; P5T, P5L |
| X1 `section` field (F4-4) | P4 if ruled | The Engineer; The Software Engineer (P5) |

Rulings in force: Design Notes 21 to 32 and the Step 1.3 gate G1 to G6 (Progress Log, 2026-11-27). Accepted state: S1 r8, S2 r9, S3 r7 in `docs/sketches/` (`--stale` 3 records, 0 differences, MEASURED at this open). Batch 2 (B2-1 to B2-10) stays with Quinn, unanswered; every stand-in stays ASSUMED.

### 1.2 Revisions of S1, S2, S3 inside 1.4

S1 r9 opens once, at P6 (F4-15). S2 r10 and S3 r8 open only if the P0 dry run fires on them (F4-3), if Sean rules item 5 A (F4-4, S3), or if Sean adopts at STOP S4-A or M2 a value for any key in their accepted `keys_read`.

| Stage | Who | Rule |
|---|---|---|
| Rule landing | The Engineer at P0 | A firing on an accepted record is reported with its cause. The drawing and the check stay unedited; the firing goes to P6 |
| Spec edit | The Engineer at P2 | S1 (and S3) holder rows and neighbour classes per STOP S4-A, edited in the same save point as s4_spec |
| Redraw | The Engineer at P6 | To `docs/sketches/wip/`. Every check green, plus the deps record. Script edits only where an expression or a label anchor must change |
| Cross-review | The Loftsman and The Topologist | Changed rows only, with hand values beside the JSON values (P7a, P7b) |
| M1 | The same fresh Designer spawn as S4 (P8) | Separate files `wip/s1_visual_gate_r9.md` (and S2/S3 equivalents); S1 V1 to V10, S2 V2 and V6 to V10, S3 V1 and V5 to V10 |
| M2 | Sean, same stop as S4 | Old and new PNGs side by side, with the changed items listed |
| Record | Orchestrator | `--accept` supersedes the earlier record; S3 re-run per F4-16 |

### 1.3 Done criteria (Step 1.4 closes when all hold)

| # | Criterion | Evidence |
|---|---|---|
| DC1 | G4: per-control time in the controls results; slowest-30 profile; fast tier (every check family has its Z and at least one B), never read by `control_tally` or `--accept`; pruning ruled by The Software Engineer, every deleted control named with its reason; full-set wall MEASURED against 200 s at the default jobs; Software Engineer PASS | P0, P0S, P0f |
| DC2 | G5 and its class: record `deps` (spec SHA, script SHA, certifier records with path and SHA); `--stale` branch with one B per dependency kind, each red on the pre-change code; legacy exemption by record name (s1 r8, s2 r9 only); S3 r7 re-recorded with deps at ORCH-A; Loftsman and Software Engineer PASS | P0, P0L, P0S; ORCH-A log |
| DC3 | G2 blinding: `--m1-controls` with fresh random tokens per round, four PNGs alone in the reviewer folder, key outside the project tree (refused inside it), no reviewer figures from `--controls`; Z and B; Software Engineer PASS; no reviewer prompt and no file a reviewer reads states an expected control outcome | P0, P0S; section 5 log |
| DC4 | G2 rule scope and G3: K4 rule (l) over reference lines, gridlines and part edges in side, plan and section views, a Z and a B per line family and view, each B red-first; Designer signs; dry-run firing list on S1 r8, S2 r9, S3 r7; every firing closed in this step's revisions | P0, P0D; P6 |
| DC5 | C1.3-b and C1.3-c: each item implemented with a Z and a B, or dispositioned with a reason; raisers re-check | P0, P0T, P0D, P0L |
| DC6 | (a) params review: plane and look direction; shape notes from build_parts for every kept part; S4-a row split; S4-b holder values; S4-c fit values; S4-d decision; advance options (Q4), collet length (Q5) and sacrificial collet or liner (Q6), each with cost; Q10 arithmetic with the min_exposed datum; S4 operator rows; ticks; X1 plan; STOP S4-A rulings recorded as a Design Note | P1; Design Note (section 6 item 9) |
| DC7 | (b) `s4_spec.yaml` signed by The Designer (part list) and The Loftsman; `reported_items`; S1 (and S3) holder spec edits per ruling; X1 equal on shared rows | P2, P3a, P3b |
| DC8 | (c) S4-1 to S4-3 in the ruled form; S4-x fixtures; tick admission rule; section_xz generalisation and X1 `section` if ruled; `--controls` green; `s4 --rev 0` red by cause; `--baseline s4`; Software Engineer, Topologist and Loftsman PASS | P4, P5, P5T, P5L |
| DC9 | (d) `docs/sketches/s4_base_section.py`; K1 to K9, X1, RPT, S4-1 to S4-3 green on the accepted revision; drawn through the section convention and the placer | `wip/s4_checks_r<k>.json`, then `docs/sketches/` |
| DC10 | (e) Loftsman and Topologist PASS with hand values on S4 (collar top 159.84 by the test_P18 formula, spigot radial gap 0.20, holder section coordinates, advance-path clearance, minimum core length on the stop, collet taper sense, nut over washer over holder, receiver floor at the bottom) and on the changed rows of S1 r9 (and S2/S3 if revised) | P7a, P7b |
| DC11 | (f) fresh image-capable M1 PASS on the exact pixels Sean accepts, for S4 and every S1/S2/S3 revision accepted in 1.4; blinded controls scored by the orchestrator from the out-of-tree key, fresh tokens each round | `wip/s4_visual_gate_r<k>.md` and equivalents; section 5 |
| DC12 | (g) Design Notes 13 rows with Sean's words; picks recorded; `--accept` copy-up equal; S3 re-run after `--accept s1 --rev 9` (F4-16); `--stale` 4 records, 0 differences, deps branch included | Design Notes 13; ORCH-B log |
| DC13 | Reported (never asserted), each a row of `s4_summary_r<k>.md` through RPT: 100 mm core top against the collar top and its exposure against `core.min_exposed`; minimum core length on the stop; advance per slice and slices per core for the drawn option; collet length options with the collar-top move and the S1 height deltas; sacrificial collet or liner; the cut-case seat drawn (collet foot on the receiver floor, receiver shoulder on the plate) | `s4_summary_r<k>.md` |
| DC14 | Records: gameplan lines applied at the save point after each agent, in the numbered Old/New format; one Progress row per agent return (fresh M1 returns included); every unmatched Old rewritten or marked superseded at the same save point; Manager close audits them and writes the accumulator entries | P10 |
| DC15 | Scratch: no file from this step on C: (C: free MEASURED at open, 6.22 GB, and at close) | P10 |

### 1.4 Sequence

STOP marks the orchestrator halting for Sean. Background is **required** for every Engineer spawn, for any spawn that runs `--controls` (about 229 s and up) and for any process over 30 s; it is recommended elsewhere. One Engineer spawn runs at a time (shared tree). Reviews in one row run in parallel and read only; none edits `docs/sketches/`.

| # | Sub-step | Who | Mode | Runs after | Background |
|---|---|---|---|---|---|
| **STOP S4-0** | Roster (F4-10) | Sean | human; asked at open, blocking only for P3b onward | open | — |
| P0 | Step 0: G4 profile and fast tier, G5 deps and `--stale` branch, G2 blinded controls, rule (l) class scope with dry run, C1.3-b, C1.3-c, record re-runs | The Engineer | agent, **parallel with P1** | open | **required** |
| P1 | (a) params review for S4 | The Designer (spawn A) | agent, **parallel with P0**, then with the P0 reviews | open | recommended |
| P0S, P0D, P0T, P0L | step 0 checks | The Software Engineer; The Designer (spawn B, not P1, never the M1 reviewer); The Topologist; The Loftsman | agents, **all four parallel** | P0 | P0S **required** (runs controls); others recommended |
| P0f | fix pass on step 0 FIXes | The Engineer | agent | P0 reviews | **required** |
| P0r | raiser re-checks (raisers with a FIX only) | raisers | agents, parallel | P0f | recommended |
| ORCH-A | re-accept the S3 r7 refreshed record (and s1 r8, s2 r9 if green and pixel-equal); `--stale` with the deps branch; `--m1-controls` trial with key outside the tree; gameplan lines; save point 1 | orchestrator | run, edit, git | P0 reviews PASS | — |
| **STOP S4-A** | (a) rulings: plane, advance option and S4-2 form, collet length, sacrificial option, holder scope and X1 `section`, values moving S1/S2/S3 keys, dry-run firings, batch 3 | Sean | human, blocking for P2 | P1 and ORCH-A | — |
| — | Design Notes entries (S4-0, S4-A); gameplan lines; save point 2 | orchestrator | edit, git | S4-A ruled | — |
| P2 | (b) overlay values, `s4_spec.yaml`, `checks_s4.py` skeleton, S1 (and S3) holder spec edits | The Engineer | agent | save point 2 | **required** |
| P3a, P3b | (b) spec sign-offs | The Designer (spawn A); The Loftsman | agents, **parallel** | P2 | recommended |
| P2f, P2r | (b) fix pass; re-sign by raiser | The Engineer; raiser | agents | P3 | **required** for P2f |
| — | gameplan lines; save point 3 (spec signed) | orchestrator | edit, git | P3 SIGNED | — |
| P4 | (c) S4-x fixtures, S4-2 ruled form, tick admission, section_xz and X1 `section` if ruled, stub, `s4 --rev 0`, `--baseline s4` | The Engineer | agent | save point 3 | **required** |
| P5, P5T, P5L | (c) checks | The Software Engineer; The Topologist; The Loftsman | agents, **all three parallel** | P4 | P5 **required**; others recommended |
| P5f, P5r | fix pass; raiser re-checks | The Engineer; raisers | agents | P5 reviews | **required** for P5f |
| — | gameplan lines; save point 4 | orchestrator | edit, git | P5 reviews PASS | — |
| P6 | (d) draw S4 r1; S1 r9 with every trigger; S2 r10 / S3 r8 if triggered; S3-3 dry run on the S1 r9 record in a scratch copy | The Engineer | agent | save point 4 | **required** |
| **STOP-T5** | first `wip/s4_*_r1.png` and `wip/s1_*_r9.png`: orientation preview | Sean | human, non-blocking | PNG mtime | — |
| ORCH-M1 | generate blinded controls for round r1 (section 5) | orchestrator | run | P6 | — |
| P7a, P7b, P8 | (e) cross-review and (f) fresh M1 on r1 (S4; S1 r9; S2/S3 if revised), **all three parallel** | The Loftsman; The Topologist; The Designer (fresh spawn C, image-capable) | agents | P6, ORCH-M1 | recommended |
| ORCH-S | score the controls against the key (section 5) | orchestrator | read | P8 | — |
| P9 | (h) one revision from (e), M1 and T5 together | The Engineer | agent | P7a, P7b, P8, T5 | **required** |
| P7r, P8r | raiser re-checks; then a fresh M1 on the new revision with a new control round | raisers; The Designer (fresh) | agents | P9 | recommended |
| — | gameplan lines; save point 5 (pre-M2) | orchestrator | edit, git | M1 PASS on the exact pixels | — |
| **STOP M2** | correction pass and picks | Sean | human, blocking | save point 5 | — |
| ORCH-B | accept S4 and S1 r9 (and S2/S3); `--stale` (S3 red expected); s3 re-run and refreshed accept; `--stale` clean; save point 6 | orchestrator | run, git | acceptance | — |
| P10 | Manager close | The Manager | agent | ORCH-B | **required** |

**Loop caps (per review).** Step 0 reviews: one fix pass (P0f) and one raiser re-check (P0r). Spec: one fix pass (P2f) and one re-sign (P2r). Red-first: one fix pass (P5f) and one re-check (P5r). Drawn revisions: r1 gets (e) and M1 in parallel. From r2 on, P7r then a fresh P8r. At most three fresh M1 rounds (r1 to r3) before M2. A FIX that names a value, field setting or coordinate carries a harness dry run, and a FIX that fails its dry run goes back to the raiser and opens no revision (detail 1 common (h)).

**A.4 ruling path when a class repeats.** When a re-check or a fresh M1 finds the same class of finding as the round before (same check family, same line family, same convention clause), the orchestrator stops the loop and does not open another revision on it:
1. Name the class in the Progress Log, with the two findings.
2. Ask the scope question: does the rule covering it reach the whole class in every view the harness draws (detail 1 common, Rule scope)? If not, rule a class-wide rule: one Engineer pass with a Z and a B per branch, signed by the raiser, applied to every accepted sketch in the same revision.
3. If the class repeats after a class-wide rule, rule flat: record the ruling as a Design Note, assign the residue to a named specialist and step, and take the sketch to M2 with the residue listed for Sean.
4. Two rounds of disagreement between paired reviewers that repeat positions (A.9) get the same treatment: present both side by side, then rule.

**T5 rule:** the orchestrator polls `docs/sketches/wip/s4_*_r1.png` and `wip/s1_*_r9.png` mtimes while P6 runs. Sean's words go to Design Notes 13 as `S4-r1` (and `S1-r9`) and into P9.

**Reviewer independence:** every M1 spawn (P8, P8r) is a fresh Designer spawn that drew nothing, signed no rule or spec in this step (not spawn A of P1/P3a, not spawn B of P0D), and was not an M1 reviewer earlier in 1.4. It gets [BLOCK DES-M1], never [BLOCK DES]. Its packet holds no key, no gate file from an earlier round and no line range of this file or the gameplan.

## 2. Stops for Sean

| Stop | When | Sean sees | Sean answers | Orchestrator then |
|---|---|---|---|---|
| **STOP S4-0** (blocking for P3b, P5T, P5L, P7a, P7b; not for P0, P1, step 0 reviews) | At open, with P0 and P1 spawned | The question below | One option | Design Note per section 6 item 8; conditional edits in section 6 items 6 and 7; Progress row |
| **STOP S4-A** (blocking for P2) | After P1 and ORCH-A | From P1 section "Decisions for Sean" and P0: (1) section plane and look direction; (2) advance option drawn (Q4) and the S4-2 form; (3) collet length (Q5): alternate outline with keys unchanged, or a value that reopens S1, S2, S3; (4) sacrificial collet or liner (Q6), option drawn; (5) holder section scope (S1 r9 and S3 r8, or S1 only) and X1 `section`; (6) every (a) value that moves a key S1 r8, S2 r9 or S3 r7 reads, with the rows that move; (7) the P0 rule (l) dry-run firings and the revisions they open; (8) batch 3 draft (receiver floor if option A, collet length, sacrificial collet), send or hold; (9) S4-c fit values and the S4-d decision (Designer proposes) | A pick per item, or corrections; deferred items go to M2 with P1's recommendation drawn | Design Note "Step 1.4 STOP S4-A rulings" with Sean's words (section 6 item 9); Progress row; hand to P2 |
| **STOP-T5** (non-blocking) | First `wip/s4_*_r1.png` during P6 | S4 PNG; S1 r9 PNGs | V1 (floor at the bottom), V3 (collet narrow end and taper sense, wing nut above the holder), V4 (core upright on the stop); for S1 r9, V1 to V5 | Design Notes 13 `S4-r1`, `S1-r9`; into P9 |
| **STOP M2** (blocking) | After M1 PASS on the exact pixels and save point 5 | S4 PNG, `wip/s4_visual_gate_r<k>.md`, `wip/s4_summary_r<k>.md`; S1 r9 beside `s1_pose_*_r8.png` with changed items and its gate file; S2/S3 if revised | V1, V3, V4, V9 yes/no for S4 (V1 to V5, V9 for S1 r9); free corrections; picks: advance option, collet length, sacrificial collet or liner, any deferred S4-A item; answers to Q4, Q5 (with Quinn), Q6, Q10; acceptance of each sketch | Design Notes 13 rows; picks in the S4-A Design Note; Open Questions Q4, Q5, Q6, Q10; ORCH-B |
| Decision mid-step (only if raised) | P2 or P4 finds a check red by construction on the ruled values, or a sign-off rules an S1/S2/S3 spec change beyond the ruled holder rows | the conflict and the raiser's options | a pick | addendum to the S4-A Design Note |

**STOP S4-0 question (exact text for Sean):**

> Detail 1.4 and Design Notes 8 say S4 computes no new placement, so S4 has no geometry cross-review. S4 now draws the holder section from build_parts/holder.py, the receiver spigot in the plate hole (0.20 radial against 0.10), the plate-hole break and the core advance path, possibly on a new section plane. It also changes S1's holder classes (receiver|holder G 0.25, collar|holder C), which opens S1 r9. Who reviews S4?
> - **A. Add The Loftsman and The Topologist** at (b) spec sign-off (Loftsman), (c) red-first (both) and (e) cross-review of S4 r1 and S1 r9's changed rows (both), and The Software Engineer at step 0 and (c). Design Notes 8 and detail 1.4 are amended.
> - **B. The Topologist only**, at (c) and (e) (kept-part orientation predicates and section sense), with The Software Engineer at step 0 and (c). S1 r9's changed rows still get the Loftsman at (e), per the 1.3 close.
> - **C. As written** (The Designer only). S1 r9's changed rows go to (e) per the 1.3 close; S4's own placement goes unreviewed.
>
> Recommendation: **A.** The A.4 step 2 geometry cross-review rule applies to placement composition, and the receiver spigot and holder section are where 1.1 (TP1.1-3, holder|collet 626.24 mm² behind class N) and 1.3 (P5L F1, receiver seated on nothing) found their base-stack defects.

## 3. Spawn prompts

Each prompt below is pasted by the orchestrator as written. The placeholders [BLOCK x] and [CTX COMMON] are replaced verbatim with the section 3.0 texts. Text in [orchestrator: ...] is replaced by the orchestrator before spawning. No prompt asks an agent to read a line range of this file. Paths are relative to the project root.

### 3.0 Persona blocks and common context

**[BLOCK DES] The Designer** (P0D, P1, P3a; never an M1 spawn)
```
SYSTEM: You are The Designer, design critic for physical products and technical documents.
Biographical anchors: Author of The Design of Everyday Things (1988), founding director of the Design Lab at UC San Diego, VP of Apple's Advanced Technology Group. He spent decades studying why well-intentioned designs fail and what makes the difference between a product people tolerate and one they love. His framework (affordances, signifiers, constraints, mappings, feedback, and conceptual models) applies to everything from door handles to technical documents to 3D-printed RC cars.
Your characteristic approach: For physical products, evaluate: Does the design communicate its intent? Would the user understand what to do without being told? Does the product look like something its creator is proud of? Are error-prone operations designed out or designed to be recoverable? In CAD/PLM work your review extends to the params level: a parameter set that describes a functional part as a dimensionally correct but geometrically non-representative placeholder is a design failure you catch before geometry exists. Your visual gates run only on an image-capable model.
Your role on this team: params review (LLM-PLM 8.4a), representative-shape notes (8.4b), spec sign-off with the shape-text part list, operator-task table, sign-off of label and leader rules; co-owner, with The Topologist, of the renderer and leader placer conventions. At 1.4 (S4): the base-stack params review, the S4 spec sign-off and the step 0 sign-off of the K4 rule (l) class extension. The M1 visual gate is a separate fresh spawn. The Engineer draws; you did not produce the images you review (gameplan Design Notes 3).

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0, Wave 2): Review found 0 BLOCKS, 10 FIX, 5 NOTE, with a 12-item Manager close checklist (all items met at close). All accepted and applied except the D3 sub-item (premise wrong). Notable accepted fixes: governing line over the superseded "Start here" lines (D1), drill drawn with distinct head and top-end block, cutter OD ASSUMED and 152.4 labelled as tube OD (D4), S1-5 split into core-to-bore-ceiling and ring-to-base checks (D5), pose table (D6), `ring.*` seeded with functional features (D7), power-off hold and hard-stop rows (D8), operator-task table and rubric V10, captured-core removal owned (D9), S4 orientation predicates for kept parts (D10), Echo Site Registry rows (D12). Correction received: D3 misread the INSITU2 range. Positions that remain relevant: Designer owns params review, representative-shape notes, spec sign-off and the M1 visual gate on an image-capable model at every sketch; a functional part seeded as an outline fails the params review.
- Cycle 1.1 (Step 1.1, S1): P1 params review set the G3 values (ring 130 above the tip, anchors 265, allowances 30/30/30, L 900 under option R), confirmed G4 (core stop 42.5), flipped both TP-2 taper senses, wrote the pose table, shape notes, S1-7 row, TP-9 wording and operator rows; Sean adopted option R and the values (Design Notes 22, 23). P3a sign-off: 6 FIX (standoff overhang, lug width, base-plate nests replaced by members on the plate top, pad radius 200, rod text, pinion support), all closed; SIGNED. NOTES N1 to N6 carried (keep-out pair, theta 270 member overhang 26, bushing length, Design Notes 1 against the bearing, tilt margin, NEMA 23 in every sector). M1 at r2 as a fresh image-capable reviewer: controls scored correctly (ctrl_a FAIL V3, ctrl_b PASS); S1 FAIL with F1 to F7; F1 to F5 fixed in r3; F6 (ring rim hides the end of the cut) assigned to Step 2 and S2 and accepted by Sean; r3 and r4 PASS except F6. Corrections received: his (a) review listed the 1 m start at 917.5, inside the uncut core (Loftsman FIX 5); r2 F1 (a) called the shaft-pinion N pair already declared (self-corrected at r3); his (b) sign-off passed shape text naming bracket arms, a pad support and shafts that had no rows, which his M1 then failed. Positions that remain relevant: (b) sign-off now carries a shape-text part list (detail 1 common (b)); projected_extent is containment only, so M1 checks parts drawn narrower than their footprints; bracket values are ASSUMED until Step 2.
- Cycle 1.2 (Step 1.2, S2): params review (21 PASS, 7 FAIL with leaves): radius 274 (option A), O1-B split of S2-5, operator sector theta 90 +- 45, guide tie, LM20UU housing; Sean accepted all but the three-pad proposal (one pad kept). Spec sign-off FIX 4 then SIGNED with a 41-row part list. Fresh M1 spawns: S2 r1 FAIL F1 to F5, S2 r2 FAIL F1 (leaders under the gear fill), S2 r3 PASS; S1 r5 FAIL F1 (note clipped), S1 r6 FAIL F1 (core-750 leader under hatch, present in accepted r4), S1 r7 PASS; reviewer controls scored correctly every time. Signed the r2 to r4 rules. Corrections received: tick toe 95.22 ruled against (Design Notes 29, pitch point 96.54); D4-1 premise wrong (anchor 3.1 mm outside tie b, proposed anchor inside the bracket outline, 150 leader fails the hatch rule; Design Notes 30). Positions that remain relevant: a FIX that sets a coordinate needs a harness dry-run before it is issued; the ring rim under unfilled guide arms goes to the S3 hidden-line renderer, co-owned with the Topologist.
- Cycle 1.3 (Step 1.3, S3): (a) params review recommended Tr12x3 over T8x8 (S3-2 1.02 at stall, WOB 874 N under the 1000 N cut), corrected K for a top-guided floating nut (0.7 or 1.0, never 2), set section A-A (x = 0, from +X, u = +Y, capture_end); Sean adopted all (Design Notes 31). P1Rd renderer conventions FIX 3 plus D4, D5, signed. (b) sign-off FIX 6 and re-sign FIX A to D (nut on three shoulder screws, adopted by orchestrator ruling). Receiver shoulder values (proposed OD 180; Sean chose OD 200 with 4 x M5, Design Notes 32). r2 values: span offset u -225 overruled to u -110 (both ends in the arm sections); hatch alternate '////' refused by the line-family lint, '--' objected to by himself, ruled '||'. Fresh M1 spawns: S1 r8 PASS, S2 r9 PASS, S3 r1 FAIL F1 to F7, r3 FAIL V8, r4 FAIL F1, r5 FAIL with both rules refused, r6 FAIL V8 (F1, F2 leaders along part edges) with dry-run fixes Sean applied as r7; signed the r6 rules. Control figures scored 4/4 at every gate, credit void: the P8 prompt section printed the key. Positions that remain relevant: part-edge collinearity (N1) and the stall-literal hold (rule j NOTE) to S4 step 0; tick marks named in five S3 shape strings are not drawn (N2, to S6).
```

**[BLOCK DES-M1] The Designer, M1 reviewer** (P8, P8r only; the orchestrator pastes this block and never [BLOCK DES] into an M1 spawn)
```
SYSTEM: You are The Designer, design critic for physical products and technical documents, acting as the M1 visual-gate reviewer.
Biographical anchors: Author of The Design of Everyday Things (1988), founding director of the Design Lab at UC San Diego, VP of Apple's Advanced Technology Group. He spent decades studying why well-intentioned designs fail and what makes the difference between a product people tolerate and one they love. His framework (affordances, signifiers, constraints, mappings, feedback, and conceptual models) applies to everything from door handles to technical documents to 3D-printed RC cars.
Your characteristic approach: Does the design communicate its intent? Would the user understand what to do without being told? Does the figure build the right mental model in a cognizant reader? You judge the pixels in front of you, item by item, and say what you see.
Your role on this team: the M1 visual gate (LLM-PLM 8.4c) on an image-capable model. You did not produce, sign or review these images or their rules before this gate. The Engineer draws.

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0, Wave 2): Review found 0 BLOCKS, 10 FIX, 5 NOTE. Notable accepted fixes: drill drawn with distinct head and top-end block, cutter OD ASSUMED and 152.4 labelled as tube OD (D4), pose table (D6), `ring.*` seeded with functional features (D7), operator-task table and rubric V10 (D9), S4 orientation predicates for kept parts (D10). Positions that remain relevant: a functional part seeded as an outline is a design failure.
- Cycle 1.1 (Step 1.1, S1): M1 at r2 as a fresh image-capable reviewer: S1 FAIL with F1 to F7; F1 to F5 fixed in r3; F6 (ring rim hides the end of the cut) assigned to Step 2 and S2 and accepted by Sean; r3 and r4 PASS except F6. Correction received: his (b) sign-off passed shape text naming parts that had no rows, which his M1 then failed. Positions that remain relevant: projected_extent is containment only, so M1 checks parts drawn narrower than their footprints.
- Cycle 1.2 (Step 1.2, S2): Fresh M1 spawns: S2 r1 FAIL F1 to F5, S2 r2 FAIL F1 (leaders under the gear fill), S2 r3 PASS; S1 r5 FAIL F1 (note clipped), S1 r6 FAIL F1 (core-750 leader under hatch, present in accepted r4), S1 r7 PASS. Correction received: a coordinate FIX (D4-1) failed the harness; a FIX that sets a coordinate needs a harness dry-run before it is issued.
- Cycle 1.3 (Step 1.3, S3): Fresh M1 spawns: S1 r8 PASS, S2 r9 PASS, S3 r1 FAIL F1 to F7 (scale, labels, dimension, section convention), r3 FAIL V8, r4 FAIL F1 (compression label stale against the load cases), r5 FAIL (leader on a gridline, nut stations unlabelled), r6 FAIL V8 (F1, F2 leaders along part edges) with dry-run fixes Sean applied as r7. Positions that remain relevant: leaders that run along a gridline, reference line or part edge read as part of the drawing; tick marks named in shape strings and not drawn are a V7 item.
```

**[BLOCK ENG] The Engineer**
```
SYSTEM: You are The Engineer, the team's jack-of-all-trades engineer with a bias toward action.
Biographical anchors: JPL Chief Engineer for the Curiosity and Perseverance Entry, Descent, and Landing systems. Author of The Right Kind of Crazy (2016). Led the team that invented the sky crane, the system that lowered a car-sized rover to the Martian surface on cables from a hovering rocket platform, a concept dismissed as insane until the team proved it worked. Twice. His career spans mechanical engineering, electrical engineering, systems integration, and project leadership. He does not specialize; he solves whatever the hardest problem is.
Your characteristic approach: "Test as you fly, fly as you test." Write the code, run it, verify the output, report results with evidence. Break impossible-seeming problems into testable pieces, test each piece, build confidence from evidence. Laconic; just the facts.
Your role on this team: you write all production code, run every check, and produce empirical evidence. On S4 you write the step 0 harness changes, the spec, the fixtures, the S4 script and S1 r9, and iterate to green. Design values go to Sean or The Designer; you never choose them in the harness.

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0): Drafted research/sean/gameplan.md from templates/gameplan.md (Objectives, Steps 1.0 to 7, step details, Context Recipes, Design Notes 1 to 13, Open Questions with N-rows). Accepted with modification: the Software Engineer rewrote Steps and details for TDD; Wave 2 raised 33 findings (SE 2 BLOCKS, 13 FIX, 3 NOTE; Designer 10 FIX, 5 NOTE). Revision applied all 33; rejected one sub-item (D3, sending an INSITU2 discrepancy to Quinn) with a correct reason. Ruled the seven Software Engineer vs Systems Engineer tensions (Design Notes 15, T1 to T7). Corrections received: drill drawn as a symmetric rectangle defeats orientation checks (D4); lift stroke conflated with travel (SE-3); drill-to-ring bearing and the axial loop through the kept base unowned (SE-1, SE-2); ring specified as an outline (D7). Positions that remain relevant: execution of shared-file changes waits for Quinn's review of the proposal (T4); one decision locus, sketch M2 decides and Step 2 consolidates (T3); Engineer draws sketches, Designer gates (DN3).
- Cycle 1.0 (Step 1.0): Wrote step3_check.py Q3-0 (red on empty, Z pass, B fire) and question batch 1 (17 rows incl. N10), approved by Sean as drafted and pushed. Wrote the sketch harness: sketch_loader.py split out so check_stack.py imports the loader only, sketch_common.py K1 to K9, check_stack.py (z_A evaluation, one conversion to z_S), check_sketch.py (--controls, --stale, --baseline), checks_s1.py, draft s1_spec.yaml, S1 stub, 41 controls. Wave 2 raised 3 BLOCK, 22 FIX, 21 NOTE; revision accepted all BLOCK and FIX, each with a new control (68 controls: Z 17, B 50, smoke 1); reproduced each defect against the Wave 1b code before claiming the fix. Corrections received: spec key `on:` parsed by YAML as True crashed K8 (SW-1); disjoint depth bands masked C and G failures (LF-1); artist transforms ignored, so a drawn part could sit anywhere (TP-1); B controls matched on exit code alone (SW-2). Edited gameplan l.140 outside his write scope (ratified at close). Positions that remain relevant: the draft overlay does not fit the lift (stroke 830.16 against travel 650; S1-4 red); the start pose is travel-defined in params, so "first contact" in the pose table contradicts `stop.start_z`; design values go to Sean or the Designer, never chosen in the harness.
- Cycle 1.1 (Step 1.1, S1): Wrote the S1 spec revision and overlay from the Designer's values (P2), the LF-16 lint, S1-7 and the R6 dispositions; fix pass on 11 sign-off FIXes (P2f: collar row, S1-4 band with g_min from the spec, pose-restricted K7 declarations, plan footprints containing their parts); 14 S1-x fixtures red-first (99 controls); `s1_side_poses.py` green on run 1 (r1); revisions r2 (cross-review), r3 (Designer M1 F1 to F5), r4 (re-checks); P10 move of 34 files to `docs/sketches/` with equal results. Ended at 117 controls (Z 35, B 81, smoke 1), S1 17/17, each new control run red against the pre-fix code first. Accepted by Sean as S1 r4. Corrections received: holder flange 8 mm low (LF1.1-1); gear taper predicate passed a falling face, "absent at park" unchecked, holder|collet interference hidden by class N (TP1.1-1 to -3); S1-4 band ignored g_min, so S1-4-B1 read clean on the pre-fix code (Loftsman FIX 2); shape-text parts undrawn and labels overlapping (Designer F1 to F5); plan-contact certified the spec and not the drawing, and the member footprint was the inscribed circle (TP1.1-11, -12, LF1.1-8); gear lower bound 15.43 was a projected separation, true 54.65 (Loftsman r3). At close: Sean's FIX 5 ruling (Design Notes 23, 1 m start-above-core term) is not in the accepted spec (Design Notes 25 H5). Positions that remain relevant: a relief rule needs its premise enforced by a check; `docs/sketches/` is the only working copy (H2); the accepted flag, `--baseline sN` and the output location are his 1.2 step 0 items (H1, H3, H4).
- Cycle 1.2 (Step 1.2, S2): step 0 harness (--accept, r0 record and --baseline sN, wip/ output rule, H5 park-rule text; found that Design Notes 23 holds exactly only for c <= 42.34, accepted by the Loftsman); S2 spec (70 rows, 47 shared with S1) and fix pass; plan-view harness rules and S2-x fixtures at (c) with every new B red-first on pre-change code; S2 r1 to r5 and S1 r5 to r7; controls 126 to 230. Every BLOCK and FIX closed; S1 r7 and S2 r5 accepted with no Sean corrections. Disproved the Designer's D4-1 fix by measurement (end-quarter hatch rule, anchor inside the bracket outline, 5 deg candidate scan), ruled closed with no geometry change (Design Notes 30). Corrections received: TP1.2-1 (radial outboard ran in side views), TP1.2-3 (S2-5b hand list), LF-c1 (pose-restricted pairs in the swept form), Software Engineer FIX 1 to 5. Positions that remain relevant: the hidden-line renderer for solid pieces under unfilled covers is the right fix and belongs at S3 (c); controls runtime needs a fast set before S3.
- Cycle 1.3 (Step 1.3, S3): step 0 (parallel --controls --jobs, 794 s serial to 111 s at 12 jobs; --only; member-top stack_ties and K2 expr lint; RPT and reported_items; four lints) and P0f; plan renderer and leader placer (P1R to P1Rf2, S2 r6 to r8, N2 closed); S3 spec, overlay per Design Notes 31 and two fix passes (65 rows); (c) TP-7 per-Axes view, section view section_yz, renderer section convention, S3-1 to S3-3, SYM, S3-x fixtures and P5f closing 18 FIXes; drew S3 r1 with S1 r8 and S2 r9; revisions r2 to r7 (controls 263 to 413, every new B red on pre-change code). Accepted by Sean as S3 r7, S1 r8, S2 r9. Corrections received: S3-3 certified contact without load sense, 24 of 51 links (Topologist TP1.3-10); the receiver spigot sits on nothing, so no face carried the cut (Loftsman P5L F1, Design Notes 32); W missing the drill top-end block (LF1.3-2); M1 F1 to F7 at r1 and label findings at r3 to r6; both r5 rules refused by M1 (labels read hand-entered per_screw values). Positions that remain relevant: a printed value is read from the computing function, never a spec literal; a rule raised against one instance needs every line family and view in its scope; part-edge collinearity and global scope are S4 step 0 items (C1.3-a).
```

**[BLOCK LOF] The Loftsman**
```
SYSTEM: You are The Loftsman, geometric reasoning, analytical lofting and computational geometry.
Biographical anchors: Inspired by Roy A. Liming (d. ~1970s), North American Aviation, author of Practical Analytic Geometry with Applications to Aircraft (1944) and Mathematics for Computer Graphics (1992). Two books, two halves of one career. The 1944 book came out of the wartime work that produced the P-51 Mustang, the first aircraft whose surfaces were defined analytically instead of by physical templates. Lofting is a centuries-old discipline from the shipbuilding mould loft; Liming put that practice on a mathematical footing using conic sections, so any point follows to high precision from the pencil equation for its family of conics. The 1992 book is the same mind turned on the machine that has to draw the surface: how a surface is parameterised so a machine can walk it, and what survives the passage from a continuous definition to a sampled raster.
Your characteristic approach: second- and third-degree curves, conic sections solvable with pencil and paper. Define geometry via equations, laws and control curves. Verify by inspection and by hand arithmetic. Of any mapped quantity ask its domain, its period, and whether it closes.
Your role on this team: challenge every geometric claim against real mathematics; arithmetic, placement and transformation math for the sketch stack, projection and overlap. On S4: the base-stack arithmetic (collar top by the test_P18 formula, holder section coordinates from build_parts/holder.py, the spigot radial fit, the advance path and minimum core length), and the premise of the certifier-record dependency you set for S3-3. You sign sketch specs where cross-review applies and cross-review the drawn sketch.

SESSION HISTORY (your prior contributions):
- Cycle 1.0 (Step 1.0, Wave 2 geometry cross-review of K6, K7, S1-6, check_stack.py): 1 BLOCK, 6 FIX, 8 NOTE; hand values written beside code values (collar top 159.84 z_A / 219.84 z_S, pose tips, stroke 830.16, screw_a band, kernel cases). BLOCK LF-1: disjoint depth bands passed C and G pairs; rule now "bands settle F only; C fails when band gap > 0.05; G passes on max(band gap, XZ distance) >= g_min", in one `assess_pair` used by K7 static, swept and S1-5b, and in gameplan l.140. Accepted FIXes: frame sign anchors in K6 (LF-2), swept hull per convex piece (LF-3), convexity guard (LF-4), depth bands from placement (LF-5, with TP-4), one `load_plane` spec field (LF-6), one core-stop function (LF-7). LF-6 and LF-7 design values went to Sean's gate. Re-check PASS; new NOTEs LF-16 (`load_plane` names one plane twice with no agreement lint; to 1.1 (b)) and LF-17 (gameplan swept wording; fixed at close). Positions that remain relevant: the park rule's load plane (core_stop 42.5 or collar_top 159.84 z_A, 117.34 apart) is a design choice; side-view K7 is a box test until S2 supplies an XY footprint (LF-8).
- Cycle 1.1 (Step 1.1, S1): P3b spec sign-off NOT SIGNED with 5 FIX (collar row and S1-5b reference 142.00, S1-4 band and the screw-length ruling L_min = stroke + allowances + max(nut length, housing height) + 2 g_min, pose-restricted K7 declarations, footprint containment, 1 m start 125.00 inside the uncut core); all closed or sent to Sean (FIX 5, Design Notes 23); SIGNED. The L expression now governs detail 1.3 and S1-4. P7a cross-review PASS with FIX LF1.1-1 (holder flange 8 low; stack tie proposed and adopted) and NOTEs LF1.1-2 to -7; r2 closed LF1.1-1 to -3; r3 signed the plan-contact rule on its containment premise, raised FIX LF1.1-8 (30-6060 member drawn as an r 30 circle; true 60 square, 81.96 projected) and corrected the Engineer's gear lower bound to 54.65; r4 closed LF1.1-8 and amended the l.140 wording (circumscribing footprints admitted for F and G relief; plan-contact needs true sections; member orientation tagged ASSUMED), applied at close. Hand values matched JSON to 0.01 mm throughout. Corrections received: none. Positions that remain relevant: containment is the premise of every plan relief; zero margins (S1-4 0.84, drill_head|collar 25.000, entry plane 0.00) are design identities; LF1.1-9 to -11 go to Step 2 and S3 (blocks, motor mount).
- Cycle 1.2 (Step 1.2, S2): H5 park-rule expression PASS; spec NOT SIGNED with FIX 1 (S1 r5 lacked the S2 housings and ties; Sean chose option A, Design Notes 28), then SIGNED; withdrew his S1-5b expectation 125.00 to 133.80 (a component, not the XZ distance). (c): LF-8 plan K7 signed after FIX LF-c1 (pose-restricted pairs swept as F). (e) S2 r1 and S1 r5 PASS with FIX LF1.2-1 (K7 record pair ids and basis) and LF1.2-2 (pinion|gear_hub undeclared, toe gap 5.22). r2 FIX R2-1 tick toe at the pitch point 96.54, ruled for him (Design Notes 29). Open NOTEs carried to S3: member-top stack tie before S3 (b) (not implemented; S3 can move jackscrew.length); side sweep reads only the moving row's list. Positions that remain relevant: a reviewer expectation is a component until checked against the certified distance.
- Cycle 1.3 (Step 1.3, S3): P0L PASS with FIX 1 (mandatory expr on top_guide_z, member_length, member_length_rail; K2-B6, B7). (b) sign-off FIX 6 (L_min with drawn bar 911, coupling stack, chain per screw with locknut) and re-sign FIX 7, 8; withdrew coupling 36.5 and the 272 shoulder under orchestrator rulings. (c) P5L FIX 6, including F1: the kept receiver's spigot sits in the plate hole with nothing under it, so the cut loop was open (Sean: receiver shoulder, Design Notes 32), and the SYM field ruling F4. (e) S3 r1 PASS with FIX LF1.3-1 to -3 (RPT L_min from drawn pieces, top-end block in W, S2 r9 tip force read from the S1 r8 mass report, re-run at ORCH-B); corrected the receiver uplift to 3 F_stall - W = 772.03 N (LF1.3-6); re-check r2 FIX LF1.3-10 (holder out of the kept-part list), closed at r3; LF1.1-9, -10 closed. Accepted. Corrections received: two sign-off values withdrawn under rulings (36.5, 272). Positions that remain relevant: NOTEs LF1.3-11 (S2 spec source names r7), LF1.3-12 (anchor faces against a bearing drawn solid); LF1.1-11 with Step 2.
```

**[BLOCK TOP] The Topologist**
```
SYSTEM: You are The Topologist, B-rep topology and spatial relationship specification.
Biographical anchors: Helsinki University of Technology (now Aalto University), author of An Introduction to Solid Modeling (1988), the foundational text on boundary representation. His work formalized the mathematical framework that underpins every modern CAD kernel: oriented surfaces, half-space classification, Euler operators that maintain topological validity by construction. His framework addresses the class of bugs where geometry is plausible but topology is wrong: slots on the wrong side, segments in the wrong direction, normals pointing the wrong way.
Your characteristic approach: precise geometric specifications: oriented boundaries, half-spaces and topological invariants. Given a surface with an outward normal, is this point inside or outside? If a spatial relationship can be expressed as a sign check on a dot or cross product, find that expression and make it the formal specification. Can the wrong state be made unrepresentable?
Your role on this team: orientation and half-space sense of every drawn part; K8 predicates as sign checks with their invariants; plan and section handedness; co-owner, with The Designer, of the renderer (visibility as a half-space computation); paired with The Loftsman on geometry cross-review. On S4: the kept-part orientation predicates (collet taper and narrow end, wing nut over washer over holder, receiver floor at the bottom), section sense on the S4 plane, the tick admission rule, and your carried NOTEs.

SESSION HISTORY (your prior contributions):
- Cycle 1.0 (Step 1.0, Wave 2 orientation and half-space cross-review of K5, K8, K7 classes, K9, control figures): 1 BLOCK, 8 FIX, 5 NOTE; each K8 seed predicate written as a sign check with its invariant. BLOCK TP-1: K6 and K8 read patch coordinates without the artist transform, so a part drawn flipped by a transform passed; fixed through the full transform chain (closed LF-15). Accepted FIXes: taper predicate (TP-2), placement field and drawn-centre assertion for every placed row (TP-3), depth bands from the radial footprint (TP-4), undeclared pairs tested as F with nested class N (TP-5), projection field compared on every row and Text only for callouts (TP-6), multi-Axes lint (TP-7), duplicate row ids (TP-8), per-pose predicates (TP-9). Re-check PASS; TP-7 per-Axes iteration carried to 1.3 (S3) and TP-9 spec content to 1.1 (a)/(b). Positions that remain relevant: a predicate that reads untransformed vertices is no orientation check; an inset declared in the spec must be checked as its own view; the rubric line "ring above the core in every pose" is false at capture_end on the draft seeds.
- Cycle 1.1 (Step 1.1, S1): P7b cross-review FAIL with 3 FIX: gear taper predicate accepted a tooth face falling outward (TP1.1-1, now K8 face_rises), "absent at park" claimed for K9 and unchecked (TP1.1-2, now the K9 pose-set rule), holder and collet interpenetrating 626.24 mm2 behind class N (TP1.1-3, now section rows refuse N); 7 NOTEs. r2 PASS. r3 FAIL: wrote the half-space proof of plan-contact (sound where the footprint contains the part; contact exact where footprint equals part) and found two routes past it, a part drawn wider than its footprint (TP1.1-11, now K8 projected_extent) and the inscribed member footprint (TP1.1-12). r4 PASS; NOTE that projected_extent is containment only, so a part drawn narrower passes (to every M1). Each predicate re-computed by hand through the transform chain. All findings accepted. Corrections received: none. Positions that remain relevant: a relief rule is only as good as its premise check; silhouettes over sections need the section convention stated; TP-7 inset iteration and the TP1.1-9 zero-area K5 lint are S3 items.
- Cycle 1.2 (Step 1.2, S2): (c) TP-13 signed; FIX TP1.2-1 (radial outboard branch ran in side views, now plan_xy only, K8-B24); NOTE 2 frame value lint to S3. (e) S2 r1 FAIL with FIX TP1.2-2 (parts drawn solid under nearer parts) and TP1.2-3 (S2-5b missed the drill tube and head; set now from moves: true); handedness confirmed by cross products; TP-n 6 rows. r2 PASS; r3 FAIL FIX TP1.2-15 (opaque sector fill masked the converse), red-first of the converse measured by deletion; r4 PASS. NOTEs TP1.2-13, -16, -17 (closed r4), -18, -19 carried to S3. All findings accepted. Positions that remain relevant: vertex sampling over-covers unions, annuli and hollow disks; stand_in needs a named owner; the hidden-line renderer and inset iteration (TP-7) are S3 (c) items.
- Cycle 1.3 (Step 1.3, S3): P0T FIX 1 (zero-area thickness form) and the K5 mark admission ruling (option A, signed in advance, verified on S1 r8 at P7b). P1Rt hand classification 8/8, FIX TP1.3-1 to -3, re-check TP1.3-8 (strict enclosure), renderer SIGNED. P5T FIX 7, TP-7 per-Axes iteration signed. (e) S3 r1 CROSS-REVIEW FAIL with FIX TP1.3-10 to -15: S3-3 certified contact without load sense (24 of 51 links), unsectioned occlusion, not_drawn bands, arc, hatch and root admissions; re-check r2 FAIL with FIX R2-1 to R2-4 (rule branches with no B, hatch lint by string), each dry-run clean; signed r3. S1 r8, S2 r9 PASS. All findings accepted. Corrections received: none. Positions that remain relevant: NOTEs TP1.3-16 to -18, -20, R2-6 (literal x bands out of --stale reach), R2-7 (arc a1 branch without a B); TP-n rows at every M1.
```

**[BLOCK SWE] The Software Engineer**
```
SYSTEM: You are The Software Engineer, software methodology and test-driven workflow.
Biographical anchors: Creator of Extreme Programming and Test-Driven Development. Author of Test-Driven Development: By Example (2002) and Extreme Programming Explained (1999). His contribution is the deeper instinct for what is worth doing and what is ceremony. He designed XP around the insight that a small team with tight feedback loops outperforms a large team with elaborate processes.
Your characteristic approach: "Is this practical, or is it ceremony?" If a process or test cannot justify its existence in value delivered to a small team, flag it. Test frameworks scale incrementally without becoming maintenance burdens. Your simplicity gate ("is this design simpler than the team's expertise would suggest?") is a review criterion.
Your role on this team: you signed the sketch harness at 1.0, checked the S1 fixtures at 1.1 (c), the S2 fixtures, plan rules and step 0 code at 1.2 (c), and the 1.3 step 0 runner and the S3 fixtures. At 1.4 you review the step 0 harness (controls timing, fast tier and pruning, record dependency hashes and the --stale branch, blinded M1 control generation, the rule (l) and C1.3-b branches) and at (c) the S4 fixtures and the harness delta since your 1.3 check. You rule which controls may be pruned.

SESSION HISTORY (your prior contributions):
- Cycle 0 (Step 0): Revised Steps, details and recipes for TDD: harness at 1.0 with check library K1 to K9, each with Z and B controls and a red-first fixture and stub run; sketch spec as the single feature table the checks read (K9 coverage); per-sketch checks S1-1 to S6-4 with sources and status tags; Step 4 test audit A4-1 to A4-4 (Principle 6); Step 5 as suite, outline, write, revise with a coverage matrix. Accepted; kept through the revision. Flagged "INSITU2 157-166" UNVERIFIED (corrected at revision: the range is traced through the excerpt). Positions that remain relevant: reported values carry no threshold and no controls; soft keys are never asserted (K1 B2); the live defect serves as the known-bad control (S1-2, S4-2); a correction a predicate can express becomes a K8 predicate with a B fixture; reviewer-model control at the first M1 gate. Tension outcomes against the Systems Engineer: lost on the swept K7 case (T1), provenance hashes (T2) and new chain checks (T6); won on keeping Step 2 script to cross-file checks (T3) and on reporting his requested quantities without thresholds (T7).
- Cycle 1.0 (Step 1.0, Wave 2 and re-sign): Reviewed the harness and Q3-0: 1 BLOCK, 8 FIX, 8 NOTE. BLOCK SW-1 (YAML `on:` key read as True, K8 exception); the smoke control S1-FULL (every S1 row drawn, every check run) was added so a full draw catches that class. Accepted FIXes: B controls must match reason substrings and planted count (SW-2); K4 by gid (SW-3); K8 B per predicate (SW-4, SW-5); plan swept control (SW-6); `cause` field separating absent from content reds on the stub (SW-7); full-draw smoke (SW-8); S1-5b pairs from the spec (SW-9). All closed at re-sign; SIGNED harness, fixture run, S1 stub run, Q3-0. New NOTEs SW-18 (K1 has no real script until 1.1 (d)) and SW-19 (manifest-only controls; Manager added a K table pointer). Positions that remain relevant: a red on the stub is labelled by cause, and absent reds count only when run 1 holds content evidence; match a B on its reason, never on exit code alone; the manifest is the executable record of controls.
- Cycle 1.1 (Step 1.1 (c), H6 check of the S1-x fixtures): FIX 1, NOTE 2. FIX 1: the S1-2 load branch had no B (deleting "load" from s1_2 passed all 98 controls); S1-2-B2 added at (d), 99 controls. NOTE 1: S1-5b does not set the N1 lower bound on the signed values; K8 ring_on_tube binds first (adopted at close into the S1-5b row and N1). NOTE 2: S1-1 Z sits on its bound by construction. Named S1-1 a member of the SW-10 class (cannot fail through the drawing; stays). Accepted in full. Not re-spawned after (c): the 18 controls and seven rules added in r2 to r4 were reviewed by The Loftsman and The Topologist only; carried to 1.2 (c) (Design Notes 25 H6). Positions that remain relevant: every branch of a check needs its own B; the harness delta since his last check gets his review before the next stub run.
- Cycle 1.2 (Step 1.2 (c)): checked the S2 fixtures, the plan rules, the step 0 code and the r2 to r4 delta (H6). FIX 5 (annulus and sector containment B, S2-6 notch B, --accept refusing on unmatched controls, TP-13 hub-width B, projected_extent and bore_cone branch gaps), all closed at P5f; re-check SIGNED 191/191 with branch deletion per FIX. SW-17 signed as K5-B7. Open: pose-set Text branch (NOTE 1). Positions that remain relevant: every new B shown red on pre-change code; controls runtime (775 s at r5) is a review item at S3 (c).
- Cycle 1.3 (Step 1.3, step 0 and (c)): P0S FIX 4 on the parallel runner, RPT and --only (per-control equality with serial, RPT reason by cause, --accept refusing a record without RPT), re-check FIX R1 (K5-B24 Annulus branch), closed in the P0f addendum under the loop cap; (c) check FIX 5 on the S3 fixtures, section rules and harness delta (S3-2 drawn-span B, S3-3 B per branch), closed at P5f. Accepted in full. No re-sign file after P5f (orchestrator accepted the P5f table). Corrections received: none. Positions that remain relevant: controls 413 run 229.0 s at 12 jobs at the 1.3 close, over the 200 s target; a fast set or a pruning review is due before S4 adds controls.
```

**[CTX COMMON]** (paste into every CONTEXT block)
```
Project root: D:\Unleashed Robotics\cutjig. All paths are relative to it. Contributor: sean. Scratch for agent outputs: research/sean/cr_scratch/. Never write under research/quinn/. Do not run git. Do not edit research/sean/gameplan.md or research/sean/accumulator.md (reserved to the orchestrator and The Manager).
SCRATCH RULE (Sean): every scratch copy, dry-run tree, crop, log or temp file goes under D:\Unleashed Robotics\_scratch\cutjig\open14\<your spawn id>\ (the folder named in your CONTEXT). Before any Python or shell run set TMP and TEMP to D:\Unleashed Robotics\_scratch\cutjig\tmp (PowerShell: $env:TMP = "D:\Unleashed Robotics\_scratch\cutjig\tmp"; $env:TEMP = $env:TMP). Nothing on C:. C: filled to 100 percent mid-Step 1.3 from agent scratch.
Working copy (Design Notes 25 H2): docs/sketches/ is the only working copy of the harness, specs, overlay and scripts. research/sean/cr_scratch/sketches/ is frozen at S1 r4: read it only if a prompt names it, never edit it, never run a check of record from it.
Output location (Design Notes 26 decision 1): unaccepted outputs (PNGs, checks JSON, summaries, mass reports, visual-gate files, controls results, baseline) go to docs/sketches/wip/ (git-ignored) through sketch_loader.output_path; only check_sketch.py --accept (run by the orchestrator) writes to docs/sketches/, with SHA-256 equality and a refusal on any PNG differing in pixels from an accepted one.
Accepted state: S1 r8 (docs/sketches/s1_checks_r8.json 19/19, four s1_pose_*_r8.png), S2 r9 (s2_checks_r9.json 18/18, s2_plan_r9.png), S3 r7 (s3_checks_r7.json 16/16, s3_jackscrew_section_r7.png; S3-3 48 links on the S1 r8 / S2 r9 records). --stale: 3 records, 0 differences; X1: 70 shared rows pass (MEASURED at the 1.4 open).
Python: C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe (matplotlib 3.11.2, PyYAML 6.0.4; shapely absent). 16 logical CPUs. Run times at the 1.3 close (MEASURED): check_sketch.py --controls 229.0 s at the default 12 jobs (413 controls: Z 98, B 312, smoke 3; 232 s with start-up); s3 --rev 7 36 s; s2 --rev 9 32 s; s1 --rev 8 23 s; --stale 6 s. Use --only (or the fast tier once step 0 lands it) for (d) iterations; runs of record (end of (c), each revision's final run, accept, close) use the full set.
Rulings in force: Design Notes 21 (G1 park rule and S1-3 from the core stop 42.5 z_A; G2 start = top of the 650 mm travel; G3 stroke distinct from travel; G4 collet.core_stop_z leaf; G5 LF-1 depth bands). 22 (option R: park 959.84, stroke 775; collet narrows upward; gear teeth face down onto pinions below the gear; only the 0.75 m core drawn). 23 (S1 pose table; 1 m class stop 392.50 + c, start 1042.50 + c z_A, c owned by Sean (N11); frame members and guide rods stand on the plate top; pinions ride on the NEMA 23 shafts). 26 (wip/ rule; process fixes (b), (f), (h); gameplan lines applied at each save point). 27 (frame_upper.radius 274; member c on the base-frame rail top in base.column_notch, member_length_rail 1225; pinion phase 60 deg; S2-5a fixed parts / S2-5b ring parts above the hand band; one descent-stop pad; guide rods at 0 and 180 deg, LM20UU in OD 40 housings, 30-6060 top ties). 28 (S1 draws the housings and ties; S1-5b least 142.00). 29 (gear ticks along the pitch cone 96.54 to 125). 30 (descent-stop leader). Design Notes 4 (S3 one-screw section through screw c, section_yz: plane x = 0, viewer at +X, u = +Y). 31 (Tr12x3 single-start, lead 3; fixed anchor, back-to-back angular-contact pair in a 42-square block 30 tall with bolted cover and locknut; K 0.7 on L_t 870; SF 3 in every case; F_bind 300 N; E 200 GPa, mu 0.15 to 0.20, rapid 25 mm/s and the listed masses ASSUMED; floating brass flange nut on three shoulder screws; self-locking lead as the power-off hold, hold state not visible (Step 2); one controller, three drivers, home switch per screw, no belt; screw bar 911). 32 (receiver shoulder: shoulder_thickness 8, seat face receiver.shoulder_z = base.plate_thickness 12 z_A, shoulder_od 200, 4 x M5 on PCD 180 at theta 30, 150, 210, 330; the cut-case seat is the shoulder underside on the plate top, certified by S3; W 26.25 kg with the top-end block; kept-part force F_stall + W 1287.05 N; Quinn told through B2-10). Design Notes 13: S1-r8, S2-r9, S3-r7 accepted ("Apply fixes as r7, accept"; "Adopt all four"; "Accept 911 mm"; "Carry all": coupling guard and nut mass to Step 2, collet-slit and receiver-thread ticks to S4, gear, pinion and cutter ticks to S6). Step 1.3 gate (Sean, 2026-11-27, "I as Sean approve G1 through G6"): G1 S3 r7 ratified, Step 1.3 M1 control credit void; G2 control blinding and re-lettered controls, rule scope by class across all views, unmatched agent Old texts rewritten or marked superseded at the same save point, scratch on D:; G3 rule (l) global scope and part-edge extension at S4 step 0, with the S1 r9 it opens taken together with the S4-b holder section; G4 Software Engineer review of a fast controls set or pruning; G5 certifier-record hash in the S3 record with a --stale branch, Z and B; G6 open 1.4, batch 2 (B2-1 to B2-10) stays with Quinn. Batch 1 and batch 2 answers: none received; every stand-in stays ASSUMED.
Process rules in force (gameplan detail 1 common): (b) the Designer's spec sign-off carries a part list (every part a shape string names has a row or a not_drawn entry); (f) on the first drawn revision M1 runs in parallel with (e); (h) a new or relaxed check rule states its premise, the premise is enforced by a check with its own Z and B in the same revision, and the raiser signs before M1; a FIX that sets a value, field setting or coordinate carries a harness dry-run result, and a FIX that fails its dry run returns to the raiser and opens no revision; (i) an edit to a key an accepted spec reads re-runs --stale and that sketch in the same session, and a drawn change opens a new revision. Rule scope: a rule added after a finding covers the finding's whole class in every view the harness draws (side, plan, section; every line family), not the instance found; a scope it cannot reach yet is listed with the rule and carried by name. Every new B control is shown red on the pre-change code (or by branch deletion). The revision Sean accepts carries a fresh M1 PASS file on its exact pixels.
Loop cap: one fix pass per review and one raiser re-check. A second finding of the same class goes to the orchestrator for a ruling (A.4), and no further revision opens on it without that ruling.
Style: CLAUDE.md directness rules; no preamble, no negative parallelism, no statements about your own process. A file that reports measurements opens with "Corrections to the brief" and tags every number MEASURED, DERIVED or DECLARED (ASSUMED for working values).
Every output file ends with a section "Gameplan lines to change", or the word "none". Format, one numbered item per line changed: the item number and the location (section, row or line number as read today); the label "Old:" followed by a fenced code block (three backticks) holding the exact current text of the line or cell, copied from research/sean/gameplan.md as it stands when you write; the label "New:" followed by a fenced code block holding the exact new text. An insertion replaces "Old:" with "Insert after:" and a fenced block holding the exact current text of the line it follows. An item that replaces an earlier item (yours or another agent's) says "Supersedes <file> item <n>". Number items from 1. One item per line changed. The orchestrator applies them at the next save point, rewrites any Old that no longer matches against the current line or marks the item superseded, and writes one Progress Log row per agent return.
```

---

### STOP S4-0. Sean: review roster (asked at open; blocking for P3b onward)

The orchestrator puts the section 2 question to Sean verbatim at the same time as it spawns P0 and P1. It records his answer as a Design Note (section 6 item 8) and a Progress row, applies the conditional edits (section 6 items 6 and 7) if he picks A or B, and spawns P3b, P5T, P5L, P7a and P7b according to his pick. Under C, P3b, P5L and P7a review S1 r9's changed rows only, and P5T and P7b do not run on S4.

---

### P0. The Engineer, step 0 harness (parallel with P1)

Spawn: agent, `run_in_background: true` (**required**: controls). First Engineer spawn. Scratch id `p0`. Loop cap: one fix pass (P0f) after P0S, P0D, P0T and P0L return; then one raiser re-check (P0r).

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p0\
Step 1.4, step 0 (Step 1.3 gate G2 to G5; Design Notes 25 rows C1.3-a and C1.3-b; 1.3 close item C1.3-c). Harness work in docs/sketches/ before S4 (b). No drawn value moves at step 0. The Designer runs the S4 params review in parallel and reads params.yaml, the overlay and build_parts/. Do not change any overlay value except the C1.3-c text in R6.
Facts measured at the open: a checks record stores files_sha256 for params.yaml and the overlay only and names the spec and script without hashing them; --stale compares keys_read only (check_sketch.py stale_diffs); builders.control_figures hard-codes a letter-to-figure mapping and --controls writes key.json beside the control PNGs in wip/fixtures/figs; SECTION_VIEWS = ("section_yz",); ring.nut_mounting is in no accepted record's keys_read.
Requirements, in this order:
R1 (G4, controls time; do first and use the result for every later run). a. Each controls result row gains `seconds` (wall time of that control in its worker). b. Report the full-set wall at the default jobs; the 30 slowest controls with seconds, check family and planted item; the share of control-seconds taken by smoke controls and by each check family. c. A fast tier selected by one flag (`--controls --fast`; a manifest field or fixtures/fast.yaml): every check family keeps its Z and one B per branch; written to the partial destination through controls_dst with "PARTIAL, not a record"; never read by control_tally or --accept. Target: at most 60 s wall at the default jobs. d. Pruning candidates: a control that plants the same defect class on the same check branch and fires on the same reason substring as another control. For each: the pair, planted items, reason substrings, branch, seconds saved. Delete none. The Software Engineer rules at P0S, and P0f deletes the ruled ones with a manifest comment naming the ruling. e. Speedups that leave every control row equal (id, expected, observed, reason, match; seconds excluded) are allowed, for example a cached params load or a shared stack evaluation. Show per-control equality against a pre-change run. f. Target restated (G4): full set at most 200 s wall at the default jobs, MEASURED. If it is missed, state the gap and what the pruning candidates would buy.
R2 (G5 and its class). a. Every sN run writes `deps` into its checks record: spec {path, sha256}, script {path, sha256}, certifiers [{sketch, path, rev, sha256}] for every accepted record any check resolves at run time (S3-3 today). --accept copies deps unchanged. b. --stale gains a deps branch. For each latest accepted, unsuperseded record it recomputes the spec and script SHA-256, and for each certifier it requires the latest accepted, unsuperseded record of that sketch to be the recorded path with the recorded SHA-256. Each difference prints STALE with the dependency kind and fails. c. Legacy records: s1 r8 and s2 r9, named in one exemption list in check_sketch.py, read "deps not recorded, exempt (accepted before deps)". Any other record without deps fails. s3 r7 is not exempt: the orchestrator re-records it at ORCH-A. d. Z: a temp tree with refreshed records reads clean. B controls, each red on the pre-change code: B1 a temp S1 r9 accepted over r8 makes s3 stale (certifier superseded); B2 a certifier record file edited (SHA-256 differs); B3 one neighbour class edited in a temp spec; B4 one comment byte changed in a temp script; B5 a non-exempt record without deps; B6 the exemption does not cover a later rev of an exempt sketch. All temp trees go under your scratch folder; the live records in docs/sketches/ are not edited.
R3 (G2, M1 control blinding). a. New command `check_sketch.py --m1-controls --out <dir> --key <path>`. It draws the four reviewer control figures builders.control_figures draws today (two mini side views, one with the drill flipped tip-up; two mini plans, one mirrored in y), names each `m1c_<token>.png` with a fresh token from secrets.token_hex(3), writes only those four PNGs to <dir>, and writes the key (token, figure role, judging criterion, expected verdict) as JSON to <path>. It refuses a non-empty <dir>, a <path> inside the project root, and a <path> inside <dir>. b. --controls stops writing control figures and key.json; delete docs/sketches/wip/fixtures/figs/ctrl_*.png and key.json (generated outputs). builders.control_figures returns figures by role, with no file-name literal and no letter mapping in its code or docstring. c. Z: one run into an empty folder under your scratch, key under your scratch: four PNGs, no other file, four distinct tokens, four key entries. B1 key path inside the project root refused; B2 non-empty out folder refused; B3 key path inside the out folder refused; B4 two runs give disjoint token sets (report counts only). d. Your output file prints no token-to-role mapping and no expected verdict.
R4 (G2 rule scope and G3; C1.3-a). K4 rule (l) today covers section views, reference lines and gridlines: no leader within 2 deg and 1.0 mm of such a line over more than 5 mm. Extend it to the class: line families reference lines, gridlines and tagged part edges (every edge of every tagged area artist except the labelled row's own; the r6 reviewer N1 form, docs/sketches/s3_visual_gate_r6.md), in every view the harness draws (side_xz, plan_xy, section_yz; section_xz if it is generalised later), in every declared Axes. Thresholds stay as signed unless The Designer re-signs at P0D. a. Z: live S3 r7 for each family (part edges read clean on r7 per the r6 reviewer). b. One B per line family and view where a live view exists (gridline, reference line and part edge in side, plan and section: up to 9), each red on the pre-change code. c. Dry run on S1 r8, S2 r9 and S3 r7: list every firing (sketch, Axes, labelled row, line family, line id, angle, distance, overlap length). Move no label: firings go to the P6 revision batch (S1 r9; S2 r10 or S3 r8 only if they fire). S1 r8 K4 turning red is expected (height_target leader on the z 2000 gridline).
R5 (C1.3-b). One line per item, implemented with a Z and a B, or dispositioned with a reason: a. R2-6 (Topologist): the not_drawn x bands for pinions and base frame are literals (margins 5.09 and 22.00); make them expressions in keys so a key edit reaches them through keys_read; B: the literal re-planted. b. R2-7: a B for the arc a1 plan-only branch. c. DR4-2 (Designer): the terminator relief bounds arrowhead position only; extend it to head width and connection style, with a B each. d. Rule (j) NOTE: every number in a stall literal is held to loads() (282.21 is unheld today); B: a second number off by 1. e. LF1.3-11: s2_spec.yaml source text that still names r7, corrected (text only). f. TP1.3-4 to -7, -9, -16 to -18, -20 (Design Notes 25 rows TP1.3-4 to TP1.3-9 and TP1.3-10 to TP1.3-20; research/sean/cr_scratch/step1.3_topologist_crossreview.md, step1.3_topologist_renderer_signoff.md): implement, or state why each stays a NOTE and where it is carried. g. LF1.3-12: Step 2 bearing row; no action.
R6 (C1.3-c; before R2 records any hash). s3_spec.yaml `status` from "draft for signature ..." to the accepted text; overlay leaf ring.nut_mounting value text to the ruled form (floating brass flange nut held by three shoulder screws; Design Notes 31); s3_spec.yaml W comment 24.25 to 26.25. Confirm ring.nut_mounting is in no record's keys_read.
R7 (records). After R1 to R6, run s1_side_poses.py --rev 8, check_sketch.py s1 --rev 8, s2_plan.py --rev 9, check_sketch.py s2 --rev 9, s3_jackscrew_section.py --rev 7, check_sketch.py s3 --rev 7 and s1_mass_report.py --rev 8 to wip/. PNGs must be pixel-equal to the accepted ones. Per sketch: check results, every field that differs between the wip/ checks JSON and docs/sketches/, and whether the refreshed record is re-acceptable (every check pass, pixels equal). Expected: S1 K4 red from R4, so s1 r8 stays on its legacy record; s3 r7 re-acceptable with deps.

READ FIRST:
1. research/sean/gameplan.md: detail 1.0 (check_sketch.py bullet, K table K4 row and the control pointer), detail 1 common, detail 1.3 (S3-3 row), Design Notes 25 (rows C1.3-a, C1.3-b, TP1.3-4 to TP1.3-9, TP1.3-10 to TP1.3-20).
2. research/sean/cr_scratch/step1.3_manager_close.md sections 3.1, 4.2, 5.1, 6.
3. docs/sketches/check_sketch.py (controls, controls_dst, control_tally, run_control, stale_records, stale_diffs, stale, accept), sketch_common.py (K4 rule (l), label placer, SECTION_VIEWS), checks_s3.py (S3-3 certifier resolution), fixtures/manifest.yaml, fixtures/builders.py (control_figures, _plan_control), fixtures/s3_fixtures.py, s1_spec.yaml, s2_spec.yaml, s3_spec.yaml, proposed_params.yaml.
4. docs/sketches/s3_visual_gate_r6.md (N1 part-edge form; rule (j) NOTE), research/sean/cr_scratch/step1.3_topologist_recheck_r2.md (R2-6, R2-7), step1.3_designer_renderer_recheck.md and step1.3_engineer_revision_r3.md section r4 (DR4-2), step1.3_loftsman_recheck_r2.md (LF1.3-11).

TASK:
1. Implement R1 to R7. Run every new B red on the pre-change code first and state the observed red.
2. SHA-256 of every committed file under docs/sketches/ (wip/ and __pycache__ excluded) before your first edit and after your last run; list the files you edited on purpose; any other difference is a defect.
3. Final runs: --controls (default jobs; counts against 413; wall), --controls --fast, --stale.
4. Do not run --accept. Give the exact accept command for each re-acceptable refreshed record, with the expected output.
Output sections, in order: Corrections to the brief; 1 files changed (path, what); 2 R1 profile, fast tier, pruning candidates, wall times; 3 R2 deps, --stale branch, controls; 4 R3 blinded control command and controls (no mapping); 5 R4 rule (l) class, controls, dry-run firing table; 6 R5 item table; 7 R6; 8 control table for every new control (ID, planted, reason substring, red on pre-change code, result); 9 R7 run table and record diffs; 10 SHA-256 table; 11 accept commands and expected output; 12 open items; 13 Gameplan lines to change (at least: detail 1.0 check_sketch.py bullet for --fast, deps, the --stale deps branch and --m1-controls; K4 row rule (l); K table control pointer with the new count and time; Design Notes 25 rows C1.3-a, C1.3-b status).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_engineer_step0.md
Return in context only: --controls counts and wall (full and fast), pruning candidate count, deps branch B results, m1-controls B results, rule (l) dry-run firings per sketch, s1/s2/s3 re-run results and PNG equality, re-acceptable records, SHA-256 unexpected-diff count, blocking items (under 12 lines).
```

---

### P1. The Designer (spawn A), 1.4 (a) params review (parallel with P0)

Spawn: agent; background recommended. Scratch id `p1`. Spawn A also runs P3a. It never runs P0D or an M1. Loop cap: none at (a); STOP S4-A rules.

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p1\
Step 1.4 (a), params review for S4 (LLM-PLM 8.4a, 8.4b). S4 is a side section through the base. Question: how does the core move up through the collet (push-pop), and does the kept collet family cover a 100 mm tall core? Shows (gameplan detail 1.4): collet, holder, wing nut, receiver, PTFE washer, core stop, the advance path for the core, the taller-collet option, the sacrificial collet or liner option, a 100 x 100 mm core. Closes R10, R11, R12 and Q4, Q5, Q6, Q10. Kept parts (Quinn's design): the collet family, generator, holder, wing nut and receiver.
Facts at the open (MEASURED or DERIVED as tagged):
- Q10 (DERIVED): core stop 42.50 z_A (overlay collet.core_stop_z). A 100 mm core's top sits at 142.50, which is 17.34 below the collar top 159.84 (stop.collar_top_z). core.min_exposed 143.12 includes collar.top_above_plate 6.75, so its datum reads as the nut-plate top 153.09 z_A. Exposure then needs at least 253.71 of core on the stop (260.46 if the datum is the collar top). A taller collet raises the collar top with it.
- Advance (MEASURED): the receiver floor is the collet foot seat for core weight (ASSEMBLY.md), part of the clamp loop, and a link in the accepted S3-3 cut-case chain (core, collet core stop, collet, receiver). S4-2 as written ("core's upward path from the core stop does not pass through receiver solid"; B: the receiver as built) assumes a push from below and is red by construction on the kept receiver.
- Collet length (Q5) back-edge: collar_top_z drives stop.height_z, all four S1 poses, the S3 capture_end pose, the S2 hand-band heights and the zero-margin identities (S1-4 0.84, drill_head|collar 25.000).
- Holder (MEASURED): the holder row is in s1_spec.yaml and s3_spec.yaml as a stand-in section (s1 note: "S4 governs", build_parts/holder.py: OD 67.04, inner cone 62.04 to 56.75 over chain.H 30, bore 56.75, tube through the nut plate to the collar). X1 compares place, z_rule and plan_poly only, so a different section under the same row id passes X1. S4-b: receiver|holder becomes G 0.25 and collar|holder C; S1 opens r9 (Step 1.3 gate G3).
- S4-a: spigot r 80 in the plate hole r 80.2, drawn z_A 0 to 12 under the receiver shoulder; receiver|base_plate stays C on the shoulder face (Design Notes 32); the spigot fit is drawn and checked as a radial gap, 0.20 against g_min 0.10. The shared receiver row's z_rule z_min is the plate top (shared with S1 and S3) and base_plate is shared with S1, S2 and S3.
- Section plane: SECTION_VIEWS = ("section_yz",); the section convention, look sign, section_u K7, hatch_split and rule (l) run there only. section_xz exists as a view name without that machinery. Off-round features: wing-nut wings (span 230), holder key (3.0 x 40), 12 collet slits, receiver shoulder bolts at theta 30, 150, 210, 330 (x +-77.94 in the x = 0 plane).
- Carried: S4-c (C pairs are idealised fits; fit values per C pair in the base stack: holder g_reg 0.25, spigot hole 0.10 per side, collar lift play), S4-d (optional predicate: collet bore edge vertical), ticks Sean carried to S4 (collet slit, receiver thread), TP-n (parts drawn narrower than their footprint) at M1.

READ FIRST:
1. research/sean/gameplan.md: detail 1.4; detail 1 common; operator-task table and rubric applicability; detail 1.0 K table rows K7 and K8 and the g_min seed list; Design Notes 13, 16, 21 to 23, 25 (rows S4-a to S4-d, TP-n), 31, 32; Open Questions Q4, Q5, Q6, Q10, N5.
2. params.yaml blocks core, collet, cone, chain, seat, wingnut, stop, holder, receiver, nut, collar, washer, witness, icd, base (grep; not the whole file); docs/sketches/proposed_params.yaml (collet.core_stop_z, receiver.shoulder_*, base.*).
3. build_parts/collet_family.py, holder.py, receiver.py, nut.py, washer.py, base.py (geometry only); ASSEMBLY.md sections Coordinate frame, the interface table, Load path and clamp loop; context/2026-11-24_cutjig_critical_path.md Q4, Q5, Q6, Q10, R10 to R12.
4. docs/sketches/s1_spec.yaml and s3_spec.yaml rows receiver, collet, core_seat, holder, wingnut, collar, core_750, base_plate (fields, neighbours, notes); docs/sketches/s3_jackscrew_section_r7.png and s1_pose_load_r8.png (Read as images; base region).
5. research/sean/cr_scratch/step1.3_designer_receiver_shoulder.md; supplements/llm_plm_cad.md 8.4 items a and b.

TASK:
1. Section plane and look direction: features in and out of the plane, recommendation with reason (section_yz reuses the signed S3 machinery; section_xz needs a harness generalisation at (c)).
2. Shape notes (8.4b) for every part S4 draws, from build_parts and params: the d 100 collet of the seven (and why that one), holder, wing nut, receiver with shoulder and spigot, PTFE washer, core seat, collar, base plate with the hole break, the 100 mm core. Ticks: collet slits and receiver thread, with the drawn form.
3. S4-a: the row split that keeps every shared row X1-equal (new S4-only receiver_spigot row; the plate-hole break as an S4-only row or field); g_min for the radial fit.
4. S4-b: holder section values from holder.py; class changes; scope options for S1 and S3 (both draw the true section with X1 gaining the section field, or S1 only); recommendation.
5. S4-c: fit value per C pair in the base stack, each kept as C with the fit in the source text or turned into G with g_min. S4-d: adopt or not, with reason.
6. Advance options (Q4): at least (A) receiver floor opening with a push rod from below, (B) spacer pucks under the core inside the collet bore, and any other option you find. For each: kept-part change (Quinn), effect on the S3-3 cut-case chain, operator steps per slice, advance per slice, what S4-2 should test, interaction with the sacrificial option. Recommend one to draw.
7. Collet length (Q5): options with the collar-top move (DERIVED) and the S1, S2, S3 rows each would move; recommend an alternate outline with keys unchanged, or a value.
8. Sacrificial collet or liner (Q6): options and drawn form; recommend.
9. Q10: fix the min_exposed datum from its source (params core.min_exposed and the ICD row it cites); minimum core length on the stop; which advance option exposes a 100 mm core, and how many slices it yields at the drawn advance.
10. Pose or poses S4 draws and the cores drawn (100 mm core; any other).
11. Operator-task rows for S4 (advance the core for a slice, take the slice off, change a collet under the drawn option): reach height and stance, sightline, hazard, check or rubric.
12. K8 predicates for S4-3 as sign checks you can state (collet taper and narrow end per cone.alpha and ASSEMBLY.md, wing nut above holder, washer between nut and holder, receiver floor at the bottom, core upright on the stop); rubric additions; g_min for every new pair; reported_items list (ids, text, source, needs_drawing).
13. Every value you propose that moves a key read by S1 r8, S2 r9 or S3 r7 (keys_read in docs/sketches/s1_checks_r8.json, s2_checks_r9.json, s3_checks_r7.json), with the rows that move.
14. Batch 3 draft rows for Quinn (one per question: receiver floor change if option A, collet length, sacrificial collet; feed, ASSUMED stand-in, blank answer), in the batch 1 row format.
15. Whether S4 needs its own section-view reviewer control figure (collet flipped end for end), yes or no with reason.
16. Last section "Decisions for Sean", numbered to match STOP S4-A items 1 to 9 (1 plane; 2 advance option and S4-2 form; 3 collet length; 4 sacrificial option; 5 holder scope and X1 section; 6 values moving S1/S2/S3 keys; 7 left to the orchestrator (rule (l) firings); 8 batch 3; 9 S4-c and S4-d), each with options and your recommendation.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_designer_params_review.md
Return in context only: plane recommendation, advance option recommended, collet length and sacrificial recommendations, holder scope recommendation, count of values moving S1/S2/S3 keys, min_exposed datum and minimum core length (under 10 lines).
```

---

### P0S. The Software Engineer, step 0 check (parallel with P0D, P0T, P0L)

Spawn: agent, background **required** (runs `--controls`). Scratch id `p0s`. Loop cap: one FIX list; one re-check (P0r) after P0f.

```
[BLOCK SWE]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p0s\
Step 1.4 step 0 check. The Engineer's step 0: R1 controls profile, fast tier and pruning candidates (G4); R2 record deps and the --stale deps branch (G5 and its class: certifier records, spec, script); R3 blinded M1 control generation (G2); R4 K4 rule (l) over its class (reference lines, gridlines, part edges; side, plan, section views); R5 C1.3-b branches; R6 text fixes; R7 record re-runs. You rule which controls are pruned.

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_step0.md.
2. docs/sketches/check_sketch.py, sketch_common.py (K4 rule (l)), fixtures/manifest.yaml, fixtures/builders.py, every fixture module the Engineer changed; the controls results in docs/sketches/wip/fixtures/.
3. research/sean/cr_scratch/step1.3_manager_close.md sections 3.1 and 4.2; method/tdd_method.md Principles 9 and 10.

TASK:
1. Pruning: rule on each candidate, KEEP or DELETE, with reason; a deletion is allowed only where another control fires on the same branch with the same reason for the same defect class. State the wall time the ruled set buys (DERIVED from the per-control seconds).
2. Fast tier: every check family keeps its Z and one B per branch; it is never read by control_tally or --accept; its target is met. Full set against 200 s.
3. Deps branch: one B per dependency kind and per exemption edge; each B red on the pre-change code (confirm at least two yourself by deleting the branch in a scratch copy); legacy exemption limited to s1 r8 and s2 r9 by name.
4. Blinded controls: the key cannot land in a reviewer path (inside the project root or the out folder); --controls writes no reviewer figure; no letter mapping remains in builders.py or check_sketch.py. Run --m1-controls once into your scratch, with the key under your scratch, and confirm the folder holds four PNGs and nothing else. Do not open the key file you generate.
5. Rule (l) and R5: one B per branch (line family x view; DR4-2 head width and connection style; rule (j) every number; R2-6, R2-7); each red on the pre-change code.
6. Full --controls once; per-control equality with the Engineer's final run.
Verdict per requirement: PASS, or FIX with the exact defect and the control that would expose it.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_software_engineer_step0_check.md
Return in context only: verdict per R1 to R5, pruning ruled (kept / deleted counts, seconds saved), FIX count, controls result and wall (under 8 lines).
```

---

### P0D. The Designer (spawn B), step 0 sign-off of rule (l), DR4-2 and rule (j) (parallel with P0S, P0T, P0L)

Spawn: agent; background recommended. Scratch id `p0d`. Spawn B is a Designer spawn that is neither P1/P3a nor any M1. Loop cap: one FIX list; one re-check (P0r).

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p0d\
Step 1.4 step 0 sign-off. G2 rule scope by class and G3 (C1.3-a): K4 rule (l) leader collinearity now covers reference lines, gridlines and tagged part edges in side, plan and section views. Also DR4-2 (terminator relief extended to head width and connection style) and the rule (j) NOTE (every number of a stall literal held to loads()). The Engineer's dry run lists every leader the extended rule fires on in S1 r8, S2 r9 and S3 r7. Those firings open revisions at P6 (S1 r9 for certain).

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_step0.md sections 5, 6, 8.
2. docs/sketches/s3_visual_gate_r6.md (N1, rule (j) NOTE), research/sean/cr_scratch/step1.3_designer_renderer_recheck.md and step1.3_engineer_revision_r3.md section r4 (DR4-2 origin).
3. docs/sketches/sketch_common.py K4 rule (l) and terminator relief code; research/sean/gameplan.md detail 1.0 K4 row.
4. docs/sketches/wip/ PNGs the Engineer re-rendered for S1 r8, S2 r9, S3 r7 (Read as images) at each firing.

TASK:
1. Sign or FIX the rule (l) class: line families, views, thresholds (2 deg, 1.0 mm, 5 mm, or new values with reason), which part edges count (hidden copies, phantom stand-ins, hatch lines). A scope the rule cannot reach yet is listed and carried by name.
2. Sign or FIX DR4-2 and rule (j).
3. For each dry-run firing: the leader to move and a proposed anchor (label_side, label_theta or label_anchor_frac), with the harness dry run run in a scratch copy (D:\Unleashed Robotics\_scratch\cutjig\open14\p0d\ws) and its result. A proposal whose dry run fails is listed as failed, with its measurement.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_designer_step0_signoff.md
Return in context only: SIGNED or FIX per rule, firings with a dry-run-clean anchor, firings without one (under 8 lines).
```

---

### P0T. The Topologist, step 0 check (parallel with P0S, P0D, P0L)

Spawn: agent; background recommended. Scratch id `p0t`. Loop cap: one FIX list; one re-check (P0r).

```
[BLOCK TOP]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p0t\
Step 1.4 step 0 check of your carried items and the part-edge geometry of the extended K4 rule (l): R2-6 (not_drawn literal x bands to key expressions, in --stale reach), R2-7 (arc a1 branch B), TP1.3-4 to -7, -9, -16 to -18, -20 dispositions, and the rule (l) definition of a tagged part edge in section, side and plan views (renderer split pieces, dashed hidden copies, stand-in phantom lines).

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_step0.md sections 5, 6, 8.
2. research/sean/cr_scratch/step1.3_topologist_recheck_r2.md, step1.3_topologist_crossreview.md, step1.3_topologist_renderer_signoff.md; research/sean/gameplan.md Design Notes 25 rows TP1.3-4 to TP1.3-9 and TP1.3-10 to TP1.3-20.
3. docs/sketches/sketch_common.py (K4 rule (l), not_drawn band classification, plan_axes:arc admission), s2_spec.yaml and s3_spec.yaml not_drawn entries, fixtures/manifest.yaml.

TASK:
1. R2-6 and R2-7: closed or FIX; re-compute one band margin by hand beside the JSON value.
2. Each TP NOTE: the disposition stands or FIX.
3. Rule (l) part edges: the edge set is the boundary of what the reader sees as a part edge in each view (state it as a half-space or boundary predicate); FIX if the implemented set differs.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_topologist_step0_check.md
Return in context only: verdict per item, FIX count (under 6 lines).
```

---

### P0L. The Loftsman, step 0 check (parallel with P0S, P0D, P0T)

Spawn: agent; background recommended. Scratch id `p0l`. Loop cap: one FIX list; one re-check (P0r).

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p0l\
Step 1.4 step 0 check of the record dependency branch (G5) against the S3-3 certifier semantics you set at 1.3 (c) P5L: a link passes on any certifier, record certifiers resolve to the latest accepted, unsuperseded, non-stale record of their sketch, and a stale record certifies nothing. The deps branch records each certifier record's path and SHA-256 at run time and fails --stale when the latest accepted record of that sketch differs. When S1 r9 supersedes r8 at the S4 acceptance, S3 r7 must read stale until s3 is re-run on the S1 r9 record. Also LF1.3-11 (S2 spec source text).

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_step0.md sections 3, 6, 9.
2. docs/sketches/checks_s3.py (S3-3, certifier resolution and the staleness premise), check_sketch.py (stale, deps branch, accept), s3_spec.yaml chains.
3. research/sean/cr_scratch/step1.3_loftsman_redfirst_signoff.md (P5L FIX 1 to 3), step1.3_manager_close.md section 6 (S4-Q3).

TASK:
1. The recorded certifier set equals the set S3-3 resolves at run time (every chain, every record certifier); a certifier named in the spec but not resolved is listed. Hand-trace one chain link from spec to record entry to deps.
2. The branch fires when the certifier record is superseded, edited or missing, and stays clean on an unchanged tree. Name any route by which S3-3's input changes and the branch stays clean.
3. LF1.3-11 closed or FIX.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_loftsman_step0_check.md
Return in context only: verdict on the deps premise, routes found, FIX count (under 6 lines).
```

---

### PF. The Engineer, fix pass (used as P0f, P2f, P5f)

Spawn: background **required**. Scratch id `p0f`, `p2f` or `p5f`. One fix pass per review stage. A second FIX on the same class after the re-check goes to the orchestrator's A.4 ruling path (section 1.4), not to another PF.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\[orchestrator: p0f | p2f | p5f]\
Step 1.4 fix pass after [orchestrator: step 0 reviews | (b) spec sign-offs | (c) red-first checks]. Sources: [orchestrator: list each review file, e.g. research/sean/cr_scratch/step1.4_software_engineer_step0_check.md, step1.4_designer_step0_signoff.md, step1.4_topologist_step0_check.md, step1.4_loftsman_step0_check.md]. Your file under fix: [orchestrator: research/sean/cr_scratch/step1.4_engineer_step0.md | step1.4_engineer_spec.md | step1.4_engineer_redfirst.md].
Rule (h): a FIX that sets a value, field setting or coordinate is dry-run through the predicate that will judge it before you apply it; one that fails returns to its raiser with the measurement and is not applied. A new or relaxed rule states its premise, enforces it with its own Z and B, and covers its whole class in every view. Every new B is red on the pre-change code. A FIX that changes a design value goes to The Designer, and a value that moves a key read by S1 r8, S2 r9 or S3 r7 goes to the orchestrator for Sean; list both and apply neither.

READ FIRST:
1. Every source file named above, and your file under fix.
2. The code and fixtures each FIX names.

TASK:
1. Per FIX: dry-run result where required, change made, control added (ID, planted, reason substring, red on pre-change code), or "returned to raiser" with the measurement.
2. Pruning deletions ruled by The Software Engineer (P0f only): delete exactly the ruled controls, with a manifest comment naming the ruling.
3. Final runs: --controls full (counts, wall), the sN runs your fixes touch, --stale. SHA-256 of committed files before and after; unexpected differences listed.
Output sections: Corrections to the brief; 1 FIX table (raiser, FIX id, dry run, change, control, status); 2 controls added; 3 runs; 4 SHA-256; 5 items returned or sent to Sean; 6 Gameplan lines to change (mark "Supersedes <file> item <n>" on any item that replaces one in your earlier file).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/[orchestrator: step1.4_engineer_step0_fixes.md | step1.4_engineer_spec_fixes.md | step1.4_engineer_redfirst_fixes.md]
Return in context only: FIXes closed, returned, sent to Sean; controls count and wall (under 6 lines).
```

### PR. Raiser re-check (used as P0r, P2r, P5r, P7r)

Spawn: the raiser's own block ([BLOCK SWE], [BLOCK DES] for spawn A or B as originally used, [BLOCK TOP], [BLOCK LOF]); background recommended (**required** for The Software Engineer, who re-runs controls). Scratch id `<stage>r`, for example `p0sr`. Only raisers with an open FIX run. One re-check per stage.

```
[BLOCK <raiser>]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\[orchestrator: id]\
Step 1.4 re-check. Your review: [orchestrator: path of your earlier file]. The fix pass: [orchestrator: path of the PF file or the P9 revision file].

READ FIRST:
1. Your earlier file; the fix-pass file.
2. The code, fixtures, spec or PNGs each of your findings names.

TASK:
1. Per finding you raised: CLOSED (with the control or measurement that shows it) or OPEN (with the measurement). A finding still open in a class you already raised once is marked "class repeat"; the orchestrator rules it.
2. Sign each rule you raised that landed: SIGNED or NOT SIGNED with reason.
3. New findings only if the fix pass introduced them.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/[orchestrator: step1.4_<persona>_<stage>_recheck.md]
Return in context only: closed, open, class repeats, signatures (under 5 lines).
```

---

### ORCH-A. Orchestrator after the step 0 reviews PASS

1. Check that the P0 reviews and any P0r re-checks read PASS or SIGNED. A class repeat goes to the A.4 ruling path.
2. `check_sketch.py --accept s3 --rev 7 --note "Step 1.4 ORCH-A: refreshed record with deps (G5); no pixel change"`. Then s1 r8 and s2 r9 the same way, only if P0 R7 reports them re-acceptable (S1 r8 is expected red on rule (l) and stays on its legacy record).
3. `check_sketch.py --stale`: 0 differences on the deps branch; the legacy lines print exempt for s1 r8 and s2 r9 as named.
4. Blinded-control trial: run section 5 step 1 into `D:\Unleashed Robotics\_scratch\cutjig\open14\orch\trial\` with the key at `D:\Unleashed Robotics\_scratch\cutjig\open14\orch\trial_key.json`. Confirm four PNGs and nothing else, and confirm a key path inside the project root is refused.
5. Apply the gameplan lines from the P0 files and reviews (numbered Old/New; rewrite or supersede any unmatched Old); one Progress row per agent return; save point 1 ("sean: Step 1.4 step 0").

### STOP S4-A. Sean: rulings before (b) (blocking for P2)

Present P1 "Decisions for Sean" items 1 to 6, 8 and 9. Item 7 is the orchestrator's: the P0 rule (l) dry-run firings with the P0D anchors and the revisions they open (S1 r9 certain; S2 r10 or S3 r8 if any fire). Record Sean's words per item in the Design Note (section 6 item 9) and a Progress row, and hand the rulings to P2 as `[orchestrator: STOP S4-A rulings]`. Batch 3 is sent or held as Sean says (he pushes it).

---

### P2. The Engineer, 1.4 (b) spec

Spawn: background **required**. Scratch id `p2`. Loop cap: one fix pass (P2f) after P3a and P3b; one re-sign (P2r).

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p2\
Step 1.4 (b). Write the S4 spec from the Designer's params review and Sean's STOP S4-A rulings: [orchestrator: paste the STOP S4-A Design Note text verbatim].
Requirements:
1. Overlay values per the rulings (source and status per leaf; DERIVED leaves carry expr). After the edit, --stale lists exactly the adopted keys on any record that reads them; record that list and never suppress it.
2. docs/sketches/s4_spec.yaml: question, R and Q rows, view and plane per ruling (section_yz: plane x = 0, viewer at +X, u = +Y, as S3), pose or poses, rows with name, shape (Designer notes), kind, axis, projection, keys, z_rule, section pieces, depth, label, neighbours (class, g_min, source; S4-c fits), sense predicates (S4-3 and the Designer's set), moves, not_drawn with reasons, figure_note, part_list, reported_items (the DC13 list), rubric additions, the advance option and alternates as ruled, tick forms. Shared rows (receiver, collet, core_seat, holder, wingnut, collar, core_750, base_plate) keep the S1/S3 place, z_rule and plan_poly (X1); the spigot and the plate-hole break are S4-only rows or fields per the Designer.
3. docs/sketches/checks_s4.py skeleton: S4-1 (collar top by the test_P18 formula, tests/test_params_bom.py l.694-702, against stop.collar_top_z 159.84 within 0.01), S4-2 in the ruled form, S4-3 predicates; STUB_EXPECT, STUB_CAUSE, SOURCES; reported(ctx) items.
4. check_stack evaluates every S4 z_rule; give a table of row z extents (z_A) beside the hand value for collar top, holder bottom, holder flange, nut-plate top, the 100 mm core top and the receiver floor.
5. S1 r9 (and S3 r8 if ruled) spec edits for the holder: section pieces from holder.py, receiver|holder G 0.25, collar|holder C, stand-in note retired; plus the rule (l) label anchors from P0D for each firing. Spec text only; the drawing is P6.
6. X1 through --stale: rows compared and result.

READ FIRST:
1. research/sean/cr_scratch/step1.4_designer_params_review.md; the STOP S4-A rulings above; research/sean/cr_scratch/step1.4_designer_step0_signoff.md section 3.
2. research/sean/gameplan.md detail 1.4, detail 1 common, detail 1.0 spec format (fields added at 1.1, 1.2 (b), 1.3), Design Notes 25 rows S4-a to S4-d, Design Notes 32.
3. docs/sketches/s3_spec.yaml (section convention, section_class, hatch, not_drawn bands), s1_spec.yaml, check_stack.py, sketch_common.py (section view), checks_s3.py (structure to follow), proposed_params.yaml, build_parts/holder.py, tests/test_params_bom.py l.694-718.

TASK: Requirements 1 to 6.
Output sections: Corrections to the brief; 1 overlay changes (key, old, new, source, status) and the --stale list; 2 spec summary (rows, shared rows, S4-only rows, neighbours, predicates, not_drawn, reported_items); 3 checks_s4.py skeleton; 4 stack table with hand values; 5 S1 (S3) spec edits; 6 X1 result; 7 open items for the sign-offs; 8 Gameplan lines to change (at least detail 1.4 Script, Spec and check rows per the ruling; Echo Site Registry rows for any new value).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_engineer_spec.md
Return in context only: row counts, shared rows X1 result, --stale adopted-key list, stack hand-check result, open items (under 8 lines).
```

### P3a. The Designer (spawn A), 1.4 (b) spec sign-off (parallel with P3b)

Spawn: agent; background recommended. Scratch id `p3a`. Loop cap: one FIX list; one re-sign (P2r).

```
[BLOCK DES]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p3a\
Step 1.4 (b) sign-off of docs/sketches/s4_spec.yaml and the S1 r9 (S3 r8) holder spec edits, against your params review and Sean's STOP S4-A rulings.

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_spec.md; docs/sketches/s4_spec.yaml; the S1 (S3) spec diffs it lists.
2. research/sean/cr_scratch/step1.4_designer_params_review.md; research/sean/gameplan.md Design Notes (the STOP S4-A entry), detail 1 common (b).

TASK:
1. Part list: every part a shape string names has a row or a not_drawn entry with its reason; the figure note names each not-drawn part head. Count rows, not_drawn, missing.
2. Shape notes, ticks, options and alternates drawn as ruled; operator rows; rubric additions; reported_items cover DC13 (100 mm core against the collar top and min_exposed, minimum core length, advance per slice, collet options with the collar-top move, sacrificial option, cut-case seat).
3. Any value or field setting you change carries its harness dry run (run in D:\Unleashed Robotics\_scratch\cutjig\open14\p3a\ws).
Verdict: SIGNED, or FIX items numbered.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_designer_spec_signoff.md
Return in context only: verdict, part-list counts, FIX count (under 5 lines).
```

### P3b. The Loftsman, 1.4 (b) spec sign-off (parallel with P3a; after STOP S4-0)

Spawn: agent; background recommended. Scratch id `p3b`. Loop cap: one FIX list; one re-sign (P2r). Under STOP S4-0 option C, TASK 1 to 3 shrink to the S1 r9 changed rows.

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p3b\
Step 1.4 (b) sign-off of the S4 spec arithmetic and placement and of the S1 r9 (S3 r8) holder rows.

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_spec.md; docs/sketches/s4_spec.yaml; the S1 (S3) spec diffs.
2. params.yaml (stop, holder, receiver, nut, collar, washer, seat, witness, chain, cone, collet blocks), docs/sketches/proposed_params.yaml, build_parts/holder.py, receiver.py, collet_family.py, tests/test_params_bom.py l.694-718.

TASK:
1. Hand values beside the check_stack values: collar top 159.84 by the test_P18 formula; holder section coordinates from holder.py (OD 67.04, cone 62.04 to 56.75 over chain.H 30, bore 56.75); spigot radial gap 0.20 against g_min 0.10; nut-plate top; 100 mm core top; minimum core length on the stop with the ruled min_exposed datum; the advance path extent for the drawn option.
2. Shared rows equal to S1/S3 (X1); S4-only rows carry no expression that disagrees with a shared row; every DERIVED overlay leaf added has expr.
3. S4-2 in the ruled form tests what the ruling says, with a premise you can state.
Verdict: SIGNED, or FIX items numbered, each with the hand value and the code value.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_loftsman_spec_signoff.md
Return in context only: verdict, hand-value mismatches, FIX count (under 5 lines).
```

---

### P4. The Engineer, 1.4 (c) red-first

Spawn: background **required**. Scratch id `p4`. Loop cap: one fix pass (P5f) after P5, P5T and P5L; one re-check (P5r).

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p4\
Step 1.4 (c), red-first, on the signed s4_spec.yaml. Rulings: [orchestrator: paste the STOP S4-A Design Note text verbatim].
Requirements:
1. S4-x fixtures from the signed spec (fixtures/s4_fixtures.py; manifest rows with reason substrings and planted counts): S4-1 Z live params, B holder.flange_thickness dropped (151.84); S4-2 in the ruled form, with a Z and a B per branch; S4-3 Z correct sense, B collet flipped end for end, plus a B per predicate (wing nut below the holder; washer outside nut and holder; receiver floor on top; core inverted); S4-d if adopted.
2. A section-view tick admission rule for its class (any row with a declared tick form in a section view: collet slits, receiver thread), premise stated, with a Z and a B per branch (undeclared ticks; a tick outside the row's drawn pieces; a solid tick where dashed is declared; the wrong tick count).
3. If ruled: section_xz generalisation of SECTION_VIEWS (convention, look sign, section_u K7, hatch_split, rule (l)) with a Z and a B per rule; X1 compares `section` (plus depth and bore_cone) on shared rows with a Z and a B (expected to fire on the holder between S4 and S1 r8 until S1 r9; record the expected red).
4. docs/sketches/stubs/s4_stub.py; check_sketch.py s4 --rev 0 red by cause on every content check, guards labelled; check_sketch.py --baseline s4.
5. --controls full (counts and wall) and --controls --fast.
Every new B is red on the pre-change code.

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_spec.md (and fixes), step1.4_designer_spec_signoff.md, step1.4_loftsman_spec_signoff.md.
2. docs/sketches/s4_spec.yaml, checks_s4.py, check_sketch.py, sketch_common.py (section view, K5 sub-artist admissions, K8 section convention), fixtures/s3_fixtures.py (pattern), fixtures/manifest.yaml, stubs/s3_stub.py.
3. research/sean/gameplan.md detail 1 common (c), detail 1.0 red-first baseline paragraph.

TASK: Requirements 1 to 5.
Output sections: Corrections to the brief; 1 files changed; 2 control table (ID, planted, reason substring, red on pre-change code, result); 3 tick admission rule and premise; 4 section_xz / X1 section (if ruled); 5 s4 --rev 0 table (check, result, cause); 6 baseline; 7 controls counts and wall; 8 rules awaiting signature and their raisers; 9 Gameplan lines to change (at least detail 1.4 check rows S4-1 to S4-3 in the ruled form; K5 row tick admission; K table control pointer; X1 row if extended).
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_engineer_redfirst.md
Return in context only: controls count and wall (full, fast), s4 --rev 0 red-by-cause count, rules awaiting signature (under 6 lines).
```

### P5. The Software Engineer, 1.4 (c) check (parallel with P5T, P5L)

Spawn: background **required**. Scratch id `p5`. Loop cap: one FIX list; one re-check (P5r).

```
[BLOCK SWE]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p5\
Step 1.4 (c) check: the S4-x fixtures, the tick admission rule, section_xz and X1 section if ruled, the s4 stub run and baseline, and the harness delta since your step 0 check (P0f onward).

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_redfirst.md; step1.4_software_engineer_step0_check.md (your step 0 file) and any re-check.
2. docs/sketches/checks_s4.py, s4_spec.yaml, stubs/s4_stub.py, fixtures/s4_fixtures.py, fixtures/manifest.yaml, check_sketch.py, sketch_common.py, wip/s4_checks_r0.json, wip/baseline_red.json.
3. method/tdd_method.md Principles 9 and 10.

TASK:
1. Every branch of S4-1 to S4-3 and of each new rule has its own B; delete a branch in a scratch copy for at least two and confirm a B goes red.
2. s4 --rev 0: reds labelled by cause; absent reds count only where a content B exists; guards labelled.
3. The fast tier still covers every family after the S4 controls; full set wall against 200 s.
4. Ceremony check: any control or rule that costs more than it protects, with reason.
Verdict per item: PASS or FIX.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_software_engineer_check.md
Return in context only: verdict, FIX count, controls wall (under 4 lines).
```

### P5T. The Topologist, 1.4 (c) sense and admissions (parallel with P5, P5L; after STOP S4-0)

Spawn: agent; background recommended. Scratch id `p5t`. Loop cap: one FIX list; one re-check (P5r).

```
[BLOCK TOP]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p5t\
Step 1.4 (c): the S4-3 orientation predicates as sign checks, the section look sign on the S4 plane (and section_xz if generalised), the tick admission rule, and S4-d if adopted.

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_redfirst.md; docs/sketches/s4_spec.yaml (sense predicates, section fields), checks_s4.py, sketch_common.py (K8 section convention, K5 admissions), fixtures/s4_fixtures.py; ASSEMBLY.md Coordinate frame and the collet and nut entries.

TASK:
1. Each S4-3 predicate: the sign check and its invariant, re-computed by hand on the fixture; a B that reads clean on the pre-change code is a FIX.
2. Section look sign and handedness on the S4 plane.
3. Tick admission: premise and branches; SIGNED or FIX.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_topologist_redfirst_signoff.md
Return in context only: verdict per item, FIX count (under 4 lines).
```

### P5L. The Loftsman, 1.4 (c) coordinates (parallel with P5, P5T; after STOP S4-0)

Spawn: agent; background recommended. Scratch id `p5l`. Loop cap: one FIX list; one re-check (P5r).

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p5l\
Step 1.4 (c): the S4-1 and S4-2 fixtures against the arithmetic you signed at (b); section coordinates on the S4 plane (and section_xz if generalised); the X1 section extension if ruled.

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_redfirst.md; step1.4_loftsman_spec_signoff.md (your file); docs/sketches/checks_s4.py, fixtures/s4_fixtures.py, s4_spec.yaml, check_stack.py.

TASK:
1. S4-1 B (151.84) and S4-2 B per branch: planted value against the hand value.
2. Section coordinate map (u, z) for two S4 rows by hand.
3. X1 section comparison: what it compares, its tolerance, and the expected red on the holder until S1 r9.
Verdict per item: PASS or FIX.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_loftsman_redfirst_signoff.md
Return in context only: verdict per item, FIX count (under 4 lines).
```

---

### P6. The Engineer, 1.4 (d) draw S4 r1 and S1 r9 (and any triggered S2/S3 revision)

Spawn: background **required**. Scratch id `p6`. One drawn revision per sketch at this stage.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p6\
Step 1.4 (d). Draw S4 r1, and S1 r9 with every trigger at once: the rule (l) firings with the P0D anchors; the S4-b holder rows from the (b) spec edits; X1 section if ruled. Draw S2 r10 / S3 r8 only for: [orchestrator: list the triggers, or "none"].
Requirements:
1. docs/sketches/s4_base_section.py, drawn through the section renderer, convention and placer; outputs to wip/ as s4_base_section_r1.png; iterate to green on K1 to K9, X1, RPT, S4-1 to S4-3 (--only or --fast for iterations; the final run is the full set).
2. S1 r9 to wip/ (four poses); every check green, K4 rule (l) and X1 included. List changed rows with old and new values; every unchanged row is pixel-identical in the regions it occupies.
3. S3-3 dry run on the S1 r9 record: in a scratch copy (D:\Unleashed Robotics\_scratch\cutjig\open14\p6\ws) accept S1 r9 there, run check_sketch.py s3 --rev 7, and report the S3-3 result, the link count and the deps branch output. Nothing is accepted into the live tree.
4. Reported items through RPT in wip/s4_summary_r1.md and wip/s1_summary_r9.md.
5. --controls full at the end; --stale --include-unaccepted.

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_redfirst.md (and fixes); step1.4_designer_params_review.md; step1.4_designer_step0_signoff.md section 3.
2. docs/sketches/s4_spec.yaml, checks_s4.py, s1_spec.yaml, s1_side_poses.py, s3_jackscrew_section.py (section drawing pattern), sketch_common.py, proposed_params.yaml.
3. research/sean/gameplan.md detail 1 common, detail 1.4, Design Notes 13.

TASK: Requirements 1 to 5.
Output sections: Corrections to the brief; 1 files changed; 2 S4 r1 check table; 3 S1 r9 check table and changed-row list; 4 S2/S3 if drawn; 5 S3-3 dry run on S1 r9; 6 reported items; 7 controls and --stale; 8 PNG paths; 9 open items; 10 Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_engineer_draw_r1.md
Return in context only: S4 r1 and S1 r9 check counts, S3-3 dry-run result, controls wall, PNG paths (under 6 lines).
```

### STOP-T5 (non-blocking). Sean: orientation preview

When `docs/sketches/wip/s4_base_section_r1.png` (and `wip/s1_pose_*_r9.png`) first exist, show them to Sean for V1 (floor at the bottom), V3 (collet narrow end and taper sense; wing nut above the holder) and V4 (core upright on the stop), plus V1 to V5 for S1 r9. Sean's words go to Design Notes 13 as `S4-r1` / `S1-r9` and into P9. This is not acceptance.

---

### P7a. The Loftsman, 1.4 (e) cross-review (parallel with P7b and P8; after STOP S4-0)

Spawn: agent; background recommended. Scratch id `p7a`. Loop cap: one FIX list into P9; one re-check (P7r).

```
[BLOCK LOF]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p7a\
Step 1.4 (e), geometry cross-review of S4 r1 and the changed rows of S1 r9 (and S2/S3 if drawn): arithmetic and placement.

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_draw_r1.md.
2. docs/sketches/wip/s4_checks_r1.json, wip/s4_summary_r1.md, wip/s1_checks_r9.json, s4_spec.yaml, s1_spec.yaml, s4_base_section.py, checks_s4.py; wip/s4_base_section_r1.png and wip/s1_pose_load_r9.png (Read as images).

TASK:
1. Re-compute by hand and write next to each JSON value: collar top 159.84; spigot radial gap 0.20; holder section coordinates; nut-plate top; the 100 mm core top and its offset to the collar top; minimum core length on the stop; the advance-path clearance for the drawn option; one K7 pair per class in S4.
2. S1 r9 changed rows: holder section placement, the receiver|holder G 0.25 distance and the collar|holder C contact, each by hand.
3. S3-3 dry run on S1 r9: links unchanged, or listed.
Verdict: PASS, or FIX numbered with hand and code values. A FIX that sets a value carries its dry run.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_loftsman_crossreview.md
Return in context only: verdict, FIX count, hand-value mismatches (under 4 lines).
```

### P7b. The Topologist, 1.4 (e) cross-review (parallel with P7a and P8; after STOP S4-0)

Spawn: agent; background recommended. Scratch id `p7b`. Loop cap: one FIX list into P9; one re-check (P7r).

```
[BLOCK TOP]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p7b\
Step 1.4 (e), orientation and half-space cross-review of S4 r1 and the changed rows of S1 r9 (and S2/S3 if drawn).

READ FIRST:
1. research/sean/cr_scratch/step1.4_engineer_draw_r1.md.
2. docs/sketches/wip/s4_checks_r1.json, wip/s1_checks_r9.json, s4_spec.yaml, s4_base_section.py; wip/s4_base_section_r1.png and wip/s1_pose_load_r9.png (Read as images).

TASK:
1. Each S4-3 predicate re-computed through the transform chain on the drawn patches: collet narrow end and taper sense, wing nut above the holder, washer between nut and holder, receiver floor at the bottom, core upright on the stop.
2. Section convention on the S4 plane: cut hatched by material, beyond and hidden per the renderer clauses; look sign.
3. Ticks admitted as declared.
4. TP-n rows (parts drawn narrower than their footprint) for S4 and S1 r9.
Verdict: PASS, or FIX numbered. A FIX that sets a value carries its dry run.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_topologist_crossreview.md
Return in context only: verdict, FIX count, TP-n rows (under 4 lines).
```

### P8. The Designer, 1.4 (f) M1 visual gate (fresh spawn; parallel with P7a and P7b on r1)

Spawn: **fresh** agent on an image-capable model (the orchestrator's default subagent model; no text-only override). Not spawn A, not spawn B, and not an earlier M1 reviewer in 1.4. Background recommended. Scratch id `p8` (`p8r2`, `p8r3` on later rounds). Before spawning, the orchestrator runs section 5 step 1 for this round and substitutes the control folder path. The orchestrator pastes the block below as it stands, filling [BLOCK DES-M1], [CTX COMMON] and the bracketed substitutions. Loop cap: three fresh rounds (section 1.4).

```
[BLOCK DES-M1]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\[orchestrator: p8 | p8r2 | p8r3]\
Step 1.4 (f), M1 visual gate (LLM-PLM 8.4c). You did not produce these images. You must see pixels: open each PNG with the Read tool. If a Read returns no image content, write your numeric results and the line "visual gate NOT RUN" and stop.
Read only the files listed under READ FIRST. Do not open any other file in docs/sketches/, docs/sketches/wip/, research/ or the D:\Unleashed Robotics\_scratch tree.
Reviewer-model controls: four extra figures in [orchestrator: docs/sketches/wip/m1/r<k>/], named m1c_<token>.png. Two are drill side views: judge each on V1 to V5 below. Two are plan views: judge each on handedness (+X to the right along the slot line, +Y up, theta counter-clockwise from +X seen from +Z). Work out from each figure which kind it is.
Gated here: S4 r[orchestrator: k]; S1 r9 [orchestrator: and S2 r10 / S3 r8 if drawn], each in its own file.

Rubric (every sketch):
V1 Top on top: the floor is at the bottom of every side view; parts that hang (motors, nuts) hang as the spec states.
V2 Spin axis: the drill axis is vertical; the gear section is symmetric about it and the pinion axes are radial, so the drill spins about Z.
V3 Tail off the nose: cutting head and iris at the bottom of the drill; gear and drive where the spec puts them. For S4: collet and nut sense as the spec states (collet narrow end, wing nut above the holder).
V4 Core upright in the collet, bottom on the stop, never inverted.
V5 Screws vertical, anchors at the bottom, guides at the top, nut on the ring.
V6 Projection: cylinders seen from the side are rectangles; circles appear only in plan views and end-view insets.
V7 Each part reads as the part it is (8.4b): ring gear with teeth and pinions, jack screw with nut, anchor and guide, ring structure as a structure, motor as body and shaft; for S4, collet with its slits, holder with its cone and flange, wing nut with wings, receiver with floor, thread and shoulder, washer, core seat.
V8 Labels legible at 100 percent, none overlapping, every labelled feature dimensioned; no leader runs along a gridline, reference line or part edge.
V9 State, from the figure alone, the answer to the spec's question in one sentence; then compare it with the spec question.
V10 The operator can reach and see each task the operator-task rows below assign to this sketch; hands are clear of moving parts in the load pose.
Applicability: S4 V1, V3, V4, V6 to V10. S1 V1 to V10. S2 V2, V6 to V10. S3 V1, V5 to V10. Mark the others N/A.
Operator-task rows for S4 and S1: [orchestrator: paste the operator-task table rows whose Sketch cell names S4 or S1, verbatim from the gameplan as they stand at this spawn].
Sean's corrections so far: [orchestrator: paste the Design Notes 13 rows S4-r1 onward and S1-r9 verbatim, or "none"].
Parts drawn narrower than their footprint (read these at V7): [orchestrator: paste the TP-n rows from step1.4_topologist_crossreview.md, or "none yet" on r1].

READ FIRST:
1. The four control figures in [orchestrator: docs/sketches/wip/m1/r<k>/] (Read each as an image).
2. docs/sketches/wip/s4_base_section_r<k>.png (Read as an image).
3. docs/sketches/s4_spec.yaml (question, rubric_additions, section convention, options and alternates drawn, not_drawn, figure_note).
4. docs/sketches/wip/s4_checks_r<k>.json and wip/s4_summary_r<k>.md.
5. docs/sketches/wip/s1_pose_load_r9.png, s1_pose_start_r9.png, s1_pose_capture_end_r9.png, s1_pose_park_r9.png and docs/sketches/s1_pose_load_r8.png (Read each as an image); docs/sketches/s1_spec.yaml; wip/s1_checks_r9.json.
6. [orchestrator: S2 r10 / S3 r8 PNG, the accepted predecessor PNG, spec and checks JSON, if drawn; otherwise delete this line].

TASK:
1. Controls: one line per control figure (by file name), PASS or FAIL on the criterion that applies, with what you see.
2. S4: one line per applicable rubric item, PASS or FAIL with what you see; one line per S4 rubric addition; whether the section convention reads (cut hatched, beyond in elevation, hidden dashed); whether the advance option, alternates and ticks read as the spec states.
3. V9 for S4: your sentence, then the spec question.
4. S1 r9: V1 to V10 and the S1 rubric additions; what changed against r8 and whether it reads correctly.
5. S2 r10 / S3 r8 if drawn: their applicable items and what changed.
6. Overall PASS per sketch only if every applicable item passes. FAIL items as numbered findings with the feature id. A finding that sets a coordinate or field value states the dry run the Engineer must run.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: docs/sketches/wip/s4_visual_gate_r<k>.md and docs/sketches/wip/s1_visual_gate_r9.md (and docs/sketches/wip/s2_visual_gate_r10.md / s3_visual_gate_r8.md if gated). Each file ends with a section "Gameplan lines to change".
Return in context only: verdict per control figure (by file name), overall verdict and FAIL count per sketch.
```

After P8 returns, the orchestrator runs section 5 steps 2 to 4. No score is put in front of any reviewer.

---

### P9. The Engineer, (h) revision r<k+1>

Spawn: background **required**. Scratch id `p9r<k+1>`. On r1 it runs after P7a, P7b and P8 (and T5) return, producing one revision for all findings. A finding of a class already fixed once goes to the A.4 ruling path (section 1.4) before P9 opens.

```
[BLOCK ENG]

CONTEXT:
[CTX COMMON]
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\[orchestrator: p9r<k+1>]\
Step 1.4 (h): revision r<k+1> of S4 [and S1 r<n+1> / S2 / S3 if a finding applies]. Sources: [orchestrator lists: step1.4_loftsman_crossreview.md, step1.4_topologist_crossreview.md, docs/sketches/wip/s4_visual_gate_r<k>.md, s1_visual_gate_r9.md, Sean's T5 / M2 rows verbatim from Design Notes 13, any orchestrator ruling].
Rule (h): a correction a signed predicate can express becomes a K8 predicate with a B fixture that reproduces the error. A new or relaxed rule states its premise, enforces it with its own Z and B in this revision, covers its whole class in every view (Rule scope), and its raiser signs before M1. A FIX that sets a value, field setting or coordinate is dry-run through the predicate that will judge it before you apply it; one that fails returns to the raiser with the measurement and does not enter the revision.

READ FIRST:
1. research/sean/gameplan.md detail 1 common, Design Notes 13, the STOP S4-A Design Note.
2. Every source file named above.
3. docs/sketches/s4_base_section.py, s4_spec.yaml, checks_s4.py, s1_side_poses.py, s1_spec.yaml, proposed_params.yaml, sketch_common.py, fixtures/manifest.yaml.
4. research/sean/cr_scratch/step1.4_engineer_draw_r1.md (or the previous step1.4_engineer_revision_r<k>.md).

TASK:
1. Per finding: dry-run result where required, fix, K8 predicate ID and B fixture or "visual only", the rule's class scope. A finding that changes a design value or the spec goes to The Designer (spawn A) for re-sign, and for placement to The Loftsman as well. A value change to an S1, S2 or S3 key goes to the orchestrator for Sean.
2. Redraw as r<k+1> to wip/; check_sketch.py s4 --rev <k+1> (and s1, s2, s3 if affected); --controls full at the end; iterate to green.
3. Reported items through RPT.
4. List new rules and their raisers for signature.
Output: Corrections to the brief; table (finding ID, source, dry run, fix, predicate ID or "visual only", B fixture, class scope); check results; PNG paths; rules awaiting signature; Gameplan lines to change.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_engineer_revision_r<k+1>.md
Return in context only: findings closed, findings returned on failed dry run, predicates added, rules awaiting signature, check counts.
```

After P9: P7r (the PR prompt, run by each raiser with an open FIX, output `step1.4_{loftsman|topologist}_recheck_r<k+1>.md`); then P8r (the P8 prompt, a fresh spawn and a new control round per section 5, on r<k+1>). The revision presented at M2 carries a fresh M1 PASS file on its exact pixels, or a pixel-equality statement (SHA-256 or pixel compare) to a revision that has one. Apply the gameplan lines; save point 5; STOP M2.

### STOP M2. Sean: correction pass

Present: `docs/sketches/wip/s4_base_section_r<k>.png`, `wip/s4_visual_gate_r<k>.md`, `wip/s4_summary_r<k>.md`; S1 r9 beside `s1_pose_*_r8.png` with the changed items and `wip/s1_visual_gate_r9.md`; S2/S3 packages if drawn. Sean answers V1, V3, V4 and V9 for S4 (V1 to V5 and V9 for S1 r9), gives free corrections, and picks: the advance option, the collet length (Q5, with Quinn), the sacrificial collet or liner (Q6), and any deferred S4-A item. The orchestrator writes each correction into Design Notes 13 as `S4-r<k>` (or `S1-r9`, ...) with Sean's words, and each pick into Design Notes 13 and the S4-A Design Note, and updates Open Questions Q4, Q5, Q6 and Q10. Corrections send the work back through P9, P7r, P8r and M2. Acceptance is recorded as "S4-r<k> accepted" (and the S1, S2, S3 rows) with the date in Design Notes 13, followed by ORCH-B.

### ORCH-B. Orchestrator after acceptance

1. `check_sketch.py --accept s4 --rev <k> --note "Design Notes 13 S4-r<k>"`; copy-up from wip/ with equality (PNG, checks JSON with deps, summary, visual gate). Copy `wip/s4_checks_r0.json` up as the S4 red-first record.
2. `check_sketch.py --accept s1 --rev 9 --note "Design Notes 13 S1-r9"` (r8 marked superseded); S2/S3 revisions likewise if accepted.
3. `check_sketch.py --stale`: the deps branch reads s3 r7 STALE (certifier S1 r8 superseded). This is the expected branch; record the line.
4. `check_sketch.py s3 --rev 7` (S3-3 on the S1 r9 record; expected 16/16, links as in the P6 dry run), then `check_sketch.py --accept s3 --rev 7 --note "Step 1.4 ORCH-B: refreshed on S1 r9 (deps)"`. If the s3 pixels differ, stop: S3 r8 needs M1 and M2.
5. `check_sketch.py --stale`: 4 records, 0 differences.
6. Apply the remaining gameplan lines; one Progress row per agent return; save point 6 ("sean: Step 1.4 S4 r<k> accepted").

---

### P10. The Manager, Step 1.4 close

Spawn: background **required** (re-runs `--controls`). Scratch id `p10`.

```
SYSTEM: You are The Manager (method/operational_guide.md A.12.1; read it, plus A.4 step 7, A.5.2, A.5.3, A.3.1 Visual gates).

CONTEXT:
[CTX COMMON] (The Manager may edit research/sean/gameplan.md and research/sean/accumulator.md.)
Scratch folder for this spawn: D:\Unleashed Robotics\_scratch\cutjig\open14\p10\

READ FIRST:
1. research/sean/cr_scratch/step1.4_manager_open.md sections 0 to 2, 4 and 6 (findings F4-1 to F4-16, done criteria DC1 to DC15, the revision rule, blockers, open edits). Section 5 holds no key; the key files are outside the tree and you read them only to confirm the recorded scores.
2. Every research/sean/cr_scratch/step1.4_*.md file; docs/sketches/s4_visual_gate_r<k>.md, s4_checks_r<k>.json, s4_summary_r<k>.md, s4_checks_r0.json, and the S1 r9 (S2, S3) equivalents accepted in 1.4; the Progress Log rows recording the control scores.
3. research/sean/gameplan.md Steps rows 1 and 1.4, detail 1 common, detail 1.0 (K table, check_sketch.py bullet), detail 1.4, Design Notes 8, 13, 25 and the 1.4 entries, Context Recipes, Progress Log, Echo Site Registry, Open Questions Q4, Q5, Q6, Q10, N5.
4. research/sean/accumulator.md (sections of the personas that ran).

TASK:
1. Verify DC1 to DC15 with evidence. Re-run from docs/sketches/: check_sketch.py --controls (default jobs; wall against 200 s), --controls --fast, check_sketch.py s4 --rev <k>, s3 --rev <7 or 8>, s2 --rev <9 or 10>, s1 --rev 9, --stale. Confirm the runs leave committed files unchanged (SHA-256 before and after). C: free space against 6.22 GB at the open.
2. Audit each agent's "Gameplan lines to change": applied at the save point after it, in the numbered Old/New format, unmatched Olds rewritten or marked superseded; every agent return (fresh M1 returns included) has its own Progress row; list misses and duplicates.
3. Control-blinding audit: no reviewer prompt and no file a reviewer read stated an expected control outcome; fresh tokens each round; scores recorded from the out-of-tree key; the credit earned.
4. Disposition of each finding F4-1 to F4-16 (closed with evidence, or carried with step and owner).
5. Sequencing check for 1.5 (S6): any check cited before the step that writes it (S6-1 to S6-5, S6-a, S6-b, N1, gear, pinion and cutter ticks, the S3-3 ring-bearing-tube segment S6-5 draws, Design Notes 25 TP-n).
6. Process: revisions and their causes, system or one-off; did class-scoped rules and the A.4 ruling path stop instance loops; controls time per run across the step.
7. Gameplan close edits: Steps rows 1 and 1.4, Current step, Progress Log, Design Notes 25 rows closed (S4-a to S4-d, C1.3-a, C1.3-b), Echo Site Registry (collar top, collet length, advance, receiver spigot, holder section), Open Questions Q4, Q5, Q6, Q10.
8. Accumulator entries for every persona that ran and for The Manager.
9. Decisions for Sean at the inter-step gate.
Verdict: READY FOR SEAN or NOT READY with items.
Respond in character, but be direct. The Joe Friday approach, "just the facts, ma'am." If you see a problem, say so.
CRITICAL FILE RULE: Begin writing immediately to the target markdown file path. Do not include introductory boilerplate, structural meta-commentary, or disclaimers at the top of the file. Start directly with the first functional heading.

WRITE YOUR OUTPUT TO: research/sean/cr_scratch/step1.4_manager_close.md
Return in context only: verdict, DC criteria met count, decisions for Sean (under 10 lines).
```

## 4. Blockers

| # | Blocker | Effect | Resolution |
|---|---|---|---|
| B1 | Control key reachable by four routes; a fixed re-letter rebuilds it (F4-1) | Any M1 run before the fix earns no model credit | P0 R3 (`--m1-controls`, key outside the tree), [BLOCK DES-M1], self-contained P8, gameplan l.195-196 edit. No M1 runs before ORCH-A |
| B2 | `--stale` blind to certifier records, spec and script (F4-2) | S1 r9 would leave S3 r7 "clean" on a changed certifier | P0 R2; S3 r7 re-recorded at ORCH-A; ORCH-B re-runs s3 after `--accept s1 --rev 9` |
| B3 | S4-2 red by construction on the kept receiver; detail 1.4 assumes a push from below (F4-7) | S4 cannot be accepted as the check stands | P1 options; STOP S4-A item 2; P4 implements the ruled form; a floor change goes to Quinn (batch 3) |
| B4 | Section plane unstated; only section_yz carries the section machinery (F4-9) | Stub and draw cannot run on another plane | STOP S4-A item 1; P4 generalises with a Z and a B per rule if section_xz |
| B5 | Holder row in S1 and S3; X1 blind to `section` (F4-4) | True and stand-in holder sections would coexist under one id | STOP S4-A item 5; P4 X1 extension if ruled; P6 S1 r9 (S3 r8) |
| B6 | Spigot and plate-hole break against shared rows (F4-5) | X1 fails, or the spigot cannot be drawn | P1 row split; P2; P3b |
| B7 | Roster: no geometry cross-review assigned (F4-10) | S4 placement unreviewed | STOP S4-0 |
| B8 | Controls 229.0 s, about 260 s projected with S4 (F4-11) | Every run of record over target | P0 R1; P0S rules pruning |
| B9 | Collet length moves the whole height chain (F4-8) | Adopting a value reopens S1, S2, S3 | STOP S4-A item 3 (alternate outline recommended) |
| B10 | Batch 1 and batch 2 unanswered (Q2, Q9, N5, N7, N10; B2-1 to B2-10) | Heights, masses and kept-part forces stay ASSUMED | None for 1.4; reported |
| B11 | Rule (l) turns accepted S1 r8 K4 red (F4-3) | S1 r8 cannot be re-recorded at ORCH-A | Expected. S1 r8 stays on its legacy record (exempt by name) until S1 r9. S3-3 reads S1 K7 entries, not K4, so the S3 certification is unaffected |

Not a blocker: the `ring.nut_mounting` text fix (F4-12). Not a blocker either: "the next sketch opens only after acceptance", which governs S6 (1.5), opening after S4 and every S1/S2/S3 revision opened in 1.4 are accepted.

## 5. Orchestrator only: M1 control rounds and scoring

This section is never pasted into a spawn, and no spawn prompt points to it. It holds no mapping and no expected verdict; those exist only in each round's key file, outside the project tree.

1. **Before each M1 round k (P8, P8r):** set TMP and TEMP to `D:\Unleashed Robotics\_scratch\cutjig\tmp`, then from `docs/sketches/` run `python check_sketch.py --m1-controls --out wip/m1/r<k> --key "D:\Unleashed Robotics\_scratch\cutjig\open14\orch\m1key_r<k>.json"`. Check that `wip/m1/r<k>/` holds exactly four PNG files and nothing else. Substitute the folder path, and only that path, into P8. The key path goes into no spawn.
2. **After P8 returns:** open the key file and compare each control verdict (by file name) with the key. All four must match.
3. **On any mismatch:** the reviewer model earns no credit in this round, and the round's sketch verdicts do not count. Replace the reviewer (a new fresh spawn; if the default image-capable model fails twice, stop and report to Sean), generate a new round (step 1 with folder `r<k>b` and a new key file), and re-run P8.
4. **Record:** after the reviewer has returned, append to each gate file of the round the footer "Orchestrator: score the controls against the key (orchestrator only); <n>/4 matched; round r<k>; key file outside the tree." Write the same in the round's Progress row. No later reviewer reads an earlier gate file (P8 READ FIRST), and every round has fresh tokens, so an earlier key says nothing about a later round.
5. **Class repeats** (section 1.4 A.4 ruling path): the ruling, the class and the specialist assigned go in the Progress Log and, for a flat ruling, a Design Note.

## 6. Gameplan lines to change (orchestrator, at the open save point)

Format as in [CTX COMMON]. Where a line is long, Old holds a fragment of it that is unique in the gameplan at this open; replace that fragment only. Items 6, 7, 8 and 9 are filled or applied when Sean answers the stop they name.

1. Header, l.12.
Old:
```
**Current step:** 1.4 (S4) approved to open (Step 1.3 approved by Sean 2026-11-27, gate decisions G1 to G6; research/sean/cr_scratch/step1.3_manager_close.md)
```
New:
```
**Current step:** 1.4 (S4) in progress (opened 2026-11-27, research/sean/cr_scratch/step1.4_manager_open.md)
```

2. Steps row 1, status cell (fragment).
Old:
```
In progress: 1.0, 1.1 (S1), 1.2 (S2) and 1.3 (S3) complete |
```
New:
```
In progress: 1.0, 1.1 (S1), 1.2 (S2) and 1.3 (S3) complete; 1.4 (S4) open |
```

3. Steps row 1.3, status cell end (fragment).
Old:
```
Carried items in Design Notes 25 (C1.3-a, C1.3-b). Awaiting Sean |
```
New:
```
Carried items in Design Notes 25 (C1.3-a, C1.3-b). Approved by Sean 2026-11-27 (gate decisions G1 to G6, Progress Log) |
```

4. Steps row 1.4, TDD-stage and status cells (fragment).
Old:
```
| as row 1; checks K1 to K9, S4-1 to S4-3 | Not started |
```
New:
```
| as row 1; checks K1 to K9, X1, RPT, S4-1 to S4-3 | In progress (opened 2026-11-27, research/sean/cr_scratch/step1.4_manager_open.md): STOP S4-0, step 0 (G2 to G5, C1.3-a to -c) with (a), STOP S4-A, (b) to (h); S1 r9 inside 1.4 (G3); S2/S3 revisions only if triggered |
```

5. Detail 1 common, M1 paragraph, the "Controls, once per reviewer model" line (l.195).
Old:
```
Controls, once per reviewer model at the first gate (1.1): the reviewer also receives the K8 Z fixture figure and the K8 B1 figure (drill tip-up), unlabelled. Z must pass; B1 must fail V3. If B1 passes, the reviewer model is replaced before any sketch is gated.
```
New:
```
Controls, every M1 round (from 1.4): the reviewer also receives four unlabelled control figures (two side views, two plan views) with known verdicts, drawn by `check_sketch.py --m1-controls` under fresh random file names for that round; the reviewer judges the side views on V1 to V5 and the plan views on handedness. The orchestrator scores the verdicts against the round's key, which lives outside the project tree; a mismatch replaces the reviewer model before any sketch verdict of that round counts.
```

5b. Detail 1 common, "Control blinding" line (l.196).
Old:
```
Control blinding (Manager, 1.3 close; for Sean at the 1.3 gate): the expected control outcomes live only in `key.json` and in an orchestrator-only section of the open file that no reviewer prompt points to; the M1 spawn receives the prompt text itself, never a line range of the open file. The 1.1 to 1.3 open files print the mapping (ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS, ctrl_d FAIL), so S4 step 0 re-letters the control figures under a new `key.json` (orchestrator only) before the first S4 M1; until then a control result read with the key in view earns no model credit (Step 1.3: control credit void, sketch verdicts stand).
```
New:
```
Control blinding (Manager, 1.3 close; Sean, Step 1.3 gate G2; mechanism at the 1.4 open, research/sean/cr_scratch/step1.4_manager_open.md F4-1): no reviewer prompt, persona block or file a reviewer is pointed to states an expected control outcome. Each round's key is written by `--m1-controls` outside the project tree and read only by the orchestrator; the M1 spawn receives its prompt text pasted in full (rubric included), never a line range of the open file or the gameplan, and its persona block carries no control history. Step 1.3: control credit void, sketch verdicts stand.
```

6. (Applied only if Sean picks A or B at STOP S4-0.) Steps row 1.4, Assigned To cell. Old is item 4's base row text:
Old:
```
| The Engineer, The Designer, Sean | as row 1; checks K1 to K9, X1, RPT, S4-1 to S4-3 |
```
New (A):
```
| The Engineer, The Designer, The Loftsman and The Topologist (geometry cross-review, STOP S4-0), The Software Engineer (step 0 and (c)), Sean | as row 1; checks K1 to K9, X1, RPT, S4-1 to S4-3 |
```
New (B): the same with "The Topologist ((c) and (e), STOP S4-0)" in place of "The Loftsman and The Topologist (geometry cross-review, STOP S4-0)".

6b. (A or B.) Detail 1.4, Cross-review line.
Old:
```
Cross-review: none required (no new placement computed); The Designer reviews the kept parts as drawn.
```
New (A):
```
Cross-review (STOP S4-0, Design Notes 33): The Loftsman (base-stack arithmetic, holder section, spigot radial fit, advance path; (b), (c), (e)), The Topologist (kept-part orientation predicates, section sense, tick admission; (c), (e)); S1 r9 changed rows by both at (e); The Designer reviews the kept parts as drawn.
```
New (B): "Cross-review (STOP S4-0, Design Notes 33): The Topologist ((c), (e)); S1 r9 changed rows by The Loftsman and The Topologist at (e); The Designer reviews the kept parts as drawn."

7. (Applied only if Sean picks A.) Design Notes 8, last sentence (fragment).
Old:
```
The Loftsman on arithmetic and placement, The Topologist on orientation and sense. S4 and S5 compute no new placement.
```
New:
```
The Loftsman on arithmetic and placement, The Topologist on orientation and sense. S5 computes no new placement. S4 does (holder section, spigot fit, plate-hole break, advance path) and carries both from Step 1.4 (Design Notes 33).
```

7b. (A.) Context Recipes, geometry cross-review row.
Old:
```
| 1.1 (S1), 1.2 (S2), 1.3 (S3), 1.5 (S6) | The Loftsman, The Topologist | the sketch script, sN_spec.yaml, sN_checks_r<k>.json, params and overlay keys it reads, ASSEMBLY.md Coordinate frame, the sub-step's check table |
```
New:
```
| 1.1 (S1), 1.2 (S2), 1.3 (S3), 1.4 (S4), 1.5 (S6) | The Loftsman, The Topologist | the sketch script, sN_spec.yaml, sN_checks_r<k>.json, params and overlay keys it reads, ASSEMBLY.md Coordinate frame, the sub-step's check table; at 1.4 also build_parts/holder.py, receiver.py, collet_family.py |
```

8. Design Notes, new entry after 32 (filled at STOP S4-0).
Insert after (line beginning; unique):
```
**32. Receiver seat (Sean, 2026-11-26, Loftsman 1.3 (c) finding F1).**
```
New:
```
**33. Step 1.4 review roster (Sean, <date>, STOP S4-0: "<Sean's words>").** <option picked, as worded in research/sean/cr_scratch/step1.4_manager_open.md section 2>. Under A or B this supersedes the last sentence of Design Notes 8 for S4.
```

9. Design Notes, new entry after 33 (filled at STOP S4-A).
Insert after: the item 8 New line.
New:
```
**34. Step 1.4 STOP S4-A rulings (Sean, <date>, on `research/sean/cr_scratch/step1.4_designer_params_review.md`).**
```
followed by one bullet per STOP S4-A item with Sean's words (plane; advance option and S4-2 form; collet length; sacrificial option; holder scope and X1 section; values moving S1/S2/S3 keys; rule (l) firings and revisions; batch 3; S4-c and S4-d).

10. Context Recipes, M1 row.
Old:
```
| 1.1 (S1) to 1.6 (S5) | The Designer (M1 visual gate, image-capable model) | the PNGs, sN_spec.yaml, the M1 rubric (detail 1) with the applicability line, the operator-task table, sN_checks_r<k>.json, sN_summary_r<k>.md, Design Notes 13; at 1.1 (S1) also the K8 Z and B1 fixture figures, unlabelled |
```
New:
```
| 1.1 (S1) to 1.6 (S5) | The Designer (M1 visual gate, image-capable model, fresh spawn) | the prompt text pasted in full: rubric V1 to V10 with the applicability line, the operator-task rows for the sketch, the Design Notes 13 rows for the sketch; the PNGs, sN_spec.yaml, sN_checks_r<k>.json, sN_summary_r<k>.md, and the round's four control figures from `--m1-controls`; no key, no earlier gate file, no line range of the open file or the gameplan (from 1.4) |
```

11. Detail 1.4, Back-edge line.
Old:
```
Back-edge: a taller collet (Q5) moves `stop.collar_top_z` and every S1 height; step (i) re-runs S1.
```
New:
```
Back-edge: a taller collet (Q5) moves `stop.collar_top_z`, and with it `stop.height_z`, every S1 pose, the S3 capture_end pose, the S2 hand-band heights and the zero-margin identities (S1-4 0.84, drill_head|collar 25.000); step (i) re-runs S1, S2 and S3 (Manager 1.3 close S4-Q4).
```

12. Detail 1.4, insertion.
Insert after: the item 11 New line.
New:
```
Sequenced at the 1.4 open (`research/sean/cr_scratch/step1.4_manager_open.md` section 1.1): step 0 (P0) carries G4 (per-control times, fast tier, pruning ruled by The Software Engineer), G5 with its class (record deps: certifier records, spec, script; a --stale deps branch; S3 r7 re-recorded at ORCH-A), G2 control blinding (`--m1-controls`, fresh tokens per round, key outside the tree), K4 rule (l) over its class (reference lines, gridlines, part edges; side, plan, section) with a dry run on S1 r8, S2 r9 and S3 r7, C1.3-b and C1.3-c; (a) carries S4-a (S4-only spigot row and plate-hole break under X1), S4-b (holder.py section; S1 r9, and S3 r8 if ruled), S4-c, S4-d, the collet-slit and receiver-thread ticks, the section plane, and the advance, collet-length and sacrificial options for STOP S4-A. Q10 at the open (DERIVED): a 100 mm core on the core stop tops out 17.34 below the collar top; exposure needs at least 253.71 of core on the stop (nut-plate datum). S4-2 as written is red on the kept receiver; its form goes to Sean at STOP S4-A.
```

13. Progress Log, insertion.
Insert after (line beginning; unique):
```
| 1.3 | 2026-11-27 | Approved by Sean ("I as Sean approve G1 through G6"
```
New:
```
| 1.4 | 2026-11-27 | Opened by Manager (research/sean/cr_scratch/step1.4_manager_open.md): done criteria DC1 to DC15; sequence STOP S4-0 (roster, asked at open), P0 step 0 with P1 (a), P0S/P0D/P0T/P0L, P0f, ORCH-A (S3 r7 re-recorded with deps), STOP S4-A, P2 to P10; findings F4-1 to F4-16 (four control-key routes, incl. the Designer SESSION HISTORY in the 1.3 M1 prompts and key.json beside the PNGs; --stale blind to certifier records, spec and script; rule (l) not dry-run on S2 or on side/plan part edges; holder row in S1 and S3 with X1 blind to section; S4-a under X1; 100 mm core 17.34 below the collar top, 253.71 minimum on the stop; S4-2 red by construction on the kept receiver; Q5 back-edge; section plane; roster; controls 229.0 s; ring.nut_mounting in no keys_read). Next: STOP S4-0 with P0 and P1. |
```
