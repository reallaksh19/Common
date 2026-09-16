# PR402 integration into the canonical Physics Blueprint

## Status

PR #350 is the canonical implementation line. PR #402 is treated as a source branch for useful observability/discovery ideas, not as a second Physics authority stack.

The source branch diverged from the current canonical architecture. Its aggregate 43-gate registry, direct admission/projection stack, SIL READY state, and run-builder authority model are therefore not merged wholesale.

## Canonical authority retained

The active Physics technical path remains:

```text
broad discovery / research inputs
        ↓
canonical per-gate V3 Physics sources
        ↓
Physics V3 validation + technical closure
        ↓
provider-owned external prerequisite closure
        ↓
Shared EngineeringGate
        ↓
Physics Blueprint authority projection
        ↓
Blueprint orchestration
        ↓
independent publication / human-review boundaries
```

A derived observer may inspect this path. It may not authorize it.

## Selectively integrated capability

PR #402's architecture-observability idea is retained through:

- `contracts/physics-architecture-observation.schema.json`
- `tools/architecture_observer/generate_observation_manifest.py`
- `policy/physics-pr402-integration.v1.json`
- `tests/test_pr402_observability_integration.py`

The observation manifest is schema-locked to:

```text
manifest_class = DERIVED_PHYSICS_ARCHITECTURE_OBSERVATION
authority = DERIVED_OBSERVABILITY_ONLY
engineering_authorization = NOT_EVALUATED
publication_authorization = NOT_IMPLIED
```

It is generated from the current canonical V3 registry plus the existing governed discovery catalog. It does not read or depend on the old aggregate V1 gate registry.

## 43-candidate breadth versus canonical V3 authority

The repository currently distinguishes discovery coverage from promoted Physics Engineering authority:

```text
43 discovery candidates
        ↓ reconciliation
24 current canonical V3 gates
+ migration holds for unpromoted candidates
```

The discovery catalog is useful for finding gaps and future engineering work. A discovery candidate is not READY merely because an older branch contains a rich gate/intelligence packet for it.

Promotion requires the normal current V3/EngineeringGate path.

## Work and Energy next boundary

The next bounded Physics stress uses the following discovery candidates:

- `PHY-WORK-ENERGY-POWER` — Grade 9 discovery candidate
- `PHY-ENERGY-CONSERVATION-LAW` — Grade 9 discovery candidate
- `PHY-WEP-VARIABLE-FORCE` — Grade 11 discovery candidate / possible extension context only

All three currently remain `MIGRATION_REQUIRED` with no canonical V3 gate IDs.

For the Grade 9 stress, do not copy a READY flag or advanced Grade 11 content from the source branch. Reconstruct the governed Grade 9 Physics scope and engineer only the V3 data justified by current curriculum/source authority.

The Physics stress must particularly falsify:

- system-boundary ambiguity;
- unconditional `K + U = constant` reasoning;
- dissipation/friction being ignored;
- sign/geometry errors in work;
- learner-state mutation of Physics truth;
- STANDARD to RESEARCH mutation of base claims;
- discovery evidence being promoted into curriculum or readiness authority;
- Blueprint topic-specific branches.

## SIL and nano-research disposition

Subtopic-intelligence and nano-research material from the source branch may be used as discovery/research input only.

It does not bypass:

- LearningEngineering source governance;
- semantic validation;
- curriculum classification;
- contradiction handling;
- V3 Physics Engineering promotion;
- external prerequisite ownership;
- Shared EngineeringGate consumer permissions.

No bulk SIL READY state is imported into runtime authority.

## Run-builder disposition

The source-branch run builder is not adopted as an authority/readiness compiler because it binds the obsolete aggregate registry and embeds policy/topic assumptions into prompt generation.

Existing AgentTasks + repository-owned Blueprint routes remain the generic delegation path. Named Physics stress cases remain Blueprint-owned regression data rather than generic task-kernel semantics.

## CI ownership

PR402 reconciliation is executed from the existing Physics Blueprint discovery regression. No standalone PR402 workflow is introduced.

A valid integration must keep:

```text
discovery breadth != Engineering readiness
observability != authority
research material != curriculum truth
technical readiness != publication authorization
```
