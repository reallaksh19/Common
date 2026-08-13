#!/usr/bin/env python3
"""Compare anchor and candidate difficulty vectors for Grade 9 bank screening.

Usage:
  python difficulty_check.py input.json

Input shape:
{
  "anchor": {"conceptual": 8.5, "recognition": 9, ...},
  "candidate": {...},
  "mode": "same_level" | "challenge"
}

The generic composite is Mathematics-oriented. Subject skills may add their own
human review dimensions; this script is only a deterministic screening aid.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WEIGHTS = {
    "conceptual": 0.25,
    "recognition": 0.25,
    "reasoning_steps": 0.15,
    "algebra": 0.15,
    "hidden_structure": 0.10,
    "constraints_cases": 0.10,
}


def score(vector: dict) -> float:
    missing = [k for k in WEIGHTS if k not in vector]
    if missing:
        raise ValueError(f"Missing difficulty dimensions: {', '.join(missing)}")
    return sum(float(vector[k]) * w for k, w in WEIGHTS.items())


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: difficulty_check.py input.json", file=sys.stderr)
        return 2

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    anchor = data["anchor"]
    candidate = data["candidate"]
    mode = data.get("mode", "same_level")

    a = score(anchor)
    c = score(candidate)
    delta = c - a

    if mode == "same_level":
        scalar_pass = abs(delta) <= 0.4
    elif mode == "challenge":
        scalar_pass = 0.8 <= delta <= 1.3
    else:
        raise ValueError("mode must be 'same_level' or 'challenge'")

    profile_deltas = {
        k: round(float(candidate.get(k, 0)) - float(anchor.get(k, 0)), 3)
        for k in set(anchor) | set(candidate)
        if isinstance(anchor.get(k, candidate.get(k)), (int, float))
        and isinstance(candidate.get(k, anchor.get(k)), (int, float))
    }

    result = {
        "anchor_score": round(a, 3),
        "candidate_score": round(c, 3),
        "delta": round(delta, 3),
        "mode": mode,
        "scalar_screen": "PASS" if scalar_pass else "FAIL",
        "profile_deltas": profile_deltas,
        "human_review_required": True,
        "note": "A scalar PASS is necessary but not sufficient; compare cognitive profile and solution path.",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if scalar_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
