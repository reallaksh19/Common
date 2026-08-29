# NMTC Bhaskara Preliminary — Topic Item Metadata Schema v1

## Purpose

Define the machine-readable contract for question/drill items across all ten topic packages.

This schema prevents a later production bank from flattening away:

- provenance;
- source conflicts;
- figure custody;
- recognition/first-move intent;
- transfer level;
- student/teacher role;
- calibration status.

## Stable item ID

Author-created topic items should receive deterministic IDs that cannot be confused with PYQ IDs.

Recommended form:

`NMTC-TOPIC-<PACKAGE>-<ASSET>-<NNN>`

Examples:

- `NMTC-TOPIC-P0-1-TR-001`
- `NMTC-TOPIC-P0-4-REC-007`
- `NMTC-TOPIC-P2-2-MAST-012`

Historical PYQs retain their separate authority IDs:

`NMTC-BH-P-YYYY-QNN`

Never convert an author-created item into a PYQ-format ID.

## Required fields

| Field | Meaning |
|---|---|
| `item_id` | stable unique ID |
| `package` | P0-1 through P2-2 |
| `asset_type` | first_step / ladder / recognition / first_line / transfer / mastery / worked_example |
| `source_file` | repository path |
| `local_item_ref` | local question/card identifier in source file |
| `domain` | broad mathematical domain |
| `mechanism` | stable mechanism/archetype label |
| `provenance` | P0/P1/P2/P3 or AUTHOR_CREATED_* |
| `historical_anchor_id` | optional `NMTC-BH-P-YYYY-QNN` when genuinely linked |
| `source_status` | CLEAN / FIGURE_GATED / SOURCE_CONFLICT / BONUS_EVIDENCE / etc. |
| `response_type` | mcq / numeric / short_answer / proof / recognition / first_line |
| `answer_custody` | answer / solution / teacher-only location |
| `first_move` | compact first useful move where teacher metadata is appropriate |
| `diagnostic_tags` | REC/FM/REP/... |
| `student_export` | true/false/projected |
| `teacher_export` | true/false |
| `figure_status` | N/A / AUTHOR_CREATED / EXACT_SOURCE_RETAINED / FIGURE_GATED |
| `timing_status` | NOT_RUN / PILOT_DATA_AVAILABLE_NOT_FROZEN / CALIBRATED_FOR_TRAINING |
| `calibration_version` | optional calibration record version |

## Difficulty profile

Do not collapse difficulty to one unsupported scalar before calibration.

Retain a vector where available:

- recognition demand;
- first-move demand;
- reasoning depth;
- algebra burden;
- calculation burden;
- trap/boundary burden;
- time-pressure burden.

Before classroom evidence, these remain authoring descriptors, not psychometric measurements.

## Provenance rules

### Author-created

Must use one of:

- `AUTHOR_CREATED_FOUNDATION`
- `AUTHOR_CREATED_TRANSFER`

No NMTC year/question number.

### Historical

Must retain:

- stable PYQ ID;
- source provenance class;
- scoring disposition where known;
- source defect/figure status;
- whether the exact stem/figure is publication-authorized.

## Figure rules

`FIGURE_GATED` means the item may remain in teacher/source analysis but cannot be published as an exact historical student anchor.

An author-created text-complete analogue is a separate item with separate ID/provenance.

## Student/teacher rules

Machine metadata is teacher/authoring authority.

A student export may use the metadata to select questions but must not leak:

- diagnostic tags;
- package label in mixed assessment;
- first move;
- answer custody;
- hidden source-conflict resolution.

## Validation invariants

When the topic ledger is populated, validation must confirm:

```text
unique item_id
valid package code
valid provenance
source_file resolves
local_item_ref resolves
historical IDs only on historical items
no author-created item marked official
FIGURE_GATED historical item not marked canonical student export
calibrated timing requires a calibration_version
```

## Current state

```text
TOPIC_METADATA_SCHEMA = DEFINED
TOPIC_METADATA_LEDGER = NOT_RUN
TOPIC_METADATA_VALIDATION = NOT_RUN
```
