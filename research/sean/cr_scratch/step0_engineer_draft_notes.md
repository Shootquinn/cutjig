# Step 0 Engineer Draft Notes

## What went where (research/sean/gameplan.md)
- Header: Current step set to "0 (drafted, awaiting approval)"; lit_review stays `no`. Start here and Repository Sync untouched.
- Objectives 1-8: week-done list as amended by Quinn's decisions; Objective 4 restates the lift item (lift chosen; sync, anchoring, anti-rotation, frame open).
- Document Structure: only for the Step 5 configuration record; Steps 1-4 produce no prose.
- Steps 0-7 with Assigned To. Step 1 has sub-steps 1.0 (harness) and 1.1-1.6, one per sketch, each with Designer params review, spec, scripts, K-checks, cross-review, image-capable visual gate, Sean's correction pass, correction logged in Design Notes 13.
- Step details: check library K1-K8 with zero and known-bad controls, red-first baseline file, per-sketch question, R/Q rows closed, params keys, script and PNG paths. [SE: ...] marks the gaps for The Software Engineer.
- Steps 2 (lift decision record), 3 (question sweep), 4 (change list then LLM-PLM execution, seed list of keys and tests), 5 (record, 5.1-5.4), 6 (Manager close), 7 (CAD placeholder).
- Context Recipes for every spawning step; Progress Log row for Step 0; Design Notes 1-13; Echo Site Registry; Open Questions table (Q1, Q3, Q7 answered; DN23 opens; N1-N3 new).

## Choices Sean must confirm at the gate
1. lit_review flag (Open Questions N3).
2. S3 redefinition: section through one jack screw (DN 4).
3. Drawing order S1, S2, S3, S4, S6, S5 (DN 5).
4. Proposed-keys overlay `research/sean/cr_scratch/sketches/proposed_params.yaml`; params.yaml untouched until Step 4 (DN 6).
5. Shared location for accepted sketches: `docs/sketches/` (DN 7).
6. Engineer draws, Designer reviews and gates (DN 3 deviation).
7. Week-close record is prose with TDD sub-steps (DN 9).
8. Seed overlay value drill.length 800 ASSUMED until Quinn answers Q2.

## Contradictions in the inputs and handling
1. Critical-path 7.3 S3 "per lift option", 7.4 and the week-done bullet "lift option chosen or narrowed to two": overtaken by section 15. S3 redefined (DN 4); Objective 4 restates the item; listed as superseded (DN 2).
2. Section 6 "twin" screws vs three in section 15 and DN23: three governs (DN 2).
3. Section 8 height stack assumes two 1540 columns and a hoist: superseded; S1 and S2 define the frame (DN 2, details 1.1, 1.2).
4. Test counts 622/50 vs 620/52: the later 620/52 governs (DN 10).
5. LLM-PLM 8.4 STEP sketch assembly vs 2D only: recorded deviation (DN 3); 7.4 interference done as 2D overlap K7.
6. lit_review no (Sean) vs yes (Quinn): goes to Sean (N3).
7. Iris drive vs three pinions: Open Questions DN23-e, owner Quinn, S6.
8. ASSEMBLY.md ICD row still reads travel 500, start_z 684.84/815 against params 650, 834.84/965: fixed at Step 4 (DN 12).
9. `stop.height_range[1]` 315 is flagged "not re-derived" in params and feeds start_z 965 and the P10 failure: S1 re-derives it with the park rule (detail 1.1).
10. `bom_stock_allocation.md` reserves the 1540 lengths for columns that are void: released in S5 and Step 4.

## Problems found
- Torque reaction: lead screws react ring torque only in bending; an 850 mm T8 is a poor torque member. S6 must show an anti-rotation member (DN 11, N2). This likely adds frame members, which is why S6 precedes S5.
- Ring position on the drill is unconstrained by any decision; it sets screw anchor and guide heights and therefore the frame height. S1 must fix it (N1).
- If the ring sits near the drill top, the ring range is roughly 985 to 1635 mm for the 0.5 m case, so screw anchors stand well above the floor and need a raised frame. S1 arithmetic decides; not yet computed.
