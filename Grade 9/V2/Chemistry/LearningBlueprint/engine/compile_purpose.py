from __future__ import annotations

from typing import Any

from common import BlueprintError, digest, load_assimilation_policy


def compile_purpose(purpose_input: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = policy or load_assimilation_policy()
    mode = purpose_input.get("mode")
    profile = policy["purpose_profiles"].get(mode)
    if not profile:
        raise BlueprintError("LEARNING_PURPOSE_UNRESOLVED", str(mode))
    packet = {
        "packet_id": f"PUR-{purpose_input['purpose_request_id']}",
        "packet_type": "PUR",
        "mode": mode,
        "terminal_capabilities": list(profile["terminal_capabilities"]),
        "representation_competition": profile["representation_competition"],
        "symbol_bridge": profile["symbol_bridge"],
        "default_fading_speed": profile["default_fading_speed"],
        "prerequisite_bypass_allowed": False
    }
    packet["digest"] = digest(packet)
    return packet
