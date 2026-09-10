# Concept Note — Core (2) Publisher

**Status:** Draft for architecture approval  
**Scope:** Grade 9–11 learning-publication pipeline  
**Primary role:** Core (2) — learner adaptation, scientific representation, composition, rendering and publication QA  
**Depends on:** a completed, versioned Core (1) Research Package  
**Related pilots:** Physics PR #155 and Chemistry PR #157 are reference implementations, not normative dependencies of this note.

---

## 1. Decision summary

Adopt a two-core production architecture for every substantial study-material request:

```text
USER PROMPT
   ↓
INTAKE / ROUTER
   ↓
CORE (1) · RESEARCH
truth · scope · evidence · concept structure · exam-demand analysis
   ↓
VERSIONED RESEARCH PACKAGE
   ↓
CORE (2) · PUBLISH
learner adaptation · representations · scaffolding · page composition · QA
   ↓
LEARNER PUBLICATION
```

The governing separation is:

> **Core (1) decides what must be taught, what is supported by evidence, and what the target assessment demands. Core (2) decides how that verified material should be experienced by this learner for this purpose.**

Core (2) must be executable by an independent cold-start agent once Core (1) has passed its hand-off gate. Core (2) must not depend on the prior chat, the original researcher agent, or undocumented research decisions.

---

## 2. Why two cores

The current Grade 9 repository already contains strong but partially overlapping concerns: source grounding, subject reasoning, concept architecture, question generation, enrichment, publication, subtopic builders and corpus audits. Physics PR #155 demonstrates an executable publication model with typed figures, mixed-transfer behavior, hints, solutions and render QA. Chemistry PR #157 demonstrates a subject-wide two-file publication contract, Appendix A/B/C discipline, concept segregation, corpus support and artifact custody.

The next scaling risk is not lack of functionality. It is loss of responsibility boundaries when these patterns are multiplied across topics.

Without a hard two-core boundary, a publishing agent can accidentally:

- research new claims while laying out pages;
- repair gaps from general knowledge without recording provenance;
- reinterpret exam demand during question selection;
- mix learner baseline with question difficulty;
- create topic-specific renderers instead of reusable scientific representation primitives;
- produce a visually polished artifact that cannot be traced back to the verified research state.

The two-core architecture prevents these failures by making the research-to-publication boundary explicit and machine-checkable.

---

## 3. Non-goals

This proposal does **not**:

- merge research and publication into one large skill;
- replace subject authorities such as Physics or Chemistry;
- require one global learner baseline for a whole topic;
- treat B30/B80 as psychometric mastery measurements;
- require all projects to include an external competitive-exam corpus;
- force a single page orientation or decorative design;
- require Core (2) to browse the web to complete missing science;
- assume every figure must be generated programmatically;
- supersede the existing source-reconstruction publication skill where an existing PDF itself is the immutable source authority.

---

## 4. Intake / router contract

Before either core starts, the router resolves four dimensions:

```text
SUBJECT + GRADE
TOPIC / SUBTOPICS
LEARNER BASELINE BY SUBTOPIC
PURPOSE / TARGET ASSESSMENT
```

The router asks only for information not already supplied.

### Example

Prompt:

> Prepare study material for Grade 9 Physics, Laws of Motion for NSO.

Already known:

```text
grade = 9
subject = Physics
topic = Laws of Motion
purpose = competitive exam
exam_target = NSO
```

The router should not ask these again. It should search the repository first, infer candidate subtopics from existing authority where possible, then ask for unresolved scope and learner baseline, for example:

> Please confirm the Laws of Motion subtopics and learner baseline. You can use B30/B50/B80 per subtopic, e.g. Newton's laws B80, free-body diagrams B50, friction B30.

For a generic request such as:

> Prepare Grade 10 Chemistry study material on Redox.

The router should ask only for missing subtopics, baseline and purpose.

---

## 5. Learner baseline model

Baseline belongs to the learner/topic relationship, not to the publication as a single global label.

Store baseline per subtopic:

```yaml
baseline_profile:
  newtons_laws:
    band: B80
    basis: USER_DECLARED
  free_body_diagrams:
    band: B50
    basis: USER_DECLARED
  friction:
    band: B30
    basis: USER_DECLARED
```

### B-band semantics

B-bands are **instructional support profiles**, not mastery scores.

```text
B20–B30  LOW PRIOR WORKING KNOWLEDGE
         build almost from first principles

B40–B60  PARTIAL KNOWLEDGE
         reconnect, diagnose, model and repair

B70–B80  STRONG PRIOR KNOWLEDGE
         compress routine basics; emphasize distinctions and application

B90+     VERY STRONG PRIOR KNOWLEDGE
         reference-first, transfer-heavy, minimal exposition
```

Every baseline value records its basis:

```text
USER_DECLARED
DIAGNOSTIC_DERIVED
TEACHER_DECLARED
EVIDENCE_ESTIMATED
```

Do not present a user-entered B80 as empirically measured mastery.

---

## 6. Purpose is independent of baseline

The same B80 learner may need very different publications for routine study and a competitive exam.

Canonical purpose profiles should include at least:

```text
ROUTINE_STUDY
CONCEPT_CLARIFICATION
SCHOOL_EXAM
COMPETITIVE_FOUNDATION
COMPETITIVE_EXAM
MOCK_EXAM_PREPARATION
REVISION
```

Purpose may carry an assessment target:

```yaml
purpose:
  type: COMPETITIVE_EXAM
  target:
    name: NSO
    level: Grade 9
```

Core (2) therefore receives two independent adaptation axes:

> **How much does the learner already know?**  
> **What must the learner be able to do?**

Do not collapse either axis into a single difficulty field.

---

## 7. Repository-first discovery

Before Core (1) performs new research, the workflow must search the repository for reusable evidence and artifacts:

- topic/chapter authority documents;
- source maps and source-obligation ledgers;
- concept maps and stable IDs;
- prior study material;
- question banks and external-corpus ledgers;
- previous exam-demand profiles;
- approved figures, diagrams and visual assets;
- prior publication models;
- prior audits and review notes.

The search result becomes part of the project manifest so that future agents can see what was reused versus newly researched.

External research fills demonstrated gaps; it does not replace existing repository authority silently.

---

## 8. Competitive-exam research behavior belongs to Core (1)

When the purpose is competitive, Core (1) should reverse-engineer the target demand from representative questions supplied by the user, available in the repository, or found from appropriate public sources.

The purpose is not to imitate questions. It is to extract the assessment demand:

```text
representative questions
  ↓
reasoning mechanisms
  ↓
representation demands
  ↓
prerequisite combinations
  ↓
common distractors / failure models
  ↓
transfer depth
  ↓
EXAM DEMAND PROFILE
```

Typical output:

```yaml
exam_demand_profile:
  target: NSO Grade 9
  dominant_demands:
    - identify interacting bodies
    - distinguish action-reaction pairs
    - choose the correct free-body diagram
    - combine F=ma with friction
  common_representations:
    - force diagrams
    - blocks
    - pulleys
    - option figures
  common_distractors:
    - action-reaction pair placed on one body
    - friction always equals muN
    - normal force always equals mg
  transfer_depth:
    typical: MULTI_STEP
```

Core (2) consumes this object; it does not independently reverse-engineer the exam again.

---

## 9. Core (1) required outputs

Markdown alone is not an adequate hand-off.

Core (1) should produce at least:

```text
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Research_Bundle.json
<Topic>_Source_Ledger.json
```

For competitive work also produce:

```text
<Topic>_Exam_Demand_Profile.json
<Topic>_Question_Evidence_Ledger.json
```

Optional approved assets live under a stable asset directory.

The JSON bundle is the canonical machine hand-off. The MD/PDF are human-review surfaces.

---

## 10. Research Bundle contract

The Research Bundle is the immutable interface between Core (1) and Core (2).

Minimum conceptual shape:

```yaml
research_bundle_version: 1.0
research_bundle_id: G9-PHY-NLM-NSO-001

project:
  grade: 9
  subject: Physics
  topic: Laws of Motion

purpose:
  type: COMPETITIVE_EXAM
  target: NSO

scope:
  included_subtopics: []
  excluded_subtopics: []

baseline_profile: {}

concepts: []
prerequisites: []
misconceptions: []
representations_required: []
equations: []
worked_reasoning: []
research_claims: []
source_registry: []
assets: []

exam_demand_profile: null

unresolved_items: []
```

Core (2) must not begin final publication if a blocking `unresolved_item` affects a required learner claim, representation or answer.

---

## 11. Stable research claims and traceability

Every Core (1) statement that can materially affect Core (2) should have a stable research claim ID.

Example:

```yaml
claim_id: R-PHY-NLM-014
concept_id: PHY-NLM-FBD-01
claim: A free-body diagram contains only forces acting on the selected body.
sources:
  - SRC-NCERT-11-042
  - SRC-NSO-2024-Q18
```

Core (2) may simplify language for the learner, but its publication model records:

```yaml
research_refs:
  - R-PHY-NLM-014
```

The trace becomes:

```text
SOURCE
  ↓
CORE (1) RESEARCH CLAIM
  ↓
CORE (2) LEARNER EXPLANATION
```

This is the required citation lineage. Core (2) should never become the hidden origin of scientific claims.

---

## 12. Core (2) mission

Core (2) receives:

```text
Research Bundle
+ learner baseline profile
+ purpose / exam-demand profile
+ publication specification
```

and performs:

```text
SELECT DEPTH
→ SELECT REPRESENTATIONS
→ ADAPT LANGUAGE
→ ORDER LEARNING
→ ADD SCAFFOLDING
→ BUILD / PLACE PRACTICE
→ APPLY BADGES
→ BUILD APPENDICES
→ LINK TO CORE (1)
→ RENDER
→ AUDIT
```

Core (2) owns learner experience, not scientific truth discovery.

---

## 13. Core (2) research embargo

Core (2) must not silently browse or use general knowledge to fill missing research.

If publication encounters a missing requirement such as:

```text
"show the molecular geometry"
```

but the Research Bundle contains no verified geometry or approved asset, Core (2) returns:

```text
CORE1_RESEARCH_GAP
```

If further research is authorized, control returns to Core (1). Core (1) updates and versions the Research Bundle, then Core (2) resumes from the new version.

Exception: non-semantic production work such as checking font support or converting an already approved equation to vector form may remain within Core (2).

---

## 14. Versioned hand-off

Every Core (2) publication model records:

```yaml
research_bundle_id: G9-PHY-NLM-NSO-001
research_bundle_version: 1.3
research_bundle_sha256: <hash>
```

If the bundle changes from `1.3` to `1.4`, the learner publication becomes stale until revalidated.

This makes the Research Package a real build dependency rather than a loose citation.

---

## 15. Core (2) input contract

Canonical input should resemble:

```yaml
publication_request:
  research_bundle:
    path: Laws_of_Motion_NSO_Research_Bundle.json

  learner:
    grade: 9
    baseline_profile:
      default: B50
      overrides:
        friction: B30
        free_body_diagrams: B80

  purpose:
    type: COMPETITIVE_EXAM
    exam_target: NSO

  requested_products:
    study_guide: true
    transfer_book: true

  publication_profile:
    orientation: AUTO
    color_mode: COLOR_AND_GRAYSCALE_SAFE
    answer_separation: true
```

If this object is complete, Core (2) proceeds without asking the user again.

---

## 16. Complete project output contract

A full project produces two separate cores plus learner artifacts.

### Core (1) Research product

```text
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Research_Bundle.json
```

### Core (2) publication products

At minimum:

```text
<Topic>_<BaselineProfile>_<Purpose>_Study_Guide.pdf
<Topic>_Study_Guide.publication.json
```

When transfer/exam practice is in scope:

```text
<Topic>_<BaselineProfile>_<Exam>_Transfer_Book.pdf
<Topic>_Transfer_Book.publication.json
```

Core (1) and Core (2) are separate reviewable products. The learner-facing PDFs are Core (2) outputs.

---

## 17. Core (2) Study Guide contract

Default learner structure:

```text
MAIN LEARNING SECTION

Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — First-Step Reference / Printable Handout
```

The appendix semantics should remain stable across Physics and Chemistry, while subject-specific content and representation needs vary.

### Appendix A — Core Practice

- independent and faded practice;
- stable concept linkage;
- sufficient variety to test recognition, representation and reasoning;
- no answer leakage from Appendix B.

### Appendix B — Core Solutions

Default structure:

```text
QUESTION RECAP
REQUIRED REPRESENTATION
WHY THIS WORKS
METHOD
ANSWER / CHECK
CONCEPT TO KEEP
RESEARCH LINK
```

### Appendix C — First-Step Reference / Printable Handout

Function:

```text
SEE THIS
→ THINK THIS
→ START HERE
```

It should be detachable, concise, standalone-usable, source-bounded and free of independent-practice answer leakage.

---

## 18. Baseline-sensitive publishing

Core (2) does not merely change the label B30/B80. It changes instructional density, prerequisite repair, worked-example depth and transfer mix.

### B30-style treatment

```text
FAMILIAR SITUATION
↓
PICTURE / MODEL
↓
WHAT TO NOTICE
↓
ORDINARY LANGUAGE
↓
SUBJECT MEANING
↓
EQUATION / SYMBOLIC FORM
↓
WHY EACH TERM EXISTS
↓
WORKED EXAMPLE
↓
GUIDED TRY
↓
FADED TRY
↓
INDEPENDENT TRY
```

### B80-style treatment

```text
QUICK RECALL
↓
DECISION BOUNDARY
↓
HIGH-VALUE CONTRAST
↓
MODEL / EQUATION
↓
NON-ROUTINE APPLICATION
↓
TRANSFER
```

Mixed baseline inside one topic is expected. One learner book may contain compressed B80 sections and more extensive B30 sections without splitting into multiple books.

---

## 19. Purpose-sensitive publishing

Baseline and purpose are orthogonal.

### Routine study

Prefer explanatory continuity, examples, retrieval and synthesis.

### Concept clarification

Prefer contrasts, misconception diagnosis, visual explanation and small conceptual probes.

### Competitive exam

Prefer disguised recognition, multi-concept combinations, option analysis, representation shifts, mixed transfer and exam-demand alignment.

### ExamSIDE-type transfer

Prefer source-linked question records, primary concept ownership, difficulty/transfer metadata, H0 attempt-first support, H1/H2/H3 hints, full solution and Core cross-link.

---

## 20. Transfer Book contract

For competitive or external-question work, use bounded study sets rather than page-count-oriented learner progress.

### Assimilation mode

Before attempt, questions may show:

```text
SOURCE
DIFFICULTY
TRANSFER
PRIMARY CONCEPT
SUPPORTS
```

Student eye path:

```text
QUESTION
→ WORK
→ STOP
→ H1 NOTICE
→ H2 MODEL
→ H3 START
```

### Mixed transfer mode

Before attempt show:

```text
CONCEPT · IDENTIFY FIRST
```

Hide the primary concept and method family. Reveal them in diagnosis/solution after marking.

Difficulty remains visible unless the publication profile deliberately suppresses it.

---

## 21. Difficulty, baseline and transfer must remain separate

Store three different concepts:

```yaml
baseline:
  band: B30

difficulty:
  source_code: D3
  learner_label: HARD

transfer:
  type: REPRESENTATION_SHIFT
```

- **Baseline** describes the learner's prior working knowledge.
- **Difficulty** describes task demand.
- **Transfer** describes distance from familiar form/context/representation.

A direct problem can be computationally hard. A far-transfer conceptual problem can be numerically easy.

---

## 22. Badge architecture belongs to Core (2)

Badges are publication components, not scientific facts.

Canonical badge families may include:

```text
SOURCE
EXAM
YEAR / SHIFT
DIFFICULTY
TRANSFER
TASK
STATUS
```

Primary/support concept hierarchy should normally use stronger semantic text hierarchy instead of reducing every field to an equal visual pill.

A badge object should carry at least:

```yaml
type: DIFFICULTY
machine_value: D3
label: HARD
visual_token: difficulty-hard
student_visible: true
```

Badge semantics must survive grayscale and cannot depend on color alone.

---

## 23. Scientific Representation Core

Before scaling Core (2) across many Physics and Chemistry topics, create one reusable **Scientific Representation Core**.

Core (2) should consume or own these representation families:

```text
XY GRAPH
NUMBER LINE / TIMELINE
VECTOR / FORCE DIAGRAM
GEOMETRIC / PATH DIAGRAM
RAY DIAGRAM
CIRCUIT DIAGRAM
WAVE DIAGRAM
FIELD DIAGRAM
APPARATUS / PROCESS DIAGRAM
PARTICLE DIAGRAM
ATOMIC / SHELL DIAGRAM
LEWIS / BONDING DIAGRAM
MOLECULAR STRUCTURE
ENERGY-LEVEL DIAGRAM
REACTION SCHEME
TABLE / GRID
EQUATION
CHEMICAL EQUATION
TRUSTED VECTOR ASSET
SOURCE CROP
```

The existing Physics pilot principle should remain: **data drives geometry; unsupported required representations fail rather than degrade silently.**

Do not scale by adding a topic-specific `elif` branch for every new diagram type.

---

## 24. Representation object

Every learner-visible scientific figure should have a semantic object independent of its final geometry.

Example:

```yaml
representation:
  id: FIG-NLM-004
  type: FORCE_DIAGRAM
  purpose: CONCEPT_EXPLANATION
  research_refs:
    - R-PHY-NLM-014
  objects:
    - block
    - surface
  vectors:
    - {label: W, direction: down}
    - {label: N, direction: up}
    - {label: f, direction: left}
  required_labels:
    - W
    - N
    - f
  student_visibility: VISIBLE
  solution_visibility: VISIBLE
  status: FINAL
```

Content semantics belong to the model. Geometry belongs to the renderer.

---

## 25. Three legitimate figure routes

A scalable publisher must support all three:

```text
STRUCTURED DATA
→ generated vector figure

APPROVED SVG / VECTOR ASSET
→ placed learner figure

SOURCE IMAGE / CROP
→ fidelity-controlled learner figure
```

Do not force every apparatus, molecule or source option figure into a procedural drawing API.

All routes must pass the same provenance, legibility, bounds and required-label QA.

---

## 26. General graph component

Do not create one renderer per graph meaning (`vt`, `xt`, `pv`, `stress_strain`, etc.).

Use a generic scientific graph object with:

- arbitrary x/y variable names and units;
- linear or selected non-linear axis scales as required;
- multiple series;
- points, segments and smooth curves;
- ticks and scientific notation;
- zero/reference lines;
- regions/area shading;
- legends;
- annotations;
- error bars where appropriate;
- discontinuities/asymptotes when needed;
- grayscale-safe series differentiation.

The graph's scientific meaning remains in Core (1) research refs and subject semantics; Core (2) controls visual grammar.

---

## 27. Equations are semantic publication objects

Do not treat scientific equations as arbitrary plain strings only.

Example:

```yaml
equation:
  id: EQ-NLM-02
  display_math: "\\vec F_{net}=m\\vec a"
  research_refs:
    - R-PHY-NLM-022
  symbol_definitions:
    F_net: net external force
    m: mass
    a: acceleration
```

Core (2) may use a specialist math-to-vector renderer while retaining the exact semantic source expression in the publication model.

Chemistry should similarly support formulae, ionic charges, reversible equations, structural notation and reaction schemes through specialist scientific typesetting rather than forcing all notation through ordinary body-text rendering.

---

## 28. Core (1) citations inside Core (2)

Student pages may show a light-touch research link where useful, for example:

```text
Research basis · R-PHY-NLM-014
```

The publication model always retains the exact `research_refs` even when student-facing citations are visually suppressed.

Core (1) MD/PDF contains the full source evidence behind those IDs.

The learner publication therefore remains traceable without becoming visually cluttered by production metadata.

---

## 29. Core (2) state machine

Core (2) should execute in this order:

```text
P0  HAND-OFF VALIDATE
P1  LEARNER PROFILE
P2  PURPOSE PROFILE
P3  CONTENT DEPTH PLAN
P4  REPRESENTATION PLAN
P5  LEARNING SEQUENCE
P6  PUBLICATION MODEL
P7  REPRESENTATIVE PROTOTYPE
P8  PROTOTYPE RENDER + REVIEW
P9  FULL BUILD
P10 CONTENT / REPRESENTATION QA
P11 QUESTION-LEVEL CLOSURE
P12 PACKAGE CERTIFICATION
```

Do not scale a full book until the representative prototype covers the required template families and passes.

---

## 30. Prototype requirements

A representative Core (2) prototype should exercise the actual risk surface of the topic, not just easy pages.

Where applicable include:

- B30 explanatory concept page;
- B80 compressed concept page;
- equation-heavy page;
- graph page;
- non-graph diagram page;
- source-crop or trusted-vector figure page;
- ordinary practice page;
- graph/diagram-heavy practice page;
- H1/H2/H3 page;
- full assimilating solution;
- Appendix C sample;
- mixed-transfer page with concept hidden;
- badge-dense external-question example.

If the topic needs a representation class that the prototype cannot render correctly, stop before scale.

---

## 31. Core (2) publication QA

Final certification is per learner obligation, not merely per PDF.

At minimum validate:

```text
HANDOFF_HASH_MATCH = 1
BLOCKING_RESEARCH_GAPS = 0
RESEARCH_REFS_RESOLVED = 1
REQUIRED_REPRESENTATIONS_PRESENT = 1
REQUIRED_REPRESENTATIONS_LEGIBLE = 1
QUESTION_DENOMINATOR_RECONCILED = 1
SOLUTION_DENOMINATOR_RECONCILED = 1
HINT_PROGRESSION_FAILURES = 0
METHOD_ASSIMILATION_FAILURES = 0
BADGE_MAPPING_FAILURES = 0
BROKEN_INTERNAL_LINKS = 0
BROKEN_SOURCE_LINKS = 0
MATH_SCIENCE_TYPOGRAPHY_FAILURES = 0
TEXT_OVERLAP_OR_CLIPPING = 0
FIGURE_BOUNDS_FAILURES = 0
ANSWER_LEAKAGE_FAILURES = 0
GRAYSCALE_INFORMATION_LOSS = 0
```

Human subject review, classroom effectiveness and psychometric calibration remain separate review states.

---

## 32. Project manifest

The router should create the project manifest before Core (1) starts.

Example:

```yaml
project_id: G9-PHY-NLM-NSO-001

grade: 9
subject: Physics

topic:
  id: laws_of_motion
  title: Laws of Motion

subtopics:
  - id: friction
    baseline: B30

purpose:
  type: COMPETITIVE_EXAM
  target: NSO

requested_products:
  core1_research: true
  core2_study_guide: true
  core2_transfer_book: true

status:
  core1: PENDING
  core2: BLOCKED_ON_CORE1
```

When Core (1) passes:

```text
core1 = PASS
core2 = READY
```

This creates an explicit two-agent workflow rather than relying on conversational memory.

---

## 33. Example A — Grade 9 Physics / Laws of Motion / NSO

Prompt:

> Prepare study material for Grade 9 Physics, Laws of Motion for NSO.

### Intake

Known automatically:

```text
Grade 9
Physics
Laws of Motion
Competitive exam
NSO
```

Repository search runs first.

Then ask only for unresolved subtopic scope and baseline, for example:

```text
Newton's laws      B80
FBDs               B50
Friction           B30
Connected systems  B30
```

### Core (1)

Reuse repository authority, research gaps, inspect representative NSO-style questions, derive exam-demand profile and produce:

```text
Laws_of_Motion_NSO_Research_Core.md
Laws_of_Motion_NSO_Research_Core.pdf
Laws_of_Motion_NSO_Research_Bundle.json
Laws_of_Motion_NSO_Exam_Demand_Profile.json
```

### Core (2)

Read only the completed research package and publication request.

Produce:

```text
Laws_of_Motion_B30-B80_NSO_Study_Guide.pdf
Laws_of_Motion_B30-B80_NSO_Transfer_Book.pdf
```

The Study Guide contains main teaching + Appendix A/B/C. The Transfer Book contains assimilation sets, mixed transfer, optional H1/H2/H3, source/difficulty/transfer metadata and complete solutions with Core (1) traceability.

---

## 34. Example B — Grade 10 Chemistry / Redox

Prompt:

> Prepare study material for Grade 10 Chemistry on Redox.

### Intake

Known:

```text
Grade 10
Chemistry
Redox
```

Ask only for missing subtopics, baseline and purpose.

Example profile:

```text
oxidation/reduction meaning       B80
oxidation numbers                 B30
oxidising/reducing agents         B30
electron transfer                 B50
purpose = routine study + competitive foundation
```

### Core (1)

Search and reuse existing Redox repository material first. Research only uncovered claims, source obligations or assessment demand. Produce the Redox Research Package.

### Core (2)

Compress B80 sections, expand B30 oxidation-number sections, choose before/after lanes and symbolic representations where supported, then publish the Study Guide with Appendix A/B/C. If external competitive questions are included, publish the separate Transfer Book from the verified corpus/evidence profile.

---

## 35. Relationship to Physics PR #155

PR #155 should be treated as a high-value implementation reference for Core (2), especially for:

- schema-before-render discipline;
- fail-closed unsupported representations;
- stable links and destinations;
- representation-dependent solution duplication;
- H1/H2/H3 rendering;
- mixed-transfer concept hiding;
- learner-facing difficulty badges;
- deterministic page planning;
- visual review bound to exact artifact hashes.

However, its current drawing implementations are Motion-oriented. Core (2) should extract reusable publication behavior and scientific primitives rather than make the Motion renderer the universal Grade 9–11 renderer.

---

## 36. Relationship to Chemistry PR #157

PR #157 should be treated as a high-value reference for:

- subject-wide two-file topic delivery;
- mandatory Appendix A/B/C semantics;
- ExamSIDE concept segregation;
- source/difficulty/transfer support metadata;
- artifact-custody rules;
- fail-closed package status;
- chapter-agnostic publication contracts.

Core (2) should generalize these useful publication rules while allowing subject-specific representations and typography. Chemistry-specific reasoning remains with Chemistry authority/Core (1); Core (2) owns the reusable publication machinery.

---

## 37. Proposed repository placement

Conceptually:

```text
Grade 9/
├── core1-research/
│   ├── SKILL.md
│   ├── schemas/
│   ├── references/
│   └── scripts/
│
├── core2-publication/
│   ├── SKILL.md
│   ├── schemas/
│   ├── renderers/
│   ├── references/
│   └── scripts/
│
├── shared/
│   ├── contracts/
│   └── scientific-representation/
│
└── projects/
```

This is a logical target, not a requirement to move existing stable skill IDs immediately. Current repository compatibility should be preserved while the new core contracts are introduced.

---

## 38. Implementation phases after approval

### Phase 1 — contracts only

Create:

- project manifest schema;
- Research Bundle hand-off schema;
- Core (2) publication-request schema;
- Research Claim / citation-link contract;
- baseline and purpose enumerations;
- Core (2) state machine and release gates.

No full renderer rewrite yet.

### Phase 2 — shared publication objects

Extract reusable components from mature pilots:

- badge object;
- question/solution object;
- appendix contract;
- link/destination system;
- generic representation envelope;
- equation object;
- generic XY graph.

### Phase 3 — scientific representation fixtures

Build golden fixtures across Physics and Chemistry, including graph, force diagram, ray/circuit/wave example, particle/bonding/energy-level example, equation-heavy page and trusted external vector asset.

### Phase 4 — independent-agent hand-off test

Run a cold-start Core (2) agent using only a completed Research Package. It must produce a faithful learner prototype without consulting the Core (1) conversation.

### Phase 5 — topic-scale pilot

Use one Physics topic and one Chemistry topic beyond the current Motion/Redox examples to prove that Core (2) is not topic-hardcoded.

---

## 39. Approval criteria for this concept

Approve the architecture if the following principles are accepted:

- [ ] Every substantial project has a separate Core (1) Research product and Core (2) Publication product.
- [ ] The router asks only for missing topic/subtopic, baseline and purpose information.
- [ ] Baseline is stored by subtopic and is separate from task difficulty and transfer distance.
- [ ] Repository search precedes new research.
- [ ] Competitive exam demand is reverse-engineered in Core (1), not rediscovered in Core (2).
- [ ] Core (1) produces a versioned structured Research Bundle, not only prose notes.
- [ ] Core (2) can operate cold from the completed Research Package.
- [ ] Core (2) may not silently repair research gaps.
- [ ] Every learner claim can trace to stable Core (1) research IDs.
- [ ] Study Guide uses stable Appendix A Core Practice / B Core Solutions / C First-Step Reference semantics.
- [ ] Transfer Book supports attempt-first H0/H1-H3, concept ownership, difficulty, transfer and mixed-transfer behavior.
- [ ] Scientific representation becomes a reusable cross-subject publication layer rather than a set of topic-specific renderers.
- [ ] Physics PR #155 and Chemistry PR #157 are mined for mature patterns without making either pilot the universal implementation.
- [ ] Final certification remains obligation-level and fail-closed.

---

## 40. Architectural invariant

The final invariant is:

> **Core (1) owns truth, scope and evidence. Core (2) owns learner adaptation, representation, scaffolding, page composition and publication QA. Core (2) may simplify presentation, but it may never silently change Core (1)'s scientific meaning.**

And operationally:

```text
ONE RESEARCH PACKAGE
      ↓
MANY VALID LEARNER PUBLICATIONS
(B30 / B80 / routine / clarification / competitive)
```

A change in learner baseline or purpose should normally require a Core (2) rebuild, not a new research exercise. A change in scientific scope, evidence or exam-demand authority requires a new Core (1) version and invalidates dependent Core (2) artifacts until revalidated.
