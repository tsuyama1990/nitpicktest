import os
import json
import pytest
from src.domain_models.todo import TodoItem, Priority, Status
from src.todo.storage import load_todos, save_todos

@pytest.fixture
def temp_storage(tmp_path):
    return os.path.join(tmp_path, "todos.json")

def test_load_empty_storage(temp_storage):
    todos = load_todos(temp_storage)
    assert todos == []

def test_save_and_load_todos(temp_storage):
    todos = [
        TodoItem(id=1, title="Task 1"),
        TodoItem(id=2, title="Task 2", priority=Priority.HIGH, status=Status.COMPLETED)
    ]
    save_todos(temp_storage, todos)

    loaded_todos = load_todos(temp_storage)
    assert len(loaded_todos) == 2
    assert loaded_todos[0].id == 1
    assert loaded_todos[0].title == "Task 1"
    assert loaded_todos[1].id == 2
    assert loaded_todos[1].status == Status.COMPLETED

def test_load_malformed_json(temp_storage):
    with open(temp_storage, "w") as f:
        f.write("{ invalid json }")

    with pytest.raises(ValueError, match="Malformed JSON"):
        load_todos(temp_storage)

def test_load_invalid_data(temp_storage):
    with open(temp_storage, "w") as f:
        json.dump([{"id": "not an int", "title": "Missing fields"}], f)

    with pytest.raises(ValueError, match="Invalid data format"):
        load_todos(temp_storage)
