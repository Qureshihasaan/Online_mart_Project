from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer
from datetime import timedelta
from fastapi import Depends, FastAPI , HTTPException ,status
from typing import AsyncGenerator, Annotated , Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_access_token
from .schema import bcrypt_context , authenticate_user
from .consumer import consume
from .producer import kafka_producer
from .database import create_db_and_tables , get_session
import asyncio
from .model import User, CreateUser , Token 
from sqlmodel import Session , select
import json
from jose import JWTError
from psycopg2 import IntegrityError
from . import setting



@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None,None]:
    print("Creating Tables...")
    task = asyncio.create_task(consume(
            # setting.KAFKA_USER_TOPIC,
            # setting.BOOTSTRAP_SERVER
            )
    )
    create_db_and_tables()
    yield


app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/Signup" , status_code=status.HTTP_201_CREATED)
async def create_user(user : CreateUser,
                      db : Annotated[Session, Depends(get_session)]
                      )->dict:
    if not user.username or not user.plain_password:
        raise HTTPException(status_code=400 , detail="Please Enter Username or Password....")
    create_user = User(
        username = user.username,
        email = user.email,
        hashed_password = bcrypt_context.hash(user.plain_password),
    )
    db.add(create_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400 , detail="User Already Exists...")
    user_created_event={
        "event_type":"UserCreated",
        "username" :  user.username,
        "email" : user.email
    }
    return {"message" : "User Account Created Successfully"}    




@app.post("/token" , response_model=Token)
async def login_with_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],
                           db : Annotated[Session, Depends(get_session)]
                           )->Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could Not Validate User")
    token = create_access_token(user.username, user.id , timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token" : token, "token_type" : "bearer"}

# @app.post("/token" , response_model=Token)
# async def login_with_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],
#                            db : Annotated[Session, Depends(get_session)]
#                            ):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
#     token = create_access_token(user.username, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     return {"access_token" : token, "token_type" : "bearer"}

@app.get("/get_access_token")
def get_access_token(username :str , user_id : Optional[int] = None):
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
       username, user_id , expires_delta=access_token_expire
    )
    return {"access_token" : access_token}


@app.get("/decode_token")
def decode_token(access_token:str):
    try:
        decode_token = decode_access_token(access_token)
        return {"decode_token" : decode_token}
    except JWTError as e:
        return {"error" : str(e)}
   

@app.get("/user/all")
def get_all_user(db:Annotated[Session,Depends(get_session)]):
    user = db.exec(select(User)).all()
    return user

@app.get("/user/me")
def read_user(token : Annotated[str, Depends(oauth2_scheme)], db : Annotated[Session, Depends(get_session)]):
    user_token_data = decode_access_token(token)
    user = db.exec(select(User).where(User.username == user_token_data["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/user/delete/{user_id}")
async def delete_user(user_id : int, db : Annotated[Session, Depends(get_session)]):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message" : "User Deleted Successfully"}