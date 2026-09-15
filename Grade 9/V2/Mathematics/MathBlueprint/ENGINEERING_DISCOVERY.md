# Mathematics Engineering Discovery Boundary

This document is normative for the non-authoritative discovery surface that precedes Mathematics Engineering authorization.

The architectural rule is:

> **Discovery may be permissive. Authority may not be.**

A learner, author, teacher, assessment tool, search tool or model may use natural-language wording, approximate text, aliases, hints or external research to find plausible Engineering candidates. None of those mechanisms creates Engineering authority.

## 1. Authority flow

```text
natural-language need / search / alias / hint / external research
        ↓
NON-AUTHORITATIVE ENGINEERING DISCOVERY
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

## 2. Contracts

Discovery request:

`contracts/mathematics-engineering-discovery-request.schema.json`

Discovery receipt:

`contracts/mathematics-engineering-discovery-receipt.schema.json`

Explicit selection:

`contracts/mathematics-engineering-discovery-selection.schema.json`

Compiler:

`engine/compile_mathematics_engineering_discovery.py`

The discovery receipt is schema-locked to:

```text
view_class = NON_AUTHORITATIVE_ENGINEERING_DISCOVERY
authority = CANDIDATE_DISCOVERY_ONLY
technical_authorization = NOT_EVALUATED
publication_authorization = NOT_IMPLIED
automatic_selection = false
requires_explicit_exact_selection = true
```

These values are not labels of convenience. They are the formal boundary preventing ranking from becoming authorization.

## 3. Discovery may be approximate

The current compiler performs deterministic approximate lexical discovery over current Engineering registry data and optional user-provided hints. It can use:

- exact candidate identity;
- exact or partial learner-facing label;
- identity-token overlap;
- learner-label token overlap;
- current Engineering content-token overlap;
- approximate label similarity;
- user-provided search hints; and
- linked-gate text when discovering a bucket.

Future discovery implementations may add richer aliases, embeddings, semantic search, web-assisted query expansion or model-generated candidate hints, provided they preserve the same non-authoritative boundary.

Topic-specific aliases, if introduced, belong in governed discovery data rather than topic branches in Blueprint Python.

## 4. Discovery is intentionally permissive

Discovery does **not** perform technical admission. It may surface a candidate whose current Engineering state is incomplete, held, out of scope for a particular source, or insufficient for the requested depth.

The receipt may display declared readiness/source-scope metadata for usability, but those fields are explanatory only.

This is deliberate. Search should help a user find what exists; authorization should decide whether it may be consumed.

## 5. Exact selection is mandatory

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

The selection compiler then emits the existing standard Mathematics Engineering request format. It does not authorize the request.

## 6. Existing exact resolver remains authoritative

`compile_mathematics_engineering_workbench.py::resolve_manifest()` remains unchanged as the authoritative resolver.

It accepts only:

1. exact Engineering Gate identity; or
2. exact `linked_buckets` membership.

Natural-language labels, approximate matches, semantic similarity, aliases, model output, web search output and conversation memory still fail if supplied directly as authoritative scope refs.

Therefore:

```text
discovery candidate ≠ Engineering authority
rank 1 ≠ Engineering authority
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

## 7. Staleness and custody

Every discovery receipt binds:

- exact discovery request digest;
- exact current Engineering registry ID;
- exact current Engineering registry digest;
- deterministic ranked candidate set.

Promotion recomputes discovery from the request and current registry. If the registry changes, labels change, candidates change, or the receipt is altered, promotion fails as stale/forged.

This custody is intentionally separate from Engineering authorization custody. Discovery custody proves what the user saw and selected; Engineering custody proves what was technically authorized.

## 8. Falsification requirements

CI must prove at least these properties:

```text
discovery output is explicitly non-authoritative
approximate discovery does not weaken exact authoritative resolution
no rank is auto-selected
selection requires exact candidate identity
selection is bound to exact discovery digest
registry drift stales discovery selection
held candidates may be discoverable but remain blocked by Engineering authority
bucket discovery still requires exact bucket identity before authoritative resolution
generic Blueprint topic-independence remains intact
```

## 9. Non-regression rule

A future discovery change is invalid if it allows any of the following:

```text
rank-1 auto-authorization
similarity-threshold authorization
LLM/model-confidence authorization
web-search-result authorization
alias-to-gate authorization without explicit exact selection
promotion from a stale discovery receipt
promotion of an identity outside the bound candidate set
discovery metadata overriding current Engineering readiness
publication authorization inferred from discovery
```

The final invariant is:

> **Use permissive tools to find candidates; use exact identities and current Engineering authority to authorize them.**
