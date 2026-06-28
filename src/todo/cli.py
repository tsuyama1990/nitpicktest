from typing import Optional, Any
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

from domain_models import TodoItem, TodoItemUpdate, Priority, Status
from todo.storage import load_todos, save_todos, search_todos, filter_todos, sort_todos
from todo.config import settings

app = typer.Typer(help="CLI-based TODO application")
console = Console()


def get_db_path() -> str:
    return settings.todo_db_path


def _print_todos(todos: list[TodoItem]) -> None:
    if not todos:
        console.print("No TODOs found.", style="bold yellow")
        return
    table = Table("ID", "Title", "Priority", "Status", "Due Date")
    for todo in todos:
        due = todo.due_date.strftime("%Y-%m-%d %H:%M") if todo.due_date else "None"
        table.add_row(str(todo.id), todo.title, todo.priority.value, todo.status.value, due)
    console.print(table)


@app.command()
def add(
    title: str = typer.Argument(..., help="Title of the task"),
    description: Optional[str] = typer.Option(None, help="Task description"),
    priority: Priority = typer.Option(Priority.MEDIUM, help="Task priority"),
    due_date: Optional[datetime] = typer.Option(None, help="Due date (YYYY-MM-DD HH:MM:SS)"),
) -> None:
    """Add a new TODO item."""
    db_path = get_db_path()
    todos = load_todos(db_path)

    new_id = 1 if not todos else max(t.id for t in todos) + 1
    new_todo = TodoItem(id=new_id, title=title, description=description, priority=priority, due_date=due_date)
    todos.append(new_todo)
    save_todos(db_path, todos)
    console.print(f"Added task: {title} (ID: {new_id})", style="bold green")


@app.command("list")
def list_todos(
    status: Optional[Status] = typer.Option(None, help="Filter by status"),
    priority: Optional[Priority] = typer.Option(None, help="Filter by priority"),
    sort_by: str = typer.Option("id", help="Sort by: id, priority, due_date"),
) -> None:
    """List TODO items with optional filtering and sorting."""
    db_path = get_db_path()
    # Apply filtering
    todos = filter_todos(db_path, status=status, priority=priority)
    # Apply sorting
    sorted_todos = sort_todos(todos, sort_by)
    _print_todos(sorted_todos)


@app.command()
def complete(item_id: int = typer.Argument(..., help="ID of the task to complete")) -> None:
    """Mark a TODO item as completed."""
    db_path = get_db_path()
    todos = load_todos(db_path)
    for todo in todos:
        if todo.id == item_id:
            todo.status = Status.COMPLETED
            save_todos(db_path, todos)
            console.print(f"Task {item_id} marked as completed.", style="bold green")
            return
    console.print(f"Task {item_id} not found.", style="bold red")


@app.command()
def delete(item_id: int = typer.Argument(..., help="ID of the task to delete")) -> None:
    """Delete a TODO item."""
    db_path = get_db_path()
    todos = load_todos(db_path)
    initial_count = len(todos)
    todos = [t for t in todos if t.id != item_id]

    if len(todos) < initial_count:
        save_todos(db_path, todos)
        console.print(f"Task {item_id} deleted.", style="bold green")
    else:
        console.print(f"Task {item_id} not found.", style="bold red")


@app.command()
def search(keyword: str = typer.Argument(..., help="Keyword to search for in title or description")) -> None:
    """Search for TODO items by keyword."""
    db_path = get_db_path()
    results = search_todos(db_path, keyword)
    _print_todos(results)


@app.command()
def edit(
    item_id: int = typer.Argument(..., help="ID of the task to edit"),
    title: Optional[str] = typer.Option(None, help="New title"),
    description: Optional[str] = typer.Option(None, help="New description"),
    priority: Optional[Priority] = typer.Option(None, help="New priority"),
    due_date: Optional[datetime] = typer.Option(None, help="New due date (YYYY-MM-DD HH:MM:SS)"),
) -> None:
    """Edit an existing TODO item."""
    db_path = get_db_path()
    todos = load_todos(db_path)

    for idx, todo in enumerate(todos):
        if todo.id == item_id:
            # Gather explicit updates avoiding explicit Nones unless intended
            provided: dict[str, Any] = {}
            if title is not None:
                provided["title"] = title
            if description is not None:
                provided["description"] = description
            if priority is not None:
                provided["priority"] = priority
            if due_date is not None:
                provided["due_date"] = due_date

            if not provided:
                console.print("No changes provided.", style="bold yellow")
                return

            # Create a new update model instance and dump using exclude_unset=True
            update_model = TodoItemUpdate(**provided)
            updates = update_model.model_dump(exclude_unset=True)

            # Merge existing data and updates
            current_data = todo.model_dump()
            current_data.update(updates)

            # Validate and apply updates
            try:
                updated_todo = TodoItem.model_validate(current_data)
                todos[idx] = updated_todo
                save_todos(db_path, todos)
                console.print(f"Task {item_id} updated.", style="bold green")
            except Exception as e:
                console.print(f"Error updating task: {e}", style="bold red")
            return

    console.print(f"Task {item_id} not found.", style="bold red")


if __name__ == "__main__":
    app()
