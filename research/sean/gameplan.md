# Cut Jig Configuration and 2D Sketch Gameplan (sean)

**Document(s) under work:** cut jig configuration: 2D sketch set (LLM-PLM section 8.4), then the upper assembly and any base redesign it requires
**Operational guide:** method/operational_guide.md. Contributor: sean. Scratch: research/sean/cr_scratch/. Repository sync rules: section "Repository Sync" at the end of this file; they apply to every step.
**Accumulator file:** none yet; research/sean/accumulator.md is created at Step 0 close
**Other reference files:**
- context/2026-11-24_cutjig_critical_path.md (read first: this week's goal, requirements, open questions, sketch set)
- workorder.md, ASSEMBLY.md, params.yaml, bom_stock_allocation.md
- research/quinn/gameplan.md (Objectives, Design Notes, CAD Test Specification, Source Verification Register; Steps 0 to 7 record)
- supplements/llm_plm_cad.md (section 8.4 sketching phase, 8.4.1 projection checklist, 8.4.2 plot conventions), method/tdd_method.md
**Date:** 2026-11-24
**Current step:** 0 (not drafted)
**lit_review:** no

---

## Start here (from Quinn, 2026-11-24)

Sean leads the cut jig; Quinn reviews. This week's job is to find out what the jig is, on paper, before any more 3D CAD or any cut extrusion.

- **The jig:** a floor-standing, arbor-press-like stand. The core stays upright in a collet at the bottom. The spinning drill (about 800 mm long) travels down over the core and back up, with about 650 mm of travel, so that it can capture a 500 mm core at the end of the project. The core is never inverted, because the test cores are weak cement with no tensile strength.
- **Two modes:**
  - Slice mode: push the core up through a tall collet and cut coaster-thick slices. The collet may be cut along with the core.
  - Capture mode: take one 500 mm core.
- **Material:** on-hand 80/20 30-6060, whole lengths where possible. Lift options are open: arbor press, twin jack screws with Sean's steppers, or something else.
- **Kept:** the collet family, generator, holder, wing nut and receiver. Everything else may be redesigned, and the redesign may change again.
- **Method:** 2D matplotlib sketches first, following LLM-PLM 8.4. The human checks each one for orientation and sense, because the model draws parts upside down and puts the tail on the nose. Start with S1, the whole-jig side view in four poses, which answers whether the jig is tall enough. The full sketch set S1 to S6, the requirements R1 to R18 and the open questions Q1 to Q11 are in `context/2026-11-24_cutjig_critical_path.md`.
- **Week done:**
  - Sketches S1 to S6 have each had a human correction pass.
  - A lift option is chosen, or narrowed to two.
  - Each open question has an answer or an owner.
  - No extrusion is cut.
- **Ask Quinn early:** Q1 (travel), Q2 (drill length and top-end hardware) and Q3 (what spins the drill).

**Update, later on 2026-11-24 (Quinn's decisions):**
- Travel is 650 mm.
- The drill spins on a big bevel ring gear driven by three NEMA 23 pinions at 120 deg. The pinions also carry the drill's weight, with a bushing support ring if needed.
- Everything rides on one ring structure that moves up and down on three jack screws, probably driven by NEMA 17s.
- Lead screws are T8, 800 to 900 mm, under $100 each.

Sketch that configuration; arbor press and hoist are off the table. Details are in section 15 of the critical-path file and Design Note 23 of `research/quinn/gameplan.md`.

Step 0 for the first session: draft the Objectives, Steps, Context Recipes and Design Notes below from `templates/gameplan.md` with the team. Keep this section, and make the sketch set the first step after Step 0.

---

## Objectives

(Drafted at Step 0.)

---

## Steps

| # | Step | Assigned To | Status |
|---|------|-------------|--------|
| 0 | Team wave to draft this gameplan from the critical-path file | The Manager, The Engineer, The Designer, The Systems Engineer, The Software Engineer | Not started |

---

## Context Recipes

(Drafted at Step 0.)

---

## Progress Log

| Step | Date | Notes |
|------|------|-------|
| | | |

---

## Design Notes

(Decisions and every human sketch correction, recorded so the next session does not repeat them.)

---

## Open Questions

See Q1 to Q11 in `context/2026-11-24_cutjig_critical_path.md`; move each here when it is answered.

---

## Repository Sync

Repo: https://github.com/Shootquinn/cutjig (public, all rights reserved). Contributors: quinn, sean. Each contributor has `research/<name>/` holding their gameplan, accumulator and `cr_scratch/`. The design files are shared: workorder.md, params.yaml, ASSEMBLY.md, bom_*.md, report_assumptions.md, build_parts/, tests/, output/, parts_cache/, docs/, context/, reference/. Either contributor may change any shared file; a change to the other contributor's design runs through LLM-PLM like any other change (FCStd wins, sync params first, re-run the tests). Never edit files in the other contributor's `research/<name>/`.

Every step in this gameplan carries these sync points:

1. **Step open:** `git pull --ff-only` before the Manager is spawned. If the fast-forward fails, stop and report to the human. If the pull brought changes to shared design files, the Manager open reads `git log --stat` since the last sync and names what changed.
2. **Save point** (each wave close and the step close, before the inter-step gate):
   ```
   git add -A
   git commit -m "sean: Step N <what finished>"
   git pull --rebase
   git push
   ```
   The rebase lands this machine's commits on top of the other contributor's, so the next `git pull --ff-only` on their machine fast-forwards.
3. **Conflicts:** a rebase conflict in a shared design file (params.yaml, a part script, a test, an FCStd, STEP or STL, ASSEMBLY.md) stops the session; `git rebase --abort` and report to the human. No agent resolves a design conflict.
4. **Background builds:** push a save point before launching a FreeCAD build; push the build's outputs as their own save point when the build finishes. Never commit a half-finished build.
5. **Never** force-push, amend or rebase a pushed commit, or skip hooks. Undoing the other contributor's work is a new change.
6. Scratch files go to `research/sean/cr_scratch/`.
