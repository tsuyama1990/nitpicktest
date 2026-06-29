# CLI TODO Application

## Overview
A lightweight and fast Command Line Interface (CLI) application for managing your daily tasks (TODOs). It operates entirely locally and saves your data into a clear and human-readable JSON file.

## Features
- **Add Tasks**: Quickly add tasks with a priority and an optional due date.
- **List Tasks**: View all your current tasks presented in an organized table layout.
- **Complete Tasks**: Simply mark tasks as done with a single command.
- **Delete Tasks**: Remove items securely when you no longer need them.
- **Local Storage**: All data securely stored on your system in a simple JSON structure.

## Installation
You can run this application immediately if you have python and `uv` installed.
1. Run `uv sync` to install dependencies and properly setup the virtual environment.

## Usage

### Add a new Task
```bash
uv run todo add "Buy groceries" --priority high
```

### List all Tasks
```bash
uv run todo list
```

### Mark a Task as Completed
```bash
uv run todo complete 1
```

### Delete a Task
```bash
uv run todo delete 1
```

## Code Structure
- `src/domain_models/`: The models governing the items used across the system using Pydantic.
- `src/todo/`: The actual business logic components, storage mechanism implementations, and the `Typer` CLI interface.
- `tests/`: End to End, integration, and unit tests covering usage functionality.
