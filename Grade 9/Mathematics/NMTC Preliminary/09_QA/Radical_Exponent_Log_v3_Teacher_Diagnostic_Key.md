# Radicals, Exponents & Logarithmic Transformations v3 — Teacher / Diagnostic Key

This key belongs **outside the student attempt surfaces**. It covers the v3 Assimilation Book only; the Wave-4 mixed-mastery bank retains its separate answer/diagnostic key.

All numerical/algebraic conclusions below were independently recomputed before this file was promoted.

---

# 1. Reconnect diagnostic

| Item | Expected response | Diagnostic bridge if missed |
|---:|---|---|
| 1 | \(6\sqrt2\) | common radical basis |
| 2 | \(|x-4|\) | principal-root model |
| 3 | \(1/8\) | negative/fractional exponent meaning |
| 4 | \(x=2\) | common-base normalization |
| 5 | No; squaring is not one-to-one on \(\mathbb R\) | reversibility |
| 6 | division assumes \(x-2\neq0\) and deletes \(x=2\) | zero-case custody |
| 7 | \(14\) | reciprocal invariant |
| 8 | \(3^4=81\) | log/exponent definition |
| 9 | \(x>5\) | log-domain meaning |
| 10 | No | false log-sum analogy |
| 11 | \(v\ge0\), with original \(x>0\) | substitution range/domain |
| 12 | divide by \(4^x>0\), set \(t=(3/2)^x>0\) | ratio-variable recognition |

Suggested diagnosis is bridge-specific; do not convert it into a fixed learner label.

---

# 2. TRY A — radicals

## A1

\[
\sqrt{98}=7\sqrt2,\qquad \sqrt8=2\sqrt2,
\]

so

\[
\frac{\sqrt{98}-\sqrt8}{\sqrt2}=5.
\]

**Answer:** \(5\).

## A2

\[
13-4\sqrt{10}=(\sqrt8-\sqrt5)^2.
\]

Because \(\sqrt8-\sqrt5>0\),

\[
\sqrt{13-4\sqrt{10}}=2\sqrt2-\sqrt5.
\]

## A3

\[
\sqrt{(3x+1)^2}=|3x+1|.
\]

It equals \(3x+1\) iff

\[
x\ge-\frac13.
\]

## A4

Each denominator rationalizes with denominator \(7-2=5\):

\[
\frac{\sqrt7-\sqrt2}{5}+\frac{\sqrt7+\sqrt2}{5}
=\frac{2\sqrt7}{5}.
\]

## A5

\[
\sqrt[3]{16}=2\sqrt[3]2,\qquad
\sqrt[3]{54}=3\sqrt[3]2.
\]

Therefore the result is

\[
4\sqrt[3]2.
\]

---

# 3. TRY B — exponents

## B1

\[
27^{-2/3}=\frac1{(\sqrt[3]{27})^2}=\frac19.
\]

## B2

\[
16^x=8^{x+1}
\iff 2^{4x}=2^{3x+3}
\iff x=3.
\]

## B3

Set \(t=3^x>0\):

\[
t^2-10t+9=(t-1)(t-9)=0.
\]

Thus

\[
x=0,2.
\]

## B4

Divide by \(4^x>0\) and set \(t=(3/2)^x>0\):

\[
t^2-5t+4=0.
\]

So

\[
t=1,4
\]

and

\[
\boxed{x=0\quad\text{or}\quad x=\log_{3/2}4}.
\]

## B5

\[
32^{3/5}=8,\qquad 8^{-2/3}=\frac14.
\]

**Answer:** \(2\).

---

# 4. TRY C — reversibility

## C1

Original side-sign restriction: \(x\ge1\).

On that domain squaring is reversible:

\[
x+1=(x-1)^2.
\]

Candidates are \(0,3\); only \(3\) satisfies \(x\ge1\).

**Answer:** \(3\).

## C2

Original domain: \(x\ge1\). Both sides are non-negative there, so squaring is reversible:

\[
2x+3=9(x-1).
\]

Hence

\[
x=\frac{12}{7}.
\]

It satisfies the original equation.

## C3

Zero-product rule:

\[
x=2,-3.
\]

## C4

1. \(x=2\Rightarrow x^2=4\): only \(\Rightarrow\).
2. \(a=b\iff a^3=b^3\) over reals: \(\iff\).
3. valid \(\log_2x=3\iff x=8\): \(\iff\).

## C5

Original domain: \(x\ge5\). Both sides are non-negative, hence

\[
x+4=4(x-5).
\]

So \(x=8\), which is valid.

---

# 5. TRY D — reciprocal invariants

Let \(S_n=x^n+x^{-n}\), with

\[
S_n=S_1S_{n-1}-S_{n-2},\qquad S_0=2.
\]

## D1

\(S_1=5\), \(S_2=23\), so

\[
S_3=5\cdot23-5=110.
\]

## D2

For \(S_1=4\):

\[
S_2=14,\quad S_3=52,\quad S_4=194,\quad S_5=724.
\]

## D3

\[
\left(x-\frac1x\right)^2=4^2-4=12,
\]

so

\[
x-\frac1x=\pm2\sqrt3.
\]

Then

\[
x^2-x^{-2}
=\left(x-x^{-1}\right)\left(x+x^{-1}\right)
=\boxed{\pm8\sqrt3}.
\]

The value is not unique.

## D4

For \(S_1=3\):

\[
S_2=7,\ S_3=18,\ S_4=47,\ S_5=123,\ S_6=322.
\]

**Answer:** \(322\).

---

# 6. TRY E — logarithms

## E1

\[
25^{\log_5 3}=(5^2)^{\log_5 3}=3^2=9.
\]

## E2

Set \(t=\log_2x\):

\[
t^2-5t+6=0\Rightarrow t=2,3.
\]

Therefore

\[
x=4,8.
\]

## E3

Set

\[
u=\sqrt{\log_2x}\ge0.
\]

Then

\[
u^2-5u+4=0\Rightarrow u=1,4.
\]

Hence

\[
\log_2x=1,16
\]

and

\[
\boxed{x=2,65536}.
\]

## E4

A valid counterexample in base 10:

\[
\log(1+9)=1,
\]

while

\[
\log1+\log9=\log9\neq1.
\]

## E5

\[
27^{\log_3 2}
=(3^3)^{\log_3 2}
=2^3=8.
\]

## E6

\[
\log_4x=\log_2y
\Rightarrow x=y^2,
\]

with \(x,y>0\). Then

\[
y^2-y=6
\]

gives positive \(y=3\), so \(x=9\).

**Answer:** \(x+y=12\).

---

# 7. TRY F — log to algebra

## F1

Domain: \(x>5\).

\[
x-3=(x-5)^2
\]

gives candidates \(4,7\). Only \(7\) lies in the original domain.

## F2

Domain: \(x>4\).

\[
x-1=(x-4)^2
\]

gives

\[
x=\frac{9\pm\sqrt{13}}2.
\]

Only

\[
\boxed{\frac{9+\sqrt{13}}2}
\]

is greater than 4.

## F3

Original common domain:

\[
1<x<7.
\]

Injectivity gives

\[
x-1=7-x,
\]

so

\[
\boxed{x=4}.
\]

## F4

\[
\log_9x=\log_3y
\Rightarrow x=y^2.
\]

Then

\[
y^2-y=20
\]

has positive solution \(y=5\); thus \(x=25\).

**Answer:** \(30\).

---

# 8. Diagnosis laboratory

| Item | First issue | Repair |
|---|---|---|
| Dg1 | invalid radical distribution over addition | product behavior does not extend to sums; use the original radicand |
| Dg2 | missing principal-root sign model | \(\sqrt{(x-2)^2}=|x-2|\); equals \(x-2\) only for \(x\ge2\) |
| Dg3 | negative exponent misread as sign | \(a^{-2}=1/a^2\) for \(a\neq0\) |
| Dg4 | method is legal but inferior | normalize \(8,4\) to powers of 2 first |
| Dg5 | missing side-sign/domain ledger | require \(x\ge1\) before squaring; filter candidates by the original condition |
| Dg6 | zero case lost | \(x=2\) disappears if dividing by \(x-2\) |
| Dg7 | invariant-recognition failure | build \(S_n\) directly; explicit roots create unnecessary radicals |
| Dg8 | original log domain ignored | reject any candidate making an original argument non-positive |
| Dg9 | source custody | keep printed source, independent derivation, and key/disposition as separate records |

---

# 9. Fading ladder answers

## Radicals

- R1: \(7\sqrt2\).
- R2: \(4-\sqrt5\).
- R3: \(|2x-5|\); equals \(2x-5\) iff \(x\ge5/2\).
- R4: \(\sqrt[3]2\).

## Exponents

- X1: \(x=2\).
- X2: with \(t=2^x>0\), \(t^2-10t+16=0\Rightarrow t=2,8\); hence \(x=1,3\).
- X3: \(x=0\) or \(x=\log_{5/2}4\).
- X4: \(9\).

## Reversibility

- C-F1: \(x=5\).
- C-F2: \(x=1,-4\).
- C-F3: first only \(\Rightarrow\); second \(\iff\).
- C-F4: original domain \(x\ge0\); squaring gives candidates \(4,-1\); answer \(4\).

## Logarithms

- L1: \(x=2,4\).
- L2: \(x=2,65536\).
- L3: \(x+y=30\).
- L4: \(x=7\).

---

# 10. ADOPT answers

| Item | First move | Answer |
|---|---|---|
| M1 | common radical basis | \(4\) |
| M2 | hidden square | \(2\sqrt3-\sqrt5\) |
| M3 | reciprocal + cube-root meaning | \(1/16\) |
| M4 | common base 2 | \(x=3/2\) |
| M5 | \(t=4^x>0\) | \(x=0\) or \(x=\log_4 9\) |
| M6 | reciprocal recurrence | \(527\) |
| M7 | write \(x\ge1\), then square | \(x=4\) |
| M8 | \(t=\log_3x\) | \(x=3,27\) |
| M9 | \(u=\sqrt{\log_2x}\ge0\) | \(x=2,16\) |
| M10 | convert to \(x=y^2\) | \(x+y=6\) |
| M11 | exact inverse, \(16=2^4\) | \(81\) |
| M12 | original-domain + source-QC audit | reject invalid candidate; record source/key disagreement without changing printed mathematics |

---

# 11. Transfer answers and verification

## T1

Use

\[
2\pm\sqrt3=\left(\frac{\sqrt6\pm\sqrt2}{2}\right)^2.
\]

Both principal roots are positive, so the sum is

\[
\boxed{\sqrt6}.
\]

## T2

\[
5+2\sqrt6=(\sqrt3+\sqrt2)^2,
\]

\[
5-2\sqrt6=(\sqrt3-\sqrt2)^2.
\]

Therefore

\[
\boxed{2\sqrt2}.
\]

## T3

Divide by \(9^x>0\) and set

\[
t=\left(\frac73\right)^x>0.
\]

Then

\[
t^2-8t+7=0,
\]

so \(t=1,7\). Hence

\[
\boxed{x=0\quad\text{or}\quad x=\log_{7/3}7}.
\]

## T4

Given

\[
x-x^{-1}=3,
\]

we get

\[
x^2+x^{-2}=3^2+2=11.
\]

Thus

\[
x^4+x^{-4}=11^2-2=\boxed{119}.
\]

## T5

Let \(S_1=a^x+a^{-x}=3\). Then

\[
S_2=7,
\qquad
S_3=3\cdot7-3=\boxed{18}.
\]

## T6

Original domain: \(x\ge-10\). Both \(\sqrt{x+10}\) and \(|x-2|\) are non-negative, so squaring is reversible on that domain:

\[
x+10=(x-2)^2.
\]

This gives

\[
x^2-5x-6=0,
\]

hence

\[
\boxed{x=-1,6}.
\]

Both satisfy the original equation.

## T7

Original domain:

\[
x\neq1.
\]

For allowed \(x\), simplify to

\[
x+2=3,
\]

which gives \(x=1\), but that value is excluded by the original denominator.

**Answer:** no solution.

## T8

\[
\log_8x=\log_2y
\Rightarrow \frac13\log_2x=\log_2y
\Rightarrow x=y^3.
\]

With \(x-y=6\):

\[
y^3-y=6.
\]

The positive solution is \(y=2\), so \(x=8\).

**Answer:** \(10\).

## T9

\[
81^{\log_3 2}
=(3^4)^{\log_3 2}
=2^4
=\boxed{16}.
\]

## T10

Original domain:

\[
x+1>0,\qquad (x-1)^2>0,
\]

so \(x>-1\) and \(x\neq1\).

Now

\[
\log_4((x-1)^2)=\frac12\log_2((x-1)^2)=\log_2|x-1|.
\]

Thus

\[
x+1=|x-1|.
\]

The \(x\ge1\) branch gives no solution; the \(x<1\) branch gives \(x=0\), which is valid.

**Answer:** \(0\).

## T11

Set

\[
u=\sqrt{\log_5x}\ge0.
\]

Then

\[
u^2+2u-3=0,
\]

so \(u=1,-3\). Reject \(-3\) because \(u\ge0\). Therefore

\[
\log_5x=1
\]

and

\[
\boxed{x=5}.
\]

## T12

Two independent audits are required:

1. **Mathematical transformation audit:** real cubing is injective, so cubing a real cube-root equality does not create a \(\pm\) branch or duplicate roots merely through the transformation. Recompute the printed mathematics independently.
2. **Source-custody audit:** preserve the printed equation, the independent derivation, and the provisional key/multiplicity convention separately. If they disagree, retain `SOURCE_CONFLICT`; do not alter the source to make the key fit.

This preserves the existing disposition of `NMTC-BH-P-2025-Q18`.

---

# 12. Independent verification summary

- diagnostic: 12/12 checked;
- TRY A-F: all numerical/domain results checked;
- diagnosis cases: 9/9 mechanism dispositions checked;
- fading ladder: 16/16 checked;
- ADOPT: 12/12 checked;
- TRANSFER: 12/12 independently re-solved;
- principal-root, log-domain, substitution-range, and zero-divisor conditions explicitly rechecked.

`V3_MATH_DOMAIN_EQUIVALENCE_AUDIT: PASS`