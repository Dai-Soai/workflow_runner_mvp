from __future__ import annotations

import argparse
import sys

from workflow_runner.executor import execute_workflow
from workflow_runner.loader import WorkflowLoadError, load_workflow
from workflow_runner.logger import write_execution_log
from workflow_runner.validator import WorkflowValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="workflow-runner",
        description="Run YAML-based workflows for RADAR Services utilities.",
    )

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run",
        help="Run a workflow YAML file.",
    )
    run_parser.add_argument(
        "workflow_file",
        help="Path to workflow YAML file.",
    )
    run_parser.add_argument(
        "--log-json",
        help="Write workflow execution log to a JSON file.",
    )

    return parser


def run_command(args: argparse.Namespace) -> int:
    try:
        workflow = load_workflow(args.workflow_file)
        result = execute_workflow(workflow)
    except (WorkflowLoadError, WorkflowValidationError) as exc:
        print(f"Workflow failed to start: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

    print(f"Workflow completed: {result.workflow_id}")
    print(f"Status: {result.status}")
    print(f"Steps executed: {result.steps_executed}")

    if args.log_json:
        log_info = write_execution_log(result, args.log_json)
        print(f"Execution log written: {log_info['log_path']}")

    if result.error:
        print(f"Error: {result.error}", file=sys.stderr)

    return 0 if result.status == "success" else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        return run_command(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
