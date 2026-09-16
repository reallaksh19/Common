# Mathematics V2 — Dual-Track Product Model

> **Consolidated Specification Notice**:
> This document is consolidated under the canonical subordinate module [`PEDAGOGY_AND_CALIBRATION.md`](PEDAGOGY_AND_CALIBRATION.md) as part of Mathematics V2 Specification Consolidation. It is preserved here for contract stability, historical references, and granular analysis.

This normative subordinate contract defines the two learner-product control systems below the current Engineering-authorized Canonical Domain Registry. It does not create mathematical authority: all mathematical identities and topic-specific technical truth consumed here must already be admitted through the exact Engineering authority path defined by `CANONICAL_ARCHITECTURE.md` and `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md`.

Core1-series study material is governed by **intrinsic mathematical difficulty**. Core2-series question material is governed by **learner adaptation against task demand**.

```text
       ENGINEERING-AUTHORIZED CANONICAL DOMAIN REGISTRY
 concepts • equations • models • representations • capabilities
 misconceptions • learning atoms • problem families • source questions
 canonical solutions • exact provenance / Engineering custody
                              │
             ┌────────────────┴────────────────┐
             │                                 │
      STUDY-MATERIAL TRACK               QUESTION TRACK
        Core1A / Core1B                  Core2A / Core2B
             │                                 │
             ▼                                 ▼
  STUDY DIFFERENTIATION UNIT          LEARNER ADAPTATION UNIT
           SDU                                  LAU
             │                                 │
 intrinsic EASY/MEDIUM/HARD          knowledge % OR owner override
 no learner % may alter depth        + task demand + purpose
             │                                 │
             ▼                                 ▼
       CONCEPT TTU FAMILY                 PROBLEM TTU FAMILY
        ┌────┴────┐                        ┌────┴────┐
        ▼         ▼                        ▼         ▼
      Core1A    Core1B                   Core2A    Core2B
     COMPLETE  RECONSTRUCTIVE           COMPLETE  RECONSTRUCTIVE
```

## 1. Canonical stage identities

| Stage | Learner-facing identity | Control basis | TTU realization |
|---|---|---|---|
| Core1A | Declarative Concept Reference | intrinsic subtopic difficulty | complete Concept TTU |
| Core1B | Open Concept Reconstruction Tutor | same intrinsic subtopic difficulty | reconstructive Concept TTU |
| Core2A | Adaptive Declarative Problem Reference | learner calibration × task demand × purpose | complete Problem TTU |
| Core2B | Adaptive Open Problem Tutor | same learner calibration × task demand × purpose | reconstructive Problem TTU |

The A/B distinction is **not** answer shown versus answer hidden.

```text
A = CANONICAL COMPLETED STATE
B = CANONICAL RECONSTRUCTION EXPERIENCE
```

A B-layer product must change the learner action. It may not be the A-layer exposition copied with blanks or reordered paragraphs.

## 2. Study Differentiation Unit (SDU) — Core1A/Core1B only

The SDU consumes:

```text
subtopic/bucket
+ intrinsic difficulty badge
+ governed mathematics
+ governed research decision/evidence when promoted or required
```

It emits:

```text
depth obligations
representation obligations
sub-subtopic decomposition where justified
Concept TTU plan
Core1A / Core1B page-cap ceiling
research obligation/binding state
```

The SDU MUST NOT inspect or infer learner knowledge percentage.

### Difficulty policy

```text
EASY   → up to 10 pages; pedagogy-enrichment research OPTIONAL
MEDIUM → up to 20 pages; TARGETED research REQUIRED
HARD   → up to 30 pages; DEEP research REQUIRED
```

These are ceilings, never quotas. Closure is the quality metric, not page count.

Research permission and research obligation are distinct. Discovery/search is allowed at every difficulty. EASY has no minimum research obligation, but if optional research is promoted its governed brief/decision and evidence references must be completely bound. MEDIUM/HARD remain fail-closed on their targeted/deep research requirements.

### Current EASY materialization limitation — C0-F007

The current policy and `validate_self_teaching_generation_spec.py` accept a fully bound optional EASY research state. The canonical `compile_sdu_lau_generation_spec.py` path currently writes research bindings only to non-EASY rows.

Therefore:

```text
OPTIONAL EASY RESEARCH POLICY / VALIDATION      = CURRENT + EXECUTABLE
OPTIONAL EASY RESEARCH AUTO-MATERIALIZATION
THROUGH THE CANONICAL SDU/LAU COMPILER          = CURRENT + DOCUMENTED ONLY
```

This contract must not be read as claiming automatic compiler materialization until a separate governed compiler migration and falsifier upgrade that status.

### Claim-level research promotion

External research is not promoted merely because a source URL was found. Promotion follows the governed claim ledger:

```text
OPEN DISCOVERY / SEARCH
        ↓
RESEARCH DECISION
(subtopic + depth + coverage + retained sources)
        ↓
PEDAGOGY CLAIM
        ↓
EVIDENCE LINKS
SUPPORTS | CONTRADICTS
        ↓
CONFIDENCE
LOW | MODERATE | HIGH
        ↓
CONTRADICTION RESOLUTION when needed
        ↓
PROMOTED GENERATION BINDING
```

The research layer may improve representation, explanation, decomposition, misconception treatment and transfer design. It may not expand legal mathematics, replace Engineering authority or create curriculum scope. There is no universal minimum source-count quota.

The exact evidence-promotion contract remains in `GENERATION_CALIBRATION.md`, `math-pedagogy-research-manifest.schema.json` and `validate_pedagogy_research_manifest.py`.

## 3. Learner Adaptation Unit (LAU) — Core2A/Core2B only

The LAU consumes:

```text
frozen/legal Core2 question authority
+ capability-specific or aggregate knowledge evidence
  OR explicit owner override when knowledge is unavailable
+ task-demand vector
+ problem family
+ purpose
```

It emits:

```text
support mode
question / transfer ceiling
representation support
hint depth
first-move support
solution exposure / delay
problem ordering
structural distance allowance
Problem TTU plan
```

The LAU may never manufacture a pseudo-knowledge percentage. Exactly one calibration path is legal:

```text
A. KNOWLEDGE_PERCENT
   + evidence/source reference
   + named calibration policy

OR

B. OWNER_OVERRIDE
   + reason knowledge is unavailable
   + explicit support controls
   + explicit Core2A demand ceiling
   + explicit Core2B transfer ceiling
```

Knowledge percentage is a support prior, not a mastery claim. It cannot rewrite frozen source identity, provenance, validated scope, Engineering authority or answer correctness.

### Task-demand vector

Difficulty is multi-dimensional rather than one scalar label. LAU may reason over dimensions including:

```text
conceptual_demand
structural_distance
representation_change
cue_visibility
hidden_constraint
model_or_method_discrimination
sign_or_direction_reversal
reversed_target
constraint_inversion
algebraic_burden
multi_step_bridge
synthesis
novelty
competitive_mixing
```

Support is routed against **learner evidence × task demand × purpose**, not knowledge percentage alone.

### Learner-support semantics

Human-facing support modes are:

```text
FOUNDATION_HIGH_SUPPORT
GUIDED
STANDARD
CHALLENGE_MINIMAL
```

They map to concrete decisions about representation supply, cue visibility, first-move support, hint depth, solution delay, verification prompting, problem ordering and structural distance.

A high-knowledge learner may still receive GUIDED support on a distant synthesis item. A low-knowledge learner may receive STANDARD support on a simple retrieval item.

## 4. Two TTU families

### Concept TTU — Core1A/Core1B

Centres on:

```text
conceptual change
object/state model
equation meaning
representation
symbol bridge
derivation
contrast / misconception
validity boundary
verification
```

Core1A exposes the canonical completed model and may then ask for reconstruction. Core1B starts from reconstruction and uses the same authorized concept graph without adding new mathematics.

Core1B learner actions should include several of:

```text
PREDICT
LABEL
DRAW
CONNECT
CLASSIFY
COMPARE
EXPLAIN
SELECT
DERIVE
REBUILD
DISCRIMINATE
VERIFY
```

### Problem TTU — Core2A/Core2B

Centres on:

```text
recognition cue
model selection
constraint/event
representation choice
first non-obvious move
solution path
wrong route
verification
nearby transfer
```

Core2A is solution apprenticeship: show how an expert recognizes, represents and solves. Core2B is problem reconstruction: make the learner recover the model, representation and attack route before canonical reveal.

## 5. Reconstructable TTU contract

A reconstructable TTU is not an arbitrary fill-in-the-blank. It contains intentionally omitted **mathematically meaningful structure**.

Supported forms include:

```text
incomplete coordinate / geometric diagrams
component assemblies
incomplete graphs
function / equation skeletons
event or state lines
tables / ledgers
proof or reasoning chains
representation maps
construction sequences
flow / dependency models
```

Every TTU binds stable identity/family/stage, exact mathematical refs, complete-state ref, exposure mode, learner action, initial/given state, missing semantic parts, target relations, bounded help, completion key, verification rule, fading level and lineage.

A fully completed diagram, graph, equation, event line or table does **not** count as reconstructable. Omissions must correspond to mathematical structure such as a constraint, component, relation, event, branch, graph feature, transformation step or representation choice.

## 6. Core-specific TTU exposure modes

```text
Core1A → MODEL_THEN_RECONSTRUCT
Core1B → RECONSTRUCT_BEFORE_CANONICAL
Core2A → SETUP_THEN_COMPLETE
Core2B → CHOOSE_OR_RECONSTRUCT_BEFORE_HINTS
```

Fading is normally monotone inside a lineage:

```text
MODELLED → GUIDED → FADED → INDEPENDENT
```

A downstream TTU may not silently become more scaffolded than its parent unless an explicit governed support reset is recorded by LAU for Core2. Core1B cannot use learner percentage to reset SDU depth.

## 7. Tutor Dialogue Contract — B layers

B layers require more than omissions. A substantial static tutor episode may use:

```text
P0 ATTEMPT     — no help
P1 NOTICE      — direct attention to a structural feature
P2 REPRESENT   — construct/select diagram, graph, table, equation or model
P3 EXPLAIN     — state why the representation/relation is legitimate
P4 CONNECT     — connect invariant, condition, event or earlier concept
P5 START       — commit only the first mathematical move
REVEAL         — canonical state after attempt
REFLECT        — compare learner route with canonical route
VERIFY         — independent mathematical check
```

The authored prompt sequence is fixed in the static product. No live diagnosis is implied. A misconception branch may be included as a fixed corrective prompt, but it cannot claim that the learner actually exhibited the misconception.

## 8. Hint semantics differ across A/B problem products

Core2A hints support understanding of an expert path:

```text
H1 principle / recognition
H2 representation
H3 first operation / first move
```

Core2B hints preserve reconstruction:

```text
H1 NOTICE      — what feature should control model choice?
H2 REPRESENT   — what representation exposes that feature?
H3 START       — write only the first governing relation / move
```

H3 may not dump the full solution.

## 9. Self-help closure

Every substantive Concept TTU and Problem TTU closes the loop:

```text
progressive authored help
canonical answer/reveal
misconception or wrong-route support when relevant
independent verification
repair/next-step pointer
```

The static product must never leave the learner at a dead end, but it also must not confuse availability of help with measured mastery.

## 10. Cross-core differentiation

Neighboring cores may share canonical mathematical identities, but learner action must differ:

```text
Core1A → EXPLAIN / DERIVE / SHOW
Core1B → PREDICT / RECONSTRUCT / EXPLAIN / VERIFY

Core2A → STUDY EXPERT SOLUTION / UNDERSTAND
Core2B → RECOGNISE / SELECT / SOLVE / JUSTIFY / TRANSFER
```

If neighboring cores use the same example, same representation, same sequence, same solution narrative and same learner action, the transformation has failed.

Immutable source stems, canonical definitions/formulas and answer identities may repeat only under governed lineage rules.

## 11. Product release and publication boundary

Publication is downstream of product release. It does not decide pedagogy and it does not authorize mathematics.

The current governed path is:

```text
ENGINEERING-AUTHORIZED DOMAIN
      ↓
SDU or LAU
      ↓
Concept TTU / Problem TTU
      ↓
Core-specific realization
      ↓
product governance / release gate
      ↓
derived Engineering visibility
NON_AUTHORITATIVE; publication_authorization = NOT_IMPLIED
      ↓
semantic learner publication bundle
      ↓
validated rendering
      ↓
rendered-artifact audit
```

The current bound-release renderer invariant is:

```text
semantic_source = LEARNER_PUBLICATION_BUNDLE_ONLY
```

A `LearnerPageBlueprint` may still be used as an internal realization contract, but it is not the canonical final semantic publication source for the governed bound-release path.

Publication may typeset governed semantics. It may not decide what to omit, which learner action to request, what the hint sequence is, how support should fade, what the canonical completion is, what verification is valid, what new mathematics is legal or how many pages should exist merely to meet a count.
