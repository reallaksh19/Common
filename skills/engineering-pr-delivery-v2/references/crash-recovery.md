# Crash Recovery

## Governing rule

The protocol never depends on an outgoing agent intentionally releasing the baton.

For canonical chains, the recovery basis is:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
+ referenced immutable endpoint
+ live repository state
```

## Recovery entry conditions

Use crash recovery when:

- the prior agent disappeared or became unavailable;
- prior chat/context is lost;
- repository changes exist after the latest endpoint and intent is not reconciled;
- the live material state cannot be proven to match the endpoint;
- previous qualification/authority is unknown;
- an orphan endpoint exists because the prior agent died before advancing `ACTIVE.md`;
- an `ACTIVE.md` write failed because another agent advanced the custody epoch.

## Recovery sequence

1. Locate `agents/chains/<CHAIN_ID>/ACTIVE.md`.
2. Record `ACTIVE_ENDPOINT`, `CUSTODY_EPOCH`, custodian, head, PR, branch, authority domain, coordination state, and dependencies.
3. Open the referenced endpoint and record its `CHECKPOINT_HEAD`, exact next action, Q1-Q5, and indexed dependencies/sources.
4. Fetch live main/base, PR head, merge base, diff, reviews, and checks.
5. Compare every material commit/path after `CHECKPOINT_HEAD`.
6. Inspect the chain's `endpoints/` directory for unreferenced/orphan or divergent successors.
7. Classify post-endpoint work and custody state.
8. Preserve known-good evidence and isolate uncertainty.
9. Create an `AGENT_LOST_RECOVERY` or reconciliation endpoint.
10. Advance `ACTIVE.md` using exact prior blob/version + next custody epoch.
11. Incoming engineering-critical mutation remains READ_ONLY until qualification.

## Post-endpoint classification

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

Agent replacement alone is not a reason to create a new PR.

## Recovery endpoint requirements

Record:

```text
ENDPOINT_REASON: AGENT_LOST_RECOVERY
RECOVERY_FROM_ENDPOINT:
RECOVERY_BASIS_HEAD:
LIVE_HEAD:
CUSTODY_EPOCH:
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

## Endpoint written but ACTIVE.md not advanced

This is a normal crash window.

The endpoint is an orphan durable artifact, not lost work:

1. do not delete it silently;
2. compare its `PREVIOUS_ENDPOINT`, `CHECKPOINT_HEAD`, and `CUSTODY_EPOCH` with current chain state;
3. check whether another successor was created from the same prior endpoint;
4. classify the orphan as valid/recoverable/divergent/untrusted;
5. either advance `ACTIVE.md` or create an explicit reconciliation/supersession endpoint.

## Stale ACTIVE.md write

If the prior blob/version or `CUSTODY_EPOCH` changed between read and update:

```text
STALE_WRITE
```

Do not force the pointer. Another agent may have advanced the same chain. Re-ground and reconcile.

This stale-write rule applies to the same chain only. A WRC chain update should not conflict with LAFEA or LoadCalc relay state because those chains own different `ACTIVE.md` files.

## Unpersisted work

Local unpushed changes are not recoverable authority. Do not invent their content from chat summaries.

## Mid-change recovery

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

## Legacy recovery

For a legacy-format chain that has not migrated, recover from `agents/agentchain.md` plus its referenced legacy endpoint. Do not rewrite historical endpoints merely to fit the new directory layout.

See `chain-concurrency.md` for migration and custody rules.
