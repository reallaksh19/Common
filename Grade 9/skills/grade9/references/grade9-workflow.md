# Grade 9 Operational Workflow

Use this reference for full multi-stage Grade 9 builds.

## Canonical pipeline

```text
Source/user request
  -> source grounding + QC
  -> subject fingerprint
  -> stable concept IDs + prerequisites
  -> difficulty calibration
  -> Core N bank
  -> Level-Up/challenge bank
  -> helpers/hints/misconceptions/diagnostics
  -> canonical master JSON
  -> textbook/question-bank/integrated publication
  -> content + render + link QA
```

## Defaults

- Core bank = 30 only when the user has not specified a count.
- Challenge bank = 20 only when the user has not specified a count.
- User counts override defaults.

## Source statuses

`VERIFIED_TRANSCRIPTION`, `RECONSTRUCTED`, `QC_ALERT`, `SOURCE_UNRESOLVED`.

Never silently correct source material. Preserve original statement/status and store verified corrections separately.

## Stable-ID contract

Every scored question has exactly one `primary_concept_id`. Use concept/question IDs as navigation authority; page numbers are render outputs.

## Difficulty contract

Treat difficulty as a cognitive vector. Same-level practice must preserve reasoning mechanism, recognition demand, representation demand, solution-path depth, and subject-specific demands. Scalar score is only a screening aid. Challenges should become harder through synthesis, not calculation clutter.

## Enrichment contract

Support recognition prompts, helpers, progressive hints, strategy, worked solution, misconception/error diagnosis, transfer, takeaway, and mastery evidence when requested.

## Linked publication contract

```text
Concept <-> practice <-> challenge <-> hints/answers <-> diagnosis <-> mixed test
```

Use purposeful page density, explicit work zones, and bidirectional links in integrated PDFs.

## Quality gates

- Source fidelity and QC
- Grade/scope appropriateness
- Concept coverage/prerequisites
- Difficulty calibration
- Bank count/variation/answer verification
- Enrichment/diagnostics
- Provenance
- Master-data integrity
- Publication render/link QA
