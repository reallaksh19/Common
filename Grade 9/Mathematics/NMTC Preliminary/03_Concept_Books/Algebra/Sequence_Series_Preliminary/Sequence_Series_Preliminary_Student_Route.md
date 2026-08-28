# Sequence & Series — NMTC Preliminary Student Route

## How to use this overlay

Use the existing deep chapter for explanation and derivation. Use this route to decide **what to recognize first under Preliminary conditions**.

Deep chapter:

`Grade 9/Mathematics/Sequence and Series/`

## Route 0 — prerequisite diagnostic

Before speed practice, confirm you can answer:

1. What is the difference between a sequence and a series?
2. What is the difference between `a_n` and `S_n`?
3. How do you test whether a list is AP or GP?
4. Why is the exponent in `ar^(n-1)` equal to `n-1`?
5. Why does an infinite GP require `|r|<1`?
6. What does `a_n=S_n-S_{n-1}` mean?
7. What do the bounds in sigma notation actually generate?

If any answer is uncertain, return to the matching upstream concept section before timing yourself.

---

# Route 1 — TERM OR SUM?

## SEE

A question asks for the 50th term.

Another asks for the sum of the first 50 terms.

They may use the same AP, but they are different objects.

## FIRST MOVE

Write one of:

`TARGET = a_n`

or

`TARGET = S_n`.

Do this before selecting a formula.

## WRONG MOVE

Using an AP sum formula merely because the question contains the word “first”.

---

# Route 2 — CHANGE OR RATIO?

## SEE

`5, 9, 13, 17,...`

Differences are constant: AP.

`5, 10, 20, 40,...`

Ratios are constant: GP.

## FIRST MOVE

Mark either:

`d = next - previous`

or

`r = next/previous`.

Do not decide from how the numbers “look”.

---

# Route 3 — HIGH INDEX? CANCEL BEFORE CALCULATING

Suppose a GP asks for a relation between `a_40` and `a_35`.

Do not expand both huge terms separately.

Use:

`a_40/a_35 = r^5`.

## PYQ CONNECTION

`NMTC-BH-P-2023-Q29` becomes short because high-index powers cancel after the correct ratio relation is written.

---

# Route 4 — WEIGHTED SUM? MAKE THE nth TERM VISIBLE

If the kth term is:

`k(3k+1)`,

then the sum is:

`Σ(3k²+k)`

`=3Σk²+Σk`.

The problem is no longer a mysterious sequence. It is an accumulation of standard polynomial terms.

## PYQ CONNECTION

- `NMTC-BH-P-2023-Q15`;
- `NMTC-BH-P-2024-Q10`.

## WRONG MOVE

Trying to force the sequence into AP or GP just because it has indexed terms.

---

# Route 5 — RECURRENCE LOOKS UGLY? CHANGE THE VARIABLE

Example:

`a_{n+1}=a_n/(1+a_n)`.

Taking reciprocals gives:

`1/a_{n+1}=1/a_n+1`.

Now the transformed sequence is AP.

## REALIZE

A nonlinear recurrence may become linear after a reciprocal, difference or shift.

## PYQ CONNECTION

`NMTC-BH-P-2024-Q11` uses this kind of recurrence linearization/telescoping behavior.

---

# Route 6 — FUNCTIONAL RECURRENCE? CHOOSE USEFUL INDICES

If:

`a_{m+n}=a_m+a_n+2mn`,

and you need `a_8`, do not automatically derive a closed formula.

Try:

`(m,n)=(1,1)`, then `(2,2)`, then `(4,4)`.

The index doubles rapidly.

## PYQ CONNECTION

`NMTC-BH-P-2019-Q29` is a clean strategic-index anchor.

---

# Route 7 — INFINITE GP? CONDITION FIRST

Before writing:

`S=a/(1-r)`,

write:

`|r|<1`.

Then translate every supplied infinite sum in terms of the same `a,r`.

## PYQ CONNECTION

`NMTC-BH-P-2024-Q27` couples two infinite-GP constraints. The efficient path is to express both in `a,r`, then eliminate.

---

# Route 8 — GIVEN S_n? REVERSE

If:

`S_n=3n²+2n`,

then:

`a_n=S_n-S_{n-1}`.

Do not guess the sequence from a few values unless asked to.

---

# Route 9 — TELESCOPING? LOOK FOR NEIGHBORS

For:

`1/[k(k+1)]`,

write:

`1/k - 1/(k+1)`.

For:

`1/(sqrt(k)+sqrt(k+1))`,

rationalize to:

`sqrt(k+1)-sqrt(k)`.

The middle terms disappear when accumulated.

---

# Route 10 — NOT AP OR GP? TRY DIFFERENCES

Sequence:

`2,6,12,20,30,...`

First differences:

`4,6,8,10,...`

Second differences are constant, suggesting a quadratic nth term.

A Preliminary solver should recognize this before trying random formulas.

---

# Route 11 — SOURCE CHECK

If a historical GP item’s wording gives one mathematics result but a key corresponds to a different term comparison, do not edit the wording silently.

`NMTC-BH-P-2025-Q30` remains a source-conflict example for this exact reason.

Correct action:

`FLAG -> PRESERVE -> DO NOT CANONICALIZE`.

---

# Adoption check

You are ready for the mixed labs only if you can look at an unlabelled question and write one of these first moves quickly:

`TERM/SUM / DIFFERENCE / RATIO / CANCEL INDEX POWERS / EXPAND nth TERM / RECIPROCAL / SHIFT / STRATEGIC INDICES / INFINITE-GP CONDITION / REVERSE FROM S_n / TELESCOPE / FINITE DIFFERENCES / SOURCE QC`.

The goal is not formula recall. The goal is choosing the right mathematical object before calculation.