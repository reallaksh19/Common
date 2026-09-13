#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator

BP = Path(__file__).resolve().parents[1]
PHYS = BP.parent
CORE1A = PHYS / "Core1A"


def mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core1_build = mod("bp_process_core1a_build", CORE1A / "engine" / "build_physics_core1a.py")
core1_render = mod("bp_process_core1a_render", CORE1A / "engine" / "render_physics_core1a.py")
publication = mod("bp_process_publication_ir", BP / "engine" / "compile_publication_ir.py")
preflight = mod("bp_process_preflight", BP / "engine" / "preflight_rendered_pdf.py")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    core1 = load(BP / "fixtures" / "render" / "process-core1-plan.json")
    core1["plan_digest"] = core1_build.digest(core1, "plan_digest")
    c1a_policy = load(CORE1A / "registry" / "physics-core1a-publication-policy.json")
    plan = core1_build.build_publication_plan(core1, c1a_policy)

    pdf = out_dir / "physics-blueprint-render-process-golden.pdf"
    renderer_report = core1_render.render_core1a(core1, plan, pdf, c1a_policy)

    pub_spec = {
        "publication_ir_id": "PUBIR-PHY-RENDER-PROCESS-GOLDEN",
        "topic_id": "PHY-RENDER-PROCESS-GOLDEN",
        "product_mode": "CORE1A_TEXTBOOK",
        "upstream_artifacts": [{
            "role": "CORE1A",
            "artifact_ref": plan["plan_id"],
            "artifact_digest": plan["plan_digest"],
            "release_state": "RELEASED",
            "semantic_units": [{
                "semantic_ref": "A-RENDER-PROCESS-PLAN",
                "content_digest": plan["plan_digest"],
                "required": True,
                "authorized_representation_refs": []
            }]
        }],
        "publication_units": [{
            "source_role": "CORE1A",
            "source_artifact_ref": plan["plan_id"],
            "semantic_ref": "A-RENDER-PROCESS-PLAN",
            "content_digest": plan["plan_digest"],
            "surface_kind": "EXPLANATION",
            "representation_refs": []
        }]
    }
    ir = publication.compile_publication_ir(pub_spec, load(BP / "policy" / "publication-boundary.v1.json"))
    custody = {
        "schema_version": "1.0.0",
        "custody_id": "RENDER-CUSTODY-PHY-PROCESS-GOLDEN",
        "publication_ir_digest": ir["publication_ir_digest"],
        "renderer_name": "Core1A.render_physics_core1a",
        "renderer_authority": "COMPOSITION_ONLY",
        "renderer_report_digest": preflight.digest(renderer_report),
        "expected_pdf_sha256": renderer_report["artifact_sha256"]
    }

    Draft202012Validator(load(BP / "contracts" / "render-custody.schema.json")).validate(custody)
    report = preflight.preflight_rendered_pdf(
        pdf_path=pdf,
        publication_ir=ir,
        renderer_report=renderer_report,
        custody=custody,
        policy=load(BP / "policy" / "render-preflight.v1.json"),
        raster_dir=out_dir / "raster-proof",
    )
    Draft202012Validator(load(BP / "contracts" / "render-preflight-report.schema.json")).validate(report)

    save(out_dir / "core1a-publication-plan.json", plan)
    save(out_dir / "renderer-report.json", renderer_report)
    save(out_dir / "publication-ir.json", ir)
    save(out_dir / "render-custody.json", custody)
    save(out_dir / "render-preflight.json", report)
    if not report["machine_preflight_pass"]:
        raise AssertionError("RENDER_PROCESS_GOLDEN_PREFLIGHT_BLOCKED:" + ",".join(report["machine_findings"]))
    return report


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    report = build(args.out_dir)
    print(json.dumps({
        "machine_preflight_pass": report["machine_preflight_pass"],
        "machine_release_state": report["machine_release_state"],
        "release_authorized": report["release_authorized"],
        "page_count": report["page_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
