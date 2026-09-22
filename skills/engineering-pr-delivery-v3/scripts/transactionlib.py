from __future__ import annotations

import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from v3lib import load_yaml, validate_schema


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
    temp = path.with_name(path.name + ".tmp-relay-v3")
    temp.write_bytes(data)
    os.replace(temp, path)


def _atomic_write_yaml(path: Path, value: Any) -> None:
    payload = yaml.safe_dump(value, sort_keys=False).encode("utf-8")
    _atomic_write_bytes(path, payload)


def _manifest_path(root: Path, tx_id: str) -> Path:
    return root / "relay/TRANSACTIONS" / tx_id / "manifest.yaml"


def load_manifest(path: Path) -> dict[str, Any]:
    value = load_yaml(path)
    errors = validate_schema("transaction", value, f"TRANSACTION {path}")
    if errors:
        raise TransactionError("; ".join(errors))
    return value


def incomplete_transactions(root: Path) -> list[tuple[Path, dict[str, Any] | None, str | None]]:
    base = root / "relay/TRANSACTIONS"
    if not base.exists():
        return []
    out = []
    for path in sorted(base.glob("TX-*/manifest.yaml")):
        try:
            manifest = load_manifest(path)
        except Exception as exc:
            out.append((path, None, str(exc)))
            continue
        if manifest.get("status") in {"PREPARED", "APPLYING", "RECOVERY_REQUIRED"}:
            out.append((path, manifest, None))
    return out


def _prepare(
    root: Path,
    *,
    tx_id: str,
    command: str,
    actor: str,
    replacements: dict[str, bytes],
) -> tuple[Path, dict[str, Any]]:
    if not tx_id.startswith("TX-"):
        raise TransactionError("transaction id must use TX-* namespace")
    tx_dir = root / "relay/TRANSACTIONS" / tx_id
    manifest_path = tx_dir / "manifest.yaml"
    if manifest_path.exists():
        raise TransactionError(f"transaction already exists: {tx_id}")
    if incomplete_transactions(root):
        raise TransactionError("another incomplete V3 transaction exists; recover it before starting a new command")

    operations = []
    for index, (relative, after_bytes) in enumerate(sorted(replacements.items())):
        target = root / relative
        staged_rel = f"relay/TRANSACTIONS/{tx_id}/staged/{index:03d}.after"
        backup_rel = f"relay/TRANSACTIONS/{tx_id}/backups/{index:03d}.before" if target.exists() else None
        staged = root / staged_rel
        staged.parent.mkdir(parents=True, exist_ok=True)
        staged.write_bytes(after_bytes)
        if backup_rel:
            backup = root / backup_rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(target, backup)
        operations.append({
            "path": relative,
            "before_exists": target.exists(),
            "before_digest": _digest_path(target),
            "after_digest": _digest_bytes(after_bytes),
            "staged_path": staged_rel,
            "backup_path": backup_rel,
        })

    now = _now()
    manifest = {
        "schema_version": "relay-v3-transaction",
        "id": tx_id,
        "command": command,
        "actor": actor,
        "status": "PREPARED",
        "created_at": now,
        "updated_at": now,
        "operations": operations,
        "applied": [],
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
            target = root / operation["path"]
            current = _digest_path(target)
            if current != operation["before_digest"]:
                manifest["status"] = "RECOVERY_REQUIRED"
                manifest["updated_at"] = _now()
                _atomic_write_yaml(manifest_path, manifest)
                raise TransactionError(
                    f"precondition changed for {operation['path']}: expected {operation['before_digest']}, got {current}"
                )
            staged = root / operation["staged_path"]
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
    return manifest


def recover(root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    if manifest.get("status") not in {"PREPARED", "APPLYING", "RECOVERY_REQUIRED"}:
        return manifest

    states = []
    for operation in manifest["operations"]:
        digest = _digest_path(root / operation["path"])
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
        return manifest

    # Any mixed/unknown state rolls back to the captured before-images.
    basis = [f"{operation['path']}={state}" for operation, state in zip(manifest["operations"], states)]
    for operation in reversed(manifest["operations"]):
        target = root / operation["path"]
        if operation["before_exists"]:
            backup = root / str(operation["backup_path"])
            if not backup.exists():
                raise TransactionError(f"cannot rollback {operation['path']}: backup is missing")
            _atomic_write_bytes(target, backup.read_bytes())
        elif target.exists():
            target.unlink()

    manifest["status"] = "ROLLED_BACK"
    manifest["recovery"] = {
        "strategy": "ROLLBACK",
        "basis": basis,
    }
    manifest["updated_at"] = _now()
    _atomic_write_yaml(manifest_path, manifest)
    return manifest


def recover_all(root: Path) -> list[dict[str, Any]]:
    results = []
    for path, manifest, error in incomplete_transactions(root):
        if error:
            raise TransactionError(f"cannot parse transaction manifest {path}: {error}")
        results.append(recover(root, path))
    return results


def yaml_bytes(value: Any) -> bytes:
    return yaml.safe_dump(value, sort_keys=False).encode("utf-8")


def jsonl_bytes(events: list[dict[str, Any]]) -> bytes:
    return ("".join(json.dumps(item, sort_keys=True) + "\n" for item in events)).encode("utf-8")
