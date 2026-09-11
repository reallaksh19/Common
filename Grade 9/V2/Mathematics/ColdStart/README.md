# Mathematics V2 M-K — repository-only cold start

Implements #246 under #235 and the cold-start requirement in #234.

## External runtime boundary

Production generation begins from only:

- `QuestionSet` — required;
- `DeclaredTopicScope` — required;
- `AttemptSet` — optional;
- repository-declared authorities from `../GENERATION_AUTHORITY_MANIFEST.json`.

`LearnerStudyModel`, assessment scope, item review, problem-family mapping, historical learner products, issue/PR history, chat history and mature-reference artifacts are derived or forbidden; they are not producer inputs.

## Run A / Run B proof

`tests/test_math_cold_start.py` executes the same Grade-9 assessment twice.

Run A has no attempt data. All learner readiness remains `UNKNOWN`, Study Synthesis stays assessment-scope complete, and treatment defaults to `ACTIVE_STUDY` rather than inventing weakness.

Run B uses the identical QuestionSet and DeclaredTopicScope plus the public synthetic AttemptSet. The deterministic CI run uses the reviewed-observation fixture only as a **test-only semantic-review oracle**. It is explicitly `producer_legal=false`; production attempt interpretation must execute or obtain the governed semantic-review stage from the supplied attempt.

The comparison requires identical assessment scope, canonical Mathematics truth and Core2 problem semantics, while learner state, treatment and learner support change where evidence warrants it.

## Evidence-localization invariants

The attempt fixture proves that:

- correct geometric modelling remains positive evidence even when later binomial expansion fails;
- correct downstream/upstream modelling remains positive evidence even when later arithmetic division fails;
- Q9 underdetermination cannot create negative learner evidence but can preserve positive relation-setup evidence;
- a copied coordinate in Q7 does not silently become a slope misconception.

## Core1 release boundary

M-K does not bypass M-G. The current production PCK registry has no fabricated promotions, and the pilot PCK candidate set does not cover every assessment-scope capability requiring full teaching. M-K therefore emits a scope-complete Core1 **authoring-obligation candidate** and machine-visible upstream blockers instead of manufacturing a releasable study guide.

Core2 may still be constructed as a complete semantic transfer candidate over all 14 original source questions. Until Core1 is legally materialized, its Core1 links remain planned and `publication_ready=false`.

## Validation

```bash
python 'Grade 9/V2/Mathematics/ColdStart/contracts/validate_contracts.py'
python 'Grade 9/V2/Mathematics/ColdStart/tests/test_math_cold_start.py'
```

Passing M-K proves repository-only semantic reproducibility and authority custody. It does not prove learning efficacy and does not replace M-L exact-candidate quality gates or authorized subject, pedagogy, assessment and visual review.
