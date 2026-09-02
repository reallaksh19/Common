# First-Step Reference - Diophantine Equations & Integer Restrictions

## Recognition atlas
| Visible clue | Structural question | First useful line |
|---|---|---|
| product/shifted product equals constant | are factors integral? | set factors equal to divisor pair |
| difference of squares | what parity must factor pair have? | `(x-y)(x+y)=N` |
| fixed product + gcd 1 | can prime-power blocks split? | allocate whole blocks |
| integer maximum/minimum | can I bound before listing? | locate feasible factor pair near real optimum |
| fraction near p/q | is scaled error an integer? | write `|qa-pb|/(qb)` |
| sum and product | is target symmetric? | use `S,P` invariants or `t^2-St+P` |
| quadratic must have integer root | is discriminant a square? | `D=b^2-4ac=k^2` |
| many variables + fixed sum | can one variable be eliminated? | substitute side condition immediately |
| finite candidates | have I proved completeness? | state case-to-solution correspondence |

## Contrast strip
- Real optimum vs integer attainment: a bound suggests where to look; divisors decide what exists.
- Factorisation vs brute force: factorisation is complete only when sign/parity branches are accounted for.
- Decimal closeness vs exact rational gap: decimals estimate; `qa-pb` certifies.
- Quadratic real root vs integer root: `D>=0` is not enough; integer feasibility is stricter.
- Sum/product reconstruction vs solving variables: symmetric targets often stop before roots.
- Prime-exponent retrieval vs local teaching: use block allocation, do not rebuild divisor theory.

## Final checks
Original equation; positivity/sign; parity; gcd/coprimality; denominator nonzero; integer reconstruction; duplicate removal; boundary endpoints; all one-way candidates rechecked.
