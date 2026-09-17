# Engineering Readiness Kernel — global authority above Blueprint

## Authority order

The Engineering Gate is upstream authority. Blueprint is a downstream consumer/adapter.

```text
DISCOVERY / EVIDENCE
        ↓
SUBJECT ENGINEERING GATES + CROSS-DOMAIN AUTHORITY RECEIPTS
        ↓
GLOBAL ENGINEERING GATE READINESS POLICY
        ↓
ENGINEERING READINESS ENVELOPE
        ↓
PHYSICS BLUEPRINT AUTHORITY PROJECTION
        ↓
BLUEPRINT / OTHER DECLARED PHYSICS CONSUMERS
```

The canonical global authority is under:

- `Grade 9/V2/Shared/EngineeringGate/policy/readiness-policy.v1.json`
- `Grade 9/V2/Shared/EngineeringGate/contracts/`
- `Grade 9/V2/Shared/EngineeringGate/engine/evaluate_readiness.py`

Blueprint-local readiness code is compatibility/orchestration only. It may compile subject receipts and pass them to the global Engineering Gate, but it does not own readiness policy.

For Physics Blueprint orchestration, `engine/compile_physics_blueprint_authority.py` is the canonical Physics-local adapter. It combines an already-derived Physics scoped-evidence receipt with the unchanged Shared EngineeringGate envelope into a digest-bound projection. It does not grant release or publication authority.

## Non-negotiable invariant

> **Blueprint must never be modified to recognize a topic, subtopic, bucket, prerequisite, downstream consumer, or exception merely because a particular case needs it.**

No Blueprint readiness branch may depend on remembered domain facts, case IDs, special topic names, fixed prerequisite IDs, or a hand-maintained consumer list.

All case variation must arrive as governed data:

- engineering request;
- engineering manifest;
- canonical subject gate registry;
- research evidence receipts when required;
- provider-owned cross-domain authority receipts;
- the global Engineering Gate policy.

If data is absent, the system holds or rejects. It does not infer from model memory.

## Physics curriculum-scope authority

A repository file reference is not, by itself, curriculum authority for a Physics scope.

For a named curriculum such as `CBSE`, support requires an exact row in:

`registry/physics-curriculum-scope-bindings.v1.json`

The selector is exact over:

```text
grade
+ curriculum
+ scope_kind
+ scope_ref
+ required_gate_ids
```

The exact binding then identifies the curriculum authority refs and classification. A non-empty `curriculum_authority_refs` list without an exact governed binding remains `HELD_INSUFFICIENT_AUTHORITY`.

This prevents semantic evidence, assessment prevalence, question-bank material, or an arbitrary repository file from being promoted into Physics curriculum truth merely because a caller supplied its path.

`REPOSITORY_GOVERNED_PHYSICS` remains the internal Engineering-scope class used by existing subject Engineering requests; it is not equivalent to an external curriculum claim such as CBSE.

## Discovery versus consumption

The governing rule remains:

> **Discovery is permissive; promotion and consumption are strict.**

Broad discovery, source inspection, reconciliation, and research dossier construction may continue while prerequisite authority is unresolved. Missing authority remains visible. A downstream consumer may proceed only when the Engineering Readiness Envelope explicitly allows that consumer.

## Exact-manifest custody

Consumer permission is data-driven from the manifest's `downstream_consumers` field. The Engineering closure receipt binds the exact manifest with `manifest_digest`.

The global evaluator rejects:

- a manifest belonging to another request;
- a receipt belonging to another manifest;
- same-ID manifest content drift;
- a domain closure bound to another engineering receipt;
- a requested consumer that is not declared by the exact manifest.

This prevents a caller from adding a consumer after engineering closure or from asking Blueprint to remember that a consumer "should" be allowed.

## Generic readiness dimensions

The global envelope exposes subject-neutral dimensions:

- `technical` — subject Engineering Gate closure;
- `research_provenance` — research evidence state when the request depth requires it;
- `external_prerequisites` — provider-owned cross-domain authority only;
- `source_authority` — independent source/legal state.

The global evaluator does not contain subject/topic prerequisite IDs. Subject adapters produce technical and cross-domain receipts; the global Engineering Gate joins them according to policy.

## Consumer permission rule

Permissions are generated only for consumers declared by the exact manifest.

For an ordinary technical consumer:

```text
ALLOWED ⇔ technical closure READY
          AND external prerequisite closure READY
```

Consumers listed in the global policy as non-authorizing domains remain `NOT_AUTHORIZED` regardless of technical readiness. Engineering readiness cannot manufacture an authority it does not own.

A consumer absent from the manifest is not `BLOCKED`, `ALLOWED`, or guessed. A request to require it fails as `E_ENG_GATE_CONSUMER_UNDECLARED`.

## Physics Blueprint authority projection

Physics Blueprint consumers must not independently recompute:

- named-curriculum support;
- technical Engineering readiness;
- external prerequisite readiness;
- Engineering consumer permissions;
- publication authorization.

They consume the Physics authority projection, which carries:

```text
exact scoped-evidence curriculum binding state
+ exact Shared EngineeringGate envelope digest
+ readiness dimensions
+ manifest-derived consumer permissions
+ publication_authorization = NOT_IMPLIED
+ release_authority = NOT_GRANTED_BY_PROJECTION
```

Blueprint may still derive Blueprint-owned orchestration state from these facts and from the existence/custody of Blueprint artifacts. For example, it may decide that a Core stage is not instantiated or is blocked before stage release. It may not reinterpret an upstream `HELD`, `BLOCKED`, or `NOT_AUTHORIZED` authority state as ready.

The seven-core stress compiler is an executable consumer of this rule. It must not import the Shared evaluator directly, inspect raw curriculum refs as authority, or derive provider readiness from raw domain-receipt status.

## Subject adapter responsibilities

A subject adapter may:

1. validate its canonical Engineering Gate registry;
2. derive recursive prerequisites from that registry;
3. compile a technical closure receipt;
4. bind the exact manifest digest;
5. compile provider-owned external prerequisite closure/demands;
6. submit those receipts plus the exact manifest to the global Engineering Gate evaluator.

A subject adapter may not:

- hardcode a downstream consumer set;
- hardcode external prerequisite IDs in readiness policy;
- grant cross-domain authority locally;
- override a global held state;
- treat a Passport or internal projection as aggregate authority.

## Adding new engineering scope

Ordinary new scope is a data operation:

1. add/reconcile canonical Engineering Gate data;
2. add/update request and manifest data;
3. add research evidence only when the request depth requires it;
4. provide authoritative external-domain receipts when available;
5. run the same global evaluator.

For an external curriculum claim, add or reconcile an exact Physics curriculum-scope binding as governed data. Do not add a Blueprint `if topic == ...`, a special workflow, or a remembered exception. New code is justified only for a genuinely new invariant class that cannot be represented by the existing Engineering Gate contracts.

## CI invariant

CI proves three layers independently:

1. `Grade 9/V2/Shared/EngineeringGate/tests/test_readiness_policy.py` uses topic-agnostic synthetic data to prove the global policy, exact-manifest custody, manifest-driven consumers, held-state behavior, and rejection of undeclared remembered consumers.
2. Physics scoped-evidence tests prove named-curriculum authority requires an exact grade/curriculum/scope/gate binding and that loose repository refs cannot promote curriculum truth.
3. Physics integration/stress tests prove that Blueprint consumes the Physics authority projection and does not reconstruct Shared EngineeringGate or curriculum authority locally.

A legitimate `HELD` state is a successful governance output. CI fails when code bypasses the gate, mutates custody, invents authority, or attempts blocked/undeclared consumption.

## Visibility

The canonical global Engineering readiness object remains the Shared Engineering Readiness Envelope. The Physics Blueprint authority projection is a digest-bound downstream adapter that combines that envelope with Physics curriculum-scope custody for Physics orchestration. Neither object grants publication or human-review authorization.
