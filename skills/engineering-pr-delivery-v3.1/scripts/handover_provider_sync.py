#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from relay_tx import _assert_event_ids_available, _event
from transactionlib import TransactionError, execute, jsonl_bytes, yaml_bytes
from v3lib import canonical_digest, load_events, load_yaml, validate_schema


START = "<!-- relay-v3.1:start -->"
END = "<!-- relay-v3.1:end -->"
Client = Callable[[str, str, str, dict[str, Any] | None], dict[str, Any]]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _marked(content: str) -> str:
    return f"{START}\n{content.strip()}\n{END}"


def _replace_marked(body: str, content: str) -> str:
    body = body or ""
    replacement = _marked(content)
    start = body.find(START)
    end = body.find(END)
    if start >= 0 and end >= start:
        end += len(END)
        return body[:start].rstrip() + ("\n\n" if body[:start].strip() else "") + replacement + body[end:]
    if not body.strip():
        return replacement
    return body.rstrip() + "\n\n" + replacement + "\n"


def _extract_marked(body: str) -> str | None:
    start = (body or "").find(START)
    end = (body or "").find(END)
    if start < 0 or end < start:
        return None
    return (body or "")[start:end + len(END)]


def _github_json(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "engineering-relay-v3.1",
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise TransactionError(f"GitHub provider request failed: {exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise TransactionError(f"GitHub provider request failed: {exc.reason}") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TransactionError("GitHub provider returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise TransactionError("GitHub provider returned a non-object response")
    return value


def _issue_url(api_base: str, repository: str, number: int) -> str:
    return f"{api_base.rstrip('/')}/repos/{repository}/issues/{number}"


def _sync_issue(
    *,
    repository: str,
    number: int,
    desired_content: str,
    token: str,
    api_base: str,
    client: Client,
) -> dict[str, Any]:
    url = _issue_url(api_base, repository, number)
    before = client("GET", url, token, None)
    before_body = str(before.get("body") or "")
    desired_body = _replace_marked(before_body, desired_content)
    updated = desired_body != before_body
    if updated:
        client("PATCH", url, token, {"body": desired_body})
    after = client("GET", url, token, None)
    after_body = str(after.get("body") or "")
    if _extract_marked(after_body) != _marked(desired_content):
        raise TransactionError(
            f"provider readback mismatch for {repository}#{number}: relay block did not converge"
        )
    html_url = str(after.get("html_url") or f"https://github.com/{repository}/issues/{number}")
    return {
        "repository": repository,
        "issue_number": number,
        "url": html_url,
        "body_digest": canonical_digest(after_body),
        "updated": updated,
    }


def sync_handover_provider(
    root: Path,
    *,
    tx_id: str,
    event_id: str,
    actor: str,
    token: str,
    ledger_path: Path | None = None,
    ledger_markdown_path: Path | None = None,
    parent_summary_path: Path | None = None,
    api_base: str = "https://api.github.com",
    client: Client = _github_json,
    fail_after: int | None = None,
) -> dict[str, Any]:
    if not token.strip():
        raise TransactionError("GitHub provider sync requires a non-empty token")

    ledger_path = ledger_path or (root / "relay/GENERATED/HANDOVER_LEDGER.yaml")
    ledger_markdown_path = ledger_markdown_path or (root / "relay/GENERATED/HANDOVER_LEDGER.md")
    parent_summary_path = parent_summary_path or (root / "relay/GENERATED/PARENT_RELAY_SUMMARY.md")
    for path, label in (
        (ledger_path, "HANDOVER_LEDGER"),
        (ledger_markdown_path, "HANDOVER_LEDGER.md"),
        (parent_summary_path, "PARENT_RELAY_SUMMARY.md"),
    ):
        if not path.exists():
            raise TransactionError(f"{label} is missing: {path}")

    ledger = load_yaml(ledger_path)
    errors = validate_schema("handover-ledger", ledger, "HANDOVER_LEDGER")
    if errors:
        raise TransactionError("; ".join(errors))

    parent = ledger.get("parent_issue") or {}
    handover = ledger.get("handover_issue") or {}
    parent_content = parent_summary_path.read_text(encoding="utf-8")
    handover_content = ledger_markdown_path.read_text(encoding="utf-8")

    parent_readback = _sync_issue(
        repository=str(parent.get("repository")),
        number=int(parent.get("number")),
        desired_content=parent_content,
        token=token,
        api_base=api_base,
        client=client,
    )
    handover_readback = _sync_issue(
        repository=str(handover.get("repository")),
        number=int(handover.get("number")),
        desired_content=handover_content,
        token=token,
        api_base=api_base,
        client=client,
    )

    status = {
        "schema_version": "relay-v3.1-handover-provider-status",
        "authority": "PROVIDER_READBACK",
        "observed_at": _now(),
        "marker": "relay-v3.1",
        "parent": parent_readback,
        "handover": handover_readback,
    }
    errors = validate_schema("handover-provider-status", status, "HANDOVER_PROVIDER_STATUS")
    if errors:
        raise TransactionError("; ".join(errors))

    events, event_errors = load_events(root / "relay/EVENTS.jsonl")
    if event_errors:
        raise TransactionError("; ".join(event_errors[:8]))
    _assert_event_ids_available(events, [event_id])
    events.append(_event(
        event_id,
        "HANDOVER_LEDGER_SYNCED",
        actor,
        f"{parent_readback['repository']}#{parent_readback['issue_number']}",
        [
            tx_id,
            parent_readback["body_digest"],
            handover_readback["body_digest"],
        ],
        {
            "handover_issue": f"{handover_readback['repository']}#{handover_readback['issue_number']}",
            "parent_updated": parent_readback["updated"],
            "handover_updated": handover_readback["updated"],
        },
    ))

    return execute(
        root,
        tx_id=tx_id,
        command="SYNC_HANDOVER_LEDGER",
        actor=actor,
        replacements={
            "relay/GENERATED/HANDOVER_PROVIDER_STATUS.yaml": yaml_bytes(status),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronize generated V3.1 parent/Handover issue projections to GitHub and verify readback.")
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--tx-id", required=True)
    parser.add_argument("--event-id", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--api-base", default="https://api.github.com")
    parser.add_argument("--ledger")
    parser.add_argument("--ledger-markdown")
    parser.add_argument("--parent-summary")
    args = parser.parse_args()

    token = os.environ.get(args.token_env, "")
    result = sync_handover_provider(
        Path(args.repo_root).resolve(),
        tx_id=args.tx_id,
        event_id=args.event_id,
        actor=args.actor,
        token=token,
        ledger_path=Path(args.ledger) if args.ledger else None,
        ledger_markdown_path=Path(args.ledger_markdown) if args.ledger_markdown else None,
        parent_summary_path=Path(args.parent_summary) if args.parent_summary else None,
        api_base=args.api_base,
    )
    print(f"{result['id']}: {result['status']}")


if __name__ == "__main__":
    main()
