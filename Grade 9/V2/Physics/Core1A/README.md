# Physics V2 — Core (1A) Learner Publication

Core (1A) is the publication compiler between the semantic **Core (1)** study plan and the learner-facing Core study-guide PDF.

It does **not** redefine Physics, learner treatment, problem-family semantics, or the two-product topology. Its job is to take an already-authored `PhysicsCore1StudyPlan` and compose it into a Grade-9 textbook-quality learner product with a deterministic page architecture, progressive disclosure, publication QA, and exact upstream custody.

```text
P-G CoreAuthoring
PhysicsCore1StudyPlan
        │
        ▼
P-GA Core1A
PhysicsCore1APublicationPlan
        │
        ▼
Core1A renderer
        │
        ▼
physics-core-study-guide.pdf
```

Core (1A) remains the existing `CORE_STUDY_GUIDE` product. It is **not a third learner product**. Appendix A/B/C remain sections of that same PDF.

## Authority boundary

Core (1A) may:

- reorder and group learner-facing Core (1) fields into textbook modules;
- choose page templates from a fixed publication policy;
- derive short navigation labels and concept badges from learner-facing text;
- allocate purposeful work space;
- render schematic instructional visuals when no source-grounded quantitative figure is available;
- consume an optional P-H `PhysicsRepresentationBundle` and prefer source-grounded figures when present;
- report publication-quality findings.

Core (1A) may **not**:

- add a new capability, law, physical model, or problem family;
- invent numerical quantities for figures or examples;
- change P-F treatment or P-G lesson mode;
- turn `CONCISE_VERIFY_ONLY` or `PROBE` into full reteaching;
- silently repair weak/template-only Core (1) content and then claim instructional maturity;
- create a third learner product.

## Learning-page grammar

A `FULL_LEARNING` lesson is compiled into a mature cycle rather than a linear dump of fields:

```text
CONCEPT BADGE
→ REAL-WORLD / PHENOMENON ANCHOR
→ SEE IT
→ KEY IDEA / PHYSICS WORDS
→ REPRESENTATION BRIDGE
→ MODEL CHECK
→ WORKED EXAMPLE
→ COMMON TRAP (why plausible → minimal contrast → repair)
→ GUIDED PRACTICE
→ FADED PRACTICE
→ INDEPENDENT PRACTICE
→ SELF-CHECK / RETRIEVAL
→ TRANSFER BRIDGE
```

Not every module is forced onto every page. The compiler targets readable page rhythm rather than a card for every field.

`CONCISE_VERIFY_ONLY` remains concise: activation → independent attempt → physical check.

`PROBE` remains pre-explanatory: probe → work space → check. No explanatory reteach may appear before the decisive probe.

## Publication quality

Core (1A) has a stricter learner-surface policy than the existing P-L survival checks:

- body text target 10.2 pt, hard floor 9.5 pt;
- caption floor 8 pt;
- A4 page with 16 mm margins;
- 70–85% meaningful page occupancy target (working space counts as meaningful);
- no orphan headings;
- no accidental half-page voids;
- no worked example split before its result/check;
- figures require captions and provenance mode;
- learner modules use restrained, stable visual vocabulary;
- every final PDF is hash-bound to its Core (1) input digest and publication-plan digest.

## Content-maturity honesty

A polished PDF must not hide generic Core (1) content. Core (1A) therefore reports `CORE1A_TEMPLATE_ONLY_CONTENT` when a worked example or practice item still contains known scaffold phrases such as "newly authored instance", "set up the system and frame", or "select the relation" without an instantiated physical situation.

This is a publication/content-maturity finding, not an authority to rewrite the example.

## Files

```text
Core1A/
├── contracts/
│   └── physics-core1a-publication-plan.schema.json
├── engine/
│   ├── build_physics_core1a.py
│   └── render_physics_core1a.py
├── registry/
│   └── physics-core1a-publication-policy.json
└── tests/
    └── test_physics_core1a.py
```

## Standalone use

```bash
python "Grade 9/V2/Physics/Core1A/engine/build_physics_core1a.py" \
  --core1 /path/to/physics-core1-study-plan.json \
  --out-dir /tmp/core1a
```

The command writes:

```text
physics-core1a-publication-plan.json
physics-core-study-guide.pdf
physics-core1a-quality-report.json
```

An optional representation bundle can be supplied with `--representations`.

## Release claim

Core (1A) can prove publication engineering properties. It cannot set `SUBJECT_CORRECTNESS`, `PEDAGOGICAL_DESIGN`, `ASSESSMENT_DESIGN`, `VISUAL_USABILITY`, or `MATURE_DESIGN_QUALITY`; those remain under the review boundary already established by P-L.
