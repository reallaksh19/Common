# Mock A — Teacher Key & Diagnostic Map v1

Student paper: `Mock_A_Student_v1.md`

All items are `AUTHOR_CREATED_TRANSFER`.

| Q | Answer | Package | First useful move | Likely miss tag |
|---:|---|---|---|---|
| 01 | B = 29 | P0-1 | `(alpha+beta)^2-2alphabeta` | REC/FM |
| 02 | A | P0-2 | seek `(sqrta+sqrtb)^2` | REP |
| 03 | B = 6 | P0-3 | AM-GM with equality at `x=3` | FM/DOM |
| 04 | B = 2 | P0-4 | cycle `2,4,1 (mod 7)` | FM/CHECK |
| 05 | C = 12 | P0-5 | radius to tangent is perpendicular | FIG |
| 06 | C = 185 | P1-1 | subtract term equations to get `d` | ALG |
| 07 | C = 48 | P1-2 | choose even unit first | CASE/COUNT |
| 08 | B = `2sqrt37` | P1-3 | median -> Apollonius | REC/FIG |
| 09 | C | P2-1 | step size 2 preserves parity | LOGIC |
| 10 | A = -3 | P2-2 | greatest integer `<= -2.3` | DOM |
| 11 | C = `x` | P0-1 | modulo `x^2=1` | REP |
| 12 | B = 4 | P0-2 | combine logs before solving | REP/DOM |
| 13 | C = 317 | P0-4 | `N-2` multiple of `lcm(5,7,9)` | FM |
| 14 | B = 68 | P0-5 | cyclic opposite angles sum 180 | FIG |
| 15 | B = 13 | P1-2 | 12 months -> pigeonhole | REC |
| 16 | 5 | P0-1 | `(alpha+beta)/(alphabeta)=5/3` | FM |
| 17 | 7 | P0-2 | `27sqrt3=3^(7/2)` | REP |
| 18 | 5 | P0-3 | convert to `1<x<7`, then count integers | DOM |
| 19 | 5 | P1-3 | hypotenuse is 10, then `R=c/2` | REC |
| 20 | 4 | P0-4 | `1+6/(n-1)` -> positive divisors of 6 | REP/DOM |
| 21 | 93 | P1-1 | finite GP sum | ALG |
| 22 | 20 | P1-2 | coefficient is `C(6,3)` | REC |
| 23 | 6 | P0-5 | tangent-secant power: `PA^2=PB*PC` | FIG |
| 24 | 65 | P1-3 | subtract two Pythagorean equations | FM |
| 25 | 21 | P2-1 | next odd term is `2n+1` | LOGIC |
| 26 | 3 | P2-2 | `2<=x/3<3` then integer filter | DOM |
| 27 | 96 | AF | multiply by `1.2*0.8` | REP |
| 28 | 8 | P0-1 | recursively reduce powers using `x^2=x+1` | REP |
| 29 | 42 | P0-4 | same remainder -> gcd of differences | FM |
| 30 | 7 | P2-2 | locate `sqrt50` between 7 and 8 | DOM |

## Minimum-path checks

### Q01
`alpha+beta=7`, `alphabeta=10`.

`alpha^2+beta^2=49-20=29`.

### Q03
`x+9/x >= 2sqrt9=6`; equality requires `x=3`.

### Q04
`2^1,2^2,2^3 ≡ 2,4,1 (mod 7)` and `2026≡1 (mod3)`.

### Q06
`a+2d=11`, `a+6d=23` -> `d=3`, `a=5`.

`S_10=5(2a+9d)=5(10+27)=185`.

### Q07
Unit digit has 2 choices (`2,4`). The remaining three positions are an ordered selection of 3 from the remaining 4 digits: `4*3*2=24`. Total `48`.

### Q08
Median square:

`m^2=[2(13^2)+2(15^2)-14^2]/4=148`, so `m=2sqrt37`.

### Q12
`log_2[x(x-2)]=3` -> `x(x-2)=8` -> `x=4` after `x>2` filtering.

### Q13
`N-2` is divisible by 5, 7 and 9. Their LCM is 315, so least admissible `N=317`.

### Q16
`1/alpha+1/beta=(alpha+beta)/(alphabeta)=5/3`.

### Q19
The hypotenuse is `sqrt(6^2+8^2)=10`. For a right triangle, the circumradius is half the hypotenuse, so `R=5`.

### Q20
`(n+5)/(n-1)=1+6/(n-1)`. Since `n` is positive and `n!=1`, admissible positive `n-1` are `1,2,3,6`, giving 4 values.

### Q23
`PA^2=4*9=36`, so `PA=6`.

### Q24
`AB^2=AD^2+9^2`, `AC^2=AD^2+4^2`; subtract to get `65`.

### Q28
`x^2=x+1` -> `x^3=2x+1`, `x^4=3x+2`, `x^5=5x+3`; hence `a+b=8`.

### Q29
The divisor divides `100-58=42` and `142-100=42`; greatest is 42.

## Diagnostic use

Do not interpret the raw score as a calibrated percentile or qualification probability.

After marking, record:

1. raw T24 training score;
2. `REC/FM/REP/...` error counts;
3. first-move accuracy separately from final-answer accuracy;
4. package clusters with two or more misses;
5. questions correct only after excessive time.

Route each miss to the smallest relevant First-Step card/lab before retesting.
