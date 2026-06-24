from __future__ import annotations

from workflow_runner.contract import WorkflowDefinition


class WorkflowValidationError(Exception):
    """Raised when workflow definition is invalid."""


SUPPORTED_ACTIONS = {
    "read_text",
    "mock_summary",
    "write_json",
}


def validate_workflow(workflow: WorkflowDefinition) -> WorkflowDefinition:
    if not workflow.workflow_id.strip():
        raise WorkflowValidationError("workflow_id is required")

    if not workflow.version.strip():
        raise WorkflowValidationError("version is required")

    if not workflow.input.path.strip():
        raise WorkflowValidationError("input.path is required")

    if not workflow.steps:
        raise WorkflowValidationError("steps must not be empty")

    seen_step_ids: set[str] = set()

    for index, step in enumerate(workflow.steps):
        if not step.id.strip():
            raise WorkflowValidationError(f"steps[{index}].id is required")

        if step.id in seen_step_ids:
            raise WorkflowValidationError(f"duplicate step id: {step.id}")

        seen_step_ids.add(step.id)

        if not step.action.strip():
            raise WorkflowValidationError(f"steps[{index}].action is required")

        if step.action not in SUPPORTED_ACTIONS:
            raise WorkflowValidationError(f"unsupported action: {step.action}")

        if not isinstance(step.params, dict):
            raise WorkflowValidationError(f"steps[{index}].params must be a dictionary")

    return workflow
