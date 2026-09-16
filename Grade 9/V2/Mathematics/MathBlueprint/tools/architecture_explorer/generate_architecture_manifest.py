#!/usr/bin/env python3
"""Blueprint Architecture Explorer - Derived Observation Manifest Generator.

Scans Mathematics V2 Blueprint contracts, policies, engines, tests, workflows,
and normative documents to generate a derived, non-authoritative observation manifest.
No hardcoded architecture diagrams or topic-specific branches are used.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

BLUEPRINT_ROOT = Path(__file__).resolve().parents[2]


def _digest(data: Any) -> str:
    serialized = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _classify_authority(name: str, path: str) -> str:
    lower = name.lower()
    if "discovery" in lower:
        return "NON_AUTHORITATIVE_DISCOVERY"
    if "engineering" in lower or "gate" in lower:
        return "ENGINEERING_GATE_AUTHORITY"
    if "ground-truth" in lower:
        return "GROUND_TRUTH"
    if "routing" in lower or "route" in lower or "core0" in lower:
        return "CORE0_ROUTING"
    if "canonical-domain" in lower or "domain-projection" in lower or "registry" in lower:
        return "CANONICAL_DOMAIN_REGISTRY"
    if "research" in lower or "pedagogy" in lower:
        return "PEDAGOGY_RESEARCH"
    if "sdu" in lower or "intrinsic" in lower:
        return "SDU_STUDY_DIFFERENTIATION"
    if "lau" in lower or "learner-knowledge" in lower or "waiver" in lower or "learner-capability" in lower:
        return "LAU_LEARNER_ADAPTATION"
    if "governance" in lower or "coverage" in lower or "similarity" in lower or "receipt" in lower:
        return "PRODUCT_GOVERNANCE"
    if "publication" in lower or "render" in lower or "blueprint_pdf" in lower or "page-blueprint" in lower:
        return "PUBLICATION_RENDERING"
    if "visibility" in lower or "passport" in lower or "explorer" in lower:
        return "DERIVED_OBSERVABILITY"
    if "core1" in lower or "assimilation" in lower:
        return "CORE1_SEMANTICS"
    if "core2" in lower:
        return "CORE2_ASSESSMENT"
    if "self-teaching" in lower or "dual-track" in lower:
        return "PEDAGOGICAL_CONTRACTS"
    return "GENERIC_BLUEPRINT_ORCHESTRATION"


def scan_components(root: Path = BLUEPRINT_ROOT) -> dict[str, Any]:
    components: dict[str, dict[str, Any]] = {}
    relations: list[dict[str, Any]] = []

    contracts_dir = root / "contracts"
    policies_dir = root / "policies"
    engine_dir = root / "engine"
    tests_dir = root / "tests"

    # 1. Discover schemas
    if contracts_dir.exists():
        for path in sorted(contracts_dir.glob("*.schema.json")):
            comp_id = f"schema:{path.name}"
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                title = data.get("title", path.stem)
                version = data.get("properties", {}).get("schema_version", {}).get("const", "1.0.0")
            except Exception:
                title = path.stem
                version = "UNKNOWN"
            components[comp_id] = {
                "component_id": comp_id,
                "name": path.name,
                "path": str(path.relative_to(root)).replace("\\", "/"),
                "component_type": "SCHEMA",
                "schema_version": version,
                "title": title,
                "authority_domain": _classify_authority(path.name, str(path)),
                "maturity_observation": "PRODUCTION" if not path.name.startswith("test-") else "TEST_FIXTURE",
                "producer_refs": [],
                "validator_refs": [],
                "consumer_refs": [],
                "policy_refs": [],
                "test_refs": [],
                "documentation_refs": [],
            }

    # 2. Discover policies
    if policies_dir.exists():
        for path in sorted(policies_dir.glob("*.json")):
            comp_id = f"policy:{path.name}"
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                policy_id = (
                    data.get("policy_id")
                    or data.get("registry_id")
                    or data.get("catalog_id")
                    or data.get("crosswalk_id")
                    or path.stem
                )
                version = data.get("schema_version", "1.0.0")
            except Exception:
                policy_id = path.stem
                version = "UNKNOWN"
            components[comp_id] = {
                "component_id": comp_id,
                "name": path.name,
                "path": str(path.relative_to(root)).replace("\\", "/"),
                "component_type": "POLICY",
                "schema_version": version,
                "title": str(policy_id),
                "authority_domain": _classify_authority(path.name, str(path)),
                "maturity_observation": "PRODUCTION",
                "producer_refs": [],
                "validator_refs": [],
                "consumer_refs": [],
                "policy_refs": [],
                "test_refs": [],
                "documentation_refs": [],
            }

    # 3. Discover engine modules
    if engine_dir.exists():
        for path in sorted(engine_dir.glob("*.py")):
            comp_id = f"engine:{path.name}"
            is_validator = path.name.startswith("validate_")
            is_renderer = "render_" in path.name
            is_compiler = path.name.startswith("compile_") or path.name.startswith("build_") or path.name.startswith("project_")
            is_runner = path.name.startswith("run_") or path.name.startswith("init_")

            ctype = "VALIDATOR" if is_validator else ("RENDERER" if is_renderer else ("COMPILER" if is_compiler else ("RUNNER" if is_runner else "EXECUTABLE_MODULE")))

            components[comp_id] = {
                "component_id": comp_id,
                "name": path.name,
                "path": str(path.relative_to(root)).replace("\\", "/"),
                "component_type": ctype,
                "schema_version": "N/A",
                "title": path.stem.replace("_", " ").title(),
                "authority_domain": _classify_authority(path.name, str(path)),
                "maturity_observation": "PRODUCTION",
                "producer_refs": [],
                "validator_refs": [],
                "consumer_refs": [],
                "policy_refs": [],
                "test_refs": [],
                "documentation_refs": [],
            }

    # 4. Discover tests
    if tests_dir.exists():
        for path in sorted(tests_dir.glob("*.py")):
            comp_id = f"test:{path.name}"
            components[comp_id] = {
                "component_id": comp_id,
                "name": path.name,
                "path": str(path.relative_to(root)).replace("\\", "/"),
                "component_type": "TEST_SUITE",
                "schema_version": "N/A",
                "title": path.stem.replace("_", " ").title(),
                "authority_domain": _classify_authority(path.name, str(path)),
                "maturity_observation": "TEST_FIXTURE",
                "producer_refs": [],
                "validator_refs": [],
                "consumer_refs": [],
                "policy_refs": [],
                "test_refs": [],
                "documentation_refs": [],
            }

    # 5. Discover documentation
    for path in sorted(root.glob("*.md")):
        comp_id = f"doc:{path.name}"
        components[comp_id] = {
            "component_id": comp_id,
            "name": path.name,
            "path": str(path.relative_to(root)).replace("\\", "/"),
            "component_type": "NORMATIVE_DOCUMENT" if path.name != "README.md" else "INFORMATIONAL_DOCUMENT",
            "schema_version": "N/A",
            "title": path.stem.replace("_", " ").title(),
            "authority_domain": _classify_authority(path.name, str(path)),
            "maturity_observation": "NORMATIVE",
            "producer_refs": [],
            "validator_refs": [],
            "consumer_refs": [],
            "policy_refs": [],
            "test_refs": [],
            "documentation_refs": [],
        }

    # 6. Extract relationships using AST / text analysis
    # A. Engine files inspection
    if engine_dir.exists():
        for path in sorted(engine_dir.glob("*.py")):
            engine_id = f"engine:{path.name}"
            content = path.read_text(encoding="utf-8")

            # Match referenced schemas
            schemas_found = set(re.findall(r'[\w-]+\.schema\.json', content))
            for s_name in schemas_found:
                s_id = f"schema:{s_name}"
                if s_id in components:
                    if components[engine_id]["component_type"] == "VALIDATOR":
                        components[s_id]["validator_refs"].append(engine_id)
                        relations.append({"source": engine_id, "target": s_id, "relation_type": "VALIDATES", "confidence": "DERIVED"})
                    elif components[engine_id]["component_type"] == "COMPILER":
                        components[s_id]["producer_refs"].append(engine_id)
                        relations.append({"source": engine_id, "target": s_id, "relation_type": "PRODUCES", "confidence": "DERIVED"})
                    else:
                        components[s_id]["consumer_refs"].append(engine_id)
                        relations.append({"source": engine_id, "target": s_id, "relation_type": "CONSUMES", "confidence": "DERIVED"})

            # Match referenced policies
            policies_found = set(re.findall(r'[\w-]+\.v\d+(?:\.[\w-]+)?\.json|math-[\w-]+\.json', content))
            for p_name in policies_found:
                p_id = f"policy:{p_name}"
                if p_id in components:
                    components[p_id]["consumer_refs"].append(engine_id)
                    relations.append({"source": engine_id, "target": p_id, "relation_type": "CONSUMES_POLICY", "confidence": "DERIVED"})

            # Match imported engine modules
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom) and node.module:
                        mod_file = f"{node.module}.py"
                        target_id = f"engine:{mod_file}"
                        if target_id in components and target_id != engine_id:
                            relations.append({"source": engine_id, "target": target_id, "relation_type": "IMPORTS", "confidence": "EXPLICIT"})
            except Exception:
                pass

    # B. Test files inspection
    if tests_dir.exists():
        for path in sorted(tests_dir.glob("*.py")):
            test_id = f"test:{path.name}"
            content = path.read_text(encoding="utf-8")

            # Match imported modules
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom) and node.module:
                        mod_file = f"{node.module}.py"
                        target_id = f"engine:{mod_file}"
                        if target_id in components:
                            components[target_id]["test_refs"].append(test_id)
                            relations.append({"source": test_id, "target": target_id, "relation_type": "TESTS", "confidence": "EXPLICIT"})
            except Exception:
                pass

            # Match referenced schemas and policies in tests
            schemas_found = set(re.findall(r'[\w-]+\.schema\.json', content))
            for s_name in schemas_found:
                s_id = f"schema:{s_name}"
                if s_id in components:
                    components[s_id]["test_refs"].append(test_id)
                    relations.append({"source": test_id, "target": s_id, "relation_type": "EXERCISES_SCHEMA", "confidence": "DERIVED"})

    # C. Documentation references inspection
    for path in sorted(root.glob("*.md")):
        doc_id = f"doc:{path.name}"
        content = path.read_text(encoding="utf-8")

        for comp_id, comp in components.items():
            if comp_id == doc_id:
                continue
            if comp["name"] in content:
                comp["documentation_refs"].append(doc_id)
                relations.append({"source": doc_id, "target": comp_id, "relation_type": "REFERENCES", "confidence": "DERIVED"})

    # 7. Deduplicate refs and sort relations
    for comp in components.values():
        comp["producer_refs"] = sorted(set(comp["producer_refs"]))
        comp["validator_refs"] = sorted(set(comp["validator_refs"]))
        comp["consumer_refs"] = sorted(set(comp["consumer_refs"]))
        comp["policy_refs"] = sorted(set(comp["policy_refs"]))
        comp["test_refs"] = sorted(set(comp["test_refs"]))
        comp["documentation_refs"] = sorted(set(comp["documentation_refs"]))

    relations.sort(key=lambda r: (r["source"], r["relation_type"], r["target"]))

    # 8. Identify gaps
    schemas_without_validator = [
        cid for cid, c in components.items()
        if c["component_type"] == "SCHEMA" and len(c["validator_refs"]) == 0
    ]
    validators_without_tests = [
        cid for cid, c in components.items()
        if c["component_type"] == "VALIDATOR" and len(c["test_refs"]) == 0
    ]
    policies_without_consumer = [
        cid for cid, c in components.items()
        if c["component_type"] == "POLICY" and len(c["consumer_refs"]) == 0
    ]
    orphan_schemas = [
        cid for cid, c in components.items()
        if c["component_type"] == "SCHEMA" and len(c["producer_refs"]) == 0 and len(c["consumer_refs"]) == 0 and len(c["validator_refs"]) == 0
    ]

    gap_reports = {
        "schemas_without_validator": schemas_without_validator,
        "validators_without_tests": validators_without_tests,
        "policies_without_consumer": policies_without_consumer,
        "orphan_schemas": orphan_schemas,
    }

    manifest = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "manifest_class": "DERIVED_ARCHITECTURE_OBSERVATION",
        "authority": "DERIVED_ARCHITECTURE_OBSERVATION",
        "technical_authorization": "NOT_EVALUATED",
        "publication_authorization": "NOT_IMPLIED",
        "component_count": len(components),
        "relation_count": len(relations),
        "components": components,
        "relations": relations,
        "gap_reports": gap_reports,
    }
    manifest["manifest_digest"] = _digest(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Blueprint Architecture Observation Manifest")
    parser.add_argument("--out", default=str(Path(__file__).parent / "architecture_observation_manifest.json"))
    parser.add_argument("--check", action="store_true", help="Check that the existing manifest on disk is up to date")
    args = parser.parse_args()

    manifest = scan_components()
    out_path = Path(args.out)

    if args.check:
        if not out_path.exists():
            raise SystemExit(f"Architecture manifest not found at {out_path}. Run without --check to generate.")
        existing = json.loads(out_path.read_text(encoding="utf-8"))
        if existing.get("manifest_digest") != manifest.get("manifest_digest"):
            raise SystemExit(
                f"Architecture observation manifest is OUT OF DATE.\n"
                f"Existing digest: {existing.get('manifest_digest')}\n"
                f"Current digest:  {manifest.get('manifest_digest')}\n"
                f"Run 'python generate_architecture_manifest.py' to regenerate."
            )
        print(f"Architecture observation manifest verified: UP TO DATE (digest: {manifest['manifest_digest']})")
        print(f"Components: {manifest['component_count']}, relations: {manifest['relation_count']}")
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Observation manifest generated at {out_path}")
    print(f"Total components: {manifest['component_count']}, relations: {manifest['relation_count']}")
    print(f"Gaps identified: {sum(len(v) for v in manifest['gap_reports'].values())}")


if __name__ == "__main__":
    main()
