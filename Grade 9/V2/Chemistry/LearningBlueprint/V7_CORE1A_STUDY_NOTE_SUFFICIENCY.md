# Chemistry LearningBlueprint v7 — Core1A study-note sufficiency

This gate exists because a structurally valid product can still be a poor study note if it contains only object labels, generic prose, page roles, or architecture vocabulary.

## Core1A study-note sufficiency

Core1A may compile only from a **content-bearing study-note authority**. Declaring `RULE`, `EQUATION`, `WORKED_EXAMPLE`, `PRACTICE`, or similar payload types is not evidence that the learner content exists.

Every learning atom must close all of these jobs before pagination:

```text
MEANING
RULE_OR_DECISION
REPRESENTATION_OR_EQUATION
REASONING_CHAIN
BOUNDARY_OR_MISCONCEPTION
WORKED_OR_MODELED_EXAMPLE
PRACTICE
ANSWER_CLOSURE
```

Every learner-facing technical object must contain an actual learner payload and must resolve to both:

```text
source_ref
ccbom_asset_id
```

An unresolved source or CCBOM reference blocks compilation.

For a HARD Core1A bucket, the authority must additionally contain multiple representation types, multiple misconception repairs, at least two reconstructable TTU references, guided and independent practice, and explicit verification objects.

## Learner-surface firewall

Internal architecture vocabulary is machine metadata, not Chemistry teaching. Terms such as `CDAU`, `SDU`, `LAU`, `PAL`, `CCBOM`, `TTU`, `falsifier`, `compiler`, `authority_ref`, `realization_ref`, `support_band`, `schema_version`, and `product_mode` must not appear as learner study content.

Chemistry notation must remain learner-safe: `e⁻`, `Zn²⁺`, `Cu²⁺`, and other governed notation must not degrade to ASCII approximations.

## Pagination doctrine

```text
CONTENT AUTHORITY
→ CONTENT CLOSURE
→ PRACTICE / ANSWER CLOSURE
→ RECONSTRUCTABLE TECHNICAL STRUCTURE
→ PAGINATION
```

Page count is an output. It must never author the content.

The Redox golden `core1a-study-note-redox-authority.json` is the executable exemplar for this gate. It is bound to the expanded Redox CCBOM and validates the content-bearing chain:

```text
species identity
→ oxidation-state change
→ electron consequence
→ agent role
```
