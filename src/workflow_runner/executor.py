from __future__ import annotations

from typing import Any

from workflow_runner.actions import ACTION_REGISTRY, ActionExecutionError
from workflow_runner.contract import StepResult, WorkflowDefinition, WorkflowResult
from workflow_runner.validator import validate_workflow


class WorkflowExecutionError(Exception):
    """Raised when workflow execution cannot start or complete."""


def execute_workflow(workflow: WorkflowDefinition) -> WorkflowResult:
    validate_workflow(workflow)

    step_results: list[StepResult] = []
    current_value: Any = workflow.input.path

    for step in workflow.steps:
        try:
            action = ACTION_REGISTRY.get(step.action)

            if action is None:
                raise WorkflowExecutionError(f"unknown action: {step.action}")

            output = action(current_value, step.params)

            step_results.append(
                StepResult(
                    step_id=step.id,
                    action=step.action,
                    status="success",
                    output=output,
                )
            )

            current_value = output

        except (ActionExecutionError, WorkflowExecutionError, Exception) as exc:
            step_results.append(
                StepResult(
                    step_id=step.id,
                    action=step.action,
                    status="failed",
                    error=str(exc),
                )
            )

            return WorkflowResult(
                workflow_id=workflow.workflow_id,
                status="failed",
                steps=step_results,
                error=str(exc),
            )

    return WorkflowResult(
        workflow_id=workflow.workflow_id,
        status="success",
        steps=step_results,
    )
