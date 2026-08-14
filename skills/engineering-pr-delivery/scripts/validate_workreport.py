#!/usr/bin/env python3
from pathlib import Path
import re, sys

REQUIRED_HEADINGS = [
    "CURRENT RECOVERY STATE",
    "Handover in 60 Seconds",
    "Repository Ground Truth",
    "Mission / Scope / Acceptance",
    "Current Implementation State",
    "Active Engineering Item Register",
    "Authority and Invariants",
    "Current Validation",
    "Changed-File Ledger",
    "Continuation State",
    "APPENDIX A",
]

REQUIRED_FIELDS = [
    "HANDOVER_READINESS:",
    "PR_RECOVERY_STATE:",
    "TAKEOVER_AUTHORITY:",
    "REPORT_BASIS_HEAD:",
    "MAIN_HEAD_LAST_CHECKED:",
    "REPORT_SYNC:",
    "APPENDIX_A_STATUS:",
    "GROUNDING_EPOCH:",
    "EXACT_NEXT_ACTION:",
]

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_workreport.py <workreport.md>", file=sys.stderr)
        return 2
    p = Path(sys.argv[1])
    text = p.read_text(encoding="utf-8")
    errors = []
    for h in REQUIRED_HEADINGS:
        if h.lower() not in text.lower():
            errors.append(f"missing heading/section: {h}")
    for f in REQUIRED_FIELDS:
        if f not in text:
            errors.append(f"missing recovery field: {f}")
    if "HANDOVER_READINESS: READY" in text:
        if "REPORT_SYNC: CURRENT" not in text:
            errors.append("READY requires REPORT_SYNC: CURRENT")
        if "APPENDIX_A_STATUS: STALE" in text:
            errors.append("READY cannot have stale Appendix A")
    if re.search(r"\bPR_PENDING_workreport\.md\b", text):
        errors.append("single shared PR_PENDING_workreport.md is forbidden; use unique WIP ID")
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("PASS: work report structural recovery gate")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
