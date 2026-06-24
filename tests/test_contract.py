from workflow_runner.contract import (
    WorkflowDefinition,
    WorkflowInput,
    WorkflowResult,
    WorkflowStep,
    StepResult,
    workflow_from_dict,
)


def test_workflow_contract_dataclasses():
    workflow = WorkflowDefinition(
        workflow_id="sample_workflow",
        version="0.1.0",
        input=WorkflowInput(path="data/inbox/sample.txt"),
        steps=[
            WorkflowStep(
                id="read_file",
                action="read_text",
                params={"encoding": "utf-8"},
            )
        ],
    )

    assert workflow.workflow_id == "sample_workflow"
    assert workflow.version == "0.1.0"
    assert workflow.input.path == "data/inbox/sample.txt"
    assert len(workflow.steps) == 1
    assert workflow.steps[0].id == "read_file"
    assert workflow.steps[0].action == "read_text"
    assert workflow.steps[0].params["encoding"] == "utf-8"


def test_workflow_result_helpers():
    result = WorkflowResult(
        workflow_id="sample_workflow",
        status="failed",
        steps=[
            StepResult(
                step_id="read_file",
                action="read_text",
                status="success",
                output="hello",
            ),
            StepResult(
                step_id="summarize",
                action="mock_summary",
                status="failed",
                error="mock error",
            ),
        ],
        error="workflow failed",
    )

    assert result.steps_executed == 2
    assert len(result.succeeded_steps) == 1
    assert len(result.failed_steps) == 1
    assert result.failed_steps[0].step_id == "summarize"


def test_workflow_from_dict():
    payload = {
        "workflow_id": "sample_summary_workflow",
        "version": "0.1.0",
        "input": {
            "path": "data/inbox/sample.txt",
        },
        "steps": [
            {
                "id": "read_file",
                "action": "read_text",
                "params": {
                    "encoding": "utf-8",
                },
            },
            {
                "id": "summarize",
                "action": "mock_summary",
                "params": {
                    "max_sentences": 3,
                },
            },
        ],
    }

    workflow = workflow_from_dict(payload)

    assert workflow.workflow_id == "sample_summary_workflow"
    assert workflow.version == "0.1.0"
    assert workflow.input.path == "data/inbox/sample.txt"
    assert len(workflow.steps) == 2
    assert workflow.steps[0].id == "read_file"
    assert workflow.steps[1].action == "mock_summary"
    assert workflow.steps[1].params["max_sentences"] == 3
