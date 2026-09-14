# Physics Engineering Workbench v1

## Purpose

The Workbench makes the existing Technical Engineering Gate layer visible and operable without changing its authority.

The canonical technical gate registry remains:

`policy/physics-technical-engineering-gates.v2.json`

The canonical production gate validator remains:

`engine/validate_engineering_gates_v2.py`

The Workbench does not create learner mastery, source legality, pedagogical authority, publication authority, or empirical calibration. It computes whether a requested topic/subtopic has complete technical-engineering prerequisite closure before CCU consumes it.

## Lifecycle

```text
ENGINEERING REQUEST
        ↓
TOPIC / SUBTOPIC MANIFEST
        ↓
CANONICAL GATE REGISTRY
        ↓
PRODUCTION GATE VALIDATION
        ↓
RECURSIVE PHYSICS PREREQUISITE CLOSURE
        ↓
RESEARCH DOSSIER + CLAIM LEDGER, when depth = RESEARCH
        ↓
ENGINEERING CLOSURE RECEIPT
        ↓
ENGINEERING PASSPORT
        ↓
ENGINEERING-READY CCU BOUNDARY
        ↓
CCU technical consumption, only when READY
```

Readiness is derived. Neither requests nor manifests contain an `engineering_ready` field.

## Engineering Request

`contracts/engineering-request.schema.json`

The request records user intent:

- requested topic and scope;
- engineering depth: `FOUNDATION | STANDARD | RESEARCH`;
- curriculum/exam scope where supplied;
- intended downstream consumers;
- `AUTO_DISCOVER` as the workflow action.

The request does not decide whether the registry operation should eventually be reuse, extension, child creation or refactor. That decision belongs to engineering discovery/review.

## Topic/Subtopic Manifest

`contracts/engineering-topic-manifest.schema.json`

A manifest declares the direct technical gates required by the requested scope. It does not manually enumerate every prerequisite. The closure compiler derives Physics prerequisites recursively from the canonical registry.

Each manifest binds its scope explicitly with:

- `scope_kind`: `TOPIC | SUBTOPIC | BUCKET`;
- `scope_ref`: the exact topic/subtopic/bucket identifier being authorized.

The manifest keeps source state independent from technical state through:

`INDEPENDENT_OF_TECHNICAL_GATE | SOURCE_HELD | SOURCE_READY`

## Closure compiler

`engine/compile_engineering_closure.py`

The compiler:

1. validates the request and manifest contracts;
2. validates the canonical registry using the existing production gate validator;
3. recursively computes Physics prerequisite closure;
4. fails on dependency cycles;
5. exposes missing/non-ready gates as blockers;
6. enforces Research Dossier + Claim Ledger readiness when `engineering_depth = RESEARCH`;
7. emits registry and closure SHA-256 digests;
8. derives `READY | BLOCKED` rather than trusting a user-authored readiness flag.

A structurally invalid canonical registry fails closed before a receipt is issued.

## Research mode

`RESEARCH` is engineering depth, not learner difficulty.

A Research request cannot close without both:

- `contracts/engineering-research-dossier.schema.json` artifact in `RESEARCH_DOSSIER_READY` state;
- `contracts/engineering-claim-ledger.schema.json` artifact in `CLAIM_LEDGER_READY` state.

This keeps research-level engineering evidence separate from Grade/exam difficulty and prevents a cosmetic research label.

## Engineering Passport

`engine/compile_engineering_passport.py`

The Passport is the human-visible projection of the closure receipt. It shows:

- topic/scope and engineering depth;
- direct and transitive gate counts;
- each gate state;
- overall technical state;
- independent source state;
- CCU technical authorization;
- next action.

The Passport cannot convert a blocked or internally inconsistent closure receipt into `ENGINEERING_READY`.

## Engineering-ready CCU boundary

`engine/validate_ccu_engineering_ready.py`

This is the execution boundary between Engineering and CCU. It does not replace the existing CCU validator. It:

1. verifies that the engineering manifest is a `BUCKET` manifest;
2. requires the manifest `scope_ref` to equal the CCU `bucket_id`;
3. requires `CCU` to be an authorized downstream technical consumer;
4. recompiles the current engineering closure from the current registry;
5. refuses CCU validation unless that closure is `READY`;
6. invokes the existing `validate_ccu_v2.py` only after the technical boundary closes;
7. returns the exact closure receipt ID/digest with the CCU validation result.

This prevents a stale or manually asserted technical-ready flag from authorizing CCU.

## SBA-23 golden proof

The v1 golden request intentionally declares only one direct gate:

`PHY-M2D-MOVING-LAUNCHER`

The compiler must derive exactly the already-established six-gate closure:

```text
PHY-VEC-BASICS
PHY-VEC-ADD-SUB
PHY-VEC-COMPONENTS
PHY-M2D-PROJECTILE-COMPONENTS
PHY-M2D-SHARED-CLOCK
PHY-M2D-MOVING-LAUNCHER
```

The corresponding manifest binds `scope_ref = M2D-SBA-23`. The engineering-ready CCU boundary must reproduce this closure before invoking the existing SBA-23 CCU validator.

The technical closure may be READY while `source_item_status = SOURCE_HELD`; source/legal custody remains downstream and independent.

## Falsification requirements

`tests/test_physics_engineering_workbench_v1.py` proves at minimum:

- the SBA-23 closure is reproduced from one direct gate;
- SBA-23 CCU validation succeeds through the engineering-ready boundary;
- missing direct gates block both the receipt and CCU boundary;
- incomplete and source-held technical gates block;
- cyclic prerequisites fail structurally;
- invalid transitive registry references are rejected by the production gate validator;
- Research depth without dossier/claim evidence blocks;
- manual readiness fields are rejected by closed-world schemas;
- Passport generation rejects a tampered contradictory receipt;
- a manifest cannot authorize a different CCU bucket.

## Deliberate v1 non-goals

Workbench v1 does not yet:

- add Gravity or Thermodynamics technical content;
- automatically choose `REUSE | EXTEND | CREATE_CHILD | REFACTOR` from semantic similarity;
- split the existing aggregate gate registry into one gate per source file;
- claim empirical/psychometric validation.

Those changes follow only after the Workbench reproduces the existing canonical closure without regression.

## Project PDF provenance rule

Any PDF produced for this project must be generated from the current repository Blueprint re-read for that specific task. Blueprint content must not be reconstructed from model memory, previous PDFs, prior chat summaries, or unauthorised subject-memory substitutions. Unsupported content remains unsupported until the current repository supplies or authorizes it.
