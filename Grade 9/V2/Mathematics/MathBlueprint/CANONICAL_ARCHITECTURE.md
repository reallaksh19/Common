# Mathematics V2 — Canonical Six-Core Architecture

This document is the canonical target architecture for Mathematics V2. It sits above the existing executable MathBlueprint increments and the dual-track product model. Existing validators/contracts remain implementation assets, but future schema/engine work must converge on this architecture rather than treating earlier one-axis adaptation assumptions as canonical.

The governing invariants remain:

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.

PLANNED PEDAGOGY
!= COMPILED STATIC PRODUCT
!= RENDERED ARTIFACT
!= LEARNER ATTEMPT
!= LEARNER PERFORMANCE EVIDENCE
```

## Consolidated Specification Architecture

The Mathematics V2 canonical architecture is organized into a single governing root specification and three strictly bounded subordinate normative modules:

- **Root Architectural Specification**:
  - [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md) (System topology, authority hierarchy, Core0–Core2 lifecycle, join, SDU/LAU, and publication boundary)
- **Subordinate Normative Modules**:
  1. [`ENGINEERING_AUTHORITY.md`](ENGINEERING_AUTHORITY.md): Upstream Engineering Gates, Transitive Closure, Non-Authoritative Discovery Boundary, and Exact Custody Binding.
  2. [`PEDAGOGY_AND_CALIBRATION.md`](PEDAGOGY_AND_CALIBRATION.md): Dual-Track Model (SDU vs LAU), Declarative Self-Teaching (A) vs Reconstructive Self-Tutoring (B), Difficulty Badges, and Reconstructable TTUs.
  3. [`PRODUCT_GOVERNANCE_GATE.md`](PRODUCT_GOVERNANCE_GATE.md): Coverage Ledger, Cross-Core Similarity Auditing, Anti-Gaming Invariants, and Publication Freeze Criteria.
  4. [`SUBTOPIC_INTELLIGENCE_INTAKE_SPECIFICATION.md`](SUBTOPIC_INTELLIGENCE_INTAKE_SPECIFICATION.md): Subtopic Intelligence Library (SIL) 4-Layer Intake Architecture, Verification Gates, and Concrete Subtopic Foundation Packets.
- **Derived Observability & Tooling**:
  - [`tools/index.html`](tools/index.html): Unified Observability Workbench Portal
  - [`tools/run_builder/index.html`](tools/run_builder/index.html): MathBlueprint Run Builder
  - [`tools/architecture_explorer/index.html`](tools/architecture_explorer/index.html): Blueprint Architecture Explorer
  - [`benchmarks/discovery/index.html`](benchmarks/discovery/index.html): Discovery Benchmark Quality Explorer
  - [`CORE_ARCHITECTURE_DRIFT_AUDIT.md`](CORE_ARCHITECTURE_DRIFT_AUDIT.md): 17-Section Normative Consistency Audit & Academician Matrix

## 1. Canonical system topology

```text
OWNER CONTROL PLANE
purpose • policy • difficulty override • routing override • inclusion/exclusion
learner-% waiver • support override • release/hold
        |
        v
ORIGINAL GROUND TRUTH
questions • syllabus • authoritative sources • figures • answers • owner scope
        |
        v
CORE0 — EVIDENCE + ROUTE
        |
        +-----------------------------+
        |                             |
        v                             v
CORE1 FIRST                      CORE2 FIRST
semantic reconstruction          assessment reconstruction
        |                             |
        v                             v
K-* packets                      D-* packets
instance ends                    instance ends
        |                             |
        v                             v
fresh CORE2                      fresh CORE1
independent GT pass              independent GT pass
        |                             |
        +-------------+---------------+
                      v
              C1 × C2 JOIN / AUDIT
                      |
                      v
            CANONICAL DOMAIN REGISTRY
concepts • models • equations • derivations • learning atoms
representations • misconceptions • problem families • frozen questions
canonical solutions • capabilities • validity • provenance
                      |
                      v
                    CDAU
       cross-core differentiation + lineage + owner governance
                      |
          +-----------+-----------+
          |                       |
          v                       v
         SDU                     LAU
Study Differentiation       Learner Adaptation
Core1A / Core1B             Core2A / Core2B
intrinsic difficulty        knowledge % OR owner override
NO learner-% depth          × task demand × family × purpose
          |                       |
          v                       v
      CONCEPT TTUs             PROBLEM TTUs
       +-----+                  +-----+
       |     |                  |     |
       v     v                  v     v
    Core1A Core1B            Core2A Core2B
    complete reconstructive  complete reconstructive
       |     |                  |     |
       +--+--+                  +--+--+
          |                       |
          v                       v
      SELF-HELP CLOSURE       SELF-HELP CLOSURE
          +-----------+-----------+
                      v
              LearnerPageBlueprint
                      |
                      v
                PUBLICATION GATE
                      |
                      v
                LEARNER PRODUCT
                      |
                      v
          optional observed learner evidence
                      |
                      v
        governed learner-intelligence update
        affecting later Core2A/Core2B only
```

## 2. Authority hierarchy

Authority domains are explicit and non-interchangeable.

| Authority | Controls |
|---|---|
| Ground Truth | what was actually supplied / verified as authoritative evidence |
| Core1 | subject-semantic structure |
| Core2 | assessment/question-demand structure and source-question custody |
| Canonical Domain Registry | validated reusable mathematics and assessment assets |
| CDAU | cross-core differentiation, lineage, duplicate control and owner-decision provenance |
| SDU | intrinsic-depth/research/representation decisions for Core1A/Core1B |
| LAU | learner-fit/support/demand decisions for Core2A/Core2B |
| TTU | technical completeness of one learning/reconstruction interaction |
| Owner | final operational controls, never historical/source truth |

Owner override preserves the system finding:

```text
SYSTEM FINDING
+ OWNER OVERRIDE
= FINAL OPERATIONAL ACTION
```

An override may change routing, difficulty badge, research intensity, decomposition, core inclusion, representation choice, learner-% waiver, support band, question-family inclusion or release/hold. It may not rewrite mathematical truth, frozen source wording, source provenance, observed evidence or answer correctness.

## 3. Core0 — evidence router, not an educational core

Core0 creates bounded relay work and decides which independent specialist should lead first. It does not teach and it does not replace Core1/Core2 intelligence.

Routing evidence should preserve separate dimensions such as:

```text
scope authority
semantic source strength
question evidence
question resolution
scope uncertainty
conflict index
```

Directionally:

```text
strong semantic authority              -> CORE1_FIRST
weak/coarse semantics + rich questions -> CORE2_FIRST
strong conflict                         -> BLOCK_CONFLICT
insufficient evidence                   -> BLOCK_EVIDENCE / OWNER_ADJUDICATION
```

Substantive relay bundles contain at most three subtopics. This is a transport limit only; it never limits learning-atom decomposition.

## 4. Independent-agent invariant

Freshness is an epistemic control, not merely a new agent identifier.

```text
same specialist profile may be reused
same analysis instance may NOT validate itself
```

For each dual-intelligence pass:

```text
PASS 1 — ground-truth-only independent analysis
PASS 2 — seal independent package
PASS 3 — expose predecessor package only after sealing
PASS 4 — claim-level CONFIRM / REFINE / MISSING / UNSUPPORTED /
         CONTRADICTED / OUT_OF_SCOPE / UNKNOWN
PASS 5 — perform role-specific downstream work
```

Cross-validation never silently mutates sealed specialist packages.

## 5. Relay bundle and subtopic granularity

A relay bundle records ground-truth refs, owner context, purpose, one-to-three subtopics, producer role/run, packet refs, validation summary, unknowns, conflicts, proposed splits and next role.

The distinction is mandatory:

```text
SUBTOPIC      = relay / publication governance unit
LEARNING ATOM = smallest cognitive teaching unit
```

An atom should split when the entity/state, governing model, representation, sign/frame convention, constraint/event, symbolic relation, algebraic transformation, interpretation, special case or misconception boundary changes. Stop splitting when the next learner transition requires no more than one permissible inferential jump.

## 6. Core1

Core1 is compact semantic authority/basic orientation. It owns concept, model, equation, derivation, prerequisite, constraint, invariant, state, validity, concept boundary, representation affordance and structural contrast.

For an important equation, Core1 should retain the full cognitive anatomy when evidence supports it:

```text
mathematical question
-> parent model/law
-> assumptions
-> frame/sign choice
-> derivation
-> why transformations are legitimate
-> final relation
-> term meaning
-> mathematical interpretation
-> graphical/geometric interpretation
-> special cases
-> inverse uses
-> validity limits
-> failure cases
```

Core1 does not inflate into Core1A prose.

## 7. Core2

Core2 preserves frozen source-question identity and authored hint custody. Source stems remain immutable.

Core2 may additionally record problem family, required capabilities, recognition cues, hidden conditions, representation requirements, first non-obvious move, inferential jumps, wrong reasoning chains, task-demand vector, H1/H2/H3 contract and transfer envelope.

When a known semantic node has no questions, the correct state is ZERO_EVIDENCE. Zero questions cannot imply zero conceptual importance, low exam importance or absence of difficulty.

## 8. Canonical Domain Registry

After Core1/Core2 independent validation and join, reusable validated objects enter the registry with stable IDs. Typical classes:

```text
CONCEPT
MODEL
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

Fresh downstream agents consume typed registry objects rather than reconstructing the world from untyped prose. Registry admission never bypasses ground-truth provenance.

## 9. CDAU — cross-core governance umbrella

CDAU remains the umbrella layer. It does not directly choose learner support.

CDAU owns:

```text
core purpose contracts
content lineage
asset reuse and source custody
representation lineage
example/problem fingerprints
duplicate detection
A/B differentiation
owner-decision provenance
self-help requirements
cross-core release policy
```

Learner adaptation is explicitly delegated to LAU; study depth is explicitly delegated to SDU.

## 10. Canonical core-purpose contracts

### Core1

```text
Purpose: compact mathematical orientation/basic notes
Learner action: read / reference / recall
```

### Core1A

```text
Purpose: deeply construct the conceptual model
Learner action: inspect / follow / compare / interpret / study complete reasoning
Control: SDU intrinsic difficulty
```

### Core1B

```text
Purpose: reconstruct and independently use the conceptual model
Learner action: predict / draw / label / generate / select / explain /
                derive / diagnose / verify
Control: same SDU intrinsic difficulty as Core1A
```

### Core2

```text
Purpose: preserve frozen source assessment and ladder hints
Learner action: attempt with governed hints/checks
```

### Core2A

```text
Purpose: learn how an expert recognizes and solves a legal problem family
Learner action: study completed/faded expert reasoning
Control: LAU learner fit × task demand × purpose
```

### Core2B

```text
Purpose: recognize, model and solve new/unfamiliar legal problems with bounded tutoring
Learner action: attempt / classify / choose representation / choose first move /
                reason / verify / transfer
Control: same LAU authority as Core2A
```

The A/B doctrine is:

```text
A = CANONICAL COMPLETED STATE
B = CANONICAL RECONSTRUCTION EXPERIENCE
```

B is never A copied with blanks or paragraphs reordered.

## 11. SDU — Study Differentiation Unit

SDU governs Core1A/Core1B only.

Inputs:

```text
subtopic/bucket
intrinsic difficulty badge EASY | MEDIUM | HARD
governed mathematics
research dossier when required
owner controls
```

Outputs include depth obligations, representation obligations, sub-subtopic decomposition, Concept TTU plan, research requirements and page ceiling.

Hard rule:

```text
SDU MUST NOT inspect or infer learner knowledge percentage.
```

Page ceilings are capacities, not targets:

```text
EASY   <= 10 pages
MEDIUM <= 20 pages
HARD   <= 30 pages
```

A shorter product may be deeper than a longer one. Release is based on closure of mathematical/cognitive obligations, not page consumption.

### Research dossier

```text
EASY   -> no pedagogy-enrichment web research by default
MEDIUM -> TARGETED research required
HARD   -> DEEP research required
```

The dossier records semantic validation, learning difficulties, misconception evidence, representation evidence, visual/translation risks, useful/rejected pedagogical candidates and source provenance. Research can improve teaching design; it cannot enlarge curriculum authority.

## 12. LAU — Learner Adaptation Unit

LAU governs Core2A/Core2B only.

Exactly one learner-conditioning path must be resolved:

```text
A. KNOWLEDGE_PERCENT 0..100
   + evidence/source ref
   + named calibration policy

OR

B. OWNER_OVERRIDE
   + owner ref
   + explicit reason knowledge is unavailable
   + explicit support profile
   + explicit Core2A demand ceiling
   + explicit Core2B transfer ceiling
```

No default or inferred pseudo-percentage is legal. Knowledge percentage is a support prior, not a mastery claim and not a replacement for UNKNOWN / DEVELOPING / READY.

LAU combines learner evidence with a multi-dimensional task-demand vector, including at least:

```text
conceptual demand
structural distance
representation change
cue visibility
hidden constraint
method/model discrimination
sign/direction reversal
reversed target
constraint inversion
algebraic burden
multi-step bridge
synthesis
novelty
competitive mixing
```

Support therefore resolves from learner state × task demand, not from knowledge percentage alone.

Human-facing support modes are:

```text
FOUNDATION_HIGH_SUPPORT
GUIDED
STANDARD
CHALLENGE_MINIMAL
```

These map to concrete decisions about representation supply, cue visibility, first-move support, hint depth, solution delay, verification prompting, problem ordering and structural distance.

## 13. Purpose is separate from learner knowledge

Learning purpose and product mode must not be collapsed into knowledge percentage.

Canonical learning-purpose semantics remain upstream concerns such as:

```text
FIRST_STUDY
CONSOLIDATION
REVISION
COMPETITIVE_EXAM
```

Existing Core2A product modes remain a distinct downstream generation control:

```text
STARTER
PRACTICE
REVISION
COMPETITION
```

Knowledge percentage answers "how much support / how far can this item push?" Purpose answers "why is this product being made?"

## 14. Two TTU families

### Concept TTU

Used by Core1A/Core1B. Its centre of gravity is conceptual change, object/state model, equation meaning, representation, symbol bridge, derivation, contrast/misconception, validity boundary and verification.

### Problem TTU

Used by Core2A/Core2B. Its centre of gravity is recognition, model/method selection, constraints, representation choice, first non-obvious move, reasoning path, wrong route, verification and transfer.

Both families preserve canonical truth and lineage; their learner actions differ.

## 15. Reconstructable TTUs

A reconstructable TTU is a governed technical object with deliberately missing mathematically meaningful structure. Supported forms include:

```text
incomplete diagrams
component assemblies
incomplete graphs
equation/function skeletons
event or state lines
tables/ledgers
proof/reasoning chains
representation maps
construction sequences
flow/dependency models
```

Every TTU declares identity/family/stage, mathematics refs, complete-state ref, learner action, given parts, missing parts + semantic roles, target relations, fixed help, completion key, verification rule, fading level, lineage transform and bounded representation geometry where visual.

A fully completed figure/equation/table does not count as reconstructable. Randomly blanking words/numbers does not count either; the omission must represent mathematical structure.

Core exposure modes are fixed:

```text
Core1A -> MODEL_THEN_RECONSTRUCT
Core1B -> RECONSTRUCT_BEFORE_CANONICAL
Core2A -> SETUP_THEN_COMPLETE
Core2B -> CHOOSE_OR_RECONSTRUCT_BEFORE_HINTS
```

Fading within a lineage is normally monotone:

```text
MODELLED -> GUIDED -> FADED -> INDEPENDENT
```

A support reset in Core2 requires explicit LAU authority; Core1B cannot use learner percentage to reset SDU depth.

## 16. Tutor Dialogue Contract for B layers

B products are reconstruction experiences, not omission templates. A substantial static tutor episode may use the following authored stages when relevant:

```text
P0 ATTEMPT   — no help
P1 NOTICE    — identify the structural feature
P2 REPRESENT — construct/select diagram, graph, table, equation or model
P3 EXPLAIN   — justify the relation/representation
P4 CONNECT   — connect invariant, condition, event or prior concept
P5 START     — commit only the first mathematical move
REVEAL       — canonical state after attempt
REFLECT      — compare learner route with canonical route
VERIFY       — independent mathematical check
```

Not every TTU needs every stage. The sequence is target-driven and statically authored. A fixed misconception branch may be included, but the product cannot claim the learner actually exhibited that misconception.

## 17. Core2 hint distinction

Core2A hints support understanding of an expert solution path:

```text
H1 recognition/principle
H2 representation
H3 first operation or first move
```

Core2B hints preserve learner reconstruction:

```text
H1 NOTICE    — what structural feature should control your choice?
H2 REPRESENT — what representation would expose it?
H3 START     — write only the first governing relation/move
```

H3 must not collapse into a full solution dump.

## 18. Self-help closure

All derivative cores are self-taught. Every substantive TTU/episode must provide an eventual route to:

```text
progressive authored help
canonical answer/reveal
misconception/wrong-route support where relevant
independent verification
repair or next-step pointer
```

Core1A normally exposes canonical explanation earlier. Core1B/Core2B normally delay reveal until after an attempt. Static answer availability is not learner evidence.

## 19. Cross-core duplication and lineage

CDAU classifies reuse as:

```text
SEMANTIC_REUSE               allowed
PEDAGOGICAL_TRANSFORMATION   allowed
FADING_ANCHOR                allowed when declared
NEAR_DUPLICATE               warning
PEDAGOGICAL_DUPLICATION      fail
```

Immutable source stems, canonical definitions/formulas and answer identities may repeat with explicit lineage. Narrative/expository reuse must be transformed.

Example/problem fingerprints should record context, problem family, known quantities, numerical values, target unknown, representation, model sequence, special condition and solution path. Cosmetic context substitution is not a new example.

## 20. Core2A -> Core2B lineage

Legal transfer relations include:

```text
FADING_ANCHOR
same problem, A complete -> B reconstructive
useful for transition; not transfer evidence

STRUCTURAL_SIBLING
new instance, same family/capabilities, altered surface/givens
normal transfer mode

FAR_TRANSFER_SIBLING
changes representation, target, constraint form, method/family combination,
sign/direction or synthesis demand
stronger transfer mode
```

All remain inside Core2A legality and the LAU ceiling.

## 21. Validation gates

Release passes through explicit gates:

| Gate | Must prove |
|---|---|
| G0 Evidence | provenance and evidence state are known |
| G1 Domain | mathematics is valid and within authority |
| G2 Purpose | interaction belongs in this core |
| G3 Differentiation | not a disguised duplicate of adjacent core |
| G4 TTU | technical teaching/reconstruction interaction is complete |
| G5 Fit | for Core2A/Core2B, learner × task × support decision is justified |
| G6 Publication | typesetting/layout preserves the governed interaction |
| G7 Calibration | later observed learner evidence can confirm/revise fit |

G5 does not use learner percentage for Core1A/Core1B.

A B-TTU is complete only when it has a semantic/problem target, canonical expert state, meaningful learner transformation, observable learner product, bounded help, canonical reveal, independent verification and repair/next-step route.

## 22. Publication state machine

A subtopic may advance through:

```text
DISCOVERED
-> ROUTED
-> CORE_GROUNDED
-> C1_C2_VALIDATED
-> REGISTRY_READY
-> CDAU_READY
-> SDU_READY / LAU_READY
-> TTU_READY
-> A/B_REALIZED
-> SELF_HELP_VALIDATED
-> PUBLICATION_VALIDATED
-> RELEASED
```

Side states remain explicit, including BLOCKED_EVIDENCE, DISPUTED, OUT_OF_SCOPE, OWNER_HELD, INSERT_PREREQUISITE, QUARANTINED and STALE.

## 23. Packet namespaces

The target packet namespace is:

```text
GT-*   original ground-truth manifests
RT-*   routing decisions
K-*    Core1 semantic packets
D-*    Core2 assessment packets
V-*    validation
J-*    C1 × C2 join
REG-*  canonical registry assets
CD-*   CDAU governance
SD-*   SDU decisions
LA-*   LAU decisions
CT-*   Concept TTU
PT-*   Problem TTU
A1-*   Core1A realization
B1-*   Core1B realization
A2-*   Core2A realization
B2-*   Core2B realization
T-*    learner/taught evidence
OVR-*  owner overrides
PUB-*  publication audit
```

Substantive packets carry stable identity, schema version, producer role/run, subtopic, ground-truth refs, upstream refs, claims, confidence/validation state, owner-override refs and content hash.

## 24. Publication boundary

Publication consumes governed learner products; it does not decide pedagogy. It may not invent mathematics, omissions, learner actions, hints, examples, representations, verification logic, answer custody or page-filling whitespace.

Publication compiles:

```text
validated Core realization + TTUs + lineage + provenance
-> LearnerPageBlueprint
-> deterministic typesetting
-> rendered-artifact semantic/surface audit
-> final PDF
```

Learner attempts and performance evidence remain post-delivery inputs outside static A/B compilation.

## 25. Implementation status and migration rule

This document freezes the target architecture. Existing executable increments remain valid where they do not conflict with it. In particular:

```text
GroundTruthManifest / routing / independence firewall / join
Core1A Assimilation Compiler
Core1A/Core1B intrinsic depth governance
Core2A/Core2B knowledge-or-owner calibration
technical composition + reconstructable TTUs
DUAL_TRACK_PRODUCT_MODEL.md
math-dual-track-product-model.schema.json
```

The next implementation work should translate this target into typed registry, CDAU, SDU, LAU, Concept-TTU and Problem-TTU contracts incrementally rather than introducing one schema for every conceptual packet.

No downstream implementation may reintroduce these rejected assumptions:

```text
learner knowledge % controls Core1A/Core1B depth
page allowance implies target page count
B = A with blanks
Core2B may exceed Core2A legal authority
owner override rewrites historical/source truth
static workbook use proves mastery
renderer authors missing mathematics or reconstruction structure
```

## 26. Central doctrine

> Ground truth determines what is supported.
>
> Core1 determines semantic authority.
>
> Core2 determines assessment authority.
>
> CDAU keeps the six products differentiated, traceable and non-duplicative.
>
> SDU determines how deeply an intrinsically difficult subtopic is taught and reconstructed in Core1A/Core1B.
>
> LAU determines what question demand and support are appropriate for Core2A/Core2B from learner evidence or explicit owner waiver.
>
> A represents the canonical completed state.
>
> B represents the canonical reconstruction experience.
>
> TTU ensures that neither state is pedagogically fake.
