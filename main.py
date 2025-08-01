from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
import models
from db import SessionLocal
from db import engine, Base

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depends = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db: db_depends):
    todos = db.query(models.Todos).all()
    return todos
    

