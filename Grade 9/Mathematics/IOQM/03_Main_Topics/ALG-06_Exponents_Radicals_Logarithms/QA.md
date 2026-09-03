# ALG-06 — Production QA

Status: `BENCHMARK_PEDAGOGY_MATH_PASS_METADATA_PDF_PENDING`

| Gate | State | Evidence |
|---|---|---|
| issue #82 scope | PASS | exponent normalization, radicals/principal roots, conjugates, nested radicals, reversible transformations, logs as exponents and integer/domain filters retained |
| production-head compatibility | PASS | branch remains topic-only and based on `grade9-ioqm-90q-corpus-v1@4b30638f984076d41998dcd2c68f4b3830a7d59c` |
| ALG-01 provider | PASS_ACCEPTED | exact `ALG01_Stable_Prerequisite_Interface_v1.md` consumed; ALG-06 owns the radical/log domain doctrine that ALG-01 explicitly does not export |
| provider boundary | PASS | retrieves target-led transformation/equivalence discipline only; principal-root/log domain doctrine is taught here |
| source anchors | PASS_2 | `IOQM-2025-Q28`, `IOQM-2023-Q02` |
| correction overlay | PASS_REQUIRED | `IOQM-2025-Q28` uses exact nested radical `sqrt(x-sqrt(x+a))=sqrt(a)-y`; stale flattened classifier string is prohibited |
| historical answers | PASS | `91`, `54` independently re-derived in `Authoring/Independent_Math_and_Source_Audit.md` |
| historical figure dependency | PASS_NONE | neither promoted anchor requires a historical figure |
| microstream interfaces | PASS_7 | exponent normalization; radicals/conjugates; nested radicals; reversible transformations; logs as exponents; domain/integer filters; source audit |
| topic-lead integration | PASS | `Authoring/Lead_Integration_Map.md` |
| integrated Assimilation Book | PASS | domain/sign first; common-base routing; principal roots; conjugates; nested radicals; reversibility; logs as exponents; historical patterns |
| First-Step Reference | PASS | compact common-base/conjugate/squaring/log/domain router authored as compression after understanding |
| Recognition/First-Line Lab | PASS_16 | recognition and first mathematical line only |
| practice ladder | PASS_20 | learner-visible five-stage fade using internal F0→F4 comments; two validated historical anchors included |
| first mastery attempt | PASS | `06_H0_Mastery_Test.md` is unlabelled/unhinted |
| mastery items | PASS_12 | exponent, principal-root, conjugate, nested radical, reversible square, logarithm and integer-domain transfer |
| benchmark assimilation lab | PASS | `07_Benchmark_Assimilation_Lab.md` adds explicit RECONNECT diagnostic, error laboratory, ADOPT first-move check, changed-surface transfer and six-question assimilation test |
| Quadratics-v2 pedagogy comparison | PASS_ARCHITECTURE | `Authoring/Quadratics_v2_Benchmark_Comparison.md`; concept map, missing-link repair, contrast, attempt, fading, first move, transfer, source and independent-math gates pass |
| benchmark final artifact equivalence | PENDING | Quadratics benchmark requires rendered/preflighted artifact quality; ALG-06 PDFs are not yet produced |
| teacher key synchronization | PASS | Recognition 16, Practice 20 and Mastery 12 independently solved and synchronized |
| required contrasts | PASS | common base vs log; simple vs nested radical; conjugate vs square; reversible vs implication-only square; domain-first vs manipulation-first |
| learner control-plane scrub | PASS_STATIC | no learner-facing issue/PR/wave/agent/H-level control labels in student documents; F labels remain comments only |
| metadata schema | PENDING | frozen 31-column `Item_Metadata.csv` not yet committed for this package |
| answer verification flag | PENDING_METADATA | authored answers are independently checked in teacher key, but metadata rows are not yet frozen |
| canonical renderer | NOT_RUN | rendering script/package not yet created |
| student PDF preflight | NOT_RUN | no PDF rendered yet |
| student PDF visual inspection | NOT_RUN | no PDF rendered yet |
| teacher PDF custody | NOT_RUN | no teacher companion rendered yet |
| classroom timing/readability | NOT_RUN | evidence-dependent classroom gate |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification/pass-mark calibration | NOT_RUN | unsupported by static authoring |
| publication approval | NOT_RUN | separate human decision |

## Independent historical checks

### `IOQM-2025-Q28 = 91`
The exact controlled stem is nested. Principal-root signs are recorded before squaring. An independent irrationality/integer argument forces `y=0`; reversible squaring then yields `sqrt(x+a)=x-a`. With `t=x-a>=0`, `a=t(t-1)/2`; `t=14` gives 91 and `t=15` exceeds the bound. `91` is nonsquare.

### `IOQM-2023-Q02 = 54`
For `a,b>=2`, set `t=log_a b>0`; then `log_b a=1/t`. The equation gives `t=2` or `3`, so `b=a^2` or `a^3`. Bounds give 43 square pairs and 11 cube pairs, total 54.

## Authored-item static checks

- every radical equation in the key records sign/domain before accepting squared candidates;
- every logarithm item checks base/argument legality;
- common-base items do not introduce unnecessary logarithms;
- nested radical items preserve the nesting;
- H0 item answers independently checked, including `108` ordered pairs in M11 and maximal `a=45` in M12.

## Quadratics-v2 benchmark judgment

The canonical Grade 9 Quadratics benchmark was inspected as an internal comparator. Its required pedagogy features are now represented explicitly in ALG-06: partial-knowledge reconnection, missing-link repair, contrast/decision boundaries, attempt-before-hint, fading, first-move independence, changed-surface transfer, error diagnosis and the six-question assimilation test.

Therefore:

`BENCHMARK_PEDAGOGY_AND_MATH_ARCHITECTURE = PASS`.

However the benchmark's stronger static-readiness state also requires completed source/artifact custody and rendered PDF inspection. ALG-06 has not yet run those gates, so:

`BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED = NOT_YET`.

## Static disposition

`BENCHMARK_PEDAGOGY_MATH_PASS_METADATA_AND_RENDER_PENDING`

This is not a claim of classroom effectiveness, retention, psychometric calibration, qualification probability or publication readiness.
