# Learner Intelligence Architecture

**Status:** DRAFT / PHASE 1
**Depends on:** PR #160 two-core ownership boundary
**Does not modify:** Core (1) truth/evidence ownership or Core (2) publication ownership

## 1. Decision

Introduce a persistent **Learner Intelligence Plane** beside the two-core production pipeline.

```text
Canonical subject knowledge -> Core (1) Research -> ResearchBundle
                                      |
                                      |        Learner evidence
                                      |       / tests / attempts
                                      |              |
                                      |              v
                                      |      Learner Intelligence
                                      |  Evidence -> Observation ->
                                      |  Diagnostic Case -> State
                                      |              |
                                      +--------------+
                                                     v
                                              LearnerStateView
                                                     |
ResearchBundle + LearnerStateView + PublicationTarget -> Core (2)
                                                     |
                                                learner product
                                                     |
                                                new attempts
                                                     +--> evidence
```

The Learner Intelligence Plane is **not Core (3)**. Core (1) and Core (2) are content-production responsibilities. Learner Intelligence is mutable, longitudinal learner state.

## 2. Epistemic separation

Four authorities MUST remain distinct:

1. **Evidence** — what the learner actually wrote, selected, drew, said, or did.
2. **Observation** — a verified comparison between learner work and a reasoning contract.
3. **Diagnostic inference** — hypotheses explaining one or more observations.
4. **Learner state** — a reproducible snapshot used to decide what support is warranted.

Invariant:

```text
OBSERVATION != DIAGNOSIS != LEARNER STATE != TEACHING DECISION
```

A single ordinary wrong answer MUST NOT confirm a misconception.

## 3. Shared versus subject-specific architecture

The following are shared across Mathematics, Physics, Chemistry and future subjects:

```text
Attempt evidence
Reasoning observations
Diagnostic cases
Capability state
Learner state snapshot
Learner state view
Inference policy/versioning
Evidence and state custody
```

The meaning of a reasoning step is subject-specific and is supplied by a subject reasoning contract in Phase 2.

The system MUST NOT create separate Math/Physics/Chemistry learner engines. It uses one evidence/inference/state engine with subject-specific reasoning semantics.

## 4. Evidence model

`LearnerEvidenceLedger` is append-only. It records assessment sessions, artifacts and attempts. Evidence may come from handwritten papers, digital responses, oral transcripts, teacher-entered observations or system interactions.

Evidence records facts, not interpretations. It may preserve:

```text
question reference
response/result
work-step transcript or normalized representation
assistance used
artifact locator
extraction method and confidence
mark/correctness if independently known
```

Low-confidence extraction MUST remain low-confidence downstream unless independently verified.

## 5. Reasoning observation

A `ReasoningObservation` compares one or more learner work steps with an expected reasoning checkpoint and records the smallest defensible finding, for example:

```text
SUCCESS
OMISSION
INVALID_TRANSFORMATION
WRONG_MODEL_SELECTION
INCONSISTENT_STATE
REPRESENTATION_MISMATCH
CALCULATION_ERROR
CONDITION_VIOLATION
UNSUPPORTED_INFERENCE
VERIFICATION_MISSING
AMBIGUOUS
```

An observation MAY nominate candidate capability or error-signature references. It MUST NOT assert a confirmed learner misconception.

## 6. Diagnostic case

A `DiagnosticCase` groups observations around a target capability and carries competing hypotheses.

Each hypothesis preserves:

```text
supporting evidence
contradicting evidence
alternative explanations
confidence/evidence strength
status
probe requirement
recommended diagnostic probes
```

Allowed status:

```text
OPEN
SUSPECTED
SUPPORTED
REFUTED
RESOLVED
```

`SUPPORTED` is not equivalent to psychometric certainty.

## 7. Learner state

`LearnerStateSnapshot` is derived from:

```text
LearnerEvidenceLedger digest
+ canonical registry version
+ diagnostic policy version
```

The machine-derived portion MUST be reproducible from the same inputs.

Capability state is qualitative in v1:

```text
UNKNOWN
REPAIR_REQUIRED
DEVELOPING
READY
ROBUST
```

The snapshot preserves underlying evidence counts/classes instead of presenting unsupported numeric mastery probabilities.

## 8. LearnerStateView

Core (2) MUST NOT require the learner's complete longitudinal history.

A `LearnerStateView` is a scoped projection for one `ScopeGraph` and `PublicationTarget`. It may contain:

```text
relevant capability states
active diagnostic cases/hypotheses
required probes
known supports/constraints
Bxx projection if requested
source snapshot/digest
```

Bxx is a publication convenience/projection, not the canonical learner model.

## 9. Cross-subject capabilities

Subject capabilities may depend on reusable cross-subject capabilities such as:

```text
SHARED-SIGNED-NUMBER-EXECUTION
SHARED-SYMBOLIC-PRESERVE-MEANING
SHARED-PROPORTIONAL-REASONING
SHARED-QUANTITATIVE-VERIFICATION
```

This permits one upstream weakness to explain failures across several subject topics without collapsing subject-specific reasoning.

## 10. Privacy and custody

Learner evidence and state are downstream/private by default and MUST NOT alter ResearchBundle identity. Learner artifacts are referenced by stable private IDs and content digests; architecture fixtures MUST use anonymized or synthetic data.

## 11. Phase boundaries

Phase 1 freezes the shared epistemic/data boundary only.

Phase 2 adds subject reasoning contracts.
Phase 3 adds deterministic inference/state derivation and cross-subject answer-sheet fixtures.
Phase 4 defines narrow Core (1)/Core (2) integration contracts.

## 12. Phase 1 acceptance invariants

```text
RESEARCH_BUNDLE_HAS_NO_LEARNER_STATE = PASS
EVIDENCE_IS_APPEND_ONLY = PASS
OBSERVATION_NOT_DIAGNOSIS = PASS
ONE_ERROR_CANNOT_CONFIRM_MISCONCEPTION = PASS
LEARNER_STATE_IS_DERIVED = PASS
LEARNER_STATE_VIEW_IS_SCOPED = PASS
LOW_CONFIDENCE_EXTRACTION_CANNOT_SILENTLY_UPGRADE = PASS
BXX_IS_NOT_CANONICAL_STATE = PASS
```
