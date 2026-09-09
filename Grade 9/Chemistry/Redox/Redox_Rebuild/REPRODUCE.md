# Reproduction and rebuild route

## Current reproducibility boundary

This review branch packages frozen source/corpus evidence, reviewed learner-PDF fingerprints, hashes and reusable skills. The exact learner PDF bytes are prepared locally but are not committed by this automated draft. The exact one-shot ReportLab generation scripts used during the interactive build are **not** yet committed as a deterministic build system, so byte-identical regeneration from repository files alone is **NOT_RUN**.

Do not interpret the file manifest as proof of deterministic regeneration.

## Supported rebuild workflow

Use the existing Grade 9 skills in this order:

1. `grade9-source-grounding`
2. `grade9-chemistry`
3. `grade9-redox-subtopic-book-builder`
4. `grade9-subtopic-completeness-auditor`
5. `grade9-transfer-coverage-auditor`
6. `grade9-redox-chapter-closeout-auditor`
7. `grade9-chemistry-publication-review` for review packaging and release-claim limits

The supplied source authority is fingerprinted in `Source/Source_Fingerprint.json`; the original source PDF is not committed in this draft. The frozen external-corpus result is `Redox_ExamSIDE_Ledger.json`.

## Package validation

Run:

```bash
python "Grade 9/skills/grade9-chemistry-publication-review/scripts/validate_redox_review_package.py" \
  "Grade 9/Chemistry/Redox/Redox_Rebuild"
```

The validator checks required files, PDF readability/page counts, embedded link counts, ledger totals and file hashes. It does not prove pedagogical effectiveness, source-page transcription fidelity beyond the stored audit, or external URL availability at the time of review.
