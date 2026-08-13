---
name: grade9-source-grounding
description: Extract, verify, classify, and preserve Grade 9 source material from uploaded PDFs, scans, notes, worksheets, screenshots, pasted notes, official papers, and web references. Use before building source-grounded textbooks or question banks, especially when notation may be ambiguous, when exact provenance matters, or when source defects must be separated from verified corrections.
---

# Grade 9 Source Grounding

Establish a reliable source layer before enrichment or question generation.

## Required source statuses

Assign each extracted item one status:

- `VERIFIED_TRANSCRIPTION` — faithful and clear.
- `RECONSTRUCTED` — scan/notation ambiguity required an explicit reconstruction.
- `QC_ALERT` — source is internally inconsistent, mathematically/scientifically defective, or likely misprinted.
- `SOURCE_UNRESOLVED` — do not use as a scored item until resolved.

## Provenance classes

Use one of:

- `USER_UPLOADED_ANCHOR`
- `OFFICIAL_PYQ`
- `SECONDARY_VERIFIED_PYQ`
- `PUBLISHED_REFERENCE`
- `ORIGINAL_CALIBRATED`
- `RECONSTRUCTED_FROM_SCAN`

Do not merge these classes into a generic `source` label in master data.

## Workflow

1. Inspect rendered pages/images when the source is visual or scanned.
2. Transcribe notation faithfully; do not normalize away meaningful wording.
3. Record source page/question identifiers.
4. Check signs, superscripts, subscripts, inequalities, brackets, units, logarithm bases, summation limits, diagrams, labels, and answer attainability.
5. Recalculate source worked examples when they will be reused as instructional or scored material.
6. If outside verification is requested or necessary, keep the verified result separate from the source statement.
7. Emit structured source records for downstream concept/question work.

## Source fidelity rule

Never silently replace the source with a corrected version.

Use a record such as:

```json
{
  "source_statement": "...",
  "transcription_status": "QC_ALERT",
  "verified_statement": "...",
  "verification_basis": "independent calculation / official source",
  "student_display_policy": "show corrected version with QC note"
}
```

## External research hierarchy

When web research is part of the request, prefer:

1. official curriculum/exam/mark-scheme sources;
2. government or academic learning platforms;
3. recognized textbooks or education repositories;
4. secondary mirrors for discovery only unless independently verified.

Do not bulk-copy commercial question banks. Retrieve for provenance and calibration, then prefer official/public questions or original calibrated questions.

## Output contract

Provide downstream skills with:

- source inventory;
- anchor records;
- transcription/QC status;
- provenance class;
- verified answer where applicable;
- unresolved issues;
- source-to-concept clues without assigning final concept IDs unless requested.
