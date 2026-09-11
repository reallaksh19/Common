# Mathematics V2 — M-D Problem Semantics

Implements #239 after merged M-A/M-B/M-C. M-D owns the learner-independent intellectual structure of a Mathematics problem **after** assessment scope is resolved and **before** learner diagnosis, teaching choreography, hints, solutions or page composition.

```text
M-C MathAssessmentCoverageMatrix
        +
MathProblemFamilyRegistry
MathReasoningRoleRegistry
MathVerificationRouteRegistry
Assessment Item Semantic Profiles
Guide Demand Badge Policy
        ↓
MathProblemSemanticsPackage
```

## Authority boundary

M-D owns problem-family semantics, semantic reasoning transitions, verification routes and multidimensional reasoning-demand description. It consumes M-C capability/problem-family/representation/verification identities and may not redefine them.

`ReasoningRoute != Hint Ladder != Solution`. A reasoning route explains why mathematical states connect. It contains no learner-state treatment, hint wording, support rung, worked answer or publication instruction. Downstream Core2 support may bind to route-step IDs without changing the route.

## Problem families

Each `MathProblemFamilyDefinition` freezes: canonical capability refs; structural recognition signature; variable roles; allowed variations; a semantic reasoning-route template; representation requirements and translation invariants; one verification route; common invalid transformations/distractor mechanisms; and near/far transfer boundaries.

The M-C family IDs are exhaustive in this phase. A family cannot be invented here without an M-C identity.

## Reasoning routes

The role vocabulary is fixed to `INTERPRET`, `REPRESENT`, `SELECT_METHOD`, `MODEL`, `EXECUTE`, `TRANSFORM`, `COMPARE`, `INFER`, `CHECK_CONDITION`, `VERIFY`, `INTERPRET_RESULT`. Runtime instantiates an assessment-item route from the exact M-C role expectations plus the bound family template.

## Demand vectors

Demand is sparse and multidimensional. It may use `reasoning_chain_length`, `algebraic_load`, `representation_shift`, `hidden_structure`, `state_tracking_load`, `method_selection_ambiguity`, `constraint_density`, `concept_combination`, `verification_demand`, and `time_pressure`. Each nonzero dimension has a level and explicit basis.

A learner-facing `EASY/MEDIUM/HARD` badge is derived only by `MATH-GUIDE-DEMAND-POLICY-v1` and is always labelled `GUIDE_ASSIGNED_REASONING_DEMAND`. It is not psychometric calibration and makes no learner-ability claim. `HARD` additionally requires a sufficiently deep semantic route; a high vector score alone cannot manufacture a hard label.

## Assessment-safety preservation

M-D reruns the merged M-C resolver. Therefore M-B validity/diagnostic-use status survives unchanged: the underdetermined Q9 remains `POSITIVE_EVIDENCE_ONLY`, Q12 remains a legitimate multiple-solution item, and outside-scope Q6 remains mathematically mapped without silently changing the declared boundary.

## Non-goals

No AttemptSet interpretation, learner diagnosis, StudyModel treatment, PCK authoring, Core1 lesson sequence, H1/H2/H3 wording, complete worked solution, psychometric difficulty, or publication rendering.
