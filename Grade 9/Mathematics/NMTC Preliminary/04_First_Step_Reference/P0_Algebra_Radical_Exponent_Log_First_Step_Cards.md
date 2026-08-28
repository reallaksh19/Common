# NMTC Bhaskara Preliminary — Radical / Exponent / Log First-Step Cards v1

## Routine

`SEE -> REALIZE -> WRITE -> CHOOSE -> CHECK`

The first useful move matters more than the number of formulas remembered.

---

## Card R1 — Several radicals, same hidden basis

### SEE
Terms such as `sqrt(12), sqrt(27), sqrt(3)` or several cube roots built from the same prime factors.

### REALIZE
The expression may use only one or two independent radicals.

### WRITE
Extract perfect powers first.

### CHOOSE
Rewrite every term in a common radical basis, then factor/cancel.

### CHECK
Never use the false rule `sqrt(a+b)=sqrt(a)+sqrt(b)`.

### PYQ evidence
- 2018 Q01
- 2023 Q26
- 2025 Q03 as nth-root extension

---

## Card R2 — `A±B√d` looks engineered

### SEE
Conjugate surds, nested radicals, fractional powers.

### REALIZE
The surd may already be a square:

`(sqrt(m)±sqrt(n))^2=m+n±2sqrt(mn)`.

### WRITE
Match:

`m+n=A`, `2sqrt(mn)=Bsqrt(d)`.

### CHOOSE
Reconstruct before taking the requested power.

### CHECK
Square your proposed reconstruction before using it.

### PYQ evidence
- 2023 Q21
- 2025 Q04
- 2024 Q26

---

## Card R3 — Reciprocal radical pair

### SEE
A ratio or pair naturally produces `t` and `1/t`.

### REALIZE
The requested target may be symmetric in the reciprocal pair.

### WRITE
Try:

`x=t+1/t`.

### CHOOSE
Use identities for `x^2`, `x^3`, etc.; do not solve `t` unless required.

### PYQ evidence
- 2018 Q21
- 2025 Q09

---

## Card R4 — Radical equation

### SEE
Square roots/nth roots on both sides.

### REALIZE
Squaring too early creates cross terms and may create extraneous roots.

### WRITE
First write domain restrictions.

### CHOOSE
Isolate radicals, then square only as needed.

### CHECK
Substitute every candidate into the original equation.

### PYQ evidence
- 2018 Q26

### Source-QC contrast
- 2025 Q18: use only to discuss distinct original roots versus multiplicity after cubing and the provisional-key conflict.

---

## Card E1 — Related exponential bases

### SEE
Bases such as `2,4,8` or `3,9,27`, or ratios of related bases.

### REALIZE
They are powers of a common base.

### WRITE
Rewrite all bases first.

### CHOOSE
Then set one variable such as `t=2^x` or `t=(2/3)^x` if it makes the equation algebraic.

### CHECK
Do not introduce logarithms if common-base normalization already solves the structural problem.

### PYQ evidence
- 2023 Q07
- 2024 Q04/Q09

---

## Card E2 — Fractional exponent on a surd

### SEE
Something like `(A+B√d)^(3/2)`.

### REALIZE
The base may be a perfect square of a simpler surd.

### WRITE
Try `A+B√d=(sqrt(m)+sqrt(n))^2`.

### CHOOSE
Convert the fractional exponent only after reconstruction.

### PYQ evidence
- 2025 Q04

---

## Card L1 — Logarithm meaning is enough

### SEE
A simple equality of logs/powers.

### REALIZE
`log_b x=y` means `b^y=x`.

### WRITE
Convert to exponent form.

### CHOOSE
Use the simplest language—log or exponent—rather than manipulating both at once.

### CHECK
`b>0`, `b!=1`, `x>0`.

---

## Card L2 — A log expression repeats

### SEE
`log_b x`, `(log_b x)^2`, or `sqrt(log_b x)` appears repeatedly.

### REALIZE
The whole repeated object is the natural algebra variable.

### WRITE
Examples:

`t=log_b x`

or

`t=sqrt(log_b x)`.

### CHOOSE
Solve in `t`, then map back.

### CHECK
If `t=sqrt(log_b x)`, then `t>=0`.

### PYQ evidence
- 2024 Q12
- 2025 Q12

---

## Card L3 — Log system hides a power relation

### SEE
Different log bases connect `x,y`.

### REALIZE
Convert to a common base or exponent form.

### WRITE
Example pattern:

`log_4 x=log_2 y`

becomes

`(1/2)log_2 x=log_2 y`, hence `x=y^2`, with positive arguments.

### CHOOSE
Solve the resulting algebraic system.

### CHECK
Restore every original log-domain restriction.

### PYQ evidence
- 2025 Q27

---

## Card L4 — Logarithm sits in an exponent

### SEE
An exact power contains a log in the exponent.

### REALIZE
Use inverse exponent/log structure before decimal approximation.

### WRITE
Seek forms such as

`b^(log_b x)=x`.

### CHOOSE
Change base only when it creates exact cancellation.

### PYQ evidence
- 2024 Q28

---

# Contrast pairs

1. common radical basis vs direct decimal approximation;
2. reconstruct surd vs expand fractional power;
3. isolate/square vs square entire radical equation immediately;
4. common-base exponent normalization vs unnecessary logarithms;
5. `t=log x` vs `t=sqrt(log x)` — choose what repeats;
6. algebraic root after squaring vs verified root of original equation;
7. distinct original solutions vs multiplicity in a transformed polynomial;
8. valid log algebra vs ignored domain.

# Recognition success criterion

On 20 mixed unlabeled prompts, student should correctly name the first-move family for at least 16 and explain why for at least 12.
