# NMTC Bhaskara Preliminary Paper Ledger

## Purpose

Track the actual Previous-Year Preliminary corpus used to ground the curriculum. This file records discovery and provenance; question-level mathematics belongs in `01_PYQ_Corpus/`.

## Current source evidence

| Paper | Stable paper ID | Source | Provenance | Observed reproduced structure | Corpus status |
|---|---|---|---|---|---|
| Bhaskara Screening 2025 | `NMTC-BH-P-2025` | Cheenta | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTED` |
| Bhaskara Screening 2024–2025 | `NMTC-BH-P-2024` | Cheenta | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTED` |
| Bhaskara Stage I 2023 | `NMTC-BH-P-2023` | Cheenta | `P2_REPUTABLE_SECONDARY_ARCHIVE` | 30 questions; Q1–15 options, Q16–30 fill-in | `SEED_FINGERPRINTED` |
| Bhaskara Stage I 2022 | `NMTC-BH-P-2022` | Cheenta resource index | `P2_DISCOVERED_SOURCE_INDEX_AMBIGUITY` | index link currently resolves incorrectly; not normalized | `BLOCKED_SOURCE_DISCOVERY` |
| Bhaskara Stage I 2019 | `NMTC-BH-P-2019` | Cheenta truncated reproduction + Resonance 2019 Junior solution PDF + matching copies | `P1_VERIFIED_FAITHFUL_REPRODUCTION` for recovered structure/content; not AMTI-hosted | **30 questions**; Q1–15 options, Q16–30 fill-in | `SOLUTION_QUALIFICATION_ACTIVE` |
| Bhaskara Stage I 2018 | `NMTC-BH-P-2018` | Cheenta + independent AMTI-paper/solution reproduction | `P1_VERIFIED_FAITHFUL_REPRODUCTION` for matched items; not AMTI-hosted | 30 questions; Q1–15 options, Q16–30 fill-in | `SOLUTION_QUALIFICATION_ACTIVE` |

## Current corpus size

Five reproduced years are now question-slot normalized:

- 2018: 30
- 2019: 30
- 2023: 30
- 2024: 30
- 2025: 30

Total seed-fingerprinted question slots: **150**.

This is not yet a 150-question verified official corpus. P1 means independently matched faithful reproduction; only an exact AMTI original can be P0.

## 2019 truncation correction

The first Cheenta 2019 page used at seed stage ends after Q25. That led to a temporary, incorrect 25-question interpretation. Independent recovery from the Resonance-hosted 2019 Junior solution PDF and matching reproductions shows Q26–Q30 and an answer key through Q30.

**Rule strengthened:** absence from one secondary webpage is never evidence that a paper ended there. Paper-length claims require either a complete source or an independent end-of-paper match.

## Format evidence

All five currently normalized complete reproductions contain 30 questions with a 15+15 split. This is useful historical evidence for these years, but still does **not** justify calling 30 questions a timeless NMTC rule. Mock format must remain versioned to current/explicit evidence.

## Source-resolution findings

### 2018

An independent reproduction carrying the AMTI paper/solution text marks Q03, Q05 and Q07 as **BONUS**. Their apparently invalid multiple-choice options therefore must not be treated as ordinary scored-item defects or included in scored difficulty/frequency counts.

### 2019

Independent recovery:

- restores Q14's missing stem/options and identifies answer A (`126` impossible);
- confirms Q15's terminal term is `T × I`, not `T × 1`;
- marks Q20 as **BONUS**;
- recovers Q26–Q30 and their answer-key values (`97,25,122,12,61`).

## Official current-cycle evidence

AMTI's 58th NMTC 2026 exam portal identifies a Preliminary Test and a Final Test in the current cycle. The portal is cycle evidence, not a question-paper source.

## Historical official pattern evidence

The official AMTI 54th NMTC 2022 prospectus describes the Preliminary as an objective-type test evaluated by participating institutions using an AMTI-supplied key and states a historical difficulty intent. Do not assume those details unchanged for 2026 without current-cycle confirmation.

## Ingestion states

- `DISCOVERED` — source exists but has not been normalized.
- `SEED_FINGERPRINTED` — stable IDs + initial mechanism classification.
- `SOLUTION_QUALIFICATION_ACTIVE` — independent mathematical derivation/source matching in progress.
- `FINGERPRINTED` — complete v1.1 fields + internally checked paths.
- `SOURCE_VERIFIED` — reproduction checked against original or independent faithful match.
- `CURRICULUM_MAPPED` — archetypes/prerequisites mapped to teaching products.

## Verification backlog

1. locate an exact official AMTI 2026 prospectus locator;
2. resolve the actual 2022 Bhaskara Stage-I paper source;
3. recover all image assets needed for clean geometry/combinatorics anchors;
4. finish solution qualification for 2023–2025;
5. preserve bonus/non-scored disposition in recurrence statistics;
6. compute quantitative cross-year recurrence only from qualified scored items.
