#!/usr/bin/env python3
"""Engineering Relay V3.1 RLL-1 Codex executor.

Reuses the deterministic RLL-1 transport core from rll_worker.py while keeping
Codex confined to repository inspection/edit/test work. GitHub provider control,
evidence publication, and branch commit/push remain launcher-owned.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

CORE_PATH = Path(__file__).with_name("rll_worker.py")
SPEC = importlib.util.spec_from_file_location("rll_worker_core", CORE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"unable to load RLL core from {CORE_PATH}")
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)

AGENT_SCHEMA = "RLL_AGENT_RESULT_V1"
TRANSIENT_RE = re.compile(
    r"(resource[_ -]?exhausted|quota|rate.?limit|too many requests|429|"
    r"timed? ?out|timeout|temporar(?:y|ily)|connection reset|network unavailable)",
    re.IGNORECASE,
)


def _authorized_exec_sources(issue, comments, authorized):
    sources = []
    issue_author = (issue.get("author") or {}).get("login")
    if issue_author in authorized and core.EXEC in (issue.get("body") or ""):
        sources.append(issue["body"])
    for comment in comments:
        if (comment.get("user") or {}).get("login") in authorized and core.EXEC in (comment.get("body") or ""):
            sources.append(comment["body"])
    return sources


def _normalize_allowed_path(value: str) -> str:
    raw = value.strip().replace("\\", "/").strip("/")
    if not raw:
        raise core.RllError("allowed_paths contains an empty path")
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts:
        raise core.RllError(f"unsafe allowed path: {value}")
    return path.as_posix()


def parse_exec(issue, comments, authorized):
    envelope = core.parse_exec(issue, comments, authorized)
    sources = _authorized_exec_sources(issue, comments, authorized)
    if not sources:
        raise core.RllError("no authorized RLL_EXECUTION_V1")
    data = core.block(sources[-1], core.EXEC)
    allowed = [
        _normalize_allowed_path(item)
        for item in data.get("allowed_paths", "").split(";")
        if item.strip()
    ]
    if envelope["mode"] == "BRANCH_RESUME" and not allowed:
        raise core.RllError(
            "Codex BRANCH_RESUME requires semicolon-delimited allowed_paths in RLL_EXECUTION_V1"
        )
    envelope["allowed_paths"] = allowed
    envelope["commit_message"] = data.get("commit_message", "").strip()
    return envelope


def path_allowed(path: str, allowed_paths: list[str]) -> bool:
    normalized = path.replace("\\", "/").strip("/")
    return any(
        normalized == allowed or normalized.startswith(allowed.rstrip("/") + "/")
        for allowed in allowed_paths
    )


def changed_paths(root: Path) -> list[str]:
    output = core.git(root, "status", "--porcelain=v1", "--untracked-files=all")
    rows = []
    for line in output.splitlines():
        if len(line) < 4:
            continue
        payload = line[3:]
        if " -> " in payload:
            payload = payload.split(" -> ", 1)[1]
        payload = payload.strip().strip('"').replace("\\", "/")
        if payload:
            rows.append(payload)
    return sorted(set(rows))


def assert_changed_paths_allowed(root: Path, allowed_paths: list[str]) -> list[str]:
    rows = changed_paths(root)
    disallowed = [path for path in rows if not path_allowed(path, allowed_paths)]
    if disallowed:
        raise core.RllError(
            "Codex changed paths outside the authorized envelope: " + ", ".join(disallowed)
        )
    return rows


def parse_duration_seconds(value: str) -> int:
    match = re.fullmatch(r"\s*(\d+)\s*([smh]?)\s*", value, re.IGNORECASE)
    if not match:
        raise core.RllError(f"invalid Codex timeout: {value}")
    amount = int(match.group(1))
    unit = match.group(2).lower() or "s"
    multiplier = {"s": 1, "m": 60, "h": 3600}[unit]
    return amount * multiplier


def issue_context(issue, comments, limit: int = 60000) -> str:
    parts = [f"ISSUE #{issue['number']}: {issue.get('title', '')}", issue.get("body") or ""]
    for comment in comments:
        body = comment.get("body") or ""
        if body.lstrip().startswith(core.STATE):
            continue
        login = (comment.get("user") or {}).get("login") or "unknown"
        parts.append(f"\n--- comment by {login} ---\n{body}")
    text = "\n".join(parts)
    if len(text) <= limit:
        return text
    return "[earlier issue context truncated]\n" + text[-limit:]


def codex_prompt(repo, issue, comments, envelope, directive_notes):
    directives = "\n".join("- " + note for note in directive_notes) or "- none"
    allowed = "\n".join("- " + path for path in envelope.get("allowed_paths", [])) or "- none"
    mode_instruction = (
        "You may edit tracked/untracked files only under the authorized paths below. "
        "Do not commit, push, rebase, merge, or change Git refs; the deterministic launcher owns .git/provider mutations."
        if envelope["mode"] == "BRANCH_RESUME"
        else
        "This is immutable exact-head evidence. Do not create, modify, or delete repository files."
    )
    return f"""You are the Engineering Relay V3.1 RLL-1 Codex local engineering worker.

Repository: {repo}
Mode: {envelope['mode']}
Base SHA: {envelope['base_sha']}
Branch: {envelope.get('branch')}
Exact head: {envelope.get('head_sha')}
Material writes authorized: {envelope['write']}

RLL is transport only. The issue/programme/approved plan and material Git truth govern engineering.
The launcher already fetched GitHub context for you. Do not invoke gh, GitHub APIs, MCP, network research,
or any provider-control command. Do not inspect or alter GitHub credentials. Do not merge, release, delete
branches, close programme work, weaken tests/oracles/tolerances, or infer Owner authority.

{mode_instruction}

Authorized paths for BRANCH_RESUME:
{allowed}

Launcher-filtered directives:
{directives}

Complete the bounded task as far as the durable issue contract permits. Run the required local validation.
Keep PASS/FAIL/BLOCKED/NOT_RUN truthful. If a protected-surface change is required, stop and return
ESCALATION_REQUIRED instead of broadening scope.

Return RLL_AGENT_RESULT_V1 matching the supplied schema. evidence_body must contain the complete durable
engineering evidence that the launcher should publish to the governing issue. Do not claim a commit SHA
or evidence URL; the launcher adds exact postflight Git/provider truth after your run.

DURABLE ISSUE CONTEXT
=====================
{issue_context(issue, comments)}
"""


def _codex_argv(prompt: str, schema: Path, output: Path, sandbox: str) -> list[str]:
    return [
        "codex",
        "exec",
        "--ephemeral",
        "--json",
        "--sandbox",
        sandbox,
        "-c",
        'approval_policy="never"',
        "-c",
        'approvals_reviewer="user"',
        "-c",
        'web_search="disabled"',
        "-c",
        "sandbox_workspace_write.network_access=false",
        "--output-schema",
        str(schema),
        "-o",
        str(output),
        prompt,
    ]


def codex(
    root: Path,
    prompt: str,
    schema: Path,
    timeout: str,
    sandbox: str,
    *,
    codex_home: str | None,
    codex_user: str | None,
):
    if sandbox == "workspace-write" and sys.platform.startswith("win"):
        raise core.RllError(
            "CODEX_NATIVE_WINDOWS_WRITE_NOT_QUALIFIED: run BRANCH_RESUME through WSL2/Linux"
        )
    env = os.environ.copy()
    for key in (
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "GITHUB_ENTERPRISE_TOKEN",
        "GH_ENTERPRISE_TOKEN",
    ):
        env.pop(key, None)

    timeout_seconds = parse_duration_seconds(timeout)
    with tempfile.TemporaryDirectory(prefix="rll-codex-result-") as tmp:
        if codex_user:
            os.chmod(tmp, 0o777)
        final_path = Path(tmp) / "final.json"
        argv = _codex_argv(prompt, schema, final_path, sandbox)

        if codex_user:
            home = codex_home or f"/home/{codex_user}/.codex-rll"
            prefixed = [
                "sudo",
                "-n",
                "-u",
                codex_user,
                "env",
                f"CODEX_HOME={home}",
                f"HOME=/home/{codex_user}",
                f"PATH={env.get('PATH', '')}",
            ]
            argv = prefixed + argv
        elif codex_home:
            env["CODEX_HOME"] = codex_home

        try:
            result = subprocess.run(
                argv,
                cwd=root,
                text=True,
                capture_output=True,
                env=env,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            raise core.RllError(f"Codex invocation timeout after {timeout}") from exc

        events = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise core.RllError("Codex --json emitted invalid JSONL") from exc

        diagnostics = "\n".join(part for part in (result.stderr, result.stdout) if part)
        if result.returncode != 0:
            prefix = "transient " if TRANSIENT_RE.search(diagnostics) else ""
            raise core.RllError(
                f"Codex {prefix}invocation failed with exit {result.returncode}: "
                + diagnostics[-4000:]
            )
        if TRANSIENT_RE.search(diagnostics) and not final_path.is_file():
            raise core.RllError("Codex transient provider condition prevented structured output")
        if not final_path.is_file():
            raise core.RllError("Codex exited without structured -o result")

        try:
            value = json.loads(final_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise core.RllError("invalid Codex structured result") from exc

        if not isinstance(value, dict):
            raise core.RllError("Codex structured result is not an object")
        if value.get("schema") != AGENT_SCHEMA:
            raise core.RllError("Codex structured result has wrong schema")
        if value.get("transport_state") not in {
            "ACTIVE",
            "RETRY_WAIT",
            "ESCALATION_REQUIRED",
            "REVIEW_READY",
        }:
            raise core.RllError("Codex structured result has invalid transport_state")
        if value["transport_state"] == "REVIEW_READY" and not str(value.get("evidence_body", "")).strip():
            raise core.RllError("Codex REVIEW_READY omitted durable evidence_body")
        value["_event_count"] = len(events)
        return value


def publish_evidence(repo: str, issue_number: int, value: dict, footer: str) -> str | None:
    body = str(value.get("evidence_body", "")).strip()
    if not body:
        return None
    if not body.startswith("TASK_EVIDENCE"):
        body = "TASK_EVIDENCE — Codex RLL execution\n\n" + body
    body = body + "\n\n---\n\n" + footer.strip() + "\n"
    row = core.ghj(
        "api",
        f"repos/{repo}/issues/{issue_number}/comments",
        "--method",
        "POST",
        "--field",
        f"body={body}",
    )
    url = row.get("html_url")
    if url:
        return url
    comment_id = row.get("id")
    if comment_id:
        return f"https://github.com/{repo}/issues/{issue_number}#issuecomment-{comment_id}"
    return None


def commit_and_push(root: Path, issue_number: int, issue_title: str, envelope: dict, pre_remote: str):
    paths = assert_changed_paths_allowed(root, envelope["allowed_paths"])
    if paths:
        check = subprocess.run(
            ["git", "-C", str(root), "diff", "--check"],
            text=True,
            capture_output=True,
        )
        if check.returncode:
            raise core.RllError("git diff --check failed before launcher commit: " + check.stdout + check.stderr)
        core.git(root, "add", "-A")
        staged = subprocess.run(
            ["git", "-C", str(root), "diff", "--cached", "--quiet"],
            text=True,
            capture_output=True,
        )
        if staged.returncode not in (0, 1):
            raise core.RllError("unable to inspect staged Codex changes")
        if staged.returncode == 1:
            message = envelope.get("commit_message") or f"RLL #{issue_number}: {issue_title}"
            core.git(root, "commit", "-m", message)

    core.git(root, "fetch", "origin")
    remote_now = core.git(root, "rev-parse", "origin/" + envelope["branch"])
    if remote_now != pre_remote:
        raise core.RllError(
            "origin branch advanced during Codex execution; refusing launcher-owned push"
        )
    local_head = core.git(root, "rev-parse", "HEAD")
    if local_head != remote_now:
        push = subprocess.run(
            ["git", "-C", str(root), "push", "origin", f"HEAD:{envelope['branch']}"],
            text=True,
            capture_output=True,
        )
        if push.returncode:
            raise core.RllError("launcher-owned push failed: " + push.stderr.strip())
    return paths, core.git(root, "rev-parse", "HEAD")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Engineering Relay V3.1 RLL-1 Codex worker.")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--repository", required=True)
    p.add_argument("--worker-id", default="codex-local")
    p.add_argument("--authorized-login", action="append", required=True)
    p.add_argument("--data-dir", default=os.environ.get("RLL_DATA_DIR", str(Path.home() / ".rll")))
    p.add_argument("--lease-minutes", type=int, default=90)
    p.add_argument("--timeout", default="2h")
    p.add_argument("--codex-home")
    p.add_argument("--codex-user")
    p.add_argument("--smoke", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    root = Path(args.repo_root).resolve()
    try:
        for command in ("git", "gh", "codex"):
            if not shutil.which(command):
                raise core.RllError(f"missing command {command}")
        if args.codex_user and not shutil.which("sudo"):
            raise core.RllError("codex-user isolation requires sudo")
        if core.cmd(["gh", "auth", "status"], check=False).returncode:
            raise core.RllError("gh authentication unavailable")
        if not core.git(root, "rev-parse", "--git-dir", check=False):
            raise core.RllError("repo-root is not a Git repository")

        data_dir = Path(args.data_dir).expanduser() / re.sub(
            r"[^A-Za-z0-9_.-]+", "-", args.repository
        )
        lock = data_dir / "worker.lock"

        with core.Mutex(lock):
            row = core.choose(
                core.issue_rows(args.repository, core.ACTIVE),
                core.issue_rows(args.repository, core.READY),
            )
            if not row:
                print(json.dumps({"status": "IDLE"}))
                return 0

            number = int(row["number"])
            issue = core.issue_view(args.repository, number)
            comments = core.comments(args.repository, number)
            authorized = set(args.authorized_login)
            envelope = parse_exec(issue, comments, authorized)
            if envelope["repository"] != args.repository or envelope["worker"] != args.worker_id:
                raise core.RllError("execution identity mismatch")

            core.validate_basis(root, envelope)
            workspace = core.prepare_workspace(root, envelope, data_dir, number)
            observation = core.observe(workspace)
            state_row = core.state_comment(comments)
            state = (
                core.parse_state(state_row["body"])
                if state_row
                else {
                    "worker": args.worker_id,
                    "issue": number,
                    "state": "READY",
                    "phase": "CLAIM",
                    "mode": envelope["mode"],
                    "branch": envelope.get("branch"),
                    "base_sha": envelope["base_sha"],
                    "material_head": observation["head"],
                    "lease_epoch": 0,
                    "lease_until": None,
                    "last_directive_sequence": 0,
                    "current": "eligible issue discovered",
                    "next": "claim lease",
                }
            )

            if envelope["mode"] == "BRANCH_RESUME" and not observation["clean"]:
                assert_changed_paths_allowed(workspace, envelope["allowed_paths"])
                if state["state"] not in {"ACTIVE", "RETRY_WAIT"}:
                    raise core.RllError(
                        "governed branch is dirty before Codex claim without resumable worker state"
                    )

            directive_rows = core.directives(
                comments, number, authorized, state["last_directive_sequence"]
            )
            invoke, directive_notes = core.apply_dirs(state, directive_rows)
            common, two_pass = core.protocol_basis()
            labels = core.labelset(issue)

            if state["state"] == "CANCELLED" or not invoke:
                core.state_write(
                    args.repository,
                    number,
                    state_row,
                    core.render(state, common, two_pass),
                )
                core.label_state(args.repository, number, labels, state["state"])
                print(json.dumps({"status": state["state"], "issue": number}))
                return 0

            core.lease(state, args.lease_minutes)
            state["material_head"] = observation["head"]
            state_id = core.state_write(
                args.repository,
                number,
                state_row,
                core.render(state, common, two_pass),
            )
            core.label_state(args.repository, number, labels, "ACTIVE")

            if args.smoke:
                state.update(
                    state="RETRY_WAIT",
                    phase="SMOKE_COMPLETE",
                    lease_until=None,
                    current="non-destructive Codex RLL smoke complete",
                    next="review before enabling Codex agent",
                )
                core.state_write(
                    args.repository,
                    number,
                    {"id": state_id},
                    core.render(state, common, two_pass),
                )
                print(json.dumps({"status": "SMOKE_COMPLETE", "issue": number}))
                return 0

            pre_head = observation["head"]
            pre_remote = (
                core.git(workspace, "rev-parse", "origin/" + envelope["branch"])
                if envelope["mode"] == "BRANCH_RESUME"
                else None
            )
            sandbox = "workspace-write" if envelope["mode"] == "BRANCH_RESUME" else "read-only"
            schema = Path(__file__).resolve().parents[1] / "schemas" / "rll-agent-result.schema.json"

            try:
                value = codex(
                    workspace,
                    codex_prompt(args.repository, issue, comments, envelope, directive_notes),
                    schema,
                    args.timeout,
                    sandbox,
                    codex_home=args.codex_home,
                    codex_user=args.codex_user,
                )
            except core.RllError as exc:
                state.update(
                    state="RETRY_WAIT",
                    phase="CODEX_INVOCATION",
                    lease_until=None,
                    current=str(exc),
                    next="retry after environment/provider recovery",
                )
                core.state_write(
                    args.repository,
                    number,
                    {"id": state_id},
                    core.render(state, common, two_pass),
                )
                print(json.dumps({"status": "RETRY_WAIT", "issue": number}))
                return 0

            after_agent = core.observe(workspace)
            if envelope["mode"] == "EXACT_HEAD_EVIDENCE":
                if after_agent["head"] != envelope["head_sha"] or not after_agent["clean"]:
                    state.update(
                        state="ESCALATION_REQUIRED",
                        phase="EXACT_HEAD_MUTATION",
                        lease_until=None,
                        current="Codex exact-head run changed immutable Git material",
                        next="discard diagnostic worktree and investigate sandbox failure",
                    )
                    core.state_write(
                        args.repository,
                        number,
                        {"id": state_id},
                        core.render(state, common, two_pass),
                    )
                    core.label_state(
                        args.repository,
                        number,
                        core.labelset(core.issue_view(args.repository, number)),
                        state["state"],
                    )
                    print(json.dumps({"status": state["state"], "issue": number}))
                    return 0
            else:
                if after_agent["head"] != pre_head:
                    state.update(
                        state="ESCALATION_REQUIRED",
                        phase="CODEX_GIT_AUTHORITY_VIOLATION",
                        lease_until=None,
                        current="Codex changed Git HEAD; launcher-owned commit boundary violated",
                        next="inspect branch and restore provider/Git authority boundary",
                    )
                    core.state_write(
                        args.repository,
                        number,
                        {"id": state_id},
                        core.render(state, common, two_pass),
                    )
                    core.label_state(
                        args.repository,
                        number,
                        core.labelset(core.issue_view(args.repository, number)),
                        state["state"],
                    )
                    print(json.dumps({"status": state["state"], "issue": number}))
                    return 0
                try:
                    assert_changed_paths_allowed(workspace, envelope["allowed_paths"])
                except core.RllError as exc:
                    state.update(
                        state="ESCALATION_REQUIRED",
                        phase="PATH_CONFINEMENT",
                        lease_until=None,
                        current=str(exc),
                        next="review unauthorized workspace changes",
                    )
                    core.state_write(
                        args.repository,
                        number,
                        {"id": state_id},
                        core.render(state, common, two_pass),
                    )
                    core.label_state(
                        args.repository,
                        number,
                        core.labelset(core.issue_view(args.repository, number)),
                        state["state"],
                    )
                    print(json.dumps({"status": state["state"], "issue": number}))
                    return 0

            evidence_url = None
            changed = changed_paths(workspace)

            if value["transport_state"] == "REVIEW_READY" and envelope["mode"] == "BRANCH_RESUME":
                try:
                    changed, _ = commit_and_push(
                        workspace,
                        number,
                        issue.get("title", "bounded task"),
                        envelope,
                        pre_remote,
                    )
                except core.RllError as exc:
                    state.update(
                        state="ESCALATION_REQUIRED",
                        phase="LAUNCHER_COMMIT_PUSH",
                        lease_until=None,
                        current=str(exc),
                        next="review branch/provider reconciliation",
                    )
                    core.state_write(
                        args.repository,
                        number,
                        {"id": state_id},
                        core.render(state, common, two_pass),
                    )
                    core.label_state(
                        args.repository,
                        number,
                        core.labelset(core.issue_view(args.repository, number)),
                        state["state"],
                    )
                    print(json.dumps({"status": state["state"], "issue": number}))
                    return 0

            final_obs = core.observe(workspace)
            if value["transport_state"] == "REVIEW_READY":
                footer = "\n".join(
                    [
                        "RLL_CODEX_POSTFLIGHT_V1",
                        f"worker: {args.worker_id}",
                        f"mode: {envelope['mode']}",
                        f"material_before: {pre_head}",
                        f"material_after: {final_obs['head']}",
                        "changed_paths: " + ("; ".join(changed) if changed else "none"),
                        f"tree_clean: {str(final_obs['clean']).lower()}",
                        f"codex_jsonl_events: {value.get('_event_count', 0)}",
                        "provider_mutations_by_agent: false",
                    ]
                )
                evidence_url = publish_evidence(args.repository, number, value, footer)

            canonical = {
                "schema": "RLL_RUN_RESULT_V1",
                "transport_state": value["transport_state"],
                "current": str(value.get("current", "")),
                "next": str(value.get("next", "")),
                "evidence_comment_url": evidence_url,
                "engineering_summary": str(value.get("engineering_summary", "")),
                "notes": [str(x) for x in value.get("notes", [])],
            }
            core.apply_result(state, canonical, final_obs, envelope)
            core.state_write(
                args.repository,
                number,
                {"id": state_id},
                core.render(state, common, two_pass),
            )
            core.label_state(
                args.repository,
                number,
                core.labelset(core.issue_view(args.repository, number)),
                state["state"],
            )
            print(
                json.dumps(
                    {
                        "status": state["state"],
                        "issue": number,
                        "material_head": state["material_head"],
                        "workspace": str(workspace),
                    }
                )
            )
            return 0
    except core.RllError as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
