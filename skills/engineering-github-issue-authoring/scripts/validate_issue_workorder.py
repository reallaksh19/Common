#!/usr/bin/env python3
"""Fail-closed structural/quality validator for engineering GitHub issue drafts."""
from pathlib import Path
import re
import sys

ROLES = {"SINGLE", "PROGRAM_ROOT", "WORK_PACKAGE", "REVISION"}
PROFILES = {"NUMERICAL_ENGINEERING", "SOFTWARE_ENGINEERING", "SOURCE_GOVERNANCE"}
OVERLAP = {"SAFE_DISJOINT", "SAFE_SERIALIZED", "COORDINATION_REQUIRED", "BLOCKED_ACTIVE_SIBLING", "UNKNOWN"}
CALC_RE = re.compile(r"\b(calculate|compute|derive|reconstruct|evaluate|close the free body|by hand)\b", re.I)
NUMERIC_RE = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?", re.I)
HEX_RE = re.compile(r"\b(?:0x)?[0-9a-f]{8,}\b", re.I)


def field(text, name):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text)
    return m.group(1).strip().strip('`') if m else None


def has_heading(text, pattern):
    return bool(re.search(rf"(?mi)^#+\s+.*(?:{pattern}).*$", text))


def require_field(text, name, errors, allowed=None):
    v = field(text, name)
    if not v:
        errors.append(f"missing required field: {name}")
        return None
    if allowed and v not in allowed:
        errors.append(f"{name} must be one of {sorted(allowed)}; found {v}")
    return v


def appendix(text):
    m = re.search(r"(?mis)^#\s+Appendix A\s+.*implementation qualification.*$\n(.*)\Z", text)
    return m.group(1) if m else ""


def question_blocks(app):
    heads = list(re.finditer(r"(?mi)^##\s+Q([1-5])\b.*$", app))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(app)
        out.append((m.group(1), app[m.start():end].strip()))
    return out


def numeric_payload_count(block):
    body = block.split("\n", 1)[1] if "\n" in block else ""
    return len(NUMERIC_RE.findall(body)) + len(HEX_RE.findall(body))


def validate_questions(text, errors):
    app = appendix(text)
    if not app:
        errors.append("Appendix A implementation qualification section not found")
        return
    pm = re.search(r"(?mi)^\s*QUESTION_PROFILE\s*:\s*([A-Z_]+)\s*$", app)
    profile = pm.group(1) if pm else None
    if profile not in PROFILES:
        errors.append(f"QUESTION_PROFILE must be one of {sorted(PROFILES)}; found {profile}")
    blocks = question_blocks(app)
    order = [n for n, _ in blocks]
    if order != ["1", "2", "3", "4", "5"]:
        errors.append(f"Appendix A must contain exactly ordered Q1-Q5; found {order}")
        return
    for n, block in blocks:
        words = len(re.findall(r"\b\w+\b", block))
        if words < 40:
            errors.append(f"Q{n} is too compressed ({words} words); require a bounded case/payload/falsifier")
    q = {n: b for n, b in blocks}
    if not re.search(r"\b(trace|walk me through|follow)\b", q["1"], re.I):
        errors.append("Q1 must require an actual production trace")
    if not CALC_RE.search(q["2"]):
        errors.append("Q2 must require calculation/exact reconstruction")
    if not re.search(r"\b(stale|invariant|authority|reject|block)\b", q["3"], re.I) or "falsif" not in q["3"].lower():
        errors.append("Q3 must test stale/authority/invariant handling and include a falsifier")
    if not re.search(r"\bindependent\b", q["4"], re.I) or not re.search(r"\b(oracle|benchmark|reference)\b", q["4"], re.I):
        errors.append("Q4 must require independent benchmark/oracle reconstruction")
    if "patch" not in q["5"].lower() or "NO-PATCH" not in q["5"]:
        errors.append("Q5 must require smallest patch and explicit NO-PATCH condition")
    if not re.search(r"\b(rollback|revert|falsifier)\b", q["5"], re.I):
        errors.append("Q5 must include rollback/revert/falsifier behavior")
    if sum(1 for _, b in blocks if "`" in b) < 3:
        errors.append("at least three questions must carry concrete live-repository anchors in backticks")
    if sum(1 for _, b in blocks if CALC_RE.search(b)) < 2:
        errors.append("at least two questions must require calculation/exact reconstruction")
    if profile == "NUMERICAL_ENGINEERING":
        numeric_q = [n for n, b in blocks if CALC_RE.search(b) and numeric_payload_count(b) >= 3]
        if len(numeric_q) < 2:
            errors.append(f"NUMERICAL_ENGINEERING requires >=2 calculation questions with >=3 concrete numeric tokens; found {numeric_q}")
    if profile == "SOFTWARE_ENGINEERING":
        exact_q = [n for n, b in blocks if CALC_RE.search(b) and (numeric_payload_count(b) >= 2 or HEX_RE.search(b))]
        if len(exact_q) < 2:
            errors.append("SOFTWARE_ENGINEERING requires >=2 deterministic reconstruction questions with concrete payload")


def validate_common(text, errors):
    if not has_heading(text, r"mission"):
        errors.append("missing Mission heading")
    if not re.search(r"\b[0-9a-f]{40}\b", text, re.I):
        errors.append("issue must record a 40-hex creation-time repository SHA")
    if "PASS" not in text or "NOT_RUN" not in text:
        errors.append("issue must preserve validation truth including PASS and NOT_RUN")
    lower = text.lower()
    for token in ("re-ground", "oracle"):
        if token not in lower:
            errors.append(f"anti-drift/oracle contract missing concept: {token}")


def validate_program_root(text, errors):
    for name in ("PROGRAM_ID", "PROGRAM_BASIS_REVISION", "COMMON_INPUT_SET_ID", "COMMON_BENCHMARK_SET_ID", "COMMON_VALIDATION_SET_ID", "COMMON_ROADMAP_SET_ID"):
        require_field(text, name, errors)
    for token, label in ((r"\bTASK-\d{3}\b", "TASK-###"), (r"\bINPUT-\d{3}\b", "INPUT-###"), (r"\bBM-\d{3}\b", "BM-###"), (r"\bVAL-\d{3}\b", "VAL-###"), (r"\bRM-\d{3}\b", "RM-###"), (r"\bWP-\d{3}\b", "WP-###")):
        if not re.search(token, text):
            errors.append(f"PROGRAM_ROOT must contain at least one {label} row")
    if not has_heading(text, r"work-package.*registry|partition.*registry"):
        errors.append("PROGRAM_ROOT must contain work-package partition/dependency registry")
    if not re.search(r"SAFE_DISJOINT|SAFE_SERIALIZED|COORDINATION_REQUIRED|BLOCKED_ACTIVE_SIBLING|UNKNOWN", text):
        errors.append("PROGRAM_ROOT must state overlap disposition vocabulary/current classification")
    if not has_heading(text, r"definition of done"):
        errors.append("PROGRAM_ROOT must define program Definition of Done")


def validate_material_issue(text, role, errors):
    required_headings = [
        r"definition of done", r"current production/repository path|current production.*path|current repository.*path",
        r"technical implementation instructions", r"pass\s*/\s*fail\s*/\s*not_run criteria|pass.*fail.*not_run criteria",
        r"benchmark.*oracle criteria|benchmark / independent oracle criteria", r"anti-drift", r"negative tests.*falsifiers",
        r"explicit exclusions.*non-goals|explicit exclusions", r"validation matrix"
    ]
    for p in required_headings:
        if not has_heading(text, p):
            errors.append(f"missing required heading matching: {p}")
    if not re.search(r"```(?:js|javascript|ts|typescript|py|python|java|c|cpp|csharp|go|rust|sql|bash|sh)\b", text, re.I):
        errors.append("material implementation issue must contain at least one code-ready skeleton")
    if "product_regression" not in text.lower() and "product regression" not in text.lower():
        errors.append("material issue must distinguish product regression from independent oracle")
    validate_questions(text, errors)
    if role in {"WORK_PACKAGE", "REVISION"}:
        for name in ("PROGRAM_ID", "PARENT_WORK_ITEM_KEY", "WORK_PACKAGE_ID", "PARTITION_KEY", "INHERITED_PROGRAM_BASIS_REVISION", "INHERITED_INPUT_SET_ID", "INHERITED_BENCHMARK_SET_ID", "INHERITED_VALIDATION_SET_ID", "INHERITED_ROADMAP_SET_ID", "PARENT_TASK_ROWS", "USES_INPUT_ROWS", "USES_BENCHMARK_ROWS", "USES_VALIDATION_ROWS"):
            require_field(text, name, errors)
        for name in ("OWNED_AUTHORITY_DOMAINS", "OWNED_PATHS_OR_COMPONENTS", "PROTECTED_SIBLING_DOMAINS", "DEPENDENCY_PREDECESSORS"):
            if name not in text:
                errors.append(f"child issue missing partition declaration: {name}")
        overlap = field(text, "OVERLAP_CLASSIFICATION")
        if not overlap:
            m = re.search(r"(?mi)Overlap classification[^:]*:\s*([A-Z_]+)", text)
            overlap = m.group(1) if m else None
        if overlap not in OVERLAP:
            errors.append(f"child issue must have valid overlap classification; found {overlap}")
        if role == "REVISION":
            pred = require_field(text, "PREDECESSOR_WORK_ITEM_KEY", errors)
            seq = require_field(text, "REVISION_SEQUENCE", errors)
            if pred and pred == "NONE":
                errors.append("REVISION requires a predecessor work item")
            if seq and seq in {"0", "NONE"}:
                errors.append("REVISION_SEQUENCE must be >0")


def validate(path):
    text = path.read_text(encoding="utf-8")
    errors = []
    role = field(text, "ISSUE_ROLE") or "SINGLE"
    if role not in ROLES:
        errors.append(f"ISSUE_ROLE must be one of {sorted(ROLES)}; found {role}")
        return errors
    validate_common(text, errors)
    if role == "PROGRAM_ROOT":
        validate_program_root(text, errors)
    else:
        if not re.search(r"\bINPUT-\d{3}\b", text) and role == "SINGLE":
            errors.append("SINGLE issue must contain at least one stable INPUT-### row")
        if not re.search(r"\bBM-\d{3}\b", text) and "BENCHMARK_STATUS: NOT_APPLICABLE" not in text:
            errors.append("material issue must contain BM-### or explicit BENCHMARK_STATUS: NOT_APPLICABLE")
        validate_material_issue(text, role, errors)
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
        for e in errors:
            print("FAIL:", e)
        return 1
    print("PASS: engineering issue draft satisfies role/topology, custody, overlap, anti-drift and qualification gates")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
