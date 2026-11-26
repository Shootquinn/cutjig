## Corrections to the brief

1. **TP1.3-3 is closed on S2 r7 by (e1), not by the enclosure exemption.** With the r7 ring text (366.84, -73.98) and the r6 anchor (209.75, -10.33), guide_tie_a contains and encloses the anchor, so the D1 exemption skips it and rule (e) reads clean. The case fails only on (e1): "on hidden ink of a row with visible ink" (MEASURED). K4-B14 plants exactly this and is the right control.
2. **The D1 exemption has a 0.05 mm band at every counted outline edge, and the Design Notes 30 defect passes through it.** `outline_encloses` accepts an anchor within TOL_Z *outside* a convex piece. An anchor on visible ring rim 0.01 to 0.047 mm outside tie a passes (e1), is exempted from tie a by the enclosure rule, and its last quarter runs 41.3 mm inside tie a with no K4 issue. At 0.058 mm outside, (e) fires (41.3 mm) (MEASURED). There is no live case. New FIX TP1.3-8, section 3.
3. **The stand-in premise as the Engineer worded it is broader than the code.** The code makes a stand-in's line count as visible only where no cover contains the anchor: `row_visibility` passes the stand-in artist's own covers to (e1). The wording "a stand-in's convention line is visible ink" drops that condition. Section 4.

Tags: runs MEASURED 2026-11-26 with Python 3.12 and matplotlib 3.11.2, on scratchpad copies of `docs/sketches/` with `params.yaml` above them (`scratchpad/p1rr/base`, `del1`, `del2`, `dr8`). The `sketch_common.py` SHA-256 is 0f54ead9b409…, equal to the Engineer's "after" value. Probes are in `scratchpad/probes/`. Nothing under `docs/sketches/` was edited. Hand values are DERIVED. Thresholds proposed here are DECLARED.

## 1 TP1.3-1: annulus radial step ≤ 2.5 mm: CLOSED

**Code.** In `_annulus_samples`, m = max(5, ceil(width / 2.5) + 1). When m = 5 it uses the COVER_RINGS fractions. Otherwise it uses m fractions evenly spaced from 0.02 to 0.98.

**Bound (DERIVED).**
- m > 5: step = 0.96 w / (m - 1) ≤ 0.96 w / (w / 2.5) = 2.4 mm.
- m = 5 (w ≤ 10): the widest COVER_RINGS gap is 0.25 w ≤ 2.5 mm.
- A sweep over w = 0.01 to 400 mm in 0.01 mm steps gives a maximum interior step of 2.500 mm, reached at w = 10 (MEASURED).

**Live annuli in S2 r7 (MEASURED widths):**

| Row | Width (mm) |
|---|---|
| ring | 110.0 (two artists) |
| bearing | 23.8 |
| gear | 36.32 |
| gear_hub | 13.8 |
| drill_tube | 3.175 |

On the ring that gives 45 fractions, step 2.4 mm.

**Deletion test** (copy `del1`: `m = len(COVER_RINGS)`; selected controls, MEASURED):

| Control | Base | Deleted |
|---|---|---|
| K8-B52 | fires 1, match | clean, **match NO** |
| K8-Z13 | clean | clean |
| K8-B6, B32, B39, B47, B49, B51, Z12 | match | match |

Only B52 detects the deletion. Z13 stays clean when the code is deleted, because the renderer and K8 share the sampler and agree on the coarse samples. That is expected: B52 is the control for this change.

**NOTE TP1.3-9 (S3).** The edge band, from the rim to the outermost sample fraction, is 0.02 w. It is 2.2 mm on the ring and exceeds 2.5 mm for w > 125 mm (DERIVED). No live annulus is that wide. At S3, if an annulus wider than 125 mm is drawn, use the fractions 1.25 / w and 1 - 1.25 / w at the ends.

## 2 TP1.3-2: cover clause (5): CLOSED

**Code.** In `cover_issues` (5), an opaque fill counts as inverted when its row has no z_max, or a z_max below the artist's by more than TOL_Z. K8 then fails on any drawn sample under an inverted fill, with one line per artist.

**Deletion test** (copy `del2`: `if False and inv:`; MEASURED):

| Control | Base (planted) | Deleted |
|---|---|---|
| K8-B51 | fires 3 (3), match | clean, **match NO** |
| K8-B6 | 3 (3), match | 2, **match NO** |
| K8-B32 | 5 (5), match | 3, **match NO** |
| K8-B39 | 7 (7), match | 3, **match NO** |
| K8-B49 | 7 (7), match | 3, **match NO** |
| K8-B52, Z12, Z13, B47 | match | match |

The counts 3, 5, 7, 7 are as signed at P1Rt. Every one of the five controls detects the deletion.

## 3 TP1.3-3 under D1: ring / tie a re-run on S2 r7

The r7 ring leader runs from text (366.84, -73.98) to anchor (205.96, -40.97): L 164.2 mm, last quarter 41.1 mm (MEASURED). The ring row is not wholly hidden, and (e1) passes: the anchor is on visible ink.

| Outline entered by the last quarter | mm | z_max | Counted (z above ring 1161.84 by > 0.05) | Exempt |
|---|---|---|---|---|
| base_frame | 41.1 | 60 | no | n/a |
| base_plate | 41.1 | 72 | no | n/a |

**Ring leader end-quarter length inside any outline it is not exempt from: 0.0 mm (MEASURED).** Tie a is not entered. TP1.3-3 is CLOSED on S2 r7 under the orchestrator's ruling. The r6 anchor with the r7 text gives (e1) and 42.4 mm in tie a, which the exemption skips (Correction 1).

The other leaders on r7 have no outline entered without exemption (MEASURED, every label):
- descent_stop (wholly hidden): enters bracket_guide_a 50.2 mm and ring 10.9 mm, both containing the anchor.
- drill_head (wholly hidden): enters ring 59.1 mm and gear 36.3 mm (both enclose), bearing 10.9 mm and gear_hub 1.0 mm (both contain).
- operator_sector (zone): enters base_plate and base_frame 21.0 mm each, both containing the anchor.

**FIX TP1.3-8 (rule (e) premise to the Designer; the Engineer implements). The enclosure exemption must be strict.**
- The reason given for the exemption is that no straight leader from outside reaches the anchor without crossing the outline. That holds only when the anchor lies inside the outer boundary with a margin.
- `outline_encloses` adds +TOL_Z outward. Anchors in the band 0 < d ≤ 0.05 mm outside a convex piece are therefore exempt, while (e1) reads them as visible: `cover_hits` is inclusive only up to d = 0.
- Measured in copy `base`: ring anchor (201.76, 34.40), 0.028 mm outside tie a, text (366.84, 34.40).
  - (e1): none;
  - (e): none;
  - last quarter 41.3 mm inside tie a.
- The same holds at 0.008 mm and 0.047 mm. At 0.058 mm, (e) fires guide_tie_a 41.3 mm.
- How the band is reached: placer candidates are ink samples at most 2 mm apart, edge ends included. An edge lying 0 to 0.05 mm off a higher outline (a plan-contact pair) puts every candidate on it inside the band.
- **Rule:** an outline is exempt only when the anchor and every point within TOL_Z of it lie inside the outline's outer boundary with holes filled. For an annulus that is r ≤ b - TOL_Z. For a visible row, (e1) then leaves only an annulus bore as an exemption, which is the case the stated reason covers. Clause (g) keeps the +TOL_Z `outline_encloses` for naming the cover.
- **Dry-run** (copy `dr8`, `_encloses_deep` in `leader_outline_issue` only, 16 points on a TOL_Z circle; MEASURED):

  | Run | Result |
  |---|---|
  | s2_plan --rev 7 | PNG SHA-256 710f124f35eb…, byte-equal to wip r7 |
  | check_sketch s2 --rev 7 | 19/19 |
  | K4 controls | 20/20 match (Z 4/4, B 16/16) |
  | Band anchors at 0.008, 0.028, 0.047 mm | (e) fires guide_tie_a 41.3 mm |

  **PASS.** The full controls suite was not run on `dr8`. The Engineer runs it when landing the change.
- **B, new (K4-B17):** the ring label at anchor (201.76, 34.40) with text (366.84, 34.40). Red on the current code: (e) and (e1) both clean (MEASURED). Fixed code: "label leader ends inside the outline of guide_tie_a (41.3 mm…)". Leader crossings on that plant are not measured, so the Engineer sets the planted count. **Z:** K4-Z3 and live S2 r7 (clean in the dry-run).

## 4 Half-space view of the DR-1 premise (stand-in phantom line as visible ink)

**What the code does.**
- `row_visibility` adds every stand_in artist to the row's solid list with its own `artist_covers`.
- `anchor_visibility_issue` then requires three things: the anchor within TOL_Z of the stand-in's ink, inside its drawn region, and outside every cover of that artist. The covers are the true outlines of rows higher by more than TOL_Z, plus the opaque fills drawn above.
- For a stand-in, (e1) is therefore the visibility predicate itself, tested point by point at the anchor: p ∉ O for every higher true outline O. Only the line style is exempt (renderer skip, K8 cover (3) exemption).
- The wholly hidden flag still comes from `plan_cover_states`. A stand-in with every sample covered reads hidden, so (e2) and (g) apply to it as to any hidden row.

**Live S2 r7 (MEASURED).**
- guide_tie_a and guide_tie_b: phantom Polygon, state visible, z_max 1285. The only candidate cover from the bounding-box filter is drill_tube.
- Of 741 ink samples per tie at 0.5 mm, 0 lie inside a higher true outline by more than TOL_Z.
- The premise holds on every live sample, and the guide_tie_a anchor (265.04, 93.96) is on uncovered ink.

**Gap left (NOTE, to stand_in_owner, unchanged from TP1.2-17/18).** A partly covered stand-in draws its covered ink in phantom, the same as its uncovered ink, because the renderer skips stand-ins. The figure then misstates visibility there. The anchor test stays correct. No live case.

**Sign: premise SOUND as implemented.** The wording should carry the cover condition: "a stand-in's convention line is visible ink where no cover contains it" (Gameplan lines).

## 5 Signatures

| Item | Verdict |
|---|---|
| Rule 1, opaque-fill clause: cover (5), opaque fill depth premise (TP1.3-2) | **SIGNED** |
| Rule 7, radial half: annulus samples ≤ 2.5 mm across the width, COVER_RINGS kept when m = 5 (TP1.3-1) | **SIGNED** |
| Renderer (opaque-fill visibility, annulus width spacing) | **SIGNED**, with all P1Rt rows 1 to 9 |
| TP1.3-3 (ring leader inside tie a) | CLOSED on S2 r7: 0.0 mm in non-exempt outlines |
| DR-1 stand-in premise | SOUND as coded; wording change below |
| Rule (e) enclosure exemption | **FIX TP1.3-8** (strict margin; dry-run PASS) |
| NOTE TP1.3-9 | annulus edge band 0.02 w > 2.5 mm for w > 125 mm; no live case; S3 |

**Verdict: FIX.** The renderer is signed. The one open item is TP1.3-8, on K4 rule (e), outside the renderer, and its dry-run passes.

## Gameplan lines to change

**l.138 (K4 row), rule cell.** Apply after the Engineer's P1Rf change.

Old:
```
(e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor (outer boundary, holes filled); (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that neither contains nor encloses the anchor (Design Notes 30; Designer P1Rd FIX D1);
```
New:
```
(e1) a row with visible ink (renderer split, certified by K8 cover; a stand-in's convention line is visible ink where no cover contains it) anchors on visible ink and its leader's last quarter lies outside every counted outline that does not enclose the anchor (outer boundary, holes filled); (e2) a wholly hidden row anchors on its hidden ink and its last quarter lies outside every counted outline that does not enclose the anchor (Design Notes 30; Designer P1Rd FIX D1); an outline encloses for (e1) and (e2) only when the anchor and every point within 0.05 of it lie inside its outer boundary with holes filled (1.3 P1Rt recheck TP1.3-8);
```

**l.138 (K4 row), B cell.** Apply after the Engineer's P1Rf change.

Old:
```
K4-B8 re-planted at 1.3 P1Rf (texts below the anchors in reverse radial order) |
```
New:
```
K4-B8 re-planted at 1.3 P1Rf (texts below the anchors in reverse radial order); K4-B17 ring label anchored on visible rim 0.028 mm outside tie a, last quarter 41.3 mm inside tie a (TP1.3-8) |
```

**l.296 (detail 1.3 carried item 4).** Apply after the Engineer's P1Rf change.

Old:
```
re-checks by the Designer and the Topologist, then the fresh M1 (P8);
```
New:
```
re-checks by the Designer and the Topologist (P1Rt recheck `research/sean/cr_scratch/step1.3_topologist_renderer_recheck.md`: TP1.3-1 and TP1.3-2 closed with deletion tests, renderer SIGNED, TP1.3-3 closed on S2 r7 at 0.0 mm, stand-in premise sound as coded, FIX TP1.3-8 rule (e) enclosure margin, dry-run PASS), then the fresh M1 (P8);
```

**l.667 (Design Notes 25, TP1.2-18/19 and N2 renderer row).** Apply after the Engineer's P1Rf change.

Old:
```
landed in S2 r7; awaiting the P1Rf re-checks |
```
New:
```
landed in S2 r7; P1Rt recheck: TP1.3-1 and TP1.3-2 SIGNED (deletion tests), renderer SIGNED, TP1.3-3 closed (ring leader 0.0 mm in non-exempt outlines); FIX TP1.3-8 (rule (e) enclosure strict by 0.05); awaiting the Designer's re-check |
```

**Design Notes 25, TP1.3-4 to TP1.3-7 row (P1Rt insertion).** Append to its text, before the first " | ":
```
; TP1.3-9: annulus edge band 0.02 x width exceeds 2.5 mm above width 125 mm (no live case; end fractions 1.25/w at S3 if one is drawn)
```
