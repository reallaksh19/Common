# Physics Gravity Research Engineering — canonicalized v3 tranche

## Purpose

This tranche is the first RESEARCH-depth new-domain proof of the canonical Engineering Workbench after SBA-23. It implements:

> Add gravitational field at RESEARCH engineering depth for Grade 9-11 competitive-exam use.

`RESEARCH` is technical-evidence depth. It does not increase learner difficulty by itself.

## Current lifecycle

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
CANONICAL V3 GATE SOURCES
engineering-gates/gravitation/**
        ↓
SUBJECT-WIDE V3 REGISTRY
        ↓
PRODUCTION V3 VALIDATION
        ↓
10-GATE TRANSITIVE CLOSURE
        ↓
ENGINEERING PASSPORT
```

Automatic semantic similarity does not choose the discovery operation. Discovery remains explicitly `HUMAN_REVIEWED`.

## Gate ownership

### `PHY-GRAV-FORCE`

Owns the Newtonian gravitational interaction model:

- mutual attraction;
- inverse-square force law;
- source/receiver direction;
- point-mass and external spherical-symmetry scope;
- third-law interaction pair;
- force-specific misconceptions and verification.

### `PHY-GRAV-FIELD`

Owns a distinct capability family:

- field as force per unit mass;
- test-mass independence within the Newtonian model;
- inward radial inverse-square field;
- field-vector representation;
- vector superposition at one common field point;
- field/force discrimination;
- local near-Earth `g` versus spatially varying gravitational field.

Putting both into `PHY-NLM-SECOND-LAW` or a monolithic `PHY-GRAVITY` gate remains rejected because the domain has independent governing relations, model conditions, representations, misconceptions, problem families and verification logic.

## Research evidence custody

The Research Dossier and Claim Ledger remain mandatory for this RESEARCH request. Gate authority refs bind the reviewed claim ledger, so canonicalization into v3 does not erase research provenance.

The evidence set includes source classes for:

- Newtonian universal gravitation and spherical-source applicability;
- gravitational field and radial inverse-square dependence;
- vector-force composition/superposition foundations;
- mass/weight and local `g` distinction;
- numerical `G` source-of-record custody;
- misconception evidence used for falsifier selection rather than Physics truth authority.

Misconception evidence supports explicit repair for models such as gravity acting only while falling, force direction following motion, universal `g = 9.8 N/kg`, and absolute page-down gravity. It does not set learner mastery or learner difficulty.

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

## Canonicalization status

The former file:

`policy/physics-technical-engineering-gates.gravity.v1.json`

is retained only as migration provenance. It is no longer merged into a v2 registry in memory for the active path.

The canonical gates are now:

`engineering-gates/gravitation/PHY-GRAV-FORCE.v3.json`

`engineering-gates/gravitation/PHY-GRAV-FIELD.v3.json`

They are assembled with the rest of Physics by:

`engine/build_physics_engineering_gate_registry_v3.py`

and validated by:

`engine/validate_engineering_gates_v3.py`

The active Gravity manifest is:

`fixtures/engineering-workbench/grav-field-manifest.v3.json`

and consumes:

`GENERATED:physics-technical-engineering-gates.v3`

No Gravity extension ref is permitted on the canonical v3 path.

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

The current Gravity proof rejects, among other cases:

- missing inverse-square field invariant;
- missing field-superposition relation;
- changing reviewed `CREATE_CHILD` to `EXTEND`;
- incorrect field parent ownership;
- a claim source absent from the dossier;
- provisional claims inside a READY ledger;
- removing evidence still referenced by claims;
- RESEARCH closure without dossier custody;
- manually making gravitational force a second direct manifest gate;
- reintroducing the legacy v2 extension mechanism;
- Gravity gate authority no longer bound to the claim ledger;
- unrelated direct-gate padding of the exact closure.

The subject-wide v3 registry separately falsifies typed symbol, model-condition, representation, reasoning, misconception, verification and invariant-profile failures.

## Publication boundary

Gravity Engineering READY authorizes technical consumption only. The Engineering Passport explicitly keeps publication authorization separate. Core1A pedagogical completion, Core2 transfer legality, learner state and PDF publication remain downstream Blueprint gates.

## PDF provenance rule

Any future PDF must be generated only after re-reading the current repository Blueprint for that exact PDF task. Earlier PDFs, previous chats, summaries, model memory, or unauthorised subject-memory reconstruction may not substitute for the current repository Blueprint.
