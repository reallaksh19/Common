# Mock C — Teacher Key & Diagnostic Map v1

Student paper: `Mock_C_Student_v1.md`

All items are `AUTHOR_CREATED_TRANSFER`.

| Q | Answer | Package | First useful move | Likely miss tag |
|---:|---|---|---|---|
| 01 | C = 6 | P0-1 | substitute the known common root | FM |
| 02 | B = 7 | P0-1 | square `x+1/x` and subtract 2 | REP |
| 03 | C = 9 | P0-3 | Cauchy/Engel bound | FM |
| 04 | B = 3 | P0-4 | compute multiplicative order of 2 mod 7 | REC |
| 05 | B = 70 | P0-5 | inscribed angle is half central angle | FIG |
| 06 | C = `9/10` | P1-1 | telescope `1/[n(n+1)]` | REP |
| 07 | C = 70 | P1-2 | coefficient is `C(8,4)` | REC |
| 08 | B = 5 | P1-3 | midpoint of BC then distance | FIG |
| 09 | A | P2-1 | several earlier cases -> strong induction | LOGIC |
| 10 | C = 0.6 | P2-2 | `{x}=x-floor(x)` | DOM |
| 11 | B = x | P0-1 | `x^3≡1` modulo `x^2+x+1` | REP |
| 12 | D = 512 | P0-2 | square transformed log variable | REP/DOM |
| 13 | B = 23 | P0-4 | simultaneous congruences / CRT reasoning | FM |
| 14 | B | P0-5 | tangent-square = external*whole secant | FIG |
| 15 | A | P1-2 | max subset with no consecutive terms is 5 | COUNT |
| 16 | 4 | P0-3 | AM-GM equality forces all roots 1 | FM |
| 17 | 5 | P0-2 | use `t^3=2` directly | REP |
| 18 | 4 | P0-3 | `|x-5|<3`, then exclude denominator zero | DOM |
| 19 | 113 | P0-5 | opposite angles of a cyclic quadrilateral sum 180 | FIG |
| 20 | 4 | P0-4 | digit sum must be divisible by 9 | FM |
| 21 | 48 | P1-1 | solve `a/(1-r)=12`, `ar=3` | REP |
| 22 | 20 | P1-2 | `C(6,3)` | COUNT |
| 23 | 24 | P1-3 | `c=2R=10`, `a+b=c+2r=14` | REP |
| 24 | 54 | P1-3 | angle-bisector split then Stewart shortcut | FIG |
| 25 | 2 | P2-1 | one base for each parity class | LOGIC |
| 26 | -1 | P2-2 | floor positive/negative separately | DOM |
| 27 | 54 | AF | radius 3, height 6 | REP |
| 28 | 1 | P0-1 | `x^3≡1`; 2025 divisible by 3 | REP |
| 29 | 42 | P0-4 | gcd of pairwise differences | FM |
| 30 | 60 | P1-2 | inclusion-exclusion for multiples of 2 or 5 | COUNT |

## Selected minimum-path checks

### Q03
By Engel form,

`1/a+4/b >= (1+2)^2/(a+b)=9/(a+b)`.

Since the left side equals 1, `a+b>=9`, and equality is attainable.

### Q04
`2^1≡2`, `2^2≡4`, `2^3≡1 (mod7)`, so the order is 3.

### Q06
`1/[n(n+1)]=1/n-1/(n+1)`. The sum through n=9 is `1-1/10=9/10`.

### Q11
`x^3-1=(x-1)(x^2+x+1)`, so modulo the divisor `x^3≡1`. Since `100≡1 (mod3)`, remainder `x`.

### Q13
23 gives residues `2 mod3`, `3 mod5`, `2 mod7`; smaller candidates satisfying the first two do not satisfy the third.

### Q15
A set with no consecutive integers can contain at most one from each pair `(1,2),(3,4),(5,6),(7,8),(9,10)`, hence at most 5. Choosing 6 forces a consecutive pair.

### Q18
`3/|x-5|>1` requires `0<|x-5|<3`. Integer solutions are `3,4,6,7`, giving 4.

### Q19
Opposite angles of a cyclic quadrilateral are supplementary, so the required angle is `180-67=113` degrees.

### Q21
`r=3/a`. Then

`a/(1-r)=a^2/(a-3)=12`

so `(a-6)^2=0`, hence `a=6`, `r=1/2`.

Sum of squares:

`36/(1-1/4)=48`.

### Q23
`c=2R=10`. For a right triangle, `r=(a+b-c)/2`, so `a+b=14`. Also `a^2+b^2=100`, hence `ab=48`; area `ab/2=24`.

### Q24
Angle-bisector theorem gives the opposite-side split `8,12`. The bisector identity from Stewart gives

`d^2=10*15-8*12=54`.

### Q26
`floor(2.4)=2`, `floor(-2.4)=-3`; sum `-1`.

### Q30
`floor(100/2)+floor(100/5)-floor(100/10)=50+20-10=60`.

## Diagnostic emphasis

Mock C is not intended merely to lower scores. Its purpose is to reveal whether recognition remains stable when mechanisms are compressed and mixed.

Pay special attention to:

- high recognition time with correct final answers;
- `REP` errors after correct chapter recognition;
- `DOM` errors on floor/absolute-value questions;
- `COUNT` errors when a structural bound replaces routine `nCr`;
- failures to choose a direct proof or compact invariant.
