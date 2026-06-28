import os
from pathlib import Path
from dev_src.todo.storage import load_todos, save_todos
from dev_src.todo.storage import search_todos, filter_todos, sort_todos
from datetime import datetime
from dev_src.domain_models.todo import TodoItem, Priority, Status


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


def test_search_todos(tmp_path: Path) -> None:
    filepath = str(tmp_path / "todos.json")
    todos = [
        TodoItem(id=1, title="Buy milk", priority=Priority.HIGH, status=Status.PENDING),
        TodoItem(
            id=2,
            title="Walk the dog",
            priority=Priority.LOW,
            status=Status.COMPLETED,
            description="Get some milk for the dog",
        ),
        TodoItem(id=3, title="Read book", priority=Priority.MEDIUM, status=Status.PENDING),
    ]
    save_todos(filepath, todos)

    results = search_todos(filepath, "milk")
    assert len(results) == 2
    assert results[0].id == 1
    assert results[1].id == 2

    results_empty = search_todos(filepath, "apple")
    assert len(results_empty) == 0


def test_filter_todos(tmp_path: Path) -> None:
    filepath = str(tmp_path / "todos.json")
    todos = [
        TodoItem(id=1, title="Buy milk", priority=Priority.HIGH, status=Status.PENDING),
        TodoItem(id=2, title="Walk the dog", priority=Priority.LOW, status=Status.COMPLETED),
        TodoItem(id=3, title="Read book", priority=Priority.HIGH, status=Status.COMPLETED),
    ]
    save_todos(filepath, todos)

    # Filter by status
    completed = filter_todos(filepath, status=Status.COMPLETED)
    assert len(completed) == 2
    assert completed[0].id == 2
    assert completed[1].id == 3

    # Filter by priority
    high = filter_todos(filepath, priority=Priority.HIGH)
    assert len(high) == 2
    assert high[0].id == 1
    assert high[1].id == 3

    # Filter by both
    high_completed = filter_todos(filepath, status=Status.COMPLETED, priority=Priority.HIGH)
    assert len(high_completed) == 1
    assert high_completed[0].id == 3


def test_sort_todos() -> None:
    todos = [
        TodoItem(id=1, title="Task A", priority=Priority.LOW, due_date=datetime(2026, 12, 1)),
        TodoItem(id=2, title="Task B", priority=Priority.HIGH, due_date=datetime(2026, 10, 1)),
        TodoItem(id=3, title="Task C", priority=Priority.MEDIUM, due_date=datetime(2026, 11, 1)),
        TodoItem(id=4, title="Task D", priority=Priority.LOW, due_date=None),
    ]

    # Sort by priority
    sorted_priority = sort_todos(todos, "priority")
    assert sorted_priority[0].id == 2  # HIGH
    assert sorted_priority[1].id == 3  # MEDIUM
    assert sorted_priority[2].id == 1  # LOW
    assert sorted_priority[3].id == 4  # LOW

    # Sort by due_date
    sorted_due = sort_todos(todos, "due_date")
    assert sorted_due[0].id == 2  # Oct
    assert sorted_due[1].id == 3  # Nov
    assert sorted_due[2].id == 1  # Dec
    assert sorted_due[3].id == 4  # None (end)
