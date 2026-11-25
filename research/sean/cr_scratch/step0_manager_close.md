# Step 0 Manager Close (sean, drafting variant A.6.4)

Date: 2026-11-24. Gameplan: research/sean/gameplan.md. Inputs: step0_manager_open.md, step0_engineer_draft_notes.md, step0_software_engineer_tdd_revision.md, step0_systems_engineer_review.md, step0_designer_review.md, step0_engineer_revision_notes.md.

**Verdict: READY FOR SEAN.** Inter-step gate. Step 1 does not open until Sean approves.

## 1. Acceptance list (step0_manager_open.md section 1)

| # | Item | Result | Where |
|---|---|---|---|
| 1 | Header unchanged except Current step; lit_review `no`, question to Sean | PASS | Header; N3 |
| 2 | "Start here" and "Repository Sync" byte for byte | PASS | Compared with `git show 4bfad31:research/sean/gameplan.md` (commit before Step 0): header to Current step, lit_review line, Start here, Repository Sync all equal. Repository Sync structure matches research/quinn/gameplan.md items 1 to 6, name substituted |
| 3 | Objectives numbered, decisions in force, lift objective restated | PASS | Objectives 1 to 8; Objective 4 |
| 4 | Steps table with Assigned To and Status; detail per step with objective, TDD stage, checks with Z and B, red-first, visual gate, human gate; Step 1 sketch set, S1 first, each sketch human-corrected before the next; set redefined per critical-path 15 | PASS | Steps table; details 1.0 to 7; detail 1 common (a) to (i); DN4 |
| 5 | Week-close step with params and test change list; later CAD as placeholder | PASS | Steps 4a to 4c, 6; Step 7 |
| 6 | Context Recipes for every spawning step | PASS after Manager edit (5.4 Engineer row added) | Context Recipes |
| 7 | Design Notes: decisions in force, superseded items, LLM-PLM 8.4 deviation | PASS | DN1, DN2, DN3 |
| 8 | Open Questions: Q1 to Q11 with Q1, Q3, Q7 answered; DN23 opens; Q2 | PASS | Open Questions |
| 9 | Progress Log row for Step 0 | PASS | Progress Log |

Out-of-scope check: commits 6b2bc5b to eefd194 touch only research/sean/gameplan.md and research/sean/cr_scratch/. The research/quinn/gameplan.md change in that range is Quinn's own commit bec5691.

## 2. Designer close checklist

All 12 items met: D1 governing line (Objectives, first paragraph); D2 Progress Log matches Steps (updated at close); D3 no bare "INSITU2 157-166" (both sites cite the excerpt line; ruling below); D4 drill head and top-end block distinct, tube labelled tube OD, cutter OD ASSUMED; D5 S1-5a and S1-5b with Z and B; D6 pose table; D7 `ring.*` functional features and Designer fail rule; D8 Step 2 hold, hard-stop and step-loss rows, `upper.metal_stop` and `upper.park_lock` retire only on Sean's ruling; D9 operator-task table, V10, N6; D10 S4-3 with flipped-collet B; D11 to D15 applied; protected sections byte-identical.

## 3. Blocking findings: owners

- **SE-1 (drill-to-ring interface).** Sketch: S6 draws the bearing as a named feature. Check with controls: S6-5 (Z fixture; B bearing removed, path runs through pinion teeth). Open question with named human: N4, Sean; Step 2 bearing row. Real owner.
- **SE-2 (axial loop through the kept base).** Check with controls: S3-3 (Z fixture; B anchor member 1 mm clear of the base frame), re-run at S6 and in X2-5. Reported kept-part forces at 1000 N and stall thrust. Open question with named human: N5, Quinn, batch 1; Design Notes 16. Real owner.

## 4. FIX dispositions spot-checked in the gameplan (12)

| ID | Landed at | Result |
|---|---|---|
| SE-3 | Lift stroke defined (detail 1.1), used in S3 length formula, Echo row, S1 reports per Q9 option | Landed |
| SE-4 | Step 2 descent-end row; S1 Shows; DN2 status line; 4a fixed dispositions; N7 | Landed |
| SE-5 | S6-3 chain closes through base, receiver, collet, core; S6 reports drill torque against 10 N m; `icd.torque_reaction` REWRITE | Landed |
| SE-6 | N2 renamed; S3 nut mounting sets K in S3-2; Step 2 guidance row citing R13; S2-4 note | Landed |
| SE-7 | Checks JSON hashes and key values, `--stale`, step (i), X2-5, detail 6 | Landed |
| SE-10 | Order 4a, 4b, 5, Quinn review, 4c, 6; 5.1 tests count proposed changes; DN15 T4 | Landed |
| SE-13 | N8 in batch 1; 4c holds ASSEMBLY.md ICD edits until Quinn rules | Landed |
| SE-14 / D3 (INSITU2) | Both sites read "INSITU2 157-166, excerpted at `context/literature/INSITU2_text.md` line 7, via Quinn DN23". Verified: line 7 of the excerpt is the row for original lines 157-166 (iris closed through the drill drivetrain). Reviewers read the range as excerpt lines. Engineer's rejection of the "send to Quinn" sub-item is correct | Landed |
| SE-15 | K7 swept case with Z4 and B4 | Landed |
| D5 | S1-5a and S1-5b, g_min seeds updated | Landed |
| D7 | `ring.*` seed lists nut housings, motor mounts, bore, gear seat, bearing seat, guide interface, material, position, mass | Landed |
| D9 | Operator-task table, V10, N6 owner Quinn | Landed |

Spot values against params.yaml: `upper.park_z` 959.84, `stop.start_z` [834.84, 965], `stop.collar_top_z` 159.84, `collar.top_above_plate` 6.75, `wingnut.sweep_clear_radius` 115, `upper.drill_advance_500core` 534.93, `icd.keepout_radius` 86.2: all agree. Cited test functions exist at the stated places (test_P18_collar_top_recomputed_from_params line 694; P10 working stroke, concept ICD, load loop; P3 1540; A2d).

## 5. Manager edits at close

- Current step: "0 (closed by Manager; awaiting Sean's approval at the gate)".
- Steps row 0 status and a Progress Log close row.
- Q3-0: detail 1.0 invoked Q3-1 on the batch file at 1.0, but `step3_check.py` was scheduled for Step 3. The script is now written at 1.0 with a batch-mode check Q3-0 (Z complete fixture batch; B blank stand-in; red-first on an empty batch). Steps row 1.0 and Document Structure updated to cite Q3-0.
- Context Recipe 5.4, The Engineer (fix), added.
- Accumulator created: research/sean/accumulator.md.

Note for the gate: the header line "Accumulator file: none yet; research/sean/accumulator.md is created at Step 0 close" is protected and left as written; the file now exists. Sean may approve updating it.

## 6. Gate brief for Sean: 13 decisions

Each decision has the team's recommended answer. Where Sean says nothing, the recommendation stands as written in the gameplan.

1. **Literature review flag (N3).** Should this phase require primary-source backing for technical claims, as Quinn's plan does? Recommended: keep `no`; the week is configuration sketches, and the one external source (INSITU2) is already traced through Quinn's register.
2. **S3 redefinition (DN4).** The old S3 (S1 drawn once per lift option) is void because the lift is decided. Recommended: S3 becomes a side section through one jack screw (anchor, nut, guide, motor, hold device, load arrows) plus a plan inset of all three screws and the sync loop.
3. **Where accepted sketches live (DN7).** Accepted sketches need a shared home Quinn can run and fix. Recommended: `docs/sketches/`, with the check harness and proposed-keys file moving there at the first acceptance (S1).
4. **Drawing order and who decides options (DN5).** Recommended: draw S1, S2, S3, S4, S6, then the Step 2 lift decision record, then S5 (stock map); Sean picks each drawn option at that sketch's correction pass, and Step 2 consolidates the picks.
5. **When shared-file changes are executed (DN15 T4).** Recommended: params.yaml, ASSEMBLY.md and test changes are executed only after Quinn reviews the proposed change list in the week-close record; Sean may choose to execute first instead.
6. **Base carries the cut reaction (DN16, N5).** With a powered screw lift, the 1000 N cutting load passes through the kept collet, holder, receiver and base plate, which ASSEMBLY.md says never happens. Recommended: accept this framing and send it to Quinn in batch 1 for a ruling on whether those parts need a rating check.
7. **Early question batch to Quinn (detail 1.0).** Recommended: push batch 1 at Step 1.0 open, before the harness work: drill length, mass, top-end hardware and cutter OD (Q2), core lengths to support (Q9), the five DN23 opens, and N5 to N9.
8. **Week-close record format (DN9).** Recommended: a short prose record for Quinn, built with test suite, outline, write and revise; the alternative is a table-only record with one check step.
9. **Proposed-keys overlay (DN6).** Recommended: new keys the sketches need live in `proposed_params.yaml` during sketching; params.yaml is untouched until the execution step (4c).
10. **Who draws the sketches (DN3).** LLM-PLM 8.4 has The Designer build a 3D sketch assembly. Recommended: 2D matplotlib only this week; The Engineer writes the sketch scripts, and The Designer reviews params, signs the spec and runs the visual gate on an image-capable model.
11. **Owners of open items.** Recommended: Sean owns ring position (N1), ring guidance and nut mounting (N2), drill-to-ring bearing (N4), descent stop and power-off hold (N7), bind force, buckling safety factor 3 and T8 root diameter; Quinn owns Q2, Q9, drill rpm and torque (DN23-c), iris drive (DN23-e), N5, N6, N8 and N9.
12. **Working assumptions Sean owns until replaced.** Recommended: accept drill length 800 mm, a 10 mm clearance between moving and fixed parts, the operator loading sector, and ring material and form as ASSUMED seeds; the S1 pose table is confirmed at the S1 spec.
13. **Software Engineer vs Systems Engineer rulings (DN15 T1 to T7).** Recommended: ratify all seven (swept-envelope clearance check inside the one overlap check; staleness hashes kept; one decision locus; execution after Quinn's review; early orientation preview of S1; new load-chain checks kept; requested forces reported without thresholds).
