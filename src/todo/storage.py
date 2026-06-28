import json
from pathlib import Path
from domain_models import TodoItem


def load_todos(filepath: str) -> list[TodoItem]:
    path = Path(filepath)
    if not path.exists():
        return []

    try:
        content = path.read_text()
        data = json.loads(content)
        if not isinstance(data, list):
            return []

        return [TodoItem.model_validate(item) for item in data]
    except (json.JSONDecodeError, Exception):
        return []


def save_todos(filepath: str, todos: list[TodoItem]) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = [todo.model_dump(mode="json") for todo in todos]
    path.write_text(json.dumps(data, indent=2))
