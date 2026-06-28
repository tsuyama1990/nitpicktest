import os
import pytest
from typer.testing import CliRunner
from src.todo.cli import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def setup_storage(tmp_path, monkeypatch):
    storage_path = os.path.join(tmp_path, "todos_uat.json")
    monkeypatch.setenv("TODO_STORAGE_FILE", storage_path)
    yield storage_path


def test_uat_01_01_add_new_todo():
    """UAT_01_01: Add a new TODO item with title and priority."""
    result = runner.invoke(app, ["add", "Buy groceries", "--priority", "high"])
    assert result.exit_code == 0
    assert "Added TODO 'Buy groceries'" in result.output

    list_result = runner.invoke(app, ["list"])
    assert "Buy groceries" in list_result.output
    assert "pending" in list_result.output
    assert "high" in list_result.output


def test_uat_01_02_list_all_todos():
    """UAT_01_02: List all TODO items."""
    runner.invoke(app, ["add", "Task A"])
    runner.invoke(app, ["add", "Task B"])

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Task A" in result.output
    assert "Task B" in result.output


def test_uat_01_03_mark_todo_as_complete():
    """UAT_01_03: Mark a pending TODO item as completed."""
    runner.invoke(app, ["add", "Finish homework"])

    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0
    assert "Marked TODO 1 as completed" in result.output

    list_result = runner.invoke(app, ["list"])
    assert "completed" in list_result.output


def test_uat_01_04_delete_todo_item():
    """UAT_01_04: Delete an existing TODO item."""
    runner.invoke(app, ["add", "Task to delete"])

    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
    assert "Deleted TODO 1" in result.output

    list_result = runner.invoke(app, ["list"])
    assert "Task to delete" not in list_result.output
    assert "No TODO items found" in list_result.output
