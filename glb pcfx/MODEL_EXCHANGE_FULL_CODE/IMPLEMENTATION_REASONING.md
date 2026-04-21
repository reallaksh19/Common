# Implementation Reasoning

## Why a new tab
The new **Model Exchange** tab is the safest place to introduce controlled interoperability without polluting existing viewer/editor tabs with multiple format-specific partial conversions.

## Why not make PCF or GLB the center
- **PCF** is strong but not expressive enough to be the universal internal truth
- **GLB** is a scene/export format, not a trustworthy engineering canonical layer

## Why three layers
### Source Record
Preserves dialect-specific and raw truth.

### Canonical Core
Provides stable engineering semantics for validation, preview, editing, and export.

### View Model
Allows scene/overlay/theme/selection logic to evolve without corrupting engineering truth.

## Why supports are first-class
Supports are neither “just geometry” nor “just annotations”. They need host references, classification, direction provenance, and exportability state.

## Why message circle / message square stay annotations
These are overlay-level objects with anchor rules and fidelity rules. They should not be flattened into core geometry.

## Why fidelity classes are mandatory
Without explicit fidelity/loss classes, the system will over-promise conversion quality and become untrustworthy.
