from pathlib import Path

from workflow_runner.contract import WorkflowDefinition, WorkflowInput, WorkflowStep
from workflow_runner.executor import execute_workflow


def test_execute_workflow_success(tmp_path: Path):
    input_file = tmp_path / "sample.txt"
    output_file = tmp_path / "output" / "summary.json"

    input_file.write_text(
        "RADAR is a service system. It can run utilities. It can automate workflows.",
        encoding="utf-8",
    )

    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path=str(input_file)),
        steps=[
            WorkflowStep(
                id="read_file",
                action="read_text",
                params={"encoding": "utf-8"},
            ),
            WorkflowStep(
                id="summarize",
                action="mock_summary",
                params={"max_sentences": 2},
            ),
            WorkflowStep(
                id="export",
                action="write_json",
                params={"output_path": str(output_file)},
            ),
        ],
    )

    result = execute_workflow(workflow)

    assert result.status == "success"
    assert result.workflow_id == "sample_workflow"
    assert result.steps_executed == 3
    assert len(result.failed_steps) == 0
    assert output_file.exists()


def test_execute_workflow_failed_step(tmp_path: Path):
    missing_file = tmp_path / "missing.txt"
    output_file = tmp_path / "output" / "summary.json"

    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path=str(missing_file)),
        steps=[
            WorkflowStep(
                id="read_file",
                action="read_text",
                params={"encoding": "utf-8"},
            ),
            WorkflowStep(
                id="export",
                action="write_json",
                params={"output_path": str(output_file)},
            ),
        ],
    )

    result = execute_workflow(workflow)

    assert result.status == "failed"
    assert result.steps_executed == 1
    assert result.failed_steps[0].step_id == "read_file"
    assert "Input file not found" in str(result.error)
    assert not output_file.exists()
