# TODO Application

## Overview
A simple, robust CLI-based TODO application that allows users to manage their tasks directly from the terminal. This tool helps you track what needs to be done, set priorities, and mark items as completed.

## Features
- Add new tasks with descriptions, priority levels (low, medium, high), and optional due dates.
- List all tasks with their current status and priority.
- Mark tasks as completed.
- Delete tasks.
- Data is securely stored locally in a JSON file.

## Installation

1. Ensure you have `uv` installed.
2. Clone this repository and navigate to the root directory.
3. Install the application and its dependencies:
```bash
uv sync
uv pip install -e .
```

## Usage

You can use the `todo` command to interact with the application.

**Add a new task:**
```bash
todo add "Buy groceries" --priority high
```

**Add a task with description and due date:**
```bash
todo add "Finish report" --desc "Quarterly financial report" --due "2023-12-31T23:59:59"
```

**List all tasks:**
```bash
todo list
```

**Complete a task:**
(Use the ID shown in the `todo list` output)
```bash
todo complete 1
```

**Delete a task:**
```bash
todo delete 1
```

## Code Structure
```
app/
├── src/
│   ├── domain_models/      # Pydantic schemas and configuration
│   │   ├── config.py
│   │   └── todo.py
│   └── todo/               # CLI logic and storage handlers
│       ├── cli.py          # Typer CLI application
│       └── storage.py      # JSON persistence logic
├── tests/                  # Unit and E2E tests
└── pyproject.toml          # Project metadata and dependencies
```
