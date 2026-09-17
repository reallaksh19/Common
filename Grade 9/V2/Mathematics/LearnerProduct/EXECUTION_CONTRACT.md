# Mathematics V2 Learner Product — canonical execution contract

This document is the **authoritative handoff for future agents** that build Core (1A) and Core (2A). It exists so a new agent can execute the learner-product workflow from repository inputs without relying on chat history, PR discussion, or undocumented judgment.

The governing rule is:

```text
IF A PRODUCTION DECISION MUST BE INFERRED, THE CONTRACT IS INCOMPLETE.
```

## Authority order

Lower layers may not override higher layers.

```text
1. Source assessment integrity / validity
2. LearnerStateSnapshot + MathLearnerStudyModel
3. Core (1) mathematical and instructional authority
4. Core (1A) bucket + representation authority
5. Core (2) source-transfer authority
6. Competitive archetype authority
7. Core (2A) challenge realization
8. Renderer / page composition
```

If authorities conflict, **do not reconcile by guessing**. Fail closed.

## Canonical execution order

Every learner-product run uses this sequence exactly:

```text
LP-00 VALIDATE_INPUT_BINDINGS
LP-01 SYNTHESIZE_CORE1A_BUCKETS
LP-02 BUILD_CORE1A_REPRESENTATIONS
LP-03 REALIZE_CORE1A
LP-04 MAP_CORE2_TO_CORE1A
LP-05 REALIZE_SOURCE_CORE2A_ITEMS
LP-06 SELECT_CHALLENGE_TARGETS
LP-07 GENERATE_CHALLENGE_CANDIDATES
LP-08 VALIDATE_CHALLENGE_MATHEMATICS
LP-09 VALIDATE_TAUGHT_SCOPE
LP-10 BIND_INLINE_CITATIONS
LP-11 AUTHOR_STAGED_HELP
LP-12 AUTHOR_THINK_IT_THROUGH
LP-13 AUTHOR_FULL_WORKING
LP-14 AUTHOR_QUICK_CHECK
LP-15 RENDER_LEARNER_PRODUCTS
LP-16 VISUAL_PREFLIGHT
LP-17 FINAL_AUDIT
```

A stage may be skipped only when its policy explicitly marks it `NOT_APPLICABLE`; silent skipping is forbidden.

## Stage contract pattern

Every stage is governed as:

```text
CONSUMES -> OPERATION -> EMITS -> PASS GATE / FAIL CLOSED
```

### LP-00 — Validate input bindings

**Consumes**
- learner study model
- Core1 study plan
- Core2 transfer plan
- PCK/problem-family authority
- competitive archetype registry when challenges are requested

**Operation**
- verify refs and digests
- verify Core1 points to the exact study model
- verify Core2 source authority

**Emits**
- validated run manifest

**Stop on**
- missing required learner state when learner-conditioned realization is requested
- digest mismatch
- source authority mismatch

### LP-01 — Synthesize Core1A buckets

**Consumes** Core1 capability lessons + exact learner study model.

**Operation**
- group only when capabilities share a grounded teaching invariant
- preserve learner state/treatment per capability exactly
- attach an unambiguous prerequisite to one dependent bucket
- shared prerequisites become their own bridge bucket
- preserve approved capability order

**Emits** `Core1ABucketPlan`.

**Pass** every required capability appears exactly once.

### LP-02 — Build Core1A representations

Every substantive teaching bucket receives an ordered representation sequence. The default sequence is:

```text
SEE_THE_OBJECT
SEPARATE_THE_PARTS
SHOW_INFORMATION_FLOW
MAP_TO_SYMBOLS
REBUILD_THE_MODEL
CHECK_UNDERSTANDING
CONNECT_TO_CORE2
```

Stages may be marked `NOT_APPLICABLE` only with a stated reason. Do not satisfy representation quality by adding decorative pictures.

### LP-03 — Realize Core1A

Use the exact learner treatment already selected upstream. Do not invent a second readiness taxonomy.

The teaching progression should be selected from:

```text
SEE / EXPLAIN / WATCH ONE / FINISH ONE / TRY WITH LESS HELP / TRY ALONE / CHECK
```

Core1A teaches the mathematical object/model before expecting transfer.

### LP-04 — Map Core2 to Core1A

For every Core2 question and each H1/H2/H3 support step, bind the support to one or more taught Core1A learning atoms.

Fail when a hint relies on mathematics that was not taught or explicitly approved upstream.

### LP-05 — Realize source Core2A items

Preserve source Core2 question order, ID, stem, givens, options, units, subparts, assessment-safety state, multiplicity, and approved attempt-before-solution structure.

Every question displays its own `WHERE THIS QUESTION CAME FROM` box on the question surface.

### LP-06 — Select challenge targets

Apply `math-core2a-execution-policy.json`. Do not invent the number or type of challenges ad hoc.

Challenge difficulty must come from mathematical thinking, not arithmetic ugliness.

### LP-07 — Generate challenge candidates

Generate from approved taught authority plus an approved competitive archetype. Competitive archives influence problem design/demand only; they do not add curriculum authority.

### LP-08 — Validate challenge mathematics

Independently solve each generated item. Confirm the stated answer, all conditions, solution multiplicity, and domain restrictions.

### LP-09 — Validate taught scope

Every required capability must already be in approved Core1/Core1A authority unless the item is explicitly governed as new stretch material. Default is fail closed.

### LP-10 — Bind inline citations

Every question must display provenance **with that question**. A consolidated bibliography does not satisfy the contract.

Generated questions must state that the wording/mathematical instance is fresh when that is true. Never imply an official JEE/IOQM/RMO/INMO/IMO provenance without a verified exact source.

### LP-11 to LP-14 — Build learner help

Learner-visible order:

```text
TRY IT FIRST
SMALL CLUE
BIGGER CLUE
HOW DO I START?
THINK IT THROUGH
FULL WORKING
QUICK CHECK
```

Semantics:
- `SMALL CLUE`: notice the useful structure
- `BIGGER CLUE`: choose the idea or representation
- `HOW DO I START?`: first executable mathematical move
- `THINK IT THROUGH`: complete strategy without collapsing into arithmetic transcript
- `FULL WORKING`: complete mathematics
- `QUICK CHECK`: independent verification where meaningful

### LP-15 — Render

Page composition may change. Semantic identity, source integrity, learner treatment, question provenance, and support order may not.

### LP-16 — Visual preflight

Inspect the rendered artifact, not only the source JSON. Check clipping, unreadable density, isolated headings, broken equations, citation placement, and whether pictorial/stepwise teaching is actually visible.

### LP-17 — Final audit

Emit an artifact manifest with policy versions, input/output digests, stage results, triggered falsifiers, and human-review requirements.

## Stable learner language

Renderers must consume `policies/math-learner-language-policy.json`. Internal labels are not learner labels.

## Stop conditions

Stop rather than improvise when any of the following is true:

- required learner evidence/state is unavailable;
- source mathematics is ambiguous, damaged, or contradictory;
- a bucket invariant cannot be grounded;
- Core1/Core1A/Core2 bindings disagree;
- a Core2 hint cannot map to taught content;
- a generated question requires untaught mathematics;
- a generated question has not been independently solved;
- exact official provenance cannot be verified for an official attribution;
- a generated item is materially too close to a source item;
- citation role (exact source vs style benchmark) is unclear.

## Schema / policy / engine / golden-fixture separation

```text
SCHEMA  = what a legal object contains
POLICY  = how production decisions are made
ENGINE  = exact ordered execution
GOLDEN  = concrete example proving the process
```

No one layer substitutes for the other three.

## Canonical run interface

The canonical run object is governed by:

`LearnerProduct/contracts/math-learner-product-run.schema.json`

The intended command is:

```bash
python 'Grade 9/V2/Mathematics/LearnerProduct/engine/run_learner_product.py' \
  --run-manifest /path/to/run.json \
  --out-dir /tmp/math-learner-product
```

Until all downstream renderers are executable, the entrypoint is required to fail closed with an explicit unsupported-stage error rather than silently omit a stage.

## Golden reference

`LearnerProduct/golden/theory-of-equations/` is the canonical process example. Future agents may copy its **process and contracts**, not its mathematical content into unrelated topics.
