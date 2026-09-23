# V3.1 material basis and semantic drift — recorder-first

V3.1 distinguishes material state from coordination state so reconstruction can identify what actually changed.

```text
material_basis.head
coordination_basis.head
```

## Sensitivity set

The derived sensitivity set remains:

- EP write scope;
- EP read scope;
- EP protected scope;
- `basis.semantic_dependencies[].path`;
- path-shaped acceptance test/oracle requirements.

Incomplete semantic-dependency declarations reduce diagnostic quality, so agents should still declare the files/pins that govern important dependencies.

## Material head

The material head is the newest commit after `EP.basis.material_base` touching the sensitivity set.

## Drift

Against a supplied current base ref:

- `DISJOINT` — base moved outside the sensitivity set;
- `RELEVANT` — base changed a sensitive path;
- `UNKNOWN` — the comparison cannot be established.

All three are **observations**.

`RELEVANT` and `UNKNOWN` no longer deny MATERIAL_WRITE or CHECKPOINT. They are recorded so the engineering agent and successor know what must be revalidated.

## CLI

```bash
python skills/engineering-pr-delivery-v3.1/scripts/material_basis.py <repo-root> --base-ref origin/main
```

`relay_can.py` includes the same drift classification in its advisory basis.
