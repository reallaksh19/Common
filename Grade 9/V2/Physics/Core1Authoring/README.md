# Physics V2 — Core1 Instructional Authoring (P-G)

Tracking: #255. Consumes the merged P-F `PhysicsLearnerStudyModel`, P-D problem-family semantics, and Physics PCK candidate/promotion registries.

## Runtime boundary

```text
PhysicsLearnerStudyModel
+ Physics PCK Candidate Registry
+ Physics PCK Promotion Registry
+ Instructional Authoring Profile
+ Scope-Completeness Policy
+ Problem-Authoring Profile
        ↓
Physics Core1 authoring gate
        ↓
PhysicsCore1StudyPlan
  └─ PhysicsCore1Lesson[]
       └─ PhysicsProblemAuthoringPlan[]
```

P-G authors a semantic teaching plan, not final pages or rendered PDFs.

## Treatment-relative authoring

Full teaching (`ACTIVE_STUDY`, `REPAIR_BEFORE`, `REPAIR_IN_UNIT`) must realize:

```text
PHENOMENON
→ DEFINE_SYSTEM
→ CHOOSE_FRAME_SIGN
→ REPRESENT
→ NOTICE_DECISIVE_FEATURE
→ ORDINARY_LANGUAGE
→ CHECK_MODEL_VALIDITY
→ RECONSTRUCT
→ MINIMAL_CONTRAST
→ WORKED_REASONING
→ GUIDED_ATTEMPT
→ FADED_ATTEMPT
→ INDEPENDENT_ATTEMPT
→ PHYSICAL_VERIFICATION
→ TRANSFER
```

`READY_VERIFY_ONLY` is deliberately concise:

```text
ACTIVATE → VERIFY
```

`PROBE_FIRST` remains pre-explanatory:

```text
DIAGNOSTIC_PROBE
```

## Original-assessment firewall

Original assessment questions remain source/scope evidence and future Core2 transfer assets. Every full-teaching problem plan must be a **new instructional instance** bound to a canonical P-D problem family:

```text
must_be_new_instance = true
source_question_reuse = false
source_question_refs = []
surface_changes >= 2
```

Model-validity and verification obligations are inherited from P-F/P-D rather than reconstructed ad hoc.

## Promotion gate

`PRE_REVIEW` mode exists only to prove instructional sufficiency and deterministic authoring from candidate PCK. Its output is `PRE_REVIEW_ONLY`.

`PRODUCTION` mode requires human-promoted PCK. Since #255 explicitly leaves authorized human review out of scope, the checked-in promotion registry is empty and production generation correctly fails closed rather than asserting approval that does not exist.

## Release blockers

The executable P-G suite rejects all issue falsifiers: repair-memo-only Core1, source-question leakage, unpromoted PCK, family-less problem instances, missing reconstruction, naked equations, dropped model validity, invisible phase handoff, incomplete graph semantics, READY padding and number-only verification.
