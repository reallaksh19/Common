# WP-03 — Strong phase / material-boundary qualification

## Outcome

WP-03 replaces metadata-only Q1–Q5 with a durable evaluated engineering admission transaction:

```text
semantic EP
  -> qualification_boundary
  -> QSET-* prepared by outgoing agent
  -> zero-chat candidate answers
  -> independent/deterministic evaluation
  -> QUAL-* PASS/FAIL
  -> TC-* cites exact QUAL id/path/digest
  -> TAKEOVER_CERTIFIED(route,candidate)
```

Qualification is required on `PHASE_CHANGED` or `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`.

## Delivered objects

- `templates/QUESTION_SET.yaml`
- `schemas/question-set.schema.yaml`
- `scripts/validate_question_set.py`
- `templates/QUALIFICATION_RECEIPT.yaml`
- `schemas/qualification-receipt.schema.yaml`
- `scripts/validate_qualification_receipt.py`

The existing EP and TC contracts were extended rather than creating a separate authority plane.

## Strong Q1-Q5 contract

Q1 requires an actual incoming production/source trace and structured outputs for production entrypoint, state owner, authority source and downstream consumer.

Q2 requires an explicit reconstruction mode. Quantitative work must carry concrete payload values; all modes require reconstruction steps, intermediate result and expected result.

Q3 carries the mutation condition, protected invariant and exact falsifier rather than only asking the candidate to describe boundaries.

Q4 references incoming benchmark/oracle IDs and requires an independent method, predicted result and tolerance/exactness.

Q5 references actual incoming implementation steps and requires the first bounded change, predicted before/after observations and exact verification.

Every question is bound to current incoming-EP IDs and the exact route/EP digest.

## Route and staleness binding

QSET and QUAL both bind to the full execution route tuple:

```text
route_key
mode
execution_ref
EP id/path
plan id/path
lane id
roadmap revision
work package
EP contract digest
```

This keeps qualification lane-specific under approved parallel execution.

A changed EP contract invalidates the QSET/QUAL basis. A changed QUAL receipt after TC issuance invalidates TC through `qualification.receipt_digest`.

## Independence

The candidate may not prepare its own QSET. `self_evaluation.allowed` is false. An `INDEPENDENT_AGENT` evaluator may not be the candidate.

A deterministic evaluator is accepted only when the QSET contains exact `deterministic_expected` mappings for all five questions and candidate outputs match exactly. Naming a validator does not itself create evaluation authority.

QUAL PASS requires every Q1–Q5 evaluation PASS with durable basis.

## Baton and takeover integration

`validate_baton_readiness.py` now includes strong QSET validation. An outgoing baton cannot claim `BATON_READY` when qualification is required but the actual QSET is missing, stale or weak.

`validate_takeover_certification.py` now requires current QUAL PASS, exact receipt ID/path and exact digest on qualification-required routes. Qualification is therefore an admission dependency, not a report field.

Qualification itself does not grant WRITE. The final runtime gate remains `material_write_ready.py`.

## Legacy retirement

Inline `phase_transition.questions` is retired. `validate_phase_transition_questions.py` remains only as a compatibility entrypoint that rejects the old inline contract and delegates to strong question-set validation.

## Synthetic acceptance

`tests/stress/test_qualification.py` proves:

1. a phase-change QSET/QUAL can produce a current TC;
2. a materially changed technical boundary inside the same phase requires and accepts fresh qualification;
3. quantitative Q2 without concrete values fails;
4. Q3 without an exact falsifier fails;
5. candidate-authored QSET fails;
6. missing required structured answer output fails;
7. candidate acting as independent evaluator fails;
8. QUAL mutation after TC issuance invalidates TC digest.

Legacy stress fixtures were migrated to assert retirement of inline phase questions and the new `qualification_boundary` admission hook.

## Validation evidence

Pre-checkpoint documentation-aligned head:

```text
3e32dcc562651db019a0ff4e9cf48e4099ab43bd
```

Workflow:

```text
35098797964
```

Result:

```text
compile                         PASS
root unit tests                 PASS
dedicated synthetic stress     PASS
```

The stress suite currently discovers 99 repository-neutral stress tests.

## Not delivered here

WP-03 does not redesign Owner progress/handover rendering, GitHub operation orchestration, quality procedures, Owner-language translation or release readiness. Those remain later serial work packages.
