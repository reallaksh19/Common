# Sequences and Recurrences — Assimilation Book

For a learner who remembers some AP/GP formulas but does not yet reliably recognize the engine of a mixed sequence problem.

## 1. RECONNECT

A sequence is an ordered list

`a_1, a_2, a_3, ...`

A partial sum is different:

`S_n=a_1+a_2+...+a_n`.

### Diagnostic — identify, do not fully solve

1. `3,7,11,15,...` — what remains constant?
2. `2,6,18,54,...` — what remains constant?
3. If `S_n=n^2+2n`, how do you get `a_n`?
4. A 5-term moving sum increases with the starting index. What should you subtract?
5. A recurrence asks for `a_100`. Must you compute 99 earlier terms?

Expected ideas: **difference, ratio, subtract partial sums, subtract adjacent windows, search for a transform/invariant**.

---

## 2. DISCOVER — term and sum are not the same object

If

`S_n=a_1+...+a_n`,

then

`S_n-S_{n-1}=a_n`.

### Example

If `S_n=n^2+2n`, then for `n>=2`,

`a_n=S_n-S_{n-1}`

`=n^2+2n-[(n-1)^2+2(n-1)]`

`=2n+1`.

Check `a_1=S_1=3`, and the same formula gives 3.

> **Adopt:** when the problem gives accumulated information but asks for one contribution, subtract adjacent accumulations.

---

## 3. MAKE SENSE — AP and GP are recognition patterns

### AP

`a_{n+1}-a_n=d` is constant.

Then

`a_n=a_1+(n-1)d`.

### GP

`a_{n+1}/a_n=r` is constant when terms are nonzero.

Then

`a_n=a_1 r^{n-1}`.

The formulas are consequences of the invariants, not the starting point.

### Contrast

Sequence `2,5,8,11,...` -> constant difference.

Sequence `2,6,18,54,...` -> constant ratio.

Sequence `2,5,10,17,...` -> neither; do not force AP/GP.

---

## 4. DISCOVER — adjacent windows collapse

Let

`W_i=a_i+a_{i+1}+...+a_{i+k-1}`.

Then

`W_{i+1}=a_{i+1}+...+a_{i+k}`.

Subtract:

`W_{i+1}-W_i=a_{i+k}-a_i`.

Almost everything cancels.

### Why this is powerful

A statement about **averages of windows** can become a simple inequality between two terms far apart.

If 4-term averages are strictly increasing, then

`a_{i+4}>a_i`.

If 7-term averages are strictly decreasing, then

`a_{i+7}<a_i`.

This is the mechanism behind the primary anchor `IOQM-2025-Q26`.

> **Adopt:** moving-window problems are usually subtraction problems before they are averaging problems.

---

## 5. MAKE SENSE — recurrence does not mean brute force

Suppose

`a_{n+2}=3a_{n+1}-2a_n`.

Subtract `a_{n+1}`:

`a_{n+2}-a_{n+1}=2(a_{n+1}-a_n)`.

So the **first differences form a GP with ratio 2**.

That transformed sequence may be much easier to understand than the original recurrence.

### Contrast

- brute force: compute `a_3,a_4,...` one by one;
- structural route: find a simpler sequence such as differences, ratios, or another invariant.

---

## 6. DISCOVER — telescoping means boundary terms survive

Consider

`1/[k(k+1)]`.

Partial fractions give

`1/[k(k+1)] = 1/k - 1/(k+1)`.

Therefore

`sum_{k=1}^n 1/[k(k+1)]`

`=(1-1/2)+(1/2-1/3)+...+(1/n-1/(n+1))`

`=1-1/(n+1)`.

The middle terms cancel.

### Recognition cue

Consecutive factors in denominators often suggest “write each term as a difference of neighbors.”

---

## 7. TRY — attempt before hints

### Problem A

A sequence has partial sums `S_n=3n^2-n`. Find `a_n`.

Try first.

**H1:** one term is the difference of what two accumulated quantities?

**H2:** compute `S_n-S_{n-1}`.

**H3:** answer `a_n=6n-4`.

### Problem B

`a_{n+2}=4a_{n+1}-3a_n`. Show the first differences follow a simple recurrence.

Try first.

**H1:** compare adjacent terms of the original recurrence.

**H2:** subtract `a_{n+1}` from both sides and regroup.

**H3:** `a_{n+2}-a_{n+1}=3(a_{n+1}-a_n)`.

---

## 8. DIAGNOSE — common wrong starts

### Wrong start 1: formula hunting

Do not ask “AP or GP?” before checking the actual differences/ratios.

### Wrong start 2: confusing `S_n` with `a_n`

If the problem gives total accumulation, subtract adjacent totals.

### Wrong start 3: generating 50 terms

A high index is a signal to search for an invariant, transformed recurrence, periodicity, or cancellation.

### Wrong start 4: treating a counting recurrence as pure algebra

If the recurrence comes from tilings/paths/states, the combinatorial model belongs to COMB-03.

---

## 9. FADE — H3 -> H0

### Faded set 1 — window cancellation

Suppose every 6-term sum is larger than the preceding 6-term sum. What termwise inequality follows?

- H3: subtract the two window sums.
- H2: five terms cancel.
- H1: compare adjacent windows.
- H0: answer independently.

### Faded set 2 — telescoping

Evaluate `sum_{k=2}^n 1/[k(k-1)]`.

- H3: write `1/[k(k-1)]=1/(k-1)-1/k`.
- H2: split into neighboring reciprocals.
- H1: look for consecutive-factor cancellation.
- H0: solve independently.

---

## 10. ADOPT — first-move rules

1. Term or sum? Identify the object.
2. Consecutive terms? Check difference and ratio.
3. Moving window? Subtract adjacent windows.
4. High-index recurrence? Transform before iterating.
5. Consecutive denominator factors? Test telescoping.
6. Counting-state recurrence? Route modelling to COMB-03.

---

## 11. PYQ ANCHORS

- `IOQM-2025-Q26` — sliding-window averages; subtract adjacent windows.
- `IOQM-2023-Q10` — recurrence/invariant recognition.

Use validated paper wording for historical deployment. Both answers are independently verified.

---

## 12. TRANSFER

The deeper pattern is cancellation under index shift:

- `S_n-S_{n-1}` isolates one term;
- `W_{i+1}-W_i` isolates entering/leaving terms;
- shifted recurrences reveal simpler difference sequences;
- telescoping sums cancel internal terms.

Different surfaces, same idea:

> **Compare neighboring indices so that most of the structure disappears.**
