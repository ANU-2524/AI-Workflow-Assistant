# fastapi_service/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Task

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return {"tasks": [
        {
            "title": t.title,
            "description": t.description,
            "due_date": t.due_date,
            "priority": t.priority,
            "status": t.status,
            "is_completed": t.is_completed
        } for t in tasks
    ]}
