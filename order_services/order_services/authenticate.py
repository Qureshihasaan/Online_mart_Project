# # from fastapi.security import OAuth2PasswordBearer
# from jose import jwt , JWTError
# from fastapi import Depends , HTTPException , status , Header
# # from typing import Annotated
# import os
# from typing import Optional
# from datetime import datetime, timedelta
# from fastapi.security import OAuth2PasswordBearer
# # from passlib.context import CryptContext
# from pydantic import BaseModel

# SECRET_KEY = os.environ.get("SECRET_KEY")   
# ALGORITHM = os.environ.get("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = 10

# def create_access_token(username : str , user_id : int , expires_delta : timedelta):
#     encode = {"sub" : username, "id" : user_id}
#     expires = datetime.utcnow() + expires_delta
#     encode.update({"exp" : expires})
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# def decode_access_token(access_token : str):
#     decoded_jwt = jwt.decode(access_token , SECRET_KEY , algorithms=[ALGORITHM])
#     return decoded_jwt



# def verify_access_token(token:str):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     return payload
    


