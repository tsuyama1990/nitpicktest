import pytest
from typer.testing import CliRunner
from todo.cli import app
from todo.storage import load_todos

runner = CliRunner()


@pytest.fixture
def mock_storage_path(tmp_path, monkeypatch):
    storage_file = tmp_path / "test_todos.json"
    monkeypatch.setenv("STORAGE_PATH", str(storage_file))
    return str(storage_file)


def test_cli_add(mock_storage_path):
    result = runner.invoke(app, ["add", "Buy groceries", "--priority", "high"])
    assert result.exit_code == 0
    assert "Added task" in result.output

    todos = load_todos(mock_storage_path)
    assert len(todos) == 1
    assert todos[0].title == "Buy groceries"
    assert todos[0].priority.value == "high"


def test_cli_list(mock_storage_path):
    runner.invoke(app, ["add", "Task 1"])
    runner.invoke(app, ["add", "Task 2"])

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Task 1" in result.output
    assert "Task 2" in result.output


def test_cli_complete(mock_storage_path):
    runner.invoke(app, ["add", "Task to complete"])

    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0
    assert "Completed task 1" in result.output

    todos = load_todos(mock_storage_path)
    assert todos[0].status.value == "completed"


def test_cli_delete(mock_storage_path):
    runner.invoke(app, ["add", "Task to delete"])

    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
    assert "Deleted task 1" in result.output

    todos = load_todos(mock_storage_path)
    assert len(todos) == 0
