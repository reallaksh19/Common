# Mathematics V2 — Technical Depth and Page Composition Contract

This contract fixes a blueprint-level failure mode: mathematically valid content can still become a weak learner product if prose substitutes for mathematics, stages repeat one another, diagrams escape their intended viewport, or page budgets become page-count targets.

This is **not a PDF patch** and it is not a renderer style guide. The fix sits upstream of Publication.

```text
GOVERNED MATHEMATICS / QUESTIONS
        ↓
STAGE-SPECIFIC PEDAGOGY
        ↓
LearnerPageBlueprint
        ↓
TECHNICAL DEPTH GATE
        ↓
COMPOSITION / REPETITION / GEOMETRY GATE
        ↓
future PublicationBlueprint
        ↓
deterministic renderer
        ↓
rendered-artifact preflight
```

The renderer remains forbidden from inventing mathematics, hints, examples, diagrams, derivations, whitespace, or page breaks to make an artifact look complete.

## 1. Governing distinction

A page is justified by a **cognitive/mathematical job**, not by an available page allowance.

```text
PAGE BUDGET = CEILING
PAGE COUNT  = RESULT OF CONTENT
PAGE COUNT != DEPTH
```

Depth must be evidenced by mathematical obligations: objects, relations, derivations, representations, cases, counterexamples, verification, reconstruction and transfer. A long document with weak obligations is still shallow.

The architecture therefore does **not** use a target fill percentage or a minimum words-per-page metric. Those would reward layout gaming. It uses typed semantic blocks and required mathematical obligations instead.

## 2. No prose-only learner pages

Except for an explicit cover, every learner page must contain at least one typed technical block. Narrative or explanatory prose must bind to one or more mathematical references.

Examples of technical blocks include:

```text
DEFINITION
EQUATION
DERIVATION
DIAGRAM / GRAPH / TABLE
WORKED_EXAMPLE
CASE_ANALYSIS
COUNTEREXAMPLE
OPEN_TASK
TECHNICAL_WORKSPACE
ANSWER_DERIVATION
VERIFICATION
PROBLEM
HINT_LADDER
SOLUTION_CHAIN
WHY_MOVE_WORKS
WRONG_CHAIN
TRANSFER_CLASSIFICATION
```

Prose can connect these objects. Prose cannot substitute for them.

## 3. Stage-specific page grammar

### Core1 — basic notes

Compact mathematical orientation. A Core1 learner page must carry actual mathematics: definition, equation, diagram, worked example or case analysis. Core1 is not expanded to satisfy a page budget.

### Core1A — declarative teaching

A Core1A page may explain first, but the explanation must be attached to a mathematical object or transformation. The page must visibly teach through derivation, equation, representation, worked example, case analysis or counterexample.

For a MEDIUM bucket, depth is not satisfied merely by writing more explanation. The blueprint must explicitly satisfy:

```text
OBJECT_MODEL
PRIMARY_RELATION
RELATION_DERIVATION
PRIMARY_REPRESENTATION
REPRESENTATION_SYMBOL_BRIDGE
WORKED_ANCHOR
VALIDITY_OR_SPECIAL_CASE
MISCONCEPTION_COUNTEREXAMPLE
INDEPENDENT_CHECK
```

For HARD, the policy adds case analysis, failure mode, multi-representation translation and transfer obligations. Optional obligations such as an alternative method may be marked `NOT_APPLICABLE`, but only with an explicit reason. Required obligations may not be waived to create pages faster.

### Core1B — open-ended reconstruction

Core1B must not replay Core1A prose. Its page grammar is mathematically productive:

```text
OPEN_TASK
+ TECHNICAL_WORKSPACE
+ concept/representation help as needed
+ ANSWER_DERIVATION
+ VERIFICATION
```

The same MEDIUM bucket must additionally prove open reconstruction, representation rebuild, method/error contrast, faded reconstruction, independent use and answer verification.

Whitespace used as learner work area is represented as an explicit typed workspace. Blank area that exists only because the layout forced a page break is not a pedagogical object.

### Core2 — frozen questions

Core2 pages are compact. They carry the immutable source problem, the authored hint ladder and an answer/check path. Core2 does not acquire explanatory filler merely because other cores are longer.

### Core2A — solution apprenticeship

A substantive Core2A page must contain:

```text
PROBLEM
SOLUTION_CHAIN
WHY_MOVE_WORKS
WRONG_CHAIN
VERIFICATION
```

The source stem may repeat exactly when it is an immutable source object. The explanation around it must be newly authored for solution apprenticeship rather than copied from Core1A/Core1B.

### Core2B — transfer tutor

A substantive Core2B page must contain:

```text
PROBLEM
TRANSFER_CLASSIFICATION
TECHNICAL_WORKSPACE
ANSWER_DERIVATION
VERIFICATION
```

The learner is asked to identify structure and select a route before the answer is exposed. Core2B may not become Core2A with the paragraphs reordered.

## 4. Cross-core repetition is governed by lineage

A downstream stage may repeat only semantic identities that genuinely must remain identical:

```text
IMMUTABLE_SOURCE
CANONICAL_FORMULA
CANONICAL_DEFINITION
ANSWER_IDENTITY
```

Repeated narrative/explanatory prose across different cores is forbidden.

Every downstream reuse must declare an upstream reference and a transformation such as:

```text
BUILD
RECONSTRUCT
CONTRAST
SOLUTION_ANATOMY
TRANSFER
VERIFY
IMMUTABLE_CARRY
```

`IMMUTABLE_CARRY` is reserved for content whose identity must not change, such as a frozen source question. This prevents six products from becoming six differently titled copies of the same notes.

## 5. Representation geometry is semantic geometry

A diagram is not allowed to draw directly into unconstrained page coordinates.

Every learner-facing representation declares:

```text
representation_id
math_refs
semantic_geometry_refs
must_make_visible
must_not_imply
viewport
clip_to_viewport = true
```

All plotted geometry — including axes, perpendicular bisectors, loci, construction lines, tangent lines and graph curves — is clipped to the representation viewport before page composition.

Therefore a mathematical line may be infinite **semantically** while its learner-page drawing remains bounded to the graph box. Extending a locus line across a title, answer block or page margin is a composition failure, not an acceptable rendering of an infinite line.

The viewport itself must lie inside the page bounds.

## 6. Pagination and whitespace

Default pagination is `FLOW`.

A forced break is legal only as `PEDAGOGIC_BREAK` with an explicit reason, for example a new cognitive phase that must begin cleanly. Manual spacer padding is forbidden.

The architecture intentionally does not set a maximum percentage of white page area. White area may be useful for learner work. Instead, blank space must have one of two explanations:

```text
1. natural remainder produced by flow pagination; or
2. explicit learner workspace with a mathematical purpose.
```

The renderer may not insert spacer blocks to approach a page target.

## 7. Technical depth precedes layout

The `EASY / MEDIUM / HARD` badge first resolves depth obligations. Only after those obligations are satisfied does page composition occur.

```text
DIFFICULTY BADGE
      ↓
DEPTH OBLIGATIONS
      ↓
mathematical content / representations / tasks
      ↓
LearnerPageBlueprint
      ↓
page flow
```

Not:

```text
DIFFICULTY BADGE
      ↓
10 / 20 / 30 pages
      ↓
fill the pages
```

The existing `10 / 20 / 30` values remain maximum stage/bucket ceilings only.

## 8. Executable contract

Canonical files:

```text
TECHNICAL_COMPOSITION.md
contracts/math-learner-page-blueprint.schema.json
policies/math-technical-composition-policy.json
engine/validate_learner_page_blueprint.py
golden/technical_composition/01-medium-equidistant-page-blueprint.json
tests/test_technical_composition.py
```

The validator fails closed on:

- prose-only pages;
- missing stage-required mathematical blocks;
- manual spacer padding;
- unbounded representation geometry;
- representation viewports outside the page;
- open-tutor pages without explicit technical workspace;
- copied narrative/explanatory signatures across cores;
- repeated immutable content without explicit lineage;
- missing MEDIUM/HARD depth obligations;
- required depth obligations marked not applicable;
- fake flow pagination carrying a hidden forced-break reason.

## 9. Publication consequence

Publication must consume a validated `LearnerPageBlueprint`; it must not discover page structure itself.

Future rendered-artifact preflight should verify the implementation-level consequences of this contract: bounding boxes stay inside their declared viewport/content frame, required semantic blocks are present, and no renderer-added content or spacer blocks appeared.

The architecture is therefore split cleanly:

```text
MathBlueprint decides WHAT mathematical/cognitive material a page must contain.
Publication decides HOW that already-governed page is typeset.
Rendered-artifact audit verifies THAT the typesetting respected the blueprint.
```
