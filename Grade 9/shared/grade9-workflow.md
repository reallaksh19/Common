# Grade 9 Reusable Learning-Production Contract

This shared contract is used by the Grade 9 skill family. The repository root `Grade9schema.md` remains the fuller human specification; this file keeps only the operational rules needed by skills.

## 1. Canonical build pipeline

```text
INPUT SOURCES / USER REQUEST
  -> source grounding and QC
  -> subject-specific fingerprint
  -> stable concept architecture
  -> difficulty calibration
  -> Core N question bank
  -> next-level challenge bank
  -> learning enrichment
  -> canonical master JSON
  -> student/question-bank/integrated publication
  -> content + link + visual QA
```

## 2. Default counts

- Core bank: 30 only when the user does not specify another count.
- Next-level appendix: 20 only when the user does not specify another count.
- User-specified counts always override defaults.

## 3. Source statuses

- `VERIFIED_TRANSCRIPTION`
- `RECONSTRUCTED`
- `QC_ALERT`
- `SOURCE_UNRESOLVED`

Never silently correct a source. Preserve source wording/status in provenance and store verified correction separately.

## 4. Provenance classes

- `USER_UPLOADED_ANCHOR`
- `OFFICIAL_PYQ`
- `SECONDARY_VERIFIED_PYQ`
- `PUBLISHED_REFERENCE`
- `ORIGINAL_CALIBRATED`
- `RECONSTRUCTED_FROM_SCAN`

## 5. Stable IDs

Use stable IDs rather than page numbers as the authority.

Typical forms:

```text
<CHAPTER>-C01       concept
Q01                 uploaded/source anchor
C21                 calibrated Core question
H01                 next-level challenge
M01                 misconception
T01                 mixed mastery test
```

Every scored question has exactly one `primary_concept_id` and may have secondary concepts.

## 6. Difficulty policy

Difficulty is a multidimensional cognitive profile. Subject skills define the most useful dimensions.

For same-level candidates:

- compare mechanism;
- compare recognition demand;
- compare reasoning-step depth;
- compare representation demand;
- compare constraint/case demand;
- compare subject-specific dimensions;
- use scalar score only as a screening aid.

For the generic Mathematics profile, a useful default screen is `anchor +/- 0.4`. Challenge questions should normally sit about `+0.8 to +1.3` above the anchor, primarily through synthesis rather than calculation clutter.

## 7. Core-bank selection

When the allowed number of new questions is limited, allocate them to concepts with:

- high recognition demand;
- high transfer value;
- weak source coverage;
- important misconceptions;
- prerequisite importance.

Do not create a fixed number of variants for every anchor unless the user requests it.

## 8. Enrichment contract

When enrichment is requested, support:

- concepts/prerequisites;
- recognition prompt (`What should I notice?`);
- helper;
- progressive hints;
- solution strategy;
- worked solution;
- misconception and diagnostic;
- transfer problem;
- takeaway;
- mastery evidence.

Helpers must not leak the full setup. Misconceptions must be specific wrong models, not generic cautions.

## 9. Linked publication contract

Preferred integrated architecture:

```text
Concept
  <-> Anchor / Core practice
  <-> Level-Up challenge
  <-> Hints / helper
  <-> Answer / solution
  <-> Misconception diagnosis
  <-> Mixed-test diagnosis
```

Generate destinations from stable IDs. Page numbers are publication outputs.

## 10. Student page-design rules

- Avoid report-like pages.
- Prefer compact concept hubs with mission, recognition, toolbox, first move, trap, try-now, level-up, exit ticket, and deliberate work zones.
- Aim for roughly 70-85% meaningful page occupancy on normal learning pages.
- Working space counts as meaningful only when explicitly intended and labelled.
- Do not put full bank solutions immediately beside first-attempt questions unless the product type requires it.

## 11. Quality gates

A full build is complete only when applicable gates pass:

- QG1 Source fidelity
- QG2 Source QC/reconstruction status
- QG3 Grade/scope appropriateness
- QG4 Concept coverage and prerequisites
- QG5 Difficulty calibration
- QG6 Bank count/variation and answer verification
- QG7 Helpers/hints/misconceptions/diagnostics
- QG8 Mastery and transfer
- QG9 Provenance
- QG10 Publication, render, and link QA

## 12. Master-data authority

All reusable outputs should be generated from canonical structured master data conforming to `grade9-master.schema.json` or a compatible extension. The PDF is a product, not the canonical database.
