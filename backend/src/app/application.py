import toml
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import UJSONResponse
from src.app.api.router import api_router
from src.app.lifetime import (
    register_shutdown_event,
    register_startup_event,
)
from src.app.midddlewares import ExceptionHandlerMiddleware, JWTAuthHandlerMiddleware
from src.app.midddlewares.exception import ExceptionResponseModel
from src.logging import configure_logging


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    file_path = "pyproject.toml"

    with open(file_path, "r") as toml_file:
        data = toml.loads(toml_file.read())

    app = FastAPI(
        title="JKTech Service",
        version=data["tool"]["poetry"]["version"],
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        openapi_schema = {
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            },
            "security": [
                {"BearerAuth": []}
            ]
        }
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Adding app middlewares
    # app.add_middleware(JWTAuthHandlerMiddleware)
    app.add_middleware(ExceptionHandlerMiddleware)
    
    # Main router for the API.
    app.include_router(
        router=api_router,
        prefix="/api",
        responses={
            400: {
                "model": ExceptionResponseModel,
                "description": "Bad Request",
            },
            500: {
                "model": ExceptionResponseModel,
                "description": "Internal Server Error",
            },
        },
    )

    return app
