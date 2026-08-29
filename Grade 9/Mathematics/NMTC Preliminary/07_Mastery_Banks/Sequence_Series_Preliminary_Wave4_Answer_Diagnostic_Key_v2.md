# Sequence & Series Preliminary Overlay — Wave 4 Answer / Diagnostic Key v2

`ISSUE_AUTHORITY: #49`

`WAVE: 4 — TEACHER / DIAGNOSTIC AUTHORITY`

`STUDENT_LAYER: NO`

This key is separate from the student paper. Use it after an attempt.

---

# A. Recognition-only key — 20/20

| ID | Expected recognition / first mechanism | Main diagnostic if missed |
|---|---|---|
| R1 | cumulative target -> `S_n` | `TERM_SUM_CONFUSION` |
| R2 | reverse cumulative information -> `a_17=S_17-S_16` | `REVERSE_CUMULATIVE_MISSED` |
| R3 | AP; test constant first difference | `AP_GP_SURFACE_CLASSIFICATION` |
| R4 | GP; test adjacent ratio | `DIFFERENCE_RATIO_NOT_TESTED` |
| R5 | check `|r|<1` before infinite-GP formula | `CONVERGENCE_OMITTED` |
| R6 | selected-term ratio; use `a_p/a_q=r^(p-q)` | `GP_HIGH_POWER_EXPANDED` |
| R7 | expose polynomial summand and split sigma | `WEIGHTED_SUM_NOT_SPLIT` |
| R8 | nested accumulation -> count multiplicity / collapse inner sum | `NESTED_MULTIPLICITY_ERROR` |
| R9 | reciprocal transform `b_n=1/a_n` | `RECIPROCAL_CUE_MISSED` |
| R10 | affine recurrence -> fixed-point shift; fixed point is `-4` | `FIXED_POINT_SHIFT_MISSED` |
| R11 | functional recurrence -> strategic index navigation | `STRATEGIC_INDEX_MISSED` |
| R12 | rational telescoping by partial fractions | `TELESCOPING_TRIGGER_MISSED` |
| R13 | rationalize to create adjacent radical differences | `TELESCOPING_TRIGGER_MISSED` |
| R14 | finite differences; constant second difference -> quadratic hypothesis, then verify | `DEGREE_HYPOTHESIS_UNVERIFIED` |
| R15 | verify proposed closed form by recurrence + initial condition | `DISCOVERY_VERIFICATION_CONFUSION` |
| R16 | block sum `S_25-S_6` | `BLOCK_SUM_ENDPOINT_ERROR` |
| R17 | finite GP is valid even if `|r|>1`; no convergence gate needed | `FINITE_INFINITE_CONFUSION` |
| R18 | geometry-primary `BRIDGE_EVIDENCE`; no Sequence-frequency inflation | `PRIMARY_DOMAIN_INFLATION` |
| R19 | solve printed mathematics independently; record/block source conflict | `SOURCE_SILENT_REPAIR` |
| R20 | GP with `r=-2`; an infinite extension diverges because `|r|>1` | `NEGATIVE_RATIO_SIGN_LOST` / `CONVERGENCE_OMITTED` |

`RECOGNITION_AUDIT: 20/20 PASS`

These are fresh Wave-4 prompts and are not the Wave-3 recognition lab.

---

# B. First-line key — 12/12

## F1
`S_30-S_11`

## F2
`a_{n+1}-a_n=5`

## F3
`a_{n+1}/a_n=3`

## F4
`|r|=2/3<1`

## F5
`a_50/a_47=r^3`

## F6
`sum k(5k+2)=5sum k^2+2sum k`

## F7
`sum_{j=1}^{k}1=k`, hence reduce the outer sum.

## F8
Set `b_n=1/a_n`.

## F9
Solve the fixed point `c=4c-6`, so `c=2`; set `b_n=a_n-2`.

## F10
`a_n=S_n-S_{n-1}`.

## F11
`1/[(k+3)(k+4)]=1/(k+3)-1/(k+4)`.

## F12
Write first differences `6,8,10,12,...`, then inspect second differences.

`FIRST_LINE_AUDIT: 12/12 PASS`

---

# C. Mixed solve / transfer key — 18/18

## C1 — `670`

`a_9-a_3=6d=18`, so `d=3`; `a=5`. Then

`S_20=20/2[2(5)+19(3)]=670`.

Diagnostic: `INDEX_GAP_ERROR`, `TERM_SUM_CONFUSION`.

## C2 — `59`

`a_n=S_n-S_{n-1}=4n-1`, so `a_15=59`.

Diagnostic: `REVERSE_CUMULATIVE_MISSED`.

## C3 — `16`

`a_7/a_4=r^3=192/24=8`, so real `r=2`. Therefore

`a_25/a_21=r^4=16`.

Diagnostic: `GP_HIGH_POWER_EXPANDED`, `INDEX_GAP_ERROR`.

## C4 — `63/16`

Finite GP:

`6[1-(-1/2)^6]/[1-(-1/2)] = 63/16`.

No convergence condition is needed because the sum is finite.

Diagnostic: `FINITE_INFINITE_CONFUSION`, `NEGATIVE_RATIO_SIGN_LOST`.

## C5 — `r=1/3`

`18=12/(1-r)` gives `1-r=2/3`, so `r=1/3`. Check `|r|=1/3<1`.

Diagnostic: `CONVERGENCE_OMITTED`.

## C6 — `1794`

`sum k(3k-2)=3sum k^2-2sum k` for `k=1..12`.

`sum k^2=650`, `sum k=78`, so `1950-156=1794`.

Diagnostic: `SUMMAND_NOT_EXPOSED`, `STANDARD_SUM_SELECTION_ERROR`.

## C7 — `680`

Inner sum:

`1+2+...+k=k(k+1)/2`.

Hence

`1/2(sum k^2 + sum k)` through 15.

`sum k^2=1240`, `sum k=120`, so result `680`.

Diagnostic: `NESTED_MULTIPLICITY_ERROR`, `SIGMA_BOUND_ERROR`.

## C8 — `1/35`

Set `b_n=1/a_n`:

`b_{n+1}=b_n+3`, `b_1=2`.

Thus `b_n=2+3(n-1)=3n-1`, so `b_12=35` and `a_12=1/35`.

Diagnostic: `RECIPROCAL_CUE_MISSED`, `INITIAL_CONDITION_ERROR`.

## C9 — `261`

Fixed point solves `c=2c-5`, so `c=5`. Set `b_n=a_n-5`.

Then `b_{n+1}=2b_n`, `b_1=2`, hence `b_n=2^n`. Therefore `a_8=256+5=261`.

Diagnostic: `FIXED_POINT_SHIFT_MISSED`, `MAP_BACK_OMITTED`.

## C10 — `36`

Use equal-index doubling:

`a_2=1+1+1=3`,

`a_4=3+3+4=10`,

`a_8=10+10+16=36`.

Diagnostic: `STRATEGIC_INDEX_MISSED`, `FUNCTIONAL_RECURRENCE_OVERGENERALIZED`.

## C11 — `20/69`

`1/[(k+2)(k+3)] = 1/(k+2)-1/(k+3)`.

The sum is

`1/3-1/23=20/69`.

Diagnostic: `TELESCOPING_ENDPOINT_ERROR`.

## C12 — `3`

Rationalize:

`1/(sqrt(k)+sqrt(k+1))=sqrt(k+1)-sqrt(k)`.

From `k=4` to `24`, survivors are `sqrt(25)-sqrt(4)=5-2=3`.

Diagnostic: `RATIONALIZATION_ERROR`, `TELESCOPING_ENDPOINT_ERROR`.

## C13 — `441`

Terms match `(n+1)^2`: `4,9,16,25,36`. The first differences `5,7,9,11` have constant second difference 2, supporting a quadratic hypothesis. Verify the rule on the supplied terms. Then

`a_20=21^2=441`.

Diagnostic: `DEGREE_HYPOTHESIS_UNVERIFIED`.

## C14 — `824`

Block sum:

`S_25-S_9`.

`S_25=25(76)/2=950`, `S_9=9(28)/2=126`, hence `824`.

Diagnostic: `BLOCK_SUM_ENDPOINT_ERROR`.

## C15 — `2005`

Directly checked finite weighted-geometric accumulation:

`1+6+27+108+405+1458=2005`.

Preferred structure is shift/alignment rather than term-by-term arithmetic for larger bounds.

Diagnostic: `WEIGHTED_GP_ENDPOINT_ERROR`.

## C16 — `-40`

Pair adjacent terms:

`(1-3)+(5-7)+...+(77-79)`.

There are 20 pairs, each `-2`, so total `-40`.

Diagnostic: `REPRESENTATION_SWITCH_MISSED`.

## C17 — `1020`

`sum_{k=1}^{30}(2k+3)=2sum k+3(30)`.

`2(465)+90=1020`.

Diagnostic: `WORDING_TO_SUMMAND_MISSED`.

## C18 — `SOURCE_CONFLICT_EVIDENCE / BLOCK_CANONICAL_USE`

Required actions:

1. solve the printed mathematics independently;
2. preserve the reproduced wording and the provisional key as separate evidence;
3. record the conflict;
4. block clean canonical historical use until resolved.

Forbidden: silently changing the term position/wording to make the key work.

Diagnostic: `SOURCE_SILENT_REPAIR`, `SOURCE_KEY_TRUSTED_OVER_MATH`.

`MIXED_SOLVE_TRANSFER_AUDIT: 18/18 PASS`

## Transfer classification — no inflation

Do **not** call all 18 items transfer.

- routine / near mastery: `C1–C6`, `C8–C9`, `C11–C14`;
- bridge-transfer: `C7`, `C10`, `C15`;
- stronger changed-surface/context transfer: `C16`, `C17`, `C18`.

`TRANSFER_COUNT_INFLATION_PREVENTED: PASS`

---

# D. WHY-NOT key — 6/6

## W1
An AP requires **constant first differences**. Here differences are `4,6,8,10,...`; regular growth of differences is a quadratic signal, not an AP invariant.

## W2
The ratio is `r=3/2`, so `|r|>1`. The infinite-GP formula requires tail decay; the series diverges.

## W3
For terms in the same GP,

`a_60/a_57=r^3`.

Computing both huge terms preserves common factors that the target immediately cancels.

## W4
A transform must simplify the recurrence. For `a_{n+1}=3a_n+4`, the fixed point solves `c=3c+4`, so `c=-2`, and `b_n=a_n+2` gives `b_{n+1}=3b_n`. A reciprocal does not expose a simpler linear invariant here.

## W5
Telescoping cancels **interior** terms, not boundary terms. The first positive term and final negative term survive.

## W6
Source custody forbids retrofitting a historical stem to its key. Preserve both pieces of evidence and block canonical use instead.

`WHY_NOT_AUDIT: 6/6 PASS`

---

# E. Recurrence / telescoping / high-index key — 4/4

## E1 — `27`

Positive-term GP gives positive `r`. From

`a_12/a_8=r^4=81`,

`r=3`. Therefore

`a_100/a_97=r^3=27`.

## E2 — `1/13`

Take reciprocals:

`1/a_{n+1}=(2+a_n)/(2a_n)=1/a_n+1/2`.

Let `b_n=1/a_n`; then `b_1=1` and

`b_n=1+(n-1)/2=(n+1)/2`.

So `b_25=13` and `a_25=1/13`.

## E3 — `20/41`

`1/[(2k-1)(2k+1)] = (1/2)[1/(2k-1)-1/(2k+1)]`.

Survivors:

`(1/2)(1-1/41)=20/41`.

## E4 — `100`

Strategic doubling:

`a_2=2+2+3=7`,

`a_4=7+7+3(2)(2)=26`,

`a_8=26+26+3(4)(4)=100`.

`STATE_RECURRENCE_HIGH_INDEX_AUDIT: 4/4 PASS`

---

# Source-custody gate

- clean scored anchors remain the six frozen Wave-0 IDs;
- `NMTC-BH-P-2024-Q11` remains one historical anchor despite recurrence/telescoping crossover;
- `NMTC-BH-P-2024-Q13` remains geometry-primary bridge evidence only;
- `NMTC-BH-P-2025-Q30` remains `SOURCE_CONFLICT_EVIDENCE / SOURCE_KEY_CONFLICT_NOT_CANONICAL`;
- no historical stem is silently reproduced or repaired in this Wave-4 paper;
- all Wave-4 problem wording is `AUTHOR_CREATED_MASTERY_OR_TRANSFER` unless explicitly described as an abstract source-QC scenario.

`SOURCE_CUSTODY: PASS`

---

# Wave-4 teacher gate

| Gate | Result |
|---|---|
| recognition prompts | 20/20 PASS |
| first-line prompts | 12/12 PASS |
| mixed solve/transfer items | 18/18 PASS |
| WHY-NOT contrasts | 6/6 PASS |
| recurrence/telescoping/high-index challenge | 4/4 PASS |
| fresh Wave-4 recognition set | PASS |
| student/teacher separation | PASS |
| independent arithmetic/index checks | PASS |
| convergence conditions | PASS |
| recurrence transforms | PASS |
| telescope endpoints | PASS |
| finite-difference verification | PASS |
| source conflict preserved | PASS |
| transfer count inflation prevented | PASS |
| PDF/render QA | NOT_RUN — Wave 5 |
| classroom timing/readability | NOT_RUN |

`WAVE4_TEACHER_KEY_GATE: PASS`