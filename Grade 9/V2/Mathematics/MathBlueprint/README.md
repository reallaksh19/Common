# Mathematics V2 — Adaptive Math Blueprint

`MathBlueprint/` is the canonical Mathematics orchestration authority above Core1/Core2/Core1A/Core2A and the downstream production kits.

Its governing invariant is:

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.
```

Core1 and Core2 reconstruct different kinds of intelligence from the same original evidence. Either may execute first when the evidence justifies it. Neither becomes ground truth because it executed first.

## Implemented runtime

```text
Original evidence
      ↓
GroundTruthManifest
      ↓
MathLearningRunBlueprint
      ↓
GT_READY
      ↓
Adaptive Evidence Router
      ↓
CORE1_FIRST | CORE2_FIRST | BLOCK
      ↓
ROUTED
      ↓
fresh first-role specialist
      ↓
GROUND-TRUTH-ONLY context
      ↓
first intelligence package sealed
      ↓
fresh second-role specialist
      ↓
GROUND-TRUTH-ONLY independent context
(first package explicitly withheld)
      ↓
independent package sealed
      ↓
validation context unlocks both sealed packages
      ↓
claim-level cross-validation
      ↓
CROSS_VALIDATED
      ↓
Join / AssimilationDemand
      ↓
JOIN_READY | BLOCKED_CONFLICT
```

Increment 1 established immutable evidence binding and root run state. Increment 2 added adaptive routing, owner routing overrides and deterministic max-three handoff bundling. Increment 3 implemented the dual-intelligence independence firewall and claim-level cross-validation. Increment 4 now compiles validated intelligence, learner capability state, purpose and owner constraints into `AssimilationDemand`.

## Increment 1 — Ground truth + run blueprint

`GroundTruthManifest` records original question corpus, syllabus, authoritative source/textbook, answer key, solution set and figure set.

Evidence availability is explicit:

```text
PRESENT
ABSENT
PARTIAL
UNRESOLVED
CONFLICTED
```

`ABSENT` means evidence is absent. It cannot be translated into low importance, low difficulty, out-of-scope status, learner weakness or a claim that the topic is not assessed.

Only `ORIGINAL_EVIDENCE` and `AUTHORITATIVE_SOURCE` are legal ground-truth authority classes. Derived claims, benchmarks, agent conclusions and owner overrides remain outside ground truth.

Every downstream artifact belongs to one `MathLearningRunBlueprint`. `run_id` remains stable while `run_digest` changes as state evolves. Learner prior, learning purpose and product mode remain separate control-plane fields.

The relay transport constraint is:

```text
1 <= subtopics per bundle <= 3
```

This does not limit learning atoms, equations, inference edges, representations or teaching steps.

## Increment 2 — Adaptive Relay / EvidenceRouter

Routing profiles each candidate subtopic with:

```text
SA  scope authority
SS  semantic source strength
QE  question evidence
QR  question resolution
UA  uncertainty
CI  conflict index
```

Derived strengths are:

```text
semantic_strength   = max(SA, SS)
assessment_strength = min(QE, QR)
```

Routing is deterministic:

```text
material conflict
→ BLOCK_CONFLICT

semantic_strength <= 1 and assessment_strength <= 1
→ BLOCK_EVIDENCE

strong semantic authority
→ CORE1_FIRST

otherwise rich + resolved question evidence
→ CORE2_FIRST

otherwise
→ BLOCK_OWNER_REVIEW
```

Owner routing control stores `SYSTEM ACTION`, `OWNER OVERRIDE` and `FINAL ACTION` separately. `HARD` may change execution without rewriting evidence; `SOFT` may select only an already admissible role.

## Increment 3 — Dual intelligence + independence firewall

Core1 semantic claims include:

```text
CONCEPT / MODEL / LAW / EQUATION / DERIVATION
PREREQUISITE / CONSTRAINT / INVARIANT / STATE
VALIDITY / CONCEPT_BOUNDARY
REPRESENTATION_AFFORDANCE / STRUCTURAL_CONTRAST
```

Core2 assessment claims include:

```text
QUESTION_DEMAND / RECOGNITION_CUE / HIDDEN_CONSTRAINT
REQUIRED_CAPABILITY / FIRST_NON_OBVIOUS_MOVE
REPRESENTATION_SWITCH / REASONING_CHAIN / WRONG_CHAIN
DIFFICULTY_VECTOR / PROBLEM_FAMILY / MISCONCEPTION
SOLUTION_STRUCTURE / TRANSFER_ENVELOPE
```

The runtime enforces:

```text
FIRST_ROLE_ANALYSIS
  context = GROUND_TRUTH_ONLY

SECOND_ROLE_INDEPENDENT
  context = GROUND_TRUTH_ONLY
  first package = WITHHELD
  second specialist = fresh instance

SECOND_ROLE_VALIDATION
  only after independent package is sealed
  context = GROUND_TRUTH_PLUS_UPSTREAM_VALIDATION
```

Every first-package claim must receive exactly one classification:

```text
CONFIRMED
REFINED
UNSUPPORTED
CONTRADICTED
OUT_OF_SCOPE
UNKNOWN
```

`MISSING` is separate and must reference an actual independently sealed second-role claim. Cross-validation never mutates either specialist package.

Key files:

```text
contracts/math-specialist-work-order.schema.json
contracts/math-agent-context-manifest.schema.json
contracts/math-specialist-package.schema.json
contracts/math-cross-validation.schema.json
contracts/math-dual-intelligence-session.schema.json
policies/math-dual-intelligence-policy.json
engine/run_dual_intelligence.py
tests/test_dual_intelligence.py
```

## Increment 4 — Join / AssimilationDemand

Join may run only after `CROSS_VALIDATED`.

```text
cross-validated Core1 semantic intelligence
        +
cross-validated / independently grounded Core2 assessment intelligence
        +
LearnerCapabilityState
        +
learning purpose
        +
owner constraints
        ↓
AssimilationDemand
```

### Learner capability state

Learner prior percentage remains provenance only. It does not automatically create mastery claims.

Capability readiness is limited to the existing vocabulary:

```text
UNKNOWN
DEVELOPING
READY
```

Each capability also records its basis:

```text
LEARNER_EVIDENCE
OWNER_DECLARED_BASELINE
UNKNOWN
```

An omitted capability is treated as `UNKNOWN`, not weak.

Join converts readiness into a pedagogical gap state:

```text
READY
→ NO_IDENTIFIED_GAP

DEVELOPING
→ BRIDGE_OR_PRACTICE_REQUIRED

UNKNOWN / UNLISTED
→ UNKNOWN_REQUIRES_PROBE_OR_FULL_SUPPORT
```

### Purpose is first-class

Join compiles purpose requirements separately from learner state.

`FIRST_STUDY`, `CONSOLIDATION`, `REVISION` and `COMPETITIVE_EXAM` have different terminal demands. Competition may increase recognition/transfer demand but carries an explicit `DO_NOT_SKIP_NECESSARY_FOUNDATIONS` requirement.

### Conflict and unknown preservation

Cross-validation results resolve as:

```text
CONFIRMED    → admissible as stated
REFINED      → admissible as refined
MISSING      → admissible independent finding
UNKNOWN      → preserved as unknown, not authority
UNSUPPORTED  → preserved as non-authoritative conflict
CONTRADICTED → preserved as non-authoritative conflict
OUT_OF_SCOPE → preserved as excluded conflict
```

Every conflict must be explicitly dispositioned as either:

```text
BLOCKING
or
DEFERRED with reason
```

An assimilation obligation may never cite `UNKNOWN`, `UNSUPPORTED`, `CONTRADICTED` or `OUT_OF_SCOPE` claims as authority.

### Assimilation obligations

Each obligation must state:

```text
obligation type
statement
origin claim refs
original evidence provenance
capability refs
learner gap states
whether required before Core2A
```

Allowed obligation types are:

```text
SEMANTIC_UNDERSTANDING
ASSESSMENT_RECOGNITION
PREREQUISITE
INFERENCE_BRIDGE
EQUATION_ASSIMILATION
REPRESENTATION
MISCONCEPTION_CONTRAST
TRANSFER
```

Owner constraints are carried with `authority_class = OWNER_CONTROL`; they never become evidence.

Increment 4 files:

```text
contracts/math-learner-capability-state.schema.json
contracts/math-assimilation-demand-build-spec.schema.json
contracts/math-assimilation-demand.schema.json
policies/math-assimilation-join-policy.json
engine/build_assimilation_demand.py
tests/test_assimilation_join.py
golden/assimilation/01-vieta-join-with-unknown-learner-state.json
```

The Join produces no textbook prose. Its output is the precise pedagogical problem the later Core1A Assimilation Compiler must solve.

## Commands

```bash
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/build_ground_truth_manifest.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/init_math_learning_run.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/route_math_learning_run.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/run_dual_intelligence.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/build_assimilation_demand.py' ...
```

The dual-intelligence runtime intentionally exposes `first-order`, `context`, `seal-package`, `second-order`, `validation-order` and `cross-validate` boundaries so the information firewall is auditable.

## Golden fixtures

Routing goldens prove Core1-first, Core2-first and conflict-blocking evidence situations. Dual-intelligence goldens prove symmetric firewall behavior for both execution orders. The AssimilationDemand golden proves that semantic + assessment intelligence can compile into a grounded teaching obligation while unknown learner state remains unknown rather than being interpreted as weakness.

Goldens demonstrate process behavior, not reusable topic content.

## Next increment

Increment 5 is the **Core1A Assimilation Compiler**:

```text
AssimilationDemand
      ↓
CognitiveTransformation
      ↓
LearningAtom + InferenceChain + EquationAssimilation
      ↓
RepresentationRequirement → candidates → decision
      ↓
MisconceptionContrast + SymbolBridge + FadingPlan + TransferBridge
      ↓
AssimilationPlan
```

Manuscript writing remains downstream and may not begin until the assimilation plan passes its validators.
