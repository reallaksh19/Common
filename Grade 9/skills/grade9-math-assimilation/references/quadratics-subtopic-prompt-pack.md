# Quadratics Assimilation — Five-Topic Prompt Pack

Use these prompts with `Grade 9/skills/grade9-math-assimilation/SKILL.md`.

Common required inputs for every prompt:

- `Grade 9/skills/grade9-math/SKILL.md`
- `Grade 9/skills/grade9-math/references/partial-knowledge-assimilation-concept-map.md`
- `Grade 9/skills/grade9-math-assimilation/SKILL.md`
- `Grade 9/skills/grade9-math-assimilation/references/quadratics-v2-retrace-runbook.md`
- `Grade 9/Mathematics/NMTC Preliminary/03_Concept_Books/Algebra/Polynomial_Root_Structure/Quadratics_Assimilation_Concept_Map.md`
- `Grade 9/Mathematics/NMTC Preliminary/03_Concept_Books/Algebra/Polynomial_Root_Structure/Polynomial_Root_Structure_Source_Coverage_Map.md`
- `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`
- PR #34 benchmark history

Common instructions:

1. Read all authorities before authoring.
2. Model a learner with about 50% prior knowledge.
3. Create the subtopic concept map before prose.
4. Use `RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`.
5. Force an attempt before hints.
6. Fade `H3 -> H2 -> H1 -> H0`.
7. Make First-Step Reference a compression layer after concept teaching.
8. Preserve source/provenance roles; never silently repair defects.
9. Independently recompute answers.
10. Render PDFs, visually inspect all pages, preflight, and record QA.
11. Use benchmark PDFs as quality comparators only; do not copy text/layout.
12. Leave classroom calibration `NOT_RUN` unless real evidence exists.

---

## Prompt 1 — Foundations and Representations

GitHub issue: #36

> Act as a Grade IX/X mathematics teacher and competitive-foundation pedagogy designer. Rebuild the Quadratics **Foundations & Representations** unit for a learner who already knows about half the topic. Read all common required inputs first. Create the subtopic concept map before writing prose. Teach standard form, factor form, roots, graph/vertex view, coefficient/root information, and equation-as-rewriting-relation as connected representations. Make the student discover that **the requested information chooses the representation**. Use same-quadratic/different-target contrast pairs. Diagnose the quadratic-formula reflex. Require first-move-only attempts before worked routes. Fade H3->H0. Produce the Assimilation module, First-Step Reference, recognition lab, transfer items, answer/diagnostic key, rendered PDF, and QA. Compare against the benchmark only for pedagogy/completeness/production quality.

---

## Prompt 2 — Discriminant and Repeated Roots

GitHub issue: #37

> Act as a Grade IX/X mathematics teacher. Build the Quadratics **Discriminant, Repeated Roots & Parameter Conditions** unit for a learner who remembers `D=b^2-4ac` but does not fully understand it. Read all common required inputs first and create the concept map before prose. Reconnect the formula to the quadratic formula, then to `sqrt(D)`, root count, graph intersection, and tangency. Explicitly contrast equal-root questions with minimum/maximum value questions, and root-count conditions with positivity conditions. Make the student translate words to `D=0`, `D>0`, or `D<0` before arithmetic. Use H3->H0 fading, independent recognition/first-line practice, and disguised parameter transfer. Keep `NMTC-BH-P-2018-Q07` as bonus mechanism evidence only. Produce student source, First-Step Reference, answer/diagnostic key, rendered PDF, and QA.

---

## Prompt 3 — Vieta and Root Invariants

GitHub issue: #38

> Act as a Grade IX/X mathematics teacher and Olympiad-foundation problem designer. Build the Quadratics **Vieta & Root Invariants** unit for a partial-knowledge learner. Read all common authorities first and create the concept map. Derive Vieta from `a(x-alpha)(x-beta)` so the sign is understood rather than memorized. Teach the symmetry test: if swapping `alpha` and `beta` does not change the target, first try rewriting using `S=alpha+beta` and `P=alpha beta`. Contrast symmetric targets with questions that truly require individual roots. Include reciprocal, squared, cubic and ratio expressions. Diagnose sign-memory, reciprocal-of-sum, and unnecessary-root-solving errors. Ground the mechanism to `NMTC-BH-P-2024-Q14` without copying full source text. Fade H3->H0 and independently audit every answer. Produce the Assimilation module, First-Step Reference, recognition lab, transfer bank, PDF, key, and QA.

---

## Prompt 4 — Transformed / Integer Roots / Structural Reduction

GitHub issue: #39

> Act as a Grade IX/X mathematics teacher and NMTC Preliminary pedagogy designer. Build the Quadratics **Transformed Roots, Integer Roots & Structural Reduction** unit for a learner who can solve quadratics but does not yet see the deeper structural shortcuts. Read all common inputs and create the concept map first. Teach shifted/reciprocal/squared roots using transformed sums/products; distinguish transformed roots from shifted function input; teach positive-real vs positive-integer restrictions using sign, factor-pair, parity/divisibility and AM-GM structure; teach a quadratic relation as a rewriting machine that reduces high powers without explicit root solving. Ground to the qualified source IDs in the source map. Preserve `NMTC-BH-P-2025-Q20` as source-conflict evidence only. Include at least four decision-boundary contrast pairs, H3->H0 fading, non-identical transfer, independent answer audit, rendered PDF, teacher diagnostics, and QA.

---

## Prompt 5 — Mixed Mastery and Transfer

GitHub issue: #40

> Act as a Grade IX/X mathematics teacher, NMTC Preliminary assessment designer, and diagnostic pedagogy specialist. Build the Quadratics **Mixed Mastery & Transfer** capstone after the first four subtopics. Read all common inputs. This is an H0 independence test: student-facing items must not reveal the method or chapter label. Build six layers: recognition-only, first-line-only, mixed solve, contrast/WHY-NOT, non-identical transfer, and source-integrity discrimination. Use the six-question assimilation test as the mastery definition. Include at least 15 recognition prompts, 12 first-line prompts, 12 unlabelled solve items, 6 contrast pairs, 6 transfer items, and 2 source-integrity items. Produce a separate teacher diagnostic key with recognition/first_move/representation/calculation/domain/source_integrity/checking/time_pressure tags and explain why the efficient first move is preferred. Independently audit every answer, render student and teacher PDFs, and report PASS/PARTIAL/NOT_RUN without inventing timing or qualification thresholds.

---

# Recommended agent execution order

`#36 -> #37 -> #38 -> #39 -> #40`

Do not combine the five issues before each passes its own internal QA.
