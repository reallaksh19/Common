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

This rule is a direct control against the failure mode observed in the earlier multi-agent Quadratics build: locally strong subchapters, but delayed integration, prerequisite inversion, repeated onboarding, overlapping concept ownership, and workflow leakage into the student artifact.

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

## Baseline official/validated source set

Initial paper corpus:

- IOQM 2023 — validated paper/key source;
- IOQM 2024 — official HBCSE paper + answer key;
- IOQM 2025 — official HBCSE paper + final answer key.

Every historical question must use stable ID:

`IOQM-YYYY-QNN`

and must retain year/question provenance in all downstream metadata.

The paper corpus controls evidence and practice emphasis. It does **not** create an unofficial syllabus or official weightage claim.

## Publication state

`ARCHITECTURE_V1_DRAFT`

No topic is publication-ready merely because this architecture exists. Each main topic must separately close its source, pedagogy, mathematics, student-export and render gates.