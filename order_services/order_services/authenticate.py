from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from fastapi import Depends , HTTPException , status
import os
from fastapi.security import HTTPBearer
# from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime , timedelta


SECRET_KEY = os.environ.get("SECRET_KEY" , "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")   
ALGORITHM = os.environ.get("ALGORITHM" , "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 10

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8002/docs/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
