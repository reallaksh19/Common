# Crash Recovery

## Governing rule

The protocol never depends on an outgoing agent intentionally releasing the baton.

The latest valid durable endpoint is the recovery basis.

## Recovery entry conditions

Use crash recovery when:

- the prior agent disappeared or became unavailable;
- the prior chat/context is lost;
- repository changes exist after the latest endpoint and their intent is not yet reconciled;
- an incoming agent cannot prove that the live material state still matches the endpoint;
- the previous agent's qualification or authority state is unknown.

## Recovery sequence

1. Locate the chain's latest endpoint in `agents/agentchain.md`.
2. Record its `CHECKPOINT_HEAD`, `MAIN_HEAD_OBSERVED`, PR, branch, exact next action, Q1-Q5, and indexed dependencies.
3. Fetch live main/base, PR head, merge base, diff, reviews, and checks.
4. Compare every material commit/path after `CHECKPOINT_HEAD`.
5. Classify post-endpoint work.
6. Preserve known-good evidence and explicitly isolate uncertainty.
7. Create a new `AGENT_LOST_RECOVERY` endpoint.
8. Regenerate Q1-Q5 if current material state or unresolved work differs materially.
9. Incoming engineering-critical mutation remains READ_ONLY until qualification.

## Post-endpoint classification

Use:

```text
RECOVERABLE
  Intent and effects can be independently established from repository evidence.

PARTIAL_UNKNOWN
  Some work is understandable, but material intent/evidence remains unknown.

CONTAMINATED
  Known-good and unsafe/unproven changes are mixed and require bounded salvage.

UNTRUSTED
  Continuing would require guessing engineering intent or authority.
```

## Recovery outcomes

```text
CONTINUE
SALVAGE_PARTIAL
SUPERSEDE
ABANDON
```

Agent replacement alone is not a reason to create a new PR. Choose a new PR only when it is the safer coherent implementation vehicle.

## Recovery endpoint requirements

Record:

```text
ENDPOINT_REASON: AGENT_LOST_RECOVERY
RECOVERY_FROM_ENDPOINT:
RECOVERY_BASIS_HEAD:
LIVE_HEAD:
POST_ENDPOINT_COMMITS:
CLASSIFICATION:
RECOVERED_KNOWN_GOOD:
PARTIAL_OR_UNTRUSTED:
SUPERSEDED_ASSUMPTIONS:
NEWLY_OBSERVED:
VALIDATION_RECHECK_REQUIRED:
EXACT_NEXT_ACTION:
```

Then provide fresh source indexes and Q1-Q5 against the recovered state.

## Unpersisted work

If the previous agent changed local files but never persisted them to a repository-visible durable state, that work is not recoverable authority.

Do not invent its content from chat summaries or infer that it was complete.

## Mid-change recovery

A diff after the latest endpoint is not automatically bad.

For each changed file ask:

```text
What changed?
Why can that intent be proven?
What authority does it touch?
What validation applies to this exact HEAD?
Did implementation and expected-value/oracle authority move together?
Can the change be isolated or reverted cleanly?
```

If any material answer requires guessing, quarantine that part before continuing.

## Concurrent resurrection

The prior agent may not actually be permanently gone.

Therefore the repository state, not session liveness, is authoritative. If two agents contribute from divergent material states, classify it as a coordination/reconciliation problem before accepting either as the current chain state.
