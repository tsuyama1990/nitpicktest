import pytest
from pydantic import ValidationError

from src.domain_models.todo import TodoItem, Priority, Status


def test_todo_item_valid():
    item = TodoItem(
        id=1, title="Test task", priority=Priority.HIGH, status=Status.COMPLETED
    )
    assert item.id == 1
    assert item.title == "Test task"
    assert item.priority == Priority.HIGH
    assert item.status == Status.COMPLETED
    assert item.description is None
    assert item.due_date is None


def test_todo_item_defaults():
    item = TodoItem(id=2, title="Another test")
    assert item.priority == Priority.MEDIUM
    assert item.status == Status.PENDING


def test_todo_item_invalid_title():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="")


def test_todo_item_extra_fields():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="Test", extra_field="not allowed")  # type: ignore[call-arg]


def test_todo_item_invalid_enum():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="Test", priority="urgent")  # type: ignore[arg-type]
