# Mathematics V2 — Core1 Instructional Authoring (M-G)

Tracking: #242. Consumes merged M-F / #241 and the Mathematics InstructionalKnowledge authority.

## Runtime boundary

```text
MathLearnerStudyModel
+ Math PCK Candidate Registry
+ Math PCK Promotion Registry
+ Math Instructional Authoring Profile
+ Math Core1 Scope-Completeness Policy
        ↓
Core1 authoring gate
        ↓
MathCore1StudyPlan
  └─ MathCore1Lesson[]
       └─ ProblemAuthoringPlan[]
```

The layer owns **how the frozen learner-conditioned StudyModel becomes a complete Core1 semantic teaching plan**. It does not own learner diagnosis, treatment selection, original-question transfer hints/solutions, renderer layout, or final PDF composition.

## Production gate

Full-teaching treatments require producer-legal promoted PCK:

```text
ACTIVE_STUDY
REPAIR_BEFORE
REPAIR_IN_UNIT
```

If a capability has no PCK candidate, generation fails with `PCK_COVERAGE_GAP`.
If a candidate exists but lacks valid human promotion, generation fails with `PCK_PROMOTION_REQUIRED`.

`VERIFY_ONLY` stays intentionally concise:

```text
ACTIVATE → VERIFY
```

`PROBE_FIRST` stays pre-explanatory:

```text
PROBE
```

No explanatory reteach is permitted before the decisive probe.

## Original assessment firewall

Original assessment questions remain scope/exam-demand evidence and Core2 transfer assets. Core1 problem plans must satisfy:

```text
must_be_new_instance = true
source_question_reuse = false
source_question_refs = []
problem_family_ref = canonical Math problem family
```

For full teaching the semantic sequence is:

```text
ANCHOR
→ REPRESENT
→ EXPLAIN
→ RECONSTRUCT
→ CONTRAST
→ WORKED
→ GUIDED
→ FADED
→ INDEPENDENT
→ VERIFY
→ TRANSFER
```

The authoring engine creates plans, not final prose or pages. Problem instances must later be authored from the bound problem-family semantics.

## Scope completeness

Exactly one Core1 lesson record is required for every capability plan in the M-F `LearnerStudyModel`. Learner evidence may change order/depth/treatment, but it may not delete assessment scope.

The production registry is currently empty because the ten PCK assets still require authorized human subject and pedagogy review. Therefore current production generation correctly fails closed rather than silently treating AI-authored drafts as producer-legal PCK.
