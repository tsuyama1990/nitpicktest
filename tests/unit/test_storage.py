import pytest
from pathlib import Path
from domain_models import TodoItem, Priority, Status
from todo.storage import load_todos, save_todos, search_todos, filter_todos, sort_todos

@pytest.fixture
def temp_todo_file(tmp_path: Path) -> str:
    return str(tmp_path / "todos.json")

def test_save_and_load_todos(temp_todo_file: str) -> None:
    todos = [
        TodoItem(id=1, title="Task 1"),
        TodoItem(id=2, title="Task 2", priority=Priority.HIGH)
    ]
    save_todos(temp_todo_file, todos)

    loaded = load_todos(temp_todo_file)
    assert len(loaded) == 2
    assert loaded[0].id == 1
    assert loaded[1].priority == Priority.HIGH

def test_load_todos_empty_file(temp_todo_file: str) -> None:
    loaded = load_todos(temp_todo_file)
    assert loaded == []

def test_search_todos(temp_todo_file: str) -> None:
    todos = [
        TodoItem(id=1, title="Buy milk"),
        TodoItem(id=2, title="Walk the dog", description="Take dog to the park"),
        TodoItem(id=3, title="Buy eggs")
    ]
    save_todos(temp_todo_file, todos)

    results = search_todos(temp_todo_file, "milk")
    assert len(results) == 1
    assert results[0].id == 1

    results = search_todos(temp_todo_file, "dog")
    assert len(results) == 1
    assert results[0].id == 2

    results = search_todos(temp_todo_file, "buy")
    assert len(results) == 2

def test_filter_todos(temp_todo_file: str) -> None:
    todos = [
        TodoItem(id=1, title="Task 1", status=Status.PENDING, priority=Priority.LOW),
        TodoItem(id=2, title="Task 2", status=Status.COMPLETED, priority=Priority.HIGH),
        TodoItem(id=3, title="Task 3", status=Status.PENDING, priority=Priority.HIGH)
    ]
    save_todos(temp_todo_file, todos)

    results = filter_todos(temp_todo_file, status=Status.COMPLETED)
    assert len(results) == 1
    assert results[0].id == 2

    results = filter_todos(temp_todo_file, priority=Priority.HIGH)
    assert len(results) == 2

    results = filter_todos(temp_todo_file, status=Status.PENDING, priority=Priority.HIGH)
    assert len(results) == 1
    assert results[0].id == 3

def test_sort_todos() -> None:
    todos = [
        TodoItem(id=1, title="Task 1", priority=Priority.LOW),
        TodoItem(id=2, title="Task 2", priority=Priority.HIGH),
        TodoItem(id=3, title="Task 3", priority=Priority.MEDIUM)
    ]

    results = sort_todos(todos, "priority")
    assert results[0].priority == Priority.HIGH
    assert results[1].priority == Priority.MEDIUM
    assert results[2].priority == Priority.LOW

    # Sort by ID (default or fallback)
    results_id = sort_todos(todos, "id")
    assert results_id[0].id == 1
    assert results_id[2].id == 3
