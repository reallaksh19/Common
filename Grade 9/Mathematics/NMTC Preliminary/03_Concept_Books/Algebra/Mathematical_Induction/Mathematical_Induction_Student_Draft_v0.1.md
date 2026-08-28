# Mathematical Induction — Student Draft v0.1

## Goal

Learn induction as a chain of logic, not as a memorized proof format.

Use:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

and while proving:

`STATE -> START -> ASSUME -> BUILD -> CLOSE -> CHECK`.

---

# 1. Why checking examples is not enough

Suppose a claim works for `n=1,2,3,4,5`.

That proves only five cases.

A universal statement such as

> for every integer `n>=1`

needs a mechanism that reaches every allowed integer.

Induction supplies that mechanism.

Think of a staircase:

1. you can stand on the first required step;
2. whenever you can stand on step `k`, you can reach step `k+1`.

Then every step from the starting one onward is reachable.

The two parts are both necessary.

---

# 2. State the proposition before proving it

For

`1+2+...+n = n(n+1)/2`,

write

`P(n): 1+2+...+n = n(n+1)/2, for integers n>=1.`

This prevents a common error: changing the claim during the proof.

### First-move check

For each prompt, first write only `P(n)` and the allowed domain.

A. `1+3+...+(2n-1)=n^2`.

B. `5 | (6^n-1)`.

C. `3^n>n^2` for `n>=2`.

---

# 3. Base case: start where the statement starts

For `P(n)` valid for `n>=2`, the base case is `P(2)`.

Do not automatically test `n=1`.

### Example

Claim:

`3^n>n^2` for every integer `n>=2`.

Base:

`3^2=9>4`.

That is the correct start.

### Trap

A proof can have a perfect induction step and still fail if the first required case is false.

---

# 4. The induction hypothesis is a temporary tool

Suppose the claim is

`1+3+...+(2n-1)=n^2`.

Assume it is true for an arbitrary `k>=1`:

`1+3+...+(2k-1)=k^2`.

This is the induction hypothesis.

You are **not** assuming the theorem for all n.

You are assuming one generic case so that you can prove the next case.

---

# 5. The decisive step: build the k+1 case

For the odd-number identity, the `k+1` case has one new odd number:

`1+3+...+(2k-1)+(2k+1)`.

Use the hypothesis:

`=k^2+(2k+1)`

`=(k+1)^2`.

That is exactly `P(k+1)`.

## REALIZE

For sum identities, the first useful line is usually:

`new sum = old sum + new term`.

This is more important than memorizing the phrase “assume true for k.”

---

# 6. Worked proof — sum of first n integers

Claim:

`P(n): 1+2+...+n = n(n+1)/2`, for `n>=1`.

### Base

At `n=1`:

`1 = 1(2)/2`.

### Hypothesis

Assume

`1+2+...+k = k(k+1)/2`.

### Build k+1

`1+2+...+k+(k+1)`

`=k(k+1)/2+(k+1)`

`=(k+1)(k/2+1)`

`=(k+1)(k+2)/2`.

This is the required formula with `n=k+1`.

Therefore the identity holds for all integers `n>=1`.

---

# 7. Divisibility induction

## Example: prove 5 divides 6^n-1

Claim:

`P(n): 5 | (6^n-1)`, for `n>=1`.

### Base

`6^1-1=5`.

### Hypothesis

Assume

`6^k-1=5q`

for some integer `q`.

### k+1 case

`6^(k+1)-1`

`=6*6^k-1`

`=6(6^k-1)+5`.

By the hypothesis, the first term is divisible by 5, and so is 5.

Therefore the whole expression is divisible by 5.

## First-move pattern

`new expression = multiple of old expression + obvious divisible remainder`.

---

# 8. When induction is valid but not cheapest

Claim:

`6 | (n^3-n)`.

Induction can prove this.

But direct factorization gives

`n^3-n=n(n-1)(n+1)`.

Three consecutive integers contain a multiple of 3 and at least one even number, so the product is divisible by 6.

That proof is shorter.

### ADOPT

Before using induction, ask:

> Is there a direct identity, factorization, parity or congruence proof that is cleaner?

Induction is a proof tool, not a compulsory ritual.

---

# 9. Inequality induction

## Example: prove 2^n >= n+1 for n>=0

Base `n=0`:

`1>=1`.

Assume

`2^k>=k+1`.

Then

`2^(k+1)=2*2^k >= 2(k+1)`.

Now we still need to reach `k+2`.

Since

`2(k+1)>=k+2`

for `k>=0`,

we get

`2^(k+1)>=k+2`.

### REALIZE

For inequalities, using the induction hypothesis is often only half of the step.

You must also prove the extra comparison that reaches the next target.

---

# 10. Later starting index

Prove

`3^n>n^2` for `n>=2`.

Base:

`9>4`.

Assume

`3^k>k^2` for `k>=2`.

Then

`3^(k+1)>3k^2`.

Need:

`3k^2>(k+1)^2`.

Difference:

`3k^2-(k+1)^2=2k^2-2k-1`.

For `k>=2`, this is positive.

Hence

`3^(k+1)>(k+1)^2`.

The domain check is part of the proof.

---

# 11. Recurrence verification

Suppose

`a_1=2`,

`a_{n+1}=2a_n+1`,

and someone proposes

`a_n=3*2^(n-1)-1`.

Induction can verify it.

Base:

`3*1-1=2`.

Assume

`a_k=3*2^(k-1)-1`.

Then

`a_{k+1}=2a_k+1`

`=2[3*2^(k-1)-1]+1`

`=3*2^k-1`.

This is the proposed formula for `k+1`.

### Important

The recurrence and the formula are different objects.

Induction verifies the formula once proposed; it does not necessarily discover it.

---

# 12. Strong induction

Ordinary induction assumes one generic previous case `P(k)`.

Strong induction may assume all earlier cases:

`P(n0), P(n0+1), ..., P(k)`.

This helps when the next case depends on more than one previous case.

### Example architecture

If a recurrence uses both `a_k` and `a_{k-1}`, a proof of a closed form may need two starting cases or a strong/multi-case hypothesis.

Do not use strong induction merely because it sounds stronger.

Use it because the recurrence structure demands more previous information.

---

# 13. Broken-proof laboratory

## Broken proof A — missing base

“Assume P(k). Then P(k+1). Therefore P(n) for all n.”

Problem: there is no known place where the chain begins.

## Broken proof B — wrong hypothesis

“Assume P(k+1). Then show P(k+1).”

Problem: circular.

## Broken proof C — wrong step size

You prove

`P(k)->P(k+2)`

but verify only one base case.

Then you may reach only every other integer.

You need enough starting cases for the step size.

## Broken proof D — hidden domain failure

The algebra uses division by `k-1` but the claimed domain includes `k=1`.

The step must be valid throughout the required domain.

---

# 14. First-move recognition

Classify before proving:

1. finite sum -> `OLD SUM + NEW TERM`;
2. product -> `OLD PRODUCT * NEW FACTOR`;
3. divisibility -> `FACTOR/REWRITE UNTIL OLD DIVISIBLE BLOCK APPEARS`;
4. inequality -> `USE IH + PROVE EXTRA COMPARISON`;
5. recurrence -> `SUBSTITUTE IH INTO RECURRENCE`;
6. two-previous-term dependence -> `TWO BASES / STRONG INDUCTION`;
7. obvious factorization -> `INDUCTION NOT CHEAPEST`.

---

# 15. Self-check set

### Q1
Prove `1+3+...+(2n-1)=n^2`.

### Q2
Prove `7 | (8^n-1)` for `n>=1`.

### Q3
Prove `1+2+...+n=n(n+1)/2`.

### Q4
Prove `2^n>=n+1` for `n>=0`.

### Q5
A student proves `P(k)->P(k+2)` and checks only `P(1)`. What is missing?

### Q6
Why is direct factorization usually better than induction for `6 | (n^3-n)`?

## Answers / checkpoints

Q1: add the next odd term `2k+1`.

Q2: `8^(k+1)-1=8(8^k-1)+7`.

Q3: add `k+1` to the old sum.

Q4: after IH, use `2(k+1)>=k+2`.

Q5: a second starting case, e.g. `P(2)`, is needed to reach both parity chains.

Q6: `n(n-1)(n+1)` immediately exposes factors 2 and 3.

---

# Source note

This chapter is syllabus-first. The current qualified five-year corpus does not justify calling induction historically recurrent. All exercises above are author-created unless separately tagged otherwise.
