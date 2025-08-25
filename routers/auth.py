from fastapi import APIRouter,Depends
from db import SessionLocal
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models


router=APIRouter()



class createuserrequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role:str 


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/auth",status_code=201)
async def creat_user(db: Annotated[Session, Depends(get_db)],
                        createuserrequest: createuserrequest):
    creat_user_model= models.User(
        username=createuserrequest.username,
        email=createuserrequest.email,
        first_name=createuserrequest.first_name,
        last_name=createuserrequest.last_name,
        hashed_password=createuserrequest.password,  # In a real app, hash the password
        role=createuserrequest.role
    )
    db.add(creat_user_model)
    db.commit()

@router.get("/auth")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.query(models.User).all()
    return users

  

