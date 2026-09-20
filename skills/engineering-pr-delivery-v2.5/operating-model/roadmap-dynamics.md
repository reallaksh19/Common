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

## Task admission is mandatory

Before creating/activating an EP, resolve the incoming task against the current roadmap.

If the task is already fully owned by an existing WP, record `MAPPED_EXISTING_WP`.

If existing execution scope must change, apply the appropriate roadmap transaction and record `REVISED_EXISTING_WP`.

If the concept remains valid but the discovered task has no WP, add a bounded execution WP and record `ADDED_EXECUTION_WP`. This can be an execution-level roadmap revision even when `concept_change = NO_CONCEPT_CHANGE`.

If no usable roadmap exists, search existing repository planning sources first, then create/bootstrap the V2.5 roadmap and record `CREATED_ROADMAP`.

An agent may not use "concept unchanged" as a reason to skip execution-roadmap reconciliation.
