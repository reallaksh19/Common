# Concept Note — Core (1) Research

**Status:** Draft for architecture approval  
**Scope:** Grade 9–11 learning-production pipeline  
**Primary role:** Core (1) — repository discovery, source custody, project scope, canonical-knowledge selection, research verification, exam-demand analysis and frozen hand-off  
**Normative downstream consumer:** Core (2) Publisher concept in [PR #161](https://github.com/reallaksh19/Common/pull/161)  
**Architecture invariant:** **Research once per evidence version → publish many**

---

## 1. Decision summary

Core (1) is the single project research/evidence workflow. It does not own learner adaptation and does not own the global canonical ontology.

```text
SHARED CANONICAL REGISTRY
        ↓
PROJECT SCOPE GRAPH
        ↓
CORE (1) RESEARCH
        ↓
VERSIONED RESEARCH BUNDLE + MANIFEST
        ↓
CORE (2) PUBLISH — PR #161
        ↑
LearnerProfile + PublicationTarget
```

Core (1) answers:

> **What canonical knowledge is in scope, what evidence supports it, what claims/representations are required, and what does the target assessment evidence actually demand?**

Core (2) answers:

> **How should that verified material be taught and published for this learner and purpose?**

---

## 2. Learner baseline is not part of Research Bundle identity

The intake/router still asks for Bxx where needed, but Bxx is learner state and must be stored separately from canonical research evidence.

Example downstream object:

```yaml
learner_profile_id: LP-G9-001
baseline:
  PHY-NLM-NEWTON1:
    band: B80
    basis: USER_DECLARED
    confidence: MEDIUM
  PHY-NLM-FBD:
    band: B30
    basis: USER_DECLARED
    confidence: MEDIUM
```

Core (1) may receive this profile as a **research-priority hint** so it can prioritize likely weak bridges, but:

```text
Bxx MUST NOT change ResearchBundle identity/hash
Bxx MUST NOT change canonical mathematical/scientific truth
Bxx MUST NOT be required for Core (1) semantic readiness
```

Core (2) consumes the LearnerProfile directly.

---

## 3. Core (1) sits below a shared canonical registry

Core (1) does not silently create or mutate global concept identity.

It references stable canonical IDs through a project `ScopeGraph`:

```yaml
scope_graph:
  scope_graph_id: SG-G9-PHY-NLM-001
  canonical_nodes:
    - PHY-FORCE-001
    - PHY-N2-001
    - PHY-FBD-001
  included_edges: [...]
  excluded_nodes: [...]
  research_candidates: [...]
```

When a genuine ontology gap is discovered:

```text
RESEARCH_CANDIDATE
      ↓
SUBJECT AUTHORITY REVIEW
      ↓
CANONICAL_PROMOTION_APPROVED | REJECTED
      ↓
NEW CANONICAL REGISTRY VERSION
```

A project Research Bundle may reference a candidate while it is unresolved, but cannot publish it as a globally canonical concept without the promotion path.

---

## 4. Intake contract

The router extracts information already present and asks only for missing fields:

```text
grade / subject
topic or candidate topic
purpose / requested product
exam family/stage/cycle when applicable
user-supplied sources
curriculum/board when material
learner Bxx by subtopic when learner targeting is requested
```

Competitive requests may perform limited exam-demand discovery before final subtopic/Bxx confirmation so the proposed scope reflects actual question mechanisms.

Generic requests normally propose/confirm topic/subtopics before broad external research.

---

## 5. Repository-first discovery

Before web research Core (1) inspects reusable repository/shared objects:

```text
subject authority
canonical concept registry
prior ScopeGraphs / Research Bundles
source snapshots / source ledgers
question content / occurrences / families
exam families / cycles / demand profiles
representation definitions
misconceptions
coverage audits / review records
```

Every relevant object receives a reuse decision:

```text
REUSE_VERIFIED_FRESH
REUSE_WITH_REVALIDATION
EXTEND_EXISTING
RESEARCH_MISSING
SOURCE_UNRESOLVED
```

A valid prior bundle should be reused or versioned rather than rebuilt from scratch.

---

## 6. Research mode by purpose

### Routine study

Use confirmed curriculum/source authority plus reusable repository knowledge. Research only missing/stale claims or requested expansion.

### Concept clarification

Research narrowly around:

```text
prerequisite
missing bridge
canonical invariant/model
competing model/method
misconception
representation
transfer boundary
```

### Competitive preparation

Reverse engineer verified representative evidence before publication:

```text
verified sample/PYQ evidence
→ concepts and hidden prerequisites
→ question families
→ recognition triggers
→ representation demands
→ model/method choice
→ distractors/wrong models
→ transfer/response contract
→ ExamDemand profile
```

Do not simply make a school chapter “harder.”

### Mock exam

Freeze an evidence-based blueprint before question authoring:

```text
question count / sections
response format
concept distribution
question-family distribution
representation distribution
demand distribution
time characteristics where evidenced
cycle/source constraints
```

Original authored mock items should be labelled `ORIGINAL_EXAM_ALIGNED` or `ORIGINAL_EDITORIAL_PROFILED`, not `ORIGINAL_CALIBRATED` unless a stated calibration basis exists.

---

## 7. Controlled web research

Search only when evidence is missing/stale or the user requests current external information.

Priority:

```text
1. official exam organizer / official board
2. official syllabus / brochure / archive
3. official past paper / official solution
4. user-supplied source authority
5. verified publisher / authorized provider
6. reputable secondary source
7. discovery/community source
```

Invariant:

> **Search → verify → fingerprint → deduplicate → map → store → reuse.**

Operationally:

> **Research once per evidence version → reuse many → refresh on stale or changed authority.**

---

## 8. Source custody and rights/use

Every accepted source record includes provenance, authority and structured use rights/status.

```yaml
source_id: SRC-...
provider: ...
source_type: ...
url_or_repo_path: ...
retrieved_at: ...
content_sha256: ...
authority_level: OFFICIAL | USER_SUPPLIED | VERIFIED_SECONDARY | DISCOVERY_ONLY
verification_status: ...
rights:
  status: REFERENCE_ONLY
  # REPRODUCTION_ALLOWED
  # USER_SUPPLIED_LIMITED
  # DISCOVERY_ONLY
  # UNKNOWN_REVIEW_REQUIRED
  basis: ...
  allowed_uses:
    - EXTRACT_FACTS
    - STORE_FINGERPRINT
    - CITE_SOURCE
  prohibited_uses:
    - REPRODUCE_FULL_CONTENT
```

Discovery availability is not reproduction permission.

---

## 9. Question identity and denominator closure

Use separate identities:

```text
QuestionContent
QuestionOccurrence
QuestionFamily
QuestionAdaptation
```

Core (1) delegates frozen-denominator mechanics to the canonical corpus-coverage authority and records the resulting evidence closure in `Question_Evidence_Ledger.json`.

Each candidate occurrence carries at least:

```yaml
occurrence_id: QO-...
disposition: REQUIRED
# REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
primary_owner: ...
source_state: VERIFIED
transcription_state: VERIFIED
answer_state: VERIFIED
question_content_id: QC-...
question_family_id: QF-...
publication_targets: [...]
exclusion_reason: null
duplicate_of: null
```

Rules:

```text
REVIEW    blocks closeout
REQUIRED  belongs to frozen denominator
EXCLUDE   requires reason
DEFER     requires future owner/release
DUPLICATE points to canonical identity
```

Subject auditors extend this contract rather than creating independent denominator systems.

---

## 10. Stable research claims

Every **material** claim that can affect Core (2) receives a stable Research Claim ID.

```yaml
claim_id: R-PHY-NLM-014
concept_id: PHY-NLM-FBD-01
claim: A free-body diagram contains only forces acting on the selected body.
sources:
  - SRC-...
verification_status: VERIFIED
conditions: []
```

Core (2) traces material objects to these IDs.

Do not create claim IDs for ordinary connective prose such as navigation, transitions or page labels.

---

## 11. Semantic representation requirements

The cross-subject rendering subsystem is the **Shared Representation Layer**.

Core (1) specifies representation meaning, not page geometry.

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

Core (2) chooses compliant rendering/composition. Missing semantics produce `CORE1_RESEARCH_GAP`.

Mathematics representation types are equally first-class: constructions, coordinate/functional graphs, proof/dependency structures, algebra transformations, combinatorial structures, number lines, etc.

---

## 12. Equations/reactions and subject semantics

Core (1) owns exact semantic expression and validity; Core (2) owns typography/rendering.

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

Chemistry equivalents record state, charge, conservation, reaction conditions and structural semantics as applicable.

Mathematics equivalents record theorem conditions, domain restrictions, derivation dependencies and edge/counterexample conditions.

---

## 13. Exam-demand profile

Competitive work produces a distinct `Exam_Demand_Profile.json` containing:

```text
exam identity / cycle / stage
source authority
response format
representative evidence denominator
concepts / question families
representation demands
hidden prerequisite combinations
distractors / wrong models
reasoning or proof demand
transfer demand
time characteristics where evidenced
source-owned difficulty codes where available
editorial demand interpretation separately
confidence / evidence basis
```

Keep statuses distinct:

```text
OFFICIAL_EXAM_REQUIREMENT
SOURCE_VERIFIED_FACT
INFERRED_FROM_VERIFIED_SAMPLE
EDITORIAL_ANALYSIS
UNRESOLVED
```

---

## 14. Core (1) required outputs

Mandatory:

```text
<Topic>_Research_Bundle.json
<Topic>_Research_Bundle_Manifest.json
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Source_Ledger.json
```

Competitive/external-question work also produces:

```text
<Topic>_Exam_Demand_Profile.json
<Topic>_Question_Evidence_Ledger.json
```

Optional approved assets are referenced from stable asset identities.

`Research_Bundle.json` is the canonical semantic machine hand-off. The manifest binds the release package. MD/PDF are derived human review surfaces.

---

## 15. Research Bundle contract

Illustrative minimum shape:

```yaml
research_bundle_version: 1.0
research_bundle_id: RB-G9-PHY-NLM-001

project:
  grade: 9
  subject: Physics
  topic: Laws of Motion

scope_graph_id: SG-G9-PHY-NLM-001

research_context:
  curriculum_profile_id: CBSE-G9-...
  assessment_context:
    exam_profile_id: SOF_ISO_G9_2026_27
    exam_demand_profile_id: EXD-SOF-ISO-G9-NLM-001

concept_refs: [...]
prerequisite_refs: [...]
misconceptions: [...]
representation_requirements: [...]
equations_or_reactions: [...]
worked_reasoning: [...]
research_claims: [...]
source_registry_refs: [...]
asset_refs: [...]
question_evidence_ledger_ref: ...
source_ledger_ref: ...
unresolved_items: []
```

Notably absent:

```text
learner Bxx
student attempt history
private learner state
publication layout choices
```

---

## 16. Research Bundle Manifest and canonical hashing

Do not store a self-referential hash inside the semantic bundle.

Canonical serialization produces the semantic bundle digest; the separate manifest binds all release artifacts.

```yaml
research_bundle_manifest:
  bundle_id: RB-G9-PHY-NLM-001
  version: 1.4
  change_class: SEMANTIC
  artifacts:
    research_bundle: {sha256: ...}
    research_core_md: {sha256: ...}
    research_core_pdf: {sha256: ...}
    source_ledger: {sha256: ...}
    exam_demand_profile: {sha256: ...}
    question_evidence_ledger: {sha256: ...}
  semantic_digest: ...
  package_digest: ...
```

Core (2) records bundle ID/version plus the digest(s) required by the publication custody profile.

---

## 17. Version change classes

Every Research Bundle release records one primary `change_class`:

```text
EDITORIAL
EVIDENCE
SEMANTIC
SCOPE
EXAM_DEMAND
ASSET
```

Core (2) uses the class to determine selective revalidation or rebuild. Unknown impact fails closed.

Typical policy:

```text
EDITORIAL   → artifact/link check
EVIDENCE    → provenance/traceability revalidation
ASSET       → affected representation re-render
SEMANTIC    → rebuild affected learner material
SCOPE       → scope reconciliation / rebuild
EXAM_DEMAND → competitive products rebuild/revalidate
```

---

## 18. Derived MD/PDF zero-drift invariant

Core (1) human documents are generated/reconciled from the semantic bundle:

```text
ResearchBundle
      ↓
Research Core view model
      ↓
MD + PDF
```

Release gates:

```text
BUNDLE_TO_MD_MATERIAL_COVERAGE = 100%
BUNDLE_TO_PDF_MATERIAL_COVERAGE = 100%
UNMAPPED_MD_MATERIAL_CLAIMS = 0
UNMAPPED_PDF_MATERIAL_CLAIMS = 0
```

Material scope includes concepts, conditions, equations/reactions, examples, representation requirements, question-family evidence and exam facts.

---

## 19. Traceability classes

Use explicit publication/research traceability classes:

```text
MATERIAL_CLAIM
MATERIAL_CONDITION
MATERIAL_EXAMPLE
MATERIAL_REPRESENTATION
MATERIAL_QUESTION
MATERIAL_SOLUTION_METHOD
MATERIAL_EXAM_FACT
PEDAGOGICAL_CONNECTIVE
PRESENTATION_ONLY
```

All `MATERIAL_*` objects require valid research lineage.

---

## 20. Gap protocol

Canonical signal from Core (2):

```yaml
status: CORE1_RESEARCH_GAP
research_bundle_id: ...
gap_type: SOURCE | CONCEPT | REPRESENTATION | EQUATION | QUESTION_FAMILY | EXAM_DEMAND | ASSET
object_id: ...
blocking: true
reason: ...
reported_by: CORE2
```

Core (1) resolves the gap, issues a new version/manifest/change class, reruns readiness gates and re-hands off.

---

## 21. Core (1) readiness gate

`READY_FOR_PUBLISH` requires:

```text
REPO_DISCOVERY_RECORDED = PASS
SCOPE_GRAPH_FROZEN = PASS
CANONICAL_REFERENCES_RESOLVED = PASS
UNAPPROVED_CANONICAL_MUTATIONS = 0
PURPOSE_OR_RESEARCH_CONTEXT_RECORDED = PASS
SOURCE_AUTHORITY_RESOLVED = PASS
SOURCE_RIGHTS_STATUS_RESOLVED = PASS
SOURCE_LEDGER_RECONCILED = PASS
RESEARCH_CLAIMS_VERIFIED = PASS
REPRESENTATION_REQUIREMENTS_RESOLVED = PASS
EQUATION_REACTION_SEMANTICS_RESOLVED = PASS | NOT_APPLICABLE
EXAM_DEMAND_RESOLVED = PASS | NOT_APPLICABLE
QUESTION_EVIDENCE_RECONCILED = PASS | NOT_APPLICABLE
QUESTION_DENOMINATOR_REVIEW_ROWS = 0 | NOT_APPLICABLE
BLOCKING_UNRESOLVED_ITEMS = 0
RESEARCH_BUNDLE_SCHEMA_VALID = PASS
RESEARCH_BUNDLE_MANIFEST_VALID = PASS
BUNDLE_TO_MD_MATERIAL_COVERAGE = 100%
BUNDLE_TO_PDF_MATERIAL_COVERAGE = 100%
CORE1_COLD_START_SUFFICIENT = PASS
```

There is deliberately no `BASELINE_PROFILE_RECORDED` gate in Core (1).

---

## 22. Cold-start hand-off acceptance

A clean Core (2) agent receives:

```text
Research_Bundle.json
Research_Bundle_Manifest.json
Research_Core.md / PDF
Source_Ledger.json
Exam_Demand_Profile.json when applicable
Question_Evidence_Ledger.json when applicable
approved assets
LearnerProfile
PublicationTarget
PublicationProfile
canonical schemas/skills
```

and no original chat/browser state.

It must determine:

1. exact project scope;
2. canonical concept/prerequisite references;
3. verified material claims;
4. required representations/equations;
5. supported exam demand;
6. question evidence/denominator closure;
7. source rights/use restrictions;
8. unresolved items;
9. version/digest/change class;
10. what Core (2) may transform and what it may not change.

Required:

```text
CORE1_COLD_START_SUFFICIENT = PASS
CORE2_UNDECLARED_RESEARCH_REQUIRED = 0
MATERIAL_RESEARCH_REF_RESOLUTION = 100%
REPRESENTATION_REQUIREMENT_RESOLUTION = 100%
BLOCKING_UNRESOLVED_ITEMS = 0
```

---

## 23. Core (2) alignment requirements

PR #161 remains the downstream Publisher concept, with these review-driven interface alignments required before implementation freeze:

```text
1. LearnerProfile/Bxx must be outside ResearchBundle.
2. Appendix C invariant should be `Printable Handout`.
3. `first_step_reference` is a handout module, not the Appendix C identity.
4. Rename `Scientific Representation Core` to `Shared Representation Layer`.
5. Core (2) should record bundle version/digest/change_class effects.
6. Traceability applies to material object classes, not connective prose.
```

---

## 24. Implementation order

```text
Phase 1
Canonical registry references + ScopeGraph
LearnerProfile + PublicationTarget
ResearchBundle + ResearchBundleManifest + change_class

Phase 2
Source rights/use + research cache
QuestionEvidenceLedger denominator closure

Phase 3
Derived Research Core MD/PDF + zero-drift checks

Phase 4
Core (2) contract alignment + Shared Representation Layer

Phase 5
cold-start replay

Phase 6
Physics/Chemistry falsifiers

Phase 7
Mathematics/IOQM/proof stress tests
```

No large skill migration should precede successful hand-off/replay.

---

## 25. Central invariant

> **Core (1) selects and verifies project-scoped knowledge from the shared canonical registry, freezes evidence and semantic obligations for one evidence version, and hands off a manifest-bound Research Bundle. Learner Bxx remains outside that bundle. Core (2) combines the Research Bundle with a LearnerProfile and PublicationTarget, and must return `CORE1_RESEARCH_GAP` rather than creating hidden research, ontology changes or unsupported truth.**