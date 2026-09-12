#!/usr/bin/env python3
"""Project a canonical authoring result into PR #327 and render real PDFs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from Primary.V2.Mathematics.Publication.engine.page_composer import PrimaryPageComposer
from Primary.V2.Mathematics.Publication.integration.canonical_plan_adapter import adapt_authoring_result


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authoring-result", type=Path, required=True)
    parser.add_argument("--content", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    authoring_result = load(args.authoring_result)
    content = load(args.content)
    core1_plan, core2_plan, trace = adapt_authoring_result(authoring_result, content)

    (args.output_dir / "core1_render_plan.json").write_text(json.dumps(core1_plan, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "core2_render_plan.json").write_text(json.dumps(core2_plan, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "projection_trace.json").write_text(json.dumps(trace, indent=2) + "\n", encoding="utf-8")

    composer = PrimaryPageComposer()
    core1_pdf = args.output_dir / "Core1.pdf"
    core2_pdf = args.output_dir / "Core2.pdf"
    core1_hash, core1_custody = composer.render_core1_study_guide(core1_plan, core1_pdf)
    core2_hash, core2_custody = composer.render_core2_companion(core2_plan, core2_pdf)

    if len(core1_hash) != 64 or len(core2_hash) != 64:
        raise SystemExit("publisher adapter smoke failed: PDF SHA256 length invalid")
    if not core1_pdf.exists() or core1_pdf.stat().st_size < 1000:
        raise SystemExit("publisher adapter smoke failed: Core1 PDF missing/too small")
    if not core2_pdf.exists() or core2_pdf.stat().st_size < 1000:
        raise SystemExit("publisher adapter smoke failed: Core2 PDF missing/too small")
    if core1_custody.get("page_count", 0) < 1 or core2_custody.get("page_count", 0) < 3:
        raise SystemExit("publisher adapter smoke failed: custody page counts invalid")

    custody = {
        "core1_sha256": core1_hash,
        "core2_sha256": core2_hash,
        "core1": core1_custody,
        "core2": core2_custody,
    }
    (args.output_dir / "custody.json").write_text(json.dumps(custody, indent=2) + "\n", encoding="utf-8")
    print(f"Primary Math V2 canonical→publisher adapter: PASS ({core1_hash[:12]} / {core2_hash[:12]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
