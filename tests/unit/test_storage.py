from domain_models import TodoItem
from todo.storage import load_todos, save_todos


def test_save_and_load_todos(tmp_path):
    filepath = tmp_path / "todos.json"

    todos = [TodoItem(id=1, title="Task 1"), TodoItem(id=2, title="Task 2")]

    save_todos(str(filepath), todos)
    assert filepath.exists()

    loaded_todos = load_todos(str(filepath))
    assert len(loaded_todos) == 2
    assert loaded_todos[0].id == 1
    assert loaded_todos[1].title == "Task 2"


def test_load_todos_nonexistent_file(tmp_path):
    filepath = tmp_path / "does_not_exist.json"
    loaded_todos = load_todos(str(filepath))
    assert loaded_todos == []


def test_load_todos_corrupted_file(tmp_path):
    filepath = tmp_path / "corrupted.json"
    filepath.write_text("invalid json {")
    loaded_todos = load_todos(str(filepath))
    assert loaded_todos == []
