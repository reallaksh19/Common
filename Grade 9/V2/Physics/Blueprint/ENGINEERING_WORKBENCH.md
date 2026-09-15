# Physics Engineering Workbench — subject adapter beneath global Engineering Gate

## Authority order

The Physics Workbench owns **Physics technical gate content and Physics technical closure**. It does not own aggregate downstream readiness.

```text
Physics gate sources + Physics invariant profile
        ↓
Physics registry builder / validator
        ↓
Physics technical closure receipt
        ┐
        ├──→ Grade 9/V2/Shared/EngineeringGate → Engineering Readiness Envelope
        ┘        ↑
provider-owned external-domain receipts ────────┘
                                             ↓
                              manifest-declared consumers
```

The global consumer authority is:

`Grade 9/V2/Shared/EngineeringGate/`

Blueprint may adapt Physics data into that authority. Blueprint must not infer a consumer, prerequisite, exception, or readiness decision from a case, topic name, fixture, or model memory.

## Physics technical authority

Canonical Physics technical-engineering authority is assembled by:

`engine/build_physics_engineering_gate_registry_v3.py`

from:

`engineering-gates/**/PHY-*.v3.json`

and validated by:

`engine/validate_engineering_gates_v3.py`

with the external invariant profile:

`policy/physics-engineering-gate-invariants.v3.json`

A source gate never self-asserts `ENGINEERING_GATE_READY`. Readiness is derived from source content × invariant profile × production validator. `DRAFT` and `SOURCE_SCOPE_HELD` remain blocked.

The legacy aggregate v2 registry and legacy extensions remain migration/regression evidence only.

## No case-driven Blueprint logic

Ordinary scope variation is data:

- Engineering Request;
- Engineering Manifest;
- canonical Physics gate sources;
- RESEARCH dossier and claim ledger when required;
- provider-owned external-domain authority receipts.

The manifest declares direct gates and downstream consumers. The subject closure compiler derives recursive Physics prerequisites from the registry. The closure receipt binds the **exact manifest bytes** with `manifest_digest`.

No new topic, bucket, subtopic, or question may require a Blueprint `if case == ...` branch. A new code path is justified only by a new invariant class that cannot be represented by the existing contracts.

## Discovery versus control authority

Broad discovery inputs are evidence, not readiness authority. Discovery may map, reuse, split, extend, or propose gates, but promotion requires canonical gate data and production validation.

Case artifacts—including SBA IDs, question IDs, and topic fixtures—may be used as stress tests. They may not define the registry algorithm, prerequisite algorithm, global readiness policy, or consumer permission rule.

## Subject closure lifecycle

```text
ENGINEERING REQUEST
        ↓
MANIFEST (direct gates + declared consumers)
        ↓
CANONICAL PHYSICS V3 REGISTRY
        ↓
PHYSICS V3 VALIDATION
        ↓
RECURSIVE PHYSICS PREREQUISITE CLOSURE
        ↓
RESEARCH DOSSIER + CLAIM LEDGER when depth = RESEARCH
        ↓
ENGINEERING CLOSURE RECEIPT
        ↓
DIAGNOSTIC PHYSICS PASSPORT (optional)
        ↓
GLOBAL ENGINEERING GATE EVALUATION
        ↓
ENGINEERING READINESS ENVELOPE
```

The Physics closure answers only whether the requested Physics technical scope is engineered. It cannot authorize a downstream consumer.

## Exact manifest and receipt custody

The closure receipt carries:

- exact request ID;
- exact manifest ID;
- exact `manifest_digest`;
- exact registry digest;
- exact direct/transitive gate sets and derived states;
- exact closure-logic digest;
- source-item state.

Bindings that custody a closure recompile the current closure and compare exact digests. Stale data fails closed. Because the manifest digest is in the closure payload, a same-ID manifest mutation changes closure custody and cannot silently expand consumers or scope.

## Cross-domain prerequisites

Physics gate data may declare external prerequisites. The Physics adapter derives external demands from the active registry and routes them through the Shared CrossDomain provider registry.

Physics may not self-certify another domain. Only provider-owned authority receipts can close an external prerequisite. Missing authority is a valid `HELD` governance state; it does not stop discovery, but it does stop affected downstream consumption at the global Engineering Gate.

## Engineering Passport

The Passport is a human-readable **diagnostic projection** of subject technical closure.

It may show:

- technical gate states and coverage;
- fragility hotspots;
- engineering difficulty profiles;
- registry/closure custody;
- source state.

It must not issue consumer permission. Its contract therefore reports:

`consumer_authorization = NOT_EVALUATED`

Any previous interpretation of the Passport as a CCU/Core authorization boundary is obsolete. Only the global Engineering Readiness Envelope may report a manifest-declared consumer as `ALLOWED` or `BLOCKED`.

## Generic CI rule

CI proves two independent layers:

1. `Grade 9/V2/Shared/EngineeringGate/tests/test_readiness_policy.py` proves the global policy with topic-agnostic synthetic data and generic consumer names.
2. Physics Workbench tests prove subject registry semantics, closure derivation, exact custody, research evidence, and that Physics receipts are accepted by the global evaluator.

The global falsifiers specifically prove that:

- permissions come from the exact manifest rather than a hardcoded consumer list;
- same-ID manifest mutation cannot add a consumer;
- an external hold blocks every declared technical consumer;
- an undeclared consumer is rejected rather than inferred from memory.

Subject integration fixtures may remain specific because they are falsification evidence, not branching logic.

## Engineering depth versus learner difficulty

`FOUNDATION | STANDARD | RESEARCH` is engineering evidence depth. It is independent of learner knowledge state and independent of the provisional intrinsic engineering-difficulty profile.

A `RESEARCH` request requires a release-ready Research Dossier and Claim Ledger. Research evidence may support engineering decisions but may not rewrite Physics truth, cross-domain authority, source custody, pedagogy, learner mastery, transfer legality, or publication authority.

## Publication boundary

Neither Physics technical closure nor its Passport authorizes publication. Publication remains independently governed downstream. The global Engineering Gate also marks publication as non-authorizing; it cannot manufacture authority outside its domain.
