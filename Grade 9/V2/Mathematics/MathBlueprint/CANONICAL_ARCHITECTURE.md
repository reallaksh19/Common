# Mathematics V2 — Canonical Six-Core Architecture

This document is the **normative architecture root** for Mathematics V2. It defines durable authority, identity, orchestration, learner-product and publication boundaries. Field-level rules that change independently remain in subordinate normative specifications and executable schemas, policies, validators and compilers.

The architecture is recovered from current governed behavior, not from conversational memory or topic-specific Blueprint logic. Design and audit material under `design/` may explain migration history, but it is non-normative and cannot override this root or executable authority.

The governing invariants are:

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.

DISCOVERY
!= TECHNICAL AUTHORITY
!= PEDAGOGY AUTHORITY
!= PUBLICATION AUTHORITY

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
- **Reference Research Standards**:
  - [`references/NANO_LEVEL_SUBTOPIC_INTELLIGENCE_RESEARCH.md`](references/NANO_LEVEL_SUBTOPIC_INTELLIGENCE_RESEARCH.md): Nano-Level Subtopic Intelligence Research (Grade 9–11 CBSE & IIT-JEE Continuum, Singularity Traps, Step-Marking Rigor, and Examiner Trap Matrices).
- **Derived Observability & Tooling**:
  - [`tools/index.html`](tools/index.html): Unified Observability Workbench Portal
  - [`tools/run_builder/index.html`](tools/run_builder/index.html): MathBlueprint Run Builder
  - [`tools/architecture_explorer/index.html`](tools/architecture_explorer/index.html): Blueprint Architecture Explorer
  - [`benchmarks/discovery/index.html`](benchmarks/discovery/index.html): Discovery Benchmark Quality Explorer
  - [`CORE_ARCHITECTURE_DRIFT_AUDIT.md`](CORE_ARCHITECTURE_DRIFT_AUDIT.md): 17-Section Normative Consistency Audit & Academician Matrix

## 1. Canonical authority topology

Human-language discovery may precede exact authority, but it never substitutes for it.

```text
OWNER CONTROL PLANE
purpose • policy • routing/difficulty override • inclusion/exclusion
learner-% waiver • support override • release/hold
        |
        v
ORIGINAL GROUND TRUTH / DECLARED SCOPE
questions • syllabus • authoritative sources • figures • answers • owner scope
        |
        +----------------------+
        |                      |
        |                NON-AUTHORITATIVE DISCOVERY
        |                labels • aliases • approximate search • hints
        |                      |
        |                      v
        |                ranked candidate identities
        |                      |
        |                EXPLICIT EXACT-ID SELECTION
        |                      |
        +----------------------+
                   |
                   v
CANONICAL MATHEMATICS ENGINEERING AUTHORITY
base registry + digest-bound extensions + governed invariant data
                   |
          schema + generic validation
          exact scope/crosswalk custody where needed
          FOUNDATION / STANDARD / RESEARCH depth
          deterministic prerequisite closure
                   |
                   v
ENGINEERING AUTHORIZATION BINDING(S)
                   |
                   v
CANONICAL DOMAIN ADMISSION
                   |
                   v
CORE0 — EVIDENCE + ROUTE
                   |
        +----------+----------+
        |                     |
        v                     v
   CORE1 FIRST            CORE2 FIRST
semantic reconstruction   assessment reconstruction
        |                     |
        v                     v
 sealed K-* package        sealed D-* package
        |                     |
        v                     v
 fresh CORE2              fresh CORE1
 independent GT pass      independent GT pass
        |                     |
        +----------+----------+
                   v
           C1 × C2 JOIN / AUDIT
                   |
                   v
          CANONICAL DOMAIN REGISTRY
canonical mathematical/assessment assets + scope memberships
                   |
                   v
                 CDAU
cross-core differentiation • lineage • owner governance
                   |
        +----------+----------+
        |                     |
        v                     v
       SDU                   LAU
Core1A / Core1B         Core2A / Core2B
intrinsic difficulty    learner evidence/waiver × task demand × purpose
        |                     |
        v                     v
   CONCEPT TTUs           PROBLEM TTUs
        |                     |
        v                     v
 Core1A / Core1B       Core2A / Core2B
        +----------+----------+
                   v
            SELF-HELP CLOSURE
                   |
                   v
            PRODUCT RELEASE GATE
                   |
                   v
DERIVED ENGINEERING VISIBILITY
non-authoritative explainability view
publication_authorization = NOT_IMPLIED
                   |
                   v
SEMANTIC LEARNER PUBLICATION BUNDLE
released product + governed examples + research custody
+ Engineering visibility + learner-facing semantic components
                   |
                   v
          deterministic rendering
                   |
                   v
     rendered-artifact semantic/surface audit
                   |
                   v
            GOVERNED LEARNER PRODUCT
                   |
                   v
      optional observed learner evidence
                   |
                   v
 governed learner-intelligence update
 affecting later Core2A/Core2B only
```

Operational execution may reorder independent work where contracts permit. No execution shortcut may bypass exact Engineering identity, current validation, requested Engineering depth, prerequisite closure or custody before mathematical authority is consumed downstream.

## 2. Authority hierarchy

Authority domains are explicit and non-interchangeable.

| Domain | Controls | Does not control |
|---|---|---|
| Ground Truth / Declared Scope | what was supplied, verified, frozen or explicitly scoped | mathematical validity by itself |
| Engineering registry + validation | canonical mathematical identities, topic-specific technical content, prerequisites, invariants, provenance, readiness and requested technical depth | pedagogy, learner fit or publication permission |
| Engineering authorization binding | exact validated gate closure a downstream scope may consume | discovery ranking or fuzzy interpretation |
| Core0 | evidence routing and bounded relay work | subject truth or teaching depth |
| Core1 | semantic reconstruction and compact orientation **within already-authorized Engineering scope** | new mathematical authority |
| Core2 | assessment/question-demand reconstruction and source-question custody **within already-authorized Engineering scope** | new mathematical authority |
| Canonical Domain Registry | validated reusable mathematical and assessment assets plus scope memberships | independent authorization outside bound upstream custody |
| CDAU | cross-core differentiation, lineage, duplicate control and owner-decision provenance | learner support |
| SDU | intrinsic-depth, representation and research obligations for Core1A/Core1B | learner-knowledge adaptation |
| LAU | learner-fit, support and demand ceilings for Core2A/Core2B | Core1 depth or subject truth |
| TTU | technical completeness of one learning/reconstruction interaction | new subject scope |
| Product release gate | cross-core governance and custody needed to release the governed product state | subject truth creation |
| Engineering visibility | derived explainability view of already-bound Engineering authority | technical or publication authorization |
| Semantic learner publication bundle | sole governed semantic input to the current bound-release renderer | new mathematics or pedagogy decisions |
| Owner | final operational controls and explicit waivers/holds | historical/source truth, mathematical truth or observed evidence |

Owner override preserves the underlying system finding:

```text
SYSTEM FINDING
+ OWNER OVERRIDE
= FINAL OPERATIONAL ACTION
```

An override may change routing, operational difficulty badge, decomposition, core inclusion, representation choice, learner-% waiver, support band, question-family inclusion or release/hold. It may not rewrite mathematical truth, frozen source wording, source provenance, observed evidence or answer correctness.

## 3. Engineering → Blueprint boundary

Engineering is upstream technical mathematical authority. Blueprint owns generic orchestration around that authority.

```text
Engineering owns:
- mathematical gate identities;
- topic/subtopic-specific mathematical content;
- prerequisites;
- gate-specific invariant data;
- provenance;
- technical readiness data.

Blueprint owns:
- non-authoritative discovery orchestration;
- exact request resolution;
- generic depth evaluation;
- deterministic prerequisite closure;
- custody/binding;
- downstream composition and release orchestration.
```

Production Blueprint/runtime must not create mathematical authority from topic-specific branches, hard-coded extension filenames, remembered aliases, fuzzy/semantic matching, LLM inference, conversation memory or undeclared capability-to-gate mappings.

A genuinely new mathematical capability is introduced through governed Engineering data. Greater rigor for the same capability uses the same gate plus a stronger generic `engineering_depth`. An existing capability newly required by a product/exam changes scope/crosswalk membership rather than mathematical truth.

The normative subsystem boundary is `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md`.

## 4. Non-authoritative Engineering discovery

Discovery answers “what might the user mean?”; Engineering authorization answers “what may the system consume?”. These are different operations.

Discovery may use natural-language labels, governed aliases, token overlap, approximate lexical similarity, hints, future embeddings, semantic search, model-assisted query expansion or web-assisted search. Those mechanisms may rank candidates only.

A discovery candidate, rank-1 result, vocabulary match, similarity score, model confidence or web result is **not** Engineering authority.

Promotion into authority requires:

```text
explicit exact identity selection
+ exact discovery-receipt custody when discovery was used
+ unchanged exact Engineering resolver
+ current Engineering validation
+ requested Engineering depth PASS
+ prerequisite closure PASS
```

The discovery receipt remains non-authoritative and cannot imply publication authorization. The normative discovery specification is `ENGINEERING_DISCOVERY.md`.

## 5. Core0 — evidence router, not an educational core

Core0 creates bounded relay work and decides which independent specialist should lead first. It does not teach and it does not replace Engineering, Core1 or Core2 authority.

Routing evidence preserves independent dimensions such as:

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

Substantive relay bundles contain at most three subtopics. This is a transport limit only; it never limits learning-atom decomposition or Engineering closure.

## 6. Independent-agent invariant

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

## 7. Core1 and Core2 responsibilities

Core1 and Core2 remain distinct downstream authorities, but neither may bypass upstream Engineering technical authorization.

### Core1

Core1 is compact semantic reconstruction/basic orientation. Within authorized scope it owns concept structure, model/equation meaning, derivation, prerequisite relationships, constraint/invariant/state representation, validity boundaries, representation affordances and structural contrasts.

Core1 may explain and organize authorized mathematics; it may not introduce a new mathematical capability or silently widen Engineering scope.

### Core2

Core2 preserves frozen source-question identity and authored hint custody. It may additionally record problem family, required capabilities, recognition cues, hidden conditions, representation requirements, first non-obvious move, inferential jumps, wrong reasoning chains, task-demand vector, hint contract and transfer envelope.

When a known semantic node has no questions, the correct state is `ZERO_EVIDENCE`. Zero questions cannot imply zero conceptual importance, low exam importance or absence of difficulty.

## 8. Canonical Domain Registry

The Canonical Domain Registry composes validated reusable objects from bound Engineering authority, Core1/Core2 reconstruction and exact source custody.

Typical object classes include:

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

Engineering source identity is canonical mathematical identity for Engineering-derived assets. The same source object is stored canonically once; teaching scope, direct/prerequisite role, local capability use and question/bucket use are represented as separate membership metadata rather than duplicate truth.

Fresh downstream agents consume typed registry objects rather than reconstructing authority from untyped prose. Registry admission never bypasses source provenance or Engineering custody.

The normative asset/custody specification is `CANONICAL_ENGINEERING_DOMAIN_ASSETS.md`.

## 9. CDAU — cross-core governance umbrella

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

Learner adaptation is delegated to LAU; study depth is delegated to SDU.

## 10. Canonical core-purpose contracts

| Stage | Purpose | Learner action | Governing control |
|---|---|---|---|
| Core1 | compact mathematical orientation/basic notes | read / reference / recall | authorized Engineering scope + Core1 semantic reconstruction |
| Core1A | deeply construct the conceptual model | inspect / follow / compare / interpret / study complete reasoning | SDU intrinsic difficulty |
| Core1B | reconstruct and independently use the conceptual model | predict / draw / label / generate / select / explain / derive / diagnose / verify | same SDU intrinsic difficulty as Core1A |
| Core2 | preserve frozen source assessment and governed hint custody | attempt with governed hints/checks | source-question custody + authorized Engineering scope |
| Core2A | learn how an expert recognizes and solves a legal problem family | study completed/faded expert reasoning | LAU learner fit × task demand × purpose |
| Core2B | recognize, model and solve new/unfamiliar legal problems with bounded tutoring | attempt / classify / choose representation / choose first move / reason / verify / transfer | same LAU authority as Core2A |

The A/B doctrine is:

```text
A = CANONICAL COMPLETED STATE
B = CANONICAL RECONSTRUCTION EXPERIENCE
```

B is never A copied with blanks or paragraphs reordered.

## 11. SDU — Study Differentiation Unit

SDU governs Core1A/Core1B only. It must not inspect or infer learner knowledge percentage.

The current governed difficulty obligations are:

```text
EASY   -> <=10-page ceiling; pedagogy research OPTIONAL
MEDIUM -> <=20-page ceiling; TARGETED research REQUIRED
HARD   -> <=30-page ceiling; DEEP research REQUIRED
```

Page budgets are ceilings, not quotas. Closure of mathematical and cognitive obligations is the quality criterion.

Research permission and research obligation are separate. Discovery/search may occur at every difficulty. EASY has no minimum pedagogy-research obligation; if optional research is promoted, its governed brief/decision and evidence custody must be complete. MEDIUM/HARD remain fail-closed on required research.

The exact generation-control rules remain in `GENERATION_CALIBRATION.md` and `SELF_TEACHING.md`.

## 12. Claim-level pedagogy-research promotion

Research discovery is permissive; promotion into generation is strict and claim-specific.

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
        ↓
PROMOTED GENERATION BINDING
```

There is no universal minimum source-count quota. A source list is not a promoted pedagogy decision. Promoted claims require explicit support, relevant retained-source classification, contradiction handling and release-class-appropriate evidence custody.

Pedagogy evidence may improve representation, explanation, decomposition, misconception repair and transfer design. It cannot create curriculum scope, mathematical truth or Engineering authority.

### Current EASY materialization limitation — C0-F007

The governed policy and generation-spec validator permit fully bound optional EASY research. However, the current canonical SDU/LAU compiler path in `compile_sdu_lau_generation_spec.py` materializes research bindings only for non-EASY rows.

Therefore:

```text
OPTIONAL EASY RESEARCH POLICY / VALIDATION      = CURRENT + EXECUTABLE
OPTIONAL EASY RESEARCH AUTO-MATERIALIZATION
THROUGH THE CANONICAL SDU/LAU COMPILER          = CURRENT + DOCUMENTED ONLY
```

Until a separate compiler migration adds and falsifies that materialization path, this root must not describe optional EASY research as automatically compiler-executable.

## 13. LAU — Learner Adaptation Unit

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

No default or inferred pseudo-percentage is legal. Knowledge percentage is a support prior, not a mastery claim and not a replacement for `UNKNOWN / DEVELOPING / READY`.

LAU combines learner evidence with multi-dimensional task demand. Purpose remains independent from learner knowledge: knowledge answers how much support/how far demand may move; purpose answers why the product is being made.

## 14. TTU families and reconstruction

### Concept TTU

Used by Core1A/Core1B. Its centre of gravity is conceptual change, object/state model, equation meaning, representation, symbol bridge, derivation, contrast/misconception, validity boundary and verification.

### Problem TTU

Used by Core2A/Core2B. Its centre of gravity is recognition, model/method selection, constraints, representation choice, first non-obvious move, reasoning path, wrong route, verification and transfer.

A reconstructable TTU deliberately omits mathematically meaningful structure, not random words or numbers. Legal reconstruction may involve diagrams, graphs, equations, event/state lines, tables, proof/reasoning chains, representation maps, construction sequences or dependency models.

Fading within a lineage is normally monotone:

```text
MODELLED -> GUIDED -> FADED -> INDEPENDENT
```

A support reset in Core2 requires explicit LAU authority; Core1B cannot use learner percentage to reset SDU depth.

Field-level TTU and A/B interaction rules remain in `DUAL_TRACK_PRODUCT_MODEL.md` and the executable contracts.

## 15. Self-help closure and differentiation

Every substantive derivative TTU/episode must provide an eventual route to progressive authored help, canonical reveal, misconception/wrong-route support where relevant, independent verification and repair/next-step guidance.

Static answer availability is not learner evidence.

CDAU distinguishes legal semantic reuse and declared pedagogical transformation from near/pedagogical duplication. Immutable source stems, canonical definitions/formulas and answer identities may repeat only with explicit lineage; surrounding pedagogy must remain governed by the applicable core-purpose contract.

## 16. Product release boundary

Product release is not publication rendering. It first proves governed coverage, differentiation, learner fit, source/answer custody and current Engineering-domain custody.

All four derivative producer stages must carry matching current Engineering-domain custody. Final release revalidates current Engineering admission. Legacy unbound artifacts may be retained only as regression evidence and may not become publishable by renderer success alone.

The normative release rules remain in `PRODUCT_GOVERNANCE.md`.

## 17. Derived Engineering visibility

A released product may expose Engineering provenance and technical structure through a derived visibility manifest compiled from exact current bound authority.

The visibility layer is explicitly non-authoritative:

```text
authority = NON_AUTHORITATIVE_VIEW_OF_BOUND_ENGINEERING_AUTHORITY
technical_authorization = ALLOWED
publication_authorization = NOT_IMPLIED
```

It may explain existing gate title, role, depth, prerequisite closure, provenance, structure, verification obligations and misconception/repair information. It may not create gate membership, prerequisite closure, readiness, mathematical scope or publication permission.

## 18. Governed publication boundary

The current bound-release publication path is:

```text
PRODUCT RELEASE GATE = PASS
        ↓
revalidate / compile derived Engineering visibility
        ↓
compile semantic learner publication bundle
        ↓
validate exact research + governed-example + visibility custody
        ↓
render from bundle semantics only
        ↓
render-object / semantic-surface audit
        ↓
final learner PDF
```

The publication invariant is:

```text
semantic_source = LEARNER_PUBLICATION_BUNDLE_ONLY
```

`LearnerPageBlueprint` remains a repository/internal realization contract where used, but it is not the canonical final semantic source for the current governed bound-release renderer.

Publication may typeset governed semantics. It may not invent mathematics, omissions, learner actions, hints, examples, representations, verification logic, answer custody or filler content.

## 19. Learner evidence boundary

Learner attempts and performance evidence are post-delivery evidence. A static product cannot infer that a learner attempted, succeeded, failed, mastered or exhibited a misconception merely because an exercise, answer or corrective branch exists.

Observed learner evidence may govern later Core2A/Core2B calibration through the applicable evidence contracts. It does not retroactively alter Core1 mathematical depth or historical/source truth.

## 20. Implementation classification

This table records current architectural status. It is not a substitute for the executable contracts it references.

| Capability / boundary | Status |
|---|---|
| Non-authoritative Engineering discovery | CURRENT + EXECUTABLE |
| Explicit exact-ID selection into unchanged exact Engineering resolver | CURRENT + EXECUTABLE |
| Engineering registry composition, validation, depth and prerequisite closure | CURRENT + EXECUTABLE |
| Exact AssessmentScope → Engineering custody bridge | CURRENT + EXECUTABLE |
| Engineering authorization binding and canonical domain admission | CURRENT + EXECUTABLE |
| Core0 routing + independent Core1/Core2 cross-validation | CURRENT + EXECUTABLE |
| Canonical Engineering-derived asset identity + separate scope membership | CURRENT + EXECUTABLE |
| SDU intrinsic-difficulty governance | CURRENT + EXECUTABLE |
| LAU knowledge-percent-or-owner-waiver governance | CURRENT + EXECUTABLE |
| Claim-level pedagogy-research promotion | CURRENT + EXECUTABLE |
| Optional EASY research accepted when fully bound at generation-spec validation boundary | CURRENT + EXECUTABLE |
| Optional EASY research automatically materialized by canonical SDU/LAU compiler | CURRENT + DOCUMENTED ONLY — C0-F007 |
| Four-producer release/cross-core governance | CURRENT + EXECUTABLE |
| Derived Engineering visibility | CURRENT + EXECUTABLE |
| Semantic learner publication bundle + bundle-only renderer semantics | CURRENT + EXECUTABLE |
| Generated architecture-reference tables from a production Architecture Catalog | ROADMAP — Stage C3 |
| Generic cross-subject Subject Adapter interface | ROADMAP — Stage C4 |
| Subtopic Intelligence Library production contracts | ROADMAP — Stage C5+ |

A documented-only capability may not be described as executable until its governed migration, validator/falsifier coverage and release evidence exist.

## 21. Normative subordinate specifications

This root intentionally does not duplicate every schema field or policy rule. The principal subordinate normative documents are:

```text
ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md
ENGINEERING_WORKBENCH.md
ENGINEERING_DISCOVERY.md
MATHEMATICS_TECHNICAL_ENGINEERING_GATES.md
CANONICAL_ENGINEERING_DOMAIN_ASSETS.md
GENERATION_CALIBRATION.md
SELF_TEACHING.md
DUAL_TRACK_PRODUCT_MODEL.md
PRODUCT_GOVERNANCE.md
```

Executable authority is additionally carried by the governed contracts, policies, validators, compilers and release gates referenced by those specifications.

If a subordinate explanatory statement conflicts with a current executable contract, the executable contract governs until an explicit migration resolves the inconsistency. If an authority-semantic change is desired, it requires a governed migration; it is not achieved by editing prose alone.

## 22. Migration and extension rule

Architecture evolution must distinguish documentation consolidation from semantic/runtime change.

A semantic migration must identify:

```text
changed governed contract or policy
authority owner/domain
producer/compiler impact
validator impact
fail-closed falsifiers
custody/version effect
release-class effect
compatibility/deprecation effect
owner decision when authority semantics change
```

Topic growth must continue to occur through governed Engineering/domain data and exact scope membership, not topic-specific Blueprint branches.

## 23. Central doctrine

> Ground truth determines what was supplied, frozen, observed or explicitly scoped.
>
> Non-authoritative discovery may help locate candidate Engineering identities, but never authorizes mathematics.
>
> Engineering determines technical mathematical authority through exact identity, current validation, requested depth and prerequisite closure.
>
> Core1 determines semantic reconstruction **within already-authorized mathematical scope**.
>
> Core2 determines assessment/question-demand reconstruction and source-question custody **within already-authorized mathematical scope**.
>
> The Canonical Domain Registry stores canonical objects once and represents teaching use through separate memberships.
>
> CDAU keeps products differentiated, traceable and non-duplicative.
>
> SDU determines intrinsic Core1A/Core1B depth; LAU determines Core2A/Core2B learner fit and demand.
>
> Research discovery is permissive; claim-level promotion is evidence-custodied and cannot create mathematical authority.
>
> A represents the canonical completed state; B represents the canonical reconstruction experience.
>
> Derived Engineering visibility explains existing authority but never creates technical or publication authority.
>
> Governed publication consumes the released semantic learner publication bundle and renders it without inventing pedagogy or mathematics.
