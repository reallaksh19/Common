# Software design blueprint

## WHEN TO APPLY
Apply when the slice changes module boundaries, state ownership, data flow, public contracts, dependency direction, lifecycle, persistence, concurrency, or architectural responsibility. Do not apply merely because a file is edited.

## REQUIRED INPUTS
Current architecture/context capsule, protected invariants, allowed/prohibited scope, affected interfaces, downstream consumers, acceptance criteria, and relevant Owner decisions.

## PROCEDURE
1. Trace the current production path and identify the authority owner for each changed responsibility.
2. State the proposed responsibility change and why the existing boundary is insufficient.
3. Check dependency direction, lifecycle ownership, compatibility, failure propagation, and migration needs.
4. Compare at least one simpler alternative and record why it is rejected.
5. Verify the design against acceptance and protected invariants before implementation is considered complete.

## BEST-PRACTICE CHECKLIST
- One authoritative owner per rule/state transition.
- Explicit interfaces and failure semantics.
- No hidden fallback authority or duplicated business policy.
- Compatibility and rollback/migration considered where state or API shape changes.
- New abstraction earns its complexity through a current requirement.

## ANTI-PATTERNS
Shotgun architecture changes, speculative frameworks, dual sources of truth, circular dependencies, hidden mutable globals, abstraction without a current consumer, and mixing Owner-intent decisions into implementation convenience.

## REQUIRED ARTIFACTS
Architecture note or QRV evidence describing before/after responsibility, affected interfaces, chosen alternative, protected invariants, and any migration/compatibility impact.

## VERIFICATION
Trace representative requests/events end to end; inspect changed dependency edges; verify tests cover contract boundaries and failure paths; confirm no prohibited domain became an implicit dependency.

## QUALITY FINDING CLASSIFICATION
Use DESIGN for responsibility/boundary flaws and MAINTAINABILITY for avoidable complexity or duplication. Findings can remain NEEDS_ATTENTION without stopping execution.

## TRUE HARD-STOP CONDITIONS
Only map to a stop when the design violates authority, a protected invariant, repository state, or creates an unsafe engineering result. Architectural preference alone is never a hard stop.

## OWNER REPORT
Explain the user/product effect, the responsibility change, retained compatibility, material risks, and any genuine Owner decision in plain language.

## SUCCESSOR HANDOVER
Record unresolved design risks, deferred alternatives, compatibility assumptions, and the exact interfaces a successor must not reinterpret silently.
