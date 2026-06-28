import pytest
from pydantic import ValidationError
from datetime import datetime
from src.domain_models import TodoItem, Priority, Status

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
        TodoItem(id=1, title="Test", extra_field="not allowed") # type: ignore

def test_todo_item_invalid_priority():
    with pytest.raises(ValidationError):
        TodoItem(id=1, title="Test", priority="invalid") # type: ignore
