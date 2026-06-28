# CYCLE01 Specification

## Summary
This cycle implements the core CRUD functionality and basic CLI interface for the TODO application. It allows users to add, list, complete, and delete tasks, storing them in a local JSON file.

## Interface Contract

### Domain Models
Schemas must be implemented in `src/domain_models/todo.py` and exported in `src/domain_models/__init__.py`.
```python
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TodoItem(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: int
    title: str = Field(..., min_length=1)
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    due_date: datetime | None = None
```

### Provided Interfaces
- `src/todo/storage.py`
  - `def load_todos(filepath: str) -> list[TodoItem]`
  - `def save_todos(filepath: str, todos: list[TodoItem]) -> None`
- `src/todo/cli.py` (Typer CLI commands)
  - `add(title: str, description: str, priority: Priority, due_date: datetime)`
  - `list()`
  - `complete(item_id: int)`
  - `delete(item_id: int)`

### Dependencies
- None. This is the foundation cycle.

## Infrastructure & Dependencies

### A. Project Secrets (`.env.example`)
- No external secrets required for this cycle. Append an empty `# Target Project Secrets` section if missing.

### B. System Configurations (`docker-compose.yml`)
- No docker configuration required for this cycle as it is a local CLI tool.

### C. Sandbox Resilience
- There are no external API calls in this cycle, so no API mocking is required. Ensure that JSON file storage uses relative or temporary paths during testing to prevent polluting the local environment.

## Implementation Notes
1. Set up the Pydantic models in `src/domain_models/todo.py` and export via `src/domain_models/__init__.py`. Ensure `ConfigDict(extra='forbid')` is strictly applied.
2. Implement JSON read/write logic in `src/todo/storage.py`. Ensure it creates the JSON file if it does not exist. Use robust error handling for malformed JSON.
3. Implement Typer commands in `src/todo/cli.py`.
4. The JSON storage structure should be a list of `TodoItem` JSON objects. Handle auto-incrementing the `id` field when creating new tasks.

## Test Strategy
- **Unit Tests:**
  - Test model validation (valid/invalid inputs).
  - Test JSON storage functions (saving and loading valid/corrupted files) using a temporary directory fixture.
- **Integration Tests:**
  - Test CLI commands using `Typer.testing.CliRunner` ensuring files are written and read correctly using a mocked file path or temporary directory.
