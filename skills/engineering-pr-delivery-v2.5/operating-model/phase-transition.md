# Phase transitions and material qualification boundaries

Qualification is engineering admission evidence, not question metadata.

Fresh qualification is mandatory when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

Same-phase work may reuse existing qualification only while the relevant production path, engineering authority, numerical method, protected invariant, input authority and verification/oracle boundary remain materially unchanged.

A routine refactor or cosmetic change does not mechanically retrigger qualification.

## Durable transaction

```text
outgoing agent prepares semantic EP
        |
        +--> qualification_boundary.required = true
        +--> QSET-* Question Set
        |
        v
BATON_READY
        |
        v
incoming candidate, zero chat context
        |
        +--> Q1-Q5 structured answers + durable evidence
        |
        v
independent / deterministic evaluation
        |
        v
QUAL-* Qualification Receipt
        |
        v
TC-* cites QUAL id/path/digest
        |
        v
TAKEOVER_CERTIFIED
```

Inline `phase_transition.questions` is retired. A required qualification boundary references a durable `QSET-*` object.

## EP qualification boundary

```yaml
qualification_boundary:
  required: true
  trigger: PHASE_CHANGED | MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
  from_phase: PHASE-001
  to_phase: PHASE-002
  changed_dimensions:
    - PRODUCTION_PATH
    - VERIFICATION_ORACLE
  basis:
    - "<durable engineering reason>"
  question_set:
    id: QSET-0021
    path: agents/relay/certifications/qualification/QSET-0021.yaml
```

For `PHASE_CHANGED`, `from_phase != to_phase` and `to_phase` is the incoming EP phase.

For `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`, `from_phase == to_phase`; the boundary changed materially inside the same nominal phase.

Allowed changed dimensions are:

```text
PRODUCTION_PATH
ENGINEERING_AUTHORITY
NUMERICAL_METHOD
PROTECTED_INVARIANT
INPUT_AUTHORITY
VERIFICATION_ORACLE
```

## QSET route binding

A Question Set is bound to the same route granularity as takeover certification:

```text
route_key
mode
execution_ref
EP id/path
plan id/path when parallel
lane id when parallel
roadmap revision
work package
EP contract digest
```

This prevents a question pack prepared for one lane or one version of an EP from qualifying another route.

## Q1-Q5 semantic contract

### Q1 — Production path

Must require an actual current trace and structured outputs including:

```text
production_entrypoint
state_owner
authority_source
downstream_consumer
```

The question must anchor to incoming WP/input/path authority rather than historical work.

### Q2 — Engineering reconstruction

Uses one explicit mode:

```text
QUANTITATIVE
LOGIC_RECONSTRUCTION
DESIGN_REASONING
```

The Question Set carries a durable payload source. `QUANTITATIVE` requires concrete `payload.values`, including units where relevant. Required outputs include reconstruction steps, an intermediate result and expected result.

A generic “explain the problem” prompt is insufficient.

### Q3 — Boundaries, mutation and falsifier

The Question Set defines:

```text
mutation condition
protected invariant
exact falsifier
```

The candidate must state the mutation effect, invariant and observation that would prove its understanding wrong.

### Q4 — Independent verification

Must reference one or more incoming benchmark/oracle IDs, state why the verification is independent of the production implementation, and require predicted result plus tolerance/exactness.

### Q5 — First safe slice

Must reference actual incoming `STEP-*` IDs and require:

```text
first exact change
predicted before observation
predicted after observation
exact verification
```

## QUAL-* receipt

A Qualification Receipt records:

- candidate identity;
- exact current QSET and route;
- Q1-Q5 responses;
- structured required outputs;
- durable evidence for each answer;
- evaluator type, identity and durable basis;
- one PASS/FAIL evaluation for each question;
- `self_evaluation.allowed: false`;
- final PASS/FAIL;
- `conversation_context_used: false`.

An `INDEPENDENT_AGENT` evaluator cannot be the candidate. The candidate cannot prepare its own QSET.

`DETERMINISTIC_VALIDATOR` evaluation is only valid when every QSET question provides an exact `deterministic_expected` output mapping and the candidate answer matches it. Merely naming a validator is not evaluation authority.

A QUAL result can be PASS only when all five per-question evaluations PASS.

## Takeover integration

For an EP with `qualification_boundary.required: true`, TC must contain:

```yaml
qualification:
  required: true
  status: PASS
  receipt_id: QUAL-0021
  receipt_path: agents/relay/certifications/qualification/QUAL-0021.yaml
  receipt_digest: sha256:...
```

The TC validator re-opens the QUAL receipt, re-runs its validation against the current route/QSET/EP, requires PASS, and checks the exact digest. Editing qualification evidence after TC issuance invalidates takeover.

Qualification does not directly grant WRITE. `MATERIAL_WRITE_READY` remains the final live gate.

## Baton-readiness implication

If an EP declares qualification required, the outgoing baton is not ready unless its referenced QSET exists and passes strong validation. The future candidate may be unknown; the exam must already be complete and independent of chat.

## Rejection examples

Reject:

- legacy inline Q1-Q5;
- missing QSET for a required boundary;
- QSET bound to a stale EP digest or wrong route/lane;
- phase-change pack with the same from/to phase;
- material-boundary pack that silently changes phase;
- quantitative Q2 without concrete payload values;
- Q3 without an exact falsifier;
- Q4 without a valid incoming oracle;
- Q5 without an incoming implementation step;
- candidate-authored QSET;
- missing structured answer outputs/evidence;
- candidate acting as independent evaluator;
- QUAL PASS with any Q evaluation not PASS;
- TC pointing to a changed/stale QUAL digest.
