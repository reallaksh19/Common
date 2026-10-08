# Engineering Relay v1 — R1-A provenance spine

**Governing:** [new programme #787](https://github.com/reallaksh19/Common/issues/787) → [R1-A #789](https://github.com/reallaksh19/Common/issues/789). Based on [R0 source contract](https://github.com/reallaksh19/Common/issues/788#issuecomment-6062357213). This is a **fresh, inert prototype**. Nothing here inherits the superseded V3.5 programme's approval or modifies its code.

## Pure API

`provenance-v1.mjs` exports `validate(document)`, `canonicalJSON(value)`, `traceClaim(document, claimId)`, and `ProvenanceError`. Uses only JavaScript standard features; no provider calls, tokens, filesystem, environment variables, GitHub writes or auto-rendered scoreboards.

Run `node --test skills/engineering-relay-v1/provenance-v1.test.mjs` from repository root with Node 20+.

## Contract

Required top-level document keys: `schema` = `relay-provenance-v1`, `parent_issue` = `owner/repo#number`, and arrays `owner_intents`, `claims`, `responsibilities`, `sessions`, `task_evidence`, `research_findings`, `owner_decisions`. Every node has globally unique ID. Cross references must point to existing nodes, leaf dependencies must be acyclic, sessions reference exact leaf, evidence references matching session and leaf. A coding END needs exact 40-hex SHA. Event types include OWNER_PROMPT, AGENT_RESPONSE, DECISION, CODE_CHANGE, ERROR, RECOVERY. START without END is valid to support real interruption recovery.

Owner record preserves raw_text and distinct `original_source` versus `first_durable_mirror`. Original source status only `UNKNOWN`, `CLAIMED` or `FIRST_DURABLE_MIRROR`; an original_source may **not** self-label itself as a mirror. Source locators/sha256 digests are syntactically validated but **not authenticated**.

ResearchFinding may be unverified/supported/contradicted **as a claim** and does not automatically change a plan. OwnerDecision has a `source`, but this validator **does not verify the issuer** or grant Owner acceptance. Likewise an evidence END does not establish CI success or source custody. Future R1-B/R2/R3 must read provider source and verify approval and currentness, with explicit trusted principal/readback.

**Never use `validate()` as acceptance, auth, approval, scoreboard or workflow writer permission.** Positive tests prove shape, not truth. The code does not persist transcripts; records must be supplied explicitly with privacy/retention controls upstream.

## R1-A acceptance limits / next responsibility

This leaf delivers **structural** referential integrity, typed source statuses and deterministic JSON; it does not provide durable cross-agent capture, hosted CI, actual graph authority, cryptographic attestation or live GitHub synchronization. R1-B should establish independent provider-authenticated owner/research/source decision receipts before any downstream snapshot or writer consumes these objects.
