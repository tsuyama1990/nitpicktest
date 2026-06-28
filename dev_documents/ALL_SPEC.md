# TODO Application

## Overview
A simple CLI-based TODO application that allows users to manage tasks.

## Functional Requirements

### Cycle 1: Core CRUD + CLI Interface
- Create TODO items with title, description, priority (low/medium/high), and due date
- List all TODO items with their status
- Mark a TODO item as complete
- Delete a TODO item
- CLI interface with commands: `add`, `list`, `complete`, `delete`
- Store data in a local JSON file

### Cycle 2: Search, Filter & Persistence Enhancement
- Filter TODOs by status (completed/pending) and priority (low/medium/high)
- Search TODOs by keyword in title/description
- Sort TODOs by due date or priority
- Edit existing TODO items
- Data validation

## Project Structure
```
todo-app/
├── todo/
│   ├── __init__.py
│   ├── cli.py
│   ├── models.py
│   ├── storage.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_cli.py
├── pyproject.toml
└── README.md
```
