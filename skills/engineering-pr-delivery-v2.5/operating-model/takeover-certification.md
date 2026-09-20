# Baton readiness and takeover certification

## Purpose

The relay separates three different facts:

1. the repository contains a complete baton for an unknown future replacement;
2. a particular execution candidate has repository-grounded admission evidence on one current execution route;
3. that candidate may write engineering material **right now** in the live checkout.

The execution candidate may be a new successor or the same custodian continuing after preparing/reconciling the EP. EP authorship does not by itself disqualify that candidate.

The first fact is repository-wide. The second is route/candidate-specific. The third is runtime-only because branch, worktree, HEAD and base drift can change after certification.

## Canonical predicates

```text
BATON_READY
=
semantic repository baton is complete for zero-context takeover
```

`BATON_READY` is candidate-independent. If the incoming EP requires qualification, its `QSET-*` must already exist and be valid before the baton is ready.

```text
TAKEOVER_CERTIFIED(route, candidate)
=
BATON_READY
AND current DISC receipt for this candidate/route PASS
AND current TC receipt for this candidate/route PASS
AND TC basis matches current roadmap / EP / profile / predecessor / material basis
AND current QUAL receipt PASS when the EP requires qualification
```

`TAKEOVER_CERTIFIED` is not persisted as one repository-wide boolean. `REPO_STATE.takeover_admissions[]` locates route/candidate evidence.

```text
PROJECTION_READY
=
required external projections represent current repository truth

HANDOVER_READY
=
BATON_READY AND PROJECTION_READY
```

```text
MATERIAL_WRITE_READY(route, candidate, live_git)
=
TAKEOVER_CERTIFIED(route, candidate)
AND live route resolves exactly this route
AND live Git/material basis is acceptable
AND current drift/continuity permits WRITE
AND material_authority == WRITE
AND execution can continue
AND no hard stop is active
```

`MATERIAL_WRITE_READY` is deliberately derived by `material_write_ready.py`; it is not a durable boolean in `REPO_STATE.yaml`.

## Route scope

Serial work:

```text
SERIAL:<EP-id>
```

Approved parallel lane:

```text
PARALLEL_LANE:<PLAN-id>:<LANE-id>:<EP-id>
```

DISC, QSET, QUAL and TC all bind to this route granularity. Different parallel lanes may therefore have different certified candidates and independent qualification evidence.

## Discovery Receipt (`DISC-*`)

The EP contains forward `DSTEP-*` discovery instructions. The execution candidate executes them against repository state and records the result in a `DISC-*` receipt.

A PASS receipt is bound to candidate, exact route, roadmap revision, protocol basis, material ref, semantic EP digest, `REPO_PROFILE` digest, predecessor-baton identity/digest, required DSTEP/output coverage and durable observed evidence. `conversation_context_used: false` means the receipt's claims and evidence were reconstructed from repository sources rather than relying on chat as authority; it does not require the candidate to be a different model/session.

## Qualification (`QSET-*` / `QUAL-*`)

When the EP carries `not_applicable_reason: THREE_PASS_COMPLETE`, follow-on QSET/QUAL is not applicable and TC uses qualification `NOT_REQUIRED`. All other takeover checks remain in force.

When `EP.qualification_boundary.required: true`, the outgoing baton contains a durable `QSET-*`. The candidate answers Q1-Q5 from repository state and an independent/deterministic evaluator produces `QUAL-*`.

The strong engineering contract is documented in `phase-transition.md`.

A QUAL receipt is bound to:

- candidate identity;
- exact route and incoming EP digest;
- exact QSET;
- Q1-Q5 structured answer outputs/evidence;
- evaluator identity/basis;
- per-question PASS/FAIL;
- zero chat context.

The candidate cannot prepare its own QSET or serve as its own `INDEPENDENT_AGENT` evaluator.

## Takeover Certification (`TC-*`)

A TC records:

- candidate identity;
- document preparer/assembler identity;
- evaluator type/identity/basis;
- `self_certification.allowed: false`;
- exact route and repository basis;
- exact PASS Discovery Receipt;
- qualification requirement/status;
- exact QUAL id/path/digest when required;
- takeover checks;
- final PASS/FAIL;
- `conversation_context_used: false`.

For a qualification-required EP:

```yaml
qualification:
  required: true
  status: PASS
  receipt_id: QUAL-0001
  receipt_path: agents/relay/certifications/qualification/QUAL-0001.yaml
  receipt_digest: sha256:...
```

For a route that does not require fresh qualification:

```yaml
qualification:
  required: false
  status: NOT_REQUIRED
  receipt_id: null
  receipt_path: null
  receipt_digest: null
```

The TC validator re-opens DISC and QUAL files and re-runs their objective validation. A YAML assertion is not authority.

### TC authorship is not certification authority

`prepared_by` records who assembled the TC document. It is provenance, not the certifier.

The candidate **may** assemble its own TC record, including when the candidate also prepared the current EP. This is not self-certification because:

- `self_certification.allowed` remains `false`;
- an `INDEPENDENT_AGENT` evaluator still cannot be the candidate;
- a `DETERMINISTIC_VALIDATOR` must be the canonical validator identity;
- the validator independently re-opens the current route, EP, DISC and QUAL evidence and recomputes the bound basis.

For a route with `qualification_boundary.required: false`, no extra agent is required merely to author TC: the candidate may execute DSTEP discovery, write DISC + TC, and use deterministic validation.

For a route with fresh qualification, the stronger qualification rules still apply: the candidate cannot author its own QSET, and it cannot act as its own independent evaluator. Deterministic qualification is valid only when the QSET carries exact machine-checkable expectations.

Editing a QUAL receipt after TC issuance changes its digest and invalidates takeover.

## Baton readiness

`validate_baton_readiness.py` derives baton readiness from repository semantics rather than lifecycle. It validates roadmap/frontier, repository profile, predecessor custody, state planes, continuity, serial EP or every approved parallel lane, report/successor contract, zero-chat requirement, and every required `QSET-*`.

`INITIALIZING` is never baton-ready. A valid `IDLE` or `TERMINAL` repository may be baton-ready even though no material route exists because a replacement can recover the complete no-work/terminal state.

## Candidate admissions in REPO_STATE

`REPO_STATE.takeover_admissions[]` is a locator/projection, not authority:

```yaml
route_key: SERIAL:EP-0001
candidate:
  agent_instance_id: agent-B
discovery_receipt:
  id: DISC-0001
  path: agents/relay/certifications/discovery/DISC-0001.yaml
certification:
  id: TC-0001
  path: agents/relay/certifications/takeover/TC-0001.yaml
```

Validators re-open all evidence and recompute current basis. Stale or mismatched admissions fail.

`INITIALIZING | IDLE | TERMINAL` do not retain active route admissions.

## Runtime write gate

Before engineering writes:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/material_write_ready.py \
  <repo-root> --candidate-id <agent-instance-id>
```

For parallel work, live branch/worktree resolution must identify exactly one approved lane. The gate rejects wrong candidate/route, stale DISC/QUAL/TC, branch mismatch, invalid material ancestry, unqualified base drift, READ_ONLY/NONE **route-level** material authority, `can_continue: false`, or an active hard stop.

Candidate admission and route material authority are separate dimensions. A missing candidate admission must not be represented by changing repository-wide `material_authority` to READ_ONLY; `TAKEOVER_CERTIFIED(route,candidate)` already carries that candidate-specific failure.

If the base moved, a drift receipt preserves write readiness only if it validates for WRITE and its `to_base` equals the currently observed base.

## Invalidation matrix

DISC/TC or QUAL/TC becomes invalid when a bound fact changes, including:

```text
roadmap revision
relay protocol basis
execution route / plan / lane
EP identity or semantic contract contents
repository profile contents
predecessor checkpoint/join/replan contents
material ref
required discovery instruction/output contract
qualification boundary
QSET contents
QUAL contents
```

Live write readiness additionally disappears when checkout/route/material ancestry changes, base drift is not qualified for WRITE, material authority is not WRITE, execution cannot continue, or a hard stop activates.

Repository baton readiness and prior candidate evidence never override those runtime facts.

## Zero-context proof

WP-02 proved candidate-independent baton readiness, route/candidate discovery, certification and live write gating. WP-03 extends that proof so a qualification-required candidate must also demonstrate engineering comprehension through QSET/QUAL before TC can pass.
