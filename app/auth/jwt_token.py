from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(email: str, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = {"sub": email}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    print(to_encode)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def check_token_valid(token: str = Depends(oauth2_scheme)) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_email = payload.get("sub")

        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return True
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
