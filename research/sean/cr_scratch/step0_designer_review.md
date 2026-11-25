# Step 0 Designer Review (Wave 2)

**Verdict:** APPROVABLE AFTER FIXES. 0 BLOCKS APPROVAL, 10 FIX BEFORE CLOSE, 5 NOTE.

The plan builds the right mental model for its executor: one harness, six sketches in dependency order, a written rubric, controls on the reviewer, every correction routed to Design Notes 13. Its gaps are physical: the drill is drawn without a nose or a tail, one clearance check tests a pair that cannot touch, the ring is specified as an outline, nothing holds the ring when power is off, and the operator appears only as a sector in plan.

## Findings

### D1. Superseded lines in "Start here" carry no signpost where they are read. FIX BEFORE CLOSE
Location: Objectives (opening), against "Start here" lines "arbor-press-like stand", "Lift options are open: arbor press, twin jack screws ...", week-done bullet "A lift option is chosen, or narrowed to two".
"Start here" must stay byte for byte, so the retirement lives in Design Notes 2, 300 lines below. An orchestrator after compaction reads "Start here" first (CLAUDE.md order) and meets three live-sounding options before any retirement.
Fix: one line at the top of Objectives: "These Objectives govern. In 'Start here', the lift-options line and the week-done bullet 'lift option chosen or narrowed to two' are superseded by Quinn's update in the same section and by Design Notes 2; 'arbor-press-like' describes the motion only."

### D2. Progress Log row is stale. FIX BEFORE CLOSE
Location: Progress Log, Step 0 row: "Pending: Software Engineer TDD revision, ...".
The Steps table row 0 says the revision is done. Two status statements for one step disagree.
Fix: rewrite the row at Engineer revision and again at Manager close; list completed passes and the gate items.

### D3. "INSITU2 157-166" cites lines that do not exist. FIX BEFORE CLOSE
Location: Document Structure, Known limitations table row 4; Open Questions row DN23-e.
`context/literature/INSITU2_text.md` has 8 lines. The Software Engineer flagged the range UNVERIFIED and corrected his own sections; the two Engineer-owned sites still carry it. Quinn's DN23 carries the same range; Sean's file may not edit Quinn's, but need not repeat the error.
Fix: both sites read "INSITU2_text.md via Quinn DN23 (line range UNVERIFIED; claim at lines 3 and 7)". Add the discrepancy to the Step 3 batch to Quinn.

### D4. The drill has no nose and no tail. FIX BEFORE CLOSE
Location: Detail 1.1 "Shows" ("drill tube (rectangle, 152.4 wide)"); Detail 1.5 "Shows"; K8 seed predicate "drill head below the gear"; M1 rubric V3; M1 reviewer control B1 (drill tip-up).
A uniform 152.4 x 800 rectangle is symmetric end for end. Flipped, it looks identical, so V3 cannot fail, the K8 predicate has no head feature to read, and the B1 reviewer control is a figure identical to its Z. This is the exact defect critical-path 7.1 exists to catch. Second issue on the same part: 152.4 is the tube OD, used as a keep-out; the 6 in cutter OD is unknown (params `drill.tube_od` source: "NOT a cutter OD"; Quinn Echo Site Registry row "Tubing"). A drawn head labelled 152.4 would state a cutter size nobody declared.
Fix: S1 and S6 specs carry a drill head feature (iris and cutters, from `drill.kerf_standoff` and `drill.dome_pole_offset`, head OD as an overlay key ASSUMED, labelled "cutter OD ASSUMED") and a top-end hardware block (overlay, ASSUMED, Q2) as separate spec rows with distinct shapes. The tube label reads "tube OD 152.4 (keep-out basis)". K9 then requires both features; K8 reads head z below top z.

### D5. S1-5 tests a pair that cannot touch, and misses the pair that can. FIX BEFORE CLOSE
Location: Detail 1.1, check S1-5; K7 g_min seed "Ring and gear against the 0.5 m core top at end of capture: G, `stop.g_stop` 25".
At end of capture the core is inside the drill tube; the ring and the gear are outside it. Moving the ring to mid-drill (the B fixture) changes nothing about core-top clearance unless something closes the bore. The two real clearances at end of capture are: (a) core top against the drill's internal ceiling (top-end hardware or any bore-closing part, Q2); (b) the ring, gear, pinions and NEMA 23 motors at their lowest position against the fixed base parts: collet, holder, wing nut (230 mm span, `wingnut.*`), receiver and frame. (b) is where a low-mounted ring crashes; (b) also sets the lower bound of N1 (ring position on the drill).
Fix: replace S1-5 with S1-5a (core top below drill internal ceiling, g_min 25, `stop.g_stop` reuse ASSUMED; B: drill internal length shortened below `upper.drill_advance_500core`) and S1-5b (lowest ring-assembly outline against base parts, K7 G, 10 mm; B: ring position at the drill's lower third). Update the g_min seed list to match.

### D6. The four poses are named and undefined. FIX BEFORE CLOSE
Location: Detail 1.1 ("One figure per pose: load, start of cut, end of 500 mm capture, park"); K6 (`z_rule` per pose); S1-2, S1-3.
`upper.park_z` source calls the park "a loading position". S1-3 tests load clearance at park. No line states what distinguishes the load pose from the park pose, or which core class the start pose uses (`stop.start_z` has two values, 834.84 and 965). K6 evaluates a `z_rule` per pose; the orchestrator cannot write one for a pose without a definition.
Fix: a pose table in detail 1.1: pose, tip z expression (params keys), core drawn, purpose. Example: load = park height with the 0.75 m core mid-insertion; park = lift at the re-derived park height, held (see D8), no operator task; start = `stop.start_z[0]` with the 0.5 m core (and `[1]` dashed for 0.75 m); end of capture = `stop.height_z`. Sean confirms at the S1 spec.

### D7. The ring structure is specified as an outline: a placeholder at params level. FIX BEFORE CLOSE
Location: Detail 1.0, overlay seed `ring.*` ("structure outline, position along the drill, mass"); V7 ("ring structure as a structure").
The ring is the one new part every load passes through. LLM-PLM 8.4a: a parameter set that describes a functional part as an outline is a design failure caught at params level. As seeded, the review at 1.1(a) has nothing to fail.
Fix: seed `ring.*` with its functional features: three lead-screw nut housings at `jackscrew` pitch radius and azimuths; three NEMA 23 mounts at `pinion` azimuths with the phase from S2; central clearance bore over the gear and `icd.keepout_radius`; gear and support-ring seat; anti-rotation interface (N2); material and form (plate, printed, or 30-6060 triangle; ASSUMED, Sean). State in 1.1(a) that the Designer fails a ring spec lacking any of these.

### D8. Nothing holds the ring when the steppers are unpowered; two DECLARED functions are retired without replacement. FIX BEFORE CLOSE
Location: Detail 1.3 "Shows"; Detail 2 row list; Detail 4a seed keys `upper.park_lock`, `upper.metal_stop`.
The load pose puts the operator's hands under a ring carrying the drill, gear and three NEMA 23 motors (about 25 kg per the Software Engineer's own estimate). The lead of the T8 screws is unstated; the common T8 brass-nut class has an 8 mm lead and back-drives. Power loss or a disabled driver then lowers the drill onto the core or the operator's hands. The old design answered this with `upper.park_lock` (pin latch, visible flag) and `upper.metal_stop` (metal descent stop, 1000 N, "the nut is never a stop", DECLARED at gate B5). The plan lists both keys for retirement and names no function that replaces them. A third failure mode follows from three motors on one axis: one motor loses steps, the ring racks and binds on the screws.
Fix: Step 2 gains rows: power-off hold (screw lead, brake, or park pin with visible state), end-of-travel hard stop and its load path, homing and step-loss detection across three screws. S3 Shows the lead (overlay `jackscrew.lead`, ASSUMED) and the hold device. Detail 4a marks `upper.metal_stop` and `upper.park_lock` as DECLARED or human-flagged functions that retire only on Sean's recorded ruling, with the replacing function named.

### D9. The operator appears only as a sector in plan. FIX BEFORE CLOSE
Location: Detail 1.2 (S2-5 operator sector); Details 1.1 and 1.4; M1 rubric.
The plan never walks the operator through a task. Missing: lifting a 0.75 m core (15.6 kg, Quinn Echo Site Registry) into a collet near the floor (collar top 159.84) under a parked ring; changing a collet (wing nut, 230 mm span, beneath the ring and between screws); advancing the core for a slice and taking the slice off; removing the 500 mm captured core from the raised drill (no step owns this); where the operator stands during a cut and what they see; pinch points at three exposed pinions and a turning ring gear at chest height during the cut.
Fix: an operator task table in detail 1 common: task, pose, sketch, reach height, sightline, hazard, check or rubric item. Assign load and collet change to S1 load pose and S2; slice advance and slice removal to S4; captured-core removal to Open Questions (new N4, owner Quinn, tied to DN23-e). Add rubric item V10: "the operator can reach and see each task drawn in this sketch; hands are clear of moving parts in the load pose".

### D10. No orientation predicate for the kept base parts. FIX BEFORE CLOSE
Location: Detail 1.4 (S4 checks); K8 seed set.
Critical-path 7.1 records the backcap failure: a part drawn upside down. The kept parts (collet, holder, wing nut, receiver, washer) are cones and threads, the parts most likely to flip. K8 seeds cover drill, screws, gear and plan handedness; none covers S4. V4 checks only the core.
Fix: S4 spec carries K8 predicates: collet taper sense per `cone.alpha` (narrow end as in ASSEMBLY.md), wing nut above holder, washer between nut and holder, receiver floor at the bottom. B fixture: collet flipped end for end.

### D11. Sub-step numbers and sketch numbers diverge at 1.5 and 1.6. NOTE
Location: Steps rows 1.5 (S6) and 1.6 (S5); Context Recipes ("1.1, 1.2, 1.3, 1.5").
Labelled correctly everywhere checked, but "1.5" invites loading S5. Fix: write "1.5 (S6)" and "1.6 (S5)" in every Steps row, recipe and cross-reference.

### D12. Echo Site Registry: one status wording and missing rows. NOTE
Location: Echo Site Registry.
T8 800 to 900 mm reads "DECLARED range"; detail 1.3 treats it as Quinn's estimate, reported and never asserted. Both are true; say so: "DECLARED estimate (DN23); reported, never asserted". Values used in three or more places with no row: core mass 10.4 kg (0.5 m) and 15.6 kg (0.75 m); 0.75 m install core; drill advance 534.93; start z 834.84 / 965; footprint 644 x 608 (open); on-hand stock list; cutter OD unknown (152.4 is tube OD). Add them.

### D13. M2 summary has no author or path. NOTE
Location: M2 ("a one-screen checks summary").
Fix: `check_sketch.py` writes `sN_summary_r<k>.md` beside the JSON.

### D14. Rubric applicability per sketch is unstated. NOTE
Location: M1 rubric; Details 1.4 and 1.6.
V1 to V6 have no object in the S5 stock map; V2 and V5 have none in S4. A reviewer forced to mark them invents a result. Fix: one line per detail block naming the V-items that apply.

### D15. S3 redefinition against critical-path 15 wording. NOTE
Location: Design Notes 4; Detail 1.3.
Critical-path 15: "S1 and S3 draw the ring and three screws." The redefined S3 is a section through one screw; the sync check (K9 pulleys at all three screws) needs all three. Fix: DN4 states S3 is a one-screw section plus a plan inset of the three screws and the sync loop, so Sean confirms against the section 15 sentence.

## Echo-site check (requested values)

| Value | Gameplan sites | Critical-path 14 / 15 | Result |
|---|---|---|---|
| Travel 650 mm | Obj 3, DN1, S1-1, Echo | R6, §15 | Agree |
| Drill about 800 mm, ASSUMED | Overlay seed, Q2, Echo, limitations table | R8 ASSUMED | Agree |
| Capture 500 mm | Obj 5, S1, Echo | R7 | Agree |
| Three screws, three pinions, 120 deg | Obj 3, DN1, S2-1, Echo | §15 | Agree |
| T8 800 to 900 mm | DN1, 1.3, Echo | §15 | Agree in value; status wording D12 |
| 1000 N axial | S3 load cases, Echo | R14 ASSUMED | Agree |
| 152.4 tube, 86.2 keep-out | 1.1, K7 seeds, Echo | §10 | Agree in value; cutter-OD labelling D4 |
| 2000 mm soft | K1 B2, reported values, Echo | R17 | Agree; never asserted |

## Manager close checklist

- [ ] Objectives open with the governing line naming the superseded "Start here" lines (D1).
- [ ] Progress Log Step 0 row matches the Steps table (D2).
- [ ] No "INSITU2 157-166" left in Sean's gameplan; discrepancy in the Step 3 batch (D3).
- [ ] S1 and S6 specs list a drill head and a top-end block as distinct features; tube labelled as tube OD; cutter OD ASSUMED (D4).
- [ ] S1-5 replaced by core-top-to-drill-ceiling and ring-to-base-parts checks, each with Z and B (D5).
- [ ] Pose table with tip z expression and core per pose in detail 1.1 (D6).
- [ ] `ring.*` seed names nut housings, motor mounts, clearance bore, gear seat, anti-rotation interface, material (D7).
- [ ] Step 2 rows for power-off hold, hard stop, homing and step loss; `upper.metal_stop` and `upper.park_lock` retire only on Sean's ruling (D8).
- [ ] Operator task table and rubric V10; captured-core removal owned in Open Questions (D9).
- [ ] S4 K8 orientation predicates for collet, nut, washer, receiver with a flipped-collet B fixture (D10).
- [ ] NOTE items D11 to D15 applied or recorded in the Engineer's disposition table.
- [ ] Header, "Start here" and "Repository Sync" byte-identical to the Step 0 open copy.
