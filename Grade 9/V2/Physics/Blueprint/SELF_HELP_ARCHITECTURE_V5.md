# Physics Self-Help Architecture V5 — technical teaching units, semantic representations, fail-closed visual publication

V5 fixes a failure that V4 still permitted: a learner page could technically contain an equation and a diagram yet remain academically weak because the visual was oversized, under-labelled, generic, disconnected from the working, or merely decorative.

The canonical publication unit is now the **Technical Teaching Unit (TTU)**.

## 1. Canonical authoring order

```text
SUBTOPIC / SBA BUCKET
        ↓
HIDDEN INVARIANT(S)
        ↓
PREREQUISITE BRIDGES
        ↓
INFERENTIAL JUMPS
        ↓
PROBLEM FAMILIES
        ↓
TECHNICAL TEACHING UNITS
        ↓
LAYER REALIZATION
```

A page count, a diagram count, an equation count or a collection of prose boxes is never the authoring unit.

## 2. Technical Teaching Unit (TTU)

A TTU is complete only when the learner can connect all of the following:

1. **PHYSICAL_SETUP** — objects, event, givens, unknown, frame/axes when material;
2. **TECHNICAL_REPRESENTATION** — a domain representation that encodes Physics structure;
3. **GOVERNING_RELATION** — the law/equation/geometric or vector relation being used;
4. **MAPPING_OR_WORKING** — the visible bridge from representation/givens to the governing relation and through intermediate steps;
5. **RESULT_OR_CONCLUSION** — numerical, symbolic or conceptual result;
6. **VERIFICATION** — sign, units, direction, limiting case, physical sense, model validity or another material check.

A page may contain one TTU or part of a TTU continued onto the immediately following page. The learner must never have to infer the missing bridge between a picture and a final equation.

## 3. What counts as a Physics technical representation

A representation counts only if it encodes domain structure needed for understanding or solving the task. Examples:

- labelled vector/component construction;
- free-body diagram;
- ray/geometry construction;
- field/force representation;
- trajectory with meaningful axes/variables;
- graph tied to physical variables;
- event timeline;
- state-transition diagram;
- coordinate/reference-frame diagram;
- physical-variable table;
- equation map where arrows represent mathematical/physical dependency.

The following do **not** count toward technical representation closure:

- generic text cards;
- decorative arrows between boxes;
- unlabeled or weakly labelled axes;
- an oversized empty coordinate plane;
- a diagram whose variables are not used in the accompanying working;
- a final equation rendered beneath a picture without a visible mapping step;
- repeated prose converted into shapes;
- decorative illustrations.

## 4. Representation-to-working binding

Every technical figure must have a declared instructional role and a **binding** to the reasoning that follows.

For example:

```text
VECTOR DIAGRAM
  v_BG = v_BT + v_TG
        ↓
COMPONENT MAP
  u_x,G = u' cos α + V
  u_y,G = u' sin α
        ↓
NUMERIC SUBSTITUTION
        ↓
RESULT + DIRECTION CHECK
```

If the learner cannot point from the figure label to the equation term that uses it, the figure is incomplete.

## 5. Core1A

Core1A is declarative-dominant and must contain complete TTUs for each major inferential jump/problem family.

A Hard Core1A must normally expose:

- notation and frame/axis conventions;
- the technical representation;
- the governing relation;
- intermediate derivation/transformation;
- representative numerical/symbolic working;
- physical/model checks.

The 10/20/30 Easy/Medium/Hard page values remain soft **Core1A capacity ceilings**, not targets.

## 6. Core1B

Core1B is generative-dominant and selective. It does not repeat Core1A page-for-page, but each fragile checkpoint must use a **reconstructable TTU**, not a prose question when the capability is technical.

Typical Core1B TTU:

```text
INCOMPLETE TECHNICAL SETUP
        ↓
LEARNER LABELS / DRAWS / SELECTS / DERIVES
        ↓
OPTIONAL H1 NOTICE
OPTIONAL H2 REPRESENT
OPTIONAL H3 START
        ↓
LEARNER WORKING
        ↓
FULL TECHNICAL CHECK
        ↓
SMALLEST REPAIR
```

For a Hard Physics bucket, a Core1B page containing only prose prompts and blank lines is noncompliant whenever an expert would naturally use a diagram, graph, component construction, equation or event representation.

## 7. Core2A

Core2A is declarative-dominant worked problem-family learning. Student knowledge % or owner override selects support density and representative legal exemplars.

Each representative worked problem must be a complete **problem TTU**:

```text
FROZEN / LEGAL QUESTION
→ EXTRACT KNOWN / UNKNOWN / FRAME / EVENT
→ CONSTRUCT TECHNICAL REPRESENTATION
→ SELECT GOVERNING RELATION
→ MAP EACH GIVEN INTO THE RELATION
→ SHOW INTERMEDIATE WORKING
→ RESULT
→ PHYSICAL / DIMENSIONAL / LIMITING CHECK
→ WRONG ROUTE / VARIATION WHEN MATERIAL
```

A large vector picture plus a final equation is not an adequate worked solution.

A model-discrimination item must compare actual Physics structure: trigger, representation/model, first move, and why competing models are rejected. Generic boxes labelled A/B/C do not count as a Physics representation.

## 8. Core2B

Core2B is generative-dominant transfer. The learner must select or construct the required representation/model when that selection is part of the transfer demand.

Core2B should use fresh legal items/variants where the pool permits rather than mirror Core2A one-for-one.

A transfer TTU requires:

```text
UNFAMILIAR QUESTION
→ LEARNER EXTRACTS SETUP
→ LEARNER SELECTS / CONSTRUCTS REPRESENTATION
→ LEARNER SELECTS GOVERNING RELATION / FIRST MOVE
→ WORKING
→ OPTIONAL PROGRESSIVE RESCUE
→ TECHNICAL CHECK
→ WHAT STAYED INVARIANT / WHAT CHANGED
→ REPAIR IF NEEDED
```

## 9. Figure semantic quality

A technical figure must satisfy all of the following when applicable:

- all variables used in the working are identifiable;
- frame/axis/direction conventions are explicit;
- labels are unambiguous and do not sit on top of vectors/objects;
- the figure contains no large unused plotting region without instructional purpose;
- important vectors/objects are visually distinguishable;
- labels and equations remain legible at normal reading zoom;
- the caption or adjacent working states what the learner should read from the figure.

The figure's purpose is to **carry reasoning**, not to occupy page area.

## 10. Layout and typography release gates

Production learner PDFs must use flow layout or collision-validated composition.

Native text/equations are preferred over rasterized text. If labels are part of a figure, the final rendered label size must remain comparable to learner body text and never become microscopic.

Every new learner layout is rendered page-by-page and fails closed on:

- text/text overlap;
- label/vector overlap that changes meaning;
- text/figure overlap;
- clipped labels;
- unreadable equations;
- broken glyphs;
- excessive unused figure whitespace that suppresses working;
- figures too small to read or too large relative to their instructional content;
- header/figure collision;
- orphaned figure separated from the working it supports.

A successful PDF generation is never a visual-preflight pass.

## 11. Authority remains unchanged

This architecture strengthens learner publication quality only.

- Core1B still cannot author new Physics semantics.
- Core2A legality still comes from frozen Core2 + taught-state custody.
- Core2B still cannot legalize transfer.
- knowledge % / owner override cannot expand the legal pool.
- solution exposure is teaching, not mastery evidence.

## 12. Normative policies

- `Blueprint/policy/self-help-core-publication.v5.json`
- `Blueprint/policy/technical-teaching-unit.v1.json`
- `Blueprint/policy/physics-representation-semantic-quality.v1.json`
- `Blueprint/policy/pdf-layout-integrity.v2.json`
- `Blueprint/policy/core1ab-bucket-authoring.v2.json`
- `Blueprint/policy/core2ab-knowledge-routing.v1.json`

V5 supersedes V4 for learner-product publication quality. V4's technical-density requirement remains directionally correct but is insufficient by itself because mere presence of a diagram/equation does not prove technical teaching quality.
