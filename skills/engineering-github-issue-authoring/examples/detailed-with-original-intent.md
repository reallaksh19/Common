# Golden example — detailed single issue with Original Intent

```text
ISSUE_ROLE: SINGLE
AUTHORING_PROFILE: DETAILED
ORIGINAL_INTENT_ISSUE: github:owner/repo#300
RELAY_PROTOCOL: V3.1_ONLY
```

## Mission

Make direct existing-item selection resolve to the exact canonical item without changing the existing mutation authority.

## Ground truth at issue creation

Observed main:

`0123456789012345678901234567890123456789`

Live code already has a canonical Inspector capability path. The missing seam is page-selection identity synchronization.

## Original Intent source

`github:owner/repo#300` preserves the Owner's direct request verbatim plus supplied screenshot and expected output.

## Owner task / expected-output ledger

| ID | Requirement | Source | Current interpretation |
| --- | --- | --- | --- |
| TASK-001 | select existing item directly | Original Intent #300 | synchronize page item with canonical Inspector item |
| TASK-002 | do not widen edit authority | Original Intent #300 | keep existing mutation command canonical |

## Current production path

```text
rendered item
→ stable page/item identity
→ canonical Inspector lookup
→ selection/highlight
→ existing mutation capability path
```

## Acceptance contract

| ID | Criterion |
| --- | --- |
| AC-01 | rendered item exposes canonical source identity |
| AC-02 | stale revision/item identity is rejected |
| AC-03 | selection routes through existing Inspector capability |
| AC-04 | no new mutation command is introduced |

## Reconstruction topology

```text
Original Intent #300
→ current Owner/Roadmap refs
→ this issue / EP
→ latest primary-agent reconciliation comment
→ OFFLOAD/Local Agent refs when present
→ RLL refs when present
→ PR/tests/runtime material
→ Task Snapshot / Handover
```

Conversation bodies stay on their owning provider surfaces. This issue and its Task Snapshot index refs only.

## Falsifier

If live code already maps the page-selected identity to the exact canonical Inspector item under stale-revision rejection, the proposed synchronization patch is unnecessary.

## Definition of Done

All AC-* criteria have exact evidence, neighboring behavior remains unchanged, verification truth preserves PASS/FAIL/NOT_RUN, and the final Task Result states what consumers may and may not infer.
