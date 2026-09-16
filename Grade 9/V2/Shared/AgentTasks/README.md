# Shared AgentTasks — Thin Delegation Kernel

Status: **EXECUTION INFRASTRUCTURE / NON-AUTHORITATIVE**

This package delegates bounded work to a clean agent without becoming a second source of Learning Engineering, subject, Engineering Gate, learner, route, or publication authority.

Authority direction is one-way:

```text
current repository authority
  -> LearningEngineering / subject authority / CrossDomain / EngineeringGate
  -> Shared/AgentTasks authority resolution
  -> deterministic execution packet
  -> clean executing agent / governed consumer
```

`Shared/AgentTasks` may bind exact repository refs and digests, classify an execution task, validate an execution report, and render a derived Engineering preflight. It must not define SKP semantics, subject ontology, source authority, Engineering readiness, learner truth, route semantics, or publication authority.

## T1 scope

The T1 kernel contains:

- `contracts/execution-task.schema.json` — human task intent only;
- `contracts/execution-packet.schema.json` — exact authority-bound delegation packet;
- `contracts/execution-report.schema.json` — execution outcome distinct from Engineering/readiness/release state;
- `registry/authority-routing.v1.json` — non-semantic routing to current repository authorities;
- `registry/task-kind-registry.v1.json` — non-semantic execution permissions and required outputs;
- `engine/resolve_execution_authority.py` — exact HEAD + authority digest resolution;
- `engine/compile_execution_packet.py` — deterministic packet compiler;
- `engine/validate_execution_report.py` — packet/report custody validation;
- `tests/test_execution_kernel.py` — determinism, stale-custody, anti-authority and anti-case-coupling falsifiers.

There are deliberately no task-owned subject profiles and no family of authoritative prose prompt templates.

## Optional opaque execution-route request

`ExecutionTask.execution_route_id` is optional. It is an opaque request passed through the delegation layer; AgentTasks does not parse it, infer its meaning, map it from `topic`/`subtopic`, or resolve it to subject artifacts.

A governed consumer may resolve the exact ID only through its current repository-owned subject authority. An absent or unknown route may remain held. A resolved route may authorize only the consumer-specific action explicitly granted by that subject authority; it does not change Engineering readiness, domain truth, learner state, consumer permissions, publication, or human-review state.

This preserves the rule:

```text
free-text intent != execution-route authority
opaque route request != subject truth
resolved route != downstream readiness
```

## Current Learning Engineering limitation

The compiler reads the current `Shared/LearningEngineering/registry/skp-schema-roadmap.v1.json` rather than pretending the future SKP runtime already exists. At the initial T1 baseline the shared SKP modules are design/PILOT/PLANNED objects and subject SKP adapters are not runtime authority. The preflight therefore reports the exact roadmap state and leaves Engineering readiness `NOT_EVALUATED` unless a downstream governed Engineering compiler has actually produced an authoritative envelope.

## Basic use

```bash
python Grade\ 9/V2/Shared/AgentTasks/engine/compile_execution_packet.py \
  --task Grade\ 9/V2/Shared/AgentTasks/fixtures/valid/physics-subtopic-engineering.task.json \
  --output /tmp/execution-packet.json
```

A packet compiled from a stale explicit SHA fails closed. Changing any bound authority file changes the packet digest. Publication remains independently governed and is always `NOT_IMPLIED` by this layer.
