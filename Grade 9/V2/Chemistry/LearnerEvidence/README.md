# Chemistry V2 — C-E optional learner evidence and diagnostic inference

This directory implements **C-E / #267**. It consumes the fixed C-C assessment scope and C-D semantic reasoning routes. `AttemptSet` is genuinely optional.

```text
same SourceSet + QuestionSet/CorpusSet + DeclaredTopicScope
                     ↓
             same C-C scope authority
                     ↓
       ┌─────────────┴─────────────┐
AttemptSet absent             AttemptSet present
       ↓                            ↓
UNKNOWN learner evidence      ChemistryReasoningObservation
no negative diagnosis         → LearnerEvidenceLedger
neutral/conservative          → DiagnosticCase
PROBE_FIRST if needed         → LearnerStateSnapshot
```

## Shared contracts

C-E completes subject-independent V2 contracts under `Grade 9/V2/Shared/LearnerIntelligence/contracts/` for `LearnerEvidenceLedger`, `DiagnosticCase` and `LearnerStateSnapshot`. Chemistry adds only the subject-specific `ChemistryReasoningObservation` vocabulary and inference policy.

## Invariants

- `NO_ATTEMPT != CHEMISTRY_WEAK`.
- Assessment/source scope is identical whether attempts are absent or present.
- Correct upstream Chemistry reasoning remains credited if a later arithmetic, naming, transcription or inference step fails.
- One wrong answer cannot confirm a misconception.
- Low-confidence evidence creates a probe requirement, not a confident negative state.
- C-B diagnostic-use restrictions remain binding; defective/underdetermined/review-required evidence cannot punish the learner.
- Shared arithmetic execution cannot erase a demonstrated Chemistry model/rule/parse.
- C-E may nominate targeted probes but cannot choose teaching treatment; treatment belongs to C-F.

## Observation vocabulary

The registry includes all #267 required mappings, including formula/charge parsing, representation level, rule/condition/exception selection, conservation, species tracking, particle model, observation→claim reasoning, symbolic transcription, agent/spectator role confusion, arithmetic execution and verification.

## Pilot evidence

The fixture deliberately includes paired evidence such as correct formula parse + arithmetic slip, correct species tracking + agent-role inversion, correct particle model + symbolic transcription error, correct observation + overclaim, correct base rule + missed exception, an invalid/low-confidence item, and a low-confidence missing-verification observation.

CI reconstructs C-B, C-C and C-D authority, runs no-attempt and attempt-present branches on the same assessment scope, enforces all 10 required C-E falsifiers, tests the two-independent-evidence confirmation threshold, and checks deterministic replay.
