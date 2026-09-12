# Primary Math V2 Authoring / Concept Engine

Tracking: #335. Parent architecture: #328 / PR #329. Canonical registries: #330 / PR #331. Publisher consumer: #324 / PR #327. Independent acceptance: #325 / PR #326.

## Boundary

```text
raw/source questions
        ↓
SEMANTIC EVIDENCE EXTRACTION
agent/model/source parser
        ↓
normalized QuestionEvidence
+ optional MathematicalWorkEvidence
+ optional topic labels
        ↓
DETERMINISTIC AUTHORING ENGINE
validate canonical refs
resolve scope/provenance
group ConceptNodes
select evidence-bounded ConceptMode
build SkillModel / Core1 / Core2 / RepresentationPlan
        ↓
PR #327 publisher
```

The deterministic engine intentionally does **not** infer mathematics from raw prose with keyword rules. A question without normalized evidence fails `SEMANTIC_EVIDENCE_REQUIRED` rather than silently guessing.

## Common PR stack

- #163: scope, canonical ontology, overlays, source boundaries.
- #171: mathematical work evidence, quantity structure, provenance.
- #172: work evidence before diagnosis and independent retry.
- #185: bounded contrasts, hypotheses and diagnostic probes.
- #182: Core1/Core2 visual-first and H1/H2/H3 obligations.
- #164: support/access separation, route change and independent evidence dimensions.

## Output authority

This engine owns semantic authoring assembly only. It emits the canonical #329 seams:

```text
PrimaryMathSkillModel
PrimaryMathCore1StudyPlan
PrimaryMathCore2CompanionPlan
PrimaryMathRepresentationPlan
```

It does not import ReportLab, page geometry, the visual renderer, the benchmark evaluator, or artifact custody code.

## Scope rules

Question/classwork observations may activate project scope but never become universal grade truth. `CURRICULUM_CONFIRMED` requires an explicit authority reference. Conflicting scope evidence becomes `MAPPING_PENDING` rather than being force-fit.

## Learner-work rules

`student_workout` is optional. When present, teacher corrections remain separate from child work, correct intermediate steps survive an incorrect final answer, ambiguity remains explicit, and `PROBE` requires 2–3 bounded hypotheses plus a diagnostic probe with outcome rules.

## Topic hints

The #329 input contract defines topic hints as optional strings. In this engine they may label a matching concept only. They cannot add capabilities, change problem families, or override scope evidence.

## Publication handoff

PR #327 receives validated plans and is responsible for primitive realization, page composition and physical artifact custody. If the publisher needs a concept/representation not present in the plan, the correct response is an unresolved authoring/registry gap—not renderer invention.
