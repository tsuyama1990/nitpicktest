import pytest
import json
from typing import Any
from pathlib import Path
from typer.testing import CliRunner
from todo.cli import app

runner = CliRunner()

@pytest.fixture
def test_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    db_path = tmp_path / "test_todos.json"
    monkeypatch.setenv("TODO_DB_PATH", str(db_path))
    return str(db_path)

def seed_db(db_path: str, data: list[dict[str, Any]]) -> None:
    with open(db_path, "w") as f:
        json.dump(data, f)

def test_uat_02_01_filter_by_status(test_db: str) -> None:
    seed_db(test_db, [
        {"id": 1, "title": "Task A", "status": "pending", "priority": "medium"},
        {"id": 2, "title": "Task B", "status": "completed", "priority": "medium"}
    ])
    result = runner.invoke(app, ["list", "--status", "completed"])
    assert result.exit_code == 0
    assert "Task A" not in result.stdout
    assert "Task B" in result.stdout

def test_uat_02_02_filter_by_priority(test_db: str) -> None:
    seed_db(test_db, [
        {"id": 1, "title": "Task A", "status": "pending", "priority": "low"},
        {"id": 2, "title": "Task B", "status": "pending", "priority": "high"}
    ])
    result = runner.invoke(app, ["list", "--priority", "high"])
    assert result.exit_code == 0
    assert "Task A" not in result.stdout
    assert "Task B" in result.stdout

def test_uat_02_03_search_by_keyword(test_db: str) -> None:
    seed_db(test_db, [
        {"id": 1, "title": "Buy milk", "status": "pending", "priority": "medium"},
        {"id": 2, "title": "Walk the dog", "status": "pending", "priority": "medium"}
    ])
    result = runner.invoke(app, ["search", "milk"])
    assert result.exit_code == 0
    assert "Buy milk" in result.stdout
    assert "Walk the dog" not in result.stdout

def test_uat_02_04_sort_by_priority(test_db: str) -> None:
    seed_db(test_db, [
        {"id": 1, "title": "Task A", "status": "pending", "priority": "low"},
        {"id": 2, "title": "Task B", "status": "pending", "priority": "high"}
    ])
    result = runner.invoke(app, ["list", "--sort-by", "priority"])
    assert result.exit_code == 0
    # Checking that Task B comes before Task A
    assert result.stdout.find("Task B") < result.stdout.find("Task A")

def test_uat_02_05_edit_todo(test_db: str) -> None:
    seed_db(test_db, [
        {"id": 1, "title": "Old Title", "status": "pending", "priority": "low"}
    ])
    result = runner.invoke(app, ["edit", "1", "--title", "New Title", "--priority", "high"])
    assert result.exit_code == 0

    with open(test_db, "r") as f:
        data = json.load(f)
    assert data[0]["title"] == "New Title"
    assert data[0]["priority"] == "high"

def test_e2e_cycle01_commands(test_db: str) -> None:
    # Test ADD
    res = runner.invoke(app, ["add", "New task", "--description", "desc", "--priority", "low"])
    assert res.exit_code == 0

    # Test COMPLETE
    res = runner.invoke(app, ["complete", "1"])
    assert res.exit_code == 0

    with open(test_db, "r") as f:
        data = json.load(f)
    assert data[0]["status"] == "completed"

    # Test DELETE
    res = runner.invoke(app, ["delete", "1"])
    assert res.exit_code == 0

    with open(test_db, "r") as f:
        data = json.load(f)
    assert len(data) == 0
