# Grade 4 English V2 — StudyDesign

StudyDesign closes the gap between task-level evidence and a self-teaching publication.

The canonical path is:

`source scan → QuestionEvidence → required learning objects → TeachingBlocks → publication`

## Why this layer exists

A worksheet question is an assessment obligation, not a complete lesson. The earlier V2 publication path could map one source question directly to one page and still claim `teach/model/practice/hints/verify = true`. That was structurally too weak.

StudyDesign makes instructional completeness explicit:

- `LearningObject` states what must be learned, its source obligations, capabilities, prerequisites and misconception targets.
- `TeachingBlock` contains the actual teaching/model/practice/hint/verification/rubric object.
- `source_coverage` may reference only real TeachingBlock IDs. Boolean coverage claims are not part of the contract.
- fresh independent evidence must be `H0`, answer-hidden and structurally separate from supported practice.
- source-boundary teaching remains source-derived; pedagogy may explain a boundary but may not invent a source category.
- open English responses use rubrics/evidence structures rather than exact-string answer truth.

## Coverage roles

Every required source obligation must resolve to at least one block for each role:

1. `teach_block_refs`
2. `model_block_refs`
3. `practice_block_refs`
4. `hint_block_refs`
5. `verify_block_refs`
6. `answer_or_rubric_block_refs`

The validator resolves every referenced ID, verifies its block type and checks that the block is actually grounded in the same source obligation.

## Publication boundary

Publication may choose layout, pagination and typography. It may not create missing teaching content, rules, hints, examples, misconception probes, rubrics or independent checks. If StudyDesign is incomplete, publication acceptance must fail rather than filling the gap in the renderer.
