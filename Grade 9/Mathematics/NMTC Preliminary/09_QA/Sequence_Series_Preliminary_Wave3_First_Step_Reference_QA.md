# Issue #49 — Wave 3 First-Step Reference QA

`WAVE: 3 — FIRST_STEP_REFERENCE`

`STATUS: WAVE3_FIRST_STEP_REFERENCE_PASS_INTERNAL`

Student artifact:

`Grade 9/Mathematics/NMTC Preliminary/04_First_Step_Reference/Sequence_Series_Preliminary_First_Step_Reference_v2.md`

---

# 1. Purpose audit

The artifact is a post-teaching compression layer rather than a second concept book.

Checks:

- governing decision flow present: PASS;
- starts from target/object and structure, not a formula list: PASS;
- first moves are shorter than Wave-2 explanations: PASS;
- conditions/index/endpoints retained despite compression: PASS;
- source custody retained: PASS;
- historical source statements not reproduced as exercise facsimiles: PASS;
- Wave-4 mastery counts not claimed from this Wave-3 lab: PASS.

---

# 2. Structural inventory

| Component | Count / status |
|---|---:|
| ten-second decision tree | 1 — PASS |
| recognition atlas | 18 trigger rows — PASS |
| phrase decoder | 12 cues — PASS |
| First-Step cards | 14 — PASS |
| critical contrasts | 10 — PASS |
| recognition-only prompts | 20 — PASS |
| recognition key | after all 20 prompts — PASS |
| thirty-second checks | 10 — PASS |
| source-to-first-step map | 9 source rows — PASS |
| independence self-check | present — PASS |

---

# 3. Recognition-only lab audit — 20/20

Each prompt was independently classified against the Wave-1 ownership matrix and Wave-2 teaching spine.

1. 80th term -> `a_n / POSITION`; correct.
2. sum of first 80 -> `S_n / ACCUMULATION`; correct.
3. `S_n` supplied, asks `a_25` -> `S_25-S_24`; correct.
4. terms 31..70 -> `S_70-S_30`; correct endpoint.
5. `11,15,19,23,...` -> AP candidate, difference 4; classification correct.
6. `3,-6,12,-24,...` -> GP candidate, ratio -2; sign custody correct.
7. infinite GP with `r=-3/4` -> convergence first; `|r|=3/4<1`; correct.
8. finite GP with `r=5/2` -> finite structure valid; no convergence gate required; correct.
9. far-index GP term ratio -> selected-term division/index-gap compression; correct.
10. `sum k(4k-3)` -> weighted polynomial summand; correct.
11. nested `sum sum 1` -> inner count/multiplicity; correct.
12. `a_{n+1}=a_n/(1+4a_n)` -> reciprocal transform; correct.
13. `a_{n+1}=5a_n-8` -> fixed point solves `c=5c-8`, hence `c=2`; `b_n=a_n-2`; correct.
14. `a_{m+n}` with target `a_16` -> strategic indices/doubling or decomposition before closed form; correct.
15. proposed formula + “prove” -> verification by recurrence + initial condition; correct discovery/verification boundary.
16. `1/[k(k+1)]` -> partial-fraction telescope; correct.
17. `1/(sqrt(k+2)+sqrt(k+3))` -> rationalize to neighboring radical difference; shifted endpoint warning correct.
18. `4,10,18,28,40,...` -> first differences `6,8,10,12`, second differences constant 2; finite differences, not AP/GP; correct.
19. constant-ratio circle radii with homothety as main reasoning -> geometry-primary bridge evidence only; correct source-domain custody.
20. printed GP term comparison conflicts with provisional key -> independent printed-math solution then flag/preserve/block; correct.

`RECOGNITION_LAB_AUDIT: 20/20 PASS`

---

# 4. First-Step card mathematics / legality audit

## Object and index cards

- `a_n=S_n-S_{n-1}` retained with `a_1=S_1` boundary: PASS.
- block sum uses `S_q-S_{p-1}`: PASS.
- AP/GP classification is based on invariant tests, not visual growth: PASS.

## GP cards

- infinite-GP convergence condition appears before formula use: PASS.
- selected-term relation `a_p/a_q=r^(p-q)` includes denominator/sign/index-gap custody: PASS.

## Accumulation cards

- weighted polynomial sum requires summand exposure before standard sums: PASS.
- nested accumulation uses inner simplification/multiplicity rather than brute expansion: PASS.

## Recurrence cards

- reciprocal trigger is structurally correct for `a_n/(1+c a_n)` family: PASS.
- affine fixed-point method uses `c=pc+q`, then `b_n=a_n-c`: PASS.
- functional recurrence directs learner to index navigation before unnecessary closed form: PASS.

## Telescope / finite-difference cards

- telescope card requires `v_k-v_{k+1}` form plus explicit endpoint survival: PASS.
- finite differences are stated as a hypothesis/degree signal requiring verification: PASS.

## Source-QC card

- `NMTC-BH-P-2025-Q30` remains blocked and is not silently repaired: PASS.

`FIRST_STEP_CARD_AUDIT: 14/14 PASS`

---

# 5. Critical contrast audit

Ten compressed contrasts preserve the high-value Wave-2 boundaries:

1. `a_n` vs `S_n`;
2. AP vs GP;
3. finite vs infinite GP;
4. direct term vs reverse from `S_n`;
5. absolute high-index term vs relative term ratio;
6. polynomial weighted vs geometric weighted structure;
7. recurrence iteration vs transform;
8. reciprocal vs fixed-point shift;
9. telescope recognition vs endpoint-complete telescope;
10. source conflict vs source repair.

`CONTRAST_COMPRESSION_GATE: 10/10 PASS`

---

# 6. Answer-leakage / attempt-order audit

- recognition prompts appear before the recognition key: PASS;
- prompts require method classification, not final numerical solving: PASS;
- no solution is embedded directly below its prompt: PASS;
- source IDs are used as provenance/mechanism anchors, not as reproduced historical exercise text: PASS;
- independence target is labeled a practice threshold, not psychometric validation: PASS.

`ANSWER_LEAKAGE_GATE: PASS`

---

# 7. Source custody audit

Clean scored anchors retained exactly as Wave 0/1:

- `NMTC-BH-P-2019-Q29` — functional recurrence;
- `NMTC-BH-P-2023-Q15` — weighted polynomial sum;
- `NMTC-BH-P-2023-Q29` — high-index GP cancellation;
- `NMTC-BH-P-2024-Q10` — weighted accumulation;
- `NMTC-BH-P-2024-Q11` — reciprocal recurrence / telescope bridge, counted once;
- `NMTC-BH-P-2024-Q27` — infinite-GP constraints.

Supporting-only:

- `NMTC-BH-P-2018-Q17` — foundation reconnect only;
- `NMTC-BH-P-2024-Q13` — geometry-primary bridge, no Sequence-frequency credit.

Blocked:

- `NMTC-BH-P-2025-Q30 = SOURCE_CONFLICT_EVIDENCE / SOURCE_KEY_CONFLICT_NOT_CANONICAL`.

`SOURCE_DOUBLE_COUNT_GUARD: PASS`

`SOURCE_CONFLICT_FREEZE: PASS`

---

# 8. Deferred gates

- PDF render/preflight: `NOT_RUN` — Wave 5 only.
- classroom timing/readability calibration: `NOT_RUN`.
- longitudinal retention/transfer evidence: `NOT_RUN`.
- formal publication approval: `NOT_READY`.

These external/deferred states are not promoted by static QA.

---

# 9. Wave-3 gate

| Gate | Result |
|---|---|
| post-teaching compression, not duplicate textbook | PASS |
| target/object decision remains first | PASS |
| 14 First-Step cards | 14/14 PASS |
| 10 critical contrasts | 10/10 PASS |
| recognition-only lab | 20/20 PASS |
| recognition key after attempt set | PASS |
| index / convergence / endpoint custody | PASS |
| recurrence-transform choice preserved | PASS |
| discovery vs verification boundary preserved | PASS |
| source-domain inflation blocked | PASS |
| 2025 Q30 conflict preserved | PASS |
| Wave-4 counts claimed from Wave 3 | NO — correctly separate |
| PDF/render QA | NOT_RUN — correctly deferred |

`WAVE3_GATE: PASS`

`NEXT_ALLOWED_STATE: WAVE4_MIXED_MASTERY_AND_TRANSFER`
