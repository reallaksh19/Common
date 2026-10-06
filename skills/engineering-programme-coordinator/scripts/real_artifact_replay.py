#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from coordlib import load_yaml, validate as schema_validate
from production_readiness import validate_readiness


ROOT = Path(__file__).resolve().parents[2]
COORDINATOR_ROOT = Path(__file__).resolve().parents[1]
LOCAL_RUNTIME = ROOT / "Local_PR_Deliverty_v1.1" / "scripts" / "responsibility.py"
V35_RUNTIME = ROOT / "engineering-pr-delivery-v3.5" / "scripts" / "embedded_coder_v35.py"


class RealArtifactReplayError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RealArtifactReplayError(message)


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RealArtifactReplayError(f"Unable to load runtime module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LOCAL = _load_module("p1ib_local_responsibility", LOCAL_RUNTIME)
V35 = _load_module("p1ib_v35", V35_RUNTIME)


class GitHubProvider:
    def __init__(self, repository: str, token: str, api_base: str = "https://api.github.com"):
        require(bool(token), "Live provider replay requires GITHUB_TOKEN")
        self.repository = repository
        self.token = token
        self.api_base = api_base.rstrip("/")

    def get_json(self, path: str) -> Any:
        request = urllib.request.Request(
            self.api_base + path,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + self.token,
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "Common-P1-I-B-real-artifact-replay",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise RealArtifactReplayError(
                f"GitHub provider read failed for {path}: HTTP {exc.code}"
            ) from exc


def _comment_ref(repository: str, issue: int, comment_id: int) -> str:
    return f"https://github.com/{repository}/issues/{issue}#issuecomment-{comment_id}"


def _verify_comment(
    provider: Any,
    repository: str,
    name: str,
    spec: dict[str, Any],
) -> dict[str, Any]:
    value = provider.get_json(f"/repos/{repository}/issues/comments/{spec['id']}")
    require(value.get("id") == spec["id"], f"{name}: provider comment ID mismatch")
    require(value.get("user", {}).get("login") == spec["author"], f"{name}: comment author mismatch")
    require(value.get("created_at") == spec["created_at"], f"{name}: comment created_at mismatch")
    require(value.get("updated_at") == spec["updated_at"], f"{name}: comment was edited after pin")
    body = value.get("body")
    require(isinstance(body, str), f"{name}: comment body missing")
    for token in spec["required_tokens"]:
        require(token in body, f"{name}: required provider token missing: {token}")
    return {
        "name": name,
        "id": spec["id"],
        "issue": spec["issue"],
        "ref": _comment_ref(repository, spec["issue"], spec["id"]),
        "updated_at": spec["updated_at"],
        "body": body,
    }


def _verify_pr_and_commit(
    provider: Any,
    repository: str,
    source: dict[str, Any],
) -> dict[str, Any]:
    pr_number = source["pr"]
    pr = provider.get_json(f"/repos/{repository}/pulls/{pr_number}")
    require(pr.get("number") == pr_number, "Provider PR identity mismatch")
    require(pr.get("head", {}).get("ref") == source["branch"], "Provider PR branch mismatch")
    require(pr.get("merged") is True, "Retained source PR is no longer provider-observed as merged")

    commit = provider.get_json(f"/repos/{repository}/commits/{source['exact_head']}")
    require(commit.get("sha") == source["exact_head"], "Exact historical candidate commit missing")

    found = False
    page = 1
    while page <= 10:
        rows = provider.get_json(
            f"/repos/{repository}/pulls/{pr_number}/commits?per_page=100&page={page}"
        )
        require(isinstance(rows, list), "PR commit history read returned non-array")
        if any(row.get("sha") == source["exact_head"] for row in rows):
            found = True
            break
        if len(rows) < 100:
            break
        page += 1
    require(found, "Exact historical candidate is absent from retained PR commit history")
    return {
        "number": pr_number,
        "current_head_sha": pr.get("head", {}).get("sha"),
        "current_base_sha": pr.get("base", {}).get("sha"),
        "merged": True,
        "exact_head_in_history": True,
    }


def _verify_workflow_runs(
    provider: Any,
    repository: str,
    specs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in specs:
        value = provider.get_json(
            f"/repos/{repository}/actions/runs/{spec['id']}"
        )
        require(value.get("id") == spec["id"], f"Workflow run {spec['id']} identity mismatch")
        require(value.get("name") == spec["name"], f"Workflow run {spec['id']} name mismatch")
        require(value.get("head_sha") == spec["head_sha"], f"Workflow run {spec['id']} candidate mismatch")
        require(value.get("conclusion") == spec["conclusion"], f"Workflow run {spec['id']} conclusion drift")
        require(value.get("status") == "completed", f"Workflow run {spec['id']} is not complete")
        rows.append({
            "id": spec["id"],
            "name": spec["name"],
            "head_sha": spec["head_sha"],
            "conclusion": spec["conclusion"],
        })
    return rows


def _local_observation(manifest: dict[str, Any]) -> dict[str, Any]:
    source = manifest["source"]
    parent = {
        "task_id": source["parent_task_id"],
        "kind": "PARENT",
        "issue": source["parent_issue"],
        "control_plane": {
            "bootstrap_state": "ESTABLISHED",
            "current_acceptance_epoch_id": source["acceptance_epoch_id"],
            "responsibility_registry": [{
                "task_id": source["responsibility_task_id"],
                "release_state": source["release_state"],
                "acceptance_profile_ref": source["acceptance_profile_ref"],
                "acceptance_profile_digest": source["acceptance_profile_digest"],
            }],
        },
    }
    task = {
        "task_id": source["responsibility_task_id"],
        "kind": "RESPONSIBILITY",
        "issue": source["child_issue"],
        "parent_issue": source["parent_issue"],
        "pr": source["pr"],
        "representation": {
            "kind": "SINGLE_ISSUE",
            "primary_issue": source["child_issue"],
            "member_issues": [source["child_issue"]],
            "predecessor_attempt_refs": [],
            "delivery_pr_history": [source["pr"]],
        },
        "acceptance_epoch_id": source["acceptance_epoch_id"],
        "acceptance_profile_ref": source["acceptance_profile_ref"],
        "acceptance_profile_digest": source["acceptance_profile_digest"],
    }
    LOCAL.validate_material_candidate(task)
    observation = LOCAL.responsibility_observation(parent, task)
    require(observation["release_state"] == source["release_state"], "Local release-state replay mismatch")
    require(observation["local_responsibility_complete"] is False, "Historical slice cannot become Local complete")
    return observation


def _v35_projection(
    manifest: dict[str, Any],
    comment_refs: list[str],
) -> dict[str, Any]:
    source = manifest["source"]
    protocols = manifest["protocol_identity"]
    context = V35.build_context(
        local_parent_task_id=source["parent_task_id"],
        local_responsibility_task_id=source["responsibility_task_id"],
        local_protocol_ref=protocols["local"]["ref"],
        local_protocol_digest=protocols["local"]["release_start_digest"],
        relay_protocol_ref=protocols["v35"]["ref"],
        relay_protocol_digest=protocols["v35"]["release_start_digest"],
        acceptance_epoch_ref=source["acceptance_epoch_id"],
        acceptance_profile_ref=source["acceptance_profile_ref"],
        acceptance_profile_digest=source["acceptance_profile_digest"],
    )
    result = V35.build_task_result(
        context,
        engineering_responsibility_complete=False,
        coverage="Retained historical SU-3 slice; nested Coder had not reached TASK_RESULT.",
        evidence_refs=comment_refs,
    )
    validated = V35.validate_task_result(context, result)
    require(
        validated["engineering_responsibility"] == source["nested_engineering_responsibility"],
        "Historical nested engineering identity mismatch",
    )
    return {
        "context_valid": True,
        "task_result_valid": True,
        "engineering_responsibility": validated["engineering_responsibility"],
        "engineering_responsibility_complete": validated["engineering_responsibility_complete"],
        "local_responsibility_complete": validated["local_responsibility_complete"],
    }


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
    )
    if proc.returncode:
        raise RealArtifactReplayError(proc.stderr.strip() or "git command failed")
    return proc.stdout.strip()


def _tree_digest(root: Path, candidate_sha: str, path: str) -> str:
    tree = _git(root, "rev-parse", f"{candidate_sha}:{path}")
    return hashlib.sha256(("git-tree-sha1:" + tree).encode("utf-8")).hexdigest()


def _current_readiness(
    *,
    repository: str,
    repo_root: Path,
    candidate_sha: str,
    source_refs: list[str],
) -> dict[str, Any]:
    local_ref = f"{repository}@{candidate_sha}:skills/Local_PR_Deliverty_v1.1"
    v35_ref = f"{repository}@{candidate_sha}:skills/engineering-pr-delivery-v3.5"
    reviewer_ref = f"{repository}@{candidate_sha}:skills/common-reviewer-protocol-v1.0"
    verified = lambda refs: {"state": "VERIFIED", "evidence_refs": list(refs), "note": None}
    conditional = lambda refs, note: {
        "state": "CONDITIONALLY_QUALIFIED",
        "evidence_refs": list(refs),
        "note": note,
    }
    not_implemented = lambda note: {
        "state": "NOT_IMPLEMENTED",
        "evidence_refs": [],
        "note": note,
    }
    replay_ref = "artifact://P1-I-B/real-provider-replay"
    prior_ref = "https://github.com/reallaksh19/Common/pull/555"
    value = {
        "schema_version": "PRODUCTION_READINESS_V1",
        "authority": "PRODUCTION_READINESS_PROJECTION",
        "target": {
            "local_runtime": "Local_PR_Deliverty_v1.1",
            "coder_runtime": "engineering-pr-delivery-v3.5",
            "coordinator": "engineering-programme-coordinator",
            "common_reviewer": "common-reviewer-protocol-v1.0",
        },
        "exact_basis": {
            "target_ref": "HEAD",
            "target_sha": candidate_sha,
            "local_protocol_ref": local_ref,
            "local_protocol_digest": _tree_digest(repo_root, candidate_sha, "skills/Local_PR_Deliverty_v1.1"),
            "v35_protocol_ref": v35_ref,
            "v35_protocol_digest": _tree_digest(repo_root, candidate_sha, "skills/engineering-pr-delivery-v3.5"),
            "common_reviewer_ref": reviewer_ref,
            "common_reviewer_digest": _tree_digest(repo_root, candidate_sha, "skills/common-reviewer-protocol-v1.0"),
        },
        "components": {
            "canonical_local_projection": verified([source_refs[0], replay_ref + "#local"]),
            "active_authority_resolution": verified([prior_ref + "#P1-R4", replay_ref]),
            "activation_state_derivation": verified([prior_ref + "#P1-R2", replay_ref]),
            "role_succession_semantics": conditional(
                [replay_ref],
                "Retained slice proves real role/authority records but is not a fresh Local adjacent-role transition qualification.",
            ),
            "acceptance_denominator_closure": not_implemented("Later programme responsibility."),
            "reviewer_definition": verified([reviewer_ref]),
            "real_artifact_horizontal_integration": verified(source_refs + [replay_ref]),
            "exact_candidate_verification": verified([source_refs[-2], source_refs[-1], replay_ref]),
            "provider_idempotency": verified([prior_ref + "#P1-R3A"]),
            "execution_kernel": verified([prior_ref + "#P1-R2"]),
            "proof_obligation_runtime": not_implemented("Phase 2 responsibility."),
            "evidence_gate": not_implemented("Phase 3 responsibility."),
            "shadow_rollout": not_implemented("Phase 4 responsibility."),
            "rollback": not_implemented("Phase 4 responsibility."),
        },
        "production_mode": "OFF",
        "cutover_authorization": {
            "authorized": False,
            "authorized_mode": None,
            "authority_ref": None,
            "authorized_at": None,
        },
        "cutover_blockers": [{
            "id": "LATER-PHASES-UNQUALIFIED",
            "severity": "HARD",
            "state": "OPEN",
            "reason": "Proof-obligation, evidence-gate, shadow and rollback phases remain unqualified.",
            "evidence_refs": [replay_ref],
        }],
        "non_blocking_residuals": [],
        "deferred_research": [],
    }
    errors = validate_readiness(value, "p1-i-b-production-readiness")
    require(not errors, "; ".join(errors))
    return value


def semantic_errors(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if value["artifact_class"] != "RETAINED_REAL_PROVIDER_ATTESTED":
        errors.append("real replay must be provider-attested")
    if value["production_readiness"]["components"]["real_artifact_horizontal_integration"]["state"] != "VERIFIED":
        errors.append("real artifact horizontal integration must be VERIFIED")
    if any(row["id"] == "P1I-REAL-ARTIFACT-MISSING" for row in value["production_readiness"]["cutover_blockers"]):
        errors.append("real-artifact-missing blocker must be absent after live attestation")
    expected_failures = {
        "Local PR Delivery v1.1",
        "Local PR Delivery v1.1 integration",
    }
    observed_failures = {
        row["name"]
        for row in value["provider_attestation_detail"]["workflow_runs"]
        if row["conclusion"] == "failure"
    } if "provider_attestation_detail" in value else expected_failures
    if observed_failures != expected_failures:
        errors.append("historical hosted failures were not preserved exactly")
    if any(value["authority_boundaries"].values()):
        errors.append("real-artifact replay cannot grant lifecycle/merge/cutover authority")
    return errors


def run_real_artifact_replay(
    manifest: dict[str, Any],
    provider: Any,
    *,
    repo_root: Path,
    candidate_sha: str,
) -> dict[str, Any]:
    require(
        manifest.get("schema_version") == "P1_I_B_REAL_ARTIFACT_MANIFEST_V1",
        "Wrong real-artifact manifest schema",
    )
    repository = manifest["repository"]
    source = manifest["source"]

    verified_comments = [
        _verify_comment(provider, repository, name, spec)
        for name, spec in manifest["comments"].items()
    ]
    comment_refs = [row["ref"] for row in verified_comments]

    pr_state = _verify_pr_and_commit(provider, repository, source)
    runs = _verify_workflow_runs(provider, repository, manifest["workflow_runs"])

    # Cross-record material identity is ref + Git tree SHA. Historical digest namespaces
    # are intentionally distinct and are both pinned by the provider-token checks above.
    local_observation = _local_observation(manifest)
    v35 = _v35_projection(manifest, comment_refs)

    super_body = next(row["body"] for row in verified_comments if row["name"] == "super_review")
    certification_body = next(row["body"] for row in verified_comments if row["name"] == "certification")
    require(source["exact_head"] in super_body and source["exact_head"] in certification_body, "Super-review exact-head binding drift")
    require("PASS_258_OF_258" in super_body and "PASS_37_OF_37" in super_body, "Super-review runtime evidence incomplete")
    require("CERTIFIED_AT_EXACT_HEAD_WITH_EXPLICIT_RESIDUALS" in certification_body, "Superseding certification state missing")

    readiness = _current_readiness(
        repository=repository,
        repo_root=repo_root,
        candidate_sha=candidate_sha,
        source_refs=comment_refs,
    )

    result = {
        "schema_version": "REAL_ARTIFACT_REPLAY_V1",
        "authority": "REAL_PROVIDER_REPLAY_PROJECTION",
        "artifact_class": "RETAINED_REAL_PROVIDER_ATTESTED",
        "artifact_id": manifest["artifact_id"],
        "provider_attestation": {
            "live_verified": True,
            "repository": repository,
            "comments_verified": len(verified_comments),
            "exact_commit_verified": True,
            "pr_history_verified": pr_state["exact_head_in_history"],
            "workflow_runs_verified": len(runs),
        },
        "historical_identity": {
            key: source[key]
            for key in [
                "parent_issue",
                "child_issue",
                "pr",
                "responsibility_task_id",
                "nested_engineering_responsibility",
                "target_sha",
                "exact_head",
                "acceptance_epoch_id",
                "acceptance_profile_ref",
                "acceptance_profile_digest",
            ]
        },
        "local_observation": local_observation,
        "v35": v35,
        "coordinator_super_review": {
            "role": "OWNER_DESIGNATED_COORDINATOR_SUPER_REVIEWER",
            "exact_head": source["exact_head"],
            "base_sha": source["target_sha"],
            "local_suite": "PASS_258_OF_258",
            "coordinator_suite": "PASS_37_OF_37",
            "authority_change": "NONE",
            "merge_authority": "NOT_GRANTED",
        },
        "historical_residuals": list(manifest["historical_residuals"]),
        "production_readiness": readiness,
        "assertions": {
            "provider_truth_live": True,
            "historical_failures_preserved": (
                {row["name"]: row["conclusion"] for row in runs}[
                    "Local PR Delivery v1.1"
                ] == "failure"
                and {row["name"]: row["conclusion"] for row in runs}[
                    "Local PR Delivery v1.1 integration"
                ] == "failure"
            ),
            "exact_candidate_bound": all(row["head_sha"] == source["exact_head"] for row in runs),
            "digest_namespaces_preserved": (
                manifest["protocol_identity"]["local"]["release_start_digest"]
                != manifest["protocol_identity"]["local"]["precode_benchmark_digest"]
                and manifest["protocol_identity"]["v35"]["release_start_digest"]
                != manifest["protocol_identity"]["v35"]["precode_benchmark_digest"]
            ),
            "real_artifact_horizontal_integration": "VERIFIED",
            "production_mode": readiness["production_mode"],
        },
        "authority_boundaries": {
            "performs_local_stage_transition": False,
            "performs_provider_mutation": False,
            "emits_engineering_pass": False,
            "grants_merge_authority": False,
            "grants_production_cutover": False,
        },
    }

    # Detailed provider rows are intentionally not part of the durable schema/output;
    # semantic preservation is asserted above and pinned by the manifest/provider reads.
    schema_errors = schema_validate("real-artifact-replay", result, "real-artifact-replay")
    require(not schema_errors, "; ".join(schema_errors))
    if not result["assertions"]["historical_failures_preserved"]:
        raise RealArtifactReplayError("Historical hosted failures were not preserved")
    if not result["assertions"]["exact_candidate_bound"]:
        raise RealArtifactReplayError("Historical workflow evidence is not bound to exact candidate")
    if not result["assertions"]["digest_namespaces_preserved"]:
        raise RealArtifactReplayError("Historical digest namespaces were collapsed")
    if any(result["authority_boundaries"].values()):
        raise RealArtifactReplayError("Replay crossed an authority boundary")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay retained real GitHub provider artifacts for P1-I-B.")
    parser.add_argument("manifest")
    parser.add_argument("--candidate-sha")
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--api-base", default="https://api.github.com")
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    args = parser.parse_args()

    manifest = load_yaml(Path(args.manifest))
    repo_root = Path(args.repository_root).resolve()
    candidate_sha = args.candidate_sha or _git(repo_root, "rev-parse", "HEAD")
    require(len(candidate_sha) == 40, "Candidate SHA must be exact 40-hex")
    provider = GitHubProvider(
        manifest["repository"],
        os.environ.get(args.token_env, ""),
        args.api_base,
    )
    result = run_real_artifact_replay(
        manifest,
        provider,
        repo_root=repo_root,
        candidate_sha=candidate_sha,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
