## 1. Per-part results (from parts_cache/{part}_result.json)

All five: isValid True, isClosed True, 1 solid, 1 shell; genus not computable (annular, periodic faces). Frames: receiver floor z 0; others bottom z 0.

| Part | Volume mm3 | Bbox (mm) | Centre of mass | Features pass | Build s |
|---|---|---|---|---|---|
| receiver | 955903.5 | 160 x 160, z -40 to 88.5 | -0.18, -0.17, 0.62 | 25/25 | 164.8 |
| holder | 407847.2 | 144.08 dia, z 0 to 104.75 | 0.18, 0.16, 56.87 | 21/21 | 0.4 |
| nut | 322244.1 | 230 x 166.28, z 0 to 56 | 0.10, -0.19, 30.53 | 41/41 | 145.1 |
| washer | 1814.2 | 143.2 dia, z 0 to 1.3 | -0.48, -0.36, 0.65 | 7/7 | 0.3 |
| footring (d 90) | 17034.9 | 133.98 dia, z 0 to 2.5 | 0.24, 0.18, 1.03 | 10/10 | 0.3 |

Each part is a PartDesign::Body: Revolution base, native SubtractiveHelix threads, one combined Boolean Fuse and one Cut.

## 2. Processes and logs

| Part | PID | Start | Done | Log |
|---|---|---|---|---|
| receiver | 35064 | 20:21:48 | about 20:24:33 | cr_scratch\step3_build_receiver.log |
| holder | 9224 | 20:21:48 | 20:21:48 | cr_scratch\step3_build_holder.log |
| nut | 27200 | 20:25:00 | about 20:27:25 | cr_scratch\step3_build_nut.log |
| washer (fg) | 31780 | 20:28:31 | 0.3 s | foreground |
| footring (fg) | 21568 | 20:28:31 | 0.3 s | foreground |

Log line 1 is `START {part} pid=.. t=..`; last line `BUILD_DONE {part}`; checked by sentinel and fresh JSON. Nut run 1 (PID 35640) failed two predicates (tab width, window count); fixed, rerun. Receiver and nut: 2.5 to 3 min, inside 2 to 10. All five inside 15 minutes. Most time is Rule M measurement.

## 3. Signed numbers, built against params (tolerance 0.05 mm)

All keys in the crossreview final table that are built read within 0.05 mm, except where listed in section 4. Cross-part (parts_cache/step3_cross_checks.json, 24 of 24 pass):
- `register.g_reg` 0.250 (bore r 67.29 less holder r 67.04). Ring clearance 0.300.
- Stacked pair at K-max: ring top 1.995, holder bottom 2.000, gap 0.005; holder bottom above floor 2.000; flange underside to rim 1.500. Overlap receiver/holder/ring 0.00 mm3.
- Key tip to slot floor 0.55 (holder and foot key). Holder to receiver minimum distance 0.125 (key tangential), not the register.
- Holder length 88.0; plate top to flange underside 16.0; holder top to plate top 0.75; nut crest bore to flange 0.60; plate hole to holder OD 1.00.
- Pads: nut/washer common volume 2.4017 mm3 (signed 2.402). Tab gaps 0.50 tangential, 1.00 radial.
- Thread mesh (nut at z 52.5): overlap 0, minimum distance 0.1061 (g_a/2 x sin 45). Right hand confirmed on both threads.
- T9: built tilt 0.6091 + rock 0.3158 = 0.9248 against 0.924 (rock lever `nut.plate_hole_dia`, not 136.44).

## 4. Deviations and unbuilt features

- Collet slits, relief holes, strain ratio, bore lead-in chamfer: not built (collet generator; a slit-cut ring is six solids).
- Ring bottom to floor gap is 0.000 (class C seat); only ring top to holder carries `fit.model_contact_gap`. Crossreview S3 says 0.005 modelled at the floor.
- Holder inner cone top r 56.7502 (exact tan 10), signed 56.75; bore 113.5004.
- Release arrow span 33.25 deg against 33.75 (checked at 1.0 deg). Pad arc 9.983 against 10.0.
- Windows at 90, 210, 330 deg (180 hit the wing).
- Wing mark: 21.86 mm long, not `nut.arrow_length` 40 (arm is 31.86). Taper symmetric, 10.665 deg per edge.
- Nut thread ends where the groove top meets the plate underside (one-ended start).
- Assumed: receiver below z 0 is a solid spigot tube to datum A; tommy axis z = 56 - `nut.tommy_hole_depth`; holder notch at -37 deg; foot ring for d 90 only.
- Literals in scripts are probe offsets, embed margins, tolerances only.

## 5. Edits and tests

- ASSEMBLY.md line 7 replaced with the section 3 frame text. gameplan.md untouched.
- params.yaml: 12 keys added (leaves 307 to 319), report_assumptions.md regenerated: `thread.run_turns`, `thread.runout_land`, `thread.tool_groove_fraction`, `holder.insert_count`, `holder.insert_circle_radius`, `holder.insert_dia`, `holder.insert_depth`, `holder.index_notch_width`, `holder.index_notch_depth`, `nut.tommy_hole_bottom_r`, `nut.plate_hole_dia`, `nut.tab_inner_radius`.
- `python -m pytest tests/test_params_bom.py -q`: 197 passed.
- Files: build_parts\{receiver,holder,nut,washer,footring,cadlib,verify_step3}.py.

## 6. Registry rows for the Manager (gameplan.md, Echo Site Registry)

Lines 687 Thread (lead-in, crest flat, run turns, runout land); 689 Slits (ligament, length, relief hole, strain; geometry unbuilt); 690 Engagement (R full-form 24.72 against 24); 702 Washer (notch, pads class P); 704 Collar 152.4 / 110.0 / 6.75; new rows: T9 (`register.t9_tilt_deg`, 0.9248 built), holder inserts and index notch (six keys), nut plate hole and tab (two keys), first-solids status.
