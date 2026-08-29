# Issue #49 — Wave 1 Integration Readiness Matrix

`WAVE: 1 — SEVEN STREAM INTERFACES`

`STATUS: PASS_INTERNAL`

No Wave-2 student teaching prose is authorized unless this matrix remains PASS.

---

# 1. Seven-stream schema audit

Every stream contains the frozen 16-field interface contract from Wave 0.

| Stream | Scope | 16/16 fields | Candidate items | Internal result |
|---|---|---:|---:|---|
| W1-A | term vs sum / object identity | PASS | 5 | PASS |
| W1-B | AP/GP first moves / finite-infinite boundary | PASS | 5 | PASS |
| W1-C | high-index cancellation | PASS | 5 | PASS |
| W1-D | weighted/nested sums | PASS | 5 | PASS |
| W1-E | recurrence transformation | PASS | 5 | PASS |
| W1-F | reverse from sum / telescoping | PASS | 5 | PASS |
| W1-G | finite differences / source QC | PASS | 5 | PASS |

`SCHEMA_GATE: 7/7 x 16/16 — PASS`

---

# 2. Cross-stream ownership matrix

| Boundary | Owner / handoff rule | Result |
|---|---|---|
| A ↔ B | A labels the target object first; B classifies AP/GP only after target identity is clear | PASS |
| A ↔ F | A owns object identity; F owns execution of `a_n=S_n-S_{n-1}` and block endpoint custody | PASS |
| B ↔ C | B establishes GP/ratio; C owns selected-term index-gap cancellation | PASS |
| B ↔ E | B owns ordinary AP/GP invariants; E owns transformation that exposes an AP/GP in a new variable | PASS |
| B ↔ G | B rejects AP/GP when invariants fail; G then owns finite-difference degree signals | PASS |
| C ↔ D | C compares selected GP terms; D owns weighted sums such as `k r^(k-1)` | PASS |
| D ↔ F | D owns summand/multiplicity reduction; F owns adjacent cancellation once a telescope representation is exposed | PASS |
| E ↔ F | E chooses reciprocal/shift/etc.; F owns telescope cancellation and boundary survivors after transformation | PASS |
| E ↔ G | E may discover a closed form; G-style verification discipline prevents a guessed form being treated as self-proving | PASS |
| G ↔ all | G/source-QC can block historical canonical use regardless of familiar mathematical mechanism | PASS |

`OWNERSHIP_OVERLAP_GATE: PASS`

---

# 3. Decision-boundary coverage

Required Issue-49 close contrasts are explicitly represented:

1. `a_n` vs `S_n` — W1-A;
2. AP vs GP — W1-B;
3. finite vs infinite GP — W1-B;
4. direct nth term vs reverse from `S_n` — W1-A/F;
5. high-index expansion vs ratio cancellation — W1-C;
6. polynomial weighted term vs AP/GP reflex — W1-D;
7. recurrence iteration vs recurrence transformation — W1-E;
8. recurrence discovery vs closed-form verification — W1-E/G;
9. ordinary summation vs telescoping — W1-F;
10. telescope recognition vs endpoint correctness — W1-F;
11. constant second difference vs AP — W1-G;
12. primary Sequence evidence vs incidental GP appearance — W1-G;
13. source conflict vs silent repair — W1-G.

`DECISION_BOUNDARY_GATE: 13 explicit boundaries — PASS_STRONG`

---

# 4. Candidate mastery independent audit — 35/35

All 35 candidates were recomputed independently from their authored explanations before this gate.

## W1-A — 5/5

- `a_20=62` for `a=5,d=3`;
- `S_20=670` for the same AP;
- from `S_n=2n^2+3n`, `a_n=4n+1`;
- `S_40-S_14=715` for `S_n=n(n+1)/2`;
- AP `a_7=20,a_15=44` gives `d=3,a=2,S_20=610`.

## W1-B — 5/5

- `7,11,15,19` -> AP `d=4`;
- `3,6,12,24` -> GP `r=2`;
- infinite GP `2,-1,1/2,-1/4,...` -> `r=-1/2`, converges, `S=4/3`;
- finite GP `a=3,r=2,n=6` -> `189`, with no convergence condition needed;
- `2,2sqrt(2),4,4sqrt(2),...` -> GP `r=sqrt(2)`; infinite extension would diverge.

## W1-C — 5/5

- `a_3=12,a_6=96` -> `r^3=8`, so `a_20/a_17=8`;
- `a_5=48,a_8=384` -> `r=2`, so `a_30/a_26=16`;
- `a_25/a_22=27` -> `r=3`, so `a_40/a_38=9`;
- `a_100/a_97=-8` -> real `r=-2`, so `a_60/a_58=4`;
- `a_4=54,a_7=1458` -> `r^3=27`, so `a_50/a_47=27`.

## W1-D — 5/5

- `sum_{1..10} k(2k+1)=825`;
- `sum_{1..20}(k^2-k)=2660`;
- nested `sum_{k=1}^{10} sum_{j=1}^k 1=55`;
- `sum_{1..10} k(k+1)=440`;
- `1+2·2+3·2^2+4·2^3+5·2^4=129`.

## W1-E — 5/5

- reciprocal recurrence gives `a_20=1/20`;
- `a_{n+1}=2a_n+3,a_1=1` gives `a_10=2045`;
- functional recurrence `a_{m+n}=a_m+a_n+2mn,a_1=1` gives `a_2=4,a_4=16,a_8=64`;
- `a_{n+1}=3a_n-4,a_1=5` gives `a_6=731` after shifting by fixed point 2;
- `a_n=2^n-1` satisfies the stated recurrence and initial condition; substitution is verification, not discovery.

## W1-F — 5/5

- `S_n=3n^2+2n` -> `a_n=6n-1`;
- triangular partial sums give block 11..25 = `270`;
- `sum_{1..20}1/[k(k+1)]=20/21`;
- radical telescope through k=24 gives `sqrt(25)-sqrt(1)=4`;
- odd-factor telescope through k=10 gives `10/21`.

## W1-G — 5/5

- `2,6,12,20,30,...` -> constant second difference 2, verified `a_n=n(n+1)`, `a_15=240`;
- `1,8,27,64,...` -> cubic rule verified, `a_8=512`;
- `3,8,15,24,35,...` -> verified `a_n=n^2+2n`, `a_10=120`;
- source stem/key mathematical conflict -> block canonical use, never repair silently;
- geometric circle-radii sequence -> geometry-primary `BRIDGE_EVIDENCE`, no Sequence-frequency credit.

`CANDIDATE_MASTERY_AUDIT: 35/35 PASS`

---

# 5. Source-custody integration

## CLEAN_SCORED_ANCHOR — 6

- `NMTC-BH-P-2019-Q29` — W1-E;
- `NMTC-BH-P-2023-Q15` — W1-D;
- `NMTC-BH-P-2023-Q29` — W1-C;
- `NMTC-BH-P-2024-Q10` — W1-D;
- `NMTC-BH-P-2024-Q11` — W1-E with W1-F bridge, counted once;
- `NMTC-BH-P-2024-Q27` — W1-B.

## Supporting, not clean-major anchors

- `NMTC-BH-P-2018-Q17` — scored foundation reconnect only;
- `NMTC-BH-P-2024-Q13` — geometry-primary bridge, no Sequence-frequency credit.

## Blocked

- `NMTC-BH-P-2025-Q30` — `SOURCE_CONFLICT_EVIDENCE / SOURCE_KEY_CONFLICT_NOT_CANONICAL`.

`SOURCE_DOUBLE_COUNT_GUARD: PASS`

`SOURCE_CONFLICT_FREEZE: PASS`

---

# 6. Wave-2 integration requirements derived from interfaces

The Assimilation Book must be one connected unit, not seven pasted mini-chapters. It must repeatedly force this order:

`TARGET OBJECT -> STABLE STRUCTURE -> REPRESENTATION SWITCH -> COLLAPSE -> INDEX/ENDPOINT/CONVERGENCE CHECK -> ORIGINAL OBJECT/SOURCE CHECK`

Mandatory integrated error lab must include at least:

- `TERM_SUM_CONFUSION`;
- `INDEX_SHIFT_OFF_BY_ONE`;
- `AP_GP_SURFACE_CLASSIFICATION`;
- `CONVERGENCE_OMITTED`;
- `GP_HIGH_POWER_EXPANDED`;
- `WEIGHTED_SUM_NOT_SPLIT`;
- `WRONG_TRANSFORM_CHOICE`;
- `DISCOVERY_VERIFICATION_CONFUSION`;
- `TELESCOPING_ENDPOINT_ERROR`;
- `DEGREE_HYPOTHESIS_UNVERIFIED`;
- `SOURCE_SILENT_REPAIR`;
- `PRIMARY_DOMAIN_INFLATION`.

At least seven close contrast pairs are required; Wave 1 supplies thirteen candidate boundaries.

---

# 7. Wave-1 gate

| Gate | Result |
|---|---|
| seven stream interfaces exist | PASS |
| 16/16 schema fields in every interface | PASS |
| prerequisites / half-knowledge explicit | PASS |
| first moves explicit | PASS |
| conditions/index/endpoints explicit | PASS |
| decision boundaries explicit | PASS_STRONG |
| misconception traps explicit | PASS |
| source custody explicit | PASS |
| candidate mastery items | 35 |
| independent candidate audit | 35/35 PASS |
| H3->H0 plan in every stream | 7/7 PASS |
| cross-stream ownership conflicts resolved | PASS |
| source double counting prevented | PASS |
| 2025 Q30 conflict preserved | PASS |
| Wave-2 prose started | NO — correctly not started |

`WAVE1_GATE: PASS`

`NEXT_ALLOWED_STATE: WAVE2_INTEGRATED_ASSIMILATION_BOOK`