## Verdict on the Step 2 concept

The concept answers most of what I raised. Clamp and stop are separate (decision 8). The nut is not a stop. The captive-flange release replaces the jacking holes. The PTFE washer is adopted. The bracket rule is full-size. Those I accept.

Three things are not designed: how a person gets a core into the jig, whether the wrong-collet defence exists as a feature, and what an operator can reach when something jams. Four items need the concept to change (S2-1, S2-2, S2-3, S2-7a). The rest Step 3 can absorb.

Visual gate NOT RUN (text-only). Numbers marked (V) are quoted from the concept; numbers marked (mine) are my arithmetic from concept values and Step 3 confirms them. The Addendum rule (large, hand-friendly hardware and access) is applied as a test throughout.

BLOCK means the concept text or the frozen ICD changes. ABSORB means a Step 3 parameter or Step 5 test carries it.

---

## S2-1. Steady rest: needed at every core length, and the release must be mechanical. BLOCK

**Concern.**
- Decision 9 says a 0.5 m core "needs no aid". That is wrong on the concept's own numbers. The core stands in a bore with 1 mm per side over a 30 mm grip, so it tips freely at about 1.9 deg. The nut takes two hands (52 N per hand on a 230 mm span). Someone has to hold a 10.4 kg core (102 N) upright while two hands turn the nut. That is the three-handed job from D5, and it is still there at 0.5 m.
- Hands needed with the rest at every length. Lower the core: 2 hands. Steady it with one hand and close the rest with the other: 2 hands. Tighten the nut with the core free-standing against the rest: 2 hands. Never more than two at a time. Without the rest at 0.5 m the sequence needs three.
- The rest's value is more than convenience. Clamping with the rest closed fixes the core pose before the collet locks. That is what makes the 0.25 + 0.25 lead-in budget true. Clamped unguided, the tilt is 0.57 deg and 5.0 to 7.5 mm at the core top. The concept does not say the rest is closed during clamping. It must.
- "Releases only after the upper assembly lead-in has captured the core (U12)" is a procedure. The descending cutter, with 1000 N behind it, meets a rest an operator forgot to open. Design the error out: a ramp or cam on the upper assembly pushes the swing arm clear once the lead-in is engaged. Then the rest cannot release early or be left in the cutter's path (keep-out radius 86.2).
- "Centring to plus or minus 0.25 mm of datum B" over a swing-away arm is a claimed precision with no mechanism behind it. Three linked rollers or a self-centring linkage can do it. A cantilever arm with three independent rollers cannot.

**Carrying parameters (Step 3, test Step 5).**
- `rest.count_of_lengths` = all (0.5, 0.75 and 1.0 m).
- `rest.height_positions` = [340, 490] mm, two positive detents.
- `rest.roller_count` 3, `rest.roller_dia`, `rest.centre_repeatability` 0.25 and its linkage type.
- `rest.arm_length` and `rest.swing_clearance_radius` at least 86.2.
- `rest.release_ramp_z` (set by U12 lead-in engagement).
- `rest.close_handle` (one-handed, large, gloved-hand size).
- `rest.hold_open_detent`.
- Test: A1 hand access and a sequence test showing the rest cannot be closed while the upper assembly is within the lead-in zone.
- Change the U12 ICD row from "rest releases only after" to "rest is released mechanically by the upper assembly after capture".

---

## S2-2. Loading envelope: the upper assembly cannot be where the core goes in. BLOCK

**Concern.**
- The core is lowered from above through the nut into the collet. Seat is about z = 40 and nut top is 150 (placeholder). The core bottom must reach the nut top before it can descend. At that moment the core top is at 150 + L: 650 mm for 0.5 m, 900 mm for 0.75 m (mine).
- The concept parks the cutter at `stop.start_z` 660 (0.5 m) and 800 (0.75 m). At 0.5 m that is 10 mm of clearance, with no allowance for tilting the core into the bore. At 0.75 m it is 100 mm short. Tilting the core 20 deg still needs about 855 mm (mine). The 0.75 m core, the design install case from gate B6, cannot be loaded with the upper assembly at start.
- The concept never defines a park or load position. `upper.travel_max` 500 is a cutting stroke. Treating it as the only vertical range is the omission.
- The column has room: 1600 mm overall, drill body about 480 mm above the cutter low point. A park at about 950 mm (cutter low) works with the body at about 1430. This is the same arithmetic the concept used to reject a 1 m core.
- A 15 kg upper assembly parked at height over the operator's hands and the core is a crush hazard if it drops. Nothing holds it.

**Carrying parameters.**
- `upper.park_z` DERIVED as `stop.nut_top_z_max + core.length_install + load_clearance` (about 950 for 0.75 m).
- `upper.park_lock`: a positive mechanical lock, with a signifier for locked and unlocked.
- `upper.load_clearance` 50 mm (assumed) to allow tilt-in.
- Test: P6 envelope check at park, A1 hand space between park position and the rest arm.
- Add an ICD row: "Park/load position, above travel, locked." `upper.travel_max` stays 500 and is not touched.

---

## S2-3. Strap point as written cannot work. BLOCK

**Concern.**
- "An M8 forged eye in a T-nut": the 30-6060 slot opening measures 8.0 mm (profile params). An M8 shank passes through an 8.0 mm opening with zero clearance. The declared stock is M6 T-nuts (`hardware.tnut_thread` M6, DECLARED). The M8 eye does not fit the profile the human supplied.
- "On a frame cross member over the axis": the frame is the base perimeter at z = 0, with no member above the axis. The columns are the only members at height. A member there is a new part, and the upper assembly occupies the axis when it is parked. A strap hung from above the axis passes through the drill.
- The 80 kg rating is on the eye. The T-nut pull-out in a 30-series slot is the unknown, and SKU 40-3914 is a 40-series part with 30-series fit ASSUMED. No test carries the 80 kg.
- A strap needs a hoist or a hand to take the load. The concept names none. "Strap" is a word, not a mechanism.

**Carrying parameters.**
- For the 0.75 m core, choose one: a hinged cradle (V-trough on the frame that tips the core upright into the receiver), or a strap anchored to a column-top cross member that the upper assembly never occupies. If the strap stays, add `strap.thread` M6, `strap.anchor_member` (a stock 728 or 980 mm piece across the column tops, both unallocated), `strap.rating_test`, `strap.hoist_type`.
- `collet.chamfer_lead_in` with funnel capture matching `icd.core_lead_in_capture` 10 mm, so a blind entry into a 1 mm-per-side bore works.
- Cradle alternative: `cradle.length`, `cradle.pivot_height`, `cradle.latch`.
- Test: a load-path check at 80 kg on the anchor, and A1 for strap clearance against the park position.

---

## S2-4. Wrong-collet defence is still a number. ABSORB

**Concern.**
- Decision 7 defines the window (d - 1.5 to d + 1.0) and says nothing of caddy, colour, rim notches or witness mark. These were D4 and D10, and I was told they were accepted. They are in no decision, no ICD row and no param.
- The concept hands me a gauge that costs nothing. The holder stroke gap is 13.126 mm relaxed, 8.59 mm at core d + 1, 1.5 mm minimum at K-max (V). The 10 deg cone turns one family step (1.25 mm radial) into about 7 mm of flange travel (mine). That is 8.59 - 1.5 = 7.09 mm, the same figure. A one-step wrong collet reads about 7 mm off its zone. A rule on the receiver rim marked in 1 mm steps reads clearly to a full-size hand.
- A collet two steps too large bottoms at 1.5 mm with the slits shut and a loose core. The gap is never loaded, so nothing stops the nut. The scale must carry a marked "wrong collet" region at gap below the zone floor. Without it the operator sees only a nut that stopped.
- A core too big for the collet is rejected by the bore (d + 2). A core between d + 1 and d + 2 enters and clamps above the zone. The scale must also flag gap above the zone ceiling.

**Carrying parameters.**
- `witness.zone_low`, `witness.zone_high` per collet, DERIVED from the window and the cone.
- `witness.scale_pitch` 1.0 mm, `witness.wrong_collet_band` marked.
- `collet.rim_notch_count` = family index (1 to 7), `collet.colour` per size, `collet.label_window_text` (engraved window, for example "91.3 to 93.8"), `collet.label_height` at least 6 mm.
- `caddy.socket_count` 7, sockets matched by colour and notch count, window printed per socket.
- Test: C-series check that zones for adjacent collets do not overlap; A1 for scale legibility from 500 mm.

---

## S2-5. Wing grip. ABSORB

**Concern.**
- The concept keeps "wing span as a parameter" and gives 52 N per hand at 230 mm. Nothing else describes a wing. A push of 52 N at a tip is a palm or edge push; the wing must be shaped for it.
- Wing height of at least 30 mm for a palm face, edge radius for the heel of the hand, and knuckle clearance below the wing to the base plate or tray lip. A full-size hand needs about 50 mm.
- Turns to clamp: a single start at 8 mm pitch with 24 mm minimum engagement plus 11.6 mm of clamp stroke is about 4.5 turns (mine). With two hands on two wings a half turn per grasp makes about 9 regrips on every core. That is a hand-fatigue number the concept does not report.
- Wing sweep radius is about 115 mm. The rest arm, the tray lip, bolt-down heads and the dust skirt are all in that sweep.
- At the metal stop the cutter sits 10 mm above the wing top. A 10 mm gap is a finger crush gap.

**Carrying parameters.**
- `wingnut.wing_count` 2, `wingnut.wing_height` 30 or more, `wingnut.wing_root_width`, `wingnut.edge_radius`.
- `wingnut.knuckle_clearance` at least 50 (wing underside to plate or tray).
- `wingnut.turns_to_clamp` DERIVED, with an advisory limit on regrips.
- `wingnut.sweep_clear_radius` 115 plus clearance, no part inside it.
- `stop.g_stop` raised from 10 to at least 25 mm (the finger crush minimum I recall from ISO 13854; Step 3 confirms against the standard). The cost is 15 mm of `core.min_exposed`, DERIVED.

---

## S2-6. Bracket and fastener access for a full-size hand. ABSORB

**Concern.**
- The rule is "at least 25 mm of clear radius for a 150 mm hex key swing". A radius around the head is necessary. A key swing needs a swept sector as well: the long arm sweeps a plane through at least 60 deg out to its full 150 mm, and the hand needs room at the arm's end. A 25 mm disc passes while a hand cannot turn the key.
- The concept does not say which face of the frame carries the brackets. Under the plate, or on inside faces blocked by the plate once it is down, the bracket is assembled once and never adjusted. A frame that cannot be squared after assembly is a recoverability failure.
- Bolt-down is the operating condition (tip-over 68 N at the column top), and its method is two words: "four bolt-down slots (M6 T-nuts)". What the bolts clamp to is not stated. A T-nut in the rail slot needs a foot plate or foot bracket to reach a floor or bench. That part does not exist yet.
- M6 socket-head screws take a 5 mm key. For the points a person touches often (rest height, stop position, feet), use star knobs or T-handles. Keep hex keys for permanent joints.

**Carrying parameters.**
- `access.key_sector_deg` at least 60, `access.key_arm_length` 150, `access.head_clear_radius` 25. Both tested in A1 on assembled solids.
- `bracket.face` = vertical inside faces, never under the plate or beneath a part that must come off to reach them.
- `bolt_down.method` (foot plate, pitch, fasteners), `bolt_down.count` 4, `bolt_down.head_access` same sector rule.
- `hardware.adjust_interface` = knob or T-handle for rest, stop and feet.
- `hardware.tnut_fit_30series` VERIFIED before bolt-down and strap rely on it (SKU 40-3914 is a 40-series part).

---

## S2-7. Release and jam recovery

**a. The wings are not reachable at the stop. BLOCK**
- With the cutter at the metal stop, 10 mm above the wing top, nobody can turn the nut. The release path is the collar back-off lift, and it needs the wings. If the drill jams on the core at or near the stop, the clamp cannot be loosened.
- The recovery path is: raise the upper assembly, then release. The concept has no manual raise.
- Add an ICD row: "Upper assembly manually raisable by one person with the drill unpowered, to park." Without it, release depends on the drill working.
- Parameters: `upper.manual_raise` (method, force), `stop.g_stop` per S2-5. Test: H8 jam trial with the drill unpowered.

**b. The lift-play dead zone reads as a seized nut. ABSORB**
- Lift play 0.75 mm on an 8 mm pitch is about 34 deg of free turn (mine). Then the nut tightens again as the collar begins to lift the holder. The operator, expecting a nut to loosen when turned, feels a second stiffening and may stop.
- `nut.release_marker`: a printed mark that aligns when the lift has engaged, and an arrow "keep turning". `nut.lift_play` stays 0.75. Test: H5 with a cold user.

**c. Tommy-bar and the over-torque case. ABSORB**
- The holder stroke gap is now "never loaded". Over-tightening is therefore limited by the operator only. The tommy-bar socket was kept in decision 4 as a response to D1, but no bar is specified. A 0.5 m bar at 100 N is 50 N m, about four times the 12 N m hand limit and about 1.6 kN axial (mine). The closed loop (receiver wall in tension, thread flank) is not checked for that.
- Decision 3 has no abuse load case. Add `loads.nut_torque_abuse` 25 N m (assumed) and check the nine members at it. Supply the bar as a part with fixed length (`nut.tommy_bar_length` sized so a hand gives at most 15 N m) so the bar is the fuse.
- If the loop fails at 25 N m, the 1.5 mm gap becomes a real contact stop. Step 3 decides from the check, and this note does not reopen the concept.

**d. The PTFE washer is a policy, not a feature. ABSORB**
- "Always fitted" depends on a loose ring (ID 136.8, OD 143.2, 1.3 thick) staying on the holder when the nut comes off. A lost washer drops the jig to 9.13 N m at d = 90, below the 10 N m requirement, with nothing to show it.
- `washer.retention` captive in the nut face (snap lip or adhesive), `washer.pocket_depth` such that the nut shows a visible gap when the washer is absent. Test: H1 with and without the washer; A1 for a missing-washer render.

---

## S2-8. Clamp versus stop separation. Accepted, with two residuals. ABSORB

**Concern.**
- Accepted: the nut never carries descent load; the metal stop is on the upper assembly. This is the right separation.
- Residual 1. The nut top moves with clamp state. Holder stroke runs from 13.126 mm relaxed to 1.5 mm, 11.6 mm in all (V). `stop.nut_top_z` 150 in the frozen ICD is a single placeholder. `g_stop` must be measured at the highest nut position, not at the nominal one, and `core.min_exposed` depends on it.
- Residual 2. `stop.height_z` is an adjustable range, 160 to 300. An adjustable 1000 N stop has a wrong-setting trap: set too low, it is the crash. Make the floor stop fixed at the nut-safe height (never adjusted) and make the 300 mm value a separate adjustable travel limiter with labelled detents, not a continuous slot.

**Carrying parameters.**
- `stop.nut_top_z_max`, `stop.nut_top_z_min` DERIVED from the stroke and the family; `stop.nut_top_z` retired as a single value.
- `stop.floor_z` fixed; `stop.travel_limit_z` with detents for 0.5, 0.75 and 1.0 m, each labelled.
- Test: A2 at the highest nut position across all seven collets.

---

## Decisions that leave a later part a placeholder

| Decision | Later part | Why it is a placeholder |
|---|---|---|
| 9 steady rest | Rest, arm, mount | Named, with a height and a 0.25 mm claim; no mechanism, no mount, no release. Covered by S2-1. |
| 9 strap point | Strap anchor | M8 eye does not fit the 8.0 mm slot; no member over the axis. Covered by S2-3. |
| 9 handling | Park position | Not defined; start_z cannot admit the core. Covered by S2-2. |
| ICD `stop.nut_top_z` 150 | Stop, exposed core | Single value for a part that moves 11.6 mm. Covered by S2-8. |
| 9 bolt-down | Foot plate | "Slots" with nothing to bolt to. Covered by S2-6. |
| 4 tommy-bar socket | Bar | Socket without a bar; the bar length is the torque limit. Covered by S2-7c. |
| 4 PTFE washer | Washer retention | Separate loose ring carries a headline number. Covered by S2-7d. |
| 7 window and family | Caddy, colour, notches, witness | Family defined as bore blanks; defence not present. Covered by S2-4. |

The four BLOCKs go back to the Engineer before Step 3 opens. Everything else I have written as a Step 3 parameter.
