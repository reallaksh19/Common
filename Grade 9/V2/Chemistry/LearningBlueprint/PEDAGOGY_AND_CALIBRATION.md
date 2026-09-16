# Chemistry V2 — Pedagogy, Calibration & Dual-Track Product Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Chemistry V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Subject**: `CHEMISTRY` only.

---

## 1. Dual-Track Architecture: SDU vs. LAU

```text
                           CANONICAL DOMAIN MODEL
            concepts • equations • derivations • models • representations
            misconceptions • learning atoms • problem families
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
          STUDY-MATERIAL TRACK               QUESTION TRACK
            Core1A / Core1B                  Core2A / Core2B
                 │                                 │
                 ▼                                 ▼
      STUDY DIFFERENTIATION UNIT          LEARNER ADAPTATION UNIT
               SDU                                  LAU
                 │                                 │
     intrinsic EASY/MEDIUM/HARD          knowledge % OR owner override
     NO learner % may alter depth        + task demand + purpose
```

### Invariants:
1. **Core1A/Core1B (SDU)**: Governed strictly by the subtopic difficulty badge. Learner diagnostic percentage MUST NOT alter Core1 depth.
2. **Core2A/Core2B (LAU)**: Conditioned on learner knowledge percentage only when bound to an explicit calibration policy and source reference, or under explicit Owner Waiver.
3. **A vs B Layers**: A-layers provide complete declarative teaching; B-layers provide active reconstructive self-tutoring via incomplete Reconstructable TTUs and verified completion keys.
