#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
PHYSICS = ROOT.parent
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from compile_engineering_closure import V3_REGISTRY_REF, compile_closure  # noqa: E402


class MigrationCompilationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str) -> None:
    raise MigrationCompilationError(code, message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_repo_ref(ref: str) -> Path:
    path_part = ref.split("#", 1)[0]
    if not path_part or Path(path_part).is_absolute():
        fail("E_MIG_COMPILE_REF", f"invalid repository reference: {ref}")
    for base in (ROOT, PHYSICS):
        candidate = (base / path_part).resolve()
        if _within(candidate, PHYSICS) and candidate.is_file():
            return candidate
    fail("E_MIG_COMPILE_REF", f"repository reference not found: {ref}")


def normalize_repo_ref(path: Path) -> str:
    path = path.resolve()
    if _within(path, ROOT):
        return path.relative_to(ROOT).as_posix()
    if _within(path, PHYSICS):
        return path.relative_to(PHYSICS).as_posix()
    fail("E_MIG_COMPILE_REF", f"path escapes Physics repository root: {path}")


def resolve_declared_relative(ref: str, anchor: Path) -> Path:
    if not ref or Path(ref).is_absolute():
        fail("E_MIG_COMPILE_REF", f"invalid declared relative reference: {ref}")
    cursor = anchor.parent.resolve()
    while _within(cursor, PHYSICS):
        candidate = (cursor / ref).resolve()
        if _within(candidate, PHYSICS) and candidate.is_file():
            return candidate
        if cursor == PHYSICS:
            break
        cursor = cursor.parent
    fail("E_MIG_COMPILE_REF", f"declared source reference not found from {anchor.name}: {ref}")


def fragment_value(obj: Any, ref: str) -> Any:
    if "#" not in ref:
        fail("E_MIG_COMPILE_FRAGMENT", f"claim reference requires fragment: {ref}")
    fragment = ref.split("#", 1)[1]
    value = obj
    for part in fragment.split("."):
        if not isinstance(value, dict) or part not in value:
            fail("E_MIG_COMPILE_FRAGMENT", f"claim fragment not found: {ref}")
        value = value[part]
    return value


def select_profile(profile_registry: dict, bucket_id: str, prior_knowledge_pct: int) -> tuple[dict, dict]:
    buckets = [row for row in profile_registry.get("buckets", []) if row.get("bucket_id") == bucket_id]
    if len(buckets) != 1:
        fail("E_MIG_COMPILE_PROFILE", f"expected one profile bucket for {bucket_id}, got {len(buckets)}")
    bucket = buckets[0]
    profiles = [row for row in bucket.get("profiles", []) if row.get("prior_knowledge_pct") == prior_knowledge_pct]
    if len(profiles) != 1:
        fail("E_MIG_COMPILE_PROFILE", f"expected one profile for prior_knowledge_pct={prior_knowledge_pct}, got {len(profiles)}")
    return bucket, profiles[0]


def select_transfer_bucket(transfer_registry: dict, bucket_id: str, prior_knowledge_pct: int) -> dict:
    rows = [
        row for row in transfer_registry.get("buckets", [])
        if row.get("bucket_id") == bucket_id and row.get("prior_knowledge_pct") == prior_knowledge_pct
    ]
    if len(rows) != 1:
        fail("E_MIG_COMPILE_TRANSFER", f"expected one transfer bucket for {bucket_id}/{prior_knowledge_pct}, got {len(rows)}")
    return rows[0]


def stage_row(stage: str, state: str, artifact_refs: list[str], evidence_refs: list[str], note: str) -> dict:
    return {
        "stage": stage,
        "evidence_state": state,
        "artifact_refs": artifact_refs,
        "evidence_refs": evidence_refs,
        "notes": [note],
    }


def _hint_coverage_complete(profile: dict, atom_ids: list[str], primary_questions: list[str]) -> bool:
    rows = profile.get("core2_hint_coverage", [])
    if {row.get("question_id") for row in rows} != set(primary_questions):
        return False
    atom_set = set(atom_ids)
    for row in rows:
        rungs = row.get("hint_rungs", [])
        if {r.get("rung") for r in rungs} != {"H1", "H2", "H3"}:
            return False
        if any(r.get("pre_taught") is not True or r.get("core1a_learning_atom") not in atom_set for r in rungs):
            return False
    return True


def _routine_plan_complete(routines: list[dict]) -> bool:
    if not routines:
        return False
    for row in routines:
        if not row.get("method_steps") or not row.get("independent_practice") or not row.get("readiness_checks"):
            return False
        ladder = row.get("hint_ladder", [])
        if {r.get("rung") for r in ladder} != {"H1", "H2", "H3"}:
            return False
    return True


def _apply_stage_receipts(spec: dict, baseline: dict[str, dict], source_refs: set[str]) -> None:
    if not spec.get("stage_evidence_refs"):
        return
    receipt_schema = load_json(ROOT / "contracts" / "core1a-migration-stage-evidence.schema.json")
    rank = {"MISSING": 0, "LEGACY_ONLY": 1, "PARTIAL": 2, "PRESENT": 3}
    seen: set[str] = set()
    for ref in spec["stage_evidence_refs"]:
        path = resolve_repo_ref(ref)
        receipt = load_json(path)
        try:
            jsonschema.validate(receipt, receipt_schema)
        except jsonschema.ValidationError as exc:
            fail("E_MIG_COMPILE_STAGE_RECEIPT_SCHEMA", f"{ref}: {exc.message}")
        if receipt["bucket_id"] != spec["bucket_id"]:
            fail("E_MIG_COMPILE_STAGE_RECEIPT_BUCKET", f"{ref}: {receipt['bucket_id']} != {spec['bucket_id']}")
        stage = receipt["stage"]
        if stage not in baseline:
            fail("E_MIG_COMPILE_STAGE_RECEIPT_STAGE", f"{ref}: unknown stage {stage}")
        if stage in seen:
            fail("E_MIG_COMPILE_STAGE_RECEIPT_DUPLICATE", f"multiple receipts for {stage}")
        seen.add(stage)
        if rank[receipt["evidence_state"]] < rank[baseline[stage]["evidence_state"]]:
            fail("E_MIG_COMPILE_STAGE_RECEIPT_DOWNGRADE", f"{ref}: cannot downgrade {stage}")
        for source_ref in receipt["source_refs"]:
            resolve_repo_ref(source_ref)
            source_refs.add(source_ref)
        source_refs.add(ref)
        baseline[stage] = {
            "stage": stage,
            "evidence_state": receipt["evidence_state"],
            "artifact_refs": receipt["artifact_refs"],
            "evidence_refs": receipt["evidence_refs"],
            "notes": [
                f"Promoted by governed migration evidence receipt {receipt['receipt_id']}."
                + (" Remaining: " + "; ".join(receipt["unresolved_requirements"]) if receipt["unresolved_requirements"] else "")
            ],
        }


def compile_audit_with_facts(spec: dict, *, spec_ref: str) -> tuple[dict, dict]:
    try:
        jsonschema.validate(spec, load_json(ROOT / "contracts" / "core1a-real-bucket-migration-spec.schema.json"))
    except jsonschema.ValidationError as exc:
        fail("E_MIG_COMPILE_SPEC_SCHEMA", exc.message)

    policy = load_json(ROOT / "policy" / "core1a-stage-machine.v1.json")
    stages = policy["pre_manuscript_stages"]

    build_path = resolve_repo_ref(spec["build_manifest_ref"])
    build = load_json(build_path)
    if build.get("bucket_id") != spec["bucket_id"]:
        fail("E_MIG_COMPILE_BUCKET", f"build manifest bucket {build.get('bucket_id')} != {spec['bucket_id']}")

    claim_path = resolve_repo_ref(spec["legacy_claim_ref"])
    if claim_path != build_path:
        fail("E_MIG_COMPILE_LEGACY_BINDING", "legacy claim must bind the declared build manifest")
    legacy_status = fragment_value(build, spec["legacy_claim_ref"])

    learner_profile = build.get("learner_profile") or {}
    prior = learner_profile.get("prior_knowledge_pct")
    if not isinstance(prior, int):
        fail("E_MIG_COMPILE_PROFILE", "build manifest learner_profile.prior_knowledge_pct is required")

    source_inputs = build.get("source_inputs") or {}
    if "profile_registry" not in source_inputs or "transfer_registry" not in source_inputs:
        fail("E_MIG_COMPILE_SOURCE_BINDING", "build manifest must declare profile_registry and transfer_registry")

    resolved_inputs = {name: resolve_declared_relative(ref, build_path) for name, ref in source_inputs.items()}
    profile_path = resolved_inputs["profile_registry"]
    transfer_path = resolved_inputs["transfer_registry"]
    profile_ref = normalize_repo_ref(profile_path)
    transfer_ref = normalize_repo_ref(transfer_path)
    profile_registry = load_json(profile_path)
    transfer_registry = load_json(transfer_path)
    _, profile = select_profile(profile_registry, spec["bucket_id"], prior)
    transfer_bucket = select_transfer_bucket(transfer_registry, spec["bucket_id"], prior)

    atom_ids = [row["atom_id"] for row in profile.get("learning_atoms", [])]
    if not atom_ids or len(set(atom_ids)) != len(atom_ids):
        fail("E_MIG_COMPILE_ATOMS", "learning atoms must be nonempty and unique")
    if set(build.get("learning_atoms", [])) != set(atom_ids):
        fail("E_MIG_COMPILE_ATOMS", "build manifest learning_atoms drift from selected profile")

    routine_ids = [row["routine_id"] for row in transfer_bucket.get("transfer_routines", [])]
    if set(build.get("transfer_routines", [])) != set(routine_ids):
        fail("E_MIG_COMPILE_TRANSFER", "build manifest transfer_routines drift from transfer registry")
    routines = transfer_bucket.get("transfer_routines", [])

    primary_questions = list(build.get("primary_questions", []))
    releases = {row["question_id"]: row for row in build.get("question_release", [])}
    if set(releases) != set(primary_questions):
        fail("E_MIG_COMPILE_RELEASE", "question_release must exactly cover primary_questions")
    routine_questions = {qid for row in routines for qid in row.get("core2_questions", [])}
    if routine_questions != set(primary_questions):
        fail("E_MIG_COMPILE_TRANSFER", "transfer routines must exactly cover primary_questions")
    held_rows = [releases[qid] for qid in primary_questions if releases[qid].get("status") == "HELD"]
    for row in held_rows:
        if not row.get("release_prerequisite_buckets"):
            fail("E_MIG_COMPILE_RELEASE", f"held question {row['question_id']} lacks release prerequisite buckets")

    request_path = resolve_repo_ref(spec["engineering_request_ref"])
    engineering_manifest_path = resolve_repo_ref(spec["engineering_manifest_ref"])
    request = load_json(request_path)
    engineering_manifest = load_json(engineering_manifest_path)
    if request.get("request_id") != engineering_manifest.get("request_id"):
        fail("E_MIG_COMPILE_ENGINEERING_BINDING", "engineering request_id and manifest request_id differ")
    if engineering_manifest.get("scope_kind") != "BUCKET" or engineering_manifest.get("scope_ref") != spec["bucket_id"]:
        fail("E_MIG_COMPILE_ENGINEERING_SCOPE", "engineering manifest must bind the migration bucket")
    if engineering_manifest.get("registry_ref") != V3_REGISTRY_REF:
        fail("E_MIG_COMPILE_ENGINEERING_REGISTRY", "migration must consume canonical v3 Engineering registry")

    receipt = compile_closure(request, engineering_manifest)
    registry = build_registry()
    gate_map = {row["subtopic_id"]: row for row in registry["gates"]}
    direct_gate_ids = list(receipt["direct_gate_ids"])
    direct_gates = [gate_map[gid] for gid in direct_gate_ids]

    all_reasoning = bool(direct_gates) and all(row.get("reasoning_sequence") for row in direct_gates)
    all_representations = bool(direct_gates) and all(row.get("representations") for row in direct_gates)
    all_relations = bool(direct_gates) and all(row.get("relations") for row in direct_gates)
    all_gate_misconceptions = bool(direct_gates) and all(row.get("misconceptions") for row in direct_gates)
    all_atom_teaching_moves = all(row.get("teaching_moves") for row in profile.get("learning_atoms", []))
    all_atom_misconceptions = all(row.get("misconceptions") for row in profile.get("learning_atoms", []))
    hint_complete = _hint_coverage_complete(profile, atom_ids, primary_questions)
    routine_plan_complete = _routine_plan_complete(routines)
    macro_order = set((build.get("publication_plan") or {}).get("macro_order", []))
    fading_macro_present = {"WATCH_ONE", "COMPLETE_ONE", "INDEPENDENT_PRACTICE"}.issubset(macro_order)
    high_fragility_steps = [
        f"{gate['subtopic_id']}:{step['step_id']}"
        for gate in direct_gates
        for step in gate.get("reasoning_sequence", [])
        if step.get("inferential_jump") == "HIGH_FRAGILITY"
    ]

    registry_ref = receipt["registry_ref"]
    reasoning_refs = [f"{registry_ref}#{gid}.reasoning_sequence" for gid in direct_gate_ids]
    representation_refs = [f"{registry_ref}#{gid}.representations" for gid in direct_gate_ids]
    misconception_refs = [f"{registry_ref}#{gid}.misconceptions" for gid in direct_gate_ids]

    baseline: dict[str, dict] = {}
    if "intrinsic_difficulty" in learner_profile and "prior_knowledge_pct" in learner_profile:
        baseline[stages[0]] = stage_row(
            stages[0], "LEGACY_ONLY", [spec["build_manifest_ref"]],
            [f"{spec['build_manifest_ref']}#learner_profile", f"{profile_ref}#policy"],
            "Legacy learner-profile routing and categorical difficulty exist, but they do not constitute the current intrinsic SDU design-state/gap receipt.",
        )
    else:
        baseline[stages[0]] = stage_row(stages[0], "MISSING", [], [], "No governed learner-state gap evidence is bound.")

    baseline[stages[1]] = stage_row(
        stages[1], "PRESENT", atom_ids,
        [f"{profile_ref}#buckets[{spec['bucket_id']}].profiles[{prior}].learning_atoms"],
        "Repository-backed learning atoms exactly match the build manifest namespace.",
    )
    baseline[stages[2]] = stage_row(
        stages[2], "PARTIAL" if all_reasoning else "MISSING",
        direct_gate_ids if all_reasoning else [], reasoning_refs if all_reasoning else [],
        "Canonical Engineering Gates expose dependency-aware reasoning and fragility, but no Core1A atom-by-atom novice omission closure receipt exists." if all_reasoning else "No complete technical reasoning sequence is available for every direct gate.",
    )
    baseline[stages[3]] = stage_row(
        stages[3], "PARTIAL" if all_atom_teaching_moves else "MISSING",
        atom_ids if all_atom_teaching_moves else [],
        [f"{profile_ref}#learning_atoms[*].teaching_moves"] if all_atom_teaching_moves else [],
        "Teaching moves exist, but they are not a governed jump-by-jump novice-to-expert cognitive transformation receipt." if all_atom_teaching_moves else "Learning-atom teaching moves are incomplete.",
    )
    baseline[stages[4]] = stage_row(
        stages[4], "PARTIAL" if all_representations else "MISSING",
        direct_gate_ids if all_representations else [], representation_refs if all_representations else [],
        "Canonical technical representation requirements exist, but Core1A still needs an atom/jump pedagogical noticing-and-purpose binding." if all_representations else "Direct-gate representation requirements are incomplete.",
    )
    baseline[stages[5]] = stage_row(
        stages[5], "MISSING", [], [],
        "No governed Core1A pedagogical representation-candidate set with rejected alternatives is bound.",
    )
    baseline[stages[6]] = stage_row(
        stages[6], "MISSING", [], [],
        "No governed Core1A primary/secondary representation decision receipt is bound.",
    )
    bridge_ready = all_atom_teaching_moves and all_representations and all_relations
    baseline[stages[7]] = stage_row(
        stages[7], "PARTIAL" if bridge_ready else "MISSING",
        atom_ids if bridge_ready else [],
        ([f"{profile_ref}#learning_atoms[*].teaching_moves"] + representation_refs) if bridge_ready else [],
        "Picture/component/equation ingredients exist, but no full picture-to-word-to-symbol-to-equation bridge receipt closes every relevant atom." if bridge_ready else "Bridge ingredients are incomplete.",
    )
    misconception_ready = all_atom_misconceptions and all_gate_misconceptions
    baseline[stages[8]] = stage_row(
        stages[8], "PRESENT" if misconception_ready else ("PARTIAL" if all_atom_misconceptions else "MISSING"),
        atom_ids if all_atom_misconceptions else [],
        ([f"{profile_ref}#learning_atoms[*].misconceptions"] + misconception_refs) if all_atom_misconceptions else [],
        "Every learning atom declares misconceptions and the direct Engineering Gates provide governed counterexample/repair requirements." if misconception_ready else "Misconception evidence exists but governed technical repair coverage is incomplete.",
    )
    plan_ready = routine_plan_complete and fading_macro_present
    baseline[stages[9]] = stage_row(
        stages[9], "PARTIAL" if plan_ready else "MISSING",
        routine_ids if plan_ready else [],
        [f"{transfer_ref}#bucket[{spec['bucket_id']}].transfer_routines", f"{spec['build_manifest_ref']}#publication_plan.macro_order"] if plan_ready else [],
        "Worked/guided/independent structure, hint ladders and readiness checks exist, but no governed worked-to-faded example lineage/fingerprint receipt proves the transformation." if plan_ready else "Worked/faded/independent planning evidence is incomplete.",
    )
    baseline[stages[10]] = stage_row(
        stages[10], "PRESENT" if hint_complete else ("PARTIAL" if profile.get("core2_hint_coverage") else "MISSING"),
        primary_questions if profile.get("core2_hint_coverage") else [],
        [f"{profile_ref}#core2_hint_coverage", f"{spec['build_manifest_ref']}#question_release"] if profile.get("core2_hint_coverage") else [],
        "Every primary Core2 question has exact H1/H2/H3 preteach trace to a repository learning atom; held transfers remain explicit in the build manifest." if hint_complete else "Core2 hint/preteach coverage is incomplete.",
    )
    baseline[stages[11]] = stage_row(
        stages[11], "PARTIAL" if all_reasoning else "MISSING",
        direct_gate_ids if all_reasoning else [], reasoning_refs if all_reasoning else [],
        f"The technical jump inventory is governed and exposes {len(high_fragility_steps)} HIGH_FRAGILITY step(s), but no Core1A unresolved-required-jump closure receipt proves the remaining count is zero." if all_reasoning else "No complete governed jump inventory is available.",
    )

    source_refs: set[str] = {spec_ref, spec["build_manifest_ref"], spec["engineering_request_ref"], spec["engineering_manifest_ref"]}
    source_refs.update(normalize_repo_ref(path) for path in resolved_inputs.values())
    _apply_stage_receipts(spec, baseline, source_refs)

    ordered_rows = [baseline[stage] for stage in stages]
    incomplete = [row for row in ordered_rows if row["evidence_state"] != "PRESENT"]
    technical_ready = receipt["closure_status"] == "READY"
    release_authorized = technical_ready and not incomplete and not held_rows

    block_reasons: list[str] = []
    if not technical_ready:
        block_reasons.append("TECHNICAL_GATE_INCOMPLETE")
    for row in ordered_rows:
        if row["evidence_state"] in {"LEGACY_ONLY", "MISSING"}:
            block_reasons.append(f"{row['evidence_state']}_STAGE_EVIDENCE:{row['stage']}")
    partials = [row["stage"] for row in ordered_rows if row["evidence_state"] == "PARTIAL"]
    if partials:
        block_reasons.append("PARTIAL_STAGE_EVIDENCE:" + ",".join(partials))
    for row in held_rows:
        block_reasons.append(
            "DOWNSTREAM_TRANSFER_HOLD:"
            + row["question_id"]
            + ":requires="
            + ",".join(row["release_prerequisite_buckets"])
        )

    audit = {
        "schema_version": "2.0.0",
        "audit_id": spec["audit_id"],
        "migration_spec_ref": spec_ref,
        "bucket_id": spec["bucket_id"],
        "source_refs": sorted(source_refs),
        "legacy_claim": {
            "status": legacy_status,
            "claim_ref": spec["legacy_claim_ref"],
            "accepted_as_v9_release_evidence": False,
        },
        "technical_gate_audit": {
            "engineering_request_ref": spec["engineering_request_ref"],
            "engineering_manifest_ref": spec["engineering_manifest_ref"],
            "registry_ref": receipt["registry_ref"],
            "direct_gate_ids": list(receipt["direct_gate_ids"]),
            "closure_gate_ids": list(receipt["transitive_gate_ids"]),
            "status": "READY" if technical_ready else "INCOMPLETE",
        },
        "stage_audit": ordered_rows,
        "release_authorized": release_authorized,
        "block_reasons": block_reasons,
    }
    facts = {
        "engineering_receipt": receipt,
        "held_questions": [row["question_id"] for row in held_rows],
        "high_fragility_step_refs": high_fragility_steps,
        "learning_atom_ids": atom_ids,
        "transfer_routine_ids": routine_ids,
        "primary_question_ids": primary_questions,
        "profile_ref": profile_ref,
        "transfer_ref": transfer_ref,
    }
    return audit, facts


def compile_audit(spec: dict, *, spec_ref: str) -> dict:
    return compile_audit_with_facts(spec, spec_ref=spec_ref)[0]


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile a real Core1A bucket migration audit from governed repository data")
    ap.add_argument("spec", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    spec_path = args.spec.resolve()
    if not spec_path.is_file():
        fail("E_MIG_COMPILE_SPEC", f"spec not found: {args.spec}")
    spec_ref = normalize_repo_ref(spec_path)
    audit = compile_audit(load_json(spec_path), spec_ref=spec_ref)
    jsonschema.validate(audit, load_json(ROOT / "contracts" / "core1a-real-bucket-migration-audit.schema.json"))
    rendered = json.dumps(audit, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
