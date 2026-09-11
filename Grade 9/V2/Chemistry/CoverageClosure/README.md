# Chemistry V2 C-J — coverage closure, transfer evidence and longitudinal update

Implements issue #272.

This phase proves record-level closure across source obligations, Core1, Appendix A/B/C, semantic representations, Core2 transfer, post-transfer evidence, learner-state updates and future longitudinal obligations.

## Authority chain

```text
AssessmentScope source/external records
→ LearnerStudyModel
→ Core1 Study Guide semantics + Appendix A/B/C
→ C-H semantic representation bundle
→ C-I Core2 transfer plan
→ TransferEvidenceEvent
→ LearnerStateUpdate
→ LongitudinalUpdate
→ PublicationCoverageClosure
```

Top-level counters are never accepted as authority. They are recomputed from record-level matrices.

## Evidence rules

- `H3_SUCCESS` is supported success, never independent success.
- `SOLUTION_EXPOSED` is not mastery evidence.
- A correct final answer with invalid Chemistry reasoning is not full capability success.
- Positive evidence such as correct rule selection, representation translation or species tracking survives later execution errors.
- Negative evidence from `EXCLUDE_FROM_NEGATIVE_INFERENCE` items is recorded but cannot create a negative learner-state update.
- Current success may update current state but cannot silently close delayed retention, far transfer, mixed discrimination, representation shift, exception discrimination, fluency or timed obligations.

## Outputs

- `ChemistrySourceCoverageMatrix`
- `ChemistryExternalCorpusCoverageMatrix`
- `ChemistryPublicationCoverageClosure`
- `ChemistryTransferEvidenceEvent`
- `ChemistryLearnerStateUpdate`
- `ChemistryLongitudinalUpdate`

The C-J machine gate is closure, not final publication approval. Cold-start orchestration and final authorized product review remain C-K/C-L.