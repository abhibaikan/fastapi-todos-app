from fastapi import Depends, FastAPI
import models
from db import SessionLocal,engine, Base
from routers import auth,todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(todos.router, prefix="/todos", tags=["todos"])

