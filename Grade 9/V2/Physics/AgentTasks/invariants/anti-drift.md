# Universal Anti-Drift Invariants

These invariants govern every execution task across the repository. They are fail-closed, non-negotiable architectural axioms. Any agent execution that violates these rules must be rejected by automated validators and human reviewers.

---

### Invariant A: Repository authority overrides memory
The current git repository state at the designated target commit HEAD is the sole source of architectural truth. Any prior memory, external assumptions, or conversational recollections are strictly advisory and subordinate to repository code, schemas, and manifests.

### Invariant B: Current schemas override examples
When an existing code fixture or legacy example contradicts a schema defined in `contracts/`, the schema is normative. Do not copy deprecated patterns from older files; adhere strictly to the active Draft 2020-12 schema definitions.

### Invariant C: Generated/canonical authority overrides diagnostic projections
Canonical artifacts (authoritative knowledge graphs, validated registries, and published manuscripts) hold authority over runtime diagnostic projections or temporary student-state projections. Diagnostic lenses observe canonical truth; they never dictate or rewrite it.

### Invariant D: Case facts belong in governed data, not global logic
All subject-matter parameters, pedagogical steps, numerical constants, and curriculum bindings belong in governed JSON/data files, never hardcoded as conditional branches (`if topic == '...'`) inside shared engines.

### Invariant E: A normal new subtopic must not require Blueprint case branches
The introduction of an ordinary new subtopic must be achievable entirely via `DATA_ONLY` additions. If an engine or Blueprint requires case-specific code branches to accept a new subtopic, the architecture has suffered case coupling.

### Invariant F: Missing evidence remains UNKNOWN/HELD/MISSING; never infer it
If a source, answer derivation, prerequisite edge, or rubric score lacks empirical or repository evidence, it must remain explicitly designated as `UNKNOWN`, `HELD`, or `MISSING`. An agent must never fabricate or heuristically hallucinate missing evidence.

### Invariant G: Learner state may change treatment, not disciplinary truth
Learner cognitive states (e.g., `NOVICE`, `MISCONCEPTION_ACTIVE`) govern pedagogical pacing, scaffolding depth, and representation sequences. Learner state must never alter disciplinary truth, mathematical laws, or physical invariants.

### Invariant H: Research depth may add evidence/depth; it may not silently mutate validated base truth
Switching from `FOUNDATION` or `STANDARD` to `RESEARCH` depth permits richer citations, historical debates, advanced limiting cases, and experimental caveats. It must never alter or invalidate the validated foundation theorems.

### Invariant I: External-domain authority must not be fabricated by the subject adapter
Subject adapters (e.g. Physics, Chemistry, Mathematics) must operate within their declared disciplinary boundaries. Cross-domain prerequisites (e.g. Physics relying on Calculus or Coordinate Geometry) must reference governed cross-domain contracts rather than inventing pseudo-mathematical authority.

### Invariant J: Publication authority must not be inferred from technical readiness
Passing a technical syntax check or schema validation is necessary but insufficient for publication. Final release authorization requires explicit human review clearance, complete provenance ledger binding, and custody seal verification.

### Invariant K: Same-ID mutated content must be rejected through digest/custody validation
Any artifact sharing an existing ID but bearing modified semantic content without an explicit version increment and digest match must be rejected as an integrity violation.

### Invariant L: New workflows/code paths require justification as a new invariant class
Introducing a new engine execution path, CLI flag, or workflow stage requires formal justification showing why existing generic abstractions cannot accommodate the requirement.

### Invariant M: If the requested result cannot be reached honestly, leave the state blocked and report exactly why
`BLOCKED` with precise evidence is a completely valid and successful execution outcome. An agent must never weaken validation rules, fabricate evidence, bypass assertions, or mark unverified tests as `PASS` merely to appear complete.
