# Workflow Runner MVP

A minimal YAML-driven workflow runner for RADAR Services utilities.

## Status

MVP Stable

Current version:

```text
v0.1.0
```

## Current test status:

34 passed

## Purpose

Workflow Runner MVP executes local workflows defined in YAML.

It is designed as a reusable automation utility for RADAR Services and can be integrated with File Watcher Automation MVP through event-based contracts.

## Core Flow

workflow.yaml
    ↓
load workflow
    ↓
validate workflow
    ↓
execute steps
    ↓
write output
    ↓
write execution log

## Features

- YAML workflow definition
- Workflow contract dataclasses
- YAML loader
- Step validator
- Sequential action executor
- Action registry
- CLI runner
- JSON execution log
- File Watcher integration example
- Pytest coverage

## Supported Actions

Current MVP actions:

read_text
mock_summary
write_json

## Example Workflow

workflow_id: sample_summary_workflow
version: "0.1.0"

input:
  path: data/inbox/sample.txt

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
      output_path: data/output/summary.json

 ## Installation

Create and activate virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install package in editable mode:

python -m pip install --upgrade pip
python -m pip install -e .     

## Usage

Run sample workflow:

workflow-runner run examples/workflow.sample.yaml

Run sample workflow and write execution log:

workflow-runner run examples/workflow.sample.yaml \
  --log-json logs/execution.sample.json

Expected output:

Workflow completed: sample_summary_workflow
Status: success
Steps executed: 3
Execution log written: logs/execution.sample.json

## Output Example
{
  "result": "RADAR Services is a utility-first system. Workflow Runner can execute YAML workflows."
}

## Execution Log Example
{
  "event_type": "workflow_execution",
  "workflow_id": "sample_summary_workflow",
  "status": "success",
  "steps_executed": 3,
  "error": null,
  "steps": [
    {
      "step_id": "read_file",
      "action": "read_text",
      "status": "success",
      "error": null
    },
    {
      "step_id": "summarize",
      "action": "mock_summary",
      "status": "success",
      "error": null
    },
    {
      "step_id": "export",
      "action": "write_json",
      "status": "success",
      "error": null
    }
  ]
}

## File Watcher Integration

Utility #8 can be triggered by Utility #7 through an event contract.

Example event:

{
  "event_type": "file_detected",
  "source_utility": "file_watcher_automation_mvp",
  "file_path": "data/inbox/sample.txt",
  "workflow_file": "examples/workflow.sample.yaml",
  "event_id": "sample-file-event-001"
}

Integration boundary:

Utility #7 owns file detection and file event logs.
Utility #8 owns workflow execution and execution logs.

No direct package dependency is introduced between Utility #7 and Utility #8.

## Project Structure

```text
workflow_runner_mvp/
├── README.md
├── pyproject.toml
├── examples/
│   ├── file_watcher_event.sample.json
│   ├── file_watcher_integration_example.md
│   └── workflow.sample.yaml
├── src/
│   └── workflow_runner/
│       ├── __init__.py
│       ├── actions.py
│       ├── cli.py
│       ├── contract.py
│       ├── executor.py
│       ├── loader.py
│       ├── logger.py
│       └── validator.py
└── tests/
    ├── test_actions.py
    ├── test_cli.py
    ├── test_contract.py
    ├── test_executor.py
    ├── test_integration_examples.py
    ├── test_loader.py
    ├── test_logger.py
    └── test_validator.py
```

## Development

Run tests:

pytest

Expected:

34 passed

## MVP Scope

Locked for v0.1.0:

- Local YAML workflow execution
- Sequential step execution
- Local file input
- JSON output action
- JSON execution log
- CLI runner
- File Watcher integration example

- Out of scope for v0.1.0:

- Parallel execution
- Conditional branches
- Retry queue
- Scheduler
- Remote execution
- Runtime event bus
- Plugin auto-discovery
- Telegram notification

## Roadmap

Future ideas:

- Plugin action registry
- Action schema validation
- Conditional workflow branches
- Retry policy
- Timeout policy
- Multi-workflow routing
- File Watcher direct trigger mode
- Telegram Notification Hub integration
- Dashboard integration
- RADAR Runtime bridge

## Release Notes
v0.1.0

Initial MVP release.

Completed milestones:

- M1 Bootstrap Project
- M2 Workflow Contract
- M3 YAML Loader
- M4 Step Validator
- M5 Action Executor
- M6 CLI Runner
- M7 Execution Log JSON
- M8 File Watcher Integration Example

Test status:

34 passed

## License

Internal RADAR Services utility.

