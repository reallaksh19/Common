# V3 action authorization

V3 authorizes **actions**, not a generic relay state.

The central interface is:

```text
relay.can(action)
```

The initial CLI surface is:

```bash
python skills/engineering-pr-delivery-v3/scripts/relay_can.py MATERIAL_WRITE <repo-root> --path path/to/file --drift DISJOINT
python skills/engineering-pr-delivery-v3/scripts/relay_can.py CHECKPOINT <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py HANDOVER <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py PR_READY <repo-root>
python skills/engineering-pr-delivery-v3/scripts/relay_can.py MERGE <repo-root>
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
1. V3 foundation validity;
2. current lifecycle and EP;
3. current ACTIVE lease where the action requires one;
4. lease/EP/route/material-base binding;
5. action authority;
6. requested write path against EP write/protected scope;
7. observed drift classification;
8. OPEN action-scoped controls;
9. checkpoint/quality requirements for delivery transitions;
10. explicit Owner delivery authority for MERGE/RELEASE.

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

Until V3-3 supplies the mechanical drift classifier, the CLI requires an explicit observed drift classification for `MATERIAL_WRITE`. `NONE` and `DISJOINT` allow the drift component; `RELEVANT` and `UNKNOWN` deny it.

## Owner delivery authority

An execution Owner override is deliberately not merge/release authority. `MERGE` and `RELEASE` require explicit durable Owner action authority represented by an OPEN `OWNER` control whose source is `OWNER` and whose `permits` contains the requested action.

This is a temporary V3-2 representation of explicit delivery authority. Later transactional command work may introduce a more specialized durable representation, but it must preserve the same semantic separation.
