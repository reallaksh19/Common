# Physics V2 — Core1B Learner Concept Construction Runtime

Core1B is the learner-facing runtime downstream of Core1A. It converts an authorized assimilation plan into teacher-quality instruction and observable learner evidence.

## Governing question

> Given the authorized Physics, Core1A plan, learner evidence, and target transfer demands, what is the smallest coherent teacher-led experience that lets this learner construct, represent, explain, and independently use the physical model?

## Inputs

- Core1 semantic authority;
- Core1A SBA/teaching requirements and T-PHY taught-state expectations;
- declared learner profile and purpose;
- prior `PhysicsLearnerCapabilityEvidence` where available.

## Outputs

- learner-facing teacher unit;
- atom/prerequisite evidence;
- learner capability evidence;
- Core1B release receipt;
- optional targeted repair receipt.

## Runtime model

```text
ANCHOR / PHENOMENON
    -> KNOWLEDGE ATOMS
    -> REPRESENTATION RAMP
    -> RECOMBINE INTO MODEL
    -> WORKED
    -> FADED
    -> INDEPENDENT
    -> RELEASE EVIDENCE
```

The runtime may skip already-secure atoms. It must not force one fixed ladder on all learners.

## Learner-facing rule

The learner sees a teacher, not a state machine. Internal identifiers such as `ATOM_*`, `DIAGNOSTIC_BRANCH`, `STATE_FRAGILE`, or `REPAIR_*` are forbidden on the learner surface.

Natural teacher moves are preferred: `What do you notice?`, `Look only at the vertical motion`, `Need a small nudge?`, `Why does this make sense?`.

## Atom contract

A Physics atom should normally introduce at most one new physical relationship and one required representation operation. Each atom declares prerequisites, a micro-example, misconception risks, an independent check, failure signatures, repair routes, merge target, and authority reference.

## Representation policy

Representations must teach or test reasoning. Typical mechanics ramp:

```text
physical situation -> arrows -> labelled diagram -> table -> points -> graph -> symbols -> equation
```

Do not require every representation for every topic. Use only those needed to remove the inferential jump. Once taught, at least one reverse translation should be tested where appropriate.

## Formula timing

For fragile learners, symbols/equations should follow physical meaning and representation. For learners with secure prerequisite evidence, the runtime may compress the sequence.

## Hint policy

Core1B hints may teach or repair, but should first localize the missing prerequisite. A stuck learner should normally move `backward to the missing atom -> short repair -> return to the original problem`, rather than simply receive progressively more of the full solution.

## Readiness

Recommended learner states:

`NOT_EXPOSED -> EXPOSED -> SUPPORTED -> INDEPENDENT -> TRANSFER_READY -> ROBUST`

Core1B normally establishes through `INDEPENDENT`. Core2B supplies transfer/robustness evidence.

A Core1B release candidate should demonstrate, for the released family:

- RECOGNISE;
- REPRESENT;
- FIRST_MOVE;
- FINISH;
- CHECK;
- and, when required by the unit, EXPLAIN/APPLICABILITY.

## Upstream custody

Core1B may reorganize, scaffold and repair authorized Physics. It may not invent new laws, problem families, source claims, or transfer permissions. Core1/Core1A remain semantic/teaching authority.

## Production surfaces

```text
contracts/
  physics-core1b-unit.schema.json
  physics-core1b-learner-evidence.schema.json
  physics-core1b-release-receipt.schema.json
registry/
  projectile-vertical-event-atoms-v1.json
engine/
  core1b_common.py
  run_core1b.py
golden/projectile-vertical-event/
  core1b-unit.json
tests/
  test_physics_core1b.py
```

The golden is deliberately small but executable: it validates authority refs, atom prerequisites, learner-surface leakage, independent readiness, and release-receipt closure.