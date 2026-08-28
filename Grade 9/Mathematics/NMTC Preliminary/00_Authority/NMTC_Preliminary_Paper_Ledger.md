# NMTC Bhaskara Preliminary Paper Ledger

## Purpose

Track the actual Previous-Year Preliminary corpus used to ground the curriculum. This file records discovery and provenance; question-level mathematics belongs in `01_PYQ_Corpus/`.

## Current source evidence

| Paper | Stable paper ID | Source | Provenance | Observed structure | Corpus status |
|---|---|---|---|---|---|
| Bhaskara Screening 2025 | `NMTC-BH-P-2025` | Cheenta, `https://cheenta.com/nmtc-screening-test-bhaskara-contest-2025/` | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTING` |
| Bhaskara Screening 2024–2025 | `NMTC-BH-P-2024` | Cheenta, `https://cheenta.com/screening-test-bhaskara-contestnmtc-junior-level-ix-and-x-grades2024-2025/` | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTING` |
| Bhaskara Stage I 2023 | `NMTC-BH-P-2023` | Listed by Cheenta NMTC Resource Center | `P2_DISCOVERED_NOT_YET_INGESTED` | not yet normalized | `DISCOVERED` |
| Bhaskara Stage I 2022 | `NMTC-BH-P-2022` | Listed by Cheenta NMTC Resource Center | `P2_DISCOVERED_NOT_YET_INGESTED` | not yet normalized | `DISCOVERED` |
| Bhaskara Stage I 2019 | `NMTC-BH-P-2019` | Listed by Cheenta NMTC Resource Center | `P2_DISCOVERED_NOT_YET_INGESTED` | not yet normalized | `DISCOVERED` |
| Bhaskara Stage I 2018 | `NMTC-BH-P-2018` | Listed by Cheenta NMTC Resource Center | `P2_DISCOVERED_NOT_YET_INGESTED` | not yet normalized | `DISCOVERED` |

Resource index: `https://cheenta.com/nmtc-past-papers-and-resources/`.

## Official current-cycle evidence

AMTI's 58th NMTC 2026 exam portal identifies:

- Preliminary Test: 30 August 2026
- Final Test: 25 October 2026

Portal: `https://nmtc.amtionline.com/Account/Login`

This confirms the two-stage current cycle, but it is not itself a question-paper source.

## Historical official pattern evidence

The official AMTI 54th NMTC 2022 prospectus describes the Preliminary as an **objective type** test evaluated by participating institutions using an AMTI-supplied key and states a difficulty intent of approximately 20% moderate and 80% higher-level questions. This historical statement is useful as policy evidence, but must not be assumed unchanged for 2026 without current-cycle confirmation.

Locator: `https://amtionline.com/54th-NMTC-Prospectus-2022.pdf`

## Ingestion states

- `DISCOVERED` — a source exists but has not been question-normalized.
- `SEED_FINGERPRINTING` — stable question IDs and initial mechanism fingerprints are being created.
- `FINGERPRINTED` — all questions have minimum required mathematical metadata.
- `SOURCE_VERIFIED` — reproduction checked against an official/original or independent matching copy.
- `CURRICULUM_MAPPED` — all archetypes/prerequisites mapped to teaching products.

## Verification backlog

1. Locate an exact official AMTI 2026 prospectus URL and promote the syllabus only after exact comparison.
2. Locate official/original or independent copies for 2024 and 2025 and compare question order, figures, notation, and answer format.
3. Ingest 2023, 2022, 2019, and 2018 Screening papers.
4. Record image-dependent questions separately; do not infer missing geometry from text alone.
5. Obtain answer-key evidence where available and store key provenance separately from solution derivations.
