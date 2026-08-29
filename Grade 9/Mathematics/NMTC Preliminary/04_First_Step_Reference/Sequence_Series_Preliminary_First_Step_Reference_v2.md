# Sequence & Series Preliminary — First-Step Reference v2

`ISSUE_AUTHORITY: #49`

`WAVE: 3 — FIRST_STEP_REFERENCE`

`STUDENT_LAYER: YES`

This is a **post-teaching compression layer**. Use it after the Assimilation Book, not instead of it.

Its purpose is simple:

> On an unlabelled Sequence & Series problem, choose the right mathematical object and write the right first line before calculation.

Core flow:

`SEE -> NAME TARGET -> CHOOSE STRUCTURE -> WRITE FIRST LINE -> CHECK CONDITION/INDEX -> GO`

---

# 1. Ten-second decision tree

```text
WHAT IS THE TARGET?
|
+-- one term --------------------------> write TARGET = a_n
|
+-- sum of first n --------------------> write TARGET = S_n
|
+-- block p...q -----------------------> write S_q - S_(p-1)
|
+-- given S_n, asks a_n ---------------> write a_n = S_n - S_(n-1)
|
+-- visible list ----------------------> test difference / ratio
|
+-- far-apart GP terms ----------------> divide selected terms
|
+-- weighted / nested sum -------------> expose kth term / multiplicity
|
+-- recurrence ------------------------> ask which transform simplifies it
|
+-- neighboring factors/radicals ------> seek telescope
|
+-- not AP/GP -------------------------> finite differences / other transform
|
+-- historical stem/key conflict ------> solve printed math independently; freeze conflict
```

Before using an infinite-GP formula, insert one compulsory gate:

`|r| < 1 ?`

Before collapsing a telescope, insert another:

`FIRST SURVIVOR? LAST SURVIVOR?`

---

# 2. Recognition atlas

| What you see | What it usually means | First useful line |
|---|---|---|
| “20th term” | local object | `TARGET=a_20` |
| “sum of first 20” | cumulative object | `TARGET=S_20` |
| “terms 15 through 40” | block accumulation | `S_40-S_14` |
| formula for `S_n`, asks `a_n` | reverse cumulative information | `a_n=S_n-S_{n-1}` |
| constant additive change | AP candidate | `a_{n+1}-a_n` |
| constant multiplicative scaling | GP candidate | `a_{n+1}/a_n` |
| infinite geometric wording | convergence gate | `|r|<1` |
| selected terms at large indices | index-gap compression | `a_p/a_q=r^(p-q)` |
| kth term polynomial in k | weighted polynomial sum | expand `T_k` |
| nested sum | multiplicity/counting | simplify inner sum / count appearances |
| `a_n/(1+c a_n)` recurrence | reciprocal transform | `b_n=1/a_n` |
| `pa_n+q` recurrence | fixed-point shift | solve `c=pc+q`; set `b_n=a_n-c` |
| `a_{m+n}` relation | index navigation | choose useful `(m,n)` |
| `1/[k(k+1)]`-type term | rational telescope | partial fractions |
| `1/(sqrt(k)+sqrt(k+1))` | radical telescope | rationalize |
| neither AP nor GP | higher-difference signal | build difference table |
| proposed closed form | verification task | check recurrence + initial condition |
| key conflicts with printed stem | source-QC | solve printed mathematics first |

---

# 3. Phrase decoder

Translate words before choosing formulas.

- **“nth term”** -> position, not accumulation.
- **“sum of the first n terms”** -> cumulative object.
- **“from the pth to qth term”** -> cumulative difference.
- **“infinite GP”** -> convergence condition before sum formula.
- **“ratio of two far-apart terms”** -> index difference, not huge powers.
- **“sum of k times...”** -> construct the kth summand.
- **“defined recursively”** -> look for a simpler variable before iterating.
- **“for all positive m,n, a_{m+n}=...”** -> choose indices strategically.
- **“find a term from S_n”** -> reverse cumulative information.
- **“neighboring factors / conjugate radicals”** -> try to manufacture adjacent differences.
- **“not AP or GP”** -> normalize, transform, or inspect finite differences.
- **“answer key says..., printed problem says...”** -> neither overrides independent mathematics.

---

# 4. Fourteen First-Step cards

## Card S1 — TARGET OBJECT

**Trigger:** term, sum, or block wording.

**Write:** `TARGET=a_n`, `TARGET=S_n`, or `TARGET=S_q-S_{p-1}`.

**Reject:** selecting a formula before naming the object.

---

## Card S2 — REVERSE FROM `S_n`

**Trigger:** formula for cumulative sum, asks for one term.

**Write:** `a_n=S_n-S_{n-1}`.

**Check:** `a_1=S_1` at the boundary.

**Reject:** guessing from sample terms.

---

## Card S3 — AP / CHANGE

**Trigger:** additive-looking pattern.

**Write:** `d=a_{n+1}-a_n`.

**Check:** is the difference actually constant?

**Reject:** “the numbers grow steadily, therefore AP.”

---

## Card S4 — GP / RATIO

**Trigger:** multiplicative-looking pattern.

**Write:** `r=a_{n+1}/a_n` where defined.

**Check:** ratio domain and sign.

**Reject:** classifying from visual size alone.

---

## Card S5 — INFINITE GP

**Trigger:** infinite geometric accumulation.

**Write first:** `|r|<1`.

**Then:** use the infinite-sum relation if the condition passes.

**Reject:** writing `a/(1-r)` before convergence.

---

## Card S6 — HIGH-INDEX GP

**Trigger:** far-apart selected terms or ratios of large-index terms.

**Write:** `a_p/a_q=r^(p-q)`.

**Reject:** calculating both high powers separately.

**Clean historical mechanism anchor:** `NMTC-BH-P-2023-Q29`.

---

## Card S7 — WEIGHTED POLYNOMIAL SUM

**Trigger:** kth term contains `k`, `k^2`, etc.

**Write:** the general summand, then expand only enough to split sigma.

**Reject:** forcing the generated list into AP/GP.

**Clean anchors:** `NMTC-BH-P-2023-Q15`, `NMTC-BH-P-2024-Q10`.

---

## Card S8 — NESTED ACCUMULATION

**Trigger:** one sum sits inside another.

**Write:** simplify the inner sum or count how often each base term appears.

**Reject:** expanding every term one by one when multiplicity is visible.

---

## Card S9 — RECIPROCAL RECURRENCE

**Trigger:** recurrence has a fraction such as `a_n/(1+c a_n)`.

**Write:** test `b_n=1/a_n`.

**Check:** transformed variable is defined and initial condition is carried over.

**Clean anchor:** `NMTC-BH-P-2024-Q11`.

---

## Card S10 — FIXED-POINT SHIFT

**Trigger:** affine recurrence `a_{n+1}=pa_n+q`.

**Write:** solve `c=pc+q`; set `b_n=a_n-c`.

**Reject:** brute-force iteration when the shift turns the update into a GP.

---

## Card S11 — FUNCTIONAL RECURRENCE

**Trigger:** rule uses `a_{m+n}`.

**Write:** choose index pairs that reach the target efficiently.

**Reject:** deriving a closed form automatically.

**Clean anchor:** `NMTC-BH-P-2019-Q29`.

---

## Card S12 — TELESCOPE

**Trigger:** neighboring factors, conjugate radicals, or transformed adjacent differences.

**Write:** a representation of the form `v_k-v_{k+1}`.

**Check:** expand the first two and last two terms; mark surviving endpoints.

**Reject:** “everything cancels.”

---

## Card S13 — FINITE DIFFERENCES

**Trigger:** neither difference nor ratio is constant, but values look polynomial.

**Write:** first differences, then second/higher differences as needed.

**Check:** a constant difference row suggests a degree; verify the proposed rule.

**Reject:** calling constant second difference an AP.

---

## Card S14 — SOURCE QC

**Trigger:** historical wording and supplied key disagree.

**Write:** solve the printed mathematics independently.

**Disposition:** `FLAG -> PRESERVE -> BLOCK CANONICAL USE` until resolved.

**Reject:** changing one word because it makes the key work.

**Issue-49 conflict case:** `NMTC-BH-P-2025-Q30`.

---

# 5. Ten critical contrasts

| Near-looking pair | Correct boundary |
|---|---|
| `a_n` vs `S_n` | one local term vs cumulative sum |
| AP vs GP | constant difference vs constant ratio |
| finite GP vs infinite GP | algebraic finite sum vs convergence-gated infinite sum |
| direct nth term vs reverse from `S_n` | parameter route vs adjacent cumulative difference |
| absolute high-index term vs term ratio | may need `a,r` vs often only index gap |
| polynomial weighted sum vs GP-looking sum | split standard sums vs geometric alignment |
| recurrence iteration vs transform | legal brute force vs structure-revealing variable change |
| reciprocal transform vs fixed-point shift | denominator structure vs affine structure |
| telescope recognized vs telescope completed | cancellation idea vs correct endpoint custody |
| source conflict vs source repair | preserve evidence vs invent canonical wording |

---

# 6. Recognition-only laboratory — 20 prompts

**Rule:** Do not solve. For each prompt, write only:

`OBJECT / METHOD FAMILY / FIRST MOVE / REQUIRED CHECK`

Stop before arithmetic.

## R1

An AP is described and the question asks for its 80th term.

## R2

The same AP asks for the sum of its first 80 terms.

## R3

A formula for `S_n` is given and the problem asks for `a_25`.

## R4

The sum of terms 31 through 70 is requested.

## R5

The list is `11,15,19,23,...`.

## R6

The list is `3,-6,12,-24,...`.

## R7

An infinite GP is presented with common ratio `-3/4`.

## R8

A finite GP is presented with common ratio `5/2`.

## R9

A GP gives `a_91` and `a_96`; the target is `a_40/a_35`.

## R10

The target is `sum_{k=1}^{30} k(4k-3)`.

## R11

The target is `sum_{k=1}^{n} sum_{j=1}^{k} 1`.

## R12

`a_{n+1}=a_n/(1+4a_n)`.

## R13

`a_{n+1}=5a_n-8`.

## R14

`a_{m+n}=a_m+a_n+mn`, and only `a_16` is requested.

## R15

A proposed formula for a recurrence is supplied and the instruction is “prove that this formula is correct.”

## R16

Evaluate structurally `sum 1/[k(k+1)]`.

## R17

Evaluate structurally `sum 1/(sqrt(k+2)+sqrt(k+3))`.

## R18

The list is `4,10,18,28,40,...`; it is neither AP nor GP.

## R19

A geometry problem generates radii in a constant ratio, but the main reasoning is homothety/tangent-circle geometry.

## R20

A reproduced historical GP item gives one result from the printed term comparison while the provisional key corresponds to a different comparison.

---

# 7. Recognition key — use only after all 20 attempts

1. `a_n / position / label target then nth-term relation / n-1 index`.
2. `S_n / accumulation / label target then finite AP sum route / term count`.
3. `a_n from cumulative / reverse / a_25=S_25-S_24 / endpoint index`.
4. `block sum / reverse accumulation / S_70-S_30 / preserve term 31`.
5. `AP / CHANGE / test first difference / constancy`.
6. `GP / RATIO / test adjacent ratio / sign + nonzero denominator`.
7. `infinite GP / convergence / write |r|<1 / passes because 3/4<1`.
8. `finite GP / finite accumulation / use finite GP structure / no convergence condition required`.
9. `selected GP ratio / high-index cancellation / divide comparable terms / exponent gap`.
10. `weighted polynomial sum / ACCUMULATION / expand kth summand / bounds + standard-sum powers`.
11. `nested accumulation / multiplicity / inner sum = k / bounds`.
12. `recurrence / reciprocal transform / b_n=1/a_n / domain + initial condition`.
13. `recurrence / fixed-point shift / solve c=5c-8 then b_n=a_n-c / initial condition`.
14. `functional recurrence / strategic indices / choose doubling/decomposition toward 16 / recurrence domain`.
15. `verification / substitution / check recurrence + initial condition / do not call this discovery`.
16. `telescoping / partial fractions / v_k-v_{k+1} / first + last survivors`.
17. `telescoping / rationalization / conjugate difference / shifted radical endpoints`.
18. `non-AP/GP / finite differences / build difference table / verify any polynomial hypothesis`.
19. `bridge classification / geometry-primary / record GP as bridge mechanism only / no Sequence-frequency inflation`.
20. `source-QC / independent printed-math solution / flag-preserve-block / no silent wording repair`.

`RECOGNITION_KEY_FINAL_ANSWERS: NONE REQUIRED`

This lab tests method selection, not arithmetic completion.

---

# 8. Thirty-second checks

Before solving, ask:

1. Did I write `a_n`, `S_n`, or a block sum explicitly?
2. If I called it AP/GP, did I actually test the invariant?
3. If the index is large, can a ratio cancel the useless powers?
4. If the sum is weighted, did I expose the kth term?
5. If the recurrence is ugly, which variable makes it simpler?
6. If it is infinite GP, did I check `|r|<1` first?
7. If it telescopes, which two boundary terms survive?
8. If I inferred a polynomial rule from differences, did I verify it?
9. If a formula is being checked, am I verifying rather than discovering?
10. If source wording/key disagree, did I preserve the conflict?

---

# 9. Source-to-first-step map

| Source evidence | First-step family | Custody |
|---|---|---|
| `NMTC-BH-P-2019-Q29` | strategic functional recurrence | `CLEAN_SCORED_ANCHOR` |
| `NMTC-BH-P-2023-Q15` | expose polynomial kth term | `CLEAN_SCORED_ANCHOR` |
| `NMTC-BH-P-2023-Q29` | high-index GP cancellation | `CLEAN_SCORED_ANCHOR` |
| `NMTC-BH-P-2024-Q10` | weighted accumulation | `CLEAN_SCORED_ANCHOR` |
| `NMTC-BH-P-2024-Q11` | reciprocal recurrence / telescoping bridge | `CLEAN_SCORED_ANCHOR`, counted once |
| `NMTC-BH-P-2024-Q27` | infinite-GP condition + coupled constraints | `CLEAN_SCORED_ANCHOR` |
| `NMTC-BH-P-2018-Q17` | light POSITION/CHANGE reconnect | `FOUNDATION_SUPPORT_ONLY` |
| `NMTC-BH-P-2024-Q13` | constant-ratio recognition in geometry | `BRIDGE_EVIDENCE`, no Sequence-frequency credit |
| `NMTC-BH-P-2025-Q30` | source-QC | `SOURCE_CONFLICT_EVIDENCE`, blocked canonical anchor |

---

# 10. Independence self-check

You are ready to leave this reference closed during mixed practice when you can do all of the following without prompts:

- distinguish `a_n` from `S_n` immediately;
- write a block sum with the correct preceding endpoint;
- test CHANGE versus RATIO rather than judge by appearance;
- state `|r|<1` before an infinite-GP sum;
- cancel high-index GP powers by index distance;
- expose a weighted/nested summand before summing;
- choose reciprocal versus fixed-point shift from recurrence shape;
- choose strategic indices for a functional recurrence;
- reverse from `S_n` and telescope with endpoint custody;
- use finite differences as a hypothesis signal and then verify;
- distinguish discovery from verification;
- preserve a source conflict rather than repairing it.

Target:

`18/20 recognition-only prompts correct without opening this reference`.

That target is a **practice threshold**, not psychometric validation.

`CLASSROOM_CALIBRATION: NOT_RUN`

`WAVE3_STUDENT_REFERENCE: COMPLETE`
