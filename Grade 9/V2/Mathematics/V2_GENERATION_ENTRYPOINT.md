# Mathematics V2 generation entrypoint — M-K cold start + governed learner-product handoff

This is the repository-only generation front door for Grade 9 Mathematics.

## Runtime inputs

Every generation begins from exactly:

1. `QuestionSet` — required.
2. `DeclaredTopicScope` — required.
3. `AttemptSet` — optional.

`LearnerStudyModel`, scope packages, problem-family maps, assessment reviews, historical products, issue/PR history, chat history, architect hints, and mature-reference artifacts are not runtime inputs.

## Authority order

The semantic producer must execute repository authorities in this order:

`M-A intake -> M-B item review -> M-C scope reconciliation -> M-D problem/reasoning semantics -> M-E learner evidence -> M-F LearnerStudyScope/LearnerStudyModel -> M-G Core1 authoring legality -> M-H representation semantics -> M-I Core2 transfer -> M-J coverage/longitudinal closure -> M-K cold-start custody`.

The machine-readable source of truth for those bindings is `GENERATION_AUTHORITY_MANIFEST.json`.

## Learner-product handoff after M-K

Core (1A) and Core (2A) are downstream learner-product stages. Future agents must not reconstruct their workflow from chat history or PR discussion.

Their canonical authority is:

`Grade 9/V2/Mathematics/LearnerProduct/EXECUTION_CONTRACT.md`

The learner-product sequence is contractually ordered as:

`LP-00 input binding -> LP-01 Core1A bucket synthesis -> LP-02 representation sequence -> LP-03 Core1A realization -> LP-04 Core2↔Core1A mapping -> LP-05 source Core2A realization -> LP-06 challenge selection -> LP-07 challenge generation -> LP-08 mathematical verification -> LP-09 taught-scope verification -> LP-10 inline citations -> LP-11/14 staged help/working/check -> LP-15 render -> LP-16 visual preflight -> LP-17 final audit`.

The canonical run contract is:

`LearnerProduct/contracts/math-learner-product-run.schema.json`

The canonical execution-policy bindings are:

- `MATH-CORE1A-EXECUTION-v1`
- `MATH-CORE2A-EXECUTION-v1`
- `MATH-LEARNER-LANGUAGE-v1`
- `MATH-QUESTION-CITATION-v1`
- `MATH-COMPETITIVE-CHALLENGE-v1`

Lower learner-product layers may not override source integrity, M-E/M-F learner state, Core1 authority, or Core2 source-transfer authority.

## No-attempt branch

When `AttemptSet` is absent:

- assessment scope is still derived completely;
- all learner readiness remains `UNKNOWN` unless repository evidence says otherwise;
- the producer must not invent a weakness or diagnosis;
- treatment is assessment-complete and learner-neutral;
- Core2 still contains every original source question with governed support and solution semantics.

Core1A/Core2A must consume this no-attempt state as-is; they may not invent labels such as `FOUNDATION`, `PARTIAL`, or a percentage-based learner estimate.

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

Core2A may add fresh challenge questions only in its generated-challenge lane. Such questions cannot replace source Core2 items and cannot require untaught mathematics.

## Learner-product stop rule

After M-K, stop rather than improvise when:

- required learner state is unavailable;
- Core1/Core1A/Core2 bindings conflict;
- a teaching-bucket invariant is ungrounded;
- a Core2 hint cannot map to taught content;
- a challenge requires untaught mathematics;
- a generated question has not been independently solved;
- exact official provenance cannot be verified for an official attribution;
- citation role is unclear.

## Release boundary

M-K proves repository-only semantic reproducibility and authority custody. It does **not** by itself authorize release. Core1A/Core2A improve learner realization but cannot upgrade provisional PCK, alter learner diagnosis, change source-question validity, or bypass M-L/human gates.

Run the cold-start falsifiers with:

```bash
python 'Grade 9/V2/Mathematics/ColdStart/contracts/validate_contracts.py'
python 'Grade 9/V2/Mathematics/ColdStart/tests/test_math_cold_start.py'
```

Validate a learner-product run contract with:

```bash
python 'Grade 9/V2/Mathematics/LearnerProduct/engine/run_learner_product.py' \
  --run-manifest /path/to/run.json \
  --out-dir /tmp/math-learner-product \
  --validate-only
```

Until all learner-product stage adapters are executable, a non-validate-only invocation must fail closed rather than silently skip stages.
