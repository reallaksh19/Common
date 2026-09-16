# Subtopic Intelligence Library — Compilation and Custody Model

> **Status: DESIGN / NON-NORMATIVE**
>
> This file resolves one major design question left implicit by the SIL roadmap: the mature Subtopic Intelligence Pack should be a **compiled, digest-bound context view**, not a manually duplicated store of subject truth.

## 1. Central rule

```text
AUTHORITATIVE / GOVERNED REGISTRIES
        ↓
GENERIC SIL COMPILER
        ↓
COMPILED SUBTOPIC INTELLIGENCE PACK
        ↓
AGENT CONTEXT PACK / downstream generation
```

The compiled pack does not become a new authority layer merely because it gathers several authorities in one place.

Its purpose is reproducibility and bounded context.

## 2. Why compilation matters

A manually authored monolithic pack would eventually drift because the same information could be edited in several places:

```text
Engineering equation
SIL copy of equation
Core1A copy of equation
question-bank annotation
prompt text
```

The desired model is instead:

```text
ONE canonical subject object
        ↓ exact refs
many legal compositions / uses
```

The pack should therefore retain references, custody digests and composition decisions, not duplicate canonical payloads except where a frozen snapshot is explicitly needed for reproducibility and clearly marked as a snapshot of another authority.

## 3. Proposed source registries

The compiler should eventually consume exact current states from domains such as:

```text
SUBJECT / ENGINEERING AUTHORITY
    gates, exact prerequisites, subject technical objects

CANONICAL DOMAIN REGISTRY
    concepts, models, equations, derivations, capabilities,
    learning atoms, representations, misconceptions,
    problem families, questions, solutions, verification

SCOPE AUTHORITY
    curriculum / exam / owner-approved memberships

LEARNING TRANSITION REGISTRY
    instructional / repair / representation transitions

SOURCE SELECTION PROFILE REGISTRY
    role and suitability rationale

ASSESSMENT / QUESTION BANK AUTHORITY
    source questions, problem-family and answer custody

PEDAGOGY RESEARCH MANIFESTS
    promoted claims and evidence

OWNER DECISIONS
    explicit overrides / waivers where legally permitted
```

Not every pack requires every source domain.

## 4. Proposed pack authority locks

A compiled pack should eventually schema-lock semantics equivalent to:

```text
view_class = COMPILED_SUBTOPIC_INTELLIGENCE_CONTEXT

authority = COMPOSITION_OF_BOUND_GOVERNED_REFERENCES

technical_authorization = NOT_GRANTED_BY_PACK

publication_authorization = NOT_IMPLIED

learner_mastery_claim = NOT_IMPLIED
```

The pack may contain references to an Engineering receipt whose technical authorization is `ALLOWED`. That does not mean the pack itself is the authority that granted it.

## 5. Generic compilation inputs

A compile request should contain only generic inputs such as:

```text
subject_id
subject_adapter_ref
canonical_subtopic_ref
scope_request_refs[]
learning_purpose
requested_engineering_depth
optional target-program refs[]
question-bank refs[]
research-policy refs[]
owner-decision refs[]
```

Free-text discovery labels should already have crossed the explicit exact-selection boundary before compilation.

## 6. Compilation algorithm

A generic compiler can follow this sequence:

```text
1. VALIDATE SUBJECT ADAPTER

2. REVALIDATE EXACT SUBJECT AUTHORITY

3. RESOLVE EXACT SCOPE MEMBERSHIP

4. COMPUTE REQUIRED SUBJECT / PREREQUISITE CLOSURE

5. SELECT CANONICAL DOMAIN OBJECTS BY EXACT IDENTITY

6. LOAD GOVERNED LEARNING TRANSITIONS

7. LOAD ASSESSMENT / PROBLEM-FAMILY EVIDENCE

8. LOAD SOURCE-SELECTION PROFILES

9. LOAD REQUIRED PROMOTED PEDAGOGY RESEARCH

10. CHECK COVERAGE PROFILE

11. EMIT EXPLICIT GAPS

12. BIND ALL MATERIAL DEPENDENCIES

13. COMPUTE PACK DIGEST

14. EMIT COMPILED PACK
```

No step should branch on a topic name.

## 7. What the compiler must not do

Forbidden:

```text
infer a missing logical prerequisite from semantic similarity;
create a missing equation;
create curriculum membership from a source article;
auto-resolve an ambiguous discovery candidate;
invent learner knowledge;
turn preferred source into subject authority;
turn a coverage PASS into publication authorization;
auto-close a library gap by generating plausible prose.
```

The compiler reports gaps to the correct owner.

## 8. Dependency custody

The pack should bind only dependencies material to the compiled context.

Proposed binding record:

```text
dependency_id
dependency_domain
dependency_ref
digest_or_version
materiality
staleness_action
```

Draft `materiality`:

```text
IDENTITY
SUBJECT_TRUTH
SCOPE
LEARNING_STRUCTURE
ASSESSMENT
PEDAGOGY
SOURCE_SELECTION
OWNER_CONTROL
```

Draft `staleness_action`:

```text
BLOCK_RECOMPILE_REQUIRED
REVIEW_REQUIRED
ADVISORY_REFRESH
```

This avoids both extremes:

```text
bind nothing → stale packs silently survive
```

and:

```text
bind entire repository → unrelated change invalidates everything
```

## 9. Example invalidation matrix

| Change | Expected effect |
|---|---|
| Exact subject gate identity removed/changed | pack BLOCKED / recompile |
| Material canonical equation payload changed | pack stale / recompile |
| Logical prerequisite graph changed | pack stale / closure recompute |
| Instructional transition wording metadata changed | transition-dependent pack refresh/review |
| Unused source profile changed | no effect on pack |
| Bound preferred-source profile changed | source-selection portion stale |
| Discovery vocabulary changes after exact selection | compiled pack normally unaffected unless discovery receipt is part of required audit custody |
| Learner percentage changes | canonical SIL pack unchanged; run/LAU context changes |
| Pedagogy claim used by pack changes | pedagogy binding stale |
| Unrelated Engineering gate added | no automatic manual SIL edit required |

The exact implementation should be derived from authority semantics, not from filename timestamps.

## 10. Pack versus Agent Context Pack

Keep two objects separate.

### 10.1 Subtopic Intelligence Pack

Reusable subject/context composition.

It answers:

```text
What is the governed structure of this subtopic for these exact scope bindings?
```

### 10.2 Agent Context Pack

Run-specific bounded context.

It additionally includes:

```text
run manifest
learner calibration
purpose
requested product/core
relevant schemas
validation commands
output obligations
current known gaps
```

It answers:

```text
What does this particular agent need for this particular run?
```

Do not bake one learner's `70%` knowledge state into the reusable canonical subtopic pack.

## 11. Pack compilation versus library authoring

Library authoring edits the owning registries:

```text
add/review learning transition
curate source-selection profile
add assessment mapping
repair subject authority
resolve scope mapping
promote pedagogy claim
```

Compilation only assembles validated current records.

This separation enables many research agents to propose library content while one deterministic compiler enforces current authority.

## 12. Gap routing

When compilation fails, route the gap by ownership.

```text
missing subject truth
    → Engineering/domain owner

missing logical prerequisite
    → Engineering owner

missing instructional bridge
    → Learning Transition registry

missing problem-family/question evidence
    → Core2 / assessment owner

missing preferred source rationale
    → Source Selection registry

missing pedagogy evidence
    → research workflow

missing learner policy
    → LAU/calibration owner

missing scope authority
    → scope/owner adjudication
```

A generic compiler should emit the owning domain in every gap.

## 13. Compiled-pack coverage

Coverage should prove presence of **required reasoning categories**, not object-count quotas.

A coverage profile can require categories such as:

```text
subject identity
scope partition
logical prerequisite closure
instructional transition coverage
canonical object coverage
representation coverage
misconception/repair coverage where relevant
assessment/problem-family coverage
verification coverage
source strategy
research promotion where required
known-gap disclosure
```

Each resolves to:

```text
SATISFIED
NOT_APPLICABLE with reason
BLOCKED with gap ref
```

## 14. Reproducibility property

For exact same dependency states and compile request:

```text
compiled canonical references
scope partition
transition references
source-profile references
coverage state
gap refs
pack digest
```

must be deterministic.

The pack must not depend on which LLM happened to run the compiler.

An LLM may assist upstream discovery/curation. It cannot be the hidden implementation of the pack compiler.

## 15. Relationship to cold-start agents

A mature workflow becomes:

```text
human request
        ↓
non-authoritative discovery
        ↓
explicit exact selection
        ↓
subject authorization
        ↓
compile SIL pack
        ↓
compile run-specific Agent Context Pack
        ↓
average cold-start agent
        ↓
governed generation / audit
```

This is the intended answer to agent drift: shrink the amount of stable structure the agent must reconstruct from prose.

## 16. Cross-agent benchmark

Given one compiled pack + one run context, compare agents.

Canonical fields should match:

```text
scope refs
subject refs
transition refs
problem-family refs
source roles
research requirements
calibration refs
reported blockers
```

Narrative prose may differ.

If canonical structure differs materially between agents, one of two things is wrong:

```text
the context pack is incomplete
or
the output contract leaves an authority decision to the agent
```

That difference should create a library/schema improvement task.

## 17. Theory-of-Equations pilot

The first real pack should be compiled rather than manually assembled as a final artifact.

The pilot process should therefore first populate/review the missing owning registries, then compile:

```text
Grade-9 foundation scope
+
future JEE bridge scope
+
exact Mathematics authority
+
learning transitions
+
problem families / question evidence
+
source-selection profiles
+
pedagogy research
```

into a pack.

If a stable piece of reasoning exists only in the final generated prompt, treat that as a defect candidate.

## 18. Chemistry stress test

A later Chemistry pack should use the same compiler interface while different subject-adapter data supplies objects such as:

```text
species
macro observations
particle models
symbolic representations
reactions / conditions
stoichiometric relations
reference data
safety constraints
```

The generic compiler should operate on exact adapter-declared object classes rather than contain Chemistry topic logic.

## 19. Production-readiness condition

Do not promote the compiled-pack architecture until a validator proves:

```text
pack cannot duplicate or override subject truth;
pack cannot authorize publication;
all exact refs resolve;
material dependencies are digest/version bound;
stale material dependencies fail closed;
unrelated changes do not cause unnecessary manual coupling;
gap ownership is explicit;
compilation is deterministic;
learner state remains run-specific;
Theory-of-Equations pilot is reproducible;
non-algebra Mathematics works;
Chemistry works through adapter data.
```

## 20. Central doctrine

> The Subtopic Intelligence Library is best understood as governed reusable registries plus a deterministic compiler, not as one giant hand-authored topic document.
>
> The compiled pack tells an agent what exact authorities, learning transitions, evidence and source choices belong together. It does not become the authority that created those things.
