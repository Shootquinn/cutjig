# Step 1.4 close fix pass (P10f), The Engineer: Manager close N1 (DEPS controls on the frozen record tree)

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\open14\p10f\`.
- Pre-change copy `pre\`.
- Red-first tree `prerun\` (pre-change code plus the new manifest and `deps_frozen_fixtures.py`), output `prerun_new.txt`.
- Accept simulation `accsim\`, output `accsim_run.txt`.
- Branch-deletion tree `del\`, output `deltest.txt`.
- DEPS-only run `deps_only.txt`.
- Final runs `run_controls.log`, `run_fast.log`, `run_s1.log` to `run_s4.log`, `run_stale.log`, `times.txt`.
- SHA-256 lists `sha_before.txt`, `sha_after.txt`.

## Corrections to the brief

1. **The fast tier holds 86 controls, not the 77 ruled at P0S** (MEASURED, run log "86 control(s) selected"). The 9 added:
   - S4-1-Z, S4-1-B1, S4-2-Z, S4-2-B2, S4-3-Z, S4-3-B2 and S4-FULL (1.4 P4: family S4-x and its smoke, per the `fast.yaml` header).
   - SPEC-Z and SPEC-B1 (1.4 P6: family SPEC).
   - Every one follows the P0S rule: a Z and a B per family, and every smoke control.
   - The 4 controls this pass adds are in family DEPS, which already has DEPS-Z and DEPS-B3 in the tier. The tier stays at 86.
2. **TASK 2 (pruning deletions ruled by The Software Engineer) has no ruling to apply.** P0S kept all 7 pairs and deleted none (Manager close DC1). No control was deleted.
3. **The s3 r9 re-run's `keys_read` holds 300 keys; the accepted `s3_checks_r9.json` holds 272** (MEASURED).
   - The 28 extra keys are S4-era leaves: carrier.\*, liner.\*, witness.\*, holder.insert_\*, collet.slit_\*, core.length_short, core.min_exposed, core.top_chamfer, nut.tommy_\*, receiver.key_\*, drill.kerf_standoff, collar.hole_dia and thread.hand.
   - The 272 shared keys are equal in value.
   - The pre-change code gives the same 300 keys (`pre_s3\`, MEASURED), so the cause predates this pass.
   - The Manager close reported s3 r9 as "equal". That does not hold on `keys_read`.
   - --stale reads only the recorded keys and stays at 0 differences.
   - Sent to the orchestrator (section 5).
4. **`_tmp()` still leaks.** `_scratch\cutjig\tmp` went from 805 to 834 entries over this pass's runs (MEASURED). N2 is outside this brief. The C: `deps_*` count stays at 113 (MEASURED), so this pass wrote nothing to C:.

## 1 FIX table

| Raiser | FIX id | Dry run | Change | Control | Status |
|---|---|---|---|---|---|
| The Manager (close) | N1 (DC1, DC2) | Not required under rule (h): no value, field setting or coordinate is set. Manager dry run (p10): dropping `superseded_by` left 13 of 18 red. This pass: DEPS-only run on the new code, 22/22 (MEASURED, `deps_only.txt`). | Five parts, listed below the table. | DEPS-Z6, DEPS-B14, DEPS-B15, DEPS-B16 (section 2) | CLOSED |

The change:
- **Frozen records.** `fixtures/deps_tree/` gains save-point-5 byte copies, taken from `open14\p0\pre\sketches\`:
  - `s1_checks_r8.json` (sha ebca440c), `s2_checks_r9.json` (cfd94ddf) and `s3_checks_r7.json` (b3b01847). Each differs from the live record only by the absent `superseded_by` (MEASURED).
  - `s1_mass_report_r8.json` (36316c8f) and `deps_exempt.json` (7476222a).
- **`_deps_tree`** reads only from `FROZEN`. The fallback to `SK` is removed, so a missing frozen file raises.
- **DEPS-Z2 and DEPS-Z4** run `cs.main` with `--docs-dir` set to `_frozen_docs()` (the frozen s1 r8, s2 r9 and mass report) and compare against the frozen SHA-256.
- **The `_frozen` guard** wraps all 17 DEPS fixtures in `step14_fixtures.py` and DEPS-Z5 in `s4_fixtures.py`. For each call it:
  - loads `cs.DEPS_EXEMPT` from the frozen exemption;
  - installs a `sys.addaudithook` "open" hook;
  - fails a result that opened a file of the live record set, with one issue per file.
- **The live record set** is the top level of `docs/sketches/`, matched by `LIVE_RECORD_RE`: `s*_checks_r*.json`, `s*_mass_report_r*.json`, `s*_summary_r*.md`, `s*_visual_gate_r*.md`, `s*_*_r*.png` and `deps_exempt.json`.

**Premise (rule (h)).** Every DEPS control reads its accepted records from `fixtures/deps_tree/`, never from the live record set, and the frozen tree matches its exemption. Enforcement:
- `deps_frozen_issues` checks three things:
  - every manifest entry of check DEPS names a fixture carrying `_deps_frozen`;
  - every frozen file is present;
  - every spec, script, spec_read, certifier and certifier-file SHA-256 in the frozen `deps_exempt.json` equals that of its frozen file.
- The guard enforces the premise at run time.
- Class: every manifest control of check DEPS, in every fixture module (`step14_fixtures.py`, `s4_fixtures.py`, `deps_frozen_fixtures.py`). The DEPS family reads no drawn view, so view scope does not apply.

**Independence evidence:**
- **Accept simulation** (`accsim\`, current code). In a copy of the tree:
  - the live s1 r8, s2 r9, s3 r7 records and the s1 r8 mass report are deleted;
  - s1 r10, s2 r11 and s3 r9 are superseded by new accepted r11, r12 and r10;
  - the live `deps_exempt.json` is emptied.

  All 22 DEPS controls match: Z 6/6, B 16/16 (MEASURED, `accsim_run.txt`).
- **Branch deletion** (`del\`). DEPS-Z is reverted to read `SK / "s3_checks_r7.json"`, and DEPS-Z4 runs without `--docs-dir`. Both go red (MEASURED, `deltest.txt`):
  - DEPS-Z: "DEPS fixture read the live record set: s3_checks_r7.json".
  - DEPS-Z4: the same text, naming s1_checks_r0.json, s1_checks_r10.json, s1_checks_r4.json, s1_checks_r7.json, s1_checks_r8.json and s1_mass_report_r10.json.

## 2 Controls added

The fixtures are in the new module `docs/sketches/fixtures/deps_frozen_fixtures.py`. They reach the guard and the lint through `getattr`. On the pre-change `step14_fixtures.py`, each B therefore reads clean and Z6 errors.

| ID | Planted | Reason substring | Pre-change code (MEASURED, `prerun_new.txt`) |
|---|---|---|---|
| DEPS-Z6 | none: live manifest and `fixtures/deps_tree/` | (clean) | error (no lint): red |
| DEPS-B14 | live manifest plus DEPS-BX, fixture `deps_frozen_fixtures.py::_unguarded` | "DEPS-BX: fixture deps_frozen_fixtures.py::_unguarded lacks the _frozen guard" (planted 1) | clean, 0 issues: red |
| DEPS-B15 | a guarded fixture opens `docs/sketches/s3_checks_r7.json`. The open is the plant: the audit event fires before the file lookup, so B15 stays red if r7 is later removed (accept simulation) | "DEPS fixture read the live record set: s3_checks_r7.json" (planted 1) | clean, 0 issues: red |
| DEPS-B16 | temp copy of the frozen tree with one field added to `s1_checks_r8.json` | "frozen tree: s2_checks_r9.json records s1_checks_r8.json sha256", "frozen tree: s3_checks_r7.json records s1_checks_r8.json sha256" (planted 2) | clean, 0 issues: red |

Existing DEPS controls on the new code: DEPS-Z to Z5 and DEPS-B1 to B13 all match. At the Manager close, 15 of the 18 were mismatches (MEASURED).

## 3 Runs

Every run is from `docs/sketches/`, with TMP and TEMP set to `D:\Unleashed Robotics\_scratch\cutjig\tmp` in the shell; the spawn workers inherit them. Walls MEASURED.

| Run | Result (MEASURED) | Wall |
|---|---|---|
| `--controls` (full, of record, 12 jobs) | 596 controls: Z clean 130/130, B fired 462/462, smoke 4/4; 0 mismatches; 5242.9 control-seconds; DEPS-Z4 106.4 s, DEPS-Z2 43.2 s | 471.5 s (474.9 s with start-up) |
| `--controls --fast` | 86 controls: Z 41/41, B 41/41, smoke 4/4 | 38.1 s (41.4 s) |
| `s4 --rev 2` | 14/14; equal to `s4_checks_r2.json` except `timestamp`, `accepted*` | 44.2 s |
| `s3 --rev 9` | 16/16; checks equal; `keys_read` 300 against 272 recorded (Corrections 3) | 35.8 s |
| `s2 --rev 11` | 18/18; equal except `timestamp`, `accepted*` | 73.9 s |
| `s1 --rev 10` | 19/19; equal except `timestamp`, `accepted*` and K8 `b_result` ("fired 126/128" recorded, "fired 128/128" now, from the control tally) | 36.5 s |
| `--stale` | 4 records, 0 differences; deps 4 records, 0 exempt, 0 differences; X1 pass (72 shared rows, section_true on 7) | 6.4 s |

## 4 SHA-256

Files under `docs/sketches/` (wip and caches excluded): 115 before, 121 after. Lists: `sha_before.txt` and `sha_after.txt`.
- **Equal:** the 91 files outside `fixtures/` (records, PNGs, specs, overlay, harness, scripts). SHA-256 equal before and after (MEASURED).
- **Changed:** `fixtures/manifest.yaml`, `fixtures/step14_fixtures.py` and `fixtures/s4_fixtures.py` (CRLF kept).
- **Added:** `fixtures/deps_frozen_fixtures.py`, plus five files in `fixtures/deps_tree/`: `s1_checks_r8.json`, `s2_checks_r9.json`, `s3_checks_r7.json`, `s1_mass_report_r8.json` and `deps_exempt.json`.
- **Unexpected differences:** none.

## 5 Items returned or sent to Sean

- **Returned to a raiser:** none.
- **To the orchestrator:** the s3 r9 `keys_read` count (Corrections 3).
  - The re-run records 28 keys more than the accepted record, and the pre-change code does the same.
  - No value moves.
  - Whether a re-record is needed is the orchestrator's call.
- **Not done in this pass** (outside the N1 brief; carried by name):
  - N2: `_tmp()` per-call cleanup, or a spawn-rooted temp folder (The Engineer).
  - The `--accept s1` mass-report precondition with its Z and B (Manager close section 6, "at the N1 pass").
  - D4: M1 control composition (awaits Sean's answer).
- **To Sean:** none. No design value changed, and no key read by an accepted record changed.

## 6 Gameplan lines to change

1. detail 1.0, `check_sketch.py` command bullet (line 124). The DEPS control clause gains the frozen-tree premise and its controls.

Old:
```
- `docs/sketches/check_sketch.py sN [--rev k]`: runs K1 to K9 and the sketch's own checks, writes `docs/sketches/wip/sN_checks_r<k>.json` (per check: ID, result, measured value, threshold, Z result, B result, source tags; per file: SHA-256 of params.yaml and of the overlay, and the list of keys the spec reads with their values) and `wip/sN_summary_r<k>.md` (one screen: pass and fail per check, reported values, open items; the M2 summary Sean reads). Output rule (Design Notes 26 decision 1, `sketch_loader.output_path`): every unaccepted and verification output (sN runs, sketch PNGs, mass report, visual-gate file, `--controls` results, `--baseline`) goes to `docs/sketches/wip/` (git-ignored); only `--accept` writes to `docs/sketches/`. `check_sketch.py --accept sN --rev k --note "<Design Notes ref>"` sets accepted, accepted_note, accepted_at, copies the revision's wip/ outputs (and the wip/ controls results and baseline record when every control matched) up with SHA-256 equality, refuses on an absent record, a check not pass, an empty note, a PNG differing in pixels from an accepted one or a wip/ controls results file with any control not matched (1.2 (c) SW FIX 4, H1-Z3, H1-B6), and marks earlier accepted records of the sketch superseded_by k. `check_sketch.py --stale` compares the latest accepted, unsuperseded record per sketch with the live params and overlay and fails on any difference (`--include-unaccepted` adds the wip/ records). `check_sketch.py --baseline sN` assembles run 2 for sN (Z and B controls: H1-Z1 to H1-Z3, H1-B1 to H1-B8). `check_sketch.py --controls --jobs N` runs the manifest in N spawn worker processes (default min(cpu_count - 2, 12)), rows in manifest order, per-control id, expected, observed, reason and match equal to `--jobs 1` (1.3 step 0, RUN-Z, RUN-B; 246 controls 113 s at 12 jobs against 775 s serial on 230); `--only <id globs or check ids>` writes `wip/fixtures/controls_results_partial.json`, "PARTIAL, not a record", never read by control_tally or `--accept` (destination from the pure function `controls_dst`, RUN-Z2, RUN-B2; its call site in `controls()`, RUN-B4); an `--only` that selects nothing exits 1 (RUN-B3); runs of record use the full set; per-control equality between job counts excludes the temporary-directory path in the H1-B5 reason (Software Engineer P0S). Every sN run ends with check RPT: each id in the spec's `reported_items` ({id, text, source, needs_drawing}) has a value from `checks_sN.py reported(ctx)["items"]`, cause absent on rev 0 for needs_drawing items; the summary carries a Reported items table; s1 r7 and s2 r5 read "not declared, exempt (accepted before RPT)" by record name; `--accept` refuses through RPT and refuses any record without an RPT row; the RPT reason states its cause (RPT-Z, RPT-Z2, RPT-Z3, RPT-B1 to RPT-B6, H1-B7, H1-B8; 1.3 open O10; Software Engineer P0S FIX 2, FIX 3). `run_control` routes any `S<n>-` check to `checks_s<n>.py`; `checks_sN.py K_CHECKS` overrides the K list (1.3 open O13). 1.4 step 0 and P0f (`research/sean/cr_scratch/step1.4_engineer_step0.md`, `step1.4_engineer_step0_fixes.md`): `--controls` submits tasks longest first by the last run's seconds, and the YAML parse (`sketch_loader.load_yaml`) and the unmutated live drawings (`fixtures/builders.draw_cache`) are cached per worker, a fresh copy per call (rows equal to the uncached run on id, expected, observed, reason and match; 413 controls 225.7 s to 128.4 s at 12 jobs); `--controls --fast` runs the fast tier `fixtures/fast.yaml` (per check family the least-time Z and the least-time B, and every smoke control; Software Engineer P0S ruling; 77 controls, 29.1 s at 12 jobs) to the partial destination, PARTIAL, not a record (FAST-Z, FAST-B1 to B3, RUN-Z3, RUN-B5 on the call site); every sN run writes `deps` (spec and script {path, sha256}; spec_read {path, sha256}, every other spec a check read, for a record with chains the specs sym_lint reads, and every spec a check records on ctx.specs_read at run time (the S4 RPT reads s3_spec.yaml through checks_s3.loads: Software Engineer P5 FIX 5, DEPS-Z5); certifiers {sketch, path, rev, sha256, files} for every accepted record a check resolved at run time, S3-3 and the S2 tip-force report, files being the side files read through that record, the S1 mass report), `--accept` copies it unchanged, and `--stale` gains a deps branch: spec, script and spec_read SHA-256 recomputed, each certifier the latest accepted, unsuperseded record at the recorded name and SHA-256 and each of its files at its SHA-256; a record without deps reads the deps its entry in `docs/sketches/deps_exempt.json` carries (s1_checks_r8.json, s2_checks_r9.json, s3_checks_r7.json, each with the deps of its P0f re-record; S3 r7 stays the accepted S3 record until S3 r8) and fails with no entry or an entry carrying no deps (DEPS-Z, DEPS-Z2 to Z4, DEPS-B1 to B13; Loftsman P0L FIX 1 to 3, Software Engineer P0S FIX 3, 4); `check_sketch.py --m1-controls --out <dir> --key <path>` draws the four reviewer control figures as `m1c_<token>.png` with fresh `secrets.token_hex(3)` tokens in a shuffled write order and writes the key (token, role, criterion, expected verdict) to <path>, refusing a non-empty <dir>, a <path> inside the project root and a <path> inside <dir>, containment tested by file identity and by the spelling-free path (M1C-Z, M1C-Z2, M1C-B1 to B5; Software Engineer P0S FIX 5); `--controls` and `--accept` write and copy no control figure, and the committed `docs/sketches/fixtures/figs/` is deleted. 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md`): `--controls` submits tasks longest first by the last run's seconds, and the YAML parse (`sketch_loader.load_yaml`) and the unmutated live drawings (`fixtures/builders.draw_cache`) are cached per worker, a fresh copy per call (rows equal to the uncached run on id, expected, observed, reason and match; 413 controls 225.7 s to 128.4 s at 12 jobs); `--controls --fast` runs the fast tier `fixtures/fast.yaml` (every check family's least-time Z and one B per branch, a branch being the manifest finding that added the B) to the partial destination, PARTIAL, not a record (FAST-Z, FAST-B1, FAST-B2, RUN-Z3); every sN run writes `deps` (spec and script {path, sha256}; certifiers {sketch, path, rev, sha256} for every accepted record a check resolved at run time, S3-3 today), `--accept` copies it unchanged, and `--stale` gains a deps branch: spec and script SHA-256 recomputed, each certifier the latest accepted, unsuperseded record at the recorded name and SHA-256, and a record without deps fails unless named in `DEPS_EXEMPT` (s1_checks_r8.json, s2_checks_r9.json) (DEPS-Z, DEPS-Z2, DEPS-B1 to B6); `check_sketch.py --m1-controls --out <dir> --key <path>` draws the four reviewer control figures as `m1c_<token>.png` with fresh `secrets.token_hex(3)` tokens and writes the key (token, role, criterion, expected verdict) to <path>, refusing a non-empty <dir>, a <path> inside the project root and a <path> inside <dir>; `--controls` and `--accept` write and copy no control figure (M1C-Z, M1C-Z2, M1C-B1 to B4).
```
New:
```
- `docs/sketches/check_sketch.py sN [--rev k]`: runs K1 to K9 and the sketch's own checks, writes `docs/sketches/wip/sN_checks_r<k>.json` (per check: ID, result, measured value, threshold, Z result, B result, source tags; per file: SHA-256 of params.yaml and of the overlay, and the list of keys the spec reads with their values) and `wip/sN_summary_r<k>.md` (one screen: pass and fail per check, reported values, open items; the M2 summary Sean reads). Output rule (Design Notes 26 decision 1, `sketch_loader.output_path`): every unaccepted and verification output (sN runs, sketch PNGs, mass report, visual-gate file, `--controls` results, `--baseline`) goes to `docs/sketches/wip/` (git-ignored); only `--accept` writes to `docs/sketches/`. `check_sketch.py --accept sN --rev k --note "<Design Notes ref>"` sets accepted, accepted_note, accepted_at, copies the revision's wip/ outputs (and the wip/ controls results and baseline record when every control matched) up with SHA-256 equality, refuses on an absent record, a check not pass, an empty note, a PNG differing in pixels from an accepted one or a wip/ controls results file with any control not matched (1.2 (c) SW FIX 4, H1-Z3, H1-B6), and marks earlier accepted records of the sketch superseded_by k. `check_sketch.py --stale` compares the latest accepted, unsuperseded record per sketch with the live params and overlay and fails on any difference (`--include-unaccepted` adds the wip/ records). `check_sketch.py --baseline sN` assembles run 2 for sN (Z and B controls: H1-Z1 to H1-Z3, H1-B1 to H1-B8). `check_sketch.py --controls --jobs N` runs the manifest in N spawn worker processes (default min(cpu_count - 2, 12)), rows in manifest order, per-control id, expected, observed, reason and match equal to `--jobs 1` (1.3 step 0, RUN-Z, RUN-B; 246 controls 113 s at 12 jobs against 775 s serial on 230); `--only <id globs or check ids>` writes `wip/fixtures/controls_results_partial.json`, "PARTIAL, not a record", never read by control_tally or `--accept` (destination from the pure function `controls_dst`, RUN-Z2, RUN-B2; its call site in `controls()`, RUN-B4); an `--only` that selects nothing exits 1 (RUN-B3); runs of record use the full set; per-control equality between job counts excludes the temporary-directory path in the H1-B5 reason (Software Engineer P0S). Every sN run ends with check RPT: each id in the spec's `reported_items` ({id, text, source, needs_drawing}) has a value from `checks_sN.py reported(ctx)["items"]`, cause absent on rev 0 for needs_drawing items; the summary carries a Reported items table; s1 r7 and s2 r5 read "not declared, exempt (accepted before RPT)" by record name; `--accept` refuses through RPT and refuses any record without an RPT row; the RPT reason states its cause (RPT-Z, RPT-Z2, RPT-Z3, RPT-B1 to RPT-B6, H1-B7, H1-B8; 1.3 open O10; Software Engineer P0S FIX 2, FIX 3). `run_control` routes any `S<n>-` check to `checks_s<n>.py`; `checks_sN.py K_CHECKS` overrides the K list (1.3 open O13). 1.4 step 0 and P0f (`research/sean/cr_scratch/step1.4_engineer_step0.md`, `step1.4_engineer_step0_fixes.md`): `--controls` submits tasks longest first by the last run's seconds, and the YAML parse (`sketch_loader.load_yaml`) and the unmutated live drawings (`fixtures/builders.draw_cache`) are cached per worker, a fresh copy per call (rows equal to the uncached run on id, expected, observed, reason and match; 413 controls 225.7 s to 128.4 s at 12 jobs); `--controls --fast` runs the fast tier `fixtures/fast.yaml` (per check family the least-time Z and the least-time B, and every smoke control; Software Engineer P0S ruling; 77 controls, 29.1 s at 12 jobs) to the partial destination, PARTIAL, not a record (FAST-Z, FAST-B1 to B3, RUN-Z3, RUN-B5 on the call site); every sN run writes `deps` (spec and script {path, sha256}; spec_read {path, sha256}, every other spec a check read, for a record with chains the specs sym_lint reads, and every spec a check records on ctx.specs_read at run time (the S4 RPT reads s3_spec.yaml through checks_s3.loads: Software Engineer P5 FIX 5, DEPS-Z5); certifiers {sketch, path, rev, sha256, files} for every accepted record a check resolved at run time, S3-3 and the S2 tip-force report, files being the side files read through that record, the S1 mass report), `--accept` copies it unchanged, and `--stale` gains a deps branch: spec, script and spec_read SHA-256 recomputed, each certifier the latest accepted, unsuperseded record at the recorded name and SHA-256 and each of its files at its SHA-256; a record without deps reads the deps its entry in `docs/sketches/deps_exempt.json` carries (s1_checks_r8.json, s2_checks_r9.json, s3_checks_r7.json, each with the deps of its P0f re-record; S3 r7 stays the accepted S3 record until S3 r8) and fails with no entry or an entry carrying no deps (DEPS-Z, DEPS-Z2 to Z4, DEPS-B1 to B13; Loftsman P0L FIX 1 to 3, Software Engineer P0S FIX 3, 4); every DEPS control reads its accepted records from `docs/sketches/fixtures/deps_tree/` (save-point-5 byte copies of s1 r8, s2 r9, s3 r7, the S1 r8 mass report and `deps_exempt.json`; Z2 and Z4 through `--docs-dir`), never from the live record set, under the `_frozen` guard (frozen exemption loaded for the call; an audit hook fails a DEPS control that opens a live record file), premise lint `deps_frozen_issues` (every manifest DEPS fixture guarded; the frozen tree equal to its exemption SHA-256) (DEPS-Z6, DEPS-B14 to B16; Manager close N1, P10f); `check_sketch.py --m1-controls --out <dir> --key <path>` draws the four reviewer control figures as `m1c_<token>.png` with fresh `secrets.token_hex(3)` tokens in a shuffled write order and writes the key (token, role, criterion, expected verdict) to <path>, refusing a non-empty <dir>, a <path> inside the project root and a <path> inside <dir>, containment tested by file identity and by the spelling-free path (M1C-Z, M1C-Z2, M1C-B1 to B5; Software Engineer P0S FIX 5); `--controls` and `--accept` write and copy no control figure, and the committed `docs/sketches/fixtures/figs/` is deleted. 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md`): `--controls` submits tasks longest first by the last run's seconds, and the YAML parse (`sketch_loader.load_yaml`) and the unmutated live drawings (`fixtures/builders.draw_cache`) are cached per worker, a fresh copy per call (rows equal to the uncached run on id, expected, observed, reason and match; 413 controls 225.7 s to 128.4 s at 12 jobs); `--controls --fast` runs the fast tier `fixtures/fast.yaml` (every check family's least-time Z and one B per branch, a branch being the manifest finding that added the B) to the partial destination, PARTIAL, not a record (FAST-Z, FAST-B1, FAST-B2, RUN-Z3); every sN run writes `deps` (spec and script {path, sha256}; certifiers {sketch, path, rev, sha256} for every accepted record a check resolved at run time, S3-3 today), `--accept` copies it unchanged, and `--stale` gains a deps branch: spec and script SHA-256 recomputed, each certifier the latest accepted, unsuperseded record at the recorded name and SHA-256, and a record without deps fails unless named in `DEPS_EXEMPT` (s1_checks_r8.json, s2_checks_r9.json) (DEPS-Z, DEPS-Z2, DEPS-B1 to B6); `check_sketch.py --m1-controls --out <dir> --key <path>` draws the four reviewer control figures as `m1c_<token>.png` with fresh `secrets.token_hex(3)` tokens and writes the key (token, role, criterion, expected verdict) to <path>, refusing a non-empty <dir>, a <path> inside the project root and a <path> inside <dir>; `--controls` and `--accept` write and copy no control figure (M1C-Z, M1C-Z2, M1C-B1 to B4).
```
