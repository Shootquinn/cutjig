# Step 1.3 step 0 re-check (P0T-r), The Topologist

Date 2026-11-26. Read: `step1.3_topologist_step0_check.md`, `step1.3_engineer_step0_fixes.md`, `docs/sketches/sketch_common.py` (`zero_area_issue`, `least_thickness`, `k5`, `artists`, `artist_polys`), `check_sketch.py` (`run_control`, `compare`), `fixtures/manifest.yaml` and `fixtures/builders.py` (K5-B19 to B23), gameplan l.139, l.296 to l.298, l.666, manager_open P4, P6, P7b. Scratch tree: `docs/sketches/` copied (wip/ and `__pycache__` excluded) to scratchpad `p0tr/base/sketches`; SHA-256 of `sketch_common.py` 79f7f8de9577994e, `check_sketch.py` 72d126d68bde081f, `builders.py` 47eb9356aec759be, `manifest.yaml` 591de03b2e9a23eb, equal to the P0f "After" column (MEASURED). Deletion trees: `p0tr/mut/<name>/sketches`, built by `p0tr/mut.py`, one clause each. Runner `p0tr/run.py` (controls through `run_control` and `compare`, probes through `builders._script_ctx`, the drawing scripts of record); `p0tr/run_ann.py` for the Annulus branch. Nothing under `docs/sketches/` edited.

## Corrections to the brief

1. FIX 1 is closed for Rectangle, Polygon, Circle, Ellipse and for Line2D and Collection under an area row's id. The Annulus clause the brief lists is implemented and has no B control: deleting it leaves all 26 K5 controls matched (section 3). FIX 1 is not fully closed; one control is missing (FIX 1r below).
2. The mark admission rule (option A) is carried in the P0f file (section 9 item 1) and in the P0f l.666 New text. Neither the P4 brief nor the P6 brief names it, and P6's brief ("fix the drawing, never the check"; script edits only where an expression must change; spec edits only as The Loftsman ruled at (b)) bars landing it at P6 as written. It needs a gameplan line naming the owner and slot (section 4).

## 1. FIX 1 items against the code

| FIX 1 item | Code (sketch_common.py) | Control | State |
|---|---|---|---|
| (a) thickness 2A/P <= TOL_Z on every Patch, transform chain | `zero_area_issue` l.1624: any `Patch` goes to `least_thickness` l.1642 (pieces from `artist_polys`, data coordinates); fails at t <= 0.05 (TOL_Z, DECLARED) | K5-B20 (sliver Rectangle), K5-B21 (Circle r 0), K5-B23 (collinear Polygon) | closed |
| (a) Annulus: radial width of the transformed rings | `least_thickness` l.1648: two largest rings, mean radius about the outer ring's centroid, t = r_out - r_in | none | **no B (FIX 1r)** |
| (b) K5-B19 substrings kept | reason "zero-area Rectangle (least thickness 0.0000 mm <= 0.05) on a cylinder row (TP1.1-9)" | K5-B19 match (MEASURED) | closed |
| (c) Line2D or Collection under the row's own id fails, independent of `projection` | l.1630 `if not isinstance(a, Patch)`, reached only when `gid` is a row id (sub-gids branch off before it in `k5`) | K5-B22 (Line2D, projection deleted) | closed |

`artists(ax)` = patches + lines + collections, so (c) sees every Line2D and Collection (MEASURED, l.423). Texts stay outside K5 and are held by K9 as at P0T.

## 2. Bypass probes on the fixed code, and the controls

Base tree, MEASURED (`p0tr/run.py`):

| Run | K5 | n | Reason (head) |
|---|---|---|---|
| S1 probe: anchor lines height 0.001 (area 0.042 mm², DERIVED 42 x 0.001) | fail | 8 | "load/anchor_a: zero-area Rectangle (least thickness 0.0010 mm <= 0.05) on a prism row (TP1.1-9)" |
| S2 probe: screw_a Circle radius 0 at load | fail | 1 | "load/screw_a: zero-area Circle (least thickness 0.0000 mm <= 0.05) on a screw row (TP1.1-9)" |
| extra: drill_tube Annulus width 0.001 (S2 script) | fail | 1 | "load/drill_tube: zero-area Annulus (least thickness 0.0010 mm <= 0.05) on a cylinder row (TP1.1-9)" |
| extra: PatchCollection under screw_a | fail | 1 | "load/screw_a: PatchCollection on a screw row draws no area (TP1.1-9)" |
| extra: Ellipse 20 x 0 under screw_a | fail | 1 | "load/screw_a: zero-area Ellipse (least thickness 0.0000 mm <= 0.05) on a screw row (TP1.1-9)" |
| live S1 r7 | fail | 8 | the 8 anchor bearing lines, t 0.0000; nothing else |
| live S2 r5 | pass | 0 | 105 artists |
| K5-B19, B20, B21, B22, B23 | match | 1, 8, 1, 1, 1 | planted counts met |
| K5-Z2, K5-Z3 | match (clean) | 0 | 295 and 99 artists |

Both bypass routes of P0T section 1 now fire.

## 3. Deletion test, one clause per scratch tree

MEASURED; "B" = the control that guards the clause; every other K5-B19 to B23 and Z2, Z3 stayed matched in each tree.

| Tree | Clause deleted | Guarding B | Probe |
|---|---|---|---|
| `a_area` | thickness replaced by the P0 test (Rectangle w or h 0; area <= TOL_AREA 0.01) | K5-B20 clean, 0 issues, "343 tagged artist(s)": mismatch | S1 sliver passes, 0 issues |
| `a_scope` | thickness test limited to Rectangle and Polygon | K5-B21 clean, 0 issues, "99 tagged artist(s)": mismatch | S2 Circle r 0 passes; Ellipse 20 x 0 passes |
| `c_none` | non-Patch clause set to `return None` (pre-P0f behaviour) | K5-B22 clean, 0 issues, "296 tagged artist(s)": mismatch | PatchCollection still fires through the projection compare (screw has an expected circle) |
| `c_drop` | non-Patch clause removed (falls to the thickness test) | K5-B22 fires with "zero-area Line2D (least thickness 0.0000 ...)": reason mismatch | |
| `ann` | Annulus branch removed (`if False:`) | **none**: all 26 K5 controls matched | Annulus width 0.001 passes, 0 issues, "105 tagged artist(s)" |

`least_thickness` and `zero_area_issue` have one caller, `k5` (grep, MEASURED), so no non-K5 control reads the Annulus branch (DERIVED). Without the branch an Annulus reads 2A/P per ring, each ring a full disk of radius about 76 mm (DERIVED from the 152.4 OD drill tube), so a zero-width annulus passes.

**FIX 1r.** Add K5-B24: S2 script drawing (`_script_ctx("s2")`), drill_tube Annulus at load set to width 0.001; reason ["load/drill_tube: zero-area Annulus (least thickness 0.0010", "on a cylinder row (TP1.1-9)"]; planted 1; finding "Topologist P0T FIX 1 (a) Annulus". Dry run, MEASURED: fixed code fires 1 with that reason; P0 code (scratchpad `p0f/pre`) passes, 0 issues, "105 tagged artist(s)" (red on the pre-change code); `ann` tree passes (red under deletion). No record moves: live S2 r5 unchanged (drill_tube wall 3.175 mm, DERIVED (152.4 - 146.05) / 2, 63x TOL_Z), S1 r7 unchanged.

## 4. K5 mark admission (option A) carried to S1 r8

| Where | Carried |
|---|---|
| P0f section 9 item 1 | yes: rule, M1 to M5, B-m1 to B-m5b, fixture and live S1 r8 Z |
| P0f l.666 New | yes: "redrawn in S1 r8 as anchor_<s>:line under the K5 mark admission rule" |
| P0f l.139 New | excluded on purpose ("lands with S1 r8") |
| gameplan now | l.139 and l.666 still hold the pre-step-0 text (P0T and P0f lines not yet applied, MEASURED) |
| manager_open P4 (harness gains at (c)) | not named |
| manager_open P6 (S1 r8 draw) | not named; brief bars check edits and limits script and spec edits |
| manager_open P7b (S1 changed rows) | covers re-check of the implementation if S1 r8 is triggered |

Status: carried in record, unscheduled in the briefs. Line below places it: the Engineer lands the K5 clause, the `mark` field and B-m1 to B-m5b at P4 (c) with the other red-first rules; P6 redraws `s1_side_poses.py` l.230 as the Line2D `anchor_<s>:line` (butt cap, zorder 1; 1 px off r7 at capture_end and park, MEASURED at P0T) and adds `mark` to the two anchor rows, as named exceptions to the P6 edit limits. The orchestrator states both in the P4 and P6 brief slots. Fall-back if the rule fails its Z or B: option B (line deleted).

## 5. Notes

**NOTE 1.** `zero_area_issue` docstring (l.1625) still describes the P0 absolute-area form. Text only; fix with K5-B24.

**NOTE 2.** 2A/P is a mean width. For a compact patch it reads half the size (Circle: r; square: w/2), so a round part of diameter below 0.1 mm fails and above passes (DERIVED). No live part is near: least live thickness 1.3636 mm, S1 core_seat (MEASURED at P0T).

## 6. Verdict

**FIX** (1 item: FIX 1r, K5-B24 for the Annulus branch). FIX 1 (a) for Rectangle, Polygon, Circle, Ellipse, (b) and (c): closed, deletion-tested. TP1.1-9 signs when K5-B24 lands matched, shown red on the P0 code and under deletion of the Annulus branch; I accept the Engineer's dry-run table for that sign-off without a further spawn if it reproduces section 3's `ann` row and the P0-code result. Mark admission option A: signed rule stands, carried in record; scheduling line below.

## Gameplan lines to change

These supersede the P0T (`step1.3_topologist_step0_check.md`) l.139 entries. The P0f l.139 first fragment (thickness rule text) and the P0f l.666 entry stand as written in `step1.3_engineer_step0_fixes.md`.

**l.139** (K table, K5 row, controls column).
Old: `K5-B19 zero-height Rectangle on the drill tube (TP1.1-9) |`
New: `K5-B19 zero-height Rectangle on the drill tube (TP1.1-9); K5-B20 S1 anchor line 0.001 high; K5-B21 S2 screw circle radius 0; K5-B22 prism row without projection drawn as a Line2D; K5-B23 collinear Polygon on the drill tube (Software Engineer P0S FIX 4); K5-B24 S2 drill tube Annulus width 0.001 (Topologist P0T re-check FIX 1r) |`

**Insertion after l.298**, the line beginning `Done at step 0 (P0, `research/sean/cr_scratch/step1.3_engineer_step0.md`; reviews P0L, P0T, P0S pending):` and ending `S1 r7 is not re-acceptable until that is resolved; S2 r5 17/17.`
New: `Carried to S1 r8 (Topologist P0T ruling, option A, signed in advance; research/sean/cr_scratch/step1.3_topologist_step0_check.md section 4): K5 mark admission for <row>:line (spec field mark: {sub: line, z, source}; checks M1 to M5; B-m1, B-m2, B-m3a, B-m3b, B-m4, B-m5a, B-m5b, each red on the pre-change code; fixture Z on the S1 fixture, live Z on S1 r8). The Engineer lands the K5 clause and its controls at P4 (c); P6 redraws the anchor bearing line (s1_side_poses.py l.230) as the Line2D anchor_<s>:line and adds mark to the two anchor rows, named exceptions to the P6 script and spec edit limits; The Topologist re-checks at P7b. If the rule fails its Z or B, option B (line deleted) applies.`
