# Repository Agent Policy — shared engineering-pr-delivery-v2 rules

This is the reusable cross-repository policy for `engineering-pr-delivery-v2`. Repository-root `AGENTS.md` files are **project overlays**, not copies of this protocol.

For new material legs, `reality-check-p0.md`, `github-issue-control-plane.md`, and `owner-progression-commands.md` are binding amendments. Where older wording conflicts, the newer specific amendment wins.

## 1. Policy layering

```text
explicit current Owner instruction
→ applicable Owner Roadmap(s)
→ repository project overlay (`AGENTS.md`)
→ this shared repository-agent policy + binding amendments
→ engineering-pr-delivery-v2 `SKILL.md` + other references
```

A project overlay may be stricter for its domain. It may not silently weaken qualification, source/oracle custody, validation truth, Owner-roadmap authority, chain/custody controls, work-item exclusivity, anti-gaming rules or merge authority.

Downstream `AGENTS.md` should contain only project identity/criticality, repository-specific roadmaps/sources, protected solver/method/data/publication domains, local validation commands/benchmarks, project-specific AUTO hard stops and stricter workflow/release restrictions. Do not duplicate generic relay/qualification/progression semantics.

## 2. Work-item source

Every new material leg declares one source:

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE | REPOSITORY_TASK | OWNER_DIRECT
```

For `GITHUB_ISSUE`, use the durable Issue control plane in `github-issue-control-plane.md`.

For `REPOSITORY_TASK` and `OWNER_DIRECT`, repository custody under `agents/chains/**` remains sufficient. Do not create fake Issue comments or Issue Basis artifacts.

## 3. Protocol-adoption gate

Before material coding, source-governance mutation, benchmark/oracle mutation, engineering-result publication work or AUTO progression into another material boundary, re-ground live Common and record:

```text
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <live Common commit actually read>
COMMON_PROTOCOL_STATUS: CURRENT | STALE_PROTOCOL | UNKNOWN
CHAIN_STATE_VERSION: 3
```

An inherited endpoint pin is history, not permission to keep using an old Common basis.

Fail closed:

```text
STALE_PROTOCOL | UNKNOWN
→ NO_MATERIAL_CODING
→ NO_AUTO_PROGRESSION
→ READ_ONLY protocol reconciliation
```

Also resolve current work-item custody, applicable Owner Roadmap(s), source/oracle authority, current PR/main drift and Owner qualification baseline.

## 4. Canonical repository custody

For every new chain, takeover migration or new material leg:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
agents/qualifications/<CHAIN_ID>/**
```

Legacy `agents/agentchain*`, PR workreports, status and claims files remain READ/CITE/RECOVER/MIGRATION-PROVENANCE only.

For issue-based work, repository custody remains authoritative while synchronized GitHub Issue comments provide the human-visible control plane.

## 5. Exact work-item custody

Every new material leg records:

```text
WORK_ITEM_KEY:
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
AGENT_INSTANCE_ID: <agent-class>:<UUID>
```

For GitHub issues use:

```text
WORK_ITEM_KEY: github:<owner>/<repo>#<issue-number>
```

A model family/name is not a unique agent instance. For `EXCLUSIVE`, a second non-terminal chain with the same work-item key is blocked before semantic overlap is considered. It joins/takes over the existing chain or stops.

`PARTITIONED` requires distinct partition identity and `WORK_ITEM_PARTITION_AUTHORITY: OWNER:<locator>`.

## 6. Owner Roadmap authority

Owner Roadmap(s) remain above the Issue Basis and issue execution plan.

Classify roadmaps:

```text
OWNER_ROADMAP
PROJECT_ROADMAP
ISSUE_EXECUTION_PLAN
ROADMAP_PROPOSAL
```

Pin applicable Owner/Project roadmap revisions/blobs where possible. The Active Handover must show current roadmap alignment/drift and mutation authority.

Issue assignment does not authorize roadmap mutation. Agent plans/proposals remain non-authoritative until Owner-authorized.

Roadmap drift classes for issue-based work are defined in `github-issue-control-plane.md`.

## 7. Issue-based durable control plane

For `WORK_ITEM_SOURCE: GITHUB_ISSUE`, create an immutable Issue Basis preserving:

```text
original task / acceptance rows
input rows
benchmark/oracle rows
roadmap rows
Owner qualification baseline
```

Then maintain exactly three Issue comment roles:

```text
1. immutable CHAIN_ROOT comment — once
2. one mutable ACTIVE HANDOVER comment — current state
3. immutable ENDPOINT checkpoint comment — one per accepted endpoint
```

The four cumulative ledgers—task, inputs, benchmarks/oracles, roadmaps—must never disappear across agents. Aggregate counts are navigation only; item-level custody remains durable.

Repository↔Issue synchronization must be `IN_SYNC` before another material progression begins. Preserve repository custody and report `STALE | NOT_RUN | FAILED` if comment synchronization did not actually occur.

Read `github-issue-control-plane.md`.

## 8. Exactly three Owner progression commands

Normal bounded progression recognizes exactly:

```text
proceed next
proceed next, no Qs
proceed next, hand over ready
```

No fourth progression mode or synonym is introduced by policy.

### `proceed next`

Continue one bounded progression. Reuse the current Q-set while its qualification scope remains valid. Refresh only if the scope materially changed or the set is stale. Hide unchanged questions; show them only when refreshed.

### `proceed next, no Qs`

Continue one bounded progression without creating, refreshing or displaying questions. If existing coverage becomes stale, preserve chain custody but set takeover-qualification readiness FALSE. This is one bounded progression only and does not authorize indefinite uncovered AUTO work.

### `proceed next, hand over ready`

Continue one bounded progression, then freeze a complete takeover-ready checkpoint. Ensure current Q1-Q5, show them in full, reconcile cumulative task/input/benchmark/roadmap/PR state, synchronize Issue comments when applicable, and stop at the checkpoint.

Read `owner-progression-commands.md`.

## 9. Qualification is scope-bound, not endpoint-bound

Questions are bound to:

```text
QUALIFICATION_SCOPE_ID:
QUESTION_SET_ID:
```

A current pack may be reused across multiple endpoints/material batches while work-item, Owner-roadmap intent, engineering authority, source/oracle authority and technical competency remain within its coverage.

A same-agent endpoint does not require a new Q-set merely because an endpoint or commit was created.

A replacement agent still requires current takeover qualification before write custody.

## 10. Owner no-downgrade floor

Before refreshing questions, inspect Owner instructions, issue appendix/questions, Owner Roadmaps and accepted handovers for Owner-authored technical questions/challenges.

The active pack may reorganize/strengthen them but may not remove supplied values, geometry, loads, materials, integration points, required derivations, mechanisms, oracles, falsifiers or negative controls.

Use `owner-qualification-baseline.md` and profile-v2 concrete payload fields.

## 11. Engineering evidence expectations

Where relevant distinguish source/input authority → geometry/topology → stiffness/load assembly → solver equilibrium → local recovery → transformation/load transport → result contract → presentation/publication.

For structural/FEA discrepancies use as applicable equilibrium/residual checks, free-body cuts, method equations, DOF ordering, local/global axes, load/moment transport and an independent oracle. Do not change several mechanics when a single-factor falsifier can isolate the first wrong boundary.

## 12. Takeover qualification and recovery

On agent loss/custody change:

```text
minimal READ_ONLY locator bootstrap
→ locate current ACTIVE / Issue control plane if applicable
→ require TAKEOVER_QUALIFICATION_READY: TRUE
→ question-set admission
→ TAKEOVER QUALIFICATION FIRST
→ independent PASS_QUALIFIED_READ_ONLY
→ post-basis reconciliation while READ_ONLY
→ drift classification
→ retain / independently confirm / requalify
→ WRITE_ALLOWED only when current-state authority is safe
```

If takeover qualification readiness is FALSE, the replacement remains READ_ONLY until an independent question authority/Owner establishes a current pack.

## 13. Validation integrity

Every material check distinguishes:

```text
STATUS      = PASS | FAIL | NOT_RUN | NOT_APPLICABLE
OBSERVATION = execution | source inspection | artifact inspection | inference
ORACLE      = implementation-coupled | independent reproduction |
              analytical | authoritative reference | cross-solver | experimental
```

Never promote source inspection, mergeability, compilation not run, empty workflow jobs or transport failure into engineering PASS.

## 14. Handover readiness planes

Use:

```text
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE: <durable evidence or NONE>
CHAIN_HANDOVER_READY: TRUE | FALSE
TAKEOVER_QUALIFICATION_READY: TRUE | FALSE
HANDOVER_READY: TRUE | FALSE
```

`CHAIN_HANDOVER_READY` means task/roadmap/input/benchmark/PR/endpoint custody is recoverable.

`TAKEOVER_QUALIFICATION_READY` means a valid current Q-set exists for immediate admission/qualification.

For new states, complete handover readiness requires both. Thus `proceed next, no Qs` may legitimately leave:

```text
CHAIN_HANDOVER_READY: TRUE
TAKEOVER_QUALIFICATION_READY: FALSE
HANDOVER_READY: FALSE
```

without losing engineering chain custody.

## 15. User-visible response contract

Every bounded repository-work response starts with:

```text
# Active handover snapshot
```

No narrative prose precedes it.

Always show in the State Card:

```text
repo/task/chain/endpoint
PR / PR status / branch / head / main
mergeability / reviews / unresolved threads / required checks
merge authority / merge authorized
engineering/custody/qualification/write/AUTO
protocol/work item/Issue Basis
Owner + other roadmap state
original-task/input/benchmark status
qualification scope/set/action/readiness
blocker / leg diagnosis / exact next action
```

Full Q1-Q5 display depends on the three Owner progression commands, not on every response. See `handover-snapshot.md` and `owner-progression-commands.md`.

After any command-required questions, ordinary reporting is `## Changed this turn` with at most eight concise bullets unless the Owner requests detail.

## 16. Scope, AUTO and merge

One coherent assignment per PR unless Owner changes scope. AUTO progresses only within approved authority. It does not authorize scope expansion, authority changes, benchmark/oracle changes, roadmap mutation, validation weakening, destructive operations or merge.

Always distinguish:

```text
MERGEABILITY: MERGEABLE | CONFLICTING | UNKNOWN
MERGE_AUTHORITY: OWNER_ONLY | AUTHORIZED
MERGE_AUTHORIZED: TRUE | FALSE
```

Merge authority remains Owner-controlled unless explicitly granted.

## 17. Completion

Distinguish `AGENT_LEG_COMPLETE`, `PR_COMPLETE`, and `CHAIN_COMPLETE`. PR merge alone does not imply chain completion.