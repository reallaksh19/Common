---
main_topic_id: IOQM-G9-NT-04
microstream_id: W3-D
microstream_title: Exact rational approximation and determinant gaps
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-04
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1, NT01_Stable_Prerequisite_Interface]
source_cutoff: 2026-09-02
---

# Exact rational approximation and determinant gaps - Research Interface

## A. Scope boundary
Included: exact comparison of rational distances by cross-products; positive determinant/gap variables; the local Farey-neighbour idea needed by the validated anchors. Excluded: a general continued-fraction algorithm, approximation of irrationals, or a broad treatment of Farey sequences.

## B. Learner-state model
`PRIOR_KNOWLEDGE:` compare fractions by cross multiplication.

`LIKELY_HALF_KNOWLEDGE:` learner converts to decimals to decide "closest" or searches denominators.

`MISSING_BRIDGES:` distance numerator is an integer; determinant gaps can be parameterized; close bounding fractions create positive integer gaps whose linear combination reconstructs numerator/denominator.

`OWNERSHIP_TARGET:` exact finite optimization for rational closeness under denominator/in-between constraints.

## C. Mathematical invariant / governing structure
**Invariant:** `CROSS-PRODUCT GAP IS AN INTEGER`: closeness becomes minimizing a small nonzero integer determinant divided by the denominator.

For target `p/q` and reduced `a/b`,
`|a/b-p/q|=|qa-pb|/(qb)`. The numerator is a nonzero integer when fractions differ, so it is at least 1. Under a denominator cap, determinant-1 candidates are strongest and the largest feasible denominator among them minimizes the distance.

For an interval `r/s < alpha/beta < p/q`, define positive gaps `u=s*alpha-r*beta` and `v=p*beta-q*alpha`. The two linear equations can often be inverted to write `alpha,beta` as linear combinations of u,v divided by the endpoint determinant. Positivity and integrality make denominator minimization exact.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| decimal-looking closeness | determinant integer | write `|qa-pb|/(qb)` | denominators positive | round decimals |
| fraction between rationals | two positive gaps | define cross-product gaps | strict inequalities | mediant guess without proof |
| determinant 1 congruence | denominator residue class | solve linear relation | reduced fraction check | test every denominator |
| denominator cap | finite extremal choice | maximize b among minimal gaps | determinant fixed | sample decimals |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| closest rational | determinant gap | decimals | Need an exact proof? | decimals feel intuitive |
| between neighbors | gap variables | mediant only | Is minimum denominator requested? | mediant often works |
| determinant 1 | solve congruence | enumerate a for each b | Can the linear equation constrain b directly? | nested loops are easy |
| irrational target | other tools | this finite rational method | Is the target rational? | "closest fraction" sounds identical |

## F. Misconception / diagnosis catalogue
`NT04-RAT-01`
- WRONG_MOVE: compare rounded decimals.
- WHY_TEMPTING: the fractions are close.
- MISSING_LINK_CLASS: REPRESENTATION.
- REPAIR_INVARIANT: exact cross-product gap.
- FALSIFIER_OR_CONTRAST: rounded distances can tie while exact distances differ.

`NT04-RAT-02`
- WRONG_MOVE: assert the mediant is minimal denominator without a determinant argument.
- WHY_TEMPTING: a memorized Farey fact.
- MISSING_LINK_CLASS: INVARIANT.
- REPAIR_INVARIANT: introduce positive integer gaps and reconstruct beta.
- FALSIFIER_OR_CONTRAST: non-neighbor endpoints need not behave identically.

`NT04-RAT-03`
- WRONG_MOVE: minimize `|qa-pb|` but ignore b in the denominator.
- WHY_TEMPTING: the integer numerator is striking.
- MISSING_LINK_CLASS: EXECUTION.
- REPAIR_INVARIANT: first minimize determinant magnitude, then maximize feasible b within that magnitude.
- FALSIFIER_OR_CONTRAST: determinant 1 at b=15 beats determinant 1 at b=13.

## G. First-move cues
- closest to p/q with denominator cap -> write `|qa-pb|/(qb)`.
- strictly between two close rationals -> define the two positive cross-product gaps.
- minimum denominator -> invert the gap equations before testing denominators.
- reduced fraction -> retain gcd check after reconstruction.

## H. H3 -> H0 fading plan
- **H3:** closest fraction to 2/5 with `b<=9`; show determinant table.
- **H2:** write the determinant objective but do not enumerate.
- **H1:** interval between two fractions; prompt only "make strict inequalities into positive integers."
- **H0:** changed endpoints; reconstruct least denominator independently.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| `IOQM-2025-Q11` | 2025/11 | CLEAN_OFFICIAL | primary | closest reduced fraction | no | FINAL_OFFICIAL_CORRECTED |
| `IOQM-2023-Q03` | 2023/03 | CLEAN_VALIDATED | primary | fraction between close rationals | no | EMBEDDED_KEY |

## J. Source-independent mathematical trace
**2025-Q11:** determinant magnitude is at least 1. For `4a-3b=-1`, b is 3 mod 4; largest `b<=15` is 15, giving a=11 and distance 1/60. The `+1` family peaks at b=13 with distance 1/52. Thus 11/15 is closest and `a+b=26`, matching the corrected final official key.

**2023-Q03:** set `u=37alpha-16beta>0`, `v=7beta-16alpha>0`. Solving gives `alpha=(7u+16v)/3`, `beta=(16u+37v)/3`. Integrality forces `u+v` divisible by 3. Minimum positive sum is 3: `(u,v)=(2,1)` gives beta=23; `(1,2)` gives beta=30. Answer 23.

## K. Contrast-pair candidates
1. decimal comparison vs exact determinant;
2. closest to target vs merely between two bounds;
3. determinant magnitude vs full distance;
4. mediant memory vs gap-based proof;
5. reduced-fraction condition vs unreduced candidate.

## L. Transfer candidates
- **T2:** lattice point distance to rational line `qa-pb=0`.
- **T2:** exact tie-breaking among candidate fractions.
- **T3:** gear-ratio context with bounded denominator.
- **T4:** geometry slope approximation where coordinates remain integers.

## M. Candidate mastery items
- Recognition: choose determinant gap over decimal conversion.
- First-line: write distance from `a/b` to `5/7`.
- Full solve: closest reduced fraction to 2/3 with `b<=20`, excluding 2/3.
- Full solve: least beta strictly between two supplied neighboring fractions.
- WHY-NOT: explain why "the mediant is between them" does not alone prove least denominator.
- Verification: check gcd and strict inequality after reconstructing alpha,beta.

## N. Dependency declarations
`REQUIRES:` cross multiplication; gcd/reduced fraction.

`BRIDGE_REQUIRES:` elementary linear elimination only.

`APPLIES:` W3-C denominator caps and W3-F completeness.

`EXPORTS:` determinant-gap representation and exact rational-closeness decision rule.

## O. Lead integration notes
This is not a continued-fractions chapter. Introduce the determinant as an integer error signal, connect both historical anchors, then return to the global finite-case router. Avoid unexplained theorem name-dropping when the gap proof is short.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE
