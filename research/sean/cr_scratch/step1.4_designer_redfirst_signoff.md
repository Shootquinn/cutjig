# Step 1.4 P5D, The Designer: (c) sign-off of R1/R2 (hatch adjacency) and O3 (-X wing admission)

Scratch: `D:\Unleashed Robotics\_scratch\cutjig\open14\p5d\`. Script `del_p5d.py`; results `del_p5d_E1_E2_E4_E5.txt`, `del_p5d_P_E3.txt`. Each edit was made on a fresh copy of docs/sketches in `ws\<id>\`. The probe and dry-run tree is `ws\P\`. Nothing under docs/sketches was edited.

## Corrections to the brief

1. **"Three premise checks" of O3.** My P3a O3 admission has three conditions, (i) to (iii), plus (w0). Condition (iii) itself carries three terms: the z band holds the vertex, r_out > |u|, and r_out <= -x_band[1]. The Engineer's D9 to D12 deleted (w0), (i), (ii) and the whole of (iii), and each went red. My deletion tests go one level down, to the three terms of (iii). Two of the three pass the full manifest (section 2).
2. **E1 and E2 deletions.** The Engineer's D27 and D28 ran `--only` on the target B. I ran the same two deletions on the full manifest, to show that no other control depends on either branch and that the target B is the only guard.

## 1 Hatch adjacency: line family (R2) and the K8 call site (R1)

| Test | Edit | Controls | Red | MEASURED |
|---|---|---|---|---|
| E1 | `out += adj` removed from `section_convention_issues` | full, 531 | K8-B106 only (clean, 0 against planted 4) | Z 119/119, B 407/408, smoke 4/4; 174.0 s |
| E2 | `hatch_family(ha) == hatch_family(hb)` replaced by `ha == hb` | full, 531 | K8-B107 only (1 issue against planted 2; the material clause still fires) | Z 119/119, B 407/408, smoke 4/4; 177.2 s |

- **R1.** K8-B106 builds the S4 figures with `s4_ctx` and removes the receiver's `hatch_variant` in the spec. It reaches the lint through `k8` → `section_convention_issues` on the drawn figures. Before P4, deleting the call site passed 488/488. It now turns K8-B106 red. **R1 CLOSED.**
- **R2.** The compare uses `hatch_family` on both sides, and the reason adds "(line family of 'x')" when the strings differ. K8-B107 plants `////` beside `//` and fires. The string compare fails it. On the live S4 figures, E2 leaves K8-Z20 clean: the S4 patterns are pairwise in different families, as I stated at P2r. **R2 CLOSED** (the class ruled by the orchestrator).
- Scope carried to P6, as listed by the Engineer: S3 r8 and S1 r9 declare the gap, and S1 uses the no-section_class form. Each takes the remedy Bs from P2r section 1.4 (S3 receiver variant removed; S1 receiver `//`; S1 descent_stop `////`).

**Adjacency lint (form, text, K8 wiring, family compare): SIGNED.**

## 2 -X wing admission by declared x_band (O3)

Live values (DERIVED from the spec): wing u -7.00 to 7.00, z_A 113.09 to 153.09; x_band [-115.00, -83.14]; r_lim = -x_band[1] = 83.14. Body, relief, pocket_rim and plate have r_out 83.14 (`wingnut.body_od / 2`). The skirt r_out exceeds 83.14, and its z band lies below the wing.

| Test | Edit (term of (iii) removed) | Controls | Red | MEASURED |
|---|---|---|---|---|
| E3 | z band holds the vertex | 7 (K5-B57 to B60, K5-Z8, K8-Z20, S4-FULL) | K5-B60 (clean, 0 against planted 2) | 11.1 s |
| E4 | r_out > \|u\| | full, 531 | **none** | 531/531 match; 168.9 s |
| E5 | r_out <= -x_band[1] | full, 531 | **none** | 531/531 match; 265.1 s |

- E3: K5-B60 deletes body and plate. Without the z term, relief and pocket_rim, at r_out 83.14 > 7, "cover" the wing ends at 113.09 and 153.09, outside their z bands. B60 guards that term.
- E4: no control places a wing vertex at |u| >= r_out. The wing is 14 wide against a body radius of 83.14, so the live drawing and every B sit far inside this term.
- E5: no control declares an x_band whose near end lies inside the row's own material. That term is the premise that the declared band lies outside the row's section, so the dashed wing is never a hidden line drawn through the row's own solid. Without it, a wing declared at x -70 to -115 (body to r 83.14) passes as "hidden behind the body" while it runs through the body.
- Probe (not a deletion): the wing drawn dashed and unfilled but with hatch `//` reads clean under K5 (P5D-P1) and under K8 (P5D-P3). See NOTE N1.

**Wing admission: NOT SIGNED** until FIX D-c1 lands. Branches (w0), (i), (ii) and the z term of (iii) are signed.

### FIX D-c1. One B per untested term of wing (iii)

Two Bs, both dry-run (MEASURED, `ws\P`, `ws\E4`, `ws\E5`; fixture text below, manifest rows as in `del_p5d.py`):

| B (P5f assigns the K5 ids) | Planted | Reason substrings | Live code | E4 (r_out > \|u\| removed) | E5 (r_out <= r_lim removed) |
|---|---|---|---|---|---|
| wing \|u\| past r_out | spec `wing.u: ["-90", "90"]`, drawn so | "(iii)" | fires 2 (both figures), match | **clean, red** | fires 2, match |
| x_band near end inside the body | spec `wing.x_band: ["-wingnut.span / 2", "-70"]`, wing drawn as live | "not occluded by a section_true piece of wingnut (r_out <= 70.00)", "(iii)" | fires 2, match | fires 2, match | **clean, red** |

Each B goes red only on its own deletion and matches on the live code.

```python
def p5d_wing_wide():
    def sm(sp):
        r = next(r for r in sp["features"] if r["id"] == "wingnut")
        r["wing"]["u"] = ["-90", "90"]
    return s4_ctx(spec_mut=sm)

def p5d_wing_band_inside():
    def sm(sp):
        r = next(r for r in sp["features"] if r["id"] == "wingnut")
        r["wing"]["x_band"] = ["-wingnut.span / 2", "-70"]
    return s4_ctx(spec_mut=sm)
```

No code change and no spec change: two fixtures and two manifest rows, planted 2 each. The loop cap allows this FIX because two deletion tests passed.

### NOTE N1 (to P6, carried by name; no FIX under the loop cap)

- Wing (i) reads "unfilled" as `get_fill()` False. A hatched outline is unfilled to matplotlib, but it reads as a cut piece: a hatched rectangle behind the plane tells the reader "this is cut material", which is the opposite of the hidden convention.
- The P5D-P1 and P5D-P3 probes read clean.
- Remedy at P6: add `or a.get_hatch()` to the (i) condition, with the hatched-wing B (P5D-P1 fixture, reason "(i)", planted 1).
- The same reading of "unfilled" applies to the K8 cover clause and the slit and sweep lines. The slits and sweep are Line2D and carry no hatch, so the hole is the wing's only.

## 3 not_drawn entries the Engineer rewrote: the shape view

The Topologist rules the beyond band and the omit form. On shape:

| Entry | Where it lies (DERIVED from the spec) | Shape view |
|---|---|---|
| base-frame rails, `deferred, owner: S3` | in the plane at \|u\| 244 to 304, outside the crop u +-130 | Correct. Drawn in S3; S4 is cropped to the base stack. |
| +X wing, `off_plane`, x [83.14, 115] | in front of the plane, cut away | Correct. The -X wing drawn hidden, labelled with the span, tells the reader the nut has two wings across 230. |
| receiver key slot, holder key, collet foot key (theta 37) | in front (x > 0) | Not drawn is right. The part sits in front, so its form is off_plane with a front x band or rows, not a deferral. A "P4" owner names a stage that has closed. |
| holder M6 inserts and collar holes (theta 135, 225; x -43.84, u +-43.84) | behind the cut face of the holder flange | Not drawn is right. They are hidden detail behind a cut face. ASME Y14.3 omits hidden lines in a section unless they are needed to read it, and these are not needed. |
| witness ruler and flange tick (theta 127; x -43.35, u 57.53) | behind the cut flange face | Not drawn is right, for the same reason. The ruler is an operator signifier. It belongs in the view the operator reads it from (S1 side, or S6), and the figure note names it. |
| wing-nut tommy bosses (theta 135, 225) | behind the cut body face (\|u\| < 83.14) | Not drawn is right. The wings carry the turning affordance in this figure. |
| collet slits other than the two ticks | inside the cut collet, behind the plane | Not drawn is right. The two declared ticks (collet:slits) are the signifier that the collet is slit, and twelve dashed lines would bury the cone. |
| washer notch, pads, tab, windows at 210 and 330 | notch and tab in front; windows past the band; pads unplaced | Not drawn is right. The theta 90 window is shown by the absent +u pocket rim, and the figure note says so. |

- The figure note names all 12 heads (process rule (b) holds; MEASURED, s4_spec.yaml figure_note).
- The shape answer for the five hidden entries is one convention: hidden detail behind a cut face is not drawn, except declared sub-artists (the slit ticks and the -X wing).
- I recommend stating that convention once in `section.convention.omitted`, so that these entries stop depending on a "P4 (TP1.3-12 converse, Topologist P5T)" owner. The omit form that carries it is the Topologist's ruling.

### NOTE N2 (to P6, label templates)

The figure-note hatch legend reads "brass, plastic oo" with no brass pattern. A legend entry without its pattern does not map the hatch to the material. The legend should read "brass .." as in S3, or drop brass if S4 draws no brass part.

## 4 Signatures

| Rule | Verdict |
|---|---|
| Hatch adjacency by line family (R2) | SIGNED |
| Adjacency through the K8 call site (R1) | SIGNED |
| -X wing admission by declared x_band (O3) | NOT SIGNED: FIX D-c1 (two Bs, dry-run clean) |
| not_drawn rewrites, shape | No shape objection. Omit form to the Topologist. Convention statement recommended (section 3). |

## Gameplan lines to change

none. The K5 row text for the two D-c1 Bs is written by the P5f fix pass when it assigns their ids.
