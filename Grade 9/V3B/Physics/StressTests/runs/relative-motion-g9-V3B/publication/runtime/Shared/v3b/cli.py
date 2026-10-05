"""Deterministic new-topic control; authoring runs in external fresh contexts."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

from .contracts import ContractError, digest, file_digest, load, require
from .owner import validate_request
from .question_sources import source_questions
from .relay import STAGES, accept_submission, advance_automatic, validate_actors, work_order
from .routing import make_bundles
from .sources import freeze_sources
from .state import RunStore


ROOT = Path(__file__).resolve().parents[2]


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".v3b-", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def initialize(request: dict, source_spec: dict, actors: list[dict], source_root: Path,
               artifact_root: Path, out: Path, expected_subject: str | None = None) -> dict:
    request = validate_request(request)
    require(expected_subject is None or request["subject"] == expected_subject, "WRONG_SUBJECT_KIT")
    validate_actors(actors, request["run_kind"])
    manifest = freeze_sources(source_spec, source_root, request)
    corpus = source_questions(manifest, source_root)
    declared = [q for topic in manifest["subtopics"] for q in topic.get("question_ids", [])]
    require(set(declared) == set(corpus), "GLOBAL_SOURCE_QUESTION_ACCOUNTING")
    require(len(declared) == len(set(declared)), "SOURCE_QUESTION_PRIMARY_HOME_DUPLICATE")
    bundles = make_bundles(manifest, request["bundles"])
    policy_path = ROOT / request["subject"] / "CoreContracts.json"
    policy = load(policy_path)
    bindings = list((ROOT / "Shared" / "v3b").glob("*.py"))
    bindings += [policy_path, ROOT / request["subject"] / "ProductionKit" / "validator.py"]
    metadata = {"request": request, "request_digest": digest(request), "manifest": manifest,
                "actors": actors, "bundles": bundles, "subject_policy": policy,
                "source_root": str(source_root.resolve()), "artifact_root": str(artifact_root.resolve()),
                "runtime_bindings": [{"path": str(x), "sha256": file_digest(x)} for x in sorted(bindings)],
                "runtime_version": "0.1.0", "release_authorized": False}
    store = RunStore.create(out, metadata)
    try:
        return status(store)
    finally:
        store.close()


def status(store: RunStore) -> dict:
    metadata = store.metadata()
    rows = []
    for bundle in metadata["bundles"]:
        state = store.bundle(bundle["bundle_id"])
        next_stage = STAGES[state["cursor"]] if state["cursor"] < len(STAGES) else "COMPLETE"
        rows.append({**state, "next_stage": next_stage, "first_role": bundle["first_role"]})
    return {"request_id": metadata["request"]["request_id"], "subject": metadata["request"]["subject"],
            "run_kind": metadata["request"]["run_kind"], "bundles": rows, "release_authorized": False,
            "agent_execution": "EXTERNAL_HOST_REQUIRED", "learner_mastery": "NOT_OBSERVED"}


def export_run(store: RunStore, out: Path) -> dict:
    from .relay import context_for
    metadata = store.metadata()
    exports = []
    for bundle in metadata["bundles"]:
        bid = bundle["bundle_id"]
        context_for(store, bid)
        for stage, packet in store.packets(bid).items():
            filename = f"{digest(bid)[:12]}-{stage}.json"
            write_json(out / filename, packet)
            exports.append({"bundle_id": bid, "stage": stage, "file": filename,
                            "sha256": file_digest(out / filename), "packet_digest": packet["digest"]})
    result = {"status": status(store), "artifacts": exports, "events": store.events(),
              "request_digest": metadata["request_digest"], "source_manifest": metadata["manifest"],
              "human_release_authorized": False}
    write_json(out / "handoff.json", result)
    return {"handoff": str(out / "handoff.json"), "artifact_count": len(exports), "release_authorized": False}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="V3B governed new-topic production")
    commands = result.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    for name in ("request", "sources", "actors", "source-root", "artifact-root", "out"):
        init.add_argument("--" + name, required=True, type=Path)
    for command in ("next", "submit", "advance", "status", "export", "invalidate"):
        sub = commands.add_parser(command)
        sub.add_argument("--run", required=True, type=Path)
        if command in {"next", "advance", "invalidate"}:
            sub.add_argument("--bundle", required=True)
        if command in {"next", "export"}:
            sub.add_argument("--out", required=True, type=Path)
        if command == "submit":
            sub.add_argument("--submission", required=True, type=Path)
        if command == "invalidate":
            sub.add_argument("--from-stage", required=True, choices=STAGES)
            sub.add_argument("--reason", required=True)
            sub.add_argument("--expected-revision", required=True, type=int)
    return result


def main(argv=None, *, expected_subject: str | None = None) -> int:
    args = parser().parse_args(argv)
    store = None
    try:
        if args.command == "init":
            output = initialize(load(args.request), load(args.sources), load(args.actors)["actors"],
                                args.source_root, args.artifact_root, args.out, expected_subject)
        else:
            store = RunStore(args.run)
            require(expected_subject is None or store.metadata()["request"]["subject"] == expected_subject,
                    "WRONG_SUBJECT_KIT")
            output = _run_command(args, store)
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0
    except (ContractError, KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "code": getattr(exc, "code", "INVALID_INPUT"), "detail": str(exc)}))
        return 2
    finally:
        if store is not None:
            store.close()


def _run_command(args, store: RunStore) -> dict:
    if args.command == "status":
        return status(store)
    if args.command == "next":
        output = work_order(store, args.bundle)
        write_json(args.out, output)
        return {"work_order": str(args.out), "stage": output["stage"], "actor": output["actor_instance_id"]}
    if args.command == "submit":
        return accept_submission(store, load(args.submission))
    if args.command == "advance":
        return advance_automatic(store, args.bundle)
    if args.command == "export":
        return export_run(store, args.out)
    index = STAGES.index(args.from_stage)
    require(bool(args.reason.strip()), "INVALIDATION_REASON_REQUIRED")
    return store.invalidate(args.bundle, list(STAGES[index:]), args.reason, args.expected_revision)
