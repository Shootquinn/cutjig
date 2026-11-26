# Step 1.3 step 0 check (P0T), The Topologist

Date 2026-11-26. Read: `step1.3_engineer_step0.md` sections 6, 7, 8, 11; `docs/sketches/sketch_common.py` (`zero_area_issue`, `k5`, `sense_lint`, `cover_issues`, `k9`, `classify`, `expected_projection`); `fixtures/manifest.yaml` and `fixtures/builders.py` (K5-B19, K8-B42, K8-B43); `s1_side_poses.py` l.220-235; `s1_spec.yaml` anchor rows; gameplan l.139, l.665-666, Design Notes 31. Probe scripts in scratchpad `p0t/` (probe.py, escape.py, dryrun.py, pix.py, pix2.py), each run on the live tree through `builders._script_ctx` (the drawing scripts of record). No file under `docs/sketches/` edited.

## Corrections to the brief

1. TP1.2-18 as implemented is the Manager's form (owner names a Step id or a sketch id). My 1.2 NOTE proposed an overlay key with status ASSUMED or a T2 row. The implemented form is accepted (NOTE 2 below).
2. The task's "deletion test as for K8-B34 to B36" is done here by monkeypatching the clause out of the loaded module (MEASURED), not by editing the file.
3. K5-Z2 is the fixture S1 drawing (`_s1_ctx`), not the S1 r7 script drawing. No Z for TP1.1-9 holds on live S1 r7; the live S1 r7 drawing is the known-bad case (section 3).

## 1. Each lint: premise, red-first, Z

| Lint | Premise | B on pre-change behaviour (clause deleted) | B with clause | Z live |
|---|---|---|---|---|
| TP1.1-9 K5 zero-area (`zero_area_issue`) | A row whose kind draws an area (not line, arrow, callout) projects a solid part, so each of its patches encloses area | K5-B19: pass, 0 issues, "296 tagged artist(s) projected" (MEASURED) | fail 1, "load/drill_tube: zero-area Rectangle (width 20, height 0) on a cylinder row (TP1.1-9)" (MEASURED) | S2 r5 clean, 105 artists (MEASURED); S1 r7 fails 8 (section 3) |
| TP1.2-18 `STAND_IN_OWNER` | A stand-in names who resolves it | K8-B42: pass, 0 issues, "190 predicate(s) hold" (regex replaced by match-any) | fail 2: owner spec error plus the cover converse on the voided exemption (MEASURED) | S2 ties "Step 2: rod top support ..." pass (Engineer s2 r5 17/17) |
| NOTE 2 `FRAME_VALUES` | `frame` takes a known value | K8-B43: pass, 0 issues, "185 predicate(s) hold" ("polar" added to the set) | fail 1, "motor23_a outboard: spec error, unknown frame 'polar' (known: radial)" (MEASURED) | S2 six `frame: radial` pass; S1 none |

Each B reproduces its defect without the clause and fires with it. TP1.2-18 and NOTE 2: SIGNED.

TP1.1-9: the premise is not enforced by the rule as written. Two routes past it, both MEASURED on the live drawings with the current code:

| Route | Planted | K5 now |
|---|---|---|
| Sliver Rectangle: area threshold is absolute, so a long thin Rectangle clears 0.01 mm² | S1 r7 anchor lines set to height 0.001 (area 42 x 0.001 = 0.042 mm², DERIVED) | pass, 0 issues, "343 tagged artist(s) projected" |
| Round patch: the lint tests Rectangle and Polygon only | S2 r5 `screw_a` Circle radius 0 at load | pass, 0 issues, "105 tagged artist(s) projected" |

The first is the exact device of TP1.1-9 with one digit changed; an r8 drawing could clear K5 that way. Both go to FIX 1.

## 2. Exemptions (line, arrow, callout, Text, ticks, outline)

| Exemption | What keeps a part row from hiding behind it | Holds |
|---|---|---|
| kind line / arrow / callout | Rows of those kinds: S1 floor, bore_ceiling, keepout, pinion_axis_a/_b, height_target; S2 base_spigot_hole, base_slots, base_key_pockets, base_pin_pocket, slot_line_c, slot_lines, pinion_axis_a/_b/_c, keepout, collet_axis (arrow), sightline_f6. None is a solid part (holes, slots and pockets are voids in the plate) (MEASURED from both specs). The kind is a spec decision; only the Designer's (b) part list guards it | yes on live specs; NOTE 1 |
| Text | `artists()` excludes `ax.texts`; K9 fails a part row whose only artist is a Text ("a Text carries its gid") unless the row is kind callout | yes |
| `<row>:ticks`, `<row>:outline` | gid differs from the row id, so K9 still needs an artist tagged `<row>` at every applicable pose, and that artist is under the zero-area lint; admission needs the row's K8 premise predicate (ticks_radial, outline_matches) | yes |
| non-Patch artist (Line2D, LineCollection) tagged with a part row's own id | Falls through `zero_area_issue`; caught today only by the projection compare (`classify` "line" against the row's expected or spec projection). Every prism, plate and sector row in S1 and S2 carries `projection` and every round kind has an expected one, so no live route; a future prism row without `projection` drawn as a Line2D passes K5 | live yes; folded into FIX 1 (c) |
| unknown sub-suffix (e.g. `anchor_a:line`) | K5 `continue`s silently; K9 fails "tagged artist anchor_a:line has no spec row" | yes, through K9 |

No exemption hides a part row on S1 r7 or S2 r5.

## 3. Live patches caught

S1 r7: 8, MEASURED, K5 reason "load/anchor_a: zero-area Rectangle (width 42, height 0) on a prism row (TP1.1-9)" and the same for anchor_b, at load, start, capture_end, park. Artist: `s1_side_poses.py` l.230, `sc.draw_rect(ax, f"anchor_{s}", x0, x1, (z0 + z1) / 2, (z0 + z1) / 2, linewidth=2)`, the bearing line the shape note calls for ("bearing line marked"). Width 42 = 2 x `jackscrew.nut_flange_od / 2` (DERIVED from the row's place half_width). It lies inside the anchor block's drawn rectangle at mid-height 280 z_A (265 + 30 / 2, DERIVED). The accepted pixels are not wrong as a picture: the line marks the bearing plane and sits inside its part. The record is wrong in kind: the part row carries an artist that is no projection of it, which is the device TP1.1-9 closes.

S2 r5: 0 (MEASURED).

## 4. K5 ruling: S1 r8 anchor mark (Engineer section 11 item 1)

Ruling: option A SIGNED, under the admission rule below, drawn in S1 r8 (Design Notes 31 opens r8 for the screw and anchor rows). Option C REFUSED (an exemption by device; the device then carries any line). Option B (delete the line) is admissible and needs no rule, but drops the Designer's shape note; it is the fall-back if the rule fails its Z or B.

**Rule K5 mark admission, `<row>:line`.** K5 admits one Line2D sub-artist `<row>:line` per row per pose, as ink on its parent part, when all hold; K9 admits the suffix (`SUB_SUFFIXES` gains `:line`) only with the parent row drawn under its own id at that pose.

Premise: a mark is ink on its part. It carries no area, lies wholly on the part's drawn area, and is fixed in place and direction by the spec, so it can neither stand in for the part nor carry a line elsewhere.

Premise checks (each in K5, each with its own B):

| # | Check | Form |
|---|---|---|
| M1 | Declared: the parent row carries `mark: {sub: line, z: <expr>, source: <text>}`; S1 r8 anchors: `z: "jackscrew.anchor_z + jackscrew.anchor_allowance / 2"` (280 z_A at the r8 values, DERIVED; the back-to-back pair's contact plane at mid-block, ASSUMED per Design Notes 31, block 30 tall) | spec field present, else "mark sub-artist without a mark declaration on its row (premise unenforced)" |
| M2 | Parent is an area row and is drawn: parent kind not in NO_AREA_KINDS, and at the pose at least one artist tagged `<row>` that passes the FIX 1 thickness test | presence; the parent's own artist carries the part |
| M3 | Form: a Line2D, exactly 2 vertices after the transform chain (TP-1), one per row per pose | type and count |
| M4 | Containment: both endpoints in the parent's drawn convex piece, half-space test on every edge e = (p, q) of the CCW piece: cross(q - p, v - p) >= -TOL_Z x abs(q - p) for each endpoint v. Endpoints inside a convex piece put the whole segment inside it | sign check |
| M5 | Place and direction (side views): abs(z1 - z0) <= TOL_Z (direction normal to the screw axis Z: dot(v1 - v0, z-hat) = 0 within TOL_Z), z = eval(mark.z) within TOL_Z, and each endpoint on one of the parent piece's two vertical edges within TOL_Z (the mark is the chord of the part at mark.z). Other views: the rule does not admit; a mark in plan or the S3 section needs its own form at (b)/(c) | sign and equality |

Z: live S1 r8 drawing (anchors with `:line`, clean). Fixture Z: `_s1_ctx` S1 with both marks drawn by rule.
B controls, each red on the pre-change code (there the `:line` gid is skipped by K5 and fails K9 "has no spec row"; the K5 reason substrings do not match):
- B-m1 `anchor_a:line` with `mark` deleted from the row (M1).
- B-m2 `anchor_a:line` drawn, `anchor_a` block artist removed at load (M2; K9 also fires "spec row anchor_a has no patch", planted count states both).
- B-m3a the mark drawn as a zero-height Rectangle under `anchor_a:line` (M3 type); B-m3b two `:line` artists on anchor_a (M3 count).
- B-m4 right endpoint 5 mm outside the block (x1 + 5) (M4).
- B-m5a mark at z 282 against mark.z 280 (M5 place); B-m5b mark tilted, z1 = z0 + 2 (M5 direction).
- The S1 r7 drawing itself is the known-bad case for the parent rule: zero-height Rectangle under the row's own id, K5 fail 8.

Pixel dry run (scratchpad `p0t/pix.py`, `pix2.py`; MEASURED; the unmodified script figures saved with `bbox_inches="tight"` are 0 pixels off the accepted r7 PNGs, so the comparison is valid):

| Line2D variant replacing the zero-height Rectangle | load | start | capture_end | park |
|---|---|---|---|---|
| color k, lw 2, defaults | 60 | 60 | 61 | 61 |
| butt cap, miter join, zorder 1 | 0 | 0 | 1 | 1 |
| butt cap, round join, zorder 1 | 0 | 0 | 1 | 1 |
| projecting cap, zorder 1 | 48 | 48 | 49 | 49 |
| closed 5-vertex path, butt, miter | 59 | 54 | 57 | 59 |

Best variant: 1 pixel at capture_end and park, an anti-aliasing step of 1/255 (0.0784 against 0.0824, 0.5451 against 0.5412), from the line now drawing after the later patches at zorder 1. Not pixel-equal, so it cannot ride on r7 under `--accept`; it lands in r8 with the Tr12x3 redraw and M1 reads it on r8 pixels. S1 r7 stays accepted as the Design Notes 13 record until r8 is accepted; ORCH-A re-accepts S2 r5 only.

Signature: the rule M1 to M5 with the listed Z and B, shown red on the pre-change code at r8, is SIGNED in advance; I re-check the implementation at (e) of S1 r8 (P7b).

## 5. Findings

**FIX 1. TP1.1-9 tests an absolute area on two patch classes; replace with a thickness test on every patch, and fail a non-patch artist on an area row.** Rule: for every artist tagged with a row id whose kind is not in NO_AREA_KINDS:
- (a) Patch (Rectangle, Polygon, Circle, Ellipse, Annulus, any other): least drawn thickness t <= TOL_Z (0.05 mm) fails. t = 2A / P over the artist's pieces in data coordinates (through the transform chain); for an Annulus t = outer radius - inner radius of the transformed rings (2A/P on the two rings as separate pieces overstates it). For a w x h rectangle 2A/P = wh / (w + h), the short side to first order.
- (b) Reason text keeps the substrings of K5-B19 ("zero-area Rectangle", "on a cylinder row (TP1.1-9)") so K5-B19 stays matched.
- (c) A Line2D or Collection tagged with an area row's own id fails ("<type> on a <kind> row draws no area (TP1.1-9)"), independent of `projection`.
Dry run (scratchpad `p0t/dryrun.py`, MEASURED): live S1 r7 fires the same 8 anchor lines and nothing else, least passing 1.3636 mm (core_seat); live S2 r5 fires 0, least passing 3.175 mm (drill_tube annulus wall, DERIVED (152.4 - 146.05) / 2) then 3.9952 mm (screw circles); fixture S1 (K5-Z2) fires 0; K5-B19 fires 1; S1 sliver 0.001 fires 8; S2 screw_a radius 0 fires 1. (c) fires 0 on both live drawings (no non-patch artist on an area row, MEASURED in `p0t/probe.py`). Margin to the thinnest live part: 27x (1.3636 / 0.05, DERIVED).
New controls, each red on the pre-change code (MEASURED above: both pass K5 today): K5-B20 S1 anchor line height 0.001; K5-B21 S2 screw_a Circle radius 0; K5-B22 a fixture prism row with `projection` deleted, drawn as a Line2D under its own id. Z: K5-Z2, K5-Z3 unchanged.
Effect on records: S1 r7 unchanged in kind (8 issues), S2 r5 17/17 (dry run).

**NOTE 1.** The NO_AREA_KINDS exemption rests on the spec's kind; nothing checks that a line row is not a solid part. The Designer's (b) part list is the guard; S3's spec sign-off should name every line row and say what it marks.

**NOTE 2.** `STAND_IN_OWNER` matches a Step or sketch token anywhere in the string: "tbd, not S3" passes, as does "Step 9". Accepted for step 0; if S3 adds stand-ins, the stronger form is an overlay key named in the owner with status ASSUMED (the S2 ties name `guide.top_support`, ASSUMED, MEASURED in the overlay).

**NOTE 3.** `frame` is read only by the outboard predicate; `frame: radial` on any other predicate passes `sense_lint` and is ignored. No live row carries one. Admit `frame` only on `outboard` when S3 adds sense rows.

Verdict: **FIX** (1 item: FIX 1). TP1.2-18 and Topologist 1.2 (c) NOTE 2 SIGNED. TP1.1-9 signs on FIX 1 closed. K5 anchor mark: option A SIGNED under rule M1 to M5 for S1 r8; option C REFUSED.

## Gameplan lines to change

**l.139** (K table, K5 row).
Old: `1.3 step 0: a Rectangle of zero width or height, or a Polygon of area <= 0.01 mm², on a row whose kind is not line, arrow or callout fails (TP1.1-9) |`
New: `1.3 step 0: on a row whose kind is not line, arrow or callout, a patch whose least drawn thickness 2A/P (Annulus: radial width) is <= 0.05 mm fails, and a Line2D or Collection under the row's own id fails (TP1.1-9; Topologist P0T FIX 1); a row carrying `mark: {sub: line, z, source}` admits one Line2D <row>:line per pose, 2 vertices, both ends in the parent's drawn piece (half-space test), horizontal at eval(mark.z) on the piece's vertical edges, with the parent drawn under its own id (Topologist P0T ruling, S1 r8 anchors) |`
Old: `K5-B19 zero-height Rectangle on the drill tube (TP1.1-9) |`
New: `K5-B19 zero-height Rectangle on the drill tube (TP1.1-9); K5-B20 S1 anchor line 0.001 high; K5-B21 S2 screw circle radius 0; K5-B22 prism row without projection drawn as a Line2D; mark controls B-m1 to B-m5b at S1 r8 |`

**l.666** (Design Notes 25, TP1.1-9 row).
Old: `| TP1.1-9 | A zero-height Rectangle passes K5 as "rectangle"; optional K5 lint for zero-area patches on non-line rows | 1.3 (S3), with TP-7 | The Topologist proposes; The Engineer |`
New: `| TP1.1-9 | A zero-height Rectangle passes K5 as "rectangle"; K5 zero-area lint landed at 1.3 step 0, thickness form per Topologist P0T FIX 1 (step1.3_topologist_step0_check.md); S1 r7 anchor bearing line (s1_side_poses.py l.230) fails 8 and is redrawn in S1 r8 as anchor_<s>:line under the K5 mark admission rule | 1.3 step 0 (P0f); S1 r8 | The Topologist proposes; The Engineer |`

**l.665** (Design Notes 25, TP1.2-18/19 row).
Old: `stand_in_owner accepts any non-empty string;`
New: `stand_in_owner must name a Step or sketch id (1.3 step 0, K8-B42, signed P0T; overlay-key form deferred to S3 stand-ins);`
