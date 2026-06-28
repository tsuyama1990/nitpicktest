import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
from datetime import datetime
import os

from domain_models import TodoItem, Priority, Status, config
from todo.storage import load_todos, save_todos

app = typer.Typer(help="Manage your TODOs")
console = Console()


def _get_storage_path() -> str:
    # Use environment variable if set (for testing), otherwise config default
    return os.environ.get("STORAGE_PATH", config.storage_path)


@app.command()
def add(
    title: str = typer.Argument(..., help="Title of the task"),
    description: Annotated[
        str, typer.Option("--desc", help="Description of the task")
    ] = "",
    priority: Annotated[
        Priority, typer.Option("--priority", help="Priority of the task")
    ] = Priority.MEDIUM,
    due_date: Annotated[
        datetime | None, typer.Option("--due", help="Due date for the task")
    ] = None,
) -> None:
    """Add a new TODO item."""
    path = _get_storage_path()
    todos = load_todos(path)

    new_id = 1
    if todos:
        new_id = max(todo.id for todo in todos) + 1

    new_todo = TodoItem(
        id=new_id,
        title=title,
        description=description if description else None,
        priority=priority,
        due_date=due_date,
    )

    todos.append(new_todo)
    save_todos(path, todos)
    console.print(f"[green]Added task '{title}' with ID {new_id}[/green]")


@app.command()
def list() -> None:
    """List all TODO items."""
    path = _get_storage_path()
    todos = load_todos(path)

    if not todos:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title")
    table.add_column("Priority")
    table.add_column("Status")

    for todo in todos:
        status_color = "green" if todo.status == Status.COMPLETED else "yellow"
        table.add_row(
            str(todo.id),
            todo.title,
            todo.priority.value,
            f"[{status_color}]{todo.status.value}[/{status_color}]",
        )

    console.print(table)


@app.command()
def complete(
    item_id: int = typer.Argument(..., help="ID of the task to complete"),
) -> None:
    """Mark a TODO item as completed."""
    path = _get_storage_path()
    todos = load_todos(path)

    found = False
    for todo in todos:
        if todo.id == item_id:
            todo.status = Status.COMPLETED
            found = True
            break

    if not found:
        console.print(f"[red]Task {item_id} not found.[/red]")
        raise typer.Exit(code=1)

    save_todos(path, todos)
    console.print(f"[green]Completed task {item_id}[/green]")


@app.command()
def delete(item_id: int = typer.Argument(..., help="ID of the task to delete")) -> None:
    """Delete a TODO item."""
    path = _get_storage_path()
    todos = load_todos(path)

    initial_count = len(todos)
    todos = [todo for todo in todos if todo.id != item_id]

    if len(todos) == initial_count:
        console.print(f"[red]Task {item_id} not found.[/red]")
        raise typer.Exit(code=1)

    save_todos(path, todos)
    console.print(f"[green]Deleted task {item_id}[/green]")


if __name__ == "__main__":
    app()
