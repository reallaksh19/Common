# IOQM Grade 9 — Mathematics Architecture

## Scope

This workspace adapts the official IOQM mathematics scope for a Grade IX learner. It is **not** a claim that IOQM publishes a separate Grade 9 syllabus.

The Grade-9 layer stages prerequisites so a student with partial school-level knowledge can assimilate Olympiad mechanisms without first completing all higher-class mathematics.

## Governing learning objective

`UNDERSTAND -> RECOGNIZE -> CHOOSE -> FIRST MOVE -> SOLVE -> CHECK -> TRANSFER`

Teaching choreography:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Performance choreography:

`RECOGNIZE -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> TRANSFER`

## Four curriculum domains

1. Number Theory
2. Algebra
3. Geometry
4. Combinatorics

Calculus and Statistics remain out of scope unless future official authority changes the competition scope.

## Production granularity

- **PROGRAM** — IOQM Grade 9;
- **DOMAIN** — four domains above;
- **MAIN TOPIC** — one pedagogically coherent student unit;
- **MICROSTREAM** — internal parallel research/verification stream.

### Non-negotiable ownership rule

`ONE MAIN TOPIC = ONE PEDAGOGICAL OWNER = ONE INTEGRATED STUDENT BOOK`

Microstream agents may research, classify PYQs, derive mathematics, propose contrasts, generate candidate transfer items or independently audit answers. They must not independently publish adjacent student-facing chapters that are later concatenated.

## Core architecture authority

Read in order:

1. `00_Architecture/IOQM_G9_Core_Architecture_v1.md`
2. `00_Architecture/IOQM_G9_Topic_Taxonomy_v1.md`
3. `00_Architecture/IOQM_G9_Knowledge_Dependency_Map_v1.md`
4. `00_Architecture/IOQM_G9_Method_Selection_and_Transfer_Map_v1.md`
5. `00_Architecture/IOQM_G9_Source_Provenance_Contract_v1.md`
6. `00_Architecture/IOQM_G9_Microstream_Interface_Schema_v1.md`
7. `00_Architecture/IOQM_G9_Production_Gates_v1.md`
8. `../../skills/ioqm-grade9-main-topic-builder/SKILL.md`

The 22-topic taxonomy and dependency graph are now frozen for v1 production. Changes require explicit architecture/change-control review.

## Validated corpus authority

Initial normalized corpus:

- IOQM 2023 — 30 questions;
- IOQM 2024 — 30 questions;
- IOQM 2025 (7 September) — 30 questions;
- total — **90 stable historical IDs**;
- independently recomputed answers — **90/90**;
- independent/key mismatches — **0**.

Primary-domain classification:

- Number Theory — 24;
- Algebra — 18;
- Geometry — 25;
- Combinatorics — 23.

These are operational classifications of this three-paper seed corpus, **not official IOQM weightage**.

Corpus authority lives under `01_Corpus/`, including source coverage, taxonomy reconciliation, QA, three independent verification batches, consolidated verification ledger and metadata-correction overlay.

Every historical item keeps stable ID `IOQM-YYYY-QNN`.

### Repository metadata corrections

Two classifier/extraction defects were found; neither is a historical source conflict:

- `IOQM-2023-Q04`: validated paper has `x^4`, not `x/4`;
- `IOQM-2025-Q28`: validated paper has nested radical `√(x-√(x+a))=√a-y`.

Exact-stem teaching use must consult the validated paper and correction overlay.

## Production control plane

Read `02_Production/README.md` and then:

1. `IOQM_G9_Main_Topic_Production_Waves_v1.md`;
2. `IOQM_G9_Canonical_Overlap_Ownership_v1.md`;
3. `IOQM_G9_Main_Topic_Prompt_Pack_v1.md`;
4. `IOQM_G9_Main_Topic_Issue_Registry_v1.md`.

All **22/22 main-topic production issues are open**:

- Wave 1: issues **#68–#76** — 9 canonical primitives, parallel-ready;
- Wave 2: issues **#77–#86** — 10 downstream topics, integrated prose waits for named prerequisite interfaces;
- Wave 3: issues **#87–#89** — 3 composite/cross-domain topics.

Downstream topics wait for a **stable prerequisite interface**, not necessarily the final upstream PDF.

## Current gates

```text
CORE_ARCHITECTURE = COMPLETE_STATIC
TOPIC_TAXONOMY_22 = V1_FROZEN_FOR_PRODUCTION
DEPENDENCY_MAP = V1_FROZEN_FOR_PRODUCTION_WAVES
CORPUS_90Q_SOURCE_KEY_CUSTODY = PASS_STATIC
CORPUS_90Q_PRIMARY_TAGGING = PASS_STATIC
TOPIC_COVERAGE_22_OF_22 = PASS_STATIC
ANSWER_KEY_VALUES_CAPTURED = 90/90
INDEPENDENT_ANSWER_RECOMPUTATION = PASS_STATIC_90_OF_90
ANSWER_KEY_MISMATCHES = 0
METADATA_EXTRACTION_DEFECTS = 2_ISOLATED
CANONICAL_OVERLAP_OWNERSHIP = FROZEN_FOR_PRODUCTION
MAIN_TOPIC_PRODUCTION_ISSUES = 22_OF_22_CREATED
WAVE_1 = READY_PARALLEL
WAVE_2 = WAIT_FOR_NAMED_INTERFACES
WAVE_3 = WAIT_FOR_NAMED_INTERFACES
DIFFICULTY_CALIBRATION = NOT_RUN
CLASSROOM_TIMING_READABILITY = NOT_RUN
PSYCHOMETRIC_CALIBRATION = NOT_RUN
```

## Program state

`CORPUS_V1_STATIC_COMPLETE__PRODUCTION_CONTROL_PLANE_READY__WAVE_1_READY_PARALLEL`

No topic is publication-ready merely because architecture, corpus and issue control are complete. Each main topic must independently close source, pedagogy, mathematics, student-export and render gates. Classroom timing, retention and psychometrics remain evidence-dependent.