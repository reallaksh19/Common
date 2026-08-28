# Owner-Governed Engineering Roadmaps

## Purpose

An owner roadmap is the durable strategic direction for one engineering domain or product workstream. It is read by agents before coding, but it is **not** ordinary agent-maintained status documentation.

Use roadmaps for long-horizon direction such as:

- major concepts and architecture;
- phased capability sequencing;
- benchmark and qualification programs;
- source/method authority milestones;
- planned additions and exclusions;
- dependency ordering;
- acceptance/exit criteria;
- deliberate deprecations and migrations.

Typical names may include:

```text
docs/roadmaps/Overallroadmap_wrc.md
docs/roadmaps/Overallroadmap_lafea.md
docs/roadmaps/Overallroadmap_loadcalc.md
```

Existing repository-specific names such as `docs/OWNER_ROADMAP.md` are also valid if registered or explicitly bound to the chain.

## Authority model

Every owner roadmap declares:

```text
ROADMAP_AUTHORITY: OWNER_CONTROLLED
ROADMAP_WRITE_POLICY: EXPLICIT_OWNER_AUTHORIZATION_REQUIRED
```

Agents may read, analyze, challenge, and propose changes. They may **not** mutate an owner roadmap merely because:

- the current implementation differs from the roadmap;
- a better architecture is discovered;
- a benchmark should be added or replaced;
- AUTO MODE is active;
- the agent owns the implementation chain;
- the PR is merge-authorized;
- a prior roadmap update was authorized;
- a roadmap proposal exists.

Roadmap write authority is a separate permission. It must be explicit for the roadmap mutation being made.

## Intent versus observed status

Roadmaps must distinguish two kinds of content.

### Owner intent

Examples:

- target architecture;
- phase order;
- required benchmark families;
- strategic scope and exclusions;
- planned authority boundaries;
- acceptance criteria.

Owner intent remains authoritative until the Owner changes it.

### Observed status

Examples:

- phase complete/partial/not started;
- benchmark count;
- current PR/issue mapping;
- implementation already exists;
- current blocker.

Observed status can become stale as the repository changes. Agents must re-ground it against live source, tests, PRs, and evidence before relying on it.

If observed status is stale, do **not** silently refresh the roadmap. Create a `STATUS_REFRESH` proposal and continue from live repository truth within the current authorized scope.

An owner roadmap can therefore be strategically authoritative while some descriptive status rows are stale.

## Roadmap registry

Recommended routing file:

```text
docs/roadmaps/ROADMAP_REGISTRY.md
```

The registry is also owner-controlled. It maps engineering domains to roadmap files and applicable path/authority domains.

Example:

```text
| Roadmap ID | Domain | Path | Applies to | State |
|---|---|---|---|---|
| WRC-OVERALL | WRC / EMP.1 | docs/roadmaps/Overallroadmap_wrc.md | src/core/emp1/**; validation/emp1/** | ACTIVE |
| LAFEA-OVERALL | LAFEA | docs/roadmaps/Overallroadmap_lafea.md | src/core/lafea/**; validation/lafea/** | ACTIVE |
| LOADCALC-OVERALL | LoadCalc | docs/roadmaps/Overallroadmap_loadcalc.md | src/core/loadcalc/** | ACTIVE |
```

Before coding, the agent must read the registry if present and determine every applicable roadmap. No roadmap match may be silently treated as `NONE`; record the discovery basis.

## Mandatory pre-coding roadmap gate

Before the first material coding action of a new chain/leg:

1. read repository `AGENTS.md`;
2. read `docs/roadmaps/ROADMAP_REGISTRY.md` when present;
3. identify every roadmap applicable to the issue, authority domain, expected changed paths, benchmarks, or dependent subsystem;
4. read the full applicable roadmap(s);
5. re-ground roadmap observed-status claims against live repository evidence when they affect the planned change;
6. record the exact roadmap path and Git blob SHA in chain state and the next endpoint;
7. classify consistency:

```text
ALIGNED
ROADMAP_STATUS_STALE_BUT_SCOPE_ALIGNED
OWNER_DECISION_REQUIRED
NO_APPLICABLE_ROADMAP
```

8. do not start material coding when the planned implementation contradicts owner intent or requires an unapproved roadmap change.

`NO_APPLICABLE_ROADMAP` is valid only when the discovery basis is explicit.

## Chain binding

Canonical `ACTIVE.md` version 2 adds:

```text
ROADMAPS: <path>@<git-blob-sha>[; <path>@<git-blob-sha> ...]
ROADMAP_REVIEW_STATUS: COMPLETE | NOT_APPLICABLE | BLOCKED
```

Examples:

```text
ROADMAPS: docs/roadmaps/Overallroadmap_wrc.md@0123456789abcdef0123456789abcdef01234567
ROADMAP_REVIEW_STATUS: COMPLETE
```

or:

```text
ROADMAPS: NONE — policy-only Common skill change; no product/domain roadmap applies
ROADMAP_REVIEW_STATUS: NOT_APPLICABLE
```

The active endpoint records the same fields and contains an `Owner roadmaps` inventory explaining:

- roadmap ID/path;
- exact blob basis;
- applicable owner intent;
- observed-status claims re-grounded for this leg;
- any stale status discovered;
- alignment classification;
- any proposal created.

A roadmap blob change invalidates the old binding. Before further material coding, the chain must re-read the new roadmap version and create/advance durable state.

## Roadmap proposals

Agents propose strategic changes in chain-local immutable artifacts:

```text
agents/chains/<CHAIN_ID>/roadmap-proposals/<PROPOSAL_ID>.md
```

Proposal IDs are chain-local, for example `RP-0001`.

Allowed proposal types include:

```text
CONCEPT_CHANGE
SCOPE_ADDITION
SCOPE_REDUCTION
BENCHMARK_ADDITION
BENCHMARK_REPLACEMENT
PHASE_REORDER
AUTHORITY_BOUNDARY_CHANGE
DEPENDENCY_CHANGE
STATUS_REFRESH
DEPRECATION
MIGRATION
```

A proposal must state evidence, expected value, impact, alternatives, risks, validation implications, affected roadmap sections, and whether current coding can safely continue without the proposal.

A proposal is **advisory only**:

```text
PROPOSAL_STATUS: PROPOSED
ROADMAP_WRITE_AUTHORITY: NONE
```

Creating a proposal does not make the proposed direction part of the roadmap.

## Owner decision receipts

When the Owner explicitly approves or rejects a roadmap proposal/change, preserve the decision separately:

```text
agents/chains/<CHAIN_ID>/roadmap-decisions/<DECISION_ID>.md
```

The receipt records:

```text
DECISION_ID:
ROADMAP_PATH:
ROADMAP_BASIS_BLOB:
PROPOSAL_REF: <path or NONE>
OWNER_DECISION: APPROVED | REJECTED | MODIFIED
AUTHORIZED_ROADMAP_MUTATION: YES | NO
AUTHORIZED_CHANGE_BOUNDARY:
AUTHORIZATION_SOURCE:
RECORDED_AT:
RECORDED_BY:
```

Do not infer approval from silence, merge authorization, AUTO MODE, or general permission to continue coding.

## Roadmap mutation leg

When `AUTHORIZED_ROADMAP_MUTATION: YES` exists:

1. re-read the current roadmap blob;
2. confirm the authorization applies to that exact roadmap and change boundary;
3. reconcile any intervening roadmap change;
4. update only the authorized roadmap content;
5. increment `ROADMAP_REVISION`;
6. update `LAST_OWNER_DECISION_REF` and the roadmap change log;
7. update the registry only if separately included in the authorization boundary;
8. re-bind affected active chains before their next material coding action.

Roadmap mutation should normally be its own leg or PR. Combining roadmap mutation with production implementation requires explicit Owner authorization for the combined scope.

## Relationship to engineering authority

A roadmap is planning and product-direction authority. It does not replace:

- governing codes/standards;
- source custody;
- physical applicability rules;
- independent engineering benchmarks;
- numerical oracles;
- software tests;
- live repository truth.

A roadmap cannot make an invalid equation valid, turn `NOT_RUN` into `PASS`, or authorize unsupported source extrapolation.

If roadmap intent conflicts with an authoritative engineering source, stop and surface the conflict for Owner resolution.

## Multi-agent behavior

WRC, LAFEA, LoadCalc, and other chains may read the same overall roadmap without relay conflict because reading creates no mutation.

Agents do not update roadmap status after every PR. Instead they may create proposals when major evidence warrants a strategic update.

This prevents a shared roadmap from becoming another high-contention agent-maintained status file.

## What should trigger a proposal

Agents should consider a roadmap proposal when they discover:

- a major concept or architecture change;
- a new benchmark family or independent validation source;
- a benchmark that is invalid, weak, or no longer representative;
- a missing phase or capability;
- a dependency/order change;
- an important new source-authority gate;
- a strategic exclusion that should be made explicit;
- repeated production evidence that makes roadmap status materially stale;
- a planned phase that is no longer the smallest safe next step.

Do not create roadmap proposals for trivial refactors, ordinary bug fixes, formatting, or routine endpoint/status updates.
