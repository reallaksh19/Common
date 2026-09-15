# EXT-001 — Add equal-velocity, different-initial-position relative motion

**Change request:** “Add equal-velocity, different-initial-position relative motion.”  
**Change version:** `M2D-EXT-001-v1.0.0`  
**Parent baseline:** `M2D-BASELINE-20260915-v1.1.0`  
**Status:** executed as a separate rehearsal extension; baseline learner files and baseline registers are preserved unchanged.  
**Scope:** `REQUESTED_ENRICHMENT`; this extension does not create a CBSE examination requirement.

## Model compatibility and dependency decision

The new subtopic is registered as `B05E` beneath the existing reference-frame / relative-position model. No new physics model is required. It reuses `EQ05` (`v_A/B=v_A/G−v_B/G`) and `EQ06` (`r_A/B(t)=r_A/B(0)+v_A/B t`) from the baseline equation register.

New obligations:

- `EXT-B05E-C01`: if two objects have equal velocity in the same ground frame, their relative velocity is zero.
- `EXT-B05E-C02`: zero relative velocity makes relative position constant; the constant need not be zero.
- `EXT-B05E-C03`: equal velocities do not imply either object is stationary in the ground frame.
- `EXT-B05E-MIS01`: repair “zero relative velocity means same position” by keeping initial relative position explicit.
- `EXT-Q-001`: learner applies the invariant to a nonzero initial separation and explains both relative and ground-frame statements.

Prerequisite graph: `B01 frame/axes/clock → B05 subtraction/signs → B05E constant relative position`. The extension is compatible with the current v3 shared-frame/vector-subtraction authority and does not import trigonometry, acceleration or projectile motion.

## Impact / staleness analysis

The source corpus `SYN-M2D-20260915-V1` and its 159-atom baseline inventory are unchanged. The following baseline consumers become **STALE_FOR_EXTENSION_ONLY** because they do not contain the new B05E obligation: Core1 B05 notes, Core1A B05 teaching, Core1B B05 reconstruction, Core2A equal-velocity anchor `2A-Q10`, Core2B prediction `2B-Q04`, bundle packet B04–B06, G2 completeness evidence, G4 practice-fit evidence, G6 cross-Core transfer evidence and G7 relay packet state. Core2 frozen source questions are not stale because the extension does not alter the frozen source corpus.

The separate extension artifacts below close those new obligations without overwriting the baseline. Baseline acceptance records remain historical evidence; extension-aware checks use the delta/revised registers in this directory.

## Rerun obligations

Rerun: extension locator checks, demand-score check for `EXT-Q-001`, impacted B05/B05E cross-Core structural comparison, packet B04–B06 successor check, and package-level existence/link validation. Independent cold restart remains `NOT_RUN`; same-instance checks are `SELF_REVIEW` only.
