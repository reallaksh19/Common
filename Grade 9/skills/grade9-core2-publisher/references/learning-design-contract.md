# Core (2) learning-design contract

## Purpose

A verified ResearchPackage is not yet a learner experience. For mature learner products, Core (2) must explicitly design what the learner is expected to understand, reconstruct, discriminate, practise and transfer before arranging content into PublicationStructure or rendering pages.

The production chain is:

```text
ResearchPackage + LearnerProfile + PublicationTarget
    -> PublicationPlan
    -> LearningDesignPlan
    -> StudyGuide / Transfer semantic models
    -> PublicationStructure
    -> physical-page mapping
    -> exact learner PDF
```

`PublicationStructure` owns order, disclosure and layout intent. `LearningDesignPlan` owns instructional semantics. Role labels such as `NOTICE`, `GUIDED_2_FADED` or `INDEPENDENT_TRANSFER` are not evidence that the underlying learner task is pedagogically valid.

## Production modes

Core (2) distinguishes:

```text
ENGINEERING_REPLAY
MATURE_LEARNER_PRODUCT
```

`ENGINEERING_REPLAY` may use conservative deterministic generated prose to test hand-off, schemas, rendering and artifact custody. It must never be presented as a mature learner-product quality proof.

`MATURE_LEARNER_PRODUCT` requires an authored and validated `LearningDesignPlan`. Generic auto-generated connective prose or baseline prompt templates cannot substitute for it.

## Required unit semantics

For every substantial learning unit, make explicit where applicable:

- learner capabilities: recognize, explain, reconstruct, apply, select a model, check conditions, predict, translate representations, discriminate misconceptions and transfer;
- prerequisite decisions and repair route;
- an observable, structural, representational, physical or symbolic anchor;
- the ordinary-language meaning the learner should be able to say;
- formal-object term origins, conditions, reconstruction route and checks;
- representation transitions and the learner job during each transition;
- specific wrong models, why they are tempting, a decisive discriminator and a repair strategy;
- deliberate contrasts where similar-looking cases require different models;
- worked -> guided -> faded -> independent support removal;
- independent-practice identity;
- transfer dimensions relative to the worked example;
- completion probes that cover every required learner capability;
- competitive-exam question-family recognition requirements, hidden prerequisites and failure models when an ExamDemandProfile applies.

## Shared quality invariants

Subject profiles may specialize these invariants, but a mature unit should not silently weaken them when they apply:

```text
NO_NAKED_FORMALISM
SYMBOLS_HAVE_MEANING
TERMS_HAVE_ORIGIN
CONDITIONS_ARE_VISIBLE
MISCONCEPTION_IS_SPECIFIC
RECONSTRUCTION_EXISTS
REPRESENTATION_HAS_A_REASONING_JOB
SUPPORT_ACTUALLY_FADES
INDEPENDENT_IS_NOT_A_COPY
TRANSFER_CHANGES_A_MEANINGFUL_DIMENSION
COMPLETION_PROBES_COVER_REQUIRED_CAPABILITIES
```

A task that changes only numbers is practice, not transfer. A diagram that carries no learner reasoning job is decorative, not representation closure. A stage named `GUIDED_2_FADED` that removes no support is not fading.

## Subject specialization

Physics may require physical-system meaning, frame/sign conventions, diagram/graph semantics, dimensional reasoning or limiting cases.

Chemistry may require macro/particle/symbolic translation, conservation or charge checks, process conditions and species-level misconception repair.

Mathematics may require structural models, invariants, reconstruction, case distinctions, counterexamples, justification and method selection.

Do not force one subject's vocabulary onto another. The shared contract describes learner cognition; subject authority defines the valid disciplinary grammar.

## Competitive-exam bridge

When `PublicationTarget` requires competitive-exam preparation and Core (1) supplies an `ExamDemandProfile`, Core (2) must map required question families into the learning design.

For each family establish, where evidence supports it:

```text
exam question family
    -> recognition requirements
    -> hidden prerequisites
    -> common failure models
    -> teaching/repair learning units
    -> supported assimilation practice
    -> independent attempt
    -> mixed transfer/diagnosis
```

Do not create difficulty or transfer labels merely to make practice look advanced.

## Machine versus human judgment

Machine validation may prove custody, required fields, capability/probe coverage, declared support removal, transfer dimensions, ordering, source bindings and exact-artifact identity.

It cannot prove that an explanation is intuitive, a misconception is authentic, or a transfer problem is intellectually excellent. Mature release therefore keeps machine technical PASS distinct from exact-artifact-bound pedagogy, subject-matter and visual review.

## Authoring sequence

For a new mature topic:

1. Validate the frozen Core (1) hand-off.
2. Build PublicationPlan.
3. Author LearningDesignPlan.
4. Validate learner capabilities, fading, transfer and exam bridge.
5. Author one representative learning unit and render it.
6. Review the representative unit for subject accuracy and pedagogy.
7. Only then author the full StudyGuide/Transfer semantic models.
8. Build PublicationStructure from those authored objects.
9. Reconcile material custody and physical-page placement.
10. Bind audits/reviews to exact final artifact hashes.

Do not scale a weak prototype into a full chapter.
