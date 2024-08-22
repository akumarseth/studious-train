import traceback
from typing import Optional

from fastapi import Request
from src.app.utils.exceptions import APIException
from src.settings import settings
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class ExceptionResponseModel(BaseModel):
    success: bool = False
    exception_type: str
    message: str
    stack: Optional[str]


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> JSONResponse:
        try:
            return await call_next(request)
        except APIException as e:
            stack_trace = (
                traceback.format_exc() if settings.environment == "dev" else None
            )
            response = ExceptionResponseModel(
                exception_type=e.__class__.__name__,
                message=e.message,
                stack=stack_trace,
            )
            return JSONResponse(status_code=400, content=response.dict())
        except Exception as e:
            stack_trace = (
                traceback.format_exc() if settings.environment == "dev" else None
            )
            response = ExceptionResponseModel(
                exception_type=e.__class__.__name__, message=str(e), stack=stack_trace
            )
            return JSONResponse(status_code=500, content=response.dict())
