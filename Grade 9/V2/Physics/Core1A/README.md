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
→ PLAIN-LANGUAGE EXPLANATION
→ PHYSICS WORDS / MODEL / FRAME
→ STAGED ILLUSTRATION
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

The staged illustration is **support for the teaching, not a replacement for it**. A D2/D3 page that contains a diagram but drops the plain-language explanation, model/frame conditions, worked reasoning, or misconception repair is a publication defect.

Not every module is forced onto every page. The compiler targets readable page rhythm rather than a card for every field.

`CONCISE_VERIFY_ONLY` remains concise: activation → independent attempt → physical check.

`PROBE` remains pre-explanatory: probe → work space → check. No explanatory reteach may appear before the decisive probe.

## Difficulty-aware scaffolding

Core (1A) uses learner-facing difficulty badges to control the amount of support:

- `D1 FOUNDATION` — direct meaning / essential vocabulary; at least one explanatory visual or representation;
- `D2 THINK CAREFULLY` — picture-to-equation, event-condition, or frame reasoning; at least two visual stages plus misconception/model support;
- `D3 CHALLENGING` — inverse reasoning, hidden state, or multiple representations; at least three visual stages plus worked reasoning and guided application;
- `D4 EXTENSION` — optional advanced/source-visible content that must be visibly marked as extension.

The badge is not decorative. Missing required support produces a Core (1A) quality finding.

## Core (1A) ↔ Core (2) learning links

Core (1A) points forward to the Core (2) transfer item that demonstrates mastery; Core (2) must point back to the exact Core (1A) repair concept/stage.

```text
Core (1A) concept
    ↓
CHECK → APPLY → TRANSFER (Txx)
                     ↓
             Core (2) protected attempt
                 ↙            ↘
              success          stuck
                                ↓
                      exact repair target
                                ↓
                         Core (1A) stage
```

The learner surface uses a compact `CORE 2 → Txx` badge where a mapped transfer item exists, plus a three-part `CHECK / APPLY / TRANSFER` gateway at the end of the concept.

See `CORE1A_UI_SPEC.md` for the normative learner UI contract.

## Publication quality

Core (1A) has a stricter learner-surface policy than the existing P-L survival checks:

- textbook body target 10.6 pt, hard floor 10.0 pt;
- caption floor 8 pt;
- diagram-label floor 8 pt;
- badge floor 7.3 pt and badges must remain one readable line;
- A4 page with 16 mm margins;
- no heading/badge collision;
- no text outside page bounds;
- learner-facing mathematics uses real Greek symbols, subscripts, superscripts, fractions/radicals where appropriate; raw strings such as `sqrt(...)`, `theta`, `v_A/B`, or `u^2` are not acceptable;
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
├── CORE1A_UI_SPEC.md
├── contracts/
│   └── physics-core1a-publication-plan.schema.json
├── engine/
│   ├── build_physics_core1a.py
│   └── render_physics_core1a.py
├── registry/
│   └── physics-core1a-publication-policy.json
└── tests/
    ├── test_physics_core1a.py
    └── test_core1a_ui_policy.py
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
