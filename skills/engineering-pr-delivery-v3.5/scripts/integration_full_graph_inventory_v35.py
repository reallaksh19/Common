"""R7-U4 — actual GitHub phase inventory and NON-AUTHORITATIVE graph coverage.

A closed issue, expected path, or valid synthetic DELP graph is never an
Owner-selected plan or a semantic progress/denominator source. This module
cannot create a new plan, score, approval or GitHub write.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Mapping
from typing import Any

import delp_projection_v35 as DELP
import integration_cold_entry_v35 as COLD
import integration_graph_authority_v35 as GRAPH
import integration_scoreboard_publish_v35 as PUBLISH

PHASES = ((1,602),(2,603),(3,604),(4,605),(5,606),(6,607),(7,608))
ROOT_ISSUE = 600
P0_ISSUE = 601  # reconciliation-only, ZERO semantic progress credit
CANDIDATE_PR = 712
_PHASE = re.compile(r"(?im)^phase:\s*P([1-7])\b")
_PARENT = re.compile(r"(?im)^Parent programme:\s*Common\s*#([0-9]+)\b")
_SHA = re.compile(r"^[a-f0-9]{40}$")


class GraphInventoryError(ValueError):
    """Invalid/foreign native source; do not infer missing authority."""


def _p0_baseline(transport: Any) -> dict[str, Any]:
    """Verify P0 as a native zero-credit *reconciliation*, never a plan leaf.

    A title that says COMPLETE does not close an issue or mint semantic
    progress. A TASK_EVIDENCE comment is evidence of P0 reconciliation,
    not graph plan, owner approval, Local custody or weighted DELP facts.
    """
    issue = transport.get_issue(P0_ISSUE)
    if not isinstance(issue, Mapping) or issue.get("number") != P0_ISSUE:
        raise GraphInventoryError("P0 native programme baseline #601 missing")
    body = str(issue.get("body") or "")
    required = (
        r"(?im)^Parent programme:\s*Common\s*#600\s*$",
        r"(?im)^phase:\s*P0\b",
        r"(?im)^responsibility_id:\s*RK-P0\s*$",
        r"(?im)^implementation_credit_at_creation:\s*0\s*$",
        r"(?im)^state_at_materialization:\s*RELEASED_RECONCILIATION_ONLY\s*$",
    )
    if not all(re.search(pattern, body) for pattern in required):
        raise GraphInventoryError("P0 baseline must identify ROOT/P0 and zero credit")
    comments = transport.list_comments(P0_ISSUE)
    if not isinstance(comments, list):
        raise GraphInventoryError("P0 native evidence comments unavailable")
    ends = [c for c in comments if isinstance(c, Mapping) and
            re.search(r"(?im)^# TASK_EVIDENCE\s*[—-]\s*END\b",
                      str(c.get("body") or ""))]
    if len(ends) != 1:
        raise GraphInventoryError("P0 requires exactly one native END reconciliation receipt")
    evidence = ends[0]
    statement = str(evidence.get("body") or "")
    evidence_claims = (
        r"(?im)^responsibility:\s*RK-P0\s*$",
        r"(?im)^issue:\s*Common#601\s*$",
        r"(?im)^result:\s*VERIFIED_RECONCILIATION_ONLY\s*$",
        r"(?im)^implementation_credit:\s*0\s*$",
        r"(?im)^source_mutation:\s*NONE\s*$",
    )
    if not all(re.search(pattern, statement) for pattern in evidence_claims):
        raise GraphInventoryError("P0 END claim is not source-bound zero-credit reconciliation")
    identifier = evidence.get("id")
    if type(identifier) is not int or identifier <= 0:
        raise GraphInventoryError("P0 END lacks a native GitHub comment identity")
    state = str(issue.get("state") or "UNKNOWN").upper()
    title = str(issue.get("title") or "")
    return {
        "issue": P0_ISSUE,
        "state": state,
        "title_claims_complete_but_open": state == "OPEN" and "COMPLETE" in title.upper(),
        "provider_end_receipt":
            f"https://github.com/reallaksh19/Common/issues/601#issuecomment-{identifier}",
        "end_sha256": hashlib.sha256(statement.encode("utf-8")).hexdigest(),
        "classification": "RECONCILIATION_ONLY_ZERO_IMPLEMENTATION_CREDIT",
        "programme_graph_weight": "NOT_AUTHORIZED_NOT_DERIVED",
        "progress_credit": "ZERO_NOT_UNIT_EVIDENCE",
    }


def _full_index(graph: Mapping[str,Any]) -> dict[str,Any]:
    """Validate candidate shape; never treat its own digest as approval."""
    try:
        DELP.require_repository_match(graph, "reallaksh19/Common", live=True)
        index = DELP.validate_graph(graph)
    except (DELP.DelpError, TypeError, ValueError) as exc:
        raise GraphInventoryError(f"candidate graph fails DELP validation: {exc}") from exc
    if index["root"] != "Common#600":
        raise GraphInventoryError("candidate root not the governed Common#600")
    nodes = index["nodes"]
    if "Common#601" in nodes:
        raise GraphInventoryError(
            "P0 #601 is reconciliation-only zero credit: no invented weighted DELP leaf"
        )
    missing = [f"Common#{n}" for _,n in PHASES if f"Common#{n}" not in nodes]
    if missing:
        raise GraphInventoryError("partial graph would erase governed P1–P7 phases: " + ", ".join(missing))
    selected = nodes["Common#604"]
    if selected["kind"] != "LEAF":
        raise GraphInventoryError("P3 #604 must be a governed selected LEAF or replan before R2-C publication")
    if not selected.get("primary_pr") or DELP.ref_number(selected["primary_pr"]) != CANDIDATE_PR:
        raise GraphInventoryError("P3 #604 must identify real primary PR #712")
    # DELP keeps legacy-compatible graphs by normalizing a missing
    # graph_generation to 1. That fallback has no production-source authority.
    if "graph_generation" not in (graph.get("programme") or {}):
        raise GraphInventoryError(
            "candidate missing explicitly declared graph_generation; "
            "legacy implicit generation 1 is not an Owner-current source"
        )
    if not index["programme"].get("graph_generation"):
        raise GraphInventoryError("graph must have a current monotonic generation")
    # This result is shape-only, never source authority, even if a caller also
    # submits a matching digest. Production issuance is a distinct OWNER act.
    return {"validation": "DELP_STRUCTURE_ONLY_NOT_OWNER_APPROVAL",
            "root": index["root"], "graph_digest": index["digest"],
            "graph_generation": index["programme"]["graph_generation"],
            "all_governed_phases_covered": True, "phase_count": 7,
            "candidate_pr": CANDIDATE_PR, "native_plan_authority": "NOT_DERIVED"}


def inspect(transport: Any, candidate: Mapping[str,Any] | None = None) -> dict[str,Any]:
    if getattr(transport, "repository", None) != "reallaksh19/Common":
        raise GraphInventoryError("inventory bound to actual programme repository")
    root = transport.get_issue(ROOT_ISSUE)
    if not isinstance(root, Mapping) or root.get("number") != ROOT_ISSUE or (
        "<!-- V35_PARENT_OWNER_INTENT_BEGIN -->" not in str(root.get("body") or "")
    ):
        raise GraphInventoryError("native #600 root identity and Owner-intent marker unavailable")
    p0 = _p0_baseline(transport)
    observations = []
    for phase,number in PHASES:
        issue = transport.get_issue(number)
        if not isinstance(issue,Mapping) or issue.get("number") != number:
            raise GraphInventoryError(f"native P{phase} #{number} issue missing")
        body = str(issue.get("body") or "")
        if set(_PHASE.findall(body)) != {str(phase)} or set(_PARENT.findall(body)) != {"600"}:
            raise GraphInventoryError(f"P{phase} issue has wrong/multiple programme or phase source")
        observations.append({
            "phase": f"P{phase}", "issue": number,
            "url": f"https://github.com/reallaksh19/Common/issues/{number}",
            "native_state": str(issue.get("state") or "UNKNOWN").upper(),
            "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "progress_credit": "NOT_DERIVED_FROM_ISSUE_CLOSURE",
        })
    pr = transport.get_pull(CANDIDATE_PR)
    if not isinstance(pr,Mapping) or pr.get("number") != CANDIDATE_PR or (
        ((pr.get("base") or {}).get("repo") or {}).get("full_name") != transport.repository
    ):
        raise GraphInventoryError("candidate PR #712 belongs to a foreign/missing repo")
    head = ((pr.get("head") or {}).get("sha"))
    if not isinstance(head,str) or not _SHA.fullmatch(head):
        raise GraphInventoryError("native selected P3 candidate PR head unavailable")
    comments = transport.list_comments(ROOT_ISSUE)
    if not isinstance(comments, list):
        raise GraphInventoryError("native root comments unavailable")
    matches = [c for c in comments if isinstance(c,Mapping) and
               GRAPH.APPROVAL_START in str(c.get("body") or "")]
    if len(matches)>1:
        raise GraphInventoryError("multiple root graph approvals require reconciliation")
    if matches:
        # Do not assume a matching marker is a valid OWNER selection: a
        # separate R2-C live authenticated approval read is still required.
        authority = "CANDIDATE_ROOT_COMMENT_PRESENT_REVERIFY_R2C"
    else:
        authority = "BLOCKED_NO_PROVIDER_APPROVED_GRAPH"
    structure = _full_index(candidate) if candidate is not None else None
    return {
        "schema":"V35_FULL_PROGRAMME_SOURCE_INVENTORY_V1",
        "repository":transport.repository,
        "root":"Common#600",
        "p0_reconciliation_baseline": p0,
        "source_phase_count":len(observations),
        "phase_source_inventory": observations,
        "p3_pr":CANDIDATE_PR,
        "p3_head":head,
        "p3_draft":bool(pr.get("draft")),
        "root_native_comment_count":len(comments),
        "root_graph_approval_marker_count":len(matches),
        "owner_graph_approval":authority,
        "source_graph_generation":"UNKNOWN_WITHOUT_OWNER_SELECTED_GRAPH",
        "source_phase_weights":"UNKNOWN_WITHOUT_OWNER_SELECTED_GRAPH",
        "source_unit_weights":"UNKNOWN_WITHOUT_OWNER_SELECTED_GRAPH",
        "source_spec_generations":"UNKNOWN_WITHOUT_OWNER_SELECTED_GRAPH",
        "source_denominator":"UNKNOWN_WITHOUT_OWNER_SELECTED_GRAPH",
        "candidate_structure":structure,
        "replay_permission":"NONE",
        "native_custody":"SOURCE_NOT_PROVEN",
        "integration_acceptance":"NOT_DERIVED",
        "actual_next":("R2C_VERIFY_EXISTING_OWNER_ROOT_SELECTION"
                       if matches else "OWNER_SELECT_FULL_P1_TO_P7_GRAPH_WITH_REAL_WEIGHT_AND_GENERATION_SOURCE"),
        "read_only":True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="V3.5 full P1–P7 native graph source inventory")
    parser.add_argument("--repository",required=True)
    args=parser.parse_args(argv)
    try:
        result=inspect(PUBLISH.ScoreboardTransport(args.repository))
        print(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False))
        # This inventory only observes native *marker presence*; it never
        # authenticates an Owner grant. R2-C must independently verify a
        # typed root comment, immutable graph bytes and its issuer.
        # Therefore a marker alone can never yield a successful (0) CLI.
        return 3
    except (GraphInventoryError, DELP.DelpError, OSError, ValueError) as exc:
        print(f"R7-U4 inventory SOURCE_REJECTED: {exc}",file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
