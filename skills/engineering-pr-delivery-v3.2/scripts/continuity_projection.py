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
TITLE_RE = re.compile(r"\s+\{P\d+% · E\d+% · [^{}]+\}\s*$")

class ContinuityError(ValueError):
    pass

def pct(n: int, d: int) -> int:
    return round(100 * n / d) if d else 0

def normalize_units(units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not units:
        raise ContinuityError("at least one declared progress unit is required")
    out, seen = [], set()
    for raw in units:
        uid = str(raw.get("id") or "").strip()
        if not uid or uid in seen:
            raise ContinuityError(f"invalid/duplicate unit id: {uid!r}")
        seen.add(uid)
        complete, evidenced = bool(raw.get("complete")), bool(raw.get("evidenced"))
        if evidenced and not complete:
            raise ContinuityError(f"{uid}: evidence cannot lead completion")
        out.append({**raw, "id": uid, "complete": complete, "evidenced": evidenced})
    return out

def progress(units: list[dict[str, Any]]) -> dict[str, Any]:
    units = normalize_units(units)
    d = len(units)
    c = sum(u["complete"] for u in units)
    e = sum(u["evidenced"] for u in units)
    return {
        "denominator": d, "completed_units": c, "evidenced_units": e,
        "progress_percent": pct(c, d), "evidence_percent": pct(e, d),
        "active_unit": next((u["id"] for u in units if not u["complete"]), None),
    }

def frontier(material: str | None, semantic: str | None, delta: int | None = None) -> dict[str, Any]:
    material = (material or "").strip() or None
    semantic = (semantic or "").strip() or None
    if delta is not None and delta < 0:
        raise ContinuityError("delta cannot be negative")
    if not material: relation = "MATERIAL_UNKNOWN"
    elif not semantic: relation = "SEMANTIC_UNKNOWN"
    elif material == semantic: relation, delta = "ALIGNED", 0
    elif delta == 0: relation = "UNRESOLVED"
    else: relation = "MATERIAL_AHEAD"
    return {
        "material_head": material, "semantic_evidence_head": semantic,
        "relation": relation, "delta_commits": delta,
        "recovery_reconciliation_needed": relation in {"MATERIAL_AHEAD", "SEMANTIC_UNKNOWN", "UNRESOLVED"},
    }

def new_snapshot(responsibility: str, units: list[dict[str, Any]], plan_ref: str | None,
                 material: str | None, semantic: str | None, delta: int | None,
                 repository: str | None = None, issue: int | None = None) -> dict[str, Any]:
    units = normalize_units(units)
    return {
        "schema": SCHEMA, "authority": AUTHORITY, "responsibility": responsibility,
        "state": "PLANNING", "plan_ref": plan_ref, "units": units, "progress": progress(units),
        "frontier": frontier(material, semantic, delta), "current": None, "next": None,
        "owner_decision": "NONE",
        "recovery": {
            "stream_loss_count": 0, "recovery_evidence_required": False,
            "handover_plan_triggered_this_lifecycle": False, "plan_for_handover_now": False,
        },
        "provider": {"type": "GITHUB" if repository and issue else None, "repository": repository, "issue_number": issue},
        "observability": {
            "provider_sync_required": False, "provider_sync_failure_blocks_engineering": False,
            "update_reason": None, "provider_sync": {"status": "NOT_REQUESTED"},
        },
    }

def event(snapshot: dict[str, Any], name: str, **kwargs: Any) -> dict[str, Any]:
    s = deepcopy(snapshot)
    if name == "implementation-start":
        if not s.get("plan_ref"): raise ContinuityError("implementation start requires published plan_ref")
        if s["state"] in {"COMPLETE", "SUPERSEDED"}: raise ContinuityError("terminal responsibility")
        s["state"] = "IMPLEMENTING"
    elif name == "stream-loss":
        r = s["recovery"]; r["stream_loss_count"] += 1; r["recovery_evidence_required"] = True
        r["plan_for_handover_now"] = r["stream_loss_count"] >= 3 and not r["handover_plan_triggered_this_lifecycle"]
        if r["plan_for_handover_now"]: r["handover_plan_triggered_this_lifecycle"] = True
        s["state"] = "RECOVERING"
    elif name == "recovery-evidence":
        if not s["recovery"]["recovery_evidence_required"]: raise ContinuityError("recovery evidence not required")
        s["frontier"] = frontier(s["frontier"]["material_head"], kwargs["semantic_head"], kwargs.get("delta", 0))
        s["recovery"]["recovery_evidence_required"] = False
        s["recovery"]["plan_for_handover_now"] = False
        s["state"] = "IMPLEMENTING"
    elif name == "unit-update":
        uid = kwargs["unit_id"]; found = False
        for u in s["units"]:
            if u["id"] == uid:
                found = True
                if kwargs.get("complete") is not None: u["complete"] = kwargs["complete"]
                if kwargs.get("evidenced") is not None: u["evidenced"] = kwargs["evidenced"]
                if u["evidenced"] and not u["complete"]: raise ContinuityError(f"{uid}: evidence cannot lead completion")
        if not found: raise ContinuityError(f"unknown unit: {uid}")
        s["progress"] = progress(s["units"])
    elif name == "task-result":
        scope, complete = kwargs["scope"], kwargs["responsibility_complete"]
        if scope not in {"STEP", "PRODUCT", "RESPONSIBILITY"}: raise ContinuityError("invalid result scope")
        if complete is True and scope != "RESPONSIBILITY": raise ContinuityError("complete YES requires RESPONSIBILITY scope")
        s["result"] = {"result_scope": scope, "coverage": kwargs["coverage"], "responsibility_complete": complete}
        if complete is True: s["state"] = "COMPLETE"
    else:
        raise ContinuityError(f"unknown event: {name}")
    s["observability"]["provider_sync_required"] = True
    s["observability"]["update_reason"] = name.upper().replace("-", "_")
    return s

def git_frontier(repo: Path, semantic: str | None) -> dict[str, Any]:
    def git(*args: str, check: bool = True):
        return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=check)
    try: material = git("rev-parse", "HEAD").stdout.strip()
    except Exception as exc: raise ContinuityError(f"cannot resolve Git HEAD: {exc}") from exc
    if not semantic: return frontier(material, None)
    if git("cat-file", "-e", f"{semantic}^{{commit}}", check=False).returncode: return frontier(material, semantic)
    if semantic == material: return frontier(material, semantic, 0)
    if git("merge-base", "--is-ancestor", semantic, material, check=False).returncode == 0:
        delta = int(git("rev-list", "--count", f"{semantic}..{material}").stdout.strip())
        return frontier(material, semantic, delta)
    return {**frontier(material, semantic), "relation": "UNRESOLVED", "delta_commits": None}

def title(snapshot: dict[str, Any], existing: str) -> str:
    p, active = snapshot["progress"], snapshot["progress"]["active_unit"]
    unit = active or ("COMPLETE" if snapshot["state"] == "COMPLETE" else "NO_ACTIVE_UNIT")
    suffix = f"{{P{p['progress_percent']}% · E{p['evidence_percent']}% · {unit} · {snapshot['state']}}}"
    return f"{TITLE_RE.sub('', existing).rstrip()} {suffix}".strip()

def markdown(snapshot: dict[str, Any]) -> str:
    p, f, r = snapshot["progress"], snapshot["frontier"], snapshot["recovery"]
    done = [u["id"] for u in snapshot["units"] if u["complete"]]
    pending = [u["id"] for u in snapshot["units"] if not u["complete"]]
    lines = [
        "FURTHER_TASK_SNAPSHOT — current", "", f"AUTHORITY: {AUTHORITY}", f"STATE: {snapshot['state']}",
        f"PROGRESS: P{p['progress_percent']}% / E{p['evidence_percent']}% ({p['completed_units']}/{p['denominator']} complete; {p['evidenced_units']}/{p['denominator']} evidenced)",
        f"ACTIVE_UNIT: {p['active_unit'] or 'NONE'}", f"PLAN: {snapshot.get('plan_ref') or 'UNKNOWN'}",
        f"FRONTIER: material={f['material_head'] or 'UNKNOWN'}; semantic/evidence={f['semantic_evidence_head'] or 'UNKNOWN'}; relation={f['relation']}",
        "", "COMPLETED", *([f"- [x] {x}" for x in done] or ["- none"]), "", "ACTIVE / PENDING",
        *([f"- [ ] {x}" for x in pending] or ["- none"]), "",
        f"CURRENT: {snapshot.get('current') or 'UNSPECIFIED'}", f"NEXT: {snapshot.get('next') or 'UNSPECIFIED'}",
        f"OWNER_DECISION: {snapshot.get('owner_decision') or 'NONE'}",
        f"RECOVERY: stream_loss_count={r['stream_loss_count']}; evidence_required={str(r['recovery_evidence_required']).lower()}; handover_plan_triggered={str(r['handover_plan_triggered_this_lifecycle']).lower()}; plan_for_handover_now={str(r['plan_for_handover_now']).lower()}",
        "", "Derived continuity view only; not engineering permission or acceptance evidence.",
    ]
    return "\n".join(lines)

def marked(body: str, content: str) -> str:
    block = f"{START}\n{content.strip()}\n{END}"; body = body or ""
    a, b = body.find(START), body.find(END)
    if a >= 0 and b >= a:
        b += len(END); return body[:a].rstrip() + ("\n\n" if body[:a].strip() else "") + block + body[b:]
    return block if not body.strip() else body.rstrip() + "\n\n" + block + "\n"

def gh_json(*args: str) -> Any:
    proc = subprocess.run(["gh", "api", *args], text=True, capture_output=True)
    if proc.returncode: raise ContinuityError(proc.stderr.strip() or "gh api failed")
    return json.loads(proc.stdout) if proc.stdout.strip() else {}

def gh_patch(endpoint: str, payload: dict[str, Any]) -> Any:
    args = ["--method", "PATCH", endpoint]
    for k, v in payload.items(): args += ["-f", f"{k}={v}"]
    return gh_json(*args)

def sync_github(snapshot: dict[str, Any]) -> dict[str, Any]:
    s = deepcopy(snapshot); provider = s.get("provider") or {}
    repo, issue = provider.get("repository"), provider.get("issue_number")
    if provider.get("type") != "GITHUB" or not repo or not isinstance(issue, int):
        s["observability"]["provider_sync"] = {"status": "NOT_CONFIGURED"}; return s
    try:
        issue_obj = gh_json(f"repos/{repo}/issues/{issue}")
        comments = gh_json(f"repos/{repo}/issues/{issue}/comments", "-f", "per_page=100")
        matches = [c for c in comments if START in str(c.get("body") or "")]
        if len(matches) > 1: raise ContinuityError("multiple managed Further Task comments")
        body = marked(str(matches[0].get("body") or "") if matches else "", markdown(s))
        if matches:
            gh_patch(f"repos/{repo}/issues/comments/{int(matches[0]['id'])}", {"body": body}); cid = int(matches[0]["id"])
        else:
            created = gh_json("--method", "POST", f"repos/{repo}/issues/{issue}/comments", "-f", f"body={body}"); cid = int(created["id"])
        desired = title(s, str(issue_obj.get("title") or ""))
        if desired != str(issue_obj.get("title") or ""): gh_patch(f"repos/{repo}/issues/{issue}", {"title": desired})
        after = gh_json(f"repos/{repo}/issues/{issue}")
        s["observability"]["provider_sync"] = {"status": "SYNCED" if after.get("title") == desired else "READBACK_MISMATCH", "status_comment_id": cid}
    except Exception as exc:
        s["observability"]["provider_sync"] = {"status": "FAILED_OBSERVABILITY_ONLY", "error": str(exc)}
    return s

def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def save(obj: Any, path: Path | None) -> None:
    text = json.dumps(obj, indent=2, sort_keys=True) + "\n"
    if path: path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8")
    else: sys.stdout.write(text)

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("--responsibility", required=True); p.add_argument("--units", type=Path, required=True)
    p.add_argument("--plan-ref"); p.add_argument("--material-head"); p.add_argument("--semantic-head"); p.add_argument("--delta", type=int)
    p.add_argument("--github-repository"); p.add_argument("--github-issue", type=int); p.add_argument("--output", type=Path)
    for name in ("implementation-start", "stream-loss"):
        p = sub.add_parser(name); p.add_argument("--snapshot", type=Path, required=True); p.add_argument("--output", type=Path)
    p = sub.add_parser("recovery-evidence"); p.add_argument("--snapshot", type=Path, required=True); p.add_argument("--semantic-head", required=True); p.add_argument("--delta", type=int, default=0); p.add_argument("--output", type=Path)
    p = sub.add_parser("unit-update"); p.add_argument("--snapshot", type=Path, required=True); p.add_argument("--unit-id", required=True); p.add_argument("--complete", choices=("YES","NO","UNCHANGED"), default="UNCHANGED"); p.add_argument("--evidenced", choices=("YES","NO","UNCHANGED"), default="UNCHANGED"); p.add_argument("--output", type=Path)
    p = sub.add_parser("observe-frontier"); p.add_argument("--snapshot", type=Path, required=True); p.add_argument("--repo-root", type=Path, required=True); p.add_argument("--semantic-head"); p.add_argument("--output", type=Path)
    p = sub.add_parser("task-result"); p.add_argument("--snapshot", type=Path, required=True); p.add_argument("--result-scope", choices=("STEP","PRODUCT","RESPONSIBILITY"), required=True); p.add_argument("--coverage", required=True); p.add_argument("--responsibility-complete", choices=("YES","NO","UNKNOWN"), default="UNKNOWN"); p.add_argument("--output", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "init":
        s = new_snapshot(a.responsibility, load(a.units), a.plan_ref, a.material_head, a.semantic_head, a.delta, a.github_repository, a.github_issue)
    else:
        s = load(a.snapshot)
        if a.cmd in ("implementation-start","stream-loss"): s = event(s, a.cmd)
        elif a.cmd == "recovery-evidence": s = event(s, a.cmd, semantic_head=a.semantic_head, delta=a.delta)
        elif a.cmd == "unit-update":
            cv = {"YES":True,"NO":False,"UNCHANGED":None}; s = event(s, a.cmd, unit_id=a.unit_id, complete=cv[a.complete], evidenced=cv[a.evidenced])
        elif a.cmd == "observe-frontier":
            s["frontier"] = git_frontier(a.repo_root, a.semantic_head or s["frontier"].get("semantic_evidence_head")); s["observability"]["provider_sync_required"] = True; s["observability"]["update_reason"] = "MATERIAL_FRONTIER_REFRESH"
        elif a.cmd == "task-result":
            rv = {"YES":True,"NO":False,"UNKNOWN":None}; s = event(s, a.cmd, scope=a.result_scope, coverage=a.coverage, responsibility_complete=rv[a.responsibility_complete])
        s = sync_github(s)
    save(s, a.output); return 0

if __name__ == "__main__":
    raise SystemExit(main())
