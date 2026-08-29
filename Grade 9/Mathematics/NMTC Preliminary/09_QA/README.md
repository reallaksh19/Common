# NMTC Bhaskara Preliminary — QA & Publication Authority Index

This directory separates **internal mathematical QA** from **publication/calibration evidence**.

## Global publication authority

- `NMTC_Preliminary_Publication_Gates.md` — normative PRELIM publication gates.
- `Cross_Package_Publication_Readiness_Matrix_v1.md` — current status across all ten packages + mock system.
- `Publication_Artifact_Split_Manifest_v1.md` — student vs teacher/export boundary.
- `Topic_Package_Production_Manifests_v1.md` — frozen source-level student/teacher projection for all ten packages.
- `Production_Notation_and_Render_Contract_v1.md` — deterministic notation/page/render requirements.
- `Classroom_Timing_Readability_Calibration_Protocol_v1.md` — how real timing/readability evidence must be collected.
- `Topic_Item_Metadata_Schema_v1.md` — machine metadata contract for topic banks.
- `Topic_Item_Metadata_Coverage_Ledger_v1.md` — explicit metadata indexing debt across all ten packages.

## Mixed mock authority

- `Mixed_Preliminary_Mock_System_QA.md` — 90-question mathematical/editorial second pass.
- `Mock_Item_Metadata_Validation_v1.md` — live-key reconciliation and machine-ledger validation.
- `Mock_Student_Render_QA_v1.md` — first actual student PDF/render inspection.
- machine ledger: `../08_Mixed_Preliminary_Tests/Mock_Item_Metadata_v1.csv`.
- schema: `../08_Mixed_Preliminary_Tests/Mock_Item_Metadata_Schema_v1.md`.

## Topic-package QA

Package-specific QA files remain the authority for internal mathematical completeness. Their `PASS_INTERNAL` status must not be interpreted as final publication approval.

## Current aggregate state

```text
TOPIC_PACKAGES_INTERNAL_COMPLETE = 10/10
MIXED_MOCK_SYSTEM_INTERNAL_COMPLETE = YES
MOCK_MACHINE_METADATA = PASS_STATIC
MOCK_STUDENT_TEACHER_SOURCE_SPLIT = PASS_STATIC
TOPIC_SOURCE_LEVEL_SPLIT = PASS_STATIC
PRODUCTION_NOTATION_CONTRACT = DEFINED
MOCK_STUDENT_LAYOUT_RENDER_QA = PASS_PREVIEW
MOCK_STUDENT_FINAL_NOTATION_QA = PARTIAL
MOCK_TEACHER_RENDER_QA = NOT_RUN
TOPIC_MACHINE_METADATA = NOT_RUN
CLASSROOM_TIMING_CALIBRATION = NOT_RUN
HISTORICAL_FIGURE_RECOVERY = PARTIAL/BLOCKED
2022_RECOVERY = BLOCKED_SOURCE
FINAL_PUBLICATION = NOT_READY
```

## Next valid work

1. normalize mock mathematical notation to final publication typesetting;
2. render/inspect teacher keys and re-run leakage checks;
3. populate topic-bank machine metadata, starting with mastery/transfer banks;
4. run classroom timing/readability pilots under the calibration protocol;
5. recover exact historical figures still required for canonical PYQ publication;
6. recover/qualify 2022 before any six-year recurrence claim.
