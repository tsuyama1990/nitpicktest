import os
import json
import pytest
from src.domain_models import TodoItem, Priority, Status
from src.todo.storage import load_todos, save_todos

@pytest.fixture
def tmp_file(tmp_path):
    return str(tmp_path / "todos.json")

def test_save_and_load_todos(tmp_file):
    todos = [
        TodoItem(id=1, title="Task 1", priority=Priority.LOW),
        TodoItem(id=2, title="Task 2", status=Status.COMPLETED)
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
