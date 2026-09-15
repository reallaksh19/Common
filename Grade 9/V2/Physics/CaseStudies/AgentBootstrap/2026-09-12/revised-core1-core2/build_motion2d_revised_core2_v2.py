from pathlib import Path
import fitz, math, json, hashlib, re
from PIL import Image

# Reuse validated source inventory / mappings / drawings from the technical case-study base.
# In the local handoff workspace this is `_core2_base_prefix.py`, extracted from the prior
# build script before its old build invocation. The complete executable copy is retained
# with the generated artifact in the ChatGPT workbench.
BASE = Path('/mnt/data/_core2_base_prefix.py')
exec(BASE.read_text(), globals())

# Core v2 contract summary:
# - all 59 source questions retained
# - attempt = question -> representation -> 3 prompt/reveal hint pairs -> exactly 2 work lines
# - each hint prompt is open-ended and self-contained
# - each reveal answers only its own prompt, with description/representation/equation as appropriate
# - solution = recap -> representation/knowns -> UNDERSTAND -> REPRESENT -> CONNECT -> CALCULATE -> INTERPRET -> answer/checks
# - CALCULATE is content-height and step-complete; no fixed-height truncation
# - C14 angular-momentum and C16/C17 inclined-plane figures use corrected semantic drawings
# - Q49/Q51 remain source-ambiguous
#
# NOTE: the full executable generated artifact is the authority for this case-study revision;
# this repository copy intentionally documents the mechanism rather than embedding the chat-only source scan.

HINT_CONTRACT = {
    'H1': 'minimum context anchor + open-ended question about decisive physics; reveal physical state only',
    'H2': 'minimum context anchor + open-ended representation question; reveal matching diagram/components/frame/equation',
    'H3': 'minimum context anchor + open-ended first-move question; reveal only the first executable constraint',
}

SOLUTION_LADDER = ['UNDERSTAND','REPRESENT','CONNECT','CALCULATE','INTERPRET']

# Publication falsifiers introduced by this revision.
FALSIFIERS = [
    'HINT_PROMPT_NOT_OPEN_ENDED',
    'HINT_REVEAL_NOT_SELF_CONTAINED',
    'HINT_PROMPT_REVEAL_MISMATCH',
    'HINT_REVEAL_LEAKS_LATER_RUNG',
    'HINT_REVEAL_RESOLVES_FINAL_ANSWER',
    'REPRESENTATION_STATE_DIVERGES_FROM_QUESTION',
    'SOLUTION_STEP_SKIPPED',
    'CALCULATE_ROW_TRUNCATED',
    'ATTEMPT_WORKSPACE_NOT_TWO_LINES',
]

if __name__ == '__main__':
    raise SystemExit('Use the complete workbench generator bundled with the generated PDF artifact; this repo file records the v2 contract and falsifiers.')
