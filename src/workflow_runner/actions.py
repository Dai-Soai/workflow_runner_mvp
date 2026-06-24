from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ActionExecutionError(Exception):
    """Raised when an action fails during execution."""


def read_text(input_path: str, params: dict[str, Any]) -> str:
    encoding = str(params.get("encoding", "utf-8"))
    path = Path(input_path)

    if not path.exists():
        raise ActionExecutionError(f"Input file not found: {path}")

    return path.read_text(encoding=encoding)


def mock_summary(content: str, params: dict[str, Any]) -> str:
    max_sentences = int(params.get("max_sentences", 3))

    sentences = [
        sentence.strip()
        for sentence in content.replace("\n", " ").split(".")
        if sentence.strip()
    ]

    selected = sentences[:max_sentences]

    if not selected:
        return ""

    return ". ".join(selected) + "."


def write_json(content: Any, params: dict[str, Any]) -> dict[str, Any]:
    output_path = params.get("output_path")

    if not output_path:
        raise ActionExecutionError("output_path is required for write_json")

    path = Path(str(output_path))
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "result": content,
    }

    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "output_path": str(path),
        "bytes_written": path.stat().st_size,
    }


ACTION_REGISTRY = {
    "read_text": read_text,
    "mock_summary": mock_summary,
    "write_json": write_json,
}
