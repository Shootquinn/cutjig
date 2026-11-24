## Verdict

The plan is a good test-and-document process wrapped around a design that has not yet been designed. The Software Engineer's revision hardened the verification. It did not close the physics. Three decisions that set the shape of every part (where the force loop closes, how the collet closes 5 mm of diameter, what the binding alignment tolerance is) are still open or unstated, and Step 1 writes the whole CAD suite before they are made. The effort is also lopsided: roughly 80 CAD cases for the jig, 130 tests for the report on the jig, and no physical test of the stated purpose.

Facts only. Arithmetic below is order-of-magnitude, with assumed friction coefficients marked. It is there to show what Step 2 must derive, not to replace it.

## Findings, ranked by severity

### S1 (critical). No load case is derived; the plan proves geometry, not that the jig holds.

- The loads in the plan are inherited, not derived. WOB 1000 N is the Borebot anchoring bound (extraction C4). Torque 20 N m is a placeholder with no source (C5). Safety factor 3 is applied to loads that do not exist yet. The 30-6060 frame is sized by what is in the stock bin, not by load, so "design load rating" in the echo registry misleads. The weak links are the printed parts.
- The cutter (ID 146.05 mm) never touches a 90 to 105 mm core. The only things that load the core are the iris leaves (closure and severing reaction, torque from friction while the cutter spins at 1 to 60 rpm) and the core's own weight (up to about 9.4 kg, DERIVED upper bound). Those act at least 106.4 mm above the holder, so the holder sees a bending moment and a torque, not WOB. Nothing in the plan states these as load cases.
- Rough holding capacity of a hand-tightened friction collet, to show the order of magnitude. Assumptions, none sourced: Tr 60 x 8 thread, friction 0.3 on thread flanks, wing couple of about 3.6 N m (30 N each on wings spanning 120 mm). The nut gives about 100 N of axial force per N m, before collar friction. Say 300 N after losses. A 10 degree cone with friction 0.3 turns that into about 2 x 300 = 600 N of summed radial force on the core. Core friction 0.4 gives about 240 N axial holding and about 10 N m of torque holding at d = 100 mm, before losses from collet stiffness and a non-round concrete core. That is single-digit N m, below the 20 N m placeholder, and barely above the 92 N core weight with a safety factor of 2. If the iris transmits anywhere near 20 N m to the core, a friction collet in PETG rotates the core. Stratigraphy order must be preserved (extraction section 6), so a rotating core is a failed test, not a nuisance.
- The test suite does not touch this. C2 and C3 compare the model to analytic values built from the same params, so they test the CAD kernel, not the design. T5 tests that the thread and slit have travel, not that the grip suffices.

### S2 (critical). The stack's force loop is ambiguous, and release is undefined.

- The draft says the holder "seats on the boss" and the nut "presses the holder axially, which closes the collet." As worded, the loop nut, holder, boss, thread does not pass through the collet, so nothing closes it. The reading that works: the collet bottoms on a boss shoulder, the holder cone travels down over it, and the loop is nut, holder cone, collet, boss shoulder, boss thread, nut. In that reading the holder must not bottom on the boss (T5 already requires one pitch of travel). State it as a closed loop in ASSEMBLY.md.
- Release. Backing the nut off does not lift the holder unless the cone half-angle exceeds arctan(friction), about 17 degrees at friction 0.3, or the nut captures the holder (ER-nut style lip). A shallow cone, which gives the wedge gain, self-locks and jams. A steep cone cuts the gain to about 1 at 17 degrees. The plan has T5 asserting a "release pose" without saying what produces it. Choose: captured nut with a modest cone, or no capture with a steep cone. This is E2 and it is more than a naming choice.
- The Software Engineer's claim that a stack reversal "changes data, not tests" is false. F1, T5 and A3 pose different contacts and different clearances depending on the loop. Step 1 must not write them until Step 2 fixes the loop.

### S3 (high). The collet cannot close 5 mm of diameter with one slit, so the family is not yet a single parametric design.

- E4 notes circumference change of 15.7 mm and leaves it as a flag. That figure sets the slit design. Closing a diameter range of 5 mm (nominals 5 mm apart, tolerance covered with no gaps) needs total slit closure of pi x 5 = 15.7 mm. With the plan's C5 "slit count equals params," that means N petals each closing at least 15.7/N mm. For N = 6, each slit is about 3.1 mm wide relaxed (2.6 mm closure plus the 0.5 mm clamped minimum in T5). Slit count and width are family parameters, not details.
- Radial closure of 2.5 mm needs axial cone travel of 2.5 / tan(alpha): 14 mm at 10 degrees, 20 mm at 7 degrees. Boss thread length is then at least 24 mm engagement + 14 mm travel + 8 mm margin + one pitch, about 55 mm. That is a derived dimension the plan has as a placeholder (min_engage PROPOSED).
- Outer cone fixed (C4) with bore varying gives wall thickness varying by about 15 mm between d = 90 and d = 105, so closing stiffness differs several-fold across the family. C4 makes the geometry uniform, not the function. The invariant that matters is the nut torque to clamp force relation across the family. Test it at both extremes in the print coupon (stiffness is why 90 and 105 are the right T5 extremes, not "monotonic stack height").
- The "adding 2.5 mm is a params change only" claim holds for geometry. It fails for function until the stiffness relation is derived. Treat it as a claim awaiting derivation, and run C8 on a derived accept range, not an asserted one.

### S4 (high). The binding alignment tolerance is the iris aperture, not the tube gap, and it is unresolved.

- The plan cites the 20.5 to 28 mm radial gap to the tube bore. That is a keep-out, not an alignment tolerance. The tolerance that matters is core versus iris open aperture. Extraction section 2: open aperture 54.2925 mm, "radius or diameter, unresolved"; INSITU2 says it matches a 100 mm core. If it is a radius, the open diameter is 108.585 mm and the 105 mm core has only 1.8 mm per side of lateral slack; the 100 mm core has 4.3 mm. If it is a diameter, a 100 mm core does not fit and neither does 105. This sits in section 7 of the extraction as item 1 ("not found") and in the register only as UNVERIFIED. It should be a Step 1 gate: the 90 to 105 range is only meaningful if the aperture accepts 105.
- With 1.8 mm per side, the coaxiality budget between drill axis and core axis is of order 1 mm, and the printed stack carries: thread radial clearance (a tilt of clearance over engagement: 0.8 mm diametral over 24 mm is about 1.9 degrees; at 100+ mm above the holder that is several mm of tip), collet bore print error (0.2 to 0.3 mm), slit non-uniformity, core out-of-round, and core tolerance (+/-1 mm, UNVERIFIED). The plan has T3 clearance and C3 at 0.02 mm. A 0.02 mm threshold on a 0.4 mm nozzle part is a model check, not a tolerance stack. No tolerance budget table exists.
- Datum scheme missing. The core axis must be located by a pilot or the cone, never by the trapezoidal thread, which is the loosest fit in the stack. Say so in the ICD.

### S5 (high). The hard-stop load path can run through the printed wing nut.

- A2 lets the Engineer choose a branch: nut passes inside the 146.05 mm bore, or the nut is the "declared hard stop." With a WOB bound of 1000 N and the iris standing 106.4 mm behind the face, the wide nut is the natural stop, so the cutter's descent load goes through a printed nut, boss thread and base plate. That is the weakest path in the jig.
- Decide it by load path, not preference. The stop should be a metal 30-6060 member on the frame, with the nut strictly below it or inside the bore. If the human wants a "very large" wing nut, the wing span stays under about 135 mm or it sits below a frame stop.
- Related unknowns that feed this and the report: stroke, stop margin, insertion depth of the core in the collet, and minimum core length. Exposed core must be at least 106.4 mm plus margin, so minimum core length = insertion depth + 106.4 + margin. Core length is stated by no source.

### S6 (high). The upper assembly hand-off is a promise, not an interface.

The plan has "Systems Engineer interface review" at Step 8 and an agenda at Step 10, with no statement of what the base exposes. The base should expose this, defined in Step 2 and recorded in params.yaml and ASSEMBLY.md as an interface control table:

1. Datum A: frame top plane (base plate underside, z = 0). Datum B: boss axis, +Z, the one alignment axis for everything. Datum C: a frame slot line fixing rotation about Z.
2. Mounting pattern: the T-slot lines on the frame top face (30 mm pitch, M6 spring-ball roll-in T-nuts) available to the column, with their positions and which are occupied by the base plate.
3. Coaxiality requirement: drill centerline to boss axis within a budget derived from S4, with a stated adjustment (slotted base plate holes, plus one printed alignment gauge that seats on the holder and centers a 152.4 mm tube; one cheap part removes a tolerance chase).
4. Keep-out envelope: cylinder of radius 76.2 mm plus margin about the boss axis, from holder top to the stroke end, with the frame stop at height H_stop and its rated load.
5. Footprint versus column height: a tip-over statement. A 1540 mm column with a drill on top over a perimeter frame needs a stated footprint, even if the number comes at Step 10.
6. Cable exit and debris path from the back cap.

None of this is a CAD test now. A3 sign checks and A2 are the only hooks.

### S7 (medium). The test plan covers parts, not the system.

- The stated purpose is hold, descend, sever, retain, retract. No test, planned or deferred, addresses any of them. Descend, sever and retain belong to the upper assembly and the drill. That is a valid reason they are not run now. It is not a reason that no acceptance spec exists. Write the end-to-end acceptance spec at Step 10 as the first deliverable, so the upper assembly is designed to be accepted by it.
- Add a physical acceptance protocol to Step 9, performed with the human's first print and a stand-in core (a 100 mm concrete cylinder or PVC section of similar weight): (a) clamp at 90 and 105 mm collets, hand-tight, torque to slip with a torque wrench and a lever arm; (b) pull-out with a spring scale; (c) lateral deflection at core top under a small side load; (d) ten clamp and release cycles, with thread wear and collet creep after a one-day hold; (e) fit of a 152.4 mm tube template passing the nut. Record against the S1 estimate.
- The tolerance stack is a report item as well as a CAD item. The plan's "tolerance" step (Step 6) checks clearance and wall, not stack-up.
- Assembly sequence for a 9 kg upright core is unaddressed (how an operator seats a 500 mm core in a release-pose collet without the core leaning, with a 1 mm clearance).

### S8 (medium). The step sequence is not ordered by design dependency.

- Step 1 writes the full CAD suite (with `pending: step2` thresholds) before Step 2 produces the loop, cone, slit and thread decisions. S2 and S3 change test shape, not only thresholds. Split Step 1: 1a foundation (params, BOM, frame, FreeCAD check), then Step 2, then 1b suite.
- Step 3 builds the collet generator before the holder and boss exist. That works only if Step 2 issues the interface table (cone angle, seat heights, shoulder, pilot, thread) as fixed numbers all parts read. Without that table, the collet family is one script and the other five parts are one-offs that happen to agree.
- Objective 2 says "all built from a single parametric generator." Detail 3 and A.14 describe a collet generator plus per-part scripts. The spine is params.yaml plus common.py. Say that, and make the interface table its first section.

### S9 (medium). The report plan overstates and under-serves its two audiences.

- The thesis sentence promises that the frame "holds any 90 to 105 mm Mines core upright and coaxial" and that "every number traces to a source or a test." The register shows torque, tolerance, core length, aperture and printer are UNVERIFIED, and the Document Structure itself promises no mechanism performance. Reword: "is designed to hold ... verified in CAD and by print coupon; open inputs are listed."
- Executive reader: page 1 has design, verification, deferrals. It lacks the decision: what the program manager approves or must supply (the aperture, the Mines core length and tolerance, the torque from Phase I) and the risk if those arrive late.
- Engineering-school reader: wants requirements, free-body diagram, derivation, tolerance budget, test against prediction, lessons. Section 3 (concept, 9 manual tests) carries the load path, with no analysis section behind it. Add a short analysis section built from S1, S3 and S4, and let Step 9 print results close against it.
- Three cold-read passes (Steps 12, 16, 17) and 130 tests (about 40 manual) for an 8 to 12 page report is more checking than the report can carry. The 12-tests-per-page ratio is an assertion, not a derivation.

### S10 (low). Over-engineering, cut or trim.

- Independent re-measure script X1 and the SHA-1 manifest (W2): the human's first print is the independent check. Keep volume and interference recompute only, if cheap; drop the rest.
- Four full interference matrices (A1): fine if parametrized. Do not hand-review four tables.
- F5 feature-presence check by result-JSON volume: a list check with little discriminating power; fold into the topology gate.
- Report suite: cut to about 60 tests and two cold reads (outline, final). Seven of 18 steps are the report path.
- Where the plan is right to keep: the register, FCStd authority, the zero and known-bad controls, C4, A2 and A1.

## What I would change

1. Insert a one-page system concept step before the test suite (Systems Engineer with Loftsman): closed force loop sentence, release mechanism, three load cases (iris torque, lateral at lever arm 106+ mm, core weight/retention) with a statics estimate like S1, stack-up tolerance budget, and the interface control table of S6. The suite is written against that.
2. Make the iris open aperture a Step 1 gate with an owner (the human or the Engineer measuring the 6 in design). If 105 mm exceeds it, cut the range before building four collets.
3. Resolve E2, E3, E4 in that concept page, not in Step 2 after tests exist. Fix E4 by making slit count a family parameter and deriving the accept range; choose petals, not one slit.
4. Put the hard stop on the frame in metal. Delete A2's printed-nut-as-stop branch, or keep it only as a documented fallback with its load rated.
5. Locate the core axis by a pilot or the cone, not the thread. Add a printed alignment gauge and slotted base holes; add a holder-release mechanism (captured nut or steep cone).
6. Add Step 9 physical hold test (torque, pull-out, deflection, cycle) with predicted values from step 1 of this list. Write the five-verb end-to-end acceptance spec at Step 10 open.
7. Add a function-level family invariant: clamp force per N m of nut torque measured on the 90 and 105 collets. State in the plan that 2.5 mm increments are a params change only for geometry.
8. Reword the thesis; add a "what we need from you" block to page 1; add an analysis section for the engineering-school reader.
9. Cut report tests to about 60, drop one cold read, and drop X1 beyond volume and interference recompute.
10. Reorder: 1a, 2, 1b, 3.

## What holds

Single params file as the spine; FCStd as authority once built; the scope-honesty list; the register separating TRACED from VERIFIED; the stock rules (30-6060, spring-ball roll-in T-nuts, full-size brackets); the control discipline on gates; the finding that the drill drivetrain closes the iris so the jig supplies no actuator. The structure is sound. Its center, the mechanism, is where it is thin.
