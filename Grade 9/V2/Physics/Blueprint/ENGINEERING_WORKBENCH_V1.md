# Physics Engineering Workbench v1 — historical migration note

This document is retained only to preserve the original Workbench-v1 design boundary and regression history.

The canonical Engineering Workbench is now documented in:

`ENGINEERING_WORKBENCH.md`

The canonical technical-engineering authority is now the v3 source-file registry assembled from:

`engineering-gates/**/PHY-*.v3.json`

by:

`engine/build_physics_engineering_gate_registry_v3.py`

and validated by:

`engine/validate_engineering_gates_v3.py`

The aggregate:

`policy/physics-technical-engineering-gates.v2.json`

and `engine/validate_engineering_gates_v2.py` are retained only as migration provenance and regression evidence. New Workbench manifests must use the v3 registry path.

Historical v1 guarantees remain regression-tested: recursive prerequisite closure, Research Dossier + Claim Ledger requirements, source-state independence, CCU technical boundary, closure receipts and Passport consistency.

Do not use this historical note as current architecture authority.
