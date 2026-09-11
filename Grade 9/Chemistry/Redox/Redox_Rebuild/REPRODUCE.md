# Reproduction and rebuild route

## Current status

This Redox review folder is the first validation instance for the subject-wide Chemistry schema. Its existing learner PDFs predate the final two-file Appendix A/B/C contract and therefore require migration/regeneration before publication readiness.

The governing Chemistry contract is:

```text
1. Core Study Guide
   Appendix A — Core Practice
   Appendix B — Core Solutions
   Appendix C — Printable Handout

2. ExamSIDE Solution & Transfer Book
   concept segregation + badges + H0/H1-H3 + transfer + Core/source links + complete solutions
```

## Supported rebuild workflow

Use the Grade 9 skills in this order:

1. `grade9-source-grounding`
2. `grade9-chemistry`
3. `grade9-chemistry-topic-builder`
4. `grade9-redox-subtopic-book-builder` for Redox-specific reasoning
5. `grade9-subtopic-completeness-auditor`
6. `grade9-transfer-coverage-auditor`
7. `grade9-redox-chapter-closeout-auditor` when doing Redox chapter closeout
8. `grade9-chemistry-publication-review` for generic Chemistry publication/review gating

The supplied source authority is fingerprinted in `Source/Source_Fingerprint.json`; the frozen Redox external-corpus evidence is `Redox_ExamSIDE_Ledger.json`.

## Generic Chemistry package validation

Once a conforming `Chemistry_Publication_Package.json` and topic-delivery records have been generated, run:

```bash
python "Grade 9/skills/grade9-chemistry-publication-review/scripts/validate_chemistry_review_package.py" \
  "Grade 9/Chemistry/Redox/Redox_Rebuild" \
  "Chemistry_Publication_Package.json"
```

The validator is chapter-agnostic. It derives topic/artifact and external-corpus state from records and fails closed if the two-file contract, Appendix A/B/C, Appendix C handout, ExamSIDE support metadata, artifact identity or final eligible-placement evidence is incomplete.

## Reproducibility boundary

Do not treat fingerprints or review mirrors as repository artifact custody. Publication PASS still requires exact learner artifact bytes to be recoverable from repository/CI state or deterministically rebuilt by a committed model/renderer.

Technical PASS does not imply independent teacher approval, classroom effectiveness or psychometric validation.
