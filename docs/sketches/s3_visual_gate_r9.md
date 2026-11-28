# Corrections to the brief

None. Measurement basis: pixels from s3_jackscrew_section_r9.png and accepted s3_jackscrew_section_r7.png at 100 percent and 2x crops in the spawn scratch folder. Scale 2.45 px/mm in original pixels (MEASURED).

# M1 visual gate, S3 r9 (s3_jackscrew_section_r9.png)

Checks file wip/s3_checks_r9.json: 16/16 pass (MEASURED, timestamp 2026-11-27T20:37:03); S3-3 48 links closed (MEASURED in the checks file). Control figures: see s4_visual_gate_r2.md section 1.

## 1. Rubric (S3: V1, V5 to V10)

| Item | Result | What I see |
|---|---|---|
| V1 | PASS | Floor at z_S 0 at the bottom; NEMA 17 hangs below the anchor; base stack on the plate. |
| V2, V3, V4 | N/A | |
| V5 | PASS | Screw c vertical; fixed anchor (bearing pair, block 42) at the bottom, about 325 to 355 z_S; radial-only top guide at 1210; nut (gold) on the ring at 380 to 395. |
| V6 | PASS | Section rectangles and true profiles; circles only in the end-view inset. |
| V7 | PASS | Jack screw with root line, nut, anchor and guide; ring as cut structure with bearing; gear section and pinion; motors as bodies. The base stack now carries the S4 true sections and hatches, the -X wing hidden box and sweep lines. Member c reads as a frame member in its own star hatch. |
| V8 | FAIL | F1, F2 below. |
| V9 | PASS | Section 3. |
| V10 | PASS | No operator-task row is assigned to S3; nothing in the figure contradicts the S1/S2 rows. |

Inset handedness: +X right, +Y up, theta counter-clockwise; A-A arrows point toward -X (viewer at +X). PASS.

## 2. Change against accepted r7

- Base stack: r7 stand-in rectangles and a dashed wing box become the true sections with per-material hatches (receiver ||, collet oo, wing nut ..), sweep lines at u +-115 and the labelled -X wing. It reads correctly and matches S4 r2.
- Member c hatch changes from xx to a star pattern, distinct from the base-frame rail (xx) it stands on. It reads.
- Leaders: the right-hand label column re-spaced, and most leaders turned oblique. The four nut/anchor labels (compression, floating nut, T per screw, fixed anchor) now fan from the screw at the left across the drill to the right column. Before r9 their leaders were horizontal. F1 and F2 come from this change.

## 3. V9

From the figure: screw c is held by a fixed back-to-back angular-contact anchor at the bottom, driven from the NEMA 17 below it, and guided radially only at the top. The 1000 N cut load reaches the ring nut and puts the screw in tension (T per screw 247.5). Three screws are synced by one controller with home switches and no belt. The self-locking Tr12x3 lead holds the ring with power off. The axial loop closes through the listed parts.

Spec question: "How is each screw anchored, guided, driven and synced, does the 1000 N axial load put it in tension, what holds the ring with power off, and does the axial load loop close?" Answered.

## 4. Findings

**F1 (V8; labels compression per screw, floating nut, T per screw, fixed anchor).** The four fan leaders pass under filled artists. Each one enters the pinion (cross-hatch, white fill) and the NEMA 23 body (grey fill) or the motor mount (// hatch, white fill) on the right side of the drill. They vanish there and reappear at the right edge of the motor: two leaders disappear between u about 95 and 215, and the lowest one under the mount (MEASURED). This is the leader-under-fill class of S2 r2 F1 and S1 r6 F1. K4 "no two leaders cross" passes, and nothing in K4 tests occlusion.

**F2 (V8; label S3-2 span, K 0.7; L_t 870).** The leader runs horizontally through the top-end block, 9 mm below and parallel to its top face, across its full width u -76.2 to +76.2 (MEASURED 22 px at 2.45 px/mm). It reads as an edge inside the block. In r7 the same label's leader ran above the block. This is the leader-along-part-edge class of S3 r6 F1, F2, which rule (l) with the part-edge extension covers; its distance band did not catch 9 mm.

Fix for both: route the four fan leaders above the gear (z_S above 500) or move their labels to the left margin beside the screw, and route the S3-2 leader above the block top (z_S above 1195). Rule (h): K4 adds (i) a leader segment under a filled artist with a higher zorder fails; (ii) the rule (l) part-edge band widens to the leader running inside a part within 5 deg of one of its edges, at any distance (the S4 F1 (iii) rule, one rule for both). Premise: every view. Each needs its Z, and its B red on r9 (F1 on "compression per screw", F2 on "S3-2 span").

Dry run the Engineer must run before r10 opens: apply the routes and the K4 additions in a dry-run tree under the spawn scratch folder; then run check_sketch.py s3 --rev 10 --only K4, then the full s3 --rev 10 set, then --stale. Run K4 on s1 --rev 10, s2 --rev 11 and s4 --rev 2 for class scope.

Class history: both F1 and F2 are second findings of classes already found (S2 r2 F1, S1 r6 F1; S3 r6 F1, F2). Per A.4 they go to the orchestrator for a ruling before r10 opens.

## 5. Notes

- N1: the "nut at start z_S 1030.84" leader crosses the top-end block bottom edge at about 7.6 deg (MEASURED), then runs through the block. It is a crossing, at a shallow angle.
- N2: "member c on the rail top" still runs horizontally across the screw, tube and core at z_S 670, unchanged from r7.

## 6. Verdict

S3 r9: FAIL, 2 findings (F1, F2; V8).

# Gameplan lines to change

none


Orchestrator: score the controls against the key (orchestrator only); 4/4 matched; round r2; key file outside the tree.
