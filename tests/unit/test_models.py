import pytest
from pydantic import ValidationError
from datetime import datetime

from domain_models import TodoItem, Priority, Status


def test_todo_item_valid() -> None:
    item = TodoItem(id=1, title="Test task")
    assert item.id == 1
    assert item.title == "Test task"
    assert item.priority == Priority.MEDIUM
    assert item.status == Status.PENDING


def test_todo_item_invalid_title() -> None:
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="")


def test_todo_item_invalid_extra_fields() -> None:
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="Test task", extra_field="not allowed")  # type: ignore[call-arg]


def test_todo_item_full_valid() -> None:
    dt = datetime(2025, 1, 1, 12, 0)
    item = TodoItem(
        id=2,
        title="Complex task",
        description="A test description",
        priority=Priority.HIGH,
        status=Status.COMPLETED,
        due_date=dt,
    )
    assert item.priority == Priority.HIGH
    assert item.status == Status.COMPLETED
    assert item.due_date == dt
