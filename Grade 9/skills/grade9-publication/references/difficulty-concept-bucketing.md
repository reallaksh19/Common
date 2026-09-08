# Difficulty Badge + Concept Bucketing Control

Use this reference for long question banks, PYQ books, transfer books, and practice collections whenever questions already carry source difficulty and concept metadata or can be linked to a canonical concept index.

The control principle is:

> Preserve canonical source metadata internally; translate it into student-friendly navigation without giving away the reasoning task.

## 1. Preserve source difficulty; derive the learner badge

Never overwrite or discard the source difficulty code. Store both:

```text
source_difficulty_code
learner_difficulty_badge
```

Default deterministic mapping for this publication family:

```text
D1 -> EASY
D2 -> MEDIUM
D3 -> HARD
D4 -> CHALLENGE
```

If a source uses another scale, do not force this mapping. Record a project-specific mapping and obtain approval before scaling.

Do not silently re-grade a question. If editorial review suggests a different level, retain `source_difficulty_code`, add `editorial_difficulty_review`, and mark the change for approval.

## 2. Badge wording and color

The visible word is mandatory; color is secondary reinforcement only.

Recommended student-facing semantic palette:

```text
EASY       green family
MEDIUM     amber/yellow family
HARD       red/orange family
CHALLENGE  purple/dark accent family
```

Requirements:

- the word must remain readable in grayscale;
- do not communicate level by color alone;
- badge contrast must pass normal-view inspection;
- never show raw `D1/D2/D3/D4` as the dominant learner label when the approved product uses words;
- raw difficulty code remains in the audit/metadata model.

## 3. Preserve canonical concept linkage

Each question record must carry:

```text
primary_concept_id
primary_concept_title
secondary_concept_ids[]
concept_source
```

Prefer the supplied study-guide/concept index as canonical authority. Do not invent a competing concept taxonomy merely to make grouping easier.

If a question has a fine-grained source concept such as `M4B-C8`, also record its broad learner bucket, for example:

```text
fine_concept_id = M4B-C8
primary_concept_id = M-ST04B
```

The mapping must be source-supported or explicitly approved.

## 4. Assimilation vs mixed-transfer visibility

Concept metadata exists for every question, but it is not always shown before the attempt.

### Assimilation mode

Use when the learner is building or consolidating one concept.

Show:

```text
EASY / MEDIUM / HARD / CHALLENGE
M-STxx - readable concept title
```

The concept badge is scaffold.

### Mixed-transfer mode

Use after the relevant concepts have already been introduced.

Show:

```text
EASY / MEDIUM / HARD / CHALLENGE
CONCEPT - IDENTIFY FIRST
```

Do not reveal the canonical concept before the first attempt. The concept may be revealed in H1 or, preferably, after attempt in the method check.

Fail if mixed transfer prints the exact concept label above the problem and thereby gives away the central recognition decision.

## 5. Grouping model

Do not sort the whole book mechanically by difficulty or concept alone.

Recommended sequence:

```text
CONCEPT ASSIMILATION
same/bounded related concept family
EASY -> MEDIUM -> HARD -> selected CHALLENGE

then

MIXED TRANSFER
interleave previously introduced concepts
retain difficulty badge
hide concept before attempt

then

SPACED RETURN
bring earlier concepts back in later sets
```

For a long book, use 6-10 questions per set by default, fewer when graph/diagram/Challenge density is high.

A concept may have one primary home and secondary cross-links. Cross-links do not duplicate primary ownership.

## 6. Concept x difficulty matrix before repagination

Before final grouping, freeze a matrix such as:

```text
concept_id | EASY | MEDIUM | HARD | CHALLENGE | total
```

Use it to decide:

- which concepts deserve standalone assimilation sets;
- which sparse concepts should be combined into a coherent family;
- whether difficulty progression is balanced;
- which questions should be reserved for mixed transfer;
- whether the intended number of sets is realistic.

Do not decide set count from page aesthetics before the matrix is known.

## 7. Per-question required metadata

For question-bank publication, add these fields to every question record:

```text
question_id
source_difficulty_code
learner_difficulty_badge
difficulty_mapping_ok
fine_concept_id
primary_concept_id
primary_concept_title
secondary_concept_ids
study_mode = ASSIMILATION | MIXED_TRANSFER
concept_visible_before_attempt
set_id
```

Required invariants:

```text
D1 => EASY
D2 => MEDIUM
D3 => HARD
D4 => CHALLENGE
concept id preserved = true
concept title resolves = true
mixed transfer => concept_visible_before_attempt = false
assimilation => concept_visible_before_attempt = true unless explicitly designed otherwise
```

## 8. Student-facing ordering

Within an assimilation bucket, prefer increasing cognitive demand rather than raw source order:

```text
recognise/direct
-> routine application
-> inverse/multi-step application
-> representation/model selection
-> challenge/novel transfer
```

Do not force exact monotonic order when a prerequisite or figure dependency makes another sequence pedagogically clearer.

Within mixed-transfer sets, interleave concepts sufficiently that the learner must identify the model from the question itself. Avoid runs of several near-identical questions that reveal the answer strategy from adjacency.

## 9. Solution behavior

The method check always reveals the canonical concept after attempt:

```text
CONCEPT
M-STxx - readable title
```

Keep the existing assimilation structure:

```text
QUESTION RECAP
required figure/options/table
WHY THIS WORKS
METHOD
ANSWER / CHECK
CONCEPT TO KEEP
```

Difficulty remains visible in the method book, but the solution should not spend space defending the rating unless the user specifically requests difficulty rationales.

## 10. Release-blocking failures

Fail the batch when any of these occur:

```text
source difficulty lost or overwritten
learner badge does not match approved mapping
badge uses color without readable word
concept id invented or unresolved
concept title mismatched to concept id
question grouped under the wrong primary concept
mixed-transfer concept revealed before attempt
challenge question compressed into unreadable layout
concept x difficulty denominator does not reconcile with frozen question count
```

## 11. Audit counters

For a question bank using this system, final audit should include:

```text
difficulty_mapping_failures = 0
unresolved_concept_ids = 0
concept_title_mismatches = 0
primary_concept_ownership_conflicts = 0
mixed_transfer_concept_leaks = 0
question_grouping_failures = 0
```

Any non-zero value blocks publication certification.
