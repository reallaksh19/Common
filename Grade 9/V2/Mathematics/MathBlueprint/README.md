# Mathematics V2 — Adaptive Math Blueprint

`MathBlueprint/` is the canonical Mathematics orchestration authority above Core1/Core2/Core1A/Core2A and downstream production/publication layers.

The governing invariant is:

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.
```

Core1 and Core2 reconstruct different intelligence from the same original evidence. Either may execute first when evidence justifies it. Neither becomes ground truth because it executed first.

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
first specialist — GROUND_TRUTH_ONLY
      ↓
first package sealed
      ↓
second fresh specialist — GROUND_TRUTH_ONLY
(first package explicitly withheld)
      ↓
independent package sealed
      ↓
claim-level cross-validation
      ↓
CROSS_VALIDATED
      ↓
Join / AssimilationDemand
      ↓
JOIN_READY | BLOCKED_CONFLICT
      ↓
Core1A Assimilation Compiler
      ↓
ASSIMILATION_COMPILED
```

Increment 1 established immutable evidence binding and root run state. Increment 2 added evidence-adaptive routing. Increment 3 implemented the Core1/Core2 independence firewall and claim-level validation. Increment 4 compiled validated intelligence plus learner state/purpose into `AssimilationDemand`. Increment 5 now compiles that demand into a validated `AssimilationPlan` before manuscript realization.

## Increment 1 — Ground truth + run blueprint

`GroundTruthManifest` records original question corpus, syllabus, authoritative source/textbook, answer key, solution set and figure set. Evidence availability is explicit:

```text
PRESENT | ABSENT | PARTIAL | UNRESOLVED | CONFLICTED
```

`ABSENT` remains absence. It cannot silently become low importance, low difficulty, out-of-scope status or learner weakness.

Only `ORIGINAL_EVIDENCE` and `AUTHORITATIVE_SOURCE` may become ground truth. Derived claims, benchmarks, agent conclusions and owner overrides remain outside ground truth.

Every downstream artifact belongs to one `MathLearningRunBlueprint`. `run_id` remains stable while `run_digest` evolves. The relay transport limit is 1–3 subtopics per handoff bundle; this is not a limit on learning atoms, equations, inference edges or teaching steps.

## Increment 2 — Adaptive Relay / EvidenceRouter

Routing profiles each subtopic with:

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
material conflict                         → BLOCK_CONFLICT
both evidence channels weak               → BLOCK_EVIDENCE
strong semantic authority                 → CORE1_FIRST
otherwise rich + resolved question corpus → CORE2_FIRST
otherwise                                 → BLOCK_OWNER_REVIEW
```

Owner routing control stores `SYSTEM ACTION`, `OWNER OVERRIDE` and `FINAL ACTION` separately. Owner control changes execution only; it never rewrites source authority.

## Increment 3 — Dual intelligence + independence firewall

Core1 uses a semantic vocabulary such as `CONCEPT`, `MODEL`, `LAW`, `EQUATION`, `DERIVATION`, `PREREQUISITE`, `INVARIANT`, `VALIDITY` and `CONCEPT_BOUNDARY`.

Core2 uses an assessment-cognition vocabulary such as `QUESTION_DEMAND`, `RECOGNITION_CUE`, `HIDDEN_CONSTRAINT`, `FIRST_NON_OBVIOUS_MOVE`, `REASONING_CHAIN`, `PROBLEM_FAMILY`, `MISCONCEPTION`, `SOLUTION_STRUCTURE` and `TRANSFER_ENVELOPE`.

The runtime proves independence structurally:

```text
FIRST_ROLE_ANALYSIS
  context = GROUND_TRUTH_ONLY

SECOND_ROLE_INDEPENDENT
  context = GROUND_TRUTH_ONLY
  first package = WITHHELD
  second specialist = different agent instance

SECOND_ROLE_VALIDATION
  unlocked only after independent package is sealed
  context = GROUND_TRUTH_PLUS_UPSTREAM_VALIDATION
```

Every first-package claim receives exactly one of:

```text
CONFIRMED | REFINED | UNSUPPORTED | CONTRADICTED | OUT_OF_SCOPE | UNKNOWN
```

`MISSING` is separate and must point to an independently sealed second-role claim. Cross-validation never mutates either specialist package.

## Increment 4 — Join / AssimilationDemand

Join may run only after `CROSS_VALIDATED`:

```text
validated Core1 semantic intelligence
+
validated / independently grounded Core2 assessment intelligence
+
LearnerCapabilityState
+
learning purpose
+
owner constraints
        ↓
AssimilationDemand
```

Learner prior percentage remains provenance only. Capability readiness is limited to:

```text
UNKNOWN | DEVELOPING | READY
```

Capability basis is explicit:

```text
LEARNER_EVIDENCE | OWNER_DECLARED_BASELINE | UNKNOWN
```

An omitted capability becomes `UNKNOWN`, never weak. Gap mapping is:

```text
READY      → NO_IDENTIFIED_GAP
DEVELOPING → BRIDGE_OR_PRACTICE_REQUIRED
UNKNOWN    → UNKNOWN_REQUIRES_PROBE_OR_FULL_SUPPORT
```

Purpose remains independent of learner state. `FIRST_STUDY`, `CONSOLIDATION`, `REVISION` and `COMPETITIVE_EXAM` compile different requirements. Competition adds recognition/transfer demand but explicitly may not skip necessary foundations.

Join preserves disagreement and uncertainty. `CONFIRMED`, `REFINED` and grounded `MISSING` findings are admissible; `UNKNOWN`, `UNSUPPORTED`, `CONTRADICTED` and `OUT_OF_SCOPE` remain visible but cannot ground teaching obligations.

Assimilation obligations are typed as:

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

Each obligation carries claim provenance, original-evidence provenance, capability refs, learner-gap state and whether it must be satisfied before Core2A.

## Increment 5 — Core1A Assimilation Compiler

The compiler consumes only a `JOIN_READY` `AssimilationDemand` and produces a machine-validated `AssimilationPlan`:

```text
AssimilationDemand
      ↓
CognitiveTransformation
      ↓
LearningAtom + prerequisite DAG
      ↓
InferenceChain + EquationAssimilation
      ↓
RepresentationRequirement
      ↓
2+ RepresentationCandidates
      ↓
admissibility + explicit RepresentationDecision
      ↓
MisconceptionContrast + SymbolBridge
      ↓
FadingPlan + TransferBridge
      ↓
obligation coverage audit
      ↓
AssimilationPlan
      ↓
ASSIMILATION_COMPILED
```

### Compiler invariants

The compiler fails closed when any of the following occurs:

- a component cites an unknown Join obligation;
- an atom prerequisite points to an unknown atom or creates a cycle;
- an `INFERENCE_BRIDGE` obligation lacks an explicit inference chain;
- an `EQUATION_ASSIMILATION` obligation lacks meaning or a symbol bridge;
- a representation requirement has fewer than two candidates;
- a selected representation is inadmissible or candidate rejection is incomplete;
- a misconception obligation lacks an explicit contrast;
- a learner capability is `DEVELOPING`/`UNKNOWN` but no staged support-fading plan is supplied;
- a transfer bridge is not grounded in `TRANSFER` or `ASSESSMENT_RECOGNITION` demand authority;
- `COMPETITIVE_EXAM` has no transfer bridge;
- a hard owner constraint is not satisfied;
- any Join obligation lacks its type-specific compiler components.

The support-fading order is fixed:

```text
MODELLED → GUIDED → FADED → INDEPENDENT
```

Representation is a governed pedagogical decision, not decoration. Each representation requirement must expose at least two candidates, record affordances/limitations, mark admissibility and choose one candidate with an explicit rationale.

Equation assimilation may not present a naked formula. It binds equation text to meaning, symbol bridges and validity conditions.

Every obligation appears exactly once in `obligation_coverage`. This makes `required_before_core2a` foundations structurally impossible to drop at the compiler boundary.

`AssimilationPlan` is a reasoning contract, not textbook prose. The compiler does not write the learner manuscript or PDF.

### Increment 5 files

```text
contracts/math-assimilation-plan-build-spec.schema.json
contracts/math-assimilation-plan.schema.json
policies/math-assimilation-compiler-policy.json
engine/compile_assimilation_plan.py
tests/test_assimilation_compiler.py
golden/assimilation_compiler/01-vieta-assimilation-plan.json
```

## Commands

```bash
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/build_ground_truth_manifest.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/init_math_learning_run.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/route_math_learning_run.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/run_dual_intelligence.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/build_assimilation_demand.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/compile_assimilation_plan.py' \
  --run /path/to/run.json \
  --demand /path/to/assimilation_demand.json \
  --spec /path/to/assimilation_plan_build_spec.json \
  --out-plan /path/to/assimilation_plan.json \
  --out-run /path/to/updated_run.json
```

## Goldens

Routing goldens prove Core1-first, Core2-first and evidence-blocking cases. Dual-intelligence goldens prove symmetric firewall behavior. The Join golden proves that learner uncertainty remains uncertainty. The Assimilation Compiler golden proves that Vieta obligations become traceable learning atoms, inference/equation structures, a governed representation decision, misconception contrast, fading and transfer without generating manuscript prose.

Goldens demonstrate process behavior, not reusable topic content.

## Next increment

Increment 6 is the **instructional exposure / evidence receipt** boundary:

```text
AssimilationPlan
      ↓
Core1A learner realization
      ↓
InstructionalExposureReceipt
      ↓
what was actually taught / represented / practised
      ↓
Core2A taught-scope eligibility
```

The receipt must distinguish planned instruction from instruction actually realized and make Core2A eligibility depend on evidenced exposure rather than assumed coverage. Deterministic publication remains downstream.
