# Physics Blueprint — AgentTasks intake boundary

Status: **BLUEPRINT CONSUMER BOUNDARY / GOVERNED P-A ROUTE SELECTION / NON-AUTHORIZING DOWNSTREAM**

`Shared/AgentTasks` may hand Physics Blueprint a deterministic execution packet, but that packet is not a source of Physics scope, domain truth, Engineering readiness, learner mastery, consumer authorization, publication authority, or route semantics.

The direction is:

```text
human execution intent
  -> optional opaque execution_route_id
  -> Shared/AgentTasks packet
  -> Physics Blueprint intake receipt
  -> current Physics generation manifest
  -> repository-owned exact route registry
  -> exact QuestionSet + DeclaredTopicScope (+ optional AttemptSet)
  -> P-A AssessmentIntake
  -> P-B AssessmentReview
  -> P-C AssessmentScope
  -> mandatory P-C.5 Shared EngineeringGate evaluation
  -> P-D and downstream Blueprint chain
```

The intake receipt proves that Blueprint received a schema-valid, digest-valid, current-HEAD packet whose bound subject matches Physics and whose bound authority files still match their SHA-256 digests. If an opaque route ID is requested, Blueprint resolves it only through the route registry declared by the exact bound Physics generation manifest.

## What Blueprint may consume from the packet

- task identity and task kind;
- optional `execution_route_id` as an opaque selection request only;
- engineering depth as requested execution/research intent;
- learner state as treatment context only;
- whether broad web research is allowed;
- requested downstream consumers as intent only;
- analyze-only versus implementation mode;
- grade/curriculum/topic/subtopic as non-authoritative labels for audit and display.

## What Blueprint must never consume from the packet as authority

- route meaning inferred from the route ID string;
- a `QuestionSet` or `DeclaredTopicScope` path supplied by free text;
- exact assessment scope or capability closure;
- Physics laws, models, relations, prerequisites or problem-family truth;
- Engineering readiness or technical closure;
- provider-owned external prerequisite authority;
- consumer permission;
- publication or human-review authorization.

Natural-language `topic` or `subtopic` labels may not select a Blueprint branch, registry row, assessment-input set, Engineering gate, capability set, or source set. The route resolver performs exact ID equality only.

## Repository-owned execution-route authority

The current Physics generation manifest declares:

```text
authorities.agent_task_execution_routes
  -> Grade 9/V2/Physics/Blueprint/registry/physics-agent-task-execution-routes.v1.json
```

That registry has explicit semantics:

```text
selector_semantics = OPAQUE_EXACT_ROUTE_ID
label_inference_allowed = false
```

Each ACTIVE route binds exact repository paths for:

```text
QUESTION_SET            required
DECLARED_TOPIC_SCOPE    required
ATTEMPT_SET             optional
```

At intake time Blueprint requires the packet HEAD to match the current checkout, re-verifies every packet-bound authority digest, verifies the Physics generation manifest digest, verifies the route-registry schema and digest, requires a clean checkout before resolving a route, and emits SHA-256 bindings for the selected P-A input artifacts.

The authorization scope is deliberately narrow:

```text
execution_route.authorization_scope = P-A_INPUT_SELECTION_ONLY
```

A resolved route does **not** authorize P-C scope, Engineering readiness, P-D consumption, Core authoring, publication, or human review. Those remain governed by their existing authorities.

## Route states

No route requested:

```text
execution_route.status = HELD_NO_ROUTE_REQUESTED
execution_route.execution_authorized = false
```

Unknown exact route ID:

```text
execution_route.status = HELD_ROUTE_UNRESOLVED
execution_route.execution_authorized = false
```

Exact current route resolves:

```text
execution_route.status = RESOLVED_REPOSITORY_ROUTE
execution_route.execution_authorized = true
execution_route.authorization_scope = P-A_INPUT_SELECTION_ONLY
execution_route.input_bindings = exact path + SHA-256 bindings
```

These states separate valid delegation context from route resolution and from every downstream authority decision.

## Fail-closed rules

`engine/consume_agent_task_packet.py` rejects:

- schema-invalid or digest-tampered packets;
- internally inconsistent packet custody;
- packets bound to a different repository HEAD;
- drift in any exact bound authority file;
- invalid or digest-drifted subject generation manifests;
- invalid or digest-drifted route registries;
- duplicate route IDs, roles or paths;
- route rows missing required P-A inputs;
- route input paths outside the Physics subject tree;
- route resolution from a dirty checkout;
- packets whose bound subject is not Physics;
- any packet that attempts to arrive with Engineering readiness, consumer authorization, or publication authority already asserted.

## Regression ownership

All regression and stress validation for this boundary runs through `.github/workflows/v2-physics-blueprint.yml` and `Blueprint/tests/test_blueprint_agent_task_intake.py`.

The principal metamorphic proof is:

```text
same opaque route ID
+ arbitrary topic/subtopic change
+ grade/curriculum label change
+ learner-state change
+ STANDARD -> RESEARCH
+ requested-consumer change
        |
        v
packet intent/custody may change
resolved P-A input bindings must not change
Blueprint downstream authority boundary must not change
```

An unknown route ID must remain held even when free-text labels exactly resemble an existing topic. Conversely, the same valid route ID must select the same P-A inputs even when all non-authoritative labels change.

## Current execution boundary

The routed intake is now proven to feed the existing P-A `build_intake` engine with the exact repository-bound `QuestionSet` and `DeclaredTopicScope`, while the `AttemptSet` remains optional. This closes the task-to-P-A **input-selection** authority gap.

It does not yet make AgentTasks a replacement cold-start runner. Any future packet-triggered P-A→P-L orchestration must consume this receipt, preserve these exact input bindings, and traverse the existing P-A/P-B/P-C/P-C.5/P-D chain without bypasses or manual readiness.
