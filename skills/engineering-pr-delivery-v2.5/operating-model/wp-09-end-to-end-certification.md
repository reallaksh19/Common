# WP-09 — End-to-end Relay Certification Matrix

## Outcome

WP-09 implements the defining V2.5 release proof: an unknown replacement agent can recover the engineering relay from repository state alone, obtain current independent qualification/certification, complete a bounded work package, and leave an equally recoverable successor baton.

This work is repository-neutral and does not adopt V2.5 into any downstream repository.

## Delivered implementation

### Zero-context reconstruction

Added:

- `scripts/zero_context_reconstruction.py`
- `scripts/validate_zero_context_reconstruction.py`
- `schemas/zero-context-reconstruction.schema.yaml`

The reconstruction derives current roadmap/progress/execution/evidence/quality/stop/projection/readiness information and, for every active route, reconstructs:

- roadmap position and why the task exists;
- governing Owner decisions;
- predecessor checkpoint facts/limitations/remaining work;
- current implementation plan;
- input authority/editability/applicability/resolution;
- benchmarks/oracles and independence/tolerance;
- allowed/protected/prohibited scope;
- quality obligations and latest QRV evidence;
- test and acceptance requirements;
- first implementation action;
- stale conditions and exact next work.

Aggregate relay conformance now includes zero-context reconstruction validation.

### Full A → B → C release proof

`tests/stress/test_zero_chat_release_proof.py` creates three dependency-ordered roadmap work packages. Agent A completes WP-1 and publishes CP-A / EP-B / QSET-B. Agent B reconstructs WP-2 from repository state, creates DISC/QUAL/TC with `conversation_context_used: false`, obtains current takeover certification, completes WP-2, and publishes CP-B / EP-C / QSET-C. Agent C reconstructs WP-3 and independently qualifies/certifies from repository state.

The proof checks that Agent C can answer the defining release questions for Owner decisions, predecessor facts, uncertainty, input authority/editability, independent oracle, scope, quality obligations, evidence, tests, acceptance, first action, staleness and next work.

### Strict repository-only boundary

`tests/stress/test_zero_chat_repository_only_boundary.py` closes the final test-harness loophole. It deliberately ignores every in-memory return value from Agent A and Agent B handoff helpers. Candidate B and candidate C reopen the active EP and QSET from disk, derive all current IDs and qualification payload from repository files, and construct their DISC/QUAL/TC evidence without predecessor process memory.

### Lifecycle certification matrix

`tests/stress/test_end_to_end_relay_certification.py` covers zero-context cold start across:

```text
ACTIVE
ACTIVE + RECONCILING
PARALLEL
ACTIVE + required projection STALE
IDLE
TERMINAL
```

Expected semantics are documented in `operating-model/relay-certification-matrix.md`. INITIALIZING remains additionally covered by bootstrap/core stress tests.

## Acceptance evidence

Pre-documentation implementation candidate:

```text
head: 0be78ca507b4eea99327713d63da3528c5df056d
workflow: 35191523488
compile: PASS
root units: 7 PASS
synthetic stress tests: 134 PASS
```

Strict repository-only boundary candidate:

```text
head: 12440cf190fd20a2b81e265ff5d97bb6dc904ed1
workflow: 35191938748
compile: PASS
root units: 7 PASS
synthetic stress tests: 135 PASS
```

## Acceptance criteria

- **AC-09-01 — repository-only reconstruction:** PASS. Active route material context is derived from repository authority objects and fails if chat context is required or required material answers are absent.
- **AC-09-02 — A → B → C continuity:** PASS. The synthetic relay crosses WP-1 → WP-2 → WP-3 with CP-A and CP-B predecessor custody.
- **AC-09-03 — independent incoming qualification:** PASS. Both B and C use repository-only DISC/QUAL/TC evidence with independent evaluator identity and current qualification bindings.
- **AC-09-04 — no process-memory shortcut:** PASS. The strict boundary regression ignores handoff return values and rebuilds candidate evidence from persisted EP/QSET state.
- **AC-09-05 — lifecycle recovery:** PASS. ACTIVE, RECONCILING, PARALLEL, stale projection, IDLE and TERMINAL recover according to their authority semantics.
- **AC-09-06 — no authority inflation:** PASS. RECONCILING remains READ_ONLY; stale required projection keeps projection/handover readiness false; IDLE/TERMINAL expose no material route.
- **AC-09-07 — exact-head whole-suite evidence:** PENDING FINAL CHECKPOINT HEAD. WP-09 is not complete until CP-R010 plus completion-program reconciliation pass compile, root units and dedicated stress discovery on their exact head.

## Deliberately not performed

- no V2 modification;
- no downstream repository writes;
- no PR merge or ready-for-review transition;
- no WP-10 self-consistency audit;
- no WP-11 PR-readiness cleanup.

## Successor

After CP-R010 exact-head verification, the only successor frontier is WP-10 — Self-consistency Audit.
