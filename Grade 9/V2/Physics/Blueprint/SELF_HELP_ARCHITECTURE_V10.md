# Physics Self-Help Architecture V10 — scope-consistent execution and executable stress receipts

V10 supersedes V9 as the canonical learner-product architecture. V9 remains historical and all of its custody, differentiation, TTU, calibration and publication guarantees remain in force unless explicitly refined here.

## V10 correction

Every governed decision must be bound to the **same declared execution scope**. Topic-wide evidence may not be silently reused to justify a subtopic, bucket or case decision. Verified absence is a first-class reconciled state; unknown evidence is not equivalent to verified absence.

```text
ORIGINAL / OBSERVED GROUND TRUTH
        ↓
SCOPED EXECUTION ENVELOPE
(non-authoritative projection of existing repository evidence)
        ↓
CORE0 — scope-matched routing
        ↓
CORE1 ↔ independent validation ↔ CORE2 COVERAGE
        ↓
JOIN
  ├─ DEMANDS_PRESENT
  ├─ VERIFIED_NO_TARGET_DEMAND
  └─ COVERAGE_UNKNOWN → BLOCK
        ↓
CANONICAL DOMAIN REGISTRY
        ↓
CROSS-DOMAIN PREREQUISITE RECEIPT
        ↓
PHYSICS TECHNICAL ENGINEERING GATES
        ↓
CCU → CDAU → SDU/LAU → TTU
        ↓
publication / learner runtime
        ↓
CAL
```

The Scoped Execution Envelope does not manufacture truth or curriculum authority. It binds execution to exact repository evidence and prevents broader-scope evidence substitution.

## Scope consistency

Supported execution scopes are `TOPIC | SUBTOPIC | BUCKET | CASE`. A narrower scope compiles a scoped evidence receipt before Core0 routing, binding exact topic authority, target scope, required technical gates, semantic refs, assessment corpus, assessment coverage, requested curriculum refs and executable repository assertions. The routing policy itself is unchanged; only its evidence boundary is hardened. A topic route and target route may legitimately differ.

## Target assessment coverage and JOIN v2

Assessment coverage has exactly three states: `DEMANDS_PRESENT | VERIFIED_NO_TARGET_DEMAND | COVERAGE_UNKNOWN`.

`VERIFIED_NO_TARGET_DEMAND` requires exact scope/corpus digests, a target match count of zero and evidence refs. It is not a failure and does not create a synthetic question. `COVERAGE_UNKNOWN` blocks assimilation because absence has not been proved.

Demand-bearing JOIN behavior remains unchanged. For verified zero target demand:

```text
VERIFIED_NO_TARGET_DEMAND
        ↓
JOIN_READY_NO_CORE2_DEMAND
assimilation_ready = true
```

This permits source-backed conceptual construction while leaving Core2/Core2A independently held when no legal target item exists.

## Cross-domain prerequisites

Physics may require external prerequisites such as Mathematics but may not certify them. Each external prerequisite is `READY_FROM_AUTHORITATIVE_DOMAIN | HELD_NO_DOMAIN_RECEIPT`. Missing authoritative-domain receipts hold cross-domain closure without mutating Physics gate readiness.

## State semantics

V10 distinguishes `PASS | READY | HELD | BLOCKED | NOT_INSTANTIATED | NOT_APPLICABLE | NOT_RUN | NOT_ISSUED`. Nonfabrication is mandatory but is not itself a PASS receipt. `PASS_BY_NONFABRICATION` and `PASS_FAIL_CLOSED_DIFFERENTIATION` are forbidden. Technical-gate difficulty metadata is not an SDU receipt; SDU is issued only for an instantiated governed Core1A/Core1B unit.

## Executable stress tests

A seven-core stress test is a governed compiler execution, not a narrative declaration. The request contains no `final_verdict`. The compiler derives scoped routing, engineering closure, external-domain closure, JOIN state, all seven Core states, downstream gates, architecture violations and the final verdict.

`STRESS_TEST_PASS` means the architecture behaved according to contract, including correct fail-closed holds. It does not mean every learner product is released.

## Normative V10 files

- `SELF_HELP_ARCHITECTURE_V10.md`
- `contracts/scoped-execution-envelope.schema.json`
- `contracts/scoped-evidence-receipt.schema.json`
- `contracts/domain-prerequisite-authority.schema.json`
- `contracts/domain-prerequisite-closure.schema.json`
- `contracts/seven-core-stress-test-request.schema.json`
- `contracts/seven-core-stress-test-receipt.schema.json`
- `policy/join-policy.v2.json`
- `policy/stress-test-state-semantics.v1.json`
- `engine/compile_scoped_evidence.py`
- `engine/compile_domain_prerequisite_closure.py`
- `engine/compile_seven_core_stress_test.py`
- `tests/test_blueprint_scope_v10.py`
- `tests/test_blueprint_stress_test_v10.py`

V10 is global. It contains no Q15-, river-, relative-motion-, or PR-specific branch in policy logic. Topic-specific data may appear only in fixtures or governed source artifacts.
