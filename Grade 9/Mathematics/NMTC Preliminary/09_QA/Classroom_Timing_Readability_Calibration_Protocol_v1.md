# NMTC Bhaskara Preliminary — Classroom Timing & Readability Calibration Protocol v1

## Purpose

This protocol defines how `CLASSROOM_TIMING_CALIBRATION` can move from `NOT_RUN` to evidence-backed status.

It deliberately does **not** invent timing thresholds, pass marks, percentiles, qualification probabilities, or psychometric claims before real student attempts exist.

## What is being calibrated

Calibration is not only total paper time. The useful observable chain is:

`READ -> RECOGNIZE -> FIRST MOVE -> EXECUTE -> CHECK -> FINAL ANSWER`

For each item, timing data should distinguish at least:

1. recognition latency;
2. first-move latency;
3. execution time after a valid first move;
4. check/review time;
5. abandonment/blank behavior.

## Required attempt record

For each student and question, record where feasible:

```text
mock_id
question_id
attempt_order
recognized_immediately: yes/no
first_move_correct: yes/no/unknown
first_move_latency_seconds
final_answer_correct: yes/no/blank
total_question_time_seconds
changed_answer: yes/no
confidence: low/medium/high
error_code: REC/FM/REP/ALG/DOM/CASE/COUNT/FIG/LOGIC/CHECK/TIME
readability_note: free text
```

No student identity is required in the curriculum repository; use an anonymized attempt ID if results are retained.

## Paper-level record

For each attempt retain:

- mock ID/version;
- date;
- supervised/unsupervised condition;
- allowed materials;
- total completion time;
- questions attempted/correct/wrong/blank;
- raw T24 training score;
- first-move accuracy;
- number of questions revisited;
- number of questions unfinished because of time;
- any wording/layout issue reported by the student or observer.

## Calibration sequence

### C0 — static editorial readiness

Before giving a paper to students:

- answer key rechecked;
- no package labels in student paper;
- no teacher diagnostic tags in student paper;
- notation unambiguous;
- all MCQ options mutually distinguishable;
- numeric questions specify the requested quantity;
- no hidden source/figure dependency;
- final render checked for clipping/overflow.

If C0 fails, do not interpret timing data because the paper itself is defective.

### C1 — pilot attempts

Use the paper under the intended training conditions and collect the required attempt record.

Do not alter questions during the same calibration series without changing the mock version.

### C2 — item review

Flag an item for editorial review when student evidence suggests one of these patterns:

- repeated correct mathematics but repeated misunderstanding of wording;
- long reading/recognition time disproportionate to the intended mechanism;
- multiple students identify the same ambiguity;
- a distractor is accidentally defensible;
- a numeric response has more than one reasonable representation not covered by the key;
- geometry labels are hard to reconstruct from text;
- correct students repeatedly miss a boundary because notation is visually unclear.

These are review triggers, not automatic proof that the mathematics is wrong.

### C3 — package diagnosis

Aggregate errors by mechanism code rather than only by chapter.

Examples:

- high `REC` -> recognition training weak;
- high `FM` with good recognition -> First-Step cards/labs need revision;
- high `REP` -> representation switching not stable;
- high `DOM` -> boundary/domain checking weak;
- high `TIME` after correct first move -> execution fluency problem;
- high `FIG` -> geometry marking/labeling problem.

### C4 — revision and retest

If an item is rewritten, increment its version or issue a new mock revision. Do not combine pre- and post-revision timing as if they came from the same item.

Retest with non-identical transfer where possible; do not simply rehearse the corrected answer.

## Readability audit questions

Observer/student comments should answer concrete questions:

- Did you know exactly what quantity was requested?
- Did any symbol/variable appear without definition?
- Did line wrapping change the meaning of an equation?
- Was a negative sign, exponent, floor/ceiling bracket, fraction or degree symbol easy to miss?
- Did an MCQ option appear duplicated/equivalent to another?
- Did the question require an unstated diagram?
- Was the amount of prose disproportionate to the mathematics?

## Timing interpretation guardrail

Do not freeze a question as “60-second”, “90-second”, “easy”, “hard”, or “qualifying level” from author judgement alone.

Until calibrated attempts exist, repository timing fields must be one of:

- `NOT_RUN`;
- `PILOT_DATA_AVAILABLE_NOT_FROZEN`;
- `CALIBRATED_FOR_TRAINING`.

`CALIBRATED_FOR_TRAINING` does not mean psychometrically validated or predictive of official NMTC qualification.

## Score interpretation guardrail

The mock raw score is a training score only:

`correct - 0.5 * wrong`

No pass mark is authorized by this protocol.

Use score jointly with:

- first-move accuracy;
- recognition latency;
- error-code distribution;
- completion record;
- blank/guess behavior.

## Calibration output file

Each completed calibration cycle should generate a versioned summary such as:

`09_QA/Calibration/Mock_A_Calibration_v1.md`

with:

- conditions;
- number of valid attempts;
- item-level descriptive timing summaries;
- ambiguity/readability findings;
- revisions made;
- items requiring retest;
- explicit limitations.

## Current state

```text
STATIC_PROTOCOL_DEFINED = YES
CLASSROOM_TIMING_CALIBRATION = NOT_RUN
PASS_MARK = NOT_DEFINED
PERCENTILE_MODEL = NOT_DEFINED
QUALIFICATION_PROBABILITY = NOT_DEFINED
```
