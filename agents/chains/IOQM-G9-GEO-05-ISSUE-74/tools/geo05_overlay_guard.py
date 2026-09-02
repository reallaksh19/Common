#!/usr/bin/env python3
"""Guard a GEO-05 intake manifest against cross-topic publication contamination."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path, PurePosixPath

TARGET_PREFIX = PurePosixPath("Grade 9/Mathematics/IOQM/03_Main_Topics/GEO-05_Coordinate_Vector_Mensuration_Representations")
EXPECTED_COUNT = 24

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("manifest", type=Path); ap.add_argument("--plan-out", type=Path, required=True); args = ap.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8")); files = data.get("files") or []; errors = []
    if data.get("schema") != "geo05-exact-byte-intake-v1": errors.append("unexpected manifest schema")
    if data.get("file_count") != EXPECTED_COUNT or len(files) != EXPECTED_COUNT: errors.append(f"expected {EXPECTED_COUNT} files")
    if data.get("admission_pass") is not True: errors.append("intake admission did not pass")
    seen = set(); entries = []
    for item in files:
        rp = PurePosixPath(item.get("repository_path", "")); rel = item.get("relative_path", "")
        if rp in seen: errors.append(f"duplicate repository path: {rp}")
        seen.add(rp)
        try: rp.relative_to(TARGET_PREFIX)
        except ValueError: errors.append(f"path escapes GEO-05 subtree: {rp}")
        if ".." in PurePosixPath(rel).parts: errors.append(f"relative path traversal: {rel}")
        for key in ("sha256", "git_blob"):
            if not item.get(key): errors.append(f"missing {key} for {rel}")
        entries.append({"path":str(rp),"relative_path":rel,"bytes":item.get("bytes"),"sha256":item.get("sha256"),"expected_git_blob":item.get("git_blob")})
    plan = {"schema":"geo05-overlay-plan-v1","target_prefix":str(TARGET_PREFIX),"base_policy":"FRESH_LIVE_PRODUCTION_TREE_REQUIRED","overlay_policy":"REPLACE_ONLY_GEO05_TARGET_SUBTREE_ENTRIES","expected_changed_file_count":EXPECTED_COUNT,"entries":sorted(entries,key=lambda x:x["path"]),"guard_pass":not errors,"errors":errors}
    args.plan_out.write_text(json.dumps(plan, indent=2, sort_keys=True)+"\n", encoding="utf-8"); print(args.plan_out)
    if errors:
        for e in errors: print(f"FAIL {e}", file=sys.stderr)
        return 1
    print("PASS overlay scope is GEO-05-only; fresh production base still required at write time"); return 0

if __name__ == "__main__": raise SystemExit(main())
