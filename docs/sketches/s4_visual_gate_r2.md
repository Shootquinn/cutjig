# Corrections to the brief

None. The pixels match the brief and s4_spec.yaml on every item read. One spec-level note: drill.head_length and drill.kerf_standoff are both 106.369 (DECLARED, overlay, ASSUMED), so line_kerf (z_S 351.21, DERIVED) lies on the drill head top edge across u -88.9 to +88.9 and shows only outboard of the head (N2).

Measurement basis: pixels read from the PNGs at 100 percent and from crops in the spawn scratch folder. Figure 1 scale 8.09 px/mm (MEASURED, original pixels); figure 2 8.06 px/mm (MEASURED). Position readings carry +-0.3 mm (MEASURED).

# M1 visual gate, S4 r2 (s4_base_section_r2.png, s4_liner_section_r2.png)

Checks file wip/s4_checks_r2.json: 14/14 pass (MEASURED, timestamp 2026-11-27T20:37:11).

## 1. Reviewer-model controls (docs/sketches/wip/m1/r2/)

| File | Kind | Verdict | What I see |
|---|---|---|---|
| m1c_8c10b6.png | plan | FAIL (handedness) | +X arrow right, +Y arrow points down; the theta arc runs from +X clockwise on screen to the +Y arrow; screw c labelled 270 sits at +y 160 and screws a 30 / b 150 sit at y -80. Mirrored plan. |
| m1c_435ac2.png | drill side | PASS (V1 to V5) | Floor line at z 0 at the bottom; drill axis vertical; cutter block (OD 177.8) at the bottom 245 to 350, top-end block at 1045 to 1195; core upright, bottom at 100 on the stop; screw vertical with a block at the bottom (325 to 395) and at the top (1195 to 1225). |
| m1c_3d83ee.png | plan | PASS (handedness) | +X right, +Y up, theta arc counter-clockwise from +X to +Y; screw a 30 deg at upper right, b 150 upper left, c 270 at -y 160. |
| m1c_b3697f.png | drill side | FAIL (V3) | The cutter block (OD 177.8 label) is at the top, 1090 to 1195, with the tube hanging below it to 245: head at the tail end, inverted. V1, V2, V4, V5 otherwise read as in 435ac2. |

## 2. Rubric, S4 (both figures unless named)

| Item | Result | What I see |
|---|---|---|
| V1 | PASS | Shop floor line at z_S 0 at the bottom of both figures; base plate at 60 to 72 z_S, stack above it. |
| V2 | N/A | |
| V3 | PASS | Collet foot ring on the receiver floor top (z_S 100), outer cone narrows upward; holder inner cone narrows upward on it; wing nut above the PTFE washer above the holder flange; collar on top at 219.84. |
| V4 | PASS | Carrier stands on the core-seat ledge (102.5 z_S) through the collet bore; 100 mm core on the carrier top (262.5), chamfer mark 3 below the core top (dashed, inside the drill head); never inverted. |
| V5 | N/A | |
| V6 | PASS | Every round part is a rectangle or true half-profile; no circles. |
| V7 | PASS | Collet with foot ring, cone, bore, chamfer and two slit ticks; holder with inner cone, tube and flange; wing nut with body, dust skirt, nut plate and the hidden -X wing (dashed box at u +-7, z_S 173 to 213, labelled); receiver with floor, debris hole, stepped wall, register chamfer, shoulder on the plate and two root lines; washer as a 1.3 band; carrier with bond line; liner as one sleeve (figure 2). |
| V8 | FAIL | F1 below. Labels legible and non-overlapping; every label carries its value. Leaders cross the section through cut parts, one passes through a part corner. |
| V9 | PASS | Section 3. |
| V10 | PASS | Section 2c. |

### 2a. S4 rubric additions

| Addition | Result | What I see |
|---|---|---|
| V3 collet foot / cone / holder cone | PASS | As V3. |
| V3 wing nut above washer on flange | PASS | Left side: flange top, washer band, nut-plate underside in that order upward; right side the theta 90 window splits the nut plate from the body (plane_cuts, named in the note). |
| V4 carrier on stop, core on carrier, chamfer, above min-exposure | PASS | Core top 362.5 z_S against the min-core line 356.2 z_S: 6.3 above (MEASURED; DECLARED expected 6.29). |
| V7 fig 2 liner sleeve, bottoms on ledge | PASS | Liner (-- hatch) runs from the ledge to the core top as one sleeve, dashed inside the head; carrier bottom and liner bottom both end on the d 105 ledge top. |
| V7 slit ticks, receiver root lines | PASS | u > 0 tick open at the collet top, 25 long, relief mark at its lower end; u < 0 tick open at the foot, relief mark at its upper end; two root lines inside the receiver thread zone. N3 on the tick line style. |
| V10 operator rows | PASS | Section 2c. |
| Section handedness | PASS | Title states x = 0, seen from +X, u = +Y; the u > 0 tick is the top-open one (theta 112), the u < 0 tick bottom-open (theta 262). |

### 2b. Section convention, options, alternates, ticks

- Cut parts hatched by material: aluminium // (plate, holder, collar), receiver and spigot ||, collet oo, wing nut and washer .., liner --. Reads.
- Beyond in elevation: -X wing dashed box, sweep r 115 dashed lines at u +-115. Reads.
- Hidden dashed: core and carrier edges inside the unsectioned drill head and tube. Reads.
- Advance option D: stop line (244.84), kerf line (351.21) and min-core line (356.21) drawn; the note states that the lift lowers the drill one slice per cut and the carrier and core stay on the stop. The advance reads from the note and the three lines; no second drill position is drawn, as the spec asks.
- Alternates: liner figure drawn as figure 2; rejected options (push rod, pucks, liner push-pop, taller collet) named in the note. Reads.
- Ticks: as the V7 addition.

### 2c. V10

Wing-nut wings and sweep r 115 lie outside the holder flange with clear space to u +-130; the stack lowers over the collar top 219.84 with the 4.5 radial gap at the collar ID visible between carrier and collar. The load pose itself is in S1; this figure shows the stop pose.

## 3. V9

From the figure: the 100 mm core stands on a 160 mm nylon carrier that stands on the collet core-seat ledge and is gripped by the d 100 collet over its straight bore (or, figure 2, sits in a cast-on liner gripped by the d 105 collet); the core top stands 6.3 above the minimum-exposure line with the drill at its stop, and the note says each slice is taken by lowering the drill one slice while the core stays put.

Spec question: "How is a core advanced through the kept base for each slice, and does the kept collet family cover a 100 mm tall core with the core gripped and exposed above the nut plate?" The figure answers both parts; the advance part rests on the figure note.

## 4. Findings

**F1 (V8; features base_plate / receiver_spigot labels, collet and collet_105 labels, collet:slits label, line core stop label).** Four leaders run through cut parts in a way that reads as drawing lines:

- (a) "spigot OD 160", both figures: the leader runs horizontally inside the base plate from u 80.2 to 130 at z_S 67 to 68 (MEASURED), parallel to the plate faces, after crossing the spigot. Inside the plate it reads as a step line in the plate.
- (b) "collet d 100" (figure 1) and "collet d 105" (figure 2): one horizontal leader at the collet top level z_S 132.2 (MEASURED) runs from the u < 0 collet apex (figure 1: from the left margin through receiver, holder and that apex) across the carrier and core to the u > 0 apex. Figure 1 puts it 2.2 mm above the 130 minor gridline (MEASURED). It reads as a reference level, and its anchor is ambiguous.
- (c) "12 slits, alternating, 25 long", both figures: a horizontal leader at z_S 112 (MEASURED) runs from the u < 0 tick across the carrier, through the u > 0 tick, holder and receiver wall.
- (d) "core stop z_S 102.5" (figure 1): the diagonal leader passes through the bottom inner corner of the u > 0 spigot (u 40.0, z_S 60.0 DECLARED; leader within 0.2 mm of it, MEASURED).

Fix: route each leader from the u > 0 instance of its part, on the label side. Run each leader oblique, at least 15 deg from horizontal and vertical, so that it does not cross u = 0, does not lie within 1 mm of a part vertex, and does not run inside a part parallel to that part's faces. A leader that ends inside a cut area ends on a dot. Rule (h): add to K4 (i) a leader crosses u = 0 in a section view, (ii) a leader passes within 0.5 mm of a drawn vertex other than its own end, (iii) a leader segment lies inside a drawn part and runs within 5 deg of one of that part's edges. Premise: section and side figures. Scope: every view the harness draws (S1 side, S2 plan, S3 section and inset, S4 section). Each rule needs its Z, and its B shown red on r2 (B for (i) on figure 1 "collet d 100", for (ii) on "core stop", for (iii) on "spigot OD 160").

Dry run the Engineer must run before r3 opens: apply the routes and the K4 additions in a dry-run tree under the spawn scratch folder; then run check_sketch.py s4 --rev 3 --only K4, then the full s4 --rev 3 set, then --stale. Report K4 Z and B counts and the three new B controls red on r2. The same K4 run on s1 --rev 10, s2 --rev 11 and s3 --rev 9 lists which accepted or gated figures the new rules fire on (scope by class).

Class history: leaders that run along or through part features were found at S3 r6 (F1, F2). This is a second finding of that class, and per A.4 it goes to the orchestrator for a ruling before r3 opens.

## 5. Notes

- N1: "min exposed 143.12" sits at the left end of its own dashed line, and its leader is collinear with the line (1 mm gap). It reads as the line's label. Leave it as it is or drop the leader.
- N2: line_kerf coincides with the drill-head top edge over u +-88.9 (head length = kerf standoff, both 106.369 ASSUMED). The kerf line is visible only outboard of the head.
- N3: at 100 percent the slit ticks read as fine solid lines. The legend says "dashed", and the dash pattern does not resolve at this scale.
- N4: the PTFE washer leader crosses the carrier and the holder neck diagonally to reach a 1.3 band; it reads, but it is the longest leader on the sheet.

## 6. Verdict

S4 r2: FAIL, 1 finding (F1, V8). Every other applicable item passes in both figures.

# Gameplan lines to change

none


Orchestrator: score the controls against the key (orchestrator only); 4/4 matched; round r2; key file outside the tree.
