# S1 r8 visual gate (M1, Step 1.3 (f))

Reviewer: The Designer, fresh image-capable spawn; did not produce the images. wip/s1_pose_{load,start,capture_end,park}_r8.png and docs/sketches/s1_pose_load_r7.png opened with Read as images; zooms in D:\Unleashed Robotics\_scratch\cutjig\p8\. key.json not opened.

## Corrections to the brief

1. Harness record wip/s1_checks_r8.json: 19/19 pass incl. RPT (MEASURED by the harness).
2. r8 load PNG 1777 x 1328 px against r7 1546 x 1328 (MEASURED); the width grows with the longer figure note.

## 1. Controls

Scored before this sketch; see wip/s3_visual_gate_r1.md section 1: ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS handedness, ctrl_d FAIL handedness.

## 2. Rubric V1 to V10

| Item | Verdict | What I see |
|---|---|---|
| V1 | PASS | Floor at z_S 0 at the bottom of all four poses; NEMA 17s hang below the anchors (grey, about z_S 245 to 295); nuts (brass) on the ring. |
| V2 | PASS | Drill axis vertical at x 0; gear section symmetric; pinion axes horizontal (radial) at the NEMA 23s. |
| V3 | PASS | Head at the bottom of the drill (tip labelled per pose), top-end block (dark) at the top. |
| V4 | PASS | 0.75 m core upright in the collet, bottom on the stop at load, start, capture_end; absent at park. |
| V5 | PASS | Screws vertical, anchors at z_S 325, top guides at z_S 1225, nuts on the ring. |
| V6 | PASS | Rectangles and polygons only; no circles. |
| V7 | PASS | Tr12x3 screws with thread ticks, nut, 42-wide anchor block with bearing diagonals, top guide; ring with gear, pinions, NEMA 23s; motor as body. |
| V8 | PASS | Labels legible, no overlap, leaders clear; every label carries its value. |
| V9 | PASS | From the figure: the jig fits under the 2000 soft target (top-end block top about 1970 at load and park); the ring sits 130 above the tip; anchors at z_S 325 and guides at 1225; park 959.84 z_A (1019.84 z_S) and stroke 775; the axial loop runs ring nut, screw, anchor and guide blocks, arms, frame 30-6060, base plate, base frame, floor. Spec question: "Is the jig tall enough, where along the drill does the ring sit, where are the screw anchors and top guides, what are the park rule and the lift stroke, and which frame and base members carry the axial loop?" Match. |
| V10 | PASS | Load pose: collet and wing nut (sweep r 115) under the parked ring at 1150 to 1162 z_S; core path clear; unchanged from r7. |

## 3. S1 rubric additions

| Item | Verdict | What I see |
|---|---|---|
| Ring assembly on the tube between head and top-end block in every pose | PASS | All four poses. |
| Motors same side of the gear, outboard of the pinions, below the gear back face | PASS | NEMA 23s outboard of the gear section in every pose. |
| 0.75 m core solid at load, start, capture_end; absent at park; no 0.5 m core | PASS | As stated. |
| Head at the bottom, top-end block at the top | PASS | As V3. |

## 4. Changes against r7

1. Screw label "T8 screw L 900" to "Tr12x3 screw L 900"; thread ticks at the finer pitch. Reads.
2. Anchor block widened to the 42 square with bearing diagonals (two-bearing fixed anchor, Design Notes 31); NEMA 17 body redrawn below it as a square. Reads.
3. Receiver shoulder D200 x 8 drawn on the plate top (outer edge at x about +-100, MEASURED at zoom) beside the receiver body (Design Notes 32). Reads as a seat on the plate.
4. Axial-loop note "T8" to "Tr12x3"; figure note adds "receiver shoulder bolts 4 x M5 (layout open)". Reads.

## 5. Findings

Overall S1 r8: **PASS**. FAIL count 0.

N1 (NOTE, park title). The park title reads "held by the Step 2 hold device"; Design Notes 31 makes the self-locking lead the power-off hold, with brake or park pin still open for Step 2. Accurate as an open pick; aligning it to "held by the self-locking lead (Design Notes 31; Step 2 hold device open)" would match the S3 callout. Text only; opens no revision on its own.

## Gameplan lines to change

none
