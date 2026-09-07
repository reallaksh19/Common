---
name: grade9-transfer-coverage-auditor
description: Audit Grade 9 source-grounded learning packages subtopic-by-subtopic so every eligible external transfer question (for example ExamSIDE PYQs) is classified, assigned to exactly one primary subtopic, linked to taught concepts, present in the correct transfer book, supported by difficulty-appropriate hints, and solved in the answer appendix. Use when proving that required external questions are covered without scope drift or silent omissions.
---

# Grade 9 Transfer Coverage Auditor

Prove external-question coverage **subtopic by subtopic**. This is a completion/audit skill, not a content-expansion skill.

## Core rule

The source-grounding layer determines whether an external question is eligible. The learner architecture determines where it belongs. The auditor verifies that every eligible question has a valid home and complete support.

```text
SOURCE SCOPE
-> FROZEN EXTERNAL CORPUS
-> ELIGIBILITY
-> PRIMARY SUBTOPIC
-> PRIMARY CONCEPT
-> TRANSFER-BOOK PLACEMENT
-> HINT SUPPORT
-> APPENDIX SOLUTION
-> LINK CHECK
-> PASS / BLOCK
```

Do not use audit failure as permission to introduce new subject content.

## Two independent statuses

Keep **scope status** and **coverage status** separate.

### Scope status

Use the source-grounding statuses already defined by the project:

- `ELIGIBLE_IN_SCOPE`
- `PARTIAL_SCOPE`
- `OUT_OF_SCOPE`
- `SOURCE_UNRESOLVED`

### Coverage status

For each corpus item also assign exactly one:

- `PLACED` — included in the correct subtopic transfer material.
- `DEFERRED_VALID` — eligible, but intentionally assigned to a named later subtopic not built yet.
- `EXCLUDED_VALID` — allowed only when scope status is `PARTIAL_SCOPE` or `OUT_OF_SCOPE`; reason required.
- `UNRESOLVED` — source cannot yet be verified/retrieved.
- `MISSING` — eligible and should already be placed, but is absent. This is a blocking failure.

At **final chapter acceptance**, no `ELIGIBLE_IN_SCOPE` item may remain `DEFERRED_VALID` or `MISSING`.

## Primary-subtopic rule

Every `ELIGIBLE_IN_SCOPE` question must have exactly one `primary_subtopic_id`.

A question may have secondary concept/subtopic links, but it must be published only once in the canonical transfer corpus unless the user explicitly asks for deliberate repetition.

This prevents:

- double counting the same PYQ in several subtopics;
- gaps caused by assuming another subtopic will cover it;
- bloated question books with repeated questions.

## Required question coverage record

```json
{
  "external_question_id": "EX-RX-018",
  "snapshot_id": "EXAMSIDE_SNAPSHOT_2026_09_07",
  "source_url": "...",
  "source_status": "VERIFIED_TRANSCRIPTION",
  "scope_status": "ELIGIBLE_IN_SCOPE",
  "scope_reason": "minimum path uses oxidation-number rules only",
  "primary_subtopic_id": "RX-ST01",
  "secondary_subtopic_ids": [],
  "primary_concept_id": "RX-ON-C04",
  "secondary_concept_ids": ["RX-ON-C02"],
  "question_family": "OXIDATION_NUMBER",
  "novelty": "KNOWN_VARIANT",
  "difficulty_level": 2,
  "coverage_status": "PLACED",
  "study_guide_concept_link": "RX-ON-C04",
  "transfer_book_question_id": "E02",
  "hint_depth_required": 2,
  "h1_present": true,
  "h2_present": true,
  "h3_present": false,
  "visual_helper_required": false,
  "visual_helper_present": false,
  "appendix_solution_id": "APP-A-E02",
  "source_link_present": true,
  "source_link_valid": true,
  "support_status": "COMPLETE"
}
```

Never use rendered PDF page numbers as the authoritative link. Stable concept/question IDs are authoritative; page numbers are derived publication metadata.

## Required subtopic audit record

Each subtopic must emit a self-check record:

```json
{
  "subtopic_id": "RX-ST01",
  "title": "Oxidation Number",
  "source_obligation_ids": ["RX-S01", "RX-S02"],
  "concept_ids": ["RX-ON-C01", "RX-ON-C02"],
  "required_external_question_ids": ["EX-RX-003", "EX-RX-015"],
  "placed_question_ids": ["EX-RX-003", "EX-RX-015"],
  "deferred_question_ids": [],
  "missing_question_ids": [],
  "wrong_subtopic_question_ids": [],
  "invalid_concept_link_ids": [],
  "missing_hint_support_ids": [],
  "missing_solution_ids": [],
  "broken_source_link_ids": [],
  "scope_leak_ids": [],
  "status": "PASS"
}
```

## Self-checklist for every subtopic

Do not mark a subtopic complete until all applicable checks pass.

### A. Corpus accounting

- [ ] External corpus snapshot ID is frozen and recorded.
- [ ] Every candidate in the snapshot has a scope status.
- [ ] Every `ELIGIBLE_IN_SCOPE` candidate has exactly one primary subtopic.
- [ ] All questions whose `primary_subtopic_id` equals this subtopic appear in the `required_external_question_ids` set.
- [ ] No required question is silently omitted.
- [ ] No question is counted twice as primary coverage.

### B. Concept support

- [ ] Every required question has one primary concept ID.
- [ ] The primary concept is actually taught in the Study Guide.
- [ ] All prerequisite concepts used by the minimum solution path are taught before transfer.
- [ ] No required question depends on untaught chemistry/mathematics/physics.
- [ ] Secondary concept links are recorded where useful but do not replace the primary link.

### C. Transfer-book placement

- [ ] Every required question is present in the correct subtopic transfer book.
- [ ] The transfer-book question ID is stable and recorded.
- [ ] The original source link is present.
- [ ] The source link resolves to the intended question/index source.
- [ ] The question is not accidentally duplicated in another subtopic as a canonical item.

### D. Difficulty support

Use the user's H1-H3 policy unless another policy is specified:

- difficulty 1 -> H1 required;
- difficulty 2 -> H1-H2 required;
- difficulty 3 -> H1-H3 required plus a reasoning/visual helper when the difficulty comes from hidden representation or multi-step recognition.

Checklist:

- [ ] Required hint depth matches difficulty.
- [ ] Hints are progressive rather than restating the final answer.
- [ ] Hard questions include a genuine concept/representation helper where needed.
- [ ] Hint language uses the same reasoning grammar as the Study Guide.

### E. Solution support

- [ ] Every required question has a full Appendix A solution.
- [ ] Solution uses only in-scope concepts.
- [ ] Solution follows the same first move / representation taught in the Study Guide.
- [ ] Final answer is verified.
- [ ] Any source ambiguity/QC issue is explicitly documented.

### F. Scope leakage

- [ ] No `PARTIAL_SCOPE` item is presented as an original in-scope PYQ unless the outside dependency has been removed and the item is clearly labelled as an original rewrite.
- [ ] No `OUT_OF_SCOPE` question appears in the learner transfer book.
- [ ] ExamSIDE/external corpus has not created a new teaching unit.

## Deterministic subtopic gates

Report these counters at the end of every subtopic build:

```text
SUBTOPIC_REQUIRED = n
SUBTOPIC_PLACED = n
SUBTOPIC_DEFERRED_VALID = n
SUBTOPIC_MISSING = 0
SUBTOPIC_WRONG_PLACEMENT = 0
SUBTOPIC_CONCEPT_LINK_FAILURES = 0
SUBTOPIC_HINT_FAILURES = 0
SUBTOPIC_SOLUTION_FAILURES = 0
SUBTOPIC_BROKEN_SOURCE_LINKS = 0
SUBTOPIC_SCOPE_LEAKS = 0
SUBTOPIC_STATUS = PASS
```

During an incremental build, `DEFERRED_VALID > 0` is allowed only when every deferred item has a named target subtopic.

At final chapter acceptance:

```text
CHAPTER_ELIGIBLE_TOTAL = n
CHAPTER_PLACED_UNIQUE = n
CHAPTER_DEFERRED = 0
CHAPTER_MISSING = 0
CHAPTER_DUPLICATE_PRIMARY_PLACEMENTS = 0
CHAPTER_UNTAUGHT_DEPENDENCY = 0
CHAPTER_STATUS = PASS
```

## Coverage equation

For a completed subtopic:

```text
coverage = PLACED / REQUIRED
```

A subtopic may be declared complete only when `coverage = 1.00` and all blocking-failure counters are zero.

Do **not** hide exclusions inside the denominator. `REQUIRED` means all corpus questions whose verified scope status is `ELIGIBLE_IN_SCOPE` and whose canonical `primary_subtopic_id` is this subtopic.

## Audit views

Always produce both views.

### View 1 — Subtopic -> questions

```text
RX-ST01 Oxidation Number
  -> EX-RX-003 PLACED
  -> EX-RX-015 PLACED
  -> EX-RX-029 PLACED
  -> required 3 / placed 3 / missing 0 -> PASS
```

### View 2 — Question -> subtopic

```text
EX-RX-015
  -> scope ELIGIBLE_IN_SCOPE
  -> primary subtopic RX-ST01
  -> concept RX-ON-C04
  -> transfer E02
  -> hints H1-H2
  -> Appendix A solution present
  -> source link valid
  -> COMPLETE
```

The second view catches orphan questions; the first catches thin or incomplete subtopics.

## Workflow

1. Read source-grounding records and the frozen external-corpus snapshot.
2. Read the concept/subtopic architecture.
3. Assign one primary subtopic to every eligible external question.
4. Build the subtopic required-question set **before** publishing its transfer book.
5. Compare required set against actual transfer-book placement.
6. Verify concept links, hint depth, helper obligations, Appendix A solutions and source links.
7. Emit `MISSING` immediately for any required uncovered item; do not silently defer it.
8. Permit `DEFERRED_VALID` only with an explicit named future subtopic.
9. Run the reverse question -> subtopic check.
10. Emit counters, blockers and `PASS` / `FAIL`.
11. At final chapter completion, rerun across all subtopics and require zero deferred eligible items.

## Failure policy

A failed audit is actionable. Report the smallest repair:

```text
EX-RX-021 -> MISSING
reason: primary_subtopic_id = RX-ST03 but no transfer-book record exists
repair: add to RX-ST03 transfer book; link RX-C07; provide H1-H2; add Appendix A solution
```

Do not repair by changing the question's scope or subtopic merely to make counters pass.

## Output contract

Return or persist:

- frozen corpus snapshot ID;
- question coverage ledger;
- subtopic self-check records;
- chapter roll-up counters;
- missing/deferred/wrong-placement lists;
- concept-link failures;
- hint/helper failures;
- solution failures;
- broken source links;
- scope-leak failures;
- final `PASS` / `FAIL` plus exact repairs.
