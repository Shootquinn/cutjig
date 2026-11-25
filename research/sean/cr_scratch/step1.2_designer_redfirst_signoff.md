# Step 1.2 (c) Designer raiser signatures

Read 2026-11-25: `research/sean/cr_scratch/step1.2_engineer_redfirst.md` (sections 1d, 1e, 2, 7, 8), `docs/sketches/checks_s2.py` (S2-3, S2-5a, S2-5b, `_outline`), `docs/sketches/sketch_common.py` (`part_head`, `figure_note_issues`), `docs/sketches/s2_spec.yaml` (`plan_figure`, `not_drawn`, `s2_checks`, gear row), `docs/sketches/s1_spec.yaml` (`not_drawn`, l.156-158).

| Rule | Controls | Verdict |
|---|---|---|
| 1 Figure note check (K4) | K4-Z2, K4-B4, K4-B5 | **NOT SIGNED** (FIX R1) |
| 2 Sector equality premise (K8) | K8-B23 | **SIGNED** |
| 3 S2-5a and S2-5b on plan outlines | S2-5a Z/B, S2-5b Z/B | **SIGNED** |
| 4 S2-3 drawn pitch point at the heel-edge midpoint | S2-3 Z/B | **SIGNED** |
| 5 Gear `section` spec edit (bore r 90 to OD r 126.32), with the Loftsman | K7-Z15 | **SIGNED (Designer)**; the Loftsman signs placement |

## Corrections to the brief

1. **The figure-note rule exempts S1 by sketch id. Only S1 r4 was accepted before the rule.** `figure_note_issues` returns no issue for `sketch: s1` whatever its `not_drawn` holds. At the 1.2 (b) fix pass S1 r5 gained a `not_drawn` entry: the LM20UU bushing inside the housing, which the S1 r5 side view draws (`s1_spec.yaml` l.157-158). S1 r5 is a new revision drawn after the rule, so detail 1 common (b) applies to it: "the figure note states the not-drawn parts". As written, the r5 figures can omit the bushing and K4 still reads clean. DERIVED, from the code.

## 1 Figure note check (K4-Z2, B4, B5): NOT SIGNED

The rule does what FIX 3 asked for S2:
- `part_head` cuts at " (" or " at ". The six S2 heads are wing nut, collet, holder, power-off hold device, descent-stop pads, LM20UU bushing. Each one appears in `plan_figure.figure_note` (whitespace-normalised) and in the drawn Text `note:figure_note`. Z2 reads clean.
- B4 (drawn note without the bushing) and B5 (a part in neither note, planted 2) fire on the reason. On the pre-change code both read clean, so these controls are what make the rule bite.
- The check covers each figure's first axes. S2 has one axes per figure (one plan figure).

**FIX R1.** Replace the sketch-id exemption with a revision exemption. A spec with `not_drawn` and no figure note fails unless it is the accepted record it was signed under. That means: exempt S1 only while its `not_drawn` is absent (r4), or key the exemption on an accepted record that predates the rule. Then S1 r5 carries `figure_note: "Not drawn: LM20UU bushing (inside the housing and lug)"`, a top-level field or a `figure` entry, and `s1_side_poses.py` draws it as Text gid `note:figure_note` on each of the four pose figures. Add one B: S1 r5 spec with `not_drawn` and no figure note, firing on "without figure_note". Re-sign scope: the exemption line in `figure_note_issues`, the S1 spec field, and the new B.

## 2 Sector equality premise (K8-B23): SIGNED

S2-5a and S2-5b read the drawn sector, so the drawn sector must be the spec wedge. K8 checks both directions:
- Drawn points inside the wedge. This fires on a sector drawn wider, such as the 130 deg S2-5a B.
- The spec boundary within 0.05 of the drawing: apex, arc at 1 deg, both edges. This fires on a sector drawn narrower: B23 at half-angle 40, boundary 34.86 outside.
- A 1 deg chord at r 400 has a sagitta of 400 (1 - cos 0.5 deg) = 0.015, under 0.05 (DERIVED). Every fixed part S2-5a tests lies inside r 304, so the arc never decides a result.
- Premise and check ship together in this revision (detail 1 common (h)).

## 3 S2-5a and S2-5b on plan outlines: SIGNED

- S2-5a measures each fixed part's plan outline, the spec footprint K8 plan_extent holds around the drawn part, against the drawn sector. It reads **11.71** (lift motor circumscribing circle: 160 sin 15 - 29.70 = 41.41 - 29.70, DERIVED). That is the value in my 1.2 (a) section 5 and in the gameplan row.
- The drawn 42 square gives 15.69 (41.41 - 21 (cos 15 + sin 15), DERIVED). The outline value is the conservative one, and it closes the narrower-than-footprint route that M1 caught at S1. A part drawn smaller than its footprint can no longer pass S2-5a.
- Touching fails (distance <= 0.05 is an issue), which is right for F.
- B: the 130 deg sector fires 18 on the reason (arms, blocks, lift motors, members at 30 and 150). Agreed.
- S2-5b selects ring parts by plan-outline overlap with the drawn sector and takes each part's whole-part lowest z at load. Taking the whole part is conservative when only a corner enters the sector.
  - A sector that holds no ring part raises Content. The premise cannot pass vacuously.
  - Z: 8 parts, least 136.84 (bearing, 1076.84 - 940). B: NEMA 23 c bottom at 930 fires on the reason. Matches the rule I raised at 1.2 (a).
- Scope stays as raised: S2-5b binds at load only. The gear passing through the sector during a cut is the Step 2 guard row (watch-row hazard), not this premise.

## 4 S2-3 drawn pitch point at the heel: SIGNED

- In a bevel pair the pitch diameter is defined at the large end (heel). `gear.pitch_diameter` 250 is the gear's back-cone pitch circle, r 125, near its OD r 126.32.
- The pinion axis is radial with its apex on the drill axis, so a point's distance from the apex along the pinion axis equals its plan radius. The two pitch cones touch along a line in the plane through the pinion axis and the drill axis. In plan, the heel pitch point therefore projects onto the pinion's radial axis at r = gear pitch radius.
- The heel edge of the drawn toothed trapezoid lies at `pinion.r_heel` 125 across the pinion diameter. Its midpoint is on the axis at r 125. So the heel-edge midpoint is the right drawn quantity. DERIVED.
- A pinion drawn off its azimuth moves the midpoint tangentially. S2-1 (azimuth) and K5 TP-13 (edge pair across the radial direction) catch that first.
- `heel_point` takes the outer of the two edges across the radial direction, so a hub rectangle cannot stand in for the heel (the trapezoid filter excludes rectangles).
- Z: three pitch points at r 125.00 within 0.000. B: `pinion.r_heel` = `gear.od / 2` (126.32) fires 3, "pitch point r 126.32 vs gear pitch radius 125.00". This is the gameplan B, "pinion placed on the gear OD".
- NOTE: Z holds by the overlay identity `pinion.r_heel` = `gear.pitch_diameter / 2`, both ASSUMED. S2-3 certifies that the drawing follows that identity. S6 sizes the pair (Step 1.6) and re-runs it.

## 5 Gear `section` (bore r 90 to OD r 126.32): SIGNED (Designer)

- Seen from above, a bevel ring gear is solid from its bore to its OD. The annulus r 90 to 126.32 is the true plan section, and it matches my 1.2 (a) shape note ("annulus r 90 to 126.32").
- The depth-band disk r 126.32 it replaces filled the bore, which made gear|gear_hub (hub r 76.2 to 90) and gear|drill_tube fail as overlaps that do not exist.
- With the section: gear|gear_hub is plan-contact at r 90 (C), gear|drill_tube is 13.80 clear in plan (90 - 76.2, DERIVED), and gear|pinion stays N. The pinion row has `place` and no `section`, so the K7 refusal of N between two section rows does not apply.
- No key, class or row moves. `section` is outside the X1 field list and the S1 gear row has none. The S1 gear stays a side-section trapezoid with its depth band, so S1 is unchanged. The Loftsman signs the placement.

## Gameplan lines to change

**l.138** (K4 row), the figure-note fragment the Engineer proposes (his section 8). Replace his new text with this version, which carries the exemption as FIX R1 rules it:

Old:
```
a label number that differs from the key value fails |
```
New:
```
a label number that differs from the key value fails; from S2 and S1 r5 on, the spec figure_note and the drawn Text note:figure_note name the head (text before " (" or " at ") of every not_drawn part; only a revision accepted before the rule with no not_drawn entry is exempt (1.2 (c), Designer 1.2 (b) FIX 3, Designer 1.2 (c) FIX R1) |
```

**l.257** (S2-5b row; the line after S2-5a), check cell. Verify the line number against the S2-5a fragment the Engineer gives at l.257.

Old:
```
at load every ring-mounted part whose plan footprint enters the sector lies at least 10 above the top of operator.hand_band (940 z_A); least: bearing bottom 1076.84, margin 136.84
```
New:
```
at load every ring-mounted part whose plan outline enters the drawn sector lies, by its lowest z, at least 10 above the top of operator.hand_band (940 z_A); no ring part in the sector is a content failure; least: bearing bottom 1076.84, margin 136.84 (1.2 (c))
```
