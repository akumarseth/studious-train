from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError
from src.app.api.auth.utils import auth_utils 
from src.db.models.user import User
from fastapi.security import OAuth2PasswordBearer

EXCLUDED_PATHS = [
    ("/", "GET"),
    ("/api/auth/token", "POST"),
    ("/api/auth/register", "POST"),
    ("/api/auth/refresh", "POST"),
    ("/api/open-endpoint", "GET"),
    ("/api/docs", "GET"),
    ("/api/redoc", "GET"),
    ("/api/openapi.json", "GET"),
]

class JWTAuthHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # Check if the path and method are in the excluded paths
        path = request.url.path
        method = request.method

        if any(path == excluded_path and method == excluded_method for excluded_path, excluded_method in EXCLUDED_PATHS):
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        
        if not authorization:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing"},
            )

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                )

            # Verify and decode the token
            payload = auth_utils.verify_access_token(token)
            
            # Retrieve the user from the token
            request.state.user = User(
                id=payload["id"],
                username=payload["username"],
                email=payload["email"],
            )
            
        except (JWTError, ValueError) as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(e)},
            )

        response = await call_next(request)
        return response
