# S1 r7 M1 visual gate (Designer, step 1.2 (f), P8r)

Figures: `docs/sketches/wip/s1_pose_{load,start,capture_end,park}_r7.png`, read at 100 percent with 3x crops of the ring assembly (load, capture_end), the collet and base (load) and the leader ends (capture_end, park). Pixel scale 0.525 px/mm (MEASURED, capture_end). Inputs: `s1_spec.yaml` (question, rubric_additions), `wip/s1_summary_r7.md`, gameplan l.176-203. Reviewer-model controls: see `s2_visual_gate_r3.md` section 1 (same reviewer, same gate).

## Corrections to the brief

None.

## 1 Rubric (S1: V1 to V10)

| Item | Verdict | What I see |
|---|---|---|
| V1 | PASS | Shop floor z_S 0 (blue) at the bottom of all four poses, base frame sections (hatched X squares) under the hatched plate. Lift motors (grey) hang under the anchor blocks at about 260 to 300 z_S; NEMA 23 bodies sit beside the gear below its back face. |
| V2 | PASS | Drill axis vertical in every pose; gear section hatched and mirror-symmetric about x 0; pinion shafts horizontal (radial) into the NEMA 23 bodies on both sides. |
| V3 | PASS | HEAD (cutter, tip) at the bottom of the tube and the dark TOP-END BLOCK (tail) at the top in all four poses: load and park tip 1019.84 z_S, start 894.84, capture_end 244.84. |
| V4 | PASS | Core 750 upright: at load bottom about 160 z_S (mid-insertion above the collar), at start and capture_end bottom on the stop, absent at park. No 0.5 m core drawn. |
| V5 | PASS | T8 screws vertical, anchors at 325 z_S at the bottom, top guides at 1225 z_S at the top, the gold nut on the ring at each pose. |
| V6 | PASS | Every cylinder (tube, core, screws, rods, members) is a rectangle; no circles in the side views. |
| V7 | PASS | Gear: hatched bevel section with the toe toward the axis; pinions hatched beside it; NEMA 23 as grey body with a dark shaft bar to the pinion; screw with thread strip, nut, anchor and guide blocks on bracket arms to the 30-6060 frame; ring as plate with nut housing, mounts and lugs; collet, holder and wing nut sweep at the base. |
| V8 | PASS | Labels legible at 100 percent, right-hand column, none overlapping. At capture_end the "tube OD", "screw frame" and "keep-out" leaders run close but separate (3x crop); "core 750" now ends on the core edge just above the gear top, clear of the hatch (r6 F1 closed). At park the "keep-out" and "lift stroke 775" leaders end 6 px apart at the head's lower corner, distinct. Every label carries its value. |
| V9 | PASS | From the figures: the jig is tall enough (top-end block top 1969.84 z_S at load and park, 30.16 under the 2000 soft target); the ring sits 130 above the tip on the tube; anchors at 325 z_S, top guides at 1225 z_S; park = max(max_k start_k, entry_plane + max L) + upper.load_clearance = 959.84 z_A = 1019.84 z_S, lift stroke 775 (park 1019.84 to capture_end 244.84); the axial loop is ring nut, T8 screw, anchor and guide blocks, bracket arms, screw frame 30-6060, base plate, base frame, floor. Spec question: height, ring position along the drill, anchors and top guides, park rule and stroke, members in the axial loop. Every part is answered. |
| V10 | PASS (F6 carried) | Load: drill head bottom 1019.84 z_S, 19.84 above the hand band top (S2-5b, MEASURED), core passes over the collar into the holder; wing nut sweep r 115 at knee height clear of moving parts at load. Watch: at start the cutter is in view under the ring; at capture_end the ring, gear and NEMA 23s at about 375 to 500 z_S sit over the head at 244.84 to 351.21 and hide it from a standing eye. F6, accepted by Sean as assigned to Step 2 and S2 (Design Notes 24); S2 r3 draws the sightline. |

## 2 S1 rubric additions

| Addition | Verdict | What I see |
|---|---|---|
| Ring assembly on the tube between head and top-end block in every pose | PASS | Bearing, ring, gear above the head and well below the top-end block in all four poses. |
| Motors on the same side of the gear, outboard of the pinions, below the gear back face | PASS | NEMA 23 bodies outboard of the hatched pinions, both sides, below the gear top, every pose. |
| 0.75 m core solid at load, start, capture_end; absent at park; no 0.5 m core | PASS | As V4. |
| Drill head at the bottom, top-end block at the top | PASS | As V3. |

## 3 Visible change against r6

Pixel difference r6 to r7 (MEASURED): load, start and park identical (0 px). capture_end differs in 2663 px inside rows 873 to 924, columns 588 to 855: the "core 750" label and its leader moved from the gear hatch to the core edge above the gear (Engineer r3: anchor (50.00, 477.50) to (50.00, 540.00)). Nothing else changed in the drawing.

## 4 Verdict

**S1 r7: PASS.** Every item passes. FAIL count 0. F6 (hidden end of cut) stays with Step 2 and S2 as accepted.

## Gameplan lines to change

none
