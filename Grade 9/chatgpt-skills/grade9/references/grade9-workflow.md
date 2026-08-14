# Grade 9 Operational Workflow

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

Defaults: Core 30 and Challenge 20 only when the user specifies no count. User counts override defaults.

Source statuses: `VERIFIED_TRANSCRIPTION`, `RECONSTRUCTED`, `QC_ALERT`, `SOURCE_UNRESOLVED`.

Every scored question has exactly one `primary_concept_id`. Concept/question IDs are navigation authority; page numbers are render outputs.

Difficulty is a cognitive vector. Scalar scores are screening aids only. Same-level items must preserve reasoning mechanism, recognition and representation demands, solution-path depth, and subject-specific demands. Challenges should become harder through synthesis rather than calculation clutter.

Support recognition prompts, helpers, hints, strategy, worked solutions, misconception/error diagnosis, transfer, takeaways, and mastery evidence when requested.

Linked publication: `Concept <-> practice <-> challenge <-> hints/answers <-> diagnosis <-> mixed test`.
