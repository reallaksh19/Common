# Standalone Delegation Layer / Task Composer

The **Standalone Delegation Layer / Task Composer** is a thin, domain-neutral client of current repository authority. It enables any autonomous AI coding or research agent to receive **one execution packet**, open the repository cold, discover authoritative manifests and engineering gates, execute a bounded task, test its work, and return a standardized execution report—without conversational memory or out-of-band context.

---

## Governing Invariants

1. **The execution packet is NOT an architecture authority**:
   The dependency direction is strictly top-down:
   ```text
   CURRENT REPOSITORY AUTHORITY
           ↓
   LearningEngineering / EngineeringGate / CrossDomain
           ↓
   Subject Authority and Adapters (Manifests)
           ↓
   Delegation / Task Compiler
           ↓
   Standalone Execution Packet
           ↓
   Clean Executing Agent
   ```
   A task prompt never invents architectural, pedagogical, or technical truth.

2. **Maximum flexibility in discovery; minimum flexibility in promotion**:
   - When `web_research_allowed = true`, agents may discover broadly from official curricula, textbooks, research papers, and question banks.
   - Discovery permission strictly does not imply canonical promotion permission (`DISCOVERY_PERMISSION != PROMOTION_PERMISSION`). Promotion is governed fail-closed by source provenance.

3. **Readiness is always derived, never asserted**:
   - `engineering_state = ENGINEERING_GATE_READY` can only be set if executable tests in `tests` pass. Manual assertions in inputs or candidate files fail validation.

4. **Zero case coupling in generic orchestration**:
   - No subtopic names, problem identifiers, or hardcoded leakage blacklists exist in generic compiler or validator logic.

5. **No Blueprint case branch**:
   - A normal new subtopic must not require `if topic == ...` in Blueprint or global engines.

6. **Separation of Completion, Engineering Readiness, and Publication**:
   - `execution_result` (`COMPLETE`, `PARTIAL`, `BLOCKED`) is distinct from `engineering_state` (`ENGINEERING_GATE_READY`, `HELD`, etc.).
   - A task can complete successfully by proving engineering remains `HELD`.
   - Publication strictly requires authorized human expert review (`PENDING_AUTHORIZED_HUMAN_REVIEW`) and cannot be inferred from engineering readiness.

---

## Directory Layout

```text
Grade 9/V2/AgentTasks/
├── contracts/
│   ├── execution-task.schema.json      # Draft 2020-12 human task intent schema
│   ├── execution-packet.schema.json    # Draft 2020-12 compiled packet schema
│   └── execution-report.schema.json    # Draft 2020-12 execution report schema
├── registry/
│   ├── task-kind-registry.json         # 13 data-driven task kinds (replaces prose templates)
│   └── subject-routing-registry.json   # Non-semantic routing (PHYSICS, MATHEMATICS, CHEMISTRY)
├── engine/
│   ├── resolve_execution_authority.py  # Git HEAD & authority digest resolver
│   ├── compile_execution_packet.py     # Deterministic packet compiler
│   ├── validate_execution_report.py    # Report validator enforcing fail-closed rules
│   └── engineering_preflight.py        # Non-authoritative Engineering Preflight / Map generator
├── cli.py                              # Unified command-line interface
├── fixtures/                           # Golden fixtures and negative falsifiers
└── tests/
    └── test_execution_kernel.py        # Comprehensive unit & falsifier test suite
```

---

## CLI Usage

### 1. Resolve Repository Authority
```bash
python "Grade 9/V2/AgentTasks/cli.py" resolve --subject PHYSICS
```

### 2. Compile an Execution Packet
```bash
python "Grade 9/V2/AgentTasks/cli.py" compile \
  --task "Grade 9/V2/AgentTasks/fixtures/sample_subtopic_engineering_task.json" \
  --out "output/packet.json"
```

### 3. Generate Non-Authoritative Engineering Preflight
```bash
python "Grade 9/V2/AgentTasks/cli.py" preflight --packet "output/packet.json"
```

### 4. Validate Execution Report
```bash
python "Grade 9/V2/AgentTasks/cli.py" validate-report \
  --report "Grade 9/V2/AgentTasks/fixtures/sample_execution_report.json" \
  --packet "output/packet.json"
```

### 5. Run Test Suite
```bash
python -m unittest "Grade 9/V2/AgentTasks/tests/test_execution_kernel.py"
```
