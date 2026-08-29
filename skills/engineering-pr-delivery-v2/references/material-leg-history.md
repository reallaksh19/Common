# Material-leg history receipts

A single current prework pointer is insufficient for AUTO MODE because a chain may execute several bounded material batches. Every completed material batch therefore gets an append-only history receipt.

Canonical location:

```text
agents/chains/<CHAIN_ID>/material-legs/<MATERIAL_LEG_ID>.md
```

Receipt schema:

```text
CHAIN_ID:
MATERIAL_LEG_ID: LEG-001
PREVIOUS_MATERIAL_LEG: NONE | LEG-000
MATERIAL_LEG_BASE: <commit before this material batch; relay-only setup may already exist>
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: agents/chains/<CHAIN_ID>/endpoints/<EP>.md
MATERIAL_LEG_HEAD: <last material commit of this batch>
MATERIAL_LEG_HISTORY_STATUS: RECORDED
MATERIAL_SCOPE: <short description>
```

`ACTIVE.md` records the root against which the chain's material coverage is audited:

```text
MATERIAL_HISTORY_ROOT_BASE: <40-hex commit before the first material batch>
```

## Ordering invariant

For every receipt:

```text
prework endpoint exists at MATERIAL_LEG_BASE or is introduced after base
prework endpoint introduction < first material commit
first material commit <= MATERIAL_LEG_HEAD
```

The endpoint and first material change in the same commit is invalid.

Between completed material legs, changes from the previous `MATERIAL_LEG_HEAD` to the next `MATERIAL_LEG_BASE` must be relay/qualification-only. This permits endpoint/ACTIVE/receipt checkpoints without hiding unreceipted material work.

After the last receipt, changes from its `MATERIAL_LEG_HEAD` to the audited branch `HEAD` must also be relay/qualification-only. Any non-relay change means a material batch is in progress or a receipt is missing; the chain is not merge/handover-complete.

## Relay-only paths for this audit

```text
agents/chains/**
agents/qualifications/**
agents/PR*_workreport.md
agents/status/**
agents/claims/**
```

Historical `agents/agentchain*` is not treated as allowed relay for new v3 work; new writes are rejected separately.

## Crash behavior

If an agent crashes during a material batch, the prior prework endpoint still exists. The missing receipt correctly signals that the batch is incomplete and must be reconciled before it can be accepted as a completed AUTO phase.

## Validation

```bash
python skills/engineering-pr-delivery-v2/scripts/validate_material_leg_history.py .
```

The validator fails closed on:

- missing/invalid root base;
- broken receipt sequence;
- material changes in an inter-leg relay gap;
- missing or late prework endpoint;
- same-commit prework + material;
- unreceipted material after the last recorded leg;
- receipt head not reachable from the audited branch.
