from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from nomenclature import (
    allocate_next_id,
    allocate_next_ids,
    canonical_id,
    next_serial,
    parse_canonical_id,
    parse_legacy_id,
    require_issue_rooted_id,
    require_rooted_id,
)


class NomenclatureTests(unittest.TestCase):
    def test_issue_rooted_repeatable_identifier(self):
        self.assertEqual("EP.1885.1", canonical_id("EP", 1885, 1))
        self.assertEqual(
            {
                "kind": "EP",
                "root": "1885",
                "scope_kind": "ISSUE",
                "issue_number": 1885,
                "serial": 1,
            },
            parse_canonical_id("EP.1885.1"),
        )

    def test_repository_and_internal_roots_are_explicit(self):
        self.assertEqual("CTRL.REPO.1", canonical_id("CTRL", "REPO", 1))
        self.assertEqual("TX.INTERNAL.2", canonical_id("TX", "INTERNAL", 2))
        self.assertEqual(
            "REPOSITORY",
            parse_canonical_id("CTRL.REPO.1")["scope_kind"],
        )
        self.assertEqual(
            "INTERNAL",
            parse_canonical_id("TX.INTERNAL.2")["scope_kind"],
        )

    def test_programme_and_work_package_singleton_rules(self):
        self.assertEqual("PGM.1760", canonical_id("PGM", 1760))
        self.assertEqual("WP.1775", canonical_id("WP", 1775))
        self.assertEqual("WP.1775.2", canonical_id("WP", 1775, 2))
        self.assertIsNone(parse_canonical_id("PGM.1760.1"))
        self.assertIsNone(parse_canonical_id("PGM.REPO"))
        self.assertIsNone(parse_canonical_id("WP.REPO.1"))

    def test_all_repeatable_namespaces_use_same_grammar(self):
        for kind in (
            "EP", "LEASE", "CP", "AC", "KI", "PEND", "CTRL", "CHANGE",
            "OFFLOAD", "LOCAL", "EVID", "HO", "REC", "ODR", "TX", "EVT",
        ):
            with self.subTest(kind=kind):
                value = canonical_id(kind, 438, 1)
                parsed = parse_canonical_id(value)
                self.assertEqual(kind, parsed["kind"])
                self.assertEqual(438, parsed["issue_number"])
                self.assertEqual(1, parsed["serial"])

    def test_provisional_is_not_a_durable_namespace(self):
        with self.assertRaisesRegex(ValueError, "unsupported Relay identifier type"):
            canonical_id("PROV", 438, 1)
        self.assertIsNone(parse_canonical_id("PROV.438.1"))

    def test_legacy_ids_remain_recognizable_without_invented_lineage(self):
        self.assertEqual(
            {"kind": "EP", "value": "EP-TA-011"},
            parse_legacy_id("EP-TA-011"),
        )
        self.assertIsNone(parse_canonical_id("EP-TA-011"))
        self.assertIsNone(parse_legacy_id("EP.1885.1"))

    def test_generic_root_validation_preserves_repository_scope(self):
        self.assertEqual(
            "TX.REPO.3",
            require_rooted_id(
                "TX.REPO.3",
                kind="TX",
                root="REPO",
                label="transaction id",
            ),
        )
        with self.assertRaisesRegex(ValueError, "does not match governing scope REPO"):
            require_rooted_id(
                "TX.1885.1",
                kind="TX",
                root="REPO",
                label="transaction id",
            )

    def test_issue_root_validation_does_not_accept_wrong_issue(self):
        self.assertEqual(
            "LEASE.1885.3",
            require_issue_rooted_id(
                "LEASE.1885.3",
                kind="LEASE",
                issue_number=1885,
                label="lease id",
            ),
        )
        with self.assertRaisesRegex(ValueError, "does not match governing scope 1885"):
            require_issue_rooted_id(
                "LEASE.1902.1",
                kind="LEASE",
                issue_number=1885,
                label="lease id",
            )

    def test_repository_allocator_treats_durable_history_as_consumed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            events = root / "relay/EVENTS.jsonl"
            events.parent.mkdir(parents=True, exist_ok=True)
            events.write_text(
                '{"subject":"LEASE.438.1","basis":["LEASE.438.4"]}\n',
                encoding="utf-8",
            )
            generated = root / "relay/GENERATED/SHOULD_NOT_COUNT.yaml"
            generated.parent.mkdir(parents=True, exist_ok=True)
            generated.write_text("id: LEASE.438.99\n", encoding="utf-8")

            self.assertEqual(
                "LEASE.438.5",
                allocate_next_id(root, kind="LEASE", root=438),
            )

    def test_batch_allocation_is_monotonic_within_one_namespace_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            events = root / "relay/EVENTS.jsonl"
            events.parent.mkdir(parents=True, exist_ok=True)
            events.write_text('{"subject":"EVT.438.2"}\n', encoding="utf-8")
            self.assertEqual(
                ["EVT.438.3", "EVT.438.4", "EVT.438.5"],
                allocate_next_ids(root, kind="EVT", root=438, count=3),
            )

    def test_serial_allocation_is_namespace_and_root_scoped_and_never_fills_gaps(self):
        existing = [
            "EP.1885.1",
            "EP.1885.4",
            "CP.1885.9",
            "EP.1902.7",
            "EP-LEGACY-99",
        ]
        self.assertEqual(5, next_serial(existing, kind="EP", issue_number=1885))
        self.assertEqual(10, next_serial(existing, kind="CP", issue_number=1885))
        self.assertEqual(8, next_serial(existing, kind="EP", issue_number=1902))
        self.assertEqual(1, next_serial(existing, kind="LEASE", issue_number=1885))


if __name__ == "__main__":
    unittest.main()
