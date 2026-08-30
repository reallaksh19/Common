#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys
import uuid

VALID_PROFILES = {
    "FEA", "WRC_LOCAL_STRESS", "LOAD_CALC", "FIXED_FORMAT_WRITER",
    "PARSER_TOPOLOGY", "SOURCE_GOVERNANCE", "GENERAL_ENGINEERING",
}


def field(text: str, name: str):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text)
    return m.group(1).strip().strip('`') if m else None


def valid_instance(value):
    if not value or ":" not in value:
        return False
    agent_class, raw = value.split(":", 1)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9._-]*", agent_class):
        return False
    try:
        return str(uuid.UUID(raw)) == raw.lower()
    except (ValueError, AttributeError):
        return False


def run(script, *args):
    return subprocess.run([sys.executable, str(Path(__file__).with_name(script)), *map(str, args)]).returncode


def main():
    if len(sys.argv) not in {2, 3}:
        print("Usage: validate_leg_adoption.py <repo-root> [active.md]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if run("validate_repository_overlay.py", root) != 0:
        return 1
    if len(sys.argv) != 3:
        print("FAIL: active.md must be supplied explicitly for the material leg", file=sys.stderr)
        return 1
    active = Path(sys.argv[2]).resolve()
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
        "HANDOVER_PROTOCOL_VERSION": "2",
        "HANDOVER_READY": "TRUE",
        "REPORTING_CONTRACT": "ACTIVE_HANDOVER_FIRST",
        "HANDOVER_RESPONSE_REQUIRED": "ALWAYS",
        "RESPONSE_DELTA_MODE": "DELTA_ONLY",
        "OWNER_QUALIFICATION_BASELINE_DISCOVERY": "COMPLETE",
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
    if not field(at, "WORK_ITEM_KEY"):
        errors.append("ACTIVE WORK_ITEM_KEY required for new material leg")
    if field(at, "WORK_ITEM_MODE") not in {"EXCLUSIVE", "PARTITIONED"}:
        errors.append("ACTIVE WORK_ITEM_MODE must be EXCLUSIVE or PARTITIONED")
    if not valid_instance(field(at, "AGENT_INSTANCE_ID")):
        errors.append("ACTIVE AGENT_INSTANCE_ID must be <agent-class>:<UUID>")

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
    ep = root / ep_rel if ep_rel else None
    if not ep_rel:
        errors.append("ACTIVE_ENDPOINT_FILE missing")
    elif not ep.is_file():
        errors.append(f"active endpoint missing: {ep_rel}")
    elif "/agents/agentchain/" in ep.as_posix() or ep.as_posix().endswith("/agents/agentchain.md"):
        errors.append("legacy agentchain endpoint cannot govern a new material leg")

    if ep and ep.is_file():
        et = ep.read_text(encoding="utf-8")
        checks = {
            "COMMON_PROTOCOL": "engineering-pr-delivery-v2",
            "COMMON_PROTOCOL_STATUS": "CURRENT",
            "PREWORK_QUALIFICATION_READY": "TRUE",
            "QUALIFICATION_PROFILE_VERSION": "2",
            "HANDOVER_PROTOCOL_VERSION": "2",
            "HANDOVER_READY": "TRUE",
            "REPORTING_CONTRACT": "ACTIVE_HANDOVER_FIRST",
            "HANDOVER_RESPONSE_REQUIRED": "ALWAYS",
            "RESPONSE_DELTA_MODE": "DELTA_ONLY",
            "OWNER_QUALIFICATION_BASELINE_DISCOVERY": "COMPLETE",
            "QUESTION_SET_STATUS": "CURRENT",
            "QUALIFICATION_PROTOCOL_VERSION": "3",
            "QUESTION_SET_ADMISSION_REQUIREMENT": "REQUIRED_ON_TAKEOVER",
        }
        for name, wanted in checks.items():
            got = field(et, name)
            if got != wanted:
                errors.append(f"endpoint {name} expected {wanted}, found {got}")
        if field(et, "COMMON_PROTOCOL_BASIS") != basis:
            errors.append(f"endpoint COMMON_PROTOCOL_BASIS {field(et, 'COMMON_PROTOCOL_BASIS')} != ACTIVE basis {basis}")
        if field(et, "WORK_ITEM_KEY") != field(at, "WORK_ITEM_KEY"):
            errors.append("endpoint WORK_ITEM_KEY must equal ACTIVE WORK_ITEM_KEY")
        if field(et, "WORK_ITEM_MODE") != field(at, "WORK_ITEM_MODE"):
            errors.append("endpoint WORK_ITEM_MODE must equal ACTIVE WORK_ITEM_MODE")
        if field(et, "AGENT_INSTANCE_ID") != field(at, "AGENT_INSTANCE_ID"):
            errors.append("endpoint AGENT_INSTANCE_ID must equal ACTIVE AGENT_INSTANCE_ID")
        profile = field(et, "QUALIFICATION_PROFILE")
        if profile not in VALID_PROFILES:
            errors.append(f"endpoint QUALIFICATION_PROFILE invalid or missing: {profile}")
        pack = re.search(r"(?mis)^###\s+Takeover qualification pack\s*$\n(.*?)(?=^###\s+|\Z)", et)
        pack_profile = field(pack.group(1), "QUALIFICATION_PROFILE") if pack else None
        if pack_profile != profile:
            errors.append(f"qualification-pack profile {pack_profile} != endpoint profile {profile}")
        qheads = re.findall(r"(?mi)^####\s+Q([1-5])\s+—", et)
        if qheads != ["1", "2", "3", "4", "5"]:
            errors.append(f"endpoint must contain exactly ordered detailed Q1-Q5, found {qheads}")
        if not re.search(r"(?mi)^###\s+Active handover snapshot\s*$", et):
            errors.append("endpoint missing Active handover snapshot")
        visible = re.search(r"(?mis)^###\s+Active qualification questions\s*$\n(.*?)(?=^###\s+|\Z)", et)
        vq = re.findall(r"(?mi)^Q([1-5])\s*:", visible.group(1)) if visible else []
        if vq != ["1", "2", "3", "4", "5"]:
            errors.append(f"endpoint Active qualification questions must contain Q1-Q5, found {vq}")

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1

    rc = 0
    for script in (
        "validate_work_item_exclusivity.py",
        "validate_handover_readiness.py",
        "validate_owner_qualification_baseline.py",
        "validate_engineering_question_payload.py",
    ):
        rc |= run(script, root)
    if rc:
        return 1
    print("PASS: material leg uses current Common protocol, canonical v3 custody, handover-v2 reporting, exact work-item identity, Owner-baseline discovery and profile-v2 Q1-Q5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
