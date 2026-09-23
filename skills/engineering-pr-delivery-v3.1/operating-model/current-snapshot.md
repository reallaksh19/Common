# V3 current snapshot and novice entrypoint

`CURRENT_SNAPSHOT.yaml` is the first-read model for an Owner, incumbent executor, or zero-context successor.

It is **never authority** and MUST declare:

```yaml
authority: DERIVED_READ_MODEL
```

The source direction is one-way:

```text
ROADMAP / STATE / EP / LEASE / CHECKPOINT / CONTROLS
                      ↓
              CURRENT_SNAPSHOT
                      ↓
       Owner / technical / handover views
```

A snapshot disagreement is a conformance failure. The snapshot never repairs, overrides, or supplies missing canonical authority.

## What the snapshot answers

A novice executor should quickly determine:
- the Owner outcome and current goal;
- current roadmap revision, programme progress, and accepted evidence coverage;
- active WP / EP / lease / executor;
- allowed, protected and prohibited scope;
- exact material basis and coordination head;
- latest accepted checkpoint and validation evidence;
- execution, handover and delivery blockers separately;
- current delivery vehicle and whether merge authority exists;
- immediate material action, delivery action and stop conditions;
- exact canonical files to open next.

## Progress

The snapshot deliberately separates programme status from native evidence coverage.

**Programme progress** is derived from authoritative ROADMAP work-package states and weights. A work package marked `COMPLETE` by the governed roadmap remains programme-complete even when historical or migrated native checkpoint artifacts were not replayed into the current protocol tree.

**Accepted evidence coverage** is derived from:
- current roadmap weights;
- checkpoints whose acceptance is PASS and quality is CLEAR;
- the EP/work package referenced by each accepted checkpoint.

Starting implementation, temporarily green tests, opening a PR, refreshing projection, or generating a handover earns neither programme completion nor accepted evidence coverage by itself.

The two percentages may legitimately differ. That difference is evidence/migration provenance information; it must not silently reopen ROADMAP-complete programme work.

If a new roadmap revision adds legitimate scope while completed work or accepted checkpoints remain unchanged, either denominator-based percentage may decrease. That does not imply accepted engineering work was lost.

## Blockers

OPEN controls are projected by the actions they block:
- execution blockers: READ / ANALYZE / MATERIAL_WRITE / TEST / CHECKPOINT;
- handover blockers: HANDOVER / LOCAL_EXECUTION_EXPORT;
- delivery blockers: DRAFT_PR_UPDATE / PR_READY / MERGE / RELEASE / CLOSE_TASK;
- informational: no declared blocked action.

One control may appear in more than one group when its declared blocked actions span multiple planes.

## Generation

For ACTIVE work, live material basis needs the current base ref:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/generate_snapshot.py <repo-root> --base-ref origin/main
```

To replace the path declared by `STATE.generated.snapshot` only after a successful build:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/generate_snapshot.py <repo-root> --base-ref origin/main --apply
```

The write uses a temporary file followed by replacement so an incomplete YAML document is not published as the current snapshot.


## Completion/status reporting

Do not create or describe a fourth authoritative "task completion snapshot".

Completion reporting is an on-demand rendering over the existing derived surfaces:

```text
CURRENT_SNAPSHOT
+ TASK_SNAPSHOT
+ IMPROVEMENT_VIEW
        ↓
V3.1 Owner / Task Status
```

The renderer must preserve the distinctions between:

- programme progress and accepted evidence coverage;
- project/programme state and task-local completion;
- current execution/custody and accepted checkpoint truth;
- execution, handover, delivery and informational blockers;
- evidence-bound improvement and work that is still not proved;
- current action and stop conditions.

All three inputs remain `DERIVED_READ_MODEL`. The combined status report is a presentation surface only and MUST NOT be persisted or consumed as execution, acceptance, programme or delivery authority.

Render it with:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/render_owner_status.py \
  relay/GENERATED/CURRENT_SNAPSHOT.yaml \
  --task-snapshot relay/GENERATED/tasks/<EP>.snapshot.yaml \
  --improvement-view relay/GENERATED/improvements/<CP>.improvement.yaml
```

## Project snapshot role and #421 task projections

The V3 `CURRENT_SNAPSHOT.yaml` defined here is the **project/programme first-read model**. It answers where the programme is, what is accepted/active, broad blocker state, delivery state, and the current frontier.

It is not intended to absorb task-local benchmark state, negative knowledge, accepted do-not-reopen guidance, or improvement classification.

Common #421 owns the complementary generated projections:

```text
PROJECT_SNAPSHOT / CURRENT_SNAPSHOT
TASK_SNAPSHOT
IMPROVEMENT_VIEW
```

All remain `DERIVED_READ_MODEL` surfaces. #421 must derive them from governed roadmap/EP/checkpoint/progress/control/event/provider truth rather than creating competing lifecycle authority.


## Destructive reconstruction requirement

Generated state is disposable. Deleting `relay/GENERATED/**` must not invalidate durable authority or change synchronous action authorization.

A zero-context successor must be able to rebuild the current project/task/improvement read models from ROADMAP, STATE, EP, LEASE, CHECKPOINT, CONTROLS, EVENTS, immutable evidence, and any live provider observation required by the boundary being crossed.

Full conformance may report an expected generated projection as missing until it is regenerated. That is projection incompleteness, not an authority failure.

See `architecture-preservation-contract.md`.
