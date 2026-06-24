import pytest

from workflow_runner.contract import (
    WorkflowDefinition,
    WorkflowInput,
    WorkflowStep,
)
from workflow_runner.validator import WorkflowValidationError, validate_workflow


def make_valid_workflow() -> WorkflowDefinition:
    return WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[
            WorkflowStep(
                id="read_file",
                action="read_text",
                params={"encoding": "utf-8"},
            ),
            WorkflowStep(
                id="summarize",
                action="mock_summary",
                params={"max_sentences": 3},
            ),
            WorkflowStep(
                id="export",
                action="write_json",
                params={"output_path": "data/output/summary.json"},
            ),
        ],
    )


def test_validate_valid_workflow():
    workflow = make_valid_workflow()

    validated = validate_workflow(workflow)

    assert validated.workflow_id == "sample_workflow"
    assert len(validated.steps) == 3


def test_validate_requires_workflow_id():
    workflow = WorkflowDefinition(
        workflow_id="",
        version="0.1.0",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[
            WorkflowStep(id="read_file", action="read_text"),
        ],
    )

    with pytest.raises(WorkflowValidationError, match="workflow_id is required"):
        validate_workflow(workflow)


def test_validate_requires_version():
    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[
            WorkflowStep(id="read_file", action="read_text"),
        ],
    )

    with pytest.raises(WorkflowValidationError, match="version is required"):
        validate_workflow(workflow)


def test_validate_requires_input_path():
    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path=""),
        steps=[
            WorkflowStep(id="read_file", action="read_text"),
        ],
    )

    with pytest.raises(WorkflowValidationError, match="input.path is required"):
        validate_workflow(workflow)


def test_validate_requires_steps():
    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[],
    )

    with pytest.raises(WorkflowValidationError, match="steps must not be empty"):
        validate_workflow(workflow)


def test_validate_requires_step_id():
    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[
            WorkflowStep(id="", action="read_text"),
        ],
    )

    with pytest.raises(WorkflowValidationError, match=r"steps\[0\].id is required"):
        validate_workflow(workflow)


def test_validate_rejects_duplicate_step_id():
    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[
            WorkflowStep(id="read_file", action="read_text"),
            WorkflowStep(id="read_file", action="mock_summary"),
        ],
    )

    with pytest.raises(WorkflowValidationError, match="duplicate step id: read_file"):
        validate_workflow(workflow)


def test_validate_requires_action():
    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[
            WorkflowStep(id="read_file", action=""),
        ],
    )

    with pytest.raises(WorkflowValidationError, match=r"steps\[0\].action is required"):
        validate_workflow(workflow)


def test_validate_rejects_unsupported_action():
    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[
            WorkflowStep(id="unknown", action="unknown_action"),
        ],
    )

    with pytest.raises(
        WorkflowValidationError, match="unsupported action: unknown_action"
    ):
        validate_workflow(workflow)
