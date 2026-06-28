import os
import typer
from typing import Optional
from datetime import datetime
from src.domain_models import TodoItem, Priority, Status
from src.todo.storage import load_todos, save_todos

app = typer.Typer()


def get_db_path() -> str:
    return os.environ.get("TODO_DB_PATH", "todos.json")


@app.command()
def add(
    title: str,
    description: Optional[str] = None,
    priority: Priority = Priority.MEDIUM,
    due_date: Optional[datetime] = None,
):
    db_path = get_db_path()
    todos = load_todos(db_path)

    new_id = 1
    if todos:
        new_id = max(todo.id for todo in todos) + 1

    new_todo = TodoItem(
        id=new_id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
    )

    todos.append(new_todo)
    save_todos(db_path, todos)
    typer.echo(f"Added task: {title} (ID: {new_id})")


@app.command()
def list():
    db_path = get_db_path()
    todos = load_todos(db_path)

    if not todos:
        typer.echo("No tasks found.")
        return

    for todo in todos:
        status = "✓" if todo.status == Status.COMPLETED else " "
        typer.echo(f"[{status}] {todo.id}: {todo.title} ({todo.priority})")


@app.command()
def complete(item_id: int):
    db_path = get_db_path()
    todos = load_todos(db_path)

    for todo in todos:
        if todo.id == item_id:
            todo.status = Status.COMPLETED
            save_todos(db_path, todos)
            typer.echo(f"Marked task {item_id} as completed.")
            return

    typer.echo(f"Task {item_id} not found.")


@app.command()
def delete(item_id: int):
    db_path = get_db_path()
    todos = load_todos(db_path)

    initial_length = len(todos)
    todos = [t for t in todos if t.id != item_id]

    if len(todos) < initial_length:
        save_todos(db_path, todos)
        typer.echo(f"Deleted task {item_id}.")
    else:
        typer.echo(f"Task {item_id} not found.")
