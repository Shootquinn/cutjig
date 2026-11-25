# Step 0 Software Engineer TDD Revision Notes

Edited in research/sean/gameplan.md: Steps table, Step details, Context Recipes; Design Note 14 added. Header, Start here, Repository Sync, Objectives, Document Structure, Design Notes 1 to 13, Echo Site Registry, Open Questions and Progress Log unchanged (header, Start here and Repository Sync byte-compared after the splice: identical).

## Added per step

- **Steps table:** TDD stage column on every row. Step 5 split into rows 5.1 to 5.4 (A.6.2 ordered stages).
- **Preamble to details:** source-tag convention ([CP §n, mm:ss], [DN23], params status); rule for reported values (no threshold, no controls, arithmetic covered by K6); soft keys never asserted.
- **1.0:** spec file format (`sN_spec.yaml`, which is also the feature table the checks read); `check_stack.py` split out with an import guard; K1 to K8 controls completed, K9 coverage added (figure against spec). Every check has Z and at least one B; K3 has one B per property. K1 allowlist {0, 1, -1, 2, 0.5}. K6 tolerance 0.05 mm in data coordinates, B at 6.75 mm (smallest collar-stack term) and a datum-A frame error (40 mm). K7: depth-band rule for side views, C/G/F tolerances, g_min seed table with sources. Red-first replaced: fixture run plus a stub-sketch run, with expected red and expected guard checks named.
- **Detail 1 common:** order (a) to (h) with spec sign-off before drawing, per-sketch red-first on the stub, cross-reviewers re-compute one value by hand, corrections turned into K8 predicates with B fixtures.
- **M1 visual gate:** rubric V1 to V9 with output file format; reviewer-model controls once at 1.1 (correct figure must pass, drill-tip-up figure must fail V3). **M2:** Sean's yes/no items and the Design Notes 13 record format.
- **1.1 to 1.6:** per-sketch check tables with Z, B and source tag. Live defects used as known-bad: S1-2 (park 959.84 below start 965), S4-2 (receiver floor). S3 load-case table (cut, static, capture lift with the 10.4 kg core, retract with bind) and Euler check S3-2 with every input labelled. S6 torque and weight chains as closed-contact checks.
- **2:** Systems Engineer checklist plus `step2_check.py` cross-file checks X2-1 to X2-4 with controls.
- **3:** Q3-1 confirmed; added B2 (ANSWERED row citing a section that does not exist, Principle 7).
- **4:** seed list completed from a grep of tests/ (P10 frozen dict, P18 pinned values, P2/P7 count tests, P7 key-scan test, A1c/A1d/A1e, A3b, P6b and their step-7 controls, probe_poses, step6 column_notch). Audit checks A4-1 to A4-4 with controls; pytest red-first baseline.
- **5:** suite groups W/S/F sized to about 30; coverage matrix and number audit with controls; link check.
- **6:** Manager re-runs every scripted check; any red blocks close.
- **Context Recipes:** specs, fixtures, checks JSON and rubric added where each agent needs them; 5.x rows split.

## Cut as ceremony

- Missing-file red-first baseline: every check fails for the same reason and proves nothing. Replaced by the stub run.
- Second overlap implementation via `matplotlib.path`: one implementation with Z and B controls carries the evidence.
- S3 "screw length in 800 to 900 mm" as a pass/fail: the range is Quinn's estimate. Now reported, flagged to Sean when outside.
- S3 separate "force per screw = load / 3" check: folded into the load-case table.
- Critical speed as a gate: traverse rate is ASSUMED; reported only.
- S1 "drill tip at end of capture equals `stop.height_z`" and S6 "pinions as trapezoids": already covered by K6 and K5 B2.
- Step 2 scripted row checks for sketch citation, reason and owner on a six-row table: a reviewer reads it in two minutes. Kept as the Systems Engineer checklist; the script keeps only the cross-file checks where slips happen.
- Any assertion against the 2000 mm soft height (would break the design freedom rule).

## Untestable as written, and the fix

- **Iris drive with three pinions (S6, DN23-e):** no defined mechanism to check. S6 carries a callout (K9 enforces it); Step 3 owns the question.
- **S2 operator sector:** untestable until the spec gives apex, half-angle and radius. The Designer sets them at the S2 params review.
- **S3-2 buckling:** testable only with stated T8 root diameter, masses and end condition. All carried as ASSUMED in the overlay; Sean replaces d_r from vendor data.
- **Step 4, test_P10_every_key_in_concept_icd_table_exists:** reads `research/quinn/cr_scratch/step2_system_concept.md`, which Sean may not edit. Retiring ICD keys turns it red with no fix available from this side. Routed to Quinn in the Step 3 batch, before 4b.

## UNVERIFIED or corrected sources

- **"INSITU2 157-166"** (Document Structure limitations table, Open Questions DN23-e; also in Quinn DN23): `context/literature/INSITU2_text.md` on disk has 12 lines. The claim (iris closed by the drill drivetrain, same drivetrain) is at its lines 3 and 7. The line range is UNVERIFIED; the claim is TRACED. My details cite "INSITU2 via [DN23]" with no line numbers. The Engineer should correct the two citations outside my sections.
- **Baseline 672 / 620 / 52** (Quinn's header): taken from the draft and the Manager open, not re-read. Detail 4 now says the measured pytest figure governs.
- Verified: drill about 800 mm at critical-path §3.2, 18:20; 10.4 kg core in Quinn's Source Verification Register (DERIVED); the T8 buckling statement in DN23 line 778; `stop.g_stop` DECLARED in test P18; test P18 formulas at tests/test_params_bom.py 694-718; the ASSEMBLY.md coordinate frame at line 7.
- All g_min values, the SF of 3, the operator sector and F_bind are mine and labelled ASSUMED.

## Problem for S3 and Step 2

T8 compression margin looks thin even with no cutting load in compression. Inputs (all ASSUMED): root diameter 6.0 mm, E 200 GPa, L 850 mm, K = 1. Then I = 63.6 mm⁴ and P_cr = 174 N per screw. With W about 25 kg (ring, drill, gear, three NEMA 23), each screw carries 82 N in the static case, for a margin of 2.1. The capture lift adds the 10.4 kg core, making 116 N per screw and a margin of 1.5. With K = 2 (nut free laterally), P_cr = 43 N and the static case fails. In the retract and capture-lift cases the screw below the nut is in compression. DN23 counts only the ring weight as compression, so these cases are a gap in it. S3 will likely push the screw-size row toward TR10/TR12 or an axial bearing at the top as well as the bottom, so the down loads go into the frame through the upper span in tension. S3-2 is built to show this with numbers.
