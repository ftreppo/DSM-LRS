import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = (ROOT / "adapter" / "generic-prototype" / "LRS_ADAPTER_GENERIC_v0.1.md").read_text(encoding="utf-8")
SCHEMA = json.loads((ROOT / "specifications" / "adapter-generic" / "PolicyPack.schema.json").read_text(encoding="utf-8"))
FIXTURE = json.loads((ROOT / "adapter" / "generic-prototype" / "fixtures" / "policy-pack.synthetic.json").read_text(encoding="utf-8"))

FORBIDDEN_DEPENDENCIES = [
    "DSM-LRS",
    "Deutsche Schule Mailand",
    "DSM-SCHULSTUFEN-GATE",
    "DSM-Leitplanken",
    "APPROVED Personal Prompt",
    "MindMap",
    "Notion",
    "drive.google.com",
    "docs.google.com",
]


def validate_work_item(item):
    required = {"material", "subject_or_activity", "objective", "use_case"}
    missing = sorted(required - set(item))
    if missing:
        return {"ok": False, "reason": "MISSING_INPUT", "missing": missing}
    if item["use_case"] not in {"STUDY", "HOMEWORK", "ASSESSMENT"}:
        return {"ok": False, "reason": "INVALID_USE_CASE"}
    if item["use_case"] == "ASSESSMENT" and not item.get("assessed_competence"):
        return {"ok": False, "reason": "ASSESSED_COMPETENCE_REQUIRED"}
    return {"ok": True}


def executable_measures(pack):
    return [m for m in pack["measures"] if m["status"] == "CONFIRMED"]


def test_generic_instruction_has_no_specific_runtime_dependency():
    lower = ADAPTER.lower()
    for term in FORBIDDEN_DEPENDENCIES:
        assert term.lower() not in lower


def test_generic_instruction_contains_required_modes_and_commands():
    for token in [
        "STUDY",
        "HOMEWORK",
        "ASSESSMENT",
        "ORIGINAL_FAITHFUL",
        "READING_OPTIMIZED",
        "LEARNING_VERSION",
        "ASSESSMENT_ADAPTATION",
        "LRS-ADAPTER HELP",
    ]:
        assert token in ADAPTER


def test_policy_fixture_conforms():
    errors = list(Draft202012Validator(SCHEMA).iter_errors(FIXTURE))
    assert errors == []


def test_study_runs_without_policy_pack():
    result = validate_work_item({
        "material": "Synthetic reading text",
        "subject_or_activity": "History",
        "objective": "Study the causes",
        "use_case": "STUDY",
    })
    assert result == {"ok": True}


def test_assessment_fails_closed_without_assessed_competence():
    result = validate_work_item({
        "material": "Synthetic assessment",
        "subject_or_activity": "Mathematics",
        "objective": "Assessment",
        "use_case": "ASSESSMENT",
    })
    assert result["ok"] is False
    assert result["reason"] == "ASSESSED_COMPETENCE_REQUIRED"


def test_assessment_accepts_competence_with_generic_fixture():
    result = validate_work_item({
        "material": "Synthetic assessment",
        "subject_or_activity": "Mathematics",
        "objective": "Assessment",
        "use_case": "ASSESSMENT",
        "assessed_competence": "solve linear equations",
        "policy_context": FIXTURE,
    })
    assert result == {"ok": True}


def test_only_confirmed_measures_are_executable_by_default():
    measures = executable_measures(FIXTURE)
    assert [m["measure_id"] for m in measures] == ["M-001"]


def test_generic_artifacts_contain_no_private_locator():
    combined = ADAPTER + json.dumps(FIXTURE)
    assert "drive.google.com" not in combined
    assert "docs.google.com" not in combined
    assert "/mnt/data" not in combined
