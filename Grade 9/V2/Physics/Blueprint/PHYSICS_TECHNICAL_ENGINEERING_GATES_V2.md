# Physics Technical Engineering Gates v2

This document absorbs the useful domain model from PR #376 into the canonical Physics Blueprint and supersedes that prototype for future Physics work on PR #350.

## Purpose

A Technical Engineering Gate answers one question before CCU/CDAU/TTU authoring:

> What irreducible Physics concepts, relations, representations, reasoning transitions, misconceptions and verification rules must exist for this subtopic to be technically coherent?

It is not a learner-mastery model, item-response model, psychometric difficulty scale, or a substitute for source custody.

## Authority position

```text
GROUND TRUTH / SOURCE
  -> Core0 / Core1 / independent Core2 / Join
  -> CANONICAL DOMAIN REGISTRY
  -> PHYSICS TECHNICAL ENGINEERING GATES
  -> CCU
  -> CDAU
  -> SDU / LAU
  -> Concept TTU / Problem TTU
  -> publication / learner runtime
  -> CAL
```

The gate layer cannot invent frozen-source wording, legalize Core2 transfer, or manufacture learner evidence.

## Why v2 exists

PR #376 established the right architectural idea and a useful Vectors/Newtonian decomposition. The canonical v2 hardens it in four ways:

1. **Production-validator falsification:** negative tests mutate the real registry and must be rejected by the same validator used in CI.
2. **Stable error codes:** validator failures are machine-auditable rather than depending on ad-hoc assertion text.
3. **Structured authority/provenance:** every gate declares whether its claims are source-defined, standard-Physics-derived, authoring recommendations, or source-scope held; unverified external citations are not used as authority decoration.
4. **Cross-reference integrity:** prerequisite gates, relation bindings, canonical asset IDs, status/maturity and required subtopic invariants are checked deterministically.

## Canonical decomposed gates

Absorbed from the PR #376 prototype:

- `PHY-VEC-BASICS`
- `PHY-VEC-ADD-SUB`
- `PHY-VEC-COMPONENTS`
- `PHY-NLM-INTERACTION`
- `PHY-NLM-FBD`
- `PHY-NLM-FIRST-LAW`
- `PHY-NLM-SECOND-LAW`
- `PHY-NLM-THIRD-LAW`
- `PHY-NLM-NORMAL`
- `PHY-NLM-TENSION`
- `PHY-NLM-FRICTION`
- `PHY-NLM-CONNECTED`

Added immediately for the active Motion-in-a-Plane pipeline:

- `PHY-M2D-PROJECTILE-COMPONENTS`
- `PHY-M2D-SHARED-CLOCK`
- `PHY-M2D-MOVING-LAUNCHER`

The last gate is explicitly linked to `M2D-SBA-23` and requires frame naming, Galilean velocity conversion before projectile evolution, inherited horizontal motion, inverse-frame verification, the zero-source-speed limiting case, and one shared post-release clock.

## Gate contract

Each gate contains:

- stable subtopic identity;
- explicit authority basis;
- prerequisite graph;
- linked SBA buckets;
- applicable Cores;
- required invariant IDs;
- canonical concept records;
- equations/relations with symbol bindings, conditions and cognitive obligations;
- technical representations with mandatory elements and equation bindings;
- reasoning sequence;
- misconception/repair records;
- independent verification modes;
- problem-family IDs;
- provisional intrinsic-difficulty engineering profile.

`ENGINEERING_GATE_READY` is not established by a self-authored checklist. The production validator derives readiness from schema validity, required invariant presence and cross-reference closure.

## Fail-closed semantics

Examples of deterministic failures include:

- vector components with no sign convention or no component-to-resultant reconstruction;
- Newton-II gate with no FBD prerequisite;
- FBD gate replaced by a decorative diagram;
- Newton-III gate losing distinct-body semantics;
- normal force treated as universally equal to `mg`;
- static friction inequality removed;
- projectile x/y equations losing one shared event clock;
- moving-launcher gate losing frame conversion before projectile dynamics;
- unknown prerequisite or representation-to-relation binding;
- source-scope-held gate marked READY;
- engineering difficulty relabelled as validated.

## Difficulty maturity

The 0–3 difficulty vector is an **ENGINEERING** authoring signal only. V9/CAL governs later calibration. A gate cannot claim empirical/psychometric validation by changing its maturity label.

## Normative files

- `contracts/physics-technical-engineering-gate-v2.schema.json`
- `policy/physics-technical-engineering-gates.v2.json`
- `engine/validate_engineering_gates_v2.py`
- `tests/test_physics_engineering_gates_v2.py`

The PR #376 prototype remains useful historical provenance, but this v2 registry is the canonical implementation owned by PR #350.
