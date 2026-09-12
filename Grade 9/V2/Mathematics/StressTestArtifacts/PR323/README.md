# PR #323 Mathematics stress-test handoff

This directory is a reusable handoff from the external Grade 9 Mathematics stress test run against PR #323 (`M-UPGRADE: close PCK promotion gap, unify Math renderer, implement M-L quality gates`).

It exists so that a later agent can continue the consolidation work from the generated learner artifacts and machine-readable manifests instead of rediscovering the same learner-product failures from scratch.

## Important status

These are **stress-test / benchmark artifacts**, not repository production authority and not release evidence. PR #323 itself correctly remains provisional: publication-engineering success is not a subject, pedagogy, assessment, or visual-usability PASS.

The stress test established a stronger target contract for Core (1) and Core (2). The consolidated PR #323 review is comment `5646045040`. Earlier topic-specific comments remain useful as case-study evidence / negative fixtures.

## Scope and official question-bank authority

Only the relevant NCERT Class IX Mathematics Exemplar units were used as topic/question scope, with the NCERT Answers booklet used for answer validation where required:

- Number Systems: https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/mathematics/ieep201.pdf
- Polynomials: https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/mathematics/ieep202.pdf
- Coordinate Geometry: https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/mathematics/ieep203.pdf
- Linear Equation in Two Variables: https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/mathematics/ieep204.pdf
- Introduction to Euclid's Geometry: https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/mathematics/ieep205.pdf
- Lines & Angles: https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/mathematics/ieep206.pdf
- Surface Areas & Volumes: https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/mathematics/ieep213.pdf
- Answers: https://ncert.nic.in/pdf/publication/exemplarproblem/classIX/mathematics/ieep2an.pdf

NCERT source PDFs are intentionally **not vendored** in this handoff.

## Final cross-core architecture reached in the stress test

The final direction is a paired learning system, not two independent PDFs:

```
Frozen source corpus
-> atomic asks
-> concept / prerequisite graph
-> reasoning demands
-> Core1 teaching evidence
-> Core2 transfer
-> math-aware typesetting
-> adaptive layout
-> post-render semantic / visual QA
-> cross-core audit
```

### Core (1) instructional contract

For every substantial concept, the mature target is:

1. learner target;
2. prerequisite probe;
3. meaning / invariant;
4. best representation (equation, diagram, table, number line, counterexample, etc.);
5. reconstruction / derivation;
6. full worked model;
7. contrast or non-example;
8. misconception repair;
9. guided practice;
10. faded practice;
11. independent practice;
12. disguised transfer;
13. executable verification;
14. explicit bridge to the Core2 reasoning states the lesson prepares.

A compact formula/revision sheet is **not** sufficient Core1 evidence for difficult transfer.

### Core (2) contract

Core2 should be complete against a frozen source-corpus manifest, including atomic subparts, while the attempt surface remains answer-neutral. The target question object contains:

- full source-linked context / full choices when applicable;
- response-mode-specific workspace;
- H1 = invariant / clue;
- H2 = representation / method;
- H3 = first executable move;
- typed, variable-depth reasoning route (`INTERPRET`, `REPRESENT`/`MODEL`, `SETUP`, `EXECUTE`/`TRANSFORM`, `COMPARE`/`INFER`, `VERIFY` as applicable);
- exact Core1 teaching-evidence references for non-trivial route states;
- separate full-context worked solution;
- executable verification witness.

### Cross-core hard invariant

> Every non-trivial reasoning state required by Core2 must resolve to explicit teaching evidence in Core1.

A `CrossCoreBridgeManifest` should make unresolved route states machine-falsifiable.

## Answer-authority requirement added during consolidation

Every learner-facing question must have an answer/check path. This includes Core1 prerequisite, guided, faded, independent, transfer, misconception-repair and readiness questions.

Expected fail-closed conditions include:

- `LEARNER_QUESTION_WITHOUT_ANSWER_AUTHORITY`
- `ATOMIC_ASK_WITHOUT_SOLUTION`
- `OPEN_RESPONSE_WITHOUT_ACCEPTANCE_CRITERIA`
- `ANSWER_WITHOUT_VERIFICATION`
- `ATTEMPT_PAGE_ANSWER_LEAKAGE`

For proofs/explanations, the answer is a model proof / acceptance criteria, not merely "answers may vary". For multiple-valid-answer tasks, the admissible set/rule must be explicit.

## Publication / typography / diagram lessons

The stress test repeatedly demonstrated that structural JSON validity and an in-bounds PDF are insufficient. The mature path needs hard gates for:

- semantic math typesetting rather than ASCII flattening (`sqrt`, `^2`, etc.);
- true superscripts/subscripts, fractions, radicals, relations and aligned equations;
- portable math-aware fonts and missing-glyph checks;
- minimum readable physical font sizes;
- content-measured question/choice panels;
- measure-then-place pagination;
- component collision and clipping checks;
- response-mode-specific workspace (not generic lined boxes);
- no excessive unused panel area when larger readable content would fit;
- learner-visible source completeness after rendering (choices/subparts cannot be hidden by later panels);
- diagram correctness as mathematical correctness: axis direction/scale, point coordinates, angle-pair identity, theorem vs converse direction, labelled assumptions, 3-D surface selection, no answer-leaking attempt figures;
- one complete solution object per page where packing would compromise readability.

## Artifact status by topic

| Topic | Core1 status | Core2 status | Manifest | Next action |
|---|---|---|---|---|
| Number Systems | **Final cross-core v2**, answer-authority retrofit | **Final cross-core v1** | bridge v2 | Keep as number/algebra reference template |
| Polynomials | **Final cross-core v1** | **Final cross-core v1** | bridge v1 | Keep; use as symbolic-algebra / multipart template |
| Coordinate Geometry | pre-final stress-test v1 | pre-final stress-test v1 | stress-test v1 | Rebuild to final cross-core contract |
| Linear Equations in Two Variables | pre-final stress-test v1 | pre-final stress-test v1 | stress-test v1 | **Next planned rebuild** |
| Euclid's Geometry | **Final cross-core v2**, answer-authority retrofit | **Final cross-core v1** | bridge v2 | Keep as proof/provenance template |
| Lines & Angles | Core1 v2 is strong but not normalized to final cross-core/answer manifest | Core2 v1 | stress-test v1 | Retrofit bridge + answer-authority normalization |
| Surface Areas & Volumes | strong v1 concept decomposition, not final cross-core | Core2 v1 | stress-test v1 | Retrofit bridge + answer-authority normalization; enhance 3-D diagrams |

## Reusable artifact payload

`STATUS.json` is the compact machine-readable handoff and `ARTIFACT_SHA256.txt` binds the exact generated PDFs/manifests from the stress-test run.

The exact binary PDFs were generated outside the repository during the stress test. The GitHub connector used to create this handoff can write repository text objects but cannot directly import those local binary PDF bytes. Therefore this branch does **not** pretend that the original PDF binaries are checked in when they are not.

For agent continuity, the handoff records the exact filenames, versions, page/status facts, SHA-256 digests, source authorities, design contract, defect history, remaining sequence, and consolidated acceptance/falsifier set. Where a binary-capable client is available, copy the exact artifacts named in `ARTIFACT_SHA256.txt` and verify their hashes before treating them as the same benchmark outputs.

## How a new agent should continue

1. Read this README, `STATUS.json`, `CONSOLIDATED_REBUILD_PLAN.md`, and `ARTIFACT_SHA256.txt`.
2. Inspect Number Systems, Euclid and Polynomials first; these embody the latest cross-core contract.
3. Continue with **Linear Equations in Two Variables** before starting any new topic.
4. Build the Core2 demand/atomic-ask map first, then author Core1 backwards from those reasoning requirements.
5. Give every Core1 learner-facing question answer authority from the first pass.
6. Emit/update a CrossCoreBridgeManifest and require zero unresolved Core2 reasoning states.
7. Render representative easy, multipart, proof/model and Appendix pages; inspect typography, choice/subpart visibility, diagrams and workspace before marking a topic complete.
8. Then rebuild Coordinate Geometry, normalize Lines & Angles, normalize Surface Areas & Volumes, and finish with a seven-topic cross-core audit.

Do **not** restart from the original compact Core1 pattern; that was one of the central stress-test failures.

## PR #323 case-study trail

The consolidated normative comment is the most important starting point:

- Consolidated learner-product contract: PR #323 comment `5646045040`

Supporting case-study comments include:

- Number Systems learner-product / math-typesetting case study: `5645107609`
- Polynomials atomic coverage / symbolic semantics / response-mode case study: `5645333463`
- Coordinate Geometry spatial-semantic correctness: `5645422690`
- Linear Equations rendered-source fidelity / solution-set invariants: `5645525718`
- Euclid proof readability / collision-safe pagination: `5645644103`
- Core1 maturity / instructional decomposition: `5645773614` and `5645798217`

## Exclusions

The handoff deliberately excludes:

- NCERT source PDFs (official links above are the authority);
- user-provided mature-reference / benchmark PDFs;
- temporary per-page render dumps and transient scratch images;
- one-off early failed/rebuild PDFs superseded by the current listed artifact.

Those exclusions keep this a reusable handoff rather than a dump of temporary working state.
