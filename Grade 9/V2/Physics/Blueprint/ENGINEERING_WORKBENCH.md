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

The legacy aggregate v2 registry, the former Gravity v1 extension and their validators are retained only as migration provenance/regression evidence. New Workbench manifests consume:

`GENERATED:physics-technical-engineering-gates.v3`

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

The deterministic v3 registry currently contains **24 gates** across:

- Vectors;
- Newtonian Mechanics;
- Gravitation;
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

## Discovery breadth versus control authority

PR #383 is consumed as a pinned **subject-wide discovery/coverage input**, not as a readiness authority. Its 43-subtopic Grade 9–11 catalog is reconciled through:

`policy/physics-engineering-discovery-catalog.pr383.v1.json`

Every discovered subtopic must be explicitly classified as an exact v3 identity, a reviewed v3 mapping, or `MIGRATION_REQUIRED`. Conversely, every live v3 gate must be reconciled as an exact/mapped target or a v3-native/refined gate.

The discovery catalog cannot carry or self-assert technical readiness. The canonical v3 source files, external invariant profile and production validator remain the only technical-readiness control plane. Item IDs, SBA buckets and other case artifacts may stress-test this machinery but may not define its logic or promote source custody.

The generic `PHY-M2D-RELATIVE-VELOCITY` gate is a subject-level example of this rule. It is source-defined from the pinned PR #383 `PHY-KIN-RELATIVE-2D` discovery and has no SBA or question linkage. It owns the reviewed 2D relative-velocity subtraction, river-bank component decomposition, perpendicular-component crossing time and parallel-component drift semantics. `PHY-M2D-MOVING-LAUNCHER` remains a separate specialised projectile gate; no dependency between those gates is inferred merely because they both use Galilean velocity reasoning.

## Workbench lifecycle

```text
ENGINEERING REQUEST
        ↓
TOPIC / SUBTOPIC / BUCKET MANIFEST
        ↓
CANONICAL SUBJECT-WIDE V3 REGISTRY
        ↓
V3 PRODUCTION VALIDATION
        ↓
RECURSIVE PHYSICS PREREQUISITE CLOSURE
        ↓
RESEARCH DOSSIER + CLAIM LEDGER, when engineering_depth = RESEARCH
        ↓
ENGINEERING CLOSURE RECEIPT
        ↓
EXACT RECEIPT CUSTODY BINDING, where a downstream binding is required
        ↓
ENGINEERING PASSPORT
        ↓
ENGINEERING-READY CCU BOUNDARY
```

The manifest declares direct gates only. `compile_engineering_closure.py` derives Physics prerequisites recursively.

## Exact closure custody

New technical bindings use `physics-technical-gate-binding-v2.schema.json` and do not redeclare a prerequisite closure or READY flag.

A binding carries:

- exact request ref;
- exact manifest ref;
- exact closure receipt ID;
- exact full receipt digest;
- exact closure-logic digest;
- exact canonical registry digest.

`validate_technical_gate_binding.py` recompiles the current Workbench closure and fails when any custodied digest is stale. Expanding the subject registry therefore invalidates stale bindings even when a scoped closure still contains the same gates. The 24-gate relative-velocity expansion exercised this rule: the SBA23 closure remained six gates, while its exact receipt and registry digests had to be refreshed.

## SBA23 stress-test integration proof

SBA23 is a case-level stress fixture only; it does not define the Workbench registry or readiness rules. Its manifest declares only:

`PHY-M2D-MOVING-LAUNCHER`

The full 24-gate registry must still derive exactly this six-gate closure:

```text
PHY-VEC-BASICS
PHY-VEC-ADD-SUB
PHY-VEC-COMPONENTS
PHY-M2D-PROJECTILE-COMPONENTS
PHY-M2D-SHARED-CLOCK
PHY-M2D-MOVING-LAUNCHER
```

This proves that expanding the subject registry does not pollute a scoped Workbench closure. The newly added generic `PHY-M2D-RELATIVE-VELOCITY` gate is deliberately absent from this closure unless a separate repository-backed dependency review changes the moving-launcher prerequisite graph.

The closure may be technically READY while `source_item_status = SOURCE_HELD`. That source/legal hold remains independently visible downstream.

## Gravity RESEARCH integration proof

The human-reviewed Gravity discovery creates two domain gates:

```text
PHY-GRAV-FORCE
      ↓
PHY-GRAV-FIELD
```

The Gravity manifest declares only `PHY-GRAV-FIELD`. At `engineering_depth = RESEARCH`, the Workbench additionally requires the release-ready Gravity Research Dossier and Claim Ledger. The canonical registry must derive exactly this 10-gate closure:

```text
PHY-VEC-BASICS
PHY-VEC-ADD-SUB
PHY-VEC-COMPONENTS
PHY-NLM-INTERACTION
PHY-NLM-FBD
PHY-NLM-FIRST-LAW
PHY-NLM-SECOND-LAW
PHY-NLM-THIRD-LAW
PHY-GRAV-FORCE
PHY-GRAV-FIELD
```

Gravitational potential, potential energy, escape speed and orbital mechanics remain outside this request and may not enter by silent scope growth.

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

The v3 suite proves, among other cases:

- deterministic full-registry assembly;
- exact legacy→v3 semantic preservation for migrated base and Gravity gates;
- globally unique semantic authorities;
- valid prerequisite graph and cycle rejection;
- external invariant-profile enforcement;
- physical symbol metadata completeness;
- model-condition bindings;
- representation semantic guards;
- reasoning dependency/order integrity;
- generic relative-velocity subtraction and river-crossing component separation;
- moving-launcher frame conversion before projectile evolution;
- meaningful misconception counterexamples and repair;
- problem-family bindings and intentional family reuse;
- Newtonian model distinctions such as `N != mg` generally, tension model dependence, static-friction inequality and system-boundary consistency;
- Gravity inverse-square, radial-direction, force/field distinction and vector-superposition custody;
- reviewed Gravity discovery and claim-level RESEARCH provenance;
- validator-derived readiness;
- exact closure custody and stale-binding rejection;
- subject-wide PR #383 discovery reconciliation without importing self-asserted readiness;
- case-level closures remaining unchanged under unrelated subject-registry growth;
- CCU authorization only after the current Workbench closure is READY.

Legacy v2 tests continue as regression proofs, but they do not define current authority.

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
