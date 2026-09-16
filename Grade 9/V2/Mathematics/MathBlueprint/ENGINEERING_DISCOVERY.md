# Mathematics Engineering Discovery Boundary

> **Consolidated Specification Notice**:
> This document is consolidated under the canonical subordinate module [`ENGINEERING_AUTHORITY.md`](ENGINEERING_AUTHORITY.md) as part of Mathematics V2 Specification Consolidation. It is preserved here for contract stability, historical references, and granular analysis.

This document is normative for the non-authoritative discovery surface that precedes Mathematics Engineering authorization.

The architectural rule is:

> **Discovery may be permissive. Authority may not be.**

A learner, author, teacher, assessment tool, search tool or model may use natural-language wording, approximate text, governed aliases, hints or external research to find plausible Engineering candidates. None of those mechanisms creates Engineering authority.

## 1. Authority flow

```text
natural-language need / search / alias / hint / external research
        ↓
NON-AUTHORITATIVE ENGINEERING DISCOVERY
        ↓
canonical registry text + governed discovery vocabulary
        ↓
deterministic generated discovery index
        ↓
ranked candidate identities
        ↓
EXPLICIT EXACT-ID SELECTION
        ↓
standard Mathematics Engineering request
        ↓
UNCHANGED EXACT AUTHORITATIVE RESOLVER
        ↓
current registry validation
        ↓
requested depth evaluation
        ↓
transitive prerequisite closure
        ↓
Engineering authorization or BLOCK
```

The discovery layer may help a user find an identity. It may not decide that an identity is authoritative.

## 2. Contracts and governed data

Discovery request:

`contracts/mathematics-engineering-discovery-request.schema.json`

Discovery receipt:

`contracts/mathematics-engineering-discovery-receipt.schema.json`

Explicit selection:

`contracts/mathematics-engineering-discovery-selection.schema.json`

Discovery vocabulary schema:

`contracts/mathematics-engineering-discovery-vocabulary.schema.json`

Governed discovery vocabulary:

`policies/mathematics-engineering-discovery-vocabulary.v1.json`

Compiler:

`engine/compile_mathematics_engineering_discovery.py`

Vocabulary validator:

`engine/validate_mathematics_engineering_discovery_vocabulary.py`

The discovery receipt is schema-locked to:

```text
view_class = NON_AUTHORITATIVE_ENGINEERING_DISCOVERY
authority = CANDIDATE_DISCOVERY_ONLY
technical_authorization = NOT_EVALUATED
publication_authorization = NOT_IMPLIED
automatic_selection = false
requires_explicit_exact_selection = true
```

These values are the formal boundary preventing ranking from becoming authorization.

## 3. Governed discovery vocabulary

Topic-specific aliases belong in governed data, never in topic branches in Blueprint Python.

The vocabulary catalog may contain only discovery metadata:

```text
exact existing target scope kind
exact existing target scope ref
phrase
term class
```

Supported term classes are learner aliases, competition terms, technical terms, notation names, common abbreviations and regional variants.

The catalog explicitly carries:

```text
authority = NON_AUTHORITATIVE_DISCOVERY_VOCABULARY
technical_authorization = NOT_EVALUATED
publication_authorization = NOT_IMPLIED
```

Its schema has `additionalProperties = false`, so vocabulary entries cannot smuggle Engineering readiness, mathematical truth, depth admission or publication authority into discovery.

The catalog binds to the stable Engineering registry identity and to exact existing gate/bucket targets. It deliberately does **not** bind to the entire current registry digest. That would create unnecessary maintenance coupling: adding or revising an unrelated Engineering gate should not require editing a vocabulary file that does not mention it.

Validation fails closed when:

- the registry identity is wrong;
- a target gate or bucket does not exist;
- the same target is declared twice;
- two phrases normalize to the same term for one target; or
- the catalog violates its non-authoritative schema.

The catalog is intentionally sparse. Every current gate and linked bucket is indexed automatically from canonical registry data; curated vocabulary only improves discoverability where natural terminology differs from canonical labels.

## 4. Deterministic generated index and exact receipt custody

The compiler constructs a deterministic non-authoritative index from:

```text
current canonical Engineering registry
+ current governed discovery vocabulary
```

Every index row carries an exact gate/bucket identity, learner-facing label, linked gate identities, a digest of current indexed Engineering text and any curated vocabulary terms.

The generated index is not stored as mathematical authority. Every discovery receipt binds the exact state actually used:

```text
registry_digest
vocabulary_catalog_digest
discovery_index_digest
```

This is the strict boundary. The catalog may survive an unrelated registry change, but a previously issued discovery receipt may not. Promotion recomputes discovery against the current registry and current vocabulary. Registry drift, vocabulary drift, index drift or receipt mutation makes the receipt stale/forged.

That gives the intended balance:

```text
loose catalog maintenance coupling
+ exact per-discovery custody
+ exact selection
+ unchanged authoritative resolver
```

## 5. Discovery may be approximate

The current compiler performs deterministic approximate lexical discovery over current Engineering registry data, governed discovery vocabulary and optional user-provided hints. It can use:

- exact candidate identity;
- exact or partial learner-facing label;
- identity-token overlap;
- learner-label token overlap;
- current Engineering content-token overlap;
- approximate label similarity;
- exact, phrase, token and approximate vocabulary matches;
- user-provided search hints; and
- linked-gate text when discovering a bucket.

Future implementations may add embeddings, semantic search, web-assisted query expansion or model-generated candidate hints, provided they remain candidate-finding only and the resulting receipt remains bound to the exact governed discovery inputs used.

## 6. Discovery is intentionally permissive

Discovery does **not** perform technical admission. It may surface a candidate whose current Engineering state is incomplete, held, out of scope for a particular source, or insufficient for the requested depth.

The receipt may display declared readiness/source-scope metadata for usability, but those fields are explanatory only.

Search should help a user find what exists; authorization should decide whether it may be consumed.

## 7. Exact selection is mandatory

A ranked candidate is not automatically selected.

To move from discovery into the authoritative request path, a separate selection object must provide:

```text
exact discovery_id
exact discovery_receipt_digest
selected_scope_kind
selected_scope_refs
engineering_depth
learning_purpose
explicit_selection_acknowledgement = EXACT_IDENTITY_CONFIRMED
```

The selected exact identities must exist in the exact digest-bound candidate set. A stale, modified or unrelated discovery receipt fails closed.

The selection compiler emits the existing standard Mathematics Engineering request format. It does not authorize the request.

## 8. Existing exact resolver remains authoritative

`compile_mathematics_engineering_workbench.py::resolve_manifest()` remains unchanged as the authoritative resolver.

It accepts only:

1. exact Engineering Gate identity; or
2. exact `linked_buckets` membership.

Natural-language labels, approximate matches, governed aliases, semantic similarity, model output, web search output and conversation memory still fail if supplied directly as authoritative scope refs.

Therefore:

```text
discovery candidate ≠ Engineering authority
rank 1 ≠ Engineering authority
vocabulary match ≠ Engineering authority
high similarity ≠ Engineering authority
model confidence ≠ Engineering authority
web evidence ≠ Engineering authority

explicit exact identity
+ unchanged exact resolver
+ current Engineering validation
+ requested depth PASS
+ prerequisite closure PASS
= technical authorization may proceed
```

## 9. Falsification requirements

CI must prove at least these properties:

```text
discovery output is explicitly non-authoritative
approximate discovery does not weaken exact authoritative resolution
governed aliases improve candidate discovery but cannot authorize directly
no rank is auto-selected
selection requires exact candidate identity
selection is bound to exact discovery digest
registry drift stales discovery selection
vocabulary drift stales discovery selection
unrelated registry changes do not require a vocabulary-catalog edit
unknown vocabulary targets fail closed
duplicate normalized target terms fail closed
vocabulary cannot carry readiness/authorization payloads
held candidates may be discoverable but remain blocked by Engineering authority
bucket discovery still requires exact bucket identity before authoritative resolution
generic Blueprint topic-independence remains intact
```

The dedicated Engineering workflow validates the vocabulary and executes these discovery falsifiers before registry-wide Blueprint authorization proof.

## 10. Non-regression rule

A future discovery change is invalid if it allows any of the following:

```text
rank-1 auto-authorization
similarity-threshold authorization
vocabulary-term authorization
LLM/model-confidence authorization
web-search-result authorization
alias-to-gate authorization without explicit exact selection
promotion from a stale registry/vocabulary/index receipt
promotion of an identity outside the bound candidate set
discovery metadata overriding current Engineering readiness
publication authorization inferred from discovery
```

The final invariant is:

> **Use permissive tools and governed vocabulary to find candidates; bind what the user saw exactly; use exact identities and current Engineering authority to authorize them.**
