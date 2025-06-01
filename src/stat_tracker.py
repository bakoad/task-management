from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from datetime import datetime

from database import SessionLocal, engine
from models import Base
from schemas import Task, TaskCreate, TaskUpdate, Status
from crud import TaskCRUD


class TaskAPIApp:
    def __init__(self):
        self.app = FastAPI(title="Task Management API")
        self._setup_database()
        self._setup_routes()

    def get_app(self):
        return self.app

    def _setup_database(self):
        Base.metadata.create_all(bind=engine)

    def _get_db(self):
        def _get():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
        return _get

    def _setup_routes(self):
        db_dep = Depends(self._get_db())

        @self.app.post("/tasks/", response_model=Task)
        def create_task(task: TaskCreate, db: Session = db_dep):
            return TaskCRUD(db).create(task)

        @self.app.get("/tasks/", response_model=list[Task])
        def list_tasks(
            due_date: datetime | None = None,
            status: Status | None = None,
            order_by: str | None = Query(
                None,
                description="Sort by 'creation_date' or 'due_date'. Prefix with '-' for descending.",
                enum=["creation_date", "-creation_date", "due_date", "-due_date"]
            ),
            db: Session = db_dep,
        ):
            return TaskCRUD(db).get_all(status=status, due_date=due_date, order_by=order_by)

        @self.app.get("/tasks/{task_id}", response_model=Task)
        def get_task(task_id: int, db: Session = db_dep):
            task = TaskCRUD(db).get_by_id(task_id)
            if task is None:
                raise HTTPException(status_code=404, detail="Task not found")
            return task

        @self.app.put("/tasks/{task_id}", response_model=Task)
        def update_task(task_id: int, task: TaskUpdate, db: Session = db_dep):
            updated = TaskCRUD(db).update(task_id, task)
            if updated is None:
                raise HTTPException(status_code=404, detail="Task not found")
            return updated

        @self.app.delete("/tasks/{task_id}")
        def delete_task(task_id: int, db: Session = db_dep):
            deleted = TaskCRUD(db).delete(task_id)
            if deleted is None:
                raise HTTPException(status_code=404, detail="Task not found")
            return {"detail": "Task deleted"}

app_instance = TaskAPIApp()

app = app_instance.get_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("stat_tracker:app", host="0.0.0.0", port=8000, reload=True)
