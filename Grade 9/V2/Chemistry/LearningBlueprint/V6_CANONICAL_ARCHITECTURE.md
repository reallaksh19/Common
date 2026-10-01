# Chemistry LearningBlueprint v6 — canonical architecture

v6 freezes the Chemistry architecture before downstream learner-product regeneration. It does **not** patch old PDFs. It defines authority, routing, TTU families and release gates that future Core1A/Core1B/Core2A/Core2B products must consume.

## Canonical system

```text
OWNER CONTROL PLANE
        │
ORIGINAL GROUND TRUTH
        │
CORE0 — evidence + route
        │
        ├───────────────┐
        ▼               ▼
      CORE1           CORE2
   semantic pass   assessment pass
        │               │
        └──── fresh cross-validation ────┐
                                         ▼
                              C1 × C2 JOIN / AUDIT
                                         │
                                         ▼
                              CANONICAL DOMAIN REGISTRY
                                         │
                                         ▼
                                        CDAU
                         cross-Core lineage / differentiation
                                         │
                         ┌───────────────┴───────────────┐
                         ▼                               ▼
                        SDU                             LAU
                 Core1A / Core1B                 Core2A / Core2B
                 intrinsic difficulty            learner/task fit
                         │                               │
                         ▼                               ▼
                    CONCEPT TTU                     PROBLEM TTU
                         │                               │
                   ┌─────┴─────┐                   ┌─────┴─────┐
                   ▼           ▼                   ▼           ▼
                Core1A       Core1B              Core2A       Core2B
             declarative   open concept        declarative   open problem
               reference      tutor              worked        tutor
                   │           │                   │           │
                   └───── self-help closure ───────┴───────────┘
                                         │
                                         ▼
                               publication / PDF gate
```

## Existing blueprint versions remain authoritative

v6 is additive and does not erase earlier controls:

```text
v0  evidence routing / Core0
v1  independent Core1/Core2 grounding + relay/join discipline
v2  learner-state/purpose assimilation reasoning
v3  Core2 transfer eligibility
v4  Core1 intrinsic bucket depth + Core2 conditioning route
v5  product completeness + reconstructable TTUs + anti-padding
v6  Canonical Registry + CDAU + SDU/LAU split + Concept/Problem TTU families
```

## Authority hierarchy

| Authority | Owns |
|---|---|
| Ground Truth | what was actually supplied |
| Core1 | Chemistry semantic structure |
| Core2 | assessment/question-demand structure |
| Canonical Domain Registry | validated reusable assets with stable IDs |
| CDAU | cross-Core lineage, purpose, differentiation, duplication and release governance |
| SDU | Core1A/Core1B intrinsic-depth decisions |
| LAU | Core2A/Core2B learner × task × purpose support fit |
| TTU | technical completeness of one learning interaction |
| Owner | auditable operational decisions without rewriting truth/provenance |

Owner action is represented as:

```text
SYSTEM FINDING
+ OWNER OVERRIDE
= FINAL OPERATIONAL ACTION
```

The historical system finding remains preserved.

## Canonical Domain Registry

The registry is downstream of the Core1 × Core2 join. It stores stable validated objects such as:

```text
CONCEPT
MODEL
LAW
EQUATION
DERIVATION
CAPABILITY
LEARNING_ATOM
REPRESENTATION
MISCONCEPTION
PROBLEM_FAMILY
SOURCE_QUESTION
CANONICAL_SOLUTION
EXAMPLE
VERIFICATION_RULE
```

Downstream products reference these stable assets instead of rebuilding domain truth from prose.

## CDAU — cross-Core governance only

CDAU owns concerns that span both tracks:

```text
Core purpose contracts
content lineage
asset reuse
source custody
representation lineage
example/problem fingerprints
duplicate detection
A/B differentiation
owner decision provenance
self-help requirements
cross-Core release policy
```

CDAU does **not** select Core2 support and does **not** rewrite Core1 intrinsic difficulty. Those belong to LAU and SDU respectively.

Legal reuse classes:

```text
SEMANTIC_REUSE                allowed
PEDAGOGICAL_TRANSFORMATION    allowed
DECLARED_FADING_ANCHOR        allowed
NEAR_DUPLICATE                warning
PEDAGOGICAL_DUPLICATION       fail
```

## SDU — Study Differentiation Unit

SDU governs **only Core1A and Core1B**.

```text
SDU MUST NOT CONSUME STUDENT KNOWLEDGE %
```

Its inputs are intrinsic subtopic difficulty, difficulty authority/evidence, research dossier, concept decomposition, representation requirements and misconception structure.

Difficulty:

```text
EASY    max normal envelope 10 pages   research NONE by default
MEDIUM  max normal envelope 20 pages   TARGETED research required
HARD    max normal envelope 30 pages   DEEP research required
```

These are capacities, not targets. Release requires closure, not page-budget exhaustion.

SDU depth release requires:

```text
all learning atoms closed
all major inferential jumps bridged
representation coverage complete
equation assimilation complete
misconception coverage complete
page budget exhaustion NOT required
```

Core1A and Core1B share the same intrinsic badge and domain authority, but not necessarily the same page count, examples, sequence, representations or learner actions.

## LAU — Learner Adaptation Unit

LAU governs **only Core2A and Core2B**.

Exactly one conditioning route is legal:

```text
KNOWLEDGE_EVIDENCE
or
OWNER_OVERRIDE when learner knowledge is unknown
```

No fabricated 50% prior is allowed.

Knowledge percentage is a routing prior, not mastery. Capability-level subdimensions refine it:

```text
recognition
representation
model selection
first move
execution
explanation
verification
```

LAU must combine learner condition with question-bound task demand and purpose.

```text
InstructionalFit = f(LearnerState or OwnerOverride, TaskDemand, Purpose)
```

Task-demand vector:

```text
conceptual_demand
structural_distance
representation_change
model_discrimination
hidden_constraint
sign_direction_reversal
reversed_target
constraint_inversion
multi_step_bridge
synthesis
competitive_mixing
calculation_load
```

Support bands:

```text
FOUNDATION_HIGH_SUPPORT
GUIDED
STANDARD
CHALLENGE_MINIMAL
```

A high-knowledge learner may still receive GUIDED support for a distant synthesis task. A low-knowledge learner may receive STANDARD support for a low-demand retrieval task. Percent alone never fixes support.

Support must never alter frozen question identity, source provenance, validated semantic scope or canonical solution correctness.

## Concept TTU

Concept TTUs are used by Core1A/Core1B and center on:

```text
conceptual change
equation meaning
representation
derivation
contrast
```

Canonical anatomy includes:

```text
identity
canonical expert state
learner before-model
target model
conceptual change
reconstruction options
reconstructable TTU references
self-help closure
verification
differentiation fingerprint
```

### Core1A

Core1A is the **Declarative Concept Reference**.

```text
show / explain / derive / model
then require completion or reconstruction
```

Exposure mode:

```text
MODEL_THEN_RECONSTRUCT
```

### Core1B

Core1B is the **Open Concept Reconstruction Tutor**.

```text
predict
draw / label / generate
select / discriminate
derive / connect
diagnose
verify
teach back
```

Exposure mode:

```text
RECONSTRUCT_BEFORE_CANONICAL
```

Core1B requires a Tutor Dialogue contract.

## Problem TTU

Problem TTUs are used by Core2A/Core2B and center on:

```text
recognition
model selection
constraint/event
representation
first move
solution path
verification
transfer
```

Canonical anatomy includes task state, expert solution state, task demand, learner interaction, transfer lineage, reconstructable TTUs, self-help and differentiation fingerprints.

Legal Core2A → Core2B lineage:

```text
FADING_ANCHOR
same problem transformed from complete to reconstructive
NOT transfer evidence

STRUCTURAL_SIBLING
same problem family, new instance/surface
near-transfer evidence

FAR_TRANSFER_SIBLING
representation/target/constraint/model combination changes
far-transfer evidence
```

### Core2A

Core2A is the **Adaptive Declarative Problem Reference**.

```text
QUESTION
→ what is tested
→ recognition cues
→ model / event / constraint
→ representation
→ first non-obvious move
→ step-by-step solution
→ why each step works
→ answer
→ independent check
→ common wrong route
→ related variation
```

Exposure mode:

```text
SETUP_THEN_COMPLETE
```

### Core2B

Core2B is the **Adaptive Open Problem Tutor**.

```text
NEW QUESTION
→ attempt
→ notice relevant structure
→ select concept/family
→ identify changing/invariant structure
→ choose/build representation
→ identify event/constraint
→ select model
→ commit first move
→ reason/calculate
→ verify
→ canonical reveal
→ compare learner/expert routes
→ repair
→ further transfer
```

Exposure mode:

```text
CHOOSE_OR_RECONSTRUCT_BEFORE_HINTS
```

Core2B requires a Tutor Dialogue contract.

## Tutor Dialogue contract

B-layer dialogue is static, bounded and target-driven. It is not a chatbot and does not infer learner state at runtime.

A dialogue always requires an answer-hidden initial attempt and an observable learner commitment. It then selects only the stages needed for the targeted conceptual/problem-solving change from:

```text
ATTEMPT
NOTICE
REPRESENT
EXPLAIN
CONNECT
START
CHECK
REFLECT
```

Not every TTU must use every stage. Repeating a generic six-stage template across all TTUs is a design failure.

Every dialogue closes with canonical reveal after attempt, learner/expert comparison, independent verification and a static repair route.

## Self-help closure

Every Core1A/Core1B/Core2A/Core2B interaction must be independently usable without a teacher.

Required closure:

```text
canonical answer/state
progressive help
misconception help
canonical reveal
independent verification
repair path
next step
```

## Reconstructable TTUs remain mandatory

v5 reconstructability remains in force. A finished diagram, graph, table or equation does not count merely because it exists.

Reconstructable forms include incomplete diagrams, component assemblies, graph completions, equation skeletons, event lines, ledgers, decision trees, reaction schemes, representation maps, particle/species maps and oxidation-state lanes.

The learner must rebuild chemically meaningful missing structure; hints must bind to that missing structure; canonical completion and independent verification must exist.

## Purpose contracts

```text
Core1A  deeply construct the conceptual model by studying complete reasoning
Core1B  reconstruct and independently use the conceptual model
Core2A  learn how an expert solves the relevant problem family
Core2B  recognise, model, solve, justify and transfer on new/unfamiliar problems
```

A/B is therefore not "answer shown versus answer hidden":

```text
A = CANONICAL COMPLETED STATE
B = CANONICAL RECONSTRUCTION EXPERIENCE
```

## Publication gates

```text
G0 Evidence
G1 Domain correctness
G2 Core purpose
G3 Differentiation / non-duplication
G4 TTU technical completeness
G5 Learner-task fit — Core2A/Core2B only
G6 Publication / rendered layout
G7 Calibration from observed learner evidence after use
```

G5 does not apply to Core1A/Core1B because learner knowledge is not a design input on the study-material track.

## State model

```text
DISCOVERED
→ ROUTED
→ CORE_GROUNDED
→ C1_C2_VALIDATED
→ REGISTRY_READY
→ CDAU_READY
→ SDU_READY / LAU_READY
→ TTU_READY
→ A/B_REALIZED
→ SELF_HELP_VALIDATED
→ PUBLICATION_VALIDATED
→ RELEASED
```

Blocking/side states remain explicit: evidence-blocked, disputed, out-of-scope, owner-held, prerequisite insertion, quarantined and stale.

## Central doctrine

> Ground truth determines what is supported.
>
> Core1 determines Chemistry semantic authority.
>
> Core2 determines assessment authority.
>
> CDAU keeps the six Core products differentiated, traceable and non-duplicative.
>
> SDU determines how deeply an intrinsically difficult subtopic is taught and reconstructed in Core1A/Core1B.
>
> LAU determines Core2A/Core2B support from learner evidence or explicit owner waiver together with task demand and purpose.
>
> A represents the canonical completed state.
>
> B represents the canonical reconstruction experience.
>
> TTU prevents either state from being pedagogically fake.

v6 is an architecture/release contract. It does not claim that a learner has mastered, retained or transferred the material merely because a compliant product was generated.
