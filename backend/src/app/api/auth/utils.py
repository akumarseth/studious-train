from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from src.config import config

# Secret key and algorithm for JWT
SECRET_KEY =  config.auth["SECRET_KEY"]  # Replace with your actual secret key
ALGORITHM = config.auth["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config.auth["ACCESS_TOKEN_EXPIRE_MINUTES"]
REFRESH_TOKEN_EXPIRE_DAYS = config.auth["REFRESH_TOKEN_EXPIRE_DAYS"]
ISSUER = config.auth["ISSUER"], 
AUDIENCE = config.auth["AUDIENCE"]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthUtils():
    def __init__(self) -> None:
        pass

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        to_encode.update({"iss": ISSUER, "aud": AUDIENCE})

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        to_encode.update({"iss": ISSUER, "aud": AUDIENCE, "type": "refresh"})
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    def verify_access_token(self,token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience=AUDIENCE)
            if payload.get("iss")[0] != ISSUER[0]:
                raise jwt.InvalidIssuerError("Invalid issuer")
            if payload.get("aud")[0] != AUDIENCE[0]:
                raise jwt.InvalidIssuerError("Invalid audience")
            
            # Extract user details from the token
            userid = payload.get("id")
            username = payload.get("username")
            email = payload.get("email")
            role = payload.get("role")

            if userid is None or username is None or email is None or role is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")


    def verify_refresh_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience=AUDIENCE)
            
            if payload.get("type") != "refresh":
                raise jwt.InvalidTokenError("Invalid token type")
            if payload.get("iss")[0] != ISSUER[0]:
                raise jwt.InvalidIssuerError("Invalid issuer")
            if payload.get("aud")[0] != AUDIENCE[0]:
                raise jwt.InvalidIssuerError("Invalid audience")
            
            # Extract user details from the token
            userid = payload.get("id")
            username = payload.get("username")
            email = payload.get("email")
            role = payload.get("role")

            if userid is None or username is None or email is None or role is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token")


    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = self.verify_access_token(token)
            
            username: str = payload.get("username")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        # Replace this with actual user retrieval from the database
        userid = payload.get("id")
        username = payload.get("username")
        email = payload.get("email")
        role = payload.get("role")
        user = {
            "id": userid,
            "username": username,
            "email": email,
            "role": role
            }
        if user is None:
            raise credentials_exception
        return user
    

auth_utils = AuthUtils()
