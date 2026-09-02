#!/usr/bin/env python3
"""Fail-closed machine custody checks for IOQM G9 GEO-05.

This script never certifies page-by-page visual QA. It checks only machine-verifiable
preconditions and leaves G15 visual inspection as a separate manual gate.
"""
from __future__ import annotations

import argparse, csv, hashlib, re, sys
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

EXPECTED_FILES = 24
EXPECTED_COLUMNS = 31
EXPECTED_ROWS = 47
EXPECTED_AUTHORED = 42
HISTORICAL = {
    "IOQM-2025-Q10": "54",
    "IOQM-2025-Q17": "23",
    "IOQM-2024-Q07": "99",
    "IOQM-2023-Q14": "40",
    "IOQM-2023-Q23": "18",
}
PDFS = {
    "PDFs/GEO05_Student_Pack_v1.pdf": (7, 14257, "45468a443e8e150110299117d2f033e0ae8be111e747492b6ce490e80f8c5247", "60ee54edc7a0f74c51723c7754f138170db43772"),
    "PDFs/GEO05_Teacher_Key_v1.pdf": (3, 4686, "54ba2add1bbdbdc4e18df11fac55dab3e739ba60f5cb8459e825bcbbeca94115", "aac1f03e31112adce627f871d033d2b06ff2ef87"),
}
FIXED = {
    "00_Concept_and_Dependency_Map.md", "01_Source_Coverage_Map.md",
    "02_Assimilation_Book.md", "03_First_Step_Reference.md",
    "04_Recognition_and_First_Line_Lab.md", "05_Practice_and_Transfer_Bank.md",
    "06_H0_Mastery_Test.md", "Teacher_Diagnostic_Key.md", "Item_Metadata.csv",
    "QA.md", "README.md", "Authoring/Microstream_Interfaces.md",
    "Authoring/GEO05_Stable_Alternate_Representation_Interface_v1.md",
    "Authoring/render_geo05_pdfs.py", "PDFs/README.md", *PDFS,
}
LEARNER = [
    "02_Assimilation_Book.md", "03_First_Step_Reference.md",
    "04_Recognition_and_First_Line_Lab.md", "05_Practice_and_Transfer_Bank.md",
    "06_H0_Mastery_Test.md",
]
ITEM = re.compile(r"<!--\s*ITEM:(GEO05-[A-Z][0-9]{2})\s*-->")
KEY = re.compile(r"^\|\s*(GEO05-[A-Z][0-9]{2})\s*\|", re.M)
IFACE = re.compile(r"^IOQM-G9-GEO-05__W1-([A-G])__.+__interface\.md$")
FORBIDDEN = {
    "wave": re.compile(r"\bW[0-9]+-[A-Z]\b", re.I),
    "H/T": re.compile(r"\b(?:H[0-9]+|T[0-9]+)\b"),
    "interface": re.compile(r"\binterfaces?\b", re.I),
    "dependency": re.compile(r"\bdependencies?\b", re.I),
    "QA": re.compile(r"\bQA\b"),
    "agent": re.compile(r"\bagents?\b", re.I),
    "GitHub": re.compile(r"\bGitHub\b", re.I),
    "PR": re.compile(r"\bpull request\b|\bPR\s*#?\d+\b", re.I),
    "production": re.compile(r"\bproduction\b", re.I),
    "topic-control": re.compile(r"\bIOQM-G9-GEO-05\b", re.I),
}

fails: list[str] = []
def check(ok: bool, msg: str):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok: fails.append(msg)

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def blobsha(p: Path) -> str:
    b = p.read_bytes()
    return hashlib.sha1(f"blob {len(b)}\0".encode() + b).hexdigest()

def main(root: Path) -> int:
    if not root.is_dir():
        print(f"FAIL package root missing: {root}", file=sys.stderr); return 2
    files = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
    fset = set(files)
    check(len(files) == EXPECTED_FILES, f"file count {len(files)} == {EXPECTED_FILES}")
    for rel in sorted(FIXED): check(rel in fset, f"required file {rel}")

    interfaces = []
    for p in (root / "Authoring").glob("*.md") if (root / "Authoring").is_dir() else []:
        m = IFACE.match(p.name)
        if m: interfaces.append(m.group(1))
    check(sorted(interfaces) == list("ABCDEFG"), f"interfaces W1-A..G: {sorted(interfaces)}")

    meta = root / "Item_Metadata.csv"
    authored = set()
    if meta.is_file():
        with meta.open(encoding="utf-8-sig", newline="") as f:
            r = csv.DictReader(f); fields = r.fieldnames or []; rows = list(r)
        check(len(fields) == EXPECTED_COLUMNS, f"metadata columns {len(fields)} == {EXPECTED_COLUMNS}")
        check(len(rows) == EXPECTED_ROWS, f"metadata rows {len(rows)} == {EXPECTED_ROWS}")
        ids = [(x.get("item_id") or "").strip() for x in rows]
        check(len(ids) == len(set(ids)), "metadata IDs unique")
        by = {x.get("item_id", "").strip(): x for x in rows}
        authored = {x for x in by if x.startswith("GEO05-")}
        check(len(authored) == EXPECTED_AUTHORED, f"authored metadata {len(authored)} == {EXPECTED_AUTHORED}")
        check({x for x in by if x.startswith("IOQM-")} == set(HISTORICAL), "historical ID set exact")
        for q, ans in HISTORICAL.items():
            row = by.get(q, {})
            check((row.get("official_answer") or "").strip() == ans, f"{q} answer {ans}")
            check((row.get("figure_required") or "").strip().lower() == "false", f"{q} figure_required=false")
            check((row.get("answer_verified_independently") or "").strip().lower() == "true", f"{q} independent=true")
    else: check(False, "Item_Metadata.csv present")

    marks = []
    for rel in LEARNER:
        p = root / rel
        if p.is_file(): marks += ITEM.findall(p.read_text(encoding="utf-8"))
    keyp = root / "Teacher_Diagnostic_Key.md"
    keys = KEY.findall(keyp.read_text(encoding="utf-8")) if keyp.is_file() else []
    check(len(marks) == EXPECTED_AUTHORED and len(set(marks)) == EXPECTED_AUTHORED, "42 unique learner markers")
    check(len(keys) == EXPECTED_AUTHORED and len(set(keys)) == EXPECTED_AUTHORED, "42 unique teacher key IDs")
    check(set(marks) == authored == set(keys), "learner/metadata/teacher closure exact")

    for rel in LEARNER:
        p = root / rel
        if not p.is_file(): continue
        s = ITEM.sub("", p.read_text(encoding="utf-8"))
        for name, pat in FORBIDDEN.items(): check(not pat.search(s), f"learner hygiene {rel}: {name}")

    for rel, (pages, size, digest, blob) in PDFS.items():
        p = root / rel
        if not p.is_file(): check(False, f"PDF present {rel}"); continue
        check(p.stat().st_size == size, f"{rel} bytes {size}")
        check(sha256(p) == digest, f"{rel} SHA-256")
        check(blobsha(p) == blob, f"{rel} Git blob")
        if PdfReader is None: check(False, "pypdf available for structural PDF check"); continue
        try:
            r = PdfReader(str(p)); check(len(r.pages) == pages, f"{rel} pages {pages}")
            check(not r.is_encrypted, f"{rel} unencrypted")
            a4 = all(abs(float(pg.mediabox.width)-595.276) <= 1 and abs(float(pg.mediabox.height)-841.89) <= 1 for pg in r.pages)
            check(a4, f"{rel} A4 MediaBox")
        except Exception as e: check(False, f"{rel} readable: {e}")

    md = "\n".join(p.read_text(encoding="utf-8") for p in root.rglob("*.md"))
    check("BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED" in md, "exact completion language present")
    for term in ("classroom", "retention", "psychometric", "qualification", "publication"):
        pat = re.compile(rf"(?is){term}.{{0,120}}NOT_RUN|NOT_RUN.{{0,120}}{term}")
        check(bool(pat.search(md)), f"{term} remains NOT_RUN")

    print("MANUAL GATE: this script does NOT certify page-by-page visual QA.")
    print("Remaining handover inspection set: student pages 4-7; teacher pages 1-3.")
    print(f"STATIC RESULT: {'FAIL' if fails else 'PASS'} ({len(fails)} failed checks)")
    return 1 if fails else 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("root", type=Path)
    ns = ap.parse_args(); raise SystemExit(main(ns.root.resolve()))
