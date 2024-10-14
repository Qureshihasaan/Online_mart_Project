from passlib.context import CryptContext
from typing import Annotated 
from .model import User
from .database import get_session
from sqlmodel import Session
from fastapi import Depends

bcrypt_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")


def authenticate_user(username : str , password :str , db : Annotated[Session,Depends(get_session)]):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


