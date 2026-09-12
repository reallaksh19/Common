# Mathematics V2 — Core (1A): learner textbook realization

Core (1) is a **semantic instructional plan**. It is not, by itself, a learner textbook.
PR #323 currently proves that Core1 obligations are present and that a PDF can be rendered,
but its learner PDF still exposes authoring obligations such as `author a new instance of ...`
and pipeline/review language.

Core (1A) is the boundary that turns Core (1) into an actual learner book.

## Contract

```text
MathCore1StudyPlan
        |
        v
Core (1A)
  - resolve the lesson capability
  - resolve bound PCK
  - resolve problem-family semantics
  - materialize fresh capability-focused learner problems inside that family
  - write learner-facing explanation
  - realize misconception repair
  - realize worked -> guided -> less-help -> independent -> challenge
  - run textbook-quality gates
  - render book-like PDF
        |
        +--> core1a_textbook_manuscript.json
        +--> core1a_quality_audit.json
        `--> core1a_student_textbook.pdf
```

Core (1A) deliberately does **not** reuse original assessment questions. Those remain Core (2)
transfer assets. Every learner problem in Core (1A) is a fresh, deterministic instance of the
problem family declared by Core (1).

## Capability first, family invariant second

Core1 is capability-driven. One problem family can exercise several capabilities. For example,
an equal-distance coordinate family can require binomial expansion, equality preservation,
axis semantics and the final equidistance model. A learner lesson on **binomial square expansion**
must therefore not be titled or written as though its instructional target were the whole
equidistance family.

The canonical Core1A entrypoint installs a capability-aware authoring layer:

- the lesson title and explanation follow `capability_ref` and its matching PCK asset;
- the authored problems still obey the declared `problem_family_ref`;
- prerequisite capabilities get their own focused worked examples rather than a generic family problem;
- when more than one PCK asset is bound, Core1A prefers the asset whose `capability_refs` explicitly contain the lesson capability.

This distinction is release-critical for textbook quality: mathematical provenance stays family-grounded,
while the student is actually taught the capability Core1 says the lesson is about.

## Why this stage is separate

`MathCore1StudyPlan` correctly records instructional obligations such as ANCHOR, REPRESENT,
WORKED, GUIDED, FADED, INDEPENDENT, VERIFY and TRANSFER. Those are machine-facing obligations.
They should not be printed as textbook prose.

Core (1A) therefore preserves Core (1)'s mathematical authority while changing the learner surface:

- internal capability/PCK/problem-family identifiers stay in trace data, not learner pages;
- a full-teaching lesson has at least two worked examples;
- required WORKED/GUIDED/FADED/INDEPENDENT/TRANSFER roles are actual problems, not plans to author problems;
- misconception information is converted into a learner-facing mistake + repair;
- hints fade rather than giving away the answer;
- lesson prose follows the mathematics rather than the pipeline;
- PDF pagination is content-driven and book-like rather than fixed-card/slide-like.

## Fail-closed behavior

The engine refuses to publish when a required family has no authored instance generator.

Important falsifiers:

- `CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED`
- `CORE1A_FAMILY_GENERATOR_MISSING`
- `CORE1A_INTERNAL_JARGON_LEAK`
- `CORE1A_INTERNAL_IDENTIFIER_LEAK`
- `CORE1A_WORKED_EXAMPLE_DEPTH_MISSING`
- `CORE1A_CONCEPT_EXPLANATION_UNDERREALIZED`
- `CORE1_MISCONCEPTION_REPAIR_NOT_MATERIALIZED`
- `CORE1A_QUALITY_GATE_FAILED`

This is intentional. A missing learner object must not be replaced by an authoring instruction.

## CLI

Use the capability-aware entrypoint:

```bash
python 'Grade 9/V2/Mathematics/Core1A/engine/realize_math_core1a.py' \
  --core1-plan /path/to/core1_study_plan.json \
  --out-dir /tmp/core1a
```

By default the engine resolves the Mathematics PCK candidate index and problem-family index from
the repository. They can be overridden with `--pck-index` and `--problem-family-index`.

## Current family coverage

The first Core (1A) implementation materializes the 14 problem families currently present in the
Math problem-family registry on PR #323:

- Euclid classification
- coordinate distance
- quadrant/sign transformation
- line intercept
- line from slope + point
- unordered-pair count
- collinearity by slope
- Euclid parallel condition
- linear parameter sufficiency
- intersection then line
- equidistant point on an axis
- equilateral-coordinate construction
- linear trend/extrapolation
- river-current linear system

It also provides explicit capability-focused authoring for prerequisite/bridge capabilities in the
current cold-start scope, including angle sum, arithmetic division, binomial-square expansion,
equality preservation, fraction arithmetic, geometric modelling, two-point line construction,
linear-system setup/solve, ordered-pair semantics, sign propagation, slope computation,
substitution, unit interpretation, variable semantics and word modelling.

A future topic is not silently generalized. If Core (1) asks Core (1A) for a new family, the run
fails until that family receives learner-authoring support.

## CI proof of the interface

The Core1A workflow first runs #323's real Mathematics cold-start chain, writes its exact
`core1_study_plan.json`, then feeds that file to Core1A. The produced PDF is text-inspected for
internal jargon/template leakage and the workflow uploads both the exact Core1 input and Core1A
outputs. This makes the Core1 -> Core1A -> PDF boundary directly auditable.

## Release meaning

Core (1A) inherits the release class of its source Core (1) plan. A better learner PDF does not
convert provisional PCK into producer-legal PCK and does not replace the M-L human gates.
