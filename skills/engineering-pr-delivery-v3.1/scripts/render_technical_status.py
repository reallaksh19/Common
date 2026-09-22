#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from v3lib import load_yaml


def render(snapshot: dict) -> str:
    g = snapshot.get("generated_from") or {}
    e = snapshot.get("execution") or {}
    m = snapshot.get("material") or {}
    s = snapshot.get("scope") or {}
    ev = snapshot.get("evidence") or {}
    c = snapshot.get("controls") or {}
    n = snapshot.get("next") or {}
    lines = [
        "# Technical status",
        "",
        f"Authority: **{snapshot.get('authority')}**",
        f"Roadmap revision: {g.get('roadmap_revision')}",
        f"Coordination head: {g.get('coordination_head')}",
        "",
        "## Execution",
        f"- Lifecycle: {e.get('lifecycle')}",
        f"- WP: {e.get('work_package')}",
        f"- EP: {e.get('ep')}",
        f"- Lease: {e.get('lease')}",
        f"- Executor: {e.get('executor')}",
        "",
        "## Material basis",
        f"- Base: {m.get('base')}",
        f"- Material head: {m.get('head')}",
        f"- Relevant paths digest: {m.get('relevant_paths_digest')}",
        f"- Dependency digest: {m.get('dependency_digest')}",
        "",
        "## Scope",
        f"- Allowed writes: {s.get('allowed_writes') or []}",
        f"- Protected: {s.get('protected') or []}",
        f"- Prohibited: {s.get('prohibited') or []}",
        "",
        "## Accepted evidence",
        f"- Latest checkpoint: {ev.get('latest_checkpoint')}",
        f"- Validation: {ev.get('latest_material_validation') or {}}",
        "",
        "## Controls",
        f"- Execution blockers: {c.get('execution_blockers') or []}",
        f"- Handover blockers: {c.get('handover_blockers') or []}",
        f"- Delivery blockers: {c.get('delivery_blockers') or []}",
        "",
        "## Exact next work",
        f"- {n.get('immediate_material_action') or 'none'}",
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
