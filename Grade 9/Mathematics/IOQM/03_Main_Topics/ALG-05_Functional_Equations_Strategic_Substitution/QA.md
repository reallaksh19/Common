# ALG-05 — Production QA

Status: `INTEGRATED_PACKAGE_STATIC_QA_PASS`

| Gate | State | Evidence |
|---|---|---|
| issue #81 scope | PASS | strategic special inputs, return-partner/involution structure, equation combinations, integer-domain functional equations and justified injectivity/surjectivity retained; formal vocabulary follows the behavior-first bridge |
| production-head compatibility | PASS | checked against `grade9-ioqm-90q-corpus-v1@4ed2377801e4fae7e1889fe7d36fa3f36b48f7ca`; intervening GEO-03 merge is outside the ALG-05 subtree |
| ALG-01 provider | PASS_ACCEPTED | exact `ALG01_Stable_Prerequisite_Interface_v1@fc685ff0a2e9bd67fbd6a920e730b7fff633404b` consumed |
| provider boundary | PASS | retrieves strategic-substitution/equivalence discipline only; function-specific strategy is taught in ALG-05 |
| ownership overlap | PASS | recurrence is treated only as a derived integer-domain consequence; general sequence canon is not re-owned |
| source anchors | PASS_2 | `IOQM-2025-Q14`, `IOQM-2024-Q16` |
| historical answers | PASS | `12`, `08` independently derived and checked against the frozen source/key custody |
| correction overlay | PASS_NOT_APPLICABLE | source map and audit show no correction overlay affecting either anchor |
| source coverage / PYQ map | PASS | `01_Source_Coverage_Map.md` |
| integrated Assimilation Book | PASS | domain first; structural-payoff substitutions; return-partner maps; equation combinations; recurrence/proof boundary; equal-output and every-target behavior taught before formal injective/surjective terminology |
| First-Step Reference | PASS | compact domain/strategic-input/partner/combine/proof router with behavior-first property language |
| Recognition/First-Line Lab | PASS_16 | first-move recognition and first-line writing without requiring full solutions; formal function vocabulary is not a prerequisite to the move |
| practice ladder | PASS_20 | five learner-visible stages with support fading and transfer; advanced property names are parenthetical after the behavior is stated |
| required contrasts | PASS | arbitrary vs strategic substitution; functional equation vs recurrence; formula guessing vs proof |
| first mastery attempt | PASS | Mixed Mastery Test is unlabelled and unhinted |
| mastery items | PASS_10 | numerical, proof, underdetermination, recurrence-boundary and candidate-verification items |
| teacher key synchronization | PASS | item mathematics and answer order unchanged by the wording bridge |
| independent math/source audit | PASS | `Authoring/Independent_Math_and_Source_Audit.md`; both historical anchors and authored item answers independently checked |
| metadata schema | PASS | frozen 31-column schema; 48 rows = 2 historical + 46 author-created |
| answer verification flag | PASS | every promoted metadata row records `answer_verified_independently=true` |
| separate microstream interfaces | PASS_6 | W1-A special values; W1-B symmetry/involution; W1-C equation combinations; W1-D integer-domain recursion; W1-E justified injectivity; W1-F source/PYQ/misconception audit |
| consolidated interface | PASS_INDEX_ONLY | `Authoring/ALG05_Microstream_Interface_Index.md` remains index-only |
| stable downstream interface | PASS | `Authoring/ALG05_Stable_Functional_Equation_Interface_v1.md` |
| learner prose control-plane scrub | PASS | no authoring-interface identifiers, source-control labels, teacher-key leakage or learner-facing H/T/wave/topic-control codes in final student PDF text |
| renderer custody | PASS | canonical FPDF rendering logic reproduced from `Authoring/render_alg05_pdfs.py` for the learner export |
| student PDF preflight | PASS | 6 pages, A4, openable, unencrypted, text-based |
| student PDF render inspection | PASS | all 6 pages rendered after the wording correction; no clipping, overlap, black squares or broken glyphs observed |
| teacher PDF preflight | PASS | unchanged 1-page custody companion remains openable, unencrypted and text-based; full solutions remain in `Teacher_Diagnostic_Key.md` |
| classroom timing/readability | NOT_RUN | evidence-dependent classroom gate |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification/pass-mark calibration | NOT_RUN | unsupported by this static package |
| publication approval | NOT_RUN | separate human decision |

## Teacher-review correction

The Grade-9 review on 2026-09-03 retained the underlying injectivity/surjectivity mathematics but moved the learner path to behavior-first language: first prove “equal outputs force equal inputs” or “construct an input for any target,” then attach the formal term. Return-partner substitution is likewise taught before the word “involution.” No answer changed.

## Independent historical checks

### `IOQM-2025-Q14`

Domain: integers. The zero substitutions are legal. Setting `m=0` forces `f(1)=2`; setting `n=0` then forces `f(m)=m+1` for every integer `m`. Therefore

`f(1)+...+f(N)=N(N+3)/2`.

At `N=12` the sum is 90 and at `N=13` it is 104, so the verified answer is `12`.

### `IOQM-2024-Q16`

Domain: reals. Replacing `x` by `3-x` is legal for every real `x` and returns to the original input after two applications. The paired equations eliminate the companion value and give

`7f(x)=x^2-24x+36`.

Hence `f(27)-f(25)=8`, matching the verified key `08`.

## PDF custody

Student:
- pages: `6`
- SHA-256: `201dc7dee9852da2636b44df478181a892e082109c5ba6856531b0111081ac68`
- Git blob SHA-1: `ba319c93127fe0598f6509f6ab44d87a8d882535`

Teacher companion (unchanged):
- pages: `1`
- SHA-256: `c16c9ae3b94082b499c1e4e8c43ad86e5a0f1b0b3268a081b3bbe23b58f16898`
- Git blob SHA-1: `b53af4c3f8599cf84166753b50904e9bb544a096`

## Static disposition

`STATIC_PRODUCTION_PACKAGE_PASS`

This is a static content/custody result. It is not a claim of classroom effectiveness, retention, psychometric calibration, qualification/pass-mark calibration or publication readiness. Those gates remain `NOT_RUN`.
