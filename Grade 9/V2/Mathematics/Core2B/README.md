# Mathematics Core2B — Static Transfer Workbook Compiler

Core2B is a build-time learner-product compiler downstream of Core2A. It publishes a fixed practice/transfer workbook from an already-legal Core2A item pool.

## Governing question

> Given Core2A legality, purpose, and a compile-time transfer ceiling supplied upstream, which fixed set and ordering should be published?

## Owns

- selection from the Core2A-legal pool;
- ordering by structural demand;
- fixed support density already authored into selected items;
- method/family discrimination set composition;
- mixed/competitive composition when permitted by the supplied ceiling;
- static workbook rendering and quality audit.

## Does not own

- Core2A mathematical legality, source identity, answer custody or provenance;
- live learner attempts;
- state transitions or escalation after an answer;
- retrieval scheduling based on post-publication behavior;
- dynamic hints or repair routing.

## Demand ladder

```text
M0_DIRECT
M1_CONTROLLED_VARIATION
M2_REPRESENTATION_TRANSFER
M3_INVERSE_TARGET
M4_HIDDEN_STRUCTURE
M5_METHOD_DISCRIMINATION
M6_FAMILY_DISCRIMINATION
M7_MULTI_STEP_SYNTHESIS
M8_MIXED_COMPETITIVE
```

`max_demand_level` is a compile-time input. Core2B may select only items at or below that ceiling and only items whose IDs are present in `core2a_legal_item_ids`.

## Static invariant

The compiler rejects live/runtime fields such as:

```text
attempts
learner_response
state_transition
next_task
retry
runtime_hint
retrieval_schedule
repair_handoff
```

The compiled output declares `delivery_mode = STATIC`.

## Fail closed

```text
CORE2B_LIVE_RUNTIME_FIELD_FORBIDDEN
CORE2B_CORE2A_AUTHORITY_MISSING
CORE2B_ITEM_NOT_CORE2A_LEGAL
CORE2B_TRANSFER_EXCEEDS_COMPILE_CEILING
CORE2B_UNAPPROVED_CAPABILITY_REF
CORE2B_FAMILY_LABEL_LEAK
CORE2B_EMPTY_SELECTION
CORE2B_INTERNAL_METADATA_LEAK
```
