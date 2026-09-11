# Physics V2 — P-D Problem Semantics

Implements **#252** under Physics assessment-first roadmap **#248** / quality programme **#234**. P-D consumes the merged P-C Question→Physics authority and turns each authorized problem-family identity into learner-independent physical reasoning semantics.

```text
P-C PhysicsAssessmentCoverageMatrix
        +
PhysicsProblemFamilyRegistry
PhysicsReasoningRoleRegistry
PhysicsVerificationRouteRegistry
Motion Item Semantic Profiles
Guide Demand Badge Policy
        ↓
PhysicsProblemSemanticsPackage
```

The governing separation is strict:

```text
PhysicsReasoningRoute != Hint Ladder != Worked Solution
```

A reasoning route records **why the physical state, representation, model, relation and verification steps connect**. It contains no hint wording, learner treatment, observed answer, worked answer or final answer.

## Physics-specific semantic closure

Every problem family owns explicit system roles, frame requirements, phase topology, state variables, model-selection criteria, model-validity conditions, allowed variations/invariants, representation requirements, reasoning-route template, verification route, common wrong models/sign errors and transfer boundaries.

P-D cannot invent a problem-family identity: the family registry must match the P-C identity set exactly and is digest-bound to the P-C scope authority.

## Canonical reasoning roles

P-D uses the #252 vocabulary exactly: `READ_PHENOMENON`, `DEFINE_SYSTEM`, `CHOOSE_FRAME`, `REPRESENT`, `IDENTIFY_PHASES`, `EXTRACT_KNOWNS_AND_HIDDEN_FACTS`, `SELECT_MODEL`, `CHECK_MODEL_VALIDITY`, `PROPAGATE_STATE`, `CHOOSE_RELATION`, `SOLVE`, `INTERPRET_SIGN_DIRECTION`, `CHECK_UNITS`, `CHECK_CONTINUITY_OR_BOUNDARY`, `VERIFY_PHYSICAL_PLAUSIBILITY`, `INTERPRET_RESULT`.

The registry separately maps the P-C scope-level expectations into those roles. In particular, P-C `COMPARE` is realized by `REPRESENT` + `INTERPRET_RESULT`; P-D does not silently add a new canonical reasoning role.

## Motion pilot

The pilot defines all **14 P-C-bound Physics problem families**, **14 verification routes**, and **17 item semantic profiles** (Q1–Q14 plus Q14.a/b/c). Important cases remain upstream-safe:

- Q8 explicitly uses `SIGNED_AREA`; signed displacement is not collapsed into distance magnitude.
- Q10 carries phase topology and state handoff through `IDENTIFY_PHASES → PROPAGATE_STATE → CHECK_CONTINUITY_OR_BOUNDARY`.
- Q11 retains the common reference frame for relative acceleration.
- Q12 preserves slope + option-discrimination semantics.
- Q13 remains `BLOCKED` with `UNRESOLVED_DUE_SOURCE`; the missing graph is not reconstructed.
- Q14 and subparts remain `BLOCKED` / `REVIEW_REQUIRED`; structural demand is represented but the learner-facing difficulty badge is withheld.

## Model validity and relation choice

Model validity is a route step, not a rendering footnote. Constant-acceleration, constant-g, release, multi-phase, relative-motion and projectile families must carry an explicit `CHECK_MODEL_VALIDITY` step. A relation is chosen from **knowns + target + licensed model**, never by surface formula matching.

## Demand semantics

Demand is a sparse 15-dimensional vector (model selection, frame/sign, representation translation, state tracking, phase count, vector/spatial reasoning, graph interpretation, equation construction/elimination, hidden conditions, reasoning-chain length, constraint density, concept combination, verification demand, numerical load, time pressure).

`EASY / MEDIUM / HARD` is derived only by `PHY-GUIDE-DEMAND-POLICY-v1` with `badge_class = GUIDE_ASSIGNED_REASONING_DEMAND` and `psychometric_claim = false`. `HARD` additionally requires route depth, role diversity and verification evidence. Upstream-blocked items retain demand vectors but withhold a learner-facing badge.

## Exit gate

Every mapped P-C item must have a P-D family binding, PhysicsReasoningRoute, model-validity binding, verification route and multidimensional demand vector while preserving P-C blocked/diagnostic states.

Next phase after merge: **#253 / P-E — optional learner evidence and diagnostic inference**.
