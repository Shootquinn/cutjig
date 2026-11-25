# Question batch 1 to Quinn (cut jig sketch phase)

Date: 2026-11-24. Source: research/sean/gameplan.md detail 1.0 line 158 and Open Questions.

Sean approves and pushes this file. Quinn answers in the Answer column or in a reply file of his choosing. Until answered, the sketches use the value in the ASSUMED column.

Source tags: [CP §n, mm:ss] is context/2026-11-24_cutjig_critical_path.md; [DN23] is Design Note 23 of research/quinn/gameplan.md; a params key carries the status written in params.yaml.

| ID | Question | Feeds | Owner | Value used until answered (ASSUMED) | Answer | Date |
|---|---|---|---|---|---|---|
| Q2a | How long is the 6 in drill, cutter tip to top end, in mm? | S1 (all heights, 2000 mm margin), S3 (screw length) | Quinn | 800 mm, ASSUMED [CP §3.2, 18:20] | | |
| Q2b | What does the drill weigh, head and top end included, in kg? | S3 (screw load), S6 (pinion load) | Quinn | 8 kg, ASSUMED (no source; the 800 mm tube alone is 3.2 kg, DERIVED from drill.tube_od, drill.tube_id and aluminium 2700 kg/m3 ASSUMED [CP §12, 09:05]) | | |
| Q2c | What hardware sits on the top end of the drill: length, OD and mass? | S1 (drill top height), S3, S6 (ring position) | Quinn | Block 150 mm long, 152.4 mm OD, 2 kg, ASSUMED (no source; OD = drill.tube_od) | | |
| Q2d | What are the OD and length of the cutter and iris head? | S1 (S1-5 clearances), S2 (keep-out circle), S6 | Quinn | OD 177.8 mm, ASSUMED (params drill.cutter_od_7in, 7 in generation, upper bound; labelled "cutter OD ASSUMED"); length 106.369 mm, ASSUMED (params drill.kerf_standoff) | | |
| Q2e | How far above the cutter tip is the lowest part that closes the drill bore? | S1-5a (500 mm core top against the bore ceiling, gap 25 mm) | Quinn | 800 mm above the cutter tip (open bore to the tube top), ASSUMED; DERIVED from Q2a | | |
| Q9 | Which core lengths must the jig load and capture: 500, 750, 1000 mm? | S1 (lift stroke, park height), S3 (screw length) | Quinn | 500 and 750 mm; 1000 mm not drawn, ASSUMED (core.length_capture, core.length_install DECLARED; gameplan Open Questions Q9) | | |
| DN23-a | Input requested: how many NEMA 17 steppers does the lift need, one per screw or fewer with a belt? | S3, Step 2 lift row | Sean | 3, one per jack screw, ASSUMED [DN23] | | |
| DN23-b | What gearbox ratio, if any, do the NEMA 23 pinion motors need? | S6 (gear ratio, torque), Step 2 | Quinn and Sean | 1:1, direct drive, ASSUMED [DN23] | | |
| DN23-c | What drill speed in rpm and drill torque in N m should the drive deliver? | S6 (pinion forces), S6-3 torque loop | Quinn | 60 rpm, ASSUMED (no source); 10 N m, ASSUMED (cap at loads.torque_design DECLARED, the core holding torque) | | |
| DN23-d | Input requested: what ring gear size and source do you suggest? | S1 (ring outline), S2 (pinion layout), S6 | Sean | Bought bevel ring gear, pitch diameter 250 mm (no source), bore 180 mm, ASSUMED (bore above 2 x icd.keepout_radius = 172.4 mm, DERIVED) | | |
| DN23-e | How does the iris drive sit with three pinions (INSITU2 157-166, excerpted at context/literature/INSITU2_text.md line 7, via Quinn DN23)? | S6 callout | Quinn | The iris runs off the same ring gear drivetrain; S6 draws a callout, no separate iris drive, ASSUMED [DN23] | | |
| N5 | Under the screw lift the cut reaction runs through the kept base parts (collet, holder, receiver, base plate). Accept, or name the rating check? | S3-3 axial loop, Step 2, 4a (ASSEMBLY.md Load path, A2d) | Quinn | Accept at 1000 N (loads.wob_max VERIFIED) with no rating check; S3 reports the force in each part, ASSUMED [gameplan Design Notes 16] | | |
| N6 | How does the captured 500 mm core come out of the raised drill? | S1 (park pose), S6 | Quinn | Drill raised to park; core lowered out of the drill bottom by hand, upright, through the opened iris; no jig feature, ASSUMED (tied to DN23-e) | | |
| N7 | Input requested: is the gate B5 metal descent stop kept under the screw lift? | S1 (lowest pose), S3, Step 2 rows | Sean | Kept, rated 1000 N axial (upper.metal_stop DECLARED); power-off hold is a separate Step 2 device, ASSUMED | | |
| N8 | May ASSEMBLY.md become the ICD authority for the redesigned rows, replacing research/quinn/cr_scratch/step2_system_concept.md? | 4a, 4c (ASSEMBLY.md edits) | Quinn | Yes, ASSEMBLY.md (or a shared ICD file under docs/); no ASSEMBLY.md ICD or load-path edit until Quinn rules, ASSUMED [gameplan detail 4a] | | |
| N9 | May test_P10_every_key_in_concept_icd_table_exists be rewritten to read the N8 ICD source in place of your cr_scratch file? | 4a, 4c (tests) | Quinn | REWRITE to read the N8 source, ASSUMED [gameplan detail 4a] | | |
| N10 | Does the base frame stand directly on the shop floor (datum A = profile.height 60 mm above the floor), or on feet or foot plates? The sketches plot heights from the shop floor. | S1 (all heights, 2000 mm margin), K6 | Quinn; Sean approves or strikes this row | 60 mm, ASSUMED; DERIVED from params profile.height (VERIFIED), no feet | | |
