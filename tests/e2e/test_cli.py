import os
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
