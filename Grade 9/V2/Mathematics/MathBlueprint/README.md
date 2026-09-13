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
```

Increment 1 established immutable evidence binding and the root run state. Increment 2 added evidence-adaptive routing, owner routing overrides and deterministic max-three handoff bundling. Increment 3 now implements the dual-intelligence independence firewall and claim-level cross-validation.

## Ground truth

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

## Root run blueprint

Every downstream artifact belongs to one `MathLearningRunBlueprint`. The run identity is assigned once and remains stable across state transitions; `run_digest` changes as state evolves.

The root binds exact ground-truth ref/digest, learner prior, learning purpose, product mode, owner override refs, routing, handoff bundles and later Core1/Core2/Join/Assimilation/Core1A/Core2A/publication refs.

The handoff transport constraint is:

```text
1 <= subtopics per bundle <= 3
```

This does not limit learning atoms, equations, inference edges, representations or teaching steps.

## Increment 2 — Adaptive Relay / EvidenceRouter

Routing profiles every candidate subtopic with six governed evidence dimensions:

```text
SA  scope authority
SS  semantic source strength
QE  question evidence
QR  question resolution
UA  uncertainty
CI  conflict index
```

All dimensions use the 0–4 rubric in `policies/math-evidence-routing-policy.json`; positive evidential strength must cite GroundTruth evidence.

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

If both roles are evidence-admissible, normal routing starts Core1 because semantic scope is already strongly established. Core2 must still independently re-ground. Missing/coarse semantic authority with rich resolved questions routes Core2 first.

## Owner override semantics

Routing stores separately:

```text
SYSTEM ACTION
OWNER OVERRIDE
FINAL ACTION
```

`HARD` may change the operational first role while preserving the system finding. `SOFT` may select only an already evidence-admissible role. Owner overrides never mutate GroundTruth.

## Increment 3 — Dual intelligence + independence firewall

Core1 and Core2 have separate claim vocabularies.

Core1 reconstructs semantic structure, including:

```text
CONCEPT / MODEL / LAW / EQUATION / DERIVATION
PREREQUISITE / CONSTRAINT / INVARIANT / STATE
VALIDITY / CONCEPT_BOUNDARY
REPRESENTATION_AFFORDANCE / STRUCTURAL_CONTRAST
```

Core2 reconstructs assessment cognition, including:

```text
QUESTION_DEMAND / RECOGNITION_CUE / HIDDEN_CONSTRAINT
REQUIRED_CAPABILITY / FIRST_NON_OBVIOUS_MOVE
REPRESENTATION_SWITCH / REASONING_CHAIN / WRONG_CHAIN
DIFFICULTY_VECTOR / PROBLEM_FAMILY / MISCONCEPTION
SOLUTION_STRUCTURE / TRANSFER_ENVELOPE
```

The runtime enforces three phases:

```text
FIRST_ROLE_ANALYSIS
  context = GROUND_TRUTH_ONLY

SECOND_ROLE_INDEPENDENT
  context = GROUND_TRUTH_ONLY
  first package = WITHHELD
  second specialist must use a different agent instance

SECOND_ROLE_VALIDATION
  allowed only after the independent package is sealed
  context = GROUND_TRUTH_PLUS_UPSTREAM_VALIDATION
  first + independent packages become visible
```

A fresh instance ID by itself is not proof of independence. The sealed work order, context manifest and independent package prove that the second specialist completed its ground-truth-only pass before upstream claims were exposed.

Every first-package claim must receive exactly one classification:

```text
CONFIRMED
REFINED
UNSUPPORTED
CONTRADICTED
OUT_OF_SCOPE
UNKNOWN
```

`MISSING` is recorded separately when the independent second-role pass finds a grounded claim absent from the first package. A missing record must point to an actual sealed independent claim.

Cross-validation does not mutate either specialist package. It creates a separate `math-cross-validation` artifact with original-evidence provenance.

## Increment 3 executable contracts

```text
contracts/math-specialist-work-order.schema.json
contracts/math-agent-context-manifest.schema.json
contracts/math-specialist-package.schema.json
contracts/math-cross-validation.schema.json
contracts/math-dual-intelligence-session.schema.json

policies/math-dual-intelligence-policy.json
engine/run_dual_intelligence.py

golden/dual_intelligence/01-core1-first-firewall.json
golden/dual_intelligence/02-core2-first-firewall.json

tests/test_dual_intelligence.py
```

The runtime is deliberately symmetric: `CORE1_FIRST` and `CORE2_FIRST` use the same firewall semantics; only specialist role order changes.

## Commands

Ground-truth and routing commands remain:

```bash
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/build_ground_truth_manifest.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/init_math_learning_run.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/route_math_learning_run.py' ...
```

The dual-intelligence runtime exposes explicit commands rather than one opaque call:

```text
first-order
context
seal-package
second-order
context
seal-package
validation-order
context
cross-validate
```

This makes the information firewall auditable at every boundary.

## Golden fixtures

Routing goldens prove:

1. strong syllabus/source + rich questions → `CORE1_FIRST`;
2. absent/coarse syllabus + rich resolved questions → `CORE2_FIRST`;
3. sparse/conflicted evidence → block rather than forced consensus.

Dual-intelligence goldens prove both Core1-first and Core2-first paths preserve the same independence firewall.

Goldens demonstrate process behavior, not reusable topic content.

## Next increment

Increment 4 builds the **Join / AssimilationDemand** layer after cross-validation:

```text
validated Core1 semantic intelligence
        +
validated Core2 assessment intelligence
        +
learner capability state
        +
learning purpose
        +
owner constraints
        ↓
AssimilationDemand
```

The Join must preserve disagreement and unknowns, record provenance for each assimilation obligation, and produce the precise pedagogical requirements that the later Core1A Assimilation Compiler must solve. Manuscript writing remains downstream and is not allowed to substitute for this reasoning layer.
