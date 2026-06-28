import pytest
from typer.testing import CliRunner
from pytest_mock import MockerFixture
from src.todo.cli import app
from src.todo.storage import load_todos

runner = CliRunner()


@pytest.fixture
def uat_storage(tmp_path: str, mocker: MockerFixture) -> str:
    test_file = f"{tmp_path}/uat_todos.json"
    mocker.patch("src.todo.cli.settings.storage_file", test_file)
    return test_file


def test_uat_01_01_add_todo(uat_storage: str) -> None:
    # Given the TODO storage is empty (ensured by fixture)
    assert load_todos(uat_storage) == []

    # When I run the CLI command to add a task
    result = runner.invoke(app, ["add", "Buy groceries", "--priority", "high"])
    assert result.exit_code == 0

    # Then the task should be saved with correct properties
    todos = load_todos(uat_storage)
    assert len(todos) == 1
    assert todos[0].title == "Buy groceries"
    assert todos[0].priority.value == "high"
    assert todos[0].status.value == "pending"


def test_uat_01_02_list_todos(uat_storage: str) -> None:
    # Given there are tasks in the system
    runner.invoke(app, ["add", "Task A"])
    runner.invoke(app, ["add", "Task B"])

    # When I run the CLI command to list tasks
    result = runner.invoke(app, ["list"])

    # Then I should see both tasks
    assert result.exit_code == 0
    assert "Task A" in result.stdout
    assert "Task B" in result.stdout


def test_uat_01_03_complete_todo(uat_storage: str) -> None:
    # Given there is a pending task with ID 1
    runner.invoke(app, ["add", "Pending Task"])
    todos_before = load_todos(uat_storage)
    assert todos_before[0].id == 1
    assert todos_before[0].status.value == "pending"

    # When I run the CLI command to complete task 1
    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0

    # Then the status of task 1 should be changed to "completed"
    todos_after = load_todos(uat_storage)
    assert todos_after[0].status.value == "completed"


def test_uat_01_04_delete_todo(uat_storage: str) -> None:
    # Given there is a task with ID 1
    runner.invoke(app, ["add", "Task to delete"])
    assert len(load_todos(uat_storage)) == 1

    # When I run the CLI command to delete task 1
    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0

    # Then task 1 should no longer exist in the system
    assert len(load_todos(uat_storage)) == 0
