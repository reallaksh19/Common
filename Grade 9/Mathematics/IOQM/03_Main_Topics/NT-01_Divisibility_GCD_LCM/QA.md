# NT-01 — QA

Status: `CONTENT_ENRICHED_RENDER_RECERTIFICATION_PENDING`
Issue: `#134`

The previous `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED` certification remains valid for its historical commit, but the current learner/teacher sources have changed to add the Bézout / extended-Euclid bridge. Therefore the previously certified PDF blobs must not be used as current-source certification.

## Current static gate table

| Gate | State | Evidence / disposition |
|---|---|---|
| G0 source authority | PASS_STATIC | historical anchors and verified answers unchanged |
| G1 dependency | PASS_STATIC | NT-02/NT-03 ownership boundaries remain intact |
| G2 governing model | PASS_STATIC_UPDATED | Euclidean reduction now distinguishes gcd-only work from extended-Euclid coefficient recovery |
| G3 ownership/overlap | PASS_HARDENED | Euclid's Lemma and Bézout/extended Euclid are NT-01-owned; NT-04 owns full Diophantine reconstruction |
| G4-G12 prior static content gates | PASS_STATIC | existing microstreams, anchor math and source custody unchanged |
| Bézout enrichment mathematics | PASS_STATIC | constructive back-substitution, solvability iff `gcd(a,b)|c`, scaling, and closest-rational boundary checked |
| teacher diagnostic synchronization | PASS_STATIC | `Teacher_Coverage_Hardening_Addendum.md` updated |
| previous student PDF | INVALIDATED_FOR_CURRENT_SOURCE | First-Step learner source changed |
| previous teacher PDF | INVALIDATED_FOR_CURRENT_SOURCE | teacher addendum changed |
| current render/preflight/page QA | PENDING | must be regenerated and inspected manually; no workflow is authorized |
| classroom timing/readability | NOT_RUN | evidence-dependent |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometrics | NOT_RUN | evidence-dependent |
| qualification probability / percentile calibration | NOT_RUN | evidence-dependent |

## Enrichment closure

The learner now distinguishes:

- Euclidean algorithm: compute `gcd(a,b)`;
- extended Euclid: also recover `x,y` with `ax+by=gcd(a,b)`;
- linear-Diophantine solvability: `ax+by=c` is integer-solvable iff `gcd(a,b)|c`;
- full solution-family/positivity/bound filtering: route to NT-04;
- closest-rational determinant logic: Bézout gives a possible minimal nonzero linear combination, but admissible bounds still decide the actual closest candidate.

## Historical PDF custody retained but not current

The previously certified student blob `f2f64c1bf9ad0c6187ed611f200e763b8ba44e56` and teacher blob `872fdba537d0d2c06bd8908ebbb43fc2a7a6bad1` remain in Git history. They certify the prior Euclid/Euler hardening revision only, not the current Bézout-enriched source state.

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

No classroom, retention, psychometric, qualification/pass-mark or publication-readiness claim is made.
