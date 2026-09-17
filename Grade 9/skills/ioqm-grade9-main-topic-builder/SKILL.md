---
name: ioqm-grade9-main-topic-builder
description: Build one integrated IOQM Grade 9 main-topic learning package from official/validated source evidence using a single pedagogical owner and parallel research interfaces. Use for Number Theory, Algebra, Geometry or Combinatorics main-topic production when the learner has partial prior knowledge and the final product must include assimilation, first-step recognition, mastery/transfer, provenance and QA without fragmented multi-agent chapter authorship.
---

# IOQM Grade 9 Main-Topic Builder

## Purpose

This skill implements the IOQM Grade 9 core architecture and prevents the earlier multi-agent failure mode where independently strong subchapter books were concatenated into a weak global learner journey.

Core rule:

> `ONE MAIN TOPIC = ONE PEDAGOGICAL OWNER = ONE INTEGRATED STUDENT BOOK`

Parallel agents are evidence/research/QA producers. They do not independently own adjacent final student chapters.

## Required authorities

Read before work:

1. `../../Mathematics/IOQM/README.md`
2. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Core_Architecture_v1.md`
3. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Topic_Taxonomy_v1.md`
4. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Knowledge_Dependency_Map_v1.md`
5. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Method_Selection_and_Transfer_Map_v1.md`
6. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Coverage_Hardening_Overlay_v1.md`
7. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Proof_Strategy_Toolkit_v1.md`
8. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Source_Provenance_Contract_v1.md`
9. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Microstream_Interface_Schema_v1.md`
10. `../../Mathematics/IOQM/00_Architecture/IOQM_G9_Production_Gates_v1.md`
11. `../grade9-math/SKILL.md`
12. `../grade9-math-assimilation/SKILL.md`

Then read all main-topic-specific source coverage and prerequisite-owner interfaces.

The coverage overlay is binding within existing topic ownership. It does not create a new main topic. Generic proof modes are retrieved from the proof toolkit rather than recreated independently inside each topic.

## Learner model

Assume the learner may know around 50% of the school concept:

- formulas may be remembered;
- routine examples may be solvable;
- the hidden mechanism is not reliably recognized;
- nearby methods are confused;
- first-move independence and transfer are unstable.

Do not reteach from zero unless diagnostic evidence shows a prerequisite gap.

## Execution protocol

### Wave 0 — Lead architecture freeze

The main-topic lead must freeze before prose:

- scope boundary;
- official-syllabus relationship;
- Grade-9 prerequisite tags;
- validated historical source set;
- Knowledge Dependency Map;
- Method Selection Map;
- Transfer Map;
- coverage-hardening obligations that fall inside this topic's canonical ownership;
- proof modes to retrieve from the shared Proof Strategy Toolkit;
- canonical overlap owners;
- governing invariant/router;
- internal microstream split.

No integrated student prose before:

`WAVE0_ARCHITECTURE_FROZEN`

### Wave 1 — Parallel research interfaces

Each microstream agent must use `IOQM_G9_Microstream_Interface_Schema_v1.md`.

Allowed outputs:

- proofs/derivations;
- PYQ mapping;
- misconception diagnostics;
- close contrasts;
- first-move cues;
- H3->H0 candidate ladders;
- transfer/mastery candidates;
- source-integrity findings;
- independent mathematical checks.

Forbidden output:

- canonical standalone student chapter intended for concatenation.

### Wave 2 — Single-lead integrated Assimilation Book

The lead consumes interfaces as evidence and writes one coherent book in dependency order.

Required teaching choreography:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Requirements:

- teach each canonical concept once;
- use retrieval rather than reteaching later;
- cross microstream boundaries through explicit contrasts;
- preserve one vocabulary/notation system;
- make the governing router visible repeatedly;
- where a named theorem/bridge is owned under the coverage overlay, teach its hypotheses, meaning, decision boundary and diagnostic contrast rather than only naming it;
- retrieve generic proof modes from the shared toolkit and specialize only the mathematics owned by this topic;
- remove agent boundaries from the learner experience.

### Wave 3 — Integrated First-Step Reference

Create only after Wave 2.

Must cover the whole main topic:

- recognition atlas;
- phrase/structure decoder;
- decision router;
- first-step cards;
- theorem-hypothesis / proof-mode checks where natural;
- contrast strip;
- traps/checks;
- recognition-only drill;
- concise source-to-mechanism map.

Do not create separate First-Step books per microstream inside one main-topic student pack.

### Wave 4 — H0 mastery/transfer

Student first attempt contains no default method labels/hints.

Required sections:

- notice/recognize;
- first useful line;
- full mixed solve;
- same surface/different decision;
- changed-surface transfer;
- WHY-NOT/verification.

Where appropriate, mastery must distinguish theorem legality from theorem-name recall and examples/conjectures from completed proof.

### Wave 5 — Independent audit

A fresh reviewer independently checks:

- every promoted answer;
- proofs/derivations;
- theorem hypotheses and proof-mode legality;
- endpoints/domains/parity/integrality/degeneracy;
- source IDs and key status;
- dependency order;
- duplicated teaching;
- student-export hygiene.

### Wave 6 — Unified PDF/render

Use one render authority/template for the full main-topic pack.

Follow PDF production skill requirements. Inspect every rendered page.

Record:

- page counts;
- SHA-256;
- preflight result;
- student/teacher leakage result.

If a previously certified learner source changes, its old PDF hashes/custody are stale until a fresh render/preflight/page inspection closes again.

## Historical source contract

Stable question ID:

`IOQM-YYYY-QNN`

Initial validated corpus:

- IOQM 2023;
- IOQM 2024;
- IOQM 2025 September 7.

Never infer an official Grade-9-only syllabus or official topic weightage from these papers.

Every historical item keeps year/question provenance and source/key status.

Author-created material receives no historical ID.

## Main-topic issue contract

Use **one GitHub issue per main topic**.

The issue contains:

- full agent prompt;
- architecture links;
- source links;
- microstream list;
- dependency declarations;
- required outputs;
- gate checklist;
- current state.

Do not create child issues for every microstream unless a specific operational blocker requires it.

Cross-topic architecture hardening that deliberately leaves the 22 main-topic boundaries unchanged may use one architecture/change-control issue rather than inventing a pseudo-topic issue.

## Mandatory RCA-derived gates

Before promotion require:

1. no dependency inversion;
2. one governing topic model;
3. canonical overlap owner matrix;
4. coverage-hardening obligations inside the topic are satisfied;
5. generic proof strategy is retrieved, not duplicated as a second chapter;
6. no direct concatenation of agent prose;
7. deduplicated student teaching;
8. cross-microstream contrast pairs;
9. attempt before hints;
10. real H3->H0 fading;
11. one integrated First-Step layer;
12. H0 mixed mastery;
13. independent math/source/theorem-hypothesis audit;
14. student-export workflow scrub;
15. unified render authority;
16. final PDF preflight/render QA.

## Required output set

For one main topic produce:

```text
00_Concept_and_Dependency_Map.md
01_Source_Coverage_Map.md
02_Assimilation_Book.md
03_First_Step_Reference.md
04_Recognition_and_First_Line_Lab.md
05_Practice_and_Transfer_Bank.md
06_H0_Mastery_Test.md
Teacher_Diagnostic_Key.md
Item_Metadata.csv
QA.md
PDFs/
```

Microstream interfaces remain in an authoring-only folder and are not student exports.

## Completion state

Static success:

`BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

Keep these `NOT_RUN` until observed:

- classroom timing/readability;
- longitudinal retention;
- psychometric calibration;
- qualification probability;
- pass-mark/percentile claims.

## Final rule

If another agent cannot continue from the repository issue, architecture files, interfaces and QA without reading chat history, the handoff is incomplete.