# Physics Engineering Workbench — canonical v3

## Authority

The canonical Physics technical-engineering authority is the source-file registry assembled by:

`engine/build_physics_engineering_gate_registry_v3.py`

from:

`engineering-gates/**/PHY-*.v3.json`

and validated by:

`engine/validate_engineering_gates_v3.py`

The external mandatory-content policy is:

`policy/physics-engineering-gate-invariants.v3.json`

The legacy aggregate v2 registry and v2 validator are retained only as migration provenance and regression evidence. They are not the canonical source for new Workbench manifests.

## Authority boundary

A v3 gate source never self-asserts `ENGINEERING_GATE_READY`.

```text
GATE SOURCE
  technical content + scope_state
        ×
EXTERNAL INVARIANT PROFILE
        ×
PRODUCTION V3 VALIDATOR
        ↓
DERIVED GATE STATE
```

`ACTIVE` may derive `ENGINEERING_GATE_READY` only after schema, graph, authority, equation/symbol, model-condition, representation, reasoning, transformation, misconception, verification, problem-family and invariant-profile checks pass.

`DRAFT` and `SOURCE_SCOPE_HELD` remain blocked.

Engineering readiness does not grant source legality, pedagogical authority, learner mastery, transfer legality or publication authority.

## Canonical registry

The current deterministic v3 registry contains 15 gates across:

- Vectors;
- Newtonian Mechanics;
- Motion in a Plane.

Each gate is stored independently. The registry builder must produce deterministic canonical JSON and a stable SHA-256 digest for the same source set.

Gate content includes:

- authority basis and source-scope state;
- Physics and external prerequisites;
- linked buckets and applicable Cores;
- required invariants;
- canonical concepts;
- equations/relations with typed symbols, physical quantity, domain, unit dimension, frame role and sign role;
- explicit model conditions and failure consequences;
- semantic representations with mandatory elements, forbidden omissions, `must_not_imply`, concept/relation bindings and verification method;
- dependency-aware reasoning steps with inferential-jump severity and failure-if-skipped;
- Core-role transformations;
- misconception models, plausibility, counterexamples and technical/representation repair;
- verification requirements;
- problem-family engineering anatomy;
- provisional intrinsic engineering difficulty vector.

Problem-family IDs may intentionally be shared across gates when the same family spans multiple technical gates. Concepts, relations, representations and misconceptions remain globally unique authorities.

## Workbench lifecycle

```text
ENGINEERING REQUEST
        ↓
TOPIC / SUBTOPIC / BUCKET MANIFEST
        ↓
CANONICAL V3 REGISTRY
        ↓
V3 PRODUCTION VALIDATION
        ↓
RECURSIVE PHYSICS PREREQUISITE CLOSURE
        ↓
RESEARCH DOSSIER + CLAIM LEDGER, when engineering_depth = RESEARCH
        ↓
ENGINEERING CLOSURE RECEIPT
        ↓
EXACT RECEIPT CUSTODY BINDING
        ↓
ENGINEERING PASSPORT
        ↓
ENGINEERING-READY CCU BOUNDARY
```

The manifest declares direct gates only. `compile_engineering_closure.py` derives Physics prerequisites recursively.

## Exact closure custody

New technical bindings use `physics-technical-gate-binding.v2.schema.json` and do not redeclare a prerequisite closure or READY flag.

A binding carries:

- exact request ref;
- exact manifest ref;
- exact closure receipt ID;
- exact full receipt digest;
- exact closure-logic digest;
- exact canonical registry digest.

`validate_technical_gate_binding.py` recompiles the current Workbench closure and fails when any custodied digest is stale.

## SBA23 integration proof

The SBA23 manifest declares only:

`PHY-M2D-MOVING-LAUNCHER`

The full 15-gate registry must still derive exactly this six-gate closure:

```text
PHY-VEC-BASICS
PHY-VEC-ADD-SUB
PHY-VEC-COMPONENTS
PHY-M2D-PROJECTILE-COMPONENTS
PHY-M2D-SHARED-CLOCK
PHY-M2D-MOVING-LAUNCHER
```

This proves that expanding the subject registry does not pollute a scoped Workbench closure.

The closure may be technically READY while `source_item_status = SOURCE_HELD`. That source/legal hold remains independently visible downstream.

## Engineering Passport

For v3 closures the Passport is a human-readable projection of validated authority. It includes:

- closure and gate states;
- technical coverage counts;
- HIGH_FRAGILITY reasoning hotspots;
- direct-gate engineering difficulty dimensions;
- registry/closure custody;
- source state;
- CCU technical authorization;
- `publication_authorization = NOT_IMPLIED`.

The Passport has no independent authority to promote a blocked closure.

## Validation/falsification

The v3 suite must prove:

- deterministic full-registry assembly;
- exact v2→v3 semantic preservation for all migrated gates;
- globally unique semantic authorities;
- valid prerequisite graph and cycle rejection;
- external invariant-profile enforcement;
- physical symbol metadata completeness;
- model-condition bindings;
- representation semantic guards;
- reasoning dependency/order integrity;
- moving-launcher frame conversion before projectile evolution;
- meaningful misconception counterexamples and repair;
- problem-family bindings and intentional family reuse;
- Newtonian model distinctions such as `N != mg` generally, tension model dependence, static-friction inequality and system-boundary consistency;
- validator-derived readiness;
- exact closure custody and stale-binding rejection;
- CCU authorization only after current Workbench closure is READY.

The legacy v2 validator/Workbench tests continue to run as regression proofs during migration, but they do not define current authority.

## Engineering depth versus learner difficulty

`FOUNDATION | STANDARD | RESEARCH` is Workbench engineering depth.

It is independent of the provisional intrinsic difficulty badge `EASY | MEDIUM | HARD` and independent of learner knowledge state.

A RESEARCH request requires a release-ready Research Dossier and Claim Ledger. Research evidence may support technical/pedagogical engineering decisions but may not rewrite Physics truth or source custody.

## Publication boundary

Engineering closure answers only:

> Is the requested Physics scope technically engineered with complete prerequisite closure?

It does not answer:

> Is Core1A pedagogically complete? Is Core2 transfer legal? Has the learner mastered it? Is a PDF authorized to publish?

Those remain downstream Blueprint gates.
