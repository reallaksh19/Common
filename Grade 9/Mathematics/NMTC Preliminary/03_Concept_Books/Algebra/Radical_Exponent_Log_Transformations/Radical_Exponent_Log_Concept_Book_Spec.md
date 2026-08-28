# Radicals, Exponents & Logarithmic Transformations — Concept Book Specification v1

## Cognitive contract

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Preliminary performance contract:

`RECOGNIZE FORM -> CHANGE REPRESENTATION -> SOLVE SMALLER PROBLEM -> CHECK DOMAIN -> TRANSFER`

Mastery target:

> The student does not attack a radical, exponent or logarithm merely in the form presented. They first ask which equivalent representation exposes the structure.

---

# Unit architecture

## Unit 0 — prerequisite diagnostic

Without notes, test:

1. simplify `sqrt(12)`;
2. simplify `a^(3/2)` for `a>=0`;
3. state whether `sqrt(x^2)=x` is always true;
4. solve `2^x=8`;
5. translate `log_2 8=3` into exponential form;
6. simplify `log_b(MN)` under valid domains;
7. identify the domain of `log_3(x-1)`;
8. explain why squaring both sides of an equation can add solutions.

Route foundational failures to repair before NMTC transformation work.

---

## Unit 1 — Radical language: simplify to a common basis

### SEE

`sqrt(12), sqrt(27), sqrt(3)` look different.

But:

`sqrt(12)=2sqrt(3)`

`sqrt(27)=3sqrt(3)`.

Now all terms speak the same language.

### REALIZE

A complicated radical expression may contain only one or two independent radical building blocks.

### UNDERSTAND

Teach:

- extracting perfect powers;
- square-root/cube-root bases;
- negative/fractional exponents as equivalent notation;
- when radical combination is legal and when it is not.

### CONTRAST

`sqrt(a+b)` is not generally `sqrt(a)+sqrt(b)`.

`sqrt(ab)=sqrt(a)sqrt(b)` needs suitable real-domain conditions.

### PYQ grounding

- 2018 Q01;
- 2023 Q26;
- 2025 Q03 as nth-root extension.

### ADOPT

Give surface-different expressions that collapse after one common-basis substitution.

---

## Unit 2 — Reconstruct a hidden square/cube before raising powers

### SEE

Show:

`(sqrt(m)+sqrt(n))^2=m+n+2sqrt(mn)`.

Then reverse the direction:

`A+Bsqrt(d)` may already be a square.

### REALIZE

Nested or conjugate surds are often deliberately built from simple binomial squares/cubes.

### UNDERSTAND

Train reconstruction using:

`m+n=A`

`2sqrt(mn)=Bsqrt(d)`.

Then use conjugate identities:

`(u+v)^3-(u-v)^3=6u^2v+2v^3`

only after the simpler `u,v` have been exposed.

### PYQ grounding

- 2023 Q21;
- 2025 Q04;
- 2024 Q26.

### WRONG MOVE

Raise `A+Bsqrt(d)` directly to fractional/high powers and expand blindly.

---

## Unit 3 — Reciprocal and symmetric radical variables

### SEE

If `x=t+1/t`, then expressions in `x^2`, `x^3` may collapse without finding `t`.

### REALIZE

Reciprocal pairs are another representation switch, closely related to Vieta/symmetric-expression thinking.

### UNDERSTAND

Derive:

`(t+1/t)^2=t^2+2+t^-2`

`(t+1/t)^3=t^3+t^-3+3(t+1/t)`.

### PYQ grounding

- 2018 Q21;
- 2025 Q09 as a radical-ratio route to `x+1/x`.

### ADOPT

Use author-created reciprocal radical pairs with changed bases and targets.

---

## Unit 4 — Radical equations: isolate, transform, verify

### SEE

Compare:

`sqrt(x+5)=2sqrt(x-1)`

with an equation containing several radical sums.

### REALIZE

Squaring should be delayed until radicals have been isolated as far as possible.

### UNDERSTAND

Required order:

1. write real-domain restrictions;
2. isolate one radical relation;
3. square only when necessary;
4. solve the resulting algebra;
5. substitute into the original equation.

Teach explicitly:

- squaring is not one-to-one over real numbers;
- cubing is one-to-one over real numbers;
- transformed polynomial multiplicity is not automatically the number of distinct roots of the original radical equation.

### PYQ grounding

- 2018 Q26 clean;
- 2025 Q18 source/convention contrast only.

---

## Unit 5 — Exponent laws as representation tools

### SEE

`8^x`, `4^x`, `2^x` are not three unrelated objects.

They are:

`2^(3x), 2^(2x), 2^x`.

### REALIZE

Mixed-base exponential equations often become ordinary algebra after common-base normalization.

### UNDERSTAND

Rebuild/verify:

- `a^m a^n=a^(m+n)`;
- `(a^m)^n=a^(mn)`;
- `a^-n=1/a^n`;
- rational exponents under valid real conditions.

Then use one variable:

`t=a^x` or `t=(a/b)^x`.

### PYQ grounding

- 2023 Q07;
- 2024 Q04;
- 2024 Q09.

### CONTRAST

Do not introduce logarithms if common-base normalization already makes the equation algebraic in one step.

---

## Unit 6 — Logarithm means exponent

### SEE

`2^5=32`

and

`log_2 32=5`

are the same statement in two languages.

### REALIZE

Logarithms are inverse exponent notation, not a separate mysterious operation.

### UNDERSTAND

Definition:

`log_b x=y <=> b^y=x`

with:

`b>0`, `b!=1`, `x>0`.

Derive laws from exponent laws:

`log_b(MN)=log_b M+log_b N`

`log_b(M/N)=log_b M-log_b N`

`log_b(M^k)=k log_b M`.

Do not give these as naked rules.

### CONTRAST

`log(a+b)` does not split into `log a+log b`.

---

## Unit 7 — Choose the repeated logarithmic object as the variable

### SEE

If an equation repeatedly contains `sqrt(log_2 x)`, compare substitutions:

`t=log_2 x`

versus

`u=sqrt(log_2 x)`.

### REALIZE

The best variable is the object repeated in the expression—not necessarily the innermost operation.

### UNDERSTAND

Teach mapping back carefully:

if `u=sqrt(log_2 x)`, then `u>=0` and

`log_2 x=u^2`, so `x=2^(u^2)`.

### PYQ grounding

- 2024 Q12;
- 2025 Q12.

### ADOPT

Use equations with `log`, squared log, square-rooted log and exponent-of-log surfaces. Student selects substitution before solving.

---

## Unit 8 — Convert logarithmic systems back to algebra

### SEE

`log_4 x=log_2 y`.

Because `log_4 x=(1/2)log_2 x`, the relation implies:

`log_2 x=2log_2 y=log_2(y^2)`.

With positive log arguments:

`x=y^2`.

### REALIZE

A log equation often encodes a simple power relation.

### UNDERSTAND

Required sequence:

1. write domain;
2. express logs in a common base or exponent form;
3. use injectivity of the valid logarithm/exponential;
4. solve the resulting algebraic system;
5. recheck positivity/domain.

### PYQ grounding

- 2025 Q27;
- 2024 Q28 as an exact exponent/log simplification bridge.

---

## Unit 9 — Exact log/exponent simplification

### SEE

Expressions such as

`a^(log_b c)`

or powers whose exponents contain a logarithm often look numerical but are structural.

### REALIZE

Convert everything to a common exponential/log language before approximating.

### UNDERSTAND

Useful identities should be derived, not memorized blindly, e.g. for positive valid quantities:

`b^(log_b x)=x`.

Use change-of-base only when it simplifies the structure.

### PYQ grounding

- 2024 Q28.

### WRONG MOVE

Use decimal logarithm approximations too early and lose exact simplification.

---

## Unit 10 — Error and source-integrity laboratory

Mandatory contrasts:

1. `sqrt(x^2)` vs `x` — principal root gives `|x|`.
2. squaring vs cubing equations — different reversibility.
3. common-base exponent route vs unnecessary logs.
4. repeated-log substitution choice.
5. log argument/base domain.
6. source/key conflict after algebraic transformation.

### Source-QC example family

2025 Q18 is retained only as a source/convention case:

- solve the printed real radical/cube-root equation;
- distinguish the distinct original solution set from multiplicity in the transformed polynomial;
- do not overwrite the mathematics to match a provisional key.

---

# First-move vocabulary for ADOPT lab

Student classifies unseen prompts as:

- `COMMON RADICAL BASIS`
- `RECONSTRUCT SURD`
- `RECIPROCAL INVARIANT`
- `ISOLATE THEN SQUARE`
- `NORMALIZE EXPONENTIAL BASES`
- `EXPONENTIAL VARIABLE`
- `LOG DEFINITION`
- `LOG VARIABLE`
- `LOG TO ALGEBRA`
- `DOMAIN CHECK`
- `SOURCE/CONVENTION CHECK`

No chapter label is shown before attempt.

---

# Mastery standard

The student must be able to:

1. derive the log laws from exponent laws;
2. explain why `sqrt(x^2)=|x|`;
3. recognize at least 8/10 transformation families without calculation;
4. solve radical equations and reject extraneous roots;
5. choose common-base exponent normalization before logs when cheaper;
6. choose the correct repeated log object as substitution;
7. restore log-domain restrictions after algebraic solving;
8. solve non-identical transfer problems from each major family;
9. detect a source/convention inconsistency instead of forcing the key.

## Source boundary

Full PYQ statements are not reproduced here. Stable IDs and mechanism descriptions are maintained in the Source Coverage Map.

`PUBLICATION_STATUS: NOT_READY`
