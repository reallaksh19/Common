# Physics Gravity Research Engineering v1

## Purpose

This tranche is the first new-domain proof of the Engineering Workbench after SBA-23. It implements the request:

> Add gravitational field at RESEARCH engineering depth for Grade 9-11 competitive-exam use.

`RESEARCH` is technical-evidence depth. It does not increase learner difficulty by itself.

## Engineering lifecycle

```text
ENG-REQ-GRAV-FIELD-V1
        ↓
HUMAN-REVIEWED DISCOVERY
        ↓
REUSE existing Vector + NLM capabilities
CREATE_CHILD PHY-GRAV-FORCE
CREATE_CHILD PHY-GRAV-FIELD
        ↓
RESEARCH DOSSIER
        ↓
CLAIM-LEVEL PROVENANCE LEDGER
        ↓
VALIDATED GRAVITY GATE EXTENSION
        ↓
CANONICAL BASE REGISTRY + EXTENSION
        ↓
PRODUCTION GATE VALIDATION
        ↓
10-GATE TRANSITIVE CLOSURE
        ↓
ENGINEERING PASSPORT
```

Automatic semantic similarity does not choose the operation. Discovery is explicitly `HUMAN_REVIEWED`.

## Why two gates

### `PHY-GRAV-FORCE`

Owns the Newtonian interaction model:

- mutual attraction;
- inverse-square force law;
- source/receiver direction;
- point-mass and external spherical-symmetry scope;
- third-law interaction pair;
- force-specific misconceptions and verification.

### `PHY-GRAV-FIELD`

Owns a different capability family:

- field as force per unit mass;
- test-mass independence within the Newtonian model;
- inward radial inverse-square field;
- field-vector representation;
- vector superposition at a common field point;
- field/force discrimination;
- local near-Earth `g` versus universal field behavior.

Putting both into `PHY-NLM-SECOND-LAW` or a monolithic `PHY-GRAVITY` gate is rejected because the new material has independent governing relations, model conditions, representations, misconceptions, problem families and verification logic.

## Research sources

The dossier binds claims to the following source classes:

- OpenStax University Physics Vol. 1, §13.1 — Newtonian universal gravitation, attractive direction, third-law pair, point/spherical-source applicability: https://openstax.org/books/university-physics-volume-1/pages/13-1-newtons-law-of-universal-gravitation
- OpenStax University Physics Vol. 1, §13.2 — gravitational field, inward radial representation and inverse-square spatial dependence: https://openstax.org/books/university-physics-volume-1/pages/13-2-gravitation-near-earths-surface
- OpenStax University Physics Vol. 1, §5.1 — vector addition of force contributions: https://openstax.org/books/university-physics-volume-1/pages/5-1-forces
- OpenStax University Physics Vol. 1, §5.4 — `w = m g` and location dependence of gravitational acceleration/field strength: https://openstax.org/books/university-physics-volume-1/pages/5-4-mass-and-weight
- NIST/CODATA constants database — current source of record for numerical `G`: https://physics.nist.gov/cuu/Constants/
- IEA/TIMSS misconception analysis — used only to select misconception falsifiers, not as Physics authority: https://link.springer.com/chapter/10.1007/978-3-030-30188-0_4

## Quantitative misconception evidence

The TIMSS analysis provides a concrete reason to engineer gravity misconceptions explicitly rather than assuming prior intuition is reliable. In one grade-eight item averaged across the sampled countries:

- **36%** correctly identified gravity as acting on a parachutist in all four tested states;
- **57%** selected responses in which gravity acted only while the jumper was falling.

The same research program reports that gravity misconceptions were generally common across countries and grades, with many misconception frequencies at or above 25% and some reaching at least 50% in individual countries/context combinations.

This evidence supports mandatory falsifiers for:

- `MIS-GRAV-FORCE-FALLING-ONLY`;
- geometry/source-based force direction rather than motion-based direction;
- local radial direction rather than an absolute page-down concept.

It does not determine learner difficulty badges or mastery.

## Scope boundary

Included:

- Newtonian two-mass gravitational force;
- point-mass relation;
- external field/force of spherically symmetric sources;
- gravitational field as force per unit mass;
- radial inward direction;
- inverse-square dependence;
- field superposition;
- relation `F_grav = m g`;
- near-Earth `g` as a local approximation.

Explicitly excluded from this request:

- gravitational potential;
- gravitational potential energy;
- escape speed;
- orbital mechanics;
- detailed interior-shell/spherical-distribution derivations;
- general relativity.

Those require later Engineering Requests rather than silent scope growth.

## Registry extension

The current 15-gate v2 base registry is not rewritten for this pilot. The manifest references:

`policy/physics-technical-engineering-gates.gravity.v1.json`

The closure compiler merges the extension into the base registry in memory, validates the combined registry with the existing production gate validator, and digest-binds the extension reference into the closure receipt.

This is an incremental addition mechanism, not a second authority registry. Duplicate IDs, unresolved prerequisites and broken representation/relation bindings still fail through the canonical validator.

## Expected closure

The single direct gate is:

`PHY-GRAV-FIELD`

Its Physics closure must resolve to exactly 10 gates:

```text
PHY-VEC-BASICS
PHY-VEC-ADD-SUB
PHY-VEC-COMPONENTS
PHY-NLM-INTERACTION
PHY-NLM-FBD
PHY-NLM-FIRST-LAW
PHY-NLM-SECOND-LAW
PHY-NLM-THIRD-LAW
PHY-GRAV-FORCE
PHY-GRAV-FIELD
```

No manual `engineering_ready` assertion exists.

## Falsification

`engine/validate_gravity_research_v1.py` and `tests/test_physics_gravity_research_v1.py` reject at least:

- missing inverse-square field invariant;
- missing superposition relation;
- changing `CREATE_CHILD` to `EXTEND`;
- incorrect field parent ownership;
- a claim source absent from the dossier;
- provisional claims inside a READY ledger;
- removing misconception evidence from the dossier while claims still depend on it;
- RESEARCH closure without the dossier reference;
- manually making gravitational force a second direct manifest gate rather than deriving it as a prerequisite.

## PDF provenance rule

The project-wide rule remains binding: any future PDF must be generated only after re-reading the current repository Blueprint for that exact PDF task. Earlier PDFs, previous chats, summaries, model memory, or unauthorised subject-memory reconstruction may not substitute for the current repository Blueprint.
