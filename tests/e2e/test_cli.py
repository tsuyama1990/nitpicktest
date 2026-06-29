from typer.testing import CliRunner
import pytest
from pytest_mock import MockerFixture
from src.todo.cli import app

runner = CliRunner()


@pytest.fixture
def mock_storage(tmp_path: str, mocker: MockerFixture) -> str:
    test_file = f"{tmp_path}/test_todos.json"
    mocker.patch("src.todo.cli.settings.storage_file", test_file)
    return test_file


def test_add_todo(mock_storage: str) -> None:
    result = runner.invoke(app, ["add", "New Task", "--priority", "high"])
    assert result.exit_code == 0
    assert "Added task: 'New Task'" in result.stdout


def test_list_todos(mock_storage: str) -> None:
    runner.invoke(app, ["add", "Task A"])
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Task A" in result.stdout


def test_complete_todo(mock_storage: str) -> None:
    runner.invoke(app, ["add", "Task B"])
    result = runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0
    assert "Marked task 1 as completed" in result.stdout

    list_res = runner.invoke(app, ["list"])
    assert "[x] Task B" in list_res.stdout


def test_delete_todo(mock_storage: str) -> None:
    runner.invoke(app, ["add", "Task C"])
    result = runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
    assert "Deleted task 1" in result.stdout

    list_res = runner.invoke(app, ["list"])
    assert "Task C" not in list_res.stdout


def test_complete_not_found(mock_storage: str) -> None:
    result = runner.invoke(app, ["complete", "999"])
    assert result.exit_code == 1
    # When using stderr, it goes to stderr not stdout unless combined, but runner captures both if not explicitly split? Let's check stderr or stdout.
    # Ah, Typer prints to stderr if err=True, and runner can access it via stderr or just stdout. Wait, runner.invoke captures everything in stdout? No, it captures stderr too? Wait, let's just check the result output (which contains both or is accessible via result.output).
    assert "Task with ID 999 not found" in result.output


def test_delete_not_found(mock_storage: str) -> None:
    result = runner.invoke(app, ["delete", "999"])
    assert result.exit_code == 1
    assert "Task with ID 999 not found" in result.output


def test_search_cmd(mock_storage: str) -> None:
    runner.invoke(app, ["add", "Apples and oranges"])
    runner.invoke(app, ["add", "Bananas"])

    result = runner.invoke(app, ["search", "apple"])
    assert result.exit_code == 0
    assert "Apples and oranges" in result.stdout
    assert "Bananas" not in result.stdout


def test_edit_cmd(mock_storage: str) -> None:
    runner.invoke(app, ["add", "Test Task", "--priority", "low"])

    result = runner.invoke(app, ["edit", "1", "--title", "Updated Task", "--priority", "high"])
    assert result.exit_code == 0
    assert "Updated task 1" in result.stdout

    list_res = runner.invoke(app, ["list"])
    assert "Updated Task" in list_res.stdout
    assert "[high]" in list_res.stdout
    assert "Test Task" not in list_res.stdout


def test_edit_cmd_not_found(mock_storage: str) -> None:
    result = runner.invoke(app, ["edit", "999", "--title", "New Title"])
    assert result.exit_code == 1
    assert "Task with ID 999 not found" in result.output
