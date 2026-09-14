# Mathematics V2 — Adaptive Math Blueprint

`MathBlueprint/` is the canonical Mathematics orchestration authority above Core1/Core2/Core1A/Core1B/Core2A/Core2B and downstream publication/evidence layers.

The governing invariant is:

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.
```

Core1 and Core2 reconstruct different intelligence from the same original evidence. Either may execute first when evidence justifies it. Neither becomes ground truth because it executed first.

A second product-layer invariant now applies:

```text
A-LAYERS GOVERN WHAT IS VALID.
B-LAYERS COMPILE STATIC LEARNER-FACING PRODUCTS.
```

Core1B and Core2B are build-time compilers. They do not ingest learner responses, mutate learner state, schedule retrieval, perform live repair, or run adaptive tutoring loops.

## Implemented topology

```text
Original evidence
      ↓
GroundTruthManifest
      ↓
MathLearningRunBlueprint
      ↓
Adaptive Evidence Router
      ↓
CORE1_FIRST | CORE2_FIRST | BLOCK
      ↓
independent Core1/Core2 passes + claim-level cross-validation
      ↓
CROSS_VALIDATED
      ↓
Join / AssimilationDemand
      ↓
JOIN_READY | BLOCKED_CONFLICT
      ↓
Core1A Assimilation Compiler
      ↓
AssimilationPlan
      ↓
ASSIMILATION_COMPILED
      ↓
Core1A governed teaching output
      ├─────────────────────────────┐
      ↓                             │
Core1B static consolidation         │
compiler                            │
      ↓                             │
fixed consolidation workbook       │
                                    │
Core2A legal practice/challenge pool│
      + purpose                     │
      + upstream compile ceiling    │
      ↓                             │
Core2B static transfer compiler     │
      ↓                             │
fixed transfer workbook             │
                                    ↓
                         deterministic Publication
                                    ↓
                       optional external learner evidence
```

Increment 1 established immutable evidence binding and root run state. Increment 2 added evidence-adaptive routing. Increment 3 implemented the Core1/Core2 independence firewall and claim-level validation. Increment 4 compiled validated intelligence plus learner state/purpose into `AssimilationDemand`. Increment 5 compiled that demand into a validated `AssimilationPlan`. Increment 6 now integrates the revised static Core1B/Core2B product boundary from PR #369.

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

An omitted capability becomes `UNKNOWN`, never weak. Purpose remains independent of learner state. `FIRST_STUDY`, `CONSOLIDATION`, `REVISION` and `COMPETITIVE_EXAM` compile different requirements.

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

The compiler fails closed on missing obligation coverage, invalid prerequisite graphs, naked equation teaching, unjustified representation choice, unsupported transfer, missing misconception contrasts, and missing support fading for `DEVELOPING`/`UNKNOWN` learner gaps.

Support fading is fixed:

```text
MODELLED → GUIDED → FADED → INDEPENDENT
```

`AssimilationPlan` is a reasoning contract, not learner prose or a PDF.

## Increment 6 — Static Core1B/Core2B compiler integration

PR #369 was revised so the B layers are no longer evidence/adaptive runtimes. The MathBlueprint now adopts that boundary.

### Core1B

Core1B is a static consolidation compiler downstream of Core1A. It may compose only already-governed mathematics and approved capability refs into paper-native structures such as:

```text
METHOD_COMPARISON
ERROR_CONTRAST
CONTROLLED_VARIATION
COMPLETION
FADED
CLOSE_INDEPENDENT
ANSWER_CHECK
```

It may use already-authorized learner treatment to choose composition at build time, but the resulting workbook is fixed after compilation.

Core1B does **not** own:

```text
learner attempts
learner-performance evidence
state transitions
live hints
repair routing
adaptive branches
post-publication diagnosis
```

It cannot add new mathematics.

### Core2B

Core2B is a static transfer-workbook compiler downstream of Core2A. It may select only Core2A-legal items and only at or below an upstream-supplied compile-time ceiling:

```text
M0_DIRECT
M1_CONTROLLED_VARIATION
M2_REPRESENTATION_TRANSFER
M3_INVERSE_TARGET
M4_HIDDEN_STRUCTURE
M5_METHOD_DISCRIMINATION
M6_FAMILY_DISCRIMINATION
M7_MULTI_STEP_SYNTHESIS
M8_MIXED_COMPETITIVE
```

The ceiling is an input. Core2B does not infer a new learner state from workbook use.

Core2B does **not** require Core1B to run first. The two B compilers are parallel product lanes with different upstream authorities:

```text
Core1A authority + learner treatment
        ↓
      Core1B

Core2A legal pool + purpose + compile ceiling
        ↓
      Core2B
```

### Static compiler integration contract

`math-b-layer-integration.schema.json` and `validate_b_layer_integration.py` now enforce:

```text
A-layers govern validity
B-layers are STATIC compilers
compiled product != learner evidence
Core1B cannot add mathematics
Core2B requires a bound Core2A legal pool
Core2B ceiling must be supplied upstream
Core2B does not require a Core1B product
B-layers do not ingest learner responses
B-layers do not emit learner-state transitions
B-layers may not rewrite upstream learner state
```

The earlier proposed Increment 6 model — where Core1B would verify learner exposure and Core2B would adapt live practice — is superseded. Those are not B-layer responsibilities in the revised architecture.

## Publication and learner evidence boundary

The remaining distinction is now:

```text
PLANNED PEDAGOGY
      !=
COMPILED STATIC PRODUCT
      !=
RENDERED ARTIFACT
      !=
LEARNER ATTEMPT
      !=
LEARNER PERFORMANCE EVIDENCE
```

Deterministic Publication must verify that compiled semantic blocks actually appear correctly in the final artifact. If learner responses are later collected, they enter through a separate evidence-ingestion boundary and may update future learner state only through the governed learner-intelligence pipeline. Static B products themselves cannot make claims that the learner attempted, learned, retained or became transfer-ready.

## Commands

```bash
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/build_ground_truth_manifest.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/init_math_learning_run.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/route_math_learning_run.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/run_dual_intelligence.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/build_assimilation_demand.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/compile_assimilation_plan.py' ...
python 'Grade 9/V2/Mathematics/MathBlueprint/engine/validate_b_layer_integration.py' ...
```

## Goldens

Routing goldens prove Core1-first, Core2-first and evidence-blocking cases. Dual-intelligence goldens prove symmetric firewall behavior. The Join golden proves that learner uncertainty remains uncertainty. The Assimilation Compiler golden proves that obligations become traceable pedagogy without generating manuscript prose. PR #369 contributes two structurally different static compiler families — coordinate geometry and linear-system modelling — to prove that Core1B/Core2B are reusable compilers rather than hidden topic-specific engines.

## Next increment

The next architecture increment is **deterministic Publication integration**:

```text
Core1A / Core1B / Core2A / Core2B compiled products
        ↓
PublicationBlueprint
        ↓
deterministic renderer
        ↓
rendered-artifact semantic/surface audit
        ↓
final PDFs
```

A separate optional learner-evidence ingestion layer comes only after product delivery and must remain outside static Core1B/Core2B.
