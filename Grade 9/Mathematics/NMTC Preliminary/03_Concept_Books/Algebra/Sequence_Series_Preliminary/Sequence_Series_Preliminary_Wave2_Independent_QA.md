# Issue #49 — Wave 2 Independent QA

`ARTIFACT: Sequence_Series_Preliminary_Assimilation_Book_v2.md`

`QA_LAYER: TEACHER / INTERNAL`

`STUDENT_ANSWER_LEAKAGE_ALLOWED: NO`

---

# 1. Architecture audit

| Requirement | Result |
|---|---|
| integrated book rather than seven pasted interfaces | PASS |
| opens with reconnect diagnostic, not formula sheet | PASS |
| governing structure repeated across streams | PASS — `TARGET OBJECT -> STABLE STRUCTURE -> REPRESENTATION SWITCH -> COLLAPSE -> CHECK -> ORIGINAL OBJECT` |
| deep chapter remains derivation authority | PASS |
| Preliminary overlay remains competition-grounding authority | PASS |
| close contrast pairs | PASS — 13 explicit |
| attempt before hint | PASS — diagnostics/fading/ADOPT/transfer precede Hint Bank |
| H3->H2->H1->H0 fading | PASS — 4 independent tracks |
| integrated error lab | PASS — 12 cases |
| mixed unlabelled ADOPT | PASS — 16 items |
| changed-surface transfer | PASS — 12 items |
| First-Step compression authored early | NO — correctly deferred to Wave 3 |
| historical exact wording reproduced | NO |
| 2025 Q30 silently repaired | NO |
| 2024 Q13 inflated as Sequence primary evidence | NO |

`WAVE2_ARCHITECTURE_GATE: PASS`

---

# 2. Contrast-pair audit — 13/13

1. `a_n` vs `S_n`;
2. direct nth-term route vs reverse from `S_n`;
3. AP vs GP;
4. finite vs infinite GP;
5. absolute high-index target vs relative ratio target;
6. polynomial indexed term vs AP/GP reflex;
7. polynomial weight vs geometric weight;
8. reciprocal recurrence vs fixed-point shift;
9. strategic indices vs global closed form;
10. discovery vs verification;
11. telescope recognition vs endpoint custody;
12. constant second difference vs AP;
13. source conflict vs silent repair, with primary-domain bridge discipline integrated.

The issue minimum is seven. Wave 2 provides thirteen structurally distinct boundaries.

`CONTRAST_GATE: 13/13 PASS`

---

# 3. Reconnect diagnostic independent key — 10/10

## D1

`4,7,10,...`, 25th term.

- target: `a_25`;
- AP `d=3`;
- result: `4+24·3=76`.

## D2

Same AP, first 25 terms.

- target: `S_25`;
- result: `25/2[2·4+24·3]=1000`.

## D3

`S_n=n(2n+1)=2n^2+n`.

`a_n=S_n-S_{n-1}=4n-1`.

## D4

`3,6,12,24,...` is GP with `r=2`.

Finite sums are valid; an infinite extension does not converge because `|r|=2>1`.

## D5

`a_8/a_5=r^3=384/48=8`; therefore `a_30/a_27=r^3=8`.

## D6

`sum k(3k-1)=3sum k^2-sum k` for `k=1..10`.

Result: `3·385-55=1100`.

## D7

Take reciprocals:

`1/a_{n+1}=1/a_n+2`.

With `a_1=1`, `1/a_n=2n-1`; e.g. `a_6=1/11`.

## D8

`1/[(k+1)(k+2)]=1/(k+1)-1/(k+2)`.

Sum `k=1..5` gives `1/2-1/7=5/14`.

## D9

First differences `4,6,8,10`; second differences constant 2.

Verified rule: `a_n=n^2+n+1`; `a_10=111`.

## D10

Correct first action: solve printed mathematics independently, compare with key, record source conflict, block canonical use. Do not repair the stem.

`RECONNECT_MATH_AUDIT: 10/10 PASS`

---

# 4. Worked-mechanism audit

Independent checks of numerical claims used in teaching prose:

- AP `a=5,d=3`: `a_20=62`, `S_20=670` — PASS;
- `S_n=3n^2+2n`: `a_n=6n-1` — PASS;
- finite GP `3+6+12+24+48+96=189` — PASS;
- infinite GP `2,-1,1/2,-1/4,...`: `r=-1/2`, sum `4/3` — PASS;
- selected GP `a_3=12,a_6=96`: `r^3=8`, so `a_20/a_17=8` — PASS;
- `sum_{1..10}k(2k+1)=825` — PASS;
- nested `sum_{k=1}^{10}sum_{j=1}^{k}1=55` — PASS;
- weighted geometric `1+2·2+3·2^2+4·2^3+5·2^4=129` — PASS;
- reciprocal recurrence `a_1=1`, `a_{n+1}=a_n/(1+a_n)`: `a_20=1/20` — PASS;
- affine recurrence `a_1=1`, `a_{n+1}=2a_n+3`: `a_10=2045` — PASS;
- functional recurrence `a_{m+n}=a_m+a_n+2mn`, `a_1=1`: `a_8=64` — PASS;
- rational telescope through 20: `20/21` — PASS;
- finite-difference rule `2,6,12,20,30 -> a_n=n(n+1)` — PASS.

`WORKED_MECHANISM_MATH_GATE: PASS`

---

# 5. Error-lab diagnostic key — 12/12

| ID | Primary diagnosis | Required repair |
|---|---|---|
| E1 | `TERM_SUM_CONFUSION / FORMULA_BEFORE_OBJECT` | label `TARGET=a_30` before selecting a formula |
| E2 | `INDEX_SHIFT_OFF_BY_ONE` | term 1 has zero repeated changes, so exponent is `n-1` |
| E3 | `AP_GP_SURFACE_CLASSIFICATION` | test differences/ratios rather than visual growth |
| E4 | `CONVERGENCE_OMITTED` | `r=3/2` fails `|r|<1`; no finite infinite-GP sum |
| E5 | `GP_HIGH_POWER_EXPANDED` | divide selected terms; target sees only exponent gap 3 |
| E6 | `WEIGHTED_SUM_FORCED_TO_AP_GP` | expose polynomial kth term and split the sum |
| E7 | `WRONG_TRANSFORM_CHOICE` | affine recurrence suggests fixed-point shift, not reciprocal |
| E8 | `DISCOVERY_VERIFICATION_CONFUSION` | substitution verifies a candidate; it does not explain discovery |
| E9 | `TELESCOPING_ENDPOINT_ERROR` | middle terms cancel; boundary survivors remain |
| E10 | `DEGREE_HYPOTHESIS_UNVERIFIED` | verify the candidate rule against all supplied data/conditions |
| E11 | `SOURCE_SILENT_REPAIR` | preserve wording/key conflict and block canonical use |
| E12 | `PRIMARY_DOMAIN_INFLATION` | geometry-primary GP appearance is bridge evidence only |

`ERROR_LAB_GATE: 12/12 PASS`

---

# 6. H3->H0 fading independent key — 16/16

## Track A — object / endpoints

- A-H3: `S_n=2n^2+3n`; `a_n=4n+1`; `a_8=33`.
- A-H2: terms 9..20 under triangular `S_n`; `S_20-S_8=210-36=174`.
- A-H1: `a_5=17,a_11=35`; `d=3,a=5`; `S_20=670`.
- A-H0: `S_n=4n^2-n`; `a_n=8n-5`; `a_15=115`.

## Track B — ratio / convergence

- B-H3: `8,-4,2,-1,...`; `r=-1/2`, convergent; infinite sum `16/3`.
- B-H2: `a_7/a_4=27=r^3`; `a_50/a_47=27`.
- B-H1: `r=-2`; `|r|>1`; no finite infinite sum.
- B-H0: `r^3=-27 -> r=-3`; `a_40/a_38=r^2=9`.

## Track C — recurrence transform

- C-H3: reciprocal gives `b_1=2`, `b_{n+1}=b_n+3`; `b_8=23`; `a_8=1/23`.
- C-H2: fixed point 5; `b_n=a_n-5`; `b_1=2`; `b_8=256`; `a_8=261`.
- C-H1: equal-index route gives `a_2=5,a_4=14,a_8=44`.
- C-H0: fixed point `-2`; `b_n=a_n+2`; `b_1=5`; `a_6=5·3^5-2=1213`.

## Track D — telescope / finite differences

- D-H3: `sum_{1..12}1/[k(k+1)]=12/13`.
- D-H2: radical telescope `sqrt(16)-sqrt(1)=3`.
- D-H1: second difference 2; verified `a_n=n^2+3n`; `a_12=180`.
- D-H0: `1/[(3k-2)(3k+1)]=(1/3)[1/(3k-2)-1/(3k+1)]`; result `10/31`.

`FADE_MATH_AUDIT: 16/16 PASS`

---

# 7. ADOPT independent key — 16/16

| ID | First move | Result |
|---|---|---|
| M1 | subtract indexed AP equations | `d=3,a=4,S_20=650` |
| M2 | `a_n=S_n-S_{n-1}` | `a_17=163` |
| M3 | finite GP | `85/32` |
| M4 | check `|r|<1` then infinite GP | `4` |
| M5 | selected-term ratio | `4` |
| M6 | `r^3=-8 -> r=-2`; use even gap | `4` |
| M7 | expand `k(k+2)` | `806` |
| M8 | inner sum is `2k` | `72` |
| M9 | reciprocal transform | `1/37` |
| M10 | fixed point `-6`, shift `a_n+6` | `378` |
| M11 | strategic doubling | `a_2=7,a_4=26,a_8=100` |
| M12 | rational telescope | `15/16` |
| M13 | rationalize | `sqrt(25)-sqrt(4)=3` |
| M14 | constant second difference 2; verify `n^2+4n` | `480` |
| M15 | `S_18-S_6` | `312` |
| M16 | source conflict custody | `SOURCE_CONFLICT_EVIDENCE / BLOCK_CANONICAL_USE`; no silent repair |

`ADOPT_MATH_AUDIT: 16/16 PASS`

---

# 8. Transfer independent key — 12/12

| ID | Structural route | Result / disposition |
|---|---|---|
| T1 | `S_20-S_19` | `79` seats |
| T2 | `r^3=125`, target `r^2` | `25` |
| T3 | infinite GP, `r=1/2` | `24` |
| T4 | `2sum k^2+3sum k`, `k=1..15` | `2840` |
| T5 | `S_12-S_11` | `70` |
| T6 | reciprocal: `1/c_n=2n-1` | `1/19` |
| T7 | fixed point 20; deviation halves | `x_5=165/8=20.625` |
| T8 | doubling: `F_2=3,F_4=10,F_8=36` | `36` |
| T9 | `1/[k(k+2)]=(1/2)(1/k-1/(k+2))` | `175/264` |
| T10 | radical telescope | `sqrt(36)-sqrt(9)=3` |
| T11 | constant second difference 2; verify `n^2+2n-1` | `674` |
| T12 | primary domain remains geometry | `BRIDGE_EVIDENCE`; no Sequence-frequency credit |

`TRANSFER_MATH_AUDIT: 12/12 PASS`

The transfer set changes representation/surface across cumulative rows, measured multiplicative states, shrinking paths, scoring schedules, concentrations, control recurrence, functional indexing, telescoping and geometric provenance. It is not a number-swap-only set.

---

# 9. Hint / answer leakage audit

Student attempt surfaces appear before the Hint Bank:

- reconnect diagnostics — before hints;
- four fading tracks — prompts before separated hints;
- ADOPT — all 16 prompts before recognition hints;
- TRANSFER — all 12 prompts before H1 hints.

The Hint Bank provides recognition/structure/execution cues but no final numerical answers.

Worked teaching examples contain instructional mathematics, but they are not the same prompts used as independent attempt items.

`ATTEMPT_BEFORE_HINT_GATE: PASS`

`STUDENT_ANSWER_LEAKAGE_GATE: PASS`

---

# 10. Source-custody audit

## Clean scored anchors — 6

- `NMTC-BH-P-2019-Q29`;
- `NMTC-BH-P-2023-Q15`;
- `NMTC-BH-P-2023-Q29`;
- `NMTC-BH-P-2024-Q10`;
- `NMTC-BH-P-2024-Q11`;
- `NMTC-BH-P-2024-Q27`.

## Supporting custody

- `NMTC-BH-P-2018-Q17` — foundation support only;
- `NMTC-BH-P-2024-Q13` — geometry-primary bridge only.

## Blocked

- `NMTC-BH-P-2025-Q30` — `SOURCE_CONFLICT_EVIDENCE / SOURCE_KEY_CONFLICT_NOT_CANONICAL`.

No exact historical problem is reproduced in the Wave-2 student attempt sets. All diagnostics/fading/ADOPT/transfer items are author-created.

`SOURCE_DOUBLE_COUNT_GUARD: PASS`

`SOURCE_CONFLICT_FREEZE: PASS`

---

# 11. Wave-2 gate

| Gate | Result |
|---|---|
| integrated rather than stitched | PASS |
| reconnect diagnostic | PASS |
| no formula-sheet opening | PASS |
| object identity taught before method selection | PASS |
| index meaning / `n-1` explained | PASS |
| AP vs GP invariant boundary | PASS |
| finite vs infinite convergence boundary | PASS |
| high-index cancellation | PASS |
| weighted/nested representation choice | PASS |
| recurrence transform selection | PASS |
| strategic functional recurrence | PASS |
| discovery vs verification | PASS |
| reverse-from-sum | PASS |
| telescope endpoint custody | PASS |
| finite-difference verification discipline | PASS |
| source conflict + primary-domain custody | PASS |
| explicit close contrasts | 13 — PASS |
| error lab | 12 — PASS |
| H3->H0 fading | 4 tracks / 16 items — PASS |
| mixed unlabelled ADOPT | 16 — PASS |
| changed-surface transfer | 12 — PASS |
| reconnect math audit | 10/10 PASS |
| fading math audit | 16/16 PASS |
| ADOPT math audit | 16/16 PASS |
| transfer math audit | 12/12 PASS |
| source custody | PASS |
| First-Step Reference written early | NO — correctly deferred |
| PDF/render QA | NOT_RUN — Wave 5 |
| classroom timing/readability | NOT_RUN |

`WAVE2_GATE: PASS`

`NEXT_ALLOWED_STATE: WAVE3_FIRST_STEP_REFERENCE`
