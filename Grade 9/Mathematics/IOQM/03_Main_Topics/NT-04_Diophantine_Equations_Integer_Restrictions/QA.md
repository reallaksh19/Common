# QA - Diophantine Equations & Integer Restrictions

State: `CONTENT_ENRICHED_RENDER_RECERTIFICATION_PENDING`.
Issue: `#134`

The learner First-Step Reference and teacher diagnostic surface changed to consume the new Bézout/extended-Euclid and consecutive-sum bridges. The earlier `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED` PDF certification remains historical evidence for its prior commit, but it no longer certifies the current source state.

## Static gates
- G0 source authority: PASS
- G1 dependency: PASS_UPDATED — retrieve Bézout/linear-solvability from NT-01 and consecutive-sum existence structure from NT-03
- G2 governing model: PASS_UPDATED
- G3 ownership/overlap: PASS_UPDATED — NT-01 owns Euclidean/Bézout theorem machinery; NT-03 owns odd-divisor existence criterion; NT-04 owns solution-family/reconstruction/filtering
- G4 separate A-P microstream interfaces: PASS
- G5 integrated lead-authored student journey: PASS
- G6 deduplication: PASS_UPDATED
- G7 cross-boundary contrasts: PASS_UPDATED
- G8 attempt-before-help/fading architecture: PASS
- G9 integrated First-Step: PASS_ENRICHED
- G10 unlabelled first-attempt mastery: PASS_UNCHANGED
- G11 independent mathematics: PASS_STATIC for existing scored items; enrichment derivations independently checked
- G12 source custody: PASS
- G13 student-export hygiene: PASS_SOURCE
- G14 previous render authority: HISTORICAL_ONLY
- G15 current-source render/preflight/page-by-page visual inspection: PENDING
- G16 transfer quality: PASS_STATIC_UPDATED
- G17 six-question ownership: PASS_STATIC

## Enrichment mathematics

### Bézout retrieval -> NT-04 reconstruction
If `g=gcd(a,b)` and `(x0,y0)` solves `ax+by=c`, then all integer solutions are

`x=x0+(b/g)t`, `y=y0-(a/g)t`, `t in Z`.

The gcd-divisibility existence test is retrieved from NT-01; positivity/bounds/completeness are NT-04-owned.

### Consecutive-sum reconstruction
Retrieve from NT-03 that a positive integer is representable as at least two consecutive positive integers iff it is not a power of 2. NT-04 reconstructs via

`2n=r(2a+r-1)`, `a=((2n/r)-r+1)/2`,

then checks integrality, `a>=1`, `r>=2`, bounds and duplicates.

## Historical rendered artifact custody — no longer current-source certification
- prior `NT04_Student_Pack_v1.pdf`: Git blob `44a5f7481821753e203d2bede342072ca88f6b0d`
- prior `NT04_Teacher_Key_v1.pdf`: Git blob `7aae1dad12e3073a47eb617bc798f670d8ab0556`

These artifacts remain valid for the earlier source snapshot only. A fresh manual render/preflight/page inspection is required after this patch. No workflow is authorized.

## Evidence-dependent gates
Classroom timing/readability: NOT_RUN
Longitudinal retention: NOT_RUN
Psychometrics: NOT_RUN
Qualification probability: NOT_RUN
Percentile/pass-mark calibration: NOT_RUN
Publication approval: NOT_RUN
