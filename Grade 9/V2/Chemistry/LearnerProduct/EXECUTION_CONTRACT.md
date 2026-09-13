# Chemistry V2 Learner Product — canonical Core (1A) / Core (2A) execution contract

This document is the repository-authoritative execution contract for Chemistry Core (1A) and Core (2A). A future agent must be able to run the learner-product process from repository inputs without reconstructing decisions from chat history, PR comments, screenshots, or intuition.

The governing rule is:

```text
IF A PRODUCTION DECISION MUST BE INFERRED, THE CONTRACT IS INCOMPLETE.
```

## Product meaning

```text
C-F LearnerStudyModel
        ↓
C-G Core (1) semantic teaching authority
        ↓
Core (1A) bucket synthesis + learner assimilation
        ↓
C-I Core (2) source-transfer authority
        ↓
Core (2A) source practice + fresh governed challenge practice
```

Core (1A) and Core (2A) are downstream learner-product layers. They may improve teaching sequence, representation, practice, scaffolding and transfer. They may not change source truth, chemistry scope, learner diagnosis/treatment, source-question validity, or release legality.

## Authority order

Lower authorities may not override higher authorities.

```text
1. Source/item integrity and validity
2. C-F LearnerStudyModel / learner treatment
3. C-G Core (1) chemistry and instructional authority
4. C-H representation semantic authority
5. Core (1A) bucket + assimilation authority
6. C-I Core (2) source-transfer authority
7. competitive-archetype authority
8. Core (2A) realization
9. renderer / page composition
```

If authorities conflict, fail closed. Do not repair by guessing.

## Canonical execution order

Every Chemistry learner-product run uses this exact sequence:

```text
C-LP-00 VALIDATE_UPSTREAM_BINDINGS
C-LP-01 FREEZE_SOURCE_DENOMINATOR
C-LP-02 CLASSIFY_SOURCE_INTEGRITY
C-LP-03 SYNTHESIZE_CORE1A_BUCKETS
C-LP-04 BIND_LEARNER_TREATMENT
C-LP-05 DECOMPOSE_LEARNING_ATOMS
C-LP-06 BUILD_REPRESENTATION_SEQUENCE
C-LP-07 BUILD_PROBLEM_FAMILIES
C-LP-08 CLOSE_CORE2_HINT_PRETEACH
C-LP-09 REALIZE_CORE1A
C-LP-10 MAP_CORE2_TO_CORE1A
C-LP-11 REALIZE_SOURCE_CORE2A_ITEMS
C-LP-12 SELECT_CHALLENGE_TARGETS
C-LP-13 GENERATE_CHALLENGE_CANDIDATES
C-LP-14 VALIDATE_CHEMISTRY
C-LP-15 VALIDATE_TAUGHT_SCOPE
C-LP-16 VALIDATE_NEAR_COPY
C-LP-17 BIND_PROVENANCE
C-LP-18 AUTHOR_STAGED_HELP
C-LP-19 AUTHOR_QUICK_CHECK
C-LP-20 AUTHOR_FULL_WORKING
C-LP-21 VALIDATE_ANSWER_CLOSURE
C-LP-22 RENDER_LEARNER_PRODUCTS
C-LP-23 VISUAL_PREFLIGHT
C-LP-24 FINAL_AUDIT
C-LP-25 FREEZE_HANDOFF
```

A stage may be skipped only when its governing policy records `NOT_APPLICABLE` with a reason. Silent skipping is forbidden.

## Stage contract pattern

Every stage is defined as:

```text
CONSUMES -> OPERATION -> EMITS -> PASS GATE / FAIL CLOSED
```

### C-LP-00 — Validate upstream bindings

**Consumes**
- exact C-F LearnerStudyModel ref + digest;
- exact C-G Core1Plan ref + digest;
- exact C-H RepresentationBundle ref + digest;
- exact C-I Core2Plan ref + digest;
- exact C-J coverage/denominator closure ref + digest;
- competitive registry when fresh challenges are requested.

**Operation**
- verify references and digests;
- verify Core1 and Core2 are from the same governed semantic run/scope;
- verify learner-conditioned realization uses the exact upstream learner model;
- verify source denominator custody.

**Emits** validated learner-product run manifest.

**Stop on** any binding/digest/scope mismatch.

### C-LP-01 — Freeze source denominator

The retained source-question denominator must be explicit before learner-product authoring.

Required counters:

```text
TOTAL_SCANNED
ELIGIBLE_IN_TOPIC
PLACED_UNIQUE
EXCLUDED_WITH_REASON
MISSING
DUPLICATE_PRIMARY
```

Required closure:

```text
ELIGIBLE_IN_TOPIC == PLACED_UNIQUE
MISSING == 0
DUPLICATE_PRIMARY == 0
```

No later stage may silently change the denominator.

### C-LP-02 — Classify source integrity

Every retained source question must carry one source-integrity state:

```text
CLEAN
TYPOGRAPHIC_OR_OCR_AMBIGUITY
SOURCE_TRUNCATED_OR_INCOMPLETE
CHEMICAL_OR_DOMAIN_ISSUE
CONTEXT_AMBIGUITY
```

Do not silently repair source text. Any normalized display form must preserve the original source identity and QC record.

### C-LP-03 — Synthesize Core1A buckets

Group Core1 capabilities only when they share a grounded Chemistry teaching invariant/problem family. Preserve every required capability exactly once as a primary bucket membership. Shared prerequisites may become bridge buckets.

Core1 capability != learner textbook bucket.

### C-LP-04 — Bind learner treatment

Intrinsic difficulty and learner readiness are separate.

Core1A consumes the exact C-F learner state/treatment. Core1A must not invent a second readiness taxonomy such as `20% learner`, `weak learner`, `foundation learner`, or `advanced learner` unless that state is explicitly governed upstream.

### C-LP-05 — Decompose learning atoms

A learning atom is the smallest teachable move required before a linked Core2 demand can legitimately be attempted.

Each atom must include:
- meaning/purpose;
- prerequisite support;
- ordinary-language bridge;
- symbolic/quantitative form when applicable;
- representation binding;
- misconception contrast;
- learner check;
- Core2 hint binding when available.

### C-LP-06 — Build representation sequence

Default Chemistry representation sequence:

```text
SEE_THE_PHENOMENON
SEE_THE_PARTICLES
SEE_THE_CHEMICAL_STRUCTURE
SEE_THE_SYMBOLS
CONNECT_THE_QUANTITIES
DO_THE_CHEMISTRY
VERIFY_THE_RESULT
CONNECT_TO_CORE2
```

A stage may be `NOT_APPLICABLE` only with a recorded reason. Decorative illustration does not satisfy representation adequacy. The representation must help the learner know what to write, draw, count, compare, cancel, label, or track next.

### C-LP-07 — Build problem families

Do not treat many Core2 questions as one undifferentiated list. Cluster by recognition signal, representation, first move and solution routine.

Each active problem family must include:
- `LOOK FOR` recognition signals;
- representation/setup;
- numbered method;
- worked analogue;
- independent attempt;
- optional staged hints after attempt;
- verification/sense check;
- readiness gate;
- exact Core2 release targets.

### C-LP-08 — Close Core2 hint pre-teaching

Internal support semantics:

```text
H1 = key chemistry concept/criterion
H2 = representation/model
H3 = first executable symbolic/quantitative move
```

Every H1/H2/H3 reveal must bind to earlier Core1A teaching evidence. If a hint teaches new chemistry, the linked question is not releasable.

### C-LP-09 — Realize Core1A

Core1A is a teaching product, not a summary sheet. It should realize the governed bucket plan through suitable combinations of:

```text
SEE / EXPLAIN / WATCH ONE / FINISH ONE /
TRY WITH LESS HELP / TRY ALONE / CHECK / TRANSFER
```

Every learner-facing practice question requires an answer path governed by the answer-path contract.

### C-LP-10 — Map Core2 to Core1A

Every Core2 question gets exact primary bucket/problem-family bindings and H1/H2/H3 learning-atom bindings. Duplicate primary placement is forbidden.

### C-LP-11 — Realize source Core2A items

Preserve source identity, order, stem/givens/options/subparts/units and approved assessment-safety state. Add learner support without silently rewriting the source.

Every item displays its own `WHERE THIS QUESTION CAME FROM` surface.

### C-LP-12 — Select challenge targets

Use the Chemistry competitive-challenge policy. Challenge count/type must not be chosen ad hoc.

Default selection is problem-family based:
- one `NEAR_TRANSFER` per eligible family;
- one structural variation for eligible D2/D3 families with a valid alternate reasoning direction;
- `MIXED_SYNTHESIS` only when at least two compatible taught buckets are mature.

### C-LP-13 — Generate challenge candidates

Generate only from taught Chemistry authority plus an approved competitive archetype. Competition sources may shape reasoning demand; they do not add curriculum authority.

### C-LP-14 — Validate chemistry

Generated items and worked solutions must be independently checked where applicable for:
- formula charge neutrality;
- atom/reaction conservation;
- ionic charge preservation;
- molar-mass recomputation;
- dimensional/unit consistency;
- entity multipliers;
- concentration denominator;
- stoichiometric mole ratio;
- oxidation-number sum/change;
- redox-direction consistency.

### C-LP-15 — Validate taught scope

Every required capability must already be authorized/taught unless explicitly governed as stretch material. Default is fail closed.

### C-LP-16 — Validate near-copy

Fresh challenges must be materially distinct from source items while preserving the intended archetype. Cosmetic number/name substitution is not sufficient novelty.

### C-LP-17 — Bind provenance

Every learner question displays provenance with that question. A consolidated bibliography is insufficient.

Generated items must identify themselves as fresh/original when true and must never claim official past-question provenance unless an exact official source is verified.

### C-LP-18 to C-LP-20 — Author learner help and answers

Approved learner sequence:

```text
TRY IT FIRST
SEE THE IDEA
WRITE THIS FIRST
SMALL CLUE
BIGGER CLUE
HOW DO I START?
WATCH FOR THIS
THINK IT THROUGH
CHECK YOUR CHEMISTRY
QUICK CHECK
FULL WORKING
WHERE THIS QUESTION CAME FROM
```

The helper must cause a useful learner action. `Use mole conversion` is insufficient; `Write n = m/M, put the mass on top, calculate molar mass below it, and check that g cancels` is actionable.

### C-LP-21 — Validate answer closure

Non-negotiable self-study rule:

> NO LEARNER-FACING QUESTION WITHOUT A CHECKABLE ANSWER PATH.

For objectively checkable items:

```text
CLOSED_QUESTIONS_TOTAL
== QUICK_CHECKS_TOTAL
== FULL_WORKINGS_TOTAL
```

For genuinely open-ended items:

```text
OPEN_QUESTIONS_TOTAL
== EXPECTED_RESPONSE_RUBRICS_TOTAL
```

This applies to Core1A guided/faded/independent practice, retrieval/readiness gates, Core2A source items and Core2A generated challenges.

### C-LP-22 — Render learner products

Page composition may change. Source integrity, chemistry semantics, learner treatment, question identity, provenance, support order and answer closure may not.

### C-LP-23 — Visual preflight

Inspect rendered pages at actual output size. Reject clipping, collisions, unreadable density, raw notation, ambiguous subscript/charge, text-only treatment where a required visual is absent, or essential meaning encoded by color alone.

### C-LP-24 — Final audit

Emit machine evidence for:
- upstream bindings/digests;
- source denominator closure;
- capability/bucket coverage;
- representation obligations;
- hint pre-teach closure;
- source Core2A placement;
- challenge validation;
- provenance;
- answer closure;
- learner-language guard;
- rendered visual checks;
- pending human review states.

### C-LP-25 — Freeze handoff

Every completed run must leave durable reusable files so another agent can continue without chat history:
- run manifest;
- exact upstream refs/digests;
- source ledger/denominator;
- Core1A bucket plan;
- learning-atom and problem-family maps;
- representation obligations;
- hint-preteach map;
- Core2A source/challenge plans;
- provenance records;
- answer-closure audit;
- rendered artifact hashes;
- visual QA result;
- known limitations;
- next active bucket/build state.

## Schema / policy / engine / golden separation

```text
SCHEMA  = what a legal object contains
POLICY  = how production decisions are made
ENGINE  = exact ordered execution
GOLDEN  = concrete end-to-end example proving the process
```

No layer substitutes for another.

## Stop conditions

Stop rather than improvise when:
- source chemistry is damaged, contradictory or ambiguous without a QC state;
- required learner state/treatment is unavailable;
- Core1/Core1A/Core2 bindings disagree;
- a bucket invariant cannot be grounded;
- a required representation cannot be semantically grounded;
- a Core2 hint cannot map to taught Core1A content;
- a generated item requires untaught chemistry;
- a generated item has not been independently verified;
- a generated item is materially too close to source;
- provenance role is unclear;
- any learner question lacks its required answer path.

## Canonical run interface

The canonical run object is governed by:

`LearnerProduct/contracts/chemistry-learner-product-run.schema.json`

The intended command is:

```bash
python 'Grade 9/V2/Chemistry/LearnerProduct/engine/run_chemistry_learner_product.py' \
  --run-manifest /path/to/run.json \
  --out-dir /tmp/chemistry-learner-product
```

Until downstream adapters are implemented, normal generation must fail closed with an explicit unsupported-stage error. `--validate-only` may be used to prove contract/policy bindings.
