import os
from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from src.domain_models.todo import Priority, Status, TodoItem
from src.todo.storage import load_todos, save_todos

app = typer.Typer(help="A simple CLI TODO application")
console = Console()

def get_storage_file() -> str:
    return os.environ.get("TODO_STORAGE_FILE", "todos.json")


def _get_next_id(todos: list[TodoItem]) -> int:
    if not todos:
        return 1
    return max(todo.id for todo in todos) + 1


@app.command()
def add(
    title: str = typer.Argument(..., help="The title of the task"),
    description: Optional[str] = typer.Option(None, help="A description of the task"),
    priority: Priority = typer.Option(Priority.MEDIUM, help="The priority of the task"),
    due_date: Optional[datetime] = typer.Option(
        None, help="The due date (YYYY-MM-DD HH:MM:SS)"
    ),
) -> None:
    """Add a new TODO item."""
    storage_file = get_storage_file()
    try:
        todos = load_todos(storage_file)
    except ValueError as e:
        console.print(f"[red]Error loading storage:[/red] {e}")
        raise typer.Exit(1)

    new_id = _get_next_id(todos)
    todo = TodoItem(
        id=new_id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
    )
    todos.append(todo)

    try:
        save_todos(storage_file, todos)
        console.print(f"[green]Added TODO '{title}' with ID {new_id}.[/green]")
    except Exception as e:
        console.print(f"[red]Error saving storage:[/red] {e}")
        raise typer.Exit(1)


@app.command(name="list")
def list_todos() -> None:
    """List all TODO items."""
    storage_file = get_storage_file()
    try:
        todos = load_todos(storage_file)
    except ValueError as e:
        console.print(f"[red]Error loading storage:[/red] {e}")
        raise typer.Exit(1)

    if not todos:
        console.print("[yellow]No TODO items found.[/yellow]")
        return

    table = Table(title="TODO Items")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Priority", style="yellow")
    table.add_column("Due Date", style="blue")

    for todo in todos:
        status_str = (
            f"[strike]{todo.status.value}[/strike]"
            if todo.status == Status.COMPLETED
            else todo.status.value
        )
        due_date_str = todo.due_date.strftime("%Y-%m-%d %H:%M") if todo.due_date else ""
        table.add_row(
            str(todo.id), todo.title, status_str, todo.priority.value, due_date_str
        )

    console.print(table)


@app.command()
def complete(
    item_id: int = typer.Argument(..., help="The ID of the task to complete"),
) -> None:
    """Mark a TODO item as completed."""
    storage_file = get_storage_file()
    try:
        todos = load_todos(storage_file)
    except ValueError as e:
        console.print(f"[red]Error loading storage:[/red] {e}")
        raise typer.Exit(1)

    for todo in todos:
        if todo.id == item_id:
            if todo.status == Status.COMPLETED:
                console.print(f"[yellow]TODO {item_id} is already completed.[/yellow]")
                return
            todo.status = Status.COMPLETED
            save_todos(storage_file, todos)
            console.print(f"[green]Marked TODO {item_id} as completed.[/green]")
            return

    console.print(f"[red]TODO {item_id} not found.[/red]")
    raise typer.Exit(1)


@app.command()
def delete(
    item_id: int = typer.Argument(..., help="The ID of the task to delete"),
) -> None:
    """Delete a TODO item."""
    storage_file = get_storage_file()
    try:
        todos = load_todos(storage_file)
    except ValueError as e:
        console.print(f"[red]Error loading storage:[/red] {e}")
        raise typer.Exit(1)

    for i, todo in enumerate(todos):
        if todo.id == item_id:
            todos.pop(i)
            save_todos(storage_file, todos)
            console.print(f"[green]Deleted TODO {item_id}.[/green]")
            return

    console.print(f"[red]TODO {item_id} not found.[/red]")
    raise typer.Exit(1)


if __name__ == "__main__":
    app()
