# Chemistry Core1B — Elicitation-First Concept Self-Tutor

Core1B is a **static learner-facing self-tutoring realization** of a Chemistry LearningBlueprint v4 instruction bucket. Core1A remains the exposition-first learner product; Core1B does not modify Core1A or independently decide Chemistry depth.

## v4 authority

Every Core1B compilation must carry an `instruction_bucket` that passes:

```text
LearningBlueprint/engine/validate_blueprint_v4.py
```

Core1A and Core1B share the same bucket authority:

```text
same subtopic / sub-subtopic scope
same capability set
same learning atoms
same prerequisites
same representation authority
same misconceptions / boundaries
same intrinsic difficulty badge
same research package
```

The difficulty badge is **intrinsic to the subtopic**, not learner knowledge.

```text
EASY   -> <= 10 page normal envelope; research optional
MEDIUM -> <= 20 page normal envelope; web research required
HARD   -> <= 30 page normal envelope; deep research required
```

These are ceilings, never page quotas. A Core1B compiler containing `knowledge_percent`, `student_knowledge_percent` or equivalent learner-readiness control fails closed.

## Purpose

Core1A explains until the learner can understand. Core1B questions until the learner can reconstruct.

Core1B therefore presents already-taught Chemistry as open-ended prompts that make the learner retrieve, represent, explain, compare, correct and generalize before seeing help.

## Page grammar

```text
OPEN-ENDED TASK
+ meaningful workspace
+ governed representation when applicable

SELF-GUIDED HELP
  H1 ORIENT / NOTICE
  H2 REPRESENT / STRUCTURE
  H3 PRINCIPLE / INVARIANT
  H4 FIRST MOVE or REASONING FRAME

CANONICAL / EXPECTED RESPONSE
+ explanation
+ independent check
```

The help is fixed at compilation time. No learner response is consumed while the artifact is being used.

## Chemistry-specific cognitive moves

Core1B may instantiate:

- observation -> evidence -> inference;
- macroscopic -> particle/model -> symbolic translation **only when upstream-authorized**;
- species identity tracking;
- conservation / charge / oxidation-state ledgers;
- correct-vs-plausible-wrong contrast;
- method/model comparison;
- completion and fading;
- controlled variation;
- concept-level retrieval and delayed recall prompts.

A visual must perform one of the v4 named reasoning jobs. Decorative image count does not satisfy depth.

## Production-depth HARD Redox golden

`golden/hard-redox-production/` is the first deliberate **production-depth** Core1B bucket rather than a one-page contract golden.

It consumes the existing Redox Core1A authority and does not modify Core1A. The bucket is `HARD`, has a 30-page v4 ceiling, and realizes **24 pages** across eight researched sub-subtopics:

```text
species identity
oxidation-state meaning
direction -> Redox label
electron consequence
agent role
representation translation
misconception / boundary diagnosis
fading / teach-back
```

Each sub-subtopic receives three learner actions, giving 24 pages total. Every page remains open-ended and closes with fixed self-help, a canonical response and an independent check. The production-quality gate also requires **eight distinct module-specific hint ladders**; a mechanically repeated hint script across all modules is not accepted as tutoring depth.

The deep-research packet records four sources addressing Redox misconceptions, high-school electrochemical concept difficulty, representation coordination and worked-example/fading design. Research may improve realization, but it does **not** expand Chemistry authority. In particular, the current Redox production profile authorizes this depth extension at the symbolic level, so this golden deliberately refuses particle/submicroscopic Redox visuals unless upstream authority expands later.

The production compiler used by CI is:

```text
engine/compile_hard_redox_bucket_v2.py
```

It reuses the validated page specification and authority checks in `compile_hard_redox_bucket.py`, then specializes the self-help by conceptual module.

The production path emits:

```text
core1b_hard_plan.json
chemistry_core1b_hard_redox.pdf
core1b_hard_quality_audit.json
```

## Static boundary

Forbidden runtime concepts include:

```text
learner_response
attempt_history
state_transition
next_task
adaptive_branch
runtime_hint
repair_route
mastery_update
```

## Outputs

The compact reference compiler emits:

```text
core1b_plan.json
chemistry_core1b.pdf
core1b_quality_audit.json
```

The plan and audit retain the resolved v4 bucket ID, difficulty badge, page-envelope ceiling, research mode and control axis.

Current goldens validate:

1. an `EASY` observation/evidence/inference bucket;
2. a compact `HARD` Redox species/oxidation-state/agent-role contract golden;
3. a 24-page production-depth `HARD` Redox self-tutor with deep research, sub-subtopic decomposition, eight module-specific hint ladders, symbolic-authority custody and complete per-page answer closure.
