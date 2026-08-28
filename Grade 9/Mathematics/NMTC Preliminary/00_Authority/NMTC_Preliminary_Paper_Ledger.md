# NMTC Bhaskara Preliminary Paper Ledger

## Purpose

Track the actual Previous-Year Preliminary corpus used to ground the curriculum. This file records discovery and provenance; question-level mathematics belongs in `01_PYQ_Corpus/`.

## Current source evidence

| Paper | Stable paper ID | Source | Provenance | Observed reproduced structure | Corpus status |
|---|---|---|---|---|---|
| Bhaskara Screening 2025 | `NMTC-BH-P-2025` | Cheenta, `https://cheenta.com/nmtc-screening-test-bhaskara-contest-2025/` | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTED` |
| Bhaskara Screening 2024–2025 | `NMTC-BH-P-2024` | Cheenta, `https://cheenta.com/screening-test-bhaskara-contestnmtc-junior-level-ix-and-x-grades2024-2025/` | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTED` |
| Bhaskara Stage I 2023 | `NMTC-BH-P-2023` | Cheenta, `https://cheenta.com/bhaskara-contest-nmtc-junior-level-ix-and-x-grades-2023-problems-and-solutions/` | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTED` |
| Bhaskara Stage I 2022 | `NMTC-BH-P-2022` | Listed by Cheenta NMTC Resource Center | `P2_DISCOVERED_SOURCE_INDEX_AMBIGUITY` | resource index currently resolves Bhaskara link to 2023 page; paper not normalized | `BLOCKED_SOURCE_DISCOVERY` |
| Bhaskara Stage I 2019 | `NMTC-BH-P-2019` | Cheenta, `https://cheenta.com/bhaskara-contest-nmtc-primary-2019-ix-and-x-grades-stage-i-problems-and-solution/` | `P2_REPUTABLE_SECONDARY_ARCHIVE` | **25 questions**; Q1–15 options, Q16–25 fill-in | `SEED_FINGERPRINTED` |
| Bhaskara Stage I 2018 | `NMTC-BH-P-2018` | Cheenta, `https://cheenta.com/bhaskara-contest-nmtc-junior-2018-ix-and-x-grades-stage-i-problems-and-solution/` | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTED` |

Resource index: `https://cheenta.com/nmtc-past-papers-and-resources/`.

## Current corpus size

Five reproduced years are now question-slot normalized:

- 2018: 30
- 2019: 25
- 2023: 30
- 2024: 30
- 2025: 30

Total seed-fingerprinted question slots: **145**.

This is not yet a 145-question verified official corpus. All five current paper sources remain P2 secondary reproductions until independently matched to original/official evidence.

## Format finding

The available reproductions falsify any assumption that the historical Preliminary format is permanently fixed at 30 questions:

- 2018: 30
- 2019: 25
- 2023: 30
- 2024: 30
- 2025: 30

Therefore mock-paper format must be **versioned and evidence-driven**. A current mock profile may choose a current-like format, but must not call that format timeless or universal.

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
- `SEED_FINGERPRINTED` — all visible question slots have stable IDs and initial mechanism classification, but solutions/source verification may remain incomplete.
- `FINGERPRINTED` — all questions have the complete v1 schema fields and internally checked mathematical paths.
- `SOURCE_VERIFIED` — reproduction checked against an official/original or independent matching copy.
- `CURRICULUM_MAPPED` — all archetypes/prerequisites mapped to teaching products.

## Verification backlog

1. Locate an exact official AMTI 2026 prospectus URL and promote the syllabus only after exact comparison.
2. Locate official/original or independent copies for 2018, 2019, 2023, 2024 and 2025 and compare question order, figures, notation, and response format.
3. Resolve the 2022 Stage-I source-index ambiguity and ingest the actual Bhaskara paper.
4. Recover all image-dependent geometry/combinatorics questions; do not infer missing diagrams from text alone.
5. Resolve all seed-stage source conflicts/transcription defects before canonical use.
6. Independently derive answers and minimum expert paths; obtain answer-key evidence where available and keep its provenance separate.
7. Compute quantitative cross-year recurrence only after the seed classifications are solution-checked.
