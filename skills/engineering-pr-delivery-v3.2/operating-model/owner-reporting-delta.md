# V3.1 Owner reporting delta

## Purpose

V3.1 should become a better reporter than V2.5 and V3 while having less power than either of them to interfere with production.

The Owner publication cursor exists only to answer:

> **What changed since the Owner was last shown status?**

It is reporting metadata, not engineering authority.

## Inputs

The delta is derived from the existing V3.1 read models:

```text
CURRENT_SNAPSHOT
TASK_SNAPSHOT
IMPROVEMENT_VIEW
        ↓
normalized Owner-visible baseline
        ↓
compare with last Owner-visible baseline
        ↓
publication delta
```

No new engineering truth is created.

## Cursor

Default path:

```text
relay/PUBLICATION/OWNER_STATUS.yaml
```

Schema:

```text
relay-v3.1-owner-publication-cursor
```

The cursor records:

- sequence;
- publication timestamp;
- source digests;
- normalized Owner-visible baseline;
- optional note.

It deliberately does **not** record permission, authorization, readiness, or blocking state beyond what already exists in the source read models.

## Evaluate without writing

```bash
python skills/engineering-pr-delivery-v3.1/scripts/owner_publication.py \
  relay/GENERATED/CURRENT_SNAPSHOT.yaml \
  --task-snapshot relay/GENERATED/tasks/<EP>.snapshot.yaml \
  --improvement-view relay/GENERATED/improvements/<CP>.improvement.yaml
```

The result includes:

- event class;
- changed dimensions;
- acceptance transitions;
- programme progress transition;
- accepted-evidence transition;
- roadmap revision transition;
- material-head transition;
- checkpoint transition.

Event classes are:

```text
INITIAL_SNAPSHOT
TASK_PROGRESS
TASK_REGRESSION
IMPLEMENTATION_CHANGE
EVIDENCE_PROGRESS
DELIVERY_OR_CUSTODY_PROGRESS
CONTROL_STATE_CHANGE
TASK_PLANNING_PROGRESS
WAITING_OR_MONITORING
NO_MATERIAL_PROGRESS
```

These are reporting classifications only.

## Render Owner status with "What changed"

```bash
python skills/engineering-pr-delivery-v3.1/scripts/render_owner_status.py \
  relay/GENERATED/CURRENT_SNAPSHOT.yaml \
  --task-snapshot relay/GENERATED/tasks/<EP>.snapshot.yaml \
  --improvement-view relay/GENERATED/improvements/<CP>.improvement.yaml \
  --publication-cursor relay/PUBLICATION/OWNER_STATUS.yaml
```

When a previous cursor exists, the report begins with a concise **What changed** section.

Important distinctions are explicit:

- implementation movement does not imply acceptance movement;
- implementation-plan / expected-observable movement does not imply implementation or acceptance completion;
- evidence movement does not imply task completion;
- regression is visible instead of hidden by aggregate percentages;
- unchanged state is reported as `NO_MATERIAL_PROGRESS`.

## Record only after the Owner-visible publication

After the report has actually been shown/published:

```bash
python skills/engineering-pr-delivery-v3.1/scripts/owner_publication.py \
  relay/GENERATED/CURRENT_SNAPSHOT.yaml \
  --task-snapshot relay/GENERATED/tasks/<EP>.snapshot.yaml \
  --improvement-view relay/GENERATED/improvements/<CP>.improvement.yaml \
  --cursor relay/PUBLICATION/OWNER_STATUS.yaml \
  --apply \
  --note "Owner status published"
```

This advances only reporting history.

## Non-interference invariant

No production path may consume the publication cursor as a gate.

In particular it must never be consulted by:

- `relay_can.py`;
- task admission;
- lease/takeover/recovery;
- material writes;
- checkpoint recording;
- handover;
- delivery;
- merge/release/closure logic.

If the cursor is missing, stale, malformed, or cannot be written, production work continues. Only delta reporting is degraded.

The governing invariant is:

> **Reporting failure may reduce observability; it must never reduce production agency.**
