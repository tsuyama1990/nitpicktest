import pytest
from pydantic import ValidationError
from datetime import datetime
from dev_src.domain_models.todo import TodoItem, Priority, Status


def test_todo_item_valid() -> None:
    item = TodoItem(
        id=1,
        title="Test Task",
        description="A task description",
        priority=Priority.HIGH,
        status=Status.PENDING,
        due_date=datetime(2025, 1, 1),
    )
    assert item.id == 1
    assert item.title == "Test Task"
    assert item.priority == Priority.HIGH
    assert item.status == Status.PENDING


def test_todo_item_default_values() -> None:
    item = TodoItem(id=1, title="Test Task")
    assert item.priority == Priority.MEDIUM
    assert item.status == Status.PENDING
    assert item.description is None
    assert item.due_date is None


def test_todo_item_invalid_title() -> None:
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="")


def test_todo_item_extra_fields_forbidden() -> None:
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="Test", extra_field="should fail")  # type: ignore[call-arg]
