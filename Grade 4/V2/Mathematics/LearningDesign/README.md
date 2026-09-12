# Primary Math V2 Learning Design / Representation Seam

This package implements issue #338, stacked on the authoring engine in #335 / PR #336.

It owns the missing contract between semantic authoring and publication:

```text
PrimaryMathSkillModel / Core1-Core2 authoring plans
        ↓
LearningDesign
        ↓
LearningRepresentationPlan
        ↓
PR #327 visual/publishing engine
```

It does **not** render PDFs and imports no publication backend.

## Authorities

- #163 — scope/ontology provenance
- #171/#172 — learner work evidence before teaching decisions
- #185 — bounded diagnostic probes
- #182 — visual-first learner publication, H1/H2/H3 + fresh retry
- #164 — support fading and independence distinctions
- #328 — Primary V2 parent architecture
- #331 — canonical capability/problem/representation registry

## Contracts

- `contracts/learner-profile.schema.json` — child readability, visual/workspace/text ratios, solution-separation and support-fading constraints.
- `contracts/hint-ladder.schema.json` — H1 LOOK, H2 REMEMBER, H3 SHOW IT, each with a visual state and learner action.
- `contracts/thinking-path.schema.json` — internal semantic role + separate child-facing label + microvisual.
- `../Representation/contracts/representation-fidelity.schema.json` — EXACT / REPRESENTATIVE_SAMPLE / SCHEMATIC honesty.
- `../Representation/contracts/work-surface.schema.json` — semantic procedural work surfaces, including long division.
- `../Representation/contracts/learning-representation-plan.schema.json` — publisher-neutral visual/hint/path/work-surface handoff.

## Key invariant

> The publisher may realize a validated learning/representation plan; it may not invent the teaching route while drawing the page.

Run:

```bash
python Primary/V2/Mathematics/LearningDesign/validation/validate_learning_representation.py
```
