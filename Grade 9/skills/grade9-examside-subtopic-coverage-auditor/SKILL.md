---
name: grade9-examside-subtopic-coverage-auditor
version: 3
purpose: Audit JEE subtopic study guides and ExamSIDE practice companions for corpus coverage, pedagogy completeness, misconception handling, helper quality, readability, and release readiness.
---

# ExamSIDE Subtopic Coverage Audit v3

## Release principle
A subtopic is complete only when **all four audits** pass:

1. **Corpus audit** - every relevant ExamSIDE source question has one declared home/disposition.
2. **Pedagogy audit** - every core concept is taught through the required learning layers.
3. **Practice integrity audit** - source links, concept backlinks, helper depth, and Appendix solutions are complete.
4. **Readability/layout audit** - the page remains comfortably readable without shrinking type to force content into a layout.

A visually finished PDF is not a completed subtopic unless all four pass.

---

## A. Corpus ledger - one row per ExamSIDE source question
Required fields:

- source_id
- source_section (MCQ / Numerical)
- source_number
- exam_year / date / shift
- source_url
- short_question_fingerprint
- permutation_relevance: PURE / HYBRID / EXCLUDE
- primary_subtopic (unique)
- secondary_subtopics (optional)
- disposition: REQUIRED / DEFER / EXCLUDE / UNCLASSIFIED
- disposition_reason
- concept_code + Study Guide page
- difficulty: D1-D5
- helper_policy: H0-H3
- misconception_tag
- required_representation: slots / tree / mapping / block / gap / case table / circular / lexicographic / inclusion-exclusion / other
- practice_question_id + page
- source_link_present Y/N
- concept_backlink_present Y/N
- Appendix-A_solution_present Y/N
- answer_verified Y/N
- audit_status: PASS / GAP / DRIFT / VERIFY

### Corpus invariants
- Every frozen source row has exactly one primary disposition.
- One question has one primary subtopic owner.
- No REQUIRED row may be absent from its practice PDF.
- No question is moved into a subtopic merely to increase question count.
- DEFER rows must name the destination subtopic.
- Chapter-wide COMPLETE requires UNCLASSIFIED = 0.

---

## B. Difficulty -> helper policy

- D1: H0 or H1 optional.
- D2: H1 required when recognition is non-obvious; H2 optional.
- D3: H1 + H2 required.
- D4-D5: H1 + H2 + H3 required.

### Helper semantics
- **H1 Recognition cue** - changes what the learner notices; no numerical setup/result.
- **H2 Visual/concept helper** - slot/tree/mapping/case/structure visual; not merely longer prose.
- **H3 Structural skeleton** - gives the product/case skeleton but stops before arithmetic/final answer.
- Use the **minimum helper needed**. If H1 restores the model, do not force H2/H3.

---

## C. Pedagogy audit - required for every core Study Guide concept
Each core concept must contain all applicable layers:

1. **Real-life / intuitive entry**
   - Concrete situation where the mathematical structure is naturally meaningful.
   - Context must illuminate the idea rather than decorate the page.

2. **Meaning before notation**
   - Student first sees what makes two outcomes different.
   - Formula/name follows the model.

3. **Concept helper / representation**
   - At least one faithful representation: slots, branch tree, choice pool, mapping, contrast, etc.
   - Two representations when the concept has a common recognition barrier.

4. **Worked teacher model**
   - Expose the expert decision sequence, not only the final algebra.

5. **Guided completion**
   - Some structure is supplied; learner completes missing choices/counts/reasoning.

6. **Misconception + repair**
   - Name the tempting wrong model.
   - Explain *why it looks plausible*.
   - Identify the exact structural assumption that fails.
   - Give a repair habit or diagnostic question.

7. **JEE trigger language**
   - Teach wording that should trigger the method/representation.

8. **Disguised transfer**
   - Same engine in a different surface form.

9. **Retrieval / explanation check**
   - Learner explains, classifies, predicts, diagnoses, or constructs the model; not only calculates.

10. **Representative PYQ link**
   - At least one ExamSIDE fingerprint/source link when directly representative.

### Pedagogy anti-drift rule
Do not compress away real-life entry, concept helpers, misconceptions, transfer, or retrieval merely to reduce page count. If a page becomes dense, **split the page**.

---

## D. Misconception taxonomy for permutations
Stable tags:

- ORDER_IGNORED
- REPETITION_ACCIDENTALLY_ALLOWED
- REPETITION_ACCIDENTALLY_FORBIDDEN
- MISSING_ASSIGNMENT_STAGE
- ADD_INSTEAD_OF_MULTIPLY
- FORMULA_FIRST_RESTRICTION_HIDDEN
- ZERO_LEADING
- BLOCK_OVERCOUNT
- GAP_OFF_BY_ONE
- CIRCULAR_ROTATION_OVERCOUNT
- DICTIONARY_PREFIX_MISCOUNT
- IE_OVERLAP_MISSED

For D2+ questions, attach at least one misconception tag when a plausible wrong model exists.

---

## E. Readability + layout audit (mandatory gate)

### 1. Typography floor
For landscape A4 study/practice PDFs:

- Page title: target 18-24 pt minimum.
- Section heading: target 13-16 pt.
- Main explanatory body: target **11-12 pt**.
- Question body: target **11-12 pt**.
- Card/helper prose: target **10.5-11.5 pt**.
- Micro-labels/chips may be 8-9 pt because they are navigation, not instructional prose.
- Solution prose: target **11 pt or larger**.

**Fail** if instructional prose is reduced below readable print size just to fit a page.

### 2. Card density
- A card should contain one dominant idea.
- Small card: ~35-45 words maximum.
- Medium card: ~55-70 words maximum.
- Large card: ~90-110 words maximum.
- If content exceeds the appropriate density, shorten, enlarge, or split the page.

### 3. Page-role gate
Every page must have one dominant role:

- ENTRY
- EXPLAIN
- COMPARE
- MODEL
- HELPER
- GUIDED
- PRACTICE
- MISCONCEPTION
- TRANSFER
- AUDIT
- SUMMARY

If multiple roles compete for dominance and type must shrink, split the page.

### 4. Box-count gate
- Avoid more than 4 dense instructional boxes on one landscape page.
- Misconception clinic: target **2-3 misconception cards per page**, never 6 dense cards.
- Real-life entry: target **2 major examples per page** plus synthesis, rather than 4 dense examples.

### 5. Visual hierarchy gate
Within ~3 seconds a learner should be able to identify:
1. what to read first,
2. what to notice second,
3. what to do next.

If hierarchy is unclear, redesign.

### 6. Whitespace rule
Whitespace must be either:
- intentional response/work space, or
- breathing room supporting hierarchy.

Avoid both extremes:
- large accidental dead zones,
- overpacked cards that force small type.

### 7. Render QA
Before release:
- render every page at ~150-200 dpi,
- inspect contact sheets and individual dense pages,
- check for clipping, overlap, text crossing boundaries, broken glyphs, and unreadably small type,
- verify links after PDF generation,
- re-render after every material typography/layout change.

### 8. Readability failure rule
If a page fails readability, do **not** solve it by reducing font size. Repair in this order:
1. shorten wording,
2. remove duplication,
3. enlarge/restructure the card,
4. move content to a new page,
5. only then make minor typographic adjustments within the typography floor.

---

## F. Practice PDF integrity gate
A subtopic practice PDF passes only if all REQUIRED rows satisfy:

- Included in practice PDF.
- Original ExamSIDE source URL present.
- Linked to an existing Study Guide concept code/page.
- Helper depth satisfies difficulty policy.
- H2 is visual/structural when required.
- Final answer is not revealed on the question page.
- Appendix A contains a complete solution.
- Question and helper text pass readability gate.
- Solution text passes readability gate.
- No duplicate question counted twice unless explicitly marked as hybrid revisit.

---

## G. Study Guide audit gate

- Every concept code referenced by practice exists.
- Concept page is inside declared subtopic scope.
- Study Guide does not teach deferred machinery prematurely.
- Real-life examples are mathematically useful, not ornamental.
- Concept helper exists where recognition is a barrier.
- Misconceptions are placed close enough to the concept to support repair.
- End-of-subtopic mastery checklist covers concepts required by the question ledger.
- Typography/layout gate passes page-by-page.

---

## H. Subtopic reconciliation report
Always publish:

- Required: X
- Included: X/X
- Source links: X/X
- Concept links: X/X
- Solutions: X/X
- Misconception tags: X/X for D2+
- H-policy failures: 0
- Pedagogy-layer failures: 0
- Readability failures: 0
- Deferred: N with destinations
- Excluded: N with reasons
- Unclassified: N
- Local status: PASS / FAIL
- Chapter status: COMPLETE / PROVISIONAL
