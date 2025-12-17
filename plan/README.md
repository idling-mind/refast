# Refast Development Plan

This directory contains detailed stage-by-stage implementation plans for building the Refast framework.

## Overview

Refast is a Python + React UI framework that enables building reactive web applications with Python-first development.

## Stages

| Stage | File | Description | Dependencies |
|-------|------|-------------|--------------|
| 1 | [stage-1-core.md](./stage-1-core.md) | Core framework foundation | None |
| 2 | [stage-2-components.md](./stage-2-components.md) | Component system | Stage 1 |
| 3 | [stage-3-events.md](./stage-3-events.md) | Event handling & WebSocket | Stage 1, 2 |
| 4 | [stage-4-sessions.md](./stage-4-sessions.md) | Session management | Stage 1 |
| 5 | [stage-5-security.md](./stage-5-security.md) | Security features | Stage 1, 4 |
| 6 | [stage-6-frontend.md](./stage-6-frontend.md) | React frontend client | Stage 2, 3 |
| 7 | [stage-7-integration.md](./stage-7-integration.md) | Full integration | All previous |
| 8 | [stage-8-docs.md](./stage-8-docs.md) | Documentation app | Stage 7 |

## Execution Order

```
Stage 1 (Core)
    │
    ├──► Stage 2 (Components)
    │         │
    │         └──────────────┐
    │                        │
    ├──► Stage 4 (Sessions)  │
    │         │              │
    │         ▼              ▼
    └──► Stage 5 (Security)  Stage 3 (Events)
              │              │
              │              ▼
              └────────► Stage 6 (Frontend)
                              │
                              ▼
                        Stage 7 (Integration)
                              │
                              ▼
                        Stage 8 (Documentation)
```

## How to Use These Plans

1. **Read the stage file** before starting implementation
2. **Follow the task order** within each stage
3. **Complete all tests** before moving to next task
4. **Update documentation** as you implement
5. **Mark tasks complete** in the stage file

## AI Agent Instructions

Each stage file contains:

- **Objectives**: What the stage achieves
- **Prerequisites**: What must be done first
- **Tasks**: Numbered list of specific implementation tasks
- **Files to Create**: Exact files with descriptions
- **Tests to Write**: Required test coverage
- **Acceptance Criteria**: How to verify completion
- **Example Code**: Reference implementations

## Updating Plans

When implementation reveals needed changes:

1. Update the relevant stage file
2. Update `../.github/copilot-instructions.md` if structure changes
3. Add notes about why changes were made
4. Keep the task numbering consistent

## Progress Tracking

Each stage file has a progress section at the top. Update status as:

- `[ ]` Not started
- `[~]` In progress
- `[x]` Complete
- `[!]` Blocked (with reason)
