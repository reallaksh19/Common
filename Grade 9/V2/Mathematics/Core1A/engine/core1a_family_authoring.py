"""Restricted data projection for migrated Core1A problem-family authoring assets."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve()
CORE1A = HERE.parent.parent
MATH = CORE1A.parent
BLUEPRINT = MATH / "MathBlueprint"
MANIFEST_PATH = CORE1A / "policies" / "core1a-family-authoring-source.v1.json"
SCHEMA_PATH = BLUEPRINT / "contracts" / "math-core1a-family-authoring-assets.schema.json"


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
    _fail("CORE1A_FAMILY_AUTHORING_MIGRATION_SYMBOL_MISSING", name)


def _function_map(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    return {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}


def _literal(node: ast.AST, label: str):
    try:
        return ast.literal_eval(node)
    except Exception as exc:
        _fail("CORE1A_FAMILY_AUTHORING_NON_LITERAL_DATA", f"{label}:{exc}")


def _extract_example(call: ast.Call, family_ref: str, index: int) -> dict:
    if not isinstance(call.func, ast.Name) or call.func.id != "inst" or call.keywords or len(call.args) != 4:
        _fail("CORE1A_FAMILY_AUTHORING_UNSAFE_EXAMPLE_EXPRESSION", f"{family_ref}:{index}")
    prompt = _literal(call.args[0], "prompt")
    steps = _literal(call.args[1], "steps")
    answer = _literal(call.args[2], "answer")
    hints = _literal(call.args[3], "hints")
    if not isinstance(prompt, str) or not isinstance(answer, str):
        _fail("CORE1A_FAMILY_AUTHORING_EXAMPLE_TEXT_INVALID", family_ref)
    if not isinstance(steps, list) or not steps or not all(isinstance(x, str) and x for x in steps):
        _fail("CORE1A_FAMILY_AUTHORING_EXAMPLE_STEPS_INVALID", family_ref)
    if not isinstance(hints, list) or len(hints) != 3 or not all(isinstance(x, str) and x for x in hints):
        _fail("CORE1A_FAMILY_AUTHORING_EXAMPLE_HINTS_INVALID", family_ref)
    material = {"prompt": prompt, "steps": steps, "answer": answer, "hints": hints}
    return {
        "example_id": "MATH-C1A-FAM-EX-" + _digest([family_ref, index, material])[:16].upper(),
        **material,
        "source_class": "AUTHORING_CANDIDATE",
    }


def _extract_bank(function: ast.FunctionDef, family_ref: str) -> list[dict]:
    returns = [node for node in function.body if isinstance(node, ast.Return)]
    if len(returns) != 1 or not isinstance(returns[0].value, ast.List):
        _fail("CORE1A_FAMILY_AUTHORING_BANK_SHAPE_INVALID", family_ref)
    rows = []
    for index, node in enumerate(returns[0].value.elts, 1):
        if not isinstance(node, ast.Call):
            _fail("CORE1A_FAMILY_AUTHORING_BANK_SHAPE_INVALID", family_ref)
        rows.append(_extract_example(node, family_ref, index))
    return rows


def _build_projection(source_text: str, manifest: dict) -> dict:
    tree = ast.parse(source_text, filename=manifest["legacy_source_ref"], mode="exec")
    family_node = _assignment(tree, "FAMILY_BANKS")
    titles = _literal(_assignment(tree, "DISPLAY_TITLES"), "DISPLAY_TITLES")
    extra_node = _assignment(tree, "EXTRA_INSTANCES")
    if not isinstance(family_node, ast.Dict) or not isinstance(extra_node, ast.Dict):
        _fail("CORE1A_FAMILY_AUTHORING_MAP_INVALID")
    if not isinstance(titles, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in titles.items()):
        _fail("CORE1A_FAMILY_AUTHORING_TITLES_INVALID")
    functions = _function_map(tree)
    function_by_family: dict[str, str] = {}
    for key_node, value_node in zip(family_node.keys, family_node.values):
        key = _literal(key_node, "FAMILY_BANKS.key")
        if not isinstance(key, str) or not isinstance(value_node, ast.Name):
            _fail("CORE1A_FAMILY_AUTHORING_MAP_INVALID")
        function_by_family[key] = value_node.id
    extras: dict[str, ast.Call] = {}
    for key_node, value_node in zip(extra_node.keys, extra_node.values):
        key = _literal(key_node, "EXTRA_INSTANCES.key")
        if not isinstance(key, str) or not isinstance(value_node, ast.Call):
            _fail("CORE1A_FAMILY_AUTHORING_EXTRA_INVALID")
        extras[key] = value_node
    if set(function_by_family) != set(titles):
        _fail("CORE1A_FAMILY_AUTHORING_TITLE_COVERAGE_DRIFT")
    if not set(extras).issubset(function_by_family):
        _fail("CORE1A_FAMILY_AUTHORING_EXTRA_UNKNOWN_FAMILY")

    rows = []
    for family_ref in sorted(function_by_family):
        fn = functions.get(function_by_family[family_ref])
        if fn is None:
            _fail("CORE1A_FAMILY_AUTHORING_BANK_FUNCTION_MISSING", function_by_family[family_ref])
        examples = _extract_bank(fn, family_ref)
        if family_ref in extras:
            examples.append(_extract_example(extras[family_ref], family_ref, len(examples) + 1))
        if len(examples) < 6:
            _fail("CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED", family_ref + ":need_six_distinct_instances")
        rows.append({"family_ref": family_ref, "title": titles[family_ref], "examples": examples})

    body = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "asset_set_id": "",
        "content_role": "CORE1A_FAMILY_AUTHORING_CANDIDATE",
        "curriculum_authority": False,
        "source_custody": {
            "source_id": manifest["source_id"],
            "legacy_source_ref": manifest["legacy_source_ref"],
            "legacy_source_git_blob_sha": manifest["legacy_source_git_blob_sha"],
            "parser_contract": manifest["parser_contract"],
        },
        "families": rows,
        "asset_set_digest": "",
    }
    identity = copy.deepcopy(body)
    identity.pop("asset_set_id")
    identity.pop("asset_set_digest")
    body["asset_set_id"] = "MATH-CORE1A-FAMILY-AUTHORING-ASSETS-" + _digest(identity)[:16].upper()
    body["asset_set_digest"] = _digest({k: v for k, v in body.items() if k != "asset_set_digest"})
    return body


def _verify_source_custody(data: bytes, manifest: dict) -> None:
    actual = _git_blob_sha(data)
    expected = manifest.get("legacy_source_git_blob_sha")
    if actual != expected:
        _fail("CORE1A_FAMILY_AUTHORING_SOURCE_CUSTODY_MISMATCH", f"{actual}!={expected}")


@lru_cache(maxsize=1)
def load_family_authoring_assets() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("subject") != "MATHEMATICS" or manifest.get("curriculum_authority") is not False:
        _fail("CORE1A_FAMILY_AUTHORING_SOURCE_AUTHORITY_INVALID")
    source_path = CORE1A / manifest["legacy_source_ref"]
    data = source_path.read_bytes()
    _verify_source_custody(data, manifest)
    projection = _build_projection(data.decode("utf-8"), manifest)
    jsonschema.validate(projection, json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    if projection["asset_set_digest"] != _digest({k: v for k, v in projection.items() if k != "asset_set_digest"}):
        _fail("CORE1A_FAMILY_AUTHORING_ASSET_DIGEST_MISMATCH")
    return projection
