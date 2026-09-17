# Relay conformance

Question: if the current conversation disappears immediately, can a competent replacement recover the correct roadmap position, locate a semantically complete baton, independently prove takeover, resolve the correct live execution route, and continue safely without hidden chat context or stale evidence?

## Implemented static conformance

PR #396 now validates:

- `REPO_STATE` lifecycle/routing and current roadmap revision;
- `REPO_PROFILE` and pinned relay-protocol basis;
- deterministic executable frontier;
- one serial semantic EP or an Owner-approved parallel router whose lane EPs are semantic;
- typed inputs/oracles, executable discovery contracts, scope/anti-drift/step/report/successor semantics;
- explicit Git execution basis and branch/worktree routing;
- drift and roadmap-continuity reconciliation;
- exact-head checkpoint evidence;
- deterministic progress and roadmap transactions;
- independent execution, quality, evidence and stop state;
- checkpoint/join/replan successor custody;
- issue graph/closure/supersession semantics;
- external projection convergence separately from baton readiness;
- candidate-independent `BATON_READY` derivation;
- route/candidate `DISC-*` and `TC-*` evidence/admissions;
- admission staleness through exact roadmap/material plus EP/profile/predecessor digests;
- no unauthorized parallel material work.

`cold_start_check.py` remains a repository-recovery diagnostic. It is no longer the final candidate admission authority; `TC-*` supplies candidate-specific admission and `material_write_ready.py` supplies the live write gate.

## Readiness predicates

V2.5 deliberately separates repository custody from candidate admission and live write permission.

### Baton readiness

```text
BATON_READY
```

Repository-wide and candidate-independent. It proves the authoritative roadmap/frontier, semantic EP/plan, predecessor custody, profile/protocol, current-slice inputs/oracles, discovery contract, scope/anti-drift, report/successor contract, and zero-chat requirement are complete.

A repository may be baton-ready before any future candidate exists.

### Candidate takeover

```text
TAKEOVER_CERTIFIED(route,candidate)
```

Route/candidate-specific. The incoming candidate must have current PASS discovery/certification evidence on the exact current basis. Serial and parallel-lane routes are independent admissions.

A TC re-runs semantic EP and basis checks. Candidate evidence binds the semantic EP digest, profile digest, predecessor-baton digest, roadmap revision, material ref and route so in-place contract mutation invalidates the old certification.

Self-certification is prohibited. The candidate may not prepare its own certification criteria. Objective facts may be deterministically evaluated; engineering comprehension that needs independent evaluation is completed by the WP-03 `QUAL-*` transaction.

If the EP declares a required phase/material qualification boundary, WP-02 rejects TC PASS until valid qualification exists. Takeover Certification does not bypass Q1-Q5.

### Projection readiness

```text
PROJECTION_READY
```

External GitHub/coordination projection is current independently of engineering repository truth.

### Handover readiness

```text
HANDOVER_READY = BATON_READY AND PROJECTION_READY
```

This is outgoing custody completeness, not candidate write permission.

### Material write readiness

```text
MATERIAL_WRITE_READY(route,candidate,live_git) =
    TAKEOVER_CERTIFIED(route,candidate)
AND live route valid
AND live Git/material basis acceptable
AND current drift/continuity permits WRITE
AND material_authority == WRITE
AND execution.can_continue == true
AND no active hard stop
```

This predicate is deliberately runtime-derived and not stored in `REPO_STATE`. An `ACTIVE` lifecycle or persisted `material_authority: WRITE` is never sufficient permission for an uncertified/wrong-route candidate.

## Live checkout boundary

Static repository files cannot prove the operator's current checkout. Before material writes, run route/Git inspection and `material_write_ready.py --candidate-id ...` against the live repository.

For moved base state, a drift receipt is accepted for the live write gate only if it validates for WRITE and its `to_base` equals the base currently observed by Git. Historical drift classification does not authorize a newer base.

## Reports and generated views

Reports, Owner status, technical status and handover Markdown are projections of authority objects. They do not become competing sources of truth. If a generated report disagrees with roadmap/EP/certification/checkpoint/progress/issue sources, the projection is stale or invalid.

## Current completion boundary

WP-02 establishes zero-context repository takeover/admission. WP-03 still has to implement the stronger `QUESTION_SET -> candidate answers -> independent evaluation -> QUAL-*` engineering comprehension transaction.

Later WPs still own complete progress/handover projection, GitHub operating transactions, quality procedures, plain-language Owner communication and the recursive A -> B -> C release test.

## Defining release test

Completion requires Agent A -> Agent B -> Agent C with chat custody deliberately removed between candidates. If Agent C needs prior conversation to reconstruct any material Owner intent, current task, input authority, benchmark/oracle, scope, evidence, quality obligation, next work or staleness condition, V2.5 completion fails.

A green generic suite proves reusable protocol checks executed successfully. It does not prove a particular downstream product, engineering calculation, release, or human UX acceptance.
