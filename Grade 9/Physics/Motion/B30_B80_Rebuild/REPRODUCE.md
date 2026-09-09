# Reproduce and check the Motion pilot

Run from the repository root with Python 3.11 or later. The pins record the publication environment. Install in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r "Grade 9/skills/grade9-physics-publication/requirements.txt"
python "Grade 9/skills/grade9-physics-publication/scripts/test_v2.py"
python "Grade 9/skills/grade9-physics-publication/scripts/validate_v2.py" "Grade 9/skills/grade9-physics-publication/examples/motion_B30_v2.json"
```

Scripts resolve bundled examples/fonts relative to the skill. Quote paths containing spaces. Build all outputs separately from the reviewed copies:

```python
from pathlib import Path
import subprocess
import sys

skill = Path('Grade 9/skills/grade9-physics-publication')
output = Path('build/physics-motion')
output.mkdir(parents=True, exist_ok=True)
for model, stem in [
    ('motion_B30_v2.json', 'Motion_B30_Rebuilt'),
    ('motion_B80_v2.json', 'Motion_B80_Rebuilt'),
    ('motion_question_bank_v2.json', 'Motion_Optional_Hint_Practice'),
]:
    source = skill / 'examples' / model
    pdf = output / (stem + '.pdf')
    for script in ['render_v2.py', 'audit_v2.py']:
        subprocess.run([sys.executable, str(skill/'scripts'/script), str(source), str(pdf)], check=True)
```

The renderer writes PDF and `.layout.json`; the auditor needs that sibling layout and writes `.audit.json`. Expected page counts: 21, 16, 10. PDF creation metadata can change regenerated hashes; committed hashes identify the reviewed copies, not a promise of identical bytes across machines.

Export schema with `python "Grade 9/skills/grade9-physics-publication/scripts/validate_v2.py" --schema` and compare its JSON object with the bundled schema. `make_motion_models.py` overwrites three example JSON files. Edit the generator and regenerate, or maintain independent models; avoid conflicting sources of truth.

For real ExamSIDE inputs, run the sibling `grade9-physics-examside/scripts/check_ledger.py` on the completed ledger. Its example is a shape illustration, not verified exam evidence. The original-question demonstration establishes no external-corpus completeness.

After teaching/layout changes, render affected pages at 200 dpi and inspect labels, equations, diagram/prose placement, answer leakage and navigation. Automated checks establish neither student understanding nor accessible PDF tagging nor syllabus approval.
