# StandaloneExecutionPrompt (SEP) Architecture & Cold-Start Agent System

The **StandaloneExecutionPrompt (SEP)** system under `Grade 9/V2/Physics/AgentTasks/` provides a governed, zero-memory execution framework for autonomous AI coding and research agents.

It ensures that any competent agent can receive **one self-contained prompt file**, open the repository cold, establish architectural ground truth, execute complex academic and engineering tasks for Grades 9–11 competitive exams (CBSE, JEE Main, JEE Advanced, NEET, IOQM), verify its work with executable falsifiers, and return a standardized report—without requiring conversational memory or out-of-band context.

---

## Directory Layout

```text
Grade 9/V2/Physics/AgentTasks/
├── contracts/
│   ├── execution-task.schema.json      # Draft 2020-12 input contract
│   ├── execution-report.schema.json    # Draft 2020-12 output report contract
│   └── validate_contracts.py          # Schema validator script
├── invariants/
│   ├── anti-drift.md                  # Universal Anti-Drift Invariants (A-M)
│   ├── repository-discovery.md        # 10-step cold-start discovery protocol
│   └── completion-report.md           # 14-section standardized Markdown + JSON report
├── subject-profiles/
│   └── physics.json                   # Physics ontology, representations & falsifiers
├── templates/
│   ├── SEP-01-architecture-discovery.md
│   ├── SEP-02-task-composer.md
│   ├── SEP-03-skp-ontology.md
│   ├── SEP-04-skp-schema.md
│   ├── SEP-05-source-governance.md
│   ├── SEP-06-subtopic-discovery.md
│   ├── SEP-07-subtopic-engineering-build.md
│   ├── SEP-08-architecture-stress-test.md
│   ├── SEP-09-research-depth-build.md
│   ├── SEP-10-curriculum-binding-research.md
│   ├── SEP-11-source-research-worker.md
│   ├── SEP-12-question-bank-miner.md
│   ├── SEP-13-problem-family-miner.md
│   ├── SEP-14-misconception-pck-research.md
│   ├── SEP-15-representation-design.md
│   ├── SEP-16-prerequisite-graph-audit.md
│   ├── SEP-17-independent-reproduction.md
│   ├── SEP-18-cross-agent-reconciliation.md
│   ├── SEP-19-physics-adapter.md
│   ├── SEP-22-legacy-migration.md
│   ├── SEP-23-library-coverage-audit.md
│   ├── SEP-24-core-architecture-document.md
│   └── SEP-25-architecture-falsification.md
├── engine/
│   ├── compile_execution_prompt.py     # Deterministic prompt compiler with linter
│   ├── validate_execution_report.py   # Output report validator
│   └── composer_ui.html               # Interactive browser Task Composer
├── fixtures/
│   ├── sample_relative_motion_task.json
│   ├── compiled_relative_motion_prompt.md
│   └── sample_execution_report.json
├── tests/
│   └── test_agent_tasks_engine.py      # Unit and regression test suite
└── README.md
```

Non-physics disciplinary adapters and profiles are isolated under `Grade 9/V2/General/` (e.g. `General/subject-profiles/mathematics.json`, `General/templates/SEP-20-mathematics-adapter.md`, `General/templates/SEP-21-chemistry-adapter.md`) ensuring that `Grade 9/V2/Mathematics/` and `Grade 9/V2/Chemistry/` production trees remain completely untouched.

---

## The 17-Section Standalone Execution Prompt Structure

Every generated prompt enforces the outer structure:

```text
EXECUTION PROMPT
│
├── 0. Editable Inputs              # ONLY section requiring human modification
├── 1. Mission                      # Task objective and constraints
├── 2. Repository / Branch Authority# Target branch, baseline PR, manifests
├── 3. Cold-Start Discovery         # 10 mandatory discovery steps
├── 4. Existing Architecture        # Normative schemas & subject profile rules
├── 5. Task Scope                   # In-scope items and boundaries
├── 6. Required Deliverables        # Exact file list to generate
├── 7. Allowed Changes              # Allowed modification tiers (DATA_ONLY, SCHEMA, etc.)
├── 8. Prohibited Changes           # Forbidden actions (e.g. BLUEPRINT_CHANGE)
├── 9. Anti-Drift Invariants        # Universal fail-closed axioms A through M
├── 10. Research / Source Policy    # Permitted source tiers and citation rules
├── 11. Implementation Procedure    # Step-by-step workflow
├── 12. Mandatory Falsifiers        # Executable checks that must pass
├── 13. Tests / CI                  # Test suites and workflows to run
├── 14. Acceptance Criteria         # Deterministic completion definitions
├── 15. Stop / Block Conditions     # Explicit permission and requirements for BLOCKED
└── 16. Exact Completion Report     # 14-section Markdown + machine JSON contract
```

---

## Universal Anti-Drift Invariants

Every prompt embeds the 13 universal invariants:

- **Invariant A**: Repository authority overrides memory.
- **Invariant B**: Current schemas override examples.
- **Invariant C**: Generated/canonical authority overrides diagnostic projections.
- **Invariant D**: Case facts belong in governed data, not global logic.
- **Invariant E**: A normal new subtopic must not require Blueprint case branches.
- **Invariant F**: Missing evidence remains UNKNOWN/HELD/MISSING; never infer it.
- **Invariant G**: Learner state may change treatment, not disciplinary truth.
- **Invariant H**: Research depth may add evidence/depth; it may not silently mutate validated base truth.
- **Invariant I**: External-domain authority must not be fabricated by the subject adapter.
- **Invariant J**: Publication authority must not be inferred from technical readiness.
- **Invariant K**: Same-ID mutated content must be rejected through digest/custody validation.
- **Invariant L**: New workflows/code paths require justification as a new invariant class.
- **Invariant M**: If the requested result cannot be reached honestly, leave the state blocked and report exactly why.

---

## CLI Usage

### 1. Compile a Standalone Prompt
```bash
python "Grade 9/V2/Physics/AgentTasks/engine/compile_execution_prompt.py" \
  --task-file "Grade 9/V2/Physics/AgentTasks/fixtures/sample_relative_motion_task.json" \
  --output "output/SEP-PHY-RELMOTION-v1.md"
```

### 2. Validate Execution Report
```bash
python "Grade 9/V2/Physics/AgentTasks/engine/validate_execution_report.py" \
  "Grade 9/V2/Physics/AgentTasks/fixtures/sample_execution_report.json"
```

### 3. Run Test Suite
```bash
python -m unittest "Grade 9/V2/Physics/AgentTasks/tests/test_agent_tasks_engine.py"
```

### 4. Interactive Browser UI
Open `Grade 9/V2/Physics/AgentTasks/engine/composer_ui.html` in any web browser to interactively configure tasks and download JSON payloads.
