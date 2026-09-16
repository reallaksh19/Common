# Subtopic Intelligence Library — Ontology, Schema Family and Delivery Roadmap

> **Status: DESIGN / NON-NORMATIVE**
>
> This document defines the proposed architecture for the future Subtopic Intelligence Library (SIL). It is deliberately not a production schema. No subject authority, publication authority or learner-release authority is granted by this file.

## 1. Purpose

The library exists to remove stable reasoning work from the agent without creating a second source of mathematical truth.

The target property is:

> An ordinary competent cold-start agent should not need to invent the prerequisite structure, canonical object selection, equation meaning, required representations, known misconceptions, problem-family anatomy, source-selection rationale or question-family coverage for a mature subtopic.

The agent should instead receive a governed composition of exact authoritative objects plus explicit, evidence-backed learning-structure metadata.

## 2. What the library is not

The SIL is not:

```text
a second Engineering registry;
a second Canonical Domain Registry;
a free-form notes folder;
a topic-to-URL bookmark list;
a cache of LLM explanations;
a replacement for Core1/Core2;
a learner mastery database;
a way to authorize material through semantic similarity;
a place to copy the same equation into every subtopic pack.
```

The strongest anti-drift invariant is:

```text
SUBJECT TRUTH
    lives in exact governed subject/Engineering/domain objects

SIL
    composes, sequences, indexes and explains the use of those objects
    through exact references and separately governed learning metadata
```

## 3. Why a composition layer is required

The existing Mathematics Canonical Domain Registry already has first-class assets including:

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

It also already enforces the important rule that one Engineering source identity should not be copied merely because it appears in several teaching scopes.

Therefore the SIL must not restate these payloads. It should reference exact canonical IDs and add only information whose authority is different, such as:

```text
subtopic composition;
learning-order constraints;
prerequisite-transition rationale;
diagnostic and repair links;
source-selection rationale;
learner/purpose suitability of explanatory sources;
coverage state;
known library gaps;
curation/maturity metadata.
```

When the SIL discovers that an equation lacks a necessary validity condition, that is not a reason to patch the SIL. It is an Engineering/domain enrichment gap.

## 4. The library's central object: Subtopic Intelligence Pack

The pack is a governed composition manifest, not a content dump.

Proposed conceptual structure:

```text
SUBTOPIC_INTELLIGENCE_PACK
│
├── identity
├── scope_bindings
├── authority_bindings
│
├── prerequisite_transition_refs[]
├── learning_atom_refs[]
├── concept_refs[]
├── model_refs[]
├── equation_refs[]
├── derivation_refs[]
├── representation_refs[]
├── misconception_refs[]
│
├── problem_family_refs[]
├── source_question_refs[]
├── verification_rule_refs[]
│
├── source_selection_profile_refs[]
├── pedagogy_research_decision_refs[]
│
├── adaptation_metadata
├── coverage_state
├── known_gap_refs[]
├── provenance
└── pack_digest
```

A pack may be small. Completeness means required reasoning is covered, not that every possible object is listed.

## 5. Identity and scope model

A human subtopic label is not a sufficient canonical identity.

The pack should distinguish:

```text
pack_id
subject_id
canonical_subtopic_ref
display_title
discovery_alias_refs[]
```

and explicit scope memberships:

```text
scope_binding_id
authority_source_ref
scope_type
scope_ref
membership_role
valid_from / version_ref
```

Recommended `scope_type` examples:

```text
CURRENT_CURRICULUM
FOUNDATION
FUTURE_TARGET_BRIDGE
COMPETITION_EXTENSION
OUT_OF_SCOPE_REFERENCE
```

`OUT_OF_SCOPE_REFERENCE` exists for explanatory comparison or roadmap context and cannot be promoted into current learner scope without a separate exact authority change.

This directly addresses cases such as:

```text
Grade 9 learner
+ future IIT-JEE trajectory
```

where current foundation and eventual target content are not the same authority claim.

## 6. Schema family — do not build one giant contract

The SIL should be implemented as a small family of composable schemas.

### S1 — `stem-subtopic-intelligence-pack.schema.json`

Owns:

```text
pack identity
exact refs
scope memberships
required component references
maturity
coverage refs
provenance refs
pack digest
```

Does **not** duplicate subject payloads.

### S2 — `stem-learning-transition.schema.json`

Owns the transition between a prerequisite state and a target learning atom/capability.

### S3 — `stem-source-selection-profile.schema.json`

Owns why a source is preferred for a role, learner context or purpose without converting it into subject authority.

### S4 — `stem-library-gap.schema.json`

Owns a normalized gap or unresolved curation need.

### S5 — `stem-library-coverage-report.schema.json`

Derived report proving the pack satisfies its required composition profile.

### S6 — `stem-subject-adapter-manifest.schema.json`

Declares the exact subject registry/validators and supported object classes used by a pack.

### Later schemas only if evidence justifies them

Potential later additions:

```text
question-bank-ingestion contract
external-source capture contract
interoperability export receipt
library migration receipt
human review decision
```

Do not pre-create schemas simply because a noun exists in this roadmap.

## 7. Learning Transition object — the most important new reasoning type

Simple prerequisite edges such as:

```text
factorisation → quadratic equations
```

are too weak for agent-independent teaching.

A mature transition should carry the reasoning another agent would otherwise invent.

Proposed shape:

```text
transition_id
subject_id
from_ref
to_ref
transition_kind

why_required

learner_entry_state[]
new_cognitive_move

representation_bridge_refs[]
concept_bridge_refs[]
equation_bridge_refs[]

success_criteria[]

diagnostic_prompt_refs[]
failure_signature_refs[]
repair_refs[]

source_refs[]
confidence
validation_refs[]
maturity
transition_digest
```

Recommended generic `transition_kind` examples:

```text
PREREQUISITE
REPRESENTATION_SHIFT
SYMBOLIZATION
ABSTRACTION
GENERALIZATION
INVERSE_USE
METHOD_DISCRIMINATION
CONSTRAINT_INTRODUCTION
SPECIAL_CASE_TO_GENERAL
```

These are cognitive/structural categories, not topic branches.

### 7.1 Subject-truth boundary

`why_required` must not become a hidden place to invent mathematical facts.

If the transition relies on a specific mathematical relation, that relation should be an exact concept/equation/capability reference.

The transition explains the **learning bridge** between governed objects.

## 8. Learning atoms

The current Canonical Domain Registry already supports `LEARNING_ATOM`.

The SIL should reference those exact atoms rather than create a competing atom type.

A pack may add composition metadata such as:

```text
required
optional_extension
recommended_order
partial_order_dependencies
repair_only
bridge_only
```

If the current atom payload lacks stable mathematical meaning required by teaching, fix the canonical domain/Engineering source rather than writing the truth only into the pack.

## 9. Equation and relation intelligence

Equation semantics are subject truth and therefore remain canonical-domain/Engineering owned.

The SIL should require equation objects to be sufficiently rich for the target pack, not copy them.

For Mathematics, a mature equation object should eventually support evidence for:

```text
expression
mathematical_question
parent model/object
assumptions / valid_when
term meanings
derivation / justification
legal transformations
risky or illegal transformations
interpretations
representation links
special cases
inverse uses
failure cases
verification rules
```

Where current canonical objects already contain these, reuse them.

Where required fields are missing, emit:

```text
ENGINEERING_ENRICHMENT_GAP
```

not a SIL-local duplicate equation.

## 10. Representation intelligence

Representations are subject-linked cognitive objects, not decoration.

The SIL should reference canonical representation objects and may add pedagogical selection metadata through a separate usage association.

The canonical representation should preserve subject meaning such as:

```text
representation type
what must become visible
what must not be implied
subject bindings
```

A `representation_usage` association may add:

```text
usage_id
representation_ref
target_learning_atom_refs[]
use_stage
why_here
translation_prompt_refs[]
known_visual_misread_refs[]
source_selection_profile_ref
```

This keeps the representation itself canonical while allowing several pedagogically distinct uses.

## 11. Misconception intelligence

A misconception should represent an incorrect model or reasoning pattern, not merely a wrong final answer.

Canonical misconception truth should be subject/domain owned.

A SIL misconception usage association may link:

```text
misconception_ref
trigger_learning_atom_refs[]
trigger_problem_family_refs[]
diagnostic_refs[]
contrast_case_refs[]
repair_transition_refs[]
representation_refs[]
pedagogy_claim_refs[]
```

If external research motivates a misconception repair technique, the technique must use the claim-level pedagogy research path. It cannot silently become universal subject truth.

## 12. Problem-family intelligence

Problem families already exist as canonical domain assets. The SIL should compose them into the subtopic rather than create duplicate family definitions.

A mature Mathematics problem-family object should eventually expose enough subject truth for downstream teaching, including:

```text
recognition cues
required capabilities
invariants
safe / forbidden variations
hidden conditions
representation options
first non-obvious move
solution structure
wrong-route refs
verification refs
near-transfer axes
far-transfer axes
```

Fields that are stable mathematical/assessment structure belong in Core2/domain authority.

Fields that are learner-specific support decisions belong downstream in LAU / generation, not the library.

## 13. Source Selection Profile

The source library must not be a list of links.

A source-selection profile explains **why a source is useful and for which role**.

Proposed shape:

```text
profile_id
source_ref
source_role
subject_id

supports_refs[]

suitable_grade_ranges[]
suitable_purposes[]
suitable_knowledge_contexts[]
suitable_target_programs[]

why_preferred
known_limitations[]
rejection_conditions[]

source_version_or_capture_ref
rights_or_reuse_state

curator_ref
review_refs[]
maturity
profile_digest
```

Recommended generic `source_role` examples:

```text
CURRICULUM_AUTHORITY
EXAM_SCOPE_AUTHORITY
SUBJECT_AUTHORITY
TECHNICAL_REFERENCE
PEDAGOGY_EVIDENCE
FOUNDATION_EXPLANATION
ADVANCED_EXPLANATION
REPRESENTATION_REFERENCE
QUESTION_BANK
COMPETITION_QUESTION_SOURCE
REFERENCE_DATA
SAFETY_AUTHORITY
```

### 13.1 Critical rule

Learner knowledge may influence which explanatory source is preferred.

Learner knowledge must not change which source is authoritative for subject truth.

Bad:

```text
30% learner → easy website becomes mathematical authority
```

Correct:

```text
authoritative subject source determines truth
+
learner-appropriate explanation source helps communicate that truth
```

## 14. Question sources and future interoperability

The current system already distinguishes frozen source questions and canonical solutions.

The future question subsystem should preserve:

```text
question identity
source/provenance
rights/reuse state
frozen vs generated
capability refs
problem-family refs
task-demand vector
answer contract
canonical solution ref
verification refs
known ambiguity
```

1EdTech QTI can be considered later as an import/export interoperability format, not as the internal authority model. QTI is designed to exchange assessment items, tests and results between systems:
https://www.1edtech.org/standards/qti

The preferred architecture is:

```text
internal governed question object
        ↓ explicit adapter
QTI import/export
```

not:

```text
QTI-valid item
        ↓
automatically trusted question
```

## 15. Scope / competency interoperability

1EdTech CASE demonstrates useful patterns for stable identifiers, hierarchical frameworks and associations among competencies/standards:
https://www.1edtech.org/standards/case

The SIL can borrow these principles for external alignment without replacing internal exact IDs.

Potential future association examples:

```text
INTERNAL_CAPABILITY_REF
↔ curriculum standard identifier
↔ exam objective identifier
↔ external competency identifier
```

Each mapping requires its own provenance and validation state.

## 16. Chemistry adaptation

The generic SIL composition should work for Chemistry, but the underlying subject objects differ.

ACS guidance stresses translation among macroscopic, particulate/submicroscopic and symbolic representations:
https://www.acs.org/education/policies/middle-and-high-school-chemistry/teaching-and-assessment.html

A Chemistry Subtopic Intelligence Pack may therefore compose exact Chemistry objects such as:

```text
chemical species
macro observation
particle model
symbolic representation
reaction
reaction condition
stoichiometric relation
thermodynamic relation
kinetic model
nomenclature rule
experimental observation
measurement / uncertainty
hazard / safety constraint
```

The generic SIL schema should not need to understand these payloads. It should reference them through the Chemistry subject adapter.

Potential source-role examples include IUPAC terminology and NIST reference data, with explicit suitability/limitations rather than hard-coded universal preference:

- https://goldbook.iupac.org/
- https://www.nist.gov/programs-projects/nist-chemistry-webbook

## 17. Coverage profile

Not every subtopic requires the same number of equations, diagrams or misconceptions.

Therefore do not impose simplistic quotas such as:

```text
3 equations
5 misconceptions
10 questions
```

Instead define required coverage categories by subject adapter / subtopic composition profile.

Example generic categories:

```text
IDENTITY_BOUNDARY
SCOPE_BINDING
PREREQUISITE_CLOSURE
LEARNING_TRANSITIONS
CANONICAL_OBJECTS
REPRESENTATIONS
MISCONCEPTION_DIAGNOSTICS
PROBLEM_FAMILIES
VERIFICATION
SOURCE_STRATEGY
QUESTION_EVIDENCE
RESEARCH_BINDING where required
KNOWN_GAPS
```

A pack is complete when every required category is either:

```text
SATISFIED
NOT_APPLICABLE with explicit reason
BLOCKED with explicit gap
```

Silent absence is invalid.

## 18. Gap taxonomy

Recommended gap classes:

```text
ENGINEERING_AUTHORITY_GAP
ENGINEERING_ENRICHMENT_GAP
SCOPE_AUTHORITY_GAP
PREREQUISITE_TRANSITION_GAP
LEARNING_ATOM_GAP
REPRESENTATION_GAP
MISCONCEPTION_GAP
PROBLEM_FAMILY_GAP
QUESTION_EVIDENCE_GAP
ANSWER_VERIFICATION_GAP
SOURCE_SELECTION_GAP
PEDAGOGY_RESEARCH_GAP
RIGHTS_REUSE_GAP
CALIBRATION_POLICY_GAP
SUBJECT_ADAPTER_GAP
STALE_DEPENDENCY_GAP
CONFLICT_REQUIRES_REVIEW
```

A gap report is derived and non-authoritative.

Closing a gap requires changing the correct owning authority, not merely marking the report resolved.

## 19. Maturity lifecycle

A pack and its subordinate library objects should move through explicit states such as:

```text
DRAFT
RESEARCHING
TECHNICALLY_BOUND
CURATION_REVIEW
STRESS_TEST_READY
VALIDATED
PRODUCTION_ELIGIBLE
STALE
DEPRECATED
```

`VALIDATED` means the pack passed its current validators. It does not independently grant learner publication authority.

`STALE` should be automatic when a bound canonical dependency digest/version changes materially.

## 20. Digest and invalidation model

The pack should bind the exact identities/versions actually used.

At minimum consider custody over:

```text
subject adapter version
canonical subject registry digest
scope authority digest
transition registry digest
source-profile registry digest
pedagogy research refs/digests
question-bank registry digest when used
pack payload digest
```

Avoid binding a manually curated profile to unrelated global data when that would force unnecessary edits. Prefer the pattern already used by Engineering discovery:

```text
loose maintenance coupling
+
exact per-run / per-pack custody
```

## 21. Migration rule

The SIL will become large. Migration must therefore be designed before mass population.

Every schema migration should classify changes as:

```text
metadata-only
compatible optional extension
compatible required-field addition with migration
breaking identity semantics
breaking authority semantics
```

A migration receipt should eventually record:

```text
from_schema_version
to_schema_version
input_pack_digest
output_pack_digest
migration_tool_ref
semantic_change_class
review_ref
```

Never rewrite thousands of packs with an LLM and declare them equivalent without deterministic validation.

## 22. Authoring and review workflow

Recommended future library workflow:

```text
1. DISCOVER
   human request → non-authoritative candidate subtopic(s)

2. SELECT EXACT SCOPE
   bind exact subject and scope identities

3. COMPOSE
   collect exact canonical object refs

4. MAP TRANSITIONS
   author/review prerequisite-learning transitions

5. CURATE SOURCES
   add source-selection profiles with reasons

6. MAP ASSESSMENT
   bind problem families + verified question evidence

7. RESEARCH PEDAGOGY
   only through governed claim-level research where needed

8. RUN COVERAGE
   derive gaps

9. REVIEW GAPS
   repair owning authorities, not the report

10. STRESS TEST
    cold-start agent consumes pack

11. CROSS-AGENT REPRODUCIBILITY
    compare canonical outputs

12. PROMOTE MATURITY
    only after validation/review
```

## 23. Average-agent context compiler

A high-value downstream tool should compile a bounded `Agent Context Pack` from the SIL rather than giving every agent the whole repository.

Proposed contents:

```text
run manifest
relevant Core Spec sections
exact subject authorization receipts
Subtopic Intelligence Pack
exact canonical objects needed
transition objects
source profiles
allowed question/problem families
learner-calibration state
required output schemas
validation commands
known gaps
```

This is likely more effective against drift than simply making prompts longer.

## 24. Cross-agent reproducibility test

The library's strategic test is not page similarity.

Run the same input through:

```text
strong agent
average agent
restricted agent
```

### Deterministic comparison fields

Require exact/near-exact agreement on:

```text
scope IDs
subject/Engineering IDs
prerequisite closure
canonical object refs
transition refs
problem-family refs
source-authority roles
research obligations
learner-calibration inputs and policy
blockers
```

### Allowed variation

Do not penalize differences in:

```text
wording
non-authoritative analogy
presentation sequence where unconstrained
selection among multiple equally legal examples
search paths before promotion
```

A future `CANONICAL_DRIFT_RATE` should score only deterministic fields.

## 25. Pilot: Theory of Equations

Before mass library creation, build one deep Mathematics pilot.

Suggested run context:

```text
SUBTOPIC_REQUEST = Theory of Equations
CURRENT_GRADE = 9
TARGET = IIT-JEE trajectory
LEARNER_KNOWLEDGE_PERCENT = 70
PURPOSE = COMPETITIVE_EXAM
ENGINEERING_DEPTH = RESEARCH
```

This is deliberately difficult because it tests:

```text
ambiguous human terminology
current-grade foundation vs future target
prerequisite graph depth
equation meaning and transformations
multiple representations
misconceptions
several problem families
competitive transfer
source-role separation
learner calibration
```

The pilot must explicitly partition:

```text
CURRENT FOUNDATION
FUTURE-TARGET BRIDGE
NOT CURRENTLY AUTHORIZED / OUT OF SCOPE
```

It must not label eventual JEE content as Grade-9 curriculum merely because the learner is in Grade 9.

## 26. Pilot acceptance questions

The Theory-of-Equations pilot should answer:

```text
Can an average cold-start agent recover the exact governed structure?

Which reasoning still had to be invented by the agent?

Was that reasoning:
    subject truth → Engineering/domain gap?
    learning transition → SIL gap?
    assessment structure → Core2/domain gap?
    source choice → source-profile gap?
    pedagogy → research/pedagogy gap?
    learner support → LAU/calibration gap?

Did any topic-specific Blueprint code become necessary?

Could the same SIL contracts describe a geometry subtopic?
```

Any stable reasoning that lives only in the agent becomes a candidate governed data object.

## 27. Horizontal Mathematics stress before scale

After Theory of Equations, test structurally different Mathematics areas before mass authoring:

```text
NUMBER SYSTEMS / RADICALS
COORDINATE GEOMETRY
EUCLIDEAN GEOMETRY
COMBINATORICS / COUNTING
FUNCTIONS / GRAPHS
```

The purpose is not content volume. It is to falsify an algebra-shaped ontology.

## 28. Chemistry pilot before mass scale

Then implement one bounded Chemistry pack, for example:

```text
MOLE CONCEPT
or
ATOMIC STRUCTURE
or
CHEMICAL BONDING
```

The pilot should force the generic SIL to handle:

```text
non-mathematical subject objects
multi-level representations
reference data
nomenclature
conditions
experimental evidence
safety where relevant
```

If the generic schema requires a field named `equation_ref` everywhere, the abstraction has failed.

## 29. Library Authoring Studio — only after schema stabilization

Once the schema family survives pilots, a UI can expose tabs such as:

```text
Scope
Prerequisites
Transitions
Learning Atoms
Canonical Objects
Representations
Misconceptions
Problem Families
Questions
Sources
Research
Coverage
Gaps
```

The UI should render explicit states:

```text
COMPLETE
PARTIAL
MISSING
UNVERIFIED
CONFLICTED
STALE
```

It must edit governed data through schema validation, not maintain a separate hidden database of truth.

## 30. Work that can be parallelized after the schema freeze

Once contracts are stable, independent agents can safely populate:

```text
source-selection profiles
prerequisite-transition candidates
misconception evidence
representation usage mappings
question-family mappings
question-bank metadata
coverage-gap investigations
pedagogy research dossiers
```

Their outputs remain proposals until validators/review promote them.

## 31. Work that remains central

Do not distribute ownership of these without explicit governance:

```text
subject authority model
identity semantics
schema family ownership
validator semantics
maturity/promotion rules
migration semantics
subject-adapter boundary
publication authority
```

## 32. Explicit limitations of this roadmap

This roadmap does not yet resolve:

1. the exact canonical identifier namespace for cross-subject packs;
2. whether learning transitions should live in a shared STEM registry or subject-specific registries behind one shared schema;
3. the final review authority for promoting transition/source-profile records to production;
4. licensing policy enums for question/source reuse;
5. the exact learner knowledge model beyond the current percent/owner-waiver path;
6. capability-level learner evidence and how it may eventually supplement a scalar percentage;
7. the correct Chemistry safety authority stack;
8. external CASE/QTI import/export mapping details;
9. storage/index technology for a very large library;
10. long-term archival/reproducibility policy for web captures;
11. multilingual terminology/alias governance;
12. how much human review is required at each maturity level.

These are declared gaps, not implementation details to infer silently.

## 33. Recommended implementation sequence

```text
L0  Review independent Phase-1 architecture audit

L1  Freeze Core Spec authority hierarchy + Architecture Catalog

L2  Implement draft subject-adapter manifest

L3  Implement Learning Transition schema + synthetic fixtures

L4  Implement Source Selection Profile schema + synthetic fixtures

L5  Implement SIL Pack composition schema

L6  Implement Gap + Coverage schemas

L7  Write validators and mutation falsifiers

L8  Build Theory-of-Equations Mathematics pilot

L9  Run average-agent reproducibility benchmark

L10 Test non-algebra Mathematics verticals

L11 Build one Chemistry adapter/pilot

L12 Revise generic contracts only for genuinely cross-subject needs

L13 Freeze v1 library contracts

L14 Build authoring/context/coverage tooling

L15 Begin mass parallel library population
```

## 34. Promotion criterion for v1

Do not call the SIL architecture v1 production-ready until it proves all of the following:

```text
no duplicate subject truth;
no topic-specific Blueprint branches;
exact canonical refs throughout;
explicit scope partition;
prerequisite transitions carry enough reasoning for a cold-start agent;
source roles are separated from learner suitability;
question evidence has answer/provenance custody;
research promotion stays claim-level;
learner calibration remains downstream and governed;
stale dependencies fail closed;
Theory-of-Equations pilot passes;
non-algebra Mathematics pilot passes;
Chemistry pilot does not require topic-specific generic runtime changes;
average-agent canonical drift is acceptably low;
known limitations remain visible.
```

## 35. Central design doctrine

> The library should store the stable reasoning an agent would otherwise have to reconstruct, but it must store that reasoning in the correct authority domain.
>
> Mathematical or chemical truth belongs to the subject authority. Assessment truth belongs to the assessment authority. Pedagogy evidence belongs to governed research. Learner adaptation belongs to learner calibration. The Subtopic Intelligence Library composes those authorities into a reproducible teaching context; it does not replace them.
