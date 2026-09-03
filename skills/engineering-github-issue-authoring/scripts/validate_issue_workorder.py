#!/usr/bin/env python3
"""Focused structural/quality validator for engineering GitHub issue drafts.

This is intentionally a fail-closed heuristic gate, not a substitute for expert review.
"""

from pathlib import Path
import re
import sys

REQUIRED_HEADINGS = [
    r"mission",
    r"ground truth at issue creation",
    r"owner intent.*authority.*scope|owner intent",
    r"definition of done",
    r"input/source inventory|input.*source inventory",
    r"current production/repository path|current production.*path|current repository.*path",
    r"technical implementation instructions",
    r"pass\s*/\s*fail\s*/\s*not_run criteria|pass.*fail.*not_run criteria",
    r"benchmark.*oracle criteria|benchmark / independent oracle criteria",
    r"anti-drift.*fail-closed logic|anti-drift",
    r"negative tests.*falsifiers",
    r"explicit exclusions.*non-goals|explicit exclusions",
    r"validation matrix",
    r"appendix a.*implementation qualification",
]

PROFILES = {"NUMERICAL_ENGINEERING", "SOFTWARE_ENGINEERING", "SOURCE_GOVERNANCE"}
CALC_RE = re.compile(r"\b(calculate|compute|derive|reconstruct|evaluate|close the free body|by hand)\b", re.I)
NUMERIC_RE = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?", re.I)
HEX_RE = re.compile(r"\b(?:0x)?[0-9a-f]{8,}\b", re.I)


def heading_present(text: str, pattern: str) -> bool:
    return bool(re.search(rf"(?mi)^#+\s+.*(?:{pattern}).*$", text))


def appendix(text: str) -> str:
    m = re.search(r"(?mis)^#\s+Appendix A\s+.*implementation qualification.*$\n(.*)\Z", text)
    return m.group(1) if m else ""


def question_blocks(app: str):
    heads = list(re.finditer(r"(?mi)^##\s+Q([1-5])\b.*$", app))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(app)
        out.append((m.group(1), app[m.start():end].strip()))
    return out


def numeric_payload_count(block: str) -> int:
    # Ignore the Q number in the heading by counting only after the first newline.
    body = block.split("\n", 1)[1] if "\n" in block else ""
    return len(NUMERIC_RE.findall(body)) + len(HEX_RE.findall(body))


def validate(path: Path):
    text = path.read_text(encoding="utf-8")
    errors = []

    for pattern in REQUIRED_HEADINGS:
        if not heading_present(text, pattern):
            errors.append(f"missing required heading matching: {pattern}")

    if not re.search(r"\b[0-9a-f]{40}\b", text, re.I):
        errors.append("issue must record a 40-hex creation-time repository SHA")

    if not re.search(r"\bINPUT-\d{3}\b", text):
        errors.append("input/source inventory must contain at least one stable INPUT-### row")

    if not re.search(r"\bBM-\d{3}\b", text) and not re.search(
        r"(?mi)^\s*BENCHMARK_STATUS\s*:\s*NOT_APPLICABLE\b", text
    ):
        errors.append("benchmark section must contain BM-### row(s) or explicit BENCHMARK_STATUS: NOT_APPLICABLE")

    if "PASS" not in text or "FAIL" not in text or "NOT_RUN" not in text:
        errors.append("issue must preserve PASS / FAIL / NOT_RUN truth explicitly")

    if not re.search(r"```(?:js|javascript|ts|typescript|py|python|java|c|cpp|csharp|go|rust|sql|bash|sh)\b", text, re.I):
        errors.append("technical issue must contain at least one code-ready implementation skeleton")

    lower = text.lower()
    for token in ("re-ground", "production output", "oracle", "tolerance"):
        if token not in lower:
            errors.append(f"anti-drift/oracle contract missing concept: {token}")

    if "product_regression" not in lower and "product regression" not in lower:
        errors.append("issue must distinguish product regression from independent oracle")

    app = appendix(text)
    if not app:
        errors.append("Appendix A implementation qualification section not found")
        return errors

    pm = re.search(r"(?mi)^\s*QUESTION_PROFILE\s*:\s*([A-Z_]+)\s*$", app)
    profile = pm.group(1) if pm else None
    if profile not in PROFILES:
        errors.append(f"QUESTION_PROFILE must be one of {sorted(PROFILES)}; found {profile}")

    blocks = question_blocks(app)
    order = [n for n, _ in blocks]
    if order != ["1", "2", "3", "4", "5"]:
        errors.append(f"Appendix A must contain exactly ordered Q1-Q5; found {order}")
        return errors

    for n, block in blocks:
        words = len(re.findall(r"\b\w+\b", block))
        if words < 40:
            errors.append(f"Q{n} is too compressed ({words} words); use a real bounded case/payload/falsifier")

    q = {n: b for n, b in blocks}
    if not re.search(r"\b(trace|walk me through|follow)\b", q["1"], re.I):
        errors.append("Q1 must require an actual production trace")
    if not CALC_RE.search(q["2"]):
        errors.append("Q2 must require a calculation or exact reconstruction")
    if not re.search(r"\b(stale|invariant|authority|reject|block)\b", q["3"], re.I) or "falsif" not in q["3"].lower():
        errors.append("Q3 must test stale/authority/invariant handling and include a falsifier")
    if not re.search(r"\bindependent\b", q["4"], re.I) or not re.search(r"\b(oracle|benchmark|reference)\b", q["4"], re.I):
        errors.append("Q4 must require an independent benchmark/oracle reconstruction")
    if not re.search(r"\bpatch\b", q["5"], re.I):
        errors.append("Q5 must require a smallest safe patch")
    if "NO-PATCH" not in q["5"]:
        errors.append("Q5 must include an explicit NO-PATCH condition")
    if not re.search(r"\b(rollback|revert|falsifier)\b", q["5"], re.I):
        errors.append("Q5 must include rollback/revert/falsifier behavior")

    anchored = sum(1 for _, block in blocks if "`" in block)
    if anchored < 3:
        errors.append("at least three questions must carry concrete live-repository anchors in backticks")

    recon = sum(1 for _, block in blocks if CALC_RE.search(block))
    if recon < 2:
        errors.append("at least two questions must require calculation/exact reconstruction")

    if profile == "NUMERICAL_ENGINEERING":
        numeric_q = [n for n, block in blocks if CALC_RE.search(block) and numeric_payload_count(block) >= 3]
        if len(numeric_q) < 2:
            errors.append(
                "NUMERICAL_ENGINEERING requires at least two calculation questions with >=3 concrete numeric payload tokens; "
                f"found {numeric_q}"
            )
    elif profile == "SOFTWARE_ENGINEERING":
        exact_q = [n for n, block in blocks if CALC_RE.search(block) and (numeric_payload_count(block) >= 2 or HEX_RE.search(block))]
        if len(exact_q) < 2:
            errors.append("SOFTWARE_ENGINEERING requires at least two exact deterministic reconstruction questions with concrete payload")

    weak_patterns = [
        r"^##\s+Q[1-5].*\n\s*Explain\s+the\s+architecture\.?\s*$",
        r"^##\s+Q[1-5].*\n\s*What\s+is\s+a\s+benchmark\??\s*$",
        r"^##\s+Q[1-5].*\n\s*Which\s+file\s+would\s+you\s+edit\??\s*$",
    ]
    for pat in weak_patterns:
        if re.search(pat, app, re.I | re.M):
            errors.append("textbook/topic-label implementation question detected")

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_issue_workorder.py <issue-draft.md>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: draft file not found: {path}")
        return 1
    errors = validate(path)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print("PASS: engineering issue draft satisfies structural, custody, anti-drift and implementation-question gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
