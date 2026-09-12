# V2-03 transfer plan

Old work is migration evidence only. V2-03 has no branch, runtime, package, generated-artifact, or validation dependency on these sources.

| source | mechanism | disposition | V2 destination | semantic change / new validation |
|---|---|---|---|---|
| #175 S3 / S1 | separate LearningGoalRequest, CanonicalTargetScope, LearnerStudyScope, PublicationScope | ADOPT | `contracts/` | executable non-overlap and preservation falsifiers |
| PR #160 ScopeGraph | project scope references versioned canonical IDs; scope does not own ontology | ADAPT | `canonical-target-scope.schema.json` | remove project-candidate promotion concerns from Goal/Scope authority |
| PR #160 prerequisite edges | canonical prerequisite references | ADAPT | synthetic registry + resolver | add deterministic transitive closure, cross-subject composition, cycle detection |
| PR #160 Core1 gap fail-back | unresolved canonical requirement must fail back to canonical authority | ADAPT | `CANONICAL_GAP_CANDIDATE` | reason-bearing gap record bound to requesting target/dependency |
| PR #159 Math specialization | subject scope references shared canonical concepts | ADAPT INTERFACE ONLY | canonical IDs used by fixtures | no Math subject truth copied into V2-03 |
| #177 Chemistry acceptance case | gas-law primary + shared proportional reasoning dependency | TEST_FIXTURE_ONLY | `fixtures/` + tests | synthetic IDs only; no Chemistry learner/product content |
| PR #156 / #157 | mature learner-product references | REJECT AS PRODUCER INPUT | none | may be used only in later final validation stages |

## Rejected transfers

- learner Bxx/profile inside canonical bundle identity;
- canonical ontology mutation through project scope;
- embedded copies of dependency semantics;
- benchmark/reference-artifact inputs;
- Study Synthesis treatment decisions;
- LearningDesign choreography;
- publication layout/page semantics.
