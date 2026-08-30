# Identities and Transformations — Assimilation Book

For the learner who can manipulate algebra but does not yet consistently choose the **right representation**.

## 1. RECONNECT

You probably know:

`(a+b)^2 = a^2+2ab+b^2`

and can expand

`(x+3)(x-5)`.

But which direction should you move in a problem?

### Diagnostic — do not solve fully

For each target, choose the better first move.

1. Evaluate `x^4+3x^2+1` given `x^2+x=1`.
2. Simplify `49^2-31^2`.
3. Given `u+v=10` and `uv=21`, find `u^2+v^2`.
4. Solve an equation after squaring both sides: what must you check afterward?

Expected ideas: **use the relation; factor as difference of squares; reconstruct a symmetric identity; check extraneous solutions**.

---

## 2. DISCOVER — representation is a choice

Consider

`49^2-31^2`.

A calculator-like approach squares both numbers.

A structural approach sees

`a^2-b^2 = (a-b)(a+b)`.

So

`49^2-31^2 = 18*80 = 1440`.

The important lesson is not the identity itself.

> **The target looked like a difference of squares, so factoring matched the target better than expansion.**

### Contrast pair

- `(x+5)^2` and you need a polynomial in powers of `x` -> expand.
- `x^2-25` and you need zero/product structure -> factor.

Same algebra. Different purpose.

---

## 3. MAKE SENSE — identity vs solution relation

An **identity** such as

`(x+1)^2 = x^2+2x+1`

is true for every permissible `x`.

A relation such as

`x^2+x=1`

is true only for values of `x` satisfying that equation.

But once a solution satisfies the relation, you may use it as a rewriting rule:

`x^2 = 1-x`.

That can be far more efficient than solving for `x`.

### Example — power reduction

Given `x^2+x=1`, find `x^4+3x^2+1`.

Use `x^2=1-x`.

First,

`x^4=(x^2)^2=(1-x)^2=1-2x+x^2=1-2x+(1-x)=2-3x`.

Then

`x^4+3x^2+1=(2-3x)+3(1-x)+1=6-6x`.

If the target can be reduced further using the original relation or another given condition, do that. The key is that we did **not** automatically solve the quadratic.

---

## 4. DISCOVER — substitution should compress structure

Suppose an equation contains

`(x+1/x)^2 - 5(x+1/x) + 6 = 0`.

The repeated block is the clue.

Set

`t = x+1/x`.

Then

`t^2-5t+6=0`.

The problem has become a low-degree equation in the quantity the expression actually depends on.

### Good substitution

Makes the repeated structure shorter and keeps all constraints visible.

### Bad substitution

Creates more symbols without reducing complexity.

---

## 5. MAKE SENSE — symmetric reconstruction

If you know

`u+v=S`, `uv=P`,

then

`u^2+v^2 = S^2-2P`,

`(u-v)^2 = S^2-4P`.

You do not need individual `u,v` unless the target distinguishes them.

This idea later becomes a major tool in Vieta (ALG-03), but here the focus is the algebraic representation decision.

### Contrast

- “find `u` and `v`” -> individual values may be necessary;
- “find `u^2+v^2`” -> test symmetric reconstruction first.

---

## 6. TRY — attempt before hints

### Problem A

Given `a+b=12`, `ab=20`, find `a^2+b^2`.

Try first.

**H1:** does the target change if `a,b` are swapped?

**H2:** use `(a+b)^2=a^2+b^2+2ab`.

**H3:** `a^2+b^2=144-40=104`.

### Problem B

Given `x^2=3x-1`, reduce `x^5` to the form `Ax+B`.

Try first.

**H1:** why solve for `x` if every power `x^2` can be replaced?

**H2:** build `x^3`, then `x^4`, then `x^5`, reducing after each multiplication.

**H3:** `x^3=8x-3`, `x^4=21x-8`, `x^5=55x-21`.

---

## 7. DIAGNOSE — transformations that can lose equivalence

### Squaring

From `A=B` we get `A^2=B^2`.

But from `A^2=B^2` we only know `A=B` **or** `A=-B`.

So squaring can add candidates.

### Dividing by an expression

From `x(x-2)=0`, dividing by `x` would lose the valid solution `x=0`.

### Clearing denominators

Record values that make any denominator zero before multiplying through.

> **Adopt:** a legal algebraic line is not automatically an equivalent line.

---

## 8. FADE — H3 -> H0

### Faded set 1: target reconstruction

Given `p+q=9`, `pq=14`, find `p^3+q^3`.

- H3: use `p^3+q^3=(p+q)^3-3pq(p+q)`.
- H2: rewrite the cubic target using sum/product.
- H1: the target is symmetric.
- H0: solve independently.

### Faded set 2: relation reduction

Given `t^2=2t+3`, find `t^6-5t^4` in the form `At+B`.

- H3: repeatedly replace `t^2`.
- H2: reduce powers after every multiplication.
- H1: treat the equation as a rewriting rule.
- H0: solve independently.

---

## 9. ADOPT — the transformation checklist

Before writing algebra, ask:

1. What exactly is requested?
2. Which representation resembles the target?
3. Is there a repeated block worth naming?
4. Is a given equation a useful rewriting rule?
5. Is my transformation reversible?
6. Am I solving more than the problem asks for?

---

## 10. PYQ ANCHORS

Use the validated paper statements for:

- `IOQM-2025-Q01` — simple-looking percentage relation where representation matters;
- `IOQM-2025-Q21` — integer/consecutive structure exposed algebraically;
- `IOQM-2024-Q05` — identity recognition;
- `IOQM-2024-Q11` — substitution/reconstruction.

All four official answers are independently verified in the corpus ledger.

---

## 11. TRANSFER

The same habits reappear in:
- ALG-03: Vieta, discriminant, polynomial reduction;
- ALG-05: strategic substitutions in functional equations;
- ALG-06: reversible radical/log transformations;
- NT-04: factorisation and integer reconstruction.

The shared question is:

> **What transformation exposes the invariant without creating unnecessary work?**
