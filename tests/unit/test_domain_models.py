import pytest
from pydantic import ValidationError
from src.domain_models import TodoItem, Priority, Status, TodoUpdate


def test_todo_item_valid():
    item = TodoItem(id=1, title="Test task", priority=Priority.HIGH)
    assert item.id == 1
    assert item.title == "Test task"
    assert item.priority == Priority.HIGH
    assert item.status == Status.PENDING


def test_todo_item_invalid_empty_title():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="")


def test_todo_item_extra_fields():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="Test", extra_field="not allowed")  # type: ignore


def test_todo_item_invalid_priority():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="Test", priority="invalid")  # type: ignore


def test_todo_update_valid_partial():
    update = TodoUpdate(title="New Title", priority=Priority.LOW)
    assert update.title == "New Title"
    assert update.priority == Priority.LOW
    assert update.description is None


def test_todo_update_empty():
    update = TodoUpdate()
    assert update.title is None
    assert update.description is None
    assert update.priority is None
    assert update.status is None
    assert update.due_date is None


def test_todo_update_invalid_empty_title():
    with pytest.raises(ValidationError):
        TodoUpdate(title="")


def test_todo_update_extra_fields():
    with pytest.raises(ValidationError):
        TodoUpdate(extra_field="not allowed")  # type: ignore
