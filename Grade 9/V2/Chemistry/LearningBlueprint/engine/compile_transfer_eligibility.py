from __future__ import annotations

from typing import Any

from common import BlueprintError, digest, load_transfer_policy

NOVELTY = ["SAME_STRUCTURE", "NEAR_TRANSFER", "INTERLEAVED_TRANSFER", "EXTENDED_WITHIN_SCOPE"]


def _index_unique(rows: list[dict[str, Any]], key: str, code: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        if not value or value in out:
            raise BlueprintError(code, str(value))
        out[value] = row
    return out


def _novelty_leq(value: str, maximum: str, order: list[str]) -> bool:
    try:
        return order.index(value) <= order.index(maximum)
    except ValueError as exc:
        raise BlueprintError("TRANSFER_NOVELTY_LEVEL_INVALID", f"{value}:{maximum}") from exc


def _validate_bindings(
    assimilation: dict[str, Any],
    taught_state: dict[str, Any],
    envelope: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    if assimilation.get("validation_status") != "PASS" or assimilation.get("manuscript_ready") is not True:
        raise BlueprintError("TRANSFER_ASSIMILATION_NOT_READY")
    if taught_state.get("assimilation_packet_ref") != assimilation.get("packet_id"):
        raise BlueprintError("TRANSFER_TAUGHT_STATE_ASSIMILATION_REF_MISMATCH")
    if taught_state.get("assimilation_digest") != assimilation.get("digest"):
        raise BlueprintError("TRANSFER_TAUGHT_STATE_ASSIMILATION_DIGEST_MISMATCH")
    if taught_state.get("purpose_mode") != assimilation.get("purpose_mode"):
        raise BlueprintError("TRANSFER_PURPOSE_BINDING_MISMATCH")
    if envelope.get("assimilation_packet_ref") != assimilation.get("packet_id"):
        raise BlueprintError("TRANSFER_ENVELOPE_ASSIMILATION_REF_MISMATCH")
    if envelope.get("assimilation_digest") != assimilation.get("digest"):
        raise BlueprintError("TRANSFER_ENVELOPE_ASSIMILATION_DIGEST_MISMATCH")

    semantic = _index_unique(assimilation.get("capability_treatments") or [], "capability_ref", "TRANSFER_SEMANTIC_SCOPE_DUPLICATE")
    taught = _index_unique(taught_state.get("capabilities") or [], "capability_ref", "TRANSFER_TAUGHT_STATE_DUPLICATE")
    env = _index_unique(envelope.get("capabilities") or [], "capability_ref", "TRANSFER_ENVELOPE_DUPLICATE")

    if set(taught) != set(semantic):
        raise BlueprintError("TRANSFER_TAUGHT_STATE_CAPABILITY_COVERAGE_MISMATCH")
    unknown = sorted(set(env) - set(semantic))
    if unknown:
        raise BlueprintError("TRANSFER_ENVELOPE_EXPANDS_SEMANTIC_SCOPE", ",".join(unknown))
    for cap, row in env.items():
        combos = set(row.get("allowed_combination_with") or [])
        outside = sorted(combos - set(env))
        if outside:
            raise BlueprintError("TRANSFER_ENVELOPE_COMBINATION_OUTSIDE_ENVELOPE", f"{cap}:{','.join(outside)}")
    return semantic, taught, env


def compile_transfer_eligibility(
    assimilation: dict[str, Any],
    taught_state: dict[str, Any],
    envelope: dict[str, Any],
    request: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or load_transfer_policy()
    semantic, taught, env = _validate_bindings(assimilation, taught_state, envelope)

    purpose = assimilation.get("purpose_mode")
    profiles = policy.get("purpose_profiles") or {}
    if purpose not in profiles:
        raise BlueprintError("TRANSFER_PURPOSE_UNSUPPORTED", str(purpose))
    profile = profiles[purpose]
    order = policy.get("novelty_order") or NOVELTY

    candidates = request.get("candidates") or []
    if not candidates:
        raise BlueprintError("TRANSFER_CANDIDATES_MISSING")
    ids = [row.get("item_id") for row in candidates]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise BlueprintError("TRANSFER_CANDIDATE_IDS_INVALID")

    decisions: list[dict[str, Any]] = []
    eligible: list[str] = []
    blocked: list[str] = []

    for candidate in candidates:
        item_id = candidate["item_id"]
        required = candidate.get("required_capability_refs") or []
        if not required or len(required) != len(set(required)):
            raise BlueprintError("TRANSFER_CANDIDATE_CAPABILITY_REFS_INVALID", item_id)
        primary = candidate.get("primary_capability_ref")
        if primary not in required:
            raise BlueprintError("TRANSFER_PRIMARY_CAPABILITY_NOT_REQUIRED", item_id)

        reasons: list[str] = []
        details: list[str] = []

        semantic_ok = all(cap in semantic for cap in required)
        if not semantic_ok:
            reasons.append("OUTSIDE_VALIDATED_SEMANTIC_SCOPE")
            details.extend(f"semantic_scope_missing:{cap}" for cap in required if cap not in semantic)
        if candidate.get("new_semantic_claims"):
            semantic_ok = False
            reasons.append("NEW_SEMANTICS_FORBIDDEN")
            details.extend(f"new_semantic_claim:{claim}" for claim in candidate["new_semantic_claims"])

        envelope_ok = all(cap in env for cap in required)
        if not envelope_ok:
            reasons.append("OUTSIDE_TRANSFER_ENVELOPE")
            details.extend(f"transfer_envelope_missing:{cap}" for cap in required if cap not in env)
        if primary in env:
            primary_row = env[primary]
            if candidate.get("question_family") not in (primary_row.get("allowed_question_families") or []):
                envelope_ok = False
                reasons.append("QUESTION_FAMILY_NOT_AUTHORIZED")
                details.append(f"question_family:{candidate.get('question_family')}")
            for support in required:
                if support == primary:
                    continue
                if support not in set(primary_row.get("allowed_combination_with") or []):
                    envelope_ok = False
                    reasons.append("CAPABILITY_COMBINATION_NOT_AUTHORIZED")
                    details.append(f"combination:{primary}+{support}")
        novelty = candidate.get("novelty_level")
        for cap in required:
            if cap in env and not _novelty_leq(novelty, env[cap]["max_novelty_level"], order):
                envelope_ok = False
                if "NOVELTY_EXCEEDS_TRANSFER_ENVELOPE" not in reasons:
                    reasons.append("NOVELTY_EXCEEDS_TRANSFER_ENVELOPE")
                details.append(f"envelope_novelty:{cap}:{novelty}>{env[cap]['max_novelty_level']}")

        support = candidate.get("support_mode")
        purpose_ok = True
        if support not in profile.get("allowed_support_modes", []):
            purpose_ok = False
            reasons.append("SUPPORT_MODE_NOT_ALLOWED_FOR_PURPOSE")
            details.append(f"support_mode:{support}")
        if not _novelty_leq(novelty, profile["max_novelty_level"], order):
            purpose_ok = False
            reasons.append("NOVELTY_EXCEEDS_PURPOSE")
            details.append(f"purpose_novelty:{novelty}>{profile['max_novelty_level']}")
        if len(required) > int(profile["max_capability_count"]):
            purpose_ok = False
            reasons.append("CAPABILITY_COMBINATION_EXCEEDS_PURPOSE")
            details.append(f"capability_count:{len(required)}>{profile['max_capability_count']}")

        required_flags = (profile.get("required_flags_by_support_mode") or {}).get(support)
        taught_ok = required_flags is not None
        if required_flags is None:
            if "SUPPORT_MODE_NOT_ALLOWED_FOR_PURPOSE" not in reasons:
                reasons.append("TAUGHT_STATE_RULE_UNRESOLVED")
        else:
            for cap in required:
                receipt = taught.get(cap)
                if receipt is None:
                    taught_ok = False
                    reasons.append("TAUGHT_STATE_MISSING")
                    details.append(f"taught_state_missing:{cap}")
                    continue
                missing_flags = [flag for flag in required_flags if receipt.get(flag) is not True]
                if missing_flags:
                    taught_ok = False
                    if "TAUGHT_STATE_INCOMPLETE" not in reasons:
                        reasons.append("TAUGHT_STATE_INCOMPLETE")
                    details.append(f"taught_state_incomplete:{cap}:{','.join(missing_flags)}")

        reasons = list(dict.fromkeys(reasons))
        details = list(dict.fromkeys(details))
        status = "ELIGIBLE" if all([semantic_ok, envelope_ok, taught_ok, purpose_ok]) else "BLOCKED"
        (eligible if status == "ELIGIBLE" else blocked).append(item_id)
        decisions.append({
            "item_id": item_id,
            "status": status,
            "required_capability_refs": required,
            "question_family": candidate.get("question_family"),
            "novelty_level": novelty,
            "support_mode": support,
            "intersection": {
                "validated_semantic_scope": semantic_ok,
                "transfer_envelope": envelope_ok,
                "taught_state": taught_ok,
                "purpose": purpose_ok,
            },
            "reason_codes": reasons,
            "reason_details": details,
        })

    packet = {
        "packet_id": f"X-{request['transfer_request_id']}",
        "packet_type": "X",
        "assimilation_packet_ref": assimilation["packet_id"],
        "assimilation_digest": assimilation["digest"],
        "taught_state_ref": taught_state["packet_id"],
        "taught_state_digest": taught_state["digest"],
        "purpose_mode": purpose,
        "envelope_ref": envelope["envelope_id"],
        "envelope_digest": digest(envelope),
        "transfer_request_id": request["transfer_request_id"],
        "decisions": decisions,
        "eligible_item_ids": eligible,
        "blocked_item_ids": blocked,
        "release_state": "TRANSFER_ITEMS_RELEASED" if eligible else "NO_TRANSFER_ITEMS_RELEASED",
    }
    packet["digest"] = digest(packet)
    return packet
