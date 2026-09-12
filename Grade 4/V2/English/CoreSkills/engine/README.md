# Grade 4 English V2 CoreSkills Engine

The engine validates and composes already-normalized semantic evidence. It does **not** infer grammar rules, response structures, source categories, or teaching moves from raw prose.

A new scan must first be converted into explicit `QuestionEvidence` and, when relevant, `SourceModel` objects.

## Required discipline

- Raw prose alone is insufficient for deterministic authoring.
- Capability IDs, task-family IDs, response-structure IDs and representation IDs must exist in the registries.
- If a source word cannot be cleanly classified by the source taxonomy, keep a source-boundary status; do not add a category in this engine.
- Open-response judgement remains rubric/source/teacher based. The engine never compares free text to one model answer and calls that correctness.
- Optional learner evidence is carried separately from source truth.

Primary entry point: `author_core_skills(primary_input)`.
