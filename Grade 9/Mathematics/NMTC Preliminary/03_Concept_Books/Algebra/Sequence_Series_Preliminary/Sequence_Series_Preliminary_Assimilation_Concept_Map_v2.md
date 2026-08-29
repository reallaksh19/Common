# Sequence & Series Preliminary Overlay — Assimilation Concept Map v2

`ISSUE_AUTHORITY: #49`

`WAVE: 0 — CONCEPT_MAP_FIRST`

`STATUS: DRAFT_CONCEPT_MAP`

Target learner: Grade IX/X learner who already remembers AP/GP formulas and basic sequence vocabulary, but whose **object choice, representation choice, index control, transformation choice and transfer** are unstable.

Authority split:

- **deep pedagogy authority:** `Grade 9/Mathematics/Sequence and Series/`;
- **NMTC Preliminary grounding/performance authority:** this overlay folder plus the qualified Preliminary corpus;
- the overlay must not flatten the deep chapter into a formula sheet, and the deep chapter must not absorb Preliminary frequency/timing assumptions.

---

# 1. Governing map

```text
VISIBLE LIST / FORMULA / SUM / RECURRENCE / WORDING
        |
        v
WHAT OBJECT IS THE TARGET?
        |
        +--> one term a_n
        +--> partial sum S_n
        +--> block / weighted / nested sum
        +--> recurrence state
        +--> infinite accumulation
        |
        v
WHICH STRUCTURE IS STABLE?
        |
        +--> POSITION      index / nth term / recurrence
        +--> CHANGE        first or higher differences
        +--> RATIO         multiplicative scaling
        +--> ACCUMULATION  S_n / sigma / weighted sums
        +--> TRANSFORM     reciprocal / shift / ratio / split / telescope
        +--> REVERSE       a_n = S_n - S_{n-1}
        |
        v
NORMALIZE BEFORE FORMULA USE
        |
        +--> compare neighboring terms
        +--> compare selected high-index terms
        +--> expose kth term inside a sum
        +--> change recurrence variable
        +--> expand only enough to split standard sums
        +--> expose neighboring cancellation
        |
        v
CHECK CONDITIONS / ENDPOINTS
        |
        +--> n versus n-1 index
        +--> number of terms
        +--> first/last surviving telescope term
        +--> |r| < 1 for infinite GP
        +--> initial condition for recurrence
        +--> source wording/key consistency
        |
        v
SOLVE / COLLAPSE / RECONSTRUCT
        |
        v
CHECK ORIGINAL OBJECT AND SOURCE
```

Cognitive contract:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Assimilation choreography:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Preliminary performance loop:

`RECOGNIZE -> WRITE THE RIGHT OBJECT -> TRANSFORM -> COLLAPSE -> CHECK -> TRANSFER`

---

# 2. PRIOR_KNOWLEDGE — likely already owned

`PK-01` A sequence is an ordered list; a series is an accumulation of terms.

`PK-02` AP vocabulary: first term `a`, common difference `d`, nth-term formula.

`PK-03` GP vocabulary: first term `a`, common ratio `r`, nth-term formula.

`PK-04` Familiar finite AP/GP sum formulas, at least procedurally.

`PK-05` Basic algebraic manipulation and substitution.

`PK-06` Recognition that some sequences grow additively and some multiplicatively.

`PK-07` Basic sigma notation may be familiar, though bounds/counter meaning may be weak.

`PK-08` Simple recurrence iteration, such as Fibonacci-type generation.

`PK-09` Difference of successive terms and ratio of successive nonzero terms.

These are reconnect nodes, not reasons to start the book with a formula sheet.

---

# 3. LIKELY_HALF_KNOWLEDGE — remembered but unstable

`HK-01` Knows both `a_n` and `S_n` formulas but may apply the sum formula to a term question or vice versa.

`HK-02` Remembers `a+(n-1)d` and `ar^(n-1)` but cannot explain the `n-1` index shift reliably.

`HK-03` Calls any regularly growing list an AP/GP before checking difference or ratio.

`HK-04` Recognizes GP but expands high powers separately instead of cancelling common powers by term ratios.

`HK-05` Uses finite- and infinite-GP formulas interchangeably and may omit `|r|<1`.

`HK-06` Sees an indexed polynomial term and tries AP/GP formulas instead of treating the problem as a weighted polynomial sum.

`HK-07` Iterates a recurrence many times even when a reciprocal/shift/difference makes it linear.

`HK-08` For `a_{m+n}`-type recurrences, tries to derive a full closed form even when strategic indices reach the target directly.

`HK-09` Given `S_n`, guesses terms from sample values instead of reversing cumulative information.

`HK-10` Understands telescoping after seeing the decomposition but does not recognize neighboring-factor/radical cues independently.

`HK-11` Cancels telescope terms mentally and loses one endpoint.

`HK-12` Recognizes first differences but does not use second differences to distinguish quadratic behavior from AP.

`HK-13` Treats proving a guessed closed form by induction as the same task as discovering the form.

`HK-14` Trusts a familiar GP interpretation even when historical wording and the supplied key conflict.

---

# 4. MISSING_BRIDGES — repair targets

`B-01 OBJECT_IDENTITY`  
Before selecting a formula, label the target explicitly as `a_n`, `S_n`, a block sum, transformed sum, or recurrence state.

`B-02 INDEX_MEANING`  
The exponent/count `n-1` records the number of changes from term 1 to term `n`; term counts and endpoint indices must be reconstructed, not memorized blindly.

`B-03 CHANGE_VS_RATIO`  
AP and GP are invariant tests: constant first difference versus constant adjacent ratio after sensible normalization.

`B-04 FINITE_VS_INFINITE_GP`  
Finite GP is algebraic cancellation with a residual term; infinite GP requires the residual to vanish, hence a convergence condition such as `|r|<1`.

`B-05 HIGH_INDEX_CANCELLATION`  
For comparable GP terms, divide before solving huge powers: `a_p/a_q=r^(p-q)`.

`B-06 WEIGHTED_SUM_TO_STANDARD_ACCUMULATION`  
Make the kth term visible, expand structurally, split by summation linearity, and use only the standard sums actually needed.

`B-07 RECURRENCE_VARIABLE_CHANGE`  
A recurrence that is nonlinear in `a_n` may be linear/additive/multiplicative in `1/a_n`, `a_n-c`, a difference, ratio, or partial-sum variable.

`B-08 STRATEGIC_INDEX_SELECTION`  
A functional recurrence is an index-navigation problem before it is a closed-form problem.

`B-09 REVERSE_CUMULATIVE_INFORMATION`  
Local term from cumulative sum: `a_n=S_n-S_{n-1}`; block sums similarly arise from differences of partial sums.

`B-10 TELESCOPING_AS_ENDPOINT_CUSTODY`  
The purpose of partial fractions/rationalization is not merely simplification; it creates neighboring cancellation, so surviving endpoints must be written explicitly.

`B-11 FINITE_DIFFERENCE_DEGREE_SIGNAL`  
Constant first differences suggest linear/AP behavior; constant second differences suggest quadratic behavior; the degree hypothesis still requires verification.

`B-12 DISCOVERY_VS_VERIFICATION`  
A recurrence closed form may be discovered by transformation/pattern and then verified by substitution/induction; verification does not explain how it was found.

`B-13 PRIMARY_MECHANISM_VS_INCIDENTAL_SEQUENCE`  
A problem containing a geometric pattern is not automatically a Sequence & Series anchor. Primary-domain custody matters.

`B-14 SOURCE_CUSTODY`  
A familiar sequence mechanism never authorizes silently editing a historical term comparison to match a key.

---

# 5. CORE INVARIANTS / STRUCTURES

`I-01 TERM_SUM_DIFFERENCE`  
`a_n=S_n-S_{n-1}` for `n>=2`, with `a_1=S_1`.

`I-02 AP_DIFFERENCE`  
`a_{n+1}-a_n=d`; indexed gaps obey `a_p-a_q=(p-q)d`.

`I-03 GP_RATIO`  
For nonzero relevant terms, `a_{n+1}/a_n=r`; selected-term ratios obey `a_p/a_q=r^(p-q)`.

`I-04 INDEX_DISTANCE`  
Moving from index 1 to index `n` applies the repeated change/ratio exactly `n-1` times.

`I-05 FINITE_GP_SHIFT_SUBTRACT`  
Multiplying a finite GP sum by `r` and subtracting aligns almost all terms and exposes endpoint cancellation.

`I-06 INFINITE_GP_CONVERGENCE`  
The infinite formula is valid only when the residual tail tends to zero; for real GP this requires `|r|<1`.

`I-07 SUM_LINEARITY`  
`Σ(αu_k+βv_k)=αΣu_k+βΣv_k`; weighted polynomial terms can therefore be reduced after structural expansion.

`I-08 RECIPROCAL_LINEARIZATION`  
A fractional recurrence can become an additive recurrence under `b_n=1/a_n` when reciprocals convert the update to a difference.

`I-09 FIXED_POINT_SHIFT`  
For affine recurrence `a_{n+1}=pa_n+q`, shifting by a fixed point can remove the constant term and expose a GP.

`I-10 STRATEGIC_FUNCTIONAL_RECURRENCE`  
For `a_{m+n}` rules, choose pairs `(m,n)` that approach the requested index efficiently; a general formula is optional unless the target demands it.

`I-11 TELESCOPING_DIFFERENCE`  
If `u_k=v_k-v_{k+1}`, then `Σu_k` collapses to boundary terms.

`I-12 FINITE_DIFFERENCE_POLYNOMIAL_SIGNAL`  
A polynomial sequence of degree `d` has constant `d`th finite differences; the converse can guide a low-degree hypothesis on equally spaced integer indices.

`I-13 BLOCK_SUM_AS_PARTIAL_SUM_DIFFERENCE`  
`a_p+...+a_q=S_q-S_{p-1}`.

`I-14 SOURCE_DOMAIN_CUSTODY`  
Cross-domain sequence appearance may be useful bridge evidence without becoming primary sequence recurrence evidence.

`I-15 SOURCE_CONFLICT_FREEZE`  
When printed wording and a key imply different mathematics, preserve both and block canonical use until resolved.

---

# 6. REPRESENTATION NETWORK

```text
QUESTION WORDING
      |
      +--> “nth term” ------------------> TARGET = a_n
      |
      +--> “sum of first n” -----------> TARGET = S_n
      |
      +--> “sum from p to q” ----------> S_q - S_{p-1}
```

```text
VISIBLE TERMS
      |
      +--> differences constant -------> AP / CHANGE
      |
      +--> ratios constant ------------> GP / RATIO
      |
      +--> neither --------------------> normalize / finite differences / transform
```

```text
HIGH-INDEX GP
      |
      v
write comparable term relations
      |
      v
divide / cancel common powers
      |
      v
small exponent gap p-q
```

```text
WEIGHTED / NESTED SUM
      |
      v
make kth term explicit
      |
      v
expand only enough
      |
      v
split sigma / count multiplicity
      |
      v
standard sums / reduced accumulation
```

```text
RECURRENCE
      |
      +--> fraction-like ------> reciprocal
      +--> affine -------------> fixed-point shift
      +--> multiplicative -----> ratio/log where justified
      +--> a_{m+n} ------------> strategic indices
      +--> partial-sum form ---> reverse/difference
```

```text
TELESCOPING CANDIDATE
      |
      +--> neighboring factors -> partial fractions
      +--> conjugate radicals --> rationalize
      +--> reciprocal recurrence -> transformed adjacent difference
      |
      v
write first few expanded terms
      |
      v
preserve first/last survivors
```

---

# 7. SEVEN ISSUE-49 STREAM PATHS

| Stream | PRIOR -> BRIDGE | Primary invariant / representation | Automatic first move | Transfer endpoint |
|---|---|---|---|---|
| W1-A Term vs sum | formula memory -> object identity -> reverse accumulation | `a_n`, `S_n`, `a_n=S_n-S_{n-1}` | write `TARGET = ...` before formula selection | same surface sequence, changed target object |
| W1-B AP / GP first moves | familiar formulas -> invariant test | first difference vs ratio; finite/infinite GP | mark `d` or `r`; for infinite write convergence condition first | disguised normalized sequence where appearance misleads |
| W1-C High-index cancellation | GP recognition -> index-distance compression | `a_p/a_q=r^(p-q)` | divide comparable term equations before solving `a,r` | far-apart selected terms with no need for huge powers |
| W1-D Weighted sums | sigma familiarity -> expose kth term | sum linearity; polynomial standard sums; multiplicity counts | write/expand `T_k` before summing | nested or weighted accumulation with changed surface |
| W1-E Recurrence transformation | recurrence iteration -> change variable | reciprocal / shift / difference / ratio | test the transformation suggested by the algebraic shape | nonlinear recurrence becoming AP/GP after transform |
| W1-F Reverse / telescoping | partial sums + fractions -> neighboring cancellation | `S_q-S_{p-1}`; `v_k-v_{k+1}` | reverse cumulative info or expose adjacent difference | radical/rational telescope with endpoint trap |
| W1-G Finite differences + source QC | pattern spotting -> degree signal + evidence discipline | higher differences; primary-domain/source disposition | build difference table; independently solve printed source before trusting key | polynomial-looking sequence + conflicted historical GP comparison |

---

# 8. DECISION BOUNDARIES / CLOSE CONTRASTS

`DB-01 a_n vs S_n`  
“20th term” and “sum of first 20 terms” may describe the same AP but require different objects and formulas.

`DB-02 AP vs GP`  
Constant additive change is not constant multiplicative change. A rapidly growing AP is still an AP; a slowly changing GP is still a GP.

`DB-03 finite GP vs infinite GP`  
Finite sum needs no convergence condition; infinite sum requires `|r|<1` before `a/(1-r)`.

`DB-04 direct nth term vs reverse from S_n`  
If `S_n` is supplied, do not infer/fit `a_n` when one subtraction gives it exactly.

`DB-05 high-index expansion vs ratio cancellation`  
Separate evaluation of `a_40` and `a_35` preserves useless powers; division exposes only `r^5`.

`DB-06 polynomial term vs AP/GP reflex`  
A sequence with `T_k=k(3k+1)` is an accumulation problem after expansion, not an AP/GP classification exercise.

`DB-07 recurrence iteration vs recurrence transform`  
Twenty iterations may be valid but structurally inferior when reciprocal/shift converts the recurrence immediately.

`DB-08 discovery vs verification`  
Substituting a proposed closed form proves consistency; it does not explain how the form was discovered.

`DB-09 strategic indices vs universal closed form`  
For functional recurrence and one requested index, a doubling path can be superior to deriving `a_n` for all `n`.

`DB-10 telescoping candidate vs ordinary summation`  
Neighboring factors/conjugates signal transformation before common-denominator arithmetic.

`DB-11 telescope cancellation vs endpoint correctness`  
Recognizing cancellation is insufficient if the first or last survivor is lost.

`DB-12 constant second difference vs AP`  
Constant second difference indicates quadratic-type behavior, not AP; AP requires constant first difference.

`DB-13 sequence-primary vs incidental geometric scaling`  
`NMTC-BH-P-2024-Q13` contains a GP in circle radii but remains geometry-primary.

`DB-14 source conflict vs “obvious correction”`  
`NMTC-BH-P-2025-Q30` must not be rewritten from “third” to “second” merely because that makes the provisional key work.

---

# 9. MISCONCEPTION / ERROR NODES

- `E-01 TERM_SUM_CONFUSION`
- `E-02 INDEX_SHIFT_OFF_BY_ONE`
- `E-03 TERM_COUNT_ENDPOINT_ERROR`
- `E-04 AP_GP_SURFACE_CLASSIFICATION`
- `E-05 GP_HIGH_POWER_EXPANDED`
- `E-06 INFINITE_GP_CONVERGENCE_OMITTED`
- `E-07 WEIGHTED_SUM_FORCED_TO_AP_GP`
- `E-08 SIGMA_BOUND_GENERATION_ERROR`
- `E-09 RECURRENCE_BRUTE_ITERATION`
- `E-10 CLOSED_FORM_DISCOVERY_VERIFICATION_CONFUSION`
- `E-11 REVERSE_FROM_SUM_MISSED`
- `E-12 TELESCOPING_DECOMPOSITION_MISSED`
- `E-13 TELESCOPING_ENDPOINT_ERROR`
- `E-14 FINITE_DIFFERENCE_DEGREE_ERROR`
- `E-15 INCIDENTAL_SEQUENCE_FREQUENCY_INFLATION`
- `E-16 SOURCE_CONFLICT_SILENT_REPAIR`

---

# 10. FIRST-MOVE ATLAS

| Visible clue | First move |
|---|---|
| nth term requested | write `TARGET=a_n` |
| sum requested | write `TARGET=S_n` or relevant partial-sum difference |
| equal additive changes | compute/mark first difference `d` |
| equal multiplicative changes | compute/mark ratio `r` |
| high selected GP indices | divide term relations; use index gap |
| infinite geometric accumulation | write `|r|<1` before infinite-sum formula |
| kth term polynomial in k | expand `T_k`; split sigma |
| nested sum | count how many times each inner term occurs / simplify inner sum first |
| fractional recurrence | test reciprocal variable |
| affine recurrence | test fixed-point shift |
| `a_{m+n}` functional rule | choose strategic index pairs |
| `S_n` given, `a_n` requested | `a_n=S_n-S_{n-1}` |
| neighboring linear factors | partial fractions |
| conjugate radicals | rationalize |
| neither AP nor GP, polynomial-looking | finite-difference table |
| historical wording/key disagreement | independently solve printed mathematics; freeze conflict |

---

# 11. TRANSFER ENDPOINTS

`T-01` Same AP data, but switch target from a term to a block sum so object selection—not formula recall—governs the start.

`T-02` A sequence hidden behind transformed variables where differences become constant only after normalization.

`T-03` A high-index GP comparison in which `a` is intentionally irrelevant and all large powers cancel.

`T-04` A nested/weighted sum whose inner multiplicity count is the main move rather than direct power-sum substitution.

`T-05` A nonlinear recurrence that becomes AP after reciprocation, then a nearby recurrence where reciprocation does **not** help and a shift does.

`T-06` A closed form supplied for verification versus a recurrence supplied for discovery; learner must distinguish the jobs.

`T-07` A telescoping radical sum where the surface is geometric/measurement language rather than a textbook sigma expression.

`T-08` A partial-sum formula used to recover an isolated term and then a block sum.

`T-09` A quadratic finite-difference sequence with a misleading near-GP growth pattern.

`T-10` A historical source-QC task requiring the learner to reject an attractive “correction” of the source.

JEE B1–B18 in the deep bridge map may inform later transfer design, but remain external bridge material and must stay provenance-distinct from NMTC PYQs and the uploaded deep source.

---

# 12. SOURCE CUSTODY

## Clean scored Preliminary anchors — 6

- `NMTC-BH-P-2019-Q29` — functional recurrence / strategic indices;
- `NMTC-BH-P-2023-Q15` — weighted polynomial accumulation;
- `NMTC-BH-P-2023-Q29` — selected/high-index GP cancellation;
- `NMTC-BH-P-2024-Q10` — weighted-square/polynomial accumulation;
- `NMTC-BH-P-2024-Q11` — recurrence reciprocal/telescoping transform;
- `NMTC-BH-P-2024-Q27` — infinite GP with convergence and coupled constraints.

## Supporting scored evidence — do not inflate recurrence

- `NMTC-BH-P-2018-Q17` — five consecutive integers / average symmetry; foundation-only POSITION/CHANGE support, not a major sequence anchor.
- `NMTC-BH-P-2024-Q13` — geometric scaling of circle radii; `BRIDGE_EVIDENCE`, geometry-primary, not Sequence-frequency evidence.

## Blocked source-conflict evidence

- `NMTC-BH-P-2025-Q30` — printed term comparison and AMTI provisional key disagree; `SOURCE_CONFLICT_EVIDENCE / SOURCE_KEY_CONFLICT_NOT_CANONICAL`.

Permitted use: source-integrity contrast and independent-math checking.

Forbidden use: exact clean GP anchor, official solved exercise, or recurrence-frequency promotion.

## Deep-source authority

`Grade 9/Mathematics/Sequence and Series/` is the primary conceptual source for POSITION / CHANGE / RATIO / ACCUMULATION / TRANSFORM / REVERSE, including the uploaded 23-page source and mapped extensions.

Do not convert JEE bridge items or author-created transfer items into NMTC historical evidence.

---

# 13. WAVE-1 INTERFACE CONTRACT FROZEN BY WAVE 0

Every W1-A...W1-G interface must contain at least:

1. concepts/scope;
2. prerequisites;
3. likely half-knowledge;
4. recognition cues;
5. automatic first moves;
6. invariant/structure;
7. representation switches;
8. condition/index/endpoint checks;
9. decision boundaries;
10. misconception traps;
11. contrast pair(s);
12. transfer mechanism;
13. source IDs/dispositions;
14. candidate mastery items;
15. diagnostic tags;
16. H3 -> H2 -> H1 -> H0 fade plan.

No Wave-2 teaching prose is authorized until all seven interfaces satisfy the contract and their candidate mathematics is independently checked.

`WAVE0_CONCEPT_MAP_GATE: PASS_INTERNAL`
