# Mathematics M-I — Core2 transfer semantics

This layer turns the **original assessment questions** into a governed transfer surface.

It does not rewrite source questions, does not invent a second reasoning model, and does not claim that a planned Core1 lesson already exists when M-G is still waiting for legitimate PCK promotion.

## Authority chain

```text
AssessmentIntake QuestionSet
+ AssessmentReview item safety
+ AssessmentScope concept/capability bindings
+ ProblemSemantics reasoning route + demand vector + verification route
+ RepresentationSemantics teaching primitives
+ Core1 linkage state
        ↓
Core2TransferPlan
        ↓
one attempt-first TransferQuestionPage per source question
```

Each page preserves the exact source stem, givens, options, units and subparts, then adds support downstream of the attempt surface:

```text
H0  attempt original question
H1  notice the structure
H2  choose a representation/method
H3  take the first executable mathematical step
ReasoningRoute  explain why mathematical states connect
SolutionRoute   execute a complete solution
Verification    independently check the result
```

Hints, reasoning and solution are separate semantic objects.

## Core1 linkage and the M-G human-review gate

M-I can create deterministic learner-readable **planned** Core1 links from canonical capabilities. A planned link is not a publication claim.

```text
PLANNED_UNTIL_PCK_PROMOTED
    → semantic Core2 plan is allowed
    → publication_ready = false

MATERIALIZED from a PRODUCTION Core1 plan
    → publication_ready may become true
```

This lets the transfer architecture progress without bypassing the human PCK-promotion requirement in M-G.

## Reference assessment safety

The current Grade-9 fixture keeps all fourteen original questions visible. In particular:

- Q6 remains a transfer question even though M-C records it as outside the supplied declared-topic boundary.
- Q9 remains `UNDERDETERMINED`; negative learner inference is forbidden and the solution explains non-uniqueness.
- Q12 remains `VALID_MULTIPLE_SOLUTIONS`; both valid third vertices must survive through solution and verification.
- Q10, Q12 and Q14 keep their M-D `HARD` guide-demand badges only because their semantic routes are genuinely multi-stage.

## Representation closure

Every M-C representation demand is converted into an M-H `RepresentationPlan`. Renderers receive declared mathematical semantic data; they do not invent mathematical meaning.

## Executable falsifiers

The test suite blocks:

```text
HINT_EQUALS_SOLUTION
H1_DISCLOSES_H3
REASONING_ROUTE_EQUALS_HINT_COPY
SOURCE_MC_OPTIONS_MISSING
GENERIC_WORKSPACE_IGNORES_RESPONSE_SHAPE
OPAQUE_CORE1_LINK_ONLY
HARD_BADGE_WITHOUT_DEEP_REASONING_STRUCTURE
ORIGINAL_TRANSFER_LEAKED_INTO_CORE1_WORKED_EXAMPLE
SOLUTION_IS_ANSWER_ONLY
ASSESSMENT_SAFETY_POLICY_LOST
MULTI_SOLUTION_COLLAPSED
REPRESENTATION_PLAN_DRIFT
SOURCE_SHAPE_DRIFT
MISSING_TRANSFER_QUESTION
GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC
UNPROMOTED_CORE1_LINK_PUBLISHED
```

M-I is a semantic product contract, not final page typography/PDF approval. Final exact-product quality belongs downstream.
