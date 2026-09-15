# Single-subtopic all-core mathematics trial

This fixture exercises one Grade 9 Mathematics subtopic through the full semantic/product topology:

`Core1 -> Core1A -> Core1B` and `Core2 -> Core2A -> Core2B`.

## Subtopic

**Point on an Axis Equidistant from Two Fixed Points**  
Canonical id: `MATH-EQUIDISTANT-POINT-ON-AXIS`

The Core1 series is deliberately marked **MEDIUM**. The badge is based on the mathematics/representation burden, not learner knowledge. The teaching path needs an axis constraint, two coordinate-distance models, an equality invariant, binomial expansion, cancellation, shortcut-vs-general-method contrast, and a locus interpretation.

## What this trial checks

- Core1 establishes the legal mathematics.
- Core1A turns that mathematics into a subtopic-wise assimilation plan with MEDIUM depth rules: visual, step-by-step, diagram-led, web-researched pedagogy, and sub-subtopic decomposition.
- Core1B consolidates only mathematics already authorised by Core1/Core1A and adds no new mathematics.
- Core2 decomposes the assessment family independently into recognition cue, hidden state, first non-obvious move, representation switch, reasoning chain, wrong chain and check.
- Core2A requires learner knowledge percentage **or** an explicit owner waiver before calibrated generation.
- Core2B requires a Core2A-legal pool plus an upstream transfer ceiling and remains a fixed static product.

## Two governed paths are preserved

### 1. Missing-calibration falsifier

`trial.json` intentionally has no learner knowledge percentage and no owner waiver. It must stop at:

`Core2A = BLOCKED_MISSING_KNOWLEDGE_CALIBRATION`

and therefore:

`Core2B = BLOCKED_UPSTREAM_CORE2A_NOT_READY`

This proves the production gate still fails closed and that no default learner percentage is invented.

### 2. Explicit owner-waived completion

After the calibration gate was surfaced, the owner instructed the run to proceed. That instruction is recorded as:

`CHAT-OWNER-APPROVAL-2026-09-14T11:40:41Z`

The continuation binds the same reduced-support M4 PRACTICE controls that had already been disclosed and exercised in the prior test-only path; the values are therefore not inferred from learner performance or silently defaulted.

The owner-waived path is stored in:

- `owner-waived-generation-spec.json`
- `owner-waived-run.json`

Bound controls:

- Core2A support profile: `REDUCED_SUPPORT`
- Core2A maximum demand: `M4_HIDDEN_STRUCTURE`
- Core2B maximum demand: `M4_HIDDEN_STRUCTURE`

This is an **owner control**, not learner evidence and not a mastery claim.

The owner-waived run reaches:

`Core1 AUTHORITY_READY`

`Core1A ASSIMILATION_COMPILED`

`Core1B STATIC_CONSOLIDATION_COMPILED`

`Core2 ASSESSMENT_INTELLIGENCE_READY`

`Core2A LEGAL_POOL_COMPILED`

`Core2B STATIC_TRANSFER_COMPILED`

Core2A contains M0, M2, M3 and M4 legal items only; Core2B selects only from that legal pool and cannot exceed M4.

## Important answer correction caught by this trial

For the hidden-structure equation

`(x+3)^2 + 16 = (x-5)^2 + 4`

the correct solution is:

`x = 1/4`, hence `P = (1/4,0)`.

The all-core trial independently verifies this value numerically. Any downstream golden carrying `P=(1,0)` for this exact equation should be corrected rather than copied forward.

## Governing distinction

`MATHEMATICAL DIFFICULTY -> Core1A/Core1B depth`

`LEARNER KNOWLEDGE % or OWNER WAIVER -> Core2A/Core2B calibration`

These inputs must never be silently substituted for one another.

See `research-brief.md` for the MEDIUM-bucket representation research and the JSON fixtures for both the fail-closed and owner-waived paths.
