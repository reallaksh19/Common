# Baton readiness and takeover certification

## Purpose

WP-02 separates three different facts that must never be collapsed into one readiness boolean:

1. the repository contains a complete baton for an unknown future replacement;
2. a particular incoming candidate has independently proved takeover on one current execution route;
3. that candidate may write engineering material **right now** in the live checkout.

The first fact is repository-wide. The second is route/candidate-specific. The third is runtime-only because branch, worktree, HEAD and base drift can change after certification.

## Canonical predicates

```text
BATON_READY
=
semantic repository baton is complete for zero-context takeover
```

`BATON_READY` is candidate-independent. A repository can and should become baton-ready before the future replacement exists.

```text
TAKEOVER_CERTIFIED(route, candidate)
=
BATON_READY
AND current DISC receipt for this candidate/route PASS
AND current TC receipt for this candidate/route PASS
AND TC basis matches current roadmap / EP / profile / predecessor / material basis
AND required qualification is satisfied
```

`TAKEOVER_CERTIFIED` is not persisted as one repository-wide boolean. `REPO_STATE.takeover_admissions[]` locates the current route/candidate evidence.

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

Serial work has one route key:

```text
SERIAL:<EP-id>
```

Approved parallel work has one independent route per lane:

```text
PARALLEL_LANE:<PLAN-id>:<LANE-id>:<EP-id>
```

This allows different incoming candidates to be certified for different approved lanes without turning lane admission into repository-wide authority.

## Discovery Receipt (`DISC-*`)

The EP contains forward discovery instructions with `DSTEP-*` IDs. The incoming candidate executes those instructions from repository state and records the result in a `DISC-*` receipt.

A PASS receipt is bound to:

- candidate agent-instance ID;
- exact current route;
- roadmap ID/revision;
- pinned relay-protocol basis;
- material ref;
- canonical semantic EP contract digest;
- canonical `REPO_PROFILE` digest;
- predecessor checkpoint/join/replan identity and digest;
- exact required DSTEP coverage;
- exact expected output names;
- durable basis for every observed output;
- `conversation_context_used: false`.

Changing the EP contract, repository profile, predecessor baton, roadmap revision, route, protocol basis, or material ref therefore invalidates an older receipt mechanically.

## Takeover Certification (`TC-*`)

A TC records:

- candidate identity;
- preparer identity;
- evaluator type/identity/basis;
- `self_certification.allowed: false`;
- exact route and basis;
- exact PASS Discovery Receipt;
- qualification requirement/status;
- takeover checks;
- final PASS/FAIL;
- `conversation_context_used: false`.

The candidate may not be the preparer. An `INDEPENDENT_AGENT` evaluator may not be the candidate. `DETERMINISTIC_VALIDATOR` evaluation is valid only when the repository validator actually re-runs the objective conformance checks; naming a validator in YAML is not itself certification.

## Qualification boundary

WP-02 provides the admission hook but does not weaken the WP-03 gate.

If the incoming EP declares a required phase/material qualification boundary, a TC cannot PASS until a valid `QUAL-*` receipt exists and WP-03 qualification validation is available. This prevents takeover certification from bypassing stronger engineering comprehension proof.

## Baton readiness

`validate_baton_readiness.py` derives baton readiness from repository semantics rather than lifecycle. It validates the roadmap/frontier, repository profile, predecessor custody, state planes, continuity, serial EP semantics or every approved parallel lane EP, report/successor contract, and zero-chat requirement.

`INITIALIZING` is never baton-ready. A valid `IDLE` or `TERMINAL` repository may be baton-ready even though no material route exists, because a successor can still recover the complete terminal/no-work state.

## Candidate admissions in REPO_STATE

`REPO_STATE.takeover_admissions[]` is a locator/projection, not the authority source. Each row names:

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

The validator re-opens the receipt files, re-computes their basis against current repository state, and rejects stale or mismatched admissions.

`INITIALIZING | IDLE | TERMINAL` do not retain active route admissions.

## Runtime write gate

Before engineering writes, the active candidate runs:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/material_write_ready.py \
  <repo-root> --candidate-id <agent-instance-id>
```

For parallel work, live branch/worktree resolution must identify exactly one approved lane. The runtime gate reuses `inspect_git_context.py` and rejects branch mismatch, invalid material ancestry, unqualified base drift, wrong candidate, stale certification, read-only authority, `can_continue: false`, or active hard stop.

If the base moved, a drift receipt may preserve write readiness only when the current receipt validates for WRITE and its `to_base` equals the base currently observed by the live Git inspection. A stale historical drift receipt cannot authorize the current checkout.

## Invalidation matrix

A previously valid DISC/TC becomes invalid when any bound fact changes, including:

```text
roadmap revision
relay protocol basis
execution route / plan / lane
EP identity or semantic contract contents
repository profile contents
predecessor checkpoint/join/replan contents
material ref
required discovery instruction/output contract
qualification requirement/basis
```

Live write readiness additionally disappears when:

```text
checked-out route no longer matches
material ancestry fails
base drift is not qualified for WRITE
material_authority != WRITE
execution.can_continue != true
hard stop becomes active
```

Repository baton readiness and an existing candidate certification do not override these runtime facts.

## Zero-context proof

The WP-02 acceptance regression creates a semantically rich repository baton, then constructs candidate DISC/TC evidence using repository state only. It proves:

- the baton can be ready before any candidate exists;
- a zero-context candidate can later become independently certified;
- self-prepared certification fails;
- contract changes invalidate old certification;
- discovery output coverage must match the EP exactly;
- parallel certification remains lane-scoped;
- the live write gate is candidate-specific and disappears on a hard stop/read-only state;
- required phase qualification cannot be bypassed.

This is the admission foundation. The deeper engineering Q1-Q5 answer/evaluation transaction remains WP-03.
