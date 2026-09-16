# Dynamic roadmap semantics

Roadmap mutation classes:

- `EXECUTION_DERIVED_STATUS`: factual state/progress/dependency updates; agent may apply when proven.
- `ENGINEERING_DISCOVERY_PROPOSAL`: new prerequisite, coupling, split, regression requirement or future risk; agent may propose but may not redefine Owner intent.
- `OWNER_INTENT_MUTATION`: feature, scope, concept, phase-order, target architecture, engineering authority or user-workflow change; requires explicit Owner authority and ODR.

Material revision transaction:
```text
change source -> classify -> new roadmap revision -> topology/status update
-> dependency reconciliation -> stale EP reconciliation -> issue projection
-> progress-basis recompute -> frontier recompute -> successor EP -> REPO_STATE
```
Every material revision explains added, removed, changed and unaffected nodes plus progress-basis impact. Checkpoint discoveries classify as `LOCAL_IMPLEMENTATION`, `CURRENT_EP_CHANGE`, `FUTURE_ROADMAP_PROPOSAL`, or `OWNER_DECISION_REQUIRED`.