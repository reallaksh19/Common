# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the **canonical orchestration root for Physics Blueprint work**. Role-specific sibling directories such as `CoreAuthoring/`, `Core2Transfer/`, `Core1A/` and `Core2A/` are subordinate execution kits; they do not define a second architecture. The mapping is frozen in `policy/role-bindings.v1.json`.

## Current executable topology

```text
ORIGINAL GROUND TRUTH
        ↓
      CORE0
        ↓
CORE1 ↔ independent second pass ↔ CORE2
        ↓
       JOIN
        ↓
learner state × purpose control state
        ↓
      CORE1A
1A0 … 1A11 cognition/assimilation gates
        ↓
   1A12 manuscript
        ↓
T-* taught-state receipts
        ↓
      CORE2A
```

Execution order is not authority order.

## Implemented Blueprint slices

- evidence normalization + adaptive `CORE1_FIRST | CORE2_FIRST | BLOCK` routing;
- fresh-instance independent second-pass protocol;
- Core1 × Core2 Join with exact Core2-demand coverage and critical-conflict blocking;
- learner-prior resolver for `20 / 50 / 80` with real learner evidence allowed to override only when provenance exists;
- orthogonal purpose contracts: `FIRST_STUDY / PRACTICE / REVISION / COMPETITIVE_EXAM`;
- explicit guard that a teaching/publication receipt cannot be used as learner-state evidence;
- Core1A stage machine requiring ordered completion of `1A0…1A11` and zero unresolved required inferential jumps before releasing `1A12_MANUSCRIPT`;
- active, taught-state-gated Core2A execution kit.

## Join Gate

Every Core2 demand claim is reconciled exactly once. `CONFIRMED`/`REFINED` claims require Core1 grounding and assimilation obligations. Required unresolved claims block Core1A; non-blocking unresolved extensions remain visible as holds.

## Learner state and purpose

The learner percentage is only a prior. It resolves into capability-level `SECURE / PARTIAL / FRAGILE / UNKNOWN` states. Actual learner-response, diagnostic or teacher-observation evidence may override the heuristic state; Core1A teaching receipts may not.

Purpose is separate from learner readiness. `COMPETITIVE_EXAM` may alter recognition/transfer emphasis but cannot bypass prerequisites or introduce untaught Physics.

## Core1A compiler gate

The pre-manuscript sequence is fixed:

```text
1A0 learner-state gap
1A1 learning atoms
1A2 inferential jumps
1A3 cognitive transformation
1A4 representation requirements
1A5 representation candidates
1A6 representation decisions
1A7 picture→word→symbol→equation bridge
1A8 misconception contrast
1A9 worked→faded→independent plan
1A10 Core2 transfer bridge
1A11 unresolved-jump audit
1A12 manuscript
```

A stage may not be skipped or reordered. A blocked stage stops later stages. `1A12_MANUSCRIPT` is released only when all twelve pre-manuscript stages pass and `unresolved_required_jump_count = 0`.

## Core2A authority boundary

```text
Core1 semantic boundary
∩ Core1A T-* TEACHING_COMPLETE receipts
∩ Core2 transfer envelope
∩ learner-product purpose
∩ owner policy
```

Teaching completion never implies learner mastery.

## Running Blueprint proofs

```bash
python 'Grade 9/V2/Physics/Blueprint/contracts/validate_contracts.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_routing.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_independence.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_join.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_control_state.py'
python 'Grade 9/V2/Physics/Blueprint/tests/test_blueprint_core1a_stage_machine.py'
```

These goldens prove process and authority behavior. They do not replace Physics subject review or authorize unsupported problem-family generation.
