## Corrections to the brief

1. **TP1.3-12 and TP1.3-14 close as rules only.** The live S3 r2 K8 is red on both, 2 issues (MEASURED, `wip/s3_checks_r2.json`). Each red waits on a Designer value: the rear nut shoulder screw convention and the cover alternate. The fixtures carry stand-ins (`_designer_pending`). That is correct scaffolding. It does not close either value.
2. **S3-3-B14 does not test the new rule.** On the pre-change code it fires and fails only on the reason text: old "no horizontal edge", new "no bottom horizontal edge" (MEASURED, `pre_rf`). With the sense clause deleted it still matches (D01 below). It guards the old face-edge branch under kind face. Its red on the old code comes from a message rename, so it is not red-first evidence. The sense clause rests on B12 and B13.
3. **K8-B80 cannot be red on the pre-change code, and does not need to be.** It guards the lower boundary of the split: block pieces keep the material hatch. The old code puts the material hatch on every piece, the strictest case, so a plant of the alternate on a block piece fires there too. Its red-first is shown by deletion. Applying the alternate to every piece of a hatch_split row turns B80 red (D16). Accepted on that basis.
4. **Four rule branches have no B.** The current controls stay matched when each one is deleted:
   - link kind face with no face z;
   - lint: face link with no S3 certifier;
   - not_drawn deferred with no owner;
   - arc head direction.
   The arc fixture draws no head at all, while the live script draws one (`s3_jackscrew_section.py` l.319). A fifth branch, arc (a1) plan only, cannot be reached in S3 (Engineer Correction 4).
5. **The hatch-alternate lint compares strings.** It admits a density variant of a material pattern. `'////'` (aluminium family) and `'\\'` (steel family, half density) both pass (MEASURED). Both are on the Engineer's candidate list to The Designer.

Tags:
- MEASURED: runs on 2026-11-26 in the scratch copies under `D:\Unleashed Robotics\_scratch\cutjig\top_r2\`:
  - `sk\`: docs/sketches at S3 r2.
  - `pre_rf\`: the Engineer's pre-change code with the r2 fixtures.
  - `del_*`: deletion copies, logs in `probes\del_*.log`.
  - `sk_fix\` and `pre_fix\`: dry-run fixtures.
  - Python 3.12, matplotlib 3.11.2. TMP and TEMP set to `_scratch\cutjig\tmp`. Nothing under `docs/sketches/` edited.
- DERIVED: hand arithmetic.
- DECLARED: spec or ruling.

**Verdict: P7r RECHECK FAIL, 4 FIX.** Every FIX carries a dry run that passes. None changes S3 r2 pixels.

| Rule | Status |
|---|---|
| clause (6) occlusion | SIGNED |
| `screw_c:root` admission | SIGNED |
| link kinds and face sense | REFUSED pending FIX R2-1 |
| not_drawn bands | REFUSED pending FIX R2-2 |
| `plan_axes:arc` admission | REFUSED pending FIX R2-3 |
| hatch alternate per piece and its lint | REFUSED pending FIX R2-4 |

## 1 Closure of TP1.3-10 to -15 and -19 on S3 r2

| ID | State in docs/sketches/ (S3 r2) | Closed |
|---|---|---|
| TP1.3-10 | Every link of chains c, a and b carries `kind` (DECLARED, `s3_spec.yaml` l.177 to 228). The base route is core_750, core_seat (one_body), collet, receiver, with face `receiver_floor` and the collet above it. Member feet and bracket ends are `fastened`. ring\|bearing and bearing\|drill_tube are `declared`. S3-3-Z is clean on fresh records (MEASURED). Link count: c 19 - 1 = 18, a and b 16 - 1 = 15 each, 18 + 15 + 15 = 48 (DERIVED; equals the Engineer dry run). Live S3-3 red on the stale S1 r7 / S2 r5 records only (7 issues, MEASURED) | rule yes; FIX R2-1 (Bs) |
| TP1.3-11 | `render_occlusion` runs in `render_section`. Live K8 carries no clause 6 issue. The PNG shows the dashed hidden copies (core inside the drill head, shaft ends in the coupling). K8-B77 and B78 match | yes |
| TP1.3-12 | Every not_drawn entry has `omit`. The rear screw band `[-18.86, -8.86]` fires live (MEASURED) | rule yes, FIX R2-2; value to The Designer |
| TP1.3-13 | `plan_axes:arc` drawn as a Line2D, 0 to 90 at r 40, with a head at 90. The inset K5 passes. In the PNG the head at 90 points toward -X, which is counter-clockwise | rule yes; FIX R2-3 (head B) |
| TP1.3-14 | `cut_hatch` per piece, used by the renderer and clause (1). Live red: no alternate declared | rule yes, FIX R2-4; value to The Designer |
| TP1.3-15 | Spec `ticks` replaced by `root {from, to, d}`. Two dashed lines are drawn. K5 passes (MEASURED) | yes |
| TP1.3-19 | lever u = `liftsync.switch_r_in * sind(jackscrew.angle[2])` and `liftsync.lever_r_tip * sind(...)` (DECLARED, l.1357 to 1358). Live K5 lever passes | yes |

## 2 Rule rulings

Red-first column: the B on `pre_rf` (MEASURED). "Red" means the control does not match there.

### 2.1 S3-3 link kinds and face sense (TP1.3-10): REFUSED pending FIX R2-1

- **Premise.** In the cut case each link x → y carries -Z of x on y. A horizontal face carries the link in compression only with x above it. A link with no axial face carries the load by its kind: thread, one body, fastened (Step 2 bolts), or declared.
- **Z:** S3-3-Z, 48 links.
- **B:** B12 (cover face at the shoulder, x below), B13 (member foot), B14 (side face), B15 (no kind).

| Branch | B | Red-first (pre_rf) | Deletion (MEASURED) |
|---|---|---|---|
| sense (x above, y below) | B12, B13 | clean (red) | D01: B12 and B13 go clean, mismatch |
| face edge exists | B14 | fires, reason text only | D01: B14 still matches (Correction 2) |
| kind lint | B15 | clean (red) | D02: B15 mismatch |
| kind face, no face z (`s3_3` l.373) | **none** | — | D03: 15/15 still match |
| lint: face link with no S3 certifier (l.274) | **none** | — | D04: 15/15 still match |

- **FIX R2-1.** Add two Bs. Dry run (`sk_fix`, MEASURED):
  - S3-3-B16: frame_upper_c\|bracket_anchor_c with kind face and no face. Fires 1, reason "S3 face link names no face z". Clean on `pre_fix` (red).
  - S3-3-B17: base_plate\|base_frame with kind face (S1/S2 certifiers only). Fires 1, reason "face link with no S3 certifier". Clean on `pre_fix` (red).
- B14 stays as a guard of the old branch. Its manifest desc should say so: "regression guard; not red-first (reason text)".
- **NOTE R2-5.** My TP1.3-10 (d) remedy asked for the K7 certifiers to be removed from the `declared` links ring\|bearing and bearing\|drill_tube. Chain c keeps "S1 ring\|bearing C", "S2 ...", "S3 ring\|bearing", and no `declared` text naming S6-5. The kind alone declares the link. Spec text for The Designer's re-sign: certifiers `["declared (S6-5 draws the axial seat)"]` on ring\|bearing in a, b and c.

### 2.2 Section convention clause (6) occlusion (TP1.3-11): SIGNED

- **Premise.** An unsectioned row has its axis in the plane: a solid of revolution with its front surface at x = +sqrt(R² - (u - u_c)²) > 0. Every section area at x <= 0 inside its outline lies behind it.
- **Premise check:** the existing clause (2) axis-in-plane test (`sketch_common` l.4974, B73).
- **Z:** K8-Z14.
- **B:** B77 (6a), B78 (6b).
- **Red-first:** B77 and B78 clean on pre_rf (red).
- **Deletion:**
  - D06 (6a removed): B77 fires with the 6b reason, mismatch.
  - D07 (6b removed): B78 clean, mismatch.
  - D08 (renderer split removed): Z14 fires, and B78 fires with the 6a reason. Both mismatch.

### 2.3 not_drawn omit and band lint (TP1.3-12): REFUSED pending FIX R2-2

- **Premise.** An omitted part lies wholly in front of the plane or wholly past one profile width, or its omission is deferred to a named owner.
- **Z:** K8-Z14.
- **B:** B83 (live screw), B84 (no omit), B85 (pinions on the footprint).
- **Red-first:** all three clean on pre_rf (red).
- **Deletion:**
  - D09 (band test): B83 and B85 mismatch.
  - D11 (omit): B84 mismatch.
  - D10 (deferred with no owner): 3/3 still match. **The deferred branch is the rule's escape hatch, and it has no B.**
- **FIX R2-2.** Add K8-B86: the receiver shoulder-bolt entry with its owner removed. Dry run: fires 1, "deferred with no owner". Clean on `pre_fix` (red).
- **NOTE R2-6.** Two entries carry literal x bands that no key reads:
  - pinions `-65.09`, a hand value from the trapezoid;
  - base-frame bands, measured from S2.
  
  `--stale` cannot reach them. Margins today are 5.09 and 22.00 (DERIVED). Write them as expressions over the pinion and base keys, as the nut-screw and standoff entries already are.

### 2.4 `plan_axes:arc` admission (TP1.3-13): REFUSED pending FIX R2-3

- **Premise.** The arc is the one artist that states the theta sense. Its direction is a sign check: cross(p_i, p_i+1) > 0, and for the head, (head - tail) . (-sin theta1, cos theta1) > 0.
- **Z:** K5-Z7.
- **B:** B40 (reversed), B41 (radius), B42 (section Axes).
- **Red-first:** fire with the wrong reason and count on pre_rf (red). This is accepted: the old code refuses the sub-artist as unadmitted.
- **Deletion:**
  - D12 (line ccw test): B40 mismatch.
  - D13 (head direction): 3/3 still match. The Z7 fixture draws no head, so every head branch runs on no control. The head is what the reader reads as the sense. A head drawn clockwise on a ccw line passes today's controls.
  - D14 (a1 plan only): 3/3 still match; unreachable in S3. **NOTE R2-7:** a1 is reachable by a spec plant: `arc` declared on a section row with a `<row>:arc` drawn in the section. Add it when K5 next changes.
- **FIX R2-3.** The fixture draws the head as the live script does. Dry run (`sk_fix`):
  - TR-Z5, head from 80 to 90 deg: clean.
  - K5-B43, head from 100 to 90 deg on the ccw line: fires 1, "arc head points against theta (clockwise)". On `pre_fix` it fires with the unadmitted reason (red).

### 2.5 hatch_split alternate per piece and its lint (TP1.3-14): REFUSED pending FIX R2-4

- **Premise.** The alternate marks the cover as a separate piece of the same material. A reader tells material by line family: direction, cross or dot. A repeated character changes only the density. An alternate must therefore differ in line family from every material pattern and every other alternate.
- **Z:** K8-Z16.
- **B:** B79 (cover plain), B80 (block alternate), B81 (equal to steel), B82 (missing).
- **Red-first:** B79, B81 and B82 clean on pre_rf (red). B80: Correction 3.
- **Deletion:**
  - D15 (clause 1 reads the plain table): Z16 fires, and B79, B80, B81 mismatch.
  - D16 (alternate on every piece): B80 mismatch.
  - D17 (lint): B81 mismatch.
- **The lint predicate is wrong.** It uses string equality. Lint output on the current code: `'////'`, `'\\'`, `'/'`, `'xxx'` and `'...'` each produce no issue (MEASURED).
- **FIX R2-4.** Compare line families: fam(h) = the set of characters of h, with `+` → {`|`, `-`} and `x`, `X` → {`/`, `\`}. The lint fires when fam(alt) equals fam of any HATCH value or of another alternate. Dry run (`sk_fix`, patched `hatch_alt_issues`):
  - `'--'`, `'\|\|'`, `'++'` pass.
  - `'////'`, `'\\'`, `'/'`, `'xxx'`, `'/\\'`, `'...'` fire.
  - K8-Z14, Z16 and B79 to B85 all match.
  - New B K8-B87 (alternate `'////'`): fires 1, and is clean on the current code (red).
  - Of the Engineer's five candidates, `'////'` and `'\\'` leave the admissible set. `'--'`, `'\|\|'` and `'++'` remain. That is a property of the rule. The pick stays with The Designer.

### 2.6 `screw_c:root` admission (TP1.3-15): SIGNED

- **Premise.** The thread is stated by its span and root only. The lead is in the label.
- **Z:** K5-Z6.
- **B:** B37 (nominal radius), B38 (past thread_end), B39 (solid).
- **Red-first:** fire with the wrong reason and count on pre_rf (red; unadmitted sub-artist).
- **Deletion:** D18 (u), D19 (z span) and D20 (dashed) each turn their B to a mismatch.
- (r5), vertices inside the screw, is implied by (r3), since d_r 8.5 < d 12. No separate B is needed.

## 3 Findings

| ID | Kind | Owner | Finding |
|---|---|---|---|
| R2-1 | FIX | The Engineer | S3-3: add B16 (face kind, no face z) and B17 (face link with no S3 certifier). Re-describe B14 as a regression guard |
| R2-2 | FIX | The Engineer | K8: add B86, a not_drawn entry deferred with no owner |
| R2-3 | FIX | The Engineer | K5 arc: the fixture draws the head; add B43, head clockwise on a ccw line |
| R2-4 | FIX | The Engineer (lint), The Designer (informed) | hatch_alt lint by line family; add B87 `'////'` |
| R2-5 | NOTE | The Designer | declared ring\|bearing and bearing\|drill_tube: replace the K7 certifiers with `declared (S6-5 ...)` text |
| R2-6 | NOTE | The Engineer, The Designer | not_drawn literal x bands (pinions, base frame) as key expressions |
| R2-7 | NOTE | The Engineer | arc (a1) plan-only branch: reachable by a spec plant, no B |

Controls after the FIXes: 392 + 6 (S3-3-B16, B17, K8-B86, B87, K5-B43, Z for the head; the Z may replace K5-Z7) = 398 or 397 (DERIVED).

## Gameplan lines to change

Apply after the Engineer r2 items (`step1.3_engineer_revision_r2.md`, Gameplan lines 2, 3, 6, 9). Each Old below is text in the Engineer's New.

1. l.139 (K5 row), after Engineer item 2.
   - Old:
     ```
     (K5-Z7, B40 reversed, B41 r + 5, B42 in the section; TP1.3-13) |
     ```
   - New:
     ```
     (K5-Z7 with the head drawn, B40 reversed, B41 r + 5, B42 in the section, B43 head clockwise on a ccw line; TP1.3-13, Topologist 1.3 P7r R2-3) |
     ```
2. l.142 (K8 row), after Engineer item 3.
   - Old:
     ```
     alternates differ from every material pattern (K8-Z16, B79 to B82; TP1.3-14)
     ```
   - New:
     ```
     alternates differ in line family (characters, + as | and -, x as / and \) from every material pattern and every other alternate (K8-Z16, B79 to B82, B87 alternate '////'; TP1.3-14, Topologist 1.3 P7r R2-4)
     ```
3. l.142 (K8 row), same item.
   - Old:
     ```
     or deferred with an owner (K8-B83 to B85; TP1.3-12)
     ```
   - New:
     ```
     or deferred with an owner (K8-B83 to B85, B86 deferred with no owner; TP1.3-12, Topologist 1.3 P7r R2-2)
     ```
4. l.288 (S3-3 row), after Engineer item 6.
   - Old:
     ```
     every link carries a kind: face with its sense, face_record, thread, one_body, fastened, declared)
     ```
   - New:
     ```
     every link carries a kind: face with its sense, face_record, thread, one_body, fastened, declared; S3-3-B12, B13 sense, B15 kind, B16 face kind with no face z, B17 face link with no S3 certifier, B14 a regression guard of the face-edge branch; Topologist 1.3 P7r R2-1)
     ```
5. Progress Log: insert after the row added by Engineer item 9 (beginning `| 1.3 | 2026-11-26 | (h) P9 (step1.3_engineer_revision_r2.md)`).
   - New:
     ```
     | 1.3 | 2026-11-26 | P7r Topologist recheck (step1.3_topologist_recheck_r2.md): TP1.3-10 to -15 and -19 closed as rules on S3 r2 (-12, -14 values with The Designer); 48 links DERIVED; SIGNED clause (6) occlusion and screw_c:root; REFUSED link kinds, not_drawn bands, plan_axes:arc, hatch alternate pending FIX R2-1 to R2-4 (five rule branches with no B: face kind without face z, face link without S3, deferred without owner, arc head direction; hatch lint by string admits '////' and '\\'), each dry-run clean in scratch; S3-3-B14 not red-first (reason text), K8-B80 red-first by deletion; NOTEs R2-5 to R2-7 |
     ```
