"""R5: one R2-D source snapshot to nine read-only relay consumer surfaces.

This module makes no GitHub writes, CI calls, Local admissions, review verdicts
or Owner attestations. A rendered TASK_EVIDENCE is a COPYABLE *TEMPLATE*,
not a proof of actual publication or an agent completion claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from typing import Any

import integration_cold_entry_v35 as COLD
import integration_scoreboard_publish_v35 as TRANSPORT

SURFACES = (
    "parent_issue", "child_issue", "draft_pr", "owner_report",
    "task_evidence_start", "task_evidence_end", "handover_prompt",
    "agent_metrics", "reviewer_checklist",
)
COMMON_CR = (
    "CR-01 Source basis, responsibility and coverage",
    "CR-02 Design and system integration",
    "CR-03 Functional negative-case correctness",
    "CR-04 Simplicity, readability and boundaries",
    "CR-05 Exact-head tests and evidence",
    "CR-06 Interfaces and compatibility",
    "CR-07 Security, provenance and trust",
    "CR-08 Race, readback and operational resilience",
    "CR-09 Documentation and owner disclosure",
    "CR-10 Integration, release and cold entry",
)
PROJECT_R = (
    "R-01 Outcome-first wrong-world falsifier",
    "R-02 Original Owner intent and source links",
    "R-03 Decomposition, claim and task evidence",
    "R-04 Candidate head, checks and currentness",
    "R-05 Native #438/#604 custody and sibling isolation",
    "R-06 Parent/child/PR status drift",
    "R-07 Chat-free independent entrant",
    "R-08 Agent metrics cannot mint facts",
    "R-09 Self-review versus independent principal",
    "R-10 Three-entry Agent-6 replay",
)


class RelayConsumerError(ValueError):
    """Source cannot be advertised as accepted or cross-consumer stable."""


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def _ref(value: Any) -> str:
    return str(value) if isinstance(value, str) and value.strip() else "UNKNOWN"


def build(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Project one canonical read-only R2-D result, never invent evidence."""
    if not isinstance(snapshot, Mapping) or snapshot.get("schema") != "V35_COLD_ENTRY_READINESS_V1":
        raise RelayConsumerError("must consume native R2-D provider-backed source")
    state = snapshot.get("status")
    if state not in ("HOLD_NO_PROVIDER_APPROVED_GRAPH",
                     "GOVERNED_GRAPH_PROVIDER_OBSERVED_READ_ONLY"):
        raise RelayConsumerError("unsupported or unverified source state")
    if snapshot.get("programme_ic_credit") != "NOT_DERIVED" or snapshot.get("native_custody") != "SOURCE_NOT_PROVEN":
        raise RelayConsumerError("refuse inflated IC or native custody authority")
    if snapshot.get("event_workflow_activation") != "NOT_AUTHORIZED" or snapshot.get("provider_read_only") is not True:
        raise RelayConsumerError("source cannot grant live publication")
    repo, root = snapshot.get("repository"), snapshot.get("root")
    if not isinstance(repo, str) or not isinstance(root, str) or not repo or not root:
        raise RelayConsumerError("provider repo and programme root required")
    approved = state.startswith("GOVERNED_")
    leaf = _ref(snapshot.get("selected_leaf"))
    pr = snapshot.get("approved_pr")
    if approved:
        candidate = _ref(snapshot.get("exact_head"))
        source_digest = _ref(snapshot.get("basis_sha256"))
        graph_digest = _ref(snapshot.get("graph_digest"))
        if candidate == "UNKNOWN" or len(candidate) != 40 or len(source_digest) != 64:
            raise RelayConsumerError("approved source has no full exact head and DELP basis")
        if not isinstance(pr, int) or pr <= 0 or leaf == "UNKNOWN" or graph_digest == "UNKNOWN":
            raise RelayConsumerError("approved selection missing graph leaf or PR")
        next_action = str((snapshot.get("actual_next") or {}).get("action") or "")
        if not next_action:
            raise RelayConsumerError("approved DELP source missing actual-next")
        progress = snapshot.get("progress")
        if not isinstance(progress, Mapping) or type(progress.get("P")) is not int or type(progress.get("E")) is not int:
            raise RelayConsumerError("approved source progress not normalized")
        if not 0 <= progress["E"] <= progress["P"] <= 100:
            raise RelayConsumerError("source P/E is contradictory")
        evidence = snapshot.get("accepted_evidence_sources", ())
        if not isinstance(evidence, (list, tuple)):
            raise RelayConsumerError("evidence source references not a list")
        evidence_refs = [str(x) for x in evidence]
        engineering = f"P{progress['P']}/E{progress['E']}"
    else:
        if snapshot.get("graph_source") != "NOT_PRESENT_IN_GOVERNING_ROOT_COMMENTS":
            raise RelayConsumerError("HOLD source must be authentic native absence")
        source_digest, graph_digest, candidate = "NO_APPROVED_GRAPH", "UNKNOWN", "UNKNOWN"
        next_action = "OWNER_PUBLISH_APPROVED_GRAPH_SELECTION_THEN_REPLAY"
        evidence_refs = []
        engineering = "UNQUALIFIED_NO_APPROVED_GRAPH"
        pr = "UNKNOWN"
    # A deterministic *report digest* is not a graph approval or evidence basis.
    data = {
        "repository": repo, "root": root, "source_status": state,
        "source_basis": source_digest, "graph_digest": graph_digest,
        "leaf": leaf, "pr": pr, "exact_head": candidate,
        "engineering": engineering, "actual_next": next_action,
        "evidence_refs": evidence_refs, "owner_original_source": "UNPROVEN",
        "custody": "SOURCE_NOT_PROVEN", "programme_ic": "NOT_DERIVED",
        "reviews": "NOT_REVIEWED", "independent_reviewer": "NOT_OBSERVED",
        "agent_health": "ADVISORY_NOT_MEASURED",
        "owner_release": "NOT_INFERRED", "event_workflow": "NOT_AUTHORIZED",
    }
    relay_digest = _digest(data)
    header = "\n".join((
        f"RELAY_REPORT_SHA256: {relay_digest}",
        f"DELP_SOURCE_BASIS: {source_digest}",
        f"SOURCE_STATUS: {state}",
        f"REPOSITORY: {repo}",
        f"PROGRAMME_ROOT: {root}",
        f"SELECTED_LEAF: {leaf}",
        f"PRIMARY_PR: {pr}",
        f"EXACT_CANDIDATE: {candidate}",
        f"ENGINEERING: {engineering}",
        f"ACTUAL_NEXT: {next_action}",
        "ORIGINAL_OWNER_CHAT: UNPROVEN",
        "NATIVE_CUSTODY: SOURCE_NOT_PROVEN",
        "PROGRAMME_IC: NOT_DERIVED",
        "LIVE_SCOREBOARD: NOT_AUTHORIZED",
        "INDEPENDENT_REVIEW: NOT_OBSERVED",
    ))
    refs = ", ".join(evidence_refs) if evidence_refs else "NONE_PROVIDER_VERIFIED"
    def surface(name: str, detail: str) -> str:
        return f"# {name}\n{header}\n{detail.strip()}\n"
    base_review = "\n".join(
        f"- [ ] {label} — UNREVIEWED" for label in COMMON_CR + PROJECT_R
    )
    outcome = "HOLD_NO_APPROVED_GRAPH" if not approved else "SOURCE_READ_ONLY_ACCEPTANCE_NOT_DERIVED"
    contents = {
        "parent_issue": surface("Parent issue — read-only scoreboard source",
            f"PROVENANCE: {outcome}\nProgress/scoreboard: {engineering}; do not write issue status.\nREADINESS: NOT_ACTIVATED"),
        "child_issue": surface("Child responsibility — read-only source",
            f"RESPONSIBILITY: {leaf}\nPROVENANCE: {outcome}\nAccepted evidence: {refs}\nNEXT: {next_action}"),
        "draft_pr": surface("Draft PR — read-only source",
            f"PR: {pr}\nHEAD: {candidate}\nPR_CHECKS: NOT_OBSERVED_IN_THIS_CONSUMER\nLOCAL_MERGE: NOT_AUTHORIZED"),
        "owner_report": surface("Owner-facing delivery reality report",
            "\n".join((
                "DELIVERED: SOURCE_EVIDENCE_ONLY_NOT_DELIVERY_ASSERTION",
                "CODED_UNQUALIFIED: UNKNOWN_FROM_THIS_SOURCE",
                "NOT_CODED: UNKNOWN_FROM_THIS_SOURCE",
                "NOT_TESTED: UNKNOWN_FROM_THIS_SOURCE",
                f"BLOCKED: {outcome}",
                f"ACCEPTED_PROVIDER_FACTS: {refs}",
                f"NEXT: {next_action}",
            ))),
        "task_evidence_start": surface("TASK_EVIDENCE START — TEMPLATE ONLY",
            f"TASK: UNKNOWN_NEW_AGENT_CLAIM\nSTART_SOURCE_REF: UNPUBLISHED\nEXACT_HEAD: {candidate}\nUNIT: UNKNOWN\nNEXT: {next_action}\nNOT_A_PROVIDER_FACT"),
        "task_evidence_end": surface("TASK_EVIDENCE END — TEMPLATE ONLY",
            f"TASK: UNKNOWN_NEW_AGENT_CLAIM\nEXECUTION_RESULT: UNPROVEN\nHOSTED_TEST_RESULT: UNKNOWN\nREVIEW: UNREVIEWED\nACTUAL_EVIDENCE_COMMENT: NOT_PUBLISHED\nNEXT: {next_action}\nNOT_A_PROVIDER_FACT"),
        "handover_prompt": surface("Cold successor handover — read-only",
            f"REENTRY: parent issue / child issue / PR all resolve through the native provider.\nACCEPTED_REFS: {refs}\nDO_NOT_RELY_ON_PREDECESSOR_CHAT\nFIRST_ACTION: {next_action}"),
        "agent_metrics": surface("Agent health matrix — advisory only",
            "AGENT_RUN_COUNT: UNKNOWN\nAGENT_CONTINUITY: UNMEASURED\nAGENT_HEALTH: ADVISORY_NOT_MEASURED\nFACT_OR_CUSTODY_CREDIT: NONE"),
        "reviewer_checklist": surface("Common + project reviewer checklist",
            "REVIEWER_PRINCIPAL: NOT_OBSERVED\nINDEPENDENCE: NONE_ASSERTED\n" + base_review),
    }
    if set(contents) != set(SURFACES):
        raise RelayConsumerError("missing a required common relay consumer")
    if any(f"RELAY_REPORT_SHA256: {relay_digest}" not in output or
           f"DELP_SOURCE_BASIS: {source_digest}" not in output for output in contents.values()):
        raise RelayConsumerError("cross-surface source basis mismatch")
    return {
        "schema": "V35_UNIFIED_RELAY_READ_CONSUMERS_V1",
        "relay_report_sha256": relay_digest,
        "source_basis": source_digest,
        "approval_status": outcome,
        "delivery_permission": "NONE",
        "state": data,
        "surfaces": contents,
    }


def from_provider(transport: Any, entry_url: str) -> dict[str, Any]:
    """Reconstruct read-only GitHub truth, then render *every* consumer."""
    return build(COLD.reconstruct(transport, entry_url))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R5 cold-entry 9-surface relay report (NO WRITES)")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--entry-url", required=True)
    args = parser.parse_args(argv)
    try:
        model = from_provider(TRANSPORT.ScoreboardTransport(args.repository), args.entry_url)
        print(json.dumps(model, sort_keys=True, indent=2, ensure_ascii=False))
        return 0 if model["approval_status"] == "SOURCE_READ_ONLY_ACCEPTANCE_NOT_DERIVED" else 3
    except (COLD.ColdEntryError, RelayConsumerError, OSError, ValueError) as exc:
        print(f"R5 relay denied: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
