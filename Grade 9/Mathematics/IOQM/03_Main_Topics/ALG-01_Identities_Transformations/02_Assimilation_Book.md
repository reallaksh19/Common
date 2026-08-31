# Identities, Transformations & Equation Structure
## Integrated Assimilation Book

For a learner who already knows many algebraic rules but does not yet consistently choose the *right form*.

> **Governing question: What form makes the requested target cheapest?**

---

## 1. RECONNECT - you know the moves; can you choose the direction?

You probably know:
- `(a+b)^2 = a^2+2ab+b^2`;
- `a^2-b^2=(a-b)(a+b)`;
- how to solve linear equations;
- how to substitute a value or expression.

The IOQM step is to decide **which move is worth making**.

### First attempt - write only the first useful line

1. Given `x^2+x=1`, find `x^4+3x`.
2. Evaluate `49^2-31^2`.
3. Given `u+v=10` and `uv=21`, find `u^2+v^2`.
4. You square both sides of an equation. What must happen before any candidate is accepted?

Do not fully solve unless the target demands it.

The intended first ideas are:
- use the given relation as a rewriting rule;
- factor a difference of squares;
- reconstruct the symmetric target;
- verify candidates in the original equation.

---

## 2. DISCOVER - factor and expand are opposite representation choices

Consider `49^2-31^2`.

Long calculation treats the two squares separately. Structure sees

`49^2-31^2 = (49-31)(49+31) = 18*80 = 1440`.

The identity was already known. The new habit is:

> **Use the direction that resembles the requested information.**

### Contrast A - expand

You need the coefficient of `x` in `(x+5)(x-2)`.

Expanding is useful:
`(x+5)(x-2)=x^2+3x-10`.

### Contrast B - factor

You need the zeros of `x^2-25`.

Factoring is useful:
`x^2-25=(x-5)(x+5)`.

Same algebra. Different target. No direction is automatically "simpler."

### Try

For each, choose `expand`, `factor`, or `leave as is`.

1. coefficient of `x` in `(2x-1)(x+7)`;
2. solve `x^2-9=0`;
3. evaluate `1003^2-997^2`;
4. find the product of the roots of `(x-4)(x+6)=0` without expanding.

The point is the decision, not speed.

---

## 3. MAKE SENSE - identity vs relation on solutions

An **identity** is true for every permissible input:

`(x+1)^2 = x^2+2x+1`.

A **relation on solutions** is true only for values satisfying a condition:

`x^2+x=1`.

For those admissible values, the relation can be rewritten as

`x^2=1-x`.

That is a local rewriting rule. It is not an identity in all real `x`.

### Example - reduce the target, not the variable

Given `x^2+x=1`, find `x^4+3x`.

From `x^2=1-x`,

`x^4=(1-x)^2=1-2x+x^2=1-2x+(1-x)=2-3x`.

Therefore

`x^4+3x = 2`.

We never needed the individual values of `x`.

### Why this matters

A common reflex is:
1. solve the quadratic;
2. substitute each root;
3. simplify.

That route may be valid, but it solves more than the target asks. Relation reduction keeps the information in its cheapest form.

### Boundary with ALG-03

Here we learn the **elementary habit** "a relation can rewrite higher powers."  
ALG-03 canonically owns polynomial remainder/reduction as a general polynomial method.

---

## 4. DISCOVER - substitution must compress structure

Suppose

`(x+1/x)^2 - 5(x+1/x) + 6 = 0`, with `x != 0`.

The block `x+1/x` repeats. Set

`t = x+1/x`.

The equation becomes

`t^2-5t+6=0`.

This is a useful substitution because one symbol replaces a repeated structure and the original restriction `x != 0` remains visible.

### Bad substitution test

If a new variable:
- appears only once,
- creates another equation of equal complexity,
- or hides a restriction you later forget,

then it may be renaming rather than simplifying.

### Contrast

- `x^4+6x^2+5=0` -> `t=x^2` compresses the even-power structure.
- `x^2+3x+7=0` -> `t=x+1` does not automatically make the target smaller.

Ask: **what complexity disappeared?**

---

## 5. MAKE SENSE - symmetric reconstruction

Suppose you know

`u+v=S` and `uv=P`.

Then

`u^2+v^2=(u+v)^2-2uv=S^2-2P`

and

`u^3+v^3=(u+v)^3-3uv(u+v)=S^3-3PS`.

If the target is unchanged when `u` and `v` are swapped, test whether sum/product data already determine it.

### Example

Given `u+v=10`, `uv=21`,

`u^2+v^2=100-42=58`.

Solving `u` and `v` individually is unnecessary.

### Contrast - when individual values matter

If the target is `u-v` rather than `(u-v)^2`, order/sign information matters. Sum and product may not decide the requested signed value by themselves.

### Boundary with Vieta

ALG-01 owns reconstruction from **already supplied** sum/product information.  
ALG-03 owns the derivation that polynomial coefficients give root sum/product.

---

## 6. MAKE SENSE - equivalence is stricter than a legal-looking line

A transformation is **equivalent** if it preserves exactly the same solution set under the recorded conditions.

### Reversible examples

- add the same expression to both sides;
- subtract the same expression;
- multiply/divide by a known nonzero constant.

### Conditional examples

#### Squaring

`A=B  =>  A^2=B^2`.

The reverse need not hold because `A^2=B^2` allows `A=B` or `A=-B`.

So squaring often creates **candidates**, not automatically solutions.

#### Dividing by an expression

From `x(x-4)=0`, dividing by `x` loses the valid branch `x=0`.

Before cancellation, ask whether the factor can vanish.

#### Clearing denominators

Before multiplying an equation by `(x-2)(x+5)`, record `x != 2,-5`.

A later algebraic candidate that violates an original denominator restriction is rejected.

> **Adopt:** "algebraically legal" and "logically equivalent" are not synonyms.

---

## 7. TRY - support fades H3 -> H2 -> H1 -> H0

Each item is attempted before using the stated support.

### H3 - execution relation supplied

Given `a+b=12`, `ab=20`, find `a^2+b^2`.

Use:
`a^2+b^2=(a+b)^2-2ab`.

Answer: `104`.

### H2 - representation supplied, execution withheld

Given `x^2=3x-1`, express `x^5` as `Ax+B`.

Representation cue: treat `x^2=3x-1` as a rewriting rule and reduce after every multiplication.

Check after your attempt: `x^5=55x-21`.

### H1 - recognition clue only

Given `p+q=9`, `pq=14`, find `p^3+q^3`.

Clue: the target is unchanged when `p,q` are swapped.

### H0 - no route supplied

Given `t^2=2t+3`, reduce `t^6-5t^4` to `At+B`.

No method label. Decide the representation, execute, and check.

---

## 8. DIAGNOSE - four tempting wrong starts

### Error 1: "Expanding is progress"

Why tempting: school exercises often ask for expanded form.  
Repair: ask what information the target needs.

### Error 2: "If I can solve the variable, I should"

Why tempting: equations invite root-finding.  
Repair: test whether the requested expression is already fixed by a relation or symmetry.

### Error 3: "A substitution is always helpful"

Why tempting: a new letter looks shorter.  
Repair: demand a measurable reduction in repeated structure or degree.

### Error 4: "Squaring/cancelling gives an equivalent equation"

Why tempting: the algebraic line is syntactically valid.  
Repair: track direction of implication, excluded values and original-equation checks.

---

## 9. ADOPT - the target-first checklist

Before writing algebra:

1. What exactly is requested?
2. Which visible form already resembles the target?
3. Would factoring expose a product/zero structure?
4. Would expanding expose coefficients or additive structure?
5. Does a composite block repeat enough to name?
6. Is the target symmetric, so individual variables may be unnecessary?
7. Can a given relation rewrite high powers?
8. Will the next step preserve equivalence?
9. Am I solving more than the problem asks?
10. How will I verify the result independently?

Compressed:

`TARGET -> STRUCTURE -> REPRESENTATION -> FIRST MOVE -> CONDITIONS -> CHECK`.

---

## 10. Historical anchor traces

Use exact historical wording from the validated papers when practicing the full PYQs.

- `IOQM-2025-Q01`: translate the given percentage statement and notice that the requested quantity is algebraically the same quantity; verified answer `40`.
- `IOQM-2025-Q21`: model the consecutive/integer structure first; a low-degree relation and admissibility condition collapse the search; verified answer `49`.
- `IOQM-2024-Q05`: set ratio variables whose product is `1`; one expansion reconstructs the requested difference; verified answer `01`.
- `IOQM-2024-Q11`: reciprocal substitutions make the two supplied constraints comparable; the transformed variables are forced equal and the target is reconstructed; verified answer `12`.

These four items are evidence for mechanisms, not a claim of official topic weightage.

---

## 11. TRANSFER - the same habit, different surfaces

### To inequalities

Before applying a bound, ALG-02 asks which representation exposes the quantity to be bounded. The transformation habit comes from here; AM-GM/equality/attainment are taught there.

### To polynomials

ALG-03 turns relation rewriting into a canonical polynomial-reduction method and turns symmetric root data into Vieta. Retrieve the target-first habit; do not duplicate those derivations here.

### To functional equations

ALG-05 uses substitution strategically: choose inputs that expose a relation instead of plugging random values.

### To radicals and logarithms

ALG-06 owns domain and reversibility doctrine for those families. The transferable ALG-01 habit is to ask whether each transformation preserves equivalence.

### To integer equations

NT-04 often uses ALG-01 factorisation or substitution to create a finite integer structure, then applies number-theoretic restrictions.

---

## Final belief

> **I do not manipulate first and interpret later. I read the target, choose the cheapest representation, preserve conditions, and stop as soon as the requested information is determined.**
