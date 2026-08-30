# IOQM Grade 9 — Validated Corpus

This folder contains the normalized historical corpus used to ground the Grade-9 pedagogical adaptation.

Current baseline:

- IOQM 2023 — 30 questions;
- IOQM 2024 — 30 questions;
- IOQM 2025 (7 September) — 30 questions;
- total — 90 stable IDs.

Files:

- `IOQM_2023_2025_90Q_Ledger_v1.csv` — question-level source/key/topic/mechanism metadata;
- `IOQM_2023_2025_Source_Coverage_Map_v1.md` — primary topic coverage and historical IDs;
- `IOQM_2023_2025_Taxonomy_Reconciliation_v1.md` — second-pass primary ownership and cross-domain rules;
- `IOQM_2023_2025_Corpus_Tagging_QA_v1.md` — structural/source-custody QA.

Important gate:

`answer_verified_independently=false` is intentionally retained for all 90 rows until the independent recomputation batch is run. Capturing an official answer key is not the same as independently verifying the mathematics.

Primary recurrence counts use exactly one `main_topic_id` per question. Secondary tags are for pedagogy and transfer only; they must not silently inflate recurrence.
