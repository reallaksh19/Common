# IOQM Grade 9 — Main-Topic GitHub Issue Template v1

Use one issue per main topic. Replace every `<...>` placeholder before opening the issue.

---

# `<MAIN_TOPIC_ID>` — `<MAIN_TOPIC_TITLE>`

## Role

Act as Grade IX mathematics teacher, Olympiad-foundation pedagogy designer, source custodian and main-topic integration lead.

You own the **whole learner journey** for this main topic. Internal microstreams may run in parallel, but they are research interfaces only. Do not create separate finished student books for each microstream and concatenate them later.

## Learner

Assume approximately 50% prior knowledge:

- school formulas/definitions partly known;
- routine questions partly solvable;
- hidden connections, method boundaries, first moves and transfer unstable.

## Required architecture — read first

1. `Grade 9/Mathematics/IOQM/README.md`
2. `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Core_Architecture_v1.md`
3. `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Topic_Taxonomy_v1.md`
4. `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Knowledge_Dependency_Map_v1.md`
5. `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Method_Selection_and_Transfer_Map_v1.md`
6. `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Source_Provenance_Contract_v1.md`
7. `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Microstream_Interface_Schema_v1.md`
8. `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Production_Gates_v1.md`
9. `Grade 9/skills/ioqm-grade9-main-topic-builder/SKILL.md`
10. relevant Grade-9 Math/assimilation skills and prerequisite-owner interfaces.

## Official/validated paper baseline

Use the source contract. Initial validated corpus:

- IOQM 2023;
- IOQM 2024;
- IOQM 2025 September 7.

Every historical item must retain stable ID `IOQM-YYYY-QNN`, source link and key status.

Do not claim an official Grade-9-only syllabus or official topic weightage.

## Main-topic boundary

`<WHAT IS INCLUDED>`

Explicit exclusions / canonical owners elsewhere:

`<WHAT IS EXCLUDED OR RETRIEVAL-ONLY>`

## Governing learner rule/router

Freeze one sentence/network that unifies the topic:

`<GOVERNING INVARIANT OR ROUTER>`

## Wave 0 — architecture freeze

Before prose create:

- Knowledge Dependency Map;
- Method Selection Map;
- Transfer Map;
- source coverage map;
- overlap/canonical-owner matrix;
- Grade-9 prerequisite tags;
- learner prior/half-knowledge/missing-bridge map;
- internal microstream split.

### Internal Wave-1 microstreams

Run in parallel after Wave 0:

- `W1-A — <...>`
- `W1-B — <...>`
- `W1-C — <...>`
- `<add as needed>`

Every stream uses `IOQM_G9_Microstream_Interface_Schema_v1.md`.

Do **not** create child issues for these streams by default.

Gate:

`WAVE0_ARCHITECTURE_FROZEN`

## Wave 1 — parallel evidence interfaces

Each stream must return:

- scope;
- prerequisite/half-knowledge model;
- derivation/invariant;
- representations;
- decision boundaries;
- misconceptions;
- first moves;
- H3->H0 plan;
- verified IOQM anchors;
- source-independent solution checks;
- contrast candidates;
- T2–T4 transfer candidates;
- dependency declarations;
- integration notes;
- QA status.

Gate:

`WAVE1_INTERFACES_COMPLETE`

## Wave 2 — one integrated Assimilation Book

Only the main-topic lead writes canonical student prose.

Use:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Requirements:

- dependency order, not agent order;
- canonical teaching once;
- retrieval later;
- one notation/voice;
- cross-stream contrast pairs;
- no production labels in student prose.

Gate:

`WAVE2_INTEGRATED_ASSIMILATION_PASS`

## Wave 3 — integrated First-Step Reference

One topic-wide compression layer after teaching:

- recognition atlas;
- phrase/structure decoder;
- decision tree/router;
- First-Step cards;
- contrast strip;
- recognition-only lab;
- traps/checks;
- source-to-mechanism map.

Gate:

`WAVE3_FIRST_STEP_PASS`

## Wave 4 — H0 mastery and transfer

Build one student paper with:

- notice/recognize;
- first-line-only;
- full mixed solve;
- same-surface/different-decision;
- changed-surface transfer;
- WHY-NOT/verification.

No method labels/hints during the first attempt.

Gate:

`WAVE4_H0_MASTERY_PASS`

## Wave 5 — independent mathematics/source/pedagogy QA

Fresh reviewer independently checks every promoted answer and all condition/source claims.

Also audit:

- no dependency inversion;
- no duplicate full teaching;
- no overlap-owner conflict;
- no fake PYQ IDs;
- no source/key silent repair;
- no student-visible Issue/PR/Wave/interface leakage.

Gate:

`WAVE5_INDEPENDENT_QA_PASS`

## Wave 6 — unified PDF production

One render authority creates:

- Concept Map;
- Assimilation Book;
- First-Step Reference;
- H0 Mastery;
- teacher/diagnostic key;
- complete learner pack where appropriate.

Render every page and inspect.

Record page counts and SHA-256 hashes.

Gate:

`WAVE6_STATIC_RENDER_QA_PASS`

## Required source files

```text
<topic-folder>/
├── 00_Concept_and_Dependency_Map.md
├── 01_Source_Coverage_Map.md
├── 02_Assimilation_Book.md
├── 03_First_Step_Reference.md
├── 04_Recognition_and_First_Line_Lab.md
├── 05_Practice_and_Transfer_Bank.md
├── 06_H0_Mastery_Test.md
├── Teacher_Diagnostic_Key.md
├── Item_Metadata.csv
├── QA.md
├── Authoring_Interfaces/
└── PDFs/
```

## Non-negotiable gates

- [ ] source authority verified
- [ ] dependency map before prose
- [ ] one governing model
- [ ] canonical overlap owners
- [ ] microstreams return interfaces, not final chapters
- [ ] single-lead integrated prose
- [ ] deduplicated teaching
- [ ] cross-stream contrast pairs
- [ ] attempt-before-hint
- [ ] H3->H0 fading
- [ ] one integrated First-Step layer
- [ ] H0 mixed mastery
- [ ] independent math/source audit
- [ ] student-export scrub
- [ ] unified render authority
- [ ] page-by-page PDF QA

## Evidence-dependent gates

Keep explicitly:

- classroom timing/readability: `NOT_RUN`
- longitudinal retention/transfer: `NOT_RUN`
- psychometric calibration: `NOT_RUN`
- qualification probability: `NOT_RUN`

unless real evidence is collected.

## Completion state

Target static completion:

`BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

## Handoff requirement

Another agent must be able to continue from the repository/issue without access to private chat history.