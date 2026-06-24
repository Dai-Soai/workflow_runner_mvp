from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from workflow_runner.contract import WorkflowDefinition, workflow_from_dict


class WorkflowLoadError(Exception):
    """Raised when workflow YAML cannot be loaded."""


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    """
    Load a YAML file and return its raw dictionary payload.
    """

    workflow_path = Path(path)

    if not workflow_path.exists():
        raise WorkflowLoadError(f"Workflow file not found: {workflow_path}")

    if not workflow_path.is_file():
        raise WorkflowLoadError(f"Workflow path is not a file: {workflow_path}")

    try:
        with workflow_path.open("r", encoding="utf-8") as file:
            payload = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        raise WorkflowLoadError(f"Invalid YAML file: {workflow_path}") from exc

    if payload is None:
        raise WorkflowLoadError(f"Workflow file is empty: {workflow_path}")

    if not isinstance(payload, dict):
        raise WorkflowLoadError(
            f"Workflow YAML root must be a dictionary: {workflow_path}"
        )

    return payload


def load_workflow(path: str | Path) -> WorkflowDefinition:
    """
    Load workflow YAML file and convert it into WorkflowDefinition.
    """

    payload = load_yaml_file(path)
    return workflow_from_dict(payload)
