#!/usr/bin/env python3
"""#718 / #733 precommitted golden-fixture stress gate.

IMPORTANT: preflight is not end-to-end acceptance.  It runs the *existing*
R-BASIS/DELP and R-PROOF source functions with a real graph and retained
negative controls.  Full mode must fail until all consuming modules exist.
No GitHub writes, no work-credit, no authority promotion, no network.
The fixture manifest was committed before this implementation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GRAPH = ROOT / ".github/v32-evidence-spine/718-proposal-v2.json"
MANIFEST = HERE / "718-golden-fixtures-v1.json"
SOURCE = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
REQUIRED = (
    "OR_LEDGER", "DECOMPOSITION_BINDING", "TASK_EVIDENCE_INPUT",
    "SOURCE_OBSERVATION", "RESPONSIBILITY_SNAPSHOT", "PARENT_TITLE",
    "CHILD_TITLE", "PR_TITLE", "PR_MANAGED_DESCRIPTION", "HANDOVER_PROMPT",
    "AGENT_MATRIX",
)
EXPECTED_IDS = (
    "GF-ORIGIN", "GF-ORIGIN-MISSING", "GF-DECOMPOSE", "GF-LEGACY",
    "GF-UNDISCOVERED", "GF-REBASE", "GF-SMART-SURFACES", "GF-PR-HEAD",
    "GF-PUBLISH-RACE", "GF-COLD-AGENT", "GF-AGENT-PROVENANCE", "GF-VERTICAL",
)
STAGES_IMPLEMENTED = {"DECOMPOSITION_BINDING", "SOURCE_OBSERVATION"}  # Existing modules only.
ORIGINAL_SOURCE_STATUS = "UNRESOLVED_CHAT_MESSAGE_LINK"


class ContractError(ValueError):
    pass


def fail(reason: str) -> None:
    raise ContractError(reason)


def canonical_digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")).hexdigest()


def load() -> tuple[dict, dict]:
    return json.loads(MANIFEST.read_text(encoding="utf-8")), json.loads(GRAPH.read_text(encoding="utf-8"))


def validate_contract(m: dict, g: dict) -> dict:
    """Independent, fail-closed checks against the precommitted source graph."""
    if m.get("schema") != "common-v32-718-precommitted-oracles-v1":
        fail("WRONG_FIXTURE_SCHEMA")
    if (m.get("programme"), m.get("responsibility"), m.get("repository")) != (
        "Common#718", "Common#733", "reallaksh19/Common"
    ):
        fail("MISMATCHED_PROGRAMME_IDENTITY")
    if g.get("programme", {}).get("root") != m["programme"]:
        fail("GRAPH_ROOT_MISMATCH")
    proposal = g["programme"]["decomposition_proposal"]
    release = proposal.get("released_proposal_digest")
    if release != m.get("released_proposal_digest"):
        fail("STALE_RELEASE_DIGEST")
    claim_index = {r["id"]: r for r in g["programme"]["acceptance_claims"]}
    if len(claim_index) != 6 or sum(r["weight"] for r in claim_index.values()) != 100:
        fail("ESC_CLAIM_WEIGHT_DRIFT")
    fixture_rows = m.get("fixtures", [])
    fixture_index = {r["id"]: r for r in fixture_rows}
    if len(fixture_index) != len(fixture_rows) or set(fixture_index) != set(EXPECTED_IDS):
        fail("GOLDEN_FIXTURE_SET_DRIFT")
    if tuple(m.get("required_stage_outputs", ())) != REQUIRED:
        fail("STAGE_CONTRACT_DRIFT")
    oi_rows = m.get("owner_intents", [])
    ois = {r["id"]: r for r in oi_rows}
    if set(ois) != {"OI-718-03", "OI-718-04"}:
        fail("OWNER_INTENT_MISSING")
    reqs = {r["id"]: r for r in m["requirements"]}
    if set(reqs) != {f"OR-718-{n:02d}" for n in range(1, 8)}:
        fail("OR_LEDGER_GAP")
    for intent in oi_rows:
        if intent.get("original_source_ref") is None:
            if intent.get("original_source_status") != ORIGINAL_SOURCE_STATUS:
                fail("UNPROVEN_ORIGIN_NOT_DISCLOSED")
        elif not isinstance(intent.get("original_source_ref"), str):
            fail("INVALID_ORIGIN_LINK")
        if not intent.get("verbatim") or not intent.get("durable_archive_ref", "").startswith("https://github.com/"):
            fail("OWNER_QUOTATION_OR_ARCHIVE_MISSING")
        if "i dont see any integration" in intent["verbatim"]:
            if "handover prompt and agent metric" not in intent["verbatim"]:
                fail("OWNER_QUOTATION_PARAPHRASED")
        for rid in intent.get("requirements", []):
            if rid not in reqs:
                fail("OWNER_TO_OR_BROKEN")
    expected_claim_by_r = {
        "R-BASIS": "ESC-1", "R-PROOF": "ESC-2",
        "R-PROJECTION": "ESC-3", "R-RECONSTRUCTION": "ESC-4",
        "R-QUALITY": "ESC-5", "G-REPLAY": "ESC-6",
    }
    proposed = {r["id"]: r for r in proposal["responsibilities"]}
    for rid, claim in expected_claim_by_r.items():
        if claim not in claim_index or rid not in proposed or claim not in proposed[rid]["owns_claims"]:
            fail("DECOMPOSITION_CLAIM_OWNERSHIP_DRIFT")
    for row in m["requirements"]:
        if row["responsibility"] not in expected_claim_by_r:
            fail("UNKNOWN_OR_OWNER")
        if row["claims"] != [expected_claim_by_r[row["responsibility"]]]:
            fail("OR_CLAIM_MISMATCH")
        for fixture_id in row["fixture_ids"]:
            if fixture_id not in fixture_index:
                fail("OR_TO_GOLDEN_GAP")
    for row in fixture_rows:
        if not row.get("source_refs") or row.get("oracle_authority") != "PRECOMMITTED_SPECIFICATION_NOT_DERIVED_FROM_RENDERER":
            fail("NON_INDEPENDENT_ORACLE")
        if row["claim"] != expected_claim_by_r[row["responsibility"]]:
            fail("FIXTURE_CLAIM_MISMATCH")
        if not any(row["id"] in rr["fixture_ids"] for rr in m["requirements"]):
            fail("ORPHAN_GOLDEN_FIXTURE")
        if not row.get("expected") or not row.get("negative_mutation"):
            fail("NO_INDEPENDENT_EXPECTED_OR_NEGATIVE")
        if not set(row["consumer_states"]).issubset(REQUIRED):
            fail("UNKNOWN_CONSUMER")
    nodes = {n.get("responsibility_id"): n for n in g["nodes"] if n.get("responsibility_id")}
    historic = {r["responsibility"]: r for r in m["observed_historical_material"]}
    for rid, expected_issue, expected_pr in (
        ("R-BASIS", "Common#720", "Common#722"),
        ("R-PROOF", "Common#724", "Common#728"),
        ("R-PROJECTION", "Common#733", None),
    ):
        if nodes.get(rid, {}).get("ref") != expected_issue or nodes[rid].get("primary_pr") != expected_pr:
            fail("PROVIDER_BINDING_DRIFT")
        if historic[rid]["issue"] != expected_issue or historic[rid]["pr"] != expected_pr:
            fail("FROZEN_HISTORY_BINDING_DRIFT")
    root = next(n for n in g["nodes"] if n["kind"] == "ROOT")
    decomposed = fixture_index["GF-DECOMPOSE"]["expected"]
    if root["reserve_weight"] != decomposed["reserve_weight"] or decomposed["reserve_weight"] != 35:
        fail("RESERVE_WEIGHT_DRIFT")
    if decomposed["bindings"] != {
        "R-BASIS": "Common#720", "R-PROOF": "Common#724",
        "R-PROJECTION": "Common#733",
    }:
        fail("GOLDEN_BINDING_DRIFT")
    if decomposed["claim_weight_sum"] != sum(c["weight"] for c in claim_index.values()):
        fail("GOLDEN_CLAIM_WEIGHT_DRIFT")
    if any(historic[r]["checkpoint_facts"] != "UNREPORTED" for r in historic):
        fail("HISTORICAL_FACTS_FABRICATED")
    legacy = fixture_index["GF-LEGACY"]["expected"]
    if (legacy["checkpoint_facts"], legacy["material_pr_states"], legacy["programme_complete"]) != (
        ["UNREPORTED", "UNREPORTED"], ["MERGED", "MERGED"], False
    ):
        fail("GOLDEN_LEGACY_ORACLE_DRIFT")
    if m["frozen_expected_current_views"].get("full_integrated_replay") != "NOT_IMPLEMENTED":
        fail("PREMATURE_FULL_PASS")
    return {"release_digest": release, "graph_nodes": len(g["nodes"]),
            "fixture_count": len(fixture_index), "OR_count": len(reqs),
            "owner_intents": len(ois), "root_reserve": root["reserve_weight"]}


def source_module(name: str):
    p = SOURCE / (name + ".py")
    spec = importlib.util.spec_from_file_location(name, p)
    if spec is None or spec.loader is None:
        fail("SOURCE_MODULE_UNAVAILABLE:" + name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate_source(m: dict, g: dict) -> dict:
    """Run *real* V3.2 source functions. No mock status projector."""
    delp = source_module("delp_projection_v32")
    history = {r["responsibility"]: r for r in m["observed_historical_material"]}
    obs = {
        r["issue"]: {"candidate_sha": r["head_sha"], "pr_state": r["pr_state"]}
        for r in history.values() if r["head_sha"]
    }
    seen = delp.project(g, [], obs)
    for issue in ("Common#720", "Common#724"):
        row = seen["nodes"][issue]
        if row["progress"]["P"] != 0 or row["progress"]["E"] != 0:
            fail("MERGE_PROMOTED_TO_SEMANTIC_PROGRESS")
        if row["state"] not in ("UNMATERIALIZED", "EVIDENCE_GAP", "NOT_RELEASEABLE"):
            fail("MISSING_FACTS_UNEXPECTEDLY_HEALTHY:" + row["state"])
    if seen["nodes"]["Common#718"]["state"] == "COMPLETE":
        fail("PARENT_COMPLETE_WITH_RESERVE_AND_MISSING_FACTS")
    if seen["nodes"]["Common#733"]["progress"]["P"] != 0:
        fail("CHILD_PROGRESS_WITHOUT_FACTS")
    if seen["rejected_facts"]:
        fail("EMPTY_LEDGER_SHOULD_NOT_REJECT")
    # The separately released qualification observer must reject green but
    # undiscovered tests. Deliberately synthetic provider, grounded by the
    # #715 real-history failure mode. Never authenticate synthetic as real.
    q = source_module("qualification_observation_v32")
    sha = m["fixtures"][4]["input"]["candidate"]
    case = "test_retained_fixture.StressCase.test_required_case"
    contract = {
        "schema": q.INPUT_SCHEMA, "repository": "reallaksh19/Common",
        "responsibility": "Common#724", "pull_number": 715,
        "candidate_sha": sha,
        "requirements": [{
            "id": "REQUIRED-TEST", "kind": "UNITTEST", "case_id": case,
            "job_name": "v32 qualification", "step_name": "Run required cases",
        }],
    }
    class GreenButMissingTest:
        def get_pull(self, repo, number):
            return {"number": 715, "head": {"sha": sha}, "state": "open"}
        def list_runs(self, repo, head):
            return [{"id": 1, "head_sha": sha, "status": "completed", "conclusion": "success"}]
        def list_jobs(self, repo, number):
            return [{"id": 2, "name": "v32 qualification", "status": "completed",
                     "conclusion": "success", "steps": [{"name": "Run required cases",
                     "status": "completed", "conclusion": "success"}]}]
        def get_job_log(self, repo, number):
            return "Ran 0 tests in 0.000s\nOK\n"
    proof = q.assess(contract, GreenButMissingTest())
    if proof["overall"] == "PROVEN" or proof["requirements"][0]["status"] == "PROVEN":
        fail("UNEXECUTED_TEST_ACQUIRED_PROOF")
    return {
        "authority": "OBSERVATION_ONLY",
        "real_projector_input_digest": seen["input_digest"],
        "programme_state": seen["nodes"]["Common#718"]["state"],
        "legacy_leaf_states": {r: seen["nodes"][r]["state"] for r in ("Common#720", "Common#724")},
        "legacy_P_E": {r: seen["nodes"][r]["progress"] for r in ("Common#720", "Common#724")},
        "unexecuted_test_overall": proof["overall"],
    }


def stress_mutations(m: dict, g: dict) -> dict:
    """Each intentional corruption must be rejected, never create green."""
    mutations = {
        "DROP_OWNER_SOURCE_STATUS": lambda a, b: a["owner_intents"][0].pop("original_source_status"),
        "BREAK_OR_TO_CLAIM": lambda a, b: a["requirements"][3].update(claims=["ESC-1"]),
        "FORGE_MERGED_P100": lambda a, b: a["fixtures"][3]["expected"].update(programme_complete=True),
        "SWAP_PR_BINDING": lambda a, b: next(x for x in b["nodes"] if x.get("responsibility_id") == "R-PROOF").update(primary_pr="Common#999"),
        "DELETE_REQUIRED_FIXTURE": lambda a, b: a["fixtures"].pop(),
        "CREATE_DUPLICATE_FIXTURE": lambda a, b: a["fixtures"].append(copy.deepcopy(a["fixtures"][0])),
        "FALSE_FULL_GREEN": lambda a, b: a["frozen_expected_current_views"].update(full_integrated_replay="PASS"),
        "REMOVE_NEGATIVE_ORACLE": lambda a, b: a["fixtures"][0].update(negative_mutation=""),
        "REWEIGHT_PROGRAMME": lambda a, b: b["programme"]["acceptance_claims"][0].update(weight=25),
    }
    results = {}
    for case, mutate in mutations.items():
        a, b = copy.deepcopy(m), copy.deepcopy(g)
        mutate(a, b)
        try:
            validate_contract(a, b)
        except ContractError as exc:
            results[case] = {"outcome": "EXPECTED_REJECTION", "reason": str(exc)}
        else:
            fail("NEGATIVE_MUTATION_NOT_DETECTED:" + case)
    return results


def run(mode: str) -> dict:
    m, g = load()
    basis = validate_contract(m, g)
    observed = evaluate_source(m, g)
    negatives = stress_mutations(m, g)
    stage_results = {
        k: ("EXISTING_SOURCE_PARTIAL" if k in STAGES_IMPLEMENTED else "NOT_IMPLEMENTED")
        for k in REQUIRED
    }
    # No task evidence was authored for the merged history, and no new PR exists.
    stage_results["TASK_EVIDENCE_INPUT"] = "UNREPORTED"
    stage_results["OR_LEDGER"] = "PRECOMMITTED_SPEC_ONLY"
    stage_results["RESPONSIBILITY_SNAPSHOT"] = "INCOMPLETE_SOURCE_JOIN"
    stage_results["PARENT_TITLE"] = "MANUAL_OBSERVED_ONLY"
    stage_results["CHILD_TITLE"] = "MANUAL_OBSERVED_ONLY"
    stage_results["PR_TITLE"] = "NO_PRODUCT_PR_AND_RENDERER_NOT_IMPLEMENTED"
    full_ready = all(x == "IMPLEMENTED_AND_GOLDEN_MATCHED" for x in stage_results.values())
    result = {
        "schema": "common-v32-718-preflight-cycle-report-v1",
        "mode": mode,
        "authority": "READ_ONLY_GOLDEN_PREFLIGHT_NOT_DELIVERY",
        "fixture_manifest_digest": canonical_digest(m),
        "graph_digest": canonical_digest(g),
        "oracle_precommit": m["main_at_precommit"],
        "baseline": basis,
        "source_executed": observed,
        "negative_mutations": negatives,
        "consumer_results": stage_results,
        "full_integrated_gate": "PASS" if full_ready else "FAIL_CLOSED_UNIMPLEMENTED_CONSUMERS",
        "actual_next": "AUTHORIZE_FROZEN_SOURCE_PATHS_AND_IMPLEMENT_RELEASED_R_PROJECTION",
    }
    if mode == "full" and not full_ready:
        result["exit_code"] = 2
    else:
        result["exit_code"] = 0
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("preflight", "full"), default="preflight")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = run(args.mode)
    except Exception as exc:
        print(f"PRECOMMITTED-GOLDEN-STRESS ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    output = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output)
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
