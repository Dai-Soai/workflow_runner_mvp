# File Watcher Integration Example

## Purpose

This document describes how Utility #7 — File Watcher Automation MVP can trigger Utility #8 — Workflow Runner MVP without creating a hard dependency between the two utilities.

## Integration Flow

```text
File Watcher detects a new file
        ↓
File Watcher emits event JSON
        ↓
Workflow Runner receives workflow file path
        ↓
Workflow Runner executes workflow YAML
        ↓
Workflow Runner writes execution log JSON
```

## Contract Boundary

Utility #7 owns:

- file detection
- file event JSON
- inbox/archive movement
- file watcher event log

Utility #8 owns:

- workflow YAML loading
- workflow validation
- sequential step execution
- workflow execution log JSON

## Locked Decision

No direct package dependency is introduced between Utility #7 and Utility #8.
