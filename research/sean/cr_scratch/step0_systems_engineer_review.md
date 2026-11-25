# Step 0 Systems Engineer Review (Wave 2)

**Verdict:** NOT APPROVABLE AS WRITTEN. Two BLOCKS APPROVAL findings, both on the axial load path in the decided configuration. The step skeleton is sound and the TDD machinery fits it; the gaps are interfaces and load paths that no sketch owns, plus back-edges in the sketch dependency graph that let an accepted sketch go stale.

**Counts:** BLOCKS APPROVAL 2; FIX BEFORE CLOSE 13; NOTE 3. Total 18.

## Answers to the review questions

| Question | Answer | Findings |
|---|---|---|
| Dependency order and output feed | Forward order S1, S2, S3, S4, S6, S5 is right for a first pass. Three back-edges have no rule: S4 sets the bottom of the S1 stack (taller collet, Q5, moves `stop.collar_top_z`, hence `stop.start_z` and park); S6 sets gear OD, motor envelope and ring mass that S1, S2 and S3 already plotted from ASSUMED overlay values; Step 2 decides members after S5 is drawn. Decisions are split between sketch specs and Step 2. | SE-7, SE-8 |
| Subsystem interfaces | Ring to nuts: drawn (S3), mounting stiffness undefined. Screws to frame: drawn (S3), frame continuity from anchor to guide unowned. Ring gear to drill tube: bore fit only; radial location and up-thrust undefined. Iris drive: callout and owner, correct for this week. Torque reaction: S6-3, chain closes on the wrong member. Collet and receiver to push-pop: S4. Cutter keep-out to ring: K7, per pose only. Ring lateral guidance: unassigned. | SE-1, SE-5, SE-6, SE-15 |
| Load paths | Axial 1000 N: assigned only at screw level (S3-1); the loop through drill, ring, frame, base and core is not closed anywhere. Spin torque: S6-3, loop wrong. Screw tension vs compression: S3-1, S3-2, good; length formula wrong. Drill weight on pinions: S6-4, good. Up-thrust from the cut: unassigned. | SE-1, SE-2, SE-3, SE-5 |
| One result | Objectives, week-done and Step 5 agree, with one split: Objective 7 and Step 4 execute shared-file changes before Quinn sees the configuration. | SE-10 |
| Superseded text | Handled consistently for arbor press, hoist, columns, twin screws, S3 per lift option (DN2, Objective 4, detail 1.3). Not handled: the metal descent stop (`upper.metal_stop`, DECLARED, gate B5), park latch, `icd.torque_reaction`, `icd.tipover_statement`, ASSEMBLY.md load path. These are neither in force (DN1) nor superseded (DN2). | SE-2, SE-4, SE-12 |
| Repository Sync and LLM-PLM | Params-first order, retirement record and the Quinn-folder test dependency are right. Gaps: ASSEMBLY.md names Quinn's cr_scratch file as its frozen authority; accepted sketches in `docs/` would import from Sean's research folder; promoted keys left in the overlay break K2. | SE-11, SE-13 |

## Findings

### SE-1. Drill-to-ring interface undefined: radial location and cut-case up-thrust. BLOCKS APPROVAL
**Location:** detail 1.5 (S6) Shows and checks S6-1 to S6-4; detail 1.3 load case "Cut: 1000 N up on the ring"; Design Notes 1 and 11; Open Questions.
**Problem:** The cut reaction pushes the drill up. DN23 and DN1 say the pinions carry drill weight, which is a downward load on pinions below the gear. Upward thrust lifts the gear off the pinions, or, if the gear is captured, passes 1000 N through the bevel teeth into three NEMA 23 shafts (about 333 N axial each plus mesh separating force), which motor bearings do not carry. Nothing in the plan locates the drill radially on the ring either: a bevel mesh centres nominally and is not a radial bearing; the support ring holds motor shafts, not the drill. S3 starts from "1000 N up on the ring" and assumes the load arrives there. The member that delivers it (a slewing or thrust bearing between drill tube and ring, or a collar on the tube bearing on the ring) is the central interface of the upper assembly and no sketch, check or open question owns it.
**Fix:** Add to S6 Shows: the drill-to-ring bearing (radial plus axial both directions) as a named feature. Add check S6-5, cut-case up-thrust chain: cutter, drill tube, tube collar or gear hub, bearing, ring; each pair class C (K7 C). Z: fixture from the spec. B: bearing removed so the chain runs only through the pinion teeth. Reported: axial and separating force per pinion in the static and cut cases. Add open question N4 "drill-to-ring bearing type and source", owner Sean, closes in S6 and Step 2. Add a Step 2 row for the bearing.

### SE-2. Axial load loop not closed; contradicts ASSEMBLY.md and changes the load on kept parts. BLOCKS APPROVAL
**Location:** detail 1.3 (S3) load cases and S3-1; detail 1.1 (S1); detail 4a seed list; Design Notes 1, 2, 12.
**Problem:** With a powered screw lift the cut force is applied by the screws and reacts through the work: cutter, core, collet core stop, collet foot, receiver floor, base plate, frame, screw anchors, screws (tension), nuts, ring, drill-to-ring bearing, drill, cutter. ASSEMBLY.md Load path says the 1000 N descent path is "cutter, carriage, metal stop, columns, frame" and never enters the nut, holder, collet, receiver or base plate; A2d sets drill-to-core axial force 0 at the stop. Under the decided lift that statement is false during the cut, and the kept parts (collet, holder, receiver, base plate) take weight on bit up to `loads.wob_max` 1000 N in a path they were not checked for. The plan lists the ASSEMBLY.md load-path bullets on the Step 4 change list, but no sketch derives the new loop, so Step 4 has nothing to write into them. A powered lift also generates thrust up to motor stall, independent of the cut (see SE-4).
**Fix:** Add check S3-3 (or S1-7), axial loop closed for the cut case: the chain above as a spec `chain` with every consecutive pair class C in the drawn figures (S1 for the base and frame members, S3 for anchor, screw, nut, ring). Z: fixture from the specs. B: anchor frame member drawn 1 mm clear of the base frame (loop open). Reported: axial force in each kept part at 1000 N and at the lift's stall thrust (NEMA 17 torque, T8 lead and efficiency stated, ASSUMED). Add `test_P10_assembly_load_loop_ten_members`, A2d and the ASSEMBLY.md descent bullet to 4a with disposition. Record in Design Notes that the base now carries the cut reaction (Sean confirms; Quinn informed in the question batch, SE-9).

### SE-3. Lift stroke conflated with travel; screw length formula short. FIX BEFORE CLOSE
**Location:** detail 1.3 Reported ("L = travel + nut length + ..."); Echo Site Registry; S1-4; Objective 5.
**Problem:** Travel 650 is the cutting travel (`upper.travel_max`, start to stop). The screws must also reach the loading park, which params defines outside working travel: `upper.park_stroke` = 959.84 - 184.84 = 775 mm today, and the re-derived park must clear the 0.75 m start at 965, so the stroke exceeds 780 mm if the 0.75 m class stays (Q9). DN23's 800 to 900 mm estimate was built on 650. With stroke about 780 plus nut, anchor and guide allowances and the ring nut housing, L lands near or above 900 mm. S1-4 checks nut travel at park and will catch it; the S3 formula reports a different number, so two sketches disagree on the same quantity.
**Fix:** Define lift stroke = park tip z - lowest stop tip z, maximum over supported core classes. Use it in the S3 L formula. Add "Lift stroke (park to lowest stop)" to the Echo Site Registry, DERIVED, separate from travel 650. S1 reports stroke and L for each Q9 option (0.5 m only; 0.5 and 0.75 m; plus 1 m), so Quinn's Q9 answer selects the screw length.

### SE-4. Descent stop and overtravel status undefined. FIX BEFORE CLOSE
**Location:** Design Notes 1 and 2; detail 1.1 (S1-1, S1-2 use `stop.*`); detail 4a (`upper.metal_stop` absent, `stop.*` listed); Step 2 rows.
**Problem:** `upper.metal_stop` is DECLARED (gate B5: metal descent stop owned by the upper assembly, rated 1000 N). `stop.height_z`, `stop.start_z` and `stop.g_stop` hang off it and S1 plots from them. The decided lift is powered, so descent ends where the controller stops it, unless a hard stop remains. A crash at stall thrust drives the cutter into the collar or core. The plan neither keeps nor retires the stop, and the park latch (`upper.park_lock`) has the same gap. Retiring a DECLARED key needs a human decision.
**Fix:** Add a Step 2 row "descent end: hard stop kept (form, location, rating against stall thrust) or replaced by limits (switch type, per-screw homing)". S1 draws the stop or states its absence in the spec. List `upper.metal_stop`, `upper.park_lock` and the strap keys in DN2 as "status set at Step 2", and put the metal-stop question to Quinn in the early batch (SE-9) since gate B5 is his.

### SE-5. Torque loop closes on the floor; drill torque against core holding torque unchecked. FIX BEFORE CLOSE
**Location:** detail 1.5, S6-3 chain and source; detail 4a.
**Problem:** S6-3 runs "... anti-rotation member, frame, floor". The jig is free-standing (R1); floor friction is not a designed member. The drill's cutting torque enters the core and returns through collet, receiver, base plate and frame to the anti-rotation member, ring, motor mounts and pinions. S6-3 cites `icd.torque_reaction` as its source, whose value is "not carried by the base": the check contradicts the key it cites. Separately, R15 holds the core at 10 N m; three NEMA 23 through a gear ratio can deliver several times that, and if drill torque exceeds the collet's holding torque the core spins in the collet.
**Fix:** Change the S6-3 chain to close through frame, base plate, receiver, collet, core, cutter. Source: Design Note 11 and this finding; mark `icd.torque_reaction` for REWRITE on the Step 4 list. Add to S6 Reported: maximum drill torque (NEMA 23 torque times ratio, DN23-b and -c open) against `loads.torque_design` 10 N m, flagged to Sean and Quinn when above.

### SE-6. Ring lateral guidance and nut mounting unassigned; ring overconstrained. FIX BEFORE CLOSE
**Location:** Open Questions N2; Objective 4; detail 1.3 (S3-2 K factor); detail 1.2 (S2-4 "outside sketch scope"); detail 2.
**Problem:** Three nuts fixed to the ring on three bottom-anchored, top-guided screws constrain the ring nine times for six degrees of freedom; any pitch-radius or parallelism error binds. If the nuts float to cure that, the screws stop guiding the ring laterally and S3-2 moves to K = 2 (P_cr about 43 N per the Software Engineer's numbers: static case fails). If the nuts are rigid, 850 mm T8 screws are the only lateral guide for a drill that must hold 1.0 mm coaxiality (R13) under cutting side load. N2 asks only for anti-rotation. The choice of what guides the ring is architecture and belongs in the sketch phase; S2-4 sets R13 aside as build tolerance.
**Fix:** Rename N2 "ring guidance: anti-rotation, lateral guide, coaxiality carrier". S3 spec states nut mounting (rigid or floating) and the K it implies; S3-2 uses that K. S2 and S6 draw the guide member (rails or rods, which may also be the anti-rotation member). Step 2 gets a guidance row whose reason cites R13. S2-4 note changes to "nominal; R13 carried by the Step 2 guidance row".

### SE-7. No rule for back-propagation into accepted sketches. FIX BEFORE CLOSE
**Location:** detail 1 common, step (h); detail 1.0 checks JSON format; detail 6.
**Problem:** Each sketch is accepted before the next opens, and later sketches edit overlay keys earlier ones plotted: S4 may raise `stop.collar_top_z` (taller collet, Q5), shifting every S1 height; S6 fixes gear OD, motor envelope and ring mass that S1 to S3 drew from seeds; Step 2 can change frame members. Only the S5 re-run after Step 2 is written down. Step 6 re-runs check_sketch on live params and overlay, so it catches numeric drift on the last day, after Steps 2 to 5 have cited the stale revisions.
**Fix:** Checks JSON records a hash of params.yaml and the overlay and the list of keys the spec reads. Add step (i) to detail 1 common: any overlay edit to a key an accepted spec reads re-runs check_sketch on that sketch the same day; a changed drawn geometry opens a new revision through M1 and M2. X2 checks and Step 6 compare hashes and fail on a stale accepted revision. Name the known back-edges in the S4 and S6 details.

### SE-8. Decision locus split between sketch specs and Step 2; S5 drawn before members are decided. FIX BEFORE CLOSE
**Location:** Steps table rows 1.3, 1.6, 2; detail 2; Design Note 5.
**Problem:** The S3 spec states a sync method and X2-2 checks the Step 2 record against it, so the sketch decides and Step 2 transcribes. Step 2 runs after S5, and any member it changes forces S5 through M1 and M2 again. Two places decide the same thing.
**Fix:** One rule: the sketch spec carries the option drawn, Sean decides at that sketch's M2 pass, and Step 2 consolidates and adds the rows no sketch carries (motor count, F_bind, bearing source, descent end). Move Step 2 ahead of S5 (order S1, S2, S3, S4, S6, Step 2, S5) so S5 places the decided members once. Record in Design Note 5.

### SE-9. Quinn's "ask early" items wait for Step 3. FIX BEFORE CLOSE
**Location:** Steps table rows 1.0 and 3; detail 3; Open Questions Q2, Q9, DN23-a to -e.
**Problem:** Start here says ask Quinn Q1 to Q3 early; critical-path 13.3 says before S1 is final. Q2 (drill length and mass) feeds S1 height, S3 buckling and the S6 weight chain; Q9 sets lift stroke (SE-3); DN23-b, -c, -d set the S6 geometry. The plan sends Quinn's batch at Step 3, after every sketch is accepted.
**Fix:** Add a question batch to Step 1.0 (or a Step 0.5 at gate approval): Q2, Q9, DN23-a to -e, the metal-stop question (SE-4), the base-carries-cut-reaction note (SE-2) and the Quinn-folder dependencies (SE-13). Step 3 becomes the closeout of that batch.

### SE-10. Shared design files change before Quinn reviews the configuration. FIX BEFORE CLOSE
**Location:** Steps 4 and 5 order; Objective 7; detail 4c; detail 5.1 (S tests count executed changes).
**Problem:** Sean leads and Quinn reviews. Step 4c promotes sketch-phase ASSUMED keys into params.yaml and rewrites or retires tests that encode Quinn's Step 2 to 7 design, then Step 5 writes the record Quinn reads. Quinn's week-done asks for the list; the scope asks for execution through LLM-PLM. Executing first gives Quinn a changed repo to review instead of a proposal.
**Fix:** Order 4a (change list), 4b (Sean approves), 5 (record carrying the proposed change list), Quinn's review on pull, then 4c (execution) and 6. If Sean wants execution before Quinn's review, record that choice in Design Notes at the gate. Adjust the 5.1 S tests from "executed" to "proposed" counts accordingly.

### SE-11. Accepted sketches in the shared location depend on Sean's research folder; promoted keys break K2. FIX BEFORE CLOSE
**Location:** Design Notes 6 and 7; detail 1.0 file list; detail 4c; detail 6.
**Problem:** An accepted script moved to `docs/sketches/` still imports `sketch_common.py` and reads `proposed_params.yaml` under `research/sean/cr_scratch/`. Quinn may not edit that folder, so a sketch he pulls is one he cannot fix. After 4c promotes overlay keys into params.yaml, K2 fails every accepted sketch on shadowing unless the overlay entries go, and Step 6 re-runs the checks after 4c.
**Fix:** At first acceptance, move the harness (sketch_common.py, check_stack.py, check_sketch.py, fixtures) and the overlay to the shared location together; accepted specs and checks JSON go with them. 4c deletes each promoted key from the overlay in the same change; Step 6 expects green with the reduced overlay. Sean confirms with Design Note 7.

### SE-12. Tip-over and bolt-down unassigned. FIX BEFORE CLOSE
**Location:** details 1.1 and 1.2; detail 2; detail 4a (`icd.tipover_statement` listed only for change).
**Problem:** `icd.tipover_statement` (old design) already requires bolt-down with the cutter above z 400 mm. The decided configuration puts ring, gear, three NEMA 23 and the drill at the top of a 780 mm stroke on a footprint S2 leaves open. R1 says free-standing. No sketch reports centre of mass or tip force.
**Fix:** S1 Reported: centre-of-mass height per pose and unbolted tip force at the top of the frame (masses from the overlay, ASSUMED). S2 Reported: footprint against that force. Step 2 row: bolt-down or footprint, with R1 named.

### SE-13. ASSEMBLY.md names Quinn's cr_scratch file as its frozen authority. FIX BEFORE CLOSE
**Location:** detail 4a, cross-contributor dependency; detail 4c (ASSEMBLY.md edits).
**Problem:** ASSEMBLY.md opens "Source: research/quinn/cr_scratch/step2_system_concept.md" and states the ICD table is frozen there. Step 4c edits ASSEMBLY.md ICD and load-path rows. The plan routes only test_P10_every_key_in_concept_icd_table_exists to Quinn. Editing ASSEMBLY.md while its declared authority stays in a file Sean may not touch leaves two sources disagreeing.
**Fix:** Extend the 4a cross-contributor item to the ASSEMBLY.md source line and ICD freeze statement: propose that ASSEMBLY.md becomes the authority for the redesigned rows (or a shared ICD file under `docs/`), and send it to Quinn in the early batch (SE-9) for a ruling before 4b.

### SE-14. "INSITU2 157-166" still cited. FIX BEFORE CLOSE
**Location:** Document Structure limitations table (line 78); Open Questions DN23-e (line 482).
**Problem:** The Software Engineer found the line range UNVERIFIED (the file has 12 lines; the claim is at lines 3 and 7). The two citations outside his sections still carry it.
**Fix:** Change both to "INSITU2 via [DN23]" to match detail 1.5.

### SE-15. K7 checks four discrete poses; the ring sweeps between them. FIX BEFORE CLOSE
**Location:** detail 1.0, K7; g_min seed "moving parts against fixed frame members, 10 mm".
**Problem:** The ring, gear, pinions and motors move continuously through the stroke. A fixed member (a frame tie, the top-guide member, a belt run) between two pose heights and inside the ring's plan outline passes K7 in all four poses and is hit in transit.
**Fix:** For each moving part, K7 also tests the swept envelope: in side views, the union of its outline from the lowest to the highest pose; in plan, the ring outline against every fixed member whose z band intersects the sweep. B: a horizontal fixed member at mid-stroke inside the ring outline, clear of all four poses, must fire.

### SE-16. Sync failure mode not addressed. NOTE
**Location:** detail 2, sync row; detail 1.3.
**Problem:** Open-loop steppers from one controller lose steps independently; one screw falls behind, the ring tilts and, with rigid nuts, binds. A belt link prevents it at the cost of the belt path (K7, K9 already cover the path).
**Fix:** The Step 2 sync row states how a lost step is detected or prevented (belt, per-screw home switches, re-level at park).

### SE-17. First human look at S1 comes after the whole harness. NOTE
**Location:** detail 1.0; detail 1 common, steps (a) to (g).
**Problem:** The critical path names the human as the detector of misconception (7.1). S1 reaches Sean after K1 to K9 with their fixtures, the spec, the stub run, the checks, cross-review and M1. If the jig is wrongly conceived, the harness work on S1 is spent first.
**Fix:** Allow an orientation preview: S1 r1 PNGs go to Sean for V1 to V5 only as soon as drawn, in parallel with cross-review and M1. It is not acceptance and records corrections in Design Notes 13 the same way.

### SE-18. Progress Log row 0 is stale. NOTE
**Location:** Progress Log, Step 0 row.
**Problem:** It lists the Software Engineer revision as pending; the Steps table row 0 says it is done.
**Fix:** Manager close updates the row.
