# V2-05 transfer plan

| Source | Disposition | What transfers | What does not transfer |
|---|---|---|---|
| #175 S5/S6 | ADOPT | Learning Design owns how; static `PublicationPlanningView` vs live `InteractionSupportState` | benchmark inputs, scope/diagnosis ownership |
| PR #173 | ADOPT | `LearnerStudyModel` is frozen what-to-study input; LearningDesign is choreography | old linear Core2 coupling |
| PR #161 | ADAPT | anchors, reconstruction, representation transitions, support progression, fading, transfer, completion probes | publication/page custody, old learner-profile ownership, Study Synthesis decisions embedded in LearningDesign |
| #165 | ADAPT | role presence != sufficiency; require instructional payload for reconstruction, worked reasoning, representation translation, misconception contrast, transfer | benchmark pages/templates as producer inputs; page-composition implementation belongs V2-06 |
| #162/#164 | ADAPT GENERAL INVARIANTS ONLY | conceptual support != access support; repeated same-route failure requires meaningful route change; substantial teaching followed by learner action | Primary ontology, Primary mastery/runtime contracts |
| PR #156/#157 | REJECT AS PRODUCER INPUT | none | all benchmark/reference content; downstream validation only |

No old branch, package, generated artifact, or validation result is a runtime dependency.
