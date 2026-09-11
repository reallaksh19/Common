import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "examples" / "grade4-english-phase5.example.json"


def fail(message):
    raise SystemExit(f"Grade 4 English Phase-5 fixture invalid: {message}")


data = json.loads(FIXTURE.read_text(encoding="utf-8"))

objects = {item["learningObjectId"]: item for item in data.get("learningObjects", [])}
if "ENG-INFERENCE-TEXT-EVIDENCE" not in objects:
    fail("missing canonical inference/text-evidence learning object")
if "ENG-ADJECTIVE-ORDER-RECOGNITION" not in objects:
    fail("missing adjective-order recognition learning object")

inference = data.get("inferenceFixture", {})
if inference.get("defensibleResponse", {}).keys() < {"answer", "textClues", "connection"}:
    fail("inference must preserve ANSWER + TEXT_CLUE + CONNECTION")
if set(inference.get("responseModes", [])) != {"ORAL", "WRITTEN"}:
    fail("inference fixture must distinguish ORAL and WRITTEN response modes")
if inference.get("responseEvidence", {}).get("answerOnly", {}).get("status") != "INSUFFICIENT_EVIDENCE":
    fail("answer-only inference may not be treated as secure evidence")
if inference.get("independentReturn", {}).get("conceptualSupport") != {"level": "H0", "type": "NONE"}:
    fail("independent return must be H0")

source = data.get("adjectiveSourceBoundaryFixture", {})
expected_order = [
    "NUMBER", "OPINION", "SIZE", "AGE", "SHAPE", "COLOUR", "ORIGIN", "MATERIAL", "PURPOSE"
]
if source.get("sourceOrder") != expected_order:
    fail("simplified source adjective order drifted")

boundaries = {item.get("word"): item for item in source.get("boundaryExamples", [])}
for word in ("heavy", "handmade", "broken"):
    item = boundaries.get(word)
    if not item:
        fail(f"missing boundary regression word {word}")
    if item.get("status") != "SOURCE_MODEL_BOUNDARY" or item.get("sourceCategory") is not None:
        fail(f"{word} must remain SOURCE_MODEL_BOUNDARY with no invented source category")

for forbidden in ("QUALITY", "PHYSICAL_QUALITY", "QUALITY_TYPE", "CONDITION"):
    if forbidden not in source.get("forbiddenInventedCategories", []):
        fail(f"missing forbidden invented category {forbidden}")

clarification = source.get("clarificationRegression", {})
if clarification.get("childInput") != "Large?":
    fail("missing Large? clarification regression")
if clarification.get("expectedAnswer") != "SIZE" or "tiny" not in clarification.get("tinyCheck", "").lower():
    fail("clarification must end with tiny -> SIZE check")

routine = source.get("tutorRoutine", [])
if routine[-1:] != ["MARK_SOURCE_BOUNDARY_IF_NO_CLEAN_MATCH"]:
    fail("tutor routine must end by marking source boundary rather than inventing a category")

print("Grade 4 English Phase-5 canonical fixture passed.")
