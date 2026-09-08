---
name: grade9-math-corpus-coverage-auditor
version: 1
description: Mathematics-specific extension of grade9-corpus-coverage-auditor. Audits external math question banks against subtopic study guides and practice books, with mathematical ownership, solution verification, representation quality, misconception tagging, helper depth, notation, difficulty, and mixed-problem transfer checks. Suitable for ExamSIDE/JEE-style corpora and other mathematics sources.
extends: grade9-corpus-coverage-auditor
---

# Grade 9 Mathematics Corpus Coverage Auditor v1

## Use with the general auditor
Run this skill **after or together with** `grade9-corpus-coverage-auditor`.

The general skill proves source-row coverage and artifact traceability. This mathematics extension adds the checks that matter specifically in mathematics:

```text
QUESTION STRUCTURE -> PRIMARY MATHEMATICAL ENGINE
PRIMARY ENGINE -> SUBTOPIC OWNER
SUBTOPIC OWNER -> REPRESENTATION / CONCEPT SUPPORT
SUPPORT -> SOLUTION METHOD
SOLUTION METHOD -> VERIFIED ANSWER
ANSWER -> STUDENT-READABLE MATHEMATICAL PUBLICATION
```

A math question is not covered merely because it appears in a practice PDF. It must be assigned to the right mathematical engine, supported by the right representation, and solved correctly under all stated constraints.

---

# 1. Mathematics question fingerprint
For every eligible source row, record a **structure fingerprint** rather than only a prose summary.

Required fields:

```yaml
source_id:
mathematical_object:
target_quantity_or_claim:
constraint_signature:
primary_engine:
secondary_engines:
representation_trigger:
answer_type:
source_difficulty:
recognition_difficulty:
setup_difficulty:
execution_difficulty:
casework_difficulty:
```

Examples of `mathematical_object`:
- integer / digit string
- word / multiset
- ordered tuple
- function / mapping
- permutation
- graph / coordinate object
- triangle / circle / polygon
- algebraic expression
- sequence / series
- probability space

Examples of `primary_engine`:
- direct counting / product rule
- multiset permutation
- position restriction
- block method
- complement
- gap method
- lexicographic counting
- circular symmetry
- inclusion-exclusion
- recurrence
- factorization
- substitution
- congruence
- inequality transformation
- coordinate geometry
- similarity
- invariant

The fingerprint must be specific enough that two superficially different questions with the same engine can be recognized as the same archetype.

---

# 2. Mathematics ownership test
The primary subtopic owner is determined by the **dominant mathematical move**, not by nouns in the question.

Use this decision sequence:

1. What must the student recognize before any calculation can start?
2. Which transformation/model makes the problem tractable?
3. Which concept accounts for most of the non-routine reasoning?
4. If that concept were removed, would the question collapse into routine execution?

That concept is the primary owner.

## Hybrid questions
For hybrid questions record:

```yaml
primary_engine:
secondary_engines:
engine_order:
```

Example:
```text
choose categories -> assign positions -> arrange selected objects
```

Only the primary engine owns mandatory coverage. Later capstone units may revisit the same question as `HYBRID_REVISIT` without double-counting.

---

# 3. Mathematics difficulty model
Do not assign difficulty from answer length alone.

Score five dimensions from 0-2:

- **R Recognition** - identifying the governing concept.
- **M Modelling** - translating words/diagram into mathematical structure.
- **C Casework** - partitioning cases without omission/overlap.
- **E Execution** - algebra/arithmetic/symbol manipulation.
- **V Verification** - checking boundary cases, double counting, domain, or interpretation.

Suggested conversion:

```text
0-2  -> D1
3-4  -> D2
5-6  -> D3
7-8  -> D4
9-10 -> D5
```

Override is allowed when a single recognition barrier is unusually severe; document the reason.

Difficulty drives helper depth, not prestige or exam year.

---

# 4. Math-specific H1-H3 helper policy

## H1 - Recognition cue
Purpose: restore the correct mathematical lens.

Examples:
- "Which positions are actually labelled?"
- "Can two different construction orders produce the same final object?"
- "Count the forbidden set first."
- "What remains fixed when the figure is rotated?"

H1 must not contain the numerical setup or final formula when recognition itself is the learning target.

## H2 - Structural / visual helper
H2 must change representation.

Allowed forms include:
- slots
- tree diagram
- mapping diagram
- table of cases
- number line
- coordinate sketch
- Venn/event diagram
- block/super-object picture
- gap skeleton
- circular anchor diagram
- lexicographic prefix table
- sign chart
- factorization tree
- graph / transformation sketch
- invariant tracker

H2 should reveal the **structure**, not merely restate the prose in a colored box.

## H3 - Mathematical skeleton
H3 supplies the setup but stops before routine completion.

Examples:
```text
Total - Bad = ...
```

```text
Arrange anchors -> identify gaps -> choose gaps -> arrange restricted objects
```

```text
prefixes before target = bucket_1 + bucket_2 + ...
```

```text
Let x = ... ; target equation becomes ...
```

H3 must not reveal the final answer.

---

# 5. Representation audit
Every core math concept must have a representation appropriate to its recognition barrier.

## Representation rules
- Meaning before symbolic compression for new concepts.
- Formula should be shown as a compressed form of a model when feasible.
- Use two representations when students commonly fail to recognize equivalence between forms.
- Diagrams must encode mathematical relationships, not decorate the page.
- A helper diagram must be consistent with the exact constraints of the question.

## Representation mismatch failures
Mark FAIL when:
- a diagram implies repetition when repetition is forbidden;
- a circular diagram is treated as a linear row;
- a case table overlaps cases;
- an algebraic diagram suppresses a domain restriction;
- a graph suggests monotonicity or intersections inaccurately;
- an H2 visual is generic and does not illuminate the actual obstruction.

---

# 6. Mathematics misconception taxonomy
Use stable tags where applicable.

## General counting / combinatorics
- ORDER_IGNORED
- ORDER_INVENTED
- REPETITION_ACCIDENTALLY_ALLOWED
- REPETITION_ACCIDENTALLY_FORBIDDEN
- DOUBLE_COUNT
- MISSING_CASE
- OVERLAPPING_CASES
- ADD_INSTEAD_OF_MULTIPLY
- MULTIPLY_INSTEAD_OF_ADD
- COMPLEMENT_UNIVERSE_WRONG
- INCLUSION_EXCLUSION_OVERLAP_MISSED
- LABELLED_UNLABELLED_CONFUSION

## Permutation-specific
- ZERO_LEADING
- BLOCK_OVERCOUNT
- BLOCK_INTERNAL_ORDER_MISSED
- GAP_OFF_BY_ONE
- GAP_CAPACITY_IGNORED
- CIRCULAR_ROTATION_OVERCOUNT
- CIRCULAR_REFLECTION_CONFUSION
- DICTIONARY_PREFIX_MISCOUNT
- DICTIONARY_OFF_BY_ONE
- FIXED_POINT_DERANGEMENT_CONFUSION

## Algebra / number / functions
- DOMAIN_RESTRICTION_MISSED
- EXTRANEOUS_ROOT_ACCEPTED
- SIGN_ERROR
- ZERO_CASE_MISSED
- DIVIDE_BY_ZERO_CASE_LOST
- MODULAR_CONDITION_MISREAD
- FUNCTION_DOMAIN_RANGE_CONFUSION

## Geometry
- DIAGRAM_ASSUMED_TO_SCALE
- ORIENTATION_CASE_MISSED
- CONGRUENCE_SIMILARITY_CONFUSION
- DIRECTED_ANGLE_SIGN_CONFUSION
- LENGTH_AREA_SCALE_CONFUSION

For D2+ items, attach at least one tag when a plausible wrong path exists.

A misconception card must answer all three:
1. Why is the wrong method tempting?
2. Exactly which mathematical assumption fails?
3. What repair question/habit prevents recurrence?

---

# 7. Mathematical solution verification gate
Every REQUIRED math source row must be independently verified before release.

## 7.1 Re-solve from the statement
Do not verify a solution merely by comparing with the source answer.

Reconstruct the solution from the actual source constraints.

## 7.2 Mandatory checks
Depending on the problem, verify:
- domain and range;
- leading-zero restrictions;
- repetition permissions;
- labelled vs unlabelled objects;
- mutually exclusive / exhaustive cases;
- overlap in inclusion-exclusion;
- boundary values;
- parity/divisibility constraints;
- symmetry quotienting;
- repeated-object factorial division;
- exact vs at-least vs at-most wording;
- whether the source asks for count, sum, probability, rank, or object itself.

## 7.3 Independent-method check
For D4-D5, or whenever the source solution is suspicious, use a second verification route when feasible:
- direct enumeration for a smaller analogous case;
- complementary count;
- recurrence vs closed form;
- algebraic vs combinatorial derivation;
- computational sanity check;
- invariant or symmetry check.

Record:
```yaml
answer_verified: YES / REVIEW
verification_method:
second_method_used: YES / NO
source_answer_agrees: YES / NO / UNKNOWN
```

## 7.4 Source solution issue
If a published source appears wrong or incomplete:
- do not copy it silently;
- move the row to REVIEW;
- state the suspected failure (double count, omitted case, ambiguous wording, etc.);
- resolve before counting it as covered if the issue changes the required solution/help.

---

# 8. Formula and notation quality gate
Mathematics must be typeset as mathematics.

## Required
- use proper superscripts/subscripts;
- use true fractions, roots, factorials, summation/product notation where appropriate;
- distinguish `nPr` from `nCr` visually and semantically;
- define symbols before first use;
- align multi-line derivations when alignment aids comprehension;
- retain equality/implication logic accurately;
- keep mathematical expressions together rather than breaking them awkwardly across lines.

## Avoid
- ASCII approximations when proper math notation is available;
- cramped formulas constructed as body text;
- unexplained variable changes;
- mixing different notations for the same object without reason;
- decorative equations without interpretation.

For permutation/counting material, prefer canonical notation such as:

```text
n!,  P(n,r) / nPr,  C(n,r) / nCr
```

but choose one primary notation and explain alternatives.

---

# 9. Real-life / intuitive bridge gate for mathematics
A context is useful only if it preserves the mathematical structure.

Good contexts:
- medals for labelled rank positions;
- access codes for ordered symbol strings;
- lift exits for assignments;
- seating for adjacency/gaps;
- dictionary ordering for lexicographic rank;
- passwords for repetition/required-symbol constraints.

Reject contexts that:
- introduce irrelevant realism;
- require assumptions not in the mathematical model;
- obscure rather than reveal the structure;
- imply a different probability/counting universe.

For each CORE concept, ask:
> Does the context make the structural distinction easier to see?

If no, remove it.

---

# 10. Math Study Guide completeness gate
For each core concept verify all applicable layers:

1. intuitive/real-life entry;
2. meaning before notation;
3. faithful mathematical representation;
4. worked teacher model exposing decisions;
5. guided completion;
6. misconception + repair;
7. exam/trigger language;
8. disguised transfer;
9. retrieval/explanation check;
10. representative source/PYQ link;
11. boundary/special-case note where relevant;
12. notation/formula summary only after meaning is established.

Do not compress away items 1, 3, 6, 8, or 9 to reduce page count.

---

# 11. Math Practice Book integrity gate
Every REQUIRED row must satisfy:

```text
[ ] source row correctly owned
[ ] source URL/file reference present
[ ] question paraphrase preserves all constraints
[ ] concept backlink resolves
[ ] D-level recorded
[ ] misconception tag recorded when applicable
[ ] helper depth satisfies D-level
[ ] H2 is genuinely structural/visual when required
[ ] H3 stops before final answer
[ ] adequate working space provided
[ ] final answer not exposed on question page
[ ] Appendix solution complete
[ ] answer independently verified
[ ] notation readable
[ ] rendered question/helper/solution pages pass QA
```

---

# 12. Math-specific duplicate and archetype audit
Two questions may be duplicates even when surface wording differs.

Create an `archetype_signature` from:

```text
mathematical object
+ constraint pattern
+ primary engine
+ target quantity
```

Examples:
- `WORD + repeated letters + all vowels together + count`
- `DIGITS + no repetition + > bound + divisible by 5 + count`
- `CIRCLE + two categories + no adjacent restricted category + count`

Use this signature to detect:
- true duplicates;
- near-duplicates useful as transfer;
- repeated years testing the same engine;
- gaps where an archetype has no supported representative example.

Do not remove useful near-duplicates merely because the final formula is similar; preserve variations that change recognition or casework.

---

# 13. Coverage depth audit
A subtopic may have 100% row coverage but poor instructional depth.

For each subtopic compute:

```text
required_rows
covered_rows
unique_archetypes
archetypes_with_model_example
archetypes_with_guided_example
archetypes_with_independent_PYQ
D3plus_rows_with_H2
D4plus_rows_with_H3
misconception_tags_covered
```

Recommended release rule:
- every REQUIRED row covered;
- every major archetype taught at least once;
- every major archetype represented in independent practice;
- every D3+ row has the required helper support;
- no known high-frequency misconception is completely untreated.

---

# 14. Mixed/capstone transfer gate
When the project contains a final mixed-mathematics or hybrid-permutation unit, ensure the learner must **choose the engine**, not just execute it.

Capstone set should include:
- unlabeled-method questions;
- superficially similar questions requiring different engines;
- two-stage or three-stage hybrids;
- at least one question where a tempting familiar method is wrong;
- at least one question requiring a classification decision before calculation.

Audit whether the solution begins with the recognition decision, not only the arithmetic.

---

# 15. Mathematics readability/render gate
In addition to the general readability rules:

- mathematical symbols must render cleanly at normal zoom and print scale;
- exponents, subscripts, radicals, and combinatorial notation must remain legible;
- diagrams must not collide with labels;
- coordinate axes/table boundaries/tree branches must remain visible;
- equation lines must not clip at card boundaries;
- answer-choice/math alignment must not suggest false grouping;
- a page failing mathematical legibility must be rebuilt, never rescued by shrinking notation.

Dense proof/solution pages should be inspected individually after export.

---

# 16. Required math audit outputs
Extend the general audit workbook/report with:

## Master ledger additional columns
```text
Mathematical Object
Constraint Signature
Primary Engine
Secondary Engines
Archetype Signature
R/M/C/E/V difficulty components
D-level
Required Representation
Misconception Tag
Independent Answer Verification
Source Answer Agreement
```

## Subtopic math summary
```text
Subtopic
Required
Covered
Unique Archetypes
Archetypes Taught
D3+ H2 Pass
D4+ H3 Pass
Answer Verified
Notation Failures
Release Gate
```

## Review queue reasons
Priority order:
1. suspected incorrect source answer/solution;
2. ambiguous source statement/figure;
3. ownership conflict;
4. uncovered REQUIRED row;
5. missing concept support;
6. helper-policy failure;
7. notation/render failure;
8. duplicate metadata cleanup.

---

# 17. Permutation-project extension
For permutation/combinatorics projects, use these canonical engine owners when they fit the actual corpus:

```text
ST01 product rule / ordered slots / nPr
ST02 repeated objects / multiset permutations
ST03 positional restrictions
ST04 together / block method
ST05 not-all-together / complement
ST06 no-two-together / gap method
ST07 number formation
ST08 dictionary / lexicographic rank
ST09 circular permutations
ST10 derangements / forbidden positions
ST11 forbidden strings / inclusion-exclusion
ST12 hybrid permutation structures
```

Ownership is still determined by primary engine, not by this list mechanically.

For each permutation row also consider:
- repeated-object signature;
- zero-leading condition;
- adjacency/together condition;
- gap capacity;
- circular equivalence;
- lexicographic prefix structure;
- fixed-point/forbidden-position structure;
- inclusion-exclusion overlap;
- choose-then-arrange hybrid stages.

---

# 18. Final math release stamp
Do not declare a mathematics subtopic complete unless:

```text
CORPUS COVERAGE = PASS
OWNERSHIP = PASS
ARCHETYPE COVERAGE = PASS
PEDAGOGY SUPPORT = PASS
H-POLICY = PASS
SOLUTION VERIFICATION = PASS
SOURCE-ISSUE QUEUE = CLEAR OR NON-BLOCKING
MATH NOTATION = PASS
READABILITY / RENDER = PASS
```

Final status:
- FAIL
- PROVISIONAL
- LOCALLY_COMPLETE
- COMPLETE

`COMPLETE` requires the general corpus auditor and this mathematics extension to agree.
