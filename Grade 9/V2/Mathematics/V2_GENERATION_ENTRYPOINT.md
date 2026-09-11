# Mathematics V2 generation entrypoint — M-K cold start

This is the repository-only generation front door for Grade 9 Mathematics.

## Runtime inputs

Every generation begins from exactly:

1. `QuestionSet` — required.
2. `DeclaredTopicScope` — required.
3. `AttemptSet` — optional.

`LearnerStudyModel`, scope packages, problem-family maps, assessment reviews, historical products, issue/PR history, chat history, architect hints, and mature-reference artifacts are not runtime inputs.

## Authority order

The producer must execute the repository authorities in this order:

`M-A intake -> M-B item review -> M-C scope reconciliation -> M-D problem/reasoning semantics -> M-E learner evidence -> M-F LearnerStudyScope/LearnerStudyModel -> M-G Core1 authoring legality -> M-H representation semantics -> M-I Core2 transfer -> M-J coverage/longitudinal closure -> M-K cold-start custody`.

The machine-readable source of truth for those bindings is `GENERATION_AUTHORITY_MANIFEST.json`.

## No-attempt branch

When `AttemptSet` is absent:

- assessment scope is still derived completely;
- all learner readiness remains `UNKNOWN` unless repository evidence says otherwise;
- the producer must not invent a weakness or diagnosis;
- treatment is assessment-complete and learner-neutral;
- Core2 still contains every original source question with governed support and solution semantics.

## Attempt-present branch

When `AttemptSet` is present:

- assessment scope, canonical Mathematics, problem-family truth, and source-question custody must remain identical to the no-attempt run;
- the semantic-review stage may add learner evidence only from the supplied attempt;
- upstream correct modelling/geometry evidence must survive later execution errors;
- treatment/support may change; canonical answers, reasoning authority and assessment validity may not.

The deterministic repository fixture uses the public synthetic reviewed-observation fixture only as a **test oracle** for that semantic-review stage. It is not a producer-legal runtime input.

## Core1 fail-closed rule

M-G remains an authority boundary. Production Core1 authoring requires both:

- candidate PCK coverage for every capability whose treatment requires full teaching; and
- legitimate `PRODUCTION` PCK promotions backed by real human review.

M-K must report missing candidate coverage or missing promotion as an upstream blocker. It must never substitute the test-only promotion registry or fabricate human authorization.

A scope-complete `LearnerStudyModel` is therefore a valid **authoring-obligation candidate**, but it is not a mature Core1 study guide until M-G authoring legally materializes it.

## Core2 rule

M-I consumes the original `QuestionSet` as the transfer surface. It may be built while Core1 is blocked, but Core1 links remain planned and publication readiness remains false. Hints, reasoning routes, solutions, verification and representations must continue to come from their explicit repository authorities.

## Release boundary

M-K proves repository-only semantic reproducibility and authority custody. It does **not** by itself authorize release. Current production blockers must remain machine-visible, and M-L is still required for exact-candidate quality gates and authorized review.

Run the cold-start falsifiers with:

```bash
python 'Grade 9/V2/Mathematics/ColdStart/contracts/validate_contracts.py'
python 'Grade 9/V2/Mathematics/ColdStart/tests/test_math_cold_start.py'
```
