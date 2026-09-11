# Chemistry V2 — C-F Learner Study Scope and Model

This phase implements issue #268. It is the join between learner-independent Chemistry authority and optional learner evidence.

## Governing invariant

```text
SOURCE / ASSESSMENT SCOPE decides WHAT must be teachable.
LEARNER INTELLIGENCE decides ORDER / DEPTH / BRIDGE / TREATMENT / SUPPORT.
```

C-F therefore derives a learner-independent `ChemistryLearnerStudyScope` first. The same C-C scope bundle, source-obligation ledger, question/capability bindings and external-corpus classification must produce the same study-scope digest whether an AttemptSet is absent or present. C-E learner evidence is applied only after that boundary is frozen.

## Inputs

```text
C-C ChemistryAssessmentScope bundle
C-C SourceObligationLedger
C-C Question/Capability bindings
C-C ExternalCorpusClassification
C-D ChemistryReasoningSemantics
C-E LearnerStateSnapshot (AttemptSet absent or present)
C-F treatment policy
```

## Outputs

```text
ChemistryLearnerStudyScope
ChemistryLearnerStudyModel
per-capability longitudinal initialization
```

Each required capability preserves source, assessment and transfer traceability; prerequisites; representation levels and representation requirements; chemical entities where assessment evidence names them; source-authorized conditions/exceptions; conservation obligations; problem-family bindings; verification requirements; and future evidence obligations.

## Treatment states

```text
READY_VERIFY_ONLY
ACTIVE_STUDY
REPAIR_BEFORE
REPAIR_IN_UNIT
PROBE_FIRST
```

`READY_VERIFY_ONLY` is intentionally small: activation plus an independent check. `ACTIVE_STUDY` is the neutral no-attempt default for required scope. Repair states require learner evidence. `PROBE_FIRST` is used when evidence is mixed or an upstream C-E diagnostic case remains unresolved.

A demonstrated prerequisite may support a downstream repair while remaining `READY_VERIFY_ONLY`; the synthesis layer may not relabel that strength as weakness for sequencing convenience.

## Longitudinal initialization

A current success never closes later obligations. C-F initializes separate dimensions for acquisition, independent reconstruction, delayed retention, near/far transfer, mixed discrimination, representation translation, condition/exception discrimination, fluency and timed performance. Delayed retention and transfer remain open after current evidence.

## Scope safety

Only `ELIGIBLE_IN_SCOPE` source obligations, question/subpart records and external candidates may enter required coverage. Non-eligible external candidates remain explicitly excluded and cannot expand Core1. Learner weakness cannot remove any required source/assessment capability.

## Non-claims

C-F does not author final Core1 prose, worked examples, appendices, Chemistry teaching primitives, Core2 H1/H2/H3 wording or PDFs. It produces the study/treatment authority those later phases must consume.
