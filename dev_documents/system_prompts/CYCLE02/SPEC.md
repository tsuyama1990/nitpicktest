# CYCLE02 Specification

## Summary
This cycle enhances the existing TODO application by adding capabilities to filter tasks by status or priority, search tasks by keyword, sort tasks by specific attributes, and edit existing task details.

## Interface Contract

### Provided Interfaces (Enhancements)
- `src/todo/storage.py`
  - `def search_todos(filepath: str, keyword: str) -> list[TodoItem]`
  - `def filter_todos(filepath: str, status: Status | None = None, priority: Priority | None = None) -> list[TodoItem]`
  - `def sort_todos(todos: list[TodoItem], sort_by: str) -> list[TodoItem]`
- `src/todo/cli.py` (Typer CLI commands)
  - Enhance `list(status: Status | None, priority: Priority | None, sort_by: str | None)`
  - `search(keyword: str)`
  - `edit(item_id: int, title: str | None, description: str | None, priority: Priority | None, due_date: datetime | None)`

### Dependencies
- Relies on the JSON storage format and domain models defined in **CYCLE01**.

## Infrastructure & Dependencies

### A. Project Secrets (`.env.example`)
- No external secrets required for this cycle. Append an empty `# Target Project Secrets` section if missing.

### B. System Configurations (`docker-compose.yml`)
- No docker configuration required for this cycle.

### C. Sandbox Resilience
- There are no external API calls in this cycle, so no API mocking is required. Ensure that JSON file storage uses relative or temporary paths during testing to prevent polluting the local environment.

## Implementation Notes
1. Enhance the `src/todo/storage.py` logic to query and filter `TodoItem` lists based on given attributes without modifying the underlying domain models in `src/domain_models/todo.py`.
2. In `src/todo/cli.py`, add the `search` and `edit` commands.
   - **CRITICAL:** For the `edit` command handling partial updates with Pydantic V2, you MUST use `model_dump(exclude_unset=True)` to extract explicitly provided fields. Avoid explicitly passing `None` during model instantiation for fields you want to remain unset, as they will override existing data with `None`.
3. Update the existing `list` CLI command to accept optional parameters for filtering (`status`, `priority`) and sorting (`sort_by`).
4. Ensure data validation is strictly applied on edit operations.

## Test Strategy
- **Unit Tests:**
  - Test filtering, searching, and sorting functions with various combinations of attributes.
  - Test partial update logic for the `edit` function.
- **Integration Tests:**
  - Test the new CLI commands using `Typer.testing.CliRunner` ensuring search and edit operations reflect accurately in the JSON storage.
