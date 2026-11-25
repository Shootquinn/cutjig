# Step 1.0 Software Engineer sign-off after the revision pass

Verdict: SIGNED (harness, fixture run, S1 stub run, step3_check.py Q3-0). SW-1 to SW-9 closed; no new BLOCK or FIX; two new NOTEs.

## 1. Re-runs (MEASURED 2026-11-24)

| Command | Exit | Result | Seconds |
|---|---|---|---|
| `check_sketch.py --controls` | 0 | Z clean 17/17, B fired 50/50, smoke 1/1 | 42.3 |
| `check_sketch.py s1 --rev 0` | 1 | K1, K2, K3, K5 pass (guard); K4, K9 red (content); K6, K7, K8, S1-1 to S1-6 red (absent) | 3.2 |
| `check_sketch.py --stale` | 0 | 0 records checked | |
| `--stale --include-unaccepted --overlay <copy with ring.thickness 13>` | 1 | "STALE s1_checks_r0.json: ring.thickness recorded 12, live 13" | |
| step3_check.py Q3-0, empty / Z / B / batch 1 | 1 / 0 / 1 / 0 | "table has no rows" / PASS / "line 6 row 'B2': blank standin" / PASS | |

baseline_red.json against my re-runs: run 1, 68 of 68 rows have the same observed result, reason and match. Run 2, 16 of 16 the same, cause labels included. The summary reads 17/17, 50/50, smoke 1/1, run 2 16/16. baseline_red_wave1b.json is kept with its 41 run-1 rows. All 41 Wave 1b controls are present in the new run with the same match outcome. My re-runs rewrote controls_results.json, s1_checks_r0.json and s1_summary_r0.md; the content is identical and only the timestamps changed. baseline_red.json was not rewritten.

## 2. Disposition per finding

| ID | Class | Status | Evidence (MEASURED) |
|---|---|---|---|
| SW-1 | BLOCK | CLOSED | The spec reads `seat: core_seat` twice, and `on:` is gone. A scratch copy restored to `on:` goes to `load_spec`, which raises "non-string keys ... row core_500 sense: key True; row core_750 sense: key True". `sense_lint` on the raw copy returns two spec errors and no exception. K8-B9 fires with "core_500 rests_on: spec error" and "True", 1 issue against 1 planted. |
| SW-2 | FIX | CLOSED | All 50 manifest B entries carry reason substrings. None of them is a short generic token. Each B sets `planted` to its expected issue count. `compare()` demands both. Synthetic probes with the right count but the wrong reason, and with the right reason plus an extra issue, both return False. |
| SW-3 | FIX | CLOSED | K4 finds each annotation by gid `label:<id>`. My swapped-core probe now fails: "label 'core 750' number differs from core.length_capture = 500", and the mirror line for core_750. K4-B3 fires with 2 issues against 2 planted. |
| SW-4 | FIX | CLOSED | Three new B controls fire as planted: K8-B4 "core_500 rests_on core_seat ... 1.000 mm", K8-B5 "gear not mirrored", K8-B6 "screw_b azimuth 270.00". |
| SW-5 | FIX | CLOSED | `side` and `outboard` predicates are added. motor23_a carries side -1 and motor23_b side +1, both outboard of their pinion. K8-B7 fires with 2 issues against 2 planted. |
| SW-6 | FIX | CLOSED | Plan-view swept controls: K7-Z5 is clean on the skip branch, and K7-B8 fires ("swept", "ring\|member"). |
| SW-7 | FIX | CLOSED | Every result carries `cause`. Run 2 expects "red (absent, fail-closed; content evidence run 1)" for K6, K7, K8 and "red (absent, fail-closed; content at 1.1 c)" for S1-x. A match requires the cause, and all 16 match. K4 and K9 are labelled content. |
| SW-8 | FIX | CLOSED | Control S1-FULL runs all 16 checks on every S1 row drawn. None errors and none is absent. K7, K8 and S1-4 are red on content, as reported values from the unsigned draft; the rest pass. This control is what would have caught SW-1. |
| SW-9 | FIX | CLOSED | The spec carries 42 S1-5b neighbours: 7 ring-assembly rows × 6 base parts, g_min 10, poses [capture_end]. checks_s1.py no longer contains RING_ASSY, BASE or 10.0. S1-5b reads the pairs and g_min from the spec and judges them through `assess_pair`, the same function K7 uses. |
| SW-10 | NOTE | carried to 1.1 | The S1-2 and S1-3 B fixtures mutate the spec `tip_z`. |
| SW-11 | NOTE | CLOSED | `_tip` disagreement raises `Content`. |
| SW-12 to SW-15, SW-17 | NOTE | no change, as dispositioned | |
| SW-16 | NOTE | CLOSED | |

## 3. LF-1 and TP-1 fixes against the Z controls

- All 17 Z controls are clean. The 12 Wave 1b Z controls keep their outcome and their state sets: K7-Z1 F, Z2 depth-separated, Z3 C, Z4 `['F', 'swept:F']`.
- K6-Z: "14 z_rule(s) match drawn extents within 0.05 mm; check_stack imports and anchors clean". The TP-1 transform path measures every drawn rectangle the same way as before.
- K8-Z: 19, 4 and 2 predicates hold, with axes not inverted.
- K5-Z now includes the 15-artist mini side figure, clean.
- K7-B5 (C pair depth-separated by 490 mm) and K7-B6 (G band gap 1 mm, g_min 10) fire on their planted reasons.
- K8-B8 fires twice, on "drill_head below gear" and "drill_head below drill_top_block".

LF-1 changes K7 semantics, so the reason strings now name it: disjoint depth bands settle class F only. K7-Z2 is a class-F pair and still reads depth-separated. It remains a valid Z under the new rule.

## 4. New notes

**SW-18 NOTE.** S1-FULL runs K1 with no script (revision notes correction 5), so K1 passes with nothing to scan. K1's evidence remains K1-Z, B1 and B2. At 1.1 (d) the real script is scanned. No change.

**SW-19 NOTE.** The new controls K7-Z5 to Z7 and B7 to B10, K3-B7, K4-B3, K5-B4, B5, K6-Z2, B4, K8-Z2, B4 to B11, K9-B3, B4 and S1-FULL are recorded in the manifest. The gameplan K table lists only K7-B5 and B6. Whether to add the others to the K table is the orchestrator's decision. The manifest is the executable record.

SIGNED (harness, fixture run, S1 stub run, step3_check.py Q3-0).
