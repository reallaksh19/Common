#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

AUTHORITY = "DERIVED_CONTINUITY_ONLY"
SCHEMA = "relay-v3.2-responsibility-continuity"
START = "<!-- relay-v3.2:further-task:start -->"
END = "<!-- relay-v3.2:further-task:end -->"
RECOVERY_MARKER_PREFIX = "<!-- relay-v3.2:recovery-evidence "
TITLE_RE = re.compile(r"\s+\{P\d+% · E\d+% · [^{}]+\}\s*$")
RECOVERY_MODES = {"NONE", "INTERRUPTED_EXECUTOR", "FRONTIER_RECONCILIATION"}

# Who may say a unit is "evidenced"?
#   LEGACY_AGENT_ASSERTED  the agent sets the flag itself (historical snapshots only; readable, never new)
#   DERIVED_FROM_FACTS     the flag is computed: complete AND durable evidence refs AND the evidence
#                          candidate equals the observed material head. Agents publish facts only.
PROJECTION_LEGACY = "LEGACY_AGENT_ASSERTED"
PROJECTION_DERIVED = "DERIVED_FROM_FACTS"
PROJECTION_MODES = {PROJECTION_LEGACY, PROJECTION_DERIVED}
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ContinuityError(ValueError):
    pass


def pct(n: int, d: int) -> int:
    return round(100 * n / d) if d else 0


def pct_derived(n: int, d: int) -> int:
    """Half-up percent that never shows 100 unless full or 0 unless empty (matches DELP)."""
    if not d or n <= 0:
        return 0
    if n >= d:
        return 100
    return min(99, max(1, (200 * n + d) // (2 * d)))


def _derived_evidenced(unit: dict[str, Any], material_head: str | None) -> bool:
    return bool(
        unit.get("complete")
        and [ref for ref in unit.get("evidence_refs") or [] if str(ref).strip()]
        and material_head
        and unit.get("evidence_candidate") == material_head
    )


def normalize_units(
    units: list[dict[str, Any]],
    *,
    derived: bool = False,
    material_head: str | None = None,
    from_agent: bool = False,
) -> list[dict[str, Any]]:
    """Validate units. `from_agent=True` marks input an agent just supplied (declaration time);
    stored units already carry a *derived* `evidenced` value that is recomputed, not trusted."""
    if not units:
        raise ContinuityError("at least one declared progress unit is required")
    out, seen = [], set()
    for raw in units:
        uid = str(raw.get("id") or "").strip()
        if not uid or uid in seen:
            raise ContinuityError(f"invalid/duplicate unit id: {uid!r}")
        seen.add(uid)
        complete = bool(raw.get("complete"))
        weight = raw.get("weight", 1)
        if isinstance(weight, bool) or not isinstance(weight, int) or weight < 1:
            raise ContinuityError(f"{uid}: weight must be a positive integer")
        if derived:
            if from_agent and raw.get("evidenced"):
                raise ContinuityError(
                    f"{uid}: 'evidenced' is derived, never asserted; publish evidence_refs "
                    "and the evidence_candidate the refs cover"
                )
            unit = {**raw, "id": uid, "complete": complete, "weight": weight}
            unit["evidenced"] = _derived_evidenced(unit, material_head)
            out.append(unit)
            continue
        evidenced = bool(raw.get("evidenced"))
        if evidenced and not complete:
            raise ContinuityError(f"{uid}: evidence cannot lead completion")
        out.append({**raw, "id": uid, "complete": complete, "evidenced": evidenced, "weight": weight})
    return out


def progress(
    units: list[dict[str, Any]],
    *,
    derived: bool = False,
    material_head: str | None = None,
) -> dict[str, Any]:
    units = normalize_units(units, derived=derived, material_head=material_head)
    denominator = sum(unit["weight"] for unit in units)
    completed = sum(unit["weight"] for unit in units if unit["complete"])
    evidenced = sum(unit["weight"] for unit in units if unit["evidenced"])
    percent = pct_derived if derived else pct
    return {
        "denominator": denominator,
        "completed_units": completed,
        "evidenced_units": evidenced,
        "progress_percent": percent(completed, denominator),
        "evidence_percent": percent(evidenced, denominator),
        "active_unit": next((unit["id"] for unit in units if not unit["complete"]), None),
    }


def _is_derived(snapshot: dict[str, Any]) -> bool:
    return snapshot.get("projection_mode") == PROJECTION_DERIVED


def reproject(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Recompute unit.evidenced and progress from facts. Idempotent; the only writer of P/E."""
    s = deepcopy(snapshot)
    derived = _is_derived(s)
    head = (s.get("frontier") or {}).get("material_head")
    s["units"] = normalize_units(s["units"], derived=derived, material_head=head)
    s["progress"] = progress(s["units"], derived=derived, material_head=head)
    return s


def frontier(
    material: str | None,
    semantic: str | None,
    delta: int | None = None,
) -> dict[str, Any]:
    material = (material or "").strip() or None
    semantic = (semantic or "").strip() or None
    if delta is not None and delta < 0:
        raise ContinuityError("delta cannot be negative")
    if not material:
        relation = "MATERIAL_UNKNOWN"
    elif not semantic:
        relation = "SEMANTIC_UNKNOWN"
    elif material == semantic:
        relation, delta = "ALIGNED", 0
    elif delta == 0:
        relation = "UNRESOLVED"
    else:
        relation = "MATERIAL_AHEAD"
    return {
        "material_head": material,
        "semantic_evidence_head": semantic,
        "relation": relation,
        "delta_commits": delta,
        "recovery_reconciliation_needed": relation
        in {"MATERIAL_AHEAD", "SEMANTIC_UNKNOWN", "UNRESOLVED"},
    }


def new_snapshot(
    responsibility: str,
    units: list[dict[str, Any]],
    plan_ref: str | None,
    material: str | None,
    semantic: str | None,
    delta: int | None,
    repository: str | None = None,
    issue: int | None = None,
    protocol_ref: str | None = None,
    projection_mode: str = PROJECTION_LEGACY,
) -> dict[str, Any]:
    if projection_mode not in PROJECTION_MODES:
        raise ContinuityError(f"invalid projection mode: {projection_mode}")
    derived = projection_mode == PROJECTION_DERIVED
    head = (material or "").strip() or None
    units = normalize_units(units, derived=derived, material_head=head, from_agent=True)
    return {
        "schema": SCHEMA,
        "authority": AUTHORITY,
        "projection_mode": projection_mode,
        "responsibility": responsibility,
        "protocol_ref": (protocol_ref or "").strip() or None,
        "state": "PLANNING",
        "plan_ref": plan_ref,
        "units": units,
        "progress": progress(units, derived=derived, material_head=head),
        "frontier": frontier(material, semantic, delta),
        "current": None,
        "next": None,
        "owner_decision": "NONE",
        "recovery": {
            "mode": "NONE",
            "stream_loss_count": 0,
            "recovery_evidence_required": False,
            "handover_plan_triggered_this_lifecycle": False,
            "plan_for_handover_now": False,
            "recovery_evidence": None,
        },
        "provider": {
            "type": "GITHUB" if repository and issue else None,
            "repository": repository,
            "issue_number": issue,
        },
        "observability": {
            "provider_sync_required": False,
            "provider_sync_failure_blocks_engineering": False,
            "update_reason": None,
            "provider_sync": {"status": "NOT_REQUESTED"},
        },
    }


def _recovery(snapshot: dict[str, Any]) -> dict[str, Any]:
    recovery = snapshot.setdefault("recovery", {})
    recovery.setdefault("mode", "NONE")
    recovery.setdefault("stream_loss_count", 0)
    recovery.setdefault("recovery_evidence_required", False)
    recovery.setdefault("handover_plan_triggered_this_lifecycle", False)
    recovery.setdefault("plan_for_handover_now", False)
    recovery.setdefault("recovery_evidence", None)
    return recovery


def event(snapshot: dict[str, Any], name: str, **kwargs: Any) -> dict[str, Any]:
    s = deepcopy(snapshot)
    recovery = _recovery(s)
    if name == "implementation-start":
        if not s.get("plan_ref"):
            raise ContinuityError("implementation start requires published plan_ref")
        if s["state"] in {"COMPLETE", "SUPERSEDED"}:
            raise ContinuityError("terminal responsibility")
        s["state"] = "IMPLEMENTING"

    elif name == "stream-loss":
        recovery["mode"] = "INTERRUPTED_EXECUTOR"
        recovery["stream_loss_count"] += 1
        recovery["recovery_evidence_required"] = True
        recovery["recovery_evidence"] = None
        recovery["plan_for_handover_now"] = (
            recovery["stream_loss_count"] >= 3
            and not recovery["handover_plan_triggered_this_lifecycle"]
        )
        if recovery["plan_for_handover_now"]:
            recovery["handover_plan_triggered_this_lifecycle"] = True
        s["state"] = "RECOVERING"

    elif name == "recovery-start":
        mode = str(kwargs.get("mode") or "FRONTIER_RECONCILIATION")
        if mode not in RECOVERY_MODES - {"NONE"}:
            raise ContinuityError(f"invalid recovery mode: {mode}")
        if (
            mode == "FRONTIER_RECONCILIATION"
            and not s.get("frontier", {}).get("recovery_reconciliation_needed")
        ):
            raise ContinuityError("frontier reconciliation recovery requires unresolved frontier")
        recovery["mode"] = mode
        recovery["recovery_evidence_required"] = True
        recovery["recovery_evidence"] = None
        recovery["plan_for_handover_now"] = False
        s["state"] = "RECOVERING"

    elif name == "recovery-evidence":
        if not recovery["recovery_evidence_required"]:
            raise ContinuityError("recovery evidence not required")
        material_head = s["frontier"].get("material_head")
        if not material_head:
            raise ContinuityError("recovery evidence requires observed material head")
        recovery["recovery_evidence"] = {
            "observed_material_head": material_head,
            "last_trusted_semantic_head": s["frontier"].get("semantic_evidence_head"),
            "recovered_delta_commits": s["frontier"].get("delta_commits"),
            "claim": kwargs.get("claim") or "Recovered live responsibility/material state.",
            "not_yet_proved": kwargs.get("not_yet_proved") or "None stated.",
            "open_work": kwargs.get("open_work") or "See current Further Task snapshot.",
            "owner_decision": kwargs.get("owner_decision") or s.get("owner_decision") or "NONE",
            "next": kwargs.get("next") or s.get("next") or "Resume first useful engineering action.",
        }
        s["state"] = "EVIDENCING"

    elif name == "unit-update":
        uid = kwargs["unit_id"]
        derived = _is_derived(s)
        if derived and kwargs.get("evidenced") is not None:
            raise ContinuityError(
                "evidenced is derived from evidence_refs + evidence_candidate; "
                "agents publish facts, never the E flag"
            )
        found = False
        for unit in s["units"]:
            if unit["id"] == uid:
                found = True
                if kwargs.get("complete") is not None:
                    unit["complete"] = kwargs["complete"]
                if kwargs.get("evidence_refs") is not None:
                    unit["evidence_refs"] = [str(r).strip() for r in kwargs["evidence_refs"] if str(r).strip()]
                if kwargs.get("evidence_candidate") is not None:
                    candidate = str(kwargs["evidence_candidate"]).strip()
                    if not _SHA_RE.fullmatch(candidate):
                        raise ContinuityError("evidence_candidate must be a 40-hex lowercase commit")
                    unit["evidence_candidate"] = candidate
                if not derived:
                    if kwargs.get("evidenced") is not None:
                        unit["evidenced"] = kwargs["evidenced"]
                    if unit["evidenced"] and not unit["complete"]:
                        raise ContinuityError(f"{uid}: evidence cannot lead completion")
                elif not unit["complete"]:
                    unit["evidence_refs"], unit["evidence_candidate"] = [], None
        if not found:
            raise ContinuityError(f"unknown unit: {uid}")
        s = reproject(s)

    elif name == "task-result":
        scope = kwargs["scope"]
        complete = kwargs["responsibility_complete"]
        if scope not in {"STEP", "PRODUCT", "RESPONSIBILITY"}:
            raise ContinuityError("invalid result scope")
        if complete is True and scope != "RESPONSIBILITY":
            raise ContinuityError("complete YES requires RESPONSIBILITY scope")
        s["result"] = {
            "result_scope": scope,
            "coverage": kwargs["coverage"],
            "responsibility_complete": complete,
        }
        if complete is True:
            s["state"] = "COMPLETE"

    else:
        raise ContinuityError(f"unknown event: {name}")

    s["observability"]["provider_sync_required"] = True
    s["observability"]["update_reason"] = name.upper().replace("-", "_")
    return s


def finalize_recovery_evidence(snapshot: dict[str, Any], comment_id: int | None = None) -> dict[str, Any]:
    s = deepcopy(snapshot)
    recovery = _recovery(s)
    evidence = recovery.get("recovery_evidence")
    if not evidence:
        raise ContinuityError("no pending recovery evidence to finalize")
    material_head = evidence["observed_material_head"]
    s["frontier"] = frontier(material_head, material_head, 0)
    s = reproject(s)
    recovery = _recovery(s)
    recovery["mode"] = "NONE"
    recovery["recovery_evidence_required"] = False
    recovery["plan_for_handover_now"] = False
    recovery["recovery_evidence"] = {
        **evidence,
        "publication_status": "READ_BACK",
        "provider_comment_id": comment_id,
    }
    s["state"] = "IMPLEMENTING"
    s["observability"]["update_reason"] = "RECOVERY_EVIDENCE_PUBLISHED"
    return s


def git_frontier(repo: Path, semantic: str | None) -> dict[str, Any]:
    def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            text=True,
            capture_output=True,
            check=check,
        )

    try:
        material = git("rev-parse", "HEAD").stdout.strip()
    except Exception as exc:
        raise ContinuityError(f"cannot resolve Git HEAD: {exc}") from exc

    if not semantic:
        return frontier(material, None)
    if git("cat-file", "-e", f"{semantic}^{{commit}}", check=False).returncode:
        return frontier(material, semantic)
    if semantic == material:
        return frontier(material, semantic, 0)
    if git("merge-base", "--is-ancestor", semantic, material, check=False).returncode == 0:
        delta = int(git("rev-list", "--count", f"{semantic}..{material}").stdout.strip())
        return frontier(material, semantic, delta)
    return {
        **frontier(material, semantic),
        "relation": "UNRESOLVED",
        "delta_commits": None,
        "recovery_reconciliation_needed": True,
    }


def title(snapshot: dict[str, Any], existing: str) -> str:
    p = snapshot["progress"]
    active = p["active_unit"]
    unit = active or ("COMPLETE" if snapshot["state"] == "COMPLETE" else "NO_ACTIVE_UNIT")
    suffix = (
        f"{{P{p['progress_percent']}% · E{p['evidence_percent']}% · "
        f"{unit} · {snapshot['state']}}}"
    )
    return f"{TITLE_RE.sub('', existing).rstrip()} {suffix}".strip()


def markdown(snapshot: dict[str, Any]) -> str:
    p, f = snapshot["progress"], snapshot["frontier"]
    r = _recovery(snapshot)
    done = [u["id"] for u in snapshot["units"] if u["complete"]]
    pending = [u["id"] for u in snapshot["units"] if not u["complete"]]
    lines = [
        "FURTHER_TASK_SNAPSHOT — current",
        "",
        f"AUTHORITY: {AUTHORITY}",
        f"PROTOCOL_REF: {snapshot.get('protocol_ref') or 'UNKNOWN'}",
        f"STATE: {snapshot['state']}",
        (
            f"PROJECTION_MODE: {snapshot.get('projection_mode') or PROJECTION_LEGACY}"
            + (
                " (E is computed from evidence refs + candidate; titles are written only by the DELP runner)"
                if _is_derived(snapshot)
                else " (historical: E was asserted by an agent; new responsibilities use DERIVED_FROM_FACTS)"
            )
        ),
        (
            f"PROGRESS: P{p['progress_percent']}% / E{p['evidence_percent']}% "
            f"({p['completed_units']}/{p['denominator']} complete; "
            f"{p['evidenced_units']}/{p['denominator']} evidenced)"
        ),
        f"ACTIVE_UNIT: {p['active_unit'] or 'NONE'}",
        f"PLAN: {snapshot.get('plan_ref') or 'UNKNOWN'}",
        (
            "FRONTIER: "
            f"material={f['material_head'] or 'UNKNOWN'}; "
            f"semantic/evidence={f['semantic_evidence_head'] or 'UNKNOWN'}; "
            f"relation={f['relation']}; "
            f"delta={f['delta_commits'] if f['delta_commits'] is not None else 'UNKNOWN'}; "
            f"reconciliation_needed={str(bool(f.get('recovery_reconciliation_needed'))).lower()}"
        ),
        "",
        "COMPLETED",
        *([f"- [x] {item}" for item in done] or ["- none"]),
        "",
        "ACTIVE / PENDING",
        *([f"- [ ] {item}" for item in pending] or ["- none"]),
        "",
        f"CURRENT: {snapshot.get('current') or 'UNSPECIFIED'}",
        f"NEXT: {snapshot.get('next') or 'UNSPECIFIED'}",
        f"OWNER_DECISION: {snapshot.get('owner_decision') or 'NONE'}",
        (
            "RECOVERY: "
            f"mode={r.get('mode', 'NONE')}; "
            f"stream_loss_count={r['stream_loss_count']}; "
            f"evidence_required={str(r['recovery_evidence_required']).lower()}; "
            f"handover_plan_triggered="
            f"{str(r['handover_plan_triggered_this_lifecycle']).lower()}; "
            f"plan_for_handover_now={str(r['plan_for_handover_now']).lower()}"
        ),
        "",
        "Derived continuity view only; not engineering permission or acceptance evidence.",
    ]
    return "\n".join(lines)


def recovery_evidence_markdown(snapshot: dict[str, Any]) -> tuple[str, str]:
    recovery = _recovery(snapshot)
    evidence = recovery.get("recovery_evidence")
    if not evidence:
        raise ContinuityError("no pending recovery evidence")
    material = evidence["observed_material_head"]
    loss = recovery["stream_loss_count"]
    marker = f"{RECOVERY_MARKER_PREFIX}loss={loss} material={material} -->"
    body = "\n".join(
        [
            marker,
            "TASK_EVIDENCE — RECOVERY",
            "",
            "RESPONSIBILITY",
            str(snapshot["responsibility"]),
            "",
            "PROTOCOL REF",
            str(snapshot.get("protocol_ref") or "UNKNOWN"),
            "",
            "RECOVERY MODE",
            str(recovery.get("mode") or "NONE"),
            "",
            "OBSERVED MATERIAL",
            f"head: {material}",
            "",
            "LAST TRUSTED SEMANTIC BASIS",
            str(evidence.get("last_trusted_semantic_head") or "UNKNOWN"),
            "",
            "RECOVERED DELTA",
            str(
                evidence.get("recovered_delta_commits")
                if evidence.get("recovered_delta_commits") is not None
                else "UNKNOWN"
            ),
            "",
            "CURRENT CLAIM",
            str(evidence["claim"]),
            "",
            "NOT YET PROVED",
            str(evidence["not_yet_proved"]),
            "",
            "OPEN WORK",
            str(evidence["open_work"]),
            "",
            "OWNER DECISION",
            str(evidence["owner_decision"]),
            "",
            "NEXT",
            str(evidence["next"]),
        ]
    )
    return marker, body


def marked(body: str, content: str) -> str:
    block = f"{START}\n{content.strip()}\n{END}"
    body = body or ""
    start = body.find(START)
    end = body.find(END)
    if start >= 0 and end >= start:
        end += len(END)
        return (
            body[:start].rstrip()
            + ("\n\n" if body[:start].strip() else "")
            + block
            + body[end:]
        )
    return block if not body.strip() else body.rstrip() + "\n\n" + block + "\n"


def gh_json(*args: str) -> Any:
    proc = subprocess.run(
        ["gh", "api", *args],
        text=True,
        capture_output=True,
    )
    if proc.returncode:
        raise ContinuityError(proc.stderr.strip() or "gh api failed")
    return json.loads(proc.stdout) if proc.stdout.strip() else {}


def gh_patch(endpoint: str, payload: dict[str, Any]) -> Any:
    args = ["--method", "PATCH", endpoint]
    for key, value in payload.items():
        args += ["-f", f"{key}={value}"]
    return gh_json(*args)


def gh_post(endpoint: str, payload: dict[str, Any]) -> Any:
    args = ["--method", "POST", endpoint]
    for key, value in payload.items():
        args += ["-f", f"{key}={value}"]
    return gh_json(*args)


def gh_comments(repo: str, issue: int) -> list[dict[str, Any]]:
    all_rows: list[dict[str, Any]] = []
    page = 1
    while True:
        rows = gh_json(
            "--method",
            "GET",
            f"repos/{repo}/issues/{issue}/comments",
            "-f",
            "per_page=100",
            "-f",
            f"page={page}",
        )
        if not isinstance(rows, list):
            raise ContinuityError("GitHub comments response must be a list")
        all_rows.extend(rows)
        if len(rows) < 100:
            return all_rows
        page += 1


def sync_github(snapshot: dict[str, Any]) -> dict[str, Any]:
    s = deepcopy(snapshot)
    provider = s.get("provider") or {}
    repo, issue = provider.get("repository"), provider.get("issue_number")
    if provider.get("type") != "GITHUB" or not repo or not isinstance(issue, int):
        s["observability"]["provider_sync"] = {"status": "NOT_CONFIGURED"}
        return s

    try:
        issue_obj = gh_json(f"repos/{repo}/issues/{issue}")
        comments = gh_comments(repo, issue)

        # Recovery evidence is append-only semantic truth. It must be posted and
        # read back successfully before recovery can be cleared or the semantic
        # frontier can advance to the observed material head.
        if s["observability"].get("update_reason") == "RECOVERY_EVIDENCE":
            marker, evidence_body = recovery_evidence_markdown(s)
            evidence_matches = [
                row
                for row in comments
                if marker in str(row.get("body") or "")
            ]
            if len(evidence_matches) > 1:
                raise ContinuityError("multiple matching recovery-evidence comments")
            if evidence_matches:
                evidence_comment = evidence_matches[0]
            else:
                evidence_comment = gh_post(
                    f"repos/{repo}/issues/{issue}/comments",
                    {"body": evidence_body},
                )
            evidence_id = int(evidence_comment["id"])
            readback = gh_json(f"repos/{repo}/issues/comments/{evidence_id}")
            readback_body = str(readback.get("body") or "")
            if marker not in readback_body or "TASK_EVIDENCE — RECOVERY" not in readback_body:
                raise ContinuityError("recovery evidence readback mismatch")
            s = finalize_recovery_evidence(s, evidence_id)
            comments = gh_comments(repo, issue)

        matches = [row for row in comments if START in str(row.get("body") or "")]
        if len(matches) > 1:
            raise ContinuityError("multiple managed Further Task comments")

        managed_body = marked(
            str(matches[0].get("body") or "") if matches else "",
            markdown(s),
        )
        if matches:
            status_comment_id = int(matches[0]["id"])
            gh_patch(
                f"repos/{repo}/issues/comments/{status_comment_id}",
                {"body": managed_body},
            )
        else:
            created = gh_post(
                f"repos/{repo}/issues/{issue}/comments",
                {"body": managed_body},
            )
            status_comment_id = int(created["id"])

        if _is_derived(s):
            # One title writer per issue: the DELP runner owns lineage/roll-up titles, so a
            # DERIVED snapshot never patches the title (no dual writers, no format fights).
            desired_title = str(issue_obj.get("title") or "")
            s["observability"]["title_authority"] = "DELP_RUNNER"
        else:
            desired_title = title(s, str(issue_obj.get("title") or ""))
            s["observability"]["title_authority"] = "LEGACY_CONTINUITY_PROJECTION"
        if desired_title != str(issue_obj.get("title") or ""):
            gh_patch(
                f"repos/{repo}/issues/{issue}",
                {"title": desired_title},
            )

        issue_readback = gh_json(f"repos/{repo}/issues/{issue}")
        status_readback = gh_json(
            f"repos/{repo}/issues/comments/{status_comment_id}"
        )
        if START not in str(status_readback.get("body") or ""):
            raise ContinuityError("Further Task readback mismatch")
        sync_status = (
            "SYNCED"
            if issue_readback.get("title") == desired_title
            else "READBACK_MISMATCH"
        )
        s["observability"]["provider_sync"] = {
            "status": sync_status,
            "status_comment_id": status_comment_id,
        }
        s["observability"]["provider_sync_required"] = False
    except Exception as exc:
        s["observability"]["provider_sync"] = {
            "status": "FAILED_OBSERVABILITY_ONLY",
            "error": str(exc),
        }
    return s


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save(obj: Any, path: Path | None) -> None:
    text = json.dumps(obj, indent=2, sort_keys=True) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init")
    init.add_argument("--responsibility", required=True)
    init.add_argument("--units", type=Path, required=True)
    init.add_argument("--plan-ref")
    init.add_argument("--protocol-ref")
    init.add_argument("--material-head")
    init.add_argument("--semantic-head")
    init.add_argument("--delta", type=int)
    init.add_argument("--github-repository")
    init.add_argument("--github-issue", type=int)
    init.add_argument(
        "--projection-mode",
        choices=sorted(PROJECTION_MODES),
        default=PROJECTION_DERIVED,
        help="DERIVED_FROM_FACTS (default): agents publish facts, E is computed. "
        "LEGACY_AGENT_ASSERTED exists only to re-open historical snapshots.",
    )
    init.add_argument("--output", type=Path)

    for name in ("implementation-start", "stream-loss"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--snapshot", type=Path, required=True)
        cmd.add_argument("--output", type=Path)

    recovery_start = sub.add_parser("recovery-start")
    recovery_start.add_argument("--snapshot", type=Path, required=True)
    recovery_start.add_argument(
        "--mode",
        choices=("FRONTIER_RECONCILIATION", "INTERRUPTED_EXECUTOR"),
        default="FRONTIER_RECONCILIATION",
    )
    recovery_start.add_argument("--output", type=Path)

    recovery = sub.add_parser("recovery-evidence")
    recovery.add_argument("--snapshot", type=Path, required=True)
    recovery.add_argument("--claim")
    recovery.add_argument("--not-proved")
    recovery.add_argument("--open-work")
    recovery.add_argument("--owner-decision")
    recovery.add_argument("--next")
    recovery.add_argument("--output", type=Path)

    unit = sub.add_parser("unit-update")
    unit.add_argument("--snapshot", type=Path, required=True)
    unit.add_argument("--unit-id", required=True)
    unit.add_argument(
        "--complete",
        choices=("YES", "NO", "UNCHANGED"),
        default="UNCHANGED",
    )
    unit.add_argument(
        "--evidenced",
        choices=("YES", "NO", "UNCHANGED"),
        default="UNCHANGED",
        help="Legacy snapshots only. DERIVED_FROM_FACTS snapshots reject it: publish --evidence-ref instead.",
    )
    unit.add_argument(
        "--evidence-ref",
        action="append",
        dest="evidence_refs",
        help="Durable evidence ref for this unit (repeatable).",
    )
    unit.add_argument(
        "--evidence-candidate",
        help="40-hex commit the evidence refs cover; E counts only while it equals the observed material head.",
    )
    unit.add_argument("--output", type=Path)

    observe = sub.add_parser("observe-frontier")
    observe.add_argument("--snapshot", type=Path, required=True)
    observe.add_argument("--repo-root", type=Path, required=True)
    observe.add_argument("--semantic-head")
    observe.add_argument("--output", type=Path)

    result = sub.add_parser("task-result")
    result.add_argument("--snapshot", type=Path, required=True)
    result.add_argument(
        "--result-scope",
        choices=("STEP", "PRODUCT", "RESPONSIBILITY"),
        required=True,
    )
    result.add_argument("--coverage", required=True)
    result.add_argument(
        "--responsibility-complete",
        choices=("YES", "NO", "UNKNOWN"),
        default="UNKNOWN",
    )
    result.add_argument("--output", type=Path)

    args = parser.parse_args(argv)

    if args.cmd == "init":
        snapshot = new_snapshot(
            args.responsibility,
            load(args.units),
            args.plan_ref,
            args.material_head,
            args.semantic_head,
            args.delta,
            args.github_repository,
            args.github_issue,
            args.protocol_ref,
            args.projection_mode,
        )
    else:
        snapshot = load(args.snapshot)
        if args.cmd in ("implementation-start", "stream-loss"):
            snapshot = event(snapshot, args.cmd)
        elif args.cmd == "recovery-start":
            snapshot = event(snapshot, args.cmd, mode=args.mode)
        elif args.cmd == "recovery-evidence":
            snapshot = event(
                snapshot,
                args.cmd,
                claim=args.claim,
                not_yet_proved=args.not_proved,
                open_work=args.open_work,
                owner_decision=args.owner_decision,
                next=args.next,
            )
        elif args.cmd == "unit-update":
            values = {"YES": True, "NO": False, "UNCHANGED": None}
            snapshot = event(
                snapshot,
                args.cmd,
                unit_id=args.unit_id,
                complete=values[args.complete],
                evidenced=values[args.evidenced],
                evidence_refs=args.evidence_refs,
                evidence_candidate=args.evidence_candidate,
            )
        elif args.cmd == "observe-frontier":
            snapshot["frontier"] = git_frontier(
                args.repo_root,
                args.semantic_head
                or snapshot["frontier"].get("semantic_evidence_head"),
            )
            snapshot = reproject(snapshot)  # E depends on the observed head
            snapshot["observability"]["provider_sync_required"] = True
            snapshot["observability"]["update_reason"] = "MATERIAL_FRONTIER_REFRESH"
        elif args.cmd == "task-result":
            result_values = {"YES": True, "NO": False, "UNKNOWN": None}
            snapshot = event(
                snapshot,
                args.cmd,
                scope=args.result_scope,
                coverage=args.coverage,
                responsibility_complete=result_values[
                    args.responsibility_complete
                ],
            )

        snapshot = sync_github(snapshot)

    save(snapshot, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())