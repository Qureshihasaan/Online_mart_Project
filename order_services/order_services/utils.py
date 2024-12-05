# from passlib.context import CryptContext
# from typing import Annotated 
# from .database import get_db
# from sqlmodel import Session
# from fastapi import Depends
# from sqlmodel import SQLModel

# bcrypt_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")


# class User(SQLModel):
#     username : str
#     email : str
#     hashed_password : str


# class Token(SQLModel):
#     access_token : str
#     token_type : str


# def authenticate_user(username : str , password :str , db : Annotated[Session,Depends(get_db)]):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         return False
#     if not bcrypt_context.verify(password, user.hashed_password):
#         return False
#     return user
