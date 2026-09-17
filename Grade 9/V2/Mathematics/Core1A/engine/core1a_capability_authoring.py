"""Capability-aware Core1A authoring adapter over repository-custodied data.

Mathematics lesson titles/examples are not authored in this executable module.
The former literal corpus is frozen as a non-executable migration source and is
projected through a restricted AST reader into a typed, digested candidate asset
set.  The source is never imported or executed and is never curriculum authority.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path

import jsonschema

import build_math_core1a_textbook as base

HERE = Path(__file__).resolve()
CORE1A = HERE.parent.parent
MATH = CORE1A.parent
BLUEPRINT = MATH / "MathBlueprint"
MANIFEST_PATH = CORE1A / "policies" / "core1a-authoring-source.v1.json"
SCHEMA_PATH = BLUEPRINT / "contracts" / "math-core1a-authoring-assets.schema.json"


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def _fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _assignment(tree: ast.Module, name: str) -> ast.AST:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return node.value
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            return node.value
    _fail("CORE1A_AUTHORING_MIGRATION_SYMBOL_MISSING", name)


def _function_map(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    return {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}


def _literal(node: ast.AST, label: str):
    try:
        return ast.literal_eval(node)
    except Exception as exc:  # pragma: no cover - exact AST failure text is irrelevant
        _fail("CORE1A_AUTHORING_NON_LITERAL_DATA", f"{label}:{exc}")


def _extract_example(call: ast.Call, capability_ref: str, index: int) -> dict:
    if not isinstance(call.func, ast.Name) or call.func.id != "I" or call.keywords or len(call.args) != 4:
        _fail("CORE1A_AUTHORING_UNSAFE_EXAMPLE_EXPRESSION", f"{capability_ref}:{index}")
    prompt = _literal(call.args[0], "prompt")
    steps = _literal(call.args[1], "steps")
    answer = _literal(call.args[2], "answer")
    hints = _literal(call.args[3], "hints")
    if not isinstance(prompt, str) or not isinstance(answer, str):
        _fail("CORE1A_AUTHORING_EXAMPLE_TEXT_INVALID", capability_ref)
    if not isinstance(steps, list) or not steps or not all(isinstance(x, str) and x for x in steps):
        _fail("CORE1A_AUTHORING_EXAMPLE_STEPS_INVALID", capability_ref)
    if not isinstance(hints, list) or len(hints) != 3 or not all(isinstance(x, str) and x for x in hints):
        _fail("CORE1A_AUTHORING_EXAMPLE_HINTS_INVALID", capability_ref)
    material = {"prompt": prompt, "steps": steps, "answer": answer, "hints": hints}
    return {
        "example_id": "MATH-C1A-EX-" + _digest([capability_ref, index, material])[:16].upper(),
        **material,
        "source_class": "AUTHORING_CANDIDATE",
    }


def _extract_bank(function: ast.FunctionDef, capability_ref: str) -> list[dict]:
    returns = [node for node in function.body if isinstance(node, ast.Return)]
    if len(returns) != 1 or not isinstance(returns[0].value, ast.List):
        _fail("CORE1A_AUTHORING_BANK_SHAPE_INVALID", capability_ref)
    return [
        _extract_example(node, capability_ref, index)
        for index, node in enumerate(returns[0].value.elts, 1)
        if isinstance(node, ast.Call)
    ]


def _build_projection(source_text: str, manifest: dict) -> dict:
    tree = ast.parse(source_text, filename=manifest["legacy_source_ref"], mode="exec")
    titles = _literal(_assignment(tree, "CAPABILITY_TITLES"), "CAPABILITY_TITLES")
    custom_node = _assignment(tree, "CUSTOM_BANKS")
    if not isinstance(titles, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in titles.items()):
        _fail("CORE1A_AUTHORING_TITLES_INVALID")
    if not isinstance(custom_node, ast.Dict):
        _fail("CORE1A_AUTHORING_CUSTOM_BANK_MAP_INVALID")
    functions = _function_map(tree)
    custom: dict[str, str] = {}
    for key_node, value_node in zip(custom_node.keys, custom_node.values):
        key = _literal(key_node, "CUSTOM_BANKS.key")
        if not isinstance(key, str) or not isinstance(value_node, ast.Name):
            _fail("CORE1A_AUTHORING_CUSTOM_BANK_MAP_INVALID")
        custom[key] = value_node.id
    if not set(custom).issubset(titles):
        _fail("CORE1A_AUTHORING_CUSTOM_BANK_WITHOUT_TITLE")

    rows = []
    for capability_ref in sorted(titles):
        examples = []
        source = "FAMILY_FALLBACK"
        if capability_ref in custom:
            fn = functions.get(custom[capability_ref])
            if fn is None:
                _fail("CORE1A_AUTHORING_BANK_FUNCTION_MISSING", custom[capability_ref])
            examples = _extract_bank(fn, capability_ref)
            if len(examples) < 6:
                _fail("CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED", capability_ref + ":need_six_instances")
            source = "CUSTOM_MIGRATED"
        rows.append({
            "capability_ref": capability_ref,
            "title": titles[capability_ref],
            "bank_source": source,
            "examples": examples,
        })

    body = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "asset_set_id": "",
        "content_role": "CORE1A_AUTHORING_CANDIDATE",
        "curriculum_authority": False,
        "source_custody": {
            "source_id": manifest["source_id"],
            "legacy_source_ref": manifest["legacy_source_ref"],
            "legacy_source_git_blob_sha": manifest["legacy_source_git_blob_sha"],
            "parser_contract": manifest["parser_contract"],
        },
        "capabilities": rows,
        "asset_set_digest": "",
    }
    identity_material = copy.deepcopy(body)
    identity_material.pop("asset_set_id")
    identity_material.pop("asset_set_digest")
    body["asset_set_id"] = "MATH-CORE1A-AUTHORING-ASSETS-" + _digest(identity_material)[:16].upper()
    body["asset_set_digest"] = _digest({k: v for k, v in body.items() if k != "asset_set_digest"})
    return body


def _verify_source_custody(data: bytes, manifest: dict) -> None:
    actual = _git_blob_sha(data)
    expected = manifest.get("legacy_source_git_blob_sha")
    if actual != expected:
        _fail("CORE1A_AUTHORING_SOURCE_CUSTODY_MISMATCH", f"{actual}!={expected}")


@lru_cache(maxsize=1)
def load_authoring_assets() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("subject") != "MATHEMATICS" or manifest.get("curriculum_authority") is not False:
        _fail("CORE1A_AUTHORING_SOURCE_AUTHORITY_INVALID")
    legacy_path = CORE1A / manifest["legacy_source_ref"]
    data = legacy_path.read_bytes()
    _verify_source_custody(data, manifest)
    projection = _build_projection(data.decode("utf-8"), manifest)
    jsonschema.validate(projection, json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    if projection["asset_set_digest"] != _digest({k: v for k, v in projection.items() if k != "asset_set_digest"}):
        _fail("CORE1A_AUTHORING_ASSET_DIGEST_MISMATCH")
    return projection


AUTHORING_ASSET_SET = load_authoring_assets()
CAPABILITY_TITLES = {row["capability_ref"]: row["title"] for row in AUTHORING_ASSET_SET["capabilities"]}
_ASSET_BY_CAPABILITY = {row["capability_ref"]: row for row in AUTHORING_ASSET_SET["capabilities"]}


def _instances_for(capability_ref: str):
    row = _ASSET_BY_CAPABILITY.get(capability_ref)
    if row is None or row["bank_source"] != "CUSTOM_MIGRATED":
        return []
    return [base.inst(x["prompt"], list(x["steps"]), x["answer"], list(x["hints"])) for x in row["examples"]]


def _bank_factory(capability_ref: str):
    return lambda: _instances_for(capability_ref)


CUSTOM_BANKS = {
    row["capability_ref"]: _bank_factory(row["capability_ref"])
    for row in AUTHORING_ASSET_SET["capabilities"]
    if row["bank_source"] == "CUSTOM_MIGRATED"
}


def capability_bank(capability_ref: str, family_ref: str):
    if capability_ref in CUSTOM_BANKS:
        rows = CUSTOM_BANKS[capability_ref]()
    else:
        rows = base.family_bank(family_ref)
    if len(rows) < 6:
        base.fail("CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED", capability_ref + ":need_six_instances")
    return rows


def choose_asset_for_capability(lesson, assets):
    capability = lesson["capability_ref"]
    candidates = [assets[x] for x in lesson.get("pck_asset_refs", []) if x in assets]
    for asset in candidates:
        if capability in asset.get("capability_refs", []):
            return asset
    return candidates[0] if candidates else None


def authored_lesson(lesson, assets, families):
    family_id = base.choose_family(lesson)
    capability = lesson["capability_ref"]
    asset = choose_asset_for_capability(lesson, assets)
    family = families.get(family_id) if family_id else None
    full = lesson["treatment"] in base.FULL_TREATMENTS

    if full and not family_id:
        base.fail("CORE1A_PROBLEM_FAMILY_REQUIRED", lesson["lesson_id"])
    if full and family_id not in base.FAMILY_BANKS:
        base.fail("CORE1A_FAMILY_GENERATOR_MISSING", family_id or lesson["lesson_id"])

    bank = capability_bank(capability, family_id) if family_id else []
    practice = base.materialize_practice(bank, lesson) if bank else {}
    title = CAPABILITY_TITLES.get(capability, lesson.get("learner_title") or base.humanize_code(capability))

    recognition = []
    if family:
        recognition = [base.sentence(x) for x in family.get("problem_signature", {}).get("recognition_cues", [])]

    ordinary = base.sentence(asset.get("ordinary_language_bridge", "")) if asset else ""
    anchor = base.sentence(asset.get("anchor", "")) if asset else ""
    route = base.public_route(asset, family)

    mistake = ""
    repair = []
    if asset:
        wrong = asset.get("misconception_discriminator", {}).get("candidate_wrong_model", "")
        probe = asset.get("misconception_discriminator", {}).get("probe", "")
        if wrong:
            mistake = base.sentence(wrong) + (" " + base.sentence(probe) if probe else "")
        repair = [base.sentence(x) for x in asset.get("repair_route", [])]
    elif family and family.get("common_invalid_mechanisms"):
        row = family["common_invalid_mechanisms"][0]
        mistake = base.sentence(row.get("invalid_move", "")) + " " + base.sentence(row.get("why_invalid", ""))

    verification = []
    if asset:
        verification.extend(base.sentence(x) for x in asset.get("verification_method", []))
    verification.extend(base.public_phrase(x) for x in lesson.get("verification_requirements", []))
    verification = list(dict.fromkeys(x for x in verification if x))

    return {
        "lesson_id": lesson["lesson_id"],
        "title": title,
        "treatment": lesson["treatment"],
        "family_ref": family_id,
        "opening": ordinary or "Begin by identifying the mathematical roles before calculating.",
        "concept_explanation": anchor or (base.sentence(family.get("problem_signature", {}).get("target_job", "")) if family else ""),
        "what_to_notice": recognition,
        "why_it_works": route,
        "common_mistake": mistake,
        "repair": repair,
        "worked_examples": (
            [
                {"prompt": bank[0].prompt, "steps": list(bank[0].steps), "answer": bank[0].answer},
                {"prompt": bank[1].prompt, "steps": list(bank[1].steps), "answer": bank[1].answer},
            ] if full else []
        ),
        "practice": practice,
        "verification": verification,
        "source_trace": {
            "core1_lesson_ref": lesson["lesson_id"],
            "assessment_question_refs": list(lesson.get("assessment_question_refs", [])),
            "pck_asset_refs": list(lesson.get("pck_asset_refs", [])),
            "authoring_asset_set_id": AUTHORING_ASSET_SET["asset_set_id"],
            "authoring_asset_set_digest": AUTHORING_ASSET_SET["asset_set_digest"],
        },
    }


def install():
    """Install capability-aware authoring into the shared Core1A infrastructure."""
    base.authored_lesson = authored_lesson
    return base
