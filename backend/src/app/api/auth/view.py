from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.app.api.auth.utils import auth_utils
from src.db.connection import aget_connection, release_connection


router = APIRouter()

@router.post("/register")
async def register(username: str, email: str, password: str):
    conn = await aget_connection()
    try:
        # Check if user already exists
        result = await conn.fetchrow("SELECT id FROM jktech.users WHERE username = $1", username)
        if result:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Insert new user
        hashed_password = auth_utils.get_password_hash(password)
        await conn.execute(
            "INSERT INTO jktech.users (username, email, hashed_password) VALUES ($1, $2, $3)",
            username, email, hashed_password
        )
        return {"msg": "User registered successfully"}
    finally:
        await release_connection(conn)


@router.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = await aget_connection()
    try:
        # Fetch the user details from the database
        user = await conn.fetchrow(
            "SELECT id, username, email, hashed_password FROM jktech.users WHERE username = $1",
            form_data.username
        )
        if not user or not auth_utils.verify_password(form_data.password, user['hashed_password']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last_login_time for the user
        await conn.execute(
            "UPDATE jktech.users SET last_login_time = CURRENT_TIMESTAMP WHERE id = $1",
            user['id']
        )

        # Create the access and refresh tokens
        # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = auth_utils.create_access_token(
            data={
                "id":user["id"],
                "username":user["username"],
                "email":user["email"],
                "role":'user'}
        )
        
        refresh_token = auth_utils.create_refresh_token(
            data={
                "id":user["id"],
                "username":user["username"],
                "email":user["email"],
                "role":'user'}
        )

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    finally:
        await release_connection(conn)


@router.post("/refresh", response_model=dict)
async def refresh_token(refresh_token: str):
    try:
        payload = auth_utils.verify_refresh_token(refresh_token)

        new_access_token = auth_utils.create_access_token(
            data={
                "id":payload.get("id"),
                "username":payload.get("username"),
                "email":payload.get("email"),
                "role":payload.get("role")}
        )
        
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

