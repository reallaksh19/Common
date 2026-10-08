"""Pure integration golden oracle for a V3.5 responsibility snapshot.

R1-B/C only: a *testable consumer contract*, not a second status authority,
new custody/lease store, or GitHub title/PR writer. The eventual runtime must
supply this snapshot from governed DELP + Owner/Local/provider observations.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class GoldenContractError(ValueError):
    pass


def _required(record: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    result = record.get(name)
    if not isinstance(result, Mapping):
        raise GoldenContractError(f"{name}: missing structured basis")
    return result


def _issue_url(repo: str, number: int) -> str:
    return f"https://github.com/{repo}/issues/{number}"


def derive(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Derive issue, draft PR, handover, agent and reviewer *views* once.

    Input is an explicit fixture or future authoritative snapshot. It MUST NOT
    be mistaken for independently authenticated live provider/Owner data.
    No percentages, custody permissions, Local stages or reviewer decisions
    are inferred from CI, health, or an agent-authored title.
    """
    if not isinstance(snapshot, Mapping) or snapshot.get("schema_version") != "v3.5-integration-golden-v1":
        raise GoldenContractError("unsupported integration golden schema")
    owner = _required(snapshot, "owner_origin")
    programme = _required(snapshot, "programme")
    leaf = _required(snapshot, "responsibility")
    pr = _required(snapshot, "candidate_pr")
    health = _required(snapshot, "agent_observation")
    review = _required(snapshot, "review_observation")

    repo = programme.get("repository")
    pn = programme.get("issue")
    ln = leaf.get("issue")
    prn = pr.get("number")
    if repo != "reallaksh19/Common" or not all(
        type(n) is int and n > 0 for n in (pn, ln, prn)
    ):
        raise GoldenContractError("unrecognised programme or issue identity")
    if leaf.get("parent_issue") != pn or pr.get("responsibility_issue") != ln:
        raise GoldenContractError("parent/leaf/PR lineage mismatch")
    if (
        programme.get("selected_issue") != ln
        or leaf.get("responsibility_id") != "RK-P3"
        or programme.get("roadmap_ref") != _issue_url(repo, pn)
    ):
        raise GoldenContractError("selected responsibility/roadmap basis mismatch")
    if (
        owner.get("original_source_status") != "UNRESOLVED_CHAT_LINK"
        or owner.get("original_source_ref") is not None
        or not isinstance(owner.get("verbatim"), str)
        or "WHy i don't see any integration" not in owner["verbatim"]
        or owner.get("first_durable_mirror") !=
        "https://github.com/reallaksh19/Common/issues/717#issuecomment-6051883834"
    ):
        raise GoldenContractError("Owner quotation or honest source provenance missing")
    if owner.get("claim_origin") != _issue_url(repo, 717):
        raise GoldenContractError("Owner source/claim binding missing")

    counts = _required(programme, "integration_acceptance")
    total, qualified = counts.get("total"), counts.get("qualified")
    if not (
        type(total) is int and total >= 1
        and type(qualified) is int and 0 <= qualified <= total
    ):
        raise GoldenContractError("integration acceptance denominator invalid")
    if leaf.get("custody_source") != "SOURCE_NOT_PROVEN":
        raise GoldenContractError("fixture must represent the real unproven custody boundary")
    if leaf.get("semantic_state") != "HOLD":
        raise GoldenContractError("fixture cannot declare P3 semantic completion")
    if pr.get("state") != "DRAFT":
        raise GoldenContractError("PR must be draft in this retained golden")
    head = pr.get("head_sha")
    assessed = pr.get("checks_head_sha")
    if not (
        isinstance(head, str) and len(head) == 40
        and all(c in "0123456789abcdef" for c in head)
        and isinstance(assessed, str) and len(assessed) == 40
        and all(c in "0123456789abcdef" for c in assessed)
    ):
        raise GoldenContractError("PR candidate/qualification SHA unproven")
    checks = _required(pr, "checks")
    passed, total_checks = checks.get("passed"), checks.get("total")
    if (
        type(passed) is not int or type(total_checks) is not int
        or not 0 <= passed <= total_checks
    ):
        raise GoldenContractError("provider checks inconsistent")
    check_label = (
        f"CI {passed}/{total_checks}@{head[:7]}"
        if head == assessed
        else "CI STALE"
    )
    if health.get("status") != "UNKNOWN" or review.get("self") != "NOT_REVIEWED":
        raise GoldenContractError("golden health/self-review observation was silently promoted")
    if review.get("independent") != "NOT_REVIEWED":
        raise GoldenContractError("golden independent review cannot be inferred from CI")
    task_evidence = leaf.get("task_evidence_end")
    if not isinstance(task_evidence, str) or not task_evidence.startswith(_issue_url(repo, 732)):
        raise GoldenContractError("leaf task evidence link missing")
    next_step = leaf.get("actual_next")
    if not isinstance(next_step, str) or "fresh independent" not in next_step:
        raise GoldenContractError("actual next must preserve source/genesis blocker")

    parent_title = (
        f"[570→{pn} | P3#{ln} HOLD · R1#736 INCOMPLETE · "
        f"IC {qualified}/{total} qualified] Responsibility kernel"
    )
    child_title = (
        f"[{pn}/P3#{ln} | B2.3 HOLD · custody UNKNOWN · PR#{prn} DRAFT]"
        " Custody/recovery"
    )
    pr_title = (
        f"[{pn}/P3#{ln}→PR#{prn} | DRAFT HOLD · {check_label} "
        "· grant UNPROVEN] Custody fencing"
    )
    handover = "\n".join([
        f"ENTRY: {_issue_url(repo, pn)} → {_issue_url(repo, ln)} → "
        f"https://github.com/{repo}/pull/{prn}",
        f"OWNER (verbatim): {owner['verbatim']}",
        f"OWNER SOURCE: {owner['original_source_status']}; first durable GitHub copy: "
        f"{owner['first_durable_mirror']}",
        f"ROADMAP: {programme['roadmap_ref']}; IC {qualified}/{total} qualified",
        f"RESPONSIBILITY: {leaf['responsibility_id']}; semantic {leaf['semantic_state']}; "
        f"custody {leaf['custody_source']}",
        f"TASK_EVIDENCE END: {task_evidence}",
        f"PR HEAD: {head}; QUALIFICATION: {check_label}, never product acceptance",
        f"AGENT HEALTH: {health['status']} (advisory only)",
        f"SELF REVIEW: {review['self']}; independent review: {review['independent']}",
        f"ONE NEXT: {next_step}",
    ])
    checks_required = (
        "CR-01 Basis, scope and coverage",
        "CR-02 Design and system fit",
        "CR-03 Functional correctness and negative behavior",
        "CR-04 Simplicity, readability and maintainability",
        "CR-05 Tests and verification quality",
        "CR-06 Interfaces, data and compatibility",
        "CR-07 Security, privacy and trust boundaries",
        "CR-08 Reliability, errors, concurrency and operability",
        "CR-09 Documentation and change communication",
        "CR-10 Integration, regression and release fitness",
    )
    project_checks = (
        "R-01 Outcome-first wrong-world falsifier",
        "R-02 Original Owner text/source status",
        "R-03 Claim/leaf/task-evidence/spec lineage",
        "R-04 Candidate SHA/CI currentness",
        "R-05 #438 source and sibling custody isolation",
        "R-06 Parent/child/PR status drift",
        "R-07 Handover cold-entry without chat",
        "R-08 Health/advisory cannot grant progress",
        "R-09 Self-review vs distinct independence",
        "R-10 Agent-6 replay from three entry URLs",
    )
    return {
        "authority": "DERIVED_GOLDEN_ONLY_NOT_PRODUCTION",
        "basis": {
            "programme_issue": pn,
            "responsibility_issue": ln,
            "candidate_pr": prn,
            "candidate_sha": head,
            "owner_original_source_status": owner["original_source_status"],
        },
        "issue_titles": {"programme": parent_title, "responsibility": child_title},
        "pr_title": pr_title,
        "qualification": "CI_MATCHES_HEAD" if head == assessed else "CI_STALE",
        "product_status": "HOLD",
        "handover_prompt": handover,
        "agent_matrix": {
            "responsibility_issue": ln,
            "health": "UNKNOWN",
            "semantic_progress_effect": "NONE",
            "custody_authority_effect": "NONE",
        },
        "review_checklist": [
            {"criterion": criterion, "state": "NOT_REVIEWED"}
            for criterion in checks_required
        ],
        "project_review_checklist": [
            {"criterion": criterion, "state": "NOT_REVIEWED"}
            for criterion in project_checks
        ],
    }
