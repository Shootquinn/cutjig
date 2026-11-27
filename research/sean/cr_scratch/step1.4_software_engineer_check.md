# Step 1.4 (c) check (P5), The Software Engineer

## Corrections to the brief

1. Tree reviewed: the live docs/sketches as P4 left it. Every run below used scratch copies under `D:\Unleashed Robotics\_scratch\cutjig\open14\p5\` (`live\` for full runs and plants, `ws\` for branch deletions; script `bin\deltest.py`, output `deltest_stdout.txt`, `deltest_all.json`; plants `plants.txt`, `dry.txt`; runs `controls_full.txt`, `controls_fast.txt`).
2. My full `--controls` wall, 259.9 s (MEASURED), ran while two other reviewers loaded the same 16 CPUs. The Engineer's 154.2 s is the uncontended figure. The 43 new controls cost 76.2 control-seconds of 1762.8 in total (MEASURED from the P4 wip/fixtures/controls_results.json), about 6 s wall at 12 jobs (DERIVED).
3. The P4 control table claims "every B is red on the pre-change code, by branch deletion, or both". That holds for every B in it. It does not cover the check branches that no B plants. Six such branches exist (FIX 1 to 4 below).

## Verdicts

| Task | Verdict | FIX |
|---|---|---|
| 1 Branch coverage of S4-1 to S4-3 and the new rules | FIX | 1, 2, 3, 4 |
| 1a S4-3 reads K8 sense lines only (Correction 5; my signature) | PASS | none |
| 1b DEPS-Z2 re-scope (P2 Correction 10; my review) | PASS | none (NOTE 1) |
| 2 s4 --rev 0: causes, absent reds, guards | PASS | none |
| 3 Fast tier families; full wall against 200 s | PASS | none |
| 4 Ceremony | FIX | 5 |

5 FIX, 5 NOTE.

## 1 Branch deletion, MEASURED

Twelve deletions, each on a fresh copy, each followed by `--controls --only` over the 43 P4 controls plus S4-FULL (45 rows, 4 jobs).

| Del | Branch deleted | Red controls | Reading |
|---|---|---|---|
| E1 | S4-3 exclusion of ` section_true:`, ` section_u:`, ` projected_` lines | S4-3-B1, B2, B3, B4, B6, B7 (planted counts 13, 5, 20, 26, 6, 5) | covered |
| E2 | S4-3 row filter `"/{r} " in t` forced true | S4-3-B4, B6 | covered |
| E3 | S4-1 drawn collar top against the formula | none | no B (FIX 1) |
| E4 | S4-1 spec `formula` string against `check_stack.collar_top_z_A` | none | no B (FIX 1) |
| E5 | S4-2 (c) grip member not drawn (liner figure) | none | no B (FIX 2) |
| E6 | S4-2 (b) `datum_piece` dropped (whole wingnut read) | none | equivalent while plate is the top piece (NOTE 2) |
| E7 | sweep (s1) type and count (sketch_common l.5993) | none of K5-Z8, K5-B49 to B63, S4-FULL | no B (FIX 3) |
| E8 | S4-3 Absent branch (all untestable) | none | covered by the stub record (task 2) |
| E9 | `between` below_piece ignored | S4-3-Z, B1 to B7, K8-Z20, B102 to B106 (14) | covered |
| E10 | `between` above_piece ignored | the same 14 | covered |
| E11 | S4-2 (a) carrier on seat pair dropped | S4-2-B3 | covered |
| E12 | S4-2 (a) core on carrier pair dropped | none | no B (FIX 4) |

The Engineer's 35 deletions (D1 to D35) stand. Together with E1, E2, E9, E10, E11 the S4-3 piece selection, the new predicate forms, slits, wing, section_true, adjacency and X1 each have a red control.

### 1a S4-3 sense-line reader

- D35 (Engineer) empties the list S4-3 reads, and S4-3-B1 goes red. A reader that reads nothing now fails a control. The P2 defect class (reading a field K8 never returned) is closed.
- E1 and E2 show that the exclusion and the row filter both move planted counts, so a change to either goes red.
- A spec error in a kept-part predicate reaches S4-3. With washer `between` stripped of `above`, S4-3 fails content: "carrier/washer between: spec error, needs below and above" (MEASURED, `plants.txt` P2).
- The row list `s4_checks.S4-3.rows` is a hand list. Today it holds every row with `sense` except drill_head, which is not a kept part (MEASURED). See NOTE 3.

Signed.

### 1b DEPS-Z2 re-scope

- Code: `specs_read = sorted(HERE.glob("s*_spec.yaml")) if spec.get("chains")`, own spec excluded in `record_deps`. Fixture: every `s*_spec.yaml` but s3, read from the tree with its SHA-256.
- Both are written to the same rule (sym_lint reads `specs_in(HERE)`, every spec). The fixture still fails on a dropped spec, an empty list, a wrong hash or the own spec included. DEPS-Z2 matched in my full run (MEASURED).

PASS. The rule's cost is NOTE 1.

## 2 s4 --rev 0 (wip/s4_checks_r0.json)

- Guards: K1, K2, K3, K5, X1 pass.
- Reds:
  - by content: K4 (38) and K9 (31);
  - by absence: K6, K7 (53), K8 (50), S4-1, S4-2, S4-3 (27) and RPT (5).
- This equals STUB_EXPECT and STUB_CAUSE and the S3 r0 pattern (K4 and K9 content; K6, K7, K8, S3-x and RPT absent).
- Content Bs behind each absent red:
  - S4-1: S4-1-B1;
  - S4-2: S4-2-B1 to B3;
  - S4-3: S4-3-B1 to B7;
  - K8: K8-B102 to B107 on the S4 figures;
  - K6, K7, RPT: the family Bs on S1 to S3 (S4 adds only K6-Z6 and K7-Z19).
- The baseline run 2 matched 14 of 14 (Engineer).
- The E8 branch (S4-3 cause absent) is held by that record.
- Fixture S4-2-B5 below also reads S4-3 absent with one part missing (MEASURED, `dry.txt`).

PASS. NOTE 4 covers K4 on S4.

## 3 Fast tier and full wall

| Run | Controls | Result | Wall |
|---|---|---|---|
| Full (mine, live copy, 12 jobs) | 531 | Z 119/119, B 408/408, smoke 4/4 | 259.9 s contended; 265 s with start-up (MEASURED) |
| Full (Engineer) | 531 | all match | 154.2 s; 157.0 s with start-up |
| Fast (mine, 12 jobs) | 84 | Z 40/40, B 40/40, smoke 4/4 | 32.1 s; 36 s with start-up (MEASURED) |

- FAST-Z is clean in both runs, and FAST-B1 to B3 fire. The tier has every family's least-time Z and B plus S4-FULL. The three S4 families entered fast.yaml as S4-1-Z/B1, S4-2-Z/B2 and S4-3-Z/B2.
- The fast tier holds its 60 s target.
- The full set is 46 s under 200 s uncontended. Under three-reviewer load it is 60 s over. Runs of record are single-agent runs, so the uncontended figure governs.
- Floor: 1762.8 control-seconds / 12 = 147 s (DERIVED). Pruning would reach the floor only by deleting controls that hold branches. No pair among the 43 meets the P0S deletion test (another control firing on the same branch with the same reason for the same defect class).

PASS.

## 4 Ceremony

- **The 43 controls: KEEP all.** They cost 4.3 percent of control-seconds. The S4-3 Bs each take 3.9 to 4.3 s, because each builds two figures. That is the price of a drawn check and needs no change.
- **S4-1 drawn branch, and S4-2 (a) core on carrier.** Each repeats a predicate that another check also asserts:
  - collar 1.00 high fires K6, K8 section_true and S4-1;
  - core 2.00 high fires S4-2 and S4-3 (MEASURED, `plants.txt` P3, `dry.txt`).
  The duplication is in rows Sean ruled (Design Notes 34) and in the gameplan S4-1 text. A B costs about 2 s, and deleting either branch reopens a ruling, so FIX 1 and FIX 4 add Bs.
- **RPT literals: FIX 5.** checks_s4 `reported`:
  - prints `kept_axial` as a string literal ("1287.05 / 1104.16 N"), with basis "checks_s3.loads (P4 reads it from the S3 spec)";
  - takes `T_kept = 1287.05` as a literal in `seat_bearing`.
  The stated basis is false. The S4 record carries no dependency on s3_spec.yaml (spec_read [] in s4_checks_r0.json), so a change to W or to F_stall leaves the S4 record unstale. Today, `checks_s3.loads(P, load_spec("s3_spec.yaml"))` gives 1287.05 and 1104.16 (dry run, MEASURED), equal to the literals. The Engineer's own 1.3 position applies: "a printed value is read from the computing function, never a spec literal".

## FIX list

**FIX 1 (S4-1, two branches without a B; E3, E4).** Dry run on the live code (`dry.txt`):
- S4-1-B2: collar drawn 1.00 high in figure 1 fires 1, "carrier: drawn collar top 160.840 z_A vs formula 159.840".
- S4-1-B3: spec `s4_checks.S4-1.formula` with " + holder.flange_thickness" removed fires 1, "spec formula 151.840 differs from check_stack.collar_top_z_A 159.840".
- Each must read red with its branch deleted (E3, E4 replay).

**FIX 2 (S4-2 (c), grip member not drawn; E5).**
- S4-2-B5: liner area artists removed in figure 2 fires 1, "liner (c): grip member liner not drawn" (dry run). It must read red with the branch deleted.

**FIX 3 (sweep (s1); E7).**
- With one sweep line deleted, the zip in (s3) compares one line and the (s1) count is the only branch that fires.
- K5-B64: the +u sweep line removed in figure 1 fires 1, "sweep on wingnut: needs two two-vertex Line2D (1 artists) (s1)" (dry run). It must read red with l.5993 replaced by `if False:`.
- The Engineer's section 3 states this gap ("There is no B for (s1)"). Under rule (h) every branch gets its B.

**FIX 4 (S4-2 (a), core on carrier; E12).**
- S4-2-B4: core_100 drawn 2.00 high in figure 1 fires 1 in S4-2, "carrier (a): core_100 bottom minus carrier top 2.000" (dry run). It must read red with the pair dropped (E12 replay).

**FIX 5 (RPT values from the computing function).**
- `kept_axial` and `seat_bearing` read `checks_s3.loads(P, load_spec(SK / "s3_spec.yaml"))`: F_stall total + W per mu, and the governing value for the stress.
- The S4 run records s3_spec.yaml in `deps.spec_read`. `record_deps` takes specs_read, so the S4 run passes the S3 spec, and `--stale` then flags a W or thread edit against S4.
- No new control is needed for the value. The deps entry needs one Z line: extend DEPS-Z2's form to an s4 run, or put an equivalent assertion in S4-FULL. The printed text stays equal today (dry run).

## NOTES

1. **DEPS-Z2 rule cost.**
   - s4_spec.yaml carries no row of SYM_FAMILIES (0 rows, MEASURED). Once S3 r8 is accepted with s4_spec.yaml in its spec_read, every later S4 spec edit will flag S3 r8 under `--stale` and force an S3 re-run. That cost is DERIVED, and no SYM result depends on the edit.
   - Cheaper form: run `sym_lint()` live inside `--stale` beside `x1_lint()` (a spec lint, under 1 s) and drop spec_read for chains.
   - The rule is the Loftsman's (P0L FIX 2). His call.
2. E6: S4-2 reads the wingnut plate piece. While the plate is the wingnut's top piece, the plate top equals the whole-row top, so a B cannot distinguish the two. K8 section_true holds the pieces to the spec. No control is required.
3. The S4-3 row list is a hand list (the TP1.2-3 class). A kept-part row added later with `sense` and left off the list still fails K8, but not S4-3. One possible form: rows with `section_true` or `kept: true` in place of the list. Not required now.
4. K4 on S4 has no Z or B at (c), because the fixture places no labels (Engineer Correction 8). The sub-artist label templates and their reader land at P6. Each needs its own Z and B in that revision, red-first.
5. The S4 fixtures draw the P6 spec state in memory (`p6_state`, asserting each Old). When P6 applies the edits on disk, the asserts fail loudly in every S4 control unless P6 also removes `x1_edits_at_p6` from s4_spec.yaml. Do both in the same edit.

## Gameplan lines to change

none
