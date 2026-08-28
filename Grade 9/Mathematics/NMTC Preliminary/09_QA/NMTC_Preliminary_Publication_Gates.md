# NMTC Bhaskara Preliminary Publication Gates

A topic/chapter cannot be published merely because notes and questions exist.

## A. Scope gates

- `PRELIM-01 PRELIMINARY_ONLY` — Stage II material does not influence weighting, difficulty, mocks, or mastery targets.
- `PRELIM-02 SYLLABUS_CUSTODY` — each concept maps to explicit syllabus or documented cumulative prerequisite.
- `PRELIM-03 NO_FREQUENCY_OVERFIT` — historically rare syllabus topics are not deleted.

## B. PYQ source gates

- `PRELIM-04 PAPER_LEDGERED` — all known relevant Preliminary sources are in the paper ledger.
- `PRELIM-05 STABLE_IDS` — each ingested question has `NMTC-BH-P-YYYY-QNN`.
- `PRELIM-06 PROVENANCE_CLASSIFIED` — each source is P0/P1/P2/P3.
- `PRELIM-07 SOURCE_DEFECTS_VISIBLE` — missing figures/transcription conflicts are explicitly blocked.
- `PRELIM-08 NO_FAKE_OFFICIAL` — no author-created or secondary-source item is labeled official without evidence.

## C. Mathematical fingerprint gates

- `PRELIM-09 PRIMARY_SECONDARY_CONCEPTS` — concepts are identified beyond chapter name.
- `PRELIM-10 HIDDEN_STRUCTURE` — invariant/transformation is explicit.
- `PRELIM-11 FIRST_MOVE` — best first useful line/construction is recorded.
- `PRELIM-12 MINIMUM_PATH` — compact expert solution path is known.
- `PRELIM-13 TRAP_MODEL` — at least one plausible wrong move or boundary risk is captured where applicable.
- `PRELIM-14 ARCHETYPE` — question maps to a stable mechanism family.
- `PRELIM-15 DIFFICULTY_VECTOR` — recognition, first-move, reasoning, algebra, calculation, traps, and time-pressure are profiled.

## D. Teaching-grounding gates

- `PRELIM-16 CONCEPT_HOME` — every recurring archetype has an explicit Concept Book home.
- `PRELIM-17 FIRST_STEP_CARD` — recurring archetypes have recognition cues and first-move rules.
- `PRELIM-18 FOUNDATION_LADDER` — prerequisite/direct/disguised levels lead to the PYQ anchor.
- `PRELIM-19 VERIFIED_PYQ_ANCHOR` — a clean source question anchors the competency where available.
- `PRELIM-20 TRANSFER` — learner solves a non-identical problem preserving the invariant.
- `PRELIM-21 CONTRAST` — learner must reject a tempting but structurally wrong method.

## E. Preliminary performance gates

- `PRELIM-22 RECOGNITION_DRILL` — mixed questions test concept recognition without solving.
- `PRELIM-23 FIRST_LINE_DRILL` — learner writes only the first useful mathematical move.
- `PRELIM-24 SHORT_SOLVE` — compact execution is trained after recognition.
- `PRELIM-25 MIXED_UNLABELLED` — chapter labels are removed in mastery assessment.
- `PRELIM-26 CHECK_STRATEGY` — answer checking, sign/domain/case verification, and option elimination are trained where appropriate.

## F. Corpus completeness gates

- `PRELIM-27 YEAR_COVERAGE` — known available years are either ingested or explicitly listed as backlog.
- `PRELIM-28 QUESTION_COVERAGE` — each ingested paper has no silently skipped questions.
- `PRELIM-29 FIGURE_RECOVERY` — image-dependent questions are either recovered or remain non-canonical.
- `PRELIM-30 CROSS_YEAR_RECURRENCE` — frequency claims are generated only after multiple years are fingerprinted.

## G. Student-facing publication gates inherited from Grade 9 Mathematics

Applicable MSRU gates remain required, especially:

- no naked formulas;
- SEE before name;
- invariant explicit;
- representation translation;
- first-move independence;
- reconstruction;
- transfer in disguise;
- source traceability;
- no silent repair;
- transform before calculate;
- genuine ADOPT mastery.

## Status output

Each chapter must publish a machine/human-readable status such as:

```text
PYQ papers relevant: 6
PYQ questions mapped: 18/18
Clean anchors: 15
Image/source blockers: 3
Recurring archetypes covered: 7/8
First-step cards: 7/8
Transfer families: 6/8
Speed drills: 5/8

STATUS: NOT_READY
BLOCKER: MODULAR_POWER_CYCLE lacks non-identical transfer and timed recognition drill.
```

Only when all applicable gates pass:

`STATUS: NMTC_PRELIMINARY_PYQ_GROUNDED`
