import os
import typer
from typing import Optional
from datetime import datetime
from src.domain_models import TodoItem, Priority, Status, TodoUpdate
from src.todo.storage import (
    load_todos,
    save_todos,
    search_todos,
    filter_todos,
    sort_todos,
)

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
def list(
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    sort_by: Optional[str] = None,
):
    db_path = get_db_path()

    # Apply filters
    todos = filter_todos(
        db_path,
        status=status.value if status else None,
        priority=priority.value if priority else None,
    )

    if not todos:
        typer.echo("No tasks found.")
        return

    # Apply sorting
    if sort_by:
        try:
            todos = sort_todos(todos, sort_by)
        except ValueError as e:
            typer.echo(f"Error: {e}")
            raise typer.Exit(code=1)

    for todo in todos:
        status_char = "✓" if todo.status == Status.COMPLETED else " "
        typer.echo(f"[{status_char}] {todo.id}: {todo.title} ({todo.priority})")


@app.command()
def search(keyword: str):
    db_path = get_db_path()
    todos = search_todos(db_path, keyword)

    if not todos:
        typer.echo(f"No tasks found matching '{keyword}'.")
        return

    for todo in todos:
        status_char = "✓" if todo.status == Status.COMPLETED else " "
        typer.echo(f"[{status_char}] {todo.id}: {todo.title} ({todo.priority})")


@app.command()
def edit(
    item_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[Priority] = None,
    due_date: Optional[datetime] = None,
):
    db_path = get_db_path()
    todos = load_todos(db_path)

    # Try to build update model to leverage Pydantic validation
    try:
        update_data = TodoUpdate(
            title=title, description=description, priority=priority, due_date=due_date
        )
    except Exception as e:
        typer.echo(f"Validation error: {e}")
        raise typer.Exit(code=1)

    found_idx = -1
    for i, todo in enumerate(todos):
        if todo.id == item_id:
            found_idx = i
            break

    if found_idx == -1:
        typer.echo(f"Task {item_id} not found.")
        return

    # Get original item and updated fields (exclude unset prevents overriding with None)
    old_item = todos[found_idx]
    updates = update_data.model_dump(exclude_unset=True)

    # To fully comply with Pydantic V2 partial updates logic specified:
    # "use model_dump(exclude_unset=True) to extract explicitly provided fields"
    # we need a way to filter out the defaults Typer gives us (which are None).
    # Since Typer doesn't have an "unset" concept like Pydantic, we will map
    # the explicitly not-None fields to an update dict and apply it.

    # We can rely on `updates` if we only pass kwargs that are not None to TodoUpdate

    update_kwargs: dict = {}
    if title is not None:
        update_kwargs["title"] = title
    if description is not None:
        update_kwargs["description"] = description
    if priority is not None:
        update_kwargs["priority"] = priority
    if due_date is not None:
        update_kwargs["due_date"] = due_date

    update_model = TodoUpdate(**update_kwargs)
    updates = update_model.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(old_item, key, value)

    save_todos(db_path, todos)
    typer.echo(f"Edited task {item_id}.")


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
