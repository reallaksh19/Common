import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "scaffold_rll_adapter.py"
SPEC = importlib.util.spec_from_file_location("scaffold_rll_adapter", MODULE_PATH)
scaffold = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scaffold)


class ScaffoldRllAdapterTests(unittest.TestCase):
    def test_sidecar_id_is_stable(self):
        self.assertEqual(
            "reallaksh19-some-other-repo-rll1",
            scaffold.sidecar_id("reallaksh19/Some_Other Repo"),
        )

    def test_render_replaces_all_tokens(self):
        source = "{{REPOSITORY}} / {{AUTHORIZED_LOGIN}} / {{WORKER_ID}} / {{SIDECAR_ID}}"
        rendered = scaffold.render(
            source,
            {
                "REPOSITORY": "owner/repo",
                "AUTHORIZED_LOGIN": "owner",
                "WORKER_ID": "antigravity-local",
                "SIDECAR_ID": "owner-repo-rll1",
            },
        )
        self.assertEqual(
            "owner/repo / owner / antigravity-local / owner-repo-rll1",
            rendered,
        )

    def test_render_rejects_missing_tokens(self):
        with self.assertRaises(ValueError):
            scaffold.render("{{REPOSITORY}} {{MISSING}}", {"REPOSITORY": "owner/repo"})

    def test_scaffold_writes_four_thin_adapter_files_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            written = scaffold.scaffold(
                root,
                repository="owner/repo",
                required_common_basis="abc123",
                authorized_login="owner",
                worker_id="antigravity-local",
                force=False,
            )
            self.assertEqual(
                sorted(scaffold.TEMPLATES),
                sorted(written),
            )
            for path in scaffold.TEMPLATES:
                self.assertTrue((root / path).is_file(), path)
            wrapper = (root / "scripts/rll1-antigravity-worker.ps1").read_text(
                encoding="utf-8"
            )
            self.assertIn("owner/repo", wrapper)
            self.assertIn("abc123", wrapper)
            self.assertNotIn("{{", wrapper)

            self.assertEqual(
                [],
                scaffold.scaffold(
                    root,
                    repository="owner/repo",
                    required_common_basis="abc123",
                    authorized_login="owner",
                    worker_id="antigravity-local",
                    force=False,
                ),
            )

    def test_scaffold_refuses_divergent_existing_file_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / ".agents/rules/rll-1.md"
            target.parent.mkdir(parents=True)
            target.write_text("custom local rule\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                scaffold.scaffold(
                    root,
                    repository="owner/repo",
                    required_common_basis="abc123",
                    authorized_login="owner",
                    worker_id="antigravity-local",
                    force=False,
                )


if __name__ == "__main__":
    unittest.main()
