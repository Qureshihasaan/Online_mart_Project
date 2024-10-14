from sqlmodel import SQLModel ,Field
from typing import Optional
from pydantic import EmailStr

class User(SQLModel , table = True):
    id : Optional[int] = Field(default=None , primary_key=True, index=True)
    username : str = Field(index=True , unique=True , nullable=False)
    email : EmailStr = Field(index=True, nullable=False , unique=True)
    hashed_password : str


class CreateUser(SQLModel):
    username : str 
    email : EmailStr
    plain_password : str


class Token(SQLModel):
    access_token : str
    token_type : str


# class User(SQLModel , table= True):
#     id : Optional[int] = Field(default=None , primary_key=True , index=True)
#     user_name : str =  Field(index=True , unique=True , nullable=False)
#     email : EmailStr =  Field(index=True , unique=True , nullable=False)
#     hashed_password : str


# class Usercreate(SQLModel):
#     username : str
#     password : str

 
# class Token(SQLModel):
#     acess_token : str
#     token_type : str