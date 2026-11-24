## Verdicts

| Item | Verdict |
|---|---|
| Decision 1, force loop, holder never bottoms | WITHHELD |
| Decision 5, datum scheme against the ICD frame | WITHHELD |
| Decision 8, stop ownership | SIGNED (one non-blocking wording edit) |
| U12 lead-in and steady-rest handoff | WITHHELD |
| Concept test IDs name one predicate from final shapes | WITHHELD |

## 1. Decision 1 closed force loop: WITHHELD

Passes:
- The chain is one closed oriented cycle. Nine members: nut thread flank, nut clamp shoulder, holder bearing flange, holder cone, collet cone, collet foot, receiver floor seat, receiver wall in tension, receiver thread flank. The cycle returns to the nut thread flank, which is not a tenth member.
- The pair holder bottom to receiver floor is class G: 2.00 at K-max, 0.50 after the 1.5 margin. This matches the stack in my Step 2 section 1.4.
- Flange to rim: 13.126 (R), 1.5 (K-max), 8.59 (core d + 1). All match.

Fails, line 5: "Holder bottom stays 2.00 above the floor at K-max (0.50 after the 1.5 stroke margin)."
- Invariant: every pair that can stop the holder is class G with gap > 0 in every pose. That includes holder bottom against the collet foot ring top, not only the receiver floor.
- Numbers, from the agreed stack (my 1.4, Loftsman section 6 "Seat"):
  - Foot ring top = z 2.00 (ring z -4 to 2, pocket depth 4, protrusion 2.0). Ring radius 63.79.
  - Holder bottom at K-max = z 2.00. Holder bottom inner radius at K-max is 62.04, so the bottom annulus is r 62.04 to 67.04.
  - Overlap annulus r 62.04 to 63.79. Gap = 0.00, area 691.8 mm2. Pair class G required, delivered 0.
- Consequence: at max closure the holder lands on the ring ledge. That opens a second path: flange to holder body to ring to floor. It skips the cone, so the grip force on the core falls.
- The rim stroke gap of 1.5 never gets used. The ring stops the holder 1.5 earlier than the rim does. The "0.50 after margin" is unreachable, because the holder would have to penetrate the ring by 1.5.
- Correction to my own Step 2 WS8 row: I put the ledge at z = 0. The ring top is z = 2.00. That row was wrong.
- Required: add the pair "holder bottom to collet foot ring top" as a G-class check, gap >= 0.5 at K-max. Move the ring top or the ring OD to meet it. WS1 stays blocked by the holder bottom inner radius 62.04 against the ring radius 63.79 at insertion, if the ring top sits below z 2.

Required edits, not blocking by themselves:
- The ASSEMBLY.md line lists "nut thread flank, nut body, nut clamp shoulder...", which is ten members. Delete "nut body" to match the nine in decision 1. The washer is the member between the flange and the plate. Name it in the line: "holder bearing flange (through the PTFE or printed washer)".
- Receiver floor to base plate: the load is self-equilibrated in the receiver only if nothing under the floor takes load in parallel. A6 must compute the contact force on the receiver underside as 0, or the receiver must be the base body. The concept does not say which. State it.

## 2. Decision 5 datum scheme: WITHHELD

Passes:
- Datum A: concept "frame top plane" equals `icd.datum_a` (z = 0, base plate underside). Same plane if the plate rests on the frame top.
- Datum C: concept "frame slot line" equals `icd.datum_c`, rotation about Z.
- Degrees of freedom: A fixes 3, B fixes 2, C fixes 1. Total 6, no repeat.

Fails, lines 13 and 46: "B receiver axis located by cone and pilot", "Drill to receiver axis (coaxiality) 1.0 (A)".
- Invariant: a datum is a fixed feature. Each degree of freedom is constrained once, by a feature of a single part.
  - Datum B as written is established by the holder and collet (moving, d-dependent parts). It should be the receiver register bore, r 67.29. The holder and collet only transfer B to the core.
  - B is a printed receiver axis. Its x, y position relative to A and C (frame) comes from 8 slotted base plate holes. No locating feature fixes it. The chain B to drill axis (plate slots, T-nut play, column feet, carriage) has no entry in the tolerance table, so the 1.0 mm coaxiality is an input with no chain.
  - The rest centres "to datum B" (decision 9) while U12 centres "to the drill axis". Both are named, and they differ by up to 1.0.
- Required:
  - Define B by the bore.
  - Add a locating feature to the frame slot line C (pin, key or stop).
  - Derive the 1.0 coaxiality as the sum of entries.
- Two zero planes: Detail 2 stack has the receiver floor at z = 0; ICD datum A is the frame top. Give the offset (receiver floor above datum A) as one parameter, since `stop.nut_top_z` 150 depends on it.

## 3. Decision 8 stop ownership: SIGNED

- (i) Descent stop: upper assembly. Load path cutter, carriage, metal stop, columns, frame. No printed member and no loop through the nut, holder, collet, receiver or base plate. The counterface lies on the column or the frame (T-slot). The stop does not touch the nut.
- (ii) Holder stroke gap: base-side gap, class G, never loaded. It is consistent with S6 only after the ring pair of section 1 is added.
- Non-blocking wording fix. ICD row `stop.g_stop` reads "nut top (wings included) to cutter lowest point". The collar top is 6.75 above the plate, and the Loftsman reply and A2 take the collar top as reference (124.38). Read from the nut top, the collar clearance is 3.25, not 10. Change the row to "collar top".
- Reserved for decision 3, outside my signature. "The 1000 N descent never enters the collet" holds only if axial contact force between the drill (iris or cutter) and the core is 0 at the stop. The core is the one member that joins the stop path to the receiver path. A2 or H8 needs the pair drill to core as class G or F (sliding, force bounded). It must not be left unstated.

## 4. U12 lead-in and steady rest: WITHHELD

Lines: row U12 "centring plus or minus 0.25 mm to the drill axis" (line 69). Decision 9: "The rest releases only after the upper assembly lead-in has captured the core."
- Invariant: the core is constrained laterally by one grounded system at a time, or through an element of stated compliance. A closed lateral chain frame to receiver to collet to core to lead-in to column to frame is a loop through the printed receiver, collet, holder and base plate, with a preload set by the mismatches.
- Where it closes:
  - At the handoff, the collet, the rest and the lead-in all hold the core. The rest is on the frame, the lead-in on the upper assembly, the collet on the printed receiver. Mismatch = coaxiality 1.0 + core offset 0.805 + rest 0.25 + lead-in 0.25, with tilt 0.57 deg.
  - During the stroke, "centring to 0.25" means the lead-in touches the core (distance 0). That is the loop for 465 mm of travel.
- The concept does not say the lead-in is compliant, nor that it clears the core after capture.
- Required, either:
  - (a) The lead-in is a funnel only: after capture the bore radius >= core radius + 1.0 + 0.805 + 0.25, so the distance core to lead-in > 0 in the working state, or
  - (b) A named compliance with a stiffness and a limit force.
  - The throat check "0.25 + 0.25" then needs the stage at which that residual holds.
- Handoff order: the rest releases after capture, and in between the core has three constraints. Give the instant the loop opens: lead-in bore tested against the core after the rest swings clear, for all seven d.

## 5. Concept test IDs: WITHHELD

Each ID must name one predicate on final shapes. Findings from the concept text:
- Overloaded IDs, each used for several different predicates:
  - A1: datum A (row 57), hex-key access 25 mm (line 30), flange to nut crest play (row 42), column feet (row 70), torque reaction (row 71), the closed loop (decision 1).
  - A3: cone-angle capture (decision 2), datum B and C (rows 58 and 59), coaxiality, lead-in, core axis offset.
  - A2: keep-out radius, stop rating, g_stop, nut_top_z, stop height.
  - P6: mounting, travel, cable, footprint, decision 9.
  - H3: side-load hold test (decision 3) and clamped tilt (row 45). H7: tilt and handling.
  - Required: a table ID to one predicate. Split with suffixes (A1a, A1b...) as C9a/C9b already do.
- ID collision with my files: my Step 2 review used H1 to H7 for thread-hand probes and A1 to A5 for axial inequalities. The concept's H1 to H8 are hold and handling tests, and its A-series are assembly checks. My local labels are retired. The concept's IDs govern.
- Not final-shape predicates, so they do not satisfy "computed from final shapes":
  - H1, H2, H3, H4, H7, H8 are physical hold, pull and handling measurements. Keep them as measured tests. Label them so, with the instrument and the pass line, outside Rule M.
  - T7 is a prediction from assumed coefficients (mu_k, mu_b, mu_t, A). Accept only if r_p, r_bm and lambda are read from the final threads. It cannot fail on a wrong coefficient, so it does not count as a pass.
  - T3, C9b, C3 have tolerance entries of kind A (0.25, 0.15, 0.15). These are inputs. The test must be a min-distance or common-volume predicate on the built collet and core envelope, not a restatement of the number.
- Datum rows: "Datum A | A1" and "Mounting | P6" have a definition in the ID column, not a predicate. Give each a flatness or common-volume predicate, or mark "no test".
- IDs cited but not defined in the four files read: T1c, T4, T5, F2, B5, C10, A6, P1, C4. I cannot confirm any of them by name. List them with predicate and input shapes.

## Conditions to flip to SIGNED

1. Add the pair holder bottom to foot ring top, gap >= 0.5 at K-max. Fix the geometry. Correct WS8.
2. ASSEMBLY.md line: nine members, washer named. State the receiver underside to base plate force as 0.
3. Datum B defined by the receiver bore, a locating feature to slot line C, a coaxiality chain, and the offset between z = 0 planes.
4. U12: a clearance after capture or a compliance, plus the handoff order and the instant the loop opens.
5. ID-to-predicate table with the overloaded IDs split and the physical tests labelled.

## Re-check

Read: Revisions, decisions 1, 5, 8, 9, ICD rows 61 to 83, Test ID key.

| Item | Verdict |
|---|---|
| Decision 1 (ten members, ring stop) | SIGNED |
| Decision 5 (datum B chain to frame) | WITHHELD |
| U12 funnel | SIGNED |
| U13 park 950 | WITHHELD |
| U14 strap anchor | SIGNED |
| U15 manual raise | WITHHELD |
| U16 steady-rest cam release | WITHHELD |
| `stop.g_stop` wording | SIGNED |
| Decision 8 text | SIGNED (stands only if U16 is fixed) |
| Split test IDs and Test ID key | WITHHELD |

### Decision 1: SIGNED
- Ten members: nut thread flank, nut clamp shoulder, washer, holder flange, holder cone, collet cone, foot ring, floor seat, receiver wall, receiver thread flank. One closed cycle. The ASSEMBLY.md sentence lists the same ten.
- Ring pair: 11.626 (R), 7.089 (K at d+1: 9.089 - 2), 0.00 (K-max). Class C at K-max, G elsewhere. Matches my stack.
- Rim pair is G, never loaded. Floor pair G 2.00. "0.50 after margin" is withdrawn. WS8 corrected.
- Contact at K-max puts the ring and floor seat in parallel with the cone. Both are chain members, so no new member joins the loop.

### Decision 5: WITHHELD
Line 13: "a plate key (T-nut with a square key) in the slot fixing the base plate in rotation and one translation".
- Invariant: A, B, C remove 6 degrees of freedom, each exactly once, through features of the frame.
- Count: plate on A removes 3. One key in one slot line removes 2 (rotation and the translation across the slot). That is 5. The translation along slot line C has no feature. The plate slides there on 8 slotted holes.
- The column feet also sit on slot lines (row "Column foot on frame slot line", 0.25), so the drill axis is also free along the slot. The coaxiality chain (0.30 + 0.25 + 0.25 + 0.20) bounds the cross-slot direction only. Along the slot, B to drill axis is unbounded.
- Required: a stop or a second key in a crossing slot line or the frame rail, with its clearance added to the chain. Name which entry carries the along-slot clearance.
- Fixed since the first pass: B is now the register bore axis (one part), the floor offset 40 is one parameter, and the chain sum is 1.00.

### U12: SIGNED
- Bore 56.0 against the largest core radius 53.0 is 3.0, against the required 2.055 (1.0 + 0.805 + 0.25). Positive for all seven d. Capture 10 against 9.31 (7.5 + 1.0 + 0.805).
- The loop is closed from first touch to the step, 40 mm of travel, and open after it. The cam release (core top + 60) comes before first touch (+0), so the rest and funnel never both hold.
- Condition for the test: the transient seating force through the collet must not exceed the lateral load H3 already takes (10.6 N m). Put it in A3d or H8.

### U13: WITHHELD
Line 74: "not a cutting position, `upper.travel_max` untouched".
- Invariant: one definition of travel. Stop (about 170) to park (950) is 780 mm of carriage range against the declared 500 (P6c "travel at most 500"). Either P6c measures the cutting stroke, or the 780 exceeds the declared value.
- Required: define travel as cutting stroke and ask the human to confirm 780 mm of carriage range, or split P6c.
- The formula 150 + 750 + 50 puts the core on the collar top. The core top is at 40 + 750 = 790, so the clearance is 160, not 50. Safe, but state it as 790 + 160.

### U14: SIGNED
- Path: strap, eye-bolt, T-nut, cross member, columns, frame. No printed member, provided the two cross-member joints use metal brackets. Add them to the joint count (8 to 10).
- Edit: row 75 cites A1c for "strap clear of drill at park". The key's A1c does not say that (see IDs). At park, a strap from the core top (z 790, on axis) to an eye at z 1600, 300 off axis, crosses z 950 at x about 59, inside the cutter radius 88.9. A1c must compute this.

### U15: WITHHELD
Line 76: "works with the cutter jammed on the core".
- Invariant: when the carriage lifts with the core gripped, the lifting force closes through the core, collet, holder, receiver, base plate, frame, columns and hoist anchor. That is a loop through four printed parts, and it is not bounded.
- The concept names neither the hoist anchor nor a force limit. Hand 80 N through a ratchet hoist can exceed the collet pull-out (H2: 204 N).
- Required: anchor on metal (column-top cross member). State the fuse: the core slips in the collet below the printed-part rating, or the nut is backed off (collar lift) before the raise. Add one predicate for it.

### U16: WITHHELD
Lines: decision 9 "a cam finger hanging 250 mm below the cutter lowest point", row 77 "finger 250 below cutter lowest point".
- Invariant: the swept volume of every upper-assembly part, over the whole stroke to the stop, has zero common volume with printed solids. Only the metal stop bears.
- Numbers: finger tip = cutter z - 250. At the stop (160 to 170 above datum A) the tip is at -80 to -90, below the frame top. It sits at r 86.2 or more, over the base plate and frame.
- The finger meets the base plate top when cutter z = plate top + 250. That is at least 80 mm before the stop. Then the 1000 N descent bears on the printed base plate, a loop through a printed part, and decision 8's stop is not reached.
- A2e checks the released arm and finger against r 86.2 and the cutter volume. It does not check the finger against the base plate, the nut wings (r to 115) or the receiver.
- Required: a finger that folds or is tripped from a column ramp (row 77 key `rest.release_ramp_z` suggests one), plus A2e extended to the finger swept volume to the stop.
- The key name in row 77 (`rest.release_ramp_z`) and params (`rest.release_finger`) differ. Fix.

### stop.g_stop wording: SIGNED
- Row 68 reads collar top (wings included), highest clamped position. A2b measures the same. The 10 against collar top is correct.
- Stale: key `stop.nut_top_z` still says nut top, and row 72 "above nut top". Rename.

### Decision 8: SIGNED
- The text is unchanged and clean: (i) metal stop on the upper assembly, A2c, A2d. (ii) holder stroke gap, G, never loaded. It holds only if the finger of U16 is fixed.

### Test IDs: WITHHELD
Stale or undefined:
- Bare "A1" is still cited at line 30 and in tolerance row 42. A1 no longer exists in the key (A1a, A1b, A1c).
- A6 is cited for three jobs in decision 1 (receiver underside force, WS8, WS9). Split A6a, A6b, A6c or define in the CAD spec.

More than one predicate in one ID:
- A1c: no printed solid in foot, strap or stop path, and column-to-base-plate pair G or F.
- A3d: bore clearance >= 2.055 and capture >= 9.31.
- A3e: "placement predicates" for four things (floor, ring, nut bearing, engagement); the ring pair also sits in A1a.
- P6c: travel <= 500 and park envelope clears.
- A2e: arm outside r 86.2, finger outside r 86.2, cutter swept volume clear.
- A3a: "or" of two predicates (cone angle, capture pair). Acceptable as one release predicate if the CAD spec says so.

Not a final-shape predicate:
- A3b: "sum of the four entries is at most 1.0" adds assumed numbers. A wrong shape cannot fail it. Make it measure the built key-to-slot, spigot-to-hole, foot-to-slot and guide clearances.
- P6a: "ICD has no empty field" is a document check. Mark it so, outside Rule M.

Accepted as one predicate: A1a (quantified over the pair table), A1b, A2a, A2b, A2c, A2d, A3c, A3f, P6b. H1 to H4, H5, H7 to H10 are marked physical. T7 is marked prediction.

IDs T1c, T4, T5, T9, F2, F4, F6, S6, C3, C4, C8, C9, C10, P1, P8 are not restated in the concept. I cannot check them from these files.

### Flip conditions
1. Decision 5: constrain the along-slot translation and put its clearance in the chain.
2. U13: define travel (cutting stroke or total) and confirm 780 mm with the human.
3. U15: anchor on metal, name the fuse, add a predicate.
4. U16: fold or ramp-trip the finger, extend A2e to the swept volume to the stop.
5. IDs: split A1c, A3d, A3e, P6c, A2e, A6. Replace bare A1. Make A3b measure the built fits. Mark P6a.

## Re-check 2

Read: Revisions second pass, decisions 1, 5, 8, 9, ICD rows 61 to 83, tolerance rows 46 to 50, Test ID key.

| Item | Verdict |
|---|---|
| Decision 5 (stop pin, chain 0.87, A3b) | WITHHELD |
| U13 (500 working stroke, 950 park, pin latch) | SIGNED |
| U14 (choke strap, no anchor) | SIGNED |
| U15 (metal anchor, 300 N shear link) | SIGNED |
| U16 (flush cam lug, trip tower) | SIGNED |
| Decision 8 | SIGNED |
| Split test IDs | WITHHELD |

### Decision 5: WITHHELD
Line 13 (and tolerance rows 46 and 48): "a plate key (T-nut with a square key) in the rail slot line fixing the base plate in rotation and in translation across that slot" and row 48 "Column foot on frame slot line 0.20".
- Passes: the plate count is now 3 (A) + 2 (key) + 1 (pin) = 6. The pin in the end-member crossing slot fixes the along-slot translation of the plate. 0.25 and 0.20 combine to 0.320. Total 0.32 + 0.20 + 0.20 + 0.15 = 0.87 against 1.0. A3b now measures built fits.
- Fails, same class as before (a degree of freedom counted but not held):
  1. One square key in one T-nut is one contact point. Two points are what remove a translation and a rotation. With a 20 to 30 mm T-nut and a 0.25 clearance, the plate rotates by about 2 x 0.25 / 25 = 0.02 rad. At a 270 mm lever that is over 5 mm at the receiver. The 0.25 entry counts the translation only.
  2. The columns stand on the rail slot lines. Rails run along the slot, so each column foot slides along it. The drill axis position along the slot has no feature. Row 48 "0.20" bounds the across-slot direction only. The pin locates the plate along X; nothing locates the columns along X to the same end member.
- Invariant: every part located to datum C has a feature in each constrained direction, and the chain entry for each direction is the clearance of that feature as built, not a translation clearance with an unbounded lever.
- Single smallest edit, one sentence in line 13: "Every part located to C is located by two spaced contacts along its slot line: two plate keys, one each side of the receiver, and each column foot abutting the end-member stop line, with the foot's along-slot clearance added to row 48."
  - Budget check: foot radial sqrt(0.20^2 + 0.20^2) = 0.283, so total 0.32 + 0.20 + 0.283 + 0.15 = 0.953, still inside 1.0.
  - The column along-slot stop must bear on the frame, not through the printed plate, so A1d stays true and the plate carries no loop.

### U13: SIGNED
- Working stroke 500 (start 660 minus stop 160, and 800 minus 300). Park 950 is separate and reached only by the manual raise. The pin latch is on the column above start_z 800: metal, so the park weight path is carriage, latch, column, frame. No printed member.
- Numbers check: 150 + 750 + 50 = 950 (core bottom at the collar top while lowering); seated core top 790, clearance 160; 0.5 m load at 650; carriage range 950 - 170 = 780.
- For the human, not a topology matter: gate B6 reads "upper assembly travel at most 0.5 m". The 780 mm carriage range is stated as not working travel. The human confirms that reading.

### U14: SIGNED
- No overhead anchor, so no structural path exists. The strap is held by hand. The concept's own check (a rope from 300 mm off axis crosses z 950 at 21 to 59 mm, inside the 88.9 cutter radius) matches mine.
- Columns 548 centre to centre, 488 clear. Non-blocking: A1e names the parked envelope only. The 250 mm handle at carry position is also 244 mm from each column inner face in y. Keep it pointing toward the operator in x, or add the columns to A1e.

### U15: SIGNED
- Raise path: carriage, hoist, metal cross member (728 mm, metal brackets at both joints), columns, frame. No printed member (A2h).
- Jam path: hoist anchor, carriage, jammed cutter, core, collet, receiver, base plate, frame, columns, cross member. This loop closes through printed parts. It is bounded: shear link 300 N, less carriage weight 147 N, caps the core force at 153 N (stated 150), below the 204 N pull-out proven by H2. Above that the link breaks and no more load enters the printed parts. That is the fuse I asked for.
- Condition on H9: run the trip at the link's upper tolerance (at +10 percent, 330 N, the jam force is 183 N, still below 204 N).

### U16: SIGNED
- Lug is flush with the cutter lowest point, radius 95, and projects nothing below it. A2f is the swept-volume predicate: upper assembly to the stop has zero common volume with printed solids, base plate and wings included. With A2b (cutter 10 above the highest collar top) only the metal stop bears. The finger of the first pass is gone.
- Heights close: arm detent 350 and 600 above datum A (310 and 560 above the seat at floor 40), plus the 250 mm tower, gives 600 and 850. That equals core top + 60 at 0.5 m (540) and 0.75 m (790). Released arm and tower at radius 125 or more, 10 outside the wings (115).

### Decision 8: SIGNED
- The stop path is cutter, carriage, metal stop, columns, frame. The finger that violated it is withdrawn. A2c and A2d stand: no member of the printed set in the path, and no axial bearing on the core at the stop.

### Test IDs: WITHHELD
Bare A1 is gone. P6a is marked a document check. A6a, A6b, A6c, A1c, A1d, A1e, A2e to A2h, A3d, A3g, A3e, A3h, A3i, P6c, P6d are split and defined.

Line 108, A3h: "nut clamp shoulder bears on the washer with at least 1 pitch of nut travel left". Two predicates: a contact pair (shoulder to washer, class C) and a gap (skirt bottom to floor, at least one pitch). The contact is already in A1a.
- Smallest edit: rewrite A3h as "nut skirt bottom is at least 1 pitch above the receiver floor in every pose".

Same edit, orphans: A1d and A3g are defined and cited by no decision or ICD row. Cite A1d in the "Column feet" row (with A1c) and A3g in the U12 row (with A3d). H8 still says "finger gap trial"; read "stop gap trial".

Accepted as one predicate each: A1a, A1b, A1c to A1e, A2a to A2h, A3a (release reachable), A3b, A3c, A3d, A3e, A3f, A3g, A3i, A6a to A6c, P6b to P6d.

### Flip conditions (last pass)
1. Line 13 and row 48: the one sentence above (two keys bracketing the receiver; column feet abutting the end-member stop line; foot along-slot clearance in the chain, total 0.953).
2. A3h: skirt-above-floor only. Cite A1d and A3g.
