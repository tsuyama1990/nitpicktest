# TODO Application

A simple and robust CLI-based TODO application for tracking personal tasks.

## Features
- Create tasks with title, optional description, priority, and due dates.
- List all your current tasks with their status.
- Mark tasks as completed.
- Delete obsolete tasks.
- Data securely stored locally in JSON format.

## Installation

Ensure you have `uv` installed, then synchronize the environment:

```bash
uv sync
```

## Usage

You can use the `todo` command line interface to manage your tasks.

```bash
# Add a new task
uv run todo add "Buy groceries" --priority high

# List all tasks
uv run todo list

# Mark task with ID 1 as complete
uv run todo complete 1

# Delete a task with ID 1
uv run todo delete 1
```

## Code Structure

```
todo-app/
├── src/
│   ├── domain_models/   # Schemas for tasks (TodoItem, Priority, Status)
│   └── todo/            # CLI interface and local JSON storage logic
├── tests/
│   ├── e2e/             # Tests CLI and user scenarios (UAT)
│   └── unit/            # Tests core logic and data models
├── pyproject.toml
└── README.md
```
