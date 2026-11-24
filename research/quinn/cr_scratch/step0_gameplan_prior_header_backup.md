# Core Cutter Test Jig Gameplan

**Document(s) under work:** workorder.md (core cutter test jig: base, core holder, wing nut, collet family; 3D models and technical report)
**Operational guide:** method/operational_guide.md
**Accumulator file:** none, new project
**Other reference files:**
- workorder.md
- supplements/llm_plm_cad.md (CAD work is active)
- method/tdd_method.md
- SBIR folder: C:\Users\Quinn Morley\OneDrive\PROJECTS\Planet Enterprises\NIAC\BOREBOTS\Unleashed Robotics\2026 PROPOSALS\2026 SBIR\ (cutter geometry and requirements; see especially "Iris Core Cutter and Retention Mechanism for Stratigraphy-Preservation Plan.docx", the proposal PDFs, context/, and documentsfromcoloradoschoolofmines.zip)
- Rigged drill model: C:\Users\Quinn Morley\OneDrive\PROJECTS\CC\gpr (locate the rigged animation model; the drill is being redesigned in 6.00 in OD / 5.75 in ID tubing)
**Date:** 2026-11-08
**Current step:** 0
**lit_review:** no

---

## Objectives

1. Review workorder.md as the contract and have the team populate the rest of the gameplan from it (Step 0, drafting variant, A.6.4).
2. Initial work: base, core holder, wing nut, and a collet family for 90 to 105 mm cores, as 3D models.
3. A concise technical report (executive summary crossed with an engineering-school project).
4. A subsequent step scoped jointly with the human for the drill-holding upper assembly.

---

## Steps

| # | Step | Assigned To | Status |
|---|------|-------------|--------|
| 0 | Team reviews workorder.md, locates and reads the cutter and drill source material, and populates the remaining gameplan (steps with TDD stages, Assigned To, context recipes, document structure, echo site registry, open questions). The Engineer plans at full scale and writes it from `templates/gameplan.md`; The Software Engineer revises for test suite, outline, and scripted checks; the rest of the team reviews; The Engineer revises; The Manager closes. | The Manager (open, close), The Engineer (plan, write), The Software Engineer (tests), The Systems Engineer, The Loftsman, The Topologist, The Designer (review) | Not started |

Steps after Step 0 are written by the team during Step 0.

---

## Context Recipes

| Step | Agent | Files / Excerpts |
|------|-------|-----------------|
| 0 | The Manager | workorder.md, this gameplan, method/operational_guide.md (A.4, A.6, A.12 roster), accumulator (none) |
| 0 | The Engineer | workorder.md, templates/gameplan.md, SBIR folder cutter documents, rigged drill model in `gpr`, supplements/llm_plm_cad.md, method/tdd_method.md |
| 0 | The Software Engineer | workorder.md, the Engineer's draft gameplan, method/tdd_method.md |
| 0 | Reviewers | workorder.md, the revised draft gameplan, the domain-relevant source files |

---

## Progress Log

| Step | Date | Notes |
|------|------|-------|
| 0 | 2026-11-08 | Opened. Work order locked as workorder.md. |

---

## Design Notes

- Drill tubing: 6.00 in OD, 5.75 in ID (1/8 in wall) before flights. Cutting face is out of scope.
- Cores are prefabricated by the Colorado School of Mines; the jig does not drill them.
- Core nominal 100 mm; collet range 90 to 105 mm, one collet per diameter.

---

## Open Questions

- 80/20 profile series and printer bed size / material (the Engineer proposes defaults if the human does not specify).
- Collet diameter increments (default proposal: 90, 95, 100, 105 mm).
