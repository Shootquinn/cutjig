## Final count

513 collected, zero collection errors. Run `python -m pytest tests -q --junitxml=results\step4_final.xml`: 255 passed, 258 failed, 0 errors, 0 skips, 0 xfails. All 258 failures start `MISSING:` or `ABSENT FEATURE:` (parsed from the junit XML). No invariant or control fails.

## Close criteria 1 to 8

| # | Criterion | State | Evidence |
|---|---|---|---|
| 1 | SE signs | Met | This file |
| 2 | Fact-Checker signs | Not met, clerical | Gate is WITHHELD on three missing tags; the tags landed (test_collet_family.py:125-127 core nominal, test_params_bom.py:28 WOB, :116 stock). Fact-Checker re-sign belongs to the Manager. Ruling 18: clerical |
| 3 | Baseline record | Met | step4_engineer_baseline.md on disk |
| 4 | Collect clean, five modules | Met | 513 collected, no errors, no sixth module |
| 5 | Run split | Met | 255 green_at_4 pass; 258 fail by MISSING/ABSENT FEATURE only |
| 6 | One label, one green_at | Met | conftest.py label gate runs at collection and passed |
| 7 | Controls green | Met | All control tests in the 255 passes |
| 8 | Greps | Met, one note | Hazard and printer terms appear only in P22 and the P1/P20 filter tests; no assertion bounds a soft key (equality freezes and P23 plants only); PZRT present in params. The `parts_cache` nut and receiver mtimes (22:42, 22:45) are later than B4 because the fix pass rebuilt them by stud-subtract; no other FCStd changed |

## Changes made

1. tests/test_thread_clamp.py:129: the T9 line `# SRC: margin 1.5 | DECLARED` matched no Register row, so P24 (an invariant) failed. The 1.5 is a design margin, not a Register claim. The line is now a plain comment citing cr_scratch/step2_loftsman_crossreview_reply.md section 3. P24 passes. No assertion, threshold or discriminator changed.

No other edits were needed. T9 passes 3 of 3.

## Verdict

SIGNED. The suite is the contract: 255 invariants and controls green, 258 discriminators red for absence only.
