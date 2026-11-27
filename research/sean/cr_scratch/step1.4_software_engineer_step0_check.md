# Step 1.4 step 0 check (P0S), The Software Engineer

## Corrections to the brief

1. Pruning candidates: the Engineer's table puts S3-3-B2 / S3-3-B8 and K7-B31 / K7-B34 on the same branch. Each pair is on two branches (R1 below). No candidate is a duplicate.
2. My full `--controls` wall, 137.4 s (MEASURED), was taken with two other reviewers loading the same 16 CPUs. The Engineer's 128.5 s is the uncontended figure.
3. Tree reviewed: the SHA-256 values of check_sketch.py, sketch_common.py, fixtures/builders.py, step14_fixtures.py, manifest.yaml and fast.yaml under docs/sketches/ match the "After" column of the Engineer's section 10 (MEASURED). Every run below used a scratch copy under `D:\Unleashed Robotics\_scratch\cutjig\open14\p0s\` (live/, pre/, mut_A to mut_F/).

## Verdicts

| Req | Verdict | FIX |
|---|---|---|
| R1 profile, fast tier, pruning (G4) | FIX | 1, 2 |
| R2 deps and the --stale deps branch (G5) | FIX | 3, 4 |
| R3 blinded M1 controls (G2) | FIX | 5 |
| R4 rule (l) by class | FIX | 6, 7 |
| R5 C1.3-b branches | FIX | 8, 9 |
| Task 6 full --controls, per-control equality | PASS | none |

9 FIX, 6 NOTE.

## R1 Pruning ruling

A deletion needs another control firing on the same branch with the same reason for the same defect class. None of the seven pairs meets that test.

| Pair | Ruling | Reason |
|---|---|---|
| K7-B31 / K7-B34 | KEEP both | B34 plants the declaration on the fixed member only (Loftsman 1.2 (c) NOTE 1: "side sweep reads only the moving row's list"). It exercises the read of the fixed row's list. A defect in that read leaves B31 firing and B34 clean. |
| RPT-B1 / RPT-B5 | KEEP both | Two inputs: the item missing from the reported dict, and the item present with value None. Each costs 0.0 s (MEASURED), so deleting one saves nothing. |
| S3-3-B2 / S3-3-B8 | KEEP both | B8 plants the pair at pose load only, so it fires only through the pose filter. B2 removes the pair entirely. A defect that admits a pair at any pose leaves B2 firing and B8 clean. NOTE 5 covers the reason text. |
| K7-B4 / K7-B8 | KEEP both | Side and plan swept forms (as the Engineer states). |
| K8-B1 / K8-B8 | KEEP both | Coordinates against the artist transform (TP-1 chain). |
| K3-B8 / K3-B9 | KEEP both | Text outside the canvas against the savefig premise branch. |
| K8-B39 / K8-B49 | KEEP both | The two ends of the alpha band. |

Ruled: 7 kept, 0 deleted, 0 control-seconds and 0 s wall saved (DERIVED). The three pairs the Engineer listed as same-branch total 12.1 control-seconds, about 1 s wall at 12 jobs (DERIVED from the per-control seconds). Pruning is not needed to meet 200 s.

## R1 Fast tier ruling (G4) and full set

- With one B per branch the tier keeps 314 of 444 controls. It ran 103.3 s (Engineer, MEASURED) and 110.7 s (mine, contended, MEASURED), against 128.5 s for the full set. It saves about 25 s per run, and every new B branch needs a fast.yaml edit or FAST-Z goes red. Branch coverage at that price is ceremony: branch coverage is the full set's job at every run of record (end of (c), each revision's final run, accept, close), and that rule stands.
- Ruling: the fast tier is, per check family, the least-time Z, the least-time B and the three smoke controls (S1-FULL, S2-FULL, S3-FULL). That is 77 controls. MEASURED on my scratch copy at 12 jobs (`--only` with the 77 ids, picked by least seconds from the Engineer's final run): **29.2 s**, all match (Z 37/37, B 37/37, smoke 3/3); 23.7 s without the smoke controls. The 60 s target stands and is met. This matches DC1 as written ("every check family has its Z and at least one B").
- Option (ii) from the Engineer's list (one build of each drawing per run, shared across workers) is not needed. Option (iii) (K4 cost on live S3) is moot.
- The fast tier is not read by `control_tally` or `--accept`: both read `CONTROLS_RESULTS` only, and `controls_dst(..., fast=True)` returns the partial file (RUN-Z3). PASS, apart from the call-site gap in FIX 1.
- Full set: 444 controls, 128.5 s (Engineer) and 137.4 s (mine, contended) against 200 s. PASS.
- The drawing cache (`draw_cache`): rows are equal to the uncached run (Engineer, MEASURED; my run reproduces the rows). Accepted as an R1 e speedup. NOTE 4 covers the key's reach.

## R2 Deps

- Each dependency kind has a B: certifier superseded (DEPS-B1), certifier edited (B2), spec (B3), script (B4). Exemption edges: a non-exempt record without deps (B5), and a later revision of an exempt sketch (B6). The exempt case itself is DEPS-Z.
- Red by branch deletion, MEASURED in scratch:
  - `elif cur.name != c.get("path")` replaced by `elif False` (mut_A): DEPS-B1 mismatches, because the reason changes from "certifier superseded" to the SHA-256 line.
  - `elif _sha(f) != d.get("sha256")` replaced by `elif False` (mut_E): DEPS-B3 and DEPS-B4 read clean, mismatch.
- Pre-change replay of all 31 new controls on the pre-change tree (check_sketch.py SHA-256 ffd7aee24aec8fb3, MEASURED): DEPS-B1 to B6 clean, DEPS-Z2 fires, DEPS-Z clean. This equals the Engineer's section 8.
- In code, the legacy exemption covers s1_checks_r8.json and s2_checks_r9.json by name only: PASS. The orchestrator ruling adds s3_checks_r7.json; FIX 4 covers that change.
- Two branches of `stale_deps` have no B (FIX 3).

## R3 Blinded controls

- `--m1-controls --out <p0s>\m1c_out --key <p0s>\m1c_key\key.json`: exit 0. The out folder holds four files, m1c_0d914b.png, m1c_645f89.png, m1c_6b532a.png and m1c_cd620d.png, and nothing else (MEASURED). The key was not opened.
- `--controls` wrote no figure: after my full run, `wip/fixtures/` holds controls_results.json and controls_results_partial.json only (MEASURED).
- `ctrl_[a-d]` and `key.json` occur 0 times in check_sketch.py and fixtures/builders.py (MEASURED by search). The committed `fixtures/figs/` (ctrl_a.png to ctrl_d.png, key.json) is still present; the orchestrator ruling removes it at P0f.
- Inside-root refusal tested against a dummy root (`root=` argument, scratch only, MEASURED). Refused: a lowercase spelling, `..` segments, forward slashes, an 8.3 short name. Not refused: an extended-length path `\\?\D:\...` and an admin-share UNC path `\\localhost\D$\...`. Both exited 0 and wrote the key inside the root (FIX 5). Both files were deleted unread.

## R4 Rule (l)

- Family x view: gridline (K4-Z4, Z3 and Z8 re-scoped to B; K4-B30), reference line (B32, B34, B29), part edge (B33, B35, B36). The 3 x 3 table is complete.
- Pre-change replay: K4-B32 to B37 clean; K4-Z9 to Z11 clean (MEASURED; equal to the Engineer's table).
- The inset branch (the parent's `script_paths`), deleted in mut_D: K4-Z8 reads clean, and K4-B26 to B31, B36 and B37 each lose the one inset firing. Red, MEASURED.
- Two branches have no control: the clip-region firing path (FIX 6) and the own-row exclusion (FIX 7).
- Gridlines are taken from tick locations. Their premise (grid drawn at every major and minor tick) holds through `setup_figure` (`ax.grid(True, which="major")`, `which="minor"`, `minorticks_on`).

## R5 Items

- R2-6 literal-band lint, deleted in mut_A (`lit = []`): K8-B90 reads clean, mismatch. Red, MEASURED.
- R2-7: K5-B48 fires on the pre-change code because the branch already existed. The Engineer showed it red by deleting the a1 branch. Accepted.
- DR4-2: K8-B91 changes mutation_scale and K8-B92 changes rad. The arrowstyle tuple test and the connection-class test have no B (FIX 8).
- Rule (j), every number: K4-B37 holds the value branch. Three other branches of `stall_literal_issues` have no B (FIX 9).

## Task 6 Full --controls

- Scratch copy of the live tree, default jobs (12): Z 104/104 clean, B 337/337 fired, smoke 3/3; wall 137.4 s, contended (MEASURED).
- Per-control equality with the Engineer's final run (wip/fixtures/controls_results.json, 13:18:13): 444 rows in the same order. id, expected, observed and match are equal on 444/444. Reason is equal on 440/444. The four that differ (H1-B5, M1C-B1, M1C-B2, M1C-B3) differ only in a temporary-directory or project-root path (NOTE 1).

## FIX list

**FIX 1 (R1, `--fast` call site).** `controls()` l.542 passes `fast` to `controls_dst`. With the argument deleted (`controls_dst(man_path, only)`, mut_F), every RUN, FAST and H1 control matches (22/22, MEASURED), and a `--fast` run would then write the record file. RUN-Z3 tests only the pure function. This is the same class as RUN-B4 (the `--only` call site). Control RUN-B5: `controls()` with `--fast` on a temporary live manifest writes the partial file and leaves the full-results path unwritten. It must be red with the call-site argument deleted.

**FIX 2 (R1, fast tier per the ruling).**
- Regenerate fixtures/fast.yaml: per check family, the least-time Z and the least-time B, plus S1-FULL, S2-FULL and S3-FULL (77 ids today).
- Change FAST-Z to family scope: every family with a Z has one Z in the tier, every family with a B has one B, every smoke control is present.
- Re-plant FAST-B2 as "every K8 B removed", fires "K8 has no B in the fast tier".
- Add FAST-B3: S2-FULL removed, fires "smoke S2-FULL not in the fast tier".
- MEASURED wall goes in the P0f file against 60 s.
- The P0f file supersedes the Engineer's gameplan item 1 text: "one B per branch, a branch being the manifest finding that added the B" becomes "the least-time Z and B of every check family and every smoke control".

**FIX 3 (R2, two `stale_deps` branches without a B).** Deleting both branches together (mut_A: `continue` ahead of each `diffs.append`) leaves all 8 DEPS controls matching (MEASURED). The branches are:
- l.850 to 851, a certifier whose sketch has no accepted, unsuperseded record. Control DEPS-B7: the temporary tree with S1 r8 set unaccepted, fires "deps certifier s1 s1_checks_r8.json: no accepted, unsuperseded record of s1".
- l.844 to 845, a spec or script path absent. Control DEPS-B8: s3_spec.yaml renamed in the temporary docs/, fires "deps spec 's3_spec.yaml' absent".

**FIX 4 (R2, the orchestrator ruling adds s3_checks_r7.json to `DEPS_EXEMPT`).** DEPS-B5 plants exactly "s3_checks_r7.json without deps" and expects it to fire. Under the ruling it reads clean. At P0f:
- (a) Add DEPS-Z3: the S3 r7 record without deps reads exempt, clean.
- (b) Re-plant DEPS-B5 on a name that is never exempt (s4_checks_r1.json accepted without deps).
- (c) Add DEPS-B9: S3 r8 accepted over r7 without deps fires "s3_checks_r8.json: deps not recorded" (the exemption ends with r7).
- (d) Update the `DEPS_EXEMPT` comment and the Engineer's gameplan item 1 text, which name s1 r8 and s2 r9 only.

**FIX 5 (R3, refusal bypass).** `m1_controls` tests containment by comparing resolved path strings. `Path.resolve()` leaves `\\?\D:\...` and `\\localhost\D$\...` unresolved to `D:\...`, so a key inside the project root is written (MEASURED, dummy root, rc 0 for both). Fix: test containment by file identity, using `os.path.samefile` on each existing ancestor of the key path against the root and against the out folder. Control M1C-B5: a key path in `\\?\` form inside a temporary root passed as `root=`, refused. Do not use the project root for this control: the current code writes the key there. It must be red on the current code.

**FIX 6 (R4, clip-region firing path without a B).** I replaced the body of `_run_near_vis` with `return 0.0` whenever a clip region is present (mut_B). All 48 K4 controls still match (MEASURED). The reasons:
- Every part-edge B (K4-B33, B35, B36) plants a quad with no clip path.
- The live drawings have 0 part-edge firings.
- K4-Z11 is the only control on the region path, and it expects 0.

So a defect that never counts a clipped piece passes. That covers every renderer split piece and hidden copy, which the rule text names. Control K4-B38: K4-Z11's quad with the complementary clip (the leader-side half kept) fires 1, "part edge of motor23_c". It must be red with the region path returning 0.

**FIX 7 (R4, the own-row exclusion has no control).** The rule text excludes the labelled row's own edges (r6 reviewer N1, "except the label's own row"). That is a relief. With `row != fid` and the per-row filter in `collinear_lines` both deleted (mut_C), all 48 K4 controls match (MEASURED). Under rule (h) the relief needs its Z. Control K4-Z12: a quad tagged with the labelled row, one edge along its own leader, reads clean; red when the exclusion is deleted. The B side already exists: the same plant tagged with another row (K4-B33, B35, B36).

**FIX 8 (R5, DR4-2 sub-conditions without a B).** With `got != TERM_STYLE or` deleted (only the mutation_scale test kept) and the Arc3 class test deleted (only the rad test kept) (mut_A), all 98 K8 controls match (MEASURED). Controls:
- K8-B93: span_lt terminator `'-|>,head_width=0.5'` at mutation_scale 14 fires "not the signed terminator".
- K8-B94: span_lt terminator with connectionstyle `angle3` (both ends on the line) fires "connection style Angle3 ... is not straight".

**FIX 9 (R5, rule (j): three branches without a B).** I deleted all three error returns in `stall_literal_issues` (mut_D, together with the inset deletion). Every K4 mismatch in that run traces to the inset deletion, and K4-B37 keeps its value-branch firing (MEASURED). The uncovered branches and their controls:
- No `(mu ...)` list. Control K4-B39: the stall_up literal with its mu list removed.
- Value and mu counts differ. Control K4-B40: an extra value.
- A mu that is not a thread_mu value. Control K4-B41: mu 0.25.

Each fires its own reason. The live inset firing reads too, until P6.

## NOTES

1. M1C-B1, B2 and B3 put absolute paths in their reasons (the temporary directory, the project root). Per-control equality between runs now has four path-only exceptions: H1-B5 and these three. Either drop the path from the fixture reason or add the three to the stated exclusion.
2. `m1_controls` writes the PNGs in `CONTROL_ROLES` order, so the file times map tokens to roles for anyone who reads builders.py, where `CONTROL_ROLES` also holds the expected verdicts. Shuffle the write order with `secrets.SystemRandom().shuffle`. M1 prompts never point at `docs/sketches/fixtures/`.
3. deps hash the spec and the script only (Engineer open item 6). Modules the script imports (sketch_common, the renderer) and checks_sN.py are outside deps, so a harness edit that changes a drawing passes `--stale`. The full sN re-run at every record point covers this today.
4. The `draw_cache` key fingerprints callables, not module constants. A fixture that patches a constant would receive a cached, unpatched drawing. That failure is loud (mismatch) but depends on run order. Today the only fixture patch is a callable (builders.py l.2806, `_style_visible`).
5. S3-3-B8's reason ("pair absent") does not name the pose, so the reason cannot tell the pose filter from absence. Naming the pose in the S3-3 reason ("present at load only") would separate B8 from B2 by reason as well as by branch.
6. M1C-B4 exercises the Z2 detector through an injected token source, not production code. M1C-Z2 is the production guard. Accepted as a premise B.

## Gameplan lines to change

none
