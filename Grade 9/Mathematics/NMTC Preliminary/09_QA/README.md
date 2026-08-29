# NMTC Bhaskara Preliminary — QA & Publication Authority Index

This directory separates **internal mathematical QA** from **publication/calibration evidence**.

## Global publication authority

- `NMTC_Preliminary_Publication_Gates.md` — normative PRELIM publication gates.
- `Cross_Package_Publication_Readiness_Matrix_v1.md` — current status across all ten packages + mock system.
- `Publication_Artifact_Split_Manifest_v1.md` — student vs teacher/export boundary.
- `Production_Notation_and_Render_Contract_v1.md` — deterministic notation/page/render requirements.
- `Classroom_Timing_Readability_Calibration_Protocol_v1.md` — how real timing/readability evidence must be collected.

## Mixed mock authority

- `Mixed_Preliminary_Mock_System_QA.md` — 90-question mathematical/editorial second pass.
- `Mock_Item_Metadata_Validation_v1.md` — live-key reconciliation and machine-ledger validation.
- machine ledger: `../08_Mixed_Preliminary_Tests/Mock_Item_Metadata_v1.csv`.
- schema: `../08_Mixed_Preliminary_Tests/Mock_Item_Metadata_Schema_v1.md`.

## Topic-package QA

Package-specific QA files remain the authority for internal mathematical completeness. Their `PASS_INTERNAL` status must not be interpreted as final publication approval.

## Current aggregate state

```text
TOPIC_PACKAGES_INTERNAL_COMPLETE = 10/10
MIXED_MOCK_SYSTEM_INTERNAL_COMPLETE = YES
MOCK_MACHINE_METADATA = PASS_STATIC
MOCK_STUDENT_TEACHER_SPLIT = PASS_STATIC
PRODUCTION_NOTATION_CONTRACT = DEFINED
CLASSROOM_TIMING_CALIBRATION = NOT_RUN
FINAL_RENDER_QA = NOT_RUN
TOPIC_PRODUCTION_MANIFESTS = NOT_RUN
HISTORICAL_FIGURE_RECOVERY = PARTIAL/BLOCKED
2022_RECOVERY = BLOCKED_SOURCE
FINAL_PUBLICATION = NOT_READY
```

## Next valid work

1. freeze package-by-package student/teacher production manifests;
2. render selected student/teacher artifacts and run the render contract;
3. run classroom timing/readability pilots under the calibration protocol;
4. recover exact historical figures still required for canonical PYQ publication;
5. recover/qualify 2022 before any six-year recurrence claim.
