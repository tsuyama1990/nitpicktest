from typing import Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class TodoItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    title: str = Field(..., min_length=1)
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    due_date: datetime | None = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
