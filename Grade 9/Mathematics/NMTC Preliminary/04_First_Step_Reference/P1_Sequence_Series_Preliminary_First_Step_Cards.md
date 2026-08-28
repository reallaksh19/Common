# P1 Sequence & Series — Preliminary First-Step Cards

Use before calculation. Each card answers: **when do I use this, what is the first line, and what is the common decoy?**

## Card S1 — TERM vs SUM
**Trigger:** asks for nth term vs sum of first n terms.
**First line:** `TARGET=a_n` or `TARGET=S_n`.
**Decoy:** choosing a formula before deciding the object.

## Card S2 — AP / constant difference
**Trigger:** equal additive change.
**First line:** `d=a_{n+1}-a_n`.
**Decoy:** using GP because numbers grow.

## Card S3 — GP / constant ratio
**Trigger:** equal multiplicative change.
**First line:** `r=a_{n+1}/a_n`.
**Decoy:** using differences on exponential growth.

## Card S4 — Selected/high-index GP
**Trigger:** terms far apart or ratios of large-index terms.
**First line:** `a_p/a_q=r^(p-q)`.
**Decoy:** calculating both large powers separately.
**PYQ:** 2023 Q29.

## Card S5 — Weighted polynomial sum
**Trigger:** kth term contains `k`, `k²`, `k³` polynomially.
**First line:** expand kth term and split sigma.
**Decoy:** force sequence into AP/GP.
**PYQ:** 2023 Q15; 2024 Q10.

## Card S6 — Recurrence reciprocal
**Trigger:** recurrence contains a fraction such as `a_n/(1+c a_n)`.
**First line:** test `b_n=1/a_n`.
**Decoy:** iterate dozens of terms.
**PYQ:** 2024 Q11 mechanism.

## Card S7 — Recurrence shift
**Trigger:** affine recurrence `a_{n+1}=p a_n+q`.
**First line:** choose `b_n=a_n-c` so the constant term vanishes.
**Decoy:** expand recursively to the target index.

## Card S8 — Functional recurrence / strategic indices
**Trigger:** rule uses `a_{m+n}`.
**First line:** choose index pairs that reach target efficiently.
**Decoy:** derive a closed form when not needed.
**PYQ:** 2019 Q29.

## Card S9 — Infinite GP
**Trigger:** infinite sum with geometric terms.
**First line:** `|r|<1`, then `S=a/(1-r)`.
**Decoy:** use infinite formula without convergence.
**PYQ:** 2024 Q27.

## Card S10 — Reverse from partial sums
**Trigger:** formula for `S_n`, asks nth term.
**First line:** `a_n=S_n-S_{n-1}`.
**Decoy:** differentiate or guess from samples.

## Card S11 — Rational telescoping
**Trigger:** neighboring factors such as `k(k+1)`.
**First line:** partial-fraction into adjacent terms.
**Decoy:** add fractions directly.

## Card S12 — Radical telescoping
**Trigger:** denominator `sqrt(k)+sqrt(k+1)`.
**First line:** rationalize.
**Decoy:** decimal approximation.

## Card S13 — Finite differences
**Trigger:** neither AP nor GP; values resemble polynomial growth.
**First line:** write first differences, then second differences.
**Decoy:** fit an AP/GP anyway.

## Card S14 — Source QC
**Trigger:** historical term wording and supplied key disagree.
**First line:** solve printed mathematics independently and record conflict.
**Decoy:** edit the stem to fit the key.
**Contrast:** 2025 Q30.

## Mastery condition

On a mixed set, at least 80% of these first moves should be selected correctly **before** calculation.