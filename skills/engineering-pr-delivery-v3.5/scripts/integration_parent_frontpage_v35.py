"""R7-U5: pure V3.5 managed parent front-page integrity / legacy archive plan.

Does not derive status, progress, graph approval, native Owner provenance,
human review, or GitHub write permission. GitHub issue body writes are done
separately by a permitted human/operator after native archive readback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

START = "<!-- V35_CURRENT_FRONT_PAGE_BEGIN -->"
END = "<!-- V35_CURRENT_FRONT_PAGE_END -->"
_FRONT = "V35_CURRENT_FRONT_PAGE"
_OWNER = "<!-- V35_PARENT_OWNER_INTENT_BEGIN -->"
_INT = "<!-- V35_INTEGRATION_CURRENT_BEGIN -->"
_MARKER = re.compile(r"<!-- (V35_[A-Z0-9_]+)_BEGIN -->")
PROTECTED = {
    600: _OWNER,      # Original Owner prose is not a status banner
    717: _INT,        # Original integration acceptance matrix
    759: "# R7",     # Original native execution issue statement
}
HISTORICAL = {
    600: frozenset((
        "V35_R7_U4D2_600", "V35_U4D_FINAL_EXEC_600",
        "V35_U4D_LATEST_600", "V35_U4D_STATUS_600",
        "V35_CURRENT_FRONTIER_600", "V35_FINAL_STAT_600",
        "V35_R7_UPDATE_U3_U4_600", "V35_DETAIL_CURRENT_600",
        "V35_R7_CURRENT_600", "V35_R6_MERGE_LIVE_RECONCILIATION_600",
        "V35_MERGED_RECONCILIATION_600", "V35_LATEST_R2C_600",
        "V35_MERGED_SOURCE_RELEASE_600",
        "V35_R3_R4_741_GOVERNANCE_600", "V35_600_R1_R2_SOURCE_FIX",
    )),
    717: frozenset((
        "V35_R7_U4D2_717", "V35_U4D_FINAL_EXEC_717",
        "V35_U4D_LATEST_717", "V35_U4D_STATUS_717",
        "V35_CURRENT_FRONTIER_717", "V35_FINAL_STAT_717",
        "V35_R7_UPDATE_U3_U4_717", "V35_DETAIL_CURRENT_717",
        "V35_R7_CURRENT_717", "V35_R6_MERGE_LIVE_RECONCILIATION_717",
        "V35_MERGED_RECONCILIATION_717", "V35_LATEST_R2C_717",
        "V35_R2B_743_STATE_717", "V35_MERGED_SOURCE_RELEASE_717",
        "V35_R3_R4_741_GOVERNANCE_717", "V35_717_R1_R2_SOURCE_FIX",
    )),
    759: frozenset((
        "V35_R7_U4D2_759", "V35_U4D_FINAL_EXEC_759",
        "V35_U4D_LATEST_759", "V35_U4D_STATUS_759",
        "V35_CURRENT_FRONTIER_759", "V35_FINAL_STAT_759",
        "V35_R7_UPDATE_U3_U4_759", "V35_DETAIL_CURRENT_759",
        "V35_R7_U3_U4_CURRENT", "V35_R7_CURRENT_759",
    )),
}
FRONT_LIMIT = 4096


class FrontPageError(ValueError):
    """Malformed front-page status or attempted human-content deletion."""


def _check_issue(issue: int) -> None:
    if issue not in HISTORICAL:
        raise FrontPageError("only audited root #600 / R7 #759 / IC #717 supported")


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _paired(body: str, tag: str, start: int = 0) -> int:
    close = f"<!-- {tag}_END -->"
    if body.count(close) != 1 or body.count(f"<!-- {tag}_BEGIN -->") != 1:
        raise FrontPageError("duplicate/missing owner-managed marker " + tag)
    at = body.find(close, start)
    if at < start:
        raise FrontPageError("reversed marker pair " + tag)
    if _MARKER.search(body, start + len(f"<!-- {tag}_BEGIN -->"), at):
        raise FrontPageError("nested marker inside managed status block " + tag)
    return at + len(close)


def archive_legacy_prefix(body: str, issue: int) -> dict[str, Any]:
    """Return verbatim candidate archive; NEVER send it to GitHub or delete it.

    Only explicitly audited OLD status markers at the START of the issue body
    are eligible. Other markers and all unowned text are protected.
    """
    _check_issue(issue)
    if not isinstance(body, str):
        raise FrontPageError("issue body must be a string")
    if body.startswith(START):
        validate_current(body, issue)
        return {"archive_text": "", "remaining_body": body, "archive_sha256": _sha(""),
                "archived_count": 0, "requires_verified_native_archive": False}
    cursor, count = 0, 0
    while cursor < len(body):
        match = _MARKER.match(body, cursor)
        if match is None:
            break
        tag = match.group(1)
        if tag not in HISTORICAL[issue]:
            raise FrontPageError(f"unknown/protected prefix cannot be archived: {tag}")
        close_end = _paired(body, tag, cursor)
        cursor = close_end
        count += 1
        whitespace = re.match(r"\s*", body[cursor:])
        next_at = cursor + len(whitespace.group())
        if next_at < len(body) and _MARKER.match(body, next_at):
            cursor = next_at
        else:
            break
    archive = body[:cursor]
    remaining = body[cursor:]
    if count and (not remaining.strip() or
                  PROTECTED[issue] not in remaining):
        raise FrontPageError("archival proposal would orphan original governing content")
    if issue == 600 and count and _OWNER in archive:
        raise FrontPageError("Owner intent cannot be archived")
    if issue == 717 and count and _INT in archive:
        raise FrontPageError("integration contract cannot be archived")
    return {
        "archive_text": archive,
        "remaining_body": remaining,
        "archive_sha256": _sha(archive),
        "archived_count": count,
        "requires_verified_native_archive": count > 0,
    }


def validate_current(body: str, issue: int) -> dict[str, Any]:
    """Require one bounded current panel; status content itself is NOT trust."""
    _check_issue(issue)
    if not isinstance(body, str) or not body.startswith(START):
        raise FrontPageError("current front page must start at byte zero")
    close_at = _paired(body, _FRONT)
    if close_at > FRONT_LIMIT:
        raise FrontPageError("current front page exceeds bounded cold-entry view")
    rest = body[close_at:]
    protected = PROTECTED[issue]
    idx = rest.find(protected)
    if idx < 0:
        raise FrontPageError("Owner/parent governing source missing after front page")
    if close_at + idx > FRONT_LIMIT:
        raise FrontPageError("Owner/parent source buried by status text")
    # No historical banner may sneak back above MY INTENT or source matrix.
    for match in _MARKER.finditer(rest[:idx]):
        if match.group(1) in HISTORICAL[issue]:
            raise FrontPageError("obsolete status banner precedes Owner/parent source")
    return {
        "schema": "V35_PARENT_FRONT_PAGE_INTEGRITY_V1",
        "issue": issue,
        "current_panel_span": close_at,
        "governing_source_position": close_at + idx,
        "protected_tail_sha256": _sha(rest),
        "status_authority": "MANUAL_NAVIGATION_ONLY_NOT_DELP_OR_OWNER",
        "writes": False,
    }


def propose(body: str, issue: int, current: str) -> dict[str, Any]:
    """Pure proposal. If archiving, first post archive + read back independently.

    Keeps every byte outside exactly one machine-owned current panel. Do not
    apply directly; no GitHub transport/credentials imported.
    """
    _check_issue(issue)
    if not isinstance(current, str) or not current.strip():
        raise FrontPageError("nonempty current panel content required")
    if "<!--" in current or "-->" in current:
        raise FrontPageError("current text may not inject HTML authority markers")
    plan = archive_legacy_prefix(body, issue)
    remaining = plan["remaining_body"]
    if remaining.startswith(START):
        end = _paired(remaining, _FRONT)
        remaining = remaining[end:]
    result = START + "\n" + current.strip() + "\n" + END + remaining
    check = validate_current(result, issue)
    return {
        "schema": "V35_PARENT_FRONT_PAGE_PROPOSAL_V1",
        "issue": issue,
        "proposed_body": result,
        "archive_text": plan["archive_text"],
        "archive_sha256": plan["archive_sha256"],
        "archive_required": plan["requires_verified_native_archive"],
        "archived_count": plan["archived_count"],
        "status_authority": "PROPOSAL_ONLY_NO_GITHUB_WRITE",
        "governing_source_position": check["governing_source_position"],
        "writes": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only V3.5 parent-front-page guard")
    parser.add_argument("--issue", required=True, type=int)
    parser.add_argument("--body-file", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate_current(args.body_file.read_text(encoding="utf-8"), args.issue)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, FrontPageError) as exc:
        print(f"V3.5 parent current front page HOLD: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
