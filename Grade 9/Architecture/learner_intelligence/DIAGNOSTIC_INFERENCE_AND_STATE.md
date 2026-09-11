# Diagnostic Inference and Learner State

**Status:** DRAFT / PHASE 3
**Depends on:** Phase 1 shared evidence/state contracts and Phase 2 subject reasoning contracts

## 1. Purpose

Convert verified reasoning observations into cautious, reproducible learner-state evidence without overdiagnosing a learner from isolated wrong answers.

The required chain is:

```text
Attempt
-> ReasoningObservation
-> candidate hypotheses
-> evidence accumulation / contradiction
-> DiagnosticCase
-> CapabilityState
-> cross-capability root-cause analysis
-> LearnerStateSnapshot
-> scoped LearnerStateView
```

## 2. No direct wrong-answer-to-state shortcut

Forbidden:

```text
wrong final answer -> weak topic -> Bxx
```

Required:

```text
wrong final answer
-> preserve successful checkpoints
-> locate first unsupported/invalid checkpoint where possible
-> classify observation
-> consider competing explanations
-> request a probe when evidence is insufficient
```

## 3. Positive evidence is first-class

A failed item may contain demonstrated capabilities. Downstream failure MUST NOT erase upstream success.

Examples:

- correct coordinate-geometry modelling followed by a bad binomial expansion preserves modelling evidence;
- correct word-to-equation translation followed by an invalid symbolic transformation preserves modelling evidence;
- correct kinematic law selection followed by a state-continuity failure preserves law-selection evidence;
- correct gas-law relation followed by imprecise equality/proportionality manipulation preserves Chemistry concept evidence.

## 4. Evidence classes

State derivation distinguishes at least:

```text
INDEPENDENT_SUCCESS
INDEPENDENT_FAILURE
GUIDED_SUCCESS
GUIDED_FAILURE
TRANSFER_SUCCESS
TRANSFER_FAILURE
DELAYED_SUCCESS
DELAYED_FAILURE
AMBIGUOUS
```

Hinted success MUST NOT be counted as independent success.

## 5. Diagnostic inference policy

A hypothesis may be `SUSPECTED` from one high-quality observation but MUST NOT become `SUPPORTED` solely from one ordinary wrong response unless the evidence itself is a direct discriminating diagnostic probe with an explicit policy rule.

`SUPPORTED` normally requires one of:

1. recurrence across independent attempts with the same discriminating signature;
2. one error signature plus a targeted probe supporting the same hypothesis;
3. a subject-authorized deterministic discriminator whose semantics make alternatives implausible.

Contradicting evidence must be retained.

## 6. Ambiguity routing

When plausible causes remain materially different, the required action is:

```text
DIAGNOSTIC_PROBE_REQUIRED
```

not a confident label.

Typical competing explanations include:

```text
conceptual misconception
missing prerequisite
representation failure
procedural error
arithmetic slip
transcription/copying error
state-tracking failure
attention/execution slip
```

The system does not infer unobservable psychological causes such as working-memory limitation from answer sheets alone.

## 7. Cross-capability RCA

Root-cause prioritization uses the prerequisite graph rather than raw error counts.

A candidate upstream capability is prioritized when it:

- has recurring evidence;
- is a prerequisite of multiple failed downstream capabilities;
- is relevant to the current publication target;
- explains failures without contradicting demonstrated strengths.

The output is an intervention priority, not a psychometric probability.

## 8. Capability state

Phase 3 retains the v1 qualitative state model:

```text
UNKNOWN
REPAIR_REQUIRED
DEVELOPING
READY
ROBUST
```

State decisions carry confidence and underlying evidence summaries. They must be recomputable under a named diagnostic policy version.

## 9. Cross-subject answer-sheet acceptance fixture

The anonymized fixture in `fixtures/cross_subject_answer_sheet_acceptance.json` captures the architecture-level patterns observed in representative Grade 9 work.

It intentionally tests that the engine can preserve strengths while locating narrow failures across Mathematics, Physics and Chemistry.

Required conclusions include:

```text
Math geometry modelling may be demonstrated even when algebra later fails.
Math word-to-equation modelling may be demonstrated even when expression meaning later fails.
Physics formula/model selection may be demonstrated even when multi-phase state propagation fails.
Chemistry gas-law relationship may be demonstrated even when proportional algebra is imprecise.
```

Required non-conclusions include:

```text
one wrong answer proves a misconception
wrong Math final answer means whole chapter failure
wrong Physics final answer means formula knowledge absent
bad shared algebra means Chemistry concept absent
answer-sheet evidence alone proves a cognitive/psychological cause
```

## 10. Phase 3 release gates

```text
UPSTREAM_SUCCESS_PRESERVED_ON_DOWNSTREAM_FAILURE = PASS
ONE_ERROR_NOT_CONFIRMED_MISCONCEPTION = PASS
AMBIGUITY_ROUTES_TO_PROBE = PASS
HINTED_SUCCESS_NOT_INDEPENDENT = PASS
CROSS_SUBJECT_PREREQUISITE_RCA = PASS
NO_UNSUPPORTED_COGNITIVE_CAUSE_INFERENCE = PASS
ANSWER_SHEET_FALSIFIERS = PASS
```
