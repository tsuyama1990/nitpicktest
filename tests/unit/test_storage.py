import os
import pytest
from src.domain_models import TodoItem, Priority, Status
from datetime import datetime
from src.todo.storage import (
    load_todos,
    save_todos,
    search_todos,
    filter_todos,
    sort_todos,
)


@pytest.fixture
def tmp_file(tmp_path):
    return str(tmp_path / "todos.json")


def test_save_and_load_todos(tmp_file):
    todos = [
        TodoItem(id=1, title="Task 1", priority=Priority.LOW),
        TodoItem(id=2, title="Task 2", status=Status.COMPLETED),
    ]
    save_todos(tmp_file, todos)

    assert os.path.exists(tmp_file)

    loaded = load_todos(tmp_file)
    assert len(loaded) == 2
    assert loaded[0].title == "Task 1"
    assert loaded[0].priority == Priority.LOW
    assert loaded[1].status == Status.COMPLETED


def test_load_nonexistent_file(tmp_file):
    # Should return an empty list or create the file
    loaded = load_todos(tmp_file)
    assert loaded == []


def test_load_corrupted_file(tmp_file):
    with open(tmp_file, "w") as f:
        f.write("{ invalid json")

    # Should probably handle it gracefully or raise a specific error
    # Let's say it returns an empty list or we can enforce raising ValueError
    with pytest.raises(ValueError):
        load_todos(tmp_file)


def test_search_todos(tmp_file):
    todos = [
        TodoItem(id=1, title="Buy milk"),
        TodoItem(id=2, title="Walk the dog", description="Take him to the park"),
        TodoItem(id=3, title="Do laundry"),
    ]
    save_todos(tmp_file, todos)

    results = search_todos(tmp_file, "milk")
    assert len(results) == 1
    assert results[0].id == 1

    results = search_todos(tmp_file, "PARK")
    assert len(results) == 1
    assert results[0].id == 2

    results = search_todos(tmp_file, "notFound")
    assert len(results) == 0


def test_filter_todos(tmp_file):
    todos = [
        TodoItem(id=1, title="A", status=Status.PENDING, priority=Priority.HIGH),
        TodoItem(id=2, title="B", status=Status.COMPLETED, priority=Priority.LOW),
        TodoItem(id=3, title="C", status=Status.PENDING, priority=Priority.MEDIUM),
    ]
    save_todos(tmp_file, todos)

    # Filter by status
    results = filter_todos(tmp_file, status=Status.PENDING)
    assert len(results) == 2

    # Filter by priority
    results = filter_todos(tmp_file, priority=Priority.LOW)
    assert len(results) == 1
    assert results[0].id == 2

    # Filter by both
    results = filter_todos(tmp_file, status=Status.PENDING, priority=Priority.HIGH)
    assert len(results) == 1
    assert results[0].id == 1


def test_sort_todos():
    todos = [
        TodoItem(
            id=1, title="A", priority=Priority.LOW, due_date=datetime(2025, 1, 10)
        ),
        TodoItem(
            id=2, title="B", priority=Priority.HIGH, due_date=datetime(2025, 1, 1)
        ),
        TodoItem(
            id=3, title="C", priority=Priority.MEDIUM, due_date=datetime(2025, 1, 5)
        ),
    ]

    # Sort by priority (HIGH -> MEDIUM -> LOW)
    sorted_by_priority = sort_todos(todos, "priority")
    assert sorted_by_priority[0].id == 2
    assert sorted_by_priority[1].id == 3
    assert sorted_by_priority[2].id == 1

    # Sort by due_date
    sorted_by_date = sort_todos(todos, "due_date")
    assert sorted_by_date[0].id == 2
    assert sorted_by_date[1].id == 3
    assert sorted_by_date[2].id == 1

    # Ensure items with no due_date sort nicely
    todos.append(TodoItem(id=4, title="D", priority=Priority.LOW, due_date=None))
    sorted_by_date = sort_todos(todos, "due_date")
    # Item 4 should be last
    assert sorted_by_date[-1].id == 4

    # Invalid sort key
    with pytest.raises(ValueError):
        sort_todos(todos, "invalid")
