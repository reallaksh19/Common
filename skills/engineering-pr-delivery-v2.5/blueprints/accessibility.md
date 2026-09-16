# Accessibility blueprint

## WHEN TO APPLY
Apply to user-visible UI, interaction, content structure, focus/navigation, color/contrast, dynamic updates, or assistive-technology semantics. Not applicable to internal-only changes with no presentation effect.

## REQUIRED INPUTS
Affected journey/components, semantic structure, supported input methods, design/content intent, accessibility standards/project policy, error/state behavior, and responsive targets.

## PROCEDURE
1. Inspect semantic roles/names/relationships and heading/landmark structure.
2. Traverse the changed path with keyboard only; verify focus order, visibility, trapping, return, and shortcuts where relevant.
3. Check labels/instructions/errors and dynamic status announcements.
4. Check contrast/non-color cues, zoom/reflow, target size, and motion behavior as applicable.
5. Use automated checks as coverage aid, then manually verify interaction semantics.

## BEST-PRACTICE CHECKLIST
- Native semantics before custom ARIA.
- Persistent visible focus.
- Errors associated with fields/actions and recoverable.
- No meaning conveyed by color alone.
- Dynamic changes perceivable without stealing focus unexpectedly.

## ANTI-PATTERNS
ARIA as a patch for wrong HTML, keyboard traps, placeholder-only labels, inaccessible custom controls, suppressing focus outlines, and claiming accessibility from automated scans alone.

## REQUIRED ARTIFACTS
Affected-path accessibility notes, manual keyboard/focus evidence, automated results when available, and QRV findings for unresolved issues.

## VERIFICATION
Manually exercise representative interactions and confirm semantic output with available accessibility tooling/inspection. Record NOT_RUN honestly if a required tool is unavailable.

## QUALITY FINDING CLASSIFICATION
Use ACCESSIBILITY, optionally UX when recovery/comprehension is the main impact. Severity reflects practical user exclusion or task impact.

## TRUE HARD-STOP CONDITIONS
Accessibility findings do not automatically stop engineering execution. A stop requires mapping to an existing protected invariant, authority requirement, or unsafe outcome established by project policy/acceptance.

## OWNER REPORT
Describe affected users/tasks, what remains usable, material exclusions, and any product/standard decision needing Owner input.

## SUCCESSOR HANDOVER
Carry exact component/path, interaction mode, unresolved finding, evidence gap, and next verification/remediation action.
