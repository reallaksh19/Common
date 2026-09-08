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
  "render_qa": {},
  "editorial_exceptions": []
}
```

## `publication`

Required fields:

```json
{
  "source_file": "motion.pdf",
  "source_pages": 272,
  "published_pages": 180,
  "grade_band": "9",
  "subject": "Physics",
  "core_preservation_required": true,
  "benchmark_status": "APPROVED_PROTOTYPE"
}
```

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
render QA defect counters = 0
text overlap findings = 0
component bounds escapes = 0
critical equation collisions = 0
editorial REVIEW_REQUIRED = 0
```

Use `scripts/check_publication_manifest.py` for a deterministic baseline manifest check and `scripts/check_text_overlaps.py` for layout collision preflight. Neither script replaces visual/subject-matter QA.
