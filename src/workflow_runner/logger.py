from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from workflow_runner.contract import WorkflowResult


def workflow_result_to_dict(result: WorkflowResult) -> dict[str, Any]:
    return {
        "event_type": "workflow_execution",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "workflow_id": result.workflow_id,
        "status": result.status,
        "steps_executed": result.steps_executed,
        "error": result.error,
        "steps": [
            {
                "step_id": step.step_id,
                "action": step.action,
                "status": step.status,
                "output": step.output,
                "error": step.error,
            }
            for step in result.steps
        ],
    }


def write_execution_log(
    result: WorkflowResult,
    log_path: str | Path,
) -> dict[str, Any]:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = workflow_result_to_dict(result)

    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "log_path": str(path),
        "bytes_written": path.stat().st_size,
    }
