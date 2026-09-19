# V3B research flexibility update — validation and boundaries

Owner-approved change: retain freedom to search, research, derive and improve teaching while enforcing minimum correctness, coverage, traceability and self-help criteria. Implementation basis is PR #364 at `26484b0d21d7d42ecac55e228ecb1b9629dbea43`; prework is recorded in EP-0010 before material edits.

## Behaviour changed

- A source-linked equation transformation can be rendered in a review draft with its reasoning and pending scientific-review notice. The frozen original is preserved. Silent changes and invalid transformation references still fail.
- A/B hints no longer have a fixed count. Optional guidance and complete explanatory answers support different tasks. Empty answer bodies/steps and missing subpart answers still fail.
- A missing or unsupported numerical evaluator permits a marked unverified draft candidate. The output counts transcription checks separately from supported-oracle checks, records oracle NONE and keeps learner release false.
- Existing supported numerical evaluators still reject incorrect answers even if an author requests expert review. No tolerance or Physics formula was changed.
- Research policy now distinguishes exploratory work, review drafts and learner-ready acceptance. Advisory similarity/layout scores alone do not stop the work. Scientific uncertainty remains an acceptance requirement for affected learner-ready claims.

## Executed verification

The focused suite contains 28 retained publication regression cases and 10 research-flexibility cases, with a shared test harness that contains no tests of its own. Test discovery executes 38 distinct cases; it does not inflate the count by inheriting the regression tests a second time. The final log is V3B-Research-Flexibility-Tests.txt.

Positive cases include source-preserving equation rearrangement, a one-hint question, a complete answer without separate hints, alternative guidance, and marked unverified numeric drafts. Negative cases retain wrong visible answer, empty solution, changed source/equation, missing Core/question/atom, bad figure binding, forged review status, stale baseline/runtime and omitted dependency checks. An author-supplied APPROVED label cannot clear a transformation's scientific review requirement.

The prior unsupported-family test is retained with a deliberately changed expectation: per owner direction, it now requires a draft with oracle NONE, one unverified transcription, fewer verified numerical answers, visible review notice and no learner release. It no longer expects all draft composition to be prohibited. This changes the approved workflow, not the expected Physics result or a numerical tolerance.

## Minimum-criteria interpretation

Complete required content and reliable source custody remain structural acceptance checks. Equation transformation metadata establishes traceability, not mathematical correctness. The existing host does not authenticate reviewers or establish semantic equivalence. Scientific correctness, Core purpose, appropriate depth, measured learner fit and final-medium usability still need their appropriate evidence before learner-ready acceptance.

The web-search policy governs authoring agents. The deterministic publisher remains offline; no claim is made that this patch implements web retrieval or a research scheduler. A single publication transaction can still fail on a defective required object; independent exploration/other packets may continue. Full accepted-packet integration and transitive authoring invalidation remain outstanding within the existing architecture work.

The earlier proof ZIP, test log and validation report are historical evidence and are preserved. The current code and new test log establish this revision. No V2, frozen Core1/Core2, Shared runtime or Physics calculator changes are made. No merge or learner release is authorized.
