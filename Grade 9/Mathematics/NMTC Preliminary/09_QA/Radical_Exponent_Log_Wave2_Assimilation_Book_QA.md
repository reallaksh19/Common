# Issue #45 — Wave 2 Integrated Assimilation Book QA

`ARTIFACT: Radical_Exponent_Log_Assimilation_Book_v2.md`

`WAVE: 2`

`STATUS: PASS_INTERNAL`

`COMPLETION_STATE: INTERNAL_ASSIMILATION_COMPLETE`

This QA audits the integrated teaching source only. It does not promote Wave 3 First-Step, Wave 4 mastery, Wave 5 PDF/render, classroom calibration or publication approval.

---

# 1. Architecture audit

| Requirement | Evidence in book | Status |
|---|---|---|
| concept map existed before prose | Wave 0 artifact precedes Wave 2 commits | PASS |
| partial-knowledge learner model | opening + RECONNECT diagnostic | PASS |
| `RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER` | Sections 1–15 | PASS |
| no naked-formula opening | starts from operating idea and diagnostic | PASS |
| representation switching central | Sections 2–6, 9–11 | PASS |
| reversibility is cross-stream, not appendix-only | Sections 0, 7, 11–13 | PASS |
| attempt before hint | every supported TRY/fade item instructs H0 first | PASS |
| H3 -> H0 fading | four 4-item tracks in Section 13 | PASS |
| error laboratory | 11 explicit failure models | PASS |
| mixed unlabelled ADOPT | 14 items | PASS |
| non-identical transfer | 6 items | PASS |
| First-Step withheld until after teaching | no Wave-3 reference artifact embedded | PASS |
| source custody visible | Sections 3–11 and 17 | PASS |

---

# 2. Decision-boundary / contrast audit

The book contains at least eight explicit close contrasts, exceeding Issue #45's minimum six:

1. product radical splitting vs false sum splitting;
2. common radical basis vs hidden-square reconstruction;
3. rationalize automatically vs use structure first;
4. negative exponent vs negative base;
5. common-base exponent normalization vs unnecessary logarithms;
6. squaring vs cubing over the reals;
7. division by a non-zero constant vs division by a zero-capable variable expression;
8. symmetric reciprocal target vs asymmetric target;
9. log product law vs nonexistent log-sum law;
10. `t=log_b x` vs `u=sqrt(log_b x)`;
11. transformed algebraic candidate vs original-domain solution;
12. learner error vs source conflict.

`CONTRAST_DECISION_BOUNDARY_GATE: PASS_STRONG`

---

# 3. Hint-fading audit

Section 13 contains four independent fading tracks:

- radical/surd;
- exponent normalization;
- reversibility;
- logarithms.

Each track uses:

`max H3 -> max H2 -> max H1 -> H0 only`

and each item still begins with an H0 attempt before any rescue cue is shown.

H3 gives a first algebraic relation or explicit representation only; it does not reveal a complete worked solution.

`ATTEMPT_BEFORE_HINT: PASS`

`H3_TO_H0_FADING: PASS`

---

# 4. Independent mathematics audit

Every distinct computed result or condition promoted in the teaching source was recomputed independently. Repeated items in the fading/ADOPT sections were checked against the same independently verified result rather than assumed correct because they appeared earlier.

## 4.1 Reconnect

| Item | Recomputed result | Status |
|---|---|---|
| `sqrt(72)` | `6sqrt(2)` | PASS |
| `16^(-3/4)` | `1/8` | PASS |
| `sqrt((x-4)^2)` | `|x-4|` | PASS |
| `4^x=8` | `x=3/2` | PASS |
| `log_3 81=4` | `3^4=81` | PASS |
| `dom log_2(x-5)` | `x>5` | PASS |
| `t+t^-1=4 -> t^2+t^-2` | `14` | PASS |
| squaring reversibility | not reversible in general | PASS |
| log sum law | false | PASS |
| `u=sqrt(log_2 x)` | `u>=0`, original `x>0` | PASS |

## 4.2 Radical / surd calculations

| Expression / claim | Independent check | Status |
|---|---|---|
| `(sqrt98-sqrt8)/sqrt2` | `(7-2)=5` | PASS |
| `sqrt(21-8sqrt5)` | `(4-sqrt5)^2=21-8sqrt5`, positive branch | PASS |
| `1/(sqrt5+sqrt2)` | conjugate gives `(sqrt5-sqrt2)/3` | PASS |
| `sqrt(13-4sqrt10)` | `(2sqrt2-sqrt5)^2=13-4sqrt10`, positive branch | PASS |
| `sqrt((3x+1)^2)` | `|3x+1|`; sign cutoff `x=-1/3` | PASS |
| `1/(sqrt7+sqrt2)+1/(sqrt7-sqrt2)` | `2sqrt7/5` | PASS |
| transfer `sqrt(28-12sqrt5)` | `(3sqrt2-sqrt10)^2=28-12sqrt5` | PASS |

The transfer item deliberately falsifies the tempting but incorrect `(3-sqrt5)^2` reconstruction before deriving the correct one. The stale pattern-match is not promoted as an answer.

## 4.3 Exponent calculations

| Expression / equation | Recomputed result | Status |
|---|---|---|
| `27^(-2/3)` | `1/9` | PASS |
| `8^x=4^(x+1)` | `x=2` | PASS |
| `9^x-10*3^x+9=0` | `x=0,2` | PASS |
| `9^x-5*6^x+4*4^x=0` | `x=0` or `log_(3/2)4` | PASS |
| `16^x=8^(x+1)` | `x=3` | PASS |
| `32^(3/5)*8^(-2/3)` | `8*(1/4)=2` | PASS |
| transfer `25^x-5*10^x+4*4^x=0` | `x=0` or `log_(5/2)4` | PASS |

All substitutions of the form `t=a^x` or ratio-power variables retain `t>0`.

## 4.4 Reversibility / equation checks

| Case | Independent conclusion | Status |
|---|---|---|
| `sqrt(x+1)=x-1` | domain `x>=1`; unique valid root `3` | PASS |
| `(x-2)(x+3)=0` | `x=2,-3`; division by `x-2` would lose a case | PASS |
| arrow lab | `=>, <=>, <=>, =>, <=>` | PASS |
| `sqrt(x+4)=x-2` | domain `x>=2`; valid root `5` | PASS |
| `(x-1)(x+4)=0` | `x=1,-4` | PASS |
| `sqrt(2x+3)=3sqrt(x-1)` | domain `x>=1`; `x=12/7`; valid | PASS |

Logical boundary rechecked:

- squaring is not injective over reals;
- cubing is injective over reals;
- multiplication by a zero-capable expression can add solutions;
- division by one can lose solutions;
- restricted nonnegative square-root equations can make squaring equivalent when both sides are known nonnegative.

## 4.5 Reciprocal invariant calculations

| Given | Target | Recomputed result | Status |
|---|---|---|---|
| `x+x^-1=5` | `x^2+x^-2` | `23` | PASS |
| same | `x^3+x^-3` | `110` | PASS |
| `x+x^-1=4` | `x^4+x^-4` | `194` | PASS |
| same | `x-x^-1` | `±2sqrt3` | PASS |
| `x+x^-1=6` | `x-x^-1` | `±4sqrt2` | PASS |

Recurrence `S_n=S_1 S_(n-1)-S_(n-2)` was rederived from multiplication, not merely copied.

## 4.6 Logarithm calculations and domains

| Expression / equation | Recomputed result | Status |
|---|---|---|
| `25^(log_5 3)` | `9` | PASS |
| `(log_2 x)^2-5log_2 x+6=0` | `x=4,8` | PASS |
| `log_2 x-5sqrt(log_2 x)+4=0` | `x=2,65536` | PASS |
| `log_3 x-4sqrt(log_3 x)+3=0` | `x=3,19683` | PASS |
| `log_4 x=log_2 y`, `x-y=6`, positive variables | `x=9,y=3,x+y=12` | PASS |
| `log_2(x-3)=2log_2(x-5)` | algebra `4,7`; domain `x>5`; valid `7` | PASS |
| fading `(log_2 x)^2-3log_2 x+2=0` | `x=2,4` | PASS |
| positive `log_9 x=log_3 y`, `x-y=20` | `x=25,y=5,x+y=30` | PASS |
| `25^(log_5 2)` | `4` | PASS |
| `27^(log_3 2)` | `8` | PASS |
| transfer `log_3(x-1)=2log_3(x-4)` | algebra roots `(9±sqrt13)/2`; domain `x>4`; retain `(9+sqrt13)/2` | PASS |

Log base/argument restrictions are stated before inverse/injectivity arguments where material. `u=sqrt(log_b x)` carries `u>=0`.

`WAVE2_MATH_AUDIT: PASS`

No stale answer was found after independent recomputation.

---

# 5. Mixed adoption / transfer audit

## ADOPT

- 14 unlabelled prompts;
- all require a first move before solution;
- covers radical basis, hidden surd, exponent meaning, base normalization, reciprocal invariant, reversibility, log substitution, log-to-algebra, exact inverse, zero-case and source QC;
- no method labels are printed with the questions.

`ADOPT_UNLABELLED: PASS`

## TRANSFER

Six transfer items alter representation or decision structure rather than merely changing numbers:

1. radical/exponent-language bridge;
2. false hidden-square near-miss requiring verification;
3. exponent ratio disguise;
4. symmetric-to-asymmetric reciprocal boundary;
5. disguised exact log/exponent inverse;
6. log-domain branch filtering after algebra.

`NON_IDENTICAL_TRANSFER: PASS`

---

# 6. Source-custody audit

| Class | Disposition | Status |
|---|---|---|
| `CLEAN_SCORED_ANCHOR` | 16 qualified mechanism IDs retained | PASS |
| `SOURCE_SENSITIVE_EVIDENCE` | 2023 Q04/Q20 remain bridge-only | PASS |
| `SOURCE_CONFLICT_EVIDENCE` | 2025 Q18 remains QC-only | PASS |
| `BONUS_EVIDENCE` | none identified; none inferred | PASS |
| `AUTHOR_CREATED_FOUNDATION` | original teaching/diagnostic examples | PASS |
| `AUTHOR_CREATED_TRANSFER` | original ADOPT/transfer material; no fake PYQ labels | PASS |

No full historical third-party problem statement was reproduced in the new Wave-2 source.

`SOURCE_CUSTODY: PASS`

---

# 7. Benchmark-quality comparison at Wave 2

Compared with the Quadratics assimilation benchmark architecture, without copying wording/layout:

| Benchmark property | Wave-2 status |
|---|---|
| partial-knowledge reconnect | PASS |
| missing bridge explicit | PASS |
| invariant/representation visible | PASS |
| decision boundary / near-miss | PASS_STRONG |
| attempt before hint | PASS |
| H3 -> H0 fading | PASS |
| independent first move | PASS |
| error diagnosis | PASS |
| non-identical transfer | PASS |
| source custody | PASS |
| independent mathematics audit | PASS |

Visual/render comparison is not applicable yet because Issue #45 reserves PDF production for Wave 5.

---

# 8. Wave-2 gate table

| Gate | Status | Note |
|---|---|---|
| one coherent Assimilation Book | PASS | six interfaces integrated, not concatenated |
| required teaching choreography | PASS | full loop present |
| no naked formula opening | PASS | diagnostic/representation first |
| at least six contrast pairs | PASS_STRONG | 12 boundaries represented |
| reversibility interleaved | PASS | radical/exponent/log checkpoints |
| attempt before hint | PASS | H0 first |
| H3 -> H0 fading | PASS | 4 tracks |
| error laboratory | PASS | 11 errors |
| mixed unlabelled ADOPT | PASS | 14 items |
| transfer | PASS | 6 non-identical items |
| source conflicts preserved | PASS | 2025 Q18 unchanged in disposition |
| independent answer/domain audit | PASS | all promoted computations rechecked |
| First-Step Reference | NOT_RUN | Wave 3, correctly deferred |
| full Wave-4 mastery counts | NOT_RUN | next after First-Step |
| student/teacher PDF render | NOT_RUN | Wave 5 |
| page-by-page render inspection | NOT_RUN | Wave 5 |
| classroom timing/readability | NOT_RUN | requires observation |
| longitudinal retention/transfer | NOT_RUN | requires evidence |

`WAVE2_INTEGRATED_ASSIMILATION_BOOK: PASS`

`NEXT_ALLOWED_STATE: WAVE3_FIRST_STEP_REFERENCE`
