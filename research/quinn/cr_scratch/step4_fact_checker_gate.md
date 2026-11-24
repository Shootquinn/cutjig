## Verdict table

| Claim | Test IDs | Lines read | Verdict |
|---|---|---|---|
| 1 Core 100 mm, conflict | P2, C8 | INSITU2_text.md (file is 12 long lines; Grep hits "pre-cast to 100" line 9, "above 100 mm" line 8; the cited 186-188 and 406-407 do not exist as line numbers); test_params_bom.py 19 | Source MATCHES. Register trace line numbers do not exist in the file. NO `# SRC:` tag for this row in any suite file; only a dict comment at test_params_bom.py:19. DEFECT |
| 2 Core 90-105, 6.00/5.75 in, 1/8 in | P1, A2 | workorder.md Grep | MATCHES (all four strings on line 1). Tag at test_collet_family.py:126 CONTRACT, correct |
| 3 Iris 54.2925 | P8 | double_dong_params.py 92 | MATCHES (comment "aperture 54.2925 -> 0"; 108.585 is 2x). Tag test_collet_family.py:232 DECLARED, matches Register |
| 4 106.369 | F4 | double_dong_params.py 372-380; params.yaml 27 | MATCHES: head tip to kerf sphere centre. 106.369+25+5+6.75=143.119; params 143.12 DERIVED. Tag test_thread_clamp.py:144 VERIFIED |
| 5 WOB 100-1000 N | loads | INSITU3_text.md Grep (100 N, 1000 N present); params.yaml 49-50 | MATCHES. No SRC tag in suite (test_params_bom.py:29-30 only). DEFECT |
| 6 Stock | P3 | params.yaml 305-317; step0_human_stock_80-20.md 7-15 | MATCHES, sum 15688. No SRC tag at the P3 stock test. DEFECT |
| 7 T-nut PZRT | P4 | step3_human_gate_decisions.md Grep; test_params_bom.py 640, 986-992 | MATCHES; tag 986 DECLARED |
| 8 Profile 916.56, 2.573 | P9 | step_measure.json 5759-5760 (916.5604); params.yaml 300-301 | MATCHES; 2.573 DERIVED (catalog string) |
| 9 Gate values | H, collet | step0 B3-B6; params 23-25, 43, 47, 70, 157 | MATCHES. g_stop 25 DECLARED, "no standard cited" |
| 10 Tag audit | all | SRC grep, 22 tags | Statuses match Register. Missing tags listed above. No Mines or SBIR attribution found |
| 11 Language | six files | Grep | Only P22 word list/planted strings (test_params_bom.py 810, 812, 838, 858-870). CLEAN |
| 12 Printer | six files | Grep | Only P1/P20 filter tests (74-78, 758-767) and P22. No printer key read. CLEAN |
| 13 Carried items | | Grep csm_sow, summary_yokeless, borebot_operating, INSITU | Not cited by the Step 4 suite; moves to the Step 13 gate |

## Defects

1. Core nominal 100 mm (Register row 1): no `# SRC: Core nominal 100 mm | VERIFIED with conflict | ...` tag. Needed at P2 and C8 (test_collet_family.py near 125).
2. WOB (Register row 395): no tag where tests read loads.wob_min/wob_max (test_params_bom.py 29-30).
3. Stock lengths (Register row 410): no tag at P3 stock test.
4. Register row 1 and INSITU line numbers (186-188, 406-407, 424-430) do not resolve in the 12-line text files; the tags should cite the quoted phrase.

Tool calls used: 17.

WITHHELD: test_params_bom.py:19, 29-30, P3 stock test; test_collet_family.py:125-126 (P2/C8 core nominal tag).
