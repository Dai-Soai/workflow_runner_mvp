from pathlib import Path

import pytest

from workflow_runner.loader import WorkflowLoadError, load_workflow, load_yaml_file


def test_load_yaml_file(tmp_path: Path):
    workflow_file = tmp_path / "workflow.yaml"
    workflow_file.write_text(
        """
workflow_id: sample_workflow
version: "0.1.0"

input:
  path: data/inbox/sample.txt

steps:
  - id: read_file
    action: read_text
    params:
      encoding: utf-8
""",
        encoding="utf-8",
    )

    payload = load_yaml_file(workflow_file)

    assert payload["workflow_id"] == "sample_workflow"
    assert payload["version"] == "0.1.0"
    assert payload["input"]["path"] == "data/inbox/sample.txt"
    assert payload["steps"][0]["id"] == "read_file"


def test_load_workflow(tmp_path: Path):
    workflow_file = tmp_path / "workflow.yaml"
    workflow_file.write_text(
        """
workflow_id: sample_workflow
version: "0.1.0"

input:
  path: data/inbox/sample.txt

steps:
  - id: read_file
    action: read_text
    params:
      encoding: utf-8
  - id: summarize
    action: mock_summary
    params:
      max_sentences: 3
""",
        encoding="utf-8",
    )

    workflow = load_workflow(workflow_file)

    assert workflow.workflow_id == "sample_workflow"
    assert workflow.version == "0.1.0"
    assert workflow.input.path == "data/inbox/sample.txt"
    assert len(workflow.steps) == 2
    assert workflow.steps[0].action == "read_text"
    assert workflow.steps[1].action == "mock_summary"


def test_load_missing_workflow_file():
    with pytest.raises(WorkflowLoadError):
        load_workflow("missing-workflow.yaml")


def test_load_empty_workflow_file(tmp_path: Path):
    workflow_file = tmp_path / "empty.yaml"
    workflow_file.write_text("", encoding="utf-8")

    with pytest.raises(WorkflowLoadError):
        load_workflow(workflow_file)


def test_load_invalid_yaml_root(tmp_path: Path):
    workflow_file = tmp_path / "invalid-root.yaml"
    workflow_file.write_text(
        """
- item1
- item2
""",
        encoding="utf-8",
    )

    with pytest.raises(WorkflowLoadError):
        load_workflow(workflow_file)
