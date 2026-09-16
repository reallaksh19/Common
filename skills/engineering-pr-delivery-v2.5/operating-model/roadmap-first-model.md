# Roadmap-first operating model

The overall roadmap is the authoritative engineering planning graph. EPs execute the current roadmap frontier; they do not define the project's next direction.

```text
Owner intent
  -> Overall roadmap
  -> Executable frontier
  -> EP
  -> implementation + validation
  -> CP
  -> roadmap reconciliation
  -> recomputed frontier
  -> successor EP
```

## Hierarchy
```text
Objective
  -> Phase
     -> Work Package
        -> EP(s)
```
A work package is the smallest roadmap planning node. An EP is an execution slice against one work package and one roadmap revision.

## Definition maturity
Roadmap nodes use `DETAILED`, `DEFINED`, `PARTIALLY_DEFINED`, `DISCOVERY_REQUIRED`, or `OWNER_REVIEW_REQUIRED`. Only `DETAILED` work packages may become executable. Future work must not contain invented precision.

## Planning and execution state
Typical planning state is `FUTURE | PLANNED | ACTIVE | COMPLETE | SUPERSEDED | CANCELLED`. Execution eligibility is separate: `WAITING | EXECUTABLE | ACTIVE | TERMINAL`.

## No duplicate authority
Do not introduce a separate WORK_GRAPH authority. `OVERALL_ROADMAP.yaml` already contains work topology and dependencies. `ISSUE_GRAPH.yaml` projects GitHub coordination; `PROGRESS.yaml` carries calculated accounting.