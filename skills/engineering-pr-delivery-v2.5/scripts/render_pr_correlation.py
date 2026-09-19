#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from pr_correlation import derive_current_correlations,render_markdown


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("repo_root",nargs="?",default=".")
    ap.add_argument("--output")
    a=ap.parse_args();root=Path(a.repo_root).resolve()
    rows,errors=derive_current_correlations(root)
    if errors:
        for error in errors:print(f"ERROR: {error}")
        raise SystemExit(2)
    text=render_markdown(rows)
    if a.output:Path(a.output).write_text(text,encoding="utf-8")
    else:print(text,end="")


if __name__=="__main__":
    main()
