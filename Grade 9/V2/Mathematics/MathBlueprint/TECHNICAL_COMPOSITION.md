# Mathematics V2 — Technical Depth and Page Composition Contract

This contract fixes a blueprint-level failure mode: mathematically valid content can still become a weak learner product if prose substitutes for mathematics, stages repeat one another, diagrams escape their intended viewport, or page budgets become page-count targets.

This is **not a PDF patch** and it is not a renderer style guide. The fix sits upstream of Publication.

```text
GOVERNED MATHEMATICS / QUESTIONS
        ↓
STAGE-SPECIFIC PEDAGOGY
        ↓
TECHNICAL DEPTH OBLIGATIONS
        ↓
RECONSTRUCTABLE TTUs
        ↓
LearnerPageBlueprint
        ↓
COMPOSITION / REPETITION / GEOMETRY GATE
        ↓
future PublicationBlueprint
        ↓
deterministic renderer
        ↓
rendered-artifact preflight
```

The renderer remains forbidden from inventing mathematics, hints, examples, diagrams, derivations, missing parts, whitespace or page breaks to make an artifact look complete.

## 1. Governing distinction

A page is justified by a **cognitive/mathematical job**, not by an available page allowance.

```text
PAGE BUDGET = CEILING
PAGE COUNT  = RESULT OF CONTENT
PAGE COUNT != DEPTH
```

Depth must be evidenced by mathematical obligations: objects, relations, derivations, representations, cases, counterexamples, verification, reconstruction and transfer. A long document with weak obligations is still shallow.

The architecture therefore does **not** use a target fill percentage or a minimum words-per-page metric. Those would reward layout gaming. It uses typed semantic blocks, reconstructable technical units and required mathematical obligations instead.

## 2. Reconstructable TTUs are mandatory

A TTU is treated here as a **reconstructable technical unit**: a bounded mathematical object whose learner-facing form is deliberately incomplete, whose missing structure is chosen upstream for a cognitive reason, and whose completed form is independently checkable.

Typical TTUs include:

```text
incomplete diagram
component model
incomplete graph
equation skeleton
event line
table skeleton
proof/reasoning chain
coordinate model
flow model
construction sequence
```

A picture with a blank box is not automatically a TTU. Every TTU must declare:

```text
ttu_id
kind
math_refs
given_parts
missing_parts
target_relations
reconstruction_prompt
completion_key
verification_refs
fading_level
source_ttu_ref / lineage_transform
viewport + clip_to_viewport
```

The key invariant is:

```text
COMPLETE TECHNICAL OBJECT
        ↓ choose cognitively meaningful omissions
LEARNER-FACING INCOMPLETE OBJECT
        ↓ learner reconstructs
COMPLETED OBJECT
        ↓
MATHEMATICAL VERIFICATION
```

The renderer may **not** choose which parts to omit and may not silently complete a TTU. Missing parts are instructional semantics, not layout decoration.

### TTU fading

TTUs use an explicit support ladder:

```text
MODELLED → GUIDED → FADED → INDEPENDENT
```

A downstream TTU may preserve or remove support; it may not increase support without a new governed decision. This prevents an open-ended product from quietly becoming more scaffolded than its declarative parent.

### TTU lineage across the cores

The same technical object should evolve rather than be re-described in prose.

```text
Core1A
build / model a reconstructable TTU
        ↓
Core1B
reconstruct the same TTU with more structure missing

Core2A
expose solution anatomy through a reconstructable TTU
        ↓
Core2B
transform that TTU under changed surface / representation / target
```

For example, a coordinate-geometry subtopic may use:

```text
Core1A  incomplete right-triangle diagram
        given A, B and the axis; reconstruct P and both distance components

Core1B  faded version of the same diagram
        reconstruct P, the distance equations and the locus

Core2A  equation skeleton
        reconstruct first move → equal-distance equation → reduced equation

Core2B  transformed equation skeleton
        recover the hidden geometry from an unfamiliar equation before solving
```

Core1B TTUs must name a Core1A TTU as their lineage source. Core2B TTUs must name a Core2A TTU. `RECONSTRUCT`, `CONTRAST` and `TRANSFER` describe the permitted downstream transformation instead of copying explanatory text.

For `HARD` Core1A/Core1B buckets, one reconstructable TTU is insufficient: multiple TTUs are required so that more than one representation or technical object must be rebuilt.

## 3. No prose-only learner pages

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

## 4. Stage-specific page grammar

### Core1 — basic notes

Compact mathematical orientation. A Core1 learner page must carry actual mathematics: definition, equation, diagram, worked example or case analysis. Core1 is not expanded to satisfy a page budget.

### Core1A — declarative teaching

A Core1A page may explain first, but the explanation must be attached to a mathematical object or transformation. The page must visibly teach through derivation, equation, representation, worked example, case analysis or counterexample.

Core1A must also contain reconstructable TTUs. Declarative does **not** mean passive. The complete method may be taught first, but the learner must then rebuild at least one technical object.

For a MEDIUM bucket, depth is not satisfied merely by writing more explanation. The blueprint must explicitly satisfy:

```text
OBJECT_MODEL
PRIMARY_RELATION
RELATION_DERIVATION
PRIMARY_REPRESENTATION
REPRESENTATION_SYMBOL_BRIDGE
WORKED_ANCHOR
RECONSTRUCTABLE_TTU
VALIDITY_OR_SPECIAL_CASE
MISCONCEPTION_COUNTEREXAMPLE
INDEPENDENT_CHECK
```

For HARD, the policy adds case analysis, failure mode, multi-representation translation, transfer obligations and **multiple reconstructable TTUs**. Optional obligations such as an alternative method may be marked `NOT_APPLICABLE`, but only with an explicit reason. Required obligations may not be waived to create pages faster.

### Core1B — open-ended reconstruction

Core1B must not replay Core1A prose. Its page grammar is mathematically productive:

```text
OPEN_TASK
+ RECONSTRUCTABLE_TTU
+ TECHNICAL_WORKSPACE
+ concept/representation help as needed
+ ANSWER_DERIVATION
+ VERIFICATION
```

Every `OPEN_TUTOR` page requires a TTU. The same MEDIUM bucket must prove open reconstruction, representation rebuild, a reconstructable TTU, method/error contrast, faded reconstruction, independent use and answer verification.

Whitespace used as learner work area is represented as an explicit typed workspace. Blank area that exists only because the layout forced a page break is not a pedagogical object.

### Core2 — frozen questions

Core2 pages are compact. They carry the immutable source problem, the authored hint ladder and an answer/check path. Core2 does not acquire explanatory filler merely because other cores are longer. If the frozen source itself contains a diagram/graph, that source representation remains source evidence; Core2 does not invent a TTU just to decorate it.

### Core2A — solution apprenticeship

A substantive Core2A page must contain:

```text
PROBLEM
SOLUTION_CHAIN
WHY_MOVE_WORKS
WRONG_CHAIN
VERIFICATION
+ reconstructable TTU somewhere in the stage
```

The source stem may repeat exactly when it is an immutable source object. The explanation around it must be newly authored for solution apprenticeship rather than copied from Core1A/Core1B.

The TTU should expose a decisive expert structure: an equation skeleton, incomplete graph, component model, case table or reasoning chain. The learner reconstructs that object after or alongside the declarative solution anatomy.

### Core2B — transfer tutor

A substantive Core2B page must contain:

```text
PROBLEM
TRANSFER_CLASSIFICATION
RECONSTRUCTABLE_TTU
TECHNICAL_WORKSPACE
ANSWER_DERIVATION
VERIFICATION
```

Every `TRANSFER_TUTOR` page requires a TTU. The learner is asked to identify structure and select a route before the answer is exposed. Core2B may not become Core2A with the paragraphs reordered.

Its TTU must be lineaged to Core2A but materially transformed by transfer: a hidden family cue, changed representation, reversed target, incomplete graph, altered event line, incomplete equation or other legal structural change.

## 5. Cross-core repetition is governed by lineage

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

`IMMUTABLE_CARRY` is reserved for content whose identity must not change, such as a frozen source question. TTU lineage uses the same principle at a finer technical-object level. This prevents six products from becoming six differently titled copies of the same notes.

## 6. Representation and TTU geometry are semantic geometry

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

Every TTU also declares its own bounded viewport. All plotted geometry — including axes, perpendicular bisectors, loci, construction lines, tangent lines, event lines and graph curves — is clipped to the representation/TTU viewport before page composition.

Therefore a mathematical line may be infinite **semantically** while its learner-page drawing remains bounded to the graph box. Extending a locus line across a title, answer block or page margin is a composition failure, not an acceptable rendering of an infinite line.

The viewport itself must lie inside the page bounds.

## 7. Pagination and whitespace

Default pagination is `FLOW`.

A forced break is legal only as `PEDAGOGIC_BREAK` with an explicit reason, for example a new cognitive phase that must begin cleanly. Manual spacer padding is forbidden.

The architecture intentionally does not set a maximum percentage of white page area. White area may be useful for learner work. Instead, blank space must have one of two explanations:

```text
1. natural remainder produced by flow pagination; or
2. explicit learner workspace / TTU reconstruction area with a mathematical purpose.
```

The renderer may not insert spacer blocks to approach a page target.

## 8. Technical depth precedes layout

The `EASY / MEDIUM / HARD` badge first resolves depth obligations. Only after those obligations are satisfied does page composition occur.

```text
DIFFICULTY BADGE
      ↓
DEPTH OBLIGATIONS
      ↓
mathematical content / representations / TTUs / tasks
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

## 9. Executable contract

Canonical files:

```text
TECHNICAL_COMPOSITION.md
contracts/math-learner-page-blueprint.schema.json
policies/math-technical-composition-policy.json
engine/validate_learner_page_blueprint.py
golden/technical_composition/02-medium-equidistant-reconstructable-ttu.json
tests/test_technical_composition.py
```

The validator fails closed on:

- prose-only pages;
- missing stage-required mathematical blocks;
- missing reconstructable TTUs in Core1A/Core1B/Core2A/Core2B;
- open/transfer tutor pages without a TTU;
- TTUs with no real missing parts;
- TTU completion keys that do not exactly cover the missing parts;
- Core1B TTUs not lineaged to Core1A;
- Core2B TTUs not lineaged to Core2A;
- downstream TTUs that increase rather than preserve/fade support;
- TTU depth obligations backed by prose instead of an actual TTU;
- manual spacer padding;
- unbounded representation or TTU geometry;
- representation/TTU viewports outside the page;
- open-tutor pages without explicit technical workspace;
- copied narrative/explanatory signatures across cores;
- repeated immutable content without explicit lineage;
- missing MEDIUM/HARD depth obligations;
- required depth obligations marked not applicable;
- fake flow pagination carrying a hidden forced-break reason.

## 10. Publication consequence

Publication must consume a validated `LearnerPageBlueprint`; it must not discover page structure or reconstruction tasks itself.

Future rendered-artifact preflight should verify the implementation-level consequences of this contract: bounding boxes stay inside their declared viewport/content frame, TTU missing parts remain visibly incomplete before the answer region, required semantic blocks are present, and no renderer-added content or spacer blocks appeared.

The architecture is therefore split cleanly:

```text
MathBlueprint decides WHAT mathematics is shown, omitted and reconstructed.
Publication decides HOW that already-governed page is typeset.
Rendered-artifact audit verifies THAT the typesetting respected the blueprint.
```
