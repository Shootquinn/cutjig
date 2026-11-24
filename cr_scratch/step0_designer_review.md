## Verdict

Not yet a part I would put my name on. The mechanism concept is sound (a cone collet closed by a nut, release by cone angle or capture, hard stop on stroke). The physical design the plan commits to still has four defects a user would hit in the first hour: the clamp probably cannot hold the core against the iris torque, the wing nut is both the thing the operator tightens and the thing the cutter crashes into, the wrong-collet defence is a label, and the operator needs three hands to load a 9 kg core. The Designer is also placed at the wrong CAD steps: there is no params review before geometry, and several functional features have no parameters at all.

Sources: workorder.md, the Software Engineer draft, Systems Engineer, Loftsman, Topologist and Fact-Checker reviews, the extraction file, the stock file, llm_plm_cad.md 8.4. Text-only: no visual gate was run. Numbers I quote are the reviewers' (PROPOSED or UNVERIFIED as they marked them); I did not derive new ones.

## Findings, ranked by severity

### Critical

**D1. The clamp cannot hold the core, and nothing in the design stops the core from turning.**
- Loftsman 5.1: hand-tight on two wings (12 N m at the nut) gives about 250 N axial and 7 to 8 N m holding torque. The placeholder load is 20 N m. Systems Engineer S1 gets single-digit N m by an independent route. Two reviewers agree; no one disagrees.
- The anti-rotation key in F5 keys the holder to the boss. Nothing keys the core to the collet. The only thing that stops core rotation is friction of concrete on printed PETG.
- A rotated core is not a nuisance: the stratigraphy order is the test measure (extraction section 6). A slipped core is a failed test and a destroyed specimen.
- Cause is geometric: the thread has to wrap the holder, so it sits near 135 to 165 mm diameter and gives 21 N of clamp per N m (Loftsman). The "very large wing nut" is large because the thread is large, not because it gives leverage.
- The plan cut the wing-nut moment-arm check as ceremony (Detail 6). It is the only check on whether the jig does its job. Reinstate it (Loftsman T7) and write the number into the Step 1 gate, not Step 9.
- Design response to put in params now: a core liner (TPU or silicone sleeve) in the collet bore for friction, a thrust washer pocket, a tommy-bar socket in the nut, and a stated required holding torque with a source or an assumption label. If the liner and washer do not close the gap, a positive core lock (set screws through the holder onto a band, or a second clamp) is the escalation. Decide before Step 3.

**D2. The wing nut is the clamp and the crash target.**
- Reviewers: the boss thread major is 135 to 165 mm (Topologist 3.1, Loftsman 2.3), so the nut OD is about 150 to 181 mm, wider than the 146.05 mm tube bore. A2 branch 2 is forced: the nut is the hard stop (Topologist E-6, Loftsman 7.3).
- Systems Engineer S5: a 1000 N descent load through a printed nut and printed thread is the weakest path in the jig.
- Designer's reading of the conceptual model: the operator turns the nut to grip, and the user's model of "nut" is "adjustable, tighten and loosen". Making it also the end-of-travel the drill slams into gives two jobs to one part. A cracked nut drops the core clamp and the stop in one failure. Separate them.
- The stop belongs to the descent assembly (Step 10 already lists "end stop above the wing nut"): a carriage stop on the columns. The nut then needs a gap to the cutter face, not a rated load. State this in the Step 0 plan as a decision, not a Step 5 test branch. Delete `nut_is_stop` as a free choice.
- Caution on the Systems Engineer's alternative (a metal stop on the frame): the cutter tube sits at radius 73.0 to 76.2 mm and the nut wraps out to 90 mm or more, so a frame post outside the nut is never touched by the tube. The metal stop has to be on the drill side or inside the nut radius. This is a Step 10 interface item. Record it in the interface table (Systems Engineer S6).

**D3. The Designer gate is at the right two steps but is missing a params review, and the params do not yet describe a real part.**
- llm_plm_cad.md 8.4a requires a Designer params review before sketch geometry, asking whether a parameter set describes a real part. The plan has no such step. Step 1 writes a seed `params.yaml` and Step 2 fills the numbers; the first Designer touch is the Step 4 completeness gate, after the scripts exist.
- The Loftsman (section 10) lists parts with "no geometry at all": anti-rotation key or flat, debris tray and drain, core stop, engraved label, wing nut planform ("very large" only). The plan's F5 test then checks those features by "nonzero removed or added volume". A key defined by nothing but a volume is the pressure-plate-as-flat-ring failure that 8.4a names. This is a params-level design failure under my gate and the plan walks into it.
- Detail 4 required-features list omits features that the reviews show are functional: boss register (pilot), holder flange and bearing recess for a thrust washer, collet slit relief holes, the hard-stop gap between holder flange and boss rim, lead-in chamfers, tighten and loosen arrows, a collet caddy, an alignment gauge (Systems Engineer S6), and any lift or steady-rest aid for the core (D5). Add them to the Step 4 list or the exploratory gate will pass an incomplete part.
- Fix: see "Gate placement" below.

**D4. Wrong-collet defence is a printed number.**
- Detail 7: engraved core diameter, checked manually on a render. W6 in the Topologist table adds the 4x4 F3 sweep (a CAD check, not an operator defence).
- At 2.5 mm family spacing (7 collets: 90, 92.5, 95, 97.5, 100, 102.5, 105) two neighbours differ by a diameter the eye cannot see. A 3D-printed engraving on a curved cone face, 0.4 mm nozzle, will be hard to read.
- Physical constraint already present: a core larger than the bore will not enter, so the too-small collet self-rejects. Good. The failure is the too-large collet: the core drops in, the nut runs down, the hard stop (Loftsman G10) arrives with the collet still open, the nut feels "tight" and the core is loose and upright. The operator sees a nut at its stop and believes the core is clamped. Nothing signals otherwise.
- Selection rule is not stated. With real cores in a tolerance band (UNVERIFIED +/-1 mm), each collet's grip window is about 2.5 mm wide (Loftsman 4.3). The operator must select by measured core diameter, not by "this is a 100 mm core". The label "92.5" is then misleading. Engrave the grip window ("91.3 to 93.8") and say "measure the core, pick the window".
- Poka-yoke set to specify now, in the order I would apply them:
  1. Collet caddy (printed rack with seven sockets, each engraved or colored the same as its collet and labelled with the window). Mapping beats memory.
  2. Color per size on the filament, plus a raised notch count on the collet rim (tactile, colorblind-safe), plus the engraved window. Three signifiers; any one survives a bad print.
  3. Witness mark: a sight line on the holder flange that meets a scale on the boss rim at a clamped-on-range core. If the flange is at the stop and the line is outside the zone, the core is wrong or the collet is wrong. This is the feedback the plan lacks. It is cheap (a printed tick).
  4. Calibrated stop gap per collet: do not share one hard stop across the family if the clamp is meant to engage before the stop for any in-window core (stack height is independent of d, Loftsman 4.1, so one stop is geometrically fine; the signifier is what changes).

### High

**D5. Loading and handling the core is a three-handed job, with pinch points and sharp edges.**
- Release pose leaves 1 mm radial clearance per side on a 30 mm grip height: free tilt 1.9 degrees, 16.6 mm at the top of a 500 mm core (Loftsman section 6). The core mass is up to about 9.4 kg (DERIVED, upper bound). The operator holds the core upright with one hand, reaches over a 165 mm tube to find the nut with the other, and turns it. The plan has no steady rest, no handle, no cradle. The plan deferred this to Step 10 (E6) with no owner.
- Fix candidates for Step 2 to evaluate: a taller holder or a second guide ring to lengthen the grip, a removable V-guide or cradle on the frame, a lifting strap point. Pick one; do not leave the core to the operator.
- Pinch points:
  1. Holder flange to boss rim gap closes from about 6.3 mm to zero as the nut runs down (Loftsman 3.2). A hand steadying the holder is in that gap.
  2. Wing sweep at radius about 115 mm: wing to frame, wing to tray lip, wing to a hand resting on the base. The wings are the dominant moving edge.
  3. Slit closure (1.5 mm relaxed to 0.5 mm minimum clamped, T5) at 12 or 20 slits: skin in the slit.
  4. A 9 kg core dropped the last millimetre onto the core stop.
- Sharp rock edges: the cut and cast core ends are not specified (no wrap or sleeve, extraction section 6). Collet lead-in chamfer and a radiused bore lip are function, not cosmetic. Step 7 says "chamfers and fillets where they serve function": state in the gate that every operator-facing edge (wing edges, flange edge, slit edges, collet mouth, tray lip) counts as function.
- Debris: the nut and thread sit under the cutter and in the rock-dust path. Grit in a printed trapezoidal thread kills clamp feel and wears the thread. A shroud or skirt on the nut and a closed top on the boss thread region is a design item for Step 4, not a Step 9 surprise.

**D6. Release is undefined, and a jammed collet around a stratigraphy core is unrecoverable.**
- Loftsman 3.1 and Topologist S16 agree: a cone half-angle below atan(mu) (about 19 to 27 degrees for PETG on PETG, UNVERIFIED) self-locks; backing off the nut leaves the collet wedged. Systems Engineer S2 adds the same from the force loop. T5 asserts a "release pose" and does not say what produces it.
- Two ways out: a steep cone (about 20 degrees, costs radial room and about 28 percent of holding torque, Loftsman) or a captive-flange nut that lifts the holder on back-off. These pull against D1: the steep cone worsens the holding-torque deficit. The captive nut is the better trade for this jig because it preserves the shallow cone's mechanical advantage and gives a positive release. Cost is two bearing faces in print. Decide in Step 2 with the coupon, not in Step 7.
- Add a jacking provision regardless: two M6 jacking holes or a pry slot on the holder flange that push the collet free. A jammed core is the one case where a user will reach for a screwdriver and crack the flange.
- Recoverability checklist for the gate: over-travel limited by the hard stop (this is the best poka-yoke in the plan, keep it); nut can be removed with a stuck collet; a cheater bar cannot exceed the stop load; a broken wing does not drop the core (the core sits on the core stop).

**D7. Thread signifiers and cross-threading at 135 to 165 mm.**
- Topologist 4.3: cross-thread register length of about 54 mm for D = 135 mm, longer at 165. That is not a reasonable boss. The nut can instead be centred on the holder flange (already coaxial with the cone) and the holder centred in the boss bore: a stacked register uses features that already exist. Loftsman to confirm numbers. A single-start 8 mm pitch thread at 165 mm diameter has a 0.9 degree lead angle (Loftsman 5.1) and no start-point cue for the operator, so the register is the only defence.
- Signifiers missing from every part list: TIGHTEN arrow and direction on the nut top (clockwise, Topologist 4.1), a witness line (D4), a bearing-face recess that shows a washer is expected, a visible key on the holder and matching slot on the boss so the holder cannot go in rotated wrong (W2). The key marks must be asymmetric (Topologist Rule P) so a flipped part is visibly wrong.
- Over-torque on printed threads: the failure mode is not thread shear at 1000 N (Loftsman 2.1, margin large); it is wing root bending (15 MPa at 150 N abuse, safety factor about 3, Loftsman 7.2), PETG creep at the bearing face, and the thread wearing in a one-day hold. The hard stop bounds the clamp force on the collet. Keep the stop; do not build a second, harder one in the nut.
- Print orientation: wings must print in-layer (vertical fin, axis vertical), threads axis vertical, 45/45 flanks (Loftsman G2). State print orientation per part in the part params so the production gate can check it.

**D8. Base stability and tip resistance are not designed.**
- The "Christmas tree stand" gets its stability from wide low feet. The plan's base is a printed plate on a perimeter frame cut from 644, 488 and 468 mm stock (Design Notes). The footprint is chosen by the stock bin, not by a load case. No feet, no leveling, no floor or bench anchoring, no mass, no tip-over statement.
- Loads: WOB downward goes into the frame; a 20 N m torque (placeholder) must be reacted at the floor; the later 1540 mm column puts a tipping moment on the same footprint (Systems Engineer S6 item 5). A free-standing frame with a top-heavy drill is a tip-over hazard on first use.
- Specify now: footprint minimum from a stated lateral load at a stated height (even if placeholder), four adjustable feet or bolt-down slots, a mass target. Record in the interface table. Without it Step 10 inherits a footprint it cannot change cheaply.
- The base plate itself: the boss is a tube of 135 to 165 mm OD on a printed plate; the plate must fit the 256 mm bed minus 5 mm (T6), leaving about 43 mm per side beyond a 165 mm boss. A tray and drain on that plate is tight. State the plate dimensions in params.

### Medium

**D9. Gate wording.**
- Step 7 gate question is "would a printer operator produce a functional part?". That tests printability (Step 6), not pride. The pride test is: would the Designer show this to a client, could a lab technician who has never seen it load a core correctly, and is every error either impossible or recoverable. Replace the question and attach the checklist below.
- Step 4 gate question "can we learn from this?" is acceptable for exploratory. The gate must also check the completeness list in D3 or it passes parts with absent features.
- The Designer is assigned image-reading gates (Step 4 renders, Step 7 renders, A5 four-view) and I run text-only here. Llm_plm_cad A.3.1 requires an image-capable reviewer for render critique; Step 5 says so, Steps 4 and 7 do not. Add it to both.

**D10. Signifiers for state, not only identity.**
Open/closed state of the clamp has no signifier other than the nut position. Witness line (D4) and a printed gap gauge address it. Add them to the exploratory list.

### Low

**D11.** "Boss" for a 135 to 165 mm OD tube is a misleading name (a boss is a stub). The workorder uses it, so keep it, but the report must define it once at first use as a tubular receiver. The Christmas tree stand comparison is a conceptual model that belongs in the report as one sentence, not as a design claim.

## What the reviewers' findings do to the stated intent

**Thread near 135 to 165 mm, tube boss.**
- "Threaded boss rises from the base to seat the collet" survives, as a tube receiver that the collet sits inside. The tree-stand analogy is arguably stronger: a cup (tube) holding a central object, clamped from the side. What fails is the user's expectation of a small boss and a handy nut.
- The base is dominated by this one feature: boss OD 165 mm, nut about 181 mm, wing span about 230 mm on a 256 mm bed. The part is large for FDM, slow, and warp-prone. State print time and warp as a risk in Step 6, not as a note.
- Topologist (135) and Loftsman (165) differ by 30 mm because of different cone half-angle and wall assumptions. The registry must not carry either as authoritative until Step 2 chooses the angle and walls. See "Echo site registry".

**Wing nut is the hard stop.**
- "Very large wing nut" survives in size (about 181 mm body, 230 mm span, both fit the bed minus 5 mm). It does not survive as a design: it cannot be both the clamp and the crash target. Recommendation D2: the nut keeps its size and loses the stop job.
- Size alone does not give leverage; at 165 mm thread diameter the clamp force per torque is poor. Large is a cost (bed, weight, print time), not a benefit, unless the wing arm and the thrust washer pay it back (D1).

**Collet family at 2.5 mm spacing.**
- Intent "a separate collet per diameter" survives as 7 collets (Loftsman 4.3). Slit count drops from about 20 (5 mm spacing) to about 12; that is better for hand clamp feel and stress.
- It raises the wrong-collet risk (D4) and the print count (seven collets, a caddy, seven labels). It also moves the user-facing question from "which diameter" to "which window".
- The thesis, Detail 3, A1 ("4 matrices"), C8, F3 ("four nominals"), file names `collet_090` to `collet_105`, the BOM and the report all say four. These are echo sites; see below.

## Gate placement (part b)

| Step | Current Designer role | Finding | Change |
|---|---|---|---|
| 1 | None | The seed params.yaml is written with no design review | Designer params review of the seed (8.4a), non-blocking, recorded in `cr_scratch/step1_designer_params.md`. Ask only: which functional features lack a specification? |
| 2 | None | The numbers that fix the boss diameter, cone angle, release method, slit count and stop are derived here and nobody judges whether the result is a real part | Designer params review of the Step 2 output before Step 3 opens. Blocking for this project: D1, D2, D3, D6 must have an answer in params. |
| 3 | None | Fine | No gate. |
| 4 | Gate: completeness | Required-features list incomplete; no Design Critique deliverable; render read needs an image-capable reviewer | Add a Designer Design Critique output (8.4c) with design notes. Gate on the completeness list (below). |
| 5 | A5 visual | Fine | Keep. Rubric must include the signifiers (arrows, witness line, caddy) and pinch points. |
| 7 | Gate: quality | Question is about printing, not pride | Replace with the production checklist (below). Image-capable reviewer for renders. |
| 9 | None | The human prints and reports; no Designer input to what is asked | Designer writes the print-review form: clamp feel, wing grip, loading the core, wrong-collet trial, jam and release, pinch points. Results feed back as a change order. |
| 12 | Structure | Fine | Keep. |
| 16 | Wave 2 | Fine | Keep. |

**Exploratory completeness checklist (Step 4).** Gate fails on any missing item.
- Boss tube: thread with lead-in and land, floor seat for collet, register for the holder, asymmetric key slot.
- Holder: cone, flange, bearing recess for thrust washer, key, jacking holes, hard-stop face.
- Collet: cone, bore, slits with relief holes, foot key, core stop, rim notches, label, lead-in chamfer.
- Wing nut: thread, bearing face, wings with planform, tighten arrows, tommy-bar socket, dust skirt.
- Base: plate, tray, drain, slotted mounting holes, T-nut provisions, feet or bolt-down.
- Frame: members and brackets from stock, with the stock allocation.
- Accessories: collet caddy, alignment gauge, steady rest or cradle, witness scale.
- The stop: either on the descent assembly interface (preferred) or the nut, marked as a hard stop with its rating.

**Production quality checklist (Step 7).**
1. Pride: would the Designer show the part to a client without apology?
2. Cold-user test: can an operator who has not seen the jig load a 90 and a 105 mm core correctly from the part marks alone?
3. Poka-yoke: each W1 to W11 defence exists as a feature, not only as a test (Topologist section 9).
4. Signifiers: identity (label, color, notch), direction (arrows), state (witness line).
5. Recoverability: jam release, over-travel bounded, broken wing leaves the core supported.
6. Operator-facing edges and pinch points reviewed individually.
7. Print orientation and wing layer direction stated per part.

## The gameplan as a document (part c)

### Step clarity and executability

| ID | Severity | Finding |
|---|---|---|
| G-1 | High | Step 9 has no Detail. The plan's only physical test of the product is the human's first print, and it is a one-line table row. Systems Engineer S7 gives the protocol; write Detail 9 with the form (see Gate placement). |
| G-2 | High | Step 1 writes the whole CAD suite before Step 2 supplies the force loop, release method, slit design and thread. Systems Engineer S8 and Topologist TP-10 say the "reversal changes data, not tests" claim is false. Agree. The operator cannot execute Step 1 as written without guessing. Split into 1a and 1b around Step 2. |
| G-3 | Medium | Step 1 lists five test modules and says "no catch-all"; Detail 6 names `tests/test_printability.py` as a sixth, "part of" two others. Either it exists or it does not. Pick one. |
| G-4 | Medium | Objective 2 says "built from a single parametric generator". Detail 3 describes one collet generator plus per-part scripts. Say the spine is params.yaml plus common.py (Systems Engineer S8). |
| G-5 | Medium | Document Structure contains a change note: "(the draft said Step 11 here and Step 12 in the table; Step 12 is correct, the suite is Step 11)". That is revision history inside the contract. Move it to the Progress Log or delete it. The same applies to the "Cut from the draft" lists in Details 1, 6 and the CAD spec footer, and the "Software Engineer changes" section: history, not plan. |
| G-6 | Medium | Many steps depend on external references (A.4, A.10 item 2, A.14, A.15, A.16, 7.2, 7.6, 5.2.1). The plan does not say what they require. An executor without the operational guide cannot act. The Context Recipes list the guide, so this is acceptable; add the one-line rule where a step turns on it (A.4 geometry cross-review, A.10 item 2 source gate). |
| G-7 | Low | Step 0 row says "The Designer" without saying what at Step 0. State: reviews physical intent and gate placement (this file). |

### Report structure

- **One-sentence point.** The sentence promises that the frame "holds any 90 to 105 mm Mines core upright and coaxial" and that "every number in the design traces to a source or a test". The register lists torque, core tolerance, core length, iris aperture and printer as UNVERIFIED; the jig is designed to hold, not verified to hold (D1). The sentence also says "four-collet family", which Loftsman and Topologist put in doubt. At 49 words it is a run-on. Proposed shape: "A 30-6060 frame with a printed tubular receiver, wing nut and collet family is designed to hold a 90 to 105 mm core upright and coaxial under the 6 in drill; CAD tests verify the fit, and three inputs (torque, iris aperture, core tolerance) are open." Systems Engineer S9 reached the same overclaim.
- **Shape.** Lead-first is right for the stated readers. Page 1 lacks the decision or request: what the program manager must supply (aperture, core length and tolerance, torque). Add a "what we need" block.
- **Opening promise versus resolution.** The opening promises "as designed and as verified in CAD and print tests". The limitation table says printing and fit are "validated in CAD and analytical coupons only until the human prints". The report is written after Step 9 only if the print result is back; otherwise "print tests" is a promise the resolution cannot keep. Rewrite the promise as "CAD verification and, if returned in time, print-coupon results".
- **Limitations placement.** The biggest limitation is missing from the table: holding torque is unverified and the analytical estimate is below the placeholder (D1). Add it. Two more: iris aperture versus the 105 mm core (Topologist E-8, Systems Engineer S4); collet coverage between nominals (E4). "Jig does not actuate the iris" sits in Section 2; a page-1 reader can misread the load path before reaching it. Put a clause on page 1.
- **Analysis section.** Absent. The engineering-school reader needs requirements, free-body diagram, derivation and tolerance budget (Systems Engineer S9). Section 3 holds the load path but no analysis behind it.
- **Test density.** Seven of eighteen steps and about 130 tests for 8 to 12 pages. I do not judge this; Systems Engineer S9 and S10 cover it. My point is narrower: 40 manual tests and three cold reads add reviewer cost without a design gain.

### Echo site registry

The registry is the right device. As written it is stale at the rows that matter.

| Row | Problem | Action |
|---|---|---|
| Boss thread spec "Tr 60 x 8" | Impossible: 60 mm major is smaller than the core (Loftsman G1, Topologist TP-1). Appears in Detail 2, T2, T4 (24 mm = 3 pitches "for Tr 60 x 8"), the registry, report sections 4 and 5, and the coupon | Replace with "thread major: Step 2 output, reviewers' range 135 to 165 mm". Carry no number until Step 2. Pitch 8 mm and 45/45 form are Loftsman PROPOSED seeds |
| Collet diameters "90, 95, 100, 105" | Four in thesis, Detail 3, A1 ("4 matrices"), C8, F3, file names, BOM, report 4 | Make count and list params-driven; registry row says "4 or 7, decided at Step 2"; file naming scheme must hold 92.5 (for example `collet_092p5`) |
| Core accepted range 90 to 105 | Also needs the grip window per collet | Add row: collet grip window, bore_free formula, closure |
| Iris standoff 106.369 mm "behind the cutting face" | Fact-Checker F-1: it is head tip to kerf sphere centre, not the pinch plane; 7 in model | Relabel; add the 34.9315 mm dome pole row |
| Spin 1 to 60 rpm | Fact-Checker F-2: motor range, not verified as cutter spin | Relabel |
| "Design load rating" | WOB 100 to 1000 N is a test range (F-4 in Fact-Checker priority table); 1000 N as jig load is a design choice; torque has no source | Rename "design loads (assumed)" and state the labels |
| Tubing 6.00 in / 5.75 in | Registry gives 152.40 / 146.05; A2 text writes "152.4 mm OD"; the plan also says "6 in" | Pick one formatting per quantity; Fact-Checker F-3: 152.4 mm is tubing, not cutter OD |
| Wing nut diameter "TBD" | Derived value is about 181 mm body, 230 mm span; bed bound is 251 mm | Row stays TBD until Step 2; add wing span as a second value |
| Missing rows | Cone half-angle; slit count and width; bore_free formula; thrust-washer; stop height or hard-stop location; core length (500 mm, DECLARED by Quinn); iris aperture (unit unresolved); footprint and feet (D8) | Add |

Additional echo hazards: "bed 256 mm" and "bed minus 5 mm" (251) both appear; "Step 11/12" numbering; "Detail 13 to 17" versus Step table; `min_engage` "PROPOSED 3 pitches = 24 mm" depends on pitch and will change with Step 2.

## Priority actions for the Engineer

1. Decide in the Step 0 plan that the nut is not the hard stop (D2); move the stop to the Step 10 interface table.
2. Add the Designer params review at Step 1 (seed) and Step 2 (blocking), and the Design Critique output at Step 4 (D3, Gate placement).
3. State a holding-torque requirement and a design response (liner, thrust washer, tommy-bar socket) before Step 3; reinstate the moment-arm check (D1).
4. Choose release (steep cone or captive nut) with a jacking provision in Step 2 (D6).
5. Add collet caddy, color, notches, grip-window labels, witness mark (D4, D10).
6. Specify a steady rest or cradle and a handle or strap point for the core; list pinch points for Step 7 (D5).
7. Specify footprint, feet and a tip-over statement (D8).
8. Replace the Step 7 gate question; write Detail 9 and the print-review form (D9, G-1).
9. Fix the registry rows and the thesis sentence; strip revision history from Document Structure (Echo site registry, G-5).
