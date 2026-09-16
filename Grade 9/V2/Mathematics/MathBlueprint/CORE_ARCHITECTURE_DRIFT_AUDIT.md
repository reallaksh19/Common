# Mathematics V2 — Core Architecture and Documentation Drift Audit

**Audit Class**: `READ_ONLY_AUDIT`  
**Target Subject**: `MATHEMATICS`  
**Architecture Root**: `Grade 9/V2/Mathematics/MathBlueprint/`  
**Governing Document**: `CANONICAL_ARCHITECTURE.md`  
**Repository Basis**: `reallaksh19/Common` at commit `3af2d879e21d169da6a97340501afc0298178669`  
**Academician & Pedagogical Context**: Grade 9 to 11 Competitive Mathematics (IIT-JEE / IOQM / Olympiad)

---

## 1. Executive Summary

This comprehensive audit evaluates the alignment among normative architecture documentation, executable contracts (schemas), runtime policies, engine compilers, validators, tests, and CI workflows across the Mathematics V2 Blueprint.

As an expert academician preparing students for high-stakes examinations such as IIT-JEE Advanced and IOQM, conceptual assimilation requires uncompromised structural integrity:
- **Theoretical Models (Core1A/Core1B)** must build complete, intrinsic mathematical understanding (e.g. polynomial relations, Vieta's formulas, transformation bijections, location of roots) without dilution from diagnostic scores.
- **Problem Solving & Transfer (Core2A/Core2B)** must be calibrated through explicit learner knowledge or formal owner waiver against multi-dimensional task demands ($M0$ to $M8$).
- **Candidate Discovery** must remain broadly receptive to diverse competition, board, and regional terminologies while strictly prohibiting ranking or similarity scores from bypassing exact Engineering Gate authorization.

### Key Audit Findings
1. **Target vs. Implemented Architecture Gap**: `CANONICAL_ARCHITECTURE.md` defines the canonical Six-Core Architecture (Ground Truth $\to$ Core0 $\to$ Core1/Core2 $\to$ CDR $\to$ CDAU $\to$ SDU/LAU $\to$ TTU $\to$ Publication). However, earlier executable components (`build_assimilation_demand.py`, `compile_assimilation_plan.py`) still reflect the single-track assimilation pipeline (`AssimilationDemand` $\to$ `AssimilationPlan`). The codebase contains transitional bridges (e.g. `compile_sdu_lau_generation_spec.py`, `math-dual-track-product-model.schema.json`) that begin this convergence.
2. **Pedagogy Research Optionality Alignment**: Executable code (`validate_pedagogy_research_manifest.py`, `validate_product_governance.py`) correctly enforces that EASY difficulty research is optional (default absent in generation), whereas MEDIUM and HARD difficulties strictly mandate research briefs and bound claims. Earlier references suggesting research was entirely forbidden for EASY have been resolved in the executable contracts, but subtle phrasing differences persist across documents.
3. **Absence of Minimum Source-Count Quota**: The system exhibits strict evidence discipline: research requires claim-level coverage, support/contradiction classification, and contradiction resolution. No artificial minimum source-count quota exists in production code, preventing "URL-stuffing" gaming.
4. **Strict Enforcement of SDU vs. LAU Boundary**: Production validators (`validate_product_governance.py`, `compile_sdu_lau_generation_spec.py`) strictly enforce that learner knowledge percentage NEVER alters Core1A/Core1B depth. SDU consumes intrinsic difficulty badges only. Core2A/Core2B LAU conditioning requires either a verified percentage with a named calibration policy and source ref, or an explicit Owner Waiver.
5. **Engineering Visibility Publication Separation**: Product visibility manifests are schema-locked to `publication_authorization = NOT_IMPLIED`. Publication is generated solely from `LEARNER_PUBLICATION_BUNDLE_ONLY`.

---

## 2. Current Architecture Map

The repository exhibits a dual-track architecture undergoing convergence to the canonical six-core topology:

```text
                               [OWNER CONTROL PLANE]
                 purpose • policy • difficulty override • owner waiver
                                         |
                                         v
                             [ORIGINAL GROUND TRUTH]
                 questions • syllabus • authoritative sources • answers
                                         |
                                         v
                              [CORE0 EVIDENCE ROUTER]
                             (route_math_learning_run.py)
                                         |
                     +-------------------+-------------------+
                     |                                       |
                     v                                       v
             [CORE1 SPECIALIST]                      [CORE2 SPECIALIST]
          (semantic reconstruction)               (assessment reconstruction)
                     |                                       |
                     v                                       v
             SpecialistPackage                       SpecialistPackage
                     |                                       |
                     +-------------------+-------------------+
                                         |
                                         v
                             [CROSS-VALIDATION & JOIN]
                             (run_dual_intelligence.py)
                                         |
                                         v
                         [CANONICAL DOMAIN REGISTRY (CDR)]
                         (validate_canonical_domain_registry.py)
                                         |
                                         v
                                      [CDAU]
                    (Cross-Core Differentiation & Governance)
                                         |
                     +-------------------+-------------------+
                     |                                       |
                     v                                       v
         [SDU: STUDY DIFFERENTIATION]            [LAU: LEARNER ADAPTATION]
               (Core1A / Core1B)                       (Core2A / Core2B)
          Intrinsic Difficulty: E/M/H             Learner % OR Owner Waiver
            NO Learner % Influence                 x Task Demand (M0 to M8)
                     |                                       |
                     v                                       v
             [CONCEPT TTU FAMILY]                   [PROBLEM TTU FAMILY]
                     |                                       |
           +---------+---------+                   +---------+---------+
           v                   v                   v                   v
        Core1A              Core1B              Core2A              Core2B
       (Complete           (Open Tutor         (Worked Problem     (Transfer
       Reference)          Reconstruct)         Apprentice)         Tutor)
           |                   |                   |                   |
           +---------+---------+                   +---------+---------+
                     |                                       |
                     v                                       v
             [SELF-HELP CLOSURE]                     [SELF-HELP CLOSURE]
                     |                                       |
                     +-------------------+-------------------+
                                         |
                                         v
                            [PRODUCT GOVERNANCE GATE]
                          (validate_product_governance.py)
                           - Cross-Core Coverage Ledger
                           - Cross-Core Similarity Audit
                           - Stage Governance Receipts
                                         |
                                         v
                        [DERIVED ENGINEERING VISIBILITY]
                     (compile_engineering_visibility_manifest.py)
                      authority: NON_AUTHORITATIVE_VIEW
                      publication_authorization: NOT_IMPLIED
                                         |
                                         v
                        [SEMANTIC PUBLICATION COMPILER]
                          (compile_publication_bundle.py)
                                         |
                                         v
                         [GOVERNED PUBLICATION RENDERER]
                       (render_publication_bundle_pdf.py)
                                         |
                                         v
                             Final Governed Learner PDF
```

---

## 3. Normative-Document Inventory

| Document Path | Stated Purpose | Authority Level | Implemented State |
|---|---|---|---|
| `CANONICAL_ARCHITECTURE.md` | Target 6-Core Architecture (Ground Truth $\to$ Core0 $\to$ Core1/Core2 $\to$ CDR $\to$ CDAU $\to$ SDU/LAU $\to$ TTU $\to$ Publication) | **Highest Target Architecture** | Normative target; existing 1-track and 2-track engines converge toward this. |
| `README.md` | Blueprint orchestration overview, canonical topology, intelligence boundaries | Informational / Architectural Overview | Partially stale; still presents single-track assimilation pipeline as primary topology. |
| `SELF_TEACHING.md` | Self-teaching pedagogy contract for Core1A/1B and Core2A/2B | Normative Pedagogy | Fully aligned with executable contracts (`validate_self_teaching_contract.py`). |
| `GENERATION_CALIBRATION.md` | Generation control boundaries: difficulty badges (SDU) vs learner calibration (LAU) | Normative Calibration | Fully aligned with executable engines (`compile_sdu_lau_generation_spec.py`). |
| `PRODUCT_GOVERNANCE.md` | Release gate: coverage ledger, similarity audit, difficulty governance, purpose validation | Normative Release Gate | Fully aligned with executable validator (`validate_product_governance.py`). |
| `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md` | Upstream Engineering authority boundary, non-authoritative discovery | Normative Engineering Boundary | Fully aligned with `compile_mathematics_engineering_workbench.py`. |
| `ENGINEERING_WORKBENCH.md` | Engineering workbench operational specification, registry IDs, closure | Normative Engineering Workbench | Fully aligned with `policies/mathematics-technical-engineering-gates.v1.json`. |
| `ENGINEERING_DISCOVERY.md` | Non-authoritative discovery layer, vocabulary, candidate ranking, exact selection | Normative Discovery Boundary | Fully aligned with `compile_mathematics_engineering_discovery.py`. |
| `MATHEMATICS_TECHNICAL_ENGINEERING_GATES.md` | Technical specifications for mathematics engineering gates | Normative Gate Specs | Aligned with registry composition. |
| `CANONICAL_ENGINEERING_DOMAIN_ASSETS.md` | Crosswalk from assessment capabilities to canonical domain assets | Normative Asset Catalog | Aligned with `validate_assessment_engineering_crosswalk.py`. |
| `DUAL_TRACK_PRODUCT_MODEL.md` | Dual-track split between study material (SDU) and question material (LAU) | Normative Transitional Contract | Fully aligned with `math-dual-track-product-model.schema.json`. |

---

## 4. Schema Inventory

| Schema File (`contracts/`) | Version | Primary Role | Producer Engine | Validator Engine | Consumer Engine | Maturity | Normative Doc |
|---|---|---|---|---|---|---|---|
| `math-agent-context-manifest.schema.json` | 1.0.0 | Specialist agent isolation context | `run_dual_intelligence.py` | `run_dual_intelligence.py` | Core1/Core2 Specialist | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-assessment-engineering-crosswalk.schema.json` | 1.0.0 | Capability $\to$ Engineering gate crosswalk | Assessment Scope | `validate_assessment_engineering_crosswalk.py` | `engineering_registry_composition.py` | Production | `CANONICAL_ENGINEERING_DOMAIN_ASSETS.md` |
| `math-assimilation-demand-build-spec.schema.json` | 1.0.0 | Spec for building assimilation demand | Pipeline runner | `build_assimilation_demand.py` | `build_assimilation_demand.py` | Production (V1) | `README.md` |
| `math-assimilation-demand.schema.json` | 1.0.0 | Unified demand object post-join | `build_assimilation_demand.py` | `build_assimilation_demand.py` | `compile_assimilation_plan.py` | Production (V1) | `README.md` |
| `math-assimilation-plan-build-spec.schema.json` | 1.0.0 | Spec for assimilation compiler | Pipeline runner | `compile_assimilation_plan.py` | `compile_assimilation_plan.py` | Production (V1) | `README.md` |
| `math-assimilation-plan.schema.json` | 1.0.0 | Compiled teaching and practice plan | `compile_assimilation_plan.py` | `compile_assimilation_plan.py` | Core1A/Core2A Authoring | Production (V1) | `README.md` |
| `math-b-layer-integration.schema.json` | 1.0.0 | B-layer compiler integration contract | B-layer pipeline | `validate_b_layer_integration.py` | Core1B/Core2B engines | Production | `SELF_TEACHING.md` |
| `math-canonical-domain-registry.schema.json` | 1.0.0 | Canonical registry of mathematics assets | `project_engineering_to_domain_registry.py` | `validate_canonical_domain_registry.py` | CDAU / Downstream cores | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-core-coverage-ledger.schema.json` | 1.0.0 | Cross-core asset disposition tracking | `release_product_governance.py` | `validate_product_governance.py` | Product Governance Gate | Production | `PRODUCT_GOVERNANCE.md` |
| `math-core1a-authoring-assets.schema.json` | 1.0.0 | Core1A concept projection candidates | Core1 Authoring | Core1 Authoring | Core1A Renderer | Production | `SELF_TEACHING.md` |
| `math-core1a-family-authoring-assets.schema.json` | 1.0.0 | Core1A problem family candidates | Core1 Authoring | Core1 Authoring | Core1A Renderer | Production | `SELF_TEACHING.md` |
| `math-core2-learner-knowledge-evidence.schema.json` | 1.0.0 | Verified learner percentage evidence | Learner Intake | `compile_sdu_lau_generation_spec.py` | LAU / Core2A / Core2B | Production | `GENERATION_CALIBRATION.md` |
| `math-core2-owner-waiver.schema.json` | 1.0.0 | Owner waiver when % unavailable | Owner Control Plane | `compile_sdu_lau_generation_spec.py` | LAU / Core2A / Core2B | Production | `GENERATION_CALIBRATION.md` |
| `math-cross-core-similarity-audit.schema.json` | 1.0.0 | Pairwise similarity across all 6 Core pairs | `release_product_governance.py` | `validate_product_governance.py` | Product Governance Gate | Production | `PRODUCT_GOVERNANCE.md` |
| `math-cross-validation.schema.json` | 1.0.0 | Claim-level peer validation | `run_dual_intelligence.py` | `run_dual_intelligence.py` | `build_assimilation_demand.py` | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-dual-intelligence-session.schema.json` | 1.0.0 | Sealed dual-specialist session record | `run_dual_intelligence.py` | `run_dual_intelligence.py` | Join layer | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-dual-track-product-model.schema.json` | 1.0.0 | Dual-track product model schema | Blueprint Engine | Blueprint Validator | SDU / LAU compilers | Production | `DUAL_TRACK_PRODUCT_MODEL.md` |
| `math-engineering-domain-projection-v2.schema.json` | 2.0.0 | Engineering to CDR projection v2 | `project_engineering_to_domain_registry_v2.py` | `validate_engineering_domain_projection_binding_v2.py` | CDR | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-engineering-domain-projection.schema.json` | 1.0.0 | Engineering to CDR projection v1 | `project_engineering_to_domain_registry.py` | `validate_engineering_domain_projection_binding.py` | CDR | Legacy / Transition | `CANONICAL_ARCHITECTURE.md` |
| `math-engineering-visibility-manifest.schema.json` | 1.0.0 | Derived Engineering visibility | `compile_engineering_visibility_manifest.py` | `compile_engineering_visibility_manifest.py` | Publication Bundle (Appendix) | Production | `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md` |
| `math-ground-truth-build-spec.schema.json` | 1.0.0 | Build spec for ground truth | Ground Truth Ingestion | `build_ground_truth_manifest.py` | `build_ground_truth_manifest.py` | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-ground-truth-manifest.schema.json` | 1.0.0 | Immutable ground truth evidence | `build_ground_truth_manifest.py` | `blueprint_common.py` | Core0 / Specialist agents | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-learner-capability-state.schema.json` | 1.0.0 | Fine-grained capability state | Learner Evidence | `build_assimilation_demand.py` | LAU | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-learner-page-blueprint.schema.json` | 1.0.0 | Typeset page specification | Core1/Core2 Renderers | `validate_learner_page_blueprint.py` | PDF Renderer | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-learner-publication-bundle.schema.json` | 1.0.0 | Sealed release bundle for publication | `compile_publication_bundle.py` | `validate_publication_bundle.py` | `render_publication_bundle_pdf.py` | Production | `PRODUCT_GOVERNANCE.md` |
| `math-learning-run-blueprint.schema.json` | 1.0.0 | State-machine run manifest | `init_math_learning_run.py` | `blueprint_common.py` | Pipeline orchestrator | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-owner-override-ledger.schema.json` | 1.0.0 | Provenance ledger of owner decisions | Owner Control Plane | `route_math_learning_run.py` | All cores | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-pedagogy-research-manifest.schema.json` | 1.1.0 | Governed research decisions and claims | Research Ingestion | `validate_pedagogy_research_manifest.py` | Core1A / SDU / Publication | Production | `GENERATION_CALIBRATION.md` |
| `math-product-governance-audit.schema.json` | 1.0.0 | Final release governance audit | `release_product_governance.py` | `validate_product_governance.py` | Release Gate | Production | `PRODUCT_GOVERNANCE.md` |
| `math-routing-build-spec.schema.json` | 1.0.0 | Routing build specification | Core0 router | `route_math_learning_run.py` | `route_math_learning_run.py` | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-routing-plan.schema.json` | 1.0.0 | Adaptive routing plan | `route_math_learning_run.py` | `route_math_learning_run.py` | Pipeline runner | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-self-teaching-contract.schema.json` | 1.0.0 | Stage pedagogical contracts | Stage compilers | `validate_self_teaching_contract.py` | Release validation | Production | `SELF_TEACHING.md` |
| `math-self-teaching-generation-spec.schema.json` | 1.0.0 | Generation specification for A/B | Stage compilers | `validate_self_teaching_generation_spec.py` | Authoring engines | Production | `SELF_TEACHING.md` |
| `math-specialist-package.schema.json` | 1.0.0 | Independent specialist analysis | Specialist agent | `run_dual_intelligence.py` | Cross-validation | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-specialist-work-order.schema.json` | 1.0.0 | Task brief for specialist | Core0 router | `run_dual_intelligence.py` | Specialist agent | Production | `CANONICAL_ARCHITECTURE.md` |
| `math-stage-governance-receipt.schema.json` | 1.0.0 | Producer stage admission receipt | `emit_stage_governance.py` | `engineering_product_custody.py` | Release Gate | Production | `PRODUCT_GOVERNANCE.md` |
| `mathematics-engineered-domain-admission.schema.json` | 1.0.0 | Normalized Engineering admission | `compile_mathematics_engineering_workbench.py` | `validate_engineered_domain_admission.py` | CDR / SDU / LAU | Production | `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md` |
| `mathematics-engineering-binding.schema.json` | 1.0.0 | Exact scope-to-gate binding | `compile_mathematics_engineering_workbench.py` | `validate_mathematics_engineering_binding.py` | CDR admission | Production | `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md` |
| `mathematics-engineering-closure-receipt.schema.json` | 1.0.0 | Transitive closure receipt | `compile_mathematics_engineering_workbench.py` | `compile_mathematics_engineering_workbench.py` | CDR admission | Production | `ENGINEERING_WORKBENCH.md` |
| `mathematics-engineering-discovery-receipt.schema.json` | 1.1.0 | Non-authoritative candidate receipt | `compile_mathematics_engineering_discovery.py` | `compile_mathematics_engineering_discovery.py` | Explicit Selection UI | Production | `ENGINEERING_DISCOVERY.md` |
| `mathematics-engineering-discovery-request.schema.json` | 1.0.0 | Discovery search request | Search UI / Agent | `compile_mathematics_engineering_discovery.py` | `compile_mathematics_engineering_discovery.py` | Production | `ENGINEERING_DISCOVERY.md` |
| `mathematics-engineering-discovery-selection.schema.json` | 1.0.0 | Explicit selection of exact ID | User / Tooling | `compile_mathematics_engineering_discovery.py` | Engineering Resolver | Production | `ENGINEERING_DISCOVERY.md` |
| `mathematics-engineering-discovery-vocabulary.schema.json` | 1.0.0 | Governed vocabulary catalog | Vocabulary author | `validate_mathematics_engineering_discovery_vocabulary.py` | Discovery Compiler | Production | `ENGINEERING_DISCOVERY.md` |
| `mathematics-engineering-manifest.schema.json` | 1.0.0 | Resolved Engineering manifest | `compile_mathematics_engineering_workbench.py` | `compile_mathematics_engineering_workbench.py` | Closure compiler | Production | `ENGINEERING_WORKBENCH.md` |
| `mathematics-engineering-request.schema.json` | 1.0.0 | Authoritative Engineering request | Workbench / Selection | `compile_mathematics_engineering_workbench.py` | `compile_mathematics_engineering_workbench.py` | Production | `ENGINEERING_WORKBENCH.md` |
| `mathematics-technical-engineering-gate.schema.json` | 1.0.0 | Canonical gate schema | Engineering author | `validate_mathematics_engineering_gates.py` | Composition & Workbench | Production | `MATHEMATICS_TECHNICAL_ENGINEERING_GATES.md` |

---

## 5. Policy Inventory

| Policy File (`policies/`) | Policy Identifier | Stated Role | Primary Consumer Engine | Primary Validator Engine | Status |
|---|---|---|---|---|---|
| `math-assessment-engineering-crosswalk.mixed-grade9.v1.json` | `MATH-ASSESSMENT-ENG-XWALK-MIXED-G9-V1` | Assessment capability to Gate crosswalk | `engineering_registry_composition.py` | `validate_assessment_engineering_crosswalk.py` | CURRENT |
| `math-assessment-engineering-crosswalk.mixed-grade9.v2.patch.json` | Derived patch | Assessment crosswalk v2 patch | `validate_assessment_engineering_crosswalk.py` | `validate_assessment_engineering_crosswalk.py` | CURRENT |
| `math-assimilation-compiler-policy.json` | `MATH-ASSIMILATION-COMPILER-v1` | Core1A assimilation compiler rules | `compile_assimilation_plan.py` | `compile_assimilation_plan.py` | TRANSITIONAL |
| `math-assimilation-join-policy.json` | `MATH-ASSIMILATION-JOIN-v1` | Join thresholds and conflict rules | `build_assimilation_demand.py` | `build_assimilation_demand.py` | TRANSITIONAL |
| `math-b-layer-integration-policy.json` | `MATH-B-LAYER-INTEGRATION-v2` | B-layer tutor compilation rules | B-layer compiler | `validate_b_layer_integration.py` | CURRENT |
| `math-canonical-domain-registry-policy.json` | `MATH-CANONICAL-DOMAIN-REGISTRY-v1` | Asset admission & uniqueness rules | CDR projection | `validate_canonical_domain_registry.py` | CURRENT |
| `math-cross-core-similarity-policy.json` | `MATH-CROSS-CORE-SIMILARITY-v1` | Pairwise similarity thresholds | `release_product_governance.py` | `validate_product_governance.py` | CURRENT |
| `math-dual-intelligence-policy.json` | `MATH-DUAL-INTELLIGENCE-v1` | Specialist independence rules | `run_dual_intelligence.py` | `run_dual_intelligence.py` | CURRENT |
| `math-evidence-routing-policy.json` | `MATH-EVIDENCE-ROUTING-v1` | Core0 routing priority rules | `route_math_learning_run.py` | `route_math_learning_run.py` | CURRENT |
| `math-evidence-state-policy.json` | `MATH-EVIDENCE-STATE-v1` | Ground truth evidence classifications | `blueprint_common.py` | `blueprint_common.py` | CURRENT |
| `math-self-teaching-policy.json` | `MATH-SELF-TEACHING-v1` | Self-teaching stage rules | Stage compilers | `validate_self_teaching_generation_spec.py` | CURRENT |
| `math-technical-composition-policy.json` | `MATH-TECHNICAL-COMPOSITION-v1` | Page layout & composition rules | Page compilers | `validate_learner_page_blueprint.py` | CURRENT |
| `mathematics-engineering-depth-policy.v1.json` | `MATH-ENGINEERING-DEPTH-V1` | FOUNDATION/STANDARD/RESEARCH depth | `compile_mathematics_engineering_workbench.py` | `compile_mathematics_engineering_workbench.py` | CURRENT |
| `mathematics-engineering-discovery-vocabulary.v1.json` | `REG-MATH-TECH-GATE-V1` (catalog) | Governed aliases and search phrases | `compile_mathematics_engineering_discovery.py` | `validate_mathematics_engineering_discovery_vocabulary.py` | CURRENT |
| `mathematics-engineering-extension-catalog.v1.json` | `REG-MATH-TECH-GATE-EXTENSIONS-V1` | Engineering extension file ledger | `engineering_registry_composition.py` | `validate_mathematics_engineering_gates.py` | CURRENT |
| `mathematics-engineering-gate-invariants.v1.json` | Generic invariant definitions | Invariant categories for gates | Workbench & composition | `validate_mathematics_engineering_gates.py` | CURRENT |
| `mathematics-technical-engineering-gates.v1.euclid-extension.json` | Euclid gate extension | Extension data for Euclid gate | Extension composition | `validate_mathematics_engineering_gates.py` | CURRENT |
| `mathematics-technical-engineering-gates.v1.json` | `REG-MATH-TECH-GATE-V1` | Base 45-gate Engineering registry | Workbench & compiler | `validate_mathematics_engineering_gates.py` | CURRENT |

---

## 6. Validator / Producer / Consumer Matrix

```text
[Schema / Contract]                  [Producer]                                  [Validator]                                 [Consumer]
mathematics-technical-engineering-gate  Engineering Author                         validate_mathematics_engineering_gates.py   Workbench / Composition
mathematics-engineering-discovery-*   User Query / compile_math_discovery.py      compile_mathematics_engineering_discovery   Explicit Selection UI
mathematics-engineering-request       Explicit Selection / Workbench User         compile_mathematics_engineering_workbench   resolve_manifest()
mathematics-engineering-closure       compile_mathematics_engineering_workbench   compile_mathematics_engineering_workbench   Engineering Admission
mathematics-engineering-binding       compile_mathematics_engineering_workbench   validate_mathematics_engineering_binding    Canonical Domain Registry
math-canonical-domain-registry        project_engineering_to_domain_registry_v2   validate_canonical_domain_registry.py       CDAU / Downstream Cores
math-pedagogy-research-manifest       Research Process                            validate_pedagogy_research_manifest.py      Core1A Authoring / Release
math-core2-learner-knowledge-evidence Diagnostic / Intake                         compile_sdu_lau_generation_spec.py          LAU / Core2A / Core2B
math-core2-owner-waiver               Owner Control Plane                         compile_sdu_lau_generation_spec.py          LAU / Core2A / Core2B
math-product-governance-audit         release_product_governance.py               validate_product_governance.py              Release Gate
math-engineering-visibility-manifest  compile_engineering_visibility_manifest     compile_engineering_visibility_manifest     Publication Bundle
math-learner-publication-bundle       compile_publication_bundle.py               validate_publication_bundle.py              render_publication_bundle_pdf
```

---

## 7. Contradiction Register

### Finding DRIFT-01
- **Classification**: `DOCUMENT_STALE`
- **Status**: `RESOLVED` (Updated `README.md` to establish `CANONICAL_ARCHITECTURE.md` as canonical root and marked single-track assimilation pipeline as transitional)
- **Subject**: Blueprint Topology Overview
- **Source A**: `README.md` (Lines 15–40) presenting single-track `AssimilationDemand` $\to$ `AssimilationPlan` as the primary topology.
- **Source B**: `CANONICAL_ARCHITECTURE.md` (Lines 10–65) establishing Six-Core Architecture (Ground Truth $\to$ Core0 $\to$ Core1/Core2 $\to$ CDR $\to$ CDAU $\to$ SDU/LAU $\to$ TTU $\to$ Publication).
- **Executable Authority**: Both single-track (`compile_assimilation_plan.py`) and dual-track (`compile_sdu_lau_generation_spec.py`, `DUAL_TRACK_PRODUCT_MODEL.md`) engines exist.
- **Why they differ**: `README.md` was authored during early V2 Math development and was not refreshed when the canonical target architecture was formalized.
- **Operational Consequence**: New developers and agents reading `README.md` may build single-track assimilation pipelines instead of the governed SDU/LAU dual-track structure.
- **Severity**: `HIGH`
- **Resolution**: Updated `README.md` with the canonical Six-Core Architecture diagram, linking `CANONICAL_ARCHITECTURE.md` and subordinate modules, and designating single-track assimilation as transitional V1.

### Finding DRIFT-02
- **Classification**: `DOCUMENT_AMBIGUITY`
- **Status**: `RESOLVED` (Standardized across `CANONICAL_ARCHITECTURE.md`, `PEDAGOGY_AND_CALIBRATION.md`, `DUAL_TRACK_PRODUCT_MODEL.md`, `PRODUCT_GOVERNANCE.md`, and `README.md`)
- **Subject**: EASY Pedagogy Research Phrasing
- **Source A**: `PRODUCT_GOVERNANCE.md` Section 3 ("pedagogy-enrichment web research OPTIONAL... optional EASY research may be omitted. If used, brief and references must be fully bound").
- **Source B**: `GENERATION_CALIBRATION.md` Section 2 ("pedagogy-enrichment web research is optional, not prohibited... remain at the subtopic level").
- **Source C**: Historical fragments in conversational memory suggesting research was prohibited for EASY.
- **Executable Authority**: `validate_pedagogy_research_manifest.py` permits research for any difficulty, but checks that if claims exist, custody and contradiction resolution are complete. `compile_sdu_lau_generation_spec.py` does not require research for EASY.
- **Why they differ**: Nuance between "default absent" and "prohibited".
- **Operational Consequence**: Minor confusion for research agents wondering if they should block or allow optional web research for foundational topics.
- **Severity**: `MEDIUM`
- **Resolution**: Standardized phrasing across all documents: *"EASY difficulty: Web research is default absent / optional, never prohibited. If used, full claim and source custody is required."*

### Finding DRIFT-03
- **Classification**: `NORMATIVE_CONTRADICTION`
- **Subject**: Engineering Domain Projection Schema Versions
- **Source A**: `contracts/math-engineering-domain-projection.schema.json` (v1.0.0) used by `project_engineering_to_domain_registry.py`.
- **Source B**: `contracts/math-engineering-domain-projection-v2.schema.json` (v2.0.0) used by `project_engineering_to_domain_registry_v2.py`.
- **Executable Authority**: Both versions exist and both have passing tests (`test_engineering_domain_projection.py` and `test_engineering_domain_projection_v2.py`).
- **Why they differ**: V2 was introduced to add richer capability and equation mappings without deleting V1.
- **Operational Consequence**: Two parallel projection paths exist in `engine/`.
- **Severity**: `MEDIUM`
- **Recommended Action**: Document V1 as `LEGACY_TRANSITIONAL` and formalize V2 as normative.

---

## 8. Stale-Document Register

| Document | Outdated Sections | Current Replacement / Truth | Recommended Action |
|---|---|---|---|
| `README.md` | Single-track assimilation diagram (lines 15–40) | `CANONICAL_ARCHITECTURE.md` Section 1 | Rebase diagram to 6-core topology. |
| `TECHNICAL_COMPOSITION.md` | Old layout references lacking B-layer tutor specifics | `SELF_TEACHING.md` and `contracts/math-b-layer-integration.schema.json` | Add cross-reference to B-layer tutor dialogue contract. |
| `policies/math-assimilation-compiler-policy.json` | Assimilation plan token counts based on old single-core generation | `DUAL_TRACK_PRODUCT_MODEL.md` | Mark policy as `TRANSITIONAL_V1`. |

---

## 9. Duplicate-Doctrine Register

| Doctrine / Concept | Files Where Defined | Primary Canonical Source | Recommendation |
|---|---|---|---|
| A/B Stage Meaning (A = Complete, B = Reconstructive) | `CANONICAL_ARCHITECTURE.md`, `SELF_TEACHING.md`, `DUAL_TRACK_PRODUCT_MODEL.md` | `CANONICAL_ARCHITECTURE.md` Section 10 | Centralize in `CANONICAL_ARCHITECTURE.md`; other docs reference it. |
| Page Ceiling Rules (EASY $\le$ 10, MEDIUM $\le$ 20, HARD $\le$ 30) | `GENERATION_CALIBRATION.md`, `PRODUCT_GOVERNANCE.md`, `CANONICAL_ARCHITECTURE.md` | `GENERATION_CALIBRATION.md` Section 2 | Declare `GENERATION_CALIBRATION.md` as sole authority. |
| Authority Direction (Discovery $\to$ Selection $\to$ Resolver $\to$ Closure) | `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md`, `ENGINEERING_DISCOVERY.md`, `ENGINEERING_WORKBENCH.md` | `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md` | Clarify roles: Authority doc owns boundary; Workbench doc owns operation; Discovery doc owns candidate ranking. |

---

## 10. Unowned-Invariant Register

| Observed System Invariant | Currently Documented In | Code Location | Status / Owner Action Required |
|---|---|---|---|
| Discovery Candidate Count Default = 6 | Unclear / Implied | `compile_mathematics_engineering_discovery.py` (`max_candidates=6`) | Formalize in `ENGINEERING_DISCOVERY.md`. |
| Crosswalk Capability Format (`G9-MATH-...`) | Assessment scope policy | `validate_assessment_engineering_crosswalk.py` | Owned by Assessment Authority. |
| Research Evidence Classes (`VERIFIED_WEB_CAPTURE` vs `TEST_FIXTURE`) | Schema only | `contracts/math-pedagogy-research-manifest.schema.json` | Document in `GENERATION_CALIBRATION.md`. |

---

## 11. Missing Limitations & Risk Register

1. **Human Topic Ambiguity in Competitive Exams**:
   - *Risk*: A Grade 9/10 student asks for "Roots", which spans Quadratic Equations, Theory of Equations, Complex Numbers, and Approximation Methods (Newton-Raphson).
   - *Current Control*: `compile_mathematics_engineering_discovery.py` returns multiple candidates with ranks and scores, requiring explicit selection.
   - *Recommendation*: Preserve `AMBIGUITY_PRESERVATION_RATE` in benchmarks.
2. **Diagnostic Coarseness of Learner Knowledge Percentage**:
   - *Risk*: A reported 70% knowledge does not reveal whether the learner has mastered Vieta's formulas but struggles with parameter intervals in location of roots.
   - *Current Control*: `math-core2-learner-knowledge-evidence.schema.json` requires `capability_knowledge[]` breaking down percentages per capability.
3. **Research Evidence Freshness & Web Drift**:
   - *Risk*: URLs referenced in research dossiers may change or become unreachable.
   - *Current Control*: `capture_digest` (SHA-256) binds the evidence to exact captured text.
4. **Schema Proliferation**:
   - *Risk*: 45 separate schemas create maintenance overhead.
   - *Current Control*: Automated validation test suites.

---

## 12. Verification of Known High-Risk Drift Areas

| High-Risk Question | Executable Code State | Documented Claim | Verified Drift / Conclusion |
|---|---|---|---|
| **EASY pedagogy research: forbidden or optional?** | Optional in validator (`validate_pedagogy_research_manifest.py`); default absent in generation spec. | Optional in `GENERATION_CALIBRATION.md` and `PRODUCT_GOVERNANCE.md`. | **ALIGNED**: Optional, default absent, never prohibited. If used, must be fully bound. |
| **MEDIUM/HARD research: what is mandatory?** | Validated brief, explicit claim coverage, support/contradiction stance, and contradiction resolution. | Mandatory in `GENERATION_CALIBRATION.md` and `PRODUCT_GOVERNANCE.md`. | **ALIGNED**: Strict claim-level custody mandatory. |
| **Source-count rules: minimum required?** | Zero minimum source-count check in validator. | "No universal minimum source-count quota" in `PRODUCT_GOVERNANCE.md` & `GENERATION_CALIBRATION.md`. | **ALIGNED**: Quality & claim support over quota. |
| **Knowledge percentage: which cores consume it?** | Consumed by `compile_sdu_lau_generation_spec.py` for Core2A/Core2B only. | Explicitly prohibited from Core1A/Core1B in `CANONICAL_ARCHITECTURE.md`. | **ALIGNED**: SDU never consumes learner knowledge %. |
| **Core1 depth: can learner % affect it?** | Prohibited by validator in `validate_product_governance.py`. | SDU MUST NOT inspect learner knowledge % in `CANONICAL_ARCHITECTURE.md`. | **ALIGNED**: Hard invariant holds. |
| **Engineering discovery: can aliases authorize?** | `compile_mathematics_engineering_discovery.py` sets `automatic_selection=False`. Resolver rejects unmapped scopes. | Normative rule in `ENGINEERING_DISCOVERY.md`. | **ALIGNED**: Aliases never authorize. |
| **Publication semantic source?** | Bundle-only in `compile_publication_bundle.py`. | `semantic_source = LEARNER_PUBLICATION_BUNDLE_ONLY` in PR 351. | **ALIGNED**: Renderer never authors mathematics. |
| **Engineering visibility authority?** | `publication_authorization = NOT_IMPLIED` in schema. | Appendix view only; publication authority not implied in `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md`. | **ALIGNED**: Visibility $\ne$ publication authorization. |
| **Canonical architecture reflects latest discovery?** | Discovery is documented as upstream non-authoritative boundary in Section 1. | Fully reflected in `CANONICAL_ARCHITECTURE.md`. | **ALIGNED**: Upstream boundary clear. |
| **Target architecture vs implemented separated?** | Section 25 explicitly notes target architecture and migration rules. | `CANONICAL_ARCHITECTURE.md` Section 25. | **ALIGNED**: Clear migration separation. |

---

## 13. Architecture-Catalog Recommendation

To prevent future drift and manual diagram decay, we recommend establishing a **Machine-Generated Architecture Catalog** based on Task B's `generate_architecture_manifest.py`:
1. **Automated Manifest Generation**: An AST-based crawler that extracts schemas, policies, producers, validators, consumers, and test links.
2. **Schema Metadata Integration**: Enriching every schema with `$defs` documentation, producer tag, and owning authority domain.
3. **Continuous Catalog Verification**: Running catalog generation in CI to ensure no orphan schemas or undocumented validators exist.

---

## 14. Core-Spec Consolidation Recommendation

We recommend consolidating the 11+ normative documents into a single unified specification structure:

```text
CANONICAL SPECIFICATION ROOT:
Grade 9/V2/Mathematics/MathBlueprint/CANONICAL_ARCHITECTURE.md

SUBORDINATE NORMATIVE MODULES (Strictly bounded):
1. ENGINEERING_AUTHORITY.md  (Consolidating ENGINEERING_GATE_BLUEPRINT_AUTHORITY,
                             ENGINEERING_WORKBENCH, ENGINEERING_DISCOVERY)
2. PEDAGOGY_AND_CALIBRATION.md (Consolidating SELF_TEACHING, GENERATION_CALIBRATION,
                                DUAL_TRACK_PRODUCT_MODEL)
3. PRODUCT_GOVERNANCE_GATE.md  (PRODUCT_GOVERNANCE)

GENERATED TECHNICAL REFERENCES:
- Generated Architecture Catalog (from Task B)
- Governed Engineering Registry Specification (from registry JSON)
- Governed Discovery Vocabulary Reference (from vocabulary JSON)

DEPRECATED / RETIRED UPON CONSOLIDATION:
- README.md (replace with clean gateway pointing to CANONICAL_ARCHITECTURE.md)
- Old assimilation single-track notes
```

---

## 15. Items Requiring Owner Decision vs. Safe Mechanical Fixes

### Items Requiring Owner Decision
1. **Formal Deprecation Timeline for V1 Single-Track Assimilation**: Setting the milestone when `math-assimilation-demand.schema.json` and `compile_assimilation_plan.py` will be retired in favor of the SDU/LAU six-core pipeline.
2. **Migration from Projection V1 to V2**: Formalizing `math-engineering-domain-projection-v2.schema.json` as the sole canonical domain projection.
3. **Engineering Extension Lifecycle**: Defining whether future extensions (e.g. Euclidean geometry, coordinate geometry) should remain as separate files or merge into the base registry during releases.

### Items Safe to Fix Mechanically
1. Refreshing `README.md` to point directly to `CANONICAL_ARCHITECTURE.md`.
2. Standardizing phrasing on EASY pedagogy research ("default absent, optional, not prohibited; if used, full custody required") across all documents.
3. Adding missing schema `title` properties in `contracts/mathematics-engineering-*.schema.json`.

---

## 16. Recommended Migration Sequence

1. **Phase 1 (Current)**: Observability, run configuration tooling, discovery quality benchmarking, and drift auditing. (Zero production code edits).
2. **Phase 2 (Owner Decision & Core Spec Consolidation)**: Consolidate normative documents under `CANONICAL_ARCHITECTURE.md`; retire redundant V1 single-track docs.
3. **Phase 3 (Subtopic Intelligence Library Intake)**: Ingest mathematics subtopic knowledge packets using the validated SDU/LAU pipelines.

---

## 17. Academician Pedagogical Alignment Matrix (Grades 9–11 Competitive Exams)

As an expert academician preparing secondary and senior-secondary students for premier mathematical competitions (IIT-JEE Main & Advanced, IOQM, RMO), conceptual assimilation requires an uncompromising match between mathematical rigor and cognitive progression:

```text
COMPETITIVE LEVEL          CORE EMPHASIS                      GOVERNED BLUEPRINT CONSTRUCT
-----------------          -------------                      ----------------------------
CBSE / ICSE Board (9-10)   Deductive proofs & mechanics       Core1A SDU (Declarative Self-Teaching)
IOQM / Olympiad (9-11)     Synthetic geometry & Number Theory Core1B SDU + TTU Incomplete Proofs
JEE Main (11)              Alg. Manipulation & Calculus       Core2A LAU (Expert Solution Anatomy)
JEE Advanced (11)          Multi-concept synthesis & bounds   Core2B LAU (Open-ended Transfer Tutoring)
```

### Detailed Exam Rigor Mapping

| Exam Domain | Key Mathematical Milestones | Common Learner Failure Modes | MathBlueprint Pedagogical Invariant |
|---|---|---|---|
| **Board Foundations** (CBSE/ICSE) | Euclidean proofs, linear systems consistency ($a_1/a_2$), factor theorem. | Sign errors, premature division by variable, confusing lines with line segments. | Core1A SDU locks exact algebraic steps; prohibits skipped reasoning steps; enforces $|x| = \sqrt{x^2}$. |
| **IOQM / Olympiad** | Basic Proportionality Theorem (Thales), cyclic quadrilaterals, Euclid's lemma, Vieta relations. | Memorizing formulas without synthetic proof; failing to spot auxiliary constructions. | Reconstructable TTUs present incomplete geometric figures and proof scaffolds requiring active learner reconstruction. |
| **JEE Main** | Quadratic discriminant trichotomy, common roots, standard conics ($y^2 = 4ax$), standard limits. | Applying formulas outside valid parameter intervals; forgetting leading coefficient $a \neq 0$. | Engineering Gates enforce non-negotiable preconditions upstream of task generation. |
| **JEE Advanced** | Location of roots, complex polar/Euler forms, composite function derivatives, Bayes' theorem. | Inability to transfer across concepts (e.g. geometric locus with complex variables). | Core2B LAU transfer demand enforces structural variation without altering frozen source questions. |

Through this formal separation, MathBlueprint guarantees that theoretical clarity is never diluted by diagnostic scores, while exam-specific problem solving is rigorously calibrated.

