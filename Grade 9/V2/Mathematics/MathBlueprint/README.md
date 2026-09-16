# Mathematics V2 — Adaptive Math Blueprint

`MathBlueprint/` is the canonical Mathematics orchestration authority above Core1/Core2/Core1A/Core1B/Core2A/Core2B and downstream publication/evidence layers.

The canonical six-core architecture specification, governance invariants, and pipeline lifecycle are governed by [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md).

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.

PLANNED PEDAGOGY
!= COMPILED STATIC PRODUCT
!= RENDERED ARTIFACT
!= LEARNER ATTEMPT
!= LEARNER PERFORMANCE EVIDENCE
```

## Canonical topology

```text
Original evidence
      ↓
GroundTruthManifest
      ↓
Adaptive Evidence Router
      ↓
independent Core1 / Core2 reconstruction
      ↓
claim-level cross-validation
      ↓
Join / AssimilationDemand
      ↓
Core1A Assimilation Compiler
      ↓
AssimilationPlan
      ↓
Core1A declarative self-teaching
Core1B open-ended self-tutoring

Core2 legal assessment intelligence
      ↓
Core2A declarative solution apprenticeship
Core2B open-ended transfer tutoring
      ↓
technical depth obligations + reconstructable TTUs
      ↓
validated LearnerPageBlueprint
      ↓
future deterministic Publication
      ↓
optional external learner-evidence ingestion
```

## Intelligence boundaries

```text
Core1  = semantic / prerequisite / concept / representation authority
Core2  = assessment / hidden-structure / first-move intelligence

Core1A = BUILD understanding                    (DECLARATIVE)
Core1B = RECONSTRUCT + CONSOLIDATE             (OPEN_ENDED)
Core2A = LEARN expert solution anatomy         (DECLARATIVE)
Core2B = SELECT + TRANSFER + DISCRIMINATE      (OPEN_ENDED)
```

A-layers remain validity/teaching layers. B-layers remain static learner-facing products: no live response ingestion, state mutation, adaptive branching or mastery claims.

## Increment 1 — Ground truth

Only original evidence and authoritative sources may become ground truth. Evidence states remain explicit:

```text
PRESENT | ABSENT | PARTIAL | UNRESOLVED | CONFLICTED
```

Absence stays absence.

## Increment 2 — Adaptive routing

Subtopics may route Core1-first or Core2-first depending on evidence. Owner overrides change execution, never historical evidence or authority.

## Increment 3 — Dual intelligence firewall

Core1 and Core2 independently reconstruct their own intelligence from original inputs. The second specialist does not see the first package until its independent package is sealed. Cross-validation is claim-level and non-mutating.

## Increment 4 — Join / AssimilationDemand

Validated Core1/Core2 intelligence + learner state + learning purpose + owner constraints become typed assimilation obligations. `UNKNOWN / DEVELOPING / READY` remain the learner-capability states.

## Increment 5 — Core1A Assimilation Compiler

```text
AssimilationDemand
→ CognitiveTransformation
→ LearningAtom DAG
→ InferenceChain / EquationAssimilation
→ RepresentationRequirement + candidate decision
→ MisconceptionContrast / SymbolBridge
→ FadingPlan / TransferBridge
→ obligation coverage
→ AssimilationPlan
```

`AssimilationPlan` is a reasoning contract, not learner prose.

## Increment 6 — Static B-layer integration

Core1B compiles only already-governed mathematics into consolidation/self-tutoring structures.

Core2B compiles only Core2A-legal transfer items at or below an upstream ceiling.

Neither B-layer may add mathematical authority or infer new learner state from workbook use.

## Increment 7 — Self-teaching pedagogy

Canonical file: `SELF_TEACHING.md`.

```text
A = explanation-first / declarative self-teaching
B = elicitation-first / open-ended self-tutoring
```

All stages close the self-help loop with explanatory answers/checks, purposeful visuals and verified mathematics.

## Increment 8 — Depth + learner-calibration governance

Canonical file: `GENERATION_CALIBRATION.md`.

This increment separates **topic depth** from **learner calibration**.

### Core1A / Core1B

Always generated subtopic-wise as buckets.

```text
bucket difficulty = EASY | MEDIUM | HARD
```

The badge controls content depth, web research, decomposition, visual density and page ceiling. It is independent of learner knowledge percentage.

| Badge | Page ceiling per stage/bucket | Pedagogy web research | Internal decomposition |
|---|---:|---|---|
| EASY | 10 | optional (default absent) | subtopic only |
| MEDIUM | 20 | required + research brief | sub-subtopics allowed |
| HARD | 30 | required + deep research brief | sub-subtopics allowed |

Page counts are ceilings, not targets. Research source count is not used as a proxy for quality. External research improves pedagogy/representation and never becomes curriculum authority.

### Core2A / Core2B

Generation requires learner knowledge percentage unless explicitly waived by the owner.

```text
knowledge % known
→ source ref + calibration policy ref
→ Core2A support profile
→ Core2A maximum generated-question demand
→ Core2B maximum transfer demand

knowledge % unknown
→ owner waiver + reason
→ owner-selected Core2A support profile
→ owner-selected Core2A maximum demand
→ owner-selected Core2B maximum demand
```

Missing both percentage and waiver blocks generation. Supplying both also blocks. No pseudo-percentage or silent default is permitted.

Learning purpose (`STARTER / PRACTICE / REVISION / COMPETITION`) remains mandatory and independent of knowledge percentage.

The percentage is a generation-calibration input; it does not overwrite `UNKNOWN / DEVELOPING / READY` and does not itself prove mastery.

No numeric percentage bands are hard-coded without an owner-approved calibration policy. A named policy resolves percentage to concrete controls.

## Increment 9 — Technical depth + reconstructable TTU composition

Canonical file: `TECHNICAL_COMPOSITION.md`.

This increment makes technical density, reconstruction and layout semantics upstream contracts rather than renderer preferences.

```text
DIFFICULTY BADGE / STAGE ROLE
        ↓
TECHNICAL DEPTH OBLIGATIONS
        ↓
MATHEMATICAL BLOCKS + RECONSTRUCTABLE TTUs
        ↓
LearnerPageBlueprint
        ↓
COMPOSITION VALIDATION
        ↓
Publication
```

A reconstructable TTU is a bounded technical object with a learner-facing incomplete state, a specific reconstruction target and a checked completed state. Supported kinds include incomplete diagrams, component models, incomplete graphs, equation skeletons, event lines, table skeletons, proof/reasoning chains, coordinate models, flow models and construction sequences.

TTUs fade as:

```text
MODELLED → GUIDED → FADED → INDEPENDENT
```

Their lineage is stage-specific:

```text
Core1A TTU → Core1B reconstruction / contrast
Core2A TTU → Core2B reconstruction / transfer
```

Key invariants:

- page count is an output, never a depth target;
- prose-only learner pages fail;
- manual spacer padding fails;
- Core1A/Core1B MEDIUM/HARD depth is proven through typed mathematical obligations, not extra paragraphs;
- Core1A/Core1B/Core2A/Core2B must contain reconstructable TTUs;
- every Core1B `OPEN_TUTOR` page and every Core2B `TRANSFER_TUTOR` page requires a TTU;
- TTUs must contain real missing parts and a completion key that covers exactly those missing parts;
- the renderer cannot choose the missing parts or complete the TTU;
- repeated narrative/explanatory content across cores fails unless the repeated object is an immutable source, canonical formula/definition or answer identity;
- downstream reuse declares lineage and a cognitive transformation (`BUILD / RECONSTRUCT / CONTRAST / SOLUTION_ANATOMY / TRANSFER / VERIFY`);
- every learner-facing diagram/graph/TTU has semantic geometry, a bounded viewport and `clip_to_viewport = true`;
- an infinite mathematical locus is clipped to its graph box and may not draw across the learner page;
- open-ended B pages require explicit technical workspace plus answer derivation and verification.

Executable files:

```text
contracts/math-learner-page-blueprint.schema.json
policies/math-technical-composition-policy.json
engine/validate_learner_page_blueprint.py
tests/test_technical_composition.py
golden/technical_composition/02-medium-equidistant-reconstructable-ttu.json
```

## Executable self-teaching/calibration contracts

```text
contracts/math-self-teaching-contract.schema.json
contracts/math-self-teaching-generation-spec.schema.json
policies/math-self-teaching-policy.json
engine/validate_self_teaching_contract.py
engine/validate_self_teaching_generation_spec.py
tests/test_self_teaching_contract.py
tests/test_self_teaching_generation_spec.py
golden/self_teaching/01-depth-and-knowledge-calibration.json
```

## Technical Engineering Gate Registry (Grades 9–11)

The Mathematics Technical Engineering Gate Registry establishes deterministic, non-negotiable technical preconditions upstream of authored TTUs (CCU / CDAU boundary).

```text
MATHEMATICS_TECHNICAL_ENGINEERING_GATES.md
contracts/mathematics-technical-engineering-gate.schema.json
policies/mathematics-technical-engineering-gates.v1.json
engine/build_mathematics_engineering_gate_registry.py
engine/validate_mathematics_engineering_gates.py
tests/test_mathematics_engineering_gates.py
```

- **10 Coherent Gates:**
  1. `MATH-NUM-RADICALS`: Real numbers, principal square root non-negativity ($\sqrt{x^2} = |x|$), conjugate rationalization.
  2. `MATH-ALG-POLYNOMIALS`: Polynomial degrees, Factor Theorem, identities, Freshman's dream trap.
  3. `MATH-LIN-EQUATIONS`: Linear systems in two variables, consistency ratios ($a_1/a_2$ vs $b_1/b_2$ vs $c_1/c_2$).
  4. `MATH-QUAD-EQUATIONS`: Non-zero leading coefficient ($a \neq 0$), discriminant trichotomy, Vieta relations.
  5. `MATH-GEO-COORDINATES`: Cartesian metric, section formula, vertical line undefined slope.
  6. `MATH-GEO-TRIANGLES`: Congruence criteria (SSA forbidden), Thales theorem, similarity criteria.
  7. `MATH-TRIG-RATIOS`: Right-triangle ratios, fundamental Pythagorean identities, acute domain.
  8. `MATH-GEO-CIRCLES`: Tangent-radius perpendicularity, external equal tangents, cyclic quadrilateral supplementary angles.
  9. `MATH-MENS-SURFACES`: Surface area internal boundary exclusion, melting volume conservation.
  10. `MATH-STAT-PROBABILITY`: Probability bounds ($0 \le P(E) \le 1$), complementary events, empirical central tendency.

- **Validation & Falsifier Battery:**
  ```bash
  python "Grade 9/V2/Mathematics/MathBlueprint/engine/validate_mathematics_engineering_gates.py"
  python -m unittest "Grade 9/V2/Mathematics/MathBlueprint/tests/test_mathematics_engineering_gates.py"
  ```

## Phase-1 Observability, Usability, Discovery Quality & Architecture Governance

The MathBlueprint repository includes a complete developer-facing and academician observability workbench:

1. **MathBlueprint Run Builder** (`tools/run_builder/`):
   - Standalone browser workbench (`index.html`, `run_builder.js`, `run_builder.css`) and CLI compiler (`compile_run.py`).
   - Compiles human run settings into reproducible prompt manifests and execution manifests with live schema validation, dependency visibility, presets for IIT-JEE, IOQM/Olympiad, and CBSE, and config export.
   - CLI fixture validation mode: `python compile_run.py --validate-fixtures`.
   - Test suite: `tools/run_builder/tests/test_run_builder.py` (15/15 tests PASS).

2. **Blueprint Architecture Explorer** (`tools/architecture_explorer/`):
   - Derived observability engine (`generate_architecture_manifest.py`) compiling 153 components and 402 relations into `architecture_observation_manifest.json`.
   - Standalone interactive explorer UI (`index.html`, `architecture_explorer.js`, `explorer.css`) featuring dependency search, layer filtering, orphaned-contract detection, and gap reporting with offline fallback.
   - CI integrity verification mode: `python generate_architecture_manifest.py --check`.
   - Test suite: `tools/architecture_explorer/tests/test_architecture_explorer.py` (10/10 tests PASS).

3. **Engineering Discovery Quality Benchmark** (`benchmarks/discovery/`):
   - Quantitative stress-test suite (`benchmark_runner.py`) running across 80 curated multi-category queries (`corpus/engineering_discovery_benchmark_corpus.v1.json`).
   - Measures candidate recall (100% Top-1 recall, 100% Top-3, 100% Top-5, 0% miss rate), noise rate, ambiguity preservation, determinism, and vocabulary contributions across 23 gates and 132 terms.
   - Generates `VOCABULARY_GAP_REPORT.md` and proves that candidate discovery ranking never bypasses exact Engineering Gate authorization.
   - Test suite: `benchmarks/discovery/tests/test_engineering_discovery_benchmark.py` (9/9 tests PASS).

4. **Core Architecture / Documentation Drift Audit** (`CORE_ARCHITECTURE_DRIFT_AUDIT.md`):
   - Exhaustive 17-section audit comparing all normative documents, schemas, and validators to maintain strict pedagogical, mathematical, and governance alignment.
   - Section 17 includes the Academician Pedagogical Alignment Matrix bridging cognitive depth, misconception diagnosis, and problem-solving pedagogy for Grades 9–11.

## Source-question integrity

```text
SOURCE QUESTION            = immutable
QUESTION INTERPRETATION    = derived
HINTS                      = derived
SOLUTION                   = independently verified
VISUAL                     = derived
GENERATED VARIANT          = new identity + new provenance
```

Difficulty adjustment never silently rewrites a frozen source question.

## Publication boundary

Do not freeze deterministic Publication until pedagogy goldens prove:

- EASY/MEDIUM/HARD Core1A/Core1B bucket behaviour;
- Core2A/Core2B generation with a real knowledge percentage;
- Core2A/Core2B generation with an owner waiver;
- Core2A question-demand calibration and Core2B transfer-demand calibration;
- self-help closure and independent answer validation;
- reconstructable TTU coverage and lineage through Core1A→Core1B and Core2A→Core2B;
- validated technical depth and non-duplicative six-core page composition;
- bounded/clipped representation and TTU geometry with explicit workspace semantics;
- no drift in authority, source identity or transfer ceiling.

Publication then becomes a deterministic compiler of an already-validated `LearnerPageBlueprint`, not a content-authoring, omission-selecting or page-filling layer.
