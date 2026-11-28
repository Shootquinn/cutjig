# Corrections to the brief

None. Measurement basis: pixels from the four r10 PNGs and accepted s1_pose_load_r8.png at 100 percent and from 4x and 6x crops in the spawn scratch folder. Scale 0.525 px/mm (MEASURED). Leader-end readings carry +-1 px, +-2 mm (MEASURED).

# M1 visual gate, S1 r10 (load, start, capture_end, park)

Checks file wip/s1_checks_r10.json: 19/19 pass (MEASURED, timestamp 2026-11-27T20:37:03); S1-5b least 142.00 (MEASURED in the checks file). Control figures: see s4_visual_gate_r2.md section 1 (8c10b6 FAIL, 435ac2 PASS, 3d83ee PASS, b3697f FAIL).

## 1. Rubric

| Item | Result | What I see |
|---|---|---|
| V1 | PASS | Shop floor z_S 0 at the bottom of every pose; lift motors hang below the anchors; NEMA 23s at gear level beside the gear. |
| V2 | PASS | Drill axis vertical at x 0; gear section symmetric about it; pinion axes radial. |
| V3 | PASS | Cutter head at the bottom of the drill and top-end block (grey fill) at the top in all four poses; gear and ring above the head, between head and block. |
| V4 | PASS | 0.75 m core upright: mid-insertion at load (bottom about 161 z_S), on the core stop at start and capture_end, absent at park. |
| V5 | PASS | Screws vertical; anchors at z_S 325 at the bottom, top guides at z_S 1225 at the top; nut (gold) on the ring. |
| V6 | PASS | Rectangles and true half-profiles only. |
| V7 | PASS | Ring gear with teeth hatch and pinions; jack screws with nut, anchor and guide; frame members as structure; motors as body and shaft. The base stack now carries true profiles: holder, collar, collet, receiver, and the wing nut with in-plane wings to about r 115 (MEASURED at 4x). |
| V8 | FAIL | F1 below. |
| V9 | PASS | Section 3. |
| V10 | PASS | At load the core top (about 911 z_S) is below the tip (1019.84) and the hand band 0.5 to 1.0 m is clear between the frame members; the collet-change zone at z_S 157 to 213 is open from the side. Ring and head overhead as the operator-task row states. |

### Rubric additions

| Addition | Result | What I see |
|---|---|---|
| Ring on the tube between head and top-end block, every pose | PASS | In every pose. |
| Motors on the same side, outboard of the pinions, below the gear back face | PASS | Grey NEMA 23 bodies outboard of the gear on both sides in every pose. |
| 0.75 m core solid at load, start, capture_end; absent at park; no 0.5 m core | PASS | As V4; one core only. |
| Drill head at the bottom, top-end block at the top | PASS | As V3. |

## 2. Change against accepted r8 (load pose compared pixel for pixel by eye)

- Base stack: r8 drew stand-in rectangles with hatch and a dashed sweep box. r10 draws the true profiles (holder tube and flange, collar, collet cone, receiver step, wing-nut body, skirt and in-plane wing boxes). The brief's footprint row "S1 r9 wingnut drawn +-95.14" is closed: the wings now reach the sweep radius. It reads correctly, at a scale where the stack is detail. S4 is the reading figure for it.
- Leaders: tube OD, TOP-END BLOCK, bore ceiling, core 750, screw frame and soft target leaders go from horizontal (r8) to oblique, and the labels re-space. "core 750" no longer runs along the 500 to 750 band horizontally.
- Unchanged: geometry above the base stack, pose heights, labels' text.

## 3. V9

From the figures: the jig's highest point is the top-end block at about 1965 z_S at load and park, under the 2000 soft target. The ring sits 130 above the tip. Screw anchors are at z_S 325 and top guides at z_S 1225. Park is tip 1019.84 by the stated park rule, with a lift stroke of 775. The axial loop runs ring nut, screw, anchor and guide blocks, bracket arms, 30-6060 frame, base plate, base frame, floor.

Spec question: "Is the jig tall enough, where along the drill does the ring sit, where are the screw anchors and top guides, what are the park rule and the lift stroke, and which frame and base members carry the axial loop?" Answered in full.

## 4. Findings

**F1 (V8; features drill_tube, drill_top_block, keepout labels; all four poses).** The leaders aimed at the drill stop about 4 px short of their part. The keep-out line lies 10 mm (5 px) outside the tube, so the stop lands on the keep-out line:

- "tube OD 152.4 (keep-out basis)": the leader ends at r about 85 (MEASURED), on the keep-out line at r 86.2 (DECLARED) and 9 mm off the tube wall at r 76.2 (DECLARED). Load r10 end x 817 px, tube wall 813, keep-out line 819.5 (MEASURED). Start and capture_end read the same way.
- "TOP-END BLOCK (tail) 150": the leader ends at x 817 px, on the keep-out line, 4 px off the block edge at 813 (MEASURED, load).
- capture_end: the "tube OD" and "keep-out r 86.2" leaders end 6 px apart in the same 10 mm band, the keep-out leader 3.5 px outside its line in empty space (MEASURED). Neither label names its own line at 100 percent.
- Accepted r8 load shows the same tube OD end point (x 817, MEASURED). The gate fails what it sees (S1 r6 F1 precedent: a fault present in an accepted revision fails the current one).

The cause read from the pixels is a uniform end gap of about 2 pt on every leader. That matches the matplotlib annotate default shrink, which K4's "ends on its part" tolerance absorbs. Fix: set the leader end gap to 0 (shrinkA and shrinkB 0 on every leader) in the shared label helper that S1 to S4 use. Rule (h): K4 tightens "leader ends on its part" to within 0.5 mm of the part's drawn edge, and adds "no other row's drawn line within 1.0 mm of the end point". Premise: side, plan and section figures. Z on the dry-run S1 r11 load figure (gap 0); B on S1 r10 load ("tube OD" ends 9 mm off the tube and 1 mm off the keep-out line). Scope by class: every leader in S1, S2, S3, S4.

Dry run the Engineer must run before r11 opens: apply the end-gap setting and the K4 change in a dry-run tree under the spawn scratch folder. Run check_sketch.py s1 --rev 11 --only K4, then the full s1 --rev 11 set. Run K4 on s2 --rev 11, s3 --rev 9 and s4 --rev 2 to show the class scope, then --stale. Report the B red on r10 and every figure the new K4 fires on. K1 note: shrink 0 is a literal from the allowed set [-1, 0, 0.5, 1, 2].

## 5. Notes

- N1: "Tr12x3 screw L 900" still runs horizontally across the core, the right screw and the frame members at z_S 745, 5 mm under the 750 gridline (MEASURED). It is unchanged from accepted r8.
- N2: the floor shape text says "ground hatch below"; no ground hatch is drawn in r8 or r10.

## 6. Verdict

S1 r10: FAIL, 1 finding (F1, V8). Every other applicable item passes in all four poses.

# Gameplan lines to change

none


Orchestrator: score the controls against the key (orchestrator only); 4/4 matched; round r2; key file outside the tree.
