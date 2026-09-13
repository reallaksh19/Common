# Grade 9 V2 — Learning Blueprint

This directory is the cross-subject evidence/control/reasoning layer above subject-specific Core1/Core2/Core1A/Core2A production systems.

The blueprint does **not** contain the subject answers. It governs what evidence exists, which specialist runs first, what each specialist must independently inspect, when packets may be revealed, how claims are validated, and when downstream pedagogy is allowed to proceed.

## v0 — evidence and adaptive routing

v0 establishes:

- original evidence and derived claims as separate namespaces;
- Core1-first and Core2-first as equally legal routes;
- routing from evidence state rather than fixed sequence;
- explicit BLOCK states for insufficient evidence and material conflict;
- maximum three subtopics per handoff without limiting later learning-atom decomposition;
- absence/unknown evidence preserved rather than converted into zero importance;
- owner overrides that change operational action while retaining the system finding.

Convenience entrypoint:

```bash
python 'Grade 9/V2/LearningBlueprint/engine/run_blueprint_v0.py' \
  --ground-truth path/to/ground-truth.json \
  --routing-input path/to/routing-input.json \
  --out-dir build/blueprint-v0
```

## v1 — independent Core1/Core2 intelligence and Join

v1 makes the fresh-agent boundary executable at the artifact level.

```text
v0 route
   ↓
FIRST SPECIALIST
original evidence only
   ↓
freeze blind pass
   ↓
SECOND SPECIALIST
fresh instance, original evidence only
   ↓
freeze blind pass
   ↓
only now reveal first packet
   ↓
claim-by-claim V-* comparison
   ↓
Core1 × Core2 Join
   ↓
J-* + OBL-* assimilation obligations
```

The second specialist blind pass may not contain upstream packet references. Its packet must be frozen before reveal. Every first-specialist claim must then receive exactly one explicit comparison status:

```text
CONFIRMED
REFINED
MISSING
UNSUPPORTED
CONTRADICTED
OUT_OF_SCOPE
UNKNOWN
```

The Join is not a prose summary. It computes the capability topology:

- assessment capability + semantic support → assimilation obligation;
- assessment capability without semantic support → `BLOCK_MISSING_SEMANTIC_SUPPORT`;
- material contradiction → `BLOCK_CONFLICT`;
- semantic capability without assessment demand → preserved explicitly as **no assessment-demand evidence**, never downgraded to low importance.

v1 entrypoint:

```bash
python 'Grade 9/V2/LearningBlueprint/engine/run_blueprint_v1.py' \
  --route build/blueprint-v0/routing_packet.json \
  --first-pass path/to/first-specialist.json \
  --second-pass path/to/second-specialist.json \
  --validation path/to/validation-packet.json \
  --out-dir build/blueprint-v1
```

The route decides whether Core1 or Core2 is first. Supplying the opposite order fails closed.

## What v1 still does not claim

The repository runner validates independently produced specialist artifacts; it does not itself host an LLM runtime or claim that a GitHub Actions job can instantiate a fresh model. The protocol nevertheless makes the epistemic boundary machine-checkable: blind access state, separate instance IDs, freeze digests, reveal order, claim coverage and Join eligibility are all enforced.

Later milestones will add learner-state compilation, purpose contracts, Core1A cognitive transformation / learning-atom / inference-chain / equation-assimilation / representation-selection stages, taught-state receipts, Core2A transfer eligibility, and finally the one-command blueprint-to-Core1/Core2/Core1A/Core2A production build.
