import os
import pytest
from typer.testing import CliRunner
from src.todo.cli import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def setup_storage(tmp_path, monkeypatch):
    storage_path = os.path.join(tmp_path, "todos.json")
    monkeypatch.setenv("TODO_STORAGE_FILE", storage_path)
    yield storage_path


def test_add_todo():
    result = runner.invoke(app, ["add", "Test task", "--priority", "high"])
    assert result.exit_code == 0
    assert "Added TODO 'Test task' with ID 1" in result.output


def test_list_empty():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "No TODO items found" in result.output


def test_list_todos():
    runner.invoke(app, ["add", "Task 1"])
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Task 1" in result.output
    assert "pending" in result.output


def test_complete_todo():
    runner.invoke(app, ["add", "Task 1"])
    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0
    assert "Marked TODO 1 as completed" in result.output


def test_delete_todo():
    runner.invoke(app, ["add", "Task 1"])
    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
    assert "Deleted TODO 1" in result.output

    list_result = runner.invoke(app, ["list"])
    assert "No TODO items found" in list_result.output
