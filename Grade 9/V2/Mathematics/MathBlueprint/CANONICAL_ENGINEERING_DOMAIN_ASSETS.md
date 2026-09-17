# Mathematics V2 — Canonical Engineering-Derived Domain Assets

This document is normative for the projection of validated Mathematics Engineering Gate authority into the Canonical Domain Registry.

The core invariant is:

> **Engineering source identity is canonical mathematical identity. Teaching scope is membership metadata, not a reason to copy mathematical truth.**

## 1. Problem this contract prevents

A single Engineering source object can be used in many teaching scopes. For example, a prerequisite gate may be a direct target in one scope and a transitive prerequisite in another.

The following storage model is forbidden:

```text
ENGINEERING SOURCE OBJECT
        x teaching scope A -> Canonical Domain asset A
        x teaching scope B -> Canonical Domain asset B
        x teaching scope C -> Canonical Domain asset C
```

That model duplicates one mathematical authority object merely because it is reused pedagogically.

## 2. Canonical identity

Every Engineering-derived Canonical Domain asset is identified by the exact tuple:

```text
(
  engineering_gate_id,
  engineering_source_kind,
  engineering_source_ref
)
```

`subtopic_id`, `join_ref`, capability membership, question membership and `DIRECT` / `PREREQUISITE_CLOSURE` role are not part of canonical mathematical identity.

The same source tuple must produce exactly one `REG-MATH-ENG-*` asset in a Canonical Domain Registry.

Two different source tuples must never be merged merely because their prose, formula or payload appears similar.

## 3. Scope membership

Every local use of a canonical Engineering-derived asset is recorded separately as a scope-membership record containing at least:

```text
membership_id
asset_ref
subtopic_id
join_ref
engineering_gate_id
engineering_gate_role
capability_refs
core2_refs
membership_digest
```

Valid roles are:

```text
DIRECT
PREREQUISITE_CLOSURE
```

Role is local to the membership. A gate may therefore be `DIRECT` in one membership and `PREREQUISITE_CLOSURE` in another without creating a second canonical asset.

## 4. Canonical asset payload

The canonical asset stores the Engineering-derived technical truth exactly once.

Local capability and Core2-question bindings are unioned onto the compatibility asset so existing producer alias resolution remains complete. The authoritative decomposition of those unions by teaching scope remains the scope-membership ledger.

For Canonical Domain schema compatibility, the asset keeps one deterministic primary `subtopic_id` and `join_ref`. These fields are a storage anchor only. They must never be interpreted as exclusive scope ownership of the mathematical object.

For `PROBLEM_FAMILY`, scope-specific required capability bindings are unioned in the canonical payload; exact per-scope capability custody remains in memberships.

## 5. Internal references

When scope copies are folded into one canonical asset, all internal `REG-MATH-ENG-*` dependencies and payload references must be rewritten to canonical source-based asset IDs.

The resulting Canonical Domain graph must still pass:

```text
schema validation
internal reference validation
acyclic dependency validation
authority-class validation
Core binding validation
```

No dangling reference to a removed scope copy is permitted.

## 6. Independent validation

Projection validation must be independent of the construction path.

For every canonical asset, the validator must prove:

```text
one exact Engineering source tuple
one canonical asset identity
asset digest matches registry payload
at least one valid scope membership
membership refs exactly equal actual memberships
canonical capability refs == union of membership capability refs
canonical Core2 refs == union of membership Core2 refs
primary compatibility anchor == deterministic first membership
```

For every membership, the validator must independently re-derive its local role from:

```text
exact capability -> Engineering gate bridge
        +
current Engineering prerequisite graph
```

No title, fuzzy, semantic or remembered mapping is permitted.

## 7. Custody

The v2 Engineering-domain projection receipt separately custodies:

```text
canonical_assets[]
scope_memberships[]
expanded_projection_digest
base_asset_count
projected_asset_count
scope_membership_count
direct_gate_ids
transitive_gate_ids
projection_digest
```

`scope_membership_count` must equal the number of local Engineering source uses produced by the expanded projection.

`projected_asset_count` must equal the number of unique exact Engineering source tuples.

For a corpus with reused prerequisites:

```text
projected_asset_count < scope_membership_count
```

The difference is the number of redundant scope copies removed from the Canonical Domain Registry, not lost teaching coverage.

## 8. Producer and release invariant

Producers consume the canonical registry, not the expanded scope-copy registry.

Their alias binding may resolve a capability to a canonical asset because the canonical asset contains the union of capability bindings across its memberships.

Final release must prove:

```text
registry_asset_count
== base_asset_count + canonical_projected_asset_count

scope_membership_count
== expanded_projected_asset_count

all canonical source tuples unique
all canonical assets covered by release governance
all memberships digest-valid
all local roles independently re-derived
no orphan canonical assets
no orphan memberships
```

Publication authority is unchanged by canonicalization. Canonicalization removes duplicate storage; it does not add, remove or weaken mathematical, pedagogical, source, answer or Engineering authority.

## 9. Current mixed Grade-9 proof

For the current Q1-Q14 / 30-capability mixed Grade-9 golden, the old expanded projection produced:

```text
base Domain assets                 102
scope-expanded Engineering assets 878
registry total                     980
```

Those 878 rows represent only 128 unique Engineering source tuples.

The canonical v2 projection therefore produces:

```text
base Domain assets                   102
canonical Engineering assets         128
scope memberships                     878
redundant registry copies removed     750
canonical registry total              230
```

These numbers are golden-fixture evidence, not hard-coded production logic. Production derives counts from current authority and scope.

The full four-producer release, Engineering custody checks, frozen-source custody, canonical-answer custody and learner-publication regeneration must pass against the 230-asset canonical registry.

## 10. Required falsifiers

CI must fail for at least:

```text
duplicate exact Engineering source identity
canonical asset digest drift
membership digest drift
membership references an unknown asset
membership gate differs from canonical asset gate
membership gate falls outside its local prerequisite closure
DIRECT/prerequisite role drift
canonical capability union drift
canonical Core2 union drift
missing membership for canonical asset
orphan membership
stale Engineering registry digest
stale crosswalk identity
registry asset count drift
release summary projection-count drift
```

A future implementation that restores one canonical asset per teaching bucket is an architectural regression even if final learner output happens to look identical.
