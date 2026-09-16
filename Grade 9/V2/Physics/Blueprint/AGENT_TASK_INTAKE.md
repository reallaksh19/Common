# Physics Blueprint — AgentTasks intake boundary

Status: **BLUEPRINT CONSUMER BOUNDARY / NON-AUTHORIZING DELEGATION CONTEXT**

`Shared/AgentTasks` may hand Physics Blueprint a deterministic execution packet, but that packet is not a source of Physics scope, domain truth, Engineering readiness, learner mastery, consumer authorization, or publication authority.

The direction is:

```text
human execution intent
  -> Shared/AgentTasks packet
  -> Physics Blueprint intake receipt
  -> repository-governed P-A/P-B/P-C scope derivation
  -> mandatory P-C.5 Shared EngineeringGate evaluation
  -> P-D and downstream Blueprint chain
```

The intake receipt proves only that Blueprint received a schema-valid, digest-valid, current-HEAD packet whose bound subject matches Physics. It preserves execution intent and human-facing labels for orchestration/audit while explicitly marking those labels as non-authoritative.

## What Blueprint may consume from the packet

- task identity and task kind;
- engineering depth as requested execution/research intent;
- learner state as treatment context only;
- whether broad web research is allowed;
- requested downstream consumers as intent only;
- analyze-only versus implementation mode;
- grade/curriculum/topic/subtopic as non-authoritative labels for audit and display.

## What Blueprint must never consume from the packet as authority

- exact assessment scope or capability closure;
- Physics laws, models, relations, prerequisites or problem-family truth;
- Engineering readiness or technical closure;
- provider-owned external prerequisite authority;
- consumer permission;
- publication or human-review authorization.

Those remain repository-governed and are recomputed by the existing chain. In particular, natural-language `topic` or `subtopic` labels may not select a Blueprint branch, registry row, Engineering gate, capability set, or source set.

## Fail-closed rules

`engine/consume_agent_task_packet.py` rejects:

- schema-invalid or digest-tampered packets;
- internally inconsistent packet custody;
- packets bound to a different repository HEAD;
- packets whose bound subject is not Physics;
- any packet that attempts to arrive with Engineering readiness, consumer authorization, or publication authority already asserted.

A successful intake emits `ACCEPTED_AS_DELEGATION_CONTEXT`, not `READY`, `AUTHORIZED`, or `PROMOTED`.

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
```

No named subject topic is required by this proof. Synthetic labels are sufficient and preferred.

## Future execution wiring

This intake receipt is intentionally not yet a scope router. If a future task packet is allowed to initiate a concrete Blueprint run, the execution route must be resolved through an exact repository-governed binding produced by the authoritative subject architecture. It must not be inferred from free-text topic labels or introduced as a task-owned subject profile.
