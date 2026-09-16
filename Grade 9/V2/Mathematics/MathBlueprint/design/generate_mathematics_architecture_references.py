from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

DESIGN = Path(__file__).resolve().parent
ROOT = DESIGN.parent
GENERATED = DESIGN / "generated"
CATALOG = DESIGN / "mathematics-architecture-catalog.candidate.json"
CATALOG_SCHEMA = DESIGN / "mathematics-architecture-catalog.candidate.schema.json"
C2_RECEIPT = DESIGN / "mathematics-normative-root-consolidation.json"
MANIFEST = GENERATED / "mathematics-architecture-reference-index.generated.json"
MARKDOWN = GENERATED / "MATHEMATICS_ARCHITECTURE_REFERENCES.generated.md"
C3_RECEIPT = DESIGN / "mathematics-generated-references.receipt.json"
GENERATOR_REL = "design/generate_mathematics_architecture_references.py"
CATALOG_REL = "design/mathematics-architecture-catalog.candidate.json"
CATALOG_SCHEMA_REL = "design/mathematics-architecture-catalog.candidate.schema.json"
C2_RECEIPT_REL = "design/mathematics-normative-root-consolidation.json"
MANIFEST_REL = "design/generated/mathematics-architecture-reference-index.generated.json"
MARKDOWN_REL = "design/generated/MATHEMATICS_ARCHITECTURE_REFERENCES.generated.md"
REFERENCE_KINDS = ("SCHEMA", "POLICY", "VALIDATOR", "TEST")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def classify_evidence_path(rel: str) -> str | None:
    if rel.startswith("contracts/") and rel.endswith(".schema.json"):
        return "SCHEMA"
    if rel.startswith("policies/"):
        return "POLICY"
    if rel.startswith("engine/") and Path(rel).name.startswith("validate_") and rel.endswith(".py"):
        return "VALIDATOR"
    if rel.startswith("tests/") and rel.endswith(".py"):
        return "TEST"
    return None


def validate_inputs(catalog: dict, catalog_schema: dict, c2_receipt: dict) -> None:
    errors = sorted(
        Draft202012Validator(catalog_schema).iter_errors(catalog),
        key=lambda error: list(error.path),
    )
    if errors:
        raise ValueError(
            "C3 source catalog failed its C1 design schema: "
            + "; ".join(error.message for error in errors)
        )

    if catalog.get("authority") != "NONE" or catalog.get("semantic_change") != "NONE":
        raise ValueError("C3 may consume only the non-authoritative, semantic-noop C1 catalog")
    if c2_receipt.get("status") != "C2_NORMATIVE_ROOT_CONSOLIDATED":
        raise ValueError("C3 requires the completed C2 consolidation receipt")
    if c2_receipt.get("authority") != "NONE" or c2_receipt.get("semantic_change") != "NONE":
        raise ValueError("C2 receipt must remain non-authoritative and semantic-noop")
    if c2_receipt.get("owner_decision_required_count") != 0:
        raise ValueError("C3 is blocked while C2 has unresolved owner decisions")
    if c2_receipt.get("next_stage") != "C3_GENERATED_REFERENCES_READY":
        raise ValueError("C2 has not authorized the C3 documentation/reference stage")
    tracked_gap = c2_receipt.get("tracked_runtime_gap", {})
    if tracked_gap.get("finding_id") != "C0-F007":
        raise ValueError("C3 requires explicit custody of the preserved C0-F007 runtime gap")
    if tracked_gap.get("classification") != "CURRENT + DOCUMENTED ONLY":
        raise ValueError("C3 must not silently upgrade C0-F007")


def project_catalog(catalog: dict, *, require_paths: bool = True) -> tuple[list[dict], dict[str, list[dict]]]:
    components: list[dict] = []
    references: dict[str, list[dict]] = {kind: [] for kind in REFERENCE_KINDS}

    for component in catalog["components"]:
        component_id = component["component_id"]
        components.append(
            {
                "component_id": component_id,
                "architecture_role": component["architecture_role"],
                "primary_authority_class": component["primary_authority_class"],
                "runtime_authority_effect": component["runtime_authority_effect"],
                "publication_authority_effect": component["publication_authority_effect"],
            }
        )
        for rel in component["evidence_paths"]:
            if require_paths and not (ROOT / rel).exists():
                raise ValueError(f"catalog evidence path is missing: {rel}")
            kind = classify_evidence_path(rel)
            if kind is not None:
                references[kind].append({"component_id": component_id, "path": rel})

    components.sort(key=lambda row: row["component_id"])
    for kind in REFERENCE_KINDS:
        references[kind].sort(key=lambda row: (row["component_id"], row["path"]))
    return components, references


def build_manifest() -> dict:
    catalog = load_json(CATALOG)
    catalog_schema = load_json(CATALOG_SCHEMA)
    c2_receipt = load_json(C2_RECEIPT)
    validate_inputs(catalog, catalog_schema, c2_receipt)
    components, references = project_catalog(catalog)

    return {
        "schema_version": "0.1.0",
        "status": "GENERATED_NON_AUTHORITATIVE_REFERENCE",
        "authority": "NONE",
        "semantic_change": "NONE",
        "view_class": "DERIVED_ARCHITECTURE_REFERENCE_ONLY",
        "publication_authorization": "NOT_IMPLIED",
        "generation_rule": "CATALOG_DECLARED_EVIDENCE_PATHS_ONLY",
        "source_custody": {
            "catalog_path": CATALOG_REL,
            "catalog_git_blob_sha": git_blob_sha(CATALOG),
            "catalog_schema_path": CATALOG_SCHEMA_REL,
            "catalog_schema_git_blob_sha": git_blob_sha(CATALOG_SCHEMA),
            "c2_receipt_path": C2_RECEIPT_REL,
            "c2_receipt_git_blob_sha": git_blob_sha(C2_RECEIPT),
            "generator_path": GENERATOR_REL,
            "generator_git_blob_sha": git_blob_sha(Path(__file__)),
        },
        "component_count": len(components),
        "reference_counts": {kind: len(references[kind]) for kind in REFERENCE_KINDS},
        "components": components,
        "references": references,
    }


def build_c3_receipt(manifest: dict) -> dict:
    return {
        "schema_version": "0.1.0",
        "status": "C3_GENERATED_REFERENCES_COMPLETE",
        "authority": "NONE",
        "semantic_change": "NONE",
        "view_class": "DERIVED_NON_AUTHORITATIVE_ARCHITECTURE_REFERENCE",
        "publication_authorization": "NOT_IMPLIED",
        "catalog_semantics": "CLASSIFICATION_ONLY_UNCHANGED",
        "production_consumers_allowed": False,
        "source_custody": manifest["source_custody"],
        "generated_outputs": {
            "manifest_path": MANIFEST_REL,
            "markdown_path": MARKDOWN_REL,
        },
        "component_count": manifest["component_count"],
        "reference_counts": manifest["reference_counts"],
        "tracked_runtime_gap": {
            "finding_id": "C0-F007",
            "classification": "CURRENT + DOCUMENTED ONLY",
            "runtime_auto_materialization_executable": False,
        },
        "next_stage": "C4_SUBJECT_ADAPTER_INTERFACE_READY",
    }


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_markdown(manifest: dict) -> str:
    custody = manifest["source_custody"]
    lines = [
        "# Mathematics Architecture Generated References",
        "",
        "> **Status: DESIGN / NON-NORMATIVE / GENERATED**",
        ">",
        "> This file is a derived reference view. It cannot authorize runtime behavior, mathematical truth, component maturity, release state or publication. Regenerate it only from the C1 architecture catalog using the C3 generator.",
        "",
        f"- Source catalog Git blob: `{custody['catalog_git_blob_sha']}`",
        f"- Source catalog schema Git blob: `{custody['catalog_schema_git_blob_sha']}`",
        f"- C2 receipt Git blob: `{custody['c2_receipt_git_blob_sha']}`",
        f"- Generator Git blob: `{custody['generator_git_blob_sha']}`",
        f"- Components: **{manifest['component_count']}**",
        "- Authority: `NONE`",
        "- Publication authorization: `NOT_IMPLIED`",
        "",
        "## Architecture components",
        "",
        "| Component | Role | Primary class | Runtime effect | Publication effect |",
        "|---|---|---|---|---|",
    ]
    for row in manifest["components"]:
        lines.append(
            "| "
            + " | ".join(
                markdown_cell(str(row[key]))
                for key in (
                    "component_id",
                    "architecture_role",
                    "primary_authority_class",
                    "runtime_authority_effect",
                    "publication_authority_effect",
                )
            )
            + " |"
        )

    titles = {
        "SCHEMA": "Schemas",
        "POLICY": "Policies",
        "VALIDATOR": "Validators",
        "TEST": "Tests",
    }
    for kind in REFERENCE_KINDS:
        lines.extend(
            [
                "",
                f"## {titles[kind]}",
                "",
                f"Count: **{manifest['reference_counts'][kind]}**",
                "",
                "| Component | Repository path |",
                "|---|---|",
            ]
        )
        for row in manifest["references"][kind]:
            lines.append(
                f"| {markdown_cell(row['component_id'])} | `{markdown_cell(row['path'])}` |"
            )

    lines.extend(
        [
            "",
            "## Non-authority boundary",
            "",
            "These tables are observability only. They do not promote a design component, alter a governed policy, select an Engineering identity, satisfy a validator, authorize a producer, pass a release gate or imply publication authority.",
            "",
            "C0-F007 remains `CURRENT + DOCUMENTED ONLY`; C3 does not make optional EASY-research auto-materialization executable.",
            "",
        ]
    )
    return "\n".join(lines)


def expected_outputs() -> tuple[dict, str, dict]:
    manifest = build_manifest()
    return manifest, render_markdown(manifest), build_c3_receipt(manifest)


def write_outputs() -> None:
    manifest, markdown, receipt = expected_outputs()
    GENERATED.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    MARKDOWN.write_text(markdown, encoding="utf-8")
    C3_RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


def check_outputs() -> None:
    expected_manifest, expected_markdown, expected_receipt = expected_outputs()
    actual_manifest = load_json(MANIFEST)
    actual_receipt = load_json(C3_RECEIPT)
    actual_markdown = MARKDOWN.read_text(encoding="utf-8")
    if actual_manifest != expected_manifest:
        raise SystemExit("C3 generated manifest is stale; run generator with --write")
    if actual_markdown != expected_markdown:
        raise SystemExit("C3 generated Markdown is stale; run generator with --write")
    if actual_receipt != expected_receipt:
        raise SystemExit("C3 receipt is stale; run generator with --write")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write_outputs()
    else:
        check_outputs()


if __name__ == "__main__":
    main()
