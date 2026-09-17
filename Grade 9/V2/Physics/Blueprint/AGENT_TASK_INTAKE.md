# Physics Blueprint — AgentTasks intake boundary

Status: **BLUEPRINT CONSUMER BOUNDARY / GOVERNED P-A INPUT ROUTING / DOWNSTREAM AUTHORITY PRESERVED**

`Shared/AgentTasks` may hand Physics Blueprint a deterministic execution packet, but that packet is not a source of Physics scope, domain truth, Engineering readiness, learner mastery, consumer authorization, publication authority, or route semantics.

The authority direction is:

```text
human execution intent
  -> optional opaque execution_route_id
  -> Shared/AgentTasks packet
  -> Physics Blueprint intake receipt
  -> current Physics generation manifest
  -> repository-owned exact route registry
  -> exact QuestionSet + DeclaredTopicScope (+ optional AttemptSet)
  -> existing governed assessment/cold-start machinery
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

At intake time Blueprint requires the packet HEAD to match the current checkout, re-verifies every packet-bound authority digest, verifies the Physics generation manifest digest, verifies the route-registry schema and digest, requires a clean checkout before resolving a route, and emits SHA-256 bindings for the selected assessment-input artifacts.

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

## Routed cold-start seam

`ColdStart/engine/physics_cold_start_runner.py` now accepts optional digest-bound `assessment_input_bindings` for exactly the three assessment-input roles above. When they are absent, legacy manifest-driven behavior is unchanged. When they are present:

- the required `QUESTION_SET` and `DECLARED_TOPIC_SCOPE` must be present and required;
- `ATTEMPT_SET`, when present, must remain optional;
- every path must be repository-relative and inside the Physics tree;
- every file SHA-256 must match the resolved route receipt;
- the no-attempt run does not read the optional attempt set;
- the with-attempts run reads that exact bound attempt set;
- every other P-B/P-C/P-C.5/P-D/downstream authority still comes from the exact Physics generation manifest.

`Blueprint/engine/run_agent_task_cold_start.py` is the thin consumer of this seam. It requires `RESOLVED_REPOSITORY_ROUTE`, passes only the exact route bindings into the existing P-K production runner, executes the existing no-attempt and with-attempt runs, applies the existing cross-run invariants, and emits `blueprint-agent-task-cold-start.schema.json` custody.

The adapter deliberately does not claim that the P-K runner consumes a serialized P-A envelope. P-A compatibility is separately falsified by feeding the same route-bound artifacts through the existing `build_physics_assessment_intake` engine. The production guarantee is therefore precise: the route owns exact assessment-input selection; existing subject machinery owns interpretation and all downstream authority.

## Fail-closed rules

`engine/consume_agent_task_packet.py` rejects:

- schema-invalid or digest-tampered packets;
- internally inconsistent packet custody;
- packets bound to a different repository HEAD;
- drift in any exact bound authority file;
- invalid or digest-drifted subject generation manifests;
- invalid or digest-drifted route registries;
- duplicate route IDs, roles or paths;
- route rows missing required assessment inputs;
- route input paths outside the Physics subject tree;
- route resolution from a dirty checkout;
- packets whose bound subject is not Physics;
- any packet that attempts to arrive with Engineering readiness, consumer authorization, or publication authority already asserted.

The cold-start seam additionally rejects malformed route bindings, duplicate/unknown roles, missing required roles, out-of-subject paths, missing files, and any SHA-256 mismatch before using the routed input.

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
resolved assessment-input bindings must not change
Blueprint downstream authority boundary must not change
```

An unknown route ID remains held even when free-text labels resemble an existing topic. Conversely, the same valid route ID selects the same assessment inputs even when all non-authoritative labels change.

The end-to-end routed proof additionally compiles a real packet, resolves the current route, runs the existing two-mode P-K chain with those exact bindings, verifies identical assessment scope and Engineering truth across learner-evidence modes, and keeps publication and human-review authorization `NOT_IMPLIED`.

## Remaining limitation

This closes the task-to-assessment-input routing gap without making AgentTasks a subject authority. It does **not** create the future production SKP→Engineering promotion path: the LearningEngineering roadmap remains non-runtime design authority, bulk population remains blocked, and subject SKP adapters remain non-authorizing until separately promoted.
