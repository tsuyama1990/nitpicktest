# TODO Application

A simple and robust CLI-based TODO application to manage tasks, built with Typer and Pydantic.

## Features
- **Add tasks:** Create TODO items with title, description, priority, and due date.
- **List & Filter:** View tasks. Filter by status (pending/completed) and priority. Sort by ID, priority, or due date.
- **Search:** Quickly find tasks by keyword in the title or description.
- **Edit tasks:** Update details of existing tasks seamlessly.
- **Complete & Delete:** Mark tasks as completed or remove them entirely.
- **JSON Storage:** All data is safely stored in a local JSON file.

## Installation

Ensure you have Python 3.12+ and `uv` installed.

```bash
uv pip install -e .
```

## Usage

You can use the `todo` command line interface to manage your tasks.

```bash
# Add a task
todo add "Buy Groceries" --description "Milk, eggs, and bread" --priority high

# List tasks
todo list
todo list --status pending --sort-by priority

# Search for a task
todo search "milk"

# Edit a task
todo edit 1 --priority medium

# Complete a task
todo complete 1

# Delete a task
todo delete 1
```

## Code Structure
- `src/domain_models/`: Contains the Pydantic data schemas.
- `src/todo/cli.py`: Contains the Typer CLI definitions and command logic.
- `src/todo/storage.py`: Handles local JSON data persistence.
