# ALG-05 Independent Math and Source Audit

Status: `PASS_STATIC_MATH_AND_SOURCE`

This audit was run after final learner wording and independently of the Teacher Diagnostic Key.

## 1. Historical anchors

### IOQM-2025-Q14

Domain: integers.

Given `f(0)=1` and the source relation involving `f(mn+1)`:

- set `m=0`: the left side is `f(1)` and the right side collapses to `2`, so `f(1)=2`;
- set `n=0`: `f(1)=f(m)-m+1`, hence `f(m)=m+1` for every integer `m`.

Therefore

`f(1)+...+f(N)=2+3+...+(N+1)=N(N+3)/2`.

At `N=12`, the sum is `90<100`; at `N=13`, it is `104>=100`. Thus the answer is `12`.

Independent result agrees with the final official key and frozen verification ledger.

### IOQM-2024-Q16

Domain: reals.

Let `A=f(x)` and `B=f(3-x)`. The source equation gives

`3A+4B=x^2`.

Replace `x` by `3-x`:

`4A+3B=(3-x)^2`.

Eliminating `B` gives

`7f(x)=x^2-24x+36`.

Hence

`f(27)-f(25)=(117-61)/7=8`.

Independent result agrees with the official HBCSE key and frozen verification ledger.

No metadata-correction overlay event affects either anchor.

## 2. Paired-equation authored items

Symbolic elimination independently confirms:

- `2f(4-x)+f(x)=x+4` gives `f(x)=4-x`; target `f(1)=3`.
- `f(x)+f(2-x)=10` together with `f(2-x)-f(x)=2-2x` gives `f(x)=x+4`; target `f(5)=9`.
- `3f(5-x)+2f(x)=x+10` gives `f(x)=5-x`; target `f(-2)=7`.
- `4f(1-x)+f(x)=3x+1` gives `f(x)=1-x`; target `f(7)=-6`.
- `2f(x)+f(3-x)=x+9` gives `f(x)=x+2`; targets `f(20)=22`, `f(10)=12`.
- `3f(x)+f(4-x)=4x+4` gives `f(x)=2x-1`; target `f(7)=13`.
- the mastery sum/difference pair at `x` and `1-x` gives `f(x)=x+2`; target `f(-4)=-2`.

All partner substitutions stay inside `R`.

## 3. Integer-domain authored items

- Additive equation on `Z` with `f(1)=3`: `f(n)=3n`, including negative integers; `f(-4)=-12`.
- `f(m+n)=f(m)+f(n)+2mn`, `f(1)=1`: subtract `n^2` to obtain an additive integer function with value zero at 1, hence `f(n)=n^2`; `f(6)=36`.
- `f(m+n)=f(m)+f(n)+mn`, `f(1)=1`: `g(n)=f(n)-n(n+1)/2` is additive on `Z` and `g(1)=0`, so `f(n)=n(n+1)/2`; targets `f(8)=36`, `f(9)=45`. Direct substitution verifies the formula.
- `f(m-n)=f(m)-n`, `f(0)=3`: set `m=0`, then relabel `t=-n`; `f(t)=t+3`, so `f(-11)=-8`.
- same equation with `f(0)=4`: `f(t)=t+4`, so `f(13)=17`.

All substitutions used are integers.

## 4. Underdetermination checks

### Real shift

`f(x+1)=f(x)+2`, `f(0)=1` does not determine a function on all reals. Choose arbitrary values on representatives in `[0,1)` (with the value at 0 fixed) and extend by `f(r+k)=h(r)+2k`. Distinct choices of `h` give distinct solutions.

### Reflection sum

`f(x)+f(2-x)=10` alone does not determine `f(5)`. Values can be chosen freely on one representative from each pair `{x,2-x}`, then the partner value is forced. At the fixed point `x=1`, only `f(1)=5` is forced.

These items correctly test the distinction between one relation and a determined function.

## 5. Injectivity and surjectivity

For `f(x+f(y))=f(x)+y` on `R`:

Injectivity: if `f(a)=f(b)`, then for any `x`,
`f(x+f(a))=f(x)+a` and `f(x+f(b))=f(x)+b`.
Equal arguments on the left give equal values, so `a=b`.

Surjectivity: setting `x=0` gives `f(f(y))=f(0)+y`. For arbitrary target `t`, choose `y=t-f(0)`. Then `f(f(y))=t`, explicitly producing a preimage.

No continuity, monotonicity, boundedness, or pre-existing inverse is assumed.

## 6. Candidate verification item

For `f(x)=x^2+1`:

`f(x+y)=(x+y)^2+1`.

The proposed right side is

`(x^2+1)+(y^2+1)+2xy-1=x^2+2xy+y^2+1`.

The two sides agree for all real `x,y`.

## 7. Domain and proof-completeness audit

PASS:
- every fractional/real input appears only in a real-domain item;
- every integer-domain propagation explicitly remains on integers;
- finite sample values are never promoted as proof;
- a derived recurrence-like relation is not treated as sufficient proof of an unrelated original two-variable equation;
- every full formula used for a promoted solve is either derived for all allowed inputs or verified in the original equation.

## Static result

`INDEPENDENT_MATH_SOURCE_AUDIT_PASS`

Classroom, retention, psychometric, calibration and publication gates are outside this audit and remain `NOT_RUN`.
