from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum


class Status(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: date
    status: Status

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    creation_date: datetime

    class Config:
        orm_mode = True
