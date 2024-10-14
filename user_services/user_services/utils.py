from datetime import datetime , timedelta
from jose import jwt
import os
from typing import Optional



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Secret_Key = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_access_token(username : str , user_id : int , expires_delta : timedelta):
    encode = {"sub" : username, "id" : user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp" : expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(access_token : str):
    decoded_jwt = jwt.decode(access_token , SECRET_KEY , algorithms=[ALGORITHM])
    return decoded_jwt



def verify_access_token(token:str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
    