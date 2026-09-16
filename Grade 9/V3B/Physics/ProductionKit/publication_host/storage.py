"""Create immutable publication directories and portable command dependencies."""

import json
import shutil
import tempfile
from pathlib import Path

from v3b.contracts import digest, file_digest, require


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding="utf-8")


def runtime_files():
    kit = Path(__file__).resolve().parents[1]
    root = kit.parents[1]
    files = list((root / "Shared").rglob('*.py'))
    files += list((root / "Shared").rglob('*.json')) + list((root / "Shared").rglob('*.md'))
    files += list((kit / "publication_host").glob('*.py')) + [kit / 'run.py', kit / 'validator.py']
    files += list(kit.glob('V3B-*.md'))
    files += [root / 'Physics/CoreContracts.json']
    files += list((root / 'Physics/Blueprint').glob('V3B-*'))
    return {str(p.relative_to(root)): p for p in sorted(files) if p.is_file()}


def runtime_manifest():
    return [{"path": 'runtime/' + name, "sha256": file_digest(path)}
            for name, path in runtime_files().items()]


def build_directory(out, action):
    require(not out.exists(), "PUBLICATION_ALREADY_EXISTS", str(out))
    out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.v3b-build-', dir=out.parent))
    try:
        result = action(staging)
        require(not out.exists(), "PUBLICATION_ALREADY_EXISTS", str(out))
        staging.rename(out)
        return result
    finally:
        if staging.exists():
            shutil.rmtree(staging)
