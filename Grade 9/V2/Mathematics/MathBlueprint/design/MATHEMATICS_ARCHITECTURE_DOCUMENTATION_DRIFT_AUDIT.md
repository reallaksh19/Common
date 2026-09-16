# Mathematics V2 — C0 Architecture / Documentation Drift Audit

> **Status: DESIGN EVIDENCE / NON-NORMATIVE**
>
> This audit records repository evidence for C2 consolidation. It does not alter runtime, subject, Engineering, product or publication authority. Production behavior remains governed by the existing schemas, policies, validators, compilers, release gates and normative subsystem specifications outside `design/`.

## Audit method

The audit was performed against repository head:

`0f5a09ca2fcb30c0669dc7ba4ee76b5531bac7cb`

The method is intentionally independent of the C1 catalog:

```text
schemas / governed policies / validators / compilers / release path
        ↓
independently derived executable architecture model
        ↓
compare normative documentation
        ↓
classify drift
        ↓
only then compare C1 catalog
```

The C1 catalog was **not** used as authority or as the source model. This is methodological independence from C1, not a claim that an external third party performed the review.

The classification vocabulary is the one prescribed by the consolidation roadmap:

```text
CURRENT + EXECUTABLE
CURRENT + DOCUMENTED ONLY
STALE
ROADMAP
CONFLICTED / OWNER DECISION REQUIRED
```

## Result

C0 found **seven material architecture/documentation findings** and **zero owner-decision blockers**.

C2 status:

```text
READY_WITH_DOCUMENTATION_REMEDIATIONS
```

That status does **not** mean every documented capability is fully implemented. In particular, C0-F007 identifies one `CURRENT + DOCUMENTED ONLY` compiler-path gap that C2 must label accurately rather than silently upgrading to executable status.

The status also does **not** mean the design folder becomes normative. It means the repository contains enough evidence to consolidate the root specification without inventing new architecture decisions.

## Finding C0-F001 — canonical authority topology is stale

**Classification:** `STALE`  
**Severity:** HIGH

`CANONICAL_ARCHITECTURE.md` still presents the principal authority path as Ground Truth → Core1/Core2 → Canonical Domain Registry and ends with the doctrine that Core1 determines semantic authority.

That description is no longer complete enough to be the canonical authority topology.

Current normative and executable evidence establishes an upstream Mathematics Engineering layer:

```text
non-authoritative discovery
        ↓
explicit exact identity
        ↓
current Engineering registry
        ↓
generic Engineering validation + depth
        ↓
transitive prerequisite closure
        ↓
Engineering authorization binding
        ↓
Canonical Domain admission / projection
        ↓
Core products
```

The correct reconciliation is **layered authority**, not deletion of Core1/Core2 roles:

```text
Engineering
    = technical mathematical authority and exact mathematical identities

Core1
    = semantic reconstruction authority inside authorized mathematics

Core2
    = assessment / source-question authority inside authorized mathematics
```

This distinction is supported both by the current Engineering boundary and by the still-active Canonical Domain schema, which retains Core1/Core2 authority classes for base domain assets.

**C2 action:** rewrite the root authority topology to include Engineering upstream, while preserving the narrower Core1/Core2 distinction.

## Finding C0-F002 — EASY research rule is contradictory

**Classification:** `STALE`  
**Severity:** HIGH

`DUAL_TRACK_PRODUCT_MODEL.md` says:

```text
EASY → no pedagogy-enrichment web research
```

Current generation governance says instead:

```text
EASY   → research OPTIONAL; if used, binding must be complete
MEDIUM → TARGETED research REQUIRED
HARD   → DEEP research REQUIRED
```

`GENERATION_CALIBRATION.md`, `SELF_TEACHING.md` and `validate_self_teaching_generation_spec.py` implement the latter policy at the generation-spec contract boundary. Tests explicitly accept a fully bound EASY research row and reject a half-bound row.

The distinction is intentional:

```text
research permission != research obligation
```

External research may improve pedagogy at any difficulty; it never creates mathematical authority.

**C2 action:** remove the EASY prohibition from the consolidated doctrine and align the dual-track documentation with optional-but-governed EASY research. C0-F007 separately records that the canonical compiler does not yet materialize this optional binding automatically.

## Finding C0-F003 — publication topology lags current release path

**Classification:** `STALE`  
**Severity:** MEDIUM

The root still describes publication principally as:

```text
validated realization + TTUs
→ LearnerPageBlueprint
→ deterministic typesetting
→ PDF
```

`math-learner-page-blueprint.schema.json` still exists, so the concept is not fictitious. However, the current governed bound-release path is materially richer:

```text
product release gate PASS
        ↓
current Engineering visibility revalidation
        ↓
semantic learner publication bundle
  - generation-spec custody
  - governed example custody
  - pedagogy-research custody
  - embedded Engineering visibility + digest
  - concept + problem components
        ↓
bundle validation
        ↓
render
        ↓
render-coverage / digest audit
```

The publication runner fails if semantic provenance drifts and requires:

`semantic_source = LEARNER_PUBLICATION_BUNDLE_ONLY`

**C2 action:** distinguish any retained internal PageBlueprint role from the actual governed publication boundary and make the semantic publication bundle the canonical bound rendering input.

## Finding C0-F004 — non-authoritative Engineering discovery is missing from the root

**Classification:** `CURRENT + EXECUTABLE`  
**Severity:** MEDIUM

The current system has a deliberate human-language usability layer before authority:

```text
natural language / aliases / approximate search
        ↓
ranked candidate exact identities
        ↓
explicit exact digest-bound selection
        ↓
unchanged exact Engineering resolver
```

The discovery receipt is explicitly candidate-only and cannot imply technical or publication authorization.

The root does not yet represent this boundary.

**C2 action:** include discovery as a non-authoritative pre-authority layer and make the exact-selection boundary explicit.

## Finding C0-F005 — claim-level pedagogy promotion is missing from the root

**Classification:** `CURRENT + EXECUTABLE`  
**Severity:** MEDIUM

The current research architecture is not merely “research dossier exists.” Promotion is:

```text
discovery
→ research decision
→ explicit pedagogy claim
→ SUPPORTS / CONTRADICTS evidence links
→ confidence
→ contradiction resolution when required
→ promoted generation binding
```

There is no universal minimum source-count quota, and pedagogy research cannot become curriculum or mathematical authority.

**C2 action:** represent the promotion boundary at architectural level without duplicating the field-level research schema into the root spec.

## Finding C0-F006 — Engineering visibility is missing from the root

**Classification:** `CURRENT + EXECUTABLE`  
**Severity:** MEDIUM

Current released products may expose Engineering provenance and structure only through a derived visibility object that is recomputed from exact current custody.

The invariant is:

```text
authority = NON_AUTHORITATIVE_VIEW_OF_BOUND_ENGINEERING_AUTHORITY
publication_authorization = NOT_IMPLIED
```

Visibility may explain Engineering authority; it cannot create it.

**C2 action:** place derived visibility between released product authority and semantic publication, explicitly outside both technical and publication authorization.

## Finding C0-F007 — optional EASY research compiler materialization is incomplete

**Classification:** `CURRENT + DOCUMENTED ONLY`  
**Severity:** MEDIUM

The governed policy and generation-spec validator support this state:

```text
EASY bucket
+ optional pedagogy research decision
+ bound research brief ref
+ bound research source refs
→ legal generation spec
```

The validator proves both sides:

```text
fully bound optional EASY research → PASS
half-bound optional EASY research  → BLOCK
```

However, the canonical `compile_sdu_lau_generation_spec.py::_bind_research()` implementation filters to:

```text
non_easy = [row for row in rows if row["difficulty_badge"] != "EASY"]
```

and writes research decision/source bindings only to those non-EASY rows. `validate_generation_research_bindings()` similarly checks promoted source retention per bucket only for non-EASY rows; an all-EASY spec with a manifest merely validates the manifest and returns.

Therefore the policy is current and validator-supported, but **automatic compiler materialization of promoted optional EASY research is not yet complete**.

This is exactly the kind of distinction the C0 classification vocabulary is intended to preserve.

**C2 action:** describe optional EASY research as current policy but mark canonical compiler materialization `CURRENT + DOCUMENTED ONLY`. Closing this gap requires a separate governed compiler migration plus a falsifier; C0 itself must not change runtime semantics.

## Confirmed current doctrine

The executable-first audit confirms these major rules as current rather than drift:

1. approximate discovery may rank candidates but exact identity is required for authority;
2. topic-specific mathematical truth belongs in governed Engineering data, not generic Blueprint topic branches;
3. Core1/Core2 retain distinct semantic/assessment roles downstream of Engineering authority;
4. canonical Engineering source identity is stored once and local teaching use is membership metadata;
5. SDU depth is intrinsic and Engineering-backed, while LAU learner fit requires governed evidence or explicit owner waiver;
6. the generation-spec validation contract allows EASY research to be absent or fully bound while MEDIUM/HARD research remains required; C0-F007 separately records the compiler materialization gap;
7. product release and current Engineering custody are revalidated before governed publication;
8. Engineering visibility is derived explainability and cannot imply publication authorization.

## C1 comparison

Only after deriving the executable model and documentation findings did the audit compare the Stage-C1 catalog.

Result:

```text
C1 components:              17
supported responsibility:   17
unsupported component IDs:  0
comparison:                  CONSISTENT_WITH_RECONCILIATION_NOTES
```

The C1 responsibility decomposition is therefore a useful candidate index for C2/C3. It is **not** promoted into authority by this finding.

Two reconciliation notes matter:

- the C1 `CALIBRATION` responsibility is real, but C0-F007 prevents C2 from describing every optional EASY research path as fully compiler-executable;
- the C1 candidate's recorded `base_head_sha` predates this audit snapshot even though the catalog describes itself as captured from the current tree. That is harmless because the candidate has `authority = NONE`, but C3 generated references should use explicit immutable source-snapshot custody rather than language implying a permanently current tree.

## C2 required remediations

C2 may now consolidate the normative root, provided it does so as an evidence-led authority/documentation migration rather than a silent runtime redesign:

```text
1. add Engineering discovery → exact selection → authorization → closure → custody upstream;
2. scope Core1/Core2 authority correctly inside that Engineering envelope;
3. correct EASY research to OPTIONAL, fully bound when used;
4. mark optional EASY compiler materialization documented-only until separately implemented;
5. represent claim-level pedagogy promotion;
6. represent derived Engineering visibility as non-authoritative;
7. make the semantic learner publication bundle the governed publication input;
8. keep design/catalog/audit files outside production authority;
9. preserve existing runtime behavior unless a separately governed migration explicitly changes it.
```

No `CONFLICTED / OWNER DECISION REQUIRED` finding was identified in C0. If C2 encounters a new conflict that cannot be resolved from existing executable/normative evidence, it must stop and surface that conflict rather than choosing a new architecture silently.
