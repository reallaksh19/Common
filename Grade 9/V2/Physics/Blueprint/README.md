# Physics V2 Blueprint — canonical orchestration

`Grade 9/V2/Physics/Blueprint/` is the canonical orchestration root. Role-specific sibling directories are subordinate execution kits. Execution order may vary; **authority order may not**.

## Canonical learner-product architecture — V10

Normative architecture: `SELF_HELP_ARCHITECTURE_V10.md`.

V10 supersedes V9 as the canonical learner-product architecture. V9 remains historical and all V9 custody, differentiation, TTU, calibration and publication guarantees remain in force unless V10 explicitly refines them.

The V10 constitutional correction is:

> Every governed decision must be bound to the same declared execution scope. Verified absence is a first-class reconciled state; unknown evidence is not equivalent to verified absence.

A topic-level route, question corpus or evidence metric may not be silently reused to authorize a narrower subtopic, bucket or case. Narrower execution must first compile a scoped evidence receipt from repository-backed authority.

## Authority topology

```text
ORIGINAL / OBSERVED GROUND TRUTH
        ↓
SCOPED EXECUTION ENVELOPE
(non-authoritative projection of repository evidence)
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
CCU
        ↓
CDAU
        ↓
SDU / LAU
        ↓
CONCEPT_TTU / PROBLEM_TTU
        ↓
CORE1A / CORE1B / CORE2A / CORE2B
        ↓
publication / learner runtime
        ↓
observed learner evidence
        ↓
CAL
```

Product-design layers never manufacture truth, rewrite frozen source wording, create observed learner evidence or expand Core2A legality.

## Scope-consistent routing

Supported execution scopes are:

`TOPIC | SUBTOPIC | BUCKET | CASE`

The existing routing policy remains evidence-adaptive. V10 changes the evidence boundary, not the routing heuristic itself. For narrower scopes, `compile_scoped_evidence.py` binds the target scope to exact repository semantic evidence, assessment coverage, requested curriculum authority and technical gates before Core0 routing.

A topic route and a target route may legitimately differ.

## JOIN v2 — verified absence vs unknown coverage

Assessment coverage states are:

`DEMANDS_PRESENT | VERIFIED_NO_TARGET_DEMAND | COVERAGE_UNKNOWN`

For ordinary demand-bearing JOINs, existing reconciliation behavior remains unchanged.

For a repository-proved zero target-demand set:

```text
VERIFIED_NO_TARGET_DEMAND
        ↓
JOIN_READY_NO_CORE2_DEMAND
assimilation_ready = true
```

This permits source-backed conceptual construction without fabricating a Core2 question. Core2/Core2A remain independently held when no legal target assessment item exists.

`COVERAGE_UNKNOWN` blocks assimilation because absence has not been proved.

## Cross-domain prerequisites

Physics may require external Mathematics or other-domain prerequisites but may not certify them itself. External prerequisites are resolved only through authoritative-domain receipts:

`READY_FROM_AUTHORITATIVE_DOMAIN | HELD_NO_DOMAIN_RECEIPT`

Missing cross-domain authority does not mutate Physics gate readiness; it holds the downstream cross-domain closure.

## Core roles

- **Core0** — routing only; no semantic authority or mastery claim.
- **Core1** — compact orientation.
- **Core1A** — complete conceptual construction and authorizing teaching semantics.
- **Core1B** — concept reconstruction/runtime; no semantic authority.
- **Core2** — frozen assessment grounding and exact source custody.
- **Core2A** — expert problem learning from the governed legal pool.
- **Core2B** — transfer/independent modelling from exact Core2A legality plus released Core1B evidence.

A-layers authorize. B-layers execute. B-layer repair requests may not rewrite A-layer authority.

## State semantics

V10 distinguishes:

`PASS | READY | HELD | BLOCKED | NOT_INSTANTIATED | NOT_APPLICABLE | NOT_RUN | NOT_ISSUED`

Nonfabrication is mandatory but is not itself a PASS receipt. Surrogate labels such as `PASS_BY_NONFABRICATION` and `PASS_FAIL_CLOSED_DIFFERENTIATION` are forbidden.

Technical-gate difficulty metadata is not an SDU receipt. SDU is issued only for an instantiated governed Core1A/Core1B unit.

## Executable seven-core stress tests

A stress test is a compiler execution, not a narrative declaration.

The request contains no `final_verdict`. The compiler derives:

- scope-consistent routing;
- Physics engineering closure;
- cross-domain prerequisite closure;
- JOIN state;
- all seven Core states;
- CCU/CDAU/SDU/LAU/TTU/publication/review states;
- architecture violations;
- final `STRESS_TEST_PASS | STRESS_TEST_FAIL`.

A stress-test PASS may contain HELD or BLOCKED downstream states when repository authority genuinely ends. Correct fail-closed behavior is an architecture success.

## Custody, differentiation and technical interaction

V9 guarantees remain normative beneath V10:

- every canonical asset receives an explicit CCU disposition;
- released learner questions require valid question/source/answer custody;
- CDAU validates Core purpose and neighboring-Core differentiation;
- SDU governs intrinsic authored difficulty for instantiated Core1A/Core1B units;
- LAU requires capability-specific learner evidence or explicit permitted owner routing;
- substantive TTUs require canonical expert state, technical representation, reasoning bindings, learner transformation, bounded help, reveal, independent verification and repair;
- full-solution exposure is support, not mastery or transfer evidence;
- CAL governs only non-deterministic policy maturity and cannot rewrite historical authority.

Historical detail: `SELF_HELP_ARCHITECTURE_V9.md`.

## Release gates

Pre-release:

1. `G-DOMAIN` — source/semantic/curriculum and cross-domain grounding valid for the declared scope;
2. `G-TECHNICAL-ENGINEERING` — applicable technical engineering closure passes;
3. `G-CUSTODY-COVERAGE` — CCU coverage and source/answer/legal custody close;
4. `G-PURPOSE` — learner action belongs in the Core;
5. `G-DIFFERENTIATION` — no accidental neighboring-Core duplication;
6. `G-TTU` — technical interaction is complete;
7. `G-DIFFICULTY` — instantiated authored/task difficulty is evidenced;
8. `G-FIT` — where applicable, learner fit is justified by governed evidence or explicit permitted owner routing;
9. `G-PUBLICATION` — rendered product is legible, integrated and custodied.

Post-use:

10. `G-CALIBRATION` — observed evidence may update future versioned policy confidence; it never creates semantic/source authority retroactively.

## Publication boundary

```text
released governed semantics
        ↓
Publication IR
        ↓
composition-only renderer
        ↓
render custody / preflight
        ↓
governed human review where required
```

Successful PDF generation is not a visual or mature-product PASS. Publication must fail closed on missing upstream manuscript/source authority, microscopic labels, unreadable equations, clipping, collisions, orphaned figures, poor figure-to-working adjacency and missing custody.

## Normative V10 files

- `SELF_HELP_ARCHITECTURE_V10.md`
- `contracts/scoped-execution-envelope.schema.json`
- `contracts/scoped-evidence-receipt.schema.json`
- `contracts/domain-prerequisite-authority.schema.json`
- `contracts/domain-prerequisite-closure.schema.json`
- `contracts/seven-core-stress-test-request.schema.json`
- `contracts/seven-core-stress-test-receipt.schema.json`
- `contracts/join-packet.schema.json`
- `policy/join-policy.v2.json`
- `policy/stress-test-state-semantics.v1.json`
- `engine/compile_scoped_evidence.py`
- `engine/compile_domain_prerequisite_closure.py`
- `engine/compile_seven_core_stress_test.py`
- `engine/compile_join.py`
- `tests/test_blueprint_contract_inventory_v10.py`
- `tests/test_blueprint_scope_v10.py`
- `tests/test_blueprint_stress_test_v10.py`

V2–V9 remain historical transition documents. **V10 is canonical for scope-consistent routing, verified assessment absence, cross-domain prerequisite custody, executable stress testing, learner-product custody, differentiation, adaptation, technical realization and calibration maturity.**

## Real Motion-in-a-Plane publication boundary

Representation readiness may exist while publication remains independently blocked until repository-backed manuscript/source authority exists. Learner-product architecture, runtime activation, owner decisions, technical readiness and visual quality cannot substitute for missing source/manuscript release evidence.
