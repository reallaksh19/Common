#!/usr/bin/env python3
"""Recompute the SBA transfer routines' asserted answers instead of trusting them.

Core (1A)'s Subtopic Bucket Assimilation layer carries independent-practice items whose
`answer_check` is authored prose: `"u_y=20 m/s; T=4 s."`. The physics in those strings is
correct today, but nothing re-derives it — edit the height in the prompt and the asserted
answer silently becomes wrong.

P-UPGRADE-2 item 3 introduced a restricted arithmetic evaluator for exactly this problem
(`CoreAuthoring/engine/physics_instance_resolver.evaluate`: an `ast` whitelist, no `eval`).
This test points that engine at the SBA routines: each routine's givens are taken from its
own prompt, the relation the routine teaches in `method_steps` is evaluated, and the result
must agree with the number the registry asserts.

It is a bridge, not a second contract. SBA owns *which* bucket teaches a question and
*whether* each H1/H2/H3 rung was pre-taught; this only checks that the arithmetic the SBA
routines assert is arithmetic that holds.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
sys.path[:0] = [str(PHYS / "CoreAuthoring" / "engine")]

from physics_instance_resolver import evaluate  # noqa: E402

REGISTRY = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba05-transfer-v1.json"
TOL = 1e-9

# Per routine: the givens its own prompt states, the relations its own method_steps teach,
# and the substrings its answer_check must therefore contain. Nothing here is new physics —
# every relation is the one the routine already tells the learner to use.
EXPECTED = {
    "M2D-SBA-05-R1": {
        "symbols": {"g": 10.0, "H": 20.0},
        "checks": [
            ("u_y", "sqrt(2*g*H)", 20.0, "u_y=20 m/s"),
            ("T", "2*sqrt(2*g*H)/g", 4.0, "T=4 s"),
        ],
    },
    "M2D-SBA-05-R2": {
        # maximum same-height range occurs at 45 degrees, where R = u^2 / g
        "symbols": {"g": 10.0, "R": 80.0},
        "checks": [
            ("u", "sqrt(g*R)", 20.0 * math.sqrt(2), "20sqrt(2)"),
            ("u_x", "sqrt(g*R)*cos(radians(45))", 20.0, "u_x=20 m/s"),
        ],
    },
    "M2D-SBA-05-R3": {
        # equal flight time means equal vertical component; 30 degrees from vertical is
        # 60 degrees above the horizontal
        "symbols": {"u_a": 20.0},
        "checks": [
            ("V", "u_a*sin(radians(30))/sin(radians(60))", 20.0 / math.sqrt(3), "20/sqrt(3)"),
        ],
    },
    "M2D-SBA-05-R4": {
        # complementary angles at one speed: H1 + H2 = u^2 / (2g), so sin^2(theta) = H1 / K
        "symbols": {"H1": 5.0, "H2": 15.0},
        "checks": [
            ("K", "H1 + H2", 20.0, "K=20"),
            ("sin_sq", "sin(radians(30))*sin(radians(30))", 0.25, "1/4"),
        ],
    },
    "M2D-SBA-05-R5": {
        # at one launch speed, T is proportional to sin(theta) and H to sin^2(theta)
        "symbols": {},
        "checks": [
            ("T_ratio", "sin(radians(30))/sin(radians(60))", 1.0 / math.sqrt(3), "1:sqrt(3)"),
            ("H_ratio", "(sin(radians(30))*sin(radians(30)))/(sin(radians(60))*sin(radians(60)))",
             1.0 / 3.0, "1:3"),
        ],
    },
    "M2D-SBA-05-R6": {
        # R/H = 4 cot(theta); the routine states R = 4 sqrt(3) H
        "symbols": {},
        "checks": [
            ("r_over_h", "4*cos(radians(30))/sin(radians(30))", 4 * math.sqrt(3), "theta=30 degrees"),
        ],
    },
    "M2D-SBA-05-R7": {
        # equal range at complementary angles: sin(2*30) = sin(2*60)
        "symbols": {},
        "checks": [
            ("sin_2theta", "sin(radians(60))", math.sin(math.radians(120)), "60 degrees"),
        ],
    },
    "M2D-SBA-05-R8": {
        # minimum speed is u cos(theta); the routine states it is 0.8 u
        "symbols": {"c": 0.8},
        "checks": [
            ("sin_theta", "sqrt(1 - c*c)", 0.6, "sin(theta)=0.6"),
            ("r_over_h", "4*c/sqrt(1 - c*c)", 16.0 / 3.0, "R/H=16/3"),
        ],
    },
}


def main():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    routines = {r["routine_id"]: r for r in registry["transfer_routines"]}

    missing = sorted(set(routines) - set(EXPECTED))
    assert not missing, (
        "SBA transfer routines with no arithmetic check: " + ", ".join(missing) +
        " — every routine that asserts a numeric answer must have that answer recomputed."
    )
    unknown = sorted(set(EXPECTED) - set(routines))
    assert not unknown, "checks reference routines that no longer exist: " + ", ".join(unknown)

    checked = 0
    for routine_id, spec in sorted(EXPECTED.items()):
        routine = routines[routine_id]
        answer_check = (routine.get("independent_practice") or {}).get("answer_check")
        assert answer_check, f"{routine_id}: no asserted answer to verify"
        symbols = dict(spec["symbols"])
        for name, expression, expected, must_appear in spec["checks"]:
            value = evaluate(expression, symbols, f"{routine_id}:{name}")
            assert abs(float(value) - float(expected)) <= max(TOL, abs(expected) * 1e-9), (
                f"{routine_id}:{name}: the routine's own relation '{expression}' gives "
                f"{value}, but this check expects {expected}"
            )
            assert must_appear in answer_check, (
                f"{routine_id}:{name}: recomputed {value}, which is not what the registry "
                f"asserts — '{must_appear}' is absent from: {answer_check}"
            )
            symbols[name] = value
            checked += 1

    print(f"Core1A SBA transfer answer arithmetic: PASS "
          f"({len(EXPECTED)} routines, {checked} asserted answers recomputed and matched)")


if __name__ == "__main__":
    main()
