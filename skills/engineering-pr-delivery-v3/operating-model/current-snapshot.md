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
- current roadmap revision and accepted progress;
- active WP / EP / lease / executor;
- allowed, protected and prohibited scope;
- exact material basis and coordination head;
- latest accepted checkpoint and validation evidence;
- execution, handover and delivery blockers separately;
- current delivery vehicle and whether merge authority exists;
- immediate material action, delivery action and stop conditions;
- exact canonical files to open next.

## Progress

Accepted progress is derived from:
- current roadmap weights;
- checkpoints whose acceptance is PASS and quality is CLEAR;
- the EP referenced by each accepted checkpoint.

Starting implementation, temporarily green tests, opening a PR, refreshing projection, or generating a handover does not earn accepted progress.

If a new roadmap revision adds legitimate scope while accepted checkpoints remain unchanged, displayed progress may decrease because the denominator changed. That is expected and does not imply accepted engineering work was lost.

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
python skills/engineering-pr-delivery-v3/scripts/generate_snapshot.py <repo-root> --base-ref origin/main
```

To replace the path declared by `STATE.generated.snapshot` only after a successful build:

```bash
python skills/engineering-pr-delivery-v3/scripts/generate_snapshot.py <repo-root> --base-ref origin/main --apply
```

The write uses a temporary file followed by replacement so an incomplete YAML document is not published as the current snapshot.


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
