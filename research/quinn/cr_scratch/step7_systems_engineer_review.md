## Verdict

SIGNED. No contradiction of the frozen concept or ICD. The five relation-row changes carry reasons (Loftsman L4); the ruling file is missing and goes to the Manager (inputs table). Receiver vertical support is open and owned by Step 8.

## Findings

| Question | Evidence | Result |
|---|---|---|
| 1 Load loop and stop ownership | Pair rows R and K, nominal 100: nut/washer P 2.387 mm3 in every pose; holder/washer C 0.005 at Kd1 and Kmax; holder/collet C 0.005; collet/core C; base/collet C; base/nut C 0.004. Ten-member chain is realised and closes inside the receiver. Receiver underside contact 0.0. Base/holder G 0.125, never loaded. | Pass. The base object is one compound of receiver and plate, so base/collet and base/nut cannot separate the receiver from the plate; the zero comes from geometry (receiver r 80, plate hole r 80.2, nearest member edge x 82). The stop, columns and carriage are not among the ten assembled parts; the stop path is unverified here |
| 2 Pose set | Flange gap 13.126 / 8.590 / 1.500; holder bottom 13.626 / 9.090 / 2.000; ring-top gap 11.631 / 7.095 / 0.005 (C at Kmax only). Ledger errors empty, placement diff 0.0, screw invariant 60.645 in all poses. Kd1 phi -237.195 replaces -237.241 (holder 9.090 against 9.0890; A3e tolerance 0.05) | Pass. One assembly, three states, S(phi) = Rz(phi)T(0,0,L phi/2pi), clockwise lowers the nut |
| 3 Clamp range | T4 and T5 at 90 and 105: engaged 25.705 / 31.400 / 38.490 (min 24), slit 1.500 / 1.238 / 0.584 (floor 0.5), stop travel 10.016 at Kmax (one pitch 8, 4.01 before the nut relief), flange gap above 0. Window d-1.5 to d+1.0 gives 88.5 to 106.0 | Pass. |
| 4 C6 resolution | Frame 644.0 x 608.0. 12 brackets (8 purchased 57 mm class, 4 printed 68 mm), 96 T-nuts at 8 per bracket. Overlaps 18,249 / 1,061 / 16,523 mm3 to 0; new T-nut/purchased bracket 716 mm3 to 0. Stock 644, 488, 468 unchanged | Pass. The result equals the Step 2 text: four corners x 2 purchased plus four printed support ends. One printed bracket per support end is DECLARED, joint capacity at Step 12 |
| 5 Upper-assembly interfaces | Stop pad top z 184.84 = collar top 159.84 + g_stop 25; cutter annulus starts at 184.84; holder/cutter 25.000 at Kd1; nut/cutter 31.740 / 38.830; stroke 684.84 - 184.84 = 500; lead-in clearance 3.5 to 11.0 against 2.055 | Pass. stop.FCStd, frame_profiles and column notch inputs untouched by mtime. |
| 6 Relation rows | Changed: base/holder g_min 1.5 to 0.12; holder/collet R 0.30 to 0.29; holder/nut K 0.75 to 0.50; nut/washer C to P; collar top/cutter R G to F. Reasons: 0.125 key clearance, 0.30 x cos 10 deg, washer proud 0.5, press pads 2.387 mm3, R unclamped 20.464 | Reasons present; no threshold weakened. `step7_class_rulings.md` does not exist; Topologist sign not recorded |

Holder collar and nut relief rebuilds have rows in `step7_rebuild_authorizations.md`. Collar id is 110.0 (params DERIVED; the concept text says 114.0); params govern.

## Inputs to later steps

| Item | Owner step |
|---|---|
| Write `step7_class_rulings.md` for the five rows above; Topologist signs | Step 7 close (Manager) |
| Receiver has no shoulder or flange (bbox r 80 throughout) and the plate hole is straight; receiver weight, core weight and the 204 N pull-out have no modelled path to the plate. Add a receiver/plate pair (C, weight) or a shoulder, then A6a against a real contact | Step 8 (receiver and base), Step 12 load check |
| Stop, columns, carriage not in the pose set; A2c, A2d, A1c, A1d, A2h decide that no printed member is in the stop path | Step 12 |
| Datum C hardware (two key T-nuts, stop dowel) is not modelled. fit_plate_key_stop_pin 0.250 subtracts the declared base.key_width 11.5 from the built pocket; pin gap reads 0.000 against the 0.20 along-slot entry | Step 9 hardware, Step 12 A3b |
| A3b closes with the column foot and carriage guide; built fits sum 0.45 against 1.0 | Step 12 |
| PZRT 3030 T-nut CAD absent, proxy stands; 96 T-nuts ASSUMED at 8 per bracket | Step 9 BOM |
| Nut relief changes nut volume and Euler; Topologist re-sign of frame, holder, nut | Step 7 topology gate |
