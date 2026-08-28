# 2019 Bhaskara Preliminary — Mathematical Qualification v1

## Authority boundary

The Cheenta page used at initial ingestion is truncated after Q25. The complete 30-question structure, missing Q14/Q15 text, Q20 bonus disposition, Q26–Q30, and answer/solution evidence were recovered from an independent 2019 Junior solution PDF hosted by Resonance and matching reproductions.

`P1_VERIFIED_FAITHFUL_REPRODUCTION` here means independently matched reproduction evidence. It does **not** mean an AMTI-hosted original (`P0`).

Where a problem depends on a supplied figure, a recovered answer/solution is **not** treated as custody of the original figure. Such items remain image-gated for student-facing canonical use.

Profile columns use the local Preliminary screen:

`C/R/F/S/A/H/K/B/T/P = conceptual / recognition / first-move / reasoning-steps / algebra / hidden-structure / constraints-cases / calculation-burden / trap-density / time-pressure` on 0–10.

## Qualified question ledger

| ID | Recovered / derived answer | Best first move | Minimum expert path | Disposition | Profile; speed |
|---|---|---|---|---|---|
| Q01 | key D | Write `ABCABC = 1001·ABC = 7·11·13·ABC` | divisibility by 13 is automatic; reduce to the stated digit constraints and count valid three-digit `ABC` values | scored; independently matched | `4/5/4/3/3/5/4/3/4/4`; FAST_IF_RECOGNIZED |
| Q02 | key D | Express the two medians as vectors / use Apollonius twice | impose perpendicularity of median vectors and eliminate the median lengths to obtain the required side relation | scored; independently matched | `6/7/6/5/4/7/3/4/6/6`; MULTISTEP |
| Q03 | key B | Use equal-side data before testing circle/tangency properties | derive angle/supplement relations from the two isosceles triangles; classify the quadrilateral rather than calculating coordinates | scored; independently matched | `6/6/5/5/3/6/4/3/6/5`; MULTISTEP |
| Q04 | key C | Enumerate integer representations of the fixed sum of two squares | recover possible integer side pairs; convert each to cube volume and apply the requested aggregation | scored; independently matched | `5/5/4/5/3/5/6/5/5/5`; CASE_HEAVY |
| Q05 | key B | Use `d1²+d2²=4s²` for a rhombus | reduce optimization of diagonal sum to a fixed sum-of-squares bound plus geometric admissibility | scored; independently matched | `6/6/5/4/4/6/4/3/6/5`; FAST_IF_RECOGNIZED |
| Q06 | key D | Work with prefix sums modulo 11 | every qualifying consecutive block is equality of two prefix residues; count equal-residue prefix pairs | scored; independently matched | `7/8/7/6/4/8/5/4/6/7`; FAST_IF_RECOGNIZED |
| Q07 | key D | Recognize the subset-product expansion | sum of products over non-empty subsets of `{1,1/2,...}` equals `∏(1+a_i)-1`; telescope/simplify the product | scored; independently matched | `7/8/7/5/5/8/3/3/6/7`; FAST_IF_RECOGNIZED |
| Q08 | key B | Reduce modulo `x²-1` using `x²≡1` | collapse every even/odd power to constant/linear terms and read the remainder | scored; independently matched | `4/5/4/3/4/5/2/2/4/4`; FAST_IF_RECOGNIZED |
| Q09 | key B | Classify vertex triples by geometric type before counting | partition box-vertex triples into acute/right/obtuse configurations; count only acute class | scored; solution matched; figure/model dependent | `7/7/6/7/3/7/6/6/6/7`; CASE_HEAVY |
| Q10 | key D | Analyze the borrow pattern, not the full decimal subtraction | identify the repeating borrow block; convert the resulting digit pattern directly to digit sum | scored; independently matched | `5/7/6/4/2/7/3/4/6/6`; FAST_IF_RECOGNIZED |
| Q11 | key D | Clear denominators and switch to sum/product variables | obtain a symmetric integer relation; use positivity, bounds and divisibility to restrict possible pairs | scored; independently matched | `7/7/6/6/6/7/7/5/6/7`; CASE_HEAVY |
| Q12 | key C | Figure required before canonical first move can be frozen | recovered solution counts connected three-stamp configurations on the supplied 16-stamp figure | scored; `IMAGE_REQUIRED_FOR_STUDENT_ANCHOR` | provisional only; do not psychometrically score until figure custody |
| Q13 | key D | Let one candidate's votes be the base unknown | translate each winning margin into linear offsets; use total votes to recover the base and all candidates | scored; independently matched | `4/4/4/4/4/3/3/3/4/4`; MULTISTEP |
| Q14 | `126` impossible (A) | Express total score by counts of the allowed scoring outcomes | derive congruence/attainability restrictions under the recovered scoring rule; test the four listed totals | scored; source stem recovered by independent match | `5/6/5/5/4/6/6/4/6/5`; CASE_HEAVY |
| Q15 | maximum `133` (C) | Recognize the expression as an expansion of a shifted product | write the recovered terminal term as `T×I`; transform to a product under fixed integer sum; balance factors to maximize | scored; transcription resolved (`I`, not `1`) | `7/8/7/6/6/8/6/4/7/7`; FAST_IF_RECOGNIZED |
| Q16 | `435` | Encode the number by place value immediately | translate quotient/remainder/digit condition into a base-10 equation and solve the resulting digit constraints | scored; independently matched | `4/5/4/4/4/5/5/3/5/4`; MULTISTEP |
| Q17 | `156` | Let `s` be the digit sum and write `N=s²+s` | combine the quadratic expression with the base-10 digit-sum condition; restrict feasible `s` and verify | scored; independently matched | `6/7/6/6/5/7/7/5/6/6`; CASE_HEAVY |
| Q18 | `16` | Use the anti-magic consecutive-total constraint before filling cells | propagate row/column/diagonal totals through the supplied square; solve the required cell | scored; answer/solution recovered; `IMAGE_REQUIRED_FOR_STUDENT_ANCHOR` | provisional until figure custody |
| Q19 | `80` | Separate escalator speed from walking speed | form two time/step equations for the same escalator length; eliminate walking rate and recover the fixed number of steps | scored; independently matched | `5/5/5/5/4/5/3/4/5/5`; MULTISTEP |
| Q20 | `62` | Model the row counts with triangular numbers / their differences | convert the tower condition to a factorable triangular-number relation and maximize the admissible row count | **BONUS**; independently recovered | not included in ordinary scored recurrence/difficulty |
| Q21 | `8/9` | Join circle centers and translate tangencies into center distances | use external/internal tangency equations plus the condition that one circle passes through the outer center; solve radius ratio | scored; answer recovered; `IMAGE_REQUIRED_FOR_STUDENT_ANCHOR` | provisional until figure custody |
| Q22 | `6` | Split `A(x)^{B(x)}=1` into exceptional cases | enumerate exponent zero, base `1`, and base `-1` with parity/domain conditions; count distinct real/integer solutions as required | scored; independently matched | `6/7/6/6/6/6/8/5/8/6`; CASE_HEAVY |
| Q23 | `127` | Model king moves as state transitions / constrained paths | count exact-length paths on the supplied grid using recurrence or state enumeration | scored; answer/solution recovered; `IMAGE_REQUIRED_FOR_STUDENT_ANCHOR` | provisional until grid custody |
| Q24 | `20°` | Mark all equal lengths first | chain isosceles/equilateral angle consequences in the supplied figure until the target angle is forced | scored; answer/solution recovered; `IMAGE_REQUIRED_FOR_STUDENT_ANCHOR` | provisional until figure custody |
| Q25 | `89` | Replace the symmetric high-degree system by `s=x+y`, `p=xy` / suitable ratio | factor/reduce the equations to a low-degree relation and evaluate the requested symmetric target without solving both variables naively | scored; independently matched | `8/8/7/7/8/8/5/5/7/8`; MULTISTEP |
| Q26 | `97` | Reduce `2019` modulo a candidate prime and use multiplicative order | if `p | 2019^8+1`, then `2019^16≡1` but `2019^8≠1`; order forces a strong congruence on odd prime divisors; test the least admissible prime | scored; independently matched; high-ceiling NT | `8/9/8/7/5/9/6/4/8/8`; FAST_IF_RECOGNIZED |
| Q27 | `25` | Factor `a²-b²=(a-b)(a+b)` and use the bounds | translate divisibility by `100c` into factor/residue restrictions; enumerate admissible bounded pairs without brute-forcing all squares | scored; independently matched | `7/7/6/7/5/7/8/6/7/7`; CASE_HEAVY |
| Q28 | `122` | Recognize balanced ternary uniqueness | signed powers of 3 give unique coefficients in `{-1,0,1}`; translate non-negativity and requested sign-count condition into coefficient cases | scored; independently matched; high-ceiling counting/NT | `8/9/8/7/5/9/8/5/8/8`; FAST_IF_RECOGNIZED |
| Q29 | `12` | Substitute equal indices to get a doubling recurrence | from `a_{m+n}=a_m+a_n+mn`, set useful pairs such as `(1,1),(2,2),(4,4)` and climb to `a8` | scored; independently matched | `5/5/4/4/4/5/2/3/4/4`; DIRECT |
| Q30 | `61` | Interpret coefficient as number of exponent pairs | coefficient of `x^90` in two finite geometric sums equals count of integer pairs `(i,j)` in their allowed ranges with `i+j=90` | scored; independently matched | `6/8/7/5/3/8/5/3/6/7`; FAST_IF_RECOGNIZED |

## Qualification counts

- complete paper slots recovered: **30**
- ordinary scored items: **29**
- recovered bonus items: **1** (`Q20`)
- figure-dependent items with answer/solution but not original-figure custody: `Q12, Q18, Q21, Q23, Q24` (Q09 also benefits from the original model/figure for clean publication)
- source truncation resolved: Q26–Q30
- source text defects resolved: Q14, Q15

## 2019 curriculum promotions

2019 materially expands the Preliminary target beyond routine textbook exercises:

1. **modular structure at two levels** — accessible prefix-residue thinking (Q06) and high-ceiling multiplicative-order filtering (Q26);
2. **combinatorial modeling beyond `nPr/nCr`** — subset products (Q07), geometric configurations (Q09/Q12), exact-move paths (Q23), balanced ternary (Q28), coefficient counting (Q30);
3. **transform-first algebra** — polynomial reduction (Q08), symmetric reduction (Q11/Q25), exceptional power cases (Q22);
4. **functional/sequence reasoning** — Q29 is a compact recurrence-first-move anchor;
5. **diagram recognition remains a separate custody problem** — recovered solutions do not authorize re-drawing unseen figures as if exact.

These promotions are evidence for concept/first-step design. They are not yet final recurrence weights until 2023–2025 receive the same solution-qualified treatment.
