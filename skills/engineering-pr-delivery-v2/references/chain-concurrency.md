# Chain-Local Concurrency and Custody

## Purpose

Allow independent engineering chains to advance without shared relay-file conflicts, while preventing accidental duplicate writers on the **same work item**.

Canonical chain state remains:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
```

`agents/agentchain.md` is historical/derived navigation, not active authority.

## Work-item identity — first concurrency gate

Path/authority overlap is not sufficient to detect two agents working the same GitHub issue. Every new material leg/successor endpoint records:

```text
WORK_ITEM_KEY: <stable work identity>
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
AGENT_INSTANCE_ID: <agent-class>:<UUID>
```

Recommended GitHub form:

```text
WORK_ITEM_KEY: github:reallaksh19/Advanced_Analysis#1535
```

`AGENT_INSTANCE_ID` identifies one live agent/conversation instance. A model family/name such as `OPENAI-GPT-5.6-SOL`, `GPT-5.6`, or `claude` is not a unique instance identity and is invalid for new material custody.

Canonical examples:

```text
AGENT_INSTANCE_ID: chatgpt:6c19e9d4-4be3-4f4c-9b4a-7a1f52d1e930
AGENT_INSTANCE_ID: codex:3487ad68-7933-4b62-a35b-c9a803948477
```

### EXCLUSIVE

For `WORK_ITEM_MODE: EXCLUSIVE`, at most one non-terminal canonical chain may hold the same `WORK_ITEM_KEY`.

If another live chain already holds it:

```text
BLOCK_NEW_CHAIN
→ READ existing ACTIVE/endpoint
→ explicit takeover/join/supersession decision
→ qualification-first if custodian changes
```

Do not create a second mutable chain merely because file/path overlap appears disjoint.

### PARTITIONED

Partitioning one work item across agents requires explicit Owner authority:

```text
WORK_ITEM_MODE: PARTITIONED
WORK_ITEM_PARTITION: <stable non-overlapping partition identity>
WORK_ITEM_PARTITION_AUTHORITY: OWNER:<durable authorization locator>
```

Two live chains may share a work-item key only when each has a distinct partition and valid Owner partition authority. Duplicate partition identity fails closed.

Exact work-item collision is evaluated **before** semantic path/authority overlap. Semantic overlap remains an additional control.

## Endpoint identity

Endpoint IDs are unique within a chain, not repository-wide. Durable endpoint key:

```text
(CHAIN_ID, ENDPOINT_ID)
```

Question-set IDs remain visibly chain-namespaced.

## ACTIVE.md identity fields

Current new-material state includes at minimum:

```text
CHAIN_STATE_VERSION: 3
CHAIN_ID:
MISSION:
ACTIVE_ENDPOINT:
ACTIVE_ENDPOINT_FILE:
PR:
BRANCH:
HEAD:
STATE:
AUTHORITY_DOMAIN:
ACTIVE_CUSTODIAN:
AGENT_INSTANCE_ID:
WORK_ITEM_KEY:
WORK_ITEM_MODE:
CUSTODY_EPOCH:
COORDINATION_STATE:
DEPENDENCIES:
```

`ACTIVE_CUSTODIAN` may be a human-readable label, but write/collision identity uses `AGENT_INSTANCE_ID`.

## Custody epoch / compare-and-swap

Each direct successor increments `CUSTODY_EPOCH` by exactly one. Before updating ACTIVE:

1. read the current ACTIVE blob/version and epoch;
2. create the next immutable endpoint from that exact state;
3. update ACTIVE using the exact prior blob/version and `epoch + 1`;
4. if the write conflicts or the epoch changed, stop and re-ground.

Do not force a stale update merely because two agents began from the same endpoint.

## Same-chain divergence

Two successors from one endpoint are not silently accepted. Competing successors require explicit reconciliation/supersession; newest timestamp or biggest diff does not win automatically.

If another `AGENT_INSTANCE_ID` attempts to continue the same chain without an accepted custody transition, it remains READ_ONLY until qualification/takeover controls clear.

## Different-work-item concurrency

Independent chains with different `WORK_ITEM_KEY` values may advance concurrently when there is no real overlap in:

```text
exact file/path
authority domain
benchmark/oracle
controlled input
release/publication authority
dependency/stacking
```

Use semantic overlap detection after the exact work-item gate.

## Derived dashboard

`render_agentchain_dashboard.py` remains navigation convenience only. Normal endpoint advancement does not require a shared dashboard commit.

## Legacy compatibility

Historical `agents/agentchain*` artifacts remain read/cite/recovery evidence and are not mass-rewritten. The next material leg deliberately adopts canonical chain-local state, exact work-item identity and agent-instance identity.
