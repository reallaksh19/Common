# Chemistry LearningBlueprint v5 — study-product completeness and reconstructable TTUs

v5 is an architectural quality gate **after** v4 control resolution and **before** learner-product pagination/rendering.

v4 answers:

```text
Core1A/Core1B: how deep must this subtopic bucket be?
Core2A/Core2B: how much support is appropriate for this learner/owner condition?
```

v5 answers a different question:

> Is the planned artifact actually a self-study product with enough Chemistry structure to teach/reconstruct/solve, or is it only an executive summary, prose booklet, repeated template, or padded PDF?

## Governing sequence

```text
validated Chemistry authority
        ↓
v4 bucket / learner conditioning
        ↓
v5 technical-object obligations
        ↓
reconstructable TTUs
        ↓
practice / question episode closure
        ↓
page-role plan
        ↓
measured PDF quality gate
        ↓
learner product
```

**Content closure precedes pagination.** The 10/20/30 Easy/Medium/Hard values remain maximum normal envelopes; they are never page targets and cannot justify blank or low-value pages.

## What counts as a study note

A Core1A learning atom is not closed by a heading plus explanation. It must carry, at minimum:

```text
MEANING
RULE / DECISION PROCEDURE
REPRESENTATION / EQUATION
REASONING CHAIN
BOUNDARY / MISCONCEPTION
WORKED OR MODELED EXAMPLE
PRACTICE
ANSWER CLOSURE
```

A HARD Core1A bucket additionally requires rule/derivation anatomy, misconception contrast, representation bridging and independent practice.

Core1B shares the same Chemistry authority but has a different learner action contract:

```text
RETRIEVE / PREDICT
REPRESENT
EXPLAIN / JUSTIFY
COMPARE / CORRECT / TEST A BOUNDARY
GENERALISE / TEACH BACK
SELF-HELP
CANONICAL RESPONSE
VERIFY
```

The A and B products may share governed facts, equations, terms and citations. They must not copy expository paragraphs, generic hint blocks or worked-solution prose.

## Reconstructable TTUs are mandatory

A TTU is not a decorative visual and not a finished diagram. It is a governed technical representation with deliberately missing, chemically meaningful structure that the learner must rebuild.

Supported TTU forms include:

```text
incomplete diagram
component assembly
incomplete / to-be-plotted graph
equation skeleton
event line / process line
conservation or oxidation-state ledger
decision tree
reaction scheme
representation map
particle/species map
oxidation-state lane
```

Every TTU must contain:

```text
owner learning atom or question
TTU type + cognitive job
learner action
initial incomplete state
explicit missing elements + semantic roles
fixed hint ladder bound to those missing elements
canonical completed state
verification rule
representation-authority references
no new Chemistry refs
```

A fully completed representation cannot be relabelled as a TTU. At least one TTU is required per major Core1A/Core1B learning atom and per selected Core2A/Core2B question.

### Exposure mode is core-specific

```text
Core1A  MODEL_THEN_RECONSTRUCT
Core1B  RECONSTRUCT_BEFORE_CANONICAL
Core2A  SETUP_THEN_COMPLETE
Core2B  CHOOSE_OR_RECONSTRUCT_BEFORE_HINTS
```

This prevents all four products from becoming the same page with different headings.

## Core2A / Core2B question episode completeness

Every selected question must have a complete self-study episode.

Core2A requires:

```text
ATTEMPT
REPRESENTATION / SETUP
FIRST MOVE
TECHNICAL BREAKDOWN
FULL SOLUTION
ERROR TRAP
VERIFICATION
RETRY / NEAR TRANSFER
RECONSTRUCTABLE TTU
```

Core2B requires:

```text
ATTEMPT
TARGET REPHRASE
RELEVANT-DATA SELECTION
REPRESENTATION CHOICE
PRINCIPLE SELECTION
FIRST-MOVE COMMITMENT
JUSTIFICATION
PROGRESSIVE HINTS
FULL SOLUTION
VERIFICATION
GENERALISE / DIAGNOSE
RECONSTRUCTABLE TTU
```

Source-question stem, provenance and canonical answer authority remain unchanged. The helper/tutor realization must be independently authored for A vs B.

## Page architecture

A page is allowed to exist only when it performs a declared product job. Valid page roles include concept explanation, rule/derivation, representation, TTU reconstruction, worked example, misconception/boundary, practice, question episode, workspace, solution and summary/handout.

Normal content pages must target at least 55% measured active area. Workspace/TTU pages may be more open, but the open area must be attached to an explicit learner action and reconstruction job. Blank space is not depth.

The eventual PDF gate must measure **actual rendered active area**. A declared page-plan ratio alone is not release evidence.

## Research translation

MEDIUM/HARD research is not satisfied by citations in prose. Research must change a governed technical object and, for HARD buckets, at least one reconstructable TTU. Example:

```text
research finding: learners confuse oxidation state with ionic charge
        ↓
technical contrast: oxidation-state vs charge table
        ↓
TTU: incomplete oxidation-state lane / charge ledger
        ↓
learner reconstructs and verifies the distinction
```

Research remains advisory to pedagogy and representation. It may not expand Chemistry scope.

## Principal v5 falsifiers

```text
CHEM_V5_SUMMARY_ONLY_ARTIFACT
CHEM_V5_PAGE_COUNT_TARGETING_FORBIDDEN
CHEM_V5_UNJUSTIFIED_EMPTY_PAGE_AREA
CHEM_V5_CROSS_CORE_EXPOSITORY_DUPLICATION
CHEM_V5_GENERIC_TEMPLATE_REPETITION_EXCESSIVE
CHEM_V5_STUDY_OBLIGATION_UNCLOSED
CHEM_V5_QUESTION_OBLIGATION_UNCLOSED
CHEM_V5_TTU_MISSING_FOR_LEARNING_ATOM
CHEM_V5_TTU_MISSING_FOR_QUESTION
CHEM_V5_TTU_NOT_RECONSTRUCTABLE_ALREADY_COMPLETE
CHEM_V5_TTU_MISSING_STRUCTURE_ABSENT
CHEM_V5_TTU_HINT_NOT_BOUND_TO_MISSING_STRUCTURE
CHEM_V5_TTU_REPRESENTATION_AUTHORITY_MISSING
CHEM_V5_TTU_NEW_CHEMISTRY_FORBIDDEN
CHEM_V5_TTU_EXPOSURE_MODE_INVALID
CHEM_V5_TTU_NOT_REALIZED
CHEM_V5_HARD_RESEARCH_NOT_TRANSLATED_TO_TTU
CHEM_V5_QUESTION_EPISODE_CLOSURE_MISSING
```

## Contracts

```text
contracts/reconstructable-ttu-v5.schema.json
contracts/study-product-v5.schema.json
contracts/question-product-v5.schema.json
policies/v5-study-product-quality-policy.json
engine/validate_blueprint_v5.py
tests/test_blueprint_v5_product_quality.py
golden/v5/*
```

v5 is still a **product-architecture gate**, not a learner-efficacy claim. Passing it means the artifact has the required technical and reconstructive structure; it does not prove mastery, retention or transfer.
