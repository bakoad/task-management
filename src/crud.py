from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate


class TaskCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        status: str | None = None,
        due_date: str | None = None,
        order_by: str | None = None,
    ) -> list[Task]:
        query = self.db.query(Task)

        if status:
            query = query.filter(Task.status == status)

        if due_date:
            query = query.filter(Task.due_date <= due_date)

        allowed_fields = {"creation_date", "due_date"}
        if order_by:
            direction = "asc"
            if order_by.startswith("-"):
                direction = "desc"
                field_name = order_by[1:]
            else:
                field_name = order_by

            if field_name not in allowed_fields:
                raise ValueError("Invalid field for ordering")

            field = getattr(Task, field_name)
            query = query.order_by(field.desc() if direction == "desc" else field.asc())

        return query.all()


    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create(self, task_data: TaskCreate) -> Task:
        task = Task(**task_data.model_dump())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task_id: int, task_data: TaskUpdate) -> Task | None:
        task = self.get_by_id(task_id)
        if task:
            for key, value in task_data.model_dump().items():
                setattr(task, key, value)
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> Task | None:
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
        return task
