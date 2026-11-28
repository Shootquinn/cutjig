# Step 1.4 re-check r2, The Topologist: TP1.4-3 to -5 on S4 r2, S1 r10, S3 r9; R1, placer and cut-outline signatures

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\open14\p7tr\`.
- `controls_only.txt`: `--controls --only` over K7-B36 to B38, K8-B110 to B123, K8-Z2*, K8-Z5, K8-Z23, K4-B61 to B64, K4-Z3, Z4, Z8, Z14. Z 10/10, B 23/23, 82.3 s. PARTIAL: written to `wip/fixtures/controls_results_partial.json`. The full record `controls_results.json` (586/586, Engineer) was not touched.
- `conv.py` / `conv.txt`: stroke-copy converse and unsectioned-pair front sign on live S3 and S4, drawn by their scripts.
- `plant6c.py` / `plant6c.txt`: line-family converse plant.
- `dpi\`, `dpi_lint.txt`: R1 premise dry run.
- Crops: `crop_line.png`, `crop_corner.png`, `crop_corner_r.png`, `crop_top.png` (S4 r2 carrier figure).

## Corrections to the brief

1. The brief calls this a re-check of "the fix pass". The fix pass carries four new check or renderer rules beyond my three FIXes (R1, the placer rules, cut_outline_issues, the K5 wing form). Section 3 signs the three the orchestrator names. The K5 wing form is the Loftsman's and the Designer's.
2. K8-B77 and B78 planted counts are 6 at r2 (`recount.txt` of the fix pass). The P7b prediction was 5. The extra firing is the TP1.4-5 line-family issue on the same plant (fix-pass section 2). It is not a discrepancy.

## 1 Findings raised at P7b

| Finding | Status | Control or measurement |
|---|---|---|
| FIX TP1.4-3 (core_seat depth under the ledge r 50.50) | **CLOSED** | Live s1 l.323, s3 l.509, s4 l.359 carry `(core.diameter_nominal + collet.grip_window_hi) / 2`, i.e. +-50.50 (DERIVED). The lint is at sketch_common l.4033 to 4055: r_max is taken over section_true pieces with plane_cuts removed. K7-B36, B37, B38 fire 1/1 each (MEASURED, `controls_only.txt`). Live S1 r10 19/19, S3 r9 16/16, S4 r2 14/14 (MEASURED, wip records). |
| FIX TP1.4-4 (front-surface sign between unsectioned bodies) | **CLOSED** | See the rows after this table. |
| FIX TP1.4-5 (clause (6) line family) | **CLOSED as named**: both live firings are split. Converse not checked: FIX TP1.4r2-1. | See the rows after this table. |
| NOTE TP1.4-6 (far-side bore edges) | OPEN, carried (fix-pass section 5, to the Designer at M1) | Not acted on |
| NOTE TP1.4-7 (placer empty-side IndexError) | OPEN, carried | Still present: sketch_common l.1474 `choice[f] = cands[f][0]` runs when `cands[f]` is empty after the l.1343 `on` filter. angled_candidates (l.1279) cannot fill an empty list. |
| NOTE TP1.4-8 (r8-era `section` fields in plan_outline) | OPEN, carried | Not acted on. Plan views still draw no section_true row (S2 r11). |

**TP1.4-4 evidence.**
- `_in_front` is at l.5845. `_occluded_by` (l.5866) applies it whenever the target row is unsectioned.
- K8-B116 fires 6/6 and B117 fires 3/3 (MEASURED).
- Every live unsectioned pair has one sign over its whole u overlap, and the sign is right (MEASURED, `conv.txt`, 400 u samples per pair). All pairs are coaxial (c 0.00 / 0.00 in S4 and S3, -160.00 / -160.00 at coupling_c).

| Occluder over target | x_front(O) - x_front(T) |
|---|---|
| drill_head over carrier / core_100 | +38.40 to +69.68 |
| drill_tube_stub over core_100 | +25.70 to +53.61 |
| drill_head over core_750 | +38.90 to +70.06 |
| coupling_c over screw_end_c | +5.50 to +8.34 |
| coupling_c over liftmotor_shaft_c | +7.00 to +8.99 |
| Each reverse pair | negative, not split |

- No pair has a mixed sign. That case (non-coaxial bodies) is NOTE TP1.4r2-3.
- Pixels:
  - S4 r2 carrier figure: the head teeth line (z_S 257.54) and the bottom edge (244.84) are solid across |u| < 50.50. The carrier/core edges inside the head are dashed (`crop_line.png`).
  - S3 r9: the head teeth line is solid across core_750, and the core inside the head is dashed (PNG read).

**TP1.4-5 evidence.**
- `_stroke_rows` (l.5890) and `_hidden_stroke` (l.5906) are read by render_occlusion (l.5976) and occlusion_issues (l.6068).
- K8-B118 fires 6/6 and B119 fires 1/1 (MEASURED).
- Live dashed stroke copies, with samples inside the copy's drawn region and no front occluder over them (MEASURED, `conv.txt`):

| Stroke copy | Dashed samples | No front occluder |
|---|---|---|
| S4 carrier:line (each figure) | 203 | 0 |
| S4 core_100:line (each figure) | 203 | 0 |
| S4 liner:outline (two copies) | 478 each | 0 |
| S3 anchor_bearing_c:line | 21 | 0 |

## 2 Signatures on my rules

| Rule | Signature | Reason |
|---|---|---|
| TP1.4-3 K7 section_true depth lint | **SIGNED** | The premise (a revolved row's band equals its radial extent) is enforced by K8 section_true_issues (the drawn pieces are the spec pieces), which has its own Z and B. Z: live S1, S3, S4. B: K7-B36 to B38, red on the pre-change tree. Scope: every side and section Axes. Plan is carried (TP1.4-8). |
| TP1.4-4 front-surface sign, (6c) area converse | **SIGNED** | Premise held by K8-B73 and K5. Z: K8-Z23 and live S3. B: B116 and B117, red on the old occluder test. |
| TP1.4-5 line-family clause (6) | **NOT SIGNED** | (6a) and (6b) read strokes; FIX TP1.4r2-1 covers the gap. Rule scope requires the (6c) converse in every line family, but occlusion_issues l.6057 reads area copies only (`_area_artists`). The renderer gives an unsectioned parent's stroke a hidden region that is a rectangle: the occluder's bbox z range over the front-u interval (l.5984 to 5999), not the occluder ring. Nothing checks that region. |

## 3 Signatures requested by the orchestrator (Design Notes 35 R1)

| Rule | Signature | Reason |
|---|---|---|
| Rule (l) at 12 px: D = max(D_spec, 12 px / px-per-mm), with K4-B61 to B64 | **NOT SIGNED** | One premise has no B (FIX TP1.4r2-2). See the evidence below the table. |
| Placer: angled candidates (LEADER_ANGLES l.1266), frac/theta angled forms first, thin-face mid-height landing (l.1293 to 1305), S1 side collinear routine (`_side_collinear` l.745, SIDE_EXTRA_ANGLES, SIDE_ANCHOR_ALTS) | **SIGNED** | Placer only. Each one reorders or extends the candidate list, and every leader is judged by K4 (collinear_issues, (k) anchor record). The P7b ruling 2 precedent holds. |
| Cut-body outline: K8 cut_outline_issues o1 to o4 (l.5759), draw_cut_outlines (l.5736), K5 :outline admission; K8-Z23, B120 to B123 | **SIGNED** | See the evidence below the table. |

**Rule (l) evidence.**
- The clearance branch is correct per Axes: collinear_scale l.2665 reads transData at the figure dpi (inset included, TP-7).
- K4-Z3, Z4, Z8, Z14 are clean, and B61 to B64 fire 1/1 each (MEASURED). Each plant is red only under the 12 px D, because 8 px is more than the old D of 2.45 px (fix pass `pre_run.txt`).
- The rule states as its premise that every script saves at the figure dpi: "K3 dpi and the save lint". K3-B6 holds the figure dpi.
- The save lint is the K1 figure-keyword branch (l.2295). It flags `savefig(..., dpi=...)`, but no manifest B plants that.
- Dry run (`dpi_lint.txt`, MEASURED):

| Script | K1 result |
|---|---|
| s4_base_section.py copy with `savefig(path, bbox_inches="tight", dpi=300)` | fails: "figure keyword dpi= outside setup_figure" |
| Live script | passes |

- `rcParams["savefig.dpi"] = 300` is caught only through the literal 300. A key-valued assignment passes: NOTE TP1.4r2-4.

**Cut-body outline evidence.**
- (o1) refuses a stroked piece edge.
- (o3) is the P7b predicate: material of the body on exactly one side of every outline sample, offset OUTLINE_EPS along the segment normal.
- (o4) requires every union-boundary sample to lie within TOL_Z of the outline.
- The premise (drawn pieces = spec pieces) is K8 section_true_issues, which has Z and B.
- Z: K8-Z23 (S4), Z21 (S1), Z22 (S3) are clean. B: B120 (S4 o1), B121 (S1 o1), B122 (S3 o4), B123 (S4 o3) fire 1/1 (MEASURED).
- S4 r2 pixels: holder+collar, receiver+spigot and collet+core_seat each read as one outlined region with no interior seam (PNG read).
- Scope: S1, S3, S4.

## 4 New findings (introduced by the fix pass)

**FIX TP1.4r2-1: (6c) converse missing from the line family. Class repeat (renderer converse: TP1.2-15, TP1.4-4). The orchestrator rules.**

*Defect.*
- TP1.4-5 split every tagged stroke, but (6c) still reads area hidden copies only.
- A stroke drawn dashed where nothing is in front of it passes K8.
- For an unsectioned parent, the renderer builds the hidden region as a rectangle: occluder z range by the front-u interval (l.5984 to 5999). A non-rectangular occluder outline would over-dash, and no check sees it.

*Plant* (`plant6c.txt`, MEASURED): S4 liner figure, both liner:outline hidden copies unclipped (dashed over the whole outline).
- occlusion_issues reports 0 issues.
- The converse predicate counts 580 of 2108 dashed samples with no occluder in front.

*Rule.* (6c) extends to every dashed stroke copy with a `_sc_hidden_copy` flag. No sample of the copy inside its drawn region may lie outside every occluder ring of another row that is in front of the parent at that u. "In front" uses the `_hidden_stroke` sign test for an unsectioned parent and plain containment otherwise.
- Z: live S3 r9 and S4 r2. Dry run `conv.txt`: 0 wrong samples on all 7 live stroke copies.
- B: the plant above on live S4 (580 samples).
- Scope: section Axes (render_section). S1 side views are carried by name (no occlusion clause).

*Dry run.* The predicate is `conv.py` (A). No value is set. A live pass means no drawn change, so it opens no revision.

**FIX TP1.4r2-2: R1 premise without a B (process rule (h)).**

*Defect.* The R1 premise "every script saves at the figure dpi" is enforced by the K1 figure-keyword branch, and no manifest control plants `savefig(dpi=...)`.

*Fix.* Add K1-B: a copy of a live script with `savefig(path, bbox_inches="tight", dpi=300)`, reason "figure keyword dpi= outside setup_figure". It is red on the live K1 (`dpi_lint.txt`). The Z is the live scripts (K1 pass).

*Dry run.* `dpi_lint.txt`. No value set and no drawn change. When this lands, R1 is SIGNED with no other change.

**NOTEs.**
- **TP1.4r2-3.** `_in_front` takes "all u samples in front". A non-coaxial occluder that is in front over only part of the overlap hides nothing, so 6a/6b pass the target drawn solid there.
  - Live: every unsectioned pair is coaxial, with one sign per pair (`conv.txt`).
  - The premise "axis in the plane" does not imply a shared axis. Add a coaxial premise check, or a per-u split, when a sketch first draws two non-coaxial unsectioned bodies that overlap.
- **TP1.4r2-4.** An rcParams `savefig.dpi` assignment with a key-valued right side passes K1. The R1 premise should also lint `rcParams` / `rc(...)` writes to `savefig.*` in the scripts.
- **TP1.4r2-5.** K4-B61 to B64 plant at 8 px. They show the class (M1 S4 F2, 7 to 8 px) but do not pin the threshold: a D of 9 px passes all four. A boundary pair would hold COLLINEAR_PX_MIN itself: 11.5 px fires, 12.5 px stays clean, on one Axes. The threshold is The Designer's.
- **Carried unchanged.** TP1.4-6, -7, -8; N1 to N7 (P5T); TP-n at every M1. S4 r2 adds no new narrower row: drill_tube_stub is drawn at its footprint r 76.20.

## Verdict

- **CLOSED:** TP1.4-3, TP1.4-4, TP1.4-5 (as named).
- **OPEN:** NOTEs TP1.4-6, -7, -8 (carried); new FIX TP1.4r2-1 (class repeat, orchestrator ruling) and TP1.4r2-2; NOTEs TP1.4r2-3 to -5.
- **SIGNED:** TP1.4-3 lint; TP1.4-4 sign and area (6c); placer rules; cut-body outline checks (K8-Z23, B120 to B123).
- **NOT SIGNED:** TP1.4-5 line family (converse, TP1.4r2-1); R1 12 px rule with K4-B61 to B64 (premise B, TP1.4r2-2).

## Gameplan lines to change

1. Design Notes open-items table, new row after row C1.3-b (line 718). Supersedes step1.4_topologist_crossreview.md item 2.
Insert after:
```
| C1.3-b | Loftsman NOTE LF1.3-11 (S2 spec source text still names r7) and LF1.3-12 (anchor faces measured against a bearing drawn solid); Topologist NOTE R2-6 (not_drawn literal x bands for pinions and base frame, margins 5.09 and 22.00, out of --stale reach) and R2-7 (arc a1 plan-only branch reachable only by a spec plant, no B); Designer DR4-2 (terminator relief bounds arrow position, not head width or connection style); r6 reviewer NOTE on rule (j) (only the first figure of a stall literal is held; 282.21 unheld); N2 ticks named in five S3 shape strings and not drawn; N4 stale W comment ; 1.4 step 0 (`research/sean/cr_scratch/step1.4_engineer_step0.md` section 6): R2-6 bands as key expressions with a literal lint (K8-B90), R2-7 B (K5-B48), DR4-2 straight connection and the signed terminator style (K8-B91, B92; numeric half-width bound to The Designer, live 2.38 mm), rule (j) every number of a stall literal (K4-B37), LF1.3-11 text corrected, N4 already corrected at 1.3 r7; LF1.3-12 to Step 2; N2 ticks to S6 | 1.4 (S4) step 0 (harness items); S6 (ticks); Step 2 (LF1.3-12 bearing row) | The Engineer; raisers re-check |
```
New:
```
| TP1.4-3 to TP1.4r2-5 (S4 / S1 / S3 cross-review and r2 re-check; step1.4_topologist_crossreview.md, step1.4_topologist_recheck_r2.md) | Closed at r2: TP1.4-3 (core_seat depth to (core.diameter_nominal + collet.grip_window_hi) / 2 in s1, s3, s4; K7 section_true depth lint, K7-B36 to B38), TP1.4-4 (front-surface sign, area (6c), K8-B116, B117), TP1.4-5 as named (stroke split, K8-B118, B119). Signed: TP1.4-3 lint, TP1.4-4, placer rules (angled candidates, thin-face mid-height, S1 collinear routine), cut-body outline checks (K8-Z23, B120 to B123). Not signed: TP1.4-5 line family (FIX TP1.4r2-1: (6c) converse over dashed stroke copies, plant on S4 liner:outline 580 of 2108 samples unchecked; class repeat, orchestrator ruling) and R1 12 px rule (FIX TP1.4r2-2: K1-B for savefig dpi= as the premise B). NOTEs: TP1.4-6 far-side bore edges (Designer at M1), TP1.4-7 placer empty-side IndexError (l.1474), TP1.4-8 r8-era section fields in plan_outline, TP1.4r2-3 non-coaxial partial front, TP1.4r2-4 rcParams savefig.dpi lint, TP1.4r2-5 K4 12 px boundary pair | 1.4 (h) r3 or orchestrator ruling (TP1.4r2-1); next fix pass (TP1.4r2-2) | The Engineer; The Topologist re-checks |
```
