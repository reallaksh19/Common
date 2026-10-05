import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "continuity_projection.py"
spec = importlib.util.spec_from_file_location("continuity_projection_pagination", MODULE_PATH)
cp = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(cp)


class ProviderCommentPaginationTests(unittest.TestCase):
    def test_gh_comments_reads_later_pages_for_managed_and_recovery_surfaces(self):
        calls = []
        first_page = [
            {"id": index, "body": f"noise-{index}"}
            for index in range(1, 101)
        ]
        second_page = [
            {"id": 101, "body": f"{cp.START}\nmanaged\n{cp.END}"},
            {
                "id": 102,
                "body": (
                    "<!-- relay-v3.2:recovery-evidence loss=1 material=head-b -->\n"
                    "TASK_EVIDENCE — RECOVERY"
                ),
            },
        ]

        old_json = cp.gh_json

        def fake_json(*args):
            self.assertEqual(args[0:2], ("--method", "GET"))
            self.assertIn("per_page=100", args)
            page_arg = next(value for value in args if value.startswith("page="))
            page = int(page_arg.split("=", 1)[1])
            calls.append(page)
            if page == 1:
                return list(first_page)
            if page == 2:
                return list(second_page)
            raise AssertionError(f"unexpected page {page}")

        cp.gh_json = fake_json
        try:
            rows = cp.gh_comments("owner/repo", 10)
        finally:
            cp.gh_json = old_json

        self.assertEqual(calls, [1, 2])
        self.assertEqual(len(rows), 102)
        self.assertTrue(any(cp.START in row["body"] for row in rows))
        self.assertTrue(
            any("TASK_EVIDENCE — RECOVERY" in row["body"] for row in rows)
        )

    def test_gh_comments_rejects_non_list_page(self):
        old_json = cp.gh_json
        cp.gh_json = lambda *args: {"message": "unexpected"}
        try:
            with self.assertRaisesRegex(
                cp.ContinuityError,
                "GitHub comments response must be a list",
            ):
                cp.gh_comments("owner/repo", 10)
        finally:
            cp.gh_json = old_json


if __name__ == "__main__":
    unittest.main()
