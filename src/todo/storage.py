import json
import os
from pydantic import TypeAdapter, ValidationError
from src.domain_models.todo import TodoItem

def load_todos(filepath: str) -> list[TodoItem]:
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        adapter = TypeAdapter(list[TodoItem])
        return adapter.validate_python(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON in {filepath}: {e}")
    except ValidationError as e:
        raise ValueError(f"Invalid data format in {filepath}: {e}")

def save_todos(filepath: str, todos: list[TodoItem]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    adapter = TypeAdapter(list[TodoItem])
    data = adapter.dump_python(todos, mode="json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
