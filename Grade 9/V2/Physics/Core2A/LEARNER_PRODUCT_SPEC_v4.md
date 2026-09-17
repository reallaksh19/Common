# Physics Core2A v4 — Declarative Worked Problem TTUs

## Purpose

Core2A is a self-guided declarative-dominant problem-learning product.

> Show me how an expert reads, represents and solves this legal problem family.

Student knowledge % or owner override controls support density and exemplar selection inside the legal Core2A pool. It never changes source legality.

## Worked problem TTU

Every representative worked item must expose the complete technical chain:

```text
QUESTION
→ EXTRACT KNOWN / UNKNOWN / FRAME / EVENT
→ CONSTRUCT TECHNICAL REPRESENTATION
→ SELECT GOVERNING RELATION
→ MAP EACH GIVEN TO THE RELATION
→ SHOW INTERMEDIATE WORKING
→ RESULT
→ VERIFY
→ WRONG ROUTE / VARIATION WHEN MATERIAL
```

A page with a large diagram and one final equation is not a worked solution.

## Technical representation rule

The representation must encode Physics structure used in the solution:

- vector/component construction;
- free-body diagram;
- geometry/ray construction;
- graph/trajectory with meaningful axes;
- event timeline;
- reference-frame diagram;
- physical-variable table;
- equation dependency map.

Generic text cards and decorative process boxes do not count.

## Figure-to-equation binding

Every major figure must support a specific reasoning step. When material, state explicitly which diagram quantity maps to which equation term.

Example:

`horizontal source vector V → u_x,G = u'_x + V`

## Model-discrimination items

A model-discrimination publication must compare actual Physics structure, not generic boxes.

Minimum fields:

1. physical trigger;
2. representation/model selected;
3. first move;
4. why a tempting competing model is rejected.

## Support routing

### FOUNDATION_HIGH_SUPPORT

Prerequisite bridge + explicit setup extraction + complete technical representation + worked first move + full TTU.

### GUIDED

Recognition cue + explicit technical representation + partially faded working + complete TTU after attempt.

### STANDARD

Attempt first + compact expert TTU + verification + variation.

### CHALLENGE_MINIMAL

Minimal pre-solution cueing + compact expert TTU after attempt + structural comparison/error analysis.

## Frozen-source rule

Frozen Core2 source wording is immutable. Adaptation changes support, ordering, completion level and already-legal generated-original variants only.

## Layout requirements

- use proportional figures cropped to instructional content;
- do not let low-information graphics displace working;
- prefer native equations/text over raster text;
- figure labels remain legible at final size;
- keep figure and working adjacent;
- render and visually inspect every page before release.

## Authority boundary

A polished Core2A solution does not prove learner transfer. Knowledge %/owner override cannot expand the legal pool.

See:

- `../Blueprint/policy/technical-teaching-unit.v1.json`
- `../Blueprint/policy/physics-representation-semantic-quality.v1.json`
- `../Blueprint/policy/pdf-layout-integrity.v2.json`
