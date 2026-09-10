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

For a production subtopic, validate its two files together after both models exist:

```bash
.venv/Scripts/python "Grade 9/skills/grade9-physics-publication/scripts/validate_v2.py" --pair \
  "path/to/topic_core_study_guide.json" \
  "path/to/topic_examside_solution.json"
```

This gate requires one topic, reciprocal model/pair IDs, identical project and canonical concept authority, matching concept segregation, a Core Study Guide with Appendices A–C, and an externally grounded ExamSIDE Solution Book with difficulty badges. The bundled Motion models are legacy two-topic pilot profiles, so they intentionally do not claim this pair gate.

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

## 5. Capture machine evidence for the exact current files

After model generation, rendering, audits, and ledger reconciliation are complete, run the evidence driver. It repeats the focused checks and records each real command, exit code, stdout/stderr hash, dependency hash, and artifact hash:

```bash
.venv/Scripts/python "Grade 9/Physics/Motion/B30_B80_Rebuild/run_review_checks.py"
```

Do not edit dependency or artifact files after this step without rerunning the evidence driver. `verify_review_package.py` rejects stale evidence even when its recorded status says `PASS`.

## 6. Visual and package closure

Render every page at 200 DPI and inspect text, equations, labels, diagrams, answer leakage, navigation, and the mixed-test cue boundary. Automated checks do not establish student understanding or source truth.

Record that review against the exact PDF hashes. Replace the reviewer and notes with the actual reviewer and observations; the page count must equal the current audited total:

```bash
.venv/Scripts/python "Grade 9/Physics/Motion/B30_B80_Rebuild/record_visual_review.py" \
  --reviewer "Reviewer name" \
  --result PASS \
  --dpi 200 \
  --pages-reviewed 65 \
  --notes "All rendered pages inspected; no clipping, collisions, cue leakage, or illegible labels found."
```

After machine and visual evidence are current, derive the review summaries, refresh the content-addressed manifest, and verify the whole chain in this exact order:

```bash
.venv/Scripts/python "Grade 9/Physics/Motion/B30_B80_Rebuild/refresh_review_summaries.py"
.venv/Scripts/python "Grade 9/Physics/Motion/B30_B80_Rebuild/refresh_file_manifest.py"
.venv/Scripts/python "Grade 9/Physics/Motion/B30_B80_Rebuild/verify_review_package.py"
```

The manifest covers the live `Grade 9/skills` tree, shared contracts, router/install validators, and the complete Motion review package. It excludes only itself and the historical delivery record. The summaries never carry a prior visual PASS forward: a PDF hash or page-count change resets the projected result until a new visual attestation is recorded.

For a real ExamSIDE/PYQ corpus, replace the pilot ledger with source-page records carrying exact hashes, pages, raw text/options/figures, URLs, provenance, transcription state, and adaptation notes. This repository includes no qualified external-corpus fixture, so real-source cold-start fidelity remains `NOT_RUN`.

When such a source supplies its own difficulty code (for example `D1`–`D4`), retain that raw code separately from any normalized internal band and learner-facing badge. This original-question pilot has no source-owned difficulty data, so no mapping is inferred here.
