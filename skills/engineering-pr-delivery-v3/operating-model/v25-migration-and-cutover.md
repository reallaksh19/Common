# V2.5 migration and V3 cutover

## Purpose

Migration preserves V2.5 engineering history while moving **present authority** to the smaller V3 model.

The migration invariant is:

> Preserve legacy evidence byte-for-byte; create new V3 present authority explicitly; never manufacture a V3 history for work that happened under V2.5.

## Phase A — inventory

`v25_migration.py report`:
- validates the source V2.5 REPO_STATE with the live Common V2.5 validator;
- inventories every file under `agents/relay/**`;
- records per-file SHA-256 digests and schema versions where readable;
- computes one stable legacy-tree digest;
- records current V2.5 lifecycle/frontier/checkpoint/delivery pointers.

The report is `DERIVED_MIGRATION_REPORT`. It is evidence about the source; it is not new execution authority.

## Phase B — non-destructive bootstrap

Bootstrap is allowed only when V2.5 REPO_STATE validation passes.

It creates:
- `relay/ROADMAP/ROADMAP.yaml`;
- `relay/STATE.yaml` in `INITIALIZING`;
- `relay/CONTROLS/controls.yaml` with `CTRL-MIGRATION-RECONCILE` OPEN;
- `relay/GENERATED/CURRENT_SNAPSHOT.yaml`;
- one current `MIGRATION_BOOTSTRAPPED` event;
- `relay/MIGRATION/V25_REPORT.yaml`;
- `relay/PROTOCOL_SELECTION.yaml` selecting `V2_5 / PREPARED`.

It creates no native V3 EP, lease, checkpoint or historical acceptance record.

Owner outcome/current goal must be supplied explicitly. They are not inferred from legacy prose.

## Phase C — native reconciliation

While the selector is `V2_5 / PREPARED`:
- V2.5 remains the live/default compatibility protocol;
- V3 may be reconciled and validated in parallel as staged authority;
- the migration control blocks V3 material/delivery transitions;
- legacy evidence remains writable only under the still-live V2.5 protocol.

Cutover is not ready until the repository has a valid native V3 lifecycle in `ACTIVE`, `IDLE`, or `TERMINAL` and the migration control is RESOLVED with durable reconciliation evidence.

## Phase D — cutover proof

`protocol_cutover.py assess` checks six independent conditions:
1. full V3 conformance PASS;
2. legacy tree digest unchanged from migration inventory;
3. source V2.5 REPO_STATE validation PASS;
4. migration control RESOLVED;
5. native V3 lifecycle ready;
6. protocol selector still in prepared V2.5 state.

All six must PASS.

## Phase E — direct Owner activation

Activation requires:
- passing cutover readiness;
- direct Owner utterance digest;
- Owner session timestamp.

The activation transaction:
- changes protocol selection to `V3 / ACTIVE`;
- changes legacy policy to `READ_ONLY_HISTORY`;
- records the readiness digest and Owner basis;
- appends `PROTOCOL_CUTOVER_ACTIVATED`;
- writes a V2.5 deprecation notice.

It does not modify `agents/relay/**`.

## Post-cutover invariant

After V3 activation, the cutover-time legacy digest becomes immutable history evidence.

If any file under `agents/relay/**` changes, `protocol_cutover.py validate` fails and `protocol_default.py` refuses to select either skill automatically.

This is intentional. Post-cutover legacy mutation is a reconciliation event, not a harmless compatibility write.

## Default selection

`protocol_default.py` is the protocol resolver:

```text
no selector
  → V2.5 LEGACY_DEFAULT

V2_5 + PREPARED
  → V2.5 remains live; V3 staged

V3 + ACTIVE + valid cutover
  → V3 live/default; V2.5 read-only history

invalid selector or changed legacy history
  → INVALID / fail closed
```

Default selection is therefore an explicit repository fact, not a guess based on which skill directory exists.
