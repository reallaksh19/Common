# Physics V2 — P-E optional learner evidence and diagnostic inference

This directory implements **P-E / #253**. It consumes the fixed P-C assessment scope and the P-D learner-independent Physics problem semantics. `AttemptSet` is optional.

```text
same QuestionSet + DeclaredTopicScope + P-D semantics
                     ↓
              same assessment scope
                     ↓
       ┌─────────────┴─────────────┐
AttemptSet absent             AttemptSet present
       ↓                            ↓
UNKNOWN learner evidence      PhysicsReasoningObservation
no negative diagnosis         → shared LearnerEvidenceLedger
neutral/conservative          → shared DiagnosticCase
PROBE_FIRST if needed         → shared LearnerStateSnapshot
```

## Authority boundary

P-E may observe and localize learner evidence. It may not redefine canonical Physics truth, alter P-C scope, rewrite P-D reasoning routes, choose Study Synthesis treatment, author Core1 teaching, design H1/H2/H3 wording, schedule review, or make psychometric claims.

The same assessment must therefore produce the same scope fingerprint whether attempts are absent or present. Only learner-conditioned evidence, diagnostic cases and probe requirements may differ.

## Shared contracts

P-E reuses the subject-independent V2 contracts under:

`Grade 9/V2/Shared/LearnerIntelligence/contracts/`

for:

- `LearnerEvidenceLedger`
- `DiagnosticCase`
- `LearnerStateSnapshot`

Physics adds only:

- `PhysicsReasoningObservation`
- a Physics observation-code registry
- a Physics diagnostic inference policy
- the deterministic P-E inference engine and falsifiers

The superseded Physics-only `LearnerIntelligence` interface scaffold is removed by this phase so shared contracts remain the single cross-subject contract family.

## Required invariants

- `NO_ATTEMPT != PHYSICS_WEAK`.
- Assessment scope is invariant across absent/present attempt branches.
- Correct upstream system/frame/model/relation reasoning survives a later state, sign, graph or arithmetic failure.
- One wrong answer cannot confirm a misconception.
- Low-confidence evidence produces a probe requirement, not a confident negative learner state.
- P-B source-integrity and diagnostic-use restrictions remain binding.
- Blocked, defective, underdetermined or review-required items cannot punish the learner.
- Shared arithmetic/algebra execution cannot erase demonstrated Physics reasoning.
- Ambiguity remains ambiguity and requests a targeted probe.
- Observations bind exact item + reasoning-route step and, where relevant, exact source or semantic representation evidence.
- P-E may nominate a probe; treatment belongs downstream to P-F.
- No unsupported psychological cause may be inferred from answer-sheet evidence.
- Fixed upstream authority + fixed attempts/evidence + fixed policy yields deterministic bytes.

## Observation vocabulary

The registry includes the #253-required Physics mappings:

`CORRECT_SYSTEM_SELECTION`, `CORRECT_REFERENCE_FRAME`, `CORRECT_MODEL_SELECTION`,
`CORRECT_RELATION_SELECTION`, `CORRECT_STATE_EXTRACTION`,
`CORRECT_REPRESENTATION_TRANSLATION`, `INVALID_STATE_RESET`,
`OMITTED_PHASE_HANDOFF`, `SIGN_DIRECTION_MISMATCH`,
`DISTANCE_DISPLACEMENT_CONFUSION`, `GRAPH_HEIGHT_SLOPE_AREA_CONFUSION`,
`APEX_COMPONENT_AMBIGUITY`, `ARITHMETIC_EXECUTION_ERROR`,
`MODEL_VALIDITY_IGNORED`, `VERIFICATION_NOT_PERFORMED`, and
`VERIFICATION_FAILED`.

## Evidence semantics

A Physics observation is not a diagnosis. It must bind:

```text
attempt_ref
item_ref
route_step_ref
route_role
representation_ref?  # source representation or P-D semantic representation
observation_code
capability_refs[]
confidence tuple
evidence fragment
```

The effective confidence is the minimum of observation, extraction, transcription and attempt extraction confidence.

Negative inference is blocked when upstream P-B/P-D marks an item as blocked or excludes negative diagnostic use.

## Exit proof

CI reconstructs and re-proves P-A, P-B, P-C and P-D before P-E tests. It then proves:

1. no-attempt run → identical assessment scope + UNKNOWN learner evidence + no negative diagnosis;
2. attempt run → identical assessment scope + localized evidence-conditioned state;
3. demonstrated Physics reasoning remains credited when a later arithmetic, phase-handoff, sign or graph step fails;
4. one error remains probe-required rather than confirmed;
5. invalid/blocked source items cannot create negative diagnosis;
6. two independent high-confidence negative observations are required before `CONFIRMED`;
7. deterministic replay is byte-stable.

No StudyModel treatment, Core1 authoring, H1/H2/H3 wording, longitudinal promotion or publication layout is implemented here.
