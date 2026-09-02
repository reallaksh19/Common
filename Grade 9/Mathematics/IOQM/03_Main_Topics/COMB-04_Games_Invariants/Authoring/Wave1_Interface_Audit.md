# COMB-04 Wave-1 Interface Audit

Status: `PASS_STATIC_INTERFACE_COMPLETENESS`

Scope: structural and authority audit of the seven Wave-1 research interfaces required by issue #89 and the frozen Microstream Interface Schema v1.

## Interface inventory

| Stream | File | A-P present | Lead status | Historical anchor verification |
|---|---|---:|---|---|
| W1-A | `IOQM-G9-COMB-04__W1-A__parity-invariants__interface.md` | PASS | READY_FOR_LEAD | Q25=36, 2023-Q28=67, Q22=66 inherited from independent corpus oracle |
| W1-B | `IOQM-G9-COMB-04__W1-B__residue-colour-invariants__interface.md` | PASS | READY_FOR_LEAD | 2023-Q28=67, Q25=36 |
| W1-C | `IOQM-G9-COMB-04__W1-C__monovariants__interface.md` | PASS | READY_FOR_LEAD | no direct historical anchor promoted; generic lemmas proved explicitly |
| W1-D | `IOQM-G9-COMB-04__W1-D__winning-losing-states__interface.md` | PASS | READY_FOR_LEAD | Q22=66 |
| W1-E | `IOQM-G9-COMB-04__W1-E__reverse-strategic-reasoning__interface.md` | PASS | READY_FOR_LEAD | Q22=66 |
| W1-F | `IOQM-G9-COMB-04__W1-F__construction-obstruction__interface.md` | PASS | READY_FOR_LEAD | Q25=36, 2023-Q28=67 |
| W1-G | `IOQM-G9-COMB-04__W1-G__source-pyq-audit__interface.md` | PASS | READY_FOR_LEAD | 66 / 36 / 67 and source identities pinned |

## Mandatory schema checks

Every interface contains:

- required YAML-like header with main topic, microstream, role, status, canonical owner, prerequisite interfaces and source cutoff;
- A scope boundary;
- B learner-state model;
- C governing invariant/structure and proof/reconstruction;
- D representation inventory;
- E at least three decision boundaries;
- F misconception/diagnosis catalogue with falsifiers/contrasts;
- G first-move cues;
- H H3 -> H0 fading plan;
- I validated source anchors or explicit no-anchor declaration;
- J source-independent mathematical trace;
- K at least five contrast-pair candidates;
- L T2-T4 transfer candidates;
- M candidate mastery-item forms;
- N dependency declarations;
- O lead integration notes;
- P QA status.

## Authority / overlap checks

- NT-01 parity/divisibility machinery is retrieved, not retaught: PASS.
- NT-02 residue/congruence legality is retrieved, not retaught: PASS.
- COMB-03 deterministic state/reverse-search ownership remains explicit: PASS.
- COMB-04 adversarial W/L and game-invariant ownership remains explicit: PASS.
- No child issues created: PASS.
- No integrated learner chapter created in Wave 1: PASS.

## Proof-safety checks

- `reachability != forceability`: explicit in W1-D/E/F.
- W/L two-direction contract: explicit in W1-D/E.
- invariant compatibility is necessary, not automatically sufficient: explicit in W1-A/B/F.
- monovariant termination does not identify winner: explicit in W1-C.
- historical figure custody for 2023-Q28: explicit in W1-B/F/G.
- no official weightage/frequency claim manufactured: explicit in W1-C/G.

## Static evidence truth

The historical numerical values promoted in Wave 1 are inherited from the frozen independent verification authority:

- `IOQM-2025-Q22 = 66`;
- `IOQM-2025-Q25 = 36`;
- `IOQM-2023-Q28 = 67`.

This Wave-1 audit does not claim new classroom or publication evidence.

```text
INTERFACE_COUNT: 7/7
A_P_COMPLETENESS: PASS
OWNERSHIP_CONFLICTS: NONE
SOURCE_ID_CONFLICTS: NONE
HISTORICAL_ANSWER_ORACLE: PASS_STATIC_INHERITED
CLASSROOM_TIMING_READABILITY: NOT_RUN
RETENTION: NOT_RUN
PSYCHOMETRICS: NOT_RUN
QUALIFICATION_PROBABILITY: NOT_RUN
PERCENTILE_PASS_MARK_CALIBRATION: NOT_RUN
PUBLICATION_APPROVAL: NOT_RUN
WAVE1_GATE: PASS_STATIC_READY_FOR_INTEGRATION
```

Wave 2 may now synthesize one integrated `02_Assimilation_Book.md`; the seven interfaces remain evidence inputs, not seven learner chapters.