#!/usr/bin/env python3
"""R1-E: self-running cross-surface cycle/stress oracle, NOT live GitHub sync.

All rendered issue/PR/Owner Report/TASK_EVIDENCE/handover/agent/reviewer views
come from one historical golden input and share one reproducible basis digest.
This module does not fetch, write, authorize, approve or merge anything.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from integration_golden_v35 import GoldenContractError, derive


FIXTURE = Path(__file__).resolve().parents[1] / "examples/integration/real-common-600-604-712.golden.json"

# Historical R1-E oracle only. Production delivery status MUST come from
# governed programme evidence and provider-current readback (R2-R6).
HISTORICAL_DELIVERY = (
    ("Owner verbatim ledger and source", "DELIVERED_MANUAL", "#600, #717 mirror"),
    ("R1-B/C issue/PR/handover golden", "DELIVERED_TESTED", "PR#737 golden test"),
    ("Cross-surface cycle demonstration", "CODED_NOT_LIVE", "This self-run oracle"),
    ("R2 live governed DELP adapter", "NOT_CODED", "#738"),
    ("R3/R4 live issue and PR sync", "NOT_CODED_NOT_TESTED", "#717"),
    ("R5 current handover and agent metric", "NOT_WIRED_NOT_TESTED", "#717"),
    ("R6 new-agent and independent review", "NOT_TESTED", "#717"),
    ("#604 native current custody grant", "BLOCKED_SOURCE_NOT_PROVEN", "#730"),
)
ORIGINS = (
    "parent_issue", "child_issue", "draft_pr",
)


def canonical_basis(source: Mapping[str, Any]) -> str:
    # expected is a fixture assertion, not source-of-truth data.
    basis = {k: v for k, v in source.items() if k != "expected"}
    encoded = json.dumps(basis, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def cycle(source: Mapping[str, Any]) -> dict[str, Any]:
    """Emit one bounded, non-authoritative multi-consumer specimen."""
    view = derive(source)
    digest = canonical_basis(source)
    p = source["programme"]
    leaf = source["responsibility"]
    candidate = source["candidate_pr"]
    origin = source["owner_origin"]
    repo = p["repository"]
    prefix = f"BASIS_SHA256: {digest}\nSOURCE: HISTORICAL_GOLDEN_NOT_PROVIDER_CURRENT\n"
    chain = (
        f"PROGRAMME: https://github.com/{repo}/issues/{p['issue']}\n"
        f"LEAF: https://github.com/{repo}/issues/{leaf['issue']}\n"
        f"DRAFT_PR: https://github.com/{repo}/pull/{candidate['number']}\n"
        f"RESPONSIBILITY_ID: {leaf['responsibility_id']}\n"
        f"SPEC_GENERATION: {leaf['spec_generation']}\n"
        f"OWNER_ORIGINAL_SOURCE: {origin['original_source_status']}\n"
        f"OWNER_FIRST_DURABLE: {origin['first_durable_mirror']}\n"
        f"EVIDENCE_REF: {leaf['task_evidence_end']}\n"
        f"CANDIDATE_SHA: {candidate['head_sha']}\n"
        f"QUALIFICATION: {view['qualification']}\n"
        f"SEMANTIC: {view['product_status']}\n"
        f"CUSTODY: {leaf['custody_source']}\n"
        f"NEXT: {leaf['actual_next']}\n"
    )
    body = prefix + chain
    delivery = "\n".join(
        f"| {name} | {state} | {proof} |"
        for name, state, proof in HISTORICAL_DELIVERY
    )
    table = ("| Capability | Delivered / coded / tested status | Evidence/next |\n"
             "|---|---|---|\n" + delivery)
    parent = (
        f"<!-- V35_CYCLE_GOLDEN_START -->\n{body}"
        "SCOPE: PROGRAMME / OWNER INTENT / CLAIM ROADMAP\n"
        f"OWNER_VERBATIM:\n{origin['verbatim']}\n"
        f"INTEGRATION_ACCEPTANCE: {p['integration_acceptance']['qualified']}/"
        f"{p['integration_acceptance']['total']} QUALIFIED\n"
        f"{table}\n<!-- V35_CYCLE_GOLDEN_END -->\n"
    )
    child = (
        f"<!-- V35_CYCLE_GOLDEN_START -->\n{body}"
        "SCOPE: LEAF / CLAIM / TASK_EVIDENCE / SOURCE SAFETY\n"
        "RESULT: prepared isolated IDLE fixture only; actual #604 authority UNPROVEN\n"
        f"{table}\n<!-- V35_CYCLE_GOLDEN_END -->\n"
    )
    prbody = (
        f"<!-- V35_PR_CYCLE_GOLDEN_START -->\n{body}"
        "SCOPE: CANDIDATE QUALIFICATION; NOT SEMANTIC COMPLETION\n"
        f"CHECKS_AT_SHA: {candidate['checks_head_sha']}\n"
        f"CI_COUNTS: {candidate['checks']['passed']}/{candidate['checks']['total']}\n"
        "STATUS: DRAFT HOLD; DO NOT MERGE\n"
        f"{table}\n<!-- V35_PR_CYCLE_GOLDEN_END -->\n"
    )
    owner_report = (
        "OR — OWNER-FACING REPORT (DEMONSTRATION; abbreviation not authority)\n"
        + body + table + "\n"
        + "SEPARATE GATES: 5/5 CI (historical) != current #604 grant or IC completion\n"
    )
    start = (
        "TASK_EVIDENCE — START [GENERATED EXAMPLE, NOT A PUBLISHED FACT]\n"
        + body
        + "UNIT: inspect source/claim/leaf and precommit falsifiers\n"
        + "REVIEW_REQUIRED: CR-01..CR-10 plus project R-01..R-10\n"
    )
    end = (
        "TASK_EVIDENCE — END [GENERATED EXAMPLE, NOT A PUBLISHED FACT]\n"
        + body
        + "MATERIAL_OUTCOME: historical fixture projection only; no production mutation\n"
        + "SELF_REVIEW: NOT_REVIEWED; PRINCIPAL_INDEPENDENCE: NONE_ASSERTED\n"
        + "INDEPENDENT_REVIEW: NOT_REVIEWED\n"
    )
    handover = body + "HANDOVER:\n" + view["handover_prompt"] + "\n"
    agent = (
        body + "AGENT_HEALTH: UNKNOWN; ADVISORY_ONLY: TRUE\n"
        + "P/E_PROGRESS_EFFECT: NONE; CUSTODY_GRANT_EFFECT: NONE\n"
        + "EXECUTOR_IDENTITY_AUTHENTICATED: NOT_PROVEN\n"
    )
    common = "\n".join(
        "- [ ] " + entry["criterion"] + " — " + entry["state"]
        for entry in view["review_checklist"]
    )
    project = "\n".join(
        "- [ ] " + entry["criterion"] + " — " + entry["state"]
        for entry in view["project_review_checklist"]
    )
    review = (
        body + "REVIEW_MODE: NOT_REVIEWED\n"
        + "PRINCIPAL_INDEPENDENCE: NONE_ASSERTED\n"
        + "COMMON REVIEWER CR-01..CR-10:\n" + common
        + "\nPROJECT R-01..R-10:\n" + project + "\n"
    )
    return {
        "mode": "OFFLINE_HISTORICAL_GOLDEN_NOT_LIVE",
        "basis_sha256": digest,
        "titles": {
            "parent_issue": view["issue_titles"]["programme"],
            "child_issue": view["issue_titles"]["responsibility"],
            "draft_pr": view["pr_title"],
        },
        "surfaces": {
            "parent_issue": parent,
            "child_issue": child,
            "draft_pr": prbody,
            "owner_report": owner_report,
            "task_evidence_start": start,
            "task_evidence_end": end,
            "handover_prompt": handover,
            "agent_metrics": agent,
            "reviewer_checklist": review,
        },
        "qualification": view["qualification"],
        "semantic": view["product_status"],
    }


def assert_same_cycle(source: Mapping[str, Any], supplied: Mapping[str, Any]) -> None:
    """Reject drift in ANY title/body/entry. Never trust a supplied digest."""
    expected = cycle(source)
    if supplied != expected:
        for category in ("titles", "surfaces"):
            found = supplied.get(category)
            if not isinstance(found, Mapping):
                raise GoldenContractError(category + ": surface missing")
            for name, value in expected[category].items():
                if found.get(name) != value:
                    raise GoldenContractError(f"{category}.{name}: basis/content drift")
        raise GoldenContractError("cycle metadata/digest drift")


def stress_check(source: Mapping[str, Any]) -> dict[str, Any]:
    """Run real renderer repeatedly, corrupt every consumer and source guard."""
    good = cycle(source)
    assert_same_cycle(source, good)
    checked = 1
    for category in ("titles", "surfaces"):
        for name in good[category]:
            tamper = copy.deepcopy(good)
            tamper[category][name] += "\nUNAUTHORIZED_OR_STALE_CHANGE"
            try:
                assert_same_cycle(source, tamper)
            except GoldenContractError:
                checked += 1
            else:
                raise AssertionError(f"tamper accepted: {category}.{name}")
    for path, value in (
        (("responsibility", "issue"), 605),
        (("responsibility", "parent_issue"), 438),
        (("candidate_pr", "responsibility_issue"), 438),
        (("owner_origin", "first_durable_mirror"), "https://fake.invalid/source"),
        (("owner_origin", "original_source_status"), "PROVEN"),
        (("responsibility", "custody_source"), "SAFE"),
        (("agent_observation", "status"), "GREEN"),
        (("review_observation", "independent"), "APPROVED"),
        (("responsibility", "task_evidence_end"), "https://fake.invalid/evidence"),
    ):
        invalid = copy.deepcopy(source)
        invalid[path[0]][path[1]] = value
        try:
            cycle(invalid)
        except GoldenContractError:
            checked += 1
        else:
            raise AssertionError(f"source forgery accepted: {path}")
    changed = copy.deepcopy(source)
    changed["candidate_pr"]["head_sha"] = "d" * 40
    stale = cycle(changed)
    if (
        stale["qualification"] != "CI_STALE"
        or stale["semantic"] != good["semantic"] == "HOLD"
        or stale["titles"]["parent_issue"] != good["titles"]["parent_issue"]
        or stale["titles"]["child_issue"] != good["titles"]["child_issue"]
        or stale["titles"]["draft_pr"] == good["titles"]["draft_pr"]
        or stale["basis_sha256"] == good["basis_sha256"]
    ):
        raise AssertionError("PR head drift must stale CI without minting progress")
    assert_same_cycle(changed, stale)
    checked += 1
    # A tamper claiming the originally-qualified view after head movement fails.
    try:
        assert_same_cycle(changed, good)
    except GoldenContractError:
        checked += 1
    else:
        raise AssertionError("old green evidence accepted after head movement")
    return {
        "result": "PASS",
        "mode": "OFFLINE_GOLDEN_ONLY",
        "basis_sha256": good["basis_sha256"],
        "checked": checked,
        "surfaces": list(good["surfaces"]),
        "titles": list(good["titles"]),
        "stale_qualification": stale["qualification"],
        "product_status": good["semantic"],
        "live_provider_sync": "NOT_IMPLEMENTED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--stress-check", action="store_true", required=True)
    parser.add_argument("--emit", action="store_true", help="print generated specimen")
    args = parser.parse_args()
    source = json.loads(args.fixture.read_text(encoding="utf-8"))
    report = stress_check(source)
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.emit:
        result = cycle(source)
        for name, title in result["titles"].items():
            print(f"\n=== TITLE {name} ===\n{title}")
        for name, body in result["surfaces"].items():
            print(f"\n=== SURFACE {name} ===\n{body}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
