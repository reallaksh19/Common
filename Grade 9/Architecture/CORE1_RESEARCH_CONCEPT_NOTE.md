# Concept Note — Core (1) Research

**Status:** Draft for architecture approval  
**Scope:** Grade 9–11 learning-production pipeline  
**Primary role:** Core (1) — repository discovery, source custody, canonical knowledge, concept architecture, research verification, exam-demand analysis and frozen hand-off  
**Normative downstream consumer:** Core (2) Publisher concept in [PR #161](https://github.com/reallaksh19/Common/pull/161)  
**Architecture invariant:** **Research once → Publish many**

---

## 1. Decision summary

Adopt Core (1) as the single research/evidence authority for every substantial study-material project.

```text
USER PROMPT
   ↓
INTAKE / ROUTER
   ↓
CORE (1) · RESEARCH
repo discovery · scope · sources · canonical concepts · verification
exam reverse engineering · question evidence · research claims
   ↓
VERSIONED RESEARCH PACKAGE
   ↓
CORE (2) · PUBLISH  — PR #161
learner adaptation · representation · scaffolding · composition · QA
   ↓
LEARNER PUBLICATION
```

Core (1) answers:

> **What is in scope, what is true, what evidence supports it, what concepts/representations are required, and what does the target assessment actually demand?**

Core (2) answers:

> **How should that verified material be taught and published for this learner and purpose?**

Core (1) must therefore finish with a machine-readable, versioned hand-off that a cold-start Core (2) agent can consume without the original chat or researcher.

---

## 2. Alignment with Core (2) PR #161

This note adopts the Core (2) interface proposed in PR #161 as the downstream requirement.

Core (1) must supply the data Core (2) explicitly expects:

```text
Research Bundle identity + version + hash
project grade / subject / topic
purpose / target assessment
included and excluded scope
baseline profile by subtopic
canonical concepts + prerequisites
misconceptions
required representations
semantic equations / reactions / claims
worked reasoning / expert paths
stable research claims
source registry / source ledger
approved assets
exam-demand profile when applicable
question-evidence ledger when applicable
explicit unresolved items
```

Core (2) PR #161 remains authoritative for learner adaptation, scientific representation rendering, badges, Appendix A/B/C, Transfer Book behavior, page composition and publication QA.

The boundary is asymmetric:

```text
Core 1 may change truth/evidence only through a new Research Bundle version.
Core 2 may change presentation but may not change Core 1 scientific meaning.
```

---

## 3. Core (1) required outputs

The mandatory hand-off names should align with PR #161:

```text
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Research_Bundle.json
<Topic>_Source_Ledger.json
```

For competitive/external-question work also produce:

```text
<Topic>_Exam_Demand_Profile.json
<Topic>_Question_Evidence_Ledger.json
```

Optional approved assets may be referenced from a stable asset directory.

The **Research Bundle JSON is the canonical machine hand-off**. The Markdown/PDF are human review surfaces. The Source Ledger proves source custody. Exam/question ledgers prove competitive-demand evidence when applicable.

---

## 4. Intake contract

The router resolves only missing information before Core (1) freezes scope:

```text
subject + grade
topic / subtopics
student baseline by subtopic
purpose / target assessment
user-supplied sources
curriculum/board when material
```

Do not ask again for values already present in the prompt.

### 4.1 Baseline meaning

`Bxx` records **estimated prior working knowledge for a subtopic**. It is not intelligence, psychometric mastery, exam difficulty or question difficulty.

Example:

```yaml
baseline_profile:
  newtons_laws:
    band: B80
    basis: USER_DECLARED
  free_body_diagrams:
    band: B30
    basis: USER_DECLARED
```

Core (1) records the baseline because it affects research priority and the eventual hand-off. It must **not** simplify canonical mathematical/scientific truth to match B30/B80.

Core (2) uses baseline aggressively for scaffolding and publication depth.

---

## 5. Repository-first discovery is mandatory

Before any web research, Core (1) searches the repository/shared store for reusable assets:

```text
subject authority
existing topic/chapter authority
prior Research Bundles
concept registries / stable IDs
source maps / obligation ledgers
source snapshots
question content / occurrences
question families
exam profiles / cycles
representation definitions
misconceptions
prior learner publications
coverage audits / review records
```

Core (1) emits a reuse decision for each relevant object:

```text
REUSE_VERIFIED_FRESH
REUSE_WITH_REVALIDATION
EXTEND_EXISTING
RESEARCH_MISSING
SOURCE_UNRESOLVED
```

A valid prior Research Bundle should be reused or versioned, not silently rebuilt from scratch.

---

## 6. Research mode depends on purpose

### Routine study

Primary evidence:

```text
user-supplied source / curriculum authority
repo subject authority
verified reference material
```

Goal: complete conceptual progression inside the confirmed scope.

### Concept clarification

Research narrowly around:

```text
prerequisite
missing bridge
canonical invariant/model
competing model
misconception
representation
transfer boundary
```

### Competitive preparation

Do not take a school chapter and merely increase question difficulty.

Core (1) first reverse-engineers the target assessment from representative verified questions/samples:

```text
verified sample/PYQ evidence
→ primary concepts
→ hidden prerequisites
→ question families
→ recognition triggers
→ representations
→ model/method choice
→ distractors / wrong models
→ transfer depth
→ response contract
→ ExamDemand profile
```

### Mock exam

Freeze a blueprint before question authoring:

```text
question count / section structure
response format
concept distribution
question-family distribution
representation distribution
demand distribution
time-pressure characteristics
source/current-cycle constraints
```

Original mock items must remain explicitly `ORIGINAL_CALIBRATED`.

---

## 7. Web research policy

Core (1) owns controlled web research. Core (2) does not normally browse.

Search only when:

1. required evidence is missing;
2. exam/curriculum data is stale for the requested cycle;
3. the user explicitly requests current/latest information;
4. source/question provenance is unresolved;
5. the frozen corpus has a documented evidence gap;
6. an exam name/pattern/syllabus may have changed;
7. the user provides an external source that must be inspected.

Source hierarchy:

```text
1. official exam organizer / official board
2. official syllabus / brochure / archive
3. official past paper / official solution
4. user-supplied source authority
5. verified publisher / authorized provider
6. reputable secondary source
7. discovery/community source
```

Secondary sites, indexes or mirrors may help discovery but do not silently override official authority.

The invariant is:

> **Search → verify → fingerprint → deduplicate → map → store → reuse.**

---

## 8. Source custody and research ledger

Every accepted source becomes a durable source record/snapshot with, as applicable:

```yaml
source_id: SRC-...
provider: ...
source_type: ...
url_or_repo_path: ...
retrieved_at: ...
content_sha256: ...
authority_level: OFFICIAL | USER_SUPPLIED | VERIFIED_SECONDARY | DISCOVERY_ONLY
scope_role: ...
license_or_use_note: ...
verification_status: ...
```

Research results must distinguish:

```text
OFFICIAL_REQUIREMENT
SOURCE_VERIFIED_FACT
INFERRED_FROM_VERIFIED_SAMPLE
EDITORIAL_ANALYSIS
UNRESOLVED
```

Patterns inferred from sample questions are evidence about recurring demand; they are not automatically official syllabus statements.

---

## 9. Shared question identities

Core (1) must not store one intellectual question repeatedly for every mirror/source.

Use separate identities:

```text
QuestionContent      canonical intellectual question
QuestionOccurrence   where/when it appeared
QuestionFamily       underlying recognition/method family
QuestionAdaptation   derived learner-facing version
```

The external/question evidence ledger maps occurrences to canonical content/families and preserves source provenance.

Semantic near-duplicates are flagged for review, not auto-merged when their decisive mechanism may differ.

---

## 10. Concept architecture

Core (1) owns canonical topic/subtopic/concept structure for the project.

Every important concept should record, as applicable:

```text
concept ID
prerequisites
bridge concepts
canonical statement/model/invariant
conditions / limits / exceptions
required representations
expert noticing / first move
nearest competing model/method
misconceptions
transfer endpoints
source/research claim references
```

Subject authority determines the semantics:

```text
Mathematics → invariant, proof/derivation, decision boundary, counterexample, method family
Physics → system, frame, model/law, sign/vector semantics, units, validity, representation translation
Chemistry → macro/particle/symbolic meaning, species, conservation, conditions, evidence, reaction/process semantics
```

Core (1) is learner-neutral in truth, but may be target-aware in research priority.

---

## 11. Stable research claims

Every claim that can materially affect Core (2) receives a stable Research Claim ID.

Example:

```yaml
claim_id: R-PHY-NLM-014
concept_id: PHY-NLM-FBD-01
claim: A free-body diagram contains only forces acting on the selected body.
sources:
  - SRC-...
verification_status: VERIFIED
conditions: []
```

Core (2) records these IDs in `research_refs`.

Required trace:

```text
SOURCE / QUESTION OCCURRENCE
      ↓
CORE (1) RESEARCH CLAIM / CONCEPT / REPRESENTATION
      ↓
CORE (2) SECTION / FIGURE / QUESTION / SOLUTION
```

Core (1) is therefore the evidence origin. Core (2) is never the hidden source of a new scientific/mathematical claim.

---

## 12. Representation requirements for Core (2)

PR #161 proposes a shared Scientific Representation Core in the publication layer. Core (1) must provide **semantic representation requirements**, not final geometry.

Example:

```yaml
representation_requirement:
  id: RREP-NLM-004
  type: FORCE_DIAGRAM
  concept_ids:
    - PHY-NLM-FBD-01
  research_refs:
    - R-PHY-NLM-014
  semantic_requirements:
    selected_body: block
    forces:
      - weight
      - normal
      - friction
  required_labels:
    - W
    - N
    - f
  approved_asset_ids: []
```

Core (2) chooses a compliant rendering route:

```text
structured generated vector
approved SVG/vector asset
source crop / fidelity-controlled asset
```

If Core (1) has not defined a required scientific representation/claim sufficiently, Core (2) must return a Core (1) gap rather than invent semantics.

---

## 13. Equation / reaction semantic objects

Core (1) owns the meaning and validity of equations/reactions. Core (2) owns typesetting/rendering.

Example:

```yaml
equation:
  id: REQ-NLM-02
  semantic_expression: "F_net = m a"
  concept_id: PHY-NLM-SECOND-LAW
  research_refs:
    - R-PHY-NLM-022
  symbol_definitions: {...}
  conditions: [...]
  unit_or_dimension_checks: [...]
```

Chemistry equivalents also record charge/state/conditions/conservation as required.

---

## 14. Competitive exam-demand profile

When competitive work is in scope, Core (1) produces a distinct `Exam_Demand_Profile.json`.

It should contain:

```text
exam identity / cycle / stage
source authority
response format
representative evidence set
dominant concepts
question families
common representations
hidden prerequisite combinations
common distractors / wrong models
reasoning/method demands
transfer demand
time-pressure characteristics where evidenced
source-owned difficulty codes when available
editorial demand interpretation separately
confidence / evidence basis
```

Core (2) consumes this object. It must not independently re-derive exam demand from new browsing.

---

## 15. Research Bundle contract

Core (1) adopts the PR #161 Research Bundle interface and makes it explicit.

Minimum shape:

```yaml
research_bundle_version: 1.0
research_bundle_id: G9-PHY-NLM-NSO-001

project:
  grade: 9
  subject: Physics
  topic: Laws of Motion

purpose:
  type: COMPETITIVE_EXAM
  target: SOF_ISO

scope:
  included_subtopics: [...]
  excluded_subtopics: [...]

baseline_profile: {...}

concepts: [...]
prerequisites: [...]
misconceptions: [...]
representations_required: [...]
equations: [...]
worked_reasoning: [...]
research_claims: [...]
source_registry: [...]
assets: [...]

exam_demand_profile: ...
question_evidence_ledger: ...
source_ledger: ...

unresolved_items: []
```

The final bundle records its own hash/fingerprint. Every Core (2) publication must record:

```text
research_bundle_id
research_bundle_version
research_bundle_sha256
```

A new Core (1) version invalidates dependent Core (2) artifacts until revalidation.

---

## 16. Gap protocol aligned to Core (2)

PR #161 uses the fail-back signal:

```text
CORE1_RESEARCH_GAP
```

Adopt this as the canonical status while keeping a structured gap object:

```yaml
status: CORE1_RESEARCH_GAP
research_bundle_id: ...
gap_type: SOURCE | CONCEPT | REPRESENTATION | EQUATION | QUESTION_FAMILY | EXAM_DEMAND | ASSET
object_id: ...
blocking: true
reason: ...
reported_by: CORE2
```

Core (1) resolves the gap, increments the Research Bundle version, records the change, re-runs its readiness gates and re-hands off.

Core (2) resumes only from the new version.

---

## 17. Core (1) readiness gate

Core (1) states:

```text
RESEARCH_IN_PROGRESS
READY_WITH_NONBLOCKING_GAPS
READY_FOR_PUBLISH
BLOCKED_RESEARCH_GAP
```

`READY_FOR_PUBLISH` requires:

```text
REPO_DISCOVERY_RECORDED = PASS
TOPIC_SCOPE_CONFIRMED = PASS
SUBTOPIC_SCOPE_CONFIRMED = PASS
BASELINE_PROFILE_RECORDED = PASS
PURPOSE_RECORDED = PASS
SOURCE_AUTHORITY_RESOLVED = PASS
SOURCE_LEDGER_RECONCILED = PASS
CANONICAL_CONCEPTS_RESOLVED = PASS
PREREQUISITE_BRIDGES_RESOLVED = PASS
RESEARCH_CLAIMS_VERIFIED = PASS
REPRESENTATION_REQUIREMENTS_RESOLVED = PASS
EQUATION_REACTION_SEMANTICS_RESOLVED = PASS | NOT_APPLICABLE
EXAM_DEMAND_RESOLVED = PASS | NOT_APPLICABLE
QUESTION_EVIDENCE_RECONCILED = PASS | NOT_APPLICABLE
BLOCKING_UNRESOLVED_ITEMS = 0
CITATION_CHAIN_COMPLETE = PASS
RESEARCH_BUNDLE_SCHEMA_VALID = PASS
RESEARCH_BUNDLE_HASHED = PASS
```

For Mathematics add mathematical verification/conditions/edge cases. For Physics add model validity/units/frame/sign semantics where applicable. For Chemistry add conservation/charge/conditions/representation integrity where applicable.

---

## 18. Cold-start hand-off acceptance

Core (1) is not complete merely because its PDF reads well.

A clean Core (2) agent must receive only:

```text
Research_Core.md
Research_Core.pdf
Research_Bundle.json
Source_Ledger.json
Exam_Demand_Profile.json when applicable
Question_Evidence_Ledger.json when applicable
approved assets
publication request
repository schemas/skills
```

and be able to determine:

1. exact scope;
2. baseline profile;
3. purpose/assessment target;
4. canonical concepts and prerequisites;
5. which claims are verified;
6. which representations/equations are required;
7. which question families/exam demands are supported;
8. which source evidence supports each material claim;
9. whether any unresolved item blocks publication;
10. what it may adapt and what it may not change.

Required acceptance counters:

```text
CORE1_COLD_START_SUFFICIENT = PASS
CORE2_UNDECLARED_RESEARCH_REQUIRED = 0
RESEARCH_CLAIM_ID_RESOLUTION = 100%
REPRESENTATION_REQUIREMENT_RESOLUTION = 100%
BLOCKING_UNRESOLVED_ITEMS = 0
```

---

## 19. Relationship to the unified architecture

Core (1) sits between shared knowledge/research infrastructure and Core (2):

```text
SHARED CANONICAL DATA
concepts · sources · questions · exam profiles · curricula
               │
               ▼
          CORE (1) RESEARCH
project scope · evidence decisions · verified claims · demand profile
               │
      versioned Research Bundle
               │
               ▼
          CORE (2) PUBLISH
         PR #161 contract
               │
               ▼
          LEARNER PRODUCTS
```

Shared canonical data is reused across projects. The Research Bundle is the project-specific frozen projection. Core (2) is a learner/purpose-specific downstream projection.

Thus:

```text
SHARED KNOWLEDGE → many Research Bundles
ONE Research Bundle → many Publish Cores
```

---

## 20. Implementation order after approval

### Phase 1 — hand-off contracts

Define schemas for:

```text
ProjectManifest
BaselineProfile
ResearchBundle
ResearchClaim
RepresentationRequirement
SourceLedger
ExamDemandProfile
QuestionEvidenceLedger
Core1ResearchGap
```

Align the exact versions/enums with PR #161's `publication_request` contract.

### Phase 2 — repo-first discovery and research cache

Add durable lookup/freshness/dedup logic for:

```text
sources
snapshots
concepts
questions / occurrences
question families
exam profiles
prior Research Bundles
```

### Phase 3 — two falsifier pilots

Use:

```text
Grade 9 Physics — Laws of Motion — competitive preparation/mock
Grade 10 Chemistry — Redox — routine study
```

Freeze one Core (1) for each and produce at least two different Bxx/purpose publications from each.

### Phase 4 — cold-start Core (2) replay

Run the PR #161 Core (2) workflow without chat history. Any undocumented research dependency is a Core (1) failure.

### Phase 5 — Mathematics / proof / broader representation stress

Test Mathematics competitive pathways, proof response contracts and additional Physics/Chemistry representation families.

---

## 21. Approval decisions requested

| ID | Decision | Recommendation |
|---|---|---|
| C1-1 | Adopt Core (1) as the single project research/evidence workflow | APPROVE |
| C1-2 | Use PR #161 Core (2) as the normative downstream publication contract | APPROVE |
| C1-3 | Make `Research_Bundle.json` the canonical machine hand-off | APPROVE |
| C1-4 | Require repository-first discovery before web research | APPROVE |
| C1-5 | Keep Bxx subtopic-specific and separate from exam/task difficulty | APPROVE |
| C1-6 | Put competitive-exam reverse engineering in Core (1) only | APPROVE |
| C1-7 | Require stable Research Claim IDs and source lineage | APPROVE |
| C1-8 | Require semantic representation/equation requirements before Core (2) renders them | APPROVE |
| C1-9 | Adopt `CORE1_RESEARCH_GAP` as the fail-back status | APPROVE |
| C1-10 | Version/hash Research Bundles and invalidate dependent Core (2) artifacts on change | APPROVE |
| C1-11 | Require cold-start Core (2) sufficiency as a Core (1) release gate | APPROVE |
| C1-12 | Reuse shared canonical data; do not clone it into every project Research Bundle | APPROVE |

---

## 22. Central invariant

> **Core (1) owns truth, scope, evidence and assessment-demand interpretation. Core (2) PR #161 owns learner adaptation, representation rendering, scaffolding and publication. Core (1) must hand off a versioned Research Bundle that makes Core (2) independently executable; Core (2) must return `CORE1_RESEARCH_GAP` rather than silently creating new scientific or mathematical truth.**
