# Common → Study-Hub → Kani handoff

Common defines educational semantics; app repositories serialize and execute them.

## Common exports semantically

```text
LearningObject IDs
TeachingTarget
LearningEpisode meaning
TeacherMove vocabulary
support/access semantics
representation-role semantics
source-boundary semantics
longitudinal evidence dimensions
```

## Study-Hub translates operationally

Study-Hub may serialize an episode into renderer-specific orchestration such as:

```text
Study-Hub activity
Print/PDF activity
Kani mission
Oral step
Delayed retrieval marker
```

Study-Hub remains authority for `kani-content-v1`, `kani-catalog-v1`, `kani-activity-v1`, and `kani-attempt-v1` transport/version governance.

## Kani executes and observes

Kani receives the minimum mission information necessary to run a game experience. It records immutable observable evidence and may produce deterministic recent-evidence summaries.

It must not receive or embed durable mastery judgement, canonical answer truth duplicated from the content contract, or a complete child pedagogical profile merely to launch a mission.

## Identity rule

Printed mission references/QRs identify a mission or activity. Learner identity is bound at runtime and must not be encoded into a printed QR.

## Return-to-learning rule

Game completion means `ACTIVITY_COMPLETED`. A Primary journey that uses Kani should normally return to a non-game independent task before independent learning evidence is claimed.

## Compatibility rule

Study-Hub/Kani transport schemas may evolve independently when serialization changes. Changes to the meaning of learning, support, evidence, diagnosis, or TeacherMove require a Common semantic change first.
