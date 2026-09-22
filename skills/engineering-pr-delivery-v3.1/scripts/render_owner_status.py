#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from v3lib import load_yaml


def render(snapshot: dict) -> str:
    p = snapshot.get("programme") or {}
    e = snapshot.get("execution") or {}
    c = snapshot.get("controls") or {}
    d = snapshot.get("delivery") or {}
    n = snapshot.get("next") or {}
    o = snapshot.get("owner") or {}
    lines = [
        "# Owner Roadmap",
        "",
        f"Roadmap revision: **{(snapshot.get('generated_from') or {}).get('roadmap_revision')}**",
        f"Accepted outcome progress: **{p.get('accepted_progress')}%**",
        "",
        "## Outcome",
        str(o.get("outcome") or "Unknown"),
        "",
        "## Current goal",
        str(o.get("current_goal") or "Unknown"),
        "",
        "## Current execution",
        f"- Lifecycle: **{e.get('lifecycle')}**",
        f"- Work package: **{e.get('work_package') or 'NONE'}**",
        f"- EP / lease: **{e.get('ep') or 'NONE'} / {e.get('lease') or 'NONE'}**",
        f"- Executor: **{e.get('executor') or 'NONE'}**",
        "",
        "## Blockers by consequence",
        f"- Execution: {', '.join(c.get('execution_blockers') or []) or 'none'}",
        f"- Handover: {', '.join(c.get('handover_blockers') or []) or 'none'}",
        f"- Delivery: {', '.join(c.get('delivery_blockers') or []) or 'none'}",
        f"- Informational: {', '.join(c.get('informational') or []) or 'none'}",
        "",
        "## Next",
        f"- Material: {n.get('immediate_material_action') or 'none'}",
        f"- Delivery: {n.get('delivery_action') or 'none'}",
        "",
        "## Delivery",
        f"- PR: {d.get('pr') or 'none'}; Issue: {d.get('issue') or 'none'}; lifecycle: {d.get('lifecycle')}",
        f"- Merge authorized: **{'YES' if d.get('merge_authorized') else 'NO'}**",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", help="Path to generated CURRENT_SNAPSHOT.yaml")
    args = parser.parse_args()
    print(render(load_yaml(Path(args.snapshot))), end="")


if __name__ == "__main__":
    main()
