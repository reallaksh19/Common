# Grade 9 Methodology v2 — Research Program

This folder contains the staged Deep Research program for developing **Grade 9 Methodology v2**.

The research is professional methodology research **for a Grade 9 learning system**. It is **not** a Grade 9 student assignment, school project, marking exercise, or lesson plan.

## Frozen baseline

Research should evaluate the repository at commit:

`cadf66e32dfef5e04c7213d9d1fe45750ee8c08f`

Do not evaluate a moving `main` branch unless a later prompt explicitly changes the baseline.

## Research sequence

1. `R1_Difficulty_and_Question_Engineering.md`
   - cognitive difficulty;
   - expert pre-calibration;
   - anchor-to-candidate equivalence;
   - same-level and challenge construction;
   - item-generation taxonomy;
   - Core-N allocation;
   - duplicate/near-duplicate control.

2. `R2_Learning_Sequence_Scaffolding_Diagnostics.md`
   - worked examples;
   - fading and hints;
   - productive struggle;
   - misconceptions and diagnostics;
   - retries and transfer;
   - retrieval practice;
   - spacing, interleaving, mixed mastery.

3. `R3_Subject_Specific_Pedagogy.md`
   - Mathematics;
   - Physics;
   - Chemistry;
   - subject difficulty dimensions;
   - fingerprints;
   - solution contracts;
   - misconception taxonomies.

4. `R4_Assessment_UX_AI_Provenance.md`
   - practice vs diagnostic vs assessment;
   - validity and psychometric boundaries;
   - textbook/question-bank UX;
   - accessibility;
   - AI correctness;
   - provenance, auditability, copyright-safe use.

5. `R5_Methodology_v2_Synthesis.md`
   - consume R1-R4 outputs;
   - build the unified evidence ledger;
   - audit every important current rule;
   - propose Methodology v2;
   - propose schema/skill/validator migrations;
   - design pilots and implementation backlog;
   - **do not implement**.

## Research-output rules

Every research package should:

- distinguish empirical evidence, professional standards, expert synthesis, and engineering inference;
- preserve uncertainty and boundary conditions;
- use durable citations: DOI, journal/publisher link, government/professional-standard URL, or official curriculum/exam URL;
- not rely on ChatGPT session citation handles as the only provenance;
- explicitly state what can and cannot be inferred without learner-response data;
- avoid universal numerical thresholds unless directly supported;
- identify recommendations that require pilot data rather than presenting hypotheses as facts.

## Evidence grades

Use these as project-level evidence grades, while stating the underlying evidence type:

- `A` — strong evidence or authoritative standard with strong applicability;
- `B` — good evidence with meaningful boundary conditions;
- `C` — promising/limited evidence or cross-context inference;
- `D` — design hypothesis requiring pilot validation.

## Current-rule verdicts

When auditing the existing methodology, use:

- `KEEP`
- `KEEP WITH CLARIFICATION`
- `MODIFY`
- `REPLACE`
- `REMOVE`
- `REQUIRES PILOT DATA`

## Implementation boundary

R1-R5 are research and planning artifacts. They must not directly modify the Grade 9 skills, schemas, validators, publication rules, or production code. Implementation requires a separate explicit authorization after the R5 synthesis is reviewed.
