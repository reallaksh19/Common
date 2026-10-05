# Project-specific acceptance contract

Common v1.1 deliberately does not know project semantics.

A project protocol is an exact, versioned engineering-acceptance contract. It declares criteria, verification method IDs, Super Reviewer harnesses, fixtures/oracles and external gates. TASK pins it by exact repository/commit/path and digest.

Super Reviewer executes that contract against the exact candidate. Product fixes are allowed; changing the protected acceptance surface during the same certification attempt is not.

Common may define a shared verification vocabulary without making every class mandatory: POSITIVE, NEGATIVE, BOUNDARY, INVARIANT, ROUND_TRIP, METAMORPHIC, PROPERTY, DIFFERENTIAL, FAULT_INJECTION, ROLLBACK, IDEMPOTENCY, REPLAY, CONCURRENCY, PRODUCER_CONSUMER, FUZZ, PERFORMANCE, EXTERNAL_ORACLE, MANUAL_VISUAL, SECURITY.

The project decides which methods apply. Common checks declared requiredness, evidence class, result semantics, source/context freshness and protected-surface integrity.
