# Physics Blueprint — AgentTasks intake boundary

Status: **BLUEPRINT CONSUMER BOUNDARY / NON-AUTHORIZING DELEGATION CONTEXT**

`Shared/AgentTasks` may hand Physics Blueprint a deterministic execution packet, but that packet is not a source of Physics scope, domain truth, Engineering readiness, learner mastery, consumer authorization, publication authority, or execution-route authority.

The direction is:

```text
human execution intent
  -> Shared/AgentTasks packet
  -> Physics Blueprint intake receipt
  -> exact repository-owned execution route REQUIRED
  -> repository-governed P-A/P-B/P-C scope derivation
  -> mandatory P-C.5 Shared EngineeringGate evaluation
  -> P-D and downstream Blueprint chain
```

The intake receipt proves only that Blueprint received a schema-valid, digest-valid, current-HEAD packet whose bound subject matches Physics and whose bound authority files still match their SHA-256 digests. It preserves execution intent and human-facing labels for orchestration/audit while explicitly marking those labels as non-authoritative.

## What Blueprint may consume from the packet

- task identity and task kind;
- engineering depth as requested execution/research intent;
- learner state as treatment context only;
- whether broad web research is allowed;
- requested downstream consumers as intent only;
- analyze-only versus implementation mode;
- grade/curriculum/topic/subtopic as non-authoritative labels for audit and display.

## What Blueprint must never consume from the packet as authority

- which `QuestionSet` or `DeclaredTopicScope` should start P-A;
- exact assessment scope or capability closure;
- Physics laws, models, relations, prerequisites or problem-family truth;
- Engineering readiness or technical closure;
- provider-owned external prerequisite authority;
- consumer permission;
- publication or human-review authorization.

Those remain repository-governed and are recomputed by the existing chain. In particular, natural-language `topic` or `subtopic` labels may not select a Blueprint branch, registry row, assessment-input set, Engineering gate, capability set, or source set.

## Current execution-route state

The repository currently has authority for:

```text
QuestionSet + DeclaredTopicScope
  -> P-A AssessmentIntake
  -> P-B AssessmentReview
  -> P-C AssessmentScope

P-C capabilities
  -> ColdStart engineering-scope bindings
  -> P-C.5 EngineeringGate
```

It does **not** currently declare a repository-owned mapping from a delegated task to the exact `QuestionSet + DeclaredTopicScope` pair that should start P-A. `GENERATION_AUTHORITY_MANIFEST.json` names the current runtime artifacts; it is not a general task-routing registry.

Therefore every current AgentTasks intake receipt must expose:

```text
execution_route.status = HELD_NO_REPOSITORY_ROUTE
execution_route.execution_authorized = false
execution_route.required_authority = REPOSITORY_OWNED_TASK_TO_ASSESSMENT_INPUT_ROUTE
execution_route.label_inference = PROHIBITED
```

This is an architectural hold, not a failed packet. The packet remains valid delegation context; concrete Blueprint execution is withheld because the missing authority may not be invented from free text, model memory, a case ID, or a topic-specific conditional.

## Fail-closed rules

`engine/consume_agent_task_packet.py` rejects:

- schema-invalid or digest-tampered packets;
- internally inconsistent packet custody;
- packets bound to a different repository HEAD;
- drift in any exact bound authority file;
- packets whose bound subject is not Physics;
- any packet that attempts to arrive with Engineering readiness, consumer authorization, or publication authority already asserted.

A successful intake emits `ACCEPTED_AS_DELEGATION_CONTEXT`, not `READY`, `AUTHORIZED`, `PROMOTED`, or execution permission.

## Regression ownership

All regression and stress validation for this boundary runs through `.github/workflows/v2-physics-blueprint.yml` and `Blueprint/tests/test_blueprint_agent_task_intake.py`.

The metamorphic requirement is:

```text
topic/subtopic change
learner-state change
STANDARD -> RESEARCH
requested-consumer change
        |
        v
packet intent/custody may change
Blueprint authority boundary must not change
execution route must remain HELD until exact repository route authority exists
```

No named subject topic is required by this proof. Synthetic labels are sufficient and preferred.

## Future execution wiring

Concrete execution may be enabled only when the authoritative Physics architecture owns an exact task-to-assessment-input route that binds to repository artifacts and has its own custody/falsifier coverage. The route should resolve identifiers to exact repository refs/digests; it must not infer scope from free-text labels or introduce a task-owned subject profile.

Once such authority exists, the intake consumer may use it to choose exact P-A inputs. P-A/P-B/P-C must still derive scope normally, P-C.5 must still recompute Engineering readiness, and no route may bypass existing Blueprint phases or publication/human-review boundaries.
