# IOQM Grade 9 — Validated Corpus

This folder contains the normalized historical corpus used to ground the Grade-9 pedagogical adaptation.

Current baseline:

- IOQM 2023 — 30 questions;
- IOQM 2024 — 30 questions;
- IOQM 2025 (7 September) — 30 questions;
- total — 90 stable IDs;
- independently recomputed answers — **90/90**;
- answer/key mismatches — **0**.

Files:

- `IOQM_2023_2025_90Q_Ledger_v1.csv` — question-level source/key/topic/mechanism metadata;
- `IOQM_2023_2025_Source_Coverage_Map_v1.md` — primary topic coverage and historical IDs;
- `IOQM_2023_2025_Taxonomy_Reconciliation_v1.md` — second-pass primary ownership and cross-domain rules;
- `IOQM_2023_2025_Corpus_Tagging_QA_v1.md` — structural/source-custody and answer-verification QA;
- `Verification/IOQM_Independent_Answer_Verification_Batch_A_Q01_Q10_v1.md` — Q01–Q10 × 3 years;
- `Verification/IOQM_Independent_Answer_Verification_Batch_B_Q11_Q20_v1.md` — Q11–Q20 × 3 years;
- `Verification/IOQM_Independent_Answer_Verification_Batch_C_Q21_Q30_v1.md` — Q21–Q30 × 3 years;
- `Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv` — authoritative 90-ID answer-verification overlay.

## Verification authority

The answer-verification overlay is authoritative for the independent-math status of each historical ID. The original detailed classifier ledger still retains its first-pass `answer_verified_independently=false` field to avoid a large silent rewrite; downstream tooling must join by stable `item_id` or use the consolidated QA state.

Two classifier/extraction strings require correction before exact-stem teaching use:

- `IOQM-2023-Q04`: validated paper has `x^4`, not `x/4`;
- `IOQM-2025-Q28`: validated paper has nested radical `√(x-√(x+a))=√a-y`.

These are repository metadata defects, not historical source conflicts. The source paper remains authority for exact wording and figures.

Primary recurrence counts use exactly one `main_topic_id` per question. Secondary tags are for pedagogy and transfer only; they must not silently inflate recurrence.

## Current state

`CORPUS_V1_STATIC_COMPLETE__90_OF_90_ANSWER_VERIFIED__NOT_CLASSROOM_CALIBRATED`

This state permits source-grounded main-topic production planning. It does not establish official IOQM weightage, classroom timing, psychometric difficulty, qualification probability, or publication readiness.