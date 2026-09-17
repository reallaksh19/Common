# Coding blueprint

## WHEN TO APPLY
Apply whenever production or relay implementation code changes. Documentation-only or data-only slices may mark it not applicable with a reason.

## REQUIRED INPUTS
Active EP scope, implementation steps, input/oracle contracts, coding conventions, protected invariants, existing tests, and the exact state/authority owners touched by the change.

## PROCEDURE
1. Reconfirm live route/scope before each material batch.
2. Make the smallest coherent change that advances named acceptance criteria.
3. Keep state ownership and failure semantics explicit; reuse the authoritative rule rather than duplicating it.
4. Preserve compatibility unless the roadmap authorizes a break.
5. Remove only in-scope dead paths made obsolete by the change.
6. Run narrow feedback during iteration and required verification on the exact material basis.
7. Persist discoveries, limitations, and evidence truth.

## BEST-PRACTICE CHECKLIST
- Clear names and bounded functions/modules.
- No hidden fallback authority.
- Errors preserve actionable context without leaking internal relay jargon to users.
- Deterministic behavior where protocol state is involved.
- Comments explain non-obvious why, not restate code.
- New dependencies justified and scoped.

## ANTI-PATTERNS
Drive-by refactors, copy-pasted business rules, silent exception swallowing, magic state transitions, test-only production branches, broad rewrites without acceptance benefit, and speculative compatibility layers.

## REQUIRED ARTIFACTS
Changed-file list, implementation-step mapping, focused review notes, and evidence references sufficient to reconstruct why each material code change exists.

## VERIFICATION
Inspect the diff against allowed writes, trace changed code to ACs/tests, run required checks, and manually inspect error/state paths that unit tests may not characterize.

## QUALITY FINDING CLASSIFICATION
Use MAINTAINABILITY, DESIGN, TEST_GAP, or OTHER. A code-quality concern is normally NEEDS_ATTENTION, not a stop.

## TRUE HARD-STOP CONDITIONS
Stop only for authority violations, protected-invariant failure, unsafe engineering behavior, write collisions, or another existing hard-stop category with durable basis.

## OWNER REPORT
Summarize observable behavior changed, important implementation tradeoffs, known limitations, and whether any finding materially affects release confidence.

## SUCCESSOR HANDOVER
Name remaining cleanup, fragile areas, assumptions, and the next exact code/test action. Never transfer "continue refactor" without bounded targets and acceptance.
