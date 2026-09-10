# Unified Two-Core Learning Architecture

**Architecture decision:** ADOPTED FOR DESIGN  
**Implementation status:** DRAFT / NOT YET MIGRATED  
**Scope:** Grades 9–11 Mathematics, Physics and Chemistry initially; extensible to additional subjects/exams  
**Core (1):** [`CORE1_RESEARCH_CONCEPT_NOTE.md`](CORE1_RESEARCH_CONCEPT_NOTE.md)  
**Core (2):** [Draft PR #161 — Core (2) Publisher](https://github.com/reallaksh19/Common/pull/161)

---

## 1. Unified decision

The production invariant is now stated precisely as:

> **Research once per evidence version → reuse many → publish many → refresh when authority/evidence becomes stale or changes.**

The architecture separates five different responsibilities that must not collapse into one another:

```text
SHARED CANONICAL REGISTRY
concepts · methods · representations · misconceptions
questions · sources · curricula · exam identities
            │
            ▼
PROJECT SCOPE GRAPH
selected canonical IDs · project inclusions/exclusions
research candidates · assessment context
            │
            ▼
CORE (1) RESEARCH
truth/evidence verification · source custody
exam-demand analysis · semantic requirements
            │
            ▼
VERSIONED RESEARCH BUNDLE
no learner Bxx inside canonical bundle identity
            │
            ├─────────────────────┐
            │                     │
            ▼                     ▼
     LEARNER PROFILE       PUBLICATION TARGET
 Bxx by subtopic + basis   purpose · exam · products
            │                     │
            └──────────┬──────────┘
                       ▼
                CORE (2) PUBLISH
 learner adaptation · shared representation layer
 scaffolding · composition · rendering · publication QA
                       │
                       ▼
                 LEARNER PRODUCTS
```

This replaces the earlier model in which learner Bxx appeared inside the Research Bundle.

---

## 2. Authority boundaries

| Concern | Canonical Registry | Project / Core (1) | Core (2) Publisher |
|---|---|---|---|
| scientific/mathematical concept identity | owns | references | consumes |
| ontology changes | subject-reviewed registry version | may propose candidates only | prohibited |
| project scope | no | owns through `ScopeGraph` | preserves |
| repository/web research | no | owns | prohibited by default |
| source custody / provenance | shared source identity | owns project evidence decision | references |
| exam-demand interpretation | shared exam identity/cycle | owns researched demand profile | consumes |
| learner Bxx | no | may see as a research-priority hint | owns application from `LearnerProfile` |
| learner sequencing/scaffolding | no | does not own | owns |
| representation meaning | canonical types + subject semantics | specifies semantic requirement | renders/composes |
| publication layout/render QA | no | research artifact QA only | owns |

The governing rule is:

> **Core (1) may select and verify canonical knowledge for a project, but it may not silently redefine the global ontology. Core (2) may transform presentation, but it may not create new mathematical/scientific truth.**

---

## 3. Bxx and learner state are downstream inputs

`Bxx` means estimated prior working knowledge for one topic/subtopic. It remains part of intake, but it is **not part of the canonical Research Bundle** and must not alter the bundle semantic hash.

Example:

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

The same Research Bundle can therefore support:

```text
B30 routine-study publication
B80 routine-study publication
B50 school-exam publication
B70 competitive publication
B40 concept-repair publication
```

Core (1) may receive Bxx during intake to prioritize research effort, but Bxx is not truth/evidence and is excluded from Research Bundle identity.

Core (2) canonical input becomes:

```text
ResearchBundle
+ LearnerProfile
+ PublicationTarget
+ PublicationProfile
```

---

## 4. Exam demand remains an evidence concern

Unlike Bxx, a researched exam-demand profile may legitimately belong to Core (1), because it represents verified assessment evidence.

A competitive Research Bundle may therefore reference:

```yaml
assessment_context:
  exam_profile_id: SOF_ISO_G9_2026_27
  exam_demand_profile_id: EXD-SOF-ISO-G9-NLM-001
```

Core (2) validates that its requested exam target is supported by the bundle:

```text
PublicationTarget.exam_demand
          ⊆
ResearchBundle.supported_exam_demand
```

If not, Core (2) returns `CORE1_RESEARCH_GAP`.

---

## 5. Shared canonical registry vs project ScopeGraph

A project Research Core must not create its own competing canonical ontology.

Use:

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

If Core (1) finds a concept or relationship that is not represented adequately in the shared registry, it creates a candidate:

```text
RESEARCH_CANDIDATE
      ↓
SUBJECT AUTHORITY REVIEW
      ↓
CANONICAL_PROMOTION_APPROVED | REJECTED
      ↓
NEW CANONICAL REGISTRY VERSION
```

Only the subject/canonical governance path may promote a candidate. Core (1) project research cannot mutate global concept identity silently.

---

## 6. Core (1) canonical output package

Mandatory outputs:

```text
<Topic>_Research_Bundle.json
<Topic>_Research_Bundle_Manifest.json
<Topic>_Research_Core.md
<Topic>_Research_Core.pdf
<Topic>_Source_Ledger.json
```

Competitive/external-question additions:

```text
<Topic>_Exam_Demand_Profile.json
<Topic>_Question_Evidence_Ledger.json
```

`Research_Bundle.json` is the canonical semantic hand-off. Markdown/PDF are derived human review surfaces. `Research_Bundle_Manifest.json` binds the released package.

---

## 7. Research Bundle identity and hashing

The Research Bundle must not contain a self-referential hash.

Use canonical serialization for the semantic bundle and store hashes in the external manifest:

```yaml
research_bundle_manifest:
  bundle_id: RB-G9-PHY-NLM-001
  version: 1.4
  change_class: EXAM_DEMAND

  artifacts:
    research_bundle:
      sha256: ...
    research_core_md:
      sha256: ...
    research_core_pdf:
      sha256: ...
    source_ledger:
      sha256: ...
    exam_demand_profile:
      sha256: ...
    question_evidence_ledger:
      sha256: ...

  semantic_digest: ...
  package_digest: ...
```

`semantic_digest` binds semantic machine content. `package_digest` binds the complete released research package including human views/assets.

Core (2) records at least:

```text
research_bundle_id
research_bundle_version
semantic_digest
package_digest when exact-artifact custody is required
```

---

## 8. Core (1) MD/PDF are derived review surfaces

Core (1) must follow one-directional generation/reconciliation:

```text
ResearchBundle semantic model
          ↓
Research Core view model
          ↓
      ┌───┴───┐
      ▼       ▼
     MD      PDF
```

Do not independently author JSON, Markdown and PDF as parallel authorities.

Release gates must reconcile material objects:

```text
BUNDLE_TO_MD_MATERIAL_COVERAGE = 100%
BUNDLE_TO_PDF_MATERIAL_COVERAGE = 100%
UNMAPPED_MD_MATERIAL_CLAIMS = 0
UNMAPPED_PDF_MATERIAL_CLAIMS = 0
```

Material objects include concepts, conditions, equations/reactions, worked examples, representation requirements, question-family findings and exam-demand facts.

---

## 9. Material traceability classes

The requirement is 100% traceability for **material learner semantics**, not for connective prose or layout text.

Recommended classes:

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

All `MATERIAL_*` Core (2) objects must resolve to Core (1) research IDs and ultimately source/question evidence where applicable.

`PEDAGOGICAL_CONNECTIVE` and `PRESENTATION_ONLY` do not require artificial claim IDs.

Required chain:

```text
SOURCE / QUESTION OCCURRENCE
      ↓
CORE (1) RESEARCH CLAIM / CONCEPT / REPRESENTATION
      ↓
CORE (2) MATERIAL OBJECT
```

---

## 10. Question evidence and denominator closure

Core (1) does not create a second corpus-accounting authority. It delegates denominator mechanics to the canonical corpus-coverage service and freezes the result in `Question_Evidence_Ledger.json`.

Each candidate occurrence should carry at least:

```yaml
occurrence_id: QO-...
disposition: REQUIRED
# REQUIRED | DEFER | EXCLUDE | REVIEW | DUPLICATE
primary_owner: PHY-FBD-01
source_state: VERIFIED
transcription_state: VERIFIED
answer_state: VERIFIED
question_content_id: QC-...
question_family_id: QF-...
publication_targets:
  - TRANSFER_BOOK
exclusion_reason: null
duplicate_of: null
```

Closure rules:

```text
REVIEW       → blocks closeout
REQUIRED     → part of frozen denominator
DUPLICATE    → points to canonical identity
EXCLUDE      → reason required
DEFER        → future owner/release required
```

Subject-specific auditors extend the generic denominator contract; they do not redefine it.

---

## 11. Source rights/use status

Discovery evidence and reproduction permission are different concerns.

Every source record should contain structured use status in addition to authority/provenance:

```yaml
rights:
  status: REFERENCE_ONLY
  # REPRODUCTION_ALLOWED
  # REFERENCE_ONLY
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

ExamSIDE, Scribd, mirrors and secondary indexes may be useful for discovery/evidence without granting permission to reproduce their full content.

---

## 12. Original-question provenance and calibration language

Do not use `ORIGINAL_CALIBRATED` unless an explicit calibration basis exists.

Default authoring statuses should be:

```text
ORIGINAL_EXAM_ALIGNED
ORIGINAL_EDITORIAL_PROFILED
```

If stronger calibration exists, record it separately:

```yaml
calibration:
  basis: SOURCE_MAPPING | EXPERT_REVIEW | EMPIRICAL
  evidence_refs: [...]
```

The same provenance rule applies to difficulty labels and learner baseline estimates.

---

## 13. Shared Representation Layer

Rename the cross-subject publication subsystem from **Scientific Representation Core** to:

> **Shared Representation Layer**

This avoids implying a third architectural Core and includes Mathematics as well as Physics/Chemistry.

Core (1) owns semantic requirements:

```text
what must be shown
relationships/constraints
required labels
conditions
approved source/asset refs
supporting research claims
```

The Shared Representation Layer provides semantic object types/rendering capability for, for example:

```text
XY graph
number line
geometric construction
proof/dependency diagram
algebra transformation
force/vector diagram
ray/circuit/wave/field diagram
apparatus/process diagram
particle/atomic/Lewis/molecular representation
energy-level/reaction scheme
equation/chemical equation
trusted vector asset/source crop
```

Core (2) selects compliant rendering/composition routes. Unsupported required representations fail closed.

---

## 14. Core (2) learner-output contract

The shared Study Guide base is frozen as:

```text
MAIN LEARNING SECTION

Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

`Appendix C` has one invariant product identity. Subject/purpose profiles define its internal modules, such as:

```text
first_step_reference
concept_map
key_rules_conditions
common_traps
process_router
self_check
```

For Mathematics, `first_step_reference` will normally be required. Other subjects may emphasize a different handout module while retaining the same Appendix C product identity.

Hints (`H0/H1/H2/H3`) remain support mechanics and do not redefine Appendix B.

Competitive/external-question work may additionally produce a separate Transfer Book.

**Alignment note:** PR #161 should adopt the same Appendix C and Shared Representation Layer terminology before implementation freeze.

---

## 15. Version change classes and selective invalidation

Every released Research Bundle version should record a `change_class`:

```text
EDITORIAL
EVIDENCE
SEMANTIC
SCOPE
EXAM_DEMAND
ASSET
```

Default revalidation policy:

| Change class | Core (2) consequence |
|---|---|
| EDITORIAL | no semantic rebuild; artifact/link check as needed |
| EVIDENCE | provenance/traceability revalidation |
| ASSET | affected representation re-render/recheck |
| SEMANTIC | rebuild affected learner sections/products |
| SCOPE | full scope reconciliation; normally rebuild affected product |
| EXAM_DEMAND | rebuild/revalidate competitive products; routine products may be unaffected |

Fail closed when impact cannot be determined.

---

## 16. Gap protocol

Core (2) never silently researches around a missing semantic/evidence dependency.

Canonical signal:

```yaml
status: CORE1_RESEARCH_GAP
research_bundle_id: ...
gap_type: SOURCE | CONCEPT | REPRESENTATION | EQUATION | QUESTION_FAMILY | EXAM_DEMAND | ASSET
object_id: ...
blocking: true
reason: ...
```

Core (1) resolves the gap, issues a new bundle version/change class, rebuilds its manifest and re-hands off.

---

## 17. Cold-start acceptance

Core (1) passes only if a clean Core (2) agent can work with:

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
canonical schemas/skills
```

No original chat or researcher state is allowed.

Required counters include:

```text
CORE1_COLD_START_SUFFICIENT = PASS
PUBLISH_AGENT_NO_HIDDEN_CONTEXT = PASS
PUBLISH_AGENT_UNDECLARED_WEB_SEARCHES = 0
MATERIAL_TRACEABILITY_COVERAGE = 100%
BLOCKING_UNRESOLVED_ITEMS = 0
BUNDLE_TO_MD_MATERIAL_COVERAGE = 100%
BUNDLE_TO_PDF_MATERIAL_COVERAGE = 100%
```

---

## 18. Implementation sequence

Do not freeze production schemas until the reviewed ownership corrections above are reflected in both Core contracts.

```text
Phase 1
Canonical IDs + ScopeGraph + LearnerProfile + PublicationTarget
ResearchBundle + ResearchBundleManifest + change_class

Phase 2
Source rights/use + repo discovery + research cache
QuestionEvidenceLedger denominator closure

Phase 3
Core (1) derived MD/PDF views + zero-drift reconciliation

Phase 4
Core (2) shared objects + Shared Representation Layer
Appendix A/B/C normalization

Phase 5
cold-start Core (1) → Core (2) replay

Phase 6
Physics Laws of Motion + Chemistry Redox falsifiers

Phase 7
Mathematics/IOQM/proof and broader representation stress tests
```

Existing stable skill IDs remain unchanged until the new contracts and replay pass.

---

## 19. Final invariant

> **Canonical knowledge is governed globally. Core (1) freezes a project ScopeGraph and verified evidence package for one evidence version. Learner Bxx stays outside that truth/evidence package. Core (2), as specified by PR #161 and this alignment, combines the Research Bundle with a LearnerProfile and PublicationTarget to create learner products. Material semantics remain traceable; research refreshes on changed/stale authority; and no agent silently creates a second source, ontology or research authority.**