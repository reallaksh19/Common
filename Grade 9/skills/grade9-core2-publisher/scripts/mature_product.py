#!/usr/bin/env python3
"""Mature learner-product gate for Core (2).

Engineering replays may continue to exercise the deterministic auto-authoring
path.  A mature learner product is different: its learning design and learner
semantic model are authored inputs, are bound to the frozen Core (1) package,
and every material learner item must state which learning capability it serves.

This module deliberately contains no subject research and no rendering logic.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path
from typing import Callable


MATURE_MODE = "MATURE_LEARNER_PRODUCT"
ENGINEERING_MODE = "ENGINEERING_REPLAY"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def arg_value(argv: list[str], name: str) -> str | None:
    if name not in argv:
        return None
    i = argv.index(name)
    if i + 1 >= len(argv):
        raise SystemExit(f"{name} requires a value")
    return argv[i + 1]


def remove_pair(argv: list[str], name: str) -> list[str]:
    out = list(argv)
    while name in out:
        i = out.index(name)
        if i + 1 >= len(out):
            raise SystemExit(f"{name} requires a value")
        del out[i:i + 2]
    return out


def remove_flag(argv: list[str], name: str) -> list[str]:
    return [x for x in argv if x != name]


def cleaned_publisher_argv(argv: list[str]) -> list[str]:
    out = list(argv)
    for name in ("--learning-design", "--study-model"):
        out = remove_pair(out, name)
    return remove_flag(out, "--mature-product")


def mature_requested(argv: list[str], design: dict | None) -> bool:
    return "--mature-product" in argv or (design or {}).get("mode") == MATURE_MODE


def preflight_errors(argv: list[str], target: dict, design: dict | None) -> list[str]:
    errors: list[str] = []
    mature = mature_requested(argv, design)
    explicit_flag = "--mature-product" in argv

    if explicit_flag and design is not None and design.get("mode") != MATURE_MODE:
        errors.append("--mature-product requires LearningDesign.mode=MATURE_LEARNER_PRODUCT")

    if not mature:
        return errors

    if design is None:
        errors.append("mature product requires --learning-design")
        return errors

    requested = target.get("requested_products", {})
    if requested.get("study_guide"):
        if not arg_value(argv, "--study-model"):
            errors.append("mature Study Guide requires authored --study-model")
        if not arg_value(argv, "--publication-structure"):
            errors.append("mature Study Guide requires authored --publication-structure")
    if requested.get("transfer_book") and not arg_value(argv, "--transfer-model"):
        errors.append("mature Transfer Book requires authored --transfer-model")
    return errors


def _learning_checker() -> object:
    contracts = Path(__file__).resolve().parents[2] / "architecture" / "core2" / "contracts" / "v1"
    path = contracts / "check_learning_design.py"
    spec = importlib.util.spec_from_file_location("core2_check_learning_design", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_learning_design_contract(design: dict) -> list[str]:
    try:
        checker = _learning_checker()
        errors = list(checker.validate_schema(design))
        errors.extend(checker.validate_semantics(design))
        return errors
    except Exception as exc:
        return [f"LearningDesign validator could not run: {exc}"]


def _plan_unit_map(plan: dict) -> dict[str, dict]:
    return {row["concept_id"]: row for row in plan.get("sections", [])}


def _design_unit_map(design: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for unit in design.get("learning_units", []):
        for cid in unit.get("concept_ids", []):
            if cid in out:
                # Duplicate ownership is surfaced later by binding_errors.
                continue
            out[cid] = unit
    return out


def learning_design_binding_errors(design: dict, plan: dict) -> list[str]:
    errors: list[str] = []
    for key in (
        "publication_plan_id",
        "research_bundle_id",
        "research_package_digest",
        "learner_profile_id",
        "publication_target_id",
        "subject",
        "topic_id",
    ):
        if design.get(key) != plan.get(key):
            errors.append(f"LearningDesign binding drift: {key}")

    plan_units = _plan_unit_map(plan)
    design_units = _design_unit_map(design)
    if set(plan_units) != set(design_units):
        missing = sorted(set(plan_units) - set(design_units))
        extra = sorted(set(design_units) - set(plan_units))
        if missing:
            errors.append("LearningDesign missing planned concepts: " + ", ".join(missing))
        if extra:
            errors.append("LearningDesign contains unplanned concepts: " + ", ".join(extra))

    seen: set[str] = set()
    duplicate: set[str] = set()
    for unit in design.get("learning_units", []):
        for cid in unit.get("concept_ids", []):
            if cid in seen:
                duplicate.add(cid)
            seen.add(cid)
    if duplicate:
        errors.append("LearningDesign concept owned by multiple units: " + ", ".join(sorted(duplicate)))

    for cid in sorted(set(plan_units) & set(design_units)):
        expected = plan_units[cid].get("instructional_profile")
        actual = design_units[cid].get("instructional_profile")
        if actual != expected:
            errors.append(f"{cid}: LearningDesign instructional_profile {actual!r} != PublicationPlan {expected!r}")
    return errors


def capability_index(design: dict) -> tuple[dict[str, dict], set[str]]:
    capabilities: dict[str, dict] = {}
    required: set[str] = set()
    for unit in design.get("learning_units", []):
        for cap in unit.get("learner_capabilities", []):
            cid = cap.get("capability_id")
            if not cid:
                continue
            capabilities[cid] = cap
            if cap.get("required") is True:
                required.add(cid)
    return capabilities, required


def _iter_material_items(study: dict):
    for section in study.get("main_sections", []):
        for item in section.get("items", []):
            if item.get("traceability_class") == "MATERIAL":
                yield f"main_sections/{section.get('section_id')}", item
    for key in ("appendix_A", "appendix_B", "appendix_C"):
        for item in study.get(key, {}).get("items", []):
            if item.get("traceability_class") == "MATERIAL":
                yield key, item


def study_learning_binding_errors(study: dict, plan: dict, design: dict) -> list[str]:
    errors: list[str] = []
    if study.get("publication_plan_id") != plan.get("publication_plan_id"):
        errors.append("StudyGuide publication_plan_id does not match PublicationPlan")
    ident = study.get("product_identity", {})
    if ident.get("delivery_contract") != plan.get("delivery_contract"):
        errors.append("StudyGuide delivery_contract does not match PublicationPlan")
    if ident.get("role") != "CORE_STUDY_GUIDE":
        errors.append("authored StudyGuide product_identity.role must be CORE_STUDY_GUIDE")

    planned = _plan_unit_map(plan)
    sections = {row.get("concept_id"): row for row in study.get("main_sections", []) if row.get("concept_id")}
    if set(sections) != set(planned):
        missing = sorted(set(planned) - set(sections))
        extra = sorted(set(sections) - set(planned))
        if missing:
            errors.append("StudyGuide missing planned concepts: " + ", ".join(missing))
        if extra:
            errors.append("StudyGuide contains unplanned concepts: " + ", ".join(extra))
    for cid in sorted(set(planned) & set(sections)):
        if sections[cid].get("instructional_profile") != planned[cid].get("instructional_profile"):
            errors.append(f"{cid}: StudyGuide instructional_profile does not match PublicationPlan")

    capabilities, required = capability_index(design)
    used: set[str] = set()
    for location, item in _iter_material_items(study):
        refs = item.get("learning_design_refs") or []
        iid = item.get("item_id", "<unknown>")
        if not refs:
            errors.append(f"{location}/{iid}: MATERIAL item requires learning_design_refs in mature mode")
            continue
        unknown = sorted(set(refs) - set(capabilities))
        if unknown:
            errors.append(f"{location}/{iid}: unknown learning_design_refs: {', '.join(unknown)}")
        used.update(set(refs) & set(capabilities))

    uncovered = sorted(required - used)
    if uncovered:
        errors.append("required LearningDesign capabilities have no MATERIAL implementation: " + ", ".join(uncovered))
    return errors


def make_study_builder(
    authored_study: dict,
    design: dict,
    contracts: Path,
    legacy: object,
) -> Callable[[dict, dict], dict]:
    """Return a drop-in build_study_model replacement for mature mode."""

    def build(bundle: dict, plan: dict) -> dict:
        legacy.validate_schema("study-guide.schema.json", authored_study, contracts)
        errors = learning_design_binding_errors(design, plan)
        errors.extend(study_learning_binding_errors(authored_study, plan, design))
        if errors:
            print("CORE2_MATURE_LEARNING_DESIGN_BINDING = FAIL")
            for error in errors:
                print("- " + error)
            raise SystemExit(2)
        print("CORE2_MATURE_LEARNING_DESIGN_BINDING = PASS")
        return copy.deepcopy(authored_study)

    return build


def finalize_learning_design(
    original_argv: list[str],
    design: dict,
    contracts: Path,
    legacy: object,
) -> list[str]:
    """Bind LearningDesign into the exact Core2 publication package."""
    out_value = arg_value(original_argv, "--out")
    prefix = arg_value(original_argv, "--prefix")
    if not out_value or not prefix:
        return ["cannot finalize LearningDesign without --out and --prefix"]
    out = Path(out_value)
    plan_path = out / f"{prefix}_Core2_Publication_Plan.json"
    manifest_path = out / f"{prefix}_Core2_Publication_Manifest.json"
    if not plan_path.exists() or not manifest_path.exists():
        return ["publisher did not emit PublicationPlan/PublicationManifest"]

    plan = load(plan_path)
    errors = learning_design_binding_errors(design, plan)
    if errors:
        return errors

    design_path = out / f"{prefix}_Core2_Learning_Design.json"
    legacy.write_json(design_path, design)
    manifest = load(manifest_path)
    artifacts = [x for x in manifest.get("artifacts", []) if x.get("role") != "LEARNING_DESIGN"]
    artifacts.append(legacy.artifact("LEARNING_DESIGN", design_path))
    manifest["artifacts"] = artifacts
    manifest["package_digest"] = legacy.package_digest(artifacts)
    legacy.validate_schema("publication-manifest.schema.json", manifest, contracts)
    legacy.write_json(manifest_path, manifest)
    print("LEARNING_DESIGN_PACKAGE_BINDING = PASS")
    return []


def print_errors(label: str, errors: list[str]) -> int:
    print(label + " = FAIL")
    for error in errors:
        print("- " + error)
    return 2
