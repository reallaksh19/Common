# Physics Core1A Technical Publication Spec v2

## Purpose

Core1A is declarative-dominant deep teaching. Medium/Hard Physics publications must make the technical model reconstructable from the page itself.

V2 replaces the weak idea that a page is technically adequate merely because it contains a diagram and an equation.

## Canonical Technical Teaching Unit

Every major inferential jump and every major problem family must be taught through a complete Technical Teaching Unit (TTU):

```text
PHYSICAL SETUP
→ TECHNICAL REPRESENTATION
→ GOVERNING RELATION
→ MAPPING / INTERMEDIATE WORKING
→ RESULT / CONCLUSION
→ VERIFICATION
```

The TTU may span two adjacent pages when necessary, but the representation-to-equation bridge must be explicit.

## Physical setup

State the information an expert would extract before calculation:

- object/system;
- event;
- known quantities;
- required quantity;
- reference frame;
- axes/sign convention;
- model conditions when material.

## Technical representation

Use a genuine Physics representation when the capability needs one:

- vector/component diagram;
- free-body diagram;
- trajectory/graph with meaningful axes;
- event timeline;
- geometry construction;
- reference-frame diagram;
- physical-variable table;
- state/equation dependency representation.

Generic text cards, decorative arrows, unlabeled axes and oversized empty plots do not count.

## Representation binding

Every figure must visibly connect to the working. The learner should be able to answer:

> Which label/vector/feature in this figure becomes which term or condition in the equation?

If that mapping is not visible, the figure is incomplete.

## Governing relation and working

Show the law/relation and the intermediate bridge from the setup/representation to the result.

Preferred worked-example grammar:

`STEP | WHY THIS STEP | TECHNICAL WORKING`

For nontrivial problems, a large figure followed by one final equation is not an adequate worked solution.

## Verification

Use the most meaningful available check:

- sign/direction;
- units/dimensions;
- limiting case;
- physical sense;
- model validity;
- alternative representation consistency.

## Hard-bucket requirement

Hard means **technical inferential closure**, not more prose and not larger pictures.

A Hard Core1A fails release if a major technical jump depends on a diagram/equation/transformation but the publication supplies only prose or a semantically weak visual.

## Page composition

- prefer flow layout;
- keep figure and bound working adjacent;
- crop figures to instructional content;
- avoid large unused plotting regions;
- native text/equations are preferred over rasterized equation text;
- labels must remain legible at final PDF size;
- figures may not displace the intermediate working they are supposed to support.

## Release preflight

Render every page. New layouts require full-resolution and montage/thumbnail review. Fail closed on:

- text/figure overlap;
- label/vector overlap;
- clipped labels;
- microscopic figure labels;
- unreadable equations;
- oversized low-information figures;
- orphaned figures separated from their working;
- broken glyphs or header collisions.

See:

- `../Blueprint/policy/technical-teaching-unit.v1.json`
- `../Blueprint/policy/physics-representation-semantic-quality.v1.json`
- `../Blueprint/policy/pdf-layout-integrity.v2.json`
