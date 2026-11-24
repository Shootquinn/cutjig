## 1. Basis

Sources: five result JSONs, Engineer report, signed crossreview, my params table. Built means a passing feature row in the JSON. Visual gate NOT RUN. This is a part-level read, not the Step 6 gate.

## 2. Receiver

Built: thread 149.58/144.58, pitch 8, 45 deg, right hand, 1 start, land 1.51 (signed 1.5); rim lead-in 1.249 (1.25); runout land 4.0; shoulder 36.5; spigot 160; register bore r 67.29; register chamfer 0.999; rim 88.5; asymmetric key slot 12 x 3.3 at 37 deg, floor to rim, off-axis (Rule P); floor hole 80.0; datum frame z -40.
Not built: none.
Drift: none beyond 0.01.
Assumption: solid spigot tube below z 0 to datum A. Acceptable. It is a datum-bearing body and no signed feature contradicts it.
**PASS**

## 3. Holder

Built: OD 134.08; cone 10 deg, height 30, bottom r 62.04, top r 56.7502; bore 113.5004; length 88.0; flange 144.08 x 8; key 11.75 x 3.0 x 40 at 37 deg, absent opposite; index notch 6 x 3, off-axis; four insert bores 5.0 x 12.0 on r 62; top 104.75.
Not built: none. The holder stop is the foot ring, a separate part.
Drift: cone top 56.7502 vs 56.75, exact tan 10. Acceptable as built; the formula governs.
**PASS**

## 4. Nut

Built: crest/root 145.28/150.28; fit offsets; tooth 3.7; right hand; bottom lead-in 0.899; one-ended thread start (groove below plate, none above); plate 7.5; overall 56.0; body OD 166.28; plate hole 136.08; bearing pocket 143.8 x 0.8; three pads (143.0 ID, 0.8 high, arc 9.983); tab 5.0 at r 70.6; three washer windows 10 wide; span 230; wings 40/28/14, taper 10.665 deg per edge, tip corners rounded; four tommy bosses OD 23, hole 13 x 20, axis z 36; release arrow depth 0.8; marked wing (Rule P); dust skirt (nut.length 48).
Not built: none.

Drift and deviations:
- Release arrow span 33.25 vs 33.75 deg. Acceptable as built. The shortfall is 0.5 deg, about 0.7 mm at the arrow radius, below the 1.0 deg check step. The shorter mark errs toward telling the user to keep turning. Directive to Engineer: record that the span includes head and mark line, so the 33.75 deg dead turn is not claimed to the arrow tip.
- Windows at 90/210/330 vs a 180 start. Acceptable. Spacing stays 120 deg, count 3, width 10, and 180 hit a wing. Directive: confirm in the JSON that no window coincides with a pad or tab azimuth. Tab gaps 0.50 tangential are already reported.
- Wing mark 21.86 mm vs `nut.arrow_length` 40. Acceptable as built, DIRECTIVE to fix the record. The wing is only 31.86 proud, so a 40 mm arrow cannot exist (it was my ASSUMED seed). Engineer: re-key `nut.arrow_length` as DERIVED = arm less two tab widths = 21.86, with source, status and the frozen test row.
- Open query, not a failure. The JSON shows one marked wing face and the release marker. It shows no separate tighten/loosen pair. Directive: state which built glyph is tighten and which is loosen; if only one exists, add the second before the Step 6 gate.
**PASS** (the arrow re-key and the tighten/loosen statement are required before Step 6)

## 5. Washer

Built: ID 136.8, OD 143.2, thickness 1.3, notch 6.0 wide x 2.0 deep, notch floor r 69.6, off-axis (Rule P). PTFE always fitted: the geometry is the full part.
Not built: none. Retention is by the nut tab (r 70.6) in the notch, a 1.00 radial gap.
Drift: none.
**PASS**

## 6. Collet foot ring (d 90 only)

Built: ring top 1.995 (2.0 less 0.005); ring OD r 66.99; lip 3.2; core seat height 2.5, width 3.0; ledge ID 86.0; foot key tip r 70.04, width 11.75, top at ring top, off-axis.
Deferred, not failed (collet generator): 12 slits, ligament 3.0, slit length 25.0; relief holes 8.0 (centres 7.0 and 25.0); bore lead-in chamfer; strain ratio; slit phase. Also listed in my params table and not in the Engineer's list: rim notches, grip-window label, colour, caddy-matched file name. Directive to Engineer: confirm in writing that these belong to the Step 5 generator. If any belongs to the foot ring, it is a failure now.
Drift and deviation:
- Ring bottom to floor 0.000 vs 0.005. Acceptable as built. The ring is a seat that must rest on the floor, and the top gap carries the 0.005. Directive: amend crossreview S3 to state the floor seat is a designed contact and the gap is carried at the holder interface. Overlap is 0.00 mm3.
**PASS** (functional features present; the deferrals must be confirmed)

## 7. Summary

| Part | Result |
|---|---|
| Receiver | PASS |
| Holder | PASS |
| Nut | PASS, with directives |
| Washer | PASS |
| Foot ring | PASS, deferrals to confirm |
