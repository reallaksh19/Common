# Engineering Coding Policy

Repository-specific standards override these general preferences unless they conflict with an explicit task requirement or engineering-safety rule.

## Structure

Prefer cohesive modules. Approximate limits of 300 physical lines for new JS/TS modules and 40 logical lines for functions are review heuristics, not correctness gates. Do not split cohesive engineering logic merely to satisfy a line count.

Split large existing files only when directly required by the task or when the change cannot be made safely without clarifying ownership.

Use branch history instead of committed `.bak`, `.old`, or copied-source backups.

## Design

Prefer:

- named exports;
- pure functions for deterministic transformations/calculations;
- explicit state ownership;
- bounded mutation at UI/runtime/store/transaction boundaries;
- explicit dependencies where authority matters.

Avoid:

- hidden globals;
- implicit singleton authority;
- mutation-heavy shared-object designs;
- duplicate sources of truth.

## Mocks, defaults, shims, abstractions

- No hidden/default mocks in production.
- No silent fallback engineering data.
- No placeholder production calculations.
- No temporary authority-changing shims.
- Compatibility adapters must be explicit, bounded, tested, and production-consumed.
- Every new adapter, resolver, service, session, store, or abstraction must have a real production consumer in the same PR.
- New unused production modules: `0`.
- No speculative infrastructure.
- If unavoidable hard-coded/default behavior exists, expose it clearly where relevant and document the authority/rationale.

## Scope control

- No broad unrelated refactor.
- No unrelated dependency upgrade.
- No generated-data churn unless required.
- No abandoned feature flags.
- No unrelated cleanup or formatting churn.
