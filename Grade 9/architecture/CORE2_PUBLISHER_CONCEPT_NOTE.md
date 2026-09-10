# Concept Note — Core (2) Publisher

**Status:** Draft / v1 hand-off frozen; Core (2) implementation contract  
**Scope:** Grades 9–11 learning-publication pipeline  
**Primary role:** Core (2) — learner adaptation, representation rendering, scaffolding, composition, learner-product generation and publication QA  
**Normative upstream contract:** PR #160, `Grade 9/Architecture/contracts/v1/`  
**Reference implementations:** Physics PR #155 and Chemistry PR #157 are mature implementation references, not normative schemas.

---

## 1. Architecture decision

Adopt two independent cores:

```text
USER PROMPT / SUPPLIED SOURCES
            │
            ▼
      INTAKE / ROUTER
            │
            ▼
       CORE (1) RESEARCH
 truth · scope · evidence · concepts
 representation semantics · exam demand
            │
            ▼
      FROZEN RESEARCH PACKAGE
            │
            ├──────── LearnerProfile
            └──────── PublicationTarget
                         │
                         ▼
                   CORE (2) PUBLISH
 learner adaptation · representations · scaffolding
 practice · appendices · composition · render QA
                         │
                         ▼
                  LEARNER PRODUCTS
```

The governing boundary is:

> **Core (1) owns what is true, in scope, evidenced and semantically required. Core (2) owns how the frozen material is transformed into a learner experience for a declared learner profile and purpose.**

Core (2) must be executable by a cold-start agent with no access to the Core (1) conversation or hidden researcher state.

---

## 2. Frozen Core (2) input formula

The v1 input is:

```text
CORE2 = ResearchPackage × LearnerProfile × PublicationTarget
```

where:

```text
ResearchPackage
  = ResearchBundle
  + ResearchBundleManifest
  + referenced SourceLedger
  + referenced ExamDemandProfile(s), when applicable
  + referenced QuestionEvidenceLedger, when applicable
  + approved assets, when applicable
```

`LearnerProfile` and `PublicationTarget` are downstream inputs. They are **not** part of `ResearchBundle` identity.

Therefore:

```text
change Bxx / learner profile       → rebuild Core (2)
change publication purpose         → rebuild Core (2)
change presentation profile        → rebuild/re-render Core (2)

change evidence / truth / scope    → version Core (1)
change supported exam demand       → version Core (1)
change approved source asset       → version/release Core (1) package
```

This is the operational meaning of:

> **Research once per evidence version → publish many.**

---

## 3. Normative v1 upstream objects

Core (2) consumes the schemas frozen in PR #160:

```text
ProjectManifest
ScopeGraph
LearnerProfile
PublicationTarget
ResearchClaim
RepresentationRequirement
SourceLedger
ExamDemandProfile
QuestionEvidenceLedger
ResearchBundle
ResearchBundleManifest
Core1ResearchGap
common ChangeClass / TraceabilityClass / rights / disposition enums
```

Core (2) must not define a parallel version of these v1 objects.

A breaking hand-off change requires a jointly reviewed `v2/` contract rather than a silent local extension.

---

## 4. Research Package identity and reproducibility

Core (2) binds to:

```text
research_bundle_id
research_package_digest
```

`research_package_digest` MUST equal:

```text
ResearchBundleManifest.package_digest
```

The package manifest also carries:

```text
evidence_version
change_class
semantic_digest
artifact hashes
material-view reconciliation
```

Core (2) must never treat one JSON-file hash as sufficient package identity when the research release includes separate ledgers, human views or assets.

Every Core (2) canonical publication model must record at minimum:

```text
publication_target_id
learner_profile_id
research_bundle_id
evidence_version
research_package_digest
core2_schema_version
```

A learner PDF without this machine lineage is not a reproducible Core (2) product.

---

## 5. Core (2) preflight is stricter than schema validity

Passing the cross-core schema/handoff validator is necessary but not sufficient for publication.

Before planning learner content, Core (2) requires:

```text
UPSTREAM_HANDOFF_SCHEMA_VALID = PASS
RESEARCH_BUNDLE_STATUS = READY_FOR_PUBLISH
RESEARCH_PACKAGE_DIGEST_BINDING = PASS
BUNDLE_MANIFEST_BINDING = PASS
LEARNER_TARGET_BINDING = PASS
MATERIAL_VIEW_RECONCILIATION = PASS
BLOCKING_RESEARCH_GAPS = 0
MATERIAL_RESEARCH_CLAIMS_VERIFIED = PASS
COMPETITIVE_EXAM_DEMAND_BINDING = PASS | NOT_APPLICABLE
QUESTION_DENOMINATOR_CLOSURE = PASS | NOT_APPLICABLE
```

### 5.1 Publisher verification rule

For v1, every Research Claim that enters a learner product as one of these material classes must be `VERIFIED`:

```text
MATERIAL_CLAIM
MATERIAL_CONDITION
MATERIAL_EXAMPLE
MATERIAL_REPRESENTATION
MATERIAL_QUESTION
MATERIAL_SOLUTION_METHOD
MATERIAL_EXAM_FACT
```

`PEDAGOGICAL_CONNECTIVE` and `PRESENTATION_ONLY` do not require artificial research-claim verification.

A `PARTIAL`, `UNVERIFIED` or `CONFLICT_REVIEW_REQUIRED` material claim must not be published as settled learner content.

---

## 6. Research embargo and fail-back

Core (2) is not a second researcher.

It may:

- simplify verified wording;
- reorganize verified material;
- choose learner sequencing;
- generate layout geometry;
- typeset an approved semantic equation;
- select a compliant renderer for a verified representation requirement;
- create pedagogical connective prose that introduces no new material claim;
- create original practice only from supported concepts/question families and within declared provenance rules.

It may not silently:

- add a scientific/mathematical claim;
- repair a missing condition;
- invent a missing diagram meaning;
- infer a new exam pattern;
- recreate missing options from general knowledge;
- reinterpret a source answer;
- promote a project research candidate into canonical knowledge.

If required material is missing, Core (2) returns the v1 object:

```text
CORE1_RESEARCH_GAP
```

with a gap type such as:

```text
SOURCE
CONCEPT
REPRESENTATION
EQUATION
QUESTION_FAMILY
EXAM_DEMAND
ASSET
RIGHTS_USE
OTHER
```

Core (1) resolves the gap and releases a new evidence version/package. Core (2) resumes only from that released package.

---

## 7. Scope and canonical knowledge boundary

Core (2) consumes project scope through `ScopeGraph` and canonical IDs.

It may not perform ontology promotion. The promotion path remains upstream:

```text
RESEARCH_CANDIDATE
→ SUBJECT_AUTHORITY_REVIEW
→ CANONICAL_PROMOTION_APPROVED
```

If Core (2) encounters a project candidate that is necessary to teach a required learner object but is not publication-ready, it must fail back rather than silently normalize it into the canonical graph.

---

## 8. LearnerProfile: Bxx is downstream adaptation state

`LearnerProfile` stores baseline by subtopic as a numeric value from 0–100, with basis and confidence.

Examples:

```text
Newton's laws            80
free-body diagrams       45
friction                 30
connected systems        25
```

The familiar labels `B30`, `B50`, `B80` are display shorthand for this downstream baseline state.

Baseline means:

> **estimated prior working knowledge for that subtopic**

It does not mean:

```text
intelligence
psychometric mastery
question difficulty
exam difficulty
transfer distance
```

Core (2) applies Bxx to:

- exposition density;
- prerequisite repair;
- number of explicit bridges;
- worked-example depth;
- representation support;
- hint availability;
- fading rate;
- timing of mixed transfer;
- recap compression.

Core (2) must preserve the recorded baseline basis and confidence. A user-declared B80 must not be presented as empirically measured mastery.

---

## 9. PublicationTarget: purpose is orthogonal to Bxx

`PublicationTarget` binds:

```text
research_bundle_id
research_package_digest
learner_profile_id
purpose
exam_profile_id, when required
curriculum_profile_id, when applicable
requested_products
publication_profile
```

Canonical v1 purpose types are:

```text
ROUTINE_STUDY
CONCEPT_CLARIFICATION
SCHOOL_EXAM
COMPETITIVE_FOUNDATION
COMPETITIVE_EXAM
MOCK_EXAM_PREPARATION
REVISION
```

The two core adaptation questions are therefore independent:

> **What does this learner already know?**  
> **What must this learner be able to do for this purpose?**

Do not collapse either into a generic `level` or `difficulty` field.

---

## 10. Core (2) mission

After preflight, Core (2) performs:

```text
P0  HAND-OFF + PUBLISHER PREFLIGHT
P1  LEARNER PROFILE INTERPRETATION
P2  PURPOSE / EXAM PROFILE INTERPRETATION
P3  CONTENT-DEPTH PLAN
P4  REPRESENTATION PLAN
P5  LEARNING-SEQUENCE PLAN
P6  PRACTICE / TRANSFER PLAN
P7  PUBLICATION MODEL
P8  REPRESENTATIVE PROTOTYPE
P9  PROTOTYPE RENDER + QA
P10 FULL BUILD
P11 MATERIAL / REPRESENTATION / QUESTION CLOSURE
P12 FINAL RENDER QA
P13 PUBLICATION PACKAGE CERTIFICATION
```

No full-book scale-up before the representative prototype passes the actual risk surface of the topic.

---

## 11. Core (2) canonical output models

The v1 upstream hand-off is frozen. The next Core (2) implementation should define downstream publication objects without changing upstream schemas.

Recommended Core (2)-owned models:

```text
PublicationPlan
StudyGuidePublicationModel
TransferBookPublicationModel
RepresentationInstance
Badge
PublicationAudit
PublicationManifest
```

### 11.1 PublicationPlan

Owns the learner transformation plan:

```text
publication_target_id
learner_profile_id
research_package_digest
subtopic adaptation decisions
sequence
page/template families
representation plan
practice plan
transfer plan
appendix plan
rights-use plan
prototype obligations
```

### 11.2 StudyGuidePublicationModel

Owns the full learner-facing Study Guide semantic content and layout-ready object tree.

### 11.3 TransferBookPublicationModel

Owns external/competitive attempt pages, supports, mixed-transfer sets, solutions and diagnosis.

### 11.4 RepresentationInstance

Binds one upstream `RepresentationRequirement` to one concrete rendering route and learner placement.

### 11.5 Badge

Owns learner-facing metadata presentation without redefining the underlying evidence.

### 11.6 PublicationAudit

Records semantic, representation, typography, links, bounds, answer-leakage and obligation-level results.

### 11.7 PublicationManifest

Binds the exact output model(s), rendered PDFs and audit artifacts by hash.

---

## 12. Study Guide product contract

Default learner product:

```text
MAIN LEARNING SECTION

Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

These names are frozen for the shared v1 publication semantics.

### Appendix A — Core Practice

Purpose:

- independent and faded practice;
- stable concept linkage;
- recognition, representation and reasoning coverage;
- no answer leakage;
- baseline-sensitive question mix.

### Appendix B — Core Solutions

Default solution grammar:

```text
QUESTION RECAP
REQUIRED REPRESENTATION, when needed
WHY THIS WORKS
METHOD
ANSWER / CHECK
CONCEPT TO KEEP
RESEARCH TRACE
```

A method is not an expanded answer key. It must explain the reusable route and decisive model/representation choice.

### Appendix C — Printable Handout

Appendix C is a printable, standalone learner reference.

`first_step_reference` is a **module/profile inside Appendix C**, not Appendix C's canonical identity.

Subject profiles may include:

```text
Mathematics
  first moves · invariants · decision router · conditions

Physics
  first moves · model cues · diagram cues · sign/frame checks · equation conditions

Chemistry
  process cues · macro/particle/symbolic bridges · conditions · common traps
```

Appendix C must not become a compressed answer sheet.

---

## 13. Optional Transfer Book contract

A Transfer Book is appropriate for competitive/external/PYQ-style practice when requested by `PublicationTarget`.

Use bounded learning sets rather than treating total page count as learner progress.

### 13.1 Assimilation mode

Before attempt, a question may expose:

```text
SOURCE / EXAM
DIFFICULTY
TRANSFER
PRIMARY CONCEPT
SUPPORTS
```

Student eye path:

```text
QUESTION
→ WORK HERE
→ STOP / OPTIONAL HELP BOUNDARY
→ H1 NOTICE
→ H2 MODEL / STRUCTURE
→ H3 START
```

### 13.2 Mixed-transfer mode

Before attempt:

```text
CONCEPT · IDENTIFY FIRST
```

Hide the actual primary concept/method family. Reveal them during diagnosis/solution.

### 13.3 External-question denominator

Core (2) consumes the frozen `QuestionEvidenceLedger`; it does not re-own corpus accounting.

Dispositions are:

```text
REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
```

`REVIEW` is blocking. Core (2) publishes only records authorized for the requested publication target and preserves source/transcription/answer/ownership state.

---

## 14. Baseline-sensitive publishing profiles

The learner baseline changes the amount of teaching, not the underlying truth.

### Low prior knowledge — approximately B0–B30

```text
FAMILIAR SITUATION
→ PICTURE / MODEL
→ WHAT TO NOTICE
→ ORDINARY LANGUAGE
→ SUBJECT MEANING
→ EQUATION / SYMBOLIC FORM
→ WHY EACH TERM / STEP EXISTS
→ WORKED MODEL
→ GUIDED TRY
→ FADED TRY
→ INDEPENDENT TRY
```

### Partial working knowledge — approximately B31–B60

```text
RECONNECT
→ EXPOSE MISSING BRIDGE
→ MODEL / REPRESENTATION
→ CONTRAST WRONG MODEL
→ GUIDED FIRST MOVE
→ FADE SUPPORT
→ INDEPENDENT APPLICATION
```

### Strong prior knowledge — approximately B61–B85

```text
QUICK RECALL
→ DECISION BOUNDARY
→ HIGH-VALUE CONTRAST
→ MODEL / CONDITION
→ NON-ROUTINE APPLICATION
→ TRANSFER
```

### Very strong prior knowledge — approximately B86–B100

```text
REFERENCE RECAP
→ CONDITIONS / EXCEPTIONS
→ METHOD SELECTION
→ REPRESENTATION SHIFT
→ MIXED / FAR TRANSFER
```

One learner publication may legitimately contain different support densities by subtopic.

---

## 15. Purpose-sensitive publishing

For the same baseline:

### Routine study

Emphasize continuity, worked examples, retrieval and coherent topic synthesis.

### Concept clarification

Emphasize missing bridges, competing models, misconceptions, representation switching and small diagnostic probes.

### School exam

Emphasize syllabus-aligned response forms, standard application, marking-relevant completeness and revision.

### Competitive foundation / competitive exam

Emphasize recognition under disguised wording, method selection, representation shifts, multi-concept combinations, distractor analysis and mixed transfer consistent with the frozen ExamDemand profile.

### Mock exam preparation

Use an upstream evidence-backed exam blueprint. Core (2) formats and publishes the mock; it does not invent the exam contract.

### Revision

Compress exposition into retrieval, conditions, first moves, misconception checks and mixed practice.

---

## 16. Baseline, difficulty and transfer are separate

A Core (2) question may have all three:

```yaml
learner_baseline: 30

difficulty:
  normalized_band: D3
  learner_label: HARD
  basis: SOURCE_MAPPING

transfer:
  type: REPRESENTATION_SHIFT
```

- baseline = learner prior working knowledge;
- difficulty = task demand;
- transfer = distance from familiar form/context/representation.

A direct question can be difficult. A far-transfer question can be computationally simple.

---

## 17. Badge system belongs to Core (2)

Badges are publication components, not research facts.

Typed badge families may include:

```text
SOURCE
EXAM
YEAR / SHIFT
DIFFICULTY
TRANSFER
TASK
STATUS
```

A badge object should carry at least:

```text
badge_type
machine_value
learner_label
visual_token
priority
student_visible
grayscale_fallback
```

Rules:

- words are mandatory; color is secondary;
- grayscale must preserve meaning;
- source-owned values must retain provenance;
- editorial difficulty labels must state their basis;
- do not turn all metadata into equal visual pills;
- `PRIMARY` concept vs supporting concepts should normally use semantic hierarchy, not merely color.

---

## 18. Shared Representation Layer

The cross-subject rendering subsystem is named:

> **Shared Representation Layer**

Core (1) owns the semantic requirement:

```text
what must be shown
relationships
required labels
conditions
approved assets
research refs
```

Core (2) owns:

```text
renderer selection
geometry
layout
asset placement
legibility
grayscale behavior
render QA
```

A required unsupported representation fails closed rather than degrading into a decorative approximation.

---

## 19. Representation routes

Core (2) must support three legitimate production routes:

```text
1. STRUCTURED SEMANTIC DATA
   → generated vector representation

2. APPROVED SVG / VECTOR / TRUSTED ASSET
   → placed learner representation

3. SOURCE IMAGE / CROP
   → fidelity-controlled learner representation
```

Do not force every laboratory apparatus, molecular structure, source option figure or historical diagram into a procedural drawing API.

All three routes must pass the same:

```text
research linkage
rights/use check
required-label check
bounds check
legibility check
print/grayscale check
student/solution dependency check
```

---

## 20. Representation families to support at platform level

The layer should be extensible across Mathematics, Physics and Chemistry rather than hard-coded per chapter.

Target families include:

```text
GENERIC XY GRAPH
NUMBER LINE / TIMELINE
GEOMETRIC / CONSTRUCTION DIAGRAM
VECTOR / FORCE DIAGRAM
PATH / TRAJECTORY DIAGRAM
RAY DIAGRAM
CIRCUIT DIAGRAM
WAVE DIAGRAM
FIELD DIAGRAM
APPARATUS / PROCESS DIAGRAM
PARTICLE DIAGRAM
ATOMIC / SHELL DIAGRAM
LEWIS / BONDING DIAGRAM
MOLECULAR STRUCTURE
ENERGY-LEVEL / ORBITAL DIAGRAM
REACTION / MECHANISM SCHEME
TABLE / GRID
PROOF / CASE / DEPENDENCY STRUCTURE
EQUATION
CHEMICAL EQUATION
TRUSTED VECTOR ASSET
SOURCE CROP
```

Implementation support should be explicit. A semantic `representation_type` existing upstream does not imply that Core (2) can render it.

---

## 21. General graph primitive

Do not create separate renderers for `vt`, `xt`, `pv`, `stress_strain`, `concentration_time`, etc.

A generic graph primitive should support, as needed:

- arbitrary x/y variables and units;
- multiple series;
- points, segments and smooth curves;
- scientific notation;
- zero/reference lines;
- legends;
- annotations;
- shaded regions;
- error bars;
- discontinuities/asymptotes;
- linear/log scales where supported;
- grayscale-safe series differentiation.

Graph semantics and required values remain traceable to Core (1). Core (2) controls visual grammar.

---

## 22. Equations and chemistry notation are semantic objects

Core (2) should not reduce equations to arbitrary body-text strings.

Upstream semantic objects provide meaning, conditions and research refs. Core (2) adds publication representation such as:

```text
display source
inline/display mode
line breaking
alignment
vector/scalar typography
unit styling
chemical charge/state styling
accessibility text
```

A specialist math/chemistry typesetter may generate vector output while the publication model retains the upstream semantic expression and IDs.

Core (2) must never infer missing index/exponent/charge semantics from typography alone.

---

## 23. Material traceability

Core (2) requires 100% research linkage for material semantic objects:

```text
MATERIAL_CLAIM
MATERIAL_CONDITION
MATERIAL_EXAMPLE
MATERIAL_REPRESENTATION
MATERIAL_QUESTION
MATERIAL_SOLUTION_METHOD
MATERIAL_EXAM_FACT
```

The trace is:

```text
SOURCE / QUESTION OCCURRENCE
        ↓
CORE (1) RESEARCH CLAIM / CONCEPT / REPRESENTATION
        ↓
CORE (2) SECTION / FIGURE / QUESTION / SOLUTION
```

Pedagogical connective prose and presentation-only objects do not require artificial research claim IDs.

Student-facing citation density is a design decision; machine traceability is mandatory.

---

## 24. Rights/use enforcement

Evidence validity does not imply reproduction permission.

Core (2) consumes upstream rights states:

```text
REPRODUCTION_ALLOWED
REFERENCE_ONLY
USER_SUPPLIED_LIMITED
DISCOVERY_ONLY
UNKNOWN_REVIEW_REQUIRED
```

The publication plan must record every direct source/asset reproduction use.

Rules:

- `REPRODUCTION_ALLOWED`: may reproduce within recorded conditions;
- `REFERENCE_ONLY`: may support research/traceability but not learner-facing verbatim/asset reproduction unless another permission applies;
- `USER_SUPPLIED_LIMITED`: obey recorded allowed/prohibited uses;
- `DISCOVERY_ONLY`: no learner-facing reproduction;
- `UNKNOWN_REVIEW_REQUIRED`: block reproduction pending resolution.

Core (2) may still express independently verified factual structure in original wording when permitted by the research/rights contract; it must not copy restricted source content merely because the source was useful evidence.

---

## 25. Original-question provenance

Do not use `ORIGINAL_CALIBRATED` by default.

Use:

```text
ORIGINAL_EXAM_ALIGNED
ORIGINAL_EDITORIAL_PROFILED
```

unless an explicit calibration basis exists:

```text
SOURCE_MAPPING
EXPERT_REVIEW
EMPIRICAL
```

Core (2) may create original practice from supported concepts/question families, but it must retain provenance and must not falsely imply it is a past-paper question.

---

## 26. Change-class aware invalidation

Core (2) recognizes upstream release changes:

```text
EDITORIAL
EVIDENCE
SEMANTIC
SCOPE
EXAM_DEMAND
ASSET
```

Default impact:

```text
EDITORIAL
  → metadata/view revalidation

EVIDENCE
  → provenance/traceability revalidation

ASSET
  → affected representation rerender/revalidation

SEMANTIC
  → rebuild affected learner objects and dependent practice/solutions

SCOPE
  → scope reconciliation; broad/full rebuild by default

EXAM_DEMAND
  → rebuild/revalidate competitive products and mock blueprints
```

If impact cannot be localized safely, fail closed and rebuild more broadly.

---

## 27. Representative prototype gate

Before full scale, prototype the actual risk surface.

Where applicable include:

- low-baseline explanatory page;
- high-baseline compressed page;
- equation-heavy page;
- general graph page;
- non-graph diagram page;
- source-crop/trusted-vector page;
- ordinary practice page;
- graph/diagram-heavy question page;
- H1/H2/H3 page;
- full assimilating solution;
- Appendix C sample;
- mixed-transfer page with concept hidden;
- badge-dense external-question page.

If a required representation family cannot pass the prototype, stop before topic-scale generation.

---

## 28. Page-density and student-eye-path contract

Core (2) owns pedagogically appropriate density, not fixed question counts per page.

Default question-bank density guidance:

```text
D1: 2–3 short questions/page when safe
D2: usually 2/page
D3: 1–2/page
D4/D5 or graph/diagram heavy: generous half/full page
```

Attempt pages should normally follow:

```text
QUESTION
→ WORK / REPRESENTATION AREA
→ STOP / OPTIONAL HELP BOUNDARY
→ H1 NOTICE
→ H2 MODEL / STRUCTURE
→ H3 START
→ METHOD-CHECK LINK
```

Hints belong below the work area unless a subject/profile explicitly requires another interaction.

---

## 29. Representation dependency closure

For every question with a non-`NONE` representation dependency require:

```text
representation present on attempt page
critical labels/data preserved
representation legible at learner size
representation present again in standalone solution when needed
```

A solution recap such as “from the graph” without the graph fails.

Option figures, statement sets and answer choices are learner obligations. Never ask the learner to choose an invisible option.

---

## 30. Solution assimilation contract

Default Core (2) solution structure:

```text
QUESTION RECAP
REQUIRED REPRESENTATION / OPTIONS
WHY THIS WORKS
METHOD
ANSWER / CHECK
CONCEPT TO KEEP
RETURN / REPAIR LINK
```

Blocking failures include:

- method identical/near-identical to answer;
- formula-only method with no model reason;
- decisive representation/model choice omitted;
- final substitution presented as the entire route;
- generic boilerplate copied across different reasoning families;
- missing required graph/table/options;
- answer without units/sign/semantic option meaning where required.

The answer is the destination. The method teaches the route.

---

## 31. Core (2) publication QA

Certification is obligation-level, not “PDF opened successfully”.

Minimum gates:

```text
CORE2_PREFLIGHT = PASS
RESEARCH_PACKAGE_DIGEST_BINDING = PASS
MATERIAL_TRACEABILITY_COVERAGE = 100%
UNSUPPORTED_NEW_MATERIAL_CLAIMS = 0
REQUIRED_REPRESENTATIONS_PRESENT = PASS
REQUIRED_REPRESENTATIONS_LEGIBLE = PASS
REPRESENTATION_BOUNDS_FAILURES = 0
QUESTION_DENOMINATOR_RECONCILED = PASS | NOT_APPLICABLE
SOLUTION_DENOMINATOR_RECONCILED = PASS
HINT_PROGRESSION_FAILURES = 0
METHOD_ASSIMILATION_FAILURES = 0
BADGE_MAPPING_FAILURES = 0
RIGHTS_USE_VIOLATIONS = 0
BROKEN_INTERNAL_LINKS = 0
BROKEN_SOURCE_LINKS = 0
MATH_SCIENCE_TYPOGRAPHY_FAILURES = 0
TEXT_OVERLAP_OR_CLIPPING = 0
ANSWER_LEAKAGE_FAILURES = 0
GRAYSCALE_INFORMATION_LOSS = 0
PUBLICATION_ARTIFACT_HASHES_BOUND = PASS
```

Independent subject review, pedagogy review, classroom effectiveness and psychometric calibration remain separate states.

---

## 32. Core (2) output package

A complete Core (2) release should contain, at minimum:

```text
PublicationTarget.json
LearnerProfile reference / resolved learner projection
PublicationPlan.json
Study_Guide.publication.json
<Topic>_<Profile>_Study_Guide.pdf
PublicationAudit.json
PublicationManifest.json
```

When requested:

```text
Transfer_Book.publication.json
<Topic>_<Profile>_Transfer_Book.pdf
```

Recommended review artifacts include:

```text
representative page renders/contact sheet
representation inventory
link audit
font/typography audit
question/solution reconciliation
rights-use reconciliation
research-to-publication trace map
```

---

## 33. Cold-start acceptance test

A clean Core (2) agent receives only:

```text
ResearchBundle
ResearchBundleManifest
referenced Source / ExamDemand / QuestionEvidence artifacts
approved assets
LearnerProfile
PublicationTarget
canonical schemas/skills
```

No prior chat, browser history or researcher scratchpad is available.

The agent must determine:

1. exact project scope;
2. released evidence version/package identity;
3. learner baseline by subtopic;
4. publication purpose and requested products;
5. verified material claims and conditions;
6. required representations and approved assets;
7. supported exam demand, when applicable;
8. question denominator and authorized publication rows, when applicable;
9. source rights relevant to reproduction;
10. any blocking gap;
11. what may be adapted versus what must remain semantically fixed.

Required result:

```text
CORE2_COLD_START_SUFFICIENT = PASS
UNDECLARED_CORE2_RESEARCH = 0
```

---

## 34. Falsifier pilots

Do not validate Core (2) only with Motion/Redox-like pages.

### Pilot A — Physics Laws of Motion / competitive

Must exercise:

```text
mixed Bxx
free-body/vector diagrams
friction/connected-system representations
competitive ExamDemand binding
external or original exam-aligned practice
mixed transfer
```

### Pilot B — Chemistry Redox / routine study

Must exercise:

```text
mixed Bxx
macro/particle/symbolic links
chemical notation
before/after/process representations
Appendix C printable handout
routine-study purpose without unnecessary competitive crawl
```

### Representation golden fixtures before broad scale

Physics/Math/Chemistry coverage should include representative examples of:

```text
generic scientific graph
force/vector diagram
geometry/construction diagram
ray/circuit/wave or field diagram
apparatus/process diagram
particle/atomic/bonding representation
molecular/energy-level representation
reaction scheme
complex equation/chemical equation
trusted vector asset/source crop
```

The goal is to falsify the assumption that one topic renderer can scale to all Grades 9–11 content.

---

## 35. Relationship to PR #155 Physics

Mine PR #155 for mature behavior:

- schema-before-render;
- data-driven figures;
- fail-closed unsupported representations;
- stable links/destinations;
- representation-dependent solution duplication;
- H1/H2/H3 support;
- mixed-transfer concept hiding;
- difficulty badges with explicit basis;
- deterministic pagination planning;
- artifact-bound render QA.

Do **not** promote the Motion-specific figure dispatcher into the universal renderer.

---

## 36. Relationship to PR #157 Chemistry

Mine PR #157 for mature behavior:

- exactly paired learner products where transfer work is in scope;
- Core Study Guide Appendix A/B/C discipline;
- concept segregation;
- source/difficulty/transfer support metadata;
- exact artifact custody;
- fail-closed package states;
- chapter-agnostic publication review.

Do **not** make Redox-specific representations or terminology the generic Chemistry renderer.

---

## 37. Existing source-PDF reconstruction remains separate

Core (2) does not supersede the existing source-PDF reconstruction workflow where an existing PDF/book itself is the immutable publication authority.

Routing distinction:

```text
validated ResearchPackage → new learner publication
  = Core (2)

existing source PDF/book → reconstruct/preserve source obligations
  = grade9-publication source-reconstruction route
```

The two routes may share representation, typography, link and render-QA components, but they do not share the same input authority.

---

## 38. Implementation sequence

### Phase 1 — frozen hand-off consumption

- keep PR #160 v1 schemas normative;
- add Core (2) publisher preflight;
- bind PublicationTarget to manifest + LearnerProfile;
- make failures fail closed.

### Phase 2 — Core (2) output schemas

Define downstream-only schemas for:

```text
PublicationPlan
StudyGuidePublicationModel
TransferBookPublicationModel
RepresentationInstance
Badge
PublicationAudit
PublicationManifest
```

Do not alter upstream v1 objects to fit renderer convenience.

### Phase 3 — Shared Representation Layer

Extract generic graph/geometry/annotation/equation/asset primitives from mature pilots and add renderer capability registry + golden fixtures.

### Phase 4 — cold-start replays

Run Laws of Motion and Redox from frozen Core (1) packages with no chat history.

### Phase 5 — subject stress

Add Math/proof, broader Physics diagrams and broader Chemistry representations before topic multiplication.

### Phase 6 — compatibility migration

Only after replay succeeds, map existing Physics/Chemistry/Math builders and publication skills into Core (2) profiles without breaking stable IDs.

---

## 39. Approval / implementation invariants

Core (2) is ready to implement only if these remain true:

```text
ResearchBundle is learner-neutral
Bxx lives in LearnerProfile
purpose/products live in PublicationTarget
Core (2) binds to ResearchBundleManifest.package_digest
Core (2) requires READY_FOR_PUBLISH
material learner claims are verified and traceable
Core (2) does not silently research
rights/use is enforced at publication
Appendix A = Core Practice
Appendix B = Core Solutions
Appendix C = Printable Handout
first_step_reference is an Appendix C module
Shared Representation Layer owns geometry/rendering, not semantic truth
question denominator remains upstream-owned
breaking hand-off changes require v2
cold-start replay is the decisive acceptance test
```

---

## 40. Central invariant

> **Core (1) owns truth, scope, evidence, canonical references, representation semantics and supported assessment demand. Core (2) binds to that released package, applies a separate LearnerProfile and PublicationTarget, and owns learner adaptation, scaffolding, representations, practice organization, composition, rendering and publication QA. Core (2) may transform presentation aggressively, but it may never silently create or change material truth.**

Operationally:

```text
ONE FROZEN RESEARCH PACKAGE
          │
          ├── B30 routine-study publication
          ├── B80 routine-study publication
          ├── B50 concept-repair publication
          ├── competitive Study Guide
          └── competitive Transfer Book
```

That is the reusable Core (2) publishing architecture for Grades 9–11.