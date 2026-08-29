#!/usr/bin/env python3
from pathlib import Path
import re
import sys

REQUIRED = {
    "COMMON_POLICY_SOURCE": r"engineering-pr-delivery-v2",
    "COMMON_POLICY_REFERENCE": r"repository-agent-policy\.md",
    "COMMON_PROTOCOL_MINIMUM_BASIS": r"[0-9a-fA-F]{40}",
    "LOCAL_POLICY_SCOPE": r"PROJECT_ONLY",
    "LEGACY_RELAY_WRITES": r"FORBIDDEN",
}

BANNED_DUPLICATED_HEADINGS = [
    "## 2. Durable relay identity",
    "## 3. Continuous crash-recovery invariant",
    "## 4. Mandatory endpoint custody",
    "## 5. Five-question takeover gate",
    "## 6. Engineering-critical takeover starts READ_ONLY",
    "## 7. Qualification freshness",
    "## 9. Multi-agent coordination",
    "## 10. Validation integrity",
    "## 12. Damaged PRs and incapable agents",
    "## 13. Legacy v1 evidence and migration",
    "## 15. AUTO MODE",
]


def field(text: str, name: str):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*(?:`)?([^`\n]+)(?:`)?\s*$", text)
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_repository_overlay.py <repo-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    path = root / "AGENTS.md"
    if not path.is_file():
        print("FAIL: repository root AGENTS.md is missing")
        return 1
    text = path.read_text(encoding="utf-8")
    errors = []
    for name, pattern in REQUIRED.items():
        value = field(text, name)
        if value is None:
            errors.append(f"missing {name}")
        elif not re.search(rf"^(?:.*)?{pattern}(?:.*)?$", value):
            errors.append(f"invalid {name}={value}")
    for heading in BANNED_DUPLICATED_HEADINGS:
        if heading.lower() in text.lower():
            errors.append(f"duplicated generic Common policy heading remains in project overlay: {heading}")
    if "agents/agentchain/<CHAIN_ID>" in text or "agents/agentchain/<CHAIN_ID>/<ENDPOINT_ID>" in text:
        errors.append("project overlay still declares legacy agentchain path as canonical")
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("PASS: project AGENTS.md is a thin Common-policy overlay")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
