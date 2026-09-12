# Mathematics V2 — Core (1A): textbook-quality teaching realization

Core (1) is the governed **semantic instructional plan**. Core (1A) is the learner-product layer that turns that approved plan into textbook-quality teaching content and a final learner PDF.

The boundary is intentionally narrow:

```text
Core (1): governed instructional structure and mathematical authority
        |
        v
Core (1A): textbook-quality teaching realization
        |
        +--> core1a_textbook_manuscript.json
        +--> core1a_quality_audit.json
        `--> core1a_student_textbook.pdf
```

Core (1A) may substantially improve explanation, examples, mathematical representation, diagrams, worked-example narration, misconception repair, hints, typography, pagination and page composition. It must **not redesign the approved instructional architecture**.

## Structure-preservation invariant

The lesson structure emitted by Core (1) is an immutable product contract. Core (1A) preserves, as applicable:

- lesson/section order and identity;
- capability and PCK bindings;
- problem-family authority;
- learner-practice identifiers and their answer mappings;
- method-selection/readiness relationships;
- required worked/guided/faded/independent/transfer roles;
- mathematical verification obligations;
- release/provenance class.

Physical page count, whitespace, visual composition and the number of explanatory micro-examples are **not** structural invariants. Core (1A) may expand a 13-page plan into a longer textbook when that is required to teach the mathematics well.

In short:

```text
preserve instructional architecture != preserve existing page composition
```

## Textbook-quality transformation

Within the preserved structure, Core (1A) should aggressively improve the learner surface:

- lead difficult ideas with concrete mathematics before abstraction where the approved lesson allows it;
- connect symbolic rules to visual or structural representations;
- use worked examples that expose the reason for each step, not only the final procedure;
- introduce technical vocabulary only when it is mathematically needed;
- materialize actual learner problems rather than authoring instructions;
- convert misconception metadata into learner-facing mistake + repair;
- provide meaningful verification/checking moves;
- use page composition that follows the mathematics rather than fixed cards or pipeline labels.

A quality pass that merely changes styling or inserts small callouts is insufficient. Core (1A) exists to add material teaching value while preserving the approved structure.

## Capability first, family invariant second

Core1 is capability-driven. One problem family can exercise several capabilities. A learner lesson must therefore follow `capability_ref` and its matching PCK asset, while authored instances remain valid members of the declared `problem_family_ref`.

The canonical Core1A entrypoint installs a capability-aware authoring layer:

- the lesson title and explanation follow `capability_ref` and its matching PCK asset;
- the authored problems still obey the declared `problem_family_ref`;
- prerequisite capabilities get focused worked examples rather than a generic family problem;
- when more than one PCK asset is bound, Core1A prefers the asset whose `capability_refs` explicitly contain the lesson capability.

This distinction is release-critical: mathematical provenance stays family-grounded while the student is actually taught the capability Core (1) says the lesson is about.

## Fresh learner instances

Core (1A) deliberately does **not** reuse original assessment questions. Those remain governed Core (2) transfer assets and are realized for learners in Core (2A).

Every Core (1A) learner problem is a fresh, deterministic instance of the family declared by Core (1).

## Fail-closed behavior

The engine refuses to publish when a required family has no authored instance generator or when learner-surface quality is under-realized.

Important falsifiers include:

- `CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED`
- `CORE1A_FAMILY_GENERATOR_MISSING`
- `CORE1A_INTERNAL_JARGON_LEAK`
- `CORE1A_INTERNAL_IDENTIFIER_LEAK`
- `CORE1A_WORKED_EXAMPLE_DEPTH_MISSING`
- `CORE1A_CONCEPT_EXPLANATION_UNDERREALIZED`
- `CORE1_MISCONCEPTION_REPAIR_NOT_MATERIALIZED`
- `CORE1A_QUALITY_GATE_FAILED`

The next quality-policy revision should also fail on **structural drift**: reordering approved lessons, losing identifiers/answer mappings, or substituting a new learner taxonomy for the approved Core (1) architecture.

## CLI

Use the capability-aware entrypoint:

```bash
python 'Grade 9/V2/Mathematics/Core1A/engine/realize_math_core1a.py' \
  --core1-plan /path/to/core1_study_plan.json \
  --out-dir /tmp/core1a
```

By default the engine resolves the Mathematics PCK candidate index and problem-family index from the repository. They can be overridden with `--pck-index` and `--problem-family-index`.

## Current family coverage

The first Core (1A) implementation materializes the 14 problem families currently present in the Mathematics problem-family registry on PR #323:

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

It also provides explicit capability-focused authoring for prerequisite/bridge capabilities in the current cold-start scope, including angle sum, arithmetic division, binomial-square expansion, equality preservation, fraction arithmetic, geometric modelling, two-point line construction, linear-system setup/solve, ordered-pair semantics, sign propagation, slope computation, substitution, unit interpretation, variable semantics and word modelling.

A future topic is not silently generalized. If Core (1) asks Core (1A) for a new family, the run fails until that family receives learner-authoring support.

## CI proof of the interface

The Core1A workflow first runs #323's real Mathematics cold-start chain, writes its exact `core1_study_plan.json`, then feeds that file to Core1A. The produced PDF is text-inspected for internal jargon/template leakage and the workflow uploads both the exact Core (1) input and Core (1A) outputs.

## Relation to Core (2A)

The final learner-product architecture is:

```text
Core (1)  --> Core (1A): textbook-quality teaching PDF
Core (2)  --> Core (2A): textbook-quality source-transfer/practice PDF
```

Core (2A) is defined separately under `Mathematics/Core2A/`. It preserves Core (2)'s source-question authority and attempt/solution structure while improving representation and worked-solution readability.

## Release meaning

Core (1A) inherits the release class of its source Core (1) plan. Better learner realization does not convert provisional PCK into producer-legal PCK and does not replace the M-L human gates.
