import json
from pathlib import Path


def test_file_watcher_event_sample_exists():
    event_file = Path("examples/file_watcher_event.sample.json")

    assert event_file.exists()


def test_file_watcher_event_sample_contract():
    event_file = Path("examples/file_watcher_event.sample.json")
    payload = json.loads(event_file.read_text(encoding="utf-8"))

    assert payload["event_type"] == "file_detected"
    assert payload["source_utility"] == "file_watcher_automation_mvp"
    assert payload["file_path"] == "data/inbox/sample.txt"
    assert payload["workflow_file"] == "examples/workflow.sample.yaml"
    assert payload["event_id"] == "sample-file-event-001"


def test_file_watcher_integration_doc_exists():
    doc_file = Path("examples/file_watcher_integration_example.md")

    assert doc_file.exists()
    content = doc_file.read_text(encoding="utf-8")

    assert "Utility #7" in content
    assert "Utility #8" in content
    assert "No direct package dependency" in content
