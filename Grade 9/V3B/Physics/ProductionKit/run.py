#!/usr/bin/env python3
"""Physics-only entry gate onto the shared V3B production runtime."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Shared"))
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in {"publish", "verify-publication"}:
        from publication_host.cli import main
        raise SystemExit(main())
    if len(sys.argv) > 1 and sys.argv[1] in {"--help", "-h"}:
        print("Additional Physics commands: publish --help | verify-publication --help\n")
    from v3b.cli import main
    raise SystemExit(main(expected_subject="Physics"))
