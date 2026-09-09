# Reproduce and verify the Motion pilot

Run from the repository root with Python 3.11 or later. Create a project-local environment and install the pinned publication dependencies:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r "Grade 9/skills/grade9-physics-publication/requirements.txt"
```

On Linux/macOS, use `.venv/bin/python` in the commands below.

## 1. Validate skill packaging separately from installation

```bash
.venv/Scripts/python "Grade 9/validate_skills.py"
.venv/Scripts/python "Grade 9/install_skills.py" --dest "build/skill-install-check"
```

Use an empty scratch destination. Installation success proves copying; `validate_skills.py` proves the copied directories satisfy the repository's skill-package contract.

## 2. Regenerate models and executable schema

```bash
.venv/Scripts/python "Grade 9/skills/grade9-physics-publication/scripts/make_motion_models.py"
.venv/Scripts/python "Grade 9/skills/grade9-physics-publication/scripts/validate_v2.py" --schema "Grade 9/skills/grade9-physics-publication/references/physics-publication-v2.schema.json"
```

`make_motion_models.py` is the authored source for all three example JSON files. It writes UTF-8 explicitly so the same command works on Windows.

## 3. Run model, profile, schema, and reconciliation checks

```bash
.venv/Scripts/python "Grade 9/skills/grade9-physics-publication/scripts/test_v2.py"
.venv/Scripts/python "Grade 9/skills/grade9-physics-examside/scripts/check_ledger.py" "Grade 9/skills/grade9-physics-examside/references/source-ledger.example.json"
.venv/Scripts/python "Grade 9/skills/grade9-physics-examside/scripts/test_reconcile.py"
```

The 72-question check is a synthetic structural-capacity test. It is not evidence that the 68-question Motion chapter was authored or reviewed.

## 4. Render and audit all committed learner artifacts

Render each model into `Grade 9/Physics/Motion/B30_B80_Rebuild`:

```python
from pathlib import Path
import subprocess
import sys

root = Path("Grade 9")
skill = root / "skills" / "grade9-physics-publication"
output = root / "Physics" / "Motion" / "B30_B80_Rebuild"
for model, stem in (
    ("motion_B30_v2.json", "Motion_B30_Rebuilt"),
    ("motion_B80_v2.json", "Motion_B80_Rebuilt"),
    ("motion_question_bank_v2.json", "Motion_Optional_Hint_Practice"),
):
    source = skill / "examples" / model
    pdf = output / f"{stem}.pdf"
    subprocess.run([sys.executable, str(skill / "scripts" / "render_v2.py"), str(source), str(pdf)], check=True)
    subprocess.run([sys.executable, str(skill / "scripts" / "audit_v2.py"), str(source), str(pdf)], check=True)
```

Then bind the original-question ledger to the exact final question-bank model and audit:

```bash
.venv/Scripts/python "Grade 9/skills/grade9-physics-examside/scripts/reconcile.py" \
  "Grade 9/skills/grade9-physics-examside/references/source-ledger.example.json" \
  "Grade 9/skills/grade9-physics-publication/examples/motion_question_bank_v2.json" \
  "Grade 9/Physics/Motion/B30_B80_Rebuild/Motion_Optional_Hint_Practice.audit.json"
```

## 5. Visual and package closure

Render every page at 200 DPI and inspect text, equations, labels, diagrams, answer leakage, navigation, and the mixed-test cue boundary. Automated checks do not establish student understanding or source truth.

After the three audits and visual review are current, refresh and verify the content-addressed package:

```bash
.venv/Scripts/python "Grade 9/Physics/Motion/B30_B80_Rebuild/refresh_file_manifest.py"
.venv/Scripts/python "Grade 9/Physics/Motion/B30_B80_Rebuild/verify_review_package.py"
```

For a real ExamSIDE/PYQ corpus, replace the pilot ledger with source-page records carrying exact hashes, pages, raw text/options/figures, URLs, provenance, transcription state, and adaptation notes. This repository includes no qualified external-corpus fixture, so real-source cold-start fidelity remains `NOT_RUN`.
