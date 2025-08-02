from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
import models
from db import SessionLocal
from db import engine, Base
from pydantic import BaseModel

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depends = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str
    description: str | None = None
    Priority: int | None = None
    completed: bool = False


@app.get("/")
async def read_all(db: db_depends):
    todos = db.query(models.Todos).all()
    return todos
    

@app.get("/todos/{todo_id}")
async def read_todo(todo_id: int, db: db_depends):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo is None:
        return {"error": "Todo not found"}
    return todo

@app.post("/todos/")
async def create_todo(todo: TodoRequest, db: db_depends):
    new_todo = models.Todos(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: TodoRequest, db: db_depends):
    existing_todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if existing_todo is None:
        return {"error": "Todo not found"}
    
    for key, value in todo.dict().items():
        setattr(existing_todo, key, value)
    
    db.commit()
    db.refresh(existing_todo)
    return existing_todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: db_depends):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo is None:
        return {"error": "Todo not found"}
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}