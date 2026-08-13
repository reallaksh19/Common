---
name: grade9-physics
description: Apply Grade 9 Physics model selection, representation translation, graph/vector reasoning, units, assumptions, experimental interpretation, physical validation, and difficulty calibration to textbooks and question banks. Use for motion, force, work/energy, gravitation, pressure, sound/waves, light, electricity, measurements, experiments, HOTS, and competitive-foundation physics within the Grade 9 learning workflow.
---

# Grade 9 Physics

Provide the subject-specific physical reasoning layer for the shared Grade 9 workflow.

## Physics fingerprint

For each question record as applicable:

- phenomenon;
- physical system;
- frame of reference;
- known and target variables;
- governing model/law;
- assumptions and model-validity conditions;
- verbal/diagram/graph/equation representations;
- required representation translations;
- units;
- minimum expert solution path;
- validation checks.

## Difficulty vector

Use 0-10 dimensions:

- `physical_model_selection`
- `conceptual_reasoning`
- `representation_translation`
- `vector_spatial_reasoning`
- `equation_construction`
- `experimental_data_reasoning`
- `constraints_cases`

Store separately:

- algebra burden;
- arithmetic burden;
- unit-conversion burden.

Long calculation alone must not make a candidate equivalent to a conceptually difficult anchor.

## Required solution structure

When quantitative:

1. identify the system;
2. state assumptions/model validity;
3. choose frame/sign convention where relevant;
4. represent the situation with diagram/graph/table if useful;
5. list knowns and unknowns;
6. select the governing law;
7. solve symbolically where practical;
8. substitute values with units;
9. check dimensions;
10. check sign, magnitude, limiting behavior, conservation, or graph consistency as relevant;
11. interpret the result physically.

## Representation principle

Treat translation among verbal, diagrammatic, graphical, and mathematical representations as a major source of difficulty. Two problems with identical formulas may not be same-level if one requires model/graph inference and the other gives the equation directly.

## Model-status metadata

Where useful classify scientific statements as:

- `EXACT_LAW`
- `IDEALIZED_MODEL`
- `EMPIRICAL_RULE`
- `QUALITATIVE_TREND`
- `APPROXIMATION`
- `SCHOOL_LEVEL_MODEL`

Record conditions/limitations so a school simplification does not become a later misconception.

## Physics misconceptions

Prefer causal models, e.g. `velocity zero -> acceleration zero`, treating action/reaction as forces on the same body, confusing mass and weight, treating graph height as distance when area/slope is relevant, or ignoring sign convention.

Use the shared question-bank and enrichment skills for calibration, hints, and diagnostics.
