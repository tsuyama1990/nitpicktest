import json
import os
from pathlib import Path
from typing import Optional, List

from src.domain_models.todo import TodoItem


def load_todos(filepath: str) -> List[TodoItem]:
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return [TodoItem.model_validate(item) for item in data]
    except (json.JSONDecodeError, ValueError):
        # In a real app we might want to log this or raise a specific error
        # but for now we'll return an empty list or raise ValueError
        return []


def save_todos(filepath: str, todos: List[TodoItem]) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w") as f:
        json.dump([todo.model_dump(mode="json") for todo in todos], f, indent=2)


def search_todos(filepath: str, keyword: str) -> List[TodoItem]:
    todos = load_todos(filepath)
    keyword = keyword.lower()
    results = []
    for todo in todos:
        if keyword in todo.title.lower():
            results.append(todo)
        elif todo.description and keyword in todo.description.lower():
            results.append(todo)
    return results


def filter_todos(
    filepath: str, status: Optional[str] = None, priority: Optional[str] = None
) -> List[TodoItem]:
    todos = load_todos(filepath)
    results = []
    for todo in todos:
        if status and todo.status != status:
            continue
        if priority and todo.priority != priority:
            continue
        results.append(todo)
    return results


def sort_todos(todos: List[TodoItem], sort_by: str) -> List[TodoItem]:
    if sort_by == "priority":
        # HIGH < MEDIUM < LOW
        priority_order = {"high": 1, "medium": 2, "low": 3}
        return sorted(todos, key=lambda t: priority_order.get(t.priority.value, 4))
    elif sort_by == "due_date":
        return sorted(todos, key=lambda t: (t.due_date is None, t.due_date))
    return todos
