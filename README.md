# TODO CLI Application

A simple and robust Command-Line Interface (CLI) application for managing your TODO lists. This application stores your tasks locally in a JSON file and uses Pydantic for data validation.

## Features
- **Add Tasks:** Create a task with a title, description, priority, and due date.
- **List Tasks:** View all your tasks, along with their status, priority, and details.
- **Complete Tasks:** Mark tasks as done to track progress.
- **Delete Tasks:** Remove unwanted or obsolete tasks from the list.

## Installation

This project uses `uv` for dependency management. To set up the environment and run the app, run the following:

```bash
uv sync
```

## Usage
The CLI uses Typer to provide clean, easy-to-use commands.

### Adding a Task
```bash
uv run todo add "Buy groceries" --priority high --desc "Milk, Eggs, Bread"
```

### Listing Tasks
```bash
uv run todo list
```

### Marking a Task Complete
```bash
uv run todo complete <ID>
```

### Deleting a Task
```bash
uv run todo delete <ID>
```

## Code Structure
- `src/domain_models/`: Contains Pydantic data schemas enforcing structure for Todo items, Priority, and Status.
- `src/todo/storage.py`: Handles local JSON read/write logic.
- `src/todo/cli.py`: Typer command definitions.
- `tests/`: Contains comprehensive unit, e2e, and User Acceptance Tests (UAT).
