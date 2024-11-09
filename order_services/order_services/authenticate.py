from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from fastapi import Depends , HTTPException , status
from typing import Annotated
import os
from typing import Optional
from datetime import datetime, timedelta

SECRET_KEY = os.environ.get("SECRET_KEY")   
ALGORITHM = os.environ.get("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token : Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str|None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
    #     return payload
    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Token has expired")
    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Invalid token...")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = verify_token(token)
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token....")
#         return user_id
    
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid token.")

def verify_refresh_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None