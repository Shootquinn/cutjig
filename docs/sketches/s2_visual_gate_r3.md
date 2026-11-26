# S2 r3 M1 visual gate (Designer, step 1.2 (f), P8r)

Figure: `docs/sketches/wip/s2_plan_r3.png` (2222 x 1487 px), read at 100 percent with 3x and 4x crops of the screw sets, the pinion c mount, the member c notch and the leader ends. Pixel scale 1.39 px/mm (MEASURED from the x ticks). Inputs: `s2_spec.yaml`, `wip/s2_checks_r3.json`, `wip/s2_summary_r3.md`, gameplan l.176-203.

## Corrections to the brief

None.

## 1 Reviewer-model controls

| Figure | Items | Verdict | What I see |
|---|---|---|---|
| ctrl_a | V1 to V5 | FAIL V3 (V1, V2, V4, V5 PASS) | Wide head block (labelled "cutter OD ASSUMED 177.8") at z 1090 to 1195, at the top of the tube; tube runs down to 245 with nothing at its lower end. Tail on the nose: the drill is tip-up. Floor at z 0 at the bottom, axis vertical, core 100 to 600 upright, screw vertical with blocks at both ends and the nut at the ring. |
| ctrl_b | V1 to V5 | PASS | Same figure with the head block at z 245 to 350, at the bottom of the tube, and a plain tube top at 1195. Floor at the bottom, axis vertical, core upright, screw vertical with blocks bottom and top. |
| ctrl_c | handedness | PASS | +X arrow to the right, +Y arrow up, theta arc from +X counter-clockwise to +Y. Screw a labelled 30 at (140, 80): atan(80/140) = 29.7 deg (DERIVED). Screw b 150 at (-140, 80), screw c 270 at (0, -160). |
| ctrl_d | handedness | FAIL | +Y arrow points down the page, so the plan is mirrored (seen from -Z). The theta arc runs from +X clockwise on the page to the downward +Y. Screw c labelled 270 sits at y +160 on the page; screws a 30 and b 150 sit below the X axis. |

## 2 Rubric (S2: V2, V6 to V10; V1, V3, V4, V5 N/A)

| Item | Verdict | What I see |
|---|---|---|
| V1 | N/A | plan view |
| V2 | PASS | Datum B cross, gear annulus, gear hub, bearing, tube and cutter rim are concentric on the origin. The three pinion axes are dash-dot radial chain lines at 90, 210 and 330 running through the NEMA 23 bodies, so the drill spins about Z. |
| V3 | N/A | plan view |
| V4 | N/A | plan view |
| V5 | N/A | plan view |
| V6 | PASS | Screws, guide rods, nut housings, anchor and guide blocks, tube, cutter rim and keep-out are circles; members are 60 x 60 squares end-on; motors are rectangles. No side-view shapes. |
| V7 | PASS | Ring: OD 420 disc with the 200 bore, three blue nut-housing bosses d 50 at the screws, NEMA 23 bodies on mounts at 90, 210, 330, two guide lugs (blue dashed, under the Step 2 ties) at 0 and 180. It reads as a structure carrying housings, mounts and lugs. Gear: annulus with dashed radial tooth ticks (teeth face down). Bevel pinions: trapezoids narrowing toward the axis, dashed under the gear, with the heel corners outside the gear OD drawn solid; hub and dark shaft bar to the motor; motor outboard. Screws: dot at the pitch radius inside the guide block circle and the blue housing boss; the nut flange is under the block (legend says so). Members a, b, c: hatched 60 squares at r 274, sections. Lift motors: dashed 42 squares centred on the screws. |
| V8 | PASS | 14 labels legible at 100 percent; right column spaced evenly, none overlapping; tags "screw a 150 deg", "pinion c 90 deg" etc. sit clear of slot line C. Leader ends checked at 4x: ring OD 420 ends on the rim at (209, 0); cutter OD on the dotted rim at (89, 0); keep-out at (85, -15); tube OD at (72, -26); gear PD at the gear OD at theta 10; base plate at the plate edge x 322; descent stop at the pad corner (r 208, theta 141.6) (all DERIVED from pixels, +-1.5 mm). Every labelled feature carries its value. See NOTE 1 on the descent-stop leader path. |
| V9 | PASS | From the figure: it fits (every part lies inside the 644 x 608 plate; member c sits in the notch on the rail top), it is coaxial (drill, gear, bearing, ring and datum B share the origin, pinions on radial axes at the gear pitch circle), and the operator side is theta 90 +- 45 between screw b (30) and screw a (150), free of fixed frame parts, with the NEMA 23 c and pinion c overhead in it. Spec question: "Does it fit, stay coaxial, and leave the operator a side to load the core and change collets?" The sentence answers all three parts; yes. |
| V10 | PASS (F6 carried) | See section 5. |

## 3 S2 rubric additions

| Addition | Verdict | What I see |
|---|---|---|
| Plan handedness, screws 30/150/270, pinions 90/210/330 | PASS | +X arrow right, +Y arrow up, theta arc counter-clockwise inside the tube bore; slot line C is the chain line at y +259 labelled "+X". Screw b at 30 upper right, screw a at 150 upper left, screw c at 270 bottom; pinion c 90 top, a 210 lower left, b 330 lower right. Legend states the same. |
| All three screw sets, pinions, NEMA 23s, lift motors and frame members drawn | PASS | Three screws with blocks, bosses and dashed lift-motor squares; three pinions with motors; members a, b, c hatched. |
| Motor outboard, pinion inboard, narrowing toward the axis | PASS | At 90, 210 and 330 the grey NEMA 23 body is outboard (r 142 to 218), the shaft bar inboard of it, and the pinion trapezoid narrows toward the axis. |
| Ring reads as a structure, not a washer | PASS | Bosses, motor bodies over their mounts, lugs and the gear give the disc its structure. The mounts are hidden under the motor bodies (same footprint, r 142 to 210 under r 142 to 218), so they read only as the motor seat. |
| Member c on the rail top inside the column notch, notch outline visible | PASS | At 3x the notch reads as a white void 5 mm either side of the hatched member and open to the plate edge; the rail-top piece in the notch draws solid. No outline stroke round the notch (N2 from r2, left open by the Engineer); the void carries it at 100 percent. |

## 4 Parts drawn narrower than their footprint (TP-n, projected_extent does not catch this)

| Part | Drawn | Reads as the part? |
|---|---|---|
| liftmotor_a/_b/_c | 42 square in a circumscribed footprint (11.71 bound vs 15.69 drawn to the sector edge, summary) | Yes: a NEMA 17 square under the anchor, dashed. |
| anchor_a..c, guide_a..c | circle r 21 (round by declaration, LF1.1-9) | Partly. A d 42 circle concentric with the screw reads as a nut ring more than a bearing block; the bracket arm attached to it gives it its role. Values ASSUMED until Step 2; acceptable. |
| motor_mount_a..c | under the motor body, 57 wide r 142 to 210 | Hidden by the motor; not separately readable. Acceptable (hidden by a nearer part). |
| descent_stop | 60 x 15 pad under the arm and ring rim, dashed | Reads only as a short dashed arc beside the rim at theta 150; legend names it. Acceptable. |
| frame_upper_a..c, guide_tie_a/_b, bracket arms | drawn equal to their footprints | Yes. |

## 5 V10 operator tasks (S2)

| Task | Reach | Sightline |
|---|---|---|
| Load core (load) | Operator in the orange sector theta 90 +- 45, torso at r >= 304 (plate edge y 304), reach about 304 to the axis plus the core radius; no fixed part inside the sector (S2-5a least 11.71 to the lift motors, MEASURED in the summary). | In plan the radial line from the sector centre to the axis passes under motor c (r 142 to 218). In z the line from an eye at 1600 z_S, r 350 down to the holder bore (about 220 z_S) is at 1079 z_S at r 218 and 780 at r 142 (DERIVED), below the NEMA 23 at 1185.34 to 1242.34 and the ring at 1149.84; the plan cannot show this and the gate takes it from the stack. Head strike when leaning in stays with the Step 2 guard (gameplan l.181). |
| Collet change (load) | Kneel in the sector, hands at r <= 115; lift motors at 30 and 150 sit outside the sector edges; descent-stop pad at 141.7 to 158.3 deg, outside the 135 edge (DERIVED). | Wing nut from the sector at knee height; nothing fixed between sector and axis in plan. |
| Stand and watch | Observer dot at r 400, theta 60, outside the plate (y 346 > 304). | Drawn sightline to the axis, labelled "ring rim r 210 hides the cut at capture_end". The end of the cut is not visible: F6, accepted by Sean as assigned to Step 2 and S2 (Design Notes 24). S2 shows it; it is not a new finding. |
| F6 sightline | as above | as above; the label carries eye z_S 1600 (operator.eye_height 1540 z_A). |

## 6 Rules awaiting the Designer's signature before M1 (process fix (h))

| Rule | Premise check | Signature |
|---|---|---|
| K4 (a') anchor under no other row's area drawn above it, (c) no area over a leader, (d) leader end clear of hatch (25 % / 25 %); labels at z order 100 | K4-B9, B10, B11, Z3, Z4 | SIGNED. On S2 r3 every leader draws above the gear and ring fills; on S1 r7 the core 750 leader ends on the core edge above the gear hatch. |
| Split convention: a partly visible dashed piece gets a solid copy under the covering fill; `plan_style: stand_in` exempts the Step 2 ties | K8-B34, B35, B36, Z8 | SIGNED. The pinion heel corners outside the gear OD read solid and the covered part dashed; the ties read dashed as stand-ins. |

## 7 Verdict

**S2 r3: PASS.** Every applicable item passes. FAIL count 0.

NOTES (no action required for acceptance):

1. NOTE `descent_stop` label: the leader runs horizontally about 520 mm from the right column to the pad at theta 150, across the operator sector, the pinion c mount and the screw b bracket arm. It crosses no leader (K4 holds), but where it crosses motor c's mount at z_S 1161 it reads like a part edge. Placing this label on the left of the figure, or allowing a leader with a bend, would shorten it to about 40 mm.
2. NOTE `bracket_guide_a/_b/_c` over `ring`: the guide bracket arms are drawn unfilled, so the blue ring rim shows solid through them although the arms are nearer at load. The hidden-line convention in the legend says a covered edge is dashed. Same class as the r2 notch item; no K8 rule covers an unfilled cover over a single-circle artist.
3. NOTE: N2 from r2 (notch outline stroke) stays open by the Engineer's disposition; the void reads at 100 percent, so it does not block.

Controls (scored blind): ctrl_a FAIL V3, ctrl_b PASS, ctrl_c PASS handedness, ctrl_d FAIL handedness. Orchestrator scoring against key.json: to be recorded here.

## Gameplan lines to change

none
