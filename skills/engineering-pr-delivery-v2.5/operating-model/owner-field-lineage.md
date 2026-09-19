# Owner field-lineage contract

The Owner communication system is source-derived, so release integrity depends on more than individual files existing.

`owner-field-lineage.yaml` is a **release/consistency contract**, not engineering authority. It records which implementation surfaces must preserve each Owner-critical datum.

Each critical field family declares:

```text
human need
→ authority/source contract
→ declarative schema
→ procedural validator
→ report projection
→ communication projection
→ Owner renderer
→ regression witness
```

`validate_owner_field_lineage.py` fails when a required surface disappears or one of the declared load-bearing field tokens is removed.

This catches defects such as:

- a template documents `files_changed` but the checkpoint schema/validator stops enforcing it;
- ISSUE_GRAPH identity exists but report projection no longer carries current issues;
- delivery readiness is projected but the Owner renderer drops merge authorization;
- `unmerged_prs` remains in source state but stops appearing in Owner summaries;
- an external/local execution requirement exists but loses its success/unblock semantics;
- a communication field remains implemented with no regression witness.

The manifest intentionally does not duplicate current engineering values. It contains only lineage metadata and expected implementation surfaces.

When adding a new Owner-critical datum, update the manifest in the same change. When intentionally removing or replacing one, update the whole lineage rather than weakening a single downstream assertion.
