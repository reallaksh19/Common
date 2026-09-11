# Grade 9 Platform Integration Addendum v1

## Purpose

The IOQM Grade 9 study-guide builder is a **specialization of the existing Grade 9 learning platform**, not a parallel replacement for it.

Use the generic Grade 9 skills for source custody, canonical master data, difficulty modelling, calibrated question generation, misconception/diagnostic objects, and PDF publishing. Use the IOQM builder for the additional contest-corpus work those generic contracts do not fully specify: recognition decomposition, opening signatures, executable first moves, legality, transfer-gap auditing, visual obligations, learner-specific short-horizon routing, and Appendix A question-to-support completeness.

The integration principle is:

```text
Grade 9 platform infrastructure
        +
IOQM contest-corpus assimilation engine
        ->
one canonical learning package
```

---

## 1. Inherited Grade 9 contracts

Before an IOQM production build, reuse these existing Grade 9 contracts rather than re-inventing them:

- `Grade 9/skills/grade9-source-grounding/SKILL.md`
- `Grade 9/skills/grade9-concept-architect/SKILL.md`
- `Grade 9/skills/grade9-math/SKILL.md` for Mathematics
- `Grade 9/skills/grade9-question-bank/SKILL.md` when creating calibrated original practice/challenges
- `Grade 9/skills/grade9-learning-enrichment/SKILL.md`
- `Grade 9/skills/grade9-textbook-publisher/SKILL.md`
- `Grade 9/skills/grade9/references/grade9-master.schema.json`
- `Grade 9/skills/grade9/references/grade9-workflow.md`

The IOQM skill adds specialization; it does not weaken these platform rules.

---

## 2. Source-grounding inheritance

Use the Grade 9 source statuses exactly:

```text
VERIFIED_TRANSCRIPTION
RECONSTRUCTED
QC_ALERT
SOURCE_UNRESOLVED
```

Use the Grade 9 provenance classes where applicable:

```text
USER_UPLOADED_ANCHOR
OFFICIAL_PYQ
SECONDARY_VERIFIED_PYQ
PUBLISHED_REFERENCE
ORIGINAL_CALIBRATED
RECONSTRUCTED_FROM_SCAN
```

Never silently repair a defective source. Preserve the original statement/status and store a verified correction separately.

IOQM adds contest-specific custody fields such as local corpus ID, source-required figure, answer-custody status, and whether an item is usable in scored Appendix A.

---

## 3. Canonical master data inheritance

Use `grade9-master.schema.json` as the canonical base object. Do not create a competing master-data format.

The schema permits additional fields. Store IOQM-specific analysis as additive extensions, for example:

```text
question.ioqm.recognition_cue
question.ioqm.representation
question.ioqm.first_move
question.ioqm.execution_route
question.ioqm.legality_check
question.ioqm.variant_ids
question.ioqm.transfer_lab_ids
question.ioqm.visual_obligation
question.ioqm.hint_route
question.ioqm.support_status

concept.ioqm.opening_signatures
concept.ioqm.transfer_range
concept.ioqm.visual_assets
concept.ioqm.teaching_unit_ids
```

Every scored question still has exactly one `primary_concept_id` and may have secondary concepts, as required by the Grade 9 concept architecture.

### Important distinction

`primary_concept_id` is navigation/analytics authority. It does **not** prove instructional sufficiency.

An IOQM question also needs an executable route:

```text
recognition
-> representation
-> first move
-> execution
-> legality/check
-> variant/transfer when needed
```

---

## 4. Concept graph vs learner teaching units

Inherit stable concept IDs and prerequisite links from `grade9-concept-architect`.

However, do not force:

```text
one concept ID = one student page
```

or:

```text
one internal stable skill = one learner-facing teaching unit
```

The internal concept/method graph is support infrastructure. Student teaching units may:

- merge several closely linked internal concepts into one coherent learning journey;
- split one broad concept into multiple learning episodes when recognition, representation, first move, legality, or transfer differs;
- nest variants inside a parent concept;
- expand a transfer-heavy idea across several pages.

The design target is **concept assimilation**, not a predetermined count of skills, concepts, chapters, or pages.

---

## 5. Difficulty inheritance and badges

Use the Grade 9 Mathematics difficulty vector underneath the learner-facing badge:

```text
conceptual
recognition
reasoning_steps
algebra
hidden_structure
constraints_cases
calculation_burden
trap_density
```

The scalar screening score is metadata, not psychometric truth.

For student display, a simple D1-D5 badge may summarize the vector, but keep these dimensions separate:

```text
DIFFICULTY != PRIORITY
DIFFICULTY != LEARNER_MASTERY
DIFFICULTY != SOURCE_STATUS
DIFFICULTY != FREQUENCY
```

### Concept badges

Prefer a range when core and transfer demand differ:

```text
Chinese Remainder Theorem
[CORE D3] [TRANSFER D5] [HIGH-YIELD]
```

### Question badges

Example:

```text
Q17 [D4 ADVANCED] [TRANSFER] [OFFICIAL PYQ]
```

After learner diagnosis, an independent personalization badge may be added:

```text
[YOUR STATUS: DEVELOPING] [DO FIRST]
```

Do not encode learner weakness into the authored difficulty badge.

---

## 6. Question-bank inheritance

The supplied/frozen Appendix A corpus remains source-grounded and must not be silently rewritten to fit a desired difficulty distribution.

Use `grade9-question-bank` when the build needs:

- same-level calibrated original practice;
- challenge/next-level variants;
- mixed mastery sets;
- Appendix B original questions;
- difficulty-vector matching.

Keep the Grade 9 candidate relationships where useful:

```text
NEAR_TWIN
STRUCTURAL_ANALOGUE
CONCEPT_REINFORCEMENT
ADVANCED_TRANSFER
```

The IOQM layer additionally checks that the intended recognition mechanism, opening signature, and transfer lineage are preserved.

---

## 7. Learning-enrichment inheritance

Borrow the Grade 9 causal misconception model:

```text
wrong response
-> likely misconception
-> diagnostic probe
-> targeted repair
-> retry / transfer
```

Store specific wrong mental models, not generic warnings.

The Grade 9 enrichment skill may internally keep richer helper/hint objects. For the normal IOQM learner surface, expose the simpler progressive ladder unless the user requests full worked-solution scaffolding:

```text
NOTICE - recognition clue
RECALL - relevant concept / representation
START - first executable setup
```

Always attempt H0/unaided work before revealing support when the context is diagnostic or transfer testing.

---

## 8. Mathematics concept-assimilation inheritance

Borrow from `grade9-math`:

```text
RECONNECT
-> DISCOVER
-> MAKE SENSE
-> TRY
-> DIAGNOSE
-> FADE
-> ADOPT
-> TRANSFER
```

and its six assimilation questions:

1. What did you notice?
2. Why does the method work?
3. What clue would make you think of it?
4. What similar-looking situation needs a different method?
5. Can you write the first useful lines without help?
6. Can you solve a disguised version?

The IOQM student-book generator operationalizes those ideas through teacher-like concept journeys, concrete first moves, close variants, legality examples, guided practice, structural visuals, and corpus-linked transfer labs.

---

## 9. Publishing inheritance

Use `grade9-textbook-publisher` as the publishing authority.

Canonical structured master data is the source of truth. PDF pages are render outputs.

Preserve the linked architecture:

```text
Concept
<-> Core practice
<-> Challenge / transfer
<-> Helper / hint
<-> Solution / answer
<-> Misconception diagnosis
<-> Mixed-test diagnosis
```

IOQM adds:

- Part 0 learner-specific Navigator when requested;
- question-to-concept/variant/transfer routing;
- visual-obligation lifecycle;
- Appendix A source custody and progressive hint behavior;
- Appendix B independent mixed transfer;
- Appendix C decision-first quick reference;
- Appendix D answers/provenance when the chosen package uses four appendices.

Keep reviewer matrices, graph exports, QA gates, and raw transfer IDs out of the normal student reading path.

---

## 10. Recommended integrated workflow

```text
1. Freeze syllabus / scope
2. Research and collect source-grounded material
3. Store reusable source notes in the domain folder
4. Freeze Appendix A corpus and custody
5. Decompose every question
6. Build canonical concept graph + IOQM opening/transfer extensions
7. Assign difficulty vectors and simple badges
8. Ask learner self-report and run a short unaided diagnostic
9. Build learner-specific Part 0 route
10. Prototype concept assimilation + question page + navigation page
11. Expand all required teaching units without a page/count target
12. Generate calibrated extra practice only when needed
13. Build Appendix A/B/C/D according to package mode
14. Publish from canonical master data
15. Render, link-check, visual-QA, answer-QA, and support-QA
```

---

## 11. Integration gates

```text
GRADE9_SOURCE_STATUSES_REUSED = PASS
GRADE9_PROVENANCE_CLASSES_REUSED = PASS
GRADE9_MASTER_SCHEMA_IS_CANONICAL = PASS
PRIMARY_CONCEPT_ID_PRESENT = PASS_n_OF_n
IOQM_EXECUTABLE_ROUTE_PRESENT = PASS_n_OF_n
GRADE9_DIFFICULTY_VECTOR_PRESENT = PASS_n_OF_n_WHERE_SCORED
CONCEPT_BADGES_PRESENT = PASS_n_OF_n_WHERE_DISPLAYED
QUESTION_BADGES_PRESENT = PASS_n_OF_n_WHERE_DISPLAYED
DIFFICULTY_PRIORITY_MASTERY_CONFLATION = 0
GRADE9_PUBLISHER_CONTRACT_REUSED = PASS
RAW_REVIEWER_DATA_IN_STUDENT_UI = 0
```

---

## Final integration rule

Use the Grade 9 platform for **reliable educational infrastructure** and the IOQM specialization for **contest-method self-sufficiency**.

The platform tells us where an item belongs, how hard it is, where it came from, and how it should be published.

The IOQM layer additionally guarantees that the learner has been taught enough to answer:

```text
What am I seeing?
What representation fits?
What do I write or draw first?
Which nearby variant changes the route?
What can make this move illegal?
How do I finish and check?
```
