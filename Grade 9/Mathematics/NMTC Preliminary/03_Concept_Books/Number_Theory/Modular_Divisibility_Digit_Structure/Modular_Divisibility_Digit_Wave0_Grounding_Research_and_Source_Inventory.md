# Issue #47 — Wave 0 Grounding Research & Source Inventory

`TOPIC: Modular / Divisibility / Digit Structures`

`STATUS: WAVE0_GROUNDING_COMPLETE`

`BRANCH_BASE: main@9573ec2bba234cc7cd6abcf73c4c3f3e2bc0892c`

This file records what was read and what is frozen before any Issue-47 assimilation prose is authored.

---

# 1. Required authorities read

## Pedagogy / authoring

1. `Grade 9/skills/grade9-math-assimilation/SKILL.md`  
   SHA `57a86a5e5049ff9ef096b5f747ab649f87aa18a8`

2. `Grade 9/skills/grade9-math/SKILL.md`  
   SHA `0596b88b1c3a618ec30d12880bbf537b0c02e553`

3. `Grade 9/skills/grade9-math/references/concept-book-see-realize-understand-adopt.md`  
   SHA `b7b754a80b8d6f80a5f188ada4dd75822e23ce85`

4. `Grade 9/skills/grade9-math/references/partial-knowledge-assimilation-concept-map.md`  
   SHA `2bdf90e9101263ceaa0c157f2beb9b2cd152dec9`

## NMTC authority

5. `Grade 9/Mathematics/NMTC Preliminary/README.md`  
   SHA `a94dd2914fb538eb59c7abb8f19e2de23799eac7`

6. `00_Authority/NMTC_Preliminary_Scope_and_Source_Policy.md`  
   SHA `2efd1a7985293516cc8b1e9552385520983e0e97`

7. `00_Authority/NMTC_Preliminary_Concept_Dependency_Map.md`  
   SHA `eb1c0ad7ada94275990ac7623f7b02acfed190d1`

## Topic authority

8. `Modular_Divisibility_Digit_Structure/README.md`  
   SHA `8fcef90737cf18bbd0a7888b205ef8105a6f543f`

9. `Modular_Divisibility_Digit_Concept_Book_Spec.md`  
   SHA `19d573abb7f8cc87a574debe4e429d34e901d197`

10. `Modular_Divisibility_Digit_Source_Coverage_Map.md`  
    original Wave-0 read SHA `9befdc9614a94a174623dff12fa12f1410dabed0`; corrected on branch to restore 2018 Q18.

11. `Modular_Divisibility_Digit_Student_Draft_v0.1.md`  
    SHA `0886d541a9c899a8adc52b802aa2f68f1e3d5f20`

12. `04_First_Step_Reference/P0_Number_Theory_First_Step_Cards.md`  
    SHA `6ff33ed4132e3bc375bb2464d29135fc2582cbbe`

13. `09_QA/P0_Number_Theory_Modular_Divisibility_Digit_QA.md`  
    SHA `564ec50be38f31a9f43972a0eb36e56aacade88d`

## Qualified paper ledgers checked for anchor custody

14. `2018_Bhaskara_Preliminary_Qualification_v1.md`  
    SHA `521b007e06a4ca6d4a56999c7f0c500116636786`

15. `2019_Bhaskara_Preliminary_Qualification_v1.md`  
    SHA `ec8396c3936e905621cd7983b0226c4ae1ea0cd8`

16. `2023_Bhaskara_Preliminary_Qualification_v1.md`  
    SHA `269aab0ce2c3bf3e0a8dbf874162662c4263f2c5`

17. `2024_Bhaskara_Preliminary_Qualification_v1.md`  
    SHA `684eb7bcc56ac17157da52accfeae78182a2119c`

18. `2025_Bhaskara_Preliminary_Qualification_v1.md`  
    SHA `835e7f5c45db9cb44b1bf503c8ac92341cae8a17`

## Benchmark

19. `Grade 9/Mathematics/benchmarks/Quadratics_Assimilation_v2/README.md`  
    SHA `889d1187b4e4436319ec89f3f609a4860d5c4b1b`

Benchmark role: pedagogy/production quality only. No wording, exercise, layout or visual composition may be copied.

---

# 2. Scope freeze

Issue #47 is **Bhaskara Preliminary / Grades IX-X** only for curriculum weighting and expected first-move depth.

Core scope:

- division algorithm and congruence meaning;
- safe modular addition/subtraction/multiplication/reduction;
- cancellation/division admissibility;
- residue cycles and exponent indexing;
- same-remainder LCM vs GCD-of-differences;
- simultaneous congruence reconstruction and compatibility;
- place-value algebra;
- divisibility rules reconstructed from powers of 10;
- digit-domain/order restrictions;
- integer-valued/divisor reduction;
- factor-pair parity/coprimality/perfect-power structure;
- prefix residues/state reasoning;
- multiplicative-order / representation ceiling bridges after core mastery;
- source integrity.

Out-of-scope as entry requirements:

- abstract ring/group formalism;
- full Chinese Remainder Theorem proof as a theorem-first chapter;
- Euler/Fermat theorem as automatic machinery when elementary cycles suffice;
- multiplicative order before cycle meaning is secure;
- treating balanced ternary as core prerequisite rather than a ceiling representation bridge.

---

# 3. Qualified evidence inventory

## 3.1 Core clean scored anchors

| ID | Frozen mechanism | Teaching role |
|---|---|---|
| `NMTC-BH-P-2018-Q10` | coprimality -> divisor restrictions | factor/divisor core |
| `NMTC-BH-P-2018-Q18` | difference of squares + same-parity factor pairs | factor-pair core |
| `NMTC-BH-P-2018-Q19` | algebraic reduction + integrality/perfect-square filtering | integrality core |
| `NMTC-BH-P-2018-Q28` | two-digit number + reversal | place-value core |
| `NMTC-BH-P-2018-Q29` | last-digit power cycle | cycle core |
| `NMTC-BH-P-2019-Q01` | repeated block `ABCABC=1001·ABC` | place-value factorization |
| `NMTC-BH-P-2019-Q16` | quotient/remainder/digit encoding | digit algebra |
| `NMTC-BH-P-2019-Q17` | digit sum + algebraic relation | digit constraint |
| `NMTC-BH-P-2019-Q27` | difference of squares + divisibility + bounds | factor/bounds transfer |
| `NMTC-BH-P-2023-Q18` | coprime consecutive product is square | coprime perfect-power core |
| `NMTC-BH-P-2024-Q20` | simultaneous congruence reconstruction | constructive congruence core |
| `NMTC-BH-P-2024-Q21` | same divisor / equal remainders -> GCD differences | flagship contrast half |
| `NMTC-BH-P-2025-Q01` | same number / equal remainder under several divisors -> LCM | flagship contrast half |
| `NMTC-BH-P-2025-Q13` | direct residue squaring modulo 11 | congruence operation core |
| `NMTC-BH-P-2025-Q14` | direct digit place-value equations | digit algebra core |
| `NMTC-BH-P-2025-Q21` | digit-count divisibility modulo 9 | digit residue/counting core |
| `NMTC-BH-P-2025-Q26` | substitution converts integrality to `t|25` | divisor-reduction core |

Core clean count after correction: **17**.

## 3.2 Clean scored ceiling / bridge anchors

These are legitimate scored Preliminary evidence but are **not** entry-level prerequisites.

| ID | Mechanism | Pedagogical disposition |
|---|---|---|
| `NMTC-BH-P-2019-Q06` | equal prefix residues -> divisible consecutive blocks | `CLEAN_SCORED_ANCHOR_CEILING_BRIDGE` |
| `NMTC-BH-P-2019-Q14` | score attainability via congruence restrictions | `CLEAN_SCORED_ANCHOR_TRANSFER_BRIDGE` |
| `NMTC-BH-P-2019-Q26` | prime-divisor filtering via multiplicative order | `CLEAN_SCORED_ANCHOR_CEILING_BRIDGE` |
| `NMTC-BH-P-2019-Q28` | balanced ternary/canonical representation | `CLEAN_SCORED_ANCHOR_CEILING_BRIDGE` |

Total clean scored mechanism IDs: **21**.

Important: “ceiling bridge” is a **teaching-role** label. It does not change the historical scoring disposition.

## 3.3 Source-sensitive blocked evidence

`NMTC-BH-P-2023-Q12`

- qualification state: `SOURCE_TRANSCRIPTION_SUSPECT`;
- recovered solution supports a modulo-4 parity/residue mechanism;
- searchable stem is corrupted;
- allowed use: research/mechanism/source-QC contrast;
- forbidden use: canonical exact student PYQ until original wording is recovered.

For Issue #47 vocabulary this is frozen as:

`SOURCE_SENSITIVE_EVIDENCE — BLOCKED_EXACT_ANCHOR`.

## 3.4 Bonus evidence

No topic-specific bonus item is required for the current evidence architecture.

`BONUS_EVIDENCE_COUNT: 0`

No recurrence or priority is inferred from unrelated bonus items.

## 3.5 Author-created bridge needs

Historical questions do not by themselves provide a sufficient teaching sequence for:

1. illegal modular cancellation and invertibility;
2. compatible vs incompatible non-coprime simultaneous congruences;
3. cycle indexing when exponent residue is zero;
4. distinction between reducing a base and reducing an exponent;
5. derivation of divisibility-by-9/11 before compression;
6. ordered vs unordered digit choices;
7. leading-zero restrictions;
8. digit identity vs residue class (`0` and `9` modulo 9);
9. negative divisor / denominator-zero filtering in integrality problems;
10. ordinary residue cycle vs multiplicative-order ceiling use.

These must be `AUTHOR_CREATED_FOUNDATION` and later `AUTHOR_CREATED_TRANSFER`, never given fake NMTC year/question IDs.

---

# 4. Source-map correction discovered in Wave 0

The legacy topic source coverage map omitted `NMTC-BH-P-2018-Q18` from its factor/divisor list.

Independent authority check:

- qualified 2018 ledger Q18 answer: `4`;
- best first move: difference of squares;
- minimum path: `(k-n)(k+n)=96` with same-parity positive factor pairs;
- disposition: `INDEPENDENT_MATCH`; scored.

Therefore the branch coverage map was corrected to add Q18 explicitly.

This does **not** replace Q19:

- Q18 = difference-of-squares / factor-pair parity;
- Q19 = integrality/perfect-square restriction after algebraic reduction.

`SOURCE_LEDGER_CORRECTION: PASS`

---

# 5. Legacy package audit against the assimilation benchmark

The existing P0 package is mathematically useful and its old QA records a second math/editorial pass. It is **not** automatically the Issue-47 assimilation product because it predates the benchmark's partial-knowledge architecture.

## What is strong and reusable

- division algorithm before congruence notation;
- derivation of addition/multiplication rules;
- flagship LCM-vs-GCD same-remainder contrast;
- place-value derivation of mod-9/mod-11 rules;
- divisor reduction for integrality;
- factor-pair parity and coprime-square structure;
- ceiling labelling for prefix residues and multiplicative order;
- source-sensitive Q12 correctly blocked;
- existing recognition/first-line/mastery inventories can seed later Wave-4 design after re-audit.

## What is insufficient for Issue #47 benchmark parity

### G-01 No explicit partial-knowledge concept map

The legacy spec lists chapter architecture but does not map `PRIOR_KNOWLEDGE -> HALF_KNOWLEDGE -> MISSING_BRIDGE -> INVARIANT -> FIRST MOVE -> TRANSFER` for all streams.

**Wave-0 repair:** new assimilation concept map v2 created before prose.

### G-02 Attempt surfaces leak answers

Legacy student diagnostic places answers immediately below the six questions. The first-move lab also places expected first moves directly beneath the prompts.

**Required later repair:** student H0 attempt must be physically separated from hints/keys.

### G-03 Modular cancellation boundary is missing

The legacy book explains safe addition and multiplication but does not teach why modular division/cancellation can fail, even though Issue #47 explicitly requires it.

**Required bridge:** invertibility / GCD condition, with a minimal counterexample.

### G-04 Simultaneous congruence compatibility is underdeveloped

Legacy reconstruction shows a compatible example but does not create a decision boundary between compatible and incompatible non-coprime conditions.

### G-05 Cycle indexing needs diagnostic emphasis

The legacy First-Step card mentions exponent-zero position, but the main teaching layer does not build a close contrast around the off-by-one trap.

### G-06 Digit-order reasoning is too compressed

Place value is strong, but ordered vs unordered digit choices, leading zero, and residue-class-vs-digit identity need explicit partial-knowledge repair.

### G-07 Fading is not yet benchmark-grade in the student teaching layer

The old package has practice ladders, but Issue #47 requires explicit attempt-before-hint and genuine `H3 -> H2 -> H1 -> H0` choreography connected to diagnosis.

### G-08 Transfer must be reclassified

Existing transfer/mastery counts cannot be promoted merely because they exist. Wave 4 must check that final transfer is structurally disguised, not a number swap, and that the student paper contains no family labels.

### G-09 Production gate is still open

Legacy QA correctly leaves final notation/typography/render and classroom evidence `NOT_RUN`. Issue #47 must not inherit a publication PASS from the old internal package.

---

# 6. Wave-0 concept architecture freeze

Seven Wave-1 streams are retained exactly from Issue #47:

- `W1-A CONGRUENCE_MEANING_AND_OPERATIONS`
- `W1-B POWER_CYCLES_AND_MULTIPLICATIVE_ORDER`
- `W1-C SAME_REMAINDER_STRUCTURE`
- `W1-D SIMULTANEOUS_CONGRUENCES`
- `W1-E PLACE_VALUE_AND_DIGIT_DIVISIBILITY`
- `W1-F FACTOR_PAIR_STRUCTURE`
- `W1-G PREFIX_RESIDUES_AND_STATE_REASONING`

Cross-stream spines that every interface must preserve:

1. `REPRESENTATION_CHOICE`
2. `LEGAL_OPERATION / ADMISSIBILITY`
3. `CORE_VS_CEILING`
4. `ORDER / DIGIT_DOMAIN`
5. `SOURCE_CUSTODY`
6. `FIRST_MOVE_INDEPENDENCE`
7. `NON_IDENTICAL_TRANSFER`

---

# 7. Required Wave-1 interface fields

Each of the seven interfaces must output, at minimum:

1. `CONCEPTS`
2. `PREREQUISITES`
3. `LIKELY_HALF_KNOWLEDGE`
4. `RECOGNITION_CUES`
5. `FIRST_MOVES`
6. `INVARIANTS`
7. `REPRESENTATION_SWITCHES`
8. `LEGALITY / ADMISSIBILITY CONDITIONS`
9. `DECISION_BOUNDARIES`
10. `MISCONCEPTION_TRAPS`
11. `CONTRAST_PAIRS`
12. `TRANSFER_MECHANISMS`
13. `SOURCE_IDS_AND_DISPOSITIONS`
14. `CANDIDATE_MASTERY_ITEMS`
15. `DIAGNOSTIC_TAGS`
16. `H3_TO_H0_FADE_PLAN`

Issue text requested a compact interface; these 16 fields make the benchmark requirements explicit without turning Wave 1 into student prose.

---

# 8. Wave-0 gate table

| Gate | Status | Evidence |
|---|---|---|
| required skills read | PASS | assimilation + Grade 9 math + concept protocol + partial-knowledge map |
| NMTC authority read | PASS | README + source policy + dependency map |
| topic folder read | PASS | README/spec/source map/student draft |
| existing first-step/QA checked | PASS | cards + P0 QA |
| benchmark read | PASS | Quadratics v2 manifest |
| qualified source ledgers checked | PASS | 2018/2019/2023/2024/2025 |
| concept map before new prose | PASS | `Modular_Divisibility_Digit_Assimilation_Concept_Map_v2.md` |
| source classes frozen | PASS | 21 clean scored; 1 source-sensitive blocked; 0 topic bonus |
| source-map discrepancy resolved | PASS | 2018 Q18 restored |
| core-vs-ceiling separation | PASS | Q06/Q14/Q26/Q28 2019 explicitly role-labelled |
| benchmark gap audit | PASS | legacy strengths/gaps recorded |
| classroom timing/readability | NOT_RUN | requires observed learner evidence |
| longitudinal mastery | NOT_RUN | requires later learner evidence |
| publication approval | NOT_READY | Wave 0 only |

`WAVE0_GATE: PASS`

`NEXT_ALLOWED_STATE: WAVE1_SEVEN_STREAM_INTERFACES`

No Wave-2 teaching prose is authorized until all seven Wave-1 interfaces pass their field and source-custody checks.