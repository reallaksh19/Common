# Reality-check P0 — reporting, qualification floor and exclusive work-item custody

This reference remains binding for the failures it originally closed: mandatory Active handover State Card, Owner-question no-downgrade, concrete engineering payload, exact work-item custody and evidence-derived readiness.

Two later references supersede only the affected parts of the original P0 wording:

```text
owner-progression-commands.md
→ supersedes “show full Q1-Q5 after every response”
→ supersedes “fresh Q1-Q5 before every same-scope material batch”

github-issue-control-plane.md
→ adds Issue Basis / cumulative Issue Current State / synchronized Issue comments
```

All other P0 protections remain in force.

## 1. Every repository-work response starts with the Active handover

For any response that performed, attempted, audited, blocked, resumed, advanced, completed or re-grounded repository work, the first user-visible section is:

```text
# Active handover snapshot
```

No narrative prose precedes it.

This applies to all three Owner progression commands, AUTO batches, audits, blockers, NOT_RUN, PR creation/update, review gates, merge gates and task completion.

Full Q1-Q5 display is **command-dependent**, not every-turn. See `owner-progression-commands.md`.

After any command-required questions, ordinary turn prose is limited to:

```text
## Changed this turn
```

with at most eight concise bullets unless the Owner asks for a detailed report.

## 2. State Card and qualification questions are separate

The State Card target remains `<220 words`. It now includes mergeability/check/review state, roadmap state, cumulative issue/task/input/benchmark status and qualification readiness.

Durable endpoints retain the current qualification pack where qualification applies. User-facing display is:

```text
proceed next
→ hide unchanged Qs; show only if refreshed

proceed next, no Qs
→ do not generate/refresh/display Qs

proceed next, hand over ready
→ show full current Q1-Q5
```

Do not shorten Owner numerical inputs, derivations, oracle requirements or falsifiers when questions are shown/refreshed.

## 3. Owner-authored qualification is a floor

Before refreshing a Q1-Q5 pack, inspect current Owner instruction, issue body/appendix, Owner Roadmap(s) and accepted handovers for existing qualification questions or explicit technical challenges.

Record:

```text
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE: NONE | <owner source locator>
OWNER_QUALIFICATION_BASELINE_MANIFEST: NONE | <repo-relative JSON manifest>
OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE | SATISFIED | BLOCKED
```

If Owner-authored questions exist, they are the minimum technical difficulty/coverage floor. A refreshed pack may reorganize or strengthen but may not silently remove:

- supplied numerical values, coordinates, geometry, loads, material data or integration points;
- requested derivations or hand calculations;
- required engineering mechanisms/theory;
- independent-oracle requirements;
- falsifiers, negative cases or safe-patch/NO-PATCH reasoning.

`proceed next, no Qs` does not downgrade the existing pack; it preserves it unchanged and may mark it `STALE` if coverage no longer reaches the new boundary.

## 4. Concrete engineering payload remains mandatory

For `FEA`, `WRC_LOCAL_STRESS`, `LOAD_CALC` and `FIXED_FORMAT_WRITER`, marker names and technical verbs are not sufficient.

New/refreshed profile-v2 packs declare:

```text
QUALIFICATION_PROFILE_VERSION: 2
```

and detailed questions carry:

```text
Concrete payload:
Required derivation:
```

For numerical profiles, at least two questions require a real hand-computable payload. A topic label such as `Reconstruct the distorted T6 Jacobian` is insufficient when coordinates/integration points are known.

## 5. Exact work-item ownership precedes semantic overlap

Every new material state records:

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE | REPOSITORY_TASK | OWNER_DIRECT
WORK_ITEM_KEY:
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
AGENT_INSTANCE_ID: <agent-class>:<UUID>
```

A model family/name is not an agent-instance identity.

For `EXCLUSIVE`, no two non-terminal canonical chains may hold the same key. `PARTITIONED` requires non-overlapping partition identity plus durable Owner authorization. Semantic path/authority/benchmark/release overlap remains an additional gate.

## 6. Readiness is multi-plane evidence

New successor endpoints distinguish:

```text
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE:
CHAIN_HANDOVER_READY: TRUE | FALSE
TAKEOVER_QUALIFICATION_READY: TRUE | FALSE
HANDOVER_READY: TRUE | FALSE
```

`CHAIN_HANDOVER_READY` means task/roadmap/input/benchmark/PR/endpoint custody is recoverable.

`TAKEOVER_QUALIFICATION_READY` means a current Q-set exists for immediate admission/qualification.

Thus `proceed next, no Qs` may validly end:

```text
CHAIN_HANDOVER_READY: TRUE
TAKEOVER_QUALIFICATION_READY: FALSE
HANDOVER_READY: FALSE
```

without losing chain state.

Complete `HANDOVER_READY: TRUE` still requires evidence-backed validation, chain readiness, takeover-qualification readiness and, for Issue work, synchronized Issue projection.

## 7. New-material adoption gate

Before a new material progression:

```text
current Common basis
canonical v3 chain path
work-item source/key/mode
valid UUID-backed agent instance
applicable Owner Roadmap/source/oracle authority
HANDOVER_PROTOCOL_VERSION: 2
Owner-baseline discovery
qualification profile version 2 when qualification applies
pre-work custody endpoint committed before material mutation
one of the exact three Owner progression-command states
GitHub-Issue cumulative/sync gate when WORK_ITEM_SOURCE=GITHUB_ISSUE
```

A fresh Q-pack is required only when the selected command/qualification scope requires it. Historical endpoints remain immutable evidence.