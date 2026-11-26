# Step 1.3 (h) r3: raiser signatures (The Topologist, The Designer)

## Corrections to the brief

1. **The live dimension line `span_lt` carries a `_` end marker 14 pt wide (29 px, 11.9 mm at 2.45 px/mm).** It runs 5.95 mm each side of the line, along each extension line (MEASURED, `s3_jackscrew_section.py` l.120, `marker="_"`, `markersize=sc.LABEL_FONTSIZE * 2`).
   - The red ink therefore runs 6.1 mm past the dimension line: px 601 to 724 against the line at 709.5 (MEASURED, `wip/s3_jackscrew_section_r3.png`, rows 386 and 2519).
   - Hiding the two `:ext` artists leaves px 695 to 724 red. Hiding `span_lt` as well leaves none (MEASURED, visibility toggle on a rebuild pixel-equal to r3).
   - e3 bounds the `:ext` artist at 2 mm past the line, and it is drawn there: data (-154, z) to (-108, z) (MEASURED). The 6 mm comes from the parent's marker. A K5 rule outside the four e-clauses governs the marker.
   - See Designer NOTE D-r3-1.
2. **The engineer's red-first table is the evidence of record for the pre-change state.** The scratch copies here hold r3 only. No pre-change code was re-run.

Tags: MEASURED (run or image read on 2026-11-26 in this session), DERIVED (hand arithmetic), DECLARED (spec, code as read, ruling).

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\sign_r3\`.
- `sk\`: a copy of `docs/sketches/` at r3, without `wip\`.
- `params.yaml`: a copy of the root params.
- `del_*\`: deletion copies, one edit each, made by `probes\deltest.py`. Logs are in `probes\del_*.log`.
- `dry_vbar\`: the Designer's cover-hatch dry run.

TMP and TEMP point at `_scratch\cutjig\tmp`. Nothing under `docs/sketches/` was edited.

**Baseline control subset on the r3 copy: 28 of 28 match** (MEASURED, `probes\base.log`).
- Subset: S3-3-Z, S3-3-B12 to B17, K8-Z14, Z16, B79 to B87, K5-Z6, Z7, B40 to B47.
- Z: 5 of 5 clean. B: 23 of 23 fire with the planted count and the stated reason.

---

## 1. The Topologist

**Verdict: all four rules SIGNED.** No FIX.

### 1.1 Evidence per rule

"Fires on r3" means the control matched on the r3 copy (MEASURED). "Red on pre-change" comes from the Engineer's §3 table (DECLARED).

The deletion test edits only the branch the new B exists for. Every other control in the 28-control subset stays matched (MEASURED).

| Rule (finding) | New B | Fires on r3 | Red on pre-change (Engineer §3) | Deletion test (one edit, scratch copy) | Result |
|---|---|---|---|---|---|
| S3-3 link kinds and face sense (R2-1) | S3-3-B16: face kind with no face z | yes, 1/1, "S3 face link names no face z" | pre-r2 `pre_r1`: clean (red) | `del_r21a`: `if kface and not face:` set to `if False:` (`checks_s3.py` l.373) | B16 clean, **mismatch**; 27 others match |
| same | S3-3-B17: face link with no S3 certifier | yes, 1/1, "face link with no S3 certifier" | pre-r2: clean (red) | `del_r21b`: the `elif k == "face" and "S3" not in heads` lint set to False (l.274) | B17 clean, **mismatch**; 27 others match |
| not_drawn bands, deferred branch (R2-2) | K8-B86: rear nut shoulder screw deferred with no owner | yes, 1/1 | pre-r2: clean (red) | `del_r22`: `if not e.get("owner"):` set to False (`sketch_common.py` l.4911) | B86 clean, **mismatch**; 27 others match |
| `plan_axes:arc` head (R2-3) | K5-B43: head 100 to 90 deg on the ccw line | yes, 1/1, "arc head points against theta (clockwise)" | r2 `pre_rf`: fires 2 against 1 planted (red, count) | `del_r23`: the head dot test `(head - tail) . (-sin t1, cos t1) <= 0` set to False (l.2572) | B43 clean, **mismatch**; Z7 (with head) stays clean |
| hatch alternate by line family (R2-4) | K8-B87: alternate `'////'` | yes, 1/1, "in the line family of material pattern(s) aluminium" | r2: clean (red) | `del_r24`: `hatch_family(h)` returns `{str(h)}`, the r2 string test (l.4790) | B87 clean, **mismatch**; B81 (equal string) still matches, as it should under string equality |

All five deletions turn the target B to a mismatch, so no deletion test passes. Each rule's B fires on r3. By the orchestrator's loop-cap ruling, no FIX round opens.

### 1.2 Sign-off per rule

- **S3-3 link kinds and face sense: SIGNED.**
  - The sense branch rests on B12 and B13. Their red-first and the D01 deletion were done at r2 (`step1.3_topologist_recheck_r2.md` §2.1), and both match on r3.
  - The kind lint rests on B15. The two escape branches now rest on B16 and B17.
  - B14 is described as a regression guard (Engineer §1), as asked.
  - R2-5 is applied: chain c's ring|bearing and bearing|drill_tube carry the `declared (S6-5 draws the axial seat)` certifier.
  - S3-3-Z stays clean on the fixture records. Live S3-3 is red on the stale S1 r7 / S2 r5 records only, and the Engineer's dry run with S1 r8 / S2 r9 is 16/16 with 48 links. That equals my r2 DERIVED count: 18 + 15 + 15.
- **not_drawn bands with the deferred-owner branch: SIGNED.**
  - Premise: an omitted part lies wholly in front of the plane or past one profile width, or is deferred to a named owner. The B for each branch:
    - band test: B83, B85;
    - omit: B84;
    - owner: B86.
  - B83 is re-planted on the rear entry (now `deferred`) and matches on r3.
  - NOTE R2-6 is carried unchanged. The pinion and base-frame x bands are still literal. Their margins are 5.09 and 22.00 (DERIVED at r2), and `--stale` cannot reach them.
- **`plan_axes:arc` admission: SIGNED.**
  - The sense now has controls on both of its artists: B40 (line cross product) and B43 (head dot product).
  - Z7 draws the head as the live script does (`_draw_arc`, FancyArrowPatch theta1 - 10 to theta1; fixture l.214 to 228, DECLARED).
  - The K5-B41 re-count of 2 (line and head both off the r + 5 circle) is the intended reading.
  - NOTE R2-7 (a1 plan-only branch reachable only by a spec plant) is carried.
- **Hatch alternate per piece and its line-family lint: SIGNED.**
  - Clause (1) per piece is held by B79 and B80 (D15 and D16 at r2). The lint is held by B81 (equal) and B87 (same family, other density).
  - `hatch_family` maps `+` to {|, -} and `x` / `X` to {/, \}, as specified in R2-4.
  - The live `'--'` passes, with K8-Z16 clean. Under this lint the admissible set from the Engineer's candidate list is `'--'`, `'||'` and `'++'`. The pick among them belongs to The Designer (section 2.3).

### 1.3 Topologist NOTE (no FIX)

- **T-r3-1.** K5-B47 under deletion of e4 still fires, but on a different reason (the parent-row clause gone, the `ext.screw` clause fires). That is a mismatch, so e4 holds. The rule's clauses are ordered so that e4 is read first. The Designer's deletion of record for the ext rule is in section 2.

---

## 2. The Designer

**Verdict: `span_lt:ext` admission (e1 to e4) SIGNED.** I object to the cover alternate `'--'` (NOTE D-r3-2, with a dry run). It is not a condition of the signature. I do not object to the offset u -110.

### 2.1 Evidence

Rule: `sketch_common.ext_issues`, l.2582 to 2632, with `EXT_OVERSHOOT_MAX` 3.0 (DECLARED). The premise and e1 to e4 match my r2 item 3 text.

Red-first evidence for K5-B44 to B47 is from the Engineer's §3 table (DECLARED). Fires-on-r3 and the deletions are MEASURED.

| Clause | B (fixture) | Fires on r3 | Red on r2 (Engineer §3) | Deletion (scratch copy) |
|---|---|---|---|---|
| e1 at a z_rule end | K5-B44: lower line 5 above the end | yes, 1/1 | fires 1, unadmitted sub-artist reason (red, reason) | `del_ext_e1`: `abs(near - z) > TOL_Z` set to False. B44 clean, **mismatch** |
| e2 starts on the screw edge | K5-B45: upper line starts 5 inboard | yes, 1/1 | same (red, reason) | `del_ext_e2`. B45 clean, **mismatch** |
| e3 ends 0 to 3 past the dimension line (**deletion of record**) | K5-B46: lower line run on 8 more (10 past) | yes, 1/1 | same (red, reason) | `del_ext_e3`: the overshoot test set to False. B46 clean, **mismatch**; K5-Z6, Z7 and the other 26 controls match |
| e4 parent is a reference line row | K5-B47: `:ext` on screw_c | yes, 1/1 | fires 2, unadmitted (red, reason and count) | `del_ext_e4`. B47 fires on another reason, **mismatch** |

- Z: live r3. The two lines are drawn at (-154, 340) to (-108, 340) and (-154, 1210) to (-108, 1210), solid, in the LOAD colour, 1 pt. The dimension line is at (-110, 340 to 1210) (MEASURED, rebuild pixel-equal to `wip/s3_jackscrew_section_r3.png`).
- The scale is 2.4514 px/mm (MEASURED, transData). The lines start at px 601, on the screw's inboard edge (-154), and the dimension line is at px 709.5 (-110.0) (MEASURED).
- The fixture docstring for B46 says "run on 10 past", and the code adds 8 to the existing 2. These agree (DERIVED).

### 2.2 Offset u -110: no objection

- The Loftsman test at u -225 puts both ends inside bracket_anchor_c and bracket_guide_c (Engineer §2, MEASURED there). Any u from -181 to -244 has the same fault, because the bearing lines lie inside the arm z bands. My r2 clear band (-244 to -210) was clear of parts along the line's length and not at its ends. Both ends of the span meet arm sections, so this withdraws my r2 pick of u -225.
- At u -110, the line crosses the ring web (z_S 380 to 400) and the gear's left piece (z_S 460 to 500), which was my r2 Correction 2. In the r3 crop the red 1 pt line reads over the black hatch and the ring outline. It sits 4.5 px clear of the bright-red drill-tube centreline at px 767.5 (MEASURED). Readability is for the fresh M1 to judge.
- The ext lines from the screw edge cross the inboard bearing race and the anchor/guide block section for about 15 mm before they reach free space (MEASURED, crops). That is unavoidable: the measured feature, the bearing line on the screw, is inside the block.

### 2.3 Cover alternate `'--'`: objection (NOTE, not a condition of signing)

- **Finding (MEASURED, `probes\cover_cmp.png`, r3 against the dry run, 5x zoom).** `'--'` puts one horizontal line in each cover piece. That line is parallel to the joint line below it and to the piece's own top and bottom edges, so the cover reads as a doubled edge or a second joint. I withdrew `'\\'` at r2 Correction 3 for the same fault: one or two lines per piece read as an unhatched piece.
- **Alternative, dry run `dry_vbar\` (MEASURED).** The value is `'||'`, with the spec hatch_alt, the hatch_split text, the legend text and FIXTURE_ALT changed:
  - `check_sketch.py s3 --rev 3`: 15/16, the same as r3. K8 is clean with 218 predicates, and S3-3 is red on the stale records only.
  - The line-family lint passes.
  - The PNG differs from r3 in 12 930 px, all at the cover and the legend line. Each cover piece shows two vertical lines, perpendicular to the joint, and reads hatched and set apart from the `//` block below.
  - Controls: K8-Z14, Z16 and B81 to B87 match. B79 and B80 fire with the right count. Their manifest reason literals name `'--'` and need `'||'` (text re-read only).
- **Disposition.** The orchestrator ruled `'--'`. The rule is signed with any admissible alternate. The value is for the orchestrator or Sean at the next drawn revision, or after the fresh M1 on r3 if M1 raises it. No FIX round is requested under the loop cap.

### 2.4 Designer NOTE (no FIX)

- **D-r3-1. Dimension terminator.** The `_` marker on `span_lt` lies along each extension line, 5.95 mm each side of the dimension line (Correction 1).
  - The dimension therefore has no terminator distinct from its extension lines, and the visible overshoot is 6.1 mm against e3's 2 mm.
  - It reads as a bracket over the span, and the label "S3-2 span L_t, K 0.7 870" names it.
  - At the next drawn revision, terminate with arrowheads or 45 deg ticks. Alternatively, e3 could read the parent's marker half-width.
  - No rule is broken: e3 governs the `:ext` artist only, and it is within bound.

---

## Gameplan lines to change

The Engineer's r3 items 2, 3 and 6 carry the rule text. Only Progress Log rows are added here.

1. Progress Log: insert after the row added by Engineer r3 item 11 (beginning `| 1.3 | 2026-11-26 | (h) P9 r3 (step1.3_engineer_revision_r3.md)`).
```
New: | 1.3 | 2026-11-26 | Raisers sign r3 (step1.3_raisers_sign_r3.md): Topologist SIGNED S3-3 link kinds and face sense (B16, B17), not_drawn deferred owner (B86), plan_axes:arc head (B43), hatch alternate line family (B87): each B fires on r3, red on pre-change per the Engineer table, one deletion per branch turns its B to a mismatch (28-control subset 28/28 on r3); Designer SIGNED span_lt:ext e1 to e4 (deletion of record e3: B46 mismatch), no objection to u -110; objection NOTE to the cover alternate '--' (one line per piece, parallel to the joint) with dry run '||' 15/16 as r3, B79/B80 reason literals only; NOTE D-r3-1 the span_lt '_' end marker runs 6 mm along each extension line (terminator); NOTEs R2-6, R2-7 carried |
```
