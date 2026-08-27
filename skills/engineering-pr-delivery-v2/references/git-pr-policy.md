# Git / PR Policy

## PR role

A PR is a coherent implementation vehicle inside a durable engineering chain.

Do not use PR number as the long-lived mission identity when the work spans multiple PRs.

## Scope

Keep one coherent assignment per PR unless the owner explicitly changes scope.

Every changed file must have an explainable relationship to the current leg.

Do not silently broaden engineering authority or product scope.

## Durable endpoints

Before intentional stop, PR transition, or merge request, ensure the latest chain endpoint describes the current material state and next work.

If the PR merges but the chain remains technically incomplete, create/preserve a `READY_FOR_NEXT_LEG` endpoint with Q1-Q5.

## Successor PR

For follow-on work:

```text
same CHAIN_ID
new LEG_ID
new PR
PREVIOUS_ENDPOINT = prior chain endpoint
```

Record predecessor/successor relationship and inherited known-good evidence.

## Commits

Prefer logical, recoverable commits. Avoid mixing unrelated authority changes, expected-value changes, and production fixes when they can be isolated.

## Workflow/security/destructive changes

Do not create or modify CI workflows, credentials, permissions, security-sensitive infrastructure, or destructive operations unless explicitly authorized.

## Merge

Merge authority is separate from implementation authority and separate from AUTO MODE.

Do not merge unless owner instructions authorize it.

## Base drift

Before merge or new engineering leg, compare the chain/PR against current base/main. Material drift that changes the unresolved problem, benchmark/source authority, or implementation boundary requires endpoint reconciliation and potentially requalification.
