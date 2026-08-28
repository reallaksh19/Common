# NMTC Preliminary Scope and Source Policy

## 1. Target examination

Target only the **NMTC Junior / Bhaskara Preliminary (Screening) Test for Grades IX–X**.

Do not use Stage II / Final questions to set curriculum weight, question difficulty, expected solution length, archetype recurrence, timed-drill targets, or mock-paper composition.

Stage II may only be referenced later as explicitly labeled optional extension material.

## 2. Syllabus authority

Current Junior syllabus transcription supplied for this project:

### Algebra

- Quadratic and higher-degree algebraic equations
- Logarithms
- Remainder theorem
- Sequences and series
- Scales of notations
- Mathematical induction
- Basic inequalities

### Geometry

- Circle theorems
- Chords
- Arcs
- Angles in segments
- Cyclic quadrilaterals
- Tangents
- Intersecting chord theorem
- Apollonius theorem
- Alternate Segment theorem
- Stewart's theorem

### Number Theory

- Modular arithmetic
- Greatest Integer function
- Least Integer function

### Combinatorics

- Fundamental Principle of Counting
- Basics of permutations and combinations
- Pigeonhole principle
- Principle of inclusion and exclusion

This transcription must be reconciled to an exact official AMTI 2026 prospectus locator before being promoted to `P0_OFFICIAL_AMTI_ORIGINAL` inside the source ledger.

## 3. Preliminary evidence hierarchy

Use the strongest available source for each paper/question.

1. `P0_OFFICIAL_AMTI_ORIGINAL` — original AMTI paper/prospectus/key hosted or otherwise directly attributable to AMTI.
2. `P1_VERIFIED_FAITHFUL_REPRODUCTION` — reproduction independently matched against another complete copy/original evidence for the relevant content.
3. `P2_REPUTABLE_SECONDARY_ARCHIVE` — reputable archive but not independently matched.
4. `P3_PARTIAL_OR_UNVERIFIED_TRANSCRIPTION` — incomplete, image-dependent, transcription-damaged, truncated, or uncertain.

**P1 is not P0.** An independently matching coaching/institute copy may resolve wording/order/answers without becoming an official AMTI source.

## 4. Stable question IDs

Format: `NMTC-BH-P-YYYY-QNN`.

Do not encode a coaching-site page title into the stable mathematical ID.

## 5. Question fingerprint contract

Every question must record at least:

- stable ID;
- source provenance and locator;
- response format;
- scoring disposition (`SCORED`, `BONUS`, `UNKNOWN`);
- primary and secondary concepts;
- visible form;
- hidden structure / invariant;
- best first move;
- minimum expert solution path;
- tempting wrong move / trap;
- case or domain restrictions;
- Preliminary difficulty vector;
- archetype ID;
- source completeness/resolution status;
- solution authority;
- student-facing use classification.

## 6. Copyright-safe corpus policy

Prefer **question metadata, mathematical fingerprints, short descriptive summaries, derived solution paths, and source locators** rather than reproducing entire third-party paper pages verbatim.

Exact wording may be retained only when source rights and project policy permit it. Author-created foundation and transfer questions must be original and clearly labeled.

## 7. Curriculum weighting rule

Historical paper evidence answers which mechanisms recur, how concepts are disguised, what algebraic compression is expected, which traps recur, what topic combinations occur, and what objective/time-pressure patterns appear.

Historical frequency does **not** remove an explicit syllabus topic.

Use:

`syllabus authority + scored-PYQ recurrence + prerequisite dependency + transfer value`

for curriculum priority.

**Bonus questions do not enter ordinary scored recurrence or difficulty distributions.** They may still identify useful high-ceiling concepts if clearly labeled as bonus evidence.

## 8. Preliminary-specific pedagogy

Concept learning:

`SEE -> REALIZE -> UNDERSTAND -> ADOPT`

Performance learning:

`SEE -> RECOGNIZE -> FIRST MOVE -> SOLVE EFFICIENTLY -> CHECK -> TRANSFER`

The student must learn to identify the structure without being told the chapter label.

## 9. Source defect rule

Never silently repair a source defect. Record an explicit source/resolution state and retain before/after evidence.

Applicable defect classes include:

- missing figure;
- damaged notation;
- incomplete stem/options;
- internal mathematical conflict;
- webpage truncation;
- ambiguous answer/scoring disposition.

A question with unresolved defects may inform research but cannot be used as a clean canonical anchor.

## 10. Complete-paper / truncation rule

**Absence from a secondary webpage is not evidence that the paper ended there.**

A paper's total-question count may be promoted only when at least one of the following is available:

- original/complete paper with a clear end;
- complete answer key covering the terminal question;
- independent matching reproductions establishing the terminal question range.

The 2019 corpus is the motivating falsifier: the initial Cheenta page stopped at Q25, but independent recovery established Q26–Q30 and a 30-question answer key.

## 11. Bonus / scoring custody

Question existence and scoring status are separate facts.

Each item records `scoring_disposition` independently of `source_status`.

A bonus item:

- remains a real paper item if source-matched;
- may be mathematically analyzed;
- may become an explicitly labeled enrichment/bridge anchor;
- **must not** inflate ordinary scored frequency, paper-difficulty, or expected-time statistics.

2018 Q03/Q05/Q07 and 2019 Q20 are current examples.

## 12. Figure custody rule

A recovered textual solution or answer is **not equivalent to custody of the original figure**.

For image-dependent geometry/combinatorics:

- solution evidence may qualify the mechanism and answer;
- exact student-facing reconstruction remains blocked until the figure is recovered or independently verified;
- do not redraw an inferred figure and label it as the PYQ figure.

## 13. Source resolution rule

When independent evidence resolves a defect, record:

- prior defect;
- independent source locator/class;
- resolved wording/notation/scoring fact;
- whether canonical student use is now allowed;
- any remaining figure/source limitations.

Resolution must be explicit and auditable; never overwrite the history as though the defect never existed.
