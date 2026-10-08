"""R7-U5: cold-entry parent guard and lossless manual historical archive."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import integration_parent_frontpage_v35 as PAGE


def governing(issue: int) -> str:
    return {
        600: "\n\n# RESPONSIBILITY KERNEL IMPLEMENTATION PROGRAMME\n\n"
             "<!-- V35_PARENT_OWNER_INTENT_BEGIN -->\n"
             "## MY INTENT — original owner prompts, byte-for-byte preserved\n"
             "Original primary link: UNKNOWN; first durable copy #717\n"
             "<!-- V35_PARENT_OWNER_INTENT_END -->\n\nThe plan remains open.\n",
        717: "\n\n# V3.5 — Unified Responsibility Integration\n\n"
             "<!-- V35_INTEGRATION_CURRENT_BEGIN -->\n"
             "IC0/8, no fake Owner approval.\n"
             "<!-- V35_INTEGRATION_CURRENT_END -->\n\nOriginal IC contract text.\n",
        759: "\n\n# R7 — actual OWNER graph release\n\n"
             "Original roadmap, dependencies, and task evidence.\n",
    }[issue]


def front(body: str) -> str:
    return PAGE.START + "\n" + body + "\n" + PAGE.END


def legacy(issue: int, n: int = 2) -> str:
    tags = sorted(PAGE.HISTORICAL[issue])[:n]
    return "".join(
        f"<!-- {tag}_BEGIN -->\n"
        f"historical stale status: QUEUED at earlier head\n"
        f"<!-- {tag}_END -->\n\n"
        for tag in tags
    ) + governing(issue)


class ParentFrontPageTests(unittest.TestCase):
    def test_current_page_for_each_real_issue_and_protected_source(self):
        for issue in (600, 717, 759):
            original = governing(issue)
            body = front("MANUAL PROVIDER CURRENT, IC0/8") + original
            with self.subTest(issue=issue):
                read = PAGE.validate_current(body, issue)
                self.assertEqual("MANUAL_NAVIGATION_ONLY_NOT_DELP_OR_OWNER",
                                 read["status_authority"])
                self.assertLess(read["governing_source_position"], 4096)
                self.assertFalse(read["writes"])

    def test_legacy_prefix_archives_only_known_statuses_verbatim(self):
        for issue in (600, 717, 759):
            body = legacy(issue)
            with self.subTest(issue=issue):
                result = PAGE.archive_legacy_prefix(body, issue)
                self.assertEqual(2, result["archived_count"])
                self.assertEqual(body, result["archive_text"] + result["remaining_body"])
                self.assertTrue(result["requires_verified_native_archive"])
                self.assertEqual(governing(issue), result["remaining_body"])

    def test_proposed_replacement_never_changes_unowned_bytes_and_is_stable(self):
        for issue in (600, 717, 759):
            body = front("MANUAL 1") + governing(issue)
            with self.subTest(issue=issue):
                candidate = PAGE.propose(body, issue, "MANUAL 2")
                self.assertEqual("", candidate["archive_text"])
                self.assertEqual(
                    governing(issue),
                    candidate["proposed_body"][candidate["proposed_body"].index(PAGE.END)
                                               + len(PAGE.END):])
                second = PAGE.propose(candidate["proposed_body"], issue, "MANUAL 2")
                self.assertEqual(candidate["proposed_body"], second["proposed_body"])
                self.assertFalse(second["archive_required"])
                self.assertFalse(candidate["writes"])

    def test_legacy_plan_requires_prior_verified_archive(self):
        for issue in (600, 717, 759):
            body = legacy(issue)
            with self.subTest(issue=issue):
                candidate = PAGE.propose(body, issue, "MANUAL CURRENT")
                self.assertEqual(2, candidate["archived_count"])
                self.assertTrue(candidate["archive_required"])
                self.assertEqual(
                    PAGE.archive_legacy_prefix(body, issue)["archive_text"],
                    candidate["archive_text"],
                )
                self.assertIn(governing(issue), candidate["proposed_body"])
                self.assertEqual("PROPOSAL_ONLY_NO_GITHUB_WRITE",
                                 candidate["status_authority"])

    def test_unknown_or_protected_marker_is_not_old_banner(self):
        for issue in (600, 717, 759):
            body = "<!-- V35_GRAPH_SELECTION_APPROVAL_V1_BEGIN -->\n"
            with self.subTest(issue=issue), self.assertRaisesRegex(
                PAGE.FrontPageError, "unknown/protected"):
                PAGE.archive_legacy_prefix(body + governing(issue), issue)

    def test_malformed_or_nested_legacy_marker_rejected(self):
        tag = sorted(PAGE.HISTORICAL[600])[0]
        bodies = (
            f"<!-- {tag}_BEGIN -->\nMissing END\n" + governing(600),
            f"<!-- {tag}_BEGIN -->\n<!-- V35_NESTED_BEGIN -->"
            f"<!-- V35_NESTED_END -->\n<!-- {tag}_END -->\n" + governing(600),
            f"<!-- {tag}_BEGIN -->\n<!-- {tag}_END -->\n"
            f"<!-- {tag}_BEGIN -->\n<!-- {tag}_END -->\n" + governing(600),
        )
        for i, body in enumerate(bodies):
            with self.subTest(case=i), self.assertRaises(PAGE.FrontPageError):
                PAGE.archive_legacy_prefix(body, 600)

    def test_missing_double_or_buried_owner_intent_rejected(self):
        correct = front("CURRENT") + governing(600)
        for body in (
            correct.replace("<!-- V35_PARENT_OWNER_INTENT_BEGIN -->", ""),
            correct + "\n<!-- V35_PARENT_OWNER_INTENT_BEGIN -->",
            front("P" * 4500) + governing(600),
            front("current") + "\n" * 4500 + governing(600),
            front("current") + "\n<!-- V35_U4D_LATEST_600_BEGIN -->\n"
            + governing(600),
            PAGE.START + "\nUnclosed " + governing(600),
        ):
            with self.subTest(body=body[:55]), self.assertRaises(PAGE.FrontPageError):
                PAGE.validate_current(body, 600)

    def test_authority_injection_and_foreign_programmes_denied(self):
        body = front("MANUAL") + governing(600)
        for content in ("", "   ", "<!-- V35_GRAPH_SELECTION_APPROVAL_V1_BEGIN -->",
                        "text --> OWNER", "<!-- malformed authority"):
            with self.subTest(content=content), self.assertRaises(PAGE.FrontPageError):
                PAGE.propose(body, 600, content)
        with self.assertRaises(PAGE.FrontPageError):
            PAGE.validate_current(body, 527)

    def test_cli_is_read_only_no_write_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "issue.md"
            target.write_text(front("MANUAL") + governing(600), encoding="utf-8")
            self.assertEqual(0, PAGE.main(["--issue", "600", "--body-file", str(target)]))
            old = target.read_bytes()
            self.assertEqual(old, target.read_bytes())
            target.write_text(legacy(600), encoding="utf-8")
            self.assertEqual(3, PAGE.main(["--issue", "600", "--body-file", str(target)]))


if __name__ == "__main__":
    unittest.main()
