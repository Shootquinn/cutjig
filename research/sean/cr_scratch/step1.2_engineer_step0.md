## Corrections to the brief

1. The Echo Site Registry park-rule row is gameplan l.650, not l.648 (l.648 is the screw-length row, l.649 the lift-stroke row).
2. R5 "so the 0.5 and 0.75 m values are unchanged" holds only for c <= 42.34 (DERIVED). The term `collet.core_stop_z + L + c - upper.travel_max` applies to every class. For the 0.75 m class it reads 142.50 + c, so above c = 42.34 the 0.75 m stop and start rise with c (start 792.50 + c). The 0.5 m class holds to c <= 292.34. Park 1209.84, stroke 1025 and L 1140 (1 m class) hold to c <= 117.34. Design Notes 23 is therefore exact on 0 <= c <= 42.34. 42.34 is the existing 0.75 m start clearance (834.84 - 792.50). Sean's ruling holds as written only if c <= 42.34; this goes to the Loftsman (P0L) and to Sean when he sets c.
3. The same coupling hit a control. S1-1-B1 plants `upper.travel_max` 500. Under the new rule the 0.75 m term governs (42.5 + 750 + c - 500 = 292.50 + c), so the drawn start depends on c, and check_stack refuses it. The control errored in the first full run (Z 38/38, B 86/87). Fix: the fixture evaluates the term at c = 0, a control input and not a design value. S1-1 reads drawn tips only, so its reason is unchanged. Rerun: 87/87. Consequence for S2 and later: any edit to `upper.travel_max`, `collet.core_stop_z` or a core length can make the drawn S1 values depend on c. check_stack then stops with "depends on symbol c" rather than draw a guessed value.
4. R1 c names the visual-gate file in the copy-up set. R4 c says the committed `fixtures/controls_results.json` and `fixtures/figs/` change only at `--accept` or the Manager close. `--accept` therefore copies up the wip/ controls results, control figures and `baseline_red.json` with the revision, but only when every control in the wip/ results matched.
5. `--baseline sN` writes to `wip/baseline_red.json`. The brief does not place it, and under the wip/ rule it is a verification output. It seeds its history from the committed `baseline_red.json`. `--accept` copies it up (item 4).
6. The `wip/s1_checks_r4.json` that the orchestrator's accept will copy up is the record from this run. It differs from the committed r4 record in timestamp and in the reported 1 m and symbol fields (section 5). keys_read, checks, files_sha256 and spec_status are equal.

## 1 Files changed

All under `docs/sketches/`. Line endings stay CRLF.

| Path | What |
|---|---|
| `check_sketch.py` | `--accept sN --rev k --note` (accept, revision_outputs, harness_outputs, PNG pixel compare, JSON field diff, supersession); `--stale` through `stale_records` (latest accepted unsuperseded record per sketch in docs/; unaccepted records in wip/ with `--include-unaccepted`) and `stale_diffs`; `--baseline sN`; per-sketch tables `SKETCH_TABLES` plus `sketch_table()` (a checks_sN.py STUB_EXPECT / STUB_CAUSE / SOURCES takes precedence) and `K_SOURCES`; `write_record` to wip/; `--controls` to wip/fixtures/; `control_tally` reads wip/ first; `--docs-dir`, `--wip-dir`; run_control accepts a fixture that returns a check result; summary prints symbol terms |
| `check_stack.py` | `PW` piecewise-linear evaluator for spec symbols (+, -, scalar *, /, min, max, abs); `symbol_names`, `numeric` (drawn value only where constant on the first segment, else ValueError), `report_value`; class_starts / class_stops / park_tip take `symbolic`; reported adds `stops_z_A`, `symbol_terms`, `drawn_symbol_validity` |
| `sketch_loader.py` | Output rule in the module docstring; `WIP`, `output_dir`, `output_path`, `find_output` |
| `s1_side_poses.py` | PNGs through `output_path` (wip/); usage line |
| `s1_mass_report.py` | Reads the summary through `find_output`, writes summary and JSON through `output_path` (wip/); docstring |
| `s1_spec.yaml` | park_rule comment block (Sean's ruling), `symbols.c`, stop_k and for_step4 with the start-above-core term; collar shape gloss |
| `fixtures/step0_fixtures.py` | new: H1 and H5 control builders (temporary docs/ and wip/ copies) |
| `fixtures/manifest.yaml` | 9 entries H1-Z1, H1-Z2, H1-B1 to H1-B5, H5-Z, H5-B |
| `fixtures/builders.py` | `s1_1_b1`: term at c = 0 (Correction 3) |
| `s1_checks_r0.json` | new: copy of the frozen scratch record |
| `.gitignore` | new: `wip/` |

## 2 R1 design and controls

Design:
- `--accept` takes the record from wip/ if present, else from docs/.
- Refused, with nothing written, when: the note is empty, the record is absent, any check is not "pass", or a wip/ PNG differs in pixels from a docs/ PNG of the same name.
- Order of work: set the flag (accepted, accepted_note, accepted_at) in the source record; copy each wip/ output up and check SHA-256 equality; keep PNGs that are byte-equal or pixel-equal; replace JSON and markdown with a printed list of the differing fields or lines; copy up the harness records (Correction 4); set `superseded_by: k` on earlier accepted records of the sketch, which keep their flag.
- A re-run writes only to wip/, so the docs record keeps its flag.

Red on the pre-change code: the controls were run against a copy of the pre-change tree (`wip/pre/`, since deleted).

| ID | Planted | Reason substring | Red on pre-change code (MEASURED) | Result |
|---|---|---|---|---|
| H1-Z1 | passing record, summary and byte-equal PNG in wip/ | (clean) | AttributeError: `check_sketch` has no `record_name` / accept | clean, match |
| H1-Z2 | accept, then `write_record` of an unflagged re-run to wip/ | (clean) | AttributeError | clean, match |
| H1-B1 | S1-4 "fail" in the record | "refused", "checks not pass: S1-4 fail" | AttributeError | fires 1, match |
| H1-B2 | note "  " | "refused: empty note" | AttributeError | fires 1, match |
| H1-B3 | overlay jackscrew.anchor_z 265 to 266 against a flagged record | "s1_checks_r4.json: jackscrew.anchor_z recorded 265" | AttributeError | fires 1, match |
| H1-B4 | r4 accepted with stale anchor_z 999; r5 with stale ring.thickness 999; accept r5 | "s1_checks_r5.json: ring.thickness recorded 999" (planted 1) | AttributeError. Pre-change `--stale` on r4 and r5 both flagged: 2 records, 2 differences (count 2, planted 1: mismatch) | fires 1, match |
| H1-B5 | wip/ PNG one pixel off the docs/ PNG of the same name | "refused", "differs in pixels" | AttributeError | fires 1, match |
| H5-Z | live S1: 1 m stop 392.50 + c, start 1042.50 + c, start_minus_core_top c; 0.75 m start 834.84; park 959.84 / 1209.84; stroke 775 / 1025; L_min 1135 | (clean) | KeyError `stops_z_A`. Pre-change 1 m start_minus_core_top -125.00 | clean, match |
| H5-B | 1 m class made a drawn class (q9_length_keys + core.length_optional) | "depends on symbol c" | read clean (no refusal): mismatch | fires 1, match |

Controls 117 to 126: Z 35 to 38, B 81 to 87, smoke 1.

## 3 R2 copy hash and --baseline s1

- `research/sean/cr_scratch/sketches/s1_checks_r0.json` and `docs/sketches/s1_checks_r0.json`: SHA-256 7454be78c0816cd2e5648d41bfe7ff76050fe062ab991a30ac5f314955faf3be for both; `cmp` byte-equal (MEASURED).
- `--baseline s1` (MEASURED): run 2 matched 17/17 from `s1_checks_r0.json`, equal to the committed `baseline_red.json` run 2 (17/17). Run 1 is 126/126 from `wip/fixtures/controls_results.json`.
- Output `wip/baseline_red.json`. Its history carries the committed record under a dated key (8 prior records). New field `run2_by_sketch` holds `{s1: ...}`. Rows carry `sketch` on run 2. Other sketches' run 2 carries over when one sketch is re-assembled.
- S2 adds STUB_EXPECT, STUB_CAUSE and SOURCES in `checks_s2.py`. `baseline()` and `run_sketch()` read them through `sketch_table()`.

## 4 R3/R4 output rule and SHA-256 table

Rule (`sketch_loader.py` docstring):
- Every unaccepted revision output and every verification output goes to `docs/sketches/wip/`, created on demand. This covers the sN run JSON and summary, sketch PNGs, the mass report, the visual-gate file, `--controls` results and figures, and `--baseline`.
- Only `--accept` writes to `docs/sketches/`.
- Scripts call `output_path()` and read through `find_output()` (wip/ first).

`--stale` reads accepted records from docs/ and, with `--include-unaccepted`, unaccepted records from wip/.

Committed files (37, everything under `docs/sketches/` outside wip/): SHA-256 before and after the full verification sequence.
- Sequence: `--controls`, `s1 --rev 4`, `s1_side_poses.py --rev 4`, `s1_mass_report.py --rev 4`, `--stale`, `--stale --include-unaccepted`, `--baseline s1`.
- Result: **0 differences** (MEASURED; the snapshots were taken after the edits below).

Against the tree at task start (first 12 hex):

| File | Before | After | Cause |
|---|---|---|---|
| .gitignore | none | 2a3c1254ccaa | R3, new |
| check_sketch.py | a54508f9aeb8 | 85b9fe351fdd | R1 to R4 |
| check_stack.py | 871d1515a2bb | 88c0120c09c4 | R5 |
| sketch_loader.py | d2f1c63369da | a6fec2eb3f19 | R3 |
| s1_side_poses.py | d167b4962338 | 535dac0be620 | R3 |
| s1_mass_report.py | 8eb804f92f48 | 5f60de14994f | R3 |
| s1_spec.yaml | aa103d7a778b | e8fb602f39d4 | R5 |
| fixtures/manifest.yaml | 4516f7b0ae6d | 1fcaf1660553 | R1, R5 controls |
| fixtures/builders.py | 9798f9911317 | e434a5b93622 | Correction 3 |
| fixtures/step0_fixtures.py | none | ad92b38c4f44 | R1, R5, new |
| s1_checks_r0.json | none | 7454be78c081 | R2, new |
| the other 26 files | | | equal: baseline_red.json, fixtures/controls_results.json, fixtures/figs/*, s1_checks_r4.json, s1_summary_r4.md, s1_mass_report_r4.json, four r4 PNGs, proposed_params.yaml, checks_s1.py, sketch_common.py, stubs, k-fixtures, s1_visual_gate_r3.md |

No `__pycache__` was written (MEASURED, none present after the runs).

## 5 R5 spec text, c treatment, values, record diff

Old (`s1_spec.yaml` l.70 to 73 and park_rule):
```
# OPEN, decision for Sean (Loftsman FIX 5, 1.1 (b)): for the 1 m class this rule gives stop 267.5 and start 917.5, and
# the 1 m core top on the core stop is 42.5 + 1000 = 1042.5 z_A, so the cutter starts 125.00 inside the uncut core
# (check_stack reported q9_options.start_minus_core_top: 292.34 / 42.34 / -125.00 for 0.5 / 0.75 / 1 m). The rule has
# no start-above-core term. The 1 m core is the third Q9 option and is not drawn in S1. No rule change at (b).
  stop_k: "max(stop.height_z, collet.core_stop_z + L + stop.g_stop - drill.bore_ceiling_above_tip)"
```
New:
```
symbols:
  c: {domain: [0, null], unit: mm, owner: "Sean (N11)", source: "Design Notes 23 (FIX 5 ruling): 1 m stop 392.50 + c, start 1042.50 + c z_A, capture 650 - c", status: "no value; reported as an expression"}
park_rule:
  stop_k: "max(stop.height_z, collet.core_stop_z + L + stop.g_stop - drill.bore_ceiling_above_tip, collet.core_stop_z + L + c - upper.travel_max)"
  for_step4: "upper.park_z = max(max_k (max(stop.height_z, collet.core_stop_z + L_k + stop.g_stop - drill.bore_ceiling_above_tip, collet.core_stop_z + L_k + c - upper.travel_max) + upper.travel_max), stop.collar_top_z + max_k L_k) + upper.load_clearance; c = start clearance above the core top (Sean, N11)"
```
The comment block above the rule now states Sean's ruling, the derived values and the c ranges (Correction 2).

Collar shape gloss: "from the wing-nut top (plate top)" now reads "from the wing-nut top (collar.top_above_plate above the wing-nut top)".

**c treatment, for the Loftsman:**
- c is a spec symbol with no value and no overlay leaf.
- check_stack evaluates every expression that reads c as an exact piecewise-linear function of c on c >= 0. The lower bound 0 comes from c being a clearance; this is DECLARED in `symbols.c.domain` and is mine to defend at P0L.
- A drawn or checked value is taken only where the function is constant on its first segment, and the upper end of that segment is recorded in `reported.drawn_symbol_validity`: lowest stop c <= 292.34, park c <= 117.34, start max c <= 42.34. Otherwise check_stack raises "depends on symbol c" (control H5-B).
- Reported values that depend on c print as expressions.

check_stack values per Q9 option (DERIVED; MEASURED from check_stack):

| Option | stop (0.5 / 0.75 / 1 m) | start (0.5 / 0.75 / 1 m) | park | stroke | L_min (at anchor_z) | start_minus_core_top |
|---|---|---|---|---|---|---|
| 0.5 m only | 184.84 / 184.84 / n/a | 834.84 / 834.84 / n/a | 959.84 | 775.00 | 885.00 (885.84) | 292.34 / 42.34 |
| 0.5 and 0.75 m | 184.84 / 184.84 / n/a | 834.84 / 834.84 / n/a | 959.84 | 775.00 | 885.00 (885.84) | 292.34 / 42.34 |
| plus 1 m | 184.84 / 184.84 / 392.50 + c | 834.84 / 834.84 / 1042.50 + c | 1209.84 | 1025.00 | 1135.00 (1135.84) | 292.34 / 42.34 / c |

Range of c for which each number holds (`symbol_terms`):

| Quantity | Holds while |
|---|---|
| 0.75 m stop and start | c <= 42.34 |
| 0.5 m stop and start | c <= 292.34 |
| park, stroke, L | c <= 117.34 |

Above c = 117.34 the 1 m class sets park to 1092.50 + c.

Record diff (`wip/s1_checks_r4.json` against `docs/sketches/s1_checks_r4.json`; 11 differing fields, MEASURED):
- timestamp;
- 1 m reported terms: `park_tip_by_plane_z_A.core_stop.core.length_optional` (1092.50 to "1092.50 + c for c >= 0"); `q9_options.plus 1 m.starts_z_A.core.length_optional` (917.5 to "1042.50 + c for c >= 0"); `q9_options.plus 1 m.start_minus_core_top.core.length_optional` (-125.00 to "c for c >= 0");
- added fields: `drawn_symbol_validity`; `stops_z_A` and `symbol_terms` in each of the three options.

spec_status, keys_read (all values), checks (17 pass, reasons equal), files_sha256 and every 0.5 / 0.75 m value are unchanged. Summary: timestamp line, the symbol-term lines, the 1 m park-by-plane entry and the Step 4 park-rule line (mass report section).

## 6 Run table (MEASURED, 2026-11-25)

| Command | Result | Time |
|---|---|---|
| `check_sketch.py --controls` (first full run) | Z 38/38, B 86/87, smoke 1/1; S1-1-B1 error (Correction 3) | 159 s |
| `check_sketch.py --controls` (final) | Z 38/38, B 87/87, smoke 1/1 (126/126; 117 prior all match), exit 0 | 158.7 s |
| `check_sketch.py s1 --rev 4` | 17/17 pass, to wip/ | 12.1 s |
| `s1_side_poses.py --rev 4` | 4 PNGs in wip/, byte-equal and pixel-equal to `docs/sketches/s1_pose_{load,start,capture_end,park}_r4.png` | 7.5 s |
| `s1_mass_report.py --rev 4` | `wip/s1_mass_report_r4.json` byte-equal to docs copy | 4.0 s |
| `check_sketch.py --stale` | 0 records, 0 differences, exit 0 | 2.8 s |
| `check_sketch.py --stale --include-unaccepted` | 1 record (wip/s1_checks_r4.json), 0 differences, exit 0 | 2.7 s |
| `check_sketch.py --baseline s1` | run 1 126/126, run 2 17/17, exit 0, to wip/ | 2.3 s |
| `--accept s1 --rev 4 --note "Design Notes 24"` on a temporary copy (`--docs-dir`/`--wip-dir`), then `--stale` there | exit 0; `--stale` 1 record, 0 differences | 3 s |

## 7 Orchestrator's accept

Run after P0L PASS, from the project root:
```
C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe docs/sketches/check_sketch.py --accept s1 --rev 4 --note "Design Notes 24"
C:\Users\UR\AppData\Local\Programs\Python\Python312\python.exe docs/sketches/check_sketch.py --stale
```
Expected output, taken from the dry run on a copy. The SHA prefixes and timestamp will differ for the timestamp-bearing files:
```
replace s1_checks_r4.json: 14 differing field(s): accepted; accepted_at (added); accepted_note (added); reported.drawn_symbol_validity (added); reported.park_tip_by_plane_z_A.core_stop.core.length_optional; reported.q9_options.0.5 and 0.75 m.stops_z_A (added); ... symbol_terms (added); timestamp
copied s1_checks_r4.json -> ...docs/sketches/s1_checks_r4.json: SHA-256 equal
replace s1_summary_r4.md: 63 differing line(s): [3, 31, ...]
copied s1_summary_r4.md -> ...: SHA-256 equal
replace s1_mass_report_r4.json: 0 differing field(s):
copied s1_mass_report_r4.json -> ...: SHA-256 equal
kept s1_pose_capture_end_r4.png (byte-equal, kept)      (and load, park, start)
copied fixtures/controls_results.json -> fixtures/controls_results.json: SHA-256 equal
kept fixtures/figs/ctrl_a.png (byte-equal)              (and ctrl_b.png, key.json)
copied baseline_red.json -> baseline_red.json: SHA-256 equal
accepted s1 r4: note 'Design Notes 24', at <timestamp>
```
Exit 0. Then `--stale`: "checked sketches/s1_checks_r4.json", "--stale: 1 record(s) checked, 0 difference(s)", exit 0.

Files staged by that accept: `s1_checks_r4.json`, `s1_summary_r4.md`, `fixtures/controls_results.json`, `baseline_red.json`. The mass report is byte-equal.

If P2 edits the overlay before the accept, re-run `s1 --rev 4` and `s1_mass_report.py --rev 4` first, then accept. A refusal prints its reason.

## 8 Open items

1. c range (Correction 2). The ruling holds only for c <= 42.34. For the Loftsman at P0L, and for Sean when he sets c (N11).
2. Travel and core-stop coupling (Correction 3). Any S2 edit to `upper.travel_max`, `collet.core_stop_z` or `core.length_*` can make S1 drawn values depend on c. check_stack refuses rather than guess.
3. The summary diff in `--accept` counts lines positionally. An insertion shows every later line as differing (63 above). Cosmetic.
4. `--accept` copies up the harness records only when all wip/ controls match. With a mismatch they stay in wip/ silently, and the accept still passes on the record. The Software Engineer may want this to block (P5, H6).
5. The H1 controls take the docs `s1_checks_r4.json` as a read-only template, with keys_read set from live values.

## 9 Gameplan lines to change

**l.124**

Old:
```
- `docs/sketches/check_sketch.py sN [--rev k]`: runs K1 to K9 and the sketch's own checks, writes `docs/sketches/sN_checks_r<k>.json` (per check: ID, result, measured value, threshold, Z result, B result, source tags; per file: SHA-256 of params.yaml and of the overlay, and the list of keys the spec reads with their values) and `sN_summary_r<k>.md` beside it (one screen: pass and fail per check, reported values, open items; the M2 summary Sean reads). `check_sketch.py --stale` compares each accepted revision's recorded key values with the live params and overlay and fails on any difference.
```

New:
```
- `docs/sketches/check_sketch.py sN [--rev k]`: runs K1 to K9 and the sketch's own checks, writes `docs/sketches/wip/sN_checks_r<k>.json` (per check: ID, result, measured value, threshold, Z result, B result, source tags; per file: SHA-256 of params.yaml and of the overlay, and the list of keys the spec reads with their values) and `wip/sN_summary_r<k>.md` (one screen: pass and fail per check, reported values, open items; the M2 summary Sean reads). Output rule (Design Notes 26 decision 1, `sketch_loader.output_path`): every unaccepted and verification output (sN runs, sketch PNGs, mass report, visual-gate file, `--controls` results and control figures, `--baseline`) goes to `docs/sketches/wip/` (git-ignored); only `--accept` writes to `docs/sketches/`. `check_sketch.py --accept sN --rev k --note "<Design Notes ref>"` sets accepted, accepted_note, accepted_at, copies the revision's wip/ outputs (and the wip/ controls results, control figures and baseline record when every control matched) up with SHA-256 equality, refuses on an absent record, a check not pass, an empty note or a PNG differing in pixels from an accepted one, and marks earlier accepted records of the sketch superseded_by k. `check_sketch.py --stale` compares the latest accepted, unsuperseded record per sketch with the live params and overlay and fails on any difference (`--include-unaccepted` adds the wip/ records). `check_sketch.py --baseline sN` assembles run 2 for sN (Z and B controls: H1-Z1, H1-Z2, H1-B1 to H1-B5).
```

**l.145** (end of the paragraph)

Old:
```
r4 added K8-Z5, K7-B20, K8-B15, K8-B16 and re-scoped K8-B7 to planted 3 (117 controls: Z 35, B 81, smoke 1; Manager re-run from `docs/sketches/` at the 1.1 close: 117/117 matched).
```

New:
```
r4 added K8-Z5, K7-B20, K8-B15, K8-B16 and re-scoped K8-B7 to planted 3 (117 controls: Z 35, B 81, smoke 1; Manager re-run from `docs/sketches/` at the 1.1 close: 117/117 matched). Step 1.2 step 0 added H1-Z1, H1-Z2, H1-B1 to H1-B5 (`--accept`, `--stale` supersession) and H5-Z, H5-B (park-rule symbol c) (126 controls: Z 38, B 87, smoke 1).
```

**l.154**

Old:
```
Red-first baseline (Principle 10), two runs, recorded in `docs/sketches/baseline_red.json` (the S1 stub record is docs/sketches/s1_checks_r0.json, copied from the frozen scratch folder at 1.2 step 0 (H3); a later sketch writes sN_checks_r0.json to docs/sketches/wip/ at its (c), copies it up with the accepted revision, and `check_sketch.py --baseline sN` assembles its run 2):
```

New:
```
Red-first baseline (Principle 10), two runs, recorded in `docs/sketches/baseline_red.json` (the S1 stub record is docs/sketches/s1_checks_r0.json, copied byte-equal from the frozen scratch folder at 1.2 step 0 (H3); a later sketch writes sN_checks_r0.json to docs/sketches/wip/ at its (c), copies it up with the accepted revision, and `check_sketch.py --baseline sN` assembles its run 2 into `wip/baseline_red.json`, run 2 per sketch under `run2_by_sketch`, prior records under dated keys, copied up by `--accept`; a sketch's stub expectations live in `checks_sN.py` STUB_EXPECT / STUB_CAUSE / SOURCES):
```

**l.206**

Old:
```
Unaccepted revision outputs (PNGs, checks JSON, summaries, visual-gate files) go where the Design Notes 25 output rule puts them; only the accepted revision's outputs are committed in `docs/sketches/`.
```

New:
```
Unaccepted revision outputs (PNGs, checks JSON, summaries, mass reports, visual-gate files) go to `docs/sketches/wip/` (git-ignored; `sketch_loader.output_path`, Design Notes 26 decision 1); `check_sketch.py --accept` copies the accepted revision's outputs up to `docs/sketches/` with SHA-256 equality, and a PNG that differs in pixels from an accepted one of the same name blocks the accept.
```

**l.650** (Echo Site Registry, park-rule row)

Old:
```
| Park rule: park = max(max_k start_k, entry plane `stop.collar_top_z` + max L) + `upper.load_clearance`; start_k = stop_k + travel; S1-3 measures from the core stop | S1 r4 spec `park_rule` (Step 4 expression `for_step4`; 1 m start-above-core term to add, Design Notes 25 H5) | DERIVED (S1 r4) |
```

New:
```
| Park rule: park = max(max_k start_k, entry plane `stop.collar_top_z` + max L) + `upper.load_clearance`; start_k = stop_k + travel; stop_k = max(stop.height_z, core_stop + L + g_stop - bore_ceiling_above_tip, core_stop + L + c - travel) with c (Sean, N11) a spec symbol reported as an expression (1 m: stop 392.50 + c, start 1042.50 + c); 0.5 and 0.75 m values unchanged for c <= 42.34, park 1209.84 / stroke 1025 / L 1140 for c <= 117.34; S1-3 measures from the core stop | S1 r4 spec `park_rule` and `symbols.c` (Step 4 expression `for_step4`; term added at 1.2 step 0, Design Notes 25 H5) | DERIVED (S1 r4) |
```
