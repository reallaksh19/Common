# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the **canonical orchestration root for Physics Blueprint work**. Role-specific sibling directories (`CoreAuthoring/`, `Core2Transfer/`, `Core1A/`, `Core2A/`) are subordinate execution kits; `policy/role-bindings.v1.json` freezes that mapping.

## Executable topology

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

## Implemented Blueprint slices

- evidence normalization + adaptive `CORE1_FIRST | CORE2_FIRST | BLOCK` routing;
- fresh-instance independent second-pass protocol;
- Core1 × Core2 Join with exact Core2-demand coverage and critical-conflict blocking;
- learner-prior resolver for `20 / 50 / 80` plus provenance-bound learner-evidence overrides;
- orthogonal `FIRST_STUDY / PRACTICE / REVISION / COMPETITIVE_EXAM` purpose contracts;
- guard that teaching/publication receipts cannot masquerade as learner-state evidence;
- Core1A stage machine requiring ordered `1A0…1A11`, exact upstream digests and zero unresolved required jumps before `1A12_MANUSCRIPT`;
- Motion-in-a-Plane as the first topic blueprint pilot;
- active taught-state-gated Core2A execution kit.

## Motion-in-a-Plane topic pilot

`topics/motion-in-a-plane.v1.json` carries the real topic evidence profile: partial/coarse scope authority, strong semantic source, the 59-question Core2 corpus, answer/QC uncertainty and figure evidence. The topic does **not** select its role by name. The current governed metrics are `SA=2, SS=3, QE=4, QR=4, UA=1, CI=1`, and the Governor therefore derives `CORE2_FIRST` through `ROUTE-C2-RICH-QUESTIONS`.

The pilot binds the Blueprint-native Join, learner/purpose control-state and Core1A stage-machine fixtures, while Core2A remains a subordinate runtime kit.

## Core1A compiler gate

`1A0 learner-state gap → 1A1 learning atoms → 1A2 inferential jumps → 1A3 cognitive transformation → 1A4 representation requirements → 1A5 candidates → 1A6 decisions → 1A7 picture/word/symbol/equation bridge → 1A8 misconception contrast → 1A9 worked/faded/independent plan → 1A10 Core2 transfer bridge → 1A11 unresolved-jump audit → 1A12 manuscript`.

A stage cannot be skipped/reordered. A block stops later stages. Manuscript release requires every pre-manuscript stage to PASS and `unresolved_required_jump_count = 0`.

## Core2A authority boundary

```text
Core1 semantic boundary
∩ Core1A T-* TEACHING_COMPLETE receipts
∩ Core2 transfer envelope
∩ learner-product purpose
∩ owner policy
```

Teaching completion never implies learner mastery.

## Current next boundary

The architecture is now proven through the first real topic blueprint pilot. The next Blueprint tranche is the **publication compiler boundary**: consume governed Core1/Core1A/Core2/Core2A representations into Publication IR, run a lossless semantic audit, then render—without allowing the renderer to become a reasoning authority.
