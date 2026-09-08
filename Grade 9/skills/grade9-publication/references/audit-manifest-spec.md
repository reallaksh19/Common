# Publication Audit Manifest Specification

Use this specification to make source-preserving reconstruction auditable by a novice agent or a deterministic script.

The recommended manifest format is JSON.

## Top-level structure

```json
{
  "publication": {},
  "source_units": [],
  "value_additions": [],
  "references": [],
  "figures": [],
  "question_records": [],
  "question_bank_qa": {},
  "render_qa": {},
  "editorial_exceptions": []
}
```

`question_records` and `question_bank_qa` are required when `publication.product_type` is a question bank, transfer book, worksheet collection, or question-plus-solution publication.

## `publication`

Required fields:

```json
{
  "source_file": "motion.pdf",
  "source_pages": 272,
  "published_pages": 180,
  "grade_band": "9",
  "subject": "Physics",
  "product_type": "question_bank",
  "core_preservation_required": true,
  "benchmark_status": "APPROVED_PROTOTYPE"
}
```

Recommended `product_type` values:

- `textbook`
- `study_guide`
- `question_bank`
- `transfer_book`
- `worksheet_collection`
- `question_plus_solution`
- `mixed`

`published_pages` may differ from `source_pages`.

## `source_units`

Every frozen core source unit must have one record.

```json
{
  "source_id": "M4A-C5",
  "source_page": 6,
  "type": "equation_derivation",
  "core": true,
  "status": "RECOMPOSED",
  "mapped_targets": ["PUB-4.1.4"],
  "raw_locator": "page 6: WHY v = u + at",
  "semantic_summary": "derives v=u+at from acceleration definition",
  "numbers_units_ok": true,
  "equation_semantics_ok": true,
  "notes": "typography normalized only"
}
```

Allowed `status` values for source units:

- `PRESERVED`
- `RECOMPOSED`
- `MERGED`
- `SPLIT`
- `INTENTIONALLY_ABSENT`
- `REVIEW_REQUIRED`

Rules:

- `source_id` must be unique.
- Every `core=true` record must have at least one `mapped_targets` item unless status is `INTENTIONALLY_ABSENT`.
- `REVIEW_REQUIRED` blocks final publication certification.
- There is no `OMITTED` status for a zero-loss build.

## `value_additions`

Value additions are not source units.

```json
{
  "value_id": "VA-M4B-01",
  "purpose": "connect",
  "supports": ["M4B-C2", "M4B-C3", "M4B-C4"],
  "description": "rectangle + triangle synthesis figure",
  "replaces_source": false
}
```

Allowed `purpose` values:

- `clarify`
- `connect`
- `diagnose`
- `practice`
- `navigate`
- `reduce_cognitive_load`

Rules:

- `replaces_source` must be false.
- `supports` should contain at least one valid source ID.

## `references`

```json
{
  "reference_id": "REF-001",
  "source_from": "EX-M4A-01",
  "target_id": "M4A-C5",
  "kind": "concept_link",
  "resolved": true,
  "published_label": "Section 4.1.4",
  "published_page": 11
}
```

Rules:

- `target_id` must resolve to a known source/publication target.
- final certification requires every reference `resolved=true`.
- visible page labels are derived data and may change.

## `figures`

```json
{
  "figure_id": "FIG-M4B-AREA",
  "source_support": ["M4B-C2", "M4B-C3", "M4B-C4"],
  "status": "REDRAW",
  "semantic_check": true,
  "labels_check": true,
  "intentional_absence": false
}
```

Allowed figure status values:

- `PRESERVE`
- `REDRAW`
- `RECONSTRUCT`
- `SUPPORT_ADD`
- `INTENTIONALLY_ABSENT`
- `REVIEW_REQUIRED`

Rules:

- `RECONSTRUCT` requires source evidence.
- `SUPPORT_ADD` is additive and must not reveal an answer intentionally withheld by the source.
- `REVIEW_REQUIRED` blocks final certification.

## `question_records` — required for question-bank products

Every frozen question must have one record. The unit of certification is the question, not merely the page.

```json
{
  "question_id": "EX-M10B-02",
  "source_page": 50,
  "set_id": "SET-7",
  "question_recap_complete": true,
  "representation_dependency": "GRAPH",
  "representation_source_status": "PRESENT_SOURCE",
  "representation_present_student": true,
  "representation_present_solution": true,
  "representation_legible": true,
  "answer_choice_status": "NOT_APPLICABLE",
  "h1_present": true,
  "h2_present": true,
  "h3_present": true,
  "hint_progression_ok": true,
  "method_has_why": true,
  "method_has_executable_route": true,
  "method_distinct_from_answer": true,
  "answer_present": true,
  "answer_semantic_if_choice": true,
  "concept_to_keep_present": true,
  "math_typography_ok": true,
  "question_to_solution_link_ok": true,
  "solution_to_question_link_ok": true,
  "source_link_ok": true,
  "copy_paste_drift_check": true,
  "status": "PASS"
}
```

Allowed `representation_dependency` values:

- `NONE`
- `GRAPH`
- `DIAGRAM`
- `TABLE`
- `TIMELINE`
- `NUMBER_LINE`
- `OPTION_FIGURES`
- `STATEMENT_SET`
- `MIXED`

Allowed `representation_source_status` values:

- `PRESENT_SOURCE`
- `INTENTIONALLY_ABSENT`
- `SOURCE_CORRUPT`
- `SOURCE_INCOMPLETE`
- `RECONSTRUCT_APPROVED`
- `REVIEW_REQUIRED`

Allowed `answer_choice_status` values:

- `NOT_APPLICABLE`
- `VISIBLE_SOURCE`
- `VISIBLE_PUBLISHED`
- `TRANSPARENTLY_ADAPTED`
- `RECONSTRUCT_APPROVED`
- `REVIEW_REQUIRED`

Allowed `status` values:

- `PASS`
- `REVIEW_REQUIRED`

Rules:

- `question_id` must be unique.
- Every question must have `question_recap_complete=true` in a standalone solution artifact.
- If `representation_dependency != NONE`, `representation_present_student`, `representation_legible`, and — for standalone solutions — `representation_present_solution` must be true.
- `answer_choice_status=REVIEW_REQUIRED` blocks release.
- `hint_progression_ok` must be true when H1-H3 are used.
- `method_distinct_from_answer` must be true.
- A quantitative/model-based solution should normally have both `method_has_why=true` and `method_has_executable_route=true`.
- `answer_present`, `math_typography_ok`, link checks, source-link check and `copy_paste_drift_check` must be true.
- `status=REVIEW_REQUIRED` blocks release.

## `question_bank_qa` — required for question-bank products

```json
{
  "questions_frozen": 61,
  "questions_published": 61,
  "unattemptable_questions": 0,
  "representation_dependency_failures": 0,
  "invisible_choice_failures": 0,
  "question_recap_failures": 0,
  "hint_progression_failures": 0,
  "method_answer_duplication_failures": 0,
  "method_reasoning_failures": 0,
  "solution_self_containment_failures": 0,
  "math_typography_failures": 0,
  "question_solution_link_failures": 0,
  "copy_paste_drift_failures": 0
}
```

Rules:

- `questions_frozen` must equal `questions_published`.
- Every defect counter must be zero.
- These counters summarize the per-question records; they do not replace them.

## `render_qa`

```json
{
  "all_pages_rendered": true,
  "clipped_core_objects": 0,
  "hidden_core_objects": 0,
  "overflow_findings": 0,
  "text_overlap_findings": 0,
  "component_bounds_escape_findings": 0,
  "critical_equation_collision_findings": 0,
  "unreadable_critical_labels": 0,
  "math_glyph_errors": 0,
  "broken_internal_links": 0,
  "unresolved_external_source_links": 0
}
```

All numeric defect counters must be zero for final certification.

The overlap counters are mandatory because a PDF can contain every required source token yet still be unusable when one component draws over another. Run `scripts/check_text_overlaps.py` on every generated PDF, then visually inspect the rendered pages. The deterministic script is a baseline gate, not a substitute for human inspection.

See `references/layout-collision-gate.md` for the reusable-component bounds contract and the reserve -> draw -> advance composition rule.

## `editorial_exceptions`

```json
{
  "exception_id": "ED-001",
  "source_id": "SRC-P044-EQN-01",
  "issue": "possible incorrect source answer",
  "status": "APPROVED",
  "approval_note": "user approved correction on 2026-09-08"
}
```

Allowed statuses:

- `APPROVED`
- `REVIEW_REQUIRED`
- `REJECTED`

Any `REVIEW_REQUIRED` exception blocks certification.

## Certification conditions

A manifest may declare publication-ready only when:

```text
all core source units accounted for
unmapped core units = 0
source-unit REVIEW_REQUIRED = 0
value additions replacing source = 0
unresolved references = 0
figure REVIEW_REQUIRED = 0
all question records PASS when product is a question bank
questions_frozen = questions_published
question-bank defect counters = 0
render QA defect counters = 0
text overlap findings = 0
component bounds escapes = 0
critical equation collisions = 0
editorial REVIEW_REQUIRED = 0
```

Use `scripts/check_publication_manifest.py` for a deterministic baseline manifest check, `scripts/check_text_overlaps.py` for layout collision preflight, and `scripts/check_math_typography.py` for source-notation leak preflight. None replaces visual or subject-matter QA.