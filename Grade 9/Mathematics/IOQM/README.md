# IOQM Grade 9 — Mathematics Architecture

## Scope

This workspace adapts the official IOQM mathematics scope for a Grade IX learner. It is **not** a claim that IOQM publishes a separate Grade 9 syllabus.

The official competition serves eligible students across multiple school classes. Grade 9 here is a pedagogical adaptation layer: prerequisites are staged so a student with partial school-level knowledge can assimilate Olympiad mechanisms without first completing all higher-class mathematics.

## Governing learning objective

Build a learner who can:

`UNDERSTAND -> RECOGNIZE -> CHOOSE -> FIRST MOVE -> SOLVE -> CHECK -> TRANSFER`

Deep teaching choreography:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Performance choreography:

`RECOGNIZE -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> TRANSFER`

## Four official-style domains used for curriculum organization

1. Number Theory
2. Algebra
3. Geometry
4. Combinatorics

Calculus and Statistics are out of scope for the current IOQM architecture unless future official source material changes the competition scope.

## Production granularity

The repository uses four levels:

- **PROGRAM** — IOQM Grade 9;
- **DOMAIN** — Number Theory / Algebra / Geometry / Combinatorics;
- **MAIN TOPIC** — one pedagogically coherent student unit;
- **MICROSTREAM** — an internal parallel research/verification stream inside a main topic.

### Non-negotiable ownership rule

`ONE MAIN TOPIC = ONE PEDAGOGICAL OWNER = ONE INTEGRATED STUDENT BOOK`

Microstream agents may research, classify PYQs, derive mathematics, propose contrasts, generate candidate transfer items, or independently audit answers. They must not independently publish adjacent student-facing chapters that are later concatenated.

This rule controls the failure mode observed in the earlier multi-agent Quadratics build: locally strong subchapters, but delayed integration, prerequisite inversion, repeated onboarding, overlapping concept ownership, and workflow leakage into the student artifact.

## Core architecture authority

Read in this order before creating any IOQM student material:

1. `00_Architecture/IOQM_G9_Core_Architecture_v1.md`
2. `00_Architecture/IOQM_G9_Topic_Taxonomy_v1.md`
3. `00_Architecture/IOQM_G9_Knowledge_Dependency_Map_v1.md`
4. `00_Architecture/IOQM_G9_Method_Selection_and_Transfer_Map_v1.md`
5. `00_Architecture/IOQM_G9_Source_Provenance_Contract_v1.md`
6. `00_Architecture/IOQM_G9_Microstream_Interface_Schema_v1.md`
7. `00_Architecture/IOQM_G9_Production_Gates_v1.md`
8. `../../skills/ioqm-grade9-main-topic-builder/SKILL.md`

## Validated corpus authority

Read `01_Corpus/` before opening any main-topic production issue.

Initial normalized corpus:

- IOQM 2023 — 30 questions;
- IOQM 2024 — 30 questions;
- IOQM 2025 (7 September) — 30 questions;
- total — **90 stable historical IDs**;
- independently recomputed answers — **90/90**;
- independent/key mismatches — **0**.

Current reconciled primary-domain classification:

- Number Theory — 24;
- Algebra — 18;
- Geometry — 25;
- Combinatorics — 23.

These are operational classifications of the three-paper seed corpus, **not official IOQM weightage**. The earlier rough pre-ledger split is superseded.

Corpus authority files:

1. `01_Corpus/IOQM_2023_2025_90Q_Ledger_v1.csv`
2. `01_Corpus/IOQM_2023_2025_Source_Coverage_Map_v1.md`
3. `01_Corpus/IOQM_2023_2025_Taxonomy_Reconciliation_v1.md`
4. `01_Corpus/IOQM_2023_2025_Corpus_Tagging_QA_v1.md`
5. `01_Corpus/Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv`
6. `01_Corpus/Verification/IOQM_2023_2025_Metadata_Correction_Overlay_v1.md`
7. three independent verification batch reports covering Q01–Q30 × all three years.

Every historical question uses stable ID:

`IOQM-YYYY-QNN`

and retains year/question provenance in downstream metadata.

### Two repository metadata corrections

The answer audit found two classifier/extraction defects, not historical source defects:

- `IOQM-2023-Q04`: validated paper has `x^4`, not `x/4`;
- `IOQM-2025-Q28`: validated paper has nested radical `√(x-√(x+a))=√a-y`.

Until the detailed classifier ledger is regenerated, the official/validated paper plus `IOQM_2023_2025_Metadata_Correction_Overlay_v1.md` controls exact-stem use for these IDs.

## Current gates

```text
CORE_ARCHITECTURE = COMPLETE_STATIC
CORPUS_90Q_SOURCE_KEY_CUSTODY = PASS_STATIC
CORPUS_90Q_PRIMARY_TAGGING = PASS_STATIC
TOPIC_COVERAGE_22_OF_22 = PASS_STATIC
ANSWER_KEY_VALUES_CAPTURED = 90/90
INDEPENDENT_ANSWER_RECOMPUTATION = PASS_STATIC_90_OF_90
ANSWER_KEY_MISMATCHES = 0
METADATA_EXTRACTION_DEFECTS = 2_ISOLATED
MEDIUM_CONFIDENCE_OVERLAP_REVIEW = PARTIAL / 41 ITEMS
DIFFICULTY_CALIBRATION = NOT_RUN
CLASSROOM_TIMING_READABILITY = NOT_RUN
PSYCHOMETRIC_CALIBRATION = NOT_RUN
```

The independently verified answers may now serve as answer-level historical teaching authority, provided future materials preserve exact paper wording/figures and source custody. This does not automatically validate any newly transcribed stem or derived solution prose.

## Production state

`CORPUS_V1_STATIC_COMPLETE__MAIN_TOPIC_PRODUCTION_PLANNING_READY`

The next static phase is to freeze main-topic production waves, overlap ownership and one-issue prompts. No main topic becomes publication-ready merely because architecture and corpus verification are complete; each must separately close source, pedagogy, mathematics, student-export and render gates.