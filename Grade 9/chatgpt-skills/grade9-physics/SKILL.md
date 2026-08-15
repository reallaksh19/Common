---
name: grade9-physics
description: Apply Grade 9 Physics model selection, representation translation, graph/vector reasoning, units, assumptions, experimental interpretation, physical validation, difficulty calibration, and concept-book pedagogy to textbooks and question banks. Use for motion, force, work/energy, gravitation, pressure, sound/waves, light, electricity, measurements, experiments, HOTS, competitive-foundation physics, and SEE -> REALIZE -> UNDERSTAND concept-book work.
---

# Grade 9 Physics

Use this skill as the subject-specific Physics reasoning layer for the Grade 9 learning workflow.

## Physics fingerprint

For each question or worked example, record as applicable:

- phenomenon and physical system;
- frame of reference / coordinate choice;
- known and target variables;
- governing model or law;
- assumptions and model-validity conditions;
- verbal, diagrammatic, graphical and mathematical representations;
- required representation translations;
- units;
- minimum expert solution path;
- validation checks.

## Difficulty profile

Use 0-10 dimensions:

- `physical_model_selection`
- `conceptual_reasoning`
- `representation_translation`
- `vector_spatial_reasoning`
- `equation_construction`
- `experimental_data_reasoning`
- `constraints_cases`

Keep algebra, arithmetic and unit-conversion burden separate. Long calculation alone does not make a problem conceptually difficult.

## Quantitative solution contract

When quantitative:

1. identify the system;
2. state assumptions/model validity;
3. choose frame/sign convention where relevant;
4. represent the situation with a useful diagram/graph/table/timeline;
5. list knowns, implicit knowns and target;
6. select the governing law;
7. solve symbolically where practical;
8. substitute values with units;
9. check dimensions;
10. check sign, magnitude, limiting behavior, conservation or graph consistency as relevant;
11. interpret the result physically.

Treat translation among words <-> diagram <-> graph <-> equation as a major source of difficulty.

## Model-status metadata

Where useful classify statements as `EXACT_LAW`, `IDEALIZED_MODEL`, `EMPIRICAL_RULE`, `QUALITATIVE_TREND`, `APPROXIMATION`, or `SCHOOL_LEVEL_MODEL`. Record limitations so a school simplification does not become a later misconception.

## Physics misconceptions

Prefer causal misconception models such as `velocity zero -> acceleration zero`, confusing mass and weight, treating graph height as distance when slope/area is relevant, or ignoring sign convention.

## Concept-book mode

For a Physics Concept Book, read `references/concept-book-see-realize-understand.md` before authoring.

Core learning sequence:

`SEE THE EQUATION -> REALIZE -> UNDERSTAND -> CONNECT`

`CONNECT` is traceability/navigation, not a fourth cognitive stage.

Required behavior:

1. Ground concept architecture to the supplied source/questions before drafting.
2. Maintain a source-coverage ledger; no source question may be orphaned.
3. Do not introduce a naked equation. Establish a physical situation, chalkboard sketch, diagram, graph, numerical pattern, timeline, experiment, area model or thought experiment first.
4. In `REALIZE`, explain the physical meaning of every term and require a plain-language statement of the equation.
5. In `UNDERSTAND`, include as applicable:
   - derivation or reconstruction;
   - assumptions and validity conditions;
   - frame/sign convention;
   - dimensional/unit check;
   - limiting and special cases;
   - graph equivalence;
   - proportional/scaling reasoning;
   - misconception contrast;
   - prediction before calculation;
   - transfer to unfamiliar source-style questions.
6. Grade 9 depth must extend beyond elementary intuition. Require symbolic reasoning, representation translation, model selection, proportional reasoning and reconstruction from earlier principles where the concept permits.
7. Preserve ambiguity, defects and missing assumptions in source material explicitly. Never silently repair source authority.
8. Use source question IDs in each `CONNECT` section when source IDs exist.
9. Explain unusual mathematical features such as `1/2`, `t^2`, squared velocity, negative signs, square-root scaling and nth-interval subtraction.
10. Success criterion: the learner can recognize, explain, reconstruct, predict and transfer.

For Motion in a Straight Line, read `references/motion-concept-book-example.md` as the worked exemplar.

## Linked learning products

- Concept Book: `SEE -> REALIZE -> UNDERSTAND`
- First-Step Reference: `SEE THE STORY -> WRITE -> CHOOSE`
- Question Bank: `RECOGNIZE -> SOLVE -> CHECK -> TRANSFER`

Use `grade9-question-bank` and `grade9-learning-enrichment` when calibration, hints, misconceptions, diagnostics or mastery evidence are required.

## Publication handoff

When concept content is sent to publication:

- preserve the SEE -> REALIZE -> UNDERSTAND sequence visually;
- use math-capable fonts with complete glyph coverage for superscripts, subscripts, arrows, Greek letters and operators;
- reject missing-glyph boxes, symbol substitutions, clipped equations or low-resolution rasterized mathematics;
- verify equation legibility at normal A4 reading size;
- retain concept/source traceability in authoring metadata.
