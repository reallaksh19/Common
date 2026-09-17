# Shared Cross-Domain Prerequisite Protocol

This directory owns only the transport, routing, custody, and receipt shape for prerequisites that cross subject boundaries in V2. It does not own subject semantics and cannot declare a provider prerequisite ready.

## Authority boundary

- The consumer subject discovers that one of its governed engineering gates requires an external prerequisite.
- `registry/domain-provider-registry.v1.json` routes the prerequisite namespace to the owning provider subject and provider repository root.
- If no provider-owned READY receipt exists, the consumer emits a schema-valid `OPEN_HELD` demand. An unknown provider emits `OPEN_UNROUTABLE`.
- A READY receipt is legal only when its repository source is under the registered provider root, its provider identity matches the registry, its digest is recomputed successfully, and every evidence reference exists in the repository.
- Consumers may validate and consume provider receipts; they may not create provider truth for another subject.

The Shared contracts are subject-neutral transport contracts. Provider subjects remain responsible for their own semantic, review, and release rules. Consumer-specific closure semantics remain in the consumer subject.

## Normative files

- `contracts/domain-prerequisite-authority.schema.json`
- `contracts/domain-prerequisite-demand.schema.json`
- `registry/domain-provider-registry.v1.json`

Current registry coverage is intentionally limited to repository-backed namespace ownership. Missing namespace mappings must fail closed rather than be inferred.
