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
