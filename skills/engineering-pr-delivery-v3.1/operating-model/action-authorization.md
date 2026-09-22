# V3 action authorization

V3 authorizes **actions**, not a generic relay state.

The central interface is:

```text
relay.can(action)
```

The CLI surface is:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py MATERIAL_WRITE <repo-root> --path path/to/file --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py CHECKPOINT <repo-root> --base-ref origin/main
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py HANDOVER <repo-root>
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py PR_READY <repo-root>
python skills/engineering-pr-delivery-v3.1/scripts/relay_can.py MERGE <repo-root>
```

## Stable action vocabulary

```text
READ
ANALYZE
MATERIAL_WRITE
TEST
CHECKPOINT
HANDOVER
LOCAL_EXECUTION_EXPORT
DRAFT_PR_UPDATE
PR_READY
MERGE
RELEASE
CLOSE_TASK
```

## Precedence

The evaluator applies:
1. durable V3 authority validity;
2. current lifecycle and EP for execution-plane actions;
3. current ACTIVE lease only where execution custody is required;
4. lease/EP/route/material-base binding;
5. action authority;
6. requested write path against EP write/protected scope;
7. live material/coordination basis inspection;
8. mechanical semantic drift classification against the supplied current base ref;
9. OPEN action-scoped controls;
10. checkpoint/quality requirements for delivery transitions;
11. explicit Owner delivery authority for MERGE/RELEASE.

The result contains deterministic `allowed`, `basis`, `blocking_controls`, and stable `reason_codes`.

## Execution-plane isolation

`MATERIAL_WRITE` intentionally does not inspect:
- generated snapshot freshness;
- external Issue projection freshness;
- PR body digests;
- handover readiness;
- successor qualification;
- provider delivery observations.

Those concerns may be represented by controls that block their own actions, but they do not block `MATERIAL_WRITE` unless a control explicitly blocks `MATERIAL_WRITE`.

For `MATERIAL_WRITE`, the caller supplies only the identity of the current base ref. V3 derives the drift result mechanically from:

```text
EP material_base..current base ref
∩
EP material sensitivity
```

`DISJOINT` satisfies the drift component. `RELEVANT` and `UNKNOWN` deny the write.

## Owner delivery authority

An execution Owner override is deliberately not merge/release authority. `MERGE` and `RELEASE` require explicit durable Owner action authority represented by an OPEN `OWNER` control whose source is `OWNER` and whose `permits` contains the requested action.

This is a V3-2/3 representation of explicit delivery authority. Later transactional command work may introduce a more specialized durable representation, but it must preserve the same semantic separation.


## Post-execution handover and delivery

Execution custody and handover/delivery coordination are deliberately separate.

- `MATERIAL_WRITE`, `TEST`, and `CHECKPOINT` require active execution custody.
- `CHECKPOINT` also requires a current base ref so relevant drift is re-evaluated at acceptance time.
- `HANDOVER` and `LOCAL_EXECUTION_EXPORT` may run after lease release when an accepted checkpoint supplies the work context.
- `DRAFT_PR_UPDATE` and `PR_READY` do not require an active execution lease; they require the relevant delivery vehicle, and `PR_READY` additionally requires accepted checkpoint/quality truth.
- `MERGE` and `RELEASE` continue to require explicit Owner delivery authority.

This prevents the delivery/handover planes from being re-coupled to material execution custody.
