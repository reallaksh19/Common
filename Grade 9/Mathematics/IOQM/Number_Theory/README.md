# IOQM Grade 9 — Number Theory

This is the domain workspace for the PR #140 question-driven rebuild of the Grade 9 IOQM Number Theory study guide.

## Current build

`v5 / phased rebuild — Phase 3B full student-book scale-up complete; Phase 4 integrated audit next`

The project is deliberately separated from `01_Source_Extracts/`: source recovery remains evidence; this folder owns the integrated Number Theory learner product and its build data.

## Folder map

- `Phase_1/` — frozen architecture, PR140 profile, phase plan, and Phase 1 foundation/custody review.
- `Phase_2/` — rebuilt teaching architecture, mixed method-selection layer, Advanced Worked Bridges, and Phase 2 review.
- `Phase_3/` — student-experience prototype plus full student-book scale-up and Appendix A/B/C repackaging work.
- `corpus/` — frozen reusable Appendix A/B corpus artifacts. Mathematical stems are not rewritten except for separately documented source corrections.
- `data/` — Appendix A/B registries, badge/hint metadata, custody hashes, question-to-method matrices, orphan-method audits, and visual-pedagogy manifests.
- `../01_Source_Extracts/ALLEN_Number_Theory_Marathon_2026/` — recovered marathon/source evidence.

## Frozen corpus policy

- Appendix A: 90 local items `NT-Q001`–`NT-Q090`.
- Appendix B: 20 reliable-source challenge items `B01`–`B20`.
- Mathematical stems are frozen for the rebuild except for separately documented source corrections.
- Badges, adaptive H1/H2/H3 hints, layout, and useful structural figures may be improved.
- `NT-Q084`–`NT-Q090` are syllabus-completion items, not claims about ALLEN video numbering.

## Phase 1 saved state

- Appendix A registry: 90/90.
- Appendix B registry: 20/20.
- Appendix B frozen corpus source saved under `corpus/`.
- PR140 profile and phased rebuild plan saved under `Phase_1/`.
- Phase 1 Foundation Review saved under `Phase_1/`.
- Appendix B method matrix saved under `data/`.
- Question-level stem hashes and custody metadata retained.

## Phase 2 saved state

- Stable Number Theory teaching skills: **36/36** taught with reconnect -> missing IOQM link -> mechanism -> first useful line -> non-identical example -> contrast -> legality/check.
- Advanced Worked Bridges: **16/16** rebuilt to the PR140 bridge contract.
- Appendix A orphan-method audit: **90/90 PASS at Phase 2 teaching-architecture level**.
- Missing stable support IDs: **0**.
- Appendix A visual decisions: **90/90**.
- `VISUAL_HELPFUL`: **18** questions; `TEXT_DOMINANT`: **72** questions.
- Teaching-layer structural visual specifications: **16/16**.
- `ORPHAN_METHODS_PHASE2 = 0`.

Phase 2 does **not** constitute the final self-sufficiency PASS.

## Phase 3A saved state

The student-facing design was prototyped against the supplied Algebra reference before scaling the full book.

The 16-page prototype contains:

1. a four-page Number Theory 3-Day Simple Navigator;
2. a 10-item first-move Quick Check;
3. a weak-topic -> stable-skill -> practice routing map;
4. three representative rich reference-core chapters;
5. a simple student support map;
6. five redesigned Appendix A pages covering frozen stems `NT-Q001`–`NT-Q012`.

The PDF was rendered at 200 dpi and all 16 pages were visually inspected. Two table-flow defects found during rendering were repaired before the Phase 3A review state.

## Phase 3B saved state

The accepted Phase 3A grammar has now been applied to the complete student-facing book.

Current Phase 3B student-book draft contains:

- **4-page Navigator** with first-move diagnostic routing and fading-hint protocol;
- **36 stable core skills** in the rich semantic page grammar;
- **30 Advanced Worked Bridges** (`NT-A01`–`NT-A30`), expanded from the initial 16 to close specific difficult/mixed transfer gaps;
- **90-question student support map**;
- **Appendix A: all 90 frozen questions**, with difficulty/family badges, adaptive H1/H2/H3, structural visuals where helpful, and answer key;
- **Appendix B: all 20 reliable-source questions**, with PYQ/difficulty/family badges, adaptive hints, and answer key;
- **Appendix C: exactly 2 pages**, containing formulas, theorem hypotheses, first-line router, and final legality checklist.

Phase 3B PDF preflight:

- 90 A4 pages;
- openable, unencrypted;
- fonts embedded;
- PDF outline present;
- SHA-256 `93e0eb483da389f73053b27993eb2328a4ecff1235b91f690bc266dbbc8a4f82`.

The reviewer-style Appendix B method-coverage table is deliberately **not** in the student section; it moves to the Reviewer / Build Dossier in Phase 4.

Phase 3B does **not** yet claim final PR140 self-sufficiency PASS.

## Phase 4 next

Run the integrated PR140 gates against the actual Phase 3B student book and build the Reviewer / Build Dossier for inclusion in the final PDF:

1. Appendix A question-to-method / orphan-method audit: 90/90;
2. Appendix A hint audit: 90/90;
3. Appendix A visual-pedagogy audit against rendered figures: 90/90;
4. Appendix A custody: 90/90;
5. Appendix B source custody / method coverage / hint audit / independent answer recomputation: 20/20;
6. source ledger, matrices, visual manifest and self-sufficiency report inside the final PDF;
7. no final PASS declaration if any row remains PARTIAL/FAIL.

## Final PDF requirement

The final PDF will contain both:

1. the student book; and
2. a reviewer/build dossier containing the profile, matrices, custody/source ledger, self-sufficiency audit, visual manifest, and final QA record.

## Hard gate

No final PDF until all PR140 content gates pass with no PARTIAL/FAIL rows.
