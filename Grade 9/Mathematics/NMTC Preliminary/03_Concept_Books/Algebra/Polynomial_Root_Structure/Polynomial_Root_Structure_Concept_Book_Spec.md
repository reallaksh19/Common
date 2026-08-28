# Polynomial & Root Structure — Concept Book Specification v1

## Cognitive contract

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Mathematical mastery target:

`FORM -> ROOT/REMAINDER RELATION -> REDUCTION -> INVARIANT -> TRANSFER`

The student should finish this unit believing:

> I do not solve a polynomial because it is present. I first ask what information the problem actually needs.

---

# Unit architecture

## Unit 0 — Diagnostic: are the foundations really ready?

Before teaching, test without hints:

1. factor common quadratics and differences of squares/cubes;
2. evaluate a polynomial at a number;
3. expand `(x+a)^2`, `(x+a)^3`;
4. solve a basic quadratic by factorization;
5. manipulate powers using a supplied relation;
6. distinguish an equation from an identity;
7. identify domain restrictions in a rational expression.

If these fail, route to foundation repair before P0 NMTC work.

---

## Unit 1 — One polynomial, three useful views

### SEE
Show the same object in three representations:

`P(x)=x^2-5x+6`

`P(x)=(x-2)(x-3)`

roots: `2,3`

Then ask:

- Which view makes evaluation easiest?
- Which view makes roots easiest?
- Which view exposes coefficient information?

### REALIZE
No representation is “the polynomial.” They are equivalent views chosen for different jobs.

### UNDERSTAND
Connect:

- coefficients;
- factors;
- roots;
- graph intercepts;
- evaluation.

### CONTRAST
`P(2)=0` means `x-2` is a factor.

`P(2)=5` does **not** mean `x-5` is a factor.

### ADOPT
Given several polynomials and several tasks, choose the best representation **without solving**.

---

## Unit 2 — Reduce powers instead of solving roots

### SEE
Start with a visible recurrence:

If

`x^2+x+1=0`,

then

`x^2=-x-1`.

Generate:

`x^3=1`,

`x^4=x`,

`x^5=x^2`, ...

before giving any general language.

### REALIZE
A low-degree equation acts as a **rewriting rule** for every higher power.

### UNDERSTAND
Explain why polynomial expressions can be reduced modulo the relation.

For a quadratic relation, every high-degree expression eventually becomes linear in `x`.

### PYQ anchor family
- 2018 Q06;
- 2023 Q03;
- 2024 Q01.

### WRONG MOVE
Quadratic formula -> radical roots -> substitute into seventh/eighth powers.

Ask the learner why that creates unnecessary information.

### REBUILD
If the reduction rule is forgotten, recreate it directly from the given equation.

---

## Unit 3 — Remainder Theorem from division, not memorization

### SEE
Use ordinary division first:

`17 = 5·3 + 2`.

Then polynomial division:

`P(x)=(x-a)Q(x)+r`.

### REALIZE
At `x=a`, the entire multiple of `x-a` disappears.

### UNDERSTAND
Substitute:

`P(a)=r`.

Derive Factor Theorem as the special case `r=0`.

### CONTRAST
For divisor `2x-3`, the zero is `x=3/2`, not `x=3`.

The student must reject the false rule “plug in the constant.”

### ADOPT
Mix divisors:

- `x-4`;
- `x+2`;
- `3x-6`;
- `x^2+1`.

Ask which ones permit one-point substitution and which require a remainder polynomial.

---

## Unit 4 — Polynomial arithmetic modulo a divisor

### SEE
For divisor `x^2-1`, show:

`x^2 ≡ 1`, hence

`x^6 ≡ 1`, `x^7 ≡ x`.

For divisor `x^2+1`:

`x^2 ≡ -1`, giving a four-step power cycle.

### REALIZE
Remainder problems often become **small power cycles**.

### UNDERSTAND
Explain that `≡` here means “has the same remainder modulo the polynomial divisor,” analogous in spirit to integer modular arithmetic.

### PYQ anchors
- 2019 Q08 (`x^2-1`);
- 2024 Q05 (`x^2+1` divisibility);
- 2024 Q16 (periodic quotient/coefficient behavior).

### TRANSFER
Use a new divisor such as `x^2+x+1` and ask the learner to derive its reduction cycle.

---

## Unit 5 — Vieta: information about roots without finding roots

### SEE
For

`x^2-7x+10=0`,

factor to roots `2,5`.

Observe:

`2+5=7`,

`2·5=10`.

Repeat with a non-factor-friendly quadratic and reveal that the coefficient relations still hold.

### REALIZE
The coefficients already contain the sum/product information.

### UNDERSTAND
From

`a(x-alpha)(x-beta)`

derive:

`alpha+beta=-b/a`,

`alpha beta=c/a`.

Do not present these as naked formulas.

### ADOPT — rewrite target first

Train:

`alpha^2+beta^2=(alpha+beta)^2-2alpha beta`

`1/alpha+1/beta=(alpha+beta)/(alpha beta)`

`alpha/beta+beta/alpha=((alpha+beta)^2-2alpha beta)/(alpha beta)`

The student should choose these transformations independently.

### PYQ anchor
2024 Q14 is a strong clean anchor: recover the original quadratic, then use Vieta for a transformed-root ratio rather than solving the roots.

---

## Unit 6 — Transformed roots

### SEE
If roots are `alpha,beta`, ask for the equation whose roots are:

- `alpha+1, beta+1`;
- `1/alpha,1/beta`;
- `alpha^2,beta^2`.

### REALIZE
New roots can often be handled through their new sum and product.

### UNDERSTAND
Derive each transformation from the original root invariants.

Alternative representation: change the variable directly, e.g. `y=x+1`.

### PYQ anchor
2024 Q22: input shift first, then root recovery.

### CONTRAST
A shift in the **input** of a function is not the same as adding a constant to its **output**.

---

## Unit 7 — Positive/integer roots are extra equations

### SEE
Compare:

“roots are real”

versus

“roots are positive integers.”

### REALIZE
Integer/positive restrictions drastically reduce possibilities.

### UNDERSTAND
Use:

- sum/product factor pairs;
- parity/divisibility;
- AM-GM equality conditions;
- bounds.

### PYQ anchors
- 2024 Q17: positive roots + fixed sum/product force equality;
- 2023 Q13: integer Diophantine/discriminant reasoning provides a nearby bridge.

### SOURCE-QC contrast
2025 Q20 is useful to teach source checking: the root constraints imply one coefficient sign, while the provisional key matches the opposite sign. Do not use as a normal exercise until source custody is resolved.

---

## Unit 8 — Cubics and quartics: reduce before using heavy machinery

### SEE
Present a quartic with an easy root such as `x=1`.

### REALIZE
A higher degree does not imply a higher-degree formula is the intended method.

### UNDERSTAND
First-move ladder:

1. factor a visible identity;
2. test easy integer/rational roots;
3. look for `x^2=t`;
4. look for reciprocal/symmetric structure;
5. use Vieta/integer-root restrictions;
6. only then consider heavier algebra.

### PYQ anchors
- 2019 Q25: symmetric high-degree reduction;
- 2024 Q24: test simple roots, factor, then handle remaining quadratic.

### BONUS bridge
2023 Q16: common-root elimination, clearly labeled bonus evidence.

---

## Unit 9 — Common roots and elimination

### SEE
Two polynomials share a root. Ask whether solving each polynomial separately is efficient.

### REALIZE
At the common root, both equations hold simultaneously; subtracting/composing can eliminate powers.

### UNDERSTAND
Use low-degree combinations of equations to eliminate the highest power or the shared parameter.

### ADOPT
Author-created transfer items should vary degrees and coefficients while preserving the elimination invariant.

---

## Unit 10 — Error-check laboratory

This section is mandatory for Preliminary robustness.

### Contrast 1 — Solve vs reduce
Given a quadratic relation and target `x^8+...`, choose between:

- quadratic formula;
- power reduction.

Explain why.

### Contrast 2 — Vieta vs explicit roots
Given an ugly quadratic and target symmetric in roots, choose Vieta.

### Contrast 3 — linear divisor vs quadratic divisor
Explain why one-point substitution solves one but not the other.

### Contrast 4 — equation vs identity
A relation true for roots cannot automatically be treated as a polynomial identity for all `x`.

### Contrast 5 — source/key conflict
Use an abstracted version of the 2025 Q20 custody issue:

- derive what the printed stem implies;
- compare against a supplied key;
- mark `SOURCE_CONFLICT` rather than forcing agreement.

---

# ADOPT laboratory

No chapter labels are shown.

Learner must classify each unseen prompt by first move:

- `REDUCE POWERS`;
- `VIETA`;
- `REMAINDER`;
- `FACTOR FIRST`;
- `COMMON ROOT ELIMINATION`;
- `INTEGER ROOT CONSTRAINT`;
- `SOURCE CHECK`.

Then solve only after classification.

## Mastery standard

Student is ready for mixed Preliminary use only if they can:

1. classify at least 8/10 first moves correctly;
2. justify the classification;
3. solve at least 7/10 compact items correctly;
4. reject a plausible wrong method in at least 4/5 contrast items;
5. rebuild Vieta and Remainder Theorem if formulas are removed;
6. solve one non-identical transfer problem for every major archetype.

---

# Source and extension boundary

PYQ-derived structure is grounded through the separate Source Coverage Map.

Do not reproduce entire third-party paper statements as ordinary chapter text.

Use:

- short mathematical descriptions;
- stable PYQ IDs;
- source locators;
- original author-created foundation/transfer problems.

Bonus/starred/source-conflicted PYQs must retain their exact disposition and must not be presented as clean scored anchors.
