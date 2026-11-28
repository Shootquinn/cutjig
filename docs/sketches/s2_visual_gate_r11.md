# Corrections to the brief

None. Measurement basis: pixels from s2_plan_r11.png and accepted s2_plan_r9.png at 100 percent and 2x and 4x crops in the spawn scratch folder. Scale 1.39 px/mm in original pixels (MEASURED).

# M1 visual gate, S2 r11 (s2_plan_r11.png)

Checks file wip/s2_checks_r11.json: 18/18 pass (MEASURED, timestamp 2026-11-27T20:37:42). Control figures: see s4_visual_gate_r2.md section 1.

## 1. Rubric (S2: V2, V6 to V10)

| Item | Result | What I see |
|---|---|---|
| V1, V3, V4, V5 | N/A | |
| V2 | PASS | Drill tube, keep-out, cutter rim, gear and ring OD concentric on the datum B cross; three pinion axes radial at 90, 210, 330. |
| V6 | PASS | Plan view: round parts as circles, profiles as squares. |
| V7 | PASS | Ring gear with teeth ticks (dashed, face down), pinions with mounts and NEMA 23 bodies, screws with nuts on r 160, frame members cross-hatched, guide lugs and rods, Step 2 rod ties in phantom brown. |
| V8 | PASS | Labels legible and non-overlapping; values on every label; no leader along a gridline, reference line or part edge. N1, N2. |
| V9 | PASS | Section 3. |
| V10 | PASS | Load and collet-change sector theta 90 +- 45 drawn as the orange wedge, open between screws a and b, with pinion c and its NEMA 23 at 90 inside it as the operator-task row states; F6 sightline drawn. |

Handedness: +X right along slot line C, +Y up, theta arc counter-clockwise from +X. PASS.

## 2. Change against accepted r9

Geometry is unchanged. Leaders and labels are re-routed: F6 sightline, load sector, slot line C, screw pitch, rod top tie and descent stop go from horizontal to oblique. The label stack re-orders (cutter OD now above base plate, gear PD below it). The r9 horizontal leaders at y 470 (descent stop) and y 515 (screw pitch) that ran across guide lugs and the rod tie box are gone. The change reads correctly.

## 3. V9

From the figure: everything sits inside the 644 base plate and the r 274 frame. The drill, keep-out, cutter, gear and ring are concentric on datum B. The operator has the theta 90 +- 45 sector between screws a and b, with only pinion c and its NEMA 23 overhead at 90, for loading and collet changes.

Spec question: "Does it fit, stay coaxial, and leave the operator a side to load the core and change collets?" Answered.

## 4. Findings

None.

## 5. Notes

- N1: the "screw pitch r 160" leader now runs up-right across the guide lug and through the cross-hatched frame member b, passing about 6 px (4 mm) below the start of the "screw frame 30-6060 r 274" leader at the member's corner (MEASURED). It is legible over the hatch. A route below member b would clear both.
- N2: the "gear PD 250", "tube OD 152.4" and "keep-out r 86.2" leaders cross the teeth band nearly parallel, 5 to 6 px apart (MEASURED). They do not touch.
- N3: the S1 F1 leader end-gap fix (shrink 0, K4 end within 0.5 mm) reaches this sheet by class; its K4 dry run lists any S2 leader it fires on.

## 6. Verdict

S2 r11: PASS, 0 FAIL.

# Gameplan lines to change

none


Orchestrator: score the controls against the key (orchestrator only); 4/4 matched; round r2; key file outside the tree.
