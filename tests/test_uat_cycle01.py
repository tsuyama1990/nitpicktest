import pytest
from typer.testing import CliRunner
from todo.cli import app
from todo.storage import load_todos
from domain_models import Status

runner = CliRunner()


@pytest.fixture
def empty_storage(tmp_path, monkeypatch):
    storage_file = tmp_path / "uat_todos.json"
    monkeypatch.setenv("STORAGE_PATH", str(storage_file))
    return str(storage_file)


def test_uat_01_01_add_todo(empty_storage):
    """
    Scenario: Adding a basic task
    Given the TODO storage is empty
    When I run the CLI command to add a task with title "Buy groceries" and priority "high"
    Then the task "Buy groceries" should be saved in the system
    And its status should be "pending"
    And its priority should be "high"
    """
    result = runner.invoke(app, ["add", "Buy groceries", "--priority", "high"])
    assert result.exit_code == 0

    todos = load_todos(empty_storage)
    assert len(todos) == 1
    task = todos[0]
    assert task.title == "Buy groceries"
    assert task.status == Status.PENDING
    assert task.priority.value == "high"


def test_uat_01_02_list_todos(empty_storage):
    """
    Scenario: Listing existing tasks
    Given there are tasks "Task A" and "Task B" in the system
    When I run the CLI command to list tasks
    Then I should see both "Task A" and "Task B" in the output
    """
    runner.invoke(app, ["add", "Task A"])
    runner.invoke(app, ["add", "Task B"])

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Task A" in result.output
    assert "Task B" in result.output


def test_uat_01_03_complete_todo(empty_storage):
    """
    Scenario: Completing a pending task
    Given there is a pending task with ID 1
    When I run the CLI command to complete task 1
    Then the status of task 1 should be changed to "completed"
    """
    runner.invoke(app, ["add", "Pending Task"])

    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0

    todos = load_todos(empty_storage)
    assert len(todos) == 1
    assert todos[0].status == Status.COMPLETED


def test_uat_01_04_delete_todo(empty_storage):
    """
    Scenario: Deleting an existing task
    Given there is a task with ID 1
    When I run the CLI command to delete task 1
    Then task 1 should no longer exist in the system
    """
    runner.invoke(app, ["add", "Task to delete"])

    todos_before = load_todos(empty_storage)
    assert len(todos_before) == 1

    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0

    todos_after = load_todos(empty_storage)
    assert len(todos_after) == 0
