from pathlib import Path

import pytest

from workflow_runner.actions import (
    ActionExecutionError,
    mock_summary,
    read_text,
    write_json,
)


def test_read_text(tmp_path: Path):
    input_file = tmp_path / "sample.txt"
    input_file.write_text("Hello RADAR.", encoding="utf-8")

    result = read_text(str(input_file), {"encoding": "utf-8"})

    assert result == "Hello RADAR."


def test_read_text_missing_file():
    with pytest.raises(ActionExecutionError, match="Input file not found"):
        read_text("missing.txt", {"encoding": "utf-8"})


def test_mock_summary_limits_sentences():
    content = "One. Two. Three. Four."

    result = mock_summary(content, {"max_sentences": 2})

    assert result == "One. Two."


def test_mock_summary_empty_content():
    result = mock_summary("", {"max_sentences": 2})

    assert result == ""


def test_write_json(tmp_path: Path):
    output_file = tmp_path / "output" / "result.json"

    result = write_json("Hello RADAR.", {"output_path": str(output_file)})

    assert output_file.exists()
    assert result["output_path"] == str(output_file)
    assert result["bytes_written"] > 0
    assert '"result": "Hello RADAR."' in output_file.read_text(encoding="utf-8")


def test_write_json_requires_output_path():
    with pytest.raises(ActionExecutionError, match="output_path is required"):
        write_json("Hello RADAR.", {})
