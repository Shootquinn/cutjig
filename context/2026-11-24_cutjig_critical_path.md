# Cut Jig Critical Path, Week of 2026-11-24

Source: Iris Core-Cutter SBIR meeting, 2026-11-24 (Quinn, Sean, Carlos, Nikki, Eytan; 91 min). The transcript stays off the repo; timestamps below point into it. This file covers only what bears on the cut jig. Where the meeting and the current design files disagree, the meeting is newer and wins until the human rules otherwise.

## 1. The week in one paragraph

Nobody yet knows what the cut jig looks like, and that is the problem this week solves. The goal is an agreed configuration, drawn as 2D sketches the humans have checked, before anyone writes more 3D CAD or cuts extrusion. Sean leads the jig; Quinn reviews (09:05, 13:12). Quinn expects "most of this week to be the 2D thing" (01:30:35). The collet and holder work stays. Everything else may be redesigned, and the redesign may change again.

## 2. What the jig does

The jig holds a rock core upright on the floor and moves the spinning iris core-cutter drill down over it, then back up.

- It sits on the ground. The drill moves; the core does not (17:40).
- It works like an arbor press: the base holds the core in a collet, and the drill travels up and down above it (14:50, 17:40).
- The drill spins about Z like any drill (34:11). The jig must carry the drill's rotation and its torque reaction, as well as its vertical travel.
- Nobody holds the drill by hand: "I'd rather not have somebody holding the drill in a bear hug" (21:34).
- The first version can be crude. "This doesn't have to be the clean room version" (21:34).

## 3. Two operating modes

### 3.1 Slice mode (early testing)

- The core sits in a tall collet.
- The core is advanced upward through the collet "like a push pop".
- The drill comes down and cuts off a coaster-thick slice, so the core is not wasted (18:20).
- Option during early tests: if the core crumbles while it is cut, the collet becomes sacrificial. The drill cuts through collet and core together, and the slice comes off with a ring of collet around it (18:20).

### 3.2 Capture mode (final deliverable)

- The end-of-project test cuts and captures a core 500 mm long. It is the last deliverable before the final report (18:20).
- Quinn's estimate: about 650 mm of vertical travel, to hold a drill "800 millimeters long or whatever" and still capture 500 mm of core (18:20).
- Sequence: lower over the core, cut, capture, raise.

## 4. Test articles

| Article | When | Notes |
|---|---|---|
| Nylon cylinder | First | Stand-in for fit and travel checks (18:20) |
| 3D-printed fake core | First | Same role as the nylon (18:20) |
| Weak cement core | Later | Made weak on purpose; see below |
| Short core, about 100 mm diameter x 100 mm tall | Possibly before year end | From a second simulant supplier being approached (45:21) |
| Long cores | Uncertain | Mines delivery is behind; nylon covers long-core tests until real cores exist (46:22) |

The cement cores imitate ice-cemented regolith with too little ice to bind it. They crumble the way that material would, have high compressive and near-zero tensile strength, and may be layered, which adds stress risers (18:20, 21:34). Two consequences for the jig follow.

1. The core may not support itself. The collet supports it.
2. The core is never inverted. Sean proposed fixing the drill and moving the core up into it from below or above (21:18). Quinn rejected it because an upside-down weak core may fall apart, "like they do at Dairy Queen" (21:34). The drill moves and the core stays upright.

## 5. Materials and parts on hand

- **Extrusion:** 80/20 30-6060 left over from a pre-COVID rover. It lies in Quinn's yard, about $2,000 worth (17:23). The inventory is in `bom_stock_allocation.md` and in the QMRD3 repo on Quinn's GitHub (35:48). On hand: 1540 x 4, 980 x 4, 952 x 1, 728 x 2, 644 x 2, 488 x 2, 468 x 2 (mm).
- **No-cut goal:** build the jig from whole stock lengths, as the photographed track-test stack was (14:50).
- **Fallbacks if a length is wrong:** order pre-cut 80/20, or set up a dedicated miter saw for extrusion. Quinn sees no need for either yet (14:50).
- **Printed parts:** brackets and other printed pieces are expected. Everything printed in the photo is scrap and is not a reference for the design (17:14).
- **Motors:** Sean owns large stepper motors (21:18), so a jack-screw lift can use them.
- **Money:** funds exist to order parts (34:54).
- **The photo:** Quinn shared a photo of an early track-system test stack. The extrusion in it is the material source. Its configuration is not a requirement (14:50, 17:14).

## 6. Lift options the meeting named

Quinn said he does not care which of these wins (17:40).

| Option | Description | Raised by |
|---|---|---|
| A. Arbor press | Take apart a real arbor press, or build one; hand lever on a rack | Quinn (14:50, 17:40) |
| B. Twin jack screws | Parallel lead screws, one each side, driven by "big chunky stepper motors" | Quinn (18:20); Sean has the motors (21:18) |
| C. Other | Any lift that gives the travel and keeps the drill steady | Quinn (18:20) |
| Rejected: fixed drill, moving core | Core travels; drill stays still | Sean proposed (21:18); Quinn rejected (21:34) |

The current design files assume a ratchet hoist for the manual raise, a metal descent stop owned by the upper assembly, and two 1540 mm columns (params `upper.*`, `hoist.*`, `column.*`). Those were Step 2 assumptions. Option B replaces the hoist with powered travel.

## 7. The 2D sketch phase

### 7.1 Why

The AI does not know what the jig looks like. It has things it thinks it remembers, and it puts "the tail of the pig on the nose" (32:58). A 2D drawing shows the human what the model believes. The human's job is to look and say "turn it over" (34:54). On the backcap jig the night before, the first sketch of a part came out upside down. Quinn caught it only because he was looking at the sketches (34:54).

This is also where Quinn stopped work on the jig a week or two ago. It was a triage decision, and the AI "didn't really understand what was supposed to be happening" (13:22). The sketches are the fix for that.

### 7.2 How

- Draw with Python and matplotlib, as on the backcap jig (32:58).
- Follow LLM-PLM section 8.4 (sketching phase) and its two checklists: 8.4.1 for projection and 8.4.2 for plot conventions.
- Equal aspect, grid on, every feature labelled with its key dimension, and the title names the view.
- In a side view a cylinder is a rectangle. A circle appears only in an end view.
- Plot from `params.yaml` values, so the sketch and the model share one source.
- Save each sketch as PNG in the contributor's `cr_scratch/`. A sketch the humans accept moves to a shared location and is committed.
- Iterate until the top is on top and the spinning part spins about the right axis (34:54). Then decide how to build it.

### 7.3 Proposed sketch set

| # | View | Shows | Question it answers |
|---|---|---|---|
| S1 | Side, XZ, whole jig | Floor, base, collet, core, drill, lift, columns; one figure per pose: load, start of cut, end of 500 mm capture, park | Is the jig tall enough? |
| S2 | Plan, XY | Footprint, column positions, drill and keep-out circle, collet axis, slot lines | Does it fit and stay coaxial? |
| S3 | Side, XZ, per lift option | S1 drawn once for option A and once for option B | Which lift? |
| S4 | Side section through the base | Collet, holder, nut, receiver, and the path that advances the core upward (push-pop) | How does the core move up? |
| S5 | Stock map | Each on-hand length placed in the frame, with what is left over | Can it be built without cutting? |
| S6 | Side, drill head close-up | Drill, spindle drive, torque reaction path to the frame | Where does the spin torque go? |

S1 comes first, because the height question decides the rest.

### 7.4 Done for this week

- S1 to S6 exist and have been through at least one human correction pass.
- The humans have chosen a lift option, or narrowed it to two with a test that picks between them.
- The open questions in section 9 each have an answer or an owner.
- Nobody has cut extrusion or started production CAD for the upper assembly. "Go slow to go fast" (01:13:32).

## 8. First-pass height check (to be redrawn in S1)

These are rough numbers from current params plus the meeting. S1 replaces them.

| Item | Value, mm | Source |
|---|---|---|
| Collar top above floor (highest clamped) | about 160 | `stop.collar_top_z` 159.84 |
| Drill advance to capture a 500 mm core | about 535 | `upper.drill_advance_500core` 534.93 |
| Travel, current params | 500 | `upper.travel_max` (gate B6) |
| Travel, meeting estimate | about 650 | 18:20 |
| Drill length | about 800 | 18:20; no params key yet |
| Loading park, tip height for a 750 mm core | about 960 | `upper.park_z` 959.84 |
| Column stock | 1540 | `bom_stock_allocation.md` |
| Soft height target | 2000 | `jig.height_target`, never a limit |

Rough stack for capture mode with 650 mm travel: stop at about 185, so the drill tip starts near 185 + 650 = 835. Add 800 of drill and the drill top is near 1635, before any spindle motor, carriage or lift hardware. Loading a 750 mm core puts the tip at about 960 and the drill top near 1760. A 1540 mm column on a 60 mm frame tops out near 1600. The on-hand columns may therefore be short. The drill and drive could stand above the column tops if the carriage rides low on the drill, and S1 has to show whether that works. Quinn raised the same doubt: "you start to wonder, is it tall enough?" (18:20).

## 9. Open questions

| # | Question | Why it matters | Who answers |
|---|---|---|---|
| Q1 | Travel: 500 (params) or about 650 (meeting)? | Sets column height and lift length | Quinn |
| Q2 | Drill length, mass and top-end hardware for the 6 in drill | Sets total height and lift load; `drill.*` has no length key | Quinn (drill is in build) |
| Q3 | What spins the drill: its own motor on the drill, or a spindle drive the jig carries? | Sets the carriage design and the torque path | Quinn |
| Q4 | Push-pop advance: what pushes the core up through the collet? | The current receiver has a floor and the core stands on the collet core stop, so nothing can move the core upward | Sean, sketch S4 |
| Q5 | Collet length: how tall? | Quinn pictures taller collets than the current "short stubby" ones (14:50, 18:20) | Quinn and Sean |
| Q6 | Sacrificial collet: a separate collet variant, or a liner? | Slice mode may cut collet with the core | Sean |
| Q7 | Lift: arbor press, jack screws, other? | Decides sections 6 and 8 | Sean proposes, Quinn picks |
| Q8 | Manual or powered travel; feed control for the cut? | Jack screws with steppers give controlled feed; an arbor press gives feel | Sean proposes |
| Q9 | Core lengths to support: 500 capture, 750 install, 1000 optional (params) | Drives loading height | Quinn |
| Q10 | Short 100 x 100 mm cores: does the collet family cover a 100 mm tall core? | First real cores may be short | Sean, sketch S4 |
| Q11 | Which existing tests and params become void with the redesign? | The redesign must run through LLM-PLM: change params, re-run tests, record what is retired | Contributor making the change |

## 10. What carries over from Steps 0 to 7

Quinn's gameplan (`research/quinn/gameplan.md`) holds the full record. The parts that matter here:

- **Kept:** the collet family and its generator (`build_parts/collet_family.py`, `docs/collet_generator_usage.md`), seven collets for 90 to 105 mm cores, the holder, the wing nut, the receiver and the PTFE washer. "The collets that designed, it all looks like it'll work, so I don't really want to focus on that" (18:20).
- **Kept as interfaces:**
  - Core diameter 90 to 105 mm.
  - Drill tube 152.4 mm OD (6 in), with a keep-out radius of 86.2 mm.
  - Iris open throat 108.585 mm, carried as a parameter.
  - Axial design load 1000 N (Phase I weight-on-bit range 100 to 1000 N).
  - Holding torque 10 N m, a design assumption.
- **Already dropped:** the steady rest (human decision 2026-11-12). The collet alone holds the core.
- **Open to redesign:** the base frame (644 x 608 footprint), columns, hoist, park latch, descent stop placement and everything else in the upper assembly. Step 12 of Quinn's gameplan ("joint scoping of the upper assembly") is the step this week pulls forward.
- **Test state at Step 7 close:** 672 collected, 622 pass, 50 fail. All 50 failures are features scheduled for later steps. A redesign will turn more tests red, and that is expected. Retire or rewrite them through the TDD method; do not delete them quietly.

## 11. Working method

- **One repo:** https://github.com/Shootquinn/cutjig.
  - Each contributor has `research/<name>/` with their own gameplan, accumulator and scratch.
  - The design files are shared, and either contributor may change any of them through LLM-PLM.
  - Quinn's settled rule: no fear of "messing up" the repo. Push to main. History makes every change reversible (28:58, 30:42).
- **Sync:** `git pull --ff-only` at step open. At every wave and step close: commit, `git pull --rebase`, push. A design-file conflict stops the session and goes to the humans. The agents do not resolve it.
- **Remote review:** Quinn's goal is to pull Sean's work and get a render or turntable of the new assembly on screen without doing anything by hand (25:45). Commit sketches and renders as well as code.
- **Leading the agents:** the agents hedge. The human sets one direction and holds it (28:58). When a sketch is wrong, say so plainly and have it redrawn.
- **Getting unstuck:** Sean stops and pushes. Quinn pulls and diagnoses, then sends Sean a correction to paste into his session (25:45).

## 12. Schedule around the jig

| When | Event | Source |
|---|---|---|
| Week of 2026-11-24 | Repo live; 2D sketch phase for the cut jig; backcap test jig fabrication starts | 01:13:32, 01:30:06 |
| Week of 2026-12-01 | Iris prototypes for the aluminum-tube installation | 09:05 |
| Week of 2026-12-07 | Assemble the drill that can cut cores; first cuts may use the hardened stainless iris leaves alone, or with brazed-on cutters | 09:05 |
| 2026-12-31 | Phase I deliverables; short report (one-page abstract plus about two pages) | 09:05, 47:53 |
| End of project | Capture a 500 mm core in the jig, before the final report | 18:20 |

The backcap test jig is Quinn's. It is the pathfinder for the drill that the cut jig will later hold (01:30:35). Its sketch-first workflow is the model for this one.

## 13. Suggested first session for the cut jig

1. Read this file, `ASSEMBLY.md`, the Objectives and Design Notes in `research/quinn/gameplan.md`, and LLM-PLM section 8.4.
2. Draft Step 0 of the contributor's gameplan. Its first step is the sketch set in section 7.3, S1 first.
3. Put Q1 to Q3 to Quinn before S1 is final. S1 can start on the meeting values (650 travel, 800 drill) and flag them.
4. Review each sketch with the human before drawing the next one. Record every correction in the gameplan Design Notes, so the next session does not repeat the mistake.
5. At the week's end, the Manager closes with the chosen configuration and a list of the params keys and tests that change.

## 14. Draft requirements for the configuration

Drafted from the meeting and current params for the sketch phase. Status follows the params convention: DECLARED is from a human, ASSUMED is a working value.

| # | Requirement | Value | Status | Source |
|---|---|---|---|---|
| R1 | Stands on the floor, free-standing | yes | DECLARED | 17:40 |
| R2 | Core axis vertical; core never inverted | yes | DECLARED | 21:34 |
| R3 | Drill moves along Z; core stays fixed during the cut | yes | DECLARED | 17:40, 21:34 |
| R4 | Drill rotates about Z while it moves | yes | DECLARED | 34:11 |
| R5 | No hand holds the drill during a cut | yes | DECLARED | 21:34 |
| R6 | Vertical travel | about 650 mm (params: 500) | ASSUMED | 18:20; Q1 |
| R7 | Capture length, final test | 500 mm core | DECLARED | 18:20 |
| R8 | Drill length | about 800 mm | ASSUMED | 18:20; Q2 |
| R9 | Core diameter range | 90 to 105 mm, one collet per 2.5 mm step | DECLARED | `core.diameters` |
| R10 | Core held by a collet that supports a weak, non-self-supporting core | yes | DECLARED | 18:20 |
| R11 | Core can be advanced upward through the collet for slices | yes | DECLARED | 18:20; Q4 |
| R12 | Collet may be cut with the core (sacrificial option) | allowed | DECLARED | 18:20 |
| R13 | Coaxiality, drill to core | 1.0 mm | ASSUMED | ASSEMBLY.md ICD |
| R14 | Axial load the frame carries | 1000 N | ASSUMED | `loads.axial_design` |
| R15 | Holding torque on the core | 10 N m | DECLARED | `loads.torque_design` |
| R16 | Frame from on-hand 30-6060, whole lengths preferred | yes | DECLARED | 14:50 |
| R17 | Overall height | 2000 mm soft target, never a limit | DECLARED | `jig.height_target` |
| R18 | First version may be crude | yes | DECLARED | 21:34 |

Any R-row a sketch cannot meet goes to the human with the sketch, together with the change that would meet it.
