# Step 1.4 P5r: raiser re-checks after P5f (Software Engineer, Topologist, Designer)

## Corrections to the brief

1. Basis (orchestrator loop-cap ruling): the P5f dry-run and red-first table (step1.4_engineer_redfirst_fixes.md sections 1 to 3) plus one fresh branch deletion per FIX. Each deletion ran on its own copy of the live docs/sketches and params.yaml in `D:\Unleashed Robotics\_scratch\cutjig\open14\p5r\ws\<id>\`, followed by `check_sketch.py --controls --only` over the Engineer's 70-control S4 set at 12 jobs. Script: `p5r\bin\del_p5r.py`. Output: `del_p5r.json`, `del_p5r_stdout.txt`, `del_p5r_stdout_tf2v.txt`. Fixture render for the tick shape: `p5r\png\s4fx_carrier.png`, `crop_pos.png`.
2. Where the Engineer's deletion edit could be varied, these deletions use a different edit. A loosened tolerance or a neutralised operand stands in for the `if False:` form, so each result is a second mutant on the branch and not a replay.
3. Topologist F3 and Software Engineer FIX 3 are the same branch, sweep (s1). One deletion (SW3_s1) serves both.
4. The first F2 deletion (TF2_gapskip, `break` changed to `continue` in the coverage merge) turned no control red. It is an equivalent mutant. The occluder intervals are sorted by z_lo, so every interval after a gap also starts above `cur`, and the gap is still reported. It was replaced by TF2_vertex, which tests the vertices only (the pre-F2 reading). That deletion turns K5-B69 red. No deletion of a real branch passed.
5. LIVE baseline, no edit: Z 10/10 clean, B 59/59 fired, smoke 1/1; 17.9 s (MEASURED). The P5f full run, which was not repeated here, reads 551/551 (Z 120, B 427, smoke 4) in 154.6 s (Engineer, MEASURED).

## Deletion results (MEASURED)

| Id | FIX | Edit (one, asserted unique) | Red controls | Reading |
|---|---|---|---|---|
| SW1_drawn | SW FIX 1 | S4-1 drawn-collar tolerance `tol` to `tol + 5` | S4-1-B2 | guarded |
| SW2_grip | SW FIX 2 | S4-2 (c) grip-member-not-drawn condition made unreachable | S4-2-B5 | guarded |
| SW3_s1 | SW FIX 3, TOP F3 | sweep (s1) `len(arts) != 2` to `len(arts) < 1` | K5-B64 | guarded |
| SW4_core | SW FIX 4 | S4-2 (a) core-on-carrier pair compares carrier top to itself | S4-2-B4 | guarded |
| SW5_deps | SW FIX 5 | checks_s4.s3_loads: `sr.append(p)` to `pass` (spec read not recorded) | DEPS-Z5 | guarded at the record source (the Engineer's deletion was at the check_sketch merge) |
| TF1_t_tol | TOP F1 (a) | (t) tick-to-wall tolerance TOL_Z to 1.5 | K5-B65 | guarded |
| TF2_gapskip | TOP F2 (a) | merge `break` to `continue` | none | equivalent mutant (Correction 4) |
| TF2_vertex | TOP F2 (a) | edge coverage replaced by vertex coverage | K5-B69 | guarded |
| TF4_between | TOP F4 | `min(a, b) <= 0` to `a * b <= 0` | S4-3-B8 | guarded |
| TF5_h3 | TOP F5 | (h3) `if not hit: bad += 1` made unreachable | K8-B111 | guarded |
| DC1_E4 | DES D-c1 | (iii) occluder filter drops `ro > um` | K5-B70 | guarded |
| DC1_E5 | DES D-c1 | (iii) occluder filter drops `ro <= r_lim + TOL_Z` | K5-B71 | guarded |
| DN1_hatch | DES N1 | wing (i) drops `or a.get_hatch()` | K5-B73 | guarded |

Each deletion turned exactly its target red, and no other control in the set changed.

---

## 1 The Software Engineer

| Finding | Status | Evidence |
|---|---|---|
| FIX 1 S4-1 E3, E4 | CLOSED | S4-1-B2 and S4-1-B3 match post (P5f). E3 and E4 deletions red (P5f). SW1_drawn red on S4-1-B2. |
| FIX 2 S4-2 (c) E5 | CLOSED | S4-2-B5 matches. SW2_grip red. |
| FIX 3 sweep (s1) E7 | CLOSED | K5-B64 matches. SW3_s1 red. |
| FIX 4 S4-2 (a) E12 | CLOSED | S4-2-B4 matches. SW4_core red. |
| FIX 5 RPT from the computing function | CLOSED | kept_axial and seat_bearing T_kept read checks_s4.s3_loads → checks_s3.loads. The s4 r0 record carries deps.spec_read [s3_spec.yaml 015AA79EDC25], and the printed text "1287.05 / 1104.16 N" is unchanged (P5f). DEPS-Z5 is red on the pre-change code and under both deletions (P5f at the merge, SW5_deps at the source). |

Class repeats: none.

Rules signed: the five FIX items add Bs and one Z on existing branches. There is no new rule to sign. FIX 5 basis: SIGNED.

New findings from the fix pass: none. Ceremony: the 20 new controls are one per branch, and the full set ran 154.6 s, inside 200 s. No pruning call.

Verdict: **SIGNED** (5/5 closed). My earlier NOTES 1, 3, 4 and 5 stay carried to P6 by name, as the P5f section 5 lists them. NOTE 5 is now urgent: P6 must apply `x1_edits_at_p6` to the live s4 spec and delete the `p6_state` call in the same edit.

---

## 2 The Topologist

| Finding | Status | Evidence |
|---|---|---|
| F1 (a) tick contained | CLOSED | `tick: wall`. The drawn ticks equal the wall chords in both figures: fig 1 [50.500, 62.408] and [-59.234, -50.500]; fig 2 [53.000, 62.408] and [-59.234, -53.000] (P5f, MEASURED). K5-B65 matches. TF1_t_tol red. |
| F1 (b) (ii) union | CLOSED | (ii) samples the line at <= 0.5 against union_chords of the side pieces. K5-B66 (u -59.80) matches; the P5f `ii` deletion is red. |
| F1 (c) (i0) behind | CLOSED | Spec lint cos(theta) < 0. K5-B67 (theta 82) matches; the `i0` deletion is red. |
| F1 (d) tick dashed | CLOSED | K5-B68 matches; the `t_dash` deletion is red. The fixture render shows the +u tick dashed. |
| F2 (a) edges, not vertices | CLOSED | Exact z coverage per drawn edge. K5-B69 (relief deleted) matches. TF2_vertex, the pre-F2 vertex reading, is red. |
| F2 (b) plane_cuts ignored | CLOSED | The `iii_cuts` deletion (plane_cuts applied) turns K5-Z8 red on the false gap 145.59 to 146.39 (P5f). The Z holds the half-profile reading. |
| F2 (c) plane_cuts theta lint and the 45 deg premise | CLOSED | K8-B108 (theta 270 on +u) and K5-B72 (u +-60, "(iii p)") match; the deletions are red (P5f). The s4_spec pocket_rim theta "180 / wingnut.wing_count" = 90.0. |
| F3 sweep (s1) | CLOSED | K5-B64. SW3_s1 red. |
| F4 between order | CLOSED | min(a, b) > 0. S4-3-B8 (a -0.85, b -0.35) matches. TF4_between, which restores the product form, is red. |
| F5 omit: hidden | CLOSED | (h1), (h2), (h3) at every figure pose. Every s4_spec entry is clean in both figures (P5f dry run). K8-B109, B110, B111 match. TF5_h3 red. The entry table follows my P5T section 9, with the witness ruler on the receiver, the 330 window in front and theta 37 off_plane [+49.89, +70.01]. |

The P5f sample counts (inserts 72 per figure, not 216) are a counting difference at t = 0, where the -t, 0 and +t samples coincide. The sample points are the same as mine. Accepted.

Class repeats: none.

Rules signed:

| Rule | Verdict |
|---|---|
| Tick admission collet:slits (i0), (n), (i), (ii), (iii), (iv), (t) | SIGNED |
| Wing (iii) by exact edge coverage, half-profile occluders, premise (iii p) | SIGNED |
| plane_cuts theta lint (K8) | SIGNED |
| Sweep sub-artist (s1) to (s3) | SIGNED |
| between, ordered form | SIGNED |
| not_drawn omit: hidden (h1) to (h3) | SIGNED |

New findings from the fix pass: none at FIX level. One NOTE goes to P6, as the P5f section 5 states. The staged `step1.4_p6_staged/s3_spec.yaml` wingnut plane_cuts entry has no theta, so the new K8 lint fails S3 r8 unless `theta: "180 / wingnut.wing_count"` lands with it. My N1 to N7 stay carried by name.

Verdict: **SIGNED** (F1 to F5 closed).

---

## 3 The Designer

| Finding | Status | Evidence |
|---|---|---|
| D-c1 (wing (iii) terms r_out > \|u\| and r_out <= -x_band[1]) | CLOSED | K5-B70 (wing.u +-90) and K5-B71 (x_band near end -70) match. Each goes red only on its own term: DC1_E4 turns only K5-B70 red, and DC1_E5 only K5-B71. The F2 rewrite keeps my reason substring "(r_out <= 70.00". |
| N1 hatched wing | CLOSED (landed at P5f) | Wing (i) adds `or a.get_hatch()`. K5-B73 matches. DN1_hatch red. |
| N2 legend "brass" with no pattern | open, carried to P6 by name | label templates at P6 |

Class repeats: none.

Rule signed: -X wing admission by declared x_band (O3), branches (w0), (i), (ii) and (iii) with all three terms and premise (iii p): **SIGNED**.

### Confirmation 1: F1 tick form `tick: wall`

CONFIRMED.
- The slit is a radial through-cut. Seen in section from behind, its closed end spans the wall from bore to outer surface, so a dashed tick across the full wall chord is the faithful outline.
- In the fixture render (+u, figure 1) the dashed slit line runs from the open top face down to a dashed tick that meets the bore edge and the cone edge. It reads as one hidden L, the end of a cut through the wall.
- A fixed-length tick would mean either a short dash floating inside the wall or one that leaves the part. The 8.00 tick at d 105, against a 6.234 wall, did the second.
- The chord-length tick changes length with the wall (11.908 at +u, 8.734 and 6.234 at -u). That is correct, because the tick describes the wall.

### Confirmation 2: no operator-task row needs a feature omitted as hidden

CONFIRMED. The gameplan rows that name S4 are:
- set a short core;
- advance for a slice;
- take the slice off (N6, open);
- change a collet (liner option).

They need:
- the collar top and holder bore (drawn);
- the wing nut, backed off and re-tightened, with sweep r 115 (wings drawn: the -X wing hidden, sweep lines dashed);
- the carrier and core stack (drawn);
- the liner (drawn in figure 2).

None of the omit: hidden features is needed:
- holder M6 inserts and collar holes: assembly fasteners, not operated at load;
- witness ruler and flange tick: the operator reads them from the side, so they belong in S1 side or S6, as the spec reason states;
- tommy bosses: the rows turn the nut by its wings;
- slits other than the two ticks;
- washer windows at 210 and 330.

The figure note names every omitted head, so a reader who looks for them finds the omission stated.

Verdict: **SIGNED** (D-c1 and N1 closed; both confirmations given; N2 to P6).

---

## Gameplan lines to change

none. The K5, K8 and S4-1 to S4-3 row texts, including the `tick: wall` form, are carried by step1.4_engineer_redfirst_fixes.md items 1 to 7.
