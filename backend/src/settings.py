import enum
import os
from pathlib import Path
from tempfile import gettempdir
from pydantic.v1 import BaseSettings
from src.config import config

TEMP_DIR = Path(gettempdir())

# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"
    port: int = config.APP_PORT
    # quantity of workers for uvicorn
    workers_count: int = 3
    # Enable uvicorn reloading
    reload: bool = True

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    class Config:
        env_file = ".env"
        env_prefix = "JKTech_API_"
        env_file_encoding = "utf-8"

settings = Settings()