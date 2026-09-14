# Physics Core1A Technical Publication Spec v1

## Purpose

Core1A is declarative-dominant deep teaching. For Medium and Hard Physics buckets, declarative depth must be technically visible, not expressed mainly as prose.

## Technical closure

When material to the capability, Core1A must include:

- formal notation for key quantities and frames;
- governing equations or transformations;
- diagrams/graphs/vector constructions that close major inferential jumps;
- visible intermediate steps in representative worked examples;
- model conditions / applicability;
- misconception contrast;
- sign, dimensional, physical or limiting-case checks;
- a problem-family method or decision structure.

For Hard buckets, a prose-only explanation is noncompliant when an expert solution requires a technical representation.

## Representation rule

Do not maximize the number of visuals. Instead:

> Every major inferential jump that materially benefits from a technical representation must receive an adequate one.

Examples include:

- vector triangle;
- component diagram;
- free-body diagram;
- trajectory/graph;
- event timeline;
- geometric projection;
- symbolic transformation table.

## Worked-example rule

A worked example must expose intermediate technical structure. Prefer forms such as:

`STEP | WHY THIS STEP | TECHNICAL WORKING`

rather than prose narrative followed by a final answer.

## Layout integrity

Production learner PDFs must use flow layout or another collision-safe composition strategy. Free-canvas text/figure overlays require explicit collision validation.

Every new layout must be rendered page-by-page and visually checked for:

- text/text overlap;
- text/figure overlap;
- clipped labels;
- broken equations/glyphs;
- header/figure collision.

Successful PDF generation is not a visual-preflight pass.

See:

- `../Blueprint/policy/technical-density-and-figure-contract.v1.json`
- `../Blueprint/policy/pdf-layout-integrity.v1.json`
