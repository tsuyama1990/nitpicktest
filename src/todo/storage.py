import json
import os
from domain_models import TodoItem, Priority, Status


def load_todos(filepath: str) -> list[TodoItem]:
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return [TodoItem.model_validate(item) for item in data]
    except (json.JSONDecodeError, IOError):
        return []


def save_todos(filepath: str, todos: list[TodoItem]) -> None:
    with open(filepath, "w") as f:
        data = [item.model_dump(mode="json") for item in todos]
        json.dump(data, f, indent=4)


def search_todos(filepath: str, keyword: str) -> list[TodoItem]:
    todos = load_todos(filepath)
    keyword_lower = keyword.lower()
    results = []
    for todo in todos:
        title_match = keyword_lower in todo.title.lower()
        desc_match = todo.description and keyword_lower in todo.description.lower()
        if title_match or desc_match:
            results.append(todo)
    return results


def filter_todos(filepath: str, status: Status | None = None, priority: Priority | None = None) -> list[TodoItem]:
    todos = load_todos(filepath)
    results = []
    for todo in todos:
        if status and todo.status != status:
            continue
        if priority and todo.priority != priority:
            continue
        results.append(todo)
    return results


def sort_todos(todos: list[TodoItem], sort_by: str) -> list[TodoItem]:
    if sort_by == "priority":
        # Sort logic for priority: HIGH > MEDIUM > LOW
        priority_order = {Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
        return sorted(todos, key=lambda x: priority_order.get(x.priority, 99))
    elif sort_by == "due_date":
        return sorted(todos, key=lambda x: x.due_date if x.due_date else "9999-12-31")
    else:
        # Fallback to ID or original order
        return sorted(todos, key=lambda x: x.id)
