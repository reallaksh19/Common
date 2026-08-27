# Relay Engineering Model

## Purpose

Engineering work is a chain of durable repository endpoints, not a sequence of chat sessions.

The outgoing agent is never required for recovery. The repository owns the baton.

## Repository layout

```text
agents/agentchain.md
agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>.md
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-answer.md
agents/qualifications/<CHAIN_ID>/<QUESTION_SET_ID>-<candidate>-verdict.md
```

`agents/agentchain.md` is intentionally compact. It contains repo-wide traffic state and endpoint locators, not full endpoint bodies.

Detailed endpoint files are immutable after durable creation. This avoids turning one large Markdown file into a multi-agent write hotspot.

## Work identity

```text
REPOSITORY
  -> CHAIN_ID
  -> LEG_ID
  -> ENDPOINT_ID
  -> PR / branch / commits
```

- `CHAIN_ID` persists for the engineering mission even when PRs change.
- `LEG_ID` identifies one coherent contribution segment.
- `ENDPOINT_ID` identifies one immutable durable checkpoint.

## Relay state

Recommended chain states:

```text
ACTIVE
QUALIFICATION_REQUIRED
RECOVERY_REQUIRED
BLOCKED
READY_FOR_NEXT_LEG
COMPLETE
SUPERSEDED
```

A normal flow is:

```text
ACTIVE
  -> endpoint file + index row
  -> QUALIFICATION_REQUIRED for new incoming custody
  -> qualified contribution
  -> endpoint file + index row
  -> ...
```

Abrupt loss is:

```text
ACTIVE
  -> last durable endpoint
  -> agent disappears
  -> RECOVERY_REQUIRED
  -> live re-ground
  -> recovery endpoint
  -> qualification
  -> ACTIVE
```

No `AGENT_A_RELEASES_BATON` event is required.

## Index authority

The index has two different mutation semantics:

```text
ACTIVE CHAINS   mutable current traffic summary
ENDPOINT LOG    append-only endpoint locator history
```

For every non-terminal chain, `ACTIVE CHAINS` must point to that chain's actual latest endpoint and endpoint file.

A terminal chain is removed from `ACTIVE CHAINS` but remains in `ENDPOINT LOG`.

## Endpoint authority

A completed detailed endpoint file is immutable.

If an earlier endpoint contains an error, a later endpoint must record:

```text
SUPERSEDES_ENDPOINT:
SUPERSEDED_ASSERTION:
CORRECTED_STATE:
EVIDENCE:
```

Do not rewrite historical custody claims.

`PREVIOUS_ENDPOINT` is chain-local. It must reference the immediately preceding endpoint for that chain, not merely any earlier repository endpoint.

## Material state

The endpoint binds to a repository material state through `CHECKPOINT_HEAD`.

Material state includes changes to:

- production behavior;
- tests/benchmarks/oracles;
- engineering input data;
- engineering source authority;
- numerical or physical conventions;
- configuration that changes behavior;
- result publication authority;
- engineering methodology.

Relay metadata-only changes do not create a new engineering material state by themselves.

## Crash-safety rule

Work that exists only in an agent's private context, local unpushed workspace, or chat is not durable authority.

The system guarantees recovery only up to the latest persisted endpoint plus later repository commits that can be independently reconciled.

If an endpoint file is created but the index update is interrupted, the endpoint is an orphan durable artifact, not lost work. Recovery must reconcile it and repair the index rather than deleting it silently.

## Separation of completion states

Never collapse these:

```text
AGENT_LEG_COMPLETE
PR_COMPLETE
CHAIN_COMPLETE
```

A merged PR may still leave the engineering chain active.

`CHAIN_COMPLETE` requires an objective completion basis and no remaining technical next leg.
