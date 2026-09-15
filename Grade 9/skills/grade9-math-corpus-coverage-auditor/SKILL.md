---
name: grade9-math-corpus-coverage-auditor
description: Unified mathematics corpus-coverage and publication-readiness auditor. Use when an external mathematics corpus (ExamSIDE, past papers, worksheets, textbook exercises, databases, URLs, or source PDFs) must be exhaustively reconciled against subtopic study guides, practice books, helpers, solutions, and final publication artifacts. Combines general source-corpus traceability with mathematics-specific ownership, solution verification, representation quality, misconception handling, helper depth, notation, difficulty, and mixed-problem transfer checks.
---

# Grade 9 Mathematics Corpus Coverage Auditor v2

## Purpose
Audit the complete chain from **source corpus -> mathematical ownership -> teaching support -> practice coverage -> verified solution -> readable publication**.

This skill replaces the former split between a general corpus auditor and a mathematics extension for math projects. It contains the generic corpus-control rules plus the mathematics-specific checks needed for rigorous release.

A finished-looking PDF is not evidence of completion.

## Final release principle
A mathematics subtopic or chapter is releasable only when all applicable gates pass:

```text
SOURCE CORPUS = PASS
OWNERSHIP / TAXONOMY = PASS
MATHEMATICAL CORRECTNESS = PASS
PEDAGOGY = PASS
PRACTICE TRACEABILITY = PASS
HELPER POLICY = PASS
MISCONCEPTION COVERAGE = PASS
REPRESENTATION QUALITY = PASS
TYPOGRAPHY / LAYOUT = PASS
UNRESOLVED SOURCE REVIEW = 0
```

Release states:

- `PROVISIONAL` - corpus still has GAP / REVIEW / UNCLASSIFIED rows.
- `LOCALLY_COMPLETE` - one subtopic has no local gaps, but chapter corpus is not fully frozen.
- `COMPLETE` - every source row has a final disposition and every REQUIRED math owner passes all gates.

---

# 1. Freeze the source corpus before auditing

A bounded source must be snapshotted before coverage claims are made.

Record:

- corpus name
- source URL / file / repository / database
- retrieval date
- visible total row/question count
- sections/types (e.g. MCQ, Numerical)
- source ordering
- duplicate identifiers where known
- source version/hash when available

For dynamic websites, freeze a source index such as:

```text
MCQ-001 ... MCQ-127
NUM-001 ... NUM-093
```

Do not claim chapter completeness from a partial screen scrape, sampled search results, or hand-picked owner list.

---

# 2. Master corpus ledger: one row per source item

Every source row must exist in the master ledger, including items later excluded.

Minimum general fields:

- `source_id`
- `source_section`
- `source_number`
- `exam_year / date / shift` when applicable
- `source_url`
- `short_question_fingerprint`
- `source_snapshot_id`
- `primary_subtopic`
- `secondary_subtopics`
- `disposition`
- `disposition_reason`
- `current_artifact`
- `practice_question_id`
- `practice_page`
- `concept_code`
- `study_guide_page`
- `source_link_present`
- `concept_backlink_present`
- `appendix_solution_present`
- `answer_verified`
- `audit_status`

Mathematics-specific fields:

- `math_relevance`: `PURE / HYBRID / EXCLUDE`
- `primary_mathematical_engine`
- `secondary_engines`
- `archetype`
- `difficulty_D1_D5`
- `recognition_load_R1_R5`
- `model_load_M1_M5`
- `calculation_load_C1_C5`
- `error_risk_E1_E5`
- `visual_need_V0_V3`
- `helper_policy_H0_H3`
- `misconception_tags`
- `required_representation`
- `solution_method`
- `independent_verification_method`
- `boundary_or_domain_check`
- `source_solution_status`

Stable source IDs are authoritative. Rendered page numbers are derived metadata.

---

# 3. Disposition model

Every row must have exactly one primary disposition:

- `REQUIRED` - belongs in the current mathematics project.
- `DEFER` - belongs to a named later subtopic or different book.
- `EXCLUDE` - outside declared scope; reason mandatory.
- `REVIEW` - cannot yet be frozen because source, figure, interpretation, overlap, or solution requires verification.
- `DUPLICATE` - same mathematical fingerprint as another source row; duplicate target required.

Never use `REVIEW` as a permanent parking state.

## Corpus invariants

- Every frozen row has exactly one primary disposition.
- Every REQUIRED row has exactly one primary subtopic owner.
- Every DEFER row names its destination.
- Every EXCLUDE row has a defensible scope reason.
- Every DUPLICATE row names the canonical source row.
- No REQUIRED row may disappear from all practice artifacts.
- Chapter-wide `COMPLETE` requires `UNCLASSIFIED = 0`, `GAP = 0`, and `REVIEW = 0`.

---

# 4. Mathematics ownership: identify the primary engine

Do not classify by surface nouns such as “digits”, “students”, “letters”, “books”, or “functions”. Classify by the mathematical engine that carries the solution.

For each question ask:

1. What decision creates the main count?
2. Which restriction changes the base universe?
3. What must the learner recognize before any arithmetic begins?
4. Which method would fail if that recognition were missed?
5. If multiple methods appear, which one is pedagogically primary?

Examples of permutation ownership engines:

- sequential ordered slots / product rule
- multiset permutation
- positional restriction
- block / together
- complement / not-all-together
- gap / separation
- digit-number formation
- lexicographic rank
- circular symmetry
- derangement / forbidden positions
- forbidden string / inclusion-exclusion
- hybrid choose -> assign -> arrange

A hybrid may reference several concepts, but it still has one primary owner unless the project explicitly permits a tagged capstone revisit.

---

# 5. Structural fingerprinting

Each source question gets a short structural fingerprint that survives wording changes.

Good fingerprints describe:

- object inventory
- ordered/unordered outcome
- repetition state
- restriction type
- symmetry/equivalence
- requested statistic/count

Example:

```text
7 distinct people around a table; no two of 3 girls adjacent; cyclic gaps
```

Avoid fingerprints that merely restate the full source wording.

Use fingerprints to detect:

- duplicates
- near-duplicates
- recurring archetypes
- owner drift
- missing practice variants
- coverage inflation

---

# 6. Archetype coverage is separate from question coverage

A chapter may include every known question but still teach an archetype poorly.

For each primary engine, track:

- number of REQUIRED source rows
- number included in practice
- number with worked teaching support
- number with transfer support
- difficulty spread
- representation spread
- repeated surface forms vs genuinely different structures

Release should fail if a high-frequency archetype is represented only by one narrow surface form even when row-level coverage numerically passes.

---

# 7. Difficulty model for mathematics

Do not assign D1-D5 using arithmetic length alone.

Audit five dimensions:

- `R` Recognition load - how hard is it to identify the method?
- `M` Model load - how hard is it to translate wording into a mathematical structure?
- `C` Calculation load - algebra/arithmetic burden.
- `E` Error risk - number of plausible wrong paths.
- `V` Visual need - benefit from a structural representation.

Suggested interpretation:

- D1: direct recognition, one-step model.
- D2: familiar engine with one modest restriction.
- D3: non-obvious model, hybrid cue, or meaningful case split.
- D4: multiple interacting restrictions / inclusion-exclusion / inverse rank / nontrivial symmetry.
- D5: deep structure, several interacting models, source ambiguity, or high proof/verification burden.

Record the reason, not only the grade.

---

# 8. H1-H3 helper policy

Difficulty determines the maximum scaffolding; actual helper need depends on the recognition barrier.

Default:

- D1: H0; H1 optional.
- D2: H1 when recognition is not obvious; H2 optional.
- D3: H1 + H2 required.
- D4-D5: H1 + H2 + H3 required.

## H1 - Recognition cue
Changes what the learner notices without setting up the full computation.

Examples:
- “Which position is restricted first?”
- “Can two selected objects exchange positions and create a new outcome?”
- “Count the bad set before trying to count the good set directly.”

## H2 - Visual / concept helper
Must be a genuine mathematical representation, not longer prose.

Possible forms:

- slots
- tree
- mapping diagram
- block/super-object
- linear gaps
- circular gaps
- case table
- prefix-bucket table
- forbidden-position grid
- Venn/event diagram
- symmetry orbit sketch
- state diagram / recurrence state

## H3 - Structural skeleton
May expose the major count structure but must stop before final arithmetic or answer.

Examples:

```text
Total - Bad = ____ - (outer arrangements x inner arrangements)
```

or

```text
prefixes before target = bucket_1 + bucket_2 + ...
```

## Helper anti-leak rule
The question page must not reveal the final answer through:

- a completed formula with evaluated arithmetic
- a helper whose last blank is trivial copying
- diagram labels that display final counts
- a source answer visible in the question crop

---

# 9. Representation-quality gate

A mathematical diagram must encode the mathematics faithfully.

Audit questions:

- Does the visual preserve labels/distinguishability correctly?
- Does it show whether order matters?
- Does it distinguish identical from distinct objects?
- Does a circular diagram avoid implying a fixed origin when rotations are equivalent?
- Does a gap diagram show end gaps when applicable?
- Does a block diagram expose internal permutations?
- Does a lexicographic table display prefix buckets in the correct order?
- Does a forbidden-position grid distinguish allowed vs forbidden cells?
- Does an inclusion-exclusion visual show overlaps that actually exist?

A decorative illustration does not satisfy H2.

---

# 10. Solution verification gate

Do not copy a source solution merely because the source is established.

For every REQUIRED question:

1. solve independently;
2. verify interpretation and domain;
3. check boundary cases;
4. verify multiplicities / symmetry factors;
5. compare against source answer when available;
6. record discrepancies explicitly.

Preferred verification methods:

- second combinatorial derivation
- small-case brute-force enumeration
- algebraic identity check
- complement/direct cross-check
- recurrence/base-case verification
- lexicographic reconstruction
- parity/divisibility sanity check
- symbolic or computational enumeration for a reduced case

Mark:

- `VERIFIED_MATCH`
- `VERIFIED_SOURCE_ERROR`
- `SOURCE_AMBIGUOUS`
- `NEEDS_REVIEW`

Never silently repair a questionable source in the student-facing book without an audit note.

---

# 11. Boundary / double-counting audit

Mathematics failures frequently arise from set boundaries rather than arithmetic.

Mandatory checks when applicable:

- leading zero
- inclusive/exclusive range endpoints
- repeated vs distinct objects
- labelled vs unlabelled destinations
- linear vs circular equivalence
- mirror/reflection equivalence
- overlapping bad events
- mutually exclusive vs overlapping cases
- multiple occurrences of the same forbidden pattern
- “not all together” vs “no two together”
- “only” vs “exactly”
- at least / at most / exactly
- duplicate words caused by repeated letters
- whether one final object can be generated by multiple case constructions

If a source solution uses a window/start-position multiplier, explicitly test whether one output can satisfy multiple windows and be double-counted.

---

# 12. Misconception taxonomy

Use stable misconception tags so coverage can be audited.

Core permutation tags:

- `ORDER_IGNORED`
- `REPETITION_ACCIDENTALLY_ALLOWED`
- `REPETITION_ACCIDENTALLY_FORBIDDEN`
- `MISSING_ASSIGNMENT_STAGE`
- `ADD_INSTEAD_OF_MULTIPLY`
- `FORMULA_FIRST_RESTRICTION_HIDDEN`
- `ZERO_LEADING`
- `BLOCK_OVERCOUNT`
- `BLOCK_INTERNAL_ORDER_MISSED`
- `GAP_OFF_BY_ONE`
- `GAP_CAPACITY_IGNORED`
- `COMPLEMENT_UNIVERSE_WRONG`
- `NOT_ALL_VS_NO_TWO_CONFUSED`
- `CIRCULAR_ROTATION_OVERCOUNT`
- `REFLECTION_CONFUSED_WITH_ROTATION`
- `DICTIONARY_PREFIX_MISCOUNT`
- `DICTIONARY_OFF_BY_ONE`
- `IE_OVERLAP_MISSED`
- `DERANGEMENT_FIXED_POINT_MISREAD`
- `CASE_OVERLAP_DOUBLE_COUNT`
- `IDENTICAL_OBJECT_OVERCOUNT`

For D2+ questions, attach at least one misconception tag whenever a plausible wrong model exists.

The Study Guide must repair high-frequency misconceptions close to the concept, not only in a final error list.

---

# 13. Pedagogy completeness gate

For every core mathematics concept, require all applicable layers:

1. **Familiar / real-life or intuitive entry**
   - Context must illuminate the mathematical structure, not decorate the page.

2. **Meaning before notation**
   - Student first sees what makes outcomes equivalent/different.

3. **Concept representation**
   - At least one faithful visual or symbolic model; two when recognition commonly fails.

4. **Worked teacher model**
   - Expose the expert decision sequence, not only algebra.

5. **Guided completion**
   - Some structure is supplied; learner completes missing choices/counts/reasoning.

6. **Misconception + repair**
   - Tempting wrong model, why it seems plausible, exact failure, repair habit.

7. **Exam trigger language**
   - Teach the wording that should activate the engine.

8. **Disguised transfer**
   - Same engine in a different surface form.

9. **Retrieval / explanation check**
   - Learner classifies, predicts, diagnoses, explains, or constructs the model.

10. **Representative source link**
   - At least one source fingerprint when directly representative.

### Anti-drift rule
Do not compress away real-life entry, visual concept helpers, misconception repair, transfer, or retrieval simply to reduce page count. If the page becomes dense, split it.

---

# 14. Practice-book integrity gate

A REQUIRED row passes only if:

- included in the intended practice artifact;
- original source link present;
- linked back to an existing Study Guide concept;
- difficulty recorded;
- helper depth satisfies policy;
- H2 is genuinely structural when required;
- misconception tag attached where appropriate;
- final answer is hidden on the question page;
- Appendix solution is complete;
- solution has been independently verified;
- source discrepancy is disclosed when relevant;
- question/helper/solution text passes readability rules.

No duplicate question may inflate the coverage numerator unless explicitly marked as a separate hybrid revisit.

---

# 15. Readability and mathematical typography gate

For landscape A4 instructional PDFs, target:

- page title: 18-24 pt+
- section heading: 13-16 pt
- body/question text: 11-12 pt
- helper/card prose: 10.5-11.5 pt
- solution prose: >=11 pt
- micro-labels/chips: 8-9 pt only when non-instructional

Mathematical notation rules:

- use real superscripts/subscripts where possible;
- distinguish `nPr`, `nCr`, factorial, powers, and indices clearly;
- align multi-line derivations;
- do not use tiny inline formulas to rescue dense layouts;
- preserve minus signs, inequality symbols, set notation, and combinatorial symbols;
- ensure repeated-object denominators and inclusion-exclusion signs are visually unambiguous.

Card/page rules:

- one dominant idea per card;
- avoid >4 dense instructional boxes per landscape page;
- misconception clinic: 2-3 cards/page;
- real-life entry: ~2 major examples/page plus synthesis;
- one dominant page role;
- whitespace must be intentional response space or breathing room.

If readability fails, repair in this order:

1. shorten wording;
2. remove duplication;
3. restructure/enlarge card;
4. split page;
5. only then make minor type adjustments within the typography floor.

Never solve a density failure by shrinking instructional prose below readable print size.

---

# 16. Render and link QA

Before release:

- render every page at roughly 150-200 dpi;
- inspect contact sheets;
- inspect all dense concept, misconception, helper, and solution pages individually;
- check clipping, overlap, broken glyphs, formula corruption, and boundary crossing;
- verify source URLs;
- verify cross-PDF concept backlinks;
- verify Appendix anchors when used;
- re-render after every material change.

Rendered PDF evidence is required; source-code inspection alone does not pass layout QA.

---

# 17. Owner-drift audit

After new subtopics are created, re-check earlier ownership decisions.

Flag `DRIFT` when:

- a question was placed in a broad early subtopic but now has a more precise owner;
- a hybrid was used to inflate two subtopic counts;
- a later concept explains the actual difficulty better;
- the source question requires machinery intentionally deferred by the Study Guide.

A chapter closeout must rerun ownership across the entire corpus, not simply aggregate local PASS stamps.

---

# 18. Source-quality review queue

Some source rows should not be frozen immediately.

Use `REVIEW` when:

- essential information is figure-dependent and the figure is not yet verified;
- displayed source solution appears to double-count;
- source wording is ambiguous;
- answer/options conflict with independent derivation;
- a dynamic webpage is missing part of the question;
- apparent duplicate status is uncertain.

For each REVIEW row record:

- issue type
- suspected owner
- independent analysis
- what evidence is missing
- resolution action
- reviewer/date

Chapter release fails while unresolved REVIEW rows remain in scope.

---

# 19. Mathematics subtopic reconciliation report

Publish for every subtopic:

- frozen source rows considered
- REQUIRED
- COVERED
- GAPS
- REVIEW
- DUPLICATES
- DEFERRED + destinations
- EXCLUDED + reasons
- source links: X/X
- concept backlinks: X/X
- Appendix solutions: X/X
- independently verified answers: X/X
- misconception tags for D2+: X/X
- H-policy failures
- pedagogy-layer failures
- representation failures
- readability failures
- notation failures
- owner-drift flags
- local status
- chapter status

Example release stamp:

```text
ST07 Number Formation
Required: 31
Covered: 31/31
Review: 0
Source links: 31/31
Concept links: 31/31
Verified solutions: 31/31
H-policy failures: 0
Representation failures: 0
Readability failures: 0
Local status: PASS
Chapter status: PROVISIONAL
```

---

# 20. Chapter closeout procedure

Run in this order:

1. Freeze corpus totals.
2. Ensure every source row exists in ledger.
3. Resolve UNCLASSIFIED.
4. Resolve REVIEW.
5. Re-run primary-engine ownership.
6. Detect duplicates and owner drift.
7. Convert every REQUIRED GAP to COVERED.
8. Verify every required solution independently.
9. Audit archetype breadth and difficulty spread.
10. Audit Study Guide concept support against required rows.
11. Audit helper and misconception coverage.
12. Audit math notation and rendered layout.
13. Verify all links/backlinks.
14. Generate per-subtopic reconciliation.
15. Generate chapter reconciliation.
16. Only then mark `COMPLETE`.

---

# 21. Anti-patterns

Fail the audit when any of these occur:

- sampling the source instead of freezing all rows;
- claiming coverage from a curated subset;
- classifying by surface nouns rather than mathematical engine;
- silently trusting source answers;
- counting duplicates twice;
- letting hybrids inflate multiple owner counts;
- using H2 as prose instead of a mathematical model;
- giving the answer away in H3;
- using formulas before explaining the mathematical meaning;
- shrinking fonts to fit a dense page;
- ornamental “real-life” examples unrelated to the engine;
- vague EXCLUDE reasons such as “not needed”;
- unresolved REVIEW rows at chapter release;
- declaring COMPLETE while GAP > 0;
- aggregating local PASS stamps without a chapter-level ownership rerun.

---

# 22. Recommended audit artifacts

For a substantial mathematics project, maintain:

1. **Master Coverage Ledger** (`.xlsx`)
   - one source row per ledger row
   - filters by owner/status/year/archetype/difficulty
   - conditional formatting for GAP/REVIEW

2. **Gap + Review Queue**
   - only unresolved rows
   - sorted by owner and severity

3. **Subtopic Reconciliation Sheet**
   - required / covered / gap / review / duplicates / release gate

4. **Source-quality Log**
   - source errors, ambiguity, figure issues, overlap concerns

5. **Publication QA Log**
   - page rendering, link verification, typography failures

6. **Chapter Closeout Report**
   - final totals and unresolved count = 0

---

# 23. Current permutation project owner taxonomy

When auditing the current JEE permutation corpus, use the present owner map unless a later ownership review justifies a change:

- ST01 Counting engine / ordered slots / product rule
- ST02 Repeated objects / multiset permutations
- ST03 Positional restrictions
- ST04 Together / block method
- ST05 Not together / complement
- ST06 No two together / gap method
- ST07 Number formation
- ST08 Dictionary / lexicographic rank
- ST09 Circular permutations
- ST10 Derangements / forbidden positions
- ST11 Forbidden strings / inclusion-exclusion
- ST12 Hybrid permutation structures

This taxonomy is project metadata, not a universal mathematics taxonomy.

---

## Final principle

A mathematics corpus is complete only when **every source item is accounted for, every eligible item has the correct mathematical owner, every owner has sufficient teaching support, every solution is verified, every helper teaches rather than leaks, every representation is mathematically faithful, and the rendered publication remains readable.**
