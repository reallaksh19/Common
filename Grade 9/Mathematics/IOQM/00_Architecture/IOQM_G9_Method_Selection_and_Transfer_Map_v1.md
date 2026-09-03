# IOQM Grade 9 — Method Selection & Transfer Map v1

Status: `DRAFT_PROGRAM_ROUTER`

Purpose: stop the curriculum from becoming a formula catalogue. The learner must learn to choose among methods, not merely recognize isolated chapter labels.

Generic proof-mode selection is governed by `IOQM_G9_Proof_Strategy_Toolkit_v1.md`; named syllabus hardening is governed by `IOQM_G9_Coverage_Hardening_Overlay_v1.md`.

## 1. Universal IOQM problem router

Before calculation, train the learner to ask:

1. **What is actually requested?**
2. **What structure is fixed?**
3. **What representation makes that structure smallest?**
4. **What nearby method is tempting but unnecessary/invalid?**
5. **What domain, parity, sign, integrality or geometric condition must survive?**
6. **What first useful line exposes the mechanism?**
7. **What proof mode fits the logical shape?**
8. **How can the result be checked independently?**

Compressed:

`REQUEST -> STRUCTURE -> REPRESENTATION -> BOUNDARY -> FIRST MOVE -> PROOF MODE -> CONDITIONS -> CHECK`

## 2. Number Theory decision boundaries

| Surface | Decision A | Decision B | Boundary question |
|---|---|---|---|
| prime divides a product | Euclid's Lemma | ordinary divisibility/factor work | Is the divisor actually prime, so divisibility may legally split across factors? |
| repeated remainder | LCM / congruence construction | GCD of differences | Are we constructing numbers satisfying common congruences, or extracting a divisor from differences? |
| huge exponent | short cycle/order | Euler/Fermat compression | Is the base coprime to the modulus, and is a named theorem cheaper than the visible cycle? |
| divisibility equation | factorisation | modular obstruction | Does factorisation make finitely many integer cases, or does a residue eliminate cases faster? |
| perfect square/cube | exponent parity/multiplicity | numerical search | Can prime exponents decide the condition before testing values? |
| integer equation | parity/gcd/divisibility | quadratic/discriminant filter | Which restriction collapses the search space first? |
| digit problem | place value | permutation counting | Is arithmetic structure or arrangement the dominant constraint? |

Number-theory theorem legality:
- Euclid's Lemma requires a **prime** divisor;
- Euler's theorem requires `gcd(a,n)=1`;
- Fermat's little theorem requires prime modulus `p` and `p` not dividing the base;
- a short residue cycle should be preferred when it is more transparent than theorem machinery.

Transfer endpoints:

- modular cycles / bounded Euler-Fermat bridge -> last digits -> digit divisibility -> invariant games;
- Euclid's Lemma -> prime factor structure -> perfect powers -> Diophantine filters;
- prime exponent parity -> perfect powers -> divisor-count parity -> Diophantine filters;
- gcd of differences -> same-remainder problems -> geometric spacing/pigeonhole bridges.

## 3. Algebra decision boundaries

| Surface | Decision A | Decision B | Boundary question |
|---|---|---|---|
| quadratic | solve roots | use root invariants/representation | Are individual roots actually requested? |
| root condition | discriminant | vertex/whole-graph reasoning | Is the target root existence/count or an extremum/sign for all x? |
| symmetric root target | Vieta | explicit roots | Does swapping roots leave the target unchanged? |
| high powers under low-degree relation | reduce/recur | solve then power | Can the governing relation replace the high power directly? |
| max/min | inequality/bound | equation solving | Is this a bound/attainment problem rather than a root problem? |
| radical/exponent equation | normalize structure | square/log mechanically | Which transformations are reversible under the domain? |
| sequence | term relation | sum relation | Is the target a term, a cumulative sum, or a recurrence invariant? |
| floor/ceiling | interval translation | ordinary equation algebra | What half-open interval is encoded? |

Transfer endpoints:

- Vieta -> rectangle dimensions -> geometry root encodings;
- discriminant -> parameter feasibility -> geometry tangency;
- recurrence -> combinatorial state evolution;
- inequality equality case -> integer restriction -> number-theoretic factor cases.

## 4. Geometry decision boundaries

| Surface | Decision A | Decision B | Boundary question |
|---|---|---|---|
| triangle with special segment | Pythagorean/Stewart/Apollonius | coordinates | What segment is present, and which representation cancels most unknowns? |
| angle-heavy circle | cyclic/angle theorem | metric power theorem | Is the target angular or length/product-based? |
| ratio/area | similarity | coordinates | Are ratios already encoded synthetically? |
| tangent | equal tangents/radius perpendicular | power of point | Is the target equality/angle or a metric product? |
| polygon | angle structure | counting/graph model | Is the target geometric measure or combinatorial incidence? |
| messy coordinates | synthetic geometry | coordinate/vector | Does a coordinate placement reduce or increase the number of variables? |

Transfer endpoints:

- cyclicity -> angle constraints -> algebraic parameter conditions;
- similarity -> ratio -> area -> number-theoretic integer-side filter;
- coordinate representation -> algebraic quadratic -> discriminant/inequality bridge.

## 5. Combinatorics decision boundaries

| Surface | Decision A | Decision B | Boundary question |
|---|---|---|---|
| arrangement | permutation/casework | complement/IE | Is the forbidden set easier to count directly or subtract? |
| choose objects | combination | ordered sequence | Does order matter? |
| repeated process | recurrence/state | closed-form counting | Does the next state depend on a small previous-state description? |
| colouring | graph model | direct casework | What are the vertices/adjacencies/constraints? |
| inevitability | pigeonhole | enumeration | Is existence forced before exact counting is needed? |
| game | invariant/monovariant | tree search | Is there a quantity that cannot change or changes one-way? |
| incidence | double counting | direct enumeration | Can the same set of incidences be counted two ways? |

Transfer endpoints:

- graph colouring -> geometric adjacency -> modular colouring invariants;
- recurrence -> tilings -> sequences;
- pigeonhole -> divisibility/residue classes -> geometry spacing;
- invariants -> parity/modular arithmetic -> game impossibility.

## 6. Proof-mode router

After choosing the mathematical method, choose the proof mode separately:

| Logical target | Typical proof mode | Boundary check |
|---|---|---|
| show a consequence from hypotheses | direct implication | did every step preserve legality? |
| transformation chain | equivalence discipline | are any steps only one-way? |
| universal claim seems impossible directly | contradiction / contrapositive | does the negation expose stronger structure? |
| disprove “always” | counterexample | does the example satisfy every hypothesis? |
| finite integer possibilities | exhaustive cases | why is the case list complete? |
| maximum/minimum | bound + equality closure | is equality actually attainable? |
| game/process | invariant / monovariant | is preservation/strict motion proved? |
| existence/impossibility | construction / obstruction | is the constructed object verified, or is the obstruction necessary for all legal objects? |

Retrieve the detailed proof obligations from `IOQM_G9_Proof_Strategy_Toolkit_v1.md` rather than reteaching generic proof theory inside each topic.

## 7. Cross-domain bridge router

A cross-domain bridge is valid only if it reduces the problem rather than creating a second full chapter inside the first.

Examples:

### Geometry -> Algebra

Geometry encodes a quadratic parameter condition.

First question:

> Is the algebra only a representation of the geometry, or is the geometry merely a context for an algebraic mechanism?

Assign one primary mechanism; tag the other as bridge.

### Algebra -> Number Theory

A quadratic has integer roots.

Route:

`REALITY -> SUM/PRODUCT -> INTEGER/FACTOR/PARITY FILTER`

Do not count the same question as full primary recurrence evidence in both domains unless the metadata explicitly supports a multi-primary policy.

### Number Theory -> Combinatorics

Residue classes become boxes or colouring states.

Route:

`RESIDUE REPRESENTATION -> PIGEONHOLE/COLOURING -> FORCED COLLISION`

### Combinatorics -> Algebra

A state count satisfies a recurrence.

Route:

`DEFINE STATE -> FIRST-STEP PARTITION -> RECURRENCE -> ALGEBRAIC/SEQUENCE ANALYSIS`

## 8. Required contrast-pair quota

Every main topic must include at least:

- 5 close decision-boundary contrasts for a narrow topic;
- 8 for a medium topic;
- 10+ for a broad topic.

At least two contrasts must cross microstream boundaries.

A contrast pair is not merely two different examples. It must answer:

> Why should two visually similar problems start differently?

## 9. Transfer quality levels

### T0 — number change only

Not transfer.

### T1 — wording change

Weak transfer.

### T2 — representation change

Acceptable.

### T3 — context/domain change

Strong.

### T4 — cross-domain surface with same invariant

Strong ceiling transfer.

A promoted transfer bank should contain meaningful T2–T4 coverage.

## 10. Mastery router requirement

The final H0 mastery paper must mix methods so the student cannot infer the method from section labels.

Required first-attempt prompts should ask for one or more of:

- visible clue;
- hidden structure;
- first useful line;
- proof mode / theorem-hypothesis check where natural;
- final condition/check.

The paper must also include `WHY NOT` items where a mathematically valid but oversized method is contrasted with the cheapest route, and items where a familiar method is invalid due to domain/condition failure.

## 11. Program-level mixed assessment

When the four domains are later mixed, do not simply interleave chapter questions.

Create deliberate cross-domain decision collisions, e.g.:

- factorisation: algebra identity vs integer divisor cases;
- recurrence: algebraic sequence vs combinatorial state count;
- colouring: geometric region colouring vs graph colouring vs modular invariant;
- quadratic: explicit roots vs integer-root Diophantine filter vs geometry tangency;
- inequality: real optimum vs integer optimum vs geometric feasibility;
- huge modular exponent: visible cycle vs Euler/Fermat theorem with legality check;
- product divisibility: prime Euclid-lemma split vs invalid composite imitation.

The capstone tests **selection**, not memory of folder names.