# Primary architecture adopted decisions

Tracking: Common #162  
Programme roadmap: Study-Hub #40

## High ROI — architecture/contract blockers

- Common is the canonical education-semantic authority.
- Kani raw/recent evidence is separate from Teacher Runtime judgement and next pedagogical action.
- `ACQUIRE → INDEPENDENT → RETAIN → TRANSFER → STRETCH` is a teaching progression, not a single mastery enum.
- Conceptual support is separate from access/load adjustments.
- `SkillState` is separate from session-scoped `CurrentLearningState`.
- Repeated same-route failure requires a meaningful teaching-route change.
- Source/scope provenance is required for Primary vertical slices.
- Real-child observation is required before broad scaling.

## Medium ROI — adopted without architecture expansion

- Representation evidence distinguishes `PROVIDED`, `CHILD_SELECTED`, and `CHILD_PRODUCED` where observable.
- Teacher Runtime supports bounded learner agency.
- A compact feedback/teacher-voice policy is part of runtime semantics.
- Game/QR completion is activity completion, not mastery, and learning journeys return to a non-game task.

## Repository correction

Earlier Study-Hub Phase-0 documents were useful prototypes, but canonical educational semantics now belong in Common. Study-Hub retains app-facing transport/orchestration governance and should consume these Common semantics through adapters/contracts.