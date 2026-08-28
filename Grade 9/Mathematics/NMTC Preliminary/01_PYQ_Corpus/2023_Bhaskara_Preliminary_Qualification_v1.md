# 2023 Bhaskara Preliminary — Mathematical Qualification v1

## Source authority

Primary qualification evidence:

- Resonance-hosted `NMTC/2023/Stage-1/solutions/junior.pdf`, carrying the Association of Mathematics Teachers of India Bhaskara Screening heading, complete Q1–Q30 answer key, and worked solutions;
- Resonance-hosted Junior answer-key PDF;
- Cheenta reproduction used for searchable question text and figure locators.

These are strong independent reproductions/solution evidence. They are not silently promoted to an AMTI-hosted `P0` original.

The complete key records:

- Q5 as `*` rather than a normal option;
- Q8 as `Bonus`;
- Q16 as `Bonus`;
- Q17 as `∞`.

Those dispositions override seed-stage guesses.

## Qualification ledger

| ID | Qualified answer/evidence | Best first move | Minimum path / source finding | Disposition |
|---|---|---|---|---|
| Q01 | D; `a+b+c=22` | Expand `(x+c)^3` and compare coefficients | `c=2,a=12,b=8`; test listed statements | scored; clean path |
| Q02 | B; `140°` in supplied solution | Use Apollonius on the median before angle chase | side data gives `AD=7`, then supplied `∠C=40°` with `AC=AD` gives `∠ADB=140°` | **SOURCE_CONFLICT**: side lengths themselves imply `∠C≠40°`; not a clean canonical anchor |
| Q03 | D; `k=70` | Divide by powers of `x` / use `x+1/x=-6` | reduce high powers using `x²+6x+1=0`; solve linear equation for `k` | scored; transform-first anchor |
| Q04 | B in official-style key; solution gives `3∛42` | Put `p=∛7,q=∛6` | recognize `x=p²+pq+q²=1/(p-q)` and collapse target | scored; **secondary text/options show notation inconsistencies; retain source locator** |
| Q05 | key `*`; derived `PQ=6√2` | Use intersecting chords / secant power | common length squared `=QC·CR=48`; second power relation gives `PQ²=72` | `SCORING_DISPOSITION=UNKNOWN/STAR`; printed options conflict; not ordinary scored recurrence |
| Q06 | C; solution computes `AE=22.5` | Mark equal arcs/chords, then seek similar triangles | recovered solution obtains `AC=15` and similarity giving `AE=22.5` | **TARGET-LABEL TRANSCRIPTION CONFLICT** in Cheenta (`AB` is already given); figure/target must be matched before canonical use |
| Q07 | B; 2 real roots | Set `a=2^x,b=3^x` or ratio `t=(2/3)^x` | factor `6t²-13t+6=0`; obtain `x=±1` | scored; strong exponential normalization anchor |
| Q08 | source key `Bonus` | Set `u=a²,v=b²`; optimize `u²v³` under `2u+5v=20` | weighted AM-GM/resource allocation gives `221.184`, absent printed choices | **BONUS**; do not count in scored difficulty/recurrence |
| Q09 | C; 2 ordered pairs | Square the first relation and subtract from the second | derive `xy²=5`; combine with `x-y²=4` to force `y=±1,x=5` | scored; compact elimination anchor |
| Q10 | B per key | Use geometry of the three unit squares, not coordinate brute force | supplied solution decomposes shaded region through midpoint/similarity/Pythagorean relations | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q11 | C per key | Mark diameter/right-angle and equal subtended-angle relations | short circle-angle chase on supplied figure | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q12 | D; `1250` in matching solution reproduction | Reduce the intended parity/residue condition modulo 4 | classify odd residues `1,3 mod 4` and count matching classes | **SOURCE_TRANSCRIPTION_SUSPECT**: searchable statement is corrupted (`m^n n^*`); mechanism may inform research but exact PYQ anchor remains blocked |
| Q13 | C in key; 2 ordered pairs | Treat as quadratic in `x` and force discriminant square/nonnegative | `Δ=73-16y`; admissible positive pairs are `(4,3),(3,4)` | scored; Diophantine discriminant anchor |
| Q14 | B | Pair the two squares as `(U+V)^2+(U-V)^2` | cancel against `2b²(1+a²)`; obtain `2(a+2)²+4ab²` | scored; identity-collapse anchor |
| Q15 | A; `122500` | Write nth term as `n(3n+1)` | sum `3Σn²+Σn` for `n=1..49` | scored; sequence/summation anchor |
| Q16 | key `Bonus` | Eliminate the common root between the cubic and quartic | use the common-root equations to reduce powers and parameter relation | **BONUS**; do not use as ordinary scored recurrence |
| Q17 | `∞` | Test whether the requested “maximum” is bounded before applying inequalities | with `abcd=1`, choose reciprocal scaling families; quadratic sum becomes unbounded | scored answer is unbounded/infinite; excellent `BOUND_BEFORE_OPTIMIZE` contrast anchor |
| Q18 | `0` | Use `gcd(n,n+1)=1` | if product of coprime consecutive positive integers is square, each must be square; no positive consecutive square pair | scored; coprime-square anchor |
| Q19 | `19` | Put the point on perpendicular bisector of `AB` from `PA=PB` | let side `s`, distance to `CD=x`; Pythagoras gives ratio, area ratio `3/16`; `m+n=19` | scored; figure helpful but text sufficiently constraining once orientation verified |
| Q20 | `4` | Convert radicals to exponent equations | reduce to relations in `x/y`; obtain `x+y=2`, solve quadratic cases, sum all roots | scored; original notation is delicate; preserve exact source before student publication |
| Q21 | `8` | Reconstruct nested radicals as squares stepwise | simplify inner radicals, match `sqrt(a)+sqrt(b)` structure; recovered solution gives `a=2,b=6` | scored; nested-radical reconstruction anchor |
| Q22 | `114°` | Mark equal lengths before cyclic-angle chasing | supplied figure gives isosceles angles, cyclic supplementary relation, then target `76+38` | scored; `FIGURE_REQUIRED_FOR_STUDENT_ANCHOR` |
| Q23 | `2` | Add 1 to the rational terms to expose `(a+b+c)/(...)` structure | transform three reciprocal-looking fractions into AP-related linear sums; solve ratios and target | scored; transform-first rational anchor |
| Q24 | `32` | Convert AM/GM immediately to sum/product | `u+v=34, uv=64`; solve quadratic or use difference square | scored; direct means anchor |
| Q25 | printed wording gives `20`; supplied key/solution gives `12` | Under printed text, choose tens digit then a different odd units digit | five odd digits imply `5·4=20`; Resonance solution inexplicably restricts to `1,3,5,7` | **SOURCE_CONFLICT**; no canonical answer until original-paper wording is recovered |
| Q26 | `84` | Set `t=∛2` | express all cube roots as powers of `t`; polynomial collapse using `t³=2` | scored; common-basis radical anchor |
| Q27 | `36` | Take reciprocals: `1/x+1/y=1`, etc. | solve the linear system in reciprocals; back-substitute into `15x-7y-z` | scored; reciprocal-linearization anchor |
| Q28 | `1` | Solve both inequalities before listing naturals | intersection is the single admissible natural integer; sum it | scored; interval/case-check anchor |
| Q29 | `5` | Factor `r³-1=(r-1)(1+r+r²)` before solving `a,r` | divide the two given GP relations to get `r=3`; recover `a=2`; huge-index ratios collapse to `r+a` | scored; high-index GP first-move anchor |
| Q30 | `7` | Let height `h`, base `h-4` | area gives `h(h-4)=192`; positive root `h=16`, base `12`, ratio `3/4` | scored; direct modeling anchor |

## Qualification status

- complete question slots: **30/30**
- explicit bonus items: **Q08, Q16**
- starred/unclear scoring item: **Q05**
- clean-source blockers despite known key/solution: **Q02, Q05, Q06, Q12, Q25**
- figure-gated canonical anchors: at least **Q06, Q10, Q11, Q22**; figure should also be retained for Q19 even though the text supports reconstruction
- ordinary scored recurrence must exclude Q08/Q16 and must not treat Q05 as scored until `*` is resolved

## Important curriculum findings

2023 reinforces several Preliminary-specific teaching requirements:

1. **First move dominates calculation**: Q03, Q07, Q09, Q14, Q23, Q27 and Q29 become short only after the right representation switch.
2. **Source-aware checking is itself mathematical discipline**: Q02 and Q25 demonstrate that a supplied key/solution does not make inconsistent wording mathematically clean.
3. **Optimization requires a boundedness check before an inequality**: Q17 is an unusually valuable contrast item because the correct answer is unbounded.
4. **Bonus questions must remain statistically separate**: Q08/Q16 are genuine paper mathematics but not ordinary scored-frequency evidence.
5. **Sequence & Series Preliminary layer is directly supported** by Q15 and Q29, with transform/summation and high-index GP recognition respectively.
