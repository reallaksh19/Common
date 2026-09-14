# Mathematics V2 — Generation Calibration

This file is the canonical generation-control boundary for Core1A/Core1B depth and Core2A/Core2B learner calibration.

## 1. Two independent control systems

```text
CORE1A / CORE1B
topic complexity → difficulty badge → depth / research / representation budget

CORE2A / CORE2B
learner knowledge % OR owner waiver → support profile / transfer ceiling
```

These must not be conflated.

## 2. Core1A/Core1B — difficulty-badge control

Every learner product is generated **subtopic-wise as a bucket**.

The same bucket badge binds Core1A and Core1B:

```text
EASY | MEDIUM | HARD
```

The badge is based on mathematical/pedagogical complexity or explicit owner designation, never learner knowledge percentage.

Useful qualitative badge evidence includes:

- prerequisite depth;
- abstraction and hidden-state burden;
- number of representation changes;
- inference-chain density;
- validity/exception density;
- misconception density;
- method branching;
- symbol-to-meaning compression.

No unexplained numeric complexity score is required.

### EASY

- up to 10 pages per bucket/product;
- visual, step-by-step and diagram-supported;
- no pedagogy-enrichment web search;
- remain at the subtopic level;
- source-integrity verification remains separate and may still be invoked if evidence is damaged or conflicted.

### MEDIUM

- up to 20 pages per bucket/product;
- mandatory web research before authoring;
- at least two credible research/source references in the research brief;
- subtopic → sub-subtopic decomposition allowed;
- high visual density and dedicated diagrams;
- explicit symbol bridges and misconception contrasts.

### HARD

- up to 30 pages per bucket/product;
- mandatory deeper web research before authoring;
- at least three credible research/source references, including at least one high-authority or peer-reviewed source where available;
- subtopic → sub-subtopic decomposition allowed;
- very high representation density;
- dedicated diagrams/graphs/tables;
- explicit inference bridges, validity boundaries and contrast cases.

Page budgets are ceilings, not quotas. Depth is measured by mathematical and cognitive coverage, not page count.

Web research may improve **how** the mathematics is represented and explained. It cannot decide **what mathematics is legal**.

## 3. Core2A/Core2B — learner-calibration control

Generation is blocked until there is one valid learner-calibration path.

### Path A — knowledge known

Required:

```text
learner_knowledge_percent = 0..100
knowledge_percent_source_ref
knowledge_calibration_policy_ref
resolved_core2a_support_profile
resolved_core2b_max_demand_level
```

The percentage is a generation-control input. It is not a new mastery label and does not replace `UNKNOWN / DEVELOPING / READY`.

### Path B — knowledge unknown

Owner waiver is allowed.

Required:

```text
owner_ref
waiver reason
owner-selected Core2A support profile
owner-selected Core2B maximum demand level
```

The system must not invent a percentage to fill the gap.

### Core2A uses calibration for

- question selection within legal scope;
- support density;
- worked-step granularity;
- representation support;
- ordering;
- generated near/structural variants with new provenance.

### Core2B uses calibration for

- maximum transfer demand;
- cue visibility;
- hint latency;
- representation shift;
- inverse target;
- hidden structure;
- method/family discrimination;
- synthesis demand.

Core2B still selects only from Core2A-legal items and generated items that satisfy the same legality/provenance controls.

## 4. Purpose remains separate

`STARTER / PRACTICE / REVISION / COMPETITION` is still mandatory for Core2A/Core2B.

```text
KNOWLEDGE % answers: how much support / transfer distance?
PURPOSE answers: what job should this product perform?
```

Neither may silently infer the other.

## 5. Fail-closed states

```text
Core1 bucket without difficulty badge                    → BLOCK
EASY bucket with pedagogy-enrichment web research        → BLOCK
MEDIUM/HARD bucket without required research evidence    → BLOCK
bucket page budget above badge ceiling                   → BLOCK
Core1 depth changed because of learner knowledge %       → BLOCK

Core2 without knowledge % and without owner waiver       → BLOCK
Core2 with both knowledge % and owner waiver             → BLOCK
knowledge % without source + calibration-policy ref      → BLOCK
owner waiver without explicit support + transfer ceiling → BLOCK
silent/default knowledge %                               → BLOCK
silent/default purpose                                   → BLOCK
```

## 6. Execution contract

`math-self-teaching-generation-spec.schema.json` captures the per-run inputs.

`validate_self_teaching_generation_spec.py` applies the semantic gates above.

The canonical policy remains `math-self-teaching-policy.json`.
