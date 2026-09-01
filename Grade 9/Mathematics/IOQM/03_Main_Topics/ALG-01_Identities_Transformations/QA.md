# ALG-01 - QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This QA record describes the repaired current source package and the regenerated student/teacher artifacts. Evidence-dependent classroom and psychometric gates remain separate from static promotion readiness.

## Current static gate table

| Gate | State | Evidence / disposition |
|---|---|---|
| G0 source authority | PASS_STATIC | Historical metadata rows use frozen `HBCSE_OFFICIAL` authority with validated paper/key URLs and stable IDs. |
| G1 dependency | PASS_STATIC_REPAIRED | Recognition #6, Practice #12/#20 and mastery #5 are domain-neutral polynomial/equivalence exercises and do not require downstream radical/principal-root doctrine. |
| G2 governing model | PASS_STATIC | `What form makes the requested target cheapest?` |
| G3 ownership/overlap | PASS_STATIC | Vieta/discriminant/general polynomial reduction, inequality attainment, and radical/log doctrine remain downstream. |
| G4 research-interface discipline | PASS_STATIC | Six per-microstream A-P interface files follow the mandatory naming/header contract; the consolidated interface file is index-only. |
| G5 lead integration | PASS_STATIC | One integrated learner book plus a topic-wide First-Step layer. |
| G6 deduplication | PASS_STATIC | Downstream canon is referenced rather than duplicated. |
| G7 decision contrasts | PASS_STATIC | factor/expand, substitution, symmetry, relation rewrite and equivalence boundaries are explicit. |
| G8 attempt-before-help / fading | PASS_STATIC | Learner support is descriptive and does not expose internal H/T labels. |
| G9 First-Step layer | PASS_STATIC | `03_First_Step_Reference.md` remains integrated. |
| G10 independent mastery | PASS_STATIC | Learner-facing title is `Independent Mixed Mastery Check`; H0 remains teacher/control metadata only. |
| G11 mathematics | PASS_STATIC | Historical anchors and repaired authored items remain consistent with the teacher key. |
| G12 source custody | PASS_STATIC | `source_authority` normalization is complete and author-created items remain distinct from PYQs. |
| G13 student-source hygiene | PASS_STATIC | Current learner sources and student PDF contain no H0-H3/T-level/Wave/PR/Issue/downstream-topic control labels. |
| G14 rendered artifact custody | PASS_CURRENT_BLOBS | Student and teacher PDFs were deterministically regenerated from the repaired learner/key snapshot at `05c6c9efba26a368111cae18e30cd0dacfc7d304`; the committed Git blobs exactly match the independently preflighted/rendered files. |
| G15 current-blob structural/visual QA | PASS | Student 9/9 pages and teacher 2/2 pages structurally preflighted, rendered and visually inspected with no clipping, overlap or broken glyphs. |
| G16 transfer quality | PASS_STATIC | Transfer intent remains present without learner-facing control taxonomy. |
| G17 ownership completeness | PASS_STATIC | meaning, trigger, boundary, first move, independent solve and transfer remain covered. |
| classroom timing/readability | NOT_RUN | evidence-dependent. |
| longitudinal retention/transfer | NOT_RUN | evidence-dependent. |
| psychometric calibration | NOT_RUN | evidence-dependent. |
| qualification probability / percentile calibration | NOT_RUN | evidence-dependent. |

## Dependency repair verification

The prior dependency inversion into the later radicals/logarithms chapter is removed:

- Recognition Lab #6: `(x+3)^2=(x-1)^2`, solved by equivalent difference-of-squares factorization;
- Practice #12: `(2x+3)^2=x^2`, giving `x=-3,-1` by equivalent factorization;
- Practice #20: `(x+6)^2-x^2=20`, giving `x=-4/3` by reversible algebraic rewriting;
- mastery #5: `(3x+4)^2=(x+2)^2`, giving `x=-1,-3/2` by equivalent factorization.

No principal-root rule, square-root domain restriction, or radical candidate-filter doctrine is needed.

## Metadata and interfaces

`Item_Metadata.csv` remains on the frozen 31-column program schema. Historical rows use exact `HBCSE_OFFICIAL`; repaired item metadata describes the current polynomial-equivalence items. Internal H0 identifiers are control metadata only.

Authoritative Wave-1 interfaces are the six separate A-P files under `Authoring/`; `Authoring/Microstream_Interfaces.md` is index/synopsis evidence only.

## Current render custody

### Student artifact

- path: `PDFs/ALG01_Student_Pack_v1.pdf`
- source snapshot: learner files at `05c6c9efba26a368111cae18e30cd0dacfc7d304`
- artifact commit: `18a20c83e3e656033763f02322b5c511d5cb9aae`
- Git blob SHA: `83927c63ff239dcfb0d3647ec0544da0960b3a80`
- SHA-256: `bfe50ceab8678edf7e8db64dd47655e5ed0e12e7c86aa8dbd9ea61045200f76f`
- bytes: 15676
- page size: US Letter
- pages: 9
- Practice inventory: 1-32 preserved in the practice section
- Independent mastery inventory: 1-16 preserved in the mastery section
- structural preflight: PASS
- forbidden learner-control label scan: PASS
- exact-artifact visual inspection: PASS 9/9

### Teacher artifact

- path: `PDFs/ALG01_Teacher_Key_v1.pdf`
- source: current `Teacher_Diagnostic_Key.md` from the repaired source snapshot
- artifact commit: `18a20c83e3e656033763f02322b5c511d5cb9aae`
- Git blob SHA: `e041d8c9f5952de6a91e73b68b3365c3850524c4`
- SHA-256: `6317edcb7008b29dae0ed8cdf1bc25f115fb34e98e37b6027afce27b2158c789`
- bytes: 4953
- page size: US Letter
- pages: 2
- structural preflight: PASS
- exact-artifact visual inspection: PASS 2/2

Teacher/control H-level and diagnostic codes are intentionally permitted in the teacher artifact and are not learner-facing leakage.

## Promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_PASS
WAVE4_MASTERY_PASS
WAVE5_STATIC_SOURCE_QA_PASS
WAVE6_STATIC_RENDER_QA_PASS
BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED
```

No classroom timing/readability, longitudinal retention, psychometric, qualification-probability or publication-readiness claim is made.
