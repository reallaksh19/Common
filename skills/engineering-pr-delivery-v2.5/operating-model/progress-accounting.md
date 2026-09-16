# Progress accounting

Progress is derived, never estimated:
```text
Acceptance Criteria -> EP -> Work Package -> Phase -> Objective -> Overall Roadmap
```
Each required acceptance criterion has non-negative weight. Earned weight follows its completion/evidence rule, not code-written status.

`PROGRESS.yaml` records a Progress Basis tied to a roadmap revision. Approved scope changes create a new basis while preserving completed work. Example: `756/1200=63%` may become `756/1320=57%` after approved scope addition. The handover explains the denominator change.