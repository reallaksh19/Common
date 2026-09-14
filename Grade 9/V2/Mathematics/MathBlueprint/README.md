# Mathematics V2 — Adaptive Math Blueprint

`MathBlueprint/` is the canonical Mathematics orchestration authority above Core1/Core2/Core1A/Core1B/Core2A/Core2B and downstream publication/evidence layers.

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

| Badge | Page ceiling per bucket/product | Pedagogy web research | Internal decomposition |
|---|---:|---|---|
| EASY | 10 | forbidden | subtopic only |
| MEDIUM | 20 | required | sub-subtopics allowed |
| HARD | 30 | required, deeper | sub-subtopics allowed |

Page counts are ceilings, not targets. Research improves pedagogy/representation and never becomes curriculum authority.

### Core2A / Core2B

Generation requires learner knowledge percentage unless explicitly waived by the owner.

```text
knowledge % known
→ source ref + calibration policy ref
→ Core2A support profile
→ Core2B maximum demand level

knowledge % unknown
→ owner waiver + reason
→ owner-selected Core2A support profile
→ owner-selected Core2B maximum demand level
```

Missing both percentage and waiver blocks generation. Supplying both also blocks. No pseudo-percentage or silent default is permitted.

Learning purpose (`STARTER / PRACTICE / REVISION / COMPETITION`) remains mandatory and independent of knowledge percentage.

The percentage is a generation-calibration input; it does not overwrite `UNKNOWN / DEVELOPING / READY` and does not itself prove mastery.

### Executable contracts

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
- self-help closure and independent answer validation;
- no drift in authority, source identity or transfer ceiling.

Publication then becomes a deterministic compiler of already-governed learner products, not a content-authoring layer.
