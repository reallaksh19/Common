# Relay Engineering Model

## Purpose

Engineering work is a chain of durable repository endpoints, not a sequence of chat sessions.

The outgoing agent is never required for recovery. The latest valid endpoint is the baton.

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
  -> endpoint
  -> QUALIFICATION_REQUIRED for new incoming custody
  -> qualified contribution
  -> endpoint
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

## Endpoint authority

A completed endpoint is append-only.

If an earlier endpoint contains an error, a later endpoint must record:

```text
SUPERSEDES_ENDPOINT:
SUPERSEDED_ASSERTION:
CORRECTED_STATE:
EVIDENCE:
```

Do not rewrite historical custody claims.

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

The system guarantees recovery only up to the latest persisted endpoint and any later repository commits that can be independently reconciled.

Therefore prefer small coherent durable units:

```text
intent/hypothesis endpoint
-> one focused engineering unit
-> validation
-> next endpoint
```

## Separation of completion states

Never collapse these:

```text
AGENT_LEG_COMPLETE
PR_COMPLETE
CHAIN_COMPLETE
```

A merged PR may still leave the engineering chain active.

`CHAIN_COMPLETE` requires an objective completion basis and no remaining technical next leg.
