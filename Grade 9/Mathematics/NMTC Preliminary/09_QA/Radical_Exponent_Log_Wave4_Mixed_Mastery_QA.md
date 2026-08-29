# Issue #45 — Wave 4 Mixed Mastery & Transfer QA

`STATUS: WAVE4_MIXED_MASTERY_PASS_INTERNAL`

Artifacts audited:

- `07_Mastery_Banks/Radical_Exponent_Log_Wave4_Mixed_Mastery_Student_v2.md`
- `07_Mastery_Banks/Radical_Exponent_Log_Wave4_Answer_Diagnostic_Key_v2.md`

This QA is independent of the answer-key prose: answers and conditions were recomputed from the mathematics before promotion.

---

# 1. Issue #45 quantity gates

| Requirement | Required | Produced | Status |
|---|---:|---:|---|
| recognition-only prompts | >=20 | 20 | PASS |
| first-line prompts | >=12 | 12 | PASS |
| mixed solve/transfer items | >=18 | 18 | PASS |
| WHY-NOT contrast items | >=6 | 6 | PASS |
| domain/extraneous checks | >=4 | 15 explicitly indexed | PASS_STRONG |

The student source is mixed and unlabelled by chapter. Radical, exponent, invariant, reversibility and logarithm mechanisms are interleaved.

`WAVE4_QUANTITY_GATE: PASS`

---

# 2. Recognition-key audit — 20/20

Each prompt was classified independently against the Wave-3 recognition atlas.

| Item | Audited code | Status |
|---:|---|---|
| A1 | `CB` | PASS |
| A2 | `HS` | PASS |
| A3 | `PR` | PASS |
| A4 | `EM` | PASS |
| A5 | `EN` | PASS |
| A6 | `EV` | PASS |
| A7 | `ER` | PASS |
| A8 | `RQ + DR` | PASS |
| A9 | `ZR` | PASS |
| A10 | `RI` | PASS |
| A11 | `LD` | PASS |
| A12 | `LV` | PASS |
| A13 | `LS` | PASS |
| A14 | `LA` | PASS |
| A15 | `LI` | PASS |
| A16 | `DR` | PASS |
| A17 | `QC + DR` | PASS |
| A18 | `DR` | PASS |
| A19 | `EM` | PASS |
| A20 | `EV` | PASS |

Notes:

- A7 is ratio-variable rather than repeated single-base variable because dividing by `4^x>0` produces a polynomial in `(3/2)^x`.
- A18 is classified under `DR` because the tested skill is transformation reversibility: cubing is injective on the reals.
- A20 is `EV` because `16^x=(4^x)^2`, making `4^x>0` the repeated object.

`RECOGNITION_AUDIT: 20/20 PASS`

---

# 3. First-line audit — 12/12

| Item | Required first structure | Condition custody | Status |
|---:|---|---|---|
| B1 | reduce all roots to `sqrt2` | none extra | PASS |
| B2 | reverse-square system `m+n=29`, `mn=180` | principal-root sign later | PASS |
| B3 | `sqrt((3x-4)^2)=|3x-4|` | equality to `3x-4` iff `x>=4/3` | PASS |
| B4 | `125^-2/3=1/(125^(2/3))` | base nonzero | PASS |
| B5 | `2^(6x)=2^(3x+6)` | valid positive common base | PASS |
| B6 | `t=3^x>0` | `t>0` explicit | PASS |
| B7 | divide by `9^x>0`; `t=(4/3)^x>0` | positivity explicit | PASS |
| B8 | `x>=2`; then square | side-sign restriction explicit | PASS |
| B9 | zero-product split | zero case preserved | PASS |
| B10 | reciprocal recurrence from `S0=2,S1=4` | `t!=0` inherent in premise | PASS |
| B11 | `t=log_5 x`, `x>0` | log domain explicit | PASS |
| B12 | `x,y>0`, then `x=y^2` | both log domains explicit | PASS |

`FIRST_LINE_AUDIT: 12/12 PASS`

---

# 4. Independent solve/transfer recomputation — 18/18

## C1

Common-basis recomputation:

`sqrt200=10sqrt2`, `sqrt32=4sqrt2`, `sqrt8=2sqrt2`.

Result `(10-4+2)=8`.

**Expected:** `8` — PASS.

## C2

Check proposed principal root:

`(2sqrt5-3)^2=20+9-12sqrt5=29-12sqrt5`.

`2sqrt5-3>0`.

**Expected:** `2sqrt5-3` — PASS.

## C3

`11±6sqrt2=(3±sqrt2)^2`, with both inner values positive.

Difference of cubes:

`(3+sqrt2)^3-(3-sqrt2)^3`

`=6*3^2*sqrt2+2*(sqrt2)^3`

`=54sqrt2+4sqrt2=58sqrt2`.

**Expected:** `58sqrt2` — PASS.

## C4

`125^(-2/3)=1/(5^2)=1/25`.

**Expected:** `1/25` — PASS.

## C5

`2^(5x)=2^(3x+6)` gives `2x=6`.

**Expected:** `x=3` — PASS.

## C6

`t=3^x>0` gives

`t^2-13t+36=(t-4)(t-9)`.

Both `4,9` are admissible.

**Expected:** `x=log_3 4, 2` — PASS.

## C7

Divide by `9^x>0`:

`t=(4/3)^x>0`, `t^2-10t+9=(t-1)(t-9)`.

**Expected:** `x=0` or `x=log_(4/3)9` — PASS.

## C8

Original side-sign requirement: `x>=2`.

Squaring on that domain gives

`x^2-5x-2=0`, roots `(5±sqrt33)/2`.

Only the positive branch is at least 2.

**Expected:** `(5+sqrt33)/2` — PASS.

Independent original-equation check: PASS.

## C9

Original domain: `x>=5`.

Squaring gives `x+4=4x-20`, hence `x=8`.

`8>=5` and substitution satisfies the original equation.

**Expected:** `8` — PASS.

## C10

Zero product gives `x=2,-5`.

Division by `x-2` would lose `x=2`.

**Expected:** `{2,-5}` plus zero-case explanation — PASS.

## C11

Recurrence with `S0=2`, `S1=4`:

`S2=14`, `S3=52`, `S4=194`, `S5=724`.

**Expected:** `724` — PASS.

## C12

`(x-1/x)^2=(x+1/x)^2-4=12`.

So `x-1/x=±2sqrt3` and

`x^2-x^-2=4(±2sqrt3)=±8sqrt3`.

**Expected:** not uniquely determined; values `±8sqrt3` — PASS.

## C13

`t=log_2 x` gives `(t-1)(t-4)=0`.

Back-map: `x=2,16`, both positive.

**Expected:** `2,16` — PASS.

## C14

`u=sqrt(log_3 x)>=0` gives `(u-1)(u-3)=0`.

Both roots satisfy `u>=0`.

Back-map: `log_3 x=1,9`.

**Expected:** `x=3,19683` — PASS.

## C15

For positive `x,y`, `log_9x=log_3y` implies `x=y^2`.

Then `y^2-y-20=(y-5)(y+4)=0`.

Positivity leaves `y=5`, so `x=25`.

**Expected:** `x+y=30` — PASS.

## C16

`27^(log_3 5)=(3^3)^(log_3 5)=5^3`.

**Expected:** `125` — PASS.

## C17

Original domain:

`x-1>0`, `7-x>0`, hence `1<x<7`.

Injectivity gives `x-1=7-x`, so `x=4`, which lies in the domain.

**Expected:** `4` — PASS.

## C18

Principal-root identity:

`sqrt((x-1)^2)=|x-1|`.

`|x-1|=3` gives `x=4,-2`.

**Expected:** `4,-2` — PASS.

The sign split belongs to solving the absolute-value equation, not to the radical symbol.

`SOLVE_TRANSFER_AUDIT: 18/18 PASS`

---

# 5. WHY-NOT audit — 6/6

| Item | Correct disposition | Status |
|---:|---|---|
| D1 radical over sum | INVALID generally; false distribution | PASS |
| D2 negative exponent -> negative value | INVALID; negative exponent means reciprocal | PASS |
| D3 logs first for related bases | VALID BUT INFERIOR; common-base normalization is shorter | PASS |
| D4 square before restrictions | forward implication valid, but unsafe/inferior as an equivalence claim; sign ledger missing | PASS |
| D5 divide by zero-capable factor | INVALID as equivalent step unless zero case separately preserved | PASS |
| D6 `t=log_2x` when `sqrt(log_2x)` repeats | VALID BUT INFERIOR; outer repeated object gives polynomial algebra and natural range | PASS |

`WHY_NOT_AUDIT: 6/6 PASS`

---

# 6. Domain / reversibility / extraneous-root coverage

Issue #45 requires at least four such checks. The student source explicitly indexes 15:

- B3 — principal-root sign;
- B8 — radical side-sign before squaring;
- B9 — zero-factor preservation;
- B12 — logarithm domains;
- C8 — radical admissibility/extraneous algebraic root;
- C9 — original radical domain;
- C10 — zero-case loss by division;
- C12 — invariant information insufficiency / branch sign;
- C14 — substitution range `u>=0`;
- C15 — log-domain positivity filter;
- C17 — common original log domain before injectivity;
- C18 — principal-root versus `±` equation logic;
- D4 — squaring implication/equivalence boundary;
- D5 — zero-capable division boundary;
- D6 — substitution-range-aware method choice.

`DOMAIN_REVERSIBILITY_COVERAGE: 15 explicit checkpoints — PASS_STRONG`

---

# 7. Assessment architecture audit

## Mixed / unlabelled

PASS. None of Sections A–D is divided into radical/exponent/log chapters. The learner must infer the mechanism.

## Recognition -> first line -> solve -> WHY-NOT

PASS. The assessment separates four competencies:

1. see the structure;
2. write the first useful line;
3. execute and check;
4. justify why a tempting alternative is invalid or inferior.

This prevents final-answer accuracy from hiding a method-choice deficit.

## Attempt-before-answer

PASS. Student source contains no answer key. The answer/diagnostic key is a separate file.

## Disguised transfer

PASS. Surfaces differ from the Wave-2 worked examples and from one another while preserving the same invariants/decision boundaries.

`ASSESSMENT_ARCHITECTURE: PASS`

---

# 8. Diagnostic coverage

The key distinguishes at least these failure classes:

- `REPRESENTATION_GAP`;
- `PRINCIPAL_ROOT_GAP`;
- `EXPONENT_INVERSE_GAP`;
- `REPEATED_OBJECT_GAP`;
- `REVERSIBILITY_GAP`;
- `ZERO_CASE_GAP`;
- `INVARIANT_GAP`;
- `INVARIANT_OVERGENERALIZED`;
- `DOMAIN_GAP`;
- `METHOD_CHOICE_GAP`;
- `SOURCE_INTEGRITY_GAP`;
- `EXECUTION_ERROR`.

A learner who calculates correctly but repeatedly selects inferior methods is therefore not conflated with a learner who lacks algebraic mechanics.

`DIAGNOSTIC_SPECIFICITY: PASS`

---

# 9. Provenance audit

Wave-4 item text is entirely author-created.

Historical source custody remains unchanged:

- 16 `CLEAN_SCORED_ANCHOR` IDs retained as mechanism provenance;
- `NMTC-BH-P-2023-Q04` and `NMTC-BH-P-2023-Q20` remain `SOURCE_SENSITIVE_EVIDENCE` only;
- `NMTC-BH-P-2025-Q18` remains `SOURCE_CONFLICT_EVIDENCE` / QC only;
- no topic-specific `BONUS_EVIDENCE` is identified or inferred;
- no author-created item receives a fake NMTC year/question label.

`SOURCE_CUSTODY: PASS`

---

# 10. Wave-4 gate table

| Gate | Status |
|---|---|
| one mixed unlabelled mastery layer | PASS |
| recognition-only >=20 | PASS — 20 |
| first-line >=12 | PASS — 12 |
| solve/transfer >=18 | PASS — 18 |
| WHY-NOT >=6 | PASS — 6 |
| domain/extraneous >=4 | PASS_STRONG — 15 indexed |
| recognition key independently checked | PASS — 20/20 |
| first-line key independently checked | PASS — 12/12 |
| solve/transfer answers independently recomputed | PASS — 18/18 |
| WHY-NOT dispositions checked | PASS — 6/6 |
| student/key separation | PASS |
| diagnostic tags map to repair | PASS |
| source custody | PASS |
| source conflict preserved | PASS |
| bonus evidence not inflated | PASS |
| PDF/render QA | NOT_RUN — Wave 5 |
| classroom timing/readability | NOT_RUN |
| longitudinal retention/transfer | NOT_RUN |

## Completion state

`WAVE4_MIXED_MASTERY_AND_TRANSFER_COMPLETE`

`NEXT_ALLOWED_STATE: WAVE5_FINAL_QA_AND_RENDER`
