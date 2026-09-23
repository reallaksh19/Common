from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
from fnmatch import fnmatch
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from v3lib import load_yaml, repo_path, require_identifier, validate_schema


COMMAND_TARGET_PATTERNS = {
    "ACTIVATE_LEASE": [
        "relay/EVENTS.jsonl",
        "relay/STATE.yaml",
        "relay/GENERATED/CURRENT_SNAPSHOT.yaml",
        "relay/LEASES/LEASE-*.yaml",
    ],
    "RENEW_LEASE": [
        "relay/EVENTS.jsonl",
        "relay/LEASES/LEASE-*.yaml",
        "relay/GENERATED/CURRENT_SNAPSHOT.yaml",
    ],
    "RECORD_RECOVERY_RECONSTRUCTED": [
        "relay/EVENTS.jsonl",
        "relay/LEASES/LEASE-*.yaml",
    ],
    "RECORD_CHANGE_HYPOTHESIS": [
        "relay/EVENTS.jsonl",
        "relay/LEASES/LEASE-*.yaml",
        "relay/CHANGES/CHANGE-*.yaml",
    ],
    "VERIFY_CHANGE_DELTA": [
        "relay/EVENTS.jsonl",
        "relay/LEASES/LEASE-*.yaml",
        "relay/CHANGES/CHANGE-*.yaml",
    ],
    "PROPOSE_CHANGE_DELTA": [
        "relay/EVENTS.jsonl",
        "relay/LEASES/LEASE-*.yaml",
        "relay/CHANGES/CHANGE-*.yaml",
    ],
    "AUTHORIZE_CHANGE_DELTA": [
        "relay/EVENTS.jsonl",
        "relay/CHANGES/CHANGE-*.yaml",
    ],
    "RESOLVE_CONTROL": [
        "relay/EVENTS.jsonl",
        "relay/LEASES/LEASE-*.yaml",
        "relay/CONTROLS/controls.yaml",
        "relay/GENERATED/CURRENT_SNAPSHOT.yaml",
    ],
    "RECONCILE_ROADMAP": [
        "relay/EVENTS.jsonl",
        "relay/LEASES/LEASE-*.yaml",
        "relay/ROADMAP/ROADMAP.yaml",
        "relay/STATE.yaml",
        "relay/GENERATED/CURRENT_SNAPSHOT.yaml",
        "relay/CHANGES/CHANGE-*.yaml",
    ],
    "SYNC_HANDOVER_LEDGER": [
        "relay/EVENTS.jsonl",
        "relay/GENERATED/HANDOVER_PROVIDER_STATUS.yaml",
        "relay/GENERATED/HANDOVER_LEDGER.yaml",
        "relay/GENERATED/HANDOVER_LEDGER.md",
        "relay/GENERATED/PARENT_RELAY_SUMMARY.md",
    ],
    "FREEZE_LEGACY_CUTOVER": [
        "relay/EVENTS.jsonl",
        "relay/PROTOCOL_SELECTION.yaml",
    ],
    "ADMIT_TASK": [
        "relay/EVENTS.jsonl",
        "relay/ROADMAP/ROADMAP.yaml",
        "relay/STATE.yaml",
        "relay/GENERATED/CURRENT_SNAPSHOT.yaml",
        "relay/WORK/EP-*.yaml",
        "relay/LEASES/LEASE-*.yaml",
    ],
}


class TransactionError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _digest_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _digest_path(path: Path) -> str | None:
    if not path.exists():
        return None
    return _digest_bytes(path.read_bytes())


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp-relay-v3.1")
    temp.write_bytes(data)
    os.replace(temp, path)


def _atomic_write_yaml(path: Path, value: Any) -> None:
    _atomic_write_bytes(path, yaml.safe_dump(value, sort_keys=False).encode("utf-8"))


def load_manifest(path: Path) -> dict[str, Any]:
    value = load_yaml(path)
    errors = validate_schema("transaction", value, f"TRANSACTION {path}")
    if errors:
        raise TransactionError("; ".join(errors))
    return value


TERMINAL_STATUSES = {"COMMITTED", "ROLLED_BACK"}


def _transaction_dirs(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted(
        path
        for path in base.iterdir()
        if path.is_dir() and (path.name.startswith("TX-") or path.name.startswith("TX."))
    )


def _compact_terminal_manifest(
    root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    """Retain a digest receipt; discard byte payload no longer needed for recovery."""

    if manifest.get("status") not in TERMINAL_STATUSES:
        return manifest

    compact = copy.deepcopy(manifest)
    for operation in compact.get("operations") or []:
        operation.pop("staged_path", None)
        operation.pop("backup_path", None)
    compact["payload_state"] = "PRUNED"
    _atomic_write_yaml(manifest_path, compact)

    tx_dir = manifest_path.parent
    for name in ("staged", "backups"):
        payload_dir = tx_dir / name
        if payload_dir.exists():
            try:
                shutil.rmtree(payload_dir)
            except OSError:
                # Payload cleanup is an optimisation, not transaction authority.
                # The compact terminal receipt is already durable; a later
                # transaction will opportunistically retry physical pruning.
                pass
    return compact


def prune_terminal_payloads(root: Path) -> list[str]:
    """Clean terminal payload residue left by a crash after commit marking."""

    base = root / "relay/TRANSACTIONS"
    if not base.exists():
        return []

    pruned: list[str] = []
    for tx_dir in _transaction_dirs(base):
        manifest_path = tx_dir / "manifest.yaml"
        if not manifest_path.exists():
            continue
        try:
            manifest = load_manifest(manifest_path)
        except Exception:
            continue
        if manifest.get("status") not in TERMINAL_STATUSES:
            continue
        has_payload = (tx_dir / "staged").exists() or (tx_dir / "backups").exists()
        has_payload_refs = any(
            "staged_path" in operation or "backup_path" in operation
            for operation in manifest.get("operations") or []
        )
        if has_payload or has_payload_refs or manifest.get("payload_state") != "PRUNED":
            _compact_terminal_manifest(root, manifest_path, manifest)
            pruned.append(str(manifest.get("id") or tx_dir.name))
    return pruned


def incomplete_transactions(root: Path) -> list[tuple[Path, dict[str, Any] | None, str | None]]:
    base = root / "relay/TRANSACTIONS"
    if not base.exists():
        return []
    out = []
    for tx_dir in _transaction_dirs(base):
        path = tx_dir / "manifest.yaml"
        if not path.exists():
            out.append((path, None, "MISSING_MANIFEST"))
            continue
        try:
            manifest = load_manifest(path)
        except Exception as exc:
            out.append((path, None, str(exc)))
            continue
        if manifest.get("status") in {"PREPARED", "APPLYING", "RECOVERY_REQUIRED"}:
            out.append((path, manifest, None))
    return out


LEASE_MUTATION_COMMANDS = {
    "ACTIVATE_LEASE",
    "RENEW_LEASE",
    "ADMIT_TASK",
    "RELEASE_LEASE",
    "CLOSE_TASK",
}


def _validate_lease_mutations(
    root: Path,
    command: str,
    actor: str,
    replacements: dict[str, bytes],
) -> None:
    lease_targets = [
        path for path in replacements
        if path.startswith("relay/LEASES/") and path.endswith(".yaml")
    ]
    if not lease_targets or command in LEASE_MUTATION_COMMANDS:
        return

    for relative in lease_targets:
        target = repo_path(root, relative, "lease liveness target")
        if not target.exists():
            raise TransactionError(f"{command} cannot create lease authority: {relative}")
        before = load_yaml(target)
        after = yaml.safe_load(replacements[relative])
        if not isinstance(before, dict) or not isinstance(after, dict):
            raise TransactionError(f"{command} lease liveness mutation must preserve a mapping")
        if str(((before.get("executor") or {}).get("id") or "")) != str(actor):
            raise TransactionError(
                f"{command} cannot renew liveness for a lease owned by another executor"
            )

        before_top = copy.deepcopy(before)
        after_top = copy.deepcopy(after)
        before_custody = before_top.pop("custody", {}) or {}
        after_custody = after_top.pop("custody", {}) or {}
        if before_top != after_top:
            raise TransactionError(
                f"{command} may only mutate lease custody liveness fields"
            )
        if before.get("state") != "ACTIVE" or after.get("state") != "ACTIVE":
            raise TransactionError(f"{command} liveness renewal requires an ACTIVE lease")

        for key in set(before_custody) | set(after_custody):
            if key in {"renewed_at", "activity_basis"}:
                continue
            if before_custody.get(key) != after_custody.get(key):
                raise TransactionError(
                    f"{command} may not mutate lease custody.{key}"
                )


def _target_matches(path: str, pattern: str) -> bool:
    if fnmatch(path, pattern):
        return True
    if "-*" in pattern:
        return fnmatch(path, pattern.replace("-*", ".*"))
    return False


def _validate_command_targets(command: str, replacements: dict[str, bytes]) -> None:
    patterns = COMMAND_TARGET_PATTERNS.get(command)
    if not patterns:
        return
    invalid = [
        path for path in replacements
        if path.startswith("relay/")
        and not any(_target_matches(path, pattern) for pattern in patterns)
    ]
    if invalid:
        raise TransactionError(
            f"{command} cannot mutate target(s): {', '.join(sorted(invalid))}"
        )


def _jsonl_records(data: bytes) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for raw in data.decode("utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise TransactionError(
                f"EVENT_HISTORY_INVALID_JSON: {exc.msg}"
            ) from exc
        if not isinstance(value, dict):
            raise TransactionError("EVENT_HISTORY_INVALID_RECORD: expected JSON object")
        records.append(value)
    return records


def _validate_append_only_history(root: Path, replacements: dict[str, bytes]) -> None:
    relative = "relay/EVENTS.jsonl"
    after = replacements.get(relative)
    if after is None:
        return
    target = root / relative
    before_records = _jsonl_records(target.read_bytes()) if target.exists() else []
    after_records = _jsonl_records(after)
    if (
        len(after_records) < len(before_records)
        or after_records[: len(before_records)] != before_records
    ):
        raise TransactionError(
            "EVENT_HISTORY_NOT_APPEND_ONLY: relay/EVENTS.jsonl replacement must extend the exact current durable event sequence"
        )


def _prepare(
    root: Path,
    *,
    tx_id: str,
    command: str,
    actor: str,
    replacements: dict[str, bytes],
) -> tuple[Path, dict[str, Any]]:
    try:
        require_identifier(tx_id, "TX-", "transaction id")
    except ValueError as exc:
        raise TransactionError(str(exc)) from exc
    prune_terminal_payloads(root)
    if incomplete_transactions(root):
        raise TransactionError("another incomplete V3 transaction exists; recover it before starting a new command")
    _validate_command_targets(command, replacements)
    _validate_lease_mutations(root, command, actor, replacements)
    _validate_append_only_history(root, replacements)
    tx_dir = repo_path(root, f"relay/TRANSACTIONS/{tx_id}", "transaction directory")
    manifest_path = tx_dir / "manifest.yaml"
    try:
        tx_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise TransactionError(f"transaction already exists: {tx_id}") from exc

    operations = []
    for index, (relative, after_bytes) in enumerate(sorted(replacements.items())):
        target = repo_path(root, relative, "transaction target")
        before_exists = target.exists()
        before_digest = _digest_path(target)
        staged_rel = f"relay/TRANSACTIONS/{tx_id}/staged/{index:03d}.after"
        backup_rel = f"relay/TRANSACTIONS/{tx_id}/backups/{index:03d}.before" if before_exists else None
        staged = root / staged_rel
        staged.parent.mkdir(parents=True, exist_ok=True)
        staged.write_bytes(after_bytes)
        if backup_rel:
            backup = root / backup_rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(target, backup)
        operations.append({
            "path": relative,
            "before_exists": before_exists,
            "before_digest": before_digest,
            "after_digest": _digest_bytes(after_bytes),
            "staged_path": staged_rel,
            "backup_path": backup_rel,
        })

    now = _now()
    manifest = {
        "schema_version": "relay-v3.1-transaction",
        "id": tx_id,
        "command": command,
        "actor": actor,
        "status": "PREPARED",
        "created_at": now,
        "updated_at": now,
        "operations": operations,
        "applied": [],
        "payload_state": "RECOVERY_PAYLOAD",
    }
    errors = validate_schema("transaction", manifest, "TRANSACTION")
    if errors:
        raise TransactionError("; ".join(errors))
    _atomic_write_yaml(manifest_path, manifest)
    return manifest_path, manifest


def execute(
    root: Path,
    *,
    tx_id: str,
    command: str,
    actor: str,
    replacements: dict[str, bytes],
    fail_after: int | None = None,
) -> dict[str, Any]:
    manifest_path, manifest = _prepare(
        root,
        tx_id=tx_id,
        command=command,
        actor=actor,
        replacements=replacements,
    )
    manifest["status"] = "APPLYING"
    manifest["updated_at"] = _now()
    _atomic_write_yaml(manifest_path, manifest)

    try:
        for index, operation in enumerate(manifest["operations"], 1):
            target = repo_path(root, operation["path"], "transaction target")
            current = _digest_path(target)
            if current != operation["before_digest"]:
                manifest["status"] = "RECOVERY_REQUIRED"
                manifest["updated_at"] = _now()
                _atomic_write_yaml(manifest_path, manifest)
                raise TransactionError(
                    f"precondition changed for {operation['path']}: expected {operation['before_digest']}, got {current}"
                )
            staged = repo_path(root, operation["staged_path"], "transaction staged path")
            _atomic_write_bytes(target, staged.read_bytes())
            manifest["applied"].append(operation["path"])
            manifest["updated_at"] = _now()
            _atomic_write_yaml(manifest_path, manifest)
            if fail_after is not None and index >= fail_after:
                raise TransactionError("injected transaction interruption")
    except Exception:
        if manifest.get("status") != "RECOVERY_REQUIRED":
            manifest["status"] = "RECOVERY_REQUIRED"
            manifest["updated_at"] = _now()
            _atomic_write_yaml(manifest_path, manifest)
        raise

    manifest["status"] = "COMMITTED"
    manifest["updated_at"] = _now()
    _atomic_write_yaml(manifest_path, manifest)
    return _compact_terminal_manifest(root, manifest_path, manifest)


def recover(root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    if manifest.get("status") not in {"PREPARED", "APPLYING", "RECOVERY_REQUIRED"}:
        return manifest

    states = []
    for operation in manifest["operations"]:
        digest = _digest_path(repo_path(root, operation["path"], "transaction target"))
        if digest == operation["after_digest"]:
            states.append("AFTER")
        elif digest == operation["before_digest"]:
            states.append("BEFORE")
        else:
            states.append("OTHER")

    if all(state == "AFTER" for state in states):
        manifest["status"] = "COMMITTED"
        manifest["recovery"] = {
            "strategy": "CONFIRM_COMMIT",
            "basis": ["Every target matches the staged after-image digest."],
        }
        manifest["applied"] = [operation["path"] for operation in manifest["operations"]]
        manifest["updated_at"] = _now()
        _atomic_write_yaml(manifest_path, manifest)
        return _compact_terminal_manifest(root, manifest_path, manifest)

    basis = [f"{operation['path']}={state}" for operation, state in zip(manifest["operations"], states)]
    if any(state == "OTHER" for state in states):
        manifest["status"] = "RECOVERY_REQUIRED"
        manifest["recovery"] = {
            "strategy": "ROLLBACK",
            "basis": basis + ["Automatic rollback refused because at least one target matches neither before nor after digest."],
        }
        manifest["updated_at"] = _now()
        _atomic_write_yaml(manifest_path, manifest)
        raise TransactionError(
            "transaction recovery found external/unknown target changes; manual reconciliation is required"
        )

    for operation in reversed(manifest["operations"]):
        target = repo_path(root, operation["path"], "transaction target")
        if operation["before_exists"]:
            backup = repo_path(root, str(operation["backup_path"]), "transaction backup path")
            if not backup.exists():
                raise TransactionError(f"cannot rollback {operation['path']}: backup is missing")
            _atomic_write_bytes(target, backup.read_bytes())
        elif target.exists():
            target.unlink()

    manifest["status"] = "ROLLED_BACK"
    manifest["recovery"] = {"strategy": "ROLLBACK", "basis": basis}
    manifest["updated_at"] = _now()
    _atomic_write_yaml(manifest_path, manifest)
    return _compact_terminal_manifest(root, manifest_path, manifest)


def recover_all(root: Path) -> list[dict[str, Any]]:
    results = []
    for path, manifest, error in incomplete_transactions(root):
        if error == "MISSING_MANIFEST":
            tx_dir = path.parent
            tx_id = tx_dir.name
            shutil.rmtree(tx_dir)
            results.append({
                "id": tx_id,
                "status": "ROLLED_BACK",
                "recovery": {
                    "strategy": "ROLLBACK",
                    "basis": ["Transaction had no manifest; canonical targets had not entered the apply phase."],
                },
            })
            continue
        if error:
            raise TransactionError(f"cannot parse transaction manifest {path}: {error}")
        results.append(recover(root, path))
    return results


def yaml_bytes(value: Any) -> bytes:
    return yaml.safe_dump(value, sort_keys=False).encode("utf-8")


def jsonl_bytes(events: list[dict[str, Any]]) -> bytes:
    return ("".join(json.dumps(item, sort_keys=True) + "\n" for item in events)).encode("utf-8")
