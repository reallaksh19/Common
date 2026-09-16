# STEM Blueprint Core Specification — Consolidation and Scalability Roadmap

> **Status: DESIGN / NON-NORMATIVE**
>
> This file is intentionally not a new source of runtime authority. It records the proposed consolidation target for review after the independent Phase-1 architecture/documentation drift audit. Existing schemas, policies, validators and normative Mathematics documents remain authoritative until an owner-approved migration explicitly promotes a replacement.

## 1. Why this roadmap exists

Mathematics V2 has reached the point where the architecture itself must become easier to recover than the history that produced it.

The long-term product requirement is not merely that a strong agent can generate a good chapter. The stronger requirement is:

> Given the same governed repository state, an ordinary competent cold-start agent should recover essentially the same legal scope, exact identities, prerequisites, subject objects, source roles, research obligations, learner-calibration state, problem-family authority and release state without relying on conversational memory or topic-specific Blueprint code.

A stronger agent may improve search, explanatory prose, example choice within legal families, optional research breadth and presentation. It must not be required to reconstruct the subject authority model.

This roadmap therefore separates four things that have historically been easy to conflate:

```text
NORMATIVE AUTHORITY
    what is legally true / allowed / required

EXECUTABLE CONTRACTS
    schemas + policies + validators + compilers + release gates

DERIVED OBSERVABILITY
    architecture maps, generated tables, dashboards, visibility views

ROADMAP / DESIGN
    proposed future work that carries no current authorization
```

## 2. Central success criterion: bounded flexibility

The system must be flexible across:

```text
new subtopic
new grade
new curriculum/exam scope
new learner-knowledge state
new learning purpose
new research depth
new question corpus
new source set
new agent capability
new subject adapter
```

but authority must remain deliberately inflexible:

```text
permissive discovery
        ↓
explicit exact identity
        ↓
current subject/Engineering authority
        ↓
generic validation + closure
        ↓
governed composition
        ↓
learner adaptation
        ↓
publication
```

Flexibility is demonstrated when the same generic orchestration survives new data. It is **not** demonstrated by adding another topic-specific branch.

## 3. Core doctrine to preserve during consolidation

The consolidated Core Specification must preserve at least these existing invariants unless an explicit architecture decision supersedes them:

1. Execution order may vary; authority order may not.
2. Discovery may be approximate; authorization may not.
3. Topic-specific mathematical truth belongs to governed Mathematics Engineering/domain data, not generic Blueprint runtime.
4. Core1 semantic authority and Core2 assessment authority remain distinct.
5. A canonical mathematical object is not duplicated because it appears in multiple teaching scopes.
6. Core1A/Core1B depth is controlled by intrinsic subtopic difficulty / governed study policy, not learner knowledge percentage.
7. Core2A/Core2B learner support and demand require explicit learner calibration or an explicit owner waiver.
8. Research discovery may be open while promotion is claim-specific, evidence-custodied and fail-closed.
9. Derived visibility or architecture views cannot become authority.
10. Publication consumes governed semantic products and must not invent missing mathematics, hints, examples, omissions, answer custody or learner actions.

## 4. Proposed document hierarchy

The final documentation set should stop making every important document look equally canonical.

### 4.1 One normative root

After the independent drift audit, either upgrade the existing `CANONICAL_ARCHITECTURE.md` or replace it through an explicit migration with one normative root such as:

```text
STEM_BLUEPRINT_CORE_SPEC.md
```

The root should define only durable architecture:

```text
mission / success criterion
authority topology
execution topology
identity and provenance rules
subject adapter boundary
Core1 / Core2 / A / B purpose contracts
SDU / LAU ownership boundaries
TTU families
research promotion boundary
assessment / question custody boundary
publication boundary
maturity / versioning model
risk / limitation policy
extension and deprecation rules
```

It should not manually duplicate every field of every JSON Schema.

### 4.2 Normative subordinate specifications

Subject- or subsystem-specific rules that change independently should remain subordinate normative documents, for example:

```text
Mathematics Engineering authority
Engineering discovery
research promotion
generation calibration
publication governance
subject-adapter specifications
```

The Core Spec should identify their role and authority, not copy all of their text.

### 4.3 Generated references

These should be generated from machine-readable catalogs rather than manually maintained:

```text
schema index
schema version table
producer → validator → consumer map
policy dependency table
test coverage matrix
authority matrix
maturity report
deprecation report
```

### 4.4 Explanatory guides

Onboarding, examples and tutorials should be explicitly non-normative. If an explanatory guide conflicts with a current executable contract, it cannot win merely because it is easier to read.

## 5. Architecture Catalog — required before the system grows further

The project should add one machine-readable catalog that describes the architecture components themselves.

This catalog is **metadata about authority**, not subject authority.

Proposed record shape:

```text
component_id
component_type
path
schema_version
status
maturity
subject_scope
authority_domain
producer_refs[]
validator_refs[]
consumer_refs[]
upstream_refs[]
policy_refs[]
test_refs[]
normative_doc_refs[]
deprecates[]
deprecated_by[]
release_class
notes
```

Recommended maturity states:

```text
DESIGN
TEST_ONLY
PRODUCTION
LEGACY
DEPRECATED
```

Recommended documentation status states:

```text
NORMATIVE
EXECUTABLE
DERIVED
EXPLANATORY
ROADMAP
```

### 5.1 Catalog invariants

CI should eventually prove:

```text
every PRODUCTION schema exists;
every declared validator exists;
every declared producer exists;
every declared policy exists;
every declared test exists;
no two active components claim the same canonical component_id;
deprecation references resolve;
current generated documentation matches the catalog.
```

The catalog must not auto-promote an item from DESIGN or TEST_ONLY to PRODUCTION.

## 6. Provenance model

Current digest binding is already a strong foundation. The Core Spec should formalize a small common provenance vocabulary inspired by, but not mechanically dependent on, W3C PROV.

W3C PROV distinguishes entities, activities and agents and uses provenance to support quality, trust and reproducibility. Reference: https://www.w3.org/TR/prov-overview/

The project can adopt the conceptual distinction without adopting RDF or the full PROV serialization stack:

```text
ENTITY
source, gate, domain asset, question, claim, pack, release, publication

ACTIVITY
search, capture, validation, derivation, compilation, selection,
research promotion, rendering, migration

AGENT
owner, source authority, research agent, compiler, validator,
human reviewer, publication process
```

Every consequential artifact should be able to answer:

```text
what exact inputs produced me?
what transformed them?
which identities are authoritative?
which assertions are derived?
what version/digest was used?
what would make me stale?
```

## 7. External interoperability: learn from standards, do not surrender authority to them

The architecture should preserve internal exact authority while allowing future interoperability adapters.

### 7.1 1EdTech CASE

CASE 1.1 provides machine-readable identifiers, frameworks, hierarchy and associations for standards/competencies. References:

- https://www.1edtech.org/standards/case
- https://standards.1edtech.org/case/

Useful design lessons:

```text
stable identifiers matter;
framework membership and object identity are different;
relationships should be explicit associations;
standards should be machine-addressable rather than trapped in PDFs.
```

Potential future use:

```text
internal governed capability / scope objects
        ↓ export/import adapter
CASE-aligned external exchange
```

CASE must not become a substitute for Mathematics Engineering validation.

### 7.2 1EdTech QTI

QTI 3 supports portable assessment items/tests and results exchange. References:

- https://www.1edtech.org/standards/qti
- https://www.1edtech.org/standards/qti/index

Potential future use:

```text
internal governed SOURCE_QUESTION / generated-item contracts
        ↓ export adapter
QTI-compatible packages
```

QTI portability must not determine problem-family authority, answer correctness or learner-demand legality.

### 7.3 Standards mapping principle

External standards are interoperability targets, not permission to weaken local governance:

```text
INTERNAL CANONICAL AUTHORITY
        ↓
explicit translation
        ↓
EXTERNAL INTEROPERABILITY FORMAT
```

Never reverse this into:

```text
external-format validity
        ↓
subject authority
```

## 8. Generic STEM kernel

The long-term generic kernel should own only cross-subject concerns:

```text
identity
scope and membership
provenance
maturity
exact-reference custody
discovery non-authority
research evidence promotion
learner calibration
learning-purpose control
prerequisite / transition composition
assessment custody
TTU lifecycle
publication lifecycle
versioning / invalidation
risk / limitation reporting
```

It should not directly encode algebra, Euclidean geometry, chemical bonding, stoichiometry or reaction mechanisms.

## 9. Subject Adapter contract

A subject adapter should expose governed subject objects and subject-specific validation while satisfying a generic interface.

Proposed adapter manifest concepts:

```text
subject_id
adapter_version
canonical_registry_ref
authority_validator_ref
discovery_provider_ref
supported_object_types[]
supported_representation_types[]
supported_verification_types[]
subject_specific_safety_policy_refs[]
interoperability_exporters[]
```

The generic kernel may ask:

```text
resolve this exact subject identity;
return prerequisite closure;
return canonical objects;
validate this transformation;
validate this representation;
validate this verification rule;
```

It must not ask:

```text
if subject == MATHEMATICS and topic == QUADRATICS ...
```

## 10. Mathematics adapter target

Mathematics requires first-class support for at least:

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

These already substantially exist in the current Canonical Domain Registry. Future library work should compose and enrich these authorities rather than create duplicate mathematical copies.

Additional Mathematics-specific validation may cover:

```text
domain/constraint legality
equivalent transformations
proof/derivation dependencies
special and limiting cases
symbol ↔ graph ↔ geometry ↔ table mappings
counterexamples
independent verification
```

## 11. Chemistry adapter target

Chemistry provides an important stress test because its knowledge objects and representations differ materially from Mathematics.

ACS high-school guidance emphasizes connecting macroscopic phenomena, particulate/submicroscopic models and symbolic representations (Johnstone's Triangle):
https://www.acs.org/education/policies/middle-and-high-school-chemistry/teaching-and-assessment.html

A Chemistry adapter should therefore support first-class subject objects such as:

```text
CHEMICAL_ENTITY
SUBSTANCE / SPECIES
MACRO_OBSERVATION
PARTICLE_MODEL
SYMBOLIC_REPRESENTATION
REACTION
REACTION_CONDITION
STOICHIOMETRIC_RELATION
MECHANISM when in scope
THERMODYNAMIC_STATE / RELATION
KINETIC_MODEL
PERIODIC_PROPERTY_RELATION
NOMENCLATURE_RULE
EXPERIMENTAL_OBSERVATION
MEASUREMENT / UNIT / UNCERTAINTY
HAZARD / LAB_SAFETY_CONSTRAINT
```

Potential authoritative technical-source roles include IUPAC terminology and curated NIST property data. References:

- https://goldbook.iupac.org/
- https://www.nist.gov/programs-projects/nist-chemistry-webbook

These are source-role examples, not hard-coded universal source assignments.

Chemistry must also add explicit safety governance where learner-facing experimental procedures are involved. A generic Blueprint cannot infer laboratory safety from plausibility.

## 12. Core Spec treatment of research

Research must remain divided into at least three conceptually distinct functions:

```text
SOURCE / SCOPE VERIFICATION
    what is officially supported?

SUBJECT TECHNICAL VERIFICATION
    is the subject claim valid?

PEDAGOGY ENRICHMENT
    how should valid subject matter be represented, explained,
    decomposed, contrasted or transferred?
```

Pedagogy evidence cannot create mathematical or chemical truth.

The current claim-level promotion model should remain the pattern:

```text
discovery
→ decision
→ explicit claim
→ support/contradiction classification
→ confidence
→ contradiction resolution
→ promoted binding
```

## 13. Average-agent reproducibility as a formal quality attribute

The Core Spec should define an eventual `COLD_START_REPRODUCIBILITY` benchmark.

Given the same exact inputs, different agents should have near-zero variance on canonical outputs such as:

```text
scope identities
Engineering/subject identities
prerequisite closure
canonical object refs
question/source custody
problem-family identity
research requirements
learner-calibration policy/result
release blockers
```

Acceptable variability includes:

```text
wording
optional analogy
presentation ordering inside allowed constraints
selection among several equally legal examples
search breadth before promotion
```

A proposed future metric is a **Canonical Drift Rate** calculated only over fields that should be deterministic. It must not score prose style.

## 14. Risks and limitations that the Core Spec must declare openly

The final Core Spec should maintain a visible risk register rather than imply completeness.

At minimum include these classes:

| Risk | Why it matters | Required control direction |
|---|---|---|
| Human subtopic ambiguity | one phrase may map to several legal capabilities | discovery separated from exact authority |
| Grade vs future-exam target | bridge content can be mistaken for current curriculum | explicit foundation / bridge / out-of-scope partition |
| Coarse knowledge percentage | one scalar hides uneven capability knowledge | percentage as support prior, not mastery truth |
| Agent capability dependence | thin data forces model reasoning to become hidden authority | richer governed reasoning substrate + reproducibility benchmark |
| Research contextuality | pedagogical effects are not universal | claim/context/confidence custody |
| Duplicate truth | a library can become a second subject registry | composition by exact canonical refs |
| Schema proliferation | agents cannot recover which contract governs | Architecture Catalog + generated docs |
| Documentation drift | manually repeated doctrine diverges | one normative root + generated reference tables |
| Source freshness | URLs and standards change | captures, versions, digests, stale-state handling |
| Copyright/licensing | question reuse may be restricted | explicit rights/reuse metadata |
| Narrow goldens | one corpus does not prove generality | multidimensional stress matrix |
| Chemistry safety | plausible generated procedure may be unsafe | subject-specific safety authority + hard gates |
| Renderer success mistaken for pedagogy success | valid PDF can still teach poorly | semantic/product-quality review remains separate |

## 15. Versioning and migration rules

The consolidated architecture should distinguish:

```text
schema version
policy version
subject-adapter version
library-pack version
source capture version
run/release identity
```

A change must declare whether it is:

```text
NON_BREAKING_METADATA
COMPATIBLE_EXTENSION
BREAKING_SCHEMA
AUTHORITY_SEMANTICS_CHANGE
DEPRECATION
```

Breaking authority changes require migration evidence, not silent recompilation.

Every migration should preserve old release reproducibility where retained artifacts claim reproducibility.

## 16. Proposed consolidation sequence

### Stage C0 — independent audit first

Consume the Phase-1 Core Architecture / Documentation Drift Audit.

Do not rewrite the canonical document before reviewing the audit because doing so can erase useful evidence about where drift occurred.

### Stage C1 — Architecture Catalog

Create the machine-readable catalog and catalog validator.

Initially classify; do not change production semantics.

### Stage C2 — normative-root consolidation

Use audit evidence to decide which current doctrine is:

```text
CURRENT + EXECUTABLE
CURRENT + DOCUMENTED ONLY
STALE
ROADMAP
CONFLICTED / OWNER DECISION REQUIRED
```

Then consolidate the root specification.

### Stage C3 — generated references

Generate schema/policy/validator/test tables from the catalog.

### Stage C4 — subject-adapter interface

Extract the cross-subject contract from current Mathematics behavior without weakening Mathematics validation.

### Stage C5 — Subtopic Intelligence Library contracts

Introduce the library only after the authority boundaries above are explicit.

### Stage C6 — Mathematics pilot

Use one high-stress vertical such as Theory of Equations with Grade-9 foundation and future JEE trajectory.

### Stage C7 — cross-agent reproducibility

Run identical governed inputs through multiple agent capability levels.

### Stage C8 — Chemistry pilot

Implement one bounded Chemistry vertical to falsify Mathematics-shaped assumptions.

### Stage C9 — scale population

Only after the ontology survives the pilots should large parallel library creation begin.

## 17. What must not happen during consolidation

Do not solve documentation complexity by weakening technical contracts.

Do not create one giant schema that duplicates every subsystem.

Do not move topic-specific Mathematics into a generic STEM runtime.

Do not move Chemistry truth into shared logic merely to make both subjects look syntactically identical.

Do not let interoperability standards become local authority.

Do not convert learner knowledge percentage into hidden global difficulty bands.

Do not interpret a successful generated artifact as proof that authority provenance is complete.

## 18. Promotion gate for this roadmap

This document may become input to a normative Core Specification only after:

```text
Phase-1 drift audit reviewed;
current executable doctrine identified;
owner conflicts explicitly resolved;
Architecture Catalog design accepted;
Subtopic Intelligence Library ownership boundary accepted;
Mathematics subject adapter boundary accepted;
Chemistry safety/representation requirements acknowledged;
known limitations retained rather than edited away.
```

Until then it remains a design roadmap, not architecture authority.
