#!/usr/bin/env python3
"""COLD-08: successor must independently verify the *current released* graph."""
from __future__ import annotations
import base64
import importlib.util
import json
import os
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "skills/engineering-pr-delivery-v3.2/scripts"))
spec = importlib.util.spec_from_file_location("c6_cold_live", HERE / "811_c6_c4_cold_successor.py")
assert spec and spec.loader
cold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cold)

class ColdReleasedGraphCurrentness(unittest.TestCase):
    def test_cold_08_unmerged_or_superseded_graph_never_reports_current(self):
        rev = "b4e61d8f61e9738833564795971692241c2e3df9"
        location = {"repository": "reallaksh19/Common",
                    "path": ".github/v32-evidence-spine/718-proposal-v2.json",
                    "revision": rev}
        old_graph = {"programme": {"repository": location["repository"]},
                     "nodes": [{"ref": "Common#718"}, {"ref": "Common#793"}]}
        new_graph = {"programme": {"repository": location["repository"]},
                     "nodes": [{"ref": "Common#718"}, {"ref": "Common#793"},
                               {"ref": "Common#900"}]}
        pinned = json.dumps(old_graph).encode("utf-8")
        released = json.dumps(new_graph).encode("utf-8")
        def content(blob):
            return {"type": "file", "encoding": "base64",
                    "content": base64.b64encode(blob).decode("ascii")}
        def gh(args, **kwargs):
            end = args[-1]
            if end == "repos/reallaksh19/Common":
                obj = {"full_name": location["repository"], "default_branch": "main"}
            elif end.endswith("?ref=" + rev):
                obj = content(pinned)
            elif end.endswith("?ref=main"):
                obj = content(released)
            else:
                raise AssertionError("unexpected source: " + end)
            return SimpleNamespace(stdout=json.dumps(obj))
        with patch.dict(os.environ, {"GH_TOKEN": "TEST_TOKEN",
                                      "GITHUB_REPOSITORY": location["repository"]}, clear=True):
            with patch("subprocess.run", side_effect=gh):
                with self.assertRaisesRegex(RuntimeError, "COLD_RELEASED_GRAPH_CHANGED_RECONCILE_REQUIRED"):
                    cold.authenticated_read_only_graph(location)

if __name__ == "__main__":
    unittest.main()
