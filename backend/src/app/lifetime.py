import asyncio
import random
from typing import Awaitable, Callable, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from src.settings import settings

from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import subprocess

# from src.config import config
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.db.connection import init_db, create_db_pool, close_db_pool, engine

def register_startup_event(app: FastAPI,) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:
        await init_db()  # Initialize the database schema
        await create_db_pool()
        try:
            subprocess.Popen('ollama serve', shell=True)
            print("Ollama server is running")
        except Exception as e:
            print("Error runing Ollama server")
            print(e)
    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await close_db_pool()
        await engine.dispose()

    return _shutdown
