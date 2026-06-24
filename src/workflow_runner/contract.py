from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

WorkflowStatus = Literal["success", "failed"]
StepStatus = Literal["success", "failed", "skipped"]


@dataclass(frozen=True)
class WorkflowInput:
    """
    Input contract for a workflow.

    For MVP v0.1.0, we only support a local input path.
    """

    path: str


@dataclass(frozen=True)
class WorkflowStep:
    """
    One executable step in a workflow.

    Example:
        id: read_file
        action: read_text
        params:
          encoding: utf-8
    """

    id: str
    action: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WorkflowDefinition:
    """
    Top-level workflow definition loaded from YAML.
    """

    workflow_id: str
    version: str
    input: WorkflowInput
    steps: list[WorkflowStep]


@dataclass(frozen=True)
class StepResult:
    """
    Result returned after one step execution.
    """

    step_id: str
    action: str
    status: StepStatus
    output: Any = None
    error: str | None = None


@dataclass(frozen=True)
class WorkflowResult:
    """
    Final workflow execution result.
    """

    workflow_id: str
    status: WorkflowStatus
    steps: list[StepResult]
    error: str | None = None

    @property
    def steps_executed(self) -> int:
        return len(self.steps)

    @property
    def failed_steps(self) -> list[StepResult]:
        return [step for step in self.steps if step.status == "failed"]

    @property
    def succeeded_steps(self) -> list[StepResult]:
        return [step for step in self.steps if step.status == "success"]


def workflow_from_dict(payload: dict[str, Any]) -> WorkflowDefinition:
    """
    Convert raw YAML dictionary into WorkflowDefinition.

    Validation is intentionally light here.
    Strong validation will live in validator.py.
    """

    input_payload = payload.get("input") or {}
    step_payloads = payload.get("steps") or []

    workflow_input = WorkflowInput(path=str(input_payload.get("path", "")))

    steps = [
        WorkflowStep(
            id=str(step.get("id", "")),
            action=str(step.get("action", "")),
            params=dict(step.get("params") or {}),
        )
        for step in step_payloads
    ]

    return WorkflowDefinition(
        workflow_id=str(payload.get("workflow_id", "")),
        version=str(payload.get("version", "")),
        input=workflow_input,
        steps=steps,
    )
