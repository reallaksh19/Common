# Inequalities, Bounds & Equality Conditions
## Integrated Assimilation Book

For a learner who remembers some inequality formulas but does not yet consistently separate **bound**, **equality**, and **attainment**.

> **Central belief: A bound is NOT automatically the requested extremum.**

---

## 1. RECONNECT - three different statements

For real `x`,

`(x-3)^2 >= 0`.

Therefore

`x^2-6x+13 >= 4`.

This proves `4` is a lower bound. Because equality occurs at `x=3`, and `3` is an allowed real number, the minimum is `4`.

Now change only the domain to `x>3`.

The same lower bound `4` is still true, but equality would require `x=3`, which is not allowed. So on `x>3`, `4` is **not** a minimum.

That one contrast contains the whole topic:

`BOUND -> EQUALITY -> ATTAINMENT`.

### First attempt

Decide whether each conclusion is justified.

1. `x^2>0` for `x!=0`, so the minimum over `x!=0` is `0`.
2. For `x>0`, AM-GM gives `x+9/x>=6`; therefore the minimum is `6`.
3. For integer `n`, `(n-1/2)^2+2>=2`; therefore the integer minimum is `2`.

Do not calculate first. Inspect the equality case and the domain.

---

## 2. DISCOVER - read the request and direction before choosing a tool

A question asking for a **minimum** needs a lower-bound route. A question asking for a **maximum** needs an upper-bound route.

This sounds obvious, but many incorrect solutions prove a true inequality in the wrong direction.

### Contrast

For nonnegative `x,y` with `x+y=10`:

`(x-y)^2>=0`

implies

`(x+y)^2>=4xy`, so `xy<=25`.

This is an **upper** bound on `xy`, useful for a maximum. It does not give a positive lower bound: `xy` can be `0` if zero is allowed, and can approach `0` without attaining it if `x,y>0`.

### Adopt the first four router questions

1. What is requested: minimum, maximum, feasibility, or just a proof?
2. What is the domain?
3. Is the expression bounded in the needed direction?
4. Which representation exposes that direction?

---

## 3. MAKE SENSE - completing the square is an optimization representation

A quadratic often reveals its bound immediately after completing the square.

### Example: minimum

`f(x)=x^2-6x+13`

becomes

`f(x)=(x-3)^2+4`.

Since a square is nonnegative, `f(x)>=4`, with equality at `x=3`.

### Example: maximum

`g(x)=10-(x-2)^2`.

Since `(x-2)^2>=0`,

`g(x)<=10`, with equality at `x=2`.

### Boundary with discriminant

If the request is “for which parameter values does a quadratic equation have real roots?”, that is a root-feasibility question canonically owned by ALG-03. Do not turn every quadratic optimization problem into a discriminant problem.

---

## 4. DISCOVER - AM-GM is a bound plus an equality condition

For positive reals `a,b`,

`a+b >= 2sqrt(ab)`.

Equality occurs exactly when `a=b`.

The hypotheses matter: positivity is not decoration.

### Example

For `x>0`, find the minimum of

`x+9/x`.

Both terms are positive. AM-GM gives

`x+9/x >= 2sqrt(9)=6`.

Equality needs

`x=9/x`, so `x=3` (the positive solution).

Because `x=3` belongs to the domain, the minimum is `6`.

### Contrast: upper bound, not lower bound

If `a,b>=0` and `a+b=12`, then

`ab <= 36`, equality at `a=b=6`.

So `36` is the maximum product. There is no reason to call it a minimum.

### Contrast: positive but no minimum product

If `a,b>0` and `a+b=12`, then `ab>0`, but values such as `a=0.1`, `b=11.9` make the product small. It can approach `0`, but never attain `0`. Thus there is no positive minimum.

---

## 5. MAKE SENSE - Cauchy/Engel only when the structure justifies it

For positive `x,y`, the Engel form gives

`1/x + 1/y >= (1+1)^2/(x+y)`.

If `x+y=10`,

`1/x+1/y >= 4/10 = 2/5`.

Equality in this case occurs at `x=y=5`, so the minimum is `2/5`.

The point is not to collect names of inequalities. The point is to recognize a representation in which the desired direction and equality condition are transparent.

### Why not use Cauchy everywhere?

If square completion gives the target in one line, importing a stronger theorem adds cognitive cost without adding information.

---

## 6. DIAGNOSE - bound, equality, attainment, discrete filter

### Error A - lower bound = minimum

For `x>0`, `x^2>0`, so `0` is a lower bound, but it is not attained. There is no minimum; the infimum is `0`.

### Error B - real equality point used in an integer problem

For real `x`,

`(x-1/2)^2+2 >= 2`, equality at `x=1/2`.

For integer `n`, `1/2` is inadmissible. Check the nearest integers:

`n=0` or `1` gives `1/4+2=9/4`.

So the integer minimum is `9/4`, not `2`.

### Error C - equality condition forgotten

An inequality theorem may prove the numerical bound correctly while the proposed equality case violates a given restriction. The correct conclusion then changes.

### Error D - wrong direction

To maximize `xy` under fixed sum, proving `xy>=0` is true but irrelevant.

---

## 7. TRY - H3 -> H2 -> H1 -> H0

Attempt before reading support.

### H3 - execution supplied

For `x>0`, minimize `x+16/x`.

Use AM-GM:
`x+16/x >= 2sqrt(16)=8`, equality at `x=4`.

### H2 - representation supplied

For real `x`, find the minimum of `x^2+8x+20`.

Cue: complete the square. Execute and verify equality yourself.

### H1 - recognition clue

For positive `a,b` with `a+b=14`, maximize `ab`.

Clue: fixed sum, product target, equality should be balanced.

### H0 - no route supplied

For integer `n`, find the minimum of `n^2-5n+9`.

Choose the continuous representation, then apply the discrete filter.

---

## 8. ADOPT - the full optimization router

```text
REQUEST
 -> DOMAIN
 -> BOUNDED?
 -> DIRECTION
 -> REPRESENTATION
 -> BOUND
 -> EQUALITY
 -> ATTAINMENT
 -> DISCRETE FILTER
 -> CHECK
```

### Stop conditions

- If the expression is unbounded in the requested direction, stop: no finite extremum.
- If equality is impossible in the domain, do not call the bound a minimum/maximum.
- If the domain is discrete, do not stop at a continuous equality point.

---

## 9. Historical anchor traces

### `IOQM-2025-Q07`

The independently verified route writes the relevant sum as `n=x+y` and uses

`(x-y)^2 = 2(n+1012)-n^2 >= 0`.

This yields an upper feasibility bound on `n`; the integer filter gives the largest admissible integer `46`.

Pedagogical role: **feasibility bound -> direction -> integer filter**.

### `IOQM-2024-Q06`

The power conditions force the variables into a very small discrete set; equality/extreme behavior can then be checked exactly. The independently verified answer is `06`.

Pedagogical role: **strong bound -> equality structure -> discrete admissibility**.

These are validated anchors, not evidence of official topic frequency.

---

## 10. TRANSFER

### Changed domain

A bound attained over reals may fail to be attained over positive reals, integers, or a punctured interval.

### Geometry

A perimeter/area problem may reduce to a fixed-sum product bound. Geometry remains the historical owner when the geometric structure is decisive; ALG-02 supplies the optimization mechanism.

### Number theory

A continuous inequality can create a short interval, after which integer/divisibility filters decide the actual answer.

### Polynomial boundary

If the request is root count/real-root existence, retrieve ALG-01 transformation habits but route to ALG-03 discriminant canon. If the request is the quadratic’s minimum value, remain in ALG-02 and complete the square.

## Final belief

> **Prove the bound, name the equality condition, test attainment in the real domain of the question, then filter discrete candidates if necessary.**
