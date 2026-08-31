# Sequences, Progressions & Recurrences — Assimilation Book

For a learner who can often compute terms or remember AP/GP formulas, but does not yet reliably choose the cheapest representation.

## The one router for this book

Before calculating, ask:

```text
TERM OR SUM?
    |
EXPLICIT OR RECURRENT?
    |
LOCAL RELATION OR GLOBAL FORMULA?
    |
CAN NEARBY RELATIONS BE SUBTRACTED?
    |
CAN THE EXPRESSION TELESCOPE?
    |
ONLY THEN COMPUTE TERMS
```

The goal is not to avoid computation. The goal is to compute **after** structure has reduced the work.

---

## 1. RECONNECT — name the object before the formula

A sequence is an ordered list:
`a_1, a_2, a_3, ...`

Here `a_n` means the **term at position n**.

A partial sum is a different object:
`S_n=a_1+a_2+...+a_n`.

### H0 reconnect check

Without solving fully, write the first question you would ask.

1. `3,7,11,15,...`
2. `2,6,18,54,...`
3. `S_n=n^2+2n`; find `a_n`.
4. `a_{n+2}=4a_{n+1}-3a_n`; find a high-index term.
5. six-term moving totals keep increasing.

Good first questions are:
- difference or ratio?
- term or sum?
- explicit or recursive?
- can nearby indices be subtracted?

### Term versus sum

If
`S_n=a_1+...+a_n`,
then neighboring accumulations differ by exactly one contribution:

`a_n=S_n-S_{n-1}` for `n>=2`.

Also `a_1=S_1`.

Example:
`S_n=n^2+2n`.

Then
`a_n=S_n-S_{n-1}`
`=n^2+2n-[(n-1)^2+2(n-1)]`
`=2n+1`.

The important move is not expansion. It is recognizing that **adjacent totals isolate one term**.

---

## 2. DISCOVER — AP and GP are local invariants

The familiar formulas should come **after** the invariant.

### Arithmetic progression

If
`a_{n+1}-a_n=d`
for every relevant `n`, the first difference is constant.

Then:
`a_n=a_1+(n-1)d`.

Why `n-1`? Moving from position 1 to position `n` requires exactly `n-1` equal jumps.

### Geometric progression

If terms are nonzero and
`a_{n+1}/a_n=r`
is constant, the ratio is invariant.

Then:
`a_n=a_1 r^(n-1)`.

### Close contrast

- `2,5,8,11,...` -> constant difference -> AP.
- `2,6,18,54,...` -> constant ratio -> GP.
- `2,5,10,17,...` -> neither. Its differences `3,5,7,...` have a simpler pattern.

Do not force a chapter label onto a sequence whose invariant is different.

---

## 3. MAKE SENSE — explicit and recursive are different representations

### Explicit definition

`a_n=2n^2-1`.

The requested term can be obtained directly from `n`.

### Recursive definition

`a_{n+1}=a_n+2n+1`, together with `a_1=1`.

The next term depends on earlier information.

A recurrence by itself is usually **not** a complete sequence. It needs:
- the index range where the rule applies;
- enough initial values.

A second-order recurrence such as
`a_{n+2}=3a_{n+1}-2a_n`
normally needs two initial terms.

### How to verify a proposed explicit formula

Suppose a recurrence is
`a_{n+2}=3a_{n+1}-2a_n`,
with `a_1=1, a_2=4`.

Someone proposes:
`a_n=3*2^(n-1)-2`.

Verification has two parts.

1. **Initial values**
   - at `n=1`: `3-2=1`;
   - at `n=2`: `6-2=4`.

2. **Recurrence for every allowed n**
   Substitute the formula into both sides and simplify. Matching a few early terms is evidence, not a proof for all indices.

> Adopt: a recurrence means **dependency + range + initialization**.

---

## 4. DISCOVER — subtract nearby windows

Let a fixed `k`-term window be

`W_i=a_i+a_{i+1}+...+a_{i+k-1}`.

The next window is

`W_{i+1}=a_{i+1}+...+a_{i+k}`.

Subtract:

`W_{i+1}-W_i=a_{i+k}-a_i`.

The `k-1` shared terms disappear.

If the windows are averages, dividing by the same positive `k` does not change which average is larger. Multiply by `k` first, then subtract the sums.

### Historical mechanism

For the validated 2025 Q26 anchor:
- increasing 4-term averages give `a_{i+4}>a_i`;
- decreasing 7-term averages give `a_{i+7}<a_i`.

The original surface is “averages.” The useful representation is an **index-shift inequality graph**.

> Adopt: a moving-window problem is usually a subtraction problem before it is an averaging problem.

---

## 5. MAKE SENSE — transform a recurrence before iterating

Consider

`a_{n+2}=4a_{n+1}-3a_n`.

Subtract `a_{n+1}` from both sides:

`a_{n+2}-a_{n+1}=3(a_{n+1}-a_n)`.

Define the first-difference sequence

`d_n=a_{n+1}-a_n`.

Then:

`d_{n+1}=3d_n`.

The original second-order recurrence has become a first-order GP for differences.

This is the local/global decision:
- global brute force: compute many `a_n`;
- local structural route: find a simpler quantity that evolves predictably.

The transform is not always “first differences.” It may be:
- a sum/difference of nearby terms;
- a ratio;
- an alternating transform;
- a neighboring-term invariant.

---

## 6. MAKE SENSE — a high-index neighboring-term invariant

A second-order recurrence can preserve a simple determinant-like combination.

Suppose

`a_{n+2}=p a_{n+1}+q a_n`.

Define

`D_n=a_n^2-a_{n-1}a_{n+1}`.

Now compare neighboring indices:

`D_{n+1}=a_{n+1}^2-a_n a_{n+2}`

Use the recurrence:

`=a_{n+1}^2-a_n(p a_{n+1}+q a_n)`

Group the first two terms:

`=a_{n+1}(a_{n+1}-p a_n)-q a_n^2`.

From the recurrence one index earlier,

`a_{n+1}-p a_n=q a_{n-1}`.

Therefore

`D_{n+1}=q a_{n-1}a_{n+1}-q a_n^2`
`=-q(a_n^2-a_{n-1}a_{n+1})`

so

`D_{n+1}=-qD_n`.

A complicated expression involving three high-index terms has become a one-step GP.

### Anchor connection

For the validated 2023 Q10 recurrence

`a_{n+2}=-4a_{n+1}-7a_n`,

we have `q=-7`, hence

`D_{n+1}=7D_n`.

That is why computing `a_49,a_50,a_51` directly is the wrong representation.

### Author-created check

Let `b_0=0, b_1=1` and
`b_{n+2}=-4b_{n+1}-7b_n`.

Then `D_1=1`, so
`D_20=7^19`.

The number of positive divisors is `19+1=20`.

The raw terms become huge; the invariant stays tiny.

---

## 7. DISCOVER — telescoping is cancellation across a sum

Consider

`1/[k(k+1)]`.

Split it:

`1/[k(k+1)]=1/k-1/(k+1)`.

Then

`sum_{k=1}^n 1/[k(k+1)]`

becomes

`(1-1/2)+(1/2-1/3)+...+(1/n-1/(n+1))`.

Every internal term cancels:

`=1-1/(n+1)=n/(n+1)`.

### Recognition cue

Neighboring factors such as `k(k+1)` or `(k-1)k` are a clue, not a guarantee. You must verify an exact decomposition `F(k)-F(k+1)`.

### Same idea, different scale

- `S_n-S_{n-1}` cancels an accumulation.
- `W_{i+1}-W_i` cancels overlapping windows.
- a shifted recurrence cancels repeated structure.
- telescoping cancels internal summands.

All are local comparisons between neighboring indices.

---

## 8. TRY — H0 first, then optional help

For each problem, attempt a first line **before** reading any hint.

### Try A — term from accumulation

`S_n=3n^2-n`. Find `a_n`.

If stuck:
- H1: one term is hidden between two neighboring totals.
- H2: compare `S_n` and `S_{n-1}`.
- H3: write `a_n=S_n-S_{n-1}`.

### Try B — moving window

Every 6-term sum is larger than the preceding 6-term sum. State the direct term inequality.

If stuck:
- H1: the two sums share five terms.
- H2: subtract adjacent 6-term windows.
- H3: write `W_{i+1}-W_i=a_{i+6}-a_i`.

### Try C — recurrence transform

`a_{n+2}=5a_{n+1}-4a_n`.

Find a recurrence for `d_n=a_{n+1}-a_n`.

If stuck:
- H1: compare neighboring terms rather than raw values.
- H2: rewrite in first differences.
- H3: `a_{n+2}-a_{n+1}=4(a_{n+1}-a_n)`.

---

## 9. DIAGNOSE — why the tempting start fails

| Wrong move | Why it is tempting | Missing link | Repair |
|---|---|---|---|
| set `a_n=S_n` | both use index `n` | representation | term = adjacent-sum difference |
| call every regular list AP/GP | formulas are familiar | recognition | test difference/ratio invariant |
| ignore initial values | recurrence looks like a formula | semantics | recurrence + range + initialization |
| verify only first few terms | examples match | proof/check | initials + recurrence for all valid `n` |
| compute 50 recurrence terms | procedure is obvious | method selection | search local transform/invariant |
| expand two moving averages | surface says “average” | representation | cancel overlapping windows |
| telescope any rational sum | one example was memorable | boundary | prove exact neighbor difference |
| derive a tiling recurrence here | notation looks identical | ownership/model | COMB-03 defines counting state first |
| lose one index | nearby subscripts look similar | execution | write both shifted relations explicitly |

---

## 10. FADE — support decreases across the set

The available support now fades.

### H3-available
`S_n=2n^2+3n`. Find `a_n`.

Maximum support if needed:
`a_n=S_n-S_{n-1}`.

### H2-maximum
`a_{n+2}=4a_{n+1}-3a_n`. Find a simpler sequence.

Maximum support:
study first differences.

### H1-maximum
Evaluate
`sum_{k=2}^n 1/[k(k-1)]`.

Maximum support:
look for neighboring-factor cancellation.

### H0
A sequence has all 4-term sums equal. Prove a periodicity statement.

No hint.

---

## 11. ADOPT — the first-move rules

1. **Term or sum?** Name the object.
2. **Explicit or recurrent?** Decide whether direct substitution or dependency is present.
3. **Local or global?** Prefer the representation that exposes the target.
4. **Nearby relations?** Subtract before iterating.
5. **Telescoping?** Seek an exact neighbor difference.
6. **High index?** Search transformed sequence/invariant.
7. **Counting state?** ALG-04 supplies notation only; COMB-03 must define the state and derive the recurrence.

Say this in your own words:

> “When neighboring indices share most of their structure, I compare them before I calculate.”

---

## 12. TRANSFER — changed surfaces

### Rolling measurements

A sensor records daily readings `r_1,r_2,...`. Every 6-day total is larger than the previous 6-day total.

The first useful line is not an average formula. It is:

`r_{i+6}>r_i`.

### Audit quantity for machine readings

Readings satisfy

`x_{n+2}=2x_{n+1}+3x_n`.

Define

`Q_n=x_n^2-x_{n-1}x_{n+1}`.

The same derivation gives:

`Q_{n+1}=-3Q_n`.

Different coefficients, same invariant mechanism.

### A recurrence from tilings

Suppose a tiling book states a recurrence `t_n=t_{n-1}+t_{n-2}`.

ALG-04 can:
- read the notation;
- use initial values;
- verify or manipulate the recurrence.

But the statement “why is the count equal to `t_{n-1}+t_{n-2}`?” belongs to COMB-03. It requires a state and a disjoint, exhaustive first-step partition.

---

## 13. Historical anchors

- IOQM 2025 Q26 — window comparison and high-index cancellation by local inequalities; verified answer `10`.
- IOQM 2023 Q10 — neighboring-term determinant invariant under a second-order recurrence; verified answer `51`.

Historical wording remains controlled by the validated papers. The exercises in this book that are not explicitly identified by year/question are author-created.

---

## 14. Exit test

You own this topic when you can answer all six questions for each major mechanism:

1. What did I notice?
2. Why does the method work?
3. What clue triggers it?
4. What similar-looking problem needs a different start?
5. Can I write the first two useful lines without help?
6. Can I solve a changed-surface version?

Formula recall alone is not the exit condition.
