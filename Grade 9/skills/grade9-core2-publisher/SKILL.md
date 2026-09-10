---
name: grade9-core2-publisher
description: Publish a frozen Core (1) ResearchPackage into baseline- and purpose-sensitive Grade 9–11 learner products without doing new subject research.
---

# Grade 9–11 Core (2) Publisher

Use this skill when a valid Core (1) ResearchPackage already exists and the task is to create learner-facing study material, practice/transfer products, appendices, scientific representations, badges, links, PDF output, and publication QA.

## Non-negotiable boundary

Core (2) consumes the frozen PR #160 v1 hand-off and never creates a parallel research contract.

```text
ResearchPackage + LearnerProfile + PublicationTarget
                    ↓
                 Core (2)
                    ↓
              learner products
```

Core (2) owns learner adaptation and publication. It does **not** own new mathematical/scientific truth, source repair, exam-demand discovery, external-corpus denominator mechanics, or canonical-ontology promotion.

If a required semantic fact, condition, representation meaning, answer basis, exam-demand object, or reproduction right is missing, return a structured `CORE1_RESEARCH_GAP` and stop the affected publication path.

## Required start sequence

1. Read `Grade 9/Architecture/contracts/v1/SCHEMA_FREEZE_V1.md` and validate the upstream package with PR #160 `validate_handoff.py`.
2. Run `Grade 9/architecture/core2/validate_core2_preflight.py`. A merely schema-valid research bundle is not sufficient; it must be publishable.
3. Read the subject authority (`grade9-math`, `grade9-physics`, or `grade9-chemistry`) only for subject-specific publishing grammar. Do not use it to invent missing Core (1) facts.
4. Build or review the Core (2) `PublicationPlan`.
5. Resolve every blocking `RepresentationRequirement` through the Shared Representation Layer. Unsupported blocking representations fail closed.
6. Render requested learner products.
7. Validate the Core (2) publication package and audit before release.

## Learner adaptation

Bxx comes only from `LearnerProfile` and is independent of task difficulty and transfer distance.

Default adaptation bands:

```text
0–35   FOUNDATION   more prerequisite repair, explicit models, worked reasoning
36–60  BRIDGE       reconnect ideas, diagnose model choice, moderate scaffolding
61–85  COMPRESSED   concise recall, distinctions, application and transfer
86–100 REFERENCE    reference-first, minimal exposition, high independence
```

If a publication concept cannot be mapped to a learner baseline, record the fallback explicitly in the PublicationPlan and surface it in the audit. Do not pretend that a fallback is measured mastery.

## Study Guide contract

Default structure:

```text
MAIN LEARNING SECTION
Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

`first_step_reference` is a module inside Appendix C, not the identity of Appendix C.

Material semantic objects must retain `research_refs`. Pedagogical connective prose and layout-only text do not need artificial claim IDs.

## Transfer Book contract

A Transfer Book may be built only when its question provenance is valid for the declared target. External-question completeness may be claimed only when the frozen upstream `QuestionEvidenceLedger` closes its denominator and contains no blocking `REVIEW` rows.

Assimilation mode may show concept ownership before attempt. Mixed-transfer mode uses `CONCEPT · IDENTIFY FIRST` and hides the primary concept/method family until diagnosis.

## Representation rule

Core (1) owns what a representation must mean and show. Core (2) owns renderer selection, geometry, typography, placement, legibility, grayscale behavior and render QA.

Valid routes are:

```text
semantic data → generated vector figure
approved vector asset → placed figure
approved source crop → fidelity-controlled figure
```

Never replace a required unsupported figure with a decorative placeholder.

## Badges

Badges are typed publication metadata. Color is secondary; the word/label is mandatory. Preserve provenance for difficulty/source/exam labels. Do not turn primary/support concept hierarchy into visually equal pills.

## Release gates

A Core (2) release must establish, where applicable:

```text
CORE2_PREFLIGHT = PASS
RESEARCH_PACKAGE_DIGEST_BINDING = PASS
MATERIAL_TRACEABILITY = PASS
REPRESENTATION_CLOSURE = PASS
BADGE_MAPPING = PASS
APPENDIX_A_B_C = PASS
ANSWER_SEPARATION = PASS
INTERNAL_LINKS = PASS
TYPOGRAPHY = PASS
RENDER_BOUNDS = PASS
GRAYSCALE_INFORMATION = PASS
PUBLICATION_MANIFEST_HASH_BINDING = PASS
```

Automated checks do not substitute for subject-matter review, classroom-effectiveness review, or psychometric calibration.

## Executable v1 falsifier

Use `scripts/run_core2.py` for the conservative deterministic replay. It intentionally demonstrates the contract boundary and publication machinery; it does not replace expert learner-authoring for production books.

The replay must be capable of starting cold from a ResearchPackage, LearnerProfile and PublicationTarget and generating a traceable Study Guide without accessing the Core (1) conversation.