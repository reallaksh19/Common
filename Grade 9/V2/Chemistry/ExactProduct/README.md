# Chemistry V2 C-L — Exact Product Quality Gate

This gate is the publication-quality firewall after C-K cold-start generation.

It binds machine evidence, exact PDF byte hashes, semantic custody, human reviews and final mature-design comparison without allowing any one class of evidence to impersonate another.

## Release sequence

```text
C-K frozen semantic candidate
-> exact Core1/Core2 PDF bytes + page/render evidence
-> machine exact-product gate
-> AI pre-review (advisory only)
-> authorized Chemistry subject review
-> authorized pedagogy review
-> authorized assessment review
-> authorized visual/usability review
-> frozen PR #157 mature-design comparison
-> V2_MATURE_INSTRUCTIONAL_PRODUCT
```

PR #157 is permitted only in the final comparison stage. It remains forbidden producer input.

## Quality states

Tracked independently:

- `PUBLICATION_ENGINEERING`
- `SUBJECT_CORRECTNESS`
- `PEDAGOGICAL_DESIGN`
- `ASSESSMENT_DESIGN`
- `VISUAL_USABILITY`
- `MATURE_DESIGN_QUALITY`
- `REFERENCE_COMPARABILITY`

Learning effectiveness is separate and defaults to `STUDY_REQUIRED`; a polished or human-approved PDF is not evidence of validated learning efficacy.

## Blocking semantics

The command-line evaluator uses:

```text
0 = exact product and all required release gates PASS
1 = technical/validation FAIL
2 = BLOCKED because exact artifacts or authorized manual gates are incomplete
```

Machine-green with missing authorized human review must return `2`, never `0`.

## Required topology

Exactly two learner-facing PDFs are supported:

1. Core Study Guide, containing main teaching plus Appendix A Core Practice, Appendix B Core Solutions and Appendix C Printable Handout.
2. ExamSIDE Solution & Transfer Book.

Appendix C is not emitted as a third required PDF.

## Current C-L boundary

The repository now defines and tests the machine quality firewall and exact-review custody semantics. Production mature status remains blocked until exact rendered Chemistry PDFs and authorized review attestations bound to those exact PDF hashes exist.
