# IOQM Grade 9 — Main-Topic Production Prompt Pack v1

Status: `READY_FOR_ONE_ISSUE_PER_MAIN_TOPIC`

This file provides the production prompt authority for all 22 main topics. One GitHub issue should be created per main topic. **Do not create child issues for microstreams.**

## Common prompt contract — applies to every topic

Act as a Grade IX/X mathematics teacher, Olympiad-foundation pedagogy designer, question-bank architect and source-custody editor.

Target learner: a Grade-9 student with roughly **50% prior knowledge** — formulas and routine school procedures may be familiar, but conceptual links, representation choice, first moves, boundary conditions and transfer are unstable.

Read before authoring:

1. `Grade 9/skills/ioqm-grade9-main-topic-builder/SKILL.md`
2. `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Core_Architecture_v1.md`
3. `.../IOQM_G9_Topic_Taxonomy_v1.md`
4. `.../IOQM_G9_Knowledge_Dependency_Map_v1.md`
5. `.../IOQM_G9_Method_Selection_and_Transfer_Map_v1.md`
6. `.../IOQM_G9_Source_Provenance_Contract_v1.md`
7. `.../IOQM_G9_Microstream_Interface_Schema_v1.md`
8. `.../IOQM_G9_Production_Gates_v1.md`
9. `Grade 9/Mathematics/IOQM/01_Corpus/IOQM_2023_2025_Source_Coverage_Map_v1.md`
10. `.../IOQM_2023_2025_Taxonomy_Reconciliation_v1.md`
11. `.../IOQM_2023_2025_Corpus_Tagging_QA_v1.md`
12. `.../Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv`
13. `.../Verification/IOQM_2023_2025_Metadata_Correction_Overlay_v1.md`
14. `Grade 9/Mathematics/IOQM/02_Production/IOQM_G9_Main_Topic_Production_Waves_v1.md`
15. `.../IOQM_G9_Canonical_Overlap_Ownership_v1.md`

Historical-paper links are carried by the source ledger. Keep `IOQM-YYYY-QNN` provenance with every cited PYQ. Do not claim official topic weightage from the 90-question seed corpus.

### Required learning architecture

Before prose create three maps:

1. **knowledge dependency map** — prerequisite -> missing bridge -> owned concept;
2. **method-selection map** — visible clue -> structural question -> first move -> near-neighbour boundary;
3. **transfer map** — same invariant under changed surface/representation.

Teaching choreography:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Hint fading:

`H3 execution -> H2 structure -> H1 recognition -> H0 independent`

Performance target:

`RECOGNIZE -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> TRANSFER`

### Parallelism contract

Wave-1 microstreams may run in parallel, but they output **structured interfaces only**: derivations, prerequisites, misconceptions, contrasts, PYQ analysis, candidate first moves, transfer candidates and independent checks. They must **not** publish independent adjacent student chapters.

One topic lead must integrate/reorder/deduplicate/rewrite into one student journey.

### Required student outputs

Produce one coherent topic package:

- Topic Concept Map;
- Integrated Assimilation Book;
- one topic-wide First-Step Reference;
- Recognition Lab;
- First-Line Lab;
- F0→F4 Practice Ladder;
- validated PYQ Anchor Map with year/Q citations;
- Transfer Bank;
- H0 Mixed Mastery Test;
- separate Teacher Diagnostic/Answer Key;
- QA report;
- rendered student PDF and separate teacher material where applicable.

Student export must remove GitHub Issue/PR/Wave/agent-control terminology.

### Hard gates

- no prerequisite inversion;
- borrowed concepts use RETRIEVE/BRIDGE/ROUTE-BACK, not duplicate canonical teaching;
- attempt before hint;
- H3→H0 fading;
- at least one contrast pair per major mechanism;
- at least one changed-surface transfer per major mechanism;
- every promoted historical answer/solution must match the 90-question verification authority;
- exact historical figures/wording remain source-controlled;
- independent math audit before render;
- page-by-page render inspection;
- classroom timing, psychometrics and qualification probability remain `NOT_RUN` unless actually observed.

---

# WAVE 1 TOPICS — may start in parallel

## IOQM-G9-NT-01 — Divisibility, GCD, LCM & Euclidean Structure

**PYQ anchors:** IOQM-2025-Q02, IOQM-2025-Q27.

**Learner likely knows:** divisibility tests, factors/multiples, routine HCF/LCM.

**Missing bridges:** gcd/lcm as structural objects; Euclidean reduction; same-remainder logic; when differences expose a common divisor; why LCM reconstruction differs from gcd-of-differences.

**Parallel microstreams:** divisibility algebra; Euclidean algorithm; gcd/lcm identities; same remainder/differences; divisibility chains; PYQ/source analysis.

**Decision contrasts:** HCF vs LCM; same remainder -> gcd of differences vs constructing common multiple; divisibility test vs prime-exponent reasoning.

**Export downstream:** stable gcd/lcm/divisibility interface for NT-02, NT-03, NT-04 and COMB-04.

## IOQM-G9-ALG-01 — Identities, Transformations & Equation Structure

**PYQ anchors:** IOQM-2025-Q01, IOQM-2025-Q21, IOQM-2024-Q05, IOQM-2024-Q11.

**Learner likely knows:** expand/factor, linear/quadratic solving, basic substitution.

**Missing bridges:** target-led transformation; equivalence vs one-way implication; hidden low-degree relations; when to substitute instead of solve; symmetric compression.

**Parallel microstreams:** factor/expand strategically; substitutions; symmetric identities; reversible transformations; hidden relation/power reduction; source analysis.

**Decision contrasts:** expand vs factor; solve variable vs transform requested expression; identity vs relation true only on solutions.

**Export downstream:** algebra-transformation/equivalence interface for ALG-02/03/05/06 and NT-04.

## IOQM-G9-ALG-04 — Sequences, Progressions & Recurrences

**PYQ anchors:** IOQM-2025-Q26, IOQM-2023-Q10.

**Learner likely knows:** AP/GP formulas and simple sequences.

**Missing bridges:** term vs sum; recurrence as a rule that generates structure; subtracting windows; invariant combinations; high-index cancellation; recurrence transformation.

**Parallel microstreams:** AP/GP recognition; term-vs-sum; recurrence reading; window differences; telescoping; invariant/Cassini-style relations; PYQ/source analysis.

**Decision contrasts:** sequence formula vs recurrence; compute terms vs subtract relations; algebraic recurrence vs counting-state recurrence.

**Export downstream:** recurrence notation interface for COMB-03.

## IOQM-G9-ALG-07 — Floor, Ceiling & Discrete Functions

**PYQ anchors:** IOQM-2024-Q21, IOQM-2024-Q26.

**Learner likely knows:** greatest-integer notation informally.

**Missing bridges:** floor/ceiling as inequalities; half-open endpoints; negative values; integer shifts; case decomposition.

**Parallel microstreams:** definitions/order; endpoint logic; negative inputs; shifts/reflection; equations/inequalities; integer counting; PYQ/source analysis.

**Decision contrasts:** truncation vs floor; real interval vs integer filter; floor equation vs ordinary algebraic equation.

**Export downstream:** discrete-filter interface for NT/COMB bridges.

## IOQM-G9-GEO-02 — Angles, Lines, Quadrilaterals & Polygon Structure

**PYQ anchors:** IOQM-2025-Q13, IOQM-2024-Q04, IOQM-2023-Q06, IOQM-2023-Q24, IOQM-2023-Q25.

**Learner likely knows:** school angle rules and common quadrilaterals.

**Missing bridges:** recognition chains; regular-polygon interior/exterior structure; diagonals; symmetry; deciding synthetic angle chase vs coordinate/vector representation.

**Parallel microstreams:** line/parallel angle chains; quadrilaterals; regular polygons; diagonal structures; symmetry; source/figure analysis.

**Decision contrasts:** local angle chase vs global polygon formula; synthetic vs coordinate route; visual symmetry vs proved symmetry.

**Export downstream:** angle/polygon interface for GEO-04.

## IOQM-G9-GEO-03 — Similarity, Ratio, Area & Centroid Structure

**PYQ anchors:** IOQM-2024-Q12, IOQM-2023-Q05.

**Learner likely knows:** basic similarity and area formulas.

**Missing bridges:** ratio transfer; squared area ratios; centroid as affine/area structure; choosing similarity instead of coordinate brute force.

**Parallel microstreams:** similarity criteria; side/area ratios; centroid; area decomposition; ratio-transfer chains; source/figure analysis.

**Decision contrasts:** equal angles -> similarity vs congruence; side ratio vs area ratio; centroid formula vs area reasoning.

**Export downstream:** similarity/ratio/area interface for GEO-01 and geometry transfer.

## IOQM-G9-GEO-05 — Coordinate, Vector & Mensuration Representations

**PYQ anchors:** IOQM-2025-Q10, IOQM-2025-Q17, IOQM-2024-Q07, IOQM-2023-Q14, IOQM-2023-Q23.

**Learner likely knows:** coordinates, distance, midpoint, elementary mensuration.

**Missing bridges:** coordinates/vectors as representation choice, not default doctrine; coordinate placement to exploit symmetry; geometry-to-integer equations in mensuration.

**Parallel microstreams:** coordinate placement; distances/slopes/midpoints; centroid coordinates; elementary vectors; mensuration constraints; synthetic-vs-coordinate contrasts.

**Decision contrasts:** synthetic vs coordinate; length calculation vs structural coordinate choice; continuous geometry vs integer mensuration restriction.

**Export downstream:** alternate-representation interface for GEO-01/03/04.

## IOQM-G9-COMB-01 — Basic Counting, Restrictions & Inclusion–Exclusion

**PYQ anchors:** IOQM-2025-Q05, Q15, Q18; IOQM-2024-Q02; IOQM-2023-Q07, Q17, Q20.

**Learner likely knows:** factorial, nPr/nCr mechanically.

**Missing bridges:** define the object first; ordered/unordered choice; restrictions; complement; repeated objects; inclusion–exclusion; why formulas emerge from structure.

**Parallel microstreams:** multiplication/addition; permutation/combination derivation; repeated objects; restrictions; complement/IE; digit-string counting; PYQ/source analysis.

**Decision contrasts:** permutation vs combination; direct count vs complement; arithmetic digit constraint (NT-05) vs counting admissible strings.

**Export downstream:** counting/model interface for COMB-02/03.

## IOQM-G9-COMB-05 — Pigeonhole & Extremal Reasoning

**PYQ anchors:** IOQM-2023-Q18, IOQM-2023-Q27.

**Learner likely knows:** informal “some two must…” arguments.

**Missing bridges:** choosing boxes/objects; generalized pigeonhole; extremal object selection; turning local inevitability into contradiction.

**Parallel microstreams:** direct pigeonhole; generalized form; extremal choice; geometric/number-theoretic surfaces; nearest/farthest arguments; source analysis.

**Decision contrasts:** pigeonhole vs inclusion–exclusion; extremal object vs optimization inequality; counting average vs structural inevitability.

---

# WAVE 2 TOPICS — start after named interfaces freeze

## IOQM-G9-NT-02 — Modular Arithmetic, Residues & Power Cycles

**Prerequisite:** NT-01 interface.

**PYQ anchors:** IOQM-2025-Q20, IOQM-2024-Q03, IOQM-2024-Q23.

**Missing bridges:** congruence as equivalence of remainders; legal cancellation/inverses; cycle detection; large powers without expansion.

**Microstreams:** congruence meaning; operations; inverses/cancellation; power cycles; last digits; simultaneous congruences; source analysis.

**Contrasts:** divisibility vs congruence; cycle vs brute-force powers; legal vs illegal cancellation.

## IOQM-G9-NT-03 — Prime Factorisation, Divisors & Perfect Powers

**Prerequisite:** NT-01 interface.

**PYQ anchors:** IOQM-2025-Q06; IOQM-2024-Q01, Q25, Q28, Q29; IOQM-2023-Q01, Q09, Q30.

**Missing bridges:** exponent-vector view; divisor count; squarefree/perfect-power signatures; valuation constraints.

**Microstreams:** FTA/exponents; divisor counting; perfect powers; squarefree; valuation comparisons; factor-pair restrictions; source analysis.

**Contrasts:** factor pairs vs prime-exponent structure; perfect square vs squarefree; divisor parity vs divisor enumeration.

## IOQM-G9-ALG-02 — Inequalities, Bounds & Equality Conditions

**Prerequisite:** ALG-01 interface.

**PYQ anchors:** IOQM-2025-Q07, IOQM-2024-Q06.

**Missing bridges:** boundedness before optimization; direction; equality/attainment; continuous bound vs discrete feasible set.

**Microstreams:** AM-GM; Cauchy/Engel as justified; complete square; feasibility; equality/attainment; integer filtering; source analysis.

**Contrasts:** lower bound vs minimum; real optimum vs integer optimum; discriminant feasibility retrieval from ALG-03 vs inequality method.

## IOQM-G9-ALG-03 — Polynomials, Roots, Vieta & Remainders

**Prerequisite:** ALG-01 interface.

**PYQ anchors:** IOQM-2025-Q16, Q24; IOQM-2024-Q24; IOQM-2023-Q12.

**Canonical ownership:** Vieta, discriminant/root behavior, polynomial remainder/reduction.

**Missing bridges:** target chooses representation; symmetric targets without individual roots; relation as rewriting machine; polynomial modulo low-degree divisor.

**Microstreams:** polynomial representations; Vieta; discriminant; transformed roots; remainder/factor theorem; polynomial reduction; common-root elimination; source analysis.

**Contrasts:** roots vs invariant; repeated root vs minimum; shifted roots vs shifted input; solve roots vs reduce high powers.

## IOQM-G9-ALG-05 — Functional Equations — Strategic Substitution

**Prerequisite:** ALG-01 bridge.

**PYQ anchors:** IOQM-2025-Q14, IOQM-2024-Q16.

**Missing bridges:** choose inputs strategically; domain/codomain only as needed; extract identity from special values.

**Microstreams:** zero/one substitutions; symmetry/involution; add/subtract equations; integer-domain recursion; injectivity only when justified; source analysis.

**Contrasts:** arbitrary substitution vs strategic substitution; function equation vs recurrence; proving a formula vs guessing from values.

## IOQM-G9-ALG-06 — Exponents, Radicals & Logarithms

**Prerequisite:** ALG-01 interface.

**PYQ anchors:** IOQM-2025-Q28, IOQM-2023-Q02.

**Mandatory source note:** 2025-Q28 exact nested radical is controlled by the metadata-correction overlay.

**Missing bridges:** normalize bases; principal-root sign/domain; reversible vs non-reversible squaring; logarithm as exponent.

**Microstreams:** exponent normalization; radicals/conjugates; nested radicals; reversible transformations; logs as exponents; integer/domain filters; source analysis.

**Contrasts:** square both sides vs preserve equivalence; common base vs logarithm; simple difference of radicals vs nested radical structure.

## IOQM-G9-GEO-01 — Triangle Feasibility, Metric Relations & Special Cevians

**Prerequisite:** GEO-03 interface; G9 angle core. GEO-05 is alternate representation.

**PYQ anchors:** IOQM-2025-Q04, Q09; IOQM-2024-Q10, Q15, Q22, Q27, Q30; IOQM-2023-Q13.

**Missing bridges:** classify the segment before selecting formula; triangle inequality as feasibility; right/acute/obtuse metric tests; cevian recognition; integer-side filtering.

**Microstreams:** feasibility; right/acute/obtuse; median/Apollonius; Stewart; angle bisector; radius bridges; integer geometry; source/figure analysis.

**Contrasts:** median vs altitude vs angle bisector; continuous geometry vs integer filtering; synthetic metric vs coordinate route.

## IOQM-G9-GEO-04 — Circles, Cyclicity & Tangency

**Prerequisite:** GEO-02 interface.

**PYQ anchors:** IOQM-2025-Q19, Q23, Q30; IOQM-2024-Q17; IOQM-2023-Q15.

**Missing bridges:** recognition chain before theorem selection; cyclicity triggers; tangent-radius/equal tangents; power of point.

**Microstreams:** angle theorems; cyclic quadrilateral; tangency; alternate segment; power of point; intersecting chords/secants; source/figure analysis.

**Contrasts:** cyclic angle relation vs generic quadrilateral; tangent vs chord; metric coordinate attack vs short synthetic chain.

## IOQM-G9-COMB-02 — Graphs, Colouring & Incidence Counting

**Prerequisite:** COMB-01 interface.

**PYQ anchors:** IOQM-2025-Q08, Q29; IOQM-2024-Q09, Q19; IOQM-2023-Q16, Q22.

**Missing bridges:** translate situation into vertices/edges; degree/incidence double counting; colouring constraints; simple Ramsey inevitability.

**Microstreams:** graph modelling; degree/handshaking; colouring; incidence; grid/knight graphs; Ramsey-style arguments; source analysis.

**Contrasts:** unrestricted assignments vs proper colouring; direct enumeration vs degree sum; graph state vs adversarial game.

## IOQM-G9-COMB-03 — Recurrence, Tilings & State Evolution

**Prerequisites:** COMB-01; ALG-04 bridge.

**PYQ anchors:** IOQM-2024-Q14, Q20; IOQM-2023-Q08, Q21, Q26.

**Missing bridges:** define the state; first-step decomposition; recurrence from combinatorial structure; reverse-state search; tiling recurrence.

**Microstreams:** tilings; path/state counting; deterministic state machines; recurrence derivation; reverse search; representation counting; source analysis.

**Contrasts:** algebraic sequence recurrence vs state-count recurrence; deterministic evolution vs adversarial game; direct count vs recursive decomposition.

---

# WAVE 3 TOPICS — composite/cross-domain

## IOQM-G9-NT-04 — Diophantine Equations & Integer Restrictions

**Prerequisites:** NT-03 + ALG-01; ALG-03 bridge when quadratic feasibility is used.

**PYQ anchors:** IOQM-2025-Q03, Q11; IOQM-2024-Q13; IOQM-2023-Q03, Q04, Q11, Q29.

**Mandatory source note:** 2023-Q04 exact exponent is controlled by the metadata-correction overlay.

**Missing bridges:** factor into finite integer cases; parity/gcd filters; discriminant/perfect-square filters; bounding; reconstruct all admissible solutions.

**Microstreams:** factorisation; gcd/parity; bounding; rational approximation/Farey-style determinant; quadratic/perfect-square filters; finite-case completeness; source analysis.

**Contrasts:** real equation vs integer equation; brute-force search vs structural factorisation; continuous optimum vs discrete factor pairs.

## IOQM-G9-NT-05 — Digits, Place Value & Base Structure

**Prerequisite:** NT-02 for advanced residue/cycle applications.

**PYQ anchors:** IOQM-2025-Q12; IOQM-2024-Q08, Q18; IOQM-2023-Q19.

**Missing bridges:** write number in place-value algebra; carrying; concatenation; digit sum/product constraints; distinguish arithmetic structure from counting strings.

**Microstreams:** decimal place value; divisibility 9/11; concatenation; carries; digit sum/product; base representation; bridge to COMB-01; source analysis.

**Contrasts:** NT-05 arithmetic constraint vs COMB-01 counting; place-value reduction vs modular cycle; digit sum vs digit product.

## IOQM-G9-COMB-04 — Games & Invariants

**Prerequisite/bridge:** F1 proof habits + NT-01/NT-02 parity/residue interface.

**PYQ anchors:** IOQM-2025-Q22, Q25; IOQM-2023-Q28.

**Missing bridges:** identify invariant/monovariant before simulating; adversarial optimal play; reverse-state reasoning; distinguish deterministic state evolution.

**Microstreams:** parity invariants; residue/colour invariants; monovariants; winning/losing states; reverse reasoning; construction/obstruction; source analysis.

**Contrasts:** invariant game vs COMB-03 deterministic state recurrence; simulation vs invariant; existence construction vs impossibility obstruction.

---

# Final integration instruction for every issue

The topic lead must finish with the six-question ownership test for every major mechanism:

1. What did the learner notice?
2. Why does the route work?
3. What clue should trigger it?
4. What similar-looking problem needs a different start?
5. Can the learner write the first two useful lines without help?
6. Can the learner solve a changed-surface version?

A topic cannot be called `PUBLICATION_READY` merely because static source/math/render QA passes. Classroom timing/readability and longitudinal evidence remain separate gates.