# Methodology

## Authority boundary

PHY-V2-07 owns only **last-step validation orchestration**. It does not own canonical Physics, learner diagnosis, Study Synthesis, Learning Design, publication realization, or human quality judgment.

Required order:

```text
exact candidate manifest
+ evidence-bound AI pre-review package
+ optional authorized human quality review
→ exact identity check
→ human quality gate check
→ reference access gate
→ later comparative validation
```

## Fail-closed rule

The reference path is not opened, hashed, parsed, or otherwise consumed until all of these are `PASS` under separate `AUTHORIZED_HUMAN_REVIEW` evidence bound to the exact candidate:

- `SUBJECT_CORRECTNESS`
- `PEDAGOGY_USABILITY`
- `VISUAL_USABILITY`

Publication-engineering success and AI pre-review cannot satisfy those gates.

## Current real acceptance case

The merged PHY-V2-06 candidate has publication-engineering PASS but the three human gates remain pending. CI therefore supplies a deliberately nonexistent comparator path. The run must still complete deterministically with `BLOCKED_HUMAN_QUALITY_GATES`, proving reference access was not attempted.

## Future unblocked state

After authorized human evidence exists, the same gate may transition to `READY_FOR_REFERENCE_COMPARISON` and bind a reference digest. That state is **not** a comparative PASS and remains `release_evidence_eligible = false`.

Actual comparison failure must produce downstream `VALIDATION_GAP`; it must not directly mutate canonical truth, learner state, StudyModel, LearningDesign, or the exact candidate.
