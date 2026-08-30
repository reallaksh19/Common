# IOQM Grade 9 — Production Gates v1

Status: `MANDATORY_STATIC_GATES`

These gates convert the multi-agent RCA into enforceable acceptance criteria.

## G0 — Source authority gate

PASS only if:

- current official competition/syllabus authority is identified;
- validated paper/key sources are linked;
- historical IDs are stable `IOQM-YYYY-QNN`;
- source/key statuses are explicit;
- no official Grade-9-only syllabus or weightage is invented.

## G1 — Dependency gate

PASS only if:

- Knowledge Dependency Map exists before student prose;
- every prerequisite is tagged `G9_CORE`, `IOQM_BRIDGE`, `JUST_IN_TIME_ADVANCED_LANGUAGE` or `DEFERRED`;
- no student section requires a concept canonically taught later;
- overlap concepts point to their canonical owner.

A prerequisite inversion is a blocking defect.

## G2 — Single governing model gate

PASS only if the main topic has one coherent learner-owned invariant/router connecting its microstreams.

A list of formulas or seven unrelated mini-chapters is not sufficient.

## G3 — Ownership/overlap gate

PASS only if every overlapping concept has one disposition:

- `CANONICAL_TEACHING_OWNER`
- `PREREQUISITE_RETRIEVAL_ONLY`
- `APPLICATION_ONLY`
- `CROSS_DOMAIN_BRIDGE`

Two independent full derivations of the same concept require explicit justification.

## G4 — Parallel-agent interface gate

PASS only if Wave-1 agents return the standard interface and do not publish canonical adjacent student chapters.

The lead must be able to inspect prerequisites, derivations, misconceptions, source anchors, contrasts, transfer candidates and QA without reverse-engineering another agent’s prose.

## G5 — Lead integration gate

PASS only if one pedagogical lead has authority to reorder, deduplicate and rewrite all microstream material.

Evidence of direct concatenation is a failure.

Checks:

- one learner voice;
- one terminology set;
- one dependency order;
- one teaching location per canonical concept;
- explicit transitions between mechanisms;
- retrieval instead of repeated onboarding.

## G6 — Deduplication gate

PASS only if repeated material is pedagogically deliberate.

Reject:

- repeated full definitions;
- repeated derivations;
- repeated concept maps;
- repeated learner contracts;
- repeated First-Step references for adjacent microstreams inside one main-topic book.

Allow:

- one-sentence retrieval cues;
- spaced retrieval questions;
- deliberate contrast revisits;
- end-of-topic integrated reference.

## G7 — Cross-boundary contrast gate

PASS only if the topic includes deliberate close contrasts that cross microstream boundaries.

Required minimum:

- narrow topic: 5;
- medium topic: 8;
- broad topic: 10.

Each contrast must state why the first move changes.

## G8 — Attempt-before-help and fading gate

PASS only if:

- student attempts H0 before seeing the route;
- hint architecture is `H3 -> H2 -> H1 -> H0`;
- later items actually remove support;
- worked-example density does not substitute for independent first moves.

## G9 — Integrated First-Step gate

PASS only if one main-topic First-Step Reference is produced **after** the integrated Assimilation Book.

It should compress the whole topic, not reproduce every microstream lesson.

## G10 — H0 mastery gate

PASS only if the final student mastery layer:

- contains no method labels by default;
- mixes microstreams;
- includes recognition, first-line, full-solve, contrast, transfer and WHY-NOT/verification items;
- requires final domain/parity/sign/attainment checks where relevant.

## G11 — Independent mathematics gate

PASS only if a fresh audit independently recomputes every promoted numerical answer and checks:

- algebra;
- domain;
- endpoints;
- degeneracy;
- parity/divisibility;
- integrality;
- geometric feasibility;
- recurrence/index conditions;
- source-key agreement.

A copied answer key is not an independent check.

## G12 — Source-custody gate

PASS only if:

- historical wording/key evidence is preserved;
- corrections are explicit;
- source conflicts are not silently repaired;
- author-created items have no fake year/question attribution;
- primary recurrence is not double-counted through bridge tags.

## G13 — Student-export hygiene gate

PASS only if the final student artifact removes authoring/control-plane leakage:

- GitHub issue/PR numbers;
- Wave labels;
- agent names;
- interface names;
- internal QA state;
- production-only source codes not needed for learning.

A concise source/provenance note may remain where pedagogically appropriate.

## G14 — One render authority gate

PASS only if the final topic PDFs use one production system for:

- fonts;
- mathematical notation;
- page size/margins;
- headings;
- First-Step boxes;
- hint boxes;
- tables;
- headers/footers;
- student/teacher distinction.

Agent-specific PDF styles must not leak into the final main-topic pack.

## G15 — Render/preflight gate

PASS only if:

- every page is rendered to an image and visually inspected;
- no clipping/overlap/broken glyphs;
- equations fit;
- diagrams are legible;
- tables do not overflow;
- student/teacher leakage is checked;
- PDF structural preflight passes;
- page count and SHA-256 are recorded.

## G16 — Transfer-quality gate

PASS only if promoted transfer is more than number substitution.

At least meaningful T2–T4 items must appear:

- representation change;
- context/domain change;
- discrete/continuous change;
- cross-domain bridge.

## G17 — Six-question ownership gate

For each major mechanism, student material must support:

1. What did I notice?
2. Why does the method work?
3. What clue triggers it?
4. What similar-looking problem needs a different method?
5. Can I write the first two useful lines unaided?
6. Can I solve a changed-surface version?

Correct calculation alone is not enough for mastery.

## G18 — Evidence-dependent gates

These remain `NOT_RUN` until evidence exists:

- classroom timing/readability;
- longitudinal retention;
- psychometric difficulty/discrimination;
- qualification probability;
- percentile/pass-mark calibration.

Do not promote static QA into human evidence.

## Gate summary states

Use:

- `ARCHITECTURE_BLOCKED`
- `WAVE0_ARCHITECTURE_FROZEN`
- `WAVE1_INTERFACES_COMPLETE`
- `WAVE2_INTEGRATED_ASSIMILATION_PASS`
- `WAVE3_FIRST_STEP_PASS`
- `WAVE4_H0_MASTERY_PASS`
- `WAVE5_INDEPENDENT_QA_PASS`
- `WAVE6_STATIC_RENDER_QA_PASS`
- `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`
- `PUBLICATION_READY` only after all required evidence/approval gates close.

## Main-topic handoff rule

At every state, another agent must be able to determine from the issue/PR:

- current frozen architecture;
- completed interfaces;
- canonical owner decisions;
- open source questions;
- exact files changed;
- QA performed;
- QA explicitly `NOT_RUN`;
- next allowed state.

No hidden chat history may be required to continue.