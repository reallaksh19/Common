# Subtopic Intelligence Library — Draft Schema Family and Validation Invariants

> **Status: DESIGN / NON-NORMATIVE / NOT A CONTRACT**
>
> This document translates the SIL roadmap into a field-level schema design before any production JSON Schema is added under `contracts/`. Names, enums and shapes remain reviewable. Existing Mathematics authority remains unchanged.

## 1. Design objective

The schema family must make a mature subtopic reproducible for an average cold-start agent while preserving authority separation.

The schema design must make these mistakes structurally difficult:

```text
copying subject truth into the library;
confusing a teaching preference with a logical prerequisite;
turning a source recommendation into subject authority;
turning learner knowledge into curriculum scope;
turning a question-bank hit into assessment authority;
letting a stale pack survive changed canonical dependencies;
using human labels where exact canonical refs are required.
```

## 2. Authority classes inside the library

The SIL must distinguish at least these classes of assertion:

```text
EXACT_SUBJECT_REFERENCE
    pointer to existing governed subject/domain authority

EXACT_SCOPE_REFERENCE
    pointer to existing curriculum/exam/owner scope authority

LEARNING_STRUCTURE
    governed sequencing/transition metadata about exact objects

SOURCE_SELECTION
    governed reason a source is suitable for a role/context

PEDAGOGY_EVIDENCE_REFERENCE
    pointer to separately governed research claims/decisions

ASSESSMENT_REFERENCE
    pointer to exact problem-family/question/capability authority

DERIVED_COVERAGE
    generated audit state; never authority

OWNER_DECISION_REFERENCE
    exact owner override/decision; never rewritten as historical truth
```

No free-text field can upgrade itself to another authority class.

## 3. Critical distinction: prerequisite is not one relation

The final schema must never expose a single ambiguous `prerequisite: true` flag.

At least these dependency classes must be distinguishable:

### 3.1 `LOGICAL_DEPENDENCY`

Meaning:

```text
the target subject object logically depends on another subject object
```

Authority owner:

```text
SUBJECT / ENGINEERING
```

The SIL may reference this relation but must not invent it.

### 3.2 `ASSESSMENT_CAPABILITY_DEPENDENCY`

Meaning:

```text
a problem family / question requires a capability
```

Authority owner:

```text
CORE2 / assessment domain
```

Again, SIL composes exact refs.

### 3.3 `INSTRUCTIONAL_SEQUENCE`

Meaning:

```text
for this teaching context, object A should normally be taught/reconstructed
before object B
```

Authority owner:

```text
LEARNING STRUCTURE / pedagogy governance
```

This may be evidence-backed and context-specific. It does not rewrite mathematical dependency.

### 3.4 `REPRESENTATION_BRIDGE`

Meaning:

```text
a learner must coordinate two representations to make the target transition
```

Authority owner:

```text
subject representation identities + governed learning structure
```

### 3.5 `REPAIR_SEQUENCE`

Meaning:

```text
a diagnostic failure should route through a bounded repair transition
```

Authority owner:

```text
learning structure / pedagogy
```

A future validator must reject attempts to encode an `INSTRUCTIONAL_SEQUENCE` record as proof of `LOGICAL_DEPENDENCY`.

## 4. Shared primitive: exact reference envelope

Where a schema points to an external governed object, prefer a typed exact-reference envelope rather than an untyped string when cross-subject scale requires it.

Draft:

```text
ref
ref_type
subject_id
registry_ref
registry_version_or_digest
```

Potential `ref_type` examples:

```text
SUBJECT_GATE
CANONICAL_ASSET
CAPABILITY
SCOPE_ITEM
PROBLEM_FAMILY
SOURCE_QUESTION
VERIFICATION_RULE
RESEARCH_DECISION
RESEARCH_CLAIM
OWNER_DECISION
SOURCE_CAPTURE
```

For current Mathematics v1 implementation, existing exact IDs may remain strings where the owning schema already provides sufficient typing. Do not introduce a wrapper only for aesthetic uniformity.

## 5. Shared primitive: dependency binding

Every mature pack should record the external states whose change may stale it.

Draft:

```text
dependency_id
dependency_type
ref
digest_or_version
staleness_class
```

Recommended `staleness_class`:

```text
IDENTITY_CRITICAL
AUTHORITY_CRITICAL
CONTENT_CRITICAL
PEDAGOGY_CRITICAL
ASSESSMENT_CRITICAL
ADVISORY
```

A pack can remain usable for some purposes while stale for others only if the state model makes that distinction explicit.

## 6. S1 — `stem-subtopic-intelligence-pack.schema.json`

### 6.1 Top-level identity

Proposed fields:

```text
schema_version
pack_id
subject_id
pack_status
maturity
canonical_subtopic_ref
subject_adapter_ref
display_title
```

`display_title` is non-authoritative.

`canonical_subtopic_ref` must be exact and current.

### 6.2 Scope bindings

```text
scope_bindings[]:
    binding_id
    scope_type
    scope_ref
    membership_role
    authority_ref
    effective_version
```

Draft `scope_type`:

```text
CURRENT_CURRICULUM
FOUNDATION
FUTURE_TARGET_BRIDGE
COMPETITION_EXTENSION
OUT_OF_SCOPE_REFERENCE
```

Draft `membership_role`:

```text
DIRECT_TARGET
PREREQUISITE_SUPPORT
TRANSFER_EXTENSION
REFERENCE_ONLY
```

Validation rule:

```text
OUT_OF_SCOPE_REFERENCE cannot be promoted to learner scope merely by being
present in the pack.
```

### 6.3 Authority bindings

```text
authority_bindings[]:
    authority_domain
    receipt_or_registry_ref
    digest_or_version
```

Expected domains include:

```text
SUBJECT_ENGINEERING
CANONICAL_DOMAIN
ASSESSMENT
SCOPE
PEDAGOGY_RESEARCH
```

Presence of an authority binding does not mean every object in that authority is in the pack.

### 6.4 Component references

Prefer grouped exact references:

```text
components:
    learning_atom_refs[]
    concept_refs[]
    model_refs[]
    equation_refs[]
    derivation_refs[]
    representation_refs[]
    misconception_refs[]
    problem_family_refs[]
    source_question_refs[]
    verification_rule_refs[]
```

The generic pack schema should not require every subject to support every field literally. Two options should be evaluated during adapter design:

```text
A. generic `subject_object_refs[]` typed by adapter
B. common cross-subject groups + adapter extension object
```

Do not choose until Mathematics and Chemistry pilot fixtures are compared.

### 6.5 SIL-owned references

```text
learning_transition_refs[]
source_selection_profile_refs[]
coverage_report_ref
known_gap_refs[]
```

### 6.6 Research binding

```text
pedagogy_research:
    required_state
    manifest_ref
    manifest_digest
    decision_refs[]
    claim_refs[]
```

The pack must not inline pedagogy claims already governed elsewhere.

### 6.7 Adaptation metadata

Only non-authoritative suitability metadata should live in the pack, for example:

```text
supported_learning_purposes[]
known_support_risks[]
calibration_policy_compatibility_refs[]
```

Forbidden inside the pack:

```text
if learner_percent > 70 then ...
resolved learner support mode
invented mastery state
silent knowledge default
```

Resolved learner adaptation remains LAU/run authority.

### 6.8 Provenance and digest

```text
provenance:
    created_by_ref
    created_from_refs[]
    reviewed_by_refs[]
    review_decision_refs[]
    created_at
    last_validated_at

dependencies[]
pack_digest
```

## 7. S2 — `stem-learning-transition.schema.json`

This is the most important new schema.

### 7.1 Identity

```text
schema_version
transition_id
subject_id
maturity
transition_authority_class
transition_kind
```

Draft `transition_authority_class`:

```text
SUBJECT_DERIVED
PEDAGOGY_GOVERNED
ASSESSMENT_DERIVED
OWNER_SEQUENCE
```

A transition cannot claim more authority than its class permits.

### 7.2 Endpoints

```text
from_refs[]
to_refs[]
```

Use arrays because some transitions genuinely synthesize several prerequisites into one new atom.

Validation should usually reject empty `from_refs` unless the transition kind explicitly permits an entry/root state.

### 7.3 Transition semantics

```text
why_required
new_cognitive_move
```

These fields explain the bridge but cannot define new subject truth.

If `why_required` contains a subject relation necessary to validity, the transition must carry exact supporting subject refs.

### 7.4 Bridge references

```text
concept_bridge_refs[]
equation_bridge_refs[]
representation_bridge_refs[]
capability_bridge_refs[]
```

Do not require Mathematics-specific bridge types in a generic implementation if Chemistry shows a better abstraction.

### 7.5 Entry state and completion

```text
learner_entry_requirements[]
success_criteria[]
```

`success_criteria` describe completion of the transition, not inferred real learner mastery from static content.

### 7.6 Diagnosis and repair

```text
diagnostic_refs[]
failure_signature_refs[]
repair_transition_refs[]
misconception_refs[]
```

A diagnostic may be a question, task or observation contract.

Do not claim the learner actually has a misconception unless observed learner evidence exists.

### 7.7 Evidence

```text
basis_refs[]
pedagogy_claim_refs[]
confidence
contradiction_resolution_ref
```

`basis_refs` should be typed/validated so pedagogy evidence cannot become subject authority.

### 7.8 Provenance

```text
created_by_ref
review_refs[]
dependency_bindings[]
transition_digest
```

## 8. S3 — `stem-source-selection-profile.schema.json`

### 8.1 Identity

```text
schema_version
profile_id
subject_id
source_ref
source_role
maturity
```

### 8.2 Source role

Draft enum:

```text
CURRICULUM_AUTHORITY
EXAM_SCOPE_AUTHORITY
SUBJECT_AUTHORITY
TECHNICAL_REFERENCE
REFERENCE_DATA
PEDAGOGY_EVIDENCE
FOUNDATION_EXPLANATION
ADVANCED_EXPLANATION
REPRESENTATION_REFERENCE
QUESTION_BANK
COMPETITION_QUESTION_SOURCE
SAFETY_AUTHORITY
```

A source can have multiple separately reviewed profiles if it genuinely serves different roles. Avoid one record whose role list becomes impossible to audit.

### 8.3 Exact support bindings

```text
supports_refs[]
```

This answers what part of the governed system the source is relevant to.

### 8.4 Suitability

```text
suitable_grade_ranges[]
suitable_learning_purposes[]
suitable_target_programs[]
suitable_knowledge_contexts[]
```

Suitability influences selection, not authority.

### 8.5 Rationale and limits

```text
why_preferred
known_limitations[]
rejection_conditions[]
```

These are essential. A URL without a reason is not a mature source profile.

### 8.6 Custody

```text
capture_or_version_ref
capture_digest
publisher_ref
rights_reuse_state
last_checked_at
```

The final rights enum requires legal/owner review before production.

### 8.7 Review

```text
curator_ref
review_refs[]
profile_digest
```

## 9. S4 — `stem-library-gap.schema.json`

A gap is a first-class unresolved state, not an error message hidden in logs.

Proposed fields:

```text
schema_version
gap_id
subject_id
pack_ref
gap_class
severity
affected_refs[]
description
detected_by_ref
owning_authority_domain
recommended_action_class
status
resolution_ref
```

Draft `status`:

```text
OPEN
UNDER_REVIEW
BLOCKED_EXTERNAL
RESOLVED
WONT_FIX_WITH_REASON
SUPERSEDED
```

Draft `recommended_action_class`:

```text
ENRICH_ENGINEERING
ADD_OR_REVIEW_SCOPE
AUTHOR_LEARNING_TRANSITION
CURATE_SOURCE_PROFILE
ADD_ASSESSMENT_EVIDENCE
VERIFY_ANSWER
RUN_PEDAGOGY_RESEARCH
RESOLVE_RIGHTS
ADD_CALIBRATION_POLICY
EXTEND_SUBJECT_ADAPTER
OWNER_ADJUDICATION
```

Closing the gap requires a `resolution_ref`; changing status alone is insufficient.

## 10. S5 — `stem-library-coverage-report.schema.json`

Coverage is derived.

It must schema-lock something equivalent to:

```text
authority = DERIVED_LIBRARY_COVERAGE
technical_authorization = NOT_IMPLIED
publication_authorization = NOT_IMPLIED
```

Proposed fields:

```text
schema_version
report_id
pack_ref
pack_digest
subject_adapter_ref
coverage_profile_ref
categories[]
open_gap_refs[]
result
report_digest
```

Each category:

```text
category
state = SATISFIED | NOT_APPLICABLE | BLOCKED
supporting_refs[]
reason
```

No arbitrary object-count quota should stand in for completeness.

## 11. S6 — `stem-subject-adapter-manifest.schema.json`

The adapter manifest allows the generic SIL/compiler to consume Mathematics and Chemistry without subject branching.

Proposed fields:

```text
schema_version
adapter_id
subject_id
adapter_version
maturity

canonical_registry_ref
authority_validator_ref
discovery_provider_ref

supported_object_types[]
supported_transition_bridge_types[]
supported_representation_types[]
supported_verification_types[]

subject_safety_policy_refs[]
source_role_extensions[]
coverage_profile_refs[]

adapter_digest
```

The manifest describes capabilities. It must not embed topic data.

## 12. Candidate ownership matrix

| Information | Primary owner | SIL behavior |
|---|---|---|
| Equation truth | Subject Engineering / Canonical Domain | exact ref only |
| Equation term meaning | Subject Engineering / Canonical Domain | exact ref; gap if insufficient |
| Derivation validity | Subject Engineering / Canonical Domain | exact ref only |
| Logical prerequisite | Subject Engineering | exact ref only |
| Assessment capability requirement | Core2 / assessment authority | exact ref only |
| Preferred instructional sequence | SIL learning structure / pedagogy | governed transition |
| Representation mathematical meaning | Subject domain | exact ref |
| Why representation is used at a learning step | SIL/pedagogy | usage/transition metadata |
| Misconception identity | Subject/domain + evidence | exact ref |
| Repair sequencing | SIL/pedagogy | governed transition |
| Problem-family identity | Core2/domain | exact ref |
| Learner support level | LAU/run | SIL cannot resolve |
| Curriculum scope | Scope authority | exact ref |
| Source authority role | source/scope governance | explicit source profile |
| Source learner suitability | source profile | governed recommendation |
| Research claim | pedagogy research manifest | exact ref |
| Publication authority | publication/release | never granted by SIL |

## 13. Generic validator invariants

The first SIL validator should be intentionally strict and topic-independent.

### 13.1 Identity/custody

```text
all exact refs resolve;
all bound registry/scope digests match current required state;
pack digest matches canonical serialization;
transition/profile IDs are unique;
duplicate canonical subject objects are rejected.
```

### 13.2 Authority separation

```text
SIL cannot inline a replacement equation payload;
SIL cannot create a new subject gate;
SIL cannot promote an alias to exact identity;
INSTRUCTIONAL_SEQUENCE cannot satisfy LOGICAL_DEPENDENCY;
source suitability cannot satisfy subject authority;
pedagogy claim cannot satisfy curriculum authority;
coverage PASS cannot imply technical or publication authorization.
```

### 13.3 Learner separation

```text
pack cannot invent learner percentage;
pack cannot hard-code percentage bands;
pack cannot modify Core1 depth from learner percentage;
pack cannot authorize Core2 demand without external LAU/run state.
```

### 13.4 Research separation

```text
research refs must resolve to promoted governed claims when used;
SIL cannot copy discovery-only evidence into production claims;
contradictory research cannot be silently flattened into a recommendation.
```

### 13.5 Scope separation

```text
future bridge does not become current curriculum;
out-of-scope references cannot satisfy direct-current-scope coverage;
competition extension cannot rewrite base curriculum authority.
```

## 14. Proposed fail-closed code families

Actual names should follow repository conventions after review.

Candidate families:

```text
SIL_REF_UNKNOWN
SIL_REF_STALE
SIL_DUPLICATE_IDENTITY
SIL_INLINE_SUBJECT_TRUTH_FORBIDDEN
SIL_TRANSITION_AUTHORITY_MISMATCH
SIL_LOGICAL_DEPENDENCY_UNSUPPORTED
SIL_ASSESSMENT_DEPENDENCY_UNSUPPORTED
SIL_INSTRUCTIONAL_SEQUENCE_EVIDENCE_MISSING
SIL_SCOPE_ROLE_CONFLICT
SIL_FUTURE_BRIDGE_AS_CURRENT_SCOPE
SIL_SOURCE_ROLE_CONFLICT
SIL_SOURCE_AUTHORITY_UNSUPPORTED
SIL_SOURCE_RIGHTS_UNKNOWN_FOR_REUSE
SIL_RESEARCH_REF_UNPROMOTED
SIL_LEARNER_PERCENT_POLICY_EMBEDDED
SIL_COVERAGE_AUTHORIZATION_FORBIDDEN
SIL_GAP_RESOLVED_WITHOUT_EVIDENCE
SIL_ADAPTER_CAPABILITY_UNSUPPORTED
```

## 15. Required synthetic falsifiers before real topic data

Before Theory of Equations enters the SIL, synthetic tests should prove the architecture itself.

At minimum:

1. synthetic canonical object can be referenced without topic-specific runtime code;
2. unknown canonical ref fails;
3. stale registry digest fails;
4. duplicate object copied inline fails;
5. instructional sequence falsely labeled logical dependency fails;
6. source explanation profile falsely labeled subject authority fails;
7. future-target bridge falsely used as current curriculum fails;
8. learner percentage embedded in pack policy logic fails;
9. research discovery source used without promoted claim fails where promotion is required;
10. coverage report with `publication_authorization = ALLOWED` fails;
11. resolved gap without resolution evidence fails;
12. synthetic new subject object type can be accepted through adapter data without generic-topic branching;
13. Chemistry adapter fixture can expose non-Mathematics object types without adding `if chemistry_topic` logic;
14. stale transition dependency invalidates the transition/pack as designed;
15. unrelated registry change does not force unnecessary manual edits when exact bound dependencies remain unchanged and current policy permits that looseness.

## 16. Theory-of-Equations pilot schema questions

The pilot is not only content authoring. It must answer schema questions.

### Identity

Can the human label resolve to one pack, several packs or a pack-of-packs without hiding ambiguity?

### Scope

Can Grade-9 foundation, future JEE bridge and out-of-scope advanced material coexist without authority leakage?

### Transition

Can the schema distinguish:

```text
logical dependency
instructional ordering
representation bridge
repair sequence
assessment capability dependency
```

### Canonical reuse

Can one equation/concept/problem-family object appear in several teaching contexts without being copied?

### Source profiles

Can one authoritative source and one learner-friendly source coexist with clearly different roles?

### Learner adaptation

Can 70% knowledge affect downstream support without modifying the pack's subject truth?

### Research

Can deep/targeted pedagogy evidence attach to the relevant claims without entering subject authority?

## 17. Chemistry falsification questions

The Chemistry pilot must test whether generic SIL assumptions are accidentally Mathematics-shaped.

Ask:

```text
Can the pack compose a macro observation + particle model + symbolic representation?
Can a transition bridge those three representations?
Can a source profile distinguish terminology authority from reference property data?
Can a safety authority be required for an experimental procedure?
Can reaction conditions be canonical subject objects rather than prose?
Can the generic pack avoid requiring equation/derivation fields when not applicable?
```

If not, revise the generic abstraction rather than adding topic-specific conditionals.

## 18. Open schema decisions requiring review

Do not resolve these silently during implementation:

1. one shared transition registry vs subject-specific transition registries using one common schema;
2. typed exact-reference envelope everywhere vs existing native exact-ID strings where already sufficient;
3. generic `subject_object_refs[]` vs cross-subject common groups + adapter extensions;
4. whether diagnostic tasks belong in SIL, Core2 or a new shared diagnostic object class;
5. rights/reuse enum and owner/legal review process;
6. production review authority for `PEDAGOGY_GOVERNED` transitions;
7. multilingual labels and alias ownership;
8. pack-level vs transition-level source-profile binding granularity;
9. whether source profiles should be globally reusable or subject-library scoped;
10. compatibility policy when a canonical object changes text but not identity/semantics.

## 19. Implementation gate

Do not create production `contracts/stem-*.schema.json` files from this draft until:

```text
Phase-1 architecture drift audit has been reviewed;
Core Spec authority hierarchy is reconciled;
Architecture Catalog direction is accepted;
current Mathematics registries have been mapped to ownership table;
Theory-of-Equations pilot requirements are frozen;
at least one Chemistry pilot fixture has been sketched;
open schema decisions above are either resolved or explicitly deferred.
```

## 20. Design doctrine

> The SIL succeeds when it makes the agent less inventive about structure without making the library more authoritative than the systems it composes.
>
> Exact subject truth remains exact subject truth. The new value is explicit learning transitions, source-selection reasoning, scope partition, coverage state, provenance and gap visibility—all typed so that an average agent can reproduce the same governed structure instead of rebuilding it from intuition.
