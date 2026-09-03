# NT-03 - QA

Status: `CONTENT_ENRICHED_RENDER_RECERTIFICATION_PENDING`
Issue: `#134`

The current learner source now includes a consecutive-sum / odd-divisor transfer. The previous `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED` render certification remains historical evidence for its prior commit, but it does not certify the enriched current source state.

## Static gate table

| Gate | State | Evidence |
|---|---|---|
| G0 source authority | PASS_STATIC | 8 stable anchors unchanged and independently verified |
| G1 dependency | PASS_STATIC_UPDATED | NT-01 remains prerequisite; NT-04 consumes the new reconstruction bridge downstream |
| G2 governing model | PASS_STATIC_UPDATED | prime/divisor structure now also routes consecutive-sum existence through odd divisors |
| G3 ownership/overlap | PASS_STATIC_UPDATED | NT-03 owns odd-divisor/power-of-two existence criterion; NT-04 owns actual consecutive-sum reconstruction |
| G4-G12 prior static content gates | PASS_STATIC | microstreams, historical mathematics, metadata and source custody unchanged |
| consecutive-sum enrichment mathematics | PASS_STATIC | `2n=r(2a+r-1)` derivation, opposite-parity factors and power-of-two obstruction checked |
| teacher diagnostic synchronization | PASS_STATIC | `Teacher_Coverage_Enrichment_Addendum.md` added |
| previous student PDF | INVALIDATED_FOR_CURRENT_SOURCE | First-Step learner source changed |
| current render/preflight/page QA | PENDING | must be regenerated and inspected manually; no workflow is authorized |
| classroom timing/readability | NOT_RUN | evidence-dependent |
| retention / psychometrics / qualification calibration | NOT_RUN | evidence-dependent |

## Enrichment closure

The learner can now decide existence without brute force:

> A positive integer is a sum of at least two consecutive positive integers iff it has an odd divisor greater than 1, equivalently iff it is not a power of 2.

The learner is also told when to stop: if the question asks for actual lengths/start values/all representations, route to NT-04 rather than expanding NT-03 into a full Diophantine reconstruction chapter.

## Historical PDF custody retained but not current

The previously certified student PDF blob `7047d67be42f63fb9643f09188457f288fbffadb` remains in Git history. It must not be cited as current-source certification after the First-Step enrichment.

## Stable downstream interface

`Authoring/NT03_Stable_Divisor_PerfectPower_Interface_v1.md` now exports the consecutive-sum existence criterion while keeping reconstruction in NT-04.

## Promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_ENRICHED_PASS
WAVE4_MASTERY_UNCHANGED_PASS
WAVE5_STATIC_CONTENT_QA_PASS
WAVE6_CURRENT_RENDER_QA_PENDING
CONTENT_ENRICHED_RENDER_RECERTIFICATION_PENDING
```

No classroom, retention, psychometric, qualification-probability, percentile or publication-readiness claim is made.
