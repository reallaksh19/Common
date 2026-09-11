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

## Required cold-start sequence

1. Read `Grade 9/Architecture/contracts/v1/SCHEMA_FREEZE_V1.md` and validate the upstream package with PR #160 `validate_handoff.py`.
2. Run `Grade 9/architecture/core2/validate_core2_preflight.py`. A merely schema-valid research bundle is not sufficient; it must be publishable.
3. Read the subject authority (`grade9-math`, `grade9-physics`, or `grade9-chemistry`) only for subject-specific publishing grammar. Do not use it to invent missing Core (1) facts.
4. Inspect the canonical product-first reference specimen/structure examples before authoring a new mature product. Treat the PDF as a visual/product reference and the JSON structure as the machine authority.
5. Build or review the Core (2) `PublicationPlan`.
6. For a mature product profile, build/validate a `PublicationStructure` sidecar before page composition.
7. Resolve every blocking `RepresentationRequirement` through the Shared Representation Layer. Unsupported blocking representations fail closed.
8. Render requested learner products.
9. Validate the Core (2) publication package and audit before release.

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

The same frozen ResearchPackage may produce materially different page sequence, support density, practice topology and representation decoding at different Bxx values. Those differences belong downstream and must not mutate the ResearchPackage.

## Product-first publication structure

A mature learner product is **not** an unordered collection of required components. Order, disclosure timing, fading, navigation and page cognitive jobs are part of publication structure.

Use `Grade 9/architecture/core2/contracts/v1/publication-structure.schema.json` to express that structure independently of subject truth.

The sidecar owns:

```text
learning-unit order
ordered pedagogical roles
one cognitive job per page intent
support progression
attempt/help/solution disclosure order
static-PDF hint separation
appendix order
question ↔ hint ↔ solution ↔ lesson navigation
```

It does not own new subject claims.

For FOUNDATION/BRIDGE, a substantial learning unit should normally make this progression executable when applicable:

```text
physical situation / depiction
→ NOTICE
→ SAY IN WORDS / CONCEPT
→ BUILD OR RECONSTRUCT RELATION
→ WORKED EXAMPLE
→ GUIDED 1
→ GUIDED 2 WITH FADED SUPPORT
→ INDEPENDENT TRANSFER
→ RETRIEVAL CHECK
```

Use explicit roles for variants/contrasts, misconception repair, model boundaries, memory anchors and concept helpers where they materially improve the unit.

For COMPRESSED/REFERENCE, do not mechanically replay the lower-baseline sequence. A high-baseline unit may instead begin from a contrast, compact representation or decision boundary and move quickly to independent transfer. Omitted worked/guided stages require an explicit `NOT_REQUIRED_WITH_REASON` decision in the structure model.

A B90 product is therefore not a shortened B40 product. It may have a different instructional topology while preserving identical research truth and package identity.

## One cognitive job per page intent

The page is a learning surface, not a dumping container. `PublicationStructure.page_intents` should state the page's primary cognitive job and the meaningful layout relationship, for example:

```text
STORY_VS_MODEL
EXAMPLE_VS_RULE
CASE_A_VS_B
REPRESENTATION_VS_REASONING
QUESTION_VS_WORKSPACE
REFERENCE_COMPRESSION
```

Columns are justified by a semantic relationship, not by available empty space.

## Study Guide contract

Default outer structure:

```text
MAIN LEARNING SECTION
Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

`first_step_reference` is a module inside Appendix C, not the identity of Appendix C.

Appendix B may contain separate optional-hint, guided-step-solution and full-solution sections according to the learner profile and structure model. In static PDF, hints must not be placed so that H3 is unavoidably visible while the learner is attempting the question.

Material semantic objects must retain `research_refs`. Pedagogical connective prose and layout-only text do not need artificial claim IDs.

## Support fading

For substantial FOUNDATION/BRIDGE application families, use a real fade rather than repeated fully worked examples:

```text
SHOW
→ COMPLETE WITH SUPPORT
→ PARTIAL
→ SKELETON
→ DRAW / CHOOSE / EXECUTE INDEPENDENTLY
```

The structure contract represents the minimum canonical progression as:

```text
WORKED_EXAMPLE
→ GUIDED_1
→ GUIDED_2_FADED
→ INDEPENDENT_TRANSFER
```

If the profile is COMPRESSED/REFERENCE, the publisher may compress this sequence only with an explicit reason and while retaining meaningful independent transfer.

## Transfer Book contract

A Transfer Book may be built only when its question provenance is valid for the declared target. External-question completeness may be claimed only when the frozen upstream `QuestionEvidenceLedger` closes its denominator and contains no blocking `REVIEW` rows.

Assimilation mode may show concept ownership before attempt. Mixed-transfer mode uses `CONCEPT · IDENTIFY FIRST` and hides the primary concept/method family until diagnosis.

Static publication topology for mature profiles is:

```text
ATTEMPTS
→ OPTIONAL HELP
→ COMPLETE SOLUTIONS
→ MIXED DIAGNOSIS when applicable
```

Do not place all H1/H2/H3 directly under the attempt in a static PDF. Put optional help in a later/coverable section or use a genuinely progressive interactive reveal.

Question navigation should support:

```text
question → hint
question → solution
solution → question
solution → relevant lesson/repair target
```

## Hint and solution grammar

Hints remain typed:

```text
H1 NOTICE  decisive clue/event
H2 MODEL   representation/model
H3 START   first executable relation/line, not the final solution
```

Complete solutions preserve:

```text
QUESTION RECAP
REPRESENTATION when material
WHY THIS WORKS
METHOD
ANSWER / CHECK
CONCEPT TO KEEP
RETURN TARGET
```

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
PRODUCT_STRUCTURE = PASS               # mature production profiles
BADGE_MAPPING = PASS
APPENDIX_A_B_C = PASS
ANSWER_SEPARATION = PASS
REQUIRED_NAVIGATION = PASS             # mature production profiles
INTERNAL_LINKS = PASS
TYPOGRAPHY = PASS
RENDER_BOUNDS = PASS
GRAYSCALE_INFORMATION = PASS
PUBLICATION_MANIFEST_HASH_BINDING = PASS
```

For mature product profiles, the `PublicationStructure` is a first-class package artifact with manifest role `PUBLICATION_STRUCTURE`. The final publication review should reconcile the exact PDF against the declared structure; merely having the right component names somewhere in the PDF is insufficient.

Automated checks do not substitute for subject-matter review, classroom-effectiveness review, or psychometric calibration.

## Executable v1 falsifier versus production morphology

Use `scripts/run_core2.py` for the conservative deterministic replay. It demonstrates contract boundary, traceability, representations, pair identity and artifact QA. It is **not** the visual/morphology authority for a mature PR156/PR157 product and must not be used to claim that the full product-first learning grammar has been exercised unless a matching PublicationStructure and exact-PDF morphology audit are also present.

The replay must be capable of starting cold from a ResearchPackage, LearnerProfile and PublicationTarget without accessing the Core (1) conversation.

The canonical reference specimen should be read in this order:

```text
PublicationStructure JSON
→ learner-facing PDF
→ audit/manifest evidence
```

The PDF teaches the product grammar visually; the JSON makes the same grammar machine-verifiable.
