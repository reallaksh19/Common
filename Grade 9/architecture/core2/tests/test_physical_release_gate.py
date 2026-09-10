#!/usr/bin/env python3
"""Regression falsifiers for release-blocking PhysicalPageMap finalization."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path

GRADE9 = Path(__file__).resolve().parents[2]
SCRIPTS = GRADE9 / "skills" / "grade9-core2-publisher" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import physical_release  # noqa: E402


class FakeLegacy:
    @staticmethod
    def load(path: Path):
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def write_json(path: Path, obj) -> None:
        path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    @staticmethod
    def validate_schema(_name: str, _obj: dict, _contracts: Path) -> None:
        # Schema shape is exercised independently by contract CI. This falsifier
        # isolates release-state behavior and exact artifact custody.
        return None

    @staticmethod
    def sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def artifact(role: str, path: Path, media_type: str) -> dict:
        return {
            "role": role,
            "path": path.name,
            "sha256": FakeLegacy.sha256(path),
            "media_type": media_type,
            "bytes": path.stat().st_size,
        }

    @staticmethod
    def package_digest(artifacts: list[dict]) -> str:
        payload = json.dumps(artifacts, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


def valid_page_map(pdf_sha: str) -> dict:
    return {
        "physical_page_map_id": "PPM-T",
        "schema_version": "1.0.0",
        "publication_structure_id": "PS-T",
        "publication_id": "SG-T",
        "pdf_role": "STUDY_GUIDE_PDF",
        "pdf_sha256": pdf_sha,
        "physical_page_count": 1,
        "page_intents": [
            {
                "page_intent_id": "PI-1",
                "physical_pages": [1],
                "content_refs": ["C-1"],
                "pagination_policy": "PREFER_SINGLE_PAGE",
                "split": False,
                "continuation_pages": [],
                "whitespace_role": "NONE",
            }
        ],
        "content_placements": [
            {
                "content_ref": "C-1",
                "page_intent_id": "PI-1",
                "physical_pages": [1],
                "fragments": [{"page": 1, "x0": 10, "y0": 10, "x1": 100, "y1": 40}],
            }
        ],
        "page_metrics": [
            {
                "page": 1,
                "semantic_fill_ratio": 0.4,
                "starts_page_intent_ids": ["PI-1"],
                "continues_page_intent_ids": [],
                "semantic_content_refs": ["C-1"],
                "orphan_continuation": False,
                "underfill_disposition": "ACCEPTABLE",
            }
        ],
    }


def write_package(root: Path, page_map: dict) -> list[str]:
    prefix = "T"
    pdf = root / f"{prefix}_Core2_Study_Guide.pdf"
    pdf.write_bytes(b"exact-study-guide-bytes")
    (root / f"{prefix}_Core2_Physical_Page_Map.json").write_text(
        json.dumps(page_map), encoding="utf-8"
    )
    (root / f"{prefix}_Core2_Publication_Audit.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "release_state": "AUTOMATED_PASS_HUMAN_REVIEW_PENDING",
                "gates": {"core2_preflight": True},
                "human_visual_review": {"status": "PENDING"},
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )
    (root / f"{prefix}_Core2_Publication_Manifest.json").write_text(
        json.dumps({"artifacts": [], "package_digest": "0" * 64}), encoding="utf-8"
    )
    return ["run_core2.py", "--out", str(root), "--prefix", prefix]


def run_case(mutator, expected_fragment: str | None) -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        pdf = root / "T_Core2_Study_Guide.pdf"
        pdf.write_bytes(b"exact-study-guide-bytes")
        page_map = valid_page_map(FakeLegacy.sha256(pdf))
        mutator(page_map)
        argv = write_package(root, page_map)
        errors = physical_release.finalize(argv, FakeLegacy, Path(td))
        audit = FakeLegacy.load(root / "T_Core2_Publication_Audit.json")
        manifest = FakeLegacy.load(root / "T_Core2_Publication_Manifest.json")

        if expected_fragment is None:
            assert errors == [], errors
            assert audit["gates"]["physical_page_custody"] is True
            assert audit["gates"]["physical_page_morphology"] is True
            assert audit["status"] == "PASS"
            assert audit["release_state"] == "AUTOMATED_PASS_HUMAN_REVIEW_PENDING"
            roles = {row["role"] for row in manifest["artifacts"]}
            assert {"PUBLICATION_AUDIT", "PHYSICAL_PAGE_MAP"} <= roles
        else:
            assert any(expected_fragment in error for error in errors), errors
            assert audit["status"] == "FAIL"
            assert audit["release_state"] == "AUTOMATED_FAIL"


def main() -> int:
    run_case(lambda _page_map: None, None)

    def orphan(page_map: dict) -> None:
        page_map["physical_page_count"] = 2
        page_map["page_intents"][0].update(
            {"physical_pages": [1, 2], "split": True, "continuation_pages": [2]}
        )
        page_map["content_placements"][0]["physical_pages"] = [1, 2]
        page_map["content_placements"][0]["fragments"].append(
            {"page": 2, "x0": 10, "y0": 10, "x1": 80, "y1": 20}
        )
        page_map["page_metrics"].append(
            {
                "page": 2,
                "semantic_fill_ratio": 0.02,
                "starts_page_intent_ids": [],
                "continues_page_intent_ids": ["PI-1"],
                "semantic_content_refs": ["C-1"],
                "orphan_continuation": True,
                "underfill_disposition": "PATHOLOGICAL",
            }
        )

    run_case(orphan, "orphan continuation")

    def missing_placement(page_map: dict) -> None:
        page_map["content_placements"] = []

    run_case(missing_placement, "no physical placement")

    def wrong_pdf_hash(page_map: dict) -> None:
        page_map["pdf_sha256"] = "f" * 64

    run_case(wrong_pdf_hash, "does not bind exact Study Guide PDF")

    print("PHYSICAL_RELEASE_GATE_FALSIFIERS = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
