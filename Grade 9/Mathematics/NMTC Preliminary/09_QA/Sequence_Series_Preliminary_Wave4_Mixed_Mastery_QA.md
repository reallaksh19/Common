# Issue #49 — Wave 4 Mixed Mastery / Transfer QA

`STATUS: WAVE4_MIXED_MASTERY_TRANSFER_PASS_INTERNAL`

`PR: #57`

`BRANCH: issue-49-wave0-sequence-series-grounding`

Wave 4 is a new assessment layer. Wave-3 recognition items are **not** reused to satisfy Wave-4 counts.

---

# 1. Deliverables

Student surface:

`Grade 9/Mathematics/NMTC Preliminary/07_Mastery_Banks/Sequence_Series_Preliminary_Wave4_Mixed_Mastery_Student_v2.md`

Teacher / diagnostic authority:

`Grade 9/Mathematics/NMTC Preliminary/07_Mastery_Banks/Sequence_Series_Preliminary_Wave4_Answer_Diagnostic_Key_v2.md`

This QA file is the independent Wave-4 gate.

---

# 2. Exact Issue-49 count gate

| Requirement | Required | Delivered | Result |
|---|---:|---:|---|
| recognition prompts | >=20 | 20 | PASS |
| first-line prompts | >=12 | 12 | PASS |
| solve/transfer items | >=18 | 18 | PASS |
| WHY-NOT contrasts | >=6 | 6 | PASS |
| recurrence/telescoping/high-index items | >=4 | 4 | PASS |

`COUNT_GATE: PASS`

The four special items are additional challenge items; they are not used to conceal a shortfall in the 18 mixed solve/transfer items.

---

# 3. Recognition audit — 20/20

The fresh Wave-4 set covers:

1. cumulative target / `S_n`;
2. reverse from partial sums;
3. AP by first difference;
4. GP by adjacent ratio;
5. infinite-GP convergence;
6. high-index GP cancellation;
7. polynomial weighted sum;
8. nested multiplicity;
9. reciprocal recurrence;
10. affine fixed-point shift;
11. functional recurrence / strategic indices;
12. rational telescoping;
13. radical telescoping;
14. finite-difference quadratic signal + verification;
15. closed-form verification versus discovery;
16. block partial-sum endpoints;
17. finite GP with `|r|>1`;
18. geometry-primary bridge classification;
19. historical source conflict;
20. negative-ratio GP plus infinite divergence.

`RECOGNITION_AUDIT: 20/20 PASS`

`WAVE3_RECOGNITION_REUSE: NO`

---

# 4. First-line audit — 12/12

Expected first lines were independently checked:

- F1 `S_30-S_11`;
- F2 first difference `=5`;
- F3 adjacent ratio `=3`;
- F4 `|r|=2/3<1`;
- F5 `a_50/a_47=r^3`;
- F6 `5sum k^2+2sum k`;
- F7 inner sum equals `k`;
- F8 `b_n=1/a_n`;
- F9 fixed point `2`, `b_n=a_n-2`;
- F10 `a_n=S_n-S_{n-1}`;
- F11 adjacent partial-fraction difference;
- F12 first differences then second differences.

`FIRST_LINE_AUDIT: 12/12 PASS`

---

# 5. Independent mixed-solve recomputation — 18/18

The authored key was not accepted on trust. Results were recomputed independently.

| ID | Recomputed result | Structural check |
|---|---|---|
| C1 | `670` | AP index gap `6d=18`, then `S_20` |
| C2 | `59` | `a_n=S_n-S_{n-1}=4n-1` |
| C3 | `16` | `r^3=8`, target `r^4` |
| C4 | `63/16` | finite GP, negative ratio retained |
| C5 | `r=1/3`; `|r|<1` | infinite-GP condition explicit |
| C6 | `1794` | `3Σk²-2Σk`, bounds 1..12 |
| C7 | `680` | inner triangular sum; bounds 1..15 |
| C8 | `1/35` | reciprocal AP `b_n=3n-1` |
| C9 | `261` | fixed-point shift at 5; map back |
| C10 | `36` | doubling `a_2=3,a_4=10,a_8=36` |
| C11 | `20/69` | survivors `1/3-1/23` |
| C12 | `3` | survivors `sqrt25-sqrt4` |
| C13 | `441` | verified `(n+1)^2`; constant second difference 2 |
| C14 | `824` | block `S_25-S_9=950-126` |
| C15 | `2005` | weighted geometric finite sum independently totalled |
| C16 | `-40` | 20 adjacent pairs of `-2` |
| C17 | `1020` | `2Σk+90`, k=1..30 |
| C18 | block canonical use; preserve conflict | source-custody decision, no silent repair |

`MIXED_SOLVE_TRANSFER_AUDIT: 18/18 PASS`

No Wave-4 numerical correction was required after independent recomputation.

---

# 6. Special challenge recomputation — 4/4

## E1
Positive-term GP:

`r^4=81 -> r=3`; target `r^3=27`.

## E2

`1/a_{n+1}=1/a_n+1/2`.

With `b_1=1`, `b_n=(n+1)/2`; `b_25=13`; result `1/13`.

## E3

`1/[(2k-1)(2k+1)] = (1/2)[1/(2k-1)-1/(2k+1)]`.

Endpoint result `(1/2)(1-1/41)=20/41`.

## E4

`a_2=7`, `a_4=26`, `a_8=100` by strategic equal-index substitutions.

`STATE_RECURRENCE_HIGH_INDEX_AUDIT: 4/4 PASS`

---

# 7. WHY-NOT audit — 6/6

The six contrasts test a distinct rejection predicate:

1. increasing first differences are not constant first differences;
2. `|r|=3/2` rejects the infinite-GP sum formula;
3. relative GP targets reject unnecessary huge-term expansion;
4. transform choice must simplify the algebra; reciprocal is not a generic recurrence ritual;
5. telescoping leaves boundary survivors;
6. source/key disagreement rejects silent historical repair.

`WHY_NOT_AUDIT: 6/6 PASS`

---

# 8. Decision-boundary coverage

Wave 4 preserves the major Issue-49 boundaries:

- `a_n` vs `S_n`;
- direct term vs reverse from `S_n`;
- AP vs GP;
- finite vs infinite GP;
- high-index expansion vs index-gap cancellation;
- polynomial weighted vs geometric weighted accumulation;
- reciprocal vs fixed-point recurrence transform;
- strategic indices vs global closed form;
- discovery vs verification;
- ordinary rational work vs telescoping;
- telescope recognition vs endpoint custody;
- constant second difference vs AP;
- primary Sequence evidence vs incidental sequence appearance;
- source conflict vs repair.

`DECISION_BOUNDARY_COVERAGE: PASS_STRONG`

---

# 9. Transfer classification discipline

The Issue asks for 18 solve/transfer items. That does not license calling all solved items transfer.

Classification retained in the teacher key:

- routine / near mastery: `C1–C6`, `C8–C9`, `C11–C14`;
- bridge-transfer: `C7`, `C10`, `C15`;
- stronger changed-surface/context transfer: `C16`, `C17`, `C18`.

`TRANSFER_COUNT_INFLATION_PREVENTED: PASS`

---

# 10. Source custody

Frozen Wave-0 source state remains unchanged:

- clean scored anchors: `2019 Q29`, `2023 Q15`, `2023 Q29`, `2024 Q10`, `2024 Q11`, `2024 Q27`;
- `2018 Q17` = foundation support only;
- `2024 Q13` = geometry-primary `BRIDGE_EVIDENCE`, no Sequence-frequency credit;
- `2025 Q30 = SOURCE_CONFLICT_EVIDENCE / SOURCE_KEY_CONFLICT_NOT_CANONICAL`.

Additional guards:

- 2024 Q11 is not double-counted because it bridges recurrence and telescoping;
- Wave-4 student items are author-created, not historical stem reproductions;
- the abstract source-QC scenarios teach disposition without fabricating an official repaired question;
- no bonus evidence is inflated into recurrence evidence.

`SOURCE_CUSTODY: PASS`

`SOURCE_DOUBLE_COUNT_GUARD: PASS`

`SOURCE_CONFLICT_FREEZE: PASS`

---

# 11. Student / teacher separation

- student paper contains no final-answer key;
- teacher key is a separate file;
- recognition and first-line tasks do not expose later solutions;
- diagnostics are teacher-side;
- Wave-5 PDF packaging must preserve this separation.

`STUDENT_TEACHER_SEPARATION: PASS`

---

# 12. Wave-5 deferred gates

| Gate | Status |
|---|---|
| independent full-package term/sum recheck | NOT_RUN — Wave 5 |
| final recurrence/convergence/endpoint audit across Waves 2–4 | NOT_RUN — Wave 5 |
| concept-map PDF render | NOT_RUN — Wave 5 |
| Assimilation Book PDF render | NOT_RUN — Wave 5 |
| First-Step Reference PDF render | NOT_RUN — Wave 5 |
| mastery/teacher render if included in final production set | NOT_RUN — Wave 5 |
| page-by-page visual inspection | NOT_RUN — Wave 5 |
| structural PDF preflight | NOT_RUN — Wave 5 |
| classroom timing/readability calibration | NOT_RUN |
| longitudinal retention/transfer evidence | NOT_RUN |

---

# 13. Wave-4 gate

| Gate | Result |
|---|---|
| recognition count | 20/20 PASS |
| first-line count | 12/12 PASS |
| mixed solve/transfer count | 18/18 PASS |
| WHY-NOT count | 6/6 PASS |
| recurrence/telescoping/high-index count | 4/4 PASS |
| independent math audit | PASS |
| decision boundaries | PASS_STRONG |
| transfer count discipline | PASS |
| student/teacher separation | PASS |
| source custody | PASS |
| Wave-5 render evidence | NOT_RUN — correctly deferred |
| classroom evidence | NOT_RUN |

`WAVE4_GATE: PASS`

`NEXT_ALLOWED_STATE: WAVE5_INDEPENDENT_FINAL_QA_AND_RENDER`