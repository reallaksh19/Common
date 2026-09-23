#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from handover_ledger_projection import render_ledger, render_parent_summary
from relay_tx import _assert_event_ids_available, _event, _issue_scoped_id, _transition_event_ids
from transactionlib import TransactionError, execute, jsonl_bytes, yaml_bytes
from v3lib import canonical_digest, load_events, load_yaml, validate_schema


START = "<!-- relay-v3.1:start -->"
END = "<!-- relay-v3.1:end -->"
CASE_MARKER_PREFIX = "<!-- relay-v3.1:case "
Client = Callable[[str, str, str, dict[str, Any] | None], Any]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _marked(content: str) -> str:
    return f"{START}\n{content.strip()}\n{END}"


def _case_marker(repository: str, number: int) -> str:
    return f"{CASE_MARKER_PREFIX}parent={repository}#{number} -->"


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


def _github_json(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> Any:
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
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TransactionError("GitHub provider returned invalid JSON") from exc


def _issue_url(api_base: str, repository: str, number: int) -> str:
    return f"{api_base.rstrip('/')}/repos/{repository}/issues/{number}"


def _subissues_url(api_base: str, repository: str, number: int) -> str:
    return f"{_issue_url(api_base, repository, number)}/sub_issues"


def _relay_candidates(rows: Any, repository: str, parent_number: int) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise TransactionError("GitHub sub-issue readback must be a list")
    marker = _case_marker(repository, parent_number)
    prefix = f"[Relay] #{parent_number}"
    result = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        title = str(row.get("title") or "")
        body = str(row.get("body") or "")
        if marker in body or title.startswith(prefix):
            result.append(row)
    return result


def _identity(issue: dict[str, Any], repository: str) -> dict[str, Any]:
    number = issue.get("number")
    if not isinstance(number, int):
        raise TransactionError("Relay issue provider response has no issue number")
    return {
        "repository": repository,
        "number": number,
        "url": str(issue.get("html_url") or f"https://github.com/{repository}/issues/{number}"),
    }


def _ensure_handover_issue(
    *,
    parent: dict[str, Any],
    requested: dict[str, Any] | None,
    token: str,
    api_base: str,
    client: Client,
) -> tuple[dict[str, Any], bool]:
    repository = str(parent.get("repository") or "")
    parent_number = int(parent.get("number"))
    rows = client("GET", _subissues_url(api_base, repository, parent_number), token, None)
    candidates = _relay_candidates(rows, repository, parent_number)
    if len(candidates) > 1:
        refs = ", ".join(f"#{row.get('number')}" for row in candidates)
        raise TransactionError(f"MULTIPLE_RELAY_ISSUES: {repository}#{parent_number} has {refs}")

    if isinstance(requested, dict):
        requested_number = int(requested.get("number"))
        if candidates and int(candidates[0].get("number")) != requested_number:
            raise TransactionError(
                f"RELAY_ISSUE_IDENTITY_MISMATCH: projection expects #{requested_number}, "
                f"parent is linked to #{candidates[0].get('number')}"
            )
        issue = client("GET", _issue_url(api_base, repository, requested_number), token, None)
        if not isinstance(issue, dict):
            raise TransactionError("requested Relay issue provider readback is invalid")
        if not candidates:
            issue_id = issue.get("id")
            if not isinstance(issue_id, int):
                raise TransactionError("requested Relay issue has no provider id for sub-issue attachment")
            client(
                "POST",
                _subissues_url(api_base, repository, parent_number),
                token,
                {"sub_issue_id": issue_id},
            )
        return _identity(issue, repository), False

    if candidates:
        return _identity(candidates[0], repository), False

    title = f"[Relay] #{parent_number} — {str(parent.get('title') or 'continuation ledger')}"
    body = "\n".join([
        _case_marker(repository, parent_number),
        "",
        "Generated Engineering Relay case file. Repository Relay objects remain engineering authority.",
    ])
    created = client(
        "POST",
        f"{api_base.rstrip('/')}/repos/{repository}/issues",
        token,
        {"title": title, "body": body},
    )
    if not isinstance(created, dict):
        raise TransactionError("GitHub Relay issue creation returned an invalid response")
    issue_id = created.get("id")
    if not isinstance(issue_id, int):
        raise TransactionError("created Relay issue has no provider id")
    client(
        "POST",
        _subissues_url(api_base, repository, parent_number),
        token,
        {"sub_issue_id": issue_id},
    )
    return _identity(created, repository), True


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
    if not isinstance(before, dict):
        raise TransactionError("GitHub issue readback must be an object")
    before_body = str(before.get("body") or "")
    desired_body = _replace_marked(before_body, desired_content)
    updated = desired_body != before_body
    if updated:
        client("PATCH", url, token, {"body": desired_body})
    after = client("GET", url, token, None)
    if not isinstance(after, dict):
        raise TransactionError("GitHub issue readback must be an object")
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
    tx_id: str | None,
    event_id: str | None,
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
    if not ledger_path.exists():
        raise TransactionError(f"HANDOVER_LEDGER is missing: {ledger_path}")

    ledger = load_yaml(ledger_path)
    errors = validate_schema("handover-ledger", ledger, "HANDOVER_LEDGER")
    if errors:
        raise TransactionError("; ".join(errors))

    parent = ledger.get("parent_issue") or {}
    governing_issue = int(parent.get("number")) if parent.get("number") is not None else None
    tx_id = _issue_scoped_id(
        root,
        kind="TX",
        value=tx_id,
        issue_number=governing_issue,
        label="transaction id",
    )
    event_id = _transition_event_ids(
        root,
        event_id=event_id,
        issue_number=governing_issue,
        legacy_suffixes=[""],
    )[0]
    handover_identity, created = _ensure_handover_issue(
        parent=parent,
        requested=ledger.get("handover_issue"),
        token=token,
        api_base=api_base,
        client=client,
    )
    resolved_ledger = copy.deepcopy(ledger)
    resolved_ledger["handover_issue"] = handover_identity
    errors = validate_schema("handover-ledger", resolved_ledger, "HANDOVER_LEDGER")
    if errors:
        raise TransactionError("; ".join(errors))

    parent_content = render_parent_summary(resolved_ledger)
    handover_content = render_ledger(resolved_ledger)
    parent_readback = _sync_issue(
        repository=str(parent.get("repository")),
        number=int(parent.get("number")),
        desired_content=parent_content,
        token=token,
        api_base=api_base,
        client=client,
    )
    handover_readback = _sync_issue(
        repository=handover_identity["repository"],
        number=int(handover_identity["number"]),
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
            "handover_issue_created": created,
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
            str(ledger_path.relative_to(root)): yaml_bytes(resolved_ledger),
            str(ledger_markdown_path.relative_to(root)): render_ledger(resolved_ledger).encode("utf-8"),
            str(parent_summary_path.relative_to(root)): render_parent_summary(resolved_ledger).encode("utf-8"),
            "relay/GENERATED/HANDOVER_PROVIDER_STATUS.yaml": yaml_bytes(status),
            "relay/EVENTS.jsonl": jsonl_bytes(events),
        },
        fail_after=fail_after,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronize generated V3.1 parent/Handover issue projections to GitHub and verify readback.")
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument(
        "--tx-id",
        help="Explicit transaction ID. Omit to allocate TX.<issue>.<serial> from the ledger parent issue.",
    )
    parser.add_argument(
        "--event-id",
        help="Explicit event ID. Omit to allocate EVT.<issue>.<serial> from the ledger parent issue.",
    )
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
