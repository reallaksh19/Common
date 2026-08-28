# Radicals, Exponents & Logarithmic Transformations
## NMTC Bhaskara Preliminary — Student Concept Book Draft v0.1

> **Goal:** stop treating radicals, exponents and logarithms as three separate formula lists. Learn to change representation until the problem becomes small.

Use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

and while solving:

`RECOGNIZE -> FIRST MOVE -> SOLVE -> CHECK -> TRANSFER`.

---

# 0. Diagnostic

Try without notes.

1. Simplify `sqrt(48)`.
2. Simplify `cuberoot(54)`.
3. Is `sqrt(x^2)=x` always true?
4. Solve `2^x=16`.
5. Rewrite `8^(2/3)` using roots.
6. Convert `3^4=81` to logarithmic form.
7. State the domain of `log_2(x-5)`.
8. Is `log(a+b)=log a+log b` true in general?

### Answers

1. `4sqrt(3)`.
2. `3cuberoot(2)`.
3. No. `sqrt(x^2)=|x|` for real `x`.
4. `x=4`.
5. `(cuberoot(8))^2=4`.
6. `log_3 81=4`.
7. `x>5`.
8. No.

If several of these are uncertain, repair the foundation before speed training.

---

# 1. Radicals become easier when they speak the same language

## SEE

`sqrt(12)+sqrt(27)-sqrt(3)`

looks like three different radicals.

But:

`sqrt(12)=2sqrt(3)`

`sqrt(27)=3sqrt(3)`.

So the expression is simply:

`2sqrt(3)+3sqrt(3)-sqrt(3)=4sqrt(3)`.

## REALIZE

Many radical questions are not testing calculation. They are testing whether you can identify a **common radical basis**.

## UNDERSTAND

The move works because we extract perfect squares:

`sqrt(12)=sqrt(4·3)=2sqrt(3)`.

For cube roots:

`cuberoot(54)=cuberoot(27·2)=3cuberoot(2)`.

### Important contrast

You may split a product under suitable real conditions:

`sqrt(4·3)=sqrt(4)sqrt(3)`.

But you cannot split a sum:

`sqrt(4+5) != sqrt(4)+sqrt(5)`.

Indeed:

`3 != 2+sqrt(5)`.

## PYQ CONNECTION

Qualified Preliminary examples support this first move:

- `NMTC-BH-P-2018-Q01`;
- `NMTC-BH-P-2023-Q26`;
- `NMTC-BH-P-2025-Q03` extends the same idea to seventh roots/fractional exponents.

## ADOPT

Simplify:

A. `sqrt(20)+sqrt(45)`

B. `cuberoot(16)+cuberoot(54)`

### Answers

A. `2sqrt(5)+3sqrt(5)=5sqrt(5)`.

B. `2cuberoot(2)+3cuberoot(2)=5cuberoot(2)`.

---

# 2. A complicated surd may already be a square

## SEE

Expand:

`(sqrt(5)+2)^2`

`=5+4+4sqrt(5)`

`=9+4sqrt(5)`.

So if you see:

`sqrt(9+4sqrt(5))`,

you should not immediately use decimals.

You can reconstruct:

`9+4sqrt(5)=(sqrt(5)+2)^2`.

Because `sqrt(5)+2>0`, the principal square root is:

`sqrt(5)+2`.

## REALIZE

A nested radical often asks you to run expansion **backwards**.

## UNDERSTAND

To rewrite

`A+Bsqrt(d)`

as

`(sqrt(m)+sqrt(n))^2`,

match:

`m+n=A`

and

`2sqrt(mn)=Bsqrt(d)`.

### Example

Simplify:

`sqrt(14-6sqrt(5))`.

Try `(3-sqrt(5))^2`:

`9+5-6sqrt(5)=14-6sqrt(5)`.

Since `3-sqrt(5)>0`, answer:

`3-sqrt(5)`.

## WHY NOT? — expand fractional powers directly

If a question contains

`(52+6sqrt(43))^(3/2)`,

the useful question is:

> Is `52+6sqrt(43)` already a square?

Qualified 2025 Preliminary evidence uses exactly this structural behavior.

## PYQ CONNECTION

- `NMTC-BH-P-2023-Q21` — nested-radical reconstruction;
- `NMTC-BH-P-2025-Q04` — conjugate surds reconstructed as squares before `3/2` powers;
- `NMTC-BH-P-2024-Q26` — structured radical normalization.

---

# 3. Principal square roots: a small sign that causes big errors

## SEE

What is `sqrt((-7)^2)`?

It is:

`sqrt(49)=7`,

not `-7`.

Therefore:

`sqrt(x^2)=|x|`.

## REALIZE

The square root symbol means the **non-negative principal square root**.

## UNDERSTAND

If `x>=0`, then `sqrt(x^2)=x`.

If `x<0`, then `sqrt(x^2)=-x=|x|`.

### Contrast

`sqrt((x-3)^2)=|x-3|`, not automatically `x-3`.

This matters in equations and inequalities.

---

# 4. Reciprocal pairs can hide inside radicals

## SEE

Let:

`X=t+1/t`.

Then:

`X^2=t^2+2+1/t^2`.

So:

`t^2+1/t^2=X^2-2`.

Also:

`X^3=t^3+1/t^3+3(t+1/t)`.

Therefore:

`t^3+1/t^3=X^3-3X`.

## REALIZE

If a radical ratio naturally creates a number and its reciprocal, the target may be much easier as `X+1/X` or a power-sum identity.

## PYQ CONNECTION

- `NMTC-BH-P-2018-Q21`;
- `NMTC-BH-P-2025-Q09`.

## ADOPT

If `t+1/t=4`, find:

1. `t^2+1/t^2`;
2. `t^3+1/t^3`.

### Answers

1. `16-2=14`.
2. `64-12=52`.

No quadratic-root calculation was needed.

---

# 5. Radical equations: isolate first, square later

## SEE

Solve:

`sqrt(x+1)=x-1`.

Before squaring, the right side must be non-negative:

`x>=1`.

Now square:

`x+1=(x-1)^2`

`x+1=x^2-2x+1`

`x(x-3)=0`.

Algebra gives `x=0,3`.

But the original domain requires `x>=1`.

So only:

`x=3`.

## REALIZE

Squaring can create candidates that were not solutions of the original equation.

## UNDERSTAND

A safe routine:

1. write domain;
2. isolate the radical relation;
3. square only when useful;
4. solve;
5. check every candidate in the original equation.

### Worked example

Solve:

`sqrt(2x+3)=3sqrt(x-1)`.

Domain: `x>=1`.

Square:

`2x+3=9x-9`

`12=7x`

`x=12/7`.

This satisfies the domain and original equation.

## Square versus cube

For real numbers, squaring is not one-to-one:

`2^2=(-2)^2`.

Cubing **is** one-to-one:

if `a^3=b^3`, then `a=b` for real `a,b`.

That distinction matters when transforming radical equations.

## PYQ CONNECTION

- `NMTC-BH-P-2018-Q26` is a clean radical-ratio anchor.
- `NMTC-BH-P-2025-Q18` is **not** a normal exercise here because the printed equation and provisional-key convention conflict about distinct roots versus multiplicity after cubing. It belongs in source-integrity training.

---

# 6. Exponents: first make the bases compatible

## SEE

Solve:

`2^(2x)-5·2^x+4=0`.

The repeated object is `2^x`.

Set:

`t=2^x`.

Then:

`t^2-5t+4=0`

`(t-1)(t-4)=0`.

So:

`t=1 or 4`.

Therefore:

`x=0 or 2`.

## REALIZE

An exponential equation may actually be an ordinary quadratic wearing exponential clothing.

## UNDERSTAND

Before using logarithms, ask:

- Can all bases be rewritten as powers of one base?
- Can I divide by one exponential factor and create a ratio variable?

### Example with related bases

`4^x=8`.

Rewrite:

`2^(2x)=2^3`.

So:

`2x=3`, `x=3/2`.

No logarithms needed.

### Example with two prime bases

Suppose an equation contains `2^x` and `3^x` in homogeneous combinations.

Divide by `3^(2x)` or another suitable factor and set:

`t=(2/3)^x`.

Now solve algebraically in `t`.

## PYQ CONNECTION

- `NMTC-BH-P-2023-Q07`;
- `NMTC-BH-P-2024-Q04`;
- `NMTC-BH-P-2024-Q09`.

---

# 7. Logarithm is simply exponent language reversed

## SEE

`2^5=32`.

Ask:

> To what power must 2 be raised to get 32?

Answer: 5.

We write:

`log_2 32=5`.

These are the same statement:

`2^5=32 <=> log_2 32=5`.

## REALIZE

A logarithm is not a new mysterious number system. It records an exponent.

## UNDERSTAND — the domain

For real logarithms:

`log_b x`

requires:

- `b>0`;
- `b!=1`;
- `x>0`.

Why must `x>0`?

A positive base raised to a real power is always positive.

---

# 8. Build the log laws from exponent laws

Suppose:

`M=b^p`

and

`N=b^q`.

Then:

`MN=b^(p+q)`.

Therefore:

`log_b(MN)=p+q`

`=log_b M+log_b N`.

So the product law comes from adding exponents.

Similarly:

`M/N=b^(p-q)`

so:

`log_b(M/N)=log_b M-log_b N`.

And:

`M^k=b^(kp)`

so:

`log_b(M^k)=klog_b M`.

## Important false rule

There is no corresponding law:

`log(a+b)=log a+log b`.

Counterexample base 10:

`log(1+9)=log 10=1`,

but:

`log1+log9=0+log9`, which is not 1.

---

# 9. Choose the object that repeats

## SEE

Solve:

`log_2 x-3sqrt(log_2 x)+2=0`.

You could set:

`t=log_2 x`.

But then you still have `sqrt(t)`.

A cleaner choice is:

`u=sqrt(log_2 x)`.

Then:

`log_2 x=u^2`, and importantly `u>=0`.

The equation becomes:

`u^2-3u+2=0`

`(u-1)(u-2)=0`.

So:

`u=1 or 2`.

Therefore:

`log_2 x=1 or 4`.

Hence:

`x=2 or 16`.

## REALIZE

The best substitution is often the **whole repeated object**, not the innermost expression.

## PYQ CONNECTION

- `NMTC-BH-P-2024-Q12`;
- `NMTC-BH-P-2025-Q12`.

---

# 10. Log systems often hide simple algebra

## SEE

Suppose:

`log_4 x=log_2 y`.

Rewrite the left side in base 2:

`log_4 x=(log_2 x)/(log_2 4)=(1/2)log_2 x`.

So:

`(1/2)log_2 x=log_2 y`.

Multiply by 2:

`log_2 x=2log_2 y=log_2(y^2)`.

Since log base 2 is one-to-one on positive inputs:

`x=y^2`.

Do not forget:

`x>0`, `y>0`.

## Example

Add:

`x-y=6`.

Then:

`y^2-y=6`

`y^2-y-6=0`

`(y-3)(y+2)=0`.

Log domain requires `y>0`, so `y=3`.

Then `x=9`.

## PYQ CONNECTION

- `NMTC-BH-P-2025-Q27`.

---

# 11. Exact log-exponent simplification beats decimals

## SEE

`2^(log_2 7)`.

By definition, `log_2 7` is exactly the exponent that turns 2 into 7.

Therefore:

`2^(log_2 7)=7`.

## REALIZE

If logarithms and exponents use compatible bases, exact cancellation is often intended.

## UNDERSTAND

The identity:

`b^(log_b x)=x`

is simply the inverse relationship between exponentiation and logarithm.

### Example

Simplify:

`(10^(-1/2))^(-2log_10 5)`.

Combine exponents:

`10^((-1/2)(-2log_10 5))`

`=10^(log_10 5)`

`=5`.

No calculator needed.

## PYQ CONNECTION

- `NMTC-BH-P-2024-Q28`.

---

# 12. FIRST-MOVE LAB — do not solve

Choose one label:

`COMMON BASIS / RECONSTRUCT SURD / RECIPROCAL / RADICAL EQUATION / NORMALIZE BASES / LOG VARIABLE / LOG TO ALGEBRA / EXACT LOG-EXPONENT / DOMAIN CHECK`.

1. `sqrt(75)+sqrt(12)-sqrt(3)`.
2. `sqrt(9+4sqrt5)`.
3. `t+1/t` is known; `t^3+1/t^3` is asked.
4. `sqrt(x+3)=2sqrt(x-2)`.
5. `4^x+2^x` appears together.
6. `(log_3 x)^2-5log_3 x+6=0`.
7. `sqrt(log_2 x)` appears three times.
8. `log_9 x=log_3 y`.
9. `5^(log_5 13)`.
10. `sqrt((x-4)^2)`.

### Classification

1. COMMON BASIS
2. RECONSTRUCT SURD
3. RECIPROCAL
4. RADICAL EQUATION
5. NORMALIZE BASES
6. LOG VARIABLE
7. LOG VARIABLE — choose the square-root log itself
8. LOG TO ALGEBRA
9. EXACT LOG-EXPONENT
10. DOMAIN/SIGN CHECK: `|x-4|`

---

# 13. Mixed self-test

## Q1
Simplify:

`(sqrt(50)+sqrt(8))/sqrt(2)`.

## Q2
Simplify:

`sqrt(11+6sqrt(2))`.

## Q3
If `t+1/t=5`, find `t^3+1/t^3`.

## Q4
Solve:

`sqrt(3x+1)=2sqrt(x-2)`.

## Q5
Solve:

`9^x-10·6^x+9·4^x=0`.

## Q6
Solve:

`(log_2 x)^2-5log_2 x+4=0`.

## Q7
Solve:

`log_3 x-5sqrt(log_3 x)+6=0`.

## Q8
Positive `x,y` satisfy:

`log_9 x=log_3 y`

and

`x-y=6`.

Find `x+y`.

## Q9
Simplify exactly:

`3^(log_3 11)`.

## Q10
Is `sqrt(x^2)=x` valid for all real `x`? State the correct identity.

---

# 14. Answers

## A1
`sqrt50=5sqrt2`, `sqrt8=2sqrt2`; numerator `7sqrt2`; divide by `sqrt2`: `7`.

## A2
`11+6sqrt2=(3+sqrt2)^2`, so answer `3+sqrt2`.

## A3
`5^3-3·5=125-15=110`.

## A4
Domain `x>=2`.

Square:

`3x+1=4x-8` -> `x=9`.

Valid.

## A5
Divide by `4^x>0`:

`(9/4)^x-10(3/2)^x+9=0`.

Set `u=(3/2)^x>0`:

`u^2-10u+9=0`.

`u=1 or 9`.

Thus `x=0` or `x=log_(3/2)9`.

## A6
Let `t=log_2 x`.

`t^2-5t+4=0`, so `t=1,4`.

`x=2,16`.

## A7
Let `u=sqrt(log_3 x)>=0`.

`u^2-5u+6=0`, so `u=2,3`.

`log_3 x=4,9`.

`x=81,19683`.

## A8
`log_9 x=(1/2)log_3 x=log_3 y`.

So `x=y^2`.

`y^2-y=6`, positive `y=3`, `x=9`.

Answer `12`.

## A9
`11`.

## A10
No. Correct identity:

`sqrt(x^2)=|x|`.

---

# 15. Source-integrity lesson

Sometimes the algebra you derive from a printed question disagrees with an answer key.

Do not force agreement.

For a radical equation:

1. decide whether your transformation is reversible;
2. distinguish distinct original solutions from multiplicity in a transformed polynomial;
3. compare the exact source statement and key;
4. mark the source conflict if it remains.

`NMTC-BH-P-2025-Q18` is retained in the corpus for exactly this reason and is **not** used as a clean scored anchor in this book.

---

# 16. Mastery checklist

You should be able to say YES to all:

- [ ] I reduce radicals to a common basis before calculating.
- [ ] I can reverse-engineer a hidden square from `A±Bsqrt(d)`.
- [ ] I know `sqrt(x^2)=|x|`.
- [ ] I isolate radical equations before squaring.
- [ ] I verify candidates after squaring.
- [ ] I normalize exponential bases before reaching for logarithms.
- [ ] I can explain a logarithm as an exponent.
- [ ] I can derive the product/quotient/power log laws.
- [ ] I know the real-log domain conditions.
- [ ] I choose the whole repeated log object as a substitution.
- [ ] I convert log systems to algebra and restore domains.
- [ ] I use exact inverse log/exponent structure before decimal approximation.
- [ ] I can identify a source/convention conflict rather than silently repairing it.

## Draft state

`STUDENT_DRAFT_v0.1`

Still required:

- reviewed transfer bank;
- timed recognition/first-line labs;
- mixed mastery test;
- item-level difficulty vectors;
- second editorial/math pass;
- publication/render QA.
