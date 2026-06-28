import json
from typer.testing import CliRunner
from src.todo.cli import app
import pytest

runner = CliRunner()


@pytest.fixture
def clean_env(tmp_path, monkeypatch):
    db_path = str(tmp_path / "todos_uat_cycle02.json")
    monkeypatch.setenv("TODO_DB_PATH", db_path)
    return db_path


def test_uat_02_01_filter_by_status(clean_env):
    """
    Scenario: Filtering by completed status
      Given there is a pending task "Task A" and a completed task "Task B"
      When I run the CLI command to list tasks with status "completed"
      Then I should only see "Task B" in the output
    """
    runner.invoke(app, ["add", "Task A"])
    runner.invoke(app, ["add", "Task B"])
    runner.invoke(app, ["complete", "2"])

    result = runner.invoke(app, ["list", "--status", "completed"])
    assert result.exit_code == 0
    assert "Task B" in result.output
    assert "Task A" not in result.output


def test_uat_02_02_filter_by_priority(clean_env):
    """
    Scenario: Filtering by high priority
      Given there is a low priority task "Task A" and a high priority task "Task B"
      When I run the CLI command to list tasks with priority "high"
      Then I should only see "Task B" in the output
    """
    runner.invoke(app, ["add", "Task A", "--priority", "low"])
    runner.invoke(app, ["add", "Task B", "--priority", "high"])

    result = runner.invoke(app, ["list", "--priority", "high"])
    assert result.exit_code == 0
    assert "Task B" in result.output
    assert "Task A" not in result.output


def test_uat_02_03_search_keyword(clean_env):
    """
    Scenario: Searching by keyword
      Given there is a task with title "Buy milk" and a task with title "Walk the dog"
      When I run the CLI command to search for "milk"
      Then I should only see "Buy milk" in the output
    """
    runner.invoke(app, ["add", "Buy milk"])
    runner.invoke(app, ["add", "Walk the dog"])

    result = runner.invoke(app, ["search", "milk"])
    assert result.exit_code == 0
    assert "Buy milk" in result.output
    assert "Walk the dog" not in result.output


def test_uat_02_04_sort_by_priority(clean_env):
    """
    Scenario: Sorting by priority
      Given there is a low priority task "Task A" and a high priority task "Task B"
      When I run the CLI command to list tasks sorted by priority
      Then I should see "Task B" before "Task A" in the output
    """
    runner.invoke(app, ["add", "Task A", "--priority", "low"])
    runner.invoke(app, ["add", "Task B", "--priority", "high"])

    result = runner.invoke(app, ["list", "--sort-by", "priority"])
    assert result.exit_code == 0
    out = result.output
    assert out.index("Task B") < out.index("Task A")


def test_uat_02_05_edit_item(clean_env):
    """
    Scenario: Editing task title and priority
      Given there is a task with ID 1, title "Old Title", and priority "low"
      When I run the CLI command to edit task 1 with title "New Title" and priority "high"
      Then the task with ID 1 should have title "New Title" and priority "high"
    """
    runner.invoke(app, ["add", "Old Title", "--priority", "low"])

    result = runner.invoke(
        app, ["edit", "1", "--title", "New Title", "--priority", "high"]
    )
    assert result.exit_code == 0

    with open(clean_env) as f:
        data = json.load(f)
        assert data[0]["title"] == "New Title"
        assert data[0]["priority"] == "high"
