import typer
from datetime import datetime
from typing import Optional, Any

from src.domain_models.todo import Priority, Status, TodoItem, TodoUpdate
from src.domain_models.config import settings
from src.todo.storage import load_todos, save_todos, filter_todos, search_todos, sort_todos

app = typer.Typer(help="TODO CLI Application")


@app.command()
def add(
    title: str = typer.Argument(..., help="The title of the task"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Description of the task"),
    priority: Priority = typer.Option(Priority.MEDIUM, "--priority", "-p", help="Task priority"),
    due_date: Optional[datetime] = typer.Option(None, "--due", "-D", help="Due date (YYYY-MM-DD)"),
) -> None:
    """Add a new TODO item."""
    todos = load_todos(settings.storage_file)

    new_id = 1 if not todos else max(t.id for t in todos) + 1

    new_todo = TodoItem(
        id=new_id, title=title, description=description, priority=priority, due_date=due_date
    )

    todos.append(new_todo)
    save_todos(settings.storage_file, todos)
    typer.echo(f"Added task: '{title}' with ID {new_id} and priority {priority.value}")


@app.command(name="list")
def list_todos(
    status: Optional[Status] = typer.Option(None, "--status", "-s", help="Filter by status"),
    priority: Optional[Priority] = typer.Option(
        None, "--priority", "-p", help="Filter by priority"
    ),
    sort_by: Optional[str] = typer.Option(
        None, "--sort-by", "-S", help="Sort by priority or due_date"
    ),
) -> None:
    """List all TODO items."""
    status_str = status.value if status else None
    priority_str = priority.value if priority else None
    todos = filter_todos(settings.storage_file, status=status_str, priority=priority_str)

    if sort_by:
        todos = sort_todos(todos, sort_by)

    if not todos:
        typer.echo("No tasks found.")
        return

    for todo in todos:
        desc = f" - {todo.description}" if todo.description else ""
        due = f" (Due: {todo.due_date.strftime('%Y-%m-%d')})" if todo.due_date else ""
        status_mark = "[x]" if todo.status == Status.COMPLETED else "[ ]"

        typer.echo(f"{todo.id}: {status_mark} {todo.title} [{todo.priority.value}]{desc}{due}")


@app.command()
def complete(item_id: int) -> None:
    """Mark a TODO item as complete."""
    todos = load_todos(settings.storage_file)

    found = False
    for todo in todos:
        if todo.id == item_id:
            todo.status = Status.COMPLETED
            found = True
            break

    if found:
        save_todos(settings.storage_file, todos)
        typer.echo(f"Marked task {item_id} as completed.")
    else:
        typer.echo(f"Task with ID {item_id} not found.", err=True)
        raise typer.Exit(code=1)


@app.command()
def delete(item_id: int) -> None:
    """Delete a TODO item."""
    todos = load_todos(settings.storage_file)

    initial_length = len(todos)
    todos = [t for t in todos if t.id != item_id]

    if len(todos) < initial_length:
        save_todos(settings.storage_file, todos)
        typer.echo(f"Deleted task {item_id}.")
    else:
        typer.echo(f"Task with ID {item_id} not found.", err=True)
        raise typer.Exit(code=1)


@app.command()
def search(keyword: str) -> None:
    """Search TODO items by keyword."""
    todos = search_todos(settings.storage_file, keyword)

    if not todos:
        typer.echo(f"No tasks found matching '{keyword}'.")
        return

    for todo in todos:
        desc = f" - {todo.description}" if todo.description else ""
        due = f" (Due: {todo.due_date.strftime('%Y-%m-%d')})" if todo.due_date else ""
        status_mark = "[x]" if todo.status == Status.COMPLETED else "[ ]"

        typer.echo(f"{todo.id}: {status_mark} {todo.title} [{todo.priority.value}]{desc}{due}")


@app.command()
def edit(
    item_id: int,
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New title"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="New description"),
    priority: Optional[Priority] = typer.Option(None, "--priority", "-p", help="New priority"),
    due_date: Optional[datetime] = typer.Option(None, "--due", "-D", help="New due date"),
) -> None:
    """Edit an existing TODO item."""
    todos = load_todos(settings.storage_file)

    found = False
    for i, todo in enumerate(todos):
        if todo.id == item_id:
            found = True

            # Avoid explicitly passing None to the model instantiation
            update_kwargs: dict[str, Any] = {}
            if title is not None:
                update_kwargs["title"] = title
            if description is not None:
                update_kwargs["description"] = description
            if priority is not None:
                update_kwargs["priority"] = priority
            if due_date is not None:
                update_kwargs["due_date"] = due_date

            if not update_kwargs:
                typer.echo("No fields to update.")
                return

            update_model = TodoUpdate(**update_kwargs)
            update_data = update_model.model_dump(exclude_unset=True)

            current_data = todo.model_dump()
            current_data.update(update_data)

            todos[i] = TodoItem.model_validate(current_data)
            break

    if found:
        save_todos(settings.storage_file, todos)
        typer.echo(f"Updated task {item_id}.")
    else:
        typer.echo(f"Task with ID {item_id} not found.", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
