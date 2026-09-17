# Mathematics Architecture Generated References

> **Status: DESIGN / NON-NORMATIVE / GENERATED**
>
> This file is a derived reference view. It cannot authorize runtime behavior, mathematical truth, component maturity, release state or publication. Regenerate it only from the C1 architecture catalog using the C3 generator.

- Source catalog Git blob: `469f1eaaf671fd274dcb5c332b4b73e1ac01b0bd`
- Source catalog schema Git blob: `b335ef39a7971eafdc464a5f759e11380bfbcfae`
- C2 receipt Git blob: `785fe5e5ac3e203ab04838e6be0b7914c6f4cec4`
- Generator Git blob: `fc55f28b2199ffd5458cf5cd963de96834a38a48`
- Components: **17**
- Authority: `NONE`
- Publication authorization: `NOT_IMPLIED`

## Architecture components

| Component | Role | Primary class | Runtime effect | Publication effect |
|---|---|---|---|---|
| MATH-ARCH-ASSESSMENT-ENGINEERING-BRIDGE | SCOPE_BRIDGE | GOVERNED_POLICY | CURRENT_EXECUTABLE_AUTHORITY | NONE |
| MATH-ARCH-DESIGN-NON-AUTHORITY-GUARD | CI_GUARD | CI_GUARD | EXECUTABLE_ORCHESTRATION_ONLY | NONE |
| MATH-ARCH-DESIGN-WORKSPACE | DESIGN_WORKSPACE | DESIGN_ONLY | NONE_DESIGN_ONLY | NONE |
| MATH-ARCH-DOMAIN-PROJECTION | DOMAIN_PROJECTION | PRODUCTION_COMPILER | EXECUTABLE_ORCHESTRATION_ONLY | NONE |
| MATH-ARCH-ENGINEERING-CUSTODY | RUNTIME_CUSTODY | SCHEMA_CONTRACT | CURRENT_EXECUTABLE_AUTHORITY | NONE |
| MATH-ARCH-ENGINEERING-DISCOVERY | NON_AUTHORITATIVE_DISCOVERY | DERIVED_NON_AUTHORITATIVE_VIEW | DERIVED_NON_AUTHORITATIVE | NOT_IMPLIED |
| MATH-ARCH-ENGINEERING-REGISTRY | SUBJECT_AUTHORITY | AUTHORITATIVE_DATA | CURRENT_EXECUTABLE_AUTHORITY | NONE |
| MATH-ARCH-ENGINEERING-VALIDATION | POLICY_AND_VALIDATION | PRODUCTION_VALIDATOR | CURRENT_EXECUTABLE_AUTHORITY | NONE |
| MATH-ARCH-ENGINEERING-VISIBILITY | DERIVED_VISIBILITY | DERIVED_NON_AUTHORITATIVE_VIEW | DERIVED_NON_AUTHORITATIVE | NOT_IMPLIED |
| MATH-ARCH-ENGINEERING-WORKBENCH | EXACT_AUTHORIZATION | PRODUCTION_COMPILER | CURRENT_EXECUTABLE_AUTHORITY | NONE |
| MATH-ARCH-PEDAGOGY-RESEARCH | PEDAGOGY_EVIDENCE | SCHEMA_CONTRACT | CURRENT_EXECUTABLE_AUTHORITY | NONE |
| MATH-ARCH-PRODUCER-GOVERNANCE | PRODUCER | PRODUCER | EXECUTABLE_ORCHESTRATION_ONLY | NONE |
| MATH-ARCH-PUBLICATION | PUBLICATION_BOUNDARY | PUBLICATION_BOUNDARY | CURRENT_EXECUTABLE_AUTHORITY | RELEASE_GATED_PUBLICATION_BOUNDARY |
| MATH-ARCH-ROUTING-ASSIMILATION | ORCHESTRATION | PRODUCTION_COMPILER | EXECUTABLE_ORCHESTRATION_ONLY | NONE |
| MATH-ARCH-SELF-TEACHING-CALIBRATION | CALIBRATION | GOVERNED_POLICY | CURRENT_EXECUTABLE_AUTHORITY | NONE |
| MATH-ARCH-STAGE-RELEASE | RELEASE_GATE | RELEASE_GATE | CURRENT_EXECUTABLE_AUTHORITY | RELEASE_GATED_PUBLICATION_BOUNDARY |
| MATH-ARCH-TOPIC-INDEPENDENCE-GUARD | CI_GUARD | CI_GUARD | EXECUTABLE_ORCHESTRATION_ONLY | NONE |

## Schemas

Count: **24**

| Component | Repository path |
|---|---|
| MATH-ARCH-ASSESSMENT-ENGINEERING-BRIDGE | `contracts/math-assessment-engineering-crosswalk.schema.json` |
| MATH-ARCH-DOMAIN-PROJECTION | `contracts/math-canonical-domain-registry.schema.json` |
| MATH-ARCH-DOMAIN-PROJECTION | `contracts/math-engineering-domain-projection-v2.schema.json` |
| MATH-ARCH-ENGINEERING-CUSTODY | `contracts/mathematics-engineering-binding.schema.json` |
| MATH-ARCH-ENGINEERING-DISCOVERY | `contracts/mathematics-engineering-discovery-receipt.schema.json` |
| MATH-ARCH-ENGINEERING-DISCOVERY | `contracts/mathematics-engineering-discovery-request.schema.json` |
| MATH-ARCH-ENGINEERING-DISCOVERY | `contracts/mathematics-engineering-discovery-selection.schema.json` |
| MATH-ARCH-ENGINEERING-DISCOVERY | `contracts/mathematics-engineering-discovery-vocabulary.schema.json` |
| MATH-ARCH-ENGINEERING-REGISTRY | `contracts/mathematics-technical-engineering-gate.schema.json` |
| MATH-ARCH-ENGINEERING-VISIBILITY | `contracts/math-engineering-visibility-manifest.schema.json` |
| MATH-ARCH-ENGINEERING-WORKBENCH | `contracts/mathematics-engineering-closure-receipt.schema.json` |
| MATH-ARCH-ENGINEERING-WORKBENCH | `contracts/mathematics-engineering-manifest.schema.json` |
| MATH-ARCH-ENGINEERING-WORKBENCH | `contracts/mathematics-engineering-request.schema.json` |
| MATH-ARCH-PEDAGOGY-RESEARCH | `contracts/math-pedagogy-research-manifest.schema.json` |
| MATH-ARCH-PRODUCER-GOVERNANCE | `contracts/math-b-layer-integration.schema.json` |
| MATH-ARCH-PRODUCER-GOVERNANCE | `contracts/math-core1a-authoring-assets.schema.json` |
| MATH-ARCH-PUBLICATION | `contracts/math-learner-publication-bundle.schema.json` |
| MATH-ARCH-ROUTING-ASSIMILATION | `contracts/math-assimilation-plan.schema.json` |
| MATH-ARCH-ROUTING-ASSIMILATION | `contracts/math-dual-intelligence-session.schema.json` |
| MATH-ARCH-ROUTING-ASSIMILATION | `contracts/math-routing-plan.schema.json` |
| MATH-ARCH-SELF-TEACHING-CALIBRATION | `contracts/math-self-teaching-contract.schema.json` |
| MATH-ARCH-SELF-TEACHING-CALIBRATION | `contracts/math-self-teaching-generation-spec.schema.json` |
| MATH-ARCH-STAGE-RELEASE | `contracts/math-product-governance-audit.schema.json` |
| MATH-ARCH-STAGE-RELEASE | `contracts/math-stage-governance-receipt.schema.json` |

## Policies

Count: **11**

| Component | Repository path |
|---|---|
| MATH-ARCH-ASSESSMENT-ENGINEERING-BRIDGE | `policies/math-assessment-engineering-crosswalk.mixed-grade9.v1.json` |
| MATH-ARCH-ASSESSMENT-ENGINEERING-BRIDGE | `policies/math-assessment-engineering-crosswalk.mixed-grade9.v2.patch.json` |
| MATH-ARCH-DOMAIN-PROJECTION | `policies/math-canonical-domain-registry-policy.json` |
| MATH-ARCH-ENGINEERING-DISCOVERY | `policies/mathematics-engineering-discovery-vocabulary.v1.json` |
| MATH-ARCH-ENGINEERING-REGISTRY | `policies/mathematics-engineering-extension-catalog.v1.json` |
| MATH-ARCH-ENGINEERING-REGISTRY | `policies/mathematics-technical-engineering-gates.v1.json` |
| MATH-ARCH-ENGINEERING-VALIDATION | `policies/mathematics-engineering-depth-policy.v1.json` |
| MATH-ARCH-ENGINEERING-VALIDATION | `policies/mathematics-engineering-gate-invariants.v1.json` |
| MATH-ARCH-ROUTING-ASSIMILATION | `policies/math-dual-intelligence-policy.json` |
| MATH-ARCH-ROUTING-ASSIMILATION | `policies/math-evidence-routing-policy.json` |
| MATH-ARCH-SELF-TEACHING-CALIBRATION | `policies/math-self-teaching-policy.json` |

## Validators

Count: **10**

| Component | Repository path |
|---|---|
| MATH-ARCH-ASSESSMENT-ENGINEERING-BRIDGE | `engine/validate_assessment_engineering_crosswalk.py` |
| MATH-ARCH-DOMAIN-PROJECTION | `engine/validate_engineering_domain_projection_binding_v2.py` |
| MATH-ARCH-ENGINEERING-CUSTODY | `engine/validate_mathematics_engineering_binding.py` |
| MATH-ARCH-ENGINEERING-DISCOVERY | `engine/validate_mathematics_engineering_discovery_vocabulary.py` |
| MATH-ARCH-ENGINEERING-VALIDATION | `engine/validate_mathematics_engineering_gates.py` |
| MATH-ARCH-PEDAGOGY-RESEARCH | `engine/validate_pedagogy_research_manifest.py` |
| MATH-ARCH-PRODUCER-GOVERNANCE | `engine/validate_b_layer_integration.py` |
| MATH-ARCH-PUBLICATION | `engine/validate_publication_bundle.py` |
| MATH-ARCH-SELF-TEACHING-CALIBRATION | `engine/validate_self_teaching_generation_spec.py` |
| MATH-ARCH-STAGE-RELEASE | `engine/validate_product_governance.py` |

## Tests

Count: **2**

| Component | Repository path |
|---|---|
| MATH-ARCH-DESIGN-NON-AUTHORITY-GUARD | `tests/test_design_authority_boundary.py` |
| MATH-ARCH-TOPIC-INDEPENDENCE-GUARD | `tests/test_blueprint_topic_independence.py` |

## Non-authority boundary

These tables are observability only. They do not promote a design component, alter a governed policy, select an Engineering identity, satisfy a validator, authorize a producer, pass a release gate or imply publication authority.

C0-F007 remains `CURRENT + DOCUMENTED ONLY`; C3 does not make optional EASY-research auto-materialization executable.
