# Physics V2 — Core (1A) Difficulty-Badged Subtopic Assimilation

> **Canonical V8 learner-product spec:** `TECHNICAL_PUBLICATION_SPEC_v5.md`.
>
> New authoring must follow `Blueprint/SELF_HELP_ARCHITECTURE_V8.md`: CCU custody/coverage → CDAU purpose/differentiation → SDU v2 intrinsic difficulty → Concept TTU v3. Older policies below remain implementation/history context where not superseded.

> **Future agents: start with `AGENT_RUNBOOK.md`, then read `TECHNICAL_PUBLICATION_SPEC_v5.md`.**

Core (1A) is the declarative deep-teaching layer between semantic **Core (1)** and learner problem work.

Core (1) answers **what Physics is authorised**.

Core (1A) answers:

> Given this stable subtopic bucket and its intrinsic difficulty badge, what complete self-help teaching product is required so a learner can understand the subtopic without a teacher physically present?

## V2 control rule

Core1A is **always subtopic/SBA-bucket-wise**.

Publication depth is driven by the bucket's intrinsic difficulty badge:

`EASY | MEDIUM | HARD`

Student knowledge percentage does **not** drive Core1A publication depth.

Legacy `prior_knowledge_pct` fields in older fixtures/manifests are retained only for migration compatibility. New Core1A publication decisions must not use them as the depth selector.

See the current V8/SDU policy first; `BUCKET_DEPTH_POLICY_v1.md` and older machine policies are historical where superseded.

## Difficulty-badge depth

### EASY

- complete but compact;
- visual and step-by-step support where useful;
- web research not required for representation planning unless factual/source uncertainty requires it;
- soft capacity ceiling: about **10 pages**.

### MEDIUM

- detailed step-by-step teaching;
- web research required for pedagogy/representation planning;
- dedicated diagrams for major model or representation changes;
- split into sub-subtopics when several distinct inferential jumps exist;
- soft capacity ceiling: about **20 pages**.

### HARD

- maximal useful granularity without padding;
- web research required for pedagogy/representation planning;
- dedicated visual sequences for major conceptual transitions;
- sub-subtopic decomposition expected when conceptual jumps can be isolated;
- soft capacity ceiling: about **30 pages**.

Page ceilings are not targets. Core1A and Core1B share the envelope but derive actual length independently.

## Mandatory declarative teaching spine

The default learner sequence is:

`SBA INDEX → PHYSICAL IDEA / PHENOMENON → PREREQUISITE BRIDGE → STAGED REPRESENTATIONS → WORDS → SYMBOLS / EQUATION → MODEL CONDITIONS → MISCONCEPTION CONTRAST → FULL WORKED EXAMPLE → CHECK → TRANSFER PREPARATION`

For hard buckets this spine may repeat at sub-subtopic level.

## Stable SBA indexing

Use semantic IDs such as `M2D-SBA-03`, never PDF page numbers as concept identifiers.

Every Revised Core (2) question has exactly one primary SBA owner. A source question may still be HELD until prerequisite/source-integrity conditions are satisfied.

## Source, answer and custody rule

CCU v1 is mandatory. Every canonical asset receives an explicit Core disposition; every learner-facing question/example has a stable ID, visible source class, retained source number where applicable, and canonical resolution. Author-created examples must be visibly author-created and may not impersonate source questions.

## Learner UI

See `CORE1A_UI_SPEC.md`.

Every visual must perform an instructional function such as REPRESENT, EXPLAIN, COMPARE, PREDICT, DERIVE or CHECK. More images are not automatically better.

## Durable handoff state

Read:

- `registry/physics-core1a-motion-in-a-plane-build-state-v1.json`;
- `registry/build-manifests/M2D-SBA-xx-v1.json`;
- run `python Grade 9/V2/Physics/Core1A/engine/next_sba.py`.

If derived queue state disagrees with build-state, the build fails.

## Release claim

Architecture and machine checks reduce silent drift. They do not replace human subject-correctness, pedagogy or visual-usability review.
