# Mathematics V2 — Generation Calibration

This file is the canonical generation-control boundary for Core1A/Core1B depth and Core2A/Core2B learner calibration.

## 1. Two independent control systems

```text
CORE1A / CORE1B
topic complexity → difficulty badge → depth / research obligation / representation budget

CORE2A / CORE2B
learner knowledge % OR owner waiver
        ↓
Core2A support + Core2A question-demand ceiling + Core2B transfer ceiling
```

These systems must not be conflated.

## 2. Core1A/Core1B — difficulty-badge control

Every learner product is generated **subtopic-wise as a bucket**. Core1A and Core1B share the same bucket identity and difficulty badge:

```text
EASY | MEDIUM | HARD
```

The badge reflects mathematical/pedagogical complexity or an explicit owner designation. It never derives from learner knowledge percentage.

Useful badge evidence includes prerequisite depth, abstraction, representation changes, inference density, validity/exception density, misconception density, method branching and symbol-to-meaning compression. No unexplained numeric complexity score is required.

Difficulty controls the **minimum research obligation**, not permission to investigate. Discovery remains open at every difficulty; promotion/release remains strict.

### EASY

- up to 10 pages per stage per bucket;
- visual, step-by-step and diagram-supported;
- pedagogy-enrichment web research is optional, not prohibited;
- if optional research is used, both a governed research brief and bound research references are required;
- remain at the subtopic level;
- Source Integrity verification remains a separate safety path and may still be used when original evidence is ambiguous, damaged or conflicted.

### MEDIUM

- up to 20 pages per stage per bucket;
- mandatory targeted web research before authoring;
- a research brief and credible web references are required;
- subtopic → sub-subtopic decomposition allowed;
- high visual density and dedicated diagrams;
- explicit symbol bridges and misconception contrasts.

### HARD

- up to 30 pages per stage per bucket;
- mandatory **deep** web research before authoring;
- a deep research brief and credible web references are required;
- subtopic → sub-subtopic decomposition allowed;
- very high representation density;
- dedicated diagrams/graphs/tables;
- explicit inference bridges, validity boundaries and contrast cases.

Page budgets are ceilings, not quotas. Depth is measured by mathematical and cognitive coverage, not by filling pages.

Research-source counts are deliberately **not** used as a proxy for quality. The research brief must explain what was learned from the sources and how it improves pedagogy. Web research may improve **how** mathematics is represented and explained; it cannot decide **what mathematics is legal**.

The promotion rule is therefore:

```text
DISCOVERY / SEARCH: permitted at every difficulty
EASY promotion: research not required; if used, custody must be complete
MEDIUM promotion: targeted research required
HARD promotion: deep research required
```

### Claim-level evidence promotion

A source entering the research workspace is not automatically promoted into pedagogy. Promotion is governed at the **decision and claim** level:

```text
OPEN DISCOVERY / SEARCH
        ↓
RESEARCH DECISION
(subtopic + depth + coverage + retained sources)
        ↓
PEDAGOGY CLAIM
(one explicit proposition for one support category)
        ↓
EVIDENCE LINKS
SUPPORTS | CONTRADICTS
        ↓
CONFIDENCE
LOW | MODERATE | HIGH
        ↓
CONTRADICTION RESOLUTION
(when disagreement exists)
        ↓
PROMOTED GENERATION BINDING
```

The executable contract is `math-pedagogy-research-manifest.schema.json` plus `validate_pedagogy_research_manifest.py`.

Promotion requirements are subject-wide and topic-independent:

- every coverage category declared by a research decision has at least one explicit promoted claim;
- every source retained by that decision that is relevant to the claim category is explicitly classified as `SUPPORTS` or `CONTRADICTS` for that claim;
- every promoted claim has at least one supporting evidence link;
- contradictory retained evidence requires an explicit resolution explaining why the promoted decision remains bounded and defensible;
- a source may support multiple claims when it genuinely bears on multiple promoted decisions; there is no universal minimum source count;
- discovery-only sources do not need to enter the promoted generation binding;
- every evidence source actually used by a promoted claim must survive into the bucket's bound research references;
- `PRODUCTION` manifests require verified web captures and reject `LOW`-confidence promoted claims;
- `TEST_ONLY` manifests may exercise the custody path but cannot authorize production.

Confidence is an evidence-promotion control, not mathematical authority. No research claim, regardless of confidence, can add curriculum scope, create a mathematical fact, or override Engineering/curriculum authority.

## 3. Core2A/Core2B — learner-calibration control

Generation is blocked until there is one valid learner-calibration path.

### Path A — knowledge percentage known

Required:

```text
learner_knowledge_percent = 0..100
knowledge_percent_source_ref
knowledge_calibration_policy_ref
resolved_core2a_support_profile
resolved_core2a_max_demand_level
resolved_core2b_max_demand_level
```

The percentage is a generation-control input. It is not a new mastery state and does not replace `UNKNOWN / DEVELOPING / READY`.

The named calibration policy, not the architecture itself, maps percentage to the three resolved controls. This avoids hard-coded pseudo-precise bands.

### Path B — knowledge percentage unknown

The owner may explicitly waive the percentage requirement.

Required:

```text
owner_ref
waiver reason
owner-selected Core2A support profile
owner-selected Core2A maximum demand level
owner-selected Core2B maximum demand level
```

The system must not invent a percentage to fill the gap.

### Core2A uses calibration for

- question selection within legal scope;
- generated-item maximum demand;
- support density;
- worked-step granularity;
- representation support;
- ordering;
- generated near/structural variants with new provenance.

Frozen Core2 source questions remain frozen. A source question above the preferred generated-item ceiling may still appear when source/purpose policy requires it, but receives the resolved support treatment rather than being rewritten.

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

`STARTER / PRACTICE / REVISION / COMPETITION` remains mandatory for Core2A/Core2B.

```text
KNOWLEDGE % answers: how much support and how far may demand move?
PURPOSE answers: what job should this product perform?
```

Neither may silently infer the other.

## 5. Fail-closed states

```text
Core1 bucket without difficulty badge                         → BLOCK
EASY bucket with half-bound optional research                 → BLOCK
MEDIUM/HARD bucket without required research brief/evidence   → BLOCK
research decision coverage without a promoted claim           → BLOCK
promoted claim without supporting evidence                    → BLOCK
relevant retained source left unclassified for a claim        → BLOCK
contradictory promoted evidence without explicit resolution   → BLOCK
PRODUCTION promotion with LOW-confidence claim                → BLOCK
promoted claim source missing from generation binding         → BLOCK
bucket page budget above badge ceiling                        → BLOCK
Core1 depth changed because of learner knowledge %            → BLOCK

Core2 without knowledge % and without owner waiver            → BLOCK
Core2 with both knowledge % and owner waiver                  → BLOCK
knowledge % without source + calibration-policy ref           → BLOCK
owner waiver without Core2A support + 2A/2B demand ceilings   → BLOCK
silent/default knowledge %                                    → BLOCK
silent/default purpose                                        → BLOCK
```

## 6. Execution contract

`math-self-teaching-generation-spec.schema.json` captures the per-run inputs.

`validate_self_teaching_generation_spec.py` applies the semantic gates above.

`math-pedagogy-research-manifest.schema.json` and `validate_pedagogy_research_manifest.py` govern research evidence promotion and its generation binding.

The canonical self-teaching policy remains `math-self-teaching-policy.json`.
