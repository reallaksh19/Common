# Math Core (1) gates

The shared object schemas are owned by `Grade 9/Architecture/contracts/v1/`. This file adds Mathematics-only semantic gates.

## READY_FOR_PUBLISH

- `project.subject == MATHEMATICS`.
- No Bxx, learner profile, support/hint level, appendix, page-layout or publication-target object exists in the ResearchBundle input.
- Every included concept has at least one VERIFIED material ResearchClaim.
- Every material ResearchClaim has at least one source reference and all refs resolve in SourceLedger.
- Every representation requirement is `subject=MATHEMATICS`, carries semantic requirements, and resolves both concept and research refs.
- Formal objects and worked-reasoning records resolve their ResearchClaim refs.
- No blocking unresolved item exists.
- No project candidate remains `RESEARCH_CANDIDATE` or `SUBJECT_AUTHORITY_REVIEW`.
- For competitive work, requested ExamDemand IDs resolve to attached profiles.
- For external-question closure, QuestionEvidenceLedger denominator is recomputed from rows and `REVIEW=0`.

## Not Core (1)

These are downstream Core (2): Bxx adaptation, H0/H1/H2/H3, lesson sequencing, Appendix A/B/C, badges, page composition, typography and learner PDF QA.
