# Physics Core2 production kit

Executable guardrail for P-I/Core2 transfer production. It sits downstream of the eligible external-transfer corpus, Core1 teaching, capability/problem-family semantics and the protected H1/H2/H3 ladder.

Run:

```bash
python production_kit/run_golden_fixtures.py
python tests/test_physics_core2_production_kit.py
```

Kit surfaces:
- `task_router.py` chooses a guide-demand scaffold for MCQ, numeric or figure-led transfer tasks.
- source contract locks the exact source body, source link, figure semantics, digest, eligibility and provenance claim.
- answer contract locks the canonical answer, full solution and verification route while declaring tokens that hints must never reveal.
- builder produces a transfer representation with preserved source body, Core1 link, First-Step Reference, H1/H2/H3 ladder, staged representation, solution and verification.
- validator rejects source rewriting, figure loss, collapsed hint ladders, answer leakage, missing Core1 links, insufficient representation depth and synthetic-as-production claims.
- three golden fixtures cover MCQ vector components, a numeric timed-event problem and a figure-led inclined-plane intersection.

The production kit does not redefine eligibility, canonical Physics, learner treatment or Core1 scope. Those remain upstream authorities.
