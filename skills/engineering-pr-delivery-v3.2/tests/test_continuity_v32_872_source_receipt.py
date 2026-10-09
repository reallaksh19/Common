"""Isolated WP1 draft: source receipts only, not DELP core or provider custody."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema
import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from source_receipt_v32 import ReceiptError, collect_receipts, extract_blocks, verify_receipt_set

G = "sha256:" + "a" * 64
F = '''```yaml
CHECKPOINT_FACTS_V1:
  responsibility:
    issue: Common#720
  material:
    candidate_sha: 1111111111111111111111111111111111111111
```'''


def comment(body=F, cid=55, login="maintainer", association="COLLABORATOR"):
    return {"id": cid, "body": body,
            "user": {"id": 101, "login": login}, "author_association": association}


def receipts(comments=None, **kw):
    return collect_receipts(repository="reallaksh19/Common", issue_number=720,
                            graph_release_digest=G,
                            comments=[comment()] if comments is None else comments, **kw)


class SourceReceiptCandidateTests(unittest.TestCase):
    def test_r01_deterministic_replay_and_schema_validation(self):
        a, b = receipts(), receipts()
        self.assertEqual(a, b)
        self.assertEqual(0, a["receipts"][0]["block"]["ordinal"])
        self.assertEqual("ACCEPT", a["receipts"][0]["trust"]["decision"])
        schema = yaml.safe_load((SCRIPTS.parent / "schemas/source-receipt-v2.schema.yaml").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(a["receipts"][0], schema)
        jsonschema.validate(a, schema)

    def test_r02_two_blocks_unique_identity(self):
        a = receipts([comment(F + "\n" + F)])
        self.assertEqual([0, 1], [v["block"]["ordinal"] for v in a["receipts"]])
        self.assertEqual(2, len(set(v["receipt_digest"] for v in a["receipts"])))
        self.assertEqual([55, 55], [v["comment"]["id"] for v in a["receipts"]])

    def test_r03_body_edit_without_fact_edit_moves_receipt(self):
        before = receipts([comment(F)])
        after = receipts([comment(F + "\nExtra unrelated prose")])
        self.assertNotEqual(before["receipts"][0]["receipt_digest"], after["receipts"][0]["receipt_digest"])
        self.assertEqual(before["receipts"][0]["block"]["facts_digest"], after["receipts"][0]["block"]["facts_digest"])

    def test_r04_author_association_and_login_change_receipt(self):
        a = receipts()
        b = receipts([comment(association="NONE")])
        self.assertEqual("ACCEPT", a["receipts"][0]["trust"]["decision"])
        self.assertEqual("REJECT", b["receipts"][0]["trust"]["decision"])
        self.assertNotEqual(a["receipt_set_digest"], b["receipt_set_digest"])
        c = receipts([comment(login="other", association="NONE")])
        self.assertNotEqual(b["receipt_set_digest"], c["receipt_set_digest"])

    def test_r05_allowlist_override_digest_and_decision(self):
        a = receipts()
        b = receipts(fact_authors=["unrelated"])
        c = receipts(fact_authors=["maintainer"])
        self.assertEqual("REJECT", b["receipts"][0]["trust"]["decision"])
        self.assertEqual("ACCEPT", c["receipts"][0]["trust"]["decision"])
        self.assertNotEqual(a["receipt_set_digest"], b["receipt_set_digest"])
        self.assertNotEqual(b["receipt_set_digest"], c["receipt_set_digest"])

    def test_r06_missing_provider_author_never_trusted(self):
        row = comment()
        row["user"] = None
        self.assertEqual("UNKNOWN", receipts([row])["receipts"][0]["trust"]["decision"])
        row = comment()
        row["author_association"] = None
        self.assertEqual("UNKNOWN", receipts([row])["receipts"][0]["trust"]["decision"])
        row = comment()
        del row["body"]
        with self.assertRaisesRegex(ReceiptError, "COMMENT_BODY_UNAVAILABLE"):
            receipts([row])

    def test_r07_duplicate_yaml_keys_fail_closed(self):
        text = F.replace("    issue: Common#720", "    issue: Common#720\n    issue: Common#722")
        with self.assertRaisesRegex(ReceiptError, "DUPLICATE_YAML_KEY"):
            receipts([comment(text)])

    def test_r07_yaml_nonnormalized_and_float_fail(self):
        text = F.replace("  material:", "  note: \"cafe\\u0301\"\n  material:")
        with self.assertRaisesRegex(ReceiptError, "NON_CANONICAL_UNICODE"):
            receipts([comment(text)])
        text = F.replace("  material:", "  note: 1.1\n  material:")
        with self.assertRaisesRegex(ReceiptError, "NON_CANONICAL_JSON_VALUE"):
            receipts([comment(text)])

    def test_r07_invalid_fence_fail_closed(self):
        with self.assertRaisesRegex(ReceiptError, "FACTS_FENCE_UNPARSEABLE"):
            receipts([comment("CHECKPOINT_FACTS_V1:\n  responsibility: 1")])

    def test_r07_duplicate_comment_id_fail_closed(self):
        with self.assertRaisesRegex(ReceiptError, "DUPLICATE_COMMENT_ID"):
            receipts([comment(), comment()])

    def test_r07_missing_comment_id_fails(self):
        r = comment()
        r.pop("id")
        with self.assertRaisesRegex(ReceiptError, "COMMENT_ID_UNAVAILABLE"):
            receipts([r])

    def test_r08_legacy_fence_parity_on_valid_yaml(self):
        block = extract_blocks(F)[0][1]
        self.assertEqual("relay-v3.2-delp-checkpoint-facts", block["schema"])
        self.assertEqual("Common#720", block["responsibility"]["issue"])
        self.assertEqual(1, len(extract_blocks(F)))

    def test_unknown_transport_provenance_no_self_authentication(self):
        a = receipts()
        self.assertEqual("UNVERIFIED_CALLER_SUPPLIED_PROVIDER_DATA", a["authority"])
        self.assertEqual("UNVERIFIED_CALLER_SUPPLIED_PROVIDER_DATA", a["receipts"][0]["transport_authenticity"])

    def test_no_facts_does_not_emit_false_evidence(self):
        a = receipts([comment("Unrelated discussion")])
        self.assertEqual([], a["receipts"])
        self.assertEqual("UNKNOWN_CALLER_SUPPLIED_COMMENT_SET", a["source_completeness"])
        self.assertTrue(verify_receipt_set(a))

    def test_policy_duplicate_author_id_rejected(self):
        with self.assertRaisesRegex(ReceiptError, "FACT_AUTHORS_POLICY_INVALID"):
            receipts(fact_authors=["maintainer", "maintainer"])

    def test_digest_is_version_domain_separated(self):
        from source_receipt_v32 import digest
        a = digest("V32/RECEIPT_SET/V2", {"k": "v"})
        b = digest("V32/SOURCE_RECEIPT/V2", {"k": "v"})
        self.assertNotEqual(a, b)
        self.assertTrue(a.startswith("sha256:"))

    def test_r09_receipt_set_replay_verifies_inner_and_outer_hashes(self):
        self.assertTrue(verify_receipt_set(receipts()))
        self.assertTrue(verify_receipt_set(receipts([comment(F + "\n" + F)])))

    def test_r09_tampered_facts_fail_even_if_outer_hash_unchanged(self):
        a = receipts()
        a["receipts"][0]["block"]["facts"]["responsibility"]["issue"] = "Common#777"
        with self.assertRaisesRegex(ReceiptError, "FACTS_BLOCK_DIGEST_MISMATCH"):
            verify_receipt_set(a)

    def test_r09_tampered_policy_decision_fails_even_rebound_receipt_hash(self):
        from source_receipt_v32 import digest
        a = receipts()
        r = a["receipts"][0]
        r["trust"]["decision"] = "REJECT"
        material = {k: v for k, v in r.items() if k != "receipt_digest"}
        r["receipt_digest"] = digest("V32/SOURCE_RECEIPT/V2", material)
        material = {k: v for k, v in a.items() if k != "receipt_set_digest"}
        a["receipt_set_digest"] = digest("V32/RECEIPT_SET/V2", material)
        with self.assertRaisesRegex(ReceiptError, "RECEIPT_TRUST_REPLAY_MISMATCH"):
            verify_receipt_set(a)

    def test_r09_changed_block_ordinal_fails(self):
        a = receipts([comment(F + "\n" + F)])
        a["receipts"][1]["block"]["ordinal"] = 0
        with self.assertRaisesRegex(ReceiptError, "FACTS_ORDINAL_SEQUENCE_INVALID"):
            verify_receipt_set(a)

    def test_r10_malformed_second_fact_fence_cannot_disappear(self):
        malformed = "```yaml invalid-language\nCHECKPOINT_FACTS_V1:\n  responsibility:\n    issue: Common#999\n```"
        with self.assertRaisesRegex(ReceiptError, "FACTS_FENCE_UNPARSEABLE"):
            receipts([comment(F + "\n" + malformed)])

    def test_r10_unfenced_fact_marker_after_valid_fence_cannot_disappear(self):
        with self.assertRaisesRegex(ReceiptError, "FACTS_FENCE_UNPARSEABLE"):
            receipts([comment(F + "\nCHECKPOINT_FACTS_V1:\n  material:\n    candidate_sha: fake")])

    def test_r11_missing_numeric_user_id_cannot_accept(self):
        row = comment()
        row["user"].pop("id")
        a = receipts([row])
        self.assertEqual("UNKNOWN", a["receipts"][0]["trust"]["decision"])
        self.assertEqual("PROVIDER_AUTHOR_ID_UNAVAILABLE", a["receipts"][0]["trust"]["reason"])
        self.assertTrue(verify_receipt_set(a))

    def test_r12_comment_input_order_is_canonical(self):
        a = receipts([comment(cid=57), comment(cid=55)])
        b = receipts([comment(cid=55), comment(cid=57)])
        self.assertEqual(a["receipt_set_digest"], b["receipt_set_digest"])
        self.assertEqual([55, 57], [r["comment"]["id"] for r in a["receipts"]])

    def test_r12_reordered_rows_rejected_even_if_outer_rehashed(self):
        from source_receipt_v32 import digest
        a = receipts([comment(cid=55), comment(cid=57)])
        a["receipts"].reverse()
        a["receipt_set_digest"] = digest(
            "V32/RECEIPT_SET/V2", {k: v for k, v in a.items() if k != "receipt_set_digest"}
        )
        with self.assertRaisesRegex(ReceiptError, "RECEIPT_COMMENT_ORDER_INVALID"):
            verify_receipt_set(a)

    def test_r13_strict_delimiter_rejects_fence_with_trailing_text(self):
        with self.assertRaisesRegex(ReceiptError, "FACTS_FENCE_UNPARSEABLE"):
            receipts([comment(F[:-3] + "```malicious")])

    def test_r13_strict_delimiter_rejects_inline_fence_opener(self):
        with self.assertRaisesRegex(ReceiptError, "FACTS_FENCE_UNPARSEABLE"):
            receipts([comment("inline opener " + F)])


if __name__ == "__main__":
    unittest.main()
