#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

VALID_PROFILES = {
    "FEA", "WRC_LOCAL_STRESS", "LOAD_CALC", "FIXED_FORMAT_WRITER",
    "PARSER_TOPOLOGY", "SOURCE_GOVERNANCE", "GENERAL_ENGINEERING",
}


def field(text: str, name: str):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text)
    return m.group(1).strip().strip('`') if m else None


def run_overlay(root: Path):
    script = Path(__file__).with_name("validate_repository_overlay.py")
    return subprocess.run([sys.executable, str(script), str(root)]).returncode


def main():
    if len(sys.argv) not in {2, 3}:
        print("Usage: validate_leg_adoption.py <repo-root> [active.md]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if run_overlay(root) != 0:
        return 1

    if len(sys.argv) == 3:
        active = Path(sys.argv[2]).resolve()
    else:
        print("FAIL: active.md must be supplied explicitly for the material leg", file=sys.stderr)
        return 1
    if not active.is_file():
        print(f"FAIL: ACTIVE.md missing: {active}")
        return 1
    try:
        active.relative_to(root / "agents" / "chains")
    except ValueError:
        print("FAIL: ACTIVE.md must be under canonical agents/chains/<CHAIN_ID>/")
        return 1

    at = active.read_text(encoding="utf-8")
    errors = []
    expected = {
        "CHAIN_STATE_VERSION": "3",
        "COMMON_PROTOCOL": "engineering-pr-delivery-v2",
        "COMMON_PROTOCOL_STATUS": "CURRENT",
        "HANDOVER_READY": "TRUE",
    }
    for name, wanted in expected.items():
        got = field(at, name)
        if got != wanted:
            errors.append(f"ACTIVE {name} expected {wanted}, found {got}")
    basis = field(at, "COMMON_PROTOCOL_BASIS")
    if not basis or not re.fullmatch(r"[0-9a-fA-F]{40}", basis):
        errors.append("ACTIVE COMMON_PROTOCOL_BASIS must be the 40-hex Common commit actually read")
    history_root = field(at, "MATERIAL_HISTORY_ROOT_BASE")
    if not history_root or not re.fullmatch(r"[0-9a-fA-F]{40}", history_root):
        errors.append("ACTIVE MATERIAL_HISTORY_ROOT_BASE must be a 40-hex commit before the chain's first material batch")

    prework_rel = field(at, "MATERIAL_LEG_PREWORK_ENDPOINT_FILE")
    if not prework_rel:
        errors.append("ACTIVE missing MATERIAL_LEG_PREWORK_ENDPOINT_FILE")
    else:
        prework = root / prework_rel
        if not prework.is_file():
            errors.append(f"material-leg prework endpoint missing: {prework_rel}")
        try:
            prework.relative_to(root / "agents" / "chains")
        except ValueError:
            errors.append("MATERIAL_LEG_PREWORK_ENDPOINT_FILE must be under agents/chains/**")

    ep_rel = field(at, "ACTIVE_ENDPOINT_FILE")
    if not ep_rel:
        errors.append("ACTIVE_ENDPOINT_FILE missing")
        ep = None
    else:
        ep = root / ep_rel
        if not ep.is_file():
            errors.append(f"active endpoint missing: {ep_rel}")
        elif "/agents/agentchain/" in ep.as_posix() or ep.as_posix().endswith("/agents/agentchain.md"):
            errors.append("legacy agentchain endpoint cannot govern a new material leg")

    if ep and ep.is_file():
        et = ep.read_text(encoding="utf-8")
        checks = {
            "COMMON_PROTOCOL": "engineering-pr-delivery-v2",
            "COMMON_PROTOCOL_STATUS": "CURRENT",
            "PREWORK_QUALIFICATION_READY": "TRUE",
            "HANDOVER_READY": "TRUE",
            "QUESTION_SET_STATUS": "CURRENT",
            "QUALIFICATION_PROTOCOL_VERSION": "3",
            "QUESTION_SET_ADMISSION_REQUIREMENT": "REQUIRED_ON_TAKEOVER",
        }
        for name, wanted in checks.items():
            got = field(et, name)
            if got != wanted:
                errors.append(f"endpoint {name} expected {wanted}, found {got}")
        ebasis = field(et, "COMMON_PROTOCOL_BASIS")
        if ebasis != basis:
            errors.append(f"endpoint COMMON_PROTOCOL_BASIS {ebasis} != ACTIVE basis {basis}")
        profile = field(et, "QUALIFICATION_PROFILE")
        if profile not in VALID_PROFILES:
            errors.append(f"endpoint QUALIFICATION_PROFILE invalid or missing: {profile}")
        pack_profile = None
        pack = re.search(r"(?mis)^###\s+Takeover qualification pack\s*$\n(.*?)(?=^###\s+|\Z)", et)
        if pack:
            pack_profile = field(pack.group(1), "QUALIFICATION_PROFILE")
        if pack_profile != profile:
            errors.append(f"qualification-pack profile {pack_profile} != endpoint profile {profile}")
        qheads = re.findall(r"(?mi)^####\s+Q([1-5])\s+—", et)
        if qheads != ["1", "2", "3", "4", "5"]:
            errors.append(f"endpoint must contain exactly ordered Q1-Q5, found {qheads}")
        snapshot = re.search(r"(?mis)^###\s+Handover snapshot\s*$\n(.*?)(?=^###\s+|\Z)", et)
        if not snapshot:
            errors.append("endpoint missing Handover snapshot")
        else:
            for n in range(1, 6):
                if not re.search(rf"(?mi)^Q{n}\s*:", snapshot.group(1)):
                    errors.append(f"Handover snapshot missing visible Q{n}")

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("PASS: material leg uses current Common protocol, canonical v3 custody, material-history root, prework anchor and profiled Q1-Q5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
