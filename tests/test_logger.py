import json
from pathlib import Path

from workflow_runner.contract import StepResult, WorkflowResult
from workflow_runner.logger import workflow_result_to_dict, write_execution_log


def test_workflow_result_to_dict():
    result = WorkflowResult(
        workflow_id="sample_workflow",
        status="success",
        steps=[
            StepResult(
                step_id="read_file",
                action="read_text",
                status="success",
                output="hello",
            )
        ],
    )

    payload = workflow_result_to_dict(result)

    assert payload["event_type"] == "workflow_execution"
    assert payload["workflow_id"] == "sample_workflow"
    assert payload["status"] == "success"
    assert payload["steps_executed"] == 1
    assert payload["error"] is None
    assert "timestamp" in payload
    assert payload["steps"][0]["step_id"] == "read_file"
    assert payload["steps"][0]["action"] == "read_text"
    assert payload["steps"][0]["status"] == "success"
    assert payload["steps"][0]["output"] == "hello"


def test_write_execution_log(tmp_path: Path):
    log_file = tmp_path / "logs" / "execution.json"

    result = WorkflowResult(
        workflow_id="sample_workflow",
        status="failed",
        steps=[
            StepResult(
                step_id="read_file",
                action="read_text",
                status="failed",
                error="Input file not found",
            )
        ],
        error="Input file not found",
    )

    info = write_execution_log(result, log_file)

    assert log_file.exists()
    assert info["log_path"] == str(log_file)
    assert info["bytes_written"] > 0

    payload = json.loads(log_file.read_text(encoding="utf-8"))

    assert payload["event_type"] == "workflow_execution"
    assert payload["workflow_id"] == "sample_workflow"
    assert payload["status"] == "failed"
    assert payload["steps_executed"] == 1
    assert payload["error"] == "Input file not found"
    assert payload["steps"][0]["status"] == "failed"
