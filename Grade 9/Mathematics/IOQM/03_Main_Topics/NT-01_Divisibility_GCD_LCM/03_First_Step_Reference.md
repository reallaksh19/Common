# NT-01 - First-Step Reference

Use this after the Assimilation Book. It is a compression layer, not a replacement for the reasoning.

## Recognition atlas

| Visible clue | Structural question | First useful move |
|---|---|---|
| `a|b`, common divisor of algebraic expressions | what integer combination removes variables/terms? | rewrite as integer multiples; combine |
| prime `p` and `p|ab` | is the divisor really prime? | apply Euclid's Lemma: `p|a` or `p|b` |
| linear integer equation `ax+by=c` | does `gcd(a,b)` divide `c`? | use Bézout/extended Euclid before searching |
| closest fraction / small determinant `|qb-pa|` | can a linear combination of `p,q` be made `±gcd(p,q)`? | use Bézout structure plus the stated bounds |
| greatest integer dividing all given numbers | common divisor target? | gcd of the numbers |
| same remainder on several given numbers; divisor unknown | what disappears under subtraction? | take differences; gcd them if greatest requested |
| least number with a prescribed remainder under several divisors | can I remove the remainder first? | `N-r` is a common multiple |
| least positive number divisible by several integers | multiple target? | lcm |
| first time cycles coincide | synchronization? | lcm |
| largest common step/spacing | divisor of all distances? | gcd |
| large gcd pair | can remainder division shrink it? | Euclidean algorithm |
| gcd and lcm both given | only product or actual pair? | `gL=ab`; normalize if reconstructing |
| `a|b|c`-style nested constraints | is there a chain? | use transitivity before casework |
| one explicit integer and a familiar digit pattern | local yes/no check only? | divisibility test may be cheapest |

## Decision router

```text
1. What is unknown?
   |
   +-- a DIVISOR -> common divisor? same-remainder differences? gcd?
   |
   +-- a NUMBER/MULTIPLE -> least common multiple? remove prescribed remainder first?
   |
   +-- integer coefficients x,y in ax+by=c -> gcd divisibility first

2. Is a PRIME divisor known to divide a product?
   -> check primality, then Euclid's Lemma: p|ab => p|a or p|b

3. Is a linear integer combination required?
   -> run Euclid, then back-substitute to get gcd(a,b)=ax+by
   -> scale only if gcd(a,b)|c

4. Is gcd computation itself large?
   -> Euclid: (a,b) -> (b, a mod b)

5. Are gcd and lcm both given?
   -> gL=ab
   -> if actual a,b needed: a=gu, b=gv, gcd(u,v)=1, uv=L/g

6. Are conditions nested?
   -> compress divisibility chain before enumeration
```

## First-step cards

**Divisibility algebra**  
`d|A` and `d|B` -> `d|(rA+sB)` for integers `r,s`.

**Euclid's Lemma - prime divisor of a product**  
If `p` is prime and `p|ab`, then `p|a` or `p|b`.

A short proof uses the same gcd structure as this topic. If `p` does not divide `a`, then `gcd(p,a)=1`. Therefore integers `r,s` exist with `rp+sa=1`. Multiply by `b`:

`rpb+sab=b`.

Both terms on the left are divisible by `p`, so `p|b`.

**Hypothesis check:** primality matters. The composite imitation is false: `6|2*3`, but `6` divides neither `2` nor `3`.

**Bézout / extended Euclid**  
For integers `a,b`, there exist integers `x,y` such that

`ax+by=gcd(a,b)`.

This is not a new black-box theorem: the coefficients can be recovered by **back-substituting the Euclidean algorithm**.

Example:

`43 = 1*30 + 13`  
`30 = 2*13 + 4`  
`13 = 3*4 + 1`.

Back-substitute:

`1 = 13-3*4 = 13-3(30-2*13) = 7*13-3*30 = 7(43-30)-3*30 = 7*43-10*30`.

So `43*7 + 30*(-10)=1`.

**Linear-Diophantine solvability:**  
`ax+by=c` has integer solutions **iff** `gcd(a,b)|c`.

- Necessity: every integer combination `ax+by` is divisible by `gcd(a,b)`.
- Sufficiency: scale a Bézout identity for `gcd(a,b)` by `c/gcd(a,b)`.

NT-04 owns the subsequent full solution-family parameterization, bounds and finite filtering.

**Closest-rational bridge**  
For fractions near `p/q`, the numerator of the difference often becomes a small integer determinant such as `|qb-pa|`. Bézout can show when the smallest possible nonzero value is `gcd(p,q)` (often `1` when `p,q` are coprime), but denominator bounds still decide which candidate is actually closest. Do not stop at the existence theorem.

**Same remainder, unknown divisor**  
`a=dq+r`, `b=dp+r` -> `d|(a-b)`.

**Prescribed remainder, unknown number**  
`N` leaves remainder `r` under each divisor -> every divisor divides `N-r`.

**Euclid**  
`a=qb+r` -> `gcd(a,b)=gcd(b,r)`.

**gcd/lcm reconstruction**  
`a=gu`, `b=gv`, `gcd(u,v)=1`, `uv=L/g`.

**Divisibility chain**  
`a|b` and `b|c` -> `a|c`.

## Contrast strip - why the first move changes

1. **gcd vs lcm:** divisor target -> gcd; common-multiple target -> lcm.
2. **same remainder fork:** unknown divisor -> differences; unknown number with prescribed remainder -> subtract remainder then lcm.
3. **prime divisor vs composite divisor:** `p|ab` with prime `p` -> Euclid's Lemma; a composite divisor need not divide either factor.
4. **Euclid vs extended Euclid:** Euclid computes the gcd; extended Euclid also recovers coefficients expressing that gcd as `ax+by`.
5. **solvability vs reconstruction:** `gcd(a,b)|c` decides whether `ax+by=c` is possible; NT-04 handles the full family and extra restrictions.
6. **Bézout vs bounded closest fraction:** Bézout supplies a possible smallest determinant; denominator/numerator bounds still determine the optimum admissible fraction.
7. **test vs structure:** one explicit integer -> divisibility test may work; variable/common-divisor relation -> translate/combine algebraically.
8. **Euclid vs factoring:** shrink by remainders when full factorization is expensive.
9. **numbers vs differences:** common divisor of the numbers -> gcd numbers; equal remainders -> gcd differences.
10. **product vs pair:** `gL=ab` answers a product question; pair reconstruction also needs coprime normalization.
11. **chain vs independent checks:** `a|b|c` contains transitive information; use it first.
12. **largest step vs first meeting:** spacing asks for gcd; synchronization asks for lcm.

## 30-second checks

Before committing to a method:

- What is the target object?
- If I want to split divisibility across a product, is the divisor prime?
- For `ax+by=c`, does `gcd(a,b)` divide `c`?
- Do I need only the gcd, or actual Bézout coefficients too?
- What disappears if I subtract?
- Can I remove a prescribed remainder?
- Is Euclid cheaper than factoring?
- Am I using an identity beyond what it actually determines?
- Is there a divisibility chain?
- Can I verify the final remainder/divisibility/coprimality condition directly?
