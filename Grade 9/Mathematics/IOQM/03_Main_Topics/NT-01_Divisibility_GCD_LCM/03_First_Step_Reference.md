# NT-01 - First-Step Reference

Use this after the Assimilation Book. It is a compression layer, not a replacement for the reasoning.

## Recognition atlas

| Visible clue | Structural question | First useful move |
|---|---|---|
| `a|b`, common divisor of algebraic expressions | what integer combination removes variables/terms? | rewrite as integer multiples; combine |
| prime `p` and `p|ab` | is the divisor really prime? | apply Euclid's Lemma: `p|a` or `p|b` |
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

2. Is a PRIME divisor known to divide a product?
   -> check primality, then Euclid's Lemma: p|ab => p|a or p|b

3. Is gcd computation itself large?
   -> Euclid: (a,b) -> (b, a mod b)

4. Are gcd and lcm both given?
   -> gL=ab
   -> if actual a,b needed: a=gu, b=gv, gcd(u,v)=1, uv=L/g

5. Are conditions nested?
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

**Decision boundary:** use the lemma to split a **prime** divisor across a product. Do not use it for an arbitrary composite divisor, and do not replace a shorter direct divisibility argument with theorem-name recall.

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
4. **test vs structure:** one explicit integer -> divisibility test may work; variable/common-divisor relation -> translate/combine algebraically.
5. **Euclid vs factoring:** shrink by remainders when full factorization is expensive.
6. **numbers vs differences:** common divisor of the numbers -> gcd numbers; equal remainders -> gcd differences.
7. **product vs pair:** `gL=ab` answers a product question; pair reconstruction also needs coprime normalization.
8. **chain vs independent checks:** `a|b|c` contains transitive information; use it first.
9. **largest step vs first meeting:** spacing asks for gcd; synchronization asks for lcm.

## 30-second checks

Before committing to a method:

- What is the target object?
- If I want to split divisibility across a product, is the divisor prime?
- What disappears if I subtract?
- Can I remove a prescribed remainder?
- Is Euclid cheaper than factoring?
- Am I using an identity beyond what it actually determines?
- Is there a divisibility chain?
- Can I verify the final remainder/divisibility/coprimality condition directly?
