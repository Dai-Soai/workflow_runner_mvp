from pathlib import Path

from workflow_runner.cli import main


def test_cli_run_success(tmp_path: Path, monkeypatch, capsys):
    input_file = tmp_path / "sample.txt"
    output_file = tmp_path / "output" / "summary.json"
    workflow_file = tmp_path / "workflow.yaml"

    input_file.write_text(
        "RADAR Services is useful. Workflow Runner executes steps. Automation comes next.",
        encoding="utf-8",
    )

    workflow_file.write_text(
        f"""
workflow_id: cli_sample_workflow
version: "0.1.0"

input:
  path: {input_file}

steps:
  - id: read_file
    action: read_text
    params:
      encoding: utf-8

  - id: summarize
    action: mock_summary
    params:
      max_sentences: 2

  - id: export
    action: write_json
    params:
      output_path: {output_file}
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["workflow-runner", "run", str(workflow_file)],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Workflow completed: cli_sample_workflow" in captured.out
    assert "Status: success" in captured.out
    assert "Steps executed: 3" in captured.out
    assert output_file.exists()


def test_cli_run_missing_file(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["workflow-runner", "run", "missing.yaml"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Workflow failed to start" in captured.err


def test_cli_help(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["workflow-runner"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Run YAML-based workflows" in captured.out


def test_cli_run_with_json_log(tmp_path: Path, monkeypatch, capsys):
    input_file = tmp_path / "sample.txt"
    output_file = tmp_path / "output" / "summary.json"
    log_file = tmp_path / "logs" / "execution.json"
    workflow_file = tmp_path / "workflow.yaml"

    input_file.write_text(
        "RADAR logs workflows. Execution logs support audit trails.",
        encoding="utf-8",
    )

    workflow_file.write_text(
        f"""
workflow_id: cli_log_workflow
version: "0.1.0"

input:
  path: {input_file}

steps:
  - id: read_file
    action: read_text
    params:
      encoding: utf-8

  - id: summarize
    action: mock_summary
    params:
      max_sentences: 2

  - id: export
    action: write_json
    params:
      output_path: {output_file}
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "workflow-runner",
            "run",
            str(workflow_file),
            "--log-json",
            str(log_file),
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Execution log written:" in captured.out
    assert log_file.exists()
