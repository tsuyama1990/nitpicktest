import json
import os
from typing import List
from src.domain_models import TodoItem


def load_todos(filepath: str) -> List[TodoItem]:
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return [TodoItem(**item) for item in data]
    except json.JSONDecodeError as e:
        raise ValueError(f"Corrupted file: {e}")


def save_todos(filepath: str, todos: List[TodoItem]) -> None:
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w") as f:
        json.dump([todo.model_dump(mode="json") for todo in todos], f, indent=4)


def search_todos(filepath: str, keyword: str) -> List[TodoItem]:
    todos = load_todos(filepath)
    keyword = keyword.lower()
    return [
        t
        for t in todos
        if keyword in t.title.lower()
        or (t.description and keyword in t.description.lower())
    ]


def filter_todos(
    filepath: str, status: str | None = None, priority: str | None = None
) -> List[TodoItem]:
    todos = load_todos(filepath)

    if status:
        todos = [t for t in todos if t.status.value == status.lower()]

    if priority:
        todos = [t for t in todos if t.priority.value == priority.lower()]

    return todos


def sort_todos(todos: List[TodoItem], sort_by: str) -> List[TodoItem]:
    if sort_by == "priority":
        # Sort HIGH -> MEDIUM -> LOW
        priority_map = {"high": 1, "medium": 2, "low": 3}
        return sorted(todos, key=lambda t: priority_map.get(t.priority.value, 4))

    elif sort_by == "due_date":
        # Use a very late date for None to place them at the end
        from datetime import datetime

        max_date = datetime.max
        # Ignore timezone info for sorting if any
        return sorted(
            todos,
            key=lambda t: t.due_date.replace(tzinfo=None) if t.due_date else max_date,
        )

    raise ValueError(f"Invalid sort key: {sort_by}")
