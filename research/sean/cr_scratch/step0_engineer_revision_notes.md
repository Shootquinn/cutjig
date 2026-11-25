# Step 0 Engineer Revision Notes

Gameplan revised: research/sean/gameplan.md. Header, "Start here (from Quinn, 2026-11-24)" and "Repository Sync" byte-compared against the pre-revision copy: identical. Software Engineer TDD content kept; every changed or added check carries Z, B and a source tag.

Counts: 33 findings. APPLIED 33 (SE 18, Designer 15). REJECTED 0 findings; 1 sub-item rejected (D3, sending the citation to Quinn). RECORDED 0. SE-14 and D3 applied with a corrected premise (see INSITU2 below).

## Blocks: owners

- **SE-1, drill-to-ring interface.** Owned by: S6 feature "drill-to-ring bearing" (`bearing.*` overlay), check S6-5 (up-thrust chain off the pinion teeth; B: bearing removed), S6 reported pinion and bearing forces, Open Question N4 (owner Sean), Step 2 bearing row. Mechanics not solved here.
- **SE-2, axial load loop.** Owned by: check S3-3 (cut-case loop through core, collet, receiver, base, frame, anchors, screws, nuts, ring, bearing, drill; B: anchor member 1 mm clear of the base frame), S3 reported kept-part forces at 1000 N and at stall thrust, Design Notes 16, Open Question N5 (owner Quinn, batch 1; Sean confirms at Step 2), A2d and the ASSEMBLY.md descent bullet on the 4a list.

## Disposition table

| ID | Reviewer | Sev | Disp | Gameplan location | Reason |
|---|---|---|---|---|---|
| SE-1 | SysEng | BLOCKS | APPLIED | 1.0 overlay `bearing.*`; 1.5 (S6) Shows, S6-5, Reported; N4; detail 2 row | Bearing is the central interface; now a feature, a check, an owner |
| SE-2 | SysEng | BLOCKS | APPLIED | 1.3 (S3) S3-3, stall case, Reported; 1.1 Shows; 4a A2d and Load path; DN16; N5 | Loop owned by a check with controls and a Quinn ruling |
| SE-3 | SysEng | FIX | APPLIED | 1.1 pose table and lift stroke; 1.3 L formula; S1 Reported per Q9; Echo row | Stroke and travel are different quantities |
| SE-4 | SysEng | FIX | APPLIED | detail 2 descent-end row; 1.1 Shows; DN2 status line; 4a fixed dispositions; N7 | DECLARED key retires only on Sean's ruling |
| SE-5 | SysEng | FIX | APPLIED | S6-3 chain through base and core; S6 Reported torque vs 10 N m; 4a `icd.torque_reaction` REWRITE; DN11 | Floor friction is no member |
| SE-6 | SysEng | FIX | APPLIED | N2 renamed; S3 nut mounting sets K; S2 and S6 guide member; Step 2 guidance row (R13); S2-4 note; DN11 | Guidance is architecture |
| SE-7 | SysEng | FIX | APPLIED | 1.0 checks JSON hashes and `--stale`; detail 1 step (i); back-edges in 1.4, 1.5; X2-5; detail 6 | Fires on a real back-edge |
| SE-8 | SysEng | FIX | APPLIED | Steps order; detail 2 rows and objective; 1.6 after Step 2; DN5; step (h) picks | One decision locus |
| SE-9 | SysEng | FIX | APPLIED | 1.0 batch 1 paragraph; Steps row 1.0; detail 3 closeout; Q2, Q9, N5 to N9 | Start here says ask early |
| SE-10 | SysEng | FIX | APPLIED | Steps 4a/4b, 5, 4c, 6; detail 4; 5.1 S tests "proposed"; Objective 7; DN15 T4 | Sean leads, Quinn reviews a proposal |
| SE-11 | SysEng | FIX | APPLIED | DN7 harness moves at first acceptance; 4c deletes promoted overlay keys; detail 6 | Quinn must be able to fix what he pulls |
| SE-12 | SysEng | FIX | APPLIED | S1 Reported COM and tip force; S2 Reported footprint; Step 2 bolt-down row | R1 free-standing needs a number |
| SE-13 | SysEng | FIX | APPLIED | 4a cross-contributor item N8; batch 1; 4c holds ICD edits until Quinn rules | Two authorities would disagree |
| SE-14 | SysEng | FIX | APPLIED | Document Structure row; DN23-e | Citation corrected; premise corrected, see below |
| SE-15 | SysEng | FIX | APPLIED | K7 swept case, Z4, B4 | Transit collision is plausible |
| SE-16 | SysEng | NOTE | APPLIED | detail 2 sync row; 1.3 Sync line | Folded into the sync row |
| SE-17 | SysEng | NOTE | APPLIED | detail 1 step (d') | Earlier human look, no check bypassed |
| SE-18 | SysEng | NOTE | APPLIED | Progress Log row 0 | Updated now; Manager updates again at close |
| D1 | Designer | FIX | APPLIED | Objectives governing line | Start here stays byte-identical |
| D2 | Designer | FIX | APPLIED | Progress Log row 0 | Same as SE-18 |
| D3 | Designer | FIX | APPLIED (sub-item rejected) | Document Structure row; DN23-e | Range is traced; nothing to send Quinn |
| D4 | Designer | FIX | APPLIED | 1.0 overlay `drill.head_*`, `drill.top_block_*`; S1, S6 Shows; K8 seed; DN14; Echo cutter OD row | Symmetric rectangle defeats V3 and K8 B1 |
| D5 | Designer | FIX | APPLIED | S1-5a, S1-5b; g_min seeds; `drill.bore_ceiling_z` | Old pair could not touch |
| D6 | Designer | FIX | APPLIED | 1.1 pose table | z_rule needs a pose definition |
| D7 | Designer | FIX | APPLIED | 1.0 `ring.*` functional features; Designer fails a ring seed lacking any | 8.4a placeholder rule |
| D8 | Designer | FIX | APPLIED | Step 2 hold, hard stop, homing rows; S3 lead and hold device; 4a fixed dispositions; N7 | Power-off hold over the operator's hands |
| D9 | Designer | FIX | APPLIED | operator-task table; V10; N6 captured-core removal (Quinn) | Operator view was a sector only |
| D10 | Designer | FIX | APPLIED | S4-3 orientation predicates, B collet flipped | Backcap failure class |
| D11 | Designer | NOTE | APPLIED | "1.5 (S6)", "1.6 (S5)" labels in Steps, recipes, DN5 | Removes the S5/S6 trap |
| D12 | Designer | NOTE | APPLIED | Echo Site Registry: T8 wording, stroke, cutter OD, core masses, 0.75 m, 534.93, start z, footprint, stock, 10 N m | Values used three or more times |
| D13 | Designer | NOTE | APPLIED | 1.0 `sN_summary_r<k>.md`; M2 | Author and path named |
| D14 | Designer | NOTE | APPLIED | detail 1 rubric applicability line; 1.6 | No invented results |
| D15 | Designer | NOTE | APPLIED | DN4; 1.3 plan inset | Meets critical-path 15 wording |

**INSITU2 citation.** `context/literature/INSITU2_text.md` is an excerpt file of 11 lines; its line 7 is the row for source lines 157-166 of the original INSITU2 text (iris closed through a braked planetary sun gear driven by the drill drivetrain). "INSITU2 157-166" in Quinn's DN23 refers to the original's lines and is TRACED through the excerpt. Both reviewers read the range as lines of the excerpt file. Gameplan now cites "INSITU2 157-166, excerpted at `context/literature/INSITU2_text.md` line 7, via Quinn DN23". The D3 request to put a discrepancy to Quinn is rejected: there is none.

## Tension rulings (Software Engineer vs Systems Engineer; Design Notes 15)

- T1 Swept K7 case added inside the one K7 implementation (no second overlap code).
- T2 Provenance hashes and `--stale` kept: they fire on a known back-edge.
- T3 Sketch M2 decides, Step 2 consolidates, Step 2 before S5; Step 2 script keeps cross-file checks only (X2-1 to X2-5).
- T4 Shared-file execution (4c) after Quinn's review of the Step 5 record.
- T5 Orientation preview (V1 to V5) added; spec sign-off and red-first still precede drawing.
- T6 New chain checks S3-3, S6-5, rewritten S6-3 kept: each B reproduces a plausible defect.
- T7 Systems Engineer quantities (stroke and L per Q9, tip force, kept-part forces, drill torque vs 10 N m, pinion forces) are reported values, no threshold, each tied to a named decision.

## Decisions for Sean at the Step 0 gate

1. lit_review flag (N3): stays `no`, or `yes` (Quinn's plan has `yes`).
2. S3 redefinition (DN4): one-screw section plus three-screw plan inset with sync loop.
3. Shared location for accepted sketches (DN7): `docs/sketches/`, with the harness and overlay moving there at S1 acceptance.
4. Drawing order and decision locus (DN5): S1, S2, S3, S4, S6, Step 2, S5; options picked at each M2.
5. Change-list execution after Quinn's review (DN15 T4), or execution before it, recorded.
6. Base carries the cut reaction (DN16): confirm the framing and that it goes to Quinn in batch 1 (N5).
7. Batch 1 to Quinn pushed at 1.0 open (contents in detail 1.0: Q2 with cutter OD, Q9, DN23-a to -e, N5 to N9).
8. Week-close record as prose with TDD sub-steps (DN9), or a table-only record.
9. Proposed-keys overlay, params.yaml untouched until 4c (DN6).
10. Engineer draws, Designer gates on an image-capable model (DN3 deviation from LLM-PLM 8.4).
11. Owners as assigned: Sean on N1, N2, N4, N7, F_bind, SF 3, T8 root diameter; Quinn on Q2, Q9, DN23-c, -e, N5, N6, N8, N9.
12. ASSUMED seeds Sean owns until replaced: drill length 800, g_min 10 mm, operator sector, ring material and form. The S1 pose table is confirmed at the S1 spec, not at this gate.
13. Tension rulings T1 to T7 (DN15): ratify or reverse.
