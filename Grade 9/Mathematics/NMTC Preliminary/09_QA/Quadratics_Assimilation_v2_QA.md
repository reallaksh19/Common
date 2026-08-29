# Quadratics Assimilation v2 — QA Snapshot

## Scope

This QA covers the partial-knowledge assimilation redesign of the Quadratics teaching layer.

## Authoring gates

- generic partial-knowledge concept map: `PASS`
- Grade 9 Math skill integration: `PASS`
- Quadratics topic concept map: `PASS`
- Assimilation Book source: `PASS_INTERNAL`
- First-Step Reference source: `PASS_INTERNAL`
- source/provenance boundary: `PASS`
- known Vieta check value `(alpha-beta)^2` for `2x^2+x-4=0`: corrected to `33/4`

## Local PDF regeneration

Generated review artifacts:

- `Quadratics_Assimilation_Book_v2.pdf` — 9 A4 pages
- `Quadratics_First_Step_Reference_v2.pdf` — 4 A4 pages
- `Quadratics_Concept_Map_v2.pdf` — 1 A4 page

Static checks:

- proper mathematical typesetting: `PASS`
- page opens/render: `PASS`
- clipping/overlap/broken glyph inspection: `PASS`
- student/teacher pedagogy separation: `PASS`
- concept map readability: `PASS`
- PDF preflight openability/encryption/XFA/scan check: `PASS`

## Pedagogy checks

Required operational loop:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Verified in source:

- partial-prior-knowledge diagnostic: `PASS`
- missing-link teaching: `PASS`
- contrast/decision boundaries: `PASS`
- attempt before hint: `PASS`
- H0/H1/H2/H3 fading model: `PASS`
- independent first-move layer: `PASS`
- six-question assimilation test: `PASS`
- First-Step Reference treated as compression, not sole teaching layer: `PASS`

## Evidence-dependent gates

- classroom timing/readability calibration: `NOT_RUN`
- longitudinal student mastery evidence: `NOT_RUN`
- publication approval: `NOT_READY`
- 2022 Bhaskara Preliminary recovery: `BLOCKED_SOURCE_RECOVERY`

No unavailable calibration is represented as PASS.
