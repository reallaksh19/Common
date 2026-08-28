# NMTC Bhaskara Preliminary — P0 Algebra First-Step Cards v1

## Purpose

Train the decision made **before** calculation.

Routine:

`SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`

These cards are grounded in the solution-qualified 2018, 2019, 2023, 2024 and 2025 Preliminary corpus. They do not reproduce full PYQ wording.

---

## Card A1 — High powers + low-degree relation

### SEE
You are given something like

`x^2 + px + q = 0`

but asked about `x^7`, `x^9`, or a large polynomial expression.

### REALIZE
Every power `x^n` with `n>=2` can be reduced to something linear in `x` using the given relation.

### WRITE

`x^2 = -px-q`

### CHOOSE
Reduce only as far as the target requires. Do **not** solve the quadratic unless individual roots are genuinely needed.

### CHECK
- Did you use the relation with the correct signs?
- Can the target be factored before repeated substitution?

### PYQ evidence
- 2018 Q06
- 2023 Q03
- 2024 Q01

### Tempting wrong move
Use the quadratic formula first, creating radicals that make the problem harder.

---

## Card A2 — Roots are present, but the target is symmetric

### SEE
The problem names roots `alpha, beta`, while the target contains expressions such as:

- `alpha^2+beta^2`;
- `alpha/beta + beta/alpha`;
- `1/alpha + 1/beta`;
- a shifted/root-transformed expression.

### REALIZE
The target may depend only on `alpha+beta` and `alpha beta`.

### WRITE
For `ax^2+bx+c=0`:

`alpha+beta = -b/a`

`alpha beta = c/a`

### CHOOSE
Rewrite the target in terms of sum/product **before** solving for either root.

### CHECK
- Is the target symmetric?
- Does it actually require knowing which root is which?
- Are roots positive/integer, adding extra constraints?

### PYQ evidence
- 2024 Q14
- 2024 Q17
- 2024 Q22 after function shift

### Tempting wrong move
Find both roots explicitly and substitute them into a long expression.

---

## Card A3 — Polynomial divisible by a factor

### SEE
A polynomial is stated to be divisible by `x-a`, `x^2+1`, `x^2-1`, or another low-degree polynomial.

### REALIZE
Divisibility means the remainder is zero.

### WRITE
For linear divisor:

`P(a)=0`

For quadratic divisor:

`P(x) = D(x)Q(x) + R(x)` with `deg R < deg D`.

### CHOOSE
Reduce powers modulo the divisor rather than performing unnecessary full division.

Examples:

- modulo `x^2-1`: `x^2 ≡ 1`;
- modulo `x^2+1`: `x^2 ≡ -1`;
- modulo `x^2+x+1`: `x^2 ≡ -x-1`.

### CHECK
Distinguish:

- `P(a)` for divisor `x-a`;
- substitution `x=a` is **not** generally valid for divisor `mx-a` unless you substitute its actual zero `a/m`.

### PYQ evidence
- 2018 Q06
- 2019 Q08
- 2024 Q05
- 2024 Q16

### Tempting wrong move
Carry out long division of a very high-degree polynomial term by term.

---

## Card A4 — Quartic/cubic looks frightening

### SEE
A cubic or quartic is presented, often with integer coefficients.

### REALIZE
Preliminary questions frequently expect reduction, not a general cubic/quartic formula.

### WRITE
Try, in order:

1. structural identity;
2. simple integer/rational root;
3. substitution (`x^2=t`, reciprocal, symmetric variable);
4. given relation / Vieta restriction.

### CHOOSE
Factor to lower degree as early as possible.

### CHECK
- Did you test obvious roots such as `±1`, factors of the constant term?
- Is the polynomial reciprocal/palindromic/symmetric?
- Are roots constrained to positive integers?

### PYQ evidence
- 2019 Q25
- 2024 Q24

### Source-custody warning
2025 Q20 belongs to this family mathematically, but is blocked as a canonical PYQ anchor because the reproduced sign and provisional key conflict.

---

## Card A5 — Conjugate radicals / surds

### SEE
Expressions like:

`A+B√d` and `A-B√d`, or nested radicals.

### REALIZE
They may be disguised squares/cubes or conjugates designed to cancel.

### WRITE
Test whether

`A±B√d = (√m ± √n)^2`

or introduce a common radical basis.

### CHOOSE
Reconstruct the simple object before raising to powers.

### CHECK
Square your reconstruction mentally/algebraically before using it.

### PYQ evidence
- 2018 Q01/Q21
- 2023 Q21/Q26
- 2025 Q04

### Tempting wrong move
Expand fractional powers directly.

---

## Card A6 — Mixed exponential bases

### SEE
Powers of 2, 3, 4, 8, 9, 27, etc., appear together.

### REALIZE
The bases are often related.

### WRITE
Rewrite all bases using the smallest useful common prime bases.

### CHOOSE
Introduce one variable only after normalization, e.g. `t=(2/3)^x`.

### CHECK
- Are bases positive?
- Are you matching exponents correctly?
- Is there an obvious factor before substitution?

### PYQ evidence
- 2023 Q07
- 2024 Q04/Q09

---

## Card A7 — Logarithm appears inside another operation

### SEE
A logarithm is squared, square-rooted, exponentiated, or coupled to another equation.

### REALIZE
The logarithm itself is often the natural algebra variable.

### WRITE
Examples:

`t = log_b x`

or, when the domain guarantees non-negativity,

`t = sqrt(log_b x)`.

### CHOOSE
Solve the algebraic equation in `t`, then map back to `x`.

### CHECK
Mandatory log domain:

- base positive and not 1;
- argument positive;
- square-rooted log nonnegative where applicable.

### PYQ evidence
- 2024 Q12/Q28
- 2025 Q12/Q27

### Tempting wrong move
Manipulate logs and exponents simultaneously without defining a simpler variable.

---

## Card A8 — Positive roots + fixed sum/product

### SEE
Several positive roots/numbers have fixed sum and product.

### REALIZE
Equality conditions can force all of them equal.

### WRITE
AM-GM or an equivalent bound, but only after confirming the quantity is bounded.

### CHOOSE
Use equality conditions to collapse the root set, then return to Vieta/coefficient comparison.

### CHECK
Before maximizing/minimizing ask:

`Is the requested quantity actually bounded?`

### PYQ evidence
- 2018 Q12
- 2024 Q17
- 2023 Q17 as the crucial **unbounded** contrast

### Tempting wrong move
Automatically apply AM-GM because the problem says “maximum” or “minimum.”

---

## Card A9 — Function shifted or composed

### SEE
You see `f(x+1)`, `f(f(x))`, or a fractional-linear function.

### REALIZE
The input transformation is usually simpler than solving the final equation directly.

### WRITE
For a shift, rename the input:

`y=x+1`.

For composition, compute the symbolic composition first.

### CHOOSE
Simplify the function structure before inserting roots/numbers.

### PYQ evidence
- 2024 Q22
- 2025 Q17

---

# Mixed recognition drill contract

The student must be shown unlabeled prompts and answer only one of:

- `REDUCE POWERS`;
- `VIETA`;
- `REMAINDER/MOD POLYNOMIAL`;
- `FACTOR FIRST`;
- `COMMON RADICAL BASIS`;
- `NORMALIZE EXPONENTIAL BASES`;
- `LOG VARIABLE`;
- `BOUND FIRST`;
- `SHIFT/COMPOSE FUNCTION`.

No calculation is allowed in the first pass.

Success criterion:

- at least 80% correct first-move classification on mixed direct/disguised items;
- student can state **why** the move applies;
- student can identify at least one nearby case where the same move would be wrong.
