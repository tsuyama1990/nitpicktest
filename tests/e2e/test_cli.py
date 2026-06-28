import json
from typer.testing import CliRunner
from src.todo.cli import app
import pytest

runner = CliRunner()


@pytest.fixture
def clean_env(tmp_path, monkeypatch):
    db_path = str(tmp_path / "todos.json")
    monkeypatch.setenv("TODO_DB_PATH", db_path)
    return db_path


def test_cli_add(clean_env):
    result = runner.invoke(app, ["add", "New Task", "--priority", "high"])
    assert result.exit_code == 0
    assert "Added" in result.output

    with open(clean_env) as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["title"] == "New Task"
        assert data[0]["priority"] == "high"


def test_cli_list(clean_env):
    runner.invoke(app, ["add", "Task 1"])
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Task 1" in result.output


def test_cli_complete(clean_env):
    runner.invoke(app, ["add", "Task 1"])
    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0
    assert "completed" in result.output.lower() or "marked" in result.output.lower()

    with open(clean_env) as f:
        data = json.load(f)
        assert data[0]["status"] == "completed"


def test_cli_delete(clean_env):
    runner.invoke(app, ["add", "Task 1"])
    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
    assert "deleted" in result.output.lower() or "removed" in result.output.lower()

    with open(clean_env) as f:
        data = json.load(f)
        assert len(data) == 0


def test_cli_list_with_filters(clean_env):
    runner.invoke(app, ["add", "Task A", "--priority", "high"])
    runner.invoke(app, ["add", "Task B", "--priority", "low"])
    runner.invoke(app, ["complete", "1"])

    # Test filter by status
    result = runner.invoke(app, ["list", "--status", "pending"])
    assert result.exit_code == 0
    assert "Task B" in result.output
    assert "Task A" not in result.output

    # Test filter by priority
    result = runner.invoke(app, ["list", "--priority", "high"])
    assert result.exit_code == 0
    assert "Task A" in result.output
    assert "Task B" not in result.output

    # Test sorting
    result = runner.invoke(app, ["list", "--sort-by", "priority"])
    assert result.exit_code == 0
    out = result.output
    assert out.index("Task A") < out.index("Task B")


def test_cli_search(clean_env):
    runner.invoke(app, ["add", "Buy groceries", "--description", "milk and eggs"])
    runner.invoke(app, ["add", "Walk dog"])

    result = runner.invoke(app, ["search", "milk"])
    assert result.exit_code == 0
    assert "Buy groceries" in result.output
    assert "Walk dog" not in result.output


def test_cli_edit(clean_env):
    runner.invoke(app, ["add", "Old Task", "--priority", "low"])

    result = runner.invoke(
        app, ["edit", "1", "--title", "New Task", "--priority", "high"]
    )
    assert result.exit_code == 0
    assert "Edited task 1" in result.output

    with open(clean_env) as f:
        data = json.load(f)
        assert data[0]["title"] == "New Task"
        assert data[0]["priority"] == "high"
        assert data[0]["status"] == "pending"  # unchanged
