# Pre-work history proof

Crash readiness is a write-ahead control, not a retrospective declaration.

For every new material leg, `ACTIVE.md` records:

```text
MATERIAL_LEG_PREWORK_ENDPOINT_FILE: agents/chains/<CHAIN_ID>/endpoints/<EP>.md
```

That endpoint must already contain `PREWORK_QUALIFICATION_READY: TRUE`, the current Common protocol basis, a current qualification profile, and the complete Q1–Q5 pack.

## Historical proof

At review/handover/merge readiness, prove from Git history that the pre-work endpoint existed **before** the first material commit in the leg:

```text
material-leg base
→ commit introducing pre-work endpoint
→ first material/non-relay commit
→ remaining material work
```

The following are invalid:

```text
material code → endpoint later
endpoint + first material change in the same commit
retrospective PREWORK_QUALIFICATION_READY: TRUE
pre-work endpoint path that cannot be found at the claimed history boundary
```

If the pre-work endpoint already existed at the exact material-leg base, that is valid provided its content at the base already carried the required pre-work/Q1–Q5 state.

## Material-path classification

For this gate, canonical relay/qualification bookkeeping is non-material:

```text
agents/chains/**
agents/qualifications/**
agents/PR*_workreport.md
agents/status/**
agents/claims/**
```

Everything else changed in the leg is treated as material for ordering purposes. New writes to historical `agents/agentchain*` are rejected separately by `validate_legacy_relay_diff.py`.

## Fail-closed outcomes

History unavailable, divergent/unrelated base, missing endpoint introduction, malformed pre-work endpoint at its historical commit, or pre-work not strictly earlier than the first material commit all mean:

```text
PREWORK_HISTORY_STATUS: INVALID_OR_UNPROVEN
→ NO MERGE-READY CLAIM
→ NO NEW AUTO MATERIAL PHASE
```

Run:

```bash
python skills/engineering-pr-delivery-v2/scripts/validate_prework_history.py \
  <repo-root> <base-ref> <head-ref> <active.md>
```
