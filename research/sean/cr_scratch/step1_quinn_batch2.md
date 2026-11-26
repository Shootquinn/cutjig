# Question batch 2 to Quinn (cut jig sketch phase, Step 1.3)

Date: 2026-11-26. Source: research/sean/cr_scratch/step1.3_designer_params_review.md; Sean sent it at STOP S3-A (gameplan Design Notes 31). Rows owned by Sean (B2-1 to B2-6) carry Sean's adopted working values; Quinn answers B2-7 to B2-9 (and may comment on any row) in the Answer column or a reply file. Until answered, the sketches use the ASSUMED value.

| ID | Question | Feeds | Owner | Value used until answered (ASSUMED) | Answer | Date |
|---|---|---|---|---|---|---|
| B2-1 | Which lead screw do you buy: thread (Tr12x3 or T8x8), root diameter, material, nut flange OD and length, machined ends? | S3-2, S1/S2 screw rows, Step 2 screw row | Sean | Tr12x3, root 8.5, steel E 200 GPa, flange 42, nut 30, ends 10 / 8 | | |
| B2-2 | Which NEMA 17 do you have (DN23-a): holding torque, body length, shaft, brake? | F_stall, WOB, lift motor rows | Sean | 0.45 N m, 48 long, shaft 5 x 24, no brake | | |
| B2-3 | What force can the cutter bind with on retract? | S3 retract case | Sean | F_bind 300 N | | |
| B2-4 | Safety factor on screw buckling, operating cases and the stall fault case | S3-2 | Sean | 3 for all cases | | |
| B2-5 | Rapid traverse speed for the lift | critical speed, cycle time | Sean | 25 mm/s | | |
| B2-6 | Masses of the drill-to-ring bearing, pinions, gear hub, guide bushings with housings | W, S3 load cases, S6 | Sean | 1.5, 0.5 each, 0.7, 0.2 each kg | | |
| B2-7 | N5 update: in a stall-down crash through the cutter the kept parts see up to 1267 N (Tr12x3), above 1000 N. Accept, or name a rating check or a current limit? | S3-3, Step 2, 4a | Quinn | accept at 1267 N with no rating check | | |
| B2-8 | Is a self-locking lead acceptable as the power-off hold while the operator loads under the ring, or must the hold state be visible (park pin)? | hold row, N7, Step 2 | Quinn and Sean | self-locking lead, no visible state | | |
| B2-9 | DN23 names T8 with TR10 or TR12 if a compression case is needed. Every lift puts the screw below the nut in compression. Do you agree to Tr12x3? | jackscrew.*, DN23 | Quinn | Tr12x3 | | |
| B2-10 | Receiver seat (Design Notes 32): the receiver spigot (r 80) sits in the plate hole (r 80.2) with nothing under it. Sean picked a shoulder on the receiver resting on the plate top around the hole. Values: shoulder OD 200, 8 thick, bolted with 4 x M5 into the plate (uplift up to 1029.5 N in retract-with-bind and stall up); this needs tray.hole_r 81.2 to 101 and changes the ASSEMBLY.md load-path line that says the receiver puts 0 force on the plate. Any objection for the kept receiver and tray? | S3-3, Step 2, 4a | Quinn | receiver shoulder OD 200 x 8, 4 x M5, tray hole r 101 (Sean, Design Notes 32) | | |
