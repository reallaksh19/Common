# Physics Core2B v8 — CCU-governed transfer Problem TTUs

Core2B is generative-dominant transfer and independent modelling. V8 adds CCU custody so fresh transfer cannot be faked by replaying a Core2A exemplar or by losing source/answer lineage.

## Authority path

`exact Core2A legal-pool custody + observed Core1B evidence → CCU lineage/duplication receipts → CDAU purpose → LAU → transfer Problem TTU → Core2B`

## Question custody

Every Core2B challenge must carry:

- stable question ID;
- source class and learner-visible source label;
- legal parent/source lineage;
- original source number where applicable;
- problem family/bucket/capabilities;
- canonical answer/solution/rubric;
- example fingerprint;
- declared Core2A→Core2B relationship.

Generated siblings may not impersonate source questions. A question without a canonical resolution cannot be released.

## Transfer lineage

Permitted relationships:

- `FADING_ANCHOR` — intentional same-item fading; never independent transfer evidence;
- `STRUCTURAL_SIBLING` — changed legal instance; may support transfer evidence;
- `FAR_TRANSFER_SIBLING` — changed representation/target/constraint/synthesis; may support stronger transfer evidence.

When a legal sibling exists, exact Core2A replay is not the default.

CCU blocks adjacent-layer exact numeric reuse unless explicitly `FADING_ANCHOR`, and blocks high structural similarity with equivalent pedagogical usage.

## Learner fit

LAU v2 requires capability-specific knowledge evidence or explicit owner override. Task demand and support are recorded separately. `OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED` must be used when no usable knowledge evidence exists; owner routing may not be presented as validated learner fit.

## Problem TTU

Transfer tasks may require generation, selection, diagnosis, derivation/connection, verification and transfer. Bounded help may rescue the learner, but full-solution exposure is learning support, not independent transfer evidence.

## Release

Production Core2B requires exact Core2A legal-pool custody, fresh legal lineage where transfer is claimed, CCU question/answer/duplication receipts, LAU fit receipt, TTU completeness and observed-evidence requirements.

Normative references:

- `../Blueprint/SELF_HELP_ARCHITECTURE_V8.md`
- `../Blueprint/policy/content-custody-coverage-unit.v1.json`
- `../Blueprint/policy/core-governance-cdau.v2.json`
- `../Blueprint/policy/learner-adaptation-unit.v2.json`
- `../Blueprint/policy/technical-teaching-unit.v3.json`
