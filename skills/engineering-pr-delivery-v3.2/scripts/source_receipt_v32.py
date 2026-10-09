"""WP1 candidate only: offline, source-identifiable CHECKPOINT_FACTS_V1 receipts.

This read-only parser is NOT a credentialed GitHub adapter or V2 DELP producer.
It does not alter legacy project().input_digest, source facts, or authority.
Only a later, independently qualified native provider adapter may attest
transport/source currentness and build a cross-consumer EvidenceBasisV2.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Mapping
from typing import Any

import yaml

RECEIPT_SCHEMA = "relay-v3.2-source-receipt-v2"
SET_SCHEMA = "relay-v3.2-source-receipt-set-v2"
LEGACY_FACTS_KEY = "CHECKPOINT_FACTS_V1"
LEGACY_FACTS_SCHEMA = "relay-v3.2-delp-checkpoint-facts"
ASSOCIATIONS = frozenset({"OWNER", "MEMBER", "COLLABORATOR"})
_SHA = re.compile(r"sha256:[0-9a-f]{64}\Z")
_REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
_FENCE = re.compile(
    r"^[ ]{0,3}```[ \t]*(?:ya?ml)?[ \t]*\r?\n(?P<body>[ \t]*"
    + LEGACY_FACTS_KEY + r":.*?)\r?\n[ ]{0,3}```[ \t]*(?=\r?$)",
    re.DOTALL | re.MULTILINE,
)
_FACTS_MARKER = re.compile(r"(?m)^[ \t]*" + LEGACY_FACTS_KEY + r"[ \t]*:")


class ReceiptError(ValueError):
    """Invalid or unavailable source payload; no partial trusted receipt."""


def _canonical_json(value: Any) -> str:
    """NFC-only UTF-8 JSON with sorted keys; no float coercion or NaN."""
    def check(item: Any) -> None:
        if isinstance(item, str):
            if not unicodedata.is_normalized("NFC", item):
                raise ReceiptError("NON_CANONICAL_UNICODE")
            try:
                item.encode("utf-8", "strict")
            except UnicodeEncodeError as exc:
                raise ReceiptError("INVALID_UNICODE") from exc
        elif item is None or isinstance(item, bool) or type(item) is int:
            return
        elif isinstance(item, (list, tuple)):
            for inner in item:
                check(inner)
        elif isinstance(item, Mapping):
            for key, inner in item.items():
                if not isinstance(key, str):
                    raise ReceiptError("NON_STRING_YAML_KEY")
                check(key)
                check(inner)
        else:
            raise ReceiptError("NON_CANONICAL_JSON_VALUE")
    check(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False)


def digest(domain: str, value: Any) -> str:
    if not re.fullmatch(r"V32/[A-Z_]+/V2", domain):
        raise ReceiptError("INVALID_DIGEST_DOMAIN")
    payload = (domain + "\0" + _canonical_json(value)).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


class _NoDuplicateKeysLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: yaml.SafeLoader, node: yaml.MappingNode) -> dict:
    loader.flatten_mapping(node)
    result: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if type(key) is not str:
            raise ReceiptError("NON_STRING_YAML_KEY")
        if key in result:
            raise ReceiptError("DUPLICATE_YAML_KEY")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


_NoDuplicateKeysLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def extract_blocks(body: str) -> list[tuple[int, dict[str, Any]]]:
    """Match the existing DELP V1 fence grammar; strict V2 YAML semantics."""
    if not isinstance(body, str):
        raise ReceiptError("COMMENT_BODY_UNAVAILABLE")
    matches = list(_FENCE.finditer(body))
    # Checking only `not matches` allowed a mixed valid+malformed comment to
    # silently drop the malformed facts block and treat the set as complete.
    # Every candidate facts marker must belong to a recognized DELP fence.
    markers = list(_FACTS_MARKER.finditer(body))
    for marker in markers:
        if not any(m.start("body") <= marker.start() < m.end("body") for m in matches):
            raise ReceiptError("FACTS_FENCE_UNPARSEABLE")
    blocks: list[tuple[int, dict[str, Any]]] = []
    for match in matches:
        try:
            parsed = yaml.load(match.group("body"), Loader=_NoDuplicateKeysLoader)
        except ReceiptError:
            raise
        except yaml.YAMLError as exc:
            raise ReceiptError("MALFORMED_FACTS_YAML") from exc
        if not isinstance(parsed, dict) or set(parsed) != {LEGACY_FACTS_KEY}:
            raise ReceiptError("FACTS_BLOCK_NOT_MAPPING")
        facts = parsed[LEGACY_FACTS_KEY]
        if not isinstance(facts, dict):
            raise ReceiptError("FACTS_CONTENT_NOT_MAPPING")
        facts = dict(facts)
        facts.setdefault("schema", LEGACY_FACTS_SCHEMA)
        _canonical_json(facts)  # Fail before returning an ambiguous source.
        blocks.append((match.start(), facts))
    return blocks


def _positive_int(item: Any, name: str) -> int:
    if type(item) is not int or item < 1:
        raise ReceiptError(name)
    return item


def _trust_decision(policy: Mapping[str, Any], user_id: int | None,
                    login: str | None, association: str | None) -> tuple[str, str]:
    """Single trust rule for constructor and independently replayed receipt."""
    if login is None:
        return "UNKNOWN", "PROVIDER_AUTHOR_UNAVAILABLE"
    if user_id is None:
        return "UNKNOWN", "PROVIDER_AUTHOR_ID_UNAVAILABLE"
    if policy["mode"] == "ALLOWLIST":
        return (("ACCEPT", "ALLOWLIST_MATCH") if login in policy["fact_authors"]
                else ("REJECT", "NOT_IN_ALLOWLIST"))
    if association is None:
        return "UNKNOWN", "PROVIDER_ASSOCIATION_UNAVAILABLE"
    if association in ASSOCIATIONS:
        return "ACCEPT", "TRUSTED_ASSOCIATION"
    return "REJECT", "UNTRUSTED_ASSOCIATION"


def collect_receipts(
    *, repository: str, issue_number: int, graph_release_digest: str,
    comments: list[Mapping[str, Any]], fact_authors: list[str] | None = None,
) -> dict[str, Any]:
    """Deterministically collect caller-supplied provider comment receipts.

    The trust *decision* is conditional on caller data; it is never provider
    authentication. Missing login/association produces UNKNOWN, never ACCEPT.
    """
    if not isinstance(repository, str) or not _REPO.fullmatch(repository):
        raise ReceiptError("REPOSITORY_INVALID")
    issue_number = _positive_int(issue_number, "ISSUE_NUMBER_INVALID")
    if not isinstance(graph_release_digest, str) or not _SHA.fullmatch(graph_release_digest):
        raise ReceiptError("GRAPH_RELEASE_DIGEST_INVALID")
    if not isinstance(comments, list):
        raise ReceiptError("COMMENTS_UNAVAILABLE")
    if fact_authors is None:
        fact_authors = []
    if (not isinstance(fact_authors, list) or
            any(not isinstance(x, str) or not x for x in fact_authors) or
            len(set(fact_authors)) != len(fact_authors)):
        raise ReceiptError("FACT_AUTHORS_POLICY_INVALID")
    policy = {
        "mode": "ALLOWLIST" if fact_authors else "ASSOCIATIONS",
        "fact_authors": sorted(fact_authors),
        "associations": sorted(ASSOCIATIONS),
        "graph_release_digest": graph_release_digest,
    }
    policy_digest = digest("V32/TRUST_POLICY/V2", policy)
    receipts: list[dict[str, Any]] = []
    # The provider may hand over pages in different orders. Stable GitHub
    # comment IDs, not arbitrary caller list order, define the V2 fold.
    comment_by_id: dict[int, Mapping[str, Any]] = {}
    for comment in comments:
        if not isinstance(comment, Mapping):
            raise ReceiptError("COMMENT_NOT_MAPPING")
        cid = _positive_int(comment.get("id"), "COMMENT_ID_UNAVAILABLE")
        if cid in comment_by_id:
            raise ReceiptError("DUPLICATE_COMMENT_ID")
        comment_by_id[cid] = comment
    for cid, comment in sorted(comment_by_id.items()):
        body = comment.get("body")
        if not isinstance(body, str):
            raise ReceiptError("COMMENT_BODY_UNAVAILABLE")
        body_digest = "sha256:" + hashlib.sha256(body.encode("utf-8", "strict")).hexdigest()
        user = comment.get("user")
        if user is not None and not isinstance(user, Mapping):
            raise ReceiptError("COMMENT_AUTHOR_INVALID")
        user = user or {}
        login = user.get("login")
        user_id = user.get("id")
        association = comment.get("author_association")
        if login is not None and (not isinstance(login, str) or not login):
            raise ReceiptError("COMMENT_LOGIN_INVALID")
        if user_id is not None:
            _positive_int(user_id, "COMMENT_AUTHOR_ID_INVALID")
        if association is not None and (not isinstance(association, str) or not association):
            raise ReceiptError("AUTHOR_ASSOCIATION_INVALID")
        decision, reason = _trust_decision(policy, user_id, login, association)
        for ordinal, (char_offset, facts) in enumerate(extract_blocks(body)):
            core = {
                "schema": RECEIPT_SCHEMA,
                "repository": repository,
                "issue_number": issue_number,
                "graph_release_digest": graph_release_digest,
                "comment": {
                    "id": cid, "user_id": user_id, "login": login,
                    "author_association": association,
                    "body_digest": body_digest,
                },
                "block": {
                    "ordinal": ordinal, "char_offset": char_offset,
                    "facts_digest": digest("V32/FACTS_BLOCK/V2", facts),
                    "facts": facts,
                },
                "trust": {
                    "policy_digest": policy_digest,
                    "decision": decision, "reason": reason,
                },
                "transport_authenticity": "UNVERIFIED_CALLER_SUPPLIED_PROVIDER_DATA",
            }
            receipts.append({**core, "receipt_digest": digest("V32/SOURCE_RECEIPT/V2", core)})
    roots = {
        "schema": SET_SCHEMA,
        "repository": repository,
        "issue_number": issue_number,
        "graph_release_digest": graph_release_digest,
        "policy_digest": policy_digest,
        "policy": policy,
        "authority": "UNVERIFIED_CALLER_SUPPLIED_PROVIDER_DATA",
        "source_completeness": "UNKNOWN_CALLER_SUPPLIED_COMMENT_SET",
        "receipts": receipts,
    }
    return {**roots, "receipt_set_digest": digest("V32/RECEIPT_SET/V2", roots)}


def verify_receipt_set(bundle: Mapping[str, Any]) -> bool:
    """Verify SELF-CONSISTENCY of the frozen V2 bundle, never GitHub truth.

    Recomputable hashes and trust classifications deter accidental/partial
    mutations, but a coherent forged bundle can still pass; provider source
    authentication and revision custody remain mandatory in later WP2/C6.
    """
    if not isinstance(bundle, Mapping) or bundle.get("schema") != SET_SCHEMA:
        raise ReceiptError("RECEIPT_SET_SCHEMA_INVALID")
    if bundle.get("authority") != "UNVERIFIED_CALLER_SUPPLIED_PROVIDER_DATA":
        raise ReceiptError("RECEIPT_SET_AUTHORITY_INVALID")
    if bundle.get("source_completeness") != "UNKNOWN_CALLER_SUPPLIED_COMMENT_SET":
        raise ReceiptError("RECEIPT_SET_COMPLETENESS_INVALID")
    repository, issue, graph = (
        bundle.get("repository"), bundle.get("issue_number"),
        bundle.get("graph_release_digest"),
    )
    if not isinstance(repository, str) or not _REPO.fullmatch(repository):
        raise ReceiptError("RECEIPT_SET_REPOSITORY_INVALID")
    _positive_int(issue, "RECEIPT_SET_ISSUE_INVALID")
    if not isinstance(graph, str) or not _SHA.fullmatch(graph):
        raise ReceiptError("RECEIPT_SET_GRAPH_INVALID")
    policy = bundle.get("policy")
    if not isinstance(policy, Mapping) or set(policy) != {
        "mode", "fact_authors", "associations", "graph_release_digest"
    } or policy["graph_release_digest"] != graph:
        raise ReceiptError("RECEIPT_SET_POLICY_INVALID")
    if (policy["mode"] not in ("ALLOWLIST", "ASSOCIATIONS")
            or not isinstance(policy["fact_authors"], list)
            or policy["fact_authors"] != sorted(set(policy["fact_authors"]))
            or any(not isinstance(x, str) or not x for x in policy["fact_authors"])
            or (policy["mode"] == "ALLOWLIST") != bool(policy["fact_authors"])
            or policy["associations"] != sorted(ASSOCIATIONS)):
        raise ReceiptError("RECEIPT_SET_POLICY_INVALID")
    policy_digest = digest("V32/TRUST_POLICY/V2", policy)
    if bundle.get("policy_digest") != policy_digest:
        raise ReceiptError("RECEIPT_SET_POLICY_DIGEST_MISMATCH")
    rows = bundle.get("receipts")
    if not isinstance(rows, list):
        raise ReceiptError("RECEIPT_SET_ROWS_INVALID")
    ordinal_by_id: dict[int, int] = {}
    authors: dict[int, Any] = {}
    previous_comment_id: int | None = None
    for r in rows:
        if not isinstance(r, Mapping) or set(r) != {
            "schema", "repository", "issue_number", "graph_release_digest",
            "comment", "block", "trust", "transport_authenticity", "receipt_digest"
        }:
            raise ReceiptError("RECEIPT_ROW_SHAPE_INVALID")
        if (r["schema"] != RECEIPT_SCHEMA or r["repository"] != repository
                or r["issue_number"] != issue or r["graph_release_digest"] != graph
                or r["transport_authenticity"] != "UNVERIFIED_CALLER_SUPPLIED_PROVIDER_DATA"):
            raise ReceiptError("RECEIPT_ROW_SOURCE_MISMATCH")
        c, b, t = r["comment"], r["block"], r["trust"]
        if not isinstance(c, Mapping) or set(c) != {
            "id", "user_id", "login", "author_association", "body_digest"
        } or not isinstance(b, Mapping) or set(b) != {
            "ordinal", "char_offset", "facts_digest", "facts"
        } or not isinstance(t, Mapping) or set(t) != {
            "policy_digest", "decision", "reason"
        }:
            raise ReceiptError("RECEIPT_ROW_NESTED_SHAPE_INVALID")
        cid = _positive_int(c["id"], "COMMENT_ID_UNAVAILABLE")
        if previous_comment_id is not None and cid < previous_comment_id:
            raise ReceiptError("RECEIPT_COMMENT_ORDER_INVALID")
        previous_comment_id = cid
        if (not isinstance(c["body_digest"], str) or not _SHA.fullmatch(c["body_digest"])
                or c["login"] is not None and (not isinstance(c["login"], str) or not c["login"])
                or c["user_id"] is not None and (type(c["user_id"]) is not int or c["user_id"] < 1)
                or c["author_association"] is not None and not isinstance(c["author_association"], str)):
            raise ReceiptError("RECEIPT_AUTHOR_IDENTITY_INVALID")
        if cid in authors and authors[cid] != dict(c):
            raise ReceiptError("COMMENT_IDENTITY_CHANGED_WITHIN_SET")
        authors[cid] = dict(c)
        if type(b["ordinal"]) is not int or b["ordinal"] != ordinal_by_id.get(cid, 0):
            raise ReceiptError("FACTS_ORDINAL_SEQUENCE_INVALID")
        ordinal_by_id[cid] = b["ordinal"] + 1
        if type(b["char_offset"]) is not int or b["char_offset"] < 0:
            raise ReceiptError("FACTS_OFFSET_INVALID")
        if b["facts_digest"] != digest("V32/FACTS_BLOCK/V2", b["facts"]):
            raise ReceiptError("FACTS_BLOCK_DIGEST_MISMATCH")
        if t["policy_digest"] != policy_digest:
            raise ReceiptError("RECEIPT_POLICY_MISMATCH")
        decision, reason = _trust_decision(policy, c["user_id"], c["login"], c["author_association"])
        if t["decision"] != decision or t["reason"] != reason:
            raise ReceiptError("RECEIPT_TRUST_REPLAY_MISMATCH")
        material = {k: v for k, v in r.items() if k != "receipt_digest"}
        if r["receipt_digest"] != digest("V32/SOURCE_RECEIPT/V2", material):
            raise ReceiptError("RECEIPT_SELF_DIGEST_MISMATCH")
    material = {k: v for k, v in bundle.items() if k != "receipt_set_digest"}
    if set(bundle) != set(material) | {"receipt_set_digest"}:
        raise ReceiptError("RECEIPT_SET_EXTRA_FIELDS")
    if bundle["receipt_set_digest"] != digest("V32/RECEIPT_SET/V2", material):
        raise ReceiptError("RECEIPT_SET_DIGEST_MISMATCH")
    return True
