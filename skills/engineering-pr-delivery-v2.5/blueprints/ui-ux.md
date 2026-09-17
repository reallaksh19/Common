# UI/UX blueprint

## WHEN TO APPLY
Apply when users see, enter, navigate, interpret, recover from, or act on changed behavior. Mark not applicable for purely internal changes with no user interaction effect.

## REQUIRED INPUTS
User goal, journey entry/exit, product language, states/data authority, acceptance criteria, accessibility requirements, supported viewports/input methods, and relevant error/empty/loading behavior.

## PROCEDURE
1. Trace the happy path and the user decision at each step.
2. Exercise partial, invalid, empty, loading, retry, and permission/authority states.
3. Verify labels, hierarchy, focus order, keyboard behavior, responsive layout, and recovery actions.
4. Check that every warning/error says what happened, why it matters, what to do, and what remains safely possible.
5. Compare implementation with the intended product journey, not only component screenshots.

## BEST-PRACTICE CHECKLIST
- Plain product language; no relay/gate/blocker jargon leaked to users.
- Visible state and authority when user decisions depend on them.
- Recoverable errors preserve entered work where safe.
- Disabled actions explain why when ambiguity would result.
- Consistent interaction patterns and responsive behavior.

## ANTI-PATTERNS
Blocking the whole workflow for advisory concerns, modal spam, unexplained disabled controls, internal error codes as UX, success states without evidence, and happy-path-only validation.

## REQUIRED ARTIFACTS
Journey notes/screenshots where useful, state matrix, accessibility/performance findings when applicable, and QRV evidence tied to the changed user path.

## VERIFICATION
Exercise representative end-to-end paths and edge states with keyboard and pointer/touch as relevant; confirm state transitions and recovery are observable and consistent.

## QUALITY FINDING CLASSIFICATION
Use UX, ACCESSIBILITY, PERFORMANCE, or DESIGN. Severity reflects user impact, not implementation inconvenience.

## TRUE HARD-STOP CONDITIONS
A UX flaw blocks execution only when it creates an existing hard-stop condition such as unsafe engineering action, authority violation, or protected invariant failure. Ordinary usability debt does not.

## OWNER REPORT
Describe what the user can do now, what remains awkward or risky, and any product decision genuinely requiring Owner judgment.

## SUCCESSOR HANDOVER
Record unresolved journey states, device/input coverage gaps, exact screens/components involved, and the next verification action.
