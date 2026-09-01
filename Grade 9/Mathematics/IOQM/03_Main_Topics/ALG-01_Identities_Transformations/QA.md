# ALG-01 - QA

Status: `STATIC_SOURCE_REPAIRED__RENDER_REVALIDATION_REQUIRED`

This file records the current branch after remediation of the independent review findings. Current-source gates are separated from stale render claims.

| Gate | State |
|---|---|
| G0 source authority | PASS_REPAIRED - historical metadata rows use exact frozen `HBCSE_OFFICIAL` authority with validated paper/key URLs and stable IDs |
| G1 dependency map before prose | PASS_REPAIRED - Lab #6, Practice #12/#20 and mastery #5 no longer require principal-root/radical-domain doctrine from downstream ALG-06 |
| G2 governing model | PASS - `What form makes the requested target cheapest?` |
| G3 canonical overlap ownership | PASS_REPAIRED - Vieta/discriminant/remainder stay ALG-03; inequality equality/attainment stays ALG-02; radical/log doctrine stays ALG-06 |
| G4 Wave-1 interfaces | PASS_REPAIRED - six per-microstream files follow the mandatory naming/header/A-P evidence contract |
| G5 single-lead integration | PASS |
| G6 deduplication | PASS |
| G7 decision contrasts | PASS |
| G8 attempt-before-help / internal fading control | PASS_STATIC - learner-facing mastery no longer uses H0 in its title |
| G9 one First-Step layer | PASS |
| G10 mastery | PASS_REPAIRED - learner-facing title is `Independent Mixed Mastery Check`; H0 remains only in teacher/control metadata |
| G11 independent mathematics | PASS_STATIC - historical anchor audit remains valid; repaired replacement items are keyed by reversible algebraic derivations |
| G12 source custody | PASS_REPAIRED - authority enum drift corrected |
| G13 student-source hygiene | PASS_REPAIRED - radical dependency examples and learner-facing transfer/H0 control labels removed from repaired sources |
| G14 one render authority | STALE_AFTER_SOURCE_CHANGE - committed PDFs predate the repaired learner/teacher sources |
| G15 page-by-page render QA | NOT_RUN_CURRENT_SOURCE - current-source PDFs must be regenerated and independently inspected |
| G16 transfer | PASS_STATIC_REPAIRED - learner-facing T2/T3/T4 labels removed while teacher metadata may retain control taxonomy |
| G17 six-question ownership | PASS_STATIC |
| classroom timing/readability | NOT_RUN |
| longitudinal retention/transfer | NOT_RUN |
| psychometric calibration | NOT_RUN |
| qualification probability | NOT_RUN |

## Dependency repair

The prior review correctly identified an inversion: ALG-01 deferred radical/principal-root doctrine to ALG-06 while learner items required it. Those items are now domain-neutral equivalence exercises:

- Recognition Lab #6: equality of polynomial squares, solved by difference-of-squares factorization;
- Practice #12: `(2x+3)^2=x^2`, solved by an equivalent factorization;
- Practice #20: `(x+6)^2-x^2=20`, solved by reversible algebraic rewriting;
- mastery #5: `(3x+4)^2=(x+2)^2`, solved by an equivalent factorization.

No square-root domain, principal-root condition, or radical candidate-filter doctrine is required by these repaired ALG-01 items.

## Metadata repair

`Item_Metadata.csv` remains on the frozen 31-column program schema. The four historical rows now use exact `HBCSE_OFFICIAL` authority rather than shortened `HBCSE`. Metadata for Practice #12/#20 and mastery #5 now describes the repaired polynomial-equivalence items rather than the superseded radical exercises. Internal H0 identifiers remain only as control metadata; learner disposition is unlabelled.

## Per-microstream interfaces

Current required authoring interfaces:

- `Authoring/IOQM-G9-ALG-01__W1-A__factor-expand__interface.md`
- `Authoring/IOQM-G9-ALG-01__W1-B__substitutions__interface.md`
- `Authoring/IOQM-G9-ALG-01__W1-C__symmetric-identities__interface.md`
- `Authoring/IOQM-G9-ALG-01__W1-D__reversible-transformations__interface.md`
- `Authoring/IOQM-G9-ALG-01__W1-E__hidden-relations-power-reduction__interface.md`
- `Authoring/IOQM-G9-ALG-01__W1-F__source-pyq-misconception-audit__interface.md`

The previous consolidated interface file is synopsis evidence only and is not used to claim schema conformance.

## Mathematical checkpoints for repaired items

- Practice #12: `(2x+3)^2-x^2=(x+3)(3x+3)=0`, giving `x=-3,-1`.
- Practice #20: `(x+6)^2-x^2=12x+36=20`, giving `x=-4/3`.
- Mastery #5: `(3x+4)^2-(x+2)^2=(2x+2)(4x+6)=0`, giving `x=-1,-3/2`.

These are equivalence-preserving algebraic transformations and do not create radical-domain obligations.

## Render custody

The repository currently contains an older student PDF, and QA previously claimed a teacher PDF that the independent re-review did not find at the reviewed head. Since the canonical learner and teacher sources have now changed again, no prior PDF hash/page inspection can certify this repaired source state.

Required before promotion:

1. regenerate the student PDF from the current canonical learner sources;
2. generate the teacher PDF if the architecture requires it and ensure it is committed;
3. record exact Git blob SHA, SHA-256 and page count for each current artifact;
4. run structural/leakage preflight;
5. independently inspect every page of the exact current blobs;
6. only then restore G14/G15 PASS claims.

## Promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE_REPAIRED
WAVE2_INTEGRATED_ASSIMILATION_SOURCE_REPAIRED
WAVE3_FIRST_STEP_PASS
WAVE4_MASTERY_SOURCE_PASS
WAVE5_STATIC_SOURCE_QA_PASS
WAVE6_CURRENT_RENDER_QA_NOT_RUN
NOT_READY__RENDER_REVALIDATION_REQUIRED
```

Classroom timing/readability, longitudinal retention, psychometrics and qualification probability remain `NOT_RUN`.
