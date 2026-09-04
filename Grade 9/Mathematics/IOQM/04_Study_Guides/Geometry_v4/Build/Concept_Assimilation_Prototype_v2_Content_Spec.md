# Geometry five-concept assimilation prototype v2 - learner content spec

This is the build specification for the revised learner-facing prototype. It is intentionally not the full geometry guide.

## Governing learner chain
Every journey is authored through:
`understand -> recognize -> represent -> start -> execute -> check -> transfer`.

The learner surface leads with readable concept names. Internal IDs remain reviewer metadata only.

## Shared concept graph
Main spine:
`equal lengths -> equal angles -> AA/cyclic cues -> similarity -> length/area transfer`.

Cross-links:
- `power of a point -> equal tangents -> equal lengths`
- `similarity -> proportional products -> power of a point`
- `cevian classification -> median/Apollonius | angle-bisector ratio | altitude/right-triangle | arbitrary/Stewart`
- `tangent circles -> centres/radii -> right triangle -> metric transfer`

## Journey 1 - Equal lengths are angle data
Role: foundation.
Core representation: equal-side ticks -> equal opposite angles; equilateral variant; chained equalities.
Worked example: `AB=AC`, angle `A=100`, `D in BC`, `AD=BD` -> angle `DAC=60`.
Risk: matching equal sides to the wrong angles.
Check: execute both triangle angle sums.
Appendix A audit pointers: Q3, Q43-Q47; linked support Q2, Q6, Q8, Q51, Q61.

## Journey 2 - Classify the cevian before choosing the theorem
Role: method selection.
Decision representation:
- midpoint -> median -> Apollonius;
- equal vertex angles -> angle bisector -> side-ratio theorem;
- perpendicular -> altitude -> right-triangle metric;
- none -> arbitrary cevian -> Stewart.
Same-triangle comparison uses side lengths 10,14,12 to make the branch change visible.
Risk: inferring special status from the sketch or from a non-midpoint split.
Appendix A audit pointers: Q17, Q20, Q22, Q41, Q42.
Calibrated syllabus-side practice: 5-7-6 triangle with split 2/4, Stewart gives cevian 5.

## Journey 3 - Flatten tangent circles onto one baseline
Role: representation/visual.
Core transformation: erase curves after marking centres; retain centre distance `r+s`, vertical difference `s-r`, horizontal baseline gap `d`.
Derivation: `d^2+(s-r)^2=(r+s)^2`, hence `d=2*sqrt(rs)`.
Worked example: radii 9 and 16 -> exact 7-24-25 centre triangle -> touchpoint separation 24.
Risk: reusing the formula for opposite-side/internal-tangency configurations.
Appendix A audit pointers: Q21, Q28, Q29.

## Journey 4 - Prove similarity, then choose the right transfer
Role: transfer.
Core representation: proof cue -> correspondence -> target lane.
Linear target uses scale `k`; area target uses `k^2`.
Worked example: `DE || BC`, `AD=6`, `DB=4`, `BC=20`, area ABC=250 -> `DE=12`, area ADE=90.
Close contrast: equal area does not imply similarity; shared-altitude area ratios can sometimes be cheaper than proving similarity.
Appendix A audit pointers: Q37 primary; Q10 and Q52 linked.

## Journey 5 - Power of a point: choose the legal product
Role: legality/branch conditions.
Core representation: one owner point with three surfaces: chord-chord, secant-secant, tangent-secant.
Worked example: outside secant order `P-A-B`, `PA=3`, `AB=5`; whole distance `PB=8`; tangent gives `PT=2*sqrt(6)`.
Risk: using outside x inside rather than outside x whole; mixing owners/circles.
Concept link: standard power proofs compress a similarity argument; equal tangents can return to the equal-length angle engine.
Appendix A audit pointers: Q20, Q22, Q28 as secondary power routes.

## Final retrieval map
The prototype ends with a decision-first table:
`What do I see? -> What structure should I name? -> What do I write/draw first? -> What must I check?`

Part 0 remains excluded until learner self-report plus unaided recognition/first-move diagnostic evidence are available.
