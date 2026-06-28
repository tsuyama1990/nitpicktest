import pytest
from pydantic import ValidationError
from domain_models import TodoItem, Priority, Status


def test_todo_item_valid():
    item = TodoItem(id=1, title="Test task")
    assert item.id == 1
    assert item.title == "Test task"
    assert item.priority == Priority.MEDIUM
    assert item.status == Status.PENDING


def test_todo_item_invalid_empty_title():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="")


def test_todo_item_all_fields():
    from datetime import datetime

    now = datetime.now()
    item = TodoItem(
        id=2,
        title="Full task",
        description="Desc",
        priority=Priority.HIGH,
        status=Status.COMPLETED,
        due_date=now,
    )
    assert item.priority == Priority.HIGH
    assert item.status == Status.COMPLETED
    assert item.description == "Desc"
    assert item.due_date == now


def test_todo_item_extra_fields():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="Task", extra_field="not allowed")  # type: ignore
