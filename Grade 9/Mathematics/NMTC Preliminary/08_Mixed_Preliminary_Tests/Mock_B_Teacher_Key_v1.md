# Mock B — Teacher Key & Diagnostic Map v1

Student paper: `Mock_B_Student_v1.md`

All items are `AUTHOR_CREATED_TRANSFER`.

| Q | Answer | Package | First useful move | Likely miss tag |
|---:|---|---|---|---|
| 01 | A = -7 | P0-1 | integer factor pair of 12 with difference 1 | REC |
| 02 | B | P0-2 | reverse a hidden square | REP |
| 03 | D | P0-3 | test boundedness before optimizing | FM/DOM |
| 04 | C = 7 | P0-4 | units-digit cycle length 4 | CHECK |
| 05 | B = 38 | P0-5 | tangent-chord theorem | FIG |
| 06 | C = 31 | P1-1 | iterate or set `b_n=a_n+1` | REP |
| 07 | C = 16 | P1-2 | even subsets are half of all subsets | COUNT |
| 08 | B = (4,6) | P1-3 | angle-bisector ratio `BD/DC=AB/AC` | FIG |
| 09 | B | P2-1 | direct factorization beats induction | FM/LOGIC |
| 10 | B = -2 | P2-2 | least integer `>= -2.3` | DOM |
| 11 | A = -1 | P0-1 | modulo `x^2=-1`; cycle mod 4 | REP |
| 12 | B = 8 | P0-2 | convert log statement to exponent | REP |
| 13 | C = 77 | P0-4 | `N-5` is multiple of lcm(6,8,9)=72 | FM |
| 14 | B = 6 | P0-5 | intersecting-chord product | FIG |
| 15 | C = 20 | P1-2 | inclusion-exclusion | COUNT |
| 16 | 16 | P0-3 | AM-GM equality forces all roots 2 | FM |
| 17 | 6 | P0-2 | common base 2 | REP |
| 18 | 9 | P0-3 | discriminant `>=0` | FM |
| 19 | 8 | P0-5 | right triangle `OPT`: `PT^2=OP^2-r^2` | FIG |
| 20 | 3 | P0-4 | `1+6/(n+1)` -> divisor reduction | REP/DOM |
| 21 | 55 | P1-1 | standard arithmetic sum | ALG |
| 22 | 30 | P1-2 | divide `5!` by repeated-letter factorials | COUNT |
| 23 | 2 | P1-3 | right-triangle `r=(a+b-c)/2` | REC |
| 24 | 19 | P1-3 | Stewart with labelled segments | FIG/ALG |
| 25 | 26 | P1-1 | recurrence increments are odd numbers | REP |
| 26 | 2 | P2-2 | translate floor equality to half-open interval | DOM |
| 27 | 75 | AF | include hour-hand motion | REP |
| 28 | 1 | P0-1 | shift argument before solving | REP |
| 29 | 9 | P0-4 | divisibility by 11 from alternating digit sum | CASE |
| 30 | 8 | P2-2 | bound sqrt80 between 8 and 9 | DOM |

## Selected minimum-path checks

### Q01
Positive integer roots with product 12 and difference 1 are 3 and 4. Their sum is 7, so `p=-7`.

### Q03
`x+4/x >=4`, but this is a **minimum**. As `x->infinity`, the expression is unbounded above, so no maximum exists.

### Q06
`1,3,7,15,31`; alternatively `a_n+1=2(a_(n-1)+1)`.

### Q07
Among all `2^5=32` subsets, even and odd cardinalities are equally numerous, so 16.

### Q11
Modulo `x^2+1`, `x^2=-1`, hence `x^4=1`. Since `2026≡2 (mod4)`, the remainder is `-1`.

### Q15
Multiples of 2: 15. Multiples of 3: 10. Multiples of 6: 5. Union count `15+10-5=20`.

### Q16
For four positive roots with product 16, AM-GM gives sum at least `4*16^(1/4)=8`. Equality with given sum 8 forces every root to be 2; square sum is 16.

### Q19
The radius to the tangent point is perpendicular to the tangent. Thus `PT^2=10^2-6^2=64`, so `PT=8`.

### Q20
`(n+7)/(n+1)=1+6/(n+1)`. For positive n, `n+1` is a positive divisor of 6 greater than 1: 2,3,6. Thus 3 values.

### Q24
Stewart:

`7^2(3)+5^2(5)=8(AD^2+15)`.

`272=8(AD^2+15)` -> `AD^2=19`.

### Q29
Divisibility by 11 requires `11-a-b` to be a multiple of 11. In its possible range, this means `a+b=0` or `11`. There is 1 pair for 0 and 8 digit pairs for 11, total 9.

## Diagnostic emphasis

Mock B should produce more `REP`, `CASE`, `DOM` and method-choice errors than Mock A. A student who scores similarly but shows a sharp rise in first-move latency is not yet transfer-stable.
