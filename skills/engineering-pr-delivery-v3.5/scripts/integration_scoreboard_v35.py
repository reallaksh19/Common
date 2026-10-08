"""R3: pure V3.5 smart issue/PR presentation from one DELP read model.

No provider I/O or mutation. DELP remains the progress/currentness owner.
The PR check-run verdict is an *observed check verdict*, never Local review,
custody, engineering completion, or programme acceptance authority.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from typing import Any

START = "<!-- V35_PR_SCOREBOARD_BEGIN -->"
END = "<!-- V35_PR_SCOREBOARD_END -->"
_TITLE = re.compile(r"^\[V35 [^\]\r\n]*\]\s*", re.UNICODE)
_SHA = re.compile(r"^[0-9a-f]{40}$")


class ScoreboardError(ValueError):
    """A missing, foreign or stale candidate must not be rendered as current."""


def _head(pull: Mapping[str, Any]) -> str:
    sha = (pull.get("head") or {}).get("sha")
    if not isinstance(sha, str) or not _SHA.fullmatch(sha):
        raise ScoreboardError("pull candidate head missing or not exact 40-char SHA")
    return sha


def _check_verdict(check_payload: Any, head_sha: str) -> dict[str, Any]:
    # Check conclusions are provider-observed, never substituted for semantic E.
    if not isinstance(check_payload, Mapping):
        return {"status": "UNKNOWN", "passed": 0, "total": 0, "reason": "CHECKS_UNOBSERVED"}
    rows = check_payload.get("check_runs")
    if not isinstance(rows, list):
        return {"status": "UNKNOWN", "passed": 0, "total": 0, "reason": "CHECKS_UNOBSERVED"}
    count = check_payload.get("total_count")
    if type(count) is not int or count != len(rows):
        return {"status": "UNKNOWN", "passed": 0, "total": len(rows), "reason": "CHECKS_PAGINATION_UNPROVEN"}
    # Exclude the writer's own check job, otherwise it can never stabilize.
    rows = [r for r in rows if isinstance(r, Mapping) and
            str(r.get("name") or "") != "V35 Smart Scoreboard"]
    if not rows:
        return {"status": "UNKNOWN", "passed": 0, "total": 0, "reason": "NO_INDEPENDENT_CHECKS"}
    if any(r.get("head_sha") != head_sha for r in rows):
        return {"status": "STALE", "passed": 0, "total": len(rows), "reason": "CHECK_RUN_HEAD_MISMATCH"}
    passed = sum(1 for r in rows if r.get("status") == "completed" and r.get("conclusion") == "success")
    bad = any(r.get("status") == "completed" and
              r.get("conclusion") in ("failure", "timed_out", "cancelled", "action_required")
              for r in rows)
    pending = any(r.get("status") != "completed" or r.get("conclusion") is None for r in rows)
    status = "FAIL" if bad else "PENDING" if pending else "PASS" if passed == len(rows) else "UNKNOWN"
    return {"status": status, "passed": passed, "total": len(rows), "reason": "PROVIDER_CHECK_RUNS_ONLY"}


def _title_base(title: str) -> str:
    """Strip only our owned prefix. A legacy bracketed title is human content."""
    return _TITLE.sub("", title, count=1).strip()


def managed_body(original: str, generated: str) -> str:
    """Replace exactly one V3.5-owned block; preserve unrelated human bytes."""
    if not isinstance(original, str) or not isinstance(generated, str):
        raise ScoreboardError("PR managed body: strings required")
    opens, closes = original.count(START), original.count(END)
    if opens != closes or opens > 1:
        raise ScoreboardError("duplicate or incomplete managed PR markers")
    block = START + "\n" + generated.rstrip() + "\n" + END
    if opens:
        left = original.index(START)
        right = original.index(END, left) + len(END)
        return original[:left] + block + original[right:]
    return block + "\n\n" + original


def render(model: Mapping[str, Any], pull: Mapping[str, Any], checks: Any) -> dict[str, Any]:
    """Render issue titles via DELP and PR title/body from exact same R2 source."""
    if model.get("mode") != "DELP_SOURCE_PROJECTED_READ_ONLY":
        raise ScoreboardError("refuse historical-only or authored progress as a production model")
    identity = model.get("source_identity")
    if not isinstance(identity, Mapping):
        raise ScoreboardError("canonical DELP identity missing")
    sha = _head(pull)
    if sha != model.get("candidate_sha"):
        raise ScoreboardError("pull head changed since DELP observation")
    ref = str(identity.get("responsibility_ref") or "")
    root = str(identity.get("programme_root") or "")
    repo = str(identity.get("repository") or "")
    if not repo or not ref or not root or not model.get("basis_sha256"):
        raise ScoreboardError("R2 model not correctly bound")
    primary = str((pull.get("base") or {}).get("repo", {}).get("full_name") or "")
    if primary and primary.casefold() != repo.casefold():
        raise ScoreboardError("PR belongs to a foreign repository")
    if bool(pull.get("merged")):
        pr_status = "MERGED_OBSERVED"
    elif pull.get("state") == "closed":
        pr_status = "CLOSED"
    elif pull.get("state") == "open" and pull.get("draft") is True:
        pr_status = "DRAFT"
    elif pull.get("state") == "open" and pull.get("draft") is False:
        pr_status = "OPEN_REVIEW"
    else:
        pr_status = "UNKNOWN"
    verdict = _check_verdict(checks, sha)
    # Current check status may change without a graph/evidence/head change.
    # Preserve the canonical DELP source basis and expose a distinct observed
    # PR presentation digest so 'same source' cannot masquerade as 'same checks'.
    presentation_digest = hashlib.sha256(
        json.dumps(
            [model["basis_sha256"], sha, pr_status, verdict],
            sort_keys=True, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()
    raw_progress = model.get("progress")
    if not isinstance(raw_progress, Mapping):
        raise ScoreboardError("projected progress absent")
    p, e = raw_progress.get("P"), raw_progress.get("E")
    if type(p) is not int or type(e) is not int or not (0 <= e <= p <= 100):
        raise ScoreboardError("DELP progress not normalized")
    action = (model.get("actual_next") or {}).get("action")
    if not isinstance(action, str) or not action:
        raise ScoreboardError("canonical actual-next missing")
    # A title contains observed material, not fabricated review/IC qualification.
    prefix = (
        f"[V35 {root}→{ref} {pr_status} P{p}/E{e} "
        f"CI:{verdict['status']}@{sha[:7]} NEXT:{action}]"
    )
    previous_title = str(pull.get("title") or "")
    base = _title_base(previous_title) or "Candidate engineering delivery"
    remaining = 256 - len(prefix) - 1
    if remaining < 12:
        raise ScoreboardError("smart PR title prefix too large")
    title = prefix + " " + base[:remaining]
    body = "\n".join((
        "## V3.5 smart candidate scoreboard — managed read-only projection",
        f"- **DELP source basis:** `{model['basis_sha256']}`",
        f"- **PR check presentation digest:** `{presentation_digest}` (separate observed CI layer)",
        f"- **Graph:** `{identity['graph_digest']}`; source: DELP accepted-facts projection",
        f"- **Repository/lineage:** `{repo}` · `{root}` → `{ref}`",
        f"- **Spec generation / contract:** `{identity.get('spec_generation') or 'UNKNOWN'}` / `{identity.get('contract_digest') or 'UNKNOWN'}`",
        f"- **Candidate:** `{sha}` · **PR:** {pr_status}",
        f"- **Engineering P/E:** `P{p}/E{e}` (never Local completion)",
        f"- **Observed CI:** `{verdict['status']} {verdict['passed']}/{verdict['total']}` — {verdict['reason']}; NOT semantic acceptance",
        f"- **Actual next:** `{action}`",
        f"- **Accepted evidence sources:** {', '.join(str(x) for x in model.get('accepted_evidence_sources', ())) or 'NONE'}",
        f"- **Owner source:** `{(model.get('owner') or {}).get('authentication') or 'UNKNOWN'}`",
        "- **Programme IC / native custody / Local reviewer / merge authority:** NOT VERIFIED BY THIS WRITER",
        "- **Writer semantics:** generated from one observed snapshot; cross-issue/PR writes are NOT atomic.",
    )) + "\n"
    return {
        "basis_sha256": model["basis_sha256"],
        "presentation_digest": presentation_digest,
        "candidate_sha": sha,
        "issue_titles": {k: model["titles"][k] for k in ("parent_issue", "child_issue")},
        "pr_title": title,
        "pr_managed_body": body,
        "checks": verdict,
        "pr_status": pr_status,
        "progress": {"P": p, "E": e},
        "actual_next": action,
        "idempotency_digest": hashlib.sha256(json.dumps(
            [model["basis_sha256"], presentation_digest, sha, title, body], ensure_ascii=False
        ).encode("utf-8")).hexdigest(),
    }
