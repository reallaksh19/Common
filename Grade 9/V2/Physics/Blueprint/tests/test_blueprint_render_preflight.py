#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas

BP = Path(__file__).resolve().parents[1]


def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preflight = mod("bp_render_preflight", BP / "engine" / "preflight_rendered_pdf.py")
builder = mod("bp_render_process_golden", BP / "engine" / "build_render_process_golden.py")
POLICY = json.loads((BP / "policy" / "render-preflight.v1.json").read_text())


def make_ir(content_digest):
    obj = {
        "schema_version": "1.0.0",
        "publication_ir_id": "PUBIR-PHY-RENDER-TEST",
        "topic_id": "PHY-RENDER-TEST",
        "product_mode": "CORE1A_TEXTBOOK",
        "authority_boundary": {
            "semantic_authority":"UPSTREAM_ONLY",
            "renderer_authority":"COMPOSITION_ONLY",
            "renderer_may_introduce_semantic_claims":False,
            "renderer_may_substitute_representation":False
        },
        "upstream_artifacts":[{
            "role":"CORE1A",
            "artifact_ref":"A-PHY-RENDER-TEST",
            "artifact_digest":content_digest,
            "release_state":"RELEASED"
        }],
        "units":[{
            "unit_id":"PUBUNIT-PHY-0001",
            "source_role":"CORE1A",
            "source_artifact_ref":"A-PHY-RENDER-TEST",
            "semantic_ref":"A-RENDER-TEST",
            "content_digest":content_digest,
            "surface_kind":"EXPLANATION",
            "representation_refs":[]
        }],
        "lossless_audit":{
            "required_semantic_ref_count":1,
            "placed_required_ref_count":1,
            "missing_refs":[],
            "duplicate_refs":[],
            "unknown_refs":[],
            "digest_mismatches":[],
            "representation_violations":[],
            "status":"PASS"
        }
    }
    obj["publication_ir_digest"] = preflight.digest(obj)
    return obj


def custody(ir, renderer_report):
    return {
        "schema_version":"1.0.0",
        "custody_id":"RENDER-CUSTODY-PHY-TEST",
        "publication_ir_digest":ir["publication_ir_digest"],
        "renderer_name":"TEST_RENDERER",
        "renderer_authority":"COMPOSITION_ONLY",
        "renderer_report_digest":preflight.digest(renderer_report),
        "expected_pdf_sha256":renderer_report["artifact_sha256"]
    }


def simple_pdf(path, pagesize=A4, text="Visible learner content", font=10):
    c = canvas.Canvas(str(path), pagesize=pagesize, invariant=1)
    c.setFont("Helvetica", font)
    c.drawString(72, pagesize[1]-72, text)
    c.save()


def simple_report(path):
    return {
        "artifact_sha256":preflight.sha256_file(path),
        "page_count":1,
        "publication_engineering_pass":True
    }


class BlueprintRenderPreflightTests(unittest.TestCase):
    def test_existing_core1a_renderer_process_golden_passes_actual_pdf_preflight(self):
        with tempfile.TemporaryDirectory() as td:
            report = builder.build(Path(td))
            self.assertTrue(report["machine_preflight_pass"], report["machine_findings"])
            self.assertFalse(report["release_authorized"])
            self.assertEqual(report["human_visual_review_state"], "PENDING")
            self.assertTrue((Path(td) / "physics-blueprint-render-process-golden.pdf").exists())
            self.assertTrue(any((Path(td) / "raster-proof").glob("*.png")))

    def test_custody_digest_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "x.pdf"
            simple_pdf(pdf)
            rr = simple_report(pdf)
            ir = make_ir("a"*64)
            c = custody(ir, rr)
            c["expected_pdf_sha256"] = "0"*64
            with self.assertRaisesRegex(AssertionError, "RENDER_CUSTODY_PDF_DIGEST_MISMATCH"):
                preflight.preflight_rendered_pdf(pdf_path=pdf, publication_ir=ir, renderer_report=rr, custody=c, policy=POLICY)

    def test_non_a4_page_blocks_machine_preflight(self):
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "letter.pdf"
            simple_pdf(pdf, pagesize=letter)
            rr = simple_report(pdf)
            ir = make_ir("b"*64)
            report = preflight.preflight_rendered_pdf(pdf_path=pdf, publication_ir=ir, renderer_report=rr, custody=custody(ir, rr), policy=POLICY)
            self.assertFalse(report["machine_preflight_pass"])
            self.assertTrue(any("PAGE_GEOMETRY_NOT_A4" in x for x in report["machine_findings"]))

    def test_internal_identifier_leak_blocks_machine_preflight(self):
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "leak.pdf"
            simple_pdf(pdf, text="Learner text PHY-CAP-SECRET should never be visible.")
            rr = simple_report(pdf)
            ir = make_ir("c"*64)
            report = preflight.preflight_rendered_pdf(pdf_path=pdf, publication_ir=ir, renderer_report=rr, custody=custody(ir, rr), policy=POLICY)
            self.assertFalse(report["machine_preflight_pass"])
            self.assertTrue(any("INTERNAL_IDENTIFIER_LEAK" in x for x in report["machine_findings"]))

    def test_actual_font_floor_is_pdf_observation_not_renderer_claim(self):
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "small.pdf"
            simple_pdf(pdf, font=5)
            rr = simple_report(pdf)
            ir = make_ir("d"*64)
            report = preflight.preflight_rendered_pdf(pdf_path=pdf, publication_ir=ir, renderer_report=rr, custody=custody(ir, rr), policy=POLICY)
            self.assertFalse(report["machine_preflight_pass"])
            self.assertIn("RENDER_ACTUAL_FONT_FLOOR_VIOLATION", report["machine_findings"])


if __name__ == "__main__":
    unittest.main()
