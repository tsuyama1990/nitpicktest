import json
from typer.testing import CliRunner
from src.todo.cli import app
import pytest

runner = CliRunner()

@pytest.fixture
def clean_env(tmp_path, monkeypatch):
    db_path = str(tmp_path / "todos_uat.json")
    monkeypatch.setenv("TODO_DB_PATH", db_path)
    return db_path

def test_uat_01_01_add_todo(clean_env):
    # Given the TODO storage is empty
    # When I run the CLI command to add a task with title "Buy groceries" and priority "high"
    result = runner.invoke(app, ["add", "Buy groceries", "--priority", "high"])
    assert result.exit_code == 0

    # Then the task "Buy groceries" should be saved in the system
    # And its status should be "pending"
    # And its priority should be "high"
    with open(clean_env) as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["title"] == "Buy groceries"
        assert data[0]["status"] == "pending"
        assert data[0]["priority"] == "high"

def test_uat_01_02_list_todos(clean_env):
    # Given there are tasks "Task A" and "Task B" in the system
    runner.invoke(app, ["add", "Task A"])
    runner.invoke(app, ["add", "Task B"])

    # When I run the CLI command to list tasks
    result = runner.invoke(app, ["list"])

    # Then I should see both "Task A" and "Task B" in the output
    assert result.exit_code == 0
    assert "Task A" in result.output
    assert "Task B" in result.output

def test_uat_01_03_mark_todo_complete(clean_env):
    # Given there is a pending task with ID 1
    runner.invoke(app, ["add", "My Task"])

    # When I run the CLI command to complete task 1
    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0

    # Then the status of task 1 should be changed to "completed"
    with open(clean_env) as f:
        data = json.load(f)
        assert data[0]["status"] == "completed"

def test_uat_01_04_delete_todo(clean_env):
    # Given there is a task with ID 1
    runner.invoke(app, ["add", "My Task to Delete"])

    # When I run the CLI command to delete task 1
    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0

    # Then task 1 should no longer exist in the system
    with open(clean_env) as f:
        data = json.load(f)
        assert len(data) == 0
