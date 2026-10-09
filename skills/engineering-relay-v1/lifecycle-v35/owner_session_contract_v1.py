"""V3.5-R14 WP1/U2: untrusted Owner-event/session observation contract.

Source links are reference claims, not authenticated original-chat sources.
Claimed stop/handover events do NOT fence another executor's credentials.
No private transcript, GitHub write, projector or positive permission is exposed.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator

from identity_contract_v1 import IdentityContractError, validate_identity

SCHEMA = "relay-lifecycle-owner-session-v1"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas/lifecycle-v35/lifecycle-owner-session-v1.schema.json"
_SOURCE_PATH = re.compile(r"^/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/(?:issues|pull)/([1-9][0-9]*)$")
_COMMENT_ID = re.compile(r"^issuecomment-[1-9][0-9]*$")


class OwnerSessionError(ValueError):
    """Malformed, contradictory or dangerously ambiguous custody evidence."""


def _mirror_url(url: str, repository: str) -> bool:
    """Allow only exact, same-repo HTTPS GitHub issue/PR comment locators.

    A GitHub URL is only *structurally plausible*: this function never GETs it.
    """
    try:
        parts = urlsplit(url)
        if parts.scheme != "https" or parts.netloc != "github.com" or parts.username or parts.password:
            return False
        if parts.query or not parts.fragment or not _COMMENT_ID.fullmatch(parts.fragment):
            return False
        if unquote(parts.path) != parts.path:
            return False
        match = _SOURCE_PATH.fullmatch(parts.path)
        return bool(match and f"{match[1]}/{match[2]}" == repository)
    except ValueError:
        return False


def _schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _linear_history(events: list[Mapping[str, Any]], kind: str) -> None:
    ids: set[str] = set()
    predecessor = None
    for index, event in enumerate(events):
        eid = event["id"]
        if eid in ids:
            raise OwnerSessionError(f"DUPLICATE_{kind}_EVENT_ID:{eid}")
        if event["predecessor_id"] != predecessor:
            raise OwnerSessionError(f"BROKEN_{kind}_HISTORY:{eid}")
        ids.add(eid)
        predecessor = eid


def validate_owner_session(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate untrusted event histories, preserving *no* authority inference.

    Cross-reference the exactly typed U1 session source commit, but do not
    reinterpret a fingerprint or a STOP_CLAIMED event as a writer lease fence.
    """
    if not isinstance(payload, dict):
        raise OwnerSessionError("ENVELOPE_OBJECT_REQUIRED")
    errors = sorted(Draft202012Validator(_schema()).iter_errors(payload),
                    key=lambda err: (tuple(map(str, err.path)), err.message))
    if errors:
        err = errors[0]
        raise OwnerSessionError("SCHEMA_INVALID:" + ".".join(map(str, err.path)) + ":" + err.message)
    try:
        source_identity = validate_identity(payload["identity"])
    except IdentityContractError as exc:
        raise OwnerSessionError("U1_IDENTITY_INVALID:" + str(exc)) from exc

    programme = payload["identity"]["programme"]
    repository = programme["repository"]
    identity_grade = payload["identity"]["owner_source_grade"]
    owner_events = payload["owner_events"]
    session_events = payload["session_events"]

    _linear_history(owner_events, "OWNER")
    _linear_history(session_events, "SESSION")
    owner_ids: set[str] = set()
    for idx, event in enumerate(owner_events):
        if (idx == 0 and event["kind"] != "REQUIREMENT_MIRROR") or (idx > 0 and event["kind"] == "REQUIREMENT_MIRROR"):
            raise OwnerSessionError("OWNER_REQUEST_ORDER_INVALID")
        grade = event["source_grade"]
        if identity_grade == "UNKNOWN" and grade != "UNKNOWN":
            raise OwnerSessionError("OWNER_GRADE_ESCALATION")
        if identity_grade == "SYNTHETIC_LAB_ONLY" and grade == "GITHUB_VERBATIM_MIRROR":
            raise OwnerSessionError("OWNER_GRADE_ESCALATION")
        if identity_grade == "GITHUB_VERBATIM_MIRROR" and grade == "SYNTHETIC_LAB_ONLY":
            raise OwnerSessionError("MIXED_OWNER_SOURCE_CONTEXT")
        if grade == "UNKNOWN":
            if event["source_url"] is not None or event["content_sha256"] is not None:
                raise OwnerSessionError("UNKNOWN_OWNER_SOURCE_HAS_MATERIAL")
        elif grade == "GITHUB_VERBATIM_MIRROR":
            if event["content_sha256"] is None or not isinstance(event["source_url"], str) or not _mirror_url(event["source_url"], repository):
                raise OwnerSessionError("GITHUB_MIRROR_LOCATOR_UNTRUSTED")
        elif event["source_url"] is not None:
            raise OwnerSessionError("SYNTHETIC_SOURCE_CANNOT_CLAIM_GITHUB")
        owner_ids.add(event["id"])

    live_claims: set[str] = set()
    started: set[str] = set()
    actor_for_session: dict[str, str] = {}
    for event in session_events:
        if event["owner_event_id"] not in owner_ids:
            raise OwnerSessionError("SESSION_UNKNOWN_OWNER_EVENT")
        sid = event["session_id"]
        if sid in actor_for_session and actor_for_session[sid] != event["actor_label"]:
            raise OwnerSessionError("SESSION_ACTOR_IDENTITY_CHANGED")
        actor_for_session[sid] = event["actor_label"]
        if event["kind"] == "START_CLAIMED":
            if sid in started:
                raise OwnerSessionError("SESSION_RESTART_AMBIGUOUS")
            started.add(sid)
            live_claims.add(sid)
        elif event["kind"] in {"HANDOVER_OFFERED", "STOP_CLAIMED"}:
            if sid not in live_claims:
                raise OwnerSessionError("SESSION_NO_LIVE_START")
            if event["kind"] == "STOP_CLAIMED":
                live_claims.remove(sid)
        # RUNNER_PREPARED does not imply that a new executor started.

    typed_session = payload["identity"]["session_source"]
    observed_current = session_events[-1]["source_commit"]
    expected_current = typed_session["commit_sha"] if typed_session["state"] == "REFERENCED" else None
    if observed_current != expected_current:
        raise OwnerSessionError("SESSION_COMMIT_IDENTITY_MISMATCH")

    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return {
        "schema": SCHEMA,
        "identity_sha256": source_identity["identity_sha256"],
        "history_sha256": "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "owner_event_count": len(owner_events),
        "session_event_count": len(session_events),
        "claimed_active_session_count": len(live_claims),
        "custody_conflict": "MULTIPLE_ACTIVE_CLAIMS" if len(live_claims) > 1 else "NOT_PROVEN_EXCLUSIVE",
        "owner_authenticity": "NOT_AUTHENTICATED",
        "session_claims": "UNVERIFIED_ACTOR_ASSERTIONS",
        "source_receipt_authenticity": "NOT_EVALUATED",
        "exclusive_execution_lease": "NOT_PROVEN",
        "writer_authorization": "NOT_GRANTED",
        "handover_admission": "HOLD_NOT_PROVEN",
        "programme_projection": "NOT_CALCULATED",
    }
