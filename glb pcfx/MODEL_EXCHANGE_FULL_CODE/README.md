# Model Exchange — Controlled Multi-Format Interoperability

This package provides a concrete starter implementation for a new **Model Exchange** tab.

## What this package is
- A code-first architecture scaffold
- A proposed folder structure
- Canonical schemas
- Import adapters
- Validation/loss-contract helpers
- Export adapters
- View builders
- State store/actions/selectors
- Reasoning docs in the same package

## What this package is not
- Not a claim of a finished production feature
- Not a promise of lossless XML/PCF/PCFX/GLB roundtrip for every path
- Not fully wired into a specific host repo/router/build system

## Core design
The package is based on three layers:
1. **Source Record**
2. **Canonical Core**
3. **View Model**

And explicit fidelity classes:
- LOSSLESS
- NORMALIZED_LOSSLESS
- RECONSTRUCTED
- METADATA_ONLY
- VIEW_ONLY
- NOT_EXPORTABLE

## Recommended first integration points
- Register `viewer/tabs/model-exchange-tab.js` in your tab router
- Mount `viewer/tabs/model-exchange-tab.css`
- Wire file-open events into `model-exchange-actions.js`
- Feed source file text/json/binary into the corresponding import adapter
