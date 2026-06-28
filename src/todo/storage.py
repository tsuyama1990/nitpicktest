import json
import os
from pathlib import Path
from typing import List

from src.domain_models.todo import TodoItem


def load_todos(filepath: str) -> List[TodoItem]:
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return [TodoItem.model_validate(item) for item in data]
    except (json.JSONDecodeError, ValueError):
        return []


def save_todos(filepath: str, todos: List[TodoItem]) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w") as f:
        json.dump([todo.model_dump(mode="json") for todo in todos], f, indent=2)
