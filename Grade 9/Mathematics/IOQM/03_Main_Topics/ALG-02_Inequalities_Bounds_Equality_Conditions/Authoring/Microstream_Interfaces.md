# ALG-02 - Wave-1 Research Interfaces

Authoring-only. These are interfaces/evidence for one integrated student book.

```yaml
main_topic_id: IOQM-G9-ALG-02
owner_role: RESEARCH_INTERFACE_ONLY
canonical_teaching_owner: IOQM-G9-ALG-02
status: READY_FOR_LEAD
source_cutoff: 2026-08-31
prerequisite_interfaces: [F0_G9_CORE, F1_IOQM_BRIDGE, IOQM-G9-ALG-01-v1]
```

## A. Scope boundary
Included: boundedness, direction, AM-GM, equality/attainment, justified Cauchy/Engel, square completion, feasibility, discrete filtering. Excluded: Vieta/discriminant/root canon (ALG-03).

## B. Learner-state model
`PRIOR_KNOWLEDGE:` order, nonnegative squares, routine algebra. `HALF_KNOWLEDGE:` remembers AM-GM formula. `MISSING_BRIDGE:` bound -> equality -> attainment -> domain.

## C. Governing invariant
An extremum claim is valid only when a bound in the required direction is combined with a feasible equality case in the actual domain.

## D. Representation inventory
- completed square -> quadratic lower/upper bound;
- positive sum/product -> AM-GM;
- reciprocal sum with fixed positive denominator sum -> Engel/Cauchy;
- continuous bound + discrete domain -> nearest/feasible candidate filter.

## E. Decision boundaries
Lower bound/minimum; upper bound/maximum; real/integer; inequality optimization/discriminant feasibility; theorem strength vs cheapest representation.

## F. Misconceptions
`R1` bound=minimum; `R2` equality not attainable; `R3` wrong direction; `R4` integer filter skipped; `R5` theorem-name hunting; `R6` ALG-03 canon imported.

## G. First-move cues
Read request/domain; test boundedness/direction; choose representation; write equality condition at the same time as the bound.

## H. H3->H0 fading
H3 execution; H2 representation; H1 structural clue; H0 unlabelled mixed optimization/feasibility/domain items.

## I. Validated anchors
`IOQM-2025-Q07` -> verified 46. `IOQM-2024-Q06` -> verified 06. No source conflict.

## J. Independent mathematical traces
2025-Q07: `s=x+y`; `(x-y)^2=2(s+1012)-s^2>=0`; largest integer s=46. 2024-Q06: power bounds collapse variables to a finite extreme set; verified answer 06.

## K. Contrast candidates
Bound/min; upper/max; real/integer; AM-GM/square completion; optimization/discriminant; attained/nonattained.

## L. Transfer candidates
T2 representation change; T3 domain change; T3 geometry; T3 number-theory filter; T4 cross-domain method selection.

## M. Mastery
16-item unlabelled H0 includes no-extremum and WHY-NOT items, not only routine equality cases.

## N. Dependencies
`REQUIRES:` frozen ALG-01 target/representation/equivalence interface. `EXPORTS:` bound/equality/attainment canon. No dependency on ALG-03 integrated prose.

## O. Lead integration
Use one router throughout; do not write separate AM-GM/Cauchy/square-completion mini-chapters disconnected from equality/attainment.

## P. QA
All authored answer paths independently recomputed; no ownership inversion found. Timing/retention/psychometrics NOT_RUN.
