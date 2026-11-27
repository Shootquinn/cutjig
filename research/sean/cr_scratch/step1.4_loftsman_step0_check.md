# Step 1.4 step 0 (P0L), The Loftsman: record dependency branch (G5) against the S3-3 certifier semantics

## Corrections to the brief

1. The orchestrator ruling exempts `s3_checks_r7.json` from the deps branch by name until S3 r8. The code does not hold it yet: `DEPS_EXEMPT` (check_sketch.py l.800) names `s1_checks_r8.json` and `s2_checks_r9.json` only (MEASURED). Today the live `--stale` reads red on "s3_checks_r7.json: deps not recorded" (Engineer section 9).
2. The premise "S3 r7 reads stale once S1 r9 supersedes r8, until s3 is re-run on the S1 r9 record" fails if the ruling goes into code as a name-only entry. A record without deps that is exempt by name has no certifier list, so superseding S1 r8 or S2 r9 changes nothing it reports (dry run A1, FIX 1). The Engineer's accept order (S1 r9, then S2 r10, then the S3 r8 run and accept) passes through exactly that window.

## 1 Recorded certifier set against the set S3-3 resolves

Spec (`s3_spec.yaml` chains, MEASURED): 48 links. Certifier heads: S3 18, S1 10, S2 10, "declared" 15, "none" 8. Record certifier sketches named: {S1, S2}.

Code path (checks_s3.py):
- `_records` (l.201) returns the latest accepted, unsuperseded record per sketch through `check_sketch.stale_records` (l.766), together with its key-branch `stale_diffs`.
- In the `s3_3` link loop (l.386 to l.406), every certifier of every link is visited. The loop does not stop at the first pass, so "passes on any certifier" still resolves all of them.
- For a head of S1 or S2 that is present in `_records`, `ctx.certifiers[head.lower()] = p` is set before the staleness and K7 tests run. Every resolved record is therefore recorded, whatever its verdict.
- `record_deps` (check_sketch.py l.812) writes {sketch, path, rev, sha256} per entry, at l.683, after `reported`.

Resolved set equals recorded set: {s1: s1_checks_r8.json, s2: s2_checks_r9.json} (MEASURED, `wip/s3_checks_r7.json` deps). No spec certifier is left unresolved. Sketch keys agree: `_records` upper-cases `rec["sketch"]` ("s1"), and `stale_deps` keys `latest` on `rec["sketch"]` ("s1") (MEASURED in both records).

Hand trace, chain c link `base_plate|base_frame` (kind face_record; s3_spec.yaml l.185):
1. Spec certifiers: "S1 base_frame|base_plate C", "S2 base_plate|base_frame z-contact".
2. Head S1: `stale_records(docs)` gives s1_checks_r8.json (accepted true, superseded_by none, highest accepted rev among r0, r4, r7, r8; MEASURED). Key-branch diffs: 0. `ctx.certifiers["s1"]` = that path.
3. `_pair_ok` on the S1 r8 K7 tests at the section pose capture_end: entry {pair base_frame|base_plate, class C, state C, distance 0.0, basis "XZ projection (exact)"} (MEASURED). State C is in C_STATES ("C", "z-contact", "plan-contact"), so the link is ok.
4. Head S2: s2_checks_r9.json, entry {pair base_plate|base_frame, state z-contact, z_gap 0.0, overlap 186000.0} (MEASURED). Also ok, and resolved and recorded.
5. Listed by S3-3 as "c base_plate|base_frame face_record" (MEASURED, wip record reason).
6. deps entry {sketch s1, path s1_checks_r8.json, rev 8, sha256 ebca440c9396c0da...}. SHA-256 of docs/sketches/s1_checks_r8.json: ebca440c9396c0da5fed3b43fb00ca60b831f4b4b2973b4dc280353fff7e8e38 (MEASURED). Equal. The S2 entry cfd94ddf8299293a... equals docs/sketches/s2_checks_r9.json (MEASURED).

Verdict R1 (recorded set = resolved set): PASS.

## 2 Firing and clean behaviour, and routes past the branch

Scratch tree `D:\Unleashed Robotics\_scratch\cutjig\open14\p0l\ws` (params.yaml and docs/sketches copied, wip/ excluded). The Engineer's S3 r7 re-record, which carries deps, is placed as accepted. `stale_deps` was called directly (scripts `dry.py`, `fixdry.py`, `fixdry2.py` in the same folder). All results MEASURED:

| Case | Deps differences | Reason |
|---|---|---|
| unchanged tree | 0 | (2 exempt notes) |
| S1 r9 accepted over r8 | 1 on S3 | "deps certifier s1 recorded s1_checks_r8.json, latest accepted is s1_checks_r9.json (certifier superseded)" |
| s1_checks_r8.json edited (one byte) | 1 | "deps certifier s1_checks_r8.json sha256 recorded ebca440c9396, live b75a78eeeb3a" |
| s2_checks_r9.json missing | 1 | "no accepted, unsuperseded record of s2" |
| s1_checks_r8.json accepted flag cleared | 1 | "no accepted, unsuperseded record of s1" |

Superseded, edited and missing all fire, and an unchanged tree stays clean. The `--accept` supersession rewrites the old record, which also changes its SHA-256. The name test runs first (elif), so the reason reads "certifier superseded".

Routes by which S3-3's input changes and `--stale` stays clean:

**Route 1, exemption window (FIX 1).** `s3_checks_r7.json` is exempt by name and carries no deps. S1 r9 is then accepted over r8.
- Dry run A1: 0 differences, so S3 r7 reads clean while its S1 certifier is superseded. S2 r10 over r9 behaves the same way.
- This window opens at the first P6 accept and lasts until S3 r8 is accepted.

**Route 2, SYM specs (FIX 2).** S3-3 certifies the a and b links whose certifiers read "none" by symmetry from c, through `sym_lint(ctx.specs)`. `ctx.specs` is unset, so `sym_lint` reads `specs_in(HERE)`: s1_spec.yaml, s2_spec.yaml and s3_spec.yaml. Only s3_spec.yaml is in S3 deps.
- Rows nut_a and nut_b appear in s1_spec and s2_spec but not in s3_spec (MEASURED from the YAML feature ids).
- An identical edit to both, nut_a place theta `jackscrew.angle[1]` to `[0]`, passes X1 (s1 = s2) and leaves every key value unchanged.
- Live `--stale` in the scratch tree: key branch 0, deps 0 (S1 r8 and S2 r9 exempt), X1 pass, exit 0.
- S3 re-run on that tree: SYM fail (2 issues) and S3-3 fail with 8 links open (chains a and b: anchor|screw, screw|nut, nut|nut_housing, nut_housing|ring, each "symmetry premise (SYM) fails").
- Once S1 and S2 carry deps, their own spec hashes fire on such an edit, but the S3 record is still not named.

**Route 3, S2 reads an S1 side file outside deps (FIX 3, same G5 class: certifier records).**
- `checks_s2.accepted_s1_mass_report` (l.249) resolves the latest accepted, unsuperseded S1 record and reads `s1_mass_report_r<k>.json` for the tip_force_footprint reported item. It does not set `ctx.certifiers`.
- The S2 re-record's deps hold `certifiers: []`, while its item basis reads "s1_mass_report_r8.json tip_force_at_com_N (latest accepted S1 report)" (MEASURED, `wip/s2_checks_r9.json`).
- An edit to s1_mass_report_r8.json reads 0 differences (MEASURED).
- An S2 r10 run before S1 r9 is accepted would carry the r8 tip force. Once accepted, nothing flags it. The mass report is a separate file, so the S1 record's SHA-256 does not cover it.

**NOTES (no FIX):**
- N1: a certifier record that turns stale by keys after the S3 run is flagged on its own record by the key branch, so `--stale` is red. The S3 record that relied on it is not named. Attribution only.
- N2: `--accept` does not test deps. A record whose deps are already stale at accept time is accepted, and `--stale` goes red afterwards. A refusal through `stale_deps(docs, wip, [(src, rec)])` before the copy would close it at the gate.
- N3: a certifier sketch with no accepted record at run time is not recorded ("no accepted record" path, l.390). A later accept of that sketch does not stale the S3 record. No live case: S1 and S2 are accepted.
- N4: harness modules (checks_sN.py, sketch_common.py, check_stack.py) are outside deps, as R2 a states (Engineer open item 6).

FIX 1 (route 1). An exemption entry for a record without deps carries the deps that record would hold, and `stale_deps` reads them.
- For s3_checks_r7.json, use the deps block of the Engineer's re-record `wip/s3_checks_r7.json`: spec s3_spec.yaml 015aa79edc255a44..., script s3_jackscrew_section.py 451478458e3bc765..., certifiers s1 s1_checks_r8.json ebca440c..., s2 s2_checks_r9.json cfd94ddf....
- Dry run (monkeypatched `stale_deps`, scratch tree):
  - unchanged: 0 differences.
  - S1 r9 over r8: 1, "certifier superseded".
  - S2 r10 over r9: 1, "certifier superseded".
- Control: one B, "s3_checks_r7.json exempt with deps; temp S1 r9 accepted; fires certifier superseded". It reads clean on the name-only exemption (A1).

FIX 2 (route 2). `record_deps` also records every spec a check read at run time ({path, sha256}; for a record with chains, the specs `sym_lint` reads), and `stale_deps` recomputes them.
- Dry run:
  - unchanged: 0.
  - nut_a edit in s1 and s2: 2 differences, "deps spec_read s1_spec.yaml sha256 recorded a585abc34bea, live 9437704e4078" and the same for s2_spec.yaml (ef3993811224 to 4e2a39d15e61).
- Control: B with that plant. On the pre-change code it reads clean, as above.

FIX 3 (route 3). `accepted_s1_mass_report` sets `ctx.certifiers["s1"]`, and the certifier entry carries the side files read through it (`files: [{path, sha256}]`). `stale_deps` recomputes them.
- Dry run on an S2 record with those deps:
  - unchanged: 0 S2 differences.
  - s1_mass_report_r8.json edited: 1, "deps certifier s1 file s1_mass_report_r8.json sha256 recorded 36316c8fc457, live 1e38e2430abd".
  - S1 r9 over r8: 1, "certifier superseded".
- Consequence for the Engineer's section 11 order: S2 r10, like S3 r8, is run again after S1 r9 is accepted and before it is accepted itself.
- Control: B per plant (file edited, S1 superseded).

Verdict R2 (fires on superseded, edited, missing; clean on unchanged): PASS on the three cases named. Routes: 3, each a FIX.

## 3 LF1.3-11

`s2_spec.yaml` l.94 source now reads "s1_mass_report_r8.json tip_force_at_com_N, lever icd.footprint_y / 2" (MEASURED). The code basis that is reported matches it ("s1_mass_report_r8.json ... (latest accepted S1 report)", wip/s2_checks_r9.json). Closed.

NOTE: the spec text names a revision literal and goes stale again when S1 r9 is accepted. At the S2 r10 batch, revision-free wording ("s1_mass_report_r<k>.json of the latest accepted S1 record, tip_force_at_com_N; lever icd.footprint_y / 2") would end the recurrence.

Verdict R3: CLOSED.

## Gameplan lines to change

none
