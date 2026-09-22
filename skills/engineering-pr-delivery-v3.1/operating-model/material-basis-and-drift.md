# V3 material basis and semantic drift

V3 separates the current coordination commit from the commit that last changed material-sensitive engineering state.

```text
material_basis.head
coordination_basis.head
```

A coordination-only commit may advance `coordination_basis.head` while `material_basis.head` remains unchanged. Engineering evidence therefore stays tied to material state rather than generic Git HEAD.

## EP sensitivity set

The mechanical sensitivity set is derived from:
- EP write scope;
- EP read scope;
- EP protected scope;
- `basis.semantic_dependencies[].path`;
- path-shaped acceptance test/oracle requirements.

Command/tool dependencies that cannot be represented as a path MUST be declared through `semantic_dependencies`; otherwise drift classification may be unsafely incomplete.

## Material head

Starting from `EP.basis.material_base`, inspect commits through current checkout HEAD. The newest commit touching any sensitivity pattern becomes `material_basis.head`.

If subsequent commits touch only coordination/non-sensitive paths:

```text
A material change
B relay metadata
C provider observation

material head     = A
coordination head = C
```

## Drift

Given the current base ref:

```text
changed_on_base
∩
EP sensitivity
```

classifies as:
- `DISJOINT`: base advanced but no sensitive path changed;
- `RELEVANT`: at least one sensitive path changed;
- `UNKNOWN`: the base cannot be resolved, ancestry is incompatible, or Git evidence cannot be inspected.

`DISJOINT` does not block `MATERIAL_WRITE`. `RELEVANT` and `UNKNOWN` do.

## CLI

```bash
python skills/engineering-pr-delivery-v3.1/scripts/material_basis.py <repo-root> --base-ref origin/main
```

`relay_can.py MATERIAL_WRITE` consumes the same mechanical classifier. The caller supplies the identity of the current base ref, not a subjective drift verdict.
