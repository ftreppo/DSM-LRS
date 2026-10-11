from pathlib import Path

STATES = {"AVAILABLE", "NOT_FOUND", "ACCESS_DENIED", "UNAVAILABLE", "UNVERIFIED"}


def resolve_local(root: Path, relative: str):
    if not root.exists():
        return {"status": "UNAVAILABLE", "content": None}
    target = (root / relative).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return {"status": "NOT_FOUND", "content": None}
    if not target.exists():
        return {"status": "NOT_FOUND", "content": None}
    try:
        return {"status": "AVAILABLE", "content": target.read_text(encoding="utf-8")}
    except PermissionError:
        return {"status": "ACCESS_DENIED", "content": None}


def status_from_provider_error(error):
    if isinstance(error, PermissionError):
        return "ACCESS_DENIED"
    if isinstance(error, FileNotFoundError):
        return "NOT_FOUND"
    return "UNAVAILABLE"


def consumer_action(result, *, authority_required=False):
    assert result["status"] in STATES
    if result["status"] == "AVAILABLE":
        return "USE_SOURCE"
    if authority_required:
        return "STOP_FAIL_CLOSED"
    return "CONTINUE_WITHOUT_LIBRARY_SOURCE"


def test_available_local_source(tmp_path):
    root = tmp_path / "library"
    root.mkdir()
    (root / "source.txt").write_text("synthetic reference", encoding="utf-8")
    result = resolve_local(root, "source.txt")
    assert result == {"status": "AVAILABLE", "content": "synthetic reference"}
    assert consumer_action(result, authority_required=True) == "USE_SOURCE"


def test_missing_root_is_unavailable_and_has_no_content(tmp_path):
    result = resolve_local(tmp_path / "missing", "source.txt")
    assert result["status"] == "UNAVAILABLE"
    assert result["content"] is None
    assert consumer_action(result, authority_required=True) == "STOP_FAIL_CLOSED"


def test_missing_source_does_not_fallback(tmp_path):
    root = tmp_path / "library"
    root.mkdir()
    result = resolve_local(root, "missing.txt")
    assert result == {"status": "NOT_FOUND", "content": None}
    assert consumer_action(result, authority_required=True) == "STOP_FAIL_CLOSED"


def test_access_denied_is_explicit():
    assert status_from_provider_error(PermissionError()) == "ACCESS_DENIED"
    result = {"status": "ACCESS_DENIED", "content": None}
    assert consumer_action(result, authority_required=True) == "STOP_FAIL_CLOSED"


def test_non_authority_workflow_can_continue_without_library():
    result = {"status": "UNAVAILABLE", "content": None}
    assert consumer_action(result, authority_required=False) == "CONTINUE_WITHOUT_LIBRARY_SOURCE"


def test_unverified_authority_fails_closed():
    result = {"status": "UNVERIFIED", "content": None}
    assert consumer_action(result, authority_required=True) == "STOP_FAIL_CLOSED"
