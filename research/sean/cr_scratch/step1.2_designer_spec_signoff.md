# Step 1.2 (b) Designer spec sign-off, S2 plan XY

Read 2026-11-25: `research/sean/cr_scratch/step1.2_designer_params_review.md`, `research/sean/cr_scratch/step1.2_engineer_spec.md`, `docs/sketches/s2_spec.yaml` (70 rows), `docs/sketches/proposed_params.yaml`, the S1 r5 text edits in `docs/sketches/s1_spec.yaml` (header l.8-14, bracket rows l.947-1012), gameplan l.145-261 and Design Notes 27. Heights z_A unless marked z_S. Plan distances DERIVED by convex-polygon distance on spec footprints (round parts as circumscribing 256-gons; script in the session scratchpad, not a project file).

**Verdict: FIX** (4 items). FIX 1 is the guide-tie pick the Engineer asked for. FIX 2 to 4 are text and spec-field edits; none moves a value or a key.

## Corrections to the brief

1. **The Engineer's no-key-change tie (z 1165 to 1225) still interferes, with the member.** His strip runs from the rod centre to the member *centre* (`plan_poly` strip `to: frame_upper.radius * cosd(...)`). That puts the tie end inside the 60 x 60 member footprint over the tie's whole 60 height (member z 12 to 1225). Declared C, it fails K7 on overlap area. The same overlap exists in the spec as written today (tie 1152 to 1212). His open item 4e lists tie|member among pairs that touch in z and overlap in plan. These two overlap in both plan and z. DERIVED.
2. Engineer Correction 2 accepted: the rod at theta 0 has its surface 4.00 from the stop-pin pocket wall. My 14 was measured from the rod centre. The two are z-separated (pocket z 0 to 4, rod from 12).
3. Engineer Correction 3 accepted: nut housings are ring-mounted and are not in the S2-5a list. My "housings 16.41" in the S2-5a Z line is withdrawn. The S2-5a least gap stays 11.71 (lift motors).
4. Engineer Correction 5 accepted: ring|guide_member reads 10.00 under my G 10 group. That is a design identity (`guide.radius` - `guide.rod_od` / 2 - `ring.od` / 2 = 230 - 10 - 210). It stays, and it is reported under tight spots.

## 1. Part list (detail 1 common (b))

Every part a `shape` string in `s2_spec.yaml` names, with its row or its `not_drawn` reason.

| Part named | In shape of | Row / not_drawn |
|---|---|---|
| base plate | base_plate, frame_upper_a/_b, guide rods | base_plate |
| receiver spigot hole | base_plate, base_spigot_hole | base_spigot_hole |
| column notch (x2), plate notch outline | base_plate, frame_upper_c | base_plate (boundary between its five pieces) |
| slotted fastener holes | base_plate, base_slots | base_slots |
| key pockets | base_plate, base_key_pockets | base_key_pockets |
| pin pocket | base_plate, base_pin_pocket | base_pin_pocket |
| base frame rails, end members, plate supports; end member under a, b; rail top under c; +Y rail | base_frame, frame_upper_a/_b/_c, slot_line_c | base_frame |
| slot line C | slot_line_c, base_key_pockets | slot_line_c |
| other rail slot lines | slot_lines | slot_lines |
| screw frame members | frame_upper_a/_b/_c, bracket rows, guide_tie | frame_upper_a, _b, _c |
| T8 screws | screw_x, liftmotor_x | screw_a, _b, _c |
| nut flanges | screw_x, nut_x, nut_housing_x | nut_a, _b, _c |
| nut-housing bosses | screw_x, nut_x, ring | nut_housing_a, _b, _c |
| anchor bracket arms | anchor_x, bracket_anchor_x, descent_stop | bracket_anchor_a, _b, _c |
| top-guide bracket arms | guide_x, bracket_guide_x | bracket_guide_a, _b, _c |
| anchor blocks (block circle r 21) | bracket_anchor_x, liftmotor_x | anchor_a, _b, _c |
| top-guide blocks | bracket_guide_x | guide_a, _b, _c |
| descent-stop pad (one) | descent_stop, descent_stop_post | descent_stop |
| descent-stop post | descent_stop | descent_stop_post |
| NEMA 17 lift motors | liftmotor_x | liftmotor_a, _b, _c |
| ring plate, clearance bore, ring rim | ring, nut_housing_x, motor_mount_x, descent_stop, sightline_f6 | ring |
| NEMA 23 mount blocks | ring, motor_mount_x | motor_mount_a, _b, _c |
| guide lugs | ring, guide_lug_x, guide rods | guide_lug_a, _b |
| LM20UU bushing housing (block d 40) | guide_lug_x, guide_bushing_x, guide rods | guide_bushing_a, _b |
| **LM20UU bushing (OD 32 x 42) inside the housing** | guide_bushing_x | **missing: no row, no not_drawn (FIX 2)** |
| drill-to-ring bearing | bearing | bearing |
| ring gear with tooth ticks | gear, bearing | gear |
| gear clamp hub | gear, gear_hub | gear_hub |
| bevel pinions with hubs | pinion_x, motor23_x | pinion_a, _b, _c |
| radial shaft (NEMA 23 output shaft) | pinion_x, motor23_x, motor_shaft_x | motor_shaft_a, _b, _c |
| pinion axes (radial chain lines) | pinion_x, motor_shaft_x, pinion_axis_x | pinion_axis_a, _b, _c |
| NEMA 23 motors | pinion_x, motor23_x, motor_mount_x | motor23_a, _b, _c |
| guide rods | guide_member/_b, guide_lug_x, guide_bushing_x, guide_tie_x | guide_member, guide_member_b |
| rod top ties | guide_tie_x | guide_tie_a, _b |
| drill tube | drill_tube, gear_hub | drill_tube |
| keep-out circle | keepout, drill_head | keepout |
| cutter rim circle | drill_head, sightline_f6 | drill_head |
| datum B cross, +X / +Y arrows, theta arrow | collet_axis | collet_axis |
| operator loading sector | operator_sector | operator_sector |
| F6 sightline, observer point | sightline_f6 | sightline_f6 |
| wing nut, collet, holder | spec `part_list` (no S2 shape names them) | not_drawn: below the drill path, drawn in S1 |
| power-off hold device | spec `part_list` | not_drawn: Step 2 (N7, T2-c) |
| descent-stop pads at jackscrew.angle[0], [2] | `not_drawn` | not_drawn: declined by Sean (Design Notes 27) |

**Count: 41 named parts with a row, 3 not_drawn entries, 1 missing (the LM20UU bushing).** Every ring.* functional feature S2 shows has a row: nut housings, motor mounts, guide lugs, clearance bore (ring `section`), bearing seat (ring|bearing C).

The second clause of detail 1 common (b), "the figure note states the not-drawn parts", has no spec carrier. `plan_figure.note` does not list them, and S1 had no such field (FIX 3).

## 2. Shapes against my notes

Every row matches my section 8 note, or improves on it. Confirmed (Engineer open item 3):
- base_plate: row references added. Confirmed.
- slot_line_c split into slot_line_c and slot_lines. Confirmed.
- bracket rows split into anchor and guide rows that share a footprint, with S1 ids, "r 244 at frame_upper.radius 274" and "dashed where a nearer part covers it". Confirmed.
- descent_stop: one pad at jackscrew.angle[1], per Design Notes 27. Confirmed. My "on each anchor arm" is superseded by Sean's ruling.
- liftmotor_x: "(liftmotor.plan_rot 0)" and the circumscribing-footprint note. Confirmed.
- motor_shaft_x, pinion_axis_x, descent_stop_post, guide_bushing_x: new strings, dimensions checked against the overlay (shaft r 121 to 142 x 8; toe tip r 95.22 to 218; post r 200 to 215 x 60; housing d 40 hanging 30). Confirmed.
- guide_tie_x: changes under FIX 1.

Dimensions in shape strings checked against the plan table: nut housing d 50, lug r 210 to 250 x 40, pinion r 95.2 to 125 with hub to 140, motor r 142 to 218 x 57, gear r 90 to 126.32, bearing r 76.2 to 100, member c y -304 to -244. All agree.

## 3. Phase, guide, lift motor, bushing, S2-5, sightline

| Item | Set at 1.2 (a) / ruled | Spec | Result |
|---|---|---|---|
| Screw-to-pinion phase | 60 deg (O1-B, Design Notes 27) | S2-1 phase_deg 60; screws 30/150/270, pinions 90/210/330 | PASS |
| Guide option (N2) | two rods r 230 at 0, 180; rails on members as M2 alternative | guide_member, guide_member_b; gameplan l.245 names the alternative | PASS |
| Lift motor | coaxial under the anchor, 42 square, plan_rot 0 | liftmotor_x, footprint r 29.70 circumscribing | PASS |
| Bushing form (S2-d) | LM20UU 32 x 42 in a d 40 housing, 30 below the ring | guide_bushing_x, `guide.bushing_*` | PASS (part-list gap, FIX 2) |
| S2-5a | sector theta 90, half 45, r 400, fixed parts all z, F | s2_checks S2-5a, 27 fixed rows, least 11.71 | PASS |
| S2-5b | premise: ring parts entering the sector at load >= 10 above 940 | s2_checks S2-5b, 23 ring rows, least 136.84 (bearing) | PASS; I raise and sign the rule (detail 1 common (h)); its Z and B are due at (c) with S2-5a |
| Sightline | r 400, theta 60, eye 1540, solid outside r 210, dashed inside | sightline_f6 | PASS. No `poses` field: it is drawn in the load figure, and its label names capture_end. Accepted |
| Descent stop | one pad (Sean) | descent_stop, stop_pad_count 1 | PASS |

## 4. Neighbour classes, g_min, keep-out pairs

- fixed_g10 (moving ring parts against members, lift motors, blocks, arms, post, rods, ties; swept): G 10 as in my section 10. PASS. ring|rod 10.00 is an identity (Correction 4).
- ring|descent_stop C at capture_end; nut_housing_a|descent_stop G 10 at capture_end (15.00). PASS.
- Rod in bushing N; rod in lug N; screw in nut, anchor and guide N; gear|pinion N (mesh). PASS.
- S2-a: 25 fixed rows against `keepout` G 0. Least 44.10 (lift motors), cutter overhang 2.70 reported. PASS. NOTE 1: guide_tie_a/_b are not in the S2-a group. As undeclared F they pass (113.47 clear under FIX 1). Add them when FIX 1 edits those rows.
- guide_member|guide_tie and guide_tie|frame_upper/bracket_guide: change under FIX 1.

## 5. Operator-task rows against the plan table

Gameplan l.180, 181 and 184 already carry the 1.2 (a) rows. Checked against the Engineer's plan table (z_S):
- Load: torso r >= 304 (member c outer face 304.00); bearing 1136.84; NEMA 23 at theta 90 at 1185.34 to 1242.34, r 142 to 218; drill tip 1019.84. Agree.
- Change a collet: lift motors 252 to 300, plus coupling to 325; anchor arms 325 to 355, r 181 to 244; pad 362.84 to 374.84, r 200 to 215, theta 150. Agree. Sector opening at r 181: 2 x 181 x sin 45 = 256. Agree.
- Watch: r 400, theta 60, eye 1600 z_S; limits 492.46 and 578.80 z_S. Agree.
- Under FIX 1 the tie lies at 1225 to 1285 z_S, theta -7 to 25 (tie b mirrored, 155 to 187), 76.35 outside the sector edge. No operator row changes.

## 6. Rubric additions

| Line | True on spec values | Predicate / visual |
|---|---|---|
| plan handedness, screws 30/150/270, pinions 90/210/330 | yes | K8 azimuth on every placed row; S2-1 |
| all three screw sets, pinions, NEMA 23s, lift motors, members drawn | yes | K9 |
| motor outboard, pinion inboard, narrowing toward the axis | yes (motor r 142 to 218 outboard of pinion r 95.22 to 140) | K8 outboard frame radial and taper inward. Both plan forms land at (c) with Z and B before M1 (Engineer open item 4b) |
| ring reads as a structure | yes (3 housings, 3 mounts, 2 lugs) | visual only (V7). NOTE 3: write "(visual only, V7)" |
| member c on the rail top inside the notch, outline visible | yes (5.00 clear on three sides) | seat: S2-6; outline visible: visual only |

## 7. FIX items

**FIX 1. guide_tie_a, guide_tie_b: pick and dimensions (blocks the signature).** I take the Engineer's option, tie on the top-guide arm top at z 1165 to 1225, and amend its plan end. The tie stops at the member's near corner. It does not run to the member centre.

Design intent: the tie is a 30-6060 stand-in lying on the top-guide bracket arm, bolted down to it. Its end butts the member's near corner. The rod top passes 47 up into a bore in the tie, which grips it 20 from the tie end and 20 from each side. The arm is the seat, so the tie takes no new support.

Values (tie a; tie b is the mirror in x, rod at guide.angle[1] to member a at jackscrew.angle[1]):

| Field | Value | Source |
|---|---|---|
| z_rule | z_min `jackscrew.top_guide_z` (1165), z_max `jackscrew.top_guide_z + profile.height` (1225) | ASSUMED; the top is flush with the member top 12 + 1213 = 1225 (identity, DERIVED) |
| plan | one strip, half-width `profile.width / 2`, along û = unit(member centre - rod centre) | DERIVED |
| strip from | rod centre - 30 û = (228.41, -29.96) | 30 = `profile.width / 2`: the tie runs 30 past the rod centre so the rod circle r 10 sits inside it |
| strip to | rod centre + s_c û = (235.09, 95.55), with s_c = û · (K - rod centre) = 95.69 and K the member's near corner = member centre - (w/2) r̂(θm) - (w/2) t̂(θm) = (226.31, 96.02); r̂ = (cos, sin), t̂ = (-sin, cos), θm = jackscrew.angle[0]. For tie b: K = member centre - (w/2) r̂ + (w/2) t̂ at θm = jackscrew.angle[1] = (-226.31, 96.02) | DERIVED; every member edge from K points forward along û (components 0.545, 0.838), so the whole member lies at s >= s_c and the tie touches it at K only |
| footprint | 125.69 x 60; corners (198.45, -28.36), (258.36, -31.55), (265.04, 93.96), (205.13, 97.15) | DERIVED |
| keys | add `jackscrew.top_guide_z`, `jackscrew.pitch_radius`, `jackscrew.nut_flange_od` (arm), drop `guide.length` from the z expression (the rod still reads it) | |

Neighbours (replace the two C rows):
- guide_member|guide_tie_a: **N**, "rod top in a bore in the tie, 1165 to 1212 (guide.top_support)". It is not a section-row pair, so K7 admits the N.
- bracket_guide_b|guide_tie_a: **C**, g_min 0, "tie bottom on the arm top at 1165, bolted (guide.top_support)". Plan overlap 492.21 with z contact. This is the plan-C case of Engineer open item 4e, and its rule comes at (c).
- frame_upper_b|guide_tie_a: **C**, g_min 0, "tie end at the member corner K (point contact, plan distance 0.00, overlap 0)".
- Add guide_tie_a/_b to the keepout S2-a group, G 0 (113.47).

Clearances at the new footprint (DERIVED, tie a; tie b is the mirror):

| Pair | Plan | z (worst pose) | Result |
|---|---|---|---|
| tie a / motor23_b, motor_mount_b (theta 330) | 46.16 | motor top at park 1182.34 overlaps 1165 to 1225 | G 10 on plan |
| tie a / pinion_b | 54.44 | pinion top at park 1199.46 | G 10 on plan |
| tie a / gear | 73.35 | gear at park 1182.07 to 1215.84 | G 10 on plan |
| tie a / ring, guide_lug_a (plan overlap) | 0 | ring and lug top at park 1101.84; gap 63.16 | G 10 on z |
| tie a / guide_b block | 44.56 | block top 1165 = tie bottom | pass |
| tie a / operator sector edge (theta 45) | 76.35 | all z | S2-5a F |
| tie a / keep-out | 113.47 | | G 0 |

Text to change with it:
- shape: "rod top tie, 30-6060 stand-in on the top-guide bracket arm (row bracket_guide_b), from 30 past the rod centre to the near corner of screw frame member b, rod top in a bore in the tie, dashed, labelled Step 2"
- notes: "z 1165 to 1225 (on the arm top, top flush with the member top); strip from rod centre - 30 û to the member near corner station 95.69; Step 2 decides the tie (guide.top_support ASSUMED)"
- overlay `guide.top_support` value: "30-6060 tie on each top-guide bracket arm at jackscrew.angle[0] and [1], z_A 1165 to 1225, rod top (1212) in a bore in the tie, tie end at the member's near corner; rod at guide.angle[0] to member at jackscrew.angle[0], rod at guide.angle[1] to member at jackscrew.angle[1]; Step 2 decides", source "Designer 1.2 (b) sign-off FIX 1", status ASSUMED.
- The Loftsman checks s_c, K and the corner list at P3b or at the re-sign.

**FIX 2. guide_bushing_a/_b: the LM20UU bushing has no row and no not_drawn entry.** Add to `not_drawn`: `{part: "LM20UU bushing (OD 32 x 42)", reason: "inside the housing (rows guide_bushing_a, _b) and the lug; concealed in plan by both; keys guide.bushing_od, guide.bushing_length on the housing rows"}`. Add a matching `part_list` line.

**FIX 3. Figure note for the not-drawn parts (detail 1 common (b), second clause).** Add `figure_note` to `plan_figure`, for example: `figure_note: "Not drawn: wing nut, collet, holder (below the drill path, S1); power-off hold device (Step 2); LM20UU bushing (inside housing and lug); descent-stop pads at 30 and 270 (one pad, Design Notes 27)"`. s2_plan.py prints it on the figure. At (c), K4 (or a label check) verifies the drawn text names every `not_drawn` part, with Z and B.

**FIX 4. Stale echo site `ring.motor_mount_placement`.** The text "phase to the screws per S2" becomes "pinion azimuths = screw azimuths + 60 deg (pinion.angle), S2; Designer 1.2 (a), Sean STOP S2-A O1-B". This is a text value only. No row reads it, but it is a derived location of the phase echo site (my section 13).

## 8. NOTES (no action required for signature)

1. S2-a group: add the ties (included in FIX 1).
2. S1 r5 header (`s1_spec.yaml` l.11-13) lists the S2-only parts: theta 270 set, member c, bushing housing. The rod top ties belong in that list. In the S1 r5 side view the rods at x ±230 will show free tops, and M1 at r5 will read that against this note.
3. Rubric line 4: mark "(visual only, V7)".
4. Engineer open item 7, the S1 r5 bracket shape strings now reading r 244: the Loftsman rules this. My position: the shape text must describe the r5 drawing. Reverting to r 270 against a 244 drawing would repeat the S1 shape-text-versus-drawing failure that cost r3.
5. Tight spots stand as identities: member c outer face 0.00 to the plate edge, ring|rod 10.00. Both are reported, not asserted.

## 9. Sign-off conditions

SPEC SIGNED (Designer) follows when FIX 1 to 4 are applied as written, with no other row changed, and the Loftsman confirms the FIX 1 footprint. Re-check scope: guide_tie_a/_b rows, the `not_drawn` and `part_list` blocks, `plan_figure`, and the two overlay text leaves.

## Gameplan lines to change

1. Echo Site Registry, after l.678 (`| Guide bushing **LM20UU 32 x 42** in an OD 40 housing hanging 30 below the ring | overlay \`guide.bushing_*\`, \`ring.guide_lug_half_width\` | ASSUMED (Designer 1.2 (a)) |`), insert:
   `| Guide rod top tie **30-6060, z_A 1165 to 1225** on the top-guide arm, rod top 1212 in the tie, end at the member's near corner (125.69 x 60) | overlay \`guide.top_support\`, \`jackscrew.top_guide_z\`, \`profile.*\`, \`frame_upper.radius\` | ASSUMED (Designer 1.2 (b) sign-off FIX 1; Step 2 decides) |`
2. l.166 (detail 1 common (b)). Old: `and the figure note states the not-drawn parts` New: `and the figure note states the not-drawn parts (spec field \`figure_note\` on the figure entry, checked against \`not_drawn\` from S2 on)`
3. Progress Log row 1.2 (append): `P3a Designer sign-off: FIX 4 (guide tie on the top-guide arm z 1165 to 1225 ending at the member corner; LM20UU bushing not_drawn; figure_note; motor_mount_placement text); part list 41 rows / 3 not_drawn / 1 missing.`
