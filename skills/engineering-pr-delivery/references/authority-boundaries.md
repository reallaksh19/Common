# Authority Boundaries

An authority boundary defines which state or component is allowed to determine an engineering/product fact.

Examples include:

- engineering calculation authority;
- geometry/topology authority;
- unit authority;
- material/property authority;
- XML/file writer authority;
- runtime publication authority;
- renderer/canvas authority;
- CAD/SVG authority;
- registry authority;
- support/classification authority;
- persistence authority;
- product-export authority.

## Before changing an authority boundary

1. Identify the current authority from production behavior/source.
2. Determine whether the approved task requires changing it.
3. Preserve it if the task does not require a change.
4. If changing it, create a `DEC-*` item.
5. Record old authority, new authority, rationale, affected consumers, migration/compatibility behavior, and focused validation.

## Invariants

For each critical invariant record:

```text
What must remain true
Where it is enforced
How it was validated
Whether this PR changes it
```

Example invariants:

```text
Preview state must never become solver authority.
Unrelated rendering must not discard uncommitted engineering input.
Model-changing mutations must invalidate incompatible execution state.
```

Future agents should not need to reconstruct important engineering intent from code archaeology alone.
