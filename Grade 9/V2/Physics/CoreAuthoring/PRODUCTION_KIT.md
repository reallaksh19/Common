# Physics Core1 production kit

Executable authoring guardrail for P-G/Core1. It is downstream of canonical Physics, P-F treatment and promoted PCK; it does not choose treatment or redefine truth.

Run:

```bash
python production_kit/run_golden_fixtures.py
python tests/test_physics_core1_production_kit.py
```

Kit surfaces:
- `task_router.py` selects a scaffold profile from treatment + prior knowledge.
- source contract locks capability, problem family, model conditions, allowed relations and forbids external Core2 candidate leakage.
- answer contract locks the authored Core1 answer, reasoning and physical verification route.
- builder produces a treatment-shaped learning representation.
- validator rejects treatment drift, missing modules, weak visual staging, practice-ladder drift and Core2 leakage.
- three golden fixtures cover `FULL_LEARNING`, `READY_VERIFY_ONLY` and `PROBE_FIRST`.
