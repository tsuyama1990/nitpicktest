from typer.testing import CliRunner
import pytest
from pytest_mock import MockerFixture
from dev_src.todo.cli import app
from dev_src.todo.storage import save_todos
from dev_src.domain_models.todo import TodoItem, Priority, Status

runner = CliRunner()


@pytest.fixture
def mock_storage(tmp_path: str, mocker: MockerFixture) -> str:
    test_file = f"{tmp_path}/test_todos.json"
    mocker.patch("dev_src.todo.cli.settings.storage_file", test_file)
    return test_file


def test_uat_02_01_filter_by_status(mock_storage: str) -> None:
    todos = [
        TodoItem(id=1, title="Task A", status=Status.PENDING),
        TodoItem(id=2, title="Task B", status=Status.COMPLETED),
    ]
    save_todos(mock_storage, todos)

    result = runner.invoke(app, ["list", "--status", "completed"])
    assert result.exit_code == 0
    assert "Task B" in result.stdout
    assert "Task A" not in result.stdout


def test_uat_02_02_filter_by_priority(mock_storage: str) -> None:
    todos = [
        TodoItem(id=1, title="Task A", priority=Priority.LOW),
        TodoItem(id=2, title="Task B", priority=Priority.HIGH),
    ]
    save_todos(mock_storage, todos)

    result = runner.invoke(app, ["list", "--priority", "high"])
    assert result.exit_code == 0
    assert "Task B" in result.stdout
    assert "Task A" not in result.stdout


def test_uat_02_03_search(mock_storage: str) -> None:
    todos = [
        TodoItem(id=1, title="Buy milk"),
        TodoItem(id=2, title="Walk the dog"),
    ]
    save_todos(mock_storage, todos)

    result = runner.invoke(app, ["search", "milk"])
    assert result.exit_code == 0
    assert "Buy milk" in result.stdout
    assert "Walk the dog" not in result.stdout


def test_uat_02_04_sort_by_priority(mock_storage: str) -> None:
    todos = [
        TodoItem(id=1, title="Task A", priority=Priority.LOW),
        TodoItem(id=2, title="Task B", priority=Priority.HIGH),
    ]
    save_todos(mock_storage, todos)

    result = runner.invoke(app, ["list", "--sort-by", "priority"])
    assert result.exit_code == 0

    out = result.stdout
    idx_b = out.find("Task B")
    idx_a = out.find("Task A")
    assert idx_b < idx_a


def test_uat_02_05_edit_task(mock_storage: str) -> None:
    todos = [
        TodoItem(id=1, title="Old Title", priority=Priority.LOW),
    ]
    save_todos(mock_storage, todos)

    result = runner.invoke(app, ["edit", "1", "--title", "New Title", "--priority", "high"])
    assert result.exit_code == 0
    assert "Updated task 1" in result.stdout

    list_res = runner.invoke(app, ["list"])
    assert "New Title" in list_res.stdout
    assert "[high]" in list_res.stdout
