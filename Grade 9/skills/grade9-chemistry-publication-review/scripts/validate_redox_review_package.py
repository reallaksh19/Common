#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
from pypdf import PdfReader

EXPECTED_PDFS = {
    "Redox_Core_Study_Guide.pdf": (68, 0),
    "Redox_ExamSIDE_Transfer_Book.pdf": (85, 30),
}
REQUIRED_TEXT = [
    "README.md", "REVIEW_GUIDE.md", "CONCEPT_REVIEW_MAP.md",
    "SOURCE_COVERAGE_MAP.md", "EXAMSIDE_COVERAGE_MAP.md",
    "CHEMISTRY_REBUILD_REVIEW.md", "REPRODUCE.md", "DELIVERY_RECORD.md",
    "Redox_ExamSIDE_Ledger.json", "Source/Source_Fingerprint.json",
    "Prepared_Artifact_Fingerprints.json", "Packaging_Validation.json", "FILE_MANIFEST.json",
]

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def link_count(reader):
    total = 0
    for page in reader.pages:
        annots = page.get("/Annots")
        if not annots:
            continue
        for ref in annots:
            try:
                if ref.get_object().get("/Subtype") == "/Link":
                    total += 1
            except Exception:
                pass
    return total

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    failures, blockers = [], []
    observed = {}

    for rel in REQUIRED_TEXT:
        if not (root / rel).is_file():
            failures.append(f"missing required text/evidence file: {rel}")

    fp_path = root / "Prepared_Artifact_Fingerprints.json"
    fingerprints = json.loads(fp_path.read_text(encoding="utf-8")) if fp_path.is_file() else {"artifacts": {}}

    for rel, (expected_pages, expected_links) in EXPECTED_PDFS.items():
        p = root / rel
        fp = fingerprints.get("artifacts", {}).get(rel, {})
        if not p.is_file():
            blockers.append(f"reviewed binary artifact not committed: {rel}")
            if fp.get("pages") != expected_pages or fp.get("embedded_link_annotations") != expected_links or not fp.get("sha256"):
                failures.append(f"incomplete prepared-artifact fingerprint: {rel}")
            continue
        r = PdfReader(str(p))
        pages, links = len(r.pages), link_count(r)
        digest = sha256(p)
        observed[rel] = {"pages": pages, "links": links, "sha256": digest}
        if pages != expected_pages:
            failures.append(f"{rel}: pages {pages} != {expected_pages}")
        if links != expected_links:
            failures.append(f"{rel}: links {links} != {expected_links}")
        if fp and digest != fp.get("sha256"):
            failures.append(f"{rel}: committed bytes do not match reviewed fingerprint")

    ledger_path = root / "Redox_ExamSIDE_Ledger.json"
    if ledger_path.is_file():
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        if ledger.get("snapshot", {}).get("candidate_count") != 74:
            failures.append("ledger candidate_count != 74")
        expected_counts = {"ELIGIBLE_IN_SCOPE":24, "PARTIAL_SCOPE":8, "OUT_OF_SCOPE":42}
        for k,v in expected_counts.items():
            if ledger.get("status_counts", {}).get(k) != v:
                failures.append(f"ledger {k} != {v}")
        expected_sub = {"RX-ST01":7,"RX-ST02":2,"RX-ST03":4,"RX-ST04":3,"RX-ST05":8}
        if ledger.get("eligible_by_primary_subtopic") != expected_sub:
            failures.append("eligible_by_primary_subtopic mismatch")

    manifest_path = root / "FILE_MANIFEST.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for rel, item in manifest.get("files", {}).items():
            p = root / rel
            if not p.is_file():
                failures.append(f"manifest path missing: {rel}")
            elif sha256(p) != item.get("sha256"):
                failures.append(f"manifest hash mismatch: {rel}")

    if failures:
        status = "FAIL"
        code = 1
    elif blockers:
        status = "DRAFT_BLOCKED_BINARY_ARTIFACT_UPLOAD"
        code = 0
    else:
        status = "PASS"
        code = 0
    print(json.dumps({"status":status, "failures":failures, "blockers":blockers, "observed_pdfs":observed}, indent=2))
    return code

if __name__ == "__main__":
    raise SystemExit(main())
