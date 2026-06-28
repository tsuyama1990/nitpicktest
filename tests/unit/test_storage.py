import os
from pathlib import Path
from src.todo.storage import load_todos, save_todos
from src.domain_models.todo import TodoItem, Priority, Status


def test_save_and_load_todos(tmp_path: Path) -> None:
    filepath = str(tmp_path / "todos.json")

    todos = [
        TodoItem(id=1, title="Task 1", priority=Priority.HIGH, status=Status.PENDING),
        TodoItem(id=2, title="Task 2", priority=Priority.LOW, status=Status.COMPLETED),
    ]

    save_todos(filepath, todos)

    assert os.path.exists(filepath)

    loaded = load_todos(filepath)
    assert len(loaded) == 2
    assert loaded[0].title == "Task 1"
    assert loaded[1].title == "Task 2"
    assert loaded[1].status == Status.COMPLETED


def test_load_nonexistent_file(tmp_path: Path) -> None:
    filepath = str(tmp_path / "nonexistent.json")
    loaded = load_todos(filepath)
    assert loaded == []


def test_load_invalid_json(tmp_path: Path) -> None:
    filepath = str(tmp_path / "invalid.json")
    with open(filepath, "w") as f:
        f.write("not json")

    loaded = load_todos(filepath)
    assert loaded == []
