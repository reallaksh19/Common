# V2-02 transfer plan from old Learner Intelligence PRs

Old PRs are migration evidence only. V2-02 starts from `main` and contains no runtime import or branch dependency on the old stack.

| Source | Disposition | Transfer | Do not transfer |
|---|---|---|---|
| PR #166 | ADAPT | evidence custody; observation/diagnosis/state separation; privacy/extraction confidence; qualitative state | old single LearnerStateView; Bxx projection |
| PR #167 | ADAPT INTERFACE ONLY | references to canonical capability/reasoning/error/probe IDs | Math/Physics/Chemistry reasoning truth and definitions |
| PR #168 | ADAPT + TEST_FIXTURE_ONLY | positive-evidence preservation; competing hypotheses; ambiguity→probe; one-error rule; no hidden-cause inference | old fixture as production evidence; direct topic-weakness labels |
| PR #169 | REJECT FOR V2-02 / MINE BOUNDARY ONLY | downstream consumes diagnosis rather than rediscovering it | BxxProjectionPolicy; legacy Core2 LearnerInput; old Core2 assumptions |
| PR #170 | ADAPT + REWRITE + TEST_FIXTURE_ONLY | canonical serialization/digests; deterministic reduction; recurrence candidate; referential integrity | underspecified time identity; old fixture registry as canonical truth |

V2 rewrites the old LearnerStateView into `ResearchLearnerView` and `PublicationPlanningView`, makes `as_of` and temporal policy mandatory state-identity inputs, and keeps canonical subject semantics outside Learner Intelligence.

A mechanism counts as transferred only after fresh V2 falsifiers pass. Old CI is source evidence, not V2 validation.
